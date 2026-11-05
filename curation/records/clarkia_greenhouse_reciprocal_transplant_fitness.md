---
unique_name: clarkia_greenhouse_reciprocal_transplant_fitness
name: Clarkia sister-species greenhouse fitness (C. concinna and C. breweri reciprocal soil and water experiment)
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
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
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (v4 of 2026-10-19, a list of 69 candidates, not in the repository), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `No` (`No Good Target / Scientific Discovery`, SEL-3, USE-2): a greenhouse
reciprocal-transplant experiment in which every feature is an assigned treatment: "The predictors included plant
species, water treatment, soil species, a water treatment by plant species interaction, and a soil species by plant
species interaction" (Methods, "Greenhouse experiment", PMC9298282).
- Source: Goff, Martinez del Rio and Kay 2021 (Am. J. Bot. 108:2002-2014); Dryad doi:10.5061/dryad.tb2rbp00h
  (2021-07-15, CC0). Usage notes: "CCCB_Fitness.csv contains the results from our greenhouse reciprocal transplant
  experiment. The number of variables has been reduced to just what we used for our study" (14 KB; not downloaded,
  Dryad answers 401 to file requests). Methods: "336 conetainers with germinants ... representing 204 C. breweri and 132
  C. concinna".
- Deciding reason: the aim is a test, "We then test these inferences with a greenhouse experiment in field soils in
  which we manipulate water availability ... We cross the water manipulation with home versus away soils for two
  populations of each species" (Introduction, last paragraph). The features are the assigned species, water and soil
  treatments and the seed and soil sites of a full cross, so a per-plant prediction is the mean of its treatment cell,
  the effect the paper already reports; no decision is left for a model (SEL-3, USE-2). The paper's "prediction" is a
  hypothesis ("we predicted that C. concinna would have a marked decrease in fitness in a xeric, short-season
  treatment").
- Siblings and duplicates: none for the data. The deposit's GBIF occurrence files are presence-only with pseudo-absences
  for the niche models, so the family's species-abundance mapping question does not come in. Designed experiments of
  the same batch: `treeline_seedling_emergence_experiment` and `vernal_pool_restoration_plant_cover` (rejected the same
  way), `pennsylvania_oak_hickory_regeneration_experiment` (2nd Tier: measured covariates beside the treatments).
  External collections: none found.
- Papers and pages: the paper (PMC9298282: Introduction, Methods, Data availability statement).
- Metric: none; a zero-inflated negative binomial GLMM tests the effects (Methods).
- Reject check (AI, 2026-10-27): stands. SEL-3 (Must). Every feature is an assigned treatment ("The predictors included
  plant species, water treatment, soil species ...", Methods, https://pmc.ncbi.nlm.nih.gov/articles/PMC9298282/), and
  the deposit keeps "just what we used for our study" (https://doi.org/10.5061/dryad.tb2rbp00h).

CC (2026-10-30, Andrej): `No`, as screened (verified on the zero-inflated screening review page).

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

Lead: the two-regime-zero workbook (v4, 2026-10-19), Master row 46 (Clarkia sister-species greenhouse fitness).
