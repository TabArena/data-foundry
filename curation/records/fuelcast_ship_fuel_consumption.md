---
unique_name: fuelcast_ship_fuel_consumption
name: 'FuelCast: ship fuel consumption under operational and environmental conditions'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Other
year: '2025'
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://huggingface.co/datasets/krohnedigital/FuelCast
- https://arxiv.org/abs/2510.08217
- https://doi.org/10.1007/978-3-032-15535-1_4
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: Coriolis-metered fuel consumption of three ships (two cruise ships, one offshore supply ship) at 5-minute resolution over 3 to 12 months, with speed and reanalysis weather, published by KROHNE Digital as a tabular regression benchmark with blocked temporal folds (FuelCast, 2025); an estimate of the consumption at the same moment, not a forecast, but the release also holds per-consumer fuel and shaft power columns that give the target away.
- Source: Viga, Mueck, Löser, Weis, "FuelCast: Benchmarking Tabular and Temporal Models for Ship Fuel Consumption", arXiv 2510.08217 (2025-10-09), ECML PKDD 2025 workshop on Advanced Analytics and Learning on Temporal Data, LNCS (2026), https://doi.org/10.1007/978-3-032-15535-1_4; data on Hugging Face (krohnedigital/FuelCast, CC BY-NC-ND 4.0), one subset per ship. As published (Sec. 3, Table 1): CPS Triton (small cruise ship) 25,351 rows over three months, CPS Poseidon (large cruise ship) 105,422 rows over 12 months, OSS Ceto (offshore supply ship) 43,213 rows over six months; operational data "with a sample rate of five minutes", hourly weather interpolated linearly; target the "total momentary fuel consumption of all consumers on the vessel" (kg/s) from "KROHNE Coriolis mass-flow meters" (inlet minus outlet per engine). The files also hold per-consumer fuel (boilers, generator engines), propeller shaft power and torque, heading, bearing, speed over ground and sea-floor depth. The paper's inputs: ten features (speed over ground, sea-floor depth, air temperature, current, wind and wave speed, height, period and direction, directions turned into the ship's frame), chosen "based on physical knowledge and manual feature importance analysis".
- Use case: a ship operator's performance monitoring and what-if runs: the expected consumption for a speed and the conditions, against which past overconsumption is found, and fuel-efficient operation (the paper's Applications section; Task 1 "can support decisions in steady cruising conditions"). Fit direct for monitoring (metered fuel, measured conditions at the same time), approximate for voyage planning (the weather would be a forecast). Not forecasting: Task 1 is "a pointwise prediction based solely on features observed at a single time step", and k-step-ahead forecasting is named as future work (SEL-11). Regime temporal: the paper's "5 disjoint temporal intervals of equal length", each a test fold, with training on all other intervals (SPLIT-19 against SPLIT-11's expanding window, to decide).
- Siblings and duplicates: no ship or maritime fuel record (`epa_fuel_economy_vehicles` holds car ratings). External collections: none in our vocabulary.
- Better data: from the curator's Zotero collection (items 8 and 145); no search for better data in this run.
- Papers and pages: the FuelCast paper (TabPFN with 1,000 context rows best on average, Task 1 MAE 0.040 kg/s and R² 0.742, Tables 3-4); the Hugging Face card (only its schema and licence loaded).
- Metric: the paper reports MAE and R² for every model and ranks its summary by MAE without naming a criterion: borderline MET-5, `mae` (kg/s) if read as its choice, else the fallback `rmse` (MET-8). Inputs none.
- Risks for /add-dataset: the per-consumer fuel columns (the target is their sum) and the propeller shaft power and torque (the engines' output at the same moment) give the target away and go (LEAK); one dataset per ship, or one with the ship as a column (three ships are too few groups for a grouped split, SPLIT-3; PROV-7 if three tasks); 5-minute rows are strongly autocorrelated, so test windows are blocks; weather is hourly reanalysis; port and idle periods (near-zero speed) to keep or drop by the use case; the licence forbids derivatives (no criterion, EV-4). Domain left empty: the vocabulary has no transport value.
- Priority: gap 0 (regression and temporal are not thin; no maritime domain value), use case + (monitoring and what-if use named by the source, direct for monitoring), source + (paper and the metering company's own release), shape + (25,000 to 105,000 rows per ship over months), risk - (leaky columns in the release and a task per ship to choose).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 145: "FuelCast: Benchmarking Tabular and Temporal Models for Ship Fuel Consumption"; the curator's Zotero collection, item 8: "FuelCast: Benchmarking Tabular and Temporal Models for Ship Fuel Consumption".
- as published: 3 ships at 5-minute resolution: CPS Poseidon (cruise, 70,000 GT) 105,422 x 65 over 12 months; OSS Ceto (offshore supply) 43,213 x 46 over 6 months; CPS Triton (cruise, 11,000 GT) 25,351 x 62 over 3 ...; target: Consumer_Total_MomentaryFuel: total momentary fuel consumption of all consumers (kg/s, Coriolis mass-flow meters); access: open.
- Why: Real metered fuel, not noon reports, published as a tabular-regression task with a blocked temporal 5-fold protocol. The inputs are concurrent conditions, with no lagged target. | real onboard sensor data joined with Copernicus/OpenMeteo weather, published as a tabular regression benchmark
- Adds: A maritime energy domain and a temporal/blocked regime with three ships (one task per ship, or ship as a group). Checks: drop the per-consumer fuel and shaft-power columns and the propeller power/torque columns (they leak); the 5-minute rows are autocorrelated; weather is reanalysis interpolated from hourly data; ...
