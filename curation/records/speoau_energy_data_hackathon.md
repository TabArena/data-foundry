---
unique_name: speoau_energy_data_hackathon
name: speoau-energy-data-hackathon
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Missing source information
- TBD
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2024'
required_split:
- '?'
problem_type: Regression
source_links:
- https://zindi.africa/competitions/speoau-energy-data-hackathon/data
source_row: 956
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: a one-week student hackathon (SPE OAU, Nigeria, 2024): solar PV power output from environmental conditions, 2,920 rows x 10 features; the data's origin is not named.
- Source: Zindi, https://zindi.africa/competitions/speoau-energy-data-hackathon (read through the Zindi API on 2026-10-22), 27 January to 2 February 2024, 23 participants; as published: "The dataset comprises 2920 data points containing 10 features", "30% of the data reserved for testing"; Train.csv (121 KB), Test.csv (49 KB), VariableDescriptions.csv. Features named: "temperature, pressure, wind speed, humidity and other factors"; no site, period or provider named.
- Use case: the page: "predicting the output of solar power systems based on environmental conditions ... for the efficient daily and hourly management of power grid production"; actor a grid or solar-farm operator, in general terms; fit approximate. Regime: temporal if the rows are a time series of one or a few plants (2,920 = 365 x 8, three-hourly for a year, is a guess); the columns could not be read without a login.
- Siblings and duplicates: `speoau_data_hackathon` (same host, electricity price, a different task). Possibly a cut of a public PV table such as the Northern Hemisphere horizontal PV data of Pasion et al. (2020, Mendeley hfhwmn8w24, 12 sites, the same weather variables); unconfirmed, check by rows (PROV-4). External collections: none found.
- Papers and pages: none beyond the Zindi page.
- Metric: RMSE, the Zindi Evaluation page ("The evaluation metric for this competition is Root Mean Squared Error"); deliberate (MET-4); inputs none.
- Risks for /add-dataset: origin (PROV-1, PROV-2; `Missing source information` kept as the open question), a likely re-upload, measured weather at the same time as the output (fine for a nowcast, a leak for a day-ahead forecast), small after the split.
- Priority: gap - (no thin value), use case - (generic), source - (origin not named), shape + (2,920 rows, about 2,000 to train), risk - (unknown origin, likely a cut of another table).

A Zindi 'speoau-energy-data-hackathon' with no details in the record. Energy hackathons frequently turn out to be consumption/generation forecasting, which would be out of scope, but it could also be a fixed predictive task. There is too little information to judge the target, modality, or split regime. A human must inspect the Zindi competition to confirm whether it is forecasting (reject) or a genuine fixed-target tabular regression/classification.
