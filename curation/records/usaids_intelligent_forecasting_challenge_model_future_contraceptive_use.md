---
unique_name: usaids_intelligent_forecasting_challenge_model_future_contraceptive_use
name: usaids-intelligent-forecasting-challenge-model-future-contraceptive-use
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Time-series (Forecasting)
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://zindi.africa/competitions/usaids-intelligent-forecasting-challenge-model-future-contraceptive-use
source_row: 918
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: the proposed fast reject (SEL-10) did not hold in the reject check, so it stays a candidate with the doubt listed.
- Proposed reject (refuted): `No` (`Time-series (Forecasting)`, SEL-10): monthly consumption of 11 contraceptives at 156 sites, predicted for the next three months from 42 months of history.
- Source: USAID's Intelligent Forecasting Challenge (<https://competitions4dev.org/forecastingprize>), mirrored on Zindi 27 Jul to 30 Aug 2020 (526 participants, read through Zindi's API, <https://zindi.africa/competitions/usaids-intelligent-forecasting-challenge-model-future-contraceptive-use>); as published: an extract of Côte d'Ivoire's eLMIS, Train.csv (2.5 MB) with site, product, year and month, plus site, product and case tables.
- Decisive words (Data page): "The goal of the Intelligent Forecasting Competition is to predict consumption (stock_distributed in the Primary Data Dictionary) for 11 contraceptives across 156 health service delivery sites ... The predictions should be made monthly for three months: October 2019, November 2019, and December 2019 ... Zindi competitors will have access to 42 months, January 2016 through June 2019, of data." The Description: USAID seeks "more accurate methods of predicting future contraceptive use", "to predict the consumption of contraceptives over three months".
- Use case: real (procurement quantities per site), but the task is future values of per-site, per-product series over a horizon, so SEL-10 applies; nothing sets it apart as a fixed task with a temporal split (SEL-11).
- Metric: RMSE on the Zindi leaderboard; USAID judged its own submissions qualitatively.
- Reject check (AI, 2026-10-22): does not stand. This is a site x product panel (156 sites x 11 products = 1,716 series, monthly). TP-10 (amended 2026-10-22 on g_research, which had history-only features) can admit such a panel, so SEL-10 alone does not decide it. Against it: the source frames the task as forecasting ("Accurate forecasting of contraceptive consumption ..."; USAID judges whether models "Outperform traditional methods"). The test months (Jul-Sep 2019) follow the end of training (June 2019), and submission rows carry only year x month x site_code x product_code, so no future-month covariates exist, unlike grocery (promotions) or hydropower (climate) (https://api.zindi.world/v1/competitions/usaids-intelligent-forecasting-challenge-model-future-contraceptive-use). What is available is the static site table (lat/lon, site type), the product table, and other eLMIS columns up to the cutoff (stock_end, stock_received, average_monthly_consumption, stockout days). Under TP-10 leg 2 those may be allowed point-in-time summaries. Leg 1 (beat each series' naive profile) needs the data. One winner (Inventec, arXiv 2304.06344) describes 'feature engineering for time-series data', and its text was not read, so leg 2 is open too. Weaker than grocery: if the measurement fails, the No comes back, as for fossil_stock_forecasting_challenge (stood, checker 10, an SKU panel with no exogenous inputs).
- For /add-dataset: TBD -> 2nd Tier, priority 2. Add stage: (1) run TP-10 at the June 2019 cutoff with horizons 1-3. Compare GBM on site/product attributes plus point-in-time eLMIS summaries against each site-product's naive profile (last value, same month a year earlier, trailing mean) under RMSE. Treat average_monthly_consumption as a trailing summary of the target, not a same-month feature. (2) Read the Inventec paper (arXiv 2304.06344) and the Zindi top-solution threads for target lags (leg 2). (3) LEAK: same-month stock_initial + stock_received - stock_end is close to stock_distributed (stock identity), so these must never be same-row features. (4) The source warns of 'invalid 0 values' (non-reported months), which are a data-quality and target-cleaning question. (5) Licence: the rules say the data is 'the sole property of USAID' and must not be redistributed; check the USAID call (competitions4dev.org/forecastingprize) for terms that allow shipping. If (1) fails, return to No with SEL-10. (Priority set to 2 by the main session, like the other refuted forecasting-like panels: grocery_store_product_forecasting_challenge, uber_movement_sanral_cape_town_challenge.)

A USAID Zindi challenge to model/forecast future contraceptive (family-planning consumption) use from historical service-delivery logistics data. The explicit objective is forecasting future values over a horizon, which is out of scope for the benchmark (time-series forecasting). The name itself ('model future ... use') makes the forecasting nature clear, so this should be rejected.
