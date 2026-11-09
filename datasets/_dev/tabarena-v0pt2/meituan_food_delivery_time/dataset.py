"""Meituan delivery duration predicted at courier acceptance; evidence in README.md."""

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

OBSERVED_EVENT_COLUMNS = (
    "platform_order_time",
    "order_push_time",
    "dispatch_time",
    "grab_time",
    "fetch_time",
    "arrive_time",
)


class MeituanFoodDeliveryTime(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How many minutes after placement will this accepted food order reach the customer?",
        use_case="An independent delivery-time model updates the customer's ETA when a courier accepts the order, using courier and merchant information without the platform's existing forecasts.",
        row="One accepted food order from the October 17-24, 2022 source cohorts in an anonymized Chinese city, including prebooked orders and 62 acceptances just after midnight October 25.",
        predicted="Total minutes from order placement to delivery, including the time already elapsed at acceptance.",
        known="Acceptance time, elapsed order and dispatch times, merchant and accepting courier, district, pickup and destination coordinates, courier location at acceptance, and the prebook flag. The platform's promise and meal-ready predictions are excluded.",
        split="Three future acceptance days, October 22-24. Each midnight refit trains on earlier accepted orders whose delivery was already recorded. Merchants and couriers can recur.",
        changes="Select accepted waybills, omit one absent arrival label, exclude both platform forecasts for independent prediction, and evaluate acceptance-time ETA updates on future days rather than broader assignment optimization.",
        fit="direct",
        fit_reason="The challenge names delivery timing prediction. Inputs describe the order by acceptance without the platform's blackbox forecasts. Only delivered orders have labels. Eight days in one city limit generalization; prebooked orders can have long known waits. The recorded promise is an external reference with unverified snapshot timing, not a predictor.",
    )
    unique_name = "meituan_food_delivery_time"
    year = "2024"
    domain = "business & marketing"
    source = "GitHub"
    source_url = "https://github.com/meituan/Meituan-INFORMS-TSL-Research-Challenge"
    license = "CC BY-NC 4.0; source additionally requests permission before redistribution"
    data_tags = ("Spatial",)
    download_description = """
        mkdir -p local-data-warehouse/meituan_food_delivery_time/raw
        curl -L https://raw.githubusercontent.com/meituan/Meituan-INFORMS-TSL-Research-Challenge/1f9b4288cee5a78d1e5da007fc306bbaa662fc6d/all_waybill_info_meituan_0322.csv.zip -o local-data-warehouse/meituan_food_delivery_time/raw/all_waybill_info_meituan_0322.csv.zip
        # ZIP SHA256: 38b51431a12dd7e73deb4fc750b1275067fbc29cfce2c4b4492339738c988ce2
        unzip -n local-data-warehouse/meituan_food_delivery_time/raw/all_waybill_info_meituan_0322.csv.zip -d local-data-warehouse/meituan_food_delivery_time/raw
    """
    bibtex = r"""
        @misc{meituan2024,
          author = {Zhao, Lei and Wang, Hai and Liang, Yile and Li, Donghui and Zhao, Jiuxia and Ding, Xuetao and Hao, Jinghua and He, Renqing},
          title = {The First INFORMS TSL Data-Driven Research Challenge: Background and Data Description},
          year = {2024},
          howpublished = {\url{https://github.com/meituan/Meituan-INFORMS-TSL-Research-Challenge}}
        }
    """
    curation_comments = """
        - Prediction point: immediately after courier acceptance. This is an ETA update, not pre-assignment prediction.
          Total placement-to-arrival minutes remain the target; elapsed minutes are known inputs (USE-3, USE-6).
        - The ZIP contains 654,343 attempts for 568,546 orders, exactly one accepted attempt each. Rejected attempts
          have structural zero event times. Keep accepted attempts; omit one absent delivery label (arrive_time=0),
          leaving 568,545 labeled orders. Do not clip or log unusual durations or discard prebooked orders.
        - Source: 2024 background Tables 1-2; October 2024 supplement sections 2.4-2.5; Wang et al. 2025 section 3.1.
          The latter places grab_lat and grab_lng at acceptance, correcting the earlier assignment description.
          Coordinates stay in the source's shifted integer units; no external geocoding or spatial matching.
        - Myunghwan (2026-11-09) chose independent ETA prediction without both platform outputs. Drop
          estimate_arrived_time and estimate_meal_prepare_time from model inputs, including derived durations.
          The recorded promise remains an external operational comparison, never a feature or split key.
          Forecast-assisted results are sensitivity evidence, not a second shipped version. This deliberately
          changes forecast refinement into independent prediction (USE-1, USE-6).
        - The recorded promise baseline is evaluated from raw rows in the decisions evidence only. Issuance history
          is unverified, so it is not a certified prospective comparator. Meal-ready forecast revisions are irrelevant
          to the primary model because that field and its missingness are excluded entirely.
        - Retain prebooked orders and their flag: long total times can include days before acceptance. Compare with
          elapsed-only and promise baselines, not only a constant mean. No target-based duration filtering.
        - Drop CSV index, order and waybill IDs, redundant dt, acceptance indicator and future fetch time. Arrival
          time certifies the entire observed training interval ended before the test window, then leaves the model frame. Merchant,
          courier and district IDs stay categorical. No full-wave membership, wave ends or future aggregates enter.
        - Convert Unix timestamps to naive China local time (UTC+8). Recompute weekend from acceptance time, since
          the original flag describes order creation. Keep one acceptance datetime and elapsed durations.
        - Three daily future windows with expanding history; every observed order event must precede refit
          (SPLIT-9, SPLIT-10). Verify creation, push, dispatch, acceptance, pickup and delivery clocks: arrival is
          the latest actual event in every labeled order, so the arrival-before-midnight guard purges entire
          unfinished training intervals. Predicted meal-ready and promised times are forecasts, not observed events. Eight source days do not test unseen cities, seasons, couriers or merchants. The 62 acceptances after midnight October 25 stay in the frame but outside the three complete-day test windows.
        - Supporting dispatch snapshots cover only three noon checkpoints daily, not continuous workload. Completed
          waves contain future information and the supplement documents a wave-start indexing defect; no joins used.
    """
    accepted_check_warnings = {
        "splits_rows_unused": "Myunghwan (2026-11-09) approved retaining the 62 October 25 acceptances outside the three complete October 22-24 acceptance-day test windows. These tail rows are retained in the frame but never scored; no incomplete test day is introduced."
    }
    target = "delivery_minutes"
    problem_type = "regression"
    metric = Metric.fallback(
        reason="The 2024 challenge background Sample Question 4, October 2024 supplement and 2025 data paper describe timing prediction but prescribe no single predictive scoring metric; use regression RMSE."
    )
    temporal = Temporal(on="accepted_at", horizon=1, horizon_unit="days")
    splits_comment = """
        Daily midnight refits predict the next acceptance day's orders, newest window first. Use October 22-24,
        the final three complete local acceptance days. Every actual training event must precede midnight and therefore
        the earliest test acceptance; arrival is verified as the latest of all six actual event clocks.
        Cadence and window count follow the eight-day operational release, not model scores. Each train side
        holds at least half of all labeled rows. Unknown labels leave training; refit boundary effects are measured.
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
        result[self.target] = (df["arrive_time"] - df["platform_order_time"]) / 60
        result["delivered_at"] = pd.to_datetime(df["arrive_time"], unit="s") + pd.Timedelta(hours=8)
        return result

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["poi_id", "courier_id", "da_id", "is_prebook", "is_weekend"],
            datetime=["accepted_at", "delivered_at"],
        )

    def _make_splits(self, df: pd.DataFrame) -> SplitPlan:
        windows = TemporalSplits(window=1, unit="days", cutoffs=("2022-10-22", "2022-10-23", "2022-10-24")).splits(
            df, "accepted_at"
        )
        splits = {}
        for repeat, folds in windows.items():
            train, test = folds[0]
            start = df["accepted_at"].iloc[test].min().normalize()
            train = np.asarray(train)
            train = train[(df["delivered_at"].iloc[train] < start).to_numpy()]
            assert len(train) >= len(df) / 2
            assert df["delivered_at"].iloc[train].max() < start
            assert df["delivered_at"].iloc[train].max() < df["accepted_at"].iloc[test].min()
            splits[repeat] = {0: (train.tolist(), test)}
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
        remaining = df[self.target] - df["elapsed_minutes"]
        delivered = df["accepted_at"] + pd.to_timedelta(remaining, unit="m")
        baseline = a.loc[a["arrive_time"].gt(0)].copy()
        baseline_acceptance = pd.to_datetime(baseline["grab_time"], unit="s") + pd.Timedelta(hours=8)
        rows = []
        for date in ("2022-10-24", "2022-10-23", "2022-10-22"):
            start = pd.Timestamp(date)
            previous = df["accepted_at"] < start
            train = df.loc[previous & (delivered < start)]
            test = df.loc[(df["accepted_at"] >= start) & (df["accepted_at"] < start + pd.Timedelta(days=1))]
            raw_test = baseline.loc[
                (baseline_acceptance >= start) & (baseline_acceptance < start + pd.Timedelta(days=1))
            ]
            assert len(raw_test) == len(test)
            promise_error = (raw_test["arrive_time"] - raw_test["estimate_arrived_time"]) / 60
            residual_mean = (train[self.target] - train["elapsed_minutes"]).mean()
            train_pairs = pd.MultiIndex.from_frame(train[["poi_id", "courier_id"]])
            test_pairs = pd.MultiIndex.from_frame(test[["poi_id", "courier_id"]])
            rows.append(
                {
                    "test day": date,
                    "train": len(train),
                    "test": len(test),
                    "unavailable labels excluded": int((previous & (delivered >= start)).sum()),
                    "merchant seen fraction": test["poi_id"].isin(train["poi_id"]).mean(),
                    "courier seen fraction": test["courier_id"].isin(train["courier_id"]).mean(),
                    "pair seen fraction": test_pairs.isin(train_pairs).mean(),
                    "recorded promise RMSE minutes (external reference)": np.sqrt((promise_error**2).mean()),
                    "elapsed plus train mean remaining RMSE minutes": np.sqrt(
                        ((test[self.target] - test["elapsed_minutes"] - residual_mean) ** 2).mean()
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
                "Retain recurring merchants and couriers for future orders, using only labels known at midnight. "
                "Known prebooking waits inflate total-duration variance: compare absolute-minute errors against "
                "the platform promise and elapsed time plus a mean remaining duration fitted on each train side, "
                "rather than interpreting high total-target R-squared as resolution of future uncertainty.",
                pd.DataFrame(rows).round(4),
            ),
        ]
