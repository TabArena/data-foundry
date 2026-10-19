---
unique_name: chesapeake_bay_bird_banding_zi_isdm
name: Species abundance from occurrence + presence-only data / zero-inflated integrated SDM, Chesapeake Bay birds (Gonnerman et al. 2026)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: Other
year: '2026'
domain: biology & life sciences
required_split:
- '?'
problem_type: Regression
original_data_state: Other
source_links:
- https://doi.org/10.5061/dryad.pnvx0k729
- https://doi.org/10.1016/j.ecolmodel.2026.111712
- https://pubs.usgs.gov/publication/70276934
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

A methods paper on a zero-inflated integrated species distribution model, validated on simulations and applied to
birds of the counties around Chesapeake Bay. The public part is `ModValData_PO.csv` (0.43 MB): Bird Banding Lab
presence-only captures with counts of at least one and covariates. The Dryad README: "eBird data is referenced as
ModValData_OC.csv in code, but is not available for distribution". `PredPoints` (1.8 GB) is a prediction grid without
a response. Not downloaded (Dryad blocks automated downloads).

Zero mechanism: none in the public part. Banding records are presence-only, and the real zeros (non-detections on
eBird checklists) are withheld. Rebuilding them needs the eBird Basic Dataset (a request form, so only a licence
note) and the paper's filters, which were not read (ScienceDirect 403), and would give a table we assembled
ourselves. Agrees with the workbook's "partial release" and goes further: the release cannot form a target with real
zeros at all. Licence: CC0 (Dryad).

## Reference

Gonnerman M., Mullinax J., Sullivan J., Kent C., Prosser D. (2026). Improved estimates of relative occurrence and
abundance using opportunistic surveys and presence-only observations: A zero-inflated integrated species
distribution model. Ecological Modelling 521:111712. doi:10.1016/j.ecolmodel.2026.111712. Data:
doi:10.5061/dryad.pnvx0k729.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 45 (Species abundance from occurrence +
presence-only data).
