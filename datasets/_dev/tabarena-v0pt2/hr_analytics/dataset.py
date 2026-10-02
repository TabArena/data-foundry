"""Curated dataset definition for `hr_analytics` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class HrAnalytics(AbstractCuratedDataset):
    # Dataset
    unique_name = "hr_analytics"
    year = "2021"
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
