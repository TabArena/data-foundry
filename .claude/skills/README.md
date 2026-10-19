# Curating datasets with Claude: start here

This folder holds the Claude Code skills we curate datasets with. Four of them are commands you type (`/name`); two
hold the knowledge every command applies and are never typed. This page is for people: what to type when, what Claude
does, what it leaves for you, and how your own decisions are checked. The dashboard shows it as "Start here" on its
Guidelines page.

## The pipeline in one picture

```text
  link or backlog record
          │
          ▼
  /screen-candidates ──────────▶ record: verdict, priority 1-5, screening notes   (AI, unverified)
          │
          ▼
  /review-screened-candidates ─▶ you, in the dashboard: accept (Yes), keep for later, or reject
          │
          ▼
  /add-dataset ────────────────▶ dataset folder + REVIEW.md: ranked questions, review-panel reports   (AI)
          │
          ▼
  /review-added-datasets ──────▶ you, on the review page: ship, change, don't ship; Claude applies it
          │
          ▼
  build and commit ────────────▶ only when you ask
```

Two stages, and in each one the AI works first and you verify:

| Stage | The AI works | You verify |
|---|---|---|
| 1. Screen: a quick pass from the source, nothing built | [`/screen-candidates`](screen-candidates/SKILL.md) | [`/review-screened-candidates`](review-screened-candidates/SKILL.md) |
| 2. Add: build the dataset and attack it | [`/add-dataset`](add-dataset/SKILL.md) | [`/review-added-datasets`](review-added-datasets/SKILL.md) |

## The commands

### `/screen-candidates`: a quick first pass

* **When:** you found a dataset; the backlog needs a pass; you want to know what to look at next; "check X" on a record
  that has no dataset folder yet.
* **You type:** `/screen-candidates https://www.kaggle.com/datasets/<owner>/<slug>`, `/screen-candidates
  some_record,another_record`, or `/screen-candidates` alone for every record without a verdict.
* **Claude:** reads the source and the web (nothing is downloaded beyond a preview, nothing built); writes into each
  record what the next stage needs (first publication, the data as published, the use case, the likely split, papers,
  related records and duplicates, risks); rejects the obvious cases (unethical, generated, non-tabular, forecasting,
  duplicate, unknown source, no use case) after a second agent tried to refute each reject; gives every other record
  `TBD -> Yes` or `TBD -> 2nd Tier` and a priority from 1 (last) to 5 (first).
* **You see:** the records in the dashboard's Screening queue, marked 🤖 until you verify them. A single name gets a
  deeper pass (the paper's text, Kaggle discussions, related records).
* **Next:** `/review-screened-candidates`.

### `/review-screened-candidates`: you verify the screening

* **When:** after a screening run, or whenever you want to work the queue.
* **Claude:** starts the dashboard on the Screening queue (highest priority first), tells you what to check per record,
  applies decisions you give in chat ("accept a and b, c is a duplicate of d"), and checks every decision for
  consistency (below).
* **You:** set `Yes` to send a record to `/add-dataset`, keep it for later with a priority, or confirm or overturn a
  reject; ✓ marks it verified.
* **Next:** `/add-dataset` on the records you accepted.

### `/add-dataset`: build it and attack it

* **When:** a record is `Yes`; or "is X ready / leaky / correct?" on a dataset that already has a folder.
* **You type:** `/add-dataset some_record`, or a dashboard filter for a batch.
* **Claude:** writes the dataset definition (`dataset.py`) from the source, loops on `dataset check` and the leak,
  task and group probes until clean, runs the verification checklist, then sends a review panel of agents at it (below)
  and writes what you must decide into the folder's `REVIEW.md`: ranked, most fundamental first, each question with its
  evidence, the rule it rests on and the decision needed; the panel's full reports below.
* **Never:** builds a container, commits or pushes on its own.
* **Next:** `/review-added-datasets`.

### `/review-added-datasets`: you decide on the review page

* **When:** after `/add-dataset`, or when you want to see everything still open.
* **Claude:** builds a page from the `REVIEW.md` files (a local HTML file, or a private Claude artifact if you prefer);
  per dataset you get the use case, your decisions, the panel's reports, the definition, its README and the record.
  You mark a verdict per dataset and each question; Claude reads the marks back, checks them for consistency, applies
  them (to `dataset.py`, the record, the CHANGELOG) and removes what is settled from `REVIEW.md`.
* **Next:** a build and a commit, when you ask ("rebuild X and Y", "commit this").

### Everyday situations

| You want to | Do |
|---|---|
| add a dataset you found | `/screen-candidates <link>`, then `/review-screened-candidates` |
| know what to look at next | `/review-screened-candidates` (the queue is sorted by priority) |
| get a dataset you accepted into the benchmark | `/add-dataset <name>` |
| know whether a dataset is ready | `/add-dataset <name>` on its folder (a re-check) |
| apply your marks from the review page | `/review-added-datasets` ("apply my review") |
| rebuild containers | ask in words: "rebuild X" or "rebuild everything" |
| ask whether a dataset belongs, or why a rule says so | just ask; Claude answers from the knowledge skills |

## The review panel

`/add-dataset` does not trust its own work. After the dataset passes its checks, these agents look at it, each from
one side (definitions in [`.claude/agents/`](../agents/)):

| Agent | Looks for |
|---|---|
| claim auditor | every claim the dataset makes about itself, tested until refuted or confirmed |
| column auditor | each column: what it means, whether it is known when the prediction is made, how it is cleaned |
| split auditor | whether the train/test split mirrors how the model would be used |
| domain practitioner | the task through the eyes of the person who would use it: is it real? |
| blind reviewer | the data and its source only, without any of our notes or rules: an outside view |
| precedent checker | how similar datasets were decided before, and whether this one is consistent |
| advocate and critic | argue for and against shipping, from the evidence above, then answer each other once |
| mediator | settles what the rules settle, and hands you the calls that are yours |
| review editor | reads `REVIEW.md` as you would and fixes what is unclear |

A full panel costs on the order of a million tokens per dataset; for a re-check after a small change Claude runs a
smaller one. In stage 1, two agents help: a screener for batches and a reject checker that argues against every quick
`No`.

## Where the rules are

* [knowledge-curation](knowledge-curation/SKILL.md): how we decide, independent of the tooling. Start with
  [principles.md](knowledge-curation/references/principles.md): the principles in rank order (ethics, scope, a real use
  case, honest evaluation, faithful data, worth benchmarking, the expert state), rule strengths (Must, Should, Weigh),
  the tensions between rules and how they are settled, exceptions and amendments.
  [evidence.md](knowledge-curation/references/evidence.md) says what counts as evidence and what a probe flag can mean.
* [knowledge-data-foundry](knowledge-data-foundry/SKILL.md): how this repository does it (records, the dashboard,
  `dataset.py`, the working copy, builds) and the house rules.
* The dashboard's Guidelines page renders both.

Every rule has an ID such as `LEAK-3`; Claude's assessments, the review questions and the panel's reports cite them,
so you can see which rule decided and why it outranks another.

## Who decides what

| You | Claude |
|---|---|
| every verdict (`Yes`, `No`, ship, don't ship) | drafts, marked unverified until you check them |
| every review mark, exception and rule change | assessments, counter-arguments, open questions |
| builds, commits, pushes | nothing of these without your ask |

## Your decisions are checked too

The rules only help when they are applied the same way every time. When Claude applies one of your decisions, it
compares it with the rules and with similar past decisions, yours and other curators'. It asks you to reflect, in one
short note per decision and never by changing your decision, when:

1. the decision departs from a rule and nothing says what sets this case apart;
2. a similar case was decided the other way before;
3. your calls on the same rule drift over time;
4. it is the third exception for the same reason (the rule may need to change).

You then choose: record it as an exception with the fact that sets it apart, treat it like the earlier case, reopen
the earlier case, or change the rule. Before you depart from a rule, ask yourself:

* What fact sets this case apart from the rule and from the closest precedent?
* Would I decide the same for its sibling datasets?
* Is it a one-off, or should the rule change?
* Which higher principle does it serve?

## More

* How a record moves through the stages, and which file is the truth for what:
  [pipeline.md](knowledge-data-foundry/references/pipeline.md).
* The working copy of TabArena v0.2 and how a new curator gets started:
  [GETTING_STARTED.md](../../datasets/_dev/tabarena-v0pt2/GETTING_STARTED.md).
