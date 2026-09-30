"""Curated dataset definition for `food_delivery_time` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class FoodDeliveryTime(AbstractCuratedDataset):
    # Dataset
    unique_name = "food_delivery_time"
    year = "2023"
    domain = "business & marketing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/rajatkumar30/food-delivery-time"
    license = "Database Contents License (DbCL) v1.0"
    download_description = """
        kaggle datasets download -d rajatkumar30/food-delivery-time -p local-data-warehouse/food_delivery_time/ --unzip
    """
    bibtex = r"""
        @misc{rajatkumar302023food,
          author       = {Kaggle User Rajatkumar30},
          title        = {Food Delivery Time},
          year         = {2023},
          howpublished = {\url{https://www.kaggle.com/datasets/rajatkumar30/food-delivery-time}},
          note         = {Kaggle dataset},
        }
    """
    curation_comments = """
        - We dropped entries with a duplicated ID, keeping only the first one.
        - We dropped the ID column.
        - Anomaly: The ID of the delivery person is given as a feature. In some contexts, this feature might not be allowed to use. Moreover, using this information might require considering a temporal split where a cold-start problem is covered.
    """

    # Task
    target = "Time_taken(min)"
    problem_type = "regression"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/deliverytime.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.drop_duplicates(subset=["ID"])
        df = df.drop(columns=["ID"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "Delivery_person_ID",
                "Type_of_order",
                "Type_of_vehicle",
            ],
        )
