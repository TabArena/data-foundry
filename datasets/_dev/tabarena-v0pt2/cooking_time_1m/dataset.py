"""Curated dataset definition for `cooking_time_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TaskSummary, Temporal, TemporalSplits


class CookingTime1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How long will a restaurant take to cook an order placed through a food delivery app?",
        use_case=(
            "When an order is placed, the delivery service estimates the restaurant's cooking time, for example to "
            "time the courier and the delivery estimate shown to the customer; the model is refit every week "
            "(TabReD)."
        ),
        row=(
            "One order placed through a food delivery app between 15 November 2023 and 3 January 2024 (TabReD "
            "release; the service is not named)."
        ),
        predicted=(
            "The time the restaurant took to cook the order, in minutes on a logarithmic scale; orders under one "
            "minute are left out."
        ),
        known=(
            "196 anonymised features built from the order's contents and the restaurant's past cooking times "
            "(TabReD), including the time of the order."
        ),
        split=(
            "Each test window is one of the last three weeks (14 December 2023 to 3 January 2024), up to 500,000 "
            "orders each; training is a random million of all earlier orders, as for a model refit every week."
        ),
        fit="direct",
        fit_reason=(
            "Order contents and past cooking times are known when an order is placed, and the windows follow a weekly"
            " refit. The features are anonymised, so their timing cannot be checked."
        ),
    )

    # Dataset
    unique_name = "cooking_time_1m"
    version_of = "cooking_time"
    version_comment = """
        We sample per test window (v2 split protocol): each window keeps at most 500k of its rows, and its train side is a random 1M of all earlier rows, drawn in one random order for all windows; the frame keeps only the rows a split uses. We follow TabReD and use random sub-sampling of the train data. The idea behind this instead of a time-based subsampling is to keep data from various time periods and model the distribution shift across the full time horizon.
    """
    year = "2024"
    domain = "industry & manufacturing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/pcovkrd84mejm/cooking-time"
    license = "CC-BY-NC-SA-4.0"
    data_tags = ("Anonymized",)
    download_description = """
        We get the TabRed data from Kaggle.

        kaggle datasets download -d pcovkrd84mejm/cooking-time -f cooking_time.parquet && unzip cooking_time.parquet.zip && rm cooking_time.parquet.zip
        mkdir -p local-data-warehouse/cooking_time && mv cooking_time.parquet local-data-warehouse/cooking_time/
    """
    bibtex = """
        @inproceedings{rubachev2025tabred,
          title={TabReD: Analyzing Pitfalls and Filling the Gaps in Tabular Deep Learning Benchmarks},
          author={Rubachev, Ivan and Kartashev, Nikolay and Gorishniy, Yury and Babenko, Artem},
          booktitle={The Thirteenth International Conference on Learning Representations},
          year={2025},
        }
    """
    curation_comments = """
        We start with data from TabRed, which already comes preprocessed.

        - We drop orders with a cooking time under one minute (168 of 12.8M, 26 of them zero or negative), as TabReD's preprocessing does.
        - The target is the natural log of the minutes, as in TabReD (the column keeps its name). TabReD's reason: the times are right-skewed, and squared error on the log is close to absolute error on the minutes, the error that matters for the task.
    """

    # Task
    target = "cooking_time_minutes"
    problem_type = "regression"

    # Splits
    splits_comment = (
        "We use each of the last 3 weeks as a test window (newest first) and all prior data as train data. Each "
        "window keeps at most 500k of its rows; each train side is a random 1M of all earlier rows (one random order "
        "for all windows)."
    )
    temporal = Temporal(
        on="timestamp",
        splits=TemporalSplits(window=7, unit="days", n_windows=3),
    )
    subsample_to_budget = True

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_parquet(raw_dir / "cooking_time.parquet")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Following TabRed
        df = df[df["cooking_time_minutes"] >= 1.0]
        df["cooking_time_minutes"] = np.log(df["cooking_time_minutes"])
        df = df.sort_values(by="timestamp", kind="stable").reset_index(drop=True)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            # We take all bin + cat as Category
            categorical=[c for c in df.columns if c.startswith(("cat", "bin"))],
            datetime=["timestamp"],
        )
