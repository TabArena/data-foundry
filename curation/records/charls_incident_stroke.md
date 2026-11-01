---
unique_name: charls_incident_stroke
name: 'China Health and Retirement Longitudinal Study (CHARLS): new-onset (incident) stroke from the 2011 baseline'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: Website
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.1093/ije/dys203
- https://charls.pku.edu.cn/en/
- https://charls.charlsdata.com/pages/data/111/en.html
- https://doi.org/10.1097/md.0000000000046065
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: a nationally representative Chinese cohort (17,708 people aged 45 or older at the 2011 baseline) with a first stroke reported at later waves, an established stroke-risk screening task; the label has to be built across waves, and access needs a sign-up.
- Source: China Health and Retirement Longitudinal Study (CHARLS), National School of Development, Peking University; cohort profile Zhao, Hu, Smith, Strauss, Yang, Int J Epidemiol 43(1):61-68 (online 2012-12-12, doi 10.1093/ije/dys203): "The national baseline survey for the study was conducted between June 2011 and March 2012 and involved 17 708 respondents"; "CHARLS respondents are followed every 2 years"; "Physical measurements are made at every 2-year follow-up, and blood sample collection is done once in every two follow-up periods". Waves 2011, 2013, 2015, 2018 and 2020 (wave 5 released 2023-11-16), each in modules, plus a Harmonized CHARLS file.
- Use case: a primary-care doctor or a screening programme estimates an adult's stroke risk at a check-up from age, sex, blood pressure, lipids, diabetes, smoking and BMI, to decide on treatment and follow-up. Wang, Zhang, Wang (Medicine 2025, doi 10.1097/md.0000000000046065, PMC12622637) build this from the 2011 baseline and call the model "a practical tool for stroke-risk screening in primary care settings". Fit direct; the outcome is a self-reported doctor's diagnosis. Regime IID over persons of one baseline; spouses are interviewed together, so check a household group (USE-10).
- Siblings and duplicates: `stroke_risk_prediction_dataset_based_on_symptoms` (`No`, AHDS: "constructed based on medical literature") is the record it was found for; `stroke_prediction` (`No`, SEL-7: an undated past stroke) shows why the label must come after the features; `aric_incident_chd` (candidate, ARIC), `framingham_heart_study_fhs` (`Yes`) and `elsa_future_sppb_score` (candidate, the English sister study) are other cohorts, populations or targets, not duplicates. External collections: none known.
- Better data: found as better data for `stroke_risk_prediction_dataset_based_on_symptoms`; no further search this round.
- Papers and pages: the cohort profile; Wang et al. 2025 (6,538 complete cases, a random 70/30 split, ten models); the scout notes other 2025-2026 studies with about 6,800 people (not read).
- Metric: Wang et al. 2025 report accuracy, sensitivity, specificity, F1 and AUC and pick the model by test AUC ("logistic regression achieved the highest test-set area under the curve (0.698; 95% CI: 0.618-0.777)", abstract): `roc_auc`, which is also the fallback (MET-5, MET-8); inputs none.
- Risks for /add-dataset: build the label from the follow-up waves (a first stroke among people free of stroke at baseline) and fix the horizon; deaths and dropouts before a stroke could be reported leave labels unmatured (USE-5, SPLIT-10); keep 2011 baseline features only (LEAK checks on later-wave items); complete cases shrink the sample (Selection Bias check); access by sign-up at charls.charlsdata.com, and the site notes it "is under review for potential modification in compliance with Administration directives" (an access risk; EV-4: no criterion).
- Priority: gap 0 (medical and binary are not thin), use case + (named by the paper that defined the task), source + (cohort profile, institution), shape + (thousands of people, mixed features), risk - (label built across waves, censoring by death).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `stroke_risk_prediction_dataset_based_on_symptoms`.
- as published: 17,708 respondents aged 45+ at the 2011-12 national baseline (cohort profile), followed every 2 years to 2020; physical measures every wave, venous blood in 2011 and 2015. An ML study of incident ...; target: New-onset stroke: a physician-diagnosed stroke first reported at a follow-up wave (2013-2020) by a respondent free of stroke at baseline; access: registration (CHARLS website sign-up with agreement; applications approved in about 3 working days per the FAQ).
- Why: The same task the Kaggle record pretends to cover (stroke risk of an individual from self-reported symptoms, conditions, age and blood pressure), on a real, nationally representative cohort with the outcome measured after the features; an established ML task on this cohort (several 2025-2026 papers). ARIC (BioLINCC, ...
- Adds: Real people instead of data 'constructed from medical literature' (the record's own description); a prospective label instead of a made-up risk score; thousands of participants over nine years. Caveats: stroke is self-reported doctor diagnosis; the panel must be joined across waves and the follow-up window fixed; ...
