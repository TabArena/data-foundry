"""Statistics of a temporal task's test windows, for the curator's choice of windows (SPLIT-15).

Which windows a temporal task tests on is a curation decision: always the newest window, the deployment period, and
others argued from the use case (other years, seasons, holidays, regime changes). This module gives the evidence,
without any model. For each window it reports:

* when: the dates, the months it covers and, for a window shorter than a week, its weekdays;
* how much: the test rows, the train rows and the train side's share of all rows (SPLIT-14's floor);
* the target: the class shares (the event's share and count of a binary target) or the mean and quantiles, on the
  test window and on its train side;
* the drift: the population stability index of each feature between the window and its train side, its maximum and
  median, the features that drift most, and the largest share of test rows with a category the train side never
  shows.

:func:`candidate_windows` lists the windows of a declared length walking back from the newest data, each train side
keeping at least ``min_train_fraction`` of the rows; :func:`window_stats` describes any windows. A definition gets
both through :meth:`~data_foundry.v2.dataset.AbstractCuratedDataset.window_stats`, and ``data-foundry dataset windows
<name>`` prints the table. The chosen windows are declared with ``TemporalSplits(cutoffs=...)``.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass

import numpy as np
import pandas as pd

from data_foundry.v2.splits import SPLIT_RANDOM_STATE, TemporalSplits, window_bounds

PSI_BINS = 10
"""A numeric feature's population stability index compares the train side's deciles."""

PSI_EPSILON = 1e-4
"""The share an empty bin counts as, so the index stays finite."""

TOP_DRIFT = 3
"""How many of the most drifting features a row names."""

MAX_LEVELS = 50
"""A categorical feature's levels beyond the train side's most frequent ones are pooled into one bin."""


@dataclass(frozen=True)
class Window:
    """One test window of a temporal task as row positions of the frame, which is sorted by time.

    Attributes:
        train: The train side's positions (every row before the window, minus the gap).
        test: The test window's positions.
        chosen: Whether the definition tests on this window.
    """

    train: Sequence[int]
    test: Sequence[int]
    chosen: bool = False


def candidate_windows(
    df: pd.DataFrame, time_on: str, windows: TemporalSplits, *, min_train_fraction: float = 0.5
) -> list[Window]:
    """The windows of ``windows``' length, gap and step, walking back from the newest data, newest first.

    Every train side keeps at least ``min_train_fraction`` of the rows (SPLIT-14). ``windows.cutoffs`` and
    ``windows.n_windows`` are ignored: these are the candidates, not the choice. Each side is a range of positions, so
    a frame of tens of millions of rows needs no index lists.
    """
    bounds = window_bounds(
        df,
        time_on=time_on,
        window=windows.window,
        unit=windows.unit,
        step=windows.step,
        gap=windows.gap,
        gap_unit=windows.gap_unit,
        min_train_fraction=min_train_fraction,
    )
    return [Window(train=range(b.train_stop), test=range(b.test_start, b.test_stop)) for b in bounds]


def window_stats(
    df: pd.DataFrame,
    windows: Iterable[Window],
    *,
    time_on: str,
    target: str,
    problem_type: str,
    features: list[str],
    time_unit: str | None = None,
    n_rows: int = 100_000,
    random_state: int = SPLIT_RANDOM_STATE,
) -> pd.DataFrame:
    """One row per window: when, how much, the target, and how far the features drift from the train side.

    The target and the population stability index read up to ``n_rows`` rows of each side, drawn at random with
    ``random_state``; the counts read every row, and so do the unseen categories (a category is unseen when no row of
    the whole train side holds it, however rare). Left out of the drift: ``time_on``, dates (a date is always newer in
    the test window) and free text (a ``string`` column: no two texts are alike, so it has no levels to compare).
    """
    rng = np.random.default_rng(random_state)
    times = df[time_on]
    used = [c for c in features if c != time_on and not _is_date(df[c]) and not _is_text(df[c])]
    levels = {c: _first_rows(df[c]) for c in used if _has_levels(df[c])}
    rows = []
    for i, window in enumerate(windows):
        test, train = window.test, window.train
        test_sample, train_sample = _sample(test, n_rows, rng), _sample(train, n_rows, rng)
        start, end = times.iloc[int(min(test))], times.iloc[int(max(test))]
        row = {
            "window": i,
            "chosen": window.chosen,
            "test_start": start,
            "test_end": end,
            "period": _period(start, end, time_unit),
            "weekdays": _weekdays(times.iloc[test_sample]) if _short(times, start, end) else "",
            "n_test": len(test),
            "n_train": len(train),
            "train_share": round(len(train) / len(df), 3),
            "target_test": _target(df[target].iloc[test_sample], problem_type, n_total=len(test)),
            "target_train": _target(df[target].iloc[train_sample], problem_type, n_total=len(train)),
        }
        row.update(_drift(df, used, train_sample, test_sample))
        row["unseen_categories"] = _unseen(levels, train, test_sample)
        rows.append(row)
    return pd.DataFrame(rows)


def _short(times: pd.Series, start: object, end: object) -> bool:
    """Whether a window on a date column spans less than a week, so its weekdays matter."""
    return pd.api.types.is_datetime64_any_dtype(times) and end - start < pd.Timedelta(days=7)


def _sample(positions: Sequence[int], n_rows: int, rng: np.random.Generator) -> np.ndarray:
    """Up to ``n_rows`` of ``positions`` at random, sorted; a range is sampled without listing it."""
    picked = (
        np.arange(len(positions)) if len(positions) <= n_rows else rng.choice(len(positions), n_rows, replace=False)
    )
    if isinstance(positions, range):
        return np.sort(positions.start + picked * positions.step)
    return np.sort(np.asarray(positions)[picked])


def _is_date(values: pd.Series) -> bool:
    return pd.api.types.is_datetime64_any_dtype(values) or isinstance(values.dtype, pd.PeriodDtype)


def _period(start: object, end: object, time_unit: str | None) -> str:
    """The months a window covers ("Nov 2023 - Jan 2024"), or its first and last time value."""
    if isinstance(start, pd.Timestamp):
        first, last = start.strftime("%b %Y"), end.strftime("%b %Y")
        return first if first == last else f"{first} - {last}"
    unit = f" ({time_unit})" if time_unit else ""
    return f"{start} - {end}{unit}"


WEEKDAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")


def _weekdays(times: pd.Series) -> str:
    """The weekdays a short window covers, in calendar order ("Sat, Sun"); empty when it covers all seven."""
    days = sorted(set(times.dt.dayofweek))
    return "" if len(days) == len(WEEKDAYS) else ", ".join(WEEKDAYS[d] for d in days)


def _target(values: pd.Series, problem_type: str, *, n_total: int) -> str:
    """The class shares (a binary target: the event's share and its count over the side), or mean and quantiles."""
    if problem_type == "regression":
        v = pd.to_numeric(values, errors="coerce").dropna()
        if v.empty:
            return ""
        q10, q50, q90 = np.quantile(v, [0.1, 0.5, 0.9])
        return f"mean {v.mean():.4g}, median {q50:.4g}, p10 {q10:.4g}, p90 {q90:.4g}"
    shares = values.value_counts(normalize=True, dropna=True)
    classes = sorted(shares.index, key=str)
    if problem_type == "binary_classification" and len(classes) <= 2:
        event = classes[-1]
        share = float(shares.get(event, 0.0))
        return f"{event} {share:.1%} (about {round(share * n_total):,})"
    return ", ".join(f"{c} {shares.get(c, 0.0):.1%}" for c in classes)


def _drift(df: pd.DataFrame, features: list[str], train: np.ndarray, test: np.ndarray) -> dict[str, object]:
    """The population stability index of every feature, and the features that drift most."""
    psi = {column: _psi(df[column].iloc[train], df[column].iloc[test]) for column in features}
    if not psi:
        return {"psi_max": np.nan, "psi_median": np.nan, "top_drift": ""}
    ranked = sorted(psi.items(), key=lambda item: -item[1])
    return {
        "psi_max": round(ranked[0][1], 3),
        "psi_median": round(float(np.median(list(psi.values()))), 3),
        "top_drift": ", ".join(f"{c} ({v:.2f})" for c, v in ranked[:TOP_DRIFT]),
    }


def _is_text(values: pd.Series) -> bool:
    return isinstance(values.dtype, pd.StringDtype)


def _has_levels(values: pd.Series) -> bool:
    """A categorical, boolean or object column: its values are levels a test row may not have seen."""
    return isinstance(values.dtype, pd.CategoricalDtype) or values.dtype == object or pd.api.types.is_bool_dtype(values)


def _first_rows(values: pd.Series) -> tuple[np.ndarray, np.ndarray]:
    """Each row's level code (-1 when missing) and, per code, the first row that holds it."""
    if isinstance(values.dtype, pd.CategoricalDtype):
        codes = values.cat.codes.to_numpy().astype(np.int64)
        n_levels = len(values.cat.categories)
    else:
        codes, uniques = pd.factorize(values)
        n_levels = len(uniques)
    first = np.full(n_levels, len(values), dtype=np.int64)
    present = codes >= 0
    found, at = np.unique(codes[present], return_index=True)
    first[found] = np.flatnonzero(present)[at]
    return codes, first


def _unseen(levels: dict[str, tuple[np.ndarray, np.ndarray]], train: Sequence[int], test: np.ndarray) -> float:
    """The largest share of test rows, over the columns with levels, whose level no row of the train side holds.

    A temporal train side is the rows before its window (a range from 0): a level is unseen when its first row comes
    after the side's end. Any other train side is read whole.
    """
    if not levels or not len(test):
        return np.nan
    prefix = isinstance(train, range) and train.start == 0 and train.step == 1
    largest = 0.0
    for codes, first in levels.values():
        at = codes[test]
        if prefix:
            new = (at >= 0) & (first[np.maximum(at, 0)] >= train.stop)
        else:
            new = (at >= 0) & ~np.isin(at, np.unique(codes[np.asarray(train)]))
        largest = max(largest, float(new.mean()))
    return round(largest, 4)


def _level_bins(values: pd.Series, levels: pd.Index) -> np.ndarray:
    """Each value's bin: its level's position, ``len(levels)`` for any other level, one more for a missing value."""
    codes = pd.Categorical(values, categories=levels).codes.astype(np.int64)
    codes[codes < 0] = len(levels)
    codes[values.isna().to_numpy()] = len(levels) + 1
    return codes


def _psi(train: pd.Series, test: pd.Series) -> float:
    """The population stability index of ``test`` against ``train``; missing values are a bin of their own."""
    numeric = pd.api.types.is_numeric_dtype(train) and not pd.api.types.is_bool_dtype(train)
    if numeric and not isinstance(train.dtype, pd.CategoricalDtype):
        a, b = train.to_numpy(dtype=float), test.to_numpy(dtype=float)
        edges = np.unique(np.nanquantile(a, np.linspace(0, 1, PSI_BINS + 1)[1:-1])) if np.isfinite(a).any() else []
        bins_a = np.where(np.isnan(a), len(edges) + 1, np.searchsorted(edges, a, side="right"))
        bins_b = np.where(np.isnan(b), len(edges) + 1, np.searchsorted(edges, b, side="right"))
        n_bins = len(edges) + 2
    else:
        a, b = train.astype("object"), test.astype("object")
        levels = a.dropna().value_counts().index[:MAX_LEVELS]
        bins_a, bins_b = _level_bins(a, levels), _level_bins(b, levels)
        n_bins = len(levels) + 2
    p = np.bincount(bins_a, minlength=n_bins) / max(len(bins_a), 1)
    q = np.bincount(bins_b, minlength=n_bins) / max(len(bins_b), 1)
    p, q = np.maximum(p, PSI_EPSILON), np.maximum(q, PSI_EPSILON)
    return float(np.sum((q - p) * np.log(q / p)))
