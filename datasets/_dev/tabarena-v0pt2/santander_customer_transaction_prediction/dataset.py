"""Curated dataset definition for `santander_customer_transaction_prediction` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Metric, Source, TaskSummary, decode, drop_columns


class SantanderCustomerTransactionPrediction(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a bank customer make a specific transaction in the future?",
        use_case=(
            "For example, Santander decides which customers to target with an offer by predicting which ones will "
            "make a specific transaction, irrespective of the amount (the competition's question)."
        ),
        row="One Santander customer (200,000 customers; country and period not stated).",
        predicted=(
            "Whether the customer makes the transaction; 10.05% do. Neither the transaction nor the time frame is "
            "stated."
        ),
        known=("200 anonymized numbers, most of them close to normally distributed; their meaning is not stated."),
        split="Random customers.",
        changes=(
            "We drop the 400 value-presence features of an earlier version, which were computed from the labels of "
            "all rows, test rows included."
        ),
        fit="approximate",
        fit_reason=(
            "The features are anonymized and look generated or transformed for the competition, and the source names "
            "neither the transaction nor the time frame, so the task stands for customer targeting only in outline."
        ),
    )

    # Dataset
    unique_name = "santander_customer_transaction_prediction"
    domain = "finance"
    sources = (
        Source(
            role="publication",
            platform="Kaggle",
            url="https://www.kaggle.com/c/santander-customer-transaction-prediction",
            license="Kaggle Competition Rules",
            year="2019",
            bibtex=r"""
                @misc{Piedra2019SantanderCustomerTransactionPrediction,
                  author = {Mercedes Piedra and Sohier Dane and Soraya Jimenez},
                  title  = {Santander Customer Transaction Prediction},
                  year   = {2019},
                  howpublished = {\url{https://kaggle.com/competitions/santander-customer-transaction-prediction}},
                  note   = {Kaggle competition}
                }
            """,
        ),
    )
    data_tags = ("Anonymized",)
    download_description = """
        We use the train.csv from the Kaggle competition.

        kaggle competitions download -c santander-customer-transaction-prediction -f train.csv && unzip train.csv.zip &&  rm train.csv.zip
        mkdir -p local-data-warehouse/santander_customer_transaction_prediction && mv train.csv local-data-warehouse/santander_customer_transaction_prediction/
    """
    curation_comments = """
        We start with the train.csv from Kaggle.

        - The data has been anonymized, so feature meanings are unknown.
        - The data seems to be generated or created for the competition. Most features are perfectly normally distributed.
        - Kaggle experts found various uniqueness-based features and had to filter fake samples from the test data. We do not ship them: the #1 solution's has_one/has_zero features (does this row's value occur in another class-1 / class-0 row?) are computed from the labels of all rows, so precomputed they encode the labels of the test-fold rows (about +0.004 ROC AUC). We ship the raw var_0..var_199.
        - The feature engineering itself can be a good idea inside a pipeline: value counts / value-presence encodings of each var, computed within each fold from the training rows (and from unlabelled rows where a method is allowed to see them), add real signal (LightGBM ROC AUC 0.899 with has_one/has_zero from the training fold's labels and 0.900 with label-free value counts, against 0.896 for the raw vars and 0.903 for the shipped leaky version; leak audit 2026-09-24).
        - The target (2026-11-01, CLEAN-25): `target` ships its classes as words (1 is the event). Binary: "Yes" is the
          event, the class that sorts second, so it is the metrics' positive class.
    """

    # Task
    target = "target"
    problem_type = "binary_classification"
    metric = Metric.source(
        "roc_auc",
        original="Area Under Receiver Operating Characteristic Curve",
        reference=(
            "https://www.kaggle.com/competitions/santander-customer-transaction-prediction (Kaggle API "
            "evaluationMetric)"
        ),
        definition="Area under the ROC curve of target = 1.",
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "train.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Ship the raw var_0..var_199 only: the #1 solution's has_one/has_zero value-presence features are computed
        # from the labels of all rows, test folds included, so they cannot be precomputed for a static benchmark.
        df = drop_columns(df, ["ID_code"])
        # the target's classes in words (CLEAN-25): "Yes" is the event the task predicts
        df = decode(df, {self.target: {"0": "No", "1": "Yes"}})
        return df
