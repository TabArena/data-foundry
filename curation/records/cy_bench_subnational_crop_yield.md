---
unique_name: cy_bench_subnational_crop_yield
name: 'CY-Bench: a comprehensive benchmark dataset for sub-national crop yield forecasting'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Other
year: '2024'
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.5281/zenodo.11502142
- https://doi.org/10.5194/essd-18-3997-2026
- https://zenodo.org/records/17279151
- https://arxiv.org/abs/2506.19046
- https://github.com/WUR-AI/AgML-CY-Bench
- https://arxiv.org/abs/2608.30392
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: reported sub-national maize and wheat yields of 38 and 29 countries with expert-curated weather, soil and satellite predictors and a peer-reviewed data paper; a forecasting-like panel that has to pass TP-10.
- Source: Kallenberg, Athanasiadis et al. (AgML, led by Wageningen University), "CY-Bench: a comprehensive benchmark dataset for sub-national crop yield forecasting", Zenodo concept 10.5281/zenodo.11502142 (v1.10 of 2025-10-06 read: `cybench-data.zip` 6.2 GB, EUPL-1.2; v1.0 of 2024 per the run, not read), paper Earth System Science Data 18:3997-4018 (2026-06-11). As published: yield statistics from national offices, EUROSTAT and FEWS NET/HarvestStat ("crop statistics from thirty-eight countries for maize and twenty-nine countries for wheat", Sec. 2.2.1); predictors 2003-2023: AgERA5 weather (daily), GLDAS soil moisture, fPAR and NDVI (dekadal), WISE soil, WorldCereal crop mask and calendar; CSV per category and country, joined on region and year; total region-years not in the text read (Tables 3 and 4).
- Use case: forecasts enable "decision-makers to plan and respond effectively to potential food shortages" (Introduction) and support "farmers, policymakers and commodity traders" (Sec. 6); the code makes the first forecast at mid-season and truncates "all time series inputs ... up to the forecast or inference time point" (GitHub README); fit direct. Regime temporal: the paper validates leave-one-year-out "to avoid spatio-temporal leakage"; a forward split by season mirrors the use (SPLIT-5, SPLIT-6), with regions as groups inside (SPLIT-13).
- Siblings and duplicates: `climate_change_agriculture_financial` (a synthetic Kaggle table) is the record this was found for; `csisa_lds_rice_yield_india_2018` and `digital_green_crop_yield_estimate_challenge` are plot-level surveys, another task (PROV-7). External collections: CY-Bench is itself a benchmark (AgML). Papers on the task from the curator's Zotero collection: Sabo et al. 2025 (arXiv:2506.19046, TabPFN on South African sub-national yields, leave-one-year-out; its own data, not CY-Bench by the abstract) and Nedungadi et al. 2026 (arXiv:2608.30392, seven agricultural datasets, not named in the abstract).
- Better data: found as better data for `climate_change_agriculture_financial` and from the curator's Zotero collection (items 259, 69); no further search this round.
- Papers and pages: Kallenberg et al. 2026 (ESSD); github.com/WUR-AI/AgML-CY-Bench (baseline tables in `results_baselines/tables`, not read).
- Metric: the paper and the code report NRMSE, MAPE and R² side by side (ESSD evaluation; README `metrics = ["normalized_rmse", "mape", "r2"]`) and name none as primary, so the fallback `rmse` (MET-5, MET-8); inputs none.
- Risks for /add-dataset: a panel of the same regions over years, so yields follow each region's level and trend: the naive-profile test decides whether it is in scope (SEL-11, TP-10); the daily and dekadal predictors must be aggregated to one row per region-season at a fixed lead time (`Needs extensive data wrangling`); maize and wheat are two tasks (two datasets, or crop as a feature); fPAR and NDVI are region means of satellite indices (SEL-15, likely measurements, to confirm); about 20 seasons give few yearly windows (SPLIT-14).
- Priority: gap 0 (environmental science & climate, regression, temporal not thin), use case + (decision-makers and food shortages named), source + (ESSD paper, Zenodo, code), shape + (dozens of countries, two decades, regional and yearly structure), risk - (forecasting-like panel, heavy aggregation): 3.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `climate_change_agriculture_financial`; the curator's Zotero collection, item 259: "Foundation Models Meet Agriculture: Challenges Beyond Pretraining"; the curator's Zotero collection, item 69: "From Rows to Yields: How Foundation Models for Tabular Data Simplify Crop Yield Prediction".
- as published: one row per sub-national administrative region (level 1-3) and year with the reported yield of maize (38 countries) or wheat (29 countries), predictors 2003-2023 at dekadal or daily resolution: ...; target: reported crop yield (t/ha) of maize or wheat in a region and season; access: open.
- Why: climate_change_agriculture_financial is a synthetic Kaggle table ('completely synthetic') of crop yield and economic impact per country, region and year from temperature, precipitation, extreme events and inputs. CY-Bench holds the real relation it pretends to show: reported regional crop yields against measured ...
- Adds: real, traceable data with a peer-reviewed data paper and an open licence (EUPL-1.2) instead of generated rows; dozens of countries, two decades, a year column for a temporal split and regions for a grouped one. Risks: a forecasting-like panel (SEL-10/SEL-11): it needs TP-10, the benchmark's own baselines include a ...
