# lending_club

**Outcome:** added. Under the rule on choosing test windows, rewritten on 2026-11-10, the AI proposes to keep the
newest quarter (October to December 2015) and April to June, and to replace July to September with January to March
2015, so the three windows spread over the one year that keeps half the loans for training (issue 1). The quarterly
horizon is kept. `dataset.py` is unchanged until you decide.

**Main points:** Test on 2015 Q4, Q2 and Q1 instead of Q4, Q3 and Q2 (issue 1)? Sign off the one-quarter horizon.

**Horizon:**

* **Verdict:** keep the three-month windows (medium confidence): LendingClub released its loan files by calendar
  quarter, the paper we start from uses random folds and states no horizon, and no refit cadence was found.
* **Length:** declared as 3 months, "a model that is refit every quarter" (`splits_comment`). Sanz-Guerrero and Arroyo
  (2025, https://arxiv.org/abs/2401.16458) shuffle the loans and use 5-fold cross-validation ("The dataset is shuffled
  to eliminate biases derived from its original ordering"), so the source gives no horizon. LendingClub's files held
  "complete loan data for all loans issued through the previous completed calendar quarter" (its file description, as
  copied in https://rdrr.io/cran/creditmodel/man/lendingclub.html), while `splits_comment` says the data was updated
  monthly; LendingClub's own refit cadence: none found (the paper, the archived file descriptions, a web search). The
  quarter is a convention that matches the quarterly files, not a stated cadence.
* **Gap:** none, by your recorded exception of 2026-10-21: a loan's outcome comes up to 36 months after issue and the
  data has no outcome dates, and a 12-month gap would leave 33-46% of the rows for training.
* **Time frame:** 36-month loans issued from April 2008 to December 2015 (609,544), the only loans whose outcomes are
  complete in the 2018 Q4 snapshot. 46% of the loans were issued in 2015, so only its four quarters keep half the rows
  for training (2015 Q1: 53.9%). In 2015 Q4, 14 new credit-bureau fields (`all_util`, `inq_fi`, `open_acc_6m`, ...)
  appear, filled on 17% of its loans and missing on every loan of the earlier quarters of 2015.
* **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | A | Three months (implemented) | quarterly windows, no gap (your exception of 2026-10-21): 4 candidates above the floor, the quarters of 2015 | matches LendingClub's quarterly loan files | a convention, not a stated cadence |
  | B | One month | 12 candidates, January to December 2015, 16,000 to 33,000 loans each | would match the "updated monthly" reading of `splits_comment` | no source either; fewer loans per window |
  | C | Six months | 2 candidates: 2015 H2 (73.4% train share) and H1 (53.9%) | more loans per window | fewer than three windows |
  | D | One year | 2015 alone | all of 2015 in one window | one candidate, fewer than three windows |

* **Recommendation:** A: the quarter matches the files LendingClub released by calendar quarter, and no source names
  another cadence. **Decision:** A, B, C or D?

**Issues for Lennart:**

1. **Which quarters of 2015 should the test windows be?**

   * **Problem:**
     - The three test windows are 2015 Q2, Q3 and Q4, walking back from the newest, and 2015 Q1 is the only other
       quarter that keeps half the loans for training (53.9%).
     - Since 2026-11-10 the newest window always stays and the others are chosen from the use case and statistics of
       the data, preferring other seasons and months over the windows just before the newest[^lc-split15].
     - Other years are not open, since 46% of the loans were issued in 2015[^lc-split14].
   * **Background:** Each quarter is a season of 2015, so today's windows cover three seasons and B covers three as
     well, with winter in place of summer. The default rate barely moves across the four quarters (14.6% to 15.4%),
     and the train sides sit at 13.2% to 13.8%. The three older quarters show little drift (median PSI 0.02 to
     0.04); the newest is set apart by the 14 bureau fields that start in it (median PSI 0.45). PSI, the population
     stability index, compares a feature's distribution in the window with its train side; above 0.25 is usually read
     as a large shift; a few bureau-history columns (`num_bc_tl` and others) drift by 0.8 to 1.1 in each of the three
     older quarters.
   * **Statistics:** from the candidate table (100,000-row samples of each side for the drift).

     | Window | In | Loans | Default rate, test | Default rate, train side | Train share | Median PSI | Largest PSI |
     |---|---|---|---|---|---|---|---|
     | Oct-Dec 2015 | A, B | 88,667 | 14.8% | 13.8% | 85.5% | 0.445 | 1.28 (`all_util`) |
     | Jul-Sep 2015 | A | 73,567 | 14.6% | 13.5% | 73.4% | 0.023 | 0.78 (`num_bc_tl`) |
     | Apr-Jun 2015 | A, B | 64,222 | 15.4% | 13.3% | 62.8% | 0.027 | 0.92 (`num_bc_tl`) |
     | Jan-Mar 2015 | B | 54,324 | 14.9% | 13.2% | 53.9% | 0.037 | 1.10 (`num_bc_tl`) |

   * **Effect on the task:** A tests the loans of April to December 2015, each with a model refit on everything up to
     the quarter before. B tests October to December, April to June and January to March, so one model is refit on
     2008-2014 alone, before the 2015 volume arrived, and the windows are spread over the whole open year instead of
     its last nine months.
   * **Consistency:** Your CC of 2026-10-01 recorded the windows as "the quarters 2015 Q2-Q4" when the 2016 loans were
     dropped; B departs from that wording, which predates the rewritten rule. The exception for gap 0 holds for both
     options; under B its numbers change (a 12-month gap would leave 28-46% of the rows for training)[^lc-split10].
   * **Sources:** the definition `datasets/_dev/tabarena-v0pt2/lending_club/dataset.py` (`splits_comment`,
     `temporal`); the record `curation/records/lending_club.md` (CC 2026-10-01, the exception of 2026-10-21); the
     candidate table `.venv/bin/python -m data_foundry.curation.cli dataset windows lending_club --root
     datasets/_dev/tabarena-v0pt2` (4 quarters); the bureau fields counted on the definition's frame.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | 2015 Q4, Q3 and Q2 (implemented) | tests Oct-Dec, Jul-Sep and Apr-Jun 2015 | the most training data (oldest 62.8%); the windows of your CC of 2026-10-01 | walks back from the newest; no window in the first months of the year |
     | B | 2015 Q4, Q2 and Q1 | tests Oct-Dec, Apr-Jun and Jan-Mar 2015 | spread over the whole open year; no window right before the newest; adds winter | the oldest trains on 53.9%, with no 2015 loan |

   * **Recommendation:** B, with low stakes: the statistics barely tell the quarters apart, so the choice follows the
     rule's default of spreading the windows over the eligible history rather than taking the quarter just before the
     newest. **Decision:** A or B?

   **Notes for the AI:** on B, `temporal = Temporal(on="issue_d", splits=TemporalSplits(window=3, unit="months",
   cutoffs=("2015-10-01", "2015-04-01", "2015-01-01")))`: test 88,667, 64,222 and 54,324 loans, train 520,877,
   383,088 and 328,764 (85.5%, 62.8%, 53.9%). Then rewrite `task_summary.split` ("Each of the last three quarters of
   2015"), `splits_comment` (the windows, the reasons and the numbers above; the exception's gap figures: a 36-month
   gap and a 12-month gap recomputed for the new windows, 12 months now 28-46%), add a CC line to the record and a
   dated CHANGELOG entry, and run `dataset check` (SPLIT-15). On A, write the reason for walking back into
   `splits_comment` and the record.

   [^lc-split15]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): "The newest window is always a test window ... Prefer windows in other years, then other seasons, then
     other months, weeks or days, over the windows just before the newest. Walking back from the newest is one choice
     among others and needs its reason too, such as a history too short for others, or a use case that only cares
     about the weeks after a refit."
   [^lc-split14]: **SPLIT-14** (Must): at least 3 windows, and no window's train side holds less than 50% of the data.
   [^lc-split10]: **SPLIT-10** (Should): when a label is known only some time after its row, train on the rows whose
     outcome is known by the window's start; the exception of 2026-10-21 (Lennart) sets gap 0 because the label's
     delay would break the 50% floor.
