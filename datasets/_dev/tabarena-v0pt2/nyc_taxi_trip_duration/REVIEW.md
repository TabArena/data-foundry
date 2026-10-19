# nyc_taxi_trip_duration

**Outcome:** added. The Kaggle sample of the 2016 NYC yellow-cab trips, target the log trip duration (regression, an
ETA at pickup with the destination known), temporal with three weekly test windows in June 2016. Ship with concerns:
which source and which rows to ship (issues 1 and 2), and the hour of day depends on the TabArena pipeline (issue 4).

**Main points:** The Kaggle sample or the TLC records; row filters that select on the target; the hour of day depends on
the TabArena pipeline.

**Record fields that disagree with the definition:**

- `domain`: record `Other`, definition `industry & manufacturing`.

**Record judgment:** valid with concerns. NYC TLC yellow-cab records of January to June 2016, sampled by Kaggle for
its 2017 playground competition; ETA at pickup is a real application. The concerns (issues 1-3) are about which rows
and which source to ship, not about validity.

**Issues for Lennart:**

1. **Kaggle sample or the primary TLC records?** The record says the TLC Parquet files serve coordinates up to
   mid-2016. They do not any more: the current files hold `PULocationID` / `DOLocationID` only (2016-01, 03, 06 read
   by me; 2012-06, 2015-01, 2016-07 by the verifier; 2009-01 still has coordinates). The 2016 coordinates survive on
   NYC Open Data (uacg-pexx, 131,165,043 trips in 2016, Socrata API; a bulk export of January to June would be tens of
   GB). Implemented: Kaggle `train.csv` (the published task, 1.46M trips, rows verified against uacg-pexx).
   Alternative: a `_1m` version built from uacg-pexx (all trips of a half-year, sampled per window; also free of the
   Kaggle no-redistribution clause).

2. **Target-selected row filters.** Trips under 30 s (4,782) and over 3 h (2,111) are dropped as data errors: under
   10 s 72% start and end at one point; over 3 h, 1,900 sit between 22 and 24 h, all VeriFone, at 0.1 km/h, and 14
   sampled TLC records of such trips carry fares of $5-$44.50 (or the $52 JFK flat fare). They hold a large share of
   the error: LightGBM RMSE 0.487-0.509 with all trips, 0.412-0.434 without (weekly windows); the verifier finds the
   same order of four model families with and without the cut. Alternative: keep them as the competition did (they
   are in its test set too; zillow_prize in this run keeps its target outliers), or cut only the 22-24 h cluster and
   the multi-day trips (RMSE 0.450-0.470 with only the over-3-h cut).

3. **Window length.** Implemented 3 x 7 days (weekly refit, as delivery_eta_1m and maps_router_eta_1m). Alternative:
   3 x 28 days (2016-04-08..05-05, 05-06..06-02, 06-03..06-30; 217k-232k test trips, train 780k-1.23M = 54-85%):
   LightGBM RMSE 0.422-0.430 against 0.419-0.440 weekly. It spans the spring-to-summer drift and uses every row (no
   `splits_rows_unused`). Calendar months are not possible: January to March holds 49.7% of the trips, under the 50%
   floor. pkdd_15 (this run) uses monthly windows.

4. **Time of day depends on the TabArena pipeline.** `tabarena_default` (skrub's DatetimeEncoder, the BeyondArena
   bundle) keeps the hour; `default` (AutoGluon's date parts, the v0.1 bundle) loses it. LightGBM RMSE 0.380 / 0.365 /
   0.378 against 0.425 / 0.414 / 0.434 on the weekly windows. The definition keeps the raw datetime. Question: which
   pipeline the v0.2 runs use; a harness change or an hour column is needed only for `default`.

5. **Train sides trimmed per window (framework).** The frame (1,451,706 rows) is under 1.5M, so it ships without
   `_1m`; its train sides (1.29M-1.40M) exceed 1M, so `cap_splits` draws an independent random 1M per window (overlap
   808k-839k) and 129,675 trips are in no split. The `_1m` mechanism (`sample_temporal_splits`: one random order,
   frame reduced to the used rows) is refused for a name without `_1m`. First such case in the working copy; accepted
   with a reason for now. Alternative: allow `subsample_to_budget` for temporal frames under 1.5M rows whose train
   sides exceed the budget.

6. **`store_and_fwd_flag` dropped.** TLC dictionary: the record "was held in vehicle memory before sending to the
   vendor ... because the vehicle did not have a connection to the server"; the record holds the dropoff time, so it
   is sent after the trip. Y for 8,045 trips, all Creative Mobile Technologies. Effect: RMSE 0.424 / 0.418 / 0.437 with
   it, 0.425 / 0.419 / 0.440 without. Alternative: keep it, as the competition's test.csv does.

7. **Daylight saving fixed, not dropped.** 86 kept trips lose 3,600 s (decision table). Alternative:
   drop them (0.006% of the rows, all in train sides).

8. **Licence (note only).** Kaggle rules: non-commercial use, no redistribution (Sec. 7A, 7B). The trip records
   themselves are public on NYC Open Data without a licence field.
