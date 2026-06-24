---
unique_name: nyc_taxi_fare_dataset
name: NYC Taxi Fare Dataset
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Data Quality Issue
- Not Representative
tags:
- 2nd Tier / Scientfic Discovery
- Non-IID (Temporal)
- Non-IID (Grouped)
- AI-Filled (Verify)
collections:
- New (BeyondArena)
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/diishasiing/revenue-for-cab-drivers
source_row: 852
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

A Kaggle taxi-revenue table where the curator notes geospatial leakage, grouped/temporal structure, and crucially 'almost no predictive signal in original features' once leaking features are removed. Predicting fare or trip time requires heavy temporal preprocessing and location-ID resolution, after which little signal remains. This combination of leakage and lack of representativeness makes it a poor benchmark task. Suggest No; a human could confirm whether any non-leaking predictive task survives, but the curator's note strongly indicates not.

---

CC: ""Temporal preprocessing needed, geospatial leakage, grouped data;

Need to preprocess dates, need to resolve location ID, need to remove features that leak the target if we predict price or if we predict time; almost no predictive signal in original features""
