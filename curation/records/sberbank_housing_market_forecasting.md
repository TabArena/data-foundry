---
unique_name: sberbank_housing_market_forecasting
name: Sberbank Housing
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
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

## Reference

Alex Matveev, Anastasia_Sidorova_50806198, and DataCanary. Sberbank Russian Housing Market. https://kaggle.com/competitions/sberbank-russian-housing-market, 2017. Kaggle.
