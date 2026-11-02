---
unique_name: morocco_forest_bird_transect_counts
name: Palaearctic rear-edge forest birds / Moroccan forest-bird transect counts (Telleria et al. 2021)
checked_by:
- Andrej
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- No Good Target / Scientific Discovery
tags:
- Two-Regime Zeros
original_source: Other
year: '2021'
domain: biology & life sciences
required_split:
- '?'
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.5061/dryad.34tmpg4kh
- https://doi.org/10.5281/zenodo.5011952
- https://doi.org/10.1111/jbi.14219
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 1: about 190 country-wide line transects of 11 forest
passerines in Morocco with local habitat covers, published to test the centre-periphery hypothesis; a multi-site
survey with habitat covariates, so the family's open species-abundance question decides it.
- Source: Tellería, Hernández-Lambraño and Carbonell 2021, "Ecological and geographical marginality in rear edge
  populations of Palaearctic forest birds", Journal of Biogeography 48(10):2538-2549 (doi:10.1111/jbi.14219); Dryad
  doi:10.5061/dryad.34tmpg4kh (CC0, about 77 KB) with "Bird occurrences" (presence points for the Maxent models) and
  "Transects" (counts of 11 species in 500 m belts, 25 m on each side, with visually estimated grass, shrub and tree
  cover and tree and shrub species numbers from two circles per transect); Zenodo 5011952 holds a README only. A 2023
  paper on the same data (Hernández-Lambraño and Tellería, Bird Conservation International 33) has "190 500-m line
  transects scattered within the country", surveyed in April and May of 2015-2017 (as quoted by the reject check); the
  rows of Transects.csv were not counted. Not downloaded.
- Aim, in the source's words: "Here we explore if habitat suitability decreases southwards"; "We also test if birds
  endemic to the area fit more poorly" (Abstract, Aim).
- Use case: none named for a prediction. For example a forest or conservation agency estimating a species' abundance
  in forest it has not surveyed, from local habitat cover; fit approximate (a use case the curation wrote). The 2023
  paper's management aim is related work, not a named use case. Regime grouped by region (SPLIT-3).
- Zeros: a species not counted on a transect; absence and non-detection are not separated, and the occurrence file is
  presence-only, so it adds no absences (earlier AI triage, from the Dryad text).
- Siblings and duplicates: none in the log. Family records on the same open question:
  `great_lakes_marsh_bird_point_counts`, `nantucket_sound_sea_duck_aerial_survey_counts`,
  `north_american_breeding_bird_survey_counts`. External collections: none found.
- Metric: none for a prediction (a zero-inflated Poisson model with a spatial iCAR term, Dryad Methods), so the
  fallback `rmse`.
- Risks for /add-dataset: count the rows of Transects.csv (the 2023 paper is related work: measure, do not cite its
  count, PROV-12); check the columns: coordinates or region, and whether Maxent suitability or distance to source
  areas is a column (model outputs: keep as an input or drop); which of the 11 species is the target and its zero
  share; split grouped by region, TP-5 on the grouped folds; the open species-abundance question (triage summary,
  "Policy questions"; SEL-3, USE-1).
- Priority: gap 0 (biology & life sciences 4; regression and grouped not thin), use case 0 (none named), source +
  (paper, Dryad), shape 0 (about 190 transects, a handful of habitat columns), risk - (the paper's key covariate is a
  model output; target species and zero share unknown).
- Reject check (AI, 2026-10-27): does not stand. About 190 transects scattered over the country with habitat covers
  per transect make a multi-site observational survey with habitat covariates, so the call belongs to the open
  species-abundance question; "one small campaign" was a size estimate.

**Assessment (AI, 2026-10-30):** The family's question on species-abundance mapping is settled without a new rule
(Andrej, 2026-10-30, policy question 1 of the zero-inflated review: "I don't think there is new rule to build here.
These are per dataset judgement calls and if a dataset is useful for a predictive application although the data was
collected for something else, then this is fine"), as SEL-2 already reads the scope rules: this record is judged on its
own use case. The verdict and priority stay.

CC (2026-10-30, Andrej): `TBD -> 2nd Tier`, priority 1, as screened (verified on the zero-inflated screening review
page).

Line-transect counts of 11 forest passerines in Morocco with local habitat covers, plus a presence-only occurrence
file for Maxent models (Telleria, Hernandez-Lambrano and Carbonell 2021). Dryad methods: "We counted all birds within
a belt 500 m long and 25 + 25 m wide", with grass, shrub and tree cover assessed at two points per transect. The
study tests the centre-periphery hypothesis (abstract: "we explore if habitat suitability decreases southwards"),
with Maxent habitat suitability, a model output, as the key predictor. `Transects.csv` is 11 KB, roughly 100-200
transects (estimate; not downloaded, Dryad blocks automated downloads).

Zero mechanism, from the Dryad text only: a species not counted on a transect; absence and non-detection are not
separated, and the occurrence file is presence-only, so it adds no absences. A biogeographic hypothesis test on a
small table rather than a count-regression task. Paper not read (Wiley 403). Licence: CC0.

## Reference

Telleria J.L., Hernandez-Lambrano R., Carbonell R. (2021). Ecological and geographical marginality in rear edge
populations of Palaearctic forest birds. Journal of Biogeography 48:2538-2549. doi:10.1111/jbi.14219. Data:
doi:10.5061/dryad.34tmpg4kh.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 34 (Palaearctic rear-edge forest birds).
