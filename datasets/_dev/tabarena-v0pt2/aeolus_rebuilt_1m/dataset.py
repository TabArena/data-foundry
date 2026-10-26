"""Curated dataset definition for `aeolus_rebuilt_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import io
import sqlite3
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import polars as pl
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    TaskSummary,
    Temporal,
    TemporalSplits,
)

HISTORY_START = "2023-01-01"
"""First flight date kept as a row, as in aeolus_1m: two seasonal cycles before the test windows, after COVID-19. The
December 2022 file is read only for the aircraft's previous flight on the first days of 2023."""

DELAY_THRESHOLD_MINUTES = 15
"""US DOT: a flight is on time when it arrives less than 15 minutes after its scheduled arrival (BTS `ArrDel15`)."""

MIN_SCHEDULED_MINUTES = 15
"""Scheduled block times below 15 minutes are errors (as in aeolus_1m); the shortest real hop is 18 minutes."""

MIN_TEMPERATURE_C = -50
"""Temperatures below -50 C are errors (as in aeolus_1m): Meteostat holds -60.6 C at Sarasota in May 2024."""

MAX_WIND_KMH = 120
"""Mean wind speeds above 120 km/h are sensor errors (as in aeolus_1m): 45 readings of up to 232 km/h, most in clear or
fair weather at ACY, HOU, FSM, BTV, EYW and ATW."""

STATION_RADIUS_KM = 15.0
"""No airport may get a weather station farther away than this (the farthest nearest station is 10.6 km away)."""

OBSERVATION_PROVIDERS = ("isd_lite", "metar")
"""Meteostat inventory providers of hourly observations: a station qualifies when one of them records its
temperature from before 2023 to after 2024."""

N_BTS_FILES = 25
"""The monthly BTS files read: December 2022 to December 2024."""

BTS_COLUMNS = {
    "FlightDate": pl.String,
    "Reporting_Airline": pl.String,
    "Tail_Number": pl.String,
    "Flight_Number_Reporting_Airline": pl.Int64,
    "OriginAirportSeqID": pl.Int64,
    "Origin": pl.String,
    "DestAirportSeqID": pl.Int64,
    "Dest": pl.String,
    "CRSDepTime": pl.Int64,
    "DepDelay": pl.Float64,
    "CRSArrTime": pl.Int64,
    "ArrDelay": pl.Float64,
    "Cancelled": pl.Float64,
    "Diverted": pl.Float64,
    "DivReachedDest": pl.Float64,
    "DivArrDelay": pl.Float64,
    "CRSElapsedTime": pl.Float64,
    "Distance": pl.Float64,
}
"""The columns of the BTS monthly files that are read. The others are recorded at or after the departure (actual
clock times, taxi and air times, delay causes, gate returns, the details of a diversion), copies of these (state, city,
market, time blocks, distance and delay groups, ArrDel15 equals ArrDelay >= 15 on every operated flight) or constant
(Flights)."""

WEATHER = {
    "temp": "TEMP",
    "rhum": "RHUM",
    "prcp": "PRCP",
    "wdir": "WDIR",
    "wspd": "WSPD",
    "pres": "PRES",
    "cldc": "CLDC",
    "coco": "COCO",
}
"""Meteostat's hourly parameters kept, with their column suffix: temperature (C), relative humidity (%), precipitation
in the hour (mm), wind direction (degrees), mean wind speed (km/h), sea-level pressure (hPa), cloud cover (oktas) and
the weather condition code. Peak gust and snow depth are empty in every file read."""

WEATHER_CONDITIONS = {
    1: "clear",
    2: "fair",
    3: "cloudy",
    4: "overcast",
    5: "fog",
    6: "freezing fog",
    7: "light rain",
    8: "rain",
    9: "heavy rain",
    10: "freezing rain",
    11: "heavy freezing rain",
    12: "sleet",
    13: "heavy sleet",
    14: "light snowfall",
    15: "snowfall",
    16: "heavy snowfall",
    17: "rain shower",
    18: "heavy rain shower",
    19: "sleet shower",
    20: "heavy sleet shower",
    21: "snow shower",
    22: "heavy snow shower",
    23: "lightning",
    24: "hail",
    25: "thunderstorm",
    26: "heavy thunderstorm",
    27: "storm",
}
"""Meteostat's weather condition codes (https://dev.meteostat.net/formats)."""

INBOUND_STATES = ("none", "not departed", "in the air", "arrived")
"""Where the aircraft's previous scheduled flight stands at the prediction point; `none` when that flight did not end
at this flight's origin (or the aircraft has no earlier flight in the files)."""

TEST_WINDOWS = (("2024-12-18", "2024-12-31"), ("2024-12-04", "2024-12-17"), ("2024-11-20", "2024-12-03"))
"""The three test windows the splits make (newest first), for the evidence tables."""


def _hhmm_minutes(col: str) -> pl.Expr:
    """BTS clock times hhmm (1 to 2400) as minutes after midnight (2400 is 1440, the end of the day)."""
    return (pl.col(col) // 100) * 60 + pl.col(col) % 100


def _local_to_utc(df: pl.DataFrame, local: str, zone: str, out: str) -> pl.DataFrame:
    """Convert the naive local datetimes in `local`, in the IANA time zone named per row in `zone`, to naive UTC.

    A clock time repeated when daylight saving time ends is read as the first one; one skipped when it starts becomes
    missing.
    """
    parts = []
    for name in sorted(df[zone].unique().to_list()):
        parts.append(
            df.filter(pl.col(zone) == name).with_columns(
                pl.col(local)
                .dt.replace_time_zone(name, ambiguous="earliest", non_existent="null")
                .dt.convert_time_zone("UTC")
                .dt.replace_time_zone(None)
                .alias(out)
            )
        )
    return pl.concat(parts)


def _haversine_km(lat: np.ndarray, lon: np.ndarray, lat0: float, lon0: float) -> np.ndarray:
    """Great-circle distances in km from (lat0, lon0) to each (lat, lon), all in degrees."""
    la, lo, la0, lo0 = np.radians(lat), np.radians(lon), np.radians(lat0), np.radians(lon0)
    h = np.sin((la - la0) / 2) ** 2 + np.cos(la0) * np.cos(la) * np.sin((lo - lo0) / 2) ** 2
    return 2 * 6371.0 * np.arcsin(np.sqrt(h))


def _airport_stations(flights: pl.DataFrame, coordinates: pl.DataFrame, stations: pl.DataFrame) -> pl.DataFrame:
    """Each airport's nearest qualifying weather station, its distance in km and its time zone.

    The airport's position is the BTS master coordinate of the newest airport sequence id its flights use; a station's
    is its NOAA ISD position where it has an ISD id, else Meteostat's.
    """
    used = pl.concat(
        [
            flights.select(pl.col("Origin").alias("code"), pl.col("OriginAirportSeqID").alias("seq"), "FlightDate"),
            flights.select(pl.col("Dest").alias("code"), pl.col("DestAirportSeqID").alias("seq"), "FlightDate"),
        ]
    )
    newest = used.sort(["code", "FlightDate", "seq"]).group_by("code", maintain_order=True).last()
    airports = newest.join(coordinates, on="seq", how="left").sort("code")
    assert airports["lat"].null_count() == 0, "an airport sequence id has no BTS master coordinate"
    candidates = stations.filter(pl.col("qualifies"))
    lat, lon = candidates["lat"].to_numpy(), candidates["lon"].to_numpy()
    rows = []
    for code, a_lat, a_lon in airports.select("code", "lat", "lon").iter_rows():
        km = _haversine_km(lat, lon, a_lat, a_lon)
        i = int(np.argmin(km))
        rows.append({"code": code, "station": candidates["id"][i], "km": round(float(km[i]), 2)})
    mapping = pl.DataFrame(rows).join(
        candidates.select("id", "timezone", "name", "icao", "position"), left_on="station", right_on="id", how="left"
    )
    assert mapping["km"].max() <= STATION_RADIUS_KM, mapping.filter(pl.col("km") > STATION_RADIUS_KM)
    return mapping.sort("code")


def _markdown_table(table: pd.DataFrame) -> str:
    """A small pandas table as GitHub markdown (for decision evidence that needs a collapsed block)."""
    lines = ["| " + " | ".join(map(str, table.columns)) + " |", "|" + "---|" * len(table.columns)]
    lines += [
        "| " + " | ".join("" if pd.isna(v) else str(v) for v in row) + " |" for row in table.itertuples(index=False)
    ]
    return "\n".join(lines)


def _flights_utc(raw: dict[str, pl.DataFrame]) -> tuple[pl.DataFrame, pl.DataFrame]:
    """Every flight of the files (December 2022 on, cancelled and diverted ones included) with its scheduled and
    actual times in UTC, the prediction point, its airports' weather stations and its aircraft's previous flight.
    Returns the flights and the airport-to-station mapping.
    """
    flights = raw["flights"].with_columns(pl.col("Tail_Number").replace("", None))
    mapping = _airport_stations(flights, raw["coordinates"], raw["stations"])
    zones = mapping.select("code", "station", "timezone")
    f = flights.join(
        zones.rename({"code": "Origin", "station": "o_station", "timezone": "o_tz"}),
        on="Origin",
        how="left",
        maintain_order="left",
    ).join(
        zones.rename({"code": "Dest", "station": "d_station", "timezone": "d_tz"}),
        on="Dest",
        how="left",
        maintain_order="left",
    )
    assert f["o_tz"].null_count() == 0, "an origin airport has no weather station"
    assert f["d_tz"].null_count() == 0, "a destination airport has no weather station"
    day = pl.col("FlightDate").cast(pl.Datetime("us"))
    f = f.with_columns(
        (day + pl.duration(minutes=_hhmm_minutes("CRSDepTime"))).alias("dep_local"),
        (day + pl.duration(minutes=_hhmm_minutes("CRSArrTime"))).alias("arr_local"),
    )
    f = _local_to_utc(f, "dep_local", "o_tz", "dep_utc")
    f = _local_to_utc(f, "arr_local", "d_tz", "arr_clock_utc")
    # The scheduled arrival: departure plus BTS's scheduled block time; where that is missing or impossible, the
    # local arrival clock time on the first date after the departure.
    clock = (
        pl.when(pl.col("arr_clock_utc") < pl.col("dep_utc"))
        .then(pl.col("arr_clock_utc") + pl.duration(days=1))
        .otherwise(pl.col("arr_clock_utc"))
    )
    valid_block = pl.col("CRSElapsedTime") >= MIN_SCHEDULED_MINUTES
    f = f.with_columns(
        pl.when(valid_block)
        .then(pl.col("dep_utc") + pl.duration(minutes=pl.col("CRSElapsedTime")))
        .otherwise(clock)
        .alias("arr_utc"),
        ((clock - pl.col("dep_utc")).dt.total_minutes()).alias("clock_block"),
        # A diverted flight that reached its destination has its arrival delay in DivArrDelay.
        pl.when(pl.col("Diverted") == 1).then(pl.col("DivArrDelay")).otherwise(pl.col("ArrDelay")).alias("arr_delay"),
        pl.col("dep_utc").dt.truncate("1h").alias("P"),
    )
    f = f.with_columns(
        (pl.col("dep_utc") + pl.duration(minutes=pl.col("DepDelay"))).alias("dep_actual"),
        (pl.col("arr_utc") + pl.duration(minutes=pl.col("arr_delay"))).alias("arr_actual"),
    )
    # The aircraft's previous flight: the tail number's flight scheduled to leave just before this one.
    keys = ["Tail_Number", "dep_utc", "Reporting_Airline", "Flight_Number_Reporting_Airline", "Origin"]
    f = f.sort(keys, nulls_last=True, maintain_order=True)
    previous = ["Dest", "dep_utc", "arr_utc", "dep_actual", "arr_actual", "DepDelay", "arr_delay", "Cancelled"]
    f = f.with_columns(
        pl.when(pl.col("Tail_Number").is_not_null()).then(pl.col(c).shift(1).over("Tail_Number")).alias(f"prev_{c}")
        for c in previous
    )
    # Its state at the prediction point: a cancelled previous flight counts as not departed (when it was cancelled is
    # not recorded), a diverted one as in the air until it reaches this airport.
    chain = (pl.col("prev_Dest") == pl.col("Origin")).fill_null(False)
    departed = (pl.col("prev_Cancelled") == 0) & (pl.col("prev_dep_actual") <= pl.col("P"))
    landed = pl.col("prev_arr_actual") <= pl.col("P")
    status = (
        pl.when(~chain)
        .then(pl.lit("none"))
        .when(~departed.fill_null(False))
        .then(pl.lit("not departed"))
        .when(~landed.fill_null(False))
        .then(pl.lit("in the air"))
        .otherwise(pl.lit("arrived"))
    )
    f = f.with_columns(status.alias("INBOUND_STATUS"), chain.alias("chain"))
    f = f.with_columns(
        pl.when(pl.col("chain"))
        .then((pl.col("dep_utc") - pl.col("prev_arr_utc")).dt.total_minutes())
        .alias("INBOUND_TURN_MIN"),
        pl.when(pl.col("chain"))
        .then((pl.col("P") - pl.col("prev_dep_utc")).dt.total_minutes())
        .alias("INBOUND_MIN_SINCE_SCHED_DEP"),
        pl.when(pl.col("INBOUND_STATUS").is_in(["in the air", "arrived"]))
        .then(pl.col("prev_DepDelay"))
        .alias("INBOUND_DEP_DELAY"),
        pl.when(pl.col("INBOUND_STATUS") == "arrived").then(pl.col("prev_arr_delay")).alias("INBOUND_ARR_DELAY"),
    )
    return f, mapping


class AeolusRebuilt1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a US domestic flight arrive 15 minutes or more late?",
        use_case=(
            "Shortly before departure, an airline, an airport or a travel app estimates which of the coming flights "
            "will arrive late, from the schedule, where the aircraft is and the current weather at both airports."
        ),
        row="One US domestic flight of 2023-2024 that operated (left and arrived where scheduled).",
        predicted=(
            "Whether it arrives at least 15 minutes after its scheduled arrival (the US DOT definition); about one "
            "flight in five does."
        ),
        known=(
            "At the full hour before the scheduled departure: the date, airline, flight number, route, distance, "
            "scheduled times, the airports' locations, the weather reported at both airports for that hour, and "
            "where the aircraft's previous flight is (not yet left, in the air or landed, with its delays so far)."
        ),
        split=(
            "Each test window is two weeks at the end of 2024; training is a random million earlier flights from 2023"
            " on, as for a model refit every two weeks."
        ),
        changes=(
            "Rebuilt from the DOT's flight records and Meteostat's station weather instead of the Aeolus release: the "
            "weather is read at the right hour, March 2024 and the flights of 43 airports the release dropped are back, "
            "and the aircraft's previous flight is added."
        ),
        fit="approximate",
        fit_reason=(
            "Cancelled and diverted flights (1.6%; 0.4 to 1.4% of a test window) are not rows: the test data holds "
            "only flights that operated, which is not known an hour before departure. The aircraft is the one that "
            "flew; a swap decided after the prediction point is kept (notes)."
        ),
    )

    # Dataset
    unique_name = "aeolus_rebuilt_1m"
    version_of = "aeolus_rebuilt"
    version_comment = """
        The BTS files hold 13,708,650 operated flights from 2023 on with an arrival delay (13,926,960 scheduled). We sample per test window (v2 split protocol): each window keeps at most 500k of its rows (all of them here), and its train side is a random 1M of the earlier flights, drawn in one random order for all windows; the frame keeps only the rows a split uses.
    """
    year = "2026"  # the snapshot we pin; the BTS table and Meteostat's archive grow every month
    domain = "industry & manufacturing"  # transport has no value of its own; as for aeolus_1m, nyc_taxi_trip_duration
    source = "GOV Website"
    source_url = "https://www.transtats.bts.gov/Fields.asp?gnoyr_VQ=FGJ"
    license = (
        "BTS on-time data and the NOAA ISD station list: US government works (public domain); Meteostat weather and "
        "station data: CC BY 4.0 (https://dev.meteostat.net/license)"
    )
    data_tags = ("Spatial",)
    download_description = """
        Four public origins, downloaded on 2026-10-26 into local-data-warehouse/aeolus_rebuilt/ (0.8 GB). No login.

        1. BTS, Reporting Carrier On-Time Performance (1987-present): the monthly files of December 2022 to December
        2024 (25 zips; the server dates them 2023-03-16 to 2025-03-14).

        mkdir -p local-data-warehouse/aeolus_rebuilt/bts && cd local-data-warehouse/aeolus_rebuilt/bts
        for ym in 2022_12 2023_{1..12} 2024_{1..12}; do
            curl -fO "https://transtats.bts.gov/PREZIP/On_Time_Reporting_Carrier_On_Time_Performance_1987_present_${ym}.zip"
        done
        cd ..

        2. BTS, Master Coordinate (Aviation Support Tables: the position of every airport sequence id): on
        https://www.transtats.bts.gov/Fields.asp?gnoyr_VQ=FLL choose "Download", tick all fields and save the zip as
        T_MASTER_CORD.zip (it holds T_MASTER_CORD.csv). The form posts back to the same page; a scripted download has to
        send its __VIEWSTATE fields.

        3. NOAA, the station history of the Integrated Surface Database (the observing stations' positions):
        curl -fO https://www.ncei.noaa.gov/pub/data/noaa/isd-history.csv

        4. Meteostat: the station database, then the hourly dumps of 2022 to 2025 of the stations the definition maps
        to the airports (nearest qualifying station, README decision 1):
        curl -fO https://data.meteostat.net/stations.db
        for year in 2022 2023 2024 2025; do mkdir -p meteostat/hourly/$year; for station in $STATIONS; do
            curl -f -o meteostat/hourly/$year/$station.csv.gz https://data.meteostat.net/hourly/$year/$station.csv.gz
        done; done
        with STATIONS =
            4P0GT 56FNV 70026 70133 70200 70219 70261 70273 70296 70321 70326 70350 70361 70367 70371 70381 70386
            70387 70395 70454 70580 72201 72202 72203 72204 72205 72206 72207 72208 72211 72214 72216 72218 72219
            72221 72223 72226 72228 72231 72234 72235 72240 72241 72243 72247 72248 72250 72251 72252 72253 72255
            72256 72258 72259 72261 72263 72265 72266 72267 72268 72270 72274 72278 72288 72290 72295 72297 72302
            72306 72308 72310 72312 72314 72315 72317 72323 72324 72326 72327 72334 72335 72344 72351 72353 72355
            72356 72363 72365 72384 72386 72389 72392 72394 72399 72401 72403 72405 72406 72407 72408 72411 72414
            72421 72422 72423 72425 72428 72429 72432 72434 72435 72438 72439 72440 72445 72446 72450 72451 72464
            72466 72476 72480 72488 72492 72493 72494 72502 72503 72505 72507 72508 72509 72510 72513 72515 72517
            72518 72519 72520 72521 72524 72526 72528 72529 72530 72532 72533 72534 72535 72536 72537 72539 72543
            72544 72545 72546 72548 72549 72550 72551 72552 72557 72562 72564 72565 72566 72569 72572 72574 72577
            72578 72592 72597 72606 72607 72617 72628 72635 72637 72639 72640 72641 72643 72644 72645 72648 72651
            72655 72658 72659 72662 72665 72666 72670 72672 72677 72681 72691 72693 72698 72713 72744 72745 72747
            72753 72755 72763 72764 72772 72773 72774 72775 72779 72781 72782 72783 72785 72793 74486 74493 74521
            74545 74745 74754 74756 74757 74783 74787 74791 78514 78526 78543 78547 8RXA6 91165 91182 91190 91212
            91232 91285 91765 A13Z0 A4QYJ KACV0 KASE0 KATW0 KAZO0 KBLI0 KBMI0 KBQK0 KBRD0 KBTR0 KBZN0 KCDC0 KCHO0
            KCIU0 KCKB0 KCLL0 KCMI0 KCNY0 KCSG0 KCWA0 KDEC0 KDHN0 KEAR0 KEAU0 KECP0 KEGE0 KELM0 KEWN0 KFAY0 KFLG0
            KGCK0 KGFK0 KGRK0 KGTR0 KGUC0 KHDN0 KHGR0 KHIB0 KHOB0 KHPN0 KHRL0 KHXD0 KHYA0 KHYS0 KIAG0 KIDA0 KIMT0
            KITH0 KIWA0 KJLN0 KJMS0 KJQF0 KJST0 KLBE0 KLBL0 KLCK0 KLFT0 KMBS0 KMCW0 KMFE0 KMGW0 KMHK0 KMLU0 KMOT0
            KMTJ0 KMVY0 KNYL0 KOAJ0 KOWB0 KPAE0 KPBG0 KPGD0 KPGV0 KPHF0 KPIB0 KPIE0 KPLN0 KPRC0 KPSC0 KPSM0 KPSP0
            KPUW0 KPVU0 KRDM0 KRHI0 KRSW0 KSAF0 KSBP0 KSFB0 KSGU0 KSJC0 KSMF0 KSNA0 KSRQ0 KSTS0 KSUN0 KSWO0 KTTN0
            KTVC0 KTWF0 KTXK0 KTYR0 KUNV0 KVEL0 KVLD0 KWYS0 KXNA0 LJ957 M44D9 O5PFW OQRHP OZNF7 PASC0 PHKO0 SC9N0
            TJPS0 TRGWI

        `_prepare_raw_files` reads every file under meteostat/hourly/ (more stations do no harm) and writes
        flights.parquet and weather.parquet next to them.

        SHA-256 (first 16 hex digits): T_MASTER_CORD.zip 5ca8c8a826c3397b, stations.db e77981135762ade8,
        isd-history.csv 1994747ab4af1b97; BTS 2022_12 93ef0f6ede001547, 2023_1 327924faa362d360, 2023_2
        bfa6eb7bebb53f10, 2023_3 1a61dce7c50e5c4f, 2023_4 adf3ecf6e3763a55, 2023_5 aec2e926b11e55f8, 2023_6
        67dc6b993ba2e7c2, 2023_7 b1b73635dcb2add3, 2023_8 d374aa3ec2b844d4, 2023_9 4e7bc3f76857accd, 2023_10
        a92cc51c6bb1e7fc, 2023_11 9ad54595568704a1, 2023_12 c8391a3f06749b6e, 2024_1 fe089b45523f9d4a, 2024_2
        8463683d100504a9, 2024_3 e2c5021406f480e8, 2024_4 d8b1e88626a7375d, 2024_5 03e4ae26c2d1247d, 2024_6
        4f329439fd6892aa, 2024_7 4d992fee134137b3, 2024_8 58d651379af90cc4, 2024_9 c0df7503b0050ca4, 2024_10
        a417136d6c166373, 2024_11 26b6e89e7c1f6616, 2024_12 a324577aa76d1f0a.
    """
    bibtex = """
        @misc{bts2026ontime,
          title        = {Airline On-Time Performance Data: Reporting Carrier On-Time Performance (1987-present)},
          author       = {{Bureau of Transportation Statistics}},
          howpublished = {\\url{https://www.transtats.bts.gov/Fields.asp?gnoyr_VQ=FGJ}},
          year         = {2026},
          note         = {US Department of Transportation, TranStats; files of December 2022 to December 2024},
        }
        @misc{meteostat2026hourly,
          title        = {Meteostat Hourly Data},
          author       = {{Meteostat}},
          howpublished = {\\url{https://dev.meteostat.net/data/timeseries/hourly}},
          year         = {2026},
          note         = {Station data dumps of 2022 to 2025, CC BY 4.0},
        }
        @inproceedings{xu2025aeolus,
          title     = {Aeolus: A Multi-structural Flight Delay Dataset},
          author    = {Xu, Lin and Yuan, Xinyun and Liang, Yuxuan and Yin, Suwan and Wu, Yuankai},
          booktitle = {Advances in Neural Information Processing Systems (NeurIPS 2025), Datasets and Benchmarks Track},
          year      = {2025},
          note      = {arXiv:2510.26616; the task this dataset rebuilds},
        }
    """
    curation_comments = """
        We start with the monthly files of the BTS Reporting Carrier On-Time Performance table for December 2022 to December 2024 (14,484,055 scheduled flights), the BTS Master Coordinate table, NOAA's ISD station history, and Meteostat's station database and hourly station dumps of 2022 to 2025. The task is the classification task of Aeolus (Xu et al., NeurIPS 2025), rebuilt from these origins instead of the authors' Kaggle release (aeolus_1m).

        - Prediction point: the full UTC hour at or before the scheduled departure, 0 to 59 minutes before it (median 27). A row holds the schedule, the weather readings of that hour and the aircraft's previous flight as far as it had got by then.
        - History: flights from 2023-01-01 on, as in aeolus_1m (`HISTORY_START`); the December 2022 file only gives the previous flight of the first days.
        - Rows: flights that operated. 184,258 of the 13,926,960 flights of 2023-2024 were cancelled (1.3%) and 34,051 diverted (0.2%); BTS leaves their arrival delay empty, the paper's cohort has none (LEAK-22), and when a cancellation was decided is not recorded (fourth decision). One operated flight without an arrival delay is dropped.
        - Target: `ARR_DEL15`, an arrival 15 minutes or more after the schedule (US DOT; equal to BTS ArrDel15 on every operated flight). The paper's classification task uses more than 15 minutes.
        - Not read (`BTS_COLUMNS`): what is recorded at or after the departure (actual times, taxi and air times, delay causes, gate returns, diversions), copies (state, city, market, time blocks, groups) and constants. The tail number only links the aircraft's flights: as an id it would add nothing BTS describes.
        - Times: BTS clock times are local. Each airport's IANA time zone is its station's in Meteostat (timezonefinder on the BTS coordinates gives the same offsets for all 359 airports); departure plus scheduled block time then matches the local arrival clock on all but 0.03% of the flights (second decision). Scheduled times also ship as local minutes after midnight (`CRS_DEP_TIME_MIN`, `CRS_ARR_TIME_MIN`; BTS's 2400 is 1440).
        - Weather: each airport's nearest station with hourly observations through 2023-2024 (first decision; 353 of 359 within 2.5 km, at most 10.6 km), read at the prediction point's hour at both airports: 8 Meteostat parameters, the condition code as a category. ISD-Lite, the source of most readings, takes each value from the ten minutes up to the full hour (ISD-Lite Technical Document, 2006: "observation minute greater than or equal to ten minutes before the top of the hour up to and including the top of the hour"), so no reading is from after the prediction point. A wind direction of 0 is calm, 360 north. Peak gust and snow depth are empty and not kept. The 2025 files give the readings of the 2024-12-31 flights whose hour falls in 2025 in UTC.
        - Note: Meteostat fills missing observations with model forecasts for the hour: 0.2% of the origin temperatures, 5.9% of the precipitation, 41% of the cloud cover and 97% of the condition codes (third decision). A forecast for an hour is issued before it, so it is known at the prediction point; the issue times are not in the files. Kept as Meteostat publishes them, as Aeolus did.
        - Impossible weather becomes missing (`MIN_TEMPERATURE_C`, `MAX_WIND_KMH`, a humidity of 0%): 4 readings of -60.6 C at Sarasota, 45 mean winds of 121-232 km/h, most in clear or fair weather, and 11 humidities of 0% at Lihue and Jackson Hole. Precipitation up to 96.5 mm in an hour (Gulf and Florida storms) stays.
        - Aircraft's previous flight: the tail number's flight scheduled to leave just before this one (`INBOUND_*`). Its scheduled times are known; its actual departure and arrival delays only when they happened by the prediction point, else missing, and `INBOUND_STATUS` says how far it had got (`none` when it did not end at this origin). The five columns add 0.15 to 0.17 ROC AUC per window (0.647-0.654 without them, 0.800-0.827 with them; untuned LightGBM, 1M training rows).
        - Potential leak, kept on purpose: BTS records the aircraft that flew. When an aircraft was swapped, the row carries the swap: for 0.9% of the flights the recorded previous flight was scheduled to land after this departure (79-98% late), for 2.1% it ended elsewhere (42% late). Whether a swap was decided before the prediction point is not recorded. On the shipped splits these rows are 2.6-3.4% of a window; setting their five columns to `none` and missing costs 0.0002 to 0.0013 ROC AUC, and scoring without them gives 0.007 to 0.011 less. Revisit if a source of planned tail assignments turns up.
        - Proxy missing values: scheduled block times below 15 minutes (5 rows) become missing. 52 others that are more than twice or less than half their route's median stay as BTS records them.
        - Coordinates: the BTS master coordinate of the airport sequence id the flight uses (Guam and Pago Pago with their true signs).
        - `OP_CARRIER_FL_NUM` is categorical (the paper's Table 9), as in aeolus_1m; one operated flight has none.
        - Note: compared with the Aeolus release, the rebuild adds March 2024 (585,413 operated flights) and the 192,954 flights of 43 airports the release left out (mostly Allegiant and SkyWest), and reads the weather in the hour before departure, not 3.5 to 11 hours earlier. With aeolus_1m's inputs (the schedule and three weather values per airport), the weather adds 0.043-0.051 ROC AUC per window here against 0.032-0.039 in aeolus_1m (the destination's alone 0.010-0.014 against 0.014-0.015; untuned LightGBM on each dataset's own splits).
        - Task probes (200k newest training rows, three windows): no flags; ROC AUC LightGBM 0.819, random forest 0.808, linear 0.760, the best single feature (`INBOUND_ARR_DELAY`) 0.729. Leak probes (50k rows): no exact copies across the split; `INBOUND_ARR_DELAY` alone 0.734 against 0.790 for all features, the core of the task (a late aircraft makes a late flight); its missing indicator 0.683, which marks a previous flight that had not landed by the prediction point, known then. Every test airport is in training (known entities, SPLIT-13).
    """

    # Task
    target = "ARR_DEL15"
    problem_type = "binary_classification"
    metric = Metric.source(
        "roc_auc",
        original="AUC and ACC for the delay-occurrence classification task",
        reference=(
            "Xu et al., Aeolus: A Multi-structural Flight Delay Dataset, NeurIPS 2025 D&B, arXiv:2510.26616 "
            "(Sec. 4, Appendix: 'using Area Under the Curve (AUC) and Accuracy (ACC) as evaluation metrics')"
        ),
        definition="ROC AUC of the probability of an arrival delay of 15+ minutes",
    )

    # Splits
    splits_comment = """
        As in aeolus_1m: a delay model is refit every two weeks and predicts the flights of the two weeks ahead. The last six weeks of 2024 are three two-week test windows (2024-12-18 to 12-31, 12-04 to 12-17 and 11-20 to 12-03, newest first; 25.9%, 16.7% and 17.5% of the operated flights late), so that one window falls in the holiday peak. Train is every flight from 2023 on dated at least two days before the window (a one-day gap): a flight's arrival delay is known only once it has landed, and the previous evening's flights land after midnight. Each window keeps all of its flights (264,245, 259,738 and 273,891); each train side is a random 1M of the earlier flights (one random order for all windows). The authors split 1-15 June 2024 chronologically 6:2:2 (Sec. 4.1), one test stretch of about three days and no season, so we depart from it. All three windows lie in late November and December: the score measures early-winter delays.
    """
    temporal = Temporal(on="FL_DATE", splits=TemporalSplits(window=14, unit="days", n_windows=3, gap=1))
    subsample_to_budget = True

    # The 25 monthly BTS files (zipped CSVs) and about 1,800 station-year weather files are converted once into two
    # parquet files; everything else is read as it is.
    prepared_raw_files = ("flights.parquet", "weather.parquet")

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        frames = []
        for path in sorted((raw_dir / "bts").glob("*.zip")):
            with zipfile.ZipFile(path) as archive:
                name = next(n for n in archive.namelist() if n.endswith(".csv"))
                data = archive.read(name)
            frames.append(pl.read_csv(io.BytesIO(data), columns=list(BTS_COLUMNS), schema_overrides=BTS_COLUMNS))
        assert len(frames) == N_BTS_FILES, f"Expected {N_BTS_FILES} monthly BTS files, found {len(frames)}."
        flights = pl.concat(frames).with_columns(pl.col("FlightDate").str.to_date("%Y-%m-%d"))
        flights.write_parquet(raw_dir / "flights.parquet")

        columns = [*WEATHER, *(f"{c}_source" for c in WEATHER)]
        parts = []
        for path in sorted((raw_dir / "meteostat" / "hourly").glob("*/*.csv.gz")):
            part = pl.read_csv(path, infer_schema_length=0)
            part = part.select(
                pl.lit(path.name.split(".")[0]).alias("station"),
                pl.datetime(*(pl.col(c).cast(pl.Int32) for c in ("year", "month", "day", "hour"))).alias("time"),
                *(pl.col(c) for c in columns if c in part.columns),
            )
            parts.append(part)
        weather = pl.concat(parts, how="diagonal").with_columns(pl.col(c).cast(pl.Float64) for c in WEATHER)
        weather.select("station", "time", *columns).sort(["station", "time"]).write_parquet(raw_dir / "weather.parquet")

    def _load_raw(self, raw_dir: Path) -> dict[str, pl.DataFrame]:
        flights = pl.read_parquet(raw_dir / "flights.parquet")
        weather = pl.read_parquet(raw_dir / "weather.parquet")
        with zipfile.ZipFile(raw_dir / "T_MASTER_CORD.zip") as archive:
            master = pl.read_csv(io.BytesIO(archive.read("T_MASTER_CORD.csv")), infer_schema_length=0)
        coordinates = master.select(
            pl.col("AIRPORT_SEQ_ID").cast(pl.Int64).alias("seq"),
            pl.col("LATITUDE").cast(pl.Float64).alias("lat"),
            pl.col("LONGITUDE").cast(pl.Float64).alias("lon"),
            pl.col("UTC_LOCAL_TIME_VARIATION").alias("utc_variation"),
        )
        connection = sqlite3.connect(raw_dir / "stations.db")
        try:
            stations = pl.read_database("select id, latitude, longitude, timezone from stations", connection)
            names = pl.read_database("select station, name from names where language = 'en'", connection)
            keys = "select station, key, value from identifiers where key in ('usaf', 'wban', 'icao')"
            identifiers = pl.read_database(keys, connection)
            inventory = pl.read_database(
                "select station, provider, start, end from inventory where parameter = 'temp'", connection
            )
        finally:
            connection.close()
        isd = pl.read_csv(raw_dir / "isd-history.csv", infer_schema_length=0).select(
            pl.col("USAF").alias("usaf"),
            pl.col("WBAN").alias("wban"),
            pl.col("STATION NAME").alias("isd_name"),
            pl.col("LAT").cast(pl.Float64, strict=False).alias("isd_lat"),
            pl.col("LON").cast(pl.Float64, strict=False).alias("isd_lon"),
        )
        qualifying = inventory.filter(
            pl.col("provider").is_in(OBSERVATION_PROVIDERS)
            & (pl.col("start") < HISTORY_START)
            & (pl.col("end") > "2025-01-01")
        )
        ids = identifiers.pivot(on="key", index="station", values="value")
        stations = (
            stations.join(ids, left_on="id", right_on="station", how="left")
            .join(names, left_on="id", right_on="station", how="left")
            .with_columns(pl.col("wban").fill_null("99999"))
            .join(isd, on=["usaf", "wban"], how="left")
            .with_columns(
                pl.coalesce("isd_lat", "latitude").alias("lat"),
                pl.coalesce("isd_lon", "longitude").alias("lon"),
                pl.when(pl.col("isd_lat").is_not_null())
                .then(pl.lit("NOAA ISD"))
                .otherwise(pl.lit("Meteostat"))
                .alias("position"),
                pl.coalesce("isd_name", "name").alias("name"),
                pl.col("id").is_in(qualifying["station"].implode()).alias("qualifies"),
            )
            .select("id", "lat", "lon", "timezone", "name", "icao", "position", "qualifies")
            .sort("id")
        )
        return {"flights": flights, "weather": weather, "coordinates": coordinates, "stations": stations}

    def _clean(self, raw: dict[str, pl.DataFrame]) -> pd.DataFrame:
        f, mapping = _flights_utc(raw)
        # Rows: the flights from 2023 on that operated; cancelled and diverted flights have no arrival delay (BTS
        # leaves ArrDel15 empty for them), and one operated flight has none either.
        f = f.filter(
            (pl.col("FlightDate") >= pl.lit(HISTORY_START).str.to_date())
            & (pl.col("Cancelled") == 0)
            & (pl.col("Diverted") == 0)
            & pl.col("ArrDelay").is_not_null()
        )
        # Weather: each airport's station, the reading of the prediction point's hour (the full hour at or before the
        # scheduled departure, in UTC), at the origin and at the destination.
        weather = raw["weather"].filter(pl.col("station").is_in(mapping["station"].implode()))
        assert set(mapping["station"]) <= set(weather["station"].unique()), "a mapped station has no weather file"
        readings = weather.select("station", "time", *WEATHER)
        for side, station in (("O", "o_station"), ("D", "d_station")):
            renamed = readings.rename(
                {"station": station, "time": "P", **{c: f"{side}_{n}" for c, n in WEATHER.items()}}
            )
            f = f.join(renamed, on=[station, "P"], how="left", maintain_order="left")
        # Impossible weather readings to missing: temperatures below -50 C, mean winds above 120 km/h and a relative
        # humidity of 0% (11 readings at Lihue and Jackson Hole, at 20-28 C).
        for side in ("O", "D"):
            f = f.with_columns(
                pl.when(pl.col(f"{side}_TEMP") >= MIN_TEMPERATURE_C).then(pl.col(f"{side}_TEMP")).alias(f"{side}_TEMP"),
                pl.when(pl.col(f"{side}_WSPD") <= MAX_WIND_KMH).then(pl.col(f"{side}_WSPD")).alias(f"{side}_WSPD"),
                pl.when(pl.col(f"{side}_RHUM") > 0).then(pl.col(f"{side}_RHUM")).alias(f"{side}_RHUM"),
            )
        conditions = pl.DataFrame(
            {"code": list(WEATHER_CONDITIONS), "label": list(WEATHER_CONDITIONS.values())},
            schema={"code": pl.Float64, "label": pl.String},
        )
        for side in ("O", "D"):
            f = f.with_columns(
                pl.col(f"{side}_COCO").replace_strict(conditions["code"], conditions["label"], default=None)
            )
        # Airport coordinates: the BTS master coordinate of the airport sequence id the flight uses.
        coordinates = raw["coordinates"].select("seq", "lat", "lon")
        for side, seq in (("O", "OriginAirportSeqID"), ("D", "DestAirportSeqID")):
            renamed = coordinates.rename({"seq": seq, "lat": f"{side}_LATITUDE", "lon": f"{side}_LONGITUDE"})
            f = f.join(renamed, on=seq, how="left", maintain_order="left")
        df = f.select(
            pl.col("FlightDate").cast(pl.Datetime("ns")).alias("FL_DATE"),
            pl.col("Reporting_Airline").alias("OP_CARRIER"),
            pl.col("Flight_Number_Reporting_Airline").alias("OP_CARRIER_FL_NUM"),
            pl.col("Origin").alias("ORIGIN"),
            pl.col("Dest").alias("DEST"),
            # Scheduled local clock times in minutes after midnight (BTS writes a midnight departure as 2400).
            _hhmm_minutes("CRSDepTime").alias("CRS_DEP_TIME_MIN"),
            _hhmm_minutes("CRSArrTime").alias("CRS_ARR_TIME_MIN"),
            # Proxy missing values: impossible scheduled block times.
            pl.when(pl.col("CRSElapsedTime") >= MIN_SCHEDULED_MINUTES)
            .then(pl.col("CRSElapsedTime"))
            .alias("CRS_ELAPSED_TIME"),
            pl.col("Distance").alias("DISTANCE"),
            "O_LATITUDE",
            "O_LONGITUDE",
            "D_LATITUDE",
            "D_LONGITUDE",
            *(f"O_{n}" for n in WEATHER.values()),
            *(f"D_{n}" for n in WEATHER.values()),
            "INBOUND_STATUS",
            "INBOUND_TURN_MIN",
            "INBOUND_MIN_SINCE_SCHED_DEP",
            "INBOUND_DEP_DELAY",
            "INBOUND_ARR_DELAY",
            # Target: an arrival 15 minutes or more after the schedule (US DOT on-time definition, BTS ArrDel15).
            pl.when(pl.col("ArrDelay") >= DELAY_THRESHOLD_MINUTES)
            .then(pl.lit("Yes"))
            .otherwise(pl.lit("No"))
            .alias("ARR_DEL15"),
        )
        df = df.to_pandas()
        # A flight number is a label of its carrier (one operated flight has none); nullable before it becomes a category.
        df["OP_CARRIER_FL_NUM"] = df["OP_CARRIER_FL_NUM"].astype("Int64")
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        del df
        return FeatureTypes(
            categorical=["OP_CARRIER", "OP_CARRIER_FL_NUM", "ORIGIN", "DEST", "O_COCO", "D_COCO", "INBOUND_STATUS"],
            datetime=["FL_DATE"],
        )

    def _decisions(self, raw: dict[str, pl.DataFrame], df: pd.DataFrame) -> list[Decision]:
        del df
        f, mapping = _flights_utc(raw)
        rows = f.filter(pl.col("FlightDate") >= pl.lit(HISTORY_START).str.to_date())
        operated = rows.filter(
            (pl.col("Cancelled") == 0) & (pl.col("Diverted") == 0) & pl.col("ArrDelay").is_not_null()
        )

        # 1. The weather station of each airport.
        flights_per_airport = (
            pl.concat([operated.select(pl.col("Origin").alias("code")), operated.select(pl.col("Dest").alias("code"))])
            .group_by("code", maintain_order=True)
            .len(name="flight ends")
        )
        stations = mapping.join(flights_per_airport, on="code", how="left").with_columns(
            pl.col("flight ends").fill_null(0)
        )
        columns = {
            "code": "airport",
            "station": "station",
            "name": "station name",
            "position": "station position from",
            "km": "km",
            "flight ends": "flight ends",
        }
        far = stations.filter((pl.col("km") > 2.5) | (pl.col("position") == "Meteostat")).sort("km", descending=True)
        every = stations.sort("code").select(list(columns)).rename(columns).to_pandas()
        station_evidence = (
            _markdown_table(far.select(list(columns)).rename(columns).to_pandas())
            + f"\n\n<details>\n<summary>All {stations.height} airports</summary>\n\n"
            + _markdown_table(every)
            + "\n\n</details>"
        )
        within = int((stations["km"] <= 2.5).sum())
        own = int(stations.select(pl.col("icao").str.ends_with(pl.col("code")).fill_null(False).sum()).item())

        # 2. Time zones: the scheduled block from the converted clock times against BTS's scheduled elapsed time.
        check = operated.filter(pl.col("CRSElapsedTime") >= MIN_SCHEDULED_MINUTES).with_columns(
            (pl.col("clock_block") == pl.col("CRSElapsedTime")).alias("agrees")
        )
        zones = (
            check.group_by("o_tz", maintain_order=True)
            .agg(
                pl.col("Origin").n_unique().alias("origin airports"),
                pl.len().alias("flights"),
                pl.col("agrees").mean().round(5).alias("share agreeing"),
            )
            .sort("flights", descending=True)
            .rename({"o_tz": "origin time zone"})
            .to_pandas()
        )

        # 3. The weather's timing and where its values come from.
        lead = operated.select(((pl.col("dep_utc") - pl.col("P")).dt.total_minutes()).alias("minutes"))
        weather = raw["weather"]
        readings = operated.select(pl.col("o_station").alias("station"), pl.col("P").alias("time")).join(
            weather, on=["station", "time"], how="left", maintain_order="left"
        )
        sources = []
        for column in WEATHER:
            source = readings[f"{column}_source"]
            present = readings[column].is_not_null()
            sources.append(
                {
                    "parameter": column,
                    "present": round(float(present.mean()), 4),
                    "observed (ISD-Lite, METAR)": round(float(source.is_in(OBSERVATION_PROVIDERS).mean()), 4),
                    "model or forecast fill": round(float((present & ~source.is_in(OBSERVATION_PROVIDERS)).mean()), 4),
                }
            )
        source_table = pd.DataFrame(sources)

        # 4. Cancelled and diverted flights in the test windows.
        windows = []
        for start, end in TEST_WINDOWS:
            w = rows.filter(pl.col("FlightDate").is_between(pl.lit(start).str.to_date(), pl.lit(end).str.to_date()))
            op = w.filter((pl.col("Cancelled") == 0) & (pl.col("Diverted") == 0))
            late = int((op["ArrDelay"] >= DELAY_THRESHOLD_MINUTES).sum())
            not_operated = w.height - op.height
            windows.append(
                {
                    "window": f"{start} to {end}",
                    "scheduled flights": w.height,
                    "cancelled": int(w["Cancelled"].sum()),
                    "diverted": int(w["Diverted"].sum()),
                    "late share of operated": round(late / op.height, 4),
                    "late share, cancelled and diverted counted late": round((late + not_operated) / w.height, 4),
                }
            )
        cohort = pd.DataFrame(windows)

        # 5. The aircraft's previous flight at the prediction point.
        inbound = (
            operated.with_columns(
                (pl.col("ArrDelay") >= DELAY_THRESHOLD_MINUTES).alias("late"),
                (pl.col("INBOUND_TURN_MIN") < 0).fill_null(False).alias("overlap"),
            )
            .group_by("INBOUND_STATUS", "overlap", maintain_order=True)
            .agg(pl.len().alias("flights"), pl.col("late").mean().round(4).alias("late share"))
            .with_columns((pl.col("flights") / operated.height).round(4).alias("share of flights"))
            .sort("flights", descending=True)
            .rename(
                {
                    "INBOUND_STATUS": "previous flight at the prediction point",
                    "overlap": "scheduled to land after this departure",
                }
            )
            .to_pandas()
        )

        return [
            Decision(
                "Each airport's weather comes from its nearest observing station",
                f"Each of the {stations.height} airports gets the Meteostat station nearest to its BTS master coordinate "
                "among the stations with hourly ISD-Lite or METAR temperatures from before 2023 to after 2024, by the "
                "station's NOAA ISD position where it has an ISD id (Meteostat's own positions of WMO stations can be "
                f"30 km off, as for Atlanta). {within} of the {stations.height} stations are within 2.5 km and {own} carry "
                "the airport's own ICAO code; the first table lists the others and the stations only Meteostat "
                "positions, the second every airport.",
                station_evidence,
            ),
            Decision(
                "Scheduled local times are converted to UTC with each airport's time zone",
                "BTS gives local clock times. With the IANA time zone of each airport's station, the scheduled "
                "departure and arrival clock times give BTS's scheduled elapsed time on nearly every flight; the rest "
                "cross the date line (Guam to Honolulu) or a change of daylight saving time.",
                zones,
            ),
            Decision(
                "The weather is the reading of the full hour before the scheduled departure",
                "The prediction point is the full UTC hour at or before the scheduled departure; both airports' "
                "readings are of that hour, so none comes after it. The departure follows the reading by "
                f"{int(lead['minutes'].min())} to {int(lead['minutes'].max())} minutes (median "
                f"{float(lead['minutes'].median()):.0f}); in the Aeolus release it was 3.5 to 11 hours. Meteostat "
                "fills gaps in the observations with model data (its forecasts for the hour); the weather condition "
                "code and part of the cloud cover come mostly from them. The table is for the origin readings.",
                source_table,
            ),
            Decision(
                "Cancelled and diverted flights are not rows",
                "BTS leaves the arrival delay empty for cancelled and diverted flights, the release has none, and "
                "their timing is not recorded. They cluster on storm days: the newest window has the most.",
                cohort,
            ),
            Decision(
                "The aircraft's previous flight, as known at the prediction point",
                "The tail number links each flight to the aircraft's flight scheduled just before it. Its actual "
                "departure and arrival count only when they happened by the prediction point. Flights whose aircraft "
                "was scheduled to land after this departure, or whose previous flight ended elsewhere, were "
                "re-planned: the recorded aircraft may come from a swap made after the prediction point (notes).",
                inbound,
            ),
        ]
