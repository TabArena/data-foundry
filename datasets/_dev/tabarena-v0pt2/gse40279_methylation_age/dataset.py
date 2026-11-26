"""Curated dataset definition for `gse40279_methylation_age` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import gzip
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.csv as pacsv
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Grouping,
    Metric,
    Source,
    TaskSummary,
    TimeBasis,
    decode,
)

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
                header.setdefault(field.removeprefix("!Sample_"), values)
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
    values = np.empty((len(accessions), table.num_rows), dtype="float64")
    for row, gsm in enumerate(accessions):
        values[row] = table.column(gsm).to_numpy(zero_copy_only=False)
    probes = table.column("ID_REF").to_pylist()
    del table
    meta = pd.DataFrame({CHARACTERISTICS[key]: header[key] for key in CHARACTERISTICS}, index=accessions)
    meta["tissue"] = header["tissue"]
    beta = pd.DataFrame(values, index=accessions, columns=probes)
    return pd.concat([meta, beta], axis=1)


def find_imputed_cells(raw_dir: Path) -> pd.DataFrame:
    """The cells of the deposit that are not BeadStudio's per-sample beta: blank in its export, or changed.

    The signal file holds BeadStudio's `AVG_Beta` of all 485,577 probes and every sample, which is max(B, 0) / (A + B +
    100) of the sample's own two signals. The paper set a beta with a detection p-value above 0.01 to missing and
    imputed the missing ones by KNN over the markers (Experimental Procedures, "Sample collection"); a deposited cell
    that differs from BeadStudio's, or where BeadStudio left the cell blank, is such an imputed value.
    """
    header, table = read_matrix_parts(raw_dir / MATRIX)
    accessions = np.asarray(header["geo_accession"], dtype=object)
    key = pd.read_csv(raw_dir / SAMPLE_KEY, sep="\t", header=None, names=["index", "sample", "sentrix"], dtype=str)
    sentrix = dict(zip("X" + key["sample"], key["sentrix"], strict=True))
    column_of = {sentrix[name]: j for j, name in enumerate(header["source_name_ch1"])}
    row_of = {probe: i for i, probe in enumerate(table.column("ID_REF").to_pylist())}
    deposit = np.column_stack([table.column(gsm).to_numpy(zero_copy_only=False) for gsm in accessions])
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
        question="How old is a person, in years, judged from the DNA methylation of their whole blood?",
        use_case=(
            "A laboratory that builds an epigenetic clock decides which model to ship: candidate clocks are fitted "
            "on profiled cohorts, and the one with the lowest held-out error in years on arrays run in a batch it "
            "never saw goes out. The clock then serves a forensic estimate of an unknown donor's age, and the "
            "reading of a predicted age against a real one as an aging rate."
        ),
        row=(
            "One person's whole-blood sample on the Illumina 450K methylation array (656 adults aged 19 to 101, "
            "recruited at four US sites and assayed on nine plates; one sample per person)."
        ),
        predicted="The person's chronological age in whole years at the blood draw.",
        known=(
            "The methylation level, between 0 and 1, at each of 473,034 sites of the genome in that blood sample, "
            "and the person's sex."
        ),
        split=(
            "Whole assay plates are held out, so every test sample was measured in a batch the model never saw, as a "
            "laboratory's new samples are."
        ),
        changes=(
            "We hold out whole plates instead of random people, leave the recruitment site and the recorded "
            "ethnicity out of the inputs, and set the 0.14% of values the authors had imputed back to missing."
        ),
        fit="direct",
        fit_reason=(
            "The fit rests on the clock builder: the inputs are what a clock reads from a blood array, the target "
            "is the age a clock is chosen by, and a held-out plate is a batch the model has not seen. The plates "
            "differ in age and each holds one recorded ethnicity, so a test fold is a shift in cohort as well as "
            "in batch. A potential leak is kept on purpose and does not change the grade: two published clocks "
            "were fitted on the ages of these very rows, and recalibrating one of them floors the error at about "
            "4.9 years with no model of our features at all, against the best honest model's 5.279 "
            '(curation_comments, "Potential leak, kept on purpose"). The fit graded here is that of the task '
            "without the leak."
        ),
    )

    # Dataset
    unique_name = "gse40279_methylation_age"
    domain = "biology & life sciences"
    sources = (
        Source(
            role="publication",
            platform="Other",
            # The GEO series of Hannum et al., public on 2012-11-21, the day the paper appeared online
            url="https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE40279",
            license=(
                "None stated by the series or its series matrix; GEO's own disclaimer governs the data "
                "(https://www.ncbi.nlm.nih.gov/geo/info/disclaimer.html)"
            ),
            year="2012",
            bibtex="""
                @article{hannum2013genome,
                  title={Genome-wide Methylation Profiles Reveal Quantitative Views of Human Aging Rates},
                  author={Hannum, Gregory and Guinney, Justin and Zhao, Ling and Zhang, Li and Hughes, Guy and
                          Sadda, SriniVas and Klotzle, Brandy and Bibikova, Marina and Fan, Jian-Bing and Gao, Yuan
                          and Deconde, Rob and Chen, Menzies and Rajapakse, Indika and Friend, Stephen and
                          Ideker, Trey and Zhang, Kang},
                  journal={Molecular Cell},
                  volume={49},
                  number={2},
                  pages={359--367},
                  year={2013},
                  doi={10.1016/j.molcel.2012.10.016}
                }
            """,
        ),
    )
    time_basis = TimeBasis(
        "UnseenGroup",
        """
        the use case applies the clock to blood measured in a batch the model has not seen, not to a later period:
        age is a fixed fact at the draw, and the series records no date per sample. It cannot test a drift of the
        assay over the years.
        """,
    )
    split_leaf = "L-PLACE.groups"
    download_description = """
        The GEO series GSE40279 from NCBI's FTP server: the series matrix (1.2 GB), BeadStudio's signal file (5.0 GB)
        and the sample key (4.5 KB).

        mkdir -p local-data-warehouse/gse40279_methylation_age && cd local-data-warehouse/gse40279_methylation_age
        wget https://ftp.ncbi.nlm.nih.gov/geo/series/GSE40nnn/GSE40279/matrix/GSE40279_series_matrix.txt.gz
        wget https://ftp.ncbi.nlm.nih.gov/geo/series/GSE40nnn/GSE40279/suppl/GSE40279_signal_intensities.txt.gz
        wget https://ftp.ncbi.nlm.nih.gov/geo/series/GSE40nnn/GSE40279/suppl/GSE40279_sample_key.txt.gz

        `_prepare_raw_files` writes `imputed_cells.parquet` (the deposited cells that are not BeadStudio's beta) from
        the three files, once. Left out: `GSE40279_average_beta.txt.gz` and its four per-sample parts, which hold the
        series matrix's own values (downloaded and compared: the same 473,034 probes and 656 samples in another row
        order, equal on all 310,310,304 cells, no blank), and `GSE40279_RAW.tar` (183 MB, by its own listing the four
        GPL13534 array manifests and nothing else; no IDAT ships, and every sample's `!Sample_supplementary_file` is
        `NONE`).
    """
    curation_comments = """
        We start with the GEO series matrix of GSE40279 (656 whole-blood samples, one per person, 473,034 average betas each, and the characteristics age, source, plate, gender, ethnicity and tissue), and BeadStudio's signal file with its sample key, which tell us which deposited values the authors imputed.

        - Prediction point: a person's blood has been drawn and run on the 450K array in a batch of its own; the model estimates the age from its methylation and the person's sex. The actor is a laboratory choosing which clock to ship, which it decides by the held-out error in years on arrays from a batch it did not fit on; the clock then serves the uses the paper names, "from health assessment and prevention of disease to forensic analysis" (Conclusions). The forensic estimate of an unknown donor's age is the decision the clock serves; reading the residual against the real age as an aging rate is a purpose and not an actor, since that reader already holds the chronological age. The plates differ in age by the cohort design (means 38.5 to 76.2 years) and each holds one recorded ethnicity, so a test fold is a shift in cohort as well as in batch.
        - Target: the characteristic `age (y)` as `age`, whole years, 19 to 101 (mean 64.0); every sample's `!Sample_title` repeats it ("age 67y 1001"), and the two agree on all 656 rows.
        - Features: the 473,034 probes as deposited (470,043 `cg`, 2,991 non-CpG `ch`, no `rs` control), betas from 0 to 0.99958; none is constant and no two are copies, and no two samples are copies (the highest correlation between two samples is 0.9946, against a median 0.9888 over all pairs). It is the paper's QC subset of the array: counted in the GPL13534 v1.1 manifest, the 485,577 assay probes less the 11,648 on X and Y and the 65 `rs` controls leave 473,864, and the "830 markers ... removed as they had greater than 5% missing values" (Experimental Procedures) make up the rest exactly (827 `cg` and 3 `ch`). Width is no reason to drop a probe (CLEAN-22).
        - Features: `sex` (the characteristic `gender`, F and M decoded to female and male), a covariate of the paper's own model ("The covariates gender, BMI, diabetes status, ethnicity, and batch were included in the model", Experimental Procedures); BMI and diabetes status are not deposited. It is an attribute of the person and not a mark of the batch: both sexes sit on every plate (female share 0.312 to 0.728, overall 0.515), and alone it scores exactly the constant (RMSE 15.566 over the plate folds).
        - Dropped: `ethnicity` (Caucasian - European 426, Hispanic - Mexican 230), because each of the nine plates holds exactly one ethnicity (plates 5, 6 and 9 Hispanic, the six others Caucasian), so the column is a two-level coarsening of the group key and hands a model back part of what the split withholds (LEAK-33). What it carries is the study's recruitment design, not biology (every error in years in this bullet is an RMSE over the plate folds, the comparison as it was measured): alone it scores 13.645 against the constant's 15.566, and predicting each test row by its ethnicity's training-side mean age cuts RMSE 16.07 to 14.18 and beats the dummy on 52 of the 60 folds, while a real model is hurt by it (the honest model 5.279 to 5.553, a 100-probe clock 6.046 to 6.060). The paper could not separate it from the batch either ("Analysis of ethnicity and diabetes status was not possible due to correlations with batch variables", Results).
        - Dropped: `site` (the characteristic `source`: UCSD 304, Utah 178, USC 139, Boston 35), the recruitment cohort, which differs in age by design (UCSD mean 70.0, Boston 52.0) and names a cohort a new sample is not from; `tissue`, whole blood on every row.
        - Imputed values set back to missing (LEAK-30, PROV-13): the paper set betas with a detection p-value above 0.01 to missing and "imputed [them] with the KNN approach (10 nearest markers)", whose neighbours are found over all samples, the test samples included; the deposit has no missing cell at all. BeadStudio's signal file holds each sample's own beta, max(B, 0) / (A + B + 100) of its two signals (checked on the 42,640 cells of the 65 `rs` probes: the two agree to 3e-7), so the cells where the deposit differs from it, or where it is blank, are the imputed ones: 430,448 of 310,310,304 (0.139%), 405,768 blank and 24,680 changed. They ship as missing, 185 to 8,315 per sample (at most 1.8% of a sample) and at most 34 of the 656 samples per probe. 304 of the 430,448 are measured rather than imputed: BeadStudio left the cell blank where the sample's signal B is at or below 0 (284 of them deposited as exactly 0.0, over 188 samples and 186 probes). They ship as missing with the rest.
        - Note: the 830-marker filter ran over all samples too; without the detection p-values, which are not deposited, it cannot be undone, and it chose markers by their failures, not by age. Kept.
        - Note: 4,616,287 cells of the deposit (1.49%), spread over 67,248 probes, are exactly 0: the formula's floor where a sample's signal B is 0 after background subtraction, not a missing value. Kept as measured.
        - Note: the betas are each sample's own ratio, so nothing was scaled across samples (probe 16's benign reading); the KNN imputation above is the one step that read all samples.
        - Potential leak, kept on purpose: two published epigenetic clocks were fitted on the ages of these very rows. Hannum et al. 2013 (71 CpGs; this series is its own fitting set, 482 of the 656 samples its primary cohort) and Lin et al. 2016 (99 CpGs, fitted on the same series) publish their coefficients, in a public Bioconductor data package among other places, and every site either clock uses is a column of this table. Every one of the 60 test folds holds rows those clocks were fitted on, on average 75% of the fold and at least 40%. What that buys, as mean RMSE in years over the 60 shipped splits: the best honest model (a ridge on a fold-honest top-5000, z-scored) errs 5.279; Hannum alone, recalibrated per split, with no model of our features at all, errs 4.949; the honest model stacked with Hannum and Lin errs 4.645, and with all five published clocks 4.487, a gain of 0.791 years. The control that stacks only the three clocks fitted elsewhere gains 0.115 years (5.163), which is what identifies most of that gain as label information rather than better modelling. No change to this definition removes it: the leak sits in the published weights and not in the site list, and refitting honestly on Hannum's own 71 sites errs 5.299, so dropping those sites does not work either. No check can detect its use: the exploit is a dot product of public numbers, and a stacked clock is invisible in a prediction vector. The second reader is warned as well: anyone using this series to validate a new clock will reach for Hannum's published predictions as the comparison, and on these rows they are not honest. Protocol: an entry on this task must not use a model, or coefficients, fitted on the ages of these 656 samples; that bound is declared rather than enforced, because nothing in the data and nothing in a submitted prediction shows it was crossed. Revisit: if this collection ever scores predictions it did not fit itself, this note is not enough and the dataset is re-examined.
        - Rows: one per person, all 656 deposited samples (the paper had already removed one sample with over 5% missing values and 24 PCA outliers). No two rows are the same person: of the 65 `rs` genotype probes in the signal file, the closest pair of samples shares 62 (X5056 and X5057, a likely first-degree relative pair), while over all pairs the median agreement is 40% of the probes and the 99.99th percentile 64%; both sit on plate 5, so no split separates them.
        - Width: 656 rows x 473,037 columns (473,035 features, the target and the group).
    """
    splits_comment = """
        Every error in years quoted below is an RMSE over the splits it names, which is how these comparisons were measured; the task's declared metric is the mean absolute error (metric reason).

        Grouped by assay plate (the characteristic `plate`: 9 plates of 17 to 92 samples), the leaf L-PLACE.groups of the split tree. The place the leaf means here is the assay batch: the use case applies the clock to blood measured in a batch the model never saw ([EXP.meets] another laboratory, site or instrument), and the series holds nine such batches ([PLACE.several]). A test fold holds every sample of three plates (146 to 267 rows over the 20 repeats x 3 folds; the 60 splits are 41 distinct test sets and 41 distinct training sides, 18 of the 20 repeats a distinct partition), so no test row keeps its own plate in training (0.0%) and no test sample shares a BeadChip with a training sample (each of the 67 chips sits on one plate).

        What the split withholds is plate membership itself, and that is measured. Plate labels permuted inside cells of ethnicity x age quintile, so that each pseudo-plate keeps its real plate's size, its single ethnicity and its age histogram while only about 29% of samples keep their real plate, cost a ridge over all probes 7.17 to 7.20 years (RMSE, three seeds) against 6.92 on folds of random people, while the real plates cost 8.71: of the +1.79 years the plate split adds over random people, +1.5 is plate membership and +0.25 the cohort composition the plates carry. The batch is recoverable from the features (the plate at 0.891 accuracy from 50 principal components against 14.0% by chance, and predicting the inferred plate's mean age alone scores 11.96 against the constant's 14.73), so folds of random people would hand a model a pure batch shortcut. A sample's nearest neighbour by Euclidean distance over the probes is on its own plate for 68.6% of the samples against 12.1% by chance (60.4% by sample correlation). The plate explains 0.446 of the variance of age against 0.011 for shuffled plates (the group statistics below), which is the cohort's age design that the plates carry, not the batch signal itself. The plate is the level the batch acts on: holding out whole BeadChips instead costs almost nothing (7.09 years), because a test chip's plate is still in training, and nothing binds above the plate either, as the 8 Sentrix lots are crossed by a plate in only 4 of the 8 cases and a lot-held-out split is easier than the plate split (a 100-probe clock 5.93 against 6.12 in the same comparison).

        The plates are not nested in the recruitment sites and the sites are not nested in the plates (plate 2 holds Utah, Boston and USC samples; the USC samples sit on plates 2, 5 and 6), so the key is a choice between the assay batch and the recruitment cohort, and it follows the application: every actor meets a new assay batch, and only sometimes a new cohort. The plate key also holds out what it claims, where the site key does not: measured on the shipped splitter the plate key leaves 0.0% of test rows with their own plate in training over 41 distinct training sides, the site key 32.3% over 10, and the site key tests measurably less (a 100-probe clock errs 5.55 years under it against 5.81 under the plate key, with a fold-to-fold sd of 2.67 against 1.24). The 12-group plate x site pair key is the weakest of the three rather than the stricter option: it breaks the plate blocks and leaves 25.2% of test rows with their own plate in training. The paper's own validation, the second cohort ("two different cohorts (N1 = 482, N2 = 174)", which the sites UCSD + Utah and USC + Boston match exactly), shares plates 2 and 5 with its training side and is one fold, so it is weaker than either and is not the shipped split (SPLIT-5). This key departs from the datasets that grouped on the population unit their source's own validation held out; what sets this case apart is the measured batch above.

        Two transfers the use case meets stay untested. The step to another recruitment cohort: 94.5% of test rows keep their own site in training under the shipped folds, 96.9% over all 84 possible three-plate folds, and 100% for UCSD's 46% of the rows, because UCSD has four plates and a fold holds three, so for nearly half the data it is structurally untestable. The step to another laboratory or array generation cannot be tested at all: one laboratory, one platform. Holding out batch and cohort at once is unavailable at any finer key, because the plate-site incidence graph has exactly two components ({UCSD; plates 1, 8, 9, 11} = 304 rows and {Boston, USC, Utah; plates 2, 3, 5, 6, 10} = 352 rows). That two-group split is the bound on what the shipped split cannot test, and its price is known (a ridge 10.15 years with a fold-to-fold sd of 2.20 and the clock 6.30, against 8.71 and 5.81 here); it is not a split protocol, since two groups give one leave-one-out pair and a 304-row test side.
    """

    # Task
    target = "age"
    problem_type = "regression"
    metric = Metric.from_context(
        "mae",
        reason=(
            "Mean absolute error in years: the source fixes no metric, and the task makes this one obvious "
            "(MET-11), so the regression fallback is overruled. Where we looked: the paper, the GEO series page "
            "and its sample records, and the literature the paper belongs to. Hannum et al. report two criteria "
            'side by side for the methylation age model, "a correlation between age and predicted age of 96% and '
            'an error of 3.9 years" on the primary cohort and 91% and 4.9 years on the validation cohort '
            '(Results, "A predictive model for the aging methylome"), and never say what that error is; the '
            "Experimental Procedures give no formula, and the one RMSE the paper names (Fig. 7A, 7.22 years) "
            "belongs to its transcriptome model, not to this one. The GEO series defines no task metric and there "
            "is no competition page, so there is no single deliberate choice to take (MET-5). The original is "
            "that unnamed error of 3.9 years, and what fixes it is the context: every actor in this field states "
            "and acts on absolute error in years (forensic age tools report a mean absolute error of about 3.2 "
            "years, inter-laboratory work a mean absolute deviation of 3.62, the standard clock a median absolute "
            "deviation). The measurement agrees, pooled over the 60 folds for a 100-probe clock: MAE 4.57 and "
            "median absolute error 3.58 against RMSE 6.14, so the paper's own 3.9 years sits between the first "
            "two and nowhere near the third. Rejected: the rmse fallback, which this declaration overrules and "
            "which is driven by the band where a clock is most biased (+2.59 years at ages 19 to 39, -4.40 at 80 "
            "to 101); median absolute error, which is closer still to how clocks are reported but which no source "
            "fixes and which is not one of our fallbacks. Little moves either way: over nine model variants the "
            "MAE and RMSE rankings agree at Kendall tau 0.889. The metric reads only the target and the "
            "prediction, so no scoring column is needed. For provenance only: the benchmark this candidate comes "
            "from states RMSE is its primary regression metric, which is another collection's choice and no "
            "evidence for ours."
        ),
    )
    grouping = Grouping(
        on="plate",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a plate of the 450K assay (the GEO characteristic `plate`: 9 plates of 17 to 92 samples, each of the 67 BeadChips on exactly one plate). The paper treats the batch as a factor of the data ("The covariates gender, BMI, diabetes status, ethnicity, and batch were included in the model", Experimental Procedures) and validates the model on a second cohort ("two different cohorts (N1 = 482, N2 = 174)", Results). The use case is a clock applied to other people's blood, "from health assessment and prevention of disease to forensic analysis" (Conclusions); their samples are measured in batches of their own, so whole plates are held out. Each person is one row and one prediction.
        """,
    )

    accepted_check_warnings = {
        "task_group_count_low": (
            "Nine plates are every assay batch the series has, and the batch is the level a clock must generalize "
            "over: a test sample is always measured in a batch of its own. The signal survives the key, so the few "
            "groups do not hollow the task out: four model families beat the dummy on all 60 splits, and shuffled "
            "ages on none of them over three seeds."
        ),
        "groups_test_groups_few": (
            "A group is one assay plate of 17 to 92 samples, a batch over which we want to generalize, and from the "
            "context a few such batches suffice, as when generalizing over a few hospitals (heart_disease stayed "
            "grouped with 3). Each fold holds three plates and 146 to 267 rows. The 60 splits are 41 distinct "
            "training sides, so the spread over repeats is descriptive rather than 60 independent experiments; a "
            "100-probe clock's per-split RMSE runs 4.62 to 6.66 with a fold-to-fold sd of 1.24, and pooled over "
            "the folds the same model scores the declared MAE of 4.57 against an RMSE of 6.14, which is the "
            "spread a score on this dataset has to be read against."
        ),
    }

    prepared_raw_files = (IMPUTED,)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        find_imputed_cells(raw_dir).to_parquet(raw_dir / IMPUTED, index=False)

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        return {"matrix": read_series_matrix(raw_dir / MATRIX), "imputed": pd.read_parquet(raw_dir / IMPUTED)}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        df = raw["matrix"]
        n_meta = len(CHARACTERISTICS) + 1  # the characteristics and `tissue` come first, then the probes
        probes = df.columns[n_meta:]
        # 1. The cells the authors imputed (blank in BeadStudio's export, or changed there) go back to missing.
        imputed = raw["imputed"]
        rows, cols = df.index.get_indexer(imputed["sample"]), probes.get_indexer(imputed["probe"])
        assert (rows >= 0).all()
        assert (cols >= 0).all()
        beta = df.iloc[:, n_meta:].to_numpy(dtype="float64", copy=True)
        beta[rows, cols] = np.nan
        meta = df.iloc[:, :n_meta].copy()
        # 2. The target: age in whole years. The group: the plate number.
        meta["age"] = meta["age"].astype("int64")
        meta["plate"] = meta["plate"].astype("int64")
        # 3. Sex in words (the deposit writes F and M).
        meta = decode(meta, {"sex": SEX})
        # 4. Drop the recruitment site and the ethnicity (both name a cohort a new sample is not from, and the
        #    ethnicity is constant within every plate, so it coarsens the group key) and the constant tissue.
        assert (meta["tissue"] == "whole blood").all()
        assert meta.groupby("plate")["ethnicity"].nunique().eq(1).all()
        meta = meta.drop(columns=["site", "ethnicity", "tissue"])
        # 5. One row per person; the base class replaces the GEO accession index by its own row index.
        assert meta.index.is_unique
        return pd.concat([meta, pd.DataFrame(beta, index=df.index, columns=probes)], axis=1)

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["sex"])

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
                    "The paper imputed failed betas by KNN over the markers, with the neighbours found over all "
                    "samples, the test samples included (LEAK-30). BeadStudio's per-sample betas in the signal file "
                    "say which deposited cells were imputed: the ones it left blank and the ones the deposit changed."
                ),
                evidence=cells,
            ),
            Decision(
                title="Grouped by assay plate",
                why=(
                    "A laboratory's new samples come in a batch of their own; the plates carry a strong batch signal "
                    "and differ in age and ethnicity, so random people would put a test sample's batch in training."
                ),
                evidence=plate_table(meta),
            ),
        ]
