"""Curated dataset definition for `bank_customer_churn` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary


class BankCustomerChurn(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a bank customer leave the bank?",
        use_case=(
            "For example, a retail bank scores its current customers to decide whom to approach with a retention "
            "offer before they leave."
        ),
        row=(
            "One customer of a bank in France, Germany or Spain (10,000 customers); the bank, the period and the "
            "original source are not stated."
        ),
        predicted=("Whether the customer left the bank (20% did); the time window for leaving is not stated."),
        known=(
            "Credit score, country, gender, age, years with the bank, account balance, number of products, whether "
            "the customer has a credit card and is an active member, and an estimated salary."
        ),
        split=("Random customers, so the test data stands for other customers of the same bank at the same time."),
        fit="approximate",
        fit_reason=(
            "The file is one snapshot with no stated horizon, and it is not stated whether the balance and activity "
            "were recorded before the customer left. It most likely comes from a data science course, and its origin "
            "is unclear."
        ),
    )

    # Dataset
    unique_name = "bank_customer_churn"
    year = "2022"
    domain = "business & marketing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/gauravtopre/bank-customer-churn-dataset"
    data_tags = ("ForcedIIDFromTemporal",)
    license = None  # Kaggle says "Other (specified in description)", and the description names none
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
        - The split is forced (ForcedIIDFromTemporal, SPLIT-8): a bank would train on customers whose leaving is known by an earlier date and score its current customers, but the file is one undated snapshot. A dated window would test a model on customers of a later period, after shifts in balances, products and the bank's offers; the cost cannot be measured here. Recover dates if the source turns up.
    """

    accepted_check_warnings = {
        "meta_license_unknown": (
            "Kaggle gives the licence as 'Other (specified in description)', but the description names none; no other "
            "licence is known (Lennart, 2026-10-14)."
        ),
    }

    # Task
    target = "churn"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason="Kaggle dataset (likely a course dataset) with no stated task metric; no first publication",
    )

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
