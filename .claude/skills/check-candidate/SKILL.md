---
name: check-candidate
description: Independent, cited second opinion on one candidate record in `curation/records/`. Traces the original source (paper, competition, repository), answers the open questions in the record's comments, checks siblings and duplicates, and writes the evidence plus a recommended verdict into the record. Use when the curator says "check X", "dive into X", "what did I miss on X", "your thoughts on X", when a record has open questions or a verdict inconsistent with a sibling, or when a dataset is suspected of a leak (its `references/leak_checks.md` holds the leak probes and the 2026 leak-audit precedents).
argument-hint: <unique_name>
user-invocable: true
---

# Check one candidate

Check one candidate dataset the curator is looking at: trace what the data really is, find what the
record misses, and report a second opinion with citations. Companion to `/triage-candidates`, which
holds the selection criteria this check applies.

**Input:** a record `unique_name` (a display name or a source link is fine; resolve it to the record first).

$ARGUMENTS

## When to invoke

* The curator is triaging a record in the dashboard and wants an independent check run in parallel:
  "check X", "dive into X", "what did I miss on X", "your thoughts on X".
* A record's `## Comments` contain open questions ("need to check duplicates", "licence unclear",
  "maybe not a real predictive task") and someone should go answer them.
* A verdict looks inconsistent with a sibling record and needs the evidence laid out.
* A shipped dataset is suspected of a leak, or an audit finding needs a deep dive before the curator decides.

Read the curation guidelines first, [`.claude/skills/triage-candidates/references/curation_guidelines.md`](../../../.claude/skills/triage-candidates/references/curation_guidelines.md): they are the
rubric. (No need to start the dashboard for this.) `/verify-dataset` is for a filled-in notebook, not for a backlog record.

## Protocol

Do every step; skip only when an earlier step settles the verdict and say so.

1. **Reload the record from disk** and read `## Comments` for what they *mean*. Write down every open
   question they contain: those are the things to answer, not a report of everything you find.
2. **Siblings.** List records with a similar name, the same source, or the same external collection
   (`grep -il` over `curation/records/`). Read their verdicts and comments: the team's precedent
   decides consistency (`hypertension` and `public_health_ins` for TableShift re-cuts, `higgs` for
   simulated physics, the `Image` list for descriptors computed from pictures).
3. **Trace the original source.** Follow every link to where the data first came from: the competition,
   the paper, the repository, the agency. Read the paper's *text*, not the abstract: the organisers'
   write-up, the data descriptor, the appendix that defines the task. Cite by section with the
   load-bearing sentence quoted. A paywalled paper: search briefly for a free copy (arXiv, Europe PMC,
   Semantic Scholar, author pages, a web search for the quoted title plus "pdf", PDF mirrors such as SciSpace,
   oa.mg, CORE), then ask the human for the PDF, with the exact Google query (title + "pdf"), instead of
   reasoning around it; ResearchGate and SciSpace block automated fetches. A Kaggle page is a claim; the discussions and notebooks are where
   problems surface. Read them with the `kaggle` CLI (>= 2.2.2 via `uvx`; `datasets topics list/show`,
   `kernels list/pull`; recipe in the curation guidelines, "Kaggle sources"), and say when that check was
   skipped.
4. **Answer the criteria with evidence.** What the data physically is (measured, computed, simulated,
   derived from an image or a signal); the original task and what solved it (the model families at the
   top of the leaderboard are a modality signal, and a strong gradient-boosting baseline's rank is the
   tabular-competitiveness number; under class imbalance never cite accuracy against the majority class as
   evidence, use ROC AUC / log loss against the class prior, and fit a quick LightGBM on prediction-time
   features yourself when the data can be loaded); the split the task design requires, not the one the paper used;
   size after cleaning; how the target was constructed (composite, computed, a supervised transform);
   ethics; duplicates by provenance, not by table shape. Licence and redistribution terms are recorded
   as a one-line note and never used as the reason for a verdict or a marker.
   If the source cannot be traced or the data looks too clean, run the tests in "Checking whether the data
   is generated" below. When the data can be loaded, name the prediction point, then run the leak probes in
   [`references/leak_checks.md`](references/leak_checks.md) (`scripts/v2/leak_probes.py <unique_name>` for a
   v2 folder). That file also lists what the 2026 leak audit decided for each kind of leak, which is the
   precedent for your recommendation.
5. **Write into the record only substance.** Add the source links you verified. Add one dated comment
   with what the data is, the decisive facts, and the recommended verdict and markers. Fill empty
   optional metadata only where the evidence is clear. Reload immediately before saving: the human edits
   the same file in the dashboard.
   * The human stated the verdict (in chat or already in the record): apply it and head the comment
     `CC (YYYY-MM-DD, Name):`.
   * The human has not: leave `suggestion` and `decision_markers` alone and head the comment
     `**Assessment (AI, YYYY-MM-DD):** recommend ...; the human has the call.` Do not use the
     `AI (UNVERIFIED)` reviewer convention here; it is for provisional triage of untriaged records.
6. **Leave the tree clean.** `git add` any new file under `curation/`, then run
   `data-foundry-curation validate` and `pytest -q tests/test_records_integrity.py`.

## Checking whether the data is generated

A table that looks clean and scores well can still be synthetic, or a real table that someone reworked
(relabelled, columns renamed, values replaced). Ordinary curation does not catch this; a few direct tests do.
Generated data is `No` + `AHDS (Artifical/Handmade/Deterministic/Simulated)` (crit. 4B in the curation guidelines), usually with
`Missing source information`, and `Data Quality Issue` when a real table was manipulated.

**When to suspect it:** no traceable first source, a data card that names only "a company" or "an airline",
"where is this from?" threads the uploader never answered, course or competition material, scores that look
too good (F1 0.97 on a survey), and distributions that look too even.

**Tests, cheapest first.** Run them on the earliest version you can find, not only on the shipped file.

1. **Trace the uploads and compare every version.** Download each upload in the chain (`kaggle datasets
   download`), including every file inside one upload, and match the rows by id or by the columns that should
   stay fixed. Then list what changed. For changed labels, fit a shallow tree on the original features to see
   whether a rule picked the changed rows. `customer_satisfaction_in_airline`: one Kaggle upload holds two files
   with the same 129,880 ids. In the derived file, 8 of 14 rating columns sit under the wrong name, distances
   were replaced, and 14,659 labels were flipped one way by a rule (Female, Personal Travel, wifi <= 3, delay
   <= 130 min) that uses Gender, a column the shipped file then drops.
2. **Look for row-counter patterns.** Sort by the id or by file order. Cross-tabulate each categorical
   column against `id mod k` for k up to a few hundred, look at the lengths of runs, and look at the target
   rate in blocks of ids. `ecommerce_shipping`: `Warehouse_block` is `ID mod 6` and `Mode_of_Shipment` a
   137-id cycle, with no exception in 10,999 rows; the target is 100% one class for the first 3,135 ids.
3. **Look for copied columns.** For every pair of columns with the same scale, compute the share of rows with
   equal values, overall and within each segment (each combination of the categorical columns). More than ~90%
   agreement between unrelated items is a copy rule. The airline base file has wifi = gate location in 95% of
   39,191 rows of one segment, and 27 segment-pairs above 90%. A real survey stays well below that: the
   Brazilian airport surveys never exceed 68%, even for near-synonyms.
4. **Look for marginals that are too even.** Categories with identical counts (1,833 rows per warehouse
   block), or ratings spread evenly over 1-5 inside a "satisfied" class.
5. **Look for class-conditional generation.** The two classes were produced by different generators when
   the correlation between two features differs strongly by class or changes sign, when a label-free
   nearest-neighbour distance predicts the label, or when number formats differ by class.
   `homeq_default_prediction`: near-copy clusters that are pure in the label, and nearest-neighbour distance
   alone gives AUC 0.92.
6. **Look for real-world structure the data should have.** Units that ought to cluster (passengers on the same
   flight; compare the share of repeated combinations with a shuffled column), physical constraints (arrival
   delay vs departure delay), impossible or odd combinations (children on business trips), and known reference
   values. The last test also shows which parts are real: the airline distances spike on actual route lengths
   (337 mi LAX-SFO, 2,475 mi JFK-LAX), so only the passenger part is synthetic.
7. **Look for a deterministic target.** A near-perfect fit from a simple formula or lookup (`video_game_fps_prediction`:
   log FPS = game + CPU + GPU, R² 0.99998) is `Trivial` and often `AHDS`.

**Calibrate before you conclude.** Run the same statistic on a real dataset of the same kind (another survey, other
transaction logs). Selection on the label also changes correlations, so a difference only counts when the real
reference does not show it. Report which columns look real and which look generated. In the record, put the
decisive test first, with its numbers, and the supporting signs after it.

## Report back

Lead with the recommended verdict and markers in one sentence. Then, as bullets with their citations,
what the record missed or got wrong, what it had right, and what could not be checked. Then what you
changed in which files, and whether anything is uncommitted. Counts and scores go in a short table, not
in the prose. Do not restate the record. Say which evidence proves a mechanism and which is only
circumstantial, and report a borderline case as a possible leak for the curator to decide rather than
clearing it.
