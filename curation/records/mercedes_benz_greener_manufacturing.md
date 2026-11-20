---
unique_name: mercedes_benz_greener_manufacturing
name: Mercedes_Benz_Greener_Manufacturing
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
priority: 3
decision_markers:
- Anonymized
tags:
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Inferred'
- 'Target: Later'
- Database Snapshot
collections:
- TabArena Reject
- TabSTAR
original_source: Kaggle
year: '2017'
collection_period: Unknown
domain: industry & manufacturing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/mercedes-benz-greener-manufacturing
- https://www.openml.org/search?type=data&id=42570
notebook_path: datasets/beyond_iid/temporal/mercedes_benz_greener_manufacturing/mercedes_benz_greener_manufacturing.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/mercedes_benz_greener_manufacturing/dataset.py
source_row: 708
type_adapter_id: curation-record-v1
---

## Comments

CC: "Using the index as a feature was predictive in the competition, might require a temporal split. But in general an interesting dataset, likely has groups of cars as multiple configurations could include the same car? Need to assess the impact of index as feature"

CC (2026-10-06, Lennart): Kept as a fine task after the task-probe review (flag `no_spread`: untuned skills +0.55 to +0.57; `X314` alone +0.39). Tuned methods spread: on BeyondArena TabPFN-2.6 reaches R^2 0.614, the median method 0.600 and the weakest about 0.47, with 10 of 29 methods tied with the best over the 9 windows of 320 test rows.

CC (2026-10-21, Lennart): CLEAN-11 amended: a row whose target the source names as not the task's quantity, or a single extreme target in the training period only, may leave, with the source's words.

**Assessment (AI, 2026-10-21):** the dropped testing time (265.3 s against a next highest of 169.9 s; mean 100.7, sd 12.7) is car 883 of 4,209 in ID order, inside the first 1,000 cars every test window trains on, so it meets the clause for a single extreme target in the training period only. The competition host does not name it, so no source's words exist; the reason is now in curation_comments.

CC (2026-10-21, Lennart): the declared metric documents the original use case's metric; overrule it only when it is biased or wrong (evidence from the paper); keep the note of the original metric (TP-6 amended).

**Assessment (AI, 2026-10-21):** metric set to `r2`, the competition's metric (Kaggle API: "R^2 score (coefficient of determination)"; was the default RMSE); within one test fold R² ranks models as RMSE does. Needs a rebuild to reach the container.

CC (2026-10-21, Lennart): "no it also bind to what experts did by default, so again more complicated case by case": CLEAN-11 amended again: a single extreme target in the training period may leave with the source's words or where experts of the field drop such a value by default, decided case by case. The one testing time of 265.3 s leaves as the experts' default for a single extreme time.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source r2 — the competition's R^2 (Kaggle evaluation page).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found a related task: `bosch_production_line_performance` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-10):** priority for the review of the test windows and horizons, which this record never had. Priority 3: gap 0, use case 0, source + (Mercedes-Benz's competition), shape +, risk 0 (the open issue is the window size and the floor).

CC (2026-11-11, Lennart): REVIEW issue 1 (which windows of cars to test), as implemented (A): the nine windows of 320 cars in ID order, from ID 2,628 on, stay, in place of the AI's nine windows of 233 cars over the newest half; SPLIT-14 as amended on 2026-11-11 admits the three oldest, which train on 46.7%, 39.1% and 31.5% of the cars (three windows under half, six at or above it).

CC (2026-11-11, Lennart): the declared horizon (320 cars, no gap, windows starting at the newest nine runs of 320 cars, IDs 7,801, 7,140, 6,487, 5,875, 5,223, 4,581, 3,920, 3,308 and 2,628) is checked, as the amended floor admits nine windows of 320, which test 2,880 cars against 2,097 at 233, and no source gives either length.

**Assessment (AI, 2026-11-11):** applied in dataset.py: `temporal` unchanged (`window=320, unit="rows", n_windows=9`); test 320 cars each, train 3,884, 3,564, 3,244, 2,924, 2,604, 2,284, 1,964, 1,644 and 1,324 (92.4%, 84.8%, 77.2%, 69.6%, 61.9%, 54.3%, 46.7%, 39.1%, 31.5% of 4,204). `task_summary.split` no longer says the first 1,000 cars are always in training (the oldest window trains on 1,324); `splits_comment` replaces the `TimeSeriesSplit` description with the windows by car ID, the train sides, the three under half with their shares, the length's origin (the first curation's `TimeSeriesSplit` arithmetic) and the reason it is kept, and the absent gap; the outlier bullet no longer names the first 1,000 cars. `dataset check`: 0 errors, 2 warnings that predate this change (11 constant and 45 duplicated option columns; README not regenerated).

CC (2026-11-17, Andrej): the declared split (temporal on `time_index`, windows of 320 rows, 9 windows, no gap) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split review, cross-dataset item).

CC (2026-11-19, Andrej): `time_index` stays a model input (Review issue 2, A as implemented): the car's ID exists before its bench test, so the planner holds it at prediction time.

CC (2026-11-19, Andrej): nine windows of 233 cars, all training on half the cars or more (320 rows was leftover arithmetic) (Review issue 3).

## Review

**Outcome:** added. On 2026-11-11 you kept the nine windows of 320 cars from ID 2,628 on (issue 1 and the horizon,
A), which the amended floor admits with the three oldest training on 46.7%, 39.1% and 31.5% of the cars.

**Main points:** Issue 2: Keep `time_index` as a model input? Settled on 2026-11-11: the nine windows of 320 cars stay (issue 1, A), and the declared length of
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

2. **Keep `time_index`, a reconstructed order, as a model input?**

   * **Problem:**
     - `time_index` is the car's ID read as its place in the testing sequence; it orders the temporal split and is a model input by default.
     - california_house_prices_2020, labour_inspection_compliance and wine_quality keep their reconstructed order out of the inputs (`feature=False`), because the actor does not hold it when predicting[^lk-2].
     - Here the actor does: a car's ID exists before its bench test, so the planner who estimates the test time holds it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as input (implemented) | `time_index` stays a feature | the actor holds it; a model can use a trend over time | the test windows lie beyond the training range of the index, where a trend extrapolates poorly |
     | B | Split order only (`feature=False`) | `time_index` orders the windows and is dropped from the inputs | no model leans on an artificial index | drops what the actor holds at prediction |

   * **Recommendation:** A. **Decision:** A or B?

   **Notes for the AI:** on B, declare `Temporal(..., feature=False)` (the time-column-as-split-metadata change of #98) and add a CC line.

   **Andrej (2026-11-19, ok):** As implemented (A).

   **Resolved (2026-11-19, Andrej):** A, as implemented: `time_index` stays a model input, as the planner holds a car's ID before its bench test.

   [^lk-2]: **LEAK-10** (Must): every feature has to have existed, and be held by the actor, at the prediction time of its row; a time column that only orders the split is declared no input.

3. **Train floor: keep the windows under half the data as the curator's exception, or drop them?**

   * **Problem:**
     - The three oldest windows train on 46.7%, 39.1% and 31.5% of the cars, beside six on 54.3% to 92.4%.
     - Since 2026-11-19, every window trains on at least half the data, and a window under half is the curator's exception for the dataset, down to 30%[^split14]; the sign-off (Lennart, 2026-11-11, review issue 1, A) was given under the earlier rule, which admitted such windows beside two at half or more.
     - The definition has 9 windows; the target an IID split would get[^split33] for 4,204 rows is 9; without the windows under half it keeps 6.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the windows as the curator's exception (implemented) | The accepted warning is reworded to the new rule; split unchanged | Keeps the periods they test, as signed off; more windows toward the target | They train on less than half the data |
     | B | Drop the windows under half | The windows under half leave the declaration; a rebuild | Every window trains on half the data or more | 3 fewer windows and the periods they test |

   * **Recommendation:** A, the sign-off's reason (periods or test rows the newest windows lack) still holds, and no window is under 30%. **Decision:** A or B?

   **Notes for the AI:** on A, reword the `splits_train_under_half` acceptance (drop "SPLIT-14's two tiers admit it", name the curator's exception and this decision) and add a CC line; on B, remove the windows from the declaration, rebuild, and update the splits comment.

   **Andrej (2026-11-19, discuss):** How exactly are the splits done? Could we reduce the window sizes while staying compliant with the use case and get to more than 50% on each train split?

   **Answer (AI, 2026-11-19):** Yes: nine windows of 233 cars fill the newest half exactly, every train side keeps 50.1% or more, and nothing in the use case ties the length.

   * **How the split is done today:** `TemporalSplits(window=320, unit="rows", n_windows=9)` on `time_index` (the car ID, the only order): nine runs of 320 cars walking back from the newest, step 320, no gap, each train side every earlier car. Scored unit: the car (4,204).

     | Window (car IDs) | Test cars | Train | Train share |
     |---|---|---|---|
     | 7,801-8,417 | 320 | 3,884 | 92.4% |
     | 7,140-7,798 | 320 | 3,564 | 84.8% |
     | 6,487-7,139 | 320 | 3,244 | 77.2% |
     | 5,875-6,486 | 320 | 2,924 | 69.6% |
     | 5,223-5,873 | 320 | 2,604 | 61.9% |
     | 4,581-5,221 | 320 | 2,284 | 54.3% |
     | 3,920-4,579 | 320 | 1,964 | 46.7% |
     | 3,308-3,919 | 320 | 1,644 | 39.1% |
     | 2,628-3,306 | 320 | 1,324 | 31.5% |

   * **What the use case and the source fix:** nothing. The competition ships no dates and held its test cars out at random; 320 is the arithmetic of the first curation's `TimeSeriesSplit`, not a horizon (signed off 2026-11-11 as such). No gap is needed (a car's time is known when it leaves the bench). Our assumption: the car ID is the order of testing.
   * **The floor:** half the cars come before ID 4,230 (the 2,108th car), so nine windows above half can hold at most 233 cars each (2,102 open cars / 9).
   * **Shorter layouts above half,** no gap, target 9 windows:

     | Layout | Windows (car IDs) | Test cars | Train shares |
     |---|---|---|---|
     | B: 320 cars, drop the three (the issue's B) | 4,581-8,417 in six runs | 6 x 320 = 1,920 | 54.3% to 92.4% |
     | C: 233 cars | 4,230-8,417 in nine runs (oldest 4,230-4,699) | 9 x 233 = 2,097 | 50.1%, 55.7%, 61.2%, 66.8%, 72.3%, 77.8%, 83.4%, 88.9%, 94.5% |

     - C is issue 1's B of 2026-11-11, recounted on today's definition (same windows). 280 cars would give seven windows above half (53.4% to 93.3%).

   **Recommendation:** C: no source ties the length, and 233 cars give the nine windows a task of this size aims at, all above half, at 783 fewer test cars than today. **Decision:** A, B or C?

   **Andrej (2026-11-19, discuss):** Agree.

   **Resolved (2026-11-19, Andrej):** C. `TemporalSplits(window=233, unit="rows", n_windows=9)`: nine windows of 233 cars by car ID, training on 50.1% to 94.5% (2,097 test cars); the under-half acceptance is gone. `dataset check`: 0 errors (two column warnings, unrelated). Not rebuilt.

   [^split14]: **SPLIT-14** (Must): every window trains on at least half the data, lower only as the curator's exception down to 30%; every test window holds at least 33 scored units.

   [^split33]: **SPLIT-33** (Should): an IID or grouped split gets 3-fold cross-validation with 20, 10, 3 or 1 repeats by the units on its train side; SPLIT-15 aims a temporal split at the same count.

## Reference

https://www.kaggle.com/competitions/mercedes-benz-greener-manufacturing
