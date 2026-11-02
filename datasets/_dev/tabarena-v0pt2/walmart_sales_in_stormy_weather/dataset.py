"""Curated dataset definition for `walmart_sales_in_stormy_weather` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    TaskSummary,
    Temporal,
    TemporalSplits,
    drop_columns,
)

COMPLETE_PERIOD_END = pd.Timestamp("2013-03-31")
"""The end of the only period none of whose days are in the competition's test file: from 2013-04-01 the days within 3
of each storm at a store's station are held in the encrypted test.csv, whose units were never released ("All days prior
to 2013-04-01 are given out as training data", data page). 197 store-days of the period are in neither file."""

N_WINDOWS = 9
WINDOW_DAYS = 7
GAP_DAYS = 1
"""The order for a day is placed at least a day ahead, so the day before a window is not yet known (SPLIT-10)."""
FIRST_TEST_DAY = COMPLETE_PERIOD_END - pd.Timedelta(days=N_WINDOWS * WINDOW_DAYS - 1)
"""The first day of the oldest test window (2013-01-28)."""

TRACE = {"preciptotal": 0.005, "snowfall": 0.05}
"""NOAA's "T" (a trace) as half the reporting unit: the QCLCD documentation gives "T = TRACE" and the units (inches and
hundredths of rain, inches and tenths of snow); forum topic 13200 states the thresholds (0.01 inch, 0.1 inch)."""

NUMERIC_WEATHER = [
    "tmax",
    "tmin",
    "tavg",
    "depart",
    "dewpoint",
    "wetbulb",
    "heat",
    "cool",
    "snowfall",
    "preciptotal",
    "stnpressure",
    "sealevel",
    "resultspeed",
    "resultdir",
    "avgspeed",
]
"""The numeric columns of weather.csv (NOAA QCLCD daily summary; units in noaa_weather_qclcd_documentation.pdf). They
are observed during the day, after the prediction point, so none is a feature (LEAK-10); the rain and snow totals count
the storm days of the decision tables."""


def storm_days(weather: pd.DataFrame) -> pd.Series:
    """The competition's weather event: more than an inch of rain or two inches of snow that day (data page)."""
    return (weather["preciptotal"] > 1) | (weather["snowfall"] > 2)


def clean_weather(raw: pd.DataFrame) -> pd.DataFrame:
    """weather.csv with NOAA's codes resolved: M (missing) and - (no sunrise or sunset) missing, T a trace."""
    weather = raw.copy()
    weather["date"] = pd.to_datetime(weather["date"], format="%Y-%m-%d")
    weather["station_nbr"] = weather["station_nbr"].astype(int)
    for column in NUMERIC_WEATHER:
        values = weather[column].str.strip()
        trace = values.eq("T")
        weather[column] = pd.to_numeric(values.where(~trace & ~values.isin(["M", "-"])), errors="raise")
        if column in TRACE:
            weather.loc[trace, column] = TRACE[column]
    # Sunrise and sunset are computed local standard times as HHMM: minutes after midnight.
    for column in ["sunrise", "sunset"]:
        hhmm = pd.to_numeric(weather[column].str.strip().replace("-", np.nan), errors="raise")
        weather[column] = (hhmm // 100) * 60 + hhmm % 100
    weather["codesum"] = weather["codesum"].str.strip().replace("", np.nan)
    return weather


class WalmartSalesInStormyWeather(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "How many units of a weather-sensitive product will a Walmart store sell on each day of the coming week, "
            "storm days included?"
        ),
        use_case=(
            "A Walmart replenishment manager sets the orders of products the store carries, such as milk, bread or "
            "umbrellas, for every day of the coming week, storms included (about 15% of the test days lie within 3 "
            "days of a storm), to avoid running out or overstocking."
        ),
        row=(
            "One day of one product in one store: 231 store-product pairs that sold before the test weeks, 45 "
            "stores, January 2012 to March 2013."
        ),
        predicted="The units of the product the store sold that day, scored on a logarithmic scale as in the competition.",
        known=(
            "The store, the product, the store's weather station, the date, and that day's computed sunrise and "
            "sunset at the station."
        ),
        split=(
            "Nine one-week windows from late January to March 2013, newest first, each trained on all earlier days "
            "except the last one, when the order goes out; the windows hold every day, storms included."
        ),
        changes=(
            "We keep January 2012 to March 2013, the only period none of whose days are in the competition's test "
            "file: later, the days around storms are in that file, whose sales were never released. We keep the "
            "store-product pairs that sold before the test weeks and drop the observed weather, which is known only "
            "after the day."
        ),
        fit="approximate",
        fit_reason=(
            "A zero can be a stock-out the data does not mark, and the inventory, prices and product names a "
            "manager has are missing. The competition scored only the days around storms; we score every day."
        ),
    )

    # Dataset
    unique_name = "walmart_sales_in_stormy_weather"
    year = "2015"
    domain = "business & marketing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/competitions/walmart-recruiting-sales-in-stormy-weather"
    license = (
        "Kaggle Competition Rules: the data is for the competition only ('use the Data solely for the purpose and "
        "duration of the Competition'), with no redistribution to anyone not participating"
    )
    data_tags = ("Anonymized",)
    download_description = r"""
        The competition's files (train.csv, weather.csv, key.csv, sampleSubmission.csv and the NOAA documentation;
        test.csv is encrypted and holds no units). Downloading needs an account that accepted the competition's rules
        and filled in the Walmart Recruiting Survey, which unlocks the zip (rules page).

        mkdir -p local-data-warehouse/walmart_sales_in_stormy_weather && cd local-data-warehouse/walmart_sales_in_stormy_weather
        kaggle competitions download -c walmart-recruiting-sales-in-stormy-weather -p .
        unzip walmart-recruiting-sales-in-stormy-weather.zip && rm walmart-recruiting-sales-in-stormy-weather.zip
        for f in train weather key sampleSubmission; do unzip -o $f.csv.zip && rm $f.csv.zip; done
    """
    bibtex = r"""
        @misc{walmart2015stormyweather,
          author = {{Walmart} and {Kaggle}},
          title = {Walmart Recruiting II: Sales in Stormy Weather},
          year = {2015},
          howpublished = {\url{https://www.kaggle.com/competitions/walmart-recruiting-sales-in-stormy-weather}},
          note = {Kaggle recruiting competition}
        }
    """
    curation_comments = """
        We start with train.csv, weather.csv and key.csv of the Kaggle competition (Walmart, 2015).

        - Prediction point: at the start of a week, a replenishment manager predicts each store-product's daily units for the next seven days from the store, the product, the date and the day's computed sunrise and sunset. The order for a day goes out at least a day ahead, so the day before the window is not known (a one-day gap). No later sale is an input.
        - Weather dropped: the 16 observed columns of weather.csv (temperature, rain, snow, pressure, wind, codesum) are a day's totals, which exist only after the day, so none is known at the start of the week (LEAK-10), although the competition hands them over ("it's as though you have a perfect weather forecast at your disposal", data page). As aeolus_1m and rain_in_australia. They added nothing: LightGBM scored 0.5272 with them and 0.5263 without (panel, one-day gap), and on the test rows within 3 days of a storm they made it worse by 0.006 to 0.008. Kept: the station id, and sunrise and sunset (computed in advance; HHMM local standard time as minutes after midnight, - missing). The rain and snow totals still count the storm days of the decision tables, a trace (T) as half the reporting unit.
        - History: we keep 2012-01-01 to 2013-03-31. The data page says "All days prior to 2013-04-01 are given out as training data"; from 2013-04-01 the days around storms are in the encrypted test.csv, whose units were never released (4,656 of its 4,747 store-days lie within 3 days of a storm at the store's station): 778 of the 799 storm store-days from April 2013 are missing from train.csv (decision table). Windows after March 2013 would hold almost no storm day (11 storm rows in nine weeks of autumn 2014).
        - Rows: the store-product pairs with at least one unit sold before the oldest test window (231 of 4,995); the others are products the store does not carry, which the top solutions that describe it set to 0 (1st place: "Exclude item/stores whose units are all zeros", forum topic 14452; the 3rd and 30th place the same, topic 14358). One pair first sells inside the test weeks and is left out. Store 35 has no rows before 2012-06-01, and no store has rows for 2012-12-25 (closed): 197 store-days of the period are in neither file; nothing is filled in.
        - Zeros stay as recorded sales: 41.1% of the rows. The data page: "sales number 0 doesn't necessarily mean there was no demand ... it could mean that the product was out of stock, or discontinued and not available"; 44% of the zeros sit in runs of 28 days or more. The winner predicted 0 inside long runs of zeros, a rule that reads the sales on both sides of a day.
        - Metric: RMSLE is the leaderboard's metric, but the leaderboard scored only the days within 3 of a storm, over all 4,995 pairs, 95% of them never-sold zeros; we score every day of 231 carried pairs, so our scores (about 0.52) are not comparable with it (MET-2). Dropping the never-sold pairs keeps the ranking.
        - TP-10, leg 1, RMSLE over the nine windows, paired SE across them (scripted probe, one-day gap, LightGBM with 1,000 trees on the shipped features, mean of 3 seeds): 0.5278, against each pair's own forecast picked on the nine weeks 2012-11-26 to 2013-01-27 (an exponentially weighted mean over 10 days plus half its weekday offset) 0.5358, 1.5% lower (1.4 SE; single seeds 1.2 to 1.7 SE), ahead in 7 of 9; against the best of 24 unfitted own-series forecasts picked on the windows themselves 0.5337, 1.1% lower (1.2 SE), ahead in 7 of 9. It loses the weeks of 2013-02-11 and 2013-02-18.
        - TP-10, full method: one pooled LightGBM (0.5293, one seed) beats one per store (0.5631) and one per product (0.5625) in 9 of 9 windows; the naive forecasts the method names (the same day a year earlier, with or without the change of level, the last known value, the last same weekday) score 0.70 to 0.79.
        - TP-10, leg 2: the top solutions modelled each pair's series over time. The 1st place fit a curve of log1p units against the day per pair, then a lasso on calendar terms with three weather flags ("weather features are not effective almost at all", topic 14452); the 5th a Gaussian process per pair on time; the 3rd bagged xgboost on store, product, date parts and the weather, with no lag of the sales (topic 14358). The competition's test days sat inside the training period, so the series could be read on both sides of each test day.
        - Anomaly: store 37 sold 5,568 units of product 5 on 2012-11-15, about 17 times the 99.9th percentile (forum topic 13319); it sold 3,369 on 2013-11-21, outside the period, and its next highest days are 154 and 129. Both are the Thursday one week before Thanksgiving, so we read it as a recurring order: it is in every training side and stays (CLEAN-11: unusual, not impossible).
        - store_nbr, item_nbr and station_nbr are categories (ids with no further information: "You will not be provided with more information about the products, store locations, or other details"); the stores of one station are near each other.
        - The target is log1p of the units; the metric is the competition's RMSLE on units, computed after the inverse (`target_transform="log1p"`).
    """

    # Task
    target = "log1p_units"
    problem_type = "regression"
    metric = Metric.source(
        "rmsle",
        original="Root Mean Squared Logarithmic Error (RMSLE)",
        reference="https://www.kaggle.com/competitions/walmart-recruiting-sales-in-stormy-weather/overview/evaluation",
        definition=(
            "sqrt(mean((log(p + 1) - log(a + 1))^2)) over the store-product-days of the test set, p the predicted "
            "and a the actual units, computed after the inverse of our log1p_units target."
        ),
        target_transform="log1p",
    )

    # Splits: nine one-week windows ending on the last day of the complete period.
    temporal = Temporal(
        on="date", splits=TemporalSplits(window=WINDOW_DAYS, unit="days", n_windows=N_WINDOWS, gap=GAP_DAYS)
    )
    splits_comment = """
        Nine test windows of seven days, 2013-01-28 to 2013-03-31, newest first; each trains on the days from 2012-01-01 to two days before the window: the one-day gap is the day the order goes out, as rossmann_store_sales (each train side 231 rows shorter). A week matches the competition's test unit (the 7 days from 3 before to 3 after a storm) and a weekly replenishment cycle. The windows end on 2013-03-31 because later days around storms were never released with their sales.
        The scored days differ from the competition's (SPLIT-19): it scored the storm weeks after 2013-04-01, inside its training period, whose labels were never released (0 of its 4,747 test store-days are in train.csv), so its test cannot be rebuilt. Scoring only the rows within 3 days of a storm would leave 62 to 616 rows per window, the oldest window from 2 stores; the windows score every day, 15.5% of their rows near a storm.
        All windows are late winter (SPLIT-20): 26 of their 65 storm store-days are snow, against 6.1% of the other storm store-days, and no summer storm is tested. Product 93 sells for the last time on 2013-02-21 and never again to 2014-10-31, so its 203 rows in each of the five newest windows (12.6% of each) are zeros of a discontinued product.
    """

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        sales = pd.read_csv(
            raw_dir / "train.csv",
            dtype={"store_nbr": "int16", "item_nbr": "int16", "units": "int32"},
            parse_dates=["date"],
            date_format="%Y-%m-%d",
        )
        return {
            "sales": sales,
            "key": pd.read_csv(raw_dir / "key.csv"),
            "weather": pd.read_csv(raw_dir / "weather.csv", dtype=str, keep_default_na=False),
            "test_ids": pd.read_csv(raw_dir / "sampleSubmission.csv", usecols=["id"]),
        }

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        sales, key = raw["sales"], raw["key"]
        # 1. The complete period: later days around storms are in the encrypted test file.
        df = sales[sales["date"] <= COMPLETE_PERIOD_END]
        # 2. The store-product pairs that sold before the oldest test window (the store carries the product).
        history = df[df["date"] < FIRST_TEST_DAY]
        sold = history.groupby(["store_nbr", "item_nbr"])["units"].sum()
        carried = sold[sold > 0].index
        df = df[pd.MultiIndex.from_frame(df[["store_nbr", "item_nbr"]]).isin(carried)]
        # 3. The store's weather station and that day's computed sunrise and sunset; the observed weather is known
        #    only after the day (LEAK-10).
        df = df.merge(key, on="store_nbr", how="left", validate="many_to_one")
        weather = clean_weather(raw["weather"])[["station_nbr", "date", "sunrise", "sunset"]]
        df = df.merge(weather, on=["station_nbr", "date"], how="left", validate="many_to_one")
        df["date"] = df["date"].astype("datetime64[ns]")
        # 4. The target on the competition's log scale.
        df["log1p_units"] = np.log1p(df["units"])
        return drop_columns(df, ["units"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["store_nbr", "item_nbr", "station_nbr"],
            datetime=["date"],
        )

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        sales, key = raw["sales"], raw["key"]
        weather = clean_weather(raw["weather"])
        storms = key.merge(weather.loc[storm_days(weather), ["station_nbr", "date"]], on="station_nbr")
        ids = raw["test_ids"]["id"].str.split("_", expand=True)
        test_days = pd.DataFrame({"store_nbr": ids[0].astype(int), "date": pd.to_datetime(ids[2])}).drop_duplicates()
        train_days = sales[["store_nbr", "date"]].drop_duplicates().astype({"store_nbr": int})
        storms = storms.merge(train_days.assign(in_train=True), how="left").merge(
            test_days.assign(in_encrypted_test=True), how="left"
        )
        storms["period"] = np.where(
            storms["date"] < "2013-04-01", "2012-01-01 to 2013-03-31", "2013-04-01 to 2014-10-31"
        )
        by_period = storms.groupby("period").agg(
            storm_store_days=("date", "size"),
            in_train_csv=("in_train", "sum"),
            in_encrypted_test_csv=("in_encrypted_test", "sum"),
        )

        pairs = sales[sales["date"] <= COMPLETE_PERIOD_END]
        before = pairs[pairs["date"] < FIRST_TEST_DAY].groupby(["store_nbr", "item_nbr"])["units"].sum()
        whole = pairs.groupby(["store_nbr", "item_nbr"])["units"].sum()
        pair_counts = pd.Series(
            {
                "store-product pairs": len(whole),
                "sold before 2013-01-28 (kept)": int((before > 0).sum()),
                "sold only from 2013-01-28 (left out)": int(((whole > 0) & ~(before > 0)).sum()),
                "never sold to 2013-03-31": int((whole == 0).sum()),
            },
            name="pairs",
        )

        windows = df[df["date"] >= FIRST_TEST_DAY]
        week = (windows["date"] - FIRST_TEST_DAY).dt.days // WINDOW_DAYS
        storm_flags = weather[["station_nbr", "date"]].assign(storm=storm_days(weather))
        storm_rows = pd.Series(
            windows[["station_nbr", "date"]].merge(storm_flags, how="left")["storm"].fillna(False).to_numpy(bool),
            index=windows.index,
        )
        by_window = pd.DataFrame(
            {
                "first_day": windows.groupby(week)["date"].min().dt.date,
                "rows": windows.groupby(week).size(),
                "storm_rows": storm_rows.groupby(week).sum(),
                "zero_share": (windows[self.target] == 0).groupby(week).mean().round(3),
            }
        ).rename_axis("week (oldest first)")
        return [
            Decision(
                "The period ends on 2013-03-31",
                "Storm store-days (more than an inch of rain or two inches of snow at the store's station) by period "
                "and by file: from April 2013 almost every storm day is in the encrypted test file, whose sales were "
                "never released, so test windows after March 2013 would hold almost no storm.",
                by_period,
            ),
            Decision(
                "Store-product pairs that sold before the test weeks",
                "A pair with no sale in the history is a product the store does not carry; the top solutions set "
                "those to 0. The rule reads only the days before the oldest test window.",
                pair_counts,
            ),
            Decision(
                "The test weeks hold storm days",
                "Rows, storm rows and the share of zero sales per test week.",
                by_window,
            ),
        ]
