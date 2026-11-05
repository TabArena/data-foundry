---
unique_name: santander_customer_transaction_prediction
name: Santander Customer Transaction Prediction
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: No (Retired)
decision_markers:
- Anonymized
- AHDS (Artifical/Handmade/Deterministic/Simulated)
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
source_row: 650
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Leak fixed: dropped the 400 `var_i_has_one`/`has_zero` features.** They follow the Kaggle #1 solution: for each var, does this row's value occur in another class-1 / class-0 row. The encoding is leave-one-out (a row never sees its own label), but it was computed over all 200k labelled rows before splitting, so every row's features encode the labels of the other rows in its test fold, which a deployment would not have. LightGBM ROC AUC (leak audit 2026-09-24, rechecked on other folds): 0.903 shipped, 0.899 with has_* recomputed from train-fold labels, 0.900 with label-free value counts, 0.896 raw 200 vars. We now ship `target` + `var_0..var_199` (200 features). The technique itself is worth applying inside a pipeline, computed per fold (or on unlabelled rows where a method may see them); this is noted in curation_comments.

CC: "Interesting dataset, but not on OpenML. License allows to use the data for research, but not distribute it - so we have an API issue."

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — Area Under Receiver Operating Characteristic Curve (https://www.kaggle.com/competitions/santander-customer-transaction-prediction (Kaggle API evaluationMetric)).

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (1 is the event).

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the folder's `REVIEW.md`. Retire as generated: within each class the 200 columns are independent at exactly the chance rate (5.1% and 0.1% of pairs outside the 95% and 99.9% bands) and real rows cannot be told from within-class shuffles (AUC 0.49); the shipped-data leak is already fixed in v0.2. Priority 1: gap 0, use case 0, source 0, shape 1, risk -1.

CC (2026-11-05, Andrej): retired as generated data (`No (Retired)`, `AHDS`). The data: the training file of Santander's Customer Transaction Prediction competition (Kaggle, 2019), 200,000 rows of 200 anonymised numbers and whether the customer made an unnamed transaction (10%).
- **Each row is 200 values drawn one column at a time given the label:** within each class the 200 columns are as independent as random draws (5.1% of the 19,900 column pairs outside the 95% noise band and 0.1% outside the 99.9% band, the rates chance gives), and a model cannot tell real rows from rows whose values were shuffled within the class (ROC AUC 0.49). Santander's real customer table (santander_customer_satisfaction) fails both tests by far (53% of pairs, ROC AUC 1.0).
- **So the best model is known in advance:** for rows drawn that way, naive Bayes, a sum of 200 one-column terms, is the right model by construction; it reaches ROC AUC 0.899, level with TabPFN-3.5 (0.897 to 0.902). The task ranks methods by how well they add up independent columns, a property of the generator, not of customers.
- **The release points the same way:** the host published nothing about the columns or the transaction, the earlier curation notes call the features generated or transformed for the competition, and competitors had to filter synthetic rows out of the test file.
- **Why the keep does not hold:** the leak fixed on 2026-09-30 is gone and masked columns alone are no reason to retire, but here the rows themselves are not records of customers.
Not changed: `Anonymized` stays.

## Reference

Mercedes Piedra, Sohier Dane, and Soraya_Jimenez. Santander Customer Transaction Prediction. https://kaggle.com/competitions/santander-customer-transaction-prediction, 2019. Kaggle.
