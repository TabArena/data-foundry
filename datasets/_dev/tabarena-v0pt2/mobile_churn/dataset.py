"""Curated dataset definition for `mobile_churn` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, TaskSummary, drop_columns

RAW_FILE = "mobile-churn-data.xlsx"
"""The one file of the Kaggle dataset dimitaryanev/mobilechurndataxlsx; one sheet, "Churn prediction data"."""

DUPLICATED_INACTIVE_DAYS = [
    f"{kind}_to_{destination}_inactive_days"
    for kind in ("calls_outgoing", "sms_outgoing")
    for destination in ("onnet", "offnet", "abroad")
]
"""Per-destination inactive days, equal to calls_outgoing_inactive_days or sms_outgoing_inactive_days in every row."""

INACTIVE_DAYS = [
    "user_no_outgoing_activity_in_days",
    "reloads_inactive_days",
    "calls_outgoing_inactive_days",
    "sms_outgoing_inactive_days",
    "gprs_inactive_days",
]
"""Days since the last activity of a kind, counted back from the snapshot at the end of the record month."""

NO_ACTIVATION_DATE = 10_000
"""user_lifetime from here on (15,856 to 15,947) is a day count from 1970-01-01, the default for a missing activation
date."""

MAX_INACTIVE_DAYS = 100
"""The longest real inactive-days value: 92 days in June (100 for user_no_outgoing_activity_in_days), 30 after June.
Larger values count back from the snapshot to one of two default dates: 2010-01-01 (1,271 to 1,338, no such activity
on record) or 2012-09-28 (270 to 337)."""


def never_activated(raw: pd.DataFrame) -> pd.Series:
    """Accounts without the intake flag and without an activation date: SIM cards not taken into use."""
    return raw["user_intake"].eq(0) & raw["user_lifetime"].ge(NO_ACTIVATION_DATE)


class MobileChurn(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a prepaid mobile customer churn?",
        use_case=(
            "At the end of each month, a mobile operator scores its activated prepaid accounts for churn, for example"
            " to decide whom to target with retention offers."
        ),
        row=(
            "One activated prepaid account of one unnamed mobile operator at the end of June, July or August 2013 "
            "(54,207 accounts, each once)."
        ),
        predicted=(
            "Whether the account churned (9.9%); the source defines neither churn nor its time window, but the data "
            "place it after the month's end."
        ),
        known=(
            "The account's tenure and balance, its calls, text messages, data use, spending and top-ups in the month "
            "and the last 100 days, and the days since each kind of activity."
        ),
        split=("Random accounts; the July and August rows are the accounts that joined in those months."),
        changes=(
            "We drop the 12,262 SIM cards never activated, which held 61% of the churners and whose label only says "
            "the card was never used."
        ),
        fit="approximate",
        fit_reason=(
            "Every input describes the account up to the scoring date, as when the model is used, but churn has no "
            "stated definition or horizon and the operator is unknown."
        ),
    )

    # Dataset
    unique_name = "mobile_churn"
    year = "2019"
    domain = "business & marketing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/dimitaryanev/mobilechurndataxlsx"
    license = None  # the Kaggle data card states "unknown"; OpenML 44231 states "Unknown"
    download_description = """
        We download the Kaggle dataset dimitaryanev/mobilechurndataxlsx (uploaded on 2019-10-31, never updated). It
        holds one file. Kaggle does not version-pin a download, so check the hash. OpenML 44231
        (https://www.openml.org/d/44231, uploaded 2022-10-05) holds the same 66,469 rows with identical values in the
        same order, as parquet (the definition reads the xlsx):
        wget -O dataset_44231.pq https://data.openml.org/datasets/0004/44231/dataset_44231.pq
        mobile-churn-data.xlsx: sha256 ebc820fad54224824a05fa5a0fbee5be5321796a2ba584b16f8f232fc70271a1

        mkdir -p local-data-warehouse/mobile_churn && cd local-data-warehouse/mobile_churn
        kaggle datasets download dimitaryanev/mobilechurndataxlsx && unzip mobilechurndataxlsx.zip
        rm mobilechurndataxlsx.zip
    """
    bibtex = """
        @misc{dimitaryanev2019mobilechurn,
          author = {dimitaryanev},
          title = {mobile-churn-data.xlsx},
          year = {2019},
          howpublished = {\\url{https://www.kaggle.com/datasets/dimitaryanev/mobilechurndataxlsx}},
          note = {Kaggle dataset uploaded on 2019-10-31 without a description; also OpenML 44231}
        }
    """
    curation_comments = """
        We start with mobile-churn-data.xlsx (66,469 rows) from the Kaggle dataset dimitaryanev/mobilechurndataxlsx (2019; OpenML 44231 is the same file): prepaid accounts of one unnamed mobile operator in June to August 2013. No paper or operator behind the data was found (the record keeps "Missing source information").

        - Prediction point: the end of the record month (30 June, 31 July or 31 August 2013), when the operator scores each activated prepaid account for churn from its state at that date and its usage in the month and the last 100 days. Churn is not defined in the source, but the data place the label after the snapshot: 52.6% of the June churners active in the last 30 days were last active 0-5 days before it, and the churn rate rises with the days without activity with no cutoff.
        - Both classes share their month's snapshot date, which the "no activity" value of the inactive-days columns gives (decision table), unlike churn_telco_europa.
        - Dropped: the 12,262 accounts never activated (user_intake = 0 and no activation date), SIM cards not taken into use (decision table). They come in provisioning batches of consecutive ids and held 8,515 of the 13,907 churners (61%), so their label reads "the SIM was never used", and a random split lets a model learn each batch's churn rate (LightGBM ROC AUC 0.908 on all rows, 0.882 with each batch held together).
        - IID split: each row is a different account (54,207 distinct user_account_id). After the drop the July and August rows are the accounts that joined in those months (527 and 1,006), so a split by record month would test a change of cohort, not of time; month stays as a feature.
        - We drop year (2013 in every row), user_account_id (an id, numbered in creation order) and the six per-destination inactive-days columns, which equal the call or SMS inactive days in every row.
        - Missing values: user_lifetime of 15,856 or more counts from 1970-01-01, the default for a missing activation date, and remains for 1,295 accounts that joined in their month. 13.8% of them were active before the day it counts to, so we set it to missing instead of rebuilding the tenure.
        - Inactive-days values above 100 count back to a default date (2010-01-01 for no activity on record, or 2012-09-28) and become missing; real values reach 92 days in June (100 for user_no_outgoing_activity_in_days). Left in, the default dates would also encode the snapshot date.
        - Target: churn mapped to Yes (5,392 accounts, 9.9%) and No.
        - Features: the remaining 57 columns as published, all numeric; derived ones such as user_spendings (the sum of three spendings columns) stay.
        - Duplicates kept: 9 rows are exact copies, and 8 feature vectors occur with both labels.
        - Anomaly: negative amounts in six spending and top-up columns (refunds or corrections); kept as published.
        - Note: the licence is "unknown" (Kaggle data card, OpenML 44231). The year 2019 is that of the Kaggle upload; the data are from 2013.
    """

    # Task
    target = "churn"
    problem_type = "binary_classification"

    accepted_check_warnings = {
        "meta_license_unknown": (
            'The Kaggle data card states the licence as "unknown" and OpenML 44231 as "Unknown"; no other source is '
            "known."
        ),
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_excel(raw_dir / RAW_FILE, sheet_name="Churn prediction data")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # SIM cards not taken into use: no intake flag and no activation date
        df = raw.loc[~never_activated(raw)]
        # a constant, the account id, and six copies of the overall call and SMS inactive days
        df = drop_columns(df, ["year", "user_account_id", *DUPLICATED_INACTIVE_DAYS])
        # day counts from default dates: 1970-01-01 (no activation date), 2010-01-01 and 2012-09-28 (no activity)
        df["user_lifetime"] = df["user_lifetime"].where(df["user_lifetime"] < NO_ACTIVATION_DATE)
        for column in INACTIVE_DAYS:
            df[column] = df[column].where(df[column] <= MAX_INACTIVE_DAYS)
        df[self.target] = df[self.target].map({1: "Yes", 0: "No"})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # every feature is numeric; the target becomes a category without being listed
        del df
        return FeatureTypes()

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        del df
        never = never_activated(raw)
        used = (
            raw["last_100_calls_outgoing_duration"].gt(0)
            | raw["last_100_sms_outgoing_count"].gt(0)
            | raw["last_100_gprs_usage"].gt(0)
        )
        month = raw["month"]
        cohorts = pd.DataFrame(
            {
                "rows": month.groupby(month).size(),
                "never activated (dropped)": never.groupby(month).sum(),
                "their churn rate": raw.loc[never, "churn"].groupby(month[never]).mean().round(3),
                "their share used in 100 days": used[never].groupby(month[never]).mean().round(3),
                "kept": (~never).groupby(month).sum(),
                "kept churn rate": raw.loc[~never, "churn"].groupby(month[~never]).mean().round(3),
                "kept share joined this month": raw.loc[~never, "user_intake"].groupby(month[~never]).mean().round(3),
            }
        )
        kept = raw.loc[~never]
        last = kept[INACTIVE_DAYS].max(axis=1)
        on_record = last.ge(1_000)
        snapshots = pd.DataFrame(
            {
                "month": kept.loc[on_record, "month"],
                "snapshot (2010-01-01 + no-activity value)": (
                    pd.Timestamp("2010-01-01") + pd.to_timedelta(last[on_record], unit="D")
                ).dt.strftime("%Y-%m-%d"),
                "churn": kept.loc[on_record, "churn"],
            }
        )
        dates = (
            snapshots.groupby(["month", "snapshot (2010-01-01 + no-activity value)"])["churn"]
            .agg(stayers=lambda s: int((s == 0).sum()), churners="sum")
            .reset_index()
        )
        return [
            Decision(
                "Accounts never activated are dropped: SIM cards not taken into use",
                "Rows without the intake flag and without an activation date have no call minutes, SMS or data in 100 "
                "days in over 99% of cases and come in provisioning batches; their label reads 'the SIM was never "
                "used', not customer churn. The kept July and August rows are the accounts that joined in those months.",
                cohorts,
            ),
            Decision(
                "Both classes share their month's snapshot date",
                "The no-activity value of the inactive-days columns is the day count from 2010-01-01 to the snapshot. "
                "Within a month, churners and stayers carry the same values, so the classes were not recorded at "
                "different dates (as in churn_telco_europa).",
                dates,
            ),
        ]
