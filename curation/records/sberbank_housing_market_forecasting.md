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

CC (2026-11-11, Lennart): REVIEW.md issue 1 ("Agree.", to the answer that the windows follow the length of the horizon sign-off): the three seven-month windows of the horizon replace the five half-years from January 2013, whose three oldest trained on 44.3%, 28.6% and 17.8% of the sales.

CC (2026-11-11, Lennart): the declared horizon (7 months, no gap, windows starting 2014-12-01, 2014-05-01 and 2013-10-01) is checked, as seven months is the shortest test period of the sources (TabReD's; the competition tests eleven months), where the half-year was our own assumption; the window under half the sales, October 2013 to April 2014 on 35.4%, beside 83.6% and 59.1%, is signed off with it (REVIEW.md horizon, a: "Reply (a): Seven months"; SPLIT-14 as amended 2026-11-11).

**Assessment (AI, 2026-11-11):** applied the horizon (a) and issue 1: `temporal` declares `TemporalSplits(window=7, unit="months", cutoffs=("2014-12-01", "2014-05-01", "2013-10-01"))`, confirmed with `window_bounds` on the definition's frame. Test 4,647, 6,936 and 6,704 sales (mean log price per square metre 11.84, 11.82, 11.80); train 23,674, 16,738 and 10,034 (83.6%, 59.1%, 35.4% of 28,321). The windows are adjacent: moving the oldest back lowers its train side (33.3% from September 2013, 31.1% from August). `accepted_check_warnings` takes `splits_train_under_half` with the sign-off; `dataset check`: 0 errors, 0 warnings, no `splits_floor_core` (the five half-years had three windows under half).

## Reference

Alex Matveev, Anastasia_Sidorova_50806198, and DataCanary. Sberbank Russian Housing Market. https://kaggle.com/competitions/sberbank-russian-housing-market, 2017. Kaggle.
