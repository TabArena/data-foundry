# g_research_crypto_forecasting

**Outcome:** added as `g_research_crypto_forecasting_1m`; recommended `No` (`Time-series (Forecasting)`). A
regression of each asset's residualised 15-minute return, temporal with three 91-day windows, with the 3rd-place
solution's lagged-return features added because a row's own bar has no signal. Even with them R² against the train
mean stays near 0. The AI recommends `No` unless the record's forecasting-as-tabular acceptance covers this case.

**Main points:** The competition is forecasting, and the RMSE signal is near zero.

**Record judgment:** valid with concerns: by its own description the competition is time-series forecasting, which
the guidelines exclude (issue 1); the record accepts it as a forecasting-as-tabular task.

**Issues for Lennart:**

1. **Scope: forecasting (recommendation: `No` + `Time-series (Forecasting)` unless you confirm the record's acceptance
   for this case).** Evidence: the competition calls itself "a forecasting competition" (Timeline) and served rows one
   minute at a time through a time-series API; the target is the asset's own Close(t+16)/Close(t+1) - 1, residualised
   against the market (rebuilt from Close by the verifier, median error 5e-7); the bar alone correlates 0.012, -0.006
   and 0.002 with it, so all the signal comes from the 18 lags of the same Close series that the definition adds. It
   would be the only working-copy dataset built on lagged targets (numerai ships the source's point-in-time features;
   rossmann and ashrae use exogenous inputs, and ashrae in this run draws the line at "no lagged targets"). The record's
   first comment predicted "will likely mostly be noise". Implemented now: added under the record's one-line acceptance
   ("Forecasting-as-tabular task"), with the lagged-target design named in the scope bullet. Alternative: retire, as
   `cryptocurrency_closing_price_prediction`, `appliances_energy_prediction` and `combined_cycle_power_plant` were.

2. **Engineered history features.** Question: may the definition add the 3rd-place solution's 18 lagged-return features?
   The house rule allows feature engineering only to remove leaks or rebuild destroyed meaning. Evidence: without them
   the task has no signal (correlation about 0.00 in all three windows); with them it is 0.037-0.051. Precedents:
   `electric_motor_temperature_prediction` adds the paper's EWMA features, and `acquire_valued_shoppers_challenge` uses
   TabReD's aggregation from a top solution. Implemented now: own-asset features plus 14-asset means and differences,
   one row per asset and minute. Alternatives: the raw bars only (a no-signal task), or the solution's wide layout with
   every asset's features in every row (174 columns).

3. **Near-zero signal under RMSE.** Question: is a task whose best measured R² is +0.0012 (correlation 0.03-0.05) a
   useful benchmark? Evidence: untuned models score below the train-mean predictor on RMSE while still correlating 0.04,
   so method rankings will hinge on shrinkage. The competition's weighted Pearson correlation would be a
   dataset-specific metric, and the adapter does not use those yet (BENCHMARK_CHANGES_TODO.md, "Dataset-specific
   metrics"). R² below 0 against the train mean holds for the untuned models only: in my runs untuned LightGBM is below
   the mean in all three windows (R² -0.002 to -0.006), but ridge (alpha 1) beats it in window 1 (+0.0008) and ties it
   in window 0 (-0.0000005), and the regularised models beat it in windows 0 and 1 (early-stopped LightGBM +0.00073 and
   +0.00115, tuned ridge +0.00048 and +0.00111) and not in window 2 (LightGBM -0.00028, ridge -0.0040), while
   correlating 0.015-0.035 in every window. By task_probes.md rules 1-2, `no_signal` from untuned models is a question,
   not a retirement reason; a method does beat the mean, so the signal is small but real, about a tenth of forest_fires'
   R² 0.013. The verifier's day-block analysis: early-stopped LightGBM R² 95% intervals [-0.0001, 0.0016], [0.0002,
   0.0022], [-0.0021, 0.0017], so only window 1's gain is outside the day-to-day noise; it is not distinguishable from
   tuned ridge day by day (paired t 0.72, 0.17, 1.48); its daily correlation is positive on 73, 70 and 78 of 91 days (t
   7.0, 6.6, 9.2). Under RMSE the ranking measures shrinkage, under correlation it measures signal. Implemented now:
   RMSE (default), with the `unstable` answer rewritten to these numbers. Proposal: register the competition's
   correlation once dataset-specific metrics are supported (BENCHMARK_CHANGES_TODO.md), as for `numerai_v5_2_1m`; or do
   not add the dataset (issue 1).

4. **Windows.** Implemented: 3 x 91 days with a 1-day gap, from the competition's 3-month live scoring; each window
   holds about 1.83M rows before sampling. Alternative: `TemporalSplits(window=3, unit="months", n_windows=3)` covers
   the same span, but its gap would have to be a whole month; shorter windows would leave the frame unchanged in size
   but test less time.

5. **Grouped by asset not used.** The record's `required_split` also lists `Grouped (NON-IID)`, and GETTING_STARTED says
   "temporal + grouped ... (anonymisation)". I chose temporal only: the competition forecasts the same 14 assets, and 14
   groups would only test a shift between assets (the covertype precedent). The assets are named in asset_details.csv,
   so the `Anonymized` tag does not apply.
