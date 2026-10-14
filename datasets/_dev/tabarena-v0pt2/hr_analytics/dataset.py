"""Curated dataset definition for `hr_analytics` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TaskSummary


class HrAnalytics(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a person who signed up for a company's data-science training look for a new job?",
        use_case=(
            "A company that trains data scientists wants to know, from sign-up information, which candidates will "
            "work for it after the training and which will look for another job, to plan its courses and cut training"
            " costs (the data card's framing)."
        ),
        row=(
            "One candidate who enrolled in the company's training (19,158 candidates, Kaggle 2020); company, place "
            "and period not stated."
        ),
        predicted=(
            "Whether the candidate is looking for a job change (24.93% are); how and when this was recorded is not "
            "stated."
        ),
        known=(
            "City (coded) and its development index, gender, education level and field, university enrolment, years "
            "of experience and whether it is relevant, current company size and type, years since the last job "
            "change, and training hours completed."
        ),
        split="Random candidates, so the test data stands for other candidates of the same programme.",
        fit="approximate",
        fit_reason=(
            "The label has no stated source or timing (a stated intention or an actual move), and training hours "
            "completed are only known after sign-up. The use case is plausible, but the data does not show when each "
            "fact was recorded."
        ),
    )

    # Dataset
    unique_name = "hr_analytics"
    year = "2020"
    domain = "business & marketing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/arashnic/hr-analytics-job-change-of-data-scientists"
    license = "CC0: Public Domain"
    data_tags = ("Spatial",)
    download_description = """
        mkdir -p local-data-warehouse/hr_analytics && cd local-data-warehouse/hr_analytics && kaggle datasets download arashnic/hr-analytics-job-change-of-data-scientists && unzip hr-analytics-job-change-of-data-scientists.zip && rm hr-analytics-job-change-of-data-scientists.zip && cd ../../
    """
    bibtex = r"""
        @misc{arashnic2021hr,
          author       = {Kaggle User Arashnic},
          title        = {HR Analytics: Job Change of Data Scientists},
          year         = {2021},
          howpublished = {\url{https://www.kaggle.com/datasets/arashnic/hr-analytics-job-change-of-data-scientists}},
          note         = {Kaggle dataset},
        }
    """
    curation_comments = """
        - We renamed the target feature and its values to be more descriptive.
        - We drop the ID column.
        - The rows come from Analytics Vidhya's Student DataFest 2018: The Data Supremacy (July 2018; the same files
          ran again as JanataHack: HR Analytics in May 2020, which the Kaggle card names as its source). Features are
          unchanged; the uploader does not say what "aug" means.
        - Anomaly: `aug_train.csv` is 16,535 rows of the hackathon's train file (labels unchanged) plus 2,623 rows of
          its unlabelled test file, all labelled 1 (55% of the positives). They do not look like real positives (89%
          of city_21's test rows against 27% positives there in the train file) and lift a quick model's CV AUC from
          0.66 to 0.80 (record, 2026-10-14).
    """

    # Task
    target = "LookingForJobChange"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "aug_train.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        target_feature = "LookingForJobChange"
        df = df.rename(columns={"target": target_feature})
        df = df.drop(columns=["enrollee_id"])
        df[target_feature] = df[target_feature].map({1: "Yes", 0: "No"})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "city",
                "gender",
                "relevent_experience",
                "enrolled_university",
                "education_level",
                "major_discipline",
                "experience",
                "company_size",
                "company_type",
                "last_new_job",
            ],
        )
