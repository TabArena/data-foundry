---
unique_name: framingham_heart_study_fhs
name: Framingham Heart Study (FHS)
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
tags:
- New IID
collections:
- New (BeyondArena)
original_source: GOV Website
year: '2013'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/christofel04/cardiovascular-study-dataset-predict-heart-disea/data
- https://www.kaggle.com/datasets/aasheesh200/framingham-heart-study-dataset
- https://www.framinghamheartstudy.org/fhs-for-researchers/data-available-overview/
- https://www.nhlbi.nih.gov/science/framingham-heart-study-fhs
- https://www.framinghamheartstudy.org/fhs-risk-functions/hard-coronary-heart-disease-10-year-risk/
v2_path: datasets/_dev/tabarena-v0pt2/framingham_heart_study_fhs/dataset.py
source_row: 667
type_adapter_id: curation-record-v1
---

## Comments

Likely use data from Kaggle

A bit hard to parse what the origin is and where the Kaggle data was downloaded from, but we can use it

**Assessment (AI, 2026-10-07):** All three Kaggle uploads are `framingham.csv` from MIT's 15.071 The Analytics Edge (OCW Spring 2017; aasheesh200 is byte-identical). Its 4,240 rows are the baseline exam (period 1, PREVCHD = 0) of the NHLBI BioLINCC Framingham teaching dataset; all 15 features match row for row. MIT's `TenYearCHD` equals TIMECHD < 10 years in all 4,240 rows, but TIMECHD is the censor date for participants without an event (documentation, p. 4). So 265 of its 644 positives had no CHD: 249 died of other causes and 16 were lost to follow-up. The v2 definition reads the teaching data (CRAN riskCommunicator) and rebuilds the label: 4,224 participants, 379 with CHD. BioLINCC calls teaching data "completely unsuitable for publication purposes".

**Assessment (AI, 2026-10-20):** priority 3 for the review of the added dataset: gap -, use case +, source +, shape +, risk - (Issue 3: teaching data perturbed by undocumented anonymisation, unsuitable for publication per BioLINCC). Classic CHD risk task with the label rebuilt (41% of the Kaggle positives were wrong), but it rests on anonymised teaching data.

**Assessment (AI, 2026-10-20):** review panel (full): ship after changes, with the anonymised teaching data recorded as a PROV-3 case and the rebuilt label as a PROV-13 repair (curator's calls); the endpoint (ANYCHD or hard CHD) stays a weighing call. Applied: the row names the first exam of about 1956, the use case a patient's first assessment, `known` the missing HDL, `fit_reason` the pre-statin era and what the anonymisation check shows (no added noise; permutation untestable), the endpoint's reason the FHS 10-year CHD risk page instead of MIT's course, plus notes on the terms, relatives and cigsPerDay heaping. Priority 3: gap - (no thin domain, problem type or regime), use case + (the classic FHS risk score, fit direct), source + (BioLINCC documentation), shape + (4,224 participants, 15 features), risk - (anonymisation by undocumented methods that cannot be fully tested, PROV-3).

CC (2026-10-21, Lennart): agree to amend PROV-3 (values the owner perturbed for privacy, with no measurable damage, are kept with a note of what was checked; this dataset is its case), but also add a note about selection bias in the curation record here. Agree to amend PROV-14: the rebuilt label is a repair and stays under this record.

**Assessment (AI, 2026-10-21):** selection bias of the teaching subset. BioLINCC's documentation (2021a, p. 1) calls the file "a subset of the data collected as part of the Framingham study" on 4,434 participants, of the 5,209 enrolled in 1948; NHLBI's teaching page (2005) says "a large subset of the original Framingham cohort participants". How the 4,434 were chosen is not documented. Period 1 is about 1956, some eight years after enrolment, so people who died or left before that exam are likely missing (a survivor selection), and Nahhas (App. A.6) names "random visit selection" among the anonymisation methods. The task therefore stands for this subset of a 1948 town cohort, not for the whole cohort; no test on the file can measure the selection. Noted in the definition's notes (Selection bullet) and in REVIEW.md issue 3.

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: male, currentSmoker, BPMeds, prevalentStroke, prevalentHyp, diabetes.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — the teaching dataset defines no task or metric; the 10-year risk context points to the C statistic, which equals roc_auc here.

## Reference

https://www.nhlbi.nih.gov/sites/default/files/media/docs/risk-assessment.pdf
