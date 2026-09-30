"""Curated dataset definition for `otto_group_product_classification_challenge` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class OttoGroupProductClassificationChallenge(AbstractCuratedDataset):
    # Dataset
    unique_name = "otto_group_product_classification_challenge"
    year = "2015"
    domain = "business & marketing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/competitions/otto-group-product-classification-challenge"
    license = "Kaggle Competition Rules"
    data_tags = ("Anonymized",)
    download_description = """
        We use the train.csv from the Kaggle competition.

        kaggle competitions download -c otto-group-product-classification-challenge -f train.csv && unzip train.csv.zip &&  rm train.csv.zip
        mkdir -p local-data-warehouse/otto_group_product_classification_challenge && mv train.csv local-data-warehouse/otto_group_product_classification_challenge/
    """
    bibtex = r"""
        @misc{Bossan2015OttoGroupProductClassificationChallenge,
          author = {Benjamin Bossan and Josef Feigl and Wendy Kan},
          title  = {Otto Group Product Classification Challenge},
          year   = {2015},
          howpublished = {\url{https://kaggle.com/competitions/otto-group-product-classification-challenge}},
          note   = {Kaggle competition}
        }
    """
    curation_comments = """
        We start with the train.csv from Kaggle.

        - The data has been anonymized, so feature meanings are unknown.
        - Features and data is clean. Top Kaggle experts applied no relevant preprocessing.
        - We drop the index column.
    """

    # Task
    target = "target"
    problem_type = "multiclass_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "train.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.drop(columns=["id"])
        return df


# MIGRATE: the v1 notebook did not shuffle; v2 shuffles IID/grouped data (set `shuffle = False` if the order matters)
