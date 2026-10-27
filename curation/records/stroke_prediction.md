---
unique_name: stroke_prediction
name: Stroke Prediction
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
- Data Quality Issue
tags:
- New IID
- 2nd Tier / Scientific Discovery
collections:
- New (BeyondArena)
original_source: Other
year: '2018'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.analyticsvidhya.com/datahack/contest/mckinsey-analytics-online-hackathon/
- https://doi.org/10.17632/x8ygrw87jw.1
source_row: 669
type_adapter_id: curation-record-v1
---

## Comments

Unclear if data is fake (https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset/discussion/218525)

When asked for the dataset source, the uploader repeatedly says that it is confidential, without commenting whether it's real or not. Also, he says "you should only use this dataset for educational purposes, not for research or economical purposes."

The data looks reasonable to use, is used a lot, and might be real. We can use it for now and filter later if needed

**Assessment (AI, 2026-10-07):** Source traced: the Kaggle file is a cut of the training file of the McKinsey Analytics Online Hackathon (Analytics Vidhya DataHack, 2018-04-14; 43,400 patients, 783 strokes; byte-identical on Mendeley Data, doi:10.17632/x8ygrw87jw.1). The file is partly generated or altered: Residence_type, ever_married and work_type carry nothing beyond age (likelihood-ratio p 0.39-0.88; BRFSS 2015 data of the same size shows clear dependence). Women and men aged 25-29 are married alike (45.0% each; BRFSS 53.8% / 40.3%), Residence_type is a coin flip independent of every column, and glucose is flat from 55 to 65 mg/dL with nothing lower. The clinical columns look real. A missing BMI follows the stroke (adjusted odds ratio 3.7). Suggest No + AHDS / Data Quality Issue.

**Assessment (AI, 2026-10-20):** priority 1 for the review of the added dataset: gap -, use case -, source -, shape +, risk - (Issue 1: partly generated or altered; run recommends No + AHDS / Data Quality Issue). Popular but partly generated hackathon data with an undated label and age-dominated signal; recommended for rejection.

**Assessment (AI, 2026-10-20):** after the review panel, recommend `No` + `No Good Target / Scientific Discovery` (SEL-7, SEL-3; the curator has the call): the label is a stroke the patient has already had, undated, the mechanism of the retired cdc_diabetes_health_indicators; keeping it needs an amendment of SEL-7 (REVIEW.md issue 5). The source is traced (the contest's 2018 training file, byte-identical on Mendeley Data, doi:10.17632/x8ygrw87jw.1). bmi is dropped (a missing BMI follows the stroke, adjusted odds ratio 3.68), and ever_married, work_type and Residence_type are dropped (nothing beyond age, PROV-3); the glucose and age marks left in shipped columns wait on the PROV-3 evidence standard (issue 1). Priority 1: gap -, use case - (fit approximate; the contest asks for future risk, the label records a past stroke), source - (contest page with a short data dictionary; no place, period or statement of how the file was made), shape + (43,400 patients, 6 mixed features), risk - (the recommendation not to ship).

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: hypertension, heart_disease.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — AUC-ROC of the McKinsey Analytics Online Hackathon (Healthcare Analytics, 2018).

CC (2026-10-26, Lennart): the record's year (2018) and source links (the contest page and the Mendeley Data deposit) take the definition's values; the Kaggle link it had, https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset, is a cut of the contest file.

CC (2026-10-26, Lennart): the declared metric is checked as declared.

CC (2026-10-26, Lennart): "This looks too bad, dont ship it" (verdict on the page).

**Assessment (AI, 2026-10-26):** retired under SEL-7 as cdc_diabetes_health_indicators: the label is a stroke already had, undated, so no decision is made with the prediction (issue 5); three columns carry nothing beyond age and look generated, and glucose and age show marks a real record would not (issue 1). `No` + `No Good Target / Scientific Discovery` and `Data Quality Issue` (replacing `Missing source information`). A screening task would need a first stroke within a horizon, from dated records. The folder left the working copy (in git history before this change).

## Reference

Kaggle
