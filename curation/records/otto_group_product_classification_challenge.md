---
unique_name: otto_group_product_classification_challenge
name: Otto-Group-Product-Classification-Challenge
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
year: '2015'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/otto-group-product-classification-challenge/overview
notebook_path: datasets/beyond_iid/new_iid/otto_group_product_classification_challenge/otto_group_product_classification_challenge.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/otto_group_product_classification_challenge/dataset.py
source_row: 648
type_adapter_id: curation-record-v1
---

## Comments

CC: "Distinguish products in 10 groups based on 93 features. Competition not won through leaks, but test-time adaptation helped. In general seems like a good tabular data task for random splits. Kaggle licence forbids distribution, but as the data is on OpenML with 'Unknown' license. Although this is one of the best datasets we might not be able to use it."

**Assessment (AI, 2026-10-14):** 9 classes, not 10: the training file's `target` holds Class_1 to Class_9 (61,878 products) and the competition's sample submission has nine class columns.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source log_loss — multi-class logarithmic loss, the competition's evaluation metric (Kaggle evaluation page).

## Reference

Benjamin Bossan, Josef Feigl, and Wendy Kan. Otto Group Product Classification Challenge. https://kaggle.com/competitions/otto-group-product-classification-challenge, 2015. Kaggle.
