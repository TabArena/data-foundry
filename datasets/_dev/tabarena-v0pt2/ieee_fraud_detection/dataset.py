"""Curated dataset definition for `ieee_fraud_detection` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary, Temporal, TemporalSplits


class IeeeFraudDetection(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Is an online card payment fraudulent?",
        use_case=(
            "When an online payment arrives, a payment processor (Vesta, the source of the data) decides whether to "
            "accept it or decline it as fraud; once a card is charged back, the client's later payments count as "
            "fraud."
        ),
        row=(
            "One e-commerce card payment processed by Vesta, December 2017 to May 2018, with dates from an assumed "
            "start day (590,540 payments)."
        ),
        predicted=(
            "Whether the payment is fraud (3.5%): a payment on a card reported as charged back, or a later payment "
            "linked to it by account, email or billing address."
        ),
        known=(
            "The amount and product, card and address details, email domains, device and browser data, counts and "
            "time gaps from the processor's records (mostly anonymized), and a client key rebuilt by the "
            "competition's winners."
        ),
        split=(
            "Each of March, April and May 2018 is a test month, trained on all payments up to one month before it, as"
            " in the competition's gap."
        ),
        changes=(
            "We split by month with a one-month gap and add the client key of the first-place solution, which links "
            "the payments of one client."
        ),
        fit="direct",
        fit_reason=(
            "The features describe the payment and its history, and later months stand for the payments to come. The "
            "calendar rests on an assumed start day, and the anonymized features cannot be checked one by one."
        ),
    )

    # Dataset
    unique_name = "ieee_fraud_detection"
    year = "2019"
    domain = "finance"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/competitions/ieee-fraud-detection/overview"
    data_tags = ("Anonymized",)
    license = "non-commercial purposes only, including academic research"
    download_description = r"""
        kaggle competitions download -c ieee-fraud-detection -p local-data-warehouse/ieee_fraud_detection \
        && unzip local-data-warehouse/ieee_fraud_detection/ieee-fraud-detection.zip -d local-data-warehouse/ieee_fraud_detection/ \
        && rm local-data-warehouse/ieee_fraud_detection/ieee-fraud-detection.zip
    """
    bibtex = r"""
        @misc{ieee-fraud-detection,
            author = {Addison Howard and Bernadette Bouchon-Meunier and IEEE CIS and inversion and John Lei and Lynn@Vesta and Marcus2010 and Prof. Hussein Abbass},
            title = {IEEE-CIS Fraud Detection},
            year = {2019},
            howpublished = {\url{https://kaggle.com/competitions/ieee-fraud-detection}},
            note = {Kaggle}
        }
    """
    curation_comments = """
        - We use insights of the first place solution on Kaggle for conceptualizing the task: https://www.kaggle.com/competitions/ieee-fraud-detection/discussion/111284
        - The data is given as transactions, but the task is to predict fraudulent clients. Once a transaction is detected as fraud, the entire account is considered fraudulent.
        - The competition host commented on the labeling logic: "The logic of our labeling is define reported chargeback on the card as fraud transaction (isFraud=1) and transactions posterior to it with either user account, email address or billing address directly linked to these attributes as fraud too" (https://www.kaggle.com/c/ieee-fraud-detection/discussion/101203#589276)
        - We load train_transaction.csv and train_identity.csv and merge them on TransactionID.
        - We derive Transaction_date from TransactionDT using the competition reference start date 2017-11-30.
        - The Kaggle competition also provides test_transaction.csv and test_identity.csv, but they are unlabeled and are therefore excluded from df for curation checks.
        - We normalize the D-columns, since they correspond to days since a certain event, we can normalize them by the transaction date to get the actual day of the event. This is also what the first place solution on Kaggle did.
        - We add a uid feature used by the first place solution on Kaggle to identify unique users. Note that this feature is not perfect and just an approximation by the Kaggle users. Moreover, due to missing values, for ~15% of the samples no uid could be reconstructed.
        - Following the first place Kaggle solution, which used month-based cross-validation, we create splits using forecasting horizons of 1 month.
        - The competition test data left a planning window of one month, so do we.
        - Anomaly: Missing values.
        - Anomaly: Several features might allow to approximate to the uid and can lead to overfitting.
        - Anomaly: Grouped data with members of a group often sharing the same label, depending on whether fraud occurred previously or not.
    """

    # Task
    target = "isFraud"
    problem_type = "binary_classification"
    metric = Metric.source(
        "roc_auc",
        original="Area under the ROC curve",
        reference="https://www.kaggle.com/competitions/ieee-fraud-detection/overview/evaluation",
        definition="Area under the ROC curve between predicted probability and isFraud, per transaction.",
    )

    # Splits
    splits_comment = """
        To define three train/test splits, we use the last three months as test sets, leave 1 month as the planning gap, and use the remaining training data.
    """
    temporal = Temporal(
        on="Transaction_date",
        splits=TemporalSplits(window=1, unit="months", n_windows=3, gap=1),
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # LOAD TRAIN
        df = pd.read_csv(raw_dir / "train_transaction.csv", index_col="TransactionID", engine="pyarrow")
        train_id = pd.read_csv(raw_dir / "train_identity.csv", index_col="TransactionID", engine="pyarrow")
        return {"df": df, "train_id": train_id}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        df, train_id = raw["df"], raw["train_id"]
        df = df.merge(train_id, how="left", left_index=True, right_index=True)
        START_DATE = datetime.datetime.strptime("2017-11-30", "%Y-%m-%d")
        df["Transaction_date"] = df["TransactionDT"].apply(lambda x: START_DATE + datetime.timedelta(seconds=x))
        df["day"] = df["TransactionDT"] / (24 * 60 * 60)
        # NORMALIZE D COLUMNS, since they correspond to days since a certain event, we can normalize them by the transaction date to get the actual day of the event. This is also what the first place solution on Kaggle did.
        for i in range(1, 16):
            if i in [1, 2, 3, 5, 9]:
                continue
            df["D" + str(i)] = df["D" + str(i)] - df["TransactionDT"] / np.float32(24 * 60 * 60)
        df = df.drop(columns=["TransactionDT"])
        # This is the uid that as used for feature engineering in the first place solution on Kaggle. They also have a better way to find uids
        # df['uid'] = df['card1'].astype(str) + '_' + df['addr1'].astype(str)  + '_' + np.floor(df.day - df.D1).astype(str)
        # df.loc[np.logical_or(df['D1'].isna(), df['addr1'].isna()),["uid"]] = np.nan
        # Use the uid version that has the best missing values (15%) vs. accuracy for same uid (99.96%)
        uids = pd.read_csv(
            self.folder / "uids_v1_no_multiuid_cleaning.csv", usecols=["TransactionID", "uid"], engine="pyarrow"
        )
        df = df.merge(uids, on="TransactionID", how="left")
        df = df.sort_values(by=["Transaction_date"], kind="stable").reset_index(drop=True)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # the categorical columns of the Kaggle data description (cards, address, e-mail domains, M flags, identity)
        categorical = ["ProductCD", "addr1", "addr2", "P_emaildomain", "R_emaildomain", "DeviceType", "DeviceInfo"]
        categorical += [f"card{i}" for i in range(1, 7)]
        categorical += [f"M{i}" for i in range(1, 10)]
        categorical += [f"id_{i}" for i in range(12, 39)]
        categorical += ["uid"]
        return FeatureTypes(categorical=categorical)
