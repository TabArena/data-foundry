# cooking_time

**Outcome:** added as `cooking_time_1m`. Under the rule on choosing test windows, rewritten on 2026-11-10, the AI
recommends keeping the three windows, the only weeks that keep half the orders for training, and stating in the splits
comment why and what they cannot test (issue 1). `dataset.py` is unchanged until you decide.

**Main points:** Keep the three weeks from 14 December 2023 to 3 January 2024, and say in the splits comment that the
score covers only the weeks before and over New Year (issue 1)?

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
     levels of `cat_5`, and on all rows the largest share is 0.5% (`cat_0`). The length (one week, TabReD's refit) and
     the one-day gap for late labels stay as they are[^split12].
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
