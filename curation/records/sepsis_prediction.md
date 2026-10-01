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
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/salikhussaini49/prediction-of-sepsis
notebook_path: datasets/beyond_iid/grouped/sepsis_prediction/sepsis_prediction_1m.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/sepsis_prediction_1m/dataset.py
source_row: 689
type_adapter_id: curation-record-v1
---

## Comments

CC: "Highly imbalanced, high missing values, requires some feature preprocessing, unclear if patient duplicates; potential data leakage for unit 1 and unit 2 or group-based data; survival prediction task transformed into binary classification (creates some problems)"

https://physionet.org/content/challenge-2019/1.0.0/

CC (2026-10-01, Lennart): Leak audit: the data is fine; the scoring has to change (planned). Each row is one patient-hour with only that hour's measurements, and SepsisLabel is 1 from 6 hours before onset onward, so at every hour the task is "sepsis within the next 6 hours"; no row feature encodes the time left in the stay. The risk is in the evaluation: grouped splits put complete patient records into the test set, and septic records end shortly after onset, so a method that uses a patient's later rows (record length, last Hour/ICULOS) can read the outcome. Going forward, predictions must be causal per patient and scored with the PhysioNet 2019 utility per patient (already declared as the metric, with group_on = Patient_ID and group_time_on = Hour) rather than as independent rows. Patient_ID is group metadata and must not be used as a model feature. Documented in the v2 definition's curation comments.

## Reference

Kaggle / PhysioNet
