---
unique_name: mover_perioperative_outcomes
name: 'MOVER: Medical Informatics Operating Room Vitals and Events Repository (UC Irvine Medical Center)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: UCI
year: '2023'
domain: medical & healthcare
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.24432/C5VS5G
- https://doi.org/10.1093/jamiaopen/ooad084
- https://archive.ics.uci.edu/dataset/877/mover:+medical+informatics+operating+room+vitals+and+events+repository
- https://mover.ics.uci.edu/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: a public operating-room EHR of UC Irvine Medical Center (83,468 surgeries of 58,799 adults, 2015-2022) whose EPIC part (64,354 surgeries, 2017-2022) records ICU transfer, in-hospital death and 11 complication classes; a large perioperative source, but relational, behind a data usage agreement, with no task of its own.
- Source: Samad, Angel, Rinehart, Kanomata, Baldi and Cannesson, "Medical Informatics Operating Room Vitals and Events Repository (MOVER): a public-access operating room database", JAMIA Open 6(4):ooad084 (October 2023; medRxiv March 2023), doi 10.1093/jamiaopen/ooad084; data doi 10.24432/C5VS5G, UCI dataset 877 ("Linked on 9/8/2023", 83,468 instances). As published (JAMIA Open, Results): the SIS part, 19,114 patients and surgeries 2015-2017 in 9 tables (patient information, I/O, vitals, observations, medications, labs, procedure events, ventilator, arterial line), and "The SIS dataset does not contain outcome information"; the EPIC part, 39,685 patients and 64,354 surgeries 2017-2022 in 10 tables (patient information, history, visit, medications, LDA, labs, measurements, postoperative complications, procedure events, coding); waveforms from all operating rooms.
- Use case: none named by the source (it offers the data for developing and benchmarking AI and for early warning of intraoperative instability). A real one: at the pre-operative assessment the anaesthesiologist decides on a post-operative ICU bed or a higher-acuity plan from history, labs and the booked procedure (written by the curation); fit approximate; regime grouped by patient (58,799 patients for 83,468 surgeries) or temporal by surgery date, to settle with the target.
- Siblings and duplicates: `vitaldb_postoperative_icu_admission` (`TBD -> Yes`, priority 2; SNUH, 6,388 operations), `inspire_surgical_case_duration` (unscreened; SNUH, about 130,000 operations; it lists MOVER's DOI 10.24432/C5VS5G among its own source_links, a related-work link to move to its comments, PROV-12), `core_temperature_surgical_infection` and `surgery_timing_complications` (Cleveland Clinic), `post_operative_patient` (`No`, Too Small, 90 rows): other hospitals and tasks, no duplicate (PROV-4). External collections: none known.
- Better data: from the curator's Zotero collection (item 78, the UCI repository listing); no further search this round.
- Papers and pages: the JAMIA Open paper and the UCI page (read); the project site mover.ics.uci.edu refused the connection, so the DUA text and the file layout were not read; the Assessment's 2026 prediction papers (30-day mortality, intraoperative hypotension, surgery time) were not verified (the run's web search budget was used up).
- Metric: none found (the paper and the UCI page define no task), so the fallback `roc_auc` for a binary outcome; inputs none, a patient id for a grouped split.
- Risks for /add-dataset: the target and the prediction point are ours to define (USE-3, USE-5): ICU transfer ("45.3% of patients are transferred to the ICU after surgery") can be a planned booking rather than an outcome, in-hospital mortality is 1.6% (1,023), complications come as 11 classes with free-text notes; the intra- and post-operative tables (vitals, medications, LDA, procedure events, complications) leak into a pre-operative task (LEAK-10, USE-4); joins across 10 tables (`Needs extensive data wrangling`); repeat surgeries of one patient; access by a data usage agreement (noted only, EV-4).
- Priority: gap 0 (medical & healthcare and binary are not thin), use case 0 (written by the curation), source + (a JAMIA Open data paper, the UCI listing), shape + (64,354 EPIC surgeries, mixed tables, patient groups), risk - (target, prediction point and leaks to define across 10 tables).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 78: "Datasets - UCI Machine Learning Repository".
- as published: 83,468 surgeries of 58,799 adult patients, 2015-2022. The EPIC part (64,354 surgeries, 39,685 patients, 2017-2022) has 10 relational tables: patient information, history, visit, medications, ...; target: To be chosen. Candidates from the EPIC tables: postoperative ICU transfer (29,131, 45.3%), in-hospital mortality (1,023, 1.6%), postoperative complication (11 ...; access: registration.
- Why: Real EHR data with recorded outcomes from a large academic hospital, in a peer-reviewed data paper. It is free after a data usage agreement and already used in 2026 prediction papers (a 30-day mortality score, intraoperative hypotension, surgery-time prediction).
- Adds: A perioperative domain: the only near record is postoperative_patient_data (90 rows). It is modern and large, with a patient grouping. Caveats: relational EHR with a task and prediction point to define, a leak risk from intra- and post-operative tables, and redistribution terms of the DUA not read (the project page ...
