---
unique_name: ljubljana_breast_cancer
name: Ljubljana Breast Cancer \
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: No (Retired)
decision_markers:
- Trivial
- Outdated
tags:
- Tiny Data
- 'Samples: Over Time'
- 'Time: Lost'
collections:
- New (BeyondArena)
- TabSTAR
original_source: UCI
year: '1988'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/faysalmiah1721758/breast-cancer-data
- https://github.com/jbrownlee/Datasets/blob/master/breast-cancer.names
- https://doi.org/10.24432/C51P4M
- https://www.openml.org/d/13
notebook_path: datasets/beyond_iid/new_iid/ljubljana_breast_cancer/ljubljana_breast_cancer.ipynb
source_row: 769
type_adapter_id: curation-record-v1
---

## Comments

looks good

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Every 1986-1988 paper on the data (Michalski et al., Clark & Niblett, Cestnik et al.) reports accuracy only, without costs or a threshold; 30% recurrence on 286 rows. Original rejected: accuracy. roc_auc is the binary fallback.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): ordinal scales shipped as numbers, left as numbers for the curator's review: `tumor-size`, `inv-nodes`, `deg-malig`.

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 3 ordinal scales shipped as numbers are ordered categories (point 3).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `metabric_breast_cancer_clinical` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 1 scores are numbers (deg-malig); age, tumour size and nodes are ordered categories of their bands, not the bands' midpoints.

CC (2026-11-10, Andrej): retired (`No (Retired)`, `Trivial`, `Outdated`): an untrained 3-item score does as well as every model, so nothing learnable is left beyond what the field already writes down.
- **The score ties every method:** one point each for malignancy grade 3, more than 2 involved nodes and a tumour through a node's capsule, nothing fitted: ROC AUC 0.710 against 0.717 for TabPFN 3.5 (the score at least as good on 28 of 60 folds), 0.710 for a random forest (29 of 60) and 0.683 for logistic regression (20 x 3 folds, seed 4267).
- **Why the real signal does not keep it:** the outcome is real and well above chance, but the methods learn nothing measurably better than the three standard prognostic factors (grade, nodal status, capsular breach); the 2-node cut-off was set in our review of 2026-10-15 without a recorded source.
- **Outdated:** 1980s clinical bands without the hormone-receptor status prognosis uses today; better data for the task is `metabric_breast_cancer_clinical`.
Markers `Trivial` and `Outdated` added, `v2_path` cleared, folder removed. Evidence: `~/claude_jobs/lbc_review/res.csv`.

CC (2026-11-11, Andrej): the Review marks of 2026-11-11 are written into their issues. They repeat the decisions of 2026-11-10, so nothing changed: issue 6, B, is the retirement already in force here (`No (Retired)`, `Trivial` and `Outdated`, `v2_path` cleared, folder gone), and issues 1 to 4 (keep with `Outdated`, forced from temporal, prediction point after the treatment decision, `Target: Varying Delay`) stay unapplied, as the dataset has no definition to change; issue 5 is `ok`, the repeated women kept.

## Review

**Outcome:** added. Recurrence of breast cancer for 286 patients of the Institute of Oncology in Ljubljana, as
Zwitter and Soklic donated them to UCI in 1988; the AI recommends shipping it with the record marker `Outdated`
(issue 1, option B). Reviewed without a panel, from the gathered evidence: the record, the earlier experiments of
2026-10-15 and model runs on the shipped data; the first version of this file (2026-10-27) migrated the
folder's open question from Andrej's review. Validity: a real outcome from a documented clinic; the recurrence has no
stated time window and radiotherapy may postdate the estimate, both named in `fit_reason` (fit approximate). Value: an
untrained 3-item score (ROC AUC 0.710) nearly ties TabPFN 3.5 (0.717), and a naive Bayes model on five columns ranks
first of 41 on the shipped splits; the benchmark methods still spread from 0.658 to 0.721, and the best single feature
(grade, 0.677) stays below the methods, so the test for `Trivial` is not met. Quality: 14 exact duplicate rows and 6
rows that share their features with a row of the other class, kept as naturally occurring; the bands of age, tumour
size and node count are ordered categories since 2026-11-01 (Lennart). Weighed: a real outcome with clear signal and
a documented clinic +, a rule of thumb as good as the models and a 1980s feature set -, better data found for the
task (not a reason by itself) -.

**Main points:** Retired (2026-11-10) with `Trivial` and `Outdated`: an untrained 3-item score matches every method
(issue 6, resolved; PR #57). The other issues are moot.

**Record judgment:** the record's "looks good" holds for validity. It does not mention the near-tie with a simple score
or the missing time window, which `fit_reason` now names. Its reference is "? UCI": it can take the definition's
citation (Zwitter and Soklic, Breast Cancer, UCI Machine Learning Repository, 1988, https://doi.org/10.24432/C51P4M),
a change that needs no mark. Since 2026-10-31 the record notes better data for the same task,
`metabric_breast_cancer_clinical` (screened `TBD -> Yes`, not added).

**Issues for Andrej:**

1. **Keep the dataset, although an untrained 3-item score does as well as the best models?**

   * **Problem:**
     - Andrej disputes Lennart's keep ("looks good"): a score that adds one point each for malignancy grade 3, more
       than 2 affected lymph nodes and a tumour that broke through a node's capsule, with nothing fitted, reaches ROC
       AUC 0.710 against 0.717 for TabPFN 3.5.
     - The test for `Trivial` asks for one raw feature that matches the methods fold by fold, and the best one, grade,
       reaches only 0.677, so the rules keep the dataset[^1a].
     - Keep it, with `Outdated` for its 1980s feature set, or retire it as `Trivial` by reading the marker as "a
       simple rule matches the best methods"[^1b]?
   * **Background:**
     - The features are 1980s clinical bands (age, tumour size and node count in ranges), menopause, the breast and
       its quadrant and whether radiotherapy was given, without the hormone-receptor status (whether the tumour grows
       on oestrogen or progesterone) that prognosis uses today.
     - The three items of the score are the natural core of breast cancer prognosis, which the test for `Trivial`
       expects to dominate[^1a].
     - A small but real signal is no reason to retire[^1c], and 0.71 is far from chance (0.5).
     - Better data for the same task was found on 2026-10-31 (`metabric_breast_cancer_clinical`, a later and larger
       cohort with receptor status); a valid task does not have to give way to a better version[^1d].
   * **Effect on the task:** the benchmark ranks methods on a task where a rule of thumb is as good as any model, so
     most differences between methods are noise; the best model's log loss is only 9.5% below that of the class
     shares (30% recurrence).
   * **Experiments:**
     - Earlier own run on the UCI file, the shipped regime (20 repeats of 3 folds, seed 4267, 60 splits): the
       untrained score 0.710; TabPFN 3.5 0.717, ahead of the score on 53% of the folds; random forest 0.710; logistic
       regression on the three columns 0.705, on all columns one-hot 0.683; grade alone 0.677. Log loss below the
       class shares: TabPFN 3.5 9.5%, logistic regression on the three columns 8.6%. Accuracy 0.734 against 0.703
       for always predicting no recurrence.
     - Cached BeyondArena results (34 folds, 29 configurations): a comparison corrected for the overlap of training
       sets across repeated folds (the Nadeau-Bengio correction) leaves 24 of the other 28 configurations level with
       the best (TabDPT, 0.721); the repository's uncorrected test leaves 2. The best method's ROC AUC per fold runs
       from 0.627 to 0.824. Tuning makes methods worse (CatBoost 0.705 by default, 0.687 tuned and ensembled).
     - Model runs on the shipped data (its 60 splits, 40 benchmark methods; bands as midpoints there, ordered
       categories in v0.2, the same order): the benchmark methods run from ROC AUC 0.658 (XGBoost, default) to 0.721
       (TabDPT), median 0.695, TabPFN 2.6 0.716, logistic regression tuned 0.690. A naive Bayes model on tumour size,
       node count, grade, capsule and radiotherapy, the four other columns left out, reaches 0.729 (0.733 with
       pairwise products), first of 41 and within one standard error (0.008) of the best benchmark method.
   * **Consistency:**
     - heart_disease_cleveland was kept on 2026-10-06 under the small-signal rule ("a real task with clear signal;
       little room between methods is the noise of a small task"), and the same corrected comparison leaves 28 of 29
       configurations tied there[^1e]. It was retired on 2026-10-21 as a duplicate of the pooled `heart_disease`,
       not for this reason, so the earlier request for "the same answer for heart_disease_cleveland" no longer has
       an object.
     - The sibling lymphography (the same 1988 Ljubljana collection) is `No` with `Outdated` and `Trivial`.
   * **Sources:** Nadeau C, Bengio Y. Inference for the generalization error. Machine Learning 2003;52(3):239-281,
     https://doi.org/10.1023/A:1024068626366; the UCI page, https://doi.org/10.24432/C51P4M.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as defined (implemented) | 286 patients and nine features; no marker | a real outcome with clear signal; meets the rules | the dated feature set is not flagged |
     | B | Keep, add `Outdated` | the record gets the marker; data unchanged | flags the 1980s bands without receptor status; no cost to the data | most differences between methods stay noise |
     | C | Retire with `Trivial` | record `No (Retired)`; folder removed | no task where a rule of thumb ties the models | widens the test for `Trivial` from one feature to a simple rule; a real outcome task leaves |

   * **Recommendation:** B: the single-feature test fails, the signal is real, and the three items are the expected
     core of the task; the marker names the dated features. **Decision:** keep as is (A), keep with `Outdated` (B),
     or retire (C)?

   **Notes for the AI:** on B, add `Outdated` to `decision_markers`, a `CC (<date>, Andrej):` line and `Andrej` to
   `checked_by`. On C, `suggestion: No (Retired)`, markers `Trivial` and `Outdated`, remove the folder and clear
   `v2_path`; TP-4 is a Must, so the decision amends it ("a simple untrained rule of the field matches the methods")
   in `task_probes.md` with this case, and the selection.md marker row stays as it reads.

   [^1a]: **TP-4** (Must): `Trivial` needs proof. Read what the dominant feature means first: the natural core of a
     task is expected to dominate. Then the raw feature, chosen on each split's training side, has to match or beat
     the methods fold by fold.
   [^1b]: selection.md, marker table: `Trivial` is "one feature or a simple rule matches the best methods, or the
     task is solved perfectly".
   [^1c]: **TP-2** (Should): a small but real signal is no reason to retire; retire, fix or keep a task for a
     concrete reason found in the task itself.
   [^1d]: **TP-6** (Must): keep two questions apart, is the task valid and is it the best version; a valid task
     stays.
   [^1e]: **EV-9** (Should): calibrate a statistic before concluding from it, against the same statistic measured
     the same way on a reference.

   **Andrej (2026-11-11, change):** Option B: Keep, add Outdated.

   **Resolved (2026-11-10, Andrej):** superseded by issue 6: retired with `Trivial` and `Outdated` (your mark B here, keep with `Outdated`, gave way to the retirement).

2. **Time basis: tag the random split as forced from temporal?**

   * **Problem:**
     - Women were operated on at one clinic over a period the source never states (before 1986), and recurrence was recorded later with no stated window; the file keeps no date and is sorted by class (201 without, then 85 with recurrence), so the time is lost.
     - The record carries `Samples: Over Time` and `Time: Lost` but no target fact (issue 4); the definition splits at random and names no time basis.
     - Recurrence follows the treatment and follow-up of the period, and the estimate is used on later patients, so the five questions give the forced tag[^2a].
   * **Background:**
     - No prototype fits: the patients share no prediction moment, and recurrence is a later outcome, not a present
       state read through a fixed relation.
     - If the label is the status at the time of the extract, patients operated on late had less time to recur, a
       period effect inside the file that a random split spreads over both sides; without dates it cannot be tested.
     - The leak test across the split: 14 exact duplicate rows, kept as distinct patients with the same bands; no id;
       no order but the class. Radiotherapy, decided around the prediction point, is issue 3.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No time basis (implemented) | as now | nothing to write | `dataset check` notes a split that is not temporal without a basis; the missing dates not stated as a forced split |
     | B | Forced from temporal | `ForcedIIDFromTemporal` and a `Time basis:` line | says that later patients are the use and the dates are missing | none found |
     | C | Stationary relation | `StationaryRelation` and a line arguing it | no forced tag | recurrence is a later outcome under the period's treatment, and no date exists to show the relation holds |

   * **Recommendation:** B. **Decision:** A, B or C?

   **Notes for the AI:** once PR #50 is in this working copy, on B: `data_tags = ("ForcedIIDFromTemporal",)` and in
   `curation_comments` the bullet `- Time basis: ForcedIIDFromTemporal: women operated on at the Institute of
   Oncology, Ljubljana, before 1986 (period not stated), recurrence recorded later with no stated window; the estimate
   is used on later patients. The file has no date and is sorted by class (Time: Lost). Leak test across the split: 14
   exact duplicate rows, kept as distinct patients; whether follow-up length differs by period cannot be tested.
   Operation and follow-up dates would allow a split by time.`; the `split` sentence names the forced split;
   `dataset check`.

   [^2a]: **SPLIT-32** (Should): the record's collection facts and the five questions; samples over time whose period
     moves the target, with the time lost, get a forced split. **SPLIT-8** (Must): the closest regime, tagged as forced
     from temporal, after a leak test across the split.

   **Andrej (2026-11-11, change):** Option B: Forced from temporal.

   **Resolved (2026-11-10, Andrej):** moot, the dataset is retired (issue 6); your mark B (forced from temporal) is not applied.

3. **Radiotherapy given (`irradiat`): keep it with the prediction point after the treatment decision, or drop it?**

   * **Problem:**
     - The use case predicts after surgery "to plan follow-up and further treatment", and radiotherapy is part of that treatment, so as written `irradiat` is decided at or after the prediction point.
     - In the file radiotherapy follows the involved nodes (given to 14% of patients with 0-2 nodes and 47-100% of those with more), and irradiated patients recur at 46% against 25%, an odds ratio of 2.5 that falls to 1.5-1.7 once node count, grade and capsule are held fixed.
     - Keep the column and move the prediction point after the treatment decision, or drop it?
   * **Background:**
     - `fit_reason` already says that whether radiotherapy is known "depends on when the estimate is made".
     - A radiotherapy given because the cancer came back would tie the column to the outcome whatever the nodes; the
       modest link left within node, grade and capsule groups fits treatment by indication. The source does not say
       when the column was recorded.
     - In the earlier model runs a naive Bayes model on five columns, radiotherapy among them, scored ROC AUC 0.729,
       first of 41 (issue 1).
   * **Experiments:** on the UCI file, no model: recurrence by radiotherapy within groups of node count (0-2, 3 or
     more) and grade; Mantel-Haenszel odds ratio 1.54 (nodes and grade), 1.71 (with capsule), against 2.54 overall.
     Example groups: 0-2 nodes and grade 2, 19% recurrence irradiated (16 patients) against 17% not (82); 3 or more
     nodes and grade 3, 74% (19) against 72% (18).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as now (implemented) | the column stays; `fit_reason` leaves the timing open | no change | the use case as written plans the treatment the column records |
     | B | Keep, prediction point after the treatment decision | `use_case` reworded to the estimate once surgery and radiotherapy are decided, to plan follow-up; `fit_reason` states the measured link | a real decision (follow-up after primary treatment) at which the column is known; the data show indication, not outcome | the estimate no longer informs the radiotherapy decision itself |
     | C | Drop the column | `irradiat` dropped in `_clean` | the estimate before any treatment decision | loses a known input of a real follow-up decision; the earlier best model used it |

   * **Recommendation:** B, the mildest fix: the column is known once the treatment is planned, and the link left
     within node and grade groups is that of an indication, not of the outcome[^3a]. **Decision:** A, B or C?

   **Notes for the AI:** on B, `use_case`: "For example, once surgery and the decision on radiotherapy are made, an
   oncologist estimates the chance that the cancer recurs, to plan follow-up."; in `fit_reason` replace the
   radiotherapy sentence with "Radiotherapy is known at that point; in the file it follows the involved nodes (odds
   ratio 2.5 overall, 1.5-1.7 within groups of node count, grade and capsule)."; `dataset check`. On C: drop
   `irradiat` in `_clean`, `known` and `changes` updated, `dataset check`. A `CC (<date>, Andrej):` line in the record
   either way.

   [^3a]: **USE-3** (Must): name the prediction point; a value that did not exist at it is a leak. **LEAK-37** (Must):
     an input the actor knows at the prediction point is not a leak. **LEAK-7** (Should): the smallest fix that keeps
     a valid signal beats dropping the column.

   **Andrej (2026-11-11, change):** Option B: Keep, prediction point after the treatment decision.

   **Resolved (2026-11-10, Andrej):** moot, the dataset is retired (issue 6); your mark B (keep, prediction point after the treatment decision) is not applied.

4. **Correct the record's collection facts: add the target fact?**

   * **Problem:**
     - The record carries `Samples: Over Time` and `Time: Lost` but no target fact, which the rule leaves out only when the target exists with the features.
     - Recurrence comes after surgery, but the source states no window: a fixed window would be `Target: Later`, a status read at the extract after follow-ups of different length `Target: Varying Delay`.
     - Add `Target: Varying Delay`, the reading that claims no window the source does not give?
   * **Background:** the UCI names file gives the classes "no-recurrence-events" and "recurrence-events" and no
     window (https://doi.org/10.24432/C51P4M); the definition's `predicted` says "the source states no time window".
     The 1986 papers on the file may state one; they were not checked here[^4a].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No target fact (implemented) | as now | no edit | reads as a target that exists with the features |
     | B | `Target: Varying Delay` | the tag added | recurrence after follow-ups that differ per patient, the reading the source allows | wrong if the 1980s papers fix a window |
     | C | `Target: Later` | the tag added | right if a fixed window exists | claims a window the source does not state |

   * **Recommendation:** B. **Decision:** A, B or C?

   **Notes for the AI:** on B or C, add the tag to the record's `tags`; a `CC (<date>, Andrej):` line and `Andrej` in
   `checked_by`.

   [^4a]: **SPLIT-32** (Should): `Target: Later` after the features at one shared date or after a fixed window;
     `Target: Varying Delay` after a delay that differs between samples (a follow-up); no tag when the target exists
     with the features.

   **Andrej (2026-11-11, change):** Option B: Target: Varying Delay.

   **Resolved (2026-11-10, Andrej):** moot, the dataset is retired (issue 6); your mark B (`Target: Varying Delay`) is not applied.

5. **Keep the repeated patients, as distinct women with the same bands?**

   * **Problem:**
     - 20 of the 286 patients (7%) repeat another patient's nine values exactly, 14 of them with the same outcome (the duplicates the notes keep), so under a random split 9% of test patients have an exact copy in training.
     - The new rules for repeats of a unit the data does not record set the verdict by three tests (is the link above chance, does the label travel with it, is there an order), and all three read these as distinct patients with the same coarse bands: the natural verdict, which keeps the random split[^5a].
     - Keep the copies as now, or drop the 14 same-outcome copies?
   * **Experiments** (2026-11-06, the 286 shipped rows):
     - **Link at chance:** the nine values are bands and yes/no answers that hang together; a null that keeps each
       class's strongest links between columns (a tree of pairwise dependences, 200 draws) gives 26 repeated rows
       (95% 16-36) against 20 observed. Shuffling each column within its class, which breaks those links, gives 8.
     - **The label does not travel:** copies share the outcome in 67% of 21 pairs, against 58% from the class
       shares, 73% for patients who differ in one value, and 81% that their bands predict; 6 of the 19 groups hold
       both outcomes.
     - **No order:** no date or id, and the file is sorted by class.
     - **Overlap:** random 3-fold splits (20 repeats): 8.7% of test patients have an exact copy in training, and
       the copies' majority outcome is right for 68% of them, about the class share.
   * **Consistency:** follows sepsis_survival_minimal_clinical_records and
     ai4d_lab_tanzania_tourism_classification_challenge, which keep repeated coarse profiles of distinct people[^5b];
     the 6 groups with both outcomes are an ambiguity the task has[^5c].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as is (implemented) | 286 patients, random split; the notes gain the verdict and the 9% overlap | the copies are distinct patients, as a clinic meets them; they occur as often as the bands' links predict | none found |
     | B | Drop the same-outcome copies | 272 patients (10 without and 4 with recurrence dropped); recurrence 29.7% to 29.8% | no identical row with one outcome on both sides | drops real patients on a link the tests find to be chance |

   * **Recommendation:** A: the copies are as frequent as the bands' own links predict and share the outcome less
     than their bands would, so they are distinct patients. **Decision:** keep (A) or drop the copies (B)?

   **Notes for the AI:** on A, once PR #62 is in, replace the bullet "We keep duplicates as they seem naturally
   occurring." with "- Entity leakage, natural (2026-11-06): 20 of 286 patients repeat another's nine values (14 with
   the same outcome); a null keeping the columns' links gives as many (26, 95% 16-36), copies share the outcome less
   than patients one value apart (67% against 73%), and the file has no order but the class, so they are distinct
   patients with the same bands. Under random 3-fold splits 8.7% of test patients have an exact copy in training."; no
   data change, no rebuild. On B, `df = df.drop_duplicates()` in `_clean`, `row`, `changes` and the notes updated, a
   `CC (<date>, Andrej):` line in the record. Evidence: `~/claude_jobs/entity_review/ljubljana_breast_cancer/`
   (`dupcheck.log`, `structure_null.log`, `drop_effect.log`; scripts one level up).

   [^5a]: **LEAK-41** (Must, draft PR #62): repeats of a unit the data does not record get one verdict; natural when
     the look-alikes are distinct units: the random split stays and the notes give the share of test rows with a
     look-alike in training. **LEAK-42** (Should, draft PR #62): three tests set the verdict: matches against a chance
     rate that keeps the data's structure, label agreement against what the shared features predict, and an order.
   [^5b]: **LEAK-18** (Should): few features and plausible repeats are natural: keep them and say so
     (sepsis_survival_minimal_clinical_records keeps 110,204 rows over 975 distinct feature rows;
     ai4d_lab_tanzania_tourism_classification_challenge its 965 exact copies, Lennart, 2026-11-05).
   [^5c]: **LEAK-20** (Should): feature vectors that occur with both labels are dropped, unless they are genuine
     label ambiguity the task has.

   **Resolved (2026-11-10, Andrej):** kept as distinct women (ok); moot with the retirement (issue 6).

6. **Does your keep with `Outdated` (issue 1, B) stand, now that a rule matching the models makes a dataset a candidate to drop?**

   * **Problem:**
     - The untrained 3-item score (one point each for malignancy grade 3, more than 2 involved nodes and a tumour that
       broke through a node's capsule) ties every method fold by fold: 0.710 against 0.717 for TabPFN 3.5 and 0.710
       for a random forest.
     - Since 2026-11-10 a rule not fitted on the data that matches the methods makes the dataset a candidate to drop,
       and the curator decides[^6a]; your mark on issue 1 was given when only a single raw feature counted.
     - Keep with `Outdated`, or retire with `Trivial`?
   * **Background:**
     - Grade, nodal status and capsular breach are the field's standard prognostic factors; the cut-off at 2 nodes
       was set in the review of 2026-10-15, which does not record whether it came from the field or from the rows.
     - Your principle of 2026-11-10: if nothing learnable from the data beats a rule not fitted on it, the data cannot
       be used for prediction. Here the methods learn nothing measurably better.
   * **Experiments:** the UCI file in the shipped regime (20 x 3 folds, seed 4267, 60 splits;
     `~/claude_jobs/lbc_review/res.csv`):

     | Method | ROC AUC | Score minus method (± SE) | Folds the score is at least as good |
     |---|---|---|---|
     | Untrained 3-item score | 0.710 | | |
     | TabPFN 3.5 | 0.717 | -0.006 ± 0.004 | 28 of 60 |
     | Random forest | 0.710 | -0.000 ± 0.003 | 29 of 60 |
     | Logistic regression, all columns one-hot | 0.683 | +0.027 ± 0.004 | 44 of 60 |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep with `Outdated`, as marked on issue 1 (implemented) | as marked | a real outcome with a real signal | no method learns more than a three-item score |
     | B | Retire with `Trivial` and `Outdated` | `No (Retired)`, folder removed | follows your principle; the rule ties every method | the 2-node cut-off may have been read off the rows |

   * **Recommendation:** B: the score matches the best methods within one standard error and beats logistic
     regression; nothing learnable is left beyond it. **Decision:** A or B?

   **Notes for the AI:** on B, `suggestion: No (Retired)`, markers `Trivial` and `Outdated`, a `CC (<date>, Andrej):`
   line with the table, the folder removed and `v2_path` cleared, the CHANGELOG entry, a TP-4 case row; issue 1's
   mark is then superseded. On A, issue 1's mark is applied as given.

   [^6a]: **TP-4** (Must, amended 2026-11-10 in PR #57): a raw feature chosen on each split's training side, or a
     rule not fitted on these data (a published formula, the field's definition, a textbook or clinical score), is
     tested against the methods fold by fold; one that beats them proves `Trivial`, one that matches them makes the
     dataset a candidate to drop, and the curator decides.

   **Andrej (2026-11-11, change):** Option B: Retire with Trivial and Outdated.

   **Resolved (2026-11-10, Andrej):** retire with `Trivial` and `Outdated` (B). In PR #57 (commit 9ae47c6a): the record `No (Retired)` with both markers, a CC line and `Andrej` in `checked_by`, `v2_path` cleared, the folder removed, a TP-4 case row and the CHANGELOG entry.

## Reference

? UCI
