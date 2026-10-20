---
unique_name: early_stage_diabetes_risk_prediction
name: Early Stage Diabetes Risk Prediction
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: Yes (Disagreement)
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

CC (2026-10-19, Andrej): I disagree with keeping it; the patients are not the population the task is for, and the file is half duplicates.

- **Wrong population:** the use case is screening adults for a blood-sugar test, but every row is a patient of a diabetes hospital, 62% diabetic (69% after dedup); UCI calls them "newly diabetic or would be diabetic". How the negatives were recruited and how the label was set is not stated. Other datasets pass with an approximate fit, but here the gap is why the features work at all.
- **The symptoms work because of who was sampled** (spectrum bias: a test looks better when cases are clear-cut and controls are healthy; Ransohoff and Feinstein 1978). Early type 2 diabetes is usually without symptoms, which is why screening uses blood tests; here symptomatic patients face hospital negatives who mostly report none. Polyuria and polydipsia (frequent urination, excessive thirst; the classic symptoms in the diagnostic criteria) added up, with no training, give AUC 0.905, LR on them plus sex 0.937. Partial paresis (partial paralysis, a late complication) is a strong positive marker, so many positives are established cases, not early ones.
- **Half the file repeats itself:** 52% of the 520 rows exactly repeat another row on all 17 columns (61% of negatives, 46% of positives), mostly rows with several symptoms, which distinct patients would rarely share; 74% of rows 260-519 repeat a row from 0-259. After dedup only 78 negatives remain (~26 per test fold), the class balance shifts from 62% to 69% positive, and which rows are real patients is unknown.

Suggest excluding.

Ransohoff DF, Feinstein AR. Problems of spectrum and bias in evaluating the efficacy of diagnostic tests. N Engl J Med. 1978;299(17):926-930. doi:10.1056/NEJM197810262991705

Islam MMF, Ferdousi R, Rahman S, Bushra HY. Likelihood prediction of diabetes at early stage using data mining techniques. In: Computer Vision and Machine Intelligence in Medical Image Analysis. Advances in Intelligent Systems and Computing, vol 992. Singapore: Springer; 2019:113-125. doi:10.1007/978-981-13-8798-2_12

## Reference

@inproceedings{islam2019likelihood,
  title={Likelihood prediction of diabetes at early stage using data mining techniques},
  author={Islam, MM Faniqul and Ferdousi, Rahatara and Rahman, Sadikur and Bushra, Humayra Yasmin},
  booktitle={Computer Vision and Machine Intelligence in Medical Image Analysis: International Symposium, ISCMM 2019},
  pages={113--125},
  year={2019},
  organization={Springer}
}
