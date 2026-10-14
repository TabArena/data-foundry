"""Curated dataset definition for `bias_correction_r_bias_correction_r_2` (data-foundry v2). Evidence: README.md."""

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

RAW_FILE = "Bias_correction_ucl.csv"

# The LDAPS forecast of each target (lapse-rate corrected to the station's elevation, Cho et al. 2020, Sec. 3.1) and
# the observed value of the present day that matches it.
FORECAST = {"Next_Tmin": "LDAPS_Tmin_lapse", "Next_Tmax": "LDAPS_Tmax_lapse"}
PRESENT = {"Next_Tmin": "Present_Tmin", "Next_Tmax": "Present_Tmax"}


def _station_mos(past: pd.DataFrame, future: pd.DataFrame, target: str, inputs: list[str]) -> np.ndarray:
    """Model output statistics per station: least squares of the target on ``inputs`` and an intercept, fitted on
    ``past``. A row missing an input gets its station's fit on the forecast alone (``inputs[0]``), and a row without a
    forecast its station's mean target. ``future`` has a RangeIndex.
    """
    prediction = np.full(len(future), np.nan)
    for station in future["station"].unique():
        rows = (future["station"] == station).to_numpy()
        history = past[past["station"] == station]
        for columns in (inputs, inputs[:1]):
            fit = history.dropna(subset=[*columns, target])
            coef = np.linalg.lstsq(np.c_[np.ones(len(fit)), fit[columns]], fit[target], rcond=None)[0]
            todo = rows & future[columns].notna().all(axis=1).to_numpy() & np.isnan(prediction)
            prediction[todo] = np.c_[np.ones(todo.sum()), future.loc[todo, columns]] @ coef
        prediction[rows & np.isnan(prediction)] = history[target].mean()
    return prediction


class BiasCorrectionRBiasCorrectionR2(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What will tomorrow's lowest air temperature be at a Seoul weather station?",
        use_case=(
            "Each evening, once the Korea Meteorological Administration's regional model run of 9 pm is out, a "
            "forecaster corrects the model's forecast of the next day's minimum temperature for each station's local "
            "bias (Cho et al. 2020)."
        ),
        row=(
            "One station on one summer day: 25 automatic weather stations in Seoul, June 30 to August 30 of each year"
            " 2013-2017."
        ),
        predicted="The station's minimum air temperature on the next day, in degrees Celsius.",
        known=(
            "The station with its location, elevation and slope, the day's incoming solar radiation, the highest and "
            "lowest temperatures observed that day up to 9 pm, and the model's forecasts for the next day "
            "(temperature, humidity, wind, latent heat, cloud cover, rain)."
        ),
        split=(
            "Nine test weeks cover the last summer (2017-06-30 to 2017-08-30); each trains on every earlier "
            "station-day up to one day before the week, as for a correction refit weekly."
        ),
        changes=(
            "We keep one of the two targets, the next day's minimum, and drop the maximum, observed after the "
            "prediction point; we split by date instead of at random, as the stations of one day share its weather."
        ),
        fit="direct",
        fit_reason=(
            "Everything the model sees is out by the evening, and each test week follows its training days as in "
            "operation. The task is narrow: 25 stations of one city, summers only."
        ),
    )

    # Dataset
    unique_name = "bias_correction_r_bias_correction_r_2"
    year = "2020"
    domain = "environmental science & climate"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C59K76"
    license = "CC BY 4.0"
    data_tags = ("Spatial",)
    download_description = """
        We download the static zip of UCI dataset 514 (donated on 2020-02-17). It holds one file, Bias_correction_ucl.csv
        (sha256 c60150c3e0c80b7bbb9e96eed7458404e1745327899d4b351462987109cbf5ea; the zip of 2026-10-07 has sha256
        822659f0ed1e778c331a1f0b1db2bd21745ee476153fa93ef9c8e1b720938bb6).

        mkdir -p local-data-warehouse/bias_correction_r_bias_correction_r_2
        wget -O local-data-warehouse/bias_correction_r_bias_correction_r_2/bias_correction.zip "https://archive.ics.uci.edu/static/public/514/bias+correction+of+numerical+prediction+model+temperature+forecast.zip"
        unzip local-data-warehouse/bias_correction_r_bias_correction_r_2/bias_correction.zip -d local-data-warehouse/bias_correction_r_bias_correction_r_2/
    """
    bibtex = """
        @article{cho2020comparative,
          title = {Comparative Assessment of Various Machine Learning-Based Bias Correction Methods for Numerical Weather
            Prediction Model Forecasts of Extreme Air Temperatures in Urban Areas},
          author = {Cho, Dongjin and Yoo, Cheolhee and Im, Jungho and Cha, Dong-Hyun},
          journal = {Earth and Space Science},
          volume = {7},
          number = {4},
          pages = {e2019EA000740},
          year = {2020},
          doi = {10.1029/2019EA000740}
        }
        @misc{uci2020biascorrection,
          title = {Bias correction of numerical prediction model temperature forecast},
          year = {2020},
          howpublished = {UCI Machine Learning Repository},
          doi = {10.24432/C59K76}
        }
    """
    curation_comments = """
        We start with Bias_correction_ucl.csv from UCI (dataset 514): 7,750 station-days of 25 automatic weather
        stations (AWS) of the Korea Meteorological Administration (KMA) in Seoul, June 30 to August 30 of each year
        2013-2017. Each row holds 14 next-day forecasts of KMA's LDAPS model, the day's observed extremes and two
        targets, the next day's minimum (`Next_Tmin`) and maximum (`Next_Tmax`) air temperature.

        - Prediction point: the evening of the present day (`Date`), once the LDAPS run of 21 KST is out; the
          present-day extremes cover 0-21 KST (Cho et al. 2020, Sec. 2.2-2.3). The model corrects the bias of the LDAPS
          forecast of the next day's minimum at the station.
        - One target, `Next_Tmin`: the v2 task holds one target. For the minimum, the mean of untuned CatBoost, LightGBM
          and ridge beats the standard correction, model output statistics (MOS) fitted per station, on 7 of 9 windows;
          for the maximum, MOS beats every untuned model (decision table). We drop `Next_Tmax`: it is observed on the
          next day, after the prediction point.
        - Temporal split, not random: the 25 stations of a day share its weather, and only 17.5% of the variance of
          `Next_Tmin` lies within a day: untuned LightGBM reaches RMSE 0.62 with random folds and 1.00 when each day's
          stations stay on one side (decision table). The paper also validates by hindcast on all earlier days (Sec.
          3.3).
        - `station` stays a feature (category): the same 25 stations report every day, and the model serves them on
          later days. The paper's leave-one-station-out test (Sec. 4.3) asks a secondary question.
        - We drop the last two rows of the file: they have no station and no date and hold the minimum and the maximum
          of every column.
        - We drop the 27 rows without a target (both targets are missing together).
        - We keep missing features as missing (the LDAPS forecasts of all stations on three days, the observed extremes
          of 60 other station-days): at prediction time a station or a model run can fail.
        - Note: the targets are the AWS daily extremes, the present-day columns the extremes of hourly readings up to 21
          KST (Sec. 2.3). So a row's label is close to, and mostly below, the next day's `Present_Tmin` at the station,
          a value known only on the next day (decision table).
        - Note: the task probes flag no_spread and unstable; we keep the task. The best family beats the training mean
          on 9 of 9 windows, the skill varies with the training mean's error between weeks, and a window of 6-7 days
          separates strong methods little. Once tuned results exist, check that tuned single models beat the per-station
          MOS.
        - Anomaly: UCI and the paper's Table 1 give `LDAPS_CC1`-`LDAPS_CC4` (cloud cover) and `LDAPS_PPT1`-`LDAPS_PPT4`
          (precipitation) in "%", but the cloud covers lie between 0 and 0.98. We keep the values as published.
        - Note: the paper scores with R^2, bias and RMSE (Sec. 3.3); we keep the default RMSE.
    """

    # Task
    target = "Next_Tmin"
    problem_type = "regression"

    # Splits
    temporal = Temporal(on="Date", splits=TemporalSplits(window=7, unit="days", n_windows=9, gap=1))
    splits_comment = (
        "Weather models are refit often (one to two weeks at most, as the curators argue for "
        "climate_model_weather_forecasting), so a bias-correction model is refit and then used every evening for 7 days. "
        "9 test windows of 7 days walk back from 2017-08-30, newest first, and cover the whole last summer (2017-06-30 to "
        "2017-08-30; the oldest window holds 6 days). Train is every earlier station-day from 2013-06-30 up to a gap of 1 "
        "day: the label of the day before a window is the minimum of the window's first day, which is complete only at "
        "midnight, after the first prediction that evening. Each window holds 149-175 station-days (6-7 days of the 25 "
        "stations), and the oldest trains on the four summers 2013-2016. The 9 windows are the 3 x 3 splits of the v2 "
        "protocol for this size; the paper's own hindcast refits every day (Cho et al. 2020, Sec. 3.3)."
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / RAW_FILE)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # The last two rows of the file hold the column minimum and maximum, without station or date.
        df = raw[raw["station"].notna()].copy()
        df["station"] = df["station"].astype(int)
        # The second target is observed on the next day, after the prediction point.
        df = drop_columns(df, ["Next_Tmax"])
        return df[df[self.target].notna()]

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["station"], datetime={"Date": "%Y-%m-%d"})

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        days = raw[raw["station"].notna()].assign(Date=lambda d: pd.to_datetime(d["Date"], format="%Y-%m-%d"))

        # How much of each target's variance lies within a day, across the 25 stations.
        spread = {}
        for target in FORECAST:
            labelled = days[days[target].notna()]
            by_day = labelled.groupby("Date")[target]
            spread[target] = {
                "standard deviation": round(labelled[target].std(), 2),
                "mean within-day standard deviation (25 stations)": round(by_day.std().mean(), 2),
                "standard deviation of the daily means": round(by_day.mean().std(), 2),
                "share of the variance within days": round(
                    (labelled[target] - by_day.transform("mean")).var() / labelled[target].var(), 3
                ),
            }

        # The raw LDAPS forecast of each target and three corrections fitted per station on the train side (the mean
        # error; MOS on the forecast; MOS on the forecast and the present-day extreme), scored on the shipped windows
        # (the same rows for both targets: the two are missing together).
        frame = days[days[self.target].notna()].sort_values("Date", kind="stable").reset_index(drop=True)
        windows = [folds[0] for folds in self.temporal.splits.splits(frame, "Date").values()]
        corrections = {}
        for target, forecast in FORECAST.items():
            scores: dict[str, list[float]] = {}
            for train, test in windows:
                past, future = frame.iloc[train], frame.iloc[test].reset_index(drop=True)
                offset = (past[forecast] - past[target]).groupby(past["station"]).mean()
                predictions = {
                    "raw forecast": future[forecast].to_numpy(),
                    "forecast minus the station's mean error": (
                        future[forecast] - future["station"].map(offset)
                    ).to_numpy(),
                    "per-station MOS on the forecast": _station_mos(past, future, target, [forecast]),
                    "per-station MOS on forecast and present extreme": _station_mos(
                        past, future, target, [forecast, PRESENT[target]]
                    ),
                }
                for name, prediction in predictions.items():
                    rmse = float(np.sqrt(np.nanmean((prediction - future[target].to_numpy()) ** 2)))
                    scores.setdefault(name, []).append(rmse)
            error = (days[forecast] - days[target]).dropna()
            corrections[target] = {
                "bias of the raw forecast, 2013-2017": round(error.mean(), 2),
                "RMSE of the raw forecast, 2013-2017": round(float(np.sqrt((error**2).mean())), 2),
                **{f"mean RMSE, 9 windows: {name}": round(float(np.mean(s)), 3) for name, s in scores.items()},
            }

        # A row's target against the next day's present-day value at the same station.
        next_day = days[["station", "Date", *PRESENT.values()]].assign(Date=lambda d: d["Date"] - pd.Timedelta(days=1))
        pairs = days.merge(next_day, on=["station", "Date"], how="left", suffixes=("", "_next_day"))
        measured = {}
        for target, present in PRESENT.items():
            difference = (pairs[target] - pairs[f"{present}_next_day"]).dropna().round(1)
            measured[f"{target} - next day's {present}"] = {
                "pairs": len(difference),
                "above": f"{(difference > 0).mean():.1%}",
                "equal": f"{(difference == 0).mean():.1%}",
                "below": f"{(difference < 0).mean():.1%}",
                "mean (degrees C)": round(difference.mean(), 2),
            }

        two_summers = ("2017-08-17", "2017-08-03", "2017-07-20", "2017-07-06", "2017-06-22")
        two_summers += ("2016-08-17", "2016-08-03", "2016-07-20", "2016-07-06")
        options = {
            "7 days x 9, gap 1 day (shipped)": self.temporal.splits,
            "7 days x 9, no gap": TemporalSplits(window=7, unit="days", n_windows=9),
            "14 days x 9 walking back, gap 1 day": TemporalSplits(window=14, unit="days", n_windows=9, gap=1),
            "14 days x 9, cutoffs in 2016 and 2017, gap 1 day": TemporalSplits(
                window=14, unit="days", gap=1, cutoffs=two_summers
            ),
        }
        sizes = {}
        for name, option in options.items():
            splits = [folds[0] for folds in option.splits(df, "Date").values()]
            sizes[name] = {
                "windows": len(splits),
                "first test day": df["Date"].iloc[min(min(test) for _, test in splits)].date(),
                "test days": sum(df["Date"].iloc[test].nunique() for _, test in splits),
                "test rows": f"{min(len(test) for _, test in splits)}-{max(len(test) for _, test in splits)}",
                "train share": f"{min(len(train) for train, _ in splits) / len(df):.0%}-"
                f"{max(len(train) for train, _ in splits) / len(df):.0%}",
            }

        return [
            Decision(
                "Temporal split: the 25 stations of a day share its weather",
                "Most of the target's variance lies between days, so a random split would train on the other stations "
                "of each test day. Untuned LightGBM on 3 folds: RMSE 0.62 with random folds, 1.00 with each day's "
                "stations on one side.",
                pd.DataFrame(spread).rename_axis("statistic"),
            ),
            Decision(
                "Next_Tmin is the target; Next_Tmax is dropped",
                "The v2 task holds one target. For the minimum, the mean of untuned CatBoost, LightGBM and ridge (RMSE "
                "0.779) beats the best per-station MOS (0.823) on 7 of the 9 windows; for the maximum, MOS on the "
                "forecast alone (1.575) beats every untuned model (1.583-1.710) and their mean (1.601). The maximum is "
                "observed on the next day, after the prediction point, so it cannot stay as a feature.",
                pd.DataFrame(corrections).rename_axis("LDAPS forecast"),
            ),
            Decision(
                "The targets are AWS daily extremes, the present-day columns hourly extremes up to 21 KST",
                "A row's target is not the next row's present-day value: the daily minimum lies below the lowest "
                "hourly reading and the daily maximum above the highest one (Cho et al. 2020, Sec. 2.3).",
                pd.DataFrame(measured).T.rename_axis("same station, next day"),
            ),
            Decision(
                "Nine one-week test windows over the last summer, with a one-day gap",
                "One- or two-week windows follow what the curators argue for weather (climate_model_weather_forecasting). "
                "Walking back from the newest data, fourteen-day windows stop after five, at the empty weeks before "
                "July 2017. Explicit cutoffs in the summers 2016 and 2017 give 9 fourteen-day windows with 118 test "
                "days, but they separate the methods no better: paired standard errors between untuned CatBoost, "
                "LightGBM and ridge of 0.023-0.047 RMSE, against 0.028-0.042 on the shipped windows.",
                pd.DataFrame(sizes).T.rename_axis("option"),
            ),
        ]
