---
unique_name: nyc_taxi_trip_duration
name: NYC Taxi Trip Duration
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
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
v2_path: datasets/_dev/tabarena-v0pt2/nyc_taxi_trip_duration_1m/dataset.py
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

**Assessment (AI, 2026-10-07):** Valid; added as `nyc_taxi_trip_duration` (ETA at pickup, 3 weekly test windows in
June 2016). The competition's test.csv is a random 30% of every day of the same half-year (28.8-31.2% per day), so its
leaderboard measured interpolation. 8 of 8 sampled training rows match NYC Open Data uacg-pexx; the TLC's current
Parquet files hold zone IDs only (2012-2016 checked). Sweep: test labels leaked through the public TLC records; about
0.15% clock-error trips (22-24 h, VeriFone meters) dominated the RMSLE. Dropped: trips under 30 s or over 3 h (0.47%)
and store_and_fwd_flag; 86 trips across the daylight-saving switch lose the skipped hour. `original_source` could
read Kaggle: the sample first appeared there (as sdss_17).

Related work, not a source: the PKDD-15 Porto taxi trip-time competition (https://www.kaggle.com/c/pkdd-15-taxi-trip-time-prediction-ii), which has its own record (pkdd_15_taxi_trip_time_prediction_ii).

**Assessment (AI, 2026-10-20):** priority 3 for the review of the added dataset: gap -, use case -, source +, shape +, no known risk. A large, well-sourced temporal ETA regression; which source copy to ship and the row filters that select on the target are still open.

**Assessment (AI, 2026-10-20):** Review panel (full tier): ship after changes, applied in the definition (a rebuild is due). The 2026-09-21 CC's statement that the TLC Parquet files hold coordinates up to mid-2016 does not hold: the 2016 files hold zone IDs only (yellow_tripdata_2016-06 read); NYC Open Data uacg-pexx serves the coordinates, and 13 of 13 sampled training rows match it. The definition drops the 4,539 trips whose drop-off coordinates equal the pickup coordinates (USE-7: no destination; mean target 6.04 against 6.47), sets passenger_count 0, 8 and 9 to missing (CLEAN-10/11), adds a one-day gap before each weekly window (SPLIT-9: 77/119/127 train trips per window ended after the window start) and rates the fit approximate (USE-8: the drop-off point stands in for the named destination, as in pkdd_15). LightGBM RMSE 0.373/0.357/0.381 on the weekly windows with the hour kept, 0.429/0.414/0.441 with AutoGluon's date parts; a random hold-out of the same size is optimistic by 0.013-0.029, mostly from distance in time. Open: the row budget (rename to _1m or amend the house rule) and the datetime encoding of v0.2 (cross-dataset). Priority 3: gap - (no thin domain, problem type or regime), use case - (fit approximate, use case written by the curation), source + (TLC records, rows verified), shape + (1.45M trips, categorical and datetime, temporal), risk 0 (the open issue is a house rule, no leak or unclear target).

CC (2026-10-21, Lennart): Cite the original publisher, the NYC Taxi and Limousine Commission trip records, as house_sales does (PROV-10).

**Assessment (AI, 2026-10-21):** bibtex now cites the TLC Trip Record Data first, next to the Kaggle competition that published the sample. Dataset check: 0 errors, 0 warnings.

CC (2026-10-21, Lennart): ok on creating the _1m version (`nyc_taxi_trip_duration_1m`): every train side is over the 1M-row budget.

**Assessment (AI, 2026-10-21):** the folder is renamed to `nyc_taxi_trip_duration_1m` (`version_of = "nyc_taxi_trip_duration"`, `subsample_to_budget = True`, as delivery_eta_1m; the full version is not kept in the working copy, as for the other `_1m` datasets). Same three weekly test windows (52,779 / 52,949 / 54,532 trips, newest first) and one-day gap; each train side is a random 1M of the 1.28M-1.39M earlier trips, drawn in one order so the sides overlap; the frame keeps the 1,166,477 trips a split uses (of 1,447,167 after cleaning), so the accepted `splits_rows_unused` warning is gone. Dataset check: 0 errors, 0 warnings. Not built.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source rmse — the competition's RMSLE, as RMSE on the shipped log1p_trip_duration (Kaggle evaluation page).
