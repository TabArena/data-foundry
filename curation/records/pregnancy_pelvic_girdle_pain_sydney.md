---
unique_name: pregnancy_pelvic_girdle_pain_sydney
name: Pelvic girdle pain in pregnancy dataset
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- No Good Target / Scientific Discovery
tags:
- AI-Filled (Verify)
original_source: Other
year: '2023'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://doi.org/10.26183/tqg2-2x04
- https://researchers.westernsydney.edu.au/en/datasets/pelvic-girdle-pain-in-pregnancy-dataset/
- https://doi.org/10.1097/BRS.0000000000003954
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: a documented study of 780 pregnant women with pelvic girdle pain classified by examination, but the label is the pain a woman has at the visit, from a cross-sectional association study, and the data is on request only.
- Source: Ceprnja and Gupta, "Pelvic girdle pain in pregnancy dataset", Western Sydney University, doi 10.26183/tqg2-2x04 (made available 2023; "Cross-sectional study conducted between December 2017 and October 2019"); paper Ceprnja, Chipchase, Fahey, Liamputtong, Gupta, "Prevalence and factors associated with pelvic girdle pain during pregnancy in Australian women: a cross-sectional study", Spine 46(14):944-949, 2021 (PMC8221721, read). As published: 780 randomly sampled women at 14-38 weeks attending antenatal care at a Sydney tertiary hospital; gestational age, parity, pregnancy type, height, weight, BMI, marital status, education, country of birth, ethnicity, personal history of low back or pelvic girdle pain, family history of PPGP, work hours, type and satisfaction, hours lying, sitting, standing and walking the previous day. Outcome: "point-prevalence of PPGP", classified by the European guidelines (self-reported pelvic girdle pain, difficulty with daily activities, and at least two of four positive provocation tests on one side); 344 of 780 (44.1%) positive. Access: "a de-identified version of the data can be discussed by contacting the author"; no licence stated (EV-4, no criterion).
- Use case: the authors propose adding prior back or pelvic pain, family history, parity, gestational age and standing time to routine antenatal assessment to identify women at risk (Discussion; Australia has no routine screening for PPGP). Fit approximate: the label is pain the woman already reports at the same visit (the first criterion is self-reported pain), not a later onset, so every positive knows she has pain; that is the SEL-7 question, kept as the concern marker `No Good Target / Scientific Discovery` rather than a reject, since the source names a screening use. Regime IID (one visit per woman).
- Siblings and duplicates: `backache` (TBD -> 2nd Tier, `Missing source information`; the 180-case StatLib file); no other record of this study (grep pelvic, pregnan). Another source, not a duplicate (PROV-4). External collections: none found.
- Better data: found as better data for `backache`; no further search this round.
- Papers and pages: the Spine paper; the study protocol in BMJ Open 2017 (e018334, PMC5695351, not read).
- Metric: the paper fits univariate and multivariable logistic models and reports Nagelkerke R2 and the ROC AUC (Statistical analysis); the models for all women were weak, and AUC 0.75-0.76 came only in a secondary subgroup of 358. Two statistics of an association study, no ranked criterion, so the fallback `roc_auc` (MET-5, MET-8); inputs none.
- Risks for /add-dataset: access by request only (no public file); the label mixes current pain with examination findings (USE-5); activity hours of the previous day may follow the pain rather than precede it (LEAK-10); one hospital; about 20 variables, so a tiny-data task.
- Priority: gap 0 (medical & healthcare, binary not thin), use case 0 (named by the authors, but the fit is approximate), source + (paper and institutional data record), shape 0 (780 women), risk - (a label the positives already know; data on request).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `backache`.
- as published: 780 pregnant women (14-38 weeks' gestation) attending antenatal care at a tertiary referral hospital in Sydney; one cross-sectional record each; variables: sociodemographics, country of birth, ...; target: pregnancy-related pelvic girdle pain present (binary), classified by the recommended guidelines including a physical examination; access: request.
- Why: the backache task (does a pregnant woman suffer back or pelvic pain, from her history, body and work) with the same kind of patient characteristics known at the antenatal visit, and the pain measured better (clinical examination instead of a recall score)
- Adds: 4.3 times the women of the 180-case StatLib file, a documented source and paper instead of an untraceable book table with no variable names; still small and on request (the page: 'a de-identified version of the data can be discussed by contacting the author'; licence not stated)
