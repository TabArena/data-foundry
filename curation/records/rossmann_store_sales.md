---
unique_name: rossmann_store_sales
name: Rossmann Store Sales
checked_by:
- Andrej
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
original_source: Kaggle
year: '2015'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/c/rossmann-store-sales
notebook_path: datasets/beyond_iid/temporal/rossmann_store_sales/rossmann_store_sales.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/rossmann_store_sales/dataset.py
source_row: 725
type_adapter_id: curation-record-v1
---

## Comments

Awesome dataset, even the forecast horizon is given.

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: Promo, SchoolHoliday, Promo2.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source rmspe — Root Mean Square Percentage Error (RMSPE) (https://www.kaggle.com/competitions/rossmann-store-sales/overview/evaluation (Kaggle API evaluationMetric: 'Root Mean Square Percentage Error')).

CC (2026-10-21, Lennart): the declared metric stays as it is (`rmspe`, as Kaggle scored; cross-dataset item "Metrics still to settle").

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): left unordered: `DayOfWeek` (a partial order); `Assortment` (a partial order).

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 1 calendar or compass cycles ordered.

CC (2026-11-01, Lennart): marks on the review board of PR #37: DayOfWeek (an unordered category before) and CompetitionOpenSinceMonth are numbers (the curator's cycle rule); Assortment stays unordered as a partial order, noted.

**Assessment (AI, 2026-11-10):** priority for the review of the test windows and horizons, which this record never had. Priority 3: gap 0, use case 0, source + (Rossmann's competition), shape +, risk 0 (the open issue is the choice of windows).

CC (2026-11-11, Lennart): Review issue 1, B ("Option B: Spread over the eligible history."): the test windows are 20 June to 31 July 2015, the Christmas weeks of 2014 (22 November 2014 to 2 January 2015) and late spring 2014 (26 April to 6 June), evenly spaced over the 11 windows that keep half the store-days, in place of the newest 18 weeks.

CC (2026-11-11, Lennart): the declared horizon (42 days, a one-day gap, windows starting 2015-06-20, 2014-11-22 and 2014-04-26) is checked, as Kaggle states the store managers' horizon as six weeks and the competition's own test period, 48 days, is about as long (Review horizon, ok).

**Assessment (AI, 2026-11-11):** applied issue 1 (B): test 40,282, 31,203 and 38,107 store-days, train 802,996, 617,355 and 443,771 (95.1%, 73.1% and 52.6%); the Christmas window sells 8,478 per open store-day against 6,837 on its train side and tests 935 stores until 31 December. The 1,114 store-days of 19 June 2015, the newest window's gap day, lie in no split (an accepted warning). `dataset check`: 0 errors, 0 warnings.

CC (2026-11-11, Andrej): review marks. Issue 1 (B, "Add 32 calendar day counters, then ship"): 32 calendar day counters (days since and until promotions, state and school holidays and the summer holidays, closures, the Promo2 cycle, the competitor's months open, days to the month's end) are computed from each store's daily calendar before the closed days are dropped and read no sales; 15 features become 47. Issue 3 (B): the store table's competitor fields (`CompetitionDistance`, `CompetitionOpenSince*`) are missing on the store-days before the competitor's opening month. `dataset check`: 0 errors, 0 warnings, 844,392 store-days x 48 columns; not rebuilt. The forecasting test behind issue 1 was run on the three newest 2015 windows, not on the windows this branch ships since issue 4 (review issue 1, answer of 2026-11-11).

## Review

**Outcome:** added; ships with 32 calendar day counters, which pass the forecasting test in all three windows (Andrej,
2026-11-10, issue 1, option B); before: `TBD -> Yes` (`Time-series (Forecasting)`), held
until the forecasting test passes, as walmart_sales_in_stormy_weather. The 844,392 open store-days of 1,115 Rossmann
drug stores, January 2013 to July 2015 (Kaggle, 2015): each day's turnover, predicted up to six weeks ahead from the
store, the calendar, promotions and holidays, scored by the competition's RMSPE over three 42-day windows with a one-day
gap. Reviewed on 2026-11-04 without a review panel, from the gathered evidence (the record and its earlier decisions; no
model run exists for it) and two checks of today on the competition's files, whose windows match the shipped ones row
for row. Validity: the use case is the managers' six-week forecast the competition names, a direct fit; closed days and
the customer count (known only afterwards) are dropped. What is open is the test every store-by-day panel must pass to
count as a tabular task rather than forecasting (issue 1): the source's top solution is a tabular model, so that leg
holds, but a model on the shipped features beats each store's own-sales forecast in the two older windows and loses in
the newest. Value: the stores recur on both sides by design (known stores); the model's gain over the store's own
forecast is 12-17% in two windows. Quality: nothing open. Weighed: a competition with a stated actor and horizon +, a
large real panel +, a forecasting task by its own description -, the newest window won by the store's own history -. Since 2026-11-11 the three test windows are the newest six weeks, the Christmas weeks of 2014 and late spring
2014 (issue 4); the forecasting test was run on the three newest windows of 2015, so it covers one of them
(issue 1, answer of 2026-11-11).

**Main points:** All issues resolved: the six-week horizon with its one-day gap kept and the test windows spread
over two years and three seasons (Horizon and issue 4, 2026-11-11); 32 calendar day counters added, with which LightGBM beats the best
own-sales forecast in every window, so the definition ships (issue 1, B); a competitor is shown only from its opening
month (issue 3, B); the three six-week windows stay (issue 2, B).

**Record judgment:** valid task; in scope only once the forecasting test passes. Its shape and source are as good as the
copy has for store sales, so the hold is about the protocol, not the data.

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

**Issues for Andrej:**

1. **Ship, or hold until the forecasting test passes?**

   * **Problem:**
     - A store's daily sales over the next six weeks is forecasting by the competition's own words, which is in scope
       only when a model on the features clearly beats each store's forecast from its own past sales on the shipped
       windows and the source's top solutions are tabular models.
     - The second part holds; the first holds in the two older windows and fails in the newest, also with the
       winner's kind of trailing sales summaries added.
     - Ship now, hold the record at `TBD -> Yes` as walmart_sales_in_stormy_weather, or extend the features and test
       again?
   * **Background:** the panel test was never run on this dataset; m5_forecasting_accuracy's record asks that the two
     be judged alike[^1a]. The winner (Gert Jacobusse, 1st place, "Rossmann_nr1_doc.pdf", section "Features Selection
     / Extraction", https://storage.googleapis.com/kaggle-forum-message-attachments/102102/3454/Rossmann_nr1_doc.pdf)
     used XGBoost and wrote that "for each train and test record, the model should have features on 1) recent data 2)
     temporal information and 3) current trends", the recent data being store-specific summaries of the sales over
     the last quarter, half year, year and two years: trailing summaries, which the test allows[^1b].
   * **Experiments:** today's checks, RMSPE on the shipped windows (oldest to newest), standard errors from 200
     store-block bootstrap draws:

     | Forecast | 2015-03-28 to 05-08 | 2015-05-09 to 06-19 | 2015-06-20 to 07-31 |
     |---|---|---|---|
     | store's own median by weekday and promotion, last 52 weeks (best of five own-sales forecasts) | 0.1619 | 0.1447 | 0.1316 |
     | LightGBM, shipped features, 100 trees | 0.1413 | 0.1405 | 0.1619 |
     | LightGBM, shipped features, 3,000 trees | 0.1369 | 0.1224 | 0.1513 |
     | the same with the store's trailing sales summaries, lagged 44 days | 0.1422 | 0.1199 | 0.1385 |

     - Against the store's own forecast the strongest model is 0.020 to 0.025 better in the older windows (standard
       errors 0.004 to 0.006) and 0.007 worse in the newest (standard error 0.0014); over the three windows it is 8.6%
       lower (0.1335 against 0.1461). The other own-sales forecasts (the last 13 or 26 weeks, all history, the same
       day a year earlier) are worse in every window.
   * **Consistency:** walmart_sales_in_stormy_weather was held on 2026-11-02 at `TBD -> Yes` with the folder kept, its
     model 1.1-1.5% below the best own-series forecast[^1c]; m5_forecasting_accuracy and
     grocery_store_product_forecasting_challenge wait at `TBD -> 2nd Tier` on the same test. Rossmann's margin in two
     windows is about ten times walmart's, which may set it apart; its loss in the newest window, the one closest to
     use, does not.
   * **Unknown:** the tuned methods' RMSPE on these windows; the BeyondArena runs of the shipped container (scored by
     RMSE) could be rescored against the store's own forecast to settle it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship as defined (implemented) | 3 six-week windows, RMSPE; the test counted as met on the mean over windows | the competition's task and horizon; a large real panel; the model wins two windows clearly | the newest window is won by each store's own history; departs from the walmart hold |
     | B | Hold at `TBD -> Yes` | the record waits with `Time-series (Forecasting)` as its reason; the folder stays, unshipped | consistent with walmart; ships once a tuned model wins every window | a strong dataset leaves v0.2 for now |
     | C | Add the trailing summaries and test again | the store's sales summaries over the last 13 and 52 weeks, by weekday and by promotion, each lagged 44 days, become features; tuned methods are rerun | follows the winner's features; closest to how the task is solved | still behind in the newest window untuned; a new definition to review |

   * **Recommendation:** B for now, with the tuned rescoring as the way to A: the test is a must, and the newest
     window fails it. **Decision:** ship (A), hold (B), or extend and re-test (C)?

   **Notes for the AI:** on B, set the record's `suggestion` to `TBD -> Yes`, add `Time-series (Forecasting)` to
   `decision_markers` with a `CC (<date>, Andrej)` line giving the table, add `Andrej` to `checked_by`, keep the
   folder unbuilt. On C, compute in `_clean` per store from the open days at least 44 days before the row's date
   (horizon 42 + gap 1 + 1): the mean of log sales over 91 and 364 days, on promotion and non-promotion days over
   364 days, and over the last 52 same weekdays (lagged 7 weeks); the check script of 2026-11-04 is the reference.

   [^1a]: m5_forecasting_accuracy's record, "Open for the curator (consistency)": Rossmann "has the same panel shape
     and has never had TP-10 run".
   [^1b]: **TP-10** (Must): a panel with one series per entity is a tabular task when (1) a model on the features
     clearly beats each entity's naive forecast on the shipped windows, by the declared metric, and (2) the source's
     top solutions are tabular models on point-in-time features with no lag of the target beyond its last
     observation; trailing summaries of the series are allowed. **SEL-10** (Must): time-series forecasting is out.
   [^1c]: walmart_sales_in_stormy_weather, issue 2: "Don't ship for now, but keep it as tbd yes" (Andrej, 2026-11-02).

   **Andrej (2026-11-05, discuss):** The winning solution was a tabular model. What do we need to do to make this pass?

   **Answer (AI, 2026-11-05):**

   * **Finding:** it passes once each row says where its day sits in the store's calendar. Day counters for the
     nearest holiday, closure and promotion, computed in `_clean` from the source's own columns before the closed days
     are dropped, put a LightGBM at 0.097 / 0.104 / 0.112 RMSPE (oldest to newest window), against 0.145 / 0.131 /
     0.130 for the best of 26 forecasts from each store's own sales, raw or scaled, picked on each window. The model
     leads by 0.048 / 0.027 / 0.018 (33%, 20% and 14%), 12 / 5 / 23 standard errors over 200 draws of the stores
     with replacement[^a1]. The counters hold no sales at all.
   * **Why the newest window failed:**
     - Dropping the closed days also drops every public holiday and closure, so no shipped column says that yesterday
       was a holiday or that a store has just reopened. A model then learns the sales jumps around those days as
       effects of the date (day of year, week) in 2013 and 2014, and the dates move: Whit Monday fell on 20 May 2013,
       9 June 2014 and 25 May 2015, and a quarter of the stores began their summer school holidays on 29 June 2015,
       about a week before the first ones did in 2014.
     - In the newest window the model on the shipped features overpredicts the weeks without a promotion by about 7%
       (22-26 June, 21-24 July); with the counters the gap is about 2%. One added column, "closed the day before",
       takes that model from 0.140 to 0.121 in the newest window; dropping its day-of-year, week and day-number columns
       instead takes it to 0.129 (one configuration each).
     - The newest window holds no public holiday, so the store's own median by weekday and promotion, which ignores
       holidays, is at its best there. In the older windows its error reaches 0.27 to 0.36 in the weeks of Easter, May
       Day and Whit Monday; in the newest it stays at or below 0.16 in every week. Much of the model's earlier lead
       came from those holiday weeks.
     - The check of 2026-11-04 also trained on the 54 open store-days with zero sales, as log sales 0. They are never
       scored, and the winner left them out; leaving them out moves the newest window from 0.151 to 0.140, and to
       0.131 for the mean of three configurations, a tie with the best own forecast (0.130).
     - Not the cause: the 180 stores without data in the second half of 2014 (16% of the newest window's rows, 17% of
       each forecast's squared error); the 176 rows of stores within weeks of a refurbishment (6% of the error, high
       for every forecast); a few bad stores (the shipped-feature model's 15 worst carry 7.5% of its error).
   * **The own-sales forecasts, made stronger:** the medians, the geometric mean and the same day a year earlier of
     2026-11-04; the store's 52-week profile by weekday and promotion plus its level over the last 4, 8 or 13 weeks
     plus none, half or all of last year's change from those weeks to the same calendar days ("recent level times
     last-year seasonality"), with and without the store's own school-holiday effect; a regression per store on its
     own last 52 weeks (weekday, promotion, school holiday, closed the day before or after, with or without a trend).
     Each also comes scaled by the constant factor that minimises RMSPE on the six weeks before the gap (the winner's
     0.985 correction). The best of the 26, raw or scaled, picked on each window, scores 0.1450 / 0.1309 / 0.1296
     against 0.1619 / 0.1447 / 0.1316 for the median of 2026-11-04, so the bar rose in every window. Picked on the six
     weeks before the gap, as a forecaster would pick, it scores 0.1637 / 0.1428 / 0.1296.
   * **Experiments:** RMSPE per window; LightGBM on log sales, the mean of three configurations (3,000 to 5,000
     trees, chosen before the windows were scored), zero-sales days left out of training, no factor applied:

     | Forecast | 2015-03-28 to 05-08 | 2015-05-09 to 06-19 | 2015-06-20 to 07-31 |
     |---|---|---|---|
     | store's own median by weekday and promotion, 52 weeks (the bar of 2026-11-04) | 0.1619 | 0.1447 | 0.1316 |
     | best of the 26 own-sales forecasts, raw or scaled, picked on each window (the bar now) | 0.1450 | 0.1309 | 0.1296 |
     | regression per store on its own last 52 weeks | 0.1458 | 0.1374 | 0.1371 |
     | LightGBM, shipped features (check of 2026-11-04, one configuration) | 0.1369 | 0.1224 | 0.1513 |
     | LightGBM, shipped features | 0.1318 | 0.1190 | 0.1307 |
     | LightGBM, plus 32 calendar day counters (option B) | 0.0971 | 0.1044 | 0.1115 |
     | LightGBM, plus the counters and 27 trailing summaries of the store's sales lagged 44 days (option C) | 0.0957 | 0.1046 | 0.1056 |

     - With the counters each of the three configurations is ahead in every window on its own (the worst: 0.100 /
       0.116 / 0.115).
     - Which counters carry it (one configuration, newest window, 0.140 without any): the holiday counters 0.116, the
       closure counters 0.116, the promotion-cycle counters 0.138, the Promo2 cycle with the competitor's months open
       and the days to month end 0.141.
     - The per-store regression reads weekday, promotion, school holiday and closures too, from each store's own year,
       and stays at the own forecasts' level: the gain comes from learning the calendar across stores, the case the
       rule has in mind.
     - Keeping the zero-sales days in training changes little (all counters: 0.098 / 0.109 / 0.109).
     - Fresher sales do not help: the summaries cut at each window's start, as fresh as the own forecasts, score
       0.1015 / 0.1027 / 0.1040 against 0.0981 / 0.1019 / 0.1041 lagged 44 days (both with every counter), as the
       winner found: "These 'month ahead models' were almost as good as the models that did use all the most recent
       data".
     - The 27 summaries without the counters pass too, more narrowly: 0.131 / 0.118 / 0.119, 2.6 standard errors in
       the middle window.
   * **The test as the rule means it:** the own forecasts use every sale up to the prediction point, two days before
     the window, and the bar is picked on the window itself out of 26 forecasts, raw or scaled, which favours it; the
     constant factor was offered to the own forecasts (it lowers the newest window from 0.1316 to 0.1296), and the
     models go without it. The model sees only the row, the planned calendar and, in C, sales at least 44 days old.
     The comparison is as strict as the rule asks, or stricter.
   * **The benchmark's tuned methods:** the cache holds their RMSE per window, not their predictions, so they cannot
     be rescored by RMSPE. By RMSE, which is not the declared metric, the best own forecast scores 1277 / 888 / 949;
     on the shipped container RealMLP, tuned and ensembled, leads it in every window (1244 / 863 / 873), and LightGBM,
     tuned and ensembled, leads in two and is 0.7% behind in the middle one (1160 / 894 / 942). A median forecast is
     not built for RMSE, so this points the same way without settling it.
   * **What changes in the definition (B):** `_load_raw` also reads `test.csv`, for its calendar of August and
     September 2015, so counters near 31 July know the coming days; `_clean` builds each store's daily calendar from
     `train.csv` with its closed days, computes the counters, then drops the closed days as now. The 32 columns: days
     since and until a state holiday, a school holiday, a promotion day and the summer school holidays, and since and
     until the first day of each; school and state holidays this, last and next week; closed the day before; days since
     the last closure on a weekday other than Sunday, and since the store reopened after a closure of four days or
     more; a promotion the day before and the day after; Promo2 running this month, days into its cycle and weeks
     since it began; months since the competitor opened; days to month end. Each is known at the prediction point
     under the definition's own assumption that promotions, holidays and opening days are planned[^a2]. The 15 shipped
     features become 47.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Hold at `TBD -> Yes` (implemented) | the definition stays; the record waits with `Time-series (Forecasting)` | nothing new to review | the model only ties the store's own forecast in the newest window; a dataset that can pass waits |
     | B | Add 32 calendar day counters, then ship | holiday, closure and promotion counters computed before the closed days are dropped; 15 features become 47 | ahead of the best own forecast by 0.018 to 0.048 in every window (5 to 23 standard errors); no sales in the features, so the lead cannot come from the store's own series; the winner's "temporal information" | a new definition, README and checks to review; three look-ahead closure counters left out (they add nothing and would rest on planned refurbishments) |
     | C | B plus 27 trailing summaries of the store's sales | the store's mean log sales over 13 to 104 weeks by weekday, promotion and school holiday, its median and trend, all from sales at least 44 days old; 74 features | the widest lead in the newest window (0.024 against 0.018); the winner's "recent data" and "current trends" | the features carry the store's own series, which pulls the task toward forecasting; 27 more columns to check |
     | D | Ship as defined | the test read on the mean over the windows | no change | the newest window is a tie with the store's own forecast; departs from the walmart hold |

   * **Recommendation:** B. It is the smallest change that passes in every window with room to spare, and it gives
     the model only what store managers know in advance, so the lead over each store's own forecast comes from the
     calendar learned across stores. The record keeps `Yes`; after your mark I would change `dataset.py` and its notes,
     rebuild, and run the checks, the probes and this test on the built container[^a3]. **Decision:** A, B, C or D?

   **Notes for the AI:** on B, in `_clean` before the closed-day filter, build per-store daily panels over 2013-01-01
   to 2015-09-17 of `Open`, `Promo`, `StateHoliday != "0"` and `SchoolHoliday` from `train.csv` and `test.csv`
   (missing where a store has no row: the 180 stores in 2014 H2, 259 stores after 2015-07-31; a missing day counts as
   no event). Per event E in promo, state holiday, school holiday and summer (school-holiday runs of at least 28
   days): `E_since` (days since the last E day, 0 on one), `E_until` (days to the next), `E_since_start` and
   `E_until_start` (to the first day of a run); caps 30 (promo), 60 (holidays), 120 (summer); missing when none is in
   reach. `closed_yesterday` (Open == 0 the day before), `closed_nonsun_since` (days since the last closed day that is
   not a Sunday, cap 60), `refurb_since_reopen` (days since the first open day after a run of at least 4 closed days,
   cap 365), `promo_yesterday`, `promo_tomorrow`, `schoolh_` and `stateh_` counts in the row's ISO week, the one before
   and the one after (missing unless all 7 days are known), `p2_active_month` (Promo2 started on the Monday of
   `Promo2SinceWeek`/`Promo2SinceYear` and the row's month in `PromoInterval`, "Sept" = 9), `p2_days_since_cycle`
   (days since the first of the latest interval month), `p2_weeks_since_start`, `comp_months_open` ((year -
   CompetitionOpenSinceYear) * 12 + month - CompetitionOpenSinceMonth), `days_to_month_end`. The 0/1 ones are
   categorical (CLEAN-14), the rest numeric. Left out: `closed_tomorrow`, `closed_nonsun_until`,
   `refurb_until_close`. The models also read day of year, week of year, month, day and a day number from `Date`, as
   the pipeline's date encoding would. On C, add per row with cutoff = date - 44 days, from log1p of the open days'
   sales: means over 91, 182, 364 and 728 days, the count over 364, the std over 91; the same weekday over 91 and 364;
   the same weekday and promotion over 91 and 364; the same promotion over 364 and the promotion lift; the same
   school-holiday status over 728 and its lift; m91 minus m91 a year earlier; m91 minus m364; the 7-day mean ending at
   date - 361 and its difference to m91 a year before the cutoff; the same weekday a year earlier; the share of days
   open over 364; a ridge per store (intercept, day number in years, weekday, promotion; alpha 1) over 91 and 364
   days, fitted at weekly cutoffs at or before date - 44 and evaluated at the row's date, with its slope; the median
   sales by weekday and promotion over 364 days at the same weekly cutoff (minimum counts 10 per window, 3 by
   weekday, 5 by promotion or holiday; the ridge needs 30 or 100 days). TP-10 leg 1 was run as in the check of
   2026-11-04 (store-block bootstrap, 200 draws), with the own-forecast family above; the study scripts of 2026-11-05
   are the reference, and the test is re-run on the built container before the record's CC line.

   [^a1]: **TP-10** (Must): a forecasting-like panel is a tabular task when a model on the features clearly beats each
     entity's naive forecast on the shipped windows by the declared metric, and the source's top solutions are
     tabular models on point-in-time features with no lag of the target beyond its last observation (trailing
     summaries of the series allowed): "Such 'tabular forecasting' tasks exist where people want to generalise across
     entities."
   [^a2]: **CLEAN-19** (Should): we build a feature when it is what a data scientist on this task would build, taking
     the best of the top solutions' features. The winner (Rossmann_nr1_doc.pdf, "Temporal information"): "For
     temporal information I created 'day counters' to express how each record relates to certain events or cycles",
     among them "the promotion cycle", "the summer holidays" and "store refurbishments", and "features on the number
     of holidays during the current week, last week and next week".
   [^a3]: walmart_sales_in_stormy_weather was held because its model led the best own-series forecast by 1.1-1.5%
     (2026-11-02); here the lead is 14% to 33% in every window.

   **Andrej (2026-11-10, discuss):** Reply (B): Add 32 calendar day counters, then ship

   **Resolved (2026-11-10, Andrej):** B: the 32 day counters are computed in `_clean` from each store's daily calendar
   (`Open`, `Promo`, `StateHoliday`, `SchoolHoliday` of train.csv and test.csv) before the closed days are dropped; no
   counter reads sales or customers. 15 features became 47; they match the study frame of 2026-11-05 on every row.
   `task_summary` (`known`, `changes`) and a curation note say so; `dataset check` passes; the record keeps `Yes` with a
   CC line. Forecasting test re-run on the new definition, with issue 3's competitor blanking (LightGBM, one
   configuration, 3,000 trees; the bar is the best own-sales forecast picked on each window):

   | RMSPE | 2015-03-28 to 05-08 | 2015-05-09 to 06-19 | 2015-06-20 to 07-31 |
   |---|---|---|---|
   | best own-sales forecast | 0.1450 | 0.1309 | 0.1296 |
   | LightGBM, counters, before the blanking | 0.0988 | 0.1094 | 0.1135 |
   | LightGBM, counters, competitor blanked | 0.0977 | 0.1104 | 0.1139 |
   | lead in standard errors (200 store draws) | 11.9 | 3.9 | 19.8 |

   Not rebuilt (builds on the curator's ask); the test runs again on the built container.

   **Answer (AI, 2026-11-11):** the counters and the blanking are now also in the definition of the branch this
   record is on, where the test windows are not the three of the test above.
   - This branch's `temporal` declares `cutoffs=("2015-06-20", "2014-11-22", "2014-04-26")` (issue 4,
     2026-11-11): the newest six weeks, the Christmas weeks of 2014 and late spring 2014.
   - The TP-10 forecasting test above was run on the three newest windows (28 March to 31 July 2015). It has not
     been re-run on the Christmas and spring windows, so the evidence that the model beats each store's own
     forecast covers one of the three windows this branch ships.
   - `dataset check` on this branch: 0 errors, 0 warnings, 47 features over 844,392 store-days.
   - The test is re-run on the built container before the record's CC line, as the resolution says; it then runs
     on these windows.

2. **Time basis: keep three six-week windows after a one-day planning gap, and write in `splits_comment` how the sales arrive?**

   * **Problem:**
     - A day's sales exist at the end of that day, and the manager forecasts all 42 days of a window from one planning
       date; the split does the same, three 42-day windows back from 31 July 2015, each trained on every open
       store-day before a one-day gap.
     - The record's collection facts (`Samples: Over Time`, `Time: Dated`, `Target: Later`) fit and a temporal split
       needs no time-basis tag[^2a], but `splits_comment` gives the horizon and calls the day a planning gap without
       saying that every training label is final at the planning date.
     - Keep the text (A), write the time facts down (B), or test nine windows back to July 2014 (C)?
   * **Background:**
     - The gap is a planning day, not a label delay: a day's turnover is counted the same evening, so no training
       label is unknown at the planning date, and no store-day of a test window, nor the weather or holidays of its
       weeks, is in training[^2b].
     - The stores recur by design: all 1,115 train and test in every window, so a store's own past is the history a
       manager has[^2c].
     - Three windows are the protocol's three folds for a table of 844,392 rows; they train on 86.3%, 90.7% and
       95.1% of the store-days (oldest to newest).
     - The source's own test, the 48 days after the release (August to mid-September 2015, 856 stores), is not in
       the training file; the windows take its horizon from the competition's description instead.
   * **Experiments:** counts on the competition's files, no model: nine 42-day windows back from 31 July 2015 would
     start on 19 July 2014 and train on 61% to 95% of the store-days; the fourth to sixth windows add the winter and
     the Christmas weeks (31,203 to 40,176 test store-days), while the three oldest hold 934 or 935 stores, as 180
     stores have no records from July to December 2014.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Three 42-day windows, one-day gap, text as is (implemented) | late March to July 2015 | the managers' horizon; the protocol's fold count | the text does not say the labels are final at the planning date, or what the gap stands for |
     | B | The same split, with its time facts in `splits_comment` | as A; the text states that a day's sales are known that evening, that the gap is the planning day, that the stores recur by design and that the store table is one read of 2015 (issue 3) | the reasons are written where the benchmark user reads them | none found |
     | C | Nine 42-day windows back to July 2014 | the same gap and horizon; windows cover a year | Christmas and winter enter the test | three times the windows the protocol gives this size; the three oldest windows miss 180 stores; issue 1's forecasting test was run on the three windows |

   * **Recommendation:** B: the split mirrors the managers' forecast as it is, and only its reasons are missing.
     **Decision:** A, B or C?

   **Notes for the AI:** on B, replace `splits_comment` with: "The description says 'Rossmann store managers are
   tasked with predicting their daily sales for up to six weeks in advance'. A manager forecasts every day of the next
   42 days from one planning date, so each window is 42 days, predicted from the store-days up to the day before a
   one-day planning gap. A day's sales are counted that evening, so every training label is final at the planning
   date; the gap stands for the planning day, not a label delay. The stores recur by design (known stores). Three
   windows, late March to July 2015, train on 86%, 91% and 95% of the store-days. The store table (store.csv) is one
   read of 2015, merged onto every day (see curation notes)." No `data_tags` change, no record change. On C,
   `TemporalSplits(window=42, unit="days", n_windows=9, gap=1)`, re-run `dataset check` and issue 1's test on the
   nine windows.

   [^2a]: **SPLIT-32** (Should): the record carries the source's collection facts (samples, time, target); a temporal
     split needs no use-case prototype.
   [^2b]: **SPLIT-10** (Should): a gap of about the label's delay; a planning gap the use case has (a forecast made a
     day ahead) is a gap too. **SPLIT-12** (Should): the horizon is a human judgment from the source ("managers predict
     sales up to six weeks in advance").
   [^2c]: **SPLIT-13** (Should): an entity that recurs across the cutoff is part of the task when the model predicts
     for known entities. **SPLIT-15** (Should): as many windows as an IID task of that size gets folds.

   **Resolved (2026-11-06, Andrej):** B, accepted through the cross-dataset item "Accept the arrival notes on temporal
   splits with one mark?" `splits_comment` is replaced by the drafted text (labels final at the planning date, the gap
   as the planning day, known stores, the store table as one read of 2015). The split, its gap and `data_tags` are
   unchanged; a temporal split takes no time-basis tag.

3. **Show a store's competitor only from its opening month, since the store table is one read of 2015?**

   * **Problem:**
     - `store.csv` is one table read at the release and merged onto all 942 days, so 8.7% to 9.4% of each window's
       training store-days (191 stores) carry the distance of a competitor that had not opened yet, and 396 to 1,024
       test store-days per window (11 to 31 stores) carry a competitor that opens after the planning date.
     - The opening moves the target: over the 8 weeks after a competitor opens, a store's log sales fall by 0.044 on
       average (105 of 160 stores fall), against a rise of 0.010 at random dates (43% fall).
     - Blank the competitor's distance and opening date before the opening month (B), also show the Promo2 scheme
       only from its start (C), or keep the table as read (A)?
   * **Background:**
     - With the date and the opening month in the same row, a model can learn the drop at an opening from the
       training stores and place it in a test window for a competitor that opens weeks after the planning date,
       which the manager may not know then[^3a].
     - The other release-time column, `Promo2`, is 1 on 7.1% to 7.8% of the training store-days before its start
       week, and 0 to 297 test store-days per window (up to 9 stores) start it after the planning date; the scheme is
       the company's own plan, known ahead, so this is no leak, only a row that reads the table rather than the
       day[^3b].
     - 354 stores have no opening date for their competitor; their distance cannot be dated and stays as read.
   * **Effect on the task:** small in rows (1% to 3% of a window's test store-days), but these are the rows where the
     table knows something about the window that the planning date did not; the rest of the task is untouched.
   * **Experiments:** counts on the competition's files (open store-days, the shipped windows), no model; the effect
     of an opening compares each store's mean log sales by weekday and promotion over the 8 weeks before and after the
     opening month's first day (160 stores whose competitor opened from April 2013 to June 2015), with 400 stores at
     random dates as the reference.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the table as read (implemented) | every day carries the 2015 values | no change | a test store-day can carry a competitor that opens after the planning date; old rows describe a competitor that did not exist yet |
     | B | Competitor as of each day | `CompetitionDistance` and `CompetitionOpenSince*` missing on store-days before the opening month | removes the located late cells; the smallest change | test store-days after an opening that falls inside the window still carry it (216, 82 and 307, newest window first), as the definition cannot hold features per window |
     | C | B, and Promo2 as of each day | as B; also `Promo2` 0 and its start and interval missing before the start week | every store column says what the day knew | changes a planned scheme that is no leak; more to review |

   * **Recommendation:** B: these cells are late and can be located, which is what the rule asks to blank, and the
     change is three columns on one condition. **Decision:** A, B or C?

   **Notes for the AI:** on B, in `_clean` after the merge: `comp_open = pd.to_datetime(dict(year=
   CompetitionOpenSinceYear, month=CompetitionOpenSinceMonth, day=1))` where both are present; on rows with `Date <
   comp_open` set `CompetitionDistance`, `CompetitionOpenSinceMonth` and `CompetitionOpenSinceYear` to missing. On C,
   also on rows with `Promo2 == 1` and `Date` before the Monday of ISO week `Promo2SinceWeek` of `Promo2SinceYear`:
   `Promo2 = 0`, `Promo2SinceWeek`, `Promo2SinceYear` and `PromoInterval` missing. If issue 1's B or C lands, compute
   `comp_months_open` after the blanking (missing before the opening). A curation bullet: "The store table is one read
   of 2015 merged onto every day: a competitor is shown only from its opening month (8.7% to 9.4% of the training
   store-days, 191 stores, carried a competitor not yet open; a store's log sales fall 0.044 in the 8 weeks after an
   opening against +0.010 at random dates); 354 stores without an opening date keep the distance as read." CHANGELOG
   entry, `dataset check`, rebuild on the curator's ask.

   [^3a]: **LEAK-10** (Must): a feature holds only what existed at the prediction point; out are attributes looked up
     after the outcome; a value read at a later pull goes where its late cells can be located: they are blanked
     (zillow_prize, melbourne_housing_market). **LEAK-7** (Should): the smallest fix that keeps a valid signal.
   [^3b]: **LEAK-37** (Must): an input the actor knows at the prediction point is not a leak, even one the company set
     itself.

   **Andrej (2026-11-11, change):** Option B: Competitor as of each day.

   **Resolved (2026-11-10, Andrej):** B: in `_clean` after the merge, `CompetitionDistance`, `CompetitionOpenSinceMonth`
   and `CompetitionOpenSinceYear` are missing on the store-days before the competitor's opening month (70,108 open
   store-days, 8.3%, of 191 stores); `comp_months_open` is computed after the blanking, so it is missing there too. The
   354 stores without an opening date keep the distance as read; Promo2 stays as read. Curation note added; `dataset
   check` passes; the forecasting test still passes (issue 1).

4. **Which six weeks should the test windows be?**

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
   has the decision CC line. `dataset check`: 0 errors, 0 warnings. (Reviewed as issue 1 of the horizon review of 2026-11-11; renumbered 4
   when that review and the BeyondArena v0.2 review of this dataset were merged into the record on 2026-11-11.)

## Reference

FlorianKnauer and Will Cukierski. Rossmann Store Sales. https://kaggle.com/competitions/rossmann-store-sales, 2015. Kaggle.
