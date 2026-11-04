"""Sendy: the seconds from a rider's pickup to arrival at the destination, the source's task (data-foundry v2)."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary

# The order's events up to the prediction point (pickup), in order; each clock ships as seconds after midnight.
KNOWN_EVENTS = ["Placement", "Confirmation", "Arrival at Pickup", "Pickup"]


def _seconds_after_midnight(clock: pd.Series) -> pd.Series:
    """A clock such as ``9:35:46 AM`` as seconds after midnight."""
    time = pd.to_datetime(clock, format="%I:%M:%S %p", errors="raise")
    return time.dt.hour * 3600 + time.dt.minute * 60 + time.dt.second


class SendyLogisticsChallenge(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="When a Sendy rider has picked up a parcel in Nairobi, how many seconds until the rider arrives at "
        "the destination?",
        use_case="Sendy tells the customer an arrival time once the rider has the parcel, and plans the rider's next "
        "orders from it.",
        row="One completed express motorbike delivery order in Nairobi from the 2019 Sendy challenge (21,201 orders, "
        "the labelled training file).",
        predicted="The seconds from the pickup to the arrival at the destination, both as the rider marks them in the "
        "app, as the source gives it. Riders often mark the pickup late, at the destination, so 2.6% of the labels are "
        "10 seconds or less; on those the parcel has already arrived, and they reward spotting a late mark rather than "
        "estimating a trip.",
        known="The customer, their platform and type, the rider, the day, weekday and time of the order's placement "
        "and of the rider's confirmation, the times of the rider's arrival at the pickup and of the pickup, the pickup "
        "and destination coordinates, the source's distance and the weather at placement.",
        split="Three repeats of three random folds over the same release; customers and riders recur. The release "
        "has the day of the month and the weekday but no month order or year, so later periods cannot be held out.",
        changes="The rider table the competition offered is left out, since its order counts, tenure and ratings "
        "were taken after these orders.",
        fit="approximate",
        fit_reason="The source's own task at its moment, with what is known then. The label is the riders' marks, "
        "and the late pickup marks make some labels near zero; random folds over one release stand in for future "
        "orders. A weak leak across rows is kept: features built from the same rider's later orders that day.",
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
        - `Rider Id` and `User Id` are categorical inputs: the rider and the customer are known at pickup (924
          riders; per the 2026-10-29 audit of Test.csv, 99.4% of its orders have a rider seen in training; 99.2-99.4%
          of the test folds' orders do).
        - Dropped: the arrival-at-destination fields (they make the label), the unique `Order No` and the
          constant `Vehicle Type`.
        - Riders.csv stays out: it is not as-of. Per the 2026-10-29 audit, every rider's `No_Of_Orders` is at least
          their orders in Train and Test, so the counts, tenure and ratings were taken after these orders.
        - Anomaly: 547 legs of 10 s or less (2.6%; 740 of 60 s or less) stay as the source's labels (CLEAN-11):
          riders mark the pickup late, when they arrive
          (https://zindi.world/learn/meet-the-winners-of-the-sendy-logisitics-challenge). The late mark shows in
          the inputs: the wait from arrival at the pickup to the pickup mark has a median of 1,505 s on these legs
          against 475 s on legs over 120 s (1,337 s at 11-60 s, 1,358 s at 61-120 s). In LightGBM on the first
          repeat they are 4.6% of the squared error, and RMSE on the other legs is 749.3 s against 761.3 s on all.
          Over the nine splits, a model trained only on legs of 100 s or more loses 11.5 RMSE (744.2 to 755.7), and
          an explicit wait feature gains 8.5; so the task partly scores spotting late marks, as the competition did.
        - Order_No_20080 and Order_No_7111 end 89-90 m from their pickup but stay (USE-7): the source distance is
          3 and 4 km and the coordinates are anonymised, so the destination exists. The 100 m radius of nyc, pkdd
          and Lusaka rests on exact coordinates.
        - No row is dropped. The two multi-day orders, Order_No_2800 and Order_No_3530, waited 22.7 and 49.1 h
          for confirmation; their pickup legs, 2,640 and 1,854 s at about 15 km/h, are ordinary. The longest leg
          is 7,883 s, and none passes 3 h.
        - Anomaly: five confirmation clocks precede placement by 1-42 s; kept as recorded.
        - Potential leak, kept on purpose (LEAK-38; Lennart, 2026-11-04): the dictionary reads "Distance covered (KM) -
          The distance from Pickup to Destination", which a trip records at arrival, while a distance Sendy computes
          when it prices the order is known at placement; the page does not say which. The data points to the
          second: 1,708 of the 2,094 repeated identical routes carry the same km, and 275 of the other 386 differ
          by 1 km; within a route, Distance does not track the label (correlation 0.013); the 547 legs marked at
          the destination carry the full route distance (median 5 km). So it is not measured between the two
          marks; a GPS total recorded after delivery is not excluded. It tracks the straight line (correlation
          0.952) and lowers RMSE from 789.6 to 761.5 s (first repeat). Revisit if a source shows it is the distance
          travelled.
        - Potential leak, kept on purpose (weak, across rows): features a participant builds from the same rider's
          later orders that day (their clocks minus this pickup, the day's order count), which do not exist at
          pickup, gain 3.4 RMSE against a noise spread of 0.3, positive on 8 of the 9 splits. Our inputs hold no
          such feature; a rider-day split cannot be built cleanly, since day and weekday merge months.
        - Weather is matched to placement by the source, "measured every three hours"; the anonymised values vary
          within an hour. Missing values stay missing. No recorded precipitation is 0 (552 values, 0.1-99.1 mm),
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
        class gives RMSE 750.1 against 748.8 for random folds of the same size, and holding out calendar days 755.1
        against 752.5 on these folds (LightGBM), so same-period orders on both sides barely help. The split is
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
