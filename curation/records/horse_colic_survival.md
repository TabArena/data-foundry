---
unique_name: horse_colic_survival
name: horse_colic_*
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Outdated
- Class-dependent Recording
tags:
- Tiny Data
- Non-IID (Grouped)
- 'Samples: Over Time'
- 'Time: Inferred'
- 'Target: Varying Delay'
- 'Entities: Recur'
- Clinical Study
collections:
- TabArena Reject
- TabSTAR
original_source: UCI
year: '1989'
collection_period: Unknown
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://github.com/EpistasisLab/pmlb/blob/master/datasets/horse_colic_lesion_type/metadata.yaml
- https://www.openml.org/search?type=data&id=25
- https://doi.org/10.24432/C58W23
notebook_path: datasets/beyond_iid/new_iid/horse_colic_survival/horse_colic_survival.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/horse_colic_survival/dataset.py
source_row: 761
type_adapter_id: curation-record-v1
---

## Comments

Has multiple possible classes (lesion or others). Decide for one that is reasonable

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — The UCI donation (McLeish & Cecile, 1989) defines no metric; its stated class attribute is the surgical lesion (attr 24), not the outcome we predict, and no paper defines an evaluation for the outcome task.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 8 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `temperature_of_extremities`, `peripheral_pulse`, `capillary_refill_time`, `peristalsis`, `abdominal_distension`, `nasogastric_tube`, `nasogastric_reflux`, `rectal_exam_feces` (the README lists their levels); their codes that mean unknown (don't know, refused, not asked) are missing in `capillary_refill_time` (CLEAN-10); left unordered: `mucous_membranes` (a partial order); `pain` (a partial order).

CC (2026-10-21, Andrej): 344 horses with colic (abdominal pain) from the University of Guelph, Canada, donated in 1989; the label is whether the horse lived, died or was euthanized (put down). I disagree with keeping it.
- **Died vs euthanized follows the admission period, and a feature gives the period away:** among non-survivors, earlier case numbers are 58 died / 14 euthanized, later ones (above about 530,560) 4 / 34, with similar clinical findings. `total_protein` (a blood value) switches from g/dL to g/L at the same time: in g/L rows 1 of 28 non-survivors died, in g/dL rows 64 of 80. Severe: one class split reflects when the horse came in, not its condition, and models use the unit (TabPFN log loss 0.68 vs 0.72 with one unit).
- Suggest excluding, or reframing as lived vs not. Evidence: the curation notes (target, recording change).

CC (2026-11-01, Lennart): marks on the review board of PR #37: pain and mucous_membranes stay unordered as partial orders, noted in the definition.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 13 coded columns carry their words.

**Assessment (AI, 2026-11-05):** marker `Class-dependent Recording`: `total_protein` (a blood value) is written in g/L for 95 horses (1 died, 27 euthanized) and in g/dL for 209 (64 died, 16 euthanized). The unit switch follows the hospital number, that is the admission period, so the unit alone tells died from euthanized (ROC AUC 0.79). Not harmonised yet: one unit for all rows raises TabPFN 3.5's log loss from 0.682 to 0.724. Noted in the definition's curation comments; data unchanged.

CC (2026-11-10, Andrej): decisions on the BeyondArena v0.2 review page.
- **Target: did the horse survive (lived against died or euthanized).** Died against euthanized follows the admission period, not the horse's condition; survival does not (Fisher p = 0.16 against the recording route). This is the usual survival-to-discharge outcome (Bishop et al. 2022, Vet Surg 51:891, https://doi.org/10.1111/vsu.13839).
- **Split: three windows of 57 horses in case-number order**, each trained on all earlier horses: a vet scores later admissions with a model built on earlier ones. A random split mixes both recording periods into every training fold.

**Assessment (AI, 2026-11-10):** collection, from the creators' papers: one hospital, the teaching hospital of the Ontario Veterinary College, Guelph; rows from its patient information system, lab values largely written by the lab equipment (Cecile & McLeish, https://arxiv.org/abs/1304.2344; McLeish et al., https://arxiv.org/abs/1304.1519). No admission dates; the case number orders the admissions. The first 229 case numbers (60% lived) match the 231 teaching-hospital horses of Pascoe et al. 1990 (Can J Vet Res, https://pmc.ncbi.nlm.nih.gov/articles/PMC1255672/, 61% survivors); the later 115 (67% lived) mostly follow the second recording route. A reading of the counts, not stated by the source. Records sometimes "ended because euthanasia was chosen as a solution for cost reasons", so missing values can follow the outcome. UCI's 300/68 files are not a time split.

CC (2026-11-10, Andrej): review page, issues 2, 4 and 5.
- **Both recordings kept as a shift between earlier and later admissions** (an exception to CLEAN-21, withdrawn on 2026-11-12), not harmonised.
- **Return visits kept:** the 10 later visits of 9 cases stay; a returning horse is an admission to score, and the time order keeps each later visit after its first. The use case and row now name admissions, first or return.
- **`Class-dependent Recording` stays:** the shipped target does not have it, but the source file does, so it stays in the curation record.

CC (2026-11-12, Andrej): review page, issues 7 and 8 (reopened after Lennart's comment on PR #55).
- **Recording harmonised, the exception to CLEAN-21 of 2026-11-10 withdrawn:** `total_protein` above 15 (g/L, 95 horses) is divided by 10 to the codebook's g/dL, and the 55 cells of 1/2 codes the later recording writes in `abdominocentesis_total_protein` and `nasogastric_reflux_ph` are missing. An analyst at the hospital knows its lab's unit, and the codes cannot be read as measurements. Kept as recorded, the unit only broke logistic regression in the window that first meets it (log loss 2.126 against 0.761 harmonised).
- **The evidence pointer of 2026-10-21** now names the curation notes instead of a folder on one machine.

CC (2026-11-12, Andrej): review page, issue 6, answering Lennart's question on PR #55 (back to a random split?): random horses grouped by case, 20 x 3 folds, in place of the three windows of case number.
- Along the case-number order, the only time order the data has, survival is flat (62.2% against 62.8%, Fisher p = 1.0), and a horse trained on its history scores like one trained on as many random horses (TabPFN 3.5, harmonised recording: +0.020 log loss, 95% interval -0.034 to +0.080, 60 horses).
- So the relation does not move with time (a stationary relation) and random horses stand for later admissions; grouping by `case_number` keeps the 10 return visits of 9 horses on the side of their first visit.
- `Temporal` removed, `case_number` is split metadata only (20 features); `required_split` `Grouped (NON-IID)`, tag `Non-IID (Grouped)` in place of `Non-IID (Temporal)`.

**Assessment (AI, 2026-11-12):** applied in `dataset.py` (`_clean`, the recording note, `changes`, the split); `dataset check` 0 errors, 0 warnings. Runs of 2026-11-12 (untuned LightGBM, logistic regression, TabPFN 3.5): random 3 x 20 against 3 x 57 windows, and single horses 200-259 trained on their history against as many random horses; no time dependence beyond the recording measurable (TabPFN, harmonised: +0.020 log loss [-0.034, +0.080]).

CC (2026-11-20, Andrej): folds grouped by case, `StationaryRelation` on the stationary-relation test (Review issue 2, C); the relation is measured for cases held out whole, not for random folds over visits.

## Review

**Outcome:** added. Split re-decided without the current split: the tree gives Temporal · rebuilt order, the definition ships Grouped · StationaryRelation by `case_number`.

**Main points:** Split: three windows of 57 admissions in case-number order instead of 20 x 3-fold cross-validation grouped by case number?

**Issues for Andrej:**

1. **Split: three windows of 57 admissions in case-number order instead of 20 x 3-fold cross-validation grouped by case number?**

   * **Problem:**
     - With every fact used the tree gives Temporal · rebuilt order: the case number orders the admissions, it built three windows of 57 (2026-11-10 to 2026-11-12), and the rule[^split-32] as amended on 2026-11-17 makes the split temporal wherever the windows can be built, however flat the relation.
     - The grouped random split was chosen on 2026-11-12 because survival is flat along the order (62.2% vs 62.8%, Fisher p = 1.0) and a horse trained on its history scores like one trained on random horses (TabPFN +0.020 log loss, 95% interval -0.034 to +0.080).
     - The case number is the only order (no dates); a recording change (total protein in g/L) falls at one point of it, as a time order would show.
   * **Background:** The hospital scores later admissions with a model built on earlier ones; the case number orders the admissions (a unit change falls at one point of it) and three ~50-row windows meet the floor, so temporal on the rebuilt order with a short discharge gap. Confidence of the blind walk: medium.
   * **Walk:** the questions as answered without the current split[^tree]:
     - Where will the model be used? (use case): at the same clinic, for later patients. Evidence: Use case: 'a veterinarian examining a horse with colic on arrival estimates whether it will survive ... with a model built on the hospital's earlier admissions'; one hospital (Ontario Veterinary College, Guelph).
     - Is an arrival order available in the data, or can it be recovered? (data): yes, rebuilt from the case number. Evidence: Hospital number's first six digits = the case number 'assigned to the horse' (UCI codebook), 514,279 to 535,415. My check (344 admissions with an outcome, sorted by case number): total_protein in g/L (>15) in 0-6% of the first seven tenths, then 100%, 74%, 88%: a recording change at one point of the case number, as a time order would show. Return visits keep their suffix after the first visit.…
     - Does the order give the windows the rule[^split-14] and the rule[^split-15] ask for? (data): yes, at the floor. Evidence: 344 admissions, 129 non-survivors (37.5%). Three test windows of ~50 admissions (e.g. positions 194-243, 244-293, 294-343) train on 56%, 71% and 85% of rows: the newest and one other above 50%; ~50 test rows and ~16-25 non-survivors each (non-survival 32-51% per tenth). A short gap (below) costs a few rows only. Small: the rule[^split-17]'s 50-row floor is just met.
   * **What the blind dossier lacked, and what it changes:** none to my answers; the definition departs. It ships Grouping on case_number (20 x 3 folds) with StationaryRelation since 2026-11-12 (review issue 6 D), replacing three windows of 57 horses in case-number order (2026-11-10 to 2026-11-12), because survival is flat along the order (62.2% vs 62.8%, Fisher p = 1.0) and a horse trained on its history scores like one trained on random horses (TabPFN +0.020 log loss, 95% CI -0.034 to +0.080). the rule[^split-32] as amended 2026-11-17 says that where the windows can be built the split is temporal however flat the relation, and StationaryRelation applies only…
   * **Missing from the blind dossier:** The flat-relation measurement and the earlier three-window split were partly in the dossier (redacted); the case-number grouping that keeps return visits together was not. In a temporal split return visits follow their first visit anyway.
   * **Source split:** yes, repository (UCI 47: horse-colic.data 300 rows, horse-colic.test 68 rows): predefined train/test files of unknown construction ("UCI ships two files without a stated construction; test rows spread over the whole case-number range (mean rank 0.46 vs 0.51) and 3 hospital numbers appear in both") https://archive.ics.uci.edu/dataset/47/horse+colic. Credible: no, Undocumented, not a time split and not grouped by horse; a convention of the 1989 donation, for a different target (surgical lesion).. Against the tree's leaf: no, UCI's predefined train/test files spread over the whole case-number range (random-like, for another target); the leaf tests later admissions on earlier ones.
   * **Key to split on:** case_number (six-digit hospital number), then the full number; order only, not an input.
   * **What changes:** dataset.py: the 2026-11-10 `Temporal` declaration replaces `Grouping`, the tag and Time basis line change, splits_comment and README rebuilt; the record's `required_split` back to temporal and a CC line; the tree's departure table loses horse_colic_survival.
   * **Blindness:** what the walker saw of the shipped split before deciding: Type fits (one veterinary teaching hospital, case numbers, no dates). saw: the tree's 'Temporal · rebuilt order' clinical leaf lists horse_colic_survival as an example, and splits.md the rule[^split-32]'s Entities bullet names it (ignored); the dossier also keeps a flat-survival measurement along the case number.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | 20 x 3-fold cross-validation grouped by `case_number`: 334 horses, about 111 per test fold (train 226-232, test 112-118 admissions), a horse's return visits with its first, `StationaryRelation` (implemented) | no change | 60 test splits over all 344 admissions give a steadier estimate than three windows of 57; the measured flat survival and flat history-vs-random score support random horses standing for later ones. | Never tests a later admission on earlier ones, so a later change of recording or practice stays untested; against the rule[^split-32] as amended 2026-11-17, a departure the tree's table must list. |
     | B | Three expanding windows of 57 admissions on `case_number` (the declaration of 2026-11-10): test case numbers 529,812-530,561, 530,562-534,519 and 534,523-535,415, train 173/230/287 admissions (50/67/83%), no gap | Replaces `Grouping(on="case_number")` with `Temporal(on="case_number", splits=TemporalSplits(window=57, unit="rows", n_windows=3, min_train_fraction=0.5))`; the tag `StationaryRelation` and its line give way to a time basis of the rebuilt order (`Time: Inferred`); the flat-relation measurement moves to the notes. | Tests later admissions on earlier ones, the vet's use; the middle window is the first to meet the second recording route. | 57 test rows per window sits at the rule[^split-17]'s floor of about 50; on those windows training on random horses scored 0.045 log loss better for LightGBM and 0.009 for TabPFN, the cost of the order. |

   * **Recommendation:** B, because the rule[^split-32] as amended on 2026-11-17 makes the split temporal wherever the windows can be built, and these three were built and shipped.. **Decision:** A or B?

   **Notes for the AI:** blind walk of 2026-11-17 (split tree at cd3877cb). Applying a change: the definition's split declaration, its time basis tag and line, the record's CC line; if A is kept, the tree's departure table with the reason.

   [^split-32]: **SPLIT-32** (Should): How the data was collected for the use case, when each sample, each feature and the target come into existence, is information for the split.

   [^split-14]: **SPLIT-14** (Must): A temporal task has at least 3 windows.

   [^split-15]: **SPLIT-15** (Must): The newest window is always a test window: it is the deployment period.

   [^split-17]: **SPLIT-17** (Should): Widen windows that get too small: below about 50 test rows per window, use wider windows and fewer splits.

   [^tree]: **SPLIT-36** (Should): walk the decision tree from the record's collection type, answering each question as if no split had been decided; a split the source prescribes is evidence, not an answer.

   **Andrej (2026-11-17, discuss):** This is a suggestion I don't get. I thought for a dataset with this sample size, we would
   have rules requiring more than three windows?

   **Answer (AI, 2026-11-17):** no rule asks for more than three windows; the rules cap them here, and a fourth is possible
   only with your sign-off.

   * Three windows is the minimum a time split must have[^hc1].
   * The tree asks for "as many windows as an IID or grouped task of that size gets folds": that is 3 folds; the 20
     repeats a small IID task gets are redraws of the same 3 folds, which a time split cannot redraw[^hc2].
   * The floors decide the rest: the newest window and one other train on at least 50% of the admissions, others
     down to 30%, never more windows under 50% than at or over it[^hc1]; and a window should keep about 50 test rows
     or more[^hc3].
   * On 344 admissions in case-number order that gives:

     | Windows | Test admissions per window | Train shares | Needs |
     |---|---|---|---|
     | 3 (as proposed) | 57 | 83%, 67%, 50% | nothing |
     | 4 | 57 | 83%, 67%, 50%, 34% | your sign-off for the window at 34% |
     | 6 | about 28 | down to 50% | goes below the ~50 test rows per window |

   * The cost you point at is real: three windows test 171 admissions once each, against every horse tested 20 times
     under the grouped folds, so the score is noisier. That is the price of testing later horses on earlier ones.

   [^hc1]: **SPLIT-14** (Must): a temporal task has at least 3 windows; the newest and at least one other train on
     at least 50% of the data, others down to 30%, and at most as many windows under 50% as at or over it.

   [^hc2]: **SPLIT-33** (Should): an IID or grouped task gets repeated 3-fold cross-validation, with 20 repeats when its
     train side holds fewer than 500 units.

   [^hc3]: **SPLIT-17** (Should): below about 50 test rows per window, use wider windows and fewer splits.

2. **Back to three windows in case-number order, as the rules now ask?**

   * **Problem:**
     - You moved horse_colic from three windows to grouped random folds on 2026-11-12 because survival along the case numbers was flat; since 2026-11-17 a split is temporal wherever windows can be built, however flat the relation[^s32w].
     - Three windows of 57 admissions train on 50%, 67% and 83% of the rows: they meet the three-window floor but not the 60 splits a task of 344 rows gets, so the answer follows the cross-dataset item on the window count.
     - The flat relation came from a Fisher test (62.2% against 62.8% survival) and a TabPFN comparison, not the stationary-relation test the rules now name; that test, run on 2026-11-18 over six runs of 57 cases, is inconclusive in each of the newest three.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | 20 x 3 folds grouped by case, `StationaryRelation` (implemented) | No change | 60 splits | No rule supports it now: windows exist, and the flat reading is not the rule's test |
     | B | Three windows of 57 admissions in case-number order (as on 2026-11-10) | The case number orders the split and is no input; the flat measurement goes in the notes | Tests later admissions, as the vet meets them | Three noisy windows on 344 rows |
     | C | The grouped folds, tagged by the stationary-relation test | `StationaryRelation` if it reads flat, else `ForcedGroupedFromTemporal` | 60 splits on a measured basis | Only open if the window-count item takes its option B |

   * **Recommendation:** B with option A of the window-count item, C with its option B. **Decision:** A, B or C?

   **Notes for the AI:** B: the 2026-11-10 declaration; the gap: survival is known at discharge, days after admission, well inside one window, so no gap, stated in the splits comment; record `required_split` back to temporal; tree: horse_colic leaves the departures.

   [^s32w]: **SPLIT-32** (Should, amended 2026-11-17): "Where the windows can be built, the split is temporal however flat the relation, and the measurement goes in the notes as what the windows cost."

   **Andrej (2026-11-18, discuss):** Do the stationary relation test.

   **Answer (AI, 2026-11-18):** run (v3): inconclusive in each tested period by the rule as drafted, flat when pooled over the three periods; so the answer now follows the two open cross-dataset items.

   * **Experiments:** six runs of 57 cases in case-number order, the newest three tested, ROC AUC gap of the forward model ± one SD over five seeds.

     | Run tested | LightGBM | Kumo-Tabular | Floor | Verdict |
     |---|---|---|---|---|
     | 6 of 6 | +0.023 ± 0.021 | +0.002 ± 0.022 | 0.003 | inconclusive |
     | 5 of 6 | +0.000 ± 0.027 | -0.001 ± 0.015 | 0.002-0.003 | inconclusive |
     | 4 of 6 | +0.008 ± 0.026 | -0.003 ± 0.022 | 0.002-0.003 | inconclusive |
     | pooled over the three | +0.010 ± 0.014 | -0.001 ± 0.012 | 0.003 | flat (Kumo-Tabular) |

   * No run is not flat: no forward model does clearly worse than the contemporaneous one.
   * With the window-count item's option a, B (three windows) stands whatever the test says; with its option b, C applies, and C's tag is `StationaryRelation` with the flat-threshold item's option a (pooled), `ForcedGroupedFromTemporal` with its option b (per period).

   **Answer (AI, 2026-11-18):** reassessed with the new forced step (the interchangeable question first; measured not flat leads to whole periods or Too Small) and the pooled flat verdict.

   - With the window-count item still open: windows (B) if three windows suffice.
   - Otherwise the forced step reads the v3 test pooled: flat (Kumo-Tabular), so C is the grouped folds tagged `StationaryRelation`, now on the rule's test, the same split as shipped with a new line.

   **Andrej (2026-11-19, change):** Agree.

   **Answer (AI, 2026-11-19):** one question before I apply it: the answer you agreed to gives B (three windows) if three windows suffice, else C (the grouped folds tagged `StationaryRelation`).

   - Under the window rules of 2026-11-19, three windows suffice: fewer than the target (60 for 344 rows) are accepted, never under three, so the rules give B.
   - On cirrhosis, a dataset of the same kind (304 patients, three windows of 50 possible), you chose the random folds with a forced tag over the windows today.

   | | Option | Splits | Test size | Tag |
   |---|---|---|---|---|
   | B | Three windows of 57 admissions in case-number order, no gap | 3 | 57 each (train 50%, 67%, 83%) | none (temporal) |
   | C | 20 x 3 folds grouped by case | 60 | about 115 each | `StationaryRelation` (pooled v3 test flat, Kumo-Tabular) |

   **Decision:** B (the rules) or C (as on cirrhosis)?

   **Andrej (2026-11-19, change):** Is this stationary once we choose the grouped setting? Did you measure it?

   **Answer (AI, 2026-11-19):** yes, measured on 2026-11-18, and the grouping does not change it: the test reads the relation along the case-number order, whatever folds the split then uses. Pooled over the three newest runs it reads flat for Kumo-Tabular; each run alone is inconclusive.

   | Run of 57 cases tested | LightGBM gap (ROC AUC) | Kumo-Tabular gap | Floor |
   |---|---|---|---|
   | 6 of 6 | +0.023 ± 0.021 | +0.002 ± 0.022 | 0.003 |
   | 5 of 6 | +0.000 ± 0.027 | -0.001 ± 0.015 | 0.002-0.003 |
   | 4 of 6 | +0.008 ± 0.026 | -0.003 ± 0.022 | 0.002-0.003 |
   | pooled | +0.010 ± 0.014 | -0.001 ± 0.012 | 0.003 |

   * By the rule (a model with skill, two SD within ten floors, no run not flat), Kumo-Tabular's pooled reading is flat: 2 x 0.012 = 0.024 against ten floors of 0.03.
   * So C would be the 20 x 3 folds grouped by case, tagged `StationaryRelation` on this test.

   **Decision:** B (three windows) or C (grouped folds, `StationaryRelation`)?

   **Andrej (2026-11-20, change):** We can do 20 x 3 folds grouped by case, tagged StationaryRelation. But note that the stationary relation only holds for the grouped setting.

   **Resolved (2026-11-20, Andrej):** C. The 20 x 3 folds grouped by case stay, `StationaryRelation`; the `Time basis:` line rests on the stationary-relation test (pooled Kumo-Tabular -0.001 ± 0.012 ROC AUC, flat) and says the relation is measured for cases held out whole (a horse's return visits on one side), not for random folds over visits. `dataset check`: 0 errors. Not rebuilt.

## Reference

McLeish, M. & Cecile, M. (1989). Horse Colic [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C58W23
