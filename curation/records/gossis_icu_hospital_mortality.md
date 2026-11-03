---
unique_name: gossis_icu_hospital_mortality
name: 'WiDS Datathon 2020: patient survival in the ICU (MIT GOSSIS extract)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: Kaggle
year: '2020'
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/widsdatathon2020
- https://physionet.org/content/eicu-crd/2.0/
- https://doi.org/10.1097/ccm.0000000000005518
- https://www.kaggle.com/datasets/mitishaagarwal/patient
- https://www.kaggle.com/competitions/widsdatathon2020/data
- https://doi.org/10.13026/530d-1e61
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: the WiDS Datathon 2020 table of 91,713 labelled ICU stays from 200+ US hospitals, scored by ROC AUC on in-hospital death from the first 24 hours; an established task, but the run created a second record for the same competition (`wids_icu_hospital_death`), and the table is a cut of the eICU database whose record proposes the same task (PROV-6).
- Source: WiDS Datathon 2020 on Kaggle (opened 2020-01-10, 951 teams; https://www.kaggle.com/competitions/widsdatathon2020), data from MIT's GOSSIS initiative, also on PhysioNet as "WiDS (Women in Data Science) Datathon 2020: ICU Mortality Prediction" v1.0.0 (2020-01-22; Lee, Raffa, Ghassemi, Pollard, Kalanidhi, Badawi, Matthys, Celi; https://doi.org/10.13026/530d-1e61, credentialed access). As published: training_v2.csv with 91,713 labelled stays and unlabeled.csv with 39,308 stays without labels, "more than 130,000 hospital Intensive Care Unit (ICU) visits"; the data dictionary (read) lists 188 variables: vitals 52, labs 60, blood gas 16, APACHE covariates 28, comorbidities 8, demographics 16 (with the target), identifiers 3 (`encounter_id`, `hospital_id`, `patient_id`), APACHE groupings 2, two APACHE IVa death probabilities and one GOSSIS example prediction; target `hospital_death` ("Whether the patient died during this hospitalization"). The US cohort is very probably the eICU-CRD part of GOSSIS (2014-2015; not stated on the PhysioNet page).
- Use case: "create a model that uses data from the first 24 hours of intensive care to predict patient survival" (PhysioNet): the prediction point is stated, the actor is not; the GOSSIS and APACHE use is an objective severity estimate for risk adjustment and ICU benchmarking (Raffa et al. 2022, not read); fit direct for that estimate at 24 h; regime IID (as `wids_diabetes_mellitus` shipped) or grouped by `hospital_id` (a score used at a new hospital), to decide; `patient_id` may repeat.
- Siblings and duplicates: `wids_icu_hospital_death` (created by the same run, screening batch 53, for the same Kaggle competition and target: the same dataset, PROV-4; one of the two should become `Duplicate`); `eicu_collaborative_research_database` (`TBD -> 2nd Tier`, priority 3, whose screening proposes ICU mortality at 24 h: this table is a cut of it with the task defined, PROV-6, the curator decides which enters); `eicu_crd_2020_2021` (unscreened, a newer eICU release); `wids_diabetes_mellitus` (`Yes`, WiDS 2021, the GOSSIS table with diabetes as target: overlapping stays and a distinct task, PROV-7); `2_month_survival_rate_prediction` (`Yes`, SUPPORT: another source). External collections: TabBank's sheet marks the Kaggle copy "Patient Survival Prediction" (https://www.kaggle.com/datasets/mitishaagarwal/patient) as a simplified version (the run's note).
- Better data: no new search; found as better data for `2_month_survival_rate_prediction`, `eicu_collaborative_research_database` and `wids_diabetes_mellitus`, and through the curator's Zotero collection (items 47, "TabBank", and 80, "PhysioNet").
- Papers and pages: the Kaggle competition; the PhysioNet page (read); Raffa et al. 2022, GOSSIS (Crit Care Med, https://doi.org/10.1097/ccm.0000000000005518, not read); top solutions not read.
- Metric: ROC AUC (Kaggle API evaluationMetric "Area Under Receiver Operating Characteristic Curve"; PhysioNet: scored "on a Kaggle leaderboard using AUROC"), a leaderboard metric (MET-4): `roc_auc`. Inputs: none.
- Risks for /add-dataset: `apache_4a_hospital_death_prob` and `apache_4a_icu_death_prob` are APACHE IVa model outputs from first-day data (known at 24 h, not fit on this table; keep as a reference or drop, to decide); the duplicate record and the eICU version (PROV-4, PROV-6); only the 91,713 labelled stays can ship; readmitted stays and repeated patients (`readmission_status`, `patient_id`); the Kaggle rules and the PhysioNet data use agreement (no criterion, EV-4).
- Priority: gap 0 (medical, binary, IID and grouped are not thin), use case 0 (the source states the prediction point, not the actor or decision), source + (PhysioNet page with authors, data dictionary, GOSSIS paper), shape + (91,713 stays, about 186 columns, hospitals), risk - (a duplicate record and an eICU version to settle).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `2_month_survival_rate_prediction`, `eicu_collaborative_research_database`, `wids_diabetes_mellitus`; a related task next to `wids_diabetes_mellitus`; the curator's Zotero collection, item 47: "TabBank"; the curator's Zotero collection, item 80: "PhysioNet".
- as published: training_v2.csv: 91,713 ICU encounters labelled (about 186 columns per the dictionary; not counted), from 'more than 130,000' ICU visits over one year in 200+ US hospitals (eICU, 2014-2015); ...; target: hospital_death (death before hospital discharge), from data of the first 24 hours of ICU care; ROC AUC; access: registration.
- Why: same quantity as SUPPORT's (short-term death of seriously ill hospitalized adults) from features of the same kind (APACHE physiology, age, diagnosis group, comorbidities, admission source) at an early prediction point; Knaus authored both APACHE and the SUPPORT model | Same GOSSIS first-24h ICU table as ...
- Adds: 10x more patients (91,713 vs 9,105), 2014-2015 instead of 1989-1994, 200+ hospitals instead of 5, hospital_id and icu_id for a grouped split; caveats: in-hospital death instead of death by day 60, ICU only, ships APACHE IV death probabilities (drop or keep as a reference); data use limited to the datathon by the ...
- A newer release of the same source as the record(s) named above (PROV-6): the curator decides which one enters.

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: the same WiDS Datathon 2020 competition (`wids_icu_hospital_death`; PROV-4). The curator keeps one, or both as distinct tasks.
