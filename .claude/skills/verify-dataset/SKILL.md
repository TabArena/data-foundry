---
name: verify-dataset
description: Verify a curated dataset before it ships. Runs the automated bundle checks (`dataset check` for a v2 `dataset.py`; `run_bundle_checks` for a shipped v1 container, see references/v1_notebooks.md), then works a 15-item judgment rubric (original source, uniqueness, scope, split regime, prediction-time availability, leakage, comments vs code, dtypes, metric, citation, record pointers) and reports pass / concern / cannot-verify with evidence. Use when a definition is filled in and checks run clean, before a PR, or when a shipped dataset is suspected of leakage, a wrong split or wrong provenance ("is X ready / correct / leaky?").
argument-hint: <unique_name | dataset folder | notebook>
user-invocable: true
---

# Verify a dataset

Verify a curated dataset before it ships: run the automated bundle checks, then work the
judgment rubric that no code can check, and report both with evidence.

**Input (optional):** a v2 dataset folder (holding `dataset.py`), a notebook path, a `unique_name`, or a container path.

$ARGUMENTS

## When to invoke

* `/add-dataset` scaffolded a v2 dataset folder, the curator has filled it in and `dataset check` runs clean, and
  it is time to check.
* A shipped dataset is suspected of a problem (leakage, wrong split, wrong provenance); for the shipped container
  itself, see the v1 path below.
* The curator asks "is this dataset ready / correct / leaky / really original?"

Related: `/triage-candidates` for the backlog record and the selection criteria; `/add-dataset` to scaffold
a v2 dataset folder; `BEYOND_ARENA.get_dataset(name)` (CLAUDE.md) to load a shipped container.

**Two paths.** Which one applies depends on what ships:

* **v2** (TabArena v0.2 and every new dataset): a folder holding `dataset.py` (one `AbstractCuratedDataset` subclass,
  the only definition), `explore.ipynb` (workbench) and a generated `README.md` (evidence; the frontmatter is
  machine-readable). Its container is format 2 (`container.format_version == 2`). Steps 0 and 1 below are this path.
* **v1** (the shipped BeyondArena containers): a curation notebook under `datasets/beyond_iid/` and a format-1
  container. Use [`references/v1_notebooks.md`](references/v1_notebooks.md) for Steps 0 and 1 and for the v1 halves
  of items 14 and 15. Steps 2 and 3 are the same; read the notebook where they say `dataset.py`, and its committed
  cell outputs where they say `README.md`.

A dataset in the v0.2 working copy has both. Verify the v2 folder for anything that ships in v0.2, and the notebook
only when the question is about the shipped container.

## What this is, and what it is not

There are two halves to verification and they must not be confused:

* **Automated** — `data_foundry.bundle_checks` proves the *mechanical* invariants (split indices,
  leakage across fold boundaries, dtypes, class coverage, BibTeX syntax, export round-trip) and judges the splits by
  the protocol of the container's format. For format 2 that is the v2 split protocol
  (`src/data_foundry/v2/splits.py`): always 3 folds or at least 3 temporal windows, at most 1M train and 500k test
  rows per split, and data over that budget only as a sub-sampled `_1m` version (IID / grouped: the frame sampled to
  1.5M rows; temporal: sampled per window). Cheap, exhaustive, and deterministic. **Run it; never re-derive its
  findings by eye.**
* **Judgment** — provenance, scope, whether the split matches the real application, whether a
  feature would have been available at prediction time, whether the comments describe what the code
  does. Code cannot settle these. This is what you are for.

Your verdict is **advisory**. A human curator has the final say (same contract as the
`AI (UNVERIFIED)` convention in `/triage-candidates`).

## Step 0 — Locate the inputs

1. **The definition** — the record's `v2_path`: the `dataset.py` in `datasets/_dev/tabarena-v0pt2/<unique_name>/`
   (or the `_1m` folder whose class declares `version_of` the record). Read it in full: the class attributes, every
   hook (`_load_raw`, `_clean`, `_feature_types`, `_make_splits`, ...), the regime (`grouping` or `temporal`) and the
   accepted warnings with their reasons. Then read the generated `README.md` next to it: the frontmatter (checksum,
   split sizes, bundle-check findings, `build`) and the sections (data checks, group structure, splits) are evidence
   to use, not to re-run.
2. **The container** — the `build.path` in the `README.md` frontmatter, under the warehouse (`<unique_name>/<uuid>/`,
   or `<version_of>/versions/<uuid>/` for a `_1m` version). Not built yet: `dataset check` (Step 1) builds the same
   container in memory.
3. **The backlog record** — `curation/records/<unique_name>.md`, if it exists. Its `## Comments` hold
   the provenance and duplicate-check reasoning already done; do not redo settled work, and do not
   contradict it without new evidence.
4. **The upstream source** — follow `original_dataset_source_download_link`. Fetch the dataset page /
   paper / competition description. Most rubric items below are unanswerable without it.

Do not run `dataset build` to verify: it mints a new UUID. `dataset check` gives the same container without saving.

## Step 1 — Run the automated checks

`.venv/bin/python -m data_foundry.curation.cli dataset check <folder>` runs the whole pipeline and the bundle checks
without saving (no UUID) and rewrites `README.md`. Compare it with the committed `README.md`: an unexpected diff
(checksum, split sizes, new findings) means the definition drifted from its evidence. Accepted warnings are the class
attribute `accepted_check_warnings` (slug → reason).

Then, in your own report:

* list every **error** — these block the PR;
* for every **warning**, say whether it is a real problem *for this dataset* or is correct as-is.
  A warning the curator accepts belongs in `accepted_check_warnings` **with the reason** — propose the exact edit,
  including the reason;
* do not re-state passing checks one by one. "Bundle checks: 0 errors, 3 warnings (2 accepted,
  see below)" is the right level.

Then run the leak probes, which the bundle checks do not cover: `.venv/bin/python .claude/skills/verify-dataset/scripts/leak_probes.py
<unique_name>`. Read them with
[`../check-candidate/references/leak_checks.md`](../check-candidate/references/leak_checks.md), which also lists the
other probes (same-label subgroups, number formats by class, target by period, entity overlap) and what the 2026 leak
audit decided for each kind of leak. Their numbers are the evidence for items 4, 5, 6, 9 and 13.

Then run the task probes: `.venv/bin/python .claude/skills/verify-dataset/scripts/task_probes.py <unique_name>` (or `--built` to read the built
container). On the shipped splits they compare dummy baselines (the train side's class shares or mean, and for a
temporal regression or multiclass task the same from the newest data) with a linear model, a random forest and
LightGBM (per group for a group-unit task with `mean`, `any` or `last`; a `select_*` task is scored per row), plus
the best single feature. Their flags are the evidence for item 13.
For a grouped task, `.claude/skills/verify-dataset/scripts/group_probes.py <unique_name>` gives the IID vs grouped gap and a permutation test
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
| 4 | **Split regime** | Does the declared regime (`Temporal`, `Grouping`, or neither) match the real application? Read the source description; a prescribed random split is a *claim*, not evidence. For a grouped task, do `prediction_unit`, `aggregation` and `context` follow the source's use case, and does the `definition` cite it? Read the README's "Group structure" section and run `.claude/skills/verify-dataset/scripts/group_probes.py` for a small or doubtful grouped task (signal across groups, IID vs grouped gap). A missing timestamp does not make a stream of contemporaneous readings IID. Check for grouped structure inside a temporal task (repeated entities over time) and vice versa. A group id must be a true id or one constructed exactly from the data (identical profile text, consecutive blocks in the raw file order), never a similarity cluster; check a claimed source split against the data (share of test entities seen in train); check that a row-order time index follows the date. |
| 5 | **Availability at prediction time** | Is the prediction point written down, and would every feature have been known then? Aggregates computed over the full dataset, post-outcome fields, or anything the source computed after the label are leaks; so is missingness caused by the outcome (fields blank because the patient died) and a feature window that ends at the outcome. Temporal tasks: is the planning gap real, and is every training row's label known at the prediction point? |
| 6 | **Irreversible leakage** | Any feature that is itself the output of a supervised transform fit on the whole dataset (discriminant score, target/mean encoding, a model's prediction, PCA of the full set)? That cannot be recomputed per split and is an exclusion, not a warning. Label-aware features computed over all rows before splitting are fixable (drop them). Recording or batch artefacts that differ by class (rounding, a source-specific assay; two same-label subgroups that separate) are fixed by harmonising, or exclude the dataset when they run through every feature. |
| 7 | **Comments vs code** | Is every claim in `curation_comments` actually implemented in `dataset.py`, and is every non-obvious code step documented? Silent drops, filters, and casts are the ones that bite. |
| 8 | **dtype semantics** | Are `category` / `string` / numeric / datetime chosen by *meaning* (finite value set vs. free text), proxy missing values converted to `NA`, uninformative identifiers dropped, informative ones kept and processed? Use the `dataset_missing_value_*` / `dataset_identifier_column` warnings as leads. |
| 9 | **Target & metric** | Is the target the original task's target, and is `objective_metric_name` the metric the original task/competition scored? If the checks flagged `task_metric_unknown`, confirm the custom metric is intended and registered downstream. Is the target complete in every test period (no right-censoring by the download date), and is the cohort the source's (no rows that cannot have the outcome, or a stated reason for them)? |
| 10 | **License & citation** | Is the license what the source actually states (the checks only see whether the field is filled)? Does the BibTeX cite the *right* work — the paper/competition that published this data, not a paper that merely used it? Syntax being valid says nothing about correctness. |
| 11 | **Reproducibility** | Would `download_description`, pasted into a shell today, recreate the raw inputs? Are URLs pinned (DOI, archived release) rather than mutable HEAD links? |
| 12 | **Ethics & representativeness** | Any subject/creator objection to ML use, obvious ethical concern, or a task tabular models would not be used for (e.g. features that are an algorithmic vectorization of image content)? See the exclusion criteria in the curation guidelines. |
| 13 | **Trivial or empty** | Read the task-probe flags. `no_signal`: no model beats the dummy, so the features do not carry the target (wrong target, lost columns, or a task too noisy to rank models). `solved` (ROC AUC or R^2 at least 0.995) and `one_feature` (one feature with 95% of the best skill): first a leak or a deterministic target, run the leak probes. `no_spread`: all three untuned families tie, which criterion 4C calls trivial, unless the folds are too noisy to tell (`unstable`). `drift_baseline`: a constant from the newest data predicts as well as the models, so the task is mostly drift. Each flag is a question: report the numbers and propose `Trivial` only with a reason. The cheap findings (`splits_test_single_class`, `splits_test_minority_few`, `splits_test_target_constant`, `task_target_value_dominant`) say whether every fold can be scored. |
| 14 | **Record pointer** | Does the record's `v2_path` name this dataset's `dataset.py` in `datasets/_dev/tabarena-v0pt2/` (a `_1m` folder only when its class declares `version_of` the record), and does its `README.md` carry the UUID once built (`build.uuid`, `build_stale` false)? `.venv/bin/python -m data_foundry.curation.cli sync-notebooks --check` must be clean; evidence is the UUID string itself. For the shipped container's `notebook_path` and the collection pin, see [`references/v1_notebooks.md`](references/v1_notebooks.md). |
| 15 | **Template conformance** | The class validates on import (`dataset list` shows it), follows the current [`datasets/_template/v2/dataset.py`](../../../datasets/_template/v2/dataset.py), keeps diagnostics out of `dataset.py` (they belong in `explore.ipynb`), and `README.md` was regenerated after the last edit (`build_stale` is false when built). Report each drift as a concrete edit. |

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
* **A definition that moves or gets superseded needs its record updated.** If the folder that ships
  changes (a `_1m` version replaces the full-size run, a folder is renamed), set the record's `v2_path` to the new
  one (or run `.venv/bin/python -m data_foundry.curation.cli sync-notebooks`) in the same change. A stale pointer
  sends every reader to a definition that did not produce the data, and `tests/test_records_integrity.py` fails on
  it.
* If you record findings in the backlog record (`curation/records/<unique_name>.md`), follow the
  `AI (UNVERIFIED)` convention from `/triage-candidates` and preserve existing human `CC (…)` notes.
* Substance over volume: a short report with three real concerns beats thirteen paragraphs of
  "verified, looks good".
