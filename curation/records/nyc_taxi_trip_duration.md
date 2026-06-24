---
unique_name: nyc_taxi_trip_duration
name: NYC Taxi Trip Duration
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
tags:
- Review Prio 1 (Atlas)
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Kaggle
year: '2016'
domain: Other
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/c/nyc-taxi-trip-duration
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

NYC Taxi Trip Duration (Kaggle, 2017 playground competition; NYC TLC 2016 data). ~1.46M training rows; target is trip duration in seconds (the competition scores RMSLE, i.e. effectively a log-scaled regression). Features include pickup/dropoff timestamps and coordinates and passenger count, so a temporal split on pickup_datetime is the natural protocol; also has spatial structure. Real-world data with a well-defined regression task in the target row range — a reasonable Atlas candidate, though confirm that 'trip duration' is a meaningful predictive task vs. a contrived competition target. No existing curation record was found, so this record was created by the AI.
