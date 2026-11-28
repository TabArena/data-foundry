"""The default sampler of a train side, and the row sampling of the split protocol.

A benchmark fits split ``(repeat, fold)`` of a container with a row budget (a ``_1m`` version) on at most
``row_budget.train`` of its train rows: :func:`subsample_train` draws them by the default sampler the container records
(``experiment_metadata.train_sampling``), and returns the train side whole for a container without a budget. The split
protocol (:mod:`data_foundry.definition.splits`) samples the test sides of a version with the same functions. Only numpy
and pandas: importing this module loads nothing of the build side.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

from data_foundry.schema import as_column_list

if TYPE_CHECKING:
    from data_foundry.curation_container import CuratedContainer

SPLIT_RANDOM_STATE = 4267
"""The seed of every split and of the sub-sampling."""

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


def _sampling_columns(
    df: pd.DataFrame, group_on: str | list[str] | None, stratify_on: str | None
) -> tuple[pd.DataFrame, str | None]:
    """Only the columns sampling reads (the group key and the stratum), and one column naming the groups.

    No sampling step copies the whole frame.
    """
    columns = list(dict.fromkeys([*as_column_list(group_on), *([stratify_on] if stratify_on is not None else [])]))
    return one_group_column(df[columns], group_on)


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

    Rows are the ``cap`` that come first in one random order of the frame (seed ``random_state``), each class of
    ``stratify_on`` keeping its share of the cap (:func:`_first_in_order`, the sampler of a train side). Groups are
    taken in a random order, each one that still fits under the cap, until the cap is reached; with ``stratify_on``
    that order interleaves the groups of each stratum (a group's stratum is its most frequent value), so the kept
    groups keep about the class balance. When no group fits under the cap it raises rather than return an empty side.
    """
    if len(positions) <= cap:
        return np.sort(positions)
    if group_on is None:
        labels = pd.factorize(df[stratify_on].to_numpy())[0] if stratify_on is not None else None
        rank = np.random.default_rng(random_state).permutation(len(df))
        return _first_in_order(np.asarray(positions), cap, rank, labels)
    side = df[list(dict.fromkeys(c for c in (group_on, stratify_on) if c is not None))].iloc[positions]

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
    if not total:
        msg = (
            f"No whole group of `{group_on}` fits under the cap of {cap:,} rows (the smallest holds {sizes.min():,}): "
            "sampling whole groups would leave the side empty. Raise the row budget or use smaller groups."
        )
        raise ValueError(msg)
    return np.sort(positions[kept[codes]])


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
    return train_positions(container, repeat, fold, n_rows, random_state=random_state).tolist()


def train_positions(
    container: CuratedContainer,
    repeat: int,
    fold: int,
    n_rows: int | None = None,
    *,
    random_state: int = SPLIT_RANDOM_STATE,
) -> np.ndarray:
    """:func:`subsample_train` as an ``int64`` array, without the round trip through a Python list."""
    meta = container.experiment_metadata
    train, _test = meta.splits[repeat][fold]
    budget = getattr(meta, "row_budget", None)
    n_rows = n_rows if n_rows is not None else (budget.train if budget is not None else None)
    if n_rows is None or len(train) <= n_rows:
        return np.asarray(train, dtype=np.int64)
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
    return np.asarray(kept, dtype=np.int64)
