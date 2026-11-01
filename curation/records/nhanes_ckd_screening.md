---
unique_name: nhanes_ckd_screening
name: NHANES chronic kidney disease screening (CKD from eGFR and urine albumin, predicted without kidney labs)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
original_source: GOV Website
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://wwwn.cdc.gov/nchs/nhanes/
- https://doi.org/10.1001/archinte.167.4.374
- https://pubmed.ncbi.nlm.nih.gov/17325299/
- https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/ALB_CR_J.htm
- https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/ALB_CR_L.htm
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: chronic kidney disease screening from interview and exam items on NHANES, the task SCORED published (Bang et al. 2007, 8,530 adults, AUC 0.88); the label comes from kidney labs kept out of the features, so it is the screening task the trivial UCI file `chronic_kidney_disease` could not be.
- Source: CDC/NCHS continuous NHANES public-use files (1999 onward, 2-year cycles; serum creatinine in the biochemistry profile, urine albumin and creatinine in ALB_CR, e.g. ALB_CR_L for 2021-2023: 8,493 records, 8,153 with the albumin-creatinine ratio, ages 3 and over). The task as published: Bang et al., "SCreening for Occult REnal Disease (SCORED)", Arch Intern Med 167(4):374-381, 2007 (abstract, read through Europe PMC): "8530 adult participants in the National Health and Nutrition Examination Surveys" of 1999-2000 and 2001-2002; "Chronic kidney disease was defined as a glomerular filtration rate less than 60 mL/min per 1.73 m(2)"; predictors age, female sex, hypertension, diabetes, peripheral vascular disease, cardiovascular disease, congestive heart failure, proteinuria and anaemia. Rows over 1999-2023 not counted (tens of thousands of adults expected).
- Use case: a primary-care clinician or community screening programme decides whom to send for a creatinine and urine albumin test from the interview and the exam; SCORED "may be a useful tool to identify individuals with a high likelihood of occult kidney disease", with "A score of 4 or greater ... as a cutoff point for screening" (abstract); fit direct; regime temporal by survey cycle, as `nhanes_undiagnosed_diabetes`.
- Siblings and duplicates: `chronic_kidney_disease` (`No`, Trivial, Tiny Data: 400 patients, the kidney labs define the label); `nhanes_undiagnosed_diabetes` (the same construction on NHANES, a distinct task, PROV-7) and the run's other NHANES candidates (distinct targets). External collections: none known (not searched: the run's web search budget was used up).
- Better data: found as better data for `chronic_kidney_disease`, and from the curator's Zotero collection (items 161 and 263, not opened here); no further search this round.
- Papers and pages: SCORED (doi 10.1001/archinte.167.4.374; external validation in ARIC, AUC 0.71). Related work on the same data: Saxena, Potturu and Nagraj, medRxiv 2026 (https://doi.org/10.64898/2026.04.03.26349862), albuminuria (UACR of 30 mg/g or more) among 687 adults with eGFR 30-59 from NHANES 2015-2018, logistic regression AUC 0.723; another target, moved from the source links to here (PROV-12).
- Metric: SCORED reports the area under the ROC curve (0.88 internal, 0.71 external) and sensitivity 92% and specificity 68% at its own point-score cutoff of 4; that cutoff belongs to SCORED's integer score, not to a probability any model outputs (MET-6), so `roc_auc`, SCORED's discrimination statistic (MET-5, MET-8); inputs none.
- Risks for /add-dataset: a label we construct (the eGFR equation, CKD-EPI 2021 or SCORED's; eGFR below 60 alone, or with UACR of 30 or more, in which case proteinuria and urine albumin leave the features, LEAK-10); serum creatinine calibration differs across cycles (the scout's note; the cycle notes not read); the urine albumin method changed in 2021-2023 (new results "6.20% higher than values measured with the old method", ALB_CR_L); people who already know of their kidney disease (the kidney questionnaire) should leave a screening task (SEL-7); heavy joins per cycle; survey weights not used.
- Priority: gap 0 (medical, binary and temporal are not thin), use case + (SCORED names the screening decision and a cutoff), source + (NCHS documentation and a published task), shape + (tens of thousands of adults, mixed features, survey cycles), risk - (a constructed label and cross-cycle calibration).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `chronic_kidney_disease`; the curator's Zotero collection, item 161: "A Hybrid Machine Learning Framework for Early Prediction of Chronic Kidney Disease ..."; the curator's Zotero collection, item 263: "LLM4CKD: Large Language Models for Early Stage Chronic Kidney Disease Screening".
- as published: One row per adult. SCORED used 8,530 adults from NHANES 1999-2002 (abstract). Every cycle since has serum creatinine and urine albumin/creatinine, so 1999-2023 should come to several tens of ...; target: CKD: eGFR below 60 mL/min/1.73 m2 (SCORED: 'Chronic kidney disease was defined as a glomerular filtration rate less than 60 mL/min per 1.73 m(2)'), optionally ...; access: open.
- Why: Same target as chronic_kidney_disease (a CKD diagnosis), with features of the same kind as the UCI file's non-renal columns: age, blood pressure, diabetes, hypertension, CAD/CVD, anaemia or haemoglobin, glucose, plus heart failure, peripheral vascular disease and BMI. SCORED's predictors were 'age, sex, hypertension, ...
- Adds: The UCI file (400 patients, one Indian hospital, 2015) is Trivial: its serum creatinine, urea and albumin define the label. On NHANES the label comes from the kidney labs, which are left out of the features, so the task is the screening one and not a restatement of the label. It adds tens of thousands of adults, a ...
