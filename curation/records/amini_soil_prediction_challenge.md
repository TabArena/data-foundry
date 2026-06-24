---
unique_name: amini_soil_prediction_challenge
name: amini-soil-prediction-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: environmental science & climate
required_split:
- '?'
problem_type: Regression
original_data_state: Other
source_links:
- https://zindi.africa/competitions/amini-soil-prediction-challenge/data
source_row: 882
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Zindi Amini soil-prediction challenge: predict availability of 11 essential soil nutrients and nutrient gaps for maize yield, i.e. a multi-target regression problem. This is a genuine real-world tabular(ish) regression task in agronomy/environmental science, already flagged as needing extensive data wrangling. The main risks are (a) inputs may be soil spectral/sensor data closer to a non-tabular modality, and (b) multi-output handling. A human must verify the input features are tabular, choose a single representative target (or confirm multi-output is acceptable), and confirm adequate cleaned size.

---

predicts the availability of 11 essential soil nutrients and calculates the nutrient gaps required for maize crops to achieve a target yield of 4 tons per hectare
