"""Periods: the target by period (probe 13, the test for right-censoring at the release end), and the period column
of probe 23 and the stationary-relation test (``period_columns``, ``outcome_periods``).
"""

from __future__ import annotations

import re

import numpy as np
import pandas as pd

from data_foundry.probes.leak.core import say

PERIOD_FREQS = ("D", "W", "M", "Q", "Y")
"""The calendar periods ``target_by_period`` picks from, finest first."""


YEARS = (1000, 3000)
"""Integer times in this range are read as years."""


PERIOD_NAMES = {
    "D": "daily",
    "W": "weekly",
    "M": "monthly",
    "Q": "quarterly",
    "Y": "yearly",
    "year": "yearly",
    "binned": "equal-count",
}


RANK_BINS = 40
"""Equal-count periods for an integer time column with about one row per value (a rank), at most."""


YEAR_LAG = {"D": 365, "W": 52, "M": 12, "Q": 4}
"""Periods back to the same period a year earlier."""


def period_times(times, *, tz: str | None = None) -> tuple[pd.Series, str]:
    """The time column as naive wall-clock timestamps (kind ``datetime``), years (``year``; also dates that all fall
    on 1 January, a year stored as a date) or other integer periods (``integer``, such as a month index). Aware
    timestamps are converted to ``tz`` first (None keeps their own offset); naive ones are read as already in ``tz``.
    Numbers, numeric categories and numeric strings are never read as nanoseconds since 1970. Raises ``ValueError``
    for booleans, fractional numbers and strings that are no dates.
    """
    s = pd.Series(times).reset_index(drop=True)
    if isinstance(s.dtype, pd.CategoricalDtype):
        s = s.astype(s.cat.categories.dtype)
    if pd.api.types.is_bool_dtype(s):
        raise ValueError("the time column is boolean, not a time")
    if s.dtype == object:
        numbers = pd.to_numeric(s, errors="coerce")
        if numbers.notna().sum() == s.notna().sum() and not s.dropna().map(lambda v: isinstance(v, bool)).any():
            s = numbers
    if pd.api.types.is_numeric_dtype(s):
        known = s.dropna().astype(float)
        if (known != known.round()).any():
            raise ValueError("the time column holds fractional numbers: give dates, years or integer periods")
        kind = "year" if len(known) and YEARS[0] <= known.min() and known.max() <= YEARS[1] else "integer"
        return s.astype("Int64"), kind
    s = _naive_dates(s, tz)
    if _years_as_dates(s):
        return s.dt.year.astype("Int64"), "year"
    return s, "datetime"


def _naive_dates(s: pd.Series, tz: str | None) -> pd.Series:
    """``s`` parsed as dates and made naive in ``tz`` (see ``period_times``)."""
    if not pd.api.types.is_datetime64_any_dtype(s):
        try:
            s = pd.to_datetime(s.astype(object), errors="raise", format="mixed")
        except (ValueError, TypeError) as err:
            raise ValueError(f"the time column is neither dates, years nor integer periods: {err}") from err
    if s.dt.tz is not None:
        s = (s.dt.tz_convert(tz) if tz else s).dt.tz_localize(None)
    return s


def _years_as_dates(s: pd.Series) -> bool:
    """Whether every date is midnight on 1 January: a year stored as a date (a fiscal year)."""
    known = s.dropna()
    return bool(len(known)) and bool(
        ((known.dt.month == 1) & (known.dt.day == 1) & (known == known.dt.normalize())).all()
    )


def choose_period(stamps: pd.Series, *, min_rows: int = 100, max_periods: int = 60) -> str:
    """The finest calendar period (``PERIOD_FREQS``) with 5 to ``max_periods`` periods and a median of at least
    ``min_rows`` rows per period that has rows; when none has that many rows, the coarsest with at least 5 periods.
    """
    fallback = None
    for freq in PERIOD_FREQS:
        per = stamps.dt.to_period(freq)
        span = (per.max() - per.min()).n + 1
        if span < 5:
            break
        fallback = freq
        if span <= max_periods and per.value_counts().median() >= min_rows:
            return freq
    if fallback is None:
        raise ValueError("the times span fewer than 5 days: probe 13 needs at least 5 periods")
    return fallback


def _period_positions(t: pd.Series, kind: str, freq: str | None, *, min_rows: int, max_periods: int):
    """Each row's period position, the period labels, the size of each period that the data covers (days for
    calendar periods, 1 otherwise), the share of each period covered, the period, and whether rows are counted per
    day (calendar periods of dates with day resolution) or per period.

    An integer column with about one row per value that is no year (a rank such as an arrival order, or a running
    id) is cut into equal-count periods by its order, at most ``RANK_BINS``, period ``binned``. Dates that label
    their period (one distinct date in every period, such as month starts) are counted per period, not per day.
    """
    if kind != "datetime":
        values = t.astype("int64").to_numpy()
        if kind == "integer" and len(values) >= 10 and len(np.unique(values)) >= 0.5 * len(values):
            bins = int(np.clip(len(values) // max(min_rows, 1), 5, min(RANK_BINS, max_periods)))
            order = np.argsort(values, kind="stable")
            pos = np.empty(len(values), dtype=np.int64)
            pos[order] = np.arange(len(values)) * bins // len(values)
            edges = [(values[order][pos[order] == b].min(), values[order][pos[order] == b].max()) for b in range(bins)]
            ones = np.ones(bins)
            return pos, [f"{lo}-{hi}" for lo, hi in edges], ones, ones, "binned", False
        steps = np.arange(values.min(), values.max() + 1) if kind == "year" else np.unique(values)
        ones = np.ones(len(steps))
        return np.searchsorted(steps, values), [str(v) for v in steps], ones, ones, kind, False
    if freq is not None and freq not in PERIOD_FREQS:
        raise ValueError(f"period {freq!r}: use one of {PERIOD_FREQS}")
    freq = freq or choose_period(t, min_rows=min_rows, max_periods=max_periods)
    per = t.dt.to_period(freq)
    index = pd.period_range(per.min(), per.max(), freq=freq)
    positions = index.get_indexer(pd.PeriodIndex(per))
    if pd.Series(t.to_numpy()).groupby(positions).nunique().max() <= 1:  # each period holds one date: its label
        ones = np.ones(len(index))
        return positions, [str(p) for p in index], ones, ones, freq, False
    day = pd.Timedelta(days=1)
    starts, ends = index.start_time, index.end_time + pd.Timedelta(1, "ns")
    length = np.asarray((ends - starts) / day, dtype=float)
    days = length.copy()
    first, last = t.min().normalize(), t.max().normalize() + day
    for i in {0, len(index) - 1}:
        days[i] = (min(ends[i], last) - max(starts[i], first)) / day
    return positions, [str(p) for p in index], days, days / length, freq, True


def _plain(value):
    """A JSON value: numpy scalars as Python ones, NaN as None."""
    value = value.item() if hasattr(value, "item") else value
    return None if isinstance(value, float) and np.isnan(value) else value


def _prefix(per_period: np.ndarray) -> np.ndarray:
    """Cumulative sums with a leading 0: the sum over periods ``a`` to ``b - 1`` is ``out[b] - out[a]``."""
    return np.concatenate([[0.0], np.cumsum(per_period)])


class _Periods:
    """The rows put in periods: positions, labels, rows and covered size, and the earlier periods that give the band."""

    def __init__(self, pos: np.ndarray, labels: list[str], size: np.ndarray, tail: int) -> None:
        self.pos, self.labels, self.tail = pos, labels, tail
        self.count = len(labels)
        self.base = self.count - tail
        self.in_base = pos < self.base
        self.rows = np.bincount(pos, minlength=self.count).astype(float)
        self.rows_c, self.size_c = _prefix(self.rows), _prefix(size)

    def total(self, a: int, b: int) -> float:
        """Rows in periods ``a`` to ``b - 1``."""
        return self.rows_c[b] - self.rows_c[a]

    def sums(self, weights: np.ndarray) -> np.ndarray:
        """``_prefix`` of the per-period sums of ``weights``."""
        return _prefix(np.bincount(self.pos, weights=weights.astype(float), minlength=self.count))


def _statistic(value, *, noise=None, show=None, log: bool = False) -> dict:
    """A statistic of a run of periods ``(a, b)``: its value (the tested one), the sampling variance of that value
    under no change (or None), the value shown (when another than the tested one) and whether it is tested on a log
    scale.
    """
    return {"value": value, "noise": noise, "show": show or value, "log": log}


def _rate(periods: _Periods, hits: np.ndarray) -> dict:
    """The share of rows with ``hits`` in a run of periods, with binomial noise at the earlier periods' share."""
    hit_c = periods.sums(hits)
    p0 = float(hits[periods.in_base].mean()) if periods.in_base.any() else float("nan")

    def value(a, b):
        return (hit_c[b] - hit_c[a]) / periods.total(a, b) if periods.total(a, b) else float("nan")

    return _statistic(value, noise=lambda a, b: p0 * (1 - p0) / periods.total(a, b))


def _rows_name(*, per_day: bool) -> str:
    """The name of the row-count statistic: per day for calendar periods of dates (months differ in length), else
    per period.
    """
    return "rows per day" if per_day else "rows per period"


def _period_statistics(
    periods: _Periods, y: pd.Series, problem_type: str, positive, rows_name: str
) -> tuple[dict, dict]:
    """The statistics probe 13 tests (see ``target_by_period``) and what the result says about the classes."""
    p = periods

    def rows_per_unit(a, b):
        return p.total(a, b) / (p.size_c[b] - p.size_c[a]) if p.total(a, b) else float("nan")

    stats = {rows_name: _statistic(rows_per_unit, noise=lambda a, b: 1.0 / p.total(a, b), log=True)}
    if problem_type == "regression":
        v = pd.to_numeric(y, errors="raise").to_numpy(dtype=float)
        sum_c, var0 = p.sums(v), float(np.var(v[p.in_base]))
        stats["mean"] = _statistic(
            lambda a, b: (sum_c[b] - sum_c[a]) / p.total(a, b) if p.total(a, b) else float("nan"),
            noise=lambda a, b: var0 / p.total(a, b),
        )
        if bool((v >= 0).all() and (v == np.round(v)).all()):  # a count
            stats["zero share"] = _rate(p, v == 0)
            return stats, {}
        groups = np.split(v[np.argsort(p.pos, kind="stable")], np.cumsum(p.rows.astype(int))[:-1])
        for q, name in ((0.5, "p50"), (0.9, "p90")):
            # tested as the share above the earlier periods' quantile, which discrete values do not break
            stat = _rate(p, v > float(np.quantile(v[p.in_base], q)))

            def show(a, b, q=q):
                return float(np.quantile(np.concatenate(groups[a:b]), q)) if p.total(a, b) else float("nan")

            stats[name] = {**stat, "show": show}
        return stats, {}
    counts = y.value_counts()
    counts = counts[counts > 0]
    values = y.to_numpy()
    if problem_type != "binary_classification" and len(counts) > 2:
        top = list(counts.index[:10])
        stats.update({f"share of {c}": _rate(p, values == c) for c in top})
        return stats, {"classes": [_plain(c) for c in top]}
    if positive is None:
        if len(counts) < 2:
            raise ValueError("the target holds one class only; name the event class with `positive`")
        positive = counts.index[-1]  # the minority class
    else:
        match = [c for c in counts.index if c == positive or str(c) == str(positive)]
        if not match:
            values_seen = [_plain(c) for c in counts.index]
            raise ValueError(
                f"the positive label {positive!r} does not occur in the target (its values: {values_seen})"
            )
        positive = match[0]
    stats[f"rate of {positive}"] = _rate(p, values == positive)
    return stats, {"positive": _plain(positive)}


def _band(p: _Periods, stat: dict, k: int) -> tuple[float, float, float] | None:
    """The median, the spread (1.4826 x MAD) and the median sampling noise of ``stat`` over every run of ``k``
    consecutive earlier periods (on the statistic's scale); None with fewer than 3 runs.
    """
    vals, noises = [], []
    for a in range(p.base - k + 1):
        value = stat["value"](a, a + k)
        if np.isfinite(value) and (value > 0 or not stat["log"]):
            vals.append(np.log(value) if stat["log"] else value)
            noises.append(stat["noise"](a, a + k) if stat["noise"] else 0.0)
    if len(vals) < 3:
        return None
    vals = np.asarray(vals)
    mid = float(np.median(vals))
    return mid, 1.4826 * float(np.median(np.abs(vals - mid))), float(np.median(noises))


def _z(stat: dict, a: int, b: int, band: tuple | None) -> float | None:
    """How far the run of periods ``(a, b)`` lies from ``band``, in its spread widened by the run's extra noise."""
    value = stat["value"](a, b)
    if band is None or not np.isfinite(value) or (stat["log"] and value <= 0):
        return None
    mid, spread, base_noise = band
    noise = stat["noise"](a, b) if stat["noise"] else 0.0
    var = max(spread**2 + max(noise - base_noise, 0.0), base_noise, 1e-12 * max(abs(mid), 1.0) ** 2)
    return float(((np.log(value) if stat["log"] else value) - mid) / np.sqrt(var))


def _newest(p: _Periods, stat: dict, freq: str, threshold: float) -> dict:
    """``stat`` on each newest period and on the newest 1 to ``tail`` pooled, and the run out of band at the end."""
    bands = {k: _band(p, stat, k) for k in range(1, p.tail + 1)}
    lag = YEAR_LAG.get(freq)
    newest = []
    for i in range(p.base, p.count):
        entry = {"period": p.labels[i], "value": _plain(stat["show"](i, i + 1)), "z": _z(stat, i, i + 1, bands[1])}
        if lag and i - lag >= 0:
            entry["year_earlier"] = _plain(stat["show"](i - lag, i - lag + 1))
        newest.append(entry)
    windows = [
        {
            "periods": k,
            "value": _plain(stat["show"](p.count - k, p.count)),
            "z": _z(stat, p.count - k, p.count, bands[k]),
        }
        for k in range(1, p.tail + 1)
    ]
    last = newest[-1]["z"]
    run_length = 0
    if last is not None and abs(last) >= threshold:
        for entry in reversed(newest):
            if entry["z"] is None or abs(entry["z"]) < threshold or np.sign(entry["z"]) != np.sign(last):
                break
            run_length += 1
    return {
        "newest_periods": newest,
        "newest_windows": windows,
        "trailing_out_of_band": run_length,
        "direction": ("falls" if last < 0 else "rises") if run_length else None,
    }


def _period_reading(out: dict, labels: list[str], period_name: str, threshold: float) -> str:
    """What the curator acts on, in two sentences."""
    flags = [s for s, o in out.items() if o["trailing_out_of_band"]]
    if flags:
        first_out = len(labels) - max(out[s]["trailing_out_of_band"] for s in flags)
        moves = ", ".join(f"{s} {out[s]['direction']}" for s in flags)
        return (
            f"The newest {period_name} periods from {labels[first_out]} on are outside the band of the earlier ones "
            f"({moves}). A fall of an event rate, an upper quantile or the row count at the end only is the mark of "
            "right-censoring: cut before that period (or set a gap of that length), or compare a second download "
            "(LEAK-24); a rise, or a shift the history also shows, is drift."
        )
    pooled = [
        (s, w) for s, o in out.items() for w in o["newest_windows"] if w["z"] is not None and abs(w["z"]) >= threshold
    ]
    if pooled:
        s, w = pooled[0]
        return (
            f"No single newest period is outside the band, but the newest {w['periods']} pooled are ({s}, z "
            f"{w['z']:+.1f}): a mild shift at the end; compare a second download or a finer period."
        )
    return (
        f"No newest period is outside the band of the earlier ones (|z| < {threshold:g}) for any statistic: no sign of "
        "censoring at the release end. It does not show which labels a model refit at a window's start would have "
        "known (SPLIT-10)."
    )


def target_by_period(  # noqa: PLR0913
    times,
    y,
    problem_type: str,
    *,
    freq: str | None = None,
    tz: str | None = None,
    positive=None,
    tail: int | None = None,
    threshold: float = 3.0,
    min_rows: int = 100,
    max_periods: int = 60,
    report: bool = True,
) -> dict:
    """Probe 13: does the target by period show the newest periods losing their late cases?

    A label that is known only some time after the prediction point (a default on the first instalment, a claim
    reported late, a duration still running at the download) is right-censored at the release end: in the newest
    periods the slow or late cases are missing, so an event rate, the upper quantiles of a duration or the row count
    falls there and nowhere else. Credit risk reads this from vintage (cohort) curves of default rates by origination
    month, insurance from the development of claims by accident period (incurred but not reported, IBNR), survival
    analysis as administrative censoring at the end of follow-up. With one release, the probe looks at the end of the
    series: every statistic of the newest periods against the band the earlier periods give.

    The times are put in periods: calendar periods (``freq`` one of ``PERIOD_FREQS``; by default the finest with 5 to
    ``max_periods`` periods and ``min_rows`` rows per period), years (dates that all fall on 1 January are years), or
    other integer periods; an integer column with about one row per value (a rank) is cut into at most ``RANK_BINS``
    equal-count periods by its order, and the output says so. The newest ``tail``
    periods (default a fifth of them, 2 to 8) are tested; the band comes from the earlier ones: for a run of ``k``
    periods, the median and the spread (1.4826 x MAD) of every run of ``k`` consecutive earlier periods, widened by
    the extra sampling noise of a smaller run. So a drop is read against the normal variation of the history, not
    against one chosen period. Statistics: the rows per day the data covers (per period for years and integer
    periods; on a log scale); for a binary target the rate of ``positive`` (default the minority class); for a
    multiclass target the share of each of the ten largest classes; for a regression the mean, and the shares above
    the earlier periods' median and 90th percentile (shown as the run's p50 and p90); for a count target the mean and
    the zero share. A statistic whose newest periods are out of band (``|z| >= threshold``), in a run from the end,
    is flagged with its direction, and the reading says what the curator acts on (LEAK-24: cut where follow-up is
    complete, or compare a second download). The same period a year earlier is shown for seasonal data. A clean
    result says nothing about which labels a model refit at a window's start would have known (SPLIT-10).

    Args:
        times: The time of each row: datetimes, date strings, years or integer periods.
        y: The target.
        problem_type: ``"regression"``, or a classification type.
        freq: The calendar period, or None to choose one (not used for years and integer periods).
        tz: The timezone whose calendar makes the periods; aware times are converted to it.
        positive: The event class of a binary target (matched by value or by its string).
        tail: The newest periods tested; the others give the band (at least 4 of them).
        threshold: The ``|z|`` from which a newest period is out of band.
        min_rows: Rows per period the automatic period choice asks for.
        max_periods: The most periods the automatic choice makes.
        report: Print the summary lines.
    """
    t, kind = period_times(times, tz=tz)
    y = pd.Series(y).reset_index(drop=True)
    if len(t) != len(y):
        raise ValueError(f"{len(t)} times for {len(y)} targets")
    missing_time, missing_target = int(t.isna().sum()), int((y.isna() & t.notna()).sum())
    keep = (t.notna() & y.notna()).to_numpy()
    t, y = t[keep].reset_index(drop=True), y[keep].reset_index(drop=True)
    if not len(t):
        raise ValueError("no row has both a time and a target")
    pos, labels, size, coverage, freq, per_day = _period_positions(
        t, kind, freq, min_rows=min_rows, max_periods=max_periods
    )
    if len(labels) < 5:
        raise ValueError(f"{len(labels)} periods: probe 13 needs at least 5 (4 for the band, 1 to test)")
    tail = min(int(np.clip(len(labels) // 5, 2, 8)) if tail is None else int(tail), len(labels) - 4)
    if tail < 1:
        raise ValueError(f"tail {tail}: test at least 1 period and keep 4 for the band")
    periods = _Periods(pos, labels, size, tail)
    rows_name = _rows_name(per_day=per_day)
    stats, extra = _period_statistics(periods, y, problem_type, positive, rows_name)
    if freq == "binned":  # equal-count periods: their row count says nothing
        stats.pop(rows_name)
    out = {name: _newest(periods, stat, freq, threshold) for name, stat in stats.items()}
    table = []
    for i in range(periods.count):
        row = {"period": labels[i], "rows": int(periods.rows[i])}
        if coverage[i] < 1:
            row["coverage"] = round(float(coverage[i]), 3)
        row.update({s: _plain(stat["show"](i, i + 1)) for s, stat in stats.items() if s != rows_name})
        table.append(row)
    result = {
        "time_kind": kind,
        "period": freq,
        "tz": tz,
        "rows": len(t),
        "missing_time": missing_time,
        "missing_target": missing_target,
        "periods": periods.count,
        "first": labels[0],
        "last": labels[-1],
        "coverage_first": round(float(coverage[0]), 3),
        "coverage_last": round(float(coverage[-1]), 3),
        "tail": tail,
        "threshold": threshold,
        "note": (
            f"an integer time column with about one row per value (a rank or an id): cut into {len(labels)} "
            "equal-count periods by its order"
            if freq == "binned"
            else ""
        ),
        **extra,
        "table": table,
        "statistics": out,
        "flags": [s for s, o in out.items() if o["trailing_out_of_band"]],
        "reading": _period_reading(out, labels, PERIOD_NAMES.get(freq, freq), threshold),
    }
    if report:
        for line in period_lines(result):
            say(line)
    return result


def _cell(entry: dict) -> str:
    """One newest period or run: its value and its z."""
    if entry["value"] is None:
        return "-"
    z = "z n/a" if entry["z"] is None else f"z {entry['z']:+.1f}"
    return f"{entry['value']:.4g} ({z})"


def period_lines(result: dict) -> list[str]:
    """``target_by_period``'s result as the lines of the report."""
    left_out = result["missing_time"] + result["missing_target"]
    head = (
        f"target by period (probe 13): {result['periods']} {PERIOD_NAMES.get(result['period'], result['period'])} "
        f"periods {result['first']} to {result['last']}; the newest {result['tail']} against the band of the "
        f"{result['periods'] - result['tail']} before (|z| >= {result['threshold']:g})"
    )
    if result["coverage_last"] < 1:
        head += f"; the last period {result['coverage_last']:.0%} covered"
    if left_out:
        head += f"; {left_out:,} rows without a time or a target left out"
    if result.get("note"):
        head += f"; {result['note']}"
    lines = [head]
    for name, stat in result["statistics"].items():
        cells = ", ".join(_cell(e) for e in stat["newest_periods"])
        pooled = ", ".join("n/a" if w["z"] is None else f"{w['z']:+.1f}" for w in stat["newest_windows"])
        run_out = stat["trailing_out_of_band"]
        flag = f"; the newest {run_out} out of band, {stat['direction']}" if run_out else ""
        lines.append(
            f"  {name}: newest periods {cells}; newest 1 to {len(stat['newest_windows'])} pooled, z {pooled}{flag}"
        )
    lines.append(f"  reading: {result['reading']}")
    return lines


OUTCOME_PERIODS = 12
"""The most periods the period-outcome test fits; more are merged into this many runs of consecutive periods."""


PERIOD_WORDS = ("year", "quarter", "month", "week", "season", "period", "era")
"""A column of whole numbers or labels named by one of these words (in at most three words) can be the period."""


def _words(name: str) -> list[str]:
    """The words of a column name, lower case: ``Calendar_Year`` and ``CalendarYear`` give ``["calendar", "year"]``,
    ``AMT_REQ_CREDIT_BUREAU_YEAR`` five words.
    """
    return [w.lower() for w in re.findall(r"[A-Z]+(?![a-z])|[A-Z]?[a-z]+|\d+", str(name))]


def period_columns(df: pd.DataFrame, exclude: list[str] | tuple[str, ...] = ()) -> list[tuple[str, str]]:
    """The columns that can give each row's period, best first, with the reason: dates; whole numbers that are years
    (2 to 60 distinct, fewest first: a calendar year before a vehicle's model year); whole numbers or labels named by a
    ``PERIOD_WORDS`` word (``year``, ``policy_year``, ``month``; not ``AMT_REQ_CREDIT_BUREAU_YEAR``). ``exclude``: the
    target, the weight.
    """
    names = [c for c in df.columns if c not in set(exclude)]
    dates = [(c, "dates") for c in names if pd.api.types.is_datetime64_any_dtype(df[c])]
    years = []
    for c in names:
        s = df[c]
        if pd.api.types.is_integer_dtype(s) and not pd.api.types.is_bool_dtype(s):
            known = s.dropna()
            if len(known) and YEARS[0] <= known.min() and known.max() <= YEARS[1] and 2 <= known.nunique() <= 60:
                years.append((known.nunique(), c))
    found = dates + [(c, "years") for _, c in sorted(years, key=lambda kv: kv[0])]
    for c in names:
        s, words = df[c], _words(c)
        labels = isinstance(s.dtype, pd.CategoricalDtype) or s.dtype == object or pd.api.types.is_string_dtype(s)
        whole = pd.api.types.is_integer_dtype(s) and not pd.api.types.is_bool_dtype(s)
        named = len(words) <= 3 and any(w in PERIOD_WORDS for w in words)
        if named and (labels or whole) and s.nunique() >= 2 and all(c != f for f, _ in found):
            found.append((c, f"named `{c}`"))
    return found


def outcome_periods(
    values, *, freq: str | None = None, tz: str | None = None, max_periods: int = OUTCOME_PERIODS
) -> tuple[np.ndarray, list[str], str]:
    """Each row's period for the period-outcome test: its code (0 to k - 1, in time order), the labels and the kind.

    Dates are cut into calendar periods (``freq``; by default the coarsest of years, quarters, months, weeks and days
    with at least 3 periods), years and other whole numbers are their own periods, a category of words (a month's
    name) is periods in the category's order, and any other labels (an era) are periods in their sorted order. More
    than ``max_periods`` periods are merged into that many runs of consecutive periods of about equal rows, labelled by
    their first and last. A missing time is a period of its own. Raises ``ValueError`` for one period only.
    """
    s = pd.Series(values).reset_index(drop=True)
    named = isinstance(s.dtype, pd.CategoricalDtype) and not pd.api.types.is_numeric_dtype(s.cat.categories)
    try:
        if named:  # a category of words (``jan``, ``feb``): in its own order, never parsed as dates
            raise ValueError("labels")
        t, kind = period_times(s, tz=tz)
    except ValueError:
        t, kind = s.astype(object), "labels"
    rank = list(s.cat.categories) if named else None
    if kind == "datetime":
        if freq is not None and freq not in PERIOD_FREQS:
            raise ValueError(f"period {freq!r}: use one of {PERIOD_FREQS}")
        coarse = [f for f in reversed(PERIOD_FREQS) if t.dt.to_period(f).nunique() >= 3]
        freq = freq or (coarse[0] if coarse else PERIOD_FREQS[0])
        keys, kind = t.dt.to_period(freq), PERIOD_NAMES[freq]
    else:
        keys, kind = t, {"year": "yearly", "integer": "whole numbers"}.get(kind, kind)
    known = keys.notna().to_numpy()
    present = set(pd.unique(keys[known]))
    order = [v for v in rank if v in present] if rank is not None else sorted(present)  # a category's own order
    if len(order) + (not known.all()) < 2:
        raise ValueError("the time column holds one period: the test needs two or more")
    codes = np.full(len(s), len(order), dtype=np.int64)  # a missing time: the last period
    codes[known] = pd.Index(order).get_indexer(keys[known])
    labels = [str(v) for v in order] + ([] if known.all() else ["missing"])
    if len(labels) > max_periods:
        rows = np.bincount(codes, minlength=len(labels))
        middle = (np.cumsum(rows) - rows / 2) / rows.sum()
        run = np.minimum((middle * max_periods).astype(np.int64), max_periods - 1)
        run = pd.factorize(run)[0]  # runs without rows dropped, the order kept
        labels = [
            f"{labels[np.flatnonzero(run == r)[0]]} to {labels[np.flatnonzero(run == r)[-1]]}"
            if (run == r).sum() > 1
            else labels[np.flatnonzero(run == r)[0]]
            for r in range(run.max() + 1)
        ]
        codes, kind = run[codes], f"{kind}, merged into {run.max() + 1} runs"
    return codes, labels, kind
