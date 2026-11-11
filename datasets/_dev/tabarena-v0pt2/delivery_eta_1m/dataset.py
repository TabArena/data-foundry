"""Curated dataset definition for `delivery_eta_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Metric,
    RowBudget,
    Source,
    TaskSummary,
    Temporal,
    TemporalSplits,
)


class DeliveryEta1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How long will it take to deliver an order from an online grocery store?",
        use_case=(
            "When an order is placed, the grocery service estimates its delivery time, for example to show the "
            "customer an arrival time and to plan couriers."
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
            "Each test window is a week, the length of TabReD's own validation and test periods: the newest (1-7 "
            "January 2024) and every other week before it (18-24 and 4-10 December 2023), up to 500,000 orders each; "
            "training is every earlier order, of which a benchmark fits on a random million."
        ),
        fit="direct",
        fit_reason=(
            "Courier availability and route data are known when an order is placed. The features are anonymised, so "
            "their timing cannot be checked."
        ),
    )

    # Dataset
    unique_name = "delivery_eta_1m"
    domain = "industry & manufacturing"
    sources = (
        Source(
            role="publication",
            platform="Kaggle",
            url="https://www.kaggle.com/datasets/pcovkrd84mejm/delivery-eta",
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
        We download the data from Kaggle.

        kaggle datasets download -d pcovkrd84mejm/delivery-eta -f delivery_eta.parquet && unzip delivery_eta.parquet.zip && rm delivery_eta.parquet.zip && mkdir -p local-data-warehouse/delivery_eta && mv delivery_eta.parquet local-data-warehouse/delivery_eta/
    """
    curation_comments = """
        We start with data from TabRed, which already comes preprocessed.

        - Potential leak, kept on purpose: TabReD releases the 217 numeric features only after a quantile transform to a normal distribution (all within ±5.1993, the clip of scikit-learn's QuantileTransformer; 152 reach it); which rows it was fit on is not documented, and the raw features are not published. Kept (Lennart, 2026-10-19): a scaling over all rows is no strong leak, and data often come this way; revisit if the TabReD authors say the fit used all rows.
        - We drop orders with a delivery time under one minute (386k of 17.0M, 2.3%), as TabReD's preprocessing does.
        - The target is the natural log of the minutes, as in TabReD (the column keeps its name). TabReD's reason, stated for its cooking-time data and applied here too: the times are right-skewed, and squared error on the log is close to absolute error on the minutes, the error that matters for the task.
        - We drop a duplicated column `cat_2` in the preprocessing.
        - We drop `num_29`, `num_36` and `num_71`, which are constant except in the same 2 of 16.7M rows (both hold 5.199 in all three columns), and `num_101`, which has a single value and is missing in exactly the rows where 19 other columns are missing, so it carries no information of its own.
        - Kept on purpose: on 23 November 2023 at 11:00 the 45 features `num_76` to `num_121` stop being recorded (99.6% to 100% missing from noon to the end; 1% to 13% before, 49% for `num_117` to `num_120`), and the deliveries get longer in the same hour (mean log minutes 1.67 before, 1.85 after); every test window lies after the cut. The cause is not published. Kept (Lennart, CC 2026-11-10): at each test window's prediction point a model gets what the service's own model got, the block missing for nearly every order, and the block is still recorded for some orders of every test window (orders carrying `num_96`: 4,508 of 4-10 December, 0.31%; 5,126 of 18-24 December, 0.35%; 7,823 of 1-7 January, 0.66%), so it is no column without values at test.
        - The row budget: Each test window keeps at most 500k of its rows, drawn at random within the window (v2 split protocol), and each train side holds every earlier order; the container keeps every row a split uses. The container records the 1M train budget, and a benchmark sub-samples each train side to 1M rows before a fit (`subsample_train`; by default a random 1M of the newest year before the window). The orders start on 20 October 2023, so the newest year is all of the history and the default is a random 1M of all earlier orders, as in TabReD: a random sample keeps data from all periods of the history.
    """

    # Task
    target = "delivery_eta_minutes"
    problem_type = "regression"
    metric = Metric.source(
        "rmse",
        original="RMSE (TabReD regression tasks)",
        reference=(
            "Rubachev et al., TabReD, ICLR 2025 (https://arxiv.org/abs/2406.19380), Sec. 4 / App.: RMSE for "
            "regression, ROC AUC for classification"
        ),
        definition="sqrt(mean((y - yhat)^2)) on the natural-log minutes target",
    )

    # Splits
    splits_comment = """
        Each test window is one week, the length of TabReD's own validation and test periods (TabReD trains on 20 October to 11 December 2023, validates on 11-18 December and tests on 18-25 December). TabReD states no refit cadence, and a delivery estimate looks only minutes ahead, so the length says how long one fitted model serves. The orders run from 20 October 2023 to 7 January 2024, so only the five weeks from 4 December on keep half the orders for training. Every other one of them is a test window (CC 2026-11-10), newest first: 1-7 January 2024, the newest, the New Year week; 18-24 December, TabReD's test week, before Christmas; and 4-10 December, outside the holidays, an early-December week of long deliveries (mean log minutes 1.910 against 1.778 in the newest week) with a train side that holds only 10 days after the change of 23 November (curation_comments). 25-31 December and 11-17 December lie between them and are not tested. Train is all prior data: 15,469,869, 12,517,876 and 9,706,793 orders (92.9%, 75.1% and 58.3%). No gap is needed: the orders pause overnight, and the last train order before each window is delivered 55 minutes to 2 hours 5 minutes before the window start (order time + delivery time; before 4 December at 22:58 on 3 December), so no train label is unknown at a refit (0 late orders in each of the 3 windows). The windows hold 1,188,182, 1,485,323 and 1,444,992 orders, of which each keeps at most 500k, drawn at random; each train side holds every earlier row, and a benchmark sub-samples it to 1M rows, by default a random 1M of the newest year before the window, here all of the history (`subsample_train`).
    """
    temporal = Temporal(
        on="timestamp",
        splits=TemporalSplits(window=7, unit="days", cutoffs=("2024-01-01", "2023-12-18", "2023-12-04")),
    )
    row_budget = RowBudget(train=1_000_000, test=500_000)

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
