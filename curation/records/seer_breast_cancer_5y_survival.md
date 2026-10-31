---
unique_name: seer_breast_cancer_5y_survival
name: 'SEER breast cancer cohort: five-year breast-cancer-specific survival'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: medical & healthcare
problem_type: Binary Classification
source_links:
- https://seer.cancer.gov/data/access.html
- https://arxiv.org/abs/2509.23268
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: five-year breast-cancer-specific death from the NCI SEER registries (tens of thousands of cases per diagnosis year, features known at diagnosis), the task of PREDICT-style prognosis tools; it is the full-registry version of `seer_breast_cancer_survival` (4,024 SEER cases on IEEE DataPort), so the two are versions of one source.
- Source: National Cancer Institute, SEER Program; the candidate paper uses "SEER*Stat Database: Incidence - SEER Research Data, 17 Registries, Nov 2024 Sub (2000-2022)", released April 2025 (its ref. 35). Access per person through a SEER*Stat account after acknowledging the SEER Research Data Use Agreement and the Treatment Data Limitations; "Each person who will access the data must submit a separate request" (seer.cancer.gov/data/access.html). Case listings per tumour hold the year of diagnosis, age, race, tumour size, nodes, grade, ER and PR, HER2 (from 2010), stage, first-course surgery, radiation and chemotherapy, survival months and cause of death. Cases not counted (SEER*Stat). The candidate paper: Pilgram, Yang, et al., "Transfer Learning and Machine Learning for Training Five Year Survival Prognostic Models in Early Breast Cancer", arXiv 2509.23268 (J Med Internet Res 2026;28:e88665), read from its PDF: trained on the MA.27 trial and validated on a SEER cohort "selected to match the relevant eligibility criteria of MA.27, namely hormone receptor positive postmenopausal women and diagnosed in 2003 ... This cohort comprised 27,064 individuals" (Sec. 2.6).
- Use case: the paper's: "The primary goal of this study was to predict 5-year breast cancer survival, as this represents an early and clinically relevant milestone to guide decision-making" (Sec. 2.4); an oncologist after surgery weighs adjuvant therapy on the estimated risk of dying of breast cancer within five years, as with PREDICT; the event is "breast cancer-related death within a 5-year observation interval" (Table 2). Fit direct for features at diagnosis and first-course treatment. Regime temporal by year of diagnosis (staging and treatment change; a five-year label needs diagnoses at least five years before the data's end).
- Siblings and duplicates: `seer_breast_cancer_survival` (a candidate of this run: 4,024 SEER patients of 2006-2010 on IEEE DataPort, whose note names the full database as "the much larger source for the same task (a version, PROV-6)"): the same task from the same registry, so one of the two enters and the curator decides (PROV-6); `seer_primary_site_from_metastases` (`TBD -> Yes`, 3) is another task on SEER (PROV-7); `metabric_breast_cancer_clinical` and `rotterdam_breast_cancer` are breast-cancer cohorts from other sources (PROV-4). External collections: none found.
- Better data: from the curator's Zotero collection (item 12, the paper); no further search this round.
- Papers and pages: the paper; the SEER access page; the paper's ref. 43 validated PREDICT v3 on "SEER data from more than 860,000 patients (diagnosed 2000–2018)".
- Metric: the paper reports AUC and the integrated calibration index and trains on the latter: "During training, the ICI for 5-years-survival prediction was used as the optimization goal. Calibration has clinically meaningful implications in prognostication tools as probability estimates typically guide decision making" (Sec. 2.4). The argued goal is calibrated probabilities; ICI needs a smoothed calibration curve and is no proper scoring rule, so `log_loss` (or the Brier score) for calibration, or the fallback `roc_auc`, is the call at /add-dataset (MET-5, MET-8); inputs none.
- Risks for /add-dataset: the cohort is ours to define in SEER*Stat (years, stage, histology, one tumour per patient), and the label needs complete five-year follow-up and SEER's cause-specific death classification (USE-5); the radiation and chemotherapy fields are "yes" against "no/unknown" (the Treatment Data Limitations), so they understate treatment; HER2 only from 2010, staging editions change; 2.5% events in MA.27, more over all stages; the agreement's terms on sharing (no criterion, EV-4).
- Priority: gap 0 (medical & healthcare and binary are not thin), use case + (the paper names the prognosis and its use in decisions, with PREDICT as practice), source + (NCI SEER, documented variables), shape + (27,064 cases in one narrow 2003 subgroup alone, mixed types), risk - (a cohort and label to build in SEER*Stat; treatment data limits).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 12: "Transfer Learning and Machine Learning for Training Five Year Survival Prognostic Models ...".
- as published: case listings of all breast cancers in the SEER registries (hundreds of thousands of cases; SEER 17 from 2000); the paper's cohort is 27,064 HR+ postmenopausal women diagnosed in 2003; target: breast-cancer-specific death within 5 years of diagnosis (cause of death and survival months); access: registration.
- Why: the population registry behind many prognosis models; features at diagnosis (age, tumour size, nodes, grade, ER/PR, HER2 from 2010, stage, first-course treatment)
- Adds: a large clinical survival-prognosis task with a temporal split by diagnosis year; the trial cohorts of the paper (MA.27, TEAM) are confidential. Checks: SEER's treatment-data limitations, 5-year follow-up censoring
