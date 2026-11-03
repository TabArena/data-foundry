---
unique_name: wids_icu_hospital_death
name: 'WiDS Datathon 2020: ICU patient survival from the first 24 hours (MIT GOSSIS data)'
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
source_links:
- https://www.kaggle.com/competitions/widsdatathon2020
- https://doi.org/10.1097/ccm.0000000000005518
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Duplicate`, PROV-4): the record names the WiDS Datathon 2020 competition on Kaggle and its target `hospital_death`, which `gossis_icu_hospital_mortality` already records and has screened (the same competition link, the same training_v2.csv, the same target): two records of one source.
- Source: WiDS Datathon 2020 on Kaggle (https://www.kaggle.com/competitions/widsdatathon2020; Kaggle API: deadline 2020-02-24, 951 teams), data from MIT's GOSSIS initiative (Raffa et al. 2022, doi 10.1097/ccm.0000000000005518), also on PhysioNet (doi 10.13026/530d-1e61): training_v2.csv with 91,713 labelled ICU encounters and about 186 columns, target `hospital_death`, scored by ROC AUC.
- Why a duplicate: `gossis_icu_hospital_mortality` (screened 2026-10-31, `TBD -> Yes`, priority 2) has this competition as its first source link, the same Raffa et al. DOI, the same file and the same target, and its block says: "`wids_icu_hospital_death` (created by the same run, screening batch 53, for the same Kaggle competition and target: the same dataset, PROV-4; one of the two should become `Duplicate`)". This record adds no task (the competition ships no ICU length-of-stay target, the run's own note) and no link the other lacks. The run's duplicate list flags the pair (screen_37).
- Siblings: `eicu_collaborative_research_database` (`TBD -> 2nd Tier`, the eICU source of the GOSSIS US cohort, a PROV-6 question for the curator on the kept record), `wids_diabetes_mellitus` (`Yes`, WiDS 2021, a distinct target, PROV-7), `icu_length_of_stay_icu_mortality` (MIMIC-III through TableShift, another source).
- Better data: found as better data for `icu_length_of_stay_icu_mortality`; the finding carries over to `gossis_icu_hospital_mortality`.
- Metric: not needed for a duplicate (the kept record declares `roc_auc`, MET-4).
- Kept record: `gossis_icu_hospital_mortality`; if the curator prefers this record's name, swap the two and keep one.
- Reject check (AI, 2026-10-31): stands. Both records have the same first link (https://www.kaggle.com/competitions/widsdatathon2020), the same Raffa et al. DOI, training_v2.csv and hospital_death. gossis_icu_hospital_mortality holds both of this record's links. The length-of-stay angle this record was found for is absent from the competition, so there is no distinct task.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `icu_length_of_stay_icu_mortality`.
- as published: 91,713 labelled ICU encounters in training_v2.csv (plus unlabeled.csv without the target), one row per encounter, about 186 columns (data dictionary file); 'more than 130,000' ICU visits 'spanning a ...; target: hospital_death (in-hospital death, binary); source metric ROC AUC; access: registration.
- Why: Same target as the record's ICU Mortality task (in-hospital death of an ICU patient from data of the first 24 h: vitals and lab extrema, diagnosis, GCS, comorbidities, demographics) and the same use case; a ready-made tabular extract instead of a MIMIC-Extract pipeline.
- Adds: 3.8x the labelled rows (91,713 vs 23,944), multi-centre (200+ hospitals, so a split by hospital is a real shift instead of TableShift's insurance shift), open through Kaggle registration instead of PhysioNet credentialing. Caveats: the 2014-2015 US GOSSIS cohort is very probably the eICU-CRD part of GOSSIS (Raffa et ...
