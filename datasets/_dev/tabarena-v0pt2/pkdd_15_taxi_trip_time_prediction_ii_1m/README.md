---
report_format: data-foundry-report-v2
unique_name: pkdd_15_taxi_trip_time_prediction_ii_1m
container_format: 2
checksum: v2:bb35c17a02f96d5c8cf27db6b561de58426c91e15bf9f30527506e4d1065d0bf
build:
  uuid: 01a217fc-2c03-74d9-baff-ea7cc624d41c
  checksum: v2:bb35c17a02f96d5c8cf27db6b561de58426c91e15bf9f30527506e4d1065d0bf
  built_at: '2026-11-26T13:12:28+00:00'
  path: pkdd_15_taxi_trip_time_prediction_ii_1m/01a217fc-2c03-74d9-baff-ea7cc624d41c
  data_foundry_version: 0.0.5
  git_sha: e3ddd55462cc45eed6aa71c38abd183086888b36
  libraries:
    python: 3.12.3
    pandas: 2.3.3
    numpy: 2.1.3
    pyarrow: 20.0.0
    scikit-learn: 1.7.2
    polars: 1.41.1
build_stale: false
data:
  n_rows: 1630753
  n_features: 8
  dtypes:
    category: 3
    datetime64[ns]: 1
    float64: 5
  n_test_dataset_rows: null
task:
  target: log1p_travel_time
  problem_type: regression
  metric: rmsle
  metric_origin: source
  scoring_columns: null
  split_regime: temporal_non_iid
  stratify_on: null
  time_on: start_time
  group_on: null
  group_labels: null
  group_time_on: null
  grouping: null
splits:
  n_repeats: 3
  n_folds: 1
  random_state: 4267
  time_horizon: 1
  time_horizon_unit: months
  time_gap: 1
  time_gap_unit: days
  reason: 'A model trained on the trips so far predicts the travel times of the next
    calendar month''s trips: 3 test windows, the calendar months June, April and February
    2014 (newest first), and train is the trips that start at least one day before
    the window. The length (the horizon checked, CC 2026-11-11): no source gives a
    refit cadence. The challenge scored five snapshots of trips under way (320 trips,
    14 August to 21 December 2014; Lam et al. 2015, arXiv:1509.05257) with one model
    trained on its year (1 July 2013 to 30 June 2014), used 1.5 to 6 months later
    without a refit, so the only horizon the source shows is months long; calendar
    months are the longest windows that still leave a choice of seasons (60 days would
    give exactly three windows that tile the half-year). nyc_taxi_trip_duration_1m
    predicts the same kind of travel time on one-week windows, a length that rests
    on its weekdays and an ETA service''s refit; its source shows no horizon either.
    The windows (CC 2026-11-10 and 2026-11-11, the curator''s pick): June, the newest,
    with São João (23-24 June); April, with Easter (18-20 April); and February, in
    the winter, when Porto''s trips are the slowest of the year (median straight-line
    speed 15.6 to 16.0 km/h from October to February, 16.7 to 17.6 from May to August).
    The file covers one year (July 2013 to June 2014), so no other year can be tested,
    and months from January 2014 keep half the trips for training; the three are spread
    evenly over the six months open. The gap of one day is part of the task: a trip
    lasts up to 3 hours, so at a refit the last trips before it have no travel time
    yet; without the gap 47, 7 and 21 train trips (June, April, February) would end
    after the window start, with it none. The 5,523 trips of 31 May 2014, the newest
    window''s gap day, lie in no split, so the frame leaves them out. The February
    window''s train side holds the winter months before it, while April and June have
    no earlier copy of their month in train.'
  n_train:
    min: 943912
    max: 1484039
  n_test:
    min: 122831
    max: 146714
  row_budget:
    train: 1000000
    test: 500000
  train_sampling:
    default: newest_year
    unit: rows
    stratify_on: null
bundle_checks:
  ok: true
  errors: []
  warnings: []
  infos: []
  accepted: {}
decisions:
- Rows dropped before the split
- Temporal split; the taxi stays a feature, not a group
- Start time in Porto local time
---

# pkdd_15_taxi_trip_time_prediction_ii_1m

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Regression of `log1p_travel_time`, scored with `rmsle` on temporal splits by `start_time`. 1,630,753 rows and 8 features. Source: Kaggle (2015).

Built as `01a217fc-2c03-74d9-baff-ea7cc624d41c` on 2026-11-26. See [Build](#build).

## In brief

**Question.** How long will a Porto taxi trip take, from its start to its destination?

**Use case.** For example, when a passenger books a ride in an app and names the destination, the taxi company estimates the trip's duration from the start, the destination and the time, to quote it and plan when the taxi will be free again.

**One row.** One trip of a Porto taxi fleet, July 2013 to June 2014 (ECML/PKDD 2015 challenge).

**Predicted.** The travel time in seconds, from the trip's GPS points (one every 15 seconds), on a log scale.

**Known at prediction time.** The local start time, the start point and the last GPS point as the destination, how the taxi was hired (dispatch call, taxi stand or street), the stand, and the taxi.

**What the test data stands for.** June, April and February 2014 are the test periods (calendar months); training is every trip that starts at least one day earlier, of which a benchmark fits on a random million, as for a model trained on the trips so far and used for the next month.

**Our changes to the source.** The challenge asked for the remaining time of a trip under way; we predict the whole trip at pickup with its end point, and drop non-trips, trips that end within 100 m of where they start, GPS jumps, meters left running and the caller's phone number.

> **Use case fit: approximate (a stand-in with a known gap).** Everything the model sees is known at pickup except the destination: the realised drop-off (the last GPS point) stands in for a destination named at pickup, which the source's dispatch system did not record. The task is framed without a routing estimate.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision, its sources and the review: [`curation/records/pkdd_15_taxi_trip_time_prediction_ii.md`](../../../../curation/records/pkdd_15_taxi_trip_time_prediction_ii.md)
- The original source: <https://www.kaggle.com/c/pkdd-15-taxi-trip-time-prediction-ii>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/pkdd_15_taxi_trip_time_prediction_ii/`. To get them:

```text
The training set of the ECML/PKDD 2015 Discovery Challenge, which its organisers donated to the UCI repository
(id 339, CC BY 4.0, https://doi.org/10.24432/C55W25). The Kaggle download needs the competition's rules
accepted (403 on our account). The UCI zip holds train.csv.zip of 533,605,607 bytes, the size to the byte of
the train.csv.zip that `kaggle competitions files` lists for both PKDD 2015 competitions; its train.csv holds
the 1,710,670 trips of the challenge. We keep train.csv only (sha256
2891d03ea99ce0fc203daedd434848a1a8baa7a8fb6da10f8d7ff26559efff6d, downloaded 2026-10-06); `_prepare_raw_files`
writes trips.parquet next to it.

mkdir -p local-data-warehouse/pkdd_15_taxi_trip_time_prediction_ii && cd local-data-warehouse/pkdd_15_taxi_trip_time_prediction_ii
wget -O taxi_service_trajectory.zip "https://archive.ics.uci.edu/static/public/339/taxi+service+trajectory+prediction+challenge+ecml+pkdd+2015.zip"
unzip taxi_service_trajectory.zip train.csv.zip && unzip train.csv.zip && rm taxi_service_trajectory.zip train.csv.zip
```

On first use, `_prepare_raw_files` writes `trips.parquet` into the same folder.

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/pkdd_15_taxi_trip_time_prediction_ii_1m   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/pkdd_15_taxi_trip_time_prediction_ii_1m   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | Kaggle: https://www.kaggle.com/c/pkdd-15-taxi-trip-time-prediction-ii |
| year | 2015 |
| domain | industry & manufacturing |
| license | CC BY 4.0 |
| data_tags | Non-IID, Temporal, Spatial |
| reference | moreiramatias2013taxi |
| rows x columns | 1,630,753 x 9 |
| task.target | log1p_travel_time |
| task.problem_type | regression |
| task.metric | rmsle |
| task.split_regime | temporal_non_iid |
| task.time_on | start_time |

**Metric**

| field | value |
|---|---|
| name | `rmsle` (standard; takes value; lower is better) |
| origin | source: the source's metric |
| original | Root Mean Squared Logarithmic Error (RMSLE) |
| reference | https://www.kaggle.com/competitions/pkdd-15-taxi-trip-time-prediction-ii/overview/evaluation |
| definition | sqrt(mean((log(p+1)-log(a+1))^2)) of travel time in seconds, computed after the inverse of the shipped log1p_travel_time target. |
| target scale | ships on the `log1p` scale for modelling; scored on the original scale after the inverse of `log1p` |

<details>
<summary>Feature types: 3 categorical, 0 string, 1 datetime</summary>

- categorical (3): `call_type`, `origin_stand`, `taxi_id`
- string (0): none
- datetime (1): `start_time`

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@misc{moreiramatias2013taxi,
  author       = {Moreira-Matias, Luis and Ferreira, Michel and Mendes-Moreira, Jo{\~a}o and others},
  title        = {{Taxi Service Trajectory - Prediction Challenge, ECML PKDD 2015}},
  year         = {2013},
  howpublished = {UCI Machine Learning Repository},
  doi          = {10.24432/C55W25},
  note         = {Training set of the ECML/PKDD 2015 Discovery Challenge (Kaggle: pkdd-15-taxi-trip-time-prediction-ii)}
}
```

</details>

## Sample rows

The first 5 of 1,630,753 rows of the final frame (the oldest rows: the frame is sorted by `start_time`). Cells are cut at 40 characters.

| log1p_travel_time | call_type | origin_stand | taxi_id | start_time | start_lon | start_lat | end_lon | end_lat |
|---|---|---|---|---|---|---|---|---|
| 5.88888 | street | nan | 20000380 | 2013-07-01 01:00:53 | -8.61029 | 41.1407 | -8.60589 | 41.1453 |
| 6.44731 | street | nan | 20000520 | 2013-07-01 01:00:54 | -8.57468 | 41.152 | -8.608 | 41.1429 |
| 5.80212 | street | nan | 20000589 | 2013-07-01 01:00:58 | -8.61864 | 41.1414 | -8.63084 | 41.1545 |
| 5.75574 | street | nan | 20000233 | 2013-07-01 01:01:15 | -8.61989 | 41.148 | -8.60949 | 41.1574 |
| 6.44731 | street | nan | 20000360 | 2013-07-01 01:01:36 | -8.6176 | 41.1461 | -8.63663 | 41.1691 |

## Curation notes

We start with train.csv of the ECML/PKDD 2015 Discovery Challenge (UCI id 339): 1,710,670 Porto taxi trips from 2013-07-01 to 2014-06-30, each with its GPS trajectory (`POLYLINE`, one point every 15 s).

- Prediction point: the start of the trip, when the meter is switched on. The task is the travel time from origin and destination, an ETA task like `nyc_taxi_trip_duration` (the challenge's Task II starts from a partial trajectory).
- Anomaly: the challenge page says that drivers "do not indicate the final destination of the ride" to the dispatch system. Our destination is the last GPS point, a stand-in for a destination named at pickup (`fit="approximate"`, as `nyc_taxi_trip_duration`), the curator's framing (record, CC 2026-09-21; confirmed CC 2026-10-26: an ETA once the passenger names the destination, as in an app booking). Without it, LightGBM's R^2 is 0.12 to 0.15 (800 trees, learning rate 0.08, 255 leaves, local hour, weekday and day of year, one fit per split, on the April, May and June windows shipped until 2026-11-11, as are the other R^2 figures of these notes).
- Target: `log1p_travel_time`, log1p of the travel time in seconds, (GPS points - 1) x 15, the challenge's definition; the metric is the challenge's RMSLE on the travel time in seconds, computed after the inverse (`target_transform="log1p"`).
- `_prepare_raw_files` parses each polyline into its number of points and its first and last point; the route is known only after the trip and is not a feature.
- `start_time`: TIMESTAMP is Unix time in UTC; the pickup profile by UTC hour shifts by one hour at both daylight-saving switches (decision table), so we convert it to Porto local time without a time zone.
- Rows dropped (counts in the decision table): under 2 GPS points; a TRIP_ID that occurs twice or more (we cannot tell which copy is right); a start outside Greater Porto (lat 41.0 to 41.3, lon -8.8 to -8.4); under 30 seconds (one GPS step: a meter switched on and off without a ride) or over 3 hours (a meter left running); a straight line from start to end faster than 120 km/h (a GPS jump); an end point within 100 m of the start point; and the last trips, which start on 1 July 2014 in local time.
- The 100 m cut (Lennart, CC 2026-10-26): in the app framing nobody books a ride to their own pickup point, so a trip that ends within 100 m of its start is no task row (USE-7); `nyc_taxi_trip_duration_1m` takes the same radius (it dropped only identical end points before; pkdd's 15-second GPS clock turns a return to the start into an end within 100 m rather than at the same point), and the cut rests on inputs known at booking, not on the target. These trips are not short: their median travel time is 555 s and 57% take over 5 minutes (round trips, a passenger who returns, a meter left on), and they held 17% of the target's squared spread. They are most of the very short trips (71% of the 15-second trips, 53% of the 30-second ones, 1.9% of all trips), so once they are gone the time cut only drops the 15-second trips, one GPS step. It replaces a 1-minute cut on the recorded time, which sat on a smooth slope and also dropped short rides that moved.
- We drop TRIP_ID (an id, the start second and the taxi), DAY_TYPE (constant "A"; the data page says it "has not been correctly calculated") and MISSING_DATA (erroneous per Lam et al. 2015, arXiv:1509.05257, and it describes the trajectory).
- We drop ORIGIN_CALL, the anonymised phone number of a dispatch-central customer: an identifier redundant with the destination. With the destination known it changes LightGBM's R^2 by -0.004 to -0.001 (same setup).
- `call_type` A, B and C become dispatch_central, taxi_stand and street. `origin_stand` is empty unless the taxi was hired at a stand; we set the empty strings missing.
- `taxi_id` stays a categorical feature, since the taxi is known at pickup; it adds 0.008 to 0.014 to LightGBM's R^2 (same setup) and is its top feature by gain. The fleet is the same in every month (decision table), so the split is temporal and not grouped by taxi.
- Anomaly: we keep the 1.2% of trips that jump more than 1 km between two GPS points (missing points, Lam et al. 2015), trips with a drive back on the meter, and the 45,171 (2.8%) that end 100 to 500 m from their start: a meter left on or a round trip is unusual, not impossible.
- The row budget: The cleaned frame holds 1,636,276 trips, above the 1.5M-row budget, and the train side of every window holds more than 1M. Each test window keeps at most 500k of its rows (all of them here), and each train side holds every trip that starts at least one day earlier; the frame keeps every trip a split uses. The 1M train budget is recorded, not applied: a benchmark sub-samples each train side to 1M before a fit with `subsample_train`, by default a random 1M of the newest year before the window, which here is all earlier trips (the file starts on 1 July 2013).

## Splits

Expanding-window temporal splits: 3 test window(s) of 1 month, starting at 2014-06-01, 2014-04-01, 2014-02-01, newest first; train is all earlier data up to a gap of 1 days. The test windows by `start_time`, as listed: 2014-06-01 to 2014-06-30 (146,714 test, 1,484,039 train rows); 2014-04-01 to 2014-04-30 (130,112 test, 1,200,383 train rows); 2014-02-01 to 2014-02-28 (122,831 test, 943,912 train rows). Each test window keeps at most 500k of its rows, drawn at random; each train side holds every earlier row, and a benchmark sub-samples it to 1M rows (by default rows drawn at random from the newest year before each window, extended back in time until it holds that many rows, `subsample_train`).

A model trained on the trips so far predicts the travel times of the next calendar month's trips: 3 test windows, the calendar months June, April and February 2014 (newest first), and train is the trips that start at least one day before the window. The length (the horizon checked, CC 2026-11-11): no source gives a refit cadence. The challenge scored five snapshots of trips under way (320 trips, 14 August to 21 December 2014; Lam et al. 2015, arXiv:1509.05257) with one model trained on its year (1 July 2013 to 30 June 2014), used 1.5 to 6 months later without a refit, so the only horizon the source shows is months long; calendar months are the longest windows that still leave a choice of seasons (60 days would give exactly three windows that tile the half-year). nyc_taxi_trip_duration_1m predicts the same kind of travel time on one-week windows, a length that rests on its weekdays and an ETA service's refit; its source shows no horizon either. The windows (CC 2026-11-10 and 2026-11-11, the curator's pick): June, the newest, with São João (23-24 June); April, with Easter (18-20 April); and February, in the winter, when Porto's trips are the slowest of the year (median straight-line speed 15.6 to 16.0 km/h from October to February, 16.7 to 17.6 from May to August). The file covers one year (July 2013 to June 2014), so no other year can be tested, and months from January 2014 keep half the trips for training; the three are spread evenly over the six months open. The gap of one day is part of the task: a trip lasts up to 3 hours, so at a refit the last trips before it have no travel time yet; without the gap 47, 7 and 21 train trips (June, April, February) would end after the window start, with it none. The 5,523 trips of 31 May 2014, the newest window's gap day, lie in no split, so the frame leaves them out. The February window's train side holds the winter months before it, while April and June have no earlier copy of their month in train.

3 repeat(s) x 1 fold(s) with seed 4267; train 943,912 to 1,484,039 rows, test 122,831 to 146,714 rows. Prediction horizon: 1 months. Gap between train and test: 1 days. Row budget: at most 500k test rows per split; a benchmark trains on at most 1M. The train sides keep every row available to them; `subsample_train` draws the 1M rows a benchmark fits on from the newest year before each window, extended back in time until it holds that many rows, at random, as rows.

| repeat | fold | n_train | n_test | train_start | train_end | test_start | test_end |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 1484039 | 146714 | 2013-07-01 01:00:53 | 2014-05-30 23:59:59 | 2014-06-01 00:00:22 | 2014-06-30 23:59:58 |
| 1 | 0 | 1200383 | 130112 | 2013-07-01 01:00:53 | 2014-03-30 23:58:39 | 2014-04-01 00:00:34 | 2014-04-30 23:59:47 |
| 2 | 0 | 943912 | 122831 | 2013-07-01 01:00:53 | 2014-01-30 23:59:10 | 2014-02-01 00:00:25 | 2014-02-28 23:59:55 |


### The test windows

Each test window against its train side, by statistics of the data, never of a model: the target, and the population stability index (PSI) of each feature, its largest value and the features that drift most (below 0.1 little shift, above 0.25 a large one), and the share of test rows with a category the train side never shows. Up to 20,000 rows per side. The candidates the windows were chosen from: `.venv/bin/python -m data_foundry.curation.cli dataset windows pkdd_15_taxi_trip_time_prediction_ii_1m`.

| window | period | n_test | train_share | target_test | target_train | psi_max | top_drift | unseen_categories |
|---|---|---|---|---|---|---|---|---|
| 0 | Jun 2014 | 146714 | 0.91 | mean 6.402, median 6.423, p10 5.707, p90 7.091 | mean 6.404, median 6.423, p10 5.656, p90 7.103 | 0.016 | taxi_id (0.02), origin_stand (0.01), end_lon (0.01) | 0 |
| 1 | Apr 2014 | 130112 | 0.736 | mean 6.394, median 6.423, p10 5.656, p90 7.078 | mean 6.401, median 6.423, p10 5.656, p90 7.103 | 0.013 | origin_stand (0.01), taxi_id (0.01), start_lon (0.00) | 0.001 |
| 2 | Feb 2014 | 122831 | 0.579 | mean 6.415, median 6.447, p10 5.656, p90 7.128 | mean 6.401, median 6.423, p10 5.656, p90 7.091 | 0.027 | origin_stand (0.03), start_lat (0.02), taxi_id (0.01) | 0 |

## Decisions

### 1. Rows dropped before the split

Trips without a travel time or a destination, duplicate ids, GPS errors, meter misuse and trips that end where they start go, and so do the last trips of the file, which start on 1 July in local time.

| rows dropped | dropped | left |
|---|---|---|
| fewer than 2 GPS points (no travel time or no destination) | 36510 | 1674160 |
| TRIP_ID (start second and taxi) more than once among the trips with 2 points or… | 21 | 1674139 |
| start outside Greater Porto | 937 | 1673202 |
| travel time under 30 s | 7363 | 1665839 |
| travel time over 3 h | 827 | 1665012 |
| straight line from start to end faster than 120 km/h | 1189 | 1663823 |
| end point within 100 m of the start point (no destination a passenger would boo… | 27426 | 1636397 |
| start on 2014-07-01 in Porto local time | 121 | 1636276 |

### 2. Temporal split; the taxi stays a feature, not a group

A v2 task is grouped or temporal, not both, so the verdict's 'temporal split, taxi as group' can only be one of them. The fleet is the same in every month (99.93% to 100% of each test month's trips are by taxis seen before), so a model in use predicts trips of taxis it has seen; a split by taxi would test new drivers, which deployment rarely meets.

| test month | trips | taxis | taxis new in this month | trips by a taxi seen before |
|---|---|---|---|---|
| 2014-02 | 122831 | 433 | 0 | 100.00% |
| 2014-04 | 130112 | 432 | 1 | 99.93% |
| 2014-06 | 146714 | 428 | 0 | 100.00% |

### 3. Start time in Porto local time

TIMESTAMP is Unix time (UTC): the weekday pickup profile moves by one UTC hour at each daylight-saving switch and matches again once shifted, so hours of the day are only comparable in local time.

| switch | correlation, same UTC hour | correlation, shifted by one hour |
|---|---|---|
| 2013-10-27, summer to winter time | 0.92 | 0.992 |
| 2014-03-30, winter to summer time | 0.901 | 0.994 |

## Bundle checks

0 error(s), 0 warning(s), 0 info (28 checks run, plus the dataset's own checks).


## Data checks

### Feature summary

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| origin_stand | category | 844707 | 51.8 | 63 | 15, 57, 9, 23, 33, 18, 53, 13, 36, 12 |
| call_type | category | 0 | 0 | 3 | taxi_stand, street, dispatch_central |
| taxi_id | category | 0 | 0 | 439 | 20000129, 20000492, 20000621, 20000403, 20000364, 20000483, 20000678, 20000089,… |
| start_time | datetime64\[ns\] | 0 | 0 | 1.58012e+06 | 2014-02-09 04:01:29, 2014-03-25 14:47:09, 2014-04-02 08:44:30, 2013-10-11 09:07… |
| start_lon | float64 | 0 | 0 | 18110 | -8.5856, -8.5856, -8.5856, -8.5857, -8.5856, -8.5857, -8.5857, -8.5856, -8.5857… |
| start_lat | float64 | 0 | 0 | 13714 | 41.1486, 41.1827, 41.1827, 41.1486, 41.1827, 41.1486, 41.1486, 41.1486, 41.1485… |
| end_lon | float64 | 0 | 0 | 28453 | -8.5856, -8.5857, -8.5857, -8.5857, -8.5856, -8.5856, -8.5857, -8.6702, -8.5857… |
| end_lat | float64 | 0 | 0 | 27722 | 41.1488, 41.1488, 41.1488, 41.1488, 41.1488, 41.1488, 41.1488, 41.1488, 41.1489… |
| log1p_travel_time | float64 | 0 | 0 | 711 | 6.2364, 6.1759, 6.2934, 6.1442, 6.3208, 6.1115, 6.2653, 6.3474, 6.0426, 6.0776 |

### Target distribution

| index | y_missing_count | non_positive_pct | skew_y | skew_log | var_y | var_log | log_used | aic_exponential | aic_lognormal | dist_hint |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | -0.254 | -0.899 | 0.36 | 0.009 | log | 1.05834e+06 | 1.66169e+17 | exponential |

### Numeric features

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| start_lon | 163075 | -8.61727 | 0.02491 | -8.72663 | -8.42183 |
| start_lat | 163075 | 41.157 | 0.0129218 | 41.0082 | 41.2827 |
| end_lon | 163075 | -8.62017 | 0.0362099 | -9.44246 | -6.73251 |
| end_lat | 163075 | 41.1624 | 0.0327179 | 38.6992 | 42.0764 |
| log1p_travel_time | 163075 | 6.40127 | 0.599851 | 3.43399 | 9.28739 |

### Categorical features

<details>
<summary>Show the table (18 rows)</summary>

| column | rank | value | count | pct |
|---|---|---|---|---|
| call_type | 1 | taxi_stand | 79986 | 49.05 |
| call_type | 2 | street | 47955 | 29.41 |
| call_type | 3 | dispatch_central | 35134 | 21.54 |
| origin_stand | 1 | &lt;NA> | 84213 | 51.64 |
| origin_stand | 2 | 15 | 7914 | 4.85 |
| origin_stand | 3 | 57 | 4863 | 2.98 |
| origin_stand | 4 | 9 | 3450 | 2.12 |
| origin_stand | 5 | 23 | 3317 | 2.03 |
| start_time | 1 | 2014-02-09 04:01:29 | 3 | 0 |
| start_time | 2 | 2014-03-25 14:47:09 | 3 | 0 |
| start_time | 3 | 2014-04-02 08:44:30 | 3 | 0 |
| start_time | 4 | 2013-10-11 09:07:36 | 2 | 0 |
| start_time | 5 | 2013-12-23 02:41:06 | 2 | 0 |
| taxi_id | 1 | 20000129 | 746 | 0.46 |
| taxi_id | 2 | 20000492 | 729 | 0.45 |
| taxi_id | 3 | 20000621 | 729 | 0.45 |
| taxi_id | 4 | 20000403 | 724 | 0.44 |
| taxi_id | 5 | 20000364 | 723 | 0.44 |

</details>

## Build

| field | value |
|---|---|
| uuid | 01a217fc-2c03-74d9-baff-ea7cc624d41c |
| checksum | v2:bb35c17a02f96d5c8cf27db6b561de58426c91e15bf9f30527506e4d1065d0bf |
| built_at | 2026-11-26T13:12:28+00:00 |
| path | pkdd_15_taxi_trip_time_prediction_ii_1m/01a217fc-2c03-74d9-baff-ea7cc624d41c |
| data_foundry_version | 0.0.5 |
| git_sha | e3ddd55462cc45eed6aa71c38abd183086888b36 |
| libraries | {'python': '3.12.3', 'pandas': '2.3.3', 'numpy': '2.1.3', 'pyarrow': '20.0.0', 'scikit-learn': '1.7.2', 'polars': '1.41.1'} |
