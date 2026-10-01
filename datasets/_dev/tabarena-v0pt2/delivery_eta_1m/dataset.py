"""Curated dataset definition for `delivery_eta_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TemporalSplits


class DeliveryEta1m(AbstractCuratedDataset):
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

        - We drop a duplicated column `cat_2` in the preprocessing.
        - We drop `num_29`, `num_36` and `num_71`, which are constant except in the same 2 of 16.7M rows (both hold 5.199 in all three columns), and `num_101`, which has a single value and is missing in exactly the rows where 19 other columns are missing, so it carries no information of its own.
    """

    # Task
    target = "delivery_eta_minutes"
    problem_type = "regression"
    time_on = "timestamp"

    # Splits
    splits_comment = (
        "We use each of the last 3 weeks as a test window (newest first) and all prior data as train data. Each "
        "window keeps at most 500k of its rows; each train side is a random 1M of all earlier rows (one random order "
        "for all windows)."
    )
    time_horizon = 7
    time_horizon_unit = "days"
    temporal_splits = TemporalSplits(window=7, unit="days", n_windows=3)
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
        df = df.sort_values(by="timestamp").reset_index(drop=True)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # We take all bin + cat as Category
        return FeatureTypes(
            categorical=[c for c in df.columns if c.startswith(("cat", "bin"))],
            datetime=["timestamp"],
        )
