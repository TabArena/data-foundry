"""The v2 split protocol: how every v2 dataset is split, and the checks that hold it.

* IID and grouped data get repeated 3-fold cross-validation. The number of repeats follows the size of the train
  side, in the units the metric scores (:func:`recommended_dimensions`): 20, 10, 3 or 1.
* Temporal data gets at least 3 expanding windows (:class:`TemporalSplits`).
* Data Foundry sets no row budget: by default the splits use the full frame and no side is capped. A sub-sampled
  version declares one (``row_budget = RowBudget(train=..., test=...)``, :class:`~data_foundry.schema.RowBudget`),
  is named after its train budget (``<name>_1m``, ``<name>_10m``) and records it in the container
  (``experiment_metadata.row_budget``); the split checks hold the container to it (:func:`protocol_checks`).
  TabArena v0.2 sub-samples its larger datasets to ``RowBudget(train=1_000_000, test=500_000)``.
* An IID or grouped version adapts its splits to the budget: a frame above ``train + test`` rows is sub-sampled to
  it (:func:`subsample_frame`), then each fold tests on up to ``test`` rows of its third and trains on every other
  row, at most ``train`` (:func:`fit_splits_to_budget`). At 1M / 500k that is plain 3-fold cross-validation on 1.5M
  rows; at 10M / 250k each fold trains on 10M and tests on 250k rows of a 10.25M-row frame.
* A temporal version samples per window instead of sampling the frame (:func:`sample_temporal_splits`): each test
  window keeps up to ``test`` of its rows, each train side a random ``train`` of all earlier rows (one random order
  for all windows), and the frame keeps only the rows some split uses. ``TemporalSplits(sample_by="time")`` draws
  whole time values instead of rows (every row of a drawn time value is kept), for data whose rows at one time form
  a cross-section.

This module does not use the v1 helpers in :mod:`data_foundry.curation_recommendations`, which keep the v1 protocol
(one 1M / 250k split from 1.25M rows on) for the v1 notebooks. The cross-validation builders give the same splits
as the v1 ones, so a dataset below 1.25M rows keeps its splits.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal

import numpy as np
import pandas as pd

from data_foundry.bundle_checks import CheckResult
from data_foundry.schema import RowBudget, TimeUnit, TrainSampling, as_column_list
from data_foundry.v2._optional import import_build_dependency

if TYPE_CHECKING:
    from data_foundry.curation_container import CuratedContainer
    from data_foundry.schema import PredictiveMLTaskMetadataV2

Splits = dict[int, dict[int, tuple[list[int], list[int]]]]
"""Outer splits: ``{repeat: {fold: (train_positions, test_positions)}}``."""

SPLIT_RANDOM_STATE = 4267
"""The seed of every split and of the sub-sampling (the same seed as the v1 helpers)."""

N_FOLDS = 3
"""Every IID and grouped split is 3-fold cross-validation."""

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

GapUnit = Literal["minutes", "hours", "days", "weeks", "months", "years"]
"""The unit of a calendar window's gap when it differs from the window's (``TemporalSplits(gap_unit=...)``)."""

_GAP_UNITS = ("minutes", "hours", *_CALENDAR_UNITS)

STEPS_PER_YEAR: dict[str, int] = {
    "minutes": 525_600,
    "hours": 8_760,
    "days": 365,
    "weeks": 52,
    "months": 12,
    "quarters": 4,
    "years": 1,
}
"""How many steps of a numeric time column (:attr:`Temporal.time_unit`) make a year."""

SampleBy = Literal["rows", "time"]
"""What a temporal version's per-window sampling to its ``row_budget`` draws (``TemporalSplits(sample_by=...)``).

* ``"rows"``: rows, in one random order of the frame (the default).
* ``"time"``: whole values of the time column, in one random order of the values; every row of a drawn value is kept.
"""


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


def metric_group_column(task: PredictiveMLTaskMetadataV2) -> str | None:
    """The column whose values the task's metric scores one by one (its ``group`` input: an instance, a patient, an
    era), or ``None`` for a metric that scores rows.
    """
    return task.objective_metric.inputs.get("group")


def scored_groups_held_out_whole(df: pd.DataFrame, group_on: str | list[str] | None, score_group_on: str) -> bool:
    """Whether every group the metric scores lies in one group of the split, so a test fold holds it whole: the
    metric's group is the split's group or sits inside one (an instance inside its problem class). ``False`` for an
    IID split, which cuts every group across folds.
    """
    if group_on is None:
        return False
    keyed, key = one_group_column(df, group_on)
    return bool(keyed.groupby(score_group_on, dropna=False, observed=True)[key].nunique(dropna=False).max() <= 1)


def recommended_dimensions(
    df: pd.DataFrame,
    *,
    group_on: str | list[str] | None = None,
    group_labels: str | None = None,
    score_group_on: str | None = None,
) -> tuple[int, int]:
    """``(n_repeats, n_folds)`` for IID or grouped cross-validation on ``df``.

    The size is the train side of a 3-fold split, in the units the metric scores: 2/3 of the distinct values of
    ``score_group_on`` when the metric scores per group and each of its groups lies in one group of the split, so a
    test fold holds it whole (one PAR10 per instance over a row per instance and solver, the instances held out or
    inside held-out classes); else of the groups for ``per_group`` labels, else of the rows. A metric group the split
    cuts across folds (a survey year over stations held out) is scored on part of its rows in every fold, so its count
    says little about the noise and the rows count. Below 500 it gets 20 repeats, below 2,500 10, below 250k 3, and 1
    above. A frame of :data:`SINGLE_REPEAT_ROWS` rows or more always gets one repeat.

    Args:
        df: The frame to split.
        group_on: The split's group column(s), for grouped data.
        group_labels: The grouping's labels; ``"per_group"`` counts the groups of ``group_on``.
        score_group_on: The metric's group column (:func:`metric_group_column`); its distinct values are counted
            when each lies in one group of ``group_on``.

    Returns:
        ``(n_repeats, n_folds)``.
    """
    n = len(df)
    if n >= SINGLE_REPEAT_ROWS:
        return 1, N_FOLDS
    if score_group_on is not None and scored_groups_held_out_whole(df, group_on, score_group_on):
        n = df[score_group_on].nunique(dropna=False)
    elif group_on is not None and group_labels == "per_group":
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
    df, group_on = _sampling_columns(df, group_on, stratify_on)
    if group_labels == "per_group":
        return _per_group_splits(df, n_repeats, n_folds, group_on, stratify_on, random_state)
    return _per_sample_splits(df, n_repeats, n_folds, group_on, stratify_on, random_state)


def _per_group_splits(
    df: pd.DataFrame, n_repeats: int, n_folds: int, group_on: str, stratify_on: str | None, random_state: int
) -> Splits:
    codes, _ = pd.factorize(df[group_on])  # groups in order of first appearance; a missing key is in no group
    in_group = np.flatnonzero(codes >= 0)
    order = in_group[np.argsort(codes[in_group], kind="stable")]  # the rows group by group, each group in row order
    group_of = codes[order]
    sizes = np.bincount(group_of)
    starts = np.cumsum(sizes) - sizes  # the first row of each group in `order`
    groups = pd.DataFrame({"group": range(len(starts))})
    if stratify_on is not None:
        values = df[stratify_on].iloc[order].reset_index(drop=True)
        if values.groupby(group_of, sort=False).nunique(dropna=False).max() > 1:
            msg = f"group_labels='per_group', but a group of `{group_on}` has several values of `{stratify_on}`."
            raise ValueError(msg)
        groups["label"] = values.iloc[starts].to_list()
    group_folds = iid_splits(
        groups,
        n_repeats=n_repeats,
        n_folds=n_folds,
        stratify_on="label" if stratify_on is not None else None,
        random_state=random_state,
    )

    def rows_of(group_positions: list[int]) -> list[int]:
        chosen = np.zeros(len(starts), dtype=bool)
        chosen[group_positions] = True
        return order[chosen[group_of]].tolist()  # group by group, as the sorted group positions come

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
        TemporalSplits(window=7, unit="days", n_windows=3)                    # 3 weekly windows
        TemporalSplits(window=91, unit="days", n_windows=3, gap=15, gap_unit="minutes", sample_by="time")

    A window of fixed length is the prediction horizon (:attr:`horizon`): ``window`` ``unit`` for a calendar unit,
    ``window`` steps for ``unit="rows"``.

    ``gap`` counts in ``unit`` unless ``gap_unit`` names another unit: a calendar window can leave a gap of minutes
    or hours (``gap=15, gap_unit="minutes"``, for a label known 16 minutes after its row). ``gap_unit`` needs a
    calendar ``unit`` and a gap.

    ``sample_by`` matters only in a version with a ``row_budget``: its test windows over the budget are sampled
    (:func:`sample_temporal_splits`), and a benchmark sub-samples its train sides (:func:`subsample_train`).
    ``"rows"`` (default) draws rows, ``"time"`` whole values of the time column, so every row of a drawn time value is
    kept or dropped together. Use ``"time"`` when the rows at one time form a cross-section the target or the features
    are relative to (the 14 coins of a minute). It does not stratify.
    """

    window: int | None = 1
    unit: TemporalUnit = "days"
    n_windows: int | None = None
    step: int | None = None
    gap: int = 0
    cutoffs: tuple | None = None
    min_train_fraction: float | None = None
    gap_unit: GapUnit | None = None
    sample_by: SampleBy = "rows"

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
        problems += self._gap_unit_and_sampling_problems()
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

    def _gap_unit_and_sampling_problems(self) -> list[str]:
        problems = []
        if self.gap_unit is not None:
            if self.gap_unit not in _GAP_UNITS:
                problems.append(f"gap_unit={self.gap_unit!r} is not one of {_GAP_UNITS}")
            if self.unit not in _CALENDAR_UNITS:
                problems.append(f"gap_unit needs a calendar unit {_CALENDAR_UNITS}, not unit={self.unit!r}")
            if not self.gap:
                problems.append("gap_unit is set, but there is no gap (gap=0)")
        if self.sample_by not in ("rows", "time"):
            problems.append(f"sample_by={self.sample_by!r} is not one of ('rows', 'time')")
        return problems

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
            gap_unit=self.gap_unit,
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
            text += f" up to a gap of {self.gap} {self.gap_unit or unit}"
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

    @property
    def gap_length(self) -> tuple[int, str] | None:
        """``(time_gap, time_gap_unit)`` of a gap in a calendar unit (``gap_unit``, else ``unit``) or in rows, else
        None.

        No gap gives None, and so does ``unit="unique"``: a gap of distinct time values has no unit, so the
        definition declares it on :class:`Temporal`.
        """
        if not self.gap:
            return None
        if self.unit in _CALENDAR_UNITS:
            return self.gap, self.gap_unit or self.unit
        if self.unit == "rows":
            return self.gap, "steps"
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
        Temporal(on="cohort", splits=TemporalSplits(unit="unique", n_windows=9, gap=5), horizon=1,
                 horizon_unit="years", gap=5, gap_unit="years")                               # gap: 5 cohorts
        Temporal(on="era", splits=TemporalSplits(window=52, unit="unique", n_windows=3, gap=4), horizon=52,
                 horizon_unit="weeks", gap=4, gap_unit="weeks", time_unit="weeks")             # an era is a week

    Attributes:
        on: The time column; the frame is sorted by it and future rows never train a split.
        splits: The declarative expanding windows; None when the definition implements ``_make_splits``.
        horizon: How far ahead the task predicts, for windows that do not fix it (``unit="unique"``, ``window=None``,
            or ``_make_splits``). A fixed-length window is the horizon (:attr:`TemporalSplits.horizon`), and
            declaring it again is an error, so the two cannot disagree.
        horizon_unit: ``steps``, ``days``, ``weeks``, ``months`` or ``years``; set together with ``horizon``.
        gap: The span between the end of training and the start of each test window, for a gap the windows do not
            state in a unit: ``TemporalSplits(unit="unique", gap=...)`` (required then) or a gap built in
            ``_make_splits``. A gap in a calendar unit or in rows is stated by the windows
            (:attr:`TemporalSplits.gap_length`), and declaring it again is an error.
        gap_unit: The unit of ``gap``, as for ``horizon_unit``; set together with ``gap``.
        time_unit: What one step of a time column that is a number counts (``minutes`` to ``years``): numerai's
            ``era`` counts weeks. It gives the column a calendar, which the newest-year rule of the train sampler
            needs (:func:`subsample_train`), so a version with a ``row_budget`` on a numeric time column declares
            it. A date column has its own calendar and declares none; a time that is only an order (a row number)
            has none.

    The container stores the column as the task's ``time_on`` (with ``time_unit``), the horizon as the splits'
    ``time_horizon`` / ``time_horizon_unit`` and the gap as their ``time_gap`` / ``time_gap_unit``.
    """

    on: str
    splits: TemporalSplits | None = None
    horizon: int | None = None
    horizon_unit: HorizonUnit | None = None
    gap: int | None = None
    gap_unit: HorizonUnit | None = None
    time_unit: TimeUnit | None = None

    def __post_init__(self) -> None:
        if self.time_unit is not None and self.time_unit not in STEPS_PER_YEAR:
            msg = f"Temporal.time_unit={self.time_unit!r} is not one of {tuple(STEPS_PER_YEAR)}."
            raise ValueError(msg)
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
        self._check_gap()

    def _check_gap(self) -> None:
        if (self.gap is None) != (self.gap_unit is None):
            msg = "Temporal: set `gap` and `gap_unit` together."
            raise ValueError(msg)
        if self.gap is not None and (not isinstance(self.gap, int) or self.gap <= 0):
            msg = f"Temporal.gap must be a positive integer, got {self.gap!r}."
            raise ValueError(msg)
        if self.splits is None:
            return
        stated = self.splits.gap_length
        if self.gap is not None and stated is not None:
            msg = (
                f"Temporal: the windows state the gap ({stated[0]} {stated[1]}); drop `gap={self.gap!r}, "
                f"gap_unit={self.gap_unit!r}`."
            )
            raise ValueError(msg)
        if self.gap is not None and not self.splits.gap:
            msg = "Temporal: `gap` is declared, but the windows leave none (TemporalSplits(gap=0))."
            raise ValueError(msg)
        if self.gap is None and self.splits.gap and stated is None:
            msg = (
                f"Temporal: the windows leave a gap of {self.splits.gap} distinct time values; state it in a unit "
                "with `gap=..., gap_unit=...` (e.g. 5 cohorts of a yearly column: gap=5, gap_unit='years')."
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

    @property
    def resolved_gap(self) -> tuple[int | None, str | None]:
        """``(gap, gap_unit)``: stated by the windows, else as declared, else ``(None, None)`` (no gap)."""
        if self.gap is not None:
            return self.gap, self.gap_unit
        if self.splits is not None and self.splits.gap_length is not None:
            return self.splits.gap_length
        return None, None


@dataclass(frozen=True)
class WindowBounds:
    """One temporal window as row positions of a frame sorted by time (:func:`window_bounds`).

    The train side is the positions ``[0, train_stop)``, the test window ``[test_start, test_stop)``. ``start``,
    ``end`` and ``train_end`` are the window's bounds on its axis (a time for a calendar unit, a position among the
    distinct values for ``"unique"``, a row for ``"rows"``; ``end`` None runs to the end of the data).
    """

    start: Any
    end: Any
    train_end: Any
    train_stop: int
    test_start: int
    test_stop: int


def temporal_window_splits(
    df: pd.DataFrame,
    *,
    time_on: str,
    window: int | None = 1,
    unit: TemporalUnit = "days",
    n_windows: int | None = None,
    step: int | None = None,
    gap: int = 0,
    gap_unit: GapUnit | None = None,
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
    side falls below ``min_train_fraction`` of all rows. Explicit ``cutoffs`` must include the newest window: the
    newest cutoff's window holds the newest row (SPLIT-15).

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
        gap_unit: The unit of ``gap`` for a calendar ``unit`` when it differs from ``unit`` (``"minutes"``,
            ``"hours"`` or a calendar unit); None counts the gap in ``unit``.
        cutoffs: Explicit test-window starts (for example ``[2023, 2024, 2025]``) instead of walking back from the
            newest data: the curator's choice of windows (SPLIT-15). They are ordered newest first; ``n_windows``
            and ``step`` are ignored.
        min_train_fraction: Stop before a window whose train side has less than this share of the data: of the
            distinct time values for ``"unique"``, of the rows otherwise.

    Returns:
        The outer splits ``{window_i: {0: (train_positions, test_positions)}}``, newest window first.
    """
    bounds = window_bounds(
        df,
        time_on=time_on,
        window=window,
        unit=unit,
        n_windows=n_windows,
        step=step,
        gap=gap,
        gap_unit=gap_unit,
        cutoffs=cutoffs,
        min_train_fraction=min_train_fraction,
    )
    return {i: {0: (list(range(b.train_stop)), list(range(b.test_start, b.test_stop)))} for i, b in enumerate(bounds)}


def window_bounds(  # noqa: C901, PLR0912 - one branch per unit and stop rule
    df: pd.DataFrame,
    *,
    time_on: str,
    window: int | None = 1,
    unit: TemporalUnit = "days",
    n_windows: int | None = None,
    step: int | None = None,
    gap: int = 0,
    gap_unit: GapUnit | None = None,
    cutoffs: list | tuple | None = None,
    min_train_fraction: float | None = None,
) -> list[WindowBounds]:
    """The windows of :func:`temporal_window_splits` as position ranges (:class:`WindowBounds`), newest first.

    The frame is sorted by ``time_on``, so every train side and every test window is a range of positions; a frame
    of tens of millions of rows and hundreds of candidate windows (:func:`~data_foundry.v2.windows.candidate_windows`)
    needs no index lists. The arguments are those of :func:`temporal_window_splits`.
    """
    times = df[time_on]
    if not times.is_monotonic_increasing:
        raise ValueError(f"`{time_on}` must be sorted ascending (sort the frame before splitting).")
    _require_range_index(df)
    if unit not in (*_CALENDAR_UNITS, "unique", "rows"):
        raise ValueError(f"Unknown unit {unit!r}.")
    if unit in _CALENDAR_UNITS and not pd.api.types.is_datetime64_any_dtype(times):
        raise ValueError(f"Calendar unit {unit!r} needs a datetime `{time_on}`; use unit='unique' or 'rows'.")
    if gap_unit is not None and (unit not in _CALENDAR_UNITS or gap_unit not in _GAP_UNITS):
        raise ValueError(f"gap_unit={gap_unit!r} needs a calendar unit and one of {_GAP_UNITS}.")
    gap_unit = gap_unit or unit
    n_rows = len(df)

    # Express every window as a half-open interval [start, end) on an ordered "axis": timestamps for
    # calendar units, positions in the sorted unique values for "unique", row positions for "rows".
    if unit == "unique":
        values = pd.Index(times.unique())
        axis = values.get_indexer(times)
        axis_max = len(values)
    elif unit == "rows":
        axis = np.arange(n_rows)
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
                train_end = start - _calendar_offset(gap_unit, gap) if gap else start
            else:
                start = int(values.get_loc(cutoff)) if unit == "unique" else int(cutoff)
                end = None if window is None else start + window
                train_end = start - gap
            intervals.append((start, end, train_end))
        _require_newest_window(intervals[0][1], times, None if unit in _CALENDAR_UNITS else axis_max, unit)
    else:
        i = 0
        while n_windows is None or i < n_windows:
            if unit in _CALENDAR_UNITS:
                end = _calendar_end(times.iloc[-1], unit) - _calendar_offset(unit, step * i)
                start = end - _calendar_offset(unit, window)
                train_end = start - _calendar_offset(gap_unit, gap) if gap else start
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

    def before(value: Any) -> int:  # how many rows lie before ``value`` on the axis
        if unit in _CALENDAR_UNITS:
            return int(times.searchsorted(value, side="left"))
        return int(np.searchsorted(axis, value, side="left"))

    bounds: list[WindowBounds] = []
    for start, end, train_end in intervals:
        test_start, test_stop = before(start), (n_rows if end is None else before(end))
        train_stop = before(train_end)
        if test_stop <= test_start or not train_stop:
            if cutoffs is not None:
                raise ValueError(f"The window starting at {start} has an empty train or test side.")
            break
        if min_train_fraction is not None:
            # Share of the axis: distinct time values for "unique", rows otherwise.
            share = train_end / axis_max if unit == "unique" else train_stop / n_rows
            if share < min_train_fraction - 1e-9:
                break
        bounds.append(WindowBounds(start, end, train_end, train_stop, test_start, test_stop))
    if not bounds:
        raise ValueError("No temporal window could be built; check window, unit and the data's time range.")
    return bounds


def _require_newest_window(end: Any, times: pd.Series, axis_max: int | None, unit: str) -> None:
    """Explicit cutoffs include the newest window: the newest cutoff's window holds the newest row (SPLIT-15)."""
    if end is None:
        return
    reaches = times.iloc[-1] < end if unit in _CALENDAR_UNITS else end >= axis_max
    if not reaches:
        msg = (
            f"The newest cutoff's window ends at {end}, before the newest data ({times.iloc[-1]}): the newest window "
            "is always a test window (SPLIT-15). Add a cutoff whose window holds the newest rows."
        )
        raise ValueError(msg)


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
    n_rows: int,
    group_on: str | list[str] | None = None,
    stratify_on: str | None = None,
    random_state: int = SPLIT_RANDOM_STATE,
) -> pd.DataFrame:
    """Sub-sample ``df`` to ``n_rows`` rows, keeping the row order.

    Without ``group_on`` rows are sampled, stratified on ``stratify_on``; with it whole groups are kept (see
    :func:`_sample_positions`). The kept rows stay in their order, so a frame sorted by time stays sorted. A frame
    within ``n_rows`` is returned as it is.
    """
    if len(df) <= n_rows:
        return df
    keyed, key = _sampling_columns(df, group_on, stratify_on)
    keep = _sample_positions(
        keyed, np.arange(len(df)), n_rows, group_on=key, stratify_on=stratify_on, random_state=random_state
    )
    return df.iloc[keep].reset_index(drop=True)


def fit_splits_to_budget(
    df: pd.DataFrame,
    splits: Splits,
    budget: RowBudget,
    *,
    group_on: str | list[str] | None = None,
    stratify_on: str | None = None,
    random_state: int = SPLIT_RANDOM_STATE,
) -> tuple[Splits, bool]:
    """Fit cross-validation splits to a row budget: each fold tests on at most ``budget.test`` rows of its test side
    and trains on every other row of the frame.

    A test side over ``budget.test`` is sampled like :func:`subsample_frame` does (rows stratified on
    ``stratify_on``, or whole groups), and the rows it leaves out train in that fold. The train sides are not capped:
    ``budget.train`` is for a benchmark, which sub-samples each train side before a fit (:func:`subsample_train`).
    Test sides within the budget are left as they are.

    Returns:
        The splits, and whether any test side was sampled.
    """
    keyed, key = _sampling_columns(df, group_on, stratify_on)

    def sample(positions: np.ndarray, cap: int) -> np.ndarray:
        return _sample_positions(
            keyed, positions, cap, group_on=key, stratify_on=stratify_on, random_state=random_state
        )

    sampled = False
    fitted: Splits = {}
    for repeat, folds in splits.items():
        fitted[repeat] = {}
        for fold, (cv_train, cv_test) in folds.items():
            train, test = cv_train, cv_test
            if len(cv_test) > budget.test:
                kept = sample(np.asarray(cv_test), budget.test)
                left_out = np.setdiff1d(cv_test, kept, assume_unique=True)  # untested rows of the fold train in it
                train, test = np.sort(np.concatenate([np.asarray(cv_train), left_out])).tolist(), kept.tolist()
                sampled = True
            fitted[repeat][fold] = (train, test)
    return fitted, sampled


def _sampling_columns(
    df: pd.DataFrame, group_on: str | list[str] | None, stratify_on: str | None
) -> tuple[pd.DataFrame, str | None]:
    """Only the columns sampling reads (the group key and the stratum), and one column naming the groups.

    No sampling step copies the whole frame.
    """
    columns = list(dict.fromkeys([*as_column_list(group_on), *([stratify_on] if stratify_on is not None else [])]))
    return one_group_column(df[columns], group_on)


def sample_temporal_splits(
    df: pd.DataFrame,
    splits: Splits,
    budget: RowBudget,
    *,
    stratify_on: str | None = None,
    whole_values_of: str | None = None,
    random_state: int = SPLIT_RANDOM_STATE,
) -> tuple[pd.DataFrame, Splits, bool]:
    """Sample the test windows of temporal splits to a row budget, then reduce the frame to the rows the splits use.

    A test side over ``budget.test`` keeps the rows that come first in one random order of the frame, so the window
    stays covered from its start to its end. The train sides are not capped: each keeps every earlier row (minus the
    gap), and ``budget.train`` is for a benchmark, which sub-samples a train side before a fit
    (:func:`subsample_train`). With ``stratify_on`` each class keeps its share of the cap. Rows no split uses are
    dropped (the newest window's rows its sample leaves out) and the positions follow; the row order is kept, so a
    frame sorted by time stays sorted.

    With ``whole_values_of`` (the time column, ``TemporalSplits(sample_by="time")``) a test side over its cap keeps
    whole values of that column instead of rows: the values come in one random order (the same seed), and a side
    takes them in that order, every row of a value, while the total stays within the cap. The value that would cross
    the cap and all later ones are dropped, so a side keeps at most the cap and at most one value's rows fewer. It
    does not stratify, so ``stratify_on`` must be None.

    Returns:
        The reduced frame, its splits, and whether any test side was over its cap.
    """
    caps = (None, budget.test)
    if whole_values_of is not None:
        if stratify_on is not None:
            msg = "Sampling whole time values does not stratify: pass `stratify_on=None` with `whole_values_of`."
            raise ValueError(msg)
        codes, uniques = pd.factorize(df[whole_values_of].to_numpy())
        value_rank = np.random.default_rng(random_state).permutation(len(uniques))  # one order of the values
    else:
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
                if cap is not None and len(positions) > cap:
                    if whole_values_of is not None:
                        positions = _first_values_in_order(positions, cap, codes, value_rank)
                    else:
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


def _first_values_in_order(positions: np.ndarray, cap: int, codes: np.ndarray, value_rank: np.ndarray) -> np.ndarray:
    """The positions of the values (``codes``) that come first in ``value_rank``, whole, while their rows fit ``cap``;
    sorted. The value that would cross the cap and every later one are dropped.
    """
    side_codes = codes[positions]
    values, counts = np.unique(side_codes, return_counts=True)
    order = np.argsort(value_rank[values], kind="stable")
    n_kept = int(np.searchsorted(np.cumsum(counts[order]), cap, side="right"))
    if n_kept == 0:
        msg = f"A single time value holds more than {cap:,} rows; whole time values cannot fit the cap."
        raise ValueError(msg)
    return np.sort(positions[np.isin(side_codes, values[order[:n_kept]])])


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
    side = df[list(dict.fromkeys(c for c in (group_on, stratify_on) if c is not None))].iloc[positions]
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


# --- the default sampler of a train side ------------------------------------------------------------------------

NEWEST_HISTORY = pd.DateOffset(years=1)
"""The history the default sampler of a temporal train side draws from: its newest year."""


def sample_train_positions(
    df: pd.DataFrame,
    positions: list[int] | np.ndarray,
    n_rows: int,
    *,
    time_on: str | None = None,
    time_unit: str | None = None,
    group_on: str | list[str] | None = None,
    stratify_on: str | None = None,
    whole_values_of: str | None = None,
    random_state: int = SPLIT_RANDOM_STATE,
) -> np.ndarray:
    """The default sub-sample of a train side: at most ``n_rows`` of ``positions`` (rows of ``df``), sorted.

    Deterministic, and blind to any model or score:

    * a temporal train side (``time_on``): the newest year, extended back in time until it holds ``n_rows`` rows, and
      a random ``n_rows`` of those (stratified on ``stratify_on``, or whole values of ``whole_values_of``). The year
      is the calendar year before the side's newest row on a date column, and :data:`STEPS_PER_YEAR` steps of
      ``time_unit`` on a numeric one (52 weekly eras);
    * a grouped one (``group_on``): whole groups in a random order, stratified by each group's most frequent class;
    * an IID one: random rows, stratified on ``stratify_on``.

    A side within ``n_rows`` is returned whole. The issue's study (#70) found the newest year best for temporal data:
    the newest rows alone lose seasons and weekdays on dense data, and all history dilutes recent data on long ones.
    """
    positions = np.asarray(positions)
    if len(positions) <= n_rows:
        return np.sort(positions)
    rng = np.random.default_rng(random_state)
    if time_on is not None:
        times = df[time_on].to_numpy()[positions]
        if pd.api.types.is_datetime64_any_dtype(df[time_on]):
            recent = positions[times >= times.max() - NEWEST_HISTORY]
        elif time_unit is not None:
            recent = positions[times > times.max() - STEPS_PER_YEAR[time_unit]]
        else:
            msg = f"`{time_on}` is no date: the newest year needs what one step of it counts (`time_unit`)."
            raise ValueError(msg)
        if len(recent) < n_rows:  # the year holds fewer: extended back in time to the newest n_rows rows
            return _newest(positions, n_rows, times, None if whole_values_of is None else df[whole_values_of])
        positions = recent
    if time_on is not None or group_on is None:
        if whole_values_of is not None:
            codes, uniques = pd.factorize(df[whole_values_of].to_numpy())
            return _first_values_in_order(positions, n_rows, codes, rng.permutation(len(uniques)))
        labels = pd.factorize(df[stratify_on].to_numpy())[0] if stratify_on is not None else None
        return _first_in_order(positions, n_rows, rng.permutation(len(df)), labels)
    keyed, key = _sampling_columns(df, group_on, stratify_on)
    return _sample_positions(keyed, positions, n_rows, group_on=key, stratify_on=stratify_on, random_state=random_state)


def _newest(positions: np.ndarray, cap: int, times: np.ndarray, values: pd.Series | None) -> np.ndarray:
    """The newest ``cap`` of ``positions`` by ``times``, sorted; with ``values``, whole values while they fit."""
    order = np.argsort(times, kind="stable")[::-1]  # newest first
    if values is None:
        return np.sort(positions[order[:cap]])
    side = values.to_numpy()[positions]
    codes, uniques = pd.factorize(side[order])  # codes in order of first appearance: newest value first
    counts = np.bincount(codes, minlength=len(uniques))
    n_kept = int(np.searchsorted(np.cumsum(counts), cap, side="right"))
    if n_kept == 0:
        msg = f"A single time value holds more than {cap:,} rows; whole time values cannot fit the cap."
        raise ValueError(msg)
    return np.sort(positions[order][codes < n_kept])


def subsample_train(
    container: CuratedContainer,
    repeat: int,
    fold: int,
    n_rows: int | None = None,
    *,
    random_state: int = SPLIT_RANDOM_STATE,
) -> list[int]:
    """The train positions a benchmark fits split ``(repeat, fold)`` on: its train side sub-sampled to the budget.

    The default sampler (:func:`sample_train_positions`) with the container's constraints
    (``experiment_metadata.train_sampling``): the newest year of a temporal side extended back to ``n_rows`` rows
    (the year of a numeric time column from ``task_metadata.time_unit``), whole groups, whole time values, the
    stratum. ``n_rows`` defaults to the container's train budget (``row_budget.train``); a container without one, or a
    side within it, gives the train side whole::

        for repeat, folds in container.experiment_metadata.splits.items():
            for fold, (train, test) in folds.items():
                train = subsample_train(container, repeat, fold)
                model.fit(X.iloc[train], y.iloc[train])
    """
    meta = container.experiment_metadata
    train, _test = meta.splits[repeat][fold]
    budget = getattr(meta, "row_budget", None)
    n_rows = n_rows if n_rows is not None else (budget.train if budget is not None else None)
    if n_rows is None or len(train) <= n_rows:
        return list(train)
    task = container.task_metadata
    sampling = getattr(meta, "train_sampling", None)
    time_on = getattr(task, "time_on", None)
    unit = sampling.unit if sampling is not None else ("groups" if task.group_on is not None else "rows")
    kept = sample_train_positions(
        container.dataset,
        train,
        n_rows,
        time_on=time_on if sampling is None or sampling.default == "newest_year" else None,
        time_unit=getattr(task, "time_unit", None),
        group_on=task.group_on if unit == "groups" else None,
        stratify_on=sampling.stratify_on if sampling is not None else task.stratify_on,
        whole_values_of=time_on if unit == "time_values" else None,
        random_state=random_state,
    )
    return kept.tolist()


# --- checks -----------------------------------------------------------------------------------------------------


def protocol_checks(container: CuratedContainer) -> list[CheckResult]:
    """The split-protocol checks of a format-2 container; :func:`~data_foundry.bundle_checks.run_bundle_checks` runs
    them in place of the v1 protocol checks.

    * ``splits_test_over_budget`` (warning): a split tests on more rows than the container's
      ``experiment_metadata.row_budget.test``. A container without a budget has no size limit; the train sides are
      sub-sampled by a benchmark, not in the container.
    * ``splits_train_sampling_missing`` (error): a container with a row budget records no ``train_sampling``.
    * ``splits_dimensions_off_protocol`` (warning): IID or grouped splits other than :func:`recommended_dimensions`.
    * ``splits_too_few`` (warning): a temporal task with fewer than :data:`MIN_TEMPORAL_SPLITS` test windows.
    """
    task = container.task_metadata
    splits = container.experiment_metadata.splits
    flat = [(r, f, train, test) for r, folds in splits.items() for f, (train, test) in folds.items()]
    meta = container.experiment_metadata
    findings = _budget_findings(flat, meta.row_budget, getattr(meta, "train_sampling", None))

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
    recommended = recommended_dimensions(
        container.dataset,
        group_on=task.group_on,
        group_labels=task.group_labels,
        score_group_on=metric_group_column(task),
    )
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


def _budget_findings(
    flat: list[tuple[int, int, list[int], list[int]]], budget: RowBudget | None, sampling: TrainSampling | None
) -> list[CheckResult]:
    """The test sides over the container's test budget (warning), and a budget without its train sampling (error)."""
    if budget is None:
        return []
    findings: list[CheckResult] = []
    over = [(r, f, len(test)) for r, f, _train, test in flat if len(test) > budget.test]
    if over:
        largest = max(n for *_, n in over)
        findings.append(
            CheckResult(
                "splits_test_over_budget",
                "warning",
                f"{len(over)} split(s) test on more than {budget.test:,} rows, the container's test budget (largest: "
                f"{largest:,}); first: {[(r, f) for r, f, _ in over[:5]]}.",
                hint="A definition with `row_budget` samples its test sides to it in `default_splits`; splits built "
                "another way must keep to the budget they record.",
            ),
        )
    if sampling is None:
        findings.append(
            CheckResult(
                "splits_train_sampling_missing",
                "error",
                "The container records a row budget but no `train_sampling`: a benchmark cannot tell how to "
                "sub-sample the train sides to the train budget.",
                hint="Build it from a v2 definition, which records both.",
            ),
        )
    return findings


def _require_range_index(df: pd.DataFrame) -> None:
    if not df.index.equals(pd.RangeIndex(len(df))):
        raise ValueError("The frame needs a fresh RangeIndex (splits are positions): call `reset_index(drop=True)`.")
