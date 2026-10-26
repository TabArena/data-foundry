---
unique_name: predictive_insights_youth_income_prediction_challenge
name: predictive-insights-youth-income-prediction-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2023'
domain: social science
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://zindi.africa/competitions/predictive-insights-youth-income-prediction-challenge/data
- https://zindi.africa/competitions/predictive-insights-youth-income-prediction-challenge
source_row: 889
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 4: whether a young South African is employed one year after a baseline labour-market survey, a clear follow-up target in a thin domain.
- Source: Zindi "Predictive Insights Youth Income Prediction Challenge" (Predictive Insights, 2023-06-08 to 2023-10-01, 648 participants); the data "comes from four rounds of a survey of youth in the South African labour market, conducted at 6-month intervals" (the survey is not named on the page); as published: Train.csv (one row per person, baseline answers plus the target "whether they were employed or not one year later") and Test.csv; numerical, categorical and free-text answers, demographics and school results; rows not checked (Train.csv 405 KB, likely a few thousand).
- Use case: the source: a baseline prediction of young people's employment outcomes, "allowing them to design and test interventions to help youth make a transition into the labour market"; actor a youth-employment programme, moment the baseline interview, decision who gets additional help; fit direct (baseline features, outcome a year later); regime IID by person, with the survey round as a possible temporal axis (to check).
- Siblings and duplicates: none found (grep youth, Predictive Insights); `adult`, `absa_customer_income_prediction_challenge` and `income_prediction_challenge_for_azubian` are different data; external collections: none known.
- Papers and pages: the competition pages read through the Zindi API; no paper; solutions not read.
- Metric: Area Under the Curve, Zindi Evaluation page ("The evaluation metric for this challenge is the Area Under the Curve"), `roc_auc`; deliberate (leaderboard metric, MET-4); inputs none.
- Risks for /add-dataset: the record's name says income but the target is employment; check that every column is from the baseline and none from the follow-up (LEAK); free-text answers (drop or keep as text); the round column decides IID against temporal (SPLIT); the survey's publisher and licence to be traced (PROV-2).
- Priority: gap + (social science is thin), use case + (the source names the decision), source 0 (a competition page only), shape + (mixed types, likely above 1,000 people), risk 0.

A Zindi competition to predict whether a young person in South Africa is employed, a clear real-world binary classification over socio-economic survey/individual records. This is a genuine predictive tabular task with a meaningful target, similar in spirit to the Adult income benchmark. It may have a temporal component if it tracks individuals over survey waves. Suggest TBD -> Yes; a human must confirm the data is a single tabular feature set (not a panel requiring grouping/temporal split), the exact target, and post-processing size.

---

predict if a young person in South Africa is employed
