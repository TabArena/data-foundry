---
unique_name: hr_analytics
name: HR_Analytics_Job_Change_of_Data_Scientists / hr_analytics
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
- 'Time: Lost'
- 'Target: Unknown'
original_source: Other
year: '2018'
required_split:
- Random (IID)
source_links:
- https://www.kaggle.com/datasets/arashnic/hr-analytics-job-change-of-data-scientists
- https://www.analyticsvidhya.com/datahack/contest/the-data-supremacy
notebook_path: datasets/beyond_iid/old_iid/hr_analytics/hr_analytics.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/hr_analytics/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Task: predict the probability of a candidate to look for a new job or will work for the company, as well as interpreting affected factors on employee decision

Potential issue: spatial inforamtio nbut correctly preprocssed

Lennart: no objections, spatial information can be likely ignored

Andrej: Not sure how exactly the target was obtained

**Assessment (AI, 2026-10-14), the aug file:** The Kaggle card (arashnic, files of 2020-12-07) names Analytics Vidhya's JanataHack: HR Analytics (2020-05-08) as its source; that hackathon reused the train and test files of Student DataFest 2018: The Data Supremacy (2018-07-05, same train file, byte-identical test file), so the data first appeared there (18,359 labelled rows, 13.2% positive; 15,021 unlabelled test rows; enrollee_id 1-33,380). All 21,287 Kaggle rows are hackathon rows with identical features. `aug_train.csv` holds 16,535 rows of the train file with their labels and 2,623 rows of the unlabelled test file, every one labelled 1, so 2,623 of its 4,777 positives come from rows whose labels the hackathon never published; `aug_test.csv` holds 1,824 train-file rows and 305 test-file rows. The card does not explain "aug". The added labels do not behave like real ones: 89% of city_21's test rows were added as positive while city_21 has 27% positives in the train file (city_11: 89% vs 24%), and a gradient-boosting model trained on the hackathon train file separates the added rows from the other test rows with ROC AUC 0.93, while it separates real positives from negatives with 0.64 (5-fold, out of fold). A rule or model seems to have picked them (most sit in cities of low development index). With them, 5-fold CV ROC AUC on `aug_train.csv` is 0.80; on its rows from the train file alone it is 0.66. The hackathon's own train file (https://datahack-prod.s3.amazonaws.com/train_file/train_jqd04QH.csv) is public and would avoid the added rows.

CC (2026-10-14, Lennart): Build from the hackathon's public train file (18,359 rows, labels from the source); source Other, the contest page, year 2018.

CC (2026-10-14, Lennart): Task probes `no_spread` accepted: the real labels give ROC AUC 0.62-0.63 for every model family (LightGBM +0.012 over random forest, paired SE 0.006), a real signal with a low ceiling.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — AUC-ROC (https://www.analyticsvidhya.com/datahack/contest/the-data-supremacy (also https://www.analyticsvidhya.com/datahack/contest/janatahack-hr-analytics)).

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 3 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `education_level`, `experience`, `company_size` (the README lists their levels); left unordered: `last_new_job` (a level outside the scale is a state of its own).

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 1 columns with a state outside the scale ordered, the state placed by the rule.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): counts with a cut end are numbers: experience, last_new_job.

CC (2026-11-01, Lennart): counts with a cut end stay ordered categories of the source's levels, the cut end a level of its own (CLEAN-14): the lossless form, chosen from the context rather than by model runs; the same day's numbers with censoring flags are reverted.

CC (2026-11-11, Andrej): the review page's marks of 2026-11-11 applied (review issues 1 to 4).
- Issue 1 (`ok`): kept; the label's unstated source and timing stay named in the approximate fit.
- Issue 2 ("Agree.", option C): the random split is tagged `ForcedIIDFromTemporal` with a `Time basis:` bullet: enrollees signed up over a period the hackathon does not state, the release has no date, and `enrollee_id` is not shown to follow sign-up (training hours flat along it; windows in its order score as random folds, ROC AUC 0.645 against 0.646).
- Issue 3 ("Option B: Drop training_hours"): the column is dropped in `_clean`; it is the training completed after sign-up, the stated prediction point, and it carries nothing (alone ROC AUC 0.495; LightGBM 0.644 without it against 0.642 with it). 11 features.
- Issue 4 ("Option B: Time: Lost"): the record's `tags` carry `Time: Lost` in place of `Time: Dated`.
- `dataset check`: 0 errors, 2 warnings, both raised by dropping the hours and left open rather than accepted: 1,988 rows (10.8%) now repeat an earlier row and 319 (1.7%) share their features with a row of the other label; the curation notes say they are different enrollees with the same coarse answers.

## Review

**Outcome:** added. The AI recommends keeping it as defined, but the decision is Andrej's open question on the label
(issue 1). Reviewed on 2026-11-04 without a panel, from the evidence already gathered (the record, the source check
and rebuild of 2026-10-14, a model run on the TabArena v0.1 task of the same source). The data are the train
file of Analytics Vidhya's hackathon "Student DataFest 2018: The Data Supremacy" (July 2018): 18,359 people enrolled
in a data-science institute's trainings, with city and its development index, gender, education, field, enrolment,
experience, current employer's size and type, years since the last job change and training hours completed; the
target is whether the enrollee is looking for a job change (13.2%). v0.2 uses the hackathon's own file instead of
Kaggle's 2020 copy, which added 2,623 rows of the unlabelled test file, all labelled positive, that a model told apart
from real rows with ROC AUC 0.93. Validity: the use case is plausible (the institute puts real job-seekers in touch
with hiring clients), but how and when the label was recorded is not stated (issue 1). Value: on the real labels every
untuned model family scores ROC AUC 0.62 to 0.63, a real but weak signal with almost no spread, kept by Lennart on
2026-10-14; the benchmark spread was measured on Kaggle's copy with the made-up positives and does not carry over.
Quality: 45 repeated rows and 17 feature rows with both labels, different enrollees, kept. Weighed: real rows from a
named hackathon +, the fake positives removed +, a label of unknown origin and timing -, a low ceiling with no spread
between untuned models -, no licence stated -.

**Main points:** Kept, with the label's gap in the fit (issue 1); the random split tagged forced from temporal (issue
2); `training_hours` dropped (issue 3); the record's `Time: Lost` (issue 4). All resolved 2026-11-09.

**Record judgment:** keep, as the rules stand. The source trace and the rebuild (2026-10-14, Lennart) are in the
definition and are sound: the hackathon's own train file is public, and the same file ran again in JanataHack (2020). The weak
signal is accepted as a real one with a low ceiling (the no-spread case of the task-probe rules). What is left is
Andrej's note from the first triage, "Not sure how exactly the target was obtained", which no later step answered;
issue 1 puts it as a decision. Neither contest page states a licence (a note only). The record has no `domain` or
`problem_type` field; the definition's values (business & marketing, binary classification) can be filled in without
a mark.

**Issues for Andrej:**

1. **Keep a label whose source and timing the hackathon never states?**

   * **Problem:**
     - The target "looking for a job change" comes from a 2018 hackathon that never says how or when it was recorded: an answer on the sign-up form, a later survey, or an observed move.
     - If it is the enrollee's own answer given with the other fields, nobody would need to predict it; if it was recorded after the training, the use case holds.
     - Keep it with the gap stated as an approximate fit, as now, or retire the dataset?
   * **Background:** the contest asks for "the probability of an enrollee to look for a new job" from "the current
     credentials/demographics/experience" (quoted in the definition); the institute, place and period are not named.
     `training_hours`, the training completed, is only known some time after sign-up, which hints that the label was
     read later, but nothing says so. A label from a named publication whose construction is undocumented may ship
     with an approximate fit and a note[^1a]; a label the respondent already knows, asked together with the features,
     is predicted by nobody[^1b].
   * **Experiments:** on the hackathon's file (record, 2026-10-14): ROC AUC LightGBM 0.625, linear 0.622, random
     forest 0.619 (LightGBM 0.012 above the forest, paired standard error 0.006). Kaggle's copy reached 0.80 only
     through the 2,623 added positives (0.66 on its rows from the train file).
   * **Consistency:** follows the datasets kept with an undocumented label and an approximate fit (mobile_churn: no
     churn rule stated). It differs from dataorg_financial_health_prediction_challenge, retired on 2026-10-22 because
     nothing was known about its target: here the target's meaning is stated, only its recording is not.
   * **Unknown:** the hackathon's problem statement tab (closed since the contest ended) or the organiser could say
     how the label was collected.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep, approximate fit (implemented) | no change; `fit_reason` names the unknown source and timing | real rows, a plausible decision, the rules' treatment of an undocumented label | a label that may be a sign-up answer; a weak signal with no spread |
     | B | Retire | record `No (Retired)`, `No Good Target / Scientific Discovery` | no task of unknown origin in the benchmark | loses a real if weak task with mixed categorical columns |

   * **Recommendation:** A: the meaning of the target is stated, training hours point to a label read after the
     training, and the rules ship such a label with the gap named; re-check the spread with the first tuned run.
     **Decision:** keep (A) or retire (B)?

   **Notes for the AI:** on A, add a `CC (2026-11-04, Andrej):` line closing his triage note; on B, set the record to
   `No (Retired)` with `No Good Target / Scientific Discovery`, remove the folder and clear `v2_path`, with a CHANGELOG
   entry.

   [^1a]: **USE-5** (Must): a label from a named publication whose construction is undocumented and cannot be checked
     may ship with `fit="approximate"` and a note naming the gap, decided case by case.
   [^1b]: **SEL-7** (Must): a label the respondent already knows, asked in the same interview as the features, is
     predicted by nobody.

   **Resolved (2026-11-09, Andrej):** A, kept, with the label's unstated source and timing named in the fit.

   **Andrej (2026-11-11, ok):** As implemented (A).

   **Resolved (2026-11-11, Andrej):** A, confirmed on this branch: the dataset stays, and `fit_reason` keeps the
   label's unstated source and timing; after issue 3 it no longer names the training hours.

2. **Split by time, or keep the random split as forced or as a stationary relation?**

   * **Problem:**
     - The release has no date, and its only order, the dropped `enrollee_id`, numbers the hackathon's train and test files together (1 to 33,380, the two files interleaved), with nothing that shows it follows sign-up time.
     - Along the id the share looking for a job change rises from 11.7% (lowest tenth) to 14.4% (highest) and the missing employer type rises and falls (17%, 32%, 24%), while the training hours completed stay flat (median 45 to 50 in every tenth), which they would not if the highest ids had signed up last.
     - Keep random as a stationary relation that treats the id as time, split in windows of the id, or keep random as forced, the time not being recoverable?
   * **Background:** how the data was collected is information for the split, and an order counts as time when it tracks time; a definition can name the use-case prototype it follows, with a `Time basis:` line: a stationary relation, measured where the time is dated, or the forced tag when the use case looks forward, time can move the target (as it can a later or behavioural value such as looking for a job change) and no usable time is there[^2a].
   * **Experiments:** the definition's rows and features, untuned LightGBM and logistic regression (LR), ROC AUC; nine windows of 1,019 enrollees back from the highest id, each trained on every lower id (50% to 94% of the rows):

     | Split | LightGBM | LR | Looking for a change, in test |
     |---|---|---|---|
     | A, random 3 x 3 folds (implemented) | 0.646 (fold SD 0.011) | 0.650 (0.009) | 13.2% |
     | B, newest window (ids 31,587 to 33,380) | 0.639 | 0.677 | 13.9% |
     | B, nine windows, mean | 0.645 (0.627 to 0.681) | 0.656 (0.625 to 0.685) | 11.9% to 15.9% (training 12.1% to 13.2%) |

     - On the same test rows of the eight older windows, training on as many enrollees drawn at random from all others scores 0.008 more for LightGBM and 0.002 less for LR: no measurable gain from higher ids.
     - The id as a feature lowers the windows' mean to 0.636 (LightGBM).
   * **Forced rather than stationary (C):** the measurements above show a relation flat only if the id is time, and it is not shown to follow sign-up, so they do not count as periods; with the time lost, a stationary relation would rest on the source alone, and looking for a job change is a value time can move, so C names the lost time instead.
   * **Unknown:** how Analytics Vidhya numbered the enrollees, and when each was recorded; the organiser could say.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random enrollees (implemented), as a stationary relation | stratified random 3 x 3 folds; definition tag `StationaryRelation`, a `Time basis:` line reading the id as sign-up order, with the windows' nil cost above | states the id order and its size; the hackathon's own split | treats as time an order the data does not show to be time; the share looking for a change rises along the id (11.7% to 14.4%) |
     | B | Windows in id order | `enrollee_id` kept as the time column; 9 windows of 1,019 back from the highest id | tests higher ids, if they are later sign-ups | splits on an order not shown to be time; the id ships as a feature, which JanataHack's rules forbid; no measured difference |
     | C | Random enrollees, forced from temporal | as A, with the definition tag `ForcedIIDFromTemporal` and its line naming the unstated period and the id's unproven order | claims no time order the data does not show; no measured cost of the id order either way | tests enrollees of the same unknown period as training |

   * **Recommendation:** C: the id is an assembly order of unknown meaning, the flat training hours speak against sign-up order, and the windows in id order score as the random folds do; A only if you read the id as sign-up order. **Decision:** stationary relation (A), windows (B) or forced (C)?

   **Notes for the AI:** on C: `data_tags = ("Spatial", "ForcedIIDFromTemporal")` and the curation note "- Time basis: ForcedIIDFromTemporal: enrollees signed up over a period the hackathon does not state, and the release has no date; `enrollee_id` numbers the train and test files together and is not shown to follow sign-up time (training hours flat along it), and windows in its order score as random folds do (ROC AUC 0.645 against 0.646, untuned LightGBM)"; replace the curation note "IID split: one row per enrollee and no dates."; record tag `Samples: Over Time`, without `Time: Dated`, as no time is recoverable. On B: keep `enrollee_id` in `_clean` as `time_index`, `temporal = Temporal(on="time_index", splits=TemporalSplits(window=1019, unit="rows", n_windows=9))`, a `splits_comment` saying the order is the organiser's numbering, record `required_split` `Temporal (NON-IID)`, tag `Non-IID (Temporal)`, and the tags `Samples: Over Time` and `Time: Dated`. On A, once PR #50 is in: `data_tags = ("Spatial", "StationaryRelation")` (no date column, so no `meta_time_present_unused` to accept), the curation note "- Time basis: StationaryRelation: `enrollee_id` numbers the enrollees of the hackathon's two files in an order read here as sign-up time (the reason of your decision); windows in that order cost nothing: the newest of nine scores ROC AUC 0.639 against 0.646 on random folds (untuned LightGBM; logistic regression 0.677 against 0.650), and on the older windows' test rows random training from all ids scores 0.008 more (LightGBM) and 0.002 less (logistic regression) than the lower ids alone", replacing "IID split: one row per enrollee and no dates."; record tags `Samples: Over Time` and `Time: Dated`.

   [^2a]: **SPLIT-32** (Should): how the data was collected is information for the split; the record's collection facts and, where one fits, the definition's use-case prototype with its `Time basis:` line. **SPLIT-8** (Must): a task temporal by its use case whose release cannot give the windows (dates lost, too few periods) ships in the closest regime, tagged as forced from temporal. **SPLIT-22** (Should): the raw file order can be the time order without a timestamp. **SPLIT-14** (Must): at least 3 windows, none trained on less than half of the data.

   **Answer (AI, 2026-11-06):** The record's collection facts no longer change with the option.

   - You accepted "Tell dated time from an inferred order in the `Time:` fact?": a record's collection facts follow the
     evidence, never the split option chosen[^2t].
   - The notes set `Time: Dated` on A and B and leave it out on C; the Time fact is now issue 4's own question, decided
     on the evidence whatever this issue takes. The record now carries `Target: Unknown`, as the label's timing is open
     (issue 1).
   - Option A is a `StationaryRelation`, which you now want always measured on a dated source; its windows are measured
     on the id, so A stands only if issue 4 counts the id as time.

   [^2t]: **SPLIT-32** (Should): the collection facts are true whatever task is built on the source and do not change
     with the split a definition chooses; a `StationaryRelation` is always measured (Andrej, 2026-11-06).

   **Resolved (2026-11-09, Andrej):** C ("Agree."): the random split is tagged `ForcedIIDFromTemporal` in `data_tags`,
   and the `Time basis:` line replaces the note "IID split: one row per enrollee and no dates."

   **Andrej (2026-11-11, ok):** Agree.

   **Resolved (2026-11-11, Andrej):** C again, now applied on this branch, which already carries the time-basis
   tags: `data_tags = ("Spatial", "ForcedIIDFromTemporal")` and the `- Time basis: ForcedIIDFromTemporal: ...` bullet
   in place of the note "IID split: one row per enrollee and no dates."; the folds do not change.

3. **Drop `training_hours`, the training completed after sign-up?**

   * **Problem:**
     - `training_hours` is the training the enrollee has completed, "known only some time after sign-up" (the definition's notes), while the prediction point the definition names is sign-up, so the column holds a value the institute does not have yet[^3a].
     - It carries nothing: alone it scores ROC AUC 0.495, and the share looking for a job change is 13.6% in the lowest fifth of hours and 13.0% in the highest.
     - Drop it, or move the prediction point to the end of the training, where the hours are known?
   * **Background:** the contest asks for the probability from "the current credentials/demographics/experience" (quoted in the definition), the answers of the sign-up form; the column was kept "as in the contest". The institute could also put people in touch with clients after the training, which would make the hours a valid input, but nothing in the contest says it does, and issue 1 leaves open when the label was recorded.
   * **Experiments:** the v0.2 frame (18,359 enrollees, 12 features), untuned LightGBM and logistic regression, ROC AUC, the shipped random 3 x 3 folds with and without the column (Slurm job 1366162): LightGBM 0.642 with it, 0.644 without; logistic regression 0.648 both.
   * **Effect on the task:** none on the score; the task as written would ask models to use a value from after the prediction point, which a deployed model scoring new sign-ups lacks.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | `training_hours` stays; `fit_reason` names its timing | the contest's columns | a value from after the stated prediction point |
     | B | Drop `training_hours` | the column leaves; the notes give the reason and the numbers | only sign-up answers remain, as the prediction point says; costs nothing measurable | departs from the contest's columns |
     | C | Keep, prediction point at the end of the training | no data change; `use_case`, the notes' prediction point and `fit_reason` say the institute scores enrollees after their training | keeps the column as a valid input | a use case the contest does not state |

   * **Recommendation:** B: the column comes after the stated prediction point and adds nothing, so dropping it makes the task match its use case at no cost. **Decision:** keep (A), drop (B) or move the prediction point (C)?

   **Notes for the AI:** on B, drop `training_hours` in `_clean`; the curation bullet "`training_hours` is the training completed ... Kept, as in the contest." becomes the reason with the numbers above (alone ROC AUC 0.495; LightGBM 0.644 without, 0.642 with); `known` loses "training hours completed"; `fit_reason` loses the training-hours clause; `dataset check`; a `CC` line in the record. On C, rewrite `use_case` ("... before it puts them in touch with clients after the training"), the prediction-point bullet and `fit_reason`.

   [^3a]: **LEAK-10** (Must): a feature holds only what existed at the prediction point. **USE-3** (Must): name the prediction point; a value that did not exist at that point is a leak. **LEAK-6** (Must): a confirmed leak goes even when small.

   **Resolved (2026-11-09, Andrej):** B: `_clean` drops `training_hours`; the curation bullet gives the numbers, and
   `known` and `fit_reason` lose the training hours.

   **Andrej (2026-11-11, change):** Option B: Drop training_hours.

   **Resolved (2026-11-11, Andrej):** B, now applied on this branch: `_clean` drops `training_hours` beside
   `enrollee_id`, the curation bullet gives the reason and the numbers, and `known` and `fit_reason` no longer name
   the hours. 11 features. `dataset check`: 0 errors, 2 warnings, both raised by the drop and documented in the
   curation notes rather than accepted: without the hours 1,988 rows (10.8%) repeat an earlier row and 319 (1.7%)
   share their features with a row of the other label; they are different enrollees with the same coarse answers.

4. **Correct the record's collection facts: `Time: Lost` in place of `Time: Dated`?**

   * **Problem:**
     - The record carries `Time: Dated`, but neither the release nor the contest pages date an enrollee, and the only order, the dropped `enrollee_id`, numbers the hackathon's train and test files together with nothing to show it follows sign-up (issue 2).
     - A time counts as dated when the release or its source keeps it or lets it be recovered, an order that tracks time included, and an assembly order of unknown meaning is not shown to be one[^4a].
     - Set `Time: Lost`, or keep `Time: Dated` because you read the id as sign-up order?
   * **Background:**
     - Along the id the share looking for a change rises (11.7% to 14.4% by tenth) and city_21's share doubles (5.9% to 12.1%), so the id carries an order; but the training hours completed stay flat (median 45 to 50 in every tenth), which they would not if the highest ids had signed up last and the hours were read at one date.
     - `Samples: Over Time` stays: the enrollees signed up over a period the contest does not state.
     - The record has no `Target:` tag, which stands for a target that exists with the features; issue 1 leaves open whether the label is a sign-up answer (no tag) or was recorded later (`Target: Varying Delay`), and no tag says the timing is unknown, so it stays as it is until issue 1 settles it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | `Time: Dated` (implemented) | the record as it is | fits issue 2's A or B, which read the id as sign-up order | claims a recoverable time the data does not show |
     | B | `Time: Lost` | the tag replaced | states what the source gives; fits issue 2's recommended C (forced from temporal) | none, unless the organiser confirms the id as sign-up order |

   * **Recommendation:** B, together with issue 2's C; A only if you decide issue 2 as A or B. **Decision:** A or B?

   **Notes for the AI:** on B, in the record's `tags` replace `'Time: Dated'` with `'Time: Lost'`, add `Andrej` to `checked_by` and a `CC` line with the reason (the id not shown to follow sign-up; training hours flat along it).

   [^4a]: **SPLIT-32** (Should): the record describes the source by collection facts true whatever task is built on it; `Time: Dated` when the release or its source keeps the time or lets us recover it (a date column, an order that tracks time, a value that encodes the period), else `Time: Lost`.

   **Resolved (2026-11-09, Andrej):** B: the record's `tags` carry `Time: Lost` in place of `Time: Dated`.

   **Andrej (2026-11-11, change):** Option B: Time: Lost.

   **Resolved (2026-11-11, Andrej):** B, now applied on this branch: the record's `tags` carry `Time: Lost` in place
   of `Time: Dated`; `Samples: Over Time` and `Target: Unknown` stay.

## Reference

https://www.kaggle.com/datasets/arashnic/hr-analytics-job-change-of-data-scientists
