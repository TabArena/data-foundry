"""Curated dataset definition for `maps_router_eta_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TemporalSplits


class MapsRouterEta1m(AbstractCuratedDataset):
    # Dataset
    unique_name = "maps_router_eta_1m"
    version_of = "maps_router_eta"
    version_comment = """
        We sample per test window (v2 split protocol): each window keeps at most 500k of its rows, and its train side is a random 1M of all earlier rows, drawn in one random order for all windows; the frame keeps only the rows a split uses. We follow TabReD and use random sub-sampling of the train data. The idea behind this instead of a time-based subsampling is to keep data from various time periods and model the distribution shift across the full time horizon.
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
        df = pd.read_parquet(raw_dir / "maps_routing.parquet")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.sort_values(by="timestamp").reset_index(drop=True)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # We take all bin + cat as Category; `timestamp` is already a datetime in the parquet file
        return FeatureTypes(
            categorical=[c for c in df.columns if c.startswith(("cat", "bin"))],
            datetime=["timestamp"],
        )
