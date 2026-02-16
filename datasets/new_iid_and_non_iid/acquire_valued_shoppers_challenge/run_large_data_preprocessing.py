from __future__ import annotations

import functools
import gzip
import operator
from pathlib import Path

import polars as pl
from data_foundry.schema import DEFAULT_LOCAL_DATA_DIR

data_path = Path(DEFAULT_LOCAL_DATA_DIR) / "acquire_valued_shoppers_challenge"


print("Loading data...")
data_offers = pl.read_csv(gzip.open(data_path / "offers.csv.gz").read())
data_train_history = pl.read_csv(
    gzip.open(data_path / "trainHistory.csv.gz").read()
).with_columns(pl.col("offerdate").str.strptime(pl.Date))
data_transactions = pl.read_csv(
    gzip.open(data_path / "transactions.csv.gz").read()
).with_columns(pl.col("date").str.strptime(pl.Date))

print("Merging data...")
data_train_offer = (
    data_train_history.join(data_offers, on="offer")
    .with_columns(pl.col("repeater").eq("t").cast(pl.Int32).alias("target"))
    .drop("repeater")
)
data_transactions = data_transactions.join(data_train_offer, on="id").with_columns(
    (pl.col("offerdate") - pl.col("date")).dt.total_days().alias("date_diff")
)
del data_train_history, data_offers, data_train_offer

print("Aggregating data...")
filters = {
    "bought_company": pl.col("company").eq(pl.col("company_right")),
    "bought_category": pl.col("category").eq(pl.col("category_right")),
    "bought_brand": pl.col("brand").eq(pl.col("brand_right")),
}
date_diffs = [
    pl.col("date_diff").lt(d).alias(f"{d}")
    for d in [1, 3, 7, 14, 21, 28, 60, 90, 120, 150, 180]
]
exprs = [
    pl.col("purchaseamount").cast(pl.Float64).sum().alias("total_spend"),
    pl.col("target").first(),
    pl.col("offervalue").first(),
    pl.col("offerdate").first(),
    pl.col("offerdate").first().dt.weekday().alias("day_of_week"),
    pl.col("offerdate").first().dt.day().alias("day_of_month"),
    pl.col("offerdate").first().dt.ordinal_day().alias("day_of_year"),
]
exprs += functools.reduce(
    operator.iadd,
    [
        [
            fv.sum().alias(f"has_{fn}"),
            pl.col("purchasequantity")
            .cast(pl.Float64)
            .filter(fv)
            .alias(f"has_{fn}_q")
            .sum(),
            pl.col("purchaseamount")
            .cast(pl.Float64)
            .filter(fv)
            .sum()
            .alias(f"has_{fn}_a"),
        ]
        for fn, fv in filters.items()
    ],
    [],
)
exprs += functools.reduce(
    operator.iadd,
    [
        [
            fv.and_(d).sum().alias(f"has_{fn}_{d.meta.output_name()}"),
            pl.col("purchasequantity")
            .cast(pl.Float64)
            .filter(fv.and_(d))
            .alias(f"has_{fn}_q_{d.meta.output_name()}")
            .sum(),
            pl.col("purchaseamount")
            .cast(pl.Float64)
            .filter(fv.and_(d))
            .alias(f"has_{fn}_a_{d.meta.output_name()}")
            .sum(),
        ]
        for d in date_diffs
        for fn, fv in filters.items()
    ],
    [],
)

data = data_transactions.group_by("id").agg(*exprs).sort(by="offerdate")

print("Saving preprocessed data...")
data.write_parquet(data_path / "merged_input_data.parquet")




##### Too inefficient Pandas Version but maybe makes it clearer what the code does:
# import numpy as np
# import pandas as pd
# print("Loading data...")
# data_offers = pd.read_csv(data_path / "offers.csv.gz")
# data_train_history = pd.read_csv(data_path / "trainHistory.csv.gz")
# data_transactions = pd.read_csv(data_path / "transactions.csv.gz")
#
# data_train_history["offerdate"] = pd.to_datetime(
#     data_train_history["offerdate"]
# ).dt.date
# data_transactions["date"] = pd.to_datetime(data_transactions["date"]).dt.date
#
# print("Merging data...")
# data_train_offer = (
#     data_train_history.merge(data_offers, on="offer", how="inner")
#     .assign(target=lambda df: (df["repeater"] == "t").astype("int32"))
#     .drop(columns="repeater")
# )
# data_transactions = data_transactions.merge(
#     data_train_offer, on="id", how="inner"
# ).assign(date_diff=lambda df: (df["offerdate"] - df["date"]).dt.days)
# del data_train_history, data_offers, data_train_offer
#
# # -- Pandas version of TabRed Polaris preprocessing
# print("Preprocessing data...")
# df = data_transactions
# df["purchaseamount"] = pd.to_numeric(df["purchaseamount"], errors="coerce")
# df["purchasequantity"] = pd.to_numeric(df["purchasequantity"], errors="coerce")
# df["date_diff"] = pd.to_numeric(df["date_diff"], errors="coerce")
#
# # Row-wise boolean filters (Polars: pl.col('x').eq(pl.col('x_right')))
# filters = {
#     "bought_company": df["company"].eq(df["company_right"]),
#     "bought_category": df["category"].eq(df["category_right"]),
#     "bought_brand": df["brand"].eq(df["brand_right"]),
# }
# date_thresholds = [1, 3, 7, 14, 21, 28, 60, 90, 120, 150, 180]
# date_diffs = {str(d): df["date_diff"].lt(d) for d in date_thresholds}
#
#
# def _group_agg(g: pd.DataFrame) -> pd.Series:
#     out = {}
#
#     # Base exprs
#     out["total_spend"] = g["purchaseamount"].sum(skipna=True)
#     out["target"] = g["target"].iloc[0] if len(g) else np.nan
#     out["offervalue"] = g["offervalue"].iloc[0] if len(g) else np.nan
#     od = g["offerdate"].iloc[0] if len(g) else pd.NaT
#     out["offerdate"] = od
#     out["day_of_week"] = od.weekday() if pd.notna(od) else np.nan
#     out["day_of_month"] = od.day if pd.notna(od) else np.nan
#     out["day_of_year"] = od.dayofyear if pd.notna(od) else np.nan
#
#     # has_{fn}, has_{fn}_q, has_{fn}_a
#     for fn, mask in filters.items():
#         m = mask.loc[g.index]
#         out[f"has_{fn}"] = int(m.sum())
#         out[f"has_{fn}_q"] = g.loc[m, "purchasequantity"].sum(skipna=True)
#         out[f"has_{fn}_a"] = g.loc[m, "purchaseamount"].sum(skipna=True)
#
#     # has_{fn}_{d}, has_{fn}_q_{d}, has_{fn}_a_{d}
#     for dname, dmask in date_diffs.items():
#         for fn, fmask in filters.items():
#             m = fmask.loc[g.index] & dmask.loc[g.index]
#             out[f"has_{fn}_{dname}"] = int(m.sum())
#             out[f"has_{fn}_q_{dname}"] = g.loc[m, "purchasequantity"].sum(skipna=True)
#             out[f"has_{fn}_a_{dname}"] = g.loc[m, "purchaseamount"].sum(skipna=True)
#
#     return pd.Series(out)
#
#
# data = (
#     df.groupby("id", sort=False, group_keys=False)
#     .apply(_group_agg)
#     .reset_index()
#     .sort_values("offerdate")
#     .reset_index(drop=True)
# )