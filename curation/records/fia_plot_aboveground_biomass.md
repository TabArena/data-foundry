---
unique_name: fia_plot_aboveground_biomass
name: US FIA forest biomass / USDA Forest Inventory and Analysis (FIADB, DataMart) plot aboveground biomass
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Needs extensive data wrangling
- No Good Target (yet)
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: GOV Website
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://research.fs.usda.gov/products/dataandtools/fia-datamart
- https://arxiv.org/abs/2503.22103
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

The US national forest inventory: per-state multi-table CSV and SQLite downloads (PLOT, COND, TREE, ...), public
domain, tens of GB in all. No fixed task table exists. The study the workbook most likely means (White et al. 2025)
uses "confidential plot data, which can not be shared publicly" (Data availability) for small-area estimation: "our
primary inferential target is the average biomass per hectare at the county level" (Sec. 2.3), with 90 m raster
covariates. Public plot coordinates are perturbed by about 805 m and some private plots are swapped, so joining
rasters to public plots blurs the covariates. A plot-level target built from DataMart would be an allometric sum over
the measured tree tally, and the condition fields derived from those trees (forest type, stand size, stand age,
stocking) would leak it. Not downloaded.

Zero mechanism, from the paper only: nonforest plots and conditions without live trees, "a mixture of continuous
positive values and true zeroes" (Sec. 1). Workbook pushback: there is no released analytic sample, and the study is
county-level estimation, not row-level prediction. Reopen only if a source releases a plot-level biomass table with
covariates. The FIADB biomass computation was not re-read for this note.

## Reference

USDA Forest Service, Forest Inventory and Analysis DataMart, https://research.fs.usda.gov/products/dataandtools/fia-datamart.
White G.W., Finley A.O., Yamamoto J.K., Green J.L., Frescino T.S., MacFarlane D.W., Andersen H.-E. (2025).
Hierarchical models for small area estimation using zero-inflated forest inventory variables. arXiv:2503.22103.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 3 (US FIA forest biomass).
