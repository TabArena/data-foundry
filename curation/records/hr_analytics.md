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

## Reference

https://www.kaggle.com/datasets/arashnic/hr-analytics-job-change-of-data-scientists
