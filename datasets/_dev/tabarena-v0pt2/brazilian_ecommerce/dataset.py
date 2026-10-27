"""Curated dataset definition for `brazilian_ecommerce` (data-foundry v2). Evidence: README.md."""

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
    drop_columns,
)

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
ORDER_TIMESTAMPS = (
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
)
# The reviews file ends with the surveys sent on 2018-08-31 (see `_decisions`). Orders placed from August 2018 on
# are only in the sample when they arrived by then; an order promised for 2018-08-24 or earlier got its survey by
# 2018-08-31 whatever its delivery time (7,649 of 7,662 late orders got it at most 7 days after the promised date).
PURCHASED_BEFORE = "2018-08-01"
PROMISED_BY = "2018-08-24"
SECONDS_PER_DAY = 86_400


def _days(delta: pd.Series) -> pd.Series:
    """A timedelta column in days (float)."""
    return delta.dt.total_seconds() / SECONDS_PER_DAY


class BrazilianEcommerce(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How many days will an online order in Brazil take to reach the customer?",
        use_case=(
            "At checkout, the Brazilian sales platform Olist estimates how long an order will take to arrive, for "
            "example to inform the customer or to flag orders likely to be late."
        ),
        row=(
            "One delivered order with a single seller, placed through Olist from 2016 to July 2018 (88,721 orders); "
            "the release is a random sample of the orders whose customer answered a review survey."
        ),
        predicted=(
            "The days from purchase to delivery at the customer, on a log scale (median 7.5 to 9 days in May-July "
            "2018)."
        ),
        known=(
            "The purchase time, the customer's and the seller's location, the seller, the product's category, size, "
            "weight, photo count and text lengths, the item count, price and freight, the payment method and "
            "instalments, and the delivery date Olist promises at checkout."
        ),
        split=(
            "Each test window is one month of orders, March to July 2018; training is the orders placed at least a "
            "month earlier and delivered before the window starts, as for a model refit every month."
        ),
        changes=(
            "We predict the delivery time instead of the review score the uploader's notebook predicts, keep orders "
            "placed before August 2018 (later ones lack their slow deliveries), and leave a one-month gap before each"
            " test month."
        ),
        fit="direct",
        fit_reason=(
            "Everything the model sees is known at checkout, and the windows mirror a monthly refit with the "
            "deliveries known by then. Only orders with an answered review are in the release; if slow orders get "
            "more answers, the mix differs from all orders."
        ),
    )

    # Dataset
    unique_name = "brazilian_ecommerce"
    year = "2018"
    domain = "business & marketing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce"
    license = "CC BY-NC-SA 4.0"
    data_tags = ("Spatial",)
    download_description = """
        We download the Kaggle dataset published by Olist (version 2, the current one since 2021-10-01; DOI
        10.34740/KAGGLE/DSV/195341). Pinned archive:
        https://www.kaggle.com/api/v1/datasets/download/olistbr/brazilian-ecommerce?datasetVersionNumber=2
        (42.6 MB; md5 in base64 8vNwTsCNVe+U/CiHvclkcg==, from Kaggle's Croissant metadata).

        mkdir -p local-data-warehouse/brazilian_ecommerce
        kaggle datasets download olistbr/brazilian-ecommerce -p local-data-warehouse/brazilian_ecommerce
        unzip local-data-warehouse/brazilian_ecommerce/brazilian-ecommerce.zip -d local-data-warehouse/brazilian_ecommerce
        rm local-data-warehouse/brazilian_ecommerce/brazilian-ecommerce.zip

        The zip holds nine CSV files; the definition reads eight of them (not olist_geolocation_dataset.csv).
    """
    bibtex = r"""
        @misc{Olist2018BrazilianEcommerce,
          author = {{Olist} and Andr{\'e} Sionek},
          title = {Brazilian E-Commerce Public Dataset by Olist},
          year = {2018},
          howpublished = {\url{https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce}},
          doi = {10.34740/KAGGLE/DSV/195341},
          note = {Kaggle dataset}
        }
    """
    curation_comments = """
        We start with olist_orders_dataset.csv of the Kaggle release by Olist (version 2), joined on their keys with the customers, order items, products, sellers and payments files; one row per order.

        - Prediction point: at checkout, from what is known when the customer places the order, including the delivery date Olist promises then.
        - Task choice: the uploader's notebook predicts the review score, but a low score reaches ROC AUC 0.60 from the checkout features alone. We take the delivery time, which the data card suggests.
        - Target: the log of the days from order_purchase_timestamp to order_delivered_customer_date, because the durations are right-skewed. The metric is RMSLE on the days, computed after the inverse (`target_transform="log"`; Lennart, 2026-10-21).
        - Cohort: the review sample ends with the surveys sent on 2018-08-31, and a survey goes out at delivery or at the promised date. We keep orders placed before 2018-08-01 and promised by 2018-08-24, so every kept order would be in the sample whatever its delivery time (decision table).
        - Cohort: delivered orders (status "delivered" with a delivery date) with one seller. The orders file has one delivery date per order, which mixes shipments when an order has several sellers.
        - We drop order_approved_at, order_delivered_carrier_date and order_status (constant after the cohort filter), all recorded after checkout, and do not take shipping_limit_date from the items file, which is set at payment approval.
        - We drop the identifiers order_id, customer_id, customer_unique_id and product_id. We keep seller_id as a category: sellers recur over time, the seller is known at checkout, and its handling speed is part of the task.
        - Item and payment rows are aggregated per order (counts, sums, the payment methods joined as in "credit_card+voucher", the most installments). The product attributes are those of the first item; 98.0% of the kept orders hold one distinct product.
        - The promised date becomes estimated_delivery_days (days after the purchase). It is Olist's own estimate at checkout, so we keep it.
        - We translate the product categories with product_category_name_translation.csv (two without a translation keep their Portuguese name) and fix the misspelled product_name_lenght and product_description_lenght.
        - A product weight of 0 g is set to missing.
        - The zip code prefixes stay numeric: CEPs are assigned by region, so their order follows geography. The geolocation file (several coordinates per prefix) is not joined.
        - Duplicates: orders that share every feature are one customer buying the same product from the same seller in the same second; we keep them as distinct orders.
        - Split: monthly test windows with a one-month gap before each; training keeps only the orders delivered before the window starts (splits_comment, decision table). Without it the newest training orders are the fast ones, and untuned LightGBM with the purchase time as a number drops from mean R^2 0.353 to -0.054 on the log days. The gap costs a model without a numeric time axis 0.04 to 0.06 R^2.
        - Anomaly: the sample holds only orders with an answered survey, which over-represents slow deliveries if their customers answer more often. We assume the effect is the same in every month; the release cannot show it.
    """

    # Task
    target = "log_delivery_days"
    problem_type = "regression"
    metric = Metric.from_context(
        "rmsle",
        reason="A Kaggle dataset, not a competition: the data card suggests the delivery-time question but defines no metric; the task is our own. For a delivery time the error that matters is relative to the time (two days late on a three-day delivery is worse than on a thirty-day one), so RMSLE on the days.",
        target_transform="log",
    )

    # Splits
    splits_comment = """
        A model refit at the start of each month predicts the delivery time of the orders placed during that month. It trains on the orders placed at least one month before the refit whose delivery is known by then. The month just before the refit is a gap: many of its orders are still in transit at the refit, and the delivered ones are the fast ones, so a model that sees the purchase time as a number (AutoGluon keeps the epoch value next to the date parts) would learn that new orders are fast (see the decisions and curation_comments). The few older orders still in transit at the refit are left out of that window's training rows, as in hotel_booking_demand. The test windows are calendar months walking back from July 2018, the newest month the review sample covers in full (see curation_comments), until the training side would fall below 50% of the rows: 5 windows, March to July 2018, newest first. The convention's 9 windows for a dataset of this size do not fit above the 50% floor with monthly windows.
    """
    temporal = Temporal(on="order_purchase_timestamp", horizon=1, horizon_unit="months", gap=1, gap_unit="months")
    accepted_check_warnings = {
        "splits_rows_unused": "Four orders placed in January and February 2018 (148 to 208 days to delivery) are in no "
        "split: they were placed before the oldest test window and were still in transit when the newest one started.",
    }

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        return {
            "orders": pd.read_csv(raw_dir / "olist_orders_dataset.csv"),
            "customers": pd.read_csv(raw_dir / "olist_customers_dataset.csv"),
            "items": pd.read_csv(raw_dir / "olist_order_items_dataset.csv"),
            "products": pd.read_csv(raw_dir / "olist_products_dataset.csv"),
            "categories": pd.read_csv(raw_dir / "product_category_name_translation.csv"),
            "sellers": pd.read_csv(raw_dir / "olist_sellers_dataset.csv"),
            "payments": pd.read_csv(raw_dir / "olist_order_payments_dataset.csv"),
            # only the survey dates, for the evidence of the cut at the end of the review sample
            "reviews": pd.read_csv(
                raw_dir / "olist_order_reviews_dataset.csv", usecols=["order_id", "review_creation_date"]
            ),
        }

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        orders = raw["orders"]
        for col in ORDER_TIMESTAMPS:
            orders[col] = pd.to_datetime(orders[col], format=TIMESTAMP_FORMAT)

        # Cohort: delivered orders, placed before the end of the review sample and promised in time for a survey
        orders = orders.loc[
            (orders["order_status"] == "delivered")
            & orders["order_delivered_customer_date"].notna()
            & (orders["order_purchase_timestamp"] < PURCHASED_BEFORE)
            & (orders["order_estimated_delivery_date"] <= PROMISED_BY)
        ]

        # Items per order: counts and sums; the product and the seller of the first item
        items = raw["items"]
        per_order = items.groupby("order_id").agg(
            n_items=("order_item_id", "size"),
            n_products=("product_id", "nunique"),
            n_sellers=("seller_id", "nunique"),
            price=("price", "sum"),
            freight_value=("freight_value", "sum"),
        )
        first_item = items.loc[items["order_item_id"] == 1, ["order_id", "product_id", "seller_id"]]

        # Payments per order: the methods used, the largest number of installments, the total paid
        payments = (
            raw["payments"]
            .groupby("order_id")
            .agg(
                payment_type=("payment_type", lambda types: "+".join(sorted(set(types)))),
                payment_installments=("payment_installments", "max"),
                payment_value=("payment_value", "sum"),
            )
        )

        # Products: fix the misspelled names, translate the categories, a weight of 0 g is missing
        products = raw["products"].rename(
            columns={
                "product_name_lenght": "product_name_length",
                "product_description_lenght": "product_description_length",
            }
        )
        translation = dict(
            zip(
                raw["categories"]["product_category_name"],
                raw["categories"]["product_category_name_english"],
                strict=True,
            )
        )
        category = products["product_category_name"]
        products["product_category_name"] = category.map(translation).fillna(category)
        products["product_weight_g"] = products["product_weight_g"].where(products["product_weight_g"] > 0)

        df = (
            orders.merge(raw["customers"], on="customer_id", how="left")
            .merge(per_order, on="order_id", how="inner")
            .merge(first_item, on="order_id", how="inner")
            .merge(products, on="product_id", how="left")
            .merge(raw["sellers"], on="seller_id", how="left")
            .merge(payments, on="order_id", how="left")
        )
        # Cohort: one seller per order (one delivery date per order)
        df = df.loc[df["n_sellers"] == 1]

        # The promise and the target in days after the purchase
        purchase = df["order_purchase_timestamp"]
        df["estimated_delivery_days"] = _days(df["order_estimated_delivery_date"] - purchase)
        df["log_delivery_days"] = np.log(_days(df["order_delivered_customer_date"] - purchase))

        # Recorded after checkout, identifiers, the promised date (now in days) and the constant seller count. The
        # delivery date stays until `_make_splits`, which needs it to keep in-transit orders out of training.
        return drop_columns(
            df,
            [
                "order_id",
                "customer_id",
                "customer_unique_id",
                "product_id",
                "order_status",
                "order_approved_at",
                "order_delivered_carrier_date",
                "order_estimated_delivery_date",
                "n_sellers",
            ],
        )

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "customer_city",
                "customer_state",
                "seller_id",
                "seller_city",
                "seller_state",
                "product_category_name",
                "payment_type",
            ],
            datetime=["order_purchase_timestamp", "order_delivered_customer_date"],
        )

    def _make_splits(self, df: pd.DataFrame) -> SplitPlan:
        """Monthly windows after a one-month gap; train keeps only the orders delivered before the window starts."""
        time_on = self.temporal.on
        windows = TemporalSplits(window=1, unit="months", gap=1, min_train_fraction=0.5).splits(df, time_on)
        purchase = df[time_on]
        delivered = df["order_delivered_customer_date"].to_numpy()
        splits = {}
        for split, folds in windows.items():
            train, test = folds[0]
            start = purchase.iloc[test].min().normalize().replace(day=1)
            train = np.asarray(train)
            known = delivered[train] < np.datetime64(start)
            splits[split] = {0: (train[known].tolist(), test)}
        return SplitPlan(splits=splits, df=df.drop(columns=["order_delivered_customer_date"]))

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        orders = raw["orders"]
        purchase = pd.to_datetime(orders["order_purchase_timestamp"], format=TIMESTAMP_FORMAT)
        delivered = pd.to_datetime(orders["order_delivered_customer_date"], format=TIMESTAMP_FORMAT)
        promised = pd.to_datetime(orders["order_estimated_delivery_date"], format=TIMESTAMP_FORMAT)
        last_survey = pd.to_datetime(raw["reviews"]["review_creation_date"], format=TIMESTAMP_FORMAT).max()
        recent = (orders["order_status"] == "delivered") & delivered.notna() & (purchase >= "2018-05-01")
        recent &= purchase < "2018-09-01"
        months = pd.DataFrame(
            {
                "purchase month": purchase[recent].dt.strftime("%Y-%m"),
                "days": _days(delivered - purchase)[recent],
                "promised after cut": promised[recent] > PROMISED_BY,
            }
        )
        by_month = months.groupby("purchase month").agg(
            delivered_orders=("days", "size"),
            p50_days=("days", "median"),
            p90_days=("days", lambda d: d.quantile(0.9)),
            max_days=("days", "max"),
            promised_after_2018_08_24=("promised after cut", "sum"),
        )

        # Per test window: how many orders are still in transit when it starts, and how fast the known ones are
        placed = df[self.temporal.on]
        days = np.exp(df[self.target])
        delivered_df = placed + pd.to_timedelta(days * SECONDS_PER_DAY, unit="s")
        rows = []
        for month in pd.period_range("2018-03", "2018-07", freq="M")[::-1]:
            start, end, gap_start = month.start_time, (month + 1).start_time, (month - 1).start_time
            known = delivered_df < start
            last_month = (placed >= gap_start) & (placed < start)
            older = placed < gap_start
            rows.append(
                {
                    "test month": str(month),
                    "test rows": int(((placed >= start) & (placed < end)).sum()),
                    "last month: orders": int(last_month.sum()),
                    "last month: in transit": f"{(last_month & ~known).sum() / last_month.sum():.1%}",
                    "last month: median days, all": round(float(days[last_month].median()), 1),
                    "last month: median days, delivered": round(float(days[last_month & known].median()), 1),
                    "older: orders": int(older.sum()),
                    "older: in transit (left out)": int((older & ~known).sum()),
                }
            )
        return [
            Decision(
                f"Orders placed from August 2018 on are cut: the last survey was sent on {last_survey:%Y-%m-%d}",
                "The sample holds orders with an answered review, and the survey goes out at delivery or at the "
                "promised date. August orders are in it only when they arrived by the end of August, so their "
                "delivery times are cut short; June and July orders promised after 2018-08-24 are dropped too.",
                by_month.round(1),
            ),
            Decision(
                "Training rows are orders placed a month or more before the window and delivered before it starts",
                "At the start of a window many orders of the last month are still in transit, and the ones already "
                "delivered are the fast ones; a model that sees the purchase time as a number would learn that new "
                "orders are fast. So the last month before each window is a gap, and the few older orders still in "
                "transit are left out of that window's training rows.",
                pd.DataFrame(rows).set_index("test month"),
            ),
        ]
