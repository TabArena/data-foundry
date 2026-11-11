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

CC (2026-11-11, Andrej): the marks of Andrej's review page applied (its issues 2, 3 and 4, merged into the record's review on this date).
- Issue 4 ("Option B: Drop DepositType"): `DepositType` is dropped in `_clean`, the data paper computes it from the payments up to arrival or cancellation, so up to three months after the prediction date; "Non Refund" bookings were cancelled at 97.3% (city) and 84.6% (resort) against 30.2% and 25.0% without a deposit, and dropping it costs nothing (LightGBM ROC AUC 0.811 without it, 0.810 with it). 27 features.
- Issue 3 (`ok`): the 90-day training rule stays; the sentence saying the choice was never tested is replaced in the curation notes and the splits comment by the measurement of 2026-11-06 (same ranking, ROC AUC 0.810; mean prediction 0.216 against 0.176, log loss 0.364 against 0.349; the alternative leaves 30% to 50% of the bookings for training).
- Issue 2 ("Option B: Seven dates"): **not applied.** It contradicts issue 1, settled the same day with all ten dates (1 September 2016 to 1 June 2017) under the floor amended on 2026-11-11; issue 2 was written on 2026-11-06, when the definition had nine dates and the floor admitted no train side under half, so it could not hold 1 June 2017, the newest date whose three months of arrivals the data holds. The choice between ten, seven and eight dates is issue 6, open.
- `dataset check`: 0 errors, 0 warnings, 1 info (296 rows, 0.4%, share all features with another row and carry a different target, 18 more than with `DepositType`). Ten windows unchanged.

## Review

**Outcome:** added. Antonio, de Almeida and Nunes' (2019) bookings of a resort hotel in the Algarve and a city
hotel in Lisbon, arrivals July 2015 to August 2017 (81,418 after removing repeated records and same-day bookings);
the target is whether the booking is cancelled (29% overall). A revenue manager sets overbooking for the next three
months, and the public version's leaks are handled: the outcome columns only cut the windows and are dropped, the
fields recorded up to check-in are dropped, training holds only bookings that arrived before the prediction date,
and `DepositType`, computed from payments up to arrival or cancellation, left on 2026-11-11 (issue 4). On 2026-11-11
Lennart chose all ten prediction dates, 1 September 2016 to 1 June 2017, the two oldest training on 48.3% and 44.0%
of the bookings (issue 1, reply a), and kept the three-month horizon (H, A); Andrej's mark of the same day asks for
seven dates (issue 2), which the ten contradict, so the dates are open again as issue 6.

**Main points:** Open: the prediction dates, where issue 1 (ten dates) and issue 2 (seven) disagree and issue 6 puts
the choice; and whether to ship as defined (issue 5). Settled on 2026-11-11: three months of arrivals at monthly
dates, the length ours since the source scores every open booking (H); the 90-day training rule kept with the
measured numbers in the note (issue 3); `DepositType` dropped (issue 4).

**Record judgment:** valid, ship. Lennart's fix of 2026-09-30 (training only on arrived bookings; the three
check-in fields dropped) is in the definition, and the training filter is the case of the rule that training labels
must be known at the prediction point. A separate review of metrics proposes log loss for this dataset (the hotels
sum the probabilities for overbooking); it is not part of this review. Nothing in the record disagrees with the
definition. The review of Andrej's page (its issues 2, 3 and 4, and its issue 1 as issue 5 here) was merged into
this one on 2026-11-11; only that issue was renumbered, and it carries no mark.

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

**Issues for Andrej and Lennart:**

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

2. **Drop the two oldest prediction dates, whose training sides hold under half of the bookings?**

   * **Problem:**
     - Each prediction date trains on the bookings that had arrived by then, and for the two oldest, 1 September and 1 October 2016, these are 35,860 and 39,297 of the 81,418 bookings (44.0% and 48.3%).
     - Every training side of a temporal task needs half of the data or more, and the other seven dates train on 52.7% (November 2016) to 74.5% (May 2017)[^2a].
     - Keep seven dates, November 2016 to May 2017, or all nine?
   * **Background:**
     - How the data arrives: bookings come in over time with their arrival date and lead time, every value is a snapshot of the day before arrival (issue 1), and the label is final at arrival, since a booking is cancelled, if at all, before it (median 41 days before, 28% more than 90 days before). The record's collection facts say this (`Samples: Over Time`, `Time: Dated`, `Target: Varying Delay`), and a temporal split carries no time-basis tag[^2b].
     - No gap is needed: training holds only bookings that arrived before the prediction date, so every training label was known then, and the already-cancelled future bookings, the shortcut fixed on 2026-09-30, stay out[^2c].
     - Counted on all bookings that had arrived before the date, the two oldest dates have 46.3% and 50.9%; the rule that leaves out bookings cancelled more than 90 days ahead (issue 3) takes both below half.
   * **Experiments:** counted with the definition's split code on the publisher's two files: test bookings per date, newest first, 6,390, 6,015, 5,768, 4,578, 2,500, 2,474, 3,228, 4,314 and 4,596 (39,863 in all).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Nine dates (implemented) | the first of each month from September 2016 to May 2017 | 39,863 test bookings | two training sides below half of the data (44.0%, 48.3%) |
     | B | Seven dates | the first of each month from November 2016 to May 2017 | every training side at 52.7% or more | 8,910 fewer test bookings (30,953); seven windows instead of nine |

   * **Recommendation:** B: the floor is a hard rule, and seven windows still give seven separate refits with 2,474 or more test bookings each. **Decision:** A or B?

   **Notes for the AI:** on B, remove `(2016, 10)` and `(2016, 9)` from `test_sets_year_month` in `_make_splits`; "9 points in time" becomes "7 points in time" in `curation_comments` and `splits_comment`; the task summary's `split`: "Seven prediction dates, the first of each month from November 2016 to May 2017. ..."; `dataset check`, rebuild, report the train shares; record `CC (<date>, Andrej):` line. No time-basis tag under either option (temporal split); once PR #50 is in, `data_tags` stays empty.

   [^2a]: **SPLIT-14** (Must): a temporal task has at least 3 windows, and no window's train side holds less than 50% of the data. **SPLIT-15** (Should): as many windows as an IID task of that size gets folds; the Must comes first.
   [^2b]: **SPLIT-32** (Should): how the data was collected (the record's facts on samples, time and target) is information for the split; a definition names a use-case prototype only for a split that is not temporal.
   [^2c]: **SPLIT-9** (Must): a training row whose label was not yet known at the prediction point must not be in train; hotel_booking_demand is its case (filtering on the arrival date removed the shortcut). **SPLIT-10** (Should): no gap is needed where the collection covers what the gap guards against.

   **Resolved (2026-11-11, Andrej):** B: `(2016, 10)` and `(2016, 9)` removed from `_make_splits`; "7 points in time" in the curation notes and the splits comment, the task summary's `split` names November 2016 to May 2017. `dataset check`: 0 errors, 0 warnings; 7 windows, training 42,942 (52.7%) to 60,693 (74.5%) of the 81,418 bookings, test 2,474 to 6,390 (30,953 in all). Not rebuilt.

   **Andrej (2026-11-11, change):** Option B: Seven dates.

   **Answer (AI, 2026-11-11):** not applied here: this mark and issue 1's reply of the same day choose different
   dates, so the question goes to issue 6 and the definition keeps issue 1's ten dates until it is settled.

   * This issue was written on 2026-11-06 against a definition with nine dates and the floor as it then read, so its
     options could not hold 1 June 2017, the newest date whose three months of arrivals the data holds.
   * Issue 1 (Lennart, 2026-11-11) chose all ten dates, 1 September 2016 to 1 June 2017, under the floor amended that
     day, which admits two train sides under half beside eight above it.
   * Option B's seven dates (November 2016 to May 2017) leave out 1 June 2017, which the newest-window rule keeps in
     every case.
   * The three choices are laid out in issue 6; nothing in the definition changed for this issue.

3. **Train only on bookings that were still open at an earlier prediction date, as the test bookings are?**

   * **Problem:**
     - A test booking is one still open on its prediction date, while a training booking is any arrived booking not cancelled more than 90 days ahead, so training is 22.3% cancelled against 14.9% in test (means over the nine dates).
     - Models trained this way rank the test bookings as well as any other training set tried (ROC AUC 0.810), but predict 21.6% cancelled on average, and the use case sums these probabilities to set overbooking.
     - Replace the 90-day rule by the condition the test bookings meet, or keep it?
   * **Background:** the definition's own note says the 90-day rule was chosen "based on assumptions without actually testing the impact of this decision". The condition of the test rows, applied to history: a training booking arrived before the prediction date and was open (made, not yet cancelled) on one of the three first-of-months before its arrival. It keeps the history the same and only leaves out bookings that would never have been open on a prediction date[^3a].
   * **Experiments:** LightGBM (400 trees, three seeds), the definition's features, the nine dates, the same test rows (14.9% cancelled); means over the dates:

     | Training rows | Rows at the newest date | Cancelled in training | ROC AUC | Log loss | Mean prediction |
     |---|---|---|---|---|---|
     | A, the 90-day rule (implemented) | 60,693 | 22.3% | 0.810 | 0.364 | 0.216 |
     | B, open at an earlier prediction date, each booking once | 40,664 | 17.4% | 0.810 | 0.349 | 0.176 |
     | C, as B, once for each earlier date it was open | 82,130 (40,386 bookings) | 13.9% | 0.810 | 0.343 | 0.162 |

     - Under B the training sides hold 29.7% (September 2016) to 49.9% (May 2017) of all bookings.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | The 90-day rule (implemented) | train on arrived bookings, without those cancelled more than 90 days ahead | the most training rows; ranks as well as B and C | training 22.3% cancelled against 14.9% in test; mean prediction 0.216 |
     | B | Open at an earlier prediction date | train on arrived bookings that were open on one of the three first-of-months before their arrival | the condition the test rows meet; mean prediction 0.176, log loss 0.349 | training sides of 30% to 50% of all bookings, below half of the data |
     | C | Once for each earlier date | as B, with a booking repeated for each date it was open | weighs bookings as the overlapping test windows do (log loss 0.343) | duplicated rows in the frame; the same floor problem as B |

   * **Recommendation:** A, with the measured numbers in the note: the ranking does not change, and B and C take every training side below half of the bookings; B is the choice if the floor is read on the history before each date, which B leaves whole. **Decision:** A, B or C?

   **Notes for the AI:** on A, replace the sentence "Note that we made this choice based on assumptions without actually testing the impact of this decision. It would be interesting to test the impact of this decision on prediction performance." in `curation_comments` and `splits_comment` with: "Tested 2026-11-06: training only on the arrived bookings that were open on one of the three monthly prediction dates before their arrival, the condition of the test rows, ranks the same (LightGBM, nine dates, ROC AUC 0.810) and lowers the mean prediction from 0.216 to 0.176 against 0.149 cancelled in test (log loss 0.364 to 0.349), but leaves 30% to 50% of the bookings for training; the 90-day rule stays." On B, replace step d) of `_make_splits` by that condition (for a training booking, the first-of-months q with `booking_date <= q < arrival_date < q + 3 months`, kept when `ReservationStatusDate > q` for one of them), rewrite the task summary's `changes` and the two notes, `dataset check`, rebuild; record `CC` line. C needs duplicated rows in the frame and is not written out.

   [^3a]: **SPLIT-1** (Must): the split mirrors the real application. **SPLIT-14** (Must): no window's train side holds less than 50% of the data. **SPLIT-20** (Should): what the train side holds is the history a model refit at each window would train on.

   **Resolved (2026-11-11, Andrej):** A (`ok` on the recommendation): the 90-day rule stays; the untested-assumption sentence in the curation notes and the splits comment is replaced by the measured numbers (same ranking, ROC AUC 0.810; mean prediction 0.216 against 0.176 under B; 30% to 50% of the bookings for training under B).

   **Andrej (2026-11-11, ok):** As implemented.

   **Resolved (2026-11-11, Andrej):** A, now applied on this branch: the sentence "Note that we made this choice
   based on assumptions ..." in `curation_comments` and `splits_comment` is replaced by the measured numbers (same
   ranking, LightGBM ROC AUC 0.810; mean prediction 0.216 against 0.176 under B, log loss 0.364 against 0.349; B
   leaves 30% to 50% of the bookings for training). The 90-day rule itself is unchanged.

4. **Drop `DepositType`, which the data paper computes from payments up to arrival or cancellation?**

   * **Problem:**
     - The data paper computes `DepositType` from "the payments identified for the booking in the transaction (TR) table before the booking's arrival or cancellation date", so a payment made after the prediction date, up to three months later, counts.
     - "Non Refund" bookings, paid in full, are cancelled at 97.3% in the city hotel (843 bookings) and 84.6% in the resort (188), against 30.2% and 25.0% without a deposit; among the open bookings of the test windows, 6 to 26 per date, they are cancelled at 83% to 100%.
     - Drop the column, or keep it with a note?
   * **Background:** the paper does not say why fully paid bookings are cancelled far more often, and the release has no payment dates, so whether a deposit came before the prediction date cannot be traced row by row. A value computed over a window that ends at the outcome goes unless the data shows it does not move with the outcome, and a value read later stays with a note only when the traced part shows no gain[^4a]. Issue 1 tested the fields guests change before arrival, not this one. "No Deposit" is 98.6% of the bookings.
   * **Experiments:** LightGBM as in issue 3, nine dates, three seeds: ROC AUC 0.811 without `DepositType` and 0.810 with it (log loss 0.366 and 0.364).
   * **Consistency:** follows kick's `WheelType`, `PRIMEUNIT` and `AUCGUART`, whose recording followed the outcome and which were dropped (2026-10-22, Lennart).
   * **Sources:** Antonio N, de Almeida A, Nunes L. Hotel booking demand datasets. Data in Brief. 2019;22:41-49, Table 1.
     <https://doi.org/10.1016/j.dib.2018.11.126>
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | the source's field | no change; no gain from it measured | computed up to arrival or cancellation; its "Non Refund" level is nearly always cancelled, unexplained |
     | B | Drop `DepositType` | one feature less | only what exists at the prediction date; no cost (0.811 without) | loses the deposit a hotel knows at booking for most rows |

   * **Recommendation:** B: the source dates the field after the prediction date, its rare level behaves like the outcome, and it adds nothing measured. **Decision:** A or B?

   **Notes for the AI:** on B, drop `DepositType` in `_clean` next to `BookingChanges`, `AssignedRoomType` and `RequiredCarParkingSpaces`, remove it from `ORDINAL_LEVELS`, add a curation note with the numbers above, remove "deposit type" from the task summary's `known`, `dataset check`, rebuild; record `CC` line. On A, a curation note with the same numbers and "kept: no gain measured".

   [^4a]: **LEAK-10** (Must): a feature holds only what existed at the prediction point; out is a feature computed from the window that defines the target, unless the data shows the window's values do not move with the outcome; a value read at a later pull goes when it may carry a gain and stays with a note only when the part that can be traced shows none.

   **Resolved (2026-11-11, Andrej):** B: `DepositType` dropped in `_clean` and removed from `ORDINAL_LEVELS` and the categorical list, with a curation note giving the numbers above; "deposit type" left the task summary's `known` and entered its `changes`. `dataset check`: 0 errors, 0 warnings; 27 features. Not rebuilt.

   **Andrej (2026-11-11, change):** Option B: Drop DepositType.

   **Resolved (2026-11-11, Andrej):** B, now applied on this branch: `_clean` drops `DepositType` beside the three
   check-in fields, and it leaves `ORDINAL_LEVELS` and the categorical list; the task summary's `known` no longer
   names the deposit type and its `changes` does; a curation bullet gives the paper's definition of the column and
   the numbers. 27 features. `dataset check`: 0 errors, 0 warnings, 1 info (296 rows, 0.4%, now share all features
   with another row and carry a different target, 18 more than with the column).


5. **Ship as defined?**

   * **Problem:**
     - Nothing open was found: the columns that give the outcome away in the public version only build the windows and are dropped, the fields recorded up to check-in are dropped, and the snapshot taken the day before arrival does not carry the score.
     - The country of the guest carries much of the score (ROC AUC 0.813 with it, 0.701 without), and the data paper warns that hotels often learn the nationality only at check-in.
     - Ship as defined, or retire?
   * **Background:** the data paper defines "the data point time for each observation" as "the day prior to each
     booking's arrival" and takes values "from the bookings change log, with a timestamp relative to the day prior to
     arrival date" (Antonio et al. 2019, Specifications table and Sec. 1). It adds: "It is also common for hotels not
     to know the correct nationality of the customer until the moment of check-in ... the distribution of some
     variables differ between non canceled and canceled bookings" (Sec. 2). The prediction date is up to three months
     earlier, so a value the guest changed in between could tell the classes apart[^5a].
   * **Experiments:** v0.2 frame and windows built with the definition's own split code from the publisher's files
     (81,418 rows, test sizes as in the README; Slurm job 1344943), LightGBM, mean over the 9 windows:
     - Bookings never amended (77% of the test bookings; the paper's `BookingChanges` counts changes of persons,
       dates, nights, room type or meal): ROC AUC 0.813, the same as on all test bookings (0.813). The score does not
       come from amended bookings, though non-cancelled bookings were amended more often (23% against 14%).
     - Without `Country` 0.701; without the fields guests change (country, adults, children, babies, nights, room
       type, meal, special requests, daily rate) 0.664.
     - No sign of a nationality filled in at check-in: the 333 resort bookings without a country are cancelled at 7%
       (other foreign guests 17%, Portuguese 39%); and among cancelled bookings (lead time 60 to 180 days) the
       Portuguese share rises the closer to arrival they cancel (city 22% to 40%, resort 56% to 74%), the opposite of
       a placeholder that guests correct before they arrive.
   * **Sources:** Antonio N, de Almeida A, Nunes L. Hotel booking demand datasets. Data in Brief. 2019;22:41-49.
     <https://doi.org/10.1016/j.dib.2018.11.126>
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship as defined (implemented) | 81,418 bookings, 9 monthly prediction dates, ROC AUC | a real revenue decision; the leaks fixed and the snapshot timing tested; two hotels with documented fields | values are a day-before-arrival snapshot, a stated gap |
     | B | Retire | record `No (Retired)`, folder removed | no snapshot taken after the prediction date | no measured defect; loses a documented temporal task |

   * **Recommendation:** A: the outcome columns and the check-in fields are gone, and the tests show no score from
     amended bookings and no check-in fill of the country. **Decision:** A or B?

   [^5a]: **LEAK-10** (Must): a feature holds only what existed at the prediction point; a value read at a later pull
     goes when its late cells may carry a gain, and stays with a note when the part that can be traced shows none.

6. **Ten prediction dates (issue 1) or seven (issue 2)?**

   * **Problem:**
     - Issue 1 was settled on 2026-11-11 with all ten dates, 1 September 2016 to 1 June 2017, and issue 2 with the
       seven dates of November 2016 to May 2017; both marks carry the same date and the definition can hold only one.
     - Issue 2 was written on 2026-11-06, when the floor admitted no train side under half and the newest date in the
       definition was 1 May 2017, so neither 1 June 2017 nor the amended floor could enter its options.
     - Which set of dates ships?
   * **Background:** the floor as amended on 2026-11-11 asks the newest window and one other to train on at least
     half of the data and admits further windows down to 30%, at most as many under half as at or above it; the ten
     dates have eight above (52.7% to 79.3%) and two under (48.3% and 44.0%). The newest window is a test window in
     every case, and 1 June 2017 is the newest date whose three months of arrivals (to 31 August 2017) the data
     holds[^6a].
   * **Experiments:** the split's own rules on the 81,418 bookings, newest first: test 6,511, 6,390, 6,015, 5,768,
     4,578, 2,500, 2,474, 3,228, 4,314 and 4,596; train 64,524 down to 35,860 (79.3%, 74.5%, 70.1%, 66.1%, 62.6%,
     59.7%, 56.4%, 52.7%, 48.3% and 44.0%).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ten dates (implemented) | 1 September 2016 to 1 June 2017, as issue 1 settled | the newest complete date and both autumn 2016 dates; the amended floor admits the two under half | two train sides under half (48.3%, 44.0%) |
     | B | Seven dates | 1 November 2016 to 1 May 2017, as issue 2's mark | every train side at 52.7% or more | the newest complete date (1 June 2017) is left out, which the newest-window rule keeps |
     | C | Eight dates | 1 November 2016 to 1 June 2017 | every train side above half and the newest complete date | no autumn 2016 arrivals; eight windows |

   * **Recommendation:** A, the later decision and the one the amended floor was written for; C if the two dates
     under half should go after all, since it still keeps the newest complete date. **Decision:** A, B or C?

   **Notes for the AI:** on B or C, remove `(2016, 10)` and `(2016, 9)` from `test_sets_year_month` in `_make_splits`
   (on B also `(2017, 6)`), drop the `splits_train_under_half` entry of `accepted_check_warnings`, and rewrite the
   date counts and shares in `task_summary.split`, `splits_comment` and `curation_comments`; `dataset check`.

   [^6a]: **SPLIT-14** (Must; amended 2026-11-11, Lennart): the newest window and at least one other train on at least
     50% of the data; further windows down to 30%, and at most as many windows under 50% as at or above it.
     **SPLIT-15** (Must for the newest window): the newest window is always a test window, the deployment period.

## Reference

Antonio, N., de Almeida, A., & Nunes, L. (2019). Hotel booking demand datasets. Data in brief, 22, 41-49.
