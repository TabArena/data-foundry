---
unique_name: southeast_asia_predator_prey_camera_trap_counts
name: Mammal predator-prey camera-trap co-abundance / tiger, clouded leopard, sambar and muntjac count histories, Southeast Asia
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
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
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 1: camera-trap count histories of tiger, clouded leopard,
sambar and muntjac in about 416 hexagonal units of 10 Southeast Asian forest landscapes with three covariates, released
for a species-interaction model whose authors decline to read the counts as abundance; abundance mapping from it is the
family's open question.
- Source: Amir, Sovie and Luskin, Ecology and Evolution 12 (2022), doi:10.1002/ece3.9627 (read via PMC9745391); data on
  Dryad, doi:10.5061/dryad.b8gtht7h3 (2022-12-20, CC0, 16.5 GB, almost all fitted models), and Zenodo 7466450. As
  published (Dryad file list): four count-history matrices (unit by five-day occasion) and a unit table
  `ECL_meta_3km_res_co-abundance_20220131.csv`. Earlier AI triage, 2026-10-19, measured on the Zenodo copy: 416 units
  (398 for tiger) by 40 occasions, 66.3% of cells missing; exact zeros among observed cells tiger 98.7%, clouded leopard
  98.3%, sambar 93.8%, muntjac 67.7%; covariates survey, landscape, camera effort, forest integrity (FLII) and human
  footprint (HFP).
- Use case: none stated. Dryad methods: "The manuscript describes a new method of analyzing camera trap data to infer
  predator-prey species interactions"; paper Sec. 2.1: "... and not to estimate latent population sizes, we refrain from
  interpreting our results in terms of absolute density". The abstract's "may be useful in forecasting cascading impacts
  following widespread predator declines" names no actor. For example a conservation agency estimating prey counts in
  unsurveyed forest; fit approximate. Regime grouped by landscape (20 sessions in 10 landscapes).
- Doubt: the earlier pass set `No` (SEL-3). The aim is inference, but the data are a multi-landscape survey with habitat
  covariates, so the open species-abundance-mapping question applies; no fast reject. The authors' own refusal to read
  the counts as abundance weighs against the mapping framing.
- Siblings and duplicates: the other camera-trap records (`freiburg_urban_mammal_camera_trap_events`,
  `wildlife_insights_camera_trap_detections`, `iwildcam_2020_camera_trap_species`) hold other data; no duplicate.
  External collections: none found.
- Papers and pages: the paper; the Dryad README, with its questions on whether a co-abundance model fits.
- Metric: none for prediction (the paper compares models by goodness of fit and convergence, Abstract); fallback `rmse`.
- Risks for /add-dataset: a count per unit sums occasions of unequal effort with two thirds of the cells missing, so the
  target needs an effort rule (an unclear target); three covariates; tiger and clouded leopard are almost all zeros;
  units are resampled hexagons with cameras pooled ("we spatially resampled the camera traps into 7.8 km2 hexagonal
  sampling units", Sec. 2.3.1), and a split by landscape leaves 10 groups.
- Priority: gap 0, use case 0, source + (paper, Dryad README), shape 0 (416 units, three covariates), risk - (effort
  rule for the target).

**Assessment (AI, 2026-10-30):** The family's question on species-abundance mapping is settled without a new rule
(Andrej, 2026-10-30, policy question 1 of the zero-inflated review: "I don't think there is new rule to build here.
These are per dataset judgement calls and if a dataset is useful for a predictive application although the data was
collected for something else, then this is fine"), as SEL-2 already reads the scope rules: this record is judged on its
own use case. The verdict and priority stay.

CC (2026-10-30, Andrej): `No` (the AI screening had `TBD -> 2nd Tier`, priority 1; zero-inflated screening review page).
No reason was given on the page; the record's markers (`No Good Target / Scientific Discovery`) stand as the reason.

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
