"""Curated dataset definition for `ghanas_indigenous_intel` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TemporalSplits


class GhanasIndigenousIntel(AbstractCuratedDataset):
    # Dataset
    unique_name = "ghanas_indigenous_intel"
    year = "2025"
    domain = "environmental science & climate"
    source = "Zindi"
    source_url = "https://www.kaggle.com/datasets/phantom50/ghanas-indigenous-intel-dataset"
    license = "CC-BY-SA 4.0"
    data_tags = ("Non-IID", "Temporal", "Grouped")
    download_description = r"""
        We download the data from Kaggle, although it was originally a Zindi competition.

        kaggle datasets download phantom50/ghanas-indigenous-intel-dataset \
        && unzip ghanas-indigenous-intel-dataset.zip \
        && rm ghanas-indigenous-intel-dataset.zip \
        && mkdir -p local-data-warehouse/ghanas_indigenous_intel \
        && mv *.csv local-data-warehouse/ghanas_indigenous_intel/
    """
    bibtex = r"""
        @misc{zindi_ghana_indigenous_intel_2025,
            author       = {{Zindi}},
            title        = {Ghana's Indigenous Intel Challenge [BEGINNERS ONLY]: Data},
            year         = {2025},
            howpublished = {\url{https://zindi.africa/competitions/ghana-indigenous-intel-challenge/data}},
            note         = {Zindi dataset page. Accessed 2026-04-11}
        }
    """
    curation_comments = """
        - Information about the data source: The data was collected by local farmers in the Pra River Basin of Ghana using the Smart Indigenous Weather App, a custom-built mobile app for data collection. Farmers made weather forecasts based on traditional signs such as cloud formations, sun position, wind, moon, heat, and specific tree or animal behaviors. The task is to predict the farmers' forecasts based on these traditional signs, which are represented as features in the dataset. The target variable is the actual amount of rain in four categories, therefore the actual task is to make a prediction correcting the farmers' forecasts.
        - The data was initially used in a Zindi competition with a temporal split, we do the same.
        - We create 6 splits using a sliding window approach with a window size of 3 days and a step size of 2 days. This means that one day overlaps among consecutive test splits.
        - We ensure that each split uses at least half of the available samples for training.
        - We drop the ID column.
        - We convert prediction_time to datetime and sort by it.
        - We rename the target column to "rainfall" for better clarity.
        - We transform object columns and user_id to categorical.

        - Note: The split that would be ideal for the task would be grouped+temporal. However, the available data is not enough for this scenario. In general the available data size reduces the task quality a lot.
        - Anomaly: For this dataset it is possible that test folds don't contain some classes.
    """

    # Task
    target = "rainfall"
    problem_type = "multiclass_classification"
    metric = "f1_macro"
    time_on = "prediction_time"

    # Splits
    splits_comment = """
        We create 6 splits using a sliding window approach with a window size of 3 days and a step size of 2 days. This means that one day overlaps among consecutive test splits. We ensure that each split uses at least half of the available samples for training.
    """
    time_horizon = 3
    time_horizon_unit = "days"
    temporal_splits = TemporalSplits(window=3, unit="days", step=2, min_train_fraction=0.5)

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "train.csv")
        test_df = pd.read_csv(raw_dir / "test.csv")
        return {"df": df, "test_df": test_df}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        df, test_df = raw["df"], raw["test_df"]
        df = df.drop(columns=["ID"])
        test_df = test_df.drop(columns=["ID"])
        df["prediction_time"] = pd.to_datetime(df["prediction_time"])
        test_df["prediction_time"] = pd.to_datetime(test_df["prediction_time"])
        df = df.rename(columns={"Target": "rainfall"})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "user_id",
                "community",
                "district",
                "indicator",
                "indicator_description",
                "time_observed",
            ],
        )
