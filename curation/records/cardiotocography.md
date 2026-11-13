---
unique_name: cardiotocography
name: Cardiotocography
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 3
decision_markers:
- Wrong Domain / Source Modality
- Time-series (Classification)
tags:
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Entities: Recur'
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

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship as defined: the expert reading is not read off any single SisPorto measure, the overlapping segments stay together in the grouped split, and the methods spread (log loss 0.205 to 0.341). Priority 3: gap 1, use case 0, source 1, shape 1, risk -1.

CC (2026-11-11, Andrej): split by exam date (issue 2 (b), "Reply (b): Windows by exam date"; issue 1 settled by it): `Date` kept as `exam_date`, the 56 segments dated 1980-01-04 (an unset clock) dropped, three nine-month windows from October 1996, July 1997 and April 1998, each trained on all earlier exams (60%, 74%, 89% of 2,070 segments); the inferred patient key leaves the frame; `DR` (constant) dropped. `required_split` Temporal (NON-IID), tag Non-IID (Temporal). The labels shift between 1996 and 1997 (suspect 14% to 1%, pathologic 4% to 13%); on the two newest windows untuned LightGBM's log loss is 1.825 and 1.608 against 0.498 and 0.444 trained on all years (Slurm job 1365902).

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

**Main points:** all settled: shipped (issue 1), split by exam date in three nine-month windows (issues 2 and 3).

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
   * Untuned LightGBM (300 trees), standardised logistic regression.

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

3. **More splits for a steadier score?**

   * **Problem:**
     - Andrej's note on the split (2026-11-11): "Could we also do more splits for better signal?"
     - More windows do not steady the score: the model ranking stays the same, and the score's relative error and the
       share of model pairs that swap places barely move, because finer windows reuse the same test exams.
     - Keep the three nine-month windows, or cut the test exams into more windows?
   * **Background:** the exams fall on 47 dates. The 50% floor (every train side at least half of the segments)
     leaves the exams from 31 August 1996 for testing: 1,010 segments of 84 exam files. The shipped windows start in
     October 1996 and test 836 segments of 67 files. Repeating a window adds nothing: the windows are fixed and the
     models are deterministic, so repeats would only re-draw model seeds, not new test exams.
   * **Experiments:** Slurm job 1378287, six untuned models (LightGBM, logistic regression, random forest, extra trees,
     HistGB, kNN). Score = mean log loss over the windows. SE = bootstrap of the test exam files within each window
     (2,000 draws). Pair swaps = share of draws in which a pair of the 6 models changes order, averaged over the 15 pairs.

     | Windows | Test exams (segments) | Smallest train | LightGBM ± SE | SE / score | Logistic regression ± SE | LightGBM − LR ± SE | Pair swaps |
     |---|---|---|---|---|---|---|---|
     | 3 x 9 months (shipped) | 67 (836) | 60% | 0.905 ± 0.203 | 0.22 | 0.472 ± 0.093 | 0.43 ± 0.19 | 5.8% |
     | 5, same exams | 67 (836) | 60% | 0.693 ± 0.151 | 0.22 | 0.410 ± 0.081 | 0.28 ± 0.15 | 6.1% |
     | 8, same exams | 67 (836) | 60% | 0.657 ± 0.144 | 0.22 | 0.396 ± 0.071 | 0.26 ± 0.14 | 5.4% |
     | 11, same exams | 67 (836) | 60% | 0.614 ± 0.135 | 0.22 | 0.408 ± 0.060 | 0.21 ± 0.11 | 5.3% |
     | 3, from 31 Aug 1996 | 84 (1,010) | 51% | 0.711 ± 0.171 | 0.24 | 0.411 ± 0.088 | 0.30 ± 0.15 | 6.0% |
     | 5, from 31 Aug 1996 | 84 (1,010) | 51% | 0.609 ± 0.134 | 0.22 | 0.360 ± 0.061 | 0.25 ± 0.12 | 5.1% |
     | 12, from 31 Aug 1996 | 84 (1,010) | 51% | 0.498 ± 0.097 | 0.19 | 0.293 ± 0.044 | 0.21 ± 0.09 | 6.4% |

     - Every scheme ranks the models the same way: extra trees, random forest, logistic regression, LightGBM. Only
       kNN and HistGB swap at the bottom.
     - The SE falls with more windows only because the score itself falls. Equal-weighted small windows dilute the
       two shifted windows (LightGBM 1.79 and 1.57). The ratio SE / score stays at 0.19 to 0.24, and LightGBM − LR
       stays at about two SEs (1.8 to 2.3).
     - With 8 or more windows, single exam dates become windows of 77 to 104 segments, most with no suspect segment.
       Each window then tests one day's exams, not a later period.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Three nine-month windows (implemented) | as now: 836 test segments of 67 exams | each window is a later period; the shift between 1996 and 1997 shows in its own windows | the score rests on 3 windows (relative SE 0.22) |
     | B | Five windows down to the 50% floor | 5 windows of about 200 segments over the exams from 31 August 1996 (84 exams), smallest train 51% | 17 more test exams | relative error and pair swaps unchanged (0.22, 5.1%); the oldest window trains on half the data; windows of uneven length |
     | C | 8 to 12 finer windows | windows of one or a few exam dates | many splits | no steadier: same exams, same ranking, same relative error; windows of single days |

   * **Recommendation:** A. More windows reuse the same test exams, so they give no better signal on this
     dataset[^3a]. B is the only option that adds test exams, and the gain does not show in the measurements.
     **Decision:** A, B or C?

   **Notes for the AI:** on B, the windows (newest first) are 10 May to 6 June 1998, 29 October 1997 to 8 April 1998,
   23 December 1996 to 25 October 1997, 6 October to 9 December 1996, and 31 August to 3 October 1996. Calendar windows
   of fixed length leave some windows empty or tiny, because the exams fall on 47 dates, so B needs the date ranges as
   explicit windows (`_make_splits`). Then rewrite `split` and `splits_comment`, recount the classes per window,
   recheck the accepted warnings and run `dataset check`. A and C: on A nothing changes; C is not drafted.

   [^3a]: **SPLIT-17** (Should): finer windows add no test rows, because the 50% floor fixes the test pool; they cut
     it into smaller, noisier pieces. **SPLIT-15** (Should): as many windows as an IID task would get folds, then
     check the windows are still meaningful. **SPLIT-14** (Must): at least 3 windows, none training on less than 50%.

   **Resolved (2026-11-11, Andrej):** A: the three nine-month windows by exam date stay as implemented; nothing
   changed in the definition.

## Reference

@misc{cardiotocography_193,
  author       = {Campos, D. and Bernardes, J.},
  title        = {{Cardiotocography}},
  year         = {2000},
  howpublished = {UCI Machine Learning Repository},
  note         = {{DOI}: https://doi.org/10.24432/C51S4N}
}
