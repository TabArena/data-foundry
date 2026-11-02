---
unique_name: vernal_pool_restoration_plant_cover
name: Vernal wetland vegetation / permanent quadrats of restored vernal pools, Santa Barbara County, 2019-2023
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
- Two-Regime Zeros
original_source: Other
year: '2025'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.5061/dryad.7m0cfxq79
- https://doi.org/10.1002/ecs2.70532
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `No` (`No Good Target / Scientific Discovery`, SEL-3, USE-2): a 2 x 2 restoration
experiment (thatch removal x native seeding) in 15 vernal pools, analysed with "repeated measures generalized linear
mixed-effects models (GLMMs) with sampling year, thatch manipulation treatment, and seeding treatment, and their
interaction effects, included as fixed effects" (Dryad methods, https://doi.org/10.5061/dryad.7m0cfxq79).
- Source: Tang and D'Antonio (Ecosphere 17:e70532); Dryad deposit of 2025-11-05, CC0: permanent-quadrat cover
  2019-2023 (3.6 MB CSV), thatch biomass, pool polygons, eDNA seed bank by quadrat, the R markdown; 180 quadrats, 12 per
  pool, five surveys. Not downloaded (Dryad answers 401 to file requests).
- Deciding reason: the aim is a test, "to test the efficacy of long-term thatch management" and "to quantify the effect
  of annual thatch removal and native seed addition" (Dryad abstract). The quadrat README (read by the reject check)
  lists only ids, date, monitor, `Location` (two sites), `Pool ID`, `Zone`, `Quadrat ID`, x/y, `Year`, `Treatment` and
  `Seeded`, species and cover. Pool area (from the polygons) and the 2019 eDNA seed-bank file are the only non-design
  covariates, and the source uses the eDNA only to justify seeding ("We coupled thatch removal with annual native seed
  addition because our analysis of environmental DNA ... revealed a lack of native plant species", Dryad abstract).
  With every treatment-year cell observed, a per-quadrat prediction is the cell mean the paper reports (SEL-3, USE-2).
- Siblings and duplicates: none for the data; designed experiments of the same batch as for
  `clarkia_greenhouse_reciprocal_transplant_fitness`. External collections: none found.
- Papers and pages: paper text not read (Wiley 403); the quotes are the authors' Dryad abstract and methods.
- Metric: none; hurdle gamma and beta GLMMs for the effects (Dryad methods).
- Reject check (AI, 2026-10-27): stands. SEL-3 (Must). The release holds year, treatment, seeding and location ids, with
  pool area and the eDNA seed bank as the only non-design covariates, and the source fits GLMMs on the design
  (https://doi.org/10.5061/dryad.7m0cfxq79).

CC (2026-10-30, Andrej): `No`, as screened (verified on the zero-inflated screening review page).

Plant cover in restored vernal pools (Tang and D'Antonio, UCSB): 180 permanent 1 m2 quadrats (12 per pool in 15
pools), surveyed in August 2019 and each June 2020-2023, so at most 900 quadrat-years; the 3.6 MB quadrat CSV is
probably long format by species (estimate; not downloaded, Dryad blocks automated downloads). It is a 2 x 2
management experiment. The abstract's aim is "to quantify the effect of annual thatch removal and native seed
addition", and the Dryad methods say "We constructed repeated measures generalized linear mixed-effects models
(GLMMs) with sampling year, thatch manipulation treatment, and seeding treatment ... as fixed effects". The features
would be pool, quadrat, year and treatment flags: a hypothesis test with 15 independent pools.

Zero mechanism, from the authors' Dryad text: a species absent from a quadrat in a year, with the treatments changing
occurrence (seeding adds natives); "bare ground percent cover and total native plant percent cover datasets were
zero-inflated, so we constructed hurdle models with gamma distributions". Workbook pushback: "secondary" overstates
it, and total cover "often exceeded 100%". Paper text not read (Wiley 403). Licence: CC0.

## Reference

Tang J., D'Antonio C. (2026). Community-based long-term management to address reinvasion of restored grassland
vernal wetlands. Ecosphere 17:e70532. doi:10.1002/ecs2.70532. Data: doi:10.5061/dryad.7m0cfxq79.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 10 (Vernal wetland vegetation).
