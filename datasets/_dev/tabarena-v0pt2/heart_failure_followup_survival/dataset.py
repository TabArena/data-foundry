"""Curated dataset definition for `heart_failure_followup_survival` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, drop_columns


class HeartFailureFollowupSurvival(AbstractCuratedDataset):
    # Dataset
    unique_name = "heart_failure_followup_survival"
    year = "2020"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5Z89R"
    license = "CC BY 4.0"
    download_description = """
        We get the data from UCI.

        wget https://archive.ics.uci.edu/static/public/519/heart+failure+clinical+records.zip && unzip heart+failure+clinical+records.zip && rm heart+failure+clinical+records.zip && mkdir -p local-data-warehouse/heart_failure_followup_survival && mv heart_failure_clinical_records_dataset.csv local-data-warehouse/heart_failure_followup_survival/
    """
    bibtex = """
        @article{chicco2020machine,
          title={Machine learning can predict survival of patients with heart failure from serum creatinine and ejection fraction alone},
          author={Chicco, Davide and Jurman, Giuseppe},
          journal={BMC medical informatics and decision making},
          volume={20},
          number={1},
          pages={16},
          year={2020},
          publisher={Springer}
        }
    """
    curation_comments = """
        We use the data as is from UCI.

        - We keep all features of the dataset. The study that introduced the dataset also curated a subset of features. We leave it to the pipeline to select the relevant features for the task.
        - We drop the "time" feature. It is the follow-up period in days (4-285; Chicco & Jurman 2020, Table 1: "Follow-up period"), and DEATH_EVENT is "If the patient died during the follow-up period". Follow-up ends at death or at censoring, so a short follow-up means an early death: the value is only known after the outcome (alone it gives ROC AUC 0.84). The paper's analysis that includes it is not a prediction-time setup.
    """

    # Task
    target = "DEATH_EVENT"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "heart_failure_clinical_records_dataset.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Follow-up time ends at death or censoring, so it is known only after the outcome
        df = drop_columns(df, ["time"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "anaemia",
                "diabetes",
                "high_blood_pressure",
                "sex",
                "smoking",
            ],
        )
