---
unique_name: early_stage_diabetes_risk_prediction
name: Early Stage Diabetes Risk Prediction
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Selection Bias
tags:
- Tiny Data
collections:
- New (BeyondArena)
- TabSTAR
original_source: UCI
year: '2020'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5VG8H
- https://www.openml.org/search?type=data&id=43643&sort=runs&status=active
- https://www.kaggle.com/datasets/ishandutta/early-stage-diabetes-risk-prediction-dataset
notebook_path: datasets/beyond_iid/new_iid/early_stage_diabetes_risk_prediction/early_stage_diabetes_risk_prediction.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/early_stage_diabetes_risk_prediction/dataset.py
source_row: 765
type_adapter_id: curation-record-v1
---

## Comments

Looks good

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Islam et al. 2019 report accuracy with precision, recall and F-measure, no unique metric and no threshold or costs (MET-5, MET-6).

## Reference

@inproceedings{islam2019likelihood,
  title={Likelihood prediction of diabetes at early stage using data mining techniques},
  author={Islam, MM Faniqul and Ferdousi, Rahatara and Rahman, Sadikur and Bushra, Humayra Yasmin},
  booktitle={Computer Vision and Machine Intelligence in Medical Image Analysis: International Symposium, ISCMM 2019},
  pages={113--125},
  year={2019},
  organization={Springer}
}
