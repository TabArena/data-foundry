# delivery_eta

**Outcome:** added as `delivery_eta_1m`. Under the rule on choosing test windows, rewritten on 2026-11-10, the AI
proposes to keep the newest week (1-7 January 2024) and 18-24 December, and to replace 25-31 December with 4-10
December 2023, so the windows are two weeks apart and one lies outside the holidays (issue 1). `dataset.py` is
unchanged until you decide.

**Main points:** Test on 1-7 January, 18-24 December and 4-10 December instead of the last three weeks (issue 1)?

**Issues for Lennart:**

1. **Which weeks should the test windows be?**

   * **Problem:**
     - The three test windows are the last three weeks (18 December 2023 to 7 January 2024), all of them holiday weeks,
       while the grocery service estimates delivery times every week.
     - Since 2026-11-10 the newest window always stays and the others are chosen from the use case and statistics of
       the data, preferring other weeks over those just before the newest[^split15].
     - The orders run from 20 October 2023 to 7 January 2024, so only five weekly windows keep half the orders for
       training (4 December onward), and other months or years are not open[^split14].
   * **Background:** On 23 and 24 November 2023 the data change: `num_96` goes from 1.8% to 99.7% missing, 31 of the
     217 numeric features move by more than half a standard deviation between the two weeks before and the two weeks
     after (3 between two earlier fortnights of November), and the deliveries get longer (weekly mean of the log minutes
     1.62 to 1.68 before, 1.91 to 1.95 in the three weeks after). The anonymised features do not tell whether the
     conditions changed (weather, demand) or the data collection. Every candidate window lies after the change; the
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
   the record and a dated CHANGELOG entry, and run `dataset check` (SPLIT-15). The change of 23-24 November is not
   noted in `curation_comments`; whether it needs a note is a separate question.

   [^split15]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): "The newest window is always a test window ... The other windows are the curator's choice, per dataset,
     argued from the use case ... The evidence is statistics of the data, never a model's score ... Prefer windows in
     other years, then other seasons, then other months, weeks or days, over the windows just before the newest."
   [^split14]: **SPLIT-14** (Must): at least 3 windows, and no window's train side holds less than 50% of the data.
   [^split10]: **SPLIT-10** (Should): when a label is known only some time after its row, train on the rows whose
     outcome is known by the window's start.
