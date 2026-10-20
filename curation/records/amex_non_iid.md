---
unique_name: amex_non_iid
name: amex
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Non-IID (Grouped)
collections:
- New (BeyondArena)
original_source: Kaggle
year: '2022'
domain: finance
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/amex-default-prediction/data?select=train_data.csv
notebook_path: datasets/beyond_iid/grouped/amex_non_iid/amex_non_iid_1m.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/amex_non_iid_1m/dataset.py
source_row: 690
type_adapter_id: curation-record-v1
---

## Comments

CC: ""Target is binary classification from a survival prediction task (thus some noise); mostly anonymized data, some categorical data; dataset made imbalanced by default and scoring is affected by this;

Temporal split needed, see train/test shift; likely also grouped-based splits (same customers in the data);

Many weird features, likely lagged-data from temporal original data; unsure how to treat recurring users""

Can be used as IID and non-iid. Several final versions of kaggle made the task iid. Moreover, you could use the non-iid version as well

TODO: decide if add groupby features or not -> add not and leave it to the pipeline but make sure good baselines create the features

CC (2026-10-02, Lennart): The per-customer prediction is the latest statement's (`aggregation="last"`), with every statement of the customer available to a model (`context="all_rows"`). The competition asks for one prediction per customer, its label comes from the 18 months after the latest statement, and its test set holds each customer's full history (top solutions aggregated features over all statements). The label is one value per customer, the same on every statement, so `max` over statements does not express "default once, always default": it lets an old statement speak for a default 18 months after the newest one. LightGBM per statement on the grouped folds, scored per customer: `last` ROC AUC 0.958 / amex metric 0.780, `max` 0.949 / 0.745, `mean` 0.946 / 0.720, unaggregated rows ROC AUC 0.938.

CC (2026-10-06, Lennart): Kept as it is after the task-probe review (flag `no_spread`). Scored per customer at the latest statement, the linear model, random forest and LightGBM all reach ROC AUC 0.95 (skill +0.898 to +0.907, standard deviation under 0.01 over the folds), and `P_2` alone reaches skill +0.82; on BeyondArena (the shipped version, one holdout per statement) TabPFN-3.5 reaches AUC 0.947 and the median method 0.943. Strong methods converging on a large, well-engineered credit dataset is expected; with 1.5M rows small gaps can still be real.

## Reference

Kaggle
