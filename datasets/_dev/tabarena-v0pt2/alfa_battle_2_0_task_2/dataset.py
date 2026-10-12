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
    Temporal,
    TemporalSplits,
    drop_columns,
)

TRANSACTIONS_DIR = "train_transactions_contest"
TARGET_FILE = "train_target.csv"
FEATURES_FILE = "train_features.parquet"
CALENDAR_FILE = "issue_calendar.csv"

# The organizers' boosting baseline (github.com/smirnovevgeny/AlfaBattle2.0, baseline_boosting/baseline.ipynb):
# `extract_basic_aggregations(transactions, cat_columns=["mcc_category", "day_of_week", "operation_type"])`. The codes
# of each column, from the organizers' feature table (Habr 2021): 28, 7 and 22 values, numbered from 1.
PIVOT_COLUMNS = {"mcc_category": 28, "day_of_week": 7, "operation_type": 22}
NUMERIC_AGGREGATIONS = {
    "amnt": ["mean", "median", "sum", "std"],
    "hour_diff": ["max", "mean", "median", "var", "std"],
    "days_before": ["min", "max", "median"],
}
AGGREGATE_COLUMNS = ["app_id", "amnt", "hour_diff", "days_before", "weekofyear", "transaction_number", *PIVOT_COLUMNS]

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


def aggregate_transactions(tx: pd.DataFrame) -> pd.DataFrame:
    """One row per application from its card transactions: the organizers' baseline aggregates.

    Two codes of the source become missing values before aggregating: `amnt` 0.0 ("0.0 corresponds to missing
    values", the organizers' feature table) and `hour_diff` -1 (the first transaction of the window, which has no
    previous one). Counts include transactions without an amount; a mean over no known amount stays missing.
    """
    tx = tx.sort_values(["app_id", "transaction_number"], kind="stable")
    tx = tx.assign(
        amnt=tx["amnt"].where(tx["amnt"] != 0.0),
        hour_diff=tx["hour_diff"].where(tx["hour_diff"] != -1).astype("float64"),
    )
    by_app = tx.groupby("app_id", sort=True)
    blocks = []
    for column, n_codes in PIVOT_COLUMNS.items():
        codes = list(range(1, n_codes + 1))
        by_value = tx.groupby(["app_id", column], sort=True)
        count = by_value.size().unstack(fill_value=0).reindex(columns=codes, fill_value=0)
        mean = by_value["amnt"].mean().unstack().reindex(columns=codes)
        count.columns = [f"count_{column}_{code}" for code in codes]
        mean.columns = [f"mean_{column}_{code}" for code in codes]
        blocks += [count, mean]
    numeric = by_app.agg(NUMERIC_AGGREGATIONS)
    numeric.columns = [f"{column}_{how}" for column, how in numeric.columns]
    # The latest transaction (highest transaction_number) dates the issue: its week code and days before the issue.
    latest = by_app[["weekofyear", "days_before"]].last()
    latest.columns = ["latest_week_code", "latest_days_before"]
    return pd.concat([*blocks, numeric, latest], axis=1)


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
        - Tabular framing: the source is an event sequence per product. Top teams reached 0.776 private ROC AUC with boosting on aggregates alone and 0.781 with an RNN blended in, so we build the aggregates of the organizers' boosting baseline: `extract_basic_aggregations` with `cat_columns=["mcc_category", "day_of_week", "operation_type"]`, the statistics of `amnt`, `hour_diff` and `days_before`, plus `product`.
        - The other transaction fields are not aggregated, as in the baseline. Counts and mean amounts per value of all of them except `weekofyear` raise one untuned LightGBM from 0.720 to 0.733 ROC AUC; we keep the baseline's set.
        - Two codes of the source become missing values before aggregating: `amnt` 0.0, which "corresponds to missing values", and `hour_diff` -1, which marks the first transaction of the window. Counts include every transaction, and a mean amount over no known amount stays missing (the baseline filled 0.0). So `mean_operation_type_20` is missing for every product and is dropped.
        - Time: the data has no dates, but the applications are numbered so that later applications have a later date. The week code of each product's latest transaction splits `app_id` into 24 runs, one per issue month (`rolling_months`). `calendar_months` moves 292 products at the month edges to the neighbouring month whose calendar fits their latest transaction, and `issue_calendar` finds one issue date per calendar month (first decision). The 5 products `app_id` 0-4 fit month 11's calendar but come first in the published order, so they stay in month 0. We keep the month as `issue_month` (0-23), the time column, and drop `app_id` and the latest-transaction fields, which only date the issue.
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
        features = pd.concat([aggregate_transactions(pd.read_parquet(p, columns=AGGREGATE_COLUMNS)) for p in paths])
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
        # (`days_before_min` keeps the days since the latest transaction). The mean amount of operation type 20 is
        # missing for every product: all its amounts are the missing code 0.0. `client_key` stays for `_make_splits`,
        # which removes it.
        return drop_columns(df, ["app_id", "latest_week_code", "latest_days_before", "mean_operation_type_20"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["product"])

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
