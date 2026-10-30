"""Sendy: recorded order-placement-to-arrival duration, proposed revised task."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary


class SendyLogisticsChallenge(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="When an order is placed, how many seconds until its recorded delivery arrival?",
        use_case="Sendy customer-communication and delivery-planning staff estimate the customer's total wait at order placement, to communicate an expected arrival and plan deliveries.",
        row="One of 21,199 retained labelled completed express motorbike delivery orders in Nairobi from the 2019 Sendy challenge, restricted to recorded total duration at most 24 hours and straight-line average speed at most 100 km/h. Cancelled, failed and longer-duration orders are not evaluated.",
        predicted="Seconds from order placement to recorded destination arrival, including dispatch, pickup and delivery. This revises the contest's pickup-to-arrival target.",
        known="Customer identifier, platform and customer type, placement day/weekday/clock, endpoint coordinates and source weather matched to placement. Source distance is retained following curator review and measured consistency checks; its calculation and recording time remain unverified. No rider identity, later event information or rider-table summaries are predictors.",
        split="Three repeats of three random folds over the same release, with recurring customers permitted. Full dates are absent; future-period performance and historical label availability cannot be tested.",
        changes="Reconstruct total duration from placement and arrival calendar/clock fields; exclude recorded totals above 24 hours and straight-line average speeds above 100 km/h, as approved by Myunghwan. This removes two long orders and zero additional speed cases. Remove later events, rider identity, original target, order number and constant vehicle type. Parse only placement time as seconds after midnight.",
        fit="approximate",
        fit_reason="Evaluation is limited to an outcome-selected completed-order cohort and comparable orders in this release; missing full dates and unsupported Order No chronology prevent future-period testing. Recorded arrival is not independently validated, and source distance timing and exact weather alignment remain undocumented.",
    )
    unique_name = "sendy_logistics_challenge"
    year = "2019"
    domain = "business & marketing"
    source = "Zindi"
    source_url = "https://zindi.world/competitions/sendy-logistics-challenge/data"
    license = "Zindi competition terms; no standalone open-data licence specified"
    data_tags = ("ForcedIIDFromTemporal", "Anonymized", "Spatial")
    download_description = """
        Sign in to Zindi, obtain the Sendy Logistics Challenge files from
        https://zindi.world/competitions/sendy-logistics-challenge/data and extract the official archive into
        local-data-warehouse/sendy_logistics_challenge/. This definition reads Train.csv.
        Original Train.csv SHA256: df36319528b756bb015010eabc3eaf9179f75d6b2222402f7772f88e83017c3c.
        Preserve Test.csv, Riders.csv, VariableDefinitions.csv and the archive manifest for source verification.
        Contest test labels are not supplied, so Test.csv cannot serve as a scored test set here.
    """
    bibtex = r"""
        @misc{sendy2019logistics,
          author = {{Sendy} and {insight2impact}},
          title = {Sendy Logistics Challenge},
          year = {2019},
          howpublished = {Zindi},
          url = {https://zindi.world/competitions/sendy-logistics-challenge}
        }
    """
    curation_comments = """
        - Prediction point: order placement, before rider confirmation or assignment. This is the revised task
          whose task, filters, retained distance, split and RMSE were accepted by Myunghwan on 2026-10-29
          after final review-added-datasets ("yes, ship"). Build and commit require a separate request.
        - The original contest predicted pickup-to-arrival seconds. The revised target is destination clock minus
          placement clock plus 86,400 times their calendar-day difference. The original source has 21,199 same-day,
          one next-day and one two-day case, all agreeing with weekday differences; all retained orders are same-day. Month/year is missing; this assumes the recorded event dates
          fall in the same calendar month and does not reconstruct a global chronology.
        - CC (2026-10-29, Myunghwan): exclude total placement-to-arrival durations above 86,400 seconds and
          straight-line endpoint average speeds above 100 km/h. Strict inequalities retain equality at either boundary.
          Haversine distance uses radius 6,371.0088 km and is divided by total duration, never the pickup leg or source Distance.
          Of 21,201 source rows, two exceed 24 hours; zero exceed 100 km/h. Retain 21,199 rows with unchanged targets.
        - Exception to CLEAN-11 (2026-10-29, Myunghwan): restrict this benchmark to ordinary completed deliveries;
          two exceptional preconfirmation delays contributed 39.31% of squared error in the prior fixed-model check.
          Serves P3/P4: state the restricted ETA application and evaluation population honestly. This is not proof that
          excluded labels are erroneous. Eligibility depends on the outcome and is not known at order placement.
          No raw records are deleted, no retained labels are corrected or capped, and no speed/eligibility flag is a predictor.
        - The 547 original pickup legs of at most ten seconds show median recorded pickup waiting of 1,505 seconds
          followed by three seconds of delivery. This supports late pickup marking, not row-level proof of true arrival.
          The revised target does not use the intermediate pickup timestamp. The winner interview describes this mechanism:
          https://zindi.world/learn/meet-the-winners-of-the-sendy-logisitics-challenge .
        - Residual concern: a 100-second total spans endpoints 2.49 km apart (source distance 6 km); another 38 orders
          with the same endpoints have median total 1,868.5 seconds. Geographic comparisons do not verify GPS arrival.
          Two totals of 87,075 and 180,156 seconds are dominated by 81,736 and 176,725 seconds before confirmation.
          These excluded cases may be actual dispatch delays; scheduled delivery or erroneous placement dates remain unverified.
        - Drop all confirmation, pickup-arrival, pickup and destination-arrival input fields, the original target,
          Rider Id, unique Order No and constant Vehicle Type. Destination events are used only to construct the label.
          Select predictors explicitly; no elapsed future-stage duration or timing-derived quality flag is a feature.
        - Riders.csv has only changing counts, tenure and ratings beyond its key; no eligible static fields and no join.
          Customer identity already in the orders is a categorical input. Platform, customer type and weekday are categorical.
        - CC (2026-10-29, Myunghwan): retain source distance when it behaves consistently; exact definition is not
          by itself a reason for omission. Filtered Train and original Test have median 8 km and correlations 0.952/0.953
          to straight-line endpoint distance. All below-straight-line shortfalls are under 1 km, compatible with
          integer precision but not proof of the convention. Repeated routes vary; a fixed routing method is not verified.
          Source distance routing/as-of remains undocumented. No later-only measurement has been demonstrated;
          revisit if provenance establishes post-placement travel-dependent values. Ablation does not establish timing.
        - Weather is source-described as matched to placement and measured every three hours. Exact past-only versus
          nearest-sample alignment is undocumented. Missing weather remains missing; no imputation or zero filling.
        - Five confirmation clocks precede placement by 1-42 seconds; these future confirmation fields are excluded.
          No reliable corrected placement or arrival timestamps exist in the supplied release.
        - CC (2026-10-29, Myunghwan): retain RMSE in original seconds after the approved filters.
          The target and its tail are changed; the original leaderboard task is not reproduced. The standard RMSE
          score is a stand-in for the revised total-duration task, with its large-error emphasis retained. No target transform, clipping or winsorization.
        - The 7,068 original test orders lack destination-arrival labels and are not scored. Full raw files and hashes
          are retained locally. The 2025 archive export date is not an observation date. Raw data is not redistributed.
    """
    target = "Time from Placement to Arrival"
    problem_type = "regression"
    metric = Metric.stand_in(
        "rmse",
        original="Root Mean Squared Error on pickup-to-arrival seconds",
        reason="The task now predicts placement-to-arrival duration. Retain squared error in seconds for the same ETA goal, as accepted after eligibility filtering and scoring review; this is not the original contest target.",
        reference="https://zindi.world/competitions/sendy-logistics-challenge",
    )
    splits_comment = """
        Default repeated random folds over labelled completed orders; recurring customers are permitted.
        Riders may recur in the source population but rider identity is excluded from predictors at placement.
        CC (2026-10-29, Myunghwan): a supported order sequence would permit a cutoff; otherwise accept random
        evaluation with limited value. Across all 28,269 original Train/Test orders, numeric Order No sorting has day/weekday adjacency 0.669% versus random 0.693%; clocks lack forward progression. No supported chronological sequence was found.
        Full dates and a supported chronological index are unavailable. This is a same-release approximation,
        forced from temporal (SPLIT-8), not a test of future periods or entirely unseen riders/customers.
        The competition's unlabelled test rows are excluded from scored evaluation. Temporal optimism is unmeasured.
        If a later source release supplies full dates, recover chronological windows and recheck that training
        outcomes were available by each prediction cutoff before interpreting later-period performance.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "Train.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        columns = [
            "User Id",
            "Platform Type",
            "Personal or Business",
            "Placement - Day of Month",
            "Placement - Weekday (Mo = 1)",
            "Distance (KM)",
            "Temperature",
            "Precipitation in millimeters",
            "Pickup Lat",
            "Pickup Long",
            "Destination Lat",
            "Destination Long",
        ]
        df = raw[columns].copy()
        placement = pd.to_datetime(raw["Placement - Time"], format="%I:%M:%S %p", errors="raise")
        arrival = pd.to_datetime(raw["Arrival at Destination - Time"], format="%I:%M:%S %p", errors="raise")
        placement_seconds = placement.dt.hour * 3600 + placement.dt.minute * 60 + placement.dt.second
        arrival_seconds = arrival.dt.hour * 3600 + arrival.dt.minute * 60 + arrival.dt.second
        day_delta = raw["Arrival at Destination - Day of Month"] - raw["Placement - Day of Month"]
        weekday_delta = (raw["Arrival at Destination - Weekday (Mo = 1)"] - raw["Placement - Weekday (Mo = 1)"]) % 7
        if not ((day_delta >= 0) & (day_delta % 7 == weekday_delta)).all():
            raise ValueError(
                "Placement/arrival calendar differences require source review; do not guess month rollover"
            )
        df["Placement - Seconds after midnight"] = placement_seconds
        df[self.target] = day_delta * 86400 + arrival_seconds - placement_seconds
        if not (df[self.target] > 0).all():
            raise ValueError("Nonpositive total duration requires source review")
        # Curator-approved outcome-based eligibility, not evidence of corrected timestamps.
        lat1, lon1, lat2, lon2 = [
            np.deg2rad(raw[column].to_numpy(dtype=float))
            for column in ["Pickup Lat", "Pickup Long", "Destination Lat", "Destination Long"]
        ]
        if not all(np.isfinite(values).all() for values in [lat1, lon1, lat2, lon2]):
            raise ValueError("Missing/nonfinite endpoints require review before applying speed eligibility")
        if not (
            (np.abs(lat1) <= np.pi / 2).all()
            and (np.abs(lat2) <= np.pi / 2).all()
            and (np.abs(lon1) <= np.pi).all()
            and (np.abs(lon2) <= np.pi).all()
        ):
            raise ValueError("Out-of-range coordinates require source review")
        haversine = np.sin((lat2 - lat1) / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2
        straight_line_km = 6371.0088 * 2 * np.arcsin(np.sqrt(np.clip(haversine, 0, 1)))
        speed_kmh = straight_line_km * 3600 / df[self.target]
        return df.loc[(df[self.target] <= 86400) & (speed_kmh <= 100)].copy()

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["User Id", "Platform Type", "Personal or Business", "Placement - Weekday (Mo = 1)"]
        )
