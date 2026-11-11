# cooking_time

**Outcome:** added as `cooking_time_1m`. On 2026-11-11 you chose the newest week and every other week before it,
28 December-3 January, 14-20 December and 4-10 December (issue 2, B), with 4-10 December training on 37.5% of the
orders and signed off; this supersedes the three newest weeks of 2026-11-10 (issue 1). The 7-day length with its
one-day gap stays for its reason, TabReD's own validation and test length.

**Main points:** Settled on 2026-11-11: test every other week from the newest, 4-10 December included (issue 2, in
place of issue 1's windows); the declared horizon is checked. Nothing is left open.

**Horizon:**

* **Verdict:** keep the 7-day windows (high confidence): a week is TabReD's own validation and test length (our two
  newest windows are exactly its validation and test weeks), a week holds every weekday once, and cooking times follow
  a weekly cycle.
* **Length:** TabReD (Rubachev et al., ICLR 2025, https://arxiv.org/abs/2406.19380; preprocessing at
  https://github.com/yandex-research/tabred/tree/main/preprocessing): train 15 November to 20 December, validation
  21-27 December, test 28 December 2023 to 3 January 2024. The definition's "refit every week (TabReD)" was our
  wording; no source names a refit cadence. Friday and Saturday orders cook about 12% longer than Monday to Thursday
  (2.57-2.64 against 2.46-2.51 log minutes), more than the shift between the weekly windows, so a one-day window would
  score the weekday more than the model.
* **Gap:** one day, the rule of the ETA family (2026-10-21); the longest cooking time is 2 hours, so a 3-hour gap
  would also leave no training label unknown and keep about 240,000 to 280,000 more orders per train side.
* **Time frame:** 15 November 2023 to 3 January 2024; 11-12 December hold no orders at all, and 31 December and
  1 January about half the usual orders.
* **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | A | One week, one-day gap (implemented) | 7-day windows: 14-20 December, 21-27 December and 28 December-3 January | TabReD's own validation and test length (its two weeks are our two newest windows); every weekday once | no source names a refit cadence |
  | B | One day, a 3-hour gap | daily windows: 22 candidates | more windows to choose from | dominated by the weekday: Friday and Saturday orders cook about 12% longer, more than the shift between the weekly windows |
  | C | Two weeks | 14-day windows: 1 candidate | more orders per window | fewer than three windows |

* **Recommendation:** A: the length of the source's own validation and test periods, and a week holds every weekday
  once. **Decision:** A, B or C?

**Resolved (2026-11-10, Lennart):** A, kept by the horizon audit, as instructed ("if the current time horizon makes
sense and is justifiable keep it and resolve them"); the record's CC line says the declared horizon is checked, and
the splits comment gives the reason (TabReD's own validation and test length; a week holds every weekday once, and
cooking times follow a weekly cycle).

**Issues for Lennart:**

1. **Keep the three weeks before and over New Year as the test windows?**

   * **Problem:**
     - The three test windows are 14-20 December, 21-27 December and 28 December to 3 January, so the score measures
       the run-up to New Year and the holiday itself, while the delivery service estimates cooking times every week.
     - Since 2026-11-10 the newest window always stays and the others are chosen from the use case, preferring other
       weeks over those just before the newest, always with at least half the orders for training[^split15][^split14].
     - The orders run from 15 November 2023 to 3 January 2024, and with the one-day gap these three weeks are the only
       ones above that floor, so there is nothing else to choose.
   * **Background:** The earliest start that keeps half the orders for training is 11 December (51.9%), but the data
     hold no orders on 11 and 12 December, so a window starting then holds five days; seven-day windows that do not
     overlap can move by three days at most. Cooking times rise toward New Year: the weekly mean of the log minutes is
     2.527 to 2.532 from 16 November to 6 December, 2.548 and 2.554 in the two older windows and 2.599 in the newest,
     about 7% longer than in November. The windows cannot test an ordinary week of November or early December, nor a
     week after the holidays (the data end on 3 January). The candidate table shows 10.5 to 10.8% of test rows with a
     category the train side never shows; that comes from its 100,000-row sample of the train side against the 123,880
     levels of `cat_5`, and on all rows the largest share is 0.5% (`cat_0`). The length (one week, TabReD's validation
     and test length) and the one-day gap for late labels stay as they are[^split12].
   * **Statistics:** the target from all orders; the drift from the candidate table (100,000-row samples of each side);
     1.66M to 2.04M orders per window, of which 500,000 are tested.

     | Window | Mean log minutes, test | Train side | Train share | Largest drift (PSI) |
     |---|---|---|---|---|
     | 28 Dec-3 Jan | 2.599 | 2.537 | 84.8% | 0.19, `num_30` |
     | 21-27 Dec | 2.554 | 2.537 | 69.0% | 0.13, `num_3` |
     | 14-20 Dec | 2.548 | 2.534 | 54.2% | 0.15, `num_3` |

   * **Effect on the task:** The score says how models do in the weeks before and over New Year, when cooking times
     are longest, and not in an ordinary week; nothing in the splits comment says so today.
   * **Consistency:** No dataset has chosen windows under the rewritten rule yet. delivery_eta_1m, from the same
     release, has five weeks to choose from and gets its own proposal.
   * **Sources:** the definition `datasets/_dev/tabarena-v0pt2/cooking_time_1m/dataset.py` (`splits_comment`,
     `temporal`); the record `curation/records/cooking_time.md` (the gap, 2026-10-21); the candidate table
     `.venv/bin/python -m data_foundry.curation.cli dataset windows cooking_time_1m --root datasets/_dev/tabarena-v0pt2`
     (3 weeks).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep, comment as is (implemented) | the three weeks; the comment calls them the last three weeks | no change | gives no reason for the windows and no limit |
     | B | Keep, state why and the limit | the same windows; the comment says they are the only weeks above the floor and cover the weeks before and over New Year | the reasons and numbers are in the definition | text only, the windows stay December |

   * **Recommendation:** B: there is no other choice of windows, and the comment should say so and what the score
     covers. **Decision:** A or B?

   **Notes for the AI:** on B, the declaration stays `TemporalSplits(window=7, unit="days", n_windows=3, gap=1)`; as
   cutoffs it is `cutoffs=("2023-12-28", "2023-12-21", "2023-12-14")`, which builds the same splits (test 1,662,794,
   2,040,512 and 1,921,331 orders before the 500k cap, train 10,856,304, 8,832,570 and 6,935,762, so 84.8%, 69.0% and
   54.2%). Add to `splits_comment` that these are the only weekly windows above the 50% floor (the earliest start that
   keeps it is 11 December, and 11-12 December hold no orders) and that all three lie in the weeks before and over New
   Year; add a CC line to the record and a dated CHANGELOG entry, and run `dataset check` (SPLIT-14, SPLIT-15).

   [^split15]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): "The newest window is always a test window ... The other windows are the curator's choice, per dataset,
     argued from the use case ... Prefer windows in other years, then other seasons, then other months, weeks or days,
     over the windows just before the newest ... Every choice stays above SPLIT-14's floor ... The splits comment names
     the windows, the reasons and the numbers they rest on."
   [^split14]: **SPLIT-14** (Must): at least 3 windows, and no window's train side holds less than 50% of the data.
   [^split12]: **SPLIT-12** (Should): the horizon is a human judgment from the source, such as the refit cadence.

   **Lennart (2026-11-10, change):** Option B: Keep, state why and the limit.

   **Resolved (2026-11-10, Lennart):** B. The windows stay; `temporal` now declares them as the cutoffs 2023-12-28,
   2023-12-21 and 2023-12-14 (7 days, one-day gap), which build the same splits. `splits_comment` says they are the
   only weekly windows above the 50% floor (the earliest start that keeps it is 11 December, and 11-12 December hold no
   orders), that all three lie in the weeks before and over New Year, and the length's reason (TabReD's own validation
   and test length; a week holds every weekday once, and cooking times follow a weekly cycle); "refit every week
   (TabReD)" is gone from the use case, the split and the fit reason, and the Background above no longer calls the week
   TabReD's refit. Test 1,662,794, 2,040,512 and 1,921,331 orders before the 500k cap, train 10,856,304, 8,832,570 and
   6,935,762 (84.8%, 69.0%, 54.2%). The record has the decision and the horizon CC lines. `dataset check`: 0 errors,
   0 warnings (README not regenerated).

2. **Test every other week, now that the amended floor opens early December?**

   * **Problem:**
     - Issue 1 kept the three weeks from 14 December 2023 to 3 January 2024 because they were the only weeks whose
       train side held half the orders; the floor amended on 2026-11-11 admits further windows down to 30%[^ck2-14].
     - 4-10 December now qualifies (37.5% of the orders for training), a full week with orders on every day, before the
       holiday run-up that all three of today's windows lie in.
     - For delivery_eta_1m, from the same TabReD release family, you chose every other week on 2026-11-10.
   * **Background:** the earliest weeks are short: 30 November-6 December trains on 28.9%, under the bound, and the weeks
     from 5 December lose orders to the empty 11-12 December. Cooking times rise toward New Year (mean log minutes 2.548,
     2.554 and 2.599 in today's windows against 2.527 to 2.532 from 16 November to 6 December).
   * **Options:**

     | | Option | What it does | Test windows | Pro | Con |
     |---|---|---|---|---|---|
     | A | The three newest weeks (implemented) | 28 December-3 January, 21-27 December, 14-20 December (84.8%, 69.0%, 54.2%) | 3 windows of 1.66M to 2.04M orders (500,000 tested each) | every train side above half; your call of 2026-11-10 | all three in the holiday run-up |
     | B | Every other week | 28 December-3 January, 14-20 December, 4-10 December (84.8%, 54.2%, 37.5%) | 3 windows of 1.66M to 1.92M orders (500,000 tested each) | a week before the run-up; decides cooking like delivery_eta_1m | the oldest trains on 37.5% |

   * **Recommendation:** B: it adds the one week before the holiday run-up the data holds, as for delivery_eta_1m.
     **Decision:** A or B?

   **Notes for the AI:** on B, `temporal = Temporal(on="timestamp", splits=TemporalSplits(window=7, unit="days",
   cutoffs=("2023-12-28", "2023-12-14", "2023-12-04"), gap=1))`: test 1,662,794, 1,921,331 and 1,861,029 orders before
   the 500k cap, train 10,856,304, 6,935,762 and 4,797,156 (84.8%, 54.2%, 37.5%). Then
   rewrite `task_summary.split` and `splits_comment` (the windows, the 37.5% window named with its share, the reason),
   a CC line, a dated CHANGELOG entry and `dataset check`.

   [^ck2-14]: **SPLIT-14** (Must; amended 2026-11-11, Lennart): the newest window and at least one other train on at
     least 50% of the data; further windows down to 30%, and at most as many under 50% as at or above.

   **Lennart (2026-11-11, change):** Option B: Every other week.

   **Resolved (2026-11-11, Lennart):** B: the test windows are the newest week and every other week before it,
   28 December-3 January, 14-20 December and 4-10 December. This supersedes issue 1's decision of 2026-11-10 (the
   three newest weeks), which stays resolved; the 7-day length and the one-day gap stay. `temporal` declares the
   cutoffs 2023-12-28, 2023-12-14 and 2023-12-04 (7 days, gap 1 day): test 1,662,794, 1,921,331 and 1,861,029 orders
   before the 500k cap, train 10,856,304, 6,935,762 and 4,797,156 (84.8%, 54.2%, 37.5%). 4-10 December is the one
   window under half, signed off: `accepted_check_warnings` accepts `splits_train_under_half`. Every day of it holds
   orders, and its mean log minutes (2.533) sit below the run-up's 2.548 and New Year's 2.599. `task_summary.split`
   and `splits_comment` (the windows and why, the counts, the shares, the gap figures for the new windows) are
   rewritten. The record has the decision CC line. `dataset check`: 0 errors, 0 warnings (README not regenerated).
