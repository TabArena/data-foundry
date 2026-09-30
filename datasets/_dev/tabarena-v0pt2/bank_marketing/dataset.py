"""Curated dataset definition for `bank_marketing` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class BankMarketing(AbstractCuratedDataset):
    # Dataset
    unique_name = "bank_marketing"
    year = "2012"
    domain = "finance"
    source = "UCI"
    source_url = "https://archive.ics.uci.edu/dataset/222/bank+marketing"
    license = "CC BY 4.0"
    download_description = """
        We download the data from the UCI repository and uzip it to a predefined folder.

        mkdir -p local-data-warehouse/bank_marketing/ && wget -P local-data-warehouse/bank_marketing/ https://archive.ics.uci.edu/static/public/222/bank+marketing.zip && unzip -o "local-data-warehouse/bank_marketing/bank+marketing.zip" -d local-data-warehouse/bank_marketing && unzip -o "local-data-warehouse/bank_marketing/bank.zip" -d local-data-warehouse/bank_marketing
    """
    bibtex = r"""
        @article{moro2014bank-marketing,
          title={A data-driven approach to predict the success of bank telemarketing},
          author={Moro, S{\'e}rgio and Cortez, Paulo and Rita, Paulo},
          journal={Decision Support Systems},
          volume={62},
          pages={22--31},
          year={2014},
          publisher={Elsevier}
        }
    """
    curation_comments = """
        - We removed the "duration" feature following its original description to obtain a "realistic predictive model".
        - We further remove the "month" and "day_of_week" features, as they also relate to the last contact -- which is not available in a real-world scenario.
    """

    # Task
    target = "SubscribeTermDeposit"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        data = pd.read_csv(f"{raw_dir}/bank-full.csv", sep=";")
        return data

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        data = raw
        # Concatenate the two datasets
        feature_names = [
            "age",
            "job",
            "marital",
            "education",
            "default",
            "balance",
            "housing",
            "loan",
            "contact",
            "day",
            "month",
            "duration",
            "campaign",
            "pdays",
            "previous",
            "poutcome",
            "SubscribeTermDeposit",
        ]
        data.columns = feature_names
        df = data
        df = df.drop(columns=["day", "month", "duration"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "job",
                "marital",
                "education",
                "default",
                "housing",
                "loan",
                "contact",
                "campaign",
                "previous",
                "poutcome",
            ],
        )
