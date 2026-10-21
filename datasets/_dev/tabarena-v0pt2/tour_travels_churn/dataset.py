"""Curated dataset definition for `tour_travels_churn` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TaskSummary


class TourTravelsChurn(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a customer of a tour and travel company churn?",
        use_case=(
            "A tour and travel company predicts which customers will churn (the data card's task), for example to "
            "target them with retention offers."
        ),
        row=(
            "One customer of an unnamed tour and travel company (954 customers); the place and period are not stated."
        ),
        predicted="Whether the customer churned; the time frame is not stated.",
        known=(
            "Age, whether the customer is a frequent flyer, annual income class, the number of services used, whether"
            " the account is linked to social media, and whether the customer booked a hotel."
        ),
        split="Random customers.",
        fit="approximate",
        fit_reason=(
            "The churn has no stated time frame and the features no stated timing; where the data comes from is "
            "unknown, and the curator would not be surprised if it were artificial."
        ),
    )

    # Dataset
    unique_name = "tour_travels_churn"
    year = "2021"
    domain = "business & marketing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/tejashvi14/tour-travels-customer-churn-prediction/"
    license = "CC0: Public Domain"
    data_tags = ("ForcedIIDFromTemporal",)
    download_description = """
        kaggle datasets download tejashvi14/tour-travels-customer-churn-prediction --unzip && mkdir -p local-data-warehouse/tour_travels_churn && mv Customertravel.csv local-data-warehouse/tour_travels_churn/
    """
    bibtex = r"""
        @misc{Tejashvi2023TourTravelsCustomerChurnPrediction,
          author = {Tejashvi},
          title  = {Tour & Travels Customer Churn Prediction},
          year   = {2023},
          howpublished = {\url{https://www.kaggle.com/datasets/tejashvi14/tour-travels-customer-churn-prediction}},
          note   = {Kaggle dataset}
        }
    """
    curation_comments = """
        The source of the data from Kaggle is unknown but the data distributions look reasonable enough to use. But I would also not be surprised if we find out the data is artificially created.

        - The split is forced (ForcedIIDFromTemporal, SPLIT-8): the company would train on customers whose churn is known by an earlier date and score its current ones, but the file is one undated snapshot. A dated window would test a model on a later season's customers, whose bookings and services may differ; the cost cannot be measured here.
    """

    # Task
    target = "Target"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "Customertravel.csv")
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "FrequentFlyer",
                "AnnualIncomeClass",
                "AccountSyncedToSocialMedia",
                "BookedHotelOrNot",
            ],
        )
