"""Curated dataset definition for `heloc` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, Source, TaskSummary, decode, set_missing

# The ordinal scales, lowest level first, from the FICO data dictionary (curation notes; the README lists them):
# the worst delinquency, from a derogatory comment to current and never delinquent.
ORDINAL_LEVELS = {
    "MaxDelq2PublicRecLast12M": [
        "derogatory comment",
        "120+ days delinquent",
        "90 days delinquent",
        "60 days delinquent",
        "30 days delinquent",
        "current and never delinquent",
    ],
    "MaxDelqEver": [
        "derogatory comment",
        "120+ days delinquent",
        "90 days delinquent",
        "60 days delinquent",
        "30 days delinquent",
        "current and never delinquent",
    ],
}


# The codebook's words for coded columns, decoded in `_clean` after the codes that mean unknown are missing
# (CLEAN-12; the curator's rule of 2026-11-01).
CODE_LABELS = {
    "MaxDelq2PublicRecLast12M": {
        "0": "derogatory comment",
        "1": "120+ days delinquent",
        "2": "90 days delinquent",
        "3": "60 days delinquent",
        "4": "30 days delinquent",
        "7": "current and never delinquent",
    },
    "MaxDelqEver": {
        "2": "derogatory comment",
        "3": "120+ days delinquent",
        "4": "90 days delinquent",
        "5": "60 days delinquent",
        "6": "30 days delinquent",
        "8": "current and never delinquent",
    },
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
    domain = "finance"
    sources = (
        Source(
            role="publication",
            platform="Other",  # FICO's Explainable Machine Learning Challenge (heloc_dataset_v1); the Kaggle file is a copy
            url="https://community.fico.com/s/explainable-machine-learning-challenge",
            license="Public",
            year="2018",
            bibtex=r"""
                @misc{averkiyoliabev2021heloc,
                  author       = {Kaggle User Averkiyoliabev},
                  title        = {Home Equity Line of Credit (HELOC)},
                  year         = {2021},
                  howpublished = {\url{https://www.kaggle.com/datasets/averkiyoliabev/home-equity-line-of-creditheloc}},
                  note         = {Kaggle dataset},
                }
            """,
        ),
        Source(
            role="copy",
            platform="Kaggle",
            url="https://www.kaggle.com/datasets/averkiyoliabev/home-equity-line-of-creditheloc",
            license=None,  # Kaggle says "Unknown"
            name="the Kaggle copy we download",
        ),
    )
    data_tags = ("ForcedIIDFromTemporal",)
    download_description = """
        We download the data from Kaggle and uzip it to a predefined folder.

        mkdir -p local-data-warehouse/heloc/ && cd local-data-warehouse/heloc && kaggle datasets download averkiyoliabev/home-equity-line-of-creditheloc && cd ../../ && unzip local-data-warehouse/heloc/home-equity-line-of-creditheloc.zip -d local-data-warehouse/heloc/ && rm local-data-warehouse/heloc/home-equity-line-of-creditheloc.zip
    """
    curation_comments = """
        - Label: "Bad" means the applicant was 90 days past due or worse at least once in the 24 months after the account was opened; "Good" means never more than 90 days overdue (FICO's challenge description, as reproduced in the AIX360 HELOC tutorial; FICO's challenge page now redirects).
        - The applicants requested a credit line of $5,000 to $150,000 (same source).
        - Anomaly: the dataset has time-related features. However, the task and features are preprocessed to be time-invariant.
        - Ordinal scales (2026-10-30, the curator's marks of 2026-10-31 and 2026-11-01, CLEAN-14): 2 columns are ordered
          categories in the order of the source's codebook (`ORDINAL_LEVELS`); 2 of them decoded from the source's codes
          into its words (`CODE_LABELS`, 2026-11-01)`MaxDelq2PublicRecLast12M` and `MaxDelqEver` are ordered categories,
          from a derogatory comment to current and never delinquent (FICO data dictionary); their codes for unknown
          delinquency, "all other" and no bureau record (-9) are missing.
        - Codes decoded (2026-11-01, CLEAN-12, CLEAN-14; the curator's rule: a code whose codebook says in words what
          each level is carries the words, a score without them is a number): 2 ordered codes carry their codebook's
          words (`CODE_LABELS`), in the same order.
        - Time basis: ForcedIIDFromTemporal: HELOC applications of an unnamed lender over a period FICO does not state,
          each account followed for 24 months; the release keeps no date and its order is the assembly of a balanced
          sample (training on the first 80% of the file scores the last 20% at ROC AUC 0.819 against 0.794 to 0.815 on
          random splits), so random applications stand in for the applications to come. A dated release would allow a
          split by application date.
    """
    accepted_check_warnings = {
        "meta_license_unknown": ("The Kaggle copy we download gives its licence as 'Unknown' (checked 2026-11-10)."),
    }

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
        df = set_missing(raw, {"MaxDelq2PublicRecLast12M": [5, 6, 9, -9], "MaxDelqEver": [7, -9]})
        # the codebook's words for its codes (CLEAN-12)
        df = decode(df, CODE_LABELS)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(ordinal=ORDINAL_LEVELS)
