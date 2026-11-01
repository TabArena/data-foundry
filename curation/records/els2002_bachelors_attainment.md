---
unique_name: els2002_bachelors_attainment
name: Education Longitudinal Study of 2002 (ELS:2002), base year to third follow-up public-use file
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: education
problem_type: Binary Classification
source_links:
- https://nces.ed.gov/surveys/els2002/avail_data.asp
- https://doi.org/10.1177/23328584241258741
- https://arxiv.org/abs/2301.03784
- https://nces.ed.gov/datalab/onlinecodebook
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: NCES's national cohort of 2002 high-school sophomores followed to 2012, with bachelor's degree attainment as the outcome; Gándara et al. (AERA Open 2024) model it for 15,244 students with 27 predictors and name the colleges' decisions; a wave cut decides the features.
- Source: National Center for Education Statistics, Education Longitudinal Study of 2002 (ELS:2002): it "follows a nationally representative cohort of 10th-graders in 2002 and 12th-graders in 2004"; base year 2002, first follow-up 2004, high-school transcripts 2005 (restricted-use only), second follow-up 2006, third follow-up 2012, postsecondary transcripts 2013 (study page); "Thirty-three percent earned a bachelor's degree or higher" by 2012. Public-use data through the Online Codebook, where "each one includes all prior follow-ups", up to the third follow-up; restricted-use data under licence (avail_data.asp). Student and school counts are not stated on the pages read; the year waits for the public-use file we pin.
- Use case: a college's student-success model predicts degree completion to inform admissions, budgeting and student-success interventions (Gándara, Anahideh, Ison, Picchiarini, "Inside the Black Box: Detecting and Mitigating Algorithmic Bias Across Racialized Groups in College Student-Success Prediction", AERA Open 10, 2024, abstract); they keep "students who attended four-year postsecondary institutions" and "label students with a bachelor's degree and higher as the favorable outcome" at the third follow-up (Data Sources). Fit approximate: a national survey sample stands in for a college's own students; their features (demographics, socioeconomic traits, grades, college preparation, high-school context) are what a college knows at entry. Regime grouped by high school (the survey samples students within schools) or IID as in the paper (80:20 random, stratified by outcome and race, 30 repeats); to decide.
- Siblings and duplicates: `hsls09_postsecondary_enrollment` (`TBD -> Yes`, 4) and `hsls09_secondary_student_achievement` (`TBD -> Yes`, 3): the later NCES cohort with other outcomes, a different dataset (PROV-7); `predict_students_dropout_and_academic_success` (`Yes`) and `upv_university_student_dropout`: university records of other countries. External collections: none found.
- Better data: from the gap scout for education; no further search this round.
- Papers and pages: the NCES study and data pages; Gándara et al. 2024 (text read from the arXiv PDF, Data Sources and Analysis Methods; the variable list is in their Appendix C, not read).
- Metric: Gándara et al. report accuracy with fairness measures (parity of false negative rates and others), no threshold or costs fixed (MET-6), so the fallback `roc_auc` (MET-8); inputs none (survey weights ship, no source scores with them).
- Risks for /add-dataset: hundreds of variables across waves: cut the features at the prediction point (college entry, the 2004 or 2006 wave) and drop every later postsecondary variable (LEAK); the four-year-institution filter uses attendance known only after high school (decide the prediction point, USE-3, USE-7); the public-use file coarsens or suppresses variables; heavy missingness (the paper drops incomplete rows); race and ethnicity as features (the paper's question; the curator decides); a cohort of 2002 to 2012.
- Priority: gap + (education), use case + (a published ML study names the decisions), source + (NCES with codebook), shape + (15,244 students, 27 mixed predictors, schools), risk - (the wave cut and the filter).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the gap scout for education.
- as published: a national sample of 2002 high school sophomores followed in 2004, 2006 and 2012; Gándara et al. 2024 model 15,244 students; the public-use file holds all four waves (total rows and schools to ...; target: bachelor's degree attainment by 2012; access: open.
- Why: a strong federal source with a codebook, open download, a measured long-run outcome and a published ML use of the task that names the decision
- Adds: a degree-completion task grouped by school; an older sibling study of HSLS:09 in the same NCES program with a different cohort and outcome, so the curator may take one or both
