# Verifying a dataset

Procedure, at every rank: what to check before a dataset is accepted, changed or shipped, and which stage checks what.
Every workflow ends with the part of this list it can run: screening checks what the source can tell, adding a dataset
(and re-checking an existing one) checks everything, a review re-checks what a change touches, a rebuild checks that
every task is still worth benchmarking. The checks are listed in rank order
([principles.md](principles.md)): a failure higher in the table outranks one below it.

## Two halves

* Automated checks prove the mechanical invariants: split indices, leakage across fold boundaries, dtypes, class
  coverage, citation syntax, the export round trip. They are cheap, exhaustive and deterministic. Run them; never
  re-derive their findings by eye.
* Judgment covers what code cannot settle: provenance, scope, whether the split matches the application, whether a
  feature existed at prediction time, whether the notes describe what the code does. This is the reviewer's job.

The verdict is advisory: the curator has the final say.

## The checks

For each: pass, concern or cannot-verify, with one line of evidence (a quote from the source, a line of the
definition, a number from a check or a probe) and the rule it rests on. "Looks fine" is no evidence, and cannot-verify
is never upgraded to pass ([evidence.md](evidence.md), EV-7).

| Rank | Check | What to look at | Rules | Stage |
|---|---|---|---|---|
| P1 | Ethics | Any objection of subjects or creators to ML use, or a harmful task? | SEL-1 | screen, add |
| P2 | Scope | Was it published for a predictive classification or regression task that simulates a decision? Scope by the original task, not the re-upload's framing; read a scope rule by how the prediction is made in practice. Forecasting, CTR, ranking and survey tables are out; a forecasting-like panel is in when a model beats each entity's naive forecast. A non-tabular modality is out where its own models are clearly better. | SEL-2 to SEL-15, TP-10 | screen, add |
| P2, P5 | Real data | Is it a real random draw, not generated, deterministic or simulated? The tests of [provenance.md](provenance.md) when the source cannot be traced or the data looks too clean. | SEL-16, PROV-3 | screen (from the source), add |
| P3 | Use case and fit | Is there an actor, a moment and a decision? Is the fit honest: approximate names its gap, and a task no decision fits goes back? Read the summary as an outsider would. | USE-1, USE-2, USE-8, USE-9 | screen, add |
| P3, P4 | Target | Is the target the real-world target, complete in every test period (no censoring by the download date), over the source's cohort? | USE-5, LEAK-22 to LEAK-26, EV-5 | add |
| P4 | Available at prediction time | Is the prediction point written down, and was every feature known then? Post-outcome fields, missingness caused by the outcome, a feature window that ends at the outcome, training rows whose label was not yet known, a planning gap the use case has. | USE-3, USE-6, LEAK-1, LEAK-2, LEAK-10 to LEAK-12, SPLIT-9, SPLIT-10 | add |
| P4 | Irreversible and all-row leakage | A feature that is the output of a supervised transform fit on the whole data is an exclusion. Label-aware features over all rows are dropped. Scaling over all rows is a weak leak (rebuild or note it). Recording artefacts that differ by class are harmonised, or the dataset goes when they run through every feature. | LEAK-13 to LEAK-15, LEAK-27 to LEAK-31 | add |
| P4 | Copies across the split | Duplicate rows and repeated entities decided, with the share. | LEAK-16 to LEAK-21, SPLIT-29 | add |
| P4 | Recording by class | Were the classes measured, formatted and filled the same way? The number format alone (probe 17), missingness and values one class only has (probes 3, 4), same-label subgroups and rows of one class with a format the other rarely has (probe 7), straight-line fills in the raw order (probe 18). Fix what lets a model tell the classes apart for reasons other than the target, after measuring it; document the rest; marker `Class-dependent Recording`. | LEAK-13 to LEAK-15, LEAK-39, LEAK-40 | add |
| P4 | Split regime | Does the regime match the application? A prescribed split is a claim; a missing timestamp does not make a stream IID; grouped structure inside a temporal task and the other way round; a true group id, never a similarity cluster; the train history a refit model would use; test windows that avoid one atypical season. For a grouped task: the prediction unit, the aggregation and what is known about a new group follow the source's use case. | SPLIT-1 to SPLIT-31, USE-10, USE-11 | screen (from the description), add |
| P5 | Source | Does the trail end at the first publication (paper, competition, institution), not an anonymous re-upload? Do the source, year and citation name it? A paper claim with its section and quote. | PROV-1, PROV-2, PROV-8 to PROV-12, PROV-16 to PROV-18 | screen, add |
| P5 | Uniqueness | Is it the same data as another dataset under another name, including another target, slice or version of one cohort? Compare canonical links and follow each to its origin. | PROV-4 to PROV-7 | screen, add |
| P5 | Damage and repair | A damaged release repaired or rebuilt from its origin before it is kept or retired. | PROV-13 to PROV-15 | add |
| P6 | Metric | Does the declared metric score the use case's decision, with its origin (source, stand-in, fallback) and where we looked? A competition's metric kept; a paper's only when it is one deliberate choice, several reported ones mean the fallback; a threshold metric only with a threshold, k or cost matrix the source fixes. Do its unit and inputs exist in our data (scoring columns, never features), and does every test fold hold what it needs (whole stays, several eras)? Is the target on the scale the metric was scored on? A general name, and a custom metric in the library, tested against the official code? | MET-1 to MET-13 | screen (from the source), add |
| P6 | Worth benchmarking | Are the task-probe flags answered? Can every fold be scored (enough units of each class per test fold, no constant target)? | TP-1 to TP-10 | add, rebuild |
| P7 | Dtypes and cleaning | Categories, text, numbers and dates chosen by meaning; proxy missing values converted; impossible values missing; identifiers dropped or turned into their meaning; encodings reversed; no feature built from labels or all-row statistics. | CLEAN-1 to CLEAN-24 | add, review |
| procedure | Notes match the code | Is every claim in the dataset's notes implemented, and every non-obvious step of the code documented? Silent drops, filters and casts are the ones that bite. | [writing.md](writing.md) | add, review |
| procedure | Licence and citation | Is the licence what the source states (noted, never a verdict reason)? Does the citation name the work that published the data? | EV-4, PROV-10 | add |
| procedure | Reproducibility | Would the download instructions, pasted into a shell today, recreate the raw inputs? Are the links pinned (a DOI, an archived release)? | | add |

A review after a change runs the checks the change touches, at least "Notes match the code" and "Dtypes and
cleaning".

## How to work the list

* Walk it in rank order and stop at a Must that fails and cannot be fixed; still list the other failures you saw.
* Run the decisive experiment before asking the curator (EV-1): the comparison that settles a question (a naive
  forecast against a model, the score with and without a column, a converted scale against the published one)
  answers it better than a question does.
* A claimed problem gets a second check that tries to refute it with its own code, and the report says which evidence
  is proof and which is circumstantial (EV-6).
* Evidence comes from our own splits, probes and the sources, never from another benchmark's scores (EV-4).
* Never claim a check you did not run. If a source could not be reached, say so (EV-7).
* Substance over volume: three real concerns beat thirteen paragraphs of "verified, looks good".

## The report

1. The verdict: ready, ready with noted concerns, needs changes, or should not ship, as a judgment record
   ([principles.md](principles.md), "How to decide").
2. The automated checks: error and warning counts, each error, and for each warning whether it is a real problem for
   this dataset or correct as it is (with the reason to accept it).
3. The checks above as a compact table in rank order, concerns and cannot-verify first within each rank; passes in one
   line each; every concern with its rule ID.
4. Proposed fixes as concrete edits, the mildest remedy first, applied only when asked.
5. What a human must still check: every cannot-verify, spelled out.

How to phrase the open questions for the curator is in [writing.md](writing.md).

## In Data Foundry

The commands for the automated checks and the probes, and the Data Foundry checks of a definition (record pointers,
template conformance, the README in step with the code):
[checks_and_probes.md](../../knowledge-data-foundry/references/checks_and_probes.md).
