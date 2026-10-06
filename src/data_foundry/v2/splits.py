"""The v2 split protocol: how every v2 dataset is split, and the checks that hold it.

* IID and grouped data get repeated 3-fold cross-validation. The number of repeats follows the size of the train
  side (:func:`recommended_dimensions`): 20, 10, 3 or 1.
* A frame larger than :data:`FRAME_ROW_BUDGET` (1.5M rows) is sub-sampled to it first, in a ``<name>_1m`` version
  (``subsample_to_budget = True``), so each of the 3 folds trains on 1M rows and tests on 500k
  (:func:`subsample_frame`).
* Temporal data gets at least 3 expanding windows (:class:`TemporalSplits`). A ``_1m`` version samples per window
  instead of sampling the frame (:func:`sample_temporal_splits`): each test window keeps up to 500k of its rows, each
  train side is a random 1M of all earlier rows (one random order for all windows), and the frame keeps only the rows
  some split uses.
* No split trains on more than :data:`TRAIN_ROW_BUDGET` or tests on more than :data:`TEST_ROW_BUDGET` rows:
  :func:`cap_splits` trims a side that uneven folds or a long history push over.

This module does not use the v1 helpers in :mod:`data_foundry.curation_recommendations`, which keep the v1 protocol
(one 1M / 250k split from 1.25M rows on) for the v1 notebooks. The cross-validation builders give the same splits
as the v1 ones, so a dataset below 1.25M rows keeps its splits.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

import numpy as np
import pandas as pd

from data_foundry.bundle_checks import CheckResult
from data_foundry.schema import as_column_list
from data_foundry.v2._optional import import_build_dependency

if TYPE_CHECKING:
    from data_foundry.curation_container import CuratedContainer

Splits = dict[int, dict[int, tuple[list[int], list[int]]]]
"""Outer splits: ``{repeat: {fold: (train_positions, test_positions)}}``."""

SPLIT_RANDOM_STATE = 4267
"""The seed of every split and of the sub-sampling (the same seed as the v1 helpers)."""

N_FOLDS = 3
"""Every IID and grouped split is 3-fold cross-validation."""

TRAIN_ROW_BUDGET = 1_000_000
"""No split trains on more rows than this."""

TEST_ROW_BUDGET = 500_000
"""No split tests on more rows than this."""

FRAME_ROW_BUDGET = 1_500_000
"""A ``_1m`` version sub-samples its frame to this many rows: 3 folds of 1M train and 500k test rows."""

SINGLE_REPEAT_ROWS = 1_250_000
"""A frame with this many rows gets a single repeat even when it has few groups (``group_labels="per_group"``)."""

MIN_TEMPORAL_SPLITS = 3
"""A temporal task needs at least this many test windows."""

REPEATS_BY_TRAIN_SIZE = ((500, 20), (2_500, 10), (250_000, 3))
"""``(train-size limit, repeats)``: a train side below the limit gets that many repeats; larger ones get 1."""

TemporalUnit = Literal["days", "weeks", "months", "years", "unique", "rows"]
"""How :class:`TemporalSplits` measures a test window.

* ``"days"`` / ``"weeks"``: calendar days (windows end on day boundaries).
* ``"months"`` / ``"years"``: calendar months / years (windows end on month / year starts).
* ``"unique"``: distinct values of the time column (dates, years, or a numeric time index).
* ``"rows"``: rows in time order (for a time index that is only a row order).
"""

_CALENDAR_UNITS = ("days", "weeks", "months", "years")


# --- split dimensions -----------------------------------------------------------------------------------------


GROUP_KEY = "__group_key__"
"""The column :func:`one_group_column` adds for a group of several columns."""


def one_group_column(df: pd.DataFrame, group_on: str | list[str] | None) -> tuple[pd.DataFrame, str | None]:
    """``df`` and one column naming the groups: ``group_on`` itself, or for several columns a key numbering their
    combinations (:data:`GROUP_KEY`, in order of first appearance; a missing value is a value of its own).
    """
    columns = as_column_list(group_on)
    if len(columns) <= 1:
        return df, columns[0] if columns else None
    key = df.groupby(columns, sort=False, observed=True, dropna=False).ngroup().to_numpy()
    return df.assign(**{GROUP_KEY: key}), GROUP_KEY


def recommended_dimensions(
    df: pd.DataFrame, *, group_on: str | list[str] | None = None, group_labels: str | None = None
) -> tuple[int, int]:
    """``(n_repeats, n_folds)`` for IID or grouped cross-validation on ``df``.

    The size is the train side of a 3-fold split (2/3 of the rows, or of the groups for ``per_group`` labels):
    below 500 it gets 20 repeats, below 2,500 10, below 250k 3, and 1 above. A frame of
    :data:`SINGLE_REPEAT_ROWS` or more always gets one repeat.
    """
    n = len(df)
    if n >= SINGLE_REPEAT_ROWS:
        return 1, N_FOLDS
    if group_on is not None and group_labels == "per_group":
        df, group_on = one_group_column(df, group_on)
        n = df[group_on].nunique()
    n_train = int(n * 2 / 3)
    for limit, repeats in REPEATS_BY_TRAIN_SIZE:
        if n_train < limit:
            return repeats, N_FOLDS
    return 1, N_FOLDS


# --- cross-validation -----------------------------------------------------------------------------------------


def iid_splits(
    df: pd.DataFrame,
    *,
    n_repeats: int,
    n_folds: int = N_FOLDS,
    stratify_on: str | None = None,
    random_state: int = SPLIT_RANDOM_STATE,
) -> Splits:
    """Repeated (stratified) k-fold cross-validation over the rows of ``df``."""
    model_selection = import_build_dependency("sklearn.model_selection")

    _require_range_index(df)
    y = df[stratify_on] if stratify_on is not None else None
    splitter_cls = model_selection.RepeatedStratifiedKFold if y is not None else model_selection.RepeatedKFold
    splitter = splitter_cls(n_splits=n_folds, n_repeats=n_repeats, random_state=random_state)
    splits: Splits = {}
    for i, (train, test) in enumerate(splitter.split(df, y)):
        splits.setdefault(i // n_folds, {})[i % n_folds] = (train.tolist(), test.tolist())
    return splits


def grouped_splits(
    df: pd.DataFrame,
    *,
    n_repeats: int,
    group_on: str | list[str],
    group_labels: str | None,
    n_folds: int = N_FOLDS,
    stratify_on: str | None = None,
    random_state: int = SPLIT_RANDOM_STATE,
) -> Splits:
    """Repeated k-fold cross-validation that keeps every group of ``group_on`` on one side (several columns: every
    combination of their values is a group).

    With ``group_labels="per_group"`` (one label per group) the folds are drawn over the groups, one row per
    group, as :func:`iid_splits` would draw them over rows; group sizes are ignored. Otherwise
    ``(Stratified)GroupKFold`` with ``shuffle=True`` and seed ``random_state + repeat`` (shuffled groups in about equal
    numbers per fold; the folds of the current datasets are within 5% of equal rows).
    """
    _require_range_index(df)
    df, group_on = one_group_column(df, group_on)
    if group_labels == "per_group":
        return _per_group_splits(df, n_repeats, n_folds, group_on, stratify_on, random_state)
    return _per_sample_splits(df, n_repeats, n_folds, group_on, stratify_on, random_state)


def _per_group_splits(
    df: pd.DataFrame, n_repeats: int, n_folds: int, group_on: str, stratify_on: str | None, random_state: int
) -> Splits:
    members: list[np.ndarray] = []
    labels: list[object] = []
    for _, rows in df.groupby(group_on, sort=False, observed=True):
        members.append(rows.index.to_numpy())
        if stratify_on is not None:
            values = rows[stratify_on].unique()
            if len(values) > 1:
                msg = f"group_labels='per_group', but a group of `{group_on}` has several values of `{stratify_on}`."
                raise ValueError(msg)
            labels.append(values[0])
    groups = pd.DataFrame({"group": range(len(members))})
    if stratify_on is not None:
        groups["label"] = labels
    group_folds = iid_splits(
        groups,
        n_repeats=n_repeats,
        n_folds=n_folds,
        stratify_on="label" if stratify_on is not None else None,
        random_state=random_state,
    )

    def rows_of(group_positions: list[int]) -> list[int]:
        return np.concatenate([members[g] for g in group_positions]).tolist()

    return {
        repeat: {fold: (rows_of(train), rows_of(test)) for fold, (train, test) in folds.items()}
        for repeat, folds in group_folds.items()
    }


def _per_sample_splits(
    df: pd.DataFrame, n_repeats: int, n_folds: int, group_on: str, stratify_on: str | None, random_state: int
) -> Splits:
    model_selection = import_build_dependency("sklearn.model_selection")
    multiclass = import_build_dependency("sklearn.utils.multiclass")

    y = df[stratify_on] if stratify_on is not None else None
    if y is not None and multiclass.type_of_target(y) not in ("binary", "multiclass"):
        msg = f"Stratified grouped splits need a binary or multiclass `{stratify_on}`; cast it to `category`."
        raise ValueError(msg)
    splitter_cls = model_selection.StratifiedGroupKFold if y is not None else model_selection.GroupKFold
    splits: Splits = {}
    for repeat in range(n_repeats):
        splitter = splitter_cls(n_splits=n_folds, shuffle=True, random_state=random_state + repeat)
        for fold, (train, test) in enumerate(splitter.split(df, y, groups=df[group_on])):
            splits.setdefault(repeat, {})[fold] = (train.tolist(), test.tolist())
    return splits


# --- temporal windows -----------------------------------------------------------------------------------------


@dataclass(frozen=True)
class TemporalSplits:
    """Declarative expanding-window temporal splits (see :func:`temporal_window_splits`).

    Test windows walk back from the newest data, train is every earlier row, and split 0 is the newest
    window. Use at least 3 windows. Examples from the collection::

        TemporalSplits(window=5, unit="days", n_windows=5)                    # the last 5 x 5 days
        TemporalSplits(window=42, unit="days", n_windows=3, gap=1)            # 6-week windows, 1-day gap
        TemporalSplits(window=1, unit="years", cutoffs=(2023, 2024, 2025))     # one calendar year each
        TemporalSplits(window=None, unit="unique", n_windows=9, min_train_fraction=0.5)
        TemporalSplits(window=7, unit="days", n_windows=3)                    # a `_1m` version: 3 weeks

    A window of fixed length is the prediction horizon (:attr:`horizon`): ``window`` ``unit`` for a calendar unit,
    ``window`` steps for ``unit="rows"``.
    """

    window: int | None = 1
    unit: TemporalUnit = "days"
    n_windows: int | None = None
    step: int | None = None
    gap: int = 0
    cutoffs: tuple | None = None
    min_train_fraction: float | None = None

    def __post_init__(self) -> None:
        problems = []
        if self.unit not in (*_CALENDAR_UNITS, "unique", "rows"):
            problems.append(f"unit={self.unit!r} is not one of {(*_CALENDAR_UNITS, 'unique', 'rows')}")
        for name in ("window", "step", "n_windows"):
            value = getattr(self, name)
            if value is not None and (not isinstance(value, int) or value <= 0):
                problems.append(f"{name}={value!r} must be a positive integer")
        if not isinstance(self.gap, int) or self.gap < 0:
            problems.append(f"gap={self.gap!r} must be a non-negative integer")
        if self.min_train_fraction is not None and not 0 < self.min_train_fraction < 1:
            problems.append(f"min_train_fraction={self.min_train_fraction!r} must lie between 0 and 1")
        if self.cutoffs is not None and (self.n_windows is not None or self.step is not None):
            problems.append("cutoffs fix the windows, so n_windows and step would be ignored")
        if self.cutoffs is None and self.n_windows is None and self.min_train_fraction is None:
            problems.append(
                "set n_windows, cutoffs or min_train_fraction: otherwise the windows walk back to the start"
            )
        if problems:
            raise ValueError("TemporalSplits: " + "; ".join(problems) + ".")

    def splits(self, df: pd.DataFrame, time_on: str) -> Splits:
        """Build the splits for ``df`` (sorted by ``time_on``)."""
        return temporal_window_splits(
            df,
            time_on=time_on,
            window=self.window,
            unit=self.unit,
            n_windows=self.n_windows,
            step=self.step,
            gap=self.gap,
            cutoffs=list(self.cutoffs) if self.cutoffs is not None else None,
            min_train_fraction=self.min_train_fraction,
        )

    def describe(self, n_built: int, *, derived_window: int | None = None) -> str:
        """The splits comment for these windows (``derived_window``: the length ``window=None`` resolved to)."""
        unit = {"unique": "time values", "rows": "rows"}.get(self.unit, self.unit)
        window = self.window if self.window is not None else derived_window
        size = f"{window} {unit}" if window is not None else "from each cutoff to the end of the data"
        if self.cutoffs is not None:
            where = f"starting at {', '.join(str(c) for c in sorted(self.cutoffs, reverse=True))}"
        else:
            where = "walking back from the newest data"
        text = f"Expanding-window temporal splits: {n_built} test window(s) of {size}, {where}, newest first"
        if self.step is not None and self.window is not None and self.step != self.window:
            text += f", moving by {self.step} {unit}"
        text += "; train is all earlier data"
        if self.gap:
            text += f" up to a gap of {self.gap} {unit}"
        return text + "."

    @property
    def horizon(self) -> tuple[int, str] | None:
        """``(time_horizon, time_horizon_unit)`` set by a fixed-length window, else None.

        A calendar window gives ``(window, unit)`` and a row window ``(window, "steps")``. ``unit="unique"`` gives
        None: a window of distinct time values has no unit (the values may be days, years or an index), and neither
        has ``window=None`` (the windows run from each cutoff to the end of the data).
        """
        if self.window is None:
            return None
        if self.unit in _CALENDAR_UNITS:
            return self.window, self.unit
        if self.unit == "rows":
            return self.window, "steps"
        return None


HorizonUnit = Literal["steps", "days", "weeks", "months", "years"]


@dataclass(frozen=True)
class Temporal:
    """The temporal regime of a v2 definition: the time column, the test windows and the prediction horizon.

    Declared as ``temporal = Temporal(...)`` in ``dataset.py``. Examples from the collection::

        Temporal(on="date", splits=TemporalSplits(window=1, unit="months", n_windows=3))      # horizon: 1 month
        Temporal(on="t", splits=TemporalSplits(window=320, unit="rows", n_windows=9))         # horizon: 320 steps
        Temporal(on="Year", splits=TemporalSplits(unit="unique", n_windows=3), horizon=1, horizon_unit="years")
        Temporal(on="arrival_date", horizon=3, horizon_unit="months")                           # `_make_splits`

    Attributes:
        on: The time column; the frame is sorted by it and future rows never train a split.
        splits: The declarative expanding windows; None when the definition implements ``_make_splits``.
        horizon: How far ahead the task predicts, for windows that do not fix it (``unit="unique"``, ``window=None``,
            or ``_make_splits``). A fixed-length window is the horizon (:attr:`TemporalSplits.horizon`), and
            declaring it again is an error, so the two cannot disagree.
        horizon_unit: ``steps``, ``days``, ``weeks``, ``months`` or ``years``; set together with ``horizon``.

    The container stores the column as the task's ``time_on`` and the horizon as the splits' ``time_horizon`` /
    ``time_horizon_unit``.
    """

    on: str
    splits: TemporalSplits | None = None
    horizon: int | None = None
    horizon_unit: HorizonUnit | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.on, str) or not self.on.strip():
            msg = "Temporal.on must name the time column."
            raise ValueError(msg)
        if self.splits is not None and not isinstance(self.splits, TemporalSplits):
            msg = f"Temporal.splits must be a TemporalSplits, got {type(self.splits).__name__}."
            raise ValueError(msg)
        if (self.horizon is None) != (self.horizon_unit is None):
            msg = "Temporal: set `horizon` and `horizon_unit` together."
            raise ValueError(msg)
        if self.horizon is not None and self.horizon <= 0:
            msg = f"Temporal.horizon must be positive, got {self.horizon!r}."
            raise ValueError(msg)
        implied = self.splits.horizon if self.splits is not None else None
        if self.horizon is not None and implied is not None:
            window, unit = implied
            msg = (
                f"Temporal: the windows set the horizon ({window} {unit}); drop `horizon={self.horizon!r}, "
                f"horizon_unit={self.horizon_unit!r}`. Declare a horizon only for windows that do not fix one "
                "(unit='unique', window=None, or `_make_splits`)."
            )
            raise ValueError(msg)

    @property
    def resolved_horizon(self) -> tuple[int | None, str | None]:
        """``(horizon, horizon_unit)``: set by the windows, else as declared, else ``(None, None)``."""
        if self.horizon is not None:
            return self.horizon, self.horizon_unit
        if self.splits is not None and self.splits.horizon is not None:
            return self.splits.horizon
        return None, None


def temporal_window_splits(  # noqa: C901, PLR0912 - one branch per unit and stop rule
    df: pd.DataFrame,
    *,
    time_on: str,
    window: int | None = 1,
    unit: TemporalUnit = "days",
    n_windows: int | None = None,
    step: int | None = None,
    gap: int = 0,
    cutoffs: list | tuple | None = None,
    min_train_fraction: float | None = None,
) -> Splits:
    """Expanding-window temporal splits: test windows walking back from the newest data, train = all earlier rows.

    Each test window covers ``window`` units; the next window moves back by ``step`` units (default: ``window``,
    so windows are contiguous; ``step < window`` makes consecutive windows overlap). Train is every row strictly
    before the window start minus ``gap`` units (a planning gap between prediction time and the test period).
    Rows after a window are unused by that split. Split 0 is the newest window (``{window_i: {0: (train, test)}}``),
    the layout the bundle checks expect.

    Windows stop when ``n_windows`` are built, when a window or its train side would be empty, or when the train
    side falls below ``min_train_fraction`` of all rows.

    Args:
        df: The frame, sorted ascending by ``time_on`` with a RangeIndex (splits are positions).
        time_on: The time column: datetime for calendar units, any sortable type for ``"unique"``/``"rows"``.
        window: Test-window length in ``unit``. With ``cutoffs``, None means "from the cutoff to the end of the
            data". For ``"unique"``/``"rows"``, None derives the length from ``n_windows`` and
            ``min_train_fraction``: the newest ``1 - min_train_fraction`` of the values (rows) is cut into
            ``n_windows`` equal windows.
        unit: See :data:`TemporalUnit`.
        n_windows: How many windows to build (None: as many as the stop rules allow).
        step: How far each window moves back, in ``unit`` (default ``window``).
        gap: Units between the end of train and the start of the test window.
        cutoffs: Explicit test-window starts (for example ``[2023, 2024, 2025]``) instead of walking back from the
            newest data. They are ordered newest first; ``n_windows`` and ``step`` are ignored.
        min_train_fraction: Stop before a window whose train side has less than this share of the data: of the
            distinct time values for ``"unique"``, of the rows otherwise.

    Returns:
        The outer splits ``{window_i: {0: (train_positions, test_positions)}}``, newest window first.
    """
    times = df[time_on]
    if not times.is_monotonic_increasing:
        raise ValueError(f"`{time_on}` must be sorted ascending (sort the frame before splitting).")
    _require_range_index(df)
    if unit not in (*_CALENDAR_UNITS, "unique", "rows"):
        raise ValueError(f"Unknown unit {unit!r}.")
    if unit in _CALENDAR_UNITS and not pd.api.types.is_datetime64_any_dtype(times):
        raise ValueError(f"Calendar unit {unit!r} needs a datetime `{time_on}`; use unit='unique' or 'rows'.")
    n_rows = len(df)
    positions = np.arange(n_rows)

    # Express every window as a half-open interval [start, end) on an ordered "axis": timestamps for
    # calendar units, positions in the sorted unique values for "unique", row positions for "rows".
    if unit == "unique":
        values = pd.Index(times.unique())
        axis = values.get_indexer(times)
        axis_max = len(values)
    elif unit == "rows":
        axis = positions
        axis_max = n_rows
    else:
        axis = times

    if window is None and cutoffs is None:
        if unit in _CALENDAR_UNITS or n_windows is None or min_train_fraction is None:
            raise ValueError("window=None needs unit 'unique'/'rows' with n_windows and min_train_fraction.")
        window = int(axis_max * (1 - min_train_fraction) / n_windows)
        if window < 1:
            raise ValueError("Too few time values for that many windows.")
    step = window if step is None else step

    intervals: list[tuple] = []
    if cutoffs is not None:
        for cutoff in sorted(cutoffs, reverse=True):
            if unit in _CALENDAR_UNITS:
                start = pd.Timestamp(str(cutoff))
                if times.dt.tz is not None and start.tzinfo is None:  # a plain cutoff means the column's time zone
                    start = start.tz_localize(times.dt.tz)
                end = None if window is None else start + _calendar_offset(unit, window)
                train_end = start - _calendar_offset(unit, gap) if gap else start
            else:
                start = int(values.get_loc(cutoff)) if unit == "unique" else int(cutoff)
                end = None if window is None else start + window
                train_end = start - gap
            intervals.append((start, end, train_end))
    else:
        i = 0
        while n_windows is None or i < n_windows:
            if unit in _CALENDAR_UNITS:
                end = _calendar_end(times.iloc[-1], unit) - _calendar_offset(unit, step * i)
                start = end - _calendar_offset(unit, window)
                train_end = start - _calendar_offset(unit, gap) if gap else start
                if train_end <= times.iloc[0]:
                    break
            else:
                end = axis_max - step * i
                start = end - window
                train_end = start - gap
                if start <= 0:
                    break
            intervals.append((start, end, train_end))
            i += 1
            if n_windows is None and i > 10_000:
                break

    splits: Splits = {}
    for start, end, train_end in intervals:
        test_mask = (axis >= start) & ((axis < end) if end is not None else True)
        train_mask = axis < train_end
        test_idx = positions[np.asarray(test_mask)].tolist()
        train_idx = positions[np.asarray(train_mask)].tolist()
        if not test_idx or not train_idx:
            if cutoffs is not None:
                raise ValueError(f"The window starting at {start} has an empty train or test side.")
            break
        if min_train_fraction is not None:
            # Share of the axis: distinct time values for "unique", rows otherwise.
            share = train_end / axis_max if unit == "unique" else len(train_idx) / n_rows
            if share < min_train_fraction - 1e-9:
                break
        splits[len(splits)] = {0: (train_idx, test_idx)}
    if not splits:
        raise ValueError("No temporal window could be built; check window, unit and the data's time range.")
    return splits


def _calendar_offset(unit: str, n: int) -> pd.DateOffset:
    return pd.DateOffset(**{unit: n})


def _calendar_end(last: pd.Timestamp, unit: str) -> pd.Timestamp:
    """The exclusive end of the newest window: the unit boundary after ``last``."""
    day = last.normalize()
    if unit in ("days", "weeks"):
        return day + pd.Timedelta(days=1)
    if unit == "months":
        return day.replace(day=1) + pd.DateOffset(months=1)
    return day.replace(month=1, day=1) + pd.DateOffset(years=1)


# --- the row budget -------------------------------------------------------------------------------------------


@dataclass
class SplitPlan:
    """What a custom ``_make_splits`` may return instead of bare splits.

    Attributes:
        splits: The outer splits as positions in ``df`` (or in the input frame if ``df`` is None).
        df: The frame the splits index into, when the split step reduces or reorders it (sub-sampling).
            None keeps the input frame.
        comment: The splits comment, for a comment computed from the data (else ``splits_comment``).
    """

    splits: Splits
    df: pd.DataFrame | None = None
    comment: str | None = None


def subsample_frame(
    df: pd.DataFrame,
    *,
    group_on: str | list[str] | None = None,
    stratify_on: str | None = None,
    n_rows: int | None = None,
    random_state: int = SPLIT_RANDOM_STATE,
) -> pd.DataFrame:
    """Sub-sample ``df`` to ``n_rows`` rows (default :data:`FRAME_ROW_BUDGET`), keeping the row order.

    Without ``group_on`` rows are sampled, stratified on ``stratify_on``; with it whole groups are kept (see
    :func:`_sample_positions`). The kept rows stay in their order, so a frame sorted by time stays sorted. A frame
    within the budget is returned as it is.
    """
    n_rows = FRAME_ROW_BUDGET if n_rows is None else n_rows
    if len(df) <= n_rows:
        return df
    keyed, key = one_group_column(df, group_on)
    keep = _sample_positions(
        keyed, np.arange(len(df)), n_rows, group_on=key, stratify_on=stratify_on, random_state=random_state
    )
    return df.iloc[keep].reset_index(drop=True)


def cap_splits(
    df: pd.DataFrame,
    splits: Splits,
    *,
    group_on: str | list[str] | None = None,
    stratify_on: str | None = None,
    train_cap: int | None = None,
    test_cap: int | None = None,
    random_state: int = SPLIT_RANDOM_STATE,
) -> tuple[Splits, bool]:
    """Trim every split side over its cap (defaults :data:`TRAIN_ROW_BUDGET`, :data:`TEST_ROW_BUDGET`).

    A side over the cap is sampled like :func:`subsample_frame` does (rows or whole groups); sides within it are
    left as they are. Returns the splits and whether any side was trimmed.
    """
    caps = (TRAIN_ROW_BUDGET if train_cap is None else train_cap, TEST_ROW_BUDGET if test_cap is None else test_cap)
    df, group_on = one_group_column(df, group_on)
    trimmed = False
    capped: Splits = {}
    for repeat, folds in splits.items():
        capped[repeat] = {}
        for fold, sides in folds.items():
            new_sides = []
            for side, cap in zip(sides, caps, strict=True):
                if len(side) > cap:
                    side = _sample_positions(  # noqa: PLW2901 - the trimmed side replaces the original
                        df, np.asarray(side), cap, group_on=group_on, stratify_on=stratify_on, random_state=random_state
                    ).tolist()
                    trimmed = True
                new_sides.append(side)
            capped[repeat][fold] = (new_sides[0], new_sides[1])
    return capped, trimmed


def sample_temporal_splits(
    df: pd.DataFrame,
    splits: Splits,
    *,
    stratify_on: str | None = None,
    train_cap: int | None = None,
    test_cap: int | None = None,
    random_state: int = SPLIT_RANDOM_STATE,
) -> tuple[pd.DataFrame, Splits, bool]:
    """Sample temporal splits to the row budget per window, then reduce the frame to the rows the splits use.

    Every side over its cap (defaults :data:`TRAIN_ROW_BUDGET`, :data:`TEST_ROW_BUDGET`) keeps the rows that come
    first in one random order of the frame, so a test window stays dense and a train side is a random draw from all
    earlier rows, and the train sides of the windows overlap as much as their caps allow. With ``stratify_on`` each
    class keeps its share of the cap. Rows no split uses are dropped and the positions follow; the row order is kept,
    so a frame sorted by time stays sorted.

    Returns:
        The reduced frame, its splits, and whether any side was over its cap.
    """
    caps = (TRAIN_ROW_BUDGET if train_cap is None else train_cap, TEST_ROW_BUDGET if test_cap is None else test_cap)
    rank = np.random.default_rng(random_state).permutation(len(df))  # one random order for every split
    labels = pd.factorize(df[stratify_on].to_numpy())[0] if stratify_on is not None else None
    trimmed = False
    sampled: Splits = {}
    for repeat, folds in splits.items():
        sampled[repeat] = {}
        for fold, sides in folds.items():
            new_sides = []
            for side, cap in zip(sides, caps, strict=True):
                positions = np.asarray(side)
                if len(positions) > cap:
                    positions = _first_in_order(positions, cap, rank, labels)
                    trimmed = True
                new_sides.append(positions)
            sampled[repeat][fold] = (new_sides[0], new_sides[1])

    used = np.unique(np.concatenate([side for folds in sampled.values() for sides in folds.values() for side in sides]))
    reduced = df.iloc[used].reset_index(drop=True)
    remapped: Splits = {
        repeat: {
            fold: (np.searchsorted(used, train).tolist(), np.searchsorted(used, test).tolist())
            for fold, (train, test) in folds.items()
        }
        for repeat, folds in sampled.items()
    }
    return reduced, remapped, trimmed


def _first_in_order(positions: np.ndarray, cap: int, rank: np.ndarray, labels: np.ndarray | None) -> np.ndarray:
    """The ``cap`` positions that come first in ``rank``, sorted; with ``labels``, each class keeps its share."""
    if labels is None:
        quotas = {None: cap}
        groups = {None: positions}
    else:
        side_labels = labels[positions]
        classes, counts = np.unique(side_labels, return_counts=True)
        exact = counts * cap / len(positions)
        quota = np.floor(exact).astype(int)
        # largest remainders get the leftover rows; a stable sort breaks ties the same way on every CPU
        quota[np.argsort(quota - exact, kind="stable")[: cap - quota.sum()]] += 1
        quotas = dict(zip(classes, quota, strict=True))
        groups = {c: positions[side_labels == c] for c in classes}
    kept = [members[np.argsort(rank[members], kind="stable")[: quotas[c]]] for c, members in groups.items()]
    return np.sort(np.concatenate(kept))


def _sample_positions(
    df: pd.DataFrame,
    positions: np.ndarray,
    cap: int,
    *,
    group_on: str | None,
    stratify_on: str | None,
    random_state: int,
) -> np.ndarray:
    """At most ``cap`` of ``positions``, sorted: sampled rows, or whole groups of ``group_on``.

    Rows are drawn stratified on ``stratify_on`` (when every class has two rows or more). Groups are taken in a
    random order, each one that still fits under the cap, until the cap is reached; with ``stratify_on`` that order
    interleaves the groups of each stratum (a group's stratum is its most frequent value), so the kept groups keep
    about the class balance.
    """
    if len(positions) <= cap:
        return np.sort(positions)
    side = df.iloc[positions]
    if group_on is None:
        model_selection = import_build_dependency("sklearn.model_selection")

        labels = side[stratify_on] if stratify_on is not None else None
        if labels is not None and labels.astype(object).value_counts().min() < 2:  # stratifying needs 2 rows per class
            labels = None
        kept, _ = model_selection.train_test_split(
            positions, train_size=cap, stratify=labels, random_state=random_state
        )
        return np.sort(kept)

    rng = np.random.default_rng(random_state)
    codes, uniques = pd.factorize(side[group_on].to_numpy())
    sizes = np.bincount(codes, minlength=len(uniques))
    order = rng.permutation(len(uniques))
    if stratify_on is not None:
        # a group's stratum is its most frequent value; a tie goes to the value that comes first in the frame (an
        # explicit order: `value_counts` sorts unstably, so ties fell differently on CPUs with and without AVX512)
        stratum_codes = pd.factorize(side[stratify_on].to_numpy())[0]
        counts = pd.DataFrame({"group": codes, "stratum": stratum_codes}).value_counts(sort=False).rename("n")
        counts = counts.reset_index().sort_values(
            ["group", "n", "stratum"], ascending=[True, False, True], kind="stable"
        )
        top = counts.drop_duplicates("group").set_index("group")["stratum"]
        strata_codes = pd.factorize(top.reindex(range(len(uniques))).to_numpy()[order])[0]
        # rank of each group inside its stratum, scaled to [0, 1): sorting on it interleaves the strata
        rank = np.zeros(len(order))
        for stratum in np.unique(strata_codes):
            members = np.flatnonzero(strata_codes == stratum)
            rank[members] = (np.arange(len(members)) + 0.5) / len(members)
        order = order[np.argsort(rank, kind="stable")]
    kept = np.zeros(len(uniques), dtype=bool)
    total = 0
    for group in order:
        if total + sizes[group] <= cap:
            kept[group] = True
            total += sizes[group]
        if total == cap:
            break
    return np.sort(positions[kept[codes]])


# --- checks -----------------------------------------------------------------------------------------------------


def protocol_checks(container: CuratedContainer) -> list[CheckResult]:
    """The split-protocol checks of a format-2 container; :func:`~data_foundry.bundle_checks.run_bundle_checks` runs
    them in place of the v1 protocol checks.

    * ``splits_dimensions_off_protocol`` (warning): IID or grouped splits other than :func:`recommended_dimensions`.
    * ``splits_test_over_budget`` (warning): a split tests on more than :data:`TEST_ROW_BUDGET` rows.
    * ``splits_too_few`` (warning): a temporal task with fewer than :data:`MIN_TEMPORAL_SPLITS` test windows.

    The train budget is the same as in v1, so ``splits_train_over_budget`` stays with the shared bundle checks.
    """
    task = container.task_metadata
    splits = container.experiment_metadata.splits
    flat = [(r, f, train, test) for r, folds in splits.items() for f, (train, test) in folds.items()]
    findings: list[CheckResult] = []

    over_test = [(r, f, len(test)) for r, f, _train, test in flat if len(test) > TEST_ROW_BUDGET]
    if over_test:
        largest = max(n for *_, n in over_test)
        findings.append(
            CheckResult(
                "splits_test_over_budget",
                "warning",
                f"{len(over_test)} split(s) test on more than {TEST_ROW_BUDGET:,} rows (largest: {largest:,}); "
                f"first: {[(r, f) for r, f, _ in over_test[:5]]}.",
                hint="Sub-sample the frame in a `<name>_1m` version (`subsample_to_budget = True`), narrow the test "
                "windows, or accept it with the reason.",
            ),
        )

    if task.time_on is not None:
        if len(flat) < MIN_TEMPORAL_SPLITS:
            findings.append(
                CheckResult(
                    "splits_too_few",
                    "warning",
                    f"{len(flat)} test window(s); the v2 protocol wants at least {MIN_TEMPORAL_SPLITS}.",
                    hint="Declare more windows, e.g. `TemporalSplits(window=7, unit='days', n_windows=3)` or three "
                    "`cutoffs`.",
                ),
            )
        return findings

    folds_per_repeat = {len(folds) for folds in splits.values()}
    if not flat or len(folds_per_repeat) != 1:
        return findings
    actual = (len(splits), folds_per_repeat.pop())
    recommended = recommended_dimensions(container.dataset, group_on=task.group_on, group_labels=task.group_labels)
    if actual != recommended:
        findings.append(
            CheckResult(
                "splits_dimensions_off_protocol",
                "warning",
                f"Splits are {actual[0]}x{actual[1]} but the v2 protocol for this size is "
                f"{recommended[0]}x{recommended[1]}.",
                hint="Deviating is allowed when the task demands it; record why in `splits_comment`.",
            ),
        )
    return findings


def rows_text(n: int) -> str:
    """A row budget for comments: 1,500,000 -> "1.5M", 500,000 -> "500k"."""
    return f"{n / 1e6:g}M" if n >= 1_000_000 else f"{n / 1e3:g}k"


def _require_range_index(df: pd.DataFrame) -> None:
    if not df.index.equals(pd.RangeIndex(len(df))):
        raise ValueError("The frame needs a fresh RangeIndex (splits are positions): call `reset_index(drop=True)`.")
