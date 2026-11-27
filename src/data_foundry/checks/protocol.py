"""The numbers of the v2 split protocol and the checks that hold a format-2 container to them.

The protocol itself, how a definition draws its splits, is :mod:`data_foundry.definition.splits`; it takes its
numbers from here (:func:`recommended_dimensions`, :data:`N_FOLDS`). The checks read only the container, so
:func:`~data_foundry.checks.bundle.run_bundle_checks` runs them for every format-2 container, built from a definition
or not (:func:`protocol_checks`).
"""

from __future__ import annotations

import hashlib
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

from data_foundry.checks.results import CheckResult
from data_foundry.sampling import one_group_column
from data_foundry.schema import as_column_list

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence

    from data_foundry.curation_container import CuratedContainer
    from data_foundry.row_table import Splits
    from data_foundry.schema import PredictiveMLTaskMetadataV2, RowBudget, TrainSampling

N_FOLDS = 3
"""Every IID and grouped split is 3-fold cross-validation."""

MIN_TEMPORAL_SPLITS = 3
"""A temporal task needs at least this many test windows."""

REPEATS_BY_TRAIN_SIZE = ((500, 20), (2_500, 10), (250_000, 3))
"""``(train-size limit, repeats)``: a train side below the limit gets that many repeats; larger ones get 1."""

# --- split dimensions ----------------------------------------------------------------------------------------


def scored_unit_column(task: PredictiveMLTaskMetadataV2) -> str | None:
    """The column of the task's scored units, the rows its metric combines into one term of its score: the metric's
    ``group`` input (an instance, a patient, an era). ``None`` for a metric that scores rows, one row a unit.
    """
    return task.objective_metric.inputs.get("group")


def scored_units_within_groups(df: pd.DataFrame, group_on: str | list[str] | None, scored_unit_on: str) -> bool:
    """Whether all rows of each scored unit are in one group of the split, so a test fold holds the unit whole: the
    unit is the group or sits inside one (an instance inside its problem class). ``False`` for an IID split, which
    cuts every unit across the folds.
    """
    if group_on is None:
        return False
    keyed, key = one_group_column(df, group_on)
    return bool(keyed.groupby(scored_unit_on, dropna=False, observed=True)[key].nunique(dropna=False).max() <= 1)


def repeats_for(n_units: int) -> int:
    """SPLIT-33's repeats of 3-fold cross-validation for ``n_units`` units: by the units on the train side (two thirds
    of them), 20, 10, 3 or 1.
    """
    n_train = int(n_units * 2 / 3)
    return next((repeats for limit, repeats in REPEATS_BY_TRAIN_SIZE if n_train < limit), 1)


def split_count(n_units: int) -> int:
    """The number of splits SPLIT-33 gives a dataset of ``n_units`` scored units: repeats x folds."""
    return repeats_for(n_units) * N_FOLDS


def training_sides(trains: Iterable[Sequence[int]]) -> int:
    """The number of distinct training sides among ``trains`` (the train positions of each split): test parts that
    share one training side test one model, so they count as one split (SPLIT-14, SPLIT-15). Sides that differ in
    length or at an end are told apart at once; only sides that agree there are hashed whole.
    """
    by_shape: dict[tuple[int, int, int], list[np.ndarray]] = {}
    for t in trains:
        side = np.asarray(t, dtype=np.int64)
        shape = (len(side), int(side.min()) if len(side) else -1, int(side.max()) if len(side) else -1)
        by_shape.setdefault(shape, []).append(side)
    count = 0
    for sides in by_shape.values():
        if len(sides) == 1:
            count += 1
        else:
            count += len({hashlib.blake2b(np.sort(s).tobytes(), digest_size=16).digest() for s in sides})
    return count


def recommended_dimensions(
    df: pd.DataFrame,
    *,
    group_on: str | list[str] | None = None,
    group_labels: str | None = None,
    scored_unit_on: str | None = None,
) -> tuple[int, int]:
    """``(n_repeats, n_folds)`` for IID or grouped cross-validation on ``df``.

    The repeats follow the units on the train side of a 3-fold split (2/3 of them): below 500 20 repeats, below
    2,500 10, below 250k 3, and 1 above, however many rows the frame has. The units, in order: the groups for
    ``per_group`` labels (one label covers a group, so the scored units inside it add none); else the scored units
    when all rows of each are in one group (one PAR10 per instance over a row per instance and solver, the instances
    held out or inside held-out classes); else the rows. A scored unit cut across groups (a survey year over held-out
    stations) is scored on part of its rows in every fold, so its count says little about the noise and the rows
    count. A row budget does not change the count: it caps the sides after the split (:func:`fit_splits_to_budget`).

    Args:
        df: The frame to split.
        group_on: The split's group column(s), for grouped data.
        group_labels: The grouping's labels; ``"per_group"`` counts the groups of ``group_on``.
        scored_unit_on: The column of the scored units (:func:`scored_unit_column`); they are counted when all rows
            of each are in one group of ``group_on``.

    Returns:
        ``(n_repeats, n_folds)``.
    """
    n, _ = counted_units(df, group_on=group_on, group_labels=group_labels, scored_unit_on=scored_unit_on)
    return repeats_for(n), N_FOLDS


def counted_units(
    df: pd.DataFrame,
    *,
    group_on: str | list[str] | None = None,
    group_labels: str | None = None,
    scored_unit_on: str | None = None,
) -> tuple[int, str]:
    """The units :func:`recommended_dimensions` counts, and what they are: ``(n, "groups")``, ``(n, "scored units")``
    or ``(n, "rows")``.
    """
    if group_on is not None and group_labels == "per_group":
        df, group_on = one_group_column(df, group_on)
        return int(df[group_on].nunique()), "groups"
    if scored_unit_on is not None and scored_units_within_groups(df, group_on, scored_unit_on):
        return int(df[scored_unit_on].nunique(dropna=False)), "scored units"
    return len(df), "rows"


def is_leave_one_group_out(df: pd.DataFrame, splits: Splits, group_on: str | list[str] | None) -> bool:
    """Whether ``splits`` hold out one whole group of ``group_on`` per fold, every group once, in one repeat, each
    fold training on all the other rows: the splits :class:`GroupedSplits` ``(kind="leave_one_group_out")`` builds.
    """
    columns = as_column_list(group_on)
    if len(splits) != 1 or len(columns) != 1 or columns[0] not in df.columns:
        return False
    keys = df[columns[0]].to_numpy()
    sizes = pd.Series(keys).value_counts(dropna=False)
    tested = []
    for train, test in next(iter(splits.values())).values():
        groups = pd.unique(keys[list(test)])
        if len(groups) != 1 or len(test) != sizes[groups[0]] or len(train) + len(test) != len(keys):
            return False
        tested.append(groups[0])
    return len(set(tested)) == len(tested) == len(sizes)


def protocol_checks(container: CuratedContainer) -> list[CheckResult]:
    """The split-protocol checks of a format-2 container; :func:`~data_foundry.checks.bundle.run_bundle_checks` runs
    them for every format-2 container.

    * ``splits_test_over_budget`` (warning): a split tests on more rows than the container's
      ``experiment_metadata.row_budget.test``. A container without a budget has no size limit; the train sides are
      sub-sampled by a benchmark, not in the container.
    * ``splits_train_sampling_missing`` (error): a container with a row budget records no ``train_sampling``.
    * ``splits_dimensions_off_protocol`` (warning): IID or grouped splits other than :func:`recommended_dimensions`
      (leave one group out, declared as ``GroupedSplits``, is the exception: :func:`is_leave_one_group_out`);
      or a temporal split with fewer windows (training sides) than SPLIT-33 gives an IID split of its scored units
      (SPLIT-15), the minimum of :data:`MIN_TEMPORAL_SPLITS` included.
    """
    task = container.task_metadata
    splits = container.experiment_metadata.splits
    flat = [(r, f, train, test) for r, folds in splits.items() for f, (train, test) in folds.items()]
    meta = container.experiment_metadata
    findings = _budget_findings(flat, meta.row_budget, getattr(meta, "train_sampling", None))

    if task.time_on is not None:
        return findings + _window_count_findings(container, [(r, train, test) for r, _f, train, test in flat])

    folds_per_repeat = {len(folds) for folds in splits.values()}
    if not flat or len(folds_per_repeat) != 1:
        return findings
    actual = (len(splits), folds_per_repeat.pop())
    if task.group_on is not None and is_leave_one_group_out(container.dataset, splits, task.group_on):
        return findings  # `GroupedSplits(kind="leave_one_group_out")`: one fold per group, repeats would copy them
    recommended = recommended_dimensions(
        container.dataset,
        group_on=task.group_on,
        group_labels=task.group_labels,
        scored_unit_on=scored_unit_column(task),
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


def scored_units_of(container: CuratedContainer, windows: list) -> pd.Series | None:
    """The scored unit of every row of a temporal split (SPLIT-33), or None when the rows count.

    A scored unit counts only where no window cuts it across its training and test sides (an era inside one
    window); a unit every window cuts (a taxon in every survey year) is scored on part of its rows in each, so the
    rows count, as SPLIT-33 counts them.

    Args:
        container: The container (its frame and task).
        windows: ``(repeat, train positions, test positions)`` of every window.
    """
    task = getattr(container, "task_metadata", None)
    unit = scored_unit_column(task) if task is not None else None
    frame = container.dataset
    if unit is None or not hasattr(frame, "columns") or unit not in frame.columns:
        return None
    units = frame[unit]
    values = units.to_numpy()
    for _repeat, train, test in windows:
        if np.intersect1d(pd.unique(values[list(test)]), pd.unique(values[list(train)])).size:
            return None
    return units


def _window_count_findings(container: CuratedContainer, windows: list) -> list[CheckResult]:
    """SPLIT-15 on a temporal split: as many windows, counted by training side, as SPLIT-33 gives an IID split of
    the scored units (:func:`scored_units_of`), never fewer than :data:`MIN_TEMPORAL_SPLITS`.
    """
    units = scored_units_of(container, windows)
    total = int(units.nunique(dropna=False)) if units is not None else len(container.dataset)
    target = split_count(total)
    n_sides = training_sides(train for _r, train, _test in windows)
    if n_sides >= target:
        return []
    shared = f" ({len(windows)} test parts)" if n_sides < len(windows) else ""
    floor = f"; the v2 protocol wants at least {MIN_TEMPORAL_SPLITS}" if n_sides < MIN_TEMPORAL_SPLITS else ""
    hint = (
        "Declare more windows, e.g. `TemporalSplits(window=7, unit='days', n_windows=3)` or three `cutoffs`: fewer "
        "than three are never accepted (SPLIT-15)."
        if floor
        else "SPLIT-15 aims at that count and accepts fewer: the splits comment names the target, the count reached "
        "and what stops more windows (the use case's horizon or gap, the training floor, the least test window); "
        "then accept this warning with it."
    )
    return [
        CheckResult(
            "splits_dimensions_off_protocol",
            "warning",
            f"{n_sides} test window(s) with their own training side{shared}, against the {target} splits an IID "
            f"split of {total:,} scored units would get (SPLIT-33){floor}.",
            hint=hint,
        )
    ]


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
