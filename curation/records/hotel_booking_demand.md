---
unique_name: hotel_booking_demand
name: Hotel booking demand
checked_by:
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
priority: 3
tags:
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Varying Delay'
- 'Features: Read Later'
collections:
- New (BeyondArena)
original_source: Other
year: '2018'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.sciencedirect.com/science/article/pii/S2352340918315191#s0005
notebook_path: datasets/beyond_iid/temporal/hotel_booking_demand/hotel_booking_demand.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/hotel_booking_demand/dataset.py
source_row: 732
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Split leak fixed: training rows with a future arrival were all cancelled.** The split kept "bookings that have arrival dates in the future, but were already canceled at the given prediction point" in training. At a prediction point, the only known future bookings are the cancelled ones, so these rows taught "arrival in the test window = cancelled": on the newest split 867 such rows (1.4% of training), 100% cancelled, against 12.5% cancelled in the test set (leak audit 2026-09-24; independent probe "Why we lose on hotel_booking_demand", 2026-08-20, gs://priorlabs-html-reports/hotel_booking_demand_probe_20260820/report.html, which shows every model over-predicting cancellations and in-context models hurt most). Fix: training uses only bookings arriving before the prediction point. Also dropped as recorded after the prediction point (Antonio et al. 2019, Data in Brief 22, Table 1): BookingChanges ("until the moment of check-in or cancellation"), AssignedRoomType (set by hotel operations) and RequiredCarParkingSpaces (> 0 in 6,470 bookings, none cancelled). Caveat from the data paper: every variable is a snapshot of "the day prior to each booking's arrival", later than our prediction point (up to three months before arrival). Result on the three newest splits: LightGBM AUC 0.81-0.83, log loss 0.32-0.36 (was about 1.7), mean prediction 0.20-0.24 vs true 0.125-0.14. The migrated split also crashed (outcome columns dropped before use); they are now dropped after splitting.

Data from two hotels - can likely be concatenated.

Notes from the paper: 
"data point time for each observation was defined as the day prior to each booking׳s arrival"

"Data was extracted via TSQL queries executed directly in the hotels' PMS database"

The authors even thought about leakage: "One of the most important properties in data for prediction models is not to promote leakage of future information [3]. In order to prevent this from happening, the timestamp of the target variable must occur after the input variables' timestamp. Thus, instead of directly extracting variables from the bookings database table, when available, the variables' values were extracted from the bookings change log, with a timestamp relative to the day prior to arrival date (for all the bookings created before their arrival date)"

"A word of caution is due for those not so familiar with hotel operations. In hotel industry it is quite common for customers to change their booking׳s attributes, like the number of persons, staying duration, or room type preferences, either at the time of their check-in or during their stay. It is also common for hotels not to know the correct nationality of the customer until the moment of check-in. Therefore, even though the capture of data took considered a timespan prior to arrival date, it is understandable that the distribution of some variables differ between non canceled and canceled bookings. Consequently, the use of these datasets may require this difference in distribution to be taken into account."
--> Might need to drop some features

The data would allow to predict no shows as a second target

The distributions are suspiciously clean, but the data source seems valid.

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: IsRepeatedGuest.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — The data paper publishes the data without a prediction task or metric; the authors' earlier cancellation-prediction papers used other (non-public) data and reported several metrics (accuracy, precision, AUC), none set as the task's metric.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 1 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `DepositType` (the README lists their levels); left unordered: `ArrivalDateMonth` (a partial order); `Meal` (a level outside the scale is a state of its own).

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 1 calendar or compass cycles ordered; 1 columns with a state outside the scale ordered, the state placed by the rule; Meal's Undefined is SC (the paper), the meal plan ordered; the arrival month ordered.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (1 is the event).

**Assessment (AI, 2026-11-10):** priority for the review of the test windows and horizons, which this record never had. Priority 3: gap 0, use case 0, source + (the data article of Antonio et al. 2019), shape +, risk 0 (the open issue is the choice of prediction dates).

CC (2026-11-11, Lennart): Review issue 1, reply (a) to the answer of 2026-11-11 ("Reply (a): All ten dates"; he had asked "Why can we not extend it or roll back from the newest data to include 1 Jun in option (A) as well?"): the test uses the ten prediction dates 1 September 2016 to 1 June 2017, today's nine and 1 June 2017, the newest date whose three months of arrivals the data holds; SPLIT-14 as amended on 2026-11-11 admits the two oldest, signed off here: 1 October and 1 September 2016 train on 48.3% and 44.0% of the bookings (two windows under half, eight at or above it).

CC (2026-11-11, Lennart): the declared horizon (three months of arrivals, no gap, windows starting on the first of each month from 2017-06-01 back to 2016-09-01) is checked, as the source's system scores every open booking and sets no length, and three months hold 38% to 69% of the open bookings while letting the newest complete date reach June 2017 (Review horizon, ok).

**Assessment (AI, 2026-11-11):** applied issue 1 (reply a): `_make_splits` lists the ten dates (1 June 2017 added; its rules unchanged). Counted with the split's own rules on the 81,418 bookings: test 6,511, 6,390, 6,015, 5,768, 4,578, 2,500, 2,474, 3,228, 4,314 and 4,596 (1 June 2017 back to 1 September 2016), train 64,524, 60,693, 57,112, 53,850, 50,982, 48,617, 45,946, 42,942, 39,297 and 35,860 (79.3%, 74.5%, 70.1%, 66.1%, 62.6%, 59.7%, 56.4%, 52.7%, 48.3% and 44.0%); 10.9% of the newest date's test bookings are cancelled (12.5% at 1 May 2017). `task_summary`, the notes and `splits_comment` name the ten dates, the latest prediction point (1 June 2017, arrivals to 31 August 2017), the two dates under half and the horizon's reason. `dataset check`: 0 errors, 0 warnings, with `splits_train_under_half` accepted on the CC line above.

## Review

**Outcome:** added. On 2026-11-11 you chose all ten prediction dates, 1 September 2016 to 1 June 2017, the two
oldest training on 48.3% and 44.0% of the bookings (issue 1, reply a), and kept the three-month horizon (H, A).

**Main points:** Settled on 2026-11-11: the test predicts at the first of each month from September 2016 to June 2017,
the newest date whose three months of arrivals the data holds (issue 1); three months of arrivals at monthly dates
hold, the length ours since the source scores every open booking (H). Nothing is left to decide.

**Horizon:**

* **Verdict:** keep three months of arrivals at monthly prediction dates (medium confidence): the source's system scores
  every open booking each day, so no source sets three months, but three months holds 38% to 69% of the open bookings
  where it can be measured and lets the newest complete date reach June 2017.
* **Length:** declared three months: at each date, the open bookings that arrive within three months. The source's
  system "trains daily with a dataset of all reservations on-the-books", predicts all future arrivals, and shows
  demand "one year in advance" (Antonio, de Almeida and Nunes 2019, Data Science Journal 18, 32,
  https://doi.org/10.5334/dsj-2019-032); the three months and the first-of-month dates are ours, from the task
  summary's revenue manager. Of the bookings open at 1 September 2016 to 1 January 2017, 38% to 69% arrive within
  three months and 71% to 82% within six (median 49 to 124 days ahead).
* **Gap:** none needed: a booking's outcome is known by its arrival date, and training holds only bookings that
  arrived before the prediction date.
* **Time frame:** arrivals from 1 July 2015 to 31 August 2017 (81,418 bookings after cleaning). A date's three months
  must end by 31 August 2017, so the newest complete date is 1 June 2017, not today's 1 May; dates from 1 November
  2016 on keep half the bookings for training (issue 1).
* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | A | Three months (implemented) | at each first-of-month date, the open bookings that arrive within three months; the newest complete date is 1 June 2017 | 9 dates of 2,474 to 6,390 open bookings (issue 1's B: 8 of 2,474 to 6,511), counted with the split's own filters | 38% to 69% of the open bookings where measured; the newest complete date reaches June 2017 | no source sets three months: the length and the dates are ours, from the task summary's revenue manager |
  | B | One month | ten dates from November 2016 to August 2017 | 10 dates of 968 to 2,439 open bookings | ten dates | 15% to 36% of the open bookings |
  | C | Six months | the newest complete date is 1 March 2017: five dates above the floor | 5 dates of 4,494 to 10,257 open bookings | closer to the source's whole book (71% to 82% of the open bookings) | five dates |
  | D | Every open booking | all future arrivals at each date | 8 dates (issue 1's B) of 6,305 to 10,257 open bookings, arrivals up to 31 August 2017 | the source's own scope | this release can never complete it: bookings are made up to 737 days ahead |

* **Recommendation:** A: three months hold 38% to 69% of the open bookings and reach June 2017, where one month holds
  15% to 36% and six months stop at March 2017 with five dates. **Decision:** A, B, C or D?

**Lennart (2026-11-11, ok):** As implemented (A).

**Resolved (2026-11-11, Lennart):** A: three months of arrivals at first-of-month dates, no gap, kept; with issue 1
the newest date is 1 June 2017, whose arrivals (2 June to 31 August 2017) the data holds complete. `splits_comment`
gives this block's reason (the source's system scores every open booking and sets no length; three months hold 38% to
69% of the open bookings and reach June 2017, where one month holds 15% to 36% and six months stop at March) and why
no gap is needed. The record has the horizon CC line. `dataset check`: 0 errors, 0 warnings.

**Issues for Lennart:**

1. **Which prediction dates should the test use?**

   * **Problem:**
     - The nine prediction dates run from 1 September 2016 to 1 May 2017, and the two oldest train on 44.0% and 48.3%
       of the bookings, under the half every train side must keep[^hb-split14].
     - The newest date whose three months of arrivals lie in the data is 1 June 2017 (arrivals 2 June to 31 August
       2017), one month after today's newest, and the newest window always stays[^hb-split15].
     - The dates that keep half the bookings for training run from 1 November 2016 to 1 June 2017: eight dates, one
       fewer than the nine a task of this size gets.
   * **Background:**
     - The split is custom: at each date the test is the bookings made by then that arrive within three months and are
       not yet cancelled; training is the bookings that arrived before the date, without those cancelled 90 days or
       more ahead (7.7% of all bookings never train).
     - The train share counts all 81,418 bookings. Counted against the bookings that can ever train, 1 October 2016
       would keep 52.3% and 1 September 47.7%; the floor counts all rows, as for every other dataset.
     - The splits comment stops at May for "three months before the end of the recorded period"; the data ends on 31
       August 2017, so the June date's three months are complete and the July date's (two months) are not.
     - The test windows overlap in arrival months by design: each date tests the next three months, so a month of
       arrivals is tested at up to three dates, with the bookings known at each.
     - B covers arrivals from November 2016 to August 2017, with the summer peak in the June date; it drops the
       autumn arrivals (September and October 2016) of A's two oldest dates.
     - The test bookings cancel less (10.9% to 18.0%) than the train sides (21.7% to 23.0%), since the test leaves out
       bookings cancelled before the date.
     - PSI, the population stability index, compares a feature's distribution in the window with its train side;
       above 0.25 is usually read as a large shift. The arrival date's year, month and week drift by design and are
       left out; the largest is then the lead time at every date.
   * **Statistics:** from the split's own rules run on the definition's frame (the candidate table cannot read a
     custom split); the drift from all rows.

     | Date | In | Test bookings | Cancelled, test | Cancelled, train side | Train share | Largest PSI (lead time) |
     |---|---|---|---|---|---|---|
     | 1 Jun 2017 | B | 6,511 | 10.9% | 23.0% | 79.3% | 1.45 |
     | 1 May 2017 | A, B, C | 6,390 | 12.5% | 23.0% | 74.5% | 1.40 |
     | 1 Apr 2017 | A, B, C | 6,015 | 13.0% | 22.7% | 70.1% | 1.43 |
     | 1 Mar 2017 | A, B, C | 5,768 | 14.0% | 22.7% | 66.1% | 0.98 |
     | 1 Feb 2017 | A, B, C | 4,578 | 15.6% | 22.5% | 62.6% | 0.65 |
     | 1 Jan 2017 | A, B, C | 2,500 | 18.0% | 22.3% | 59.7% | 0.67 |
     | 1 Dec 2016 | A, B, C | 2,474 | 17.1% | 22.0% | 56.4% | 0.56 |
     | 1 Nov 2016 | A, B, C | 3,228 | 14.8% | 22.0% | 52.7% | 0.65 |
     | 1 Oct 2016 | A | 4,314 | 15.0% | 21.8% | 48.3% | 0.85 |
     | 1 Sep 2016 | A | 4,596 | 13.8% | 21.7% | 44.0% | 1.20 |

   * **Effect on the task:** A scores two of its nine dates with models fit on less than half the bookings and leaves
     out the newest date the data completes. B tests eight dates, each model fit on at least 52.7% of the bookings, and
     its newest date is the deployment period the release ends with.
   * **Consistency:** california_house_prices_2020 moved its oldest window from 25% to 50% of the rows (2026-10-21).
     The split's leak fix (2026-09-30, training only on bookings that arrived before the date) is unchanged by either
     option. No dataset has chosen windows under the rewritten rule yet; delivery_eta_1m's issue 1 is open.
   * **Sources:** the definition `datasets/_dev/tabarena-v0pt2/hotel_booking_demand/dataset.py` (`_make_splits`,
     `splits_comment`, `task_summary.split`); the record `curation/records/hotel_booking_demand.md` (the CC of
     2026-09-30 on the split; no earlier call on the dates); the data paper (Antonio, de Almeida and Nunes 2019, Data in
     Brief 22, 41-49).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | September 2016 to May 2017 (implemented) | predicts at nine dates, 1 Sep 2016 to 1 May 2017 | nine dates; arrivals from September 2016 | two train sides under the floor (44.0%, 48.3%); the newest complete date (1 June 2017) left out |
     | B | November 2016 to June 2017 | predicts at eight dates, 1 Nov 2016 to 1 Jun 2017 | every train side keeps at least 52.7%; the newest complete date; summer arrivals to August 2017 | eight dates instead of nine; no autumn arrivals |
     | C | November 2016 to May 2017 | predicts at seven dates, 1 Nov 2016 to 1 May 2017 | every train side keeps at least 52.7%; today's newest date | the newest complete date left out; seven dates |

   * **Recommendation:** B: it keeps every date that the floor allows and adds the newest one the data completes,
     which the rule keeps in every case. **Decision:** A, B or C?

   **Notes for the AI:** the split is custom, so `temporal = Temporal(on="arrival_date", horizon=3,
   horizon_unit="months")` stays; on B, set `test_sets_year_month = [(2017, 6), (2017, 5), (2017, 4), (2017, 3),
   (2017, 2), (2017, 1), (2016, 12), (2016, 11)]` in `_make_splits` (on C, the same without `(2017, 6)`). Computed with
   the split's rules on the definition's frame (81,418 bookings): test 6,511, 6,390, 6,015, 5,768, 4,578, 2,500, 2,474
   and 3,228; train 64,524, 60,693, 57,112, 53,850, 50,982, 48,617, 45,946 and 42,942 (79.3% to 52.7%). Then rewrite
   `task_summary.split` ("Nine prediction dates, the first of each month from September 2016 to May 2017"),
   `task_summary.predicted` ("12.5% of the test bookings of the newest split"; 10.9% under B), and the sentence on the
   latest prediction point in `splits_comment` and `curation_comments`; add a CC line to the record and a dated
   CHANGELOG entry, and run `dataset check` (SPLIT-14, SPLIT-15). `dataset windows hotel_booking_demand` stops with
   `KeyError: 'ReservationStatus'`: `AbstractCuratedDataset.window_stats` takes the features from the frame before the
   split and the custom windows' statistics from the split's frame, which drops the outcome columns; a framework fix,
   not part of this decision.

   [^hb-split14]: **SPLIT-14** (Must): "A temporal task has at least 3 windows, and no window's train side holds less
     than 50% of the data."
   [^hb-split15]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): "The newest window is always a test window: it is the deployment period. ... Every choice stays above
     SPLIT-14's floor; the length and the gap come from SPLIT-12; as many windows as an IID or grouped task of that
     size would get folds, then check that they are still meaningful (SPLIT-16 to SPLIT-18)."

   **Lennart (2026-11-11, discuss):** Why can we not extend it or roll back from the newest data to include 1 Jun in
   option (A) as well?

   **Answer (AI, 2026-11-11):** Test all ten dates, 1 September 2016 to 1 June 2017, now that the amended floor admits
   the two oldest?

   * **Problem:**
     - Option A left out 1 June 2017 only because it kept today's nine dates, and B left out September and October 2016
       because their train sides hold 44.0% and 48.3% of the bookings.
     - Since 2026-11-11 windows under half are admitted down to 30% when the newest and one other window are above it
       and no more windows are under half than above[^a-14]: the ten dates have eight above half and two under.
     - 1 June 2017 is the newest date whose arrivals the data holds complete (to 31 August 2017).
   * **Options:**

     | | Option | What it does | Test windows | Pro | Con |
     |---|---|---|---|---|---|
     | a | All ten dates | the nine dates of A and 1 June 2017 | 10 dates of 2,474 to 6,511 open bookings | every date with complete arrivals; both autumns 2016 and the summer 2017 | two train sides under half (44.0%, 48.3%) |
     | b | B as proposed | the eight dates 1 November 2016 to 1 June 2017 | 8 dates of 2,474 to 6,511 open bookings | every train side above half | no September or October date |

   * **Recommendation:** a: it adds the newest complete date to today's dates, and the amended floor admits the two
     oldest. **Decision:** a or b?

   [^a-14]: **SPLIT-14** (Must; amended 2026-11-11, Lennart): the newest window and at least one other train on at least 50% of the data; further windows down to 30%, and at most as many windows under 50% as at or above it.

   **Lennart (2026-11-11, discuss):** Reply (a): All ten dates

   **Resolved (2026-11-11, Lennart):** a: the test predicts at ten dates, the first of each month from 1 September 2016
   to 1 June 2017. `_make_splits` changes only its list of dates (`(2017, 6)` added); its rules are unchanged. Counted
   with those rules on the 81,418 bookings, newest first: test 6,511, 6,390, 6,015, 5,768, 4,578, 2,500, 2,474, 3,228,
   4,314 and 4,596, train 64,524 down to 35,860 (79.3%, 74.5%, 70.1%, 66.1%, 62.6%, 59.7%, 56.4%, 52.7%, 48.3% and
   44.0%), as the issue gave. The two under half, 1 October 2016 (48.3%) and 1 September 2016 (44.0%), are signed off
   with this mark: the record's CC line names them and the definition accepts `splits_train_under_half` with them.
   `task_summary` (ten dates; 10.9% of the newest date's test bookings cancelled, against 12.5% at 1 May),
   `splits_comment` and the curation notes name the ten dates, the latest prediction point (1 June 2017) and the two
   dates under half; the leak measurement of 867 rows is dated to the split of 1 May 2017. `dataset check`: 0 errors,
   0 warnings.

## Reference

Antonio, N., de Almeida, A., & Nunes, L. (2019). Hotel booking demand datasets. Data in brief, 22, 41-49.
