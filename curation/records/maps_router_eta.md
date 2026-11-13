---
unique_name: maps_router_eta
name: Maps Routing
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
priority: 3
decision_markers:
- Anonymized
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabRed
- tabular-dl-more-data
original_source: Kaggle
year: '2024'
domain: industry & manufacturing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/pcovkrd84mejm/maps-routing
- https://github.com/yandex-research/tabred/tree/main/preprocessing#maps-router-eta
notebook_path: datasets/beyond_iid/temporal/maps_router_eta/maps_router_eta_1m.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/maps_router_eta_1m/dataset.py
source_row: 714
type_adapter_id: curation-record-v1
---

## Comments

Was downsampled/filtered by TabRed via preprocessing.

TabRed, 1 week horizon.

Not much more, need to follow preprocessing from TabRed most likely.

CC (2026-10-19, Lennart): TabReD's quantile transform of the numeric features may be fit on all rows (undocumented); kept, with a `Potential leak, kept on purpose` note in the definition: a scaling over all rows is no strong leak and often happens in reality. It is a reason for `No` only when a strong leak is suspected or the data can be rebuilt.

CC (2026-10-21, Lennart): check SPLIT-9 on the weekly test windows and add a gap where train labels arrive late, as for nyc_taxi_trip_duration and pkdd_15 (cross-dataset review, marked ok).

**Assessment (AI, 2026-10-21):** SPLIT-9 late labels in maps_router_eta_1m (request time + exp(target) s/km x track_length, read as metres: its minimum is 1,000.0, and the median speed is 27 km/h; drives up to 16.6 h): without a gap 656, 654 and 578 train routes per weekly window (newest first; starts 2023-12-04, 11-27, 11-20) end after the window start; with a gap of one day (TemporalSplits(..., gap=1)) none. The gap removes 292k, 313k and 299k of the 11.2M, 8.8M and 6.4M earlier routes (2.6 to 4.7%); each train side is still a random 1M. Gap set in dataset.py, counts in splits_comment.

**Assessment (AI, 2026-10-21):** Unit and errors of track_length (follow-up to the SPLIT-9 gap). TabReD's paper (App. B.2) defines only the target, log seconds per km; neither the paper nor its preprocessing README/code states the unit of track_length. It is metres: min 1,000.0, median 5,168, max 1,103,597, no value a multiple of 10; read as metres the drive takes 0.03 to 16.6 h (median 0.19 h), read as km the median is 194 h. Implied speed (3600 / exp(target)) is 0.97 to 160 km/h, median 27, 99.9% 90. Implausible rows: 31 of 13.64M (0.0002%): 12 above 150 km/h, 5 below 2 km/h, 14 longer than 12 h (944 longer than 6 h, median 477 km at 67 km/h, plausible long drives); 26, 19, 12 in the train sides and 5, 7, 7 in the test windows (newest first). None of the 656, 654, 578 late routes is implausible (late drives median 0.35 h, 13 km, requested median 9 min before the window start, at most 11.4 h), so the one-day gap stands; no CLEAN-11 fix proposed.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source rmse — RMSE (TabReD's regression metric) (Rubachev et al., TabReD, ICLR 2025 (https://arxiv.org/abs/2406.19380)).

**Assessment (AI, 2026-11-10):** priority for the review of the test windows (PR #78), which this record never had. Priority 3: gap 0, use case 0 (TabReD names the task, not who acts on it), source + (the TabReD paper), shape +, risk 0 (the oldest window below the floor is repairable, issue 1).

CC (2026-11-11, Lennart): REVIEW issue 1 (which three test weeks), "As implemented (A), in reply to the consistency check.": the three newest weeks, 4-10 December, 27 November to 3 December and 20-26 November 2023, stay, in place of the AI's overlapping weeks; this answers the consistency check of 2026-11-10, as SPLIT-14 as amended on 2026-11-11 admits the oldest week, which trains on 44.8% of all routes (one window under half, two above; counted on all rows). The windows walk back from the newest because the 40 days leave no other choice: a fourth whole week would train on about a quarter.

CC (2026-11-11, Lennart): the declared horizon (7 days, a one-day gap, the newest three weeks) is checked, as a week is TabReD's own validation and test length and holds every weekday once; TabReD states no refit cadence, so "a model refit every week" is no longer claimed.

**Assessment (AI, 2026-11-11):** applied in dataset.py, text only: `temporal` unchanged (`window=7, unit="days", n_windows=3, gap=1`); counted on all 13,639,272 routes, test 2,444,459, 2,385,262 and 2,401,353 before the 500k sampling (500,000 tested each), train 10,902,438, 8,496,883 and 6,108,934 (79.9%, 62.3%, 44.8%); a fourth week, 13-19 November, would train on 3,704,756 (27.2%). "As for a model refit every week" is gone from `task_summary.split`, and `splits_comment` reads "at a window's start" for "at a weekly refit"; both now name the three weeks (the two older ones TabReD's own validation and test weeks), the oldest under half with its share, why the windows walk back, and that TabReD states no refit cadence. The definition's split step gives these windows and train sides; `dataset check` was not run to the end (a full check of the 13.6M routes was stopped after 52 minutes, on the coordinator's instruction) and is due with the next build (README not regenerated).

## Review

**Outcome:** added as `maps_router_eta_1m`. On 2026-11-11 you kept the three newest weeks, 20 November to 10
December 2023, with the one-day gap (issue 1, in reply to the consistency check, and the horizon, A), which the
amended floor admits with the oldest week training on 44.8% of the routes.

**Main points:** Settled on 2026-11-11: the three newest weeks stay (issue 1, A, closing the consistency check),
and the declared horizon of one week with a one-day gap is checked, a week being TabReD's own validation and test
length.

**Horizon:**

* **Verdict:** keep the 7-day windows (medium confidence): a week is TabReD's own validation and test length, a week
  holds every weekday once, and travel times are lower on weekends.
* **Length:** TabReD (Rubachev et al., ICLR 2025, https://arxiv.org/abs/2406.19380; preprocessing at
  https://github.com/yandex-research/tabred/tree/main/preprocessing): train 1-20 November, validation 20-27 November,
  test 27 November to 4 December 2023 (its own split trains on 47% of the rows and leaves 4-10 December unused). "As
  for a model refit every week" is our wording; no source names the router's refit cadence. If it is daily, one-day
  windows become the right horizon.
* **Gap:** one day; the longest route takes 16.6 hours, so 17 hours would also do.
* **Time frame:** 1 November to 10 December 2023, no missing day; Monday 6 November, a Russian public holiday, runs
  like a Sunday and lies in every train side.
* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | A | One week, one-day gap (implemented) | 7-day windows; which weeks is issue 1 | 3 windows of 2.39M to 2.44M routes (500,000 tested each) | TabReD's own validation and test length; every weekday once | only two whole weeks without overlap keep half the routes for training (issue 1); no source names the refit cadence |
  | B | One day, a 17-hour gap | daily windows: 18 candidates | 18 candidates of 292,375 to 386,308 routes | issue 1's floor problem disappears; the right horizon if the router refits daily | each window tests one weekday, and weekends run lower |
  | C | Six days | issue 1's option C: 23-28 November, 29 November-4 December and 5-10 December | 3 windows of 2.05M to 2.12M routes (500,000 tested each) | every train side above half; no overlap | each window misses one weekday |
  | D | Two weeks | 14-day windows: 1 candidate | 1 candidate of 4.83M routes (500,000 tested) | more routes per window | fewer than three windows |

* **Recommendation:** A: the length of the source's own validation and test periods, holding every weekday once; the
  floor is issue 1's question, and a daily refit, which one-day windows would fit, is named by no source.
  **Decision:** A, B, C or D?

**Lennart (2026-11-11, ok):** As implemented (A).

**Resolved (2026-11-11, Lennart):** A, 7-day windows with a one-day gap, kept: a week is TabReD's own validation and
test length, holds every weekday once, and travel times are lower on weekends. "As for a model refit every week" is
gone from `task_summary.split` and from `splits_comment` ("at a weekly refit" now reads "at a window's start"), which
now say that TabReD states no refit cadence, so the length says how long one fitted model serves; the one-day gap
covers the longest drive, 16.6 hours. `temporal` is unchanged. The record has the horizon CC line. `dataset check`
was not run to the end for this text-only change (a full check of the 13.6M routes was stopped after 52 minutes);
the windows were counted with the definition's own split step (README not regenerated).

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
   * **Sources:** the definition [dataset.py](../../datasets/_dev/tabarena-v0pt2/maps_router_eta_1m/dataset.py) (`temporal`, `splits_comment`, `task_summary.split`), the record [maps_router_eta](maps_router_eta.md); the statistics come from `dataset windows maps_router_eta_1m` (2026-11-10).
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

   **Lennart (2026-11-10, ok):** As implemented (A).

   **Consistency check (AI, 2026-11-10):** Keep the three newest weeks, whose oldest train side holds 44.8% of the
   routes, when the floor is a Must and its 40% allowance needs test entities that recur, which anonymous routes do not?

   * **Problem:**
     - A tests 20-26 November on 44.8% of the 13,639,272 routes; the floor is a Must[^mc-14], and the amendment of
       2026-11-08 admits one older window at 40% or more only when most test entities recur and folds by entity would
       test unseen ones (wisconsin: 97.6% to 98.8% of each test year's members known), while the routes here are
       anonymous.
     - No higher rule calls for A: the newest week is in B and C too, and the weekly length (a Should) stays in
       B[^mc-15][^mc-12].
     - Every earlier floor breach was fixed or amended (california_house_prices_2020, pricing_game_2016_french_fleet,
       wisconsin), and today cooking_time_1m, from the same TabReD family at the same length, kept its windows because
       they are "the only weekly windows above the floor".
   * **Background:**
     - A fact that could set maps apart: a 40-day release in which three whole weeks without overlap cannot all keep
       half the routes; A's two older weeks are TabReD's own validation and test weeks, and TabReD's own split trains on
       47.0%[^mc-19].
     - Counted on the rows the container ships (the newest week capped at 500,000), the oldest side holds 52.2%; the
       floor is counted on all rows, as for wisconsin (40.6%) and ashrae (49.5%).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Amend the floor | admit one older window at 40% or more also when a release is too short for three whole weeks above the floor, whatever the entities | whole weeks without overlap; TabReD's own weeks | widens a Must two days after it was narrowed to recurring entities; applies to every short release |
     | b | B, three overlapping weeks | 23-29 November, 29 November-5 December, 4-10 December (51.8%, 67.0%, 79.9%) | keeps the floor and whole weeks; decides maps like cooking_time_1m | 3 of 21 test days tested twice |
     | c | C, three six-day windows | train sides 51.8%, 67.0%, 82.1% | keeps the floor, no overlap | each window misses one weekday |
     | d | Count the floor on the shipped rows | A passes at 52.2% | the floor would depend on the test budget, not the data, for every `_1m` version |

   * **Recommendation:** b: it keeps the Must and the weekly length, and decides maps like cooking_time_1m today;
     choose a only if whole weeks without overlap should outrank the floor for every short release. **Decision:** a, b,
     c or d?

   [^mc-14]: **SPLIT-14** (Must; amended 2026-11-08, Lennart, on wisconsin_local_government_property_insurance_fund):
     at least 3 windows, no train side below 50% of the data; one older window at 40% or more only "when most test
     entities recur ... and folds by entity would test unseen ones".
   [^mc-15]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10): "Every choice stays
     above SPLIT-14's floor."
   [^mc-12]: **SPLIT-12** (Should): the horizon comes from the source or the refit cadence.
   [^mc-19]: **SPLIT-19** (Should): follow the source's split; it ranks below SPLIT-14, a Must.

   **Lennart (2026-11-11, ok):** As implemented (A), in reply to the consistency check.

   **Resolved (2026-11-11, Lennart):** A, as implemented: the three newest weeks stay, 4-10 December, 27 November to
   3 December and 20-26 November 2023 (the last two TabReD's own test and validation weeks). This closes the
   consistency check of 2026-11-10: SPLIT-14 as amended on 2026-11-11 admits the oldest week, since the newest window
   and at least one other train on half the rows or more and a further window may train on down to 30%, with no
   condition on recurring entities; counted on all 13,639,272 routes, the train sides hold 10,902,438, 8,496,883 and
   6,108,934 (79.9%, 62.3% and 44.8%), one window under half against two above. The windows walk back from the newest
   because the 40 days leave no other choice: a fourth whole week, 13-19 November, would train on 27.2%. `temporal` is
   unchanged; `task_summary.split` and `splits_comment` name the three weeks, their 2,444,459, 2,385,262 and 2,401,353
   routes before the 500k sampling, the train sides, the oldest under half with its share and why, and what the 40
   days cannot test. The record has the decision and the horizon CC lines. `dataset check` was not run to the end
   (stopped after 52 minutes on the 13.6M routes; the change is text only); the definition's split step gives the
   same three windows and train sides (README not regenerated).

## Reference

TabRed
