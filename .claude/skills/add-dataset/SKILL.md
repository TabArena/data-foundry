---
name: add-dataset
description: "Add a dataset to the TabArena v0.2 working copy and attack it before the curator sees it: builds the v2 folder (one dataset.py class and a generated README.md) from the curation record and the source, loops on dataset check and the leak, task and group probes until clean, runs the verification checklist, then a review panel of agents (claim auditor, column and split auditors, domain practitioner, a blind reviewer without our notes, precedent checker, an advocate and a critic, a mediator, an editor), and leaves the open questions, ranked, in the folder's REVIEW.md. Use for an accepted record (`Yes`), for a batch on a dashboard filter, or to re-check an existing folder (\"is X ready / leaky / correct?\"). The curator reviews the result with /review-added-datasets. v2 only; never builds a container."
argument-hint: "<unique_name | dashboard filter> [--panel full|focused]"
user-invocable: true
---

# Add a dataset (v2)

Stage 2 of the pipeline ([pipeline.md](../knowledge-data-foundry/references/pipeline.md)): turn an accepted record into
a v2 dataset folder in `datasets/_dev/tabarena-v0pt2/<unique_name>/`, then try to break it. The aim is a dataset the
curator can judge in minutes: a short summary first, every detail below it. Screening comes first
(`/screen-candidates`, then the curator's `Yes`); the curator's review comes after (`/review-added-datasets`).

$ARGUMENTS

Two modes:

* **A record without a folder:** every step below.
* **An existing folder** ("is X ready?", or after a change): a re-check. Skip steps 0-3 (the claim stays), run steps
  4-8, and update the existing `REVIEW.md` (new issues take the next free number).

## Knowledge used

| Step | Read |
|---|---|
| all | [principles.md](../knowledge-curation/references/principles.md): rank, strengths, the remedy ladder, the judgment record |
| 0 | [claims.md](../knowledge-data-foundry/references/claims.md), [records.md](../knowledge-data-foundry/references/records.md) (pointers); for a batch [agent_runs.md](../knowledge-data-foundry/references/agent_runs.md) |
| 1 | [use_case.md](../knowledge-curation/references/use_case.md), [provenance.md](../knowledge-curation/references/provenance.md), [metrics.md](../knowledge-curation/references/metrics.md) (MET-1 to MET-3) |
| 1-3 | [definitions.md](../knowledge-data-foundry/references/definitions.md): the folder, the class, the field mapping, the recipe, the split declarations, the reference definitions |
| 3 | [cleaning_features.md](../knowledge-curation/references/cleaning_features.md), [splits.md](../knowledge-curation/references/splits.md), [metrics.md](../knowledge-curation/references/metrics.md) (MET-11 to MET-13) and definitions.md, "Metrics" |
| 5 | [leak_checks.md](../knowledge-curation/references/leak_checks.md), [task_probes.md](../knowledge-curation/references/task_probes.md), [evidence.md](../knowledge-curation/references/evidence.md) (reading a probe), [checks_and_probes.md](../knowledge-data-foundry/references/checks_and_probes.md) |
| 6 | [verification.md](../knowledge-curation/references/verification.md) |
| 7 | [review_panel.md](references/review_panel.md) |
| 8 | [writing.md](../knowledge-curation/references/writing.md), [working_copy.md](../knowledge-data-foundry/references/working_copy.md) (`REVIEW.md`, CHANGELOG) |

## The one rule

You have not seen the data until it is downloaded. Pre-fill structure, never facts:

* anything you can derive from the record or a convention, fill in;
* anything that needs a look at the data, write as an ordered, commented step with a `# TODO(verify): ...` marker
  saying what to check, in the method where it belongs;
* never invent a column name, a class label, a leak or a horizon. `"TODO"` is a safe value in a free-text field; a
  plausible guess is not. `domain`, `source` and `problem_type` take fixed values, so pick the closest match and say so.

The markers are enforced: `meta_placeholder_left`, `definition_license_placeholder` and `definition_todo_left` are
errors, and `dataset build` refuses to save while any remains.

## Step 0: Gather inputs and claim

Read `curation/records/<unique_name>.md`: the front matter and the comments, above all the screening block (the
source, the use case, the regime, the risks). Verify its claims as you go instead of redoing its research; a
measurement on the data supersedes what screening read from the page. No record: stop and point to
`/screen-candidates`. Claim the records first, in the curator's name: `claims claim <names> --stage add --note
"add-dataset"` ([claims.md](../knowledge-data-foundry/references/claims.md)); it pushes the claim to the board and
writes `WIP (DF)` and `claimed_by` into the records. Never work on a dataset another curator holds: a name the command
skips is left out and reported.

A batch (several names or a dashboard filter) runs one `dataset-builder` agent per source unit for steps 0-6
([agent_runs.md](../knowledge-data-foundry/references/agent_runs.md)); the main session then runs the panel (step 7)
for each dataset, because subagents do not start subagents.

## Step 1: The source, the use case and the fields

Follow `source_links` to the first publication. Write the use case first, in `task_summary`: who uses the prediction,
when, the decision it informs, what one row is, what is predicted and what is known then. A dataset no decision fits
(`fit="none"`) is not added: it goes back as `No Good Target / Scientific Discovery`. Write the prediction point into
the first `curation_comments` bullet; every later choice is checked against it. Then map the fields (definitions.md,
"Field mapping"); for a grouped task note what one real-world prediction is and what is known about a new group.

Find the metric the source scored before falling back (MET-1): the competition's evaluation page (Kaggle's Evaluation
tab or the API's `evaluationMetric`, Zindi, DrivenData, a challenge page), the task description, the evaluation section
of the paper that defined the task (which may be later than the data). Start from the record's `Metric:` screening
line. Decide by MET-4 to MET-10 whether to keep it: a competition's metric, yes; a paper's only when it is one
deliberate choice; a threshold metric only with the threshold, k or cost matrix the source fixes. Then check on the
data that it fits (MET-2: its unit exists, every input it needs ships and the test folds hold it, the task still means
what the source's meant) and that the target is on the scale the source scored (MET-3). Note where you looked, for the
reason of a fallback.

## Step 2: Scaffold

Read the closest reference definition in full (definitions.md, "Reference definitions"), then:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset new <unique_name> --root datasets/_dev/tabarena-v0pt2
```

It copies `datasets/_template/dataset.py`, names the class and pre-fills year, link, problem type,
domain and source from the record.

## Step 3: Fill `dataset.py`

1. The attributes: `task_summary` first, then every field of Step 1; `"TODO"` where the data must be seen first.
2. `_load_raw(self, raw_dir)`: reading only (and a join along the source's own keys). It is cached.
3. `_clean(self, raw)`: the recipe as ordered, commented steps with `TODO(verify)` markers, and
   `_feature_types(self, df)` for the dtypes.
4. The regime: nothing for IID, `grouping = Grouping(...)` or `temporal = Temporal(...)` with a `splits_comment`
   saying why this window (and any gap, sub-sampling or trimming).
5. The metric: `metric = Metric.source(name, original=..., reference=..., params=..., inputs=...)`,
   `Metric.stand_in(name, original=..., reason=..., reference=...)` or `Metric.fallback(reason=<where we looked, and
   which source metric was rejected and why>)` (definitions.md, "Field mapping", `metric`; MET-11). A standard name
   for a standard metric, a general one for a custom metric (MET-12). Every column the metric reads (a group, a time,
   a weight) stays in the frame and is declared in `scoring_columns = (ScoringColumn(column=..., role=..., used_by=...,
   description=...),)`; it is never a feature. A custom metric that is not yet in `METRICS` is added to
   `src/data_foundry/v2/metrics.py` in the same change (MET-13, definitions.md, "Metrics"): the fastest well-tested
   implementation (scikit-learn or scipy, otherwise vectorised numpy; for a competition whose official code is slow,
   look for the faster versions in its Kaggle discussions and notebooks and check them), tested in
   `tests/test_v2_metrics_custom.py` to equal the official code on random inputs, on one hand-computed case, and timed
   on 1M rows. Never `Metric.local` in the working copy.
6. `accepted_check_warnings` stays empty: the curator fills it once the warnings are known, one reason per slug.
7. `_decisions` and `_extra_checks` only when there is something to show or test.

Then point the record at the definition:
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
data (`ds = workbench()` in a scratch notebook or script, never committed), re-run, read the README diff. Stop when there are no errors and every warning is fixed or
proposed for acceptance with a reason. Run `dataset check` again after every `ruff --fix`.

Then run the leak probes and the task probes, the group probes for a grouped task and the hidden-group probe for an
IID one ([checks_and_probes.md](../knowledge-data-foundry/references/checks_and_probes.md)). Read every flag by
[evidence.md](../knowledge-curation/references/evidence.md), "Reading a probe": the highest-ranked reading first. A
leak gets the mildest remedy that removes it (drop, lag, filter, re-split) with the deciding number in a bullet; a
task-probe flag is answered by the rules of [task_probes.md](../knowledge-curation/references/task_probes.md).

## Step 6: The checklist

Run every check of [verification.md](../knowledge-curation/references/verification.md) marked "add", in its rank order,
with evidence and the rule IDs. The "Metric" row checks the declared spec against the source: open the `reference`
and confirm it names this metric (the `original`) with these params; for a fallback, that the reason says where we
looked; that the `task_metric_*` checks are clean (the metric computes on every fold, its inputs are scoring columns,
not features); and that a custom metric's tests against the official code pass. Fix what can be fixed now (re-run `dataset check` after each fix); everything else
becomes a draft issue for step 8.

## Step 7: The review panel

Attack the finished definition with the agents of [review_panel.md](references/review_panel.md): the evidence agents
in parallel, then the advocate and the critic with one rebuttal each, then the mediator. `--panel full` (all agents)
is the default for a new folder; `--panel focused` (the claim auditor, the auditors the change touches, the mediator
and the editor) for a re-check after a small change. Say which tier ran.

## Step 8: Synthesis and hand-over

1. Apply what the panel settled that needs no decision (a refuted claim with an obvious fix, a missing note), re-run
   `dataset check` and the probes it touches.
2. Write `REVIEW.md` ([review file format](../review-added-datasets/references/review_file_format.md)): the outcome as a
   judgment record ([principles.md](../knowledge-curation/references/principles.md)), the main points, the record fields
   that disagree with the definition, the issues in rank order (validity first, Must first), each with the rule ID,
   the evidence and the decision needed ([writing.md](../knowledge-curation/references/writing.md)), and the
   `**Review panel:**` block with each agent's full report.
3. The `review-editor` agent reads the draft as the curator would; apply its fixes.
4. Add a dated CHANGELOG entry for the new folder, and an `**Assessment (AI, <date>):**` line in the record. Never
   build: a build is the curator's call ([rebuild.md](../knowledge-data-foundry/references/rebuild.md)).
5. Set the record's `priority` again from what was measured, so the review page puts the most important datasets
   first ([selection.md](../knowledge-curation/references/selection.md), "Priority"): `priority_factors.py <name>`
   (in `knowledge-data-foundry/scripts/`) gives the gap and the shape; judge the use case, the source and the risk
   from the source and the open issues (the recommendation not to ship is a risk). End the assessment line with
   `Priority <n>: gap ±, use case ±, source ±, shape ±, risk ± (<the reason for each sign that is not obvious>).`

Report: the folder and its outcome in one line; the panel's recommendation and the disputed points; the issues for the
curator by rank; every `TODO(verify)` left, grouped by method; what could not be checked; next steps with paths filled
in (`/review-added-datasets`, with `--names` for a batch).
