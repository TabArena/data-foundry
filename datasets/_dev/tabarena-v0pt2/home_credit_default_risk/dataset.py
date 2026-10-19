"""Curated dataset definition for `home_credit_default_risk` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TaskSummary, object_columns

TABLES = {
    "application": "application_train.csv",
    "bureau": "bureau.csv",
    "bureau_balance": "bureau_balance.csv",
    "previous_application": "previous_application.csv",
    "pos_cash": "POS_CASH_balance.csv",
    "installments": "installments_payments.csv",
    "credit_card": "credit_card_balance.csv",
}

CATEGORICAL = [
    "NAME_CONTRACT_TYPE",
    "CODE_GENDER",
    "FLAG_OWN_CAR",
    "FLAG_OWN_REALTY",
    "NAME_TYPE_SUITE",
    "NAME_INCOME_TYPE",
    "NAME_EDUCATION_TYPE",
    "NAME_FAMILY_STATUS",
    "NAME_HOUSING_TYPE",
    "OCCUPATION_TYPE",
    "WEEKDAY_APPR_PROCESS_START",
    "FLAG_WORK_PHONE",
    "FLAG_PHONE",
    "REG_CITY_NOT_LIVE_CITY",
    "LIVE_CITY_NOT_WORK_CITY",
    "ORGANIZATION_TYPE",
    "FONDKAPREMONT_MODE",
    "HOUSETYPE_MODE",
    "WALLSMATERIAL_MODE",
    "EMERGENCYSTATE_MODE",
    "FLAG_DOCUMENT_3",
    "FLAG_DOCUMENT_8",
    "FLAG_DOCUMENT_18",
]


class HomeCreditDefaultRisk(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a loan applicant have trouble repaying the loan?",
        use_case=(
            "When a client applies for a loan, a consumer lender scores the risk of payment difficulties from the "
            "application and the client's earlier credits, to decide whether to lend (the Home Credit competition's "
            "task)."
        ),
        row=(
            "One loan application to Home Credit, with the client's earlier credits at Home Credit and at the credit "
            "bureau; the release gives no dates and no country."
        ),
        predicted=(
            "Whether the client paid late, by more than a number of days the source does not state, on at least one "
            "of the loan's first installments."
        ),
        known=(
            "504 features: the application (contract type, amounts, income, family, job, housing, documents and three"
            " external scores) and summaries of the client's credit bureau loans, earlier Home Credit applications "
            "and their installment, card and cash-loan payment records."
        ),
        split="Random applications; the data has no application dates.",
        changes=(
            "We build the features as a popular public competition notebook does, keeping categories as categories, "
            "and keep the features it selected."
        ),
        fit="approximate",
        fit_reason=(
            "The features are known at the application and the label follows within the first installments, but "
            "without application dates the test applications come from the same period as the training ones, whereas "
            "a lender scores later applicants."
        ),
    )

    # Dataset
    unique_name = "home_credit_default_risk"
    year = "2018"
    domain = "finance"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/c/home-credit-default-risk"
    license = "Kaggle Competition Rules"
    data_tags = ("ForcedIIDFromTemporal",)
    download_description = """
        We download the files from the Kaggle data. This dataset starts as a SQL database with multiple tables, so it has multiple files.

        kaggle competitions download -c home-credit-default-risk && unzip home-credit-default-risk.zip -d data_files && rm home-credit-default-risk.zip
        mkdir -p local-data-warehouse/home_credit_default_risk && mv data_files local-data-warehouse/home_credit_default_risk/
    """
    bibtex = r"""
        @misc{Montoya2018HomeCreditDefaultRisk,
          author = {Anna Montoya and inversion and Kirill Odintsov and Martin Kotek},
          title  = {Home Credit Default Risk},
          year   = {2018},
          howpublished = {\url{https://kaggle.com/competitions/home-credit-default-risk}},
          note   = {Kaggle competition}
        }
    """
    curation_comments = """
        We start with the SQL tables from Kaggle. We then merge these tables into a single file following the top Kaggle solutions.
        We start from this file.

        - The top solutions start with various features from public notebooks/kernels. When selecting the kernel to use as our starting point, we looked among the most popular and best performance on the leaderboard. We found https://www.kaggle.com/code/jsaguiar/lightgbm-with-simple-features?scriptVersionId=6025993 and its follow-up https://www.kaggle.com/code/ogrellier/lighgbm-with-selected-features. We use the features of the later one, because it performs better, but not its feature selection (below).
        - We do not follow the script exactly. We do not ordinal encode binary features. Moreover, we do not apply one-hot encoding to all categorical columns. Instead, we do it only when need for aggregations and otherwise keep the categorical column with the original semantics. Moreover, we fix some bugs in the original script that cause it to crash when run out of the box.
        - We drop the columns that hold one value besides missing or copy an earlier column, mostly the shares of the "nan" category the one-hot encoding adds to every table.
        - We compute no statistic over all rows (Lennart, 2026-10-19): the kernel's median income per organisation type (`NEW_INC_BY_ORG`) is dropped, `NEW_SCORES_STD` stays missing where the kernel filled in its mean, and the kernel's feature selection (columns without LightGBM importance, measured on all labelled rows) is not applied, so 709 features ship instead of 504. The kernel computed these over Kaggle's train and test applications, as a competition allows; whether to keep that transductive setting for this task can be checked later.
        - Potential leak, kept on purpose: the 43 building columns (`*_AVG`, `*_MODE`, `*_MEDI`, `TOTALAREA_MODE`) are "normalized information about building where the client lives" (HomeCredit_columns_description.csv) and each spans exactly 0 to 1, so Home Credit likely scaled them over all applications, ours included; the method is not documented and no raw values exist. Kept (Lennart, 2026-10-19): a scaling over all rows is no strong leak; revisit if Home Credit documents it.
        - We replace values that became inf after aggregation with NaN. This occurred across several aggregated columns.
        - Tagged ForcedIIDFromTemporal: applications arrive over time, but the release has no application dates (its DAYS_ columns are "time only relative to the application", HomeCredit_columns_description.csv), so the split is random.
    """

    # Task
    target = "TARGET"
    problem_type = "binary_classification"
    accepted_check_warnings = {
        "dataset_missing_value_sentinel": "POS_MONTHS_BALANCE_MAX = -1 is a real value: MONTHS_BALANCE counts months "
        "relative to the application, so -1 is a POS/cash loan still reported in the month before it.",
    }

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        return {name: pd.read_csv(raw_dir / "data_files" / file) for name, file in TABLES.items()}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        # Follows the kernel's functions: application features, then one aggregate table per source table.
        df = _application_features(raw["application"])
        aggregates = [
            _bureau_features(raw["bureau"], raw["bureau_balance"]),
            _previous_application_features(raw["previous_application"]),
            _pos_cash_features(raw["pos_cash"]),
            _installments_features(raw["installments"]),
            _credit_card_features(raw["credit_card"]),
        ]
        for agg in aggregates:
            df = df.join(agg, how="left", on="SK_ID_CURR")
        # The kernel's feature selection (LightGBM importance on all labelled rows) is not applied: every column stays
        df = df.drop(columns=["SK_ID_CURR"])
        # Extra preprocessing and cleaning from us
        df = df.drop(columns=["POS_COUNT"])  # duplicate of POS_MONTHS_BALANCE_SIZE
        # ratios that divide by zero give +-inf: missing
        numeric = df.select_dtypes("number").columns
        df[numeric] = df[numeric].replace([np.inf, -np.inf], np.nan)
        # the min and max of a one-hot flag come out as True/False with gaps (applicants without the table): 0/1
        for column in object_columns(df):
            if df[column].dropna().map(type).eq(bool).all():
                df[column] = df[column].astype("float64")
        # columns without information: one value besides missing, or a copy of an earlier column (mostly the shares
        # of the "nan" category the one-hot encoding adds to every table)
        features = df.columns.drop(self.target)
        df = df.drop(columns=[c for c in features if df[c].nunique() <= 1])
        return df.drop(columns=_copies(df.drop(columns=self.target)))

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=CATEGORICAL)


def _copies(df: pd.DataFrame) -> list[str]:
    """The columns equal to an earlier column in every row (missing values included), in column order."""
    seen, copies = {}, []
    for column in df.columns:
        key = int(pd.util.hash_pandas_object(df[column], index=False).sum())
        if any(df[column].equals(df[other]) for other in seen.get(key, [])):
            copies.append(column)
        else:
            seen.setdefault(key, []).append(column)
    return copies


def _application_features(df: pd.DataFrame) -> pd.DataFrame:
    """The kernel's `application_train_test`: cleaning and ratio features on the application table."""
    # Remove 4 applications with XNA CODE_GENDER (train set)
    df = df[df["CODE_GENDER"] != "XNA"].copy()
    # NaN values for DAYS_EMPLOYED: 365.243 -> nan
    df["DAYS_EMPLOYED"] = df["DAYS_EMPLOYED"].replace(365243, np.nan)
    # Special features docs and live
    docs = [_f for _f in df.columns if "FLAG_DOC" in _f]
    df["NEW_DOC_IND_AVG"] = df[docs].mean(axis=1)
    df["NEW_DOC_IND_STD"] = df[docs].std(axis=1)
    df["NEW_DOC_IND_KURT"] = df[docs].kurtosis(axis=1)
    live = [_f for _f in df.columns if ("FLAG_" in _f) & ("FLAG_DOC" not in _f) & ("_FLAG_" not in _f)]
    tmp_live_df = df[live].copy()
    for bin_feature in ["FLAG_OWN_CAR", "FLAG_OWN_REALTY"]:
        tmp_live_df[bin_feature], _ = pd.factorize(tmp_live_df[bin_feature])
    df["NEW_LIVE_IND_SUM"] = tmp_live_df.sum(axis=1)
    df["NEW_LIVE_IND_STD"] = tmp_live_df.std(axis=1)
    df["NEW_LIVE_IND_KURT"] = tmp_live_df[live].kurtosis(axis=1)
    # Special features
    df["NEW_CREDIT_TO_ANNUITY_RATIO"] = df["AMT_CREDIT"] / df["AMT_ANNUITY"]
    df["NEW_CREDIT_TO_GOODS_RATIO"] = df["AMT_CREDIT"] / df["AMT_GOODS_PRICE"]
    df["NEW_INC_PER_CHLD"] = df["AMT_INCOME_TOTAL"] / (1 + df["CNT_CHILDREN"])
    df["NEW_EMPLOY_TO_BIRTH_RATIO"] = df["DAYS_EMPLOYED"] / df["DAYS_BIRTH"]
    df["NEW_ANNUITY_TO_INCOME_RATIO"] = df["AMT_ANNUITY"] / (1 + df["AMT_INCOME_TOTAL"])
    df["NEW_SOURCES_PROD"] = df["EXT_SOURCE_1"] * df["EXT_SOURCE_2"] * df["EXT_SOURCE_3"]
    df["NEW_EXT_SOURCES_MEAN"] = df[["EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3"]].mean(axis=1)
    df["NEW_SCORES_STD"] = df[["EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3"]].std(axis=1)
    df["NEW_CAR_TO_BIRTH_RATIO"] = df["OWN_CAR_AGE"] / df["DAYS_BIRTH"]
    df["NEW_CAR_TO_EMPLOY_RATIO"] = df["OWN_CAR_AGE"] / df["DAYS_EMPLOYED"]
    df["NEW_PHONE_TO_BIRTH_RATIO"] = df["DAYS_LAST_PHONE_CHANGE"] / df["DAYS_BIRTH"]
    df["NEW_PHONE_TO_EMPLOY_RATIO"] = df["DAYS_LAST_PHONE_CHANGE"] / df["DAYS_EMPLOYED"]
    df["NEW_CREDIT_TO_INCOME_RATIO"] = df["AMT_CREDIT"] / df["AMT_INCOME_TOTAL"]
    return df


def _bureau_features(bureau: pd.DataFrame, bb: pd.DataFrame) -> pd.DataFrame:
    """The kernel's `bureau_and_balance`: aggregates per applicant (SK_ID_CURR)."""
    # Bureau balance: Perform aggregations and merge with bureau.csv
    bb_w_one_hot = pd.get_dummies(bb, columns=["STATUS"], dummy_na=True)
    bb_one_hot_cat_cols = [c for c in bb_w_one_hot.columns if c not in bb.columns]
    bb_aggregations = {"MONTHS_BALANCE": ["min", "max", "size"]}
    for col in bb_one_hot_cat_cols:
        bb_aggregations[col] = ["mean"]
    bb_agg = bb_w_one_hot.groupby("SK_ID_BUREAU").agg(bb_aggregations)
    bb_agg.columns = pd.Index([e[0] + "_" + e[1].upper() for e in bb_agg.columns.tolist()])
    bureau = bureau.join(bb_agg, how="left", on="SK_ID_BUREAU")
    bureau.drop(["SK_ID_BUREAU"], axis=1, inplace=True)
    # Bureau and bureau_balance numeric features
    num_aggregations = {
        "DAYS_CREDIT": ["min", "max", "mean", "var"],
        "DAYS_CREDIT_ENDDATE": ["min", "max", "mean"],
        "DAYS_CREDIT_UPDATE": ["mean"],
        "CREDIT_DAY_OVERDUE": ["max", "mean"],
        "AMT_CREDIT_MAX_OVERDUE": ["mean"],
        "AMT_CREDIT_SUM": ["max", "mean", "sum"],
        "AMT_CREDIT_SUM_DEBT": ["max", "mean", "sum"],
        "AMT_CREDIT_SUM_OVERDUE": ["mean"],
        "AMT_CREDIT_SUM_LIMIT": ["mean", "sum"],
        "AMT_ANNUITY": ["max", "mean"],
        "CNT_CREDIT_PROLONG": ["sum"],
        "MONTHS_BALANCE_MIN": ["min"],
        "MONTHS_BALANCE_MAX": ["max"],
        "MONTHS_BALANCE_SIZE": ["mean", "sum"],
    }
    # Bureau and bureau_balance categorical features
    cat_aggregations = {}
    for cat in bb_one_hot_cat_cols:
        cat_aggregations[cat + "_MEAN"] = ["mean"]
    org_cols = list(bureau.columns)
    bureau = pd.get_dummies(bureau, columns=["CREDIT_ACTIVE", "CREDIT_CURRENCY", "CREDIT_TYPE"], dummy_na=True)
    bureau_one_hot_cat_cols = [c for c in bureau.columns if c not in org_cols]
    for cat in bureau_one_hot_cat_cols:
        cat_aggregations[cat] = ["mean"]
    bureau_agg = bureau.groupby("SK_ID_CURR").agg({**num_aggregations, **cat_aggregations})
    bureau_agg.columns = pd.Index(["BURO_" + e[0] + "_" + e[1].upper() for e in bureau_agg.columns.tolist()])
    # Bureau: Active credits - using only numerical aggregations
    active = bureau[bureau["CREDIT_ACTIVE_Active"] == 1]
    active_agg = active.groupby("SK_ID_CURR").agg(num_aggregations)
    cols = active_agg.columns.tolist()
    active_agg.columns = pd.Index(["ACTIVE_" + e[0] + "_" + e[1].upper() for e in active_agg.columns.tolist()])
    bureau_agg = bureau_agg.join(active_agg, how="left", on="SK_ID_CURR")
    # Bureau: Closed credits - using only numerical aggregations
    closed = bureau[bureau["CREDIT_ACTIVE_Closed"] == 1]
    closed_agg = closed.groupby("SK_ID_CURR").agg(num_aggregations)
    closed_agg.columns = pd.Index(["CLOSED_" + e[0] + "_" + e[1].upper() for e in closed_agg.columns.tolist()])
    bureau_agg = bureau_agg.join(closed_agg, how="left", on="SK_ID_CURR")
    for e in cols:
        bureau_agg["NEW_RATIO_BURO_" + e[0] + "_" + e[1].upper()] = (
            bureau_agg["ACTIVE_" + e[0] + "_" + e[1].upper()] / bureau_agg["CLOSED_" + e[0] + "_" + e[1].upper()]
        )
    return bureau_agg


def _previous_application_features(prev: pd.DataFrame) -> pd.DataFrame:
    """The kernel's `previous_applications`: aggregates per applicant."""
    # Cat encode for aggregations
    org_cols = list(prev.columns)
    prev = pd.get_dummies(prev, columns=object_columns(prev), dummy_na=True)
    prev_cat_cols = [c for c in prev.columns if c not in org_cols]
    # Days 365.243 values -> nan
    prev["DAYS_FIRST_DRAWING"] = prev["DAYS_FIRST_DRAWING"].replace(365243, np.nan)
    prev["DAYS_FIRST_DUE"] = prev["DAYS_FIRST_DUE"].replace(365243, np.nan)
    prev["DAYS_LAST_DUE_1ST_VERSION"] = prev["DAYS_LAST_DUE_1ST_VERSION"].replace(365243, np.nan)
    prev["DAYS_LAST_DUE"] = prev["DAYS_LAST_DUE"].replace(365243, np.nan)
    prev["DAYS_TERMINATION"] = prev["DAYS_TERMINATION"].replace(365243, np.nan)
    # Add feature: value ask / value received percentage
    prev["APP_CREDIT_PERC"] = prev["AMT_APPLICATION"] / prev["AMT_CREDIT"]
    # Previous applications numeric features
    num_aggregations = {
        "AMT_ANNUITY": ["min", "max", "mean"],
        "AMT_APPLICATION": ["min", "max", "mean"],
        "AMT_CREDIT": ["min", "max", "mean"],
        "APP_CREDIT_PERC": ["min", "max", "mean", "var"],
        "AMT_DOWN_PAYMENT": ["min", "max", "mean"],
        "AMT_GOODS_PRICE": ["min", "max", "mean"],
        "HOUR_APPR_PROCESS_START": ["min", "max", "mean"],
        "RATE_DOWN_PAYMENT": ["min", "max", "mean"],
        "DAYS_DECISION": ["min", "max", "mean"],
        "CNT_PAYMENT": ["mean", "sum"],
    }
    # Previous applications categorical features
    cat_aggregations = {}
    for cat in prev_cat_cols:
        cat_aggregations[cat] = ["mean"]
    prev_agg = prev.groupby("SK_ID_CURR").agg({**num_aggregations, **cat_aggregations})
    prev_agg.columns = pd.Index(["PREV_" + e[0] + "_" + e[1].upper() for e in prev_agg.columns.tolist()])
    # Previous Applications: Approved Applications - only numerical features
    approved = prev[prev["NAME_CONTRACT_STATUS_Approved"] == 1]
    approved_agg = approved.groupby("SK_ID_CURR").agg(num_aggregations)
    cols = approved_agg.columns.tolist()
    approved_agg.columns = pd.Index(["APPROVED_" + e[0] + "_" + e[1].upper() for e in approved_agg.columns.tolist()])
    prev_agg = prev_agg.join(approved_agg, how="left", on="SK_ID_CURR")
    # Previous Applications: Refused Applications - only numerical features
    refused = prev[prev["NAME_CONTRACT_STATUS_Refused"] == 1]
    refused_agg = refused.groupby("SK_ID_CURR").agg(num_aggregations)
    refused_agg.columns = pd.Index(["REFUSED_" + e[0] + "_" + e[1].upper() for e in refused_agg.columns.tolist()])
    prev_agg = prev_agg.join(refused_agg, how="left", on="SK_ID_CURR")
    for e in cols:
        prev_agg["NEW_RATIO_PREV_" + e[0] + "_" + e[1].upper()] = (
            prev_agg["APPROVED_" + e[0] + "_" + e[1].upper()] / prev_agg["REFUSED_" + e[0] + "_" + e[1].upper()]
        )
    return prev_agg


def _pos_cash_features(pos: pd.DataFrame) -> pd.DataFrame:
    """The kernel's `pos_cash`: aggregates per applicant."""
    # Cat encode for aggregations
    org_cols = list(pos.columns)
    pos = pd.get_dummies(pos, columns=object_columns(pos), dummy_na=True)
    pos_cat_cols = [c for c in pos.columns if c not in org_cols]
    # Features
    aggregations = {
        "MONTHS_BALANCE": ["max", "mean", "size"],
        "SK_DPD": ["max", "mean"],
        "SK_DPD_DEF": ["max", "mean"],
    }
    for cat in pos_cat_cols:
        aggregations[cat] = ["mean"]
    pos_agg = pos.groupby("SK_ID_CURR").agg(aggregations)
    pos_agg.columns = pd.Index(["POS_" + e[0] + "_" + e[1].upper() for e in pos_agg.columns.tolist()])
    # Count pos cash accounts
    pos_agg["POS_COUNT"] = pos.groupby("SK_ID_CURR").size()
    return pos_agg


def _installments_features(ins: pd.DataFrame) -> pd.DataFrame:
    """The kernel's `installments_payments`: aggregates per applicant."""
    # Cat encode for aggregations
    org_cols = list(ins.columns)
    ins = pd.get_dummies(ins, columns=object_columns(ins), dummy_na=True)
    ins_cat_cols = [c for c in ins.columns if c not in org_cols]
    # Percentage and difference paid in each installment (amount paid and installment value)
    ins["PAYMENT_PERC"] = ins["AMT_PAYMENT"] / ins["AMT_INSTALMENT"]
    ins["PAYMENT_DIFF"] = ins["AMT_INSTALMENT"] - ins["AMT_PAYMENT"]
    # Days past due and days before due (no negative values)
    ins["DPD"] = ins["DAYS_ENTRY_PAYMENT"] - ins["DAYS_INSTALMENT"]
    ins["DBD"] = ins["DAYS_INSTALMENT"] - ins["DAYS_ENTRY_PAYMENT"]
    ins["DPD"] = ins["DPD"].apply(lambda x: x if x > 0 else 0)
    ins["DBD"] = ins["DBD"].apply(lambda x: x if x > 0 else 0)
    # Features: Perform aggregations
    aggregations = {
        "NUM_INSTALMENT_VERSION": ["nunique"],
        "DPD": ["max", "mean", "sum"],
        "DBD": ["max", "mean", "sum"],
        "PAYMENT_PERC": ["max", "mean", "sum", "var"],
        "PAYMENT_DIFF": ["max", "mean", "sum", "var"],
        "AMT_INSTALMENT": ["max", "mean", "sum"],
        "AMT_PAYMENT": ["min", "max", "mean", "sum"],
        "DAYS_ENTRY_PAYMENT": ["max", "mean", "sum"],
    }
    for cat in ins_cat_cols:
        aggregations[cat] = ["mean"]
    ins_agg = ins.groupby("SK_ID_CURR").agg(aggregations)
    ins_agg.columns = pd.Index(["INSTAL_" + e[0] + "_" + e[1].upper() for e in ins_agg.columns.tolist()])
    # Count installments accounts
    ins_agg["INSTAL_COUNT"] = ins.groupby("SK_ID_CURR").size()
    return ins_agg


def _credit_card_features(cc: pd.DataFrame) -> pd.DataFrame:
    """The kernel's `credit_card_balance`: aggregates per applicant."""
    # Cat encode for aggregations
    cc = pd.get_dummies(cc, columns=object_columns(cc), dummy_na=True)
    # General aggregations
    cc.drop(["SK_ID_PREV"], axis=1, inplace=True)
    cc_agg = cc.groupby("SK_ID_CURR").agg(["min", "max", "mean", "sum", "var"])
    cc_agg.columns = pd.Index(["CC_" + e[0] + "_" + e[1].upper() for e in cc_agg.columns.tolist()])
    # Count credit card lines
    cc_agg["CC_COUNT"] = cc.groupby("SK_ID_CURR").size()
    return cc_agg
