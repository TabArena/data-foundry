---
unique_name: recs_2020_household_electricity
name: Residential Energy Consumption Survey (RECS) 2020, public-use microdata
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- Many features
- AI-Filled (Verify)
original_source: GOV Website
year: '2023'
domain: environmental science & climate
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.eia.gov/consumption/residential/data/2020/index.php?view=microdata
- https://www.eia.gov/consumption/residential/data/2020/
- https://arxiv.org/abs/2608.09255
- https://www.eia.gov/consumption/residential/data/2020/pdf/2020%20RECS%20CE%20Methodology%20-%20Monthly%20Appendix%20-%20Final.pdf
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: EIA's national household survey of 2020, nearly 18,500 households with several hundred housing, equipment and climate variables and the annual electricity use from supplier billing data; a real estimation task with a strong source, but 14% of the targets are imputed by a model and many columns restate the target.
- Source: U.S. Energy Information Administration, Residential Energy Consumption Survey (RECS) 2020, public-use microdata `recs2020_public_v7.csv` with the "RECS 2020 Codebook for Public File - v7"; first released July 2022 (household characteristics only), consumption, expenditures and end-use estimates added June 2023, v7 January 2024. Nearly 18,500 households representing 123.5 million occupied primary residences, with sampling weights. The 15th wave since 1978; earlier microdata for 2015, 2009, 2005 and before, and a 2024 wave in preparation (preliminary characteristics only).
- How the target is made (2020 RECS Consumption and Expenditures Technical Documentation, Table 3 and the section "Imputation"): the mandatory Energy Supplier Survey collects the household's 2020 bills; for electricity 15,290 households (83%) have complete billing data, 675 (4%) partial and 2,531 (14%) none; partial years are filled, and "for households with no billing data, we imputed the annual total" with regression models on the modelled end uses by housing type and climate zone. End-use splits (heating, cooling, appliances) are engineering-model outputs calibrated to the total.
- Use case: a utility or efficiency programme estimates a household's annual electricity use from its characteristics before any bills or audit exist (the framing of Ramnarayan et al. 2026, arXiv 2608.09255: estimates needed "before detailed envelope characteristics, equipment efficiencies, infiltration, sensor, or billing data are available"); EIA itself publishes statistics, not predictions, so the actor is the curation's, fit approximate. Regime IID: one year of a probability sample of households.
- Siblings and duplicates: `cbecs_2018_building_energy_use` (`TBD -> Yes`, the same agency's commercial-building survey, another task); `elusage` (`TBD -> 2nd Tier`, `Too Small`); `energy_efficiency`, `energy_efficiency_2`, `energy_consumption_dataset_linear_regression`, `household_monthly_electricity_bill` and `renewable_energy_optimized_interior_design_dataset` (all `No`); no other RECS record. External collections: none found.
- Better data: found as better data for `elusage`, `energy_consumption_dataset_linear_regression`, `energy_efficiency`, `energy_efficiency_2`, `household_monthly_electricity_bill`, `renewable_energy_optimized_interior_design_dataset`, and from the curator's Zotero collection (item 236); no further search this round.
- Papers and pages: the EIA microdata page and technical documentation; Ramnarayan, Evren, Gunderson, Rosenberg, "Full-Feature versus Limited-Input Machine Learning for Residential Energy Estimation: A Comparative Analysis of RECS and ResStock Under Realistic Input Constraints", arXiv 2608.09255 (2026): CatBoost best, R² 0.61 with ten low-burden inputs (abstract).
- Metric: none from the source (a statistical survey); the paper reports R² in its abstract only, not read further, so the fallback `rmse`; a skewed kWh total may call for `rmsle` from context (MET-11), the curator's call; the sampling weight (NWEIGHT) is a possible metric input, never a feature (MET-2).
- Risks for /add-dataset: the 2,531 households whose annual electricity is model-imputed (drop them if the file flags them, which the codebook should say; otherwise the target is partly a model output, USE-5); every column that restates the target goes: end-use kWh, dollars (DOLLAREL and the end-use dollars), BTU totals and the other fuels' totals where they share the model (LEAK-10, LEAK-2 column by column); the imputation flags of the characteristics; the replicate weights; the arXiv paper's restricted feature set is one framing, the full set another.
- Priority: gap 0 (the environmental domain, regression and IID are not thin), use case 0 (the actor is the paper's framing, not the source's), source + (a federal survey with codebook and methods), shape + (about 18,500 households, several hundred mixed variables), risk - (imputed targets and target-restating columns).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `elusage`, `energy_consumption_dataset_linear_regression`, `energy_efficiency`, `energy_efficiency_2`, `household_monthly_electricity_bill`, `renewable_energy_optimized_interior_design_dataset`; the curator's Zotero collection, item 236: "Full-Feature versus Limited-Input Machine Learning for Residential Energy Estimation: A ...".
- as published: Households; 'nearly 18,500 households' representing 123.5 million housing units, several hundred variables (codebook v7, CSV recs2020_public_v7), survey year 2020 with weights. Earlier waves 2015, ...; target: Annual household electricity use in kWh (KWH); access: open.
- Why: The same quantity as elusage (household electricity use driven by temperature) measured on a national sample, with features of the same kind (local heating and cooling degree days) plus the household's own characteristics, all known before the year's consumption. | the synthetic record predicts energy consumption ...
- Adds: About 18,500 households against 55 monthly readings of one series, 2020 instead of a 1990s textbook example, an agency source with a codebook. To check: how far KWH comes from supplier billing data and how far it is modelled or imputed (EIA consumption and expenditures technical documentation), and the survey ...
