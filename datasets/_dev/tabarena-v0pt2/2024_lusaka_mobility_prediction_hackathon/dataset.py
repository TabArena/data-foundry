"""Curated Lusaka ride-time regression (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    Source,
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

MAX_TRIP_MINUTES = 3 * 60
"""A longer trip was not closed in the app (Lennart, 2026-11-05), as the meter left running of
pkdd_15_taxi_trip_time_prediction_ii_1m (`MAX_TRAVEL_TIME_S`) and the 3 h cap of nyc_taxi_trip_duration_1m."""

MAX_STRAIGHT_LINE_KMH = 120
"""A faster straight line from start to end means a wrong duration or endpoint (Lennart, 2026-11-05; as pkdd): the
source computes `str_distance_km` from the unmasked points, so the speed is exact."""

WEATHER_LAG_HOURS = 3
"""A trip gets the weather row stamped this long before its start hour (Lennart, 2026-11-05): the weather's daily
curve fits UTC stamps (Lusaka is UTC+2) against the dictionary's local clock, so the row precedes the start on
either clock."""


def _trip_start(trips: pd.DataFrame) -> pd.Series:
    """The recorded start, missing where the source left it blank."""
    return pd.to_datetime(trips["lcl_start_transporting_dttm"], format="ISO8601", errors="coerce")


def _row_filters(trips: pd.DataFrame) -> list[tuple[str, pd.Series]]:
    """The row filters of `_clean`, in the order the README counts them: (reason, mask of the rows kept)."""
    minutes, km = trips["Target"], trips["str_distance_km"]
    return [
        ("no start time (no chronological window)", _trip_start(trips).notna()),
        (
            f"straight line from start to end under {MIN_STRAIGHT_LINE_KM} km (no destination a passenger would book)",
            km >= MIN_STRAIGHT_LINE_KM,
        ),
        (f"trip over {MAX_TRIP_MINUTES // 60} h (not closed in the app)", minutes <= MAX_TRIP_MINUTES),
        (
            f"straight line from start to end faster than {MAX_STRAIGHT_LINE_KMH} km/h (wrong duration or endpoint)",
            km <= MAX_STRAIGHT_LINE_KMH * minutes / 60,
        ),
    ]


class LusakaMobility2024(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How many minutes will an individual Yango trip in Lusaka take?",
        use_case=(
            "At pickup, when the driver starts the ride, a ride-hailing app estimates the minutes to the destination "
            "to show the passenger an arrival time. A model is refit every four days using completed earlier trips."
        ),
        row=(
            "One labeled trip from the 2024 Lusaka challenge's participant mirror: 110,336 trips with start times "
            "that end at least 100 m from their start, last at most 3 hours and imply at most 120 km/h in a straight "
            "line. "
            "The files record January 2023 and early February, despite the source description saying January 2024."
        ),
        predicted="The actual trip duration in minutes, unchanged from the source target.",
        known=(
            "Retained inputs are start time, masked endpoints, original-point straight-line distance and the weather "
            "stamped 3 hours before the start hour, earlier than the start whether the weather clock is local or "
            "UTC. Endpoints stand in for requested locations; destination capture and weather publication "
            "timing are unverified, so departure-time availability is an assumption."
        ),
        split=(
            "Three four-day periods beginning January 21, 25 and 29 on the recorded 2023 calendar. "
            "Training contains trips starting at least one day before each period."
        ),
        changes=(
            "Remove actual traveled distance, trip ID and duplicate date; exclude 21 trips without start times, "
            "2,364 that end within 100 m of their start, 20 over 3 hours (not closed in the app) and 19 faster than "
            "120 km/h in a straight line; replace random-row evaluation with chronological windows and lag the "
            "weather by 3 hours."
        ),
        fit="approximate",
        fit_reason=(
            "No routing-engine route or ETA ships, so the estimate rests on geometry, time and weather alone. "
            "Recorded destination and straight-line distance stand in for the planned route endpoints. "
            "Their capture time and weather publication latency are undocumented, and the weather clock is only "
            "inferred from the data. The sample "
            "year conflicts with its description, and only a participant copy was accessible."
        ),
    )
    unique_name = "2024_lusaka_mobility_prediction_hackathon"
    domain = "industry & manufacturing"
    sources = (
        Source(
            role="publication",
            platform="Zindi",
            url="https://zindi.world/competitions/2024-lusaka-mobility-prediction-hackathon",
            license="Zindi Competition Rules (Yango private property)",
            year="2024",
            bibtex=r"""
                @misc{yango2024lusaka,
                  author = {{Yango} and {Zindi}},
                  title = {2024 Lusaka Mobility Prediction Hackathon},
                  year = {2024},
                  howpublished = {\url{https://zindi.world/competitions/2024-lusaka-mobility-prediction-hackathon}},
                  note = {Trip-duration competition; participant download copy pinned separately}
                }
            """,
        ),
    )
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
    curation_comments = """
        We start with Train.csv and Lusaka_weather.csv from the participant mirror pinned in download_description.

        - Prediction point: trip start, to estimate minutes to the destination. Actual traveled distance is removed because it is measured over the completed trip. The inspected participant-copy starter includes it; that is not evidence it exists at departure (USE-3, LEAK-10).
        - Endpoint approximation: the source says endpoint coordinates are geomasked and straight-line distance uses the original points. It does not state when the destination was captured. Recorded destination and straight-line distance stand in for the requested destination, as in the NYC taxi precedent; direct prospective availability is not certified. The recorded end means two things: in some trips the realised drop-off (the round trips dropped below), in others a requested destination the rider did not reach (1,756 kept trips, 1.6%, drove under 0.9 times the straight line, 290 under 0.5 times). Where it is the drop-off, the destination and `str_distance_km` carry some post-trip location. These rows stay: a filter on the driven distance would select rows on the outcome (USE-3, LEAK-1). No routing-engine route or ETA ships (USE-8).
        - Cohort and provenance: the source describes January 2024, while the pinned trip timestamps run from 2023-01-01 to early 2023-02-01 and the weather and inspected participant-copy starter notebook identify January 2023. We preserve the supplied dates and publication year 2024; no calendar shift or original-byte equality is asserted. Only labeled Train.csv is used; competition test labels are not available.
        - Rows: drop the 21 missing start timestamps, which cannot be assigned honestly to chronological windows. The source already removed very short trips using an unspecified threshold; that selection cannot be undone.
        - We drop the 2,364 trips (2.1% of the 112,739 with a start; 1.3 to 2.9% on every day) whose straight-line distance from start to end is under 0.1 km (Lennart, 2026-11-04: "drop them, this is not a relevant prediction goal here imo"; USE-7, the 100 m radius of nyc_taxi_trip_duration_1m and pkdd_15_taxi_trip_time_prediction_ii_1m): nobody books a ride to their own pickup point, so these rows lack the destination the ETA acts on. The cut is on the recorded endpoint, which for these rows is not a booked destination, not on the target, and exact although the coordinates are masked, because the source computes `str_distance_km` from the original points. These trips are not short: median 22.1 minutes against 10.8 for the others, 93% over 5 minutes, median travelled distance 4.5 km (round trips), and they held 16% of the target's squared spread. 110,375 trips remained after this cut, with complete positive targets.
        - Features: drop trip_id and the duplicate day-only start column. Keep coordinates and straight-line kilometers numeric; no route-distance or speed feature is calculated. Durations are kept as published; the two cuts below drop rows, they change no value.
        - CC (2026-11-05, Lennart): drop the 20 trips over 3 hours as not closed in the app (issue 4, B; CLEAN-11, then CLEAN-15; as pkdd_15_taxi_trip_time_prediction_ii_1m's meter left running, `MAX_TRAVEL_TIME_S`, and nyc_taxi_trip_duration_1m's 3 h cap). The longest lasted 788 minutes for 20.2 km driven and 1.1 km in a straight line (1.5 km/h), and two ran at 0.3 km/h for 240 and 304 minutes. The source does not say how a trip is closed, so the impossibility rests on these values. The 20 held 11.8% of the target's squared spread, and 8 were test rows: the 788-minute trip alone held 21% of a constant prediction's squared error in the window from 2023-01-25. The longest kept trip lasts 175 minutes.
        - CC (2026-11-05, Lennart): drop the 19 trips faster than 120 km/h in a straight line from start to end (issue 5, B; CLEAN-11, then CLEAN-15; as pkdd's GPS jumps, `MAX_STRAIGHT_LINE_KMH`). The source computes the straight line from the unmasked points, so the speed is exact and the duration or the endpoint is wrong: 10 exceed 150 km/h, the fastest 416 km/h (8.9 km in 1.3 minutes). sendy_logistics_challenge treats its fast legs by their late pickup mark, which shows in the inputs (the wait at the pickup): since 2026-11-05 it drops its legs of 60 s or less, which takes 723 of its 803 legs over 120 km/h, and the 80 longer ones stay; here neither these trips nor the unclosed ones leave a mark in the inputs. They held under 0.1% of the squared spread; 4 were test rows. The two cuts share no trip: 110,336 trips remain.
        - CC (2026-11-05, Lennart): a trip gets the exact hourly weather record stamped floor(trip_start) - 3 hours (issue 3, B; LEAK-10, EV-2: a measurement on the data outranks the dictionary). The dictionary calls both clocks local, but the weather's own daily curve fits UTC stamps (Lusaka is UTC+2): mean temperature is flat at stamps 02 to 04, rises 1.09 °C at 05, about 50 minutes before the 05:50 sunrise, and peaks at 12 to 13, solar noon on a local clock but the usual 14 to 15 on a UTC one; the trip file also spans a calendar month in UTC (02:03 local on 1 January to 02:09 local on 1 February). With the 3-hour lag the row is that of the hour before the start hour on a UTC clock and of 3 hours before on a local one, so it precedes the start either way. The lag costs no measured skill: each weather column alone scores about 0, and hourly trip pace correlates with precipitation between -0.019 and 0.023 at every shift from -4 to +4 hours. It is not a verified publication delay. The 175 trips that start on 1 January before 03:00 have no weather row that early and keep missing weather; no future fill or date/year correction is used. The weather's row counter/date/time are join metadata, not predictors; precipitation type is categorical.
        - Metric: source RMSE on actual minutes, with identity target transform (MET-4). No logarithm is introduced, and the only rows cut on the target are the impossible ones above. The score still leans on a few rows (MET-2): the largest 1% of an untuned LightGBM's errors hold 43 to 53% of its squared error, and trips over 120 minutes hold 7.9%, 6.3% and 12.0% of the squared deviation of the windows from 2023-01-21, 2023-01-25 and 2023-01-29 (one fit per window, 3 windows); no single trip holds over 2% of a window's constant-prediction squared error.
        - CC (2026-11-05, Lennart): the declared metric (RMSE on minutes, the source's) is checked and stays as declared.
        - Split: chronological four-day windows with a one-day training gap. Every kept trip lasts at most 3 hours (the longest 175 minutes), so the gap puts observed training trip ends before refit; reporting delay beyond trip completion is not known. The participant copy's train/test files interpolate throughout the same month; our evaluation instead tests later trips.
        - Curator decision (2026-10-29, Myunghwan): "approximate version is fine." Accept the documented endpoint and earlier-hour weather stand-ins; capture/publication and reporting timing remain unverified rather than certified by acceptance.
        - Source/calendar decision (2026-10-29, Myunghwan): "if timestamps between trips and weather algined, it's ok. this is the source we have to live with." The supplied trip/weather calendars align in 2023, with an exact preceding-hour match for 110,352 of the kept rides and 23 out-of-coverage rides retaining missing weather (superseded 2026-11-05: with the 3-hour lag and the two cuts, 110,161 of the 110,336 rides have a weather row; the 175 without one start on 1 January before 03:00). Preserve the supplied dates and identified participant copy; organizer-original equality, actual timezone and the reason for the 2024 narrative remain unverified.
        - Scope: one released city/month, with masked locations and uncertain endpoint timing. The last test period has a partial final day because the file ends early February 1; this does not establish all-season, other-city or complete four-day deployment performance.
    """
    target = "Target"
    problem_type = "regression"
    metric = Metric.source(
        "rmse",
        original="Root Mean Squared Error",
        reference="https://zindi.world/competitions/2024-lusaka-mobility-prediction-hackathon#evaluation",
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
        kept trip lasts at most 3 hours (the longest 175 minutes), so training trips finish before each
        test-start/refit time. Subsequent
        label reporting delay and original cohort extraction/follow-up timing are undocumented. A fourth
        earlier four-day window would violate the half-data training floor after this gap. The latest window ends
        February 2 but only has observations through early February 1. No performance was used to choose windows.
        The windows hold different weekday mixes (the one from January 25 has no Sunday); trips are shorter on all
        five Sundays (11.1 to 12.1 minutes on average, against 13.7 to 14.7 on other days), a weekly pattern, not
        drift.
        Missing starts, trips ending within 100 m of their start, trips over 3 hours and trips faster than 120 km/h in
        a straight line are excluded; other rows, target units and dates are preserved.
    """
    accepted_check_warnings = {}

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        folder = raw_dir / MIRROR_COMMIT
        return {"trips": pd.read_csv(folder / "Train.csv"), "weather": pd.read_csv(folder / "Lusaka_weather.csv")}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        trips = raw["trips"]
        keep = pd.Series(True, index=trips.index)
        for _, mask in _row_filters(trips):
            keep &= mask
        df = trips.loc[keep, [*COORDINATES, "str_distance_km", "Target"]].copy()
        df["trip_start"] = _trip_start(trips).loc[df.index]
        key = df["trip_start"].dt.floor("h") - pd.Timedelta(hours=WEATHER_LAG_HOURS)
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
        left = pd.Series(True, index=trips.index)
        steps = [{"rows dropped": "(labeled raw rows)", "dropped": 0, "left": len(trips)}]
        for reason, keep in _row_filters(trips):
            kept = left & keep
            steps.append({"rows dropped": reason, "dropped": int(left.sum() - kept.sum()), "left": int(kept.sum())})
            left = kept
        return [
            Decision(
                title="Rows dropped before the split",
                why=(
                    "A trip without a start cannot be placed in a window; one ending within 100 m of its start has no "
                    "destination a passenger would book; one over 3 hours was not closed in the app, and one faster "
                    "than 120 km/h in a straight line has a wrong duration or endpoint (both as pkdd). The two last "
                    "cuts share no trip."
                ),
                evidence=pd.DataFrame(steps),
            ),
            Decision(
                title="Source dates, weather 3 hours before the start hour, and the duration-label gap",
                why=(
                    "Dates are preserved despite the description's 2024 claim. The weather row is stamped 3 hours "
                    "before the start hour, earlier than the start on a local or a UTC clock; the one-day gap exceeds "
                    "the longest kept trip."
                ),
                evidence=pd.DataFrame(
                    {
                        "quantity": [
                            "first kept start",
                            "last kept start",
                            f"trips without a weather row {WEATHER_LAG_HOURS} h before the start hour",
                            "maximum trip minutes",
                            "gap minutes",
                        ],
                        "value": [
                            str(df.trip_start.min()),
                            str(df.trip_start.max()),
                            str(df.temperature_C.isna().sum()),
                            str(df.Target.max()),
                            "1440",
                        ],
                    }
                ),
            ),
        ]
