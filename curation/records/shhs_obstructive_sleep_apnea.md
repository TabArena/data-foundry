---
unique_name: shhs_obstructive_sleep_apnea
name: Sleep Heart Health Study (SHHS)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Other
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://doi.org/10.1093/sleep/20.12.1077
- https://biolincc.nhlbi.nih.gov/studies/shhs/
- https://sleepdata.org/datasets/shhs
- https://github.com/nsrr/shhs-data-dictionary
- https://doi.org/10.1093/jamia/ocy064
- https://doi.org/10.5664/jcsm.9268
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the NHLBI Sleep Heart Health Study, about 5,800 community adults aged 40 and older with a home polysomnogram and the clinical and questionnaire data of the same visit; moderate-to-severe sleep apnea from the visit data is a screening task already studied on this cohort.
- Source: Quan et al., "The Sleep Heart Health Study: design, rationale, and methods", Sleep 20(12):1077-1085 (1997); data through the National Sleep Research Resource (sleepdata.org/datasets/shhs, read 2026-10-31; Zhang et al. 2018, JAMIA, doi 10.1093/jamia/ocy064) and BioLINCC. The NSRR page: "5,804 adults aged 40 and older"; "6,441 men and women aged 40 years and older were enrolled between November 1, 1995 and January 31, 1998"; "a second polysomnogram (SHHS Visit 2) was obtained in 3,295 of the participants"; covariate datasets of Visits 1 and 2, the polysomnography signals and annotations, and CVD outcomes to 2011; the data dictionary is on GitHub (nsrr/shhs-data-dictionary, not read). Access by a data access request and agreement (no criterion, EV-4). The page notes "This repository is under review for potential modification in compliance with Administration directives."
- Use case: a primary-care physician decides whether to refer a patient for a sleep study, from age, sex, BMI, neck and waist, blood pressure, snoring, witnessed apneas and sleepiness, all known at the visit. Vana et al. 2021 (J Clin Sleep Med 17(8):1635-1643, doi 10.5664/jcsm.9268) evaluate this screen on "6,167 participants from the Sleep Heart Health Study baseline evaluation", with moderate-to-severe apnea from the polysomnogram as the target. Fit direct. Regime IID by participant at Visit 1 (the parent cohorts are a possible group).
- Siblings and duplicates: `sleep_health_and_lifestyle_dataset` (`No`, declared synthetic by its author) and `sleep` (`TBD -> 2nd Tier`, unknown source) are the records whose task this covers; `aric_incident_chd` and `framingham_heart_study_fhs` come from parent cohorts of SHHS (shared participants, other tasks, PROV-7). External collections: none known.
- Better data: found as better data for `sleep_health_and_lifestyle_dataset` (the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: Quan et al. 1997; Zhang et al. 2018 (NSRR); Vana et al. 2021.
- Metric: Vana et al. 2021 derive cut points with their sensitivity and specificity and compare the screens by the area under the ROC curve ("no statistical difference with listwise comparison of the NHR and dSBQ areas under the receiver operator curves"), so `roc_auc` (MET-5; the fallback too); inputs none.
- Risks for /add-dataset: the covariate files hold many variables derived from the polysomnogram (event indices, oxygen saturation, sleep stages) that must all be dropped (LEAK). The threshold (AHI of 15 per hour) and the AHI definition (hypopneas with 3% or 4% desaturation) are a choice to document. Participants already diagnosed or treated for sleep apnea should be checked (SEL-7). The data comes only through a request and agreement.
- Priority: gap 0 (medical, binary and IID are not thin), use case + (Vana et al. name the screening decision), source + (NHLBI study, NSRR data dictionary), shape + (about 5,800 adults, hundreds of mixed variables), risk - (polysomnography-derived columns).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `sleep_health_and_lifestyle_dataset`.
- as published: 6,441 adults aged 40+ enrolled 1995-1998; data of 5,839 consenting participants shared (BioLINCC); second home polysomnogram in 3,295 (2001-2003); hundreds of variables; target: Obstructive sleep apnea from the home polysomnogram (apnea-hypopnea index, e.g. AHI >= 15/h, or none/mild/moderate/severe); insomnia symptoms from the Sleep ...; access: request.
- Why: The Kaggle record (374 to 400 rows, declared synthetic by its author) predicts a sleep disorder (none, insomnia, sleep apnea) from age, sex, BMI category, blood pressure, heart rate and lifestyle; SHHS has the same kind of features with apnea measured by polysomnography. Vana et al. 2021 (JCSM, doi 10.5664/jcsm.9268) ...
- Adds: A real NIH cohort of about 5,800 adults with a polysomnography-based target instead of a made-up table. Open alternative not checked: NHANES sleep questionnaire (SLQ: doctor-told sleep disorder, snoring, stopped breathing) with exam data, self-reported target
