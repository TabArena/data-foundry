"""Curated dataset definition for `rain_in_australia` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from datetime import datetime, time
from pathlib import Path
from zoneinfo import ZoneInfo

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
    cast_dtypes,
    drop_columns,
)

# When BoM records each column of day D ("Notes to accompany Daily Weather Observations", IDCJDW0000).
RECORDED = {
    "MinTemp": "24 h to 9 am on D",
    "MaxTemp": "24 h from 9 am on D",
    "Evaporation": "24 h to 9 am on D",
    "Sunshine": "24 h to midnight on D",
    "WindGustSpeed": "24 h to midnight on D",
    "WindSpeed9am": "9 am on D",
    "WindSpeed3pm": "3 pm on D",
    "Humidity9am": "9 am on D",
    "Humidity3pm": "3 pm on D",
    "Pressure9am": "9 am on D",
    "Pressure3pm": "3 pm on D",
    "Cloud9am": "9 am on D",
    "Cloud3pm": "3 pm on D",
    "Temp9am": "9 am on D",
    "Temp3pm": "3 pm on D",
}

# The columns of day D recorded after the 9 am observation, inside the window of the label (rain from 9 am on D to
# 9 am on D+1). They are replaced by their values of D-1 at the same location.
AFTER_9AM = (
    "MaxTemp",
    "Sunshine",
    "WindGustDir",
    "WindGustSpeed",
    "WindDir3pm",
    "WindSpeed3pm",
    "Humidity3pm",
    "Pressure3pm",
    "Cloud3pm",
    "Temp3pm",
)

# The 9 am readings of the other locations that each row also reads, from the same date (CLEAN-19 as amended on
# 2026-10-26): a forecaster reads the weather upwind at 9 am.
NEIGHBOUR_READINGS = ("Rainfall", "Pressure9am", "Humidity9am")

# The time zone of each location (tz database), to tell whose 9 am comes before a row's own.
LOCATION_TIME_ZONES = {
    "Australia/Perth": ("Albany", "PearceRAAF", "Perth", "PerthAirport", "SalmonGums", "Walpole", "Witchcliffe"),
    "Australia/Darwin": ("AliceSprings", "Darwin", "Katherine", "Uluru"),
    "Australia/Adelaide": ("Adelaide", "MountGambier", "Nuriootpa", "Woomera"),
    "Australia/Brisbane": ("Brisbane", "Cairns", "GoldCoast", "Townsville"),
    "Australia/Sydney": (
        "Albury",
        "BadgerysCreek",
        "Cobar",
        "CoffsHarbour",
        "Moree",
        "Newcastle",
        "NorahHead",
        "Penrith",
        "Richmond",
        "Sydney",
        "SydneyAirport",
        "WaggaWagga",
        "Williamtown",
        "Wollongong",
        "Canberra",
        "Tuggeranong",
        "MountGinini",
    ),
    "Australia/Melbourne": (
        "Ballarat",
        "Bendigo",
        "Dartmoor",
        "Melbourne",
        "MelbourneAirport",
        "Mildura",
        "Nhil",
        "Portland",
        "Sale",
        "Watsonia",
    ),
    "Australia/Hobart": ("Hobart", "Launceston"),
    "Pacific/Norfolk": ("NorfolkIsland",),
}


def _utc_offsets_at_9am(dates: pd.DatetimeIndex, zone: str) -> tuple[np.ndarray, np.ndarray]:
    """The UTC offset (hours) of 9 am on each date in a time zone: by the clock (daylight saving) and by standard time."""
    tz = ZoneInfo(zone)
    nine = [datetime.combine(d.date(), time(9), tzinfo=tz) for d in dates]
    clock = np.array([t.utcoffset().total_seconds() / 3600 for t in nine])
    standard = np.array([(t.utcoffset() - t.dst()).total_seconds() / 3600 for t in nine])
    return clock, standard


def _known_locations(dates: pd.DatetimeIndex, locations: list[str], rows: pd.DataFrame) -> np.ndarray:
    """Rows x locations: whether the location's 9 am of the row's date is not later than the row's own 9 am.

    Checked under both clock and standard time, since BoM's notes do not say which a station's 9 am follows; a
    row's own location is excluded (its readings are its own columns).
    """
    zone = {loc: z for z, locs in LOCATION_TIME_ZONES.items() for loc in locs}
    assert set(locations) <= set(zone), set(locations) - set(zone)
    offsets = {z: _utc_offsets_at_9am(dates, z) for z in LOCATION_TIME_ZONES}
    clock = np.column_stack([offsets[zone[loc]][0] for loc in locations])
    standard = np.column_stack([offsets[zone[loc]][1] for loc in locations])
    d = dates.get_indexer(rows["Date"])
    own = pd.Index(locations).get_indexer(rows["Location"])
    # 9 am at M is not later than 9 am at L when M's UTC offset is at least L's
    known = (clock[d] >= clock[d, own][:, None]) & (standard[d] >= standard[d, own][:, None])
    known[np.arange(len(rows)), own] = False
    return known


def _neighbour_readings(observations: pd.DataFrame, rows: pd.DataFrame) -> pd.DataFrame:
    """For each row, the other locations' 9 am readings of its date (`<reading>_at_<Location>`), missing where that
    location's 9 am is later than the row's own or it has no reading. A location that never records a reading (four
    record no pressure) has no column for it.
    """
    locations = sorted(observations["Location"].unique())
    dates = pd.DatetimeIndex(sorted(observations["Date"].unique()))
    known = _known_locations(dates, locations, rows)
    d = dates.get_indexer(rows["Date"])
    wide = observations.pivot(index="Date", columns="Location", values=list(NEIGHBOUR_READINGS))
    columns = {}
    for reading in NEIGHBOUR_READINGS:
        values = np.where(known, wide[reading].reindex(index=dates, columns=locations).to_numpy()[d], np.nan)
        recorded = wide[reading].reindex(columns=locations).notna().any().to_numpy()
        columns.update({f"{reading}_at_{loc}": values[:, j] for j, loc in enumerate(locations) if recorded[j]})
    return pd.DataFrame(columns, index=rows.index)


class RainInAustralia(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will it rain more than 1 mm at this Australian weather location in the next 24 hours?",
        use_case=(
            "For example, each morning at 9 am a farmer or local forecaster estimates from a location's observations "
            "whether more than 1 mm of rain will fall there by 9 am the next day."
        ),
        row=(
            "One day at one of 49 Australian locations of the Bureau of Meteorology (its Daily Weather Observations "
            "pages, some combining several stations), November 2007 to January 2026 (264,562 location-days)."
        ),
        predicted="Whether more than 1 mm of rain falls in the 24 hours from 9 am that day (22% of days).",
        known=(
            "The 9 am observations (temperature, humidity, pressure, cloud, wind), the minimum temperature, rain and "
            "evaporation of the 24 hours to 9 am, the previous day's maximum temperature, sunshine, strongest gust "
            "and 3 pm observations, the location and the date, and the rain, pressure and humidity read at 9 am that "
            "day at the other locations whose 9 am comes no later."
        ),
        split=(
            "26 test windows of 14 days, one after the other from February 2025 to January 2026, newest first; "
            "each trains on every earlier day, as for a model refit every two weeks."
        ),
        changes=(
            "We replace the ten values recorded after 9 am by the previous day's, drop the rain amount behind the "
            "label, drop rows whose next record is more than a day later or that lack a label (8,076) or their own "
            "9 am rain reading (2,571), and add the other locations' 9 am rain, pressure and humidity of the day."
        ),
        fit="approximate",
        fit_reason=(
            "A forecast from the location's own observations, standing in for the forecast-informed decision: a "
            "forecaster would also have weather-model output, which the data lack. Every input is read by 9 am, the "
            "label covers the next 24 hours, and each window follows its training days, as in daily use."
        ),
    )

    # Dataset
    unique_name = "rain_in_australia"
    year = "2026"
    domain = "environmental science & climate"
    source = "GOV Website"  # the Bureau of Meteorology's Daily Weather Observations; we download rattle's compilation
    source_url = "https://www.bom.gov.au/climate/dwo/"
    license = (
        "Copyright Commonwealth of Australia, Bureau of Meteorology; used with the Bureau's permission (rattle "
        "documentation of weatherAUS); rattle package GPL (>= 2)"
    )
    data_tags = ("Spatial",)
    download_description = r"""
        We download weatherAUS.csv of the R package rattle (Graham Williams, Togaware), a compilation of the Bureau of
        Meteorology's Daily Weather Observations (https://www.bom.gov.au/climate/dwo/) and the source of the Kaggle dataset
        "Rain in Australia" (https://www.kaggle.com/datasets/jsphyg/weather-dataset-rattle-package, a snapshot that ends
        on 2017-06-25). The live file https://rattle.togaware.com/weatherAUS.csv grows with the Bureau of Meteorology's
        daily weather observations, so we pin the Internet Archive capture of 2026-10-05. It is byte-identical to our
        download of the live file on 2026-10-06 (last modified 2026-02-07, observations to 2026-01-30).

        mkdir -p local-data-warehouse/rain_in_australia
        wget -O local-data-warehouse/rain_in_australia/weatherAUS_20260207.csv \
          "https://web.archive.org/web/20261005005127id_/https://rattle.togaware.com/weatherAUS.csv"
        sha256sum local-data-warehouse/rain_in_australia/weatherAUS_20260207.csv
        # 6598e6857fb13aa46b3b41fec849f94e6884d30a7f8696455c433b9378b549fc

        A second permanent copy: the CRAN package rattle 5.6.2 (published 2026-02-08;
        https://cran.r-project.org/src/contrib/rattle_5.6.2.tar.gz, later under src/contrib/Archive/rattle/; sha256
        8b226e45f9438d5402214a0fb8374a15bc9fbefb3c2dffa2744eddbba7cd22fd). Its data/weatherAUS.RData holds the same
        275,410 x 24 values as the CSV (compared cell by cell with pyreadr); export it in R with
        write.csv(weatherAUS, "weatherAUS_20260207.csv", row.names = FALSE).
    """
    bibtex = r"""
        @book{williams2011rattle,
          title = {Data Mining with {Rattle} and {R}: The Art of Excavating Data for Knowledge Discovery},
          author = {Williams, Graham J.},
          publisher = {Springer},
          series = {Use R!},
          year = {2011},
          doi = {10.1007/978-1-4419-9890-3}
        }
        @misc{williams2026weatheraus,
          author = {Williams, Graham J.},
          title = {weatherAUS: Daily Weather Observations from Multiple Australian Weather Stations},
          year = {2026},
          howpublished = {\url{https://rattle.togaware.com/weatherAUS.csv}},
          note = {Dataset of the R package rattle (version of 2026-02-07, as in rattle 5.6.2); observations from the
            Australian Bureau of Meteorology}
        }
    """
    curation_comments = """
        We start with weatherAUS.csv of the R package rattle: daily observations of 49 Australian locations (BoM Daily
        Weather Observations pages, some combining several stations) from the Bureau of Meteorology (BoM), 2007-11-01
        to 2026-01-30, with the target RainTomorrow.

        - Prediction point: the 9 am observation at a location on day D. The model predicts whether more than 1 mm of
          rain falls by 9 am on D+1 (RainTomorrow), from the observations up to 9 am on D and those recorded on D-1.
        - BoM records rainfall "in the 24 hours to 9am" (BoM notes), so the label's window starts at 9 am on D, and ten
          columns of day D are recorded inside it: MaxTemp (the label's own 24 hours), Sunshine and the wind gust (to
          midnight) and the six 3 pm observations. Five of them are tied more closely to the label than to the rain
          read at 9 am on D (Sunshine ROC AUC 0.805 against 0.733; decision table). We replace the ten columns by their
          values of D-1 at the same location (`<column>_prev_day`, missing when the location has no row for D-1).
        - We drop RISK_MM, the label's rain amount: RainTomorrow is RISK_MM > 1 mm in every labelled row.
        - rattle takes RainTomorrow from the location's next row in the file, which before the periods missing from the
          file is 29-401 days later. We drop every row whose next row is more than one day later (decision table).
          The last row of each location keeps its label; it matches BoM's reading of the next day at the 7 locations
          checked.
        - We drop the rows without a label and the rows whose own 9 am rain reading is missing, since BoM's next value
          can then be "accumulated over several days rather than the normal one day" (decision table). Both kinds of
          dropped rows carry a label over 48 hours or more (42.6% rain days against 21.8%), another quantity than the
          24-hour call of the task (USE-5; CC 2026-10-26).
        - Rainfall and RainToday (Rainfall > 1 mm in every row) are the location's 9 am gauge reading on D, i.e. the
          label of D-1, known at the prediction point. They add 0.0027 ROC AUC on the 9 shipped windows (LightGBM,
          0.8495 with them, 0.8467 without; log loss 0.3516 against 0.3549), and the features without the location's
          rain series beat persistence and the location-by-month climatology in 9 of 9 windows, so the skill does not
          come from the lagged target. A forecast of the rain amount from the location's own rain series with a > 1 mm
          rule reaches ROC AUC 0.75 against 0.849 (9 of 9 windows). We keep both: the reading is the last observation,
          known at 9 am, and an input the forecaster has (TP-10 as amended 2026-10-26).
        - CLEAN-19 as amended (Lennart, 2026-10-26): each row also reads the other locations' 9 am Rainfall, Pressure9am
          and Humidity9am of the same day (`<reading>_at_<Location>`, 143 columns: four locations record no pressure), as a forecaster reads the weather
          upwind. A location counts only when its 9 am comes no later than the row's own, under both clock and standard
          time (`_known_locations`): Perth's 9 am is 11:00-11:30 in the east, so an eastern row cannot read it. A row
          reads 32 other locations on average (decision table); the rest are missing by construction. On the 9 windows
          shipped before (LightGBM, 400 trees) this lifts ROC AUC from 0.850 to 0.870 (paired SE 0.0045, better in 8 of 9).
        - The wind direction is blank in every row with a wind speed of 0; we set it to "Calm" there (WindDir9am,
          WindDir3pm before the lag; 15,003 and 1,609 rows of the cleaned data).
        - A relative humidity of 0% is impossible; we set it to missing (5 cells, all at Woomera).
        - `Location`, the wind directions and RainToday are categorical, `Date` a date.
        - Location stays a feature, and the split is temporal, not grouped by location: a model is used at the same
          locations on later days (splits comment).
        - Anomaly: the file has no rows for any location in 2011-04, 2012-12 and 2013-02, and from 2016-01-27 to
          2017-02-28.
        - Anomaly: Evaporation is a multi-day total after days without a reading, and Cloud9am and Cloud3pm hold 9 (sky
          obscured) in 3 rows. We keep the values as recorded.
        - Anomaly: missing Sunshine and Evaporation grow from 34-46% of the rows in 2009-2013 to 66-79% in 2017-2025.
        - Anomaly: a blank Cloud9am is mostly a clear or near-clear sky at the time of the observation, mixed with
          true gaps. Among the locations that record cloud, rain follows 11.7% of blank mornings against 24.7% of
          mornings with a reading, and the gap holds within RainToday x humidity strata. Days with a blank Cloud3pm have
          8.5 h of sunshine, against 10.5-11.2 h at 0-1 oktas and 4.8 h at 7 oktas, and the locations with the most
          blanks record almost no 0 oktas (Uluru 76% blank, 0.1% zeros). The blank is set at 9 am, so we keep it
          (effect 0.003 ROC AUC); a recode to 0 is not safe because true gaps are mixed in. Revisit if BoM states
          otherwise. rattle's cloud values also differ from current BoM pages at Melbourne and Hobart (a revision
          between versions).
        - Anomaly: paired locations (Perth and PerthAirport, Sydney and SydneyAirport, Melbourne and MelbourneAirport)
          share Sunshine on 100% of their shared days. The split is unaffected, since a date is never on both sides.
        - Anomaly: in 2,648 kept rows the location's previous reading or row is missing, so Rainfall and RainToday may
          be a total over several days (RainToday 40.6% against 21.8%). We keep them, as known at 9 am.
        - Note: BoM's terms allow personal and in-house use; the rattle documentation records the Bureau's permission to
          use the data with BoM acknowledged as the source.
    """

    # Task
    target = "RainTomorrow"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "The data is a Kaggle dataset / rattle example file built from BoM observations with no task "
            "description or metric; no paper defines one. Binary fallback roc_auc."
        ),
    )

    # Splits
    temporal = Temporal(on="Date", splits=TemporalSplits(window=14, unit="days", n_windows=26))
    splits_comment = """
        Weather models are refit often (one to two weeks, the horizon the curators set for
        climate_model_weather_forecasting), so a model is refit and then used every morning for 14 days. 26 test windows
        of 14 days, one after the other from 2025-02-01 to 2026-01-30, newest first, so that the windows cover every
        season of the last year (6-7 per season); train is every earlier day (from 2007-11-01), at least 93.8% of the
        rows. Each window holds 619-642 location-days with 63-222 rain days, 16,457 test rows in all. The window AUCs
        vary as much as the earlier 9 windows' (standard deviation 0.04-0.05), so the count of windows sets how steady
        the mean is: its standard error is 0.008 against 0.016 for 9 windows spaced six weeks apart (LightGBM; the
        correlation of neighbouring windows, 0.24, makes it about 0.010) (CC 2026-10-26). No gap: the label of the last
        training day is read at 9 am on the first test day, before the first prediction. The history has a break (no
        rows from 2016-01-27 to 2017-02-28) and Sunshine and Evaporation are missing far more often after it; training
        from 2017-03 gives ROC AUC 0.842 against 0.847 with the full history, so the old years do no harm.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "weatherAUS_20260207.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = cast_dtypes(raw, datetime={"Date": "%Y-%m-%d"})  # the lag below needs the dates
        # A blank direction at a speed of 0 is a calm wind; RH 0% is impossible (Woomera only).
        for direction, speed in (("WindDir9am", "WindSpeed9am"), ("WindDir3pm", "WindSpeed3pm")):
            df[direction] = df[direction].mask(df[speed].eq(0), "Calm")
        for humidity in ("Humidity9am", "Humidity3pm"):
            df[humidity] = df[humidity].mask(df[humidity].eq(0))
        # Every location's 9 am readings, before any row is dropped: the other locations read them (below).
        observations = df[["Location", "Date", *NEIGHBOUR_READINGS]]
        # The columns recorded after 9 am on D, replaced by their values of D-1 at the same location.
        keys = ["Location", "Date"]
        previous = df[[*keys, *AFTER_9AM]].assign(Date=df["Date"] + pd.Timedelta(days=1))
        previous = previous.rename(columns={c: f"{c}_prev_day" for c in AFTER_9AM})
        df = df.merge(previous, on=keys, how="left", validate="one_to_one")
        # RISK_MM is the label's rain amount.
        df = drop_columns(df, [*AFTER_9AM, "RISK_MM"])
        # rattle takes RainTomorrow from the station's next row in the file; before a period missing from the file
        # that row is 29-401 days later. The station's last row (no next row) keeps its label.
        df = df.sort_values(keys, kind="stable")
        next_row_gap = df.groupby("Location", sort=False)["Date"].shift(-1) - df["Date"]
        df = df[~(next_row_gap > pd.Timedelta(days=1))]
        # No label, or no 9 am reading on D (the next reading may then cover several days).
        df = df[df["RainTomorrow"].notna() & df["Rainfall"].notna()]
        # The other locations' 9 am readings of the same day whose 9 am comes no later than the row's own.
        return pd.concat([df, _neighbour_readings(observations, df)], axis=1)

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["Location", "WindDir9am", "RainToday", "WindGustDir_prev_day", "WindDir3pm_prev_day"],
            datetime={"Date": "%Y-%m-%d"},
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        from sklearn.metrics import roc_auc_score

        def auc(feature: pd.Series, label: pd.Series) -> float:
            known = feature.notna() & label.notna()
            score = roc_auc_score(label[known] == "Yes", feature[known])
            return round(max(score, 1 - score), 3)

        windows = pd.DataFrame(
            {
                "recorded": RECORDED,
                "ROC AUC for rain to 9 am on D (RainToday)": {c: auc(raw[c], raw["RainToday"]) for c in RECORDED},
                "ROC AUC for rain to 9 am on D+1 (label)": {c: auc(raw[c], raw["RainTomorrow"]) for c in RECORDED},
            }
        )
        windows["replaced by D-1"] = windows.index.isin(AFTER_9AM)

        labelled = raw[raw["RainTomorrow"].notna()]
        reading = (
            labelled["Rainfall"].isna().map({False: "9 am reading on D present", True: "9 am reading on D missing"})
        )
        accumulated = labelled.groupby(reading).agg(
            rows=("RainTomorrow", "size"),
            rain_days=("RainTomorrow", lambda y: f"{(y == 'Yes').mean():.1%}"),
            next_reading_median_mm=("RISK_MM", "median"),
            next_reading_p75_mm=("RISK_MM", lambda r: r.quantile(0.75)),
        )

        # Labels taken across a period missing from the file: the next row of the station is more than a day later.
        stations = raw.assign(Date=pd.to_datetime(raw["Date"])).sort_values(["Location", "Date"], kind="stable")
        by_station = stations.groupby("Location", sort=False)
        stations = stations.assign(
            next_row_days=(by_station["Date"].shift(-1) - stations["Date"]).dt.days,
            next_row_rainfall=by_station["Rainfall"].shift(-1),
        )
        across = stations[(stations["next_row_days"] > 1) & stations["RainTomorrow"].notna()]
        across_gap = across.groupby(across["Date"].dt.date).agg(
            stations=("Location", "size"),
            days_to_next_row=("next_row_days", lambda d: f"{d.min():.0f}-{d.max():.0f}"),
            RISK_MM_equals_next_row_rainfall=(
                "RISK_MM",
                lambda r: f"{(r == across.loc[r.index, 'next_row_rainfall']).sum()} of {len(r)}",
            ),
        )

        options = {
            "14 days, contiguous, 26 windows (shipped)": self.temporal.splits,
            "14 days, every 6 weeks, 9 windows": TemporalSplits(window=14, unit="days", n_windows=9, step=42),
            "14 days, every 3 weeks, 18 windows": TemporalSplits(window=14, unit="days", n_windows=18, step=21),
            "7 days, every 6 weeks": TemporalSplits(window=7, unit="days", n_windows=9, step=42),
            "1 month, contiguous": TemporalSplits(window=1, unit="months", n_windows=9),
            "12 months (train >= 50%)": TemporalSplits(window=12, unit="months", n_windows=9, min_train_fraction=0.5),
        }
        rows = {}
        for name, option in options.items():
            tests = [test for folds in option.splits(df, "Date").values() for _, test in folds.values()]
            rain = [int((df["RainTomorrow"].iloc[test] == "Yes").sum()) for test in tests]
            rows[name] = {
                "windows": len(tests),
                "first test day": df["Date"].iloc[min(min(test) for test in tests)].date(),
                "test rows": f"{min(map(len, tests)):,}-{max(map(len, tests)):,}",
                "rain days": f"{min(rain):,}-{max(rain):,}",
            }
        # The other locations a row reads, by the time zone of the row's location
        zone = {loc: z for z, locs in LOCATION_TIME_ZONES.items() for loc in locs}
        reads = df[[c for c in df.columns if c.startswith("Rainfall_at_")]].notna().sum(axis=1)
        neighbours = (
            reads.groupby(df["Location"].map(zone).rename("time zone of the row"))
            .agg(rows="size", mean_other_locations_read="mean")
            .round(1)
        )

        return [
            Decision(
                "Ten columns of day D are recorded inside the label's window and replaced by their values of D-1",
                "BoM reads the rain gauge at 9 am, so RainTomorrow covers 9 am on D to 9 am on D+1. Sunshine, the wind "
                "gust and the 3 pm humidity, cloud and pressure are tied more closely to that window than to the rain "
                "read at 9 am on D, and MaxTemp covers the same 24 hours as the label. At the prediction point (9 am "
                "on D) only their values of D-1 are known.",
                windows,
            ),
            Decision(
                "Rows labelled from a reading weeks or months later are dropped",
                "rattle takes RainTomorrow and RISK_MM from the station's next row in the file. Before the periods "
                "missing from the file that row is 29-401 days later, and RISK_MM equals its rainfall.",
                across_gap,
            ),
            Decision(
                "Rows whose own 9 am rain reading is missing are dropped",
                "BoM: after a missing reading the next value can be accumulated over several days, so the label of "
                "these rows can cover more than 24 hours.",
                accumulated,
            ),
            Decision(
                "26 two-week test windows, one after the other over the last year",
                "The source gives no refit cadence; for weather the curators set one to two weeks "
                "(climate_model_weather_forecasting). 26 contiguous two-week windows cover every season of the last "
                "year with three times the test rows of 9 windows spaced six weeks apart, which halves the standard "
                "error of the mean score (CC 2026-10-26).",
                pd.DataFrame(rows).T,
            ),
            Decision(
                "The other locations' 9 am readings a row reads",
                "Rainfall, Pressure9am and Humidity9am of the same day at every other location whose 9 am comes no later "
                "than the row's own, under both clock and standard time; a later location is missing. A western row "
                "reads every other location, an eastern one only those east of it or in its own zone. Rows by the time "
                "zone of their location, and the mean number of other locations with a 9 am rain reading they read.",
                neighbours,
            ),
        ]
