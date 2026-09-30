"""Curated dataset definition for `maps_router_eta_1m` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, TemporalSplits


class MapsRouterEta1m(AbstractCuratedDataset):
    # Dataset
    unique_name = "maps_router_eta_1m"
    version_of = "maps_router_eta"
    version_comment = """
        We randomly sub-sample the train to 1 million and test data 250k rows. We follow TabReD and use random sub-sampling. The idea behind this instead of a time-based subsampling is to keep data from various time periods and model the distribution shift across the full time horizon.
    """
    year = "2024"
    domain = "industry & manufacturing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/pcovkrd84mejm/maps-routing"
    license = "CC-BY-NC-SA-4.0"
    data_tags = ("Anonymized",)
    download_description = """
        We get the TabRed data from Kaggle.

        kaggle datasets download -d pcovkrd84mejm/maps-routing -f maps_routing.parquet && unzip maps_routing.parquet.zip && rm maps_routing.parquet.zip && mkdir -p local-data-warehouse/maps_router_eta && mv maps_routing.parquet local-data-warehouse/maps_router_eta/
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
        We perform no additional preprocessing steps.
    """

    # Task
    target = "target_log_spkm"
    problem_type = "regression"
    time_on = "timestamp"

    # Splits
    splits_comment = "We use the last week as test data and all prior data as train data."
    time_horizon = 7
    time_horizon_unit = "days"
    temporal_splits = TemporalSplits(window=7, unit="days", n_windows=1)
    subsample_to_budget = True

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_parquet(raw_dir / "maps_routing.parquet")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        # We take all bin + cat as Category
        cat_cols = [c for c in df.columns if c.startswith(("cat", "bin"))]
        df[cat_cols] = df[cat_cols].astype("category")
        df = df.sort_values(by="timestamp").reset_index(drop=True)
        return df
