"""Curated dataset definition for `credit_g` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TaskSummary


class CreditG(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a loan applicant fail to repay the loan as agreed in the contract?",
        use_case=(
            "A bank, when a loan application arrives, scores the applicant to decide whether to grant the credit; the "
            "source scores errors with a cost matrix that penalises accepting a bad customer most."
        ),
        row=(
            "One loan granted in 1973 to 1975 by a large regional bank in southern Germany (1,000 loans, released in "
            "1994). A stratified sample: bad loans are oversampled from about 5% to 30%."
        ),
        predicted=(
            "Whether the customer did not comply with the loan contract as required (bad, 30%) or complied fully "
            "(good). The source states no horizon."
        ),
        known=(
            "The application: checking and savings balances, loan duration, amount (transformed by an unknown "
            "monotonic function), purpose and instalment rate, "
            "credit history, other loans, employment, personal status combined with sex, age, housing, property, "
            "job, dependants, guarantors, telephone and whether a foreign worker."
        ),
        split="Random loans of the same bank and period.",
        changes=(
            "We relabelled the categories with Grömping's (2019) corrected code table; the Statlog table mislabels "
            "8 of the 20 features."
        ),
        fit="approximate",
        fit_reason=(
            "The features are what a bank knows at the application, but the loans are undated and have no stated "
            "horizon, so the random split stands in for scoring later applicants. Only granted loans have an "
            "outcome, and the data are 50 years old."
        ),
    )

    # Dataset
    unique_name = "credit_g"
    year = "1994"
    domain = "finance"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5NC77"
    license = "CC BY 4.0"
    download_description = """
        We download the data from the UCI repository and unzip it to a predefined folder.

        mkdir -p local-data-warehouse/credit_g/ && wget -P local-data-warehouse/credit_g/ https://archive.ics.uci.edu/static/public/144/statlog+german+credit+data.zip && unzip local-data-warehouse/credit_g/statlog+german+credit+data.zip -d local-data-warehouse/credit_g/
    """
    bibtex = r"""
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
        - Anomaly: the original task used a cost matrix for evaluation.
        - The code table in the Statlog `german.doc` is wrong (Grömping 2019, "South German Credit Data: Correcting a
          Widely Used Data Set", Report 4/2019, Beuth University of Applied Sciences Berlin). Its levels are mixed up
          for checking_status, credit_history, credit_purpose, savings_status, personal_status_sex, property, housing
          and foreign_worker. We relabel these with Grömping's corrected table (the codetable.txt of UCI dataset 522): a
          Statlog code A<i><k> means level k of that table, except foreign_worker, whose two levels are swapped (as are
          those of people_liable, which stays an integer code). Check (2026-10-15): matched on duration, amount and age,
          990 of the 1,000 rows agree with South German Credit (`SouthGermanCredit.asc`, the Open Data LMU file) in
          every column except other_installment_plans (34 rows), housing (1) and foreign_worker (10), the differences
          Grömping reports; the other 10 rows differ in one amount or age each (731 vs 713, 50 vs 40).
        - Typos kept: Hofmann typed the Statlog rows by hand, and we leave the values that differ from South German
          Credit as Statlog has them. We treat them as a data-quality issue that real data has too, not as something to
          repair. Only one is shown to be a Statlog error: the loan of 48 months, amount 7582, age 31 is `A153` (own)
          in Statlog and rent in South German Credit, and Fahrmeir and Hamerle's (1984) Table 2.1 (Grömping 2019,
          Table 1) matches the latter (75.43% rent / 9.00% own among good loans; Statlog gives 75.29% / 9.14%). The
          table cannot decide the other_installment_plans and foreign_worker differences (both files give its shares),
          and it holds no amounts or ages.
        - personal_status_sex: level 2 holds both non-single females and single males, so sex cannot be derived.
        - installment_rate_percent, residence_since, existing_credits_count and people_liable are band codes, kept as
          the Statlog integers; they are not percentages, years or counts. The bands (Grömping's table):
          installment_rate_percent 1 = >= 35%, 2 = 25 to < 35%, 3 = 20 to < 25%, 4 = < 20% of disposable income;
          residence_since 1 = < 1 year, 2 = 1 to < 4, 3 = 4 to < 7, 4 = >= 7 years; existing_credits_count 1 = 1,
          2 = 2-3, 3 = 4-5, 4 = >= 6 credits at this bank; people_liable 1 = 0 to 2, 2 = 3 or more dependants.
        - The loans are from 1973 to 1975 (Häußler 1979; Fahrmeir and Hamerle 1984); Hofmann typed the 1,000 rows from
          the appendix of Fahrmeir and Hamerle (1984). Only granted loans are in the sample, bad loans are oversampled
          (about 5% in the bank's portfolio), and the credit amounts are an unknown monotonic transformation of the
          real amounts (Grömping 2019, Sec. 3).
    """

    # Task
    target = "good_or_bad_customer"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/german.data", header=None, sep=r"\s+")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        feature_names = {
            0: "checking_status",
            1: "duration_months",
            2: "credit_history",
            3: "credit_purpose",
            4: "credit_amount",
            5: "savings_status",
            6: "employment_since",
            7: "installment_rate_percent",
            8: "personal_status_sex",
            9: "other_debtors",
            10: "residence_since",
            11: "property",
            12: "age_years",
            13: "other_installment_plans",
            14: "housing",
            15: "existing_credits_count",
            16: "job",
            17: "people_liable",
            18: "telephone",
            19: "foreign_worker",
            20: "good_or_bad_customer",
        }
        # Grömping's (2019) corrected code table; the one in the Statlog german.doc is wrong (curation_comments).
        category_mappings = {
            "checking_status": {
                "A11": "no checking account",
                "A12": "< 0 DM",
                "A13": "0 <= ... < 200 DM",
                "A14": ">= 200 DM / salary for at least 1 year",
            },
            "credit_history": {
                "A30": "delay in paying off in the past",
                "A31": "critical account / other credits elsewhere",
                "A32": "no credits taken / all credits paid back duly",
                "A33": "existing credits paid back duly till now",
                "A34": "all credits at this bank paid back duly",
            },
            "credit_purpose": {
                "A40": "others",
                "A41": "car (new)",
                "A42": "car (used)",
                "A43": "furniture/equipment",
                "A44": "radio/television",
                "A45": "domestic appliances",
                "A46": "repairs",
                "A47": "education",
                "A48": "vacation",
                "A49": "retraining",
                "A410": "business",
            },
            "savings_status": {
                "A61": "unknown / no savings account",
                "A62": "< 100 DM",
                "A63": "100 <= ... < 500 DM",
                "A64": "500 <= ... < 1000 DM",
                "A65": ">= 1000 DM",
            },
            "employment_since": {
                "A71": "unemployed",
                "A72": "< 1 year",
                "A73": "1 <= ... < 4 years",
                "A74": "4 <= ... < 7 years",
                "A75": ">= 7 years",
            },
            "personal_status_sex": {
                "A91": "male: divorced/separated",
                "A92": "female: non-single or male: single",
                "A93": "male: married/widowed",
                "A94": "female: single",
            },
            "other_debtors": {"A101": "none", "A102": "co-applicant", "A103": "guarantor"},
            "property": {
                "A121": "unknown / no property",
                "A122": "car or other",
                "A123": "building society savings / life insurance",
                "A124": "real estate",
            },
            "other_installment_plans": {"A141": "bank", "A142": "stores", "A143": "none"},
            "housing": {"A151": "for free", "A152": "rent", "A153": "own"},
            "job": {
                "A171": "unemployed / unskilled non-resident",
                "A172": "unskilled resident",
                "A173": "skilled employee / official",
                "A174": "management / self-employed / highly qualified",
            },
            "telephone": {"A191": "no", "A192": "yes, under customer name"},
            "foreign_worker": {"A201": "no", "A202": "yes"},
            "good_or_bad_customer": {"1": "good", "2": "bad"},
        }
        df.columns = list(feature_names.values())
        for feature_idx in range(len(list(df))):
            fname = feature_names[feature_idx]
            if fname in category_mappings:
                mapping = category_mappings[fname]
                df[fname] = df[fname].apply(lambda x: mapping[str(x)])  # noqa: B023
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
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
