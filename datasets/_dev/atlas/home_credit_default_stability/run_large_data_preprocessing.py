"""Following TabRed: https://github.com/yandex-research/tabred/blob/main/preprocessing/homecredit.py"""

from __future__ import annotations

import numpy as np
from pathlib import Path
import itertools
from typing import Iterable

import polars as pl
from loguru import logger
from data_foundry.schema import DEFAULT_LOCAL_DATA_DIR


def set_table_dtypes(df):
    "set dtypes to optimize data size"

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
        elif col_type in float_types:
            if c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                df = df.with_columns(pl.col(col).cast(pl.Float32))
    return df


def read_tables(table_paths: Iterable):
    table_paths = list(table_paths)
    res = pl.concat(
        [pl.scan_parquet(p, low_memory=True, rechunk=True) for p in table_paths],
        how="vertical_relaxed",
    )

    logger.info(f"Read {[p.name for p in table_paths]}")
    return res


def aggregate_features(df: pl.LazyFrame):
    "Aggregation expressions"

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
    exprs = sum(
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
    exprs += sum(
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
    exprs += sum(
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
    exprs += [
        pl.col(col).max().alias(f"max_{col}") for col in cols if "num_group" in cols
    ]

    return [df.sort("num_group1").group_by("case_id").agg(exprs)]


def main():
    data_path = (
        Path(DEFAULT_LOCAL_DATA_DIR)
        / "home_credit_default_stability"
        / "parquet_files"
        / "train"
    )

    train_basetable = read_tables(data_path.glob("train_base.parquet")).pipe(
        set_table_dtypes
    )
    train_static = read_tables(data_path.glob("train_static_0_*.parquet")).pipe(
        set_table_dtypes
    )
    train_static_cb = read_tables(data_path.glob("train_static_cb_0.parquet")).pipe(
        set_table_dtypes
    )

    train_aggregated = list(
        itertools.chain.from_iterable(
            [
                aggregate_features(
                    read_tables(data_path.glob(name)).pipe(set_table_dtypes)
                )
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

    logger.info("Constructing train data table")
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

    many_nulls = data.select(pl.col('*').is_null().mean().gt(0.95))
    n_unique = data.select(pl.col('*').drop_nulls().n_unique())

    drop_cols = [
        c for c, dtype in data.schema.items()
        if (many_nulls[c].item() or n_unique[c].item() == 1)
    ]

    data = data.drop(drop_cols)

    # Drop duplicated columns
    logger.info("Start dropping duplicated columns...")
    col_hashes = {
        col: data.select(pl.col(col).hash().sum()).item()
        for col in data.columns
    }

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

    print(f"Original columns: {data.width}")
    print(f"Duplicate columns found: {len(duplicates)}")
    print(f"Columns dropped: {duplicates}")
    data = data.drop(duplicates)

    print("Saving preprocessed data...")
    data.write_parquet(data_path.parent.parent / "merged_input_data.parquet")

    print(data.shape)


if __name__ == "__main__":
    main()
