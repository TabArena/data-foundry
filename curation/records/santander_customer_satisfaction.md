---
unique_name: santander_customer_satisfaction
name: SantanderCustomerSatisfaction
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Anonymized
tags:
- Larger IID Data
collections:
- TabArena Reject
original_source: Kaggle
year: '2016'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/c/santander-customer-satisfaction
notebook_path: datasets/beyond_iid/new_iid/santander_customer_satisfaction/santander_customer_satisfaction.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/santander_customer_satisfaction/dataset.py
source_row: 649
type_adapter_id: curation-record-v1
---

## Comments

CC: "work with hundreds of anonymized features to predict if a customer is satisfied or dissatisfied with their banking experience. Very nice dataset. Data was uploaded to OpenML with Public license, but the actual license might be more prohibitive. Unsure how to deal with that. also, we don't know the split, but as competition winners used random, this should be fine."

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: the 56 ind_var indicators, which hold only 0 and 1 (found on the data in `_feature_types`).

CC (2026-10-21, Lennart): on which 0/1 columns are flags: "no if we can infer from the semantic context, keep it a number, this is a real-world bias. We want to make things categorical if we know from the context they are indeed such" (CLEAN-14, amended again). Kept categorical: the 56 ind_var columns, indicators by their name, now an explicit list.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — Area Under Receiver Operating Characteristic Curve (https://www.kaggle.com/competitions/santander-customer-satisfaction (Kaggle API evaluationMetric)).

## Reference

Soraya_Jimenez and Will Cukierski. Santander Customer Satisfaction. https://kaggle.com/competitions/santander-customer-satisfaction, 2016. Kaggle.
