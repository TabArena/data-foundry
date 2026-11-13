---
unique_name: pkdd_15_taxi_trip_time_prediction_ii
name: 'ECML/PKDD 15: Taxi Trip Time Prediction (II)'
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- Review Prio 1 (Atlas)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Varying Delay'
- 'Entities: Recur'
original_source: Kaggle
year: '2015'
domain: industry & manufacturing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/c/pkdd-15-taxi-trip-time-prediction-ii
- https://www.kaggle.com/c/pkdd-15-predict-taxi-service-trajectory-i
- https://archive.ics.uci.edu/dataset/339/taxi+service+trajectory+prediction+challenge+ecml+pkdd+2015
- https://arxiv.org/abs/1508.00021
v2_path: datasets/_dev/tabarena-v0pt2/pkdd_15_taxi_trip_time_prediction_ii_1m/dataset.py
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

**Assessment (AI, 2026-10-07):** Added as `pkdd_15_taxi_trip_time_prediction_ii_1m`: travel time at trip start from origin, destination (last GPS point), Porto local start time, call type, stand and taxi. Log1p target, monthly test windows Apr-Jun 2014, 1,655,983 trips after dropping non-trips, GPS errors and meter misuse. The taxi stays a feature: 99.93-100% of each test month's trips are by taxis seen before. ORIGIN_CALL is dropped: it adds nothing once the destination is known. Open: the challenge page says drivers "do not indicate the final destination of the ride", so the destination framing is ours. Its 2026-09-21 reason, a weak pickup-only signal, no longer holds under task_probes.md rule 2. Pickup-only LightGBM reaches R² 0.11-0.15, against 0.48-0.50 with the destination.

**Assessment (AI, 2026-10-20):** priority 2 for the review of the added dataset: gap -, use case -, source +, shape +, risk - (Issue 1: source says drivers do not enter the destination, so that feature may not exist at pickup). A large temporal ETA regression from a documented challenge; without the destination, which may not be known at pickup, the signal is weak.

**Assessment (AI, 2026-10-20):** Re-checked by the full review panel; recommend shipping `pkdd_15_taxi_trip_time_prediction_ii_1m` with this review's changes, the curator has the call. The definition now drops the 90 trips whose end point equals the start point (USE-7, as nyc_taxi_trip_duration) and takes monthly test windows of 30 days from 1 April, 1 May and 1 June 2014 with a one-day gap (SPLIT-9: without it 48, 36 and 8 train trips per window end after the window start). LightGBM R² 0.51-0.54 with the destination, 0.12-0.15 without, linear 0.04. Open (the Review): the reason for the destination framing, since the CC's weak-signal reason no longer holds under TP-2 (issue 1), and the short-trip cut at 60, 45 or 30 s (issue 2). Two counts of the 2026-09-21 investigation do not reproduce with the definition's Greater Porto box: 1,084 trips start outside it (not 1,459) and 1,672,375 rows remain after those filters (not 1,672,071); the decision table in the README is authoritative. Priority 2: gap -, use case -, source +, shape +, risk - (use case: the destination-at-pickup ETA is our framing, the source names no actor who knows the destination at pickup; risk: issue 1, the destination is recorded after the trip).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source rmse — RMSLE of the travel time, the competition's evaluation metric, as RMSE on the log1p_travel_time target (Kaggle evaluation page).

**Assessment (AI, 2026-10-21):** metric now `Metric.source("rmsle", target_transform="log1p")` instead of rmse on the log1p target: the competition's RMSLE on the travel time in seconds, computed after the inverse of the shipped log1p (MET-3); the score is the same number as before. Needs a rebuild to reach the container.

CC (2026-10-21, Lennart): the datetime encoding of v0.2 (cross-dataset item from the nyc_taxi_trip_duration review): nothing to change while the v0.2 runs encode datetimes with the hour; the definition adds no hour column (CLEAN-2).

CC (2026-10-26, Lennart): the declared metric is checked as declared.

CC (2026-10-26, Lennart): issue 1: (a), "which is also more correct nowadays, where one would add it in an app. I think it is fine to use the destination as well for now and work on that": an ETA once the passenger names the destination, `fit="approximate"`, as nyc_taxi_trip_duration.

CC (2026-10-26, Lennart): the record's domain takes the definition's value (industry & manufacturing).

CC (2026-10-26, Lennart): issue 2: drop the trips that end within 100 m of their start, with a time cut at 30 s, and reopen nyc_taxi_trip_duration_1m for the same radius (option (c): "we just forgot to check for this for nyc and for these cases it also does not matter much to do a taxi trip right?").

**Assessment (AI, 2026-10-26):** issue 2 applied: `MIN_STRAIGHT_LINE_KM = 0.1` replaces the identical-end-point rule and `MIN_TRAVEL_TIME_S` falls from 60 to 30 s; 1,636,276 trips after the filters (1,655,893 before). The trips within 100 m are no short rides (median 555 s, 57% over 5 min, 17% of the target's squared spread): in the app framing nobody books them. dataset check: 0 errors, 0 warnings. No open issue left.

CC (2026-10-26, Lennart): verdict ship.

**Assessment (AI, 2026-10-26):** what the encoding is worth here, from the review panel of 2026-10-20 (before the 100 m cut): LightGBM (300 trees, learning rate 0.1, 63 leaves, one fit per split) scored R^2 0.503 / 0.482 / 0.498 on the June / May / April windows with the local hour, weekday and day of year, and 0.483 / 0.452 / 0.462 with AutoGluon's date parts.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `chicago_taxi_trip_duration` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-11, Lennart): Review issue 1, B ("Agree. Option B: February, April and June."): the test windows are the calendar months February, April and June 2014 (horizon, B), in place of April, May and June, so one window falls in the winter.

CC (2026-11-11, Lennart): the declared horizon (calendar months, a one-day gap, windows starting 2014-06-01, 2014-04-01 and 2014-02-01) is checked, as no source gives a refit cadence and the only horizon the source shows is one model trained on the year and used for months without a refit, so calendar months are the longest windows that leave a choice of seasons (Review horizon, B: "Option B: Calendar months.").

**Assessment (AI, 2026-11-11):** applied issue 1 (B) and the horizon (B): `temporal` declares calendar months from 2014-06-01, 2014-04-01 and 2014-02-01 with a one-day gap; test 146,714, 130,112 and 122,831 trips, train 1,484,039, 1,200,383 and 943,912 (90.7%, 73.4% and 57.7% of the 1,636,276 trips); without the gap 47, 7 and 21 training trips would end after the window start, with it none; 100%, 99.93% and 100% of the June, April and February trips are by taxis seen before. The R^2 figures of the notes stay those of the April-June windows, dated as such. `dataset check`: 0 errors, 0 warnings.

## Review

**Outcome:** added as `pkdd_15_taxi_trip_time_prediction_ii_1m`. Verdict ship on 2026-10-26; on 2026-11-11 you chose
calendar months (H, B) and February, April and June 2014 as the test months (issue 1, B); both are applied and nothing
is left open.

**Main points:** Settled on 2026-11-11: the test windows are the calendar months February, April and June 2014, as one
model trained on the trips so far serves for months, and one window falls in the winter.

**Horizon:**

* **Verdict:** change the 30-day windows to calendar months (medium confidence): no source gives a refit cadence, the
  definition's reason for a month misreads the challenge, and the only horizon the source shows is months long and
  without a refit.
* **Length:** the splits comment says "The monthly length follows the source: the challenge tested on 320 trips 1.5
  to 6 months after its training year". The challenge asked for five snapshots (14 August to 21 December 2014;
  BlueTaxi, https://arxiv.org/abs/1509.05257) of one model trained on the year (1 July 2013 to 30 June 2014;
  https://arxiv.org/abs/1508.00021), used 1.5 to 6 months later without a refit: that defines no month, and it speaks
  for the longer of the lengths below. The windows were calendar months at first and became 30 days when the one-day
  gap was added; the 30-day unit ends the May window on 30 May and makes a February window run to 2 March. Calendar
  months with a one-day gap now work. nyc_taxi_trip_duration_1m predicts the same thing, a taxi trip's duration when
  it starts, on one-week windows, so the two taxi tasks assume different refit cadences; no source of either dataset
  states one, and nyc's week rests on the weekdays and on how often an ETA service usually refits[^h-split12]. A
  month-long window scores a model that serves a month, a week one that serves a week, as on nyc.
* **Gap:** one day: a trip lasts at most 3 hours (without the gap 48, 36 and 8 training trips would end after the
  window starts).
* **Time frame:** the challenge's year; months from January 2014 keep half the trips for training; 60 days would give
  exactly three windows that tile the half-year, with no choice left. Drift between months is small (largest PSI 0.023
  to 0.025), so the length changes how long one model serves more than what the windows hold, and the scores differ
  more in how many trips each window holds than in their level. Your pick of issue 1 (February, April and June) holds
  under a month and is chosen again under a week.
* **Statistics:** calendar months with a one-day gap, from the definition's frame:

  | Window | Trips tested | Train side | Train share | Mean log seconds, test and train |
  |---|---|---|---|---|
  | June 2014 | 146,714 | 1,484,039 | 90.7% | 6.402, 6.404 |
  | April 2014 | 130,112 | 1,200,383 | 73.4% | 6.390, 6.399 |
  | February 2014 | 122,831 | 943,912 | 57.7% | 6.419, 6.395 |

* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | A | 30 days (implemented) | issue 1's pick as 30-day windows from 1 February, 1 April and 1 June | 3 windows of 130,112 to 146,714 trips | no change of unit | the February window runs to 2 March; a length no source gives |
  | B | Calendar months | February, April and June 2014 (57.7%, 73.4%, 90.7%); 6 candidates, January to June | 3 windows of 122,831 to 146,714 trips | your pick exactly; the longer length the source's months-long use speaks for | a different length from nyc for the same use case |
  | C | One week, as nyc | three weeks chosen again under issue 1; about 25 candidates | 25 candidates of 27,072 to 39,547 trips | one length for the taxi tasks | no source either; a week where the source used one model for months |

* **Recommendation:** B: it is your pick of issue 1 as calendar months, and where the source shows any horizon it is
  months long; nyc has no such source, so a week stays its length. **Decision:** A, B or C?

**Notes for the AI:** on B, `temporal = Temporal(on="start_time", splits=TemporalSplits(window=1, unit="months",
cutoffs=("2014-06-01", "2014-04-01", "2014-02-01"), gap=1, gap_unit="days"))`: test 146,714, 130,112 and 122,831
trips, train 1,484,039, 1,200,383 and 943,912 (90.7%, 73.4%, 57.7%). Then resolve issue 1 with B, rewrite
`task_summary.split` and `splits_comment` (the windows, the reason from the Horizon block: one model trained on the
year and used for months; calendar months as the longest cadence that leaves a choice of seasons), a CC line in the
record with the CC line that the declared horizon is checked, a dated CHANGELOG entry, `dataset check`. On C, propose
three weeks in issue 1 again (`dataset windows ... --window 7 --unit days --gap 1 --gap-unit days`).

[^h-split12]: **SPLIT-12** (Should): "The horizon is a human judgment from the source: how far ahead the actor
  predicts ..., the competition's own test window, the refit cadence. Choose the test windows to match it and write
  the reasoning down."

**Lennart (2026-11-11, change):** Option B: Calendar months.

**Resolved (2026-11-11, Lennart):** B. `temporal` declares calendar months starting 2014-06-01, 2014-04-01 and
2014-02-01 with `gap=1, gap_unit="days"`. `task_summary.split` and `splits_comment` give the reason from this block: no
source gives a refit cadence, the challenge used one model trained on its year for months without a refit, and
calendar months are the longest windows that still leave a choice of seasons; the comment names the week of
nyc_taxi_trip_duration_1m and why it differs, and drops "the monthly length follows the source". Without the gap 47, 7
and 21 training trips (June, April, February) would end after the window start, with it none. Test 146,714, 130,112
and 122,831 trips, train 1,484,039, 1,200,383 and 943,912 (90.7%, 73.4%, 57.7% of 1,636,276); the 5,523 trips of 31
May 2014, the newest window's gap day, lie in no split. The record has the horizon CC line. `dataset check`: 0 errors,
0 warnings (README not regenerated).

**Issues for Lennart:**

1. **Test on February, April and June 2014 instead of April, May and June?**

   * **Problem:**
     - The test windows are the 30 days from 1 April, 1 May and 1 June 2014, the three months just before the end of the file, all in spring and early summer.
     - The rule keeps the newest month and prefers windows in other seasons over the months just before it[^pk-newest].
     - The file covers one year (July 2013 to June 2014), and with every train side at half the trips or more the windows can start from January 2014, so no other year can be tested but the winter can.
   * **Background:**
     - Winter trips in Porto are the slowest of the year: the median straight-line speed is 15.6 to 16.0 km/h from October to February, 16.4 in March and April, and 16.7 to 17.6 from May to August (one value per month).
     - The eligible months hold three calendar events: Easter (18-20 April; the two weeks around it have the shortest trips of the first half of 2014, mean log time 6.36 to 6.37 against 6.38 to 6.43), the student festival Queima das Fitas (4-10 May: 40,770 trips that week against about 31,000, and 22% to 27% of weekday trips at night against 7% to 8%) and São João (23-24 June, in the newest window).
     - A January window would train on 50.1% of the trips, at the floor, so February is the winter month proposed.
   * **Effect on the task:** Today the score tests spring and early summer three times; a deployed model also predicts winter trips, when the city is slowest, and no test window holds one.
   * **Data statistics:** 30-day windows from the first of each month, one-day gap (window statistics, 2026-11-10).
     - February: 133,071 trips, train side 57.7%, mean log time 6.407 against 6.400 on the train side, largest drift 0.022 (`origin_stand`).
     - April, May and June (now): 130,112, 149,602 and 146,714 trips, train sides 73.4%, 81.3% and 90.7%, mean log time 6.389, 6.421 and 6.396 against 6.398 to 6.402, largest drift 0.005, 0.018 and 0.011.
     - The features barely drift in any month (largest population stability index 0.023, `start_lat` in January), and the target's mean moves by at most 0.03, so the choice rests on the season.
   * **Consistency:** No dataset of the working copy declares windows chosen this way yet. The other ETA tasks of the collection (nyc_taxi_trip_duration_1m, maps_router_eta_1m) get the same question in their own review files. The 30-day length and the one-day gap stay, as the monthly refit sets them[^pk-length].
   * **Sources:** the definition [dataset.py](../../datasets/_dev/tabarena-v0pt2/pkdd_15_taxi_trip_time_prediction_ii_1m/dataset.py) (`temporal`, `splits_comment`, `task_summary.split`), the record [pkdd_15_taxi_trip_time_prediction_ii](pkdd_15_taxi_trip_time_prediction_ii.md); the statistics come from `dataset windows pkdd_15_taxi_trip_time_prediction_ii_1m` and monthly counts of the frame (2026-11-10); the festival's dates from its listing ([last.fm](https://www.last.fm/sv/festival/3848973+Queima+das+Fitas+Porto+2014)).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | April, May and June (implemented) | test 1-30 April, 1-30 May and 1-30 June (130,112 to 149,602 trips), train sides 73.4% to 90.7% | the most training data; Easter, the student festival and São João each in a window | no winter window; May and June are the two months just before the end |
     | B | February, April and June | test 1 February-2 March, 1-30 April and 1-30 June (133,071, 130,112 and 146,714 trips), train sides 57.7%, 73.4% and 90.7% | one window in each season the file allows; spread evenly over the six eligible months; Easter and São João stay | the festival week leaves the test windows; the February window trains on seven months |

   * **Recommendation:** B: it keeps the newest month and adds the winter, the season a deployed model finds slowest, with every train side above half the trips[^pk-floor]. **Decision:** A or B?

   **Notes for the AI:** on B, `splits=TemporalSplits(window=30, unit="days", gap=1, cutoffs=("2014-02-01",
   "2014-04-01", "2014-06-01"))` (checked 2026-11-10: train 1,484,039, 1,200,383 and 943,912 trips; test 146,714,
   130,112 and 133,071). Then rewrite `splits_comment` (the windows, why each, the numbers; its sentence "the April to
   June test season has no earlier copy in train" changes, as the February window's train side holds December and
   January), `task_summary.split` ("April, May and June 2014 are the test periods"); recount the training trips that
   end after each window start for the gap (the 48, 36 and 8 of the splits comment are for June, May and April);
   the splits comment's 131,648 to 151,406 trips per window are stale since the 100 m cut of 2026-10-26. Then `dataset
   check`, a CHANGELOG entry and a CC line in the record.

   [^pk-newest]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): the newest window is always a test window; the others are chosen per dataset from the use case (other
     years, seasons, holidays, events, a change of rules or of the data collection), with statistics of the data as
     evidence and never a model's score; windows in other years, then other seasons, then other months, weeks or days
     are preferred over the windows just before the newest, and walking back from the newest needs its reason too.
   [^pk-length]: **SPLIT-12** (Should): the window length and the gap come from the use case, here a model refit every
     month; **SPLIT-10** (Should): the one-day gap covers trips still under way at a refit.
   [^pk-floor]: **SPLIT-14** (Must): at least 3 windows, and no train side below 50% of the rows.

   **Lennart (2026-11-10, change):** Option B: February, April and June.

   **Answer (AI, 2026-11-10):**
   - The horizon audit found that the 30-day length has no source behind it (the Horizon block above), so the horizon
     sign-off (H) asks about the length first.
   - Your months stand under its options A (30 days, the February window running to 2 March) and B (calendar months);
     under C (one week, as nyc_taxi_trip_duration_1m) the windows are proposed again. This issue waits on the horizon
     sign-off (H).

   **Lennart (2026-11-11, change):** Agree. Option B: February, April and June.

   **Resolved (2026-11-11, Lennart):** B, as calendar months (H, B): the test windows are June, April and February 2014.
   `splits_comment` names them and why each (June the newest, with São João; April with Easter; February in the
   winter, when the trips are slowest), replaces "the April to June test season has no earlier copy in train" (the
   February window's train side holds the winter months before it), recounts the trips that end after a window start
   without the gap (47, 7 and 21) and gives 146,714, 130,112 and 122,831 trips per window in place of the stale 131,648
   to 151,406. The decision table of recurring taxis follows the test months (100%, 99.93% and 100% of the February,
   April and June trips by taxis seen before), and the notes' R^2 figures are dated as measured on the April-June
   windows. The record has the decision CC line. `dataset check`: 0 errors, 0 warnings.
