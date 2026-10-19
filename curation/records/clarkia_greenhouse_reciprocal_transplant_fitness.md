---
unique_name: clarkia_greenhouse_reciprocal_transplant_fitness
name: Clarkia sister-species greenhouse fitness (C. concinna and C. breweri reciprocal soil and water experiment)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: Other
year: '2021'
domain: biology & life sciences
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.5061/dryad.tb2rbp00h
- https://doi.org/10.5281/zenodo.5106813
- https://doi.org/10.1002/ajb2.1756
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

A greenhouse experiment testing ecogeographic isolation between two Clarkia sister species (Goff, Martinez del Rio
and Kay 2021; paper read via PMC9298282). Methods: "336 conetainers with germinants ... 204 C. breweri and 132 C.
concinna", crossed over 2 seed sites, 3 soils and 2 water treatments, with maternal lineage recorded. Seed count is
the fitness response, modelled with a zero-inflated negative binomial GLMM on the design factors only; every feature
is a treatment code. `CCCB_Fitness.csv` (14 KB) was not downloaded (Dryad blocks automated downloads).

Zero mechanism, from the paper only: "plants that germinated and did not flower and/or set seed were included,
causing significant zero-inflation", a real no-reproduction zero. The workbook already calls it a greenhouse
experiment; that is the reason for the verdict. Licence: CC0.

## Reference

Goff K.A., Martinez del Rio C., Kay K.M. (2021). A greenhouse experiment partially supports inferences of
ecogeographic isolation from niche models of Clarkia sister species. American Journal of Botany 108:2002-2014.
doi:10.1002/ajb2.1756. Data: doi:10.5061/dryad.tb2rbp00h.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 46 (Clarkia sister-species greenhouse fitness).
