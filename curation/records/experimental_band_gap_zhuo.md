---
unique_name: experimental_band_gap_zhuo
name: 'Matbench matbench_expt_gap: experimental band gaps of inorganic compositions'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Other
year: '2018'
domain: chemistry & material science
problem_type: Regression
original_data_state: One Table
source_links:
- https://matbench.materialsproject.org/Benchmark%20Info/matbench_v0.1/
- https://doi.org/10.1038/s41524-020-00406-3
- https://doi.org/10.1021/acs.jpclett.8b00124
- https://github.com/materialsproject/matbench/blob/main/scripts/mbv01/expt_gap.py
- https://hackingmaterials.lbl.gov/matminer/dataset_summary.html
- https://pubs.acs.org/doi/suppl/10.1021/acs.jpclett.8b00124
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: experimentally measured band gaps of inorganic compounds compiled by Zhuo, Mansouri Tehrani and Brgoch (2018; 6,354 values), cut by Matbench to 4,604 compositions; the standard measured-property regression from the composition, the materials sibling of `superconductivity`.
- Source: Zhuo, Mansouri Tehrani, Brgoch, "Predicting the Band Gaps of Inorganic Solids by Machine Learning", J Phys Chem Lett 9(7):1668-1673 (2018), doi 10.1021/acs.jpclett.8b00124, data in its Supporting Information (matminer `expt_gap`: "Experimental band gaps of 6354 inorganic semiconductors", `formula`, `gap expt` in eV). Matbench v0.1 (Dunn et al., npj Comput Mater 6:138, 2020) built `matbench_expt_gap` (4,604): formulas reduced, "we don't keep any compositions with a range of bandgaps more than 0.1eV", one value per composition (script `scripts/mbv01/expt_gap.py`); `matbench_expt_is_metal` (4,921) is the is-metal framing of the same data; matminer's `expt_gap_kingsbury` adds Materials Project ids to the 4,604.
- Use case: a materials chemist screens candidate compositions for a target band gap (photovoltaics, phosphors, wide-gap semiconductors) before synthesis or a costly calculation; fit approximate (no decision named; the compositions are those someone measured). Regime: IID over compositions, as Matbench's five folds; a split grouped by chemical system is the open question for closely related compositions.
- Siblings and duplicates: no record holds measured gaps (grep for band gap, Matbench, Zhuo); `materials_project_properties` and `mp_formation_energies` (DFT values, proposed `No` as AHDS in this run); `superconductivity` (Yes, composition to Tc) the closest accepted sibling; `perovskite_solar_cell_database` (device band gaps, another task). External collections: Matbench v0.1 (`matbench_expt_gap`, `matbench_expt_is_metal`).
- Better data: from the curator's Zotero collection (items 99 and 160) and the awesome-chemistry-datasets list; no search for better data in this run.
- Papers and pages: Zhuo 2018 (SVR on composition features); Dunn 2020 (Matbench, Automatminer); the Matbench leaderboard (Darwin 0.287 eV, Ax/SAASBO CrabNet 0.331, MODNet 0.333 mean MAE).
- Metric: `mae` in eV: the Matbench per-task leaderboard sorts its entries by "mean mae", the benchmark's metric that every entry optimised (MET-4 by analogy, MET-1); inputs none.
- Risks for /add-dataset: features computed from the formula (element fractions and Magpie-style statistics, as in `superconductivity`); many zero gaps (metals) give a point mass; from the 6,354-row source, group the repeated compositions; Matbench's drop of compositions whose reports disagree removes polymorphs (a selection to note); the is-metal framing stays a comment, not a second dataset (CLEAN-18).
- Priority: gap 0 (chemistry & material science and regression are not thin), use case 0 (no decision named), source + (a paper's Supporting Information and a documented benchmark cut), shape + (4,604 compositions, derived features), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the awesome-chemistry-datasets list (github.com/kjappelbaum/awesome-chemistry-datasets); the curator's Zotero collection, item 160: "How and why does deep ensemble coupled with transfer learning increase performance in ..."; the curator's Zotero collection, item 99: "blaiszik/awesome-matchem-datasets".
- as published: 4,604 compositions with a measured band gap in eV, after Matbench dropped compositions whose measurements spread by more than 0.1 eV and kept one value per composition. Composition is the only ...; target: Experimental band gap in eV (regression); is_metal as the binary sibling; access: open.
- Why: A measured property in an open, standard materials benchmark, with the same shape as superconductivity (composition to property). | measured target, which DFT band gaps systematically underestimate; a well-known benchmark we lack
- Adds: A second composition-to-property materials task; no Matbench record exists. Caveats: all features must be derived from the formula; many zero gaps (metals); small. Going back to the 6,354-row source would keep the duplicates (grouping needed). | a materials-property regression with measured labels. Risks: ...
