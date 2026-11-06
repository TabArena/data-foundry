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
            "One client's record in one phone campaign of a Portuguese bank, May 2008 to November 2010; a client can "
            "recur across campaigns (45,211 records)."
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
        - We drop `day` (the day of the month; `day_of_week` is a column of the authors' 2014 release only) and `month` of the last contact: the campaign's end sets that date, since the calls stop at a subscription or when the bank stops calling (LEAK-10). The source keeps the month of each call as an input (Moro et al. 2014, Table 2, "month in which the call is made"); this file has only the last call's.
        - `campaign` and `previous` are counts of contacts (UCI: "number of contacts performed during this campaign",
          "... before this campaign"), so they stay numeric. The BeyondArena notebook typed them categorical (48 and
          41 levels), which lost the order and left the high counts as rare levels (issue #34).
        - Potential leak, kept on purpose (the LEAK-10 Cases row on spans the outcome sets, 2026-11-06): `campaign` counts this campaign's contacts including the last (UCI: "number of contacts performed during this campaign and for this client (numeric, includes last contact)"). The calls stop at a subscription or when the bank stops calling, so the outcome draws the end only for subscribers, who cannot be told apart without the label. Without it ROC AUC falls by 0.0060 (LightGBM, 9 splits x 5 seeds, lower in 9 of 9) and 0.0079 (logistic regression); given the year of the last contact (rebuilt from the file's date order, not shipped) it adds 0.0013 and 0.0016, about one seed SD of LightGBM. Most of its worth is the period's call intensity (3.2 calls per client at 5.1% subscribed in 2008, 1.9 at 51.6% in 2010). In 2008 the rate is flat over 1 to 10 calls (5.3% at 1 call, 5.3% at 6 to 10), but not in 2009 (19.0% at 1 call, 7.2% at 6 to 10) or in 2010 (51.9% to 39.2%). Revisit if the dates are restored or the split becomes temporal.
        - `contact` (cellular, telephone, unknown) belongs to the last contact in the codebook, but it is no span: its "unknown" covers all 12,443 rows of May-June 2008 (3.7% subscribed), so it marks the period (the authors' 2014 release codes these rows "telephone"). It is worth 0.021 ROC AUC in both models, nearly all of it the period: replaced by an unknown-or-not flag, it loses 0.0005 (LightGBM, 9 splits x 3 seeds), although the raw rates of cellular and telephone differ within a period (2009: 17.4% against 13.6%; 2010: 57.1% against 45.5%). Kept, with "unknown" as a level.
        - `pdays` (days since the client was last contacted in an earlier campaign): the data lean to counting to this campaign's start, not its end, but do not settle it. At a fixed date of the last contact it falls by 2.2 days per extra call, and by 1.0 with `previous` and `poutcome` also held fixed, so about half of the slope is who gets called more. It is worth 0.0048 ROC AUC with LightGBM and nothing with logistic regression (9 splits); kept. Its -1 means "client was not previously contacted" (UCI) and matches `previous` == 0 row for row (36,954 rows), so it stays as the source's code (CLEAN-10), and the bundle's sentinel warning is accepted for it.
        - Note: `balance` is the "average yearly balance, in euros" (UCI); the source does not say which year. 995 pairs of rows in two different years share the profile and the balance to the euro, mostly one client seen twice (the later row has more earlier contacts in 95%), and in 71% of them the age moves by one year while the balance stays: it may be one reading of unknown date. A subscription could move money, but nothing shows the reading falls after the calls, so it stays, as the registry fields of tunisian_fraud_detection_challenge did (LEAK-10, 2026-11-05). Revisit if the source dates it.
        - `job`'s "unknown" (288 rows) is missing, as `education`'s (1,857 rows): the authors' 2014 codebook says "There are several missing values in some categorical attributes, all coded with the 'unknown' label" (CLEAN-10; ROC AUC unchanged on 9 of 9 splits). `contact`'s "unknown" stays a level, as it marks the period (above).
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
    accepted_check_warnings = {
        "dataset_missing_value_sentinel": "pdays = -1 is the source's code for 'client was not previously contacted' "
        "(UCI codebook), not a missing value: it matches previous == 0 row for row (36,954 rows), so it stays as a "
        "code with a meaning (CLEAN-10).",
    }

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
        # "unknown" codes a missing value (the authors' 2014 codebook; CLEAN-10, CLEAN-14). `contact`'s
        # "unknown" stays a level: it marks May-June 2008 (curation notes).
        df = set_missing(
            df,
            {
                "job": ["unknown"],
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
