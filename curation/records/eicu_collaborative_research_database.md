---
unique_name: eicu_collaborative_research_database
name: eICU Collaborative Research Database
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- 2nd Tier / Scientific Discovery
- '?'
- AI-Filled (Verify)
collections:
- New (BeyondArena)
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: TBD
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://physionet.org/content/eicu-crd/2.0/
source_row: 841
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 3: a large, well-documented multi-centre ICU database with real outcomes (hospital and ICU mortality, length of stay), but no task as published: one has to be defined and the tables joined; the old `No Good Target / Scientific Discovery` marker is refuted and dropped.
- Source: the eICU Collaborative Research Database by MIT LCP and Philips (PhysioNet, https://physionet.org/content/eicu-crd/2.0/, v2.0 of 15 Apr 2019; Pollard et al. 2018, Scientific Data 5:180178, "a freely available multi-center database for critical care research"). As published: a relational database of over 200,000 ICU unit stays of over 139,000 patients in 208 US hospitals (335 units), 2014-2015: patient, vital signs, labs, medications, diagnoses, care plan, APACHE IVa components and results; credentialed access (CITI training and a data use agreement; no criterion, EV-4). `year` left empty: the first release before v2.0 not checked.
- Use case: ICU mortality or length of stay at 24 h after admission, the APACHE IV setting (an intensivist's severity score for triage and for benchmarking units); the source names no decision ("secondary analysis of electronic health records"), so the use case is ours; fit approximate; regime grouped by hospital (a model trained on some hospitals used at a new one), patients repeat across stays.
- Siblings and duplicates: `mimic_iv` (`TBD -> 2nd Tier`, same kind of credentialed database), `icu_length_of_stay_icu_mortality` (MIMIC-III via TableShift, Lennart: `TBD -> Yes`), `sepsis_prediction` (PhysioNet 2019, other hospitals): no duplicate. External collections: YAIB (van de Water et al. 2024) and Sheikhalishahi et al. 2020 (PLOS ONE) define eICU tasks (mortality at 24 h, length of stay, AKI, sepsis); not read in detail here.
- Papers and pages: Pollard et al. 2018; the public eicu-code repository of MIT-LCP on GitHub; the benchmarks above.
- Metric: none for the database (PhysioNet page, Pollard et al. 2018); a derived benchmark's metric would be the source if we take its task (YAIB reports AUROC and AUPRC side by side: fallback, MET-5); otherwise the fallback (`roc_auc` / `log_loss`, `rmse`). Inputs: a hospital id for the grouped split (ships, `hospitalid`).
- Risks for /add-dataset: the task and the cohort have to be defined (first stay per patient, 24 h window); features charted after the prediction point and the APACHE predictions themselves (LEAK); heavy joins; size under the 500k cap is fine.
- Priority: gap + (grouped regime is thin), use case 0 (written by us), source + (Scientific Data paper, PhysioNet), shape + (200k stays, mixed types, hospital groups), risk - (heavy joins, a task to define).


The eICU Collaborative Research Database (PhysioNet) is a large multi-center ICU relational database with many tables (patients, vitals, labs, diagnoses), not a single curated predictive table. Real tabular tasks (e.g., ICU mortality, length-of-stay) can be derived from it, but doing so requires substantial wrangling, cohort definition, and a patient-grouped split, and it is credentialed-access (data-use agreement). It is already flagged 2nd Tier / '?'. A human must decide on a specific extracted task and target, handle the credentialing/access, and define the join and grouping before this could be promoted.
