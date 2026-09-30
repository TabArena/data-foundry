"""Curated dataset definition for `california_house_prices_2020` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, TemporalSplits


class CaliforniaHousePrices2020(AbstractCuratedDataset):
    # Dataset
    unique_name = "california_house_prices_2020"
    year = "2021"
    domain = "business & marketing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/competitions/california-house-prices/data?select=train.csv"
    license = "Custom Kaggle Competition Rules"
    data_tags = ("Spatial",)
    download_description = """
        We utilize the train.csv from the Kaggle competition. We use the following commands to download and organize the data:

        kaggle competitions download -c california-house-prices -f train.csv && unzip train.csv.zip train.csv && rm train.csv.zip
        mkdir -p local-data-warehouse/california_house_prices_2020 && mv train.csv local-data-warehouse/california_house_prices_2020
    """
    bibtex = r"""
        @misc{d2lcourse2021california_house_prices,
          author       = {d2lcourse},
          title        = {California House Prices},
          year         = {2021},
          howpublished = {\url{https://kaggle.com/competitions/california-house-prices}},
          note         = {Kaggle}
        }
    """
    curation_comments = """
        We follow some common preprocessing steps from Kaggle and enhance features as much as possible.

        We found out that the data was web scraped from redfin.com and that the houses are ordered by the time they were sold such that a house with a higher ID was sold later. We confirmed this by looking at the history of various houses on redfin.com that we found in the dataset and checking their order in the ID with the time they were sold. Houses with a higher ID were sold later.

        - We log scale the target variable.
        - We do not have the exact dates but we know a higher ID means a later sale. We name the ID column accordingly to "time_index" and use it as a time feature.
        - The descriptions did contain the last sold price with a standard phrase such as "This home last sold for $X in January 2020. The Zestimate for this house is $Y The Rent Zestimate for this home is $Z/mo.". In these cases $X is identical to the target variable. Given such a drastic data leakage, we remove all rows (5413) that contain this phrase in the description to ensure they are not different in other ways too.
        - Note, sometime descriptions are missing and we intend that models/pipelines need to be able to handle this.
        - When investigating the "Lot" column we found many cases where the lot size (given in sq ft) is incorrect compared to the official lot size on the internet. The parser seems to have had an issue because the website often incorrectly showed the sq ft but gave the unit as acres. We found cases that were wrong by checking the acres size of the houses and anything with more than 2000 acres was investigated and subsequently corrected.
        - We parsed the bedrooms with a proxy following Kaggle and added an additional column containing only the semi-free text descriptions of the bedrooms.
        - We fix the parser errors for two cases for total interior livable area that were clear outliers based on the real data on redfin.
        - Garage and total space were in most cases the same values parsed from different fields. We keep Garage space and add an 'Extra Space' column that is the difference between total and garage space as an additional feature. This results in some cases with negative extra space that are most likely parser errors. We set them to nan. Note, we observed that that garage space number is in many cases a parsing error and does not reflect the real garage count.
        - The data has a lot of spatial features that are already semi-resolved to distances. This could be further enhanced using the address information. We leave it to the pipeline to handle this, if at all.
        - The dataset contains many text-like many categorical that are also high-cardinality, so perfect string data.
        - We drop all entries from the State of Arizona (AZ) as they are only a small fraction (n=431 after our preprocessing). The dataset is specified to be for California house prices.
        - We treat ZIP codes as strings. But we add a new categorical features that puts zip code in to approximate relevant buckets of regions.
        - We fixed one entry that had a negative value for garage space, likely due to a typo. This error still exists on the website.
        - After all the above preprocessing, there exist 63 houses that appear multiple times in the dataset (same address, zip code, year built). We only keep the newest entry to avoid group-related target leakage.
    """

    # Task
    target = "Sold Price"
    problem_type = "regression"
    time_on = "time_index"

    # Splits
    splits_comment = """
        We create a sklearn TimeSeriesSplit with 3 splits. We treat each split as a separate repeat with one fold. Each fold has 25% of the original data as test set. We simulate as if we deploy a model at a time point x, for the next time period (e.g. for a whole next year like in the original competition task). As we do not know the time periods from the time_index, we split based on number of samples.
    """
    time_horizon = 10382
    time_horizon_unit = "steps"
    temporal_splits = TemporalSplits(window=None, unit="rows", n_windows=3, min_train_fraction=0.25)

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "train.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.rename(
            columns={
                "Id": "time_index",
            }
        )
        as_date_cols = ["Listed On", "Last Sold On"]
        as_string_cols = [
            "Summary",
            "Type",
            "Heating",
            "Cooling",
            "Parking",
            "Region",
            "Elementary School",
            "Middle School",
            "High School",
            "Flooring",
            "Heating features",
            "Cooling features",
            "Appliances included",
            "Laundry features",
            "Parking features",
            "City",
            "Address",
            "State",
        ]
        # Remove rows with target leakage in description
        leak_mask = ~df["Summary"].isna() & (df["Summary"].str.contains("last sold for"))
        df = df[~leak_mask]
        # Set wrongly parsed years to NaN
        df.loc[df["Year built"].isin([0, 19, 9999, 1471, 2281]), "Year built"] = np.nan
        # Fix wrong lot sizes
        #   - found by: wrong_lot_size_mask = (df["Lot"]/43560) > 2000
        for time_index, correct_size in [
            (1701, 6660),
            (5198, 5500),
            (11205, 5768),
            (16036, 4200),
            (17241, 7650),
            (19469, 60984),
            (23605, 7700),
            (23807, 35283.6),
            (30942, 4500),
            (31871, 6500),
            (34622, 6403),
            (39769, 2584),
            (43009, 7546),
            # still says acres
            (13280, 5804),
            (46033, 6216),
        ]:
            df.loc[df["time_index"] == time_index, "Lot"] = correct_size
        assert ((df["Lot"] / 43560) > 2000).sum() == 0, "There are still wrong lot sizes > 2000 acres"
        # Ensure dtypes
        c = "Year built"  # special case
        nan_mask = df[c].isna()
        df.loc[nan_mask, c] = df.loc[~df[c].isna(), c].iloc[0]
        df[c] = pd.to_datetime(df[c].astype(int).astype(str), errors="raise")
        df.loc[nan_mask, c] = pd.NaT
        for c in as_date_cols:
            nan_mask = df[c].isna()
            df.loc[nan_mask, c] = df.loc[~df[c].isna(), c].iloc[0]  # Temp fill to allow conversion
            df[c] = pd.to_datetime(df[c], errors="raise")
            df.loc[nan_mask, c] = pd.NaT
        c = "Zip"  # ensure zip string is without .0 at the end.
        nan_mask = df[c].isna()
        df[c] = df[c].astype("string")
        df.loc[nan_mask, c] = np.nan
        df.loc[~nan_mask, c] = df.loc[~nan_mask, c].astype(int).astype("string")
        for c in as_string_cols:
            nan_mask = df[c].isna()
            df.loc[nan_mask, c] = np.nan
            df[c] = df[c].astype("string")
        # Extra FE for Bedrooms
        bedroom_description_mask = pd.to_numeric(df["Bedrooms"], errors="coerce").isna()
        df["Bedrooms_description"] = df["Bedrooms"].astype("string")
        df.loc[(~bedroom_description_mask) | (df["Bedrooms"].isna()), "Bedrooms_description"] = np.nan
        df["Bedrooms_description"] = df["Bedrooms_description"].astype("string")

        # Compute a proxy for bedrooms from the description
        # https://www.kaggle.com/code/wuwawa/automl-using-h2o
        def bedroom_proxy(x):
            if not pd.isna(x) and not x.isdigit():
                temp = x.split(",")
                n = len(x.split(","))
                if "Walk-in Closet" in temp:
                    n -= 1
                if "Reverse Floor Plan" in temp:
                    n -= 1
                if n <= 0:
                    n = np.nan
                return n
            return x

        df.loc[bedroom_description_mask, "Bedrooms"] = df.loc[bedroom_description_mask, "Bedrooms"].apply(bedroom_proxy)
        df["Bedrooms"] = pd.to_numeric(df["Bedrooms"], errors="coerce")
        # Fix wrong sqft parsing outliers
        for time_index, correct_size in [
            (43911, 702),
            (26533, 700),
        ]:
            df.loc[df["time_index"] == time_index, "Total interior livable area"] = correct_size
        # Add extra space and remove total space duplicates
        df.loc[df["time_index"] == 41450, "Garage spaces"] = 5  # fix data error
        df["Extra Space"] = df["Total spaces"] - df["Garage spaces"]
        df.loc[df["Extra Space"] < 0, "Extra Space"] = np.nan
        df = df.drop(columns=["Total spaces"])
        # Drop entries from AZ state
        df = df[df["State"] != "AZ"]
        df = df.drop(columns=["State"])

        # Zip code buckets for CA
        def zip_buckets(x):
            if pd.isna(x):
                return np.nan

            x = int(x)

            if x < 91911:
                return "Southern California / LA Area"

            if x < 93000:
                return "San Diego Area"
            if x < 94000:
                return "Central California"
            if x < 95200:
                return "San Francisco Bay Area"
            if x < 97000:
                return "Northern California"

            raise ValueError(f"Unexpected zip code: {x}")

        df["Zip Region"] = df["Zip"].apply(zip_buckets).astype("category")
        # Only keep the newest entry for houses that appear multiple times
        n_data = len(df)
        idx = df.groupby(["Address", "Zip", "Year built"], dropna=False)["time_index"].idxmax()
        df = df.loc[idx].reset_index(drop=True)
        assert (
            n_data - len(df) == 67
        )  # We have 63 houses with multiple entries (either 2 or 3) for a total of 130 entire. We keep one entry per house, thus 130 - 63 = 67
        # Log scale target as it is exp distributed
        df[self.task_metadata.target_column_name] = np.log1p(df[self.task_metadata.target_column_name])
        # Rest time_index (to avoid gaps from dropping rows)
        df = df.drop(columns=["time_index"]).reset_index().rename(columns={"index": "time_index"})
        return df
