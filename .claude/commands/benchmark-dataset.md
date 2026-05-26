Fit and evaluate a model on a BeyondArena dataset across its outer CV
splits, honoring the dataset's split regime (IID vs. temporal non-IID vs.
grouped non-IID).

## When to invoke

* The user wants to **train + score** a model on a named BeyondArena
  dataset.
* The user wants a **per-fold** metric printout, a **mean ± std** summary
  over all splits, or both.
* The user is comparing multiple sklearn-style estimators on the same
  dataset.

If the user only wants to *load* the dataset, use `/get-dataset` —
no need to involve a model.

If the user wants to compare datasets, not models, use `/browse-collection`
or `/get-dataset` and let `container.describe()` do the talking.

## Required iteration shape

This is the OpenML / TabArena / BeyondArena convention — match it exactly
so results are comparable. The outer loop is over `repeat_id`, the inner
loop is over `fold_id`:

```python
splits = container.experiment_metadata.splits        # {repeat: {fold: (train_idx, test_idx)}}
target = container.task_metadata.target_column_name
df = container.dataset

scores: list[float] = []
for repeat_id, folds in splits.items():
    for fold_id, (train_idx, test_idx) in folds.items():
        X_train, y_train = df.iloc[train_idx].drop(columns=target), df.iloc[train_idx][target]
        X_test,  y_test  = df.iloc[test_idx].drop(columns=target),  df.iloc[test_idx][target]
        # fit + score …
        scores.append(metric_value)
```

**Do not** shuffle / re-split the data — the curator already produced
splits that respect the regime. Bypassing them defeats the point of the
curated container.

## Picking the metric

Read `container.task_metadata.objective_metric_name` and prefer the
matching sklearn metric:

| `objective_metric_name` | sklearn import |
|---|---|
| `"rmse"` | `sklearn.metrics.root_mean_squared_error` (sklearn ≥1.4) |
| `"roc_auc"` | `sklearn.metrics.roc_auc_score` (use `predict_proba(...)[:, 1]`) |
| `"log_loss"` | `sklearn.metrics.log_loss` (use `predict_proba`) |
| anything else | check `task_metadata.problem_type` and pick a sensible default |

`container.task_metadata.is_classification` flips you between regressor
and classifier — handy for picking the model.

## Canonical example to read

[`examples/benchmark_on_beyond_arena.py`](../../examples/benchmark_on_beyond_arena.py)
— Random Forest on `airfoil_self_noise`, full describe printout, per-fold
RMSE, mean ± std. That file is the reference layout; copy its structure
unless the user asks for something else.

## Quick recipe

```python
import numpy as np
from data_foundry.collections import BEYOND_ARENA
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error

container = BEYOND_ARENA.get_dataset("airfoil_self_noise")
print(container.describe())                       # confirm the regime + target

df = container.dataset
splits = container.experiment_metadata.splits
target = container.task_metadata.target_column_name

rmses: list[float] = []
for repeat_id, folds in splits.items():
    for fold_id, (train_idx, test_idx) in folds.items():
        X_train, y_train = df.iloc[train_idx].drop(columns=target), df.iloc[train_idx][target]
        X_test,  y_test  = df.iloc[test_idx].drop(columns=target),  df.iloc[test_idx][target]
        model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
        model.fit(X_train, y_train)
        rmse = float(root_mean_squared_error(y_test, model.predict(X_test)))
        rmses.append(rmse)
        print(f"  repeat {repeat_id}  fold {fold_id}:  RMSE={rmse:.4f}")

print(f"Mean RMSE over {len(rmses)} splits: {np.mean(rmses):.4f} (std {np.std(rmses):.4f})")
```

## Gotchas

* **Categorical / text / datetime features** are not numeric — most linear
  models and plain trees will choke. Pick a model that handles raw mixed
  dtypes (Random Forest, gradient-boosted trees with categorical support,
  TabPFN, etc.) or add a preprocessing pipeline. `container._feature_dtype_counts()`
  tells you what to expect before you fit.
* **Grouped non-IID, `group_labels="per_sample"`**: rows in one group can
  have different targets — confirm with the user that they want
  group-leakage protection (the splits already enforce it) but that the
  prediction unit is the **row**, not the group.
* **Temporal non-IID**: do not shuffle, do not stratify, do not refit on
  the test fold. The split order already encodes time direction.
* **Don't over-claim performance** on datasets with known anomalies — read
  `container.dataset_metadata.curation_comments`, which often calls out
  duplicates or quirks worth a footnote.
