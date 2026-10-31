---
unique_name: fueleconomy_vehicles
name: Vehicles
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
collections:
- STRABLE
source_links:
- https://www.fueleconomy.gov/feg/download.shtml
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/vehicles
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Duplicate`, PROV-6): a model-year-2025 cut (1,238 vehicles) of the fueleconomy.gov vehicles file that `epa_fuel_economy_vehicles` records in full (1984 on), with the target swapped to youSaveSpend, a 5-year fuel-cost difference that fueleconomy.gov computes from the vehicle's fuel economy and fuel prices: the same fuel-economy task, no distinct one.
- Source: DOE/EPA fueleconomy.gov vehicles data (https://www.fueleconomy.gov/feg/download.shtml, vehicles.csv; field list https://www.fueleconomy.gov/feg/ws/index.shtml): "youSaveSpend - you save/spend over 5 years compared to an average car ($). Savings are positive; a greater amount spent yields a negative number"; "fuelCost08 - annual fuel cost for fuelType1 ($) (7)", with note (7): "Annual fuel cost is based on 15,000 miles, 55% city driving, and the price of fuel used by the vehicle."
- STRABLE's cut (scripts/script_preprocess_data/preprocess_fueleconomy-vehicles.py): fuel-economy_vehicles.csv filtered by `data[(data.year>2024)&(data.year<2026)]`, the MPG, fuel-cost, range, CO2, displacement and cylinder columns dropped: 1,238 rows x 29 columns, target youSaveSpend (64 distinct values in steps of $250).
- Siblings and duplicates: `epa_fuel_economy_vehicles` (the same file, all model years, target combined MPG; found as better data for `stalib_cars`) is the canonical record; `fueleconomy_tax_incentives` (another fueleconomy.gov table). External collections: STRABLE ("Vehicles", App. C.2: "to predict the annual fuel cost").
- Better data: a candidate of the benchmark STRABLE (the run searched no further).
- Metric: none found; STRABLE scores R^2 (App. D.1).
- Also: the target is a published formula of fuel economy and fuel price (SEL-5); with its inputs dropped, what remains is the sibling's MPG task on one model year.
- Reject check (AI, 2026-10-31): stands. STRABLE's script reads fuel-economy_vehicles.csv, keeps `data[(data.year>2024)&(data.year<2026)]` and sets target youSaveSpend (https://github.com/soda-inria/strable/blob/main/scripts/script_preprocess_data/preprocess_fueleconomy-vehicles.py). fueleconomy.gov computes that target from the fuel cost, 'based on 15,000 miles, 55% city driving, and the price of fuel' (https://www.fueleconomy.gov/feg/ws/index.shtml). So this is one model year of the vehicles.csv that epa_fuel_economy_vehicles records in full, with a swapped target that is a formula of that record's MPG task. STRABLE is already on the canonical record.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 1,238 rows x 29 columns incl. target (STRABLE parquet); target: youSaveSpend.
- Why: Predict a vehicle's 5-year fuel cost saving/spending relative to an average car
- Notes: fueleconomy.gov vehicles file; 1,238 rows (a subset). youSaveSpend is computed by fueleconomy.gov from fuel economy and fuel prices, so check for formula inputs among the features (AHDS risk).
