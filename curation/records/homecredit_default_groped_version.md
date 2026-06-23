---
unique_name: homecredit_default_groped_version
name: Homecredit Default (Groped Version)
checked_by:
- Lennart
suggestion: TBD -> Yes
tags:
- Non-IID (Temporal)
- Non-IID (Grouped)
collections:
- TabArena Reject
- TabRed
original_source: Kaggle
year: '2024'
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/competitions/home-credit-credit-risk-model-stability
- https://github.com/yandex-research/tabred/tree/main/preprocessing#homecredit-default-stability-homecredit-20
source_row: 635
type_adapter_id: curation-record-v1
---

# Homecredit Default (Groped Version)

## Comments

Again, the data was in theory grouped but never solved as such, we could again try yo get a model for it! 

Follow the preprocessing from TabRed as well. Verify that TabRed preprocessing gets similar feature sets to top solutions

Kaggle solutions used IID CV splits. There is also a problem with metric hacking on the Kaggle submissions.

TabRed uses 4/5 month as time horizon

## Reference

Daniel Herman, Tomas Jelinek, Walter Reade, Maggie Demkin, and Addison Howard. Home Credit - Credit Risk Model Stability. https://kaggle.com/competitions/home-credit-credit-risk-model-stability, 2024. Kaggle.
