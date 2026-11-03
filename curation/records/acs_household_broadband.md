---
unique_name: acs_household_broadband
name: American Community Survey Public Use Microdata Sample (household internet subscription)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
original_source: GOV Website
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.census.gov/programs-surveys/acs/microdata.html
- https://api.census.gov/data/2023/acs/acs1/pums/variables/HISPEED.json
- https://api.census.gov/data/2023/acs/acs1/pums/variables/ACCESSINET.json
- https://microdata.worldbank.org/index.php/catalog/6279
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: open ACS microdata with a household broadband-subscription item, proposed as an open stand-in for the Togo fiber-uptake challenge; no source defines a prediction task on it, and the household reports the target in the same interview as the features.
- Source: US Census Bureau, ACS PUMS 1-year files (annual; internet-subscription items since the 2013 survey per the scout, not re-checked; latest 2024). As published: housing and person files joined by SERIALNO, about 1% of US housing units a year, geography down to PUMA. Targets: HISPEED, "Broadband (high speed) Internet service such as cable, fiber optic, or DSL service" (1 yes, 2 no, 0 for group quarters, vacant units or no paid access, 8 "Suppressed for data year 2023 for select PUMAs"; ACS API variable page, 2023), or ACCESSINET (paid internet access).
- Use case: none named by any source. The scout's reading, a state broadband office or a provider targeting adoption subsidies or marketing from household characteristics, is written by the curation and does not count (USE-1). The Togo challenge's operator task is the closest real one, on other data; the fit would be approximate at best (US households, and service availability is not in the data, so uptake mixes demand and supply); regime temporal by survey year if kept.
- Siblings and duplicates: `togo_fiber_optics_uptake_prediction_challenge` (Zindi; `No`, Andrej: "Data distribution explicitly not allowed", a licence reason that EV-4 no longer accepts); the ACS siblings `acs_food_stamps_2014_2024`, `food_stamps` and `folktables_acs_income` (other targets of the same survey, PROV-7); `adult` and `census_income` are `No` with `No Good Target / Scientific Discovery` ("no actor decides on whether income exceeds 50K"), the closest precedent. External collections: none found (not a folktables or TableShift task).
- Better data: found as better data for `togo_fiber_optics_uptake_prediction_challenge`; no further search this round. The scout also named the Togo EHCVM household surveys of 2018-19 and 2021-22 (World Bank microdata catalog 6279) as a same-country alternative, internet variables not checked.
- Papers and pages: the ACS PUMS documentation and API variable pages; no paper found that defines HISPEED prediction as a task (web search ran out in this pass, so this was not searched further).
- Metric: none found (no task definer), so the fallback `roc_auc` (MET-1, MET-11).
- Risks for /add-dataset: settle the task before any work: the target is a survey answer the household knows (SEL-7) and no source defines the task (SEL-3, `No Good Target (yet)`), in line with `adult`; HISPEED is 0 for households without paid access and suppressed in some PUMAs in 2023 (define the population); a household-person join; computer, smartphone and other internet items of the same interview are near-proxies of the target (LEAK-10).
- Priority: gap 0, use case 0 (written by the curation), source +, shape + (over a million households a year, mixed types, annual waves), risk - (no defined target, SEL-3 and SEL-7 open).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `togo_fiber_optics_uptake_prediction_challenge`.
- as published: about 1% of US housing units per 1-year file (over a million housing-unit records per year, not counted), household and person files joined by SERIALNO; geography down to PUMA; target: HISPEED: the household subscribes to broadband such as cable, fiber optic or DSL (or ACCESSINET: paid internet access, yes/no); access: open.
- Why: the same target as the Togo challenge (does a household take up fixed internet, AUC-scored) with socio-demographic and geographic features of the same kind, on open data, whereas the Zindi data may not be redistributed
- Adds: open and redistributable, about a thousand times more households, a decade of annual waves (temporal split possible). Caveats: US not Togo; availability is not in the data (uptake mixes demand and supply); HISPEED is suppressed (code 8) in some PUMAs for 2023. Same-country alternative: Togo EHCVM 2018-19 and 2021-22 ...
