---
report_format: data-foundry-report-v2
unique_name: nyc_taxi_trip_duration_1m
container_format: 2
checksum: v2:593b09d390a6b60f1cf87ca279ad34f1f7a57050949d2f4f759c621b187d4e3a
build:
  uuid: 01a217ff-7634-71b3-b9be-45b56e41ec3e
  checksum: v2:593b09d390a6b60f1cf87ca279ad34f1f7a57050949d2f4f759c621b187d4e3a
  built_at: '2026-11-26T13:15:59+00:00'
  path: nyc_taxi_trip_duration_1m/01a217ff-7634-71b3-b9be-45b56e41ec3e
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
  n_rows: 1434623
  n_features: 7
  dtypes:
    category: 1
    datetime64[ns]: 1
    float64: 6
  n_test_dataset_rows: null
task:
  target: log1p_trip_duration
  problem_type: regression
  metric: rmsle
  metric_origin: source
  scoring_columns: null
  split_regime: temporal_non_iid
  stratify_on: null
  time_on: pickup_datetime
  group_on: null
  group_labels: null
  group_time_on: null
  grouping: null
splits:
  n_repeats: 3
  n_folds: 1
  random_state: 4267
  time_horizon: 7
  time_horizon_unit: days
  time_gap: 1
  time_gap_unit: days
  reason: 'The competition gives no horizon: its test set is a random 30% of the same
    days (curation_comments), so a random split is optimistic here. An ETA service
    refits often; a week is the shortest window that holds each weekday once, and
    no source speaks for a calendar month here (unlike pkdd_15_taxi_trip_time_prediction_ii_1m,
    whose challenge used one model for months), though under the floor as amended
    on 2026-11-11 months would give three windows (June, May, and April on 49.1% of
    the trips). The trips cover January to June 2016, and only the weeks from 8 April
    on keep half the trips for training, so another year or the winter cannot be tested:
    January to March (New Year''s Day, Martin Luther King Day, Presidents'' Day, the
    blizzard of 23 January) are training only. Of the 12 eligible weeks (Friday to
    Thursday) we test three (CC 2026-11-10), newest first: 24-30 June, the newest;
    27 May to 2 June, the week of Memorial Day (Monday 30 May), the one public holiday
    among them (7,041 trips a day against 7,973 and 8,065 in the weeks before and
    after, median straight-line speed 13.3 km/h against 12.2 and 12.4); and 8-14 April,
    a spring week (8,522 trips a day, 12.6 km/h). The features do not drift in any
    eligible week (largest population stability index 0.003), so the choice rests
    on the calendar. The gap of one day is part of the task: a trip lasts up to 3
    hours, so at a refit the last trips before it have no duration yet; without the
    gap 77, 112 and 100 train trips per window would end after the window start, with
    it none. The 8,028 trips of 23 June, the gap day before the newest window, lie
    in no split, so the frame leaves them out. Measured before 2026-11-10, with the
    last three weeks of June as the windows: LightGBM (300 trees, learning rate 0.1,
    63 leaves, a random 200k of each train side, one fit per split) scored RMSE 0.357-0.381
    on the weekly windows, 0.355-0.364 on 3 folds of whole days and 0.353-0.355 on
    3 random folds when the encoding keeps the hour (skrub''s DatetimeEncoder), and
    0.414-0.441, 0.401-0.410 and 0.390-0.392 with AutoGluon''s date parts. Trips of
    one day sharing traffic and weather explain about 0.01 of the gap; the rest is
    the distance in time.'
  n_train:
    min: 766644
    max: 1382016
  n_test:
    min: 49284
    max: 59653
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
  accepted:
    meta_license_unknown: The TLC trip records carry no explicit licence (NYC Open
      Data terms of use); the Kaggle sample we download is under the competition's
      rules.
decisions:
- Trips under 30 s or over 3 h are dropped
- Trips whose drop-off lies within 100 m of the pickup are dropped
- store_and_fwd_flag is dropped
- Trips across the switch to daylight saving time lose the skipped hour
---

# nyc_taxi_trip_duration_1m

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Regression of `log1p_trip_duration`, scored with `rmsle` on temporal splits by `pickup_datetime`. 1,434,623 rows and 7 features. Source: GOV Website (2016).

Built as `01a217ff-7634-71b3-b9be-45b56e41ec3e` on 2026-11-26. See [Build](#build).

## In brief

**Question.** How long will a New York taxi ride take, from pickup to drop-off?

**Use case.** When a passenger gets in and names the destination, the taxi's system estimates the arrival time with a model refit every week on the trips since January.

**One row.** One yellow-cab trip in New York City, January to June 2016, from a sample of the Taxi and Limousine Commission's trip records (1,442,651 trips after cleaning; the 8,028 of 23 June 2016, the gap day before the newest window, are in no split).

**Predicted.** The trip's duration in seconds, on a log scale.

**Known at prediction time.** The pickup time and point, the drop-off point taken as the destination, the number of passengers and the company of the cab's meter system.

**What the test data stands for.** The test windows are three weeks of 2016: the newest (24-30 June), the Memorial Day week (27 May-2 June) and a spring week (8-14 April); a week is the shortest window that holds each weekday once. Training is every trip picked up at least a day before the window, of which a benchmark fits on at most a random million.

**Our changes to the source.** We split by week instead of the competition's random sample of the same days, drop a flag set only after the trip, non-rides under 30 seconds, broken clocks over 3 hours and trips whose drop-off lies within 100 m of the pickup, blank impossible passenger counts, and correct trips across the daylight-saving switch.

> **Use case fit: approximate (a stand-in with a known gap).** Everything the model sees is known at pickup except the destination: the recorded drop-off point stands in for the one named at pickup, and differs from it when a passenger changes the destination or gets out early. The task is framed without a routing estimate.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision, its sources and the review: [`curation/records/nyc_taxi_trip_duration.md`](../../../../curation/records/nyc_taxi_trip_duration.md)
- The original source: <https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page>
- A copy (the Kaggle competition's sample of the 2016 trips, which we download): <https://www.kaggle.com/c/nyc-taxi-trip-duration>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/nyc_taxi_trip_duration/`. To get them:

```text
We download the training file of the Kaggle competition (its rules must be accepted on the competition page
first). train.csv holds 1,458,644 trips (sha256 fc8c777a4ab99a362d8b6b6f2038ff8a2c4625b9593248a47352d0d26fa99927),
a sample of the 2016 yellow-cab trip records that the NYC Taxi and Limousine Commission first published on
its trip record page (https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page). NYC Open Data still
serves them with the coordinates as "2016 Yellow Taxi Trip Data" (https://data.cityofnewyork.us/d/uacg-pexx).

mkdir -p local-data-warehouse/nyc_taxi_trip_duration
kaggle competitions download -c nyc-taxi-trip-duration -f train.zip -p local-data-warehouse/nyc_taxi_trip_duration
unzip local-data-warehouse/nyc_taxi_trip_duration/train.zip -d local-data-warehouse/nyc_taxi_trip_duration/
rm local-data-warehouse/nyc_taxi_trip_duration/train.zip
```

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/nyc_taxi_trip_duration_1m   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/nyc_taxi_trip_duration_1m   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | GOV Website: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page |
| year | 2016 |
| domain | industry & manufacturing |
| license |  |
| data_tags | Non-IID, Temporal, Spatial |
| reference | nyctlc2016trips,risdal2017nyctaxi |
| copy: the Kaggle competition's sample of the 2016 trips, which we download | Kaggle (2017): https://www.kaggle.com/c/nyc-taxi-trip-duration; license: Kaggle Competition Rules |
| rows x columns | 1,434,623 x 8 |
| task.target | log1p_trip_duration |
| task.problem_type | regression |
| task.metric | rmsle |
| task.split_regime | temporal_non_iid |
| task.time_on | pickup_datetime |

**Metric**

| field | value |
|---|---|
| name | `rmsle` (standard; takes value; lower is better) |
| origin | source: the source's metric |
| original | RMSLE (Root Mean Squared Logarithmic Error) |
| reference | https://www.kaggle.com/competitions/nyc-taxi-trip-duration/overview/evaluation |
| definition | sqrt(mean((log(p+1) - log(a+1))^2)) on trip_duration in seconds, computed after the inverse of our log1p_trip_duration target. |
| target scale | ships on the `log1p` scale for modelling; scored on the original scale after the inverse of `log1p` |

<details>
<summary>Feature types: 1 categorical, 0 string, 1 datetime</summary>

- categorical (1): `vendor_id`
- string (0): none
- datetime (1): `pickup_datetime (%Y-%m-%d %H:%M:%S)`

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@misc{nyctlc2016trips,
  author = {{NYC Taxi and Limousine Commission}},
  title = {{TLC} Trip Record Data: Yellow Taxi Trip Records, January to June 2016},
  year = {2016},
  howpublished = {\url{https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page}}
}
@misc{risdal2017nyctaxi,
  author = {Meg Risdal},
  title = {New York City Taxi Trip Duration},
  year = {2017},
  howpublished = {\url{https://kaggle.com/competitions/nyc-taxi-trip-duration}},
  note = {Kaggle playground competition on a sample of the 2016 yellow taxi trip records of the NYC Taxi and Limousine Commission}
}
```

</details>

## Sample rows

The first 5 of 1,434,623 rows of the final frame (the oldest rows: the frame is sorted by `pickup_datetime`). Cells are cut at 40 characters.

| log1p_trip_duration | vendor_id | pickup_datetime | passenger_count | pickup_longitude | pickup_latitude | dropoff_longitude | dropoff_latitude |
|---|---|---|---|---|---|---|---|
| 6.74524 | VeriFone | 2016-01-01 00:00:17 | 5 | -73.9817 | 40.7192 | -73.9388 | 40.8292 |
| 7.16627 | Creative Mobile Technologies | 2016-01-01 00:00:53 | 1 | -73.9851 | 40.7472 | -73.958 | 40.7175 |
| 6.01372 | VeriFone | 2016-01-01 00:01:01 | 5 | -73.9653 | 40.801 | -73.9475 | 40.8152 |
| 5.63835 | Creative Mobile Technologies | 2016-01-01 00:01:14 | 1 | -73.9823 | 40.7513 | -73.9913 | 40.7503 |
| 6.60259 | Creative Mobile Technologies | 2016-01-01 00:01:20 | 1 | -73.9701 | 40.7598 | -73.9894 | 40.743 |

## Curation notes

We start with train.csv of the Kaggle playground competition "New York City Taxi Trip Duration" (2017): 1,458,644 yellow-cab trips with pickup times from 2016-01-01 to 2016-06-30, sampled from the trip records of the NYC Taxi and Limousine Commission (TLC).

- Prediction point: when the meter is engaged and the passenger has named the destination, an ETA from the vendor of the cab's meter system, the pickup time and point, the passenger count and the dropoff point. The dropoff point is recorded when the meter is disengaged; we take it as the destination named at pickup (Lennart, 2026-09-21), and the data page keeps it on purpose.
- Target: `log1p_trip_duration`, the trip duration in seconds, log1p-scaled. The competition scored RMSLE on the duration in seconds, which the metric computes after the inverse (`target_transform="log1p"`).
- We drop id, an identifier, and dropoff_datetime, which equals pickup_datetime plus the target.
- We drop store_and_fwd_flag: it says whether the trip record "was held in vehicle memory before sending to the vendor" (TLC data dictionary), and the record is sent after the trip, so the flag is not known at the prediction point.
- We map vendor_id to the vendor names of the TLC data dictionary (a category); pickup_datetime is a datetime.
- We drop 7 trips that are exact copies of another trip under a second id.
- We take 3,600 s off the trips picked up before 02:00 on 2016-03-13 and dropped off after the clocks jumped to 03:00. The times are wall-clock times, so these trips were recorded one hour too long (decision table).
- We drop trips shorter than 30 s, which are not rides (most start and end at one point), and trips longer than 3 h, whose clock is broken (a cluster just below 24 h from VeriFone meters at walking speed; decision table). The two filters remove 0.47% of the trips.
- We drop 38 trips with an end outside the box of longitude -75 to -72 and latitude 40 to 41.5: GPS errors on trips of a few minutes.
- We drop the trips whose drop-off lies within 100 m of the pickup (Lennart, CC 2026-10-26, USE-7; the radius of pkdd_15_taxi_trip_time_prediction_ii_1m): nobody names a destination that close to where they are picked up, so these rows lack the input the ETA acts on. They are the 4,539 trips (0.31%, 0.29-0.34% in every month, 73% VeriFone) whose drop-off coordinates equal the pickup coordinates to the last digit, mean target 6.04 against 6.47 for the other trips, and about 4,500 more at other coordinates: 1,082 within 10 m (median 69 s) and 3,436 at 10 to 100 m (median 230 s) (decision table).
- We set passenger_count to missing where it is 0 (the driver did not enter it) or above the 6 seats of a cab (8 and 9), 23 trips in all, and keep the trips.
- Anomaly: 46 kept trips imply more than 100 km/h. We keep them, as they cannot be told from real trips with certainty.
- Split: three weekly test windows, the newest week (24-30 June 2016), the Memorial Day week (27 May-2 June) and a week in April (8-14 April) (splits_comment; CC 2026-11-10). The competition's test set is a random 30% of every day of the same half-year, so its leaderboard measures interpolation within the period; we do not use test.csv.
- Note: pickup_datetime is the only time feature, and the hour matters most. LightGBM (300 trees, learning rate 0.1, 63 leaves, a random 200k of each train side, one fit per window) scored RMSE 0.373, 0.357 and 0.381 on the windows before 2026-11-10, the last three weeks of June (newest first), when the encoding keeps the hour (skrub's DatetimeEncoder in tabarena_default) and 0.429, 0.414 and 0.441 with AutoGluon's date parts, which lose it.
- Note: the Kaggle rules (Sec. 7) allow academic research and other non-commercial use and forbid redistribution; the TLC publishes the same records on NYC Open Data without an explicit licence.
- The row budget: The two newer train sides hold 1,382,016 and 1,169,775 trips, above the 1M-row budget, so the dataset ships only as this version (definitions.md, Lennart 2026-10-21); the April one holds 766,644. Each test window keeps at most 500k of its rows (none reaches it), and each train side holds every trip picked up at least a day before the window, so the frame keeps every trip a split uses: all but the 8,028 of 23 June, the gap day before the newest window. The 1M train budget is recorded, not applied: a benchmark sub-samples each train side over 1M to 1M before a fit with `subsample_train`, by default a random 1M of the newest year before the window. The data cover six months of 2016, so the newest year is all earlier trips: as in delivery_eta_1m, the sample is random rather than the latest trips, and it covers the whole half-year.

## Splits

Expanding-window temporal splits: 3 test window(s) of 7 days, starting at 2016-06-24, 2016-05-27, 2016-04-08, newest first; train is all earlier data up to a gap of 1 days. The test windows by `pickup_datetime`, as listed: 2016-06-24 to 2016-06-30 (52,607 test, 1,382,016 train rows); 2016-05-27 to 2016-06-02 (49,284 test, 1,169,775 train rows); 2016-04-08 to 2016-04-14 (59,653 test, 766,644 train rows). Each test window keeps at most 500k of its rows, drawn at random; each train side holds every earlier row, and a benchmark sub-samples it to 1M rows (by default rows drawn at random from the newest year before each window, extended back in time until it holds that many rows, `subsample_train`).

The competition gives no horizon: its test set is a random 30% of the same days (curation_comments), so a random split is optimistic here. An ETA service refits often; a week is the shortest window that holds each weekday once, and no source speaks for a calendar month here (unlike pkdd_15_taxi_trip_time_prediction_ii_1m, whose challenge used one model for months), though under the floor as amended on 2026-11-11 months would give three windows (June, May, and April on 49.1% of the trips). The trips cover January to June 2016, and only the weeks from 8 April on keep half the trips for training, so another year or the winter cannot be tested: January to March (New Year's Day, Martin Luther King Day, Presidents' Day, the blizzard of 23 January) are training only. Of the 12 eligible weeks (Friday to Thursday) we test three (CC 2026-11-10), newest first: 24-30 June, the newest; 27 May to 2 June, the week of Memorial Day (Monday 30 May), the one public holiday among them (7,041 trips a day against 7,973 and 8,065 in the weeks before and after, median straight-line speed 13.3 km/h against 12.2 and 12.4); and 8-14 April, a spring week (8,522 trips a day, 12.6 km/h). The features do not drift in any eligible week (largest population stability index 0.003), so the choice rests on the calendar. The gap of one day is part of the task: a trip lasts up to 3 hours, so at a refit the last trips before it have no duration yet; without the gap 77, 112 and 100 train trips per window would end after the window start, with it none. The 8,028 trips of 23 June, the gap day before the newest window, lie in no split, so the frame leaves them out. Measured before 2026-11-10, with the last three weeks of June as the windows: LightGBM (300 trees, learning rate 0.1, 63 leaves, a random 200k of each train side, one fit per split) scored RMSE 0.357-0.381 on the weekly windows, 0.355-0.364 on 3 folds of whole days and 0.353-0.355 on 3 random folds when the encoding keeps the hour (skrub's DatetimeEncoder), and 0.414-0.441, 0.401-0.410 and 0.390-0.392 with AutoGluon's date parts. Trips of one day sharing traffic and weather explain about 0.01 of the gap; the rest is the distance in time.

3 repeat(s) x 1 fold(s) with seed 4267; train 766,644 to 1,382,016 rows, test 49,284 to 59,653 rows. Prediction horizon: 7 days. Gap between train and test: 1 days. Row budget: at most 500k test rows per split; a benchmark trains on at most 1M. The train sides keep every row available to them; `subsample_train` draws the 1M rows a benchmark fits on from the newest year before each window, extended back in time until it holds that many rows, at random, as rows.

| repeat | fold | n_train | n_test | train_start | train_end | test_start | test_end |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 1382016 | 52607 | 2016-01-01 00:00:17 | 2016-06-22 23:59:46 | 2016-06-24 00:00:01 | 2016-06-30 23:59:39 |
| 1 | 0 | 1169775 | 49284 | 2016-01-01 00:00:17 | 2016-05-25 23:59:55 | 2016-05-27 00:00:41 | 2016-06-02 23:59:54 |
| 2 | 0 | 766644 | 59653 | 2016-01-01 00:00:17 | 2016-04-06 23:59:57 | 2016-04-08 00:00:29 | 2016-04-14 23:59:54 |


### The test windows

Each test window against its train side, by statistics of the data, never of a model: the target, and the population stability index (PSI) of each feature, its largest value and the features that drift most (below 0.1 little shift, above 0.25 a large one), and the share of test rows with a category the train side never shows. Up to 20,000 rows per side. The candidates the windows were chosen from: `.venv/bin/python -m data_foundry.curation.cli dataset windows nyc_taxi_trip_duration_1m`.

| window | period | n_test | train_share | target_test | target_train | psi_max | top_drift | unseen_categories |
|---|---|---|---|---|---|---|---|---|
| 0 | Jun 2016 | 52607 | 0.963 | mean 6.512, median 6.526, p10 5.553, p90 7.463 | mean 6.478, median 6.497, p10 5.529, p90 7.401 | 0.003 | dropoff_longitude (0.00), pickup_latitude (0.00), dropoff_latitude (0.00) | 0 |
| 1 | May 2016 - Jun 2016 | 49284 | 0.815 | mean 6.483, median 6.512, p10 5.501, p90 7.424 | mean 6.465, median 6.483, p10 5.517, p90 7.386 | 0.003 | pickup_longitude (0.00), dropoff_latitude (0.00), pickup_latitude (0.00) | 0 |
| 2 | Apr 2016 | 59653 | 0.534 | mean 6.487, median 6.51, p10 5.533, p90 7.407 | mean 6.451, median 6.479, p10 5.513, p90 7.353 | 0.002 | pickup_longitude (0.00), pickup_latitude (0.00), dropoff_longitude (0.00) | 0 |

## Decisions

### 1. Trips under 30 s or over 3 h are dropped

Below 30 s most records start and end at one point (no ride); above 3 h the clock is broken: a cluster just below 24 h from VeriFone meters at walking speed, whose TLC records carry the fares of trips of minutes.

| band | trips | median_km | share_at_one_point | median_kmh | share_verifone | kept |
|---|---|---|---|---|---|---|
| < 10 s | 1984 | 0.002 | 0.721 | 1.326 | 0.34 | no |
| 10-29 s | 2798 | 0.005 | 0.565 | 1.067 | 0.388 | no |
| 30-59 s | 3812 | 0.172 | 0.209 | 13.788 | 0.456 | yes |
| 1-2 min | 19222 | 0.554 | 0.029 | 20.913 | 0.528 | yes |
| 2 min-1 h | 1418575 | 2.121 | 0.003 | 12.733 | 0.535 | yes |
| 1-2 h | 9994 | 20.134 | 0.002 | 16.112 | 0.56 | yes |
| 2-3 h | 141 | 18.385 | 0 | 6.86 | 0.56 | yes |
| 3-22 h | 207 | 4.121 | 0.014 | 0.446 | 0.918 | no |
| 22-24 h | 1900 | 2.322 | 0.004 | 0.098 | 1 | no |
| >= 24 h | 4 | 12.942 | 0 | 0.015 | 0 | no |

### 2. Trips whose drop-off lies within 100 m of the pickup are dropped

The task takes the drop-off point as the destination named at pickup, and nobody names a destination within 100 m of where they are picked up: these rows lack the input the ETA acts on (a failed GPS fix at the drop-off, a ride that did not happen, or a trip back to the start). The same radius serves pkdd_15_taxi_trip_time_prediction_ii_1m. Trips of 30 s to 3 h, before the box filter:

| distance | trips | mean_log1p_duration | median_seconds | share_verifone |
|---|---|---|---|---|
| same coordinates | 4558 | 6.038 | 494.5 | 0.728 |
| within 10 m, not the same | 1082 | 4.635 | 69 | 0.36 |
| 10-100 m | 3436 | 5.502 | 230 | 0.51 |
| 100 m or more | 1442668 | 6.478 | 665 | 0.534 |

### 3. store_and_fwd_flag is dropped

The flag says whether the trip record was held in the vehicle's memory because there was no connection to the server when it was sent, which happens at the end of the trip: it is not known when the ETA is made. Only Creative Mobile Technologies meters set it.

| store_and_fwd_flag | trips | of them Creative Mobile Technologies | mean log1p duration (30 s to 3 h) |
|---|---|---|---|
| N | 1450592 | 670297 | 6.472 |
| Y | 8045 | 8045 | 6.681 |

### 4. Trips across the switch to daylight saving time lose the skipped hour

The times are wall-clock times, so a trip picked up before 02:00 on 2016-03-13 and dropped off after the clocks jumped to 03:00 is recorded one hour too long. Pickups between 01:00 and 01:59 (kept trips) on that night and on the Sundays before and after:

| index | trips | recorded at least 60 min | median recorded (min) | median shipped (min) | 75th percentile shipped (min) |
|---|---|---|---|---|---|
| 2016-03-06 | 503 | 0 | 10.5 | 10.5 | 16 |
| 2016-03-13 | 472 | 86 | 11.9 | 10.6 | 17 |
| 2016-03-20 | 494 | 0 | 10.4 | 10.4 | 16.1 |

## Bundle checks

0 error(s), 0 warning(s), 0 info (28 checks run, plus the dataset's own checks).


Accepted on purpose:

- `meta_license_unknown`: The TLC trip records carry no explicit licence (NYC Open Data terms of use); the Kaggle sample we download is under the competition's rules.

## Data checks

### Feature summary

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| vendor_id | category | 0 | 0 | 2 | VeriFone, Creative Mobile Technologies |
| pickup_datetime | datetime64\[ns\] | 0 | 0 | 1.35822e+06 | 2016-01-13 08:25:24, 2016-05-07 18:34:41, 2016-05-30 14:17:36, 2016-06-24 23:00… |
| passenger_count | float64 | 15 | 0 | 6 | 1.0, 2.0, 5.0, 3.0, 6.0, 4.0 |
| pickup_longitude | float64 | 0 | 0 | 21829 | -73.9821, -73.9823, -73.982, -73.9822, -73.9821, -73.9823, -73.982, -73.9822, -… |
| pickup_latitude | float64 | 0 | 0 | 44376 | 40.7741, 40.7741, 40.7741, 40.7511, 40.7742, 40.7741, 40.7741, 40.7741, 40.774,… |
| dropoff_longitude | float64 | 0 | 0 | 33021 | -73.9821, -73.9774, -73.9823, -73.982, -73.9911, -73.9921, -73.9822, -73.9912, … |
| dropoff_latitude | float64 | 0 | 0 | 61983 | 40.7743, 40.7504, 40.7617, 40.7502, 40.7501, 40.75, 40.7743, 40.7564, 40.7577, … |
| log1p_trip_duration | float64 | 0 | 0 | 5997 | 6.1549, 6.1654, 6.0845, 5.8289, 5.9162, 6.0307, 5.8435, 6.1463, 5.7071, 5.7621 |

### Target distribution

| index | y_missing_count | non_positive_pct | skew_y | skew_log | var_y | var_log | log_used | aic_exponential | aic_lognormal | dist_hint |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | -0.181 | -0.57 | 0.537 | 0.014 | log | 930045 | 3.059e+16 | exponential |

### Numeric features

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| passenger_count | 143462 | 1.66765 | 1.31848 | 1 | 6 |
| pickup_longitude | 143462 | -73.9737 | 0.0375089 | -74.1788 | -73.4773 |
| pickup_latitude | 143462 | 40.751 | 0.0277326 | 40.5319 | 41.006 |
| dropoff_longitude | 143462 | -73.9735 | 0.0353647 | -74.6475 | -73.3328 |
| dropoff_latitude | 143462 | 40.7519 | 0.0321314 | 40.2933 | 41.4214 |
| log1p_trip_duration | 143462 | 6.47473 | 0.732793 | 3.43399 | 9.25455 |

### Categorical features

| column | rank | value | count | pct |
|---|---|---|---|---|
| pickup_datetime | 1 | 2016-01-13 08:25:24 | 3 | 0 |
| pickup_datetime | 2 | 2016-05-07 18:34:41 | 3 | 0 |
| pickup_datetime | 3 | 2016-05-30 14:17:36 | 3 | 0 |
| pickup_datetime | 4 | 2016-06-24 23:00:23 | 3 | 0 |
| pickup_datetime | 5 | 2016-06-21 18:07:01 | 2 | 0 |
| vendor_id | 1 | VeriFone | 76592 | 53.39 |
| vendor_id | 2 | Creative Mobile Technologies | 66870 | 46.61 |

## Build

| field | value |
|---|---|
| uuid | 01a217ff-7634-71b3-b9be-45b56e41ec3e |
| checksum | v2:593b09d390a6b60f1cf87ca279ad34f1f7a57050949d2f4f759c621b187d4e3a |
| built_at | 2026-11-26T13:15:59+00:00 |
| path | nyc_taxi_trip_duration_1m/01a217ff-7634-71b3-b9be-45b56e41ec3e |
| data_foundry_version | 0.0.5 |
| git_sha | e3ddd55462cc45eed6aa71c38abd183086888b36 |
| libraries | {'python': '3.12.3', 'pandas': '2.3.3', 'numpy': '2.1.3', 'pyarrow': '20.0.0', 'scikit-learn': '1.7.2', 'polars': '1.41.1'} |
