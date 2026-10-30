"""Approximate scene-based injury prediction from Chicago's police crash release."""

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
    TemporalSplits,
)
from data_foundry.v2.splits import sample_temporal_splits


class ChicagoTrafficCrashes(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What is the most serious police-recorded injury in this crash?",
        use_case=(
            "An emergency-response analyst estimates injury severity from crash and road conditions to help assess response "
            "needs. Finalized police reports approximate those facts without reconstructing their timely availability."
        ),
        row="One CPD-recorded Chicago crash before October 2026; early coverage is partial and citywide coverage starts in September 2017.",
        predicted=(
            "The most severe injury among people involved: fatal, incapacitating, nonincapacitating, reported but not "
            "evident, or no indication. This is an officer-recorded classification, potentially amended later, not a fixed medical follow-up."
        ),
        known="Recorded crash conditions: crash hour and location, weather, lighting, road surface, traffic controls, posted speed, initial collision type, units involved and sparse scene flags; initial availability of finalized values is not verified.",
        split="Nine later three-month crash cohorts are tested against expanding earlier history notified before each quarterly refit; labels are from the final snapshot.",
        fit="approximate",
        fit_reason=(
            "Myunghwan accepts finalized records as a closer-to-fact approximation, rather than timely initial-call information. "
            "Per-field availability and historical injury-label versions are unavailable; operational dispatch performance remains unvalidated."
        ),
        changes="We exclude reporting activity, injury/damage outcomes, investigation judgments and identifiers; retain five physical-condition fields by curator direction with their measured recording risk, harmonize crash time to hours and retain all five source injury classes.",
    )
    unique_name = "chicago_traffic_crashes_1m"
    version_of = "chicago_traffic_crashes"
    version_comment = "Temporal train sides above 1M rows are sampled by the shared fixed-seed protocol after notification eligibility. The returned frame contains only rows used by a split; test sides retain their cleaned original event-time cohorts."
    year = "2017"
    domain = "social science"
    source = "GOV Website"
    source_url = "https://data.cityofchicago.org/Transportation/Traffic-Crashes-Crashes/85ca-t3if"
    license = "See Terms of Use (City of Chicago Data Portal)"
    data_tags = ("Spatial",)
    download_description = """
        Download the official CSV export to local-data-warehouse/chicago_traffic_crashes/crashes.csv:
        https://data.cityofchicago.org/api/views/85ca-t3if/rows.csv?accessType=DOWNLOAD
        The inspected snapshot was acquired on 2026-10-29. Preserve its acquisition receipt and hash;
        the live portal can amend historical records, so downloading again need not reproduce those bytes.
    """
    bibtex = r"""
        @misc{chicago_crashes,
          author = {{City of Chicago, Chicago Police Department}},
          title = {Traffic Crashes - Crashes},
          year = {2017},
          howpublished = {\url{https://data.cityofchicago.org/Transportation/Traffic-Crashes-Crashes/85ca-t3if}}
        }
    """
    target = "most_severe_injury"
    problem_type = "multiclass_classification"
    metric = Metric.fallback(
        reason="The original City portal, field dictionary and linked SR1050 manual define a crash-report release, not a scored prediction competition or a single defining model-selection metric. Use multiclass log loss for the five-class probability task approved for investigation."
    )
    accepted_check_warnings = {
        "dataset_missing_value_label": "DEVICE_CONDITION=MISSING denotes a physically absent traffic-control device, distinct from UNKNOWN and NO CONTROLS in the official IDOT dictionary; preserve its source meaning.",
    }
    temporal = Temporal(on="crash_date", horizon=3, horizon_unit="months")
    splits_comment = """
        Nine consecutive three-month windows, newest first, on event time CRASH_DATE, with expanding earlier history. Each train side above one million rows is capped by the native fixed-seed temporal sampling protocol; test sides remain below 500,000 rows.
        October 2026 is excluded because the source snapshot ends within that month; the newest test is July-September 2026.
        Training requires DATE_POLICE_NOTIFIED strictly before the actual calendar-quarter start and not before the
        recorded event. This intermediate timestamp is removed before the model frame is returned. The eligibility
        filter precedes the shared fixed-seed, class-stratified 1M train/500k test sampling protocol. Source event
        timestamps determine cohorts; only the returned event-time predictor is floored to whole hours for every row.
        The three-month horizon is an evaluation/refit cadence, not a medical outcome window.
        Locations can recur across time; this is not unseen-location evaluation. No dated report or injury-label availability
        history is provided, so label availability at historical refits cannot be reproduced exactly. No fabricated availability
        date or claim that a fixed gap solves that limitation is made.
    """
    curation_comments = """
        We start with the original City's 2026-10-29 bulk CSV export, not a Kaggle re-upload.

        - Prediction point: an approximate scene-based injury assessment using underlying crash and road facts, before using the injury classification itself. On 2026-10-29 Myunghwan accepted closer-to-fact finalized information rather than reconstructing timely initial-call availability. Later administrative/reporting activity, injury consequences and outcome encodings remain excluded; Myunghwan accepted this exact approximate task for shipping on 2026-10-29; build and repository integration are separate steps.
        - Exception to SPLIT-10 (2026-10-29, Myunghwan): accept final-snapshot police injury labels as a reasonable retrospective approximation because no historical label versions or amendment times are available. Serves P3/USE-8: faithfully state the accepted approximate task rather than fabricate a maturation gap. Strict notification eligibility remains; this does not reproduce labels available at historical refits or use the training-floor rationale of alfa/lending.
        - CRASH_DATE is the event timestamp: its original precision defines cohorts and source-copy checks; the returned datetime predictor is floored to whole hours for every row. Exact-hour recording differed by injury even within report type (on-scene: 8.21% injured versus 13.07% uninjured; desk: 18.86% versus 25.09%). The paired three-quarter diagnostic removed minute information for 889,076 rows without moving any quarter; mean log loss changed from 0.550174 to 0.550105. This harmonizes minute precision, not event-time accuracy. DATE_POLICE_NOTIFIED is notification time, used only as intermediate training-eligibility metadata and excluded from predictors together with delays. CRASH_DATE_EST_I is a later reporting flag, not a timestamp. The source carries no timezone offset; no UTC conversion is assumed.
        - Injury counts, CRASH_TYPE and DAMAGE are outcome information; REPORT_TYPE, photo/statement flags, and primary/secondary contributory causes are reporting or investigation information and are excluded. INTERSECTION_RELATED_I is a causal judgment, not an at-intersection indicator. HIT_AND_RUN_I is withheld as post-collision flight/aid behavior rather than an initial physical condition; no injury-caused mechanism is claimed proved for that flag.
        - Keep underlying trafficway, posted speed, location and initial-collision facts as approximate candidates. FIRST_CRASH_TYPE follows the manual's first damage/injury event and sequence rules; it is not necessarily a raw caller observation. The bulk header NOT_RIGHT_OF_WAY_I corresponds to API alias private_property_i, meaning contact beginning outside the public right-of-way. Blank Y/N fields remain missing, not inferred N.
        - Exclude LANE_CNT, ALIGNMENT and ROAD_DEFECT from the initial recipe: the IDOT March 2011 dictionary, printed elements 80, 81 and 84 (PDF pages 40 and 43), requires them for injury/towing reports but not minor drive-away reports. Their underlying road facts preexist injury, but outcome-dependent collection makes the stored fields unsafe stand-ins without reconstruction. This is a source-based precaution, not a claim that every value is demonstrably leaked.
        - POSTED_SPEED_LIMIT has the same historical N/Y requirement (element 50); omission from the earlier sibling sweep was corrected. Recent matched zero-speed rates were 0.0755% without injury versus 0.0931% with injury, weakening that specific injury-dependent default concern. All 66 source values of 99 occur in 2015, but no verified sentinel definition supports replacing them. Keep speed with this historical-code uncertainty; the check does not validate every earlier or nonzero default. Myunghwan accepted keeping posted speed as implemented on 2026-10-29; no source-value replacement or reconstruction was requested.
        - Potential leak, kept on purpose: WEATHER_CONDITION, LIGHTING_CONDITION, ROADWAY_SURFACE_COND, TRAFFIC_CONTROL_DEVICE and DEVICE_CONDITION describe crash-time physical conditions. Myunghwan directed their inclusion on 2026-10-29 after reviewing the availability evidence. In three 2026 held-out quarters (83,644 crashes), five recorded/unknown flags alone give any-injury AUC 0.555; adding them to the other 16 inputs improves mean five-class log loss from 0.554416 to 0.551600, versus 0.550105 with the five actual fields. This model-specific association does not establish injury-caused collection or prove the fields safe. Original context-matched unknown-rate gaps shrink after report-type/delay stratification, which may condition on the reporting mechanism and does not establish causal clearance. The earlier panel recommended exclusion under LEAK-10/38; retention is the curator-directed choice for this approximate task, not a claim of compliance with that conditional-fill criterion or a standing amendment. Initial availability, report completion and revision history are unverified. Revisit if dated snapshots or field-specific evidence show injury-driven recording or changed physical values. Preserve unknowns without imputation or complete-case selection. DEVICE_CONDITION=MISSING means a physically absent device and NO CONTROLS is a valid recorded condition; neither means an unavailable cell.
        - Remove exact source copies using every original field except CRASH_RECORD_ID, IDOT_CONTROL_NO and REPORT_TYPE; keep the first source-order representative. The inspected full export has 63 extra copies on that key, 36 already matching even with the control number included. The broader key removes 26 additional rows from the labeled pre-October cohort; raw rows remain preserved. Distinct administrative IDs alone do not establish independent events. Do not deduplicate on the reduced or hour-rounded predictor vector: some source-distinct crashes coincide after context is removed, and conflicting reduced profiles can be genuine label ambiguity. The remaining reused control number with different time/location is not collapsed. Missing labels and the unfinished October cohort are excluded; classes are not merged. Partial early coverage does not establish citywide incident rates.
        - CRASH_HOUR, CRASH_DAY_OF_WEEK and CRASH_MONTH are redundant components of CRASH_DATE. LOCATION repeats latitude/longitude; report identifiers are not predictors. Coordinate zeros are made missing because they cannot identify a Chicago crash location. Unknown/unreported categorical codes become missing; no outcome-based imputation is used.
        - Retrospective officer judgments, outcome-dependent reporting completeness and historical label amendments remain limitations. The source permits more complete forms for injury/towing and amendment after later deaths (SR1050 manual, printed pages 2-3 and 9). The approximate fit does not waive feature-specific leakage checks or establish deployment validity.
    """
    candidate_columns = (
        "crash_date",
        "posted_speed_limit",
        "weather_condition",
        "lighting_condition",
        "roadway_surface_cond",
        "traffic_control_device",
        "device_condition",
        "first_crash_type",
        "trafficway_type",
        "not_right_of_way_i",
        "street_no",
        "street_direction",
        "street_name",
        "beat_of_occurrence",
        "dooring_i",
        "work_zone_i",
        "work_zone_type",
        "workers_present_i",
        "num_units",
        "latitude",
        "longitude",
    )
    numeric_columns = ("posted_speed_limit", "street_no", "num_units", "latitude", "longitude")

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "crashes.csv", dtype="string[pyarrow]")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.rename(columns=str.lower)
        # Source-copy identity precedes feature removal or time-precision harmonization.
        source_key = [c for c in df.columns if c not in {"crash_record_id", "idot_control_no", "report_type"}]
        df = df.drop_duplicates(subset=source_key)
        # Notification stays only until _make_splits; it never reaches predictors or metric inputs.
        df = df.loc[df[self.target].notna(), [*self.candidate_columns, "date_police_notified", self.target]].copy()
        df["crash_date"] = pd.to_datetime(df["crash_date"], format="mixed", errors="raise")
        df["date_police_notified"] = pd.to_datetime(df["date_police_notified"], format="mixed", errors="raise")
        df = df.loc[df["crash_date"] < pd.Timestamp("2026-10-01")].copy()
        for c in self.numeric_columns:
            df[c] = pd.to_numeric(df[c], errors="raise").astype("float64")
        for c in ("latitude", "longitude"):
            df.loc[df[c].eq(0), c] = float("nan")
        for c in sorted(set(self.candidate_columns) - set(self.numeric_columns) - {"crash_date"}):
            df[c] = df[c].replace({"UNKNOWN": pd.NA, "NOT REPORTED": pd.NA, "UNABLE TO DETERMINE": pd.NA})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=sorted(set(self.candidate_columns) - set(self.numeric_columns) - {"crash_date"}),
            datetime=("crash_date", "date_police_notified"),
        )

    def _make_splits(self, df: pd.DataFrame) -> SplitPlan:
        """Original event-time cohorts; notification eligibility before native row-budget sampling."""
        windows = TemporalSplits(window=3, unit="months", n_windows=9, min_train_fraction=0.5).splits(df, "crash_date")
        event = df["crash_date"]
        notified = df["date_police_notified"]
        eligible_order = notified.ge(event)
        splits = {}
        evidence = []
        for split, folds in windows.items():
            train, test = folds[0]
            start = event.iloc[test].min().to_period("Q").start_time
            train = np.asarray(train)
            known = (notified.lt(start) & eligible_order).iloc[train].to_numpy()
            evidence.append(
                {
                    "quarter start": start,
                    "prior rows": len(train),
                    "not yet notified": int(notified.iloc[train].ge(start).sum()),
                    "notification before event": int((~eligible_order.iloc[train]).sum()),
                    "eligible train pool": int(known.sum()),
                    "test rows": len(test),
                }
            )
            splits[split] = {0: (train[known].tolist(), test)}
        self._eligibility_evidence = pd.DataFrame(evidence)
        model = df.drop(columns="date_police_notified").copy()
        model["crash_date"] = model["crash_date"].dt.floor("h")
        model, splits, trimmed = sample_temporal_splits(
            model,
            splits,
            stratify_on=self.target,
            random_state=self.SPLIT_RANDOM_STATE,
        )
        if not trimmed:
            raise ValueError("No eligible split exceeds the budget; reassess the _1m version.")
        return SplitPlan(df=model, splits=splits)

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        source = raw.rename(columns=str.lower)
        return [
            Decision(
                title="Keep all five police injury classes",
                why="Source classes remain distinct; missing labels are not interpreted as no injury. October 2026 is not a complete cohort.",
                evidence=pd.DataFrame(
                    {
                        "source": source[self.target].value_counts(dropna=False),
                        "retained": df[self.target].value_counts(dropna=False),
                    }
                ).fillna(0),
            ),
            Decision(
                title="Filter measurable notification unavailability before each refit",
                why="Notification must precede refit and cannot precede its recorded event. It is eligibility metadata only; this does not establish injury-label finalization or amendment availability.",
                evidence=self._eligibility_evidence,
            ),
        ]
