---
unique_name: urban_air_pollution_challenge
name: Urban Air Pollution Challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/urban-air-pollution-challenge
source_row: 1024
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 2: same-day PM2.5 estimation for cities worldwide from Sentinel-5P gas columns and GFS weather, test on other locations; not forecasting, so the old `Time-series (Forecasting)` marker is dropped.
- Source: #ZindiWeekendz hackathon "Urban Air Pollution Challenge", 10-12 April 2020, with the World Air Quality Index project and Microsoft (236 participants; read through Zindi's API, <https://zindi.africa/competitions/urban-air-pollution-challenge>); as published: Train.csv (37,182,338 B, 349 locations, about three months from 2020-01-02), Test.csv (19,024,059 B, "covers 179 different locations", no target), SampleSubmission.csv; target the daily mean PM2.5 from ground sensors (WAQI); inputs GFS humidity, temperature and wind and every band of the Sentinel-5P L3 products from Google Earth Engine (NO2, CO, SO2, O3, HCHO, CH4, aerosol index, cloud), one table keyed by `Place_ID X Date`.
- Use case: "finding ways to track air quality and how it is changing, even in places without ground-based sensors" (Description): estimate today's PM2.5 for a place without a monitor; no actor named, fit approximate; regime grouped by place (the test holds other locations; SPLIT-3), not temporal: the target is the same-day level, not a future value (SEL-10 does not apply), so `required_split` changes from the AI-filled `Temporal (NON-IID)` to `Grouped (NON-IID)`.
- Siblings and duplicates: `urban_air_pollution_challenge_daust_students` is a 2024 re-run with this competition as Zindi `parent` and identical file sizes (a duplicate, proposed `No`); the same kind of task on other data: `airqo_african_air_quality_prediction_challenge` (2024, 8 African cities, AI `TBD -> Yes`, priority 4), `layerai_air_quality_prediction_challenge` (AI `TBD -> Yes`, priority 3) and `zindi_weekendz_layerai_air_quality_prediction_challenge`; a curator may want one or two Sentinel-5P PM2.5 tasks, and this one has by far the most locations. External collections: none found.
- Papers and pages: the Zindi Description, Data and Evaluation tabs; winners' code on GitHub per the rules, not read; no paper.
- Metric: RMSE ("The error metric for this competition is the Root Mean Squared Error", Evaluation tab); a competition's leaderboard metric (MET-4); inputs none (the group `Place_ID` is a split column, not a feature).
- Risks for /add-dataset: drop the target-related columns of Train.csv ("columns for minimum and maximum readings on that day, the variance of the readings and the total number (count) of sensor readings", LEAK); only Train.csv is labelled, so the split is by `Place_ID` inside it; the Sentinel-5P columns are satellite retrievals: SEL-13 names remote-sensing spectra as image-derived, these are retrieved gas columns used as measurements (SEL-15), a call for the curator as on airqo; the "metadata like the satellite altitude" columns and the many missing retrievals (CH4); three months during the 2020 lockdowns.
- Priority: gap + (grouped regime thin), use case 0 (no actor named), source 0 (a weekend hackathon page, products documented on GEE), shape + (about 30,000 rows over 349 places, many numeric columns, grouped), risk - (the modality question and three sibling tasks).

A Zindi challenge to predict air quality (PM2.5) in cities worldwide using engineered features derived from Sentinel-5P satellite data plus weather, provided as a tabular feature table. While the underlying source is satellite imagery, the competition exposes aggregated tabular features, so it could be a valid regression task; however it has a strong temporal/forecasting character (predicting daily pollution levels). A human must verify whether the released data is genuinely tabular features (not raw imagery), the exact target and temporal-split protocol, and dataset size, so a provisional 2nd-tier hold is appropriate.

---

predict air quality in cities around the world using satellite data
