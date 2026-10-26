---
unique_name: ljubljana_breast_cancer
name: Ljubljana Breast Cancer \
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Tiny Data
collections:
- New (BeyondArena)
- TabSTAR
original_source: UCI
year: '1988'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/faysalmiah1721758/breast-cancer-data
- https://github.com/jbrownlee/Datasets/blob/master/breast-cancer.names
- https://doi.org/10.24432/C51P4M
- https://www.openml.org/d/13
notebook_path: datasets/beyond_iid/new_iid/ljubljana_breast_cancer/ljubljana_breast_cancer.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/ljubljana_breast_cancer/dataset.py
source_row: 769
type_adapter_id: curation-record-v1
---

## Comments

looks good

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Every 1986-1988 paper on the data (Michalski et al., Clark & Niblett, Cestnik et al.) reports accuracy only, without costs or a threshold; 30% recurrence on 286 rows. Original rejected: accuracy. roc_auc is the binary fallback.

## Reference

? UCI
