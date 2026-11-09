"""Scheduled imaging exam-start delay prediction (facilities F1-F3) from the authenticated author workbook."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    Source,
    SplitPlan,
    TaskSummary,
    Temporal,
)

SCHEDULED = ("F1", "F2", "F3")
# Statistics of an empty set, written as 0 by the source (CLEAN-10; issue 10). The sums stay 0, their true value.
LINE_AVERAGES = ("AvgHowEarlyWaiting", "AvgWaitByTaskTypeLine", "AvgAgePeopleWaiting")
COMPLETED_AVERAGES = ("Median5", "AvgWaitLastK1Customers", "AvgWaitLastK2Customers", "AvgWaitLastK3Customers")
WINDOW_MINUTES = {"AvgWaitLastW1": 30, "AvgWaitLastW2": 60, "AvgWaitLastW3": 120}
# The source tests on "a further consecutive two weeks" after six months of training (Crowley et al. 2020).
WINDOW_DAYS = 14


def _begun_before_arrival(df: pd.DataFrame, minutes: int | None = None) -> pd.Series:
    """Count the other visits of the same facility and day whose exam had begun at this visit's arrival.

    Without ``minutes``: the exams begun strictly before the arrival (the day so far, as ``AvgDelayForDay`` averages
    them). With ``minutes``: those begun from ``minutes`` before the arrival up to the arrival, both ends included (the
    window of ``AvgWaitLastW1-3``).
    """
    counts = pd.Series(0, index=df.index, dtype="int64")
    for _, visits in df.groupby(["facility", df["x_ArrivalDTTM"].dt.normalize()], sort=False):
        begins = np.sort(visits["x_BeginDTTM"].to_numpy())
        arrivals = visits["x_ArrivalDTTM"].to_numpy()
        if minutes is None:
            counts[visits.index] = np.searchsorted(begins, arrivals, side="left")
            continue
        start = arrivals - np.timedelta64(minutes, "m")
        own = visits["x_BeginDTTM"].to_numpy()
        in_window = np.searchsorted(begins, arrivals, side="right") - np.searchsorted(begins, start, side="left")
        counts[visits.index] = in_window - ((own >= start) & (own <= arrivals))
    return counts


class MedicalFacilityOperationalData(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How many minutes after its scheduled time will this patient's imaging exam start at this facility?",
        use_case="At patient arrival, imaging operations staff estimate the exam-start delay against the appointment from the current workflow and the known appointment plan.",
        row="One of 82,001 visits of the three scheduled facilities F1-F3, with the facility as context.",
        predicted="The exam start minus the scheduled time, in minutes, signed: an exam that starts early has a negative delay.",
        known="Facility, how many minutes before or after the appointment this patient arrived, the current queue and resource state, histories of completed exams, the source's time features, counts of booked visits from the schedule and the source's per-exam-type delay and duration estimates, whose making is not documented. This patient's exam type is not an input.",
        split="Nine two-week windows of later visits in time order, as the source tests two weeks after six months of training; each window trains on all visits whose exam had begun before it. The anonymised timestamps are one shift of the real clock for all facilities, and every window has thousands of training visits of each facility.",
        changes="Only the scheduled facilities: the walk-in facility F4 measures another quantity (the wait from arrival) and is left out. The raw timestamps are dropped; their arrival rank is the time column and an input. How many minutes before the appointment this patient arrived, which the source's features lack, is derived from them and added as an input. Summaries of an empty set, 0 in the source, are missing.",
        fit="approximate",
        fit_reason="The source's own delay task on the facilities' own records, in real time order, with this patient's arrival against the appointment added. The gap: the source's aggregation removed this patient's exam type, contrast and inpatient status, so the other inputs describe the facility's state for whoever comes next. Kept on purpose as potential leaks: the expected-delay table, of undocumented origin, and the schedule fields, which reflect the final schedule.",
    )
    unique_name = "medical_facility_operational_data"
    domain = "medical & healthcare"
    sources = (
        Source(
            role="publication",
            platform="Other",
            url="https://medicalanalytics.group/operational-data-challenge/",
            license="CC0 1.0 (Harvard Dataverse doi:10.7910/DVN/X4SJWS, author deposit by Pianykh, 2020-05-24)",
            year="2020",
            bibtex=r"""
                @article{Pianykh2020,
                  author = {Pianykh, Oleg S. and Guitron, Steven and Parke, Darren and Zhang, Chengzhao and Pandharipande, Pari and Brink, James and Rosenthal, Daniel},
                  title = {Improving healthcare operations management with machine learning},
                  journal = {Nature Machine Intelligence}, volume = {2}, pages = {266--273}, year = {2020},
                  doi = {10.1038/s42256-020-0176-3}
                }
                @article{Crowley2020,
                  author = {Crowley, Colm and Guitron, Steven and Son, Joseph and Pianykh, Oleg S.},
                  title = {Modeling workflows: Identifying the most predictive features in healthcare operational processes},
                  journal = {PLOS ONE}, volume = {15}, number = {6}, pages = {e0233810}, year = {2020},
                  doi = {10.1371/journal.pone.0233810}
                }
            """,
        ),
    )
    data_tags = ("Anonymized",)
    download_description = """
        Primary author release, linked by Pianykh et al. (2020), Nature Machine Intelligence:
        https://medicalanalytics.group/operational-data-challenge/
        mkdir -p local-data-warehouse/medical_facility_operational_data
        curl -L --fail 'https://medicalanalytics.group/wp-content/uploads/2020/04/codeanddata.zip' -o local-data-warehouse/medical_facility_operational_data/author-codeanddata.zip
        unzip -p local-data-warehouse/medical_facility_operational_data/author-codeanddata.zip CodeAndData/Data/WaitData.Published.xlsx > local-data-warehouse/medical_facility_operational_data/WaitData.Published.xlsx
        Author archive SHA256 307f5991208b33e60615ef9c145bb7c30dff3bdbccab292d60c86460e8f01c80.
        Workbook SHA256 153cff36b4bbf2d972f415c00a786ae5d5e65557ae23b0379fd33efb69060f2e.
        This workbook is byte-identical to Kaggle mirror version 1, updated 2021-02-10:
        https://www.kaggle.com/api/v1/datasets/download/weirdolucifer/medical-facility-operational-data?datasetVersionNumber=1
        Mirror archive SHA256 d2427f01c225122fd406bcd28d55e78439e60a1465f7514caf22e593ebd9f256.
        Read the four worksheets F1-F4; the definition keeps the scheduled facilities F1-F3. Counts differ from the related PLOS analytical cohort; exact cohort equivalence is not claimed.
    """
    curation_comments = """
        We start with worksheets F1-F3 of the authenticated author workbook WaitData.Published.xlsx (all four sheets are read; F4 is left out).

        - Prediction point: arrival, before the exam starts. Wait is the exam start minus the scheduled time, signed, and agrees with the source timestamps within one minute in every row. Valid negatives and zeros stay, without log transform, clipping or rescaling.
        - One meaning of the target (Lennart, 2026-11-04): only the scheduled facilities F1-F3 (82,001 visits). F4's Wait is another quantity, the wait from arrival of walk-in patients (USE-5, as rain_in_australia; Crowley et al. 2020 model delay and wait separately); a dataset of its own is a separate decision. AvgWaitForDay exists only on F4 and goes with it.
        - Facility is the source worksheet ID, kept as context; neutral F1-F3 labels, as the author code and the PLOS cohort disagree on the modality names. No unseen-facility generalization is claimed.
        - Dtypes: counts and sums numeric; facility and the four yes/no flags categorical. DayOfWeek (1-7) and Month (1-12) ship as numbers and stay numbers, like DayOfYear (CLEAN-14, the cycle rule of 2026-11-01).
        - The three raw timestamps are dropped. The arrival and start timestamps order the rows and decide which labels are known; their dense arrival-order rank is the time column and an input (known at arrival; dropping it changes LightGBM's MAE by +0.12, mean of the nine 14-day windows and 2 seeds, higher in 16 of 18 fits). The sheets list the visits in exactly reverse arrival order. The scheduled timestamp goes after `minutes_early` is derived from it (next bullet). Superseded 2026-11-05: until then this patient's own minutes early (correlation -0.605 with Wait) left with it, as in the source's patient-agnostic features ("the next patient, whoever it will be", Crowley et al. 2020).
        - CC (2026-11-05, Lennart): add `minutes_early` (issue 6, A; USE-6, CLEAN-19): this patient's scheduled time minus arrival time in minutes, positive when the patient arrives early and negative when late, derived before `x_ScheduledDTTM` is dropped; the inputs go from 87 to 88. It is known at check-in, the prediction point: the appointment is in the plan and the arrival is now. CLEAN-19's ground is "restores meaning the source destroyed": the anonymisation shifted every timestamp by one clock and kept the difference, while the source treats its timestamps as "only for sorting" and its features describe the next patient, whoever it is. No value is missing; it runs from -328 to +522 minutes (median 20.8; late in 27.2%, 6.6% and 9.3% of F1-F3 visits), and since every exam begins after its arrival, Wait is at least minus `minutes_early` in all 82,001 rows. Untuned LightGBM (L1 loss, 500 trees) on this frame and the nine 14-day windows: MAE 15.47 without it and 13.70 with it (-11%, mean of 9 windows, 2 seeds, lower in all 18 fits; the training median scores 21.63; on the earlier 42-53-day windows 15.29 and 13.56). This sets it apart from protein_model_quality_rf_pcp, kept with no new features (2026-11-04): there the signal of a built feature was weak and the dataset is marked `Outdated`; here one input the actor reads at check-in lowers the error by a ninth. The fit stays approximate: this patient's exam type stays lost in the source's aggregation (USE-8).
        - The anonymisation is one shift of the real clock for all facilities: in every row the fictitious arrival time of day is the source's StartTime plus 60 minutes, DayOfWeek differs from the fictitious weekday by one constant offset and DayOfYear from the fictitious day of the year by 2 or 3 days (leap years), and the facilities agree on all 459 days shared by all three (694 shared by at least two), with 0 conflicts. So the common arrival order is the real order across facilities, to the minute.
        - Potential leak, kept on purpose (LEAK-10, LEAK-6): the schedule fields (`AheadCount`, `IsFirst`, `IsLast`, `FutFlowCount2/4`, `NumScheduledNextSlot`, `NumScheduledNextW2`, `SumTimeToCompleteNextSlot`, `SumTimeToCompleteNextW2`) describe the final schedule, not the plan at arrival: they match the scheduled visits that took place in 99.9-100% of rows (`IsLast` in 2,166 of 2,166), so no-shows are missing and later add-ons are included (32.1% of rows have an add-on booked within the next hour). Dropping all nine changes LightGBM's MAE by +0.05 (mean of the nine 14-day windows and 2 seeds; -0.06 to +0.14 per fit, higher in 15 of 18; a window's MAE differs by 0.05 between seeds on average; +0.14 and R^2 0.660 to 0.644 with the leak probe's L2 model, where `AheadCount` alone is worth +0.11); on the earlier windows seven of them were worth +0.08 to +0.16 (2 seeds x 3 windows; seed noise about 0.07). They stay because the effect is weak and booking-version snapshots are not supplied; revisit if the authors supply them.
        - CC (2026-11-05, Lennart): the nine schedule fields stay (issue 11, A), as an application of LEAK-10's clause on values read at a later pull (answer (a)): the late cells cannot be located row by row, so the whole-field worth is an upper bound on the late part, and it sits within about two seed SDs (+0.08 to +0.16 against 0.07 on the earlier windows; +0.05 against 0.05 on the 14-day windows), so the late part shows no gain.
        - Potential leak, kept on purpose (LEAK-38; Lennart, 2026-11-04: "keep them"): `ExpectedDelayNextExam` and the sums built from it (`SumDelayWaitingByExamCode`) are one fixed table of expected delay per exam type (49, 215 and 195 values at F1-F3, reused over the whole period), of undocumented origin and reference period. The risk is a table fit over all rows, test windows included (LEAK-27, LEAK-32): the values correlate 0.44, 0.70 and 0.77 (F1-F3) with the mean Wait of their rows without equalling it (median gap 2.7, 4.9 and 8.8 minutes). They do not match the realised delays (a median gap of 6.0-11.7 minutes for a patient waiting alone), and dropping them changes LightGBM's MAE by -0.005 minutes (mean of the nine 14-day windows and 2 seeds, higher in 7 of 18 fits; 0.01-0.02 on the earlier windows), within seed noise. The duration estimates `SumTimeToComplete*` appear to come from the same undocumented estimator family. Revisit if the authors document the table.
        - CC (2026-11-05, Lennart): the expected-delay table stays under LEAK-38 as amended on this dataset and tunisian_fraud_detection_challenge (issue 9, D, scope (a)): fields that may be post-outcome, anonymised or named, whose timing the source leaves undocumented and no test can establish, in data the data owner released for its own challenge, stay with this note and are named in `fit_reason` as kept (USE-8). The authors released this workbook for their own operational data challenge, and `fit_reason` names the table.
        - Potential leak, kept on purpose (LEAK-9, an evaluation leak): every queue field is history at its own row's arrival, but later rows reveal earlier rows' targets. With one exam in progress, `SumDelayInProgress` equals that patient's Wait (14,150 of 14,150 rows), and `SumWaits`, `LineCount0` and `SumHowEarlyWaiting` rebuild the line. A participant who reads the later test rows of a window lowers MAE from 13.85 to 6.83 (-51%, lower in all 9 windows: default LightGBM against the task gamer's decode, on this frame and the 14-day windows); the features of the next arrivals alone give 11.52. On the 2026-11-04 frame, without `minutes_early`, the figures are 15.65, 8.70 and 13.72 (15.57, 8.70 and 13.64 on the earlier windows). Each test visit is predicted from the training rows and its own features only; no feature or model step may use other test rows. The columns stay: dropping them removes honest signal, and the counts still leak through lead features.
        - CC (2026-11-05, Lennart): the protocol line stays as implemented (issue 7, A), under LEAK-9 as amended on this dataset (answer (c)): an evaluation leak is fixed in the scoring or by a protocol line the benchmark checks, and a method that learns from the test block is called out and not benchmarked ("we investigate models, and would find out if they do transductive learning which we can call out and not benchmark"). The benchmark-side check is listed in the working copy's `BENCHMARK_CHANGES_TODO.md`.
        - mintime and maxtime stay. The dictionary's daily-wait wording is contradicted by exact identities with the exams in progress (zero with none, both equal SumInProgress with one, min+max equals it with two, no count/sum envelope violations): they are elapsed times of the active exams, not the day's extremes.
        - Operational history is not the current patient's target: no recent-history field changes between arrivals without a completed exam, and linked completed exams support the signed end-minus-scheduled histories; exact updater/default rules remain incompletely documented.
        - `OutpatientWaitingCount` equals `LineCount0` + 1 in 80,886 of 82,001 rows and `MalesWaitingCount` exceeds `LineCount0` in 9,376, so both appear to count the arriving patient: attributes known before arrival, no leak. `MalesWaitingCount` is not in Table 1 of Crowley et al. (2020).
        - Codebook: Table 1 of Crowley et al. (2020) names the source features. The window suffixes read as 2/4 = 30/60 minutes, W1-W3 = 30/60/120 minutes and K1-K3 = 2/4/8 customers (our inference from Table 1, not a source statement). Superseded 2026-11-05: the data show K1-K3 = the day's last 5/10/15 completed exams and confirm W1-W3 = 30/60/120 minutes (the CC line on issue 10 below).
        - Zeros stand in for statistics of empty sets (CLEAN-10), kept as the source ships them: `AvgHowEarlyWaiting` and `AvgWaitByTaskTypeLine` are 0 in all 13,454 empty-line rows, `AvgAgePeopleWaiting` is 0 for an empty line at F1 but a repeated constant at F2 and F3, `AvgDelayForDay` is 0 in 5,898 rows before any exam began, and `MostRecent1-5`, `Median5` and `AvgWaitLastK1-3Customers` are 0 when nothing is completed (`Median5` in 10,040 rows), though 0 is also a valid delay. The flags `NoneInLine` and `NoneCompleted` mark these rows. Superseded 2026-11-05: these values are missing now (next bullet); `AvgDelayForDay` has no begun exam in 5,774 rows (5,898 counted the rows with none completed), and `NoneCompleted` marks `Median5` = 0, not "nothing completed".
        - CC (2026-11-05, Lennart): summaries of an empty set set to missing (issue 10, B; CLEAN-10, as ashrae's and rain_in_australia's cloud cover 9 and house_sales's `yr_renovated` 0). The source writes 0 for an average, a median or a recent delay over an empty set, and 0 is also a valid delay. The sums (`Sum*`) stay 0, their true value. Each condition is derived in `_clean` from the data there; 186,047 cells in 16 columns, every one a 0 except the `AvgAgePeopleWaiting` constants (counts per column in the README's decision table):
          - Empty line, `NoneInLine` (equal to `LineCount0` = 0 in every row): `AvgHowEarlyWaiting`, `AvgWaitByTaskTypeLine` and `AvgAgePeopleWaiting`, 13,454 rows each (9,776, 2,991 and 687 at F1-F3). `AvgAgePeopleWaiting` held 0 at F1 and, at F2 and F3, six repeated constants (37.0586 in 1,952 rows, 94.8172 in 377) and 160 zeros; in the 68,547 rows with a line these constants occur once and 0 never. The 407 zeros kept in `AvgHowEarlyWaiting` are real: a whole-minute mean of minutes early near 0.
          - Nothing completed today, `NumCompletedToday` = 0 (9,779 rows): `Median5` and `AvgWaitLastK1-3Customers`; `MostRecentk` where fewer than k exams are completed today (9,779, 12,379, 14,965, 17,318 and 19,412 rows for k = 1-5), where it is 0 in every row. The flag `NoneCompleted` is not the condition: it equals `Median5` = 0 in all 82,001 rows and so also marks 261 rows with completed exams whose recent delays have a median within half a minute of 0, a real value. The zeros kept (261 in `Median5`, 379-566 per `MostRecentk`) are real delays of 0.
          - `AvgWaitLastK1-3Customers` is the sum of the day's last 5, 10 or 15 completed delays divided by 5, 10 or 15 and cut to a whole minute (exact in every row we can test: all rows for K1, rows with at most five completed for K2 and K3). With 1 to 14 completed exams it is that sum over K, defined and kept as the source ships it; with none it averages nothing. Its zeros kept (636, 1,190 and 1,677) come from cutting small sums.
          - `AvgDelayForDay` is the mean Wait of the day's exams begun strictly before the arrival (to 0.01 minutes in all but one of the 76,227 rows with one): missing in the 5,774 rows with none, counted from the timestamps before they are dropped. Its 323 zeros kept have begun exams (322 with a mean Wait of exactly 0, one a stray 0 against a mean of -4.1).
          - `AvgWaitLastW1-3` is the mean start-minus-arrival time of the exams begun in the 30, 60 or 120 minutes up to the arrival, both ends included (within a minute in 97% of rows), not of completed exams: with no completion in the window it is nonzero in 41-50% of rows. Missing where no other exam began in the window (12,841, 8,253 and 5,848 rows), all of which held 0; the 175, 88 and 28 zeros kept have begun exams with a mean near 0.
          - A 0 can be a real value in every blanked column except `AvgWaitByTaskTypeLine` and `AvgAgePeopleWaiting`, so no column is blanked on its zeros alone.
          - Effect: untuned LightGBM (L1 loss, 500 trees) on this frame and the nine 14-day windows scores MAE 13.681 with the source's values and 13.698 with the missing values (+0.017, mean of 9 windows and 2 seeds, lower in 6 of 18 fits; a window's MAE differs by 0.05 between seeds on average; on the earlier windows 13.565 and 13.577): no measurable change. The flags stay as inputs.
        - Source MAE is deliberate in the author challenge (its goal is an MAE reduction against the intercept model) and in the paper's comparisons, which evaluate it per facility (author code WTModel.m; Crowley et al. 2020, Tables 2 and 6). We score per-visit MAE in each window and the equal mean of the nine window scores (Myunghwan, 2026-10-28), not an official source aggregation. The author code labels an RMSE calculation MSE; our RMSE uses the standard definition.
        - CC (2026-11-05, Lennart): the declared metric (the source's MAE in minutes, per window, the equal mean of the nine windows) is checked and stays as declared.
        - CC (2026-11-05, Lennart): the source's two-week test windows (issue 8, B, choice (b); SPLIT-12, SPLIT-19): nine 14-day windows, each from the first whole day at or after the start of one of the nine equal-count windows shipped before (42 to 53 days long), so the folds stay nine and the test visits go from 40,995 to 12,408. The training side stays expanding (the source trained on six months; here 50.1% to 94.6% of the visits, so SPLIT-14's floor and its three windows hold). The day comes from the arrival timestamp in `_clean`, since the time column is the arrival rank, and leaves with the timestamps in `_make_splits`. The planned exception to SPLIT-19 is dropped: the split follows the source. The longer windows had cost nothing measurable (two-week windows 14.40 against 14.42 on the same weeks). The MAE figures in these notes are re-measured on the new windows, with the earlier figures beside them.
        - All source negatives, repeated operational states and missing values remain.
    """
    target = "Wait"
    problem_type = "regression"
    metric = Metric.source(
        "mae",
        original="Mean absolute error in minutes: the challenge's goal is an MAE reduction against the intercept model; the author code (WTModel.m) and Crowley et al. (2020) evaluate it per facility.",
        reference="https://medicalanalytics.group/operational-data-challenge/",
        definition="Source MAE formula in minutes on all held-out visits within each window, summarized by the standard equal mean of nine window MAEs. The source does not prescribe cross-facility or across-window weighting; no facility normalization is applied.",
    )
    temporal = Temporal(on="arrival_order", horizon=WINDOW_DAYS, horizon_unit="days")
    splits_comment = """
        Expanding windows in the common arrival order of F1-F3, newest window first. The source trains on six months
        and tests on "a further consecutive two weeks" (Crowley et al. 2020), so each test window is 14 whole days.
        The nine windows start on the first whole day at or after nine points that divide the distinct arrival instants
        after the training floor into equal parts; before the first, at least half of all visits have arrived and begun
        their exams. They start 44 to 53 days apart and do not tile the period: 12,408 test visits in all, 1,140 to
        1,540 per window, and the 2,921 visits after the newest window are in no split. Each window trains on every
        visit that arrived and began its exam before its first day: 41,048 to 77,557 of 82,001 (50.1% to 94.6%). No
        exam begins on a later day than its arrival, and no visit arrives between 22:00 and 07:00, so a day boundary
        cuts no visit. Every window has training visits of each facility (at least 24,478 of F1, 8,339 of F2 and 8,231
        of F3) and 217 to 688 test visits of each. The timestamps are one shift of the real clock for all facilities,
        so the order is real time. F3 starts later than F1 and F2: about eight months and 8,231 visits of F3 history
        precede the oldest window. Each test visit is predicted from the training rows and its own features only; no
        feature or model step may use other test rows. No held-out-facility or new-patient guarantee is asserted.
    """
    accepted_check_warnings = {
        "splits_rows_unused": "By design (Lennart, 2026-11-05, issue 8): the nine 14-day windows start at the nine "
        "equal-count points of the arrival instants and do not tile the period, so the 2,921 visits after the newest "
        "window's last day are in no split; every visit before it is in a training side.",
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        tables = pd.read_excel(
            raw_dir / "WaitData.Published.xlsx", sheet_name=["F1", "F2", "F3", "F4"], engine="calamine"
        )
        return pd.concat([table.assign(facility=name) for name, table in tables.items()], ignore_index=True, sort=False)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw[raw["facility"].isin(SCHEDULED)].copy()
        df["arrival_order"] = df["x_ArrivalDTTM"].rank(method="dense").astype("int64") - 1
        # This patient's appointment against the arrival, known at check-in: positive when early, negative when late.
        df["minutes_early"] = (df["x_ScheduledDTTM"] - df["x_ArrivalDTTM"]).dt.total_seconds() / 60
        # The arrival day (days since the first arrival's), for the 14-day test windows; it leaves in `_make_splits`.
        df["x_ArrivalDay"] = (df["x_ArrivalDTTM"].dt.normalize() - df["x_ArrivalDTTM"].min().normalize()).dt.days
        # Statistics of an empty set: the source writes 0, which reads as an on-time history; set to missing.
        empty_line = df["NoneInLine"].eq(1)
        for column in LINE_AVERAGES:
            df[column] = df[column].where(~empty_line)
        completed = df["NumCompletedToday"]
        for column in COMPLETED_AVERAGES:
            df[column] = df[column].where(completed.gt(0))
        for k in range(1, 6):
            df[f"MostRecent{k}"] = df[f"MostRecent{k}"].where(completed.ge(k))
        df["AvgDelayForDay"] = df["AvgDelayForDay"].where(_begun_before_arrival(df).gt(0))
        for column, minutes in WINDOW_MINUTES.items():
            df[column] = df[column].where(_begun_before_arrival(df, minutes).gt(0))
        return df.drop(columns=["x_ScheduledDTTM", "AvgWaitForDay"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=("facility", "IsLast", "IsFirst", "NoneInProgress", "NoneCompleted", "NoneInLine"),
            datetime=("x_ArrivalDTTM", "x_BeginDTTM"),
        )

    def _make_splits(self, df: pd.DataFrame) -> SplitPlan:
        arrivals = df["x_ArrivalDTTM"]
        begun = df["x_BeginDTTM"]
        day = df["x_ArrivalDay"]
        first_day = arrivals.min().normalize()
        # Nine starts that divide the arrival instants after the 50% training floor into equal parts.
        instants = np.sort(arrivals.unique())
        floor = (len(df) + 1) // 2
        first = int(np.searchsorted(instants, np.sort(arrivals.to_numpy())[floor], side="left"))
        while int((arrivals.lt(instants[first]) & begun.lt(instants[first])).sum()) < floor:
            first += 1
        edges = np.linspace(first, len(instants), 10, dtype=int)[:-1]
        splits = {}
        for chronological, edge in enumerate(edges):
            # Each window is the WINDOW_DAYS whole days from the first day that starts at or after the instant.
            start_day = int(day[arrivals.eq(instants[edge])].iloc[0])
            if arrivals[day.eq(start_day)].lt(instants[edge]).any():
                start_day += 1
            start = first_day + pd.Timedelta(days=start_day)
            train = np.flatnonzero((arrivals.lt(start) & begun.lt(start)).to_numpy())
            assert len(train) >= floor, (start_day, len(train))
            test = np.flatnonzero((day.ge(start_day) & day.lt(start_day + WINDOW_DAYS)).to_numpy())
            splits[8 - chronological] = {0: (train.tolist(), test.tolist())}
        return SplitPlan(
            splits=dict(sorted(splits.items())), df=df.drop(columns=["x_ArrivalDTTM", "x_BeginDTTM", "x_ArrivalDay"])
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        rows = []
        for facility, table in raw.groupby("facility", sort=True):
            rows.append(
                {
                    "facility": facility,
                    "shipped": facility in SCHEDULED,
                    "target meaning": "start minus scheduled" if facility in SCHEDULED else "start minus arrival",
                    "visits": len(table),
                    "negative targets": int(table.Wait.lt(0).sum()),
                    "zero targets": int(table.Wait.eq(0).sum()),
                    "median minutes": float(table.Wait.median()),
                    "p99 minutes": float(table.Wait.quantile(0.99)),
                    "standard deviation minutes": float(table.Wait.std()),
                }
            )
        empty_sets = [
            *((column, "empty line (`NoneInLine`)") for column in LINE_AVERAGES),
            *((column, "no exam completed today (`NumCompletedToday` = 0)") for column in COMPLETED_AVERAGES),
            *((f"MostRecent{k}", f"fewer than {k} exams completed today") for k in range(1, 6)),
            ("AvgDelayForDay", "no exam of the day begun before the arrival"),
            *(
                (column, f"no other exam begun in the {minutes} minutes up to the arrival")
                for column, minutes in WINDOW_MINUTES.items()
            ),
        ]
        empty = pd.DataFrame(
            [
                {
                    "column": column,
                    "empty set": condition,
                    "set to missing": int(df[column].isna().sum()),
                    "zeros kept as values": int(df[column].eq(0).sum()),
                }
                for column, condition in empty_sets
            ]
        ).set_index("column")
        return [
            Decision(
                "One meaning of the target: the scheduled facilities F1-F3",
                "Ship the signed exam-start delay against the appointment of F1-F3, with facility as context. F4's "
                "Wait is the walk-in wait from arrival, another quantity, and is left out (Lennart, 2026-11-04).",
                pd.DataFrame(rows).set_index("facility"),
            ),
            Decision(
                "Summaries of an empty set are missing",
                "The source writes 0 for an average, median or recent delay over an empty set, and 0 is also a valid "
                "delay. Those values are missing now; the zeros that remain are real values. The sums stay 0 "
                "(Lennart, 2026-11-05; CLEAN-10).",
                empty,
            ),
        ]
