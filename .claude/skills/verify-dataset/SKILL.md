---
name: verify-dataset
description: Verify a curated dataset before it ships. Runs the automated bundle checks (`dataset check` for a v2 `dataset.py`, `run_bundle_checks` for a v1 notebook or saved container), then works a 15-item judgment rubric (original source, uniqueness, scope, split regime, prediction-time availability, leakage, comments vs code, dtypes, metric, citation, record pointers) and reports pass / concern / cannot-verify with evidence. Use when a definition is filled in and checks run clean, before a PR, or when a shipped dataset is suspected of leakage, a wrong split or wrong provenance ("is X ready / correct / leaky?").
argument-hint: <unique_name | dataset folder | notebook>
user-invocable: true
---

# Verify a dataset

Verify a curated dataset before it ships: run the automated bundle checks, then work the
judgment rubric that no code can check, and report both with evidence.

**Input (optional):** a v2 dataset folder (holding `dataset.py`), a notebook path, a `unique_name`, or a container path.

$ARGUMENTS

## When to invoke

* A curation notebook has been filled in and the curator wants a second pass before the PR.
* `/add-dataset` scaffolded a v2 dataset folder, the curator has filled it in and `dataset check` runs clean, and
  it is time to check.
* A shipped dataset is suspected of a problem (leakage, wrong split, wrong provenance).
* The curator asks "is this dataset ready / correct / leaky / really original?"

Related: `/triage-candidates` for the backlog record and the selection criteria; `/add-dataset` to scaffold
a v2 dataset folder; `BEYOND_ARENA.get_dataset(name)` (CLAUDE.md) to load a shipped container.

**Two formats.** New datasets are v2 folders: `dataset.py` (one `AbstractCuratedDataset` subclass, the only
definition), `explore.ipynb` (workbench) and a generated `README.md` (evidence; frontmatter is machine-readable).
Shipped datasets are still v1 notebooks. Where the steps below say "notebook", read `dataset.py` for a v2
dataset, and read `README.md` where they say "committed cell outputs".

## What this is, and what it is not

There are two halves to verification and they must not be confused:

* **Automated** — `data_foundry.bundle_checks` proves the *mechanical* invariants (split indices,
  leakage across fold boundaries, dtypes, class coverage, the per-split row budget of at most 1M
  train and 250k test rows for a v1 notebook, BibTeX syntax, export round-trip). For a v2 definition
  `dataset check` swaps in the v2 split protocol (`src/data_foundry/v2/splits.py`): always 3 folds or at
  least 3 temporal windows, at most 1M train and 500k test rows per split, and data over that budget only
  as a sub-sampled `_1m` version (IID / grouped: the frame sampled to 1.5M rows; temporal: sampled per
  window). Cheap, exhaustive, and already
  deterministic. **Run it; never re-derive its findings by eye.**
* **Judgment** — provenance, scope, whether the split matches the real application, whether a
  feature would have been available at prediction time, whether the comments describe what the code
  does. Code cannot settle these. This is what you are for.

Your verdict is **advisory**. A human curator has the final say (same contract as the
`AI (UNVERIFIED)` convention in `/triage-candidates`).

## Step 0 — Locate the inputs

1. **The definition** — the record carries two pointers: `v2_path`, the `dataset.py` in the TabArena v0.2
   working copy (verify this one for anything that will ship in v0.2), and `notebook_path`, the BeyondArena
   notebook that produced the shipped container. For the notebook: it is the record's own pointer
   to the one notebook behind this dataset, so use it rather than assuming
   `datasets/**/<unique_name>/<unique_name>.ipynb`. That matters where a dataset has sibling runs:
   a sub-sampled `<unique_name>_1m.ipynb` or an alternative target `<unique_name>_clf.ipynb` may be
   the run that shipped, and verifying the other one verifies a dataset nobody uses. If the record
   has no pointer yet, resolve it with `data-foundry-curation sync-notebooks` (or list
   `<unique_name>*.ipynb` in the dataset directory and match the UUID as in item 14). Read it in
   full: the metadata cell, every preprocessing step, the split construction, and the committed cell
   *outputs* (the `run_all_checks` tables are evidence you should use, not re-run).
2. **The container** — the saved bundle. Either `local-data-warehouse/<unique_name>/<uuid>/` or, for
   a shipped dataset, `BEYOND_ARENA.get_dataset("<unique_name>")`.
3. **The backlog record** — `curation/records/<unique_name>.md`, if it exists. Its `## Comments` hold
   the provenance and duplicate-check reasoning already done; do not redo settled work, and do not
   contradict it without new evidence.
4. **The upstream source** — follow `original_dataset_source_download_link`. Fetch the dataset page /
   paper / competition description. Most rubric items below are unanswerable without it.

If the container has not been saved yet, run the notebook's Bundle + Bundle Checks cells' logic
yourself (construct the container in a scratch script) — **do not re-run the notebook end to end and
re-save**: `save()` mints a new UUID, and for a shipped dataset that breaks the collection pin.

## Step 1 — Run the automated checks

**v2 dataset:** `.venv/bin/python -m data_foundry.curation.cli dataset check <folder>` runs the whole pipeline and
the bundle checks without saving (no UUID) and rewrites `README.md`. Compare it with the committed `README.md`: an
unexpected diff (checksum, split sizes, new findings) means the definition drifted from its evidence. Accepted
warnings are the class attribute `accepted_check_warnings` (slug → reason). For a v1 notebook or a shipped
container:

```python
from data_foundry.bundle_checks import run_bundle_checks
from data_foundry.collections import BEYOND_ARENA          # or CuratedContainer.load(path)

container = BEYOND_ARENA.get_dataset("<unique_name>")
report = run_bundle_checks(container)                       # prints the report
```

For a whole collection: `python scripts/beyond_arena/check_collection_bundles.py --examples 5`.

Then, in your own report:

* list every **error** — these block the PR;
* for every **warning**, say whether it is a real problem *for this dataset* or is correct as-is.
  A warning the curator accepts belongs in `accepted_check_warnings` (v2) or the notebook's `ignore=[...]`
  (v1) **with the reason** — propose the exact edit, including the reason;
* do not re-state passing checks one by one. "Bundle checks: 0 errors, 3 warnings (2 accepted,
  see below)" is the right level.

Then run the leak probes, which the bundle checks do not cover: `.venv/bin/python scripts/v2/leak_probes.py
<unique_name>` (v2; for a shipped container, the same probes by hand on its splits). Read them with
[`../check-candidate/references/leak_checks.md`](../check-candidate/references/leak_checks.md), which also lists the
other probes (same-label subgroups, number formats by class, target by period, entity overlap) and what the 2026 leak
audit decided for each kind of leak. Their numbers are the evidence for items 4, 5, 6, 9 and 13.

Then run the task probes: `.venv/bin/python scripts/v2/task_probes.py <unique_name>` (or `--built` to read the built
container). On the shipped splits they compare dummy baselines (the train side's class shares or mean, and for a
temporal regression or multiclass task the same from the newest data) with a linear model, a random forest and
LightGBM, per group for a group-unit task, plus the best single feature. Their flags are the evidence for item 13.
For a grouped task, `scripts/v2/group_probes.py <unique_name>` gives the IID vs grouped gap and a permutation test
across groups (item 4).

## Step 2 — Work the judgment rubric

For each item: **pass / concern / cannot-verify**, plus one line of *evidence* (a quote from the
source page, a notebook line, a number from the check output). "Looks fine" is not evidence.
`cannot-verify` is a legitimate and useful verdict — never upgrade it to `pass`.

| # | Item | What to actually check |
|---|---|---|
| 1 | **Original source** | Does the link bottom out at the *original* publication (paper, competition, institution), not an anonymous re-upload? A working Kaggle/OpenML link is not provenance. Does `dataset_source` name where the data first appeared? |
| 2 | **Uniqueness** | Is this the same underlying data as another dataset in the collection under a different name — including a different target/slice/version of one cohort? Compare canonical links and follow each to its origin (see *Checking for duplicates* in the curation guidelines). |
| 3 | **Scope** | Was it *published for* a predictive classification/regression task? Exclude time-series forecasting, CTR, ranking/recsys, non-predictive survey/discovery tables. Scope by the **original** task, not the re-upload's framing. |
| 4 | **Split regime** | Does the declared regime (`Temporal`, `Grouping`, or neither) match the real application? Read the source description; a prescribed random split is a *claim*, not evidence. For a grouped task, do `prediction_unit`, `aggregation` and `context` follow the source's use case, and does the `definition` cite it? Read the README's "Group structure" section and run `scripts/v2/group_probes.py` for a small or doubtful grouped task (signal across groups, IID vs grouped gap). A missing timestamp does not make a stream of contemporaneous readings IID. Check for grouped structure inside a temporal task (repeated entities over time) and vice versa. A group id must be a true id or one constructed exactly from the data (identical profile text, consecutive blocks in the raw file order), never a similarity cluster; check a claimed source split against the data (share of test entities seen in train); check that a row-order time index follows the date. |
| 5 | **Availability at prediction time** | Is the prediction point written down, and would every feature have been known then? Aggregates computed over the full dataset, post-outcome fields, or anything the source computed after the label are leaks; so is missingness caused by the outcome (fields blank because the patient died) and a feature window that ends at the outcome. Temporal tasks: is the planning gap real, and is every training row's label known at the prediction point? |
| 6 | **Irreversible leakage** | Any feature that is itself the output of a supervised transform fit on the whole dataset (discriminant score, target/mean encoding, a model's prediction, PCA of the full set)? That cannot be recomputed per split and is an exclusion, not a warning. Label-aware features computed over all rows before splitting are fixable (drop them). Recording or batch artefacts that differ by class (rounding, a source-specific assay; two same-label subgroups that separate) are fixed by harmonising, or exclude the dataset when they run through every feature. |
| 7 | **Comments vs code** | Is every claim in `curation_comments` actually implemented in the notebook, and is every non-obvious code step documented? Silent drops, filters, and casts are the ones that bite. |
| 8 | **dtype semantics** | Are `category` / `string` / numeric / datetime chosen by *meaning* (finite value set vs. free text), proxy missing values converted to `NA`, uninformative identifiers dropped, informative ones kept and processed? Use the `dataset_missing_value_*` / `dataset_identifier_column` warnings as leads. |
| 9 | **Target & metric** | Is the target the original task's target, and is `objective_metric_name` the metric the original task/competition scored? If the checks flagged `task_metric_unknown`, confirm the custom metric is intended and registered downstream. Is the target complete in every test period (no right-censoring by the download date), and is the cohort the source's (no rows that cannot have the outcome, or a stated reason for them)? |
| 10 | **License & citation** | Is the license what the source actually states (the checks only see whether the field is filled)? Does the BibTeX cite the *right* work — the paper/competition that published this data, not a paper that merely used it? Syntax being valid says nothing about correctness. |
| 11 | **Reproducibility** | Would `download_description`, pasted into a shell today, recreate the raw inputs? Are URLs pinned (DOI, archived release) rather than mutable HEAD links? |
| 12 | **Ethics & representativeness** | Any subject/creator objection to ML use, obvious ethical concern, or a task tabular models would not be used for (e.g. features that are an algorithmic vectorization of image content)? See the exclusion criteria in the curation guidelines. |
| 13 | **Trivial or empty** | Read the task-probe flags. `no_signal`: no model beats the dummy, so the features do not carry the target (wrong target, lost columns, or a task too noisy to rank models). `solved` (ROC AUC or R^2 at least 0.995) and `one_feature` (one feature with 95% of the best skill): first a leak or a deterministic target, run the leak probes. `no_spread`: all three untuned families tie, which criterion 4C calls trivial, unless the folds are too noisy to tell (`unstable`). `drift_baseline`: a constant from the newest data predicts as well as the models, so the task is mostly drift. Each flag is a question: report the numbers and propose `Trivial` only with a reason. The cheap findings (`splits_test_single_class`, `splits_test_minority_few`, `splits_test_target_constant`, `task_target_value_dominant`) say whether every fold can be scored. |
| 14 | **Record pointer** | Does the record's `notebook_path` name *this* notebook, is it under the tree the dataset ships from (`datasets/beyond_iid/` for BeyondArena — never `datasets/_dev/`, which holds work in progress and superseded copies), and does this notebook's saved output carry the UUID the collection pins (`BEYOND_ARENA` entry / `datasets/beyond_iid/final_uuid_list.py`)? Does `v2_path` name this dataset's `dataset.py` in `datasets/_dev/tabarena-v0pt2/` (a `_1m` folder only when its class declares `version_of` the record), and does its `README.md` carry the UUID once built? A mismatch means the record points at the wrong run, or the notebook was re-run after the collection was pinned — say which. `data-foundry-curation sync-notebooks --check` must be clean; evidence is the UUID string itself. |
| 15 | **Template conformance** | *v2:* the class validates on import (`dataset list` shows it), follows the current [`datasets/_template/v2/dataset.py`](../../../datasets/_template/v2/dataset.py), keeps diagnostics out of `dataset.py` (they belong in `explore.ipynb`), and `README.md` was regenerated after the last edit (`build_stale` is false when built). *v1:* does the notebook follow the *current* [`datasets/_template/_template.ipynb`](../../../datasets/_template/_template.ipynb)? Open the template and compare section by section, not from memory, since it changes. Today that means the headings *Dataset and Task Metadata → Preprocessing → Data Checks → Task Curation → Bundle → Bundle Checks → Export* in that order; `run_all_checks(..., problem_type=task_mold.problem_type)` (not the old `classification=`); a *Bundle Checks* cell with `run_bundle_checks(curated_data, ignore=[...]).raise_if_errors()` before `save()`, where every `ignore` entry carries its reason; and `verify_saved_container(...)` after `save()`. Any other deviation from the template needs a reason in `curation_comments` or a cell comment. Report each drift as a concrete edit; restructuring an old notebook must not change its preprocessing or split logic. |

Read the selection criteria and processing conventions in [`.claude/skills/triage-candidates/references/curation_guidelines.md`](../../../.claude/skills/triage-candidates/references/curation_guidelines.md) before judging items 1–4 and
12–13; they encode decisions you would otherwise guess at.

## Step 3 — Report

1. **Verdict** — one of: *ready*, *ready with noted concerns*, *needs changes*, *should not ship*.
2. **Automated** — error/warning counts, each error, and the per-warning call from Step 1.
3. **Rubric** — a compact table of the 15 items with verdict + evidence. Put `concern` and
   `cannot-verify` rows first; the passes can be one line each.
4. **Proposed fixes** — concrete edits (`dataset.py` attribute or hook, notebook cell, accepted-warning entry with its
   reason). Apply them only if the user asks.
5. **What a human must still check** — every `cannot-verify`, spelled out so it can be picked up.

## Rules

* **Never claim verification you did not perform.** If you could not reach the source page, say so.
* **Do not silently re-save the container.** New UUID = broken pin. Say what needs re-running and
  let the curator do it.
* **Do not edit committed notebook outputs.** They are the evidence trail.
* **A notebook that moves or gets superseded needs its record updated.** If the run that ships
  changes — a `_1m` sub-sample replaces the full-size run, a notebook is renamed or relocated — set
  the record's `notebook_path` / `v2_path` to the new one (or run `data-foundry-curation sync-notebooks`) in the
  same change. A stale pointer sends every reader to a notebook that did not produce the data, and
  `tests/test_records_integrity.py` fails on it.
* If you record findings in the backlog record (`curation/records/<unique_name>.md`), follow the
  `AI (UNVERIFIED)` convention from `/triage-candidates` and preserve existing human `CC (…)` notes.
* Substance over volume: a short report with three real concerns beats thirteen paragraphs of
  "verified, looks good".
