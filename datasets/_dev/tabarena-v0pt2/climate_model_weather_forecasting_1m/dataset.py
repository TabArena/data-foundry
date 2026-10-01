"""Curated dataset definition for `climate_model_weather_forecasting_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TemporalSplits


class ClimateModelWeatherForecasting1m(AbstractCuratedDataset):
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

        - This data is similar to data from https://arxiv.org/abs/2406.19380. This paper also describes the feature in more detail. The column `apply_time_rl` is new and might relate to a rolling lag/window indicator.
        - We drop duplicated columns `cmc_0_1_66_0` , `cmc_0_1_67_0`, `cmc_0_1_68_0`, and `cmc_0_1_11_0`, which is like them 0.0 or missing in every row.
        - We set -9999 to missing in `gfs_soil_temperature` (31% of rows), `cmc_0_0_0_2_grad` (1.9%) and `gfs_temperature_sea_grad` (0.3%): it is a fill value, as the other values of these columns lie between about -21 and 52, and every row with -9999 in `gfs_temperature_sea_grad` also has it in `gfs_soil_temperature`.
    """

    # Task
    target = "fact_temperature"
    problem_type = "regression"
    time_on = "fact_time"

    # Splits
    splits_comment = (
        "We use each of the last 3 weeks as a test window (newest first) and all prior data as train data. Each "
        "window keeps at most 500k of its rows; each train side is a random 1M of all earlier rows (one random order "
        "for all windows)."
    )
    time_horizon = 7
    time_horizon_unit = "days"
    temporal_splits = TemporalSplits(window=7, unit="days", n_windows=3)
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
        df = df.sort_values(by="fact_time").reset_index(drop=True)
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
