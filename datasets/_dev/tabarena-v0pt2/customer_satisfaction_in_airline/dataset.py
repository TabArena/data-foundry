"""Curated dataset definition for `customer_satisfaction_in_airline` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class CustomerSatisfactionInAirline(AbstractCuratedDataset):
    # Dataset
    unique_name = "customer_satisfaction_in_airline"
    year = "2023"
    domain = "biology & life sciences"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/yakhyojon/customer-satisfaction-in-airline"
    license = "Public Domain"
    download_description = """
        We download the data from Kaggle and uzip it to a predefined folder.

        mkdir -p local-data-warehouse/customer_satisfaction_in_airline/ && cd local-data-warehouse/customer_satisfaction_in_airline/ && kaggle datasets download yakhyojon/customer-satisfaction-in-airline && cd ../../ && unzip local-data-warehouse/customer_satisfaction_in_airline/customer-satisfaction-in-airline.zip -d local-data-warehouse/customer_satisfaction_in_airline/ && rm local-data-warehouse/customer_satisfaction_in_airline/customer-satisfaction-in-airline.zip
    """
    bibtex = """
        @misc{yakhyojon2023airlinesatisfaction,
            author = {Kaggle User Yakhyojon},
            title = {Customer Satisfaction in Airline.},
            year = {2023},
            howpublished = {url{https://www.kaggle.com/datasets/yakhyojon/customer-satisfaction-in-airline}},
            note = {Kaggle}
        }
    """
    curation_comments = """
        - We renamed the target column from "satisfaction" to "satisfied" for clarity and mapped the values to "Yes" and "No"
    """

    # Task
    target = "satisfied"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/Invistico_Airline.csv", header=0)
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df.rename(columns={"satisfaction": "satisfied"}, inplace=True)
        df["satisfied"] = df["satisfied"].map({"satisfied": "Yes", "dissatisfied": "No"})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "Customer Type",
                "Type of Travel",
                "Class",
                "Seat comfort",
                "Departure/Arrival time convenient",
                "Food and drink",
                "Gate location",
                "Inflight wifi service",
                "Inflight entertainment",
                "Online support",
                "Ease of Online booking",
                "On-board service",
                "Leg room service",
                "Baggage handling",
                "Checkin service",
                "Cleanliness",
                "Online boarding",
            ],
        )
