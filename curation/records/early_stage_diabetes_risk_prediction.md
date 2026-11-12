---
unique_name: early_stage_diabetes_risk_prediction
name: Early Stage Diabetes Risk Prediction
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: No (Retired)
decision_markers:
- No Good Target / Scientific Discovery
- Not Representative
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

American Diabetes Association Professional Practice Committee. 2. Diagnosis and Classification of Diabetes: Standards of Care in Diabetes—2025. Diabetes Care. 2025;48(Suppl 1):S27-S49. doi:10.2337/dc25-S002

Bang H, Edwards AM, Bomback AS, et al. Development and validation of a patient self-assessment score for diabetes risk. Ann Intern Med. 2009;151(11):775-783. doi:10.7326/0003-4819-151-11-200912010-00005

Lindström J, Tuomilehto J. The diabetes risk score: a practical tool to predict type 2 diabetes risk. Diabetes Care. 2003;26(3):725-731. doi:10.2337/diacare.26.3.725

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Islam et al. 2019 report accuracy with precision, recall and F-measure, no unique metric and no threshold or costs (MET-5, MET-6).

CC (2026-11-10, Andrej): stays retired, for several reasons that hold together, not one: the selection bias (69% diabetic, late symptoms such as partial paresis in 57% of positives, negatives mostly men) makes the task not even an approximate fit for early-stage screening; an untrained symptom rule reaching ROC AUC 0.905 is far too high for the noisy real task; and models solving it almost perfectly (TabPFN 3.5 0.972) is unrealistic. Markers `Selection Bias` and `Not Representative`.

CC (2026-11-11, Lennart): retired because no decision is made from these features (USE-2; the fit None, USE-8). The use case was a doctor or an app deciding from a symptom questionnaire whether a person should have a blood-sugar test, but symptoms are not where that decision needs a prediction. A person with the symptoms of high blood sugar this table records (frequent urination, thirst, weight loss, blurred vision) is tested because of them, and the classic ones with one random plasma glucose of 200 mg/dL or more are a diagnosis (ADA 2025). Once the actor holds these inputs, they act on them (USE-2). People without symptoms are screened on risk factors (age, BMI, family history, blood pressure, physical activity: the ADA risk test, Bang et al. 2009; FINDRISC, Lindström and Tuomilehto 2003), of which the table has only age, sex and a yes/no obesity. No other use case fits (USE-9): the diabetes hospital the rows come from can measure blood sugar directly. The screening task is `nhanes_undiagnosed_diabetes` (adults never told they have diabetes, HbA1c at the exam), where methods reach ROC AUC 0.81 to 0.86 (AI assessment in its record) against 0.947 to 0.977 here. Markers: `No Good Target / Scientific Discovery` for the fit None; `Not Representative`, as no testing decision is made from symptoms; `Selection Bias` for the sample (patients of a diabetes hospital, 69% diabetic, 67 of the 78 negatives men, so 80 of the 91 women are positive). The reasons of 2026-11-10 would not retire it on their own: a selection the setting does not share makes the fit approximate (USE-8; eryhemato_squamous_disease and hepatitis_c_prediction kept), the untrained symptom rule (ROC AUC 0.906) stays below the methods and so is no proof of `Trivial` (TP-4), and the tuned methods spread (TP-3: tuned CatBoost above tuned logistic regression on 97% of BeyondArena's 60 folds, +0.022), while a near-saturated score is no reason by itself. This line replaces the reasons of the CC of 2026-11-10.

## Reference

@inproceedings{islam2019likelihood,
  title={Likelihood prediction of diabetes at early stage using data mining techniques},
  author={Islam, MM Faniqul and Ferdousi, Rahatara and Rahman, Sadikur and Bushra, Humayra Yasmin},
  booktitle={Computer Vision and Machine Intelligence in Medical Image Analysis: International Symposium, ISCMM 2019},
  pages={113--125},
  year={2019},
  organization={Springer}
}
