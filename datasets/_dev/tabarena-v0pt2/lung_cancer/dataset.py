"""Curated dataset definition for `lung_cancer` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import gzip
import io
import re
import tarfile
from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Metric, Source, TaskSummary

SERIES_MATRIX = "GSE83227_series_matrix.txt.gz"
ARRAY_DIR = "gse83227_txt"
CAARRAY = "GSE83227_caArray_meyer-00191.tar.gz"
METASTASIS_FLAGS = ("Colon Met", "Breast", "other met")


def _patient(title: str) -> str:
    """The patient of an adenocarcinoma title, without leading zeros (`157T2` -> `157`, `043T2` -> `43`,
    `A1T1` -> `A1`); `None` for any other specimen.
    """
    m = re.match(r"^(A?)0*(\d+)(?:T\d|$)", title)
    return m.group(1) + m.group(2) if m else None


def _metastasis_flags(archive: Path) -> pd.Series:
    """The study's flags of possible metastases from another organ, per adenocarcinoma patient (`True` when any of
    the columns `Colon Met`, `Breast`, `other met` of the sheet DATASET B in `SampleData.xls` holds a 1).
    """
    with tarfile.open(archive) as tar:
        member = next(m for m in tar.getmembers() if m.name.endswith("SampleData.xls"))
        sheet = pd.read_excel(io.BytesIO(tar.extractfile(member).read()), sheet_name="DATASET B")
    sheet.columns = [str(c).strip() for c in sheet.columns]
    names = sheet["SIMPLE ANNOTATION"].astype(str)
    ad = sheet[names.str.match(r"^AD\d+$")]
    patient = ad["SIMPLE ANNOTATION"].str.removeprefix("AD").str.lstrip("0")
    return pd.Series(ad[list(METASTASIS_FLAGS)].notna().any(axis=1).to_numpy(), index=patient.to_numpy())


class LungCancer(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Is an adenocarcinoma resected from the lung a primary lung cancer, or a metastasis from another organ?"
        ),
        use_case=(
            "For example, a pathologist working up an adenocarcinoma in the lung of a patient with an earlier cancer "
            "elsewhere decides whether it is a new lung primary or a metastasis, which changes staging and treatment; "
            'the source calls this "a key issue in lung tumor diagnosis" (Bhattacharjee et al. 2001).'
        ),
        row=(
            "One adenocarcinoma resected from the lung in a 2001 study in Boston (Bhattacharjee et al.), profiled on "
            "one microarray: 127 patients whose clinical history the study recorded."
        ),
        predicted=(
            "Whether the study's annotation sheet flags the tumour as a possible metastasis from another organ "
            "(16, 13%: 8 colon, 4 breast, 4 other) or not (a primary lung adenocarcinoma)."
        ),
        known="The expression of 12,625 probe sets on the tumour's array, summarised on that array alone (MAS5).",
        split="Random patients, so the test data stands for tumours of new patients of the same study.",
        changes=(
            "We take the target from the study's annotation sheet in GEO (`SampleData.xls`, sheet DATASET B), not "
            "the histology of its Dataset A, and keep only the adenocarcinomas with a recorded clinical history. We "
            "rebuild the arrays from GEO: one array per tumour (the first piece and first hybridisation) instead of "
            "the mean of up to four, and each array's own MAS5 signal instead of the published MAS4 values."
        ),
        fit="approximate",
        fit_reason=(
            "The label is the study's flag of a possible metastasis, set from the clinical history and the pathology "
            'report ("c/w colon met", "?Br MET"), not a confirmed origin; the rows are resected tumours of one '
            "centre, where the real question arises on any adenocarcinoma in the lung of a patient with another "
            "cancer."
        ),
    )

    # Dataset
    unique_name = "lung_cancer"
    domain = "medical & healthcare"
    sources = (
        Source(
            role="publication",
            platform="Other",  # the study's deposit of its arrays in GEO
            url="https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE83227",
            license=None,  # GEO gives no licence for the deposit; the PNAS supplement states none either
            year="2001",
            bibtex="""
                @article{bhattacharjee2001classification,
                  title={Classification of human lung carcinomas by mRNA expression profiling reveals distinct adenocarcinoma subclasses},
                  author={Bhattacharjee, Arindam and Richards, William G and Staunton, Jane and Li, Cheng and Monti, Stefano and Vasa, Priya and Ladd, Christine and Beheshti, Javad and Bueno, Raphael and Gillette, Michael and others},
                  journal={Proceedings of the National Academy of Sciences},
                  volume={98},
                  number={24},
                  pages={13790--13795},
                  year={2001},
                  publisher={The National Academy of Sciences}
                }
            """,
        ),
    )
    download_description = """
        We download the study's own deposit of its arrays from GEO (GSE83227, "caArray_meyer-00191"): the series
        matrix (sample titles and histology), each array's MAS5 output file (`.txt.gz`; the arrays of the 127
        adenocarcinomas with a clinical history are used) and the caArray archive, whose `SampleData.xls` holds the
        study's annotation sheet (read from the archive, not extracted).

        W=local-data-warehouse/lung_cancer && mkdir -p $W/gse83227_txt
        wget -P $W https://ftp.ncbi.nlm.nih.gov/geo/series/GSE83nnn/GSE83227/matrix/GSE83227_series_matrix.txt.gz
        zcat $W/GSE83227_series_matrix.txt.gz | grep '^!Sample_supplementary_file' | tr '\\t' '\\n' \\
          | tr -d '"' | grep '\\.txt\\.gz$' | wget -q -P $W/gse83227_txt -i -
        wget -P $W https://ftp.ncbi.nlm.nih.gov/geo/series/GSE83nnn/GSE83227/suppl/GSE83227_caArray_meyer-00191.tar.gz
    """
    curation_comments = """
        - Prediction point: an adenocarcinoma has been resected from the lung and profiled; the clinical history (an earlier cancer elsewhere) is what the pathologist weighs, and the profile is the second opinion. The source names the task: "A key issue in lung tumor diagnosis is the discrimination of a primary lung adenocarcinoma from a distant metastasis to the lung" (Bhattacharjee et al. 2001, Results), and "metastases of nonlung origin can be difficult to distinguish from lung adenocarcinomas" (Introduction).
        - CC (2026-11-11, Andrej): re-targeted from the histology (retired 2026-11-10: the slide settles it on resected tumours) to metastasis against primary (BeyondArena v0.2 review page, issue 7, B). The target is the study's own: sheet DATASET B of `SampleData.xls` (in GEO's caArray archive) marks 16 of its 139 adenocarcinomas as "possible mets" in three columns (`Colon Met` 8, `Breast` 4, `other met` 4) and counts the other 123 as "Adenocarcinoma w/ no history or path indicating non adeno". The paper's Methods: "Other adenocarcinomas (n = 12) were suspected to be extrapulmonary metastases based on clinical history".
        - Rows: the 127 adenocarcinomas of Dataset A's numbered patients. The 12 whose title starts with `A` (`A1T1`, `A31`; `AD1` to `AD31` in the sheet) carry no clinical annotation in Dataset A (no history, stage or survival), so "no metastasis flag" is not a finding for them: dropped. Which flagged rows count (the soft "c/w" and "?" calls, a flag with no pathology note) is open (`REVIEW.md`, issue 8).
        - Size (2026-11-11, `~/claude_jobs/lung_raw/probe_met/`, 10 repeats of 3 stratified folds): 5 or 6 metastases per test fold. The task probe raises no flag (random forest ROC AUC 0.887, ahead of the class shares on 30 of 30 splits; best against worst family 0.127, paired SE 0.035; best single probe 0.663); SVM 0.885, TabPFN 3.5 0.882, logistic regression 0.850, k-nearest neighbours 0.779. Ten marker genes a pathologist stains for (CDX2, KRT20, CDH17, GATA3, TFF1, ESR1 against NKX2-1, NAPSA, SFTPC, SFTPB), unfitted, reach 0.819. Logistic regression and LightGBM score worse than the class shares on log loss (0.487 and 0.592 against 0.379), so the metric is ROC AUC.
        - Source: GEO GSE83227, the study's deposit of all 254 arrays (Affymetrix HG-U95Av2), each with its raw scan, its MAS5 output and the specimen's histology. The paper's Dataset A (PNAS supplement, `dataseta_12600gene.xls`; OpenML 45093 is a copy) is a summary of the same arrays: it averages all arrays of one adenocarcinoma patient (up to four: pieces `T1`, `T2` of one tumour, repeat hybridisations `T1-1`, `T1-2`) and uses the older MAS4 "average difference" values, where each array's overall intensity stays in.
        - CC (2026-11-10, Andrej): rebuilt from GEO (issue 1, D). One array per tumour, the first piece and first hybridisation (the first title in sorted order: `157T1` before `157T2`, `347T1-1` before `347T1-2`; Dataset A averaged them), because a lab profiles a new specimen once; the value is the array's MAS5 `Signal`, scaled on that array alone, so no test array depends on the training arrays (RMA from the raw scans would normalise all arrays together). All 12,625 probe sets ship, the 67 `AFFX` control probes included.
        - Class-dependent recording (record marker `Class-dependent Recording`), found in Dataset A and gone in the rebuild (2026-11-10, histology target): Dataset A's per-patient means occurred in the adenocarcinomas only, and its 41 non-human spike-in controls alone separated the classes (one-vs-rest ROC AUC 0.85); on one MAS5 array per specimen they reached 0.57 and the scan date 0.58. On the metastasis target (2026-11-11, same splits as the size check, logistic regression) the 67 control probes reach ROC AUC 0.42, the non-human spike-ins 0.40 and the array QC values (scale factor, background, noise) 0.52: no recording signal.
        - Not features: GEO's age, sex, stage and pack-years, and the sheet's survival, stage and relapse site. The clinical history that sets the label is not in the data, and the study's annotation columns were filled with the same review.
        - The paper's clustering found a cluster of 12 putative colon metastases, of which "only seven samples had been previously diagnosed as metastases of colonic origin", against 8 colon flags on the sheet; whether a flag came from the expression clusters rather than the history is open with the label question (issue 8).
        - Time basis: Timeless: whether a resected tumour started in the lung or elsewhere does not change; the profiles were measured on banked specimens for one study (Bhattacharjee et al. 2001), so when a tumour was resected plays no role. The order of array processing acts on the features only, and the scan date carried no class signal on the histology target. Not tested: tumours from another hospital, or arrays processed in another laboratory.
    """
    accepted_check_warnings = {
        "meta_license_unknown": (
            "GEO gives no licence for the GSE83227 deposit; the PNAS supplement states none either."
        ),
        "splits_test_minority_few": (
            "16 metastases give 5 or 6 per test fold; the task probe on these folds raises no flag and the methods "
            "separate (random forest ROC AUC 0.887 against logistic regression 0.850; 2026-11-11, Andrej, issue 7)."
        ),
    }

    # Task
    target = "Metastasis"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "The source clusters the samples and names the discrimination of primary lung adenocarcinomas from "
            "metastases as a diagnostic use, but scores no classifier for it (Bhattacharjee et al. 2001)."
        ),
    )

    # Splits
    splits_comment = """
        Random patients, stratified on the target: each row is the one tumour of one patient (the normal lung of patient 268 is not a row), so no grouping is needed. 5 or 6 metastases fall in each test fold of a 3-fold split.
    """

    def _load_raw(self, raw_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
        meta: dict[str, list[str]] = {}
        with gzip.open(raw_dir / SERIES_MATRIX, "rt") as f:
            for line in f:
                key, *values = line.rstrip("\n").split("\t")
                values = [v.strip('"') for v in values]
                if key in ("!Sample_title", "!Sample_geo_accession"):
                    meta[key] = values
                elif key == "!Sample_characteristics_ch1" and values[0].startswith("histology: "):
                    meta["histology"] = [v.removeprefix("histology: ") for v in values]
        samples = pd.DataFrame(
            {
                "gsm": meta["!Sample_geo_accession"],
                "title": [t.removeprefix("meyer-00191: ") for t in meta["!Sample_title"]],
                "histology": meta["histology"],
            }
        )
        samples = samples[samples["histology"] == "Lung Adenocarcinoma"]
        signals = {}
        for gsm in samples["gsm"]:
            path = sorted((raw_dir / ARRAY_DIR).glob(f"{gsm}_*.txt.gz"))[0]
            with gzip.open(path, "rt") as f:
                lines = f.read().split("\n")
            start = next(i for i, line in enumerate(lines) if line.startswith("Probe Set Name\t"))
            rows = [line.split("\t") for line in lines[start + 1 :] if line.strip()]
            signals[gsm] = pd.Series({r[0]: float(r[3]) for r in rows})
        return samples, pd.DataFrame(signals).T, _metastasis_flags(raw_dir / CAARRAY)

    def _clean(self, raw: tuple[pd.DataFrame, pd.DataFrame, pd.Series]) -> pd.DataFrame:
        samples, signals, flags = raw
        samples = samples.assign(patient=samples["title"].map(_patient))
        # the 12 `A` patients have no clinical annotation, so their tumours were never assessed for a metastasis
        samples = samples[~samples["patient"].str.startswith("A")]
        # one array per tumour: the first piece and first hybridisation, where Dataset A averaged all of them
        # (`157T1`, `157T2`; `347T1-1`, `347T1-2`)
        first = (
            samples.sort_values("title", kind="stable").groupby("patient", sort=False).head(1).sort_index(kind="stable")
        )
        missing = set(first["patient"]) - set(flags.index)
        if missing:
            raise ValueError(f"adenocarcinoma patients missing from SampleData.xls: {sorted(missing)}")
        df = signals.loc[first["gsm"]].reset_index(drop=True)
        label = flags.loc[first["patient"]].map({True: "metastasis from another organ", False: "primary lung"})
        df.insert(0, "Metastasis", label.to_numpy())
        return df
