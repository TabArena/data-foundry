"""Curated dataset definition for `bank_customer_churn` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class BankCustomerChurn(AbstractCuratedDataset):
    # Dataset
    unique_name = "bank_customer_churn"
    year = "2020"
    domain = "business & marketing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/gauravtopre/bank-customer-churn-dataset"
    license = "Public Domain"
    download_description = """
        We download the data from Kaggle to a .csv file in a predefined folder.

        mkdir -p local-data-warehouse/bank_customer_churn && cd local-data-warehouse/bank_customer_churn && kaggle datasets download gauravtopre/bank-customer-churn-dataset && unzip bank-customer-churn-dataset.zip && rm bank-customer-churn-dataset.zip && cd ../../
    """
    bibtex = """
        @misc{Topre2022BankCustomerChurn,
          title={Bank Customer Churn Dataset},
          author={Gaurav Topre},
          year={2022},
          publisher={Kaggle},
          url={https://www.kaggle.com/datasets/gauravtopre/bank-customer-churn-dataset}
        }
    """
    curation_comments = """
        - We remove the customer_id column.
    """

    # Task
    target = "churn"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "Bank Customer Churn Prediction.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df["churn"] = df["churn"].map({1: "Yes", 0: "No"})
        df = df.drop(columns=["customer_id"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "active_member",
                "country",
                "gender",
                "credit_card",
            ],
        )
