---
unique_name: script_carpediem_icu
name: 'SCRIPT CarpeDiem: per-ICU-day clinical parameters and pneumonia adjudication for critically ill patients'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- Non-IID (Grouped)
- AI-Filled (Verify)
original_source: Other
year: '2023'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
original_data_state: One Table
source_links:
- https://physionet.org/content/script-carpediem-dataset/
- https://doi.org/10.13026/5phr-4r89
- https://doi.org/10.13026/1qke-qx33
- https://doi.org/10.64898/2026.03.10.26348076
- https://arxiv.org/abs/2509.07330
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: a curated single-CSV ICU cohort (704 ventilated patients with suspected pneumonia at one hospital, 21,931 patient-days, 2018-2023) with physician-adjudicated pneumonia episodes and discharge outcomes; real and documented, but small in patients, single-centre, and published to describe daily trajectories, with prediction only suggested as future work.
- Source: Markov, Gao, Stoeger, et al., NU SCRIPT Study Investigators, "SCRIPT CarpeDiem Dataset: demographics, outcomes, and per-day clinical parameters for critically ill patients with suspected pneumonia", PhysioNet, first published 2023-03-13 as v1.1.0 (doi 10.13026/5phr-4r89: "12,495 patient-ICU-days from 585 patients enrolled in the SCRIPT study between June 2018 and March 2022"); current v1.9.1 of 2026-08-13 (doi 10.13026/1qke-qx33): "21,931 patient-hospital-days from 704 patients", enrolled June 2018 to May 2023 at Northwestern Memorial Hospital (named in the acknowledgements). Data descriptor: Gao et al., medRxiv 2026 (doi 10.64898/2026.03.10.26348076). As published (v1.9.1 page): one CSV, one row per patient-day: 46 demographic and outcome columns (age, sex, BMI, admission source, APS, SOFA, discharge disposition Home, Rehab, SNF, LTACH, Hospice or Died, cumulative ICU and intubation days, tracheostomy), 113 daily parameters (vitals, ventilator settings, labs, SOFA components, ECMO, dialysis; medications and BAL results since v1.8) and 38 adjudication columns (pneumonia group, episode type, cure: 390 cured, 168 indeterminate, 277 not cured). 45% had an unfavourable outcome (hospice or death). Access: PhysioNet credentialed, CITI training and the Credentialed Health Data Use Agreement 1.5.0.
- Use case: for example, the ICU team on daily rounds estimates whether a ventilated pneumonia patient will die or go to hospice, or whether a pneumonia episode will be cured, to plan care (ours to state: the page reports unsupervised clustering into 14 daily states and suggests outcome prediction as future work). Fit approximate. Regime grouped by patient (`is_repeat_hospitalization` flags readmissions, and the page advises care with train and test splits and patient-level analyses).
- Siblings and duplicates: `mimic_iv` (`TBD -> 2nd Tier`, 2), `eicu_collaborative_research_database` (`TBD -> 2nd Tier`, 3), `amsterdamumcdb` (`TBD -> 2nd Tier`, 2) and `wids_icu_hospital_death` (a candidate) are larger multi-centre ICU sources with other cohorts (PROV-7); no other SCRIPT record (grep: carpediem, SCRIPT, pneumonia). External collections: none; the GDP paper (arXiv 2509.07330) uses it among its cohorts.
- Better data: from the curator's Zotero collection (item 23, the GDP paper); no further search this round.
- Papers and pages: the PhysioNet pages (v1.1.0, v1.9.1); the medRxiv descriptor; Gao et al., medRxiv 2022 (doi 10.1101/2022.09.23.22280118), the clustering study the v1.1.0 page cites; the GDP paper (abstract only, which names no dataset or metric).
- Metric: none found (the PhysioNet pages and the medRxiv abstract define no prediction task; the GDP abstract names no metric), so the fallback, `roc_auc` for a binary outcome or `log_loss` for the three-way cure (MET-1, MET-11); inputs none.
- Risks for /add-dataset: choose one target and prediction point (an outcome from the first ICU day, or a per-day outcome) (USE-1, USE-3); the outcome columns repeat on every day row, and cumulative ICU and intubation days, tracheostomy and later adjudications are known only after the day (LEAK-10); a patient's days stay in one fold; lung-transplant recipients are coded as died; 704 patients are the units.
- Priority: gap 0 (medical, binary and grouped are not thin), use case 0 (no prediction stated by the source), source + (PhysioNet with a data descriptor), shape 0 (704 patients, under about 1,000 units, though 21,931 day rows with 113 parameters), risk - (outcome columns on every row; a target to choose).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 23: "General Demographic Foundation Models for Enhancing Predictive Performance Across Diseases".
- as published: v1.1.0: 585 patients, 12,495 patient-ICU-days, 20 demographic/outcome + 47 daily + 5 adjudication columns, enrolment June 2018 - March 2022. v1.9.1: 704 patients, 21,931 patient-days, 113 clinical ...; target: discharge disposition in six categories (hospice or death = unfavourable, 45% of the cohort), pneumonia episode outcome (cured 317 / indeterminate 131 / not ...; access: request.
- Why: a single curated CSV of real ICU care with physician-adjudicated outcomes, grouped by patient and ordered in time; the task is the one the GDP paper runs (LightGBM on the aggregated table)
- Adds: an ICU outcome table that needs no database wrangling, unlike mimic_iv and icu_length_of_stay_icu_mortality; day-level adjudication labels that MIMIC does not carry
