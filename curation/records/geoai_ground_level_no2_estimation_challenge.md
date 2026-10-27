---
unique_name: geoai_ground_level_no2_estimation_challenge
name: geoai-ground-level-no2-estimation-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- Non-IID (Grouped)
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2024'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/geoai-ground-level-no2-estimation-challenge
- https://zindi.africa/competitions/geoai-ground-level-no2-estimation-challenge/data
source_row: 878
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 3: estimate daily ground-level NO2 at monitoring stations in Lombardy and Veneto from public satellite and weather data, scored on stations held out, a grouped task.
- Source: Zindi competition "GeoAI Ground-level NO2 Estimation Challenge" (ITU AI for Good with the GEOAIR project, 2024-05-22 to 2024-11-15, 370 on the leaderboard); "develop ML models to estimate surface NO2 concentrations using only public remote sensing data as predictor variables"; data: "Ground-truth data from air quality monitoring stations in the continental part of Lombardy and Veneto regions", Sentinel-5P TROPOMI NO2, CHIRPS precipitation and NOAA land surface temperature from Google Earth Engine; Train.csv, Test.csv, DataDescription.pdf. Rows not checked (Zindi login).
- Use case: an environmental agency estimates surface NO2 where no station measures it (exposure maps, monitoring); fit direct for estimation at unmonitored sites; regime grouped by station, because the source scores "in-situ data from selected ground stations not provided to participants" and states "The ground truth data used for evaluation are independent from the training data set" (`required_split` changed from Temporal to Grouped; a temporal component remains: models must hold "regardless of season").
- Siblings and duplicates: `geoai_challenge_for_air_pollution_susceptibility_mapping` (same series, Milan AQI maps, a different task); `no2` (OpenML, Norwegian road traffic NO2, a different dataset). External collections: none found; related paper on dense NO2 estimation from sparse stations and satellite data (arXiv 2504.17039).
- Papers and pages: https://zindi.africa/competitions/geoai-ground-level-no2-estimation-challenge (Zindi API read 2026-10-22); discussions 21512, 22132, 23436 (an unofficial third place: features from longitude and latitude, three towns removed as outliers, ensembles); GEOAIR outputs https://www.cirgeo.unipd.it/geoair/index.php?id=outputs.
- Metric: RMSE on `GT_NO2`, the Zindi Evaluation page ("The evaluation metric for this competition is Root Mean Squared Error"); leaderboard metric (MET-4); the jury also reported Pearson r and MAE. Inputs: none for the metric; the station id is needed for the grouped split (check it ships).
- Risks for /add-dataset: the satellite columns are retrieved physical quantities at the station point (TROPOMI NO2 column), which reads as a measurement (SEL-15) rather than image descriptors (SEL-13), to confirm; satellite gaps (clouds); whether the Zindi Test.csv holds other stations or other days of the same stations; coordinates and station identity as features under a grouped split (LEAK).
- Priority: gap + (grouped regime thin), use case 0 (the actor is not named by the source), source + (ITU, GEOAIR, a data description), shape + (daily station series over two regions, assumed thousands of rows), risk - (SEL-13 reading and the held-out design to confirm).

GeoAI Zindi challenge to estimate ground-level NO2 concentrations, tagged Non-IID (temporal). Unlike a pure horizon forecast this is an estimation/regression mapping task (predicting NO2 from satellite-column, meteorological and geospatial features), which could be a legitimate tabular regression if the inputs are tabularized. However it is geospatial/satellite-derived and may carry raster modality and heavy wrangling, and the split likely needs to be temporal or spatial. A human must inspect whether the features are genuinely tabular vs. raw raster, the target definition, and the appropriate split regime; place in 2nd tier pending that.
