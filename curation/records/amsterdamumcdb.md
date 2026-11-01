---
unique_name: amsterdamumcdb
name: AmsterdamUMCdb (Rembrandt 1.0.2)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: Other
year: '2019'
domain: medical & healthcare
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://amsterdammedicaldatascience.nl/
- https://doi.org/10.1097/CCM.0000000000004916
- https://github.com/AmsterdamUMC/AmsterdamUMCdb
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and papers, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: a documented European ICU database (23,106 admissions, 2003-2016) with real outcomes, but a relational database without a task of its own, access by personal licence, and time-stamped measurements to aggregate; screened like `mimic_iv` and `eicu_collaborative_research_database`.
- Source: Amsterdam UMC, AmsterdamUMCdb, described in Thoral et al. 2021, "Sharing ICU Patient Data Responsibly Under the Society of Critical Care Medicine/European Society of Intensive Care Medicine Joint Data Science Collaboration: The Amsterdam University Medical Centers Database (AmsterdamUMCdb) Example", Crit Care Med 49(6):e563-e577 (doi 10.1097/CCM.0000000000004916). Versions (GitHub README and amsterdammedicaldatascience.nl, read 2026-10-31): 1.0 (November 2019); "Rembrandt" 1.0.2 (March 2020, legacy tables `admissions`, `drugitems`, `freetextitems`, `listitems`, `numericitems`, `procedureorderitems`, `processitems`), "23,106 admissions of 20,109 patients admitted from 2003 to 2016" to the ICU and high-dependency units of location AMC, adults; 1.5.0 (May 2024, OMOP CDM 5.4, "only to close collaborators for now"). "Van Gogh" (both locations, AMC and VUmc, 2002-2023, provisionally about 74,000 admissions) is "forthcoming, in preparation". Access: "personal and bound to an End User License" for "lawful, non-commercial scientific research", with CITI training and a practising intensivist as reference; files from DANS.
- Use case: none as published (a research database). Tasks others defined on it: YAIB (van de Water et al., "Yet Another ICU Benchmark", ICLR 2024; "AUMCdb") ships mortality, acute kidney injury, sepsis, kidney function and length of stay. An intensivist or bed manager at a fixed hour of the stay deciding on escalation or discharge planning would be ours to state; fit approximate until a task is fixed. Regime grouped by patient (20,109 patients, 23,106 admissions) or temporal by admission period; to decide with the task.
- Siblings and duplicates: no record of this source. `mimic_iv` (`TBD -> 2nd Tier`, priority 2, `Needs extensive data wrangling`) and `eicu_collaborative_research_database` (`TBD -> 2nd Tier`, priority 3) are the US counterparts, screened the same way; `gossis_icu_hospital_mortality` and `wids_icu_hospital_death` are tasks cut from eICU. External collections: YAIB; the ricu R package (concepts across MIMIC, eICU, HiRID and AUMCdb).
- Better data: from the curator's Zotero collection (item 82); no further search this round.
- Papers and pages: Thoral et al. 2021 (the data); github.com/AmsterdamUMC/AmsterdamUMCdb (code and tutorials, MIT); amsterdammedicaldatascience.nl (versions, access); van de Water et al. 2024 (YAIB tasks).
- Metric: none for the database (the paper and the site define no task). YAIB reports AUROC and AUPRC for its classification tasks and MAE for regression side by side; one is chosen with the task (MET-1, MET-5), otherwise the fallback (`roc_auc`, `rmse`).
- Risks for /add-dataset: a task, cohort and prediction point to define, and long tables of time-stamped measurements to aggregate to one row per admission (`Needs extensive data wrangling`); readmissions of the same patient (group by patient, SPLIT-29); the build needs an approved personal licence (no criterion, EV-4) and would use 1.0.2, since 1.5.0 is restricted.
- Priority: gap 0 (medical & healthcare is not thin), use case 0 (no task named by the source), source +, shape + (23,106 admissions, rich clinical tables), risk - (joins and aggregation, a task to define).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 82: "Amsterdam Medical Data Science".
- as published: 23,106 ICU/high-dependency admissions of 20,109 patients at AMC, 2003-2016 (multi-table: demographics, vitals, labs, medications); Van Gogh about 74,000 admissions 2002-2023; target: no task as published; usual ICU targets are mortality and length of stay (as in the eicu record); access: request.
- Why: European ICU database, a counterpart to MIMIC and eICU.
- Adds: Non-US ICU data; low priority: needs a task and extensive wrangling. Access on request with a non-commercial End User License.
