"""Curated dataset definition for `early_stage_diabetes_risk_prediction` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary


class EarlyStageDiabetesRiskPrediction(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Does a person have diabetes, judging from a symptom questionnaire?",
        use_case=(
            "For example, a doctor or a screening app decides from a short symptom questionnaire whether a person "
            "should have a blood-sugar test (the source paper predicts the likelihood of diabetes at an early stage)."
        ),
        row=(
            "One patient of Sylhet Diabetes Hospital, Bangladesh, newly diabetic or at risk, who answered a direct "
            "questionnaire (251 rows after dropping repeated rows; the period is not stated)."
        ),
        predicted=(
            "Whether the patient is diabetic (69% of the rows); how and when this was established is not stated."
        ),
        known=(
            "Age, sex, obesity and 13 yes/no symptoms, such as frequent urination, excessive thirst, sudden weight "
            "loss, weakness, blurred vision and slow healing."
        ),
        split="Random patients, so the test data stands for other patients of the same hospital.",
        changes="We drop exact repeated rows, half of the file.",
        fit="approximate",
        fit_reason=(
            "The rows are patients of a diabetes hospital, 69% of them diabetic, not the people a screening "
            "questionnaire is meant for, and the source does not state how or when the label was set."
        ),
    )

    # Dataset
    unique_name = "early_stage_diabetes_risk_prediction"
    year = "2020"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5VG8H"
    license = "CC BY 4.0"
    download_description = """
        We get the data from UCI.

        wget https://archive.ics.uci.edu/static/public/529/early+stage+diabetes+risk+prediction+dataset.zip && unzip early+stage+diabetes+risk+prediction+dataset.zip && rm early+stage+diabetes+risk+prediction+dataset.zip && mkdir -p local-data-warehouse/early_stage_diabetes_risk_prediction && mv diabetes_data_upload.csv local-data-warehouse/early_stage_diabetes_risk_prediction/
    """
    bibtex = """
        @inproceedings{islam2019likelihood,
          title={Likelihood prediction of diabetes at early stage using data mining techniques},
          author={Islam, MM Faniqul and Ferdousi, Rahatara and Rahman, Sadikur and Bushra, Humayra Yasmin},
          booktitle={Computer Vision and Machine Intelligence in Medical Image Analysis: International Symposium, ISCMM 2019},
          pages={113--125},
          year={2019},
          organization={Springer}
        }
    """
    curation_comments = """
        We start with diabetes_data_upload.csv from UCI.

        - We drop exact duplicate rows: 269 of 520 (51.7%) repeat another row, and 107 profiles of age, gender and 14 symptoms occur 2 to 16 times. Distinct patients would rarely agree on all 16 answers, so we treat the copies as a collection artifact (no copies conflict on the label).
    """

    # Task
    target = "class"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "Islam et al. 2019 report accuracy with precision, recall and F-measure (no unique metric, MET-5); no "
            "threshold or costs; 251 deduplicated rows, 69% positive. roc_auc is the binary fallback."
        ),
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "diabetes_data_upload.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.drop_duplicates()
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=[c for c in df.columns if c not in ("Age", self.target)])
