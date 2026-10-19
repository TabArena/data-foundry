---
name: check-candidate
description: Independent, cited second opinion on one dataset at any stage, from a backlog record to a finished v2 definition. Traces the original source, answers the open questions in the record's comments, checks siblings and duplicates, runs the leak, task and group probes when the data loads, and, for a dataset with a `dataset.py`, the full verification (dataset check, probes, the verification checklist). Writes the evidence and a recommended verdict into the record. Use when the curator says "check X", "dive into X", "what did I miss on X", "your thoughts on X", "is X ready / correct / leaky?", when a record has open questions or a verdict inconsistent with a sibling, or when a dataset is suspected of a leak.
argument-hint: <unique_name>
user-invocable: true
---

# Check one dataset

Check one dataset the curator is looking at: trace what the data really is, find what the record or the definition
misses, and report a second opinion with citations.

**Input:** a record `unique_name` (a display name or a source link is fine; resolve it to the record first).

$ARGUMENTS

## Knowledge used

| Step | Read |
|---|---|
| all | [selection.md](../knowledge-curation/references/selection.md): the criteria this check applies |
| 1, 6 | [records.md](../knowledge-data-foundry/references/records.md): reloading, comment lines, pointers |
| 3 | [provenance.md](../knowledge-curation/references/provenance.md), [sources_access.md](../knowledge-data-foundry/references/sources_access.md) |
| 4 | [use_case.md](../knowledge-curation/references/use_case.md), [splits.md](../knowledge-curation/references/splits.md), [leak_checks.md](../knowledge-curation/references/leak_checks.md), [task_probes.md](../knowledge-curation/references/task_probes.md), [cleaning_features.md](../knowledge-curation/references/cleaning_features.md) |
| 4, 5 | [checks_and_probes.md](../knowledge-data-foundry/references/checks_and_probes.md): the commands |
| 5 | [verification.md](../knowledge-curation/references/verification.md), [definitions.md](../knowledge-data-foundry/references/definitions.md) |
| 7 | [writing.md](../knowledge-curation/references/writing.md) |

## Protocol

Do every step; skip one only when an earlier step settles the verdict, and say so.

1. **Reload the record** and read its comments for what they mean. Write down every open question they contain:
   those are what to answer, not a report of everything you find. Note whether it has a `v2_path` (a definition).
2. **Siblings.** List records with a similar name, the same source or the same external collection (`grep -il` over
   `curation/records/`), and read their verdicts and comments: the team's precedent decides consistency
   (`hypertension` and `public_health_ins` for TableShift re-cuts, `higgs` for simulated physics, the `Image` list for
   descriptors computed from pictures).
3. **Trace the original source.** Follow every link to where the data first came from and read the paper's text, not
   the abstract; cite by section with the load-bearing sentence quoted. A paywalled paper: search briefly for a free
   copy, then ask the curator for the PDF with the exact query. Read competition discussions and notebooks with the
   `kaggle` command line, and say when that check was skipped.
4. **Answer the criteria with evidence.** What the data physically is (measured, computed, simulated, derived from an
   image or a signal); the original task and what solved it (the model families at the top of a leaderboard are a
   modality signal); the use case and the prediction point; the split the task design requires; the real-world
   target and how the label was built; the size after cleaning; ethics; duplicates by provenance. Under class
   imbalance use ROC AUC or log loss against the class prior and fit a quick LightGBM on the prediction-time features
   when the data loads. A licence is a one-line note, never a reason. If the source cannot be traced or the data looks
   too clean, run the generated-data tests. When the data loads, run the leak probes; when the question is whether a
   task is empty, trivial or too small, the task probes and their rules.
5. **A dataset with a definition, or the question "is it ready?":** run the full verification. `dataset check` on
   its folder, the probes that apply (leak and task always, group for a grouped task, hidden groups for an IID one,
   generated data when suspected), every check of [verification.md](../knowledge-curation/references/verification.md)
   with its evidence, and the Data Foundry checks (pointer, template, README in step). Never build.
6. **Write only substance into the record.** Add the source links you verified and one dated comment with what the
   data is, the decisive facts and the recommendation. Fill empty optional metadata only where the evidence is clear.
   Reload right before saving. The curator stated the verdict: apply it, as their `CC (YYYY-MM-DD, Name):` line. They
   have not: leave the verdict and markers alone and write `**Assessment (AI, YYYY-MM-DD):** recommend ...; the curator
   has the call.` Issues about a definition that need the curator's decision go into its folder's `REVIEW.md`
   ([working_copy.md](../knowledge-data-foundry/references/working_copy.md)).
7. **Report back.** The recommended verdict in one sentence; then, with citations, what was missed or wrong, what was
   right and what could not be checked; for a definition the verification report of
   [verification.md](../knowledge-curation/references/verification.md). Counts and scores go in a short table. Then what
   you changed in which files.
8. **Leave the tree clean.** `git add` any new file under `curation/`, then
   `.venv/bin/python -m data_foundry.curation.cli validate` and `.venv/bin/python -m pytest -q tests/test_records_integrity.py`.
