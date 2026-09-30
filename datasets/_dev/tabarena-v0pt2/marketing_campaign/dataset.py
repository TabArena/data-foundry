"""Curated dataset definition for `marketing_campaign` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class MarketingCampaign(AbstractCuratedDataset):
    # Dataset
    unique_name = "marketing_campaign"
    year = "2020"
    domain = "business & marketing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/rodsaldanha/arketing-campaign"
    license = "CC BY 4.0"
    download_description = """
        We download the data from the Kaggle repository and uzip it to a predefined folder.

        mkdir -p local-data-warehouse/marketing_campaign/ && cd local-data-warehouse/marketing_campaign/ && kaggle datasets download rodsaldanha/arketing-campaign && cd ../../ && unzip local-data-warehouse/marketing_campaign/arketing-campaign.zip -d local-data-warehouse/marketing_campaign/ && rm local-data-warehouse/marketing_campaign/arketing-campaign.zip && rm local-data-warehouse/marketing_campaign/marketing_campaign.xlsx
    """
    bibtex = r"""
        @misc{saldanha2020marketing,
          author       = {Saldanha, Rodolfo},
          title        = {Marketing Campaign},
          year         = {2020},
          howpublished = {\url{https://www.kaggle.com/datasets/rodsaldanha/arketing-campaign}},
          note         = {Kaggle dataset},
        }
    """
    curation_comments = """
        - We ensure Dt_Customer is a pandas datetime.
        - We drop the ID column.
        - We rename the values of the target variable to be more descriptive.
        - We drop constant columns.
    """

    # Task
    target = "Response"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/marketing_campaign.csv", sep=";")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df.drop(columns=["ID", "Z_CostContact", "Z_Revenue"], inplace=True)
        cat_features = [
            "AcceptedCmp1",
            "AcceptedCmp2",
            "AcceptedCmp3",
            "AcceptedCmp4",
            "AcceptedCmp5",
            "Marital_Status",
            "Education",
            "Response",
        ]
        df[cat_features] = df[cat_features].astype("category")
        df["Response"] = df["Response"].map({0: "No", 1: "Yes"})
        df["AcceptedCmp1"] = df["AcceptedCmp1"].map({0: "No", 1: "Yes"})
        df["AcceptedCmp2"] = df["AcceptedCmp2"].map({0: "No", 1: "Yes"})
        df["AcceptedCmp3"] = df["AcceptedCmp3"].map({0: "No", 1: "Yes"})
        df["AcceptedCmp4"] = df["AcceptedCmp4"].map({0: "No", 1: "Yes"})
        df["AcceptedCmp5"] = df["AcceptedCmp5"].map({0: "No", 1: "Yes"})
        df["Dt_Customer"] = pd.to_datetime(df["Dt_Customer"], format="%Y-%m-%d")
        return df
