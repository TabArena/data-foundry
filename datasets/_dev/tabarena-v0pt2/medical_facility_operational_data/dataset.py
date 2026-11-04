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
    SplitPlan,
    TaskSummary,
    Temporal,
)

SCHEDULED = ("F1", "F2", "F3")


class MedicalFacilityOperationalData(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How many minutes after its scheduled time will this patient's imaging exam start at this facility?",
        use_case="At patient arrival, imaging operations staff estimate the exam-start delay against the appointment from the current workflow and the known appointment plan.",
        row="One of 82,001 visits of the three scheduled facilities F1-F3, with the facility as context.",
        predicted="The exam start minus the scheduled time, in minutes, signed: an exam that starts early has a negative delay.",
        known="Facility, current queue and resource state, histories of completed exams, the source's time features, counts of booked visits from the appointment schedule and the source's per-exam-type delay and duration estimates. How those estimates were made is not documented. This patient's own appointment time against the arrival, and this patient's exam type, are not inputs: the source's features describe the facility's state for the next patient, whoever it is.",
        split="Nine windows of later visits in time order, each trained on the visits whose exam had begun before the window. The anonymised timestamps are one shift of the real clock for all facilities, and every window has thousands of training visits of each facility.",
        changes="Only the scheduled facilities: the walk-in facility F4 measures another quantity (the wait from arrival) and is left out. The raw timestamps are dropped; their arrival rank is the time column and an input.",
        fit="approximate",
        fit_reason="The source's own delay task on the facilities' own records, in real time order. The gaps: the inputs are the source's patient-agnostic facility state, so this patient's own lateness against the appointment is not an input, and this patient's exam type, contrast and inpatient status were removed by the source's aggregation. The per-exam-type expected-delay table and the schedule fields are kept on purpose as potential leaks, not gaps.",
    )
    unique_name = "medical_facility_operational_data"
    year = "2020"
    domain = "medical & healthcare"
    source = "Other"
    source_url = "https://medicalanalytics.group/operational-data-challenge/"
    license = "CC0 1.0 (Harvard Dataverse doi:10.7910/DVN/X4SJWS, author deposit by Pianykh, 2020-05-24)"
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
    bibtex = r"""
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
    """
    curation_comments = """
        We start with worksheets F1-F3 of the authenticated author workbook WaitData.Published.xlsx (all four sheets are read; F4 is left out).

        - Prediction point: arrival, before the exam starts. Wait is the exam start minus the scheduled time, signed, and agrees with the source timestamps within one minute in every row. Valid negatives and zeros stay, without log transform, clipping or rescaling.
        - One meaning of the target (Lennart, 2026-11-04): only the scheduled facilities F1-F3 (82,001 visits). F4's Wait is another quantity, the wait from arrival of walk-in patients (USE-5, as rain_in_australia; Crowley et al. 2020 model delay and wait separately); a dataset of its own is a separate decision. AvgWaitForDay exists only on F4 and goes with it.
        - Facility is the source worksheet ID, kept as context; neutral F1-F3 labels, as the author code and the PLOS cohort disagree on the modality names. No unseen-facility generalization is claimed.
        - Dtypes: counts and sums numeric; facility and the four yes/no flags categorical. DayOfWeek (1-7) and Month (1-12) ship as numbers and stay numbers, like DayOfYear (CLEAN-14, the cycle rule of 2026-11-01).
        - The three raw timestamps are dropped. The arrival and start timestamps order the rows and decide which labels are known; their dense arrival-order rank is the time column and an input (known at arrival; dropping it changes LightGBM's MAE by +0.08, mean of 9 windows). The sheets list the visits in exactly reverse arrival order. With the scheduled timestamp goes this patient's own minutes early (scheduled minus arrival, correlation -0.605 with Wait), as in the source's patient-agnostic features ("the next patient, whoever it will be", Crowley et al. 2020).
        - The anonymisation is one shift of the real clock for all facilities: in every row the fictitious arrival time of day is the source's StartTime plus 60 minutes, DayOfWeek differs from the fictitious weekday by one constant offset and DayOfYear from the fictitious day of the year by 2 or 3 days (leap years), and the facilities agree on all 459 days shared by all three (694 shared by at least two), with 0 conflicts. So the common arrival order is the real order across facilities, to the minute.
        - Potential leak, kept on purpose (LEAK-10, LEAK-6): the schedule fields (`AheadCount`, `IsFirst`, `IsLast`, `FutFlowCount2/4`, `NumScheduledNextSlot`, `NumScheduledNextW2`, `SumTimeToCompleteNextSlot`, `SumTimeToCompleteNextW2`) describe the final schedule, not the plan at arrival: they match the scheduled visits that took place in 99.9-100% of rows (`IsLast` in 2,166 of 2,166), so no-shows are missing and later add-ons are included (32.1% of rows have an add-on booked within the next hour). Dropping them changes LightGBM's MAE by +0.08 to +0.16 (2 seeds x 3 windows; seed noise about 0.07). They stay because the effect is weak and booking-version snapshots are not supplied; revisit if the authors supply them.
        - Potential leak, kept on purpose (LEAK-38; Lennart, 2026-11-04: "keep them"): `ExpectedDelayNextExam` and the sums built from it (`SumDelayWaitingByExamCode`) are one fixed table of expected delay per exam type (49, 215 and 195 values at F1-F3, reused over the whole period), of undocumented origin and reference period. The risk is a table fit over all rows, test windows included (LEAK-27, LEAK-32): the values correlate 0.44, 0.70 and 0.77 (F1-F3) with the mean Wait of their rows without equalling it (median gap 2.7, 4.9 and 8.8 minutes). They do not match the realised delays (a median gap of 6.0-11.7 minutes for a patient waiting alone), and dropping them changes LightGBM's MAE by 0.01-0.02 minutes, within seed noise. The duration estimates `SumTimeToComplete*` appear to come from the same undocumented estimator family. Revisit if the authors document the table.
        - Potential leak, kept on purpose (LEAK-9, an evaluation leak): every queue field is history at its own row's arrival, but later rows reveal earlier rows' targets. With one exam in progress, `SumDelayInProgress` equals that patient's Wait (14,150 of 14,150 rows), and `SumWaits`, `LineCount0` and `SumHowEarlyWaiting` rebuild the line. A participant who reads the later test rows of a window lowers MAE from 15.57 to 8.70 (-44%, all 9 splits); lead features alone give 13.64. Each test visit is predicted from the training rows and its own features only; no feature or model step may use other test rows. The columns stay: dropping them removes honest signal, and the counts still leak through lead features.
        - mintime and maxtime stay. The dictionary's daily-wait wording is contradicted by exact identities with the exams in progress (zero with none, both equal SumInProgress with one, min+max equals it with two, no count/sum envelope violations): they are elapsed times of the active exams, not the day's extremes.
        - Operational history is not the current patient's target: no recent-history field changes between arrivals without a completed exam, and linked completed exams support the signed end-minus-scheduled histories; exact updater/default rules remain incompletely documented.
        - `OutpatientWaitingCount` equals `LineCount0` + 1 in 80,886 of 82,001 rows and `MalesWaitingCount` exceeds `LineCount0` in 9,376, so both appear to count the arriving patient: attributes known before arrival, no leak. `MalesWaitingCount` is not in Table 1 of Crowley et al. (2020).
        - Codebook: Table 1 of Crowley et al. (2020) names the source features. The window suffixes read as 2/4 = 30/60 minutes, W1-W3 = 30/60/120 minutes and K1-K3 = 2/4/8 customers (our inference from Table 1, not a source statement).
        - Zeros stand in for statistics of empty sets (CLEAN-10), kept as the source ships them: `AvgHowEarlyWaiting` and `AvgWaitByTaskTypeLine` are 0 in all 13,454 empty-line rows, `AvgAgePeopleWaiting` is 0 for an empty line at F1 but a repeated constant at F2 and F3, `AvgDelayForDay` is 0 in 5,898 rows before any exam began, and `MostRecent1-5`, `Median5` and `AvgWaitLastK1-3Customers` are 0 when nothing is completed (`Median5` in 10,040 rows), though 0 is also a valid delay. The flags `NoneInLine` and `NoneCompleted` mark these rows.
        - Source MAE is deliberate in the author challenge (its goal is an MAE reduction against the intercept model) and in the paper's comparisons, which evaluate it per facility (author code WTModel.m; Crowley et al. 2020, Tables 2 and 6). We score per-visit MAE in each window and the equal mean of the nine window scores (Myunghwan, 2026-10-28), not an official source aggregation. The author code labels an RMSE calculation MSE; our RMSE uses the standard definition.
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
    temporal = Temporal(on="arrival_order", horizon=4523, horizon_unit="steps")
    splits_comment = """
        Expanding windows in the common arrival order of F1-F3, newest window first. Start after at least half of all
        visits have both arrived and begun their exams; divide the remaining distinct arrival instants into nine windows
        of about 4,523, keeping timestamp ties intact. Every train arrival and begin precedes its test start. Every
        window has training visits of each facility from before it (at least 24,461 of F1, 8,326 of F2 and 8,215 of
        F3) and 702 to 2,108 test visits of each; the minimum train is 41,002 of 82,001. The timestamps are one shift of
        the real clock for all facilities, so the order is real time; a window is 42 to 53 days. The source tests two
        weeks after six months of training; the longer windows keep about 4,550 test visits each, and the measured cost
        is nil: two-week windows score MAE 14.40 against 14.42 for the shipped windows on the same weeks, and the MAE by
        fortnight since the window start is 15.37, 15.06, 15.33 and 15.47. F3 starts later than F1 and F2: about eight
        months and 8,215 visits of F3 history precede the oldest window. Each test visit is predicted from the training
        rows and its own features only; no feature or model step may use other test rows. No held-out-facility or
        new-patient guarantee is asserted.
    """
    accepted_check_warnings = {}

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        tables = pd.read_excel(
            raw_dir / "WaitData.Published.xlsx", sheet_name=["F1", "F2", "F3", "F4"], engine="calamine"
        )
        return pd.concat([table.assign(facility=name) for name, table in tables.items()], ignore_index=True, sort=False)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw[raw["facility"].isin(SCHEDULED)].copy()
        df["arrival_order"] = df["x_ArrivalDTTM"].rank(method="dense").astype("int64") - 1
        return df.drop(columns=["x_ScheduledDTTM", "AvgWaitForDay"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=("facility", "IsLast", "IsFirst", "NoneInProgress", "NoneCompleted", "NoneInLine"),
            datetime=("x_ArrivalDTTM", "x_BeginDTTM"),
        )

    def _make_splits(self, df: pd.DataFrame) -> SplitPlan:
        arrivals = df["x_ArrivalDTTM"]
        begun = df["x_BeginDTTM"]
        instants = np.sort(arrivals.unique())
        floor = (len(df) + 1) // 2
        first = int(np.searchsorted(instants, np.sort(arrivals.to_numpy())[floor], side="left"))
        while int((arrivals.lt(instants[first]) & begun.lt(instants[first])).sum()) < floor:
            first += 1
        edges = np.linspace(first, len(instants), 10, dtype=int)
        splits = {}
        for chronological in range(9):
            lo = instants[edges[chronological]]
            train = np.flatnonzero((arrivals.lt(lo) & begun.lt(lo)).to_numpy())
            test_mask = arrivals.ge(lo)
            if edges[chronological + 1] < len(instants):
                test_mask &= arrivals.lt(instants[edges[chronological + 1]])
            test = np.flatnonzero(test_mask.to_numpy())
            splits[8 - chronological] = {0: (train.tolist(), test.tolist())}
        return SplitPlan(splits=dict(sorted(splits.items())), df=df.drop(columns=["x_ArrivalDTTM", "x_BeginDTTM"]))

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
        return [
            Decision(
                "One meaning of the target: the scheduled facilities F1-F3",
                "Ship the signed exam-start delay against the appointment of F1-F3, with facility as context. F4's "
                "Wait is the walk-in wait from arrival, another quantity, and is left out (Lennart, 2026-11-04).",
                pd.DataFrame(rows).set_index("facility"),
            )
        ]
