"""Curated dataset definition for lt_vehicle_loan_default_prediction (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    TaskSummary,
    Temporal,
    TemporalSplits,
    drop_columns,
)

TRAIN_SHA256 = "f515a34e7f72446b520b128f4ccfab7cf7761860b44e789765eb640a4e6383d6"


class LtVehicleLoanDefaultPrediction(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will an issued vehicle loan default on its first monthly instalment due date?",
        use_case=(
            "When a vehicle loan is up for approval at sanction, just before disbursement, the lender scores the "
            "borrower's risk of defaulting on the first monthly instalment to decide whether to grant it: the "
            "organizer's underwriting problem, with rejection rates rising as underwriting tightened."
        ),
        row="One issued vehicle loan/customer record; 233,154 labeled records disbursed in August-October 2018.",
        predicted=(
            "Whether the borrower defaulted on the first monthly instalment (EMI), the organizer's binary label "
            "(21.7% defaults); the release does not give the due date."
        ),
        known=(
            "The release supplies loan terms/channel, borrower profile, document flags and bureau score/history. "
            "The dictionary dates certain account aggregates to disbursement; other bureau freeze dates and "
            "account scope remain unverified (D2), with no demonstrated leakage."
        ),
        split=(
            "Nine four-day windows of later issued loans, September 26-October 31, 2018, each trained on all earlier "
            "disbursals with no gap. The outcomes of at least the last month's training loans were not yet known at "
            "a window's start; measured, they add little, a small part through recent default rates of the same "
            "dealer, branch, employee or postcode."
        ),
        changes=(
            "Exclude the forbidden customer identifier and constant mobile flag; repair birth-date chronology, "
            "numeric history durations and missing bureau scores. The previously inspected supplied November test is unlabeled. "
            "The generated four-day prediction-horizon label means evaluation-window width here, not a supplied due-date lag."
        ),
        fit="approximate",
        fit_reason=(
            "The rows are issued loans only: the model is trained and scored on the loans L&T approved, not every "
            "applicant. The label, a missed first EMI on its due date (21.7%), is an early-delinquency proxy for "
            "credit loss. The training side holds outcomes of at least the last month, which a refit at the "
            "window's start would not yet know. Some bureau freeze dates remain unverified, with no demonstrated "
            "leakage."
        ),
    )

    unique_name = "lt_vehicle_loan_default_prediction"
    year = "2019"
    domain = "finance"
    source = "Other"
    source_url = "https://www.analyticsvidhya.com/datahack/contest/ltfs-datascience-finhack-an-online-hackathon/"
    license = "Not stated in the inspected organizer task and dictionary; resolve terms before release."
    data_tags = ("Spatial", "Anonymized")
    download_description = """
        Original organizer archive, retained intact; extract train.csv and Data Dictionary.xlsx without modification.
        export DATA_FOUNDRY_WAREHOUSE="$PWD/local-data-warehouse"
        mkdir -p local-data-warehouse/lt_vehicle_loan_default_prediction
        curl -fL https://datahack-prod.s3.amazonaws.com/train_file/train_aox2Jxw.zip -o local-data-warehouse/lt_vehicle_loan_default_prediction/train_aox2Jxw.zip
        unzip -n local-data-warehouse/lt_vehicle_loan_default_prediction/train_aox2Jxw.zip 'train.csv' 'Data Dictionary.xlsx' -d local-data-warehouse/lt_vehicle_loan_default_prediction
        Archive SHA-256: 2fabf846906252bee90017b0eaa77469215f01ee65dcc24af47d8a93d3be2e00.
        train.csv SHA-256: f515a34e7f72446b520b128f4ccfab7cf7761860b44e789765eb640a4e6383d6.
        The original unlabeled test_bqCt9Pv.csv was inspected previously for provenance only, not joined or scored;
        it was not available for fresh rereading in the 2026-10-27 qualification.
    """
    bibtex = r"""
        @misc{ltfs2019finhack,
          author = {{L\&T Financial Services} and {Analytics Vidhya}},
          title = {LTFS Data Science FinHack: Vehicle Loan Default Prediction},
          year = {2019},
          howpublished = {\url{https://www.analyticsvidhya.com/datahack/contest/ltfs-datascience-finhack-an-online-hackathon/}}
        }
    """
    curation_comments = """
        - Direct add/review recheck (2026-10-28): all source rows/labels, categorical network codes and exact nine temporal splits remain unchanged; Myunghwan's existing final ship and four task choices remain authoritative. Fresh full independent review found no new demonstrated timing or leakage mechanism requiring a scientific change.
        - Birth-date precision caveat: 55,227 original records (23.6869%) have January 1 birth dates, unchanged by cleaning. The source establishes no sentinel or coarsening convention. Preserve the supplied dates; plausible age chronology does not verify exact day/month or biological accuracy.
        - Final curator verdict (2026-10-28, Myunghwan): "ship for L&T." Accept the current first-instalment default task, source ROC AUC and nine temporal tests, preserving no end trim, retrospective finalized labels with zero added maturity gap, and evidence-conditioned bureau retention. Bureau timing, historical label availability and borrower linkage remain unverified; no build or repository integration is implied.
        - Source follow-up (2026-10-28): reviewed the mirror's six vote-ranked topic metadata/comment responses and top three notebook sources via the authorized gateway. No concrete contrary source correction or leakage mechanism emerged. Original organizer-forum and mirror opening-post bodies remained unavailable; exhaustive forum coverage is not claimed.
        We start with train.csv and Data Dictionary.xlsx from the original organizer's train_aox2Jxw.zip.

        - Prediction point: disbursement, for issued loans and original first-instalment default; no rejected-applicant generalization. Source ROC AUC is retained.
        - UniqueID is excluded as the organizer forbids it. MobileNo_Avl_Flag is 1 in all 233,154 rows and is dropped. All rows remain; the 39 source candidate features become 38.
        - Numeric codes for branch, supplier, manufacturer, postcode, state and employee are categories, as are employment, bureau description and five document flags. Flags co-occur and stay separate.
        - Birth dates use day-month-two-digit-year. Subtract 100 years only where parsing puts birth after disbursement (19,866 rows); resulting ages are 18.00-69.13 years. This chronology repair does not independently verify biological birth dates. Birth remains datetime, without using today's date.
        - Six rows have CREDIT.HISTORY.LENGTH longer than recorded age in completed months (3-100 months); three exceed it by over 24 months. One also has AVERAGE.ACCT.AGE longer by 100 months. None uses the century repair. The dictionary does not settle account scope or which field is wrong; retain with this caveat rather than guessing a repair. This is not evidence of later-populated predictors.
        - AVERAGE.ACCT.AGE and CREDIT.HISTORY.LENGTH are parsed losslessly from years/months to total months, retaining their names. Every labeled value matches the format.
        - Bureau scores marked No Bureau History Available or Not Scored become missing; descriptions remain categorical. Codes 0, 11 and 14-18 encode status. Historical account zeros and 448 primary/61 secondary negative balances stay: no source rule establishes that they are missing or impossible.
        - PERFORM_CNS.SCORE.DESCRIPTION stays an unordered category (CLEAN-14; Lennart, 2026-11-04): it holds the bureau's risk bands, A-Very Low Risk to M-Very High Risk, beside states outside the scale (No Bureau History Available and six Not Scored: ... reasons), a second dimension. The bands' order is in PERFORM_CNS.SCORE.
        - The dictionary dates PRI/SEC account counts, balances and sanctioned/disbursed totals to disbursement, and NEW.ACCTS.IN.LAST.SIX.MONTHS to the preceding six months. The freeze dates and account scope of weakly anchored score, instalment, delinquency, inquiry and duration fields remain unverified (D2). No later-populated predictor or leakage is demonstrated; names and correlations cannot establish timing. The bureau record does not count this loan: all 116,950 rows without bureau history are 0 on every PRI field and 94.1% of them have no enquiries, and the overdue and delinquency fields score flat by disbursal month.
        - Curator decision (2026-10-26, Myunghwan): retain the currently supplied bureau predictors, including fields with unverified snapshot timing/account scope. Retention is not verification of prediction-time availability. Reopen only for new concrete source or actual-data evidence demonstrating incompatible field timing or a leakage mechanism.
        - No exact feature duplicates or conflicting feature-vector labels occur in the labeled source. UniqueID does not recur; this does not prove distinct real borrowers. No guessed customer grouping is introduced.
        - Temporal evaluation: nine four-day windows, the widest whole-day equal windows fitting the recommended nine above the 50% train floor. Length follows coverage, not scores or an assumed due-date lag. Full-table constant detection approximates the pipeline at each refit.
        - The generated "Prediction horizon: 4 days" denotes only evaluation-cohort width here; the first-instalment due-date lag is not supplied.
        - Zero gap (SPLIT-10 as amended 2026-11-04, Lennart; how to record it is open in REVIEW.md): the release gives no due date. Inferred from "monthly instalment", the first instalment falls due at least about a month after disbursement (1-2 months under fixed EMI dates), so a refit at a window's start would not yet know the outcomes of the loans disbursed in the 30 days before it, 40-60% of each training side. Measured on the nine windows: no gap scores 0.007-0.017 ROC AUC above a 30-day gap, depending on the learner (untuned LightGBM, three seeds: 0.0167, 0.009-0.033 per window). A random draw of the no-gap side at the gap side's size keeps 0.0018 to 0.0051 of it across four learners, 11-44% of the gap's cost; the rest is training size. A small part runs through recent labels of the same supplier, branch, employee or postcode: at equal pool size their last-30-day default rates add 0.0026 ROC AUC (0.0005-0.0051, positive in 9 of 9 windows) beyond the older rates on top of a gap model, at most about 0.005 in other encodings; it does not grow in the newest windows, and no borrower recurs. Not through the higher default level of late October: ROC AUC is per window, the true daily default rate ranks a window's loans at only 0.503-0.530, and without the codes and the disbursal-date features the equal-size gain is 0.0019. On these nine windows a 30-day gap would leave 20-53% of the rows for training (SPLIT-14); three two-day windows from 26 October would meet the 50% floor (50.39-56.27%) with three windows instead of nine (SPLIT-15), all in the month-end surge, and at a 45-day lag no three-window design meets it (best 38.8%). Gap 0 widens the margin between learners (gradient boosting over logistic 0.0035 with a 30-day gap, 0.0079 without; the sign changes in 3 of 9 windows); the mean order holds.
        - The newest labeled cohorts stay without release-end trimming: October's default rate (23.5%) is above August's (21.6%) and September's (19.2%), the rise holds in every risk decile and with and without bureau history, and month-ends rise on mature September labels too, so the release end shows drift (month-end and festive season), not censoring. The organizer scored its November loans on the same label, so October's labels had matured.
    """
    target = "loan_default"
    problem_type = "binary_classification"
    metric = Metric.source(
        "roc_auc",
        original="area under the ROC curve",
        reference=source_url,
        definition="ROC AUC between predicted default probabilities and the original observed first-EMI outcome.",
    )
    temporal = Temporal(
        on="DisbursalDate",
        splits=TemporalSplits(window=4, unit="days", n_windows=9, min_train_fraction=0.5),
    )
    splits_comment = """
        Nine adjacent four-day test windows of issued loans, newest first, from 2018-09-26 through 2018-10-31
        (exclusive final boundary 2018-11-01), each trained on every loan disbursed before its start, without a gap.
        The oldest train holds 117,490 of 233,154 rows (50.39%); five-day windows allow only seven windows above that
        floor. The source's November test is unlabeled. The four-day width follows the coverage, not the first
        instalment's due date, which the release does not give. Inferred from the monthly instalment, it falls due at
        least about a month after disbursement, so 40-60% of each training side holds outcomes a refit at the
        window's start would not yet know. Measured, they add little, a small part of it through recent default rates
        of the dealer, branch, staff and postcode codes, with no row-level link (curation notes, "Zero gap"). A 30-day
        gap would leave 20-53% of the rows for training on these windows; three two-day windows would meet the floor
        but give up six of the nine. Every test window starts the day after the newest training labels, and 55% of
        the test rows fall in the 20-31 October month-end and festive surge, where defaults run 1.19-1.36 times what
        a model fitted on August-September predicts. The newest cohorts stay untrimmed.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        path = raw_dir / "train.csv"
        if hashlib.sha256(path.read_bytes()).hexdigest() != TRAIN_SHA256:
            raise ValueError("train.csv differs from the inspected original source; re-audit before use.")
        return pd.read_csv(path)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.copy()
        assert set(df[self.target].unique()) == {0, 1}
        df[self.target] = df[self.target].map({0: "No", 1: "Yes"})
        disbursal = pd.to_datetime(df["DisbursalDate"], format="%d-%m-%y", errors="raise")
        birth = pd.to_datetime(df["Date.of.Birth"], format="%d-%m-%y", errors="raise")
        df["Date.of.Birth"] = birth.where(birth <= disbursal, birth - pd.DateOffset(years=100))
        df["DisbursalDate"] = disbursal
        for column in ("AVERAGE.ACCT.AGE", "CREDIT.HISTORY.LENGTH"):
            parts = df[column].str.extract(r"^(\d+)yrs (\d+)mon$")
            assert parts.notna().all().all()
            months = parts.astype("int64")
            assert months[1].between(0, 11).all()
            df[column] = months[0] * 12 + months[1]
        status = df["PERFORM_CNS.SCORE.DESCRIPTION"].str.startswith(("No Bureau", "Not Scored"))
        df["PERFORM_CNS.SCORE"] = df["PERFORM_CNS.SCORE"].mask(status)
        assert df["MobileNo_Avl_Flag"].eq(1).all()
        return drop_columns(df, ["UniqueID", "MobileNo_Avl_Flag"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=(
                "branch_id",
                "supplier_id",
                "manufacturer_id",
                "Current_pincode_ID",
                "Employment.Type",
                "State_ID",
                "Employee_code_ID",
                "Aadhar_flag",
                "PAN_flag",
                "VoterID_flag",
                "Driving_flag",
                "Passport_flag",
                "PERFORM_CNS.SCORE.DESCRIPTION",
            ),
            datetime=("Date.of.Birth", "DisbursalDate"),
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        monthly = df.groupby(df["DisbursalDate"].dt.to_period("M"), observed=True)[self.target].agg(
            rows="size", defaults=lambda s: s.eq("Yes").sum()
        )
        return [
            Decision(
                "Zero gap, newest cohorts kept",
                "Each window trains on every earlier disbursal; the outcomes of its last month's loans add little, a "
                "small part of it through recent default rates of the dealer, branch, staff and postcode codes "
                "(curation notes, 'Zero gap'). October's default "
                "rate is above August's and September's, so the release end shows no censoring and is not trimmed.",
                monthly,
            )
        ]
