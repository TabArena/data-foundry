---
unique_name: college_scorecard
name: College scorecard
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
decision_markers:
- Selection Bias
tags:
- Non-IID (Temporal)
- '?'
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Fixed Delay'
- 'Entities: Recur'
- Panel Data
collections:
- TableShift
- TabSTAR
original_source: GOV Website
collection_period: 2001-2018
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://www.openml.org/d/46674
- https://collegescorecard.ed.gov/
- https://tableshift.org/datasets.html#college-scorecard
v2_path: datasets/_dev/tabarena-v0pt2/college_scorecard/dataset.py
source_row: 704
type_adapter_id: curation-record-v1
---

## Comments

Need to figure out real task/target. Binarized version of regression by TableShift.

Data looks good, but the group split is synthetically created and not part of the real task. Real task is just temporal and we have (de facto) data from each institution at time point T. Need to take some more time to look at the data but from the description it sounds taken out of context for the sake of the benchmark (which is fine in general, but not for us where we want to have real tasks!).

**Assessment (AI, 2026-10-07):** OpenML 46674 should not be the source. TableShift's `(C150_4 > 0.5).astype(int)` turns a missing rate into class 0, so roughly 90,000 of its 108,794 negatives have no completion rate, and its features come from the year the rate is reported, six years after the cohort entered. The v2 definition uses the Department of Education's June 2026 files: one row per four-year institution and entering cohort (fall 2001-2018), features from the entry-year file (with the institution's latest published completion and retention rates), target C150_4 from the file six years later, temporal split with a five-cohort label gap. Untuned LightGBM R² 0.80-0.81; the carried-forward rate 0.73-0.76. `colleges` (OpenML 42727) is a one-year Scorecard snapshot with target `percent_pell_grant`.

CC (2026-10-19, Lennart): ship. The Department of Education's files, not OpenML 46674; one row per four-year institution and entering cohort, target C150_4 six files later (regression), the institution's published completion and retention rates as features, cohorts of 30 or more, temporal by cohort with a five-year label gap; SAT math and average converted to the old scale from 2017 on, the reading percentiles left out.

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: MAIN, DISTANCEONLY.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — The Scorecard release defines no prediction task; TableShift binarizes the rate at 0.5 and scores accuracy, a different target from ours.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels): 3 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `PREDDEG`, `HIGHDEG`, `ADMCON7` (the README lists their levels); their codes that mean unknown (don't know, refused, not asked) are missing in `PREDDEG`, `ADMCON7` (CLEAN-10).

CC (2026-11-11, Lennart): accepted `splits_feature_missing_in_test` with a note naming the columns (cross-dataset item "Accept splits_feature_missing_in_test where a column starts or stops being recorded within the history?", A: the data as the deployed model met it).

**Assessment (AI, 2026-11-11):** `DISTANCEONLY` is missing in every cohort before 2011; the 2015 and 2016 windows train on 2001-2009 and 2001-2010.

CC (2026-11-17, Andrej): the declared split (temporal on `cohort_year`, windows of 1 value, up to 9 windows while training keeps 50% of the rows (4 in the build), gap 5 values) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split walk, cross-dataset item).

CC (2026-11-27, Andrej): Review issue 1: Option B, `Selection Bias` marker and a `fit_reason` sentence, keep `Yes` ("Selection Bias marker and a fit_reason sentence, keep Yes"). The record carries `Selection Bias`; the fit reason and the notes name the survivor cut (a row exists only if the college is still in the file six years after entry: 699 of 3,335 entry rows absent in the 2015 test cohort, 409 of 3,111 in 2018, for-profit colleges most, and the absent colleges completed less); `fit` stays direct.

CC (2026-11-27, Andrej): Review issue 2: Option B, narrow the wording ("Narrow the wording"). The use case now names the college, or an agency that receives its entry-year report, as the actor and drops "published"; the task, data and split are unchanged.

**Assessment (AI, 2026-11-27):** applied; `dataset check` 0 errors, 1 warning left from before this round (`splits_below_target`, 4 windows against 9) and 1 info; no data change. The text fixes the audit listed for the next edit (the new below-target warning, the `DISTANCEONLY` note, `UG25ABV`, the no-gap R^2 figures, the zip folder date) are not part of these marks and are not applied.

## Review

**Outcome:** added as `college_scorecard`; re-audited 2026-11-27 against the pinned Wayback zip (MD5 matches the recorded ETag): 34,431 rows, 2,569 institutions, 92 features, LightGBM RMSE 0.085 against 0.198 for the dummy on all 4 windows. Decided 2026-11-27: `Selection Bias` and the survivor cut named, `Yes` kept (issue 1, B); the use case narrowed to the college as actor (issue 2, B).

**Main points:** Task gamer (blind, 2026-11-27): nothing gamed. Untuned LightGBM RMSE 0.0851 (0.0824 to 0.0864 over 4 windows; a random column adds 0.0003); institution keys rebuilt from stable columns, missing-value patterns, formats and row order found nothing, and training on all history beats the last 12 years. It suspects `C150_4_LATEST` (worth 0.004) of coming from a later cohort; the definition takes it from the entry-year file, the cohort six years older. The split (one cohort per window, gap five, 2015-2018) holds and stays. Text fixes for the next edit: accept the new `splits_below_target` warning; the `DISTANCEONLY` note should name the 13 other columns first recorded inside the history (dropping all costs 0.002 R^2); `UG25ABV` is recorded in odd years only; "without the gap R^2 0.86 instead of 0.81" recomputes to 0.850 against 0.803; the zip's folder is dated 3 June, not 10 June.

**Issues for Andrej and Lennart:**

1. **Name the survivor cut and add `Selection Bias`?**

   * **Problem:**
     - A row exists only if the institution is still in the file six years after entry (its rate is published then) and its class has 30 or more students; the notes name only the 30-student cut.
     - The survivor cut removes 699 of 3,335 entry rows in the 2015 test cohort and 409 of 3,111 in 2018, for-profit colleges most (57% absent in 2015, 36% in 2018).
   * **Effect on the task:** The removed colleges complete less (prior completion rate 0.34 to 0.39 against 0.52 to 0.53 kept), so the task scores colleges that survived, and a deployed model sees all entering classes, the closing colleges included.
   * **Experiments:**

     | Test cohort | Entry rows | Kept | Absent from file six years later | Class under 30 |
     |---|---|---|---|---|
     | 2015 | 3,335 | 1,842 | 699 | 244 |
     | 2018 | 3,111 | 1,858 | 409 | 265 |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | As now (implemented) | nothing changes | no work | a selection a user cannot see |
     | B | `Selection Bias` marker and a `fit_reason` sentence, keep `Yes` | names the survivor cut and its size; `fit` stays direct | honest at no cost to the task | the cut stays |
     | C | B, and `fit` to approximate | as B, and the task no longer claims the deployed population | states that the closing colleges are missing | one more label to keep in step |

   * **Recommendation:** B: the cut follows from the label (no rate without a later file), so it cannot be undone, only named. **Decision:** A, B or C?

   **Andrej (2026-11-27, change):** Option B: Selection Bias marker and a fit_reason sentence, keep Yes.

   **Resolved (2026-11-27, Andrej):** B. `Selection Bias` is on the record; the `fit_reason` and a note in the curation notes name the survivor cut and its size; `fit` stays direct and the verdict `Yes`. `dataset check` 0 errors.

2. **Narrow the use case's actor to the college?**

   * **Problem:**
     - The use case has a state agency, an accreditor or the college estimate the rate "from the college's published data" when a class enters; every column is reported in the IPEDS year c to c+1, and the file of year c was released about two years after the entry fall (the 2016-17 file in fall 2018).
     - The college holds its own numbers at entry, so the features are available to it, not to an outside actor.
   * **Effect on the task:** For the college the task is as shipped; for an outside actor the latest completion and retention rates would be a file older, R^2 0.803 to 0.789 (0.784 with a gap one cohort longer).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | As now (implemented) | nothing changes | no work | the use case names actors who do not hold the data then |
     | B | Narrow the wording | the actor is the college (or an agency receiving its entry-year report); "published" dropped | same task, true use case | text change |
     | C | Lag the two rates one file | outside actors stay; `C150_4_LATEST` and `RET_FT4` from the previous file | keeps the agency use case | rebuild and its own PR; R^2 0.789 |

   * **Recommendation:** B, as a text change. **Decision:** A, B or C?

   **Notes for the AI:** the column-by-column period table and the horizon options are in `local-data-warehouse/_runs/2026-11-26_review33/college_scorecard/findings_audit.md`.

   **Andrej (2026-11-27, change):** Option B: Narrow the wording.

   **Resolved (2026-11-27, Andrej):** B. The use case's actor is the college (or an agency receiving its entry-year report) and "published" is dropped from it and from the notes on the entry-year features; same task, data and split. `dataset check` 0 errors.
