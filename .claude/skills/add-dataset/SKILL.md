---
name: add-dataset
description: Add a curated dataset to data-foundry as a v2 dataset folder (one `dataset.py` class + `explore.ipynb` + a generated `README.md`). Use this whenever a triaged candidate that came out `Yes` should be processed, or the user says "add / process / curate / scaffold dataset X". Reads the curation record, scaffolds the folder with `.venv/bin/python -m data_foundry.curation.cli dataset new`, fills the metadata and the preprocessing from the source, and loops on `dataset check` until the bundle checks are clean. v2 only: never writes a v1 curation notebook.
argument-hint: <unique_name>
user-invocable: true
---

# Add a dataset to data-foundry (v2)

Every dataset lives in **one folder**, `datasets/_dev/tabarena-v0pt2/<unique_name>/` for now (the TabArena v0.2
working copy):

| File | Written by | Role |
|---|---|---|
| `dataset.py` | you | The **only** definition: one `AbstractCuratedDataset` subclass. Flat class attributes declare the metadata, the task, the standard preprocessing and the splits; a few hooks hold the code. |
| `explore.ipynb` | the template, then whoever explores | The workbench: `ds = workbench()` loads this folder's dataset and picks up every edit to `dataset.py`. Committed without outputs: the README is the page GitHub shows, and its checksum tells when it is stale. |
| `README.md` (+ `figures/*.png`) | `dataset check` / `build` | The dataset card and evidence, which GitHub shows below the folder's files: YAML frontmatter (machine-readable build record, data/split shape, bundle-check slugs, decision titles), then the files of the folder, links (record, source, collection), how to rebuild, the dataset and task, the curation notes, the splits, the decisions with their tables and figures, the check results and the build record. Never edit it by hand: it is rewritten from `dataset.py`. |

The interface is `data_foundry.v2.AbstractCuratedDataset` (`src/data_foundry/v2/dataset.py`, read its class
docstrings before writing); discovery is `data_foundry.v2.discover_datasets(root)`, and `tests/test_v2_datasets.py`
tests every discovered folder, so there is no per-dataset test file and no registry to edit.

The triage comes first (`/triage-candidates`: the record must be a `Yes`); the judgment pass comes after
(`/verify-dataset`).

## The one rule that governs everything below

**You have not seen the data.** At scaffold time the raw files are usually not even downloaded. So: **pre-fill
structure, never facts.**

* Anything you can derive from the curation record or from a convention → fill it in.
* Anything that needs a look at the data → emit it as an *ordered, commented step* with a `# TODO(verify): …`
  marker saying what to check, in the method where it belongs.
* Never invent a column name, a class label, a leak, or a horizon. `"TODO"` as a value is correct and safe in a
  free-text field; a plausible-looking guess is not. `domain`, `source` and `problem_type` take one of a fixed set of
  values, so the class does not import with `"TODO"` there: pick the closest match from §A and say so in the report.

TODO markers are enforced, not decorative: `dataset check` reports `meta_placeholder_left` for any `TODO` / `FIXME`
in the metadata, `definition_license_placeholder` for a `license` that is still `"TODO"`, and `definition_todo_left`
for any `TODO(verify)` left in `dataset.py`; all three are errors, and `dataset build` refuses to save while any
remains. Say so in your report.

## What the base class does for you (do not re-implement it)

* **Metadata:** builds `DatasetMetadata` / `PredictiveMLTaskMetadataV2` (container format 2) from the flat attributes. Multi-line text
  (`download_description`, `bibtex`, `curation_comments`, `version_comment`, `splits_comment`) is indented like code
  and dedented for you. The BibTeX key is parsed from `bibtex`. The regime tags (`IID`, or `Non-IID` +
  `Temporal`/`Grouped`) are added from the task; `data_tags` lists only context tags (`Spatial`, `Anonymized`, …).
* **Defaults:** `metric` is the one for the problem type (`roc_auc` / `log_loss` / `rmse`, canonical short names);
  `stratify_on` is the target for classification. Set them only to deviate.
* **Standard steps after `_clean`**: cast the columns `_feature_types` names (`FeatureTypes(categorical=...,
  string=..., datetime=...)`, a dict gives datetime formats; unused categories removed; a classification target
  becomes a category without being listed), then fix the row order — a stable sort by
  the time column for temporal tasks, otherwise a shuffle with seed 42 (`shuffle = False` to opt out, with a reason in
  `curation_comments`). Never shuffle, sort or `reset_index` yourself.
* **Seeds:** one shuffle seed (42) and one split seed (4267) for the whole benchmark, fixed in the base class.
* **Same data on every run and machine:** sorts take `kind="stable"`, file listings are `sorted(...)`, a polars
  `group_by` keeps `maintain_order=True`, and a polars join's output is sorted before it is written
  (`definition_nondeterministic` checks the first three). The rows and splits are then the same everywhere; only the
  last bit of a numpy log or exp can differ between CPUs, so a rebuild elsewhere may give another checksum for a
  log-scaled target.
* **Refused at import:** besides missing attributes, a multi-column group key or `stratify_on` (build one key in
  `_clean`), `Temporal(splits=...)` or `subsample_to_budget` together with a custom `_make_splits` (they would be
  ignored), `subsample_to_budget` on a name without `_1m`, and `TemporalSplits` without `n_windows`, `cutoffs` or
  `min_train_fraction`. After `_clean`, a declared column that is missing, or a group or time column with missing
  values, stops the run with the attribute's name.
* **Regime:** one object. A grouped task declares `grouping = Grouping(on=..., labels=..., prediction_unit=...,
  aggregation=..., context=..., definition=...)`, stored in the container; the `definition` (what a group is, why it
  is held out, the use case with its source) is required. A temporal task declares `temporal = Temporal(on=...,
  splits=TemporalSplits(...))`; a window of fixed length (calendar or rows) is the horizon, and only windows that do
  not fix one (`unit="unique"`, `window=None`, `_make_splits`) add `horizon=..., horizon_unit=...`. Neither is an IID
  task. The flat `time_on`,
  `group_on`, `group_labels`, `group_time_on`, `temporal_splits`, `time_horizon` and `time_horizon_unit` attributes no
  longer import (patterns, "The definition file").
* **Splits:** the v2 split protocol (`src/data_foundry/v2/splits.py`): the recommended IID / grouped 3-fold
  cross-validation with the default comment; `Temporal(splits=TemporalSplits(...))` with at least 3 windows for
  temporal tasks (the comment and, for fixed-length windows, the horizon are derived); `subsample_to_budget = True` for a
  `_1m` version of data over the row budget (patterns §C). `_make_splits` only for what none of these express.

## Step 0: Gather inputs

Parse `$ARGUMENTS` for the `unique_name`. Read `curation/records/<unique_name>.md`: its frontmatter carries the
name, `original_source`, `year`, `domain`, `required_split`, `problem_type`, `source_links`, `original_data_state`,
and its `## Comments` hold the provenance and duplicate-check reasoning already done (do not redo settled work).
Ask only for what is missing or contradictory. If there is no record, stop and point to `/triage-candidates`.

## Step 1: Understand the source and map the fields

Follow `source_links` to the original publication (paper, competition page, institution). Then map the fields; the
full rules are in [`references/dataset_patterns.md`](references/dataset_patterns.md) §A: `unique_name` (snake_case,
equal to the folder), `year`, `domain`, `source` (where the data *first appeared*), `source_url`, `license`,
`download_description`, `bibtex` (cite the work that *published the data*), `curation_comments` (house format),
`target`, `problem_type`, and per regime `temporal = Temporal(...)` or `grouping = Grouping(...)`. For a grouped
task, also write down the use case from the source: what one real-world prediction is (a row, or a whole group with
an aggregation), and what is known about a new group when predicting (patterns §C).

Write down the prediction point in the first `curation_comments` bullet: when the model is used and what is known
then (at launch, at admission, at quote time, before the stay ends). Every column, filter and split decision below
is checked against it. In the 2026 leak audit it found columns no probe flagged (kickstarter's `staff_pick`, awarded
mid-campaign, once the task was "predict at launch").

## Step 2: Pick the regime and read a reference dataset

Read the closest reference in full before writing (paths under `datasets/_dev/tabarena-v0pt2/`):

| Regime | Reference | What it shows |
|---|---|---|
| IID | `airfoil_self_noise/dataset.py` | The minimal definition: attributes, `_load_raw`, a short `_clean`. |
| Grouped | `early_learning_predictors/dataset.py`, `musk/dataset.py`, `emscad/dataset.py` | `Grouping` with a `definition` citing the source (musk: one prediction per molecule, `aggregation="any"`), rule-based leak drops in `_clean`, long feature lists (early_learning), a group id built from the data and an accepted group finding (emscad). |
| Temporal | `kick/dataset.py` | `TemporalSplits(window=None, unit="unique", n_windows=9, min_train_fraction=0.5)`, a datetime in `_feature_types`, and `_decisions` with a table and a figure. |
| Sub-sampled `_1m` | `sepsis_prediction_1m/dataset.py` (grouped), `delivery_eta_1m/dataset.py` (temporal) | `version_of`, `version_comment`, `subsample_to_budget`, grouped labels per sample; 3 weekly `TemporalSplits` with a `splits_comment` that states the sub-sampling. |
| Heavy raw data | `acquire_valued_shoppers_challenge/dataset.py` | `prepared_raw_files` + `_prepare_raw_files` (a polars join run once), fixed calendar windows. |

## Step 3: Scaffold and fill `dataset.py`

```bash
.venv/bin/python -m data_foundry.curation.cli dataset new <unique_name> --root datasets/_dev/tabarena-v0pt2
```

This copies `datasets/_template/{dataset.py,explore.ipynb}`, names the class, and pre-fills year, link and
problem type from the record. Then fill in, following `references/dataset_patterns.md`:

1. **Attributes:** every field from Step 1; `"TODO"` where the data must be seen first.
2. **`_load_raw(self, raw_dir)`:** only reading (and a join along the source's own keys). It is cached, so edits to
   the cleaning never re-read the files. Return one frame, or a dict of frames for multi-table sources.
3. **`_clean(self, raw)`:** the §B recipe as ordered, commented steps with `TODO(verify)` markers — renames,
   label mapping, proxy-missing values, column drops (`drop_columns(df, [...])` fails on a misspelled name),
   row filters, target transforms. Sibling files are under `self.folder`.
   **`_feature_types(self, df)`:** return the `FeatureTypes` of the cleaned frame; the lists may be computed from
   `df`. Cast mid-way in `_clean` (`cast_dtypes`) only when a later step needs the dtype.
4. **Regime and splits:** IID: nothing to declare. Grouped: `grouping = Grouping(...)` from §C with the default
   split. Temporal: `temporal = Temporal(on=..., splits=TemporalSplits(...))` from §C, with `splits_comment` saying
   why this window; `horizon`/`horizon_unit` only when the window is not a calendar one. A `splits_comment` replaces
   the generated text, so restate the windows (and any sub-sampling or trimming) in it.
5. **`accepted_check_warnings`:** leave empty. The curator fills it once they have seen which warnings apply, one
   reason per slug.
6. **`_decisions`** (optional, §F) and **`_extra_checks`** (a dataset-specific check such as a leak test) only when
   there is something to show or test.

Do not write `explore.ipynb` cells beyond the template; that is the curator's space.

## Step 4: Point the curation record at the definition

A record carries two pointers: `v2_path` (its `dataset.py`, the one this skill writes) and, for a dataset that
shipped in BeyondArena, `notebook_path` (the v1 notebook it shipped from; never write or edit one, see
`DATA_FOUNDRY_V1.md`). Run `.venv/bin/python -m data_foundry.curation.cli sync-notebooks`
to fill both from the tree; `--check` must stay clean (`tests/test_records_integrity.py` checks it).

## Step 5: Verify the scaffold

```bash
.venv/bin/python -m data_foundry.curation.cli dataset list --root datasets/_dev/tabarena-v0pt2   # the class imports and validates
.venv/bin/ruff check --fix datasets/_dev/tabarena-v0pt2/<unique_name>/dataset.py && .venv/bin/ruff format datasets/_dev/tabarena-v0pt2/<unique_name>/dataset.py
```

`dataset list` logs `Skipping <name>: …` and exits non-zero when a class does not import or validate (missing
attribute, name/folder mismatch, a temporal task without windows, a grouping without a `definition`, …): fix it
before handing off. ruff fixes the quoting and import order.

## Step 6: The loop (curator, or you when the raw data is present)

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/<unique_name>
```

runs the whole pipeline, the data checks, the bundle checks and `_decisions`, **without saving** (no UUID), and
writes `README.md`. Iterate: resolve TODOs in `dataset.py`, look at the data in `explore.ipynb` (edits are picked up
automatically), re-run `check`, read the `README.md` diff. Stop when there are no errors and every warning is fixed
or accepted with a reason. Use the §E table to pre-empt the checks.

The bundle checks catch mechanical problems, not most leaks. Once the data loads, run the leak probes and read them
with [`../check-candidate/references/leak_checks.md`](../check-candidate/references/leak_checks.md):

```bash
.venv/bin/python .claude/skills/verify-dataset/scripts/leak_probes.py <unique_name>
```

A single feature that comes close to the full model, a missing-value indicator that predicts the label, test rows
copied from train, or a `dataset_pure_feature_value` warning each need a decision before the warning is accepted:
drop, lag, filter, re-split or keep on purpose, with the numbers in a `curation_comments` bullet (or a `_decisions`
table). The precedents for each kind of leak are in that file's §3-§5.

Then check that the task is worth benchmarking: dummy baselines against three untuned model families on the shipped
splits, scored per group for a group-unit task with `mean`, `any` or `last` (per row for `select_*`), with a drift baseline for temporal regression and multiclass tasks:

```bash
.venv/bin/python .claude/skills/verify-dataset/scripts/task_probes.py <unique_name>
```

Each flag needs a decision written down: `no_signal` (no model beats the dummy; check the features and the target),
`solved` or `one_feature` (a leak or a lookup first: back to the leak probes), `no_spread` (all families tie; on a
small task this may be noise), `drift_baseline` (a constant from the newest data is as good as the models),
`unstable` (few test rows or groups). For a grouped task also run `.claude/skills/verify-dataset/scripts/group_probes.py <unique_name>`.

## Step 7: Build (curator only)

```bash
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/<unique_name>
```

saves the container to the warehouse (new UUID), verifies the export, and records UUID, checksum and git commit in
the `README.md` frontmatter. There is no v0.2 collection in the registry yet: record the UUID in the working
copy's `CHANGELOG.md` and its `README.md` table, and never add it to `BEYOND_ARENA_UUIDS`. Never run `build`
yourself unless asked.

## Step 8: Report

* The folder you created and a summary of the populated attributes.
* **Every `TODO(verify)` marker you left, grouped by method**, so the curator has the work list.
* Mapping decisions that were ambiguous, and which §D traps you flagged as plausible for *this* dataset, and why.
* What happens next, with paths filled in: fill the TODOs and loop on `dataset check` (Step 6); once it is clean,
  run `/verify-dataset <unique_name>`. Do not run `/verify-dataset` yourself right after scaffolding: there is no
  data to check yet.
