---
unique_name: qatar_biobank_t2dm_onset
name: 'Qatar Biobank cohort: type 2 diabetes onset from baseline clinical and DXA data'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
original_source: Other
domain: medical & healthcare
problem_type: Binary Classification
source_links:
- https://www.qphi.org.qa/
- https://arxiv.org/abs/2601.12981
- https://doi.org/10.1186/s12889-015-2522-7
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: incident type 2 diabetes from baseline clinical and DXA data of the Qatar Biobank, but the paper's set is 1,382 participants with a follow-up DXA, its text does not say that people diabetic at baseline were excluded, and the same task has a far larger open cohort in `rich_healthcare_china_incident_diabetes`.
- Source: Qatar Biobank (Qatar Precision Health Institute, Qatar Foundation), described by Al Kuwari et al., "The Qatar Biobank: background and methods", BMC Public Health 2015 (doi 10.1186/s12889-015-2522-7; abstract via Europe PMC): it aims "to follow up these same individuals over the long term", and baseline phenotyping includes "total body dual energy X-ray absorptiometry" and "A panel of 66 clinical biomarkers"; QPHI reports "recruitment of nearly 50,000 participants" (qphi.org.qa). The candidate task comes from Khan, Biswas, Shah, "Early Prediction of Type 2 Diabetes Using Multimodal data and Tabular Transformers", arXiv 2601.12981 (January 2026; QBB project QF-QBB-RES-ACC-00181), read from its PDF. Sec. II.B: "From the initial cohort of 1,941 participants, 1,382 individuals had available follow-up DXA scan data. The study population contains: T2DM cases (n=287) and controls (n=1,095)" (Sec. IV says 1,103 and 279); label "Self-reported T2DM OR HbA1c ≥ 7% OR fasting glucose ≥ 126 mg/dL OR current use of antidiabetic medications/insulin therapy"; features clinical (EHR: LDL, HDL, HbA1c, demographics) and DXA. Access: an application through QPHI's research portal (terms not read).
- Use case: a physician or prevention programme at the baseline visit identifies adults likely to develop type 2 diabetes ("predict the future onset of T2DM", Sec. II.C: "follow-up records were analyzed to identify individuals who developed diabetes over time"); fit approximate, since the text does not say that participants diabetic at baseline were removed, and no follow-up interval is stated. Regime IID, one row per participant.
- Siblings and duplicates: `rich_healthcare_china_incident_diabetes` (a candidate of this run: 211,833 Chinese adults free of diabetes at baseline, open on Dryad) holds the same task; `cdc_diabetes_health_indicators` (`No`, SEL-7) and `knhanes_undiagnosed_diabetes` (a candidate: undiagnosed, not incident, diabetes) are other diabetes tasks. No other QBB record (grep: qatar, qphi, biobank). External collections: none.
- Better data: from the curator's Zotero collection (item 75, the arXiv paper); no further search this round.
- Papers and pages: the QBB cohort paper; the arXiv paper.
- Metric: ROC AUC, the paper's stated choice ("ROC-AUC as the primary and F1-score as the secondary selection metric", Sec. III.B.1), so `roc_auc` from the source (MET-5); inputs none.
- Risks for /add-dataset: participants diabetic at baseline must be excluded, or the label is largely prevalent diabetes given away by baseline HbA1c and glucose (SEL-7, LEAK-10); the paper's selection (a follow-up DXA) and the follow-up length are to be rebuilt from QBB's baseline and follow-up tables (joins); the paper's SMOTE variants, augmentation and forward-fill imputation are its modelling, not the data; 279 or 287 cases, small but scorable.
- Priority: gap 0 (medical & healthcare and binary are not thin), use case 0 (early prediction named without an actor or decision), source + (a documented national cohort), shape + (1,382 participants with clinical and DXA features), risk - (prevalent cases may be in the label; a far larger open cohort holds the same task).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 75: "Early Prediction of Type 2 Diabetes Using Multimodal data and Tabular Transformers".
- as published: paper subset: 1,382 adults (725 men, 657 women) with baseline and follow-up visits, 287 T2DM / 1,095 controls; clinical (EHR) and DXA body-composition columns; full cohort size not stated on the ...; target: T2DM at follow-up (self-report, HbA1c >= 7%, fasting glucose >= 126 mg/dL or antidiabetic medication); access: request.
- Why: incident diabetes with a lab-defined label in a real cohort, from a population thin in the records
- Adds: an incident-T2DM task (baseline to follow-up) with DXA; pima_indians_diabetes_database is No (Ethical) and cdc_diabetes_health_indicators fails SEL-7
