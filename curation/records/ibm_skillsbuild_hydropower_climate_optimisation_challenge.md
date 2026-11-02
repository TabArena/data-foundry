---
unique_name: ibm_skillsbuild_hydropower_climate_optimisation_challenge
name: ibm-skillsbuild-hydropower-climate-optimisation-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Time-series (Forecasting)
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Other
source_links:
- https://zindi.africa/competitions/ibm-skillsbuild-hydropower-climate-optimisation-challenge/data
source_row: 871
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: the proposed fast reject (SEL-10) did not hold in the reject check, so it stays a candidate with the doubt listed.
- Proposed reject (refuted): `No` (`Time-series (Forecasting)`, SEL-10): the task is to "forecast the total daily energy consumption (kWh) per data user for one month into the future" from 5-minute meter series.
- Source: Zindi with IBM SkillsBuild (2025-03-03 to 2025-04-14, 1,241 participants); data curated by CISNR, UET Peshawar, from micro-hydropower plants in the Kalam region of Pakistan. As published: Data.zip (166 MB) of 5-minute readings per consumer device and data user (voltage per phase, current, power factor, kWh) and Climate Data.zip (temperature, dew point, wind speed, precipitation); submission rows are user-days of the following month.
- Use case: load planning of an off-grid micro-hydropower plant; the prediction is future values of each user's consumption series over a one-month horizon.
- Siblings and duplicates: none among `curation/records/`.
- Papers and pages: the Zindi page; top solutions not read.
- Metric: RMSE on daily kWh (Zindi Evaluation page), a leaderboard metric.
- Counterpoint for the checker: the workbook note says "time-series, but the 1st place solution is tabular"; a tabular model on lagged or calendar features is still a forecast of the series, and SEL-11 / TP-10 would need the naive-profile test and top solutions without lagged targets, which cannot be shown from the source.
- Reject check (AI, 2026-10-22): does not stand. The source says it is a forecast ('forecast the total daily energy consumption (kWh) per data user for one month into the future', https://zindi.africa/competitions/ibm-skillsbuild-hydropower-climate-optimisation-challenge). But it is a panel of users, and the 1st-place write-up (https://zindi.africa/competitions/ibm-skillsbuild-hydropower-climate-optimisation-challenge/discussions/26290) uses LightGBM on daily climate, calendar, holiday and Ramadan features with 5-fold CV and names no lagged target. SEL-11/TP-10 can bring it back into scope, and only the naive-profile measurement on the data can settle that.
- For /add-dataset: TBD -> 2nd Tier, priority 4. Add stage: run TP-10 (a model on the features against each user's naive daily profile); check whether the test month comes with 5-minute voltage, current or power-factor readings (if so, kWh is close to V*I*PF: Trivial or LEAK); read the 1st-place notebook (discussion 26337) for lagged targets; temporal split by month.
- Priority set to 2 by the main session (the checker proposed 4), like the other refuted forecasting-like panels (grocery_store_product_forecasting_challenge, uber_movement_sanral_cape_town_challenge): the TP-10 risk takes a point off.

Zindi IBM SkillsBuild hydropower/climate challenge, flagged as time-series but with a note that the winning solution was tabular. The framing (predicting/optimizing hydropower output from climate inputs over time) leans toward forecasting, which is out of scope, yet the tabular winning approach suggests it might be reframable as a fixed predictive regression with a temporal split. It likely needs substantial wrangling of climate/operational data. A human must determine whether the target is a genuine static prediction vs. a horizon forecast and assess data size/quality; keep in 2nd tier pending that.

---

time-series, but the 1st place solution is tabular
