"""Descriptive release-boundary label rates, not proof of individual label availability.

Dates are UTC calendar days and intervals are half-open. The caller chooses the positive
label, historical reference, windows, buffers and optional rate-ratio criterion before
interpreting the grid. No model is fitted and no rows or split memberships are changed.
"""

from __future__ import annotations

import math
from numbers import Integral

import pandas as pd

DEFAULT_WINDOWS = (1, 3, 7, 14, 21, 28, None)
DEFAULT_BUFFERS = (0, 3, 7, 14, 21, 28, 31)


def _day(value) -> pd.Timestamp:
    stamp = pd.Timestamp(value)
    if pd.isna(stamp):
        raise ValueError("Dates must not be missing.")
    stamp = stamp.tz_localize("UTC") if stamp.tzinfo is None else stamp.tz_convert("UTC")
    return stamp.normalize()


def _ratio(numerator, denominator):
    return numerator / denominator if numerator is not None and denominator not in (None, 0) else None


def _days(values, *, allow_all: bool):
    result = list(values)
    if not result or len(set(result)) != len(result):
        raise ValueError("Specify a nonempty sequence without duplicate windows or buffers.")
    for value in result:
        if value is None and allow_all:
            continue
        if isinstance(value, bool) or not isinstance(value, Integral) or value < int(allow_all):
            raise ValueError("Windows must be positive day counts or None; buffers nonnegative day counts.")
    return result


def _observations(dates, labels, positive_label):
    dates = pd.Series(pd.to_datetime(list(dates), utc=True, errors="raise")).dt.normalize()
    labels = pd.Series(list(labels))
    if len(dates) != len(labels) or dates.empty or dates.isna().any() or labels.isna().any():
        raise ValueError("Dates and labels must be nonempty, aligned and have no missing values.")
    if labels.nunique() > 2:
        raise ValueError("This diagnostic requires a binary event label.")
    if not pd.api.types.is_scalar(positive_label) or pd.isna(positive_label):
        raise ValueError("The positive label must be a nonmissing scalar.")
    if labels.nunique() == 2 and positive_label not in labels.unique():
        raise ValueError("The positive label must be one of the observed binary labels.")
    return dates, labels


def run(
    dates,
    labels,
    *,
    reference_start,
    reference_end,
    positive_label=1,
    windows=DEFAULT_WINDOWS,
    buffers=DEFAULT_BUFFERS,
    end=None,
    min_rate_ratio=None,
) -> dict:
    """Return the full window/buffer grid and reference rates for a binary event label.

    ``None`` as a window uses all retained history before the buffered end. Empty
    windows and a zero-event reference have undefined ratios, represented by None.
    A criterion is optional and dataset-specific; it never produces a maturity verdict.
    """
    dates, labels = _observations(dates, labels, positive_label)
    windows, buffers = _days(windows, allow_all=True), _days(buffers, allow_all=False)
    if min_rate_ratio is not None and (not math.isfinite(min_rate_ratio) or min_rate_ratio <= 0):
        raise ValueError("min_rate_ratio must be finite and positive, or None.")
    start, stop = _day(reference_start), _day(reference_end)
    end = _day(end) if end is not None else dates.max() + pd.Timedelta(days=1)
    if start >= stop or stop > end or end <= dates.min() or end > dates.max() + pd.Timedelta(days=1):
        raise ValueError("Use an ordered reference within the release end and an end within observed support.")
    data = pd.DataFrame({"date": dates, "event": labels.eq(positive_label).astype(int)})

    def aggregate(lower, upper):
        selected = data.loc[data.date.lt(upper) & (data.date.ge(lower) if lower is not None else True)]
        count = len(selected)
        return {
            "start": lower.date().isoformat() if lower is not None else None,
            "end_exclusive": upper.date().isoformat(),
            "first_observed": selected.date.min().date().isoformat() if count else None,
            "last_observed": selected.date.max().date().isoformat() if count else None,
            "rows": count,
            "events": int(selected.event.sum()),
            "rate": float(selected.event.mean()) if count else None,
        }

    reference = aggregate(start, stop)
    if not reference["rows"]:
        raise ValueError("The historical reference contains no observations.")
    daily = data.groupby("date").event.agg(["size", "sum"])
    reference_periods = []
    left = start
    while left < stop:
        right = min(left + pd.offsets.MonthBegin(1), stop)
        reference_periods.append(aggregate(left, right))
        left = right
    grid = []
    for buffer in buffers:
        cutoff = end - pd.Timedelta(days=int(buffer))
        for width in windows:
            lower = cutoff - pd.Timedelta(days=int(width)) if width is not None else None
            recent = aggregate(lower, cutoff)
            previous = aggregate(lower - pd.Timedelta(days=int(width)), lower) if width is not None else None
            earlier = aggregate(None, lower) if width is not None else None
            ratio = _ratio(recent["rate"], reference["rate"])
            grid.append(
                {
                    "window_days": int(width) if width is not None else None,
                    "end_buffer_days": int(buffer),
                    "recent": recent,
                    "reference_overlap": bool(cutoff > start and (lower is None or lower < stop)),
                    "rate_ratio": ratio,
                    "meets_rate_criterion": ratio >= min_rate_ratio if ratio is not None and min_rate_ratio else None,
                    "previous_equal_window": previous,
                    "ratio_to_previous": _ratio(recent["rate"], previous["rate"]) if previous else None,
                    "all_earlier": earlier,
                    "ratio_to_all_earlier": _ratio(recent["rate"], earlier["rate"]) if earlier else None,
                }
            )
    return {
        "rows": len(data),
        "end_exclusive": end.date().isoformat(),
        "reference": reference,
        "reference_months": reference_periods,
        "min_rate_ratio": min_rate_ratio,
        "daily": [
            {"date": day.date().isoformat(), "rows": int(row["size"]), "events": int(row["sum"])}
            for day, row in daily.iterrows()
        ],
        "grid": grid,
        "interpretation": "Rate ratios only. Check reference stability and changing case mix. Passing does not "
        "prove complete follow-up or label availability at historical training cutoffs. Overlapping "
        "windows are dependent; a threshold is a case-specific screen, not a universal rule.",
    }
