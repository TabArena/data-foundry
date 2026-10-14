"""Curated dataset definition for `wine_world_cost` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TaskSummary


class WineWorldCost(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What does a bottle of wine cost, given its description?",
        use_case=(
            "For example, a wine merchant sets the shelf price of a newly listed wine from its attributes and tasting"
            " notes, or checks a supplier's price against similar wines."
        ),
        row=(
            "One wine sold by the bottle in a UK online wine shop, priced in pounds and scraped in 2023 (1,279 wines;"
            " most likely Majestic Wine, which 78 descriptions name)."
        ),
        predicted="The price of one bottle in pounds, on a log scale.",
        known=(
            "The wine's name and the shop's description, grapes, country, region and appellation, colour, style, "
            "tasting characteristics, closure, bottle size, alcohol content and vintage year."
        ),
        split="Random wines of the same shop and time.",
        fit="direct",
        fit_reason=(
            "The attributes and the description exist when a wine is listed, and no description states the wine's own"
            " price (its price wording adds 0.003 R²). The task covers one shop's range at one time."
        ),
    )

    # Dataset
    unique_name = "wine_world_cost"
    year = "2023"
    domain = "business & marketing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/elvinrustam/wine-dataset"
    license = "CC0: Public Domain"
    download_description = """
        There are many different wine datasets available, but this one is a comprehensive collection of wine-related data that includes information on various wine characteristics and text. So we stick to it.

        kaggle datasets download elvinrustam/wine-dataset && unzip wine-dataset.zip && rm wine-dataset.zip
        mkdir -p local-data-warehouse/wine_world_cost && mv WineDataset.csv local-data-warehouse/wine_world_cost
    """
    bibtex = r"""
        @misc{Rustamov2023WineDataset,
          author = {Elvin Rustamov},
          title  = {Wine Dataset},
          year   = {2023},
          howpublished = {\url{https://www.kaggle.com/datasets/elvinrustam/wine-dataset}},
          note   = {Kaggle dataset}
        }
    """
    curation_comments = """
        We start with the Kaggle version. We resolve several issues from the web scrapper.

        - We create a task to predict the price per bottle. We remove the 11 rows that have price information per case or each.
        - Create the price target by parsing the price column.
        - We map capacity to numeric values in ML.
        - We parse the ABV to a numeric value
        - We parse the vintage to a numeric date value, ensuring that each wine maps to the oldest year in its special syntax.
        - We log scale the target, as the price distribution is very skewed.
        - No description states the wine's own price. Removing every sentence with price or value words changes R^2 by 0.003, so we keep the description (evidence in the record, 2026-10-14).
    """

    # Task
    target = "Price"
    problem_type = "regression"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "WineDataset.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df[df["Per bottle / case / each"] == "per bottle"].reset_index(drop=True)
        df["Price"] = df["Price"].apply(lambda x: x.replace("£", "").replace(" per bottle", "")).astype(float)
        df["ABV%"] = df["ABV"].apply(lambda x: str(x).replace("ABV ", "").replace("%", "")).astype(float)
        df["Capacity"] = (
            df["Capacity"]
            .map(
                {
                    "75CL": 750,
                    "37.5CL": 375,
                    "1.5LTR": 1500,
                    "750ML": 750,
                    "150CL": 1500,
                    "50CL": 500,
                    "70CL": 700,
                    "500ML": 500,
                    "375ML": 375,
                    "300CL": 3000,
                }
            )
            .astype(float)
        )
        df["VintageYear"] = pd.to_datetime(df["Vintage"].apply(lambda x: x.split("/")[0]).replace("NV", np.nan)).dt.year
        df = df.drop(
            columns=[
                # Constant
                "Per bottle / case / each",
                # Meaning of feature is missing, and it is unclear how to interpret it
                "Unit",
                # Copied columns
                "ABV",
                "Vintage",
            ]
        )
        # Log scale target
        df["Price"] = np.log(df["Price"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "Closure",
                "Type",
                "Style",
            ],
            string=[
                "Title",
                "Description",
                "Grape",
                "Secondary Grape Varieties",
                "Country",
                "Characteristics",
                "Region",
                "Appellation",
            ],
        )
