---
unique_name: predict_students_dropout_and_academic_success
name: predict_students_dropout_and_academic_success
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
tags:
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Later'
original_source: UCI
year: '2021'
domain: education
required_split:
- Random (IID)
problem_type: Multiclass Classification
source_links:
- https://doi.org/10.24432/C5MC89
notebook_path: datasets/beyond_iid/old_iid/predict_students_dropout_and_academic_success/predict_students_dropout_and_academic_success.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/predict_students_dropout_and_academic_success/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Identify students at risk of failrue. As it is human data, ethical issues need to be considered. Need to look closer at features and how the task was conceptualized - i.e., which point in time the features represent. But apparently the features were collected after 2nd semestre - hence should be fine.

Potential issue: -

Lennart: No objection, ethical issues are likely minor if at all

Andrej: As the task is non-discriminative but supportive in nature, I see no issues in the use of demographic features

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — the UCI page and the data paper define no task metric; the case study compares classifiers on several scores (not verified in full text).

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): left unordered: `Previous_qualification` (a partial order); `Mothers_qualification` (a partial order); `Fathers_qualification` (a partial order); ordinal scales shipped as numbers, left as numbers for the curator's review: `Application_order`.

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 1 ordinal scales shipped as numbers are ordered categories (point 3).

CC (2026-11-01, Lennart): marks on the review board of PR #37: the three qualification columns stay unordered (ties and side branches), noted in the definition.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `upv_university_student_dropout` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 1 scores are numbers (Application_order).

CC (2026-11-11, Andrej): review marks. Issue 1 (the fee and debt status of unknown date) stays open for discussion, and issue 2 (the split by enrolment year) with it: the answer of 2026-11-11 to the gap question shows that the label is the status at the end of the course's normal length, so a gap is needed, and offers a per-degree gap with four windows (b2) beside the three windows of b. Nothing changed in the definition; the review moved from the folder's file into this record.

CC (2026-11-11, Andrej): the record's empty `problem_type` and `domain` filled from the definition (Multiclass Classification, education), as the review's record judgment asks; no value disagreed.

## Review

**Outcome:** added. UCI's "Predict Students' Dropout and Academic Success" (UCI 697, https://doi.org/10.24432/C5MC89;
Realinho et al., "Predicting Student Dropout and Academic Success", Data 2022;7(11):146,
https://doi.org/10.3390/data7110146): 4,424 students of 17 degrees at one Portuguese institution, their background at
enrolment, fee and debt status, three national economic figures and the units and grades of their first two semesters,
and whether at the end of the course's normal length they had graduated (50%), dropped out (32%) or were still enrolled
(18%); random splits, log loss (fallback). The AI recommends shipping it after two changes (issues 1 and 2). Reviewed on
2026-11-04 without a panel, from the gathered evidence (the record, model runs on the shipped data and on
TabArena v0.1's copy) and two checks. Validity: no feature is the outcome itself, but the fee and debt status have no
recording date and 87% of the students behind on fees dropped out (issue 1); the three economic figures identify the
enrolment year 2008-2017 exactly, so the cohorts the definition calls unknown are known and the random split mixes them
(issue 2); the label is read at the course's normal end, and the newest cohort shows no sign of being cut short
(checked). Value: on the shipped splits the 40 benchmark methods spread from log loss 0.505 (KUMO) over a median of
0.542
to 0.589 (default extra trees), logistic regression 0.558 to 0.567; methods separate. Quality: codes decoded, the
partial orders noted (Lennart, 2026-11-01). Weighed: a documented institutional dataset with a stated aim +, a real
three-way outcome and a spread +, a fee status of unknown date and a split that ignores a recoverable year -.

**Main points:** Drop the fee and debt status, whose recording date is unknown and which mark most dropouts (issue 1)?
Split by enrolment year, recovered from the economic figures, or keep the random split with no time-basis tag (issue 2; a
random split flatters log loss by 0.04 to 0.20 at equal training size, answer of 2026-11-06; three windows are the most
that keep half of the rows in training with b's gap; a gap per degree gives four, answer of 2026-11-11 to the gap
note)? Keep the scholarship
status, as undated as the fee status but possible at the prediction point, with a note (issue 3, new)?

**Record judgment:** valid. The record has no `problem_type` (Multiclass Classification) and no `domain` (education);
Claude fills them, as no value disagrees. The TabArena note "the features were collected after 2nd semestre" matches
the definition's prediction point, the end of the first year. The data scouting found `upv_university_student_dropout`;
it is screened in its own record and does not change this task's validity.

**Issues for Andrej:**

1. **Drop `Tuition_fees_up_to_date` and `Debtor`, whose recording date is not stated and which mark most dropouts?**

   * **Problem:**
     - The source says its features are "information known at the time of student enrollment" and the first two
       semesters' results, but fee arrears and debt cannot exist at enrolment, and no date for them is given.
     - The data come "from several disjoint databases", so the status may be the one read when the file was made,
       years after a student left; 87% of the students behind on fees dropped out.
     - A value read after the outcome whose late cells cannot be located goes when it may carry a gain[^1a]; drop
       both, or keep them?
   * **Experiments:** check of 2026-11-04 on the shipped data: 528 students are behind on fees, 86.6% of them dropouts
     (457, a third of all 1,421 dropouts), against 24.7% of the others; 503 are debtors, 62.0% dropouts against 28.3%.
   * **Effect on the task:** if the status was read after students left, a model learns "stopped paying, so dropped
     out", which an adviser at the end of the first year could not see.
   * **Unknown:** the date of the fee and debt status; the data paper's text would settle it (the MDPI page refused the
     AI's request).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | both columns; `fit_reason` names the unknown date | arrears at the end of year one would be a real early warning | a likely post-outcome status that marks a third of the dropouts |
     | B | Drop both | `Tuition_fees_up_to_date` and `Debtor` dropped | no feature that may be read after the outcome | loses a real warning sign if the status is from year one |
     | C | Keep with a note | as A, plus a `Potential leak, kept on purpose:` note with the numbers | documents the risk | the possible leak stays readable |

   * **Recommendation:** B: the status cannot be dated, a later pull is likely, and the gain is large. **Decision:**
     keep (A), drop (B) or keep with a note (C)?

   **Notes for the AI:** on B, drop both columns in `_clean` and from the decoding maps and `categorical`; a curation
   note with the numbers; `known` in the task summary loses "fee and debt status"; `fit_reason` loses the fee sentence;
   `dataset check`. If the paper dates the status at the end of the first year, close the issue as A with the quote.

   [^1a]: **LEAK-10** (Must): a feature holds only what existed at the prediction point; clause amended 2026-10-26
     (Lennart): a value read at a later pull goes where its late cells can be located; where they cannot be located row
     by row, the values go when they may carry a gain.

2. **Split by enrolment year, which the economic figures give exactly?**

   * **Problem:**
     - The definition says the file has no enrolment year, but unemployment, inflation and GDP take ten value triples,
       and each matches Portugal's annual figures of one year, 2008 to 2017, so every student's cohort is known.
     - An institution trains on earlier cohorts and scores the newest one, so the task is temporal by its use case, and
       a hidden year does not make it random[^2a].
     - Keep the random split, or test on the newest cohorts with only cohorts whose outcome is known by then in training?
   * **Background:** the triples are, for example, unemployment 7.6% with inflation 2.6% and GDP growth 0.32% (2008),
     16.2%, 0.3% and -0.92% (2013), 8.9%, 1.4% and 3.51% (2017), Portugal's published rates for those years. The label
     is read at the end of the course's normal length, so a model refit at the end of a cohort's first year knows only
     the outcomes of cohorts whose normal length has ended[^2b].
   * **Experiments:** check of 2026-11-04 on the shipped data: cohorts of 362 (2013) to 571 (2008) students; dropout
     24.0% to 38.4% and still enrolled 12.7% to 20.9% by cohort, with the newest cohort (2017) at 27.7% and 20.9%, so it
     is not cut short. Model runs found the study plans changing between cohorts (for example Nursing students
     passing 7 of 8 units: 89% graduates in the years whose plan had one unit not passable in the semester), which a
     random split lets models learn from classmates of the same cohort.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random (implemented) | 3 x 3 random folds over all cohorts | as the source's 80/20 split | rewards learning each cohort's quirks from its own students; ignores a known year |
     | B | Three cohort windows | an `enrolment_year` from the triple (split metadata, not a feature); test 2015, 2016, 2017, each trained on cohorts at least three years older (55% to 72% of the rows) | tests on a new cohort, as an institution would; the gap keeps outcomes not yet known out of training | fewer test rows (368 to 445 per window); the year map rests on published national figures |
     | C | Random, tagged forced | as A, with `ForcedIIDFromTemporal` and a note | flags the gap | the year is known, so the force is not needed |

   * **Recommendation:** B: the year is recovered exactly and every window meets the split rules. **Decision:** random
     (A), cohort windows (B) or random tagged (C)?

   **Notes for the AI:** on B, map `Unemployment_rate` to the year (7.6: 2008, 9.4: 2009, 10.8: 2010, 12.7: 2011, 15.5:
   2012, 16.2: 2013, 13.9: 2014, 12.4: 2015, 11.1: 2016, 8.9: 2017; assert all rows map and that inflation and GDP agree)
   into a time column used only by the splits; three one-year windows 2015-2017, each trained on cohorts up to three
   years older (a gap of two cohorts, enough for courses of up to four years); the macro triple stays a feature;
   `fit_reason` loses "no enrolment year"; cite INE/Pordata for the series; `dataset check`.

   [^2a]: **SPLIT-7** (Must): a missing or hidden timestamp does not make a task IID. **SPLIT-14** (Must): a temporal
     task has at least 3 windows, and no window's train side holds less than 50% of the data.
   [^2b]: **SPLIT-10** (Should): when a label is known only some time after its row, train on the rows whose outcome is
     known by the window's start, with a gap of about the label's delay.

   **Answer (AI, 2026-11-06):** Split by cohort, or keep the random split with no time-basis tag, now that its cost is
   measured?

   * **Problem:**
     - The outcome mix moves between cohorts, the economic triple gives every student's enrolment year exactly, and
       the institution predicts for the next cohort, so the enrolment year is information for the split, and the
       measured cost below shows no stationary relation[^2c].
     - C's forced tag no longer fits: it stands for a release with no usable time or too few periods, and with the year
       known and three valid windows a random split is no longer forced, only a split with no time-basis tag (A).
     - The cost is large: trained on the cohorts whose outcomes are known, the models' log loss on a new cohort is 0.04
       to 0.20 higher than when trained on as many students drawn from all cohorts.
   * **Experiments:** the 4,424 shipped students and 36 features, untuned LightGBM and logistic regression (one-hot
     categories), log loss (Slurm job 1365899):
     - Shipped random split (3 x 3): LightGBM 0.595 (0.571 to 0.615), logistic regression 0.568 (0.535 to 0.585).
     - B's windows, each trained on cohorts at least three years older: LightGBM 0.846 (2017, the newest), 0.814
       (2016) and 0.704 (2015); logistic regression 0.753, 0.715 and 0.568.
     - Same test students and same training size (each window's students in 3 folds, 3 seeds; older cohorts only
       against students drawn from all other cohorts): LightGBM +0.196, +0.136 and +0.114 (2017, 2016, 2015; higher on
       26 of 27 folds), logistic regression +0.155, +0.099 and +0.041 (26 of 27).
     - Without the gap (trained on every older cohort, also those whose outcome is not known when the window's cohort
       is scored): LightGBM 0.649, 0.751 and 0.630, +0.039, +0.119 and +0.060 at equal size; most of the 2017 cost
       comes from leaving out the two newest cohorts, as the gap must[^2b].
     - Outcome by cohort: dropout 30.3% to 38.4% in 2008-2014 and 24.0% to 28.3% in the test cohorts 2015-2017, still
       enrolled 12.7% to 20.9%; a random split trains on the test cohorts' own level.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Random split, no time-basis tag (A) | as now; no use-case prototype named (`StationaryRelation` is not shown: the dropout share falls from 30-38% to 24-28% and B's windows cost +0.11 to +0.20 log loss (LightGBM) at equal training size; three valid windows, so no forced tag) | the source's random 80/20 split; more test rows | flatters log loss by 0.04 to 0.20 at equal training size; test students share their cohort's level and study plans with training students |
     | b | Three cohort windows (B) | test 2015, 2016 and 2017, each trained on cohorts at least three years older (55% to 72% of the rows) | tests a new cohort, as the institution meets it, with only known outcomes in training | 368 to 445 test students per window; scores far below the random split's |

   * **Recommendation:** b: the year is exact, the windows meet the split rules, and the measured cost shows that the
     random split hides a real change between cohorts (the dropout share falls from 30-38% to 24-28% in the test
     cohorts) that an institution scoring its next cohort meets. **Decision:** a or b?

   **Notes for the AI:** on b, B's notes above, as `Temporal(on="enrolment_year", splits=TemporalSplits(window=1,
   unit="years", cutoffs=(2015, 2016, 2017), gap=2))` with `enrolment_year` a date (1 January of the year): the gap
   of two years trains the 2015 window on cohorts up to 2012; `splits_comment` states the gap and why (the outcome is
   read at the end of the course's normal length, three to four years); record tag `Non-IID (Temporal)`. On a, no
   time-basis tag in the definition; a curation bullet `- Time order: the enrolment year 2008-2017 is known exactly from the national unemployment, inflation and GDP figures; not split by
   cohort, because <the curator's reason>; three cohort windows (2015-2017, each trained on cohorts at least three
   years older) cost +0.11 to +0.20 log loss at equal training size (untuned LightGBM 0.846 against 0.650 on 2017;
   logistic regression +0.04 to +0.15).` The frame has no date column on a, so no warning to accept. Under either
   option the record gets the tags `Samples: Over Time` and `Time: Dated`. Results: Slurm job 1365899.

   [^2c]: **SPLIT-32** (Should): how the data was collected is information for the split; the record's collection
     facts and, where one fits, the definition's use-case prototype with its `Time basis:` line.

   **Andrej (2026-11-11, discuss):** How many cohort windows can we use at max while still having at least 50% of the
   data in each train split? If its more than three, add it as an option.

   **Answer (AI, 2026-11-11):** three, with the gap of two cohorts that option b needs; so no new option.

   | Test cohort | Test students | Train: cohorts up to | Train students (share of 4,424) | Gap 0 train share |
   |---|---|---|---|---|
   | 2017 | 368 | 2014 | 3,197 (72%) | 92% |
   | 2016 | 414 | 2013 | 2,807 (63%) | 82% |
   | 2015 | 445 | 2012 | 2,445 (55%) | 72% |
   | 2014 | 390 | 2011 | 2,048 (46%) | 63% |
   | 2013 | 362 | 2010 | 1,629 (37%) | 55% |
   | 2012 | 397 | 2009 | 1,104 (25%) | 46% |

   * With the gap of two cohorts, the 2014 window trains on 46%, so 2015-2017 is the maximum.
   * A gap of one cohort gives four windows (2014 trains on 55%), but Nursing, the largest degree (766 students, 17%),
     runs four years, so its outcomes would not be known when the window's cohort is scored[^2b].
   * Without a gap there would be five windows (2013-2017), but each would train on the two to three cohorts whose
     outcomes are not yet known; the 2026-11-06 answer measured that variant (LightGBM 0.649 against 0.846 on 2017).
   * Cohort sizes and the year map from the unemployment rate as in issue 2's notes (all 4,424 rows map; inflation
     and GDP agree within each year). Script `~/claude_jobs/marks_1111/predict_students_dropout_and_academic_success/windows.py`.
   * **Recommendation:** b as drafted (three windows, gap of two cohorts). **Decision:** a or b?

   **Andrej (2026-11-11, discuss):** Wait, why is there a gap for this task, I think there shouldn't be one since at
   the end of one school year the data is there to predict the next?

   **Answer (AI, 2026-11-11):** The features are there, the labels are not: the label is the status at the end of the
   course's normal length, not after the next year, so a gap is needed, but a smaller one than b's for most degrees.

   * Each student's label (graduate, dropout, still enrolled) is read when the course's normal length ends: three
     years, four for Nursing (17% of the students).
   * When cohort 2017 finishes its first year (summer 2018), cohort 2016 has its first-year data but is only in year
     two: a student still enrolled may yet drop out or graduate. Training on it uses outcomes not known yet[^2b].
   * Your reading would hold for a target "status after the next year"; the file does not record that.
   * b's gap of two cohorts is set by Nursing. An exact gap per degree (one cohort for three-year degrees, two for
     Nursing) gives four windows instead of three.
   * Measured (untuned LightGBM and logistic regression, log loss, same features; Slurm job 1378300):

     | Split | Windows | Train share | LightGBM per window (2017 ... oldest) | Cost vs random, equal size (LightGBM) |
     |---|---|---|---|---|
     | b: gap of two cohorts | 3 (2015-2017) | 55% to 72% | 0.846, 0.814, 0.704 | +0.11 to +0.20 |
     | per-degree gap | 4 (2014-2017) | 54% to 81% | 0.740, 0.791, 0.694, 0.706 | +0.02 to +0.14 |
     | no gap | 5 (2013-2017) | 55% to 92% | 0.649, 0.751, 0.630, 0.674, 0.617 | +0.04 to +0.12 |

   * Logistic regression, per-degree gap: 0.704, 0.697, 0.566, 0.664. The degree lengths are an assumption (Portuguese
     licenciaturas: 180 ECTS, three years; Nursing 240 ECTS); counting Oral Hygiene (86 students) as four years too
     moves the shares by under 0.3 points. Script `~/claude_jobs/marks_1111/predict_students_dropout_and_academic_success/mkbundle.py`.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Random split | as now | more test rows | flatters log loss by 0.04 to 0.20 |
     | b | Three cohort windows, gap of two cohorts | as drafted | one `TemporalSplits` line | one window fewer than needed for three-year degrees |
     | b2 | Four cohort windows, gap per degree | test 2014-2017; train on students whose course's normal end is before the test cohort's first year ends | trains on every known outcome; four windows | a custom `_make_splits`; degree lengths from the ECTS of the degrees |
     | d | Five cohort windows, no gap | test 2013-2017, train on all earlier cohorts | most windows and history | trains on outcomes not known at the prediction point |

   * **Recommendation:** b2: it uses exactly the outcomes known at the prediction point and gains a window.
     **Decision:** a, b, b2 or d?

3. **`Scholarship_holder` is as undated as the fee status of issue 1: keep it with a note, or drop it too?**

   * **Problem:**
     - `Scholarship_holder` is a yearly financial status like the fee and debt status of issue 1, and the source gives it no date either, so it may be the status of a later year, which a grant's renewal ties to passing the first[^3a].
     - Unlike fee arrears, a scholarship can exist at the prediction point, and nothing in the data shows it was read after the outcome; it adds little: log loss 0.591 without it against 0.587 with it (LightGBM; fee and debt status 0.633 without them).
     - Keep it with a note naming the unknown date, drop it with the fee status, or keep it as it is?
   * **Background:**
     - Holders drop out at 12.2% against 38.7% of the others and graduate at 76.0% against 41.3%.
     - Among students who passed no unit in the first semester, 10.3% hold a scholarship against 27.7% of the others; a grant given at enrolment does not know who will fail, so this fits a later year's status, but it fits a grant that helps a student pass as well.
     - The holders' share is 11.2% of the 2008 cohort and 21% to 31% of each later one, a change of policy or of when the status was read; the source does not say.
   * **Experiments:** the shipped frame (4,424 students, 36 features), untuned LightGBM and logistic regression (LR), log loss, the shipped random 3 x 3 folds with and without the columns (Slurm job 1366162): all columns LightGBM 0.587, LR 0.567; without `Scholarship_holder` 0.591 and 0.569; without the fee and debt status 0.633 and 0.599; without all three 0.634 and 0.602.
   * **Effect on the task:** if the flag is a later year's status, a model reads a little of the outcome from it (0.004 log loss); if it is the status at enrolment or in the first year, it is a real early-warning input.
   * **Unknown:** the date of the status; the data paper (Realinho et al. 2022) or the institution could say, as for issue 1.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as it is (implemented) | the column stays; no note | a status that can exist at the prediction point | its date is as unknown as the fee status, and the notes do not say so |
     | B | Drop it with the fee status | `Scholarship_holder` leaves with `Tuition_fees_up_to_date` and `Debtor` | no financial status of unknown date left | drops a likely valid input for a 0.004 gain whose source is unknown |
     | C | Keep with a note | the column stays; a curation bullet names the unknown date, the numbers above and why it stays while the fee status goes (if issue 1 drops it) | the sibling of issue 1 decided in the open; keeps a plausible early-warning input | a later status, if it is one, stays |

   * **Recommendation:** C: a scholarship, unlike arrears, can exist at the prediction point, the data shows no sign that it was read after the outcome, and its gain is small; if the paper dates the financial statuses to the extract, B[^3b]. **Decision:** A, B or C?

   **Notes for the AI:** on C, a curation bullet "- `Scholarship_holder`: no recording date, like the fee and debt status; kept, as a scholarship can exist by the end of the first year and the data shows no sign of a later read (holders drop out at 12% against 39%; without it log loss rises by 0.004, untuned LightGBM)"; `fit_reason` names the unknown date with the fee status. On B, drop it in `_clean` with the issue-1 columns and from the decoding maps and `categorical`; `known` loses "scholarship"; `dataset check`. A `CC` line in the record either way.

   [^3a]: **LEAK-2** (Must): a flagged column is rarely alone; sweep the codebook and the use case for its siblings.
   [^3b]: **LEAK-10** (Must): a feature holds only what existed at the prediction point; a value read at a later pull goes when it may carry a gain and its late cells cannot be located (clause amended 2026-10-26, Lennart), which needs the later read shown first. **LEAK-6** (Must): measure before acting.

## Reference

Early prediction of student's performance in higher education: a case study
 By Mónica V. Martins, Daniel Tolledo, Jorge Machado, Luís M. T. Baptista, and Valentim Realinho. 2021
 
 Published in Trends and Applications in Information Systems and Technologies
