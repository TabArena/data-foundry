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
            "A lender estimates first-instalment default risk at disbursement, for example to prioritize risk "
            "monitoring of its issued loans. This cohort cannot validate decisions for rejected applicants."
        ),
        row="One issued vehicle loan/customer record; 233,154 labeled records disbursed in August-October 2018.",
        predicted=(
            "The original binary first-EMI default outcome, using finalized labels regardless of observation time; "
            "the due-date lag is not supplied."
        ),
        known=(
            "The release supplies loan terms/channel, borrower profile, document flags and bureau score/history. "
            "The dictionary dates certain account aggregates to disbursement; other bureau freeze dates and "
            "account scope remain unverified (D2), with no demonstrated leakage."
        ),
        split=(
            "Nine four-day windows of later issued loans, September 26-October 31, 2018, with earlier disbursals "
            "for training with zero added training-label gap. Finalized labels are used retrospectively; historical "
            "operational label availability is not established."
        ),
        changes=(
            "Exclude the forbidden customer identifier and constant mobile flag; repair birth-date chronology, "
            "numeric history durations and missing bureau scores. The previously inspected supplied November test is unlabeled. "
            "The generated four-day prediction-horizon label means evaluation-window width here, not a supplied due-date lag."
        ),
        fit="approximate",
        fit_reason=(
            "This retrospective evaluation follows the curator's disbursement-time task and permits finalized labels "
            "with zero added training-label gap. It does not establish operational label availability at each "
            "historical cutoff. Some bureau freeze dates remain unverified, with no demonstrated leakage."
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
        - The dictionary dates PRI/SEC account counts, balances and sanctioned/disbursed totals to disbursement, and NEW.ACCTS.IN.LAST.SIX.MONTHS to the preceding six months. The freeze dates and account scope of weakly anchored score, instalment, delinquency, inquiry and duration fields remain unverified (D2). No later-populated predictor or leakage is demonstrated; names and correlations cannot establish timing.
        - Curator decision (2026-10-26, Myunghwan): retain the currently supplied bureau predictors, including fields with unverified snapshot timing/account scope. Retention is not verification of prediction-time availability. Reopen only for new concrete source or actual-data evidence demonstrating incompatible field timing or a leakage mechanism.
        - No exact feature duplicates or conflicting feature-vector labels occur in the labeled source. UniqueID does not recur; this does not prove distinct real borrowers. No guessed customer grouping is introduced.
        - Temporal evaluation: nine four-day windows, the widest whole-day equal windows fitting the recommended nine above the 50% train floor. Length follows coverage, not scores or an assumed due-date lag. Full-table constant detection approximates the pipeline at each refit.
        - The generated "Prediction horizon: 4 days" denotes only evaluation-cohort width here; the first-instalment due-date lag is not supplied.
        - Exception to SPLIT-10 (2026-10-23, Myunghwan): zero added gap serves the explicitly retrospective issued-loan cohort task (P3/USE-1), rather than replay of operational historical refits. Historical label availability is not established, and a demonstrated SPLIT-9 shortcut would still require repair.
        - The curator approved finalized training labels regardless of observation time: use strictly earlier disbursals with zero added training-label gap. Keep the newest labeled cohorts without release-end trimming, following the saved release-boundary diagnostic and curator decision. This retrospective approximation does not establish operational label availability at each historical cutoff; no due-date lag is inferred.
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
        Retrospective temporal evaluation windows, newest first: nine adjacent four-day intervals from 2018-09-26 through
        2018-10-31 (exclusive final boundary 2018-11-01). Every training date precedes its test start. The oldest
        train holds 117,490 of 233,154 rows (50.39%). Five-day windows allow only seven windows above that floor.
        The source's November test is unlabeled. Neither the four-day evaluation span nor zero extra gap specifies
        the first-instalment horizon. By the curator's decision, earlier-disbursal training rows use finalized labels
        regardless of when those labels became observable, with zero added training-label gap and no release-end
        trimming. This retrospective evaluation does not establish operational label availability at each
        historical cutoff.
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
                "Retrospective finalized-label convention",
                "The curator permits finalized labels regardless of observation time, with zero added "
                "training-label gap and strictly earlier-disbursal training. The newest labeled cohorts are "
                "retained by the saved release-boundary diagnostic and curator decision. Its August-September reference "
                "is short and only approximately stable: September's default rate was 88.97% of August's. "
                "These monthly counts "
                "are descriptive and do not establish operational label availability at historical cutoffs "
                "or independently exclude censoring. Bureau freeze dates remain unverified (D2), with no "
                "demonstrated leakage.",
                monthly,
            )
        ]
