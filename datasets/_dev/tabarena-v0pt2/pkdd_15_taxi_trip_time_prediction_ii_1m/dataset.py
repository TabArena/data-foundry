"""Curated dataset definition for `pkdd_15_taxi_trip_time_prediction_ii_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    TaskSummary,
    Temporal,
    TemporalSplits,
    drop_columns,
)

GPS_STEP_SECONDS = 15
"""One GPS point every 15 seconds; the challenge defines the travel time as (points - 1) x 15 s."""

PORTO_LAT, PORTO_LON = (41.0, 41.3), (-8.8, -8.4)
"""Greater Porto: the city, Matosinhos, Maia with the airport, Vila Nova de Gaia, Gondomar and Valongo."""

MIN_TRAVEL_TIME_S, MAX_TRAVEL_TIME_S = 60, 3 * 3600
"""Shorter trips are a meter switched on and off without a ride, longer ones a meter left running."""

MAX_STRAIGHT_LINE_KMH = 120
"""A faster straight line from the start to the end point is a GPS jump or a gap in the GPS points."""

LOCAL_END = "2014-07-01"
"""The file covers the challenge's year in UTC; its last trips start on 1 July in Porto local time."""

CALL_TYPES = {"A": "dispatch_central", "B": "taxi_stand", "C": "street"}
"""CALL_TYPE as the challenge's data page defines it."""


def _local_start_time(timestamp: pd.Series) -> pd.Series:
    """The Unix TIMESTAMP (UTC) as Porto wall-clock time, without a time zone."""
    utc = pd.to_datetime(pd.to_numeric(timestamp), unit="s", utc=True)
    return utc.dt.tz_convert("Europe/Lisbon").dt.tz_localize(None)


def _straight_line_km(lat1: pd.Series, lon1: pd.Series, lat2: pd.Series, lon2: pd.Series) -> pd.Series:
    """The great-circle distance in km between two points (haversine, Earth radius 6,371 km)."""
    lat1, lon1, lat2, lon2 = (np.radians(x) for x in (lat1, lon1, lat2, lon2))
    a = np.sin((lat2 - lat1) / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2
    return 2 * 6371 * np.arcsin(np.sqrt(a))


def _row_filters(raw: pd.DataFrame) -> list[tuple[str, pd.Series]]:
    """The row filters of `_clean`, in the order the README counts them: (reason, mask of the rows kept)."""
    travel_time = (raw["n_points"] - 1) * GPS_STEP_SECONDS
    two_points = raw["n_points"] >= 2
    distance = _straight_line_km(raw["start_lat"], raw["start_lon"], raw["end_lat"], raw["end_lon"])
    return [
        ("fewer than 2 GPS points (no travel time or no destination)", two_points),
        (
            "TRIP_ID (start second and taxi) more than once among the trips with 2 points or more",
            ~(raw["TRIP_ID"].where(two_points).duplicated(keep=False) & two_points),
        ),
        ("start outside Greater Porto", raw["start_lat"].between(*PORTO_LAT) & raw["start_lon"].between(*PORTO_LON)),
        (f"travel time under {MIN_TRAVEL_TIME_S} s", travel_time >= MIN_TRAVEL_TIME_S),
        (f"travel time over {MAX_TRAVEL_TIME_S // 3600} h", travel_time <= MAX_TRAVEL_TIME_S),
        (
            f"straight line from start to end faster than {MAX_STRAIGHT_LINE_KMH} km/h",
            distance <= MAX_STRAIGHT_LINE_KMH * travel_time / 3600,
        ),
        (
            "end point identical to the start point (no destination a passenger would name)",
            ~(raw["end_lat"].eq(raw["start_lat"]) & raw["end_lon"].eq(raw["start_lon"])),
        ),
        ("start on 2014-07-01 in Porto local time", _local_start_time(raw["TIMESTAMP"]) < LOCAL_END),
    ]


class Pkdd15TaxiTripTimePredictionIi1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How long will a Porto taxi trip take, from its start to its destination?",
        use_case=(
            "For example, at pickup a taxi company estimates the trip's duration from the start, the destination and "
            "the time, to plan when the taxi will be free again."
        ),
        row="One trip of a Porto taxi fleet, July 2013 to June 2014 (ECML/PKDD 2015 challenge).",
        predicted=("The travel time in seconds, from the trip's GPS points (one every 15 seconds), on a log scale."),
        known=(
            "The local start time, the start point and the last GPS point as the destination, how the taxi was hired "
            "(dispatch call, taxi stand or street), the stand, and the taxi."
        ),
        split=(
            "April, May and June 2014 are the test periods (30 days from the first of each month); training is a "
            "random million trips that start at least one day earlier, as for a model refit monthly."
        ),
        changes=(
            "The challenge asked for the remaining time of a trip under way; we predict the whole trip at pickup with"
            " its end point, and drop non-trips, trips that end where they start, GPS jumps, meters left running and the"
            " caller's phone number."
        ),
        fit="approximate",
        fit_reason=(
            "Everything the model sees is known at pickup except the destination: the realised drop-off (the last GPS "
            "point) stands in for a destination named at pickup, which the source's dispatch system did not record. "
            "The task is framed without a routing estimate."
        ),
    )

    # Dataset
    unique_name = "pkdd_15_taxi_trip_time_prediction_ii_1m"
    version_of = "pkdd_15_taxi_trip_time_prediction_ii"
    version_comment = """
        The cleaned frame holds 1,655,893 trips, above the 1.5M-row budget, and the train side of every window holds more than 1M. We sample per test window (v2 split protocol): each window keeps at most 500k of its rows (all of them here), and its train side is a random 1M of the trips that start at least one day earlier, drawn in one random order for all windows; the frame keeps only the rows a split uses.
    """
    year = "2015"
    domain = "industry & manufacturing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/c/pkdd-15-taxi-trip-time-prediction-ii"
    license = "CC BY 4.0"
    data_tags = ("Spatial",)
    download_description = """
        The training set of the ECML/PKDD 2015 Discovery Challenge, which its organisers donated to the UCI repository
        (id 339, CC BY 4.0, https://doi.org/10.24432/C55W25). The Kaggle download needs the competition's rules
        accepted (403 on our account). The UCI zip holds train.csv.zip of 533,605,607 bytes, the size to the byte of
        the train.csv.zip that `kaggle competitions files` lists for both PKDD 2015 competitions; its train.csv holds
        the 1,710,670 trips of the challenge. We keep train.csv only (sha256
        2891d03ea99ce0fc203daedd434848a1a8baa7a8fb6da10f8d7ff26559efff6d, downloaded 2026-10-06); `_prepare_raw_files`
        writes trips.parquet next to it.

        mkdir -p local-data-warehouse/pkdd_15_taxi_trip_time_prediction_ii && cd local-data-warehouse/pkdd_15_taxi_trip_time_prediction_ii
        wget -O taxi_service_trajectory.zip "https://archive.ics.uci.edu/static/public/339/taxi+service+trajectory+prediction+challenge+ecml+pkdd+2015.zip"
        unzip taxi_service_trajectory.zip train.csv.zip && unzip train.csv.zip && rm taxi_service_trajectory.zip train.csv.zip
    """
    bibtex = r"""
        @misc{moreiramatias2013taxi,
          author       = {Moreira-Matias, Luis and Ferreira, Michel and Mendes-Moreira, Jo{\~a}o and others},
          title        = {{Taxi Service Trajectory - Prediction Challenge, ECML PKDD 2015}},
          year         = {2013},
          howpublished = {UCI Machine Learning Repository},
          doi          = {10.24432/C55W25},
          note         = {Training set of the ECML/PKDD 2015 Discovery Challenge (Kaggle: pkdd-15-taxi-trip-time-prediction-ii)}
        }
    """
    curation_comments = """
        We start with train.csv of the ECML/PKDD 2015 Discovery Challenge (UCI id 339): 1,710,670 Porto taxi trips from 2013-07-01 to 2014-06-30, each with its GPS trajectory (`POLYLINE`, one point every 15 s).

        - Prediction point: the start of the trip, when the meter is switched on. The task is the travel time from origin and destination, an ETA task like `nyc_taxi_trip_duration` (the challenge's Task II starts from a partial trajectory).
        - Anomaly: the challenge page says that drivers "do not indicate the final destination of the ride" to the dispatch system. Our destination is the last GPS point, a stand-in for a destination named at pickup (`fit="approximate"`, as `nyc_taxi_trip_duration`), the curator's framing (record, CC 2026-09-21). Without it, LightGBM's R^2 is 0.12 to 0.15 (800 trees, learning rate 0.08, 255 leaves, local hour, weekday and day of year, one fit per split).
        - Target: `log1p_travel_time`, log1p of the travel time in seconds, (GPS points - 1) x 15, the challenge's definition; RMSE on it is the challenge's metric, RMSLE.
        - `_prepare_raw_files` parses each polyline into its number of points and its first and last point; the route is known only after the trip and is not a feature.
        - `start_time`: TIMESTAMP is Unix time in UTC; the pickup profile by UTC hour shifts by one hour at both daylight-saving switches (decision table), so we convert it to Porto local time without a time zone.
        - Rows dropped (counts in the decision table): under 2 GPS points; a TRIP_ID that occurs twice or more (we cannot tell which copy is right); a start outside Greater Porto (lat 41.0 to 41.3, lon -8.8 to -8.4); under 1 minute (a meter switched on and off without a ride) or over 3 hours (a meter left running); a straight line from start to end faster than 120 km/h (a GPS jump); an end point identical to the start point (no destination a passenger would name, as in `nyc_taxi_trip_duration`); and the last trips, which start on 1 July 2014 in local time. The 1-minute cut sits on a slope (other filters on): 71% of 15-second trips end within 100 m of their start, 53% at 30 s, 41% at 45 s, 32% at 60 s and 7% at 120 s, against 1.9% of all trips.
        - We drop TRIP_ID (an id, the start second and the taxi), DAY_TYPE (constant "A"; the data page says it "has not been correctly calculated") and MISSING_DATA (erroneous per Lam et al. 2015, arXiv:1509.05257, and it describes the trajectory).
        - We drop ORIGIN_CALL, the anonymised phone number of a dispatch-central customer: an identifier redundant with the destination. With the destination known it changes LightGBM's R^2 by -0.004 to -0.001 (same setup).
        - `call_type` A, B and C become dispatch_central, taxi_stand and street. `origin_stand` is empty unless the taxi was hired at a stand; we set the empty strings missing.
        - `taxi_id` stays a categorical feature, since the taxi is known at pickup; it adds 0.008 to 0.014 to LightGBM's R^2 (same setup) and is its top feature by gain. The fleet is the same in every month (decision table), so the split is temporal and not grouped by taxi.
        - Anomaly: we keep the 1.2% of trips that jump more than 1 km between two GPS points (missing points, Lam et al. 2015), trips with a drive back on the meter, and the 65,618 (4.0%) that end within 500 m of their start but not at the same point: a meter left on or a round trip is unusual, not impossible.
    """

    # Task
    target = "log1p_travel_time"
    problem_type = "regression"

    # Splits
    temporal = Temporal(
        on="start_time",
        splits=TemporalSplits(window=30, unit="days", cutoffs=("2014-04-01", "2014-05-01", "2014-06-01"), gap=1),
    )
    splits_comment = """
        A model refit every month predicts the travel times of the next month's trips: 3 test windows of 30 days that start on 1 June, 1 May and 1 April 2014 (newest first; the May window leaves out 31 May), and train is the trips that start at least one day before the window. The gap of one day is part of the task: a trip lasts up to 3 hours, so at a refit the last trips before it have no travel time yet; without the gap 48, 36 and 8 train trips per window (June, May, April) would end after the window start, with it none. Each window keeps all of its trips (131,648 to 151,406, under the 500k budget); each train side is a random 1M of the eligible earlier trips (one random order for all windows). The monthly length follows the source: the challenge tested on 320 trips 1.5 to 6 months after its training year. The file covers one year, so the April to June test season has no earlier copy in train.
    """
    subsample_to_budget = True

    # train.csv holds every GPS point of every trip (1.9 GB of text); `_prepare_raw_files` parses the polylines once
    # into their number of points and their first and last point, and `_load_raw` starts from that table.
    prepared_raw_files = ("trips.parquet",)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        import polars as pl

        trips = pl.read_csv(raw_dir / "train.csv", infer_schema=False)  # every column as text, as in the file
        points = trips["POLYLINE"].str.json_decode(dtype=pl.List(pl.List(pl.Float64)))  # [[lon, lat], ...]
        first, last = points.list.first(), points.list.last()
        trips = trips.drop("POLYLINE").with_columns(
            n_points=points.list.len().cast(pl.Int64),
            start_lon=first.list.get(0, null_on_oob=True),
            start_lat=first.list.get(1, null_on_oob=True),
            end_lon=last.list.get(0, null_on_oob=True),
            end_lat=last.list.get(1, null_on_oob=True),
        )
        trips.write_parquet(raw_dir / "trips.parquet")

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_parquet(raw_dir / "trips.parquet")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        keep = np.logical_and.reduce([mask.to_numpy() for _, mask in _row_filters(df)])
        df = df[keep]
        # TRIP_ID is the start second and the taxi; DAY_TYPE is constant; MISSING_DATA is unreliable and post-trip;
        # ORIGIN_CALL, the caller's phone id, is an identifier redundant with the destination (curation_comments).
        df = drop_columns(df, ["TRIP_ID", "ORIGIN_CALL", "DAY_TYPE", "MISSING_DATA"])
        df = df.assign(
            CALL_TYPE=df["CALL_TYPE"].map(CALL_TYPES),
            ORIGIN_STAND=df["ORIGIN_STAND"].where(df["ORIGIN_STAND"] != ""),  # empty unless hired at a stand
            TIMESTAMP=_local_start_time(df["TIMESTAMP"]),
            log1p_travel_time=np.log1p((df["n_points"] - 1) * GPS_STEP_SECONDS),
        )
        df = drop_columns(df, ["n_points"])
        return df.rename(
            columns={
                "CALL_TYPE": "call_type",
                "ORIGIN_STAND": "origin_stand",
                "TAXI_ID": "taxi_id",
                "TIMESTAMP": "start_time",
            }
        )

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["call_type", "origin_stand", "taxi_id"], datetime=["start_time"])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        del df
        # The rows each filter drops, in order.
        left = pd.Series(True, index=raw.index)
        steps = []
        for reason, keep in _row_filters(raw):
            kept = left & keep
            steps.append({"rows dropped": reason, "dropped": int(left.sum() - kept.sum()), "left": int(kept.sum())})
            left = kept
        filters = pd.DataFrame(steps)

        # The taxis of each test month already drove in the months before it.
        trips = raw.loc[left, ["TAXI_ID", "TIMESTAMP"]]
        month = _local_start_time(trips["TIMESTAMP"]).dt.to_period("M")
        recurring = []
        for window in sorted(month.unique())[-3:]:
            earlier = set(trips.loc[month < window, "TAXI_ID"])
            taxis = trips.loc[month == window, "TAXI_ID"]
            recurring.append(
                {
                    "test month": str(window),
                    "trips": len(taxis),
                    "taxis": taxis.nunique(),
                    "taxis new in this month": int((~pd.Series(taxis.unique()).isin(earlier)).sum()),
                    "trips by a taxi seen before": f"{taxis.isin(earlier).mean():.2%}",
                }
            )

        # Weekday pickups by UTC hour, two weeks before and after each daylight-saving switch: the profile moves by
        # one UTC hour, so the timestamps are UTC and local time is the clock the city keeps.
        utc = pd.to_datetime(pd.to_numeric(raw["TIMESTAMP"]), unit="s")

        def profile(start: str, end: str) -> np.ndarray:
            hours = utc[(utc >= start) & (utc < end) & (utc.dt.dayofweek < 5)].dt.hour
            return hours.value_counts(normalize=True).reindex(range(24), fill_value=0).to_numpy()

        switches = {
            "2013-10-27, summer to winter time": ("2013-10-14", "2013-10-26", "2013-10-28", "2013-11-09", -1),
            "2014-03-30, winter to summer time": ("2014-03-17", "2014-03-29", "2014-03-31", "2014-04-12", 1),
        }
        clock = []
        for switch, (b0, b1, a0, a1, shift) in switches.items():
            before, after = profile(b0, b1), profile(a0, a1)
            clock.append(
                {
                    "switch": switch,
                    "correlation, same UTC hour": round(float(np.corrcoef(before, after)[0, 1]), 3),
                    "correlation, shifted by one hour": round(
                        float(np.corrcoef(before, np.roll(after, shift))[0, 1]), 3
                    ),
                }
            )

        return [
            Decision(
                "Rows dropped before the split",
                "Trips without a travel time or a destination, duplicate ids, GPS errors, meter misuse and trips that "
                "end where they start go, and so do the last trips of the file, which start on 1 July in local time.",
                filters,
            ),
            Decision(
                "Temporal split; the taxi stays a feature, not a group",
                "A v2 task is grouped or temporal, not both, so the verdict's 'temporal split, taxi as group' can only "
                "be one of them. The fleet is the same in every month (99.93% to 100% of each test month's trips are "
                "by taxis seen before), so a model in use predicts trips of taxis it has seen; a split by taxi would "
                "test new drivers, which deployment rarely meets.",
                pd.DataFrame(recurring),
            ),
            Decision(
                "Start time in Porto local time",
                "TIMESTAMP is Unix time (UTC): the weekday pickup profile moves by one UTC hour at each daylight-saving "
                "switch and matches again once shifted, so hours of the day are only comparable in local time.",
                pd.DataFrame(clock),
            ),
        ]
