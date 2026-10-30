"""Curated dataset definition for `sberbank_housing_market_forecasting` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import zipfile
from pathlib import Path
from typing import TYPE_CHECKING

import polars as pl
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Metric,
    TaskSummary,
    Temporal,
    TemporalSplits,
    set_missing,
)

if TYPE_CHECKING:
    import pandas as pd

MONTHLY = [
    "oil_urals",
    "cpi",
    "ppi",
    "balance_trade",
    "net_capital_export",
    "deposits_value",
    "deposits_growth",
    "deposits_rate",
    "mortgage_value",
    "mortgage_growth",
    "mortgage_rate",
    "income_per_cap",
    "fixed_basket",
    "rent_price_4+room_bus",
    "rent_price_3room_bus",
    "rent_price_2room_bus",
    "rent_price_1room_bus",
    "rent_price_3room_eco",
    "rent_price_2room_eco",
    "rent_price_1room_eco",
]
"""Macro columns with one value per month, the month's own (`oil_urals` of January 2015 is 46.3, that month's Urals
average; `income_per_cap` peaks in December). `deposits_value` and `deposits_growth` also change once in the middle of
six Augusts and Septembers. The model sees the value of one month before the sale."""

QUARTERLY = [
    "gdp_quart",
    "gdp_quart_growth",
    "balance_trade_growth",
    "average_provision_of_build_contract",
    "average_provision_of_build_contract_moscow",
]
"""Macro columns with one value per quarter. The model sees the value of one quarter before the sale. `gdp_quart`
already holds the previous quarter's GDP (the 2015 Q2 rows hold 2015 Q1's 18,209.7 bn rubles and growth of -2.8%), so
the model sees the GDP of two quarters back, as mortgage does."""

YEARLY_ALREADY_LAGGED = ["gdp_annual", "gdp_annual_growth"]
"""Yearly columns that already hold the previous year: the 2014 rows hold Russia's 2013 GDP (71,016.7 bn rubles) and
growth (1.3%). Kept as joined."""

YEARLY = [
    "gdp_deflator",
    "grp",
    "grp_growth",
    "real_dispos_income_per_cap_growth",
    "salary",
    "salary_growth",
    "retail_trade_turnover",
    "retail_trade_turnover_per_cap",
    "retail_trade_turnover_growth",
    "labor_force",
    "unemployment",
    "employment",
    "invest_fixed_capital_per_cap",
    "invest_fixed_assets",
    "profitable_enterpr_share",
    "unprofitable_enterpr_share",
    "share_own_revenues",
    "overdue_wages_per_cap",
    "fin_res_per_cap",
    "marriages_per_1000_cap",
    "divorce_rate",
    "construction_value",
    "invest_fixed_assets_phys",
    "pop_natural_increase",
    "pop_migration",
    "pop_total_inc",
    "childbirth",
    "mortality",
    "housing_fund_sqm",
    "lodging_sqm_per_cap",
    "water_pipes_share",
    "baths_share",
    "sewerage_share",
    "gas_share",
    "hot_water_share",
    "electric_stove_share",
    "heating_share",
    "old_house_share",
    "average_life_exp",
    "infant_mortarity_per_1000_cap",
    "perinatal_mort_per_1000_cap",
    "incidence_population",
    "load_of_teachers_preschool_per_teacher",
    "child_on_acc_pre_school",
    "load_of_teachers_school_per_teacher",
    "students_state_oneshift",
    "modern_education_share",
    "old_education_build_share",
    "provision_doctors",
    "provision_nurse",
    "load_on_doctors",
    "power_clinics",
    "hospital_beds_available_per_cap",
    "hospital_bed_occupancy_per_year",
    "provision_retail_space_sqm",
    "turnover_catering_per_cap",
    "theaters_viewers_per_1000_cap",
    "seats_theather_rfmin_per_100000_cap",
    "museum_visitis_per_100_cap",
    "bandwidth_sports",
    "population_reg_sports_share",
    "students_reg_sports_share",
    "apartment_build",
    "apartment_fund_sqm",
]
"""Macro columns with one value per calendar year, set from January 1 of the year it describes (Moscow's average
salary of 2014, 61,208 rubles, sits on every 2014 row) and published in the next year. The model sees the value of
one year before the sale."""

LAGS = {"1mo": MONTHLY, "3mo": QUARTERLY, "1y": YEARLY}
"""How far before the sale date each group of macro columns is read, and the suffix of its columns."""

SUFFIX = {"1mo": "_lag_1m", "3mo": "_lag_1q", "1y": "_lag_1y"}


# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "state": [1.0, 2.0, 3.0, 4.0],
    "ecology": ["poor", "satisfactory", "good", "excellent"],
}


class SberbankHousingMarketForecasting(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What will a Moscow flat sell for, per square metre?",
        use_case=(
            "Sberbank predicts the price of a flat when it is sold, so that renters, developers and lenders can be "
            "more confident when they sign (the Kaggle competition's purpose)."
        ),
        row=(
            "One sale of a flat in Moscow, August 2011 to June 2015 (28,321 sales), either an owner-occupier purchase"
            " or an investment."
        ),
        predicted="The sale price per square metre of total area, on a logarithmic scale.",
        known=(
            "The flat (areas, floor, number of floors, rooms, build year, material, condition, purchase type), its "
            "district's population, schools, facilities, ecology and distances to points of interest, the market "
            "prices of the sale date (exchange rates, oil, stock indices) and the monthly, quarterly and yearly "
            "economic statistics of one period before it."
        ),
        split=(
            "Five test windows of six months, from January 2013 to June 2015, newest first; each trains on every "
            "earlier sale, as for a model refit every half year."
        ),
        changes=(
            "Following the TabReD benchmark, the target is the price per square metre, and we drop sales at prices up"
            " to 1 million rubles or of exactly 2 or 3 million, and flats of 5 square metres or less. The economic "
            "statistics are those of the month, quarter or year before the sale, not of the sale's own period."
        ),
        fit="direct",
        fit_reason=(
            "The flat's and district's figures are known at the sale, and the half-year windows match a model refit "
            "twice a year. The economic statistics are lagged by one period because their release dates are not "
            "given; a monthly figure may still come out a few days after a sale early in the month."
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
          after the first-place solution); RMSE on it is the competition's RMSLE on `price_doc` (TP-6).
        - Address fix: 603 sales whose address could not be located carry the distances of central Moscow (the
          smallest `kremlin_km`). The hosts posted location features for 550 of them in Kaggle discussion 34364
          (BAD_ADDRESS_FIX.xlsx, taken from the nearest known building); we apply them and drop the other 53.
        - As TabReD, we drop sales at 1 million rubles or less or at exactly 2 or 3 million (fake low prices, by the
          first-place report often set to avoid tax), and flats with a total area of 5 m2 or less or of 5326 m2 (a
          typo for 53).
        - We join macro.csv on the sale date. Market prices (exchange rates, oil, stock indices) are daily and keep the
          sale date's value. The monthly, quarterly and yearly statistics hold their own period's value from its first
          day (published later; the source gives no release dates), so we read them one period before the sale, as
          mortgage lags its macro series to their release (LEAK-10; Lennart, 2026-10-21): 20 monthly columns one
          month back (`_lag_1m`), 5 quarterly one quarter back (`_lag_1q`) and 64 yearly one year back (`_lag_1y`).
          `gdp_quart` already holds the previous quarter, so the model sees GDP two quarters back; `gdp_annual` and
          `gdp_annual_growth` already hold the previous year (a 2014 sale has Russia's 2013 GDP) and are kept as
          joined.
        - We drop two duplicated columns with the same values as other columns: "0_6_all", "7_14_all"
        - We drop the ID column as it does not provide information.
        - Note, the dataset contains a lot of spatial feature and even more already decoded spatial information (like distances to various points of interest).
        - We keep the 1,126 sales whose build_year is later than the year of sale (Lennart, 2026-10-14; until then they were dropped as errors). 1,124 were sold 0 to 4 years before it, which fits flats sold before completion; 2 have a build_year coded from a range (such as 20052009), kept as it is.
        - Ordinal scales (2026-10-30, CLEAN-14): 2 columns typed as ordered categories in the order of the source's
          codebook (`ORDINAL_LEVELS`); their codes that mean unknown (don't know, refused, not asked) are missing
          (CLEAN-10).
    """

    # Task
    target = "price_doc"
    problem_type = "regression"
    metric = Metric.source(
        "rmse",
        original="Root Mean Squared Logarithmic Error (RMSLE) on price_doc",
        reference="https://www.kaggle.com/competitions/sberbank-russian-housing-market/overview/evaluation",
        definition=(
            "RMSE on log(price_doc / full_sq); since full_sq is known per row, log(price/sq) - "
            "log(price_hat/sq) = log(price) - log(price_hat), so this is the competition's RMSLE on the sale "
            "price up to log vs log1p (negligible at prices of 10^5 to 10^8 RUB)"
        ),
    )

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
        # The daily market prices of the sale date, and every monthly, quarterly and yearly statistic as of one
        # period before it (their release dates are not given; mortgage lags its macro series the same way). Each
        # statistic holds one value per period (deposits_value and deposits_growth change once within six months).
        lagged = [c for cols in LAGS.values() for c in cols]
        for period, cols in {
            "1mo": [c for c in MONTHLY if c not in ("deposits_value", "deposits_growth")],
            "1q": QUARTERLY,
            "1y": YEARLY,
        }.items():
            per_period = data_macro.group_by(pl.col("timestamp").dt.truncate(period), maintain_order=True).agg(
                pl.col(cols).drop_nulls()
            )
            assert per_period.select(pl.col(cols).list.n_unique().max()).max_horizontal().item() <= 1, period
        data = data.join(data_macro.drop(lagged), on="timestamp")
        for offset, cols in LAGS.items():
            data = data.with_columns(pl.col("timestamp").dt.offset_by(f"-{offset}").alias("_macro_date")).join(
                data_macro.select(
                    pl.col("timestamp").alias("_macro_date"), *[pl.col(c).alias(c + SUFFIX[offset]) for c in cols]
                ),
                on="_macro_date",
                how="left",
            )
        data = data.drop("_macro_date")
        # log scale target as in TabRed
        data = data.with_columns((pl.col("price_doc") / pl.col("full_sq")).log().alias("price_doc"))
        data = data.to_pandas()
        data = data.drop(columns=["0_6_all", "7_14_all", "id"])
        data = data.reset_index(drop=True)
        df = data
        # codes outside a scale that mean unknown (don't know, refused, not asked): missing (CLEAN-10)
        df = set_missing(
            df,
            {
                "state": [33.0],
                "ecology": ["no data"],
            },
        )
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal=ORDINAL_LEVELS,
            categorical=[
                # 1-4; the one row with 33 (id 10092, likely a typo for 3) also has the range-coded build_year
                # 20052009; both values are kept as they are
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
