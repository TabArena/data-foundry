---
name: review-screened-candidates
description: "The curator's review of what /screen-candidates did: starts the local curation dashboard on the Screening queue (AI-screened records, highest priority first), explains what to check on each record, applies the decisions the curator gives in chat, checks every decision against the rules and similar past decisions and asks the curator to reflect when one looks inconsistent, and hands the accepted records to /add-dataset. Use when the curator wants to open the dashboard, review or verify screened candidates, accept or reject records, or asks what to look at next."
argument-hint: "[<unique_name>,... | <dashboard filter>]"
user-invocable: true
---

# Review screened candidates

Stage 1, the curator's half ([pipeline.md](../knowledge-data-foundry/references/pipeline.md)). `/screen-candidates`
left each record with a verdict (`TBD -> Yes`, `TBD -> 2nd Tier` or `No`), a priority and a screening block, all
marked `AI (UNVERIFIED)`. Here the curator verifies them; Claude runs the dashboard, explains, applies and checks the
decisions for consistency.

$ARGUMENTS

## Knowledge used

| Step | Read |
|---|---|
| 1 | [dashboard.md](../knowledge-data-foundry/references/dashboard.md) |
| 2 | [principles.md](../knowledge-curation/references/principles.md), [selection.md](../knowledge-curation/references/selection.md) |
| 3 | [records.md](../knowledge-data-foundry/references/records.md): `CC` and `Exception to` lines, the ✓ action |
| 4 | [principles.md](../knowledge-curation/references/principles.md), "Consistent judgement" |

## Step 1: Open the queue

Start the dashboard unless it already runs (`curl -s localhost:8765 >/dev/null` answers):

```bash
.venv/bin/python -m data_foundry.curation.cli serve            # http://127.0.0.1:8765
```

Point the curator at the Screening pill: the records the AI screened whose verdict is not `No`, highest priority first.
The AI's rejects are found with the status funnel (🤖 required, ✗ required). With names or a filter in the input,
give the link to that view instead (the dashboard's 🔗 copy-link hash syntax).

## Step 2: Say what to check

For each record the curator opens: the screening block's one-line reason, the decisive fact and the rule it rests on,
the priority factors, and what the AI could not check. Their choices:

| The curator wants to | In the dashboard |
|---|---|
| accept it for adding | set `Yes`, then ✓ (their name replaces the AI's) |
| keep it for later | leave `TBD -> Yes` or `TBD -> 2nd Tier`, set the priority, ✓ |
| confirm a reject | ✓ |
| overturn a reject | change the verdict and markers, set a priority, ✓ |

Questions about a record are answered from the knowledge files with the rule IDs; argue a call when the evidence
says so ([principles.md](../knowledge-curation/references/principles.md), "Arguing a call").

## Step 3: Apply decisions given in chat

"Accept a and b, c is a duplicate of d" is applied through the store API, each record reloaded right before its
change: the fields, the curator's name in place of `AI (UNVERIFIED)` in `checked_by`, and a
`CC (<date>, <curator>):` line with their reason. A departure from a rule is written as an `**Exception to <ID>**`
line ([records.md](../knowledge-data-foundry/references/records.md)).

## Step 4: Check each decision for consistency

Before applying a decision from chat, and for the decisions read back from the dashboard (records whose `checked_by`
changed from `AI (UNVERIFIED)` to a curator since the screening; compare with `git diff curation/records/`), run the
check of [principles.md](../knowledge-curation/references/principles.md), "Consistent judgement":

```bash
.venv/bin/python .claude/skills/knowledge-data-foundry/scripts/decision_register.py --since <date of the screening>
```

and give the `precedent-checker` agent the decisions with the register's output. When a decision departs from a rule
without a fact that sets it apart, contradicts a similar precedent, drifts from the curator's earlier calls on the
same rule, or is the third exception of its kind, put the short reflection prompt to the curator (one per decision,
in chat) and record their answer: an exception with its fact, the other record reopened, or a rule amendment written
into the knowledge file. Never change their decision yourself.

## Step 5: Hand over

* The records accepted in this session, by priority, and the filter that lists them for `/add-dataset`
  ([pipeline.md](../knowledge-data-foundry/references/pipeline.md), "The queues").
* The consistency prompts still open.
* `validate`, `git add` every changed file under `curation/`, and the uncommitted changes, so the curator can ask for
  a commit.
