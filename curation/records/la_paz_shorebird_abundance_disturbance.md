---
unique_name: la_paz_shorebird_abundance_disturbance
name: Non-breeding shorebirds in a subtropical wetland / shorebird counts and human disturbance, Ensenada de La Paz
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
- Too Small
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: Other
year: '2022'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.5061/dryad.cjsxksn85
- https://doi.org/10.5281/zenodo.6685707
- https://doi.org/10.1111/btp.13139
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

Shorebird counts at 12 sampling units of a Baja California Sur wetland, 15 visits each from September 2014 to April
2015, i.e. 180 surveys (Palacios et al. 2022; Dryad methods). The R code (Zenodo, read as text) fits a
zero-inflated negative binomial in long format, one row per survey and species (21 species, about 3,800 rows by
estimate): count ~ log(area) + habitat + % flooded + human and raptor events per minute, with random effects for
unit and species. Dryad methods: "We conducted an observational cross-sectional study with repeated surveys to
determine effects of potential raptor and human disturbance on abundance of shorebirds." Inference with 12
independent units. The one data file is Apple Numbers (`ds3_fin.numbers`, 1.02 MB) and was not downloaded (Dryad
blocks automated downloads).

Zero mechanism, from the paper and code only: a species not counted on a visit, in a zero-filled species-by-survey
matrix; the usage notes say "the distribution of shorebird counts had excess zeros and was overdispersed". Licence:
CC0.

## Reference

Palacios E., Vargas J., Fernandez G., Reiter M.E. (2022). Impact of human disturbance on the abundance of
non-breeding shorebirds in a subtropical wetland. Biotropica 54:1160-1169. doi:10.1111/btp.13139. Data:
doi:10.5061/dryad.cjsxksn85.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 36 (Non-breeding shorebirds in subtropical
wetland).
