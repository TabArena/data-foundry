"""Curated dataset definition for `tour_travels_churn` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class TourTravelsChurn(AbstractCuratedDataset):
    # Dataset
    unique_name = "tour_travels_churn"
    year = "2021"
    domain = "business & marketing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/tejashvi14/tour-travels-customer-churn-prediction/"
    license = "CC0: Public Domain"
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
