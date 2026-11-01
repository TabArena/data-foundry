---
unique_name: wns_hr_employee_promotion
name: 'WNS Analytics Hackathon 2018 (DataHack ''HR Analytics''): employee recommended for promotion'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Website
year: '2018'
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.analyticsvidhya.com/datahack/contest/wns-analytics-hackathon-2018-1
- https://www.kaggle.com/datasets/arashnic/hr-ana
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 54,808 labelled employees at a promotion checkpoint of an unnamed "large MNC", from the WNS Analytics Wizard hackathon on Analytics Vidhya (September 2018), with a stated decision (spot the eligible candidates early) and a competition F1; the data owner is unnamed and the Kaggle mirror lacks one column of the original.
- Source: WNS Analytics Wizard 2018, an online hackathon on Analytics Vidhya, 14-16 September 2018 ("3800+ registrations, 364 teams, and more than 1,200 submissions", AV solutions blog of December 2018); the contest page (`wns-analytics-hackathon-2018-1`) shows its problem statement, rules and files only after login, so they were not read there. As published: `train.csv` with 54,808 rows (4,668 promoted, 8.5%) and an unlabelled `test.csv` with 23,490 rows; AV's data dictionary (AV blog of October 2020) has 14 columns: `employee_id`, `department`, `region`, `education`, `gender`, `recruitment_channel`, `no_of_trainings`, `age`, `previous_year_rating`, `length_of_service`, `KPIs_met >80%` ("if Percent of KPIs(Key performance Indicators) >80% then 1 else 0"), `awards_won?`, `avg_training_score` ("Average score in current training evaluations") and the target `is_promoted` ("Recommended for promotion"). The Kaggle mirror arashnic/hr-ana (files dated 2020-12-23, "CC0-1.0", source given as the AV problem statement) was previewed: 54,808 rows x 13 columns, without `KPIs_met >80%` (a problem of that copy, PROV-15); 2,409 missing `education`, 4,124 missing `previous_year_rating`, 219 rows duplicated apart from the id, 9 departments, 34 regions.
- Use case: the HR team, at a checkpoint before the promotion evaluation ends, picks the employees likely to be promoted so it can prepare them in time. The source: "The final promotions are only announced after the evaluation and this leads to delay in transition to new roles. Hence, company needs help in identifying the eligible candidates at a particular checkpoint so that they can expedite the entire promotion cycle" (the AV statement, as copied on the Kaggle card). Fit direct. Regime IID: the release is one checkpoint of one company, one row per employee, with no dates or cycles (a next cycle would be temporal, but none is recorded).
- Siblings and duplicates: no record holds this data (grep by promot, WNS, is_promoted, hr-ana). Other HR records: `hr_analytics` (accepted; AV's job change of data scientists, another task), `happyforce_employee_churn` (TBD -> Yes), `ibm_hr_analytics_employee_attrition_performance_employee_ibm_attrition` (`No`, fictional data). External collections: none found on the pages read.
- Better data: from the curator's Zotero collection (item 90, the DataHack platform); no further search this round.
- Papers and pages: AV blog "WNS Hackathon Solutions by Top Finishers" (https://www.analyticsvidhya.com/blog/2018/12/wns-hackathon-solutions-by-top-finishers/; rank 1 XGBoost with imputation and degree-2 interactions, rank 2 LightGBM on kNN and aggregate features, rank 3 a 29-model ensemble with threshold tuning); AV blog "Ultimate Beginners Guide to Breaking into the Top 10% in Machine Learning Hackathons" (https://www.analyticsvidhya.com/blog/2020/10/ultimate-beginners-guide-top-10-machine-learning-hackathons/, walks through this hackathon with the data dictionary); a Responsible AI Toolbox case study (readthedocs) uses the AV file with `KPIs_met >80%`.
- Metric: F1 on the hard label: "F1 score is the evaluation metric for this Hackathon" (AV blog of October 2020; the contest page itself needs login), and the 2018 blog has a top team tuning its cut-off; a competition's metric (MET-4), so `f1` with `is_promoted` = 1 as the positive class, the threshold chosen on the training side; inputs none.
- Risks for /add-dataset: take the AV original with `KPIs_met >80%` (login) rather than the mirror, or note the column as lost (PROV-15, PROV-13); `avg_training_score` comes from the "current training evaluations" of the same promotion cycle (in the preview 87.7% of employees above 90 are promoted, against 8.5% overall): check it is known at the checkpoint and is not part of the final evaluation (USE-3, LEAK-10); the data owner is unnamed and no paper describes the collection, so an approximate-fit note (PROV-2) and the PROV-3 tests for generated data; `gender` as an input of a promotion task is a fairness question for the curator; the test labels are not public, so only the 54,808 training rows can be used.
- Priority: gap 0 (binary, IID and business are covered), use case + (the source names the actor, the checkpoint and the decision), source 0 (a hackathon platform, the company unnamed), shape + (54,808 employees, 12 features of mixed types).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 90: "DataHack Platform: Compete, Learn & Grow in Data Science".
- as published: One row per employee at the promotion checkpoint. 54,808 labelled training rows (4,668 promoted, 8.5%) and 23,490 unlabelled test rows, per third-party write-ups (not counted); Kaggle mirror ...; target: is_promoted: recommended for promotion after the evaluation (binary); access: registration.
- Why: An HR decision task with a stated prediction point, not recorded; hr_analytics is a different AV task (data scientists changing jobs).
- Adds: An employee-promotion task next to the attrition and job-change records. Sizes now confirmed (the first pass had not counted rows). Caveats: thin provenance (no provider named); AV terms (the Kaggle mirror claims CC0 but redistributes AV data); gender as a feature; previous_year_rating missing for new joiners. Likely ...
