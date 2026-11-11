"""Curated dataset definition for `lung_adenocarcinoma_metastasis` (data-foundry v2). Evidence: README.md."""

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
# numbered adenocarcinoma patients whose clinical fields are all empty in DATASET A, like the `A` patients
NO_CLINICAL_DATA = ("355", "360")
# adenocarcinoma patients whose flag the sheet leaves undetermined: AD218 is flagged only by the study's second
# pathology review ("ad w met?") and lies in the paper's colon-metastasis expression cluster, so its flag may follow
# the clustering; AD224 carries the same kind of note ("ad m met?") and is coded primary
UNDETERMINED = ("218", "224")


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


class LungAdenocarcinomaMetastasis(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Is an adenocarcinoma resected from the lung a primary lung cancer, or a metastasis from another organ?"
        ),
        use_case=(
            "For example, a pathologist working up an adenocarcinoma in the lung of a patient with an earlier cancer "
            "elsewhere decides whether it is a new lung primary or a metastasis, which changes staging and treatment "
            '("a key issue in lung tumor diagnosis", Bhattacharjee et al. 2001). The call is read from the tumour\'s '
            "pathology but is not settled there: it rests on the earlier cancer."
        ),
        row=(
            "One adenocarcinoma resected from the lung in a 2001 study in Boston (Bhattacharjee et al.), profiled on "
            "one microarray: the 123 patients with clinical data and a determined flag."
        ),
        predicted=(
            "Whether the study's annotation sheet flags the tumour as a possible metastasis from another organ "
            "(15, 12%: 8 colon, 4 breast, 3 other) or not (a primary lung adenocarcinoma)."
        ),
        known=(
            "The expression of the 12,558 human probe sets on the tumour's array, summarised on that array alone "
            "(MAS5), on its linear scale."
        ),
        split="Random patients, so the test data stands for tumours of new patients of the same study.",
        changes=(
            "The target comes from the study's annotation sheet in GEO (`SampleData.xls`, DATASET B), not the "
            "histology of its Dataset A; only adenocarcinomas with clinical data and a determined flag are kept, and "
            "the 67 control probes are dropped. The arrays are rebuilt from GEO: one per tumour (first piece, first "
            "hybridisation), each with its own MAS5 signal, instead of Dataset A's MAS4 means of up to four."
        ),
        fit="approximate",
        fit_reason=(
            "The label is the study's flag of a possible metastasis, written in the tumour's pathology report from the "
            'clinical history ("c/w colon met", "?Br MET"), not a confirmed origin; the 8 colon calls are the firmest '
            "and the easiest. The rows are all resected adenocarcinomas of one centre, while the question arises only "
            "in patients with an earlier cancer elsewhere, and which primaries had one is not recorded (`Selection "
            "Bias`)."
        ),
    )

    # Dataset
    unique_name = "lung_adenocarcinoma_metastasis"
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
        matrix (sample titles and histology), each array's MAS5 output file (`.txt.gz`; the arrays of the 123
        adenocarcinomas with clinical data and a determined flag are used) and the caArray archive, whose
        `SampleData.xls` holds the study's annotation sheet (read from the archive, not extracted).

        W=local-data-warehouse/lung_adenocarcinoma_metastasis && mkdir -p $W/gse83227_txt
        wget -P $W https://ftp.ncbi.nlm.nih.gov/geo/series/GSE83nnn/GSE83227/matrix/GSE83227_series_matrix.txt.gz
        zcat $W/GSE83227_series_matrix.txt.gz | grep '^!Sample_supplementary_file' | tr '\\t' '\\n' \\
          | tr -d '"' | grep '\\.txt\\.gz$' | wget -q -P $W/gse83227_txt -i -
        wget -P $W https://ftp.ncbi.nlm.nih.gov/geo/series/GSE83nnn/GSE83227/suppl/GSE83227_caArray_meyer-00191.tar.gz
    """
    curation_comments = """
        - Prediction point: an adenocarcinoma has been resected from the lung and profiled; the pathologist weighs the clinical history (an earlier cancer elsewhere), and the profile is a second opinion. The source names the task: "A key issue in lung tumor diagnosis is the discrimination of a primary lung adenocarcinoma from a distant metastasis to the lung" (Bhattacharjee et al. 2001, Results); "metastases of nonlung origin can be difficult to distinguish from lung adenocarcinomas" (Introduction). In practice the work-up is immunohistochemistry and comparison with the earlier tumour; an expression array is not used today.
        - CC (2026-11-11, Andrej): a new dataset from the arrays of `lung_cancer`, whose histology target was retired on 2026-11-10 (the slide settles it on resected tumours): the target is metastasis against primary, under its own record since rows, target and values all changed (lung_cancer review issues 7, B, and 4, B). All flags of the sheet count (issue 8, A) except AD218's, dropped with AD224 as undetermined (2026-11-11, Andrej, review issue 2, B).
        - Label: sheet DATASET B of `SampleData.xls` marks 16 of the study's 139 adenocarcinomas as "possible mets" (`Colon Met` 8, `Breast` 4, `other met` 4) and counts the rest as "Adenocarcinoma w/ no history or path indicating non adeno". 15 of the 16 are written in the resected tumour's own clinical pathology note ("MET COLON", "c/w colon met", "?Br MET", "(met)"); AD218's only note is the study's second reading (`PATH II`, "ad w met?"). The call is read from the specimen's pathology but not settled there: it rests on the earlier cancer outside the specimen. The 8 colon flags are the firmest; 7 of them are the paper's "seven samples [...] previously diagnosed as metastases of colonic origin". The paper speaks of 12 suspected metastases: 12 flags carry a firm note, the other 4 are the three "?Br MET" (AD163, AD172, AD186) and AD218 (dropped, below). 15 flags remain.
        - Rows: 123 adenocarcinomas. Of the paper's "125 adenocarcinoma samples [...] associated with clinical data", AD218 and AD224 are dropped as undetermined (below). Dropped as never assessed: the 12 patients whose title starts with `A` (`AD1` to `AD31` in the sheet) and AD355 and AD360, whose clinical fields are all empty.
        - Size (2026-11-11, shipped splits of the 123 rows, task probe, 30 of the 60 splits): 5 metastases per test fold; no flag; random forest ROC AUC 0.876 (ahead of the class shares on every split), selected-features linear 0.851, logistic regression 0.836, LightGBM 0.811; the best single probe set chosen on each training side 0.652. On the 125 rows before AD218 and AD224 were dropped: random forest 0.886, logistic regression 0.851 (other splits; on the same folds dropping the two moves no score). On the 127 rows before the last changes TabPFN 3.5 reached 0.882 and k-nearest neighbours 0.779; ten pathology marker genes, unfitted (CDX2, KRT20, CDH17, GATA3, TFF1, ESR1 against NKX2-1, NAPSA, SFTPC, SFTPB), 0.819. Out of fold the random forest separates the colon metastases at 0.984, the breast ones at 0.76 and the others at 0.83: the score rests mostly on colon against lung.
        - Metric: ROC AUC, the fallback for a binary task; the source scores no classifier. On log loss the random forest beats the class shares (0.289 against 0.371) while logistic regression and LightGBM do not.
        - Class-dependent recording (record marker `Class-dependent Recording`, 2026-11-11, review panel): the metastasis arrays call fewer probe sets present (share present, ROC AUC 0.722, permutation p 0.01) and show a higher noise floor (0.70) and more 18S rRNA (control probe 0.784). Whether a metastasis's other transcriptome or weaker RNA causes it is open; tumour content does not (Spearman -0.20), nor the processing batch. The 67 `AFFX` control probes (0.695 together, p 0.02) measure the preparation and are dropped, at no cost (random forest 0.894 to 0.893). The share present runs through every gene and cannot be removed: subtracting each array's noise floor leaves logistic regression at 0.855 to 0.857. An earlier note here gave the controls 0.42; that run paired the labels with the wrong arrays.
        - CC (2026-11-11, Andrej): AD218 and AD224 dropped as undetermined (review issue 2, B). AD218 (`other met`) is flagged only by the study's second pathology review (`PATH II`, "ad w met?") and lies in the study's colon-metastasis expression cluster `CM`, so its flag may follow the clustering; AD224 carries the same `PATH II` wording ("ad m met?") and is coded primary. The sheet codes the same evidence both ways; dropping both takes no side. No score moves (random forest 0.895 to 0.893, panel experiment on the shipped folds).
        - Known label doubts, kept as the source codes them (never relabelled from expression): AD320 (unflagged, in `CM`, the random forest's top-ranked row) and AD368 (the paper: high "albumin, transferrin, and other markers associated with the liver", "not identified as a metastasis") are primaries the source itself suspects. AD350, the colon flag outside `CM`, is a mucinous tumour, a known lung mimic of colon.
        - Selection (record marker `Selection Bias`): the rows are all resected adenocarcinomas, but the question arises only in patients with an earlier cancer elsewhere, and which primaries had one is not recorded; neither is the earlier cancer, the input the pathologist always has.
        - Not features: GEO's age, sex, stage and pack-years, and the sheet's survival, stage, relapse site, expression cluster and pathology notes (the cluster holds 8 of the 15 positives; GEO's stage reads M1 for 11 of the 15 flags).
        - Values: the MAS5 signal ships on its linear scale, as the study deposited it. Every row is a public GEO array whose flag is published in the same series.
        - Source: GEO GSE83227, the study's deposit of all 254 arrays (Affymetrix HG-U95Av2), each with its raw scan, its MAS5 output and the specimen's histology; the caArray archive in the same series holds the annotation sheet and the paper (13790.pdf). The paper's Dataset A (PNAS supplement; OpenML 45093 is a copy) averages up to four arrays per adenocarcinoma patient and uses MAS4 values.
        - CC (2026-11-10, Andrej): rebuilt from GEO (lung_cancer issue 1, D). One array per tumour, the first piece and first hybridisation (the first title in sorted order: `157T1` before `157T2`, `347T1-1` before `347T1-2`), because a lab profiles a new specimen once; the value is the array's MAS5 `Signal`, scaled on that array alone, so no test array depends on the training arrays.
        - Time basis: Timeless: whether a resected tumour started in the lung or elsewhere does not change; the profiles were measured on banked specimens for one study, scanned between 16 March and 17 April 2001, so when a tumour was resected plays no role. Not tested: tumours from another hospital, or arrays processed in another laboratory.
    """
    accepted_check_warnings = {
        "meta_license_unknown": (
            "GEO gives no licence for the GSE83227 deposit; the PNAS supplement states none either."
        ),
        "splits_test_minority_few": (
            "15 metastases give 5 per test fold; the task probe on these folds raises no flag and the methods "
            "separate (random forest ROC AUC 0.876 against logistic regression 0.836; 2026-11-11, Andrej, lung_cancer "
            "review issue 7)."
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
        Random patients, stratified on the target: each row is the one tumour of one patient (the normal lung of patient 268 is not a row), so no grouping is needed. 5 metastases fall in each test fold of a 3-fold split; 5 folds would leave 3. The 6 IVT batches and 10 scan days hold 0 to 4 metastases each, and folds grouped by either score as the random split does (random forest pooled ROC AUC 0.883 to 0.889 against 0.884, review panel 2026-11-11).
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
        # the 12 `A` patients and the two in NO_CLINICAL_DATA have no clinical annotation, so their tumours were
        # never assessed for a metastasis: "no flag" is no finding for them
        samples = samples[~samples["patient"].str.startswith("A") & ~samples["patient"].isin(NO_CLINICAL_DATA)]
        # the sheet codes the same second-review note both ways for these two: dropped as undetermined
        samples = samples[~samples["patient"].isin(UNDETERMINED)]
        # one array per tumour: the first piece and first hybridisation, where Dataset A averaged all of them
        # (`157T1`, `157T2`; `347T1-1`, `347T1-2`)
        first = (
            samples.sort_values("title", kind="stable").groupby("patient", sort=False).head(1).sort_index(kind="stable")
        )
        missing = set(first["patient"]) - set(flags.index)
        if missing:
            raise ValueError(f"adenocarcinoma patients missing from SampleData.xls: {sorted(missing)}")
        df = signals.loc[first["gsm"]].reset_index(drop=True)
        # the 67 `AFFX` control probes measure the preparation and hybridisation, not the tumour, and separate the
        # classes (ROC AUC 0.695): dropped
        df = df.drop(columns=[c for c in df.columns if c.startswith("AFFX")])
        label = flags.loc[first["patient"]].map({True: "metastasis from another organ", False: "primary lung"})
        df.insert(0, "Metastasis", label.to_numpy())
        return df
