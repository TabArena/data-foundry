---
unique_name: sepsis_prediction
name: SepsisPrediction
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
- TabSTAR
original_source: Kaggle
year: '2019'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/salikhussaini49/prediction-of-sepsis
source_row: 689
type_adapter_id: curation-record-v1
---

# SepsisPrediction

## Comments

CC: "Highly imbalanced, high missing values, requires some feature preprocessing, unclear if patient duplicates; potential data leakage for unit 1 and unit 2 or group-based data; survival prediction task transformed into binary classification (creates some problems)"

https://physionet.org/content/challenge-2019/1.0.0/

## Reference

Kaggle / PhysioNet
