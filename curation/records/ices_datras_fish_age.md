---
unique_name: ices_datras_fish_age
name: 'ICES DATRAS trawl survey age data (CA records: age, length, sex, maturity per sampled fish)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: Other
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://datras.ices.dk
- https://www.ices.dk/data/data-portals/Pages/DATRAS.aspx
- https://datras.ices.dk/WebServices/Webservices.aspx
- https://doi.org/10.17895/ices.pub.33972736
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: otolith-read ages of fish from ICES's maintained trawl-survey database, with length, sex, maturity, weight, area and time as features; a real, large and open version of the abalone task, which needs a species and survey chosen and a join to the haul records first.
- Source: ICES (International Council for the Exploration of the Sea), DATRAS, the Database of Trawl Surveys: "an online database of trawl surveys with access to standard data products"; "At present, there are more than 45 years of continuous time series data in DATRAS"; bottom-trawl surveys from the Baltic to Gibraltar, updated by national institutes and quality-checked on entry; open data under CC BY 4.0 by the ICES Data Policy; downloads, web services and the R package icesDatras (ices.dk DATRAS page). Record types HH (haul), HL (length-based) and CA (age-based: "Get age-based data such as sex, maturity, and age counts per length of sampled species", icesDatras `getCAdata`), linked by survey, haul, species and length class; ICES publishes a spreadsheet of all field definitions (DATRAS format description). Row counts of CA were not read.
- Use case: a stock-assessment scientist assigns ages to the unaged fish of a survey catch from length (and sex, maturity, weight, area), the age-length key the CA records feed; that is the field's practice but is not stated on the ICES pages read, so fit approximate. Regime grouped by survey or haul, or temporal by year.
- Siblings and duplicates: `abalone` (`No`, AHDS: "The larger part of the samples follows a deterministic function"); no other DATRAS or otolith record (`grep -il datras/otolith`). External collections: none found.
- Better data: found as better data for `abalone`; no further search this round.
- Papers and pages: the ICES DATRAS pages and format description, the icesDatras R documentation; the ICES library report "ICES Database of Trawl Surveys" (doi 10.17895/ices.pub.33972736; returned 403 here).
- Metric: none found (the ICES DATRAS pages and the icesDatras documentation define no prediction), so the regression fallback `rmse` on age in years (MET-8). Inputs none.
- Risks for /add-dataset: one species and one survey (or several, as groups) to pick, since the task differs by species (`Needs extensive data wrangling`); in some surveys a CA row is a count of fish per length and age class rather than one fish, so rows are expanded or weighted; ages are sampled per length class, so the length mix differs from the catch the use case ages (`Selection Bias` to weigh); individual weight and maturity are recorded only in some surveys and years; the join to HH for position, depth and date; age from length alone may be near trivial for a young, fast-growing species (TP-4 to probe).
- Priority: gap 0 (environmental and biology domains not thin), use case 0 (the age-length-key practice is not stated by the source read), source + (ICES, a maintained database with a format description), shape + (decades and many surveys, grouped and temporal structure), risk - (species and survey choice, count rows and joins before a table exists).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `abalone`.
- as published: age-based (CA) records from many surveys across 45+ years: age read from otoliths, length class, sex, maturity, individual weight where recorded, species, area, year and quarter. Counts were not ...; target: the age of a fish in years, read from its otolith; access: open.
- Why: Abalone predicts an animal's age, read from growth rings, from its body measurements so that the ring count can be skipped. DATRAS holds the same task with real ring-based age readings in a maintained public database.
- Adds: Real, traceable, maintained data with many species, regions and decades, against 4,177 abalone from one 1994 study. Gives grouped (survey, area) and temporal (year) structure. Caveats: the task is per species, so one species and survey would be picked; it needs a join of CA with HH (haul) records.
