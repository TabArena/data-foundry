# nyc_taxi_trip_duration

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
   * **Sources:** the definition [dataset.py](dataset.py) (`temporal`, `splits_comment`, `task_summary.split`), the record [nyc_taxi_trip_duration](../../../../curation/records/nyc_taxi_trip_duration.md); the statistics come from `dataset windows nyc_taxi_trip_duration_1m` (2026-11-10).
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
