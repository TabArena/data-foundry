# Data Foundry v1: the notebooks behind BeyondArena

Data Foundry v1 is the notebook-based curation flow. The 142 datasets of
[BeyondArena](https://huggingface.co/datasets/TabArena/BeyondArena) and the re-curated TabArena v0.1 datasets were
built with it, and their shipped containers are v1 containers (format 1).

> [!IMPORTANT]
> v1 is retired for new datasets. Add every new dataset as a v2 folder: see
> [CONTRIBUTING_DATASETS.md](CONTRIBUTING_DATASETS.md) and the `/add-dataset` skill. The TabArena v0.2 working copy
> ([`datasets/_dev/tabarena-v0pt2/`](datasets/_dev/tabarena-v0pt2/)) re-curates the BeyondArena datasets as v2
> definitions.

This page keeps what is still needed to read, check or maintain a v1 dataset. Loading and benchmarking a shipped
container needs none of it: `BEYOND_ARENA.get_dataset(name)` works the same for both formats (the
[README](README.md)).

## Where v1 lives

| Path | What it is |
|---|---|
| [`datasets/beyond_iid/`](datasets/beyond_iid/) | The BeyondArena notebooks (`old_iid/`, `new_iid/`, `temporal/`, `grouped/`, one `<name>/<name>.ipynb` each) and [`final_uuid_list.py`](datasets/beyond_iid/final_uuid_list.py), which pins every shipped container by `(unique_name, uuid)`. |
| [`datasets/_maintenance/`](datasets/_maintenance/) | v1 notebooks outside a shipped collection: the re-curated TabArena v0.1 datasets (`_old_collections/tabarena-v0pt1/`), deprecated, suspended and out-of-scope datasets. |
| [`datasets/_dev/feature_selection/`](datasets/_dev/feature_selection/) | v1 notebooks of the feature-selection work (SelectArena). |
| [`src/data_foundry/curation_recommendations.py`](src/data_foundry/curation_recommendations.py) | The v1 split helpers. |
| a record's `notebook_path` | The notebook that produced the shipped container (`v2_path` names its v2 definition). |

The v1 notebook template, `datasets/_template/_template.ipynb`, was removed on 2026-10-02; its last version is in
git (`git show 04e6cfe:datasets/_template/_template.ipynb`).

## Format-1 containers

* The task metadata is `PredictiveMLTaskMetadata` (`predictive-ml-task-mold-v1`): the regime is the flat
  `time_on`, or `group_on` with `group_labels` and an optional `group_time_on`. There is no grouping block, so
  `container.grouping` raises; `container.format_version` is 1, and `container_metadata.json` has no
  `format_version` key.
* The format-1 classes keep exactly the fields the shipped checksums encode. A field added later is left out of the
  checksum while unset (`_OMIT_WHEN_UNSET`), so every shipped container still verifies: `container.verify()`.
  Their checksum is version 1 (no `v2:` prefix), which hashes the dtype names, the values and the index.
* Format 2 (v2 definitions) stores the group fields once, in `grouping`; `task_metadata.group_on`, `group_labels`
  and `group_time_on` read the same in both formats.

## The v1 split protocol

`curation_recommendations.get_recommended_splits_dimensions` sets the repeats by the train size N (2/3 of the rows,
or of the groups for `per_group` labels): 20 x 3 below 500, 10 x 3 below 2,500, 3 x 3 below 250,000, 1 x 3 below
1M. From 1.25M rows a dataset gets one holdout split of 1M train and 250k test rows, in a sub-sampled `<name>_1m`
notebook (`subsample_split_to_budget`). IID and grouped splits come from `get_recommended_iid_splits` and
`get_recommended_grouped_splits`; temporal splits were written by hand in each notebook. `run_bundle_checks` judges
a format-1 container by this protocol (`splits_dimensions_off_protocol`, the 250k `splits_test_over_budget`); v2
has its own protocol (always 3 folds, at most 1M train and 500k test rows).

## The notebook pipeline

A v1 notebook ran these steps, in this order, with the rendered output of each committed as evidence:

```python
from data_foundry.schema import DatasetMetadata, PredictiveMLTaskMetadata, PredictiveMLSplitsMetadata
from data_foundry import dataset_checks
from data_foundry.curation_recommendations import get_recommended_splits_dimensions, get_recommended_iid_splits
from data_foundry.curation_container import CuratedContainer
from data_foundry.bundle_checks import run_bundle_checks, verify_saved_container

dataset_mold = DatasetMetadata(unique_name="blood_transfusion", ...)    # 1. what the data is
task_mold = PredictiveMLTaskMetadata(target_column_name="DonatedBloodInMarch2007",
                                     problem_type="binary_classification", objective_metric_name="roc_auc",
                                     stratify_on="DonatedBloodInMarch2007")  # the task and its regime columns

df = ...                                                                 # 2. load and clean from dataset_mold.path
df = df.sample(frac=1, random_state=42).reset_index(drop=True)           #    shuffle IID data; sort temporal data

dataset_checks.run_all_checks(data=df, target_feature=task_mold.target_column_name,
                              problem_type=task_mold.problem_type)       # 3. five tables, kept in the output

n_repeats, n_splits, test_size = get_recommended_splits_dimensions(dataset=df)   # 4. outer splits
splits = get_recommended_iid_splits(dataset=df, n_repeats=n_repeats, n_splits=n_splits, test_size=test_size,
                                    stratify_on=task_mold.stratify_on)

curated = CuratedContainer(dataset=df, dataset_metadata=dataset_mold, task_metadata=task_mold,
                           experiment_metadata=PredictiveMLSplitsMetadata(splits_comment="...", splits=splits))
run_bundle_checks(curated, ignore=[]).raise_if_errors()                  # 5.-6. bundle, then check it
save_path = curated.save()                                               # 7. new UUID and checksum
verify_saved_container(save_path, container=curated).raise_if_errors()
```

* A warning accepted on purpose went into `ignore=["<slug>"]`, with the reason in a comment next to it.
* A sub-sampled or otherwise derived version set `DatasetMetadata.version_from_unique_name` and `version_comment`,
  and saved under `<original_name>/versions/<uuid>/`.
* `save()` mints a new UUID each time, so a notebook was run to the end once and its output committed.

## Checking a shipped container

For a shipped BeyondArena dataset (the `/verify-dataset` skill covers v2 definitions only):

1. **Inputs.** The notebook is the record's `notebook_path`. Use it rather than guessing
   `datasets/**/<name>/<name>.ipynb`: a sibling such as `<name>_1m.ipynb` or `<name>_clf.ipynb` may be the run that
   shipped. Read the metadata cell, every preprocessing step, the split construction and the committed outputs. The
   container is `BEYOND_ARENA.get_dataset("<name>")`. The record's `## Comments` and the upstream source are read as
   for a v2 dataset.
2. **Automated checks.**

   ```python
   from data_foundry.bundle_checks import run_bundle_checks
   from data_foundry.collections import BEYOND_ARENA

   report = run_bundle_checks(BEYOND_ARENA.get_dataset("<name>"))   # prints the report
   ```

   For the whole collection: `.venv/bin/python .claude/skills/verify-dataset/scripts/check_collection_bundles.py
   --collection BeyondArena --examples 5`. The leak, task and group probes run on v2 definitions; for a shipped
   container, run them on its v2 folder when the splits match, or the same probes by hand
   ([`leak_checks.md`](.claude/skills/check-candidate/references/leak_checks.md)).
3. **Pointer and pin.** The record's `notebook_path` names the notebook under the tree it ships from
   (`datasets/beyond_iid/`, never `datasets/_dev/`), and the notebook's saved output carries the UUID that
   `final_uuid_list.py` pins. A mismatch means the record points at the wrong run, or the notebook was re-run after
   the collection was pinned. `.venv/bin/python -m data_foundry.curation.cli sync-notebooks --check` must be clean.
4. **Template conformance.** The notebook follows the headings *Dataset and Task Metadata → Preprocessing → Data
   Checks → Task Curation → Bundle → Bundle Checks → Export*, calls `run_all_checks(..., problem_type=...)`, has a
   *Bundle Checks* cell with `run_bundle_checks(curated_data, ignore=[...]).raise_if_errors()` before `save()` (each
   `ignore` entry with its reason) and `verify_saved_container(...)` after it.

## Maintaining a v1 notebook

* Do not re-run a shipped notebook end to end and re-save: `save()` mints a new UUID and breaks the collection pin.
  A collection release re-ran notebooks and rewrote `final_uuid_list.py` with
  [`scripts/beyond_arena/rerun_notebooks_update_uuids.py`](scripts/beyond_arena/rerun_notebooks_update_uuids.py);
  [`scripts/beyond_arena/export_warehouse_bundle.py`](scripts/beyond_arena/export_warehouse_bundle.py) zips the
  pinned containers.
* Do not edit committed notebook outputs; they are the evidence. Notebooks must stay valid JSON: edit them with
  `nbformat`, never by hand in the cell `source` arrays.
* A notebook that moves or is superseded needs its record's `notebook_path` updated in the same change
  (`sync-notebooks`); `tests/test_records_integrity.py` fails on a stale pointer.
* A fix that changes data belongs in the dataset's v2 definition in the working copy, not in the v1 notebook.
