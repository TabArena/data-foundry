"""Curated dataset definition for `cooking_time_1m` (data-foundry v2). Evidence: README.md."""

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


class CookingTime1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How long will a restaurant take to cook an order placed through a food delivery app?",
        use_case=(
            "When an order is placed, the delivery service estimates the restaurant's cooking time, for example to "
            "time the courier and the delivery estimate shown to the customer."
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
            "Each test window is a week, TabReD's own validation and test length: the newest (28 December 2023 to 3 "
            "January 2024) and every other week before it (14-20 December and 4-10 December), up to 500,000 orders "
            "each. Training is every order placed at least a day before the window, of which a benchmark fits on a "
            "random million."
        ),
        fit="direct",
        fit_reason=(
            "Order contents and past cooking times are known when an order is placed. The features are anonymised, so"
            " their timing cannot be checked."
        ),
    )

    # Dataset
    unique_name = "cooking_time_1m"
    domain = "industry & manufacturing"
    sources = (
        Source(
            role="publication",
            platform="Kaggle",
            url="https://www.kaggle.com/datasets/pcovkrd84mejm/cooking-time",
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

        kaggle datasets download -d pcovkrd84mejm/cooking-time -f cooking_time.parquet && unzip cooking_time.parquet.zip && rm cooking_time.parquet.zip
        mkdir -p local-data-warehouse/cooking_time && mv cooking_time.parquet local-data-warehouse/cooking_time/
    """
    curation_comments = """
        We start with data from TabRed, which already comes preprocessed.

        - Potential leak, kept on purpose: TabReD releases the 186 numeric features only after a quantile transform to a normal distribution (all within ±5.1993, the clip of scikit-learn's QuantileTransformer; 155 reach it); which rows it was fit on is not documented, and the raw features are not published. Kept (Lennart, 2026-10-19): a scaling over all rows is no strong leak, and data often come this way; revisit if the TabReD authors say the fit used all rows.
        - We drop orders with a cooking time under one minute (168 of 12.8M, 26 of them zero or negative), as TabReD's preprocessing does.
        - The target is the natural log of the minutes, as in TabReD (the column keeps its name). TabReD's reason: the times are right-skewed, and squared error on the log is close to absolute error on the minutes, the error that matters for the task.
        - The row budget: Each test window keeps at most 500k of its rows, drawn at random within the window (v2 split protocol), and each train side holds every earlier order outside the one-day gap; the container keeps every row a split uses. The container records the 1M train budget, and a benchmark sub-samples each train side to 1M rows before a fit (`subsample_train`; by default a random 1M of the newest year before the window). The orders start on 15 November 2023, so the newest year is all of the history and the default is a random 1M of all earlier orders, as in TabReD: a random sample keeps data from all periods of the history.
    """

    # Task
    target = "cooking_time_minutes"
    problem_type = "regression"
    metric = Metric.source(
        "rmse",
        original="RMSE (TabReD regression tasks)",
        reference=(
            "Rubachev et al., TabReD, ICLR 2025 (https://arxiv.org/abs/2406.19380), Sec. 4 / App.: RMSE "
            "for regression, ROC AUC for classification"
        ),
        definition="sqrt(mean((y - yhat)^2)) on the natural-log minutes target",
    )

    # Splits
    splits_comment = """
        Each test window is one week, TabReD's own validation and test length: TabReD trains on 15 November to 20 December 2023, validates on 21-27 December and tests on 28 December to 3 January. TabReD states no refit cadence. A week holds every weekday once, and cooking times follow a weekly cycle: Friday and Saturday orders cook about 12% longer than Monday to Thursday orders (mean log minutes 2.57 to 2.64 against 2.46 to 2.51), more than the shift between the weekly windows. The test windows are the newest week and every other week before it (CC 2026-11-11, as for delivery_eta_1m; it supersedes the three newest weeks of 2026-11-10), newest first: 28 December to 3 January, TabReD's test week, over New Year; 14-20 December, in the run-up to the holidays; and 4-10 December, a week before the run-up. 21-27 December, TabReD's validation week, is not tested. Train is the orders placed at least one day before each window: 10,856,304, 6,935,762 and 4,797,156 orders (84.8%, 54.2% and 37.5% of the 12,799,474). 4-10 December trains on less than half the orders (37.5%), beside 84.8% and 54.2%. The orders run from 15 November 2023 to 3 January 2024, so only the weeks from 11 December keep half the orders for training (51.9% for a start on 11 December). 4-10 December is the last full week before 11-12 December, which hold no orders, and every day of it holds 208,774 to 326,051 orders; two weeks before 14 December, 30 November to 6 December, would train on 28.9%, under 30%. Cooking times rise toward New Year (mean log minutes 2.533, 2.548 and 2.599 in the oldest, middle and newest window, against 2.527 to 2.532 in the weeks from 16 November to 6 December), so the score covers a week before the run-up, the run-up and the holiday itself, but not a week after the holidays (the data end on 3 January). The gap of one day is part of the task: a cooking time is known only when the order is cooked (up to 2 hours after it is placed), so at a refit the last orders before it have no label yet; without the gap 172, 108 and 155 train orders per window (start + cooking time) would end after the window start, with it none. The gap removes 280k, 239k and 278k of the 11.1M, 7.2M and 5.1M earlier orders (2.5 to 5.5%). Each window keeps at most 500k of its rows (1,662,794, 1,921,331 and 1,861,029 before sampling); each train side holds every eligible earlier row, and a benchmark sub-samples it to 1M rows, by default a random 1M of the newest year before the window, here all of the history (`subsample_train`).
    """
    temporal = Temporal(
        on="timestamp",
        splits=TemporalSplits(window=7, unit="days", gap=1, cutoffs=("2023-12-28", "2023-12-14", "2023-12-04")),
    )
    accepted_check_warnings = {
        "splits_train_under_half": (
            "Signed off (Lennart, 2026-11-11, review issue 2, B): 4-10 December trains on 37.5% of the orders, beside "
            "28 December-3 January and 14-20 December on 84.8% and 54.2%; SPLIT-14's two tiers admit it."
        ),
    }
    row_budget = RowBudget(train=1_000_000, test=500_000)

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
