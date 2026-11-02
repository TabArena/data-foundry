---
unique_name: dutch_vegetation_plot_species_cover
name: Dutch vegetation-plot plant cover (OZAB) / three-species vegetation-plot records (van Strien et al. 2024)
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
- Two-Regime Zeros
original_source: Other
year: '2024'
domain: biology & life sciences
required_split:
- '?'
problem_type: Other
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.5061/dryad.4xgxd25g4
- https://doi.org/10.1111/jvs.13295
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `No` (`No Good Target / Scientific Discovery`, SEL-3, USE-2): the three-species
extract behind a trend-detection method, with no column besides site, visit, period, species and cover: "Our primary
question is if we can detect species trends in vegetation-plot time series data with this modelling approach" (Dryad
abstract, "Questions.", https://doi.org/10.5061/dryad.4xgxd25g4).
- Source: van Strien, Irvine and Retel 2024 (J. Veg. Sci. 35:e13295); Dryad deposit of 2024-06-14, CC0, from the Dutch
  national vegetation monitoring scheme ("more than 10.000 fixed plots ... surveyed once every four years"). Dryad
  methods: "This data package contains all observations of the species Acer pseudoplantanus, Senecio inaequidens and
  Caltha palustris from the period 1999 - 2022"; cover on "the extended Braun-Blanquet cover scale", ordinal classes.
  Not downloaded (Dryad answers 401 to file requests).
- Deciding reason: the README (Dryad landing page, read by the reject check) lists every column: visits `Site_id`,
  `Visit_id`, `Period`; observations `Site_id`, `Visit_id`, `Species_id`, `Cover`, `Cover_class`; species
  `Species_id`, `Scientific_name`. With no habitat covariate, the only prediction the rows support is a site's cover
  from its id and period, which is the trend the source estimates, a look back at the population (SEL-3, USE-2); the
  family's species-abundance mapping question needs habitat covariates and does not come in.
- Siblings and duplicates: none. The national scheme as a whole (10,000 plots, all species) would be a separate lead,
  not this deposit. `cape_floristic_region_family_cover` is another plant-cover record of the family. External
  collections: none found.
- Papers and pages: paper not read (paywalled; Europe PMC and Unpaywall list no open full text).
- Metric: none for prediction.
- Reject check (AI, 2026-10-27): stands. SEL-3 (Must). The README lists only site, visit, period, species and cover
  columns, no habitat covariate, and the source's question is trend detection
  (https://datadryad.org/dataset/doi:10.5061/dryad.4xgxd25g4).

CC (2026-10-30, Andrej): `No`, as screened (verified on the zero-inflated screening review page).

Dutch vegetation-plot records for three species behind a trend-estimation method (van Strien, Irvine and Retel 2024).
Dryad methods: "This data package contains all observations of the species Acer pseudoplantanus, Senecio inaequidens
and Caltha palustris"; the files are observations, visits and species tables (0.13-0.15 MB, colon-separated; not
downloaded, Dryad blocks automated downloads), and no habitat covariates are listed. The abstract's question is "if
we can detect species trends", and cover was recorded "using the extended Braun-Blanquet cover scale", an ordinal
class. Trend estimation for three species, not a prediction task.

Zero mechanism, from the Dryad text only: the species not recorded at a plot visit, i.e. zeros from filling the
observations against the visits. Workbook pushback: the deposit is not ">10,000 plots" of bounded continuous cover
but three species on an ordinal scale. Paper not read (paywalled). Licence: CC0.

## Reference

van Strien A.J., Irvine K.M., Retel C. (2024). Trends in plant cover derived from vegetation plot data using ordinal
zero-augmented beta regression. Journal of Vegetation Science 35:e13295. doi:10.1111/jvs.13295. Data:
doi:10.5061/dryad.4xgxd25g4.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 33 (Dutch vegetation-plot plant cover (OZAB)).
