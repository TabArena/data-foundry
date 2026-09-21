---
unique_name: nyc_taxi_fare_dataset
name: NYC Taxi Fare Dataset
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Data Quality Issue
- Not Representative
- Duplicate
tags:
- 2nd Tier / Scientfic Discovery
- Non-IID (Temporal)
- Non-IID (Grouped)
collections:
- New (BeyondArena)
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/diishasiing/revenue-for-cab-drivers
- https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
source_row: 852
type_adapter_id: curation-record-v1
---

## Comments

A Kaggle taxi-revenue table where the curator notes geospatial leakage, grouped/temporal structure, and crucially 'almost no predictive signal in original features' once leaking features are removed. Predicting fare or trip time requires heavy temporal preprocessing and location-ID resolution, after which little signal remains. This combination of leakage and lack of representativeness makes it a poor benchmark task. Suggest No; a human could confirm whether any non-leaking predictive task survives, but the curator's note strongly indicates not.

---

CC: ""Temporal preprocessing needed, geospatial leakage, grouped data;

Need to preprocess dates, need to resolve location ID, need to remove features that leak the target if we predict price or if we predict time; almost no predictive signal in original features""

CC (2026-09-21, Lennart): **Version case of the NYC TLC trip records → `Duplicate`.** The zone-ID columns the
earlier note mentions are the post-2016 TLC schema, so this is a re-upload of TLC yellow-cab data with
fare/revenue as target; the Kaggle page sits behind a bot check and was not re-inspected. We keep
`nyc_taxi_trip_duration`.
