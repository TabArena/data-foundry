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

INJURY_SEVERITY = (
    "NO INDICATION OF INJURY",
    "REPORTED, NOT EVIDENT",
    "NONINCAPACITATING INJURY",
    "INCAPACITATING INJURY",
    "FATAL",
)


class ChicagoTrafficCrashes(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What is the most serious police-recorded injury in this crash?",
        use_case=(
            "A city road-safety analyst estimates, for each reported crash, the probability of each police injury level "
            "from the recorded crash and road facts, to estimate the expected number of people killed or seriously "
            "injured at each site and rank sites for countermeasures."
        ),
        row="One CPD-recorded Chicago crash before October 2026; from September 2017, when citywide coverage starts.",
        predicted=(
            "The most severe injury among people involved: fatal, incapacitating, nonincapacitating, reported but not "
            "evident, or no indication. This is an officer-recorded classification, potentially amended later, not a fixed medical follow-up."
        ),
        known=(
            "The finalized report's crash and road facts, without its injury, damage or reporting fields: crash hour and "
            "location, posted speed, trafficway type, first collision type, units involved, and sparse work-zone and "
            "private-property flags."
        ),
        split=(
            "Nine later three-month crash cohorts are tested against expanding earlier history that ends one month "
            "before each window and was notified before each quarterly refit; labels are from the final snapshot."
        ),
        fit="approximate",
        fit_reason=(
            "The police injury level stands in for the serious injuries the analyst counts: trauma-registry linkage finds "
            "police reports catch about half of them (Traffic Injury Prevention 2024), and the share of 'reported, not "
            "evident' injuries steps up in late 2023. Lane count, alignment, road defects, weather, lighting, surface and "
            "traffic control are dropped because injury reports record them more completely, though an analyst could "
            "take them from road inventories."
        ),
        changes=(
            "We exclude reporting activity, injury/damage outcomes, investigation judgments, identifiers, the road and "
            "condition fields whose recording follows the injury and the door-opening flag; start at September 2017; "
            "floor crash time to whole hours."
        ),
    )
    unique_name = "chicago_traffic_crashes"
    year = "2026"  # the snapshot we pin; the source grows over time (PROV-9)
    domain = "social science"
    source = "GOV Website"
    source_url = "https://data.cityofchicago.org/Transportation/Traffic-Crashes-Crashes/85ca-t3if"
    license = "See Terms of Use (City of Chicago Data Portal)"
    data_tags = ("Spatial",)
    download_description = """
        Download the official CSV export to local-data-warehouse/chicago_traffic_crashes/crashes.csv:
        https://data.cityofchicago.org/api/views/85ca-t3if/rows.csv?accessType=DOWNLOAD
        The pinned snapshot is the export downloaded on 2026-11-04 (1,109,972 rows; sha256
        4bf63b07d869d992887c08d70bc017a357f731e6bf563dd6098546417b29027b). The 2026-10-29 bytes are no longer kept.
        The live portal amends historical records, so downloading again need not reproduce those bytes, and the
        export URL stops working on 2026-12-22.
    """
    bibtex = r"""
        @misc{chicago_crashes,
          author = {{City of Chicago, Chicago Police Department}},
          title = {Traffic Crashes - Crashes},
          year = {2026},
          howpublished = {\url{https://data.cityofchicago.org/Transportation/Traffic-Crashes-Crashes/85ca-t3if}}
        }
    """
    target = "most_severe_injury"
    problem_type = "multiclass_classification"
    metric = Metric.fallback(
        reason="The original City portal, field dictionary and linked SR1050 manual define a crash-report release, not a scored prediction competition or a single defining model-selection metric. Use multiclass log loss for the accepted five-class probability task. On the newest window about 35% of the loss is in the 'reported, not evident' class and about 10% in incapacitating plus fatal; skill over the class prior is 18.0% on all rows against 11.8% on on-scene reports alone (one quick LightGBM on most of the shipped inputs, 2026-11-05)."
    )
    accepted_check_warnings = {
        "splits_rows_unused": (
            "One crash is notified before its recorded event, so no training side takes it, and it falls before the "
            "oldest test window; it stays in the frame unused rather than being dropped by its timestamps."
        ),
    }
    temporal = Temporal(on="crash_date", horizon=3, horizon_unit="months", gap=1, gap_unit="months")
    splits_comment = """
        Nine consecutive three-month windows, newest first, on event time CRASH_DATE, with expanding earlier history. Training starts on 2017-09-01; no side is sampled.
        October 2026 is excluded because the source snapshot ends within that month; the newest test is July-September 2026.
        Train ends one month before each window (a one-month gap, as zillow_prize): a model refit at a quarter start
        would not yet see the final class of the last month's crashes, since the SR1050 manual lets a report be amended
        when a person dies later (printed pages 2-3 and 9) and a traffic death is counted within 30 days of the crash.
        The source has no label versions or amendment dates. The portal's row field :updated_at bounds the delay: for
        crashes of June-August 2026 the last update is a median 16.1 days after the crash and 99.4% of rows are last
        updated within 30 days; 5 of 32 fatal crashes were updated later (33-102 days); injury shares do not shift
        across the update. Limits: :updated_at changes with any field, not only the label; the bulk reload of
        2026-05-21 hides earlier history; 1,904 older crashes were rewritten in one batch on 2026-11-03.
        lt_vehicle_loan_default_prediction has no gap because there a 30-day gap would leave training sides under
        SPLIT-14's 50% floor and its measured effect was small; here the floor holds and the gap costs 1.0-1.4% of a
        training side.
        Training also requires DATE_POLICE_NOTIFIED strictly before the actual calendar-quarter start and not before the
        recorded event. This intermediate timestamp is removed before the model frame is returned. The event time is
        floored to whole hours in `_clean`, before the rows are sorted by it, and cohorts are drawn on the floored hour
        (window and gap bounds fall on midnight, so no cohort changes); only the check "not notified before the
        recorded event" reads the source minute, through a flag removed with the timestamp (2026-11-05, LEAK-13).
        The windows are calendar quarters only because the data is cut at 2026-10-01; a cut at another month would
        put the notification cutoff before the window start (stricter, still safe).
        The three-month horizon is an evaluation/refit cadence, not a medical outcome window.
        Locations can recur across time; this is not unseen-location evaluation.
        Drift (SPLIT-20, USE-5 open): the share of "REPORTED, NOT EVIDENT" steps from 4.09-4.71% (2022Q1-2023Q3) to
        5.56% in 2023Q4, then 6.07-6.54% (2024Q2-2026Q1) and 6.64-6.74% (2026Q2-Q3, a further rise in desk reports),
        while incapacitating plus fatal falls from about 2.0% to 1.4%; the desk-report share stays at 50-53%. Every test
        window lies after the 2023Q4 step. Its cause (a change in recording practice?) is not known.
    """
    curation_comments = """
        We start with the original City's 2026-11-04 bulk CSV export, not a Kaggle re-upload. Figures marked
        "(2026-10-29)" were measured on the earlier export, whose bytes are no longer kept.

        - Prediction point: a reported crash's finalized crash and road facts, before its injury classification, from which a city road-safety analyst estimates the chance of each injury level to rank sites by expected people killed or seriously injured (2026-11-05; superseded: an approximate scene-based injury assessment for emergency response). On 2026-10-29 Myunghwan accepted closer-to-fact finalized information rather than reconstructing timely initial-call availability (superseded 2026-11-05 for the actor: finalized records are what the analyst works from, so they are no longer the gap). Later administrative/reporting activity, injury consequences and outcome encodings remain excluded; Myunghwan accepted this exact approximate task for shipping on 2026-10-29; build and repository integration are separate steps.
        - CC (2026-11-05, Lennart): the use case is a city road-safety analyst who ranks sites by expected people killed or seriously injured (issue 7, A; USE-1, USE-9: the blind reviewer named the same actor without our notes). It supersedes the emergency-response framing Myunghwan accepted on 2026-10-29: 50.9% of the rows are desk reports nobody was dispatched to (5.3% injured against 25.5% on scene). Every row stays. The fit stays approximate: police reports catch about half of serious injuries in trauma-registry linkage, the 'reported, not evident' share steps up in 2023Q4, and the road facts recorded more completely for injury crashes are dropped.
        - Late labels (SPLIT-10; 2026-11-04, Lennart): a one-month gap between train and test, as zillow_prize. A report can be amended after a later death, and a traffic death counts within 30 days of the crash, so a refit at a quarter start would see the newest month's crashes in a lower class than the final snapshot gives. The source has no label versions or amendment times; the portal's :updated_at field (any field, not only the label) puts 99.4% of last updates within 30 days of the crash (median 16.1 days, crashes of June-August 2026), with 5 of 32 fatal crashes updated later, at 33-102 days. Labels stay those of the final snapshot. A month is 1.0-1.4% of a training side, and the strict notification eligibility remains.
        - CC (2026-11-05, Lennart): the one-month gap stays (issue 11, as implemented; SPLIT-10 as amended 2026-11-04: the gap is about the label's delay). It covers 99.4% of last updates; two months would cover 4 of the 5 late fatal updates and cost about 1% of each training side.
        - CC (2026-11-05, Lennart): the step in 'reported, not evident' in 2023Q4 is accepted as drift, with the shares in `splits_comment` (issue 8, as implemented; USE-5 fails only when the label is shown to be another quantity, SPLIT-20).
        - CRASH_DATE is the event timestamp: its original precision defines source-copy checks, and it is floored to whole hours for every row in `_clean`, before the framework sorts the rows by it (cohorts: original precision until 2026-11-05, now the floored hour, the same windows). Exact-hour recording differed by injury even within report type (on-scene: 8.21% injured versus 13.07% uninjured; desk: 18.86% versus 25.09%). The paired three-quarter diagnostic (2026-10-29, 21-input recipe) removed minute information for 889,076 rows without moving any quarter; mean log loss changed from 0.550174 to 0.550105. This harmonizes minute precision, not event-time accuracy. DATE_POLICE_NOTIFIED is notification time, used only as intermediate training-eligibility metadata and excluded from predictors together with delays. CRASH_DATE_EST_I is a later reporting flag, not a timestamp. The source carries no timezone offset; no UTC conversion is assumed.
        - CC (2026-11-05, Lennart): `crash_date` is floored in `_clean`, not in `_make_splits` (issue 9, B; LEAK-13, as hepatitis_c_prediction and gallstone_disease). The framework sorts the rows by the time column between the two steps, so the floor in `_make_splits` left each hour in minute order, and a row's rank in its hour lowered log loss by 0.00098 (0.00008 to 0.00202, on all 9 splits). Each hour now keeps the content order, the windows are the same, and the one crash notified before its recorded time stays unused through a flag computed from the source minute.
        - Injury counts, CRASH_TYPE and DAMAGE are outcome information; REPORT_TYPE, photo/statement flags, and primary/secondary contributory causes are reporting or investigation information and are excluded. INTERSECTION_RELATED_I is a causal judgment, not an at-intersection indicator. HIT_AND_RUN_I is withheld as post-collision flight/aid behavior rather than an initial physical condition; no injury-caused mechanism is claimed proved for that flag.
        - Keep underlying trafficway, posted speed, location and initial-collision facts as approximate candidates. FIRST_CRASH_TYPE follows the manual's first damage/injury event and sequence rules; it is not necessarily a raw caller observation. The bulk header NOT_RIGHT_OF_WAY_I corresponds to API alias private_property_i, meaning contact beginning outside the public right-of-way. Blank Y/N fields remain missing, not inferred N.
        - Exclude LANE_CNT, ALIGNMENT and ROAD_DEFECT from the initial recipe: the IDOT March 2011 dictionary, printed elements 80, 81 and 84 (PDF pages 40 and 43), requires them for injury/towing reports but not minor drive-away reports. Their underlying road facts preexist injury, but outcome-dependent collection makes the stored fields unsafe stand-ins without reconstruction. This is a source-based precaution, not a claim that every value is demonstrably leaked.
        - POSTED_SPEED_LIMIT has the same historical N/Y requirement (element 50); omission from the earlier sibling sweep was corrected. A zero speed is 0.548% of uninjured against 0.280% of injured crashes in the frame, but 39% of zeros are parking-lot crashes and within parking lots the rates are 3.00% against 2.80%: a zero mostly marks a place without a posted limit, a scene fact, not a field left blank on minor reports. The 66 source values of 99 all fall in 2015, before the frame starts. The check does not validate every nonzero default. Myunghwan accepted keeping posted speed as implemented on 2026-10-29; no source-value replacement or reconstruction was requested.
        - WEATHER_CONDITION, LIGHTING_CONDITION, ROADWAY_SURFACE_COND, TRAFFIC_CONTROL_DEVICE and DEVICE_CONDITION are dropped (LEAK-10; Lennart, 2026-11-04), as LANE_CNT, ALIGNMENT and ROAD_DEFECT: on the three newest windows they lower the five-class log loss by 0.0039, and flags saying only whether each was recorded win back 0.0028 of that (72%), so most of their gain is whether the field was filled in. Without them the task still rests on the collision type, the units involved, the hour and the road layout (log loss 0.4960 against the class prior's 0.6140; superseded 2026-11-05: 0.4962 against 0.6130 on the shipped 15 inputs from 2017-09, the same LightGBM, mean of the three newest windows).
        - CC (2026-11-05, Lennart): `dooring_i` is dropped (issue 10, B; LEAK-10 through LEAK-38's measured clause, as the five fields). Within a crash type, injured crashes have it filled in 4-8 times as often, though the 'N' value alone shows no consistent difference by outcome; the drop costs 0.00011 log loss (0.49609 to 0.49620, three newest windows). If the LEAK-38 amendment opened on 2026-11-05 takes the any-source scope, `dooring_i` falls under it too.
        - Training starts on 2017-09-01, when citywide coverage starts (SPLIT-20; Lennart, 2026-11-04): before it, 7.3% of crashes have any injury against 15.3% after, with 4,000-7,000 crashes a month against 9,000-10,000. It leaves the score unchanged (0.49609 against 0.49600 from 2013, on the 16 inputs of 2026-11-04; 0.49620 against 0.49610 on the shipped 15 inputs, 2026-11-05) and costs about 99,100 rows per training side. No training side then exceeds one million rows, so the task ships unsampled, not as a `_1m` version.
        - Remove exact source copies using every original field except CRASH_RECORD_ID, IDOT_CONTROL_NO and REPORT_TYPE; keep the first source-order representative. The full export has 63 extra copies on that key (both exports); on the 2026-10-29 export 36 already matched even with the control number included, and the broader key removed 26 additional rows from the labeled pre-October cohort; raw rows remain preserved. Distinct administrative IDs alone do not establish independent events. Do not deduplicate on the reduced or hour-rounded predictor vector: some source-distinct crashes coincide after context is removed, and conflicting reduced profiles can be genuine label ambiguity. The remaining reused control number with different time/location is not collapsed. Missing labels and the unfinished October cohort are excluded; classes are not merged. Partial early coverage does not establish citywide incident rates.
        - CRASH_HOUR, CRASH_DAY_OF_WEEK and CRASH_MONTH are redundant components of CRASH_DATE. LOCATION repeats latitude/longitude; report identifiers are not predictors. Coordinate zeros are made missing because they cannot identify a Chicago crash location. Unknown/unreported categorical codes become missing; no outcome-based imputation is used.
        - CC (2026-11-05, Lennart): the declared metric (the fallback multiclass log loss over the five police injury classes) is checked and stays as declared.
        - Retrospective officer judgments, outcome-dependent reporting completeness and historical label amendments remain limitations. The source permits more complete forms for injury/towing and amendment after later deaths (SR1050 manual, printed pages 2-3 and 9). The approximate fit does not waive feature-specific leakage checks or establish deployment validity.
    """
    candidate_columns = (
        "crash_date",
        "posted_speed_limit",
        "first_crash_type",
        "trafficway_type",
        "not_right_of_way_i",
        "street_no",
        "street_direction",
        "street_name",
        "beat_of_occurrence",
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
        # Citywide coverage starts in September 2017 (the portal); the earlier, partial years leave (SPLIT-20).
        df = df.loc[
            df["crash_date"].ge(pd.Timestamp("2017-09-01")) & df["crash_date"].lt(pd.Timestamp("2026-10-01"))
        ].copy()
        # The notification check alone reads the source minute; the flag leaves with the timestamp in _make_splits.
        df["notified_before_event"] = df["date_police_notified"].lt(df["crash_date"])
        # Floored here, before the framework sorts the rows by time, so no row order inside an hour keeps the
        # minute (LEAK-13). Window and gap bounds fall on midnight, so no cohort changes.
        df["crash_date"] = df["crash_date"].dt.floor("h")
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
            # The KABCO severity scale, lowest first (CLEAN-25; 2026-11-04, Lennart).
            ordinal={self.target: list(INJURY_SEVERITY)},
        )

    def _make_splits(self, df: pd.DataFrame) -> SplitPlan:
        """Event-time cohorts (the floored hour) with a one-month gap, after notification eligibility; no sampling."""
        windows = TemporalSplits(window=3, unit="months", n_windows=9, min_train_fraction=0.5, gap=1).splits(
            df, "crash_date"
        )
        event = df["crash_date"]
        notified = df["date_police_notified"]
        eligible_order = ~df["notified_before_event"]
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
                    "gap month rows": int((event.ge(start - pd.DateOffset(months=1)) & event.lt(start)).sum()),
                    "prior rows": len(train),
                    "not yet notified": int(notified.iloc[train].ge(start).sum()),
                    "notification before event": int((~eligible_order.iloc[train]).sum()),
                    "eligible train pool": int(known.sum()),
                    "test rows": len(test),
                }
            )
            splits[split] = {0: (train[known].tolist(), test)}
        self._eligibility_evidence = pd.DataFrame(evidence)
        return SplitPlan(df=df.drop(columns=["date_police_notified", "notified_before_event"]), splits=splits)

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
                why="Notification must precede refit and cannot precede its recorded event. It is eligibility metadata only and does not date the injury label; the one-month gap before each window (its rows counted here) stands in for later amendments.",
                evidence=self._eligibility_evidence,
            ),
        ]
