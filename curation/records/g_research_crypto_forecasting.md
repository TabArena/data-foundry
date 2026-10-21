---
unique_name: g_research_crypto_forecasting
name: G-Research Crypto Forecasting
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
- Review Prio 1 (Atlas)
collections:
- New (BeyondArena)
original_source: Kaggle
year: '2021'
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/competitions/g-research-crypto-forecasting/data?select=train.csv
v2_path: datasets/_dev/tabarena-v0pt2/g_research_crypto_forecasting_1m/dataset.py
source_row: 707
type_adapter_id: curation-record-v1
---

## Comments

CC: "Stock data could be used, requires very specific splits and a lot of preprocessing, given its raw form, could try as is but will likely mostly be noise "

Forecasting-as-tabular task. Unsure if timestamps exist to create real splits. Would need some thought how to subsample

Solved with LGBM twice, training data seems to have enough data for creating our own splits for the future: https://www.kaggle.com/code/sugghi/training-3rd-place-solution

CV was temporal

**Assessment (AI, 2026-10-07):** This is time-series forecasting by the guidelines: the competition calls itself "a forecasting competition" (Timeline), and the target is the asset's own Close(t+16)/Close(t+1) − 1, residualised against the market (rebuilt from Close, median error 5e-7). The one-minute bar alone correlates 0.012, −0.006 and 0.002 with it on three 91-day windows; all signal comes from 18 lags of the same Close series (3rd-place solution), the only lagged-target design in the working copy. Even then R² against the train mean is +0.0007, +0.0012, −0.0003 (only the middle window outside day-to-day noise). Suggest `No` + `Time-series (Forecasting)` unless the "Forecasting-as-tabular" acceptance is meant for this case; the definition `g_research_crypto_forecasting_1m` is ready either way.

**Assessment (AI, 2026-10-20):** priority 3 for the review of the added dataset: gap -, use case +, source +, shape +, risk - (Issue 1: time-series forecasting on lagged targets; run recommends No). Out of scope as time-series forecasting: signal comes only from lagged returns and R² stays near zero under RMSE.

**Assessment (AI, 2026-10-20):** review panel (full): don't ship, `No` + `Time-series (Forecasting)` (SEL-10, TP-10 fail on both legs: LightGBM R² +0.0006 / +0.0013 / +0.0004 against the coin's mean, no window outside the day-to-day noise; the added lagged-return features correlate 0.80-0.83 with sums of the coin's own past targets); keeping it needs a TP-10 amendment. These numbers replace those of the 2026-10-07 assessment. Applied: notes corrected (scope, signal and early-stopping numbers, wording), negative `Volume` set to missing, History note. Priority 3: gap 0, use case +, source +, shape +, risk - (recommendation not to ship).

CC (2026-10-21, Lennart): the declared metric documents the original use case's metric; overrule it only when it is biased or wrong (evidence from the paper); keep the note of the original metric (TP-6 amended).

**Assessment (AI, 2026-10-21):** metric set to `pearsonr` (was the default RMSE) for the competition's "Weighted Correlation Coefficient" (Kaggle API), a Pearson correlation with each row weighted by its asset's `Weight` (1.10 to 6.78). On the shipped windows, over seven predictions per window (ridge with two penalties, four LightGBM sizes, one raw feature), pooled Pearson ranks them as the weighted correlation in all three windows (Kendall tau 1.0), within 0.008 of it. The notes name the original and its weights. Moot if the dataset is retired (REVIEW.md issue 1). Needs a rebuild to reach the container.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source weighted_pearsonr inputs weight=Weight — the Kaggle evaluation's weighted Pearson correlation, each row weighted by its asset's Weight from asset_details.csv, now a scoring column (replaces the pooled pearsonr stand-in). Needs a rebuild to reach the container.

## Reference

Alessandro Ticchi, Andrew Scherer, Carla McIntyre, Carlos Stein N Brito, Derek Snow, Develra, dstern, James Colless, Kieran Garvey, Maggie, Maria Perez Ortiz, Ryan Lynch, and Sohier Dane. G-Research Crypto Forecasting . https://kaggle.com/competitions/g-research-crypto-forecasting, 2021. Kaggle.
