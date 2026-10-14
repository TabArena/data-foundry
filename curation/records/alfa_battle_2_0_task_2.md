---
unique_name: alfa_battle_2_0_task_2
name: Alfa Battle 2.0 (Task 2)
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
- Review Prio 1 (Atlas)
collections:
- New (BeyondArena)
original_source: Other
year: '2020'
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://boosters.pro/championship/alfabattle2/overview
- https://ods.ai/competitions/dl-fintech-card-transactions
- https://www.kaggle.com/datasets/mrmorj/alfabattle-20?select=alfabattle2_alpha_sample.csv
- https://www.kaggle.com/datasets/sokolovaleks/alfabattle2-sandbox/data
- https://github.com/SlayZar/alpha_task_2
v2_path: datasets/_dev/tabarena-v0pt2/alfa_battle_2_0_task_2/dataset.py
source_row: 743
type_adapter_id: curation-record-v1
---

## Comments

"A key component of our work is responsible lending, based on a model-based assessment of the likelihood of a borrower defaulting on their obligations."
"The training set was collected over N days, and the test set over the following K days. Position on the leaderboard depends on how well we can predict past and future borrower defaults. The target variable is a binary value taking values 0 and 1"
ROC AUC

**Assessment (AI, 2026-10-07):** Boosters' links are dead; Alfa-Bank re-hosted byte-identical files for its 2022 ODS.ai competition (no login). Tabular models are competitive here (organizers' boosting baseline on aggregates 0.737 public AUC, their RNN 0.760), so the v2 folder uses that baseline's 127 aggregates per product. Boosters says the products are numbered by date; the transactions' week codes give 24 monthly issue dates, tested in 3 two-month windows. A client's products share identical transactions: when the earlier one defaulted, the later one defaults in 96% of cases, a flag not yet known at the later issue, so such products are removed from the training sides. Licence (noted only): the competition rules forbid passing on the data; Alfa-Bank later allowed research use.

CC (2026-10-13, Lennart): Features like the top solutions of the competition, what a data scientist would build, instead of the organizers' 127-feature baseline: 513 aggregates over restored ruble amounts (amount and timing statistics, per-value shares and means, mode and last values, money in against out, daily activity, a balance proxy, the last 30 and 90 days). Label-based encodings, embeddings and sequence-model scores stay out (modelling steps). Sources: 1st place slides (six LightGBMs, 0.780 private without the RNN), 4th private place slides (3,289 features), 9th place code (github.com/aizakharov94/AlfaBattle_task2); slides in the Drive folder linked from Habr 551130. Untuned LightGBM on our windows: ROC AUC 0.787 / 0.771 / 0.772 against 0.774 / 0.757 / 0.763.

## Reference

Booster
