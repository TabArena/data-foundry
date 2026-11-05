---
unique_name: sacramento_green_sturgeon_sonar_counts
name: Green Sturgeon abundance / side-scan sonar counts in Sacramento River spawning pools, 2020-2022
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
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
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (v4 of 2026-10-19, a list of 69 candidates, not in the repository), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `No` (`No Good Target / Scientific Discovery`, SEL-3): repeated sonar counts per pool
for a yearly population estimate, with no covariate of abundance to predict a count from.
- Source: Battaile, Mora, Lehman and Dudley, Dryad doi:10.7291/D1738V (2023-04-06, CC0; Zenodo companion record
  7783467, MIT); paper Battaile et al. 2024, Can. J. Fish. Aquat. Sci. 81:935-951 (open access; read on the NOAA
  repository, https://repository.library.noaa.gov/view/noaa/61755). As published (Dryad file list from its metadata
  API, 2026-10-27; files not downloaded, Dryad refuses automated downloads): `Count2020.csv`, `Count2021.csv`,
  `Count2022.csv`, `Count2022S.csv` (pool-by-pass counts, about 2 KB each; 32, 38 and 69 pools, 3 to 7 passes),
  `UpDownStream.txt` (the pass direction) and `README.md`; nothing else.
- Use case: none. Introduction (p. 936): "Our overall objective of this research was to evaluate the ability for
  side-scan sonar (SSS) and N-mixture models to improve upon estimates of green sturgeon abundance relative to the
  current system"; Data analysis (p. 938): "but if there are no covariates, as in our case"; p. 939: "In our case, we
  only investigated a model that incorporated covariates into detectability, which we noticed is greatly influenced by
  the direction of the survey relative to the river flow"; Discussion (pp. 948-949): "our covariate data were not
  informative enough to help in this regard". The only covariate is the pass direction, for detection; a count has
  nothing to be predicted from but its pool and pass, and the output is a yearly population estimate against a
  recovery criterion (Abstract), a survey statistic.
- Siblings and duplicates: none (grep sturgeon, side-scan, N-mixture). External collections: none.
- Metric: none (no task).
- Zeros: "a large percentage of zeroes (32 of 90)" (Results) is a detection question inside the estimate, not a target.
- Reject check (AI, 2026-10-27): stands. SEL-3 (Must). The release is four pool-by-pass count matrices and a pass
  direction file, and the paper states "if there are no covariates, as in our case" (p. 938,
  https://repository.library.noaa.gov/view/noaa/61755).

CC (2026-10-30, Andrej): `No`, as screened (verified on the zero-inflated screening review page).

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

Lead: the two-regime-zero workbook (v4, 2026-10-19), Master row 40 (Green Sturgeon abundance).
