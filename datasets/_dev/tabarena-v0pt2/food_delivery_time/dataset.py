"""Curated dataset definition for `food_delivery_time` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TaskSummary


class FoodDeliveryTime(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How many minutes will a food delivery take?",
        use_case=(
            "For example, a food-delivery platform, when it assigns an order to a courier, estimates the delivery "
            "time to show the customer and to plan the courier's next orders."
        ),
        row=(
            "One delivered order of a food-delivery platform (45,451 orders, Kaggle 2023); place and period not stated."
        ),
        predicted="The delivery time in minutes (10 to 54, 26 on average).",
        known=(
            "The courier's ID, age and rating, the vehicle (motorcycle, scooter and others), the order type (snack, "
            "meal, drinks, buffet), and the coordinates of the restaurant and of the delivery address, which is the "
            "restaurant plus one of 12 fixed offsets."
        ),
        split=(
            "Random orders, so the test data stands for other orders of the same couriers and period; a courier's "
            "other orders can be in training."
        ),
        changes="We correct the sign of 424 restaurant coordinates; restaurants at (0, 0), a missing code, stay.",
        fit="approximate",
        fit_reason=(
            "The release has no order time, so the test orders are a random draw from the period rather than later "
            "orders, and time of day, traffic and weather are missing. Whether a courier's rating includes later "
            "orders is not stated."
        ),
    )

    # Dataset
    unique_name = "food_delivery_time"
    year = "2023"
    domain = "business & marketing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/rajatkumar30/food-delivery-time"
    license = "Database Contents License (DbCL) v1.0"
    data_tags = ("ForcedIIDFromTemporal",)
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
        - We flip the sign of the restaurant's latitude in 424 rows (159 also its longitude): the same restaurants appear elsewhere with positive coordinates, as all of India has.
        - 3,630 rows (8%) have the restaurant at (0, 0), a missing-value code. We keep them as they are: the delivery point is still the offset, so the distance is right, and their mean time (26.1 min) matches the rest (26.3).
        - The delivery point is always the restaurant plus one of 12 equal offsets in latitude and longitude (0.01 to 0.14 degrees), so the delivery addresses are synthetic and only the distance class carries information.
        - Tagged ForcedIIDFromTemporal: orders arrive over time, but the release has no order date or time, so the split is random.
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
        # 424 restaurant latitudes (159 longitudes) carry a flipped sign; India lies at positive coordinates
        for c in ["Restaurant_latitude", "Restaurant_longitude"]:
            df[c] = df[c].abs()
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "Delivery_person_ID",
                "Type_of_order",
                "Type_of_vehicle",
            ],
        )
