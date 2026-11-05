the """Train a model on one BeyondArena dataset across every outer CV split, scored by RMSE.

BeyondArena ships format-1 containers: the metric is named only (``task_metadata.objective_metric_name``). This
example fits a random forest regressor and scores RMSE, so it takes the numeric regression datasets. For a Data
Foundry v2 container (the TabArena v0.2 collection, or one built locally), with its metric spec, scoring columns and
feature types, see ``benchmark_container.py``.

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

Requires ``scikit-learn>=1.4`` (for :func:`sklearn.metrics.root_mean_squared_error`).
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
from data_foundry.collections import BEYOND_ARENA
from data_foundry.schema import as_column_list
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error

if TYPE_CHECKING:
    from data_foundry.curation_container import CuratedContainer

EXAMPLE_DATASET = "airfoil_self_noise"


def main(cache_dir: Path | None, dataset_name: str) -> list[float]:
    """Benchmark one BeyondArena dataset; return the RMSE of every split."""
    print(f"Loading `{dataset_name}` from {BEYOND_ARENA.source!r}")
    print(f"Cache override: {cache_dir}\n")
    container = BEYOND_ARENA.get_dataset(dataset_name, cache_dir=cache_dir)
    print(container.describe())
    print()
    return benchmark_format_1(container)


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
    args = parser.parse_args()
    main(args.cache_dir, args.dataset)
