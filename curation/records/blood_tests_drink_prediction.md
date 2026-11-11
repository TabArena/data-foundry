---
unique_name: blood_tests_drink_prediction
name: liver-disorders
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: No (Retired)
decision_markers:
- Outdated
- Not Representative
- Selection Bias
- No Good Target / Scientific Discovery
tags:
- Tiny Data
collections:
- TabArena Reject
original_source: UCI
year: '1990'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.openml.org/d/8
- https://doi.org/10.24432/C54G67
notebook_path: datasets/beyond_iid/new_iid/blood_tests_drink_prediction/blood_tests_drink_prediction.ipynb
source_row: 751
type_adapter_id: curation-record-v1
---

## Comments

need to create the drinks column as a target, need to see if it is still a good task then. (drinks>5) otherwise, we can just treat it as a regression task...

Unclear if the target makes for a relevant, real-world dataset but for now we can add it and filter later again (which might happen)

Discussion: Task is to predict no. of drinks a person consumes as a proxy for liver diseases based on blood tests. This is not a meaningful task, e.g., what kind of decision would it motivate? If a doctor has the time to collect blood samples, asking for drinking behavior is simple.
Also, there is selection bias as almost only drinking people (336/345) and only males are in the sample.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — The source frames a classification of liver disorder (the selector column was misread as the label); McDermott & Forsyth say the intended label is drinks dichotomised, with no metric for a regression on the count. Our regression on drinks is our own task, so the regression fallback applies.

**Assessment (AI, 2026-10-21):** metric now `Metric.from_context("rmsle", target_transform="log1p")` instead of the fallback rmse on the log1p target: drinks per day is a right-skewed count whose error matters relative to the amount; the target still ships as log1p, and RMSLE is computed after the inverse, on the original scale (MET-3). Needs a rebuild to reach the container.

CC (2026-10-21, Lennart): ship the target on the modelling scale, score on the original scale (target_transform).

**Assessment (AI, 2026-10-27):** The open questions for the curator are in the folder's `REVIEW.md` (review of the Tiny Data datasets, written from the earlier findings, no review panel); the AI recommends shipping it. Priority 1: gap -, use case - (written by the curators), source +, shape -, risk - (undocumented label origin; `Trivial` untested).
**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `nhanes_alcohol_drinks_from_blood_tests` (TBD -> 2nd Tier, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the folder's `REVIEW.md`. Keep with changes: the source's own task (drinks from blood markers) with a weak but real signal; drop the four records entered twice (a lookup of the copies beats every benchmark method) and remove the refuted Trivial marker. Priority 1: gap 0, use case 0, source 1, shape 0, risk -1.

CC (2026-11-05, Andrej): retired (`No (Retired)`, `No Good Target / Scientific Discovery`): no decision rests on the prediction. The data is the BUPA liver-disorders file (UCI, 1990): 345 men, five blood tests that respond to alcohol, and the number of drinks per day each reported.
- **As a stand-in for liver damage it fails:** the file was framed as a test for liver disorders with the drinks as a proxy (McDermott & Forsyth 2016: the intended label is the drinks, cut into two classes), but a drink count is not a measure of damage, and the blood tests themselves are the better measure.
- **As the definition's use case it leads to nothing:** the definition reads it as checking a patient's account of drinking from blood markers; once a doctor has the blood values, those values guide what happens next, and an estimate of the drinks adds nothing to act on (asking is simpler).
- **The sample would not carry over:** men only, 336 of 345 drink, and how the drinks were recorded is not stated.
Not changed: `Trivial` stays for now (open on the review page: the single-feature test refuted it, skill +0.05 against +0.10 to +0.17 for the methods). Had the dataset stayed, the four records entered twice would have been dropped.

CC (2026-11-10, Andrej): `Trivial` removed (review page issue 2, B): the test refuted it; the best single feature reaches skill +0.05 against +0.10 to +0.17 for every method configuration. The retirement's reasons stand.

CC (2026-11-11, Andrej): review marks on the three issues; this record already carries the state they ask for, so nothing changed beyond the review itself.

- Issue 1 (change, no note): the retirement stands. `No (Retired)` with `No Good Target / Scientific Discovery`, `v2_path` cleared, no folder in the working copy: a drink count is no measure of liver damage, the file's first framing, and once the blood values are known they guide what happens next, so an estimate of the drinks adds nothing to act on.
- Issue 2 (ok, "Reply (B): Remove Trivial"): `Trivial` is not among the markers. Its test refuted it: on 39 shipped folds the best single feature reaches skill +0.05 against +0.10 to +0.17 for every one of the 29 method configurations (TP-4).
- Issue 3 (change, no note): no change to make, the dataset being retired; the four records that appear twice (identical in the five blood tests and in the drinks, which no chance match explains) stay on record for anyone who revives these rows and for `nhanes_alcohol_drinks_from_blood_tests`.
- The review moved from the folder's `REVIEW.md` (the folder is gone; the file was still in the other working copy) into this record's `## Review` section.

## Review

**Outcome:** added. The BUPA liver-disorders file (UCI, 1990): 345 men, five blood tests that respond to alcohol, and
the number of drinks per day, shipped on the log scale and scored by RMSLE on the count. Reviewed without a panel, from
the gathered evidence: the record, model runs on the shipped BeyondArena data (the same rows) and two checks
of 2026-11-04. The AI recommends keeping it with one change to the data, dropping the second copy of four records
entered twice (issue 3), and without the `Trivial` marker (issue 2). Validity: estimating a man's drinking from blood
markers is the task the data was collected for (SEL-8; the old "liver disorder" label was the train/test selector), but
the origin of the label is not stated and the use case is doubted (issue 1); four records are in the file twice with the
same label, which no chance match explains, so about two test rows per split find their copy in training (issue 3).
Value: every method configuration beats the mean on average, with a small spread (skill +0.10 to +0.17, R² about 0.15);
one raw feature reaches +0.05 and beats no method, so the record's `Trivial` does not hold (issue 2). Quality: men only,
336 of 345 drink (`Selection Bias`). Weighed: the source's own task against a label of unknown origin and a weak signal.

**Main points:** Retired (2026-11-05, issue 1); the refuted `Trivial` removed from the record (issue 2, resolved
2026-11-10). Nothing open.

**Record judgment:** valid source, weak use case. The Discussion asks what decision the prediction would support and
notes the selection; Lennart kept it to "filter later". The suggestion is `Yes (Disagreement)`. The data-scouting run
of 2026-10-31 screened `nhanes_alcohol_drinks_from_blood_tests` (AI-filled, `TBD -> 2nd Tier`): the same five tests
and a drinking question for thousands of adults, with the same doubt about the use case.

**Issues for Andrej:**

1. **Retire because no decision rests on predicting drinks from blood tests?**

   * **Problem:**
     - The target is the number of drinks per day, and the source does not say how it was recorded (an interview,
       a diary).
     - The Discussion argues that a doctor who takes blood can just ask about drinking, and that the sample is almost
       all drinkers and only men.
     - Keep the regression on drinks with the approximate fit, or retire the dataset?
   * **Background:** the file's intended label is the number of drinks, dichotomised: McDermott J, Forsyth RS.
     Diagnosing a disorder in a classification benchmark. Pattern Recognit Lett. 2016;73:41-43.
     https://doi.org/10.1016/j.patrec.2016.01.004, as the UCI page notes (https://doi.org/10.24432/C54G67). So the
     regression is a variant of the source's task, not a relabelling[^1b]. Gamma-GT, the liver enzymes (ALT, AST) and
     the red-cell volume (MCV) are used in practice as objective markers when a patient's account is in doubt; that is
     the use case in `task_summary`.
   * **Effect on the task:** if the label is the men's own account, a model learns to reproduce the account that the
     markers are meant to check, and under-reporting carries into the target. The predicted amounts refer to this
     sample, not to a clinic's patients.
   * **Consistency:** cdc_diabetes_health_indicators and stroke_prediction were set to `No` because the label was a
     diagnosis the person already had, recorded with the features[^1c]; here the features are lab measurements and
     the label an amount, not a diagnosis.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as defined (implemented) | regression on drinks, fit approximate, the unknown origin of the label and the reviewers' doubt named in `fit_reason` | the source's intended label; a check doctors make | a weak use case and a narrow sample stay |
     | B | Retire | `No (Retired)` with `No Good Target / Scientific Discovery` | no task with a doubted decision behind it | the one alcohol-marker task leaves |

   * **Recommendation:** A: the regression is the source's own task, and an unverified label definition makes the fit
     approximate, not the task invalid[^1a]. **Decision:** keep (A) or retire (B)?

   **Notes for the AI:** on B: `suggestion: No (Retired)`, marker `No Good Target / Scientific Discovery`, a dated CC
   line, the folder removed with a CHANGELOG entry and `v2_path` cleared.

   [^1a]: **USE-8** (Must): an unverified label definition is a known gap and makes the fit approximate; **SEL-3**
     (Must): the target is an observed outcome or an expert annotation, simulating a decision someone makes with the
     prediction.
   [^1b]: **SEL-8** (Must): the original task decides the scope; trace what the data was collected and used for.
   [^1c]: **SEL-7** (Must): a label the respondent already knows, asked in the same interview as the features, is
     predicted by nobody.

   **Andrej (2026-11-05, change):** Retire this dataset because it is flawed in many ways:
   - The task does not make sense. Originally it was made up as a proxy for liver damage. Now Claude made up a different
     task, but this one does not make sense because once a doctor knows the blood values, predicting the drinking
     behavior from them does not lead to anything actionable.

   **Resolved (2026-11-05, Andrej):** retired (B): the record is `No (Retired)` with `No Good Target / Scientific
   Discovery`, and its CC line gives the reasons: a drink count is no measure of liver damage, the file's first framing;
   and once the blood values are known they guide what happens next, so an estimate of the drinks adds nothing to act
   on; men only, 336 of 345 drinkers. The regression on drinks itself was not new (the curators' first note and Lennart's
   metric of 2026-10-21; McDermott & Forsyth name the drinks as the intended label), so the CC line rests on the missing
   decision. The folder stays until this file is committed. The same ground applies to
   nhanes_alcohol_drinks_from_blood_tests (screened `2nd Tier`, the same five tests), not changed here.

   **Resolved (2026-11-11, Andrej):** his mark of today (change, no note) confirms the retirement, which this branch
   carries: `suggestion: No (Retired)` with `No Good Target / Scientific Discovery`, `v2_path` cleared and no folder in
   the working copy.

2. **Only if the dataset stays: remove the `Trivial` marker, now that the test has run?**

   * **Problem:**
     - The record carries `Trivial`, which needs proof that one raw feature, chosen on each split's training side,
       matches or beats the methods fold by fold.
     - That test ran on 2026-11-04 on the shipped data: the best single feature scores below all 29 method
       configurations on average and below the best one on every fold.
     - Keep the marker, or remove it?
   * **Effect on the task:** none on the data; on the record the marker reads as a reason not to ship.
   * **Experiments:** on 39 shipped folds (those 90% of the methods cover), RMSE on the log scale: the mean 0.739;
     the best single feature (gamma-GT on 21 folds, MCV on 18), as a monotone fit on the training side, 0.720 (skill
     +0.05); the 29 configurations 0.673 to 0.703 (skill +0.10 to +0.17, median +0.14), every one above the mean on
     35 or more folds, 2 tied with the best, rank agreement across folds 0.35 (Kendall's W). The signal is real but
     weak (R² about 0.15), not trivial.
   * **Consistency:** follows thyroid_discordant, whose `Trivial` was removed on 2026-10-22 after the same test.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `Trivial` (implemented) | the record unchanged | none found | the test refutes it |
     | B | Remove `Trivial` | the marker leaves the record, with a dated line giving the test | the record says what was measured | none found |

   * **Recommendation:** B: one raw feature is far behind every method[^2a]. **Decision:** keep (A) or remove (B)?

   **Notes for the AI:** on B, remove `Trivial` from `decision_markers` and add a CC line with the numbers above
   (`tuned_results.py blood_tests_drink_prediction --feature auto`, BeyondArena runs).

   [^2a]: **TP-4** (Must): `Trivial` needs proof: the raw feature, chosen on each split's training side, has to match
     or beat the methods fold by fold. Cases: fitness_club (yes), sepsis_survival and california (no).

   **Answer (AI, 2026-11-05):**

   * **Your mark:** as implemented, so `Trivial` stays on the retired record.
   * **Found:** on a retired record the markers read as its reasons, and this one was refuted: the best single feature
     reaches skill +0.05 against +0.10 to +0.17 for every method configuration[^d1]. A refuted `Trivial` was removed from a
     `No` record before (heart_disease_switzerland, 2026-10-27) and from thyroid_discordant (2026-10-22). What sets this
     one apart?

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `Trivial` (your mark) | the record unchanged | none found | the record gives a reason the test refuted |
     | B | Remove `Trivial` | the marker leaves, with a dated line giving the test | the record's reasons are the ones that hold | none found |

   * **Recommendation:** B: the issue applied only if the dataset stayed, and the marker should leave either way.
     **Decision:** keep (A) or remove (B)?

   [^d1]: **TP-4** (Must): `Trivial` needs proof: the raw feature, chosen on each split's training side, has to match
     or beat the methods fold by fold.

   **Andrej (2026-11-10, ok):** Reply (B): Remove Trivial.

   **Resolved (2026-11-10, Andrej):** B: `Trivial` left the record, with a dated line giving the test (best single
   feature skill +0.05 against +0.10 to +0.17 for every method).

   **Andrej (2026-11-11, ok):** Reply (B): Remove Trivial

   **Resolved (2026-11-11, Andrej):** B, confirmed: this branch's copy of the record carries `Outdated`, `Not
   Representative`, `Selection Bias` and `No Good Target / Scientific Discovery`, and no `Trivial`. Nothing further to
   apply.

3. **Drop the second copy of the four records that are in the file twice?**

   * **Problem:**
     - Four records appear twice, identical in all five blood tests and in the number of drinks, and the definition
       keeps them as natural duplicates.
     - With five integer lab values, no copy arises by chance: none of 500 tables with each column shuffled on its
       own held a single repeated row.
     - Drop one copy of each pair (341 rows), or keep all 345?
   * **Effect on the task:** on a random split about two test rows per split (0 to 3 of 115) have their copy among the
     training rows and are predicted by recall of the copy, which a new patient never offers.
   * **Experiments:** model runs on the shipped data found the copies and used them: a ridge model on the
     log blood tests scored RMSE 0.6717, and the same model taking a copy's label where one exists 0.6676, ahead of
     the best of 40 benchmark methods (0.6726); the lookup is worth about as much as the gap between the first and the
     sixth benchmark method. The check of 2026-11-04 found no near copies (one value changed by up to 10 units), as
     few as chance gives (0.18 per shuffled table).
   * **Consistency:** follows obesity_estimation (its 10 exact copies dropped, 2026-10-14) and audiology_diagnosis (27
     copies dropped)[^3a]. A copy of one record is a collection artefact when the columns leave many values to
     match[^3b].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep all rows (implemented) | 345 rows, four records twice | the file as published | about two test rows per split are recalled, not predicted |
     | B | Drop the second copy | 341 rows; a `curation_comments` bullet with the check | each record once; nothing to recall | a new checksum, a rebuild |

   * **Recommendation:** B: the copies are no natural repeats, and a lookup of them moves the ranking.
     **Decision:** keep (A) or drop the copies (B)?

   **Notes for the AI:** on B, add `df = df.drop_duplicates()` in `_clean` after dropping `selector` (the pairs are
   rows 58/317, 72/201, 192/204 and 212/330 of the BeyondArena container), replace the bullet "The data contains natural
   duplicates, so we keep them." with the check, re-run `dataset check` (the `dataset_duplicate_rows` warning goes)
   and add a CHANGELOG entry.

   [^3a]: **LEAK-19** (Should): exact copies with the same label are dropped rather than grouped on the duplicate key.
   [^3b]: **LEAK-18** (Should): many degrees of freedom and an exact match: a collection artefact, drop it and give the
     share; few features and plausible repeats: natural, keep them and say so.

   **Andrej (2026-11-05, change):** If we would keep the task, we would drop.

   **Resolved (2026-11-05, Andrej):** no change: the dataset is retired (issue 1); had it stayed, the second copy of the
   four records would have been dropped (B).

   **Resolved (2026-11-11, Andrej):** his mark of today (change, no note) changes nothing: the dataset is retired, so
   there is no definition to drop the copies from. The finding stays on record for
   `nhanes_alcohol_drinks_from_blood_tests` and for anyone who revives these rows: four records appear twice,
   identical in the five blood tests and the number of drinks, which no chance match explains (none of 500 tables
   with each column shuffled held a repeated row).

## Reference

@book{forsyth1986machine,
  title={Machine learning: applications in expert systems and information retrieval},
  author={Forsyth, Richard and Rada, Roy},
  year={1986},
  publisher={Halsted Press}
}
