"""Train a model on one BeyondArena dataset (or any container) across every outer CV split, scored by its metric.

Calls :meth:`CuratedContainer.describe` to highlight every field of the
container's metadata — including the feature-dtype counts and the split
regime (IID vs. temporal non-IID via ``time_on`` vs. grouped non-IID via
``group_on``).

The default dataset is ``airfoil_self_noise`` — a small all-numeric
regression task, so a random forest runs without any preprocessing.

Run::

    # Default: airfoil_self_noise, default cache.
    python examples/benchmark_on_beyond_arena.py

    # Override the cache directory.
    python examples/benchmark_on_beyond_arena.py /tmp/my_cache

    # Pick a different (numeric regression) BeyondArena dataset.
    python examples/benchmark_on_beyond_arena.py /tmp/my_cache concrete_compressive_strength

    # A format-2 container (the TabArena v0.2 collection, or one built locally) from its folder.
    python examples/benchmark_on_beyond_arena.py --container <container folder>

The two container formats score differently:

* Format 1 (BeyondArena) names its metric only (``task_metadata.objective_metric_name``); this example fits a random
  forest regressor and scores RMSE, so it takes the numeric regression datasets.
* Format 2 carries the metric spec (``task_metadata.objective_metric``: the name, what it takes, its origin and
  reference) and the scoring columns, the metric's inputs that are never features. The features are
  ``feature_columns(container)`` (no target, group or scoring column), and ``scorer(container)`` scores the test
  rows by the spec, taking the scoring columns' values by row index. The model is a histogram gradient boosting
  model, which takes numeric and categorical columns; other columns (strings, datetimes) are left out here.

Requires ``scikit-learn>=1.4`` (for :func:`sklearn.metrics.root_mean_squared_error`).
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.collections import BEYOND_ARENA
from data_foundry.curation_container import CuratedContainer, feature_columns
from data_foundry.schema import as_column_list
from data_foundry.v2.metrics import scorer
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import root_mean_squared_error

EXAMPLE_DATASET = "airfoil_self_noise"


def main(cache_dir: Path | None, dataset_name: str, container_path: Path | None = None) -> list[float]:
    """Benchmark one dataset (a BeyondArena name, or the container at ``container_path``); return the scores."""
    if container_path is not None:
        container = CuratedContainer.load(container_path)
    else:
        print(f"Loading `{dataset_name}` from {BEYOND_ARENA.source!r}")
        print(f"Cache override: {cache_dir}\n")
        container = BEYOND_ARENA.get_dataset(dataset_name, cache_dir=cache_dir)
    print(container.describe())
    print()
    if container.format_version >= 2:
        return benchmark_by_spec(container)
    return benchmark_format_1(container)


def benchmark_by_spec(container: CuratedContainer) -> list[float]:
    """Format 2: the features without the scoring columns, the score by the container's metric spec."""
    df = container.dataset
    task = container.task_metadata
    spec = task.objective_metric
    target_name = task.target_column_name
    features = [c for c in feature_columns(container) if _usable(df[c])]
    score = scorer(container)  # score(y_true, y_pred, row_index): looks up the scoring columns by row index
    labels = list(df[target_name].cat.categories) if task.problem_type != "regression" else None
    print(f"Metric: {spec.name} ({spec.origin}; takes {spec.prediction}; ", end="")
    print(f"{'higher' if spec.greater_is_better else 'lower'} is better); {len(features)} features")

    scores: list[float] = []
    for repeat_id, folds in container.experiment_metadata.splits.items():
        for fold_id, (train_indices, test_indices) in folds.items():
            train_data, test_data = df.iloc[train_indices], df.iloc[test_indices]
            if labels is None:
                model = HistGradientBoostingRegressor(categorical_features="from_dtype", random_state=42)
            else:
                model = HistGradientBoostingClassifier(categorical_features="from_dtype", random_state=42)
            model.fit(train_data[features], train_data[target_name])
            X_test = test_data[features]
            if spec.prediction == "proba":
                # The probability columns in the target's category order (the scorer's default labels).
                proba = pd.DataFrame(model.predict_proba(X_test), columns=model.classes_)
                proba = proba.reindex(columns=labels, fill_value=0.0).to_numpy()
                y_pred = proba[:, 1] if len(labels) == 2 else proba
            else:
                y_pred = model.predict(X_test)
            value = score(test_data[target_name].to_numpy(), y_pred, test_indices)
            scores.append(value)
            print(f"  repeat {repeat_id}  fold {fold_id}:  {spec.name}={value:.4f}")
    print(f"\nMean {spec.name} over {len(scores)} splits: {np.mean(scores):.4f}  (std {np.std(scores):.4f})")
    return scores


def _usable(column: pd.Series) -> bool:
    """A column the gradient boosting model takes as it is: numeric, boolean or categorical."""
    return pd.api.types.is_numeric_dtype(column) or isinstance(column.dtype, pd.CategoricalDtype)


def benchmark_format_1(container: CuratedContainer) -> list[float]:
    """Format 1 (BeyondArena): a random forest regressor scored by RMSE (``objective_metric_name``)."""
    df = container.dataset
    splits = container.experiment_metadata.splits
    target_name = container.task_metadata.target_column_name
    # The group column of a grouped task is split metadata, never a feature: a test group is unseen.
    # (`task_metadata.group_on` reads the same in both container formats.)
    not_features = [target_name, *as_column_list(container.task_metadata.group_on)]

    # Iterate over every (repeat, fold) split — same shape as the OpenML example.
    rmses: list[float] = []
    print("Benchmarking random forest across splits:")
    for repeat_id, folds in splits.items():
        for fold_id, (train_indices, test_indices) in folds.items():
            train_data = df.iloc[train_indices]
            test_data = df.iloc[test_indices]
            X_train = train_data.drop(columns=not_features)
            y_train = train_data[target_name]
            X_test = test_data.drop(columns=not_features)
            y_test = test_data[target_name]

            model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            rmse = float(root_mean_squared_error(y_test, y_pred))
            rmses.append(rmse)
            print(f"  repeat {repeat_id}  fold {fold_id}:  RMSE={rmse:.4f}")

    print(
        f"\nMean RMSE over {len(rmses)} splits: {np.mean(rmses):.4f}  (std {np.std(rmses):.4f})",
    )
    return rmses


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("cache_dir", nargs="?", type=Path, default=None, help="Override the BeyondArena cache.")
    parser.add_argument("dataset", nargs="?", default=EXAMPLE_DATASET, help="A BeyondArena dataset name.")
    parser.add_argument("--container", type=Path, default=None, help="Load this container folder instead.")
    args = parser.parse_args()
    main(args.cache_dir, args.dataset, args.container)
