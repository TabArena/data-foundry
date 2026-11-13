---
unique_name: thyroid_discordant
name: Thyroid Disease
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (DF)
claimed_by: Andrej
suggestion: No (Retired)
decision_markers:
- Duplicate
tags:
- Tiny Data
- New IID
collections:
- TabArena Reject
- TabSTAR
original_source: UCI
year: '1987'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.24432/C5D010
notebook_path: datasets/beyond_iid/new_iid/thyroid_discordant/thyroid_discordant.ipynb
source_row: 790
type_adapter_id: curation-record-v1
---

## Comments

Data might be trivial, could be good to investigate all the data in this collection and add all the useful cases

Checkout all the data and add the datasets as we see valid

Insights from the reference:
1. Hypothyroid -> main dataset
2. dis -> version / same data as Hypothyroid

Based on this, we strongly believe that all other cases that have the same sample and feature count as listed below are just different versions/duplicates of Hypothyroid! Thus, for now, we only take Hypothyroid and ignore the other faulty entries. We might come back to this if Hypothyroid is too simple.
After a simple test, we saw that Hypothyroid is trivial to solve (almost 100 ROC AUC). Hence, we use dis instead. It still seems trivial. We will likely filter this later.


Patient ID at the end of the line does not matter.


A lot of weird data but a lot of okay ones that are super similar, so likely not use multiple? Read paper and make judgement call

Data in the repo:
1. thyroid0387 - Thyroid disease, Garavan Institute -> does not have a real target but just various diagnosis, seems like a scientific discovery task without a good target
2. sick-euthyroid.data -> according to UCI it might be corrupted, the .names file does not include any more information, missing more source information this is quite risky to use
3. sick -> has a clear class, but is missing any source information (first entry in the UCI description), likely a real predictive task
4. new-thyroid -> data from Stefan Aeberhard, seems good and has more source information
5. Hypothyroid -> same as sick-euthyroid
6. dis -> same as sick, looks good
7. ann-thyroid -> same as above, good
8. allrep -> same as above, good
9. allhypo -> same as above
10. allhyper -> same as above
11. allbp -> same as above

**Assessment (AI, 2026-10-19):** open since the leak audit of 2026-10-01 (no leak): one row has an `age` of 455. Under the rule for impossible values (they become missing and the row stays; caracas_cervical_cancer, 2026-10-15) the definition should set it to missing in the next pass.

CC (2026-10-21, Lennart): "ok" on the cross-dataset item that the `Trivial` marker was never tested under TP-4: run the test and keep or remove the marker by the result.

**Assessment (AI, 2026-10-21):** TP-4 test on the 30 shipped splits: the best single raw feature, chosen on each training side, is `FTI` on all 30, ROC AUC 0.822 on average (0.691 to 0.897), against 0.974 (0.913 to 0.996) for a default random forest and 0.973 (0.900 to 0.996) for LightGBM; the single feature is worse than both on 30 of 30 splits (task probe: one-feature LightGBM 0.869, random forest 0.976, no flag). The marker is refuted; recommend removing it (Review issue 1); the curator has the call.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — no publication defines a task or metric for the discordant file; accuracy is uninformative at about 1.6% positives.

CC (2026-10-22, Lennart): verdict ship. Issue 1: remove the `Trivial` marker and go ahead.

**Assessment (AI, 2026-10-22):** `Trivial` removed (TP-4: the best single feature, `FTI`, reaches ROC AUC 0.822 against 0.974 for a random forest on the 30 shipped splits). REVIEW.md removed (nothing left open). Not built yet.

**Assessment (AI, 2026-10-27):** The open questions for the curator are in the record's Review (review of the Tiny Data datasets, written from the earlier findings, no review panel); the AI recommends shipping it after changes. Priority 2: gap -, use case - (the label is undefined; our use case), source +, shape +, risk - (the label may be a rule on the five tests, untested).

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship: shallow trees on the five thyroid tests reach ROC AUC 0.83-0.87 against 0.975 for a random forest on all 30 splits, so the undefined 'discordant' label is no short rule and the methods spread; set the impossible age of 455 to missing first. Priority 2: gap 0, use case 0, source 1, shape 1, risk -1.

CC (2026-11-11, Andrej): Review issue 3, option B: set the impossible age of 455 to missing.
- Applied: `_clean` sets `age` above 120 to missing and keeps the row (one patient); curation note added; `dataset check` passes (0 errors, 0 warnings), new checksum v2:5ab55ec0, not built.

**Assessment (AI, 2026-11-12):** the shallow-tree check on the label (Review issue 2), the 30 shipped splits, ROC AUC:

| Model | Inputs | ROC AUC |
|---|---|---|
| Decision tree, depth 2 to 5 | the five thyroid tests (TSH, T3, TT4, T4U, FTI) | 0.833 to 0.871 (0.60 to 0.98 per split) |
| Decision tree, depth 3 | all features | 0.872 |
| Random forest | the five thyroid tests | 0.967 |
| Random forest | all features | 0.975 |
| LightGBM | all features | 0.974 |

No tree reaches the forest or LightGBM on any of the 30 splits; the best depth-3 tree puts 45 of the 58 discordant patients in one pocket (FTI above 155.5, T3 at most 3.55, TSH above 0.01) with 126 other patients. So the label is a reading of the five tests, but not a short rule on them.

CC (2026-11-12, Andrej): Review issue 2, option A: ship as is, no `Trivial` marker.
- The label "discordant" is undefined by the source and reads the five thyroid tests, but shallow trees on them stay far below the methods on every split (0.83 to 0.87 against 0.975), so it is no short rule; fit `approximate` with the undefined label in `fit_reason`, as before. `dataset.py` unchanged.

CC (2026-11-12, Andrej): retired (`No (Retired)`, `Duplicate`; BeyondArena v0.2 review page, issue 4, reply a, after thyroid_discordant_archive's issue 1, B): `thyroid_discordant_archive` is the copy that stays and ships, the same discordant task from the source's fuller version of the archive (`thyroid0387`, 9,162 requests and 197 discordant against 3,711 and 58 here, split by request date). It holds 3,553 of this dataset's 3,711 rows with the same label for all 58 positives (PROV-6). This file, one of Quinlan's 1987 extracts from the same UCI zip, came in by lineage and was never chosen over the archive. The folder stays until the retirement PR removes it and clears `v2_path`; the claim stays.

## Review

**Outcome:** added; retired on 2026-11-12 as `Duplicate` of thyroid_discordant_archive, which ships (issue 4, a);
the folder leaves in a retirement PR. Before that the AI recommended shipping it; the one fix, the impossible age of
455 set to missing, is applied (issue 3).
The shallow-tree check that issue 2 asked for was run on 2026-11-04: the label is not a short rule on the five thyroid
tests, so it stays. Reviewed without a review panel, from the record, the earlier experiments and a model run on
the shipped data (same 3,711 rows and 26 features as the v0.2 frame). Validity: the Garvan Institute records via UCI's
`dis` file; the label "discordant" (1.56%, 58 patients) is a reading of the thyroid test results that the source does
not define, which `fit_reason` names (fit `approximate`). Value: shallow trees on the five tests reach ROC AUC 0.83 to
0.87 against 0.975 for a random forest, below it on 30 of 30 splits; the benchmark methods spread widely (best 0.991,
median 0.983, logistic regression 0.825 to 0.836), and the `Trivial` marker was refuted and removed on 2026-10-22.
Quality: the one impossible age (455) is missing since 2026-11-11 (issue 3). Weighed: a large, clean
clinical file whose methods separate +, a label of unknown origin that only automates a reading of the same tests -.

**Main points:** Nothing open. Retired as `Duplicate` of thyroid_discordant_archive (issue 4, a, 2026-11-12); the
folder leaves in a retirement PR. Settled before: ship as is, since the shallow-tree check finds no short rule on the
five tests (issue 2, A, 2026-11-12); the age of 455 is missing (issue 3, B, 2026-11-11).

**Record judgment:** valid, with the label's origin unknown (fit `approximate`). The `Trivial` marker was removed by
Lennart on 2026-10-22 after the single-feature test (`FTI` 0.822 against 0.974). The record's two links to copies of the
new-thyroid file, another dataset of the same UCI collection, were replaced on 2026-10-27 by the definition's link
(https://doi.org/10.24432/C5D010).

**Issues for Andrej:**

2. **Is "discordant" a rule on the five thyroid tests? The shallow-tree check is run: ship?**

   * **Problem:**
     - The label marks a case as discordant, a reading of the thyroid test results (TSH, T3, TT4, T4U, FTI) that are
       features, and the source does not say who assigned it or by what rule.
     - If a few cut-offs on the five tests give the label, the model learns that rule and the task is `Trivial`;
       otherwise the task automates an expert's reading, the approximate fit the definition states.
     - The check asked for on 2026-10-27 is now run and finds no short rule: ship as is, or retire?
   * **Background:** TSH, T3, TT4, T4U and FTI are blood tests of thyroid function (FTI, the free thyroxine index, is
     TT4 divided by T4U). "Discordant" results are test values that contradict each other. `fit_reason` already says
     the model reproduces that reading rather than predicting an outcome, which serves only to automate it. A label
     set by a published rule from the columns is `Trivial` when the rule's inputs are the whole task, and a shallow
     tree on the defining columns is the test[^2a].
   * **Experiments:**
     - Earlier (2026-10-21): one feature does not give it: `FTI`, the best single feature on all 30 training sides,
       ROC AUC 0.822 against 0.974 for a random forest, lower on 30 of 30 splits.
     - Shallow trees (2026-11-04, the 30 shipped splits): decision trees of depth 2 to 5 on the five tests reach ROC
       AUC 0.833 to 0.871 on average (0.60 to 0.98 per split), a depth-3 tree on all features 0.872, against 0.975 for
       a random forest and 0.974 for LightGBM on all features; no tree reaches either on any of the 30 splits. A
       random forest on the five tests alone reaches 0.967, so the label is a reading of these tests, but not a short
       one.
     - The best depth-3 tree puts 45 of the 58 discordant patients in one pocket (FTI above 155.5, T3 at most 3.55,
       TSH above 0.01), together with 126 other patients; the other 13 are spread over the rest.
     - A model run on the shipped data: 40 benchmark methods from ROC AUC 0.991 (best) over 0.983 (median) to 0.825
       (tuned logistic regression); a rule list on the tests, added to a CatBoost and density model, ranks 5th of 41
       (0.989), not above the best methods.
   * **Consistency:** the same question is open on audiology_diagnosis (five defining tests reach 0.903 accuracy, all
     features 0.938) and biomechanical_orthopaedic_prediction, both still disputed. Unlike them, here no short rule
     on the defining tests comes close to the methods.
   * **Unknown:** who assigned the label. One reading takes it as the output of the Garvan Institute's
     expert system for thyroid reports (threshold rules on the tests, sex and the treatment flags); that is its
     reading, not checked against Quinlan et al. 1987, the papers that would say so. Even if so, the forests do not
     recover it exactly (0.975), so it is not a rule on the shipped columns that a model can read off.
   * **Sources:** Quinlan JR. Simplifying decision trees. Int J Man-Mach Stud. 1987;27(3):221-234.
     doi:10.1016/S0020-7373(87)80053-6. UCI Thyroid Disease: https://doi.org/10.24432/C5D010.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship as is (implemented) | all features, fit `approximate` with the undefined label named in `fit_reason` | no short rule on the five tests matches the methods (0.87 against 0.975); the methods spread widely | the task automates an undefined reading of the same tests |
     | B | Retire as `Trivial` | record `No`, marker `Trivial`, folder removed | none found: the check that would support it came out the other way | loses a task on which the methods separate |

   * **Recommendation:** A, ship: the shallow trees stay far below the methods on every split, and the methods
     separate. **Decision:** ship as is (A), or retire (B)?

   **Notes for the AI:** the check script and its log are in the review's checks folder for this dataset (job
   1344939); on A, add a dated Assessment line to the record with the tree numbers.

   [^2a]: **SEL-5** (Must): a label the source computes with a published, deterministic rule from the columns: drop
     the rule's inputs when the rest still makes a real task, `Trivial` when the inputs are the whole task.
     **LEAK-4** (Must): a depth-2 or depth-3 tree on the label's defining columns shows whether the target is a rule.
     **TP-4** (Must): `Trivial` needs proof. **TP-3** (Must): if tuned methods spread, keep the dataset. The
     circular-feature check of the verification list asks whether a feature is the criterion that assigns the label.

   **Resolved (2026-11-12, Andrej):** A (`ok`): ship as is, all features, fit `approximate` with the undefined label
   named in `fit_reason`, no `Trivial` marker: shallow trees on the five tests reach ROC AUC 0.833 to 0.871 against
   0.975 for a random forest, below it on 30 of 30 splits. `dataset.py` unchanged; the record has an Assessment line
   with the tree numbers and a CC line.

3. **Set the impossible age of 455 to missing?**

   * **Problem:**
     - One patient has `age` 455, the README's maximum; no other age is above 120 (checked on the shipped table).
     - The leak audit of 2026-10-01 found it, and the record's assessment of 2026-10-19 says the definition should set
       it to missing, but `_clean` does not.
     - Set it to missing and keep the row?
   * **Background:** impossible values become missing and the row stays[^3a]. The rule's case table already lists
     this dataset with "`age = 455`: missing, applied", so the knowledge file and the definition disagree.
   * **Effect on the task:** one row carries an age no patient can have; a model may treat it as an extreme age.
   * **Consistency:** follows caracas_cervical_cancer (impossible values set to missing, 2026-10-15).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep it (implemented) | the value ships | none found | an impossible value; contradicts the rule's case table |
     | B | Set it to missing | `age` missing for that row, the row stays; the checksum changes | follows the rule and its case row | a rebuild |

   * **Recommendation:** B, set it to missing. **Decision:** keep (A), or set to missing (B)?

   **Notes for the AI:** on B, in `_clean` set `df.loc[df["age"] > 120, "age"] = np.nan` (import numpy), add a
   curation note, run `dataset check` and a CHANGELOG entry. The 2026-10-27 file lettered these options the other way
   round ((a) set to missing, (b) keep); the recommendation is the same.

   [^3a]: **CLEAN-11** (Should): impossible values become missing, and the row stays; values that are only unusual
     stay.

   **Resolved (2026-11-11, Andrej):** B: `_clean` sets `age` above 120 to missing and keeps the row (one patient);
   curation note added; `dataset check` passes (0 errors, 0 warnings, 3,711 rows), checksum `v2:5ab55ec0`, not built.

4. **Split by time, or keep the random split as a stationary relation?**

   * **Problem:**
     - The record numbers the definition strips from the label lead to the request dates: 3,553 of the 3,711 shipped
       patients match exactly one record of the Garvan archive in the same UCI folder (`thyroid0387`), whose ids carry
       the date, January to December 1985, and a lab flags later requests, so the request date is information for
       the split[^4a].
     - The newest half of the year holds only 30 discordant patients, 2 to 8 per monthly window and 6 to 15 per
       two-month window, so a temporal score would rest on a handful of positives, which the rules call too few[^4b].
     - Keep the random split as a stationary relation, or split by request date?
   * **Background:** each raw row ends with `|<record number>`; its 29 recorded values match one `thyroid0387` record,
     whose id is the date (YYMMDD) and a sequence number, for 3,563 of the 3,772 raw rows (1985 for 3,553; 10 match a
     1987 id and count as undated). All 58 discordant patients are dated, and the 158 undated shipped rows hold none.
     The record number follows the date only roughly (Spearman 0.87). The discordant share is flat over the year: 0.5%
     to 2.2% in each month with more than one request, no trend (chi-square across months, p = 0.82).
   * **Experiments:** the 3,711 shipped rows and 26 features, untuned LightGBM and logistic regression (one-hot
     categories), ROC AUC (Slurm job 1365900):
     - Shipped random split (10 x 3): LightGBM 0.974 (0.919 to 0.996), logistic regression 0.811.
     - Five monthly windows, August to December, each trained on all earlier dated months (50% to 92% of the dated
       rows): LightGBM 0.946 to 0.998, logistic regression 0.68 to 0.92; three two-month windows (August-September,
       October-November, December): LightGBM 0.946, 0.989 and 0.998.
     - Same test patients and same training size (each window in 3 folds, 3 seeds; earlier months only against rows
       drawn from all months), pooled over the five monthly windows (1,760 rows, 30 positives): LightGBM 0.980 against
       0.973 (seeds 0.963 to 0.989), logistic regression 0.806 against 0.845 (0.821 to 0.877); the fold-level
       differences have standard deviations of 0.004 to 0.18, so neither is told apart from noise.
   * **Effect on the task:** with a flat label share, a random split could flatter a model only through a change in
     how cases were read during the year, and none is measurable; a temporal test would mostly add noise.
   * **Unknown:** whether the labelling changed during 1985; Quinlan's papers or the Garvan Institute would say.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random split as a stationary relation (implemented) | 10 x 3 random folds; the definition gets the tag `StationaryRelation` and a `Time basis:` line: the requests are dated through the archive's ids, the discordant share is flat over the months and the windows (2 to 15 positives each) score within noise of random training | 30 splits over all 58 positives; no measurable cost; the target, a reading of the current tests, fits the prototype | the request order is known and unused |
     | B | Three windows by request date | the time from `thyroid0387`, the 158 undated rows dropped; test August-September, October-November and December 1985, each trained on all earlier months (50%, 72% and 92% of the dated rows) | tests later requests, as a lab meets them | 15, 9 and 6 positives per window, so the scores are near noise; the time rests on a match with another file of the folder |

   * **Recommendation:** A: each window would hold a handful of positives, the discordant share does not move over the
     year, and the measured difference is within the noise, so the stationary relation is shown as far as the data
     can show it and keeps a stable score. **Decision:** A or B?

   **Notes for the AI:** on A, once PR #50 is in: `data_tags = ("StationaryRelation",)`; a curation bullet `- Time
   basis: StationaryRelation: the requests are dated through their record numbers: 3,553 of 3,711 rows match exactly one
   record of thyroid0387 (same UCI folder), whose ids give January to December 1985; not split by date, because the
   newest half of the year holds 30 discordant patients (2 to 8 per monthly window) and the discordant share is flat
   over the months (chi-square p = 0.82); five monthly windows (August to December) score as random training of the
   same size within noise (untuned LightGBM 0.980 against 0.973 pooled; logistic regression 0.806 against 0.845, seed
   range 0.821 to 0.877).` The frame has no date column, so no warning to accept. On B, `download_description` also
   extracts `thyroid0387.data`; `_load_raw` keeps the record number; `_clean` matches the 29 raw values (all but the
   label) to `thyroid0387` records with a unique match, takes the date from the id's first six digits, drops the rows
   without a 1985 date, and declares `Temporal(on="request_date", splits=TemporalSplits(window=2, unit="months",
   cutoffs=("1985-08-01", "1985-10-01", "1985-12-01")))` (the last window ends with the data); the notes give the
   positives per window; record `required_split` Temporal, tag `Non-IID (Temporal)`; `dataset check`. Under either
   option the record gets the tags `Samples: Over Time` and `Time: Dated`. The date match is in the review's checks
   for this dataset (job 1365900).

   [^4a]: **SPLIT-32** (Should): how the data was collected is information for the split; the record's collection
     facts and, where one fits, the definition's use-case prototype with its `Time basis:` line.
   [^4b]: **TP-9** (Must): count the positives per test window of a temporal task; when the windows hold a handful or
     none, the scores are noise, and wider windows are the alternative to try (seismic_bumps: 0 to 5 per window).
     **SPLIT-16** (Must): do not fall back to a random split for a non-stationary sequence whose windows hold too few
     positives; here the sequence shows no change in the label share. **SPLIT-14** (Must): at least 3 windows, none
     training on less than half of the data.

   **Andrej (2026-11-11, discuss):** Can we measure and argue whether stationary relation is justified?

   **Answer (AI, 2026-11-11):**
   - The parent archive has the same label over 2.5 years. `thyroid0387` (same UCI folder: 9,172 Garvan records,
     August 1984 to January 1987, dated ids) gives each record the Garvan's report comment codes. The shipped
     "discordant" is exactly code R, "discordant assay results": all 58 matched positives, and no matched negative
     except one "D|R". So the relation can be measured across years, not only within 1985.
   - What the tag needs (SPLIT-32): the target and its relation to the features stay flat across periods, and a
     temporal split costs nothing.
   - Within the shipped year 1985 this holds: the share is flat (p = 0.82) and the monthly windows score within noise
     (see above).
   - Across 1984-1987 the relation carries over between years. Adding the quarter as a feature changes nothing.
   - The flatness is not perfect across years:
     - training on earlier quarters only costs LightGBM 0.008 (lower in 5 of 6 quarters);
     - the R share jumps to 4.4% in 1986Q3;
     - T3 is ordered less often from late 1985 on.
   - Side fact for issue 2: the label is the Garvan's own report comment, which answers "who assigned it". The
     `fit_reason` text is not changed.

   | Test on the archive (9,038 rows without duplicates, 197 R; untuned, ROC AUC; Slurm job 1377365) | Result |
   |---|---|
   | R share by quarter | 0.6% to 2.8%, but 4.4% in 1986Q3; chi-square p < 0.001, p = 0.60 without 1986Q3 |
   | Tests ordered | T3 measured in 80-87% of requests up to 1985Q3, 32-75% after |
   | Telling 1985 from 1986 by the features | AUC 0.72 (mostly TSH, T3): the case mix and the tests ordered move |
   | 1985 model on 1986 against a 1986 model of the same size | LightGBM 0.972 against 0.972; logistic regression 0.845 against 0.879 |
   | 1986 model on 1985 against a 1985 model | LightGBM 0.983 against 0.974; logistic regression 0.828 against 0.817 |
   | 1984 model on 1986 against a 1986 model | LightGBM 0.947 against 0.964; logistic regression 0.833 against 0.865 |
   | Quarter as a feature, 5-fold CV over all rows | 0.9917 with, 0.9916 without, 0.9914 with the quarter shuffled |
   | Quarters 1985Q3-1986Q4: earlier quarters only against random rows of the same size, same test rows, pooled | LightGBM 0.983 against 0.991 (seeds 0.990-0.993); logistic regression 0.854 against 0.871 (0.863-0.879) |

   | | Option | What it does | Pro | Con |
   |---|---|---|---|---|
   | A | Random split as `StationaryRelation` (implemented) | the `Time basis:` line also gives the label as archive code R and the archive measurements. It ends with what the split cannot test: a later year, and a change in labelling like 1986Q3 | flat within the shipped year; between years the relation carries over and the quarter adds nothing | across years the cost is small but not zero (0.008) |
   | B | Three windows by request date within 1985 | as in the table above | tests later requests | 15, 9 and 6 positives, so near noise |
   | C | Rebuild from the parent archive with a temporal split | label = code R. Train on 1984Q3-1985Q4 (61% of rows, 94 R); test on 1986H1, 1986Q3 and 1986Q4 plus January 1987 (24, 54 and 25 R) | 2.4 times the rows and 3.4 times the positives; tests the drift instead of assuming it | a new source file and build, and a different task; the 1986Q3 spike falls in one window; repeat patients cannot be traced (no patient id) |

   **Recommendation:** A. Within the year the file covers, the relation is flat. The cost across years is small,
   and the `Time basis:` line can state it. C would give a better-tested task, but it is a new dataset; if you want
   it, it gets its own issue. **Decision:** A, B or C?

   **Andrej (2026-11-12, discuss):** Do C and add it as a new dataset, then I decide on this

   **Answer (AI, 2026-11-12):**
   - Built as the new dataset `thyroid_discordant_archive` (folder and record; `dataset check` passes, one warning;
     not built).
   - Label code R of `thyroid0387`, the referral source dropped as here, TBG kept (constant in the dis file).
   - Windows of four months instead of option C's half-year, quarter and four months, which one declaration
     cannot express: they differ from option C's by 3 requests of January and June 1986, none discordant, and keep
     its positives.
   - Its Review issue 1 asks: keep it, this dataset, or both. The AI recommends the archive version, which
     contains 3,553 of this dataset's 3,711 rows.
   - This issue stays open until you decide there.

   | | thyroid_discordant | thyroid_discordant_archive |
   |---|---|---|
   | Requests, discordant | 3,711, 58 | 9,162, 197 |
   | Split | 10 x 3 random | February-May 1986, June-September 1986, October 1986-January 1987 |
   | Test positives | 19-20 per fold | 24, 54, 25 |
   | Untuned LightGBM / logistic regression, ROC AUC | 0.972 / 0.828 | 0.987 / 0.878 (windows 0.977-0.996 / 0.849-0.903) |

   **Andrej (2026-11-12, discuss):** Before finally deciding to drop this dataset, why was it even here if there is a
   larger version of the very same dataset?

   **Answer (AI, 2026-11-12):** it came in by lineage, never by a choice between versions: the curation sheet's row was
   UCI's whole "Thyroid Disease" entry, Lennart picked one of Quinlan's 1987 extracts from its zip, and the larger
   archive in the same zip carries the label only as comment code R, which nobody read as the same label until
   2026-11-11.

   | File in the UCI zip | At UCI | Requests | Label | On OpenML |
   |---|---|---|---|---|
   | `dis.data` + `dis.test` (this dataset) | left by Quinlan in 1987; file date 30 May 1989 | 2,800 + 972 = 3,772, of 1985 | "discordant", 58 | 40713 `dis` (PMLB import, 2017): this file; 40478 `thyroid-dis` (2016): a different file, see below |
   | `sick`, `allbp`, `allhyper`, `allhypo`, `allrep` | same | the same 3,772 requests and record numbers | one group of comments each | 38 `sick` (OpenML-CC18), 40707 `allbp`, 40708 `allrep` |
   | `thyroid0387.data` (the archive version) | added later; file date 16 Jul 1992 | 9,172, August 1984 to January 1987 | a string of comment codes per request; R = discordant | 47589, uploaded 2026-10-23, class = referral source, codes dropped |

   * **Quinlan's files are one sample labelled six ways:** dis, sick, allbp, allhyper, allhypo and allrep hold the same
     3,772 requests in the same order, values and record numbers identical (checked), each labelled for one group of
     comments: "In experiments with an earlier version of this archive, decision trees were derived for the most
     frequent classes of comments, namely ... discordant results (R)" (`thyroid0387.names`). The zip's `HELLO`: "left
     at the University of California at Irvine by Ross Quinlan during his visit in 1987"; thyroid0387 is "the latest
     version of an archive", added afterwards.
   * **How it came here:** the record's sheet row (collections `TabArena Reject`, `TabSTAR`) named the UCI entry, with
     links to copies of new-thyroid (replaced 2026-10-27). Lennart's screening note: hypothyroid first, "trivial to
     solve (almost 100 ROC AUC). Hence, we use dis instead." The BeyondArena notebook downloads `dis.data` and
     `dis.test` from UCI, not from OpenML.
   * **Why not the archive:** the same note reads thyroid0387 as "does not have a real target but just various
     diagnosis, seems like a scientific discovery task without a good target". Its label is no column: code R sits in
     a code string per request ("R", "D|R", "-") and is named only in the `.names` letter table. No benchmark carried
     it either: OpenML-CC18 and PMLB hold Quinlan's files, and OpenML got the archive only on 2026-10-23, without the
     codes.
   * **OpenML's `thyroid-dis` (40478) has no discordant label:** it is byte-identical to its `allbp`, `allhyper`,
     `allhypo` and `allrep` uploads (40474 to 40477), and its 5-valued class has the counts of `dis.data`'s referral
     source (1,632, 771, 275, 91, 31).
   * **The earlier reviews judged dis alone:** the `Trivial` test (2026-10-21) and the reviews of 2026-10-27 and
     2026-11-04 never compared it with the archive; the match (3,553 of 3,711 rows, all 58 positives code R) was first
     measured on 2026-11-11 for this issue.
   * **So:** the smaller file has nothing of its own over the archive version; it was only reviewed and built first.

   | | Option | What it does | Pro | Con |
   |---|---|---|---|---|
   | a | Retire as `Duplicate` (the archive version's issue 1, B) | record `No (Retired)` with `Duplicate`, priority removed, a CC line naming thyroid_discordant_archive; the folder leaves in a retirement PR; issues 2 and 4 closed as superseded | one dataset per task[^4c]; the archive is the source's fuller version and ships | this dataset's review and build are set aside |
   | b | Keep it next to the archive version | both ship | nothing removed | the same task and 3,553 requests twice in the benchmark |

   **Recommendation:** a: this file was never chosen over the archive, only reached first. **Decision:** retire as
   `Duplicate` (a), or keep (b)?

   [^4c]: **PROV-6** (Must): different versions or cuts of one underlying dataset are duplicates when neither adds a
     distinct task. **PROV-4** (Must): a dataset enters once.

   **Andrej (2026-11-12, discuss):** Reply (a): Retire as Duplicate (the archive version's issue 1, B)

   **Resolved (2026-11-12, Andrej):** a (verdict `dont`): retired as `Duplicate` of thyroid_discordant_archive, the
   copy that stays and ships. Record `suggestion` `No (Retired)` with the marker `Duplicate`, priority removed, a CC
   line naming the archive version; `data_foundry_status` (`DF: Yes`, `BeyondArena`, `WIP (DF)`) and the claim stay.
   The folder and `v2_path` stay too: they leave in a retirement PR. Issues 2 and 3 were already resolved.

## Reference

@article{quinlan1987simplifying,
  title={Simplifying decision trees},
  author={Quinlan, J. Ross},
  journal={International journal of man-machine studies},
  volume={27},
  number={3},
  pages={221--234},
  year={1987},
  publisher={Elsevier}
}
@inproceedings{quinlan1987inductive,
  title={Inductive knowledge acquisition: a case study},
  author={Quinlan, John Ross and Compton, Paul J and Horn, KA and Lazarus, Leslie},
  booktitle={Proceedings of the Second Australian Conference on Applications of expert systems},
  pages={137--156},
  year={1987}
}
