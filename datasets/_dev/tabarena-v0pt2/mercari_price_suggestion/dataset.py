"""Curated dataset definition for `mercari_price_suggestion` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary

# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "item_condition_id": [5, 4, 3, 2, 1],
}


class MercariPriceSuggestion(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What price will a second-hand item sell for on the Mercari app?",
        use_case=(
            "When a seller lists an item on Mercari, the app suggests a price from the listing (the competition's "
            "stated aim)."
        ),
        row=(
            "One item listing on Mercari, a shopping app for second-hand goods (1,482,486 listings); the place and "
            "period are not stated."
        ),
        predicted="The price the item sold for, in US dollars, on a log scale.",
        known=(
            "The item's name, condition, category, brand, whether the seller pays shipping, and the seller's "
            "free-text description."
        ),
        split=(
            "Random listings, as in the competition, so the test data stands for other listings of the same period."
        ),
        fit="direct",
        fit_reason=(
            "Everything the model sees is what a seller enters when listing, and the label is the price a suggestion "
            "should hit. The release has no dates, so the split cannot follow time."
        ),
    )

    # Dataset
    unique_name = "mercari_price_suggestion"
    year = "2017"
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

        - We log1p scale the target; the metric is the competition's RMSLE on the price, computed after the inverse (`target_transform="log1p"`).
        - The dataset was solved by Kaggle experts by tabular models and a lot of custom string preprocessing. So it is a great use case to test encoding pipelines! The dataset also has mostly string data.
        - The task was treated and solved as an IID task on Kaggle.
        - We replace "No description yet" with NaN.
        - We take the full data (about 1.48M rows after de-duplication) with 3-fold cross-validation, so every fold trains on about 990k rows. Until 2026-10 a `mercari_price_suggestion_1m` version sub-sampled it to one 1M / 250k split.
        - Ordinal scales (2026-10-30, CLEAN-14): 1 columns typed as ordered categories in the order of the source's
          codebook (`ORDINAL_LEVELS`).
    """

    # Task
    target = "price"
    problem_type = "regression"
    metric = Metric.source(
        "rmsle",
        original="Root Mean Squared Logarithmic Error",
        reference="https://www.kaggle.com/competitions/mercari-price-suggestion-challenge/overview/evaluation",
        definition="sqrt(mean((log1p(p) - log1p(a))^2)) of the price in US dollars, computed after the inverse of the "
        "shipped log1p(price)",
        target_transform="log1p",
    )

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
            ordinal=ORDINAL_LEVELS,
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
