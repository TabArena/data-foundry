# rain_in_australia

**Outcome:** added. Will more than 1 mm of rain fall at a station by 9 am tomorrow, predicted at 9 am from that
morning's observations and the ten later columns of the day before, on rattle's full weatherAUS file (2007-2026).
Temporal: nine 14-day test windows, one every six weeks. The AI recommends shipping it; the forecasting scope is
open.

**Main points:** Predicted at 9 am; next-row labels dropped; 14-day windows every 6 weeks; the original rattle file.

**Record fields that disagree with the definition:**

- `year`: record `2017`, definition `2026`.

**Record judgment:** valid with concerns: the forecasting scope (issue 4), which the curator's comment already
weighs.

**Issues for Lennart:**

2. **Test windows: 14 days every 6 weeks (implemented) or monthly?** Your comment on
   `climate_model_weather_forecasting` ("TabRed uses 1 month refit horizon. For weather this is a bit much. I would
   argue for one or two weeks at most?") sets the horizon. Implemented: `TemporalSplits(window=14, unit="days",
   n_windows=9, step=42)`, 9 two-week windows 2025-02-15 to 2026-01-30 that cover every season, 622-642 rows and 63-205
   rain days each. No other dataset spaces its windows yet (step larger than the window). Alternatives (README,
   decision 4): contiguous 14-day windows cover only 2025-09-27 to 2026-01-30 (619-640 rows, 83-205 rain days); 7 days
   every 6 weeks: 309-322 rows, 27-100 rain days; monthly: May 2025 to January 2026, 1,333-1,417 rows, 192-400 rain
   days; yearly: only 7 windows above the 50% train floor.

3. **Source version: original rattle file (implemented) or the Kaggle snapshot of the record?** The Kaggle file
   (record's `source_links`) is a snapshot to 2017-06-25: 145,460 rows, 140,787 after the first cleaning, no `RISK_MM`
   (a 2019 discussion thread still asks about it; the current Kaggle file is the version of 2020-12-11). The rattle
   file adds 2017-07 to 2026-01 but lacks 2016-01-27 to 2017-02-28 (the snapshot has it), and 1,135 of the 125,900
   rows both hold (0.9%) differ in at least one value (580 Rainfall, 184 RainTomorrow cells), so old values change
   between versions of the file. The definition uses `source = "GOV Website"` (the Bureau of Meteorology) and
   `year = "2026"`; the record says 2017.

4. **Scope: forecasting or a fixed predictive task?** The target is the next value of a station's rain series, which
   the `el_nino_dataset` reasoning ("We do not predict a target that we would not automatically obtain at time point
   t") would call forecasting. The skill comes from the morning observations, not from the series: on the 9 monthly
   windows of the first version (verifier's run, LightGBM) ROC AUC is 0.856 with all features, 0.855 without Rainfall
   and RainToday, 0.732 with only the station's rain series, station and calendar, and 0.650 with station and
   calendar alone (log-loss skill 31.2%, 30.8%, 13.2%, 5.6%). Andrej accepted it ("Time-series data, but target is
   lagged. Might work as a task."), and `climate_model_weather_forecasting_1m` and `bias_correction` (Yes) are
   one-step weather tasks with covariates, so the dataset is added; the question stays open for you.

5. **Rows without their own 9 am rain reading dropped (2,575).** BoM: "Sometimes when the daily maximum and minimum
   temperatures, rainfall or evaporation are missing, the next value given has been accumulated over several days
   rather than the normal one day" (BoM notes, Data availability). These rows are 42.6% rain days against 21.8%, with
   a median next reading of 0.4 mm against 0.0 mm, so their label can cover 48 hours or more. Alternative: keep them
   (the model then learns the missing reading as a rain signal).
