"""Curated dataset definition for `gse40279_methylation_age` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import gzip
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.csv as pacsv
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Grouping, Metric, TaskSummary, decode

MATRIX = "GSE40279_series_matrix.txt.gz"
"""GEO's series matrix: the sample characteristics in `!Sample_*` lines, then one row per probe, one column per sample."""

SIGNALS = "GSE40279_signal_intensities.txt.gz"
"""BeadStudio's export: per probe and sample the average beta and the two signals (`<sentrix>.AVG_Beta`, ...)."""

SAMPLE_KEY = "GSE40279_sample_key.txt.gz"
"""The array position (Sentrix barcode) of each sample number; it names the sample columns of the signal file."""

IMPUTED = "imputed_cells.parquet"
"""Written by `_prepare_raw_files`: the cells where the deposit is not BeadStudio's per-sample beta."""

N_PROBES = 473_034
"""Probes per sample in the deposit (`!Sample_data_row_count`): the paper's QC subset of the 485,577 on the array."""

TOLERANCE = 1e-6
"""Both files write the betas with 7 significant digits; a cell differs when its two values differ by more."""

CHARACTERISTICS = {"age (y)": "age", "source": "site", "plate": "plate", "gender": "sex", "ethnicity": "ethnicity"}
"""The GEO sample characteristics we read (`!Sample_characteristics_ch1`, `key: value`), and their column names."""

SEX = {"F": "female", "M": "male"}


def _end_marker(row) -> str:
    """Skip the matrix's closing line `!series_matrix_table_end`; any other malformed row is an error."""
    if row.text.startswith("!series_matrix_table_end"):
        return "skip"
    return "error"


def read_matrix_parts(path: Path) -> tuple[dict[str, list[str]], pa.Table]:
    """The series matrix as its sample lines and its probe table.

    The sample lines are keyed by field (`geo_accession`, `source_name_ch1`) or, for a characteristic, by its key
    (`age (y)`), one value per sample; the table has 473,034 rows, `ID_REF` and one column per sample accession.
    """
    header: dict[str, list[str]] = {}
    with gzip.open(path, "rb") as fh:
        for raw_line in fh:
            line = raw_line.decode()
            if line.startswith("!series_matrix_table_begin"):
                break
            if not line.startswith("!Sample_"):
                continue
            field, *values = (v.strip('"') for v in line.rstrip("\n").split("\t"))
            if field == "!Sample_characteristics_ch1":
                key = values[0].split(": ", 1)[0]
                assert all(v.startswith(f"{key}: ") for v in values), key
                header[key] = [v.split(": ", 1)[1] for v in values]
            else:
                header[field.removeprefix("!Sample_")] = values
        table = pacsv.read_csv(fh, parse_options=pacsv.ParseOptions(delimiter="\t", invalid_row_handler=_end_marker))
    assert table.column_names[1:] == header["geo_accession"], "the table's columns are not the samples of the header"
    assert table.num_rows == N_PROBES, table.num_rows
    return header, table


def read_series_matrix(path: Path) -> pd.DataFrame:
    """One row per sample: the GEO accession as index, the characteristics, then one float column per probe.

    The probe table is transposed once into a single float64 block of 656 x 473,034 values.
    """
    header, table = read_matrix_parts(path)
    accessions = header["geo_accession"]
    values = np.column_stack([table.column(gsm).to_numpy() for gsm in accessions]).T  # samples x probes
    meta = pd.DataFrame({CHARACTERISTICS[key]: header[key] for key in CHARACTERISTICS}, index=accessions)
    meta["tissue"] = header["tissue"]
    beta = pd.DataFrame(values, index=accessions, columns=table.column("ID_REF").to_pylist())
    return pd.concat([meta, beta], axis=1)


def find_imputed_cells(raw_dir: Path) -> pd.DataFrame:
    """The cells of the deposit that are not BeadStudio's per-sample beta: blank in its export, or changed.

    The signal file holds BeadStudio's `AVG_Beta` of all 485,577 probes and every sample, which is max(B, 0) / (A + B +
    100) of the sample's own two signals. The paper set a beta with a detection p-value above 0.01 to missing and
    imputed the missing ones by KNN over the markers (Experimental Procedures, "Sample collection"); a deposited cell
    that differs from BeadStudio's, or where BeadStudio left the cell blank, is such an imputed value.
    """
    header, table = read_matrix_parts(raw_dir / MATRIX)
    accessions = header["geo_accession"]
    key = pd.read_csv(raw_dir / SAMPLE_KEY, sep="\t", header=None, names=["index", "sample", "sentrix"], dtype=str)
    sentrix = dict(zip("X" + key["sample"], key["sentrix"], strict=True))
    column_of = {sentrix[name]: j for j, name in enumerate(header["source_name_ch1"])}
    row_of = {probe: i for i, probe in enumerate(table.column("ID_REF").to_pylist())}
    deposit = np.column_stack([table.column(gsm).to_numpy() for gsm in accessions])  # probes x samples
    del table
    with gzip.open(raw_dir / SIGNALS, "rt") as fh:
        names = fh.readline().rstrip("\n").split("\t")
    floats = {
        name: pa.float64()
        for name in names
        if name.rsplit(".", 1)[-1] in {"AVG_Beta", "Intensity", "SignalA", "SignalB"}
    }
    reader = pacsv.open_csv(
        raw_dir / SIGNALS,
        read_options=pacsv.ReadOptions(block_size=1 << 26),
        parse_options=pacsv.ParseOptions(delimiter="\t"),
        convert_options=pacsv.ConvertOptions(
            column_types={**floats, "TargetID": pa.string()}, null_values=["", " "], strings_can_be_null=True
        ),
    )
    found, matched = [], 0
    for batch in reader:
        targets = np.asarray(batch.column("TargetID").to_pylist(), dtype=object)
        rows = np.array([row_of.get(t, -1) for t in targets])
        keep = rows >= 0
        matched += int(keep.sum())
        for name in names:
            if not name.endswith(".AVG_Beta"):
                continue
            j = column_of[name.removesuffix(".AVG_Beta")]
            beadstudio = batch.column(name).to_numpy(zero_copy_only=False)[keep]
            deposited = deposit[rows[keep], j]
            changed = np.flatnonzero(np.isnan(beadstudio) | (np.abs(deposited - beadstudio) > TOLERANCE))
            found.append(
                pd.DataFrame(
                    {
                        "probe": targets[keep][changed],
                        "sample": accessions[j],
                        "deposited": deposited[changed],
                        "beadstudio": beadstudio[changed],
                    }
                )
            )
    assert matched == N_PROBES, f"{matched} of the deposit's {N_PROBES} probes are in the signal file"
    cells = pd.concat(found, ignore_index=True)
    return cells.sort_values(["sample", "probe"], kind="stable", ignore_index=True)


def plate_table(meta: pd.DataFrame) -> pd.DataFrame:
    """Per plate: the samples, their age, the Hispanic share and the recruitment sites (from the raw characteristics)."""
    m = meta.assign(age=meta["age"].astype(int), hispanic=meta["ethnicity"].str.startswith("Hispanic"))
    return (
        m.groupby(m["plate"].astype(int))
        .agg(
            samples=("age", "size"),
            mean_age=("age", "mean"),
            min_age=("age", "min"),
            max_age=("age", "max"),
            hispanic=("hispanic", "sum"),
            sites=("site", lambda s: ", ".join(sorted(set(s)))),
        )
        .round(1)
    )


class Gse40279MethylationAge(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How old is a person, in years, judged from the DNA methylation of their blood?",
        use_case=(
            "An aging study reads a person's age predicted from blood against their real age, as an aging rate "
            "(an epigenetic clock); second, and only approximately, a forensic lab estimating an unknown donor's age "
            "(such labs use panels of a few sites and do not know a recorded ethnicity). The paper names both uses."
        ),
        row=(
            "One person's whole-blood sample, measured on the Illumina 450K methylation array (656 adults aged 19 to "
            "101, from four US recruitment sites, run on nine plates)."
        ),
        predicted="The person's chronological age in whole years at blood draw.",
        known=(
            "The methylation level (0 to 1) at 473,034 sites of the genome in that blood sample, and the person's "
            "sex and recorded ethnicity."
        ),
        split=(
            "Whole processing plates are held out, so each test sample was measured in a batch the model never saw, "
            "as a lab's new samples are."
        ),
        changes=(
            "We hold out whole plates rather than random people, leave the recruitment site out of the inputs, and "
            "set the 0.14% of values the authors had imputed back to missing."
        ),
        fit="direct",
        fit_reason=(
            "The inputs are what an aging study's clock reads from a blood array, and new samples come from a batch not in "
            "training. The plates differ in age (mean 38.5 to 76.2 years) and ethnicity, so a test fold is also a "
            "shift in cohort."
        ),
    )

    # Dataset
    unique_name = "gse40279_methylation_age"
    year = "2012"
    domain = "biology & life sciences"
    # GEO (NCBI) series of the paper, public on 2012-11-21, the day the paper went online
    source = "Other"
    source_url = "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE40279"
    license = (
        "None stated on the series; GEO's disclaimer: NCBI places no restrictions on the use or distribution of GEO "
        "data, though submitters may claim rights (https://www.ncbi.nlm.nih.gov/geo/info/disclaimer.html)"
    )
    download_description = """
        The GEO series GSE40279 (Hannum et al. 2013) from NCBI's FTP server: the series matrix (1.2 GB), BeadStudio's
        signal file (5.0 GB) and the sample key (4.5 KB).

        mkdir -p local-data-warehouse/gse40279_methylation_age && cd local-data-warehouse/gse40279_methylation_age
        wget https://ftp.ncbi.nlm.nih.gov/geo/series/GSE40nnn/GSE40279/matrix/GSE40279_series_matrix.txt.gz
        wget https://ftp.ncbi.nlm.nih.gov/geo/series/GSE40nnn/GSE40279/suppl/GSE40279_signal_intensities.txt.gz
        wget https://ftp.ncbi.nlm.nih.gov/geo/series/GSE40nnn/GSE40279/suppl/GSE40279_sample_key.txt.gz

        `_prepare_raw_files` writes `imputed_cells.parquet` (the deposited cells that are not BeadStudio's beta) from
        the three files, once. Left out: GSE40279_average_beta.txt.gz (the series matrix's values, checked equal on
        all 310,310,304 cells) and GSE40279_RAW.tar (the array manifests only, no IDAT files).
    """
    bibtex = """
        @article{hannum2013genome,
          title={Genome-wide Methylation Profiles Reveal Quantitative Views of Human Aging Rates},
          author={Hannum, Gregory and Guinney, Justin and Zhao, Ling and Zhang, Li and Hughes, Guy and Sadda, SriniVas
                  and Klotzle, Brandy and Bibikova, Marina and Fan, Jian-Bing and Gao, Yuan and Deconde, Rob and
                  Chen, Menzies and Rajapakse, Indika and Friend, Stephen and Ideker, Trey and Zhang, Kang},
          journal={Molecular Cell},
          volume={49},
          number={2},
          pages={359--367},
          year={2013},
          doi={10.1016/j.molcel.2012.10.016}
        }
    """
    curation_comments = """
        We start with the GEO series matrix of GSE40279 (`GSE40279_series_matrix.txt.gz`: 656 whole-blood samples, one per person, 473,034 average betas each, and the characteristics age, site, plate, gender, ethnicity, tissue), and BeadStudio's signal file of the series (`GSE40279_signal_intensities.txt.gz`) with its sample key, to find the imputed values.

        - Prediction point: a blood sample of a person of unknown age has been run on the 450K array in a new batch; the model estimates the age from its methylation, the person's sex and recorded ethnicity. The paper names the uses: "from health assessment and prevention of disease to forensic analysis" (Conclusions).
        - Target: `age (y)` as `age`, whole years from 19 to 101 (mean 64.0).
        - Features: the 473,034 probes as deposited (470,043 `cg`, 2,991 non-CpG `ch`), betas from 0 to 1, the paper's QC subset: the array's 485,577 less the 11,648 on X and Y, the 65 SNP (`rs`) probes and "830 markers ... removed as they had greater than 5% missing values" (Experimental Procedures). None is constant or a copy of another; no two samples are copies (highest correlation 0.9946). Width is no reason to drop any (CLEAN-22).
        - Features: `sex` (F and M decoded to female and male) and `ethnicity` (Caucasian - European 426, Hispanic - Mexican 230), covariates of the paper's own model ("The covariates gender, BMI, diabetes status, ethnicity, and batch were included in the model", Experimental Procedures); BMI and diabetes are not deposited.
        - Note: `ethnicity` is constant per plate (plates 5, 6 and 9 all Hispanic, the six others all Caucasian), so under the plate split it also marks the cohort: in 16 of 60 folds one side has no Hispanic sample, and in repeat 12 fold 2 every test sample is Hispanic and no training sample is. Kept as the paper's covariate, known to the aging study that uses the clock; no probe flagged the column.
        - Dropped: the recruitment site (UCSD 304, Utah 178, USC 139, Boston 35), a property of the cohort, which differs in age by design (UCSD mean 70.0, Boston 52.0); `tissue`, whole blood for all.
        - Imputed values set back to missing (LEAK-30, PROV-13): the paper set betas with a detection p-value above 0.01 to missing and "imputed with the KNN approach (10 nearest markers)"; a marker's neighbours are found by comparing markers across all samples, test samples included. The signal file holds each sample's own beta, max(B, 0) / (A + B + 100) of its two signals (its `AVG_Beta`, to 3e-7). The deposit equals it on all cells but 430,448 (0.139%): 405,768 that BeadStudio left blank and 24,680 changed, failed measurements (signal A + B a median 3% of the probe's median; 99.4% under half). They ship as missing: 185 to 8,315 per sample (at most 1.8%), at most 34 per probe (5.2%).
        - Note: 4,612,760 cells (1.5%) are exactly 0, nearly all on unmethylated probes whose signal B is 0 after background subtraction: the formula's floor, kept.
        - Note: the 830-marker filter was computed over all samples too; without detection p-values (not deposited) it cannot be undone, and it chose probes by failures, not by age; kept.
        - Width: ultra-wide, 656 rows x 473,038 columns (473,036 features, the target and the plate); every probe is kept.
        - Rows: all 656 samples; the paper had removed one sample with over 5% missing values and 24 PCA outliers.
    """
    splits_comment = """
        Grouped by processing plate (9 plates of 17 to 92 samples), 3 folds: a test fold holds every sample of three plates (146 to 267 rows). A lab applies an age clock to samples run in its own batches, so a test sample's batch is never in training; the batch is strong (a sample's nearest neighbour is on its own plate for 68% of the samples, 12% by chance), and it matters: an elastic-net clock (the paper's model family, fitted inside each fold) errs by 5.4 years (RMSE) on these folds against 4.8 on folds of random people (3 repeats of 3 folds); a ridge on all probes by 9.1 against 6.8 random, 7.1 on folds of whole array chips (a test chip's plate in training) and 8.9 leaving out one recruitment site. The plates differ in age (plate means 38.5 to 76.2 years) and ethnicity (plates 5, 6 and 9 hold the 230 Hispanic samples, the other six none), so each fold also shifts the cohort, as a clock applied in a new study meets. The 20 repeats give 18 distinct partitions of the 9 plates into 3 test folds (repeats 9 and 11, and 8 and 13, coincide), as chance makes likely with 280 possible partitions; the protocol default is kept.
    """

    # Task
    target = "age"
    problem_type = "regression"
    metric = Metric.fallback(
        reason=(
            'Hannum et al. (2013) report two criteria side by side for the age model, "a correlation between age and '
            'predicted age of 96% and an error of 3.9 years" on the primary cohort and 91% and 4.9 years on the '
            'validation cohort (Results, "A predictive model for the aging methylome"), and do not name the error '
            "(MET-5: no single deliberate choice). Their Fig. 7A calls the same authors' error a "
            '"standard error (RMSE = 7.22 years)", so rmse in years is the likely reading. The GEO series defines '
            "no task metric."
        ),
    )
    grouping = Grouping(
        on="plate",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a processing plate of the 450K assay (the GEO characteristic `plate`; 9 plates, 17 to 92 samples, each of the 67 array chips on one plate). The paper treats batch as a factor of the data ("The covariates gender, BMI, diabetes status, ethnicity, and batch were included in the model", Experimental Procedures) and validates the model on a second cohort ("two different cohorts (N1 = 482, N2 = 174)", Results). Its use case is a clock applied to new people's blood, "from health assessment and prevention of disease to forensic analysis" (Conclusions); their samples are measured in batches of their own, so whole plates are held out. Each person is one row and one prediction.
        """,
    )

    prepared_raw_files = (IMPUTED,)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        find_imputed_cells(raw_dir).to_parquet(raw_dir / IMPUTED, index=False)

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        return {"matrix": read_series_matrix(raw_dir / MATRIX), "imputed": pd.read_parquet(raw_dir / IMPUTED)}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        df = raw["matrix"]
        n_meta = len(CHARACTERISTICS) + 1  # the characteristics and `tissue` come first, then the probes
        probes = df.columns[n_meta:]
        # 1. The cells the authors imputed (blank in BeadStudio's export, or changed) go back to missing.
        imputed = raw["imputed"]
        rows, cols = df.index.get_indexer(imputed["sample"]), probes.get_indexer(imputed["probe"])
        assert (rows >= 0).all()
        assert (cols >= 0).all()
        beta = df.iloc[:, n_meta:].to_numpy(dtype="float64", copy=True)
        beta[rows, cols] = np.nan
        meta = df.iloc[:, :n_meta].copy()
        # 2. The target: age in whole years; the group: the plate number.
        meta["age"] = meta["age"].astype("int64")
        meta["plate"] = meta["plate"].astype("int64")
        # 3. Sex in words (the deposit writes F and M).
        meta = decode(meta, {"sex": SEX})
        # 4. Drop the recruitment site (a cohort the model will not see again) and the constant tissue.
        assert (meta["tissue"] == "whole blood").all()
        meta = meta.drop(columns=["site", "tissue"])
        # 5. One row per person; the GEO accession index is replaced by the base class's row index.
        assert meta.index.is_unique
        return pd.concat([meta, pd.DataFrame(beta, index=df.index, columns=probes)], axis=1)

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["sex", "ethnicity"])

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        imputed = raw["imputed"]
        blank = imputed["beadstudio"].isna()
        per_sample = imputed.groupby("sample").size()
        cells = pd.DataFrame(
            {
                "count": [
                    N_PROBES * len(raw["matrix"]),
                    int(blank.sum()),
                    int((~blank).sum()),
                    len(imputed),
                    int(per_sample.min()),
                    int(per_sample.median()),
                    int(per_sample.max()),
                ]
            },
            index=pd.Index(
                [
                    "deposited cells (656 samples x 473,034 probes)",
                    "blank in BeadStudio's export, filled in the deposit",
                    "BeadStudio's value changed in the deposit",
                    "set back to missing (both)",
                    "per sample, fewest",
                    "per sample, median",
                    "per sample, most",
                ],
                name="cells",
            ),
        )
        meta = raw["matrix"].iloc[:, : len(CHARACTERISTICS) + 1]
        return [
            Decision(
                title="The values the authors imputed are set back to missing",
                why=(
                    "The paper imputed failed betas by KNN over the markers, with neighbours chosen on all samples, "
                    "test samples included (LEAK-30). BeadStudio's per-sample betas in the signal file show which "
                    "deposited cells were imputed: the ones it left blank and the ones the deposit changed."
                ),
                evidence=cells,
            ),
            Decision(
                title="Grouped by processing plate",
                why=(
                    "A lab's new samples come in a batch of their own; the plates carry a strong batch signal and "
                    "differ in age and ethnicity, so random people would put a test sample's batch in training."
                ),
                evidence=plate_table(meta),
            ),
        ]
