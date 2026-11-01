---
unique_name: thoracic_surgery_one_year_survival
name: Thoracic Surgery Data (post-operative life expectancy in lung cancer patients)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Tiny Data
original_source: UCI
year: '2013'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/277/thoracic+surgery+data
- https://www.openml.org/d/1506
- https://doi.org/10.1016/j.asoc.2013.07.016
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: a real surgical-outcome task with pre-operative features from one Polish centre (470 patients, 70 deaths within a year); a tiny-data task, small but not `Too Small`, with the paper's metric unread.
- Source: Zięba, Tomczak, Lubicz and Świątek, "Boosted SVM for extracting rules from imbalanced data in application to prediction of the post-operative life expectancy in the lung cancer patients", Applied Soft Computing 14:99-108 (2014, doi 10.1016/j.asoc.2013.07.016); donated to UCI on 2013-12-11 (dataset 277, CC BY 4.0). UCI: the data "was collected retrospectively at Wroclaw Thoracic Surgery Centre for patients who underwent major lung resections for primary lung cancer in the years 2007–2011", part of the National Lung Cancer Registry (Institute of Tuberculosis and Pulmonary Diseases, Warsaw). As published: 470 patients x 16 features (DGN diagnosis code, FVC, FEV1, Zubrod performance status, pain, haemoptysis, dyspnoea, cough and weakness before surgery, clinical T category, type 2 diabetes, MI within six months, peripheral arterial disease, smoking, asthma, age) and Risk1Yr (death within one year); no missing values; 70 deaths and 400 survivors (OpenML 1506 qualities).
- Use case: a thoracic surgeon or tumour board weighs the one-year mortality risk from pre-operative data when deciding on a major lung resection; the paper's title names the prediction (post-operative life expectancy) but who acts on it was not read, so the use case point is not given; fit direct at the pre-operative assessment. Only operated patients have an outcome, which holds for every dataset of the task (no `Selection Bias`, selection.md). Regime IID: one centre, 2007-2011, no dates in the data.
- Siblings and duplicates: no record (grep for thoracic, lung resection, Wroclaw); `vitaldb_postoperative_icu_admission` is another surgical outcome (PROV-7). Copies: OpenML 1506 (`thoracic-surgery`, columns renamed V1-V16), 4329 (`thoracic_surgery`) and 46595 (`Thoracic_Surgery_Data`, 2025). External collections: CLIMB, a class-imbalance benchmark (arXiv 2505.17451; moved here from the links, PROV-12).
- Better data: from the curator's Zotero collection (item 1); no further search this round.
- Papers and pages: Zięba et al. 2014 (paywalled, no abstract on Crossref; not read).
- Metric: not read (paywalled). A rule learner for imbalanced data usually reports G-mean with sensitivity and specificity, threshold metrics without a fixed decision (MET-5, MET-6), so the fallback `roc_auc` unless the paper names one deliberate criterion. Inputs none.
- Risks for /add-dataset: 70 deaths, about 14 per test fold in 5-fold CV (tiny data, not `Too Small` under TP-5; musk keeps 13 per fold); check FVC and FEV1 ranges for entry errors (FEV1 above FVC); many rare DGN codes; surgical practice of 2007-2011.
- Priority: gap 0 (medical, binary and IID are covered), use case 0 (not read in the paper), source + (paper, UCI, national registry), shape 0 (470 patients), no extra risk.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 1: "CLIMB: Class-imbalanced Learning Benchmark on Tabular Data".
- as published: 470 patients x 16 pre-operative features (DGN, PRE4-PRE32, AGE), major lung resections for primary lung cancer 2007-2011, 70 deaths; target: Risk1Yr: death within one year after surgery (binary); access: open.
- Why: A real clinical outcome with features known before surgery. CLIMB uses it and we have no record. OpenML has duplicates: 4329 and 46595.
- Adds: A tiny surgical-outcome task. It is small: about 14 deaths per test fold in 5-fold CV.
