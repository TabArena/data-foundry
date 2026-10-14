"""Curated dataset definition for `expresso_churn_prediction_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, TaskSummary, drop_columns

TARGET = "CHURN"

ACTIVITY = [
    "MONTANT",
    "FREQUENCE_RECH",
    "REVENUE",
    "ARPU_SEGMENT",
    "FREQUENCE",
    "DATA_VOLUME",
    "ON_NET",
    "ORANGE",
    "TIGO",
    "ZONE1",
    "ZONE2",
    "TOP_PACK",
    "FREQ_TOP_PACK",
]
"""The usage aggregates of the observation window; missing when the customer had no such activity in it."""


class ExpressoChurnPrediction1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a mobile phone customer in Senegal stop using the service for the next 90 days?",
        use_case=(
            "At the end of an observation window of about three months, the telecom operator Expresso scores each "
            "customer active in it for the risk of churning, for example to target retention offers."
        ),
        row=(
            "One Expresso customer in Senegal who was active in the observation window: a random 1.5 million of the "
            "2,154,048 customers of the competition file, whose dates are not published."
        ),
        predicted=(
            "Whether the customer churns, that is makes no transaction for 90 days after the window (18.75% do)."
        ),
        known=(
            "The tenure band and the window's activity: top-up amounts and counts, revenue, data volume, calls within"
            " the network, to other operators and to other zones, the most used package, and the number of active "
            "days."
        ),
        split=(
            "Random customers of the same snapshot, as in the competition, whose test set is a random 15% of the "
            "extract; each fold trains on 1 million and tests on 500,000 customers."
        ),
        changes=(
            "We drop the region, whose missing values follow the outcome and were most likely filled in after the "
            "window, and sub-sample 1.5 million customers."
        ),
        fit="approximate",
        fit_reason=(
            "Everything the model sees is from the window and churn follows it. But the release is one snapshot "
            "without dates: training and test customers share one window, while a deployed model is trained on an "
            "earlier one, and the label's timing is inferred, not published."
        ),
    )

    # Dataset
    unique_name = "expresso_churn_prediction_1m"
    version_of = "expresso_churn_prediction"
    version_comment = """
        We sub-sample the frame (2,154,048 customers) to 1.5M customers, stratified on the target, and use 3-fold cross-validation, so every fold trains on 1M and tests on 500k customers (v2 split protocol).
    """
    year = "2020"
    domain = "business & marketing"
    source = "Zindi"
    source_url = "https://zindi.africa/competitions/expresso-churn-prediction"
    license = "Zindi Competition Rules"
    download_description = """
        Train.csv of the Zindi competition "Expresso Churn Prediction Challenge" (2021). Zindi needs a login, so we take
        the Kaggle copy by hamzaghanmi (version 1, 2021-08-30), which holds the competition's Train.csv, Test.csv and
        SampleSubmission.csv with the byte sizes the Zindi API lists for them (Train.csv: 259,026,777 bytes, sha256
        15d3438d098bea4dc107ba77c81e364705527845f24d7adcbc332e1e33c8777d; 2,154,048 rows and a header). A second upload,
        hossamshokry/expresso-churn-datasets (2025-09-01), holds a Train.csv with the same sha256. Only Train.csv is used:
        Test.csv has no labels.

        uvx --from kaggle==2.2.2 kaggle datasets download hamzaghanmi/expresso-churn-prediction-challenge/1
        mkdir -p local-data-warehouse/expresso_churn_prediction
        unzip expresso-churn-prediction-challenge.zip Train.csv -d local-data-warehouse/expresso_churn_prediction
        rm expresso-churn-prediction-challenge.zip
    """
    bibtex = r"""
        @misc{zindi2021expressochurn,
          author = {{Zindi} and {Expresso}},
          title = {Expresso Churn Prediction Challenge},
          year = {2021},
          howpublished = {\url{https://zindi.africa/competitions/expresso-churn-prediction}},
          note = {Zindi competition, 27 August to 28 November 2021. The data was first released for the UmojaHack Africa hackathons in Senegal and Ghana on 27 June 2020}
        }
    """
    curation_comments = """
        We start with Train.csv of the Zindi competition Expresso Churn Prediction Challenge (2021): 2,154,048 customers of the telecom operator Expresso in Senegal, one row each. The competition's Test.csv has no labels and is not used.

        - Prediction point: the end of an observation window of about three months, when Expresso scores each customer active in it for churn, "becoming inactive and not making any transactions for 90 days" (competition Description page). Zindi publishes no dates; the label window follows the observation window, as every customer was active in it (REGULARITY is at least 1) and 612 churners were active on all of its last 62 days.
        - Target: CHURN mapped from 1/0 to Yes/No; 403,986 customers (18.75%) churned.
        - We drop `user_id`, the SHA-1 hash of the customer's row number in Expresso's extract; the 3rd-place solution used the decoded row order as a feature (Zindi discussion 9379).
        - We drop `MRG` (value-added services flag): "NO" in every row.
        - We drop REGION: whether it is missing follows the outcome, not the window, so it was most likely filled after the window. Among churners the region is missing for 92% to 95% at every number of active days, while among those who stayed the share falls from 67% at 1 active day to 7% at 62, as the window's own columns do in both groups (decision table); dropping it lowers ROC AUC from 0.930 to 0.901 (LightGBM, 400,000 customers, 3-fold cross-validation).
        - IID split, as in the competition: the file is one snapshot of the customer base with no time index, and Zindi's test set is a uniform random 15% of the extract.
        - Duplicates kept: without user_id and REGION, 678,270 rows (31.5%) repeat another row exactly. Each row is a different customer, 75.3% of the copies have no activity value, and the copies hold 317,548 of the 403,986 churners, so dropping them would turn an 18.75% churn task into a 5.9% one about active customers (decision table).
        - dtypes: TENURE (8 bands) and TOP_PACK (140 packs, written inconsistently by Expresso) are categorical; the other columns are counts or amounts.
        - Note: the activity columns are missing when the customer had none of that activity in the window; we keep them missing.
        - Note: REGULARITY counts the active days in the last 62 days of the window (1 to 62), while FREQUENCE, the days with revenue, reaches 91. ARPU_SEGMENT is REVENUE / 3 rounded in every row; both are kept as released.
        - Note: the task probes flag one_feature (REGULARITY alone ROC AUC 0.890). We keep the task by rule 4 of task_probes.md: active days are the natural core of a churn task, and on the shipped folds an untuned LightGBM beats REGULARITY alone on 3 of 3 folds (0.9023 to 0.9031 against 0.8896 to 0.8902).
        - Note: Zindi's rules forbid redistributing the data, uploads to Kaggle or GitHub included; the Kaggle copies we name are such uploads.
    """

    # Task
    target = TARGET
    problem_type = "binary_classification"

    # Splits: IID (one snapshot, no time index); the `_1m` version sub-samples the frame to the 1.5M-row budget.
    subsample_to_budget = True
    accepted_check_warnings = {
        "dataset_duplicate_rows": "Every row is a different customer (unique user_id). The copies are customers "
        "described only by a tenure band and their active days (75.3% of the 678,270 copies in the full file have no "
        "activity value), all active in the window, so the profiles repeat naturally. The copies hold 317,548 of the "
        "403,986 churners: deduplicating would leave a 5.9% churn task about active customers (2026-10-07).",
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "Train.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df[TARGET] = df[TARGET].map({1: "Yes", 0: "No"})
        # user_id: SHA-1 of the row number in Expresso's extract; MRG: "NO" in every row; REGION: whether it is missing
        # follows the outcome, not the window (curation comments)
        return drop_columns(df, ["user_id", "MRG", "REGION"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["TENURE", "TOP_PACK"])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        # REGION is dropped from `df`, so its evidence comes from the raw file
        outcome = raw[TARGET].map({1: "churned", 0: "stayed"})
        active_days = pd.cut(raw["REGULARITY"], [0, 1, 3, 10, 30, 50, 61, 62])
        signature = (
            pd.DataFrame(
                {
                    "active days (REGULARITY)": active_days,
                    "outcome": outcome,
                    "region": raw["REGION"].isna(),
                    "montant": raw["MONTANT"].isna(),
                }
            )
            .groupby(["active days (REGULARITY)", "outcome"], observed=True)
            .agg(customers=("region", "size"), REGION_missing=("region", "mean"), MONTANT_missing=("montant", "mean"))
            .unstack("outcome")
        )
        labels = {"customers": "customers", "REGION_missing": "REGION missing", "MONTANT_missing": "MONTANT missing"}
        signature.columns = [f"{labels[name]}, {group}" for name, group in signature.columns]
        features = [c for c in df.columns if c != TARGET]
        repeats = df.duplicated(keep="first")
        per_vector = df.groupby(features, dropna=False, observed=True)[TARGET].nunique()
        conflicting = per_vector[per_vector > 1]
        in_conflict = df.set_index(features).index.isin(conflicting.index)
        no_activity = df[ACTIVITY].isna().all(axis=1)
        duplicates = pd.Series(
            {
                "customers": len(df),
                "exact copies of another row (features and label)": int(repeats.sum()),
                "feature vectors with both labels": len(conflicting),
                "rows in those vectors": int(in_conflict.sum()),
                "rows in those vectors with no activity value": int((in_conflict & no_activity).sum()),
                "customers with no activity value": int(no_activity.sum()),
            },
            name="rows",
        )
        return [
            Decision(
                title="REGION is dropped: whether it is missing follows the outcome, not the window",
                why=(
                    "Among churners the region is missing for 92-95% at every number of active days, while among "
                    "those who stayed the share falls with activity, as it does for the window's own columns "
                    "(MONTANT) in both groups. A field taken from the window would follow the churners' activity "
                    "too, so the region was most likely filled after the window (full file, 2,154,048 customers)."
                ),
                evidence=signature.round(3),
            ),
            Decision(
                title="Duplicate rows are kept: different customers with sparse profiles",
                why=(
                    "Every row is a different customer (unique ids). The copies are customers with no or little "
                    "activity in the window, described only by a tenure band and their active days, so repeats and "
                    "conflicting labels are expected."
                ),
                evidence=duplicates,
            ),
        ]
