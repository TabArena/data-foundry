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


class LusakaMobility2024(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How many minutes will an individual Yango trip in Lusaka take?",
        use_case=(
            "At trip start, a ride-hailing app estimates travel time to inform the passenger. "
            "A model is refit every four days using completed earlier trips."
        ),
        row=(
            "One labeled trip from the 2024 Lusaka challenge's participant mirror: 112,739 trips with start times. "
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
            "Remove actual traveled distance, trip ID and duplicate date; exclude 21 trips without start times; "
            "replace random-row evaluation with chronological windows and use earlier-hour weather."
        ),
        fit="approximate",
        fit_reason=(
            "Recorded destination and straight-line distance stand in for the planned route endpoints. "
            "Their capture time and weather publication latency are undocumented. The sample year conflicts "
            "with its description, and only a participant copy was accessible."
        ),
    )
    unique_name = "2024_lusaka_mobility_prediction_hackathon"
    year = "2024"
    domain = "technology & internet"
    source = "Zindi"
    source_url = "https://zindi.world/competitions/2024-lusaka-mobility-prediction-hackathon"
    license = "Zindi Competition Rules (Yango private property)"
    data_tags = ("Spatial", "Anonymized")
    download_description = """
        The first publisher is Yango's 2024 Lusaka challenge on Zindi. Original downloads require access unavailable
        to this session. We use the public participant copy Mwandamena/yango-hackathon, pinned at commit
        2fa7817be0740ea1739143ea6e61a28d6cf1462d. Its training, test, weather and submission byte lengths match the
        organizer listing; full original byte identity is unverified. Only Train.csv and Lusaka_weather.csv are read.

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
        - Endpoint approximation: the source says endpoint coordinates are geomasked and straight-line distance uses the original points. It does not state when the destination was captured. Recorded destination and straight-line distance stand in for the requested destination, as in the NYC taxi precedent; direct prospective availability is not certified.
        - Cohort and provenance: the source describes January 2024, while the pinned trip timestamps run from 2023-01-01 to early 2023-02-01 and the weather and inspected participant-copy starter notebook identify January 2023. We preserve the supplied dates and publication year 2024; no calendar shift or original-byte equality is asserted. Only labeled Train.csv is used; competition test labels are not available.
        - Rows: drop only the 21 missing start timestamps, which cannot be assigned honestly to chronological windows. The remaining 112,739 trips have complete positive targets. The source already removed very short trips using an unspecified threshold; that selection cannot be undone.
        - Features: drop trip_id and the duplicate day-only start column. Keep coordinates and straight-line kilometers numeric; no route-distance or speed feature is calculated. Keep zero straight-line distance and all durations, including long rides, because neither the source nor the inspected values proves they are errors.
        - Weather: map the exact hourly record at floor(trip_start)-1 hour, never the current-hour record. This is a conservative lag on supplied hourly measurements, not a verified publication delay. No future fill or date/year correction is used. The weather's row counter/date/time are join metadata, not predictors; precipitation type is categorical. Missing earlier weather remains missing.
        - Metric: source RMSE on actual minutes, with identity target transform. No target-based filtering or logarithm is introduced.
        - Split: chronological four-day windows with a one-day training gap. Every observed duration is under one day, so the gap puts observed training trip ends before refit; reporting delay beyond trip completion is not known. The participant copy's train/test files interpolate throughout the same month; our evaluation instead tests later trips.
        - Curator decision (2026-10-29, Myunghwan): "approximate version is fine." Accept the documented endpoint and earlier-hour weather stand-ins; capture/publication and reporting timing remain unverified rather than certified by acceptance.
        - Source/calendar decision (2026-10-29, Myunghwan): "if timestamps between trips and weather algined, it's ok. this is the source we have to live with." The supplied trip/weather calendars align in 2023, with an exact preceding-hour match for 112,716 rides and 23 out-of-coverage rides retaining missing weather. Preserve the supplied dates and identified participant copy; organizer-original equality, actual timezone and the reason for the 2024 narrative remain unverified.
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
        Missing starts are excluded; other rows, target units and dates are preserved.
    """
    accepted_check_warnings = {}

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        folder = raw_dir / MIRROR_COMMIT
        return {"trips": pd.read_csv(folder / "Train.csv"), "weather": pd.read_csv(folder / "Lusaka_weather.csv")}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        trips = raw["trips"]
        start = pd.to_datetime(trips["lcl_start_transporting_dttm"], format="ISO8601", errors="coerce")
        df = trips.loc[start.notna(), [*COORDINATES, "str_distance_km", "Target"]].copy()
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
        return [
            Decision(
                title="Source dates and chronological row eligibility",
                why="Dates are preserved despite the description's 2024 claim; missing starts cannot support temporal tests.",
                evidence=pd.DataFrame(
                    {
                        "quantity": [
                            "labeled raw rows",
                            "kept rows",
                            "missing start",
                            "recorded minimum",
                            "recorded maximum",
                        ],
                        "value": [
                            str(len(trips)),
                            str(len(df)),
                            str(len(trips) - len(df)),
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
