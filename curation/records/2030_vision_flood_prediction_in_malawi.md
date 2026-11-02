---
unique_name: 2030_vision_flood_prediction_in_malawi
name: 2030-vision-flood-prediction-in-malawi
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2019'
domain: environmental science & climate
required_split:
- '?'
problem_type: Regression
source_links:
- https://zindi.africa/competitions/2030-vision-flood-prediction-in-malawi/data
- https://zindi.africa/competitions/2030-vision-flood-prediction-in-malawi
source_row: 915
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: the flooded fraction of each ~1 km cell in southern Malawi for a flood event, from elevation, land cover and weekly rainfall; a fixed regression, not a series forecast, but only one event is labelled in the public train file.
- Source: Zindi, "UNICEF Arm 2030 Vision #1: Flood Prediction in Malawi", Dec 2019 to May 2020, sponsored by Arm and UNICEF (2030Vision) (https://zindi.africa/competitions/2030-vision-flood-prediction-in-malawi, read through Zindi's page API); as published: one Train.csv (7.1 MB) of ~1 km x 1 km cells (0.01 degree, X and Y centres) with "the fraction (percentage) of that rectangle that was flooded in 2015", mean elevation, dominant land cover (MODIS LC_Type1), and weekly precipitation "for 18 weeks beginning 2 months before the flooding" for both the 2015 and 2019 events; the test is the same cells' extent for cyclone Idai, March 2019 ("target_2019"), scored on Zindi. Rows not counted.
- Use case: "a machine learning model that helps predict the location and extent of floods in southern Malawi" (Description), for humanitarian preparedness (UNICEF; Zindi blog "Zindi solutions will help Malawi prepare better for flooding"); actor and decision not named, fit approximate: the rainfall covers the flood weeks, so it estimates extent at the event rather than ahead. Regime: by event (train 2015, test 2019) with strong spatial autocorrelation; with only 2015 labelled, our split would be spatially grouped within one event, which does not mirror a next flood.
- Siblings and duplicates: none among the records (searched malawi, flood); external collections: none found. A participant's repo (kmezhoud, learn_by_example, Flood_prediction_Malawi) claims 2015 and 2019 datasets: whether the 2019 labels are public is to check.
- Papers and pages: no paper; the competition's tabs, discussions 644, 646, 1241, 1363; a Kaggle U-Net baseline ("zindi-flood-in-malawi-unet-baseline") treats the cells as a raster.
- Metric: RMSE on the fraction ("The error metric for this competition is the Root Mean Squared Error", Evaluation tab); MET-4; inputs none.
- Risks for /add-dataset: the target is derived from satellite flood maps and the cells form a grid where a U-Net is a baseline: judge SEL-12 on what wins (the features are tabular); the 2019 labels; the split (one event, spatial blocks); many cells at 0 (a hurdle shape, per a moderator).
- Markers: the old `Missing source information` is refuted (Zindi, UNICEF and Arm, a documented page); `Time-series (Forecasting)` dropped: the target is an event's extent per cell, not future values of a series, though Zindi tags it "Forecast".
- Priority: gap + (a spatially grouped regime is thin), use case 0 (approximate, actor unnamed), source 0, shape + (thousands of cells, 20+ features, spatial structure), risk - (one labelled event, raster structure).

A Zindi flood-prediction challenge for Malawi with no descriptive comments. Flood prediction can be either a spatio-temporal forecast (excluded) or a fixed per-location/per-event risk classification on tabular hydrological/geospatial features (potentially viable). Without details the modality (it may rely on satellite/remote-sensing rasters rather than tabular features) and the target are unknown. A human must inspect whether the data is genuinely tabular and whether the task is a fixed prediction vs. a time-horizon forecast.
