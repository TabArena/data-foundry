# Principles: how we decide

Part 0 of the curation rules; read it before any other file. The rules of this skill are ordered like a law book: an
earlier part is more fundamental than a later one and wins a conflict with it, and within a file an earlier rule wins
over a later one of the same strength. Every rule has a stable ID (`LEAK-3`) and a strength, so an assessment, a review
issue or an agent's brief can say which rule decided and why it outranks the other.

## The principles

A dataset is in the benchmark when it is a real tabular prediction task that we can evaluate honestly, on faithful
data, that is worth benchmarking, and that is cleaned the way an expert would ship it. In order of rank:

| Rank | Principle | Kind | Part and file | IDs |
|---|---|---|---|---|
| P1 | **Ethics.** No dataset whose subjects or creators object to its use for ML, and no harmful task. | validity | 1, [selection.md](selection.md) | `SEL` |
| P2 | **Scope.** Real tabular data, published for a classification or regression task that simulates a decision. | validity | 1, [selection.md](selection.md) | `SEL` |
| P3 | **A real use case.** An actor, a moment and a decision: the prediction point and the real-world target. | validity | 2, [use_case.md](use_case.md) | `USE` |
| P4 | **Honest evaluation.** Only what is known at the prediction point, and a split that mirrors the application. | validity | 3, [leak_checks.md](leak_checks.md); 4, [splits.md](splits.md) | `LEAK`, `SPLIT` |
| P5 | **Faithful, unique data.** The data is what it claims to be, from its first publication, in one copy, repaired from its origin. | validity | 5, [provenance.md](provenance.md) | `PROV` |
| P6 | **Worth benchmarking.** Not trivial, not too small, every fold can be scored. | value | 6, [task_probes.md](task_probes.md) | `TP` |
| P7 | **The expert state.** Cleaned as an expert would ship it: minimal and documented. | quality | 7, [cleaning_features.md](cleaning_features.md) | `CLEAN` |

Outside the ranking, because they apply at every rank:

* the procedure: [evidence.md](evidence.md) (`EV`: what counts as evidence and what a probe can mean),
  [verification.md](verification.md) (the checklist) and [writing.md](writing.md) (how to write for the curator);
* the house rules of the repository (knowledge-data-foundry): limits on what an agent may do, never weighed.

P3 informs P2: a scope rule stands in for the real-world use, so when a scope rule seems to exclude a dataset, check how
the prediction is made in practice and let the use case decide (Lennart, 2026-10-15; breast_cancer_prediction).

## Strengths

* **Must** decides on its own. A violation is fixed in the definition when it can be (drop, lag, filter, re-split,
  re-target); otherwise the verdict is `No` with the rule's marker. Only a higher-ranked Must overrides it.
* **Should** is the default. A departure needs the fact that sets the case apart and the higher principle it serves,
  and is recorded as an exception.
* **Weigh** is a factor. Factors are weighed together on the calls the rules leave open (a borderline keep, which
  framing to ship, a record's priority); the decision names the factors on each side. No factor decides alone, and no
  number of factors overrides a Must.

A rule may grade its strength by severity, such as a leak that is a Must when strong and a Should when weak.

## How to decide

1. **Facts first.** Settle a disputed fact with the decisive experiment before arguing about rules
   ([evidence.md](evidence.md), EV-1); a measurement on the data outranks what a page says about it (EV-2).
2. **Walk the parts in order**, and within a part the rules in file order. Write down each rule that the dataset
   triggers.
3. **Validity, then value, then quality.** A validity problem (P1-P5) means the benchmark would measure the wrong
   thing: it is fixed, or the dataset goes. A value problem (P6) is judged by the task-probe rules. A quality problem
   (P7) makes the benchmark a little worse: it is fixed when the fix is cheap and safe, and otherwise kept with a note.
   A very real task carries cleaning imperfections when they are written down; it does not carry a leak.
4. **Independent failures are not conflicts.** The ranking settles conflicts, where meeting one rule means breaking
   another. It does not rescue a failure on its own: every Must has to hold. A very real task with a handful of units
   per class per test fold is still `Too Small`, because nothing ranked above it makes the fold scorable.
5. **The remedy ladder.** Take the mildest remedy that resolves the problem: repair from the origin; fix the
   definition (drop, lag, filter, re-split, re-target); keep it with a documented note (an exception); exclude the
   dataset. Exclusion is for a Must that cannot be fixed.
6. **Write the judgment record.** Every assessment, `REVIEW.md` outcome and mediator report has the same shape, so the
   curator sees what decided:

   ```text
   Verdict: ship after changes.
   Validity: SEL-3 holds; USE-1 holds (direct fit); LEAK-10 triggered, fixed (dropped `staff_pick`); SPLIT-1 holds.
   Value: TP-2, a small real signal (keep).
   Quality: CLEAN-12 departure kept with a note (exception: the use case needs the raw codes, USE-1).
   Weighed: size -, source +, gap +.
   For the curator: issue 2, a weighing call (<one line>).
   ```

## Conflicts between rules

* A higher part wins over a lower part.
* Within a part, Must wins over Should, and Should over Weigh. At equal strength the earlier rule wins, unless the
  later one says it narrows the earlier one (`narrows LEAK-1`): then it wins within its scope.
* Rules win over patterns (quick ways to apply them) and over precedents (how they were applied). The dataset at hand
  wins over a pattern.
* Treat like cases alike: a precedent with the same facts is followed unless a fact sets the new case apart. A
  precedent that contradicts a rule is flagged, not followed; one of the two is wrong.

## Tensions

The conflicts that come up again and again, with how they are settled. Each row says which side wins, where that
stops, and the case that set it. A new decision on a tension not listed becomes a row.

| Tension | Which side wins | Where it stops | Cases |
|---|---|---|---|
| Ethics against anything (P1; SEL-1) | ethics | | |
| A real task against imperfect cleaning (P3 over P7; USE-1, USE-8 against CLEAN rules) | keep the task; fix what is cheap and safe, note the rest | a cleaning gap that changes what the target means is a validity question (P3, P5) | churn_telco_south_asia (impossible values made missing, churn timing kept as a stated risk) |
| A real task against a leak (P3 and P4; USE-12, LEAK-10) | fix the leak and keep the task: a leak is no reason to reject a task whose use case is real | a leak that cannot be undone (a supervised transform fit on all rows) excludes the dataset (LEAK-27) | yeast (`No`); kickstarter (`staff_pick` dropped once the task was "predict at launch") |
| A real task against a scope pattern (P3 informs P2; SEL-2, SEL-14) | the use case decides whether the scope rule applies | | breast_cancer_prediction kept (human readings used by tabular models), breast_w out (Lennart, 2026-10-15) |
| A weak transductive leak against the data as published (P4; LEAK-30) | keep it with a `Potential leak, kept on purpose:` note | a strong suspected leak makes it `No`; fix it when we can | scaling over all rows: sf_permit_time and home_credit fixed, the rest kept with notes (Lennart, 2026-10-19) |
| The right split against the score (P4 over P6; SPLIT-4, TP-2) | the split follows the application; a small signal under it is no reason to retire | | forest_fires; "the split follows what the task does in reality, not the size of the gap" |
| Temporal against grouped (within P4; SPLIT-3, USE-10) | one regime, the one the use case implies | | Lennart, 2026-10-12 |
| Unmatured training labels against the training floor (within P4; SPLIT-9, SPLIT-10 against SPLIT-14) | SPLIT-9 is met by removing the measurable shortcut (training labels shown to tell a test row's outcome); the diffuse rest of unmatured labels falls under SPLIT-10 (Should), departed from for SPLIT-14's 50% floor and recorded as an exception | a shortcut that can be measured is always removed, whatever it costs the floor | alfa_battle_2_0_task_2 (products of the test window's clients dropped), lending_club (Lennart, 2026-10-21) |
| A better version against our own fix (P5 over P6; TP-6, USE-4) | a version the source defines replaces ours; a fix of our own invention does not | | eryhemato |
| Repair against cleaning around damage (P5 over P7; PROV-13, CLEAN-1) | repair or rebuild from the origin first | when the origin cannot be reached, keep with a note or retire | coad, corporate_credit_rating, SUPPORT2, ashrae units |
| The real-world target against a convenient label (P3; USE-5) | predict what the actor acts on | | corporate_credit_rating retired, rebuilt as corporate_issuer_credit_rating |
| Uniqueness against a distinct task (P5 and P3; PROV-6, PROV-7) | a shared source with distinct tasks is not a duplicate | versions or cuts without a distinct task are duplicates | |
| Tiny but real (P3 and P6; TP-5, TP-8) | a small dataset is a tiny-data task | `Too Small` when a class has a handful of units per test fold | musk kept; parkinsons retired |
| Width against model limits (P6, P7; CLEAN-22, EV-4) | width is no reason to drop features; a model's input cap is never an argument | | coad (Lennart, 2026-10-15) |

## Precedence in the process

The same thinking orders everything else in the process: when two sources, people or stages disagree, the first
named wins.

| Facet | Order, first wins |
|---|---|
| Who decides | the curator's decision (a `CC` line, a review mark) > an AI assessment > an AI draft marked unverified > imported or legacy values. A newer decision of the curator beats an older one. The AI argues (a counter-argument) and never overrides. |
| Limits on actions | the house rules hold always and are never weighed. |
| Evidence | a measurement on the data > the source's primary documents > its page > third-party pages > inference ([evidence.md](evidence.md), EV-2). |
| Stages | a later stage's measured finding supersedes an earlier stage's reading: a screening verdict is provisional until the dataset is added and probed. |
| Remedies | repair > fix the definition > keep with a note > exclude (the remedy ladder above). |
| What the curator reads first | issues and findings in rank order (P1 first), then by strength (Must first), then by effect size. A summary leads with the highest-ranked issue. |
| Maintenance of the rules | an amendment > an exception > a precedent > a pattern. |
| A review panel | the mediator settles a dispute by rank; a weighing call goes to the curator. |

Which file is the truth for what (the definition, the record, the review file, the generated README) is repository
specific: [pipeline.md](../../knowledge-data-foundry/references/pipeline.md).

## Exceptions and amendments

* **An exception** departs from a Should rule for one dataset, without changing the rule. It names the fact that sets
  the case apart and the higher principle it serves:
  `**Exception to CLEAN-12 (2026-10-20, Lennart):** the clinic records the raw codes the model would see. Serves P3:
  the use case needs them.` It goes into the record, into the dataset's notes, and as a row of kind `exception` into the
  Cases table of the rule's file. A Must has no exceptions: only a higher-ranked Must overrides it, and anything else is
  an amendment.
* **An amendment** changes the rule. Its text is replaced in place under the same ID, with the date, the curator and
  the case that prompted it; the old wording goes, so the newer decision wins without two versions side by side. When
  the same reason has produced three exceptions, the next pass proposes an amendment.

## Consistent judgement, the curator's included

The rules only help when they are applied the same way every time, by the AI and by the curators. The AI checks every
decision when it applies it (a decision given in chat, a verdict changed in the dashboard, a mark on a review page)
and calls the curator out, with a question and never an override, in four cases:

1. The decision departs from a rule and gives no fact that sets the case apart, or it would break a Must of a higher
   rank (then it is not a reasonable exception: offer an amendment of the rule instead, as a deliberate change).
2. A precedent with similar facts was decided the other way: by this curator, another curator, or an AI recommendation
   a curator accepted.
3. The same curator's decisions on the same rule drift over time.
4. The same reason has produced its third exception.

The prompt is short, one per decision, and offers the ways out:

```text
**Consistency check (AI, 2026-10-20):** your call on A (keep, a departure from LEAK-30) differs from B (retired
2026-10-14, the same mechanism: scaling over all rows, a strong signal). What sets A apart?
(a) <the AI's best guess at the distinguishing fact>, recorded as an exception; (b) treat A like B;
(c) reopen B to match A; (d) change the rule (an amendment).
```

The answer is recorded as the curator's decision: an exception with its fact, the other dataset reopened with an
issue of its own, or an amendment of the rule. Questions for the curator to ask themselves before departing from a
rule:

* What fact sets this case apart from the rule and from the closest precedent?
* Would I decide the same for its sibling datasets?
* Is it a one-off, or should the rule change?
* Which higher principle does it serve?

## Arguing a call

A documented decision is not a correct one. When the evidence contradicts the stated reasoning, say so and argue the
case.

* Argue from what the data is (the feature composition, the true source, the size, the actual target), not from how
  someone might solve the broader problem today. For example, whether a table whose features are mostly URL and text
  tokens plus a few geometry numbers is an image task is argued from that breakdown (a vision model could not see the
  dominant features), not from the fact that the objects pictured were ads (internet_advertisements: the record keeps
  `No` with `Image` and `Wrong Domain / Source Modality`; the marker is the open point, not the verdict).
* Steelman the existing decision first, then give a concrete counter-argument that can be checked: numbers, the feature
  breakdown, what a model can or cannot access, and the rule IDs on each side.
* Surface it, do not override it: the curator has the call.
* It cuts both ways: argue for keeping an exclusion the curator is inclined to overturn when the evidence says so.

## Keeping the rules current

* A curator's decision that becomes a standing rule goes into the file of its topic in the same change, as a new rule
  placed by rank or an amendment of an existing one, with the name and date (`Lennart, 2026-10-19`) and the case as a
  Cases row.
* One rule lives in one file; other files cite its ID. An ID never changes and is never reused; the position of a rule
  in its file sets its precedence.
* Definitions and records cite `task_probes.md` by its rule numbers (rule N is TP-N) and `leak_checks.md` by name:
  keep both names and those numbers stable.

## In Data Foundry

* How the comment lines are written (`CC`, `Assessment`, `Exception to`, `Consistency check`):
  [records.md](../../knowledge-data-foundry/references/records.md).
* The stages, which file is the truth for what, and how a record moves between queues:
  [pipeline.md](../../knowledge-data-foundry/references/pipeline.md).
* The decisions grouped by rule, with the four consistency flags:
  `.claude/skills/knowledge-data-foundry/scripts/decision_register.py`.
