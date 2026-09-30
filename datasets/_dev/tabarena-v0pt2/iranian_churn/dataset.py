"""Curated dataset definition for `iranian_churn` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class IranianChurn(AbstractCuratedDataset):
    # Dataset
    unique_name = "iranian_churn"
    year = "2011"
    domain = "business & marketing"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5JW3Z"
    license = "CC BY 4.0"
    download_description = """
        mkdir -p local-data-warehouse/iranian_churn && wget -P local-data-warehouse/iranian_churn/ https://archive.ics.uci.edu/static/public/563/iranian+churn+dataset.zip && unzip local-data-warehouse/iranian_churn/iranian+churn+dataset.zip -d local-data-warehouse/iranian_churn/ && rm local-data-warehouse/iranian_churn/iranian+churn+dataset.zip
    """
    bibtex = """
        @article{keramati2011churn,
          title={Churn analysis for an Iranian mobile operator},
          author={Keramati, Abbas and Ardabili, Seyed MS},
          journal={Telecommunications Policy},
          volume={35},
          number={4},
          pages={344--356},
          year={2011},
          publisher={Elsevier}
        }
    """
    curation_comments = """
        - The data collection process for the task is not ideal. The data was collected for each individual right up to the churn month. That means, for the churners we observed varying length periods, while for the other individuals we observed the full period.
        - Nevertheless, the features are not collected after the churn and the task is still valid, if we conceptualize it as “identify customers close to churn” rather than “predict churn ahead of time”.
        - We remove exact duplicates (9.52% of the samples) from the data to avoid leaks. The data contains features like "Seconds of Use", "Frequency of use", "Frequency of SMS", "Distinct Called Numbers", and most importantly a customer value assignment. Given just 3000 samples, it is reasonable to assume that if feature values with so many degrees of freedom are exactly the same, they belong to the same customer.
    """

    # Task
    target = "Churn"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "Customer Churn.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.drop_duplicates().reset_index(drop=True)
        df["Tariff Plan"] = df["Tariff Plan"].map({1: "Pay as you go", 2: "Contractual"})
        df["Status"] = df["Status"].map({1: "Active", 2: "Non-active"})
        df["Churn"] = df["Churn"].map({1: "Churn", 0: "Non-churn"})
        df["Complains"] = df["Complains"].map({0: "No complaint", 1: "Complaint"})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "Tariff Plan",
                "Complains",
                "Status",
            ],
        )
