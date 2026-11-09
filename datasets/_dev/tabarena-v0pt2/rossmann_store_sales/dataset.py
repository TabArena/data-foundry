"""Curated dataset definition for `rossmann_store_sales` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, Source, TaskSummary, Temporal, TemporalSplits


class RossmannStoreSales(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How much will a Rossmann store sell on each day of the next six weeks?",
        use_case=(
            "Rossmann store managers forecast their daily sales up to six weeks ahead, to plan staff schedules (the "
            "competition's description)."
        ),
        row=("One day of one open Rossmann drug store in Germany (1,115 stores, January 2013 to July 2015)."),
        predicted="The store's turnover that day; the currency is not stated.",
        known=(
            "The store, the date and weekday, whether a promotion runs, state and school holidays, the store type and"
            " assortment, the nearest competitor's distance and opening date, and the store's recurring promotion "
            "scheme."
        ),
        split=(
            "Three windows of six weeks, newest first: 20 June to 31 July 2015, the Christmas weeks (22 November 2014 "
            "to 2 January 2015) and late spring 2014 (26 April to 6 June), each trained on all earlier days with a "
            "one-day gap."
        ),
        changes=(
            "We drop closed days, which all have zero sales, and the day's number of customers, known only afterwards."
        ),
        fit="direct",
        fit_reason=(
            "Promotions, holidays and opening days are planned in advance, and six-week windows match the managers' "
            "horizon. Closed days are left out, so the model assumes the store's opening days are known."
        ),
    )

    # Dataset
    unique_name = "rossmann_store_sales"
    domain = "business & marketing"
    sources = (
        Source(
            role="publication",
            platform="Kaggle",
            url="https://www.kaggle.com/competitions/rossmann-store-sales/overview",
            license="Kaggle License",
            year="2015",
            bibtex=r"""
                @misc{kaggle_rossmann_store_sales,
                    title        = {Rossmann Store Sales},
                    author       = {{Kaggle}},
                    howpublished = {\url{https://www.kaggle.com/competitions/rossmann-store-sales/overview}},
                    note         = {Kaggle competition page. Accessed: 2026-03-19},
                    year         = {2015}
                }
            """,
        ),
    )
    download_description = r"""
        kaggle competitions download -c rossmann-store-sales \
        && mkdir -p local-data-warehouse/rossmann_store_sales \
        && mv rossmann-store-sales.zip local-data-warehouse/rossmann_store_sales \
        && unzip local-data-warehouse/rossmann_store_sales/rossmann-store-sales.zip -d local-data-warehouse/rossmann_store_sales \
        && rm local-data-warehouse/rossmann_store_sales/rossmann-store-sales.zip
    """
    curation_comments = """
        - We merge the store data with the train data.
        - The data is from a Kaggle competition with a temporal split, so the test data cannot be used for unsupervised approachs.
        - The winning solution is public: https://storage.googleapis.com/kaggle-forum-message-attachments/102102/3454/Rossmann_nr1_doc.pdf.
        - The competition used 48 days for testing. The description says "Rossmann store managers are tasked with predicting their daily sales for up to six weeks in advance". Therefore, we define the same horizon for defining our test splits and add one day between train/test as a planning gap.
        - We transform the date column to datetime format.
        - We exclude days when the store is closed since they all have zero sales and are trivial to predict. We drop the Open column.
        - We assign categorical data type to the Store column.
        - For the train data, the # of customers per day is given, which is not available at the prediction point for the test data. The 1st-place solution says that one model variation computed recent-history features on the number of customers instead of sales, and also used store-level aggregates such as average sales per customer. However this would mean that we have to define split-specific splits. Since many high performing solutions did not utilize customer information, we drop the column.
        - The StateHoliday column has two encodings for the entry 0, one as number and one as object. We combine them into one category.
        - The Kaggle test file covers 2015-08-01 to 2015-09-17 (48 days) for 856 of the 1,115 stores; the train file covers 2013-01-01 to 2015-07-31 (942 days) for all 1,115 (from the v1 exploration, counted 2026-10-22).
        - Partial order, left unordered (2026-11-01, CLEAN-14): `Assortment`: a (basic) is the lowest, but whether b
          (extra) is below or above c (extended) is not stated.
        - Cycle (2026-11-01, CLEAN-14, Lennart's rule): `DayOfWeek` (1-7, an unordered category before) and
          `CompetitionOpenSinceMonth` (1-12) are numbers. A weekday or a month is a position in a continuous cycle
          (weekday 1.5 is Monday noon), and the source ships it as a number; named weekdays and months are ordered
          categories instead.
    """

    # Task
    target = "Sales"
    problem_type = "regression"
    metric = Metric.source(
        "rmspe",
        original="Root Mean Square Percentage Error (RMSPE)",
        reference=(
            "https://www.kaggle.com/competitions/rossmann-store-sales/overview/evaluation (Kaggle API "
            "evaluationMetric: 'Root Mean Square Percentage Error')"
        ),
        definition="sqrt(mean(((y - p) / y)^2)) over the store-days with Sales != 0, on the raw sales",
    )

    # Splits
    splits_comment = """
        The description says 'Rossmann store managers are tasked with predicting their daily sales for up to six weeks in advance', to plan staff schedules, and the competition's own test period (1 August to 17 September 2015, 48 days) is about as long, so each test window is six weeks (42 days; the horizon checked, CC 2026-11-11). We add one day between train and test as a planning gap: a day's turnover is known when the store closes, so no label arrives late, and the gap only drops the last day before each window from training. The three windows, newest first (CC 2026-11-11), evenly spaced over the 11 windows that keep half the store-days for training (the 1st, 6th and 11th): 2015-06-20 to 07-31, the newest; 2014-11-22 to 2015-01-02, the Christmas weeks, when sales are highest (8,478 per open store-day against 6,837 on the train side, 24% more) and staffing matters most; and 2014-04-26 to 06-06, late spring of the other year. So the test spans two years and three seasons. Test 40,282, 31,203 and 38,107 store-days; train 802,996, 617,355 and 443,771 (95.1%, 73.1% and 52.6% of the 844,392 open store-days); the 1,114 store-days of 19 June 2015, the newest window's gap day, lie in no split. 180 stores have no rows from 1 July to 31 December 2014, so the Christmas window tests 935 stores until 31 December and all 1,115 only on 2 January 2015; the other two windows test every store.
    """
    accepted_check_warnings = {
        "splits_rows_unused": (
            "By design: the 1,114 store-days of 19 June 2015, the one-day gap before the newest window, are in no "
            "split (Lennart, 2026-11-11, review issue 1)."
        ),
    }
    temporal = Temporal(
        on="Date",
        splits=TemporalSplits(window=42, unit="days", gap=1, cutoffs=("2015-06-20", "2014-11-22", "2014-04-26")),
    )

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        """NOTES:
        - We need to do some FE to make the "Customers" column useful. Test how much the full aggregated set differs from the splits.
        """
        train = pd.read_csv(raw_dir / "train.csv")
        store = pd.read_csv(raw_dir / "store.csv")
        return {"train": train, "store": store}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        train, store = raw["train"], raw["store"]
        df = pd.merge(train, store, on="Store", how="left")
        df["Date"] = pd.to_datetime(df["Date"])  # parsed here: the sort below runs on the dates
        df = df[df["Open"] == 1].copy()
        df = df.drop(columns=["Open"])
        # Drop customer information. TODO: Enable split-specific data storage and feature engineering to utilize this information.
        df = df.drop(columns=["Customers"])
        df["StateHoliday"] = df["StateHoliday"].astype(str)
        df = df.sort_values("Date", kind="stable").reset_index(drop=True)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "Store",
                "StateHoliday",
                "StoreType",
                "Assortment",
                "PromoInterval",
                # 0/1 flags (CLEAN-14)
                "Promo",
                "SchoolHoliday",
                "Promo2",
            ],
            datetime=["Date"],
        )
