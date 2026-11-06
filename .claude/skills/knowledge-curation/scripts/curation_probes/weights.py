"""The task's training weight and its own metric in the probes, shared by the probe modules.

Tooling-independent (NumPy, pandas and scikit-learn). A task may train with a weight: a rate's realized denominator,
such as the years insured of a claims-per-year target, which the metric also weights the rows by. The probes then
fit every model with it as each row's weight (``fit``; a model that takes no weight, such as kNN, is fitted without
it), take the weighted dummy (``reference``: the weighted mean, ``sum(w * y) / sum(w)``, or the weighted class
shares) and weight their scores (R^2, RMSE, ROC AUC, log loss) by the test rows' weights. Without a weight nothing
changes.

The task's own metric is passed as a dict, ``metric``:

* ``name``, ``greater_is_better``;
* ``prediction``: what ``score`` takes, ``proba``, ``label`` or ``value``;
* ``score``: ``score(y_true, y_pred, rows) -> float``, the true values (as the target ships) and the prediction of the
  rows ``rows`` (positions into the probe's frame): class probabilities as a DataFrame whose columns are the classes,
  the predicted classes, or the values on the target's shipped scale. It computes the metric as the benchmark does,
  the per-group aggregation and the metric's input columns (a weight, an era) included;
* optional: ``floor``, the smallest prediction the metric scores (``min_prediction``, on the shipped scale);
  ``gini``, whether it is a Gini (probe 22 then scores 1/weight alone); ``row_weight``, the column it weights the
  rows by; ``params``, the metric's parameters (a Tweedie deviance's ``power``).

``declared_score`` scores a probe's prediction by it and ``at_floor`` gives the share of predictions at or below its
floor.
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.utils.validation import has_fit_parameter


def take(weight: np.ndarray | None, rows: np.ndarray) -> np.ndarray | None:
    """``weight[rows]``, or None without a weight."""
    return None if weight is None else weight[rows]


def fit(model: Any, X: pd.DataFrame, y: np.ndarray, weight: np.ndarray | None = None) -> Any:
    """Fit ``model`` with ``weight`` as each row's weight; a pipeline passes it to its last step. Without a weight, or
    for a model that takes none (kNN), the fit is unweighted.
    """
    final = model.steps[-1][1] if isinstance(model, Pipeline) else model
    if weight is None or not has_fit_parameter(final, "sample_weight"):
        return model.fit(X, y)
    if isinstance(model, Pipeline):
        return model.fit(X, y, **{f"{model.steps[-1][0]}__sample_weight": weight})
    return model.fit(X, y, sample_weight=weight)


def reference(y: np.ndarray, rows: np.ndarray, n_classes: int, weight: np.ndarray | None = None) -> np.ndarray:
    """The dummy's prediction from the rows ``rows`` of ``y``: the mean (``n_classes=0``) or the class shares as one
    row, both weighted by ``weight`` (aligned with ``y``) when given.
    """
    w = take(weight, rows)
    if not n_classes:
        return np.array([np.average(y[rows], weights=w)])
    counts = np.bincount(y[rows], weights=w, minlength=n_classes)
    return (counts / counts.sum())[None, :]


def declared_prediction(pred: np.ndarray, classes: Any, prediction: str) -> Any:
    """A probe's prediction (class probabilities with a column per entry of ``classes``, or values) in the kind the
    metric takes: a DataFrame named by the classes (``proba``), the most likely class (``label``) or the values.
    """
    if prediction == "value":
        return np.asarray(pred, dtype=float)
    if prediction == "label":
        return np.asarray(classes)[np.argmax(pred, axis=1)]
    return pd.DataFrame(np.asarray(pred, dtype=float), columns=list(classes))


def declared_score(
    metric: dict, y_true: np.ndarray, pred: np.ndarray, rows: np.ndarray, classes: Any = ()
) -> tuple[float, str | None]:
    """The task's metric of a probe's prediction on ``rows``, and None; or NaN and the error, when it fails (a fold
    the metric cannot score is a finding, not a crash).
    """
    try:
        value = metric["score"](y_true, declared_prediction(pred, classes, metric["prediction"]), rows)
    except (ValueError, TypeError, KeyError, ZeroDivisionError) as error:
        return float("nan"), f"{type(error).__name__}: {error}"
    return float(value), None


def at_floor(pred: np.ndarray, floor: float | None) -> float | None:
    """The share of the predictions at or below ``floor`` (the metric's ``min_prediction``), or None without one."""
    if floor is None:
        return None
    return float(np.mean(np.asarray(pred, dtype=float) <= floor))
