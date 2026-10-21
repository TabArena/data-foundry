"""Curated dataset definition for `maps_router_eta_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TaskSummary, Temporal, TemporalSplits


class MapsRouterEta1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=("How long will a car take per kilometre on a requested route, given the current road conditions?"),
        use_case=(
            "A car navigation service, when a driver requests a route, predicts the travel time from the current road"
            " conditions (TabReD's description)."
        ),
        row=(
            "One car route of a navigation service from 1 November to 10 December 2023, from TabReD's 2.5% random "
            "sample of the log; service and region not stated."
        ),
        predicted="The travel time per kilometre, as the log of seconds per kilometre.",
        known=(
            "Anonymous numeric, categorical and yes/no features that summarise the route's road graph, its current "
            "traffic and road details such as speed limits, plus the time of the request."
        ),
        split=(
            "Each test window is one week (20 November to 10 December 2023); training is a random million earlier "
            "routes from 1 November, as for a model refit every week."
        ),
        fit="direct",
        fit_reason=(
            "The features describe the route and the road conditions at the request, and later weeks are tested. They"
            " are anonymous, so their timing cannot be checked one by one."
        ),
    )

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

        - Potential leak, kept on purpose: TabReD releases the 984 numeric features only after a quantile transform to a normal distribution (all within ±5.1993, the clip of scikit-learn's QuantileTransformer; 624 reach it); which rows it was fit on is not documented, and the raw features are not published. Kept (Lennart, 2026-10-19): a scaling over all rows is no strong leak, and data often come this way; revisit if the TabReD authors say the fit used all rows.
    """

    # Task
    target = "target_log_spkm"
    problem_type = "regression"

    # Splits
    splits_comment = """
        We use each of the last 3 weeks as a test window (newest first) and the routes requested at least one day before it as train data. The gap of one day is part of the task: a travel time is known only when the drive ends (up to 16.6 hours after the request, from the target and track_length in metres), so at a weekly refit the last routes before it have no label yet; without the gap 656, 654 and 578 train routes per window (request time + seconds per km x km) would end after the window start, with it none. The gap removes 292k, 313k and 299k of the 11.2M, 8.8M and 6.4M earlier routes (2.6 to 4.7%). Each window keeps at most 500k of its rows (2.4M before sampling); each train side is a random 1M of the eligible earlier rows (one random order for all windows).
    """
    temporal = Temporal(
        on="timestamp",
        splits=TemporalSplits(window=7, unit="days", n_windows=3, gap=1),
    )
    subsample_to_budget = True

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_parquet(raw_dir / "maps_routing.parquet")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.sort_values(by="timestamp", kind="stable").reset_index(drop=True)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # We take all bin + cat as Category; `timestamp` is already a datetime in the parquet file
        return FeatureTypes(
            categorical=[c for c in df.columns if c.startswith(("cat", "bin"))],
            datetime=["timestamp"],
        )
