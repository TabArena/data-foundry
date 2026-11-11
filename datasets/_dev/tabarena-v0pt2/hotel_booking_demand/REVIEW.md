# hotel_booking_demand

**Outcome:** added. Under the rule on choosing test windows, rewritten on 2026-11-10, the AI proposes the eight
prediction dates from 1 November 2016 to 1 June 2017 in place of the nine from 1 September 2016 to 1 May 2017: the two
oldest train on less than half the bookings, and 1 June 2017 is the newest date whose three months of arrivals lie in
the data (issue 1). The three-month horizon stays. `dataset.py` is unchanged until you decide.

**Main points:** Predict on the eight first-of-month dates from November 2016 to June 2017 instead of the nine from
September 2016 to May 2017 (issue 1)?

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

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | A | Three months (implemented) | at each first-of-month date, the open bookings that arrive within three months; the newest complete date is 1 June 2017 | 38% to 69% of the open bookings where measured; the newest complete date reaches June 2017 | no source sets three months: the length and the dates are ours, from the task summary's revenue manager |
  | B | One month | ten dates from November 2016 to August 2017 | ten dates | 15% to 36% of the open bookings |
  | C | Six months | the newest complete date is 1 March 2017: five dates above the floor | closer to the source's whole book (71% to 82% of the open bookings) | five dates |
  | D | Every open booking | all future arrivals at each date | the source's own scope | this release can never complete it: bookings are made up to 737 days ahead |

* **Recommendation:** A: three months hold 38% to 69% of the open bookings and reach June 2017, where one month holds
  15% to 36% and six months stop at March 2017 with five dates. **Decision:** A, B, C or D?

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
