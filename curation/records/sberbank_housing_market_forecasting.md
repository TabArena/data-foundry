---
unique_name: sberbank_housing_market_forecasting
name: Sberbank Housing
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
priority: 3
tags:
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Later'
- 'Features: Read Later'
collections:
- TabArena Reject
- TabRed
original_source: Kaggle
year: '2017'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/competitions/sberbank-russian-housing-market
- https://github.com/yandex-research/tabred/tree/main/preprocessing#sberbank-housing-market-forecasting
notebook_path: datasets/beyond_iid/temporal/sberbank_housing_market_forecasting/sberbank_housing_market_forecasting.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/sberbank_housing_market_forecasting/dataset.py
source_row: 711
type_adapter_id: curation-record-v1
---

## Comments

Use TabRed preprocessing (verify it)

TabRed uses 5 and 7 months for splits

Data splits used by Kaggle experts were grouped/stratified IID ("CV for Investment type model was almost unusable, but CV for OwnerOccupier"). The predicted mean was then off for test data and they used some magic numbers to correct. Thus it sounds like real temporal splits would be better. https://www.kaggle.com/competitions/sberbank-russian-housing-market/discussion/32717

Moreover, it seems that the data is merged from two groups!

CC (2026-10-14, Lennart): Keep all 1,126 sales whose build year is after the year of sale (1,124 look like flats sold before completion). 28,321 rows.

CC (2026-10-21, Lennart): "ok" on the consistency check against mortgage (which lags each macro series to its release, LEAK-10); mortgage's lag applied: the monthly and quarterly macro series are lagged by one period.

**Assessment (AI, 2026-10-21):** Frequencies read from macro.csv (values constant within each period over 2010-2016): 7 daily market series (exchange rates, Brent, stock indices) keep the sale date; 20 monthly (one month back), 5 quarterly (one quarter back) and 66 yearly series. The yearly series change only on January 1 and hold their own year (Moscow salary of 2014, 61,208 rubles, on 2014 sales), so 64 are lagged by one year; `gdp_annual` and `gdp_annual_growth` already hold the previous year (2014 rows: Russia's 2013 GDP) and stay. `gdp_quart` already holds the previous quarter, so the model now sees GDP two quarters back, as in mortgage. Rows and feature count unchanged (28,321, 386; lagged columns renamed `_lag_1m`/`_lag_1q`/`_lag_1y`). Effect on LightGBM (500 trees, lr 0.03) RMSE over the 5 windows, newest first: 0.2268/0.2448/0.2647/0.2730/0.2548 before, 0.2269/0.2452/0.2633/0.2698/0.2548 after (mean 0.2528 to 0.2520; dummy 0.39), so the unlagged statistics carried no measurable signal. dataset check: 0 errors, 0 warnings; the build is stale (not rebuilt).

CC (2026-10-21, Lennart): the declared metric documents the original use case's metric; overrule it only when it is biased or wrong (evidence from the paper); keep the note of the original metric (TP-6 amended).

**Assessment (AI, 2026-10-21):** metric stays the default RMSE: the competition scored RMSLE on the flat's price (Kaggle API), and the task ships log price per square metre (TabReD), a target the competition did not score, so RMSE on the log target is the nearest listed metric (rule 4). The notes now name RMSLE. Needs a rebuild to reach the container (notes only).

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: mosque_count_500, mosque_count_1000, mosque_count_1500, mosque_count_2000.

CC (2026-10-21, Lennart): on which 0/1 columns are flags: "no if we can infer from the semantic context, keep it a number, this is a real-world bias. We want to make things categorical if we know from the context they are indeed such" (CLEAN-14, amended again). Reverted: mosque_count_500, mosque_count_1000, mosque_count_1500, mosque_count_2000 (counts) stay numeric.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source rmse — Root Mean Squared Logarithmic Error (RMSLE) on price_doc (https://www.kaggle.com/competitions/sberbank-russian-housing-market/overview/evaluation).

**Assessment (AI, 2026-10-21):** metric stays rmse on log(price_doc / full_sq), not `rmsle` + `target_transform`: the inverse of the shipped target is the price per square metre, not the price the competition scored, so RMSLE after the inverse would score the price per m2 (off by log vs log1p and by the per-m2 scale) and is no closer to the competition's RMSLE than the current RMSE, which equals RMSE of log(price) up to log vs log1p.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 2 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `state`, `ecology` (the README lists their levels); their codes that mean unknown (don't know, refused, not asked) are missing in `state`, `ecology` (CLEAN-10).

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): ID_metro a category, like the other station ids.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `dubai_dld_sales_transactions` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 1 coded columns carry their words; 1 scores are numbers (state).

**Assessment (AI, 2026-11-10):** priority for the review of the test windows and horizons, which this record never had. Priority 3: gap 0, use case 0, source + (Sberbank's competition), shape +, risk 0 (the open issue is the window length and the floor).

CC (2026-11-11, Lennart): Review issue 1 ("Agree.", to the answer that the windows follow the length of the horizon sign-off): the three seven-month windows of the horizon replace the five half-years from January 2013, whose three oldest trained on 44.3%, 28.6% and 17.8% of the sales.

CC (2026-11-11, Lennart): the declared horizon (7 months, no gap, windows starting 2014-12-01, 2014-05-01 and 2013-10-01) is checked, as seven months is the shortest test period of the sources (TabReD's; the competition tests eleven months), where the half-year was our own assumption; the window under half the sales, October 2013 to April 2014 on 35.4%, beside 83.6% and 59.1%, is signed off with it (Review horizon, a: "Reply (a): Seven months"; SPLIT-14 as amended 2026-11-11).

**Assessment (AI, 2026-11-11):** applied the horizon (a) and issue 1: `temporal` declares `TemporalSplits(window=7, unit="months", cutoffs=("2014-12-01", "2014-05-01", "2013-10-01"))`, confirmed with `window_bounds` on the definition's frame. Test 4,647, 6,936 and 6,704 sales (mean log price per square metre 11.84, 11.82, 11.80); train 23,674, 16,738 and 10,034 (83.6%, 59.1%, 35.4% of 28,321). The windows are adjacent: moving the oldest back lowers its train side (33.3% from September 2013, 31.1% from August). `accepted_check_warnings` takes `splits_train_under_half` with the sign-off; `dataset check`: 0 errors, 0 warnings, no `splits_floor_core` (the five half-years had three windows under half).

CC (2026-11-11, Lennart): accepted `splits_feature_missing_in_test` with a note naming the columns (cross-dataset item "Accept splits_feature_missing_in_test where a column starts or stops being recorded within the history?", A: the data as the deployed model met it).

CC (2026-11-11, Lennart): accepted `time_newest_period_short` with its reason (cross-dataset item "What to do with a newest period that holds far fewer rows than the periods before it?", A).

**Assessment (AI, 2026-11-11):** the lag of `provision_retail_space_sqm` is recorded from 2012 Q1 to 2013 Q4, the two education lags from 2014 Q1; 2015 holds 394 to 724 sales a month, 1,044 to 1,583 from September to December 2014, with a flat log price (11.80 to 11.87).

## Review

**Outcome:** added. On 2026-11-11 you chose seven-month windows (H, a), which also settles the windows (issue 1):
December 2014 to June 2015, May to November 2014 and October 2013 to April 2014, the oldest on 35.4% of the sales with
your sign-off; both are applied and nothing is left open.

**Main points:** Settled on 2026-11-11: three seven-month test windows, the shortest test period of the sources, in
place of five half-years from January 2013.

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

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | A | Six months (implemented) | half-year windows, as for a refit every half year: only July to December 2014 and January to June 2015 keep half the sales for training | 5 windows of 3,051 to 6,434 sales (2 above the floor) | today's length; within TabReD's analysis windows of "roughly 5-7 month" | a half-year refit is our assumption: no source gives Sberbank's cadence; two windows above the floor, not three |
  | B | Five months | three separate windows from April 2014 to June 2015, within the sixteen months open | 3 windows of 2,670 to 5,234 sales | the longest length that keeps three separate windows above the floor; the low end of TabReD's analysis windows | shorter than the sources' test periods of seven to eleven months; three windows, the fewest allowed |
  | C | Four months | four windows over all sixteen months open | 4 windows of 2,219 to 4,562 sales | four windows; every month open tested | shorter than any source's test period |
  | D | Six months stepping by three | today's length, four windows three months apart | 4 overlapping windows of 3,064 to 6,288 sales | keeps today's length; four windows | the windows overlap: the sales of July 2014 to March 2015 are tested twice |
  | E | Three months | five quarters from April 2014 | 5 windows of 1,430 to 3,791 sales | five windows | half the shortest source period |

* **Recommendation:** B: five months is the longest length that keeps three separate windows above the floor in the
  sixteen months open, nearest the sources' test periods. **Decision:** A, B, C, D or E?

**Lennart (2026-11-11, discuss):** So we should do 7-11 months from the source, why dont we do 7 then? or is it too little
training data?

**Answer (AI, 2026-11-11):** Use 7-month windows, the shortest test period of the sources, now that the amended floor
admits one window at 35%?

* **Problem:**
  - The sources test 7 to 11 months (Kaggle: July 2015 to May 2016; TabReD: 7 months), and 7 months was out only
    because its third window trains on 35.4% of the sales.
  - Since 2026-11-11 the newest window and one other must train on at least half the sales and further windows on at
    least 30%[^a-14], so 7 months gives exactly three windows: two above half and one at 35.4%.
  - Today's six months test five windows, three of them under half (44.3%, 29%, 17.8%), which the amended floor does
    not admit.
* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | a | Seven months | December 2014-June 2015, May-November 2014, October 2013-April 2014 (83.6%, 59.1%, 35.4%) | 3 windows of 4,647 to 6,936 sales | the sources' shortest test period; no choice of windows left to argue | the oldest trains on 35.4% |
  | b | Six months, three windows | January-June 2015, July-December 2014, January-June 2014 (89.2%, 67.0%, 44.3%) | 3 windows of 3,064 to 6,434 sales | today's length; the oldest trains on 44.3% | a length no source uses |
  | c | Five months (the block's B) | February-June 2015, September 2014-January 2015, April-August 2014 (90.6%, 72.1%, 54.8%) | 3 windows of 2,670 to 5,234 sales | every window above half | shorter than every source's test period |

* **Recommendation:** a: the length the sources use, and the amended floor admits its third window.
  **Decision:** a, b or c?

[^a-14]: **SPLIT-14** (Must; amended 2026-11-11, Lennart): the newest window and at least one other train on at least 50% of the data; further windows down to 30%, and at most as many windows under 50% as at or above it.

**Lennart (2026-11-11, discuss):** Reply (a): Seven months

**Resolved (2026-11-11, Lennart):** a, seven-month windows with no gap, the shortest test period of the sources
(TabReD's seven months; the competition tests eleven), in place of the half-year, our own assumption. `temporal`
declares `TemporalSplits(window=7, unit="months", cutoffs=("2014-12-01", "2014-05-01", "2013-10-01"))`, confirmed with
`window_bounds` on the definition's frame: test 4,647, 6,936 and 6,704 sales, train 23,674, 16,738 and 10,034 (83.6%,
59.1%, 35.4%). Your mark signs off the window under half, October 2013 to April 2014 on 35.4%:
`accepted_check_warnings` takes `splits_train_under_half` with it, and the splits comment names it and its share.
`task_summary.split`, the half-year sentence of `fit_reason`, `splits_comment` (the length's reason from this block,
the windows and the counts) and a curation note are rewritten. The record has the horizon CC line. `dataset check`: 0
errors, 0 warnings; the `splits_floor_core` error of the five half-years is gone (README not regenerated).

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

   **Lennart (2026-11-11, discuss):** 27 and 18 % seem to low indeed, come back to this case here after you looked over
   the others and my prompt

   **Answer (AI, 2026-11-11):**
   - The floor is amended (2026-11-11): two windows on at least half the sales, further windows down to 30%, never more
     windows under half than above. The 29% and 17.8% windows stay out under it.
   - The windows now follow the length you choose in the horizon (H): at 7 months, 6 months or 5 months exactly three
     windows remain, so this issue closes with H's choice.

   **Lennart (2026-11-11, discuss):** Agree.

   **Resolved (2026-11-11, Lennart):** closed with the horizon's choice (a): three adjacent seven-month windows,
   December 2014 to June 2015, May to November 2014 and October 2013 to April 2014, in place of the five half-years
   from January 2013; the oldest trains on 35.4%, signed off with the horizon's mark, beside 83.6% and 59.1%. Moving the
   older windows back would only lower their train sides (from September 2013 the oldest would train on 33.3%). The same
   edits as the horizon's; the record has the CC line. `dataset check`: 0 errors, 0 warnings.

## Reference

Alex Matveev, Anastasia_Sidorova_50806198, and DataCanary. Sberbank Russian Housing Market. https://kaggle.com/competitions/sberbank-russian-housing-market, 2017. Kaggle.
