"""Curated dataset definition for `nyc_taxi_trip_duration_1m` (data-foundry v2). Evidence: README.md."""

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

MIN_SECONDS = 30
"""Shorter records are not rides: most start and end at one point (the meter engaged and disengaged in place)."""

MAX_SECONDS = 3 * 3600
"""Longer records have a broken clock: the trips per 20 minutes fall smoothly to 18 at 3 h, then a cluster just
below 24 h follows (VeriFone meters) whose metered fares are those of trips of a few minutes."""

LONGITUDE = (-75.0, -72.0)
LATITUDE = (40.0, 41.5)
"""A box around New York City (Manhattan lies at -74.0, 40.75), reaching about 80 km west, north and south and
170 km east: it keeps the airports, New Jersey, Long Island, Westchester and Connecticut."""

COORDINATES = ["pickup_longitude", "pickup_latitude", "dropoff_longitude", "dropoff_latitude"]

PASSENGER_SEATS = 6
"""A yellow cab seats at most 5 passengers, a minivan cab 6 (the counts 5 and 6 are 99.5% VeriFone meters). A count
of 0 means the driver did not enter it, and 8 or 9 cannot be carried: both are set to missing."""

VENDORS = {1: "Creative Mobile Technologies", 2: "VeriFone"}
"""TLC data dictionary: "1=Creative Mobile Technologies, LLC; 2=VeriFone Inc."."""

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

DST_START = pd.Timestamp("2016-03-13 02:00:00")
"""New York clocks jumped from 02:00 to 03:00 (wall-clock time, as in the trip records)."""


def deduplicated_with_dst_fix(raw: pd.DataFrame) -> pd.DataFrame:
    """The raw trips without exact copies, with the hour skipped at the switch to daylight saving time taken out.

    The times are wall-clock times and trip_duration is dropoff minus pickup, so a trip picked up before 02:00 on
    2016-03-13 and dropped off at 03:00 or later is recorded 3,600 s too long. Used by ``_clean`` and ``_decisions``.
    """
    df = raw[~raw.drop(columns="id").duplicated(keep="first")]
    pickup = pd.to_datetime(df["pickup_datetime"], format=TIME_FORMAT)
    dropoff = pd.to_datetime(df["dropoff_datetime"], format=TIME_FORMAT)
    across_switch = (pickup < DST_START) & (dropoff >= DST_START + pd.Timedelta(hours=1))
    return df.assign(trip_duration=df["trip_duration"] - 3600 * across_switch.astype("int64"))


def same_point(df: pd.DataFrame) -> pd.Series:
    """Whether the recorded pickup and drop-off coordinates are identical (no destination for the ETA)."""
    return df["pickup_longitude"].eq(df["dropoff_longitude"]) & df["pickup_latitude"].eq(df["dropoff_latitude"])


def haversine_km(df: pd.DataFrame) -> pd.Series:
    """The great-circle distance between the pickup and the dropoff point in km (evidence only, not a feature)."""
    lon1, lat1, lon2, lat2 = (np.radians(df[c]) for c in COORDINATES)
    h = np.sin((lat2 - lat1) / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2
    return 6371 * 2 * np.arcsin(np.sqrt(h))


class NycTaxiTripDuration1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How long will a New York taxi ride take, from pickup to drop-off?",
        use_case=(
            "When a passenger gets in and names the destination, the taxi's system estimates the arrival time with a "
            "model refit every week on the trips since January."
        ),
        row=(
            "One yellow-cab trip in New York City, January to June 2016, from a sample of the Taxi and Limousine "
            "Commission's trip records (1,447,167 trips after cleaning, of which the 1,166,477 that a split uses are "
            "kept)."
        ),
        predicted="The trip's duration in seconds, on a log scale.",
        known=(
            "The pickup time and point, the drop-off point taken as the destination, the number of passengers and the"
            " company of the cab's meter system."
        ),
        split=(
            "Each of the last three weeks of June 2016 is a test window; training is a random million trips picked "
            "up at least a day before the window, as for a model refit weekly."
        ),
        changes=(
            "We split by week instead of the competition's random sample of the same days, drop a flag set only after"
            " the trip, non-rides under 30 seconds, broken clocks over 3 hours and trips whose drop-off point equals "
            "the pickup point, blank impossible passenger counts, and correct trips across the daylight-saving switch."
        ),
        fit="approximate",
        fit_reason=(
            "Everything the model sees is known at pickup except the destination: the recorded drop-off point stands "
            "in for the one named at pickup, and differs from it when a passenger changes the destination or gets out"
            " early. The task is framed without a routing estimate."
        ),
    )

    # Dataset
    unique_name = "nyc_taxi_trip_duration_1m"
    version_of = "nyc_taxi_trip_duration"
    version_comment = """
        Every train side holds 1.28M to 1.39M trips, above the 1M-row budget, so the dataset ships only as this version (definitions.md, Lennart 2026-10-21). We sample per test window (v2 split protocol): each window keeps at most 500k of its rows (none reaches it), and its train side is a random 1M of all trips picked up at least a day before the window, drawn in one random order for all windows so the train sides overlap; the frame keeps only the rows a split uses. As in delivery_eta_1m, the sample is random rather than the latest trips, so the train sides cover the whole half-year.
    """
    year = "2016"
    domain = "industry & manufacturing"  # transport has no value of its own; as for delivery_eta_1m, maps_router_eta_1m
    source = "GOV Website"  # the NYC TLC trip records; we download the Kaggle competition's sample of them
    source_url = "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page"
    license = "Kaggle Competition Rules"  # the TLC trip records carry no explicit licence (NYC Open Data terms)
    data_tags = ("Spatial",)
    download_description = """
        We download the training file of the Kaggle competition (its rules must be accepted on the competition page
        first). train.csv holds 1,458,644 trips (sha256 fc8c777a4ab99a362d8b6b6f2038ff8a2c4625b9593248a47352d0d26fa99927),
        a sample of the 2016 yellow-cab trip records that the NYC Taxi and Limousine Commission first published on
        its trip record page (https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page). NYC Open Data still
        serves them with the coordinates as "2016 Yellow Taxi Trip Data" (https://data.cityofnewyork.us/d/uacg-pexx).

        mkdir -p local-data-warehouse/nyc_taxi_trip_duration
        kaggle competitions download -c nyc-taxi-trip-duration -f train.zip -p local-data-warehouse/nyc_taxi_trip_duration
        unzip local-data-warehouse/nyc_taxi_trip_duration/train.zip -d local-data-warehouse/nyc_taxi_trip_duration/
        rm local-data-warehouse/nyc_taxi_trip_duration/train.zip
    """
    bibtex = r"""
        @misc{nyctlc2016trips,
          author = {{NYC Taxi and Limousine Commission}},
          title = {{TLC} Trip Record Data: Yellow Taxi Trip Records, January to June 2016},
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
    """
    curation_comments = """
        We start with train.csv of the Kaggle playground competition "New York City Taxi Trip Duration" (2017): 1,458,644 yellow-cab trips with pickup times from 2016-01-01 to 2016-06-30, sampled from the trip records of the NYC Taxi and Limousine Commission (TLC).

        - Prediction point: when the meter is engaged and the passenger has named the destination, an ETA from the vendor of the cab's meter system, the pickup time and point, the passenger count and the dropoff point. The dropoff point is recorded when the meter is disengaged; we take it as the destination named at pickup (Lennart, 2026-09-21), and the data page keeps it on purpose.
        - Target: `log1p_trip_duration`, the trip duration in seconds, log1p-scaled. The competition scored RMSLE, so RMSE on this target is the competition's metric.
        - We drop id, an identifier, and dropoff_datetime, which equals pickup_datetime plus the target.
        - We drop store_and_fwd_flag: it says whether the trip record "was held in vehicle memory before sending to the vendor" (TLC data dictionary), and the record is sent after the trip, so the flag is not known at the prediction point.
        - We map vendor_id to the vendor names of the TLC data dictionary (a category); pickup_datetime is a datetime.
        - We drop 7 trips that are exact copies of another trip under a second id.
        - We take 3,600 s off the trips picked up before 02:00 on 2016-03-13 and dropped off after the clocks jumped to 03:00. The times are wall-clock times, so these trips were recorded one hour too long (decision table).
        - We drop trips shorter than 30 s, which are not rides (most start and end at one point), and trips longer than 3 h, whose clock is broken (a cluster just below 24 h from VeriFone meters at walking speed; decision table). The two filters remove 0.47% of the trips.
        - We drop 38 trips with an end outside the box of longitude -75 to -72 and latitude 40 to 41.5: GPS errors on trips of a few minutes.
        - We drop 4,539 trips (0.31%, 0.29-0.34% in every month, 73% VeriFone) whose drop-off coordinates equal the pickup coordinates to the last digit: a named destination is never the pickup point, so these rows lack the input the ETA acts on (decision table). Their mean target is 6.04 against 6.47 for the other trips.
        - We set passenger_count to missing where it is 0 (the driver did not enter it) or above the 6 seats of a cab (8 and 9), 23 trips in all, and keep the trips.
        - Anomaly: 1,082 kept trips start and end within 10 m but not at the same coordinates, and 46 imply more than 100 km/h. We keep them, as they cannot be told from real trips with certainty.
        - Split: weekly test windows over the last 3 weeks of June 2016 (splits_comment). The competition's test set is a random 30% of every day of the same half-year, so its leaderboard measures interpolation within the period; we do not use test.csv.
        - Note: pickup_datetime is the only time feature, and the hour matters most. LightGBM (300 trees, learning rate 0.1, 63 leaves, a random 200k of each train side, one fit per window) scores RMSE 0.373, 0.357 and 0.381 on the weekly windows (newest first) when the encoding keeps the hour (skrub's DatetimeEncoder in tabarena_default) and 0.429, 0.414 and 0.441 with AutoGluon's date parts, which lose it.
        - Note: the Kaggle rules (Sec. 7) allow academic research and other non-commercial use and forbid redistribution; the TLC publishes the same records on NYC Open Data without an explicit licence.
    """

    # Task
    target = "log1p_trip_duration"
    problem_type = "regression"

    # Splits
    temporal = Temporal(on="pickup_datetime", splits=TemporalSplits(window=7, unit="days", n_windows=3, gap=1))
    subsample_to_budget = True
    splits_comment = """
        An ETA model refit every week predicts the trips of the next week, as for the other ETA tasks of the collection (delivery_eta_1m, maps_router_eta_1m). We use each of the last 3 weeks of June 2016 as a test window (newest first, 52,779 to 54,532 trips each) and the trips picked up at least one day before it as train data: 3 windows, the 1 x 3 an IID task of this size would get, and every train side holds at least 88% of the trips. The gap of one day is part of the task: a trip lasts up to 3 hours, so at a refit the last trips before it have no duration yet; without the gap 77, 119 and 127 train trips per window would end after the window start. Each train side (1.28M to 1.39M trips before the cap) is a random 1M of the earlier trips, drawn in one random order for all windows so the train sides overlap, and no test window reaches 500k rows; the frame keeps only the trips a split uses (version_comment). The competition's test set is a random sample of the same days (curation_comments); a random split is optimistic here. LightGBM (300 trees, learning rate 0.1, 63 leaves, a random 200k of each train side, one fit per split) scores RMSE 0.357-0.381 on the weekly windows, 0.355-0.364 on 3 folds of whole days and 0.353-0.355 on 3 random folds when the encoding keeps the hour (skrub's DatetimeEncoder), and 0.414-0.441, 0.401-0.410 and 0.390-0.392 with AutoGluon's date parts. Trips of one day sharing traffic and weather explain about 0.01 of the gap; the rest is the distance in time.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "train.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # 7 exact copies of a trip under a second id; 86 kept trips across the daylight-saving switch lose 3,600 s
        df = deduplicated_with_dst_fix(raw)
        # no ride (under 30 s) or a broken clock (over 3 h)
        df = df[df["trip_duration"].between(MIN_SECONDS, MAX_SECONDS)]
        # GPS errors: an end outside the region
        inside = pd.Series(True, index=df.index)
        for c in COORDINATES:
            inside &= df[c].between(*(LONGITUDE if c.endswith("longitude") else LATITUDE))
        df = df[inside]
        # no destination: the drop-off point is the pickup point to the last digit
        df = df[~same_point(df)]
        # 0 (not entered) and more than the seats of a cab (8, 9) are not passenger counts
        count = df["passenger_count"]
        df["passenger_count"] = count.astype(float).mask(count.eq(0) | count.gt(PASSENGER_SEATS))
        df["vendor_id"] = df["vendor_id"].map(VENDORS)
        # the competition scored RMSLE: RMSE on log1p(duration) is that metric
        df[self.target] = np.log1p(df["trip_duration"])
        # dropoff_datetime = pickup_datetime + trip_duration (the target); the flag is set when the record is sent
        return drop_columns(df, ["id", "dropoff_datetime", "trip_duration", "store_and_fwd_flag"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["vendor_id"], datetime={"pickup_datetime": TIME_FORMAT})

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        # the trips the duration filter sees: deduplicated, with the daylight-saving hour taken out
        base = deduplicated_with_dst_fix(raw)
        km = haversine_km(base)
        seconds = base["trip_duration"]
        # bands closed on the left; the kept range is MIN_SECONDS <= duration <= MAX_SECONDS
        edges = [0, 10, MIN_SECONDS, 60, 120, 3600, 2 * 3600, MAX_SECONDS + 1, 22 * 3600, 24 * 3600, np.inf]
        labels = [
            "< 10 s",
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
                "kmh": km / (seconds / 3600),
                "verifone": base["vendor_id"].eq(2),
            }
        )
        by_band = frame.groupby("band", observed=True).agg(
            trips=("km", "size"),
            median_km=("km", "median"),
            share_at_one_point=("one_point", "mean"),
            median_kmh=("kmh", "median"),
            share_verifone=("verifone", "mean"),
        )
        by_band["kept"] = ["no", "no", "yes", "yes", "yes", "yes", "yes", "no", "no", "no"]

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

        # the trips of the duration window by how far the drop-off lies from the pickup
        trips = base[kept]
        distance = np.select(
            [same_point(trips), km[kept] < 0.01], ["same coordinates", "within 10 m, not the same"], "10 m or more"
        )
        points = (
            pd.DataFrame(
                {
                    "distance": distance,
                    "log1p": np.log1p(seconds[kept]),
                    "verifone": trips["vendor_id"].eq(2),
                    "seconds": seconds[kept],
                }
            )
            .groupby("distance")
            .agg(
                trips=("log1p", "size"),
                mean_log1p_duration=("log1p", "mean"),
                median_seconds=("seconds", "median"),
                share_verifone=("verifone", "mean"),
            )
            .reindex(["same coordinates", "within 10 m, not the same", "10 m or more"])
        )

        # trips picked up between 01:00 and 01:59 on the night of the switch and on the Sundays before and after
        pickup = pd.to_datetime(base["pickup_datetime"], format=TIME_FORMAT)
        recorded = (pd.to_datetime(base["dropoff_datetime"], format=TIME_FORMAT) - pickup).dt.total_seconds()
        nights = {}
        for day in ("2016-03-06", "2016-03-13", "2016-03-20"):
            start = pd.Timestamp(f"{day} 01:00:00")
            hour = (pickup >= start) & (pickup < start + pd.Timedelta(hours=1)) & kept
            nights[day] = {
                "trips": int(hour.sum()),
                "recorded at least 60 min": int((recorded[hour] >= 3600).sum()),
                "median recorded (min)": round(recorded[hour].median() / 60, 1),
                "median shipped (min)": round(seconds[hour].median() / 60, 1),
                "75th percentile shipped (min)": round(seconds[hour].quantile(0.75) / 60, 1),
            }
        return [
            Decision(
                "Trips under 30 s or over 3 h are dropped",
                "Below 30 s most records start and end at one point (no ride); above 3 h the clock is broken: a "
                "cluster just below 24 h from VeriFone meters at walking speed, whose TLC records carry the fares of "
                "trips of minutes.",
                by_band.round(3),
            ),
            Decision(
                "Trips whose drop-off coordinates equal the pickup coordinates are dropped",
                "The task takes the drop-off point as the destination named at pickup, and a named destination is "
                "never the pickup point: these rows lack the input the ETA acts on (a failed GPS fix at the drop-off "
                "or a ride that did not happen). Trips that end within 10 m at other coordinates are kept, as they "
                "cannot be told from short real rides. Trips of 30 s to 3 h, before the box filter:",
                points.round(3),
            ),
            Decision(
                "store_and_fwd_flag is dropped",
                "The flag says whether the trip record was held in the vehicle's memory because there was no "
                "connection to the server when it was sent, which happens at the end of the trip: it is not known "
                "when the ETA is made. Only Creative Mobile Technologies meters set it.",
                flag.round(3),
            ),
            Decision(
                "Trips across the switch to daylight saving time lose the skipped hour",
                "The times are wall-clock times, so a trip picked up before 02:00 on 2016-03-13 and dropped off after "
                "the clocks jumped to 03:00 is recorded one hour too long. Pickups between 01:00 and 01:59 (kept "
                "trips) on that night and on the Sundays before and after:",
                pd.DataFrame(nights).T,
            ),
        ]
