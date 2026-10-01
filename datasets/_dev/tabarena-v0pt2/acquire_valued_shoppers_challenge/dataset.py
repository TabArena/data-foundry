"""Curated dataset definition for `acquire_valued_shoppers_challenge` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import functools
import gzip
import operator
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TemporalSplits, drop_columns


class AcquireValuedShoppersChallenge(AbstractCuratedDataset):
    # Dataset
    unique_name = "acquire_valued_shoppers_challenge"
    year = "2014"
    domain = "business & marketing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/c/acquire-valued-shoppers-challenge"
    license = "Kaggle Competition Rules"
    data_tags = ("Anonymized",)
    download_description = """
        We start with the data from Kaggle.

        kaggle competitions download -c acquire-valued-shoppers-challenge
        mkdir -p local-data-warehouse/acquire_valued_shoppers_challenge && mv acquire-valued-shoppers-challenge.zip local-data-warehouse/acquire_valued_shoppers_challenge/ && cd local-data-warehouse/acquire_valued_shoppers_challenge/ && unzip acquire-valued-shoppers-challenge.zip && rm acquire-valued-shoppers-challenge.zip testHistory.csv.gz sampleSubmission.csv.gz
    """
    bibtex = r"""
        @misc{DMDave2014AcquireValuedShoppersChallenge,
          author = {DMDave and Todd B and Will Cukierski},
          title  = {Acquire Valued Shoppers Challenge},
          year   = {2014},
          howpublished = {\url{https://kaggle.com/competitions/acquire-valued-shoppers-challenge}},
          note   = {Kaggle competition}
        }
    """
    curation_comments = """
        We follow the preprocessing from TabRed https://github.com/yandex-research/tabred/tree/main/preprocessing#ecom-offers-acquire-valued-shoppers-by-dmdave (which follows a top solution https://github.com/MLWave/kaggle_acquire-valued-shoppers-challenge).

        - The preprocessing by TabRed collapses customer groups into single entries per customer. So we go from grouped-temporal data to only temporal data. Future work could look into a version without preprocessing.
    """

    # Task
    target = "target"
    problem_type = "binary_classification"
    time_on = "offerdate"

    # Splits: a model deployed for 5 days before it is refit (the test window of TabRed), 5 windows back.
    temporal_splits = TemporalSplits(window=5, unit="days", n_windows=5)

    # The raw tables are too large for pandas: `_prepare_raw_files` joins them with polars once and
    # aggregates the purchase history per offer (the TabRed features); `_load_raw` starts from its output.
    prepared_raw_files = ("merged_input_data.parquet",)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        import polars as pl

        offers = pl.read_csv(gzip.decompress((raw_dir / "offers.csv.gz").read_bytes()))
        history = pl.read_csv(gzip.decompress((raw_dir / "trainHistory.csv.gz").read_bytes())).with_columns(
            pl.col("offerdate").str.strptime(pl.Date)
        )
        transactions = pl.read_csv(gzip.decompress((raw_dir / "transactions.csv.gz").read_bytes())).with_columns(
            pl.col("date").str.strptime(pl.Date)
        )

        train_offer = (
            history.join(offers, on="offer")
            .with_columns(pl.col("repeater").eq("t").cast(pl.Int32).alias("target"))
            .drop("repeater")
        )
        transactions = transactions.join(train_offer, on="id").with_columns(
            (pl.col("offerdate") - pl.col("date")).dt.total_days().alias("date_diff")
        )
        del history, offers, train_offer

        filters = {
            "bought_company": pl.col("company").eq(pl.col("company_right")),
            "bought_category": pl.col("category").eq(pl.col("category_right")),
            "bought_brand": pl.col("brand").eq(pl.col("brand_right")),
        }
        date_diffs = [pl.col("date_diff").lt(d).alias(f"{d}") for d in [1, 3, 7, 14, 21, 28, 60, 90, 120, 150, 180]]
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
                    pl.col("purchasequantity").cast(pl.Float64).filter(fv).alias(f"has_{fn}_q").sum(),
                    pl.col("purchaseamount").cast(pl.Float64).filter(fv).sum().alias(f"has_{fn}_a"),
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
        data = transactions.group_by("id").agg(*exprs).sort(by="offerdate")
        data.write_parquet(raw_dir / "merged_input_data.parquet")

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_parquet(raw_dir / "merged_input_data.parquet")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Add the binary purchase-history indicators again (TabRed drops them after aggregating).
        binary_df = df.assign(
            **{f"never_bought_{c}": (df[f"has_bought_{c}"] == 0) for c in ["company", "category", "brand"]},
            has_bought_brand_company_category=(
                (df["has_bought_brand"] != 0) & (df["has_bought_category"] != 0) & (df["has_bought_company"] != 0)
            ),
            has_bought_brand_category=((df["has_bought_brand"] != 0) & (df["has_bought_category"] != 0)),
            has_bought_brand_company=((df["has_bought_brand"] != 0) & (df["has_bought_company"] != 0)),
        )[
            [
                "never_bought_company",
                "never_bought_category",
                "never_bought_brand",
                "has_bought_brand_company_category",
                "has_bought_brand_category",
                "has_bought_brand_company",
            ]
        ].astype(np.float32)
        df = pd.concat([df, binary_df], axis=1)
        df = drop_columns(
            df,
            [
                "id",
                "has_bought_company_q_1",
                "has_bought_company_a_1",
                "has_bought_category_1",
                "has_bought_category_q_1",
                "has_bought_category_a_1",
                "has_bought_brand_1",
                "has_bought_brand_q_1",
                "has_bought_brand_a_1",
                "has_bought_company_1",
            ],
        )
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=(
                "target",
                "never_bought_company",
                "never_bought_category",
                "never_bought_brand",
                "has_bought_brand_company_category",
                "has_bought_brand_category",
                "has_bought_brand_company",
            ),
            datetime={"offerdate": "%Y-%m-%d"},
        )
