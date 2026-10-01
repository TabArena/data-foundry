"""Curated dataset definition for `santander_customer_satisfaction` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class SantanderCustomerSatisfaction(AbstractCuratedDataset):
    # Dataset
    unique_name = "santander_customer_satisfaction"
    year = "2016"
    domain = "business & marketing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/competitions/santander-customer-satisfaction"
    license = "Kaggle Competition Rules"
    data_tags = ("Anonymized",)
    download_description = """
        We use the train.csv from the Kaggle competition.

        kaggle competitions download -c santander-customer-satisfaction -f train.csv && unzip train.csv.zip &&  rm train.csv.zip
        mkdir -p local-data-warehouse/santander_customer_satisfaction && mv train.csv local-data-warehouse/santander_customer_satisfaction/
    """
    bibtex = r"""
        @misc{Jimenez2016SantanderCustomerSatisfaction,
          author = {Soraya Jimenez and Will Cukierski},
          title  = {Santander Customer Satisfaction},
          year   = {2016},
          howpublished = {\url{https://kaggle.com/competitions/santander-customer-satisfaction}},
          note   = {Kaggle competition}
        }
    """
    curation_comments = """
        We start with the train.csv from Kaggle.

        - The data has been anonymized, so feature meanings are unknown.
        - We remove duplicated columns and zero-variance columns.
        - We add a zero-count feature (number of zeros per row). #1 Kaggle experts also applied a lot of other features and feature selection but each experts used something different (https://www.kaggle.com/competitions/santander-customer-satisfaction/writeups/1-leustagos-3rd-place-solution).
        - We drop duplicates as their origin is unclear and they could create data leaks when splitting the training data.
        - We replace -999999 in var3 with with nan.
        - We keep the data otherwise as it. Several columns might be categorical and contain encoded nan values but we are not able to determine this due to anonymization.
    """

    # Task
    target = "TARGET"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "train.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # remove duplicated columns
        df = df.loc[:, ~df.T.duplicated()]
        # remove zero-variance columns
        df = df.loc[:, df.nunique(dropna=False) > 1]
        # add zero-count feature
        numeric_cols = df.drop(columns=["ID", "TARGET"])
        df["zero_count"] = (numeric_cols == 0).sum(axis=1)
        df = df.drop(columns=["ID"])
        # Drop duplicates w/o target col
        df = df.drop_duplicates(subset=df.columns.difference([self.task_metadata.target_column_name]))
        # Replace -999999 with np.nan
        df["var3"] = df["var3"].replace(-999999, np.nan)
        return df
