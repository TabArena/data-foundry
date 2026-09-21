---
unique_name: nyc_taxi_trip_duration
name: NYC Taxi Trip Duration
checked_by:
- Lennart
suggestion: 'Yes'
tags:
- Review Prio 1 (Atlas)
collections:
- New (BeyondArena)
original_source: GOV Website
year: '2016'
domain: Other
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/c/nyc-taxi-trip-duration
- https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
- https://data.cityofnewyork.us/Transportation/2016-Yellow-Taxi-Trip-Data/uacg-pexx
- https://www.kaggle.com/code/jeffreycbw/nyc-taxi-trip-public-0-37399-private-0-37206
- https://www.kaggle.com/datasets/wol4aravio/ny-taxi-trip-duration-enriched-by-mathematica
- https://www.openml.org/d/42729
- https://www.kaggle.com/datasets/diishasiing/revenue-for-cab-drivers
- https://www.kaggle.com/c/pkdd-15-taxi-trip-time-prediction-ii
type_adapter_id: curation-record-v1
---

## Comments

NYC Taxi Trip Duration (Kaggle, 2017 playground competition; NYC TLC 2016 data). ~1.46M training rows; target is trip duration in seconds (the competition scores RMSLE, i.e. effectively a log-scaled regression). Features include pickup/dropoff timestamps and coordinates and passenger count, so a temporal split on pickup_datetime is the natural protocol; also has spatial structure. Real-world data with a well-defined regression task in the target row range — a reasonable Atlas candidate, though confirm that 'trip duration' is a meaningful predictive task vs. a contrived competition target. No existing curation record was found, so this record was created by the AI.

CC (2026-09-21, Lennart): **Kept as the one NYC-TLC dataset.** Provenance: Kaggle 2017
playground built from the 2016 NYC yellow-cab TLC trip records (via the BigQuery public dataset), "sampled
and cleaned"; 1,458,644 train rows; dropoff coordinates were deliberately left in. `nyc_taxi_green_dec_2016`
(OpenML 42729: green cabs, Dec 2016, target `tip_amount`) and `nyc_taxi_fare_dataset` (anonymous Kaggle
re-upload) are other cuts of the same TLC data → `Duplicate`, No. `pkdd_15_taxi_trip_time_prediction_ii`
(Porto, ECML/PKDD 2015) is a separate source with the same task type and stays open as its own candidate.

The primary source can be used directly: the TLC page serves monthly Parquet files 2009–2026 (pickup/dropoff
datetime, trip distance, itemized fares, payment type, passenger count); pickup/dropoff *coordinates* exist
only up to mid-2016, zone IDs afterwards. No explicit license on the TLC page; NYC Open Data terms: data
"provided for informational purposes", no warranty. Preprocessing idea using the latest source:
https://www.kaggle.com/code/jeffreycbw/nyc-taxi-trip-public-0-37399-private-0-37206 (public 0.37399 /
private 0.37206 on the competition).

Task: ETA-at-pickup regression (destination known), temporal split on `pickup_datetime`, log-scale the target
(competition metric was RMSLE). The competition's own test split is a same-period sample (unverified), so its
leaderboard says nothing about difficulty under a temporal split. Related shipped ETA tasks: `delivery_eta`,
`maps_router_eta` (TabRed). Kaggle discussion / notebook sweep still to do beyond the notebook above.
