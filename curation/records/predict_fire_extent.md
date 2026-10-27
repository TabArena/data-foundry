---
unique_name: predict_fire_extent
name: predict-fire-extent
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://zindi.africa/competitions/predict-fire-extent/data
source_row: 884
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Duplicate`, PROV-4): Zindi's competition `predict-fire-extent` (shown as "Wildfire Prediction Challenge", 2024-07-16 to 2024-08-14) is a re-run of the Zimbabwe burned-area data first used in the Zindi "Fighting Fire with Data Hackathon" (2020-06-27).
- Source: the Zindi API lists the same files for `fighting-fire-with-data-hackathon` (2020), `cmu-africa-fighting-fire-with-data` (2020), `data-science-zw-2022-fire-prediction` (2022), `predict-fire-extent` (2024) and `wildfire-prediction-challenge` (2024): Train.csv 19,531,802 bytes, Test.csv 5,802,277, SampleSubmission.csv 429,661, variable_definitions.csv 2,344, and a starter notebook named "Fighting_Fire_with_Data_Starter_Notebook.ipynb"; as published: monthly burned-area fraction per area square across Zimbabwe since 2001 with TerraClimate, MODIS land cover, population and elevation covariates; train to 2013, test 2014-2016.
- Siblings and duplicates: `data_science_zw_2022_fire_prediction` (TBD -> 2nd Tier, its `source_links` carry the 2020 fighting-fire hackathons, so it holds the first publication) and `wildfire_prediction_challenge` (`No`, `Time-series (Forecasting)`), both the same files. Whichever record the curator keeps as canonical, this one adds no distinct task.
- Metric: Root Mean Squared Error on the burned fraction (the Evaluation page).
- Note for the canonical record: the task predicts "the burned area in different locations over 2014 to 2016" from the series to 2013 with covariates "that extends into the test period", a forecasting-like panel (SEL-10 / SEL-11, TP-10).
- Reject check (AI, 2026-10-22): stands. I checked the Zindi API myself. predict-fire-extent and fighting-fire-with-data-hackathon (https://zindi.africa/competitions/fighting-fire-with-data-hackathon, 2020-06-27) have identical sizes: Train.csv 19531802, Test.csv 5802277, SampleSubmission.csv 429661, variable_definitions.csv 2344. The 2024 Description repeats the 2020 task (predict burned area 2014-2016 from data to 2013), so PROV-4 applies. data_science_zw_2022_fire_prediction already carries the 2020 links and stays the canonical record.

A Zindi competition to predict the burned area of wildfires in Zimbabwe, i.e. a regression target. Such challenges often supply geospatial/satellite-derived features which may be raster imagery (out of scope) or pre-extracted tabular covariates per location-time. There is also a risk this is a forecasting task over time. Suggest TBD -> 2nd Tier; a human must verify whether inputs are tabular features versus imagery, whether the task is a fixed predictive (temporal-split) regression rather than forecasting, and the dataset size.

---

predict the burned area of wildfires in Zimbabwe
