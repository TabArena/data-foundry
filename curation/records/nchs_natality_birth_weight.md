---
unique_name: nchs_natality_birth_weight
name: NCHS Natality (birth certificate) public-use data files, US births 1968-2025
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: medical & healthcare
original_data_state: One Table
source_links:
- https://www.cdc.gov/nchs/data_access/vitalstatsonline.htm
- '# NBER copies of the files (CSV, Stata, SAS) and codebooks for 2018-2022'
- https://www.nber.org/research/data/vital-statistics-natality-birth-data
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: the US birth register (about 3.6 million births a year, open public-use files for 1968-2025 with a user guide per year), birth weight predicted from what is known early in pregnancy; documented and very large, but the fields known only at or after delivery have to go and the task is ours to define.
- Source: NCHS, National Vital Statistics System, Birth (natality) public-use files (cdc.gov/nchs/data_access/vitalstatsonline.htm): one file per data year 1968-2025, each with a User's Guide; the 2025 U.S. file is a 226 MB zip of fixed-width records; the files are for "independent research and analyses" under a Data Users Agreement (agreement text not read). NBER mirrors them as CSV, Stata and SAS, with codebooks for 2018-2022, and notes that the public files "from 2005-on [do] not include geographic detail due to restrictions imposed by the states". As published: one row per live birth (about 3.6 million a year from NCHS reports; not counted on a file); the revised (2003) certificate holds the mother's age, race, education, pre-pregnancy weight and BMI, cigarettes before pregnancy, previous preterm birth, pre-pregnancy diabetes and hypertension, infertility treatment and plurality, and the outcomes birth weight in grams, gestational age, Apgar and delivery method (variable names such as DBWT to verify on the user guide, which could not be read as text here).
- Use case: an obstetric provider at the first prenatal visit estimates the risk of a baby under 2,500 g, to plan closer monitoring; the source names no such use (vital statistics), so the fit is approximate (USE-8): the certificate records the risk factors at delivery. Regime temporal by data year (fit on past births, score the next year).
- Siblings and duplicates: `lowbwt` (`No`, BNG rows generated from Hosmer and Lemeshow's 189 mothers); `nvss_natality_pregnancy_outcomes` (unscreened) holds the same files with another target (hypertensive disorder, preterm birth): one source, distinct tasks (PROV-7), so the curator picks the target or targets. External collections: none found.
- Better data: found as better data for `lowbwt`; no further search this round.
- Papers and pages: the NCHS User's Guides per year; Dola and Valderrama, "Exploring parental factors influencing low birth weight on the 2022 CDC natality dataset", BMC Med Inform Decis Mak 24:367, 2024 (doi 10.1186/s12911-024-02783-x; abstract only: five models on the 2022 file, a risk-factor study).
- Metric: none found (the NCHS page is documentation; the 2024 paper's abstract names no metric, its text was not reached), so the fallback: `rmse` on grams, or `roc_auc` on the under-2,500 g flag (MET-1, MET-8); inputs none.
- Risks for /add-dataset: drop what is known only at or after delivery (gestational age, Apgar, delivery method, labour items, gestational diabetes and hypertension, weight gain, number of prenatal visits; LEAK-10, USE-3); plurality and the month prenatal care began need a call on the prediction point; pick the target (grams or the flag) and the years; millions of rows a year need a subsample; the 2003 certificate was adopted state by state until 2016, so earlier years mix two forms; the data-use terms forbid re-identification (no criterion, EV-4).
- Priority: gap 0 (medical, regression and temporal are not thin), use case 0 (ours, not the source's), source + (NCHS, a user guide per year), shape + (millions of births, mixed types, many years), risk - (many delivery-time fields to drop, a target and years to choose).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `lowbwt`.
- as published: one row per live birth, about 3.6 million per year (figure from NCHS birth reports, verify on the file); fixed-width flatfiles (2025 zip 226 MB) with user guides per year; public-use files have no ...; target: infant birth weight in grams (DBWT), or low birth weight under 2,500 g; access: open.
- Why: same target and use case as the 189-mother Hosmer-Lemeshow study behind BNG(lowbwt) (birth weight from maternal risk factors), with features of the same kind known at the first visit: mother's age, race, pre-pregnancy weight and BMI, smoking before pregnancy, previous preterm births, chronic hypertension, ...
- Adds: real records instead of rows sampled from a Bayesian network; millions of births per year against 189 mothers; 2016-2025 for a temporal split. Must drop what is known only at or after delivery (gestational age, delivery method, Apgar, gestational hypertension and diabetes if diagnosed late, plurality if not known ...

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: the same natality files with two targets (`nvss_natality_pregnancy_outcomes`; PROV-7, weigh). The curator keeps one, or both as distinct tasks.
