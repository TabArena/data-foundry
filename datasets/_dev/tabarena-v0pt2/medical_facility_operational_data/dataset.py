"""All-facility imaging delay/wait prediction from the authenticated author workbook."""

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


class MedicalFacilityOperationalData(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What delay or waiting time, in minutes, will this patient's imaging visit have at this facility?",
        use_case="At patient arrival, imaging operations staff estimate exam-start delay or waiting time using the current workflow and known appointment plan.",
        row="One of 130,431 visits across all four source worksheets F1-F4, with facility identity as categorical context.",
        predicted="The original Wait in minutes: signed exam-start minus scheduled time for F1-F3, arrival-to-start waiting for F4. Negative scheduled delays and zero waits remain.",
        known="Facility, current queue/resource state, completion-driven histories, published time features and planned appointment demand. Exact updater and estimator fitting provenance remain incomplete.",
        split="Nine expanding windows in the common anonymized source event order; training arrivals and exam starts precede each test start. Common-day consistency supports this approximate ordering, without proving intra-day clock synchronization or real calendar cadence.",
        changes="Stack all four source sheets and add facility. Remove artificial timestamps from model inputs, retain legitimate scheduled demand and elapsed active-exam extrema, and mask the unavailable F4 last-visit flag. Retain ordinary per-visit MAE in each test window and the standard equal mean of nine window scores after curator review of facility imbalance.",
        fit="approximate",
        fit_reason="The source defines real operational delay/wait tasks and the workbook is authenticated. Ordering and feature-estimator provenance have explicit limits. The curator accepted the approximate source-order split and retained ordinary MAE; final scientific inclusion is approved by Myunghwan.",
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
        Read all four worksheets F1-F4 and preserve their facility identity. Counts differ from the related PLOS analytical cohort; exact cohort equivalence is not claimed. Dataverse retrieval returned HTTP 403, but primary author workbook identity is verified independently.
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
        - Final curator verdict (2026-10-28, Myunghwan): "ship this". Accept all four facilities, 130,431 visits, 88 predictors including facility, original signed delay/wait targets, the accepted nine approximate source-order windows and ordinary MAE with equal window averaging. Earlier notes below preserve the review history. Source-clock, calendar-cadence, estimator-fitting and booking-lineage limitations remain disclosed.
        - Curator decision (2026-10-28, Myunghwan): "Is MAE the main metric from the original task? If so, our current imbalance is somewhat acceptable." The primary author explicitly uses MAE. Retain the implemented per-visit MAE and proposed equal mean of nine test-window MAEs; accept the measured facility imbalance. This resolves scoring, not final inclusion.
        - Curator decision (2026-10-28, Myunghwan): "accept this split". Accept the exact nine common source-event-order windows across all four facilities, observed training labels and tied arrivals, with the disclosed synchronization/calendar limits. This accepts the approximation; it does not verify a real shared clock or settle scoring or final inclusion.
        We start with all four worksheets F1-F4 of the authenticated author workbook WaitData.Published.xlsx.

        - Curator scope: all-facility prediction with facility as meaningful categorical context. The earlier F4-only definition did not fulfill the saved instruction. All 130,431 source visits and original Wait values are retained; no final ship is inferred from this redo.
        - Prediction point: arrival, before the imaging exam starts. F1-F3 Wait is signed exam-start minus scheduled time; F4 Wait is exam-start minus arrival. All targets agree with source timestamp diagnostics within one minute. Keep valid negatives and zeros, without log transform, clipping or outcome rescaling.
        - Facility is the source worksheet ID, not a fabricated patient/entity ID. Use neutral F1-F4 labels: the author code and a separate PLOS cohort disagree on F1/F2 modality labels. All groups remain represented; no unseen-facility generalization is claimed.
        - Stack the union of published columns; absent facility-specific fields remain structurally missing, never fabricated zeros. Preserve AvgDelayForDay and AvgWaitForDay as separate source fields. Numeric counts stay numeric; facility, flags, source weekday and month are categorical.
        - Remove all three artificial timestamp columns from model inputs. Arrival/start timestamps survive only until ordering and label-availability construction. A dense global arrival-order rank is the temporal variable; no real dates, time gaps or calendar features are reconstructed from fictitious timestamps.
        - Across 413 artificial scheduled days represented by all facilities, source DayOfYear, Month and DayOfWeek agree without conflict. Their common weekday displacement corroborates common-day alignment. The source permits sorting, but exact intra-day cross-facility alignment and authentic calendar cadence remain unverified; the global-order candidate is approximate and explicitly reviewed.
        - Planned demand is allowed at arrival: scheduled counts in the following 30/60 minutes, next-slot/hour bookings, and source expected completion/delay estimates are not realized future outcomes merely because they refer to later appointments. Exact expected-duration fitting lineage remains unverified without demonstrated future-label fitting.
        - Retain IsLast for scheduled F1-F3: it exactly identifies the last scheduled appointment time and can be known from the plan; source booking-version snapshots are not supplied. Mask it for walk-in F4, whose pseudo-schedule/last-visit availability is not established. IsFirst and current-state flags are retained with the source operational context.
        - Restore mintime and maxtime in all facilities. The dictionary's daily-wait wording is contradicted by exact current active-exam elapsed-state identities: zero with no exams, both equal SumInProgress with one exam, min+max equals that sum with two, and no count/sum envelope violations in all 130,431 visits. Stable-population increments also track elapsed minutes; F4 has 11/9 small min/max transition residuals among 10,214 cases. No full-day target-extrema interpretation or future leak is inferred.
        - Operational history is not the current patient's target. Across all facilities no recent-history field changes during same-day transitions with unchanged completion count; independently linked completed exams support signed end-minus-scheduled histories. Daily source target means match already-begun visits outside source missing-calendar rows; the three recent-window AvgWaitLastW fields instead average already-begun arrival-to-start waits in every facility, not the signed scheduled target. Exact updater/default/reset rules remain incompletely documented, so this supports availability without claiming complete generator reconstruction.
        - Source MAE is deliberate in the author challenge and paper comparisons. Its source evaluates facilities separately and does not prescribe a pooled all-facility scorer. The curator conditionally accepted the observed imbalance if MAE was the original objective; the author challenge confirms this. Retain ordinary per-visit MAE within each window and the standard equal mean across nine windows. This combined weighting is the retained benchmark composition, not an official source aggregation. Equal-window averaging differs from pooling all held-out visits; facility-level errors remain diagnostics. The author's code historically labels an RMSE calculation MSE; our reported RMSE and squared errors use their standard definitions.
        - All source negatives, repeated operational states and missing values remain unless a demonstrated defect requires repair. The old F4-only model results are historical for that feature inventory; the restored extrema and all-facility task receive fresh diagnostics.
    """
    target = "Wait"
    problem_type = "regression"
    metric = Metric.source(
        "mae",
        original="Mean absolute error in minutes, evaluated separately for source facilities.",
        reference="https://medicalanalytics.group/operational-data-challenge/",
        definition="Source MAE formula in minutes on all held-out visits within each window, summarized by the standard equal mean of nine window MAEs. Retained after Myunghwan's 2026-10-28 conditional acceptance of the observed imbalance and verification of deliberate source MAE. The source does not prescribe cross-facility or across-window weighting; no facility normalization is applied.",
    )
    temporal = Temporal(on="arrival_order", horizon=7300, horizon_unit="steps")
    splits_comment = """
        Curator-accepted approximate global source-event-order evaluation, newest window first. Start after at least half of all visits
        have both arrived and begun their exams; divide the remaining distinct arrival instants into nine windows,
        keeping timestamp ties intact. Every train arrival and begin precedes its test start. All facilities occur in
        every train/test, with their actual support reported; the minimum mature train is 65,217/130,431 (50.00115%).
        About 7,300 source events is a typical cohort width, not a real calendar forecast horizon or label-maturity gap.
        Shared-day calendar-feature consistency supports common anonymous ordering, without proving intra-day clock
        equivalence or the paper's calendar cadence. No held-out-facility or new-patient guarantee is asserted.
    """
    accepted_check_warnings = {}

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        tables = pd.read_excel(
            raw_dir / "WaitData.Published.xlsx", sheet_name=["F1", "F2", "F3", "F4"], engine="calamine"
        )
        return pd.concat([table.assign(facility=name) for name, table in tables.items()], ignore_index=True, sort=False)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.copy()
        df["arrival_order"] = df["x_ArrivalDTTM"].rank(method="dense").astype("int64") - 1
        df.loc[df["facility"].eq("F4"), "IsLast"] = np.nan
        return df.drop(columns=["x_ScheduledDTTM"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=(
                "facility",
                "IsLast",
                "IsFirst",
                "NoneInProgress",
                "NoneCompleted",
                "NoneInLine",
                "DayOfWeek",
                "Month",
            ),
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
                "All source facilities and target meanings",
                "Preserve original signed scheduled delay for F1-F3 and nonnegative arrival waiting for F4, with facility as context. Ordinary per-visit MAE and standard equal-window averaging are retained after review of facility contributions.",
                pd.DataFrame(rows).set_index("facility"),
            )
        ]
