---
name: screen-candidates
description: "Screen candidate datasets: a quick first pass from the source link and the web, without building anything. Fills each curation record with what the next stage needs (first publication, the data as published, the use case, the likely split, papers, siblings and duplicates, risks), rejects the obvious cases fast (unethical, generated, non-tabular, forecasting, duplicate, unknown source, no use case) and gives every other record a priority from 1 to 5 for the curator's review. On request it also finds new candidates: better data (a larger or newer public dataset of the same task) for existing records, screened as new links. Use when the curator shares a new dataset link, wants the backlog screened or prioritized, asks to check a record that has no dataset folder yet (\"check X\", \"what did I miss on X\"), or wants better data found for existing records (\"better data\", the records tagged Search for better data, or all). The curator verifies the result with /review-screened-candidates."
argument-hint: "[<unique_name>,... | <dashboard filter> | <source link> | better data [<names> | <filter> | all]]"
user-invocable: true
---

# Screen candidates

Stage 1 of the pipeline ([pipeline.md](../knowledge-data-foundry/references/pipeline.md)): a quick pass that decides
which candidates are worth a curator's time, and prepares their records so `/add-dataset` does not redo the research.
Nothing is downloaded beyond a preview and nothing is built. The curator checks the result with
`/review-screened-candidates`; only the curator sets a plain `Yes`.

**Input:** record names, a dashboard filter, or source links (a link without a record gets a new record). Without an
argument: every record without a verdict. A single name gets the deep pass (below). `better data`, with names, a
filter, `all` or nothing: search existing records for a larger or newer dataset of the same task, and screen the hits
as new links ("Search for better data", below).

$ARGUMENTS

## Knowledge used

| Step | Read |
|---|---|
| all | [principles.md](../knowledge-curation/references/principles.md): the ranking, strengths and the judgment record |
| better data | [selection.md](../knowledge-curation/references/selection.md), "Small or dated, and the task is still done today"; [provenance.md](../knowledge-curation/references/provenance.md) (PROV-4, PROV-6); [use_case.md](../knowledge-curation/references/use_case.md) |
| 3 | [provenance.md](../knowledge-curation/references/provenance.md), [use_case.md](../knowledge-curation/references/use_case.md), [splits.md](../knowledge-curation/references/splits.md), [metrics.md](../knowledge-curation/references/metrics.md) (MET-1, MET-4 to MET-7), [sources_access.md](../knowledge-data-foundry/references/sources_access.md) |
| 4 | [selection.md](../knowledge-curation/references/selection.md) (the scope rules and patterns, the markers), [evidence.md](../knowledge-curation/references/evidence.md) |
| 5 | [selection.md](../knowledge-curation/references/selection.md), "Priority" |
| 6 | [records.md](../knowledge-data-foundry/references/records.md): the store API, the `AI (UNVERIFIED)` convention, the screening block |
| 7 | [verification.md](../knowledge-curation/references/verification.md): the checks marked "screen"; [writing.md](../knowledge-curation/references/writing.md) |

## Search for better data (on request)

Only when the input starts with `better data`; a screening never searches on its own. It looks for new candidates: a
larger or newer public dataset of the same task as a record we already have. Its hits go through steps 1 to 7 like
any new link.

**Which records.** The names or the filter given. `better data` alone: the records tagged `Search for better data`,
the curator's mark for this search. `better data all`: every record whose task is in scope, small and dated ones first
(`Tiny Data`, `Too Small`, `Outdated`, `Not Representative`, a classic UCI or StatLib set). Skip a record rejected for
its task (ethics, scope, no use case): other data does not fix that. Search a `Duplicate` through its original. Before
a run over more than about 50 records, say how many records and agents it takes, and ask.

**Same task, better data.** The same target (or the same quantity measured better) and use case, with features of the
same kind known at the prediction point; they need not match column for column. Better is larger or newer, ideally
both. Look at the old data's publisher (a later release or survey wave), the papers that cite it and newer studies of
the task, government surveys and registries, competitions and the usual repositories. Preview only, as in step 3.

**Run.** The `data-scout` agent, about 10 records per agent, all in one message. It writes nothing and returns per
record the hits (link, publisher, year, rows as published, why the task is the same, what it adds) or where it looked.
Then the main session:

* drops a hit that already has a record (`grep -il` over `curation/records/` by name and link) and reports it;
* merges a hit that several records found;
* gives every other hit a record (step 1) and a screening (steps 2 to 7). A hit from another source is its own record,
  not a `Duplicate` (PROV-4); a newer release of the same source is a version (PROV-6), and the curator decides which
  one enters. The siblings line of the screening block names the old record and what the hit adds.

**The old record** (claimed for the write, released after; one another curator holds is skipped and listed) gets one
line in its comments: ``**Better data (AI, <date>):** `<new_record>`: <what it adds>; screened: <verdict, priority>.``
A record tagged `Search for better data` gets the line without a hit too: none found, and where we looked. Nothing
else changes: the verdict, markers, priority and tags stay, the tag until the curator removes it, and the record goes
into no queue. Precedent: `body_density_prediction` (252 men, 1985) → NHANES DXA body fat (21,768 people).

**Report**, with step 7's: per old record, the hits with their new records, verdicts and priorities; the hits that
already had a record; how many records were searched without a hit.

## Step 1: List the records

Resolve the input to records under `curation/records/`; create a record for a new link (`unique_name` in snake_case,
`name`, the link in `source_links`) through the store API. Claim the records for the run (`claims claim <names>
--stage triage --note "screening"`, [claims.md](../knowledge-data-foundry/references/claims.md)) and skip every one
the command skips: another curator holds it. Release them when the screening is written (`claims release <names>`).
A record that already has a screening block is screened again only when the curator asks.

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
* the metric the source scored (MET-1): the competition's evaluation page (Kaggle: the Evaluation tab, or the API's
  `evaluationMetric` via `uvx kaggle==2.2.2 competitions list -s <slug>`; Zindi, DrivenData and challenge pages state
  it), the task description, or the evaluation section of the paper that defined the task. Note whether it is a
  deliberate choice (a leaderboard metric, MET-4; a paper's one ranked criterion, MET-5) or one of several reported,
  and for a threshold metric whether the source fixes the threshold, k or cost matrix (MET-6, MET-7). Note any extra
  inputs it needs (a group such as a patient or an era, a time, a weight) and whether they ship. When nothing is
  found, say where you looked;
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
- Metric: <the source's metric and where it is defined (link, section)>; <deliberate | one of several | habit>;
  inputs <none | the columns it needs, and whether they ship> (MET-1, MET-5, MET-6). Or: none found (<where we
  looked>), so the fallback.
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
