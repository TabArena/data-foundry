"""Curated dataset definition for `ieee_fraud_detection` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Metric,
    Source,
    TaskSummary,
    Temporal,
    TemporalSplits,
    decode,
)

# The codebook's words for coded columns, decoded in `_clean` after the codes that mean unknown are missing
# (CLEAN-12; the curator's rule of 2026-11-01).
CODE_LABELS = {
    "id_14": {
        "-660": "UTC-11:00",
        "-600": "UTC-10:00",
        "-540": "UTC-09:00",
        "-480": "UTC-08:00",
        "-420": "UTC-07:00",
        "-360": "UTC-06:00",
        "-300": "UTC-05:00",
        "-240": "UTC-04:00",
        "-210": "UTC-03:30",
        "-180": "UTC-03:00",
        "-120": "UTC-02:00",
        "0": "UTC+00:00",
        "60": "UTC+01:00",
        "120": "UTC+02:00",
        "180": "UTC+03:00",
        "240": "UTC+04:00",
        "270": "UTC+04:30",
        "300": "UTC+05:00",
        "330": "UTC+05:30",
        "360": "UTC+06:00",
        "420": "UTC+07:00",
        "480": "UTC+08:00",
        "540": "UTC+09:00",
        "600": "UTC+10:00",
        "720": "UTC+12:00",
    },
}


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
            "Each of the three newest months, May, April and March 2018, is a test window, trained on all payments up "
            "to one month before it, the competition's gap; a month is the group the winning team validated on. The "
            "March window trains on December and January only, 39% of the payments."
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
    domain = "finance"
    sources = (
        Source(
            role="publication",
            platform="Kaggle",
            url="https://www.kaggle.com/competitions/ieee-fraud-detection/overview",
            license="non-commercial purposes only, including academic research",
            year="2019",
            bibtex=r"""
                @misc{ieee-fraud-detection,
                    author = {Addison Howard and Bernadette Bouchon-Meunier and IEEE CIS and inversion and John Lei and Lynn@Vesta and Marcus2010 and Prof. Hussein Abbass},
                    title = {IEEE-CIS Fraud Detection},
                    year = {2019},
                    howpublished = {\url{https://kaggle.com/competitions/ieee-fraud-detection}},
                    note = {Kaggle}
                }
            """,
        ),
    )
    data_tags = ("Anonymized",)
    download_description = r"""
        kaggle competitions download -c ieee-fraud-detection -p local-data-warehouse/ieee_fraud_detection \
        && unzip local-data-warehouse/ieee_fraud_detection/ieee-fraud-detection.zip -d local-data-warehouse/ieee_fraud_detection/ \
        && rm local-data-warehouse/ieee_fraud_detection/ieee-fraud-detection.zip
    """
    curation_comments = """
        - We use insights of the first place solution on Kaggle for conceptualizing the task: https://www.kaggle.com/competitions/ieee-fraud-detection/discussion/111284
        - The data is given as transactions, but the task is to predict fraudulent clients. Once a transaction is detected as fraud, the entire account is considered fraudulent.
        - The competition host commented on the labeling logic: "The logic of our labeling is define reported chargeback on the card as fraud transaction (isFraud=1) and transactions posterior to it with either user account, email address or billing address directly linked to these attributes as fraud too" (https://www.kaggle.com/c/ieee-fraud-detection/discussion/101203#589276)
        - We load train_transaction.csv and train_identity.csv and merge them on TransactionID.
        - We drop `TransactionID` after the merges: it is a row number, unique, consecutive and in the order of
          TransactionDT (rank correlation 1.0 over 590,540 rows), so it holds only the time, which `day` gives; a code
          shipped as a number with no meaning of its own (CLEAN-3; the curator's marks of 2026-10-31, point 4).
        - We derive Transaction_date from TransactionDT using the competition reference start date 2017-11-30.
        - The Kaggle competition also provides test_transaction.csv and test_identity.csv, but they are unlabeled and are therefore excluded from df for curation checks.
        - We normalize the D-columns, since they correspond to days since a certain event, we can normalize them by the transaction date to get the actual day of the event. This is also what the first place solution on Kaggle did.
        - We add a uid feature used by the first place solution on Kaggle to identify unique users. Note that this feature is not perfect and just an approximation by the Kaggle users. Moreover, due to missing values, for ~15% of the samples no uid could be reconstructed.
        - Test windows of one calendar month, the group of the first-place solution's validation ("GroupKFold training validation data splitting, with ordered months as non-overlapping groups"); a validation scheme, not a refit cadence, which neither Vesta nor the competition states (CC 2026-11-11; splits comment).
        - A gap of one month, the competition's: its labelled payments end on 31 May 2018 and its unlabelled test payments start on 1 July 2018.
        - Anomaly: Missing values.
        - Anomaly: Several features might allow to approximate to the uid and can lead to overfitting.
        - Anomaly: Grouped data with members of a group often sharing the same label, depending on whether fraud occurred previously or not.
        - Codes decoded (2026-11-01, CLEAN-12, CLEAN-14; the curator's rule: a code whose codebook says in words what
          each level is carries the words, a score without them is a number): 1 unordered codes carry their words:
          `id_14`.
        - The target (2026-11-01, CLEAN-25): `isFraud` ships its classes as words (1 is the event). Binary: "Yes" is the
          event, the class that sorts second, so it is the metrics' positive class.
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
        Each test window is one calendar month, the group the first-place team validated on ("GroupKFold training validation data splitting, with ordered months as non-overlapping groups", https://developer.nvidia.com/blog/leveraging-machine-learning-to-detect-fraud-tips-to-developing-a-winning-kaggle-solution). It is a validation scheme, not a refit cadence: Vesta decides on each payment as it arrives and states no cadence, and the competition scores one model on six months (July to December 2018), so the length says how long one fitted model serves. The gap is one month, the competition's: its labelled payments end on 31 May 2018 and its test payments start on 1 July 2018. A fraud label waits for the cardholder's chargeback, which Visa accepts up to 120 days after a card-absent payment, so the gap is shorter than the longest delay. The payments run from 1 December 2017 to 31 May 2018 (dated from the assumed start day of 30 November 2017), and the test windows are the three newest months (CC 2026-11-11), newest first: May, April and March 2018, with 89,326, 83,655 and 101,632 payments (fraud 3.5%, 3.4% and 4.0%). Train is every payment before the gap, up to 31 March, 28 February and 31 January: 417,559, 315,927 and 229,906 payments (70.7%, 53.5% and 38.9%). The March window trains on less than half the payments (38.9%, December and January); the two newest train on more. The windows walk back from the newest because six months of payments leave no other choice: with the one-month gap a February window would train on December only (about 23%).
    """
    temporal = Temporal(
        on="Transaction_date",
        splits=TemporalSplits(window=1, unit="months", n_windows=3, gap=1),
    )
    accepted_check_warnings = {
        "splits_train_under_half": (
            "Signed off (Lennart, 2026-11-11, review issue 1, A): March 2018 trains on 38.9% of the payments, "
            "beside May and April on 70.7% and 53.5%; SPLIT-14's two tiers admit it."
        ),
    }

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
        # a running row number in time order: an identifier, the time is `day` (curation notes; CLEAN-3)
        df = df.drop(columns=["TransactionID"])
        df = df.sort_values(by=["Transaction_date"], kind="stable").reset_index(drop=True)
        # the codebook's words for its codes (CLEAN-12)
        df = decode(df, CODE_LABELS)
        # the target's classes in words (CLEAN-25): "Yes" is the event the task predicts
        df = decode(df, {self.target: {"0": "No", "1": "Yes"}})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # the categorical columns of the Kaggle data description (cards, address, e-mail domains, M flags, identity)
        categorical = ["ProductCD", "addr1", "addr2", "P_emaildomain", "R_emaildomain", "DeviceType", "DeviceInfo"]
        categorical += [f"card{i}" for i in range(1, 7)]
        categorical += [f"M{i}" for i in range(1, 10)]
        categorical += [f"id_{i}" for i in range(12, 39)]
        categorical += ["uid"]
        return FeatureTypes(categorical=categorical)
