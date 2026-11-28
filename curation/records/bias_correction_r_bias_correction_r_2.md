---
unique_name: bias_correction_r_bias_correction_r_2
name: Bias_correction_r/Bias_correction_r_2
checked_by:
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
tags:
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Fixed Delay'
- 'Entities: Recur'
- Panel Data
collections:
- TabArena Reject
original_source: UCI
year: '2020'
collection_period: 2013-2017
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://doi.org/10.24432/C59K76
v2_path: datasets/_dev/tabarena-v0pt2/bias_correction_r_bias_correction_r_2/dataset.py
source_row: 739
type_adapter_id: curation-record-v1
---

## Comments

CC: "2 targets. Target is to predict the next-day minimum/maximum air temperature for bias correction. Needs temporal split - although the features themselves are time-invariant, the samples are non-iid"

bias correction in numerical weather prediction (NWP) seems to be a whole research field. Therefore, this is a valid task.

Has two targets: predict min and max temperature of a day. Not sure if it makes sense to use only one

**Assessment (AI, 2026-10-07):** Valid task, added with target `Next_Tmin`. A v2 task holds one target; TALENT's `Bias_correction_r` is `Next_Tmax` and `_r_2` is `Next_Tmin`. On 9 weekly windows of summer 2017, the mean of untuned CatBoost, LightGBM and ridge (RMSE 0.78) beats a per-station MOS of the LDAPS forecast (0.82) on 7 of 9 windows. For `Next_Tmax`, MOS on the forecast alone (1.58) beats every untuned model. The split must be temporal: the 25 stations of a day share its weather (LightGBM RMSE 0.62 on random folds, 1.00 with each day kept together). Prediction point: the evening, once the LDAPS run started at 21 KST is out (Cho et al. 2020, Sec. 2.2-2.3).

CC (2026-10-15, Lennart): The task corrects the LDAPS forecast; without one there is nothing to correct, so the three days without an LDAPS run are dropped.

**Assessment (AI, 2026-10-15):** 75 station-days dropped (2013-08-10, 2016-07-31, 2016-08-20, all on the training side; 7,648 rows remain). On the shipped windows the mean of untuned CatBoost, LightGBM and ridge still beats per-station MOS on forecast and present-day minimum on 7 of 9 windows (RMSE 0.785 against 0.823, paired SE 0.022).

CC (2026-10-15, Lennart): Ship (review of the 2026-10-07 run).

**Assessment (AI, 2026-10-19):** Multi-target removed: one target; the rule from caracas_cervical_cancer (2026-10-15) removes tags that do not apply.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — Cho et al. 2020 report R^2, bias and RMSE side by side (Sec. 3.3) without naming one as the criterion; rmse is the regression fallback (and one of the reported metrics).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `ppnn_ecmwf_t2m_postprocessing_germany` (TBD -> Yes, priority 4), `euppbench_t2m_station_postprocessing` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-17, Andrej): the declared split (temporal on `Date`, windows of 7 days, 9 windows, gap 1 day) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split walk, cross-dataset item).

CC (2026-11-27, Andrej): Review issue 1: Option A, state the measurement and a protocol line ("State the measurement and a protocol line"). The notes and the splits comment now say a station's next-day row, within 0.42 degrees of the label, sits in the same test window for six of seven days, that a model joining it roughly halves its error (untuned LightGBM RMSE 0.809 on each row, 0.438 with the next-day minimum), and that no step may read other test rows; the data and the windows are unchanged.

CC (2026-11-27, Andrej): the declared metric (RMSE on Next_Tmin, over the 9 test windows) is checked and stays as declared.

**Assessment (AI, 2026-11-27):** applied; `dataset check` 0 errors, 7,648 rows and the 9 windows unchanged. Issue 2 (the windows over two summers) has no mark yet and stays open.

CC (2026-11-27, Andrej): Review issue 2: A, confirmed after the consistency check: the nine consecutive weeks of 2017 stay. **Exception to SPLIT-15 (2026-11-27, Andrej):** the windows stay in the newest summer instead of spreading over 2016 and 2017; the newest weeks are the period an evening refit serves, and the spread windows separated the methods no better (paired SEs 0.023-0.047 against 0.028-0.042).

## Review

**Outcome:** added. Re-audited on 2026-11-27: the data reproduce (checksum matches, 7,648 rows recomputed, `dataset check` clean), the second target is not shipped as a feature, the one-day gap is right, and the split tree's leaf matches what ships. Issue 1 decided on 2026-11-27 (A): the next-day row that carries the label is stated with its measurement and a protocol line. One issue is open: the nine windows sit in a single summer for a reason the window rule does not accept (2); your ok of 2026-11-27 waits on the reason to keep them. Needing no decision: the solar radiation column is not the day's observation but the station's calendar-day potential radiation, identical every year, which is why it drifts in every window; and 9 of 25 stations lack the day's minimum on 2017-06-30.

**Main points:** Task gamer (blind, 2026-11-27): found issue 1's leak on its own and at the same size (the same station's next-day `Present_Tmin` cuts RMSE from 0.816 to 0.432); it also proposes dropping `Present_Tmin` and `Present_Tmax`, which removes the evening's own observation that a deployed model has, so the protocol line was chosen instead. Nothing else found. One for you: spread the test windows over two summers with a reason from the data (2).

**Issues for Andrej:**

1. **Say that a station's next-day row in the same test window carries the label?**

   * **Problem:**
     - The target of day d is the next day's minimum temperature, and the same station's row for day d+1 records that day's minimum as an input, within 0.42 degrees of the target (correlation 0.990).
     - For six of the seven days of each window, that next-day row sits inside the same test window, so it is in the frame a participant is handed.
     - The notes say the two are "close to" each other but not that reading it halves the error, and no protocol line forbids it.
   * **Effect on the task:** A model reading each row on its own gains nothing, so the shipped scores are honest; a method that looks at the other test rows, such as a lead feature built over the test frame or an in-context model, roughly halves its error.
   * **Experiments:** untuned LightGBM on the nine shipped windows, with and without the next-day minimum joined from the test window.

     | Measure | RMSE |
     |---|---|
     | the model on each row | 0.809 |
     | the model with the next-day row joined | 0.438 |
     | the training mean | 2.071 |

   * **Consistency:** The same mechanism raised on `rain_in_australia` (the next day's row inside the window) and on `mortgage` (later rows after the window), and the four datasets that carry a protocol line for it. It is also the subject of a cross-dataset item on rows after a test window.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | State the measurement and a protocol line | the notes and the splits comment say no step may read other rows of the test frame, and give the numbers above | cheap and honest; matches the precedents | does not stop misuse |
     | B | Test windows of one day | no next-day row inside a window | closes the channel | 25 rows per window, under the 33-unit floor |
     | C | Leave it as it is (implemented) | nothing changes | no work | the notes do not say a lead feature halves the error |

   * **Recommendation:** A. It follows from the chosen windows, so it is best accepted together with the window decision in issue 2. **Decision:** A, B or C?

   **Andrej (2026-11-27, change):** Option A: State the measurement and a protocol line.

   **Resolved (2026-11-27, Andrej):** A. The curation notes carry a "Potential leak, kept on purpose" line with the measurement and the protocol (each test row is predicted from the training rows and its own features only; no feature or model step may use other test rows), and the splits comment ends with the same protocol line. Data and windows are unchanged; `dataset check` 0 errors.

2. **Spread the test windows over two summers, with the reason restated from the data?**

   * **Problem:**
     - The nine windows are nine consecutive weeks of the summer of 2017, while the window rule prefers other years, then other seasons, then other months, and asks a reason for walking back from the newest.
     - The reason the notes give is a comparison of model scores between window choices, which the rule forbids as the basis for choosing windows.
     - The history offers a second summer: one-week windows in 2016 still keep 64 to 77% of the rows for training.
   * **Effect on the task:** The score measures one summer only, and its newest window is an outlier that dominates any mean across windows: its target averages 18.2 against 23.0 on the training side, and the training mean scores 5.27 there against 1.0 to 2.7 elsewhere.
   * **Options:**

     | | Option | What it does | Test windows (rows; smallest training share) | Pro | Con |
     |---|---|---|---|---|---|
     | A | Nine consecutive weeks of 2017 (implemented) | as shipped | 1,538 rows; 80% | the newest period tested | one summer, chosen on scores |
     | B | Nine one-week windows over 2016 and 2017 | alternate weeks of two summers | 1,516 rows; 64% | a second year | the oldest windows train on three summers |
     | C | As B with 14-day windows | longer windows | 9 windows of 14 days | more rows per window | at the upper edge of a week or two for weather |

   * **Recommendation:** B, with the reason restated from the data (target and feature drift by window) rather than from model scores. **Decision:** A, B or C?

   **Notes for the AI:** B is a split change: new cutoffs in `temporal`, the splits comment rewritten from data statistics, `dataset check` re-run, its own pull request. Whether the source paper defines its own split (training on 2013-2016 and testing on 2017) was not checked; if it does, the rule to follow a source-defined split comes first.

   **Andrej (2026-11-27, ok):** As implemented (A).

   **Answer (AI, 2026-11-27):**
   * A consistency check before applying: A keeps windows whose only recorded reason is a comparison of model scores, which the window rule does not accept as the basis for choosing windows. The windows themselves can stay; the reason cannot.
   * Keeping A needs a reason from the data or the use, for example that the newest weeks are the period a deployed forecaster serves. Under A the score comparison leaves the notes and that reason replaces it.
   * **Decision:** A with a reason from the data (which one?), or B as recommended?

   **Andrej (2026-11-27, ok):** As implemented (A), confirmed after the consistency check.

   **Resolved (2026-11-27, Andrej):** A, confirmed as a departure from the window rule's preference for other years and seasons: the nine consecutive weeks of 2017 stay as the test windows (1,538 test rows, 80% training floor); no change to the definition.

**Review panel:** ship after changes (re-audit against the source, 2026-11-27; no separate mediator). Claims: the row
count and every dropped day reproduce; the solar radiation column is mislabelled as an observation. Columns: no
post-outcome value. Split: the tree reaches the leaf that ships; window placement is disputed (issue 2). Disputed:
the next-day row (issue 1) and the windows (issue 2).

## Reference

Cho, D., Yoo, C., & Im, J. (2020). Comparative Assessment of Various Machine Learning-Based Bias Correction Methods for Numerical Weather Prediction Model Forecasts of Extreme Air Temperatures in Urban Areas. Earth and Space Science, 7(4), e2019EA000740. DOI: 10.1029/2019EA000740.
