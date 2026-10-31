"""Curated dataset definition for `immoscout_german_house_prices` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import arff
import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary

# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "Energy_efficiency_class": [" H ", " G ", " F ", " E ", " D ", " C ", " B ", " A ", " A+ "],
    "Furnishing_quality": ["simple", "normal", "sophisticated", "luxury"],
}

# The scrape's English labels are permuted (curation notes): ImmoScout24's own code for each label, found by matching
# the houses to an April 2020 scrape that keeps the codes. None is the scrape's missing value; a code of None is
# ImmoScout24's "no information".
IS24_CODES = {
    "Condition": {
        "modernized": "well_kept",
        "refurbished": "need_of_renovation",
        "dilapidated": "mint_condition",
        "maintained": None,
        "renovated": "modernized",
        "fixer-upper": "refurbished",
        "first occupation after refurbishment": "fully_renovated",
        "first occupation": "first_time_use_after_refurbishment",
        "by arrangement": "negotiable",
        "as new": "ripe_for_demolition",
        None: "first_time_use",
    },
    "Furnishing_quality": {
        "refined": "simple",
        "normal": "normal",
        "basic": None,
        "luxus": "luxury",
        None: "sophisticated",
    },
    "Type": {
        "Mid-terrace house": "single_family_house",
        "Duplex": "multi_family_house",
        "Single dwelling": "semidetached_house",
        "Villa": "villa",
        "Farmhouse": "mid_terrace_house",
        "Residential property": None,
        "Multiple dwelling": "end_terrace_house",
        "Bungalow": "special_real_estate",
        "Special property": "bungalow",
        "Corner house": "farmhouse",
        "Castle": "castle_manor_house",
        None: "other",
    },
    "Heating": {
        "stove heating": "central_heating",
        "central heating": None,
        "heat pump": "gas_heating",
        "oil heating": "floor_heating",
        "underfloor heating": "stove_heating",
        "night storage heater": "self_contained_central_heating",
        "district heating": "heat_pump",
        "wood-pellet heating": "electric_heating",
        "floor heating": "night_storage_heater",
        "electric heating": "district_heating",
        "gas heating": "wood_pellet_heating",
        "cogeneration units": "combined_heat_and_power_plant",
        "solar heating": "solar_heating",
        None: "oil_heating",
    },
}


class ImmoscoutGermanHousePrices(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="At what price will a house for sale in Germany be listed?",
        use_case=("A seller or agent sets the asking price of a house from the other houses currently on the market."),
        row=(
            "One house listed for sale on the German property portal ImmoScout24, from one scrape of 14 July 2020 "
            "(10,317 houses across the 16 states)."
        ),
        predicted="The asking price in euros, on a log scale; the sale price is not in the data.",
        known=(
            "The house type, living space, lot and usable area, rooms, bedrooms, bathrooms, floors, year built and "
            "renovated, furnishing quality, condition, heating, energy certificate, class and source, garages, and "
            "the state, city and place."
        ),
        split=(
            "Random listings of the same snapshot, so the test data stands for other houses on the market at the same"
            " time."
        ),
        changes=(
            'We drop listings priced under 10,000 euros (mostly 0, likely "price on request") or with under 10 square'
            " metres of living space, and listings repeated with identical features."
        ),
        fit="direct",
        fit_reason=(
            "The features are what a seller knows when listing, and the other listings of the same snapshot are the "
            "market the price is set in. Price trends over time are not covered."
        ),
    )

    # Dataset
    unique_name = "immoscout_german_house_prices"
    year = "2020"
    domain = "business & marketing"
    source = "Kaggle"  # original source Kaggle, download source OpenML.
    source_url = "https://www.openml.org/d/43342"
    license = "CC BY-NC-SA 4.0"  # From OpenML, no idea about the original license as it was on Kaggle.
    download_description = """
        We download the data from OpenML (original Kaggle dataset has been deleted).

        Also available at:
        - https://www.kaggle.com/code/shritech1404/german-housing-price-prediction (reference only, original dataset deleted)

        wget https://www.openml.org/data/download/22102167/dataset -O dataset.arff && mkdir -p local-data-warehouse/immoscout_german_house_prices && mv dataset.arff local-data-warehouse/immoscout_german_house_prices/
    """
    bibtex = r"""
        @misc{OpenML43342Dataset,
          author = {{OpenML}},
          title  = {ImmoScout24 OpenML Dataset 43342},
          year   = {2023},
          howpublished = {\url{https://www.openml.org/d/43342}},
          note   = {OpenML dataset}
        }
        @misc{Shritech2020GermanHousingPricePrediction,
          author = {shritech1404},
          title  = {German Housing Price Prediction},
          year   = {2020},
          howpublished = {\url{https://www.kaggle.com/code/shritech1404/german-housing-price-prediction}},
          note   = {Kaggle notebook}
        }
    """
    bibtex_key = "Shritech2020GermanHousingPricePrediction,OpenML43342Dataset"
    curation_comments = """
        - The data first appeared on Kaggle as the dataset `german-house-prices` (file `germany_housing_data_14.07.2020.csv`, scraped from ImmoScout24 on 14 July 2020). It has since been deleted and its owner is unknown, so `source` is Kaggle and `source_url` points to the copy on OpenML (43342, uploaded 2022-03-23), which carries the Kaggle card's text.
        We treat this as an IID time-independent task, because the prices is not sold prices but instead the offer price, so the snapshot here represents a task where someone would want to predict the price they should offer for their house given other houses that are currently on the market. Thus, it seems like a real IID task where someone would want to build a model to know how much they should offer their houses at in the current market (with the limitation that past trends are ignored)

        - We log scale it, as is appropriate for house price prediction tasks. We do not normalize by lot or living space, as both houses with a lot of land and small living space and houses with a lot of living space and small land are interesting to predict the price of, and normalization would bias towards one of them, as both cannot be homogenised.
        - We drop Free_of_Relation as it indicates a (mostly) price-independent variable; showing logistic information. Note that this column also indicates that the houses are most likely from the same time, further justifying our use case of an IID task.
        - We drop all cases where the price is less than 10k (most of which have a price of 0) as we think this might be a data error, or a case where the price is put to 0 to be marked as "price on request" (which is common in house listings).
        - We drop all duplicates as these are most likely repeated entries given the feature space.
        - `Condition`, `Furnishing_quality`, `Type` and `Heating` carry ImmoScout24's own codes (`IS24_CODES`; the
          curator's marks of 2026-10-31, CLEAN-12): the scrape's English labels are permuted, and in each column the
          missing value took a real label while one real level became missing. "dilapidated" (1,137 houses) has the
          newest median year built (2010) and the highest price, "as new" (11) the oldest (1870). The codes come from a
          match: 3,548 of the 10,552 houses are also in an ImmoScout24 scrape of April 2020 that keeps the portal's
          codes (Kaggle `phanindraparashar/germany-housing-rent-and-price-data-set-apr-20`, `apr20_price.csv`),
          matched exactly on state, living space, lot and rooms, then on year built and price within 0.8-1.25, and
          only where one house fits. The pairs are the same houses (energy class agrees for 99.5%, year renovated
          98.4%, floors 99.1%), and each label maps to one code for 93-100% of its matched houses (96-100% where
          price and year built agree exactly); the levels' median year built and price per m2 match the April codes'
          over the whole file. "maintained", "basic", "Residential property" and "central heating" are ImmoScout24's
          "no information" (missing); the missing values are first occupation (new builds), upscale, other and oil
          heating. `Furnishing_quality` is then ImmoScout24's scale simple < normal < sophisticated < luxury;
          `Condition` stays unordered, as "negotiable" is no state and "well_kept" does not sit against the
          renovation levels. No copy with the German labels and no scraper code were found; the Kaggle upload is
          deleted.
        - We drop all rows where the living space is less than 10 (in Germany, this would likely not be enough living space for a real house, and thus might be a data error.
        - Ordinal scales (2026-10-30, the curator's marks of 2026-10-31, CLEAN-14): 2 columns are ordered categories in
          the order of the source's codebook (`ORDINAL_LEVELS`).
    """

    # Task
    target = "LogPrice"
    problem_type = "regression"
    metric = Metric.from_context(
        "rmsle",
        reason="A scraped Kaggle dataset (since deleted) and its OpenML copy; neither defines a task or metric. For an asking price the error that matters is relative to the price, so RMSLE on the price.",
        target_transform="log",
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        with open(raw_dir / "dataset.arff") as f:
            data = arff.load(f)
        df = pd.DataFrame(data["data"], columns=[attr[0] for attr in data["attributes"]])
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # ImmoScout24's codes for the permuted labels; an unknown label raises
        for col, codes in IS24_CODES.items():
            df[col] = [codes[None if pd.isna(v) else v] for v in df[col]]
        # Data realistic drops
        df = df[df["Price"] >= 10000]
        df = df[df["Living_space"] >= 10]
        # Normalize target
        df["LogPrice"] = np.log(df["Price"])
        # Drop cols
        df = df.drop(
            columns=[
                "Unnamed:_0",
                "Price",
                "Free_of_Relation",
            ]
        )
        # Drop duplicates ignoring the target
        df = df.drop_duplicates(subset=[c for c in df.columns if c != self.task_metadata.target_column_name])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal=ORDINAL_LEVELS,
            categorical=[
                "Type",
                "Furnishing_quality",
                "Condition",
                "Heating",
                "Energy_certificate",
                "Energy_certificate_type",
                "Energy_efficiency_class",
                "Garagetype",
            ],
            string=[
                "Energy_source",
                "State",
                "City",
                "Place",
            ],
        )
