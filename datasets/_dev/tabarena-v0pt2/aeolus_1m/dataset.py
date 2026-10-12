"""Curated dataset definition for `aeolus_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Temporal, TemporalSplits, drop_columns

DELAY_THRESHOLD_MINUTES = 15
"""US DOT: a flight is on time when it arrives less than 15 minutes after its scheduled arrival (BTS `ARR_DEL15`)."""

PRECIPITATION_CODE_MM = 200
"""Hourly precipitation from 200 mm on is a missing-value code: 213.4 to 257.3 mm (8.4 to 10.1 inches)."""

MIN_SCHEDULED_MINUTES = 15
"""Scheduled block times below 15 minutes are errors; the shortest real hop (Wrangell-Petersburg) is 18 minutes."""

FLIGHT_KEY = ["FL_DATE", "OP_CARRIER", "OP_CARRIER_FL_NUM", "ORIGIN", "DEST", "CRS_DEP_TIME"]
"""One scheduled flight: date, carrier, flight number, route and scheduled departure."""

SKIPPED_COLUMNS = (
    "DEP_DELAY",
    "TAXI_OUT",
    "WHEELS_OFF",
    "WHEELS_ON",
    "TAXI_IN",
    "ACTUAL_ELAPSED_TIME",
    "AIR_TIME",
    "FLIGHTS",
    "MONTH",
    "DAY_OF_MONTH",
    "DAY_OF_WEEK",
    "ORIGIN_INDEX",
    "DEST_INDEX",
)
"""Source columns `_load_raw` does not read: recorded at or after the departure (DEP_DELAY to AIR_TIME), always 1
(FLIGHTS), parts of FL_DATE (MONTH, DAY_OF_MONTH, DAY_OF_WEEK) and one index per airport code."""

SUMMER_ZONES = {
    "JFK": "America/New_York",
    "ATL": "America/New_York",
    "ORD": "America/Chicago",
    "DEN": "America/Denver",
    "PHX": "America/Phoenix",
    "LAX": "America/Los_Angeles",
    "SEA": "America/Los_Angeles",
    "ANC": "America/Anchorage",
    "HNL": "Pacific/Honolulu",
}
"""Nine airports across the US time zones, for the second decision (the daily temperature cycle)."""


class Aeolus1m(AbstractCuratedDataset):
    # Dataset
    unique_name = "aeolus_1m"
    version_of = "aeolus"
    version_comment = """
        The nine years hold 54,674,003 flights. We sample per test window (v2 split protocol): each window keeps at most 500k of its rows (all of them here), and its train side is a random 1M of all earlier flights, drawn in one random order for all windows; the frame keeps only the rows a split uses. We follow TabReD and use random sub-sampling of the train data. The idea behind this instead of a time-based subsampling is to keep data from various time periods and model the distribution shift across the full time horizon.
    """
    year = "2025"
    domain = "business & marketing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/flnny123/mfddmulti-modal-flight-delay-dataset"
    license = "Apache-2.0 (Kaggle data card); the paper (Appendix A.3) states CC BY-NC 4.0"
    data_tags = ("Spatial",)
    download_description = """
        The nine yearly tables of the release's tabular modality (Aeolus/Flight_Tab, 15.2 GB) from the authors' Kaggle
        dataset; the flight-chain (.pt) and flight-network (.dgl) files of the release are not used. Kaggle offers no
        versioned download for this dataset: the files are dated 2025-10-17 (downloaded 2026-10-07).

        mkdir -p local-data-warehouse/aeolus && cd local-data-warehouse/aeolus
        for year in 2016 2017 2018 2019 2020 2021 2022 2023 2024; do
            kaggle datasets download flnny123/mfddmulti-modal-flight-delay-dataset -f Aeolus/Flight_Tab/flight_with_weather_${year}.csv -p .
        done

        SHA-256 of the CSVs (first 16 hex digits): 2016 4ed92ed732721a38, 2017 67b8dbd6678576b1, 2018 0398bab8f1b79a5f,
        2019 eec50211a1a63f37, 2020 787981046c9fe0f4, 2021 5b7cc4801a6ff5cf, 2022 45eb45e801d6eeeb,
        2023 9c9e20f55d3dd10a, 2024 f938ade95a031088. `_prepare_raw_files` writes aeolus_flights.parquet next to them.
    """
    bibtex = """
        @inproceedings{xu2025aeolus,
          title     = {Aeolus: A Multi-structural Flight Delay Dataset},
          author    = {Xu, Lin and Yuan, Xinyun and Liang, Yuxuan and Yin, Suwan and Wu, Yuankai},
          booktitle = {Advances in Neural Information Processing Systems (NeurIPS 2025), Datasets and Benchmarks Track},
          year      = {2025},
          note      = {arXiv:2510.26616},
        }
    """
    curation_comments = """
        We start with the nine yearly tables `Aeolus/Flight_Tab/flight_with_weather_<year>.csv` (2016-2024) of the authors' Kaggle release of Aeolus (Xu et al., NeurIPS 2025): 54,674,003 completed US domestic flights with hourly Meteostat weather at both airports.

        - Prediction point: shortly before the scheduled departure, with the paper's tabular features (Table 9).
        - Target: `ARR_DEL15` is "Yes" for an arrival 15 minutes or more after the schedule, the US DOT definition and the paper's classification task. We do not use the minutes (ARR_DELAY): in every year the 1% longest delays hold 56-71% of their variance, so an RMSE would mostly score a few extreme delays (third decision).
        - Note: the authors' classifier code labels `abs(ARR_DELAY) > 15`, which counts early arrivals as delayed; we follow the DOT definition.
        - Dropped as recorded at or after the departure: `_load_raw` skips DEP_DELAY, TAXI_OUT, WHEELS_OFF, WHEELS_ON, TAXI_IN, ACTUAL_ELAPSED_TIME and AIR_TIME; `_clean` drops DEP_TIME and ARR_TIME (read for the first decision) and ARR_DELAY, the target's source.
        - `_load_raw` also skips FLIGHTS (always 1), ORIGIN_INDEX and DEST_INDEX (one per airport code) and MONTH, DAY_OF_MONTH and DAY_OF_WEEK (parts of FL_DATE).
        - CRS_DEP_TIME and CRS_ARR_TIME are local clock times dated on the flight date, also after midnight. We keep their time of day as minutes since midnight (`CRS_DEP_TIME_MIN`, `CRS_ARR_TIME_MIN`, as the authors' code does).
        - Anomaly: the release joined Meteostat's hourly records, whose timestamps are UTC, to the local scheduled clock times (first and second decision). So the origin weather is from a median 5.2 hours before the departure, the destination weather a median 3.0 hours.
        - Potential leak, kept on purpose: the destination weather of 1.86% of the flights (1.0% in each test week) is read after the scheduled departure, a median 0.75 hours after it, and the 3,243 departures from Guam get weather from after the departure. All of the destination weather adds 0.010 to 0.016 ROC AUC (untuned LightGBM), an upper bound for its late part. We keep the weather as released; re-joining it would be our own fix. Revisit if the authors correct the join.
        - Proxy missing values: hourly precipitation of 213.4 to 257.3 mm is a missing-value code, 99.8% of it at EWR, LGA and JFK in 2016-2018 (fourth decision). We set values from 200 mm on to missing. Scheduled block times below 15 minutes (17 rows) become missing; the shortest real hop is 18 minutes.
        - Duplicates: one scheduled flight occurs twice with arrival delays of 941 and 4 minutes; we drop both rows.
        - OP_CARRIER_FL_NUM is categorical (the paper's Table 9): a flight number names a recurring service of its carrier.
        - Task probes flag no_spread at 50k training rows per window and not at 300k; the benchmark trains on 1M.
        - Note: the release holds no cancelled or diverted flights, so the task is the delay of a flight that operates.
        - Anomaly: 2020 (COVID-19) has 9.7% delayed flights against 17-21% in the other years.
        - Anomaly: March 2024 is missing from the release; the test weeks are not affected.
    """

    # Task
    target = "ARR_DEL15"
    problem_type = "binary_classification"

    # Splits
    splits_comment = """
        A delay model is refit every week and predicts the flights of the week ahead from the schedule and the weather. We use each of the last 3 weeks of 2024 as a test window (2024-12-25 to 12-31, 12-18 to 12-24 and 12-11 to 12-17, newest first). Train is every flight dated at least two days before the window (a one-day gap): a flight's arrival delay is known only once it has landed, and the previous evening's departures and long delays land after midnight. Each window keeps all of its flights (127,743, 130,808 and 128,644); each train side is a random 1M of all earlier flights back to 2016 (one random order for all windows), following TabReD. Training on 1M flights from 2022 on or from 2024 alone gave no consistently better LightGBM (ROC AUC from 2016, 2022 and 2024 on: 0.652, 0.628 and 0.648 in the newest window, 0.618, 0.624 and 0.617 in the second, 0.615, 0.625 and 0.643 in the third), so we keep the whole release.
    """
    temporal = Temporal(on="FL_DATE", splits=TemporalSplits(window=7, unit="days", n_windows=3, gap=1))
    subsample_to_budget = True

    # The nine CSVs (15.2 GB) are too large for pandas: `_prepare_raw_files` converts them once, streaming with
    # polars, into one parquet file with every source column and the timestamps parsed.
    prepared_raw_files = ("aeolus_flights.parquet",)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        import polars as pl

        files = sorted(raw_dir.glob("flight_with_weather_*.csv"))
        assert len(files) == 9, f"Expected the nine yearly files 2016-2024, found {len(files)}."
        header = files[0].open().readline().strip().split(",")
        timestamps = ["FL_DATE", "CRS_DEP_TIME", "DEP_TIME", "WHEELS_OFF", "WHEELS_ON", "CRS_ARR_TIME", "ARR_TIME"]
        text = [*timestamps, "OP_CARRIER", "ORIGIN", "DEST"]
        integers = ["MONTH", "DAY_OF_MONTH", "DAY_OF_WEEK", "ORIGIN_INDEX", "DEST_INDEX"]
        schema = {c: pl.String if c in text else pl.Int64 if c in integers else pl.Float64 for c in header}
        frames = [pl.scan_csv(f, schema=schema) for f in files]
        pl.concat(frames, how="vertical").with_columns(
            pl.col(c).str.to_datetime("%Y-%m-%d %H:%M:%S", time_unit="us", strict=True) for c in timestamps
        ).sink_parquet(raw_dir / "aeolus_flights.parquet")

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        import pyarrow.parquet as pq

        path = raw_dir / "aeolus_flights.parquet"
        columns = [c for c in pq.read_schema(path).names if c not in SKIPPED_COLUMNS]  # in the source's order
        table = pq.read_table(path, columns=columns, read_dictionary=["OP_CARRIER", "ORIGIN", "DEST"])
        return table.to_pandas(split_blocks=True, self_destruct=True)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # One flight recorded twice with different outcomes: both copies go (the mask is applied after the drops).
        duplicated = df.duplicated(subset=FLIGHT_KEY, keep=False).to_numpy()
        # Target: an arrival 15 minutes or more after the schedule (US DOT on-time definition, BTS `ARR_DEL15`).
        late = (df["ARR_DELAY"] >= DELAY_THRESHOLD_MINUTES).to_numpy().astype("int8")
        df["ARR_DEL15"] = pd.Categorical.from_codes(late, categories=["No", "Yes"])
        # The scheduled times as local minutes since midnight (their date part is FL_DATE, also after midnight).
        for col in ("CRS_DEP_TIME", "CRS_ARR_TIME"):
            df[f"{col}_MIN"] = (df[col].dt.hour * 60 + df[col].dt.minute).astype("int64")
        # Proxy missing values: the precipitation code and impossible scheduled block times.
        for col in ("O_PRCP", "D_PRCP"):
            df[col] = df[col].mask(df[col] >= PRECIPITATION_CODE_MM)
        df["CRS_ELAPSED_TIME"] = df["CRS_ELAPSED_TIME"].mask(df["CRS_ELAPSED_TIME"] < MIN_SCHEDULED_MINUTES)
        # A flight number is a label of its carrier, not a quantity (the CSV writes 4814.0).
        df["OP_CARRIER_FL_NUM"] = df["OP_CARRIER_FL_NUM"].astype("int64")
        # Categories in sorted order, whatever order the parquet dictionary had.
        for col in ("OP_CARRIER", "ORIGIN", "DEST"):
            df[col] = df[col].cat.reorder_categories(sorted(df[col].cat.categories))
        df = drop_columns(
            df,
            [
                "DEP_TIME",  # the actual times, read for the first decision only
                "ARR_TIME",
                "ARR_DELAY",  # the target's source
                "CRS_DEP_TIME",  # replaced by CRS_DEP_TIME_MIN
                "CRS_ARR_TIME",  # replaced by CRS_ARR_TIME_MIN
            ],
        )
        return df[~duplicated]

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["OP_CARRIER", "OP_CARRIER_FL_NUM", "ORIGIN", "DEST"],
            datetime=["FL_DATE"],
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        del df
        year = raw["FL_DATE"].dt.year
        # 1. Which times the weather belongs to: in 2024, the share of (airport, hour) groups of flights with one value.
        times = ["CRS_DEP_TIME", "DEP_TIME", "CRS_ARR_TIME", "ARR_TIME"]
        last = raw.loc[(year == 2024).to_numpy(), ["ORIGIN", "DEST", "O_TEMP", "D_TEMP", *times]]
        rows = []
        for side, airport, weather, keys in (
            ("origin", "ORIGIN", "O_TEMP", ("CRS_DEP_TIME", "DEP_TIME")),
            ("destination", "DEST", "D_TEMP", ("CRS_ARR_TIME", "ARR_TIME")),
        ):
            for key in keys:
                for how in ("nearest, half up", "floor"):
                    shift = pd.Timedelta(minutes=30 if how == "floor" else 0)
                    hour = (last[key] + pd.Timedelta(minutes=30) - shift).dt.floor("h")
                    groups = last.groupby([last[airport], hour], observed=True)[weather].agg(["nunique", "size"])
                    groups = groups[(groups["size"] > 1) & (groups["nunique"] > 0)]
                    rows.append(
                        {
                            "weather": side,
                            "time": key,
                            "hour": how,
                            "groups of 2+ flights": len(groups),
                            "share with one value": round(float((groups["nunique"] == 1).mean()), 4),
                        }
                    )
        alignment = pd.DataFrame(rows)

        # 2. The clock hour was read as UTC: the coldest and warmest scheduled departure hours of summer 2024 per
        # airport (mean origin temperature, hours with 30 or more flights), and the local time of those readings.
        summer = (
            (raw["FL_DATE"] >= "2024-06-01") & (raw["FL_DATE"] < "2024-09-01") & raw["ORIGIN"].isin(list(SUMMER_ZONES))
        )
        flights = raw.loc[summer.to_numpy(), ["ORIGIN", "CRS_DEP_TIME", "O_TEMP"]]
        clock = (flights["CRS_DEP_TIME"] + pd.Timedelta(minutes=30)).dt.floor("h").dt.hour.rename("clock")
        means = flights.groupby([flights["ORIGIN"].astype(str), clock])["O_TEMP"].agg(["mean", "size"])
        means = means[means["size"] >= 30]
        cycle = []
        for airport, zone in SUMMER_ZONES.items():
            offset = int(pd.Timestamp("2024-07-01", tz=zone).utcoffset().total_seconds() // 3600)
            hours = means.loc[airport, "mean"].sort_values(kind="stable")
            coldest, warmest = int(hours.index[0]), int(hours.index[-1])
            cycle.append(
                {
                    "airport": airport,
                    "UTC offset (July)": offset,
                    "coldest scheduled hour": coldest,
                    "coldest mean (C)": round(float(hours.iloc[0]), 1),
                    "coldest reading, local hour": (coldest + offset) % 24,
                    "warmest scheduled hour": warmest,
                    "warmest mean (C)": round(float(hours.iloc[-1]), 1),
                    "warmest reading, local hour": (warmest + offset) % 24,
                }
            )
        utc_reading = pd.DataFrame(cycle)

        # 3. The target: the minutes are dominated by a few long delays; the 15-minute indicator is not.
        delay = raw["ARR_DELAY"]
        per_year = []
        for y, minutes in delay.groupby(year):
            squared = (minutes - minutes.mean()) ** 2
            top = minutes >= minutes.quantile(0.99)
            per_year.append(
                {
                    "year": int(y),
                    "flights": len(minutes),
                    "mean delay (min)": round(float(minutes.mean()), 2),
                    "share 15 min or more": round(float((minutes >= DELAY_THRESHOLD_MINUTES).mean()), 4),
                    "99th percentile (min)": float(minutes.quantile(0.99)),
                    "variance share of the top 1%": round(float(squared[top].sum() / squared.sum()), 3),
                }
            )
        target = pd.DataFrame(per_year)

        # 4. The precipitation code: where and when it occurs.
        coded = pd.concat(
            [
                raw.loc[raw[f"{p}_PRCP"] >= PRECIPITATION_CODE_MM, [airport, f"{p}_PRCP", "FL_DATE"]].set_axis(
                    ["airport", "precipitation (mm)", "date"], axis=1
                )
                for p, airport in (("O", "ORIGIN"), ("D", "DEST"))
            ]
        )
        coded["airport"] = coded["airport"].astype(str)
        code_table = (
            coded.groupby("airport")
            .agg(
                values=("precipitation (mm)", "size"),
                lowest=("precipitation (mm)", "min"),
                highest=("precipitation (mm)", "max"),
                first=("date", "min"),
                last=("date", "max"),
            )
            .sort_values("values", ascending=False, kind="stable")
        )
        below = max(float(raw.loc[raw[c] < PRECIPITATION_CODE_MM, c].max()) for c in ("O_PRCP", "D_PRCP"))
        return [
            Decision(
                "The weather is looked up by the scheduled clock times",
                "Grouped by airport and scheduled time rounded to the nearest hour (half up), every group of 2024 "
                "flights shares one weather value; grouped by the actual times far fewer do. So the actual departure "
                "and arrival, which carry the delay, played no part in the lookup. The next decision shows which hour "
                "the lookup returned.",
                alignment,
            ),
            Decision(
                "The scheduled clock hour was read as UTC: the weather is from 3.5 to 10 hours earlier",
                "The release joined Meteostat's hourly records, whose timestamps are UTC, to the local scheduled "
                "clock times. Read as local time, each airport's daily temperature cycle is shifted by its UTC offset "
                "(Honolulu would be coldest at 15 h and warmest at midnight); read as UTC, the coldest readings fall "
                "at 4-6 h and the warmest at 12-17 h local time at all nine airports. Meteostat's station files "
                "agree: read as UTC, the origin temperatures of 2024 equal them at 99.6% to 100% of the "
                "airport-hours at JFK, ORD, DEN, PHX, LAX, SEA and HNL, against 2% to 8% at the airports' real "
                "offsets (checked 2026-10-07; the station files are not part of the raw data).",
                utc_reading,
            ),
            Decision(
                "Target: arrival 15 minutes or more late",
                "In every year the 1% longest delays hold most of the variance of the arrival delay in minutes, so "
                "an RMSE on the minutes would mostly score a few extreme delays. The 15-minute indicator is the US "
                "DOT definition and the paper's classification task.",
                target,
            ),
            Decision(
                "Precipitation of 200 mm or more in an hour is a code, set to missing",
                f"The values cluster at 213-257 mm (8.4 to 10.1 inches) at three New York airports in 2016-2018; the "
                f"largest value below them is {below} mm. At JFK, Meteostat's station record (74486, read on "
                f"2026-10-07) has no precipitation value at any of the 39 coded hours of 2016-2018 and equals the "
                f"release at all 21,398 other hours where it has one: the code stands for a missing reading.",
                code_table,
            ),
        ]
