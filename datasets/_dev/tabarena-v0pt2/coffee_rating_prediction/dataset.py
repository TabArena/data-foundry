"""Curated dataset definition for `coffee_rating_prediction` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TemporalSplits


class CoffeeRatingPrediction(AbstractCuratedDataset):
    # Dataset
    unique_name = "coffee_rating_prediction"
    year = "2023"
    domain = "business & marketing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/hanifalirsyad/coffee-scrap-coffeereview"
    license = "None"
    data_tags = ("Spatial", "2ndTierData")
    download_description = """
        We download the data from Kaggle, which comes from scrapping www.coffeereview.com.

        kaggle datasets download hanifalirsyad/coffee-scrap-coffeereview -f coffee_clean.csv && unzip coffee_clean.csv.zip && rm coffee_clean.csv.zip
        mkdir -p local-data-warehouse/coffee_rating_prediction && mv coffee_clean.csv local-data-warehouse/coffee_rating_prediction
    """
    bibtex = r"""
        @misc{AlIrsyad2023CoffeeDataCoffeeReview,
          author = {Hanif Al Irsyad},
          title  = {Coffee Data CoffeeReview},
          year   = {2023},
          howpublished = {\url{https://www.kaggle.com/datasets/hanifalirsyad/coffee-scrap-coffeereview}},
          note   = {Kaggle dataset}
        }
    """
    curation_comments = """
        We start with the Kaggle version. Note, we acknowledge that the dataset is not of the highest quality and likely does not represent a real-world prediction task. Nevertheless, it can be used to test models.

        - We drop slug as it is a unique identifier that does not have predictive power.
        - We drop desc_2 as it in general includes notes that may or may not be related to the coffee quality. Moreover, it sometimes leaks the rating (e.g. through award notes). We only keep desc_1 and desc_3, which are mostly descriptions of the coffee.
        - We drop all_text as it is a concatenation of desc_1, desc_2, and desc_3. And desc_2 includes data leakage (such as if the coffee won an award or not). Thus, we drop all_test.
        - We drop aroma, acid, body, flavor, aftertaste, and with_milk as they are all features of the rating and thus leaking the target. Any of them could be used as a target, we focus on the overall rating.
        - We parse agtron into a lower and upper value as float.
        - Note, the data contains several spatial features about locations. We do not resolve these.
        - The price feature is extremely messy as a result of web scrapping. We resolve this feature as real tabular data (not from a web scrapper but from the database source), would have these information stored in a more structured way. We drop coffees that are measured in "capsules" units as they exist only 8 times and seem to be strong outliers. We normalizes the price to be per grams. Moreover, we convert all currencies to USD (with a fixed rate); we ignore the temporal incorrectness this may introduce as it is most likely minimal.
    """

    # Task
    target = "rating"
    problem_type = "regression"
    time_on = "review_date"

    # Splits
    splits_comment = """
        We simulate a setting where we refit the model every 2 months and only test on the next 2 months, walking back
        from the newest review until the training data would fall below 50% of the rows (13 windows). Monthly windows
        (26) would follow the split-count convention, but some months hold only 2-10 reviews, which makes per-window
        RMSE noise; 2-month windows keep at least ~50 test rows each.
    """
    time_horizon = 2
    time_horizon_unit = "months"
    temporal_splits = TemporalSplits(window=2, unit="months", min_train_fraction=0.5)

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "coffee_clean.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Ensure date time
        df["review_date"] = pd.to_datetime(df["review_date"], format="%B %Y")
        # Parse argton
        df[["agtron_lower", "agtron_upper"]] = df["agtron"].str.split("/", expand=True)
        df["agtron_lower"] = (
            df["agtron_lower"]
            .replace(
                {
                    "": np.nan,
                    "NA": np.nan,
                    # Fix parsing errors
                    "5252": "52",
                    "547": "54",
                    "555": "55",
                }
            )
            .astype(float)
        )
        df["agtron_upper"] = df["agtron_upper"].replace({"": np.nan, "NA": np.nan}).astype(float)
        # Parse est_price
        s = df["est_price"].astype("string")
        # --- normalize a bit (handles 'NT$650/230g', extra spaces, etc.)
        norm = (
            s.str.strip()
            .str.replace(r"\s+", " ", regex=True)
            .str.replace(r"NT\s*\$", "NT $", regex=True)  # NT$ -> NT $
            .str.replace(r"\$(?=\d)", "$", regex=True)  # keep $ tight to digits ok
        )
        # --- flag messy rows (parentheses, multiple prices separated by ';', or extra explanatory text)
        messy_pat = r"\(|\)|;|currently on sale|limited availability|includes shipping|available in store only|see website|more information"
        norm.str.contains(messy_pat, case=False, regex=True)
        norm = norm.replace(
            {
                # Handle all special cases
                "NA (available in store only)": pd.NA,
                "$32.00/boxed set (125 grams of this coffee plus 125 grams of an anaerobic-processed coffee from the same farm)": "$32.00/125 grams",
                "$280.00/70 grams; $200.00/50 grams": "$280.00/70 grams",
                "$4.00/12-ounce bottle; $20.00/6-pack": "$4.00/12-ounce bottle",
                "$18.00/4-12-ounce bottles; 32 ounces/$12; 64-ounces/$20.00": "$18.00/4-12-ounce bottles",
                "$3.00/sachet (plus one donated)": "$3.00/sachet",
                "$15.00/20 ounces (2 types)": "$15.00/20 ounces",
                "$45.95/8 ounces (currently on sale for $36.76)": "$45.95/8 ounces",
                "$15.00/12 ounces; $35.00/2 pounds": "$15.00/12 ounces",
                "$13.99/12 ounces ($79.00/5 pounds)": "$13.99/12 ounces",
                "$21.00/12 ounces (includes shipping)": "$21.00/12 ounces",
                "$16.00/12 ounces; $50.00/5 pounds": "$16.00/12 ounces",
                "€29.95/1 kilo (35.3 ounces)": "€29.95/1 kilo",
                "$125.00/4 ounces; limited availability": "$125.00/4 ounces",
                '$39.95/8 ounces (packaged as a "duo" with Bourbon Rey Guatemala)': "$39.95/8 ounces",
                '$39.95/8 ounces (packaged as a "duo" with the Bourbon Rey Jamaica)': "$39.95/8 ounces",
                "See website for more information": pd.NA,
            }
        )
        pat_clean = (
            r"^\s*(?:(?P<special>NT)\s*)?"
            r"(?P<currency>(?:USD|US|CAD|AUD|HKD|HK|AED|RMB|RM|IDR|KRW|NTD)\s*\$?|[\$€£¥])\s*"
            r"(?P<price>\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+(?:\.\d+)?)\s*/\s*"
            r"(?P<unit_qty>\d+(?:\.\d+)?)\s*"
            r"(?P<unit>ounces?|oz|grams?|g|ml|kilo|kg|pounds?|lb|capsules?|caps)\.?\s*$"
        )
        parsed = norm.str.extract(pat_clean)
        df["NT_price"] = parsed["special"]
        df["currency_raw"] = parsed["currency"]
        df["price"] = parsed["price"].str.replace(",", "", regex=False).astype("float")
        df["unit_qty"] = parsed["unit_qty"].astype("float")
        df["unit_raw"] = parsed["unit"].str.lower()
        # unify qty
        to_grams = {
            "g": 1,
            "grams": 1,
            "pounds": 453.59237,
            "kilo": 1000,
            "ounces": 28.349523125,
        }
        mask = df["unit_raw"].isin(list(to_grams.keys()))
        df.loc[mask, "unit_qty"] = df.loc[mask, "unit_qty"] * df.loc[mask, "unit_raw"].map(to_grams)
        df.loc[mask, "unit_raw"] = "grams"
        df = df[df["unit_raw"] != "capsules"].reset_index(drop=True)
        df["price_per_gram"] = df["price"] / df["unit_qty"]
        fx_to_usd = {
            "HKD $": 0.128,
            "HK $": 0.128,
            "CAD $": 0.74,
            "AUD $": 0.66,
            "USD $": 1.0,
            "US $": 1.0,
            "¥": 0.0067,
            "RMB": 0.14,
            "RMB ": 0.14,
            "£": 1.27,
            "€": 1.09,
            "NTD $": 0.031,
            "RM": 0.21,
            "RM ": 0.21,
            "AED $": 0.27,
            "IDR $": 0.000064,
            "KRW $": 0.00075,
            "$": 1.0,
        }
        assert set(df["currency_raw"].dropna().unique()).issubset(set(fx_to_usd.keys())), (
            f"Found currencies not in fx_to_usd mapping: {set(df['currency_raw'].dropna().unique()) - (set(fx_to_usd.keys()))}"
        )
        df["price_per_gram_in_usd"] = df["price_per_gram"] * df["currency_raw"].map(fx_to_usd)
        df = df.drop(columns=["unit_qty", "unit_raw", "price", "currency_raw", "price_per_gram"])
        as_str_column = [
            "roaster",
            "name",
            "location",
            "origin",
            "desc_1",
            "desc_3",
        ]
        for c in as_str_column:
            nan_mask = df[c].isna()
            df.loc[nan_mask, c] = np.nan
            df[c] = df[c].astype("string")
        # Drop columns
        df = df.drop(
            columns=[
                "slug",
                "desc_2",
                "all_text",
                "aroma",
                "acid",
                "body",
                "flavor",
                "aftertaste",
                "with_milk",
                "agtron",
                "est_price",
            ]
        )
        # drop the 1 duplicate row
        df = df.drop_duplicates()
        df = df.sort_values(by="review_date").reset_index(drop=True)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "roast",
                "NT_price",
            ],
        )
