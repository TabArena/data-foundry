"""Curated dataset definition for `in_vehicle_coupon_recommendation` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class InVehicleCouponRecommendation(AbstractCuratedDataset):
    # Dataset
    unique_name = "in_vehicle_coupon_recommendation"
    year = "2017"
    domain = "business & marketing"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5GS4P"
    license = "CC BY 4.0"
    download_description = """
        We download the data from the UCI repository and uzip it to a predefined folder.

        mkdir -p local-data-warehouse/in_vehicle_coupon_recommendation/ && wget -P local-data-warehouse/in_vehicle_coupon_recommendation/ https://archive.ics.uci.edu/static/public/603/in+vehicle+coupon+recommendation.zip && unzip local-data-warehouse/in_vehicle_coupon_recommendation/in+vehicle+coupon+recommendation.zip -d local-data-warehouse/in_vehicle_coupon_recommendation/
    """
    bibtex = """
        @article{wang2017bayesian,
          title={A bayesian framework for learning rule sets for interpretable classification},
          author={Wang, Tong and Rudin, Cynthia and Doshi-Velez, Finale and Liu, Yimin and Klampfl, Erica and MacNeille, Perry},
          journal={Journal of Machine Learning Research},
          volume={18},
          number={70},
          pages={1--37},
          year={2017}
        }
    """
    curation_comments = """
        - We renamed the target feature and its value to be more descriptive.
        - We removed text data from the "time" feature to make it numeric.
        - We drop constant columns.
        - We fixed a typo in the feature names.
        - Anomaly: the data has many binned numeric features that are treated as categorical features with text describing the bins.
        - Anomaly: the numeric features in the dataset are low-cardinality (<25)
    """

    # Task
    target = "AcceptCoupon"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/in-vehicle-coupon-recommendation.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        target_feature = "AcceptCoupon"
        df = df.rename(columns={"Y": target_feature})
        df[target_feature] = df[target_feature].map({0: "No", 1: "Yes"})
        # Transform time to 24-hour format to be fully numeric.
        df["time"] = (
            df["time"]
            .apply(lambda x: int(x.replace("AM", "")) if "AM" in x else int(x.replace("PM", "")) + 12)
            .astype(int)
        )
        # Drop constant columns
        df = df.drop(columns=["toCoupon_GEQ5min"])
        df = df.rename(columns={"passanger": "passenger"})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "expiration",
                "destination",
                "passenger",
                "weather",
                "coupon",
                "gender",
                "age",
                "maritalStatus",
                "has_children",
                "education",
                "occupation",
                "income",
                "car",
                "Bar",
                "CoffeeHouse",
                "CarryAway",
                "RestaurantLessThan20",
                "Restaurant20To50",
                "toCoupon_GEQ15min",
                "toCoupon_GEQ25min",
                "direction_same",
                "direction_opp",
            ],
        )
