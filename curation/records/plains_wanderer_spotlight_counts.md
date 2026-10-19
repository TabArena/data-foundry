---
unique_name: plains_wanderer_spotlight_counts
name: Plains-wanderer abundance / spotlight surveys at 16 grassland sites, 2014-2022
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
year: '2024'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.5061/dryad.t1g1jwtb9
- https://doi.org/10.1002/eap.3046
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

Spotlight counts of the endangered plains-wanderer (Parker et al. 2024, UNSW; paper read via PMC11610650). Methods:
"Field surveys were conducted at 16 sites", one to three times a year, "giving a total of 249 surveys" (2014-2022),
with grass height, fox presence and location as predictors. The aim is explanatory ("The aim of this study was to
investigate the impact of grassland structure and fox numbers on plains-wanderer abundance", Introduction), and both
predictors came out non-significant. One 32 KB xlsx; not downloaded (Dryad blocks automated downloads).

Zero mechanism, from the paper only: no bird inside the 5.2 m effective strip. Birds were seen on 16.45% of surveys,
i.e. 41 positive surveys and about 84% zeros, and the authors argue the zeros are real ("we are confident that
absences were predominantly true zeroes because we restricted our analyses to observations within the effective
strip"). Workbook pushback: the 249 "transects" are repeat visits to 16 sites, so a grouped split leaves a handful of
sites and positives per fold. Licence: CC0.

## Reference

Parker D., Cameron M., Gordon C., Letnic M. (2024). Habitat structure and an introduced predator limit the abundance
of an endangered ground-nesting bird. Ecological Applications 34:e3046. doi:10.1002/eap.3046. Data:
doi:10.5061/dryad.t1g1jwtb9.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 16 (Plains-wanderer abundance).
