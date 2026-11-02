---
unique_name: localised_precipitation_forecasting_in_brazzaville_in_republic_of_congo_using_ai
name: localised-precipitation-forecasting-in-brazzaville-in-republic-of-congo-using-ai
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Time-series (Forecasting)
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2025'
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://zindi.africa/competitions/localised-precipitation-forecasting-in-brazzaville-in-republic-of-congo-using-ai
- https://power.larc.nasa.gov/
source_row: 948
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: a same-day precipitation estimate from NASA POWER gridded daily data for one location, not clearly a forecast, with no decision behind it.
- Source: Zindi hackathon "Localised Precipitation Forecasting in Brazzaville Using AI", 10-31 July 2025, open only to Congolese nationals and students at Congolese universities (Zindi API, rules page). The Data page says: "The data is sampled from the Source Native Resolution Daily Data collected by NASA/POWER from January 01, 2010 to January 01, 2024. It includes weather observations from Brazzaville." Files: Train_data.csv (304,839 bytes), Test_data.csv (123,272 bytes), VariableDefinitions.csv (361 bytes), so roughly 5,100 days with fewer than 10 variables. The column list was not read (it needs a login).
- Use case: the description names urban planning, agriculture, water management and flood prevention, with the goal "predict daily or sub-daily precipitation levels in Brazzaville using meteorological and spatio-temporal data". No actor or decision is named, and nobody acts on a same-day rainfall estimate made from other same-day POWER variables, because POWER publishes the precipitation itself. Fit: approximate at best. Regime: temporal (one daily series), but the sample IDs on the Evaluation page (`ID_ZdrVnE_20110615`, `ID_MdWBtU_20230910`) suggest the test days are interleaved with the training span rather than a future horizon.
- Siblings and duplicates: none in `curation/records/` (searched for brazzaville and NASA POWER). External collections: none known.
- Papers and pages: Zindi page only. NASA POWER (https://power.larc.nasa.gov/) is the upstream source. POWER's daily meteorology comes from the MERRA-2 reanalysis and its precipitation from a gridded product, so features and target are model or satellite estimates for one grid cell, not station readings.
- Metric: RMSE, on the Zindi Evaluation page ("The evaluation metric for this competition is Root Mean Squared Error"; API `error_metric: root_mean_squared_error`). A leaderboard metric (MET-4). Inputs: none.
- Risks for /add-dataset: whether lagged values make this a forecast of a series (SEL-10; the old `Time-series (Forecasting)` marker stays as the open concern); gridded reanalysis inputs and target (SEL-16 / PROV-3 to weigh); a single series of about 5k days with a few weather variables, so `Too Small` is unlikely but the task may be close to `Trivial` (humidity and pressure against rain).
- Priority: gap - (environmental science, regression, temporal: none thin), use case - (no actor or decision), source + (NASA POWER is documented), shape - (one grid cell, about 5k days, few features), risk - (forecast framing, model-generated values); floor 1.

A Zindi competition whose name explicitly states localised precipitation forecasting for Brazzaville. Forecasting future precipitation values over a horizon is time-series forecasting, which is explicitly excluded from the benchmark scope. The name alone strongly signals a forecasting task rather than a fixed predictive task that merely needs a temporal split. A human could double-check whether it is framed as nowcasting from concurrent features (which might change the verdict), but on the name and typical framing this is a No.
