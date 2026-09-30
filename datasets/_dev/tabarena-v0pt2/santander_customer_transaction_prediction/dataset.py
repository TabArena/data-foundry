"""Curated dataset definition for `santander_customer_transaction_prediction` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class SantanderCustomerTransactionPrediction(AbstractCuratedDataset):
    # Dataset
    unique_name = "santander_customer_transaction_prediction"
    year = "2019"
    domain = "finance"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/c/santander-customer-transaction-prediction"
    license = "Kaggle Competition Rules"
    data_tags = ("Anonymized",)
    download_description = """
        We use the train.csv from the Kaggle competition.

        kaggle competitions download -c santander-customer-transaction-prediction -f train.csv && unzip train.csv.zip &&  rm train.csv.zip
        mkdir -p local-data-warehouse/santander_customer_transaction_prediction && mv train.csv local-data-warehouse/santander_customer_transaction_prediction/
    """
    bibtex = r"""
        @misc{Piedra2019SantanderCustomerTransactionPrediction,
          author = {Mercedes Piedra and Sohier Dane and Soraya Jimenez},
          title  = {Santander Customer Transaction Prediction},
          year   = {2019},
          howpublished = {\url{https://kaggle.com/competitions/santander-customer-transaction-prediction}},
          note   = {Kaggle competition}
        }
    """
    curation_comments = """
        We start with the train.csv from Kaggle.

        - The data has been anonymized, so feature meanings are unknown.
        - The data seems to be generated or created for the competition. Most features are perfectly normally distributed.
        - Kaggle experts found various uniqueness-based features and had to filter fake samples from the test data. We apply the uniqueness-based features.
    """

    # Task
    target = "target"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "train.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Follow #1 solution https://www.kaggle.com/code/fl2ooo/create-data
        # - We do not create the feature that is used for / requires test-time adaption for the fake test samples (that do not exist in the train data).
        orig = [f"var_{i}" for i in range(200)]
        has_one = [f"var_{i}_has_one" for i in range(200)]
        has_zero = [f"var_{i}_has_zero" for i in range(200)]
        target = self.task_metadata.target_column_name
        for f in orig:
            df[f + "_has_one"] = 0
            df[f + "_has_zero"] = 0
            f_1 = df.loc[df[target] == 1, f].value_counts()

            f_1_1 = set(f_1.index[f_1 > 1])
            f_0_1 = set(f_1.index[f_1 > 0])

            f_0 = df.loc[df[target] == 0, f].value_counts()
            f_0_0 = set(f_0.index[f_0 > 1])
            f_1_0 = set(f_0.index[f_0 > 0])

            df.loc[df[target] == 1, f + "_has_one"] = df.loc[df[target] == 1, f].isin(f_1_1).astype(int)
            df.loc[df[target] == 0, f + "_has_one"] = df.loc[df[target] == 0, f].isin(f_0_1).astype(int)
            df.loc[df[target] == 1, f + "_has_zero"] = df.loc[df[target] == 1, f].isin(f_1_0).astype(int)
            df.loc[df[target] == 0, f + "_has_zero"] = df.loc[df[target] == 0, f].isin(f_0_0).astype(int)
            df = df.copy()
        df.loc[:, has_one] = 2 * df.loc[:, has_one].values + df.loc[:, has_zero].values
        df = df.drop(columns=["ID_code"])
        cat_cols = [self.task_metadata.target_column_name] + has_one + has_zero
        for col in cat_cols:
            df[col] = df[col].astype("category")
        return df


# MIGRATE: the v1 notebook did not shuffle; v2 shuffles IID/grouped data (set `shuffle = False` if the order matters)
