"""Curated dataset definition for `expresso_churn_prediction_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Metric, TaskSummary, drop_columns

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
"""The usage aggregates of the observation window; missing when the extract has no record, 0 is a record of none."""


# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "TENURE": [
        "D 3-6 month",
        "E 6-9 month",
        "F 9-12 month",
        "G 12-15 month",
        "H 15-18 month",
        "I 18-21 month",
        "J 21-24 month",
        "K > 24 month",
    ],  # open-ended
}


class ExpressoChurnPrediction1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a mobile phone customer in Senegal stop using the service for the next 90 days?",
        use_case=(
            "At the end of an observation window of about three months, the telecom operator Expresso scores each "
            "customer active in it for the risk of churning, for example to target retention offers."
        ),
        row=(
            "One Expresso customer in Senegal who was active in the observation window: a random 1.5 million of the "
            "2,154,048 customers of the competition file, whose dates are not published. Almost all are long-tenure "
            "customers (94.9% over 24 months, none under 3 months)."
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
            "The release is one undated snapshot: a deployed model trains on an earlier window. When the 90 days "
            "start is inferred (the window's end), not published; they may count from each customer's last activity."
            " And 80.9% of churners had no revenue in the window (2.0% of its revenue), so the task mostly ranks "
            "SIMs that are already dormant."
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
    source_url = "https://zindi.africa/competitions/umojahack-ghana-expresso-churn-prediction-challenge"
    license = "Zindi Competition Rules"
    data_tags = ("ForcedIIDFromTemporal",)
    download_description = """
        Train.csv of the Zindi hackathon "UmojaHack Ghana: Expresso Churn Prediction Challenge" (27 June 2020), re-run
        as the Zindi competition "Expresso Churn Prediction Challenge" (2021) with the same five files: the Zindi API
        lists identical byte sizes for both (Train.csv: 259,026,777 bytes, sha256
        15d3438d098bea4dc107ba77c81e364705527845f24d7adcbc332e1e33c8777d; 2,154,048 rows and a header). Zindi needs a
        login, so we take the Kaggle copy by hamzaghanmi (version 1, 2021-08-30), which holds the competition's
        Train.csv, Test.csv and SampleSubmission.csv with those byte sizes. A second upload,
        hossamshokry/expresso-churn-datasets (2025-09-01), holds a Train.csv with the same sha256. Only Train.csv is
        used: Test.csv has no labels. The codebook is Zindi's VariableDefinitions.csv (1,441 bytes, French and
        English), listed with the files on both pages.

        uvx --from kaggle==2.2.2 kaggle datasets download hamzaghanmi/expresso-churn-prediction-challenge/1
        mkdir -p local-data-warehouse/expresso_churn_prediction
        unzip expresso-churn-prediction-challenge.zip Train.csv -d local-data-warehouse/expresso_churn_prediction
        rm expresso-churn-prediction-challenge.zip
    """
    bibtex = r"""
        @misc{zindi2020expressochurn,
          author = {{Zindi} and {Expresso}},
          title = {UmojaHack Ghana: Expresso Churn Prediction Challenge},
          year = {2020},
          howpublished = {\url{https://zindi.africa/competitions/umojahack-ghana-expresso-churn-prediction-challenge}},
          note = {Zindi hackathon, 27 June 2020. Re-run with the same files as the Zindi competition Expresso Churn Prediction Challenge, 27 August to 28 November 2021, \url{https://zindi.africa/competitions/expresso-churn-prediction}}
        }
    """
    curation_comments = """
        We start with Train.csv of the Zindi hackathon UmojaHack Ghana: Expresso Churn Prediction Challenge (2020), re-run with the same files as the Expresso Churn Prediction Challenge (2021): 2,154,048 customers of the telecom operator Expresso in Senegal, one row each. Zindi's Test.csv has no labels and is not used.

        - Prediction point: the end of an observation window of about three months, when Expresso scores each customer active in it for churn, "becoming inactive and not making any transactions for 90 days" (competition page). Zindi publishes no dates and does not say when the 90 days start. We infer that they start at the window's end: every customer was active in the window (REGULARITY at least 1), and 612 churners were active on all of its last 62 days. The other reading, 90 days from each customer's last activity, would put part of the label period inside the window for customers with little activity; the 612 rule it out only for active customers, and nothing in the release settles it.
        - Target: CHURN mapped from 1/0 to Yes/No; 403,986 customers (18.75%) churned.
        - We drop `user_id`, the SHA-1 hash of the customer's row number in Expresso's extract; the 3rd-place solution used the decoded row order as a feature (Zindi discussion 9379).
        - We drop `MRG` (codebook: a customer who uses value-added services): "NO" in every row.
        - We drop REGION (LEAK-10): its missing flag follows the outcome, not the window. Among customers active on all 62 days, the flag alone separates churners at ROC AUC 0.936, while no window column's missing flag passes 0.59. Among churners, REGION is missing for 90-96% at every number of active days, while every activity column's missing share falls with activity (decision tables). Its whole value is the flag: LightGBM with the window and the flag scores 0.9309, with REGION 0.9311, and 0.901 without it (400,000 customers, 3-fold cross-validation).
        - IID split, as in the competition: the file is one snapshot of the customer base with no time index, and Zindi's test set is a uniform random 15% of the extract (84.8-85.2% of every 100k block in Train). A deployed model trains on an earlier window, with a gap of at least the 90-day label delay and the customers' history, so the task is tagged ForcedIIDFromTemporal (SPLIT-8). The release has neither dates nor earlier windows, so the cost of the missing time axis cannot be measured: a hold-out by extract order (thirds 0.9026, 100k blocks 0.9028, random 0.9028) measures a customer sort, not time. Recover the dates and earlier windows if a later release has them.
        - Duplicates kept (LEAK-18): without user_id and REGION, 678,270 rows (31.5%) repeat another row exactly. Each row is a different customer with few effective features, so the repeats are natural: 75.3% of the copies have no activity value. The copies hold 317,548 of the 403,986 churners, so dropping them would turn an 18.75% churn task into a 5.9% one about active customers (decision table).
        - dtypes: TENURE (8 bands, none under 3 months) and TOP_PACK (140 packs, written inconsistently by Expresso) are categorical; the other columns are counts or amounts.
        - Note: an activity column is missing when the extract has no record of it; 0 is a record of none. Zeros and missing values coexist in six columns and carry different churn (ON_NET: missing 42.3%, 0 12.6%, above 0 4.6%), so we keep them as released.
        - Note: REGULARITY ranges from 1 to 62; the codebook calls it "nombre de fois que le client est actif pendant 90 jours", so reading it as the active days in the last 62 days of the window is our inference. FREQUENCE, "the number of times the client made revenue" (codebook), reaches 91. ARPU_SEGMENT is REVENUE / 3 rounded in every row; both are kept as released.
        - Note: the task probes flag one_feature (REGULARITY alone ROC AUC 0.890). We keep the task by rule 4 of task_probes.md: active days are the natural core of a churn task, and on the shipped folds an untuned LightGBM beats REGULARITY alone on 3 of 3 folds (0.9023 to 0.9031 against 0.8896 to 0.8902).
        - Note: Zindi's rules forbid redistributing the data, uploads to Kaggle or GitHub included; the Kaggle copies we name are such uploads.
        - Ordinal scales (2026-10-30, the curator's marks of 2026-10-31, CLEAN-14): 1 columns are ordered categories in
          the order of the source's codebook (`ORDINAL_LEVELS`).
    """

    # Task
    target = TARGET
    problem_type = "binary_classification"
    metric = Metric.source(
        "roc_auc",
        original="Area Under the Curve (AUC)",
        reference=(
            "https://zindi.africa/competitions/expresso-churn-prediction (now zindi.world), Evaluation section: 'The "
            "evaluation metric for this challenge is Area Under the Curve (AUC).'"
        ),
        definition="ROC AUC of the churn probability against CHURN",
    )

    # Splits: IID (one snapshot, no time index); the `_1m` version sub-samples the frame to the 1.5M-row budget.
    subsample_to_budget = True
    accepted_check_warnings = {
        "dataset_duplicate_rows": "Every row is a different customer (unique user_id). The copies are customers "
        "mostly (75.3% of the 678,270 copies in the full file) described only by a tenure band and their active days, "
        "all active in the window, so the profiles repeat naturally (LEAK-18). The copies hold 317,548 of the 403,986 "
        "churners: deduplicating would leave a 5.9% churn task about active customers (2026-10-07).",
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "Train.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df[TARGET] = df[TARGET].map({1: "Yes", 0: "No"})
        # user_id: SHA-1 of the row number in Expresso's extract; MRG: "NO" in every row; REGION: its missing flag
        # follows the outcome, not the window (curation comments)
        return drop_columns(df, ["user_id", "MRG", "REGION"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(ordinal=ORDINAL_LEVELS, categorical=["TENURE", "TOP_PACK"])

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
        # ROC AUC of a binary score (the missing flag) is 0.5 + (share missing among churners - among stayers) / 2
        strata = pd.cut(raw["REGULARITY"], [0, 3, 29, 50, 61, 62], labels=["1-3", "4-29", "30-50", "51-61", "62"])
        missing = raw[["REGION", *ACTIVITY]].isna()
        shares = missing.groupby([strata, outcome], observed=True).mean()
        flag_auc = (0.5 + (shares.xs("churned", level=1) - shares.xs("stayed", level=1)) / 2).T
        flag_auc.columns = [f"active days {band}" for band in flag_auc.columns]
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
                    "Among churners the region is missing for 90-96% at every number of active days, while among "
                    "those who stayed the share falls with activity, as it does for the window's own columns "
                    "(MONTANT) in both groups. A field taken from the window would follow the churners' activity "
                    "too, so the region was most likely filled after the window (full file, 2,154,048 customers)."
                ),
                evidence=signature.round(3),
            ),
            Decision(
                title="Among equally active customers, only REGION's missing flag separates churners",
                why=(
                    "ROC AUC of each column's missing flag for churn, within bands of active days (0.5 is no "
                    "separation). Among customers active on all 62 days, missing REGION separates churners at 0.936, "
                    "while no window column passes 0.59 (full file)."
                ),
                evidence=flag_auc.round(3),
            ),
            Decision(
                title="Duplicate rows are kept: different customers with sparse profiles",
                why=(
                    "Every row is a different customer (unique ids). The copies are customers with no or little "
                    "activity in the window, mostly (75.3%) described only by a tenure band and their active days, "
                    "so repeats and conflicting labels are expected (LEAK-18)."
                ),
                evidence=duplicates,
            ),
        ]
