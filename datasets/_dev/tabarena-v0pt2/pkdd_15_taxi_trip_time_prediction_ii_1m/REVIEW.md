# pkdd_15_taxi_trip_time_prediction_ii

**Outcome:** added as `pkdd_15_taxi_trip_time_prediction_ii_1m`. Verdict ship on 2026-10-26; the rule on test windows
was rewritten on 2026-11-10, so the three test months (April, May and June 2014) are put to the curator again. The AI
proposes keeping June and April and testing February instead of May, so that one window falls in winter.

**Main points:** First the horizon sign-off (H), from the horizon audit of 2026-11-10: calendar months, 30 days or
weeks as for nyc? Issue 1 waits on it: April, May and June 2014 (as now), or February, April and June (your pick)?

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
   * **Sources:** the definition [dataset.py](dataset.py) (`temporal`, `splits_comment`, `task_summary.split`), the record [pkdd_15_taxi_trip_time_prediction_ii](../../../../curation/records/pkdd_15_taxi_trip_time_prediction_ii.md); the statistics come from `dataset windows pkdd_15_taxi_trip_time_prediction_ii_1m` and monthly counts of the frame (2026-11-10); the festival's dates from its listing ([last.fm](https://www.last.fm/sv/festival/3848973+Queima+das+Fitas+Porto+2014)).
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
