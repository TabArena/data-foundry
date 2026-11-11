---
unique_name: delivery_eta
name: Delivery ETA
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
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Varying Delay'
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
- https://www.kaggle.com/datasets/pcovkrd84mejm/delivery-eta
- https://github.com/yandex-research/tabred/tree/main/preprocessing#delivery-eta
notebook_path: datasets/beyond_iid/temporal/delivery_eta/delivery_eta_1m.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/delivery_eta_1m/dataset.py
source_row: 713
type_adapter_id: curation-record-v1
---

## Comments

Was downsampled/filtered by TabRed via preprocessing

CC (2026-10-19, Lennart): TabReD's quantile transform of the numeric features may be fit on all rows (undocumented); kept, with a `Potential leak, kept on purpose` note in the definition: a scaling over all rows is no strong leak and often happens in reality. It is a reason for `No` only when a strong leak is suspected or the data can be rebuilt.

CC (2026-10-21, Lennart): check SPLIT-9 on the weekly test windows and add a gap where train labels arrive late, as for nyc_taxi_trip_duration and pkdd_15 (cross-dataset review, marked ok).

**Assessment (AI, 2026-10-21):** SPLIT-9 late labels in delivery_eta_1m (order time + delivery time, from the raw file after the under-one-minute filter): 0 train orders in each of the 3 weekly windows (starts 2024-01-01 04:02, 2023-12-25 00:03, 12-18 00:02) end after the window start, because orders pause overnight and the last train order of a window is delivered 57 minutes to 6 hours before it. No gap added; the counts are in splits_comment. Script local-data-warehouse/_runs/2026-10-21_crosscut/x21-0/late_labels.py.

**Assessment (AI, 2026-10-21):** Metric declared for `delivery_eta_1m` under MET-1..13: source rmse — TabReD (Rubachev et al., ICLR 2025) scores RMSE on the log minutes.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found a related task: `lade_last_mile_delivery_eta` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-10):** priority for the review of the test windows (PR #78), which this record never had. Priority 3: gap 0, use case 0 (TabReD names the task, not who acts on it), source + (the TabReD paper), shape +, risk 0 (the 45 features that stop on 23 November 2023 are a data change, not a leak, issue 2).

CC (2026-11-10, Lennart): REVIEW issue 1 (which weeks to test), "Option B: Every other week.": the test windows are 1-7 January 2024, 18-24 December and 4-10 December 2023 instead of the last three weeks (18 December 2023 to 7 January 2024), under SPLIT-15 as amended on 2026-11-10.

CC (2026-11-10, Lennart): REVIEW issue 2, as implemented (A): the 45 features `num_76` to `num_121`, which stop being recorded on 23 November 2023 at 11:00, stay, with a `Kept on purpose` note: at each test window's prediction point a model gets what the service's own model got, and the block is still recorded for some orders of every test window, unlike anes_voting_2026's 327 dropped columns with no variation in any test year.

CC (2026-11-10, Lennart): the declared horizon (7 days, no gap, windows starting 2024-01-01, 2023-12-18 and 2023-12-04) is checked, kept: each window is one week, the length of TabReD's own validation and test periods; TabReD states no refit cadence.

**Assessment (AI, 2026-11-10):** applied in dataset.py: `temporal` with the three cutoffs; test 1,188,182, 1,485,323 and 1,444,992 orders before the 500k cap, train 15,469,869, 12,517,876 and 9,706,793 (92.9%, 75.1%, 58.3%); 0 late orders at each start (the last training order before 4 December is delivered at 22:58 on 3 December, before 18 December at 23:04, before 1 January at 21:55), so still no gap. Orders carrying `num_96` in the test windows, measured on the frame: 4,508 of 4-10 December (0.31%), 5,126 of 18-24 December (0.35%), 7,823 of 1-7 January (0.66%). The `Kept on purpose:` bullet of issue 2 is in the notes; "refit every week (TabReD)" is gone from the use case, the split and the fit reason. Horizon audit (split-auditor, model-free): TabReD (arXiv 2406.19380, its datasheet and preprocessing) trains on 20 October to 11 December, validates on 11-18 December and tests on 18-25 December 2023 and names no refit cadence (the median label delay is 5.5 minutes); one day gives 41 candidates without a source, two weeks 2 (fails SPLIT-14). `dataset check`: 0 errors, 0 warnings (README not regenerated).

## Review

**Outcome:** added as `delivery_eta_1m`. On 2026-11-10 you chose every other week as the test windows (issue 1, B:
1-7 January, 18-24 December and 4-10 December) and kept the 45 features that stop on 23 November 2023, with a note
(issue 2, A); the 7-day length stays for its reason, TabReD's own validation and test length. Nothing is left open.

**Main points:** Settled on 2026-11-10: the test weeks are 1-7 January, 18-24 December and 4-10 December (issue 1, B),
the block `num_76` to `num_121` stays with a note (issue 2, A), and the declared horizon is checked.

**Horizon:**

* **Verdict:** keep the 7-day windows (medium confidence): a week is the length of TabReD's own validation and test
  periods; no source states how often the service refits its model.
* **Length:** TabReD (Rubachev et al., ICLR 2025, https://arxiv.org/abs/2406.19380; preprocessing at
  https://github.com/yandex-research/tabred/tree/main/preprocessing) tests on one week and validates on the week
  before ("Validation and test are the last two weeks, train is the prior month": train 20 October to 11 December,
  validation 11-18 December, test 18-25 December 2023). The definition's "refit every week (TabReD)" was our wording:
  the paper, the datasheet and the scripts name no refit cadence, and no Yandex or industry source gives one (Uber's
  DeepETA post says only "Periodic auto retraining"). A delivery estimate looks minutes ahead, so the length says how
  long one fitted model serves.
* **Gap:** none needed: at every midnight no training order is still undelivered (0 late orders at all 41 daily
  cutoffs; the longest delivery takes 2.8 hours).
* **Time frame:** the release, 20 October 2023 to 7 January 2024; every eligible window lies after the change of
  23 November (issue 2), and 1-7 January is the New Year holiday week with the fewest orders.
* **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | A | One week (implemented) | 7-day windows, the length of TabReD's validation and test periods | the source's own test length; every weekday once per window | no refit cadence stated by any source |
  | B | One day | daily windows: 41 candidates above the floor | fits a daily refit, common for ETA models | no source; shorter than TabReD's test; one weekday per window |
  | C | Two weeks | 14-day windows | more orders per window | only 2 candidates above the floor, fewer than three windows |

* **Recommendation:** A: the length of the source's own test period, and no source names another. **Decision:** A, B
  or C?

**Resolved (2026-11-10, Lennart):** A, kept by the horizon audit, as instructed ("if the current time horizon makes
sense and is justifiable keep it and resolve them"); the record's CC line says the declared horizon is checked, and
the splits comment gives the reason.

**Issues for Lennart:**

1. **Which weeks should the test windows be?**

   * **Problem:**
     - The three test windows are the last three weeks (18 December 2023 to 7 January 2024), all of them holiday weeks,
       while the grocery service estimates delivery times every week.
     - Since 2026-11-10 the newest window always stays and the others are chosen from the use case and statistics of
       the data, preferring other weeks over those just before the newest[^split15].
     - The orders run from 20 October 2023 to 7 January 2024, so only five weekly windows keep half the orders for
       training (4 December onward), and other months or years are not open[^split14].
   * **Background:** On 23 November 2023 at 11:00 the data change: 45 features stop being recorded, and the deliveries
     get longer (weekly mean of the log minutes 1.62 to 1.68 before, 1.91 to 1.95 in the three weeks after); issue 2
     asks what to do about it. Every candidate window lies after the change; the
     older the window, the fewer days after the change its train side holds and the larger the drift. The two
     early-December weeks have the longest deliveries, the three holiday weeks shorter ones. PSI, the population
     stability index, compares a feature's distribution in the window with its train side; above 0.25 is usually read
     as a large shift. The new windows need no gap either: the last training order before 4 December is delivered at
     22:58 on 3 December, so no training label arrives after the window starts[^split10].
   * **Statistics:** the target from all orders; the drift from the candidate table (100,000-row samples of each
     side); 1.19M to 1.49M orders per window, of which 500,000 are tested.

     | Window | In | Mean log minutes, test | Train side | Train share | Days after the change in training | Largest drift (PSI) |
     |---|---|---|---|---|---|---|
     | 1-7 Jan | A, B | 1.778 | 1.769 | 92.9% | 38 | 2.90 |
     | 25-31 Dec | A | 1.749 | 1.772 | 84.1% | 31 | 3.67 |
     | 18-24 Dec | A, B | 1.808 | 1.767 | 75.1% | 24 | 4.22 |
     | 11-17 Dec | none | 1.954 | 1.744 | 66.9% | 17 | 5.20 |
     | 4-10 Dec | B | 1.910 | 1.720 | 58.3% | 10 | 6.35 |

   * **Effect on the task:** A ranks models on three holiday weeks, each refit at least 24 days after the change.
     B spreads the windows over the five weeks open, two weeks apart, and adds a week of the longest deliveries with a
     refit 10 days after the change, as the service would have had to make it.
   * **Consistency:** The no-gap check of 2026-10-21 in the record holds for the new windows. No dataset has chosen
     windows under the rewritten rule yet.
   * **Sources:** the definition `datasets/_dev/tabarena-v0pt2/delivery_eta_1m/dataset.py` (`splits_comment`,
     `temporal`); the record `curation/records/delivery_eta.md`; the candidate table `.venv/bin/python -m
     data_foundry.curation.cli dataset windows delivery_eta_1m --root datasets/_dev/tabarena-v0pt2` (5 weeks).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Last three weeks (implemented) | tests 1-7 Jan, 25-31 Dec and 18-24 Dec | the weeks right after a refit | three holiday weeks; nothing soon after the change |
     | B | Every other week | tests 1-7 Jan, 18-24 Dec and 4-10 Dec | the holidays and a week outside them; a refit soon after the change | the oldest window trains on 58.3% |

   * **Recommendation:** B: with five weeks open, every other week covers the holidays and the early-December weeks,
     whose deliveries are 14 to 19% longer than in the newest week. **Decision:** A or B?

   **Notes for the AI:** on B, `temporal = Temporal(on="timestamp", splits=TemporalSplits(window=7, unit="days",
   cutoffs=("2024-01-01", "2023-12-18", "2023-12-04")))`. Built on the definition's frame: test 1,188,182, 1,485,323
   and 1,444,992 orders before the 500k cap, train 15,469,869, 12,517,876 and 9,706,793 (92.9%, 75.1%, 58.3%). Then
   rewrite `task_summary.split` ("the last three weeks (18 December 2023 to 7 January 2024)") and `splits_comment`
   (the windows, the reasons and the numbers above; the no-gap sentence with the 4-December figure), add a CC line to
   the record and a dated CHANGELOG entry, and run `dataset check` (SPLIT-15). The change of 23 November is
   issue 2; under its option C only today's windows keep half the orders for training.

   [^split15]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): "The newest window is always a test window ... The other windows are the curator's choice, per dataset,
     argued from the use case ... The evidence is statistics of the data, never a model's score ... Prefer windows in
     other years, then other seasons, then other months, weeks or days, over the windows just before the newest."
   [^split14]: **SPLIT-14** (Must): at least 3 windows, and no window's train side holds less than 50% of the data.
   [^split10]: **SPLIT-10** (Should): when a label is known only some time after its row, train on the rows whose
     outcome is known by the window's start.

   **Lennart (2026-11-10, change):** Option B: Every other week.

   **Resolved (2026-11-10, Lennart):** B. `temporal` declares the cutoffs 2024-01-01, 2023-12-18 and 2023-12-04 (7
   days, no gap); `task_summary.split` and `splits_comment` name the windows, why each, the numbers and the length's
   reason (TabReD's own validation and test length; TabReD states no refit cadence), and "refit every week (TabReD)"
   is gone from the use case, the split and the fit reason. Test 1,188,182, 1,485,323 and 1,444,992 orders before the
   500k cap, train 15,469,869, 12,517,876 and 9,706,793 (92.9%, 75.1%, 58.3%). No gap is needed: 0 late orders at each
   start, and the last training order before 4 December is delivered at 22:58 on 3 December. The record has the
   decision and the horizon CC lines. `dataset check`: 0 errors, 0 warnings (README not regenerated).

2. **What to do with the 45 features that stop on 23 November 2023?**

   * **Problem:**
     - On 23 November 2023 between 11:00 and 12:00, the 45 features `num_76` to `num_121` stop being recorded: before,
       1% to 13% of the orders miss them (49% for `num_117` to `num_120`), from noon on 99.6% to 100%, to the end of
       the data.
     - In the same hour the deliveries get longer, by about 10% (mean log minutes at noon 1.88, against 1.77 to 1.79
       on the three days before), and they stay longer until mid-December.
     - Every test window lies after the cut, while 48% to 59% of the orders on its train side lie before it (77% for
       the 4 December window of issue 1), so models learn from 45 features that the test orders lack.
   * **Background:**
     - The 45 columns are one block of the published numbering, and they stop together: the share of orders missing
       `num_80`, `num_96` or `num_110` is 6% from 10:00, 82% from 11:00 and 100% from 12:00. The evening before, the
       block drops out for a few hours (`num_96` missing for 10% to 41% of the orders from 19:00 to 23:00 on
       22 November), then returns until 11:00.
     - Nothing else changes at the cut: the orders per day (about 200,000 to 230,000), the levels of `cat_0` and
       `cat_1`, the hours of the day the orders come in; no feature starts being recorded in the block's place.
     - The 0.37% of later orders that still carry the block (33,434 of 9.1M, spread over all 516 levels of `cat_1`)
       take as long as the orders before the cut (mean log minutes 1.59, against 1.86 for the other later orders and
       1.67 before the cut).
     - Before the cut, the block carries signal: `num_117` to `num_120` correlate with the target at 0.26 to 0.46,
       next only to `num_10` and `num_8` (0.59 and 0.58), and 8 of the 20 features most correlated with the target lie
       in the block.
     - The drift of issue 1's window table (largest PSI 2.9 to 6.4) is this cut: the features that drift most are all
       in the block.
   * **Effect on the task:** A model fit on a train side learns the block from the orders before the cut and predicts
     test orders that all lack it, so the score partly measures how a model handles 45 features that are missing at
     test, which methods handle differently (a tree routes missing values on its own, a network sees the imputed
     value); the block's missing values also mark the orders after the cut, as the date does.
   * **Experiments:** LightGBM (600 trees, one seed) on a random million of each train side, scored on 500,000 orders
     of the window, RMSE on the log minutes (target standard deviation 0.72 and 0.73):

     | Window | All features | Without the block | Only orders after the cut, without the block |
     |---|---|---|---|
     | 1-7 Jan | 0.5233 | 0.5269 | 0.5242 |
     | 18-24 Dec | 0.5501 | 0.5461 | 0.5538 |

     The block moves the score by under 1%, one way in the newest window and the other in 18-24 December.
   * **Consistency:** anes_voting_2026 keeps questions asked only in some election years, missing in the others
     (Lennart, 2026-10-19)[^clean8]; those return in later studies, while this block stops for good before every test
     window. No dataset has decided a feature source that stops within its history.
   * **Unknown:** whether the block's source was switched off or replaced, and whether the longer deliveries are part
     of the same change (a new dispatch, another definition of the delivery time) or of late November's conditions.
     TabReD's paper and preprocessing do not mention it, and the features are anonymised; the TabReD authors could say
     (github.com/yandex-research/tabred).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the block (implemented), add a note | the 45 features stay; a curation note describes the cut and the longer deliveries | the data as published, with the outage the service's own model met; the score moves under 1% | models are partly compared on how they handle 45 features missing at test |
     | B | Drop the block | 172 numeric features instead of 217; every order and window stays | the same features before and after the cut, as a weekly refit after the cut would use | the block's signal on the 7.4M orders before the cut is lost; the longer deliveries stay in the history |
     | C | Start the data at the cut | orders from 24 November on (9.1M of 16.7M), the block dropped | one regime of features and delivery times | 45% of the orders gone; only today's windows keep half the orders for training, so issue 1 has only its option A |

   * **Recommendation:** A: a missing value is what the deployed model saw at every test window's prediction
     point[^use3], the block moves the score by under 1%, and columns leave for what they are, not for when they were
     recorded[^clean22]; the note makes the cut visible to anyone reading the scores. **Decision:** A, B or C?

   **Notes for the AI:** on A, add a bullet to `curation_comments`: "Kept on purpose: on 23 November 2023 at 11:00 the
   45 features `num_76` to `num_121` stop being recorded (99.6% to 100% missing from noon to the end; 1% to 13%
   before, 49% for `num_117` to `num_120`), and the deliveries get longer in the same hour (mean log minutes 1.67
   before, 1.85 after); every test window lies after the cut. The cause is not published." On B, add
   `[f"num_{i}" for i in range(76, 122)]` to the drop in `_clean` (`num_101` is dropped already) and rewrite `known`
   (221 to 176 features with the time). On C, also keep the orders from `2023-11-23 12:00` on and settle issue 1 as
   its option A. In each case: a CC line in the record, a dated CHANGELOG entry, `dataset check`, and the window
   statistics again (`dataset windows delivery_eta_1m`). Measured on the raw file after the definition's filter, from
   daily and hourly counts of every column. Writing to the TabReD authors is the curator's call; nothing was sent.

   [^use3]: **USE-3** (Must): "Name the prediction point: when the model is used and what is known then."
   [^clean22]: **CLEAN-22** (Must): "Columns leave for what they are (a leak, an identifier, a copy, the measurement
     that defines the label), never for how many there are."
   [^clean8]: **CLEAN-8** (Must; narrows CLEAN-7): choosing which columns to keep by counts over the whole table (the
     most frequent codes, questions asked in one year only) is ordinary cleaning that follows the task's best practice.

   **Lennart (2026-11-10, ok):** As implemented (A).

   **Resolved (2026-11-10, Lennart):** A. The 45 features stay; `curation_comments` has the `Kept on purpose:` bullet
   of the notes, with the reason: at each test window's prediction point a model gets what the service's own model got,
   and the block is still recorded for some orders of every test window (orders carrying `num_96`: 4,508 of 4-10
   December, 0.31%; 5,126 of 18-24 December, 0.35%; 7,823 of 1-7 January, 0.66%), unlike the 327 columns
   anes_voting_2026 dropped, which have no variation in any test year. The record has the CC line. Writing to the
   TabReD authors stays your call; nothing was sent.

## Reference

TabRed
