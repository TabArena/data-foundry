"""Curated dataset definition for `sberbank_housing_market_forecasting` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import zipfile
from pathlib import Path
from typing import TYPE_CHECKING

import polars as pl
from data_foundry.v2 import AbstractCuratedDataset, TemporalSplits

if TYPE_CHECKING:
    import pandas as pd


class SberbankHousingMarketForecasting(AbstractCuratedDataset):
    # Dataset
    unique_name = "sberbank_housing_market_forecasting"
    year = "2017"
    domain = "business & marketing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/competitions/sberbank-russian-housing-market"
    license = "Kaggle Competition Rules"
    data_tags = ("Spatial",)
    download_description = """
        We use the data from Kaggle:

        kaggle competitions download -c sberbank-russian-housing-market
        mkdir -p local-data-warehouse/sberbank_housing_market_forecasting && mv sberbank-russian-housing-market.zip local-data-warehouse/sberbank_housing_market_forecasting/ && cd local-data-warehouse/sberbank_housing_market_forecasting/ && unzip sberbank-russian-housing-market.zip && rm test.csv.zip sample_submission.csv.zip data_dictionary.txt sberbank-russian-housing-market.zip
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
        We follow the preprocessing from TabRed (https://github.com/yandex-research/tabred/tree/main/preprocessing#sberbank-housing-market-forecasting).

        - We drop two duplicated columns with the same values as other columns: "0_6_all", "7_14_all"
        - We drop the ID column as it does not provide information.
        - Note, the dataset contains a lot of spatial feature and even more already decoded spatial information (like distances to various points of interest).
        - We drop all rows that have a build_year higher than their own timestamp of being sold. It is unclear from the original data what kind of house market data this comes from. The description for the column is "year built" and not "year to be finished" so we assume these are all data errors. Plus this drops around 150 samples for which the build_year is incorrectly encoded as integer derived from a range like "2000-2005".
    """

    # Task
    target = "price_doc"
    problem_type = "regression"
    time_on = "timestamp"

    # Splits
    splits_comment = """
        We always use 6 month of the data as test data and all prior data as training data. This simulate a model that is refit every half year. We create 5 splits going back 6 months each, starting from the newest date.
    """
    time_horizon = 6
    time_horizon_unit = "months"
    temporal_splits = TemporalSplits(window=6, unit="months", n_windows=5)

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # From: https://github.com/yandex-research/tabred/blob/main/preprocessing/sberbank-housing.py
        data = pl.read_csv(
            zipfile.ZipFile(raw_dir / "train.csv.zip").read("train.csv"), null_values=["NA"], infer_schema_length=30_000
        ).with_columns(pl.col("timestamp").str.strptime(pl.Date))
        data_macro = (
            pl.read_csv(
                zipfile.ZipFile(raw_dir / "macro.csv.zip").read("macro.csv"),
                null_values=["NA"],
                infer_schema_length=30_000,
            )
            .with_columns(
                pl.col("timestamp").str.strptime(pl.Date),
                pl.col("child_on_acc_pre_school").str.replace(",", ".").cast(pl.Float32, strict=False),
                pl.col("modern_education_share").str.replace(",", ".").cast(pl.Float32),
                pl.col("old_education_build_share").str.replace(",", ".").cast(pl.Float32),
            )
            .drop("provision_retail_space_modern_sqm")
        )  # this feature has one value except for nulls
        data_fixup = pl.read_excel(self.folder / "BAD_ADDRESS_FIX.xlsx").with_columns(
            pl.col(pl.Utf8).replace("NA", None)
        )
        return {"data": data, "data_macro": data_macro, "data_fixup": data_fixup}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        data, data_macro, data_fixup = raw["data"], raw["data_macro"], raw["data_fixup"]
        data = data.filter(
            pl.col("kremlin_km").ne(pl.col("kremlin_km").min()) | pl.col("id").is_in(data_fixup["id"])
        ).update(data_fixup, on="id")
        data = data.filter(
            pl.col("full_sq").gt(5.0)
            & pl.col("full_sq").ne(5326.0)
            & pl.col("price_doc").gt(1_000_000)
            & pl.col("price_doc").ne(2_000_000)
            & pl.col("price_doc").ne(3_000_000)
        )
        data = data.join(data_macro, on="timestamp")
        # log scale target as in TabRed
        data = data.with_columns((pl.col("price_doc") / pl.col("full_sq")).log().alias("price_doc"))
        data = data.to_pandas()
        cat_cols = [
            "ID_railroad_station_walk",
            "ID_railroad_station_avto",
            "ID_big_road1",
            "ID_big_road2",
            "ID_railroad_terminal",
            "ID_bus_terminal",
            "ecology",
            "material",
            "state",
            "sub_area",
            "product_type",
            "culture_objects_top_25",
            "thermal_power_plant_raion",
            "incineration_raion",
            "oil_chemistry_raion",
            "radiation_raion",
            "railroad_terminal_raion",
            "big_market_raion",
            "nuclear_reactor_raion",
            "detention_facility_raion",
            "water_1line",
            "big_road1_1line",
            "railroad_1line",
        ]
        data[cat_cols] = data[cat_cols].astype("category")
        data = data.drop(columns=["0_6_all", "7_14_all", "id"])
        data = data[~(data["build_year"] > data["timestamp"].dt.year)]
        data = data.reset_index(drop=True)
        df = data
        return df
