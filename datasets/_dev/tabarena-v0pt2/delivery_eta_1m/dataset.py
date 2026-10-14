"""Curated dataset definition for `delivery_eta_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TaskSummary, Temporal, TemporalSplits


class DeliveryEta1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How long will it take to deliver an order from an online grocery store?",
        use_case=(
            "When an order is placed, the grocery service estimates its delivery time, for example to show the "
            "customer an arrival time and to plan couriers; the model is refit every week (TabReD)."
        ),
        row=(
            "One order of an online grocery store between 20 October 2023 and 7 January 2024 (TabReD release; the "
            "store is not named)."
        ),
        predicted=(
            "The time the delivery took, in minutes on a logarithmic scale; orders under one minute are left out."
        ),
        known=(
            "221 anonymised features built from courier availability, navigation data and other aggregates (TabReD), "
            "including the time of the order."
        ),
        split=(
            "Each test window is one of the last three weeks (18 December 2023 to 7 January 2024), up to 500,000 "
            "orders each; training is a random million of all earlier orders, as for a model refit every week."
        ),
        fit="direct",
        fit_reason=(
            "Courier availability and route data are known when an order is placed, and the windows follow a weekly "
            "refit. The features are anonymised, so their timing cannot be checked."
        ),
    )

    # Dataset
    unique_name = "delivery_eta_1m"
    version_of = "delivery_eta"
    version_comment = """
        We sample per test window (v2 split protocol): each window keeps at most 500k of its rows, and its train side is a random 1M of all earlier rows, drawn in one random order for all windows; the frame keeps only the rows a split uses. We follow TabReD and use random sub-sampling of the train data. The idea behind this instead of a time-based subsampling is to keep data from various time periods and model the distribution shift across the full time horizon.
    """
    year = "2024"
    domain = "industry & manufacturing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/pcovkrd84mejm/delivery-eta"
    license = "CC-BY-NC-SA-4.0"
    data_tags = ("Anonymized",)
    download_description = """
        We download the data from Kaggle.

        kaggle datasets download -d pcovkrd84mejm/delivery-eta -f delivery_eta.parquet && unzip delivery_eta.parquet.zip && rm delivery_eta.parquet.zip && mkdir -p local-data-warehouse/delivery_eta && mv delivery_eta.parquet local-data-warehouse/delivery_eta/
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

        - We drop orders with a delivery time under one minute (386k of 17.0M, 2.3%), as TabReD's preprocessing does.
        - The target is the natural log of the minutes, as in TabReD (the column keeps its name). TabReD's reason, stated for its cooking-time data and applied here too: the times are right-skewed, and squared error on the log is close to absolute error on the minutes, the error that matters for the task.
        - We drop a duplicated column `cat_2` in the preprocessing.
        - We drop `num_29`, `num_36` and `num_71`, which are constant except in the same 2 of 16.7M rows (both hold 5.199 in all three columns), and `num_101`, which has a single value and is missing in exactly the rows where 19 other columns are missing, so it carries no information of its own.
    """

    # Task
    target = "delivery_eta_minutes"
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
        df = pd.read_parquet(raw_dir / "delivery_eta.parquet")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Following TabRed
        df = df[df["delivery_eta_minutes"] >= 1.0]
        df["delivery_eta_minutes"] = np.log(df["delivery_eta_minutes"])
        df = df.drop(columns=["cat_2", "num_29", "num_36", "num_71", "num_101"])
        df = df.sort_values(by="timestamp", kind="stable").reset_index(drop=True)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # We take all bin + cat as Category
        return FeatureTypes(
            categorical=[c for c in df.columns if c.startswith(("cat", "bin"))],
            datetime=["timestamp"],
        )
