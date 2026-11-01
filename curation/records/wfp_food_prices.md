---
unique_name: wfp_food_prices
name: Food Prices
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
collections:
- STRABLE
original_source: GOV Website
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- '# the older WFP dataset on HDX, no longer updated; its replacement, which holds STRABLE''s 2024 file, follows'
- https://data.humdata.org/dataset/wfp-food-prices
- https://data.humdata.org/dataset/global-wfp-food-prices
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/food-prices_wide
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: WFP's market price monitoring is a large, documented source, and the World Bank fills missing market prices with machine learning, a real use; but the data are monthly price series, so only an unmonitored-market framing stays clear of forecasting, and STRABLE's cut (2024, one row per series, date and local price dropped, exchange rates and wages mixed in) is not that framing.
- Source: World Food Programme (WFP) Price Database via HDX, "Global - Food Prices" (CC BY-IGO, https://data.humdata.org/dataset/global-wfp-food-prices): "covers foods such as maize, rice, beans, fish, and sugar for 98 countries and some 3000 markets. It is updated weekly but contains to a large extent monthly data. The data goes back as far as 1992 for a few countries"; one CSV per year (1990-2026; 2024: 59.5 MB) with `countryiso3, date, admin1, admin2, market, market_id, latitude, longitude, category, commodity, commodity_id, unit, priceflag, pricetype, currency, price, usdprice` (header read 2026-10-31). The record's first link, https://data.humdata.org/dataset/wfp-food-prices, is the older dataset: "This no longer updated dataset [...] has been replaced by a new and ongoing global food prices dataset". As published by STRABLE (`food-prices_wide`, file `wfp_food_prices_global_2024.csv`): 50,443 rows x 15 columns, exactly one row per market x commodity x unit x price type x flag x currency (2,509 markets, 67 countries, 633 commodities), without `date` and `price`; target `usdprice` (transformed by STRABLE).
- Use case: a food-security analyst estimates the price of an item at a market and month that no enumerator reported, from the prices at other markets and of related items and the exchange rate: the World Bank's Real-Time Prices data, built on WFP prices (Andrée 2021, "Estimating Food Price Inflation from Partial Surveys", World Bank Policy Research Working Paper 9886; Microdata Library, DOI 10.48529/2ZH0-JF55). STRABLE's cut does not mirror it (no month, one observation per series), so the fit is approximate; regime grouped by market for an unmonitored market. A split in time within each series makes it forecasting (SEL-10).
- Siblings and duplicates: no other food-price record; `hdx_conflict_events` is another HDX table in STRABLE, unrelated. No duplicate. External collections: STRABLE (config `food-prices_wide`; the config names the source "OHCA", but the publisher is WFP).
- Better data: a candidate of the benchmark STRABLE; no new search in this run. The HDX year files hold every year since 1990 with the date, against STRABLE's one row per series of 2024.
- Papers and pages: the HDX pages above; Andrée 2021 (PRWP 9886; read from a search summary, not the paper); STRABLE, Blayer et al. 2026, "STRABLE: Benchmarking Tabular Machine Learning with Strings", arXiv:2605.12292, App. C item 45 ("predict staple crop price").
- Metric: none from WFP (a price database). Andrée 2021 judges imputations against observed prices (the paper's metric not read). STRABLE, the benchmark that framed the task, scores R² for every regression table (arXiv:2605.12292, App. D.1: "R2 for regression; AUROC for classification"; 3 outer folds, rendered "33", on a target it transformed to minimise skew, App. C): one metric for the whole benchmark, not a choice for this task (MET-5), so the fallback `rmse` (MET-8) on the amount as published, with any log shipped as `target_transform` (MET-3); inputs none (MET-1, MET-6).
- Risks for /add-dataset: the rows mix units (KG 36,113, L 3,241, "25 KG", "Head", "Day" and more) and non-food series (exchange rates with unit `USD/LCU`, 313 rows; fuel; wages), so restrict to food and model per unit (USE-5); 41% of rows are flagged `aggregate`; how STRABLE reduced the 2024 file to one row per series is not documented, so rebuild from the HDX year files with the date; `price` divided by the exchange rate is `usdprice`, keep it out (LEAK-10); the imputation framing needs other markets' prices of the same month as features and must beat each series' naive profile (TP-10, SEL-11).
- Priority: gap 0, use case 0 (a later paper names it, but STRABLE's cut does not mirror it), source + (WFP, HDX documentation), shape + (50,443 rows, 2,509 markets with coordinates), risk - (price series: SEL-10 unless framed as imputation).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 50,443 rows x 15 columns incl. target (STRABLE parquet); target: usdprice.
- Why: Predict the USD price of a commodity at a market
- Notes: Raw file wfp_food_prices_global_2024.csv (WFP via HDX, 2024 only). Market price observations; a cross-sectional price-estimation framing of what is usually a time series.
