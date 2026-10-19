---
name: knowledge-curation
description: "Reference knowledge, no workflow: how we decide whether a tabular dataset belongs in TabArena and how we curate it, independent of the tooling. Selection criteria and verdicts, the use case and prediction point, IID / grouped / temporal splits, leaks, cleaning and features, whether a task is trivial or too small, sources and duplicates, the verification checklist, and how to write for the curator; plus a general probe library. Load it when advising on any of these, or when a workflow skill (/triage-candidates, /check-candidate, /add-dataset, /review-added-datasets) points to one of its files."
user-invocable: false
---

# Curation knowledge

This skill holds knowledge, not steps: it never acts on its own. The workflow skills (`/triage-candidates`,
`/check-candidate`, `/add-dataset`, `/review-added-datasets`, `/rebuild-working-copy`) say which file to read at which
step. Everything here would still hold with tooling other than Data Foundry; how this repository implements it is in
the sibling skill [knowledge-data-foundry](../knowledge-data-foundry/SKILL.md).

| Topic | File | Read it when |
|---|---|---|
| What belongs in the benchmark: scope, the five criteria, quick decision patterns, verdict values, markers, arguing a call | [selection.md](references/selection.md) | triaging or re-judging any record |
| The use case, its fit, the prediction point, the real-world target, inputs known at prediction time, recurring entities and the cold start | [use_case.md](references/use_case.md) | before choosing a target, a column, a filter or a split |
| IID, grouped and temporal splits: forecasting vs temporal tasks, windows, gaps and late labels, training history, group ids, hidden groups | [splits.md](references/splits.md) | deciding or checking a split |
| Leaks: probes, mechanisms and what we did, what is not a leak, copies across the split, lessons from first suggestions | [leak_checks.md](references/leak_checks.md) | the data loads, or a column or dataset is suspected |
| Cleaning to an expert state, missing and impossible values, encodings, dtypes, the target, which features we build, width | [cleaning_features.md](references/cleaning_features.md) | writing or reviewing the cleaning of a dataset |
| Whether a task is worth benchmarking: the rules for the task-probe flags, forecasting-like tasks, cases, hidden-group and generated-data probes | [task_probes.md](references/task_probes.md) | before proposing `Trivial` or `Too Small`, or answering a probe flag |
| Sources and year, duplicates, third-party copies, repairing from the origin, citing papers, competition pages, generated data | [provenance.md](references/provenance.md) | tracing a source or a duplicate |
| The verification checklist and which stage runs which check | [verification.md](references/verification.md) | the last step of every workflow |
| Record comments, dataset notes, the task summary, issues for the curator, reporting back | [writing.md](references/writing.md) | writing anything the curator will read |

The general probe methods (leak, task, group, hidden-group and generated-data probes, as functions on a frame, a
target and splits) are in [scripts/](scripts/); the commands that run them on a Data Foundry dataset are in the sibling
skill.

## Keeping it current

* A curator's decision that becomes a standing rule goes into the file of its topic in the same change, with the name
  and date (`Lennart, 2026-10-19`), and the case that prompted it as the example.
* One rule lives in one file; other files link to it. When two statements disagree, the newer decision wins, and the
  older text is corrected rather than left next to it.
* Definitions and records cite `task_probes.md` by its rule numbers and `leak_checks.md` by name: keep both names and
  the rule numbers stable.
