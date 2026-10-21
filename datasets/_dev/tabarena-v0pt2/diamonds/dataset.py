"""Curated dataset definition for `diamonds` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary


class Diamonds(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What is the price of a diamond with these grading characteristics?",
        use_case=(
            "For example, an online diamond seller prices a newly listed stone from its grading (weight, cut, colour,"
            " clarity, proportions), in line with the rest of its catalogue."
        ),
        row=(
            "One diamond with its price, from the diamonds data of the ggplot2 R package (53,940 stones); the seller "
            "and the date of the prices are not stated."
        ),
        predicted="The price in US dollars.",
        known=(
            "Weight in carats, cut quality, colour grade, clarity grade, total depth and table width in percent, and "
            "length, width and depth in millimetres."
        ),
        split="Random stones, so the test data stands for other stones of the same price list.",
        fit="direct",
        fit_reason=(
            "The features are the grading a seller has before pricing a stone, and random stones of one price list "
            "match pricing new stock against it. Neither the seller nor the date of the prices is stated."
        ),
    )

    # Dataset
    unique_name = "diamonds"
    year = "2007"
    domain = "business & marketing"
    source = "Other"
    source_url = "https://github.com/tidyverse/ggplot2/blob/main/data-raw/diamonds.csv"
    license = "MIT License"
    download_description = """
        We download the CSV directly from the ggplot2 GitHub repository.

        mkdir -p local-data-warehouse/diamonds/ && wget -O local-data-warehouse/diamonds/original_diamonds.csv https://raw.githubusercontent.com/tidyverse/ggplot2/main/data-raw/diamonds.csv
    """
    bibtex = """
        @incollection{wickham2016data,
          title={Data analysis},
          author={Wickham, Hadley},
          booktitle={ggplot2: Elegant graphics for data analysis},
          pages={189--201},
          year={2016},
          publisher={Springer}
        }
    """
    curation_comments = """
        - The price ships in US dollars and is scored by RMSLE (Lennart, 2026-10-21): a price's error matters relative
          to the price, which an earlier version got by log-scaling the target.
    """

    # Task
    target = "price"
    problem_type = "regression"
    metric = Metric.from_context(
        "rmsle",
        reason=(
            "A teaching dataset of the ggplot2 package defines no task or score; for a price the error that matters "
            "is relative to the price (a $500 miss means more on a $1,000 stone than on a $15,000 one), so RMSLE."
        ),
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/original_diamonds.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        return raw

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "cut",
                "color",
                "clarity",
            ],
        )
