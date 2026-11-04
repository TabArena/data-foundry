"""Curated Lusaka ride-time regression (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    TaskSummary,
    Temporal,
    TemporalSplits,
)

MIRROR_COMMIT = "2fa7817be0740ea1739143ea6e61a28d6cf1462d"
COORDINATES = ("origin_lat", "origin_lon", "destination_lat", "destination_lon")
WEATHER_COLUMNS = ("precipitation_type", "prev_hour_precipitation_mm", "temperature_C")

MIN_STRAIGHT_LINE_KM = 0.1
"""A trip that ends closer to its start has no destination a passenger would book (Lennart, 2026-11-04; the radius of
nyc_taxi_trip_duration_1m and pkdd_15_taxi_trip_time_prediction_ii_1m)."""


class LusakaMobility2024(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How many minutes will an individual Yango trip in Lusaka take?",
        use_case=(
            "At pickup, when the driver starts the ride, a ride-hailing app estimates the minutes to the destination "
            "to show the passenger an arrival time. A model is refit every four days using completed earlier trips."
        ),
        row=(
            "One labeled trip from the 2024 Lusaka challenge's participant mirror: 110,375 trips with start times "
            "that end at least 100 m from their start. "
            "The files record January 2023 and early February, despite the source description saying January 2024."
        ),
        predicted="The actual trip duration in minutes, unchanged from the source target.",
        known=(
            "Retained inputs are start time, masked endpoints, original-point straight-line distance and earlier-hour "
            "weather. Endpoints stand in for requested locations; destination capture and weather publication "
            "timing are unverified, so departure-time availability is an assumption."
        ),
        split=(
            "Three four-day periods beginning January 21, 25 and 29 on the recorded 2023 calendar. "
            "Training contains trips starting at least one day before each period."
        ),
        changes=(
            "Remove actual traveled distance, trip ID and duplicate date; exclude 21 trips without start times and "
            "2,364 that end within 100 m of their start; replace random-row evaluation with chronological windows "
            "and use earlier-hour weather."
        ),
        fit="approximate",
        fit_reason=(
            "No routing-engine route or ETA ships, so the estimate rests on geometry, time and weather alone. "
            "Recorded destination and straight-line distance stand in for the planned route endpoints. "
            "Their capture time, the weather clock and weather publication latency are undocumented. The sample "
            "year conflicts with its description, and only a participant copy was accessible."
        ),
    )
    unique_name = "2024_lusaka_mobility_prediction_hackathon"
    year = "2024"
    domain = "industry & manufacturing"
    source = "Zindi"
    source_url = "https://zindi.world/competitions/2024-lusaka-mobility-prediction-hackathon"
    license = "Zindi Competition Rules (Yango private property)"
    data_tags = ("Spatial", "Anonymized")
    download_description = """
        The first publisher is Yango's 2024 Lusaka challenge on Zindi. Original downloads require access unavailable
        to this session. We use the public participant copy Mwandamena/yango-hackathon, pinned at commit
        2fa7817be0740ea1739143ea6e61a28d6cf1462d. Its training, test and weather file sizes match the organizer
        listing's rounded sizes (15.6 MB, 6.4 MB, 49 KB); byte identity with the organizer files is unverified. Only Train.csv and Lusaka_weather.csv are read.

        mkdir -p local-data-warehouse/2024_lusaka_mobility_prediction_hackathon/2fa7817be0740ea1739143ea6e61a28d6cf1462d
        curl --fail --location https://raw.githubusercontent.com/Mwandamena/yango-hackathon/2fa7817be0740ea1739143ea6e61a28d6cf1462d/data/Train.csv -o local-data-warehouse/2024_lusaka_mobility_prediction_hackathon/2fa7817be0740ea1739143ea6e61a28d6cf1462d/Train.csv
        curl --fail --location https://raw.githubusercontent.com/Mwandamena/yango-hackathon/2fa7817be0740ea1739143ea6e61a28d6cf1462d/data/Lusaka_weather.csv -o local-data-warehouse/2024_lusaka_mobility_prediction_hackathon/2fa7817be0740ea1739143ea6e61a28d6cf1462d/Lusaka_weather.csv

        The original competition/reuse restrictions remain separate from this copy's technical accessibility.
    """
    bibtex = r"""
        @misc{yango2024lusaka,
          author = {{Yango} and {Zindi}},
          title = {2024 Lusaka Mobility Prediction Hackathon},
          year = {2024},
          howpublished = {\url{https://zindi.world/competitions/2024-lusaka-mobility-prediction-hackathon}},
          note = {Trip-duration competition; participant download copy pinned separately}
        }
    """
    curation_comments = """
        We start with Train.csv and Lusaka_weather.csv from the participant mirror pinned in download_description.

        - Prediction point: trip start, to estimate minutes to the destination. Actual traveled distance is removed because it is measured over the completed trip. The inspected participant-copy starter includes it; that is not evidence it exists at departure (USE-3, LEAK-10).
        - Endpoint approximation: the source says endpoint coordinates are geomasked and straight-line distance uses the original points. It does not state when the destination was captured. Recorded destination and straight-line distance stand in for the requested destination, as in the NYC taxi precedent; direct prospective availability is not certified. The recorded end means two things: in some trips the realised drop-off (the round trips dropped below), in others a requested destination the rider did not reach (1,756 kept trips, 1.6%, drove under 0.9 times the straight line, 290 under 0.5 times). Where it is the drop-off, the destination and `str_distance_km` carry some post-trip location. These rows stay: a filter on the driven distance would select rows on the outcome (USE-3, LEAK-1). No routing-engine route or ETA ships (USE-8).
        - Cohort and provenance: the source describes January 2024, while the pinned trip timestamps run from 2023-01-01 to early 2023-02-01 and the weather and inspected participant-copy starter notebook identify January 2023. We preserve the supplied dates and publication year 2024; no calendar shift or original-byte equality is asserted. Only labeled Train.csv is used; competition test labels are not available.
        - Rows: drop the 21 missing start timestamps, which cannot be assigned honestly to chronological windows. The source already removed very short trips using an unspecified threshold; that selection cannot be undone.
        - We drop the 2,364 trips (2.1% of the 112,739 with a start; 1.3 to 2.9% on every day) whose straight-line distance from start to end is under 0.1 km (Lennart, 2026-11-04: "drop them, this is not a relevant prediction goal here imo"; USE-7, the 100 m radius of nyc_taxi_trip_duration_1m and pkdd_15_taxi_trip_time_prediction_ii_1m): nobody books a ride to their own pickup point, so these rows lack the destination the ETA acts on. The cut is on the recorded endpoint, which for these rows is not a booked destination, not on the target, and exact although the coordinates are masked, because the source computes `str_distance_km` from the original points. These trips are not short: median 22.1 minutes against 10.8 for the others, 93% over 5 minutes, median travelled distance 4.5 km (round trips), and they held 16% of the target's squared spread. 110,375 trips remain, with complete positive targets.
        - Features: drop trip_id and the duplicate day-only start column. Keep coordinates and straight-line kilometers numeric; no route-distance or speed feature is calculated. All remaining durations are kept as published.
        - Anomaly: some kept durations look like recording errors. 20 trips last over 3 hours, the longest 788 minutes for 20.2 km driven and 1.1 km in a straight line (1.5 km/h over the driven distance), and some run under 0.5 km/h for 4 to 5 hours: trips perhaps not closed in the app. 19 trips imply over 120 km/h in a straight line, up to 416 km/h (8.9 km in 1.3 minutes). Both groups stay until the curator decides (CLEAN-11).
        - Weather: map the exact hourly record stamped floor(trip_start)-1 hour. The source dictionary calls both clocks local, but the weather's daily temperature curve (flat minimum at stamps 02 to 04, a rise at 05 before the 05:50 sunrise, maximum at 12 to 13) fits UTC stamps; if they are UTC (local is UTC+2), the joined record is that of the start hour and overlaps the ride. Unverified; the weather columns score about 0 alone, and weather of the following hours gained nothing beyond noise for a participant model. This lag is not a verified publication delay. No future fill or date/year correction is used. The weather's row counter/date/time are join metadata, not predictors; precipitation type is categorical. Missing earlier weather remains missing.
        - Metric: source RMSE on actual minutes, with identity target transform (MET-4). No target-based filtering or logarithm is introduced. The score leans on a few rows: the largest 1% of a LightGBM's errors hold 54 to 66% of its squared error, trips over 120 minutes hold 16.9%, 28.8% and 15.7% of each test window's squared deviation, and the one 788-minute trip holds 21% in the window from 2023-01-25 (constant-prediction RMSE 13.33, 11.85 without it) (MET-2).
        - Split: chronological four-day windows with a one-day training gap. Every observed duration is under one day, so the gap puts observed training trip ends before refit; reporting delay beyond trip completion is not known. The participant copy's train/test files interpolate throughout the same month; our evaluation instead tests later trips.
        - Curator decision (2026-10-29, Myunghwan): "approximate version is fine." Accept the documented endpoint and earlier-hour weather stand-ins; capture/publication and reporting timing remain unverified rather than certified by acceptance.
        - Source/calendar decision (2026-10-29, Myunghwan): "if timestamps between trips and weather algined, it's ok. this is the source we have to live with." The supplied trip/weather calendars align in 2023, with an exact preceding-hour match for 110,352 of the kept rides and 23 out-of-coverage rides retaining missing weather. Preserve the supplied dates and identified participant copy; organizer-original equality, actual timezone and the reason for the 2024 narrative remain unverified.
        - Scope: one released city/month, with masked locations and uncertain endpoint timing. The last test period has a partial final day because the file ends early February 1; this does not establish all-season, other-city or complete four-day deployment performance.
    """
    target = "Target"
    problem_type = "regression"
    metric = Metric.source(
        "rmse",
        original="Root Mean Squared Error",
        reference=source_url + "#evaluation",
        definition="Square root of mean squared error on trip duration in minutes; identity target transform.",
    )
    temporal = Temporal(
        on="trip_start",
        splits=TemporalSplits(
            window=4,
            unit="days",
            cutoffs=("2023-01-21", "2023-01-25", "2023-01-29"),
            gap=1,
            min_train_fraction=0.5,
        ),
    )
    splits_comment = """
        Three four-day windows start on the recorded calendar at 2023-01-29, 2023-01-25 and 2023-01-21,
        newest first. Four-day refits are a benchmark design choice within the one-month extract, not an organizer
        cadence. Each training side uses all earlier trips starting at least one day before its test start; every
        observed trip lasts less than 24 hours, so training trips finish before each test-start/refit time. Subsequent
        label reporting delay and original cohort extraction/follow-up timing are undocumented. A fourth
        earlier four-day window would violate the half-data training floor after this gap. The latest window ends
        February 2 but only has observations through early February 1. No performance was used to choose windows.
        The windows hold different weekday mixes (the one from January 25 has no Sunday); trips are shorter on all
        five Sundays (11.1 to 12.1 minutes on average, against 13.7 to 14.7 on other days), a weekly pattern, not
        drift.
        Missing starts and trips ending within 100 m of their start are excluded; other rows, target units and dates
        are preserved.
    """
    accepted_check_warnings = {}

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        folder = raw_dir / MIRROR_COMMIT
        return {"trips": pd.read_csv(folder / "Train.csv"), "weather": pd.read_csv(folder / "Lusaka_weather.csv")}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        trips = raw["trips"]
        start = pd.to_datetime(trips["lcl_start_transporting_dttm"], format="ISO8601", errors="coerce")
        keep = start.notna() & (trips["str_distance_km"] >= MIN_STRAIGHT_LINE_KM)
        df = trips.loc[keep, [*COORDINATES, "str_distance_km", "Target"]].copy()
        df["trip_start"] = start.loc[df.index]
        key = df["trip_start"].dt.floor("h") - pd.Timedelta(hours=1)
        weather = raw["weather"].copy()
        weather["stamp"] = pd.to_datetime(weather["lcl_datetime"], format="ISO8601")
        assert weather["stamp"].is_unique
        weather = weather.set_index("stamp")
        for column in WEATHER_COLUMNS:
            df[column] = key.map(weather[column])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["precipitation_type"], datetime=["trip_start"])

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        trips = raw["trips"]
        has_start = pd.to_datetime(trips["lcl_start_transporting_dttm"], format="ISO8601", errors="coerce").notna()
        return [
            Decision(
                title="Source dates and chronological row eligibility",
                why=(
                    "Dates are preserved despite the description's 2024 claim; missing starts cannot support temporal "
                    "tests; a trip ending within 100 m of its start has no destination a passenger would book."
                ),
                evidence=pd.DataFrame(
                    {
                        "quantity": [
                            "labeled raw rows",
                            "kept rows",
                            "missing start",
                            f"start, straight line under {MIN_STRAIGHT_LINE_KM} km",
                            "recorded minimum",
                            "recorded maximum",
                        ],
                        "value": [
                            str(len(trips)),
                            str(len(df)),
                            str(int((~has_start).sum())),
                            str(int((has_start & (trips["str_distance_km"] < MIN_STRAIGHT_LINE_KM)).sum())),
                            str(df.trip_start.min()),
                            str(df.trip_start.max()),
                        ],
                    }
                ),
            ),
            Decision(
                title="Earlier-hour weather and duration-label gap",
                why="Use only an exact prior-hour weather row, and compare the one-day gap with observed trip duration.",
                evidence=pd.DataFrame(
                    {
                        "quantity": ["trips without previous-hour weather", "maximum trip minutes", "gap minutes"],
                        "value": [str(df.temperature_C.isna().sum()), str(df.Target.max()), "1440"],
                    }
                ),
            ),
        ]
