"""Meituan minutes to delivery predicted at courier acceptance; evidence in README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from data_foundry.definition import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    Source,
    SplitPlan,
    TaskSummary,
    Temporal,
)

OBSERVED_EVENT_COLUMNS = (
    "platform_order_time",
    "order_push_time",
    "dispatch_time",
    "grab_time",
    "fetch_time",
    "arrive_time",
)
TEST_DAYS = ("2022-10-24", "2022-10-23", "2022-10-22")
"""Window starts, newest first; each window is one local acceptance day, the newest to the end of the data."""
GAP = pd.Timedelta(hours=3)
"""Data snapshot before each window's midnight: time to extract, train with tuning and roll out the nightly refit."""


class MeituanFoodDeliveryTime(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How many minutes after courier acceptance will this food order reach the customer?",
        use_case="An independent delivery-time model updates the customer's ETA when a courier accepts the order, using courier and merchant information without the platform's existing forecasts.",
        row="One accepted food order from the October 17-24, 2022 source cohorts in an anonymized Chinese city, including prebooked orders; acceptances run to 00:23 on October 25.",
        predicted="Minutes from courier acceptance to delivery.",
        known="Acceptance time, elapsed order and dispatch times, merchant and accepting courier, business area of the accepted waybill, pickup and destination coordinates, courier location at acceptance, and the prebook flag. The platform's promise and meal-ready predictions are excluded.",
        split="Three future acceptance days, October 22-24; the newest window runs from October 24 to the end of the data (00:23 on October 25). Each nightly refit takes its data 3 hours before midnight, leaving time to train, tune and roll out, and trains on the orders accepted and delivered by then. Merchants and couriers can recur.",
        changes="Select accepted waybills, omit one absent arrival label, predict the minutes remaining after acceptance rather than the total since placement, exclude both platform forecasts for independent prediction, and evaluate acceptance-time ETA updates on future days rather than broader assignment optimization.",
        fit="direct",
        fit_reason="The challenge names delivery timing prediction. Inputs describe the order by acceptance without the platform's blackbox forecasts. Only delivered orders have labels. Eight days in one city limit generalization; prebooked orders can have long known waits. The recorded promise is an external reference with unverified snapshot timing, not a predictor; prebooked orders therefore also lack the delivery slot the customer most likely booked.",
    )
    unique_name = "meituan_food_delivery_time"
    sources = (
        Source(
            role="publication",
            platform="GitHub",
            url="https://github.com/meituan/Meituan-INFORMS-TSL-Research-Challenge",
            license="CC BY-NC 4.0; source additionally requests permission before redistribution",
            year="2024",
            bibtex=r"""
        @misc{meituan2024,
          author = {Zhao, Lei and Wang, Hai and Liang, Yile and Li, Donghui and Zhao, Jiuxia and Ding, Xuetao and Hao, Jinghua and He, Renqing},
          title = {The First INFORMS TSL Data-Driven Research Challenge: Background and Data Description},
          year = {2024},
          howpublished = {\url{https://github.com/meituan/Meituan-INFORMS-TSL-Research-Challenge}}
        }
    """,
        ),
    )
    domain = "business & marketing"
    data_tags = ("Spatial",)
    download_description = """
        mkdir -p local-data-warehouse/meituan_food_delivery_time/raw
        curl -L https://raw.githubusercontent.com/meituan/Meituan-INFORMS-TSL-Research-Challenge/1f9b4288cee5a78d1e5da007fc306bbaa662fc6d/all_waybill_info_meituan_0322.csv.zip -o local-data-warehouse/meituan_food_delivery_time/raw/all_waybill_info_meituan_0322.csv.zip
        # ZIP SHA256: 38b51431a12dd7e73deb4fc750b1275067fbc29cfce2c4b4492339738c988ce2
        unzip -n local-data-warehouse/meituan_food_delivery_time/raw/all_waybill_info_meituan_0322.csv.zip -d local-data-warehouse/meituan_food_delivery_time/raw
    """
    curation_comments = """
        - Prediction point: immediately after courier acceptance. This is an ETA update, not pre-assignment prediction.
          The target is the minutes from acceptance to arrival, the part still unknown; the minutes elapsed since
          placement are a known input, not part of the target (USE-3, USE-5, USE-6). The total since placement
          (the first target) made the score a test of adding back the known elapsed time on prebooked orders.
        - The ZIP contains 654,343 attempts for 568,546 orders, exactly one accepted attempt each. Rejected attempts
          have structural zeros in grab, fetch and arrive times and the courier coordinates. Keep accepted attempts; omit one absent delivery label (arrive_time=0),
          leaving 568,545 labeled orders. Do not clip or log unusual durations or discard prebooked orders.
        - Long durations (CLEAN-11): 42 orders have over 3 hours remaining after acceptance; 33 are prebooks, 9 are
          not (2 over 6 hours, at most 652 minutes). Kept: nothing marks them as errors, and dropping training rows
          over 180 minutes changes no score. The ETA family drops trips over 3 hours (Lusaka trips, NYC and Porto taxis).
        - Source: 2024 background Tables 1-2; October 2024 supplement sections 2.4-2.5; Wang et al. 2025 section 3.1.
          The latter places grab_lat and grab_lng at acceptance, correcting the earlier assignment description;
          they match the dispatch snapshots' courier positions (median 35 m within 30 seconds).
          Coordinates stay in the source's shifted integer units; no external geocoding or spatial matching.
        - Myunghwan (2026-11-09) chose independent ETA prediction without both platform outputs. Drop
          estimate_arrived_time and estimate_meal_prepare_time from model inputs, including derived durations.
          The recorded promise remains an external operational comparison, never a feature or split key.
          Forecast-assisted results are sensitivity evidence, not a second shipped version. This deliberately
          changes forecast refinement into independent prediction (USE-1, USE-6).
        - The recorded promise baseline is evaluated from raw rows in the decisions evidence only. Issuance history
          is unverified, so it is not a certified prospective comparator. Meal-ready forecast revisions are irrelevant
          to the primary model because that field and its missingness are excluded entirely.
        - Retain prebooked orders and their flag: their days before acceptance are in the elapsed input, not in the
          target. Compare with the promise and a training-mean baseline. No target-based duration filtering.
        - Drop CSV index, order and waybill IDs, dt (the source's cohort date; it differs from the local creation
          date for 1,758 orders), acceptance indicator and future fetch time. Arrival
          time certifies the entire observed training interval ended before the test window, then leaves the model frame. Merchant,
          courier and business-area (da_id, the accepted waybill's: it follows the accepting courier in the 1,963 orders
          where it changes, not the order's district) IDs stay categorical. No full-wave membership, wave ends or future aggregates enter.
        - Convert Unix timestamps to naive China local time (UTC+8). Recompute weekend from acceptance time, since
          the original flag describes order creation. Keep one acceptance datetime and elapsed durations.
        - Three daily future windows with expanding history; every observed order event must precede the refit's
          data snapshot, 3 hours before each window's midnight (SPLIT-9, SPLIT-10). Verify creation, push, dispatch,
          acceptance, pickup and delivery clocks: arrival is the latest actual event in every labeled order, so the
          arrival-before-snapshot guard purges entire unfinished training intervals. Predicted meal-ready and promised times are forecasts, not observed events. Eight source days do not test unseen cities, seasons, couriers or merchants. The newest window holds every
          acceptance from October 24 00:00 to the end of the data, with the 62 acceptances up to 00:23 on October 25.
        - Supporting dispatch snapshots cover only three noon checkpoints daily, not continuous workload. Completed
          waves contain future information and the supplement documents a wave-start indexing defect; no joins used.
        - Potential leak, kept on purpose (LEAK-9, an evaluation leak): within a test day the accepting courier's
          next acceptances (time to the next one, accepts in the next 30/60 minutes, where the next pickup is)
          tell when this order was delivered. Read from other test rows they lowered LightGBM RMSE from
          7.72/8.29/7.45 to 7.07/7.61/6.76 minutes (22/23/24 October, measured 2026-11-21 on complete days; gain
          0.65-0.70 on 3 of 3 days); no column
          drop closes it without removing the courier's legitimate history. Each test order is predicted from the
          training rows and its own features only; a method that reads other test rows is called out and not
          benchmarked (as for loan_default_prediction_imperial_college).
        - Metric (MET-8): RMSE in minutes scores the mean remaining time, not the padded ETA a customer is shown.
        - Split walk (the split decision tree, SPLIT-36, from the record's collection type Dated Event Log): [LOG.meets] the model predicts orders after the data, cases after the data → Order and windows step → [ORDER.order] the acceptance time is recorded: yes → [ORDER.windows] three one-day test windows, the oldest training on 59.5% of the rows: yes → leaf L-ORDER.windows, Temporal · windows on the time key, the split the definition ships (`split_leaf`). The gap follows the gap rules: three hours, the time a nightly refit needs to extract its data, train with tuning and roll out (the source states none; the curator's sign-off of 2026-11-24, Andrej), and training keeps only orders delivered before that snapshot.
    """
    accepted_check_warnings = {
        "meta_time_horizon_mismatch": "Andrej (2026-11-24, issue 5 B): the newest test window keeps the 62 "
        "acceptances up to 00:23 on 25 October (issue 2 C), so it runs 24 hours 23 minutes (67,411 rows); the check "
        "counts its span as 2 days against the 1-day horizon. The other two windows are whole local days.",
    }
    target = "remaining_minutes"
    problem_type = "regression"
    metric = Metric.fallback(
        reason="The 2024 challenge background Sample Question 4, October 2024 supplement and 2025 data paper describe timing prediction but prescribe no single predictive scoring metric; use regression RMSE."
    )
    temporal = Temporal(on="accepted_at", horizon=1, horizon_unit="days", gap=3, gap_unit="hours")
    split_leaf = "L-ORDER.windows"
    splits_comment = """
        Leaf: L-ORDER.windows (dated event log, cases after the data: windows on the acceptance time, the gap by the
        gap rules). The source is silent on the horizon, the refit cadence and any deployment delay: a nightly refit
        that predicts the next local acceptance day is assumed. Gap: 3 hours, signed off by the curator (2026-11-24,
        Andrej): a refit cannot serve at the moment its data ends, since the data must be extracted and the model
        trained with per-split tuning and rolled out, so each training side is the data snapshot at 21:00 before the
        window's midnight, after the evening peak. Training keeps the orders accepted and delivered before the
        snapshot; arrival is verified as the latest of all six actual event clocks, so every training event precedes
        the snapshot, and the test windows stay whole local days. The orders accepted in the gap (5,827 / 5,768 /
        5,179 for October 22 / 23 / 24) and the ones still undelivered at the snapshot (1,556 / 1,325 / 1,301) are
        left out. The label delay (p99 55-58 minutes, at most 652) still selects the last training hour before the
        snapshot: the kept orders are 1.8-2.2 minutes faster in remaining time than all orders of that hour, as at
        midnight, where training on the filtered side scored within 0.02 RMSE of every true label (2026-11-21). Cost
        of the gap against a midnight snapshot: +0.02 to +0.09 LightGBM RMSE minutes; 1 hour -0.03 to +0.01, 6 or 12
        hours +0.24 to +0.69 (2026-11-23). The half-the-rows floor fixed the windows: only October 22-24, the three
        newest days, train on at least half the labeled rows (338,395 / 416,321 / 494,654 rows, 59.5% / 73.2% /
        87.0%; October 21 would train on about 48.7% even without a gap), 3 windows against SPLIT-33's 3, newest
        first. The newest window runs from October 24 00:00 to the end of the data, so the 62 acceptances up to 00:23
        on October 25 are scored (67,411 test rows; 77,719 and 77,637 on October 23 and 22). Protocol (LEAK-9): each
        test order is predicted from the training rows and its own features only; no feature or model step may use
        other test rows (the same courier's next acceptances in the test day were worth 0.65-0.70 RMSE), and a method
        that reads other test rows is called out and not benchmarked.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "raw" / "all_waybill_info_meituan_0322.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.loc[raw["is_courier_grabbed"].eq(1) & raw["arrive_time"].gt(0)].copy()
        assert df["order_id"].is_unique
        assert (df["arrive_time"] >= df["grab_time"]).all()
        assert (df["grab_time"] >= df["platform_order_time"]).all()
        # Arrival must cover every observed event for the as-of training guard to certify full intervals.
        assert df[list(OBSERVED_EVENT_COLUMNS)].max(axis=1).eq(df["arrive_time"]).all()
        result = df[
            [
                "poi_id",
                "courier_id",
                "da_id",
                "is_prebook",
                "sender_lng",
                "sender_lat",
                "recipient_lng",
                "recipient_lat",
                "grab_lng",
                "grab_lat",
            ]
        ].copy()
        result["accepted_at"] = pd.to_datetime(df["grab_time"], unit="s") + pd.Timedelta(hours=8)
        result["is_weekend"] = result["accepted_at"].dt.dayofweek.ge(5).astype(int)
        result["elapsed_minutes"] = (df["grab_time"] - df["platform_order_time"]) / 60
        dispatch = df["dispatch_time"].where(df["dispatch_time"].gt(0))
        result["dispatch_to_accept_minutes"] = (df["grab_time"] - dispatch) / 60
        result["push_to_accept_minutes"] = (df["grab_time"] - df["order_push_time"]) / 60
        result[self.target] = (df["arrive_time"] - df["grab_time"]) / 60
        result["delivered_at"] = pd.to_datetime(df["arrive_time"], unit="s") + pd.Timedelta(hours=8)
        return result

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["poi_id", "courier_id", "da_id", "is_prebook", "is_weekend"],
            datetime=["accepted_at", "delivered_at"],
        )

    def _make_splits(self, df: pd.DataFrame) -> SplitPlan:
        # One local acceptance day per window, newest first; the newest runs to the end of the data (00:23 on
        # 25 October), which TemporalSplits cannot express, so the windows are built here. Training keeps the
        # orders accepted and delivered before the data snapshot, 3 hours before the window's midnight.
        accepted = df["accepted_at"].to_numpy()
        splits = {}
        for repeat, start in enumerate(pd.Timestamp(day) for day in TEST_DAYS):
            in_window = accepted >= start
            if repeat:
                in_window &= accepted < start + pd.Timedelta(days=1)
            test = np.flatnonzero(in_window)
            snapshot = start - GAP
            train = np.flatnonzero((accepted < snapshot) & (df["delivered_at"] < snapshot).to_numpy())
            assert len(train) >= len(df) / 2
            assert df["delivered_at"].iloc[train].max() < snapshot < start <= df["accepted_at"].iloc[test].min()
            splits[repeat] = {0: (train.tolist(), test.tolist())}
        return SplitPlan(splits=splits, df=df.drop(columns="delivered_at"))

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        a = raw.loc[raw["is_courier_grabbed"].eq(1)]
        counts = pd.Series(
            {
                "raw attempts": len(raw),
                "orders": raw["order_id"].nunique(),
                "accepted attempts": len(a),
                "missing arrival": int(a["arrive_time"].eq(0).sum()),
                "labeled orders": len(df),
                "merchants": df["poi_id"].nunique(),
                "couriers": df["courier_id"].nunique(),
                "prebooked": int(df["is_prebook"].eq(1).sum()),
            },
            name="rows or entities",
        )
        delivered = df["accepted_at"] + pd.to_timedelta(df[self.target], unit="m")
        baseline = a.loc[a["arrive_time"].gt(0)].copy()
        baseline_acceptance = pd.to_datetime(baseline["grab_time"], unit="s") + pd.Timedelta(hours=8)
        rows = []
        for i, date in enumerate(TEST_DAYS):
            start = pd.Timestamp(date)
            end = start + pd.Timedelta(days=1) if i else pd.Timestamp.max
            snapshot = start - GAP
            previous = df["accepted_at"] < snapshot
            train = df.loc[previous & (delivered < snapshot)]
            test = df.loc[(df["accepted_at"] >= start) & (df["accepted_at"] < end)]
            raw_test = baseline.loc[(baseline_acceptance >= start) & (baseline_acceptance < end)]
            assert len(raw_test) == len(test)
            promise_error = (raw_test["arrive_time"] - raw_test["estimate_arrived_time"]) / 60
            train_pairs = pd.MultiIndex.from_frame(train[["poi_id", "courier_id"]])
            test_pairs = pd.MultiIndex.from_frame(test[["poi_id", "courier_id"]])
            rows.append(
                {
                    "test window": date if i else f"{date} to end of data",
                    "train": len(train),
                    "test": len(test),
                    "accepted in the 3-hour gap": int(
                        ((df["accepted_at"] >= snapshot) & (df["accepted_at"] < start)).sum()
                    ),
                    "undelivered at the snapshot, excluded": int((previous & (delivered >= snapshot)).sum()),
                    "merchant seen fraction": test["poi_id"].isin(train["poi_id"]).mean(),
                    "courier seen fraction": test["courier_id"].isin(train["courier_id"]).mean(),
                    "pair seen fraction": test_pairs.isin(train_pairs).mean(),
                    "recorded promise RMSE minutes (external reference)": np.sqrt((promise_error**2).mean()),
                    "train mean remaining RMSE minutes": np.sqrt(
                        ((test[self.target] - train[self.target].mean()) ** 2).mean()
                    ),
                }
            )
        return [
            Decision(
                "One labeled accepted waybill per order",
                "Rejected attempts are not zero-duration deliveries. Retain prebooked and unusual durations; omit only the absent accepted arrival label.",
                counts,
            ),
            Decision(
                "Future-day windows and operational baselines",
                "Retain recurring merchants and couriers for future orders, using only labels known at the data snapshot "
                "3 hours before midnight. "
                "The target is the time still to come after acceptance, so a prebook's known wait is an input, not "
                "error: compare minute errors against the platform promise and the training side's mean remaining "
                "time.",
                pd.DataFrame(rows).round(4),
            ),
        ]
