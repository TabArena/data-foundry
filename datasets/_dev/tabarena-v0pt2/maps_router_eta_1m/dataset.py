"""Curated dataset definition for `maps_router_eta_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Metric,
    Source,
    TaskSummary,
    Temporal,
    TemporalSplits,
)


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
            "Each test window is one of the three newest weeks (20 November to 10 December 2023), up to 500,000 "
            "routes each; a week is TabReD's own validation and test length. Training is every route requested at "
            "least a day before the window, of which a benchmark fits on a random million; the oldest window trains "
            "on 45% of the routes."
        ),
        fit="direct",
        fit_reason=(
            "The features describe the route and the road conditions at the request, and later weeks are tested. They"
            " are anonymous, so their timing cannot be checked one by one."
        ),
    )

    # Dataset
    unique_name = "maps_router_eta_1m"
    domain = "industry & manufacturing"
    sources = (
        Source(
            role="publication",
            platform="Kaggle",
            url="https://www.kaggle.com/datasets/pcovkrd84mejm/maps-routing",
            license="CC-BY-NC-SA-4.0",
            year="2024",
            bibtex="""
                @inproceedings{rubachev2025tabred,
                  title={TabReD: Analyzing Pitfalls and Filling the Gaps in Tabular Deep Learning Benchmarks},
                  author={Rubachev, Ivan and Kartashev, Nikolay and Gorishniy, Yury and Babenko, Artem},
                  booktitle={The Thirteenth International Conference on Learning Representations},
                  year={2025},
                }
            """,
        ),
    )
    data_tags = ("Anonymized",)
    download_description = """
        We get the TabRed data from Kaggle.

        kaggle datasets download -d pcovkrd84mejm/maps-routing -f maps_routing.parquet && unzip maps_routing.parquet.zip && rm maps_routing.parquet.zip && mkdir -p local-data-warehouse/maps_router_eta && mv maps_routing.parquet local-data-warehouse/maps_router_eta/
    """
    curation_comments = """
        We start with data from TabRed, which already comes preprocessed.
        We perform no additional preprocessing steps.

        - Potential leak, kept on purpose: TabReD releases the 984 numeric features only after a quantile transform to a normal distribution (all within ±5.1993, the clip of scikit-learn's QuantileTransformer; 624 reach it); which rows it was fit on is not documented, and the raw features are not published. Kept (Lennart, 2026-10-19): a scaling over all rows is no strong leak, and data often come this way; revisit if the TabReD authors say the fit used all rows.
        - The row budget: each test window keeps at most 500k of its rows, drawn at random within the window, and each train side holds every earlier row (minus the one-day gap); the frame keeps every row a split uses. The 1M train budget is recorded, not applied: a benchmark sub-samples each train side to 1M rows before a fit with `subsample_train`, by default a random 1M of the newest year before the window. The data span 1 November to 10 December 2023, so that is a random 1M of all earlier routes, as in TabReD: random sub-sampling instead of a time-based one keeps data from the whole period and the distribution shift across it.
    """

    # Task
    target = "target_log_spkm"
    problem_type = "regression"
    metric = Metric.source(
        "rmse",
        original="RMSE (TabReD's regression metric)",
        reference="Rubachev et al., TabReD, ICLR 2025 (https://arxiv.org/abs/2406.19380)",
        definition="Root mean squared error of the log seconds-per-km target, as TabReD scores its regression tasks",
    )

    # Splits
    splits_comment = """
        Each test window is one week, TabReD's own validation and test length: TabReD trains on 1-20 November 2023, validates on 20-27 November and tests on 27 November to 4 December (https://arxiv.org/abs/2406.19380). TabReD states no refit cadence, so the length says how long one fitted model serves. A week holds every weekday once, and travel times are lower on weekends. The routes run over 40 days, 1 November to 10 December 2023, so every possible window is a late-autumn week: none can test another year, another season or the year-end holidays. The test windows are the three newest weeks (CC 2026-11-11), newest first: 4-10 December, 27 November to 3 December and 20-26 November, the last two TabReD's own test and validation weeks. They hold 2,444,459, 2,385,262 and 2,401,353 routes before sampling. Train is the routes requested at least one day before each window: 10,902,438, 8,496,883 and 6,108,934 routes (79.9%, 62.3% and 44.8% of all 13,639,272 routes). The oldest window, 20-26 November, trains on less than half the routes (44.8%); the two newest train on more. The windows walk back from the newest because the 40 days leave no other choice: a fourth whole week, 13-19 November, would train on about a quarter (27.2%). The gap of one day is part of the task: a travel time is known only when the drive ends (up to 16.6 hours after the request, from the target and track_length in metres), so at a window's start the last routes before it have no label yet; without the gap 656, 654 and 578 train routes per window (request time + seconds per km x km) would end after the window start, with it none. The gap removes 292k, 313k and 299k of the 11.2M, 8.8M and 6.4M earlier routes (2.6 to 4.7%). Each window keeps at most 500k of its rows (2.4M before sampling); each train side holds every eligible earlier row, and a benchmark sub-samples it to a random 1M before a fit (`subsample_train`; the newest year before a window is all of the data before it). TabReD documents only the target (log seconds per km), not the unit of track_length; we read it as metres because no value is below 1,000.0 (TabReD's 1 km floor, we assume) and the implied drive is then 0.03 to 16.6 hours (median 12 minutes), against a median of 194 hours if read as km. The data have few implausible rows: 31 of 13.6M (12 above 150 km/h, 5 below 2 km/h, 14 longer than 12 hours), none among the late routes, so the gap is set by ordinary short drives requested in the last hours before a window start.
    """
    temporal = Temporal(
        on="timestamp",
        splits=TemporalSplits(window=7, unit="days", n_windows=3, gap=1),
    )
    accepted_check_warnings = {
        "splits_train_under_half": (
            "Signed off (Lennart, 2026-11-11, review issue 1, A): the oldest week trains on 44.8% of all routes, "
            "beside 79.9% and 62.3%; SPLIT-14's two tiers admit it."
        ),
    }

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
