"""The scores the probes share: ROC AUC, R^2, skill against the dummy, the training weight and the declared metric.

* ``auc``: ROC AUC of class probabilities; for more than two classes, the mean one-vs-rest ROC AUC over the classes
  present (a grouped or temporal fold can lack a class); NaN when one class only is present.
* ``auc_or_r2``: ``auc``, or R^2 for a regression; ``skill``: the same as a skill against the prior (``2 AUC - 1``,
  ``1 - MSE / MSE(mean)``).
* ``scores``: the task probe's scores of a prediction (ROC AUC, macro ROC AUC and log loss, or R^2 and RMSE) and its
  skill against the dummy's constant prediction.

A task may train with a weight: a rate's realized denominator, such as the years insured of a claims-per-year target,
which the metric also weights the rows by. The probes then fit every model with it as each row's weight
(``models.fit``), take the weighted dummy (``reference``: the weighted mean, ``sum(w * y) / sum(w)``, or the weighted
class shares) and weight their scores by the test rows' weights. Without a weight nothing changes.

The task's own metric (``ProbeInput.declared_metric()``) is passed as a dict, ``metric``:

* ``name``, ``greater_is_better``;
* ``prediction``: what ``score`` takes, ``proba``, ``label`` or ``value``;
* ``score``: ``score(y_true, y_pred, rows) -> float``, the true values (as the target ships) and the prediction of the
  rows ``rows`` (positions into the probe's frame): class probabilities as a DataFrame whose columns are the classes,
  the predicted classes, or the values on the target's shipped scale. It computes the metric as the benchmark does,
  the per-group aggregation and the metric's input columns (a weight, an era) included;
* optional: ``floor``, the smallest prediction the metric scores (``min_prediction``, on the shipped scale);
  ``gini``, whether it is a Gini (probe 22 then scores 1/weight alone, else a fit of the target on the weight);
  ``row_weight``, the column it weights the rows by; ``params``, the metric's parameters (a Tweedie deviance's
  ``power``); ``transform``, the ``target_transform`` the target ships under.

``declared_score`` scores a probe's prediction by it and ``at_floor`` gives the share of predictions at or below its
floor.
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import log_loss, r2_score, roc_auc_score


def take(weight: np.ndarray | None, rows: np.ndarray) -> np.ndarray | None:
    """``weight[rows]``, or None without a weight."""
    return None if weight is None else weight[rows]


def auc(y_true: np.ndarray, proba: np.ndarray, classes: Any, weight: np.ndarray | None = None) -> float:
    """ROC AUC of ``proba`` (one column per entry of ``classes``); for more than two classes, the mean one-vs-rest
    ROC AUC over the classes present in ``y_true``. NaN when ``y_true`` holds one class only. ``weight``: each row's
    weight, or None.
    """
    present = [k for k, c in enumerate(classes) if np.any(y_true == c)]
    if len(present) < 2:
        return float("nan")
    if len(classes) == 2:  # binary
        return float(roc_auc_score(y_true == classes[1], proba[:, 1], sample_weight=weight))
    return float(np.mean([roc_auc_score(y_true == classes[k], proba[:, k], sample_weight=weight) for k in present]))


def auc_or_r2(y: np.ndarray, pred: np.ndarray, n_classes: int, weight: np.ndarray | None = None) -> float:
    """``auc`` of class probabilities for labels coded ``0 .. n_classes - 1``, or R^2 of values (``n_classes=0``;
    ``pred`` one column or flat), each row weighted by ``weight`` when given; higher is better.
    """
    if not n_classes:
        return float(r2_score(y, np.asarray(pred).reshape(len(y), -1)[:, 0], sample_weight=weight))
    return auc(y, pred, np.arange(n_classes), weight)


def skill(y: np.ndarray, pred: np.ndarray, n_classes: int) -> float:
    """``2 AUC - 1`` (``auc``), or ``1 - MSE / MSE(mean)`` for regression (``n_classes=0``); unweighted."""
    if n_classes == 0:
        dummy = float(np.mean((y - y.mean()) ** 2))
        return float("nan") if dummy == 0 else 1.0 - float(np.mean((y - pred) ** 2)) / dummy
    return 2.0 * auc(y, pred, np.arange(n_classes)) - 1.0


def scores(
    y: np.ndarray, pred: np.ndarray, reference: np.ndarray, n_classes: int, weight: np.ndarray | None = None
) -> dict[str, float]:
    """The task probe's scores of ``pred`` and its skill against the constant ``reference`` (the dummy's prediction),
    each row weighted by ``weight`` when given: ROC AUC and log loss (binary, skill ``2 AUC - 1``), macro ROC AUC and
    log loss (multiclass, skill ``1 - log loss / dummy log loss``), RMSE and R^2 (regression, skill
    ``1 - MSE / dummy MSE``).
    """
    if not n_classes:
        mse = float(np.average((y - pred) ** 2, weights=weight))
        dummy = float(np.average((y - reference) ** 2, weights=weight))
        total = float(np.average((y - np.average(y, weights=weight)) ** 2, weights=weight))
        return {
            "rmse": mse**0.5,
            "r2": 1 - mse / total if total else float("nan"),
            "skill": 1 - mse / dummy if dummy else float("nan"),
        }
    labels = list(range(n_classes))
    p = np.clip(pred, 1e-12, 1)
    p = np.round(p / p.sum(axis=1, keepdims=True), 12)  # a constant averaged per group stays a constant
    q = np.clip(np.broadcast_to(reference, p.shape), 1e-12, 1)
    q = q / q.sum(axis=1, keepdims=True)
    present = np.unique(y)
    if n_classes == 2:  # binary
        value = float(roc_auc_score(y, p[:, 1], sample_weight=weight)) if len(present) == 2 else float("nan")
        ll = float(log_loss(y, p, labels=labels, sample_weight=weight))
        return {"auc": value, "log_loss": ll, "skill": 2 * value - 1}
    ll = float(log_loss(y, p, labels=labels, sample_weight=weight))
    ll_dummy = float(log_loss(y, q, labels=labels, sample_weight=weight))
    value = float("nan")
    if len(present) > 2:
        sub = p[:, present] / p[:, present].sum(axis=1, keepdims=True)
        value = float(roc_auc_score(y, sub, multi_class="ovr", labels=list(present), sample_weight=weight))
    return {"macro_auc": value, "log_loss": ll, "skill": 1 - ll / ll_dummy if ll_dummy else float("nan")}


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
