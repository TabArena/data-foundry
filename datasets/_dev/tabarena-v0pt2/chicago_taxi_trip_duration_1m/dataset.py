"""Curated dataset definition for `chicago_taxi_trip_duration_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    RowBudget,
    TaskSummary,
    Temporal,
    TemporalSplits,
    anonymize_ids,
    drop_columns,
)

MONTHS = tuple(str(p) for p in pd.period_range("2025-09", "2026-09", freq="M"))
"""The calendar months of trip starts we download: a year of history before the September 2026 test weeks."""

RAW_FILES = tuple(f"taxi_trips_{month}.csv" for month in MONTHS)

TEXT_COLUMNS = (
    "trip_id",
    "taxi_id",
    "trip_start_timestamp",
    "trip_end_timestamp",
    "pickup_census_tract",
    "dropoff_census_tract",
    "payment_type",
    "company",
)
"""Read as text: the ids, the timestamps as published, the 11-digit tract codes (never numbers) and the labels."""

TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

POST_TRIP = ["trip_end_timestamp", "trip_miles", "fare", "tips", "tolls", "extras", "trip_total", "payment_type"]
"""Recorded when the meter stops (LEAK-10): the end time is the start plus the target, the rest are the meter's
distance and the charges and payment of the finished trip."""

TRACTS = ["pickup_census_tract", "dropoff_census_tract"]
"""Hidden by the City depending on the trip's own arrival quarter hour (LEAK-10): dropped, every trip is placed by its
community area."""

MIN_SECONDS = 60
"""Records of a minute or less are not rides: 85% record no mile below 30 s, and the systems that record whole minutes
write a non-ride as 0 s or 60 s (80,861 at 0 s, 95% without a mile, and 26,044 at 60 s, 82%), against 2.3% of the
trips of 5 to 60 minutes; with area centroids no rule on the inputs can remove them instead."""

SHORT_NO_MILE_SECONDS = 120
"""Records under 2 minutes with no mile on the meter that end in their pickup community area are no rides either
(curator issue 1, option A): they pay the flag drop and about a minute and a half of waiting, mostly in cash."""

MAX_SECONDS = 3 * 3600
"""Longer records have a broken clock (a meter left running): from 3 h on the median speed falls below 5 mph, and a
cluster sits at 12 to 24 h; the cut of nyc_taxi_trip_duration_1m and pkdd_15_taxi_trip_time_prediction_ii_1m."""

MAX_STRAIGHT_LINE_KMH = 120
"""Faster in a straight line between the two ends is no real trip (the duration or an end is wrong), the rule of
pkdd_15_taxi_trip_time_prediction_ii_1m and 2024_lusaka_mobility_prediction_hackathon."""

AREA_SLACK_KM = 3.0
"""Slack per end of the straight line: a trip can start or end a few km from its community area's centroid."""

SPRING_FORWARD_SLOT = "2026-03-08T03:00:00.000"
"""The first quarter hour after the clocks went forward on 2026-03-08: the meter of 24 trips that start in it counted
the skipped hour."""

OWNER_OPERATOR = r"^\d+ - \d+ "
"""Company values of an owner-operator: two numbers, then the owner's name or firm ("2733 - 74600 <name>")."""

COMMUNITY_AREAS = {
    1: "Rogers Park",
    2: "West Ridge",
    3: "Uptown",
    4: "Lincoln Square",
    5: "North Center",
    6: "Lake View",
    7: "Lincoln Park",
    8: "Near North Side",
    9: "Edison Park",
    10: "Norwood Park",
    11: "Jefferson Park",
    12: "Forest Glen",
    13: "North Park",
    14: "Albany Park",
    15: "Portage Park",
    16: "Irving Park",
    17: "Dunning",
    18: "Montclare",
    19: "Belmont Cragin",
    20: "Hermosa",
    21: "Avondale",
    22: "Logan Square",
    23: "Humboldt Park",
    24: "West Town",
    25: "Austin",
    26: "West Garfield Park",
    27: "East Garfield Park",
    28: "Near West Side",
    29: "North Lawndale",
    30: "South Lawndale",
    31: "Lower West Side",
    32: "Loop",
    33: "Near South Side",
    34: "Armour Square",
    35: "Douglas",
    36: "Oakland",
    37: "Fuller Park",
    38: "Grand Boulevard",
    39: "Kenwood",
    40: "Washington Park",
    41: "Hyde Park",
    42: "Woodlawn",
    43: "South Shore",
    44: "Chatham",
    45: "Avalon Park",
    46: "South Chicago",
    47: "Burnside",
    48: "Calumet Heights",
    49: "Roseland",
    50: "Pullman",
    51: "South Deering",
    52: "East Side",
    53: "West Pullman",
    54: "Riverdale",
    55: "Hegewisch",
    56: "Garfield Ridge",
    57: "Archer Heights",
    58: "Brighton Park",
    59: "McKinley Park",
    60: "Bridgeport",
    61: "New City",
    62: "West Elsdon",
    63: "Gage Park",
    64: "Clearing",
    65: "West Lawn",
    66: "Chicago Lawn",
    67: "West Englewood",
    68: "Englewood",
    69: "Greater Grand Crossing",
    70: "Ashburn",
    71: "Auburn Gresham",
    72: "Beverly",
    73: "Washington Heights",
    74: "Mount Greenwood",
    75: "Morgan Park",
    76: "O'Hare",
    77: "Edgewater",
}
"""The City's 77 community areas by number ("Boundaries - Community Areas", data.cityofchicago.org/d/igwz-8jzy)."""

OHARE = 76

CUTOFFS = ("2026-09-10", "2026-09-17", "2026-09-24")


def reported_company(company: pd.Series) -> pd.Series:
    """The company as reported, with each owner-operator's name replaced by a stable code (CLEAN-4)."""
    owner = company.str.contains(OWNER_OPERATOR, regex=True, na=False)
    out = company.astype(object)
    out[owner] = "owner-operator " + anonymize_ids(company[owner], length=8)
    return out


def spring_forward_hits(raw: pd.DataFrame) -> pd.Series:
    """The trips whose meter counted the hour skipped at the switch to daylight saving time on 2026-03-08: they start
    in its first quarter hour and their trip_seconds exceed the end minus the start time by more than 3,000 s.
    """
    slot = raw["trip_start_timestamp"].eq(SPRING_FORWARD_SLOT)
    start = pd.to_datetime(raw.loc[slot, "trip_start_timestamp"], format=TIME_FORMAT)
    end = pd.to_datetime(raw.loc[slot, "trip_end_timestamp"], format=TIME_FORMAT)
    over = raw.loc[slot, "trip_seconds"] - (end - start).dt.total_seconds()
    hits = pd.Series(False, index=raw.index)
    hits[over.index[over > 3000]] = True
    assert int(hits.sum()) == 24, int(hits.sum())
    return hits


def spring_forward_fixed(raw: pd.DataFrame) -> pd.DataFrame:
    """The raw trips with the skipped hour taken off the trips whose meter counted it, before any filter (USE-5), as
    nyc_taxi_trip_duration_1m does.
    """
    hits = spring_forward_hits(raw)
    return raw.assign(trip_seconds=raw["trip_seconds"] - 3600 * hits.astype("int64"))


def area_centroids(raw: pd.DataFrame) -> pd.DataFrame:
    """Each community area's centroid: the point the City publishes for a trip whose tract it hides, one per area."""
    sides = []
    for side in ("pickup", "dropoff"):
        hidden = (
            raw[f"{side}_census_tract"].isna()
            & raw[f"{side}_community_area"].notna()
            & raw[f"{side}_centroid_latitude"].notna()
        )
        columns = [f"{side}_community_area", f"{side}_centroid_latitude", f"{side}_centroid_longitude"]
        sides.append(raw.loc[hidden, columns].set_axis(["area", "latitude", "longitude"], axis=1))
    points = pd.concat(sides).drop_duplicates()
    assert points["area"].is_unique, points["area"].value_counts().head()
    assert set(points["area"]) == set(COMMUNITY_AREAS), sorted(set(COMMUNITY_AREAS) - set(points["area"]))
    return points.set_index("area")


def straight_line_km(raw: pd.DataFrame, points: pd.DataFrame) -> pd.Series:
    """The great-circle distance in km between the pickup and the drop-off area centroids (haversine, 6,371 km)."""
    pickup, dropoff = raw["pickup_community_area"], raw["dropoff_community_area"]
    lat1, lat2 = np.radians(pickup.map(points["latitude"])), np.radians(dropoff.map(points["latitude"]))
    dlon = np.radians(dropoff.map(points["longitude"]) - pickup.map(points["longitude"]))
    a = np.sin((lat2 - lat1) / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return 2 * 6371.0 * np.arcsin(np.sqrt(a))


def row_filters(raw: pd.DataFrame, points: pd.DataFrame) -> list[tuple[str, pd.Series]]:
    """The row filters of ``_clean``, in order, on the raw trips with the spring-forward hour taken off: (the reason,
    the mask of the rows kept).
    """
    seconds = raw["trip_seconds"]
    pickup, dropoff = raw["pickup_community_area"], raw["dropoff_community_area"]
    reach_km = MAX_STRAIGHT_LINE_KMH * seconds / 3600 + 2 * AREA_SLACK_KM
    short_no_mile = (
        seconds.between(MIN_SECONDS + 1, SHORT_NO_MILE_SECONDS - 1) & raw["trip_miles"].eq(0) & pickup.eq(dropoff)
    )
    return [
        ("trip_seconds missing", seconds.notna()),
        ("a copy of another trip in every column but trip_id", ~raw.drop(columns="trip_id").duplicated(keep="first")),
        (f"{MIN_SECONDS} s or shorter (not a ride)", ~(seconds <= MIN_SECONDS)),
        (f"longer than {MAX_SECONDS // 3600} h (a broken clock)", ~(seconds > MAX_SECONDS)),
        ("no pickup or no drop-off community area (outside Chicago or not recorded)", pickup.notna() & dropoff.notna()),
        (
            f"faster than {MAX_STRAIGHT_LINE_KMH} km/h in a straight line between the area centroids, with "
            f"{AREA_SLACK_KM:g} km of slack per end",
            ~(straight_line_km(raw, points) > reach_km),
        ),
        (
            f"{MIN_SECONDS + 1} to {SHORT_NO_MILE_SECONDS - 1} s with no mile and the same community area at both ends "
            "(not a ride)",
            ~short_no_mile,
        ),
    ]


class ChicagoTaxiTripDuration1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How long will a Chicago taxi ride take, from pickup to drop-off?",
        use_case=(
            "For example, when a passenger gets in or books a cab and names the destination, the taxi company's "
            "dispatch system estimates the arrival time with a model refit every week on the past year of trips."
        ),
        row=(
            "One taxi trip reported to the City of Chicago with its pickup and its drop-off inside the city, picked "
            "up from September 2025 to September 2026 (6,631,275 trips after cleaning, of which the 1,371,608 that a "
            "split uses are kept)."
        ),
        predicted="The trip's duration in seconds as the meter recorded it, on a log scale.",
        known=(
            "The pickup time to the quarter hour, the pickup and drop-off community area (one of the City's 77, with "
            "its centroid), the taxi and its company."
        ),
        split=(
            "Each of the last three weeks of September 2026 is a test window; training is a random million trips "
            "picked up at least a day before the window, as for a model refit weekly."
        ),
        changes=(
            "We drop the fare, the payment, the distance and the end time, known only after the trip, and the census "
            "tracts, which the City hides depending on when the trip ends. We drop non-rides (a minute or less, or "
            "under 2 minutes with no mile within one area), broken clocks over 3 hours, impossible speeds and trips "
            "that start or end outside Chicago, and fix 24 spring-forward durations."
        ),
        fit="approximate",
        fit_reason=(
            "Everything the model sees is known at pickup except the destination, for which the recorded drop-off "
            "area stands in. Places are coarser than a dispatcher's: times are rounded to 15 minutes, and every trip "
            "is placed by its community area, as the City hides the census tract depending on the arrival time. Only "
            "trips with both ends in Chicago are in (8% of rides leave, 24% of O'Hare pickups)."
        ),
    )

    # Dataset
    unique_name = "chicago_taxi_trip_duration_1m"
    version_of = "chicago_taxi_trip_duration"
    version_comment = """
        Every train side holds 6.24M to 6.49M trips, above the 1M-row budget, so the dataset ships only as this version (definitions.md, Lennart 2026-10-21). We sample per test window (v2 split protocol): each window keeps all of its 118,581 to 126,382 trips (under 500k), and its train side is a random 1M of all trips picked up at least a day before the window, drawn in one random order for all windows so the train sides overlap; the frame keeps only the 1,371,608 rows a split uses. As in nyc_taxi_trip_duration_1m, the sample is random rather than the latest trips, so the train sides cover the whole year: the latest 1M would score 0.002 to 0.005 RMSLE better but lose the season of the year before, and the history is not chosen from the test windows (review panel, 2026-11-09).
    """
    year = "2026"  # the snapshot we pin; the table grows every month (PROV-9), as chicago_traffic_crashes
    domain = "industry & manufacturing"  # transport has no value of its own; as nyc_taxi_trip_duration_1m
    source = "GOV Website"
    source_url = "https://data.cityofchicago.org/Transportation/Taxi-Trips-2024-/ajtu-isnz"
    license = "See Terms of Use (City of Chicago Data Portal)"
    data_tags = ("Spatial",)
    download_description = """
        The City of Chicago's "Taxi Trips (2024-)" table (ajtu-isnz) on its Socrata data portal, read through the SODA
        API without a login on 2026-11-08: one CSV per calendar month of trip start, 2025-09 to 2026-09, with every
        column but the two location points, which repeat the centroid coordinates. The rows of each file equal the
        API's count for its month (`$select=count(*)` with the same `$where`): 623,661, 641,251, 519,892, 552,599,
        462,991, 450,152, 583,469, 604,151, 679,289, 713,394, 663,239, 598,559 and 597,323. A month's stream
        can break off at a line boundary or time out (408), so check each file's rows against the count; when a month
        times out, fetch it in pieces of days and join them under one header (we fetched March 2026 in two halves,
        April 2026 as days 1-15 and four pieces of the rest). The API returns the rows in no fixed
        order, so the bytes of a new download differ; the portal also amends rows and adds a month at a time. The
        bulk export (api/views/ajtu-isnz/rows.csv) is deprecated and stops on 2026-12-22.

        mkdir -p local-data-warehouse/chicago_taxi_trip_duration && cd local-data-warehouse/chicago_taxi_trip_duration
        SEL=trip_id,taxi_id,trip_start_timestamp,trip_end_timestamp,trip_seconds,trip_miles,pickup_census_tract,dropoff_census_tract,pickup_community_area,dropoff_community_area,fare,tips,tolls,extras,trip_total,payment_type,company,pickup_centroid_latitude,pickup_centroid_longitude,dropoff_centroid_latitude,dropoff_centroid_longitude
        for m in 2025-09 2025-10 2025-11 2025-12 2026-01 2026-02 2026-03 2026-04 2026-05 2026-06 2026-07 2026-08 2026-09; do
          end=$(date -d "$m-01 +1 month" +%Y-%m-01)
          curl -s --compressed -G "https://data.cityofchicago.org/resource/ajtu-isnz.csv" \\
            --data-urlencode "\\$select=$SEL" \\
            --data-urlencode "\\$where=trip_start_timestamp >= '$m-01T00:00:00' AND trip_start_timestamp < '${end}T00:00:00'" \\
            --data-urlencode '$limit=10000000' -o "taxi_trips_$m.csv"
        done
    """
    bibtex = r"""
        @misc{chicago_taxi_trips_2024,
          author = {{City of Chicago, Department of Business Affairs and Consumer Protection}},
          title = {Taxi Trips (2024-)},
          year = {2026},
          howpublished = {\url{https://data.cityofchicago.org/Transportation/Taxi-Trips-2024-/ajtu-isnz}}
        }
    """
    curation_comments = """
        We start with the City of Chicago's "Taxi Trips (2024-)" table (ajtu-isnz), downloaded on 2026-11-08 through its API: the 7,689,970 trips picked up from 2025-09-01 to 2026-09-30, one CSV per month.

        - Prediction point: when the passenger is picked up and has named the destination, the taxi's dispatch system estimates the arrival time from the pickup time and area, the drop-off area, the taxi and its company. The drop-off area is recorded when the meter stops; we take it as the destination named at pickup, as nyc_taxi_trip_duration_1m and pkdd_15_taxi_trip_time_prediction_ii_1m do. The City states no use case: it publishes the trips "in its role as a regulatory agency".
        - Target: `log1p_trip_seconds`, log1p of trip_seconds, the meter's duration ("Time of the trip in seconds"). It agrees with the end minus the start time to within the 15-minute rounding on all but 45 of the 7.69M rows (Anomaly below). The metric is RMSLE on the seconds, computed after the inverse (`target_transform="log1p"`).
        - History: a year of trips before the September 2026 test weeks (September 2025 on), so every test week has its season of the year before in training. The 2013-2023 table (wrvz-psew, 211.7M trips) and the 2024 to August 2025 trips of this table are left out: a weekly refit trains on its recent past, and the train sides take a random 1M anyway.
        - We drop the columns known only after the trip (LEAK-10): trip_end_timestamp (the start plus the target), trip_miles (the meter's distance), fare, tips, tolls, extras, trip_total and payment_type. We drop trip_id, an identifier, and the two census tracts (Location below); the two location points of the portal repeat the centroid coordinates and are not downloaded.
        - Rows dropped, in order (decision table): 1,347 without trip_seconds; 2,140 copies of another trip in every column but trip_id (the same taxi, times, duration, distance and fare reported twice); 436,222 records of 60 s or less, which are no rides; 6,355 records over 3 hours, a meter left running (median speed under 5 mph, a cluster at 12 to 24 h); 603,644 trips without a pickup or a drop-off community area; 1,094 trips too fast for the straight line between their areas; and 7,893 records of 61 to 119 s with no mile that end in their pickup area. 6,631,275 trips are left. The 3 h cut is that of nyc_taxi_trip_duration_1m and pkdd_15_taxi_trip_time_prediction_ii_1m; the bullets below give the reasons of the others.
        - The short cut sits at 60 s, not at the siblings' 30 s. 85% of the records under 30 s log no mile, and the systems that record whole minutes write a non-ride as 0 s or 60 s (80,861 records at 0 s, 95% without a mile, and 26,044 at 60 s, 82%). The siblings' 30 s held together with their rule that drops trips ending within 100 m of the start, which removed their non-rides on the inputs; here the places are area centroids and no rule on the inputs can. The cost: in the systems that record seconds the 30 to 59 s band sits on a smooth slope (38-42% without a mile at 55-59 s, 34-36% at 61-64 s), so the cut also drops about 25,600 records of 30 to 60 s that log a mile. The 61 to 119 s band left in weighs far more than its share: in the first draft its 0.6% of the test rows held 10.0-10.7% of the test squared error (review panel, 2026-11-09).
        - We also drop the 7,893 records of 61 to 119 s that log no mile and end in their pickup community area (the curator's issue 1, option A). They pay like a meter switched on and off without a ride: a median fare of $3.56 (the flag drop and about a minute and a half of waiting) against $4.18 for the band's records with a mile to another area, 82% paid in cash against 61%, 9% tipped against 24% (decision table), and 36% of their cabs start again from the same place in the same or the next quarter hour, against 12% (review panel). In the systems that record distance to 0.01 mile, 6,772 records of 61 to 119 s show 0.00 mile against 884 at 0.01 and 571 to 787 at each step up to 0.08, so about 85% of them stand out from the run of small distances. The rule reads the target itself (61 to 119 s) and trip_miles, known only after the trip and no feature, so whether a row stays depends on its own outcome, and its 2-minute bound is a choice: no-mile records that end in their pickup area keep the same signature past 2 minutes (in the systems that record seconds, 9,075 at 121 to 299 s and 7,533 at 5 to 10 minutes, 91-92% paid in cash), and they stay. In the first draft the band's records with no mile held 2.3-2.8% of the test squared error on 0.11-0.14% of the test rows.
        - Trips without a pickup or a drop-off community area leave: the City leaves the area blank "for locations outside Chicago", so these trips lack the origin or the destination the estimate acts on (USE-7). We filter on the area, which the City never hides, not on the centroid: the City publishes a centroid for one tract outside the city (17031770700, by O'Hare) only when it shows the tract, so a centroid filter would keep a trip there only when its tract is shown (Location below). The selection is named in fit_reason: 8.3% of the records of 61 s to 3 h leave, among them 24% of the O'Hare pickups (321,388 of 1,326,053; 71% of the trips without a drop-off area leave O'Hare, a median 12.7 miles, for the suburbs) and 14% of the rides over 45 minutes. Some blanks have a second cause: the 83,405 trips with neither area run a median 4.8 miles, and a few reporting systems leave both blank far more often than the rest (decision table).
        - Location: every trip is placed by its pickup and drop-off community area, one of the City's 77, decoded into the City's names, and by the area's centroid, the point the City itself publishes for a trip whose tract it hides (one point per area, checked). We drop the census tracts and replace the tract centroids by the area's (LEAK-10): the City hides the tract of 51% of the trips, both ends together, and the hiding reads the trip's own arrival quarter hour, the start plus the target. Among shown tracts the drop-off tract is alone in its arrival quarter hour for 1.2% of the trips and in its start quarter hour for 5.4%, while the community areas, which are never hidden, give the same share under both keys (6.68% against 6.75%); within cells of pickup area, drop-off area and start quarter hour, a hidden tract follows the number of other trips that end in the drop-off area in the trip's own arrival quarter hour (coefficient -0.198, SE 0.003) and not in the quarter hours 15 or 30 minutes either side (+0.006 to +0.014). The hidden flag is thus missingness drawn in part by the outcome, and the tract centroids repeat it. LightGBM with community areas only, against the same plus the flag, 5 seeds each on a random 700k of the train side: the flag is worth 0.0034, 0.0039 and 0.0028 RMSLE (newest window first), 3.6 to 6.6 SDs of the paired gain, a gain in all 15 fits. As the hiding is joint, nothing short of placing every trip by its area removes it. It costs the shown tract's real detail, 0.024 to 0.025 RMSLE (one seed, a random 400k: 0.3669, 0.3615 and 0.3658 with the tracts as published, 0.3918, 0.3876 and 0.3934 with the areas only); the task stays well above its dummy (0.76 to 0.79). The City does not publish its rule; a third-party account says a tract is shown when "multiple trips" share it in "the same 15-minute interval" (toddwschneider.com/posts/chicago-taxi-data).
        - Potential leak, kept on purpose (LEAK-9, an evaluation leak): each test week keeps all its trips with the taxi and the quarter-hour start, so a method that reads the other test rows finds the same taxi's next pickup, which bounds this trip's end; 97.8% of the newest week's test trips have one. No deployed model has it at pickup. Read from the test rows, it takes 0.0051 to 0.0056 RMSLE off a LightGBM per window (about 7 times the noise; about 0.009 at most, with test labels), and 0.007 to 0.008 with a full week of chains in training. Training on the later windows' labelled test weeks, which the frame holds for the older splits, gains 0.0055 and 0.0145 on the two older windows. Both are closed by the protocol lines in splits_comment, not in the data: the taxi stays a feature (known at pickup), and blanking it in the test rows alone would make the test unlike the training rows (review panel, 2026-11-09, on the first draft).
        - `taxi_id` stays as a categorical feature, as in pkdd_15_taxi_trip_time_prediction_ii_1m: the cab is known at pickup, and 99.9% of the test trips are by a taxi seen in training. We shorten the City's 128-character hash to a stable 12-character code (`anonymize_ids`). Without it the RMSLE is 0.0018 and 0.0016 worse on the two newest windows and 0.0008 better on the oldest (the first draft, one seed); a few trips have none. Some ids are a reporting id rather than one cab: about 0.7% of the trips start before the same id's previous trip can have ended, mostly in the dispatch systems that record whole minutes (the TAC companies 5.2-7.4% of their trips, Transit Administrative Center 1.8%), and one id records 27 O'Hare pickups in one quarter hour. The feature stays; a model learns what the id carries.
        - `company` stays as reported, 33 values. Two spellings of one firm stay apart: "Taxicab Insurance Agency  LLC" records 94% of durations in whole minutes and "Taxicab Insurance Agency Llc" 1.6%, so they are two reporting systems, and the spelling tells the precision of the target (decision table). Four owner-operators are reported as "<number> - <number> <owner's name>"; we replace each by "owner-operator <code>" (CLEAN-4).
        - `trip_start` is the start time as published, local Chicago time rounded to the quarter hour. The meter times the ride itself, so the clock changes leave the target alone, except for 24 trips at the spring switch (next bullet).
        - Anomaly: 45 raw trips record a trip_seconds that differs from the end minus the start time by more than the rounding allows, all on 2026-03-08, the switch to daylight saving time (decision table). 21 start at 01:15 to 01:45 and end at 03:00: their trip_seconds is right, and only the wall-clock end holds the skipped hour. 24 start at 03:00, and their meter counted the skipped hour (a median 2.8 mph as recorded and 17.9 mph without the hour, where trips of 1 to 4 a.m. in March run at 26 mph): we take 3,600 s off them before the duration filters, as nyc_taxi_trip_duration_1m does; 20 of them are kept, all in training.
        - We drop the 1,094 trips whose area centroids lie farther apart than 120 km/h allows in their duration, with 3 km of slack at each end for the size of an area (a median 163 s, 0.42 meter mile and 23 km between the centroids; 696 have an O'Hare end; 11, 11 and 14 per test week): the duration or an end is wrong. This is the rule of pkdd_15_taxi_trip_time_prediction_ii_1m and 2024_lusaka_mobility_prediction_hackathon, on centroids.
        - The siblings' rule that drops trips ending within 100 m of their start (USE-7, nyc_taxi_trip_duration_1m and pkdd_15_taxi_trip_time_prediction_ii_1m) cannot apply here: area centroids cannot locate a return to the start. 1,115,514 kept trips (16.8%) start and end in the same community area, and 96% of them log a mile (a median 0.89 mile and 6.7 minutes, against 16.2 minutes for the other trips), so they are mostly real short rides and stay, as in sendy_logistics_challenge, whose note says that the 100 m radius "rests on exact coordinates" (decision table). The short ones that log no mile are the rule of the bullet above.
        - Anomaly: in the shipped frame, 2,564 trips share every feature with another trip and differ in duration, and 49 repeat one in every column: trips of one taxi in one quarter hour between the same areas, which the coarse times and areas make look alike. We keep them.
        - Note: the City says that "not all trips are reported but the City believes that most are". Late reports do not thin the newest weeks: the City's later monthly updates added 84, 60 and 94 trips to months already published (at most 0.016% of a month; three archived snapshots of the portal's counts against today's), and in the newest week the companies' shares, the duration's mean, median and 90th percentile lie within the weeks before (leak probe 13, |z| at most 1.4). The test weeks held 4.4% fewer trips than the same dates of 2025 (the first draft).
    """

    # Task
    target = "log1p_trip_seconds"
    problem_type = "regression"
    metric = Metric.from_context(
        "rmsle",
        reason=(
            "On this data the choice of metric decides the ranking: a LightGBM fit on the log and one fit on the "
            "seconds rank in opposite order under RMSLE and under RMSE in seconds in 3 of 3 windows, because trips "
            "over an hour (3.8-4.8% of the test trips) hold 38-45% of the squared error in seconds; RMSE would rank "
            "models by those few long trips (review panel, 2026-11-09, on the first draft). RMSLE scores an "
            "estimate's error relative to the trip's length, as the actor judges an arrival estimate (five minutes "
            "off on a ten-minute ride is worse than on an hour's). The City publishes a register of trips, with no "
            "task and no metric (the portal page and its metadata, read 2026-11-08); the competitions of the same "
            "task, nyc_taxi_trip_duration_1m (Kaggle 2017) and pkdd_15_taxi_trip_time_prediction_ii_1m (ECML/PKDD "
            "2015), both scored RMSLE on the duration in seconds."
        ),
        target_transform="log1p",
    )

    # Splits
    temporal = Temporal(
        on="trip_start",
        splits=TemporalSplits(window=7, unit="days", cutoffs=CUTOFFS, gap=1),
    )
    row_budget = RowBudget(train=1_000_000, test=500_000)
    splits_comment = """
        An arrival-time model refit every week predicts the trips of the next week, as for nyc_taxi_trip_duration_1m and the other ETA tasks of the collection. We use each of the last 3 weeks of September 2026 as a test window (newest first, 118,581, 123,718 and 126,382 trips; the table ends with the trips picked up on 2026-09-30) and the trips picked up at least one day before it as train data: 3 windows, the 1 x 3 an IID task of this size would get, and every train side holds at least 94% of the trips. The gap of one day is part of the task: a trip lasts up to 3 hours, so at a refit the last trips before it have no duration yet; without the gap 42, 41 and 30 train trips per window (oldest first) would end after the window starts. The history starts on 2025-09-01, so each test week has the same weeks of 2025 in training (SPLIT-20). Each train side (6.24M to 6.49M trips before the cap) is a random 1M of the earlier trips, drawn in one random order for all windows so the train sides overlap (version_comment).

        Protocol (LEAK-9): each test trip is predicted from the training rows and its own features only; no feature or model step may use other test rows, and a method that does is called out and not benchmarked (the same taxi's next pickup among the test rows bounds a trip's end; curation_comments). A model sees only its split's rows: the frame holds the later windows' labelled test weeks, which an older split must not train on.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        import pyarrow as pa
        import pyarrow.csv as pacsv

        options = pacsv.ConvertOptions(strings_can_be_null=True, column_types={c: pa.string() for c in TEXT_COLUMNS})
        tables = [pacsv.read_csv(raw_dir / name, convert_options=options) for name in RAW_FILES]
        return pa.concat_tables(tables).to_pandas()

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # the skipped hour off the spring-forward trips, before the filters
        raw = spring_forward_fixed(raw)
        points = area_centroids(raw)
        # the filters in order: no duration, copies, non-rides, broken clocks, outside Chicago, too fast, non-rides
        keep = np.logical_and.reduce([mask.to_numpy() for _, mask in row_filters(raw, points)])
        df = raw[keep]
        # every community-area code is one of the City's 77
        for side in ("pickup", "dropoff"):
            assert df[f"{side}_community_area"].isin(list(COMMUNITY_AREAS)).all(), side
        # every trip is placed by its community area: the area's centroid replaces the tract's (LEAK-10)
        centroids = {
            f"{side}_centroid_{axis}": df[f"{side}_community_area"].map(points[axis])
            for side in ("pickup", "dropoff")
            for axis in ("latitude", "longitude")
        }
        df = df.assign(
            trip_start=pd.to_datetime(df["trip_start_timestamp"], format=TIME_FORMAT),
            **centroids,
            pickup_community_area=df["pickup_community_area"].map(COMMUNITY_AREAS),
            dropoff_community_area=df["dropoff_community_area"].map(COMMUNITY_AREAS),
            company=reported_company(df["company"]),  # owner-operators are reported under their name
            taxi_id=anonymize_ids(df["taxi_id"]),
            log1p_trip_seconds=np.log1p(df["trip_seconds"]),
        )
        return drop_columns(df, ["trip_id", "trip_start_timestamp", "trip_seconds", *TRACTS, *POST_TRIP])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["taxi_id", "company", "pickup_community_area", "dropoff_community_area"],
            datetime=["trip_start"],
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        del df
        published = raw["trip_seconds"]
        hits = spring_forward_hits(raw)
        raw = spring_forward_fixed(raw)
        points = area_centroids(raw)
        masks = [(reason, keep.to_numpy()) for reason, keep in row_filters(raw, points)]
        seconds, miles = raw["trip_seconds"], raw["trip_miles"]
        pickup, dropoff = raw["pickup_community_area"], raw["dropoff_community_area"]
        same_area = pickup.eq(dropoff)

        # The rows each filter drops, in order.
        left = np.ones(len(raw), dtype=bool)
        steps, before = [], []
        for reason, keep in masks:
            before.append(left)
            kept = left & keep
            steps.append({"rows dropped": reason, "dropped": int(left.sum() - kept.sum()), "left": int(kept.sum())})
            left = kept
        filters = pd.DataFrame(steps)
        final = left

        # The records by duration band (with a duration, no copies): no mile recorded, the same community area at
        # both ends, the meter's median distance and speed.
        base_mask = masks[0][1] & masks[1][1]
        base = raw[base_mask]
        bs = base["trip_seconds"]
        edges = [0, 30, 60, 61, 90, 120, 300, 3600, 2 * 3600, MAX_SECONDS + 1, 6 * 3600, 12 * 3600, 24 * 3600 + 1]
        labels = ["0-29 s", "30-59 s", "60 s", "61-89 s", "90-119 s", "2-5 min", "5-60 min", "1-2 h", "2-3 h"]
        labels += ["3-6 h", "6-12 h", "12-24 h"]
        band = pd.cut(bs, bins=edges, right=False, labels=labels)
        by_band = pd.DataFrame(
            {
                "trips": band.value_counts(sort=False),
                "share_no_mile": base["trip_miles"].eq(0).groupby(band, observed=False).mean(),
                "share_same_area": same_area[base_mask].groupby(band, observed=False).mean(),
                "median_miles": base["trip_miles"].groupby(band, observed=False).median(),
                "median_mph": (base["trip_miles"] / (bs / 3600)).groupby(band, observed=False).median(),
            }
        )
        by_band["kept"] = ["no", "no", "no", "partly", "partly", "yes", "yes", "yes", "yes", "no", "no", "no"]
        at_zero = base[bs.eq(0)]
        whole = bs.gt(0) & bs.mod(60).eq(0)
        systems = reported_company(base["company"])
        whole_systems = whole.groupby(systems).transform("mean").gt(0.5)
        at_60 = base[bs.eq(60) & whole_systems]
        zero_sentence = (
            f"The systems that record whole minutes write {int(whole_systems[bs.eq(0)].sum()):,} records at 0 s "
            f"({at_zero['trip_miles'][whole_systems[bs.eq(0)]].eq(0).mean():.0%} without a mile) and "
            f"{len(at_60):,} at 60 s ({at_60['trip_miles'].eq(0).mean():.0%} without a mile)."
        )

        # Durations in whole minutes by company: the reporting systems differ in precision.
        precision = (
            pd.DataFrame({"company": systems, "whole": whole})
            .groupby("company")["whole"]
            .agg(trips="size", share_whole_minutes="mean")
            .sort_values("trips", ascending=False, kind="stable")
            .head(16)
        )

        # Trips without a pickup or a drop-off community area (after the duration filters).
        rides_mask = before[4]
        rides = raw[rides_mask]
        has_pickup, has_dropoff = rides["pickup_community_area"].notna(), rides["dropoff_community_area"].notna()
        where = pd.Series(
            np.select(
                [has_pickup & has_dropoff, has_pickup & ~has_dropoff, ~has_pickup & has_dropoff],
                ["both", "no drop-off", "no pickup"],
                "neither",
            ),
            index=rides.index,
        )
        locations = (
            pd.DataFrame(
                {
                    "where": where,
                    "miles": rides["trip_miles"],
                    "minutes": rides["trip_seconds"] / 60,
                    "from_ohare": rides["pickup_community_area"].eq(OHARE),
                    "tract_7707": rides["dropoff_census_tract"].eq("17031770700")
                    | rides["pickup_census_tract"].eq("17031770700"),
                }
            )
            .groupby("where")
            .agg(
                trips=("miles", "size"),
                median_miles=("miles", "median"),
                median_minutes=("minutes", "median"),
                share_from_ohare=("from_ohare", "mean"),
                share_tract_by_ohare_outside=("tract_7707", "mean"),
            )
            .reindex(["both", "no drop-off", "no pickup", "neither"])
        )
        locations["kept"] = ["yes", "no", "no", "no"]
        neither = where.eq("neither").groupby(reported_company(rides["company"])).agg(["size", "mean"])
        neither = neither[neither["size"] >= 50_000].sort_values("mean", ascending=False, kind="stable").head(4)
        neither_sentence = "; ".join(f'"{c}" {s:.1%}' for c, s in neither["mean"].items())
        ohare = rides["pickup_community_area"].eq(OHARE)
        long_rides = rides["trip_seconds"].gt(45 * 60)
        selection = (
            f"Of the records of 61 s to 3 h, {(where != 'both').mean():.1%} leave: {(where[ohare] != 'both').mean():.1%}"
            f" of the {int(ohare.sum()):,} O'Hare pickups and {(where[long_rides] != 'both').mean():.1%} of the rides "
            f"over 45 minutes. The share of each large reporting system's rides with neither area: {neither_sentence}."
        )

        # The hidden tract: its share by pickup hour, and the duration of hidden against shown trips that share the
        # community-area pair and the 15-minute start (trips kept by the filters, before the tracts are dropped).
        kept = raw[final]
        hidden = kept["pickup_census_tract"].isna()
        hour = pd.to_datetime(kept["trip_start_timestamp"], format=TIME_FORMAT).dt.hour
        cell = [kept["pickup_community_area"], kept["dropoff_community_area"], kept["trip_start_timestamp"]]
        log_seconds = np.log1p(kept["trip_seconds"])
        deviation = log_seconds - log_seconds.groupby(cell).transform("mean")
        mixed = hidden.groupby(cell).transform("mean").between(0, 1, inclusive="neither")
        hidden_by_hour = (
            pd.DataFrame({"hour": hour, "hidden": hidden})
            .groupby("hour")["hidden"]
            .agg(trips="size", share_tract_hidden="mean")
        )
        within = (
            f"In the {int(mixed.sum()):,} kept trips whose community-area pair and quarter hour hold both, the log1p "
            f"duration lies {deviation[mixed & hidden].mean():+.3f} from the pair's mean where the tract is hidden "
            f"and {deviation[mixed & ~hidden].mean():+.3f} where it is shown; {hidden.mean():.1%} of the kept trips "
            "have their tract hidden."
        )

        # The trips whose trip_seconds disagrees with the end minus the start time beyond the rounding.
        span = pd.to_datetime(raw["trip_end_timestamp"], format=TIME_FORMAT) - pd.to_datetime(
            raw["trip_start_timestamp"], format=TIME_FORMAT
        )
        odd_rows = raw.index[(published - span.dt.total_seconds()).abs().gt(900)]
        odd = raw.loc[odd_rows]
        odd_start = pd.to_datetime(odd["trip_start_timestamp"], format=TIME_FORMAT)
        odd_span = (pd.to_datetime(odd["trip_end_timestamp"], format=TIME_FORMAT) - odd_start).dt.total_seconds()
        dst = (
            pd.DataFrame(
                {
                    "group": np.where(
                        hits[odd_rows],
                        "start 03:00, the meter counted the skipped hour (3,600 s taken off)",
                        "start 01:15 to 01:45, end 03:00 (only the end time holds the skipped hour)",
                    ),
                    "day": odd_start.dt.date.astype(str),
                    "published_seconds": published[odd_rows],
                    "end_minus_start": odd_span,
                    "mph_published": odd["trip_miles"] / (published[odd_rows] / 3600),
                    "mph_target": odd["trip_miles"] / (odd["trip_seconds"] / 3600),
                    "kept": final[raw.index.get_indexer(odd_rows)],
                }
            )
            .groupby(["group", "day"])
            .agg(
                trips=("kept", "size"),
                kept=("kept", "sum"),
                median_published_seconds=("published_seconds", "median"),
                median_end_minus_start=("end_minus_start", "median"),
                median_mph_published=("mph_published", "median"),
                median_mph_target=("mph_target", "median"),
            )
        )

        # The trips too fast for the straight line between their area centroids.
        fast_mask = before[5] & ~masks[5][1]
        fast = raw[fast_mask]
        fast_start = pd.to_datetime(fast["trip_start_timestamp"], format=TIME_FORMAT)
        per_week = ", ".join(
            str(int(fast_start.between(c, c + pd.Timedelta(days=7), inclusive="left").sum()))
            for c in pd.to_datetime(list(CUTOFFS))
        )
        speed = (
            pd.DataFrame(
                {
                    "end": np.where(
                        fast["pickup_community_area"].eq(OHARE) | fast["dropoff_community_area"].eq(OHARE),
                        "an end at O'Hare",
                        "no end at O'Hare",
                    ),
                    "seconds": fast["trip_seconds"],
                    "miles": fast["trip_miles"],
                    "km": straight_line_km(fast, points),
                }
            )
            .groupby("end")
            .agg(
                trips=("seconds", "size"),
                median_seconds=("seconds", "median"),
                median_meter_miles=("miles", "median"),
                median_centroid_km=("km", "median"),
            )
        )

        # The kept trips that start and end in the same community area (the siblings' 100 m rule).
        same_kept = same_area[final]
        same = (
            pd.DataFrame(
                {
                    "ends": np.where(same_kept, "the same community area", "two community areas"),
                    "mile": kept["trip_miles"].gt(0),
                    "miles": kept["trip_miles"],
                    "minutes": kept["trip_seconds"] / 60,
                }
            )
            .groupby("ends")
            .agg(
                trips=("mile", "size"),
                share_with_a_mile=("mile", "mean"),
                median_miles=("miles", "median"),
                median_minutes=("minutes", "median"),
            )
        )
        same["share_of_trips"] = same["trips"] / same["trips"].sum()

        # The 61-119 s band before the short no-mile rule: what the records paid.
        short_mask = before[6] & seconds.between(MIN_SECONDS + 1, SHORT_NO_MILE_SECONDS - 1).to_numpy()
        ride_mask = before[6] & seconds.between(SHORT_NO_MILE_SECONDS, 299).to_numpy() & miles.gt(0).to_numpy()
        pay = raw[short_mask | ride_mask]
        group = np.select(
            [
                pay["trip_seconds"].ge(SHORT_NO_MILE_SECONDS),
                pay["trip_miles"].eq(0) & same_area[pay.index],
                pay["trip_miles"].eq(0),
                same_area[pay.index],
            ],
            [
                "2-5 min with a mile (reference)",
                "61-119 s, no mile, the same area (dropped)",
                "61-119 s, no mile, another area",
                "61-119 s, a mile, the same area",
            ],
            "61-119 s, a mile, another area",
        )
        short = (
            pd.DataFrame(
                {
                    "records": group,
                    "fare": pay["fare"],
                    "cash": pay["payment_type"].eq("Cash"),
                    "tipped": pay["tips"].fillna(0).gt(0),
                }
            )
            .groupby("records")
            .agg(
                trips=("fare", "size"),
                median_fare=("fare", "median"),
                share_cash=("cash", "mean"),
                share_tipped=("tipped", "mean"),
            )
        )

        return [
            Decision(
                "Rows dropped before the split",
                "The skipped hour is taken off the 24 spring-forward trips first; then trips without a duration, "
                "copies of another trip, records that are no ride, broken clocks, trips without a pickup or a drop-off "
                "community area, trips too fast for the straight line and short records with no mile within one area "
                "go, in this order.",
                filters,
            ),
            Decision(
                "Records of a minute or less and over 3 hours are dropped",
                "Below a minute most records have no mile on the meter and the same area at both ends (the meter "
                f"switched on and off). {zero_sentence} No rule on the inputs can remove the non-rides here (the places "
                "are area centroids), so the cut sits at 60 s rather than the siblings' 30 s. From 3 hours on the "
                "median speed falls below 5 mph and a cluster sits at 12 to 24 hours: a meter left running. Trips "
                "with a duration, without copies, after the spring-forward fix:",
                by_band.round(3),
            ),
            Decision(
                "Records of 61 to 119 s with no mile that end in their pickup area are dropped (curator issue 1)",
                "Records of 61 to 119 s that log no mile and end in their pickup community area pay like a meter "
                "switched on and off: a fare near the flag drop, mostly cash, seldom a tip, unlike the rides of the "
                "same band that log a mile. The rule reads the target's band and the meter's distance (no feature), "
                "so it is not label-free. Trips kept by the earlier filters:",
                short.round(3),
            ),
            Decision(
                "The company is kept as reported, and two spellings stay two values",
                "Some reporting systems write the duration in whole minutes and the others in seconds; the two "
                "spellings of Taxicab Insurance Agency are one of each, so the spelling tells the precision of the "
                "target and we do not merge them. The 16 largest companies (owner-operators named by a code):",
                precision.round(3),
            ),
            Decision(
                "Trips without a pickup or a drop-off community area are dropped",
                "The City leaves the area blank for locations outside Chicago, so these trips have no origin or no "
                "destination for the estimate (USE-7); most trips without a drop-off area leave O'Hare for the "
                "suburbs. The filter reads the area, never hidden, not the centroid, which exists outside the city "
                f"only for tract 17031770700 by O'Hare and only when it is shown. {selection} Records of 61 s to 3 h:",
                locations.round(3),
            ),
            Decision(
                "Every trip is placed by its community area; the census tracts are dropped",
                "The City hides the census tract, both ends together, more often when few other trips end in the "
                "drop-off area in the trip's own arrival quarter hour, the start plus the target: the hidden flag and "
                "the tract centroids that repeat it read the outcome (curation_comments). The area and its centroid, "
                f"which the City shows for every trip in Chicago, replace them. {within} Kept trips by pickup hour:",
                hidden_by_hour.round(3),
            ),
            Decision(
                "The spring-forward trips lose the skipped hour",
                "Every trip whose trip_seconds disagrees with the end minus the start time by more than the 15-minute "
                "rounding (900 s) falls on the night the clocks went forward. Where the start is 03:00, the meter "
                "counted the skipped hour (a speed far below the night's), and 3,600 s come off before the filters, "
                "as in nyc_taxi_trip_duration_1m:",
                dst.round(1),
            ),
            Decision(
                f"Trips faster than {MAX_STRAIGHT_LINE_KMH} km/h in a straight line are dropped",
                f"The straight line between the two area centroids, less {AREA_SLACK_KM:g} km at each end for the size "
                f"of an area, needs more than {MAX_STRAIGHT_LINE_KMH} km/h in the recorded duration: the duration or "
                f"an end is wrong, as in pkdd_15_taxi_trip_time_prediction_ii_1m. Per test week: {per_week}. "
                "Trips dropped:",
                speed.round(2),
            ),
            Decision(
                "Trips within one community area stay: the siblings' 100 m rule cannot apply",
                "nyc_taxi_trip_duration_1m and pkdd_15_taxi_trip_time_prediction_ii_1m drop trips that end within "
                "100 m of their start; area centroids cannot locate a return to the start, and the trips within one "
                "area are mostly short rides that moved (as sendy_logistics_challenge, whose 100 m radius rests on "
                "exact coordinates). Kept trips:",
                same.round(3),
            ),
        ]
