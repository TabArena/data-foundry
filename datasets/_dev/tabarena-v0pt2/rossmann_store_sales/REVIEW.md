# rossmann_store_sales

**Outcome:** added. On 2026-11-11 you kept the six-week windows with the one-day gap (Horizon, ok) and chose the newest
six weeks, the Christmas weeks of 2014 and late spring 2014 as the test windows (issue 1, B); both are applied and
nothing is left open.

**Main points:** Settled on 2026-11-11: three six-week windows over two years and three seasons, the Christmas peak
among them, with the managers' six-week horizon checked.

**Horizon:**

* **Verdict:** keep the 42-day windows with the one-day gap (high confidence): Kaggle states the store managers' horizon
  as six weeks, and the competition's own test period, 48 days, is about as long.
* **Length:** declared 42 days. Kaggle's description: "Rossmann store managers are tasked with predicting their daily
  sales for up to six weeks in advance", to plan staff schedules
  (https://www.kaggle.com/competitions/rossmann-store-sales/overview). The competition's hidden test period ran 48
  days, 1 August to 17 September 2015, for 856 of the 1,115 stores (its `test.csv`). The length follows the source,
  not a convention of another dataset.
* **Gap:** one day, ours ("a planning gap" in the notes). The competition's test starts the day after its training
  data end (31 July and 1 August 2015), and a day's turnover is known when the store closes, so no label arrives late;
  the gap only drops the last day before each window from training.
* **Time frame:** the open days from 1 January 2013 to 31 July 2015 (844,392 store-days). Eleven windows of 42 days
  keep half the store-days for training, from 26 April 2014 (52.6%) to the newest. 180 stores have no rows from
  1 July to 31 December 2014 (935 of the 1,115 stores in that half-year), so the windows of that half-year test fewer
  stores. The competition's test period is not in the release.
* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | A | 42 days, one-day gap (implemented) | six-week windows, the last day before each left out of training: 11 candidates above the floor, from 26 April 2014 | 3 windows of 31,203 to 40,282 store-days (issue 1's B; today's three: 37,044 to 40,282) | the managers' horizon of "up to six weeks" that Kaggle states | the one-day gap is ours ("a planning gap"), not the competition's |
  | B | 48 days | the length of the competition's test: 10 candidates above the floor, back to 8 April 2014 | 10 candidates of 37,559 to 45,884 store-days | the period Kaggle scored | longer than the managers' stated horizon |
  | C | 42 days, no gap | as in the competition: one more training day per window | the windows of A: 3 of 31,203 to 40,282 store-days | the competition's own setup; a day's turnover is known when the store closes | too small a difference to change the definition for |

* **Recommendation:** A: six weeks is the managers' horizon as Kaggle states it, and the gap changes one training day
  per window. **Decision:** A, B or C?

**Lennart (2026-11-11, ok):** As implemented (A).

**Resolved (2026-11-11, Lennart):** A, the 42-day windows with the one-day gap stay. `splits_comment` gives the reason
from this block: Kaggle states the managers' horizon as six weeks, the competition's own test period (48 days) is about
as long, and the gap is ours, a planning gap that drops one training day per window. The record has the horizon CC
line. `dataset check`: 0 errors, 0 warnings (README not regenerated).

**Issues for Lennart:**

1. **Which six weeks should the test windows be?**

   * **Problem:**
     - The three test windows are the newest 18 weeks (28 March to 31 July 2015), all in the spring and early summer
       of 2015, while the managers forecast six weeks ahead all year.
     - Since 2026-11-10 the newest window always stays and the others are chosen from the use case and statistics of
       the data, preferring other years and seasons over the windows just before the newest[^rss-split15].
     - Eleven six-week windows keep at least half the store-days for training, back to 26 April 2014, so another year
       and the Christmas season are open[^rss-split14].
   * **Background:** The Christmas window (22 November 2014 to 2 January 2015) has the highest sales of the eligible
     history: 8,478 per store-day on average against 6,847 on its train side, 24% more. The summer window of 2014
     (19 July to 29 August) falls in the season of the competition's own test (August to mid-September), with school
     holidays on 69% of its store-days against 33% in the newest window. From 1 July to 31 December 2014, 180 stores
     have no rows, so windows in that half-year test 935 stores (the Christmas window reaches all 1,115 only on
     2 January 2015). The features hardly drift: PSI, the population stability index, compares a feature's
     distribution in the window with its train side (above 0.25 is usually read as a large shift), and its largest
     value is 0.24 or less in every window weighed here except the school-holiday flag in the summer of 2014 (1.22).
   * **Statistics:** from the candidate table (100,000-row samples of each side for the target and the drift; the
     counts from all rows); sales per open store-day.

     | Window | In | Store-days | Stores | Mean sales, test | Train side | Train share | Largest drift (PSI) |
     |---|---|---|---|---|---|---|---|
     | 20 Jun-31 Jul 2015 | A, B, C | 40,282 | 1,115 | 6,979 | 6,950 | 95.1% | 0.11 `SchoolHoliday` |
     | 9 May-19 Jun 2015 | A | 37,473 | 1,115 | 7,280 | 6,941 | 90.7% | 0.10 `SchoolHoliday` |
     | 28 Mar-8 May 2015 | A | 37,044 | 1,115 | 7,652 | 6,897 | 86.3% | 0.04 `Promo` |
     | 22 Nov 2014-2 Jan 2015 | B, C | 31,203 | 935 to 31 Dec | 8,478 | 6,847 | 73.1% | 0.03 `Promo2SinceWeek` |
     | 19 Jul-29 Aug 2014 | C | 33,716 | 934 | 6,710 | 6,853 | 61.3% | 1.22 `SchoolHoliday` |
     | 26 Apr-6 Jun 2014 | B | 38,107 | 1,115 | 7,344 | 6,789 | 52.6% | 0.24 `SchoolHoliday` |

   * **Effect on the task:** A ranks models on spring and early summer 2015 only, three windows in a row with little
     drift. B keeps the newest window and adds the Christmas peak, when staffing matters most and sales run a quarter
     above the train side, and late spring 2014, a window of the other year with every store. C adds the summer
     holidays of 2014, the competition's own season, in place of spring 2014.
   * **Consistency:** aeolus tests one of its three windows in the holiday peak (Lennart, 2026-10-12) and airqo
     spreads its windows over both seasons (Lennart, 2026-11-05)[^rss-split20]; the same kind of spread is proposed
     today for delivery_eta_1m. No dataset keeps only its newest windows without a stated reason.
   * **Sources:** Kaggle's competition pages (https://www.kaggle.com/competitions/rossmann-store-sales/overview,
     https://www.kaggle.com/competitions/rossmann-store-sales/data); the definition
     `datasets/_dev/tabarena-v0pt2/rossmann_store_sales/dataset.py` (`temporal`, `splits_comment`); the record
     `curation/records/rossmann_store_sales.md`; the candidate table `.venv/bin/python -m data_foundry.curation.cli
     dataset windows rossmann_store_sales --root datasets/_dev/tabarena-v0pt2` (11 windows); the store counts from the
     release's `train.csv`.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Newest three windows (implemented) | tests 20 Jun-31 Jul, 9 May-19 Jun and 28 Mar-8 May 2015 | the weeks right after a refit; all 1,115 stores; the largest train sides (86% to 95%) | one year and one season; no Christmas; three windows with almost the same features |
     | B | Spread over the eligible history | tests 20 Jun-31 Jul 2015, 22 Nov 2014-2 Jan 2015 and 26 Apr-6 Jun 2014 | two years and three seasons; the Christmas peak; evenly spaced (the 1st, 6th and 11th candidate) | the oldest trains on 52.6%; the Christmas window tests 935 stores until 31 December |
     | C | Newest, Christmas, summer 2014 | tests 20 Jun-31 Jul 2015, 22 Nov 2014-2 Jan 2015 and 19 Jul-29 Aug 2014 | the Christmas peak; the summer holidays of the competition's own season | two of three windows test 935 stores; two summer windows and no spring |

   * **Recommendation:** B: the newest window stays, the Christmas weeks are the season a store manager staffs up
     for, and late spring 2014 adds the other year with every store; the three are evenly spaced over the eligible
     history and every train side keeps more than half the store-days. **Decision:** A, B or C?

   **Notes for the AI:** on B, `temporal = Temporal(on="Date", splits=TemporalSplits(window=42, unit="days", gap=1,
   cutoffs=("2015-06-20", "2014-11-22", "2014-04-26")))`: test 40,282, 31,203 and 38,107 store-days, train 802,996,
   617,355 and 443,771 (95.1%, 73.1%, 52.6%). On C, `temporal = Temporal(on="Date", splits=TemporalSplits(window=42,
   unit="days", gap=1, cutoffs=("2015-06-20", "2014-11-22", "2014-07-19")))`: test 40,282, 31,203 and 33,716, train
   802,996, 617,355 and 517,626 (95.1%, 73.1%, 61.3%). Built with `TemporalSplits.splits` on the definition's frame
   (844,392 store-days); each train side ends two days before its window (the one-day gap). Then rewrite
   `task_summary.split` ("Three windows of six weeks from late March to July 2015") and `splits_comment` (the
   windows, the reasons and the numbers above, the 180 stores without rows from July to December 2014), add a CC line
   to the record and a dated CHANGELOG entry, and run `dataset check` (SPLIT-15).

   [^rss-split15]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): "The newest window is always a test window ... The other windows are the curator's choice, per dataset,
     argued from the use case ... The evidence is statistics of the data, never a model's score ... Prefer windows in
     other years, then other seasons, then other months, weeks or days, over the windows just before the newest."
   [^rss-split14]: **SPLIT-14** (Must; amended 2026-11-08, Lennart): "A temporal task has at least 3 windows, and no
     window's train side holds less than 50% of the data."
   [^rss-split20]: **SPLIT-20** (Should), cases: aeolus, "two-week windows with one of three in the holiday peak
     (2026-10-12, Lennart)"; airqo_low_cost_air_quality_monitor_calibration_challenge, "five monthly windows from
     October 2020 ... so the test covers both seasons" (2026-11-05, Lennart, issue 1).

   **Lennart (2026-11-11, change):** Option B: Spread over the eligible history.

   **Resolved (2026-11-11, Lennart):** B. `temporal` declares `cutoffs=("2015-06-20", "2014-11-22", "2014-04-26")`
   with the one-day gap: test 40,282, 31,203 and 38,107 store-days, train 802,996, 617,355 and 443,771 (95.1%, 73.1%,
   52.6%). `task_summary.split` and `splits_comment` name the windows and why each, "evenly spaced over the 11 windows
   that keep half the store-days" (the Christmas weeks sell 8,478 per open store-day against 6,837 on their train side,
   24% more), and the 180 stores without rows from July to December 2014. The 1,114 store-days of 19 June 2015, the
   newest window's gap day, are now in no split (an accepted `splits_rows_unused` warning with that reason). The record
   has the decision CC line. `dataset check`: 0 errors, 0 warnings.
