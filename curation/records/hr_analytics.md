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
- Database Snapshot
original_source: Other
year: '2018'
collection_period: Unknown
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

CC (2026-11-17, Andrej): the declared split (random, 3x3 folds, `ForcedIIDFromTemporal`) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split review, cross-dataset item).

CC (2026-11-18, Andrej): the forced tag stays (Review issue 1, A; stationarity reasoning, SPLIT-32 as amended today): no reason to take later samples as interchangeable. A labour-market behaviour with an undocumented target and not-flat similar intent sets; a low ceiling is no stationarity reason.

## Review

**Outcome:** added. Stationarity reasoning of 2026-11-18: the definition reaches the forced step with no time to measure; decided below.

**Main points:** Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?

**Issues for Andrej:**

1. **Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?**

   * **Problem:**
     - Time: Enrollees signed up over an unstated period; no date in the release and enrollee_id is not shown to follow sign-up time (training hours flat along it), so its windows (0.645 vs 0.646 random ROC AUC) are not a time test.
     - Use: A training institute screens new enrollees for job-seeking intent before passing them to hiring clients, after the July 2018 hackathon data.
     - Mechanism: Whether a data-science trainee looks for a new job depends on the labour market (demand, layoffs, salaries) and the institute's intake; both move between years, the 2018 data-science hiring boom especially.
   * **Background:** similar datasets[^asr].

     | Similar dataset or source | What was measured | Verdict | Why similar |
     |---|---|---|---|
     | mobile_churn (splits.md Cases) | train on June, test later joiners: ROC AUC 0.661 vs 0.690 IID | not flat | a person's intent to leave read from profile attributes |
     | online_shoppers_purchasing_intention_dataset | stationary-relation test (v3) | not flat | a behavioural intent target |

   * **For a stationary use case:**
     - Low-signal task (ROC AUC 0.62-0.63 for every family), so drift has little to shift in absolute terms.
   * **Against:**
     - Markets: job-change intent follows the labour market, which changed sharply after 2018.
     - Intake changes: who enrolls depends on the institute's marketing and course mix.
     - Target: Unknown (how and when 'looking for a job' was recorded is not stated).
     - Similar intent targets measured in the collection are not flat.
   * **Earlier views:**
     - CC (2026-11-17, Andrej): blind walk reaches the shipped random split with ForcedIIDFromTemporal.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedIIDFromTemporal` (implemented) | The folds stay; the Time basis line names the reasoning below | Claims only what is known | The split stands for later samples only as far as the use case is stationary |
     | B | `AssumedStationaryRelation` | The folds stay; you give the reason (eight words or more) | Documents why random folds stand for later samples | Markets: job-change intent follows the labour market, which changed sharply after 2018.; Intake changes: who enrolls depends on the institute's marketing and course mix. |

   * **Recommendation:** A, a labour-market behaviour with an undocumented target and not-flat similar intent sets; a low ceiling is no stationarity reason. Confidence: high. **Decision:** A or B?

   [^asr]: **SPLIT-32** (Should; amended 2026-11-18, Andrej): "where it holds none, the review reasons whether the use case can be taken as stationary, from the domain's mechanism and from similar datasets ..., where the AI offers `AssumedStationaryRelation` with a recommendation for a person to decide." `AssumedStationaryRelation` keeps the forced split's folds and replaces only the tag; its line opens `AssumedStationaryRelation (<person>, <date>): <reason>`.

   **Andrej (2026-11-18, ok):** as implemented.

   **Resolved (2026-11-18, Andrej):** A, as implemented: the forced tag stays; the `Time basis:` line gives the reasoning (A labour-market behaviour with an undocumented target and not-flat similar intent sets; a low ceiling is no stationarity reason.)

## Reference

https://www.kaggle.com/datasets/arashnic/hr-analytics-job-change-of-data-scientists
