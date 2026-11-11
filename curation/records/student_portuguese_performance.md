---
unique_name: student_portuguese_performance
name: archive_r56_Portuguese
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Tiny Data
- 'Samples: One Moment'
- 'Target: Later'
collections:
- TabArena Reject
- TabSTAR
original_source: UCI
year: '2014'
domain: education
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/whenamancodes/student-performance/data
- https://doi.org/10.24432/C5TG7T
- https://www.openml.org/d/44967
notebook_path: datasets/beyond_iid/new_iid/student_portuguese_performance/student_portuguese_performance.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/student_portuguese_performance/dataset.py
source_row: 763
type_adapter_id: curation-record-v1
---

## Comments

CC: "Cortez and Silva, 2008. Students from two schools - predict student performance. Would require temporal split or time-invariant features. The latter can be assumed to be true. If the features would have been created at a similar time as the target this would be a scientific discovery task more than a predictive performance task. But most features seem time-invariant. need to select a target as there are multiple possible, also might need to exclude some features as intermediate grades or non-time-invariant features. No objection if G features/targets are handled"

We can treat the g3 as the prediction target and use g1 and g2 or drop it and just aim for predicting this for the next year for these students. might have some problem as features talk about the entire time or past behavior for the newest grade

We use the port data and ignore the math data, as it is more or less a different version/target (382 students overlap) and the port data is larger. We only predict G3

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source rmse — RMSE of G3 in regression setup C of Cortez & Silva 2008.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): ordinal scales shipped as numbers, left as numbers for the curator's review: `Medu`, `Fedu`, `traveltime`, `studytime`, `failures`, `famrel`, `freetime`, `goout`, `Dalc`, `Walc`, `health`.

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 11 ordinal scales shipped as numbers are ordered categories (point 3).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `hsls09_secondary_student_achievement` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 9 coded columns carry their words; 6 scores are numbers (famrel, freetime, goout, Dalc, Walc, health).

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): counts with a cut end are numbers: failures.

CC (2026-11-01, Lennart): counts with a cut end stay ordered categories of the source's levels, the cut end a level of its own (CLEAN-14): the lossless form, chosen from the context rather than by model runs; the same day's numbers with censoring flags are reverted.

CC (2026-11-06, Andrej): time basis `DelayedTarget` accepted on the BeyondArena v0.2 review page (issue 3, B, through the cross-dataset item on `DelayedTarget` issues of one-moment releases): one cohort of the 2005-2006 school year, the target the final grade at the year's end. The random split is IID here, as every row shares the moment and the outcome window, so no test row is later than a training row. The `Time basis:` line is in the definition's notes; the tag enters `data_tags` once PR #50 is in the working copy.

CC (2026-11-09, Andrej): `absences` is dropped (review page issue 4, C): the school report's count is 0 for every student without a final grade. The 15 final grades of 0 stay, with a note (issue 2, A).

CC (2026-11-11, Andrej): `No Good Target / Scientific Discovery` removed (BeyondArena v0.2 review page, issue 1, A): a school's early support decision fits the final grade, the period grades and `absences` are dropped, and the timing doubt of the questionnaire is in the approximate fit.

CC (2026-11-11, Andrej): split checked, random kept with a note (issue 5, A): no class, teacher or year is recorded, so classmates sit on both sides; the use case is a school supporting its own students, and two schools are too few groups.

## Review

**Outcome:** added. Reviewed without a review panel, from the evidence already gathered: the record, the earlier
experiments on the shipped splits and a model run on the shipped data. The source is UCI 320 (Cortez and
Silva 2008): 649 students of the Portuguese-language course at two Portuguese secondary schools, with background,
family and habit answers from school reports and a questionnaire; the target is the final grade from 0 to 20, scored
by the paper's RMSE. The first- and second-period grades are dropped, so the final grade is predicted from background
and habits alone. The AI recommends shipping after two small changes, both open since 2026-10-27. Validity: a real
decision stands behind it (a school offers extra support early to students likely to fail), and the dropped period
grades keep it a prediction rather than a look back; the absences and the habit answers cover the same school year as
the grade and their timing is not stated, so the fit is approximate, which is written into the definition. The marker
`No Good Target / Scientific Discovery`, which contradicted its `Yes`, is removed (issue 1, 2026-11-11). Value: the
methods separate on the shipped splits. Over the benchmark methods the RMSE runs from 2.63 to 2.76
(TabPFN-3.5 2.66, tuned logistic-style linear regression 2.72, median 2.68) against 3.23 for predicting the mean;
an earlier check put TabPFN at R² 0.32 and ahead of ridge on 58 of 60 splits. A hand-written two-part model (a
drop-out part for the zero grades, a ridge for the rest) ranks first of the 41 methods at 2.60, so much of the task is
a few background rules plus the zero process: a note on how much a benchmark learns here, not a reason to retire.
Quality: 15 final grades of 0 look like students who never sat the final assessment and carry a quarter to a third of
the squared error (issue 2); the ordinal scales and codes were settled by Lennart on 2026-10-31 and 2026-11-01.
Weighed: a documented source and paper +, a real support decision +, a small and dated table of two schools -,
questionnaire timing unstated -, methods close together but ordered -. Left for Andrej: issues 1 and 2.

**Main points:** all issues resolved: `absences` dropped (issue 4) and the 15 zero grades kept with a note (issue 2)
on 2026-11-09; the `No Good Target` marker removed (issue 1) and the random split kept with a note on the unrecorded
classes (issue 5) on 2026-11-11. Needs a rebuild.

**Record judgment:** a real, non-trivial prediction from background data; the timing of a few questionnaire answers is
unstated but carries almost none of the score. Two corrections need no decision: the definition's BibTeX names only
"Silva, Alice" with no venue, where the paper is Cortez, P. and Silva, A. M. G. (2008), "Using data mining to predict
secondary school student performance", in Brito, A. and Teixeira, J. (eds.), *Proceedings of 5th FUture BUsiness
TEChnology Conference (FUBUTEC 2008)*, pp. 5-12, EUROSIS, ISBN 978-9077381-39-7; and the built container is stale
against the current definition, so the dataset needs a rebuild. A data-scouting run found a larger, newer dataset for
the same task on 2026-10-31 (the US HSLS:09 cohort, 23,000 ninth-graders of 944 schools, with the achievement measured
in a later wave); it is screened as its own record and does not by itself reject this one, which keeps the verdict its
own data earns.

**Issues for Andrej:**

1. **Remove the `No Good Target / Scientific Discovery` marker?**

   * **Problem:**
     - The record carries a marker that says the dataset has no genuine predictive target, which would mean `No`,
       while the record's verdict is `Yes`.
     - The marker most likely records the screening concern that the features and the grade come from the same
       school year, which would make the task a look back rather than a prediction.
     - Remove the marker, or keep it and decide what the record's verdict should be?
   * **Background:** the marker is the one for a table built for a study looking back, a survey or a label no decision
     fits[^1a]. Here a decision does fit: a school predicts the final Portuguese grade early in the year to offer
     extra support to the students likely to fail, and the definition drops the first- and second-period grades so
     that the prediction uses background and habits only[^1b].
   * **Effect on the task:** none on the data; on the record the marker reads as a reason not to ship.
   * **Experiments:** over 60 splits (20 repeats of 3 folds), TabPFN reaches R² 0.32 against about 0 for the training
     mean; dropping `absences`, the answer whose timing is least certain, costs 0.004 R²; on the three strongest
     features alone TabPFN falls to R² 0.25, so the signal is spread over the background columns rather than carried
     by one same-time answer. The remaining timing doubt is written into the definition as an approximate fit.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Remove the marker | the record keeps `Yes` with no marker; nothing changes in the data | the record then says what the review found; a support decision fits the label | the screening concern is no longer visible on the record |
     | B | Keep the marker (implemented) | the record stays as it is | the timing doubt stays visible | a marker that means "no predictive target" sits on a `Yes`; it reads as a reason not to ship |
     | C | Keep it and set the record to `No` | the dataset leaves the benchmark | consistent with what the marker means | the timing doubt costs 0.004 R², so the look-back reading is not supported |

   * **Recommendation:** A, remove it: the fit text already carries the timing doubt, and the measurements show the
     same-time answers carry almost none of the signal. **Decision:** A, B or C?

   **Notes for the AI:** on A, remove `No Good Target / Scientific Discovery` from the record's `decision_markers` and
   add `Andrej` to `checked_by`; the definition is unchanged. On C, set `suggestion` to `No (Retired)` and follow the
   retirement steps for the folder.

   [^1a]: **SEL-3** (Must): the dataset is published for a predictive task, simulating a decision someone makes with
     the prediction; the marker `No Good Target / Scientific Discovery` is for a label no decision fits.
   [^1b]: **USE-3** (Must): name the prediction point, when the model is used and what is known then; a value that
     did not exist at that point is a leak.

   **Andrej (2026-11-11, change):** Option A: Remove the marker.

   **Resolved (2026-11-11, Andrej):** A: `No Good Target / Scientific Discovery` removed from the record's
   `decision_markers`, with a CC line; the definition is unchanged.

2. **Document the 15 final grades of 0, or drop the rows?**

   * **Problem:**
     - 15 of the 649 students have a final grade of 0, and all 15 have zero recorded absences, 14 of them at one of
       the two schools, while every one of them has a first-period grade above 0.
     - This looks like students who never sat the final assessment rather than students who scored 0, but the
       source's attribute file says only "from 0 to 20".
     - Keep the rows with a note, or drop them as students without a final grade?
   * **Effect on the task:** under the squared-error metric these 2.3% of rows carry 25 to 32% of the squared error,
     depending on the model, so a score depends much on whether a model predicts a 0 for a student who may have left
     the course.
   * **Experiments:** a model run on the shipped data arrived at the same reading from the data alone and
     built it into its best model: a two-part model whose first part predicts "left the course" from drop-out risk
     factors (school, a repeated year, plans for higher education, age, sex, study time) and whose second part is a
     ridge on the students who sat the exam reaches RMSE 2.60, ahead of all 41 benchmark methods, the best of which
     scores 2.63. A variant whose drop-out part uses only risk factors fixed before the zero rows were looked at
     still reaches 2.64. So the zeros are a second process the metric rewards modelling, whichever option is taken.
   * **Unknown:** whether a 0 means "did not sit the assessment" is not stated anywhere in the source we could read
     (the attribute file and the data page); only the pattern above supports it. The authors could be asked.
   * **Consistency:** a proxy code becomes missing only when the description and the context show the encoding, and
     the description does not show it here[^2a]; a row whose target is missing leaves[^2b], which is what option B
     would make of these rows.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the rows, add the note | the data is unchanged; the curation notes and the summary say a 0 likely marks a student without a final grade | keeps the data as published; a reader is warned; the benchmark keeps 649 rows | a quarter to a third of the squared error rests on rows that may not be grades |
     | B | Drop the 15 rows | 634 rows; the zero process leaves the task | the target is then a grade a student actually earned | rests on an inference the source does not state; a school's support decision covers students who drop out too |
     | C | Keep the rows with no note (implemented) | nothing changes | nothing to decide | a reader cannot see what the zeros are |

   * **Recommendation:** A, keep the rows and write what the zeros look like: dropping them rests on an inference the
     source does not state, and the students who leave are part of the support decision. **Decision:** A, B or C?

   **Notes for the AI:** on A, add a `curation_comments` bullet with the pattern (15 zeros, all with zero recorded
   absences, 14 at Mousinho da Silveira, every one with a first-period grade above 0) and extend
   `task_summary.predicted` by one clause; re-run the dataset check so the README follows. On B, drop the rows in
   `_clean` with the same bullet as the reason, and re-check the split sizes.

   [^2a]: **CLEAN-10** (Should): convert proxy missing values to real missing values when the encoding can be
     inferred from the description and the context.
   [^2b]: **CLEAN-15** (Must): drop rows with a missing target.

   **Andrej (2026-11-11, change):** Option A: Keep the rows, add the note.

   **Resolved (2026-11-09, Andrej):** A: the rows stay, with a curation note on the 15 zeros and a clause in
   `predicted`.

3. **Time basis: name the random split a `DelayedTarget`, one school year predicted at its start?**

   * **Problem:**
     - All 649 students are one cohort, the 2005-2006 school year at two schools, the use case predicts early in that year from background and habits, and the final grade arrives at the year's end, the same date for every student.
     - The record's collection facts fit (`Samples: One Moment`, `Target: Later`), and the random split carries no time basis.
     - Name it a `DelayedTarget`, with the line below?
   * **Background:** a delayed target needs its window closed for every row and every feature in existence at the
     moment[^3t1]. The window closed: every student has a final grade (15 of them 0, issue 2). The features: the
     background (parents' schooling and jobs, past failures, family) predates the year; the questionnaire was answered
     in class on a date the paper does not give; the absences come from the school report with the three period
     grades (issue 4). What the split cannot test: the next school year.
   * **Effect on the task:** none on rows, splits or scores.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random, no time basis (implemented) | as now | none found | the score's time meaning is not stated; `dataset check` notes the missing basis |
     | B | Random, named `DelayedTarget` | `data_tags` gain `DelayedTarget`; a `Time basis:` line names the year, the prediction point and the grade | states one cohort and one outcome date | the questionnaire's date stays unknown |
     | C | Random, forced from temporal | `data_tags` gain `ForcedIIDFromTemporal` | marks the stand-in for the next year | the amended rule gives one exam round a prototype, not the forced tag[^3t2] |

   * **Recommendation:** B. **Decision:** A, B or C?

   **Notes for the AI:** once PR #50 is in, on B: `data_tags = ("DelayedTarget",)` (no tag is listed now) and the
   curation bullet "- Time basis: DelayedTarget: one cohort, the 2005-2006 school year at two public schools of the
   Alentejo; the use case predicts early in the year from background and habits, and the target is the final grade
   at the year's end, one date closed for every student. The questionnaire's date in the year is not stated. Not
   tested: the next school year."; `dataset check`. The record's facts stay.

   [^3t1]: **SPLIT-32** (Should): a definition can name the use-case prototype it follows, with a `Time basis:` line
     stating the fact. A `DelayedTarget` has one prediction moment for all rows and the target after it; its line
     names the moment and the window, the window has closed for every row, and every feature existed at the moment.
     **LEAK-10** (Must): a feature holds only what existed at the prediction point.
   [^3t2]: **SPLIT-8** (Must; reworded 2026-11-05): a release that is one moment (one extract, one stock month, one
     exam round) is not forced; SPLIT-32 gives it `Snapshot` or `DelayedTarget`.

   **Resolved (2026-11-06, Andrej):** B, accepted through the cross-dataset item "Accept the `DelayedTarget` issues of
   one-moment releases with one mark?" The `Time basis: DelayedTarget:` bullet is in `curation_comments`; it says why
   the random split is IID here (every row shares the moment and the outcome window, so no test row is later than a
   training row) and ends with what the split cannot test (the next school year). The split and `data_tags` are
   unchanged; the tag `DelayedTarget` enters `data_tags` once PR #50 is in the working copy.

4. **Drop `absences`, the school report's count that is 0 for every student without a final grade?**

   * **Problem:**
     - All 15 students with a final grade of 0 have zero recorded absences, and none of the 405 students with any recorded absence has a final grade of 0, so a zero count partly records the outcome.
     - The count comes from the school report together with the three period grades, most likely the year's total, after the early-year prediction point.
     - Drop the column, or keep it with a note?
   * **Background:** the paper names two sources, school reports "including few attributes (i.e. the three period
     grades and number of school absences)" and a questionnaire answered in class (Cortez and Silva 2008). A value
     from the window that ends at the outcome, or a value that is missing because of the outcome, is out of the
     features unless the data shows it does not move with the outcome[^4t1]. The count also carries ordinary signal:
     among students with a final grade above 0 it correlates with the final grade at -0.20 and with the first-period
     grade at -0.18.
   * **Experiments:** on the UCI file (`student-por.csv`, 649 students): 244 have zero absences, 15 of them (6.1%)
     with a final grade of 0, 14 of these at Mousinho da Silveira (14 of its 98 students with zero absences), against
     0 of the 405 with any absence. An earlier check: dropping `absences` costs 0.004 R² (TabPFN, 60 splits).
   * **Effect on the task:** a model learns that only a zero count allows the zero grade, which a school does not
     know early in the year; if issue 2 drops the 15 rows, this part goes and the timing part stays.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | as now | the source's column | a year-end count whose zero records the outcome |
     | B | Keep, with a note | a curation note with the counts above; `fit_reason` names it | the reader sees it | the model still reads the outcome from the zero |
     | C | Drop `absences` | the column goes; `known` loses "school absences" | every feature then predates the outcome; costs 0.004 R² | loses the ordinary part of the signal |

   * **Recommendation:** C: the count is from after the prediction point and its zero records the outcome, for a cost
     of 0.004 R². **Decision:** A, B or C?

   **Notes for the AI:** on C, drop `absences` in `_clean` with a comment, remove "school absences" from
   `task_summary.known`, add a curation note with the counts above, `dataset check`, a CHANGELOG entry and a `CC`
   line in the record. On B, the curation note only. Data: `~/claude_jobs/spp_review/student-por.csv` (UCI 320).

   [^4t1]: **LEAK-10** (Must): a feature holds only what existed at the prediction point; out are a feature computed
     from the window that defines the target, unless the data shows the window's values do not move with the outcome
     given what is known at the prediction point, and missingness that encodes the outcome. **LEAK-7** (Should): the
     smallest fix that keeps a valid signal beats dropping the column; here no smaller fix separates the zero.

   **Andrej (2026-11-11, change):** Option C: Drop absences.

   **Resolved (2026-11-09, Andrej):** C: `_clean` drops `absences`; a curation note gives the counts, and `known` and
   `fit_reason` lose the absences.

5. **Split: random students, although classes and teachers are not recorded?**

   * **Problem:**
     - Andrej (2026-11-09): "How many school classes and years are in the data? A random split for this seems wrong
       since it doesn't take into account dynamics of same teacher and possible group dynamics."
     - The release records no class, teacher or year: 649 students of two schools (Gabriel Pereira 423, Mousinho da
       Silveira 226), from one school year (2005-2006, Cortez and Silva 2008).
     - So classmates sit on both sides of a random split, and a teacher's grading can reach a test student through
       classmates in training. How much cannot be measured: there is no class id.
     - The only recorded group is the school: two groups, with different grades (mean final grade 12.6 against 10.7).
   * **Options:**

   | | Option | What it does | Pro | Con |
   |---|---|---|---|---|
   | A | Random, with a note (implemented) | a curation note names the unrecorded classes and teachers | a school flagging its own students has their classmates in its data | class effects stay unmeasured |
   | B | By school | train on one school, test on the other (2 folds) | no shared teacher across the split | two groups only; tests a new school, which the use case does not ask |
   | C | Retire | no unit to group and one year | avoids an unmeasured class effect | loses a task whose use case is real |

   * **Recommendation:** A: the use case is a school supporting its own students, whose classmates it knows; classes
     cannot be rebuilt, and two schools are too few groups. **Decision:** A, B or C?

   **Notes for the AI:** on A, a curation bullet: no class, teacher or year recorded; one school year, two schools;
   classmates sit on both sides of the split. On B, `Grouping(on="school")` with two folds and the floor checked.

   **Resolved (2026-11-11, Andrej):** A (`ok`): random split kept; a curation bullet says no class, teacher or year is
   recorded (one school year, two schools: 423 and 226 students), so classmates sit on both sides of the split, and
   why it stays random. A CC line in the record. Text only, data unchanged.

## Reference

Cortez, P., & Silva, A. M. G. (2008). Using data mining to predict secondary school student performance.
