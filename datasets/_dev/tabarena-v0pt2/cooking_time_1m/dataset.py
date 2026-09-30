"""Curated dataset definition for `cooking_time_1m` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, TemporalSplits


class CookingTime1m(AbstractCuratedDataset):
    # Dataset
    unique_name = "cooking_time_1m"
    version_of = "cooking_time"
    version_comment = """
        We randomly sub-sample the train to 1 million and test data 250k rows. We follow TabReD and use random sub-sampling. The idea behind this instead of a time-based subsampling is to keep data from various time periods and model the distribution shift across the full time horizon.
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
    """

    # Task
    target = "cooking_time_minutes"
    problem_type = "regression"
    time_on = "timestamp"

    # Splits
    splits_comment = "We use the last week as test data and all prior data as train data."
    time_horizon = 7
    time_horizon_unit = "days"
    temporal_splits = TemporalSplits(window=7, unit="days", n_windows=1)
    subsample_to_budget = True

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_parquet(raw_dir / "cooking_time.parquet")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        # Following TabRed
        df = df[df["cooking_time_minutes"] >= 1.0]
        # We take all bin + cat as Category
        cat_cols = [c for c in df.columns if c.startswith(("cat", "bin"))]
        df[cat_cols] = df[cat_cols].astype("category")
        df["cooking_time_minutes"] = np.log(df["cooking_time_minutes"])
        df = df.sort_values(by="timestamp").reset_index(drop=True)
        return df
