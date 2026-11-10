# nyc_taxi_trip_duration

**Outcome:** added as `nyc_taxi_trip_duration_1m`. Verdict ship on 2026-10-22; the rule on test windows was rewritten
on 2026-11-10, so the three test weeks (the last three of June 2016) are put to the curator again. The AI proposes
keeping the newest week and testing the Memorial Day week and a week in April instead of the two June weeks before it.

**Main points:** Which weeks to test on: the last three weeks of June (as now), or the newest June week, the Memorial
Day week and a week in April?

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
