# Writing for the curator

How we write the record comments, the notes on a dataset, the plain-language task summary and the questions for the
curator. The general style rules (no em dashes, no bold-first bullets, no inflated wording) are the "AI Writing
Tropes to Avoid" section of [AGENTS.md](../../../../AGENTS.md); they apply to everything below, to docstrings and to
commit messages.

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
* says what was implemented and what the alternative is, each with its cost;
* ends with a recommendation and the decision needed.

Raise only what changes one of our decisions. A problem of someone else's copy, another benchmark's scores, a model's
pretraining data or a model's input limit is no issue ([provenance.md](provenance.md)). One issue per decision, and a
record field that disagrees with the definition is a field correction, not an issue.

When the curator says "do as you see fit" or "fix as needed", decide, apply it, and record the decision and the reason
the same way as one of theirs. When a decision becomes a standing rule, write it into the knowledge files in the same
change.

## Reporting back

Lead with the recommendation in one sentence. Then what the record or definition missed or got wrong, what it had
right and what could not be checked, with citations; counts and scores in a short table. Do not restate the record.
Say which evidence proves a mechanism and which is circumstantial.

## In Data Foundry

Where each kind of text lives (record comment lines, `curation_comments`, `task_summary`, `REVIEW.md`) and the
prefixes our notes use: [records.md](../../knowledge-data-foundry/references/records.md) and
[definitions.md](../../knowledge-data-foundry/references/definitions.md).
