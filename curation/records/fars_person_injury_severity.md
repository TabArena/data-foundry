---
unique_name: fars_person_injury_severity
name: NHTSA Fatality Analysis Reporting System (FARS), person file, injury severity, data years to 2024
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: GOV Website
year: '? (1975)'
domain: social science
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.nhtsa.gov/research-data/fatality-analysis-reporting-system-fars
- https://static.nhtsa.gov/nhtsa/downloads/FARS/2024/National/FARS2024NationalCSV.zip
- https://static.nhtsa.gov/nhtsa/downloads/FARS/2001/National/FARS2001NationalCSV.zip
- https://sci2s.ugr.es/keel/dataset.php?cod=191
- https://www.openml.org/d/40672
- https://www.nhtsa.gov/file-downloads?p=nhtsa/downloads/FARS/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: the documented NHTSA census behind `fars`, with person files for 50 data years; but a crash enters it only because someone died, so a person's injury severity is predicted inside a population chosen by the outcome.
- Source: NHTSA National Center for Statistics and Analysis, Fatality Analysis Reporting System (FARS), a census of US motor-vehicle crashes with a death within 30 days; national CSV zips for data years 1975 to 2024 (1975, 1982, 2001, 2010, 2023 and 2024 answer 200; the 2024 zip is 32.7 MB, last modified 2026-04-01). As published: per data year about 30 CSV tables (accident, vehicle, person and child tables such as drugs, drimpair, safetyeq, race, factor; listing of the 2024 zip read from its central directory), joined on the case number and the vehicle and person numbers; target the person file's injury severity (KABCO, plus died prior and unknown). The KEEL / PMLB / OpenML 40672 cut (the `fars` record) is the 2001 person file: 100,968 persons x 29 attributes, 8 classes of INJURY_SEVERITY, "all of the people involved in car accidents in the U.S. during 2001" (https://sci2s.ugr.es/keel/dataset.php?cod=191). Persons per year of the newer files not counted. The NHTSA FARS page answers 403 here, so the coding manuals were not read.
- Use case: none named by the source (FARS exists for national statistics). Closest decision: EMS triage of the occupants at a crash scene; fit approximate at best, because the selection (someone died within 30 days) is not known at the scene, and several person fields (taken to hospital, extrication, death date and time, later test results) are recorded after the crash. Regime temporal by data year (coding changes across years), the crash as group inside (its persons share it).
- Siblings and duplicates: `fars` (Lennart `TBD -> 2nd Tier`, `Missing source information`; TabArena Reject, TabSTAR): the 2001 cut of this source, a version (PROV-6), and this record names its source; `nhtsa_crss_crash_severity` (AI `TBD -> Yes`, priority 3): NHTSA's sample of all police-reported crashes, without the selection on a death, the better severity task (the run's note says the same); `us_accidents`, `road_safety` (`No`). External collections: TabSTAR and TabArena Reject hold the 2001 cut (on `fars`).
- Better data: found as better data for `fars`; no further search this round.
- Papers and pages: the NHTSA FARS page and file server (links above); the KEEL and OpenML pages of the 2001 cut; papers not searched (the session's web search budget ran out).
- Metric: none found (NHTSA publishes a census for estimates; KEEL lists the set without a task metric), so the fallback `log_loss` (MET-1, MET-8); inputs none.
- Risks for /add-dataset: the selection on the outcome decides whether any use case fits (USE-1, USE-8); post-crash person fields (hospital transport, extrication, death fields, alcohol and drug test results) must go (LEAK); the "died prior" and unknown classes; joins of the person, vehicle and accident tables and coding changes across 50 years (PROV-13); a temporal split by data year.
- Priority: gap + (social science and multiclass thin), use case 0 (none named), source + (NHTSA's documented census), shape + (100,968 persons in 2001, mixed, temporal), risk - (selection on the outcome, post-crash fields, joins).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `fars`; the dead-link check of the curator's Zotero collection.
- as published: a census of US fatal crashes; national CSV zip of 32.7 MB per year (ACCIDENT, VEHICLE, PERSON and more tables). Persons per year not counted; the KEEL 2001 cut has 100,968 persons x 29; target: injury severity (KABCO) of each person involved in a fatal crash; access: open.
- Why: it is the real, documented source behind the fars record, which had none: settles 'Missing source information', with 23 newer data years and coding manuals | The PMLB/OpenML columns (CASE_STATE, AGE, SEX, PERSON_TYPE, SEATING_POSITION, RESTRAINT_SYSTEM-USE, AIR_BAG, EJECTION, EXTRICATION, alcohol and drug tests, ...
- Adds: newer and traceable, several years for a temporal split. For injury severity, the better task is nhtsa_crss_crash_severity (already recorded, all police-reported crashes). | Fixes the record's 'Missing source information' marker: the first publication, the coding manual and the year are known. It also adds 50 annual ...
- A newer release of the same source as the record(s) named above (PROV-6): the curator decides which one enters.
