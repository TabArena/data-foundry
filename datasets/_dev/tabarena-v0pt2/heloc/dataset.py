"""Curated dataset definition for `heloc` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary, set_missing

# The ordinal scales, lowest level first, from the FICO data dictionary (curation notes; the README lists them):
# the worst delinquency, from a derogatory comment to current and never delinquent.
ORDINAL_LEVELS = {
    "MaxDelq2PublicRecLast12M": [0, 1, 2, 3, 4, 7],
    "MaxDelqEver": [2, 3, 4, 5, 6, 8],
}


class Heloc(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Will an applicant for a home equity line of credit fall seriously behind on payments within two years?"
        ),
        use_case=(
            "A lender, when an application for a home equity line of credit arrives, decides from the applicant's "
            "credit report whether to approve it (FICO's Explainable Machine Learning Challenge)."
        ),
        row=(
            "One anonymised application for a credit line of $5,000 to $150,000 secured by the applicant's home, from"
            " FICO's 2018 challenge (10,459 applications; lender, place and period not stated)."
        ),
        predicted=(
            "Whether the borrower was 90 days or more past due at least once in the 24 months after the account "
            'opened ("Bad", 52%).'
        ),
        known=(
            "23 summaries of the credit report: an external risk estimate, the age of the credit history, numbers of "
            "accounts and of delinquent ones, recent delinquencies, recent credit inquiries and the debt burden; "
            "negative codes mark a missing report or a condition not met."
        ),
        split="Random applications.",
        fit="direct",
        fit_reason=(
            "Everything comes from the credit report at the application, and the outcome covers the first two years "
            "of the account. The rows are opened accounts, as in any credit scoring data."
        ),
    )

    # Dataset
    unique_name = "heloc"
    year = "2018"
    domain = "finance"
    source = "Other"  # FICO's Explainable Machine Learning Challenge (heloc_dataset_v1); the Kaggle file is a copy
    source_url = "https://community.fico.com/s/explainable-machine-learning-challenge"
    license = "Public"
    download_description = """
        We download the data from Kaggle and uzip it to a predefined folder.

        mkdir -p local-data-warehouse/heloc/ && cd local-data-warehouse/heloc && kaggle datasets download averkiyoliabev/home-equity-line-of-creditheloc && cd ../../ && unzip local-data-warehouse/heloc/home-equity-line-of-creditheloc.zip -d local-data-warehouse/heloc/ && rm local-data-warehouse/heloc/home-equity-line-of-creditheloc.zip
    """
    bibtex = r"""
        @misc{averkiyoliabev2021heloc,
          author       = {Kaggle User Averkiyoliabev},
          title        = {Home Equity Line of Credit (HELOC)},
          year         = {2021},
          howpublished = {\url{https://www.kaggle.com/datasets/averkiyoliabev/home-equity-line-of-creditheloc}},
          note         = {Kaggle dataset},
        }
    """
    curation_comments = """
        - Label: "Bad" means the applicant was 90 days past due or worse at least once in the 24 months after the account was opened; "Good" means never more than 90 days overdue (FICO's challenge description, as reproduced in the AIX360 HELOC tutorial; FICO's challenge page now redirects).
        - The applicants requested a credit line of $5,000 to $150,000 (same source).
        - Anomaly: the dataset has time-related features. However, the task and features are preprocessed to be time-invariant.
        - Ordinal scales (2026-10-30, the curator's marks of 2026-10-31, CLEAN-14): `MaxDelq2PublicRecLast12M` and
          `MaxDelqEver` are ordered categories, from a derogatory comment to current and never delinquent (FICO data
          dictionary); their codes for unknown delinquency, "all other" and no bureau record (-9) are missing.
    """

    # Task
    target = "RiskPerformance"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason="The challenge defined no predictive scoring rule: judging criteria were not announced in advance and mixed an empirical evaluation with qualitative judging of explanations; only accuracy figures (~72-74%) were reported for entries.",
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/heloc_dataset_v1 (1).csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # codes outside the delinquency scales (CLEAN-10, CLEAN-14): unknown delinquency, all other, no bureau record
        return set_missing(raw, {"MaxDelq2PublicRecLast12M": [5, 6, 9, -9], "MaxDelqEver": [7, -9]})

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(ordinal=ORDINAL_LEVELS)
