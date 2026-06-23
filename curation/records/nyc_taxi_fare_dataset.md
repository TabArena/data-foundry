---
unique_name: nyc_taxi_fare_dataset
name: NYC Taxi Fare Dataset
tags:
- 2nd Tier / Scientfic Discovery
- Non-IID (Temporal)
- Non-IID (Grouped)
collections:
- New (BeyondArena)
source_links:
- https://www.kaggle.com/datasets/diishasiing/revenue-for-cab-drivers
source_row: 852
needs_review:
- suggestion
type_adapter_id: curation-record-v1
---

# NYC Taxi Fare Dataset

## Comments

CC: ""Temporal preprocessing needed, geospatial leakage, grouped data;

Need to preprocess dates, need to resolve location ID, need to remove features that leak the target if we predict price or if we predict time; almost no predictive signal in original features""
