"""Curated dataset definition for `credit_card_clients_default` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TaskSummary


class CreditCardClientsDefault(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a credit card holder miss next month's payment?",
        use_case=(
            "For example, a card issuer at the end of a month estimates each client's chance of defaulting on the "
            "next payment, to adjust credit limits or start collection early."
        ),
        row=(
            "One credit card client of a bank in Taiwan, with six months of history from April to September 2005 "
            "(30,000 clients)."
        ),
        predicted="Whether the client defaults on the payment of the following month (22% do).",
        known=(
            "The credit limit, sex, education, marital status and age, and for each of the six months the repayment "
            "status (paid on time or months of delay), the bill amount and the amount paid."
        ),
        split="Random clients of the same bank and the same months.",
        fit="approximate",
        fit_reason=(
            "The file is one snapshot: every client is scored for the same month, so training and test share that "
            "month's conditions, where a bank trains on earlier months and scores the next."
        ),
    )

    # Dataset
    unique_name = "credit_card_clients_default"
    year = "2016"
    domain = "finance"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C55S3H"
    license = "CC BY 4.0"
    download_description = """
        We download the data from the UCI repository and uzip it to a predefined folder.

        mkdir -p local-data-warehouse/credit_card_clients_default/ && wget -P local-data-warehouse/credit_card_clients_default/ https://archive.ics.uci.edu/static/public/350/default+of+credit+card+clients.zip && unzip local-data-warehouse/credit_card_clients_default/default+of+credit+card+clients.zip -d local-data-warehouse/credit_card_clients_default/ && rm local-data-warehouse/credit_card_clients_default/default+of+credit+card+clients.zip
    """
    bibtex = """
        @article{yeh2009comparisons,
          title={The comparisons of data mining techniques for the predictive accuracy of probability of default of credit card clients},
          author={Yeh, I-Cheng and Lien, Che-hui},
          journal={Expert systems with applications},
          volume={36},
          number={2},
          pages={2473--2480},
          year={2009},
          publisher={Elsevier}
        }
    """
    curation_comments = """
        - We rename the target variable and restore the original class names.
        - We drop the "ID" column.
        - Anomaly: the data has temporal features but the task is time-invariant.
    """

    # Task
    target = "DefaultOnPaymentNextMonth"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_excel(raw_dir / "default of credit card clients.xls", skiprows=[0])
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.drop(columns=["ID"])
        target_feature = "DefaultOnPaymentNextMonth"
        df = df.rename(columns={"default payment next month": target_feature})
        df[target_feature] = df[target_feature].map({1: "Yes", 0: "No"})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "SEX",
                "MARRIAGE",
                "EDUCATION",
            ],
        )
