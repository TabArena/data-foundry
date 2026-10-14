"""Curated dataset definition for `dataorg_financial_health_prediction_challenge` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, TaskSummary, drop_columns, object_columns

TARGET = "financial_health"

ANSWER_SPELLINGS = {
    "Don’t know": "Don't know",
    "Don’t know or N/A": "Don't know",
    "Don’t know (Do not show)": "Don't know",
    "Don't Know": "Don't know",
    "Don?t know / doesn?t apply": "Don't know",
    " Do not know / N\u200e/A": "Don't know",
    "Used to have but don’t have now": "Used to have but don't have now",
}
"""Spellings of one answer that differ by country (curly apostrophes, a lost apostrophe, a stray space and a
left-to-right mark); each column has one spelling per country."""

FORMAL_ANSWERS = {
    "loan account: Have now": ("has_loan_account", "Have now"),
    "debit card: Have now": ("has_debit_card", "Have now"),
    "internet banking: Have now": ("has_internet_banking", "Have now"),
    "motor vehicle insurance: Have now": ("motor_vehicle_insurance", "Have now"),
    "income tax compliance: Yes": ("compliance_income_tax", "Yes"),
    "friends and family: Have now": ("uses_friends_family_savings", "Have now"),
}
"""The answers compared across countries for the Lesotho decision (the last one is informal, for contrast)."""

INSURANCE = ["has_insurance", "funeral_insurance", "medical_insurance", "motor_vehicle_insurance"]
CREDIT = ["has_credit_card", "has_loan_account"]
"""The answers that act as inputs of the index (curation comments, "Potential leak, kept on purpose")."""


class DataorgFinancialHealthPredictionChallenge(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Is a small business's financial health low, medium or high?",
        use_case=(
            "An institution, such as a lender, assesses a small business from what its owner reports in one "
            "interview, the prediction point the definition sets for data.org's Zindi competition (2025)."
        ),
        row=(
            "One small or micro business in Eswatini (2023), Malawi (2019) or Zimbabwe (2022), from FinMark Trust's "
            "FinScope surveys of business owners (7,674 businesses)."
        ),
        predicted=(
            "The class of the business's Financial Health Index at the interview: Low (66.54%), Medium (27.42%) or "
            "High (6.05%)."
        ),
        known=(
            "The country, the owner's age and sex, the business's age, turnover and expenses, the owner's income "
            "(local currency), and answers on finance held (accounts, cards, loans, mobile money, insurance), record "
            "keeping, tax, problems, risks and attitudes."
        ),
        split=(
            "Random businesses, as in the competition, so the test data stands for other businesses of the same "
            "surveys."
        ),
        changes=(
            "We drop Lesotho's 1,944 businesses, whose label runs against the index's own parts and against the other"
            " countries."
        ),
        fit="approximate",
        fit_reason=(
            "The index comes from an unpublished formula over survey answers, among them the insurance and credit "
            "products that are features, so the task partly recovers that formula (a small tree on those columns: log"
            " loss 0.285; all columns: 0.260). The countries asked different questions, so some columns are missing "
            "for whole countries."
        ),
    )

    # Dataset
    unique_name = "dataorg_financial_health_prediction_challenge"
    year = "2025"
    domain = "finance"
    source = "Zindi"
    source_url = "https://zindi.africa/competitions/dataorg-financial-health-prediction-challenge"
    license = "CC BY-SA 4.0"
    download_description = """
        Train.csv of the Zindi competition "data.org Financial Health Prediction Challenge" (2025). Zindi needs a login,
        so we take a Kaggle copy by muhammadbehroz (version 1, 2026-01-08) of the competition's zip: Train.csv, Test.csv,
        SampleSubmission.csv, VariableDefinitions.csv, the starter notebook and Zindi's manifest of the zip (generated
        2025-12-04). The files have the byte sizes the Zindi API lists for the competition
        (api.zindi.africa/v1/competitions/dataorg-financial-health-prediction-challenge, field `datafiles`); Train.csv:
        2,126,637 bytes, sha256 7e3ea585a86dbdd022b0c8c50263b1984ad9f6830466320b23f4038a6cb248d5, 9,618 rows and a
        header. Three other uploads hold the same Train.csv (Kaggle amishamanga/zindi-financial-health-data-prediction-challenge
        and robertoulisesquiroz/dataorg-financial-health-prediction-challenge2025; GitHub
        sylvan42/dataorg-financial-health-prediction-challenge20251204-19827-m2tn1n, 2025-12-20). Only Train.csv is
        read (Test.csv has no labels); VariableDefinitions.csv documents the columns.

        mkdir -p local-data-warehouse/dataorg_financial_health_prediction_challenge
        uvx --from kaggle==2.2.2 kaggle datasets download muhammadbehroz/dataorg-financial-health-prediction-challenge/1 -p local-data-warehouse/dataorg_financial_health_prediction_challenge
        unzip local-data-warehouse/dataorg_financial_health_prediction_challenge/dataorg-financial-health-prediction-challenge.zip Train.csv VariableDefinitions.csv -d local-data-warehouse/dataorg_financial_health_prediction_challenge
        rm local-data-warehouse/dataorg_financial_health_prediction_challenge/dataorg-financial-health-prediction-challenge.zip
    """
    bibtex = r"""
        @misc{zindi2025dataorgfinancialhealth,
          author = {{Zindi} and {data.org} and {FinMark Trust}},
          title = {data.org Financial Health Prediction Challenge},
          year = {2025},
          howpublished = {\url{https://zindi.africa/competitions/dataorg-financial-health-prediction-challenge}},
          note = {Zindi competition, 12 December 2025 to 15 March 2026. Data from FinMark Trust's FinScope MSME surveys of Eswatini (2023), Lesotho (2023), Malawi (2019) and Zimbabwe (2022)}
        }
    """
    curation_comments = """
        We start with Train.csv of the Zindi competition "data.org Financial Health Prediction Challenge" (2025): 9,618 small businesses in Eswatini, Lesotho, Malawi and Zimbabwe from FinMark Trust's FinScope MSME surveys, with 37 survey answers and the class of the business's Financial Health Index (FHI): Low, Medium or High.

        - Prediction point: an institution, such as a lender, assesses a small business from what its owner reports in one interview. The index describes the business at the same interview, so no column is recorded after the label.
        - Target: `Target` renamed to `financial_health`. The competition scored weighted F1 (Zindi discussion 29971); we keep the default metric, log loss.
        - We drop Lesotho's 1,944 rows: its label runs against the index's own dimensions and the other three countries, a recording problem we cannot repair. In Lesotho every formal-finance answer goes with a lower class, elsewhere with a higher one (decision table). LightGBM trained on two of the other countries ranks the third at ROC AUC 0.63 to 0.68 and Lesotho at 0.46, and swapping Low and Medium does not repair it (0.54). Revisit if data.org or FinMark Trust explain how Lesotho's FHI was computed.
        - Potential leak, kept on purpose: the FHI is computed from survey answers, among them the insurance and credit products that are columns here; none of the 1,896 businesses with an insurance product is Low. A depth-6 tree on country and the 11 product columns reaches log loss 0.285 against 0.260 for untuned LightGBM on all columns (class shares 0.796) and is worse on all 9 splits. We keep the columns: a business reports them at the assessment, the competition predicts the FHI from all columns, and the formula is not published. Revisit if data.org or FinMark Trust publish it.
        - Anomaly: the competition merged surveys with different questionnaires, and we keep the answers as released. Columns a country did not ask are missing for all its rows, and Malawi asked the three insurance products of only 147 of its businesses, 91% of them Medium or High against 14% of the others.
        - We unify the seven spellings of "Don't know" and the two of "Used to have but don't have now" (`ANSWER_SPELLINGS`). Each column has one spelling per country, and country is a column, so no information is lost.
        - current_problem_cash_flow: Eswatini's "0" becomes "No", as Malawi writes it; Zimbabwe's missing values stay missing.
        - Malawi records the age of a business under a year in months, with the years missing; we set those 225 businesses' years to 0, as Eswatini and Zimbabwe record such a business.
        - The amounts stay in local currency, since country is a column.
        - We drop ID, a random id per row.
        - IID split, as in the competition (its test set is a random 20% of every country). Each survey is one cross-section, and a business appears once.
        - dtypes: country and the 31 answer columns are categorical; owner_age, the three amounts and the age of the business (years, months) are numeric.
    """

    # Task
    target = TARGET
    problem_type = "multiclass_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "Train.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = drop_columns(raw.rename(columns={"Target": TARGET}), ["ID"])  # ID: a random "ID_" + 6 characters

        # Lesotho's label runs against formal finance and income, unlike the other countries (curation comments)
        df = df[df["country"] != "lesotho"]

        # One answer, one spelling (the spellings differ by country)
        answers = [c for c in object_columns(df) if c not in ("country", TARGET)]
        df[answers] = df[answers].replace(ANSWER_SPELLINGS)
        # Eswatini answers "Yes" / "0"; Malawi "Yes" / "No"; Zimbabwe "Yes" / missing
        df["current_problem_cash_flow"] = df["current_problem_cash_flow"].replace({"0": "No"})

        # Malawi gives months instead of years for a business under a year
        under_a_year = (df["country"] == "malawi") & df["business_age_years"].isna() & df["business_age_months"].notna()
        df.loc[under_a_year, "business_age_years"] = 0
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # every text column (also once cast, as the README's summary reads the final frame)
        return FeatureTypes(
            categorical=[c for c in df.columns if c != TARGET and not pd.api.types.is_numeric_dtype(df[c])]
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        # 1. Lesotho: formal-finance answers go with a lower class, in the other countries with a higher one
        up = raw["Target"].ne("Low")
        rows = []
        for name, (col, value) in FORMAL_ANSWERS.items():
            row = {"answer": name}
            for country in ["eswatini", "malawi", "zimbabwe", "lesotho"]:
                asked = raw["country"].eq(country) & raw[col].notna()
                given = asked & raw[col].eq(value)
                if given.any() and (asked & ~given).any():
                    row[country] = f"{up[given].mean():.2f} vs {up[asked & ~given].mean():.2f} (n = {int(given.sum())})"
                else:
                    row[country] = "not asked"
            rows.append(row)
        direction = pd.DataFrame(rows).set_index("answer")

        # 2. The products a business holds largely set its class
        held = lambda col: df[col].eq("Have now") | df[col].eq("Yes")  # has_insurance answers Yes / No
        insured = np.where(pd.concat([held(c) for c in INSURANCE], axis=1).any(axis=1), "yes", "no")
        credit = sum(held(c).astype(int) for c in CREDIT)
        lookup = pd.crosstab(
            [
                df["country"].rename("country"),
                pd.Series(insured, index=df.index, name="any insurance product"),
                credit.rename("formal credit products"),
            ],
            df[TARGET],
        )[["Low", "Medium", "High"]]

        return [
            Decision(
                "Lesotho dropped: its label runs against formal finance and income",
                "Share of Medium or High among the businesses that gave the answer against those that gave another "
                "answer to the same question (n: the businesses that gave it), from the raw file. In Eswatini, Malawi "
                "and Zimbabwe every formal-finance answer goes with a higher class; in Lesotho every one goes with a "
                "lower class, and the class falls with income, expenses and turnover (Spearman -0.12, -0.11, -0.11; "
                "+0.14 to +0.24 in the other countries). The informal friends-and-family answer goes with a higher "
                "class everywhere. The 1,944 Lesotho rows are dropped.",
                direction,
            ),
            Decision(
                "Product columns kept although the index is computed from such answers",
                "Class counts by country, any insurance product and the number of formal credit products (credit "
                "card, loan account). On the shipped splits a depth-6 tree on country and the 11 product columns "
                "reaches log loss 0.285 against 0.260 for untuned LightGBM on all columns (class shares 0.796) and is "
                "worse on all 9 splits; within identical product answers the most frequent class covers 93.8% of the "
                "rows. The formula is not published, and the competition predicts the index from all columns.",
                lookup,
            ),
        ]
