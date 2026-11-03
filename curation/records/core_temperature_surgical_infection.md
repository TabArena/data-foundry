---
unique_name: core_temperature_surgical_infection
name: Core Temperature (colorectal surgery surgical site infection)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: Website
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://causeweb.org/tshs/core-temperature/
- https://doi.org/10.1016/j.jclinane.2020.109758
- https://www.causeweb.org/tshs/datasets/Core_Temperature_Data_Dictionary2.pdf
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: a Cleveland Clinic registry of 7,908 colorectal operations (2005-2014) with pre- and intraoperative features and a 30-day infection outcome, released as a teaching dataset; the source study estimates the effect of hypothermia, so the prediction use case is ours, and the component-infection and in-hospital sequelae columns must go.
- Source: Walters, Tanios, Koyuncu, Mao, Valente, Sessler, "Intraoperative core temperature and infectious complications after colorectal surgery: a registry analysis", J Clin Anesth 63:109758 (online 2020-04-23): retrospective, single centre, "Adult patients having colorectal surgery at least 1 h in length" under general anaesthesia with oesophageal core-temperature monitoring, January 2005 to December 2014, 7,908 patients; primary outcome "a composite of serious infections obtained from a surgical registry and billing codes" (abstract, read on em-consulte). As published: the Teaching of Statistics in the Health Sciences (TSHS) portal (causeweb.org/tshs/core-temperature), 7,908 observations x 47 variables: two core-temperature measures (time-weighted average `TWATemp`, end-of-case `EndCaseTemp`; also `LastReadingTemp`), three infection outcomes (`AnyInfection` within 30 postoperative days, a serious-infection composite, and component indicators such as deep or organ-space SSI, superficial SSI, sepsis, wound infection), demographics, comorbidities, in-hospital surgical sequelae and in-hospital mortality; the dictionary states CC BY-NC-SA 4.0 (noted only, EV-4). These details come from search-result summaries of the portal and its dictionary: both pages failed TLS certificate verification here and were not read directly.
- Use case: the surgical and anaesthesia team, at the end of a colorectal operation, estimates the patient's risk of a serious infection within 30 days to decide on closer wound surveillance (ours: the paper reports adjusted odds ratios and builds no predictor); fit approximate; regime temporal if a surgery year or date ships (2005-2014, a deployed model scores later patients; the run's first pass saw a YEAR column), otherwise IID with the SPLIT-7 check.
- Siblings and duplicates: `surgery_timing_complications` (same TSHS portal, another Cleveland Clinic cohort and outcome: not a duplicate, PROV-7); `vitaldb_postoperative_icu_admission`, `mover_perioperative_outcomes`, `inspire_surgical_case_duration` (perioperative tasks from other sources). No other record of the study (grep: causeweb, tshs, surgical site, core temperature, hypotherm). External collections: none found; a Duke STA 210 homework (Spring 2023) uses the file (`temperature.csv`) with `AnyInfection` as the outcome.
- Better data: from the curator's Zotero collection (item 139); no further search this round.
- Papers and pages: Walters et al. 2020 (doi 10.1016/j.jclinane.2020.109758); the TSHS page and its data dictionary (the page asks to cite Homoki and Nowacki 2023 for the dataset, per the search summary).
- Metric: none found for a prediction: the paper is an association analysis ("assessed with logistic regression, adjusted for potential confounding factors", abstract), so the fallback `roc_auc` (MET-1, MET-8); inputs none.
- Risks for /add-dataset: the component-infection columns are parts of the target, and the in-hospital sequelae and mortality are known only after the operation: drop them (LEAK-10, USE-3); choose the target between `AnyInfection` and the paper's serious-infection composite (USE-5); TSHS files are prepared for teaching, so check whether values were altered for de-identification (PROV-3; the portal's wording could not be read); the cohort is selected on oesophageal monitoring and an operation of at least 1 h, which the use case shares.
- Priority: gap 0 (medical, binary, temporal not thin), use case 0 (ours; the source is an association study), source + (a peer-reviewed registry analysis and a teaching release with a data dictionary), shape + (7,908 patients, 47 mixed columns), risk - (post-operative and component-outcome columns to drop; a teaching release that may be altered).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 139: "Dataset – Teaching of Statistics in the Health Sciences".
- as published: patients, 7,908 rows x 47 columns, surgery years 2009-2014; target: any / serious infection within 30 postoperative days (binary); access: open.
- Why: real registry with pre- and intra-operative features (comorbidities, duration, open vs laparoscopic, core temperatures) and a YEAR column for a temporal split
- Adds: surgical-site-infection task; Season Effect (2,919, same portal) is the smaller version of the task. Risk: the 14 component infection columns are parts of the target and must be dropped
