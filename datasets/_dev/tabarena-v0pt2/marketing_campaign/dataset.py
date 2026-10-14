"""Curated dataset definition for `marketing_campaign` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TaskSummary


class MarketingCampaign(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a customer accept the offer of the company's next marketing campaign?",
        use_case=(
            "Before a campaign, a company decides which customers to send the offer to, to maximise the campaign's "
            "profit (the data card's task, from a SAS textbook)."
        ),
        row=(
            "One customer of a company (not named) selling wine, meat, fish, fruit, sweets and gold products in "
            "stores, by catalogue and on its website (2,240 customers)."
        ),
        predicted="Whether the customer accepted the offer of the last campaign.",
        known=(
            "Birth year, education, marital status, income, children at home, date of joining, days since the last "
            "purchase, spending per product type and purchases per channel over two years, website visits in the last"
            " month, a complaint flag, and whether the customer accepted each of five earlier campaigns."
        ),
        split="Random customers of the same campaign.",
        fit="approximate",
        fit_reason=(
            "One campaign stands in for the next, and the source does not say whether spending and visits were "
            "counted before the campaign. How the data was obtained is not documented; the curators suspect it may be"
            " artificial."
        ),
    )

    # Dataset
    unique_name = "marketing_campaign"
    year = "2019"
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
        df["Response"] = df["Response"].map({0: "No", 1: "Yes"})
        df["AcceptedCmp1"] = df["AcceptedCmp1"].map({0: "No", 1: "Yes"})
        df["AcceptedCmp2"] = df["AcceptedCmp2"].map({0: "No", 1: "Yes"})
        df["AcceptedCmp3"] = df["AcceptedCmp3"].map({0: "No", 1: "Yes"})
        df["AcceptedCmp4"] = df["AcceptedCmp4"].map({0: "No", 1: "Yes"})
        df["AcceptedCmp5"] = df["AcceptedCmp5"].map({0: "No", 1: "Yes"})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "AcceptedCmp1",
                "AcceptedCmp2",
                "AcceptedCmp3",
                "AcceptedCmp4",
                "AcceptedCmp5",
                "Marital_Status",
                "Education",
            ],
            datetime={"Dt_Customer": "%Y-%m-%d"},
        )
