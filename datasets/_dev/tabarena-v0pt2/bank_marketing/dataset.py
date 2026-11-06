"""Curated dataset definition for `bank_marketing` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary, set_missing

# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "education": ["primary", "secondary", "tertiary"],
}


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
            "one, so it partly reflects how the campaign ended (kept, worth 0.006 ROC AUC, about 0.0015 of it once "
            "the period is known)."
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
        - Potential leak, kept on purpose (the LEAK-10 Cases row on spans the outcome sets, 2026-11-06): `campaign` counts this campaign's contacts including the last (UCI: "number of contacts performed during this campaign and for this client (numeric, includes last contact)"). The calls stop at a subscription or when the bank stops calling, so the outcome draws the end only for subscribers, who cannot be told apart without the label. Without it ROC AUC falls by 0.0060 (LightGBM, 9 splits x 5 seeds, lower in 9 of 9) and 0.0079 (logistic regression); given the year of the last contact (rebuilt from the file's date order, not shipped) it adds 0.0013 and 0.0016, about one seed SD of LightGBM. Most of its worth is the period's call intensity (3.2 calls per client at 5.1% subscribed in 2008, 1.9 at 51.6% in 2010), and in 2008 the rate is flat over 1 to 10 calls. Revisit if the dates are restored or the split becomes temporal.
        - `contact` (cellular, telephone, unknown) belongs to the last contact in the codebook, but it is no span: its "unknown" covers all 12,443 rows of May-June 2008 (3.7% subscribed), so it marks the period, and within a period cellular and telephone barely differ. It is worth 0.021 ROC AUC in both models; kept. `pdays` counts to this campaign's start, not its end (at a fixed last-contact date it falls by 2.2 days per extra call); kept.
        - Ordinal scales (2026-10-30, the curator's marks of 2026-10-31 and 2026-11-01, CLEAN-14): 1 column is ordered
          categories in the order of the source's codebook (`ORDINAL_LEVELS`); codes that mean unknown are missing
          (CLEAN-10).
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
        # codes outside a scale that mean unknown, and states outside it placed as missing (CLEAN-10,
        # CLEAN-14): don't know, refused, not asked, other
        df = set_missing(
            df,
            {
                "education": ["unknown"],
            },
        )
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal=ORDINAL_LEVELS,
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
