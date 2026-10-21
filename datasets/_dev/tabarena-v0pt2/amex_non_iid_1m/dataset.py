"""Curated dataset definition for `amex_non_iid_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Grouping, TaskSummary


class AmexNonIid1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=("Will a credit card customer fail to pay within 18 months of the latest monthly statement?"),
        use_case=(
            "At a customer's latest monthly statement, the card issuer estimates whether the customer will default in"
            " the next 18 months, to manage its lending risk, for example the credit it extends."
        ),
        row=(
            "One monthly statement of an American Express credit card customer; a customer has 1 to 13 statements, "
            "and the prediction is made once per customer, at the latest one (124,466 customers)."
        ),
        predicted=(
            "Whether the customer defaults on a payment in the 18 months after the latest statement. The source kept "
            "only 5% of the customers who paid, so defaulters' statements are 24.9% of the rows."
        ),
        known=(
            "All of the customer's statements up to the latest, with their dates, each with anonymized, normalized "
            "variables that the source groups into delinquency, spending, payments, balances and risk."
        ),
        split=(
            "Whole customers are held out, so the test data stands for other customers of the same months, each "
            "scored at the latest statement."
        ),
        fit="direct",
        fit_reason=(
            "Every statement is in the past at the prediction point, and the label covers a fixed 18 months after it,"
            " as in use. The test customers come from the same months as the training ones, and the features are "
            "anonymized."
        ),
    )

    # Dataset
    unique_name = "amex_non_iid_1m"
    version_of = "amex_non_iid"
    version_comment = """
        We sub-sample the frame to 1.5M rows by whole customers (stratified on the target) and use grouped 3-fold cross-validation, so every fold trains on about 1M and tests on about 500k rows (v2 split protocol).
    """
    year = "2022"
    domain = "finance"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/competitions/amex-default-prediction/"
    license = "Kaggle Competition License"
    data_tags = ("Non-IID", "Grouped", "Anonymized")
    download_description = """
        We start with the preprocessed version of the dataset in Parquet format provided by
        the user 'raddar' on Kaggle. At the root of this project, I ran on linux with
        the kaggle CLI installed and authenticated:

        kaggle datasets download -d raddar/amex-data-integer-dtypes-parquet-format --unzip -p amex_dataset && rm amex_dataset/test.parquet
        kaggle competitions download -c amex-default-prediction -f train_labels.csv -p amex_dataset && cd amex_dataset && unzip train_labels.csv.zip train_labels.csv && rm train_labels.csv.zip && cd ..
        mkdir -p local-data-warehouse/amex_non_iid && mv amex_dataset/* local-data-warehouse/amex_non_iid/ && rm -rf amex_dataset
    """
    bibtex = """
        @misc{howard2022amex,
          author       = {Howard, Addison and AritraAmex and Xu, Di and Vashani, Hossein and inversion and Negin and Dane, Sohier},
          title        = {American Express -- Default Prediction},
          year         = {2022},
          howpublished = {Kaggle Competition},
          url          = {https://kaggle.com/competitions/amex-default-prediction},
          note         = {Accessed via Kaggle}
        }
    """
    curation_comments = """
        We start with the raw data from Kaggle and do not apply any further preprocessing to simulate a pipeline that can handle raw non-IID grouped data.
    """

    # Task
    target = "target"
    problem_type = "binary_classification"
    metric = "amex_metric"
    grouping = Grouping(
        on="customer_ID",
        labels="per_group",
        time_on="S_2",
        prediction_unit="group",
        aggregation="last",
        context="all_rows",
        definition="""
            One group is a customer; its rows are its monthly statements (1 to 13). The task is "to predict, for each customer_ID, the probability of a future payment default", with the label "calculated by observing 18 months performance window after the latest credit card statement" (AmEx Default Prediction, Kaggle). So one prediction per customer, made at its latest statement (`S_2`) from all its statements, which are all in the past at that point; the Kaggle test customers are disjoint from the training customers. The competition scores `amex_metric` per customer.
        """,
    )

    # Splits
    subsample_to_budget = True
    accepted_check_warnings = {
        "splits_rows_never_tested": "The v2 protocol caps each test fold at 500k rows; the grouped folds of the 1.5M-row "
        "frame overshoot by whole groups, so 325 rows (0.02%) are trimmed from a test fold (2026-10-01).",
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_parquet(raw_dir / "train.parquet")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df.S_2 = pd.to_datetime(df.S_2)
        df = df.sort_values(["customer_ID", "S_2"], kind="stable")
        df = df.set_index("customer_ID")
        # Add labels
        targets = pd.read_csv(self.raw_dir / "train_labels.csv")
        targets = targets.set_index("customer_ID")
        df = df.merge(targets, left_index=True, right_index=True, how="left")
        df.target = df.target.astype("int8")
        del targets
        df = df.reset_index().reset_index(drop=True)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # 0/1 flags (features holding only 0 and 1, plus missing values) are categorical (CLEAN-14)
        flags = [
            c
            for c in df.columns.drop(self.target)
            if pd.api.types.is_numeric_dtype(df[c]) and df[c].nunique() == 2 and df[c].dropna().isin([0, 1]).all()
        ]
        listed = [
            "B_30",
            "B_38",
            "D_114",
            "D_116",
            "D_117",
            "D_120",
            "D_126",
            "D_63",
            "D_64",
            "D_66",
            "D_68",
            "customer_ID",
        ]
        return FeatureTypes(categorical=[*listed, *(c for c in flags if c not in listed)])
