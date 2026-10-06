---
unique_name: fitness_club
name: Fitness_Club_c / fitness_club
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: No (Retired)
decision_markers:
- Trivial
original_source: Kaggle
year: '2023'
required_split:
- Random (IID)
source_links:
- https://www.kaggle.com/datasets/ddosad/datacamps-data-science-associate-certification
notebook_path: datasets/beyond_iid/old_iid/fitness_club/fitness_club.ipynb
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Seems rather simple, but interesting. Might require time split. Features are time-invariant, but distribution shifts due to changing classes and instructors are still likely. Unclear which time period the 1500 sampes span

Linear model is best for this dataset - data is from a datacamp course and might have been artificially generated.

Potential issue: temporal split required

Lennart: Maybe simple task but no other objections

Andrej: Not the best data for this task as a lot of important information is missing. But interesting enough to ignore that; Also license might be an issue

CC (2026-10-05, Lennart): Retired from TabArena v0.2 as trivial (task-probe review, flag `one_feature`). Ranking the members by `months_as_member` alone, with no model, gives ROC AUC 0.822 on the 30 shipped folds, above all 37 BeyondArena configurations (best RealTabPFN-2.5 0.821, median 0.818, worst ExtraTrees 0.776), and above the best on 21 of 30 folds. Every other feature lowers the score (weight 0.821, all features in a logistic model 0.813, CatBoost 0.805), so the dataset ranks methods only by how much they lose by fitting the other five columns. The rows also look generated: `days_before` equals 2 x the weekday's number (Monday 1 to Sunday 7) in 1,251 of the 1,500 rows (1,094 of the 1,141 AM classes) and is within a day of it in 1,451, where a fixed booking day would add one day per weekday; the raw file carries the planted errors of a cleaning exam (410 targets written `-0`, mixed weekday spellings, " days" suffixes, `-` as a category).

## Reference

https://www.kaggle.com/datasets/ddosad/datacamps-data-science-associate-certification
