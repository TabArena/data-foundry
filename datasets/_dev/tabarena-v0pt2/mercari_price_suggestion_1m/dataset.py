"""Curated dataset definition for `mercari_price_suggestion_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class MercariPriceSuggestion1m(AbstractCuratedDataset):
    # Dataset
    unique_name = "mercari_price_suggestion_1m"
    version_of = "mercari_price_suggestion"
    version_comment = """
        We build the recommended single train/test split (250k test rows) and sub-sample it to at most 1M train and 250k test rows with `curation_recommendations.subsample_split_to_budget`.
    """
    year = "2018"
    domain = "business & marketing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/competitions/mercari-price-suggestion-challenge"
    license = "Kaggle Competition Rules"
    download_description = """
        train.tsv.7z

        kaggle competitions download -c mercari-price-suggestion-challenge -f train.tsv.7z && 7z x train.tsv.7z && rm train.tsv.7z
        mkdir -p local-data-warehouse/mercari_price_suggestion && mv train.tsv local-data-warehouse/mercari_price_suggestion
    """
    bibtex = r"""
        @misc{Howard2017MercariPriceSuggestionChallenge,
          author = {{Kaggle} and Addison Howard and kaoriiida and Kei Otagaki and Mark McDonald and mueno and Wendy Kan and Zhang and zyaga},
          title  = {Mercari Price Suggestion Challenge},
          year   = {2017},
          howpublished = {\url{https://kaggle.com/competitions/mercari-price-suggestion-challenge}},
          note   = {Kaggle competition}
        }
    """
    curation_comments = """
        We start from the Kaggle competition dataset.

        - We log1p scale the target to match the target metric of the competition by default RMSE.
        - The dataset was solved by Kaggle experts by tabular models and a lot of custom string preprocessing. So it is a great use case to test encoding pipelines! The dataset also has mostly string data.
        - The task was treated and solved as an IID task on Kaggle.
        - We replace "No description yet" with NaN.
    """

    # Task
    target = "price"
    problem_type = "regression"

    # Splits
    subsample_to_budget = True

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "train.tsv", sep="\t")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df["price"] = np.log1p(df["price"])
        df = df.drop(columns=["train_id"])
        df["item_description"] = df["item_description"].replace("No description yet", np.nan)
        as_string_dtype = [
            "name",
            "category_name",  # multi-categorical, not just one category name!
            "brand_name",
            "item_description",
        ]
        for c in as_string_dtype:
            nan_mask = df[c].isna()
            df.loc[nan_mask, c] = np.nan
            df[c] = df[c].astype("string")
        # Drop duplicates
        df = df.drop_duplicates()
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "item_condition_id",
                "shipping",
            ],
        )
