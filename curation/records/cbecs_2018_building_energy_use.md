---
unique_name: cbecs_2018_building_energy_use
name: 2018 Commercial Buildings Energy Consumption Survey (CBECS) public use microdata
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Many features
original_source: GOV Website
year: '2021'
domain: environmental science & climate
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.eia.gov/consumption/commercial/data/2018/index.php?view=microdata
- https://arxiv.org/abs/1910.14563
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: EIA's national probability sample of 6,436 US commercial buildings with their annual energy use and about 620 building variables, the data behind ENERGY STAR-style benchmark models; many columns restate the target and some targets are imputed.
- Source: U.S. Energy Information Administration, 2018 Commercial Buildings Energy Consumption Survey (CBECS) public use microdata (https://www.eia.gov/consumption/commercial/data/2018/index.php?view=microdata), released November 2021, CSV, SAS file and codebook revised December 2022: "6,436 records", "approximately 620 questionnaire variables, plus imputation flags and survey weights"; "The sample represents an estimated 5.9 million total buildings"; masked for disclosure ("results tabulated from this file will not exactly match the published CBECS data tables"); the smallest geography is the census division. Files: cbecs2018_final_public.csv, codebook, user's guide, questionnaire. Earlier waves (2012 and before) are other releases of the survey (PROV-6).
- Use case: EPA's ENERGY STAR Portfolio Manager scores a building by comparing its energy use with what a regression on CBECS predicts from its characteristics (activity, floor area, workers, hours, climate); owners and city benchmarking programmes act on the score; fit direct (named in the run's assessment and in Arjunan et al. 2020; EPA's technical reference not read here). Regime IID: one cross-section of a probability sample, one row per building.
- Siblings and duplicates: `recs_2020_household_electricity` (this run, EIA's residential survey, another population, PROV-7); `ashrae_great_energy_predictor_iii` (`Yes`, hourly meter readings, another task); `deepflow_ai_hackflow` (`TBD -> 2nd Tier`, AHDS) and `energy_consumption_dataset_linear_regression` (`No`, AHDS), for which the run proposed it. No duplicate (grep for cbecs, eia.gov). External collections: none found.
- Better data: from the run's search, found as better data for `deepflow_ai_hackflow` and `energy_consumption_dataset_linear_regression`, and as a related task next to `ashrae_great_energy_predictor_iii`; no further search this round.
- Papers and pages: Arjunan, Poolla, Miller, "EnergyStar++: Towards more accurate and explanatory building energy benchmarking", Applied Energy 276, 2020 (arXiv 1910.14563): ENERGY STAR-type models on the 2012 CBECS (1,812 buildings), scored by adjusted R2 and NRMSE.
- Metric: none found for these data as one choice (EnergyStar++ reports adjusted R2 and NRMSE side by side, and on the 2012 wave), so the fallback `rmse`, on the scale the target ships (total use, or use per square foot; MET-3, MET-5, MET-8); the final survey weight is a weight, never a feature (MET-2).
- Risks for /add-dataset: dozens of consumption and expenditure columns by fuel and end use restate the target (LEAK-10); consumption imputed or modelled for some buildings, marked by the imputation flags (drop or keep, a decision to record); disclosure masking (a PROV-3 note, as framingham_heart_study_fhs); replicate weights and flags are no features; the target choice (major fuel, electricity, or intensity, USE-5); about 620 columns.
- Priority: gap 0 (environmental science & climate and regression are not thin), use case + (the ENERGY STAR benchmark model is a documented use), source + (a federal survey with a codebook and user's guide), shape + (6,436 buildings, about 620 mixed variables), risk - (many target-restating columns, partly imputed targets).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `deepflow_ai_hackflow`, `energy_consumption_dataset_linear_regression`; a related task next to `ashrae_great_energy_predictor_iii`.
- as published: 6,436 buildings (weighted to 5.9M US commercial buildings), about 620 questionnaire variables plus imputation flags and survey weights; CSV; target: annual energy consumption of the building (total major fuel or electricity); access: open.
- Why: a different task in the building-energy domain (annual use from building characteristics, for benchmarking), with a national probability sample and a stated user; ASHRAE's 'better' search found nothing beyond BDG2, which the record already uses | The real, traceable version of the Hackflow task (operational energy of ...
- Adds: building characteristics (activity, floor area, HVAC, hours, workers) for thousands of buildings; check which consumption values are imputed or modelled | Measured (surveyed and billed) consumption instead of likely simulated values, a national probability sample, an agency source with a codebook. Also proposed by ...
