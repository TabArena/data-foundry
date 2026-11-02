---
unique_name: bicerano_polymer_tg
name: bicerano_dataset
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- AI-Filled (Verify)
- Tiny Data
collections:
- ChemPile
original_source: Other
year: '? (2021)'
domain: chemistry & material science
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.1021/acsapm.0c00524
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/bicerano_dataset ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/bicerano_dataset ; original: https://github.com/OpenBioML/chemnlp/blob/main/data/tabular/bicerano_dataset/HT_MD_polymer_properties.csv'
- https://arxiv.org/abs/2505.12534
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: 315 polymers with an experimental glass transition temperature, a real materials task on a tiny table whose open copy is currently unreachable.
- Source: Afzal et al. 2021, "High-Throughput Molecular Dynamics Simulations and Validation of Thermophysical Properties of Polymers for Various Applications", ACS Appl Polym Mater 3(2):620 (doi 10.1021/acsapm.0c00524, online 2020-12-21). The abstract: the workflow calculates "glass transition temperatures (Tgs) of 315 polymers for which Bicerano reported experimental values [Bicerano, J. Prediction of Polymer Properties; Marcel Dekker Inc.: New York, 1996.]" - so the experimental column was first published in Bicerano's book and this file pairs it with simulation output; the year is written `? (2021)` for that reason (PROV-9). As published (the ChemNLP meta.yaml, `num_points: 315`): compound_name, PSMILES, Tg_exp (K), Tg_calc, Tg_calc_std, rho_300K_exp, rho_300K_calc, rho_300K_calc_std, glass_CTE_calc, rubber_CTE_calc and their standard deviations.
- Use case: a polymer chemist choosing a repeat unit for a coating, casing or composite, before synthesis, predicts the glass transition temperature the polymer will have; fit approximate (the measured values are a book compilation whose conditions are not restated); regime likely grouped by repeat-unit chemistry, not settled, and with 315 rows every grouping costs folds.
- Siblings and duplicates: no record of this source. Other polymer records of this run: `polymer_gas_solubility_rhnet`, `solid_polymer_electrolyte_ionic_conductivity`, `block_copolymer_phase` (other targets, PROV-7). External collections: ChemPile / ChemNLP (config `bicerano_dataset`).
- Better data: a candidate of the benchmark ChemPile; no further search this round.
- Papers and pages: Afzal et al. 2021; the ChemNLP builder `data/tabular/bicerano_dataset` (its transform.py pulls HT_MD_polymer_properties.csv from the Hugging Face dataset `chemNLP/bicerano_polymers`).
- Metric: none found. The paper validates its simulation against the experimental values rather than defining a prediction task, and neither ChemNLP nor ChemPile declares a metric; looked at the paper's abstract, the ChemNLP meta.yaml and the ChemPile-LIFT card. So the fallback, `rmse` on Tg in K.
- Risks for /add-dataset: 315 rows is a tiny-data task (TP-5; tag `Tiny Data`), and a grouped split would leave very small folds; Tg_calc, rho_300K_calc and the CTE columns are MD output for the same polymer, not inputs the use case has, so they cannot be features (LEAK-10) and the simulated columns are out of scope as a target (SEL-16); both open routes are closed today (the GitHub CSV this record links returns 404, and `chemNLP/bicerano_polymers` on Hugging Face answers with an authentication error, checked 2026-10-31), so the data may have to come from the paper's supplement (ACS, paywalled) or from ChemPile-LIFT's prompts (cc-by-nc-sa-4.0; a licence is no verdict reason, EV-4).
- Priority: gap 0, use case 0 (an MD validation study, no actor named), source + (a paper with a documented table), shape - (315 rows), risk - (simulation columns, and no open copy found).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 315 polymers (ChemNLP); in ChemPile-LIFT 7,222 text prompts over 1 config(s); target: experimental Tg (K); the file also carries an MD-calculated Tg and density.
- Why: Predict the glass transition temperature of a polymer from its repeat unit
- Notes: Afzal et al. 2021 (ACS Appl Polym Mater 3:620), experimental Tg values reported by Bicerano with MD simulated counterparts. Only the experimental column is measured; Tg_calc and rho_300K_calc are simulation output and would be a leak as features. Very small (315 rows). Features: PSMILES string. No record (grep ...
