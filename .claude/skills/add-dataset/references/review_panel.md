# The review panel

Step 7 of `/add-dataset`: before the curator sees a dataset, a panel of agents tries to break it from different sides,
then argues it out, so the curator gets a short, ranked summary with the evidence under it. The agents are custom
agents in `.claude/agents/`; the main session runs them, because subagents do not start subagents. Every agent cites
rule IDs and ranks by [principles.md](../../knowledge-curation/references/principles.md), except the blind reviewer,
which reads none of our files on purpose.

## Before the panel

Prepare once per dataset, in the run folder `local-data-warehouse/_runs/<date>_<run>/<unique_name>/panel/` (never
committed):

* the definition passes `dataset check`, and the probe outputs of step 5 are saved there as JSON;
* the clean room for the blind reviewer:

  ```bash
  .venv/bin/python .claude/skills/knowledge-data-foundry/scripts/clean_room.py <unique_name> --out <panel>/clean_room
  ```

  It holds only `data.parquet` and `task.md` (target, problem type, size, regime column, source links): no task summary,
  no notes, no record.
* the claims list: every statement the dataset makes about itself (the `task_summary`, each `curation_comments`
  bullet, the `splits_comment`, each accepted warning, the record's assessments and the screening block).

Give every agent the paths, the unique name, the folder, the run folder for its scratch output and the thread caps of
[agent_runs.md](../../knowledge-data-foundry/references/agent_runs.md). Name agents (`<role>-<unique_name>`) so the
advocate and the critic can be resumed for their rebuttals.

## Phase A: evidence (all in one message, in parallel)

| Agent | Its question | It returns |
|---|---|---|
| `claim-auditor` | Does each claim hold? It tries to refute every claim with a test on the data. | one row per claim: claim, source, the test run, holds / refuted / untested, the evidence, the rule |
| `column-auditor` | Column by column: what it means (the codebook), whether it is known at the prediction point, whether its dtype and cleaning are right. | one row per column with its verdict; the problems ranked |
| `split-auditor` | Does the split mirror the application: the regime, the windows, the gap and late labels, the training history, the group ids, hidden groups? It runs the alternatives it doubts. | the split's verdict, each problem with its evidence and rule |
| `domain-practitioner` | Playing the actor of the use case: would I have these inputs then, is this the target I act on, would I use this model? | how real the task is (direct / approximate / none), the gaps, what an expert would change |
| `blind-reviewer` | With no notes and no rules, only the data and the source: what is this task, would I benchmark on it, what is wrong? | its verdict and its concerns, ranked, with evidence |
| `precedent-checker` | How were similar cases decided before (the decision register, sibling records, the Cases tables)? Is this definition consistent with them? | the precedents, consistent / departs, and for a departure the fact that sets this case apart or its absence |

The precedent checker reads the register first:

```bash
.venv/bin/python .claude/skills/knowledge-data-foundry/scripts/decision_register.py --json <panel>/register.json
```

## Phase B: the debate

* `advocate` argues to ship the dataset as defined; `critic` argues not to ship it, or to ship it changed. Each gets
  the phase A reports and writes an opening brief: at most seven points, each with its evidence and the rule ID.
* Then each gets the other's brief (resume the named agent with `SendMessage`) and writes one rebuttal: which points
  it concedes, which it disputes and why. One round; a second only when a new fact came up.

## Phase C: the mediator

`mediator` gets every report, both briefs and both rebuttals. It settles each disputed point by
[principles.md](../../knowledge-curation/references/principles.md): facts first (the decisive experiment, which it may
run), then rank and strength, then the remedy ladder. A point that is a weighing call is not settled: it goes to the
curator with each side's best evidence. It returns:

* the recommendation as a judgment record (ship / ship after changes / don't ship);
* the agreed facts;
* the changes to make now, the ones that need the curator, each with the rule;
* the disputed points: each side's best evidence, the rule each side rests on, what would settle it;
* consistency: precedents followed, and departures with the fact that sets this case apart, or a reflection question
  for the curator when there is none.

## Phase D: the editor

The main session applies the changes that need no decision, writes `REVIEW.md` (SKILL step 8), and gives the draft to
`review-editor`, which reads it cold as the curator would: is every issue's problem, effect, evidence and decision clear,
are the issues in rank order, is every sentence of the summary backed by the details, is anything raised that would
change no decision? The main session applies its fixes.

## What lands in REVIEW.md

The issues come from the mediator's "needs the curator" list and the disputed points, in rank order. After them, the
`**Review panel:**` block ([review file format](../../review-added-datasets/references/review_file_format.md)):

```markdown
**Review panel:** ship after changes (mediator). Claims: 14, 12 hold, 1 refuted (fixed), 1 untested. Blind review:
would benchmark; its main concern is the year column. Agreed: the split. Disputed: keep `region` (issue 3).

<details><summary>Mediator</summary>

...the mediator's report...

</details>

<details><summary>Claim audit</summary>

...one section per agent, its report as returned, trimmed only of process chatter...

</details>
```

The block leaves with the file once the curator has settled every issue; the decisive evidence goes into the record as
`CC` and `Assessment` lines on the way.

## Tiers

| Tier | Agents | When |
|---|---|---|
| `full` (default) | all of phase A, the advocate and the critic with one rebuttal each, the mediator, the editor: 10 agents and 2 resumed turns | a new folder |
| `focused` | the claim auditor, the auditors the change touches (columns, split, or both), the mediator, the editor | a re-check after a change, an answer to a review mark |

A full panel costs on the order of a million tokens per dataset (an estimate from the agents' reading and probing);
say the tier and the agents that ran in the report. In a batch, keep within the concurrency limit of
[agent_runs.md](../../knowledge-data-foundry/references/agent_runs.md): run one dataset's phase A (6 agents) while
another's debate runs.

## Rules

* The blind reviewer gets only the clean room. Give it no path into the repository, no notes and no rule names. If its
  report shows it read our files (it cites a rule ID or a curation note), discard it and run it again with
  `claude --safe-mode -p` from the clean-room folder.
* An agent's claim without a test is a question, not a finding (evidence.md, EV-6 and EV-7).
* The panel recommends; the curator decides. Nothing the panel says changes a verdict field.
* Personal data in the raw files stays in the run folder; reports quote no rows that identify a person.
