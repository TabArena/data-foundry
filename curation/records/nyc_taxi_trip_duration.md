---
unique_name: nyc_taxi_trip_duration
name: NYC Taxi Trip Duration
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 3
tags:
- Review Prio 1 (Atlas)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Varying Delay'
collections:
- New (BeyondArena)
original_source: GOV Website
year: '2016'
domain: industry & manufacturing
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

**Assessment (AI, 2026-10-21):** metric now `Metric.source("rmsle", target_transform="log1p")` instead of rmse on the log1p target: the competition's RMSLE on the trip duration in seconds, computed after the inverse of the shipped log1p (MET-3); the score is the same number as before. Needs a rebuild to reach the container.

CC (2026-10-21, Lennart): the datetime encoding of v0.2 (the cross-dataset item from this review): nothing to change while the v0.2 runs encode datetimes with the hour ("we will always run with datetime encoding in v0.2, most likely some evolution of tabarena_default"); the definition adds no hour column (CLEAN-2). This closes the second open point of the assessment of 2026-10-20.

CC (2026-10-22, Lennart): verdict ship. Record field `domain` takes the definition's value (industry & manufacturing).

**Assessment (AI, 2026-10-22):** ships as `nyc_taxi_trip_duration_1m`; REVIEW.md removed (nothing left open). Not built yet.

CC (2026-10-26, Lennart): reopened from pkdd_15_taxi_trip_time_prediction_ii issue 2, option (c): trips whose drop-off lies within 100 m of the pickup are dropped, as in pkdd ("we just forgot to check for this for nyc"; USE-7: nobody names a destination that close). This supersedes the review panel's keep of the near-start trips at other coordinates (Assessment 2026-10-20, CLEAN-11).

**Assessment (AI, 2026-10-26):** applied in dataset.py: `MIN_STRAIGHT_LINE_KM = 0.1` replaces the identical-coordinate rule. Besides the 4,539 trips at identical coordinates, about 4,500 more leave (of the trips of 30 s to 3 h before the box filter: 1,082 within 10 m, median 69 s; 3,436 at 10-100 m, median 230 s). The sampled frame has 1,165,967 rows (1,166,477 before). dataset check: 0 errors, 0 warnings. Not built, so nothing published changes.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `chicago_taxi_trip_duration` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-10, Lennart): REVIEW issue 1 (which weeks to test), "Option B: Newest week, Memorial Day week, a week in April.": the test windows are 24-30 June, 27 May-2 June and 8-14 April 2016 instead of the last three weeks of June, under SPLIT-15 as amended on 2026-11-10.

CC (2026-11-10, Lennart): the declared horizon (7 days, a one-day gap, windows starting 2016-06-24, 2016-05-27 and 2016-04-08) is checked, kept for a new reason: the competition gives no horizon (its test set is a random 30% of the same days); an ETA service refits often, a week is the shortest window that holds each weekday once, and calendar months would leave only May and June above the 50% floor.

**Assessment (AI, 2026-11-10):** applied in dataset.py: `temporal` with the three cutoffs; test 52,607, 49,284 and 59,653 trips, train 1,382,016, 1,169,775 and 766,644 (95.8%, 81.1%, 53.1% of the 1,442,651 cleaned trips). Late labels recounted on the frame (pickup + duration): without the gap 77, 112 and 100 training trips would end after the window starts (the splits comment's 119 for the old start of 17 June is 117 on today's frame), with the one-day gap none (SPLIT-9, SPLIT-10). The 8,028 trips of 23 June, the newest window's gap day, are in no split, so the container holds 1,434,623; the April train side is under the 1M budget and is fitted whole. `task_summary` (split and row count), `splits_comment` and the notes' Split and row-budget bullets rewritten; the stale 52,779 to 54,532 trips per window are gone, and the LightGBM scores are labelled as measured on the June weeks. Horizon audit (split-auditor, model-free): the Kaggle test set is a random 30% of the same days; no source gives a refit cadence (Uber's DeepETA post: "Periodic auto retraining"); the largest PSI of any eligible week is 0.003; 14 days gives 6 candidates from 8 April, calendar months two windows above the floor (SPLIT-14). `dataset check`: 0 errors, 0 warnings (README not regenerated).

**Assessment (AI, 2026-11-11):** the horizon CC of 2026-11-10 gave as one reason for a week that calendar months would leave only May and June above the 50% floor; under SPLIT-14 as amended on 2026-11-11 months give three windows (June 83.5%, May 66.3%, April 49.1% of the trips). The week stands on its other reasons (no source gives a horizon or a cadence, the week holds each weekday once, the default of the ETA tasks whose labels arrive within a day); the splits comment and the Horizon block are reworded (Lennart, 2026-11-11: "reopen cooking and nyc as needed or change the wording").

## Review

**Outcome:** added as `nyc_taxi_trip_duration_1m`. Verdict ship on 2026-10-22; under the rule on test windows
rewritten on 2026-11-10 you chose B (issue 1): the test windows are the newest June week, the Memorial Day week and a
week in April, and the 7-day length stays with a new reason. Nothing is left open.

**Main points:** Settled on 2026-11-10: the test weeks are 24-30 June, 27 May-2 June and 8-14 April 2016 (issue 1,
B), and the declared horizon is checked.

**Horizon:**

* **Verdict:** keep the 7-day windows with a new reason (medium-high confidence): the competition gives no horizon
  (its test set is a random 30% of the same days); an ETA service refits often, a week is the shortest window that
  holds each weekday once, and no source speaks for a calendar month (under the floor amended on 2026-11-11 months
  would give three windows, June, May and April on 49.1%; before it only May and June).
* **Length:** the splits comment said only "as for the other ETA tasks of the collection", a reason of consistency;
  no source on how often a trip-duration model is refit was found (the Kaggle competition; Uber's DeepETA post:
  "Periodic auto retraining workflows are set up to retrain and validate the model").
* **Gap:** one day: the meter has each duration at drop-off, at most 3 hours after pickup (without the gap 77, 112
  and 100 training trips would end after the start of the windows of issue 1, newest first).
* **Time frame:** January-June 2016, the Kaggle sample; weeks from 8 April keep half the trips for training, so
  January-March (the January blizzard, the holidays) are training only. Adding 2015 from NYC Open Data would be a
  separate rebuild.
* **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | A | One week, one-day gap (implemented) | 7-day windows: 24-30 June, 27 May-2 June and 8-14 April 2016 | the shortest window that holds each weekday once; an ETA service refits often | the competition gives no horizon; no source on a refit cadence |
  | B | A calendar month | June, May and April 2016 (83.5%, 66.3%, 49.1%; before the floor's amendment of 2026-11-11 only May and June) | more trips per window | no source for a month; the windows tile April to June, no choice left |
  | C | 14 days | 6 candidates from 8 April | each weekday twice | three of them cover half the eligible span; no reason from the use case |

* **Recommendation:** A: the shortest window that holds each weekday once; a calendar month leaves two windows, and
  14 days has no reason from the use case. **Decision:** A, B or C?

**Resolved (2026-11-10, Lennart):** A, kept by the horizon audit, as instructed ("if the current time horizon makes
sense and is justifiable keep it and resolve them"); the record's CC line says the declared horizon is checked, and
`splits_comment`, `task_summary.split` and the notes' `Split:` bullet give the new reason.

**Issues for Lennart:**

1. **Test on the newest June week, the Memorial Day week and a week in April instead of the last three weeks of June?**

   * **Problem:**
     - The three test weeks are 10-30 June 2016 (Friday to Thursday), three early-summer weeks with nearly the same trips per day, speeds and durations.
     - The rule keeps the newest week and asks that the others be chosen for the periods a deployed ETA model must handle (seasons, holidays, events), preferring other seasons and months over the weeks just before the newest[^nyc-newest].
     - The trips cover January to June 2016, and with every train side at half the trips or more the eligible weeks start on 8 April, so April, May and June can be tested but another year or the winter cannot.
   * **Background:**
     - Traffic slows from winter to summer: the median straight-line speed falls from 13.2 km/h in January to 12.6 in June, and the mean log duration rises from 6.43 to 6.53.
     - Memorial Day (Monday 30 May) is the one public holiday in the eligible weeks. Its week (27 May to 2 June) has 7,041 trips a day against 7,973 and 8,065 in the weeks before and after, and a median of 13.3 km/h against 12.2 and 12.4; on the Monday itself 5,511 trips at 17.4 km/h.
     - Every train side holds New Year's Day, Martin Luther King Day (18 January) and Presidents' Day (15 February), and the blizzard of 23 January (11.5 km/h, the slowest week of the half-year), so a holiday week tests what a model learnt from earlier holidays.
   * **Effect on the task:** Today the score is a model refit in early summer, three times over. A deployed model also meets spring weeks and holiday weeks; with B, one window of each is in the score.
   * **Data statistics:** from the window statistics of the 12 eligible weeks (8 April to 30 June) and weekly counts of the frame.
     - The features do not drift in any eligible week (largest population stability index 0.003), so the choice rests on the calendar.
     - The June weeks: 7,515 to 7,768 trips a day, 12.7 to 13.0 km/h, mean log duration 6.505 to 6.520 (train sides 6.474 to 6.475).
     - 8-14 April: 8,522 trips a day, 12.6 km/h, mean 6.488 against 6.444 on its train side; 13-19 May, the slowest eligible week: 12.45 km/h, mean 6.560 against 6.460.
   * **Consistency:** No dataset of the working copy declares windows chosen this way yet. The other ETA tasks of the collection (pkdd_15_taxi_trip_time_prediction_ii_1m, maps_router_eta_1m) get the same question in their own review files. The weekly length and the one-day gap stay, as the use case sets them[^nyc-length].
   * **Sources:** the definition [dataset.py](../../datasets/_dev/tabarena-v0pt2/nyc_taxi_trip_duration_1m/dataset.py) (`temporal`, `splits_comment`, `task_summary.split`), the record [nyc_taxi_trip_duration](nyc_taxi_trip_duration.md); the statistics come from `dataset windows nyc_taxi_trip_duration_1m` (2026-11-10).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Last three weeks of June (implemented) | test 10-16, 17-23 and 24-30 June (52,607 to 54,373 trips), train sides 88.4% to 95.8% of the trips | the weeks right after a refit; the most training data | three alike early-summer weeks; no spring week; no holiday |
     | B | Newest week, Memorial Day week, a week in April | test 24-30 June, 27 May-2 June and 8-14 April (52,607, 49,284 and 59,653 trips), train sides 95.8%, 81.1% and 53.1% | three months and two seasons; the one holiday the eligible weeks hold | the April window trains on 53.1%, near the floor; a holiday week is a third of the score, more than its share of a year (about one week in five) |
     | C | Newest week, mid-May, a week in April | test 24-30 June, 13-19 May and 8-14 April (52,607, 58,217 and 59,653 trips), train sides 95.8%, 73.1% and 53.1% | spread evenly over the eligible weeks; holds the slowest eligible week | no holiday; the April window trains on 53.1% |

   * **Recommendation:** B: it keeps the newest week, adds the spring and the one holiday a deployed model meets in these months, and every train side keeps half the trips[^nyc-floor]. **Decision:** A, B or C?

   **Notes for the AI:** on B, `temporal = Temporal(on="pickup_datetime", splits=TemporalSplits(window=7, unit="days",
   gap=1, cutoffs=("2016-04-08", "2016-05-27", "2016-06-24")))` (checked 2026-11-10: train 1,382,016, 1,169,775 and
   766,644 trips; test 52,607, 49,284 and 59,653). On C, the cutoffs `("2016-04-08", "2016-05-13", "2016-06-24")`
   (train 1,382,016, 1,054,711 and 766,644; test 52,607, 58,217 and 59,653). Then rewrite `splits_comment` (the
   windows, why each, the numbers above), `task_summary.split` and the `Split:` bullet of `curation_comments`; recount
   the training trips that end after each new window start (the 77, 119 and 127 of the splits comment are for the June
   weeks) to confirm the one-day gap (SPLIT-9, SPLIT-10); the splits comment's 52,779 to 54,532 trips per window are
   stale since the 100 m cut of 2026-10-26; the LightGBM scores in the notes and the splits comment were measured on
   the June weeks, so drop them or say which windows they come from. Then `dataset check`, a CHANGELOG entry and a CC
   line in the record.

   [^nyc-newest]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): the newest window is always a test window; the others are chosen per dataset from the use case (other
     years, seasons, holidays, events, a change of rules or of the data collection), with statistics of the data as
     evidence and never a model's score; windows in other years, then other seasons, then other months, weeks or days
     are preferred over the windows just before the newest, and walking back from the newest needs its reason too.
   [^nyc-length]: **SPLIT-12** (Should): the window length and the gap come from the use case, here a model refit every
     week; **SPLIT-10** (Should): the one-day gap covers trips still under way at a refit.
   [^nyc-floor]: **SPLIT-14** (Must): at least 3 windows, and no train side below 50% of the rows.

   **Lennart (2026-11-10, change):** Option B: Newest week, Memorial Day week, a week in April.

   **Resolved (2026-11-10, Lennart):** B. `temporal` declares the cutoffs 2016-06-24, 2016-05-27 and 2016-04-08 (7
   days, one-day gap); `splits_comment`, `task_summary.split` and the notes' `Split:` bullet name the windows, why each,
   the numbers and the length's new reason (the competition gives no horizon; a week is the shortest window that holds
   each weekday once, and calendar months would leave only May and June above the floor). Test 52,607, 49,284 and
   59,653 trips, train 1,382,016, 1,169,775 and 766,644 (95.8%, 81.1%, 53.1%). Recounted on the frame: without the gap
   77, 112 and 100 training trips would end after the window starts, with it none, so the one-day gap holds. The stale
   52,779 to 54,532 trips per window are gone, and the LightGBM scores are labelled as measured on the June weeks. The
   8,028 trips of 23 June, the newest window's gap day, are in no split, so the frame holds 1,434,623 of the 1,442,651
   cleaned trips (the task summary's 1,447,167 predated the 100 m cut); the April train side (766,644) is under the 1M
   budget and is fitted whole. The record has the decision and the horizon CC lines. `dataset check`: 0 errors, 0
   warnings (README not regenerated).
