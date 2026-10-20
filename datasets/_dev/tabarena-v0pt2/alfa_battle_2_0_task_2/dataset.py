"""Curated dataset definition for `alfa_battle_2_0_task_2` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    SplitPlan,
    TaskSummary,
    Temporal,
    TemporalSplits,
    drop_columns,
)

TRANSACTIONS_DIR = "train_transactions_contest"
TARGET_FILE = "train_target.csv"
FEATURES_FILE = "train_features.parquet"
CALENDAR_FILE = "issue_calendar.csv"

# The features (curation_comments, "Features"): the aggregates the top solutions of the competition share (1st place
# and 4th private place slides, 9th place code; see the record), per product over its transactions before the issue.
RUBLE_SCALE = 17.8209
"""`amnt` is a scaled log of the amount: exp(amnt * 17.8209) - 1 restores rubles (competition chat, used by the 1st,
9th and 15th place); 98.8% of the restored amounts are whole rubles."""
INFLOW_CODE = 2
"""`income_flag` 2 marks money coming in (8% of the transactions, median 5,600 rubles); 1 is spending."""
SALARY_RUB = 15_000
"""An inflow of at least this many rubles counts as salary-like (9th place)."""
RECENT_DAYS = (30, 90)
"""Windows before the issue for the recent-activity features (`days_before` runs from 1 to 359)."""
N_BLOCKS = 12
"""30-day blocks of the year before the issue, block 0 the newest."""
NIGHT_HOURS = (23, 0, 1, 2, 3)
HOUR_DIFF_BINS = {
    "0": (-0.5, 0.5),
    "1_2": (0.5, 2.5),
    "3_10": (2.5, 10.5),
    "11_100": (10.5, 100.5),
    "over_100": (100.5, np.inf),
}
"""Bins of the hours since the previous transaction (9th place)."""
CATEGORICAL_COLUMNS = [
    "currency",
    "operation_kind",
    "card_type",
    "operation_type",
    "operation_type_group",
    "ecommerce_flag",
    "payment_system",
    "income_flag",
    "mcc",
    "country",
    "city",
    "mcc_category",
    "day_of_week",
    "hour",
]
PIVOT_COLUMNS = [
    "operation_kind",
    "operation_type",
    "operation_type_group",
    "mcc_category",
    "currency",
    "payment_system",
    "ecommerce_flag",
    "income_flag",
    "country",
    "day_of_week",
]
"""Per value: count share, amount share and mean amount, for the values with at least `PIVOT_MIN_SHARE` of all
transactions."""
PIVOT_MIN_SHARE = 0.001
TOP_PIVOT_COLUMNS = {"mcc": 30, "card_type": 30}
"""Per value of the most frequent codes: count share and mean amount."""
MODE_COLUMNS = ["mcc", "mcc_category", "card_type", "operation_type", "city", "country"]
"""The mode (by count) and the last value, categorical, and the share of the mode."""
TX_COLUMNS = ["app_id", "transaction_number", "amnt", "hour_diff", "days_before", "weekofyear", *CATEGORICAL_COLUMNS]

# Issue months (curation_comments, "Time"): the week code of the latest transaction along `app_id`.
N_ISSUE_MONTHS = 24
ISSUE_WEEK_MAX_DAYS = 2  # a latest transaction at most this many days before the issue lies in the issue week
ISSUE_WEEK_WINDOW = 501  # products (with such a transaction) per rolling majority of the week code
GAP_SEARCH = range(20, 41)  # days between the issue dates of consecutive months that are tried
CALENDAR_MIN_TRANSACTIONS = 50  # a (month, days_before) cell of the calendar needs this many transactions

# Repeat clients (curation_comments, "Repeat clients"): products of one client share identical transactions.
LINK_WINDOW_DAYS = 28  # the transactions compared: the 28 days before each month's issue date
LINK_MIN_SHARED = 3  # a link needs at least 3 identical transactions in a window ...
LINK_MIN_SHARE = 0.8  # ... that are at least 80% of the transactions of the product with fewer in the window
LINK_MAX_HOLDERS = 20  # a transaction held by more products (a standard fee) is not used
DAY_OFFSET = 400  # calendar days run from -359 (the oldest transaction of month 0) to about 700
LINK_FIELDS = (  # field and bits: two transactions are the same when the day, the amount and all of these agree
    ("hour", 5),
    ("mcc", 7),
    ("card_type", 8),
    ("city", 8),
    ("operation_type", 5),
    ("currency", 4),
    ("country", 5),
    ("payment_system", 3),
    ("operation_kind", 3),
    ("income_flag", 2),
    ("ecommerce_flag", 2),
)

# Test windows: the 3 newest pairs of issue months; train is every earlier month (see `_make_splits`).
SPLIT_WINDOWS = TemporalSplits(window=2, unit="unique", n_windows=3)


def pivot_values(paths: list[Path]) -> dict[str, list[int]]:
    """The codes that get their own features: by share of all transactions (`PIVOT_COLUMNS`) or by rank."""
    columns = [*PIVOT_COLUMNS, *TOP_PIVOT_COLUMNS]
    counts = {column: pd.Series(dtype="int64") for column in columns}
    total = 0
    for path in paths:
        tx = pd.read_parquet(path, columns=columns)
        total += len(tx)
        for column in columns:
            counts[column] = counts[column].add(tx[column].value_counts(), fill_value=0)
    values = {}
    for column, n in counts.items():
        ranked = n.sort_index(kind="stable").sort_values(ascending=False, kind="stable")  # ties: the lower code first
        keep = (
            ranked.index[: TOP_PIVOT_COLUMNS[column]]
            if column in TOP_PIVOT_COLUMNS
            else ranked.index[ranked >= PIVOT_MIN_SHARE * total]
        )
        values[column] = sorted(int(v) for v in keep)
    return values


def aggregate_transactions(tx: pd.DataFrame, values: dict[str, list[int]]) -> pd.DataFrame:
    """One row per application from its card transactions (curation_comments, "Features").

    Two codes of the source become missing values first: `amnt` 0.0 ("0.0 corresponds to missing values", the
    organizers' feature table) and `hour_diff` -1 (the first transaction of the window). Counts include transactions
    without an amount; a statistic over no known amount stays missing.
    """
    tx = tx.sort_values(["app_id", "transaction_number"], kind="stable").reset_index(drop=True)
    rub = np.expm1(tx["amnt"].where(tx["amnt"] != 0.0) * RUBLE_SCALE)
    inflow = tx["income_flag"].eq(INFLOW_CODE)
    t = pd.DataFrame(
        {
            "app_id": tx["app_id"],
            "rub": rub,
            "out_rub": rub.where(~inflow),
            "in_rub": rub.where(inflow),
            "hour_diff": tx["hour_diff"].where(tx["hour_diff"] != -1).astype("float64"),
            "days_before": tx["days_before"],
            "hour": tx["hour"],
            "night": tx["hour"].isin(NIGHT_HOURS),
            "no_amount": rub.isna(),
            "block": (tx["days_before"] - 1) // 30,
        }
    )
    app = t["app_id"]
    g = t.groupby("app_id", sort=True)
    apps = g.size().index

    # Statistics of the amount, the gaps, the recency and the hour.
    stats = g.agg(
        n_transactions=("rub", "size"),
        share_no_amount=("no_amount", "mean"),
        rub_sum=("rub", "sum"),
        rub_mean=("rub", "mean"),
        rub_median=("rub", "median"),
        rub_std=("rub", "std"),
        rub_min=("rub", "min"),
        rub_max=("rub", "max"),
        hour_diff_mean=("hour_diff", "mean"),
        hour_diff_median=("hour_diff", "median"),
        hour_diff_std=("hour_diff", "std"),
        hour_diff_max=("hour_diff", "max"),
        days_before_min=("days_before", "min"),
        days_before_max=("days_before", "max"),
        days_before_mean=("days_before", "mean"),
        days_before_median=("days_before", "median"),
        hour_mean=("hour", "mean"),
        hour_std=("hour", "std"),
        share_night=("night", "mean"),
    )
    quantiles = g["rub"].quantile([0.05, 0.25, 0.75, 0.95]).unstack()
    quantiles.columns = [f"rub_q{round(q * 100):02d}" for q in quantiles.columns]
    gap_quantiles = g["hour_diff"].quantile([0.25, 0.75]).unstack()
    gap_quantiles.columns = [f"hour_diff_q{round(q * 100):02d}" for q in gap_quantiles.columns]
    known_gap = t["hour_diff"].notna().groupby(app).sum()
    gap_bins = pd.DataFrame(
        {
            f"share_hour_diff_{name}": t["hour_diff"].between(lo, hi, inclusive="right").groupby(app).sum() / known_gap
            for name, (lo, hi) in HOUR_DIFF_BINS.items()
        }
    )
    blocks = [stats, quantiles, gap_quantiles, gap_bins]

    # Per value of a column: count share, amount share and mean amount.
    total_rub = stats["rub_sum"].replace(0.0, np.nan)
    for column in [*PIVOT_COLUMNS, *TOP_PIVOT_COLUMNS]:
        codes = values[column]
        by_value = t["rub"].groupby([app, tx[column]], sort=True).agg(["size", "sum", "mean"])
        by_value = by_value[by_value.index.get_level_values(1).isin(codes)]
        count = by_value["size"].unstack().reindex(index=apps, columns=codes).fillna(0)
        part = {"share": count.div(stats["n_transactions"], axis=0)}
        if column in PIVOT_COLUMNS:
            amount = by_value["sum"].unstack().reindex(index=apps, columns=codes).fillna(0)
            part["amount_share"] = amount.div(total_rub, axis=0)
        part["mean_rub"] = by_value["mean"].unstack().reindex(index=apps, columns=codes)
        for name, frame in part.items():
            frame.columns = [f"{name}_{column}_{code}" for code in codes]
            blocks.append(frame)

    # Diversity: distinct values per column; mode, its share and the last value of the main columns.
    distinct = tx.groupby("app_id", sort=True)[CATEGORICAL_COLUMNS].nunique()
    distinct.columns = [f"n_distinct_{column}" for column in CATEGORICAL_COLUMNS]
    last = tx.groupby("app_id", sort=True)[MODE_COLUMNS].last()
    last.columns = [f"last_{column}" for column in MODE_COLUMNS]
    blocks += [distinct, last]
    for column in MODE_COLUMNS:
        n = tx.groupby(["app_id", column], sort=True).size().rename("n").reset_index()
        n = n.sort_values(["app_id", "n", column], ascending=[True, False, True], kind="stable")
        mode = n.drop_duplicates("app_id").set_index("app_id")
        blocks.append(
            pd.DataFrame({f"mode_{column}": mode[column], f"share_mode_{column}": mode["n"] / stats["n_transactions"]})
        )

    # Money in against money out.
    flows = g.agg(
        out_sum=("out_rub", "sum"),
        out_mean=("out_rub", "mean"),
        out_max=("out_rub", "max"),
        out_count=("out_rub", "count"),
        in_sum=("in_rub", "sum"),
        in_mean=("in_rub", "mean"),
        in_max=("in_rub", "max"),
        in_count=("in_rub", "count"),
    )
    flows["out_in_ratio"] = flows["out_sum"] / flows["in_sum"].replace(0.0, np.nan)
    flows["n_salary_inflows"] = (t["in_rub"] >= SALARY_RUB).groupby(app).sum()
    # 30-day blocks within the product's history (newer than its oldest transaction): spending and income per block.
    oldest = stats["days_before_max"].sub(1).floordiv(30).to_numpy()
    within = np.arange(N_BLOCKS)[None, :] <= oldest[:, None]
    by_block = {}
    for side in ("out_rub", "in_rub"):
        summed = t[side].fillna(0.0).groupby([app, t["block"]], sort=True).sum().unstack()
        by_block[side] = summed.reindex(index=apps, columns=range(N_BLOCKS)).fillna(0.0).where(within)
    income = by_block["in_rub"]
    flows["in_block_mean"] = income.mean(axis=1)
    flows["in_block_std"] = income.std(axis=1)
    flows["in_block_max"] = income.max(axis=1)
    flows["n_blocks_with_income"] = (income > 0).sum(axis=1)
    spend = by_block["out_rub"]
    spend_share = spend.div(flows["out_sum"].replace(0.0, np.nan), axis=0)
    spend.columns = [f"out_sum_block_{b}" for b in range(N_BLOCKS)]
    spend_share.columns = [f"share_out_block_{b}" for b in range(N_BLOCKS)]
    blocks += [flows, spend, spend_share]

    # Daily activity: active days, per-day counts and spending, gaps between active days.
    daily = t.groupby(["app_id", "days_before"], sort=True).agg(n=("rub", "size"), out=("out_rub", "sum"))
    day_app = daily.index.get_level_values(0)
    day = pd.Series(daily.index.get_level_values(1), index=daily.index)
    gap = day.groupby(day_app).diff()
    by_day = daily.groupby(day_app)
    activity = pd.DataFrame(
        {
            "active_days": by_day.size(),
            "daily_count_mean": by_day["n"].mean(),
            "daily_count_max": by_day["n"].max(),
            "daily_count_std": by_day["n"].std(),
            "daily_out_mean": by_day["out"].mean(),
            "daily_out_max": by_day["out"].max(),
            "daily_out_std": by_day["out"].std(),
            "gap_days_max": gap.groupby(day_app).max(),
            "gap_days_mean": gap.groupby(day_app).mean(),
            "gap_days_std": gap.groupby(day_app).std(),
            "gap_days_max_30d": gap.where(day <= RECENT_DAYS[0]).groupby(day_app).max(),
            "active_weeks": (day // 7).groupby(day_app).nunique(),
        }
    )
    for days in RECENT_DAYS:
        activity[f"active_days_{days}d"] = (day <= days).groupby(day_app).sum()
    activity["transactions_per_active_week"] = stats["n_transactions"] / activity["active_weeks"]
    blocks.append(activity)

    # A balance proxy: the running sum of money in less money out, in transaction order.
    running = (t["in_rub"].fillna(0.0) - t["out_rub"].fillna(0.0)).groupby(app).cumsum()
    by_running = running.groupby(app)
    blocks.append(
        pd.DataFrame(
            {
                "balance_min": by_running.min(),
                "balance_max": by_running.max(),
                "balance_mean": by_running.mean(),
                "balance_last": by_running.last(),
                "balance_min_days_before": t["days_before"].to_numpy()[by_running.idxmin().to_numpy()],
                "balance_max_days_before": t["days_before"].to_numpy()[by_running.idxmax().to_numpy()],
            },
            index=apps,
        )
    )

    # The last 30 and 90 days, and how they compare with the year.
    recent = pd.DataFrame(index=apps)
    for days in RECENT_DAYS:
        inside = t["days_before"] <= days
        r = t[inside].groupby("app_id", sort=True)
        counts = (
            pd.DataFrame(
                {
                    f"n_transactions_{days}d": r.size(),
                    f"rub_sum_{days}d": r["rub"].sum(),
                    f"out_sum_{days}d": r["out_rub"].sum(),
                    f"in_sum_{days}d": r["in_rub"].sum(),
                    f"n_distinct_mcc_{days}d": tx.loc[inside, "mcc"].groupby(app[inside]).nunique(),
                }
            )
            .reindex(apps)
            .fillna(0)
        )
        recent = recent.join(counts)
        recent[f"rub_mean_{days}d"] = r["rub"].mean().reindex(apps)
        recent[f"rub_max_{days}d"] = r["rub"].max().reindex(apps)
    recent["out_ratio_30d_90d"] = recent["out_sum_30d"] / recent["out_sum_90d"].replace(0.0, np.nan)
    recent["out_ratio_90d_year"] = recent["out_sum_90d"] / flows["out_sum"].replace(0.0, np.nan)
    recent["count_ratio_30d_90d"] = recent["n_transactions_30d"] / recent["n_transactions_90d"].replace(0, np.nan)
    blocks.append(recent)

    features = pd.concat(blocks, axis=1).drop(columns=["active_weeks"])
    numeric = [c for c in features.columns if not c.startswith(("mode_", "last_"))]
    features[numeric] = features[numeric].astype("float32")
    # The latest transaction (highest transaction_number) dates the issue: its week code and days before the issue.
    latest = g[["days_before"]].last().rename(columns={"days_before": "latest_days_before"})
    latest["latest_week_code"] = tx.groupby("app_id", sort=True)["weekofyear"].last()
    return pd.concat([features, latest], axis=1)


def rolling_months(app_id: pd.Series, week_code: pd.Series, days_before: pd.Series) -> np.ndarray:
    """First pass of `issue_months`: the issue month of each product from runs of week codes along `app_id`.

    Products whose latest transaction is at most `ISSUE_WEEK_MAX_DAYS` days before the issue carry the week code of
    the issue week. Along `app_id` (the issue order) these codes form runs, one per month; a rolling majority over
    `ISSUE_WEEK_WINDOW` such products removes the noise at week boundaries, a new month starts where the majority code
    changes, and every other product belongs to the month of the closest such product before it.
    """
    order = np.argsort(app_id.to_numpy(), kind="stable")
    ids, codes, days = app_id.to_numpy()[order], week_code.to_numpy()[order], days_before.to_numpy()[order]
    near = days <= ISSUE_WEEK_MAX_DAYS
    near_ids, near_codes = ids[near], codes[near]
    half = ISSUE_WEEK_WINDOW // 2
    best_count = np.zeros(len(near_codes), dtype=np.int64)
    best_code = np.zeros(len(near_codes), dtype=near_codes.dtype)
    position = np.arange(len(near_codes))
    upper = np.minimum(position + half, len(near_codes) - 1)
    lower = position - half - 1
    for code in np.unique(near_codes):  # ascending: a tie keeps the smaller code
        hits = np.concatenate([[0], np.cumsum(near_codes == code)])
        count = hits[upper + 1] - hits[np.maximum(lower, -1) + 1]
        better = count > best_count
        best_count[better], best_code[better] = count[better], code
    month_of_near = np.concatenate([[0], np.cumsum(best_code[1:] != best_code[:-1])])
    result = np.empty(len(ids), dtype=np.int64)
    result[order] = month_of_near[np.maximum(np.searchsorted(near_ids, ids, side="right") - 1, 0)]
    return result


def calendar_months(
    months: np.ndarray, week_code: pd.Series, days_before: pd.Series, calendar_counts: np.ndarray
) -> np.ndarray:
    """Second pass of the issue months: move the products whose latest transaction fits a neighbouring month only.

    All products of a month share one issue date, so (days before the issue -> week code) is one calendar per month;
    `calendar_counts[m, d, c]` counts all transactions of month-m products made `d` days before the issue with week
    code `c`. A product whose latest transaction disagrees with its month's calendar and agrees with the calendar of
    exactly one neighbouring month moves there: the rolling majority switches late at the edges of the months whose
    issue date is a Tuesday, where the products of the issue week carry two codes.
    """
    codes, days = week_code.to_numpy().astype(np.int64), days_before.to_numpy().astype(np.int64)
    calendar = calendar_counts.argmax(axis=2)
    known = calendar_counts.sum(axis=2) >= CALENDAR_MIN_TRANSACTIONS
    last = calendar.shape[0] - 1

    def agrees(month: np.ndarray) -> np.ndarray:
        return known[month, days] & (calendar[month, days] == codes)

    previous_ok = (months > 0) & agrees(np.maximum(months - 1, 0))
    next_ok = (months < last) & agrees(np.minimum(months + 1, last))
    move = ~agrees(months) & (previous_ok ^ next_ok)
    return np.where(move & previous_ok, months - 1, np.where(move & next_ok, months + 1, months))


def issue_calendar(calendar_counts: np.ndarray) -> pd.DataFrame:
    """Per month: the days from month 0's issue date (`issue_day`), from the week-code calendars of all transactions.

    `calendar_counts[m, d, c]` counts the transactions of month-m products made `d` days before the issue with week
    code `c`; the dominant code per (m, d) is month m's calendar, and `calendar_share` is the smallest share of the
    dominant code over the (m, d) cells. Read `gap` days further back, month m + 1's calendar equals month m's for
    exactly one gap in `GAP_SEARCH`: the days between the two issue dates (`agreement` is the share of agreeing cells
    at that gap; the second best gap stays far below).
    """
    calendar = calendar_counts.argmax(axis=2)
    totals = calendar_counts.sum(axis=2)
    known = totals >= CALENDAR_MIN_TRANSACTIONS
    share = np.where(known, calendar_counts.max(axis=2) / np.maximum(totals, 1), np.nan)
    gaps, agreements, runner_up = [], [np.nan], [np.nan]
    for month in range(calendar.shape[0] - 1):
        agreement = {}
        for gap in GAP_SEARCH:
            d = np.arange(1, calendar.shape[1] - gap)
            ok = known[month, d] & known[month + 1, d + gap]
            agreement[gap] = float((calendar[month, d][ok] == calendar[month + 1, d + gap][ok]).mean())
        best = max(agreement, key=agreement.get)
        assert agreement[best] >= 0.99, f"months {month} and {month + 1}: no gap fits ({agreement[best]:.3f})"
        gaps.append(best)
        agreements.append(agreement[best])
        runner_up.append(sorted(agreement.values())[-2])
    return pd.DataFrame(
        {
            "issue_day": np.concatenate([[0], np.cumsum(gaps)]),
            "agreement": agreements,
            "second_best_agreement": runner_up,
            "calendar_share": np.nanmin(share, axis=1),
        }
    ).rename_axis("issue_month")


def _mix64(x: np.ndarray) -> np.ndarray:
    """The splitmix64 finalizer: a fixed bijective mix of 64-bit integers (the same on every machine)."""
    x = (x ^ (x >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)
    x = (x ^ (x >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)
    return x ^ (x >> np.uint64(31))


def transaction_keys(tx: pd.DataFrame, day: np.ndarray) -> np.ndarray:
    """A 64-bit key per transaction from its calendar day, amount and `LINK_FIELDS`: equal for the same transaction."""
    packed = (day + DAY_OFFSET).astype(np.uint64)
    assert ((day + DAY_OFFSET) >= 0).all(), "calendar day below the offset"
    assert ((day + DAY_OFFSET) < 2**11).all(), "calendar day does not fit in 11 bits"
    for field, bits in LINK_FIELDS:
        values = tx[field].to_numpy().astype(np.uint64)
        assert (values < 2**bits).all(), f"{field} does not fit in {bits} bits"
        packed = (packed << np.uint64(bits)) | values
    amount = tx["amnt"].to_numpy(dtype=np.float64).view(np.uint64)
    return _mix64(packed ^ _mix64(amount))


def window_links(app: np.ndarray, key: np.ndarray) -> pd.DataFrame:
    """Pairs of products (`app_x` < `app_y`) that share identical transactions in one window (`LINK_*` rules)."""
    frame = pd.DataFrame({"key": key, "app": app}).drop_duplicates()
    n_tx = frame["app"].value_counts()
    holders = frame.groupby("key")["app"].transform("size")
    shared = frame[(holders >= 2) & (holders <= LINK_MAX_HOLDERS)]
    pairs = shared.merge(shared, on="key")
    pairs = pairs[pairs["app_x"] < pairs["app_y"]]
    n_shared = pairs.groupby(["app_x", "app_y"]).size().rename("n_shared").reset_index()
    smaller = np.minimum(n_tx.reindex(n_shared["app_x"]).to_numpy(), n_tx.reindex(n_shared["app_y"]).to_numpy())
    keep = (n_shared["n_shared"] >= LINK_MIN_SHARED) & (n_shared["n_shared"] >= LINK_MIN_SHARE * smaller)
    return n_shared.loc[keep, ["app_x", "app_y"]]


def client_keys(app_ids: np.ndarray, links: pd.DataFrame) -> np.ndarray:
    """The smallest `app_id` of each product's connected component of links: one key per client."""
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components

    index = pd.Index(app_ids)
    x, y = index.get_indexer(links["app_x"]), index.get_indexer(links["app_y"])
    graph = coo_matrix((np.ones(len(x), dtype=np.int8), (x, y)), shape=(len(index), len(index)))
    _, component = connected_components(graph, directed=False)
    smallest = pd.Series(app_ids).groupby(component).transform("min")
    return smallest.to_numpy()


class AlfaBattle20Task2(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a client default on a credit product the bank has just issued?",
        use_case=(
            "When a bank issues a credit product, it scores the client's default risk from the client's card "
            "transactions, to decide on the product and its terms."
        ),
        row="One issued credit product, with the client's card transactions of the year before.",
        predicted="Whether the client defaulted on it (2.8% did); the source states no horizon.",
        known=(
            "The product type and 513 summaries of the year's card transactions (amounts, timing, merchants, money in"
            " and out, recent activity)."
        ),
        split=(
            "Each test window is two months of issues at the end of the period; training is every earlier issue, "
            "without the products of clients who also have one in the test window."
        ),
        changes=(
            "We reconstruct the issue month from the transactions, as the data has no dates, and summarise the "
            "transactions like the competition's top solutions."
        ),
        fit="approximate",
        fit_reason=(
            "The issue months are reconstructed rather than given, and the default has no stated horizon, so the "
            "newest training products may not yet show a default that will come."
        ),
    )

    # Dataset
    unique_name = "alfa_battle_2_0_task_2"
    year = "2020"
    domain = "finance"
    source = "Other"
    source_url = "https://boosters.pro/championship/alfabattle2/overview"
    license = (
        "Competition rules (Alfa Battle 2.0 Rules, Sec. 3.10 and 5.6): participants must not publish or pass on the "
        "data. Alfa-Bank later allowed its use in scientific publications and theses "
        "(habr.com/ru/companies/alfa/articles/551130) and re-hosted it for its 2022 ODS.ai competition; the Kaggle "
        "mirror mrmorj/alfabattle-20 labels it CC0-1.0 (the uploader's label)"
    )
    data_tags = ("Anonymized",)
    download_description = """
        The competition files were hosted on boosters.pro, whose download links (https://boosters.pro/api/ch/files/pub/<file>) now redirect to a 404 page (checked 2026-10-06). Alfa-Bank re-hosted them, without a login, for its 2022 ODS.ai competition on the same data (https://ods.ai/competitions/dl-fintech-card-transactions, data tab); the archive holds the organizer's files of November 2020. We download the labelled train files (the test labels were never released).

        mkdir -p local-data-warehouse/alfa_battle_2_0_task_2 && cd local-data-warehouse/alfa_battle_2_0_task_2
        wget https://storage.yandexcloud.net/ds-ods/files/materials/3634ff95/train_target.csv
        wget https://storage.yandexcloud.net/ds-ods/files/materials/6e991b7f/train_transactions_contest.zip
        unzip train_transactions_contest.zip -x '__MACOSX/*' && rm train_transactions_contest.zip

        This gives train_target.csv (10,498,134 bytes, sha256 470ea19c...3d74) and the 50 files train_transactions_contest/part_*.parquet (4,242,459,450 bytes). Fallback: the Kaggle mirror mrmorj/alfabattle-20 (uploaded 2020-12-12) holds byte-identical files (sha256 compared 2026-10-07) as alfabattle2_train_target.csv and alfabattle2_train_transactions_contest/train_transactions_contest/part_*.parquet; rename them to the paths above. `_prepare_raw_files` aggregates the transactions once into train_features.parquet.
    """
    bibtex = r"""
        @misc{AlfaBank2020AlfaBattle2,
          author = {{Alfa-Bank}},
          title  = {{AlfaBattle} 2.0, Task 2: Credit Scoring from Card Transactions},
          year   = {2020},
          howpublished = {\url{https://boosters.pro/championship/alfabattle2/overview}},
          note   = {Data science competition on Boosters.pro, 12 December 2020 to 18 January 2021, final on 29 January 2021}
        }
    """
    curation_comments = """
        We start with train_target.csv and the 50 train transaction files of AlfaBattle 2.0, task 2 (Alfa-Bank on Boosters.pro, 2020), from the organizer's archive on ODS.ai.

        - Prediction point: a credit product is issued. The bank knows the product type and the client's card transactions of the preceding year (Alfa-Bank on Habr, 2021). The target `default` is the source's flag "1 - факт ухода в дефолт" (1: the applicant defaulted), with no horizon stated.
        - Features: the source is an event sequence per product; we aggregate it like the competition's top solutions (record), whose boosting reached 0.774-0.780 private ROC AUC against 0.737 public for the organizers' 127-feature baseline. Their label encodings, embeddings and sequence-model scores are modelling steps and stay out.
        - We restore rubles (`exp(amnt * 17.8209) - 1`, as the 1st, 9th and 15th place did; 98.8% come out whole) and aggregate: amount, gap and recency statistics; count share, amount share and mean amount per value of ten coded columns and of the 30 most frequent `mcc` and `card_type` codes; distinct values, mode and last values; money in (`income_flag` 2) against out and twelve 30-day blocks; daily activity; a running balance proxy; the last 30 and 90 days. Untuned LightGBM: ROC AUC 0.787 / 0.771 / 0.772 on the windows, 0.774 / 0.757 / 0.763 with the 127.
        - The coded values and the 30 most frequent codes are chosen over all transactions, test windows included: a pipeline choice that approximates the task (a deployed model would choose from its own history), not a value computed from test rows; kept (Lennart, 2026-10-19).
        - Two codes of the source become missing values before aggregating: `amnt` 0.0, which "corresponds to missing values", and `hour_diff` -1, which marks the first transaction of the window. Counts include every transaction, and a statistic over no known amount stays missing.
        - Time: the data has no dates, but later applications have a later `app_id`. The week code of each product's latest transaction splits `app_id` into 24 runs, one per issue month (`rolling_months`); `calendar_months` moves 292 products at the month edges to the month whose calendar fits them, and `issue_calendar` finds one issue date per month (first decision; `app_id` 0-4 stay in month 0). We keep `issue_month` (0-23) as the time column and drop `app_id` and the latest-transaction fields, which only date the issue.
        - Repeat clients: there is no client id, but a client's products issued less than a year apart share identical transactions. We link two products by the `LINK_*` rules (at least 3 identical transactions, 80% of the smaller product's, in the 28 days before an issue date) and take connected products as one client (`client_keys`). In the newest window the test products whose client's earlier product defaulted default in 95.6% of cases, the others in 2.5% (second decision). That earlier flag was most likely set after the test product was issued, so it carries the test product's own outcome. `_make_splits` removes from each training side the products of clients with a product in the test window (as in hotel_booking_demand: a training label not known at the prediction point is left out).
        - Note: the default rate rises from 2.0-2.6% (months 1-12) to 3.0-3.4% (months 18-23). The competition labelled 7 later months with the same flag, so we see no sign of right-censoring.
        - No duplicate rows.
    """

    # Task
    target = "default"
    problem_type = "binary_classification"

    # Splits
    splits_comment = """
        A scoring model is refit on all products issued so far and used for the next two months. We use 3 test windows of two issue months each, newest first: months 22-23, 20-21 and 18-19, each training on all earlier months. From each training side we remove the products of clients that also have a product in the test window (curation_comments, "Repeat clients"): their default flags were not known when the test products were issued. The competition trained on these 24 months and tested on the 7 months after a month that was not released; its test labels are not public, so we split the 24 labelled months, and 3 windows of 7 months would leave less than half of the data for training. The flag of any product issued in the 12 months before a window may still change after the window starts, so the other training products of those months hold labels a deployed model would not have had yet, as in the competition; a 12-month gap would leave 13-27% of the rows for training.
    """
    temporal = Temporal(on="issue_month", horizon=2, horizon_unit="months")
    accepted_check_warnings = {
        "splits_rows_unused": "By design: these products of months 0-17 belong to clients with a product in each of "
        "the three test windows, so the repeat-client filter removes them from every training side (curation_comments, "
        "'Repeat clients').",
    }

    # The raw transactions (270M rows) are aggregated and linked once; `_load_raw` starts from the result.
    prepared_raw_files = (FEATURES_FILE, CALENDAR_FILE)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        # every partition holds all transactions of its products, so the partitions are read one by one
        paths = sorted((raw_dir / TRANSACTIONS_DIR).glob("part_*.parquet"))
        values = pivot_values(paths)
        features = pd.concat([aggregate_transactions(pd.read_parquet(p, columns=TX_COLUMNS), values) for p in paths])
        features = features.sort_index(kind="stable")
        app_ids = features.index.to_numpy()
        latest_code, latest_days = features["latest_week_code"], features["latest_days_before"]
        first_pass = rolling_months(features.index.to_series(), latest_code, latest_days)
        assert first_pass.max() + 1 == N_ISSUE_MONTHS, f"expected {N_ISSUE_MONTHS} issue months"
        month_of = np.full(app_ids.max() + 1, -1, dtype=np.int64)
        month_of[app_ids] = first_pass

        # the week-code calendar of every month, from all transactions: the second pass of the months and the days
        # between the issue dates
        counts = np.zeros(N_ISSUE_MONTHS * 360 * 54, dtype=np.int64)
        for path in paths:
            tx = pd.read_parquet(path, columns=["app_id", "days_before", "weekofyear"])
            month = month_of[tx["app_id"].to_numpy()]
            cell = (month * 360 + tx["days_before"].to_numpy()) * 54 + tx["weekofyear"].to_numpy()
            counts += np.bincount(cell, minlength=len(counts))
        counts = counts.reshape(N_ISSUE_MONTHS, 360, 54)
        months = calendar_months(first_pass, latest_code, latest_days, counts)
        month_of[app_ids] = months
        calendar = issue_calendar(counts)
        days = calendar["issue_day"].to_numpy()

        # repeat clients: identical transactions in the 28 days before each month's issue date
        starts = days - LINK_WINDOW_DAYS
        by_window: dict[int, list[tuple[np.ndarray, np.ndarray]]] = {w: [] for w in range(N_ISSUE_MONTHS - 1)}
        columns = ["app_id", "days_before", "amnt", *(field for field, _ in LINK_FIELDS)]
        for path in paths:
            tx = pd.read_parquet(path, columns=columns)
            day = days[month_of[tx["app_id"].to_numpy()]] - tx["days_before"].to_numpy()
            window = np.searchsorted(starts, day, side="right") - 1
            inside = (window >= 0) & (window < N_ISSUE_MONTHS - 1) & (day < days[np.clip(window, 0, None)])
            keys = transaction_keys(tx[inside], day[inside])
            apps, windows = tx["app_id"].to_numpy()[inside], window[inside]
            for w in np.unique(windows):
                by_window[int(w)].append((apps[windows == w], keys[windows == w]))
        links = pd.concat(
            [
                window_links(np.concatenate([a for a, _ in parts]), np.concatenate([k for _, k in parts]))
                for parts in by_window.values()
                if parts
            ]
        ).drop_duplicates()

        features["issue_month"] = months
        features["client_key"] = client_keys(app_ids, links)
        features.index.name = "app_id"
        features.reset_index().to_parquet(raw_dir / FEATURES_FILE, index=False)
        calendar.to_csv(raw_dir / CALENDAR_FILE)

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        return {
            "features": pd.read_parquet(raw_dir / FEATURES_FILE),
            "calendar": pd.read_csv(raw_dir / CALENDAR_FILE, index_col="issue_month"),
            "target": pd.read_csv(raw_dir / TARGET_FILE),
        }

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        features, target = raw["features"], raw["target"]
        df = target.merge(features, on="app_id", how="inner", validate="one_to_one")
        assert len(df) == len(target) == len(features), "every labelled product has transactions"
        df.insert(0, "issue_month", df.pop("issue_month"))
        df["default"] = df.pop("flag").map({1: "Yes", 0: "No"})
        # `app_id` only orders the products (now `issue_month`); the latest-transaction fields only date the issue
        # (`days_before_min` keeps the days since the latest transaction). `client_key` stays for `_make_splits`,
        # which removes it.
        return drop_columns(df, ["app_id", "latest_week_code", "latest_days_before"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        codes = [c for c in df.columns if c.startswith(("mode_", "last_"))]  # transaction codes, not quantities
        return FeatureTypes(categorical=["product", *codes])

    def _make_splits(self, df: pd.DataFrame) -> SplitPlan:
        # The declarative windows, then each training side without the products of the window's clients.
        windows = SPLIT_WINDOWS.splits(df, self.temporal.on)
        client = df["client_key"].to_numpy()
        splits = {}
        for repeat, folds in windows.items():
            train, test = (np.asarray(side) for side in folds[0])
            same_client = np.isin(client[train], np.unique(client[test]))
            splits[repeat] = {0: (train[~same_client].tolist(), test.tolist())}
        return SplitPlan(splits=splits, df=drop_columns(df, ["client_key"]))

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        features, target = raw["features"], raw["target"]
        frame = target.merge(features, on="app_id")
        near = frame[frame["latest_days_before"] <= ISSUE_WEEK_MAX_DAYS]
        code_share = near.groupby("issue_month")["latest_week_code"].agg(
            week_code=lambda s: int(s.mode().iloc[0]),
            share=lambda s: round(float(s.value_counts(normalize=True).iloc[0]), 3),
        )
        months = frame.groupby("issue_month").agg(
            first_app_id=("app_id", "min"),
            last_app_id=("app_id", "max"),
            products=("flag", "size"),
            default_rate=("flag", "mean"),
        )
        months = months.join(raw["calendar"])
        months["days_since_previous"] = months["issue_day"].diff()
        months = months.join(code_share)
        months["default_rate"] = months["default_rate"].round(4)
        first_pass = rolling_months(frame["app_id"], frame["latest_week_code"], frame["latest_days_before"])
        moved = int((frame["issue_month"].to_numpy() != first_pass).sum())

        clients = frame.groupby("client_key")["app_id"].transform("size")
        two_in_one_month = int(
            frame[clients > 1].groupby("client_key")["issue_month"].agg(lambda s: s.duplicated().any()).sum()
        )
        ordered = frame.sort_values("issue_month", kind="stable").reset_index(drop=True)
        rows = []
        for repeat, folds in SPLIT_WINDOWS.splits(ordered, "issue_month").items():
            train, test = ordered.iloc[folds[0][0]], ordered.iloc[folds[0][1]]
            removed = train[train["client_key"].isin(test["client_key"])]
            earlier = removed.groupby("client_key")["flag"].max()  # 1 when any earlier product of the client defaulted
            linked = test[test["client_key"].isin(earlier.index)]
            earlier_flag = linked["client_key"].map(earlier)
            others = test[~test["client_key"].isin(earlier.index)]
            rows.append(
                {
                    "split": repeat,
                    "test months": f"{test['issue_month'].min()}-{test['issue_month'].max()}",
                    "test products": len(test),
                    "test products with an earlier product of the client": len(linked),
                    "training products removed": len(removed),
                    "training products kept": len(train) - len(removed),
                    "test products whose client's earlier product defaulted": int((earlier_flag == 1).sum()),
                    "their default rate": round(float(linked["flag"][earlier_flag == 1].mean()), 3),
                    "default rate when it did not": round(float(linked["flag"][earlier_flag == 0].mean()), 4),
                    "default rate of the other test products": round(float(others["flag"].mean()), 4),
                }
            )
        return [
            Decision(
                "Issue month reconstructed from the week codes of the transactions",
                "Along app_id (the issue order) the week code of a product's latest transaction marks 24 runs, and 11 "
                "of the 12 codes recur in the second year: 24 monthly issue dates of two years. `share` is the share "
                "of products with the run's code among those whose latest transaction is at most 2 days before the "
                "issue (months 7 and 16, issued on a Tuesday, mix two codes). `issue_day` and `days_since_previous` "
                "come from the week-code calendars of all transactions (`issue_calendar`): `agreement` is the share of "
                "days-before values on which a month's calendar equals the previous month's at that gap, "
                "`second_best_agreement` the same at the next best gap, and `calendar_share` the smallest share of a "
                f"month's dominant week code per days-before value. `calendar_months` moved {moved} products to a "
                "neighbouring month.",
                months,
            ),
            Decision(
                "Training sides without the products of the test window's clients",
                "A product is linked to the client's other products by identical transactions: "
                f"{int((clients > 1).sum()):,} products belong to a client with several products, "
                f"{int((clients > 1).groupby(frame['client_key']).any().sum()):,} clients, of whom {two_in_one_month} "
                "have two products in one month. The earlier product's default flag was not known when the test "
                "product was issued, so the earlier product is removed from the training side.",
                pd.DataFrame(rows).set_index("split"),
            ),
        ]
