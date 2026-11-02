---
unique_name: crash_head_injury_outcome
name: CRASH trial (Corticosteroid Randomisation After Significant Head Injury) patient data
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Other
year: '? (2005)'
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.17037/DATA.11
- https://freebird.lshtm.ac.uk/home/
- https://datacompass.lshtm.ac.uk/id/eprint/35/7/CRASH_Data_Dictionary_HTML.html
- https://doi.org/10.1136/bmj.39461.643438.25
- https://doi.org/10.1016/S0140-6736(04)17188-2
- https://www.re3data.org/repository/r3d100012213
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 10,008 adults with head injury from the CRASH trial (1999-2004) with a widely validated prognostic model (death at 14 days, death or severe disability at 6 months); few baseline inputs, CT findings recorded on the 14-day forms, and access only through freeBIRD.
- Source: CRASH trial collaborators, Lancet 2004 (doi 10.1016/S0140-6736(04)17188-2); the data are released by the LSHTM Clinical Trials Unit through freeBIRD and recorded in LSHTM Data Compass (doi 10.17037/DATA.11, record 35): 10,008 adult records, 87 fields, collection May 1999 to May 2004, "Access to this dataset is available via https://freebird.lshtm.ac.uk/"; the dictionaries are under CC BY 3.0; country, hospital code and treatment allocation are excluded and "may be obtained on direct request to LSHTM CTU". Data dictionary (public HTML, read 2026-10-31): baseline sex, age, randomisation date and time, minutes since injury, GCS eye, motor and verbal, whether the GCS is current, left and right pupil reactivity; the 14-day forms of the admitting and the transfer hospital: cause of injury, outcome and its date, symptoms, ICU days, seizure, GI bleeding, infections, neurosurgery, major extracranial injury, trial-drug doses, head CT with its date and findings (petechial haemorrhages, obliterated third ventricle or basal cisterns, subarachnoid bleed, midline shift above 5 mm, evacuated and non-evacuated haematoma); the 6-month questionnaires with GOS (5 and 8 levels) and tracking codes.
- Use case: the clinician, at admission of an adult with head injury, estimates the risk of death within 14 days (or death or severe disability at 6 months) to inform treatment and the family; the MRC CRASH 2008 paper concludes "Simple prognostic models can be used to obtain valid predictions of relevant outcomes" (abstract) but names no decision, so the actor is ours; fit direct for the baseline model; regime IID across patients (hospital and country withheld; the randomisation date ships for a temporal check, SPLIT-7).
- Siblings and duplicates: `crash2_trauma_early_death` (CRASH-2, same trials unit, another trial of bleeding trauma: not a duplicate, PROV-7); `pecarn_pediatric_head_trauma_citbi` (children with minor head trauma, a CT decision: another task). No other record of the CRASH trial (grep: crash, head injury, traumatic brain, freebird). External collections: none found.
- Better data: from the curator's Zotero collection (items 79, 127, 136); no further search this round.
- Papers and pages: MRC CRASH Trial Collaborators, "Predicting outcome after traumatic brain injury: practical prognostic models based on large cohort of international patients", BMJ 2008;336:425-9 (PMID 18270239): death at 14 days and death or severe disability at 6 months; a basic model (age, GCS, pupil reactivity, major extracranial injury; country income level) and a CT model; "excellent discrimination (C statistic above 0.80)" in derivation; external validation in 8,509 IMPACT patients; the CRASH online calculator.
- Metric: the BMJ 2008 paper reports discrimination (C statistic) and calibration (graphically and Hosmer-Lemeshow) of risk models: `roc_auc` (MET-5, MET-8); inputs none.
- Risks for /add-dataset: keep the baseline only; the 14-day and 6-month forms hold outcomes (LEAK-10); "major extracranial injury" and the CT findings sit on the 14-day forms: keep a CT finding only when its date precedes the prediction point (or define the CT model's point after the first scan) and check when extracranial injury was recorded (USE-3, USE-4); country income level, a predictor of the published models, is withheld; choose one target, death at 14 days or the 6-month unfavourable outcome (two framings of one prognosis, CLEAN-18); loss to follow-up at 6 months; freeBIRD answers scripts with 403, and its terms reportedly require the chief investigators' permission to publish results (not verified; a release-checklist item, EV-4).
- Priority: gap 0 (medical, binary not thin), use case 0 (the paper names the prediction, not the decision), source + (the trials unit's release with a DOI and a public dictionary), shape + (10,008 patients, about 10 baseline inputs plus dated CT findings, mixed types), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the dead-link check of the curator's Zotero collection; the curator's Zotero collection, item 127: "Datasets"; the curator's Zotero collection, item 136: "Datasets"; the curator's Zotero collection, item 79: "Datasets".
- as published: 10,008 adults with head injury and GCS <= 14 within 8 h, 239 hospitals in 49 countries, 1999-2004; one CSV (CRASH data.csv): baseline (sex, age, minutes since injury, GCS eye/motor/verbal, pupil ...; target: death within 14 days (also death or severe disability at 6 months, GOS); access: registration, registration (freeBIRD; its terms reportedly forbid publicising data or results without the Chief Investigators' permission, not verified: freeBIRD answers 403 to scripts).
- Why: A large international trial cohort with a published, widely validated prognostic model and a clear prediction point; it comes from the first publisher (LSHTM), and its data dictionary is public. | A large trial cohort with a widely used prognostic model, a documented dictionary and a fixed prediction point | A large ...
- Adds: Traumatic brain injury prognosis, absent from the records; a sibling of crash2_trauma_early_death. Caveats: few baseline inputs (about 8, plus CT findings that carry a date, so the pre-prediction ones can be kept). Country, hospital and the trial arm are excluded from the shared file and only on request from the CTU, ...
