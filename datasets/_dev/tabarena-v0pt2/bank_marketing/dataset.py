"""Curated dataset definition for `bank_marketing` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary


class BankMarketing(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a bank client subscribe to a term deposit after the bank's telemarketing calls?",
        use_case=(
            "A Portuguese bank's marketing team picks which clients to call in a term-deposit campaign, to spend its "
            "calls on the likely buyers (Moro et al. 2014)."
        ),
        row=(
            "One client contacted in a phone campaign of a Portuguese bank, May 2008 to November 2010 (45,211 clients)."
        ),
        predicted=("Whether the client subscribed to a term deposit by the end of the campaign's calls; 11.7% did."),
        known=(
            "Age, job, marital status, education, whether the client has defaulted on credit, the account balance, "
            "housing and personal loans, the phone type, the number of calls in this campaign, and the contacts with "
            "and outcome of earlier campaigns."
        ),
        split=("Random clients, so the test data stands for other clients of the same campaigns and years."),
        changes=(
            "We drop the duration of the last call, which the source says is unknown before the call and ends with "
            "the outcome, and the day and month of the last contact."
        ),
        fit="approximate",
        fit_reason=(
            "The calls span two and a half years, but the dates are dropped and the split is random, so the test "
            "clients do not stand for a later campaign. The number of calls in this campaign counts up to the last "
            "one, so it partly reflects how the campaign ended."
        ),
    )

    # Dataset
    unique_name = "bank_marketing"
    year = "2012"
    domain = "finance"
    source = "UCI"
    source_url = "https://archive.ics.uci.edu/dataset/222/bank+marketing"
    license = "CC BY 4.0"
    download_description = """
        We download the data from the UCI repository and uzip it to a predefined folder.

        mkdir -p local-data-warehouse/bank_marketing/ && wget -P local-data-warehouse/bank_marketing/ https://archive.ics.uci.edu/static/public/222/bank+marketing.zip && unzip -o "local-data-warehouse/bank_marketing/bank+marketing.zip" -d local-data-warehouse/bank_marketing && unzip -o "local-data-warehouse/bank_marketing/bank.zip" -d local-data-warehouse/bank_marketing
    """
    bibtex = r"""
        @article{moro2014bank-marketing,
          title={A data-driven approach to predict the success of bank telemarketing},
          author={Moro, S{\'e}rgio and Cortez, Paulo and Rita, Paulo},
          journal={Decision Support Systems},
          volume={62},
          pages={22--31},
          year={2014},
          publisher={Elsevier}
        }
    """
    curation_comments = """
        - We removed the "duration" feature following its original description to obtain a "realistic predictive model".
        - We further remove the "month" and "day_of_week" features, as they also relate to the last contact -- which is not available in a real-world scenario.
        - `campaign` and `previous` are counts of contacts (UCI: "number of contacts performed during this campaign",
          "... before this campaign"), so they stay numeric. The BeyondArena notebook typed them categorical (48 and
          41 levels), which lost the order and left the high counts as rare levels (issue #34).
    """

    # Task
    target = "SubscribeTermDeposit"
    problem_type = "binary_classification"
    metric = Metric.source(
        "roc_auc",
        original="AUC (area under the ROC curve), with ALIFT (area under the cumulative lift curve) as second metric",
        reference="Moro, Cortez, Rita 2014, A data-driven approach to predict the success of bank telemarketing, Decision Support Systems 62:22-31 (also Moro, Laureano, Cortez 2011, ESM, on the bank-full data)",
        definition="ROC AUC of term-deposit subscription.",
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        data = pd.read_csv(f"{raw_dir}/bank-full.csv", sep=";")
        return data

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        data = raw
        # Concatenate the two datasets
        feature_names = [
            "age",
            "job",
            "marital",
            "education",
            "default",
            "balance",
            "housing",
            "loan",
            "contact",
            "day",
            "month",
            "duration",
            "campaign",
            "pdays",
            "previous",
            "poutcome",
            "SubscribeTermDeposit",
        ]
        data.columns = feature_names
        df = data
        df = df.drop(columns=["day", "month", "duration"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "job",
                "marital",
                "education",
                "default",
                "housing",
                "loan",
                "contact",
                "poutcome",
            ],
        )
