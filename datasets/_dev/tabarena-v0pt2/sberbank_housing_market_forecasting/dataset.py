"""Curated dataset definition for `sberbank_housing_market_forecasting` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import zipfile
from pathlib import Path
from typing import TYPE_CHECKING

import polars as pl
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TaskSummary, Temporal, TemporalSplits

if TYPE_CHECKING:
    import pandas as pd


class SberbankHousingMarketForecasting(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What will a Moscow flat sell for, per square metre?",
        use_case=(
            "Sberbank predicts the price of a flat when it is sold, so that renters, developers and lenders can be "
            "more confident when they sign (the Kaggle competition's purpose)."
        ),
        row=(
            "One sale of a flat in Moscow, August 2011 to June 2015 (27,195 sales), either an owner-occupier purchase"
            " or an investment."
        ),
        predicted="The sale price per square metre of total area, on a logarithmic scale.",
        known=(
            "The flat (areas, floor, number of floors, rooms, build year, material, condition, purchase type), its "
            "district's population, schools, facilities, ecology and distances to points of interest, and the "
            "macroeconomic indicators of the sale date."
        ),
        split=(
            "Five test windows of six months, from January 2013 to June 2015, newest first; each trains on every "
            "earlier sale, as for a model refit every half year."
        ),
        changes=(
            "Following the TabReD benchmark, the target is the price per square metre, and we drop sales at prices up"
            " to 1 million rubles or of exactly 2 or 3 million, flats of 5 square metres or less, and flats built "
            "after their sale."
        ),
        fit="direct",
        fit_reason=(
            "The flat's and district's figures are known at the sale, and the half-year windows match a model refit "
            "twice a year. Whether every macroeconomic indicator joined on the sale date was already published then "
            "is not stated."
        ),
    )

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
        @misc{Matveev2017SberbankRussianHousingMarket,
          author = {Alex Matveev and Anastasia Sidorova and DataCanary},
          title  = {Sberbank Russian Housing Market},
          year   = {2017},
          howpublished = {\url{https://kaggle.com/competitions/sberbank-russian-housing-market}},
          note   = {Kaggle competition}
        }
    """
    curation_comments = """
        We follow the preprocessing from TabRed (https://github.com/yandex-research/tabred/tree/main/preprocessing#sberbank-housing-market-forecasting).

        - The target is log(price_doc / full_sq), the log of the sale price per square metre of total area (TabReD,
          after the first-place solution).
        - Address fix: 603 sales whose address could not be located carry the distances of central Moscow (the
          smallest `kremlin_km`). The hosts posted location features for 550 of them in Kaggle discussion 34364
          (BAD_ADDRESS_FIX.xlsx, taken from the nearest known building); we apply them and drop the other 53.
        - As TabReD, we drop sales at 1 million rubles or less or at exactly 2 or 3 million (fake low prices, by the
          first-place report often set to avoid tax), and flats with a total area of 5 m2 or less or of 5326 m2 (a
          typo for 53).
        - We join macro.csv on the sale date. Market prices (exchange rates, oil, stock indices) are daily; monthly,
          quarterly and annual statistics change on the first day of their period, and `gdp_annual` on a 2014 sale is
          Russia's 2013 GDP. The source does not say when each figure was published, so some may postdate the sale.
        - We drop two duplicated columns with the same values as other columns: "0_6_all", "7_14_all"
        - We drop the ID column as it does not provide information.
        - Note, the dataset contains a lot of spatial feature and even more already decoded spatial information (like distances to various points of interest).
        - We drop the 1,126 sales whose build_year is later than the year of sale. The column is described as "year built", not "year to be finished", so we treat them as errors. Only 2 of them have a build_year coded from a range such as "2000-2005"; the other 1,124 were sold 0 to 4 years before it, which may be flats sold before completion.
    """

    # Task
    target = "price_doc"
    problem_type = "regression"

    # Splits
    splits_comment = """
        We always use 6 month of the data as test data and all prior data as training data. This simulate a model that is refit every half year. We create 5 splits going back 6 months each, starting from the newest date.
    """
    temporal = Temporal(
        on="timestamp",
        splits=TemporalSplits(window=6, unit="months", n_windows=5),
    )

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
        data = data.drop(columns=["0_6_all", "7_14_all", "id"])
        data = data[~(data["build_year"] > data["timestamp"].dt.year)]
        data = data.reset_index(drop=True)
        df = data
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                # 1-4; the one row with 33 (id 10092, likely a typo for 3) also has the range-coded build_year
                # 20052009 and is dropped by the build-year filter
                "state",
                "ID_railroad_station_walk",
                "ID_railroad_station_avto",
                "ID_big_road1",
                "ID_big_road2",
                "ID_railroad_terminal",
                "ID_bus_terminal",
                "ecology",
                "material",
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
            ],
        )
