"""Time recovery: does a table whose split is not temporal still carry a time order (SPLIT-32, question 3)?

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

Flags, each a question for the curator, never a verdict: ``time_column``, ``time_dropped``, ``order_drift``,
``id_drift``, ``period_values``, and ``sorted_by_target`` for an order that follows the target in blocks (few label
changes between neighbouring rows, or a near-smooth number), which is how a file was put together, not a clock. Names
that say a duration or an age (``duration_months``, ``age_in_days``) are not time columns.
"""

from __future__ import annotations

import re

import numpy as np
import pandas as pd
from scipy import stats

from . import leak

TIME_WORDS = re.compile(
    r"(^|[_\W])(date|datetime|timestamp|dt|year|yr|month|week|quarter|qtr|season|period|wave|round|cohort|era|"
    r"fiscal)([_\W]|$)",
    re.IGNORECASE,
)
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


def _is_time_like(name: str, series: pd.Series) -> str | None:
    """Why a column looks like time, or None."""
    if pd.api.types.is_datetime64_any_dtype(series) or isinstance(series.dtype, pd.PeriodDtype):
        return "date dtype"
    if TIME_WORDS.search(str(name)) and not DURATION_WORDS.search(str(name)):
        return "name"
    values = pd.to_numeric(series, errors="coerce").dropna()
    if len(values) and pd.api.types.is_numeric_dtype(series) and (values % 1 == 0).all():
        low, high = values.min(), values.max()
        if YEAR_RANGE[0] <= low and high <= YEAR_RANGE[1] and values.nunique() >= 2:
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


def check_frame(
    df: pd.DataFrame,
    target: str,
    problem_type: str,
    *,
    exclude: tuple[str, ...] = (),
    raw: pd.DataFrame | None = None,
    raw_rows: np.ndarray | None = None,
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
    """
    skip = {target, *exclude}
    result: dict = {"problem_type": problem_type, "rows": len(df)}
    result["time_columns"] = time_columns(df, skip)
    if raw is not None:
        dropped = raw.drop(columns=[c for c in raw.columns if c in df.columns or c == target])
        result["dropped_time_columns"] = time_columns(dropped, set())
    if raw_rows is not None:
        y = df[target].iloc[np.argsort(raw_rows, kind="stable")]
        result["order_source"] = "raw"
    else:
        y = df[target]
        result["order_source"] = "frame"
    result["order"] = _drift(y, problem_type)
    result["id_orders"] = id_orders(df, target, problem_type, skip, raw=raw, raw_rows=raw_rows)
    result["period_values"] = period_values(df, target, problem_type, skip)
    flags = []
    if result["time_columns"]:
        flags.append("time_column")
    if result.get("dropped_time_columns"):
        flags.append("time_dropped")
    drift = [result["order"], *result["id_orders"].values()]
    if result["order"]["flag"] and result["order"]["p"] < DRIFT_P and not result["order"]["sorted_by_target"]:
        flags.append("order_drift")
    if any(o["flag"] and o["p"] < DRIFT_P and not o["sorted_by_target"] for o in result["id_orders"].values()):
        flags.append("id_drift")
    if any(o["flag"] and o["sorted_by_target"] for o in drift):
        flags.append("sorted_by_target")
    if result["period_values"].get("p", 1.0) < DRIFT_P:
        flags.append("period_values")
    result["flags"] = flags
    return result
