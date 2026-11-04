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
        known="Facility, current queue and resource state, histories of completed exams, the source's time features, the appointment plan and the source's per-exam-type delay and duration estimates. How those estimates were made is not documented.",
        split="Nine windows of later visits in time order, each trained on the visits whose exam had begun before the window. The anonymised timestamps are one shift of the real clock for all facilities, and every window has thousands of training visits of each facility.",
        changes="Only the scheduled facilities: the walk-in facility F4 measures another quantity (the wait from arrival) and is left out. The timestamps only order the rows and are no inputs.",
        fit="approximate",
        fit_reason="The source's own delay task on the facilities' own records, in time order. The gaps: the visits ship without real dates, so the windows count events, not days, and the source does not document how its per-exam-type estimates were made.",
    )
    unique_name = "medical_facility_operational_data"
    year = "2020"
    domain = "medical & healthcare"
    source = "Other"
    source_url = "https://medicalanalytics.group/operational-data-challenge/"
    license = "CC0: Public Domain (Kaggle mirror; original terms not independently retrieved)"
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
        Read the four worksheets F1-F4; the definition keeps the scheduled facilities F1-F3. Counts differ from the related PLOS analytical cohort; exact cohort equivalence is not claimed. Dataverse retrieval returned HTTP 403, but primary author workbook identity is verified independently.
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
        - One meaning of the target (Lennart, 2026-11-04): only the scheduled facilities F1-F3 (82,001 visits). F4's Wait is another quantity, the wait from arrival of walk-in patients (CLEAN-21, USE-5; Crowley et al. 2020 model delay and wait separately); a dataset of its own is a separate decision. AvgWaitForDay exists only on F4 and goes with it.
        - Facility is the source worksheet ID, kept as context; neutral F1-F3 labels, as the author code and the PLOS cohort disagree on the modality names. No unseen-facility generalization is claimed.
        - Dtypes: counts and sums numeric; facility and the four yes/no flags categorical. DayOfWeek (1-7) and Month (1-12) ship as numbers and stay numbers, like DayOfYear (CLEAN-14, the cycle rule of 2026-11-01).
        - The three artificial timestamps are no inputs. The arrival and start timestamps order the rows and decide which labels are known, then are dropped; a dense arrival-order rank is the time column. The sheets list the visits in exactly reverse arrival order.
        - The anonymisation is one shift of the real clock for all facilities: in every row the fictitious arrival time of day is the source's StartTime plus 60 minutes, DayOfWeek differs from the fictitious weekday by one constant offset and DayOfYear from the fictitious day of the year by 2 or 3 days (leap years), and the facilities agree on all 459 shared days. So the common arrival order is the real order across facilities, to the minute.
        - Planned demand is allowed at arrival: scheduled counts in the following 30/60 minutes, next-slot/hour bookings and the source's per-exam-type estimates refer to the plan, not to realised outcomes. How the estimates were made is not documented.
        - Potential leak, kept on purpose (LEAK-38; Lennart, 2026-11-04: "keep them"): `ExpectedDelayNextExam` and the sums built from it (`SumDelayWaitingByExamCode`) are one fixed table of expected delay per exam type (49, 215 and 195 values at F1-F3, reused over the whole period), of undocumented origin and reference period. They do not match the realised delays (a median gap of 6.0-11.7 minutes for a patient waiting alone), and dropping them changes LightGBM's MAE by 0.01-0.02 minutes, within seed noise. Revisit if the authors document the table.
        - IsLast stays: it identifies the last scheduled appointment of the day and is known from the plan; booking-version snapshots are not supplied.
        - mintime and maxtime stay. The dictionary's daily-wait wording is contradicted by exact identities with the exams in progress (zero with none, both equal SumInProgress with one, min+max equals it with two, no count/sum envelope violations): they are elapsed times of the active exams, not the day's extremes.
        - Operational history is not the current patient's target: no recent-history field changes between arrivals without a completed exam, and linked completed exams support the signed end-minus-scheduled histories; exact updater/default rules remain incompletely documented.
        - Source MAE is deliberate in the author challenge and paper comparisons, per facility. We score per-visit MAE in each window and the equal mean of the nine window scores (Myunghwan, 2026-10-28), not an official source aggregation. The author code labels an RMSE calculation MSE; our RMSE uses the standard definition.
        - All source negatives, repeated operational states and missing values remain.
    """
    target = "Wait"
    problem_type = "regression"
    metric = Metric.source(
        "mae",
        original="Mean absolute error in minutes, evaluated separately for source facilities.",
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
        the real clock for all facilities, so the order is real time; a window is about six to seven weeks of the shifted
        calendar, not a calendar-based horizon. No held-out-facility or new-patient guarantee is asserted.
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
