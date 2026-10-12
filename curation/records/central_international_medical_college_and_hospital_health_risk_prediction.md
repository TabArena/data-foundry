---
unique_name: central_international_medical_college_and_hospital_health_risk_prediction
name: Central International Medical College and Hospital Health Risk Prediction
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Trivial
tags:
- New IID
collections:
- New (BeyondArena)
original_source: Kaggle
year: '2025'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/ludocielbeckett/health-risk-prediction-anonymized-real-data
v2_path: datasets/_dev/tabarena-v0pt2/central_international_medical_college_and_hospital_health_risk_prediction/dataset.py
source_row: 670
type_adapter_id: curation-record-v1
---

## Comments

Even if some information are missing, this looks like very real data from https://dcimch.com/

Target variable might be noisy/fake and thus the task might be trivial. We will see post hoc.

**Assessment (AI, 2026-10-07):** Risk_Level is the NEWS2 band of the eight features (RCP 2017 NEWS2 Charts 1, 2 and 4: total 0 Normal, 1-4 Low, a 3 in one parameter or 5-6 Medium, 7+ High) in 1,000 of 1,000 rows, with the SpO2 scale-2 points also given on air (987 rows under Chart 1's on-oxygen condition). The label is a lookup of the features, not an outcome: Trivial (crit. 4C), AHDS (deterministic). The vitals also look generated: Patient_ID runs in label blocks (P0001-P0160 all Normal, P0722-P1000 all High), and within a class pulse is unrelated to temperature (r -0.07 to -0.03) and SpO2 to oxygen or scale. Suggest No (Trivial, AHDS). Evidence: the v2 folder's README, decisions 1-3.

CC (2026-10-12, Lennart): No: the label is the NEWS2 chart applied to the vital signs the data ship, a published rule whose inputs are the whole task (a lookup scores log loss 0).

## Reference

Kaggle
