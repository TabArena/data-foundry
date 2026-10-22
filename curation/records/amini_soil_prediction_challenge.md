---
unique_name: amini_soil_prediction_challenge
name: amini-soil-prediction-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Multi-target
collections:
- New (BeyondArena)
original_source: Zindi
year: '2025'
domain: environmental science & climate
required_split:
- '?'
problem_type: Regression
original_data_state: Other
source_links:
- https://zindi.africa/competitions/amini-soil-prediction-challenge/data
- https://zindi.africa/competitions/amini-soil-prediction-challenge
- https://www.zindi.africa/blog/first-place-solution-amini-soil-prediction-a-hundred-heads-are-better-than-one
source_row: 882
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 2: predict 11 soil nutrients from environmental features for fertilizer recommendations to farmers; the soil samples' origin is unclear and the release is many tables.
- Source: Zindi competition by Amini (amini.ai, a data company), 2025-04-02 to 2025-06-23 ($7,000, 1,076 participants); as published: Train.csv/Test.csv with "measured soil chemical properties (in ppm)", "environmental and spatial features" and bulk density from "a set of soil from 2019 ... collected from farms across Africa" at 20 cm depth; Gap_Train.csv/Gap_Test.csv; satellite tables to join by field (LANDSAT8, MODIS MOD09GA/MOD11A1/MOD13Q1/MOD16A2/MCD43A4, Sentinel-1, Sentinel-2); row counts not stated.
- Use case: Amini gives farmers "precise recommendations, helping them optimize fertilizer use" from scalable soil estimates instead of a lab test per field; fit direct for the nutrient levels; regime IID or grouped by site/region (spatial; to check).
- Siblings and duplicates: `africa_soil_property_prediction_challenge` (AfSIS Kaggle, TBD -> 2nd Tier), `africa_soil_profiles_database`, `wosis_soil_profiles`, `lucas_topsoil`, `open_soil_data`; the 2019 African farm samples may come from AfSIS or iSDA (not stated): a possible duplicate to trace (PROV-4). External collections: none found.
- Papers and pages: <https://zindi.africa/competitions/amini-soil-prediction-challenge>; first-place write-up on the Zindi blog (an ensemble of many models).
- Metric: RMSE on the nutrient gap in kg/ha (Zindi evaluation page: "The evaluation metric for this competition is Root Mean Squared Error"), where the gap is a published deterministic formula of the predicted ppm: "Available (kg/ha) = ppm x soil depth (cm) x bulk density (g/cm³) x 0.1", "Gap (kg/ha) = Required - Available"; deliberate (leaderboard, MET-4); inputs bulk density and the per-nutrient requirement, which ship. The gap is a known transform of the nutrient (SEL-5: the task is the nutrient level; the formula belongs to the metric).
- Risks for /add-dataset: 11 targets (`Multi-target`; pick one or ship several, CLEAN-18); the satellite tables are remote-sensing spectra (SEL-13 leans them out; the soil and environmental columns may suffice); joins by PID; provenance of the soil samples (PROV-1, PROV-4); a spatial grouping to decide.
- Priority: gap - (environmental, regression, IID not thin), use case + (Amini names it), source - (a company page; the samples' origin is not stated), shape + (many features, likely thousands of fields), risk - (joins, multi-target, possible duplicate).

Zindi Amini soil-prediction challenge: predict availability of 11 essential soil nutrients and nutrient gaps for maize yield, i.e. a multi-target regression problem. This is a genuine real-world tabular(ish) regression task in agronomy/environmental science, already flagged as needing extensive data wrangling. The main risks are (a) inputs may be soil spectral/sensor data closer to a non-tabular modality, and (b) multi-output handling. A human must verify the input features are tabular, choose a single representative target (or confirm multi-output is acceptable), and confirm adequate cleaned size.

---

predicts the availability of 11 essential soil nutrients and calculates the nutrient gaps required for maize crops to achieve a target yield of 4 tons per hectare
