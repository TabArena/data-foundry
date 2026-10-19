---
unique_name: sacramento_green_sturgeon_sonar_counts
name: Green Sturgeon abundance / side-scan sonar counts in Sacramento River spawning pools, 2020-2022
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: Other
year: '2023'
domain: biology & life sciences
required_split:
- '?'
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.7291/D1738V
- https://doi.org/10.5281/zenodo.7783467
- https://doi.org/10.1139/cjfas-2023-0228
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

Repeated side-scan sonar counts of green sturgeon in spawning pools (Battaile et al. 2024): pool-by-pass count
matrices for 32, 38 and 69 pools in 2020-2022 with 3-7 passes, plus a size-restricted 2022 subset (`Count2022S`),
about 2 KB each (not downloaded; Dryad blocks automated downloads). The analysis is population estimation with
N-mixture models and no features at all; Data Analysis (accepted manuscript, p. 10): "if there are no covariates, as
in our case". The abstract ends by recommending "much simpler population estimates".

Zero mechanism, from the paper only: no sturgeon seen on a pass, non-detection or absence; "a large percentage of
zeroes (32 of 90)" in 2020 (Results). Agrees with the workbook that the observed counts are not abundance, and adds
that there is nothing to predict them from. Licence: CC0.

## Reference

Battaile B., Mora E., Lehman B., Dudley P. (2024). Estimating spawning green sturgeon abundance in the Sacramento
River using side-scan sonar and N-mixture models. Canadian Journal of Fisheries and Aquatic Sciences 81:935-951.
doi:10.1139/cjfas-2023-0228. Data: doi:10.7291/D1738V.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 40 (Green Sturgeon abundance).
