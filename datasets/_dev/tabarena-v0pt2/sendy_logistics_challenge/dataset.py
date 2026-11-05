"""Sendy: the seconds from a rider's pickup to arrival at the destination, the source's task (data-foundry v2)."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Metric, TaskSummary

# The order's events up to the prediction point (pickup), in order; each clock ships as seconds after midnight.
KNOWN_EVENTS = ["Placement", "Confirmation", "Arrival at Pickup", "Pickup"]

MAX_LATE_MARK_SECONDS = 60
"""A pickup leg this short was marked at the destination: the rider "forgot to mark that he took the order and did it
just before it was delivered" (the winners' page). Such legs leave (Lennart, 2026-11-05; CLEAN-11)."""

LATE_MARKED_LEGS = 740
"""The legs of ``MAX_LATE_MARK_SECONDS`` or less in Train.csv; another count means another file."""


def _seconds_after_midnight(clock: pd.Series) -> pd.Series:
    """A clock such as ``9:35:46 AM`` as seconds after midnight."""
    time = pd.to_datetime(clock, format="%I:%M:%S %p", errors="raise")
    return time.dt.hour * 3600 + time.dt.minute * 60 + time.dt.second


def _straight_line_km(raw: pd.DataFrame) -> pd.Series:
    """The great-circle distance from the pickup to the destination coordinates, in km."""
    lat1, lon1, lat2, lon2 = (
        np.radians(raw[c]) for c in ["Pickup Lat", "Pickup Long", "Destination Lat", "Destination Long"]
    )
    a = np.sin((lat2 - lat1) / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2
    return 2 * 6371 * np.arcsin(np.sqrt(a))


class SendyLogisticsChallenge(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="When a Sendy rider has picked up a parcel in Nairobi, how many seconds until the rider arrives at "
        "the destination?",
        use_case="Sendy tells the customer an arrival time once the rider has the parcel, and plans the rider's next "
        "orders from it.",
        row="One completed express motorbike delivery order in Nairobi from the 2019 Sendy challenge (20,461 of the "
        "21,201 orders of the labelled training file).",
        predicted="The seconds from the pickup to the arrival at the destination, both as the rider marks them in the "
        "app, as the source gives it.",
        known="The customer, their platform and type, the rider, the day, weekday and time of the order's placement "
        "and of the rider's confirmation, the times of the rider's arrival at the pickup and of the pickup, the pickup "
        "and destination coordinates, the source's distance and the weather at placement.",
        split="Three repeats of three random folds over the same release; customers and riders recur. The release "
        "has the day of the month and the weekday but no month order or year, so later periods cannot be held out.",
        changes="The rider table the competition offered is left out, since its order counts, tenure and ratings "
        "were taken after these orders. The 740 legs of 60 seconds or less leave: the rider marked the pickup at the "
        "destination, so the customer already had the parcel and no one acts on that arrival time.",
        fit="approximate",
        fit_reason="The source's own task at its moment. The label is the riders' marks; a few late pickup marks "
        "above 60 seconds may remain. Random folds over one release stand in for future orders. Kept: a weak leak "
        "across rows (features from the same rider's later orders that day) and the source distance, not measured "
        "between the rider's taps but possibly a GPS total recorded after delivery.",
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
        We start with Train.csv of the Zindi Sendy Logistics Challenge (21,201 labelled orders).

        - Prediction point: the rider has picked up the parcel, the source's task (Lennart, 2026-11-04: switch to
          the source task). It replaces our placement-to-arrival target, two thirds of whose variance came before
          the parcel moved, from the wait for a rider, which no input describes.
        - Target: `Time from Pickup to Arrival` in seconds, as the source gives it; it equals the destination
          clock minus the pickup clock in every row.
        - Inputs: the events up to pickup. Each clock (placement, confirmation, arrival at the pickup, pickup) is
          parsed to seconds after midnight; the day of month and weekday of placement and of confirmation stay.
        - The two weekdays (1-7) are numbers, a cycle as rossmann's `DayOfWeek` (CLEAN-14; Lennart, 2026-11-04).
          Those of arrival at the pickup and of pickup equal the confirmation's in every row and are dropped as
          copies.
        - `Rider Id` and `User Id` are categorical inputs: the rider and the customer are known at pickup (922
          riders; per the 2026-10-29 audit of Test.csv, 99.4% of its orders have a rider seen in training; 99.1-99.4%
          of the test folds' orders do).
        - Dropped: the arrival-at-destination fields (they make the label), the unique `Order No` and the
          constant `Vehicle Type`.
        - Riders.csv stays out: it is not as-of. Per the 2026-10-29 audit, every rider's `No_Of_Orders` is at least
          their orders in Train and Test, so the counts, tenure and ratings were taken after these orders.
        - Anomaly: riders mark the pickup late, at the destination, so 547 legs are 10 s or less (2.6%) and 740 are
          60 s or less. Lennart kept them as the source's labels on 2026-11-04 (CLEAN-11) (superseded 2026-11-05:
          the 740 leave, CC below). With them, LightGBM on the first repeat put 4.6% of its squared error on the
          legs of 10 s or less, a model trained only on legs of 100 s or more lost 11.5 RMSE over the nine splits
          (744.2 to 755.7), and an explicit wait feature gained 8.5: the task partly scored spotting late marks.
        - CC (2026-11-05, Lennart): the 740 pickup legs of 60 s or less leave (issue 4, B; CLEAN-11's clause for a
          row whose target the source names as not the task's quantity; `MAX_LATE_MARK_SECONDS`, guarded at 740).
          The winners' page says the rider "forgot to mark that he took the order and did it just before it was
          delivered" (https://zindi.world/learn/meet-the-winners-of-the-sendy-logisitics-challenge). On these legs
          the customer already has the parcel and no one acts on the ETA, so a deployed team leaves them out of
          training and does not judge its model on them. The late tap shows in the inputs: the wait from arrival
          at the pickup to the pickup mark has a median of 1,505 s on legs of 10 s or less (1,337 s at 11-60 s)
          against 475 s on legs over 120 s. They are real deliveries (median 2.64 km in a straight line, none
          within 100 m), so this departs from the task Zindi scored. The 82 legs of 61-120 s stay, though their
          median wait of 1,358 s says some are late marks too. LightGBM, first repeat: RMSE 761.3 to 742.8 s; nine
          splits: the wait feature's gain 8.5 to 3.2 (0.0 to 7.8 per split), and training only on legs of 100 s or
          more now costs 0.2 (733.1 to 733.2). 20,461 orders remain; 2 of the 924 riders leave with them.
        - Order_No_20080 and Order_No_7111 end 89-90 m from their pickup but stay (USE-7): the source distance is
          3 and 4 km and the coordinates are anonymised, so the destination exists. The 100 m radius of nyc, pkdd
          and Lusaka rests on exact coordinates.
        - No other row is dropped. The two multi-day orders, Order_No_2800 and Order_No_3530, waited 22.7 and 49.1 h
          for confirmation; their pickup legs, 2,640 and 1,854 s at about 15 km/h, are ordinary. The longest leg
          is 7,883 s, and none passes 3 h.
        - Anomaly: five confirmation clocks precede placement by 1-42 s; kept as recorded.
        - `Distance (KM)`, tested: not measured between the rider's two taps; a GPS total recorded after delivery not
          excluded (Lennart, 2026-11-05, issue 5, A as (a); it replaces the `Potential leak, kept on purpose` label of
          2026-11-04; LEAK-38 names it among the kept fields). The dictionary reads "Distance covered (KM) - The
          distance from Pickup to Destination", which a trip records at arrival, while a distance Sendy computes
          when it prices the order is known at placement; the page does not say which. On Train.csv's 21,201 orders
          the data points to the second: 1,708 of the 2,094 repeated identical routes carry the same km, and 275 of
          the other 386 differ by 1 km; within a route, Distance does not track the label (correlation 0.013); the
          547 legs marked at the destination carry the full route distance (median 5 km). It tracks the straight
          line (correlation 0.952) and lowers RMSE from 766.6 to 742.8 s (first repeat; 789.6 to 761.5 before the
          drop above). The untested part stays a kept risk, named in `fit_reason` (USE-8). Revisit if a source shows
          it is the distance travelled.
        - Potential leak, kept on purpose (weak, across rows): features a participant builds from the same rider's
          later orders that day (their clocks minus this pickup, the day's order count), which do not exist at
          pickup, gain 4.2 RMSE against a noise spread of 0.2, positive on all 9 splits (3.4, 0.3 and 8 of 9 before
          the drop above). Our inputs hold no such feature; a rider-day split cannot be built cleanly, since day and
          weekday merge months.
        - Weather is matched to placement by the source, "measured every three hours"; the anonymised values vary
          within an hour. Missing values stay missing. No recorded precipitation is 0 (541 values, 0.1-99.1 mm),
          so a blank where a temperature exists most likely means no rain; every row without a temperature also
          lacks precipitation.
        - Metric: the source's RMSE in seconds, with no target transform.
        - Test.csv's 7,068 orders (per the 2026-10-29 audit) have no labels and are not used.
    """
    target = "Time from Pickup to Arrival"
    problem_type = "regression"
    metric = Metric.source(
        "rmse",
        original="Root Mean Squared Error on Time from Pickup to Arrival, in seconds",
        reference="https://zindi.world/competitions/sendy-logistics-challenge",
    )
    splits_comment = """
        Default repeated random folds over the labelled orders; customers and riders recur, as both are known at
        pickup. A temporal split is not possible: the release has the day of the month and the weekday but no month
        order or year. CC (2026-10-29, Myunghwan): a supported order sequence would permit a cutoff; otherwise accept
        random evaluation with limited value. Sorting by the number in `Order No` gives day/weekday adjacency of
        0.669% against 0.693% at random over all 28,269 Train/Test orders (the 2026-10-29 audit; 0.627% against
        0.731% on Train alone), so it holds no chronology. Weekday minus day of month (mod 7) gives the weekday each
        month started on: 7 month classes, which no run of calendar months puts in a unique order. Holding out one
        class gives RMSE 734.1 against 733.0 for random folds of the same size, and holding out calendar days 737.0
        against 734.9 on these folds (LightGBM; 750.1 against 748.8 and 755.1 against 752.5 before the 2026-11-05
        drop of the short legs), so same-period orders on both sides barely help. The split is
        forced from temporal (SPLIT-8) and does not test future periods. If a later release supplies full dates,
        build chronological windows.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "Train.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # Arrival at the pickup and pickup share the confirmation's day and weekday in every row: drop the copies.
        for event in ["Arrival at Pickup", "Pickup"]:
            for part in ["Day of Month", "Weekday (Mo = 1)"]:
                if not raw[f"{event} - {part}"].equals(raw[f"Confirmation - {part}"]):
                    raise ValueError(f"{event} - {part} no longer equals the confirmation's; keep it as an input")
        # The source's label is the destination clock minus the pickup clock.
        day_delta = raw["Arrival at Destination - Day of Month"] - raw["Pickup - Day of Month"]
        recorded = (
            day_delta * 86400
            + _seconds_after_midnight(raw["Arrival at Destination - Time"])
            - _seconds_after_midnight(raw["Pickup - Time"])
        )
        if not recorded.equals(raw[self.target]):
            raise ValueError("The target no longer equals the recorded pickup-to-arrival clocks; review the source")
        # The pickup legs marked at the destination leave (CLEAN-11, the source's words in MAX_LATE_MARK_SECONDS).
        late = raw[self.target] <= MAX_LATE_MARK_SECONDS
        if late.sum() != LATE_MARKED_LEGS:
            raise ValueError(f"{late.sum()} legs of {MAX_LATE_MARK_SECONDS} s or less, not {LATE_MARKED_LEGS}")
        raw = raw[~late]
        columns = [
            "User Id",
            "Rider Id",
            "Platform Type",
            "Personal or Business",
            "Placement - Day of Month",
            "Placement - Weekday (Mo = 1)",
            "Confirmation - Day of Month",
            "Confirmation - Weekday (Mo = 1)",
            "Distance (KM)",
            "Temperature",
            "Precipitation in millimeters",
            "Pickup Lat",
            "Pickup Long",
            "Destination Lat",
            "Destination Long",
            self.target,
        ]
        df = raw[columns].copy()
        for event in KNOWN_EVENTS:
            df[f"{event} - Seconds after midnight"] = _seconds_after_midnight(raw[f"{event} - Time"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "User Id",
                "Rider Id",
                "Platform Type",
                "Personal or Business",
            ]
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        leg = raw[self.target]
        wait = _seconds_after_midnight(raw["Pickup - Time"]) - _seconds_after_midnight(raw["Arrival at Pickup - Time"])
        band = pd.cut(
            leg, [0, 10, MAX_LATE_MARK_SECONDS, 120, np.inf], labels=["1-10 s", "11-60 s", "61-120 s", "over 120 s"]
        )
        table = (
            pd.DataFrame({"pickup leg": band, "wait": wait, "km": _straight_line_km(raw), "dist": raw["Distance (KM)"]})
            .groupby("pickup leg", observed=True)
            .agg(
                orders=("wait", "size"),
                **{
                    "median wait from arrival at the pickup to the pickup mark (s)": ("wait", "median"),
                    "median straight line (km)": ("km", lambda s: round(s.median(), 2)),
                    "median Distance (KM)": ("dist", "median"),
                },
            )
            .reset_index()
        )
        table["rows"] = np.where(table["pickup leg"].isin(["1-10 s", "11-60 s"]), "dropped", "kept")
        return [
            Decision(
                title=f"Pickup legs of {MAX_LATE_MARK_SECONDS} s or less dropped",
                why=(
                    "The rider marked the pickup at the destination (the winners' page), so the customer already has "
                    "the parcel and no one acts on the ETA. The late tap shows in the long wait before the pickup "
                    "mark; the legs are real deliveries, kilometres long. Lennart, 2026-11-05 (CLEAN-11)."
                ),
                evidence=table,
            )
        ]
