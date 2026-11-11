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
collections:
- TabArena Reject
- TabSTAR
original_source: Kaggle
year: '2017'
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

CC (2026-11-11, Andrej): BeyondArena v0.2 review page, mercedes_benz_greener_manufacturing:
- Issue 2, B: `X3`, `X6` and `X8` are restored; only `X4`, `X5` and `X11` stay dropped. A check of 2026-11-06 found no time pattern in the three (Cramér's V against the ID decile 0.176, 0.055 and 0.086, close to the kept `X0` to `X2` and far from `X5` at 0.928; no level confined to a part of the ID range) and no measurable gain or loss (R² +0.0015, standard error 0.0039). Columns leave for what they are, not for being unexplained.
- Issue 1 (the test windows) is open again: the mark of the review page chose nine windows of 233 cars in the newest half, which the resolution of the same day replaced by the nine windows of 320. The mark was given against the floor as it read before its amendment of 2026-11-11, which now names this dataset's 31.5% window as one to keep, so the definition is unchanged and the Review asks which stands.

## Review

**Outcome:** added. On 2026-11-11 you kept the nine windows of 320 cars from ID 2,628 on (issue 1 and the horizon,
A), which the amended floor admits with the three oldest training on 46.7%, 39.1% and 31.5% of the cars.

**Main points:** Settled on 2026-11-11: the nine windows of 320 cars stay (issue 1, A), and the declared length of
320 cars without a gap is checked: no source gives a length, and 320 tests 2,880 cars where 233 would test 2,097. A second
mark of 2026-11-11, from a parallel review of the same question, chose nine windows of 233 cars instead; issue 1 asks
which stands. Issue 2, new on 2026-11-11, restores `X3`, `X6` and `X8` and is resolved.

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

**Issues for the curator:**

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

   **Andrej (2026-11-11, change):** Option C: 9 windows of 233 cars in the newest half.

   **Answer (AI, 2026-11-11):** the mark chooses what the resolution above replaced the same day, so it is not
   applied here; the question is reopened as issue 3, with the floor's amendment of 2026-11-11 as the new
   fact. The definition is unchanged.

2. **Restore `X3`, `X6` and `X8`?**

   * **Problem:**
     - Of the eight coded categories the definition keeps `X0`, `X1` and `X2`, drops `X5` as a time marker and `X4` as
       near constant, and drops `X3`, `X6` and `X8` "to be safe", as nothing is known about them and `X8` "seems" drawn
       from all rows.
     - A check of 2026-11-06 finds no time pattern in the three and no gain or loss from them.
     - Keep them dropped, or restore them?
   * **Background:** columns leave for what they are (a leak, an identifier, a copy, the measurement that defines the
     label), and a fix rests on a test, not an argument; what has no such reason stays, with a note[^mb2a].
   * **Experiments:** the check on the competition's file:
     - Strength of the link between each code and the ID decile (Cramér's V, 0 none, 1 complete; shuffled IDs in
       brackets): `X5` 0.928 (0.080), and each of its 24 levels with five or more cars lies within 20% of the ID range;
       `X3` 0.176 (0.047), `X6` 0.055 (0.050), `X8` 0.086 (0.076), close to the kept `X0` to `X2` (0.108 to 0.138
       against 0.078 to 0.106); no level of `X3`, `X6` or `X8` is confined to a part of the ID range, and each `X8`
       level spans the IDs from the first to the last hundred.
     - R² on the 9 shipped windows (untuned LightGBM, 3 seeds): adding `X3`, `X6` and `X8` changes it by +0.0015
       (standard error 0.0039, better in 6 of 9); adding `X5` by -0.012 (standard error 0.006, better in 2 of 9), the
       drop the definition makes for a reason.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep them dropped (implemented) | five coded categories dropped | no change | three columns of the car's configuration leave without a reason found |
     | B | Restore `X3`, `X6` and `X8` | three categorical columns back; `X4` and `X5` stay dropped | the source's columns where no reason to drop them is found; the test is written into the notes | three anonymised codes nobody can explain |

   * **Recommendation:** B: the check finds neither a time marker nor a leak in them. **Decision:** keep dropped (A)
     or restore (B)?

   **Notes for the AI:** on B, remove `X3`, `X6`, `X8` from the drop list in `_clean` (they are categorical through
   `_feature_types`), replace the notes' bullet on them with the check's numbers, re-run `dataset check`.

   [^mb2a]: **CLEAN-22** (Must): columns leave for what they are (a leak, an identifier, a copy, the measurement that
     defines the label), never for how many there are. The curator's standing preference (Andrej): fix what lets a
     model tell the outcome for reasons other than the task, tested, not argued; keep and document the rest.

   **Andrej (2026-11-11, change):** Option B: Restore X3, X6 and X8.

   **Resolved (2026-11-11, Andrej):** B: `X3`, `X6` and `X8` removed from the drop list in `_clean` (categorical
   through `_feature_types`); only `X4`, `X5` and `X11` stay dropped. The notes' bullet on them now gives the check's
   numbers, and the task summary says six coded categories and no longer names "other coded categories of unknown
   meaning". `dataset check`: 0 errors; its 2 warnings (11 constant and 45 duplicated option columns) are about the
   data and are not settled here. This issue was raised in a parallel review of the same dataset and is carried over
   here with its number, since this review had none.

3. **Keep the nine windows of 320 cars, or move to nine of 233 in the newest half?**

   * **Problem:**
     - The floor rule was amended on 2026-11-11 and now names this dataset's 31.5% window as one the curator kept, so
       the reason the 233-car windows were recommended for ("none training on less than half") no longer holds[^mb3a].
     - The two marks are of the same date on two reviews of the same dataset: the one in this record (A, as
       implemented) and one in a parallel review whose issue 1 was resolved C, nine windows of 233 cars in the newest
       half.
     - The definition still has the nine windows of 320 cars, with the `splits_train_under_half` warning accepted on
       the resolution of issue 1.
   * **Background:** the parallel review's issue 1 quoted the floor in its pre-amendment wording ("at least 3
     windows, none training on less than half of the data"); the amended rule allows further windows down to 30%, with
     at most as many under 50% as at or above it, and asks for the curator's sign-off, which the record's CC line
     carries.
   * **Experiments:** the earlier check in that review (untuned LightGBM, 3 seeds, R²): 0.570 over the nine shipped
     windows of 320, 0.567 over the six newest, 0.580 over nine windows of 233 in the newest half; the scores do not
     decide between them.
   * **Statistics:**

     | Windows | Test cars | Train sides | Under 50% |
     |---|---|---|---|
     | 9 of 320 (implemented) | 2,880 | 1,324 to 3,884 cars (31.5% to 92.4%) | 3 (46.7%, 39.1%, 31.5%) |
     | 9 of 233, newest half | 2,097 | 2,107 to 3,971 cars (50.1% to 94.5%) | 0 |
     | 6 of 320 | 1,920 | 2,284 to 3,884 cars (54.3% to 92.4%) | 0 |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the nine windows of 320 (implemented) | nothing changes; the accepted warning and the CC line stay | the amended floor admits them, and names this dataset; 2,880 test cars | three windows train on 31.5% to 46.7% of the cars |
     | B | Nine windows of 233 in the newest half | `TemporalSplits(window=None, unit="rows", n_windows=9, min_train_fraction=0.5)` with `horizon=233, horizon_unit="steps"`; the accepted warning and the sign-off leave | every train side keeps at least 50.1%; about one block of the dropped `X5` code per window | 2,097 test cars; each window's R² rests on 233 cars; undoes a resolution of the same day |

   * **Recommendation:** A: the mark for the 233-car windows was given against the floor as it read before
     2026-11-11, and the amendment that followed names this dataset's own window as one to keep. **Decision:** A or B?

   **Notes for the AI:** on B, `temporal = Temporal(on="time_index", splits=TemporalSplits(window=None, unit="rows",
   n_windows=9, min_train_fraction=0.5), horizon=233, horizon_unit="steps")`, the `accepted_check_warnings` entry for
   `splits_train_under_half` removed, `task_summary.split` and `splits_comment` rewritten to the nine windows of 233
   cars (train sides 2,107 to 3,971), a CC line in the record and `dataset check`. On A, nothing changes.

   [^mb3a]: **SPLIT-14** (Must; amended 2026-11-08 and 2026-11-11): the newest window and at least one other train on
     at least 50% of the data, further windows may train down to 30%, at most as many under 50% as at or above it,
     each with the curator's sign-off in a CC line. Its reason names "mercedes_benz_greener_manufacturing (31.5%)" as
     a window a flat 40% floor would lose.

## Reference

https://www.kaggle.com/competitions/mercedes-benz-greener-manufacturing
