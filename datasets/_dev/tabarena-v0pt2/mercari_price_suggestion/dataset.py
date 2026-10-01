"""Curated dataset definition for `mercari_price_suggestion` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class MercariPriceSuggestion(AbstractCuratedDataset):
    # Dataset
    unique_name = "mercari_price_suggestion"
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
        - We take the full data (about 1.48M rows after de-duplication) with 3-fold cross-validation, so every fold trains on about 990k rows. Until 2026-10 a `mercari_price_suggestion_1m` version sub-sampled it to one 1M / 250k split.
    """

    # Task
    target = "price"
    problem_type = "regression"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "train.tsv", sep="\t")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df["price"] = np.log1p(df["price"])
        df = df.drop(columns=["train_id"])
        df["item_description"] = df["item_description"].replace("No description yet", np.nan)
        # Drop duplicates
        df = df.drop_duplicates()
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "item_condition_id",
                "shipping",
            ],
            string=[
                "name",
                "category_name",  # multi-categorical, not just one category name!
                "brand_name",
                "item_description",
            ],
        )
