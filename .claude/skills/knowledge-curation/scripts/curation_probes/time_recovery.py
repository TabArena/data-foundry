"""Time recovery: does a table whose split is not temporal still carry a time order (SPLIT-32, question 4)?

A release can lose its dates and keep its time: a date column the definition dropped, a row order that follows entry
time, an ID handed out in sequence, a few columns whose values change only from one period to the next (yearly
unemployment, inflation and GDP figures). Each check here is model-free and returns plain numbers:

* ``time_columns``: columns typed as dates, named like a time (date, time, year, month, day, week, quarter, season,
  period, wave, round, cohort, era) or holding whole numbers between 1900 and 2100 only.
* ``dropped_time_columns``: the same test on the raw columns that do not reach the frame.
* ``order``: the target along the rows' order (the raw order when the rows can be traced, else the frame's), by
  ``leak.row_order``.
* ``id_orders``: the target along each ID-like column (whole numbers, nearly one value per row, named like an ID or
  following the row order), as if the ID were the order: an ID handed out in sequence is a clock. IDs the definition
  dropped are read from the raw table through the rows' raw positions.
* ``period_values``: numeric columns with few distinct values that are not whole numbers (rates, indices, prices of a
  period), taken together as one key; with three or more levels, the target across the levels.
* ``periodic_blocks``: rows that repeat one block length later, as a panel of company-years stored year block by year
  block (``taiwanese_bankruptcy_prediction``), and the target one block later.
* ``entity_runs``: one entity's rows in consecutive rows, as a patient's admissions (``sepsis_survival_...``): a
  counter that goes up by 1 while fixed fields repeat, and where the target sits in the runs (deaths on the last row).
* ``class_block_drift``: in a file sorted by class, the features shift along a class's rows: the class block is
  several pieces, sources or periods (``naticusdroid_android_permissions_dataset``), unless a feature sorts it.

The checks of the row order (the order, the three above) read the raw order, else the frame's; ``order_known=False``
(a built container, whose rows were shuffled) leaves them out.

Flags, each a question for the curator, never a verdict: ``time_column``, ``time_dropped``, ``order_drift``,
``id_drift``, ``period_values``, ``periodic_blocks``, ``entity_runs``, ``class_block_drift``, and
``sorted_by_target`` for an order that follows the target in blocks (few label changes between neighbouring rows, or a
near-smooth number), which is how a file was put together, not a clock; ``class_block_drift`` says when its blocks
are themselves several pieces. Names that say a duration or an age (``duration_months``, ``age_in_days``) are not
time columns, nor are fractional numbers outside 1900-2100 (a ratio named ``three_year_...``) or numbers named with
``dt`` (``edge_dt``, a delta t).
"""

from __future__ import annotations

import re

import numpy as np
import pandas as pd
from scipy import stats

from . import leak

TIME_WORDS = re.compile(
    r"(^|[_\W])(date|datetime|timestamp|year|yr|month|week|quarter|qtr|season|period|wave|round|cohort|era|"
    r"fiscal)([_\W]|$)",
    re.IGNORECASE,
)
TEXT_TIME_WORDS = re.compile(r"(^|[_\W])dt([_\W]|$)", re.IGNORECASE)  # a date or a delta t: counts on text only
DURATION_WORDS = re.compile(
    r"(^|[_\W])(age|duration|length|since|elapsed|until|refill|tenure|lag|span|interval|survival|follow|next|last|"
    r"previous|prev|ago|count|number|num|per|in)s?([_\W]|$)",
    re.IGNORECASE,
)
YEAR_RANGE = (1900, 2100)
ID_UNIQUE_SHARE = 0.9
ID_WORDS = re.compile(r"(^|[_\W])(id|no|nr|num|number|key|index|idx|record|case|seq|serial|row)([_\W]|$)", re.I)
ID_ORDER_CORRELATION = 0.9
PERIOD_MAX_LEVELS = 40
PERIOD_MIN_LEVELS = 3
PERIOD_MIN_ROWS = 50
SORTED_CHANGE_RATIO = 0.5
SORTED_AUTOCORRELATION = 0.5
DRIFT_P = 1e-3

PERIOD_LAGS = (5, 250)  # the lags scanned; taiwanese_bankruptcy_prediction's blocks run 26 to about 200 rows
PERIOD_WINDOW = 500  # rows per window: the block length may change along the file
PERIOD_MAX_WINDOWS = 40
PERIOD_MAX_FEATURES = 100
PERIOD_CLOSE = 0.01  # a pair of rows is close below the 1st percentile of random-pair distances
PERIOD_Z = 6.0  # a window's lag stands out this many standard errors above the lags around it
PERIOD_RATIO = 2.0  # and with at least twice their close share
PERIOD_MIN_SHARE = 1 / 3  # the share of windows with a lag that stands out, for the flag
PERIOD_TOLERANCE = 3  # rows around one block later, for the target: a company may be missing from a year

RUN_COUNTER_MAX = 100  # a counter counts from 0 or 1 to at least 2 and at most this
RUN_SHARE = 0.8  # the share of rows above the counter's start whose row before holds the counter minus one
RUN_EXCESS = 0.3  # above the share a shuffled order gives
RUN_FIXED_RATIO = 0.5  # a fixed field changes within a run at most this share of how often it changes between runs
RUN_MIN_RUNS = 20  # runs of two rows or more

CLASS_DRIFT_MIN_ROWS = 100  # rows of a class, for the drift within its block
CLASS_DRIFT_P = 1e-6  # a feature drifts: its tenths of the class's rows differ at this p value (Kruskal-Wallis)
CLASS_DRIFT_SHARE = 0.2  # the share of drifting features, for the flag
CLASS_SORT_KEY = 0.01  # a feature of 10 values or more that steps down (or up) at most this often sorts the block
CLASS_SORT_LEVELS = (2, 10, 0.1)  # a feature of 2 to 10 values, each on a tenth of the rows, can sort it too (sex)


def _is_time_like(name: str, series: pd.Series) -> str | None:
    """Why a column looks like time, or None.

    A name counts unless the values are fractional numbers outside 1900-2100 (a ratio named ``three_year_...``);
    ``dt`` (a date, or a delta t such as ``edge_dt``) counts on text only.
    """
    if pd.api.types.is_datetime64_any_dtype(series) or isinstance(series.dtype, pd.PeriodDtype):
        return "date dtype"
    numeric = pd.api.types.is_numeric_dtype(series) and not pd.api.types.is_bool_dtype(series)
    values = pd.to_numeric(series, errors="coerce").dropna() if numeric else pd.Series(dtype=float)
    in_years = bool(len(values)) and bool(values.between(*YEAR_RANGE).all())
    fraction = bool(len(values)) and bool((values % 1 != 0).any())
    named = TIME_WORDS.search(str(name)) or (TEXT_TIME_WORDS.search(str(name)) and not numeric)
    if named and not DURATION_WORDS.search(str(name)) and not (fraction and not in_years):
        return "name"
    if in_years and not fraction and values.nunique() >= 2:
        return "whole numbers within 1900-2100"
    return None


def time_columns(df: pd.DataFrame, exclude: set[str]) -> dict[str, str]:
    """The columns of ``df`` that look like time, with the reason."""
    out = {}
    for column in df.columns:
        if column in exclude:
            continue
        reason = _is_time_like(column, df[column])
        if reason:
            out[str(column)] = reason
    return out


def _drift(y: pd.Series, problem_type: str) -> dict:
    """The target across the levels of an order (already sorted): ``leak.row_order`` plus a test p value."""
    out = leak.row_order(y, problem_type)
    n = len(y)
    tenth = np.minimum(np.arange(n) * 10 // max(n, 1), 9)
    out["p"] = _level_test(pd.Series(tenth), y.reset_index(drop=True), problem_type)
    out["sorted_by_target"] = _sorted_by_target(y.reset_index(drop=True), problem_type, out)
    return out


def _sorted_by_target(y: pd.Series, problem_type: str, order: dict) -> bool:
    """Rows sorted or blocked by the target, not drifting in time: few label changes between neighbours (a class
    target), or a near-smooth sequence (a number).
    """
    if problem_type == "regression":
        return bool(order.get("lag1_autocorrelation", 0) >= SORTED_AUTOCORRELATION)
    values = y.astype(str).where(y.notna()).to_numpy()
    both = pd.notna(values[1:]) & pd.notna(values[:-1])
    if not both.any():
        return False
    changes = float((values[1:][both] != values[:-1][both]).mean())
    expected = 1 - order.get("chance", 1.0)
    return bool(expected > 0 and changes / expected < SORTED_CHANGE_RATIO)


def _level_test(levels: pd.Series, y: pd.Series, problem_type: str) -> float:
    """The p value of the target differing across ``levels``: chi-squared for classes, Kruskal-Wallis for a number."""
    keep = y.notna().to_numpy() & levels.notna().to_numpy()
    levels, y = levels[keep], y[keep]
    if levels.nunique() < 2:
        return float("nan")
    if problem_type == "regression":
        groups = [pd.to_numeric(y[levels == level], errors="coerce").dropna() for level in levels.unique()]
        groups = [g for g in groups if len(g) > 1]
        return float(stats.kruskal(*groups).pvalue) if len(groups) > 1 else float("nan")
    table = pd.crosstab(levels, y.astype(str))
    if table.shape[1] < 2:
        return float("nan")
    return float(stats.chi2_contingency(table.to_numpy())[1])


def _is_id_like(name: str, values: pd.Series) -> bool:
    """Whole numbers, nearly one per row, named like an ID or following the row order."""
    if not pd.api.types.is_numeric_dtype(values) or values.isna().mean() > 0.1:
        return False
    present = values.dropna()
    if present.empty or not (present % 1 == 0).all() or present.nunique() < ID_UNIQUE_SHARE * len(values):
        return False
    if ID_WORDS.search(str(name)):
        return True
    position = pd.Series(np.arange(len(values)), index=values.index, dtype=float)
    return bool(abs(position.corr(values.astype(float), method="spearman")) >= ID_ORDER_CORRELATION)


def id_orders(
    df: pd.DataFrame,
    target: str,
    problem_type: str,
    exclude: set[str],
    *,
    raw: pd.DataFrame | None = None,
    raw_rows: np.ndarray | None = None,
) -> dict[str, dict]:
    """The target along each ID-like column, of the frame and, traced through ``raw_rows``, of the raw columns the
    frame does not keep (an ID the definition dropped).
    """
    candidates = {str(c): df[c] for c in df.columns if c not in exclude and c != target and _is_id_like(c, df[c])}
    if raw is not None and raw_rows is not None:
        for column in raw.columns:
            if column in df.columns or column == target or not _is_id_like(column, raw[column]):
                continue
            candidates[f"{column} (dropped)"] = pd.Series(raw[column].to_numpy()[raw_rows], index=df.index)
    out = {}
    for name, values in candidates.items():
        order = np.argsort(values.to_numpy(), kind="stable")
        out[name] = _drift(df[target].iloc[order], problem_type)
    return out


def period_values(df: pd.DataFrame, target: str, problem_type: str, exclude: set[str]) -> dict:
    """Few-valued numeric columns that are not whole numbers, as one key, and the target across its levels."""
    columns = []
    for column in df.columns:
        if column in exclude or column == target or not pd.api.types.is_numeric_dtype(df[column]):
            continue
        values = df[column].dropna()
        if values.empty or (values % 1 == 0).all():
            continue
        if PERIOD_MIN_LEVELS <= values.nunique() <= PERIOD_MAX_LEVELS:
            columns.append(column)
    if not columns:
        return {"columns": []}
    key = df[columns].astype(str).agg("|".join, axis=1)
    levels = int(key.nunique())
    widest = max(df[c].nunique() for c in columns)
    out = {"columns": [str(c) for c in columns], "levels": levels}
    together = levels <= 1.5 * widest  # the columns move together, as figures of one period do
    if PERIOD_MIN_LEVELS <= levels <= PERIOD_MAX_LEVELS and together and len(df) / levels >= PERIOD_MIN_ROWS:
        out["p"] = _level_test(key.reset_index(drop=True), df[target].reset_index(drop=True), problem_type)
    return out


def _as_numbers(features: pd.DataFrame) -> pd.DataFrame:
    """The columns of ``features`` that hold numbers: numeric ones, and categories or text whose values all parse."""
    out = {}
    for column in features.columns:
        series = features[column]
        if pd.api.types.is_bool_dtype(series) or pd.api.types.is_numeric_dtype(series):
            out[column] = series.astype(float)
        elif not pd.api.types.is_datetime64_any_dtype(series):
            parsed = pd.to_numeric(series.astype(object), errors="coerce")
            if parsed.notna().sum() == series.notna().sum() > 0:
                out[column] = parsed.astype(float)
    return pd.DataFrame(out, index=features.index)


def _distance(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.sqrt(((a - b) ** 2).sum(axis=1))


def periodic_blocks(features: pd.DataFrame, y: pd.Series, problem_type: str) -> dict:
    """Rows that repeat one block length later, as company-years of a panel stored year block by year block.

    In windows of ``PERIOD_WINDOW`` rows, row i is compared with row i + L for each lag L in ``PERIOD_LAGS``, on the
    ranks of the numeric features with more than two values; a pair is close below the 1st percentile of the
    distances of random pairs. A window's lag stands out when its close share is ``PERIOD_Z`` standard errors above,
    and ``PERIOD_RATIO`` times, the lags around it (lags near 1 are close in any file sorted by something; only a
    rise again after them is a period). The target: of the rarest class's rows, the share with a row of their class
    within ``PERIOD_TOLERANCE`` rows of one block later, against half and one and a half blocks later (for a number,
    the Spearman correlation of the target one block apart, against the same).

    Args:
        features: The features in the order read (the raw order when the rows can be traced).
        y: The target in the same order.
        problem_type: ``regression`` or a classification type.
    """
    numbers = _as_numbers(features)
    numbers = numbers.loc[:, numbers.nunique() > 2]
    n = len(numbers)
    high = min(PERIOD_LAGS[1], (n - 1) // 4)
    if numbers.shape[1] == 0 or high < 2 * PERIOD_LAGS[0]:
        return {"run": False, "note": "no numeric feature with more than two values" if n > 40 else "too few rows"}
    rng = np.random.default_rng(0)
    if numbers.shape[1] > PERIOD_MAX_FEATURES:
        keep = np.sort(rng.choice(numbers.shape[1], PERIOD_MAX_FEATURES, replace=False))
        numbers = numbers.iloc[:, keep]
    ranks = numbers.rank(pct=True).fillna(0.5).to_numpy(dtype=np.float32)
    pairs = rng.integers(0, n, (20_000, 2))
    pairs = pairs[pairs[:, 0] != pairs[:, 1]]
    threshold = float(np.quantile(_distance(ranks[pairs[:, 0]], ranks[pairs[:, 1]]), PERIOD_CLOSE))
    last = n - high  # the anchors that have every lag after them
    starts = np.arange(0, last, PERIOD_WINDOW)
    if len(starts) > PERIOD_MAX_WINDOWS:
        starts = starts[np.linspace(0, len(starts) - 1, PERIOD_MAX_WINDOWS).round().astype(int)]
    windows = [np.arange(s, min(s + PERIOD_WINDOW, last)) for s in starts]
    windows = [w for w in windows if len(w) >= min(100, last)]
    anchors = np.concatenate(windows)
    close = np.zeros((len(anchors), high + 1), dtype=bool)
    for lag in range(1, high + 1):
        close[:, lag] = _distance(ranks[anchors], ranks[anchors + lag]) <= threshold
    found, offset = [], 0
    for window in windows:
        share = close[offset : offset + len(window)].mean(axis=0)
        offset += len(window)
        best = _standout_lag(share, len(window), high)
        if best is not None:
            found.append((window, *best))
    out: dict = {"run": True, "windows": len(windows), "standout_windows": len(found)}
    if not found:
        return out | {"flag": False}
    lags = [lag for _, lag, _, _ in found]
    out.update(
        lags=lags,
        lag=int(np.median(lags)),
        close_at_lag=float(np.mean([s for _, _, s, _ in found])),
        close_around=float(np.mean([b for _, _, _, b in found])),
    )
    out["flag"] = bool(len(found) >= max(2, PERIOD_MIN_SHARE * len(windows)))
    out["target"] = _target_one_block_later(y.to_numpy(), found, problem_type)
    return out


def _standout_lag(share: np.ndarray, rows: int, high: int) -> tuple[int, float, float] | None:
    """The lag whose close share stands out from the lags around it, with that share and theirs, or None.

    Every multiple of a block length stands out too: the smallest lag at least half as close as the best is the block.
    """
    standing = []
    for lag in range(PERIOD_LAGS[0], high + 1):
        half = max(lag // 2, 3)
        left, right = share[max(1, lag - half) : lag - 2], share[lag + 3 : lag + half + 3]
        if len(left) == 0 or len(right) == 0:
            continue
        around = max(float(np.median(left)), float(np.median(right)))
        se = np.sqrt(max(around, 1 / rows) * (1 - around) / rows)
        if (share[lag] - around) / se >= PERIOD_Z and share[lag] >= PERIOD_RATIO * around:
            standing.append((lag, float(share[lag]), around))
    if not standing:
        return None
    closest = max(s for _, s, _ in standing)
    return next(item for item in standing if item[1] >= closest / 2)


def _target_one_block_later(y: np.ndarray, found: list[tuple], problem_type: str) -> dict:
    """The target one block later against half and one and a half blocks later, over the windows with a period."""
    n, t = len(y), PERIOD_TOLERANCE

    def rows_at(window: np.ndarray, lag: int) -> tuple[np.ndarray, np.ndarray]:
        keep = window + lag + t < n
        return window[keep], window[keep] + lag

    if problem_type == "regression":
        values = pd.to_numeric(pd.Series(y), errors="coerce").to_numpy()
        out = {}
        for name, factor in (("one_block", 1.0), ("half_block", 0.5), ("one_and_a_half_blocks", 1.5)):
            pairs = [rows_at(w, round(lag * factor)) for w, lag, _, _ in found]
            a = np.concatenate([p[0] for p in pairs])
            b = np.concatenate([p[1] for p in pairs])
            out[f"spearman_{name}"] = float(pd.Series(values[a]).corr(pd.Series(values[b]), method="spearman"))
        return out
    labels = pd.Series(y).astype(str).to_numpy()
    rare = pd.Series(labels).value_counts().idxmin()
    out = {"class": rare, "share": float((labels == rare).mean())}
    for name, factor in (("one_block", 1.0), ("half_block", 0.5), ("one_and_a_half_blocks", 1.5)):
        hits = []
        for window, lag, _, _ in found:
            start, _ = rows_at(window[labels[window] == rare], round(lag * factor))
            for i in start:
                hits.append(bool((labels[i + round(lag * factor) - t : i + round(lag * factor) + t + 1] == rare).any()))
        out[f"same_class_{name}"] = float(np.mean(hits)) if hits else float("nan")
    out["rows"] = int(sum((labels[w] == rare).sum() for w, *_ in found))
    return out


def entity_runs(features: pd.DataFrame, y: pd.Series, problem_type: str) -> dict:
    """Runs of consecutive rows of one entity: a counter that goes up by 1 from row to row while fixed fields repeat.

    A counter holds whole numbers from 0 or 1 up to at most ``RUN_COUNTER_MAX`` (an admission or visit number).
    The rows above its start should follow a row that holds the counter minus one: ``RUN_SHARE`` of them or more, and
    ``RUN_EXCESS`` above the share a shuffled order gives. A fixed field (age, sex) changes inside a run at most
    ``RUN_FIXED_RATIO`` times as often as between runs; a run goes on while the counter goes up by 1 and every fixed
    field holds (a number within the change most runs show). The target: the share of each class on a run's last row
    against the share of all rows (an outcome that ends the runs, such as death, sits on the last row); for a number,
    the mean on the last rows against the others, in standard deviations.

    Args:
        features: The features in the order read.
        y: The target in the same order.
        problem_type: ``regression`` or a classification type.
    """
    numbers = _as_numbers(features)
    best = None
    for column in numbers.columns:
        values = numbers[column]
        present = values.dropna()
        if values.isna().mean() > 0.1 or present.empty or (present % 1 != 0).any():
            continue
        low, top = present.min(), present.max()
        if low not in (0, 1) or not 2 <= top <= RUN_COUNTER_MAX:
            continue
        v = values.to_numpy()
        after = v[1:] > low
        if after.sum() < RUN_MIN_RUNS:
            continue
        follows = (v[1:] == v[:-1] + 1)[after]
        shares = present.value_counts(normalize=True)
        expected = float(pd.Series(v[1:][after] - 1).map(shares).fillna(0).mean())
        observed = float(follows.mean())
        if best is None or observed - expected > best[1] - best[2]:
            best = (column, observed, expected)
    if best is None:
        return {"counter": None, "flag": False}
    column, observed, expected = best
    v = numbers[column].to_numpy()
    counted = v[1:] == v[:-1] + 1
    fixed = _fixed_fields(features.drop(columns=[column]), counted)
    step = np.r_[False, counted & _fields_hold(features, fixed, counted)]  # row i continues the run of row i - 1
    run = np.cumsum(~step) - 1
    sizes = np.bincount(run)
    last = np.r_[~step[1:], True]
    out: dict = {
        "counter": str(column),
        "follow_share": observed,
        "follow_share_shuffled": expected,
        "runs": len(sizes),
        "runs_from_start": int((v[~step] == np.nanmin(v)).sum()),
        "runs_of_two_or_more": int((sizes >= 2).sum()),
        "longest_run": int(sizes.max()),
        "fixed_fields": fixed,
    }
    if problem_type == "regression":
        values = pd.to_numeric(y, errors="coerce").to_numpy()
        sd = float(np.nanstd(values))
        out["target_last_minus_other_sd"] = (
            float((np.nanmean(values[last]) - np.nanmean(values[~last])) / sd) if sd and (~last).any() else float("nan")
        )
    else:
        labels = y.astype(str).to_numpy()
        out["last_row_share"] = float(last.mean())
        out["class_on_last_row"] = {str(k): float(last[labels == k].mean()) for k in pd.unique(labels)}
    out["flag"] = bool(
        observed >= RUN_SHARE
        and observed - expected >= RUN_EXCESS
        and out["runs_of_two_or_more"] >= RUN_MIN_RUNS
        and out["fixed_fields"]
    )
    return out


def _fixed_fields(features: pd.DataFrame, inside: np.ndarray) -> dict[str, list[float]]:
    """The columns that change inside runs (``inside``: each step from row i to i + 1) at most ``RUN_FIXED_RATIO``
    times as often as between runs, with both change shares.
    """
    out = {}
    if not inside.any() or inside.all():
        return out
    for column in features.columns:
        codes = pd.factorize(features[column])[0]  # missing is -1: two missing values are the same
        same = codes[1:] == codes[:-1]
        changed_inside, changed_between = 1 - float(same[inside].mean()), 1 - float(same[~inside].mean())
        if changed_between > 0 and changed_inside <= RUN_FIXED_RATIO * changed_between:
            out[str(column)] = [round(changed_inside, 4), round(changed_between, 4)]
    return out


def _fields_hold(features: pd.DataFrame, fixed: dict, inside: np.ndarray) -> np.ndarray:
    """For each step from row i to i + 1: every fixed field the same, a number within the change most runs show
    (the 90th percentile inside runs: an age may go up by one between two admissions).
    """
    hold = np.ones(len(features) - 1, dtype=bool)
    for column in fixed:
        series = features[column]
        if pd.api.types.is_numeric_dtype(series) and not pd.api.types.is_bool_dtype(series):
            values = series.astype(float).to_numpy()
            change = np.abs(values[1:] - values[:-1])
            missing = np.isnan(change)
            known = inside & ~missing
            tolerance = float(np.quantile(change[known], 0.9)) if known.any() else 0.0
            hold &= missing | (change <= tolerance)
        else:
            codes = pd.factorize(series)[0]
            hold &= codes[1:] == codes[:-1]
    return hold


def class_block_drift(features: pd.DataFrame, y: pd.Series) -> dict:
    """In a file sorted by class, do the features shift along each class's rows (the block is several pieces)?

    For each class with ``CLASS_DRIFT_MIN_ROWS`` rows or more, its rows in the order read are cut into tenths; a
    numeric feature (up to ``PERIOD_MAX_FEATURES`` of them) drifts when the tenths differ at a Kruskal-Wallis p value
    below ``CLASS_DRIFT_P`` (a shuffled class block gives none). ``largest`` names the features whose tenth means
    sit farthest from the class's, in standard deviations of rank. A class block whose features drift is several
    pieces put one after the other: sources or periods, which a file sorted by class otherwise hides. ``sorted_by``
    names the features that sort the block: 10 values or more, a step down (or up) at most ``CLASS_SORT_KEY`` of the
    time (age), or 2 to 10 values (``CLASS_SORT_LEVELS``) that change between neighbouring rows less than
    ``SORTED_CHANGE_RATIO`` times as often as in a shuffled order (sex). Blood donors sorted by sex, then age, drift
    for that reason: the drift then follows from the sort, and the block may be one piece.

    Args:
        features: The features in the order read.
        y: The class of each row, in the same order.
    """
    numbers = _as_numbers(features)
    numbers = numbers.loc[:, numbers.nunique() >= 2]
    if numbers.shape[1] > PERIOD_MAX_FEATURES:
        keep = np.sort(np.random.default_rng(0).choice(numbers.shape[1], PERIOD_MAX_FEATURES, replace=False))
        numbers = numbers.iloc[:, keep]
    out: dict = {}
    labels = y.astype(str).where(y.notna()).to_numpy()
    for label, count in pd.Series(labels).value_counts().items():
        if count < CLASS_DRIFT_MIN_ROWS or numbers.shape[1] == 0:
            continue
        rows = numbers[labels == label]
        ranks = rows.rank(pct=True)
        sd = ranks.std()
        tenth = np.minimum(np.arange(len(rows)) * 10 // len(rows), 9)
        gap = ((ranks.groupby(tenth).mean() - ranks.mean()).abs().max() / sd)[sd > 0]
        drifting = {}
        for column in gap.index:
            values = rows[column].to_numpy()
            parts = [part for t in range(10) if len(part := values[(tenth == t) & ~np.isnan(values)])]
            with np.errstate(divide="ignore", invalid="ignore"):  # all values tied: no p value, no drift
                p = stats.kruskal(*parts).pvalue if len(parts) > 1 else np.nan
            if p < CLASS_DRIFT_P:
                drifting[str(column)] = round(float(gap[column]), 3)
        steps = np.diff(rows.to_numpy(), axis=0)
        known = np.maximum((~np.isnan(steps)).sum(axis=0), 1)
        rarer = np.minimum((steps < 0).sum(axis=0), (steps > 0).sum(axis=0)) / known
        keys = [*rows.columns[(rows.nunique().to_numpy() >= 10) & (rarer <= CLASS_SORT_KEY)]]
        keys += [c for c in features.columns if c not in keys and _sorts_by_level(features[c][labels == label])]
        out[str(label)] = {
            "rows": int(count),
            "features": len(gap),
            "drifting": len(drifting),
            "share": float(len(drifting) / len(gap)) if len(gap) else 0.0,
            "largest": dict(sorted(drifting.items(), key=lambda item: -item[1])[:5]),
            "sorted_by": [str(c) for c in keys],
        }
    return out


def _sorts_by_level(values: pd.Series) -> bool:
    """A column of a few values, each on a tenth of the rows or more, in long runs: rows sorted by it (sex)."""
    shares = values.value_counts(normalize=True)
    low, high, share = CLASS_SORT_LEVELS
    if not low <= len(shares) <= high or shares.min() < share:
        return False
    codes = pd.factorize(values)[0]
    both = (codes[1:] >= 0) & (codes[:-1] >= 0)
    changes = float((codes[1:] != codes[:-1])[both].mean()) if both.any() else 1.0
    return changes < SORTED_CHANGE_RATIO * (1 - float((shares**2).sum()))


def check_frame(
    df: pd.DataFrame,
    target: str,
    problem_type: str,
    *,
    exclude: tuple[str, ...] = (),
    raw: pd.DataFrame | None = None,
    raw_rows: np.ndarray | None = None,
    order_known: bool = True,
) -> dict:
    """Run the checks of the module docstring and set the flags.

    Args:
        df: The rows as the split sees them, with the target.
        target: The target column.
        problem_type: ``regression`` or a classification type.
        exclude: Columns to leave out (group or scoring columns).
        raw: The raw table in source order, when there is one; its columns that do not reach ``df`` are checked
            for time.
        raw_rows: The raw position of each row of ``df``, to read the order in the source's order.
        order_known: False when the row order of ``df`` is not the source's and ``raw_rows`` cannot restore it (a
            built container, whose rows were shuffled): the checks of the row order are then not run.
    """
    skip = {target, *exclude}
    result: dict = {"problem_type": problem_type, "rows": len(df)}
    result["time_columns"] = time_columns(df, skip)
    if raw is not None:
        dropped = raw.drop(columns=[c for c in raw.columns if c in df.columns or c == target])
        result["dropped_time_columns"] = time_columns(dropped, set())
    result["order_source"] = "raw" if raw_rows is not None else "frame" if order_known else "none"
    if result["order_source"] != "none":
        ordered = df.iloc[np.argsort(raw_rows, kind="stable")] if raw_rows is not None else df
        result |= _order_checks(
            ordered.drop(columns=[c for c in skip if c in ordered.columns]), ordered[target], problem_type
        )
    result["id_orders"] = id_orders(df, target, problem_type, skip, raw=raw, raw_rows=raw_rows)
    result["period_values"] = period_values(df, target, problem_type, skip)
    result["flags"] = _flags(result)
    return result


def _order_checks(features: pd.DataFrame, y: pd.Series, problem_type: str) -> dict:
    """The checks of the row order: the target along it, periodic blocks, entity runs and, in a file sorted by class,
    the drift within the class blocks.
    """
    out = {"order": _drift(y, problem_type)}
    out["periodic_blocks"] = periodic_blocks(features, y, problem_type)
    out["entity_runs"] = entity_runs(features, y, problem_type)
    if problem_type != "regression" and out["order"]["flag"] and out["order"]["sorted_by_target"]:
        out["class_block_drift"] = class_block_drift(features, y)
    return out


def _flags(result: dict) -> list[str]:
    """The flags of ``check_frame``'s result."""
    flags = []
    if result["time_columns"]:
        flags.append("time_column")
    if result.get("dropped_time_columns"):
        flags.append("time_dropped")
    order = result.get("order")
    if order and order["flag"] and order["p"] < DRIFT_P and not order["sorted_by_target"]:
        flags.append("order_drift")
    if any(o["flag"] and o["p"] < DRIFT_P and not o["sorted_by_target"] for o in result["id_orders"].values()):
        flags.append("id_drift")
    sorted_order = bool(order and order["flag"] and order["sorted_by_target"])
    if sorted_order or any(o["flag"] and o["sorted_by_target"] for o in result["id_orders"].values()):
        flags.append("sorted_by_target")
    if result["period_values"].get("p", 1.0) < DRIFT_P:
        flags.append("period_values")
    if result.get("periodic_blocks", {}).get("flag"):
        flags.append("periodic_blocks")
    if result.get("entity_runs", {}).get("flag"):
        flags.append("entity_runs")
    drift = result.get("class_block_drift", {})
    if sorted_order and any(c["share"] >= CLASS_DRIFT_SHARE and not c["sorted_by"] for c in drift.values()):
        flags.append("class_block_drift")
    return flags
