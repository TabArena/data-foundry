"""Curated dataset definition for `home_credit_default_risk` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class HomeCreditDefaultRisk(AbstractCuratedDataset):
    # Dataset
    unique_name = "home_credit_default_risk"
    year = "2018"
    domain = "finance"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/c/home-credit-default-risk"
    license = "Kaggle Competition Rules"
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

        - The top solutions start with various features from public notebooks/kernels. When selecting the kernel to use as our starting point, we looked among the most popular and best performance on the leaderboard. We found https://www.kaggle.com/code/jsaguiar/lightgbm-with-simple-features?scriptVersionId=6025993 and its follow-up https://www.kaggle.com/code/ogrellier/lighgbm-with-selected-features. We use the later one, because it performance better and comes with a reduced set of features from the initial raw merges. Note, this may introduce a slight bias, as the feature selection was done for LGBM.
        - We do not follow the script exactly. We do not ordinal encode binary features. Moreover, we do not apply one-hot encoding to all categorical columns. Instead, we do it only when need for aggregations and otherwise keep the categorical column with the original semantics. Moreover, we fix some bugs in the original script that cause it to crash when run out of the box.
        - We drop a duplicated column after preprocessing.
        - We replace values that became inf after aggregation with NaN. This occurred across several aggregated columns.
    """

    # Task
    target = "TARGET"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # =========== `def application_train_test` refactored ===========
        df = pd.read_csv(raw_dir / "data_files" / "application_train.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Remove 4 applications with XNA CODE_GENDER (train set)
        df = df[df["CODE_GENDER"] != "XNA"]
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
        del tmp_live_df
        # Special features
        inc_by_org = (
            df[["AMT_INCOME_TOTAL", "ORGANIZATION_TYPE"]].groupby("ORGANIZATION_TYPE").median()["AMT_INCOME_TOTAL"]
        )
        df["NEW_INC_BY_ORG"] = df["ORGANIZATION_TYPE"].map(inc_by_org)
        df["NEW_CREDIT_TO_ANNUITY_RATIO"] = df["AMT_CREDIT"] / df["AMT_ANNUITY"]
        df["NEW_CREDIT_TO_GOODS_RATIO"] = df["AMT_CREDIT"] / df["AMT_GOODS_PRICE"]
        df["NEW_INC_PER_CHLD"] = df["AMT_INCOME_TOTAL"] / (1 + df["CNT_CHILDREN"])
        df["NEW_EMPLOY_TO_BIRTH_RATIO"] = df["DAYS_EMPLOYED"] / df["DAYS_BIRTH"]
        df["NEW_ANNUITY_TO_INCOME_RATIO"] = df["AMT_ANNUITY"] / (1 + df["AMT_INCOME_TOTAL"])
        df["NEW_SOURCES_PROD"] = df["EXT_SOURCE_1"] * df["EXT_SOURCE_2"] * df["EXT_SOURCE_3"]
        df["NEW_EXT_SOURCES_MEAN"] = df[["EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3"]].mean(axis=1)
        df["NEW_SCORES_STD"] = df[["EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3"]].std(axis=1)
        df["NEW_SCORES_STD"] = df["NEW_SCORES_STD"].fillna(df["NEW_SCORES_STD"].mean())
        df["NEW_CAR_TO_BIRTH_RATIO"] = df["OWN_CAR_AGE"] / df["DAYS_BIRTH"]
        df["NEW_CAR_TO_EMPLOY_RATIO"] = df["OWN_CAR_AGE"] / df["DAYS_EMPLOYED"]
        df["NEW_PHONE_TO_BIRTH_RATIO"] = df["DAYS_LAST_PHONE_CHANGE"] / df["DAYS_BIRTH"]
        df["NEW_PHONE_TO_EMPLOY_RATIO"] = df["DAYS_LAST_PHONE_CHANGE"] / df["DAYS_EMPLOYED"]
        df["NEW_CREDIT_TO_INCOME_RATIO"] = df["AMT_CREDIT"] / df["AMT_INCOME_TOTAL"]
        del docs, live, inc_by_org
        as_cat_dtype = [
            "TARGET",
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
            "FLAG_OWN_CAR",
            "FLAG_MOBIL",
            "FLAG_EMP_PHONE",
            "FLAG_WORK_PHONE",
            "FLAG_CONT_MOBILE",
            "FLAG_PHONE",
            "FLAG_EMAILREG_REGION_NOT_LIVE_REGION",
            "REG_REGION_NOT_WORK_REGION",
            "LIVE_REGION_NOT_WORK_REGION",
            "REG_CITY_NOT_LIVE_CITY",
            "REG_CITY_NOT_WORK_CITY",
            "LIVE_CITY_NOT_WORK_CITY",
            "ORGANIZATION_TYPE",
            "FONDKAPREMONT_MODE",
            "HOUSETYPE_MODE",
            "WALLSMATERIAL_MODE",
            "EMERGENCYSTATE_MODE",
            # Document flags
            "FLAG_DOCUMENT_2",
            "FLAG_DOCUMENT_3",
            "FLAG_DOCUMENT_4",
            "FLAG_DOCUMENT_5",
            "FLAG_DOCUMENT_6",
            "FLAG_DOCUMENT_7",
            "FLAG_DOCUMENT_8",
            "FLAG_DOCUMENT_9",
            "FLAG_DOCUMENT_10",
            "FLAG_DOCUMENT_11",
            "FLAG_DOCUMENT_12",
            "FLAG_DOCUMENT_13",
            "FLAG_DOCUMENT_14",
            "FLAG_DOCUMENT_15",
            "FLAG_DOCUMENT_16",
            "FLAG_DOCUMENT_17",
            "FLAG_DOCUMENT_18",
            "FLAG_DOCUMENT_19",
            "FLAG_DOCUMENT_20",
            "FLAG_DOCUMENT_21",
        ]
        # =========== `def bureau_and_balance` refactored ===========
        bureau = pd.read_csv(self.raw_dir / "data_files" / "bureau.csv")
        # Bureau balance: Perform aggregations and merge with bureau.csv
        bb = pd.read_csv(self.raw_dir / "data_files" / "bureau_balance.csv")
        bb_w_one_hot = pd.get_dummies(bb, columns=["STATUS"], dummy_na=True)
        bb_one_hot_cat_cols = [c for c in bb_w_one_hot.columns if c not in bb.columns]
        bb_aggregations = {"MONTHS_BALANCE": ["min", "max", "size"]}
        for col in bb_one_hot_cat_cols:
            bb_aggregations[col] = ["mean"]
        bb_agg = bb_w_one_hot.groupby("SK_ID_BUREAU").agg(bb_aggregations)
        bb_agg.columns = pd.Index([e[0] + "_" + e[1].upper() for e in bb_agg.columns.tolist()])
        bureau = bureau.join(bb_agg, how="left", on="SK_ID_BUREAU")
        bureau.drop(["SK_ID_BUREAU"], axis=1, inplace=True)
        del bb, bb_agg, bb_w_one_hot
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
        del active, active_agg, bureau
        df = df.join(bureau_agg, how="left", on="SK_ID_CURR")
        del bureau_agg
        # =========== `def previous_applications` refactored ===========
        prev = pd.read_csv(self.raw_dir / "data_files" / "previous_application.csv")
        # Cat encode for aggregations
        org_cols = list(prev.columns)
        prev = pd.get_dummies(prev, columns=list(prev.select_dtypes(include=["object"]).columns), dummy_na=True)
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
        approved_agg.columns = pd.Index(
            ["APPROVED_" + e[0] + "_" + e[1].upper() for e in approved_agg.columns.tolist()]
        )
        prev_agg = prev_agg.join(approved_agg, how="left", on="SK_ID_CURR")
        # Previous Applications: Refused Applications - only numerical features
        refused = prev[prev["NAME_CONTRACT_STATUS_Refused"] == 1]
        refused_agg = refused.groupby("SK_ID_CURR").agg(num_aggregations)
        refused_agg.columns = pd.Index(["REFUSED_" + e[0] + "_" + e[1].upper() for e in refused_agg.columns.tolist()])
        prev_agg = prev_agg.join(refused_agg, how="left", on="SK_ID_CURR")
        del refused, refused_agg, approved, approved_agg, prev, prev_cat_cols
        for e in cols:
            prev_agg["NEW_RATIO_PREV_" + e[0] + "_" + e[1].upper()] = (
                prev_agg["APPROVED_" + e[0] + "_" + e[1].upper()] / prev_agg["REFUSED_" + e[0] + "_" + e[1].upper()]
            )
        df = df.join(prev_agg, how="left", on="SK_ID_CURR")
        del prev_agg
        # =========== `def pos_cash` refactored ===========
        pos = pd.read_csv(self.raw_dir / "data_files" / "POS_CASH_balance.csv")
        # Cat encode for aggregations
        org_cols = list(pos.columns)
        pos = pd.get_dummies(pos, columns=list(pos.select_dtypes(include=["object"]).columns), dummy_na=True)
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
        df = df.join(pos_agg, how="left", on="SK_ID_CURR")
        del pos, pos_agg, pos_cat_cols
        # =========== `def installments_payments` refactored ===========
        ins = pd.read_csv(self.raw_dir / "data_files" / "installments_payments.csv")
        # Cat encode for aggregations
        org_cols = list(ins.columns)
        ins = pd.get_dummies(ins, columns=list(ins.select_dtypes(include=["object"]).columns), dummy_na=True)
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
        df = df.join(ins_agg, how="left", on="SK_ID_CURR")
        del ins, ins_agg, ins_cat_cols
        # =========== `def credit_card_balance` refactored ===========
        cc = pd.read_csv(self.raw_dir / "data_files" / "credit_card_balance.csv")
        # Cat encode for aggregations
        org_cols = list(cc.columns)
        cc = pd.get_dummies(cc, columns=list(cc.select_dtypes(include=["object"]).columns), dummy_na=True)
        cc_cat_cols = [c for c in cc.columns if c not in org_cols]
        # General aggregations
        cc.drop(["SK_ID_PREV"], axis=1, inplace=True)
        cc_agg = cc.groupby("SK_ID_CURR").agg(["min", "max", "mean", "sum", "var"])
        cc_agg.columns = pd.Index(["CC_" + e[0] + "_" + e[1].upper() for e in cc_agg.columns.tolist()])
        # Count credit card lines
        cc_agg["CC_COUNT"] = cc.groupby("SK_ID_CURR").size()
        df = df.join(cc_agg, how="left", on="SK_ID_CURR")
        del cc, cc_agg, cc_cat_cols
        # =========== Feature selection ===========
        features_with_no_imp_at_least_twice = [
            "ACTIVE_CNT_CREDIT_PROLONG_SUM",
            "ACTIVE_CREDIT_DAY_OVERDUE_MEAN",
            "AMT_REQ_CREDIT_BUREAU_DAY",
            "AMT_REQ_CREDIT_BUREAU_HOUR",
            "AMT_REQ_CREDIT_BUREAU_WEEK",
            "BURO_CNT_CREDIT_PROLONG_SUM",
            "BURO_CREDIT_ACTIVE_Bad debt_MEAN",
            "BURO_CREDIT_ACTIVE_nan_MEAN",
            "BURO_CREDIT_CURRENCY_currency 1_MEAN",
            "BURO_CREDIT_CURRENCY_currency 2_MEAN",
            "BURO_CREDIT_CURRENCY_currency 3_MEAN",
            "BURO_CREDIT_CURRENCY_currency 4_MEAN",
            "BURO_CREDIT_CURRENCY_nan_MEAN",
            "BURO_CREDIT_DAY_OVERDUE_MAX",
            "BURO_CREDIT_DAY_OVERDUE_MEAN",
            "BURO_CREDIT_TYPE_Cash loan (non-earmarked)_MEAN",
            "BURO_CREDIT_TYPE_Interbank credit_MEAN",
            "BURO_CREDIT_TYPE_Loan for business development_MEAN",
            "BURO_CREDIT_TYPE_Loan for purchase of shares (margin lending)_MEAN",
            "BURO_CREDIT_TYPE_Loan for the purchase of equipment_MEAN",
            "BURO_CREDIT_TYPE_Loan for working capital replenishment_MEAN",
            "BURO_CREDIT_TYPE_Mobile operator loan_MEAN",
            "BURO_CREDIT_TYPE_Real estate loan_MEAN",
            "BURO_CREDIT_TYPE_Unknown type of loan_MEAN",
            "BURO_CREDIT_TYPE_nan_MEAN",
            "BURO_MONTHS_BALANCE_MAX_MAX",
            "BURO_STATUS_2_MEAN_MEAN",
            "BURO_STATUS_3_MEAN_MEAN",
            "BURO_STATUS_4_MEAN_MEAN",
            "BURO_STATUS_5_MEAN_MEAN",
            "BURO_STATUS_nan_MEAN_MEAN",
            "CC_AMT_DRAWINGS_ATM_CURRENT_MIN",
            "CC_AMT_DRAWINGS_CURRENT_MIN",
            "CC_AMT_DRAWINGS_OTHER_CURRENT_MAX",
            "CC_AMT_DRAWINGS_OTHER_CURRENT_MEAN",
            "CC_AMT_DRAWINGS_OTHER_CURRENT_MIN",
            "CC_AMT_DRAWINGS_OTHER_CURRENT_SUM",
            "CC_AMT_DRAWINGS_OTHER_CURRENT_VAR",
            "CC_AMT_INST_MIN_REGULARITY_MIN",
            "CC_AMT_PAYMENT_TOTAL_CURRENT_MIN",
            "CC_AMT_PAYMENT_TOTAL_CURRENT_VAR",
            "CC_AMT_RECIVABLE_SUM",
            "CC_AMT_TOTAL_RECEIVABLE_MAX",
            "CC_AMT_TOTAL_RECEIVABLE_MIN",
            "CC_AMT_TOTAL_RECEIVABLE_SUM",
            "CC_AMT_TOTAL_RECEIVABLE_VAR",
            "CC_CNT_DRAWINGS_ATM_CURRENT_MIN",
            "CC_CNT_DRAWINGS_CURRENT_MIN",
            "CC_CNT_DRAWINGS_OTHER_CURRENT_MAX",
            "CC_CNT_DRAWINGS_OTHER_CURRENT_MEAN",
            "CC_CNT_DRAWINGS_OTHER_CURRENT_MIN",
            "CC_CNT_DRAWINGS_OTHER_CURRENT_SUM",
            "CC_CNT_DRAWINGS_OTHER_CURRENT_VAR",
            "CC_CNT_DRAWINGS_POS_CURRENT_SUM",
            "CC_CNT_INSTALMENT_MATURE_CUM_MAX",
            "CC_CNT_INSTALMENT_MATURE_CUM_MIN",
            "CC_COUNT",
            "CC_MONTHS_BALANCE_MAX",
            "CC_MONTHS_BALANCE_MEAN",
            "CC_MONTHS_BALANCE_MIN",
            "CC_MONTHS_BALANCE_SUM",
            "CC_NAME_CONTRACT_STATUS_Active_MAX",
            "CC_NAME_CONTRACT_STATUS_Active_MIN",
            "CC_NAME_CONTRACT_STATUS_Approved_MAX",
            "CC_NAME_CONTRACT_STATUS_Approved_MEAN",
            "CC_NAME_CONTRACT_STATUS_Approved_MIN",
            "CC_NAME_CONTRACT_STATUS_Approved_SUM",
            "CC_NAME_CONTRACT_STATUS_Approved_VAR",
            "CC_NAME_CONTRACT_STATUS_Completed_MAX",
            "CC_NAME_CONTRACT_STATUS_Completed_MEAN",
            "CC_NAME_CONTRACT_STATUS_Completed_MIN",
            "CC_NAME_CONTRACT_STATUS_Completed_SUM",
            "CC_NAME_CONTRACT_STATUS_Completed_VAR",
            "CC_NAME_CONTRACT_STATUS_Demand_MAX",
            "CC_NAME_CONTRACT_STATUS_Demand_MEAN",
            "CC_NAME_CONTRACT_STATUS_Demand_MIN",
            "CC_NAME_CONTRACT_STATUS_Demand_SUM",
            "CC_NAME_CONTRACT_STATUS_Demand_VAR",
            "CC_NAME_CONTRACT_STATUS_Refused_MAX",
            "CC_NAME_CONTRACT_STATUS_Refused_MEAN",
            "CC_NAME_CONTRACT_STATUS_Refused_MIN",
            "CC_NAME_CONTRACT_STATUS_Refused_SUM",
            "CC_NAME_CONTRACT_STATUS_Refused_VAR",
            "CC_NAME_CONTRACT_STATUS_Sent proposal_MAX",
            "CC_NAME_CONTRACT_STATUS_Sent proposal_MEAN",
            "CC_NAME_CONTRACT_STATUS_Sent proposal_MIN",
            "CC_NAME_CONTRACT_STATUS_Sent proposal_SUM",
            "CC_NAME_CONTRACT_STATUS_Sent proposal_VAR",
            "CC_NAME_CONTRACT_STATUS_Signed_MAX",
            "CC_NAME_CONTRACT_STATUS_Signed_MEAN",
            "CC_NAME_CONTRACT_STATUS_Signed_MIN",
            "CC_NAME_CONTRACT_STATUS_Signed_SUM",
            "CC_NAME_CONTRACT_STATUS_Signed_VAR",
            "CC_NAME_CONTRACT_STATUS_nan_MAX",
            "CC_NAME_CONTRACT_STATUS_nan_MEAN",
            "CC_NAME_CONTRACT_STATUS_nan_MIN",
            "CC_NAME_CONTRACT_STATUS_nan_SUM",
            "CC_NAME_CONTRACT_STATUS_nan_VAR",
            "CC_SK_DPD_DEF_MAX",
            "CC_SK_DPD_DEF_MIN",
            "CC_SK_DPD_DEF_SUM",
            "CC_SK_DPD_DEF_VAR",
            "CC_SK_DPD_MAX",
            "CC_SK_DPD_MEAN",
            "CC_SK_DPD_MIN",
            "CC_SK_DPD_SUM",
            "CC_SK_DPD_VAR",
            "CLOSED_AMT_CREDIT_SUM_LIMIT_MEAN",
            "CLOSED_AMT_CREDIT_SUM_LIMIT_SUM",
            "CLOSED_AMT_CREDIT_SUM_OVERDUE_MEAN",
            "CLOSED_CNT_CREDIT_PROLONG_SUM",
            "CLOSED_CREDIT_DAY_OVERDUE_MAX",
            "CLOSED_CREDIT_DAY_OVERDUE_MEAN",
            "CLOSED_MONTHS_BALANCE_MAX_MAX",
            "CNT_CHILDREN",
            "ELEVATORS_MEDI",
            "ELEVATORS_MODE",
            "EMERGENCYSTATE_MODE_No",
            "EMERGENCYSTATE_MODE_Yes",
            "ENTRANCES_MODE",
            "FLAG_CONT_MOBILE",
            "FLAG_DOCUMENT_10",
            "FLAG_DOCUMENT_11",
            "FLAG_DOCUMENT_12",
            "FLAG_DOCUMENT_13",
            "FLAG_DOCUMENT_14",
            "FLAG_DOCUMENT_15",
            "FLAG_DOCUMENT_16",
            "FLAG_DOCUMENT_17",
            "FLAG_DOCUMENT_19",
            "FLAG_DOCUMENT_2",
            "FLAG_DOCUMENT_20",
            "FLAG_DOCUMENT_21",
            "FLAG_DOCUMENT_4",
            "FLAG_DOCUMENT_5",
            "FLAG_DOCUMENT_6",
            "FLAG_DOCUMENT_7",
            "FLAG_DOCUMENT_9",
            "FLAG_EMAIL",
            "FLAG_EMP_PHONE",
            "FLAG_MOBIL",
            "FLAG_OWN_CAR",
            "FLOORSMAX_MODE",
            "FONDKAPREMONT_MODE_not specified",
            "FONDKAPREMONT_MODE_org spec account",
            "FONDKAPREMONT_MODE_reg oper account",
            "FONDKAPREMONT_MODE_reg oper spec account",
            "HOUSETYPE_MODE_block of flats",
            "HOUSETYPE_MODE_specific housing",
            "HOUSETYPE_MODE_terraced house",
            "LIVE_REGION_NOT_WORK_REGION",
            "NAME_CONTRACT_TYPE_Revolving loans",
            "NAME_EDUCATION_TYPE_Academic degree",
            "NAME_FAMILY_STATUS_Civil marriage",
            "NAME_FAMILY_STATUS_Single / not married",
            "NAME_FAMILY_STATUS_Unknown",
            "NAME_FAMILY_STATUS_Widow",
            "NAME_HOUSING_TYPE_Co-op apartment",
            "NAME_HOUSING_TYPE_With parents",
            "NAME_INCOME_TYPE_Businessman",
            "NAME_INCOME_TYPE_Maternity leave",
            "NAME_INCOME_TYPE_Pensioner",
            "NAME_INCOME_TYPE_Student",
            "NAME_INCOME_TYPE_Unemployed",
            "NAME_TYPE_SUITE_Children",
            "NAME_TYPE_SUITE_Family",
            "NAME_TYPE_SUITE_Group of people",
            "NAME_TYPE_SUITE_Other_A",
            "NAME_TYPE_SUITE_Other_B",
            "NAME_TYPE_SUITE_Spouse, partner",
            "NAME_TYPE_SUITE_Unaccompanied",
            "NEW_RATIO_BURO_AMT_CREDIT_SUM_DEBT_MEAN",
            "NEW_RATIO_BURO_AMT_CREDIT_SUM_LIMIT_SUM",
            "NEW_RATIO_BURO_AMT_CREDIT_SUM_OVERDUE_MEAN",
            "NEW_RATIO_BURO_CNT_CREDIT_PROLONG_SUM",
            "NEW_RATIO_BURO_CREDIT_DAY_OVERDUE_MAX",
            "NEW_RATIO_BURO_CREDIT_DAY_OVERDUE_MEAN",
            "NEW_RATIO_BURO_MONTHS_BALANCE_MAX_MAX",
            "NEW_RATIO_PREV_AMT_DOWN_PAYMENT_MIN",
            "NEW_RATIO_PREV_RATE_DOWN_PAYMENT_MAX",
            "OCCUPATION_TYPE_Cleaning staff",
            "OCCUPATION_TYPE_Cooking staff",
            "OCCUPATION_TYPE_HR staff",
            "OCCUPATION_TYPE_IT staff",
            "OCCUPATION_TYPE_Low-skill Laborers",
            "OCCUPATION_TYPE_Managers",
            "OCCUPATION_TYPE_Private service staff",
            "OCCUPATION_TYPE_Realty agents",
            "OCCUPATION_TYPE_Sales staff",
            "OCCUPATION_TYPE_Secretaries",
            "OCCUPATION_TYPE_Security staff",
            "OCCUPATION_TYPE_Waiters/barmen staff",
            "ORGANIZATION_TYPE_Advertising",
            "ORGANIZATION_TYPE_Agriculture",
            "ORGANIZATION_TYPE_Business Entity Type 1",
            "ORGANIZATION_TYPE_Business Entity Type 2",
            "ORGANIZATION_TYPE_Cleaning",
            "ORGANIZATION_TYPE_Culture",
            "ORGANIZATION_TYPE_Electricity",
            "ORGANIZATION_TYPE_Emergency",
            "ORGANIZATION_TYPE_Government",
            "ORGANIZATION_TYPE_Hotel",
            "ORGANIZATION_TYPE_Housing",
            "ORGANIZATION_TYPE_Industry: type 1",
            "ORGANIZATION_TYPE_Industry: type 10",
            "ORGANIZATION_TYPE_Industry: type 11",
            "ORGANIZATION_TYPE_Industry: type 12",
            "ORGANIZATION_TYPE_Industry: type 13",
            "ORGANIZATION_TYPE_Industry: type 2",
            "ORGANIZATION_TYPE_Industry: type 3",
            "ORGANIZATION_TYPE_Industry: type 4",
            "ORGANIZATION_TYPE_Industry: type 5",
            "ORGANIZATION_TYPE_Industry: type 6",
            "ORGANIZATION_TYPE_Industry: type 7",
            "ORGANIZATION_TYPE_Industry: type 8",
            "ORGANIZATION_TYPE_Insurance",
            "ORGANIZATION_TYPE_Legal Services",
            "ORGANIZATION_TYPE_Mobile",
            "ORGANIZATION_TYPE_Other",
            "ORGANIZATION_TYPE_Postal",
            "ORGANIZATION_TYPE_Realtor",
            "ORGANIZATION_TYPE_Religion",
            "ORGANIZATION_TYPE_Restaurant",
            "ORGANIZATION_TYPE_Security",
            "ORGANIZATION_TYPE_Security Ministries",
            "ORGANIZATION_TYPE_Services",
            "ORGANIZATION_TYPE_Telecom",
            "ORGANIZATION_TYPE_Trade: type 1",
            "ORGANIZATION_TYPE_Trade: type 2",
            "ORGANIZATION_TYPE_Trade: type 3",
            "ORGANIZATION_TYPE_Trade: type 4",
            "ORGANIZATION_TYPE_Trade: type 5",
            "ORGANIZATION_TYPE_Trade: type 6",
            "ORGANIZATION_TYPE_Trade: type 7",
            "ORGANIZATION_TYPE_Transport: type 1",
            "ORGANIZATION_TYPE_Transport: type 2",
            "ORGANIZATION_TYPE_Transport: type 4",
            "ORGANIZATION_TYPE_University",
            "ORGANIZATION_TYPE_XNA",
            "POS_NAME_CONTRACT_STATUS_Amortized debt_MEAN",
            "POS_NAME_CONTRACT_STATUS_Approved_MEAN",
            "POS_NAME_CONTRACT_STATUS_Canceled_MEAN",
            "POS_NAME_CONTRACT_STATUS_Demand_MEAN",
            "POS_NAME_CONTRACT_STATUS_XNA_MEAN",
            "POS_NAME_CONTRACT_STATUS_nan_MEAN",
            "PREV_CHANNEL_TYPE_Car dealer_MEAN",
            "PREV_CHANNEL_TYPE_nan_MEAN",
            "PREV_CODE_REJECT_REASON_CLIENT_MEAN",
            "PREV_CODE_REJECT_REASON_SYSTEM_MEAN",
            "PREV_CODE_REJECT_REASON_VERIF_MEAN",
            "PREV_CODE_REJECT_REASON_XNA_MEAN",
            "PREV_CODE_REJECT_REASON_nan_MEAN",
            "PREV_FLAG_LAST_APPL_PER_CONTRACT_N_MEAN",
            "PREV_FLAG_LAST_APPL_PER_CONTRACT_Y_MEAN",
            "PREV_FLAG_LAST_APPL_PER_CONTRACT_nan_MEAN",
            "PREV_NAME_CASH_LOAN_PURPOSE_Building a house or an annex_MEAN",
            "PREV_NAME_CASH_LOAN_PURPOSE_Business development_MEAN",
            "PREV_NAME_CASH_LOAN_PURPOSE_Buying a garage_MEAN",
            "PREV_NAME_CASH_LOAN_PURPOSE_Buying a holiday home / land_MEAN",
            "PREV_NAME_CASH_LOAN_PURPOSE_Buying a home_MEAN",
            "PREV_NAME_CASH_LOAN_PURPOSE_Buying a new car_MEAN",
            "PREV_NAME_CASH_LOAN_PURPOSE_Buying a used car_MEAN",
            "PREV_NAME_CASH_LOAN_PURPOSE_Education_MEAN",
            "PREV_NAME_CASH_LOAN_PURPOSE_Everyday expenses_MEAN",
            "PREV_NAME_CASH_LOAN_PURPOSE_Furniture_MEAN",
            "PREV_NAME_CASH_LOAN_PURPOSE_Gasification / water supply_MEAN",
            "PREV_NAME_CASH_LOAN_PURPOSE_Hobby_MEAN",
            "PREV_NAME_CASH_LOAN_PURPOSE_Journey_MEAN",
            "PREV_NAME_CASH_LOAN_PURPOSE_Money for a third person_MEAN",
            "PREV_NAME_CASH_LOAN_PURPOSE_Other_MEAN",
            "PREV_NAME_CASH_LOAN_PURPOSE_Payments on other loans_MEAN",
            "PREV_NAME_CASH_LOAN_PURPOSE_Purchase of electronic equipment_MEAN",
            "PREV_NAME_CASH_LOAN_PURPOSE_Refusal to name the goal_MEAN",
            "PREV_NAME_CASH_LOAN_PURPOSE_Wedding / gift / holiday_MEAN",
            "PREV_NAME_CASH_LOAN_PURPOSE_XAP_MEAN",
            "PREV_NAME_CASH_LOAN_PURPOSE_nan_MEAN",
            "PREV_NAME_CLIENT_TYPE_XNA_MEAN",
            "PREV_NAME_CLIENT_TYPE_nan_MEAN",
            "PREV_NAME_CONTRACT_STATUS_Unused offer_MEAN",
            "PREV_NAME_CONTRACT_STATUS_nan_MEAN",
            "PREV_NAME_CONTRACT_TYPE_XNA_MEAN",
            "PREV_NAME_CONTRACT_TYPE_nan_MEAN",
            "PREV_NAME_GOODS_CATEGORY_Additional Service_MEAN",
            "PREV_NAME_GOODS_CATEGORY_Animals_MEAN",
            "PREV_NAME_GOODS_CATEGORY_Auto Accessories_MEAN",
            "PREV_NAME_GOODS_CATEGORY_Clothing and Accessories_MEAN",
            "PREV_NAME_GOODS_CATEGORY_Construction Materials_MEAN",
            "PREV_NAME_GOODS_CATEGORY_Direct Sales_MEAN",
            "PREV_NAME_GOODS_CATEGORY_Education_MEAN",
            "PREV_NAME_GOODS_CATEGORY_Fitness_MEAN",
            "PREV_NAME_GOODS_CATEGORY_Gardening_MEAN",
            "PREV_NAME_GOODS_CATEGORY_Homewares_MEAN",
            "PREV_NAME_GOODS_CATEGORY_House Construction_MEAN",
            "PREV_NAME_GOODS_CATEGORY_Insurance_MEAN",
            "PREV_NAME_GOODS_CATEGORY_Jewelry_MEAN",
            "PREV_NAME_GOODS_CATEGORY_Medical Supplies_MEAN",
            "PREV_NAME_GOODS_CATEGORY_Medicine_MEAN",
            "PREV_NAME_GOODS_CATEGORY_Office Appliances_MEAN",
            "PREV_NAME_GOODS_CATEGORY_Other_MEAN",
            "PREV_NAME_GOODS_CATEGORY_Tourism_MEAN",
            "PREV_NAME_GOODS_CATEGORY_Vehicles_MEAN",
            "PREV_NAME_GOODS_CATEGORY_Weapon_MEAN",
            "PREV_NAME_GOODS_CATEGORY_XNA_MEAN",
            "PREV_NAME_GOODS_CATEGORY_nan_MEAN",
            "PREV_NAME_PAYMENT_TYPE_Cashless from the account of the employer_MEAN",
            "PREV_NAME_PAYMENT_TYPE_Non-cash from your account_MEAN",
            "PREV_NAME_PAYMENT_TYPE_nan_MEAN",
            "PREV_NAME_PORTFOLIO_Cars_MEAN",
            "PREV_NAME_PORTFOLIO_nan_MEAN",
            "PREV_NAME_PRODUCT_TYPE_nan_MEAN",
            "PREV_NAME_SELLER_INDUSTRY_Construction_MEAN",
            "PREV_NAME_SELLER_INDUSTRY_Furniture_MEAN",
            "PREV_NAME_SELLER_INDUSTRY_Industry_MEAN",
            "PREV_NAME_SELLER_INDUSTRY_Jewelry_MEAN",
            "PREV_NAME_SELLER_INDUSTRY_MLM partners_MEAN",
            "PREV_NAME_SELLER_INDUSTRY_Tourism_MEAN",
            "PREV_NAME_SELLER_INDUSTRY_nan_MEAN",
            "PREV_NAME_TYPE_SUITE_Group of people_MEAN",
            "PREV_NAME_YIELD_GROUP_nan_MEAN",
            "PREV_PRODUCT_COMBINATION_POS industry without interest_MEAN",
            "PREV_PRODUCT_COMBINATION_POS mobile without interest_MEAN",
            "PREV_PRODUCT_COMBINATION_POS others without interest_MEAN",
            "PREV_PRODUCT_COMBINATION_nan_MEAN",
            "PREV_WEEKDAY_APPR_PROCESS_START_nan_MEAN",
            "REFUSED_AMT_DOWN_PAYMENT_MAX",
            "REFUSED_AMT_DOWN_PAYMENT_MEAN",
            "REFUSED_RATE_DOWN_PAYMENT_MIN",
            "REG_CITY_NOT_WORK_CITY",
            "REG_REGION_NOT_LIVE_REGION",
            "REG_REGION_NOT_WORK_REGION",
            "WALLSMATERIAL_MODE_Block",
            "WALLSMATERIAL_MODE_Mixed",
            "WALLSMATERIAL_MODE_Monolithic",
            "WALLSMATERIAL_MODE_Others",
            "WALLSMATERIAL_MODE_Panel",
            "WALLSMATERIAL_MODE_Wooden",
            "WEEKDAY_APPR_PROCESS_START_FRIDAY",
            "WEEKDAY_APPR_PROCESS_START_THURSDAY",
            "WEEKDAY_APPR_PROCESS_START_TUESDAY",
        ]
        # Filter to cols in our data w/o one hot of categories
        features_with_no_imp_at_least_twice = [f for f in features_with_no_imp_at_least_twice if f in df.columns]
        df = df.drop(columns=features_with_no_imp_at_least_twice)
        as_cat_dtype = [f for f in as_cat_dtype if f in df.columns]
        df = df.drop(columns=["SK_ID_CURR"])
        # Extra Preprocessing and cleaning from us
        df = df.drop(columns=["POS_COUNT"])  # Drop duplicated feature
        features_win_inf = [
            "PREV_APP_CREDIT_PERC_MAX",
            "PREV_APP_CREDIT_PERC_MEAN",
            "REFUSED_APP_CREDIT_PERC_MAX",
            "REFUSED_APP_CREDIT_PERC_MEAN",
            "NEW_RATIO_PREV_AMT_ANNUITY_MIN",
            "NEW_RATIO_PREV_AMT_ANNUITY_MAX",
            "NEW_RATIO_PREV_AMT_ANNUITY_MEAN",
            "NEW_RATIO_PREV_AMT_APPLICATION_MIN",
            "NEW_RATIO_PREV_AMT_APPLICATION_MAX",
            "NEW_RATIO_PREV_AMT_APPLICATION_MEAN",
            "NEW_RATIO_PREV_AMT_CREDIT_MIN",
            "NEW_RATIO_PREV_AMT_CREDIT_MAX",
            "NEW_RATIO_PREV_AMT_CREDIT_MEAN",
            "NEW_RATIO_PREV_APP_CREDIT_PERC_MIN",
            "NEW_RATIO_PREV_APP_CREDIT_PERC_MAX",
            "NEW_RATIO_PREV_APP_CREDIT_PERC_MEAN",
            "NEW_RATIO_PREV_APP_CREDIT_PERC_VAR",
            "NEW_RATIO_PREV_AMT_DOWN_PAYMENT_MAX",
            "NEW_RATIO_PREV_AMT_DOWN_PAYMENT_MEAN",
            "NEW_RATIO_PREV_AMT_GOODS_PRICE_MIN",
            "NEW_RATIO_PREV_AMT_GOODS_PRICE_MAX",
            "NEW_RATIO_PREV_AMT_GOODS_PRICE_MEAN",
            "NEW_RATIO_PREV_HOUR_APPR_PROCESS_START_MIN",
            "NEW_RATIO_PREV_HOUR_APPR_PROCESS_START_MAX",
            "NEW_RATIO_PREV_HOUR_APPR_PROCESS_START_MEAN",
            "NEW_RATIO_PREV_RATE_DOWN_PAYMENT_MIN",
            "NEW_RATIO_PREV_RATE_DOWN_PAYMENT_MEAN",
            "NEW_RATIO_PREV_CNT_PAYMENT_MEAN",
            "NEW_RATIO_PREV_CNT_PAYMENT_SUM",
            "INSTAL_PAYMENT_PERC_MAX",
            "INSTAL_PAYMENT_PERC_MEAN",
            "INSTAL_PAYMENT_PERC_SUM",
            "NEW_RATIO_BURO_DAYS_CREDIT_VAR",
            "NEW_RATIO_BURO_DAYS_CREDIT_ENDDATE_MIN",
            "NEW_RATIO_BURO_DAYS_CREDIT_ENDDATE_MAX",
            "NEW_RATIO_BURO_DAYS_CREDIT_ENDDATE_MEAN",
            "NEW_RATIO_BURO_DAYS_CREDIT_UPDATE_MEAN",
            "NEW_RATIO_BURO_AMT_CREDIT_MAX_OVERDUE_MEAN",
            "NEW_RATIO_BURO_AMT_CREDIT_SUM_MAX",
            "NEW_RATIO_BURO_AMT_CREDIT_SUM_MEAN",
            "NEW_RATIO_BURO_AMT_CREDIT_SUM_SUM",
            "NEW_RATIO_BURO_AMT_CREDIT_SUM_DEBT_MAX",
            "NEW_RATIO_BURO_AMT_CREDIT_SUM_DEBT_SUM",
            "NEW_RATIO_BURO_AMT_CREDIT_SUM_LIMIT_MEAN",
            "NEW_RATIO_BURO_AMT_ANNUITY_MAX",
            "NEW_RATIO_BURO_AMT_ANNUITY_MEAN",
            "NEW_RATIO_BURO_MONTHS_BALANCE_MIN_MIN",
            "NEW_RATIO_BURO_MONTHS_BALANCE_SIZE_SUM",
            "NEW_RATIO_BURO_DAYS_CREDIT_MAX",
            "NEW_PHONE_TO_EMPLOY_RATIO",
        ]
        for c in features_win_inf:
            df[c] = df[c].replace([np.inf, -np.inf], np.nan)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
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
                "FLAG_MOBIL",
                "FLAG_EMP_PHONE",
                "FLAG_WORK_PHONE",
                "FLAG_CONT_MOBILE",
                "FLAG_PHONE",
                "FLAG_EMAILREG_REGION_NOT_LIVE_REGION",
                "REG_REGION_NOT_WORK_REGION",
                "LIVE_REGION_NOT_WORK_REGION",
                "REG_CITY_NOT_LIVE_CITY",
                "REG_CITY_NOT_WORK_CITY",
                "LIVE_CITY_NOT_WORK_CITY",
                "ORGANIZATION_TYPE",
                "FONDKAPREMONT_MODE",
                "HOUSETYPE_MODE",
                "WALLSMATERIAL_MODE",
                "EMERGENCYSTATE_MODE",
                "FLAG_DOCUMENT_2",
                "FLAG_DOCUMENT_3",
                "FLAG_DOCUMENT_4",
                "FLAG_DOCUMENT_5",
                "FLAG_DOCUMENT_6",
                "FLAG_DOCUMENT_7",
                "FLAG_DOCUMENT_8",
                "FLAG_DOCUMENT_9",
                "FLAG_DOCUMENT_10",
                "FLAG_DOCUMENT_11",
                "FLAG_DOCUMENT_12",
                "FLAG_DOCUMENT_13",
                "FLAG_DOCUMENT_14",
                "FLAG_DOCUMENT_15",
                "FLAG_DOCUMENT_16",
                "FLAG_DOCUMENT_17",
                "FLAG_DOCUMENT_18",
                "FLAG_DOCUMENT_19",
                "FLAG_DOCUMENT_20",
                "FLAG_DOCUMENT_21",
            ],
        )
