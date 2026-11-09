"""Curated SuperLender repeat-loan timely-settlement task. Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Metric, TaskSummary

SOURCE = "https://zindi.africa/competitions/data-science-nigeria-challenge-1-loan-default-prediction"
COPY_COMMIT = "16379560b10bda88b957c180d4767a37a61454a3"
SECONDS_PER_DAY = 86400
CATEGORIES = (
    "bank_account_type",
    "bank_name_clients",
    "bank_branch_clients",
    "employment_status_clients",
    "level_of_education_clients",
    "was_referred",
)


def _features(raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
    performance = raw["performance"].dropna(subset=["good_bad_flag"]).copy()
    assert performance["systemloanid"].is_unique
    assert performance["good_bad_flag"].isin(["Good", "Bad"]).all()
    performance["creationdate"] = pd.to_datetime(performance["creationdate"], format="mixed")
    performance["_row"] = np.arange(len(performance))
    demographics = raw["demographics"].drop_duplicates().copy()
    assert demographics["customerid"].is_unique
    df = performance.merge(demographics, on="customerid", how="left", validate="many_to_one", sort=False)
    assert len(df) == len(performance)
    birth = pd.to_datetime(df["birthdate"], format="mixed", errors="coerce")
    moment = df["creationdate"]
    before_birthday = (moment.dt.month < birth.dt.month) | (
        (moment.dt.month == birth.dt.month) & (moment.dt.day < birth.dt.day)
    )
    df["age_years"] = moment.dt.year - birth.dt.year - before_birthday.astype(int)
    df["age_years"] = df["age_years"].where(df["age_years"] >= 0)
    df["longitude_gps"] = df["longitude_gps"].where(df["longitude_gps"].between(-180, 180))
    df["latitude_gps"] = df["latitude_gps"].where(df["latitude_gps"].between(-90, 90))
    df["was_referred"] = np.where(df["referredby"].notna(), "Yes", "No")

    history = raw["history"].copy()
    assert history["systemloanid"].is_unique
    for col in ["creationdate", "approveddate", "closeddate", "firstduedate", "firstrepaiddate"]:
        history[col] = pd.to_datetime(history[col], format="mixed", errors="coerce")
    history = history.merge(
        performance[["customerid", "_row", "creationdate"]].rename(columns={"creationdate": "_score_time"}),
        on="customerid",
        how="inner",
        sort=False,
    )
    history = history.loc[
        (history["creationdate"] < history["_score_time"]) & (history["approveddate"] < history["_score_time"])
    ].copy()
    closed = history["closeddate"] < history["_score_time"]
    paid = history["firstrepaiddate"] < history["_score_time"]
    history["_closed"] = closed.astype(int)
    history["_first_paid"] = paid.astype(int)
    history["_open"] = (~closed).astype(int)
    history["_overdue_first_unpaid"] = ((history["firstduedate"] < history["_score_time"]) & ~paid).astype(int)
    history["_first_payment_delay"] = (
        (history["firstrepaiddate"] - history["firstduedate"]).dt.total_seconds() / SECONDS_PER_DAY
    ).where(paid)
    history["_settled_duration"] = (
        (history["closeddate"] - history["approveddate"]).dt.total_seconds() / SECONDS_PER_DAY
    ).where(closed)
    history["_days_since_issue"] = (
        history["_score_time"] - history["creationdate"]
    ).dt.total_seconds() / SECONDS_PER_DAY
    history["_days_since_close"] = (
        (history["_score_time"] - history["closeddate"]).dt.total_seconds() / SECONDS_PER_DAY
    ).where(closed)
    history["_days_to_first_due"] = (
        history["firstduedate"] - history["_score_time"]
    ).dt.total_seconds() / SECONDS_PER_DAY
    history["_approval_hours"] = (history["approveddate"] - history["creationdate"]).dt.total_seconds() / 3600
    history["_referred"] = history["referredby"].notna().astype(int)
    summary = history.groupby("_row", sort=False).agg(
        observed_prior_loan_count=("systemloanid", "size"),
        prior_loanamount_mean=("loanamount", "mean"),
        prior_loanamount_max=("loanamount", "max"),
        prior_totaldue_mean=("totaldue", "mean"),
        prior_termdays_mean=("termdays", "mean"),
        prior_loan_sequence_max=("loannumber", "max"),
        prior_closed_count=("_closed", "sum"),
        prior_open_count=("_open", "sum"),
        prior_observed_first_payment_count=("_first_paid", "sum"),
        prior_overdue_first_unpaid_count=("_overdue_first_unpaid", "sum"),
        prior_first_payment_delay_mean_days=("_first_payment_delay", "mean"),
        prior_settled_duration_mean_days=("_settled_duration", "mean"),
        days_since_first_prior_application=("_days_since_issue", "max"),
        days_since_last_prior_application=("_days_since_issue", "min"),
        days_since_last_observed_settlement=("_days_since_close", "min"),
        prior_first_due_offset_mean_days=("_days_to_first_due", "mean"),
        prior_approval_delay_mean_hours=("_approval_hours", "mean"),
        prior_referred_share=("_referred", "mean"),
    )
    df = df.join(summary, on="_row", validate="one_to_one")
    counts = [c for c in summary if c.endswith("_count")]
    df[counts] = df[counts].fillna(0).astype("int64")
    return df.drop(columns=["_row", "customerid", "systemloanid", "approveddate", "referredby", "birthdate"])


class LoanDefaultPredictionChallenge(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will this customer's repeat loan be settled on time?",
        use_case=(
            "SuperLender uses earlier borrowing history to assess repeat-loan applications. This approximate task "
            "conditions on recorded issued-loan terms; availability for approval or offer decisions is unverified."
        ),
        row="One of 4,368 labeled SuperLender loans, one per customer, applied for during July 1-30, 2017.",
        predicted=(
            "The published Good or Bad flag: settled on time or not settled on time. The grace period, extraction "
            "cutoff and exact label-arrival dates are not supplied; Bad includes failure to settle on time."
        ),
        known=(
            "Application time, recorded loan amount, total due and duration, loan sequence and referral status; "
            "customer age, location, bank, employment and education; summaries of issued history and only payments "
            "and settlements recorded before application. Demographic snapshot and offer timing are unverified."
        ),
        split=(
            "Random held-out customers from this July cohort, not a verified simulation of later applications. "
            "All labels come from one month and their arrival times are missing, preventing verified temporal refits."
        ),
        changes=(
            "We unite the two unlabeled demographic files, collapse exact demographic copies, join one row per "
            "scored loan, and aggregate earlier history while masking later payment/settlement events. Evaluation "
            "uses random holdouts of this one-month cohort; no current loan is relabeled or added from history."
        ),
        fit="approximate",
        fit_reason=(
            "This is one granted-loan cohort with unavailable label-arrival dates, an unspecified label grace rule "
            "and unverified demographic/offer timing. Random splits cannot establish chronological deployment "
            "performance. The pinned participant copy is not authenticated against organizer bytes."
        ),
    )
    unique_name = "loan_default_prediction_challenge"
    year = "2018"
    domain = "finance"
    source = "Zindi"
    source_url = SOURCE
    license = "Zindi competition terms; original challenge restricts redistribution to participants"
    data_tags = ("Spatial", "ForcedIIDFromTemporal")
    download_description = f"""
        Origin: Data Science Nigeria's 2018 Zindi challenge. The organizer download requires platform access.
        This qualification uses Megan Beckett's public participant copy, pinned at Git commit {COPY_COMMIT}.
        Git blob hashes authenticate that copy only, not equivalence to organizer bytes. Do not redistribute the
        data without resolving the applicable source terms; the separate 2022 rerun states different terms.

        mkdir -p local-data-warehouse/loan_default_prediction_challenge
        base=https://raw.githubusercontent.com/MeganBeckett/zindi-loan-prediction/{COPY_COMMIT}/raw_data
        for name in trainperf.csv traindemographics.csv testdemographics.csv trainprevloans.csv; do
            curl --fail --location "$base/$name" -o local-data-warehouse/loan_default_prediction_challenge/$name
        done
    """
    bibtex = r"""
        @misc{DSN2018SuperLender,
          author = {{Data Science Nigeria} and {Zindi}},
          title = {Data Science Nigeria Challenge 1: Loan Default Prediction},
          year = {2018},
          howpublished = {\url{https://zindi.africa/competitions/data-science-nigeria-challenge-1-loan-default-prediction}},
          note = {Competition data; SuperLender repeat-loan repayment}
        }
    """
    curation_comments = """
        We start with four CSV inputs from the pinned Megan Beckett participant copy of the 2018 DSN/Zindi release.
        Myunghwan accepted this identified copy on 2026-11-05; organizer-byte equivalence remains unverified.

        - Prediction point: application, conditional on recorded issued-loan terms. Current approval time is
          dropped because it follows creation. Offer finalization and demographic snapshot timing cannot be verified
          from this release; they remain approximate-fit limitations, not demonstrated outcome leaks. Myunghwan
          chose to retain loanamount, totaldue and termdays on 2026-11-05 with this uncertainty explicit.
        - Source label: Good means timely settlement and Bad means not timely settlement; preserve both classes and
          all 4,368 labeled loans. There are 3,416 Good and 952 Bad outcomes. No days-past-due cutoff or
          label-availability timestamp is invented.
        - Demographic join: concatenate train and test demographics, remove 15 exact copies, then join by customerid
          with a unique-key assertion. The 5,818 distinct customer records have no conflicts; 1,099 labeled
          customers' profiles are in testdemographics. No test labels or fitted all-row statistics are used.
        - History: retain loans whose creation and approval precede the scored application's published creation
          timestamp. Aggregate amounts, terms, observed counts, issue recencies, approval delays and referral share
          to one row per scored loan. Nine scored customers have no supplied prior rows despite loan sequence at
          least two; their observed counts are zero and historical means stay missing. Counts match sequence minus
          one for 4,336 of 4,368 loans, so complete history is not asserted.
        - History events: payments and settlements contribute only when their recorded dates precede application.
          Mask 756 later settlements and 664 later first payments. Scheduled first-due dates are known loan terms,
          including future due dates. Keep counts of observed open loans and overdue unpaid first installments. The
          clocks' time zones are unspecified; no one-hour offset repair is guessed. All masked events fall within
          one hour after application, consistent with an unknown clock or recording offset, not proof of one.
        - Features: birthdate becomes completed age at application; drop raw borrower/loan/referrer identifiers,
          birthdate and current approval time. Retain referral as a category. Categories follow bank/account/branch,
          employment and education meanings; monetary values, counts, durations and GPS coordinates stay numeric.
          Physically invalid coordinates become missing without dropping a loan. Missing categorical fields remain
          missing for the model pipeline. Branch entries are treated as nominal locations without inferred address
          normalization or merges. Myunghwan retained the undated bank, employment, education and GPS profile
          fields on 2026-11-05; their application-time availability remains unverified.
        - Split: ForcedIIDFromTemporal under SPLIT-8. The labeled cohort spans July 1-30, 2017 and lacks
          current-loan settlement/label-arrival dates. At July 30 midnight, 299 loans reach the contractual due proxy
          before cutoff; even all 919 shortest-term loans are below the 2,184-row training floor. Due dates are not
          measured label-arrival times. The source test file has no labels and clock-only application dates. This
          does not prove a temporal deployment is impossible; it prevents verified mature-label windows in this
          copy. No valid temporal score comparison is claimed.
        - Metric: context roc_auc, a curator-selected departure from the source's hard-label error.
          **Exception to MET-4 (2026-11-08, Myunghwan):** The source scores hard-label misclassification error (accuracy = 1 - error). Myunghwan knowingly chose
          threshold-free ROC AUC after the source override was explained. On the unchanged nine splits,
          always Good scores 0.782051 accuracy and 0.5 AUC; matched untuned LightGBM with training-only
          threshold selection scores 0.787698 accuracy and 0.694156 AUC. The curator prefers comparing
          discrimination rather than this majority-dominated hard-label score. This is a case-specific
          preference, not proof accuracy is invalid or a claim that the organizer chose a ranking workflow.
          Serves P3: the curator-selected criterion for comparing this bounded timely-settlement prediction
          task. No lender cost ratio or operational threshold is invented.
          AUROC scores discrimination, not probability calibration or lending profit. The original error remains
          computable and is retained as a diagnostic; AUROC is neither its identity nor an uncomputable-metric stand-in.
        - Cohort/source limits: only granted loans, one July cohort, uncertain label grace/recording window,
          potential demographic/offer snapshot timing, and participant-copy provenance. No unrecorded rejected
          applications are reconstructed. Release permission must be resolved separately; the original and 2022
          challenge pages state different terms.
    """
    target = "good_bad_flag"
    problem_type = "binary_classification"
    metric = Metric.from_context(
        "roc_auc",
        reason=(
            "Myunghwan overruled source misclassification error on 2026-11-08 after its scoring was explained. "
            "Always-Good accuracy is 0.782051; matched LightGBM accuracy is 0.787698 and ROC AUC 0.694156 "
            "on nine unchanged folds, with thresholds chosen within training. The curator prefers threshold-free "
            "discrimination for this bounded task (case-specific MET-4 departure; MET-11 context). "
            "This does not establish accuracy is invalid, calibrated probabilities, or lending utility. "
            "Source: " + SOURCE
        ),
        definition="Standard binary ROC AUC; same value for Bad risk or the complementary Good probability.",
    )
    splits_comment = (
        "Default stratified IID splits, forced from temporal under SPLIT-8: held-out loans/customers of the same "
        "July 2017 cohort, not prospective refits. Label-arrival dates are unavailable; chronological training "
        "with mature outcomes cannot be verified. The contractual due proxy is not treated as measured arrival."
    )

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        ids = {"customerid": "string", "systemloanid": "string", "referredby": "string"}
        return {
            "performance": pd.read_csv(raw_dir / "trainperf.csv", dtype=ids),
            "demographics": pd.concat(
                [
                    pd.read_csv(raw_dir / "traindemographics.csv", dtype=ids),
                    pd.read_csv(raw_dir / "testdemographics.csv", dtype=ids),
                ],
                ignore_index=True,
            ),
            "history": pd.read_csv(raw_dir / "trainprevloans.csv", dtype=ids),
        }

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        return _features(raw)

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=list(CATEGORIES), datetime=["creationdate"])

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        dates = pd.to_datetime(raw["performance"]["creationdate"], format="mixed")
        approval = pd.to_datetime(raw["performance"]["approveddate"], format="mixed")
        due_proxy = approval + pd.to_timedelta(raw["performance"]["termdays"], unit="D")
        rows = []
        for cutoff in ["2017-07-16", "2017-07-21", "2017-07-26", "2017-07-30"]:
            moment = pd.Timestamp(cutoff)
            rows.append(
                {
                    "cutoff": cutoff,
                    "earlier_applications": int((dates < moment).sum()),
                    "contractually_due_before_cutoff": int((due_proxy < moment).sum()),
                    "required_half_cohort": len(dates) // 2,
                }
            )
        return [
            Decision(
                "One labeled cohort cannot establish verified mature-label temporal refits",
                "The contract's due time is a diagnostic proxy, not a measured label-arrival timestamp. "
                "Early settlements and the grace/recording rule are unobserved for current loans. Random splits are "
                "an explicit approximation under SPLIT-8, not a new embargo exception.",
                pd.DataFrame(rows),
            )
        ]
