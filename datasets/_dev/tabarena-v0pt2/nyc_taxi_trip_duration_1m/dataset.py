"""Curated dataset definition for `nyc_taxi_trip_duration_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from data_foundry.definition import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    Source,
    TaskSummary,
    Temporal,
    TemporalSplits,
    drop_columns,
)

FIRST_DAY, LAST_DAY = "2016-04-21", "2016-06-30"
"""The pickup days we download. 30 June 2016 is the last day the TLC trip records carry coordinates (from July on
they carry taxi zones only); 21 April is the first day that leaves the Memorial Day window (27 May) half the trips
for training."""

OPEN_DATA = "open_data"
"""The folder under the raw folder that holds one CSV per pickup day (``2016-04-21.csv`` ...)."""

OPEN_DATA_COLUMNS = [
    "vendorid",
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "passenger_count",
    "pickup_longitude",
    "pickup_latitude",
    "dropoff_longitude",
    "dropoff_latitude",
    "ratecodeid",
    "store_and_fwd_flag",
]
"""The columns we download. The others (trip distance, payment type, the fare and its parts) are set at the end of
the trip."""

MIN_SECONDS = 30
"""Shorter records are not rides: most start and end at one point (the meter engaged and disengaged in place)."""

MIN_STRAIGHT_LINE_KM = 0.1
"""A trip that ends closer to its pickup has no destination a passenger would name (CC 2026-10-26, as in pkdd)."""

MAX_STRAIGHT_LINE_KMH = 120
"""A faster straight line from pickup to drop-off is a broken clock or a broken GPS fix: no route is shorter than the
straight line, and the region's highest speed limit is 65 mph (105 km/h). The constant of
pkdd_15_taxi_trip_time_prediction_ii_1m and 2024_lusaka_mobility_prediction_hackathon."""

MAX_SECONDS = 3 * 3600
"""Longer records have a broken clock: the trips thin out towards 3 h, then a cluster just below 24 h follows
(VeriFone meters) at walking speed."""

LONGITUDE = (-75.0, -72.0)
LATITUDE = (40.0, 41.5)
"""A box around New York City (Manhattan lies at -74.0, 40.75), reaching about 80 km west, north and south and
170 km east: it keeps the airports, New Jersey, Long Island, Westchester and Connecticut."""

COORDINATES = ["pickup_longitude", "pickup_latitude", "dropoff_longitude", "dropoff_latitude"]

PASSENGER_SEATS = 6
"""A yellow cab seats at most 5 passengers, a minivan cab 6. A count of 0 means the driver did not enter it, and more
than 6 cannot be carried: both are set to missing."""

VENDORS = {1: "Creative Mobile Technologies", 2: "VeriFone"}
"""TLC data dictionary: "1=Creative Mobile Technologies, LLC; 2=VeriFone Inc."."""

RATE_CODES = {
    1: "Standard rate",
    2: "JFK",
    3: "Newark",
    4: "Nassau or Westchester",
    5: "Negotiated fare",
    6: "Group ride",
}
"""TLC data dictionary (RateCodeID). The code 99 is not in the dictionary and is set to missing."""

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def read_open_data(raw_dir: Path) -> pd.DataFrame:
    """The downloaded trips of FIRST_DAY to LAST_DAY, one CSV per pickup day, in day order."""
    days = pd.date_range(FIRST_DAY, LAST_DAY, freq="D").strftime("%Y-%m-%d")
    dtypes = {"vendorid": "int64", "passenger_count": "int64", "ratecodeid": "int64", "store_and_fwd_flag": "string"}
    frames = [pd.read_csv(raw_dir / OPEN_DATA / f"{day}.csv", dtype=dtypes) for day in days]
    return pd.concat(frames, ignore_index=True)[OPEN_DATA_COLUMNS]


def trips(raw: pd.DataFrame) -> pd.DataFrame:
    """The raw trips without exact copies, with the times in the TLC's wall-clock format and the duration in seconds.

    Used by ``_clean`` and ``_decisions``.
    """
    df = raw[~raw.duplicated(keep="first")]
    pickup = pd.to_datetime(df["tpep_pickup_datetime"], format="ISO8601")
    dropoff = pd.to_datetime(df["tpep_dropoff_datetime"], format="ISO8601")
    return pd.DataFrame(
        {
            "vendor_id": df["vendorid"],
            "pickup_datetime": pickup.dt.strftime(TIME_FORMAT),
            "passenger_count": df["passenger_count"],
            **{c: df[c] for c in COORDINATES},
            "ratecodeid": df["ratecodeid"],
            "store_and_fwd_flag": df["store_and_fwd_flag"],
            "trip_duration": (dropoff - pickup).dt.total_seconds(),
        },
        index=df.index,
    )


def haversine_km(df: pd.DataFrame) -> pd.Series:
    """The great-circle distance between the pickup and the dropoff point in km (evidence only, not a feature)."""
    lon1, lat1, lon2, lat2 = (np.radians(df[c]) for c in COORDINATES)
    h = np.sin((lat2 - lat1) / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2
    return 6371 * 2 * np.arcsin(np.sqrt(h))


def inside_box(df: pd.DataFrame) -> pd.Series:
    """Whether both ends of a trip lie in the box around New York City."""
    inside = pd.Series(True, index=df.index)
    for c in COORDINATES:
        inside &= df[c].between(*(LONGITUDE if c.endswith("longitude") else LATITUDE))
    return inside


class NycTaxiTripDuration1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How long will a New York taxi ride take, from pickup to drop-off?",
        use_case=(
            "When a passenger gets in and names the destination, the taxi's system estimates the arrival time with a "
            "model refit every week on the trips before it."
        ),
        row=(
            "One yellow-cab trip in New York City picked up from 21 April to 30 June 2016, from the Taxi and Limousine "
            "Commission's trip records (26,131,305 trips after cleaning; the 379,839 of 23 June, the gap day before "
            "the newest window, are in no split)."
        ),
        predicted="The trip's duration in seconds, on a log scale.",
        known=(
            "The pickup time and point, the drop-off point taken as the destination, the number of passengers, the "
            "rate code (standard, an airport flat fare, out of the city, negotiated or a group ride) and the company "
            "of the cab's meter system."
        ),
        split=(
            "The test windows are three weeks of 2016: the newest (24-30 June), the Memorial Day week (27 May-2 June) "
            "and 10-16 June; a week is the shortest window that holds each weekday once. Training is every trip picked"
            " up at least a day before the window, of which a benchmark fits on a random million; each test window "
            "keeps a random 500,000 of its trips."
        ),
        changes=(
            "We take every TLC trip of the ten weeks before July 2016 instead of the Kaggle competition's sample, "
            "split by week instead of at random, drop a flag set after the trip, non-rides under 30 s, broken clocks "
            "over 3 h, drop-offs within 100 m of the pickup and trips faster than 120 km/h, and blank impossible "
            "passenger counts and an undefined rate code."
        ),
        fit="approximate",
        fit_reason=(
            "Everything the model sees is known at pickup except the destination: the recorded drop-off point stands "
            "in for the one named at pickup, and differs from it when a passenger changes the destination or gets out"
            " early. The rate code, recorded at the end of the trip, follows from the pickup, the destination and a "
            "fare agreed before the ride."
        ),
    )

    # Dataset
    unique_name = "nyc_taxi_trip_duration_1m"
    domain = "industry & manufacturing"  # transport has no value of its own; as for delivery_eta_1m, maps_router_eta_1m
    sources = (
        Source(
            role="publication",
            platform="GOV Website",
            url="https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page",
            license=None,  # the TLC trip records carry no explicit licence (NYC Open Data terms of use)
            year="2016",
            bibtex=r"""
                @misc{nyctlc2016trips,
                  author = {{NYC Taxi and Limousine Commission}},
                  title = {{TLC} Trip Record Data: Yellow Taxi Trip Records, 2016},
                  year = {2016},
                  howpublished = {\url{https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page}}
                }
                @misc{risdal2017nyctaxi,
                  author = {Meg Risdal},
                  title = {New York City Taxi Trip Duration},
                  year = {2017},
                  howpublished = {\url{https://kaggle.com/competitions/nyc-taxi-trip-duration}},
                  note = {Kaggle playground competition on a sample of the 2016 yellow taxi trip records of the NYC Taxi and Limousine Commission}
                }
            """,
        ),
        Source(
            role="copy",
            platform="GOV Website",
            url="https://data.cityofnewyork.us/d/uacg-pexx",
            license=None,
            name="NYC Open Data's 2016 Yellow Taxi Trip Data, which we download",
            files=[f"{OPEN_DATA}/*.csv"],
        ),
    )
    data_tags = ("Spatial",)
    download_description = """
        We download from NYC Open Data's "2016 Yellow Taxi Trip Data" (https://data.cityofnewyork.us/d/uacg-pexx), the
        TLC's 2016 yellow-cab trip records with the pickup and drop-off coordinates (the TLC's own monthly files of
        2016 now carry taxi zones only). One CSV per pickup day from 2016-04-21 to 2016-06-30, ten columns, 4.2 GB,
        through the dataset's query API: about 9 minutes per day, so about 10 hours one day at a time (2 hours with six
        requests at a time, as in a shell loop run with `xargs -P 6`):

        mkdir -p local-data-warehouse/nyc_taxi_trip_duration/open_data
        cd local-data-warehouse/nyc_taxi_trip_duration/open_data
        cols=vendorid,tpep_pickup_datetime,tpep_dropoff_datetime,passenger_count,pickup_longitude,pickup_latitude,dropoff_longitude,dropoff_latitude,ratecodeid,store_and_fwd_flag
        for d in $(seq 0 70); do
          day=$(date -d "2016-04-21 + $d day" +%F)
          curl -sf --retry 3 -o $day.csv "https://data.cityofnewyork.us/resource/uacg-pexx.csv?%24select=$cols&%24where=tpep_pickup_datetime%20between%20%27${day}T00:00:00%27%20and%20%27${day}T23:59:59%27&%24limit=5000000"
        done

        Each file's row count matches the API's count for its day (%24select=count(*) with the same %24where).
    """
    curation_comments = """
        We start with NYC Open Data's "2016 Yellow Taxi Trip Data", the TLC's yellow-cab trip records with coordinates, and take every trip picked up from 2016-04-21 to 2016-06-30: 26,818,607 trips. The task is that of the Kaggle playground competition "New York City Taxi Trip Duration" (2017), whose train.csv is a sample of 1,458,644 of the same records from January to June 2016; until 2026-11-27 we shipped that sample. The open-data release gives every trip of the period, so each of three weekly windows trains on far more than the 1M-row budget, and it adds the rate code, which the Kaggle sample lacks (CC 2026-11-27).

        - Prediction point: when the meter is engaged and the passenger has named the destination, an ETA from the vendor of the cab's meter system, the pickup time and point, the passenger count, the rate code and the dropoff point. The dropoff point is recorded when the meter is disengaged; we take it as the destination named at pickup (Lennart, 2026-09-21), and the data page keeps it on purpose.
        - Target: `log1p_trip_duration`, the trip duration in seconds (dropoff time minus pickup time), log1p-scaled. The competition scored RMSLE on the duration in seconds, which the metric computes after the inverse (`target_transform="log1p"`).
        - The period: 30 June 2016 is the last day of TLC records with coordinates; from July 2016 on they carry taxi zones only. We start on 21 April, the first day that leaves the Memorial Day window half of the trips for training (51.8%; by the API's daily counts, from 22 April 50.4% and from 23 April under half).
        - We download ten columns. The others (trip distance, payment type, the fare and its parts) are set at the end of the trip. We drop dropoff_datetime, which is pickup_datetime plus the target.
        - We drop store_and_fwd_flag: it says whether the trip record "was held in vehicle memory before sending to the vendor" (TLC data dictionary), and the record is sent after the trip, so the flag is not known at the prediction point.
        - We keep ratecodeid as a feature with the names of the TLC data dictionary (a category): 97.4% standard rate, 2.2% JFK, 0.2% Newark, 0.14% negotiated fare, 0.05% Nassau or Westchester, and 55 group rides. The dictionary calls it "the final rate code in effect at the end of the trip"; the codes follow from the pickup, the destination and an agreement before the ride (decision table). The 236 trips with the code 99, which the dictionary does not define, get a missing value.
        - We map vendor_id to the vendor names of the TLC data dictionary (a category); pickup_datetime is a datetime.
        - We drop 11,591 exact copies of a record.
        - We drop trips shorter than 30 s (154,235), which are not rides (most start and end at one point), and trips longer than 3 h (41,787), whose clock is broken (a cluster just below 24 h from VeriFone meters at walking speed; decision table): 0.73% of the trips.
        - We drop 316,554 trips with an end outside the box of longitude -75 to -72 and latitude 40 to 41.5: GPS errors.
        - We drop the 162,491 trips whose drop-off lies within 100 m of the pickup (0.62%; Lennart, CC 2026-10-26, USE-7; the radius of pkdd_15_taxi_trip_time_prediction_ii_1m): nobody names a destination that close to where they are picked up, so these rows lack the input the ETA acts on. 81,620 of them end at the pickup coordinates exactly (decision table).
        - We drop the 644 trips that imply more than 120 km/h in a straight line from pickup to drop-off (up to 2,104 km/h; CC 2026-11-27; the constant of pkdd_15_taxi_trip_time_prediction_ii_1m and 2024_lusaka_mobility_prediction_hackathon). No route is shorter than the straight line and the region's highest speed limit is 65 mph (105 km/h), so each has a broken clock or a broken GPS fix and an impossible target; which of the two is broken cannot be told, so the row goes rather than a value being blanked. The 235 trips between 100 and 120 km/h stay.
        - We set passenger_count to missing where it is 0 (the driver did not enter it) or above the 6 seats of a cab, 303 trips in all, and keep the trips.
        - Split: three weekly test windows, the newest week (24-30 June 2016), the Memorial Day week (27 May-2 June) and 10-16 June (splits_comment; CC 2026-11-10 and 2026-11-27). The competition's test set is a random 30% of every day of its half-year, so its leaderboard measures interpolation within the period.
        - Note: the TLC publishes the records on NYC Open Data without an explicit licence, under the portal's terms of use. The Kaggle sample, whose rules forbid redistribution, is no longer used.
        - The row budget: the frame holds 25,751,466 trips, every trip a split uses (all but the 379,839 of 23 June, the gap day before the newest window). Each test window keeps a random 500,000 of its 2.3M to 2.5M trips, so the container holds 23,784,905 rows. The 1M train budget is recorded, not applied: a benchmark sub-samples each train side (13.3M to 23.3M trips) to 1M before a fit with `subsample_train`, by default a random 1M of the newest year before the window, which here is every earlier trip of the period.
    """
    accepted_check_warnings = {
        "meta_license_unknown": (
            "The TLC trip records carry no explicit licence; NYC Open Data serves them under its terms of use."
        ),
    }

    # Task
    target = "log1p_trip_duration"
    problem_type = "regression"
    metric = Metric.source(
        "rmsle",
        original="RMSLE (Root Mean Squared Logarithmic Error)",
        reference="https://www.kaggle.com/competitions/nyc-taxi-trip-duration/overview/evaluation",
        definition=(
            "sqrt(mean((log(p+1) - log(a+1))^2)) on trip_duration in seconds, computed after the inverse of our "
            "log1p_trip_duration target."
        ),
        target_transform="log1p",
    )

    split_leaf = "L-ORDER.windows"
    # Splits
    temporal = Temporal(
        on="pickup_datetime",
        splits=TemporalSplits(window=7, unit="days", gap=1, cutoffs=("2016-06-24", "2016-05-27", "2016-06-10")),
    )
    splits_comment = """
        The competition gives no horizon: its test set is a random 30% of the same days (curation_comments), so a random split is optimistic here. An ETA service refits often; a week is the shortest window that holds each weekday once, and no source speaks for a calendar month. The trips cover 21 April to 30 June 2016 (CC 2026-11-27): the last day with coordinates, and the first day that leaves the Memorial Day window half of the trips for training. Another year, the winter and the spring weeks chosen before (8-14 April, on the Kaggle sample) cannot be tested. We test three weeks (Friday to Thursday), newest first: 24-30 June, the newest; 27 May to 2 June, the week of Memorial Day (Monday 30 May), the one public holiday of the period (336,662 recorded trips a day against 387,542 and 383,395 in the weeks before and after); and 10-16 June, a week between the two. The features do not drift in any window (largest population stability index 0.006, by the README's window table), so the choice rests on the calendar. The gap of one day is part of the task: a weekly refit is not instantaneous (the week's trips are collected, the model fit, checked and deployed), so the model that serves a week was trained on the trips up to a day before it. The label delay alone needs less: a trip lasts up to 3 hours, and without a gap 4,588, 4,936 and 5,393 train trips would end after the window start, with a gap of 3 hours none. The 379,839 trips of 23 June, the gap day before the newest window, lie in no split, so the frame leaves them out.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return read_open_data(raw_dir)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # exact copies of a record; the times in the TLC's wall-clock format, the duration in seconds
        df = trips(raw)
        # no ride (under 30 s) or a broken clock (over 3 h)
        df = df[df["trip_duration"].between(MIN_SECONDS, MAX_SECONDS)]
        # GPS errors: an end outside the region
        df = df[inside_box(df)]
        # no destination: the drop-off lies within 100 m of the pickup (a named destination is never there)
        df = df[haversine_km(df) >= MIN_STRAIGHT_LINE_KM]
        # an impossible speed: a broken clock or GPS fix (the sibling taxi tasks' 120 km/h in a straight line)
        df = df[haversine_km(df) <= MAX_STRAIGHT_LINE_KMH * df["trip_duration"] / 3600]
        # 0 (not entered) and more than the seats of a cab are not passenger counts
        count = df["passenger_count"]
        df["passenger_count"] = count.astype(float).mask(count.eq(0) | count.gt(PASSENGER_SEATS))
        df["vendor_id"] = df["vendor_id"].map(VENDORS)
        # 99 is not a rate code of the data dictionary
        df["ratecodeid"] = df["ratecodeid"].map(RATE_CODES)
        # the competition scored RMSLE: the metric inverts log1p (target_transform="log1p")
        df[self.target] = np.log1p(df["trip_duration"])
        # the flag is set when the record is sent, after the trip
        return drop_columns(df, ["trip_duration", "store_and_fwd_flag"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["vendor_id", "ratecodeid"], datetime={"pickup_datetime": TIME_FORMAT})

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        base = trips(raw)
        km = haversine_km(base)
        seconds = base["trip_duration"]
        # bands closed on the left; the kept range is MIN_SECONDS <= duration <= MAX_SECONDS
        edges = [-np.inf, 0, 10, MIN_SECONDS, 60, 120, 3600, 2 * 3600, MAX_SECONDS + 1, 22 * 3600, 24 * 3600, np.inf]
        labels = [
            "< 0 s",
            "0-9 s",
            "10-29 s",
            "30-59 s",
            "1-2 min",
            "2 min-1 h",
            "1-2 h",
            "2-3 h",
            "3-22 h",
            "22-24 h",
            ">= 24 h",
        ]
        frame = pd.DataFrame(
            {
                "band": pd.cut(seconds, bins=edges, right=False, labels=labels),
                "km": km,
                "one_point": km < 0.01,
                "kmh": km / (seconds.clip(lower=1) / 3600),
                "verifone": base["vendor_id"].eq(2),
            }
        )
        by_band = frame.groupby("band", observed=False).agg(
            trips=("km", "size"),
            median_km=("km", "median"),
            share_at_one_point=("one_point", "mean"),
            median_kmh=("kmh", "median"),
            share_verifone=("verifone", "mean"),
        )
        by_band["kept"] = ["no", "no", "no", "yes", "yes", "yes", "yes", "yes", "no", "no", "no"]

        kept = seconds.between(MIN_SECONDS, MAX_SECONDS)
        flag = pd.DataFrame(
            {
                "trips": base["store_and_fwd_flag"].value_counts(),
                "of them Creative Mobile Technologies": base.loc[base["vendor_id"].eq(1), "store_and_fwd_flag"]
                .value_counts()
                .reindex(["N", "Y"], fill_value=0),
                "mean log1p duration (30 s to 3 h)": np.log1p(seconds[kept])
                .groupby(base["store_and_fwd_flag"][kept])
                .mean(),
            }
        )

        # the trips of the duration window inside the box, by how far the drop-off lies from the pickup and how fast
        window = base[kept & inside_box(base)]
        wkm = km[window.index]
        kmh = wkm / (window["trip_duration"] / 3600)
        group = np.select(
            [wkm < 0.01, wkm < MIN_STRAIGHT_LINE_KM, kmh > MAX_STRAIGHT_LINE_KMH, kmh > 100],
            ["within 10 m", "10-100 m", "faster than 120 km/h", "100-120 km/h"],
            "100 m or more, up to 100 km/h",
        )
        points = (
            pd.DataFrame(
                {"group": group, "log1p": np.log1p(window["trip_duration"]), "seconds": window["trip_duration"]},
                index=window.index,
            )
            .assign(km=wkm)
            .groupby("group")
            .agg(
                trips=("log1p", "size"),
                mean_log1p_duration=("log1p", "mean"),
                median_seconds=("seconds", "median"),
                median_km=("km", "median"),
            )
            .reindex(
                ["within 10 m", "10-100 m", "faster than 120 km/h", "100-120 km/h", "100 m or more, up to 100 km/h"]
            )
        )

        rates = (
            pd.DataFrame(
                {
                    "rate code": df["ratecodeid"].astype("object").fillna("missing (99)"),
                    "log1p": df[self.target],
                    "km": haversine_km(df),
                }
            )
            .groupby("rate code")
            .agg(trips=("log1p", "size"), mean_log1p_duration=("log1p", "mean"), median_km=("km", "median"))
            .sort_values("trips", ascending=False, kind="stable")
        )
        return [
            Decision(
                "Trips under 30 s or over 3 h are dropped",
                "Below 30 s most records start and end at one point (no ride); above 3 h the clock is broken: a "
                "cluster just below 24 h from VeriFone meters at walking speed. Deduplicated trips:",
                by_band.round(3),
            ),
            Decision(
                "Trips whose drop-off lies within 100 m of the pickup, or faster than 120 km/h, are dropped",
                "The task takes the drop-off point as the destination named at pickup, and nobody names a destination "
                "within 100 m of where they are picked up: these rows lack the input the ETA acts on. A straight line "
                "faster than 120 km/h is a broken clock or GPS fix, so the target is impossible; which of the two is "
                "broken cannot be told, so the row goes. The same constants serve "
                "pkdd_15_taxi_trip_time_prediction_ii_1m. Trips of 30 s to 3 h inside the box:",
                points.round(3),
            ),
            Decision(
                "store_and_fwd_flag is dropped",
                "The flag says whether the trip record was held in the vehicle's memory because there was no "
                "connection to the server when it was sent, which happens at the end of the trip: it is not known "
                "when the ETA is made.",
                flag.round(3),
            ),
            Decision(
                "ratecodeid is kept as a feature",
                "The TLC records the rate code in effect at the end of the trip. The codes other than the standard "
                "rate follow from what is known at pickup: the airport flat fares (JFK, Newark) and the out-of-city "
                "rate (Nassau or Westchester) from the pickup and the destination, a negotiated fare or a group ride "
                "from an agreement before the ride. Kept trips:",
                rates.round(3),
            ),
        ]
