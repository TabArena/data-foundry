---
name: triage-candidates
description: Triage candidate datasets in the curation backlog (`curation/records/`). Starts the local curation dashboard, advises on whether a dataset belongs in the benchmark, which split it needs and how to process it, and drafts provisional verdicts for untriaged records under the `AI (UNVERIFIED)` convention. Use when the user wants to open the dashboard, work the backlog, add or edit a candidate record, or asks whether a dataset belongs in the benchmark. The knowledge it applies is in the knowledge-curation and knowledge-data-foundry skills.
user-invocable: true
---

# Triage candidates

Start the dashboard and help the curator decide which candidates belong in the benchmark. Triage is the first step of
the pipeline: AI triage here, the curator's check of it in the dashboard, `/add-dataset` for the accepted records, and
the curator's review of what was added on the page `/review-added-datasets` builds.

Other requests go elsewhere: an independent deep check of one record, or "is X ready / leaky?", is `/check-candidate`;
processing a decided record into a v2 definition is `/add-dataset`.

## Knowledge used

| Step | Read |
|---|---|
| 1 | [dashboard.md](../knowledge-data-foundry/references/dashboard.md) |
| 2, 3 | [selection.md](../knowledge-curation/references/selection.md) in full, before advising on any record |
| 2, 3 | as the question needs: [use_case.md](../knowledge-curation/references/use_case.md), [splits.md](../knowledge-curation/references/splits.md), [provenance.md](../knowledge-curation/references/provenance.md), [leak_checks.md](../knowledge-curation/references/leak_checks.md) (before calling a column or a dataset leaky), [task_probes.md](../knowledge-curation/references/task_probes.md) (before proposing `Trivial` or `Too Small`) |
| 3, 4 | [records.md](../knowledge-data-foundry/references/records.md): editing, comment lines, the `AI (UNVERIFIED)` convention, claims |
| 4 | [verification.md](../knowledge-curation/references/verification.md): the checks marked "triage"; [writing.md](../knowledge-curation/references/writing.md) |

## Step 1: Start the dashboard

```bash
.venv/bin/python -m data_foundry.curation.cli serve            # http://127.0.0.1:8765
```

Run it in the background and point the curator at http://127.0.0.1:8765. Records saved through the store API show up
in the open tab within seconds; the Guidelines button opens the two knowledge skills.

## Step 2: Advise

Answer from the knowledge files, citing the rule and its precedent. Read each record's comments first and understand
what they mean; they usually hold the decisive fact. You may second-guess a documented decision: steelman it, argue
from what the data is, and record a counter-argument rather than flipping a field
([selection.md](../knowledge-curation/references/selection.md), "Arguing a call").

## Step 3: Draft verdicts for untriaged records

For a record without a verdict, follow the `AI (UNVERIFIED)` convention of
[records.md](../knowledge-data-foundry/references/records.md): a verdict and justified markers, empty metadata only
where it can be inferred with confidence, `AI (UNVERIFIED)` in `checked_by` and `AI-Filled (Verify)` in `tags`, the
disclaimer and the assessment at the top of the comments, every existing note kept. Skip records claimed by another
curator. Reload each record right before saving it.

## Step 4: Check before handing back

For every record you triaged, run the checks of [verification.md](../knowledge-curation/references/verification.md)
marked "triage" (source, uniqueness, scope, use case and fit, split regime from the description, ethics) and put the
evidence for each decisive one into the assessment. Then run
`.venv/bin/python -m data_foundry.curation.cli validate`, `git add` every new file under `curation/`, and name the
uncommitted curation changes so the curator can ask for a commit.
