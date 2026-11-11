---
unique_name: gallstone_disease
name: Gallstone
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Selection Bias
tags:
- Tiny Data
- 'Samples: Over Time'
- 'Time: Lost'
collections:
- New (BeyondArena)
original_source: UCI
year: '2025'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/1150/gallstone-1
- https://doi.org/10.1097/md.0000000000037258
notebook_path: datasets/beyond_iid/new_iid/gallstone_disease/gallstone_disease.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/gallstone_disease/dataset.py
source_row: 768
type_adapter_id: curation-record-v1
---

## Comments

looks good

CC (2026-10-06, Lennart): Kept after the task-probe review: the `no_spread` flag does not hold. The three untuned families differ by 0.036 in skill (+0.683 to +0.719), which the probe compared, unpaired, with twice their typical standard error over 5 splits (0.054). Tuned methods spread clearly: on BeyondArena TabPFN-3.5 reaches ROC AUC 0.911 and the median method 0.883, with 8 of 29 methods tied with the best.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Esen et al. 2024 report accuracy, precision, recall, F-measure and AUC side by side, none named as the criterion (MET-5).

CC (2026-10-27, Lennart): keep it as Andrej marked it: the Selection Bias marker and fit direct (USE-8, amended on the review of PR #16); how the patients were chosen is not stated.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): ordinal scales shipped as numbers, left as numbers for the curator's review: `Hepatic Fat Accumulation (HFA)`.

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 1 ordinal scales shipped as numbers are ordered categories (point 3); Comorbidity's three undocumented 2 and 3 (each with one listed disease) recoded to 1, the rows kept (CLEAN-11); the fat-accumulation grade an ordered category.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `nhanes_iii_gallstones` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 3 coded columns carry their words; the target keeps its codes.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (0 means gallstones present (UCI)).

CC (2026-11-11, Andrej): BeyondArena v0.2 review page, gallstone_disease. Both marks confirm what the review already decided, and neither could be carried into this branch's definition.
- Issue 2 (`ok`, A): the fit is `approximate`, for two gaps that are not the selection: the fatty-liver grade comes from the ultrasound that also finds the gallstones, and the two groups were recorded apart. This supersedes the `direct` of Lennart's CC of 2026-10-27, which answered the selection question on a definition without those gaps. In the reworked definition the target is decoded with 1 = gallstones, superseding "0 means gallstones present (UCI)" in the CC of 2026-11-01.
- Issue 3 (`discuss`, A): the random split is a `StationaryRelation`, argued from the use case: the diagnosis and every feature come from one visit, within one year of consecutive outpatients. The measured drift (ordered halves 0.06-0.07 ROC AUC below random ones, from the controls' AST/ALT step) runs along the file's sort order, which is not shown to be time, so it does not contradict the reading. The random split cannot test later outpatients, nor whether the two groups came in different months (vitamin D follows the season). The `StationaryRelation` tag enters `data_tags` once PR #50 is in.
- Not applied here: this branch's `dataset.py` is the 319-row version from before the 2026-10-21/11-04 rework (`fit="direct"`, no second-route filter, target decoded the other way), so the fit and the `Time basis:` bullet go in with that rework rather than on top of it. The definition was left untouched.
- The review moved from the folder's file into this record's `## Review` section.

## Review

**Outcome:** added. Of the 319 outpatients of one Ankara clinic (2022-2023) in the UCI file, 242 remain, and the task is
whether they have gallstone disease (86 do), from body composition, an ultrasound liver grade and blood tests. Reviewed
without a panel, from the gathered evidence: the record, the earlier checks of 2026-10-21 to 2026-10-23 and the
model runs on the shipped BeyondArena data. Kept on review (issue 1, resolved): Andrej's changes of 2026-10-21 and
Lennart's keep of 2026-10-27; the merge of 2026-11-04 decodes the target with 1 = gallstones. The AI recommends shipping
it, with one call left on the use-case fit (issue 2). Validity: the artefacts that let a model tell the groups apart for
reasons other than gallstones are removed (a second recording route, a column recorded for one group, number formats;
LEAK-13, LEAK-39). Model runs used the UCI file before these changes and found exactly that leak: the decimal
counts alone beat every benchmark method (1 - ROC AUC 0.038 against 0.089 for TabPFN 3.5); on the v0.2 frame the number
format alone gives ROC AUC 0.557. Value: tuned methods spread (TP-3); TabPFN 3.5 0.838, gradient boosting 0.778,
logistic regression 0.762 ROC AUC. Quality: filled cells, the ultrasound grade and entry errors are kept with their
measured effect (`Class-dependent Recording`, `Selection Bias`). Weighed: a documented clinical study against a small,
partly repaired file.

**Main points:** Fit settled 2026-11-11: `approximate` (issue 2). Time basis settled 2026-11-11: random split as a
`StationaryRelation`, argued from the use case, with the drift along the file order named (issue 3). Nothing open.

**Record judgment:** valid after repair, settled by CC 2026-10-21 (Andrej: keep, with the changes listed there) and
CC 2026-10-27 (Lennart: keep); marker `Class-dependent Recording` added 2026-10-26. Lennart's CC of 2026-11-01 says
"0 means gallstones present (UCI)", but the definition, after the merge of 2026-11-04, decodes 1 as gallstones
("Yes"), as the paper and the file show (class 1 is 57% women and has lower vitamin D); the CC of 2026-11-11 says
so; Lennart should be told. The data-scouting run of 2026-10-31 screened `nhanes_iii_gallstones`
(AI-filled): gallbladder ultrasound of about 14,000 adults in a national survey, a task we would construct.

**Issues for Andrej:**

1. **Ship in TabArena v0.2 as defined?**
   - Checked and settled (CC 2026-10-21, Andrej): 77 rows of a second recording route (72 with gallstones) are
     dropped, since models recognised the route (its cases against the controls 0.993); hyperlipidemia, recorded for
     one group only, is dropped; five columns are written at their measured precision, which takes the number format
     alone from 0.947 to 0.557. UCI's reversed label coding, the 134 excluded outpatients, the ultrasound origin of
     the fatty-liver grade and the `approximate` fit are in the texts.
   - Kept on purpose, each with its measured effect (TabPFN 3.5 ROC AUC, 3-fold x 20, 0.838 with every column):
     the straight-line fills (re-imputed inside each training fold without the label, 0.864, so no leak), the
     fatty-liver grade (0.834 without it), AST (0.826 without it against 0.827 with it, on another fold order),
     single-cell entry errors. The task probes' flag `no_spread` is answered: TabPFN beats the other three methods
     by 0.06 to 0.08 on 92-93% of the splits.
   - Implemented: the definition as committed on 2026-10-23; 242 rows, 86 with gallstones.
   - (a) Ship. (b) Discuss.
   - Rule: the rule that class-specific recording conventions are harmonised (LEAK-13, Must); the rule that a task
     whose tuned methods spread stays (TP-3, Must). The full data are not public (shared on request): a note, never
     a reason.
   - Precedent: this dataset is the case behind the `Class-dependent Recording` marker;
     regensburg_pediatric_appendicitis was kept on 2026-10-27 with the same kind of format fix.
   - Recommendation: (a). Decision needed: (a) or (b).

   **Resolved (2026-10-27, Andrej and Lennart):** kept as defined. Andrej kept it with the three changes on
   2026-10-21 (CC), and Lennart kept it "as Andrej marked it" on 2026-10-27 (CC). The merge of 2026-11-04 (Andrej)
   added the decoded target with 1 = gallstones ("Yes"), not 0 as the UCI page and the CC of 2026-11-01 say. The fit
   stays open in issue 2.

2. **Keep the fit `approximate` of your review, or take Lennart's `direct` of 2026-10-27?**

   * **Problem:**
     - Lennart's CC of 2026-10-27 keeps the dataset "as Andrej marked it" with fit `direct`, a call made in the
       review of the selection-bias marker on main's definition, which did not yet have your changes of 2026-10-21.
     - Your review rated the fit `approximate` for two gaps that are not the selection: the fatty-liver grade comes
       from the ultrasound that also finds the gallstones, and the groups were recorded apart.
     - The merge of 2026-11-04 kept `approximate`; which fit stands?
   * **Background:** a selection bias alone does not lower the fit, but a known gap between the data and the use case
     does[^2a]. The use case screens outpatients "to decide who goes on to imaging", yet one feature, the liver grade,
     comes from that imaging; and vitamin D was measured for all 86 with gallstones but for 79 of the 156 without.
     Your review kept the liver grade as a real association (TabPFN 3.5 0.834 without it, 0.838 with it) and named
     the gap in `fit_reason`.
   * **Effect on the task:** none on the data or the scores; the fit is shown with the task, and a direct fit counts
     towards the record's priority.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | `approximate` (implemented) | `fit_reason` names the ultrasound grade and the separate recording of the groups | names both gaps of the shipped features | departs from Lennart's last line on the fit |
     | B | `direct` | `fit_reason` names the narrow base and the unstated selection only | follows Lennart's line | hides that one feature comes from the imaging the use case decides on |

   * **Recommendation:** A: Lennart's call answered the selection question only, on a definition without the two gaps
     your review found. **Decision:** approximate (A) or direct (B)?

   **Notes for the AI:** either way, add a dated CC line stating the fit, and one saying that the target is decoded
   with 1 = gallstones (the merge of 2026-11-04), superseding "0 means gallstones present (UCI)" in the CC of
   2026-11-01. On B, set `fit="direct"` and rewrite `fit_reason` from main's version (the narrow base, the unstated
   selection), keeping the liver grade's origin in `known`; re-run `dataset check`.

   [^2a]: **USE-8** (Must): an approximate fit is a stand-in with a known gap, named as such; a selection bias does not
     by itself make a fit approximate (amended on the review of the selection-bias marker).

   **Resolved (2026-11-11, Andrej):** A: the fit stays `approximate` (dataset.py unchanged); a CC line in the record
   states the fit and that the target is decoded with 1 = gallstones, superseding "0 means gallstones present (UCI)" in
   the CC of 2026-11-01.

   **Andrej (2026-11-11, ok):**

   **Answer (AI, 2026-11-11):** A confirmed, and it cannot be carried out on this branch: the `dataset.py` here is
   the one from before the rework the issue argues about, so "dataset.py unchanged" would leave the wrong fit.

   * This branch's definition is the 319-row version: `fit="direct"`, a `fit_reason` naming only the narrow base
     and the unstated selection, `Hyperlipidemia` dropped by name rather than by the recording test, the target
     decoded with 0 = gallstones, and no second-route filter. It has none of the 2026-10-21/11-04 changes the
     review describes (242 rows, the dropped second recording route, the rounded measured values).
   * Setting `fit="approximate"` alone here would name no gap: the `fit_reason` that carries the two gaps (the
     fatty-liver grade read off the imaging the use case decides on, and the groups recorded apart) belongs to the
     reworked definition, and the second gap is written as "dropped here", which is not true on this branch.
   * Nothing was changed in `datasets/_dev/tabarena-v0pt2/gallstone_disease/dataset.py`. Once the rework lands on
     this branch, A is already satisfied by it (it carries `fit="approximate"`), and only the CC lines remain.
   * The CC line the notes ask for is in the record, with this qualification: the target decoding "1 = gallstones"
     holds for the reworked definition, not for the one on this branch.

3. **Time basis: name the random split a `StationaryRelation`?**

   * **Problem:**
     - The outpatients were seen over one year, June 2022 to June 2023, and the body-composition scan, the blood tests and the diagnosis come from the same visit, so the target is a present state; the file keeps no visit date and is sorted by class and, among those without gallstones, by sex, so the time is lost.
     - The record's facts, `Samples: Over Time` and `Time: Lost`, fit, and the rule names this dataset as its example of a `StationaryRelation`: gallstones and how they relate to body composition and blood values do not move within a year, beyond the share of patients and the clinic's practice.
     - Name the random split a `StationaryRelation`, argued from the source, or a `ForcedIIDFromTemporal`?
   * **Background:**
     - A prospective study of 454 outpatients of one internal-medicine clinic in Ankara (Esen et al. 2024); the study left out 134 without a gallbladder, and the definition drops 77 of a second recording route (issue 1).
     - The prototypes, by the rule's questions: gallstones can form or be removed, so not `Timeless`; the use case screens later outpatients, so not a `Snapshot`; the visits share no prediction moment, so not a `DelayedTarget`; a present state read at the visit, so a `StationaryRelation`[^3a].
   * **Experiments:** the time probe of 2026-11-06 finds no date column and a raw order that follows the class, the known sort, so no time can be recovered from the file.
   * **Unknown:** whether the two groups were recruited in different months; vitamin D follows the season, so a group seen mostly in winter would carry its label in vitamin D for a reason other than gallstones. The paper gives no visit months; the authors would know.
   * **Effect on the task:** none on the data or the scores; the tag and its line state why a random split stands for the use case.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random split, `StationaryRelation` (implemented) | the shipped split; once PR #50 is in, the tag and a `Time basis:` line | the rule's own example; the diagnosis and every feature come from one visit | argued from the source; the visit months are unknown |
     | B | Random split, `ForcedIIDFromTemporal` | the same split, tagged as forced from temporal[^3b] | says that later patients are not tested | nothing found that moves the relation within one year; the file has no time for the leak test the forced tag asks for |

   * **Recommendation:** A: one year of consecutive outpatients, diagnosed at the visit where every feature is measured. **Decision:** A or B?

   **Notes for the AI:** on A, once PR #50 is in: `data_tags = ("StationaryRelation",)` and a curation bullet `- Time
   basis: StationaryRelation: consecutive outpatients of one clinic, June 2022 to June 2023 (Esen et al. 2024); the
   diagnosis and every feature come from the same visit. The file keeps no visit date (sorted by class and sex), so this
   is argued from the source, not measured; whether the two groups were recruited in different months (vitamin D
   follows the season) is unknown.` No `splits_comment` change. On B, `data_tags = ("ForcedIIDFromTemporal",)` and a
   bullet saying that visit dates would allow a split by month.

   [^3a]: **SPLIT-32** (Should): how the data was collected is information for the split; the record carries the
     collection facts, and a definition can name the use-case prototype it follows with a `Time basis:` line. A
     present state read through a relation that time does not move, beyond prevalence and practice, is a
     `StationaryRelation`, measured on a dated source and argued from the source when the time is lost; the rule's
     cases name gallstone_disease.
   [^3b]: **SPLIT-8** (Must): a task temporal in nature or by its use case whose release cannot give the windows ships
     in the closest regime, tagged as forced from temporal, after a leak test across the split; the definition says
     what a timestamp would change.

   **Answer (AI, 2026-11-06):** `StationaryRelation` now needs a measurement: name the random split forced from temporal
   (a, the issue's B), or leave it without a prototype (b)?

   * **Problem:**
     - On the item "One meaning for `StationaryRelation`, measured or argued?" you wrote "I want this to be always
       measured": the tag now needs a dated source on which the target and its relation to the features are shown flat,
       so option A, argued from the source, no longer exists[^3s].
     - The visits of June 2022 to June 2023 carry no date in the release and no parent source dates them (none
       published; the authors could give the months), so the relation cannot be measured.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Random split, `ForcedIIDFromTemporal` | the issue's B: the tag and a `Time basis:` line saying the outpatients came over one year with no visit date released; visit months would test later outpatients and whether the two groups were recruited in different seasons (vitamin D) | the regime the rules give a forward use case whose time is lost; the split stays | the leak test across the split can check repeats and hidden groups, not periods |
     | b | Random split, no prototype | a `Time basis:` line saying why none fits, no tag | claims nothing | `dataset check` keeps noting the missing basis |

   * **Recommendation:** a: the use case screens later outpatients, and the visit months that would show the relation
     flat are not released. **Decision:** a or b?

   [^3s]: **SPLIT-32** (Should; Andrej, 2026-11-06): a `StationaryRelation` is always measured on a dated source; where
     time is lost it cannot be, and a forward use case takes the forced tag. **SPLIT-8** (Must): the forced split ships
     after its leak test, and its line names the reason and what a dated release would change.

   **Andrej (2026-11-11, discuss):** Test if it is stationary.

   **Answer (AI, 2026-11-11):** not along the file's order: splitting by it costs 0.06-0.07 ROC AUC for every model,
   but the order cannot be shown to be time. So a (forced from temporal) still fits, now backed by a measured drift.

   * The only order is the file's: cases in one block, controls sorted by sex, so "position" = rank within each of
     the three blocks of the 242 rows; a split by it pairs early cases with early controls.
   * Splits along that order are harder than random ones of the same size, and within the first half the task is
     much easier than within the second.
   * Little covariate shift: early vs late is barely told apart (TabPFN 0.58 against a null of 0.49; LR and HGB at the
     null). What moves is the relation: AST and ALT of the controls step up mid-file in both sex blocks (AST median
     16-19 to 21-30), the cases' stay flat, so AST's class AUC goes from 0.42 to 0.23.
   * Is the order time? Not shown: vitamin D has no seasonal wave along any block (p = 0.07-0.63), and its dips sit
     at different places in the two control blocks; the groups were sorted apart, so their early rows need not share
     months. A lab change, a recruitment batch or an unknown sort fit the drift as well.

   | Test (ROC AUC, 242 rows) | LR | HGB | TabPFN 3.5 |
   |---|---|---|---|
   | random half -> other half (20 draws) | 0.764 | 0.755 | 0.827 |
   | early half -> late half | 0.764 | 0.758 | 0.664 |
   | late half -> early half | 0.652 | 0.674 | 0.746 |
   | all 4 contiguous halvings, both ways (mean of 8) | 0.700 | 0.687 | 0.754 |
   | 4 ordered quarters as folds / random 4-fold (x10) | 0.707 / 0.780 | 0.705 / 0.792 | 0.794 / 0.839 |
   | CV within early half / within late half | 0.812 / 0.726 | 0.812 / 0.731 | 0.891 / 0.750 |
   | early vs late, adversarial (null: random halves) | 0.468 (0.456) | 0.519 (0.526) | 0.581 (0.485) |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Random split, `ForcedIIDFromTemporal` | the 2026-11-06 answer's a; its `Time basis:` line adds the drift along the file order (contiguous halves -0.06 to -0.07; the controls' AST step) | rests on a measurement now; split unchanged | random folds score about 0.07 above ordered ones |
     | b | Split by file-order chunks | contiguous quarters of each block as folds | tests the drift | the order is not shown to be time, and the case and control orders need not align; quarter folds vary by 0.10 |
     | c | Random split, no prototype | a `Time basis:` line only, no tag | claims nothing | leaves the measured drift out of the tags |

   * **Recommendation:** a: the relation is not flat along the only order there is, which backs the forced tag, but
     that order is no date, so a split by it would test an unknown sort. Scripts and results in
     `~/claude_jobs/marks_1111/gallstone/` (`stat_test.py`, `diag.py`, `season.py`, `uni.py`). **Decision:** a, b or c?

   **Andrej (2026-11-11, discuss):** It can be a random split, but I would say it is save to assume stationary relation
   based on the use case?

   **Answer (AI, 2026-11-11):** yes, it holds: the drift was measured along the file's sort order, not along time, so
   nothing measured speaks against a stationary relation, and the use case argues for one.

   * The diagnosis and every feature come from one visit, within one year: a present state, as the tag describes.
   * The drift (ordered halves 0.06-0.07 ROC AUC below random halves) sits in the controls' AST and ALT, a step that
     fits a lab or practice change, which the tag allows.
   * It departs from your "always measured" of 2026-11-06: here it is argued from the use case, since no visit date is
     released. SPLIT-32's cases in PR #50 should list it as argued.
   * What the random split cannot test: later outpatients, and whether the two groups came in different months
     (vitamin D follows the season).

   **Resolved (2026-11-11, Andrej):** A (`StationaryRelation`, random split): split unchanged; a `- Time basis:
   StationaryRelation: ...` bullet in `curation_comments` names the one-visit present state, the drift along the file
   order (contiguous halves 0.06-0.07 below random ones, the controls' AST/ALT step, order not shown to be time) and
   what the split cannot test; a CC line in the record. The tag enters `data_tags` once PR #50 is in the working copy.
   `dataset check` (Slurm job 1378123): 0 errors, 0 warnings.

   **Andrej (2026-11-11, discuss):** It can be a random split, but I would say it is save to assume stationary
   relation based on the use case?

   **Answer (AI, 2026-11-11):** The reading holds, as the answer above says, and the bullet it asks for was not
   written into this branch's definition.

   * Nothing measured speaks against a stationary relation: the drift of 0.06 to 0.07 ROC AUC sits along the file's
     sort order (cases in one block, controls sorted by sex), and that order is not shown to be time; vitamin D has
     no seasonal wave along any block (p = 0.07 to 0.63).
   * The use case argues for it: the diagnosis and every feature come from one visit, inside one year of consecutive
     outpatients of one clinic.
   * The `- Time basis: StationaryRelation:` bullet is not in this branch's `curation_comments`: its numbers were
     measured on the 242-row definition, which this branch does not have (see the answer in issue 2). It goes in with
     the rework, together with the `StationaryRelation` tag that waits for PR #50.
   * This departs from "a StationaryRelation is always measured" of 2026-11-06: here it is argued from the use case,
     since no visit date is released. SPLIT-32's cases should list it as argued; the rules under
     `knowledge-curation/references/` were not edited.

## Reference

@article{esen2024early,
  title={Early prediction of gallstone disease with a machine learning-based method from bioimpedance and laboratory data},
  author={Esen, {\.I}rfan and Arslan, Hilal and Esen, Selin Akt{\"u}rk and G{\"u}l{\c{s}}en, Mervenur and K{\"u}ltekin, Nimet and {\"O}zdemir, O{\u{g}}uzhan},
  journal={Medicine},
  volume={103},
  number={8},
  pages={e37258},
  year={2024},
  publisher={LWW}
}
