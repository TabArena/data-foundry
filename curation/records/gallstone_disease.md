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
- Class-dependent Recording
tags:
- Tiny Data
- 'Samples: Over Time'
- 'Time: Lost'
- Clinical Study
collections:
- New (BeyondArena)
original_source: UCI
year: '2025'
collection_period: Jun 2022 - Jun 2023
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

CC (2026-10-21, Andrej): Keep, with three changes to the data in `dataset.py` (not built). 319 outpatients of one Ankara clinic (2022-2023), in the file the 161 without gallstones first, then the 158 with; 242 remain. ROC AUC (3-fold x 20): TabPFN 3.5 0.838 (0.913 on the UCI file), gradient boosting 0.778, random forest 0.773, logistic regression 0.762 (0.857).

**Changes made:**
1. **Problem:** 77 rows (72 with gallstones, 5 without) were recorded through a second route: body fat to two decimals, water in whole kg, obesity % not from BMI, and a lower extracellular share of body water although they are heavier. Models recognise the route, not the disease: TabPFN 3.5 separates these cases from the controls at 0.993, the other cases at 0.842, and gives the 5 such controls a gallstone probability of 0.77 (0.22 for the others). Only 5 controls, so the route cannot be aligned with the other rows. **Change:** the 77 rows are dropped.
2. **Problem:** hyperlipidemia is set for 8 people with gallstones and nobody without, although total cholesterol of 240 mg/dL or more is as common (32 of 158 with, 35 of 161 without): it was recorded for one group only. **Change:** the column is dropped.
3. **Problem:** the number format gives the group away. GFR (kidney filtration rate) has two decimals for 80% of those without gallstones and 15% of those with, and the filled cells (below) carry up to 8 decimals in one group only; formatting alone gives ROC AUC 0.947. **Change:** GFR is written in whole numbers, vitamin D and visceral muscle area to one decimal, CRP (an inflammation marker) and creatinine to two, the precision of their measured values; formatting alone now gives 0.557.
4. **Problem:** UCI documents the label reversed (0 = gallstones), but the paper and the risk factors (57% vs 42% women, more body fat, lower vitamin D, more diabetes in class 1) show 1 = gallstones. **Change:** the task description says 1 = gallstones (86 of 242); the label values stay.
5. **Problem:** the task description did not say that the study left out 134 of its 454 outpatients, those whose gallbladder had been removed. **Change:** the description of a row says so, and that the second route is dropped.
6. **Problem:** the task description listed liver fat as a bioimpedance measure, but the fatty-liver grade comes from the ultrasound that also finds gallstones. **Change:** the list of known features names it as an ultrasound grade.
7. **Problem:** the use-case fit was rated "direct", although the groups were recorded apart and the liver grade needs an ultrasound. **Change:** rated "approximate", with both gaps named.
8. **Problem:** none of this was documented. **Change:** the curation comments describe each problem with its effect on the scores, with a table of the second route and a figure of the filled cells.
9. Record: Andrej added as reviewer (`checked_by`).
10. **Problem:** no marker said that the classes were measured, formatted and filled differently (`Selection Bias` is about which rows were sampled). **Change:** new marker `Class-dependent Recording`.

**Problems found, not changed** (they do not let a model tell the groups apart for reasons other than gallstones):
- Filled-in cells: 134 of the remaining values were filled with straight lines between the rows above and below (e.g. CRP 5.2, 4.16, 3.12, 2.08, 1.04, 0), although UCI calls the file complete: vitamin D 77 (all without gallstones), visceral muscle area 35 (all with), GFR 13, CRP 6, creatinine 3. Not a leak: re-imputed from the other features inside each training fold, without the label, TabPFN 3.5 reaches 0.864 (0.838 with the fills). Set to missing they would mark the groups, since vitamin D was measured for all 86 with gallstones but only 79 of the 156 without.
- The fatty-liver grade from ultrasound: a real association (TabPFN 3.5 0.834 without it).
- Data-entry errors, e.g. GFR 11.34 where the CKD-EPI 2021 equation gives 111.34, triglyceride 1.39.
- AST (a liver enzyme) is lower with gallstones (median 16.5 against 20), against what biliary disease would suggest, while ALT does not differ; possibly the groups' labs were run differently. It does not carry the score: TabPFN 3.5 0.826 without it, 0.827 with it (same folds).
- The fatty-liver grades look like two scales: no fatty liver about as common in both groups (41% without gallstones, 44% with), mild much rarer with gallstones (6% against 21%), moderate more common (38% against 29%). Small effect (TabPFN 3.5 0.834 without the column, 0.838 with it).
- Task probes flag `no_spread` (untuned linear model, random forest, LightGBM 0.754-0.768), but methods spread: TabPFN 3.5 beats the other three by 0.06-0.08 on 92-93% of the splits.
- Data access: the full data are not public (the paper: third-party data, shared on request); UCI lists the paper's authors as donors under CC BY 4.0.
- Not `Data Quality Issue`, which is for damage that cannot be repaired: the remaining artefacts do not leak.

Reference: Inker LA, Eneanya ND, Coresh J, et al. New creatinine- and cystatin C-based equations to estimate GFR without race. N Engl J Med. 2021;385(19):1737-1749. doi:10.1056/NEJMoa2102953.

CC (2026-10-27, Lennart): keep it as Andrej marked it: the Selection Bias marker and fit direct (USE-8, amended on the review of PR #16); how the patients were chosen is not stated.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): ordinal scales shipped as numbers, left as numbers for the curator's review: `Hepatic Fat Accumulation (HFA)`.

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 1 ordinal scales shipped as numbers are ordered categories (point 3); Comorbidity's three undocumented 2 and 3 (each with one listed disease) recoded to 1, the rows kept (CLEAN-11); the fat-accumulation grade an ordered category.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `nhanes_iii_gallstones` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 3 coded columns carry their words; the target keeps its codes.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (0 means gallstones present (UCI)).

CC (2026-11-11, Andrej): fit stays `approximate` (Review issue 2, A): the liver grade comes from the ultrasound that finds the gallstones, and the groups were recorded apart; Lennart's `direct` of 2026-10-27 answered the selection question only, on a definition without these changes. The target is decoded with 1 = gallstones ("Yes"; the merge of 2026-11-04, as in the paper and the file: class 1 is 57% women and has lower vitamin D); this supersedes "0 means gallstones present (UCI)" in the CC of 2026-11-01.

CC (2026-11-11, Andrej): random split kept as a `StationaryRelation` (Review issue 3, A): "it is safe to assume stationary relation based on the use case": diagnosis and every feature come from one visit within one year. Argued, not measured (no visit date released). The drift found along the file's sort order (contiguous halves 0.06-0.07 ROC AUC below random halves, the controls' AST/ALT step) is not shown to be time and is named in the `Time basis:` line with what the split cannot test.

CC (2026-11-13, Andrej): the time basis is `ForcedIIDFromTemporal` instead of `StationaryRelation`:
- `StationaryRelation` asks for a measurement on dated data, and the file keeps no visit date (`Time: Lost`), so the stationary relation was argued, not measured.
- The random split stays; the forced tag says what it is: random patients standing in for later ones, with the drift along the file's order and what a dated release would test in the `Time basis:` line.

CC (2026-11-17, Andrej): the declared split (random, 20x3 folds, `ForcedIIDFromTemporal`) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split walk).

CC (2026-11-18, Andrej): the forced tag stays (Review issue 5, A; stationarity reasoning, SPLIT-32 as amended today): no reason to take later samples as interchangeable. The mechanism and one-year span would support ASR, but the measured drift along the file order is an explicit fact against; mixed, so forced.

## Review

**Outcome:** added. Of the 319 outpatients of one Ankara clinic (2022-2023) in the UCI file, 242 remain, and the task is
whether they have gallstone disease (86 do), from body composition, an ultrasound liver grade and blood tests. Kept on
review (issue 1): Andrej's changes of 2026-10-21 (a second recording route, a column recorded for one group and the
number formats removed; LEAK-13) and Lennart's keep of 2026-10-27; the merge of 2026-11-04 decodes the target with
1 = gallstones. Value: tuned methods spread (TP-3); TabPFN 3.5 0.838, gradient boosting 0.778, logistic regression
0.762 ROC AUC. Quality: filled cells, the ultrasound grade and entry errors are kept with their measured effect
(`Class-dependent Recording`, `Selection Bias`). A question on `CrossSectional` (2026-11-13) was withdrawn when the
prototype was dropped.

**Main points:** Nothing open. Fit `approximate` (issue 2, A, 2026-11-11). Time basis: the `StationaryRelation` of
issue 3 (2026-11-11) was replaced by `ForcedIIDFromTemporal` on 2026-11-13; issue 4 withdrawn on 2026-11-13; the
forced tag stays (issue 5, A, 2026-11-18).

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
     | A | Random split, `StationaryRelation` (implemented) | the shipped split; once the time-basis tags are in, the tag and a `Time basis:` line | the rule's own example; the diagnosis and every feature come from one visit | argued from the source; the visit months are unknown |
     | B | Random split, `ForcedIIDFromTemporal` | the same split, tagged as forced from temporal[^3b] | says that later patients are not tested | nothing found that moves the relation within one year; the file has no time for the leak test the forced tag asks for |

   * **Recommendation:** A: one year of consecutive outpatients, diagnosed at the visit where every feature is measured. **Decision:** A or B?

   **Notes for the AI:** on A, once the time-basis tags are in: `data_tags = ("StationaryRelation",)` and a curation bullet `- Time
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
     that order is no date, so a split by it would test an unknown sort. **Decision:** a, b or c?

   **Andrej (2026-11-11, discuss):** It can be a random split, but I would say it is save to assume stationary relation
   based on the use case?

   **Answer (AI, 2026-11-11):** yes, it holds: the drift was measured along the file's sort order, not along time, so
   nothing measured speaks against a stationary relation, and the use case argues for one.

   * The diagnosis and every feature come from one visit, within one year: a present state, as the tag describes.
   * The drift (ordered halves 0.06-0.07 ROC AUC below random halves) sits in the controls' AST and ALT, a step that
     fits a lab or practice change, which the tag allows.
   * It departs from your "always measured" of 2026-11-06: here it is argued from the use case, since no visit date is
     released. SPLIT-32's cases should list it as argued.
   * What the random split cannot test: later outpatients, and whether the two groups came in different months
     (vitamin D follows the season).

   **Resolved (2026-11-11, Andrej):** A (`StationaryRelation`, random split): split unchanged; a `- Time basis:
   StationaryRelation: ...` bullet in `curation_comments` names the one-visit present state, the drift along the file
   order (contiguous halves 0.06-0.07 below random ones, the controls' AST/ALT step, order not shown to be time) and
   what the split cannot test; a CC line in the record. The tag enters `data_tags` once the time-basis tags are in.

   Replaced on 2026-11-13 (CC): the time basis is `ForcedIIDFromTemporal`, since a `StationaryRelation` needs a measurement on dated data; kept on 2026-11-18 (issue 5).

4. **`CrossSectional` instead of `ForcedIIDFromTemporal`?**

   * **Problem:**
     - The definition is tagged `ForcedIIDFromTemporal`, a forward use case whose time was lost[^fo-1].
     - The target is a present state measured with the features: the diagnosis at the visit, read from the same visit's laboratory values and body composition, and the use case reads it for new units at their own present[^cs-1].
     - The tag alone changes: the split stays random.
   * **Background:** you made the tag `ForcedIIDFromTemporal` on 2026-11-13, before `CrossSectional` existed, because `StationaryRelation` cannot be measured without dates. The use case is screening at the visit where the diagnosis is made, a present state, which `CrossSectional` now names without claiming a measurement.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Stay `ForcedIIDFromTemporal` (implemented) | the tag and its line stay | the decision stands | the tag claims a forecast the use case does not make |
     | B | `CrossSectional` | the tag and a `Time basis:` line naming the present state, the untested drift for later units and what a dated release would show | names the use case; no claim of a lost forward split | a new prototype on a decided tag |

   * **Recommendation:** B. **Decision:** A or B?

   **Notes for the AI:** on B, swap the tag, write the line, add a CC line; the split does not change.

   [^cs-1]: **SPLIT-32** (Should, 2026-11-13): a target measured together with the features, which the use case reads for new units at their own present, is `CrossSectional`, whether the dates survive or not; its line says whether the drift of the relation was measured or is untested. A label that only arrives later is no present state.
   [^fo-1]: **SPLIT-8** (Must): a forward use case without usable time ships in the closest regime, tagged forced from temporal, with a `Time basis:` line naming the reason.

   **Resolved (2026-11-13, Andrej):** withdrawn: `CrossSectional` was dropped the same day (it named no split the existing prototypes do not give: a present state used later is forced or a measured `StationaryRelation`, used within the covered time `Retrospective`). The tag stays.

5. **Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?**

   * **Problem:**
     - Time: Lost: no visit date (outpatients June 2022 to June 2023, Esen et al. 2024); the file order (rank within sorted blocks) is not shown to be time.
     - Use: An internal-medicine clinic screens outpatients for imaging referral, right after or a few years after 2022-23.
     - Mechanism: Bioimpedance body composition and routine labs (lipids, liver enzymes, CRP, vitamin D) vs ultrasound-confirmed gallstones: largely physiology and physical measurement, little practice dependence.
   * **Background:** similar datasets[^asr].

     | Similar dataset or source | What was measured | Verdict | Why similar |
     |---|---|---|---|
     | gallstone_disease's own file order | contiguous half vs random halves | not flat along the order: 0.06-0.07 ROC AUC lower, AST/ALT of controls step up mid-file | same data |
     | infrared_thermography_temperature | v3 test over 12 months 2016-18 | flat | only physical-measurement case: shows what a fixed-instrument mechanism looks like (contrast) |
     | Davis SE et al., 'Calibration drift in regression and machine learning models for acute kidney injury', JAMIA 2017;24(6):1052-1061 (literature, cited from memory: check) | VA hospital models over 9 years | discrimination stable, calibration drifted | routine-lab clinical risk model used years after fitting |

   * **For a stationary use case:**
     - one year of collection, use within or right after it is plausible.
     - body composition and labs are physical/physiological measurements.
     - curator argued StationaryRelation on 2026-11-11.
   * **Against:**
     - structure in the file order: half-vs-half costs 0.06-0.07 ROC AUC.
     - controls and cases possibly recruited in different months (vitamin D seasonal); selection unstated.
     - lab assays/analysers vary by site and over time.
   * **Earlier views:**
     - CC 2026-11-13 (Andrej): ForcedIIDFromTemporal instead of the curator's StationaryRelation (2026-11-11), which was argued, not measured.
     - Resolved 2026-11-13 (Andrej, issue 4): CrossSectional withdrawn, tag stays.
     - CC 2026-11-17 (Andrej): forced random split checked by blind walk.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedIIDFromTemporal` (implemented) | The folds stay; the Time basis line names the reasoning below | Claims only what is known | The split stands for later samples only as far as the use case is stationary |
     | B | `AssumedStationaryRelation` | The folds stay; you give the reason (eight words or more) | Documents why random folds stand for later samples | structure in the file order: half-vs-half costs 0.06-0.07 ROC AUC; controls and cases possibly recruited in different months (vitamin D seasonal); selection unstated |

   * **Recommendation:** A, the mechanism and one-year span would support ASR, but the measured drift along the file order is an explicit fact against; mixed, so forced. Confidence: medium. **Decision:** A or B?

   [^asr]: **SPLIT-32** (Should; amended 2026-11-18, Andrej): "where it holds none, the review reasons whether the use case can be taken as stationary, from the domain's mechanism and from similar datasets ..., where the AI offers `AssumedStationaryRelation` with a recommendation for a person to decide." `AssumedStationaryRelation` keeps the forced split's folds and replaces only the tag; its line opens `AssumedStationaryRelation (<person>, <date>): <reason>`.

   **Andrej (2026-11-18, ok):** as implemented.

   **Resolved (2026-11-18, Andrej):** A, as implemented: the forced tag stays; the `Time basis:` line gives the reasoning (The mechanism and one-year span would support ASR, but the measured drift along the file order is an explicit fact against; mixed, so forced.)

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
