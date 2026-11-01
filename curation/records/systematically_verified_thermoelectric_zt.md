---
unique_name: systematically_verified_thermoelectric_zt
name: 'sysTEm: Systematically Verified Experimental Thermoelectric Dataset'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: Github
year: '2025'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://github.com/tankylz/sysTEm_dataset
- https://doi.org/10.1007/s40192-026-00446-5
- https://doi.org/10.26434/chemrxiv-2025-4gxmc
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: 8,650 experimental thermoelectric measurements (1,430 reduced compositions from 365 papers, 1991-2024) with zT and the transport properties it is computed from, checked against the zT formula; a materials-screening regression grouped by composition, once the columns that define zT are dropped and composition features are built.
- Source: Tang, Purdy, Mohanty, Ng and Sparks, "Systematically Verified Experimental Thermoelectric Dataset For Data-driven Approaches", Integrating Materials and Manufacturing Innovation 15(1):181-193, 2026 (doi 10.1007/s40192-026-00446-5; ChemRxiv preprint 2025, doi 10.26434/chemrxiv-2025-4gxmc; both answered 403, so only the README and the data were read); data on GitHub tankylz/sysTEm_dataset (created 2025-06-21, MIT): `sysTEm_dataset.xlsx`. As published (README): "a compilation of experimental thermoelectric (TE) data, comprising information on the composition, temperature, and transport properties", mostly read from published plots with WebPlotDigitizer and merged with an updated MRL dataset and the ESTM dataset, validated "utilizing the zT formula (below), with a tolerance of 10% between the calculated value and the extracted value". Preview of the xlsx (871 KB, 2026-10-31): 8,650 rows x 16 columns (`#`, `Initial Dataset`, `Source Paper`, three composition strings, `Type of Formula`, `Year`, `Temperature (K)`, electrical conductivity, Seebeck coefficient, power factor, `zT`, total, lattice and electronic thermal conductivity); 1,430 reduced compositions, 365 source papers, publication years 1991-2024 (median 2020); zT in 7,991 rows; ESTM 5,054 rows, new extractions 2,234, extended MRL 1,362.
- Use case: a materials researcher screens candidate compositions for a high zT at an operating temperature before synthesis (README: "materials screening and discovery", "in the hopes of discovering higher performance TE materials"); no decision is named, and published materials lean towards promising ones (`Selection Bias` to weigh), so fit approximate. Regime grouped by composition (rows are temperature points of one material, SPLIT-29); the publication year allows a temporal alternative.
- Siblings and duplicates: `superconductivity` (`Yes`, a composition-to-property task of the same kind), `supercon_mdr_2024` and `experimental_band_gap_zhuo` (other properties): no duplicate. ESTM (Na and Chang 2022) and MRL (Gaultois et al. 2013) are merged into this table and have no record of their own. External collections: none found.
- Better data: found as better data for `superconductivity` and from the curator's Zotero collection (item 179); it measures another property (zT), so it is a related task rather than better data for Tc; no further search this round.
- Papers and pages: the IMMI paper; Na and Chang, npj Computational Materials, 2022 (ESTM, doi 10.1038/s41524-022-00897-2); Gaultois et al., Chemistry of Materials, 2013 (MRL, doi 10.1021/cm400893e); the updated MRL dataset on Zenodo (doi 10.5281/zenodo.15365344).
- Metric: none found (the README defines no task; the paper's text was not reachable), so the fallback `rmse` (MET-8); inputs none.
- Risks for /add-dataset: zT = σS²T/κ, so conductivity, Seebeck coefficient, power factor and the thermal conductivities are the target's inputs and go (SEL-5, LEAK-10), which leaves composition, formula type and temperature; composition features to build (for example Magpie), documented as ours (PROV-11); 659 rows without zT; mixed formulas ("Te + 0.1 wt% InP3") parse poorly; the same material may appear from ESTM and from the new extractions (check the merge for duplicates); digitised values carry plot-reading error.
- Priority: gap 0 (chemistry & material science has 12 accepted datasets; regression and grouped not thin), use case 0 (screening named, no decision, approximate fit), source + (a peer-reviewed data paper and an open repository), shape + (8,650 rows, 1,430 compositions as groups), risk - (the target's inputs in the table, features to build).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `superconductivity`; the curator's Zotero collection, item 179: "Building informative materials datasets beyond targeted objectives".
- as published: measurements; about 8,400 rows (composition x temperature); over 1,400 unique materials, 70 elements; columns: composition strings, publication year, temperature, seven transport properties; source ...; target: thermoelectric figure of merit zT (alternatives: Seebeck coefficient, electrical or thermal conductivity) at a given temperature; access: open.
- Why: Real, experimentally measured data from the literature, validated against the zT formula and documented in a paper; materials property regression like superconductivity. Notes: the features must be built from the formula (e.g. matminer Magpie), so 'Needs extensive data wrangling'. The other transport properties ...
- Adds: A new materials-property task (thermoelectrics) with a group structure and a publication-year column; merges and validates the older MRL and ESTM thermoelectric sets
