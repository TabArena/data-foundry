# maps_router_eta

**Outcome:** added as `maps_router_eta_1m`. In the working copy since the migration; the rule on test windows was
rewritten on 2026-11-10. The data cover 40 days, so no window can test another year, season or holiday period, and
the oldest of today's three test weeks trains on 44.8% of the routes, below the half every train side must keep. The
AI proposes three whole weeks that overlap by one or two days, which keep every train side above half.

**Main points:** Keep the three newest weeks (the oldest below the floor), or test three overlapping weeks or three
six-day windows that keep it?

**Issues for Lennart:**

1. **Which three test windows, when the 40 days allow only two whole weeks above the floor?**

   * **Problem:**
     - The routes run from 1 November to 10 December 2023, so every possible test window lies in late November or early December, and no choice can test another year, season or holiday period.
     - The oldest of the three test weeks (20-26 November) trains on the routes before 19 November, 44.8% of all routes, below the half every train side must keep[^mr-floor], and only two whole weeks that do not overlap clear that line.
     - Three whole weeks from 23 November, 29 November and 4 December keep every train side above half (51.8% to 79.9%) but share one and two days, and three six-day windows keep it without overlap but each miss one weekday.
   * **Background:**
     - Half the routes were requested before 21 November 07:34; with the one-day gap, a window that starts before 23 November trains on less than half.
     - Counted on the rows the container keeps (the newest week sampled down to 500k routes), the oldest week's train side is 52.2%; the window statistics count every route, as this issue does.
     - The target (log seconds per km) rises slowly over the 40 days, from a daily mean of 4.85 to 4.86 on the first weekdays of November to 4.91 to 4.93 on the weekdays of December, and is lowest on Sundays; every whole week holds each weekday once.
     - What none of the options tests: the year-end holidays, summer roads, a second year, or a change of the service; the notes should say so.
   * **Effect on the task:** Any choice scores a weekly refit in three late-autumn weeks, so the score covers a router's model in the weeks just after its training data and says nothing about other times of the year.
   * **Data statistics:** window statistics of 2026-11-10 and daily counts of the frame.
     - Today's weeks, newest first: 2,444,459, 2,385,262 and 2,401,353 routes (500k of each tested), train sides 79.9%, 62.3% and 44.8%; mean target 4.895, 4.890 and 4.877 against 4.856, 4.847 and 4.838 on the train sides.
     - The features drift little in any week (largest population stability index 0.054, `num_100` to `num_102` in the oldest week), and at most 0.01% of a week's routes hold a category its train side never shows.
   * **Consistency:** The rule allows a third window that trains on at least 40% only when most test entities recur, as the members of an insurance fund do; the routes are anonymous, so it does not apply as written[^mr-amend]. Overlapping windows were declared before (ghana, now retired: 3-day windows moving by 2 days). The weekly length and the one-day gap come from the use case and from TabReD's one-week horizon[^mr-length].
   * **Sources:** the definition [dataset.py](dataset.py) (`temporal`, `splits_comment`, `task_summary.split`), the record [maps_router_eta](../../../../curation/records/maps_router_eta.md); the statistics come from `dataset windows maps_router_eta_1m` (2026-11-10).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | The three newest weeks (implemented) | test 20-26 November, 27 November-3 December and 4-10 December, train sides 44.8%, 62.3% and 79.9% | whole weeks without overlap; the source's weekly horizon | the oldest train side holds less than half the routes |
     | B | Three overlapping weeks | test 23-29 November, 29 November-5 December and 4-10 December (2,402,332, 2,390,042 and 2,444,459 routes, 500k of each tested), train sides 51.8%, 67.0% and 79.9% | every train side above half; whole weeks with every weekday; the weekly horizon stays | 29 November and 4-5 December are tested twice (3 of 21 test days); the windows are even closer copies of each other |
     | C | Three six-day windows | test 23-28 November, 29 November-4 December and 5-10 December, train sides 51.8%, 67.0% and 82.1% | every train side above half; no overlap | each window misses one weekday (Wednesday, Tuesday, Monday); six days where the refit is weekly |

   * **Recommendation:** B: it keeps the floor and the weekly horizon, and the shared days cost little where every possible window is a late-autumn week like the others[^mr-newest]. **Decision:** A, B or C?

   **Notes for the AI:** on B, `temporal = Temporal(on="timestamp", splits=TemporalSplits(window=7, unit="days", gap=1,
   cutoffs=("2023-11-23", "2023-11-29", "2023-12-04")))` (checked 2026-11-10 on the timestamps of all 13,639,272
   routes: train 10,902,438, 9,136,118 and 7,066,897; test 2,444,459, 2,390,042 and 2,402,332 before sampling). On C,
   `TemporalSplits(window=6, unit="days", gap=1, cutoffs=("2023-11-23", "2023-11-29", "2023-12-05"))` (train
   11,194,813, 9,136,118 and 7,066,897; test 2,117,217, 2,051,212 and 2,063,680), and the horizon becomes 6 days. Then
   rewrite `splits_comment` (the windows, the overlap or the six days, why: SPLIT-14's floor; the 40 days and what they
   cannot test, SPLIT-15), `task_summary.split` ("one week (20 November to 10 December 2023)"); recount the late routes
   per window for the gap (the 656, 654 and 578 and the 292k, 313k and 299k removed routes are for today's weeks;
   SPLIT-9, SPLIT-10). On A, the floor needs an amendment of SPLIT-14 (a Must has no exceptions). Then `dataset check`,
   a CHANGELOG entry and a CC line in the record.

   [^mr-floor]: **SPLIT-14** (Must; amended 2026-11-08, Lennart): a temporal task has at least 3 windows, and no
     window's train side holds less than 50% of the data; a task that cannot meet it ships in the closest regime that
     keeps the rows (**SPLIT-8**).
   [^mr-amend]: **SPLIT-14**, amendment of 2026-11-08 (Lennart, on wisconsin_local_government_property_insurance_fund):
     a release with two windows above the floor may add one older window that trains on at least 40% of the rows, when
     most test entities recur (the actor re-rates entities it knows) and folds by entity would test unseen ones.
   [^mr-length]: **SPLIT-12** (Should): the window length and the gap come from the use case, here a model refit every
     week; **SPLIT-10** (Should): the one-day gap covers drives still under way at a refit.
   [^mr-newest]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): the newest window is always a test window; the others are chosen per dataset from the use case, with
     statistics of the data as evidence and never a model's score; walking back from the newest needs its reason, such
     as a history too short for others.
