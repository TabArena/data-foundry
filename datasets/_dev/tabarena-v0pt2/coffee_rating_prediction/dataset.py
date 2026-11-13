"""Curated dataset definition for `coffee_rating_prediction` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, Source, TaskSummary, Temporal, TemporalSplits

# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "roast": ["Light", "Medium-Light", "Medium", "Medium-Dark", "Dark"],
}


class CoffeeRatingPrediction(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What overall score will Coffee Review give a coffee?",
        use_case=(
            "For example, a roaster or importer predicts the overall score one specific rating service, here Coffee "
            "Review, would give a coffee, to decide which coffees to submit for review, stock or feature; the model "
            "learns that service's scoring, not a general measure of quality."
        ),
        row="One coffee reviewed by Coffee Review (coffeereview.com), October 2018 to September 2023.",
        predicted="The review's overall score on a 100-point scale (82 to 98 here, mean 93).",
        known=(
            "The roaster and its location, the coffee's name and origin, the roast level and roast colour readings, "
            "the price per gram in US dollars; the review month orders the split but is no model input."
        ),
        split=(
            "Thirteen test periods of two months, walking back from the newest review, each with every earlier review"
            " for training, as for a model refit every two months."
        ),
        changes=(
            "We drop the scores for aroma, acidity, body, flavour, aftertaste and with milk, which make up the "
            "overall score, the review notes, which can mention awards, and the two passages of the review that "
            "describe the coffee's taste and sum it up, which the reviewer writes with the score. We convert the "
            "prices in New Taiwan dollars to US dollars."
        ),
        fit="approximate",
        fit_reason=(
            "The features are what a roaster knows before the review, but one rating service stands for the quality "
            "a buyer meets, and the time from a roaster's submission to the review is not stated."
        ),
    )

    # Dataset
    unique_name = "coffee_rating_prediction"
    domain = "business & marketing"
    sources = (
        Source(
            role="publication",
            platform="Kaggle",
            url="https://www.kaggle.com/datasets/hanifalirsyad/coffee-scrap-coffeereview",
            license=None,  # Kaggle says "Other (specified in description)", and the description names none
            year="2023",
            bibtex=r"""
                @misc{AlIrsyad2023CoffeeDataCoffeeReview,
                  author = {Hanif Al Irsyad},
                  title  = {Coffee Data CoffeeReview},
                  year   = {2023},
                  howpublished = {\url{https://www.kaggle.com/datasets/hanifalirsyad/coffee-scrap-coffeereview}},
                  note   = {Kaggle dataset}
                }
            """,
        ),
    )
    data_tags = ("Spatial",)
    download_description = """
        We download the data from Kaggle, which comes from scrapping www.coffeereview.com.

        kaggle datasets download hanifalirsyad/coffee-scrap-coffeereview -f coffee_clean.csv && unzip coffee_clean.csv.zip && rm coffee_clean.csv.zip
        mkdir -p local-data-warehouse/coffee_rating_prediction && mv coffee_clean.csv local-data-warehouse/coffee_rating_prediction
    """
    curation_comments = """
        We start with the Kaggle version. Note, we acknowledge that the dataset is not of the highest quality and likely does not represent a real-world prediction task. Nevertheless, it can be used to test models.

        - We drop slug as it is a unique identifier that does not have predictive power.
        - We drop desc_2 as it in general includes notes that may or may not be related to the coffee quality. Moreover, it sometimes leaks the rating (e.g. through award notes).
        - Dropped (Andrej, 2026-11-10; LEAK-10): desc_1 (the blind assessment) and desc_3 (the bottom line), the
          reviewer's passages written together with the score, one clause per sensory sub-score. A roaster has neither
          before the review; ridge on their TF-IDF alone reached skill 0.71 (RMSE 0.861 against the training mean's
          1.598 on the 13 windows) and beat every benchmark method. Exception to LEAK-35 (2026-11-10, Andrej): the
          passages alone explain most of the score (skill 0.71 against the rule's case of 0.25 to 0.67), and the use
          case's roaster predicts before the review; the roaster's own information keeps skill 0.34 to 0.36.
        - `review_date` orders and splits the rows and is no model input (`Temporal(..., feature=False)`): it arrives with the target (2026-11-12, Andrej). The roaster decides which coffees to submit before any review, and the month is the month Coffee Review published the score.
        - We drop all_text as it is a concatenation of desc_1, desc_2, and desc_3. And desc_2 includes data leakage (such as if the coffee won an award or not). Thus, we drop all_test.
        - We drop aroma, acid, body, flavor, aftertaste, and with_milk as they are all features of the rating and thus leaking the target. Any of them could be used as a target, we focus on the overall rating.
        - We parse agtron into a lower and upper value as float.
        - Note, the data contains several spatial features about locations. We do not resolve these.
        - The prices in New Taiwan dollars (606 coffees, all from Taiwanese roasters, written "NT $") were read as US
          dollars, as the parser split "NT" off the currency; they are converted at the table's NTD rate (0.031) and the
          `NT_price` flag is dropped (Andrej, 2026-11-10; CLEAN-21): the Taiwanese median price per gram falls from
          1.98 to 0.06, the others' range.
        - The price feature is extremely messy as a result of web scrapping. We resolve this feature as real tabular data (not from a web scrapper but from the database source), would have these information stored in a more structured way. We drop coffees that are measured in "capsules" units as they exist only 8 times and seem to be strong outliers. We normalizes the price to be per grams. Moreover, we convert all currencies to USD (with a fixed rate); we ignore the temporal incorrectness this may introduce as it is most likely minimal.
        - Ordinal scales (2026-10-30, the curator's marks of 2026-10-31 and 2026-11-01, CLEAN-14): 1 column is ordered
          categories in the order of the source's codebook (`ORDINAL_LEVELS`).
        - We drop the 2 reviews of October 2023, the scrape's partial last month (24 to 65 reviews a month in the rest of 2023; cross-dataset item of 2026-11-11, Lennart). The windows walk back from September 2023.
    """
    accepted_check_warnings = {
        "meta_license_unknown": (
            "Kaggle gives the licence as 'Other (specified in description)', but the description names none (checked "
            "2026-11-10)."
        ),
    }

    # Task
    target = "rating"
    problem_type = "regression"
    metric = Metric.fallback(
        reason="Scraped Kaggle dataset with no task, competition or paper; no metric defined.",
    )

    # Splits
    splits_comment = """
        We simulate a setting where we refit the model every 2 months and only test on the next 2 months, walking back
        from the newest review until the training data would fall below 50% of the rows (12 windows,
        August-September 2023 back to October-November 2021, 62 to 137 test reviews each). Monthly windows
        (25) would follow the split-count convention, but some months hold only 2-10 reviews, which makes per-window
        RMSE noise; 2-month windows keep at least ~50 test rows each.
        A score is published with its review month, so every training label is known when a window starts and no gap
        is needed; the time from a roaster's submission to the review is not stated. Reviews of one month share their
        scoring (the month explains 8% of the score's variance; some months are themed tastings), and whole two-month
        windows keep each month on one side.
    """
    temporal = Temporal(
        on="review_date",
        splits=TemporalSplits(window=2, unit="months", min_train_fraction=0.5),
        feature=False,  # the review month arrives with the score: no model input (2026-11-12, Andrej)
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "coffee_clean.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Ensure date time (parsed here: the sort at the end needs the date)
        df["review_date"] = pd.to_datetime(df["review_date"], format="%B %Y")
        # The scrape's partial last month: October 2023 holds 2 reviews (cross-dataset item of 2026-11-11).
        df = df.loc[df["review_date"] < "2023-10-01"].copy()
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
        # "NT $" is New Taiwan dollars: the regex splits "NT" off, so set the currency here (CLEAN-21; Andrej, 2026-11-10)
        df.loc[df["NT_price"] == "NT", "currency_raw"] = "NTD $"
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
        df = df.drop(columns=["unit_qty", "unit_raw", "price", "currency_raw", "price_per_gram", "NT_price"])
        # Drop columns
        df = df.drop(
            columns=[
                "slug",
                # the reviewer's passages, written with the score (Andrej, 2026-11-10)
                "desc_1",
                "desc_2",
                "desc_3",
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
        df = df.sort_values(by="review_date", kind="stable").reset_index(drop=True)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal=ORDINAL_LEVELS,
            categorical=[
                "roast",
            ],
            string=[
                "roaster",
                "name",
                "location",
                "origin",
            ],
            datetime={"review_date": "%B %Y"},
        )
