---
name: add-dataset
description: Add a curated dataset to data-foundry as a v2 dataset folder (one `dataset.py` class + `explore.ipynb` + a generated `README.md`). Use this whenever a triaged candidate that came out `Yes` should be processed, or the user says "add / process / curate / scaffold dataset X", for one record or a batch (a dashboard filter). Reads the curation record, scaffolds the folder with `dataset new`, fills the metadata and the preprocessing from the source, loops on `dataset check` and the probes until clean, verifies the result, and leaves the open questions for the curator in the folder's `REVIEW.md`. v2 only: never writes a v1 curation notebook.
argument-hint: <unique_name | dashboard filter>
user-invocable: true
---

# Add a dataset (v2)

Turn an accepted record into a v2 dataset folder in the TabArena v0.2 working copy,
`datasets/_dev/tabarena-v0pt2/<unique_name>/`. The triage comes first (`/triage-candidates`: the record is a `Yes`);
the curator's review comes after (`/review-added-datasets`).

$ARGUMENTS

## Knowledge used

| Step | Read |
|---|---|
| 0 | [records.md](../knowledge-data-foundry/references/records.md) (claims, pointers); for a batch [agent_runs.md](../knowledge-data-foundry/references/agent_runs.md) |
| 1 | [use_case.md](../knowledge-curation/references/use_case.md), [provenance.md](../knowledge-curation/references/provenance.md) |
| 1-3 | [definitions.md](../knowledge-data-foundry/references/definitions.md): the folder, the class, the base class, the field mapping, the recipe, the split declarations, the reference definitions |
| 3 | [cleaning_features.md](../knowledge-curation/references/cleaning_features.md), [splits.md](../knowledge-curation/references/splits.md) |
| 5 | [leak_checks.md](../knowledge-curation/references/leak_checks.md), [task_probes.md](../knowledge-curation/references/task_probes.md), [checks_and_probes.md](../knowledge-data-foundry/references/checks_and_probes.md) |
| 6 | [verification.md](../knowledge-curation/references/verification.md), [writing.md](../knowledge-curation/references/writing.md), [working_copy.md](../knowledge-data-foundry/references/working_copy.md) (`REVIEW.md`, CHANGELOG) |

## The one rule

You have not seen the data until it is downloaded. Pre-fill structure, never facts:

* anything you can derive from the record or a convention, fill in;
* anything that needs a look at the data, write as an ordered, commented step with a `# TODO(verify): ...` marker
  saying what to check, in the method where it belongs;
* never invent a column name, a class label, a leak or a horizon. `"TODO"` is a safe value in a free-text field; a
  plausible guess is not. `domain`, `source` and `problem_type` take fixed values, so pick the closest match and say so.

The markers are enforced: `meta_placeholder_left`, `definition_license_placeholder` and `definition_todo_left` are
errors, and `dataset build` refuses to save while any remains.

## Step 0: Gather inputs

Read `curation/records/<unique_name>.md`: the front matter (name, source, year, domain, split, problem type, links,
data state) and the comments (the provenance and duplicate checks already done; do not redo settled work). Ask only
for what is missing or contradictory. No record: stop and point to `/triage-candidates`. Never work on a record
another curator has claimed; the records you take get `WIP (DF)` and the curator's name in `claimed_by` first, and the
claim goes to `main` in its own small PR.

A batch (several names or a dashboard filter) runs as [agent_runs.md](../knowledge-data-foundry/references/agent_runs.md)
describes: units per source, one agent working and a second verifying each unit.

## Step 1: The source, the use case and the fields

Follow `source_links` to the first publication. Write the use case first, in `task_summary`: who uses the prediction,
when, the decision it informs, what one row is, what is predicted and what is known then. A dataset no decision fits
(`fit="none"`) is not added: it goes back to triage as `No Good Target / Scientific Discovery`. Write the prediction
point into the first `curation_comments` bullet; every later choice is checked against it. Then map the fields
(definitions.md, "Field mapping"); for a grouped task note what one real-world prediction is and what is known about a
new group.

## Step 2: Scaffold

Read the closest reference definition in full (definitions.md, "Reference definitions"), then:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset new <unique_name> --root datasets/_dev/tabarena-v0pt2
```

It copies `datasets/_template/{dataset.py,explore.ipynb}`, names the class and pre-fills year, link, problem type,
domain and source from the record.

## Step 3: Fill `dataset.py`

1. The attributes: `task_summary` first, then every field of Step 1; `"TODO"` where the data must be seen first.
2. `_load_raw(self, raw_dir)`: reading only (and a join along the source's own keys). It is cached.
3. `_clean(self, raw)`: the recipe as ordered, commented steps with `TODO(verify)` markers, and
   `_feature_types(self, df)` for the dtypes.
4. The regime: nothing for IID, `grouping = Grouping(...)` or `temporal = Temporal(...)` with a `splits_comment`
   saying why this window (and any gap, sub-sampling or trimming).
5. `accepted_check_warnings` stays empty: the curator fills it once the warnings are known, one reason per slug.
6. `_decisions` and `_extra_checks` only when there is something to show or test.

Leave `explore.ipynb` as the template made it; it is the curator's space. Then point the record at the definition:
`.venv/bin/python -m data_foundry.curation.cli sync-notebooks` (`--check` must stay clean).

## Step 4: Validate the scaffold

```bash
.venv/bin/python -m data_foundry.curation.cli dataset list --root datasets/_dev/tabarena-v0pt2
uvx ruff@0.15.15 check --fix datasets/_dev/tabarena-v0pt2/<unique_name>/dataset.py && uvx ruff@0.15.15 format datasets/_dev/tabarena-v0pt2/<unique_name>/dataset.py
```

`dataset list` exits non-zero when a class does not import or validate; fix it before going on.

## Step 5: The loop (when the raw data is present)

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/<unique_name>
```

runs the pipeline, the checks and `_decisions` without saving, and writes `README.md`. Resolve the TODOs, look at the
data in `explore.ipynb`, re-run, read the README diff. Stop when there are no errors and every warning is fixed or
proposed for acceptance with a reason. Run `dataset check` again after every `ruff --fix`.

Then run the leak probes and the task probes, and the group probes for a grouped task, the hidden-group probe for an
IID one ([checks_and_probes.md](../knowledge-data-foundry/references/checks_and_probes.md)). A feature that comes
close to the full model, a missing indicator that predicts the label, copies across the split or a pure-value warning
each need a decision (drop, lag, filter, re-split, keep on purpose) with the deciding number in a bullet. Answer each
task-probe flag by the rules of [task_probes.md](../knowledge-curation/references/task_probes.md).

## Step 6: Verify and hand over

Run every check of [verification.md](../knowledge-curation/references/verification.md) marked "add", with evidence;
in a batch the second agent does it and the first applies or rejects each finding. Write what needs the curator's
decision into the folder's `REVIEW.md`, phrased as [writing.md](../knowledge-curation/references/writing.md) says, and
add a dated CHANGELOG entry for the new folder. Never build: a build is the curator's call
([working_copy.md](../knowledge-data-foundry/references/working_copy.md)).

Report: the folder and a summary of the attributes; every `TODO(verify)` left, grouped by method; the mapping choices
that were ambiguous and the traps you flagged; the verification verdict; and next steps with paths filled in (for a
batch: the review page, `/review-added-datasets`).
