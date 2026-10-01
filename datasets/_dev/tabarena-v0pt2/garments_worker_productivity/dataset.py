"""Curated dataset definition for `garments_worker_productivity` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Temporal, TemporalSplits


class GarmentsWorkerProductivity(AbstractCuratedDataset):
    # Dataset
    unique_name = "garments_worker_productivity"
    year = "2020"
    domain = "industry & manufacturing"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C51S6D"
    license = "CC BY 4.0"
    download_description = r"""
        mkdir -p local-data-warehouse/garments_worker_productivity \
        && wget -P local-data-warehouse/garments_worker_productivity/ https://archive.ics.uci.edu/static/public/597/productivity+prediction+of+garment+employees.zip \
        && unzip local-data-warehouse/garments_worker_productivity/productivity+prediction+of+garment+employees.zip -d local-data-warehouse/garments_worker_productivity/ \
        &&  rm local-data-warehouse/garments_worker_productivity/productivity+prediction+of+garment+employees.zip
    """
    bibtex = """
        @article{imran2021mining,
            title={Mining the productivity data of the garment industry},
            author={Imran, Abdullah Al and Rahim, Md Shamsur and Ahmed, Tanvir},
            journal={International Journal of Business Intelligence and Data Mining},
            volume={19},
            number={3},
            pages={319--342},
            year={2021},
            publisher={Inderscience Publishers (IEL)}
        }
    """
    curation_comments = """
        - We fix typos in data entries (e.g., "finishing " becomes "finishing").
        - We transform the date to datetime.
        - The associated paper conceptualizes the task as an interpretable ML task without consideration of realistic predictive scenarios. Therefore, we define a new predictive ML task.
        - We define the decision point in time as the start of the day.
        - We set the target variable to "actual_productivity", and use the targeted_productivity as an input feature.
        - We do not include all features directly for prediction, because some can't be expected to be available at the decision point in time: "smv", "wip", "over_time", "idle_time", "idle_men", "incentive". To still keep as much information as possible, we impute the value of the previous recorded working day (by department and team).
        - "incentive" is a structured incentive, i.e. "higher pay for achieving the milestone or targeted performance", which "depends on the performance, so it fluctuates with the change in performance level" (Al Imran et al. 2021, Sec. 3.1). It is paid for the day's achieved output and recorded in the end-of-day efficiency report. In sewing, day-to-day changes in the incentive follow the same day's productivity (Spearman 0.53 within teams) and not the previous day's (0.07). We therefore use the previous day's value.
        - Because the timestamps are irregularly spaced, we additionally include the days passed sind the last recording per department and team.
        - Note that we try to keep feature engineering minimalistic and only with the sole purpose to prevent leaks with minimal loss of information.
        - It can be expected that feature engineering exposing the non-iid properties of the dataset will be crucial for good predictive performance.
        - We cannot fully exclude the possibility of leaks, since not enough information about the date of collection for some features is given.
        - We define 30 splits with one day for testing each, resulting in small test sizes of 17-24 samples per split.
    """

    # Task
    target = "actual_productivity"
    problem_type = "regression"

    # Splits
    splits_comment = """
        We define 30 splits with one day for testing each, resulting in small test sizes of 17-24 samples per split. The split with the smallest train sizes uses exactly half of the available samples.
    """
    temporal = Temporal(
        on="date",
        splits=TemporalSplits(window=1, unit="unique", n_windows=30),
        horizon=1,
        horizon_unit="days",
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "garments_worker_productivity.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # NOTE: "date", "quarter", "department", "day", "team", "targeted_productivity", "actual_productivity" are safe to keep. For "no_of_style_change", "no_of_workers" it's a guess.
        # "incentive" is paid for the day's achieved output (paper Sec. 3.1), so it is lagged like the end-of-day columns.
        lag_cols = ["smv", "wip", "over_time", "idle_time", "idle_men", "incentive"]
        df.department = df.department.str.strip(" ")
        df.date = pd.to_datetime(df.date)
        entity_cols = ["department", "team"]
        date_col = "date"
        lags = (1,)
        assert not df.duplicated(["department", "team", "date"]).any(), (
            "Found duplicate rows for the same department-team-date."
        )
        df = df.sort_values(list(entity_cols) + [date_col]).reset_index(drop=True)
        g = df.groupby(list(entity_cols), sort=False)
        prev_date = g[date_col].shift(1)
        df["days_since_prev_obs"] = (df[date_col] - prev_date).dt.days
        for col in lag_cols:
            for lag in lags:
                df[f"{col}_lag_{lag}"] = g[col].shift(lag)
        df = df.drop(columns=lag_cols)
        df = df.sort_values(by=date_col).reset_index(drop=True)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "quarter",
                "department",
                "day",
                "team",
            ],
        )
