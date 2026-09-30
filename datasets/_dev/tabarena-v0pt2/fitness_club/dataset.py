"""Curated dataset definition for `fitness_club` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class FitnessClub(AbstractCuratedDataset):
    # Dataset
    unique_name = "fitness_club"
    year = "2023"
    domain = "business & marketing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/ddosad/datacamps-data-science-associate-certification"
    license = "Public Domain"
    download_description = """
        kaggle datasets download -d ddosad/datacamps-data-science-associate-certification -p local-data-warehouse/fitness_club/ --unzip
    """
    bibtex = r"""
        @misc{ddosad2023fitness,
          author       = {Kaggle User Ddosad},
          title        = {Fitness Club Dataset for ML Classification},
          year         = {2023},
          howpublished = {\url{https://www.kaggle.com/datasets/ddosad/datacamps-data-science-associate-certification}},
          note         = {Kaggle dataset},
        }
    """
    curation_comments = """
        - We dropped the booking_id column.
        - We renamed the values of the target variable to be more meaningful ("Yes"/"No").
        - We treat "-0" values as "0" values for the target, following the description.
        - We removed trailing words (like "days") from "days_before".
        - We aligned the naming of "day_of_week" to be consistent per day.
    """

    # Task
    target = "attended"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/fitness_class_2212.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.drop(columns=["booking_id"])
        target_feature = "attended"
        df[target_feature] = abs(df[target_feature])
        df[target_feature] = df[target_feature].map({0: "No", 1: "Yes"})
        # Remove trailing text from column
        df["days_before"] = df["days_before"].str.replace(" days", "").astype(int)
        df["day_of_week"] = (
            df["day_of_week"].str.replace("Wednesday", "Wed").replace("Monday", "Mon").replace("Fri.", "Fri")
        )
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "day_of_week",
                "time",
                "category",
            ],
        )
