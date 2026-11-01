---
unique_name: nvss_natality_pregnancy_outcomes
name: NVSS Birth (natality) public-use data files
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.cdc.gov/nchs/data_access/vitalstatsonline.htm
- https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Dataset_Documentation/DVS/natality/UserGuide2024.pdf
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and previews of the published tables, NOT from a built dataset. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: the US birth-certificate file of NCHS (3,638,436 records for 2024, yearly files from 1968 to 2025), with checkbox outcomes taken from the medical record (gestational hypertension, eclampsia, ICU admission) next to pre-pregnancy risk factors; a real, documented register for the task `maternal_health_risk` stood for, though the outcomes are under-reported and many fields are filled at delivery.
- Source: National Center for Health Statistics (NCHS), National Vital Statistics System, natality public-use files (https://www.cdc.gov/nchs/data_access/vitalstatsonline.htm: US data 1968-2025, the 2025 zip 226 MB, one User's Guide per year, files "available for independent research and analyses" under the NCHS data use agreement). As published (User Guide 2024): a fixed-width flat file, one record per live birth, "Record count 3,638,436"; the 2003 revised certificate's items include pre-pregnancy diabetes and hypertension (RF_PDIAB, RF_PHYPE), gestational diabetes and hypertension (RF_GDIAB, RF_GHYPE), eclampsia (RF_EHYPE, all states since 2022), previous preterm birth, infertility treatment, previous cesarean, and maternal morbidity such as ICU admission (MM_AICU). Since 2005 "the public release micro-data natality file no longer includes geographic detail".
- Use case: none named by NCHS (vital statistics). A real one from obstetric practice: at the first prenatal visit a clinician rates the risk of a hypertensive disorder of pregnancy from history (age, BMI, chronic hypertension, diabetes, parity, previous preterm birth, infertility treatment) to decide on closer monitoring or prophylaxis; written by the curation, so the fit is approximate (live births only, checkbox outcomes). Regime temporal by birth year.
- Siblings and duplicates: `nchs_natality_birth_weight` is the same file with birth weight as the target (PROV-7, a distinct task; the curator may choose one natality task); `numom2b_pregnancy_outcomes` (nuMoM2b, 10,038 nulliparous women, adjudicated outcomes, by request) holds the same outcomes measured better for far fewer women; `maternal_health_risk` (`No (Retired)`) is the task it stands in for. External collections: none found.
- Better data: found as better data for `maternal_health_risk`; no further search this round.
- Papers and pages: the Vital Statistics Online page; the 2024 User Guide (https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Dataset_Documentation/DVS/natality/UserGuide2024.pdf), whose comparison with medical records finds that "some health and medical condition items on the birth certificate are likely underreported". Papers that model these outcomes on natality files were not searched: the session's web search budget ran out.
- Metric: none found (NCHS publishes statistics, no task), so the fallback `roc_auc` (MET-1, MET-8).
- Risks for /add-dataset: choose the target and keep only what is known at the first prenatal visit: labour, delivery, newborn, morbidity and other in-pregnancy items go (LEAK-10, USE-3), and the month prenatal care began, WIC and the payment source need a timing call; the checkbox outcome is under-reported, and the guide flags areas where "more than 25% of births occurred in facilities that reported no cases" of eclampsia (USE-5, a noisy target); fetal deaths sit in another file, so pregnancies lost before birth are missing; 3.6 million rows a year are over the 500k cap (a sample per year); no state or facility, so no grouped split.
- Priority: gap 0 (medical & healthcare and binary are not thin), use case 0 (written by the curation), source + (NCHS user guide and record layout), shape + (millions of births a year, mixed items, yearly files), risk - (an under-reported checkbox target and fields filled at delivery).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `maternal_health_risk`.
- as published: one row per US birth, about 3.6 million a year (figure from memory). Variables of the revised certificate: mother's age, race, education, pre-pregnancy height and weight (BMI), pre-pregnancy ...; target: an adverse pregnancy outcome, e.g. a hypertensive disorder of pregnancy (gestational hypertension or eclampsia), preterm birth, or maternal ICU admission; access: open.
- Why: The task maternal_health_risk stood for (pregnancy risk from maternal age, blood pressure and blood sugar), with the quantity measured better: an observed outcome instead of a risk level set 'with the help of medical experts'. Features of the same kind (age, hypertension and diabetes before pregnancy, BMI) known at ...
- Adds: A national register with a documented source in place of a retired file of 1,014 rows, two thirds copies, with no recoverable site or patient. Millions of births per year and many years for a temporal split. Gaps: no measured vital signs (blood pressure and glucose are history flags), and many fields are recorded at ...

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: the same natality files with two targets (`nchs_natality_birth_weight`; PROV-7, weigh). The curator keeps one, or both as distinct tasks.
