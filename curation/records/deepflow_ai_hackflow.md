---
unique_name: deepflow_ai_hackflow
name: deepflow-ai-hackflow
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- Missing source information
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2023'
required_split:
- '?'
problem_type: Regression
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/deepflow-ai-hackflow/data
source_row: 974
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: a building-energy regression whose columns read like the inputs of a parametric energy simulation, with no named origin; likely `No` under SEL-16 or PROV-1 once the data is seen, but the page does not say it is simulated.
- Source: Zindi hackathon "DeepFlow - AI HackFlow", Tunisia, 6-7 May 2023 (https://zindi.africa/competitions/deepflow-ai-hackflow); as published: "78 000 entries", Train.csv (30.3 MB) and Test.csv (12.2 MB), target "Operational Energy"; columns `building`, `File` ("a file name for the building shape"), setpoints, cooling and heating COP, WWR, thermal resistances (wall, roof, floors, windows), infiltration, boiler efficiency, internal mass, permeability, occupancy, `Town`, and "random load measures"; IDs like `Building_10005_Town_2`. No data provider is named; the licence is CC-BY SA 4.0 (rules page).
- Use case: the page names designers optimising a building "before building construction" (early-stage energy prediction); that is a surrogate for a simulation, not a measured outcome; regime grouped by `Town` would be the natural check if the data were real.
- Siblings and duplicates: none in `curation/records/` (`nyc_building_energy_and_water_data_disclosure_for_local_law_84_2022_present` is measured NYC benchmarking data, another source). External collections: none found; two web searches on the column names found no upstream dataset.
- Papers and pages: none found.
- Metric: RMSE, Zindi Evaluation page ("The error metric for this competition is the Root Mean Squared Error"); a leaderboard choice (MET-4); inputs none.
- Risks for /add-dataset: PROV-3 / SEL-16 (a design-parameter grid with a "building shape" file per row and "random load measures" points at an EnergyPlus-style parametric study: check the value grids, duplicates per parameter and whether the target is a deterministic function of the inputs); PROV-1 (no provider named); `EUI` is energy per floor area and with `Total Floors Area` may give the target away (LEAK).
- Metadata filled from the page: problem type Regression, year 2023, one table.
- Priority: gap 0, use case 0 (design-stage surrogate), source 0 (no provider, no codebook beyond the page), shape + (78,000 rows, about 30 columns), risk - (likely simulated, EUI leak): 1.

Zindi 'deepflow-ai-hackflow' competition with no description, comments, or metadata in the record, so task type, target, domain, modality, and size are all unknown. The 'deep ... flow' naming gives no reliable signal and Zindi competitions span tabular, image, and forecasting tasks. Insufficient information to assess, and that alone is not a rejection reason. A human must inspect the competition page to determine modality, task, target, size, and split.
