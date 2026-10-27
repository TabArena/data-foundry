"""Curated dataset definition for `climate_model_weather_forecasting_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary, Temporal, TemporalSplits


class ClimateModelWeatherForecasting1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "What temperature will a weather station measure at a given time, given the weather models' forecasts for"
            " that place and time?"
        ),
        use_case=(
            "For example, a weather service corrects the raw forecasts of global weather models at each station, to "
            "publish a more accurate local temperature forecast (Yandex station data, released with the TabReD "
            "benchmark)."
        ),
        row=(
            "One temperature measurement at one of 1,864 weather stations, July 2022 to July 2023, as filtered and "
            "sub-sampled by TabReD."
        ),
        predicted="The temperature measured at the station; the unit is not stated.",
        known=(
            "The station, its location and the time; the forecasts of two global weather models (CMC and GFS) for "
            "that place and time, with their lead times (temperature at several heights, wind, humidity, pressure, "
            "cloud, precipitation); and the station's climate averages of temperature and pressure."
        ),
        split=(
            "Each of the last three weeks of July 2023 is a test window; training is a random million of all earlier "
            "measurements, as for a model refit every week."
        ),
        changes=(
            "We test on one-week windows instead of TabReD's one month, which the curator judged long for weather."
        ),
        fit="direct",
        fit_reason=(
            "The features are forecasts and climate averages available before the measurement, and later weeks stand "
            "for the forecasts to come. The meaning of one time column of TabReD's release is unclear."
        ),
    )

    # Dataset
    unique_name = "climate_model_weather_forecasting_1m"
    version_of = "climate_model_weather_forecasting"
    version_comment = """
        We sample per test window (v2 split protocol): each window keeps at most 500k of its rows, and its train side is a random 1M of all earlier rows, drawn in one random order for all windows; the frame keeps only the rows a split uses. We follow TabReD and use random sub-sampling of the train data. The idea behind this instead of a time-based subsampling is to keep data from various time periods and model the distribution shift across the full time horizon.
    """
    year = "2024"
    domain = "environmental science & climate"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/pcovkrd84mejm/tabred-weather"
    license = "CC-BY-NC-SA-4.0"
    download_description = """
        We get the TabRed data from Kaggle.

        kaggle datasets download -d pcovkrd84mejm/tabred-weather -f weather.parquet && unzip weather.parquet.zip && rm weather.parquet.zip && mkdir -p local-data-warehouse/climate_model_weather_forecasting && mv weather.parquet local-data-warehouse/climate_model_weather_forecasting/
    """
    bibtex = """
        @inproceedings{rubachev2025tabred,
          title={TabReD: Analyzing Pitfalls and Filling the Gaps in Tabular Deep Learning Benchmarks},
          author={Rubachev, Ivan and Kartashev, Nikolay and Gorishniy, Yury and Babenko, Artem},
          booktitle={The Thirteenth International Conference on Learning Representations},
          year={2025},
        }
    """
    curation_comments = """
        We start with data from TabRed, which already comes preprocessed.

        - The data comes from TabReD (https://arxiv.org/abs/2406.19380), which calls it similar to the Shifts weather data (Malinin et al. 2021, https://arxiv.org/abs/2107.07455) but larger and with a time-based split; the Shifts appendix describes the features.
        - Note: Neither paper explains `apply_time_rl`, which Shifts does not have. It holds epoch seconds between 3 minutes and 3.1 days before `fact_time` in every row; we keep it as a number.
        - Note: TabReD states no unit for the target ("the true temperature"). Its values, mostly whole numbers with median 27, fit degrees Celsius, the unit of Shifts.
        - We drop duplicated columns `cmc_0_1_66_0` , `cmc_0_1_67_0`, `cmc_0_1_68_0`, and `cmc_0_1_11_0`, which is like them 0.0 or missing in every row.
        - We set -9999 to missing in `gfs_soil_temperature` (31% of rows), `cmc_0_0_0_2_grad` (1.9%) and `gfs_temperature_sea_grad` (0.3%): it is a fill value, as the other values of these columns lie between about -21 and 52, and every row with -9999 in `gfs_temperature_sea_grad` also has it in `gfs_soil_temperature`.
    """

    # Task
    target = "fact_temperature"
    problem_type = "regression"
    metric = Metric.source(
        "rmse",
        original="RMSE",
        reference=(
            "Rubachev et al. 2025, TabReD (ICLR), https://arxiv.org/abs/2406.19380; Shifts weather "
            "(Malinin et al. 2021) also uses RMSE"
        ),
        definition="Root mean squared error of fact_temperature.",
    )

    # Splits
    splits_comment = (
        "We use each of the last 3 weeks as a test window (newest first) and all prior data as train data. Each "
        "window keeps at most 500k of its rows; each train side is a random 1M of all earlier rows (one random order "
        "for all windows)."
    )
    temporal = Temporal(
        on="fact_time",
        splits=TemporalSplits(window=7, unit="days", n_windows=3),
    )
    subsample_to_budget = True

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_parquet(raw_dir / "weather.parquet")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df["fact_time"] = pd.to_datetime(df["fact_time"] * 10**6, unit="us")
        df = df.drop(columns=["cmc_0_1_66_0", "cmc_0_1_67_0", "cmc_0_1_68_0", "cmc_0_1_11_0"])
        fill_value_columns = ["gfs_soil_temperature", "cmc_0_0_0_2_grad", "gfs_temperature_sea_grad"]
        df[fill_value_columns] = df[fill_value_columns].replace(-9999, np.nan)
        df = df.sort_values(by="fact_time", kind="stable").reset_index(drop=True)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "fact_station_id",
                "cmc_available",
                "gfs_available",
                "gfs_soil_temperature_available",
            ],
            datetime=["fact_time"],  # parsed from epoch seconds in `_clean`
        )
