---
unique_name: pkdd_15_taxi_trip_time_prediction_ii
name: 'ECML/PKDD 15: Taxi Trip Time Prediction (II)'
checked_by:
- Lennart
suggestion: 'Yes'
decision_markers:
- Needs extensive data wrangling
tags:
- Review Prio 1 (Atlas)
original_source: Kaggle
year: '2015'
domain: Other
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/c/pkdd-15-taxi-trip-time-prediction-ii
- https://www.kaggle.com/c/pkdd-15-predict-taxi-service-trajectory-i
- https://archive.ics.uci.edu/dataset/339/taxi+service+trajectory+prediction+challenge+ecml+pkdd+2015
- https://arxiv.org/abs/1508.00021
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-21, Lennart): **Open candidate, not a duplicate: a different source from the NYC TLC data
(`nyc_taxi_trip_duration`); we may take several taxi trip-time datasets.** Porto, Portugal: all trips of 442
taxis, 2013-07-01 to 2014-06-30, ~1.7M trips, a GPS point every 15 s (`POLYLINE`) plus call type, origin call /
stand, taxi id, timestamp and day type. Data is CC BY 4.0 on UCI (id 339).

**To check during curation:** the competition's Task II is total travel time given a *partial* trajectory; de
Brébisson et al. 2015 (arXiv:1508.00021): "The testing dataset is composed of 320 partial trajectories, which
were created from five snapshots taken at different timestamps." The public baseline
`max((len(POLYLINE)-1)*15, 660)` scores well because the elapsed prefix time lower-bounds the target, not
because test data leaked — the competition signal sits in the GPS sequence (hence the provisional
`Wrong Domain / Source Modality` marker). A tabular framing would predict full trip time at pickup from start
point, time, call type, stand and taxi id, with no destination feature; whether that carries enough signal
decides the verdict. Grouped structure by `TAXI_ID` (442 drivers) besides the temporal one.

**Investigation (2026-09-21, agent; data inspected from the UCI zip):** 1,710,670 rows (81 `TRIP_ID`s
duplicated, 3 rows fully identical); 2013-07-01 → 2014-06-30, 126k–162k trips per month; 448 taxis.
`DAY_TYPE` is constant "A" (drop). `MISSING_DATA` is True for only 10 rows although 5,901 polylines are empty
and 30,609 have a single point (0 s): the flag is unreliable (Lam et al. 2015, arXiv:1509.05257, note the
same). Duration = (points − 1) · 15 s: median 600 s, 95th pct 1,530 s, 10,094 trips > 1 h and 135 > 6 h
(meter left running); 1,459 trips start outside Porto (GPS errors). `ORIGIN_CALL` (57k phone IDs) exists only
for call type A, `ORIGIN_STAND` (63 stands) for B, with 11k B-trips lacking a stand. After dropping < 2 points,
> 3 h, out-of-bbox starts and duplicates: 1,672,071 rows.

Test set: 320 prefixes cut at five timestamps *after* the training year (2014-08-14 18:00, 09-30 08:30,
10-06 17:45, 11-01 04:00, 12-21 14:30). The elapsed prefix explains most of the target (corr 0.84);
`max(elapsed, 660)` scores RMSLE 0.636 vs 0.794 for a constant, and 0.3% of targets lie below the elapsed
time.

Tabular signal (LightGBM, log target, train ≤ 2014-04, test 2014-05/06): pickup-time features only (start
coordinates, time, call type, stand, taxi id) reach RMSLE 0.622 / R² 0.14 vs 0.670 for a constant — weak.
Adding the drop-off point (the ETA framing of `nyc_taxi_trip_duration`) gives RMSLE 0.472 / R² 0.50, MAE
210 s. `TAXI_ID` is the top feature in both (driver habits). So the viable framing is ETA from origin +
destination + time with a temporal split and grouped structure by taxi; a pickup-only framing has too little
signal. Kaggle discussion / notebook sweep not done (pages unreadable for the agent).

CC (2026-09-21, Lennart): **Verdict so far: gut feeling Yes, but heavy processing is needed to make it a
good benchmark dataset (`Needs extensive data wrangling`).** The data itself is real and nice: a full year of
every trip of a city's taxi fleet, with dispatch metadata, under CC BY 4.0. Do not ship the competition's
task definition (remaining time from a partial trajectory); use the real one: ETA at pickup from origin,
destination, time, call type, stand and taxi, temporal split, taxi as group. That framing carries clear signal
(R² 0.50 in log space above), the pickup-only one does not. Processing to do: parse the polylines into
endpoints and duration, drop empty / single-point trips, meter-left-on outliers, out-of-city starts and
duplicate IDs, drop the constant `DAY_TYPE`, ignore the unreliable `MISSING_DATA`, and decide how to treat
the 57k `ORIGIN_CALL` IDs. Work on it a bit more before the final call.
