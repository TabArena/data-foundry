"""Curated dataset definition for `amex_non_iid_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Grouping, Metric, TaskSummary


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
        - Missing values: raddar's integer re-encoding writes a missing value as -1. In the 55 integer columns that hold
          -1 (int8 and int16, among them the categorical D_64, D_66, D_68, B_30, B_38, D_114, D_116, D_117, D_120 and
          D_126), -1 is the minimum, no cell is missing, and the -1 cells fall on the same rows across blocks (the same
          176,716 rows in D_113 to D_125, 101,548 in D_103, D_107, D_129, D_139, D_143 and D_145, 2,016 in B_16 to
          B_38). `_clean` sets them back to missing (CLEAN-10, 2026-10-30).
    """

    # Task
    target = "target"
    problem_type = "binary_classification"
    metric = Metric.source(
        "gini_top_capture",
        original="AmEx competition metric M = 0.5*(G + D)",
        reference="https://www.kaggle.com/competitions/amex-default-prediction/overview/evaluation",
        definition=(
            "Mean of the normalized Gini (G) and the default rate captured in the top 4% of predictions (D), "
            "both with negatives weighted 20x for the competition's 5% subsampling of non-defaults."
        ),
        params={"top_fraction": 0.04, "negative_weight": 20},
    )
    grouping = Grouping(
        on="customer_ID",
        labels="per_group",
        time_on="S_2",
        prediction_unit="group",
        aggregation="last",
        context="all_rows",
        definition="""
            One group is a customer; its rows are its monthly statements (1 to 13). The task is "to predict, for each customer_ID, the probability of a future payment default", with the label "calculated by observing 18 months performance window after the latest credit card statement" (AmEx Default Prediction, Kaggle). So one prediction per customer, made at its latest statement (`S_2`) from all its statements, which are all in the past at that point; the Kaggle test customers are disjoint from the training customers. The competition scores its metric (`gini_top_capture`) per customer.
        """,
    )

    # Splits
    subsample_to_budget = True
    accepted_check_warnings = {
        "splits_rows_never_tested": "The v2 protocol caps each test fold at 500k rows; the grouped folds of the 1.5M-row "
        "frame overshoot by whole groups, so 325 rows (0.02%) are trimmed from a test fold (2026-10-01).",
        "dataset_constant_column": "D_87 is 1 or missing, as in AMEX's original data (1 in 3,865 of 5.5M statements); "
        "raddar's -1 is its missing value (CLEAN-10, 2026-10-30), so whether it is present is the column's information.",
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_parquet(raw_dir / "train.parquet")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # raddar's integer columns code a missing value as -1 (curation notes)
        for col in [c for c in df.columns if pd.api.types.is_integer_dtype(df[c]) and (df[c] == -1).any()]:
            df[col] = df[col].where(df[col].ne(-1)).astype("float32")
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
        return FeatureTypes(
            categorical=[
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
            ],
        )
