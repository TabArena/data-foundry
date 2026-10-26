---
unique_name: geoai_challenge_for_air_pollution_susceptibility_mapping
name: geoai-challenge-for-air-pollution-susceptibility-mapping
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Needs extensive data wrangling
- TBD
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2023'
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: Other
source_links:
- https://zindi.africa/competitions/geoai-challenge-for-air-pollution-susceptibility-mapping/discussions
- https://zindi.africa/competitions/geoai-challenge-for-air-pollution-susceptibility-mapping/data
source_row: 891
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: a small ITU GeoAI challenge to map seasonal AQI classes of Milan in 2022 from station series and terrain layers; the target must be built from the pollutants and the scored unit is unclear.
- Source: Zindi competition "GeoAI Challenge for Air Pollution Susceptibility Mapping" (ITU AI for Good, 2023-07-21 to 2023-10-14, 35 on the leaderboard); "The challenge is to implement a machine learning method which can accurately estimate the pollution levels (AQI) of the city of Milan during 2022 ... the expected output are the seasonal (spring, summer, autumn, and winter) AQI susceptibility maps during 2022"; data: daily meteorological series 2016-2022, daily pollutant series 2016-2021 (NOx, SO2, CO, O3, PM2.5, PM10, benzene) at the stations, terrain, land cover and geology at the stations and on a 100 m grid; files Train.csv, Test.csv, four `meteo_<season>_2022.csv`, `air_pollution_Milan_Comune_topo_only.csv`. The AQI target is to be computed by the participant from the EEA guidelines ("must be used to prepare the data").
- Use case: the city of Milan maps where pollution is likely high ("support decision-making to improve the resilience of the city"); fit approximate (no actor or decision named); regime temporal (train 2016-2021, score 2022) and spatial (interpolation between stations).
- Forecasting (SEL-10)? Zindi tags the problem "Forecast", but the 2022 meteorology is given and the output is a seasonal map, an estimation rather than future values of a series; not a clear reject from the source's words, so it stays with the doubt noted.
- Siblings and duplicates: `geoai_ground_level_no2_estimation_challenge` (same ITU GeoAI series, Lombardy and Veneto NO2 from satellite data, a different task); `geoai_challenge_for_cropland_mapping_in_dry_environments`; `no2` (OpenML Norwegian traffic NO2, unrelated). External collections: none found.
- Papers and pages: https://zindi.africa/competitions/geoai-challenge-for-air-pollution-susceptibility-mapping (Zindi API read 2026-10-22); the GEOAIR project of the University of Padova (https://www.cirgeo.unipd.it/geoair/) runs the GeoAI challenges.
- Metric: accuracy on the AQI class (1 to 5), the Zindi Evaluation page ("The error metric for this competition is Accuracy"); leaderboard metric (MET-4); inputs none.
- Risks for /add-dataset: the target has to be built (AQI from up to five pollutants, by station type); few stations, so the task may be `Too Small` (TP-5); Test.csv rows and their unit (station-season or grid point) not checked; `problem_type` changed from Regression to Multiclass Classification (the source scores AQI classes by accuracy).
- Priority: gap 0, use case 0, source + (ITU and the GEOAIR project document the data), shape 0 (size unknown, likely small), risk - (target to build, unclear unit).

GeoAI Zindi challenge whose stated task is to predict the pollution levels (AQI) of Milan over a year, flagged as time-series in the record. This is forecasting air-quality values over a temporal horizon, which is explicitly out of scope. The data is also geospatial/satellite-derived, adding a non-tabular modality concern. On the stated framing this is a forecasting exclusion; a human need only confirm there is no static reframing before final rejection.

---

predict the pollution levels (AQI) of the city of Milan during 202

time-series
