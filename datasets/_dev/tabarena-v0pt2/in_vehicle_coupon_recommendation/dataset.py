"""Curated dataset definition for `in_vehicle_coupon_recommendation` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Grouping, anonymize_ids

RESPONDENT_COLUMNS = [
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
]
"""Answers to the survey's first part (demographics and habits), asked once per respondent."""


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
        - We simulate a cold-start model (as used before a recommender has any history for a user): predict whether a person accepts a coupon from their profile, stated habits and the scenario, for people not seen in training. The data is a survey (Wang et al. 2017, Sec. 6.2): each MTurk respondent first gave demographics and preferences, then answered hypothetical driving scenarios (22 per person in the file, 19 fixed questionnaire versions), all in one sitting and without timestamps, so there is no real interaction history for a warm-start setting. A random split puts about two-thirds of each person's other answers in train, which lets a model learn that person's tendency to say yes (ROC AUC 0.83 random vs 0.76 grouped; leak audit 2026-09-24).
        - The respondent id is not shipped with the data. The raw file lists each respondent's answers as a consecutive block with identical first-part answers, so a block of the same profile is one respondent: 587 blocks, 517 of them with 22 rows, against 652 accepted surveys in the paper, so a few blocks likely merge two adjacent respondents with identical profiles, which only makes the grouping stricter. The paper reports out-of-sample AUC from 5-fold testing (Table 3) without saying whether folds were split by respondent; a random split would be a warm start.
    """

    # Task
    target = "AcceptCoupon"
    problem_type = "binary_classification"
    grouping = Grouping(
        on="respondent",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a survey respondent; its rows are the coupon offers in about 20 driving scenarios, answered in one sitting (Wang et al. 2017). The use case is an in-vehicle recommender for a new user (cold start), so each offer is one prediction, made from its own row; without timestamps, a warm start cannot be simulated.
        """,
    )

    # Splits
    splits_comment = """
        Grouped splits on the survey respondent: all answers of one person stay on one side, so the task is a cold-start
        model that predicts a new person's response from their profile, stated habits and the driving scenario.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/in-vehicle-coupon-recommendation.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # The raw file lists each respondent's answers as one consecutive block with the same first-part answers;
        # a block is one respondent (or, rarely, two adjacent respondents with identical answers)
        profile = df[RESPONDENT_COLUMNS].astype(str).agg("|".join, axis=1)
        block = (profile != profile.shift()).cumsum()
        df["respondent"] = anonymize_ids(block.astype(str))
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
                "respondent",
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
