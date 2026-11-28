"""The benchmark's view of a container: one object with everything a harness needs to fit and score a task.

``task = container.task()`` (:class:`BenchmarkTask`) gathers what a benchmark otherwise reads from several helpers
and from rules written in prose: the model inputs, the columns an inner validation split reads, the special features,
the training and validation weights, the folds within the row budget, the metric with its best value, and the scorer.
It reads both container formats::

    task = container.task()
    for fold in task.folds():
        model.fit(task.X(fold.train), task.y(fold.train), sample_weight=task.train_weight(fold.train))
        value = task.score(task.y(fold.test), model.predict(task.X(fold.test)), fold.test)
        error = task.error(value)  # lower is better, 0 at the metric's optimum

The view derives everything from the container's metadata through the helpers of
:mod:`data_foundry.curation_container`, :mod:`data_foundry.sampling` and :mod:`data_foundry.metrics`, which stay the
place of each rule. :meth:`BenchmarkTask.to_dict` writes the derived facts as JSON-able data; a format-2 container
saves them next to its metadata as ``benchmark_task.json`` (:data:`BENCHMARK_TASK_FILE`), for code that reads the
files without Data Foundry, with the Data Foundry version that wrote it; ``verify_saved_container`` recomputes it and
flags a file that no longer matches. Like the other consumer modules, this one loads nothing of the build side.
"""

from __future__ import annotations

import contextlib
import functools
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from importlib import metadata
from typing import TYPE_CHECKING, Any, Literal

import numpy as np
import pandas as pd
from pydantic import TypeAdapter

from data_foundry.curation_container import (
    feature_columns,
    sample_weight,
    special_features,
    split_columns,
    unit_weight,
    validation_weight,
)
from data_foundry.metrics import FALLBACK_METRICS, METRICS, metric_optimum, scorer
from data_foundry.sampling import SPLIT_RANDOM_STATE, STEPS_PER_YEAR, train_positions
from data_foundry.schema import Grouping, MetricSpec, RowBudget, SpecialFeature, as_column_list

if TYPE_CHECKING:
    from data_foundry.curation_container import CuratedContainer

BENCHMARK_TASK_FILE = "benchmark_task.json"
"""The file a format-2 container saves :meth:`BenchmarkTask.to_dict` in, next to its metadata. Derived from the
metadata, so it is not part of the checksum."""

TASK_VIEW_VERSION = 2
"""The version of the layout of :meth:`BenchmarkTask.to_dict`; raised when a key changes meaning or goes away.

Version 2 added ``regime``, ``split_roles``, ``needs_encoding`` and ``data_foundry_version``, and gives a format-1
group column as ``split_roles.group`` instead of a ``grouping``."""

Regime = Literal["iid", "grouped", "temporal"]
"""The split regime of a task, as a harness reads it: the shipped folds and an inner validation split follow it."""

SpecialMode = Literal["drop", "encode", "raw"]
"""How :meth:`BenchmarkTask.X` passes the special features on (see there)."""

_REGIMES: dict[str, Regime] = {"iid": "iid", "grouped_non_iid": "grouped", "temporal_non_iid": "temporal"}
_PANDAS_3 = int(pd.__version__.split(".", maxsplit=1)[0]) >= 3


def data_foundry_version() -> str:
    """The installed Data Foundry version (``unknown`` when the package metadata is missing, as in a source tree)."""
    try:
        return metadata.version("data-foundry")
    except metadata.PackageNotFoundError:
        return "unknown"


@dataclass(frozen=True)
class SplitRoles:
    """What each column an inner validation split reads is for (:attr:`BenchmarkTask.split_columns` is the flat list).

    Attributes:
        group: The group column(s): a group's rows stay on one side. Empty for a task without groups. A format-1
            group column is here (format 1 records no :class:`~data_foundry.schema.Grouping`).
        time: The time column of a temporal task (``time_on``): the newest rows are held out. ``None`` otherwise.
        gap: The gap the outer splits leave between a train side and its test window
            (``experiment_metadata.time_gap``), in :attr:`gap_unit`; ``None`` without one.
        gap_unit: The unit of :attr:`gap` (``steps``: distinct time values; a calendar unit otherwise).
        unit: The unit of a unit weight (each unit counts once in the score): a unit's rows stay on one side.
    """

    group: tuple[str, ...] = ()
    time: str | None = None
    gap: float | None = None
    gap_unit: str | None = None
    unit: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """The roles as JSON-able data."""
        return {
            "group": list(self.group),
            "time": self.time,
            "gap": self.gap,
            "gap_unit": self.gap_unit,
            "unit": self.unit,
        }


@dataclass(frozen=True, eq=False)
class Fold:
    """One outer split of a task: the rows a model fits on and the rows it is scored on, as positions in
    ``container.dataset``.

    Attributes:
        repeat: The repeat of the split.
        fold: The fold of the split within its repeat.
        train: The rows to fit on: the train side, or its default sample within the row budget (``_1m`` versions).
        test: The rows to score.
        train_side: The whole train side as shipped. A method that picks its own rows within the budget picks them
            from here, keeping the unit of ``experiment_metadata.train_sampling`` (a separate leaderboard track).
    """

    repeat: int
    fold: int
    train: np.ndarray
    test: np.ndarray
    train_side: np.ndarray


@dataclass(frozen=True, eq=False)
class BenchmarkTask:
    """What a benchmark needs to fit and score one container, built by :meth:`CuratedContainer.task`.

    A format-1 container (BeyondArena) gets the same view: its metric name as a spec, no weights, no special features,
    no grouping (as ``container.grouping``), and its group column (if any) in :attr:`split_roles`.

    Attributes:
        name: The dataset's ``unique_name``.
        format_version: The container format, 1 or 2.
        target: The target column.
        problem_type: ``binary_classification``, ``multiclass_classification`` or ``regression``.
        classes: The classes in sorted order (scikit-learn's ``classes_``): the column order of ``predict_proba`` the
            scorer reads, also for an ordered target, whose declared order is type information only. ``None`` for a
            regression task. A binary task's positive class is ``classes[1]``.
        features: Every model input (:func:`~data_foundry.curation_container.feature_columns`): no target, group,
            scoring or unit column, and no time column that dates the label. The columns of the special features are
            among them; :meth:`X` leaves out those in :attr:`needs_encoding` unless asked otherwise.
        needs_encoding: The feature columns whose raw values are no model input (a SMILES string: a special feature
            with ``encoding_required``). :meth:`X` drops them by default.
        regime: ``iid``, ``grouped`` or ``temporal``: what the shipped folds and an inner validation split follow.
        split_columns: The columns an inner validation split reads (group, time, unit;
            :func:`~data_foundry.curation_container.split_columns`), never inputs unless :attr:`features` lists them.
        split_roles: The role of each of them (:class:`SplitRoles`); :meth:`validation_split` cuts by these.
        special_features: The inputs that need an encoding by kind (a SMILES, a spectrum); ``X(rows,
            special="encode")`` encodes each with ``data_foundry.special.encode_special_feature``.
        metric: The metric spec; format 1 gets its ``objective_metric_name`` as one.
        greater_is_better: Whether a higher score is better.
        optimum: The best score any prediction can reach (1 for ROC AUC, 0 for RMSE), or ``None`` for a metric whose
            best value changes with the scored rows (``net_revenue_at_cost``, ``ordered_lorenz_gini``).
        grouping: How a grouped task is used (``container.grouping``), or ``None`` (always for format 1).
            ``grouping.prediction_unit == "group"`` means one prediction per group; the scorer aggregates row
            predictions by ``grouping.aggregation``.
        sample_weight: The training weight column, or ``None``: every fit takes it as the row weight
            (:meth:`train_weight`); it is never a feature, and its test-row values are for the scorer only.
        validation_weight: The column a validation loss is weighted by (the metric's row weight), or ``None``
            (:meth:`validation_weights`).
        unit_column: The unit of a unit weight (each unit counts once in the score), or ``None``: keep a unit's rows
            on one side of an inner split. Never a training weight.
        row_budget: The most rows a fit and a test side may hold (a ``_1m`` version), or ``None``. :meth:`folds`
            draws the training rows within it.
        time_unit: The calendar of a numeric time column (numerai's eras count ``weeks``), or ``None``.
    """

    container: CuratedContainer = field(repr=False)
    name: str
    format_version: int
    target: str
    problem_type: str
    classes: tuple[Any, ...] | None
    features: tuple[str, ...]
    needs_encoding: tuple[str, ...]
    regime: Regime
    split_columns: tuple[str, ...]
    split_roles: SplitRoles
    special_features: tuple[SpecialFeature, ...]
    metric: MetricSpec
    greater_is_better: bool
    optimum: float | None
    grouping: Grouping | None
    sample_weight: str | None
    validation_weight: str | None
    unit_column: str | None
    row_budget: RowBudget | None
    time_unit: str | None

    @classmethod
    def from_container(cls, container: CuratedContainer) -> BenchmarkTask:
        """The view of ``container`` (format 1 or 2); it needs the loaded frame."""
        if container.dataset is None:
            raise ValueError("the task view reads the frame: load the container with load_dataset=True.")
        task = container.task_metadata
        metric = task.objective_metric if container.format_version >= 2 else _format_1_spec(task)
        unit = unit_weight(container)
        special = tuple(special_features(container))
        features = tuple(feature_columns(container))
        coded = {c for f in special if f.encoding_required for c in f.columns}
        experiment = container.experiment_metadata
        gap = getattr(experiment, "time_gap", None)
        return cls(
            container=container,
            name=container.dataset_metadata.unique_name,
            format_version=container.format_version,
            target=task.target_column_name,
            problem_type=task.problem_type,
            classes=_classes(container.dataset[task.target_column_name], task.problem_type),
            features=features,
            needs_encoding=tuple(c for c in features if c in coded),
            regime=_REGIMES[task.split_regime],
            split_columns=tuple(split_columns(container)),
            split_roles=SplitRoles(
                group=tuple(as_column_list(task.group_on)),
                time=task.time_on,
                gap=None if gap is None else float(gap),
                gap_unit=getattr(experiment, "time_gap_unit", None),
                unit=unit.unit if unit is not None else None,
            ),
            special_features=special,
            metric=metric,
            greater_is_better=bool(metric.greater_is_better),
            optimum=metric_optimum(metric),
            grouping=container.grouping,
            sample_weight=sample_weight(container),
            validation_weight=validation_weight(container),
            unit_column=unit.unit if unit is not None else None,
            row_budget=getattr(experiment, "row_budget", None),
            time_unit=getattr(task, "time_unit", None),
        )

    # --- rows ---------------------------------------------------------------------------------------------------

    def folds(self, *, budget: bool = True) -> Iterator[Fold]:
        """Every outer split as shipped (never re-split or shuffle them: they encode the regime).

        The positions are read-only arrays; the default sample of each train side is drawn once per task and reused.

        Args:
            budget: Fit on the default sample of the train side within the row budget
                (:func:`~data_foundry.sampling.subsample_train`), the protocol of a ``_1m`` version. ``False`` gives
                the whole train side; a container without a budget gives it either way.
        """
        for repeat, folds in self.container.experiment_metadata.splits.items():
            for fold, (train, test) in folds.items():
                side = _read_only(np.asarray(train, dtype=np.int64))
                rows = side
                if budget and self.row_budget is not None:
                    rows = self._train_sample(repeat, fold)
                yield Fold(repeat, fold, rows, _read_only(np.asarray(test, dtype=np.int64)), side)

    @functools.cached_property
    def _train_samples(self) -> dict[tuple[int, int], np.ndarray]:
        return {}

    def _train_sample(self, repeat: int, fold: int) -> np.ndarray:
        """The default sample of a train side within the budget, drawn on first use."""
        key = (repeat, fold)
        if key not in self._train_samples:
            self._train_samples[key] = _read_only(train_positions(self.container, repeat, fold))
        return self._train_samples[key]

    def X(self, rows: Any = None, *, special: SpecialMode = "drop") -> pd.DataFrame:
        """The model inputs of ``rows`` (positions; default all), with the container's index (the positions).

        The columns are selected before the rows, so the call holds about the result's size in memory.

        Args:
            rows: The positions in ``container.dataset``.
            special: How the special features enter. ``"drop"`` (default) leaves out the columns in
                :attr:`needs_encoding` (a SMILES string, no model input as text) and keeps a spectrum's numeric
                columns; ``"encode"`` replaces every special feature, spectra included, by its recommended encoding
                (``data_foundry.special.encode_special_feature``; RDKit for a SMILES); ``"raw"`` passes every column
                on as stored, for a method that brings its own encoder.
        """
        if special not in ("drop", "encode", "raw"):
            raise ValueError(f"special must be 'drop', 'encode' or 'raw', got {special!r}.")
        dropped = set(self.needs_encoding) if special == "drop" else set()
        x = self._select([c for c in self.features if c not in dropped], rows)
        if special == "encode":
            from data_foundry.special import encode_special_feature  # noqa: PLC0415 - RDKit or scipy by kind

            for feature in self.special_features:
                x = encode_special_feature(x, feature)
        return x

    def y(self, rows: Any = None) -> pd.Series:
        """The target of ``rows``, on the scale it ships, with the container's index: :meth:`score` reads the rows
        from it when it gets no ``rows``.
        """
        column = self.container.dataset[self.target]
        return column if rows is None else column.iloc[np.asarray(rows)]

    def train_weight(self, rows: Any = None) -> np.ndarray | None:
        """The training weight of ``rows`` as floats, or ``None`` for a task that trains unweighted."""
        return self._column(self.sample_weight, rows)

    def validation_weights(self, rows: Any = None) -> np.ndarray | None:
        """The weight of each of ``rows`` in a validation loss (early stopping, tuning, ensembling), or ``None`` when
        every row weighs the same: the metric's row weight, so validation optimises what the test score counts.
        """
        return self._column(self.validation_weight, rows)

    def validation_split(
        self, rows: Any, *, fraction: float = 0.2, random_state: int | None = None
    ) -> tuple[np.ndarray, np.ndarray]:
        """The default inner validation split of ``rows`` (a fold's training rows), cut by :attr:`split_roles`.

        A harness may use it for early stopping and tuning, or cut its own by the same roles:

        * temporal: the newest rows (about ``fraction`` of them, whole time values) are held out; the fit side keeps
          the rows before the start of the hold-out minus the gap (``split_roles.gap``), so the gap of the outer
          splits recurs inside. Rows without a time are on neither side.
        * grouped or with a unit weight: whole groups and whole units on one side, drawn at random until the
          validation side holds about ``fraction`` of the rows.
        * iid: rows at random.

        In every regime a row that shares a group or a unit with a validation row stays out of the fit side.

        Args:
            rows: The positions in ``container.dataset`` to split.
            fraction: The share of ``rows`` to hold out, between 0 and 1.
            random_state: The seed of the draw; default the container's ``split_random_state`` (or Data Foundry's
                split seed). A temporal hold-out draws nothing.

        Returns:
            ``(fit, validation)``: sorted positions in ``container.dataset``, both subsets of ``rows``.

        Raises:
            ValueError: ``fraction`` is outside (0, 1), or ``rows`` cannot be cut into two non-empty sides (a single
                time value, a single group).
        """
        if not 0 < fraction < 1:
            raise ValueError(f"fraction must be between 0 and 1, got {fraction!r}.")
        rows = np.unique(np.asarray(rows, dtype=np.int64))
        roles = self.split_roles
        frame = self.container.dataset
        together = [list(c) for c in (roles.group, (roles.unit,) if roles.unit else ()) if c]
        if self.regime == "temporal" and roles.time is not None:
            fit, val = self._temporal_holdout(frame[roles.time].iloc[rows], fraction)
        else:
            seed = getattr(self.container.experiment_metadata, "split_random_state", None)
            seed = random_state if random_state is not None else (seed if seed is not None else SPLIT_RANDOM_STATE)
            codes = _codes(frame, together[0], rows) if together else np.arange(len(rows))
            val = _draw_keys(codes, fraction, np.random.default_rng(seed))
            fit = ~val
        for columns in together:  # a group or unit with rows on both sides keeps them on the validation side only
            codes = _codes(frame, columns, rows)
            fit &= ~np.isin(codes, codes[val])
        if not fit.any() or not val.any():
            raise ValueError(
                f"{len(rows)} rows give no inner validation split by {roles}: one side would be empty "
                "(a single time value or group, or a gap as long as the rows)."
            )
        return rows[fit], rows[val]

    def _temporal_holdout(self, times: pd.Series, fraction: float) -> tuple[np.ndarray, np.ndarray]:
        """Masks of the fit side and of the newest ``fraction`` of the rows, the gap left out between them."""
        known = times.notna().to_numpy()
        ordered = np.sort(times[known].to_numpy())
        if len(ordered) < 2:  # two rows make two sides
            return np.zeros(len(times), dtype=bool), known
        start = ordered[min(len(ordered) - 1, max(1, int(np.floor(len(ordered) * (1 - fraction)))))]
        val = known & (times >= start).to_numpy()
        fit = known & (times < self._gap_end(times, ordered, start)).to_numpy()
        return fit, val

    def _gap_end(self, times: pd.Series, ordered: np.ndarray, start: Any) -> Any:
        """The first time the fit side may not hold: the start of the hold-out moved back by the gap."""
        roles = self.split_roles
        if roles.gap is None:
            return start
        if roles.gap_unit == "steps":  # distinct time values
            distinct = pd.unique(ordered)
            position = int(np.searchsorted(distinct, start)) - int(roles.gap)
            return distinct[max(position, 0)]
        if pd.api.types.is_datetime64_any_dtype(times):
            stamp = pd.Timestamp(start)
            if roles.gap_unit in ("months", "years"):
                months = roles.gap * (12 if roles.gap_unit == "years" else 1)
                if float(months).is_integer():
                    return stamp - pd.DateOffset(months=int(months))
                return stamp - pd.Timedelta(days=months * 365.25 / 12)
            return stamp - pd.Timedelta(roles.gap, unit=roles.gap_unit)
        if self.time_unit is None or roles.gap_unit not in STEPS_PER_YEAR:
            raise ValueError(
                f"a gap of {roles.gap} {roles.gap_unit} on the numeric time column {roles.time!r} needs its "
                "calendar (task_metadata.time_unit)."
            )
        return start - roles.gap * STEPS_PER_YEAR[self.time_unit] / STEPS_PER_YEAR[roles.gap_unit]

    def _select(self, columns: list[str], rows: Any) -> pd.DataFrame:
        """``columns`` of ``rows``: the columns first, then the rows, so only the result is copied. The result is a
        frame of its own: writing to it changes nothing in the container and raises no ``SettingWithCopyWarning``.
        """
        frame = self.container.dataset
        if rows is None:
            return frame.reindex(columns=columns)
        with _copy_on_write():  # the column selection stays a view until the rows are taken
            return frame[columns].iloc[np.asarray(rows)]

    def _column(self, column: str | None, rows: Any) -> np.ndarray | None:
        if column is None:
            return None
        values = self.container.dataset[column]
        return (values if rows is None else values.iloc[np.asarray(rows)]).to_numpy(dtype=float)

    # --- scoring ------------------------------------------------------------------------------------------------

    @functools.cached_property
    def _scorer(self) -> Callable[..., float]:
        return scorer(self.container, metric=self.metric)

    def score(self, y_true: Any, y_pred: Any, rows: Any = None) -> float:
        """The metric of ``y_pred`` on the scored rows (:func:`data_foundry.metrics.scorer`).

        Args:
            y_true: The target of the scored rows, on the shipped scale (:meth:`y`).
            y_pred: Probabilities in the order of :attr:`classes` (or a DataFrame whose columns are the class names),
                labels, or values on the shipped scale, as the metric's ``prediction`` says.
            rows: The positions of the scored rows. Needed by a metric with inputs (a group, a weight) and by a task
                scored per group; without it a pandas ``y_true`` gives them by its index (:meth:`y` keeps it).

        Returns:
            The score; NaN where the metric is undefined on these rows (one class for an AUC).
        """
        return self._scorer(y_true, y_pred, rows)

    def error(self, score: float) -> float:
        """The score as an error: lower is better, 0 at the metric's :attr:`optimum` (``optimum - score`` when higher
        is better, ``score - optimum`` otherwise).

        Raises:
            ValueError: The metric has no fixed optimum, so a distance to one would measure nothing
                (``BENCHMARK_CHANGES_TODO.md``, decision B).
        """
        if self.optimum is None:
            raise ValueError(
                f"metric {self.metric.name!r} has no fixed optimum: its best value changes with the scored rows, so "
                "an error optimum - score is not defined. Rank its scores directly, or normalize the metric first "
                "(open decision B of the benchmark hand-off)."
            )
        return float(self.optimum - score) if self.greater_is_better else float(score - self.optimum)

    # --- export -------------------------------------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """The derived facts as JSON-able data (what ``benchmark_task.json`` holds); no rows, no splits.

        ``data_foundry_version`` records the release that wrote them; :func:`task_view_mismatch` compares a saved copy
        with a fresh one.
        """
        budget = self.row_budget
        return {
            "task_view_version": TASK_VIEW_VERSION,
            "data_foundry_version": data_foundry_version(),
            "name": self.name,
            "format_version": self.format_version,
            "target": self.target,
            "problem_type": self.problem_type,
            "classes": None if self.classes is None else [_plain(c) for c in self.classes],
            "features": list(self.features),
            "needs_encoding": list(self.needs_encoding),
            "regime": self.regime,
            "split_columns": list(self.split_columns),
            "split_roles": self.split_roles.to_dict(),
            "special_features": [_dump(f) for f in self.special_features],
            "metric": _dump(self.metric),
            "greater_is_better": self.greater_is_better,
            "optimum": self.optimum,
            "grouping": None if self.grouping is None else _dump(self.grouping),
            "sample_weight": self.sample_weight,
            "validation_weight": self.validation_weight,
            "unit_column": self.unit_column,
            "row_budget": None if budget is None else _dump(budget),
            "time_unit": self.time_unit,
        }


def _classes(target: pd.Series, problem_type: str) -> tuple[Any, ...] | None:
    """The sorted classes of a classification target: its categories, or its values when it is not categorical."""
    if problem_type == "regression":
        return None
    if isinstance(target.dtype, pd.CategoricalDtype):
        return tuple(sorted(target.cat.categories))
    return tuple(sorted(target.dropna().unique()))


def _format_1_spec(task: Any) -> MetricSpec:
    """A format-1 task's metric name as a spec: the registry's kind, prediction and direction."""
    name = task.objective_metric_name
    if name not in METRICS:
        raise ValueError(f"format-1 metric {name!r} is not in the metric registry (data_foundry.metrics.METRICS).")
    definition = METRICS[name]
    default = FALLBACK_METRICS.get(task.problem_type) == name
    return MetricSpec(
        name=name,
        kind=definition.kind,
        prediction=definition.prediction,
        greater_is_better=definition.greater_is_better,
        origin="fallback" if default else "context",
        reason="Container format 1 stores the metric's name only (BeyondArena: the default of the problem type).",
        definition=definition.definition,
    )


def task_view_mismatch(saved: dict[str, Any], task: BenchmarkTask) -> list[str]:
    """The keys where a saved ``benchmark_task.json`` differs from ``task.to_dict()`` (``data_foundry_version`` aside:
    a new release that derives the same facts leaves the file valid). Empty when the file is current.
    """
    fresh = task.to_dict()
    keys = (set(saved) | set(fresh)) - {"data_foundry_version"}
    return sorted(k for k in keys if saved.get(k, _MISSING) != fresh.get(k, _MISSING))


_MISSING = object()


def _read_only(array: np.ndarray) -> np.ndarray:
    """A read-only view of ``array``, so a caller cannot change positions the task hands out again (the array itself,
    which may be the container's, stays as it is).
    """
    view = array.view()
    view.flags.writeable = False
    return view


@contextlib.contextmanager
def _copy_on_write() -> Iterator[None]:
    """Run with pandas copy-on-write (always on in pandas 3), so a column selection copies nothing until it is used."""
    if _PANDAS_3:
        yield
        return
    with pd.option_context("mode.copy_on_write", True):  # noqa: FBT003 - pandas option API
        yield


def _codes(frame: pd.DataFrame, columns: list[str], rows: np.ndarray) -> np.ndarray:
    """One integer per row of ``rows`` that names its value of ``columns`` (missing values form a value too)."""
    if len(columns) == 1:
        return pd.factorize(frame[columns[0]].iloc[rows], use_na_sentinel=False)[0]
    with _copy_on_write():
        part = frame[columns].iloc[rows]
    return part.groupby(columns, dropna=False, sort=False, observed=True).ngroup().to_numpy()


def _draw_keys(codes: np.ndarray, fraction: float, rng: np.random.Generator) -> np.ndarray:
    """A mask of the rows of whole keys, drawn in random order until they hold about ``fraction`` of the rows."""
    counts = np.bincount(codes)
    order = rng.permutation(len(counts))
    reached = np.cumsum(counts[order]) >= fraction * len(codes)
    n_kept = min(int(np.argmax(reached)) + 1, len(counts) - 1) if len(counts) > 1 else 0
    return np.isin(codes, order[:n_kept])


def _dump(obj: Any) -> Any:
    """A pydantic dataclass as JSON-able data."""
    return TypeAdapter(type(obj)).dump_python(obj, mode="json")


def _plain(value: Any) -> Any:
    """A class label as a JSON value (a numpy scalar as its Python value)."""
    return value.item() if isinstance(value, np.generic) else value


__all__ = [
    "BENCHMARK_TASK_FILE",
    "TASK_VIEW_VERSION",
    "BenchmarkTask",
    "Fold",
    "Regime",
    "SpecialMode",
    "SplitRoles",
    "data_foundry_version",
    "task_view_mismatch",
]
