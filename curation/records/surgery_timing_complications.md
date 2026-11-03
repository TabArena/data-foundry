---
unique_name: surgery_timing_complications
name: Surgery Timing (Cleveland Clinic elective general surgery)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: Website
year: '2016'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://causeweb.org/tshs/surgery-timing/
- https://doi.org/10.1213/ane.0b013e3182315a6d
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and papers, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: 32,001 elective general-surgery patients of the Cleveland Clinic (January 2005 to September 2010) with pre-operative risk factors, procedure category and operation timing, and two outcomes (in-hospital complication, about 13%; 30-day mortality, about 0.4%), released for teaching; the source study tests timing hypotheses, so the prediction use case is ours, and two procedure-level outcome rates must go.
- Source: Sessler, Kurz, Saager and Dalton, "Operation timing and 30-day mortality after elective general surgery", Anesth Analg 113:1423-8 (2011); the rows on the Teaching of Statistics in the Health Sciences portal (causeweb.org/tshs/surgery-timing, posted 2016-07-30, contributed by Amy Nowacki, Cleveland Clinic, cited as "Surgery Timing Dataset", TSHS Resources Portal (2016); files in R, SAS, Stata, SPSS, Minitab and Excel). As published (data dictionary and introduction PDFs, read 2026-10-31): 32,001 x 25: `ahrq_ccs` (AHRQ CCS procedure category), `age`, `gender`, `race`, `asa_status` (I-II, III, IV-VI), `bmi`, eight baseline comorbidity flags (cancer, cardiovascular, dementia, diabetes, digestive, osteoarthritis, psychiatric, pulmonary), `baseline_charlson`, `mortality_rsi` and `complication_rsi` (Risk Stratification Index), `ccsMort30Rate` and `ccsComplicationRate` ("Overall Incidence of 30-day Mortality for Each AHRQ-CCS Procedure Category", and of in-hospital complications), `hour`, `dow`, `month`, `moonphase`, and the outcomes `mort30` and `complication`; "The dataset is cleaned and complete (no missing data except for bmi)". The outcome rates (0.43% deaths, 13% complications) come from press coverage of the paper, not from the data.
- Use case: the surgical and anaesthesia team, before an elective operation, estimates the risk of a complication or of death to plan consent, monitoring and post-operative care; ours: the study "tested the hypotheses that the risk of 30-day mortality ... 1) increases from morning to evening throughout the routine workday; 2) increases from Monday to Friday through the workweek; and 3) is more frequent in July and August" (introduction PDF) and found no such effect; fit approximate. Regime IID: no year or date ships (only month, weekday and hour), so a temporal split cannot be built (SPLIT-7).
- Siblings and duplicates: `core_temperature_surgical_infection` (`TBD -> Yes`, 2; another Cleveland Clinic cohort from the same portal, colorectal surgery and infections: PROV-7); `vitaldb_postoperative_icu_admission` (`TBD -> Yes`, 2), `mover_perioperative_outcomes`, `inspire_surgical_case_duration`, `thoracic_surgery_one_year_survival`, `postoperative_patient_data`: other sources and tasks. No other record of this cohort (grep: causeweb, tshs, sessler, surgery timing). External collections: none found.
- Better data: from the curator's Zotero collection (item 139, the TSHS portal); no further search this round.
- Papers and pages: Sessler et al. 2011 (not read; facts from the portal and press coverage); the TSHS page with its dictionary and introduction.
- Metric: none found for a prediction (the paper is a hypothesis test with risk-adjusted models; the portal lists contingency tables and logistic regression as teaching topics), so the fallback `roc_auc` on `complication`, or on `mort30` (MET-1, MET-8); inputs none.
- Risks for /add-dataset: `ccsMort30Rate` and `ccsComplicationRate` are outcome rates per procedure category; the dictionary does not say where they were computed, and if on this cohort they are target encodings over all rows: drop them and let `ahrq_ccs` carry the procedure (LEAK-10, LEAK-27); the RSI is built from ICD-9 codes, and whether only codes present on admission entered is not stated (USE-3, check the RSI papers); 30-day mortality has about 140 deaths, so `complication` is the stronger target (TP-5, USE-5); the portal's use agreement says "the datasets of the TSHS Resources Portal may have been modified to properly deidentify them" (whether values were altered is a PROV-3 question) and that the portal "is intended for educational purposes only" (terms, EV-4, no criterion).
- Priority: gap 0 (medical & healthcare and binary classification are not thin), use case 0 (ours; the study tests timing effects), source + (a peer-reviewed study and a teaching release with a dictionary), shape + (32,001 patients, 22 mixed inputs), risk - (procedure-level outcome rates, RSI timing, a teaching release that may be altered).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 139: "Dataset – Teaching of Statistics in the Health Sciences".
- as published: patients, 32,001 rows x 25 columns, Jan 2005 - Sep 2010; target: in-hospital complication (composite) or 30-day mortality (binary); access: open.
- Why: real hospital cohort, pre-operative features (ASA, comorbidities, Charlson, RSI risk indices, procedure category, timing)
- Adds: a perioperative risk task of useful size. Risks: ccsMort30Rate / ccsComplicationRate are procedure-level outcome rates (check if computed in-sample, LEAK-10); mortality is rare; portal notes data may be modified for de-identification
