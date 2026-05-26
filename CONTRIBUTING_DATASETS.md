# Contributing a Dataset to Data Foundry

Thanks for adding a dataset! This guide walks you through the full curation
flow — from "I have a raw CSV" to "a `CuratedContainer` that can be used in benchmarks.

> [!TIP]
> Already in a hurry? The minimum viable contribution is a notebook under
> `datasets/_dev/<topic>/<unique_name>/<unique_name>.ipynb` that runs cleanly
> on the [`datasets/_template/_template.ipynb`](datasets/_template/_template.ipynb)
> skeleton and writes a `CuratedContainer` to the local warehouse. The rest
> of this document explains the conventions and the why.

---

## 1. Where dataset curation lives

```
datasets/
├── _dev/                        # ← contributions land here first
│   └── <topic>/
│       └── <unique_name>/
│           └── <unique_name>.ipynb
├── _template/_template.ipynb    # the canonical skeleton to copy
├── _maintenance/                # corrections / re-runs of already-released datasets
└── beyond_iid/                  # promoted datasets pinned by BeyondArena
    ├── new_iid/
    ├── temporal/
    ├── grouped/
    └── final_uuid_list.py       # the immutable (name, uuid) registry
```

* **Add new datasets in `datasets/_dev/`.** Pick (or create) a `_dev/<topic>/`
  subfolder that loosely groups related datasets (e.g. `feature_selection/`).
  Submit a PR that adds your `<unique_name>/<unique_name>.ipynb` there.
* Once reviewers and the curators sign off, the dataset is moved to a relevant collection, the data uploaded, 
  and the UUID is pinned.
  The UUID **never changes** afterwards — that's the whole point of pinning.
* Don't open a PR that edits `beyond_iid/` directly unless you are
  re-curating a released dataset (in which case use `_maintenance/`).

> **Want a head start?** Run `/new-dataset` inside Claude Code from this repo
> (slash command defined in `.claude/commands/new-dataset.md`). Paste
> tab-separated metadata from the curation spreadsheet and it scaffolds a
> notebook in the right `_dev/` subfolder with most fields pre-filled.

---

## 2. The five-step curation pipeline

Every notebook follows the same five steps, mirrored by
[`examples/curate_a_dataset.py`](examples/curate_a_dataset.py). The full
end-to-end script in there is the most authoritative reference; the sections
below explain *what* each step is doing and *why*.

### 2.1 Write the dataset and task metadata

```python
from data_foundry.schema import DatasetMetadata, PredictiveMLTaskMetadata
```

* **`DatasetMetadata`** — what the data is (domain, source, license,
  reference, free-form curation comments, version lineage).
* **`PredictiveMLTaskMetadata`** — what the task on top of it is (target
  column, problem type, objective metric, and crucially the columns that
  drive the split regime — `time_on`, `group_on`, `stratify_on`,
  `group_time_on`, `group_labels`).

`PredictiveMLTaskMetadata.split_regime` returns one of `"iid"`,
`"temporal_non_iid"`, `"grouped_non_iid"` — let that be your sanity check.
`time_on` and `group_on` are mutually exclusive (enforced in
`__post_init__`); see the docstrings in
[`src/data_foundry/schema.py`](src/data_foundry/schema.py) for the exact
semantics, including the subtle `group_labels` ∈ {`per_group`, `per_sample`}
distinction.

### 2.2 Load and clean the data

Stick to **minimal, reproducible** transformations:

* Rename columns for clarity (don't paper over upstream bugs — note them in
  `curation_comments`).
* Map raw target encodings into something meaningful (e.g. `0/1` → `"No"/"Yes"`).
* Cast categorical columns to `pd.CategoricalDtype` — `_feature_dtype_counts`
  in [`CuratedContainer`](src/data_foundry/curation_container.py) and the
  characteristics plotter both rely on dtypes being accurate. A column with
  exactly two distinct non-null values is counted as `binary` regardless of
  dtype, so a binary `category` is fine.
* If the dataset is IID, shuffle deterministically (`df.sample(frac=1,
  random_state=42)`) before generating splits, so the outer CV folds are
  reproducible.

### 2.3 Run the dataset checks

```python
from data_foundry import dataset_checks
df_head, summary, numeric_stats, cat_stats, target_df = dataset_checks.run_all_checks(
    data=df,
    target_feature=task_mold.target_column_name,
    problem_type=task_mold.problem_type,
)
```

`run_all_checks` returns five DataFrames that you should leave in the
notebook output: a head sample, summary stats, numeric/categorical column
stats, and the target distribution. Reviewers use these to catch obvious
issues (highly imbalanced targets, columns that are 100% missing, mislabeled
problem types, …) without re-running the pipeline.

### 2.4 Generate outer CV splits

The split helpers in
[`src/data_foundry/curation_recommendations.py`](src/data_foundry/curation_recommendations.py)
encode the conventions BeyondArena uses (how many repeats × folds per row-count
bucket, stratification rules, etc.):

* IID datasets → `get_recommended_splits_dimensions(...)` + `get_recommended_iid_splits(...)`
* Grouped datasets → `get_recommended_grouped_splits(...)` (passes `group_on`
  / `group_labels`, optionally shows the resulting label balance per fold)
* Temporal datasets → today this is a manual splits dict; document the
  cutoff(s) clearly and store the rationale in `splits_comment`.

The returned `splits` dict is `{repeat_id: {fold_id: (train_idx, test_idx)}}`
— same shape OpenML uses.

### 2.5 Bundle and save

```python
from data_foundry.curation_container import CuratedContainer

curated = CuratedContainer(
    dataset=df,
    dataset_metadata=dataset_mold,
    task_metadata=task_mold,
    experiment_metadata=splits_mold,
)
curated.save()
print(curated.uuid, curated.checksum)
```

`save()` writes the container to
`local-data-warehouse/<unique_name>/<uuid>/`. The UUID is generated by
`uuid7()` so it's monotone-by-time; the checksum is a Blake2b digest over
the dataframe + every metadata object, so any later edit changes it.
Print both at the bottom of the notebook — that's what reviewers diff against.

---

## 3. Best practices

**Versioning.** If you are creating an alternative version of an existing
dataset (e.g. subsampling), set
`DatasetMetadata.version_from_unique_name` to the original `unique_name` and
write a short `version_comment` explaining what changed. The container is
saved under
`<original_name>/versions/<uuid>/` so the lineage is visible in the
warehouse layout and on Hugging Face.

**Reproducibility.** The `download_description` field is a *human-runnable*
script. Future-you (or another contributor) should be able to copy-paste it
into a shell and recreate the raw inputs. Pin URLs to permanent locations
(DOI, archived release) rather than mutable HEAD links.

**Honest comments.** `curation_comments` is the place to record:

* anomalies you deliberately did **not** fix (duplicate rows, leaking columns
  you considered but kept, …),
* sampling choices (downsampling, capping rows, …),
* dataset-specific dtype quirks the loader has to work around.

A short paragraph here is worth its weight when someone else has to
re-curate the data in two years.

**Don't fight pandas dtypes.** The container persists dtypes via
`dtypes.json` and restores them on load; the checksum is computed on the
dataframe *after* dtype application. If a column round-trips to a different
dtype, the checksum will silently drift between save and reload — fix the
dtype before saving rather than after.

**One task per container.** If you have two reasonable target columns or two
different split regimes, save two containers with different `unique_name`s
rather than packing them together.

---

## 4. Opening the PR

1. **Run the notebook end-to-end.** Reviewers expect to see populated check
   tables, the recommended split dimensions, and the final UUID + checksum
   in the saved notebook output.
2. **Keep raw downloads out of the repo.** The `local-data-warehouse/` tree
   is gitignored — that's intentional. Only the notebook lands in the PR.
3. **Reference the parsed metadata source** in the PR description (e.g. a
   row of the curation spreadsheet, an issue, a Slack thread) so reviewers
   can audit the field mappings.
4. **Mark TODOs explicitly.** If you can't resolve something (e.g. the BibTeX
   entry is a placeholder, the temporal split needs a maintainer decision),
   leave a `# TODO:` comment in the relevant cell rather than silently
   shipping a placeholder.

When a PR merges:

* The container is uploaded to a data source (e.g., Hugging Face).
* The pinned UUID is added to a relevant collection.
* The dataset becomes available to anyone via the collection!

---

## 5. References

* Template notebook — [`datasets/_template/_template.ipynb`](datasets/_template/_template.ipynb)
* Schema — [`src/data_foundry/schema.py`](src/data_foundry/schema.py)
* Split helpers — [`src/data_foundry/curation_recommendations.py`](src/data_foundry/curation_recommendations.py)
* Dataset checks — [`src/data_foundry/dataset_checks.py`](src/data_foundry/dataset_checks.py)
* Worked example — [`examples/curate_a_dataset.py`](examples/curate_a_dataset.py)
* Claude Code scaffolding — [`.claude/commands/new-dataset.md`](.claude/commands/new-dataset.md)
