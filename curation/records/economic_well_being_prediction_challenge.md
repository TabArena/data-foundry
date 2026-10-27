---
unique_name: economic_well_being_prediction_challenge
name: economic-well-being-prediction-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2021'
domain: social science
required_split:
- Grouped (NON-IID)
problem_type: Regression
source_links:
- https://zindi.africa/competitions/economic-well-being-prediction-challenge/data
source_row: 909
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 3: survey-cluster wealth index predicted from Africa-wide geospatial layers for countries not in training; a known poverty-mapping task with a grouped (country) split; the inputs are remote-sensing products, the one scope question.
- Source: first published as the Zindi "AIMS Data Science Hackathon" (Microsoft, for AIMS and CMU Africa students, 25 Jan 2021), re-opened publicly as "Economic Well-Being Prediction Challenge" (16 Apr - 15 Aug 2021, https://zindi.africa/competitions/economic-well-being-prediction-challenge); same text and the same Train.csv (5,829,604 bytes), Test.csv and SampleSubmission.csv. As published: one row per survey cluster; target "a derived 'wealth index' based on responses in various household surveys ... on a scale from 0 to 1"; features: GHSL built-up fractions by epoch, water surface, population density (5 km radius), Copernicus land-cover fractions (crops, urban, permanent and seasonal water), nighttime lights, distance to capital and to shoreline, urban or rural. Rows not counted (login); the survey programme is not named (likely DHS).
- Use case: "Granular information on economic well-being is extremely useful for governments, policy makers, and NGOs ... A successful model could be useful for filling in the gaps between the more expensive surveys" (Description): an agency estimates wealth where no recent survey exists; fit direct; regime grouped because "you must correctly predict the cluster-level estimated wealth measures found from surveys in 7 different countries not covered in the training data" (only Train.csv has labels: group by country within it).
- Siblings and duplicates: no other record of the AIMS hackathon or of DHS wealth mapping found (`grep` for wealth, poverty, well-being, aims); the old `Missing source information` marker is refuted (the competition documents every layer). External collections: none found.
- Papers and pages: the competition tabs (read through Zindi's API); the task follows the satellite poverty-mapping literature (Jean et al. 2016, Yeh et al. 2020), not checked as a source of these rows.
- Metric: RMSE ("The evaluation metric for this competition is Root Mean Squared Error", Evaluation tab); MET-4; inputs: a country column for the grouped split (to check that it ships; the API listed the AIMS parent's metric as MAE while its page says RMSE).
- Risks for /add-dataset: SEL-13 (land-cover fractions and night lights are classified satellite products aggregated to 5 km, a layer of abstraction above spectra; argue it from the columns); whether Train.csv carries country and survey year; clusters near each other across surveys (spatial leakage within a country).
- Priority: gap + (social science and the grouped regime are thin), use case + (the source names the actors and the gap-filling decision), source 0 (the competition documents the layers, not the surveys), shape + (thousands of clusters in 18 countries, grouped), risk - (SEL-13 question).


Zindi 'Economic Well-Being Prediction Challenge'; the record has no body, but the title strongly implies predicting a household/regional wealth or well-being index, typically a regression task over survey and/or geospatial covariates. This is a plausible real-world tabular task in the social-science domain. There is a risk the features are derived from satellite imagery (which would lean non-tabular) or require a grouped/spatial split. A human must check the feature set (tabular vs. imagery-derived), the exact continuous target, sample size, and whether a grouped/spatial split is needed.
