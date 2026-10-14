"""Curated dataset definition for `immoscout_german_house_prices` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import arff
import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TaskSummary


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
        - We drop all rows where the living space is less than 10 (in Germany, this would likely not be enough living space for a real house, and thus might be a data error.
    """

    # Task
    target = "LogPrice"
    problem_type = "regression"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        with open(raw_dir / "dataset.arff") as f:
            data = arff.load(f)
        df = pd.DataFrame(data["data"], columns=[attr[0] for attr in data["attributes"]])
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
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
