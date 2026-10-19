---
unique_name: southeast_asia_predator_prey_camera_trap_counts
name: Mammal predator-prey camera-trap co-abundance / tiger, clouded leopard, sambar and muntjac count histories, Southeast Asia
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: Other
year: '2022'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.5061/dryad.b8gtht7h3
- https://zenodo.org/records/7466450
- https://doi.org/10.1002/ece3.9627
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

Camera-trap count histories for two predator-prey pairs across 20 surveys in 10 Southeast Asian landscapes (Amir,
Sovie and Luskin 2022; paper read via PMC9745391). The workbook's correction from birds to mammals is right.
Downloaded the Zenodo copy (same files as Dryad, CC0) on 2026-10-19: four matrices of 416 sampling units (398 for
tiger) x 40 five-day occasions, 66.3% of the cells missing, and a covariate table of 418 units with survey, landscape,
camera effort, forest integrity and human footprint. Exact zeros among the observed cells: tiger 98.7%, clouded
leopard 98.3%, sambar 93.8%, muntjac 67.7%; units with a zero total: 91%, 87%, 66% and 33%. The rest of the 16.5 GB
release is fitted model objects.

The aim is inference on species interactions (Methods, "A two-species N-mixture model": "our primary goal ... was the
examine the directional impact of a dominant species' local abundance upon a subordinate species' local abundance,
and not to estimate latent population sizes"). As a table it would be 416 units with three numeric covariates in 10
landscapes. Zero mechanism: non-detection on an occasion (the design aims to "decrease the number of false zeros")
plus true absence where a species is extirpated; shares confirmed from the data, mechanism from the paper.

## Reference

Amir Z., Sovie A., Luskin M.S. (2022). Inferring predator-prey interactions from camera traps: A Bayesian co-abundance
modeling approach. Ecology and Evolution 12. doi:10.1002/ece3.9627. Data: doi:10.5061/dryad.b8gtht7h3.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 44 (Mammal predator-prey camera-trap
co-abundance).
