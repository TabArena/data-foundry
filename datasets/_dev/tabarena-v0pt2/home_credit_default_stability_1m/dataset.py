"""Curated dataset definition for `home_credit_default_stability_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import functools
import itertools
import operator
from collections.abc import Iterable
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TemporalSplits


def set_table_dtypes(df):
    """Set dtypes to optimize data size."""
    import polars as pl

    for col in df.columns:
        if col in ["case_id", "WEEK_NUM", "num_group1", "num_group2"]:
            df = df.with_columns(pl.col(col).cast(pl.Int32))
        elif col in ["date_decision"] or col[-1] == "D":
            df = df.with_columns(pl.col(col).cast(pl.Date))

    # Type downcasting
    int_types = [pl.Int8, pl.Int16, pl.Int32, pl.Int64]
    float_types = [pl.Float32, pl.Float64]
    table_min = df.select(pl.col(df.columns).min()).collect(engine="streaming")
    table_max = df.select(pl.col(df.columns).max()).collect(engine="streaming")

    for col, col_type in df.schema.items():
        c_min = table_min[col].item()
        c_max = table_max[col].item()

        if col_type in int_types:
            if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                df = df.with_columns(pl.col(col).cast(pl.Int8))
            elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                df = df.with_columns(pl.col(col).cast(pl.Int16))
            elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                df = df.with_columns(pl.col(col).cast(pl.Int32))
            elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                df = df.with_columns(pl.col(col).cast(pl.Int64))
        elif col_type in float_types and c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
            df = df.with_columns(pl.col(col).cast(pl.Float32))
    return df


def read_tables(table_paths: Iterable):
    """Scan and concatenate parquet tables lazily."""
    import polars as pl

    table_paths = list(table_paths)
    res = pl.concat(
        [pl.scan_parquet(p, low_memory=True, rechunk=True) for p in table_paths],
        how="vertical_relaxed",
    )

    return res


def aggregate_features(df):
    """Aggregation expressions."""
    import polars as pl

    # The code from TabRed crashes as it tries to use numerical aggregations on string data.
    # We filter these and treat them as categorical instead, using different aggregations.
    special_string_cols = [
        "credacc_status_367L",
        "credtype_587L",
        "familystate_726L",
        "inittransactioncode_279L",
        "status_219L",
        "periodicityofpmts_997L",
        "empl_employedtotal_800L",
        "empl_industry_691L",
        "familystate_447L",
        "gender_992L",
        "housetype_905L",
        "housingtype_772L",
        "incometype_1044T",
        "maritalst_703L",
        "relationshiptoclient_415T",
        "relationshiptoclient_642T",
        "role_1084L",
        "role_993L",
        "sex_738L",
        "type_25L",
    ]

    # Basic logic -- all numeric values we aggregate with max, min, std, mean
    cols = df.columns
    # Numeric values
    exprs = functools.reduce(
        operator.iadd,
        [
            [
                pl.col(col).max().alias(f"max_{col}"),
                pl.col(col).min().alias(f"min_{col}"),
                pl.col(col).mean().alias(f"mean_{col}"),
                pl.col(col).std().alias(f"std_{col}"),
            ]
            for col in cols
            if (col[-1] in ("P", "A", "T", "L") and (col not in special_string_cols))
        ],
        [],
    )

    # categorical expressions (strings)
    exprs += functools.reduce(
        operator.iadd,
        [
            [
                pl.col(col).last().alias(f"last_{col}"),
                pl.col(col).n_unique().alias(f"n_unique_{col}"),
                pl.col(col).first().alias(f"first_{col}"),
            ]
            for col in cols
            if (col[-1] == "M") or (col in special_string_cols)
        ],
        [],
    )
    # Dates
    exprs += functools.reduce(
        operator.iadd,
        [
            [
                pl.col(col).max().alias(f"max_{col}"),
                pl.col(col).min().alias(f"min_{col}"),
                pl.col(col).mean().alias(f"mean_{col}"),
            ]
            for col in cols
            if col[-1] == "D"
        ],
        [],
    )

    # Count aggregates
    exprs += [pl.col(col).max().alias(f"max_{col}") for col in cols if "num_group" in cols]

    return [df.sort("num_group1").group_by("case_id").agg(exprs)]


class HomeCreditDefaultStability1m(AbstractCuratedDataset):
    # Dataset
    unique_name = "home_credit_default_stability_1m"
    version_of = "home_credit_default_stability"
    version_comment = """
        We sample per test window (v2 split protocol): each window keeps at most 500k of its rows, and its train side is a random 1M of all earlier rows, drawn in one random order for all windows; the frame keeps only the rows a split uses. We follow TabReD and use random sub-sampling of the train data. The idea behind this instead of a time-based subsampling is to keep data from various time periods and model the distribution shift across the full time horizon.
    """
    year = "2024"
    domain = "finance"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/competitions/home-credit-credit-risk-model-stability"
    license = "Kaggle Competition Rules"
    download_description = """
        We get the data from the Kaggle competition.

        kaggle competitions download -c home-credit-credit-risk-model-stability
        mkdir -p local-data-warehouse/home_credit_default_stability && mv home-credit-credit-risk-model-stability.zip local-data-warehouse/home_credit_default_stability/ && cd local-data-warehouse/home_credit_default_stability/ && unzip home-credit-credit-risk-model-stability.zip && rm home-credit-credit-risk-model-stability.zip && rm -rf csv_files && rm -rf parquet_files/test && rm sample_submission.csv feature_definitions.csv
    """
    bibtex = r"""
        @misc{Herman2024HomeCreditCreditRiskModelStability,
          author = {Daniel Herman and Tomas Jelinek and Walter Reade and Maggie Demkin and Addison Howard},
          title  = {Home Credit - Credit Risk Model Stability},
          year   = {2024},
          howpublished = {\url{https://kaggle.com/competitions/home-credit-credit-risk-model-stability}},
          note   = {Kaggle competition}
        }
    """
    curation_comments = """
        We start with the data from Kaggle and follow the preprocessing from TabRed (https://github.com/yandex-research/tabred/tree/main/preprocessing#homecredit-default-stability-homecredit-20), which in turn follows two Kaggle solutions (https://www.kaggle.com/competitions/home-credit-credit-risk-model-stability/discussion/507946, https://www.kaggle.com/code/yuuniekiri/fork-of-home-credit-catboost-inference).

        - We follow TabRed and use temporal splits for the task. The Kaggle experts used various strategies and most commonly StratifiedGroupKFold to align offline CV with the temporal-split data on the leaderboard. That is, the split used for training can be StratifiedGroupKFold, but not for testing.
        - Note, the original competition was heavily influenced by metric hacking, which is not relevant for our offline benchmark tasks. Thus, results are not directly comparable ot transferable.
        - We change the preprocessing from Kaggle and TabRed in specific steps: (A) we depart from the TabRed and Kaggle solutions in that we do not drop high-cardinality string columns, (B) we do not drop month and week, as it was only dropped due to the metric leak in the competition, (C) we only drop constant columns if they are constant w.r.t. NaN and non-NaN values, (D) we do not perform ordinal encoding and drop minor categories, (E) we do not sub-sample the data, (F) we keep the date column without transformations for the pipelines to handle, and (G) the code from TabRed is outdated and does not function the same anymore when it comes to down-casting string and categorical data of the data from Kaggle, we fix this by treating categorical data as categorical following the original Kaggle scripts, moreover, we had to remove getting the std() of a date column, which is not supported anymore.
        - We drop case_id as it is already collapsed and thus does not contain extra information.
        - We cast all object and string columns to be categorical. Note that they are anonymized and string preprocessing likely does not add a lot of value as a result.
        - We drop name-related columns as they do not hold relevant information. These were otherwise dropped as high-cardinality string columns in TabRed or on Kaggle.
    """

    # Task
    target = "target"
    problem_type = "binary_classification"
    time_on = "date_decision"

    # Splits
    splits_comment = """
        We follow TabRed's test period (2020-05-01 to 2020-10-05) and split it into 3 test windows of 2 months (May-June, July-August, September to 2020-10-05), simulating a model refit every 2 months; each window trains on all previous data. Each window keeps at most 500k of its rows; each train side is a random 1M of all earlier rows (one random order for all windows).
    """
    # 3 windows of 2 months replace TabRed's single 4.5-month test period (v2 split protocol, 2026-10), so the horizon
    # drops from 5 to 2 months and results are not comparable with TabRed's. Before sampling the windows hold 74,687 /
    # 79,743 / 70,497 rows (about 1.8k / 1.7k / 1.5k defaults); every train side is capped at 1M. 5-month windows
    # (cutoffs 2019-07-01, 2019-12-01, 2020-05-01) would keep the horizon, but the oldest would train on 439k rows
    # (Jan-Jun 2019) and test 506k pre-COVID rows, and the middle one would span the April 2020 drop in volume and
    # default rate.
    time_horizon = 2
    time_horizon_unit = "months"
    temporal_splits = TemporalSplits(window=2, unit="months", cutoffs=("2020-05-01", "2020-07-01", "2020-09-01"))
    accepted_check_warnings = {
        "dataset_missing_value_sentinel": "-1 is a real value: the avgdbd* columns are 'average days past or before "
        "due of payment' (Kaggle feature_definitions.csv), negative means paid early; -1 is the mode of a smooth "
        "distribution (-1 4.8%, -2 4.7%, -3 4.2%, 0 3.8%, down to -1220), missing values are NaN, and the default "
        "rate rises from 2.1% (< -1) over 3.3% (-1) and 4.5% (0) to 8.6% (late).",
    }
    subsample_to_budget = True

    # The raw tables are too large for pandas: `_prepare_raw_files` joins them with polars once (following
    # TabRed's homecredit.py, https://github.com/yandex-research/tabred/blob/main/preprocessing/homecredit.py)
    # and writes `merged_input_data.parquet`, which `_load_raw` starts from.
    prepared_raw_files = ("merged_input_data.parquet",)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        import polars as pl

        data_path = raw_dir / "parquet_files" / "train"
        train_basetable = read_tables(data_path.glob("train_base.parquet")).pipe(set_table_dtypes)
        train_static = read_tables(data_path.glob("train_static_0_*.parquet")).pipe(set_table_dtypes)
        train_static_cb = read_tables(data_path.glob("train_static_cb_0.parquet")).pipe(set_table_dtypes)

        train_aggregated = list(
            itertools.chain.from_iterable(
                [
                    aggregate_features(read_tables(data_path.glob(name)).pipe(set_table_dtypes))
                    for name in [
                        "train_applprev_1_*.parquet",
                        "train_tax_registry_a_1.parquet",
                        "train_tax_registry_b_1.parquet",
                        "train_tax_registry_c_1.parquet",
                        "train_credit_bureau_a_1_*.parquet",
                        "train_credit_bureau_b_1.parquet",
                        "train_other_1.parquet",
                        "train_person_1.parquet",
                        "train_deposit_1.parquet",
                        "train_debitcard_1.parquet",
                        "train_credit_bureau_a_2_*.parquet",
                        "train_credit_bureau_b_2.parquet",
                    ]
                ]
            )
        )

        data = train_basetable.clone()
        for i, df in enumerate([train_static, train_static_cb] + train_aggregated):
            data = data.join(df, how="left", on="case_id", suffix=f"_{i}")

        data = data.collect(engine="streaming")
        data = data.with_columns(
            [
                (pl.col(col) - pl.col("date_decision")).dt.total_days().cast(pl.Float32)
                for col in data.columns
                if col.endswith("D")
            ]
        )

        # CHANGED from TabRed: we only drop constant columns, not others
        n_unique = data.select(pl.col("*").n_unique())
        drop_cols = [c for c, dtype in data.schema.items() if (n_unique[c].item() <= 1)]
        data = data.drop(drop_cols)

        many_nulls = data.select(pl.col("*").is_null().mean().gt(0.95))
        n_unique = data.select(pl.col("*").drop_nulls().n_unique())

        drop_cols = [c for c, dtype in data.schema.items() if (many_nulls[c].item() or n_unique[c].item() == 1)]

        data = data.drop(drop_cols)

        # Drop duplicated columns
        col_hashes = {col: data.select(pl.col(col).hash().sum()).item() for col in data.columns}

        seen = {}
        duplicates = []

        for col, h in col_hashes.items():
            if h in seen:
                # Double check equality to avoid rare hash collisions
                if data[col].equals(data[seen[h]]):
                    duplicates.append(col)
                else:
                    seen[h] = col
            else:
                seen[h] = col

        data = data.drop(duplicates)

        data.write_parquet(raw_dir / "merged_input_data.parquet")

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_parquet(raw_dir / "merged_input_data.parquet")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Drop constant columns
        df = df.drop(
            columns=[
                # ID column (already collapsed and thus no extra information
                "case_id",
                # Name columns that are missing or have no affect due to case-id related grouping and anonymization
                "last_name_4917606M",
                "first_name_4917606M",
                "last_name_4527232M",
                "first_name_4527232M",
                "last_employername_160M",
                "first_employername_160M",
            ]
        )
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        text_cols = df.columns[(df.dtypes == "object") | (df.dtypes == "string")]
        return FeatureTypes(
            categorical=[c for c in text_cols if c != "date_decision"],
            datetime={"date_decision": "%Y-%m-%d"},
        )
