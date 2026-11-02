---
unique_name: crash2_trauma_early_death
name: CRASH-2 trial data (tranexamic acid in bleeding trauma patients)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
original_source: Other
year: '? (2010)'
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://hbiostat.org/data/repo/crash2.html
- https://freebird.lshtm.ac.uk/
- https://doi.org/10.1016/S0140-6736(10)60835-5
- https://doi.org/10.1136/bmj.e5166
- https://doi.org/10.17037/DATA.10
- https://datacompass.lshtm.ac.uk/34/
- https://hbiostat.org/data/repo/ccrash2
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: 20,207 bleeding trauma patients from 274 hospitals in 40 countries (CRASH-2 trial, 2005-2010), open under CC BY 3.0, with a published and externally validated prognostic model for in-hospital death within 4 weeks from about ten baseline inputs.
- Source: CRASH-2 trial collaborators, Lancet 2010;376:23-32 (doi 10.1016/S0140-6736(10)60835-5); the data are released by the LSHTM Clinical Trials Unit through freeBIRD and recorded in LSHTM Data Compass (doi 10.17037/DATA.10, record 34): 20,207 patient records (20,211 randomised, four withdrew consent), 46 fields, collection 2004-12-01 to 2010-01-01, deposited 2015-07-31, "Available under Creative Commons: Attribution 3.0"; site name and identifier, country and the treatment allocation are excluded and "may be obtained on direct request". An open copy is on hbiostat.org (Vanderbilt Biostatistics, "generously supplied by the freeBIRD Bank of Injury and Emergency Research Data"): 20,207 x 44 (R data dictionary at hbiostat.org/data/repo/ccrash2, read 2026-10-31). Baseline: sex, age, hours since injury, injury type, systolic BP, respiratory rate, central capillary refill, heart rate, GCS eye, motor, verbal and total, randomisation date. After randomisation: date and main cause of death (3,086 deaths dated), status, condition and date at discharge or day 28, ICU days, significant head injury, neurosurgery, chest, abdominal and pelvic surgery, PE, DVT, stroke, MI, GI bleeding, surgery for bleeding, trial-drug loading and maintenance doses, transfusions and units, factor VIIa; `boxid` and `packnum` (treatment pack numbers).
- Use case: the emergency clinician, at the first assessment of a bleeding trauma patient, estimates the risk of death to triage and speed up imaging, surgery and tranexamic acid: Perel et al. 2012 conclude the model "can be used to obtain valid predictions of mortality in patients with traumatic bleeding" and tie it to triage and faster lifesaving procedures (abstract); fit direct for the baseline inputs (country income level, a predictor of the published model, is withheld); regime IID across patients (hospital and country are withheld, so no group can be recovered; the randomisation date allows a temporal check, SPLIT-7).
- Siblings and duplicates: `crash_head_injury_outcome` (the CRASH trial of head injury, same trials unit, another trial and population: not a duplicate, PROV-7); `pecarn_pediatric_head_trauma_citbi`, `nhamcs_ed_hospitalization` (other emergency tasks). No other record of CRASH-2 (grep: crash2, crash-2, tranexamic, freebird). External collections: the Vanderbilt Biostatistics dataset repository (hbiostat.org/data).
- Better data: from the curator's Zotero collection (items 79, 127, 136); no further search this round.
- Papers and pages: CRASH-2 Lancet 2010 (primary outcome "death in hospital within four weeks of injury", Data Compass abstract); Perel et al., "Predicting early death in patients with traumatic bleeding: development and validation of prognostic model", BMJ 2012;345:e5166 (PMID 22896030): 20,127 CRASH-2 patients, outcome "In-hospital death within 4 weeks of injury", predictors GCS, age, systolic BP, country income level, heart rate, time since injury and injury type, external validation in 14,220 TARN patients; CRASH-2 Intracranial Bleeding Study, BMJ 2011;342:d3795.
- Metric: Perel et al. judge the model by discrimination and calibration ("Discrimination and calibration were satisfactory, with C statistics above 0.80 in both CRASH-2 and TARN", abstract): a probability task, so `roc_auc` (the C statistic; MET-5, MET-8); inputs none.
- Risks for /add-dataset: every post-randomisation column is after the prediction point: keep only the baseline (LEAK-10, USE-3); build the label from the death and randomisation dates (death in hospital within 28 days) and check the 80 rows without an outcome record (`outcomeid` missing) and deaths after discharge; drop `boxid` and `packnum`; the treatment arm is withheld, so the trial's treatment effect on mortality stays unexplained noise; freeBIRD answers scripts with errors, while the hbiostat copy is open (check that it matches the CSV of the trials unit, PROV-15).
- Priority: gap 0 (medical, binary not thin), use case + (the prognostic-model paper names triage and the prediction point), source + (the trials unit's release with a DOI and a dictionary), shape + (20,207 patients, about 12 mixed baseline inputs), risk 0 (the leaking columns are named by the dictionary and simply dropped).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 127: "Datasets"; the curator's Zotero collection, item 136: "Datasets"; the curator's Zotero collection, item 79: "Datasets".
- as published: 20,207 adult trauma patients with significant haemorrhage, 274 hospitals in 40 countries, 2005-2010. The hbiostat copy has 44 variables: about 10 baseline inputs (age, sex, hours since injury, ...; target: Death within 28 days (also cause of death); access: open, registration, registration (freeBIRD); an open mirror on hbiostat.
- Why: Large, multi-country, documented trial data with a published prognostic task. | Large international trial cohort with a published prognostic model and baseline features known at the prediction point | A large open trial dataset with a published prognostic model and a clear prediction point.
- Adds: Trauma and emergency medicine, absent from the records. Caveats: few baseline inputs; the post-randomisation columns leak and must be dropped; freeBIRD (registration) is unreachable now, while hbiostat hosts the copy 'generously supplied by freeBIRD'. | A trauma prognosis task; no record covers it. Corrected against ...
