---
unique_name: santander_customer_transaction_prediction
name: Santander Customer Transaction Prediction
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Larger IID Data
collections:
- TabArena Reject
original_source: Kaggle
year: '2019'
domain: finance
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/santander-customer-transaction-prediction
notebook_path: datasets/beyond_iid/new_iid/santander_customer_transaction_prediction/santander_customer_transaction_prediction.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/santander_customer_transaction_prediction/dataset.py
source_row: 650
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Leak fixed: dropped the 400 `var_i_has_one`/`has_zero` features.** They follow the Kaggle #1 solution: for each var, does this row's value occur in another class-1 / class-0 row. The encoding is leave-one-out (a row never sees its own label), but it was computed over all 200k labelled rows before splitting, so every row's features encode the labels of the other rows in its test fold, which a deployment would not have. LightGBM ROC AUC (leak audit 2026-09-24, rechecked on other folds): 0.903 shipped, 0.899 with has_* recomputed from train-fold labels, 0.900 with label-free value counts, 0.896 raw 200 vars. We now ship `target` + `var_0..var_199` (200 features). The technique itself is worth applying inside a pipeline, computed per fold (or on unlabelled rows where a method may see them); this is noted in curation_comments.

CC: "Interesting dataset, but not on OpenML. License allows to use the data for research, but not distribute it - so we have an API issue."

## Reference

Mercedes Piedra, Sohier Dane, and Soraya_Jimenez. Santander Customer Transaction Prediction. https://kaggle.com/competitions/santander-customer-transaction-prediction, 2019. Kaggle.
