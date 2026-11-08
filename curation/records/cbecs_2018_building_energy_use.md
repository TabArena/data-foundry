---
unique_name: cbecs_2018_building_energy_use
name: 2018 Commercial Buildings Energy Consumption Survey (CBECS) public use microdata
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Lennart
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

**Assessment (AI, 2026-11-08):** size check for the large-datasets review: 6,357 buildings with a major-fuel consumption (4,512 reported, 1,845 imputed or estimated) x 569 inputs after the identifier and 50 energy-outcome columns; the call stands, priority 3.
- As published: `cbecs2018_final_public.csv` (https://www.eia.gov/consumption/commercial/data/2018/xls/cbecs2018_final_public.csv, 19,851,402 bytes, Last-Modified 2022-12-05), read in full on 2026-11-08: 6,436 rows x 1,249 columns = 620 survey variables + 477 imputation flags (`Z*`) + 152 weights (`FINALWT`, `FINALWT1` to `FINALWT151`). The codebook (`2018microdata_codebook.xlsx`) labels each variable's source: 462 questionnaire or third-party (`HDD65`, `CDD65`, `PUBCLIM`), 114 "Derived variable", 35 "Modeled variable", 9 "Building/energy supplier variable". User's guide (January 2023): "Other energy consumption data variables are based on models that we have developed using the CBECS data. These are indicated by labels beginning with Modeled variable."
- The task's table: one row per building. The 50 energy-use outcomes: the 9 supplier variables (annual electricity, natural gas and fuel oil consumption in Btu and in native units, and their expenditures: `ELBTU`, `ELCNS`, `ELEXP`, `NGBTU`, `NGCNS`, `NGEXP`, `FKBTU`, `FKCNS`, `FKEXP`), 4 derived totals (`MFBTU`, `MFEXP`, `DHBTU`, `DHEXP`), 35 modeled end uses (`MF*BTU`, `EL*BTU`, `NG*BTU`, `FK*BTU`, `DH*BTU` for heating, cooling, ventilation, water heating, lighting, cooking, refrigeration, office equipment, computing, other) and `WOEXP`, `WOEXPC` (wood expenditures). One is the target; the others are parts or restatements of it (LEAK-10), and the modeled end uses are fit on the survey (LEAK-27). The fuel-use flags (`ELHT1`, `NGCOOK` and the like) are characteristics and stay. `MFBTU` and `ELCNS` are missing for 79 buildings (`EGYUSED` = 2 for 77), so 6,357 rows; `ZMFBTU`: 4,512 reported, 1,637 imputed ("consumption and/or expenditures data that were imputed using regression models"), 208 "Estimated for strip center"; for electricity 4,656 reported (computed on the file). Inputs: 620 - `PUBID` - 50 outcomes = 569 (459 questionnaire and third-party, 110 derived); some restate others (`SQFTC`, `WKHRSC`, `NWKERC`, `NOCCAT`, `YRCONC`, the percent-heated and percent-cooled shares), so the distinct width is lower; conditional items are blank when inapplicable. The imputation flags and weights are no features.
- Access: open download, CSV (also SAS), no login; public federal data. Masking per the guide: no geography below the census division, square footage rounded, floors and heights top-coded, climate zone suppressed for buildings over a million square feet and some activities.
- Changes the call: none; priority 3 stands. A decision for /add-dataset: keep only the 4,512 reported targets (SEL-3: the target is an observed outcome, and an imputed one is EIA's regression on the same characteristics) or keep the 1,845 others with a note. The 2018 survey is the newest CBECS (EIA's page, read 2026-11-08). EPA's score-updates page cites the 2012 CBECS for the ENERGY STAR models released in 2018-2019 and lists a CBECS-based update for 2025 without naming the survey year, so the use on the 2018 data is not yet documented.
- Not checked: EPA's technical references; which questionnaire items a benchmarking programme holds for a building before it reports its energy use.
