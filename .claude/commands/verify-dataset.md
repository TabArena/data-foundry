Verify a curated dataset before it ships: run the automated bundle checks, then work the
judgment rubric that no code can check, and report both with evidence.

**Input (optional):** a notebook path, a `unique_name`, or a container path.

$ARGUMENTS

## When to invoke

* A curation notebook has been filled in and the curator wants a second pass before the PR.
* `/process-dataset` scaffolded a notebook, the curator has since run it, and it is time to check.
* A shipped dataset is suspected of a problem (leakage, wrong split, wrong provenance).
* The curator asks "is this dataset ready / correct / leaky / really original?"

Related: `/triage-candidates` for the backlog record and the selection criteria; `/process-dataset` to scaffold
a notebook; `/get-dataset` to load a shipped container.

## What this is, and what it is not

There are two halves to verification and they must not be confused:

* **Automated** — `data_foundry.bundle_checks` proves the *mechanical* invariants (split indices,
  leakage across fold boundaries, dtypes, class coverage, BibTeX syntax, export round-trip). Cheap,
  exhaustive, and already deterministic. **Run it; never re-derive its findings by eye.**
* **Judgment** — provenance, scope, whether the split matches the real application, whether a
  feature would have been available at prediction time, whether the comments describe what the code
  does. Code cannot settle these. This is what you are for.

Your verdict is **advisory**. A human curator has the final say (same contract as the
`AI (UNVERIFIED)` convention in `/triage-candidates`).

## Step 0 — Locate the inputs

1. **The notebook** — read `notebook_path` from the backlog record; it is the record's own pointer
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
  A warning the curator accepts belongs in the notebook's `ignore=[...]` **with the reason** —
  propose the exact edit, including the comment;
* do not re-state passing checks one by one. "Bundle checks: 0 errors, 3 warnings (2 accepted,
  see below)" is the right level.

## Step 2 — Work the judgment rubric

For each item: **pass / concern / cannot-verify**, plus one line of *evidence* (a quote from the
source page, a notebook line, a number from the check output). "Looks fine" is not evidence.
`cannot-verify` is a legitimate and useful verdict — never upgrade it to `pass`.

| # | Item | What to actually check |
|---|---|---|
| 1 | **Original source** | Does the link bottom out at the *original* publication (paper, competition, institution), not an anonymous re-upload? A working Kaggle/OpenML link is not provenance. Does `dataset_source` name where the data first appeared? |
| 2 | **Uniqueness** | Is this the same underlying data as another dataset in the collection under a different name — including a different target/slice/version of one cohort? Compare canonical links and follow each to its origin (see `/triage-candidates` for the method). |
| 3 | **Scope** | Was it *published for* a predictive classification/regression task? Exclude time-series forecasting, CTR, ranking/recsys, non-predictive survey/discovery tables. Scope by the **original** task, not the re-upload's framing. |
| 4 | **Split regime** | Does `time_on`/`group_on`/neither match the real application? Read the source description; a prescribed random split is a *claim*, not evidence. A missing timestamp does not make a stream of contemporaneous readings IID. Check for grouped structure inside a temporal task (repeated entities over time) and vice versa. |
| 5 | **Availability at prediction time** | Would every feature have been known at time *t*? Aggregates computed over the full dataset, post-outcome fields, or anything the source computed after the label are leaks. Temporal tasks: is the planning gap real? |
| 6 | **Irreversible leakage** | Any feature that is itself the output of a supervised transform fit on the whole dataset (discriminant score, target/mean encoding, a model's prediction, PCA of the full set)? That cannot be recomputed per split and is an exclusion, not a warning. |
| 7 | **Comments vs code** | Is every claim in `curation_comments` actually implemented in the notebook, and is every non-obvious code step documented? Silent drops, filters, and casts are the ones that bite. |
| 8 | **dtype semantics** | Are `category` / `string` / numeric / datetime chosen by *meaning* (finite value set vs. free text), proxy missing values converted to `NA`, uninformative identifiers dropped, informative ones kept and processed? Use the `dataset_missing_value_*` / `dataset_identifier_column` warnings as leads. |
| 9 | **Target & metric** | Is the target the original task's target, and is `objective_metric_name` the metric the original task/competition scored? If the checks flagged `task_metric_unknown`, confirm the custom metric is intended and registered downstream. |
| 10 | **License & citation** | Is the license what the source actually states (the checks only see whether the field is filled)? Does the BibTeX cite the *right* work — the paper/competition that published this data, not a paper that merely used it? Syntax being valid says nothing about correctness. |
| 11 | **Reproducibility** | Would `download_description`, pasted into a shell today, recreate the raw inputs? Are URLs pinned (DOI, archived release) rather than mutable HEAD links? |
| 12 | **Ethics & representativeness** | Any subject/creator objection to ML use, obvious ethical concern, or a task tabular models would not be used for (e.g. features that are an algorithmic vectorization of image content)? See the exclusion criteria in `/triage-candidates`. |
| 13 | **Trivial** | Do the committed check outputs suggest every model would score identically or solve it perfectly? If so, flag it — a trivial task is an exclusion. |
| 14 | **Record pointer** | Does the record's `notebook_path` name *this* notebook, and does this notebook's saved output carry the UUID the collection pins (`BEYOND_ARENA` entry / `datasets/beyond_iid/final_uuid_list.py`)? A mismatch means the record points at the wrong run, or the notebook was re-run after the collection was pinned — say which. `data-foundry-curation sync-notebooks --check` must be clean; evidence is the UUID string itself. |

Load the selection criteria and processing conventions from `/triage-candidates` before judging items 1–4 and
12–13; they encode decisions you would otherwise guess at.

## Step 3 — Report

1. **Verdict** — one of: *ready*, *ready with noted concerns*, *needs changes*, *should not ship*.
2. **Automated** — error/warning counts, each error, and the per-warning call from Step 1.
3. **Rubric** — a compact table of the 14 items with verdict + evidence. Put `concern` and
   `cannot-verify` rows first; the passes can be one line each.
4. **Proposed fixes** — concrete edits (notebook cell, metadata field, `ignore=[...]` entry with its
   reason). Apply them only if the user asks.
5. **What a human must still check** — every `cannot-verify`, spelled out so it can be picked up.

## Rules

* **Never claim verification you did not perform.** If you could not reach the source page, say so.
* **Do not silently re-save the container.** New UUID = broken pin. Say what needs re-running and
  let the curator do it.
* **Do not edit committed notebook outputs.** They are the evidence trail.
* **A notebook that moves or gets superseded needs its record updated.** If the run that ships
  changes — a `_1m` sub-sample replaces the full-size run, a notebook is renamed or relocated — set
  the record's `notebook_path` to the new one (or run `data-foundry-curation sync-notebooks`) in the
  same change. A stale pointer sends every reader to a notebook that did not produce the data, and
  `tests/test_records_integrity.py` fails on it.
* If you record findings in the backlog record (`curation/records/<unique_name>.md`), follow the
  `AI (UNVERIFIED)` convention from `/triage-candidates` and preserve existing human `CC (…)` notes.
* Substance over volume: a short report with three real concerns beats thirteen paragraphs of
  "verified, looks good".
