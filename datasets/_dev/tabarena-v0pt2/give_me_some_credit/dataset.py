"""Curated dataset definition for `give_me_some_credit` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Metric, TaskSummary


class GiveMeSomeCredit(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a borrower fall 90 days or more behind on a payment within the next two years?",
        use_case=(
            "A bank, deciding whether to grant a loan and on what terms, estimates the probability that the borrower "
            "will be in financial distress within two years (the competition's framing)."
        ),
        row=(
            "One borrower (150,000 in the training file of Kaggle's Give Me Some Credit, 2011); lender, place and "
            "period not stated."
        ),
        predicted="Whether the borrower is 90 days or more past due within two years (6.68% are).",
        known=(
            "Age, monthly income, dependents, debt ratio, the used share of credit-card and personal credit limits, "
            "the numbers of open credit lines and real-estate loans, and how often the borrower was 30-59, 60-89 and "
            "90 or more days late before."
        ),
        split=("Random borrowers, so the test data stands for other borrowers of the same lender and period."),
        fit="direct",
        fit_reason=(
            "The features are a credit file at the scoring date and the outcome follows within two years, as when a "
            "lender scores an applicant. The test borrowers come from the same undated period, so the task does not "
            "measure change over time."
        ),
    )

    # Dataset
    unique_name = "give_me_some_credit"
    year = "2011"
    domain = "finance"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/competitions/GiveMeSomeCredit/overview"
    license = "Public"
    download_description = """
        We download the data from Kaggle and uzip it to a predefined folder.

        mkdir -p local-data-warehouse/give_me_some_credit/ && cd local-data-warehouse/give_me_some_credit && kaggle competitions download -c GiveMeSomeCredit && cd ../../ && unzip local-data-warehouse/give_me_some_credit/GiveMeSomeCredit.zip -d local-data-warehouse/give_me_some_credit/ && rm local-data-warehouse/give_me_some_credit/GiveMeSomeCredit.zip
    """
    bibtex = """
        @misc{cukierski2011credit,
            author = {Credit Fusion and Will Cukierski},
            title = {Give Me Some Credit},
            year = {2011},
            howpublished = {url{https://kaggle.com/competitions/GiveMeSomeCredit}},
            note = {Kaggle}
        }
    """
    curation_comments = """
        - We renamed the target feature and its value to be more descriptive.
    """

    # Task
    target = "FinancialDistressNextTwoYears"
    problem_type = "binary_classification"
    metric = Metric.source(
        "roc_auc",
        original="AUC",
        reference="https://www.kaggle.com/competitions/GiveMeSomeCredit/overview/evaluation",
        definition="ROC AUC of the probability of 90+ days delinquency within two years.",
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/cs-training.csv", index_col=0, na_values="NA")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        target_feature = "FinancialDistressNextTwoYears"
        df = df.rename(columns={"SeriousDlqin2yrs": target_feature})
        df[target_feature] = df[target_feature].map({1: "Yes", 0: "No"})
        return df
