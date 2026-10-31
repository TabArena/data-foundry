---
unique_name: epa_fuel_economy_vehicles
name: Fuel economy data for light-duty vehicles, model years 1984 to present (vehicles.csv)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
collections:
- STRABLE
original_source: GOV Website
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.fueleconomy.gov/feg/ws/index.shtml
- https://www.fueleconomy.gov/feg/epadata/vehicles.csv.zip
- '# NRCan Fuel Consumption Ratings (Canada), a related dataset of another publisher, not this record''s data'
- https://open.canada.ca/data/en/dataset/98f1a129-f628-4ce4-b24d-6f16bf24dd64
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: the official EPA and DOE fuel-economy file of every light-duty configuration since model year 1984, the measured MPG target of the old StatLib cars task at about 100 times its size; as for `stalib_cars`, the source names no decision for MPG from specifications, and the file holds several near-twins of the target.
- Source: U.S. Department of Energy and Environmental Protection Agency, fueleconomy.gov (administered by Oak Ridge National Laboratory), `vehicles.csv` (https://www.fueleconomy.gov/feg/epadata/vehicles.csv.zip), field list https://www.fueleconomy.gov/feg/ws/index.shtml. As published: one row per make, model, model year, engine and transmission from model year 1984; fields include `year`, `make`, `model`, `baseModel`, `VClass`, `drive`, `trany`, `displ`, `cylinders`, `eng_dscr`, `atvType`, `evMotor`, `sCharger`, `tCharger`, `startStop`, `guzzler`, and the target candidates `comb08` ("combined MPG for fuelType1"), `city08`, `highway08`, `UCity` and `UHighway` (unadjusted), `co2TailpipeGpm`, `fuelCost08`, `youSaveSpend`, `feScore`, `ghgScore`. The row count is not stated on the page (the Assessment's 48,000 is to verify).
- Use case: an engineer or analyst estimates a configuration's label fuel economy from its specification before the EPA test; fit approximate: no use is named by the source, and every vehicle sold gets a tested or derived label; regime temporal by model year.
- Siblings and duplicates: `fueleconomy_vehicles` (STRABLE's model-year-2025 cut of the same file with the target youSaveSpend; proposed `Duplicate` of this record, PROV-6, in screening batch 17); `fueleconomy_tax_incentives` (another fueleconomy.gov table, another task); `stalib_cars` (`TBD -> 2nd Tier`, `Outdated`, the 1983 ASA cars data whose MPG task this is). External collections: STRABLE (the 2025 cut; added to `collections`).
- Better data: found as better data for `stalib_cars` (the data-scouting run of 2026-10-30/31); no further search. The NRCan Fuel Consumption Ratings link in `source_links` is another publisher's data (Canada), noted there as related.
- Papers and pages: the fueleconomy.gov download and field pages; STRABLE (https://arxiv.org/abs/2605.12292).
- Metric: none found (the source defines no task), so the fallback `rmse` on `comb08`; inputs none.
- Risks for /add-dataset: drop the target's twins (`city08`, `highway08`, `UCity`, `UHighway`, `co2TailpipeGpm`, `fuelCost08`, `barrels08`, `youSaveSpend` and the scores; combined MPG is a weighting of city and highway, SEL-5, LEAK-10); MPG of model years 1985-2007 was recomputed with the 2008 method ("have been updated", footnote 2); electric and CNG rows give MPGe (footnote 11), another scale: filter or separate them; values derived for untested sister models near-duplicate tested rows (LEAK-16); CO2 before model year 2013 is estimated from an emission factor (footnote 5).
- Priority: gap 0, use case 0 (none named by the source), source + (DOE and EPA, documented fields), shape + (tens of thousands of configurations, mixed types, model years), risk - (twin targets, derived rows).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `stalib_cars`.
- as published: One row per vehicle configuration (make, model, year, engine, transmission); tens of thousands of rows (roughly 48,000, count not stated on the page, to verify) for model years 1984 to the current ...; target: Combined fuel economy (comb08, MPG) or tailpipe CO2 (g/mile), from EPA certification tests; access: open.
- Why: The StatLib 1983 ASA cars data (406 cars; its UCI sibling is Auto MPG) is built around MPG from engine and body specs; this is the same quantity, officially measured, with the same kind of spec features. Caveat: the OpenML copy (id 455) sets the target to origin, which has no use case; the hit fits the MPG task
- Adds: About 100x more vehicles, four decades up to the current model year, official test values, a model-year column for a temporal split. Risks: derived sister-model rows near-duplicate tested ones; MPG and CO2 are near-deterministic transforms of each other (keep one); EVs need separate handling. The Natural Resources ...
