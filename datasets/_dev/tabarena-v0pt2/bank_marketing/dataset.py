"""Curated dataset definition for `bank_marketing` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Metric,
    Source,
    TaskSummary,
    Temporal,
    TemporalSplits,
    set_missing,
)

# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "education": ["primary", "secondary", "tertiary"],
}
# The file's month names, for the date of the last contact rebuilt in `_clean`.
MONTHS = ("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec")


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
            "Before the campaign's first call: age, job, marital status, education, whether the client has defaulted "
            "on credit, the account balance, housing and personal loans, the phone type, the contacts with and "
            "outcome of earlier campaigns, and the record's place in the file's date order."
        ),
        split=(
            "Five stretches of the file's date order, 4,521 records each from August 2008 to November 2010, each "
            "trained on every earlier record, so the test data stands for the clients the bank calls next."
        ),
        changes=(
            "We drop what the campaign's calls set: the duration of the last call (which the source says is unknown "
            "before the call), the number of calls in this campaign and the day and month of the last contact. We "
            "split by time on the file's date order instead of at random."
        ),
        fit="approximate",
        fit_reason=(
            "The windows follow the file's date order, as the source's own evaluation does, but count records, not "
            "campaigns: the file names no campaign and dates each record by its last call, so a window can start "
            "inside a campaign. In the newest window a recurring client's later record gives an earlier one's label "
            "away to a model that reads other test records, which the protocol forbids."
        ),
    )

    # Dataset
    unique_name = "bank_marketing"
    domain = "finance"
    sources = (
        Source(
            role="publication",
            platform="UCI",
            url="https://archive.ics.uci.edu/dataset/222/bank+marketing",
            license="CC BY 4.0",
            year="2012",
            bibtex=r"""
                @article{moro2014bank-marketing,
                  title={A data-driven approach to predict the success of bank telemarketing},
                  author={Moro, S{\'e}rgio and Cortez, Paulo and Rita, Paulo},
                  journal={Decision Support Systems},
                  volume={62},
                  pages={22--31},
                  year={2014},
                  publisher={Elsevier}
                }
            """,
        ),
    )
    download_description = """
        We download the data from the UCI repository and uzip it to a predefined folder.

        mkdir -p local-data-warehouse/bank_marketing/ && wget -P local-data-warehouse/bank_marketing/ https://archive.ics.uci.edu/static/public/222/bank+marketing.zip && unzip -o "local-data-warehouse/bank_marketing/bank+marketing.zip" -d local-data-warehouse/bank_marketing && unzip -o "local-data-warehouse/bank_marketing/bank.zip" -d local-data-warehouse/bank_marketing
    """
    curation_comments = """
        - Prediction point (USE-3; CC 2026-11-08, Lennart, Review issue 2): before the campaign's first call to the client, when the team picks whom to call. Known then: the client's profile and the earlier campaigns, nothing of this campaign's calls; so `duration`, `campaign`, `day` and `month` leave (below).
        - We removed the "duration" feature following its original description to obtain a "realistic predictive model".
        - The file has the day (`day`, the day of the month) and the month (`month`) of the last contact, but not the year. `_clean` rebuilds the year where the month wraps from December to January (2008: 27,729 records, 2009: 14,862, 2010: 2,620), checks that the dates never fall in the file's order (UCI: "ordered by date"; May 2008 to November 2010, with no record in September 2008), keeps the file position as the time key `time_index` (SPLIT-22), and drops `day` and `month` (`day_of_week` is a column of the authors' 2014 release only): the campaign's end sets the last contact's date, since the calls stop at a subscription or when the bank stops calling (LEAK-10). The source keeps the month of each call as an input (Moro et al. 2014, Table 2, "month in which the call is made"); this file has only the last call's, and whether it comes back is Review issue 4.
        - Split by time (CC 2026-11-08, Lennart, Review issue 1; SPLIT-1, SPLIT-19, SPLIT-22, LEAK-17), in place of the random split shipped until 2026-11-08; `splits_comment` gives the windows. Clients recur across campaigns: 995 pairs of records in two different years share the profile and the balance to the euro, the later record has more earlier contacts in 95% of them, and where the earlier record subscribed, the later one's `poutcome` says "success" in 562 of 581 pairs. Under the random split about 3.7% of the test records had the same client's later record in training (a lookup of it: +0.020 ROC AUC to LightGBM, higher on 9 of 9 splits), and models learnt each period's rate (5.1% subscribed in 2008, 17.1% in 2009, 51.6% in 2010) from records of the same months: most of that split's 0.76 ROC AUC came from telling the periods apart. Under the windows a client's earlier records train as its history (LEAK-34), and its later ones never do. On the five windows, newest first, LightGBM scores ROC AUC 0.570, 0.679, 0.605, 0.552 and 0.522 (mean 0.586; 3 seeds, early stopping on the newest tenth of the training side, seed SD 0.029 per window) and logistic regression 0.633, 0.701, 0.640, 0.603 and 0.490 (mean 0.614). The time key as an input is worth +0.018 to LightGBM (lower without it in 3 of 5 windows) and +0.004 to logistic regression.
        - Protocol (LEAK-9, an evaluation leak): in the newest window (August 2009 to November 2010) 703 test records (15.6%) have a later record of the same client in the same window, and its `poutcome` gives the label away: 419 say "success", all of them subscribers (19.7% of the window's positives; 7 to 18 records in each older window). Each test record is predicted from the training records and its own inputs only; no feature or model step may use other test records.
        - `campaign` is dropped (LEAK-10; CC 2026-11-08, Lennart, Review issue 2, in place of the keep with a note of 2026-11-06): it counts this campaign's contacts including the last (UCI: "number of contacts performed during this campaign and for this client (numeric, includes last contact)"), none of which exists at the prediction point, and the calls stop at a subscription or when the bank stops calling. It is the shape of heart_failure_followup_survival's `time`, a span from the prediction point to the outcome or a criterion without it. Under the random split it was worth 0.0060 ROC AUC to LightGBM (9 splits x 5 seeds, lower without it in 9 of 9) and 0.0079 to logistic regression, 0.0013 and 0.0016 once the year was known; on the five windows it adds +0.0065 to logistic regression (higher in 5 of 5) and -0.014 to LightGBM (higher in 1 of 5).
        - `previous` is a count of contacts (UCI: "number of contacts performed before this campaign and for this client"), so it stays numeric. The BeyondArena notebook typed it and `campaign` categorical (41 and 48 levels), which lost the order and left the high counts as rare levels (issue #34).
        - `contact` (cellular, telephone, unknown) belongs to the last contact in the codebook, but it is no span: its "unknown" covers all 12,443 rows of May-June 2008 (3.7% subscribed), so it marks the period (the authors' 2014 release codes these rows "telephone"). Under the random split it was worth 0.021 ROC AUC in both models, nearly all of it the period: replaced by an unknown-or-not flag, it lost 0.0005 (LightGBM, 9 splits x 3 seeds), although the raw rates of cellular and telephone differ within a period (2009: 17.4% against 13.6%; 2010: 57.1% against 45.5%). On the five windows, where the period it marks lies wholly in training, dropping it lowers LightGBM by 0.006 (lower in 3 of 5) and raises logistic regression by 0.014 (higher in 4 of 5). Kept, with "unknown" as a level.
        - `pdays` (days since the client was last contacted in an earlier campaign): the data lean to counting to this campaign's start, not its end, but do not settle it. At a fixed date of the last contact it falls by 2.2 days per extra call, and by 1.0 with `previous` and `poutcome` also held fixed, so about half of the slope is who gets called more. It was worth 0.0048 ROC AUC with LightGBM and nothing with logistic regression on the random split (9 splits), and 0.002 with both on the five windows; kept. Its -1 means "client was not previously contacted" (UCI) and matches `previous` == 0 row for row (36,954 rows), so it stays as the source's code (CLEAN-10), and the bundle's sentinel warning is accepted for it.
        - Note: `balance` is the "average yearly balance, in euros" (UCI); the source does not say which year. 995 pairs of rows in two different years share the profile and the balance to the euro, mostly one client seen twice (the later row has more earlier contacts in 95%), and in 71% of them the age moves by one year while the balance stays: it may be one reading of unknown date. A subscription could move money, but nothing shows the reading falls after the calls, so it stays, as the registry fields of tunisian_fraud_detection_challenge did (LEAK-10, 2026-11-05). Revisit if the source dates it.
        - `job`'s "unknown" (288 rows) is missing, as `education`'s (1,857 rows): the authors' 2014 codebook says "There are several missing values in some categorical attributes, all coded with the 'unknown' label" (CLEAN-10; ROC AUC unchanged on 9 of 9 random splits). `contact`'s "unknown" stays a level, as it marks the period (above).
        - Duplicates (LEAK-16, LEAK-18): on the twelve inputs without the time key, 811 records (1.8%) copy another, label included, and 82 more copy another's inputs with the other label (274 and 32 while `campaign` was an input); 89% of the copy rows have a balance of 0, plausible repeats of common profiles, so they stay. The time key makes every record distinct, so the bundle check counts none. On the five windows 0.8% to 4.3% of the test records (the oldest window the most) have a copy of every input but the time key in training, 0.6% to 4.0% with the same label: an earlier record, the client's history when it is one client (LEAK-34). Kept with this note (CC 2026-11-08, Lennart; Review issue 3).
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
    temporal = Temporal(
        on="time_index",
        splits=TemporalSplits(window=None, unit="rows", n_windows=5, min_train_fraction=0.5),
        horizon=4521,
        horizon_unit="steps",
    )
    splits_comment = """
        Five expanding windows on the file's date order (UCI: "ordered by date"), newest first: the newest half of the
        45,211 records cut into five stretches of 4,521, each trained on every earlier record (90%, 80%, 70%, 60% and
        50% of the records; SPLIT-14). By the date of the last contact, rebuilt in `_clean` and not shipped, the test
        windows run from 2009-08-07 to 2010-11-17 (2,129 subscribers, 47.1%), 2009-05-11 to 2009-08-07 (727, 16.1%),
        2009-04-06 to 2009-05-11 (593, 13.1%), 2008-11-21 to 2009-04-06 (473, 10.5%) and 2008-08-22 to 2008-11-21
        (279, 6.2%). The time key `time_index` is the record's position in the file. Each cut falls inside a day, whose
        earlier records in the file train (8 to 295 records); the order inside a day carries no signal (the position
        in the day alone: ROC AUC 0.501 over the days with 20 records or more). The source scores its model on
        time-ordered windows too: a random split does "not reflect the temporal dimension that a real prediction
        system would have to follow" (Moro et al. 2014, p. 5). The windows count records, not campaigns, as the file
        names no campaign. No gap (SPLIT-10): a record is dated by its last call, which ends the client's calls in that
        campaign, so its outcome is known by the date that orders it. Each test record is predicted from the training
        records and its own inputs only; no feature or model step may use other test records (curation notes,
        Protocol).
    """

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
        # The file is "ordered by date" (UCI), May 2008 to November 2010, and has no year: it steps up where the
        # month of the last contact wraps from December to January. Check that the rebuilt dates never fall in the
        # file order, then keep the file position as the time key (SPLIT-22); the date itself leaves (curation notes).
        month = df["month"].map({name: number for number, name in enumerate(MONTHS, start=1)})
        step = month.diff().fillna(0)
        wraps = step.lt(-6)
        if int(step.lt(0).sum()) != int(wraps.sum()):
            raise ValueError("Expected the month to fall only where it wraps from December to January")
        date = pd.to_datetime(pd.DataFrame({"year": 2008 + wraps.cumsum(), "month": month, "day": df["day"]}))
        if not date.is_monotonic_increasing:
            raise ValueError("Expected the file in date order")
        if (date.iloc[0].strftime("%Y-%m"), date.iloc[-1].strftime("%Y-%m")) != ("2008-05", "2010-11"):
            raise ValueError("Expected the calls of May 2008 to November 2010")
        df["time_index"] = np.arange(len(df))
        df = df.drop(columns=["day", "month", "duration", "campaign"])
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
