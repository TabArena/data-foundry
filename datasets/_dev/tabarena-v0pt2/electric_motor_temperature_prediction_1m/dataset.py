"""Curated dataset definition for `electric_motor_temperature_prediction_1m` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class ElectricMotorTemperaturePrediction1m(AbstractCuratedDataset):
    # Dataset
    unique_name = "electric_motor_temperature_prediction_1m"
    version_of = "electric_motor_temperature_prediction"
    version_comment = """
        We build the recommended single train/test split (250k test rows) and sub-sample it to at most 1M train and 250k test rows with `curation_recommendations.subsample_split_to_budget`, keeping whole profiles.
    """
    year = "2021"
    domain = "industry & manufacturing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/wkirgsn/electric-motor-temperature"
    license = "CC BY-SA 4.0"
    data_tags = ("Non-IID", "Grouped")
    download_description = """
        kaggle datasets download wkirgsn/electric-motor-temperature --unzip && mkdir -p local-data-warehouse/electric_motor_temperature_prediction && mv measures_v2.csv local-data-warehouse/electric_motor_temperature_prediction/
    """
    bibtex = """
        @article{kirchgassner2020estimating,
          title={Estimating electric motor temperatures with deep residual machine learning},
          author={Kirchg{"a}ssner, Wilhelm and Wallscheid, Oliver and B{"o}cker, Joachim},
          journal={IEEE Transactions on Power Electronics},
          volume={36},
          number={7},
          pages={7480--7488},
          year={2020},
          publisher={IEEE}
        }
    """
    curation_comments = """
        We select the task to predict permanent magnet temperature from the input features. We create grouped splits on the profile_id, which corresponds to predicting the temperature for an unseen motor run session, thus simulating how the model would be used in reality.

        - The original study also incorporates temporal connection within the session. We re-create a time-index (https://www.kaggle.com/datasets/wkirgsn/electric-motor-temperature/discussion/147446).
        - We also add the derived inputs used in the original study.
        - We also add the EWMA/WEMS features with window sizes of [500, 2000, 4000, 8000]. To avoid the problem of having an incorrect EWMA/WEMS state and since not all recording are warmed up (https://www.kaggle.com/datasets/wkirgsn/electric-motor-temperature/discussion/117319), we drop the first 500 samples (first span) of each profile to simulate such a warm-up.
    """

    # Task
    target = "permanent_magnet_temperature"
    problem_type = "regression"
    group_on = "profile_id"
    group_labels = "per_sample"
    group_time_on = "profile_time_index"

    # Splits
    subsample_to_budget = True

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "measures_v2.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Add time feature
        df["profile_time_index"] = df.groupby("profile_id").cumcount() + 1
        df = df.rename(
            columns={
                "pm": "permanent_magnet_temperature",
            }
        )
        df = df.drop(
            columns=[
                # Other targets
                "stator_winding",
                "stator_tooth",
                "stator_yoke",
                # excluded as in the original study
                "torque",
            ]
        )
        # Add derived features  (from Table II)
        # Voltage magnitude
        df["u_s"] = np.sqrt(df["u_d"] ** 2 + df["u_q"] ** 2)
        # Current magnitude
        df["i_s"] = np.sqrt(df["i_d"] ** 2 + df["i_q"] ** 2)
        # Apparent power
        df["S_el"] = df["u_s"] * df["i_s"]
        # Joint interaction terms
        df["i_s_omega"] = df["i_s"] * df["motor_speed"]
        df["S_el_omega"] = df["S_el"] * df["motor_speed"]

        def add_grouped_ewm_features(
            input_df: pd.DataFrame,
            group_col: str,
            time_col: str,
            cols: list[str],
            input_spans: list[int],
        ) -> pd.DataFrame:
            input_df = input_df.sort_values([group_col, time_col]).copy()

            for col in cols:
                for span in input_spans:
                    alpha = 2 / (span + 1)

                    # EWMA
                    input_df[f"{col}_ewma_{span}"] = input_df.groupby(group_col, sort=False)[col].transform(
                        lambda s: s.ewm(alpha=alpha, adjust=False).mean()  # noqa: B023
                    )

                    # EWMS
                    input_df[f"{col}_ewms_{span}"] = input_df.groupby(group_col, sort=False)[col].transform(
                        lambda s: s.ewm(alpha=alpha, adjust=False).std()  # noqa: B023
                    )

            return input_df

        input_cols = [
            # Original features
            "u_d",
            "u_q",
            "i_d",
            "i_q",
            "coolant",
            "motor_speed",
            "ambient",
            # Derived features
            "u_s",
            "i_s",
            "S_el",
            "i_s_omega",
            "S_el_omega",
        ]
        spans = [500, 2000, 4000, 8000]
        df = add_grouped_ewm_features(
            input_df=df,
            group_col="profile_id",
            time_col="profile_time_index",
            cols=input_cols,
            input_spans=spans,
        )
        # Drop the first 500 samples of each profile to simulate warm-up and avoid incorrect EWMA/WEMS state
        df = (
            df.sort_values(["profile_id", "profile_time_index"])
            .loc[lambda d: d.groupby("profile_id").cumcount() >= 500]
            .reset_index(drop=True)
        )
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "profile_id",
            ],
        )
