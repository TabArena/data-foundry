"""Curated dataset definition for `climate_model_weather_forecasting_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Metric,
    Source,
    TaskSummary,
    Temporal,
    TemporalSplits,
)


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
            "Three one-week test windows of 2023, newest first: 24-30 July, 1-7 May (the warmest month) and 13-19 "
            "February (late winter), as for a model refit every week; training is every measurement taken at least "
            "three days before the window, since a forecast is issued up to three days ahead, of which a benchmark "
            "fits on a random million of the newest year (almost all of the history)."
        ),
        changes=(
            "We test three one-week windows spread from February to July 2023 instead of TabReD's one month of July, "
            "which the curator judged long for weather, and leave the three days before each window out of training."
        ),
        fit="direct",
        fit_reason=(
            "The features are forecasts and climate averages available before the measurement, and later weeks stand "
            "for the forecasts to come. The meaning of one time column of TabReD's release is unclear."
        ),
    )

    # Dataset
    unique_name = "climate_model_weather_forecasting_1m"
    domain = "environmental science & climate"
    sources = (
        Source(
            role="publication",
            platform="Kaggle",
            url="https://www.kaggle.com/datasets/pcovkrd84mejm/tabred-weather",
            license="CC-BY-NC-SA-4.0",
            year="2024",
            bibtex="""
                @inproceedings{rubachev2025tabred,
                  title={TabReD: Analyzing Pitfalls and Filling the Gaps in Tabular Deep Learning Benchmarks},
                  author={Rubachev, Ivan and Kartashev, Nikolay and Gorishniy, Yury and Babenko, Artem},
                  booktitle={The Thirteenth International Conference on Learning Representations},
                  year={2025},
                }
            """,
        ),
    )
    download_description = """
        We get the TabRed data from Kaggle.

        kaggle datasets download -d pcovkrd84mejm/tabred-weather -f weather.parquet && unzip weather.parquet.zip && rm weather.parquet.zip && mkdir -p local-data-warehouse/climate_model_weather_forecasting && mv weather.parquet local-data-warehouse/climate_model_weather_forecasting/
    """
    curation_comments = """
        We start with data from TabRed, which already comes preprocessed.

        - The data comes from TabReD (https://arxiv.org/abs/2406.19380), which calls it similar to the Shifts weather data (Malinin et al. 2021, https://arxiv.org/abs/2107.07455) but larger and with a time-based split; the Shifts appendix describes the features.
        - Note: Neither paper explains `apply_time_rl`, which Shifts does not have. It holds epoch seconds between 3 minutes and 3.1 days before `fact_time` in every row; we keep it as a number.
        - Note: TabReD states no unit for the target ("the true temperature"). Its values, mostly whole numbers with median 27, fit degrees Celsius, the unit of Shifts.
        - We drop duplicated columns `cmc_0_1_66_0` , `cmc_0_1_67_0`, `cmc_0_1_68_0`, and `cmc_0_1_11_0`, which is like them 0.0 or missing in every row.
        - We set -9999 to missing in `gfs_soil_temperature` (31% of rows), `cmc_0_0_0_2_grad` (1.9%) and `gfs_temperature_sea_grad` (0.3%): it is a fill value, as the other values of these columns lie between about -21 and 52, and every row with -9999 in `gfs_temperature_sea_grad` also has it in `gfs_soil_temperature`.
        - The row budget: Each test window keeps at most 500k of its rows (v2 split protocol; all of them here, 271k to 386k), and each train side holds every row up to three days before its window, so the container holds every row a split uses (the three days before the newest window lie in no split). The container records the 1M train budget, and a benchmark sub-samples each train side to 1M rows before a fit (`subsample_train`; by default a random 1M of the newest year before the window). The data start in July 2022, so the newest year leaves out only part of July 2022 and the default is close to the random sub-sampling of TabReD, which keeps data from all periods of the history.
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
    splits_comment = """
        Each test window is one week (the horizon checked, CC 2026-11-11). TabReD tests one month (1-30 July 2023), which the curator judged long for weather, and states no refit cadence; post-processing models are re-estimated every day on the last 30-60 days (https://npg.copernicus.org/articles/27/23/2020/), so a weekly refit is conservative and a week still spans several weather situations. One day would test one weather situation per window and be shorter than a forecast's lead of up to three days, and 14 days is the upper bound of the rule on weather windows. The windows, newest first (CC 2026-11-10 and 2026-11-11, the curator's pick): 2023-07-24 to 07-30, the newest; 2023-05-01 to 05-07, in the warmest month (mean measured temperature 28.06 against 26.55 on its train side); and 2023-02-13 to 02-19, in late winter, when the models' upper-air temperature forecasts (`gfs_temperature_5000`, `gfs_temperature_7000`) differ most from training. TabReD's year runs from 1 July 2022 to 30 July 2023, so no other year can be tested, and the one-week windows that keep half the rows for training run from February to July 2023; the three are 11 and 12 weeks apart. The floor as amended on 2026-11-11 would also admit 6-12 February (49.95% of the rows for training with the gap), the February week first proposed; 13-19 February is the curator's pick. The gap of three days: a forecast is issued up to 74 hours before its measurement (`apply_time_rl`; median 31.5 hours, 99.2% within 72 hours), so 19.7%, 21.8% and 21.3% of the windows' forecasts were issued before the window starts. Without the gap their train side would hold readings of their own station taken after the forecast was issued, and a station's daily error carries over for days (the daily error minus the station's mean correlates 0.34, 0.23 and 0.18 at lags of one, two and three days, 0.14 at seven), so the model that corrects a forecast is trained only on what was measured by the time it was issued: train is every measurement taken at least three days before the window. Each window keeps at most 500k of its rows (all of them here: 377,992, 385,508 and 270,717); each train side holds every earlier row (16,429,730, 11,733,079 and 8,739,284: 96.9%, 69.2% and 51.6% of the 16,951,828 rows), and a benchmark sub-samples it to 1M rows, by default a random 1M of the newest year before the window (`subsample_train`). The 144,106 rows of 21-23 July 2023, the newest window's gap, lie in no split, so the frame leaves them out.
    """
    temporal = Temporal(
        on="fact_time",
        splits=TemporalSplits(
            window=7, unit="days", cutoffs=("2023-07-24", "2023-05-01", "2023-02-13"), gap=3, gap_unit="days"
        ),
    )

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
