---
name: knowledge-curation
description: "Reference knowledge, no workflow: how we decide whether a tabular dataset belongs in TabArena and how we curate it, independent of the tooling, as ranked rules with IDs and strengths. The principles and how to decide (rank, Must / Should / Weigh, tensions, exceptions, consistent judgement), ethics and scope, the use case and prediction point, leaks, IID / grouped / temporal splits, sources and duplicates, whether a task is trivial or too small, which metric scores it, cleaning and features; plus evidence and reading probes, the verification checklist, writing for the curator, and a general probe library. Load it when advising on any of these, or when a workflow skill (/screen-candidates, /review-screened-candidates, /add-dataset, /review-added-datasets) points to one of its files."
user-invocable: false
---

# Curation knowledge

This skill holds knowledge, not steps: it never acts on its own. The workflow skills say which file to read at which
step. Everything here would still hold with tooling other than Data Foundry; how this repository implements it is in
the sibling skill [knowledge-data-foundry](../knowledge-data-foundry/SKILL.md). The overview for people is the
[skills README](../README.md).

The files are ordered like a law book: an earlier part wins a conflict with a later one, and within a file an earlier
rule wins over a later one of the same strength. Every rule has an ID (`LEAK-3`) and a strength (Must, Should,
Weigh); cite them. Read [principles.md](references/principles.md) first.

| Part | Principle | File | IDs | Read it when |
|---|---|---|---|---|
| 0 | how to decide | [principles.md](references/principles.md) | P1-P7 | before any judgment: the ranking, strengths, how to decide, tensions, exceptions and amendments, consistent judgement, arguing a call |
| 1 | P1 ethics, P2 scope | [selection.md](references/selection.md) | `SEL` | screening or re-judging any record: scope rules, quick decision patterns, verdict values, the markers, the screening priority |
| 2 | P3 a real use case | [use_case.md](references/use_case.md) | `USE` | before choosing a target, a column, a filter or a split |
| 3 | P4 honest evaluation: leaks | [leak_checks.md](references/leak_checks.md) | `LEAK` | the data loads, or a column or dataset is suspected |
| 4 | P4 honest evaluation: splits | [splits.md](references/splits.md) | `SPLIT` | deciding or checking a split |
| 5 | P5 faithful, unique data | [provenance.md](references/provenance.md) | `PROV` | tracing a source or a duplicate, judging whether data is generated |
| 6 | P6 worth benchmarking | [task_probes.md](references/task_probes.md) | `TP` | before proposing `Trivial` or `Too Small`, or answering a task-probe flag |
| 6b | P6 worth benchmarking: the metric | [metrics.md](references/metrics.md) | `MET` | choosing or checking the metric a dataset declares: whose metric to trust, threshold metrics, cost matrices, the target's scale, matching the data to the metric, names and implementations |
| 7 | P7 the expert state | [cleaning_features.md](references/cleaning_features.md) | `CLEAN` | writing or reviewing the cleaning of a dataset |

Procedure, at every rank:

| File | IDs | Read it when |
|---|---|---|
| [evidence.md](references/evidence.md) | `EV` | weighing evidence, settling a disputed fact, reading a probe flag |
| [verification.md](references/verification.md) | | the last step of every workflow: the checklist and which stage runs which check |
| [writing.md](references/writing.md) | | writing anything the curator will read: comments, notes, issues, the judgment record, reports |

The general probe methods (leak, task, group, hidden-group and generated-data probes, as functions on a frame, a
target and splits) are in [scripts/](scripts/); the commands that run them on a Data Foundry dataset are in the sibling
skill.

## Keeping it current

A curator's decision that becomes a standing rule goes into the file of its topic in the same change: a new rule placed
by rank, or an amendment of an existing one under its ID, with the name and date and the case as a Cases row. An
exception for one dataset leaves the rule unchanged. The details, and which names and numbers must stay stable, are in
[principles.md](references/principles.md), "Exceptions and amendments" and "Keeping the rules current".
