# mercedes_benz_greener_manufacturing

**Outcome:** added. On 2026-11-11 you kept the nine windows of 320 cars from ID 2,628 on (issue 1 and the horizon,
A), which the amended floor admits with the three oldest training on 46.7%, 39.1% and 31.5% of the cars.

**Main points:** Settled on 2026-11-11: the nine windows of 320 cars stay (issue 1, A), and the declared length of
320 cars without a gap is checked: no source gives a length, and 320 tests 2,880 cars where 233 would test 2,097.

**Horizon:**

* **Verdict:** change to windows of 233 cars (low confidence): no source gives a length or even a date, so the length
  follows from the newest half of the cars cut into the nine windows a task of this size gets; 233 cars is also about
  one block of the dropped time-group code `X5`.
* **Length:** declared 320 cars in ID order. The number is the arithmetic of the scikit-learn `TimeSeriesSplit` of
  the first curation (the cars after the first 1,000, cut into ten parts), not a horizon. Source: none found. The
  competition (https://www.kaggle.com/competitions/mercedes-benz-greener-manufacturing) ships no dates, and it held out
  its own test cars at random: `train.csv` holds 4,209 of the IDs 0 to 8,417, and the competition's test file the
  others. The coded category `X5`, dropped as a time group, comes in blocks of consecutive IDs: from ID 4,319 to the
  last two blocks, each holds 177 to 231 cars of `train.csv`. What a block is (a shift, a day) is not stated; 233 cars
  is about one block, 320 about one and a half.
* **Gap:** none needed: a car's testing time is known when it leaves the bench, and no row carries a date to measure a
  longer delay.
* **Time frame:** 4,204 cars after cleaning, IDs 0 to 8,417, dates not stated. The newest half (from the 2,108th car,
  ID 4,230) is open for testing; today's windows reach back to the 1,325th car (ID 2,628).
* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | A | 320 cars (implemented) | windows of 320 cars in ID order, back to the 1,325th car (ID 2,628): six keep half the cars for training | 9 windows of 320 cars each (6 above the floor) | today's length; more cars per window (2,880 test cars in all) | the arithmetic of the first curation's `TimeSeriesSplit`, not a horizon; three of the nine train sides under the floor (46.7%, 39.1%, 31.5%) |
  | B | 233 cars | nine windows over the newest half, from the 2,108th car (ID 4,230) | 9 windows of 233 cars each | the nine windows a task of this size gets, all above the floor; about one block of the dropped `X5` code | no source either; each window's score rests on 233 cars and is noisier |
  | C | 700 cars | three windows over the newest half | 3 windows of 700 cars each | the shape california_house_prices_2020 has; larger windows | three windows instead of the nine a task of this size gets |
  | D | Whole `X5` blocks | windows of the blocks of consecutive IDs, 177 to 231 cars of `train.csv` each from ID 4,319 | 11 candidates above the floor, 20 to 231 cars each (the blocks from ID 4,319) | a time unit from the data | a dropped code whose meaning is not published; its last two blocks hold 20 and 112 cars |

* **Recommendation:** B: with no source for a length, 233 cars fill the newest half the floor allows with the nine
  windows a task of this size gets, at about one block of the data's own `X5` code. **Decision:** A, B, C or D?

**Lennart (2026-11-11, ok):** As implemented (A).

**Resolved (2026-11-11, Lennart):** A, windows of 320 cars without a gap, kept, in place of the AI's 233: no source
gives either length, and the amended floor of 2026-11-11 admits nine windows of 320, which test 2,880 cars against
2,097 at 233. `splits_comment` now says that 320 is the arithmetic of the first curation's `TimeSeriesSplit`, not a
horizon, and why it is kept, and that no gap is needed (a car's time is known when it leaves the bench). `temporal` is
unchanged. The record has the horizon CC line. `dataset check`: 0 errors; its 2 warnings (11 constant and 45
duplicated option columns) are about the data, not the windows, and are not settled here (README not regenerated).

**Issues for Lennart:**

1. **Which windows of cars should the test use?**

   * **Problem:**
     - The nine test windows of 320 cars in ID order reach back to the 1,325th car, and the three oldest train on
       46.7%, 39.1% and 31.5% of the cars, under the half every train side must keep[^mb-split14].
     - Six windows of 320 cars keep half the cars for training, while a task of 4,204 rows gets nine windows, and the
       length 320 has no source[^mb-split15].
     - Nine windows of 233 cars fill the newest half exactly, and 233 cars is about one block of the dropped `X5` code.
   * **Background:**
     - The car ID is the only order, and the source does not confirm it is the order of testing (the fit is
       approximate); the windows are equal runs of cars, with no season or period to choose between.
     - The one exception to the floor, an older window on at least 40% of the rows when only two windows are above the
       floor and most test entities recur, does not apply: six or nine windows are above it, and each car is tested
       once.
     - The target moves little: the mean testing time is 98.7 to 102.6 seconds per window, 100.7 to 101.5 on the train
       sides.
     - PSI, the population stability index, compares a feature's distribution in the window with its train side;
       above 0.25 is usually read as a large shift. The largest is 0.23 to 0.58 in every candidate, in the coded
       categories `X0` to `X2` and the option `X38`.
     - The task summary says "the first 1,000 cars are always in training"; today the oldest window trains on 1,324,
       under B on 2,107.
   * **Statistics:** from the candidate tables, over all cars.

     | Window (car IDs) | In | Mean seconds, test | Train side | Train share | Largest PSI |
     |---|---|---|---|---|---|
     | 7,973-8,417 | B | 98.9 | 100.7 | 94.5% | 0.57 |
     | 7,499-7,972 | B | 99.1 | 100.8 | 88.9% | 0.40 |
     | 7,005-7,498 | B | 99.5 | 100.9 | 83.4% | 0.31 |
     | 6,539-7,004 | B | 99.0 | 101.0 | 77.8% | 0.34 |
     | 6,111-6,538 | B | 100.5 | 101.1 | 72.3% | 0.30 |
     | 5,630-6,103 | B | 101.0 | 101.1 | 66.7% | 0.30 |
     | 5,163-5,627 | B | 101.5 | 101.1 | 61.2% | 0.30 |
     | 4,701-5,162 | B | 102.6 | 100.9 | 55.7% | 0.51 |
     | 4,230-4,699 | B | 99.9 | 101.0 | 50.1% | 0.29 |
     | six of 320 cars, 4,581-8,417 | A, C | 98.7 to 101.9 | 100.8 to 101.1 | 54.3% to 92.4% | 0.23 to 0.56 |
     | 3,920-4,579 | A | 100.1 | 101.1 | 46.7% | 0.58 |
     | 3,308-3,919 | A | 100.3 | 101.3 | 39.1% | 0.28 |
     | 2,628-3,306 | A | 100.5 | 101.5 | 31.5% | 0.40 |

   * **Effect on the task:** A scores three of its nine windows with models fit on 1,324 to 1,964 cars, under half of
     them. B scores nine windows of 233 cars over the newest half, each model fit on at least 2,107 cars; a window's
     R^2 rests on 233 cars instead of 320, so each is noisier, while the nine together test 2,097 cars (A 2,880, C
     1,920).
   * **Consistency:** california_house_prices_2020, the other dataset ordered only by rows, moved its oldest window
     from 25% to 50% of the rows and tests three windows over the newest half (2026-10-21). coffee_rating_prediction
     widened windows of under about 50 test rows; 233 is well above. No dataset has chosen windows under the rewritten
     rule yet; delivery_eta_1m's issue 1 is open.
   * **Sources:** the definition `datasets/_dev/tabarena-v0pt2/mercedes_benz_greener_manufacturing/dataset.py`
     (`temporal`, `splits_comment`, `task_summary.split`, the `X5` bullet of `curation_comments`); the record
     `curation/records/mercedes_benz_greener_manufacturing.md` (no earlier call on the windows); the candidate tables
     `.venv/bin/python -m data_foundry.curation.cli dataset windows mercedes_benz_greener_manufacturing --root
     datasets/_dev/tabarena-v0pt2` (9 windows) and the same with `--window 233 --unit rows` (9 above the floor); the
     `X5` blocks from `train.csv` (the first ID and the count of each code).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Nine windows of 320 cars (implemented) | tests the cars from ID 2,628 on | today's windows; 2,880 test cars | three train sides under the floor (46.7%, 39.1%, 31.5%); the length has no source |
     | B | Nine windows of 233 cars | tests the newest half, from ID 4,230 on | every train side keeps at least 50.1%; the nine windows a task of this size gets; about one `X5` block per window | 233 cars per window, so each window's score is noisier; 2,097 test cars |
     | C | Six windows of 320 cars | tests the newest six of today's windows, from ID 4,581 on | keeps today's length; every train side keeps at least 54.3% | six windows instead of nine; 1,920 test cars |

   * **Recommendation:** B: the newest half is all the floor allows, nine windows of it keep the count a task of this
     size gets, and with no source for a length the windows should follow the data's own block of about 200 cars
     rather than an old split's arithmetic. **Decision:** A, B or C?

   **Notes for the AI:** on B, `temporal = Temporal(on="time_index", splits=TemporalSplits(window=233, unit="rows",
   cutoffs=(3971, 3738, 3505, 3272, 3039, 2806, 2573, 2340, 2107)))`; the cutoffs are row positions of the sorted
   frame, not IDs. The same windows come from `TemporalSplits(window=None, unit="rows", n_windows=9,
   min_train_fraction=0.5)` with `horizon=233, horizon_unit="steps"`, california's form. Built with `window_bounds` on
   the definition's frame: test 233 cars each, train 3,971, 3,738, 3,505, 3,272, 3,039, 2,806, 2,573, 2,340 and 2,107
   (94.5% to 50.1%). On C, `TemporalSplits(window=320, unit="rows", cutoffs=(3884, 3564, 3244, 2924, 2604, 2284))`:
   test 320 each, train 3,884, 3,564, 3,244, 2,924, 2,604 and 2,284 (92.4% to 54.3%). Then rewrite `task_summary.split`
   ("The first 1,000 cars are always in training; the rest form 9 test windows of 320 cars") and `splits_comment` (the
   windows, the reasons and the numbers above), add a CC line to the record and a dated CHANGELOG entry, and run
   `dataset check` (SPLIT-14, SPLIT-15).

   [^mb-split14]: **SPLIT-14** (Must): "A temporal task has at least 3 windows, and no window's train side holds less
     than 50% of the data. ... A release with two windows above the floor may add one older window that trains on at
     least 40% of the rows, when most test entities recur (the actor re-rates entities it knows) and folds by entity
     would test unseen ones."
   [^mb-split15]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): "The newest window is always a test window ... The other windows are the curator's choice, per dataset,
     argued from the use case ... Every choice stays above SPLIT-14's floor; the length and the gap come from
     SPLIT-12; as many windows as an IID or grouped task of that size would get folds, then check that they are still
     meaningful (SPLIT-16 to SPLIT-18)."

   **Lennart (2026-11-11, ok):** As implemented (A).

   **Resolved (2026-11-11, Lennart):** A, as implemented: the nine windows of 320 cars, IDs 2,628 to 8,417, stay.
   SPLIT-14 as amended on 2026-11-11 admits them: the six newest train on 54.3% to 92.4% of the cars, and the three
   oldest on 46.7%, 39.1% and 31.5%, all above 30% and fewer windows under half than at or above it. They test 2,880
   cars, against 2,097 for nine windows of 233; no source gives either length. `temporal` is unchanged;
   `task_summary.split` no longer says "the first 1,000 cars are always in training" (the oldest window trains on
   1,324) and names the train sides, `splits_comment` names the nine windows by car ID, the train sides of 3,884 down
   to 1,324 cars, the three under half with their shares, the length's origin and reason, and the absent gap, and the
   outlier bullet of `curation_comments` no longer speaks of the first 1,000 cars. The record has the decision and the
   horizon CC lines. `dataset check`: 0 errors; its 2 warnings (constant and duplicated option columns) are about the
   data and not settled here (README not regenerated).
