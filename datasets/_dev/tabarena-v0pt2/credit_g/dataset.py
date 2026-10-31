"""Curated dataset definition for `credit_g` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary, set_missing

# The corrected code table of UCI 573 (codetable.txt): code -> label per column
CODES = {
    "checking_status": {
        1: "no checking account",
        2: "< 0 DM",
        3: "0 <= ... < 200 DM",
        4: ">= 200 DM / salary for at least 1 year",
    },
    "credit_history": {
        0: "delay in paying off in the past",
        1: "critical account / other credits elsewhere",
        2: "no credits taken / all credits paid back duly",
        3: "existing credits paid back duly till now",
        4: "all credits at this bank paid back duly",
    },
    "credit_purpose": {
        0: "others",
        1: "car (new)",
        2: "car (used)",
        3: "furniture/equipment",
        4: "radio/television",
        5: "domestic appliances",
        6: "repairs",
        7: "education",
        8: "vacation",
        9: "retraining",
        10: "business",
    },
    "savings_status": {
        1: "unknown / no savings account",
        2: "< 100 DM",
        3: "100 <= ... < 500 DM",
        4: "500 <= ... < 1000 DM",
        5: ">= 1000 DM",
    },
    "employment_since": {1: "unemployed", 2: "< 1 yr", 3: "1 <= ... < 4 yrs", 4: "4 <= ... < 7 yrs", 5: ">= 7 yrs"},
    "installment_rate_percent": {1: ">= 35", 2: "25 <= ... < 35", 3: "20 <= ... < 25", 4: "< 20"},
    "personal_status_sex": {
        1: "male: divorced/separated",
        2: "female: non-single or male: single",
        3: "male: married/widowed",
        4: "female: single",
    },
    "other_debtors": {1: "none", 2: "co-applicant", 3: "guarantor"},
    "residence_since": {1: "< 1 yr", 2: "1 <= ... < 4 yrs", 3: "4 <= ... < 7 yrs", 4: ">= 7 yrs"},
    "property": {
        1: "unknown / no property",
        2: "car or other",
        3: "building soc. savings agr./life insurance",
        4: "real estate",
    },
    "other_installment_plans": {1: "bank", 2: "stores", 3: "none"},
    "housing": {1: "for free", 2: "rent", 3: "own"},
    "existing_credits_count": {1: "1", 2: "2-3", 3: "4-5", 4: ">= 6"},
    "job": {
        1: "unemployed/unskilled - non-resident",
        2: "unskilled - resident",
        3: "skilled employee/official",
        4: "manager/self-empl./highly qualif. employee",
    },
    "people_liable": {1: "3 or more", 2: "0 to 2"},
    "telephone": {1: "no", 2: "yes (under customer name)"},
    "foreign_worker": {1: "yes", 2: "no"},
    "good_or_bad_customer": {0: "bad", 1: "good"},
}

# The ordinal scales, lowest level first (curation notes; the README lists them). An open-ended level holds everything
# beyond it. "no checking account", "unknown / no savings account" and "unknown / no property" are states outside the
# scales: missing, by the curator's rule (the data has no other missing value).
ORDINAL_LEVELS = {
    "checking_status": ["< 0 DM", "0 <= ... < 200 DM", ">= 200 DM / salary for at least 1 year"],  # open-ended
    "savings_status": ["< 100 DM", "100 <= ... < 500 DM", "500 <= ... < 1000 DM", ">= 1000 DM"],  # open-ended
    "employment_since": ["unemployed", "< 1 yr", "1 <= ... < 4 yrs", "4 <= ... < 7 yrs", ">= 7 yrs"],  # open-ended
    "installment_rate_percent": ["< 20", "20 <= ... < 25", "25 <= ... < 35", ">= 35"],  # open-ended
    "residence_since": ["< 1 yr", "1 <= ... < 4 yrs", "4 <= ... < 7 yrs", ">= 7 yrs"],  # open-ended
    "property": ["car or other", "building soc. savings agr./life insurance", "real estate"],
    "existing_credits_count": ["1", "2-3", "4-5", ">= 6"],  # open-ended
    "job": [
        "unemployed/unskilled - non-resident",
        "unskilled - resident",
        "skilled employee/official",
        "manager/self-empl./highly qualif. employee",
    ],
    "people_liable": ["0 to 2", "3 or more"],  # open-ended
}


class CreditG(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Is a loan applicant a good or a bad credit risk?",
        use_case=(
            "A bank, when a loan application arrives, decides whether to grant the credit; the source scores errors "
            "with a cost matrix that penalises accepting a bad customer most."
        ),
        row=(
            "One applicant of a German bank, with amounts in Deutsche Mark (1,000 applicants, released in 1994; the "
            "period of the loans is not stated)."
        ),
        predicted=(
            "Whether the customer was rated good or bad (30% bad); the source defines neither the rating nor when it "
            "was made."
        ),
        known=(
            "The application: checking and savings balances, loan duration, amount, purpose and instalment rate, "
            "credit history, other loans, employment, personal status and sex, age, housing, property, job, "
            "dependants, guarantors, telephone and whether a foreign worker."
        ),
        split="Random applicants of the same bank and period.",
        fit="approximate",
        fit_reason=(
            "The features are what a bank knows at the application, but the source gives no dates and no definition "
            "or horizon of a bad customer, so the random split stands in for scoring later applicants. The data are "
            "old."
        ),
    )

    # Dataset
    unique_name = "credit_g"
    year = "1994"
    domain = "finance"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5QG88"  # South German Credit (UPDATE): Statlog's data, corrected
    license = "CC BY 4.0"
    download_description = """
        We download the corrected data (UCI 573, South German Credit) from the UCI repository and unzip it to a
        predefined folder.

        mkdir -p local-data-warehouse/credit_g/ && wget -P local-data-warehouse/credit_g/ "https://archive.ics.uci.edu/static/public/573/south+german+credit+update.zip" && unzip -o "local-data-warehouse/credit_g/south+german+credit+update.zip" -d local-data-warehouse/credit_g/
    """
    bibtex = r"""
        @misc{uci2020southgermancredit,
          title        = {South German Credit [Dataset]},
          year         = {2020},
          howpublished = {\url{https://doi.org/10.24432/C5QG88}},
          note         = {UCI Machine Learning Repository; the corrected Statlog German credit data, see Groemping, U.
                          (2019), South German Credit Data: Correcting a Widely Used Data Set, Report 4/2019, Beuth
                          University of Applied Sciences Berlin},
        }
        @misc{hofmann1994statlog,
          author       = {Hofmann, H.},
          title        = {Statlog (German Credit Data) [Dataset]},
          year         = {1994},
          howpublished = {\url{https://doi.org/10.24432/C5NC77}},
          note         = {UCI Machine Learning Repository},
        }
    """
    curation_comments = """
        - We reversed the original ordinal encoding.
        - Source (2026-10-31, the curator's marks): UCI 573 South German Credit, the corrected version of Statlog's
          german.data (Groemping 2019, "South German Credit Data: Correcting a Widely Used Data Set"; the UCI page:
          Statlog "suffers from severe errors in the coding information"). The same 1,000 applicants and the same
          700 good and 300 bad: matched on duration, amount and age, Statlog's codes correspond one to one (A11 is
          code 1 and so on; foreign_worker reversed), but german.doc's labels are wrong for checking_status,
          credit_history, credit_purpose, savings_status, personal_status_sex, property, housing and foreign_worker,
          and UCI 573 corrects 57 coded values (12 of credit_purpose, 34 of other_installment_plans, 10 of
          foreign_worker, 1 of housing) and a typo in the amount or the age of 10 applicants. Every code is labelled
          by UCI 573's code table, the number-coded columns too: installment_rate_percent is the share of disposable
          income (">= 35" is code 1), residence_since and existing_credits_count are bands, people_liable is "0 to
          2" or "3 or more".
        - Metric: the Statlog cost matrix on probabilities, each applicant predicted as the class of least expected cost (the AI's choice; the curator was unsure and noted TabArena's threshold tuning, 2026-10-21).
        - Ordinal scales (2026-10-30, the curator's marks of 2026-10-31, CLEAN-14): 9 columns are ordered categories
          (`ORDINAL_LEVELS`): the balances, employment, instalment rate, residence, property, number of credits, job
          and people liable. "no checking account", "unknown / no savings account" and "unknown / no property" are
          states outside their scales: missing, by the curator's rule, as the data has no other missing value.
    """

    # Task
    target = "good_or_bad_customer"
    problem_type = "binary_classification"
    metric = Metric.source(
        "cost_matrix",
        original="Statlog German credit cost matrix (average misclassification cost)",
        reference=(
            "UCI Statlog (German Credit Data) page https://doi.org/10.24432/C5NC77 (german.doc); Michie, "
            "Spiegelhalter & Taylor 1994, Statlog book, Ch. 9 (German credit, average cost)"
        ),
        definition=(
            "mean cost per applicant: 5 for a bad customer predicted good, 1 for a good customer predicted bad; from "
            "probabilities, predicted bad when p(bad) > 1/6"
        ),
        params={"labels": ["good", "bad"], "matrix": [[0, 1], [5, 0]], "prediction": "proba"},
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "SouthGermanCredit.asc", sep=r"\s+")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        names = {
            "laufkont": "checking_status",
            "laufzeit": "duration_months",
            "moral": "credit_history",
            "verw": "credit_purpose",
            "hoehe": "credit_amount",
            "sparkont": "savings_status",
            "beszeit": "employment_since",
            "rate": "installment_rate_percent",
            "famges": "personal_status_sex",
            "buerge": "other_debtors",
            "wohnzeit": "residence_since",
            "verm": "property",
            "alter": "age_years",
            "weitkred": "other_installment_plans",
            "wohn": "housing",
            "bishkred": "existing_credits_count",
            "beruf": "job",
            "pers": "people_liable",
            "telef": "telephone",
            "gastarb": "foreign_worker",
            "kredit": "good_or_bad_customer",
        }
        df = raw.rename(columns=names)
        for col, labels in CODES.items():
            assert df[col].isin(labels).all(), col  # every code is in the code table
            df[col] = df[col].map(labels)
        # states outside the ordinal scales: missing, by the curator's rule (curation notes)
        return set_missing(
            df,
            {
                "checking_status": ["no checking account"],
                "savings_status": ["unknown / no savings account"],
                "property": ["unknown / no property"],
            },
        )

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal=ORDINAL_LEVELS,
            categorical=[
                "checking_status",
                "credit_history",
                "credit_purpose",
                "savings_status",
                "employment_since",
                "personal_status_sex",
                "other_debtors",
                "property",
                "other_installment_plans",
                "housing",
                "job",
                "telephone",
                "foreign_worker",
            ],
        )
