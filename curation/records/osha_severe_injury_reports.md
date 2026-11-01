---
unique_name: osha_severe_injury_reports
name: OSHA Severe Injury Reports (SIR), full data set
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
original_source: GOV Website
year: '2015'
original_data_state: One Table
source_links:
- https://www.osha.gov/severe-injury-reports
- https://catalog.data.gov/dataset/severe-injury-report-sir-data
- https://osha.prod.pace.dol.gov/sites/default/files/2024_Annual_Report_of_Fed_OSHA_SIRs.pdf
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: about 9,000 employer reports a year (2015 to November 2025) of amputations, in-patient hospitalizations and losses of an eye in federal-OSHA states, with coded event, source, nature and body part and a narrative; real and official, but no predictive target is published.
- Source: US Department of Labor, OSHA, Severe Injury Reports (osha.gov/severe-injury-reports, read 2026-10-31): severe injuries "defined as an amputation, in-patient hospitalization, or loss of an eye", reportable since January 1, 2015; the full downloadable file "covers reports from 1/1/2015 through 11/30/2025"; federal jurisdiction only, the data "do not include incidents under state plan state jurisdiction"; injuries coded with the Occupational Injury and Illness Classification System; the data "will be updated periodically"; a full ZIP download. 9,034 reports in 2024 per OSHA's annual report (the scout's reading). Fields per the page: event date, establishment name and address, NAICS, a description of the incident, the OIICS codes; the per-report flags (hospitalized, amputation, inspection) are the scout's reading, not checked.
- Use case: none from the source. The scout's candidates: whether OSHA opens an inspection rather than a rapid response investigation when a report comes in (OSHA's own decision, partly set by its enforcement procedures), or amputation against hospitalization, which the report itself states. Neither has a documented actor who predicts it: `No Good Target (yet)`, as on the sibling. Regime temporal once a target is found (dated reports).
- Siblings and duplicates: `osha_accidents_data` (Lennart and Mustafa `TBD -> 2nd Tier`, `No Good Target (yet)`). Correction to the run's note that its Kaggle file is a slice of this release: that file ("OSHA HSE DATA_ALL ABSTRACTS 15-17_FINAL.csv", Kaggle ruqaiyaship) holds "abstracts of the accidents and injuries of construction workers from 2015-2017" with "Degree of Injury, Body Part(s) Affected, and Construction End Use" (Kaggle description, read 2026-10-31), fields of OSHA's accident investigation tables (DOL `OSHA_accident`, `OSHA_accident_abstract`, `OSHA_accident_injury`, ids 10331 to 10333), which this release does not carry. So this record is a related OSHA release with another task, not a newer version of that record (PROV-7, not PROV-6). `osha_inspection_violations` (this run) is the enforcement data. External collections: none found.
- Better data: found as better data for `osha_accidents_data`; no further search this round.
- Papers and pages: the OSHA page and its annual severe-injury reports.
- Metric: none found (no task published); the fallback once a target is chosen (MET-8).
- Risks for /add-dataset: the target (SEL-3, USE-2); the outcome flags are part of the report, so predicting them from the narrative is a text task (SEL-12); establishment names and addresses to drop.
- Priority: gap 0, use case 0 (no target), source + (OSHA's official release), shape + (on the order of 100,000 dated reports with codes and text), risk - (no target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `osha_accidents_data`.
- as published: employer reports of amputations, in-patient hospitalizations and loss of an eye under 29 CFR 1904.39, federal-OSHA states only; about 9,000 reports a year (9,034 in 2024 per OSHA's annual report), ...; target: not fixed by the source (the record's open issue): candidates are the injury outcome flags (amputation vs hospitalization) or whether OSHA opened an ...; access: open.
- Why: the record's Kaggle file (ruqaiyaship, 2015-2017) is a re-upload of a slice of this OSHA release; the full release is the first publication of the same rows plus eight more years
- Adds: about 11 years instead of 3 (roughly 3-4x the rows), the official first publication instead of a Kaggle re-upload, and a temporal range long enough for a temporal split; the target question stays open
- A newer release of the same source as the record(s) named above (PROV-6): the curator decides which one enters.
