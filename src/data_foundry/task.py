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
files without Data Foundry. Like the other consumer modules, this one loads nothing of the build side.
"""

from __future__ import annotations

import functools
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

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
from data_foundry.sampling import subsample_train
from data_foundry.schema import Grouping, MetricSpec, RowBudget, SpecialFeature

if TYPE_CHECKING:
    from data_foundry.curation_container import CuratedContainer

BENCHMARK_TASK_FILE = "benchmark_task.json"
"""The file a format-2 container saves :meth:`BenchmarkTask.to_dict` in, next to its metadata. Derived from the
metadata, so it is not part of the checksum."""

TASK_VIEW_VERSION = 1
"""The version of the layout of :meth:`BenchmarkTask.to_dict`; raised when a key changes meaning or goes away."""


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
    and its group column (if any) as a :class:`~data_foundry.schema.Grouping` with one prediction per row.

    Attributes:
        name: The dataset's ``unique_name``.
        format_version: The container format, 1 or 2.
        target: The target column.
        problem_type: ``binary_classification``, ``multiclass_classification`` or ``regression``.
        classes: The classes in sorted order (scikit-learn's ``classes_``): the column order of ``predict_proba`` the
            scorer reads, also for an ordered target, whose declared order is type information only. ``None`` for a
            regression task. A binary task's positive class is ``classes[1]``.
        features: The model inputs (:func:`~data_foundry.curation_container.feature_columns`): no target, group,
            scoring or unit column, and no time column that dates the label.
        split_columns: The columns an inner validation split reads (group, time, unit;
            :func:`~data_foundry.curation_container.split_columns`), never inputs unless :attr:`features` lists them.
        special_features: The inputs that need an encoding by kind (a SMILES, a spectrum); encode each with
            ``data_foundry.special.encode_special_feature(frame, feature)``.
        metric: The metric spec; format 1 gets its ``objective_metric_name`` as one.
        greater_is_better: Whether a higher score is better.
        optimum: The best score any prediction can reach (1 for ROC AUC, 0 for RMSE), or ``None`` for a metric whose
            best value changes with the scored rows (``net_revenue_at_cost``, ``ordered_lorenz_gini``).
        grouping: How a grouped task is used, or ``None``. ``grouping.prediction_unit == "group"`` means one prediction
            per group; the scorer aggregates row predictions by ``grouping.aggregation``.
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
    split_columns: tuple[str, ...]
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
        return cls(
            container=container,
            name=container.dataset_metadata.unique_name,
            format_version=container.format_version,
            target=task.target_column_name,
            problem_type=task.problem_type,
            classes=_classes(container.dataset[task.target_column_name], task.problem_type),
            features=tuple(feature_columns(container)),
            split_columns=tuple(split_columns(container)),
            special_features=tuple(special_features(container)),
            metric=metric,
            greater_is_better=bool(metric.greater_is_better),
            optimum=metric_optimum(metric),
            grouping=container.grouping if container.format_version >= 2 else _format_1_grouping(task),
            sample_weight=sample_weight(container),
            validation_weight=validation_weight(container),
            unit_column=unit.unit if unit is not None else None,
            row_budget=getattr(container.experiment_metadata, "row_budget", None),
            time_unit=getattr(task, "time_unit", None),
        )

    # --- rows ---------------------------------------------------------------------------------------------------

    def folds(self, *, budget: bool = True) -> Iterator[Fold]:
        """Every outer split as shipped (never re-split or shuffle them: they encode the regime).

        Args:
            budget: Fit on the default sample of the train side within the row budget
                (:func:`~data_foundry.sampling.subsample_train`), the protocol of a ``_1m`` version. ``False`` gives
                the whole train side; a container without a budget gives it either way.
        """
        for repeat, folds in self.container.experiment_metadata.splits.items():
            for fold, (train, test) in folds.items():
                side = np.asarray(train, dtype=np.int64)
                rows = side
                if budget and self.row_budget is not None:
                    rows = np.asarray(subsample_train(self.container, repeat, fold), dtype=np.int64)
                yield Fold(repeat, fold, rows, np.asarray(test, dtype=np.int64), side)

    def X(self, rows: Any = None) -> pd.DataFrame:
        """The model inputs of ``rows`` (positions; default all), with the container's index (the positions)."""
        return self._rows(rows)[list(self.features)]

    def y(self, rows: Any = None) -> pd.Series:
        """The target of ``rows``, on the scale it ships, with the container's index: :meth:`score` reads the rows
        from it when it gets no ``rows``.
        """
        return self._rows(rows)[self.target]

    def train_weight(self, rows: Any = None) -> np.ndarray | None:
        """The training weight of ``rows`` as floats, or ``None`` for a task that trains unweighted."""
        return self._column(self.sample_weight, rows)

    def validation_weights(self, rows: Any = None) -> np.ndarray | None:
        """The weight of each of ``rows`` in a validation loss (early stopping, tuning, ensembling), or ``None`` when
        every row weighs the same: the metric's row weight, so validation optimises what the test score counts.
        """
        return self._column(self.validation_weight, rows)

    def _rows(self, rows: Any) -> pd.DataFrame:
        frame = self.container.dataset
        return frame if rows is None else frame.iloc[np.asarray(rows)]

    def _column(self, column: str | None, rows: Any) -> np.ndarray | None:
        if column is None:
            return None
        return self._rows(rows)[column].to_numpy(dtype=float)

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
        """The derived facts as JSON-able data (what ``benchmark_task.json`` holds); no rows, no splits."""
        budget = self.row_budget
        return {
            "task_view_version": TASK_VIEW_VERSION,
            "name": self.name,
            "format_version": self.format_version,
            "target": self.target,
            "problem_type": self.problem_type,
            "classes": None if self.classes is None else [_plain(c) for c in self.classes],
            "features": list(self.features),
            "split_columns": list(self.split_columns),
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


def _format_1_grouping(task: Any) -> Grouping | None:
    """A format-1 group column as a grouping with one prediction per row (format 1 records no unit or context)."""
    if task.group_on is None:
        return None
    return Grouping(on=task.group_on, labels=task.group_labels or "per_sample", time_on=task.group_time_on)


def _dump(obj: Any) -> Any:
    """A pydantic dataclass as JSON-able data."""
    return TypeAdapter(type(obj)).dump_python(obj, mode="json")


def _plain(value: Any) -> Any:
    """A class label as a JSON value (a numpy scalar as its Python value)."""
    return value.item() if isinstance(value, np.generic) else value


__all__ = ["BENCHMARK_TASK_FILE", "TASK_VIEW_VERSION", "BenchmarkTask", "Fold"]
