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
    Splits,
    TaskSummary,
    Temporal,
    set_missing,
)

# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "education": ["primary", "secondary", "tertiary"],
}
# The file's month names, for the date of the last contact rebuilt in `_clean`.
MONTHS = ("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec")
# The test windows, newest first: the date each starts on and the file position (`time_index`) of its first record.
# Four campaign periods (each from its burst's first day or the gap before it) and six calendar quarters of the
# trickle from June 2009; each runs to the next start (Andrej, 2026-11-20). `_clean` checks that each position is the first
# record of its date.
WINDOW_STARTS = (
    ("2010-09-01", 44_619),
    ("2010-06-01", 43_838),
    ("2010-03-01", 43_171),
    ("2009-12-02", 42_390),
    ("2009-09-01", 41_373),
    ("2009-06-01", 39_752),
    ("2009-05-04", 34_177),
    ("2009-04-16", 32_193),
    ("2009-01-28", 27_729),
    ("2008-10-17", 24_038),
)


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
            "on credit, the account balance, housing and personal loans, the contacts with and outcome of earlier "
            "campaigns, and the number of clients the bank calls that day."
        ),
        split=(
            "Ten periods of the date of the last contact from October 2008 to November 2010, each trained on every "
            "earlier record: the four calling campaigns after the summer 2008 wave, one window each, then six "
            "calendar quarters of the one-by-one calls from June 2009, so the test data stands for the clients the "
            "bank calls next."
        ),
        changes=(
            "We drop what the campaign's calls set: the last call's duration, this campaign's number of calls and "
            "the day, month and phone type of the last contact. We add the day's calling volume (records on the same date), which "
            "the subscription rate follows, and split by time on the rebuilt date instead of at random."
        ),
        fit="approximate",
        fit_reason=(
            "The windows cut at the calling campaigns the dates show, but the file names no campaign, so the calls "
            "from June 2009 are cut by calendar quarter; the day's call count, built from the file's own records, "
            "approximates the campaign's planned size. Inside a window a client's later record can give an earlier "
            "one's label away to a model that reads other test records, which the protocol forbids."
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
        - Prediction point (USE-3; CC 2026-11-08, Lennart): before the campaign's first call to the client, when the team picks whom to call. Known then: the client's profile and the earlier campaigns, nothing of this campaign's calls; so `duration`, `campaign`, `day`, `month` and `contact` leave (below).
        - We removed the "duration" feature following its original description to obtain a "realistic predictive model".
        - The file has the day (`day`, the day of the month) and the month (`month`) of the last contact, but not the year. `_clean` rebuilds the year where the month wraps from December to January (2008: 27,729 records, 2009: 14,862, 2010: 2,620), checks that the dates never fall in the file's order (UCI: "ordered by date"; May 2008 to November 2010, with no record in September 2008), keeps the file position as the time key `time_index` (SPLIT-22), counts the records of each date as `calls_that_day` (below), and drops `day` and `month` (`day_of_week` is a column of the authors' 2014 release only); the rebuilt date sets the test windows (`WINDOW_STARTS`, `splits_comment`) and is not shipped: the campaign's end sets the last contact's date, since the calls stop at a subscription or when the bank stops calling (LEAK-10). The source keeps the month of each call as an input (Moro et al. 2014, Table 2, "month in which the call is made"); this file has only the last call's, and it stays out with the day: every input exists before the first call, and the period is in the time key (Lennart, 2026-11-08).
        - Split by time (CC 2026-11-08, Lennart; SPLIT-1, SPLIT-19, SPLIT-22, LEAK-17), in place of the random split shipped until 2026-11-08; `splits_comment` gives the ten windows on the rebuilt date (Andrej, 2026-11-20), which replace five windows of 4,521 records on the file order. Clients recur across campaigns: 995 pairs of records in two different years share the profile and the balance to the euro, the later record has more earlier contacts in 95% of them, and where the earlier record subscribed, the later one's `poutcome` says "success" in 562 of 581 pairs. Under the random split about 3.7% of the test records had the same client's later record in training (a lookup of it: +0.020 ROC AUC to LightGBM, higher on 9 of 9 splits), and models learnt each period's rate (5.1% subscribed in 2008, 17.1% in 2009, 51.6% in 2010) from records of the same months: most of that split's 0.76 ROC AUC came from telling the periods apart. Under the windows a client's earlier records train as its history (LEAK-34), and its later ones never do. On the earlier five windows of 4,521 records (August 2008 to November 2010), newest first, LightGBM scores ROC AUC 0.570, 0.679, 0.605, 0.552 and 0.522 (mean 0.586; 3 seeds, early stopping on the newest tenth of the training side, seed SD 0.029 per window) and logistic regression 0.633, 0.701, 0.640, 0.603 and 0.490 (mean 0.614). The time key is no model input (`time_of="label"`, Andrej, 2026-11-21): it is the record's position in a file ordered by the date of the last contact, and 61.2% of the records (27,667) take more than one call, so that date falls after the prediction point and is set by when the calling stopped - at a subscription or when the bank gave up (the subscription rate falls from 14.6% at one call to 5.8% at six or more). It is the reason the rebuilt date is not shipped either. While it was an input it was worth +0.018 to LightGBM and +0.004 to logistic regression on the earlier five windows; the file position holds no finer information about the outcome than the date does - within a calling day (days with 20 or more calls, 42,187 records) the position does not rank the label (Spearman 0.0013; the subscription rate is 7.4% to 10.0% across the ten within-day deciles). Those five windows are the ones this definition shipped until 2026-11-20, not the ten it ships now; the window scores here and the measurements of `campaign`, `contact`, `pdays` and `balance` below were taken on them (those of `contact` also on the random split and on nine quarterly windows, as its note says) and are kept as measured, not re-run on the ten (Andrej, 2026-11-21).
        - Protocol (LEAK-9, an evaluation leak): inside a test window a client's later record can give an earlier test record's label away in its `poutcome`. Linked on the profile, housing and personal loan, the balance to the euro (non-zero), age +0 or +1 and the contacts adding up (a link that finds about 73% of repeat records), 3 to 18 test records per window have a later record of the same client in the same window (99 in all, 0.1% to 2.1% of a window; 5 of 592 in the newest), and in 40 of them it says "success", all of them subscribers (0 to 9 per window). Each test record is predicted from the training records and its own inputs only; no feature or model step may use other test records.
        - `campaign` is dropped (LEAK-10; CC 2026-11-08, Lennart, in place of the keep with a note of 2026-11-06): it counts this campaign's contacts including the last (UCI: "number of contacts performed during this campaign and for this client (numeric, includes last contact)"), none of which exists at the prediction point, and the calls stop at a subscription or when the bank stops calling. It is the shape of heart_failure_followup_survival's `time`, a span from the prediction point to the outcome or a criterion without it. Under the random split it was worth 0.0060 ROC AUC to LightGBM (9 splits x 5 seeds, lower without it in 9 of 9) and 0.0079 to logistic regression, 0.0013 and 0.0016 once the year was known; on the earlier five windows it adds +0.0065 to logistic regression (higher in 5 of 5) and -0.014 to LightGBM (higher in 1 of 5).
        - `previous` is a count of contacts (UCI: "number of contacts performed before this campaign and for this client"), so it stays numeric. The BeyondArena notebook typed it and `campaign` categorical (41 and 48 levels), which lost the order and left the high counts as rare levels.
        - `contact` (cellular, telephone, unknown) is dropped (Andrej, 2026-11-13) with the other fields of the last contact: the codebook lists it with day, month and duration as "related with the last contact of the current campaign". The phone type itself is probably known before the call (where two linked records of a client both record one, it is the same in 3,571 of 3,721) but tells little: in 2009 and 2010, 22.7% of the cellular contacts subscribed and 19.1% of the telephone ones. The column's weight is its "unknown" level, a recording state rather than a phone: it covers all 12,443 rows of May-June 2008 (3.7% subscribed; the authors' 2014 release codes these rows "telephone"), and in later periods its few contacts subscribe far from the cellular ones, above or below (37.8% against 5.8% in September to November 2008; 8.6% and 2.9% against 61.3% and 53.9% in June to August and September to November 2010). Under the random split it was worth 0.021 ROC AUC in both models, nearly all of it the period: replaced by an unknown-or-not flag, it lost 0.0005 (LightGBM, 9 splits x 3 seeds). On the earlier five windows, dropping it lowered LightGBM by 0.006 (lower in 3 of 5) and raised logistic regression by 0.014 (higher in 4 of 5). On nine quarterly windows of the rebuilt date (September 2008 to November 2010, untuned, 2026-11-12) LightGBM scored ROC AUC 0.614 without it and 0.610 with it, logistic regression 0.619 and 0.623: it gained 0.024 to 0.051 on the two windows of June to November 2010, where the unknowns subscribe at 3% to 9%, and lost 0.025 to 0.059 (LightGBM) on the three oldest, carrying 2008's low rate onto later unknowns. None of these was re-run on the ten windows shipped now.
        - `pdays` (days since the client was last contacted in an earlier campaign): the data lean to counting to this campaign's start, not its end, but do not settle it. At a fixed date of the last contact it falls by 2.2 days per extra call, and by 1.0 with `previous` and `poutcome` also held fixed, so about half of the slope is who gets called more. It was worth 0.0048 ROC AUC with LightGBM and nothing with logistic regression on the random split (9 splits), and 0.002 with both on the earlier five windows; kept. Its -1 means "client was not previously contacted" (UCI) and matches `previous` == 0 row for row (36,954 rows), so it stays as the source's code (CLEAN-10), and the bundle's sentinel warning is accepted for it.
        - Note: `balance` is the "average yearly balance, in euros" (UCI), one value per client: linked without it (profile, age +0/+1, contacts adding up), the same client's records share it to the euro in 17.1% of pairs against 1.2% for different clients, with no excess of slightly changed balances, while age moves. The source does not date it. A reading after the calls could carry a subscription, but on the five windows logistic regression loses 0.002 to 0.003 ROC AUC without it whether or not the client has a later record, so it stays (LEAK-10; as tunisian_fraud_detection_challenge's registry fields). These numbers were measured on the earlier five windows of 4,521 records, which the ten windows of 2026-11-20 replace, and are kept as measured (Andrej, 2026-11-21). Revisit if the source dates it.
        - `job`'s "unknown" (288 rows) is missing, as `education`'s (1,857 rows): the authors' 2014 codebook says "There are several missing values in some categorical attributes, all coded with the 'unknown' label" (CLEAN-10; ROC AUC unchanged on 9 of 9 random splits).
        - Duplicates (LEAK-16, LEAK-18): on the twelve inputs without the time key, 62 records (0.1%) copy another, label included, and 5 more copy another's inputs with the other label; 92% of the copy rows have a balance of 0, plausible repeats of common profiles called the same day, so they stay. While `contact` was an input (thirteen inputs, until 2026-11-23) the counts were 55 and 1; before `calls_that_day` was an input (twelve inputs, `contact` among them) 811 and 82 (274 and 32 while `campaign` was an input). Since 2026-11-21 the time key is no input, so these are the counts the bundle check sees (it counted none while the key was an input and made every record distinct). In the ten windows two test records have a copy of every input but the time key in training: one in the window from 2 Dec 2009, with the other label, and one in the window from 1 Sep 2009, with the same label; on the twelve inputs before `calls_that_day` it was 0.4% to 1.9% (0.1% to 1.7% with the same label): an earlier record, the client's history when it is one client (LEAK-34). Kept with this note (CC 2026-11-08, Lennart).
        - `calls_that_day` (Andrej, 2026-11-20): the number of records in the file with the same rebuilt date of the last contact, counted in `_clean` over the whole file (1 to 825; the definition filters no rows). The subscription rate follows the day's calling volume: 5.8% on the 95 days with 200 calls or more (36,656 records), 12.3% at 101-200, 25.0% at 51-100, 41.0% at 21-50 and 48.5% on days with 20 or fewer (3,224 records), and 44.2% there even for first-time clients (`previous` = 0), so returning clients do not explain it; UCI's second release (`bank-additional-full.csv`, with Banco de Portugal's indicators) shows the same rise, with the bank's monthly calls falling after 2008 and the share subscribing rising. The bank knows how many clients it calls that day when it draws the list, so it is known at the prediction point. Caveat: it is built from the file's own records, dated by each client's last call, so it approximates the campaign's planned size and the day's calls rather than recording them.
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
        "dataset_sequential_id_column": "`time_index` is the record's position in the file, which the source orders "
        'by the date of the last contact: it is the declared temporal order (`Temporal(on="time_index", '
        'time_of="label")`), it sets the test windows, and since 2026-11-21 it is no model input. It is kept in '
        "the frame because the split needs it and the file holds no date.",
    }
    # Splits: ten windows of unequal length from `WINDOW_STARTS` (`_make_splits`); declared windows have one length
    temporal = Temporal(
        on="time_index",
        horizon=3,
        horizon_unit="months",
        # The file position dates the last call, which ends the client's calls: it orders the split and is no input
        # (Andrej, 2026-11-21).
        time_of="label",
    )
    splits_comment = """
        Ten expanding windows on the date of the last contact, rebuilt in `_clean` (the year from where the months
        wrap) and not shipped, newest first; each test window runs from its start to the next one and trains on every
        earlier record, no gap (Andrej, 2026-11-20):

        | Test window | Kind | Train share | Test records | Subscribers |
        |---|---|---|---|---|
        | 1 Sep-17 Nov 2010 | trickle, quarter | 98.7% | 592 | 272 (45.9%) |
        | 1 Jun-31 Aug 2010 | trickle, quarter | 97.0% | 781 | 407 (52.1%) |
        | 1 Mar-31 May 2010 | trickle, quarter | 95.5% | 667 | 383 (57.4%) |
        | 2 Dec 2009-26 Feb 2010 | trickle, quarter | 93.8% | 781 | 389 (49.8%) |
        | 1 Sep-30 Nov 2009 | trickle, quarter | 91.5% | 1,017 | 454 (44.6%) |
        | 1 Jun-31 Aug 2009 | trickle, quarter | 87.9% | 1,621 | 581 (35.8%) |
        | 4-28 May 2009 | May campaign | 75.6% | 5,575 | 533 (9.6%) |
        | 16-30 Apr 2009 | April campaign | 71.2% | 1,984 | 332 (16.7%) |
        | 28 Jan-15 Apr 2009 | Jan-Feb campaign + trickle | 61.3% | 4,464 | 537 (12.0%) |
        | 17 Oct-27 Dec 2008 | November campaign + trickle | 53.2% | 3,691 | 270 (7.3%) |

        The windows follow the bank's calling. The source names "17 campaigns that occurred between May 2008 and
        November 2010" (Moro, Laureano, Cortez 2011) without dates, and the file has no campaign id, so the campaigns
        are read from the dates: five bursts of mass calling (days of 150 records or more: 5 May-29 Aug 2008, 17-21 Nov
        2008, 28 Jan-9 Feb 2009, 16-30 Apr 2009, 4-18 May 2009; 5-14% subscribed), and from June 2009 a trickle of
        one-by-one calls, at most 115 a day (36-57% subscribed). Each campaign window starts at its burst's first day
        or in the calling gap before it (no record from 30 Aug to 16 Oct 2008, nor from 28 Dec 2008 to 27 Jan 2009) and
        holds the burst and the trickle after it, so no cut splits a campaign; the trickle has no campaign to cut at,
        so it is cut by calendar quarter. The summer 2008 wave is 53.2% of the records, so it trains every window and
        is never tested. The subscription rate follows the day's calling volume (5.8% on days with 200 calls or more,
        48.5% on days with 20 or fewer), which the input `calls_that_day` carries; the burst windows test mass calling,
        the trickle windows selected calls, and a mean over the windows gives the trickle six of ten votes for 12% of
        the records.

        Ten windows against the nine an IID split of 45,211 records would get (SPLIT-15): the target is reached, every
        window trains on more than half the records (SPLIT-14), and the smallest holds 272 subscribers. The source
        scores its model on time-ordered windows too: a random split does "not reflect the temporal dimension that a
        real prediction system would have to follow" (Moro et al. 2014, p. 5). The time key `time_index` is the
        record's position in the file, which is in date order; it orders the windows and is no model input, and every
        window starts at the first record of its date.
        No gap (SPLIT-10): a record is dated by its last call, which ends the client's calls in that campaign, so its
        outcome is known by the date that orders it. Each test record is predicted from the training records and its
        own inputs only; no feature or model step may use other test records (curation notes, Protocol).
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
        for start, position in WINDOW_STARTS:
            if not (date.iloc[position] == pd.Timestamp(start) and date.iloc[position - 1] < pd.Timestamp(start)):
                raise ValueError(f"Expected the first record of {start} at file position {position}")
        df["time_index"] = np.arange(len(df))
        # The day's calling volume: the records in the file with the same date of the last contact, counted over the
        # whole file (curation notes).
        df["calls_that_day"] = date.map(date.value_counts()).astype("int64").to_numpy()
        # The last contact's day, month, phone type and duration, and this campaign's calls (curation notes).
        df = df.drop(columns=["day", "month", "contact", "duration", "campaign"])
        # "unknown" codes a missing value (the authors' 2014 codebook; CLEAN-10, CLEAN-14).
        df = set_missing(
            df,
            {
                "job": ["unknown"],
                "education": ["unknown"],
            },
        )
        return df

    def _make_splits(self, df: pd.DataFrame) -> Splits:
        """The windows of `WINDOW_STARTS`, newest first, each up to the next start and trained on every earlier record."""
        time_index = df["time_index"].to_numpy()  # the frame arrives sorted by `time_index` with a RangeIndex
        positions = np.arange(len(df))
        splits: Splits = {}
        end = None
        for _, start in WINDOW_STARTS:
            test = (time_index >= start) & (time_index < end) if end is not None else time_index >= start
            splits[len(splits)] = {0: (positions[time_index < start].tolist(), positions[test].tolist())}
            end = start
        return splits

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
                "poutcome",
            ],
        )
