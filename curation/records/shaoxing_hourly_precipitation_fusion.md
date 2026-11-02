---
unique_name: shaoxing_hourly_precipitation_fusion
name: Two-stage multi-source hourly precipitation fusion, Shaoxing (rain gauges, radar QPE, IMERG)
checked_by:
- Andrej
suggestion: TBD -> Yes
priority: 2
decision_markers:
- Available on Request
tags:
- Two-Regime Zeros
original_source: Other
year: '2026'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.3390/atmos17080762
- https://www.mdpi.com/2073-4433/17/8/762
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> Yes`, priority 2: hourly rain at gauges held out from training, estimated from
satellite (IMERG) and radar estimates, terrain and time, is a real fusion task with a station-grouped split; the derived
table has to be requested from the authors.
- Source: Wang, Zhao, Ding et al. (2026), Atmosphere 17(8):762 (MDPI, read from the PDF). Abstract: "After quality
  control, the dataset comprised 41,458 hourly station samples from 72 rain gauges" in Shaoxing's 2025 flood season,
  with "A 61-dimensional feature set ... integrating satellite precipitation estimates, weather-radar precipitation
  estimates from the Zhejiang radar network, temporal-lag and accumulation statistics, neighborhood descriptors, cyclic
  time variables, and terrain-derived interaction features, with gauge observations used as the training target". The
  lags and windows are of the IMERG and radar inputs, not of the gauges (Sec. 3.1: "For each precipitation source x
  (GPM IMERG or radar QPE), lagged predictors and moving-window statistics were calculated using only information
  available at or before the target hour"). Not deposited; Data Availability Statement (pp. 21-22): "The rain-gauge
  observations and operational radar QPE data ... are not publicly available due to data-use restrictions. The derived
  datasets are available from the corresponding author upon reasonable request, subject to approval by the original
  data providers."
- Target and zeros: the gauge's hourly total; Sec. 2.2: "A threshold of 0.1 mm h-1 was used to distinguish rainy and
  non-rainy samples", so dry hours are an observed regime (trace counted as dry), and the paper's model is a hurdle
  (LightGBM occurrence, XGBoost residual on rainy hours, Sec. 3.2-3.3).
- Use case: Sec. 1: "Accurate high-resolution precipitation information is a prerequisite for flash-flood warning,
  hydrological forecasting, and hydrological risk management"; for example a provincial hydrological service estimating
  hourly rain at ungauged 1 km cells for flash-flood warnings. No actor named; fit approximate: the inputs use IMERG
  Late Run (Data Availability Statement), whose target latency is 14 hours (GES DISC catalogue), so a product made at
  the target hour would have the Early Run instead. Regime grouped by gauge: "The stations were divided at the station
  level into a 57-station development set and a fixed 15-station held-out spatial test set" (abstract), which mirrors
  estimating where no gauge stands (SPLIT-4).
- Siblings and duplicates: none in the records (searched precipitation, radar, IMERG, Shaoxing).
  `bias_correction_r_bias_correction_r_2` (Yes, Andrej) is the precedent for correcting a gridded product at stations
  with the product as an input (USE-6); `how_much_did_it_rain` estimates gauge rain from radar alone, without station
  ids. External collections: none found.
- Papers and pages: the paper only (doi:10.3390/atmos17080762).
- Metric: several reported side by side (POD, FAR, CSI and F1 for occurrence; CC, RMSE, MAE, R² and bias for amounts,
  Sec. 3.4); MAE on rainy samples is only the tuning objective of the second stage (Sec. 3.3), so no single deliberate
  metric: the fallback `rmse` (MET-5). Inputs: the station id for the split, to confirm in the derived table.
- Risks for /add-dataset: missing radar values and record-start lags are filled with 0 (Sec. 3.1: "Missing values
  caused by insufficient temporal history at the beginning of records were filled with zero"; a `QPE_available` flag
  marks missing radar), to recode as missing (CLEAN); the IMERG latency at the prediction point (USE-3); one season at
  72 gauges. Open policy question: coded zeros (trace below 0.1 mm as dry). Access only on request, subject to the
  providers' approval, is a note and no reason for the verdict or a marker (EV-4); the earlier `Not Available (from
  Paper))` is dropped, since whether the table can be obtained is not known yet (`Data Requested` once asked).
- Priority: gap 0 (environmental science, regression, grouped: none thin), use case 0 (application named, actor not),
  source + (paper with a 61-feature appendix), shape + (41,458 gauge-hours, 61 features, 72 gauges), risk - (IMERG
  latency at the prediction point, zero-filled feature gaps).

**Assessment (AI, 2026-10-30):** The family's open question on coded and censored zeros is settled (Andrej, 2026-10-30,
policy question 2 of the zero-inflated review: "We don't care. We want to add any relevant predictive task, independent
if it is zero inflated or not"), so how the source codes its zeros is no reason for a No or a lower priority. Trace
below 0.1 mm counted as dry is the source's convention and stays as recorded. The verdict and priority stay.

CC (2026-10-30, Andrej): `TBD -> 2nd Tier`, priority 2 (the AI screening had `TBD -> Yes`, priority 2; zero-inflated
screening review page). "Since the table has to be requested we shelf it for now"

CC (2026-10-30, Andrej), in chat: `TBD -> Yes`, priority 2: "Data on request shall be a TBD then for the cases where it
mattered." The verdict rests on the merits; `Available on Request` records that the request is still to be made (EV-4:
access alone decides no verdict).

Gauge-hour precipitation fusion for Shaoxing: 41,458 hourly samples from 72 rain gauges in the 2025 flood season,
61 features (IMERG, radar QPE with an availability flag, lags and accumulations, neighbourhood, terrain), a LightGBM
wet/dry stage and an XGBoost intensity stage, and a fixed 15-station spatial test set (abstract). The table is not
released. Data Availability Statement (pp. 21-22): "The rain-gauge observations and operational radar QPE data ...
are not publicly available due to data-use restrictions. The derived datasets are available from the corresponding
author upon reasonable request, subject to approval by the original data providers." Unreleased paper data, so the
precedent is `No` with `Not Available (from Paper))`. The task itself (a measured target, grouped by gauge) would be
in scope if the authors deposited the table.

Zero mechanism, from the paper only: dry hours are a threshold. Sec. 2.2: "A threshold of 0.1 mm h-1 was used to
distinguish rainy and non-rainy samples", so trace rain counts as dry. Missing radar values are set to 0 and flagged.

## Reference

Wang H., Zhao L., Ding K., Liu F., Zhang R., Chen L., Qin J., Cao P., Wang S. (2026). A Two-Stage Machine Learning
Framework for High-Resolution Multi-Source Precipitation Fusion in Complex Terrain: A Case Study of Shaoxing, China.
Atmosphere 17(8):762. doi:10.3390/atmos17080762.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 47 (Precipitation fusion - Shaoxing).
