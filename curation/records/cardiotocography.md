---
unique_name: cardiotocography
name: Cardiotocography
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Wrong Domain / Source Modality
- Time-series (Classification)
tags:
- 'Samples: Over Time'
- 'Time: Dated'
- Non-IID (Temporal)
collections:
- TabArena Reject
original_source: UCI
year: '2010'
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/193/cardiotocography
- https://doi.org/10.24432/C51S4N
notebook_path: datasets/beyond_iid/grouped/cardiotocography/cardiotocography.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/cardiotocography/dataset.py
source_row: 693
type_adapter_id: curation-record-v1
---

## Comments

The label is the consensus of three experts (so likely noisy).

Can be either 10 or 3 class problem.
Raw data has dates!


From going through the raw data description, it seems one had one or multiple measurements per patient and split it into multiple rows or segments and then created tabular features. Targets can be different per instance. Need to take raw data to get the group IDs.

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: DS (DR is constant 0 and stays as it is).

CC (2026-10-21, Lennart): on which 0/1 columns are flags: "no if we can infer from the semantic context, keep it a number, this is a real-world bias. We want to make things categorical if we know from the context they are indeed such" (CLEAN-14, amended again). Reverted: DS (severe decelerations per second, a measured rate) stays numeric.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — UCI page defines no task metric; the SisPorto 2.0 paper describes the analysis program and expert agreement, not a prediction benchmark.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): ordinal scales shipped as numbers, left as numbers for the curator's review: `Tendency`.

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 1 ordinal scales shipped as numbers are ordered categories (point 3).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `jnu_ctg_fetal_wellbeing` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 1 coded columns carry their words.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target is an ordered category, normal < suspect < pathologic.

CC (2026-11-11, Andrej): split by exam date (Review issue 2, reply (b) "Reply (b): Windows by exam date"; issue 1 settled by it, "discussed in issue 2", shipped as defined).

- `Date` is kept as `exam_date` (a datetime feature and the time column) and the 56 segments dated 1980-01-04 (an unset clock) are dropped: 2,070 segments of 335 files.
- Three nine-month windows from October 1996, July 1997 and April 1998, each trained on all earlier exams (60%, 74% and 89% of the segments); the inferred patient key leaves the frame, and `DR` (0 in every row) is dropped.
- The labels shift between 1996 and 1997 (suspect 14% to 1%, pathologic 4% to 13%); trained on earlier exams, untuned LightGBM's log loss on the two newest windows is 1.825 and 1.608, against 0.498 and 0.444 trained on as many segments of all years (Slurm job 1365902). The grouped split hid that shift; it leaked nothing, but it does not use the date either.
- Record: `required_split` Temporal (NON-IID), tag `Non-IID (Temporal)` in place of `Non-IID (Grouped)`.
- `dataset check`: 0 errors, 2 warnings accepted with reasons in the definition (the newest window ends on 1998-06-06; no suspect segment in the July 1997 to March 1998 window).

**Assessment (AI, 2026-11-11):** split-row mark ("Could we also do more splits for better signal?"), opened as Review issue 3 and measured (Slurm jobs 1378380 and 1378382). More windows are possible only by cutting on the exam count, not on the calendar: the 2,070 segments come from 47 exam dates in bursts of 1 to 240, so 6-month windows leave one window with 17 segments and 3-month windows leave one with none. Windows of equal segment count keep 102 to 324 segments each and lower the standard error of a paired method comparison from 0.63 to 0.40-0.46 (untuned LightGBM against standardised logistic regression, multiclass log loss), but the gap between the two is three to four standard errors wide in every layout and logistic regression wins in every single window, so no layout changes the verdict. Recommended: keep the three nine-month windows; the equal-count layout is written down in the issue for a later close comparison. The curator has the call.

## Review

**Outcome:** added. The UCI Cardiotocography table (UCI 193, https://doi.org/10.24432/C51S4N), measured by the SisPorto
2.0 program (Ayres-de-Campos et al., "SisPorto 2.0: a program for automated analysis of cardiotocograms", Journal of
Maternal-Fetal Medicine 2000;9(5):311-318, https://doi.org/10.1002/1520-6661(200009/10)9:5<311::AID-MFM12>3.0.CO;2-9):
2,126 segments of 352 fetal heart-rate recordings, 22 automatic measures of each segment, and the fetal state three
expert obstetricians agreed on (normal 78%, suspect 14%, pathologic 8%); split by a patient key inferred from the file
names, log loss (fallback). The AI recommends shipping it as defined. Reviewed on 2026-11-04 without a panel, from the
gathered evidence (the record, the CHANGELOG, a model run on the shipped data) and one check. Validity: the
label is the experts' reading of the trace and the features are the program's measures of the same segment, the
inputs of that reading rather than the reading itself; the 10-class pattern label and its one-hot columns, which encode
the reading, are dropped; a model of the guideline's thresholds (no accelerations, reduced variability,
prolonged decelerations) ranks 3rd of 41, so the label follows the guideline without being read off one feature; the
segment's length, which the definition drops while the event columns are counts per segment, is not tied to the class
(checked). Value: on the shipped splits the 40 benchmark methods spread from log loss 0.205 (TabPFN-3.5) over a median
of 0.236 to 0.341 (default logistic regression), so the methods separate. Quality: `DR` is constant; the patient key is
a heuristic the notes describe. Weighed: an established clinical program's measures with an expert label +, a grouped
split +, a clear spread +, an inferred patient key and a 1990s Portuguese hospital -.

**Main points:** Keep the three nine-month windows, or cut more of them (issue 3)? Shipped (issue 1) with the
split by exam date, under which the labels shift between 1996 and 1997 (issue 2, resolved 2026-11-11).

**Record judgment:** valid. The record keeps the TabArena rejection markers `Wrong Domain / Source Modality` and
`Time-series (Classification)` next to Lennart's `Yes`; the raw traces are not in the release, and the program's measures
are what clinical software reports, so the markers read as history, not as a reason against. The house rule drops a
constant column, so `DR` (0 in every row, bundle warning) goes at the next edit; no decision is needed. The data
scouting found `jnu_ctg_fetal_wellbeing` (20,769 recordings, 2026, not verified); it is screened in its own record and
does not change this task's validity. The metric review proposes an ordinal score on its own page.

**Issues for Andrej:**

1. **Ship as defined?**

   * **Problem:**
     - Nothing open was found: no feature gives the experts' reading away, the overlapping segments of one recording
       stay together in the split, and the methods spread.
     - The label is an expert judgement of the trace, not the baby's outcome, and the patient key is inferred from file
       names, both stated in `fit_reason`.
     - Ship as defined, or retire?
   * **Background:** each row is a segment of a recording, and 1,706 of the 1,774 consecutive segment pairs within a
     file overlap; the key merges files with the same name stem (176 keys for 352 files), which can only make the split
     stricter.
   * **Experiments:** check of 2026-11-04 on the UCI file: the segment length (`e - b`, 117 to 3,599 samples) separates
     neither pathologic from the rest (ROC AUC 0.53) nor suspect from normal (0.51), and the event counts score as
     their per-second rates do on their own (accelerations 0.808 against 0.809, contractions 0.677 against 0.687).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship as defined (implemented) | 2,126 segments, 22 features, split by inferred patient, log loss | an established program's measures with an expert label; the methods separate | the label is a judgement; the patient key is a guess |
     | B | Retire | `No (Retired)`, a CC line, the folder removed | none found beyond the TabArena modality markers | no defect of the data found; reverses Lennart's `Yes` |

   * **Recommendation:** A: a valid task whose methods spread[^1a]. **Decision:** A or B?

   [^1a]: **TP-3** (Must): if tuned methods spread, keep the dataset. **SEL-14** (Must): readings that real tabular
     models take as inputs stay in scope when the reading is the established clinical result tabular models are used on.

   **Andrej (2026-11-10, discuss):** Does the grouped split introduce leaks or not?

   **Answer (AI, 2026-11-10):** no, the grouped split brings in no leak; it removes one. The measurements are in issue
   2's answer.

   * A random split would leak: 93% of its test segments overlap a training segment of the same exam.
   * The patient groups never cross a fold, and the exam year is not in the frame.

   **Andrej (2026-11-11, discuss):** discussed in issue 2.

   **Resolved (2026-11-11, Andrej):** A, shipped with issue 2's split by exam date: the dataset stays; no retirement.

2. **Split by time, or keep the grouped split without a measured time basis?**

   * **Problem:**
     - The raw sheet dates every exam (January 1995 to June 1998), the definition drops the date, and between 1996 and
       1997 the experts' labels change sharply: suspect falls from 14% of the segments to 1%, pathologic rises from 4%
       to 13%.
     - Monitoring software meets later exams, so the exam date is information for the split, and the cost is too large
       to show a stationary relation: trained on earlier exams, LightGBM's
       log loss on the two newest windows is 1.6 to 1.8, against 0.44 to 0.50 when trained on as many segments of all
       years[^2a].
     - Split by exam date, or keep the patient split without a measured time basis?
   * **Background:** `Date` is in the "Raw Data" sheet of `CTG.xls`; each file has one date, so the overlapping
     segments of an exam never straddle a cut by date. 56 segments of 5 name stems carry 1980-01-04, an unset clock, so
     they have no usable date. Segments per year: 313 (1995), 1,174 (1996), 330 (1997), 253 (1998); labels normal,
     suspect and pathologic 50%, 36% and 14% in 1995, 83%, 14% and 4% in 1996, 86%, 1% and 13% in 1997, 80%, 2% and
     18% in 1998. Three windows of nine months, October 1996 to June 1997 (307 segments, 27 files), July 1997 to March
     1998 (305, 26 files) and April to June 1998 (224, 14 files), train on 60%, 74% and 89% of the dated segments.
   * **Experiments:** the 2,126 shipped segments and 22 features, untuned LightGBM and logistic regression, log loss
     (Slurm job 1365902):
     - Shipped split by patient (10 x 3): LightGBM 0.358 (0.207 to 0.570), logistic regression 0.367.
     - The three windows, each trained on all earlier dated segments: LightGBM 1.789 (April to June 1998, the newest),
       1.570 (July 1997 to March 1998) and 0.449 (October 1996 to June 1997); logistic regression 0.768, 0.632 and
       0.351.
     - Same test segments and same training size (each window in 3 folds by patient, 3 seeds; earlier exams only
       against dated segments of all years, the fold's patients left out): LightGBM 1.825 against 0.498, 1.608 against
       0.444 and 0.455 against 0.464; logistic regression 0.767 against 0.406, 0.659 against 0.191 and 0.339 against
       0.311.
     - What changes: trained on earlier exams, LightGBM calls 74 of the 182 normal segments of spring 1998 suspect or
       pathologic (24 when trained on all years) and 23 of the 50 pathologic segments of late 1997 suspect.
     - Leaving the test window's patients out of training changes little: an earlier exam of the same patient is in
       training for 20% of the oldest window's segments and for 0% to 1% in the other two.
   * **Effect on the task:** under the patient split a test segment is scored by a model that learned its own year's
     label mix from other patients of that year; software trained on earlier exams meets a different reading.
   * **Unknown:** whether the change lies in the experts' reading, in which exams were sent for classification, or in
     the program's measures; the source (Ayres-de-Campos et al. 2000) or the authors would say.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Patient split, as a stationary relation by your reading (implemented) | 10 x 3 folds by inferred patient; the definition gets the tag `StationaryRelation` and a `Time basis:` line: the exam date is in the raw sheet, the yearly label mix read as a selection of the collection, and a split by date raises LightGBM's log loss on the two newest windows from 0.44-0.50 to 1.6-1.8 at equal training size | 30 splits over all years; every class in every test fold | the measurement does not show the prototype, so it rests on your reading alone; the score hides a change of the labels between 1996 and 1997 that deployed software meets |
     | B | Three windows by exam date | the date kept as the time column, the 56 segments dated 1980 dropped; test October 1996 to June 1997, July 1997 to March 1998 and April to June 1998, each trained on all earlier exams | tests later exams, as software meets them; the change of labels becomes part of the task | the newest windows hold 0 and 5 suspect segments; the task then largely measures a shift whose cause is unknown |

   * **Recommendation:** B: the date is in the source, the use case meets later exams, and the measured cost is the
     largest of the datasets checked, so keeping the patient split would hide what deployed software meets. If you
     read the yearly label mix as a selection of the source's collection rather than a change over time, A as a
     stationary relation with that reason, which the measured cost does not show. **Decision:** A or B?

   **Notes for the AI:** on B, keep `Date` as `exam_date` in `_clean`, drop the 56 rows dated 1980-01-04 (an unset
   clock), and declare `Temporal(on="exam_date", splits=TemporalSplits(window=9, unit="months",
   cutoffs=("1996-10-01", "1997-07-01", "1998-04-01")))` in place of the grouping (one regime per definition; an
   exam's segments share its date, so they stay on one side); `patient_id` leaves the frame; `split`, `changes`,
   `fit_reason` and `splits_comment` say why (the label mix by year, the cost); the record's `required_split` becomes
   Temporal, tag `Non-IID (Temporal)`; `dataset check`, and recount the classes per test window. On A, once PR #50 is
   in: `data_tags = ("StationaryRelation",)` if you read the label mix as a selection (else no time-basis tag), and a
   curation bullet `- Time basis: StationaryRelation: every exam is dated in the
   raw sheet (January 1995 to June 1998; 56 segments carry an unset clock), and the labels shift between
   1996 and 1997 (suspect 14% to 1%, pathologic 4% to 13%); not split by date, because <the curator's reason>; three
   nine-month windows from October 1996 raise untuned LightGBM's log loss to 1.825 and 1.608 on the two newest, against
   0.498 and 0.444 trained on as many segments of all years (logistic regression 0.767 and 0.659 against 0.406 and
   0.191).` The frame has no date column on A, so no warning to accept. Under either option the record gets the tags
   `Samples: Over Time` and `Time: Dated`. Results: Slurm job 1365902.

   [^2a]: **SPLIT-32** (Should): how the data was collected is information for the split; the record's collection
     facts and, where one fits, the definition's use-case prototype with its `Time basis:` line. **SPLIT-14** (Must):
     at least 3 windows,
     none training on less than half of the data. **SPLIT-3** (Must): a task is grouped or temporal, never both; the
     split decides which dependency the test measures.

   **Andrej (2026-11-10, discuss):** Does the grouped split introduce leaks or not?

   **Answer (AI, 2026-11-10):** no. The grouped split removes the one real leak, the overlapping segments of an exam.
   What it leaves is the change of labels over the years, which is a shift, not a leak (this issue).

   | Split (10 x 3) | Test segments overlapping a training segment | Files / patients on both sides | LightGBM log loss | Logistic regression |
   |---|---|---|---|---|
   | Random segments | 93% | 319 / 169 | 0.285 | 0.244 |
   | Grouped by exam file | 0% | 0 / 61 | 0.427 | 0.269 |
   | Grouped by inferred patient (shipped) | 0% | 0 / 0 | 0.448 | 0.345 |
   | Shipped, exam year added as a feature | 0% | 0 / 0 | 0.370 | 0.353 |
   | Exam year alone (training class mix per year) | | | 0.659 | |
   | Class shares alone | | | 0.687 | |

   | Pairs of segments | Same label |
   |---|---|
   | Same exam file | 84% |
   | Same patient key, any file | 74% |
   | Same patient key, different files (each file's main label) | 55% (chance 57%) |
   | Any two segments (chance) | 63% |

   * The label is shared within an exam, not within a patient key: files merged under one name stem agree no more than
     chance. Merging them makes the split stricter and leaks nothing.
   * The year carries information that the 22 measures do not: adding it lowers LightGBM's log loss from 0.448 to 0.370.
     The patient split mixes all years in training and test, so it hides this shift. It does not use it.
   * The windows by exam date (this issue) show the cost: 1.6 to 1.8 on the two newest windows.
   * Untuned LightGBM (300 trees), standardised logistic regression; script
     `~/claude_jobs/marks_1110/cardiotocography/split_leak.py`.

   | | Option | What it does | Pro | Con |
   |---|---|---|---|---|
   | a | Patient split (implemented) | as now (option A above) | no leak; every class in every fold | hides the change of labels between 1996 and 1997 |
   | b | Windows by exam date | option B above | tests later exams, as software meets them | few suspect segments in the newest windows |

   * **Recommendation:** b, as before. The grouping leaks nothing, but the year shift is real and deployed software
     meets it. **Decision:** a or b?

   **Andrej (2026-11-11, discuss):** Reply (b): Windows by exam date

   **Resolved (2026-11-11, Andrej):** b (B): split by exam date. `_clean` keeps `Date` as `exam_date` (a datetime
   feature and the time column) and drops the 56 segments dated 1980-01-04; `temporal = Temporal(on="exam_date",
   splits=TemporalSplits(window=9, unit="months", cutoffs=("1996-10-01", "1997-07-01", "1998-04-01")))` replaces the
   grouping, and `patient_id` leaves the frame. `DR` (constant) dropped as the record judgment planned. `split`,
   `changes`, `row`, `fit_reason`, curation notes and `splits_comment` rewritten. Record: `required_split` Temporal
   (NON-IID), tag `Non-IID (Temporal)`, CC line; `Samples: Over Time` and `Time: Dated` were already there.
   `dataset check` (Slurm job 1377585): 0 errors, 2 warnings accepted with reasons (`meta_time_horizon_mismatch`: the
   newest window holds 6 April to 6 June 1998 only; `splits_test_class_missing`: no suspect segment in July 1997 to
   March 1998).

   | Test window | Train segments (share of 2,070) | Test segments | Normal | Suspect | Pathologic |
   |---|---|---|---|---|---|
   | April to June 1998 | 1,846 (89%) | 224 | 182 | 5 | 37 |
   | July 1997 to March 1998 | 1,541 (74%) | 305 | 255 | 0 | 50 |
   | October 1996 to June 1997 | 1,234 (60%) | 307 | 252 | 46 | 9 |

3. **More test windows, for a better-separated comparison?**

   * **Problem:**
     - The split of issue 2 tests 836 of the 2,070 dated segments in three nine-month windows, so a comparison of two
       methods rests on three numbers.
     - The exams fall on 47 dates in bursts of 1 to 240 segments, so a shorter calendar window can hold 17 segments
       or none at all.
     - Keep the three nine-month windows, or cut more windows?
   * **Background:** every training side must hold at least half of the segments, and a layout needs at least three
     windows[^3a]; the earliest cut that keeps half in training is 31 August 1996 (51%), and the data ends on 6 June
     1998, so every window lies in the last 21 months. Windows below about 50 test rows are to be widened rather than
     multiplied[^3b].
   * **Experiments:** untuned LightGBM and standardised logistic regression, multiclass log loss, one fit per window
     (Slurm jobs 1378380 and 1378382; `~/claude_jobs/marks_b2/ctg_windows/`). The featurisation is the quick one of
     this run, so the log losses are not the numbers of issue 2's run; only the comparison between layouts is meant.

     Finer calendar windows run empty (segments per test window, oldest first):

     | Calendar layout | Test segments per window |
     |---|---|
     | 3 windows of 9 months (implemented) | 307, 305, 224 |
     | 4 windows of 6 months | 307, 17, 288, 224 |
     | 5 windows of 4 months | 274, 33, 17, 259, 176 |
     | 7 windows of 3 months | 253, 54, 0, 17, 259, 29, 224 |

     Windows of equal segment count, cut on exam dates, keep every window usable, and more of them tighten the paired
     comparison:

     | Layout | Windows | Test segments | Windows with all three classes | Mean log loss difference (LightGBM - logistic regression) | Standard error | Logistic regression better in |
     |---|---|---|---|---|---|---|
     | 3 calendar windows of 9 months (implemented) | 3 | 224-307 | 2 | 1.69 | 0.63 | 3 of 3 |
     | 3 windows of equal count | 3 | 266-405 | 3 | 1.44 | 0.64 | 3 of 3 |
     | 4 windows of equal count | 4 | 174-324 | 2 | 1.38 | 0.46 | 4 of 4 |
     | 5 windows of equal count | 5 | 174-233 | 3 | 1.49 | 0.43 | 5 of 5 |
     | 6 windows of equal count | 6 | 102-232 | 3 | 1.39 | 0.40 | 6 of 6 |

   * **Effect on the task:** more windows cut the standard error of the paired difference by about a third, but the
     gap between the two methods is three to four standard errors wide in every layout and its direction never
     changes, so no layout changes what the comparison says. The windows also stay calendar periods only in A.
   * **Unknown:** whether the benchmark methods, which sit far closer together than these two, separate as clearly;
     that shows after a rebuild.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Three nine-month windows (implemented) | as decided in issue 2 | calendar windows a reader can date; 224 to 307 test segments each | three comparison points; the middle window holds no suspect segment |
     | B | Four to six windows of equal segment count | cuts at exam dates so each window holds about the same number of segments | a third less noise in a paired comparison; more windows hold all three classes | the windows are no longer calendar periods, and the cut dates are an artefact of how many exams a day brought |
     | C | Finer calendar windows (3 to 6 months) | shorter windows of the same kind | more windows | windows of 0 to 54 segments; below the floor for a window's size |

   * **Recommendation:** A. The three windows already separate these two methods by three to four standard errors,
     and the exams arrive in bursts, so more windows buy noise reduction at the price of windows that are no longer
     periods. B is the one worth having if a close method comparison later needs the extra precision.
     **Decision:** A, B or C?

   **Notes for the AI:** on B, replace `TemporalSplits(window=9, unit="months", cutoffs=...)` with the cut dates of
   the chosen k (the script prints them: k=4 gives 1996-08-31, 1996-10-03, 1997-10-01, 1998-03-23), state in
   `splits_comment` that the windows hold about equal numbers of segments rather than equal periods, re-check the
   accepted warnings (the horizon warning changes with the window length), and re-run `dataset check`.

   [^3a]: **SPLIT-14** (Must): at least 3 windows, none trained on less than half of the data.
   [^3b]: **SPLIT-17** (Should): widen windows that get too small; below about 50 test rows per window use wider
     windows and fewer splits, since finer windows add no test rows and only cut the test pool into noisier pieces.
     Its case is coffee_rating_prediction, where 26 monthly windows of 2 to 72 reviews doubled the confidence
     interval of a model comparison.

   **Andrej (2026-11-11, discuss):** Could we also do more splits for better signal?

   **Answer (AI, 2026-11-11):** yes, but only by cutting on the exam count, not on the calendar, and the gain is
   small. Finer calendar windows land empty (table above: a three-month layout has a window with no exam at all),
   because the 2,070 segments come from 47 exam dates. Windows of equal segment count keep 102 to 324 segments each
   and lower the standard error of the paired difference from 0.63 to 0.40-0.46, but every layout gives the same
   verdict with the same direction in every single window, so the extra windows change no conclusion. The shift the
   split is chosen to test also keeps the newest windows short of suspect segments whichever way they are cut.
   Recommendation: A, keep the three windows; B is written down for the day a close comparison needs it.

## Reference

@misc{cardiotocography_193,
  author       = {Campos, D. and Bernardes, J.},
  title        = {{Cardiotocography}},
  year         = {2000},
  howpublished = {UCI Machine Learning Repository},
  note         = {{DOI}: https://doi.org/10.24432/C51S4N}
}
