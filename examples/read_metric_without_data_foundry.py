"""Read a container's metric with plain ``json`` and pandas, and score a dummy prediction with scikit-learn.

A container is a folder of plain files, so code that does not install Data Foundry can still benchmark on it. This
script imports nothing from ``data_foundry``. It:

1. reads ``task_metadata.*.json``: the metric spec ``objective_metric`` in container format 2 (name, kind, prediction,
   origin, original, reference, definition, params, inputs, target_transform), or the bare ``objective_metric_name``
   in format 1 (BeyondArena);
2. lists the scoring columns (format 2: ``scoring_columns``), the columns the metric needs, which are never features;
3. takes the features as every column but the target, the group column(s) and the scoring columns;
4. scores a dummy prediction on the test side of the first split with the scikit-learn function of a standard
   metric. A custom metric (``kind: "custom"``) is implemented from its ``definition`` and ``params``, or by copying
   ``src/data_foundry/v2/metrics.py`` (numpy, pandas, scikit-learn and scipy only) into your code. A regression
   target may ship on a modelling scale (``target_transform``: ``log``, ``log1p``, ``log10``); the metric is
   computed after the inverse of both the true values and the predictions.

Run::

    # Default: the toy container shipped in this repository.
    python examples/read_metric_without_data_foundry.py

    # Any container folder (the one holding dataset.parquet and the *.json files).
    python examples/read_metric_without_data_foundry.py ~/.cache/data_foundry/<collection>/<name>/<uuid>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn import metrics

TOY_CONTAINER = Path(__file__).resolve().parents[1] / "src" / "data_foundry" / "examples" / "toy_container"

# The standard names of the spec, as scikit-learn functions of (y_true, y_pred).
STANDARD = {
    "roc_auc": metrics.roc_auc_score,
    "average_precision": metrics.average_precision_score,
    "log_loss": metrics.log_loss,
    "accuracy": metrics.accuracy_score,
    "balanced_accuracy": metrics.balanced_accuracy_score,
    "f1_macro": lambda y, p: metrics.f1_score(y, p, average="macro"),
    "f1_weighted": lambda y, p: metrics.f1_score(y, p, average="weighted"),
    "mcc": metrics.matthews_corrcoef,
    "rmse": lambda y, p: metrics.mean_squared_error(y, p) ** 0.5,
    "mae": metrics.mean_absolute_error,
    "mse": metrics.mean_squared_error,
    "r2": metrics.r2_score,
    "rmsle": lambda y, p: metrics.mean_squared_log_error(y, p) ** 0.5,
}

# The inverse of the spec's ``target_transform``: the target ships on that scale, the metric is on the original one.
INVERSE = {"identity": lambda v: v, "log": np.exp, "log1p": np.expm1, "log10": lambda v: np.power(10.0, v)}


def find_container(path: Path) -> Path:
    """The container folder at or below ``path`` (the folder with a ``task_metadata.*.json``)."""
    found = sorted(p.parent for p in path.rglob("task_metadata.*.json"))
    if not found:
        raise SystemExit(f"no task_metadata.*.json under {path}")
    return found[0]


def read_json(folder: Path, prefix: str) -> dict:
    """The one ``<prefix>.<type id>.json`` file of the container."""
    (file,) = folder.glob(f"{prefix}.*.json")
    return json.loads(file.read_text())


def metric_spec(task: dict) -> dict:
    """The metric spec: format 2's ``objective_metric``, or format 1's name as a spec without the extra fields."""
    if "objective_metric" in task:
        return task["objective_metric"]
    name = task["objective_metric_name"]
    prediction = "proba" if name in ("roc_auc", "log_loss") else "value"
    return {"name": name, "kind": "standard", "prediction": prediction, "origin": None, "params": {}, "inputs": {}}


def group_columns(task: dict) -> list[str]:
    """The group column(s): format 2 keeps them in ``grouping.on``, format 1 in ``group_on``."""
    on = (task.get("grouping") or {}).get("on") or task.get("group_on")
    if on is None:
        return []
    return [on] if isinstance(on, str) else list(on)


def dummy_prediction(prediction: str, y_train: pd.Series, n: int, classes: list) -> np.ndarray:
    """A random prediction of the kind the metric takes (not a baseline)."""
    rng = np.random.default_rng(0)
    if prediction == "proba":
        proba = rng.dirichlet(np.ones(len(classes)), size=n)
        return proba[:, 1] if len(classes) == 2 else proba  # binary: the probability of classes[1]
    return rng.choice(y_train.to_numpy(), size=n)  # a label or a value drawn from the training side


def main(path: Path) -> float | None:
    """Print the spec and the scoring columns, then score a dummy prediction; return the score (None if custom)."""
    folder = find_container(path)
    task = read_json(folder, "task_metadata")
    splits = read_json(folder, "experiment_metadata")["splits"]
    df = pd.read_parquet(folder / "dataset.parquet")

    spec = metric_spec(task)
    print(f"Container: {folder}")
    print(f"Target: {task['target_column_name']} ({task['problem_type']})")
    print("Metric spec:")
    for key in ("name", "kind", "prediction", "greater_is_better", "origin", "original", "reference", "definition"):
        if spec.get(key) is not None:
            print(f"  {key}: {spec[key]}")
    for key in ("params", "inputs", "reason", "target_transform"):
        if spec.get(key):
            print(f"  {key}: {spec[key]}")

    scoring = task.get("scoring_columns") or []
    print("Scoring columns (never features):" if scoring else "Scoring columns: none")
    for column in scoring:
        print(f"  {column['column']}: role {column['role']}, used by {column['used_by']}: {column['description']}")

    target = task["target_column_name"]
    not_features = {target, *group_columns(task), *(c["column"] for c in scoring)}
    features = [c for c in df.columns if c not in not_features]
    print(f"Features: {len(features)} of {df.shape[1]} columns")

    # The first split, as shipped: never re-split or shuffle.
    train_idx, test_idx = next(iter(next(iter(splits.values())).values()))
    y_train, y_test = df[target].iloc[train_idx], df[target].iloc[test_idx]
    # The class order of the probabilities: the target's categories (as saved), else the sorted classes.
    classes = []
    if task["problem_type"] != "regression":
        y = df[target]
        classes = list(y.cat.categories) if isinstance(y.dtype, pd.CategoricalDtype) else sorted(y.unique())
    y_pred = dummy_prediction(spec["prediction"], y_train, len(test_idx), classes)

    if spec.get("kind") != "standard" or spec["name"] not in STANDARD:
        print(
            f"`{spec['name']}` is a {spec.get('kind')} metric: implement it from its definition and params, or copy "
            "src/data_foundry/v2/metrics.py; its inputs are the test rows' values of the scoring columns: "
            f"{ {role: df[col].iloc[test_idx].head(3).tolist() for role, col in (spec.get('inputs') or {}).items()} }"
        )
        return None
    y_true, labels = y_test, classes
    if spec["prediction"] == "proba" and len(classes) == 2:
        y_true, labels = (y_test == classes[1]).astype(int), [0, 1]  # the positive class is the second
    kwargs = {"labels": labels} if spec["name"] == "log_loss" else {}
    inverse = INVERSE[spec.get("target_transform") or "identity"]  # identity in format 1 and for classification
    if spec["prediction"] == "value":
        y_true, y_pred = inverse(np.asarray(y_true, dtype=float)), inverse(np.asarray(y_pred, dtype=float))
    value = float(STANDARD[spec["name"]](y_true, y_pred, **kwargs))
    print(f"{spec['name']} of a random prediction on the first test fold ({len(test_idx)} rows): {value:.4f}")
    return value


if __name__ == "__main__":
    main(Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else TOY_CONTAINER)
