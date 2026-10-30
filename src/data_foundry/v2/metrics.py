"""The metrics that score a task, and their reference implementations.

A container of format 2 stores its metric as data, the ``objective_metric`` spec of its task metadata
(:class:`data_foundry.schema.MetricSpec`): a name, its kind, what it takes, its origin, and the params and input
columns it needs. This module holds the registry of names (:data:`METRICS`) and scores a prediction by a spec:

* :class:`Metric`: what a v2 definition declares (``metric = Metric.source("rmse", reference=...)``), turned into a
  spec when the dataset is built (:meth:`Metric.spec`).
* :func:`score`: score ``y_pred`` against ``y_true`` by a spec (a :class:`~data_foundry.schema.MetricSpec`, the plain
  ``dict`` of the JSON file, or a :class:`Metric`).
* :func:`scorer`: a scorer for one container that looks up the scoring columns' values by row index, so a benchmark
  passes only the test indices: ``scorer(container)(y_test, y_pred, test_idx)``.
* :func:`to_sklearn_scorer`: a scikit-learn scorer, for ``cross_val_score`` and the like.

The module depends on numpy, pandas, scikit-learn and scipy only, and imports nothing else from Data Foundry (the
containers it reads are duck-typed), so it can be copied out on its own into code that reads the container files with
plain ``json``. scikit-learn and scipy are imported when a metric is computed, not when the module is imported.

Conventions of the predictions:

* ``proba``: class probabilities. Binary: the probability of the positive class, ``labels[1]``, as a vector (or a
  two-column array in ``labels`` order). Multiclass: one column per class in ``labels`` order. ``labels`` defaults
  to the sorted classes of ``y_true``; :func:`scorer` passes the categories of the container's target column.
* ``label``: predicted classes, in the values of ``y_true``. Binary metrics that need a positive class
  (``f1``, ``precision``, ``recall``) take ``labels[1]``.
* ``value``: a number per row (regression).

The scale of a regression target: a target may ship on the scale a practitioner models it on (``log`` of a price,
``log1p`` of a count) while the task means the original scale. The spec's ``target_transform`` (``identity``, the
default, ``log``, ``log1p`` or ``log10``) says how the target ships transformed for modelling; :func:`score` (and so
:func:`scorer` and :func:`to_sklearn_scorer`) applies the inverse (``exp``, ``expm1``, ``10**``) to both ``y_true``
and ``y_pred`` before the metric, so the metric is computed on the original scale. Predictions are passed on the
shipped scale, as the model makes them. RMSLE of a ``log1p``-shipped target is thus the RMSE of the shipped values,
and the declared metric is always the one on the original scale.

Every implementation is the fastest well-tested one available: scikit-learn or scipy where they cover the metric,
otherwise vectorised numpy; each is tested against the reference implementation (``tests/test_v2_metrics.py``; the
custom metrics against their official code, vendored in ``tests/test_v2_metrics_custom.py``).

The custom metrics (``kind="custom"``): ``cost_matrix``, ``precision_at_k``, ``average_precision_at_k``, ``rmspe``,
``gini_top_capture``, ``weighted_pearsonr``, ``mean_group_pearsonr``, ``hierarchical_balanced_accuracy``,
``mean_absolute_log1p_error``, ``gini_stability``, ``par_k`` and ``normalized_early_detection_utility``. Each
:class:`MetricDef` holds its formula,
its reference, its prediction kind, its input roles and its params. A metric with inputs takes the values of the
scored rows by role: ``group`` (rows of one unit: an era, a patient, an instance), ``order`` (sorts rows in time: a
week, an hour; rows arrive in any order, so no metric relies on row position) and ``weight``. A metric scores the
rows it receives: when a task's prediction unit is a group (the grouping's ``aggregation``, e.g. a customer's last
statement), the caller aggregates the predictions first; :func:`scorer` does not.

TabArena (later, no change there now) would wrap a spec in an AutoGluon scorer::

    from autogluon.core.metrics import make_scorer

    ag_metric = make_scorer(
        spec["name"],
        lambda y_true, y_pred: score(spec, y_true, y_pred),
        optimum=...,  # the metric's best value, e.g. 1 for roc_auc, 0 for rmse
        greater_is_better=spec["greater_is_better"],
        needs_proba=spec["prediction"] == "proba",
        needs_class=spec["prediction"] == "label",
    )

A metric with ``inputs`` (a group or weight column) needs the test rows' values of those columns as well, so it is
scored outside AutoGluon's scorer interface, through :func:`scorer`.
"""

from __future__ import annotations

import dataclasses
import difflib
import math
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Any

import numpy as np
import pandas as pd

PROBLEM_TYPES = ("binary_classification", "multiclass_classification", "regression")

FALLBACK_METRICS: dict[str, str] = {
    "binary_classification": "roc_auc",
    "multiclass_classification": "log_loss",
    "regression": "rmse",
}
"""The metric of :meth:`Metric.fallback` per problem type (TabArena's defaults)."""

ORIGINS = ("source", "stand_in", "context", "fallback")
PREDICTIONS = ("proba", "label", "value")

INVERSE_TRANSFORMS: dict[str, Callable[[np.ndarray], np.ndarray]] = {
    "identity": lambda v: v,
    "log": np.exp,
    "log1p": np.expm1,
    "log10": lambda v: np.power(10.0, v),
}
"""The inverse of each ``target_transform`` a spec may declare: the target ships transformed for modelling, and the
metric is computed after this inverse of both the true values and the predictions."""
TARGET_TRANSFORMS = tuple(INVERSE_TRANSFORMS)


def _sklearn_metrics() -> Any:
    import sklearn.metrics  # noqa: PLC0415 - imported when a metric is computed, not with the module

    return sklearn.metrics


def _scipy_stats() -> Any:
    import scipy.stats  # noqa: PLC0415 - imported when a metric is computed, not with the module

    return scipy.stats


# --- prediction helpers -------------------------------------------------------------------------------------------


def _labels(y_true: np.ndarray, labels: Any) -> list:
    """The class labels in their column order: ``labels`` as given, else the sorted classes of ``y_true``."""
    if labels is not None:
        return list(labels)
    return sorted(pd.unique(pd.Series(np.asarray(y_true)).dropna()))


def _codes(y_true: Any, labels: list) -> np.ndarray:
    """``y_true`` as positions in ``labels``; a class not in ``labels`` is an error."""
    lookup = pd.Index(list(labels))
    if not lookup.is_unique:
        raise ValueError(f"labels must be unique, got {list(labels)}.")
    values = np.asarray(y_true)
    codes = lookup.get_indexer(values)
    if (codes < 0).any():
        bad = values[np.flatnonzero(codes < 0)[0]]
        raise ValueError(f"y_true holds the class {bad!r}, which is not in labels {list(labels)}.")
    return codes.astype(np.int64)


def _positive_proba(y_pred: Any) -> np.ndarray:
    """The probability of the positive class: a vector as is, or the second column of a two-column array."""
    proba = np.asarray(y_pred, dtype=float)
    if proba.ndim == 2:
        if proba.shape[1] != 2:
            raise ValueError(f"a binary metric takes one or two probability columns, got {proba.shape[1]}.")
        return proba[:, 1]
    return proba


def _class_proba(y_pred: Any, n_classes: int) -> np.ndarray:
    proba = np.asarray(y_pred, dtype=float)
    if proba.ndim == 1 and n_classes == 2:
        return np.column_stack([1 - proba, proba])
    if proba.ndim != 2 or proba.shape[1] != n_classes:
        raise ValueError(f"expected one probability column per class ({n_classes}), got shape {proba.shape}.")
    return proba


def _binary_truth(y_true: np.ndarray, labels: Any) -> np.ndarray:
    """``y_true`` as 0/1, with ``labels[1]`` as the positive class."""
    labels = _labels(y_true, labels)
    if len(labels) != 2:
        raise ValueError(f"a binary metric needs two classes, got {len(labels)}: {labels[:10]}.")
    return _codes(y_true, labels)


def _positive_label(y_true: np.ndarray, y_pred: np.ndarray, labels: Any) -> Any:
    if labels is not None:
        return list(labels)[-1]
    classes = sorted(pd.unique(pd.Series(np.concatenate([y_true, y_pred]))))
    return classes[-1]


# --- the standard metrics -----------------------------------------------------------------------------------------


def _roc_auc(y_true, y_pred, *, labels=None, **_):
    return _sklearn_metrics().roc_auc_score(_binary_truth(y_true, labels), _positive_proba(y_pred))


def _average_precision(y_true, y_pred, *, labels=None, **_):
    return _sklearn_metrics().average_precision_score(_binary_truth(y_true, labels), _positive_proba(y_pred))


def _log_loss(y_true, y_pred, *, labels=None, **_):
    labels = _labels(y_true, labels)
    proba = _class_proba(y_pred, len(labels))
    return _sklearn_metrics().log_loss(_codes(y_true, labels), proba, labels=list(range(len(labels))))


def _roc_auc_multiclass(multi_class: str) -> Callable:
    def fn(y_true, y_pred, *, labels=None, **_):
        labels_ = _labels(y_true, labels)
        proba = _class_proba(y_pred, len(labels_))
        return _sklearn_metrics().roc_auc_score(
            _codes(y_true, labels_),
            proba,
            multi_class=multi_class,
            average="macro",
            labels=list(range(len(labels_))),
        )

    return fn


def _label_metric(func_name: str, **kwargs: Any) -> Callable:
    def fn(y_true, y_pred, **_):
        return getattr(_sklearn_metrics(), func_name)(y_true, y_pred, **kwargs)

    return fn


def _positive_label_metric(func_name: str) -> Callable:
    def fn(y_true, y_pred, *, labels=None, **_):
        y_pred = np.asarray(y_pred)
        pos_label = _positive_label(y_true, y_pred, labels)
        return getattr(_sklearn_metrics(), func_name)(y_true, y_pred, pos_label=pos_label, average="binary")

    return fn


def _value_metric(func_name: str) -> Callable:
    def fn(y_true, y_pred, **_):
        return getattr(_sklearn_metrics(), func_name)(np.asarray(y_true, dtype=float), np.asarray(y_pred, dtype=float))

    return fn


def _correlation(func_name: str) -> Callable:
    def fn(y_true, y_pred, **_):
        result = getattr(_scipy_stats(), func_name)(np.asarray(y_true, dtype=float), np.asarray(y_pred, dtype=float))
        return result.statistic

    return fn


@dataclass(frozen=True)
class MetricDef:
    """One metric of the registry: what it takes and how it is computed.

    Attributes:
        name: The registry name (the spec's ``name``).
        problem_types: The problem types it scores.
        prediction: ``proba``, ``label`` or ``value``.
        greater_is_better: Whether a higher score is better.
        fn: ``fn(y_true, y_pred, *, labels=None, params, **inputs) -> float``.
        implementation: The function it calls, for the reader (``sklearn.metrics.roc_auc_score``).
        definition: The metric as a one-line formula.
        kind: ``standard`` (a scikit-learn / scipy function) or ``custom`` (implemented here).
        inputs: The input roles it needs (``group``, ``weight``): columns of the frame passed by role.
        params: The params it takes, each with a short description (the params schema).
        predictions: Other prediction kinds it takes, chosen by ``params["prediction"]``.
        check_params: Raises a ValueError on invalid params (a missing matrix, a bad ``k``).
        reference: Where the metric is defined, and the official implementation it is tested against.
    """

    name: str
    problem_types: tuple[str, ...]
    prediction: str
    greater_is_better: bool
    fn: Callable[..., float]
    implementation: str
    definition: str
    kind: str = "standard"
    inputs: tuple[str, ...] = ()
    params: Mapping[str, str] = field(default_factory=dict)
    predictions: tuple[str, ...] = ()
    check_params: Callable[[Mapping[str, Any]], None] | None = field(default=None, compare=False)
    reference: str | None = None

    def prediction_for(self, params: Mapping[str, Any] | None) -> str:
        """The prediction kind under ``params``: :attr:`prediction`, or ``params["prediction"]`` when the metric
        also takes one of :attr:`predictions` (``cost_matrix`` scores labels, or probabilities by their least
        expected cost).
        """
        chosen = (params or {}).get("prediction", self.prediction)
        allowed = (self.prediction, *self.predictions)
        if chosen not in allowed:
            raise ValueError(f"metric {self.name!r} takes the prediction kind(s) {list(allowed)}, not {chosen!r}.")
        return chosen

    def validate(self, params: Mapping[str, Any] | None) -> None:
        """Raise a ValueError when ``params`` do not fit the metric (unknown names, missing or invalid values)."""
        params = dict(params or {})
        unknown = sorted(set(params) - set(self.params))
        if unknown:
            raise ValueError(f"metric {self.name!r} takes the params {sorted(self.params)}, not {unknown}.")
        self.prediction_for(params)
        if self.check_params is not None:
            self.check_params(params)


def _standard(name, problem_types, prediction, greater_is_better, fn, implementation, definition) -> MetricDef:
    return MetricDef(name, tuple(problem_types), prediction, greater_is_better, fn, implementation, definition)


_BIN = ("binary_classification",)
_MULTI = ("multiclass_classification",)
_CLF = (*_BIN, *_MULTI)
_REG = ("regression",)
_HIGHER, _LOWER = True, False  # greater_is_better

METRICS: dict[str, MetricDef] = {
    d.name: d
    for d in (
        # binary classification
        _standard(
            "roc_auc", _BIN, "proba", _HIGHER, _roc_auc, "sklearn.metrics.roc_auc_score", "area under the ROC curve"
        ),
        _standard(
            "average_precision",
            _BIN,
            "proba",
            _HIGHER,
            _average_precision,
            "sklearn.metrics.average_precision_score",
            "area under the precision-recall curve (step-wise)",
        ),
        _standard(
            "log_loss", _CLF, "proba", _LOWER, _log_loss, "sklearn.metrics.log_loss", "mean of -log p(true class)"
        ),
        _standard(
            "accuracy",
            _CLF,
            "label",
            _HIGHER,
            _label_metric("accuracy_score"),
            "sklearn.metrics.accuracy_score",
            "share of rows with the right class",
        ),
        _standard(
            "balanced_accuracy",
            _CLF,
            "label",
            _HIGHER,
            _label_metric("balanced_accuracy_score"),
            "sklearn.metrics.balanced_accuracy_score",
            "mean of the per-class recalls",
        ),
        _standard(
            "f1",
            _BIN,
            "label",
            _HIGHER,
            _positive_label_metric("f1_score"),
            "sklearn.metrics.f1_score(pos_label=labels[1])",
            "harmonic mean of precision and recall of the positive class",
        ),
        _standard(
            "mcc",
            _CLF,
            "label",
            _HIGHER,
            _label_metric("matthews_corrcoef"),
            "sklearn.metrics.matthews_corrcoef",
            "Matthews correlation coefficient",
        ),
        _standard(
            "precision",
            _BIN,
            "label",
            _HIGHER,
            _positive_label_metric("precision_score"),
            "sklearn.metrics.precision_score(pos_label=labels[1])",
            "TP / (TP + FP) of the positive class",
        ),
        _standard(
            "recall",
            _BIN,
            "label",
            _HIGHER,
            _positive_label_metric("recall_score"),
            "sklearn.metrics.recall_score(pos_label=labels[1])",
            "TP / (TP + FN) of the positive class",
        ),
        # multiclass classification
        _standard(
            "f1_macro",
            _MULTI,
            "label",
            _HIGHER,
            _label_metric("f1_score", average="macro"),
            "sklearn.metrics.f1_score(average='macro')",
            "unweighted mean of the per-class F1",
        ),
        _standard(
            "f1_micro",
            _MULTI,
            "label",
            _HIGHER,
            _label_metric("f1_score", average="micro"),
            "sklearn.metrics.f1_score(average='micro')",
            "F1 of the pooled counts (equals accuracy for single-label data)",
        ),
        _standard(
            "f1_weighted",
            _MULTI,
            "label",
            _HIGHER,
            _label_metric("f1_score", average="weighted"),
            "sklearn.metrics.f1_score(average='weighted')",
            "mean of the per-class F1 weighted by class support",
        ),
        _standard(
            "roc_auc_ovo_macro",
            _MULTI,
            "proba",
            _HIGHER,
            _roc_auc_multiclass("ovo"),
            "sklearn.metrics.roc_auc_score(multi_class='ovo', average='macro')",
            "mean ROC AUC over all pairs of classes",
        ),
        _standard(
            "roc_auc_ovr_macro",
            _MULTI,
            "proba",
            _HIGHER,
            _roc_auc_multiclass("ovr"),
            "sklearn.metrics.roc_auc_score(multi_class='ovr', average='macro')",
            "mean ROC AUC of each class against the rest",
        ),
        # regression
        _standard(
            "mean_poisson_deviance",
            _REG,
            "value",
            _LOWER,
            _value_metric("mean_poisson_deviance"),
            "sklearn.metrics.mean_poisson_deviance",
            "2*mean(y*log(y/p)-y+p); finite y>=0 and p>0; 0*log(0/p)=0",
        ),
        _standard(
            "rmse",
            _REG,
            "value",
            _LOWER,
            _value_metric("root_mean_squared_error"),
            "sklearn.metrics.root_mean_squared_error",
            "sqrt(mean((y - p)^2))",
        ),
        _standard(
            "mae",
            _REG,
            "value",
            _LOWER,
            _value_metric("mean_absolute_error"),
            "sklearn.metrics.mean_absolute_error",
            "mean(|y - p|)",
        ),
        _standard(
            "mse",
            _REG,
            "value",
            _LOWER,
            _value_metric("mean_squared_error"),
            "sklearn.metrics.mean_squared_error",
            "mean((y - p)^2)",
        ),
        _standard(
            "r2", _REG, "value", _HIGHER, _value_metric("r2_score"), "sklearn.metrics.r2_score", "1 - SS_res / SS_tot"
        ),
        _standard(
            "rmsle",
            _REG,
            "value",
            _LOWER,
            _value_metric("root_mean_squared_log_error"),
            "sklearn.metrics.root_mean_squared_log_error",
            "sqrt(mean((log1p(y) - log1p(p))^2)); y and p non-negative",
        ),
        _standard(
            "mape",
            _REG,
            "value",
            _LOWER,
            _value_metric("mean_absolute_percentage_error"),
            "sklearn.metrics.mean_absolute_percentage_error",
            "mean(|y - p| / max(|y|, eps))",
        ),
        _standard(
            "median_absolute_error",
            _REG,
            "value",
            _LOWER,
            _value_metric("median_absolute_error"),
            "sklearn.metrics.median_absolute_error",
            "median(|y - p|)",
        ),
        _standard(
            "pearsonr",
            _REG,
            "value",
            _HIGHER,
            _correlation("pearsonr"),
            "scipy.stats.pearsonr",
            "Pearson correlation of y and p",
        ),
        _standard(
            "spearmanr",
            _REG,
            "value",
            _HIGHER,
            _correlation("spearmanr"),
            "scipy.stats.spearmanr",
            "Spearman rank correlation of y and p",
        ),
    )
}
"""Every metric a spec may name, by name."""


# --- the custom metrics -------------------------------------------------------------------------------------------
#
# Each takes ``fn(y_true, y_pred, *, labels=None, params, **inputs)`` with the inputs by role, as numpy arrays of the
# scored rows in any order: a metric that needs an order sorts by its ``order`` input, never by row position. A metric
# scores the rows it receives; a task whose prediction unit is a group (a customer's last statement, an instance's
# selected algorithm) is aggregated by the caller as the task's grouping declares, except where the metric itself
# defines the per-group step (``par_k``, ``mean_group_pearsonr``, ...). Each is tested against the official or
# reference implementation in ``tests/test_v2_metrics_custom.py``.


def _mean_absolute_log1p_error(y_true, y_pred, **_):
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    # A clipping floor would change the chosen error cost.
    if any(not np.isfinite(v).all() or (v <= -1).any() for v in (y_true, y_pred)):
        raise ValueError("mean_absolute_log1p_error needs finite values greater than -1.")
    return _sklearn_metrics().mean_absolute_error(np.log1p(y_true), np.log1p(y_pred))


def _require(params: Mapping[str, Any], *names: str) -> None:
    missing = [n for n in names if n not in params]
    if missing:
        raise ValueError(f"missing param(s) {missing}.")


def _group_codes(values: Any) -> tuple[np.ndarray, int]:
    """Group ids as codes 0..G-1 (NaN is an error) and the number of groups."""
    codes, uniques = pd.factorize(np.asarray(values), use_na_sentinel=True)
    if (codes < 0).any():
        raise ValueError("a group or order input holds missing values.")
    return codes.astype(np.int64), len(uniques)


def _positive_mask(y: Any, labels: Any, y_true: np.ndarray) -> np.ndarray:
    """Whether each value of ``y`` (true or predicted labels) is the positive class, ``labels[1]``."""
    labels = _labels(y_true, labels)
    if len(labels) != 2:
        raise ValueError(f"a binary metric needs two classes, got {len(labels)}: {labels[:10]}.")
    return np.asarray(y) == labels[1]


def _top_k(params: Mapping[str, Any], n: int) -> int:
    """The cut-off ``k`` for ``n`` scored rows: ``params["k"]``, or ``ceil(k_fraction * n)``; at most ``n``."""
    k = int(params["k"]) if "k" in params else math.ceil(float(params["k_fraction"]) * n - 1e-09)
    return max(1, min(k, n))


def _check_top_k(params: Mapping[str, Any]) -> None:
    if ("k" in params) == ("k_fraction" in params):
        raise ValueError("give exactly one of k (a number of rows) and k_fraction (a share of the scored rows).")
    if "k" in params and not (isinstance(params["k"], int) and params["k"] >= 1):
        raise ValueError(f"k is a positive integer, not {params['k']!r}.")
    if "k_fraction" in params and not 0 < float(params["k_fraction"]) <= 1:
        raise ValueError(f"k_fraction is in (0, 1], not {params['k_fraction']!r}.")


# cost_matrix


def _check_cost_matrix(params: Mapping[str, Any]) -> None:
    _require(params, "labels", "matrix")
    labels, matrix = list(params["labels"]), np.asarray(params["matrix"], dtype=float)
    if len(set(labels)) != len(labels):
        raise ValueError(f"cost_matrix labels must be unique, got {labels}.")
    if matrix.shape != (len(labels), len(labels)):
        raise ValueError(f"cost_matrix matrix must be {len(labels)} x {len(labels)} (labels), got {matrix.shape}.")
    if not np.isfinite(matrix).all():
        raise ValueError("cost_matrix matrix must be finite.")


def _cost_matrix(y_true, y_pred, *, labels=None, params, **_):
    """Mean of ``matrix[true][pred]`` over the rows; from probabilities, ``pred`` is the least expected cost class."""
    cost_labels = list(params["labels"])
    matrix = np.asarray(params["matrix"], dtype=float)
    truth = _codes(y_true, cost_labels)
    if params.get("prediction", "label") == "proba":
        proba_labels = _labels(y_true, labels)
        proba = _class_proba(y_pred, len(proba_labels))
        columns = {label: i for i, label in enumerate(proba_labels)}
        unknown = [label for label in proba_labels if label not in set(cost_labels)]
        if unknown:
            raise ValueError(f"probability columns {unknown} are not in the cost matrix labels {cost_labels}.")
        in_cost_order = np.zeros((len(proba), len(cost_labels)))
        for j, label in enumerate(cost_labels):
            if label in columns:
                in_cost_order[:, j] = proba[:, columns[label]]
        predicted = np.argmin(in_cost_order @ matrix, axis=1)  # expected cost of predicting each class; ties: first
    else:
        predicted = _codes(y_pred, cost_labels)
    return float(matrix[truth, predicted].mean())


# precision_at_k / average_precision_at_k


def _precision_at_k(y_true, y_pred, *, labels=None, params, **_):
    """Share of positives among the ``k`` highest scores; rows tied at the cut-off count by their expected share."""
    positive = _binary_truth(np.asarray(y_true), labels).astype(float)
    scores = _positive_proba(y_pred)
    k = _top_k(params, len(scores))
    cut = np.partition(scores, len(scores) - k)[len(scores) - k]  # the k-th highest score
    above = scores > cut
    tied = scores == cut
    slots = k - int(above.sum())
    hits = positive[above].sum() + slots * positive[tied].mean()
    return float(hits / k)


def _average_precision_at_k(y_true, y_pred, *, labels=None, params, **_):
    """AP@k: sum over ranks i <= k of precision@i * rel_i, over min(k, #positives); ties keep the row order."""
    positive = _binary_truth(np.asarray(y_true), labels).astype(float)
    scores = _positive_proba(y_pred)
    k = _top_k(params, len(scores))
    n_positive = positive.sum()
    if n_positive == 0:
        return 0.0
    cut = np.partition(scores, len(scores) - k)[len(scores) - k]  # the k-th highest score
    candidates = np.flatnonzero(scores >= cut)  # the top k and the rows tied at the cut-off, in row order
    order = candidates[np.argsort(-scores[candidates], kind="stable")[:k]]
    rel = positive[order]
    precision = np.cumsum(rel) / np.arange(1, k + 1)
    return float((precision * rel).sum() / min(k, n_positive))


# rmspe


def _rmspe(y_true, y_pred, **_):
    """sqrt(mean(((y - p) / y)^2)) over the rows with y != 0."""
    y = np.asarray(y_true, dtype=float)
    p = np.asarray(y_pred, dtype=float)
    keep = y != 0
    if not keep.any():
        return float("nan")
    return float(np.sqrt(np.mean(((y[keep] - p[keep]) / y[keep]) ** 2)))


# gini_top_capture: the AmEx default-prediction metric


def _check_gini_top_capture(params: Mapping[str, Any]) -> None:
    if not 0 < float(params.get("top_fraction", 0.04)) <= 1:
        raise ValueError("top_fraction is in (0, 1].")
    if float(params.get("negative_weight", 20)) <= 0:
        raise ValueError("negative_weight is positive.")


def _weighted_gini_sorted(target: np.ndarray, weight: np.ndarray) -> float:
    """The AmEx weighted Gini of rows already sorted by descending score."""
    random = np.cumsum(weight / weight.sum())
    weighted_target = target * weight
    lorentz = np.cumsum(weighted_target) / weighted_target.sum()
    return float(((lorentz - random) * weight).sum())


def _gini_top_capture(y_true, y_pred, *, labels=None, params, **_):
    """0.5 * (normalized weighted Gini + share of positives in the top ``top_fraction`` of the weight)."""
    top_fraction = float(params.get("top_fraction", 0.04))
    negative_weight = float(params.get("negative_weight", 20))
    positive = _binary_truth(np.asarray(y_true), labels).astype(float)
    scores = _positive_proba(y_pred)
    target = positive[np.argsort(-scores, kind="stable")]
    weight = np.where(target == 0, negative_weight, 1.0)
    cutoff = int(top_fraction * weight.sum())
    captured = target[np.cumsum(weight) <= cutoff].sum() / target.sum()
    perfect = np.sort(positive)[::-1]
    gini = _weighted_gini_sorted(target, weight)
    gini_max = _weighted_gini_sorted(perfect, np.where(perfect == 0, negative_weight, 1.0))
    return float(0.5 * (gini / gini_max + captured))


# weighted_pearsonr


def _check_weights(params: Mapping[str, Any]) -> None:
    weights = params.get("weights")
    if weights is not None:
        if not isinstance(weights, Mapping) or not weights:
            raise ValueError("weights maps each value of the weight column to its weight: {'Bitcoin': 6.78, ...}.")
        if not all(isinstance(w, (int, float)) and w >= 0 for w in weights.values()):
            raise ValueError("weights are non-negative numbers.")


def _row_weights(weight: Any, params: Mapping[str, Any]) -> np.ndarray:
    mapping = params.get("weights")
    if mapping is None:
        return np.asarray(weight, dtype=float)
    mapped = pd.Series(np.asarray(weight)).astype(object).map(dict(mapping))
    if mapped.isna().any():
        missing = sorted({str(v) for v in pd.Series(np.asarray(weight))[mapped.isna().to_numpy()]})[:10]
        raise ValueError(f"weight column values {missing} have no entry in params['weights'].")
    return mapped.to_numpy(dtype=float)


def _weighted_pearsonr(y_true, y_pred, *, weight, params, **_):
    """Pearson correlation of y and p with the rows weighted by ``weight`` (or ``params['weights'][weight]``)."""
    w = _row_weights(weight, params)
    y = np.asarray(y_true, dtype=float)
    p = np.asarray(y_pred, dtype=float)
    sum_w = w.sum()
    dy = y - (w * y).sum() / sum_w
    dp = p - (w * p).sum() / sum_w
    cov = (w * dy * dp).sum()
    return float(cov / np.sqrt((w * dy * dy).sum() * (w * dp * dp).sum()))


# mean_group_pearsonr


def _group_center(values: np.ndarray, codes: np.ndarray, n_groups: int) -> np.ndarray:
    means = np.bincount(codes, weights=values, minlength=n_groups) / np.bincount(codes, minlength=n_groups)
    return values - means[codes]


def _signed_power(values: np.ndarray, power: float) -> np.ndarray:
    return np.sign(values) * np.abs(values) ** power


def _check_group_corr(params: Mapping[str, Any]) -> None:
    if params.get("method", "pearson") not in ("pearson", "numerai_corr"):
        raise ValueError(f"method is 'pearson' or 'numerai_corr', not {params.get('method')!r}.")


def _mean_group_pearsonr(y_true, y_pred, *, group, params, **_):
    """Mean over groups of the per-group Pearson correlation; ``method="numerai_corr"`` first transforms as Numerai's
    CORR (predictions: per-group rank, gaussianized, signed power 1.5; target: per-group centred, signed power 1.5).
    Groups whose correlation is undefined (one row, or no variance) are left out of the mean.
    """
    codes, n_groups = _group_codes(group)
    y = np.asarray(y_true, dtype=float)
    p = np.asarray(y_pred, dtype=float)
    if params.get("method", "pearson") == "numerai_corr":
        from scipy.special import ndtri  # noqa: PLC0415 - imported when a metric is computed, not with the module

        frame = pd.DataFrame({"g": codes, "p": p})
        ranks = frame.groupby("g", sort=False)["p"].rank(method="average").to_numpy()
        counts = np.bincount(codes, minlength=n_groups)[codes]
        p = _signed_power(ndtri((ranks - 0.5) / counts), 1.5)
        y = _signed_power(_group_center(y, codes, n_groups), 1.5)
    dy = _group_center(y, codes, n_groups)
    dp = _group_center(p, codes, n_groups)
    cov = np.bincount(codes, weights=dy * dp, minlength=n_groups)
    var = np.bincount(codes, weights=dy * dy, minlength=n_groups) * np.bincount(
        codes, weights=dp * dp, minlength=n_groups
    )
    with np.errstate(invalid="ignore", divide="ignore"):
        corr = cov / np.sqrt(var)
    corr = corr[var > 0]
    return float(corr.mean()) if len(corr) else float("nan")


# hierarchical_balanced_accuracy


def _hierarchical_balanced_accuracy(y_true, y_pred, *, group, **_):
    """Accuracy per group (fine level, e.g. strain), averaged over the groups of each true class (coarse level, e.g.
    species), then averaged over the classes present.
    """
    truth = np.asarray(y_true)
    correct = (truth == np.asarray(y_pred)).astype(float)
    class_codes, _ = _group_codes(truth)
    group_codes, _ = _group_codes(group)
    pair_codes, pairs = pd.factorize(pd.MultiIndex.from_arrays([class_codes, group_codes]))
    n_pairs = len(pairs)
    per_group = np.bincount(pair_codes, weights=correct, minlength=n_pairs) / np.bincount(pair_codes, minlength=n_pairs)
    pair_class = pairs.get_level_values(0).to_numpy()
    per_class = pd.Series(per_group).groupby(pair_class).mean()
    return float(per_class.mean())


# gini_stability (Home Credit 2024)


def _rank_auc_per_group(positive: np.ndarray, scores: np.ndarray, codes: np.ndarray, n_groups: int) -> np.ndarray:
    """ROC AUC per group by the rank-sum (Mann-Whitney) formula, ties at half; NaN for a group with one class."""
    ranks = pd.DataFrame({"g": codes, "s": scores}).groupby("g", sort=False)["s"].rank(method="average").to_numpy()
    n_pos = np.bincount(codes, weights=positive, minlength=n_groups)
    n_all = np.bincount(codes, minlength=n_groups)
    n_neg = n_all - n_pos
    rank_sum = np.bincount(codes, weights=ranks * positive, minlength=n_groups)
    with np.errstate(invalid="ignore", divide="ignore"):
        return (rank_sum - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg)


def _gini_stability(y_true, y_pred, *, labels=None, params, order, **_):
    """Per period (sorted ``order`` value) gini = 2 AUC - 1; a least-squares line over the period index (0, 1, ...);
    mean(gini) + slope_weight * min(0, slope) - residual_std_weight * std(residuals). Periods with one class are
    left out (the official code fails on them).
    """
    positive = _binary_truth(np.asarray(y_true), labels).astype(float)
    scores = _positive_proba(y_pred)
    codes, uniques = pd.factorize(np.asarray(order), sort=True)
    if (codes < 0).any():
        raise ValueError("the order input holds missing values.")
    gini = 2 * _rank_auc_per_group(positive, scores, codes, len(uniques)) - 1
    gini = gini[np.isfinite(gini)]
    if len(gini) < 2:
        return float("nan")
    x = np.arange(len(gini))
    slope, intercept = np.polyfit(x, gini, 1)
    residuals = gini - (slope * x + intercept)
    return float(
        np.mean(gini)
        + float(params.get("slope_weight", 88.0)) * min(0.0, slope)
        - float(params.get("residual_std_weight", 0.5)) * np.std(residuals)
    )


# par_k


def _check_par_k(params: Mapping[str, Any]) -> None:
    _require(params, "cutoff")
    if float(params["cutoff"]) <= 0:
        raise ValueError("cutoff is a positive runtime.")
    if float(params.get("k", 10)) <= 0:
        raise ValueError("k is positive.")


def _par_k(y_true, y_pred, *, group, params, **_):
    """Per group (instance) select the row (algorithm) with the lowest prediction, ties to the first row; its true
    runtime counts as is, or as ``k * cutoff`` when it timed out (runtime >= cutoff * (1 - rel_tol)); mean over groups.
    """
    cutoff = float(params["cutoff"])
    k = float(params.get("k", 10))
    rel_tol = float(params.get("timeout_rel_tol", 1e-9))
    runtime = np.asarray(y_true, dtype=float)  # on the original scale: score() inverts the spec's target_transform
    penalized = np.where(runtime >= cutoff * (1 - rel_tol), k * cutoff, runtime)
    codes, _ = _group_codes(group)
    predicted = np.asarray(y_pred, dtype=float)
    rows = np.lexsort((np.arange(len(codes)), predicted, codes))  # by group, then prediction, then row
    first = np.ones(len(rows), dtype=bool)
    first[1:] = codes[rows][1:] != codes[rows][:-1]
    return float(penalized[rows[first]].mean())


# normalized_early_detection_utility (PhysioNet/CinC 2019)

_UTILITY_DEFAULTS = {
    "dt_early": -12.0,
    "dt_optimal": -6.0,
    "dt_late": 3.0,
    "max_u_tp": 1.0,
    "min_u_fn": -2.0,
    "u_fp": -0.05,
    "u_tn": 0.0,
}


def _check_utility(params: Mapping[str, Any]) -> None:
    p = {**_UTILITY_DEFAULTS, **{k: v for k, v in params.items() if k in _UTILITY_DEFAULTS}}
    if not p["dt_early"] < p["dt_optimal"] < p["dt_late"]:
        raise ValueError("dt_early < dt_optimal < dt_late.")
    if "threshold" in params and params.get("prediction", "label") != "proba":
        raise ValueError("threshold applies to prediction='proba' only.")


def _row_utility(predicted: np.ndarray, septic: np.ndarray, dt: np.ndarray, p: Mapping[str, float]) -> np.ndarray:
    """The official per-hour utility (``compute_prediction_utility``), vectorised; ``dt = t - t_sepsis``."""
    m_1 = float(p["max_u_tp"]) / float(p["dt_optimal"] - p["dt_early"])
    b_1 = -m_1 * p["dt_early"]
    m_2 = float(-p["max_u_tp"]) / float(p["dt_late"] - p["dt_optimal"])
    b_2 = -m_2 * p["dt_late"]
    m_3 = float(p["min_u_fn"]) / float(p["dt_late"] - p["dt_optimal"])
    b_3 = -m_3 * p["dt_optimal"]
    early = dt <= p["dt_optimal"]
    in_window = dt <= p["dt_late"]
    tp = np.where(early, np.maximum(m_1 * dt + b_1, p["u_fp"]), m_2 * dt + b_2)
    fn = np.where(early, 0.0, m_3 * dt + b_3)
    septic_u = np.where(in_window, np.where(predicted, tp, fn), 0.0)
    return np.where(septic, septic_u, np.where(predicted, p["u_fp"], p["u_tn"]))


def _normalized_early_detection_utility(y_true, y_pred, *, labels=None, params, group, order, **_):
    """PhysioNet/CinC 2019 normalized utility: (U - U_no_alarm) / (U_best - U_no_alarm), summed over the hours of
    all groups (patients). Hours are each patient's rows sorted by ``order``; ``t`` is the position in that order and
    the onset is ``t_sepsis = first positive position - dt_optimal``, as in the official code.
    """
    p = {**_UTILITY_DEFAULTS, **{k: float(v) for k, v in params.items() if k in _UTILITY_DEFAULTS}}
    y_true = np.asarray(y_true)
    truth = _positive_mask(y_true, labels, y_true)
    if params.get("prediction", "label") == "proba":
        predicted = _positive_proba(y_pred) >= float(params.get("threshold", 0.5))
    else:
        predicted = _positive_mask(y_pred, labels, y_true)
    codes, n_groups = _group_codes(group)
    rows = np.lexsort((np.arange(len(codes)), np.asarray(order), codes))
    codes, truth, predicted = codes[rows], truth[rows], predicted[rows]
    starts = np.flatnonzero(np.r_[True, codes[1:] != codes[:-1]])
    position = np.arange(len(codes)) - np.repeat(starts, np.diff(np.r_[starts, len(codes)]))
    first_positive = np.full(n_groups, -1, dtype=np.int64)
    positive_groups, first_index = np.unique(codes[truth], return_index=True)
    first_positive[positive_groups] = position[truth][first_index]
    septic = first_positive[codes] >= 0
    dt = position - (first_positive[codes] - p["dt_optimal"])
    observed = _row_utility(predicted, septic, dt, p).sum()
    best = _row_utility(septic & (dt >= p["dt_early"]) & (dt <= p["dt_late"]), septic, dt, p).sum()
    inaction = _row_utility(np.zeros(len(codes), dtype=bool), septic, dt, p).sum()
    with np.errstate(invalid="ignore", divide="ignore"):
        return float((observed - inaction) / (best - inaction))


def _custom(name, problem_types, prediction, greater_is_better, fn, definition, reference, **extra) -> MetricDef:
    return MetricDef(
        name=name,
        problem_types=tuple(problem_types),
        prediction=prediction,
        greater_is_better=greater_is_better,
        fn=fn,
        implementation=f"data_foundry.v2.metrics.{fn.__name__}",
        definition=definition,
        kind="custom",
        reference=reference,
        **extra,
    )


_TOP_K_PARAMS = {
    "k": "the cut-off as a number of rows (give k or k_fraction)",
    "k_fraction": "the cut-off as a share of the scored rows, k = ceil(k_fraction * n)",
}

_CUSTOM_METRICS = (
    _custom(
        "mean_absolute_log1p_error",
        _REG,
        "value",
        _LOWER,
        _mean_absolute_log1p_error,
        "mean(|log1p(y) - log1p(p)|); finite y and p greater than -1, without clipping",
        "numpy.log1p followed by sklearn.metrics.mean_absolute_error; context-selected CPS88 prediction loss",
    ),
    _custom(
        "cost_matrix",
        _CLF,
        "label",
        _LOWER,
        _cost_matrix,
        "mean over rows of matrix[true][pred] (lower is better; a source that reports -mean or the total cost is a "
        "sign or a scale away)",
        "FORCE 2020 score(): https://github.com/bolgebrygg/Force-2020-Machine-Learning-competition (starter notebook); "
        "Statlog German credit cost matrix; IDA 2016 APS challenge",
        params={
            "labels": "the classes in the order of the matrix rows and columns",
            "matrix": "matrix[i][j]: the cost of predicting labels[j] for a row of class labels[i]",
            "prediction": "'label' (default): hard predictions; 'proba': probabilities, each row predicted as the "
            "class of least expected cost, argmin_j sum_i p_i matrix[i][j]",
        },
        predictions=("proba",),
        check_params=_check_cost_matrix,
    ),
    _custom(
        "precision_at_k",
        _BIN,
        "proba",
        _HIGHER,
        _precision_at_k,
        "share of positives among the k highest-scored rows; rows tied at the cut-off count by their expected share",
        "CoIL Challenge 2000 (https://kdd.ics.uci.edu/databases/tic/tic.task.html); Flogard & Mengshoel 2022",
        params=_TOP_K_PARAMS,
        check_params=_check_top_k,
    ),
    _custom(
        "average_precision_at_k",
        _BIN,
        "proba",
        _HIGHER,
        _average_precision_at_k,
        "sum_{i<=k} precision@i * rel_i / min(k, #positives) over the rows by descending score (ties: row order); 0 "
        "without positives",
        "AP@K, https://www.kaggle.com/competitions/avito-prohibited-content/overview/evaluation",
        params=_TOP_K_PARAMS,
        check_params=_check_top_k,
    ),
    _custom(
        "rmspe",
        _REG,
        "value",
        _LOWER,
        _rmspe,
        "sqrt(mean(((y - p) / y)^2)) over the rows with y != 0",
        "https://www.kaggle.com/competitions/rossmann-store-sales/overview/evaluation",
    ),
    _custom(
        "gini_top_capture",
        _BIN,
        "proba",
        _HIGHER,
        _gini_top_capture,
        "0.5 * (normalized weighted Gini + share of the positives in the top top_fraction of the total weight), "
        "negatives weighted negative_weight (AmEx: 0.04 and 20)",
        "https://www.kaggle.com/code/inversion/amex-competition-metric-python",
        params={
            "top_fraction": "the share of the total weight that counts as the top (default 0.04)",
            "negative_weight": "the weight of a negative row, a positive weighs 1 (default 20)",
        },
        check_params=_check_gini_top_capture,
    ),
    _custom(
        "weighted_pearsonr",
        _REG,
        "value",
        _HIGHER,
        _weighted_pearsonr,
        "sum w (y - ybar_w)(p - pbar_w) / sqrt(sum w (y - ybar_w)^2 * sum w (p - pbar_w)^2)",
        "https://www.kaggle.com/competitions/g-research-crypto-forecasting/overview/evaluation",
        inputs=("weight",),
        params={
            "weights": "optional {value: weight}: the weight input holds a key per row (an asset), mapped to its "
            "weight; without it the weight input holds the weights"
        },
        check_params=_check_weights,
    ),
    _custom(
        "mean_group_pearsonr",
        _REG,
        "value",
        _HIGHER,
        _mean_group_pearsonr,
        "mean over groups of the Pearson correlation within the group; method='numerai_corr' transforms first as "
        "Numerai's CORR",
        "https://docs.numer.ai/numerai-tournament/scoring/correlation-corr; numerai_tools.scoring.numerai_corr",
        inputs=("group",),
        params={
            "method": "'pearson' (default) or 'numerai_corr': per group, predictions ranked (average ties, "
            "(rank - 0.5) / n), gaussianized and raised to the signed power 1.5; the target centred and raised to the "
            "signed power 1.5"
        },
        check_params=_check_group_corr,
    ),
    _custom(
        "hierarchical_balanced_accuracy",
        _CLF,
        "label",
        _HIGHER,
        _hierarchical_balanced_accuracy,
        "mean over true classes of the mean over the class's groups of the group's accuracy",
        "Vervier et al. 2015, arXiv:1506.07251",
        inputs=("group",),
    ),
    _custom(
        "gini_stability",
        _BIN,
        "proba",
        _HIGHER,
        _gini_stability,
        "per period gini = 2 AUC - 1; fit gini = a * index + b; mean(gini) + 88 * min(0, a) - 0.5 * std(residuals)",
        "https://www.kaggle.com/competitions/home-credit-credit-risk-model-stability/overview/evaluation "
        "(gini_stability in the hosts' starter notebook, jetakow/home-credit-2024-starter-notebook)",
        inputs=("order",),
        params={
            "slope_weight": "the weight of min(0, slope) (default 88.0)",
            "residual_std_weight": "the weight subtracted per unit of the residuals' std (default 0.5)",
        },
    ),
    _custom(
        "par_k",
        _REG,
        "value",
        _LOWER,
        _par_k,
        "mean over groups of the true runtime of the row with the lowest prediction, a timeout counted as k * cutoff",
        "Bischl et al. 2016, ASlib (PAR10); llama::parscores (https://cran.r-project.org/package=llama)",
        inputs=("group",),
        params={
            "cutoff": "the runtime limit; a true runtime >= cutoff * (1 - timeout_rel_tol) is a timeout",
            "k": "the penalty factor of a timeout (default 10)",
            "timeout_rel_tol": "relative tolerance of the timeout test (default 1e-9)",
        },
        check_params=_check_par_k,
    ),
    _custom(
        "normalized_early_detection_utility",
        _BIN,
        "label",
        _HIGHER,
        _normalized_early_detection_utility,
        "PhysioNet 2019 utility per patient-hour by its time to onset, summed and normalized as (U - U_no_alarm) / "
        "(U_best - U_no_alarm)",
        "https://github.com/physionetchallenges/evaluation-2019/blob/master/evaluate_sepsis_score.py",
        inputs=("group", "order"),
        params={
            **{
                name: f"the official utility parameter (default {value:g})" for name, value in _UTILITY_DEFAULTS.items()
            },
            "prediction": "'label' (default): hard predictions; 'proba': probabilities, positive at >= threshold",
            "threshold": "the probability at which a 'proba' prediction raises an alarm (default 0.5)",
        },
        predictions=("proba",),
        check_params=_check_utility,
    ),
)
METRICS.update({d.name: d for d in _CUSTOM_METRICS})


def known_metrics() -> dict[str, set[str]]:
    """The metric names per problem type, from :data:`METRICS`."""
    return {p: {name for name, d in METRICS.items() if p in d.problem_types} for p in PROBLEM_TYPES}


def _unknown_name_message(name: str) -> str:
    close = difflib.get_close_matches(str(name).lower(), METRICS, n=3)
    hint = f" Did you mean {', '.join(close)}?" if close else ""
    return (
        f"unknown metric {name!r}.{hint} A custom metric is added to data_foundry.v2.metrics under a general name; "
        f"the known names are {sorted(METRICS)}."
    )


# --- what a definition declares -----------------------------------------------------------------------------------


@dataclass(frozen=True)
class Metric:
    """The metric a v2 definition declares (``metric = Metric.source(...)``), built into the container's spec.

    Use a constructor:

    * :meth:`source`: the metric the source scored (the competition's evaluation page, the paper, the task
      description).
    * :meth:`stand_in`: the closest computable metric to an original that cannot be computed.
    * :meth:`from_context`: the source defines no metric, but the task makes one obvious (a relative error for a
      price).
    * :meth:`fallback`: the source defines no metric the task would use in practice, and none is obvious; roc_auc /
      log_loss / rmse by problem type.
    * :meth:`local`: code only the definition holds, for a user's own dataset that is never shipped (refused by
      ``build`` unless ``allow_local_metric=True``).
    """

    name: str | None
    origin: str
    original: str | None = None
    reference: str | None = None
    definition: str | None = None
    reason: str | None = None
    params: Mapping[str, Any] = field(default_factory=dict)
    inputs: Mapping[str, str] = field(default_factory=dict)
    fn: Callable[..., float] | None = field(default=None, compare=False)
    prediction: str | None = None
    greater_is_better: bool | None = None
    target_transform: str = "identity"
    """Regression only: the target ships transformed for modelling (``log``, ``log1p``, ``log10``); the metric is
    computed after the inverse of both the true values and the predictions, on the original scale."""

    def __post_init__(self) -> None:
        if self.origin not in ORIGINS:
            raise ValueError(f"Metric origin is one of {ORIGINS}, not {self.origin!r}.")
        if self.target_transform not in INVERSE_TRANSFORMS:
            raise ValueError(f"target_transform is one of {TARGET_TRANSFORMS}, not {self.target_transform!r}.")
        if self.target_transform != "identity":
            prediction = self.prediction
            if self.fn is None and self.name is not None and self.name in METRICS:
                prediction = METRICS[self.name].prediction_for(self.params)
            if prediction is not None and prediction != "value":
                raise ValueError(
                    f"target_transform={self.target_transform!r} is for a regression metric, not {self.name!r} "
                    f"(it takes {prediction!r})."
                )
        if self.fn is None and self.name is not None:
            if self.name not in METRICS:
                raise ValueError(_unknown_name_message(self.name))
            METRICS[self.name].validate(self.params)
        if not isinstance(self.inputs, Mapping) or not all(isinstance(c, str) for c in self.inputs.values()):
            raise ValueError("Metric inputs map each role to a column name: {'group': 'era'}.")

    # --- constructors ---
    @classmethod
    def source(
        cls,
        name: str,
        *,
        original: str | None = None,
        reference: str | None = None,
        params: Mapping[str, Any] | None = None,
        inputs: Mapping[str, str] | None = None,
        definition: str | None = None,
        target_transform: str = "identity",
    ) -> Metric:
        """The metric the source scored, under its registry name; ``reference`` links where the source defines it.

        ``target_transform``: the scale the target ships on for modelling (regression); the metric is computed after
        its inverse, on the original scale.
        """
        return cls(
            name=name,
            origin="source",
            original=original,
            reference=reference,
            definition=definition,
            params=dict(params or {}),
            inputs=dict(inputs or {}),
            target_transform=target_transform,
        )

    @classmethod
    def stand_in(
        cls,
        name: str,
        *,
        original: str,
        reason: str,
        reference: str | None = None,
        params: Mapping[str, Any] | None = None,
        inputs: Mapping[str, str] | None = None,
        definition: str | None = None,
        target_transform: str = "identity",
    ) -> Metric:
        """The closest computable metric to ``original``, which cannot be computed (``reason`` says why)."""
        return cls(
            name=name,
            origin="stand_in",
            original=original,
            reason=reason,
            reference=reference,
            definition=definition,
            params=dict(params or {}),
            inputs=dict(inputs or {}),
            target_transform=target_transform,
        )

    @classmethod
    def from_context(
        cls,
        name: str,
        *,
        reason: str,
        params: Mapping[str, Any] | None = None,
        inputs: Mapping[str, str] | None = None,
        definition: str | None = None,
        target_transform: str = "identity",
    ) -> Metric:
        """No metric defined by the source, but the task makes ``name`` the obvious one (``reason`` says why, e.g.
        "a price's error matters relative to the price"). Used instead of the fallback only when the context is clear.
        ``target_transform``: the scale the target ships on (e.g. ``log`` of a price scored by RMSLE on the price).
        """
        return cls(
            name=name,
            origin="context",
            reason=reason,
            definition=definition,
            params=dict(params or {}),
            inputs=dict(inputs or {}),
            target_transform=target_transform,
        )

    @classmethod
    def fallback(cls, *, reason: str, target_transform: str = "identity") -> Metric:
        """No metric defined by the source (``reason``: where we looked); roc_auc / log_loss / rmse at build.

        ``target_transform`` (regression only) makes the fallback rmse the RMSE on the original scale, after the
        inverse; a log target whose relative error is the obvious goal declares :meth:`from_context` ``rmsle``
        instead.
        """
        return cls(name=None, origin="fallback", reason=reason, target_transform=target_transform)

    @classmethod
    def local(  # noqa: PLR0913 - the spec's fields, all keyword-only
        cls,
        fn: Callable[..., float],
        *,
        name: str,
        prediction: str,
        greater_is_better: bool,
        origin: str = "source",
        original: str | None = None,
        reference: str | None = None,
        definition: str | None = None,
        reason: str | None = None,
        params: Mapping[str, Any] | None = None,
        inputs: Mapping[str, str] | None = None,
        target_transform: str = "identity",
    ) -> Metric:
        """A metric whose code only the definition holds: ``fn(y_true, y_pred, *, labels=None, params, **inputs)``.

        For a user's own dataset that is never shipped. The container's spec says ``kind: "local"``, so a reader
        of the files cannot compute it; ``dataset check`` warns and ``build`` refuses it unless asked
        (``build(allow_local_metric=True)``). A shipped dataset adds its custom metric to :data:`METRICS` instead.
        """
        if prediction not in PREDICTIONS:
            raise ValueError(f"prediction is one of {PREDICTIONS}, not {prediction!r}.")
        if not callable(fn):
            raise ValueError("Metric.local takes the metric function first.")
        return cls(
            name=name,
            origin=origin,
            original=original,
            reference=reference,
            definition=definition,
            reason=reason,
            params=dict(params or {}),
            inputs=dict(inputs or {}),
            fn=fn,
            prediction=prediction,
            greater_is_better=bool(greater_is_better),
            target_transform=target_transform,
        )

    # --- resolution ---
    @property
    def is_local(self) -> bool:
        """Whether the metric's code is only in the definition."""
        return self.fn is not None

    def resolve(self, problem_type: str) -> Metric:
        """The metric with its name set: a fallback takes the problem type's default."""
        if self.name is not None:
            return self
        if problem_type not in FALLBACK_METRICS:
            raise ValueError(f"unknown problem type {problem_type!r}.")
        return dataclasses.replace(self, name=FALLBACK_METRICS[problem_type])

    def spec(self, problem_type: str) -> dict[str, Any]:
        """The fields of the container's spec (:class:`data_foundry.schema.MetricSpec`) for ``problem_type``."""
        resolved = self.resolve(problem_type)
        if resolved.target_transform != "identity" and problem_type != "regression":
            raise ValueError(
                f"target_transform={resolved.target_transform!r} is for a regression target, not {problem_type}."
            )
        if resolved.fn is not None:
            kind, prediction, greater_is_better = "local", resolved.prediction, resolved.greater_is_better
        else:
            definition = METRICS[resolved.name]
            kind, greater_is_better = definition.kind, definition.greater_is_better
            prediction = definition.prediction_for(resolved.params)
        return {
            "name": resolved.name,
            "kind": kind,
            "prediction": prediction,
            "greater_is_better": greater_is_better,
            "origin": resolved.origin,
            "params": dict(resolved.params),
            "inputs": dict(resolved.inputs),
            "original": resolved.original,
            "reference": resolved.reference,
            "definition": resolved.definition or (METRICS[resolved.name].definition if resolved.fn is None else None),
            "reason": resolved.reason,
            "target_transform": resolved.target_transform,
        }


# --- scoring ------------------------------------------------------------------------------------------------------


def _as_dict(spec: Any) -> dict[str, Any]:
    """A spec as a plain dict: a MetricSpec (a dataclass), a dict from the JSON file, or a resolved :class:`Metric`."""
    if isinstance(spec, Mapping):
        return dict(spec)
    if isinstance(spec, Metric):
        if spec.name is None:
            raise ValueError("a fallback Metric has no name before it is resolved: use metric.resolve(problem_type).")
        out = {f.name: getattr(spec, f.name) for f in dataclasses.fields(spec)}
        if spec.fn is None:
            definition = METRICS[spec.name]
            out |= {
                "kind": definition.kind,
                "prediction": definition.prediction_for(spec.params),
                "greater_is_better": definition.greater_is_better,
            }
        else:
            out |= {"kind": "local"}
        return out
    if dataclasses.is_dataclass(spec):
        return {f.name: getattr(spec, f.name) for f in dataclasses.fields(spec)}
    raise TypeError(f"not a metric spec: {type(spec).__name__}.")


def metric_fn(spec: Any) -> Callable[..., float]:
    """The function that computes ``spec``: the registry's, or the code of a local :class:`Metric`."""
    if isinstance(spec, Metric) and spec.fn is not None:
        return spec.fn
    fields = _as_dict(spec)
    if fields.get("kind") == "local":
        raise ValueError(
            f"metric {fields['name']!r} is local: its code is only in the dataset's definition, not in the container."
        )
    if fields["name"] not in METRICS:
        raise ValueError(_unknown_name_message(fields["name"]))
    return METRICS[fields["name"]].fn


def score(spec: Any, y_true: Any, y_pred: Any, *, labels: Any = None, **inputs: Any) -> float:
    """Score ``y_pred`` against ``y_true`` by ``spec``.

    Args:
        spec: A :class:`~data_foundry.schema.MetricSpec`, the ``objective_metric`` dict of the JSON file, or a
            :class:`Metric` (resolved, or local).
        y_true: The true values of the scored rows, on the scale the target ships on.
        y_pred: The predictions (see the module docstring for the ``proba`` / ``label`` / ``value`` conventions), on
            the shipped scale; a spec's ``target_transform`` is inverted on both before the metric.
        labels: The class labels in the order of the probability columns (classification); default the sorted
            classes of ``y_true``.
        **inputs: The values of the spec's input columns for the scored rows, by role (``group=...``).

    Returns:
        The score as a float.
    """
    fields = _as_dict(spec)
    fn = metric_fn(spec)
    needed = METRICS[fields["name"]].inputs if fields.get("kind") != "local" else tuple(fields.get("inputs") or {})
    missing = [role for role in needed if role not in inputs]
    if missing:
        raise ValueError(f"metric {fields['name']!r} needs the input(s) {missing} (pass them by role).")
    y_true = np.asarray(y_true)
    transform = fields.get("target_transform") or "identity"
    if transform == "log1p" and fn is _mean_absolute_log1p_error:
        # Cancel log1p(expm1(z)) before overflow or rounding a very negative inverse to -1.
        return float(_sklearn_metrics().mean_absolute_error(y_true, y_pred))
    if transform != "identity":  # the target ships transformed for modelling: score on the original scale
        if transform not in INVERSE_TRANSFORMS:
            raise ValueError(f"target_transform is one of {TARGET_TRANSFORMS}, not {transform!r}.")
        inverse = INVERSE_TRANSFORMS[transform]
        y_true = inverse(y_true.astype(float))
        y_pred = inverse(np.asarray(y_pred, dtype=float))
    values = {role: np.asarray(v) for role, v in inputs.items()}
    return float(fn(y_true, y_pred, labels=labels, params=dict(fields.get("params") or {}), **values))


def scorer(container: Any, *, metric: Any = None) -> Callable[..., float]:
    """A scorer for one container: ``score(y_true, y_pred, row_index=None, labels=None)``.

    ``row_index`` are the positions of the scored rows in ``container.dataset`` (the test side of a split, as in
    ``experiment_metadata.splits``); the scorer takes the values of the spec's input columns from those rows, so a
    benchmark passes only the test indices. It is needed when the metric has inputs. ``labels`` defaults to the
    categories of the target column, the column order of the probabilities. Values are passed on the shipped scale:
    a per-group aggregation works on it, and :func:`score` then inverts the spec's ``target_transform``.

    Args:
        container: A format-2 container (anything with ``dataset`` and ``task_metadata.objective_metric``).
        metric: Score by this spec or :class:`Metric` instead of the container's (e.g. a local metric).
    """
    task = container.task_metadata
    spec = metric if metric is not None else task.objective_metric
    fields = _as_dict(spec)
    frame = container.dataset
    target = frame[task.target_column_name] if frame is not None else None
    default_labels = None
    if target is not None and isinstance(target.dtype, pd.CategoricalDtype):
        default_labels = list(target.cat.categories)
    input_columns = dict(fields.get("inputs") or {})
    grouping = getattr(task, "grouping", None)
    per_group = grouping is not None and getattr(grouping, "prediction_unit", "row") == "group"

    def score_rows(
        y_true: Any, y_pred: Any, row_index: Any = None, *, labels: Any = None, aggregate: bool = True
    ) -> float:
        y_true, y_pred = np.asarray(y_true), np.asarray(y_pred)
        rows = None if row_index is None else np.asarray(row_index)
        if per_group and aggregate:
            if rows is None:
                raise ValueError("the task predicts one value per group: pass the rows' row_index to aggregate them.")
            y_true, y_pred, rows = _aggregate(frame, grouping, y_true, y_pred, rows)
        values = {}
        if input_columns:
            if rows is None:
                raise ValueError(f"metric {fields['name']!r} uses {input_columns}: pass the rows' row_index.")
            values = {role: frame[column].iloc[rows].to_numpy() for role, column in input_columns.items()}
        return score(spec, y_true, y_pred, labels=labels if labels is not None else default_labels, **values)

    return score_rows


def _aggregate(frame: pd.DataFrame, grouping: Any, y_true: np.ndarray, y_pred: np.ndarray, rows: np.ndarray) -> tuple:
    """One prediction per group, as the task's grouping says (``prediction_unit="group"``).

    ``mean`` averages the rows' predictions (probabilities column by column) and keeps the group's one label; ``any``
    takes the maximum; ``last`` keeps the row latest in ``grouping.time_on``; ``select_min`` / ``select_max`` keep the
    row with the lowest / highest prediction and score that row's true value. Returns the group-level ``y_true``,
    ``y_pred`` and the representative row of each group (whose input columns the metric then reads).
    """
    on = [grouping.on] if isinstance(grouping.on, str) else list(grouping.on)
    keys = (
        frame[on].iloc[rows].astype(str).agg("\x1f".join, axis=1).to_numpy()
        if len(on) > 1
        else (frame[on[0]].iloc[rows].astype(str).to_numpy())
    )
    codes, _ = pd.factorize(keys)
    how = grouping.aggregation
    score_1d = y_pred if y_pred.ndim == 1 else y_pred[:, -1]
    order = np.arange(len(rows))
    if how == "last":
        order = np.lexsort((frame[grouping.time_on].iloc[rows].to_numpy(), codes))
        pick = order[np.r_[codes[order][1:] != codes[order][:-1], True]]
    elif how in ("select_min", "select_max"):
        sign = 1.0 if how == "select_min" else -1.0
        order = np.lexsort((sign * score_1d, codes))
        pick = order[np.r_[True, codes[order][1:] != codes[order][:-1]]]
    else:
        pick = np.unique(codes, return_index=True)[1]  # the group's first row: its label and its inputs
    pick = pick[np.argsort(codes[pick])]
    if how in ("mean", "any"):
        n = codes.max() + 1
        reduce = np.add if how == "mean" else np.maximum
        cols = y_pred.reshape(len(rows), -1).astype(float)
        out = np.full((n, cols.shape[1]), 0.0 if how == "mean" else -np.inf)
        for j in range(cols.shape[1]):
            reduce.at(out[:, j], codes, cols[:, j])
        if how == "mean":
            out /= np.bincount(codes, minlength=n)[:, None]
        pred = out[:, 0] if y_pred.ndim == 1 else out
        true = y_true[pick] if how == "mean" else pd.Series(y_true).groupby(codes).max().to_numpy()
        return true, pred, rows[pick]
    return y_true[pick], y_pred[pick], rows[pick]


def to_sklearn_scorer(spec: Any, *, labels: Any = None) -> Callable[..., float]:
    """A scikit-learn scorer (``make_scorer``) for a metric without inputs.

    scikit-learn hands a binary ``predict_proba`` scorer the positive class's column (``classes_[1]``) and a
    multiclass one every column in ``classes_`` order (sorted), the defaults here; pass ``labels`` otherwise.
    """
    fields = _as_dict(spec)
    if fields.get("inputs"):
        raise ValueError(f"metric {fields['name']!r} has inputs {fields['inputs']}: use scorer(container).")

    def fn(y_true: Any, y_pred: Any) -> float:
        return score(spec, y_true, y_pred, labels=labels)

    response_method = {"proba": "predict_proba", "label": "predict", "value": "predict"}[fields["prediction"]]
    return _sklearn_metrics().make_scorer(
        fn, greater_is_better=bool(fields["greater_is_better"]), response_method=response_method
    )


def dummy_prediction(prediction: str, y_train: Any, n: int, *, labels: Any = None, seed: int = 0) -> np.ndarray:
    """A random prediction for ``n`` rows that matches the kind: draws of the training values (``label`` /
    ``value``) or random probabilities over ``labels`` (``proba``; a vector for two classes). Used to check that a
    metric computes on every split; not a baseline.
    """
    rng = np.random.default_rng(seed)
    y_train = np.asarray(y_train)
    if prediction == "proba":
        labels = _labels(y_train, labels)
        proba = rng.dirichlet(np.ones(len(labels)), size=n)
        return proba[:, 1] if len(labels) == 2 else proba
    if prediction in ("label", "value"):
        return rng.choice(y_train, size=n, replace=True)
    raise ValueError(f"prediction is one of {PREDICTIONS}, not {prediction!r}.")


def is_finite(value: float) -> bool:
    """Whether a score is a finite number."""
    return isinstance(value, (int, float)) and math.isfinite(value)
