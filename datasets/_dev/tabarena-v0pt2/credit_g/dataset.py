"""Curated dataset definition for `credit_g` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class CreditG(AbstractCuratedDataset):
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
        category_mappings = {
            "checking_status": {
                "A11": "<0 DM",
                "A12": "0 <= ... < 200 DM",
                "A13": ">= 200 DM / salary assignments for >= 1 year",
                "A14": "no checking account",
            },
            "credit_history": {
                "A30": "no credits taken / all paid duly",
                "A31": "all credits at this bank paid duly",
                "A32": "existing credits paid duly till now",
                "A33": "delay in paying off in past",
                "A34": "critical account / other credits existing",
            },
            "credit_purpose": {
                "A40": "car (new)",
                "A41": "car (used)",
                "A42": "furniture/equipment",
                "A43": "radio/television",
                "A44": "domestic appliances",
                "A45": "repairs",
                "A46": "education",
                "A47": "vacation",
                "A48": "retraining",
                "A49": "business",
                "A410": "others",
            },
            "savings_status": {
                "A61": "< 100 DM",
                "A62": "100 <= ... < 500 DM",
                "A63": "500 <= ... < 1000 DM",
                "A64": ">= 1000 DM",
                "A65": "unknown / no savings",
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
                "A92": "female: divorced/separated/married",
                "A93": "male: single",
                "A94": "male: married/widowed",
                "A95": "female: single",
            },
            "other_debtors": {"A101": "none", "A102": "co-applicant", "A103": "guarantor"},
            "property": {
                "A121": "real estate",
                "A122": "building society savings / life insurance",
                "A123": "car or other (not savings)",
                "A124": "unknown / no property",
            },
            "other_installment_plans": {"A141": "bank", "A142": "stores", "A143": "none"},
            "housing": {"A151": "rent", "A152": "own", "A153": "for free"},
            "job": {
                "A171": "unemployed / unskilled non-resident",
                "A172": "unskilled resident",
                "A173": "skilled employee / official",
                "A174": "management / self-employed / highly qualified",
            },
            "telephone": {"A191": "none", "A192": "yes, registered"},
            "foreign_worker": {"A201": "yes", "A202": "no"},
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
