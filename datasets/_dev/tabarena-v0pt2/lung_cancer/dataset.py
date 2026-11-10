"""Curated dataset definition for `lung_cancer` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import gzip
import re
from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Grouping, Metric, Source, TaskSummary

SERIES_MATRIX = "GSE83227_series_matrix.txt.gz"
ARRAY_DIR = "gse83227_txt"
CLASSES = {
    "Lung Adenocarcinoma": "lung adenocarcinoma",
    "Squamous Cell Lung Carcinoma": "squamous cell carcinoma",
    "Lung Carcinoid Tumor": "pulmonary carcinoid",
    "Normal Cell": "normal lung",
    "Small Cell Lung Carcinoma": "small-cell lung carcinoma",
}


def _patient(title: str) -> str:
    """The patient: the number of an adenocarcinoma title (`157T2` -> `157`), also for a normal lung taken from an
    adenocarcinoma patient (`NL268n1` -> `268`); every other title is its own patient.
    """
    m = re.match(r"^(A?\d+)T\d", title) or re.match(r"^NL(\d+)n\d$", title)
    return m.group(1) if m else title


class LungCancer(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=("Which type of lung tissue, tumour or normal, does a specimen's gene expression profile show?"),
        use_case=(
            "For example, a pathology lab assigns a lung specimen to its tissue type from its gene expression "
            "profile, as a check on the microscope reading."
        ),
        row=(
            "One lung tissue specimen of a 2001 study in Boston (Bhattacharjee et al.), profiled on one microarray: "
            "197 specimens of 196 patients, without the 6 small-cell carcinomas."
        ),
        predicted=(
            "The tissue type by histology: adenocarcinoma (71%, including 12 suspected metastases of adenocarcinomas "
            "from other organs), squamous cell carcinoma (11%), pulmonary carcinoid (10%) or normal lung (9%)."
        ),
        known="The expression of 12,625 probe sets on the specimen's array, summarised on that array alone (MAS5).",
        split="Random patients, so the test data stands for specimens of new patients of the same study.",
        changes=(
            "We rebuild the study's Dataset A from its arrays: one array per specimen (the first piece and first "
            "hybridisation) instead of the mean of up to four, and each array's own MAS5 signal instead of the "
            "published MAS4 values. We drop the 6 small-cell carcinomas. The source merges lung adenocarcinomas "
            "with 12 suspected metastases from other organs, and we keep them in that class."
        ),
        fit="approximate",
        fit_reason=(
            "The label is the histology pathologists already read under the microscope, so the profile reproduces a "
            "known diagnosis; the adenocarcinoma class mixes lung tumours with metastases, and whether expression "
            "would be measured for this purpose is unclear (record). The study itself used the data to find "
            "subclasses."
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
        matrix (sample titles and histology) and each array's MAS5 output file (`.txt.gz`, 248 of the 254 arrays,
        without the small-cell carcinomas, are used).

        W=local-data-warehouse/lung_cancer && mkdir -p $W/gse83227_txt
        wget -P $W https://ftp.ncbi.nlm.nih.gov/geo/series/GSE83nnn/GSE83227/matrix/GSE83227_series_matrix.txt.gz
        zcat $W/GSE83227_series_matrix.txt.gz | grep '^!Sample_supplementary_file' | tr '\\t' '\\n' \\
          | tr -d '"' | grep '\\.txt\\.gz$' | wget -q -P $W/gse83227_txt -i -
    """
    curation_comments = """
        - Source: GEO GSE83227, the study's deposit of all 254 arrays (Affymetrix HG-U95Av2), each with its raw scan, its MAS5 output and the specimen's histology. The paper's Dataset A (PNAS supplement, `dataseta_12600gene.xls`; OpenML 45093 is a copy) is a summary of the same arrays: it averages all arrays of one adenocarcinoma patient (up to four: pieces `T1`, `T2` of one tumour, repeat hybridisations `T1-1`, `T1-2`) and uses the older MAS4 "average difference" values, where each array's overall intensity stays in. The arrays give the same 197 specimens (139 / 21 / 20 / 17) once the small-cell carcinomas are dropped.
        - CC (2026-11-10, Andrej): rebuilt from GEO (issue 1, D); whether it stays under this record is open (issue 4). One array per specimen, the first piece and first hybridisation (the first title in sorted order: `157T1` before `157T2`, `347T1-1` before `347T1-2`; Dataset A averaged them), because a lab profiles a new specimen once; the value is the array's MAS5 `Signal`, scaled on that array alone, so no test array depends on the training arrays (RMA from the raw scans would normalise all arrays together). All 12,625 probe sets ship, the 67 `AFFX` control probes included.
        - Class-dependent recording (record marker `Class-dependent Recording`), found in Dataset A and gone in the rebuild (2026-11-10, logistic regression, 20 repeats of 3 folds): Dataset A's per-patient means occurred in the adenocarcinomas only, and its 41 non-human spike-in controls alone separated the classes (one-vs-rest ROC AUC 0.85). On one MAS5 array per specimen the spike-ins reach 0.57, the scan date (in each array's file name, 16 March to 25 April 2001, spread over all classes, chi-squared p = 0.15) 0.58, and the array's QC values (scale factor, background, noise) 0.65. The 26 human control probes (GAPDH, actin and others) still separate the classes (0.94): they are tissue genes. Log loss on all human probes is 0.123 here, 0.141 on Dataset A.
        - Not features: GEO also gives age, sex, stage and pack-years, but only for adenocarcinomas (blank in every other class), so each would give the class away.
        - The source merges lung adenocarcinomas and 12 suspected extrapulmonary metastases into one class, and we keep that. The study's annotation sheet in GEO's caArray archive (`GSE83227_caArray_meyer-00191.tar.gz`, `SampleData.xls`, sheet DATASET B) flags 16 of them as possible metastases (8 colon, 4 breast, 4 other; the paper names 12); the 12 adenocarcinomas whose title starts with `A` (`A1T1`, `A31`) are the ones without any clinical annotation. Whether to make the metastases a class of their own is open (`REVIEW.md`, issues 5 and 6).
        - We drop the class "small-cell lung carcinoma" as it only has 6 samples, which is not a meaningful sample size for benchmarking, or the predictive task.
        - Time basis: Timeless: the label is the histology of an excised specimen, which does not change; the profiles
          were measured on banked specimens for one study (Bhattacharjee et al. 2001), so when a specimen was resected
          plays no role. The order of array processing acts on the features only, and the scan date carries no class
          signal (the class-dependent recording note). Not tested: specimens from another hospital, or arrays
          processed in another laboratory.
    """
    accepted_check_warnings = {
        "meta_license_unknown": (
            "GEO gives no licence for the GSE83227 deposit; the PNAS supplement states none either."
        ),
    }

    # Task
    target = "CancerType"
    problem_type = "multiclass_classification"
    metric = Metric.fallback(
        reason=(
            "The source paper clusters the samples (hierarchical and probabilistic clustering) to find "
            "adenocarcinoma subclasses and declares no classification metric for predicting the class."
        ),
    )
    grouping = Grouping(
        on="patient",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a patient: the specimen title's number (`157T1` and `NL157n1` are patient 157), every other specimen its own patient. 196 patients for 197 specimens: patient 268 gave both an adenocarcinoma and a normal lung specimen, which stay on one side. The use case is a specimen of a new patient (the study profiled resected specimens of its patients, Bhattacharjee et al. 2001); each specimen is one prediction.
        """,
    )

    # Splits
    splits_comment = """
        Grouped splits on the patient. All but one patient have one specimen, so the split is close to random specimens; grouping keeps patient 268's adenocarcinoma and normal lung on one side (log loss 0.126 grouped against 0.123 at random, logistic regression, 2026-11-10).
    """

    def _load_raw(self, raw_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
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
        signals = {}
        for path in sorted((raw_dir / ARRAY_DIR).glob("GSM*.txt.gz")):
            with gzip.open(path, "rt") as f:
                lines = f.read().split("\n")
            start = next(i for i, line in enumerate(lines) if line.startswith("Probe Set Name\t"))
            rows = [line.split("\t") for line in lines[start + 1 :] if line.strip()]
            signals[path.name.split("_")[0]] = pd.Series({r[0]: float(r[3]) for r in rows})
        return samples, pd.DataFrame(signals).T

    def _clean(self, raw: tuple[pd.DataFrame, pd.DataFrame]) -> pd.DataFrame:
        samples, signals = raw
        samples["CancerType"] = samples["histology"].map(CLASSES)
        samples = samples[samples["CancerType"] != "small-cell lung carcinoma"]
        samples["patient"] = samples["title"].map(_patient)
        # one array per specimen (a patient's tumour, or its normal lung): the first piece and first hybridisation,
        # where Dataset A averaged all of them (`157T1`, `157T2`; `347T1-1`, `347T1-2`)
        first = (
            samples.sort_values("title", kind="stable")
            .groupby(["patient", "CancerType"], sort=False)
            .head(1)
            .sort_index(kind="stable")
        )
        df = signals.loc[first["gsm"]].reset_index(drop=True)
        df.insert(0, "patient", first["patient"].to_numpy())
        df.insert(0, "CancerType", first["CancerType"].to_numpy())
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=("patient",))
