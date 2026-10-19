# Verifying a dataset

What to check before a dataset is accepted, changed or shipped, and what each stage of the work checks. Every
workflow ends with the part of this list it can run: triage checks the record, a deep check checks the source and,
when the data loads, the data, adding a dataset checks everything, and a review re-checks what a change touches.

## Two halves

* Automated checks prove the mechanical invariants: split indices, leakage across fold boundaries, dtypes, class
  coverage, citation syntax, the export round trip. They are cheap, exhaustive and deterministic. Run them; never
  re-derive their findings by eye.
* Judgment covers what code cannot settle: provenance, scope, whether the split matches the application, whether a
  feature existed at prediction time, whether the notes describe what the code does. This is the reviewer's job.

The verdict is advisory: the curator has the final say.

## The checks

For each: pass, concern or cannot-verify, with one line of evidence (a quote from the source, a line of the
definition, a number from a check or a probe). "Looks fine" is no evidence, and cannot-verify is never upgraded to
pass.

| Check | What to look at | Stage |
|---|---|---|
| Source | Does the trail end at the first publication (paper, competition, institution), not an anonymous re-upload? Do the source and year name it ([provenance.md](provenance.md))? | triage, deep check, add |
| Uniqueness | Is it the same data as another dataset under another name, including another target, slice or version of one cohort? Compare canonical links and follow each to its origin. | triage, deep check, add |
| Scope | Was it published for a predictive classification or regression task? Scope by the original task, not the re-upload's framing. Forecasting, CTR, ranking and survey tables are out; a forecasting-like panel is in when a model beats each entity's naive forecast ([task_probes.md](task_probes.md)). | triage, deep check, add |
| Use case and fit | Is there an actor, a moment and a decision? Is the fit honest: approximate names its gap, and a task no decision fits goes back to triage ([use_case.md](use_case.md))? Read the summary as an outsider would. | triage, deep check, add |
| Split regime | Does the regime match the application ([splits.md](splits.md))? A prescribed split is a claim; a missing timestamp does not make a stream IID; grouped structure inside a temporal task and the other way round; a true group id, never a similarity cluster; the train history a refit model would use; test windows that avoid one atypical season. For a grouped task: the prediction unit, the aggregation and what is known about a new group follow the source's use case. | triage (from the description), deep check, add |
| Available at prediction time | Is the prediction point written down, and was every feature known then? Post-outcome fields, missingness caused by the outcome, a feature window that ends at the outcome, training rows whose label was not yet known, a planning gap the use case has ([leak_checks.md](leak_checks.md)). | deep check, add |
| Irreversible leakage | A feature that is the output of a supervised transform fit on the whole data is an exclusion. Label-aware features over all rows are fixable (drop them). Scaling over all rows is a weak leak (rebuild or note it). Recording artefacts that differ by class are harmonised, or exclude the dataset when they run through every feature. | deep check, add |
| Notes match the code | Is every claim in the dataset's notes implemented, and every non-obvious step of the code documented? Silent drops, filters and casts are the ones that bite. | add, review |
| Dtypes and cleaning | Categories, text, numbers and dates chosen by meaning; proxy missing values converted; impossible values missing; identifiers dropped or turned into their meaning; encodings reversed ([cleaning_features.md](cleaning_features.md)). | add, review |
| Target and metric | Is the target the real-world target, complete in every test period (no censoring by the download date), over the source's cohort? Does the metric fit the task? | deep check, add |
| Licence and citation | Is the licence what the source states (noted, never a verdict reason)? Does the citation name the work that published the data? | add |
| Reproducibility | Would the download instructions, pasted into a shell today, recreate the raw inputs? Are the links pinned (a DOI, an archived release)? | add |
| Ethics and representativeness | Any objection of subjects or creators to ML use, an ethical concern, or a task tabular models would not be used for? | triage, deep check, add |
| Worth benchmarking | Are the task-probe flags answered ([task_probes.md](task_probes.md))? Can every fold be scored (enough rows of each class per test fold, no constant target)? | add, rebuild |

## How to work the list

* Run the decisive experiment before asking the curator: the comparison that settles a question (a naive forecast
  against a model, the score with and without a column, a converted scale against the published one) answers it
  better than a question does.
* A claimed problem gets a second check that tries to refute it with its own code.
* Evidence comes from our own splits, probes and the sources, never from another benchmark's scores
  ([provenance.md](provenance.md)).
* Say which evidence is proof and which is circumstantial, and report a borderline case as a possible problem for the
  curator to decide.
* Never claim a check you did not run. If a source could not be reached, say so.
* Substance over volume: three real concerns beat thirteen paragraphs of "verified, looks good".

## The report

1. The verdict: ready, ready with noted concerns, needs changes, or should not ship.
2. The automated checks: error and warning counts, each error, and for each warning whether it is a real problem for
   this dataset or correct as it is (with the reason to accept it).
3. The checks above as a compact table, concerns and cannot-verify first; passes in one line each.
4. Proposed fixes as concrete edits, applied only when asked.
5. What a human must still check: every cannot-verify, spelled out.

How to phrase the open questions for the curator is in [writing.md](writing.md).

## In Data Foundry

The commands for the automated checks and the probes, and the Data Foundry checks of a definition (record pointers,
template conformance, the README in step with the code):
[checks_and_probes.md](../../knowledge-data-foundry/references/checks_and_probes.md).
