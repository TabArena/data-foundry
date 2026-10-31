---
unique_name: pulse_oximetry_sao2_correction
name: 'Pulse-oximetry correction: MIT Critical Datathon 2023 (MIMIC-IV) and BOLD'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: Other
year: '2023'
domain: medical & healthcare
original_data_state: One Table
source_links:
- https://doi.org/10.13026/8vsr-1f85
- https://doi.org/10.13026/vfba-0n65
- https://physionet.org/content/mit-critical-datathon-2023/1.0.0/
- https://physionet.org/content/blood-gas-oximetry/
- https://doi.org/10.1038/s41597-024-03225-z
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: ICU pairs of a pulse-oximeter reading (SpO2) and the arterial blood-gas saturation (SaO2) drawn after it, with clinical covariates, published on PhysioNet for pulse-oximetry correction models; a real measurement-correction task, but two releases of one group in one record and covariates whose timing must be checked.
- Source: two PhysioNet releases by Matos, Struja, Celi et al. (MIT Critical Data). (a) "MIT Critical Datathon 2023: a MIMIC-IV Derived Dataset for Pulse Oximetry Correction Models", v1.0.0, 2023-05-08 (doi 10.13026/jfpc-pz79, latest-version doi 10.13026/8vsr-1f85): 81,797 ICU SaO2-SpO2 pairs from MIMIC-IV v2.2, a pair formed "when an SpO2 measurement is found within 90 minutes before an SaO2 value", the offset kept; files `mimic_pulseOx_data.csv` and `mimic_pulseOx_dictionary.csv`. (b) "BOLD, a blood-gas and oximetry linked dataset", v1.0, 2023-11-08 (doi 10.13026/phvt-3277, latest 10.13026/vfba-0n65), data paper Matos et al., Scientific Data 11:535 (2024, doi 10.1038/s41597-024-03225-z): 49,099 pairs of 44,907 patients (eICU-CRD 43,438, MIMIC-IV 4,921, MIMIC-III 740), SpO2 up to 5 minutes before SaO2, only the first pair per hospitalisation, both 70-100%; covariates demographics (age, sex, race and ethnicity), comorbidity scores, BMI, admission data, vitals, lab panels with a time delta each, hourly SOFA, and outcomes such as in-hospital mortality; one CSV and a PDF dictionary. Both under PhysioNet credentialed access (Credentialed Health Data License 1.5.0, CITI training; a note, not a criterion, EV-4).
- Use case: an ICU clinician reads SpO2 and decides on oxygen therapy or an arterial blood gas; a correction model estimates SaO2, or flags hidden hypoxaemia (SaO2 < 88% with SpO2 >= 88%), from the reading and the covariates known then. The pages name the purpose ("supports the building of pulse oximetry correction models"; BOLD: "develop debiasing algorithms") but no actor or decision, so the fit is approximate for now. Regime grouped: by patient in (a), where a stay gives many pairs; by hospital in (b), where eICU-CRD spans many hospitals (the hospital id is to be checked in the BOLD file).
- Siblings and duplicates: `mimic_iv` (`TBD -> 2nd Tier`, a database without a task) and `eicu_collaborative_research_database` (`TBD -> 2nd Tier`): the parent databases, not duplicates, since these releases define a task of their own (PROV-7). (a) and (b) share MIMIC-IV pairs: BOLD's 4,921 MIMIC-IV pairs are a 5-minute, first-pair cut of the same source as (a), so the two are versions of one task (PROV-6) and the curator picks one; BOLD is the wider one (three databases, about 25% minority patients per the page), (a) the larger in pairs. No other oximetry record. External collections: none found.
- Better data: found as better data for `mimic_iv` and from the curator's Zotero collection (item 80); no further search this round.
- Papers and pages: the two PhysioNet pages; Matos et al. 2024, Scientific Data 11:535 (medRxiv 2023.10.03.23296485); BOLD's code on GitHub (linked from PhysioNet, not opened).
- Metric: none found. The datathon page says no metrics are defined and users are "free to design their own fair evaluation metrics"; BOLD's page and abstract report no model metric (the paper's full text was not read). So the fallback: `rmse` for SaO2 (or the SaO2-SpO2 gap), `roc_auc` for hidden hypoxaemia (MET-1, MET-8); inputs none.
- Risks for /add-dataset: in-hospital mortality and other outcomes ship as covariates and must go, and every time-varying covariate must be measured before the SpO2 reading, read from its time delta (LEAK-10, USE-3); SpO2 is the natural core of the task, so a high score from it alone is no `Trivial` (TP-4), and the gap target shows the residual; race and ethnicity as an input of a correction model is a question for the curator (the source's aim is to measure the bias by group); (a)'s 90-minute window lets the patient change between the two readings, BOLD's 5-minute window does not; choose one release (PROV-6); access needs a PhysioNet credential.
- Priority: gap 0 (medical, regression or binary, grouped are not thin), use case 0 (the purpose is named, not the actor), source + (PhysioNet releases and a Scientific Data paper), shape + (49,099 to 81,797 pairs, mixed covariates, patient and hospital groups), risk - (outcome and post-reading covariates to remove).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `mimic_iv`; the curator's Zotero collection, item 80: "PhysioNet".
- as published: 81,797 paired SaO2-SpO2 measurements of ICU patients from MIMIC-IV v2.2 with clinical covariates; BOLD: 49,099 pairs within 5 minutes from MIMIC-III, MIMIC-IV and eICU-CRD (about 25% minority groups); target: arterial oxygen saturation SaO2 (regression), or hidden hypoxaemia (SaO2 < 88% with SpO2 >= 88%); access: registration.
- Why: A defined regression task with a real reference measurement and a health-equity use; a task-defined subset of the MIMIC-IV record.
- Adds: Measurement correction in critical care; BOLD adds a multi-database source. Caveats: SpO2 dominates (check Trivial), credentialed licence.
