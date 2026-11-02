---
unique_name: ncands_child_file
name: National Child Abuse and Neglect Data System (NCANDS) Child File
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: social science
problem_type: Binary Classification
source_links:
- https://doi.org/10.34681/3acz-h041
- https://www.ndacan.acf.hhs.gov/datasets/dataset-details.cfm?ID=306
- https://doi.org/10.34681/7gy0-e516
- https://doi.org/10.34681/dbm1-b519
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: the federal case-level file of every investigated child-maltreatment report, documented by NDACAN with a DOI per fiscal year; the task it offers (a CPS disposition or a removal) is the kind whose ethics the curators doubted on `swd`, and that question comes first (SEL-1).
- Source: Children's Bureau (ACYF, ACF, HHS), "National Child Abuse and Neglect Data System (NCANDS) Child File", distributed by NDACAN, one release per federal fiscal year: FFY 2024 (https://doi.org/10.34681/3acz-h041, DataCite 2025), FFY 2019 (https://doi.org/10.34681/7gy0-e516, 2021), FFY 2001 (https://doi.org/10.34681/dbm1-b519, 2004). As published: "Records are provided at the level of each child on a report, also known as the report-child pair", for the investigations or assessments that received a disposition in the year, submitted voluntarily by the states; child and perpetrator demographics, maltreatment types, dispositions, risk factors and services (NDACAN page of dataset 306); no row count on the page; the distributed version has "confidentiality protections and NDACAN-derived variables" and is ordered through a restricted-data request.
- Use case: NCANDS exists "for the purpose of tracking the volume and nature of child maltreatment reporting" (DataCite abstract, FFY 2019), not for prediction. The decision a model would touch is a caseworker's disposition or a removal, as screening tools in some US counties do (our reading); fit approximate, and the label is itself a worker's judgment under state-specific standards. Regime temporal by fiscal year, with states as groups (their definitions differ).
- Siblings and duplicates: `swd` (`No`, `Missing source information`; the comments say "social worker decisions, child abuse use case" and "Lennart: ethical questionable") is the record this was found for; no other record names NCANDS or NDACAN (searched). External collections: none among the records.
- Better data: found as better data for `swd`; no further search this run.
- Papers and pages: the NDACAN dataset page and the DataCite records; the codebook and the Children's Bureau's annual Child Maltreatment reports (not read).
- Metric: none found (NDACAN page, DataCite); the fallback `roc_auc` (MET-8); inputs none.
- Risks for /add-dataset: the ethics call first (SEL-1: a high-stakes decision on families, with demographics among the features); services, foster-care placement and other post-investigation fields are recorded after the disposition and go for a disposition task (USE-3); the target and how its codes map (substantiated or indicated against not, or removal; USE-5); report-child pairs repeat a child across reports and years (group on the child id if the release keeps one, SPLIT-24); state submissions differ (LEAK-13 to check); millions of rows a year (a `_1m` cap); restricted access with a data use agreement (EV-4, noted only).
- Priority: gap + (social science is thin), use case 0 (no decision named), source + (a federal file with DOIs and a codebook), shape + (millions of report-child pairs, coded fields, years and states), risk - (the ethics question and post-disposition fields): 3.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `swd`.
- as published: one row per report-child pair for every investigated or assessed maltreatment report that received a disposition in the year, all participating states; the NDACAN page gives no row count (the ...; target: the investigation or assessment disposition (substantiated or indicated against not), or a post-investigation service such as removal to foster care; access: request.
- Why: the same actor and judgement as swd (social workers' assessment of the risk to a child staying with the family, presented to courts), recorded as the official disposition, with features of the same kind known at the decision: child and perpetrator demographics, maltreatment types, child and caregiver risk factors, ...
- Adds: a federal administrative source with documentation and codebooks instead of 1,000 anonymous ordinal rows of unknown origin; millions of rows a year, many years, named features. Caveats: the ethics concern in the swd record applies at least as much (high-stakes decisions on families, known racial disparities in ...
