---
unique_name: dutch_vegetation_plot_species_cover
name: Dutch vegetation-plot plant cover (OZAB) / three-species vegetation-plot records (van Strien et al. 2024)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
tags:
- AI-Filled (Verify)
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
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

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
