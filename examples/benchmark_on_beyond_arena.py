"""Train a random forest on one BeyondArena dataset across every outer CV split.

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

import sys
from pathlib import Path

import numpy as np
from data_foundry.collections import BEYOND_ARENA
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error

EXAMPLE_DATASET = "airfoil_self_noise"


def main(cache_dir: Path | None, dataset_name: str) -> None:
    print(f"Loading `{dataset_name}` from {BEYOND_ARENA.source!r}")
    print(f"Cache override: {cache_dir}\n")

    container = BEYOND_ARENA.get_dataset(dataset_name, cache_dir=cache_dir)
    print(container.describe())
    print()

    df = container.dataset
    splits = container.experiment_metadata.splits
    target_name = container.task_metadata.target_column_name

    # Iterate over every (repeat, fold) split — same shape as the OpenML example.
    rmses: list[float] = []
    print("Benchmarking random forest across splits:")
    for repeat_id, folds in splits.items():
        for fold_id, (train_indices, test_indices) in folds.items():
            train_data = df.iloc[train_indices]
            test_data = df.iloc[test_indices]
            X_train = train_data.drop(columns=target_name)
            y_train = train_data[target_name]
            X_test = test_data.drop(columns=target_name)
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


if __name__ == "__main__":
    override = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    dataset = sys.argv[2] if len(sys.argv) > 2 else EXAMPLE_DATASET
    main(override, dataset)
