# Writing for the curator

Procedure, at every rank. How we write the record comments, the notes on a dataset, the plain-language task summary and
the questions for the curator. The general style rules (no em dashes, no bold-first bullets, no inflated wording) are
the "AI Writing Tropes to Avoid" section of [AGENTS.md](../../../../AGENTS.md); they apply to everything below, to
docstrings and to commit messages.

## The judgment record

A verdict, an assessment, a `REVIEW.md` outcome and a mediator's report all have the shape of
[principles.md](principles.md), "How to decide": the verdict first, then validity, value and quality with the rule IDs
that held, were triggered (and how fixed) or were departed from, the factors weighed, and what is left for the
curator. A reader sees in a few lines which rule decided and why it outranks another.

## Record comments

The comments hold substance, not a change log: provenance, leak mechanisms, the real target and split, why a verdict
was reached, what still needs checking. Do not add lines that only restate a field edit ("marked WIP", "set the
verdict to No"); the history already records who changed what. A dated comment carries new reasoning or facts.

Keep them minimal: what the dataset really is, the decisive reason for the verdict, where the data can be obtained,
what still needs checking. A few sentences is normal; a screenful is almost always too much. Leave out per-column
missingness, byte sizes, checksums, download mechanics and side observations. When asked for one thing (a link, a
duplicate check), write that down, not a report of the whole investigation. The long evidence for a dataset we keep
(probe numbers, quotes, the verification history) goes into the record, the short decisions into the dataset's notes.

## Notes on a dataset

One opening line naming the exact starting artefact, then one bullet per decision: what was done and the fact or
number that decides it, in one or two sentences, about 400 words in all. Every non-obvious step of the code has a
bullet, and every bullet has code. Name the prediction point in the first bullet. A suspect kept on purpose says the
mechanism, the numbers, why it stays and when to revisit it. A pipeline choice that approximates the task (columns
chosen by counts over all rows in a temporal task) says so.

Show a number only where it decides the call. A column recorded after the prediction point goes whatever it scores
alone, and a column known at the prediction point stays whatever it scores, so a single-column score for a drop the
context settles repeats the context and invites the reader to weigh it. Say how many splits a number comes from.

## The task summary

What the dataset simulates, in plain words, for a reader who has not seen the source: the use case first (an actor,
a moment, a decision), then what one row is, what is predicted and by when, what is known then, what the test data
stands for, and our changes that alter the task. Then the judgement of the fit ([use_case.md](use_case.md)). One or two
sentences per part; no jargon ("IID", "log1p", metric names) except where a number decides the fit; only facts from
the definition, its notes, the record and the source; "not stated" rather than a guess. Keep it in step with the notes:
a change to the task updates both.

## Questions and issues for the curator

The curator reads many of these in one sitting and decides each one. Questions like "what does this mean?", "why was
this brought up here?" and "explain this" in the reviews of October 2026 show where an issue failed. Each issue:

* states the problem in plain words, and defines any term a reader outside the analysis would not know (what
  "swapped" means, what a z-score over all patients does to a test fold);
* says what it does to the real task: which prediction gets better or worse than it would be in practice, and why;
* gives the evidence, with numbers only where they decide;
* lays out the options, the implemented one first, each with what it does to the dataset and its pros and cons;
* names the rule it rests on (its ID and strength), and for a weighing call the factors on each side;
* says whether it follows or departs from a precedent (a similar dataset decided before);
* ends with a recommendation and the decision needed.

The shape is fixed, so the curator finds each part in the same place (Andrej, 2026-11-03). Only bullets, each opened
by a bold lead, never a paragraph of prose:

| Bullet | | What goes in |
|---|---|---|
| `**Problem:**` | required | What is decided and why it is a question: at most three sub-bullets, each one sentence; a sentence may be long (Andrej, 2026-11-03). |
| `**Background:**` | when the problem needs more | The rest of the context: how the data or definition works, terms defined. |
| `**Effect on the task:**` | when it differs from the problem | Which prediction gets better or worse than in practice. |
| `**Experiments:**` | when something was measured | The numbers that decide, with how many splits or seeds. |
| `**Consistency:**` | when a similar dataset was decided | The precedents, and whether this follows or departs. |
| `**Panel:**` | when the panel disagreed | Each side's best argument in one sentence. |
| `**Unknown:**` | when a fact could not be checked | What would settle it. |
| `**Options:**` | required | A table, one row per option, see below. |
| `**Recommendation:**` | required | The option and the reason, then `**Decision:**` and the question. |

The page shows the problem, then a closed Details box with every bullet other than the problem, the options and the
recommendation, then the options and the recommendation (Andrej, 2026-11-03). So the problem, the options table and
the recommendation must read alone: a curator who never opens Details knows what is decided, what each option does
and what is recommended. Another bullet with a bold lead is fine when it helps (`**Sources:**`, `**Cost:**`). The
options table has the columns `| | Option | What it does | Pro | Con |`: a letter (A, B, ...), the option in a few words
with `(implemented)` on the one the definition has now, what it changes in the dataset (rows, columns, split, score),
and its pros and cons in a few words each. A cell with several points separates them with `; `, and the page shows them
as bullets (Andrej, 2026-11-03), so keep a `;` out of a single point. Every issue has at least two rows; the curator's
mark "as implemented" takes the implemented row, and "change" names the letter. Mark one row `(implemented)` also
when the question is whether to change something elsewhere (a sibling, a rule): the row that changes nothing is what
the definition has now, and the page names it on the "As implemented" button.

The text for the curator reads without the rules. Rule IDs, rule wording, the strength of a rule and the curator's
earlier calls quoted as precedent go into footnotes (`[^1]` in the text, `[^1]: **LEAK-31** (Should): ...` at the
end of the issue): the sentence says in plain words what the rule asks ("a feature chosen by its link to the target
is kept only with a note"), and the footnote names it. Use as many footnotes as the context needs; the page shows
them in a closed box. What only Claude needs to apply a decision (the code to change, the exact text for the record,
paths, the exception's wording, the probes to re-run) goes into a `**Notes for the AI:**` block after the bullets,
also closed on the page. An answer to the curator in the issue (`**Answer (AI, <date>):**`) takes the same shape when
it puts a new choice to the curator, and plain bullets otherwise.

Order the issues by rank: validity before value before quality, Must before Should, then by how much each changes the
task. Raise only what changes one of our decisions. A problem of someone else's copy is a note on that copy
([provenance.md](provenance.md), PROV-15); another benchmark's scores, a model's pretraining data or a model's input
limit are no evidence ([evidence.md](evidence.md), EV-4). One issue per decision, and a record field that disagrees
with the definition is a field correction, not an issue.

When the curator says "do as you see fit" or "fix as needed", decide, apply it, and record the decision and the reason
the same way as one of theirs. When a decision becomes a standing rule, write it into the knowledge files in the same
change; when it departs from a rule for one dataset, record it as an exception with the fact that sets the case apart
([principles.md](principles.md), "Exceptions and amendments").

A question about the consistency of a curator's decision (a consistency check) is short and asks, never argues at
length: the decision, the precedent or rule it departs from, the AI's best guess at the fact that sets it apart, and the
ways out ([principles.md](principles.md), "Consistent judgement").

## Reporting back

Lead with the recommendation in one sentence. Then what the record or definition missed or got wrong, in rank order
with the rule IDs, what it had right and what could not be checked, with citations; counts and scores in a short table.
Do not restate the record. Say which evidence proves a mechanism and which is circumstantial (EV-6). A summary comes
first and the details below it, so the curator can stop reading once the decision is clear.

## In Data Foundry

Where each kind of text lives (record comment lines, `curation_comments`, `task_summary`, `REVIEW.md`) and the
prefixes our notes use: [records.md](../../knowledge-data-foundry/references/records.md) and
[definitions.md](../../knowledge-data-foundry/references/definitions.md).
