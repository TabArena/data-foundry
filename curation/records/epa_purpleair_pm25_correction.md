---
unique_name: epa_purpleair_pm25_correction
name: 'Dataset: Development and application of a United States-wide correction for PM2.5 data collected with the PurpleAir sensor'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: GOV Website
year: '2021'
domain: environmental science & climate
problem_type: Regression
source_links:
- https://doi.org/10.23719/1522388
- https://doi.org/10.5194/amt-14-4617-2021
- https://catalog.data.gov/dataset/dataset-development-and-application-of-a-united-states-wide-correction-for-pm2-5-data-coll
- https://pasteur.epa.gov/uploads/10.23719/1522388/Data_DevelopmentUSPAcorrection_210408.zip
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: EPA's national collocation set behind the PurpleAir PM2.5 correction that the AirNow Fire and Smoke Map applies, about 12,000 sensor-days at 39 sites in 16 states; few, strong features and a near-linear relation make `Trivial` the question to probe.
- Source: Barkjohn, Gantt and Clements, "Development and application of a United States-wide correction for PM2.5 data collected with the PurpleAir sensor", Atmospheric Measurement Techniques 14, 4617-4637, 2021 (doi:10.5194/amt-14-4617-2021); data on EPA ScienceHub, doi:10.23719/1522388 ("A dataset of 24-hr averaged PurpleAir data collocated at government monitoring sites", `Data_DevelopmentUSPAcorrection_210408.zip`, EPA Office of Research and Development, 2021-05-04). As published (paper): "almost 12 000 24 h averaged PM2.5 measurements" from 50 sensors at 39 sites in 16 states, September 2017 to January 2020 (Sect. 2.1, 3.3); target the collocated FRM or FEM PM2.5; inputs the PurpleAir PM2.5 channels A and B, relative humidity, temperature and dew point (Sect. 4.1). The zip's columns were not read.
- Use case: EPA, when it shows a PurpleAir sensor on the AirNow Fire and Smoke Map, converts the sensor reading to an estimate of regulatory PM2.5 (abstract: "This correction equation, along with proposed data cleaning criteria, has been applied to PurpleAir PM2.5 measurements across the US on the AirNow Fire and Smoke Map"); fit direct; regime grouped by site or state (the paper's leave-one-state-out cross-validation, Sect. 5.1, mirrors sensors in new places), with its leave-out-by-date scheme as the alternative.
- Siblings and duplicates: `airqo_low_cost_air_quality_monitor_calibration_challenge` (`TBD -> Yes`, priority 4; Kampala, hourly) and its hackathon copy `airqo_low_cost_air_quality_monitor_calibration_challenge_2` (`No`); `senseurcity_low_cost_sensor_calibration` (three European cities); `air_quality_prediction_from_low_cost_iot_devices` (`TBD -> 2nd Tier`, the record this was found next to). The same task from other sources (PROV-7). External collections: none found.
- Better data: found as a related task next to `air_quality_prediction_from_low_cost_iot_devices` (the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: the AMT paper (Sect. 4.1.1 model selection, 5.1 cross-validation, 5.3 the final equation PM2.5 = 0.524 x PA(cf_1) - 0.0862 x RH + 5.75).
- Metric: RMSE, by which the paper picked the best model at each level of complexity ("RMSE was used to determine the best models of each increasing level of complexity moving forward", Sect. 4.1.1); MAE, MBE and Spearman correlation are reported beside it, and the final equation was chosen as "the most robust" (Sect. 5.2); declare `rmse` (MET-5); inputs none.
- Risks for /add-dataset: few features and a near-linear relation, so the agency's two-variable linear fit is the baseline to beat (TP-4: a probe, not a verdict); the A and B channel agreement filter and the excluded sensors (Sect. 3.3) decide which rows ship; FRM against FEM reference monitors (keep the type as a column); site and state ids are split metadata (LEAK-33).
- Priority: gap 0 (environmental science and regression are not thin), use case + (the Fire and Smoke Map correction, named by the source), source + (EPA dataset DOI and peer-reviewed paper), shape + (about 12,000 rows with site groups, though few features), risk - (near-linear target, `Trivial` to probe).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `air_quality_prediction_from_low_cost_iot_devices`.
- as published: almost 12,000 24-h averages from 50 PurpleAir sensors at 39 regulatory sites in 16 states, September 2017 to January 2020; one zip; target: 24-h FRM/FEM reference PM2.5 at the collocated monitor; access: open (EPA ScienceHub).
- Why: low-cost sensor calibration for PM2.5 instead of CO2; the same task as airqo_low_cost_air_quality_monitor_calibration_challenge(_2), with an agency source and a deployed use
- Adds: a national, agency-published calibration set with a paper and an operational user
