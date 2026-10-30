"""Curated dataset definition for `credit_g` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary

# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "employment_since": [
        "unemployed",
        "< 1 year",
        "1 <= ... < 4 years",
        "4 <= ... < 7 years",
        ">= 7 years",
    ],  # open-ended
    "job": [
        "unemployed / unskilled non-resident",
        "unskilled resident",
        "skilled employee / official",
        "management / self-employed / highly qualified",
    ],
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
        - Labels follow the corrected code table (Groemping 2019, "South German Credit Data: Correcting a Widely Used
          Data Set", UCI 573), not Statlog's german.doc, which is wrong for checking_status, credit_history,
          credit_purpose, savings_status, personal_status_sex, property, housing and foreign_worker. The codes keep
          their order: matched on duration, amount and age (990 of 1,000 rows unique in both files), A11 is code 1,
          A12 code 2 and so on in every column, with foreign_worker reversed (A201 is "no"). The numeric codes mean:
          installment_rate_percent 1 = >= 35%, 2 = 25-35%, 3 = 20-25%, 4 = < 20% of disposable income (a higher code
          is a lower rate); residence_since 1 = < 1 year to 4 = >= 7 years; existing_credits_count 1 = 1, 2 = 2-3,
          3 = 4-5, 4 = >= 6; people_liable 1 = 0 to 2, 2 = 3 or more. UCI 573 also corrects a few values (34 rows of
          other_installment_plans, 10 of foreign_worker, 1 of housing); this definition keeps Statlog's values
          (2026-10-30).
        - Metric: the Statlog cost matrix on probabilities, each applicant predicted as the class of least expected cost (the AI's choice; the curator was unsure and noted TabArena's threshold tuning, 2026-10-21).
        - Ordinal scales (2026-10-30, CLEAN-14): 2 columns typed as ordered categories in the order of the source's
          codebook (`ORDINAL_LEVELS`).
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
        category_mappings = {
            # the labels of the corrected code table (Groemping 2019, UCI 573 South German Credit); the Statlog
            # german.doc table is wrong for these columns (curation notes)
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
                "A92": "female: non-single, or male: single",
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
            "telephone": {"A191": "none", "A192": "yes, registered"},
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
