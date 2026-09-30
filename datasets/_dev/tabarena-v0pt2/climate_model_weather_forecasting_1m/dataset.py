"""Curated dataset definition for `climate_model_weather_forecasting_1m` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TemporalSplits


class ClimateModelWeatherForecasting1m(AbstractCuratedDataset):
    # Dataset
    unique_name = "climate_model_weather_forecasting_1m"
    version_of = "climate_model_weather_forecasting"
    version_comment = """
        We randomly sub-sample the train to 1 million and test data 250k rows. We follow TabReD and use random sub-sampling. The idea behind this instead of a time-based subsampling is to keep data from various time periods and model the distribution shift across the full time horizon.
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
        - We drop duplicated columns `cmc_0_1_66_0` , `cmc_0_1_67_0`, `cmc_0_1_68_0`.
    """

    # Task
    target = "fact_temperature"
    problem_type = "regression"
    time_on = "fact_time"

    # Splits
    splits_comment = "We use the last week as test data and all prior data as train data."
    time_horizon = 7
    time_horizon_unit = "days"
    temporal_splits = TemporalSplits(window=7, unit="days", n_windows=1)
    subsample_to_budget = True

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_parquet(raw_dir / "weather.parquet")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df["fact_time"] = pd.to_datetime(df["fact_time"] * 10**6, unit="us")
        df = df.drop(columns=["cmc_0_1_66_0", "cmc_0_1_67_0", "cmc_0_1_68_0"])
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
        )
