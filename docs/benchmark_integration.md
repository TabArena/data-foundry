# Benchmark integration

This page is for whoever connects a benchmark harness (TabArena, or your own) to Data Foundry containers. It covers
loading a container, the task view that holds the protocol, and the rules a harness has to keep. The work still open
on the TabArena side, with the evidence behind each item, is in
[`BENCHMARK_CHANGES_TODO.md`](../datasets/_dev/tabarena-v0pt2/BENCHMARK_CHANGES_TODO.md).

The short version: load a container, call `container.task()`, and use only what the task view gives you.

```python
from data_foundry.examples import load_toy_container

task = load_toy_container(format_version=2).task()
for fold in task.folds():
    model.fit(task.X(fold.train), task.y(fold.train), sample_weight=task.train_weight(fold.train))
    score = task.score(task.y(fold.test), model.predict(task.X(fold.test)), fold.test)
    error = task.error(score)  # lower is better, 0 at the metric's best value
```

[`examples/minimal_adapter.py`](../examples/minimal_adapter.py) is this loop as a script (about 40 lines), and
[`examples/benchmark_container.py`](../examples/benchmark_container.py) adds the recommended encodings of dates, text
and special features.

## Install

| Install | What it gives |
|---|---|
| `pip install data-foundry` | loading containers, the collections, the task view, the folds and the row budget |
| `pip install "data-foundry[benchmark]"` | also scoring: scikit-learn (within the pin of `build`) and scipy, imported when a metric is computed |
| `pip install "data-foundry[encodings]"` | skrub's date encoding and the e5 text embeddings (pulls in torch) |
| `pip install "data-foundry[build]"` | building datasets from their definitions, and RDKit for the SMILES encodings |

A harness needs the core install plus `benchmark`. The consumer modules (`data_foundry.task`, `metrics`, `sampling`,
`special`, `encodings`, `curation_container`) import nothing of the build side; a test guards it.

## Load

Containers ship in collections, pinned by `(unique_name, uuid)` and fetched from Hugging Face into a local cache
(`~/.cache/data_foundry/<collection>/`, or `$DATA_FOUNDRY_CACHE`):

```python
from data_foundry.collections import BEYOND_ARENA, get_collection, list_collections

container = BEYOND_ARENA.get_dataset("airfoil_self_noise", verify=True)  # verify: recompute the checksum
```

`prefetch()` and `iter_containers()` download a whole collection (several GB). Two toy containers ship inside the
package and need no network: `load_toy_container()` is format 1 (binary classification, IID folds) and
`load_toy_container(format_version=2)` is format 2 (claims per year insured, grouped by customer, a weight scoring
column that is also the training weight, an ordered category). A folder on disk loads with
`CuratedContainer.load(path)` from `data_foundry.curation_container`.

## The task view

`container.task()` returns a frozen `BenchmarkTask` (`data_foundry.task`). Its fields are facts derived from the
container's metadata:

| Field | What it is |
|---|---|
| `name`, `format_version`, `target`, `problem_type` | the dataset, its container format (1 or 2), the target column and the problem type |
| `classes` | the sorted classes: the column order of `predict_proba` the scorer reads; `None` for regression |
| `features` | the model inputs |
| `split_columns` | the columns an inner validation split reads (group, time, unit) |
| `special_features` | inputs that need an encoding by kind (a SMILES column, a spectrum's group of columns) |
| `metric`, `greater_is_better`, `optimum` | the metric spec, its direction and its best value |
| `grouping` | how a grouped task is used (`data_foundry.schema.Grouping`), or `None` |
| `sample_weight`, `validation_weight`, `unit_column` | the training weight, the validation weight, the unit of a unit weight |
| `row_budget`, `time_unit` | the most rows a fit may use (`_1m` versions), the calendar of a numeric time column |

Its methods take row positions in `container.dataset`:

| Method | Returns |
|---|---|
| `folds(budget=True)` | every outer split as a `Fold(repeat, fold, train, test, train_side)` |
| `X(rows)`, `y(rows)` | the inputs and the target of the rows, indexed by their positions |
| `train_weight(rows)`, `validation_weights(rows)` | the weights as floats, or `None` |
| `score(y_true, y_pred, rows)` | the metric on the rows |
| `error(score)` | the distance to the optimum, 0 at best |
| `to_dict()` | the fields above as JSON-able data |

The view uses the helpers of `data_foundry.curation_container` (`feature_columns`, `split_columns`, `sample_weight`,
`validation_weight`, `unit_weight`, `special_features`), `data_foundry.sampling.subsample_train` and
`data_foundry.metrics.scorer`. They stay available, and each rule lives in one of them.

A format-2 container saves `to_dict()` next to its metadata as `benchmark_task.json`. The file is derived from the
metadata and is not part of the checksum, so `verify()` ignores it. Code that reads the container files without Data
Foundry takes the feature list from it
([`examples/read_metric_without_data_foundry.py`](../examples/read_metric_without_data_foundry.py)).

## Folds and the row budget

`task.folds()` yields the shipped splits. Never re-split or shuffle them: they encode the regime (IID, temporal,
grouped). A container with a row budget (a `<name>_1m` version, `task.row_budget`) caps its test sides and keeps
every row a train side may use; `fold.train` is the default sample of the train side, at most
`row_budget.train` rows, drawn by the sampler the container records (`experiment_metadata.train_sampling`: for a
temporal side the newest year, extended back in time until it holds that many rows, then sampled at random; whole
groups of a grouped side; stratified rows otherwise). The sample is deterministic. `fold.train_side` is the whole
side; `folds(budget=False)` fits on it. A method that picks its own rows takes them from `train_side` only, keeps the
unit `train_sampling` names, and goes on a separate leaderboard track. The budget is a hard cap, inner validation
included, and is read from the container, never assumed to be 1M.

A numeric time column carries its calendar in `task.time_unit`: numerai's `era` counts weeks, so the newest year of
a train side is its last 52 eras.

## Inputs and special features

Build X from `task.X(rows)`, for every pipeline. `task.features` leaves out the target, the group column(s), the
scoring columns (metric inputs such as an era or a weight), the unit of a unit weight, and a time column that dates
the label (`time_of == "label"`: the moment the label became known, after the prediction point). These columns stay
in the frame for the split and the scorer.

An inner validation split (early stopping, tuning) reads `task.split_columns` from the same rows before the model
fits on the features: whole groups on one side for a grouped task, the newest rows held out for a temporal one, a
unit's rows on one side for a unit weight. A time column of the prediction point is in both lists; a group column or
a label time only in `split_columns`.

Features come in several dtypes: numeric, categorical, ordinal (an ordered categorical, whose order a model should
get, for example as its codes), `datetime` and `string` (free text). Pick a model that takes mixed dtypes, or encode
them; `data_foundry.encodings` has the recommended encodings of dates and text. A special feature
(`task.special_features`) is encoded by its kind with `data_foundry.special.encode_special_feature(frame, feature)`,
or by your own encoder. Where `feature.encoding_required` is true (a SMILES) the raw column is no model input: encode
it or leave it out, never pass it on as text.

## Weights

A task may declare a training weight, `task.sample_weight` (6 tasks of TabArena v0.2, all insurance rates): fit
every model with `task.train_weight(fold.train)` as the row weight. It is never a feature, and its test-row values
are for the scorer only (they are the realized exposure, which a model at the quote does not have).

`task.validation_weights(rows)` is the metric's row weight: weight every validation loss by it, so a model selects
and stops on what the test score counts. It is the training weight when there is one, or a unit weight
(`task.unit_column` set) that counts each unit once; a unit weight is never a training weight.

## Scoring and errors

`task.score(y_true, y_pred, rows)` scores by the container's metric spec (`task.metric`: name, kind, prediction,
params, inputs, origin and reference). Predictions follow `task.metric.prediction`:

- `proba`: class probabilities with the columns in the order of `task.classes` (sorted, scikit-learn's `classes_`),
  also for an ordered target, whose declared order is type information only; a binary task may pass the probability
  of `classes[1]` alone. A DataFrame whose columns are the class names is matched by name.
- `label`: predicted classes.
- `value`: numbers on the scale the target ships on. A target shipped on a modelling scale (`target_transform` `log`,
  `log1p`, `log10`) is scored after the inverse of both the truth and the predictions.

The scorer takes the metric's input columns (a group, an order, a weight) from the scored rows, floors the
predictions of a deviance at its `min_prediction`, and aggregates the row predictions of a task scored per group
(`grouping.prediction_unit == "group"`). It needs the rows for that. Without `rows`, a pandas `y_true` gives them by its
index: `task.y(rows)` keeps the container's index (`0..n-1`), so a caller that passes only `(y_true, y_pred)`, as
AutoGluon's scorer interface does, still scores a metric with inputs. The scorer checks that `y_true` is the target on
those rows and raises otherwise.

A score is NaN where the metric is undefined on the rows (one class in a fold for an AUC). The build checks refuse
shipped folds where the declared metric is undefined, so a NaN on a shipped split means the harness scored other rows.

`task.error(score)` is `optimum - score` when higher is better and `score - optimum` otherwise: lower is better and 0
is the best value. The optimum per metric is in the registry (`data_foundry.metrics.METRICS[name].optimum_for(params)`):

| Optimum | Metrics |
|---|---|
| 1 | the AUCs, average precision, accuracy, balanced accuracy, F1, precision, recall, MCC, r2, the correlations, the normalized Ginis, `gini_top_capture`, `precision_at_k`, `average_precision_at_k`, `mean_group_top_k_overlap`, `hierarchical_balanced_accuracy`, `gini_stability`, `normalized_early_detection_utility` |
| 0 | the losses and deviances (log loss, RMSE, MAE, MSE, RMSLE, MAPE, the Poisson and Tweedie deviances), `rmspe`, `mean_group_normalized_rmse`, `par_k` |
| from the params | `cost_matrix`: the smallest cost of its matrix |
| none | `net_revenue_at_cost`, `ordered_lorenz_gini`: their best value changes with the scored rows |

For the two metrics without an optimum `error()` raises, since a distance to a fixed value would measure nothing. Rank
their scores directly; how TabArena handles them is open decision B of the hand-off.

To wrap the scorer for AutoGluon, use `greater_is_better` and `optimum` from the task view, `needs_proba` for
`prediction == "proba"` and `needs_class` for `"label"`, and call `task.score` inside. Inner validation, early
stopping and tuning use the same scorer.

## Format 1 and format 2

`task.format_version` is 2 for a container built by a `dataset.py` definition (the TabArena v0.2 collection and every
new dataset) and 1 for the shipped BeyondArena containers. The task view reads both:

| | Format 1 (BeyondArena) | Format 2 (TabArena v0.2) |
|---|---|---|
| metric | `objective_metric_name` (`roc_auc`, `log_loss`, `rmse`), turned into a spec | `objective_metric`, the full spec |
| grouping | the group column as a grouping with one prediction per row, or `None` | `Grouping`: prediction unit, aggregation, context |
| weights, special features, scoring columns | none | as declared |
| row budget | none | `_1m` versions |
| `benchmark_task.json` | not written | written on save |
| splits on disk | inline in the experiment metadata | the row table `rows.parquet` |

`container.experiment_metadata.splits` returns `{repeat: {fold: (train, test)}}` for both formats; `task.folds()`
reads it.

## What the harness still has to do

[`BENCHMARK_CHANGES_TODO.md`](../datasets/_dev/tabarena-v0pt2/BENCHMARK_CHANGES_TODO.md) lists the changes on the
TabArena side, in order, with the datasets each one touches: pinning the release that reads format 2, inner
validation that follows the outer split, scoring at the prediction unit, the group context, the encoding caches,
and the open decisions (losses for deviance-scored tasks, errors of metrics without an optimum, threshold tuning,
the default encodings of spectra, text and dates).
