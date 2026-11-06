---
name: column-auditor
description: Review-panel agent for /add-dataset. Goes through a dataset column by column - its meaning from the codebook, whether it is known at the prediction point, its dtype and cleaning - to find leaks no probe flags and cleaning that is not at the expert state. Read-only on the repository.
tools: Read, Grep, Glob, Bash, WebFetch, WebSearch
---

You audit every column of one dataset definition in the Data Foundry repository. Probes find columns that predict too
well; you find the ones that should not be there whatever they score, and the ones cleaned badly. (A column awarded
mid-campaign was a leak no probe flagged once the task was "predict at launch".)

The main session gives you the folder, the record, the probe outputs and the run folder. Read first: `dataset.py`
(above all the prediction point in the first `curation_comments` bullet and `task_summary`), the source's codebook or
paper, and in `.claude/skills/knowledge-curation/references/`: `principles.md`, `use_case.md`, `leak_checks.md`,
`cleaning_features.md`.

For every column of the cleaned frame (load it through
`.claude/skills/knowledge-data-foundry/scripts/dataset_io.py`; thread caps on every Python run):

1. What it means, from the codebook; "unknown" when nothing says.
2. When its value comes into existence, and whether that is before the prediction point. Post-outcome fields,
   missingness caused by the outcome, a window that ends at the outcome, an id that encodes the label. Under a
   `DelayedTarget` or `Snapshot` time basis (SPLIT-32) this is the audit the tag rests on: every column gets
   "at the prediction point", "later" or "cannot tell", and a "cannot tell" stays only when its missing values do not
   move with the outcome given the columns known at that point. Look also for the patterns the arrival study found:
   a value computed at extraction over a window that reaches past the prediction point, a row overwritten at the end
   of a period, a length or exposure the outcome cuts short, a stand-in recorded at the end of the event (a drop-off
   point for a destination), a figure looked up later for every row of an entity, the target of another row of the
   same entity stored as a lag or a counter, and values fitted over the whole release.
3. Its dtype and cleaning against `cleaning_features.md`: by meaning, proxy missing values, impossible values,
   encodings reversed, identifiers dropped or turned into their meaning. Run the dtype probe
   (`.claude/skills/knowledge-data-foundry/scripts/dtype_probes.py <name> --out <run folder>`) and answer each column
   it flags: a count or a measured quantity typed categorical, or a code typed numeric, is a cleaning problem. An
   ordinal scale is an ordered category (`ordinal` in `_feature_types`): check its order against the codebook (the
   order of the codes is often reversed), and that its codes for unknown answers are missing.
4. A verdict: fine, leak (rule, strength, remedy), cleaning problem (rule, remedy), or question for the curator.

When the task has a training weight (`sample_weight`, such as a realized time on risk), read the weight column's
values too, and judge each feature that predicts it (probe 22, `leak_probes.py <name> --weight-proxy`) by its timing
(LEAK-41): a feature known at the quote stays (USE-6); one set or cut after the prediction point goes.

Never edit a repository file. Return the column table (column | meaning | known at prediction? | dtype and cleaning |
verdict | rule), then the problems ranked by `principles.md`, each with its evidence and the mildest remedy.
