---
unique_name: carbon_dioxide_prediction_challenge
name: carbon-dioxide-prediction-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2023'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/carbon-dioxide-prediction-challenge
- https://zindi.africa/competitions/data-journey-nairobi
- https://zindi.africa/competitions/indabax-zambia-2023
- https://zindi.africa/competitions/ey-carbon-prediction-hackathon/data
- https://zindi.africa/competitions/umojahack-africa-2023-beginner-challenge
source_row: 967
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: Sentinel-5P pollutant columns per location-week against a modelled emission inventory; a spatial split, but the target is a model product.
- Source: first run as the Ernst & Young Carbon Prediction Competition on Zindi (2023-02-23 to 2023-05-01); the same data and pages were reused in UmojaHack Africa 2023 (beginner, 2023-03), IndabaX Zambia 2023, Data Journey Nairobi (2023-06) and the 2024 Carbon Dioxide Prediction Challenge (child of the UmojaHack page): one dataset, five competition pages, all in `source_links`. As published: `Train.csv` / `Test.csv`, IDs `ID_LAT_LON_YEAR_WEEK`, about 800 locations in 20 areas of South Africa (train 361 locations, test 137), weekly 2019-01 to 2022-11, seven Sentinel-5P products (SO2, CO, NO2, HCHO, UV aerosol index, O3, cloud) with sub-features, target `emission` "collected from GRACED and EDGAR".
- Use case: governments and others "estimate carbon emission levels across Africa, even in places where on-the-ground monitoring is not possible" (the source's words); fit approximate, because the target is itself a gridded inventory estimate (GRACED, EDGAR) that already covers those places; regime grouped by location (the source: "The test set is from a different province to the train set"), with a weekly time axis.
- Siblings and duplicates: the five Zindi pages are one dataset (kept in one record); `zindi_weekendz_layerai_air_quality_prediction_challenge` and `urban_air_pollution_challenge` use Sentinel-5P for other targets (AI-screened, no human verdict). The Kaggle Playground S3E20 (Rwanda CO2) uses a similar Sentinel-5P setup on other locations (not checked). External collections: none found.
- Papers and pages: https://zindi.africa/competitions/ey-carbon-prediction-hackathon (first), https://zindi.africa/competitions/carbon-dioxide-prediction-challenge.
- Metric: rmse (every page's Evaluation: "The error metric for this competition is the Root Mean Squared Error"), a leaderboard metric (MET-4); inputs none.
- Risks for /add-dataset: the target is a model output (GRACED/EDGAR), which may make it a smooth per-location profile (TP-10 naive-profile check, SEL-16 question whether a modelled target is real); Sentinel-5P L3 values are retrieved column densities (SEL-15 measurement rather than SEL-13, to confirm); lat/lon in the ID; which of the five releases to take.
- Priority: gap + (grouped regime thin), use case - (fit approximate), source - (Zindi pages only), shape + (about 80k location-weeks, ~70 features, grouped and temporal), risk - (modelled target).

Zindi CO2/carbon-emissions prediction challenge (several linked competition variants, including an EY carbon hackathon). Such challenges frequently derive features from satellite products (e.g. Sentinel-5P) over geographic locations and time, which raises both a remote-sensing/geospatial modality concern and a possible spatio-temporal/forecasting framing rather than a clean IID tabular regression. The underlying task could still be a fixed regression on engineered tabular features, so it is not an automatic reject. A human must determine which competition variant is intended, whether the features are tabular engineered covariates versus raw imagery, and whether the split is IID, temporal, or spatial.
