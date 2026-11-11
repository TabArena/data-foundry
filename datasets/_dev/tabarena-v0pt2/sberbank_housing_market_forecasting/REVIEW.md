# sberbank_housing_market_forecasting

**Outcome:** added. Under the rule on choosing test windows, rewritten on 2026-11-10, the AI proposes three windows
of five months from April 2014 to June 2015 in place of five half-years from January 2013, three of which train on
less than half the sales (issue 1). `dataset.py` is unchanged until you decide.

**Main points:** Test three five-month windows (April 2014 to June 2015) instead of five half-years reaching back to
January 2013, so every train side keeps half the sales (issue 1)?

**Horizon:**

* **Verdict:** change to five-month windows (medium confidence): the sources test seven to eleven months, the half-year
  is our own reading of a refit cadence, and five months is the longest length that keeps three separate windows above
  half the sales in the sixteen months open.
* **Length:** declared six months, "a model that is refit every half year", our assumption: no source gives
  Sberbank's refit cadence. The competition tests the eleven months after its training data ("The test set contains
  ~7K realty transactions spanning from July 2015 to May 2016",
  https://www.r-bloggers.com/2017/06/a-data-scientists-guide-to-predicting-housing-prices-in-russia/). TabReD tests
  seven months (1 December 2014 to 30 June 2015) after five months of validation, and its analysis splits use windows
  of 4,500 sales, "roughly 5-7 month time-frame" (https://github.com/yandex-research/tabred/tree/main/preprocessing);
  the record's "TabRed uses 5 and 7 months for splits" is that. A lender values the flat at its sale, so the length
  says how long one fitted model serves.
* **Gap:** none needed: a sale's price is known when it is signed, and the economic statistics are already read one
  period back for their release delay.
* **Time frame:** 28,321 sales from August 2011 to June 2015, dense from 2014: 1,000 to 1,200 a month in 2014, 1,583
  in December 2014 (the month the ruble fell), 394 to 724 a month in 2015. Half the sales lie before March 2014, so the
  windows open are March 2014 to June 2015 (16 months, 13,914 sales); today's windows reach back to January 2013.
* **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | A | Six months (implemented) | half-year windows, as for a refit every half year: only July to December 2014 and January to June 2015 keep half the sales for training | today's length; within TabReD's analysis windows of "roughly 5-7 month" | a half-year refit is our assumption: no source gives Sberbank's cadence; two windows above the floor, not three |
  | B | Five months | three separate windows from April 2014 to June 2015, within the sixteen months open | the longest length that keeps three separate windows above the floor; the low end of TabReD's analysis windows | shorter than the sources' test periods of seven to eleven months; three windows, the fewest allowed |
  | C | Four months | four windows over all sixteen months open | four windows; every month open tested | shorter than any source's test period |
  | D | Six months stepping by three | today's length, four windows three months apart | keeps today's length; four windows | the windows overlap: the sales of July 2014 to March 2015 are tested twice |
  | E | Three months | five quarters from April 2014 | five windows | half the shortest source period |

* **Recommendation:** B: five months is the longest length that keeps three separate windows above the floor in the
  sixteen months open, nearest the sources' test periods. **Decision:** A, B, C, D or E?

**Issues for Lennart:**

1. **Which test windows should replace the five half-years from January 2013?**

   * **Problem:**
     - The five half-year test windows reach back to January 2013, and the three oldest train on 44.3%, 28.6% and
       17.8% of the sales, under the half every train side must keep[^sh-split14].
     - Half the sales lie before March 2014, so only two half-years (July to December 2014, January to June 2015) keep
       half for training, one fewer than the three windows every temporal task needs.
     - The newest window always stays and the others are chosen from the use case and statistics of the data, while
       the length comes from the source's horizon, and no source gives six months[^sh-split15][^sh-split12].
   * **Background:**
     - The one exception to the floor, an older window on at least 40% of the rows when two windows are above the
       floor and most test entities recur, does not apply: January to June 2014 trains on 44.3%, but a test row is a
       flat valued once at its sale (the release has no flat id), not an entity the lender re-rates.
     - The sixteen months open hold three phases of the market: 2014 with 1,000 to 1,200 sales a month, December 2014
       with 1,583, and 2015 with 394 to 724. B puts one window in each (April to August 2014, September 2014 to January
       2015, February to June 2015); C cuts all sixteen months into four; D keeps six months with windows three months
       apart, which overlap, so the sales of July 2014 to March 2015 are tested twice.
     - The target, the log price per square metre, has a mean of 11.81 to 11.85 in every candidate window and 11.73 to
       11.77 on the train sides; the 2013 windows of A are lower (11.68 and 11.76).
     - PSI, the population stability index, compares a feature's distribution in the window with its train side;
       above 0.25 is usually read as a large shift. The yearly and quarterly economic statistics hold one value per
       period, so their PSI is large in every window (8 to 18); the median over all features tells the windows apart.
   * **Statistics:** from the candidate tables, over all sales (every side is smaller than the tool's 100,000-row
     sample).

     | Window | In | Test sales | Mean target, test | Train side | Train share | Largest / median PSI |
     |---|---|---|---|---|---|---|
     | Mar-Jun 2015 | C | 2,219 | 11.82 | 11.77 | 92.2% | 11.7 / 0.084 |
     | Feb-Jun 2015 | B | 2,670 | 11.83 | 11.77 | 90.6% | 12.7 / 0.064 |
     | Jan-Jun 2015 | A, D | 3,064 | 11.83 | 11.77 | 89.2% | 17.4 / 0.056 |
     | Nov 2014-Feb 2015 | C | 3,592 | 11.85 | 11.76 | 79.5% | 9.1 / 0.027 |
     | Oct 2014-Mar 2015 | D | 5,221 | 11.84 | 11.76 | 75.8% | 8.8 / 0.034 |
     | Sep 2014-Jan 2015 | B | 5,234 | 11.83 | 11.76 | 72.1% | 8.5 / 0.032 |
     | Jul-Dec 2014 | A, D | 6,288 | 11.83 | 11.75 | 67.0% | 10.6 / 0.028 |
     | Jul-Oct 2014 | C | 3,541 | 11.81 | 11.75 | 67.0% | 12.9 / 0.025 |
     | Apr-Sep 2014 | D | 5,942 | 11.82 | 11.74 | 54.8% | 10.6 / 0.021 |
     | Apr-Aug 2014 | B | 4,893 | 11.82 | 11.74 | 54.8% | 9.8 / 0.020 |
     | Mar-Jun 2014 | C | 4,562 | 11.81 | 11.73 | 50.9% | 9.7 / 0.030 |
     | Jan-Jun 2014 | A | 6,434 | 11.81 | 11.72 | 44.3% | 18.4 / 0.035 |
     | Jul-Dec 2013 | A | 4,431 | 11.76 | 11.70 | 28.6% | 16.5 / 0.059 |
     | Jan-Jun 2013 | A | 3,051 | 11.68 | 11.72 | 17.8% | 18.4 / 0.117 |

   * **Effect on the task:** A scores three of its five windows with models fit on 18% to 44% of the sales, mostly the
     thin years 2011 to 2013. B scores three separate windows, before, around and after the December 2014 rush, each
     model fit on at least 54.8% of the sales and serving five months, against seven to eleven in the sources.
   * **Consistency:** california_house_prices_2020 moved its oldest window from 25% to 50% of the rows (2026-10-21).
     The housing family keeps each source's own horizon rather than one length for all (2026-10-21), and
     medical_facility_operational_data took its window length from its source (2026-11-05); here the source lengths
     do not fit three times into the history open, so B takes the longest that does. No dataset has chosen windows
     under the rewritten rule yet; delivery_eta_1m's issue 1 is open.
   * **Sources:** the definition `datasets/_dev/tabarena-v0pt2/sberbank_housing_market_forecasting/dataset.py`
     (`temporal`, `splits_comment`, `task_summary.split`, `fit_reason`); the record
     `curation/records/sberbank_housing_market_forecasting.md` (no earlier call on the windows); the candidate tables
     `.venv/bin/python -m data_foundry.curation.cli dataset windows sberbank_housing_market_forecasting --root
     datasets/_dev/tabarena-v0pt2` (5 windows) and the same with `--window 5 --unit months` (3 above the floor),
     `--window 4 --unit months` (4) and `--window 6 --unit months --step 3` (4).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Five half-years (implemented) | tests Jan 2013 to Jun 2015 in six-month windows | today's windows; 23,268 test sales | three train sides under the floor (44.3%, 28.6%, 17.8%); the half-year has no source |
     | B | Three five-month windows | tests Feb-Jun 2015, Sep 2014-Jan 2015 and Apr-Aug 2014 | every train side keeps at least 54.8%; one window before, around and after the December 2014 rush; the longest length that fits, nearest the sources | three windows, the fewest allowed; March 2014 untested; 12,797 test sales |
     | C | Four four-month windows | tests Mar-Jun 2015, Nov 2014-Feb 2015, Jul-Oct 2014 and Mar-Jun 2014 | four windows over all sixteen months open; 13,914 test sales | shorter than any source's test period; the oldest trains on 50.9% |
     | D | Six months, three months apart | tests Jan-Jun 2015, Oct 2014-Mar 2015, Jul-Dec 2014 and Apr-Sep 2014 | keeps today's length; four windows, every train side at least 54.8% | the windows overlap, so the sales of July 2014 to March 2015 are tested twice |

   * **Recommendation:** B: the longest length that keeps three separate windows above the floor, nearest the
     sources' seven to eleven months, with one window in each phase of the market. **Decision:** A, B, C or D?

   **Notes for the AI:** on B, `temporal = Temporal(on="timestamp", splits=TemporalSplits(window=5, unit="months",
   cutoffs=("2015-02-01", "2014-09-01", "2014-04-01")))`. Built with `window_bounds` on the definition's frame: test
   2,670, 5,234 and 4,893 sales, train 25,651, 20,417 and 15,524 (90.6%, 72.1%, 54.8%). On C, `TemporalSplits(window=4,
   unit="months", cutoffs=("2015-03-01", "2014-11-01", "2014-07-01", "2014-03-01"))`: test 2,219, 3,592, 3,541 and
   4,562, train 26,102, 22,510, 18,969 and 14,407 (92.2%, 79.5%, 67.0%, 50.9%). On D, `TemporalSplits(window=6,
   unit="months", cutoffs=("2015-01-01", "2014-10-01", "2014-07-01", "2014-04-01"))`: test 3,064, 5,221, 6,288 and
   5,942, train 25,257, 21,466, 18,969 and 15,524 (89.2%, 75.8%, 67.0%, 54.8%). Then rewrite `task_summary.split`
   ("Five test windows of six months, from January 2013 to June 2015 ... as for a model refit every half year"), the
   half-year sentence of `fit_reason` and `splits_comment` (the windows, the reasons and the numbers above), add a CC
   line to the record and a dated CHANGELOG entry, and run `dataset check` (SPLIT-12, SPLIT-14, SPLIT-15).

   [^sh-split14]: **SPLIT-14** (Must): "A temporal task has at least 3 windows, and no window's train side holds less
     than 50% of the data. ... A release with two windows above the floor may add one older window that trains on at
     least 40% of the rows, when most test entities recur (the actor re-rates entities it knows) and folds by entity
     would test unseen ones."
   [^sh-split15]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): "The newest window is always a test window ... The other windows are the curator's choice, per dataset,
     argued from the use case ... The evidence is statistics of the data, never a model's score ... Every choice stays
     above SPLIT-14's floor; the length and the gap come from SPLIT-12."
   [^sh-split12]: **SPLIT-12** (Should): "The horizon is a human judgment from the source: how far ahead the actor
     predicts ..., the competition's own test window, the refit cadence. Choose the test windows to match it and write
     the reasoning down."
