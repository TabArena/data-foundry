---
unique_name: spatio_temporal_beam_level_traffic_forecasting_challenge
name: spatio-temporal-beam-level-traffic-forecasting-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Time-series (Forecasting)
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: technology & internet
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://zindi.africa/competitions/spatio-temporal-beam-level-traffic-forecasting-challenge/data
source_row: 886
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Time-series (Forecasting)`, SEL-10): forecast future hourly traffic volume per beam from the past five weeks of the same and three companion series.
- Source: Zindi competition by ITU AI for Good, 24 July to 11 October 2024, 742 participants, 12,000 CHF (https://zindi.africa/competitions/spatio-temporal-beam-level-traffic-forecasting-challenge, read through the Zindi API); as published: four wide hourly tables (traffic_DLThpVol, DLThpTime, DLPRB, MR_number; about 35-39 MB each) for 2,880 beams (30 base stations x 3 cells x 32 beams) over five weeks; licence CC-BY-SA 4.0.
- Use case: network resource planning by an operator; the task is a multi-horizon forecast of the series itself (weeks 6 and 11), with no other features than the series.
- TP-10 cannot rescue it: there are no non-lag features; the curator's note that the first place used tree models does not change the task (trees on lags are still forecasting).
- Metric: MAE (Zindi Evaluation page).
- Reject check (AI, 2026-10-22): stands. SEL-10 (Must), from the source's words: "The objective of this challenge is to develop a multivariate time series forecasting model for traffic volume (DLThpVol) at the beam level"; "We remind the participants that the objective is to forecast future values of traffic volume"; target weeks 6 and 11 after five weeks of history, type_of_problem Forecast (https://api.zindi.world/v1/competitions/spatio-temporal-beam-level-traffic-forecasting-challenge). The only files are the four hourly series, with nothing given for the target weeks, so every feature is a lag of the target or of a companion series. TP-10 leg (2) cannot hold, whatever model type the winner used.

A Zindi challenge to forecast spatio-temporal beam-level cellular traffic. The name and the comment ('time-series') make clear this is forecasting future traffic over a horizon, which is explicitly out of scope for the benchmark even though the winning solution used tree models. The forecasting setup (predicting future values per beam/time) is not a fixed predictive task that merely needs a temporal split. Recommend reject; a human could confirm there is no reframable fixed-target variant.

---

time-series, but 1st place solution uses tree-based models
