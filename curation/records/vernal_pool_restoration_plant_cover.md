---
unique_name: vernal_pool_restoration_plant_cover
name: Vernal wetland vegetation / permanent quadrats of restored vernal pools, Santa Barbara County, 2019-2023
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
tags:
- AI-Filled (Verify)
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
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

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
