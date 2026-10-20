---
name: screen-candidates
description: "Screen candidate datasets: a quick first pass from the source link and the web, without building anything. Fills each curation record with what the next stage needs (first publication, the data as published, the use case, the likely split, papers, siblings and duplicates, risks), rejects the obvious cases fast (unethical, generated, non-tabular, forecasting, duplicate, unknown source, no use case) and gives every other record a priority from 1 to 5 for the curator's review. Use when the curator shares a new dataset link, wants the backlog screened or prioritized, or asks to check a record that has no dataset folder yet (\"check X\", \"what did I miss on X\"). The curator verifies the result with /review-screened-candidates."
argument-hint: "[<unique_name>,... | <dashboard filter> | <source link>]"
user-invocable: true
---

# Screen candidates

Stage 1 of the pipeline ([pipeline.md](../knowledge-data-foundry/references/pipeline.md)): a quick pass that decides
which candidates are worth a curator's time, and prepares their records so `/add-dataset` does not redo the research.
Nothing is downloaded beyond a preview and nothing is built. The curator checks the result with
`/review-screened-candidates`; only the curator sets a plain `Yes`.

**Input:** record names, a dashboard filter, or source links (a link without a record gets a new record). Without an
argument: every record without a verdict. A single name gets the deep pass (below).

$ARGUMENTS

## Knowledge used

| Step | Read |
|---|---|
| all | [principles.md](../knowledge-curation/references/principles.md): the ranking, strengths and the judgment record |
| 3 | [provenance.md](../knowledge-curation/references/provenance.md), [use_case.md](../knowledge-curation/references/use_case.md), [splits.md](../knowledge-curation/references/splits.md), [sources_access.md](../knowledge-data-foundry/references/sources_access.md) |
| 4 | [selection.md](../knowledge-curation/references/selection.md) (the scope rules and patterns, the markers), [evidence.md](../knowledge-curation/references/evidence.md) |
| 5 | [selection.md](../knowledge-curation/references/selection.md), "Screening priority" |
| 6 | [records.md](../knowledge-data-foundry/references/records.md): the store API, the `AI (UNVERIFIED)` convention, the screening block |
| 7 | [verification.md](../knowledge-curation/references/verification.md): the checks marked "screen"; [writing.md](../knowledge-curation/references/writing.md) |

## Step 1: List the records

Resolve the input to records under `curation/records/`; create a record for a new link (`unique_name` in snake_case,
`name`, the link in `source_links`) through the store API. Skip every record claimed by another curator. A record that
already has a screening block is screened again only when the curator asks.

A batch runs on the `candidate-screener` agent, about 10 records per agent, all in one message; the main session keeps
the coverage snapshot, the reject check and the report. Mind the limits in
[agent_runs.md](../knowledge-data-foundry/references/agent_runs.md).

## Step 2: The coverage snapshot

```bash
.venv/bin/python .claude/skills/knowledge-data-foundry/scripts/benchmark_coverage.py
```

Once per run: the accepted datasets per domain, problem type, regime and source, with the thin values marked. It feeds
the "gap" factor of the priority.

## Step 3: Research from the context

Follow the start link to the first publication and read around it on the web. A data preview, a column list or a file
listing is fine; nothing is built. Collect, with links:

* the first publication, who published it and the year;
* the data as published: rows, columns, the target, the tables and how they join;
* the original task and who solved it (competition pages and top solutions are claims, read them as such);
* the use case: who acts, when, on which decision, and what is known then; how closely the data mirrors it;
* the likely regime (IID, grouped, temporal) and why;
* the paper that published the data and papers that used it;
* sibling records and duplicates (`grep -il` over `curation/records/` by name, source and links), and external
  collections that carry it;
* risks for the next stage: columns that may not be known at prediction time, joins, an unclear target.

**The deep pass** (a single name, or "check X" on a record without a folder): read the paper's text and quote the
load-bearing sentence by section, read the Kaggle discussions and notebooks with the `kaggle` command line, read the
siblings' decisions and follow their precedent, and download the data when one fact decides the verdict (a
duplicate by rows, a deterministic target). Say which checks were skipped.

## Step 4: Fast reject, or not

Walk the Must rules of parts 1, 2 and 5 that the context can decide: ethics, scope (non-tabular, generated or
simulated, forecasting, CTR or ranking, survey and discovery tables, labels the task cannot have), a use case no
decision fits, a duplicate by provenance, a source that cannot be traced. When one clearly fails from the source, the
verdict is `No` with its marker and the rule ID, and there is no priority.

Before a reject is written, the `reject-checker` agent tries to refute it (all rejects of a batch in one message). A
reject it refutes, or one that rests on a reading rather than on the source's own words, is not a fast reject: give
the record a priority and list the doubt. A rejected dataset is rarely looked at again; a wrong `No` costs more than a
low priority.

## Step 5: Verdict and priority

Every other record gets `TBD -> Yes` (or `TBD -> 2nd Tier` when it is plausible but secondary) and a priority from 1
(look at it last) to 5 (look at it first), by the screening factors of
[selection.md](../knowledge-curation/references/selection.md): one point to start, plus one each for a gap in the
benchmark, a clear use case, a strong source and a good shape; minus one for a known risk; never below 1. Never set a
plain `Yes`: that is the curator's call.

## Step 6: Write the dossier

Through the store API, right after reloading the record ([records.md](../knowledge-data-foundry/references/records.md)):
the verified links in `source_links`, empty metadata only where the source states it, `priority`, `AI (UNVERIFIED)`
in `checked_by`, `AI-Filled (Verify)` in `tags`, and at the top of the comments the disclaimer followed by the
screening block, every existing note kept below it:

```markdown
**Screening (AI, 2026-10-20):** `TBD -> Yes`, priority 4: <why, one line>.
- Source: <first publication, who, year>; as published: <rows x columns, target, tables>.
- Use case: <actor, moment, decision>; fit <direct | approximate>; regime <IID | grouped | temporal> because <...>.
- Siblings and duplicates: <records checked, and what they decided>; external collections: <...>.
- Papers and pages: <the paper that published the data, papers that used it, competition, top solutions>.
- Risks for /add-dataset: <columns to check, joins, the target> (rule IDs).
- Priority: gap +, use case +, source +, shape - (<reason>).
```

A rejected record's block starts with the verdict and the rule (`` `No` (`Duplicate`, PROV-…): ... ``) and has no
priority line. For a record that already has a curator's verdict, write an `**Assessment (AI, <date>):**` instead and
leave the fields alone.

## Step 7: Check and report

Run the checks of [verification.md](../knowledge-curation/references/verification.md) marked "screen" for every record
and put the decisive evidence into its block. Then
`.venv/bin/python -m data_foundry.curation.cli validate`, `git add` every new file under `curation/`, and report:

* one table: record, verdict, priority, the one-line reason, the rule for a reject;
* what could not be checked and why;
* the next step: `/review-screened-candidates` (the dashboard's Screening queue), and the uncommitted changes.
