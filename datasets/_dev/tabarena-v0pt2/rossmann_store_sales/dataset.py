"""Curated dataset definition for `rossmann_store_sales` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, Source, TaskSummary, Temporal, TemporalSplits

# The calendar the day counters read: every store-day of train.csv (2013-01-01 to 2015-07-31) and test.csv (to
# 2015-09-17), closed days included. A store-day without a row is unknown and counts as no event.
_CAL_START = pd.Timestamp("2013-01-01")
_CAL_END = pd.Timestamp("2015-09-17")
_MONTHS = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sept": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}
# 0/1 day counters (categorical, CLEAN-14); the other counters are numbers.
_FLAG_COUNTERS = ["closed_yesterday", "promo_yesterday", "promo_tomorrow", "p2_active_month"]


def _last_index(flag: np.ndarray, *, forward: bool = True) -> np.ndarray:
    """Per day and store, the index of the last day at or before (forward) or the first at or after a True day."""
    idx = pd.DataFrame(np.where(flag, np.arange(flag.shape[0])[:, None], np.nan))
    return (idx.ffill() if forward else idx.bfill()).to_numpy()


def _in_long_runs(flag: np.ndarray, min_len: int) -> np.ndarray:
    """Mark the days inside runs of at least ``min_len`` consecutive True days of each store (column)."""
    prev = np.vstack([np.zeros((1, flag.shape[1]), bool), flag[:-1]])
    start = (flag & ~prev).ravel(order="F")
    run_id = np.cumsum(start)
    flat = flag.ravel(order="F")
    lengths = np.bincount(run_id[flat], minlength=run_id.max() + 1)
    return (flat & (lengths[run_id] >= min_len)).reshape(flag.shape, order="F")


def _day_counters(calendar: pd.DataFrame, rows: pd.DataFrame, store: pd.DataFrame) -> pd.DataFrame:
    """The 32 calendar day counters for ``rows`` (Store, Date), from the stores' daily calendar; no sales are read.

    Events: promotion days, state holidays, school holidays, summer holidays (school-holiday runs of at least 28
    days), closures and the Promo2 cycle (1st place, Rossmann_nr1_doc.pdf, "Temporal information": "day counters to
    express how each record relates to certain events or cycles").
    """
    dates = pd.date_range(_CAL_START, _CAL_END, freq="D")
    n_days, n_stores = len(dates), int(store["Store"].max())
    ci = (calendar["Date"] - _CAL_START).dt.days.to_numpy()
    cs = calendar["Store"].to_numpy() - 1

    def panel(values: np.ndarray) -> np.ndarray:
        out = np.full((n_days, n_stores), np.nan)
        out[ci, cs] = values
        return out

    is_open = panel(calendar["Open"].to_numpy(float))
    promo = panel(calendar["Promo"].to_numpy(float))
    school = panel(calendar["SchoolHoliday"].to_numpy(float))
    state = panel((calendar["StateHoliday"].astype(str) != "0").to_numpy(float))
    known = ~np.isnan(is_open)
    closed = np.where(known, (is_open == 0).astype(float), np.nan)

    rt = (rows["Date"] - _CAL_START).dt.days.to_numpy()
    rs = rows["Store"].to_numpy() - 1
    tt = np.arange(n_days)[:, None]
    feat: dict[str, np.ndarray] = {}

    def event_counters(flag: np.ndarray, name: str, cap: int) -> None:
        prev = np.vstack([np.zeros((1, n_stores), bool), flag[:-1]])
        start = flag & ~prev
        feat[f"{name}_since"] = np.minimum(tt - _last_index(flag), cap)[rt, rs]
        feat[f"{name}_until"] = np.minimum(_last_index(flag, forward=False) - tt, cap)[rt, rs]
        feat[f"{name}_since_start"] = np.minimum(tt - _last_index(start), cap)[rt, rs]
        feat[f"{name}_until_start"] = np.minimum(_last_index(start, forward=False) - tt, cap)[rt, rs]

    school_on = np.nan_to_num(school) > 0.5
    event_counters(np.nan_to_num(promo) > 0.5, "promo", 30)
    event_counters(np.nan_to_num(state) > 0.5, "stateh", 60)
    event_counters(school_on, "schoolh", 60)
    event_counters(_in_long_runs(school_on, 28), "summer", 120)

    closed_on = np.nan_to_num(closed) > 0.5
    long_closed = _in_long_runs(closed_on, 4)
    prev_long = np.vstack([np.zeros((1, n_stores), bool), long_closed[:-1]])
    reopen = ~long_closed & prev_long & (np.nan_to_num(is_open) == 1)
    weekday = np.repeat(dates.dayofweek.to_numpy()[:, None], n_stores, axis=1)  # 0 = Monday
    feat["closed_yesterday"] = np.vstack([np.full((1, n_stores), np.nan), closed[:-1]])[rt, rs]
    feat["closed_nonsun_since"] = np.minimum(tt - _last_index(closed_on & (weekday != 6)), 60)[rt, rs]
    feat["refurb_since_reopen"] = np.minimum(tt - _last_index(reopen), 365)[rt, rs]
    feat["promo_yesterday"] = np.vstack([np.full((1, n_stores), np.nan), promo[:-1]])[rt, rs]
    feat["promo_tomorrow"] = np.vstack([promo[1:], np.full((1, n_stores), np.nan)])[rt, rs]

    # holidays in the row's ISO week (Monday to Sunday), the week before and the week after; missing unless all
    # seven days of that week are known
    week = (np.arange(n_days) + _CAL_START.dayofweek) // 7
    row_week = week[rt]
    for name, values in (("schoolh", school), ("stateh", state)):
        sums = pd.DataFrame(np.nan_to_num(values)).groupby(week).sum()
        counts = pd.DataFrame(~np.isnan(values)).groupby(week).sum()
        by_week = sums.where(counts == 7).to_numpy()
        for label, offset in (("thisweek", 0), ("lastweek", -1), ("nextweek", 1)):
            w = row_week + offset
            valid = (w >= 0) & (w < by_week.shape[0])
            out = np.full(len(rows), np.nan)
            out[valid] = by_week[w[valid], rs[valid]]
            feat[f"{name}_{label}"] = out

    # Promo2: started on the Monday of Promo2SinceWeek of Promo2SinceYear, renewed in the months of PromoInterval
    st = store.set_index("Store")
    has_p2 = st["Promo2"] == 1
    p2_start = pd.Series(pd.NaT, index=st.index, dtype="datetime64[ns]")
    p2_start[has_p2] = [
        pd.Timestamp.fromisocalendar(int(y), int(w), 1)
        for y, w in zip(st.loc[has_p2, "Promo2SinceYear"], st.loc[has_p2, "Promo2SinceWeek"])
    ]
    interval = st["PromoInterval"].fillna("").map(lambda v: [_MONTHS[m] for m in v.split(",") if m])
    d = rows["Date"].reset_index(drop=True)
    starts = rows["Store"].map(p2_start).reset_index(drop=True)
    months = rows["Store"].map(interval).reset_index(drop=True)
    started = (d >= starts).to_numpy()
    month = d.dt.month.to_numpy()
    in_month = np.array([m in lst for m, lst in zip(month, months)])
    since_cycle = np.full(len(rows), np.nan)
    for i, (m, lst, day) in enumerate(zip(month, months, d)):
        if started[i] and lst:
            earlier = [x for x in lst if x <= m]
            first = pd.Timestamp(day.year, max(earlier), 1) if earlier else pd.Timestamp(day.year - 1, max(lst), 1)
            since_cycle[i] = (day - first).days
    feat["p2_active_month"] = (started & in_month).astype(float)
    feat["p2_days_since_cycle"] = since_cycle
    feat["p2_weeks_since_start"] = ((d - starts).dt.days / 7).to_numpy()
    feat["comp_months_open"] = (
        (d.dt.year.to_numpy() - rows["CompetitionOpenSinceYear"].to_numpy()) * 12
        + month
        - rows["CompetitionOpenSinceMonth"].to_numpy()
    )
    feat["days_to_month_end"] = (d.dt.days_in_month - d.dt.day).to_numpy().astype(float)
    return pd.DataFrame(feat, index=rows.index)


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
            " assortment, the nearest competitor's distance and opening date once it has opened, the store's "
            "recurring promotion scheme, and day counters to the nearest holidays, closures and promotions."
        ),
        split=(
            "Three windows of six weeks, newest first: 20 June to 31 July 2015, the Christmas weeks (22 November 2014 "
            "to 2 January 2015) and late spring 2014 (26 April to 6 June), each trained on all earlier days with a "
            "one-day gap."
        ),
        changes=(
            "We add 32 day counters from the stores' calendar of holidays, closures and promotions (no sales), then "
            "drop closed days, which all have zero sales, and the day's number of customers, known only afterwards. "
            "A competitor is shown only from its opening month."
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
        - Day counters (2026-11-10, Andrej; review issue 1, B): 32 columns that place each day in the store's calendar,
          the winner's "temporal information" (Rossmann_nr1_doc.pdf: "day counters to express how each record relates
          to certain events or cycles"). They are computed in `_clean` from each store's daily `Open`, `Promo`,
          `StateHoliday` and `SchoolHoliday` of train.csv and test.csv (the calendar of August and September 2015, no
          sales), before the closed days are dropped: days since and until a promotion day, a state holiday, a school
          holiday and the summer holidays (school-holiday runs of at least 28 days), and since and until the first day
          of each (caps 30, 60, 60 and 120 days; missing when no such day exists on that side); `closed_yesterday`,
          days since the last closure on a day other than Sunday (cap 60), days since the reopening after a closure of
          at least four days (`refurb_since_reopen`, cap 365); `promo_yesterday`, `promo_tomorrow`; school and state
          holiday days in the row's ISO week, the week before and the week after (missing unless all seven days are
          known); Promo2 running this month, days into its current cycle and weeks since it began; months since the
          competitor opened; days to the month's end. A store-day without a row (180 stores in July to December 2014,
          259 stores after 2015-07-31) counts as no event. The counters assume, as the definition does, that
          promotions, holidays and opening days are planned. Three look-ahead closure counters (closed tomorrow, days
          to the next closure, days to a refurbishment) are left out: they add nothing and would rest on planned
          refurbishments. No counter reads sales or customers.
        - Forecasting test (2026-11-05, re-run 2026-11-10; TP-10): LightGBM on the 47 features beats the best of 26
          forecasts from each store's own sales, picked on each window, in all three windows (RMSPE oldest to newest:
          model 0.097 / 0.104 / 0.112, mean of three configurations, against 0.145 / 0.131 / 0.130); on the 15
          features of before, it tied the store's own forecast in the newest window. Re-run on this definition, with
          the competitor blanked (one configuration, 3,000 trees): 0.098 / 0.110 / 0.114, the same as before the
          blanking (0.099 / 0.109 / 0.114), 4 to 20 standard errors ahead (200 draws of the stores).
        - Competitor as of each day (2026-11-10, Andrej; review issue 3, B): the store table is one read of 2015
          merged onto every day, so `CompetitionDistance`, `CompetitionOpenSinceMonth` and
          `CompetitionOpenSinceYear` are missing on the store-days before the competitor's opening month (70,108
          open store-days, 8.3%; 191 stores). A store's log sales fall 0.044 in the 8 weeks after an opening against
          +0.010 at random dates, so a model could otherwise place a later opening's drop in a test window. The 354
          stores without an opening date keep the distance as read. Promo2 stays as read: the scheme is the company's
          own plan, known ahead.
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
        The description says 'Rossmann store managers are tasked with predicting their daily sales for up to six weeks in advance', to plan staff schedules, and the competition's own test period (1 August to 17 September 2015, 48 days) is about as long, so each test window is six weeks (42 days; the horizon checked, CC 2026-11-11). We add one day between train and test as a planning gap: a day's turnover is known when the store closes, so no label arrives late, and the gap only drops the last day before each window from training. The three windows, newest first (CC 2026-11-11), evenly spaced over the 11 windows that keep half the store-days for training (the 1st, 6th and 11th): 2015-06-20 to 07-31, the newest; 2014-11-22 to 2015-01-02, the Christmas weeks, when sales are highest (8,478 per open store-day against 6,837 on the train side, 24% more) and staffing matters most; and 2014-04-26 to 06-06, late spring of the other year. So the test spans two years and three seasons. Test 40,282, 31,203 and 38,107 store-days; train 802,996, 617,355 and 443,771 (95.1%, 73.1% and 52.6% of the 844,392 open store-days); the 1,114 store-days of 19 June 2015, the newest window's gap day, lie in no split. 180 stores have no rows from 1 July to 31 December 2014, so the Christmas window tests 935 stores until 31 December and all 1,115 only on 2 January 2015; the other two windows test every store. The store table (store.csv) is one read of 2015, merged onto every day: a competitor is shown only from its opening month (see the curation notes).
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
        train = pd.read_csv(raw_dir / "train.csv", dtype={"StateHoliday": str})
        store = pd.read_csv(raw_dir / "store.csv")
        # test.csv only for its calendar of August and September 2015 (opening days, promotions, holidays), so the
        # day counters near 31 July know the coming days; it has no sales
        test = pd.read_csv(raw_dir / "test.csv", dtype={"StateHoliday": str})
        return {"train": train, "store": store, "test": test}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        train, store, test = raw["train"], raw["store"], raw["test"]
        df = pd.merge(train, store, on="Store", how="left")
        df["Date"] = pd.to_datetime(df["Date"])  # parsed here: the sort below runs on the dates
        # The store table is one read of 2015: a competitor is shown only from its opening month (issue 3, B).
        has_open = df["CompetitionOpenSinceYear"].notna() & df["CompetitionOpenSinceMonth"].notna()
        comp_open = pd.to_datetime(
            pd.DataFrame(
                {
                    "year": df["CompetitionOpenSinceYear"].where(has_open, 1900),
                    "month": df["CompetitionOpenSinceMonth"].where(has_open, 1),
                    "day": 1,
                }
            )
        )
        not_open_yet = has_open & (df["Date"] < comp_open)
        df.loc[not_open_yet, ["CompetitionDistance", "CompetitionOpenSinceMonth", "CompetitionOpenSinceYear"]] = np.nan
        # Day counters from the daily calendar with its closed days, before those are dropped (issue 1, B).
        cols = ["Store", "Date", "Open", "Promo", "StateHoliday", "SchoolHoliday"]
        calendar = pd.concat([df[cols], test[cols].assign(Date=pd.to_datetime(test["Date"]))], ignore_index=True)
        df = pd.concat([df, _day_counters(calendar, df, store)], axis=1)
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
                *_FLAG_COUNTERS,
            ],
            datetime=["Date"],
        )
