"""Curated dataset definition for `heart_failure_followup_survival` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TaskSummary, drop_columns


class HeartFailureFollowupSurvival(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a patient with heart failure die during follow-up?",
        use_case=(
            "For example, a cardiologist estimates a heart-failure patient's risk of dying in the coming months from "
            "routine findings and blood tests, to decide on closer follow-up or treatment."
        ),
        row=(
            "One patient with heart failure, aged 40 or older, at the Faisalabad Institute of Cardiology or the "
            "Allied Hospital in Faisalabad, Pakistan, April-December 2015 (299 patients)."
        ),
        predicted=("Whether the patient died during a follow-up of 4 to 285 days that differs by patient (32% did)."),
        known=(
            "Age, sex, smoking, anaemia, diabetes, high blood pressure, the heart's ejection fraction, and blood "
            "values (creatinine phosphokinase, platelets, serum creatinine, serum sodium)."
        ),
        split=("Random patients, so the test data stands for new patients of the same hospitals and year."),
        changes=("We drop the length of follow-up: it ends at death, so a short follow-up gives the outcome away."),
        fit="approximate",
        fit_reason=(
            "The outcome has no fixed horizon: a patient whose follow-up ended early counts as a survivor, and some "
            "may have died later. Whether follow-up ended on one date for all is not stated (the censored times fit "
            "mid-January 2016). When the measurements were taken is not stated."
        ),
    )

    # Dataset
    unique_name = "heart_failure_followup_survival"
    year = "2017"
    domain = "medical & healthcare"
    source = "Other"  # S1 Data of Ahmad et al. 2017 (PLoS ONE); UCI 519 is the 2020 re-upload
    source_url = "https://doi.org/10.1371/journal.pone.0181001"
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
