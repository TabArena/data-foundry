# aeolus_rebuilt

**Outcome:** added as `aeolus_rebuilt_1m`. Under the rule on choosing test windows, rewritten on 2026-11-10, the AI
proposes to keep the newest fortnight (18-31 December 2024) and to replace the two other early-winter fortnights with
one in July and one in March 2024 (issue 1). `dataset.py` is unchanged until you decide.

**Main points:** Test on 18-31 December, 3-16 July and 13-26 March 2024 instead of the six weeks from 20 November to 31
December (issue 1)?

**Issues for Lennart:**

1. **Which fortnights of 2024 should the test windows be?**

   * **Problem:**
     - The three test windows are the newest six weeks (20 November to 31 December 2024), so the score measures
       early-winter delays only, while an airline or a travel app uses the model in every season.
     - Since 2026-11-10 the newest window always stays and the others are chosen from the use case and statistics of
       the data, preferring other seasons over the weeks just before the newest[^split15].
     - Every two-week window from 17 January 2024 on keeps at least half the flights for training, so all seasons of
       2024 are open to choose from, while no fortnight of 2023 is[^split14].
   * **Background:** The share of late flights follows the season in both years: by month it is highest in June and
     July (25 to 30%) and lowest in October and November (13 to 16%). The holiday fortnight is late in 2024 (25.9%) but
     was not in 2023 (18.2% from 20 December to 2 January). The two older windows of A are near copies of each other:
     both in the weeks before Christmas (Thanksgiving included), 16.7% and 17.5% late, with the same drift of the
     temperatures.
     The fortnight of 17-30 July holds the CrowdStrike outage of 19 July: 58.3% of that day's flights arrived late and
     92% of Delta's, Delta operated about 40% fewer flights from 19 to 22 July, and its late share stayed above 60%
     through 23 July. The length (two weeks, the refit cadence) and the one-day gap stay as they are[^split12]. Each
     train side of B holds the same season of 2023, so the model has seen each test season once. PSI, the population
     stability index, compares a feature's distribution in the window with its train side; above 0.25 is usually read
     as a large shift.
   * **Statistics:** late shares from all flights; the drift from the candidate table (100,000-row samples of each
     side); 264k to 278k flights per window.

     | Window (2024) | In | Late, test | Late, train side | Train share | Largest drift (PSI) |
     |---|---|---|---|---|---|
     | 18-31 Dec | A, B, C | 25.9% | 20.6% | 97.9% | 1.10, temperatures |
     | 4-17 Dec | A | 16.7% | 20.7% | 96.0% | 1.21, temperatures |
     | 20 Nov-3 Dec | A | 17.5% | 20.8% | 94.0% | 1.09, temperatures |
     | 3-16 Jul | B | 26.9% | 21.1% | 74.2% | 2.43, temperatures |
     | 17-30 Jul | C | 34.0% | 21.2% | 76.2% | 2.22, temperatures |
     | 13-26 Mar | B, C | 21.3% | 20.5% | 58.3% | 0.33, temperatures |

   * **Effect on the task:** Under A, models are ranked by how they handle December traffic. B adds the summer peak,
     when the most flights are late and the weather inputs differ most from training, and a spring fortnight close to
     the year's average (20.7% of all flights late).
   * **Consistency:** Today's windows come from your call of 2026-10-12 on aeolus (two-week windows, one of three in
     the holiday peak)[^split20], made before the rule allowed windows away from the newest weeks; B keeps one window in
     the holiday peak. No dataset has chosen windows under the rewritten rule yet.
   * **Sources:** the definition `datasets/_dev/tabarena-v0pt2/aeolus_rebuilt_1m/dataset.py` (`splits_comment`,
     `temporal`); the records `curation/records/aeolus_rebuilt.md` and `curation/records/aeolus.md` (CC 2026-10-12);
     the candidate table `.venv/bin/python -m data_foundry.curation.cli dataset windows aeolus_rebuilt_1m --root
     datasets/_dev/tabarena-v0pt2` (25 fortnights, 17 January to 31 December 2024).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Newest six weeks (implemented) | tests 18-31 Dec, 4-17 Dec and 20 Nov-3 Dec 2024 | the weeks right after a refit; one window in the holiday peak | November and December only; two windows are near copies |
     | B | Holidays, July, March | tests 18-31 Dec, 3-16 Jul and 13-26 Mar 2024 | winter, summer and spring; the summer peak and its weather shift | the older windows train on 74% and 58% of the flights |
     | C | Holidays, the outage, March | as B, with 17-30 Jul in place of 3-16 Jul | tests an event no input announces | one airline's five-day outage makes a third of the score |

   * **Recommendation:** B: it keeps the holiday fortnight and adds the two seasons that differ most from it, the
     summer peak (26.9% late, the largest drift of the weather inputs) and spring at about the year's average (21.3%).
     **Decision:** A, B or C?

   **Notes for the AI:** on B, `temporal = Temporal(on="FL_DATE", splits=TemporalSplits(window=14, unit="days",
   gap=1, cutoffs=("2024-12-18", "2024-07-03", "2024-03-13")))`. Built on the definition's frame: test 264,245, 278,071
   and 267,477 flights, train 13,426,458, 10,166,861 and 7,987,461 (97.9%, 74.2%, 58.3%). On C, the cutoffs
   `("2024-12-18", "2024-07-17", "2024-03-13")`: the July window tests 276,107 flights on 10,444,754 (76.2%). Then
   rewrite `task_summary.split` and `splits_comment` (the windows, the reasons and the numbers above; drop "The last six
   weeks of 2024" and "All three windows lie in late November and December"), add a CC line to the record and a dated
   CHANGELOG entry, and run `dataset check` (SPLIT-15).

   [^split15]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): "The newest window is always a test window ... The other windows are the curator's choice, per dataset,
     argued from the use case ... The evidence is statistics of the data, never a model's score ... Prefer windows in
     other years, then other seasons, then other months, weeks or days, over the windows just before the newest."
   [^split14]: **SPLIT-14** (Must): at least 3 windows, and no window's train side holds less than 50% of the data.
   [^split12]: **SPLIT-12** (Should): the horizon is a human judgment from the source, such as the refit cadence.
   [^split20]: **SPLIT-20** (Should): "Check whether the newest windows fall in an atypical season and widen them so
     most do not. Cases: aeolus."
