---
unique_name: elaia1_aki_progression
name: 'ELAIA-1: progression, dialysis or death within 14 days in inpatients with acute kidney injury'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Other
year: '2020'
domain: medical & healthcare
problem_type: Binary Classification
source_links:
- https://doi.org/10.5061/dryad.4f4qrfj95
- https://doi.org/10.1136/bmj.m4786
- https://clinicaltrials.gov/study/NCT02753751
- https://doi.org/10.5061/dryad.kh189327p
- https://bingkaiwang.github.io/RCT_Bench-main/website/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 6,030 adult inpatients with KDIGO acute kidney injury at six US hospitals, randomized at AKI detection in the ELAIA-1 alert trial, with a composite of AKI progression, dialysis or death within 14 days (1,275 events, 21%); an open CC0 file with a data dictionary and a clear prediction point, but no prediction metric from the source.
- Source: Wilson et al., "Electronic health record alerts for acute kidney injury: multicenter, randomized clinical trial", BMJ 2021;372:m4786 (2021-01-18); data: Wilson, "Randomized trial of AKI alerts in hospitalized patients", Dryad, 2020-11-30, doi 10.5061/dryad.4f4qrfj95, CC0 (`ELAIA-1_deidentified_data_10-6-2020.csv`, 2.2 MB; `ELAIA-1_data_dictionary_10-6-2020.csv`); NCT02753751. As published (Dryad abstract): "6,030 adult inpatients with AKI, as defined by the Kidney Disease: Improving Global Outcomes (KDIGO) creatinine criteria", randomized over 22 months to a pop-up alert with an order set or usual care at "Six diverse hospitals (four teaching and two non-teaching)"; the primary outcome "occurred in 653 (21.4%) patients in the alert group and 622 (20.9%) in the usual care group (relative risk 1.02)"; in the two non-teaching hospitals the alert went with more events (RR 1.49) and deaths. The columns were not previewed (the Dryad download needs a token); the run's Assessment reports about 25 baseline covariates in the RCT Bench copy.
- Use case: when the EHR detects AKI, the hospital or a nephrology service decides whom to escalate (consult, monitoring, nephrotoxin review) by the risk of progression, dialysis or death within 14 days; fit direct for the moment and the label (the trial's primary outcome at a fixed horizon from detection), with half the rows under a randomized alert (no effect overall). Regime: one row per patient; IID, or grouped by hospital (six hospitals whose outcomes differed by type), to decide at add time.
- Siblings and duplicates: `kumc_inpatient_aki_prediction` (AKI onset in KUMC inpatients, another task and source). ELAIA-2 (Dryad 2023-03-28, doi 10.5061/dryad.kh189327p, CC0: 5,060 AKI inpatients with an order for an NSAID, RAAS inhibitor or PPI, the same composite outcome, NCT02771977) is the sibling trial of the same group with its own population (PROV-7); it has no record and could be pooled with a trial column or kept apart. `eicu_collaborative_research_database`, `mimic_iv` are ICU databases. External collections: RCT Bench (Shao, Lyu, Yu, Wang, J Clin Epidemiol 2026; a covariate-adjustment collection of 125 trials; the ELAIA-1 entry was not visible on its page).
- Better data: from the curator's Zotero collection (item 136); no search for better data in this run.
- Papers and pages: the BMJ paper; the Dryad usage note on `time_to`: "The "time_to" data reflects the time from randomization to the event of interest, discharge, or 14 days (whichever comes first). Be careful when analyzing this!".
- Metric: none found (the Dryad record, the BMJ abstract on it and the RCT Bench page report relative risks, no prediction); fallback `roc_auc` (MET-1); inputs none.
- Risks for /add-dataset: drop the post-randomization columns: the outcome components, `time_to`, and the AKI care practices after the alert (the trial's secondary outcomes) (LEAK-10); decide whether the randomized arm stays as a feature (known at the prediction point; it changed outcomes in the non-teaching hospitals) or only usual care is kept (USE-3); patients discharged alive before day 14 count as event-free in the paper (USE-5); hospital as a group or a feature.
- Priority: gap 0 (medical & healthcare and binary are not thin), use case 0 (the decision is the curation's; the trial tests an alert, not a risk model), source + (BMJ trial, Dryad with a dictionary), shape + (6,030 patients, mixed baseline covariates, six hospitals), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 136: "Datasets".
- as published: 6,030 adult inpatients with KDIGO AKI at six hospitals; ELAIA-1_deidentified_data CSV 2.2 MB plus a dictionary (raw file not opened); the RCT Bench copy shows about 25 baseline covariates (hospital, ...; target: Composite of AKI progression to a higher KDIGO stage, dialysis or death within 14 days of AKI detection (binary); access: open.
- Why: Real EHR data with a clear prediction point (AKI detection), an objective outcome, open under CC0 with a trial paper; found by scanning RCT Bench, linked from the hbiostat page.
- Adds: Acute kidney injury prognosis, a task with no record. Caveats: the alert arm is a randomized treatment (no effect on the outcome in the paper; keep or drop); 'time_to' runs to discharge or day 14 (the Dryad notes warn); ELAIA-2 (5,060 AKI inpatients on nephrotoxic drugs, Dryad 2023, CC0) is a sibling (PROV-7).
