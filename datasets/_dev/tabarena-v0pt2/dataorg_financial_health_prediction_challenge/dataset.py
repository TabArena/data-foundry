"""Curated dataset definition for `dataorg_financial_health_prediction_challenge` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    TaskSummary,
    drop_columns,
    object_columns,
)

TARGET = "financial_health"

ANSWER_SPELLINGS = {
    "Don’t know": "Don't know",
    "Don’t know or N/A": "Don't know",
    "Don't Know": "Don't know",
    "Don?t know / doesn?t apply": "Don't know",
    " Do not know / N\u200e/A": "Don't know",
}
"""Spellings of one answer that differ by country (curly apostrophes, a lost apostrophe, a stray space and a
left-to-right mark); each column has one spelling per country."""

PRODUCTS = [
    "has_insurance",
    "funeral_insurance",
    "medical_insurance",
    "motor_vehicle_insurance",
    "has_credit_card",
    "has_loan_account",
    "has_debit_card",
    "has_internet_banking",
    "has_mobile_money",
    "uses_friends_family_savings",
    "uses_informal_lender",
]
"""The financial products a business holds: inputs of the index's "access to credit and financial services"
dimension, dropped (curation comments, decision 2)."""

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
"""The product answers tabulated against the class in decision 2."""


class DataorgFinancialHealthPredictionChallenge(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Is a small business's financial health low, medium or high?",
        use_case=(
            "A development partner or government agency screens a small business from one interview with its owner, "
            "to find vulnerable businesses and target support (the use the competition page names besides lenders' "
            "credit risk)."
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
            "(local currency), and answers on record keeping, tax, problems, risks and attitudes."
        ),
        split=(
            "Random businesses, as in the competition, so the test data stands for other businesses of the same "
            "surveys, not a later survey or another country."
        ),
        changes=(
            "We drop Lesotho's 1,944 businesses, whose label runs against the index's own parts and against the other"
            " countries, and the 11 answers on financial products held, which are inputs of the index."
        ),
        fit="approximate",
        fit_reason=(
            "The competition introduced the index and did not publish its formula or who acts on its class; the "
            "screening use is the page's own. Without the product answers the task predicts the class from the "
            "business's profile, money and attitudes. The countries asked different questions, so some columns are "
            "missing for whole countries, and the test data comes from the same surveys."
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
        We start with Train.csv of the Zindi competition "data.org Financial Health Prediction Challenge" (2025): 9,618 small businesses in Eswatini, Lesotho, Malawi and Zimbabwe from FinMark Trust's FinScope MSME surveys, with the country, 36 survey answers and the class of the business's Financial Health Index (FHI): Low, Medium or High.

        - Prediction point: a development partner or government agency screens a small business from one interview with its owner, to target support (the competition page names this use and lenders' credit risk; no source shows a lender acting on the class). The index describes the business at the same interview, so no column is recorded after the label. The page says the challenge "introduces a data-driven Financial Health Index"; its formula and author are not published.
        - Target: `Target` renamed to `financial_health`.
        - Metric: the evaluation page does not say how F1 averages the three classes; participants who submitted single-class files found the leaderboard fits weighted F1, not macro or micro F1 (Zindi discussion 29971; not confirmed by the host).
        - We drop Lesotho's 1,944 rows: its label runs against the index's own dimensions and the other three countries, and its answers are damaged too (decision 1), a recording problem we cannot repair. In Lesotho every formal-finance answer goes with a lower class, elsewhere with a higher one. LightGBM trained on the other countries ranks Lesotho at ROC AUC 0.43 to 0.50, against 0.62 to 0.95 for the other countries, and swapping Low and Medium in Lesotho's labels does not repair it (ROC AUC 0.54). Revisit if data.org or FinMark Trust explain how Lesotho's FHI was computed.
        - We drop the 11 answers on financial products held (`PRODUCTS`: insurance, cards, loan and other accounts, mobile money, informal sources): the page names "access to credit and financial services" as one of the FHI's four dimensions, so these answers are parts of the target (LEAK-10), although the owner gives them at the interview. None of the 1,896 businesses with an insurance product is Low. With the same LightGBM, country and the 11 answers reach log loss 0.255 against 0.266 for all columns (better on 9 of 9 splits); the 26 remaining columns reach 0.694 (macro ROC AUC 0.756) against 0.796 for the class shares, better on 9 of 9. Dropping only the 8 formal products would leave 0.678; mobile money and the informal sources go too, as they likely feed the access or debt dimensions.
        - Anomaly: the competition merged surveys with different questionnaires, and we keep the answers as released. Columns a country did not ask are missing for all its rows. In Zimbabwe (motivation_make_more_money, current_problem_cash_flow) and Eswatini (problem_sourcing_money, marketing_word_of_mouth) the answer is "Yes" or missing, and missing means not ticked; we keep it missing, as the questionnaires are not at hand.
        - We unify the six spellings of "Don't know" (`ANSWER_SPELLINGS`). Each column has one spelling per country, and country is a column, so no information is lost.
        - current_problem_cash_flow: Eswatini's "0" becomes "No", as Malawi writes it; Zimbabwe's missing values stay missing.
        - Malawi records the age of a business under a year in months, with the years missing; we set those 225 businesses' years to 0, as Eswatini and Zimbabwe record such a business.
        - business_age_years and business_age_months become missing in the 6 rows where the business is older than its owner (for example an owner of 20 with a business of 25 years).
        - The amounts stay in local currency, since country is a column. Their period may differ by country too (personal income over turnover has a median of 0.06 in Zimbabwe against 0.33 elsewhere), which country also covers.
        - The page lists traded commodities, trade activity, firm size and location as inputs; Train.csv has none of them.
        - We drop ID, a random id per row.
        - IID split, as in the competition (its test set is a random 20% of every country). Each survey is one cross-section, and a business appears once. The score holds for the same surveys: untuned LightGBM trained on Malawi 2019 and Zimbabwe 2022 scores Eswatini 2023 at log loss 1.14, against 0.905 under the random split and 0.958 for Eswatini's own class shares. Three country-years are too few for a grouped or temporal split.
        - dtypes: country and the 19 answer columns are categorical; owner_age, the three amounts and the age of the business (years, months) are numeric.
    """

    # Task
    target = TARGET
    problem_type = "multiclass_classification"
    metric = Metric.source(
        "f1_weighted",
        original="F1 (Zindi API error_metric 'f1_multiclass')",
        reference=(
            "https://zindi.africa/competitions/dataorg-financial-health-prediction-challenge (Evaluation); "
            "api.zindi.world/v1/competitions/dataorg-financial-health-prediction-challenge error_metric=f1_multiclass "
            "(checked 2026-10-21); Zindi discussion 29971"
        ),
        definition="support-weighted mean of per-class F1 over Low / Medium / High",
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "Train.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = drop_columns(raw.rename(columns={"Target": TARGET}), ["ID"])  # ID: a random "ID_" + 6 characters
        # The products held are inputs of the index's access-to-finance dimension (curation comments, decision 2)
        df = drop_columns(df, PRODUCTS)

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

        # A business older than its owner is impossible: its age becomes missing
        older = df["business_age_years"] > df["owner_age"]
        df.loc[older, ["business_age_years", "business_age_months"]] = np.nan
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

        # 2. The products a business holds largely set its class (raw answers of the kept countries)
        kept = raw[raw["country"] != "lesotho"]
        held = lambda col: kept[col].eq("Have now") | kept[col].eq("Yes")  # has_insurance answers Yes / No
        insured = np.where(pd.concat([held(c) for c in INSURANCE], axis=1).any(axis=1), "yes", "no")
        credit = sum(held(c).astype(int) for c in CREDIT)
        lookup = pd.crosstab(
            [
                kept["country"].rename("country"),
                pd.Series(insured, index=kept.index, name="any insurance product"),
                credit.rename("formal credit products"),
            ],
            kept["Target"].rename(TARGET),
        )[["Low", "Medium", "High"]]

        return [
            Decision(
                "Lesotho dropped: its label runs against formal finance and income",
                "Share of Medium or High among the businesses that gave the answer against those that gave another "
                "answer to the same question (n: the businesses that gave it), from the raw file. In Eswatini, Malawi "
                "and Zimbabwe every formal-finance answer goes with a higher class; in Lesotho every one goes with a "
                "lower class, and the class falls with income, expenses and turnover (Spearman -0.12, -0.11, -0.11 "
                "without the 97/98/99 codes; -0.055, -0.073, -0.052 as released; +0.14 to +0.24 in the other "
                "countries). The informal friends-and-family answer goes with a higher class everywhere. The answers "
                "are damaged too: 12 columns are missing for every Lesotho business, among them three insurance "
                "columns, the credit card and record keeping, and 86% answer that they used to have an informal "
                "lender. The 1,944 Lesotho rows are dropped.",
                direction,
            ),
            Decision(
                "The 11 product columns dropped: inputs of the index",
                "Class counts by country, any insurance product and the number of formal credit products (credit "
                "card, loan account), from the raw answers of the three kept countries. The competition page names "
                "access to credit and financial services as one of the index's four dimensions. With the same "
                "LightGBM on the shipped splits, country and the 11 product columns reach log loss 0.255 against "
                "0.266 for all columns, better on 9 of 9; within identical product answers the most frequent class "
                "covers 93.8% of the rows. The 26 remaining columns reach 0.694 against 0.796 for the class shares.",
                lookup,
            ),
        ]
