"""Curated dataset definition for `santander_customer_transaction_prediction` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, drop_columns


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
        - Kaggle experts found various uniqueness-based features and had to filter fake samples from the test data. We do not ship them: the #1 solution's has_one/has_zero features (does this row's value occur in another class-1 / class-0 row?) are computed from the labels of all rows, so precomputed they encode the labels of the test-fold rows (about +0.004 ROC AUC). We ship the raw var_0..var_199.
        - The feature engineering itself can be a good idea inside a pipeline: value counts / value-presence encodings of each var, computed within each fold from the training rows (and from unlabelled rows where a method is allowed to see them), add real signal (LightGBM ROC AUC 0.899 with has_one/has_zero from the training fold's labels and 0.900 with label-free value counts, against 0.896 for the raw vars and 0.903 for the shipped leaky version; leak audit 2026-09-24).
    """

    # Task
    target = "target"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "train.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Ship the raw var_0..var_199 only: the #1 solution's has_one/has_zero value-presence features are computed
        # from the labels of all rows, test folds included, so they cannot be precomputed for a static benchmark.
        df = drop_columns(df, ["ID_code"])
        return df


# MIGRATE: the v1 notebook did not shuffle; v2 shuffles IID/grouped data (set `shuffle = False` if the order matters)
