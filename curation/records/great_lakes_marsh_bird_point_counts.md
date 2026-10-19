---
unique_name: great_lakes_marsh_bird_point_counts
name: Great Lakes marsh birds / Great Lakes Coastal Wetland Monitoring Program maximum counts, 2011-2021
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
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.5061/dryad.vq83bk40k
- https://doi.org/10.5281/zenodo.10161723
- https://doi.org/10.1093/ornithapp/duad062
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

Marsh-bird point counts of the Great Lakes Coastal Wetland Monitoring Program (Tozer et al. 2023, Birds Canada).
Dryad: "8,120 surveys ... at 1,962 point count locations in 792 coastal wetlands ... 2011-2021". The analysis code
(Zenodo, read as text) uses site, point, year, coordinates, wetland class, basin, area, watershed agriculture and
development, % wetland, lake level, the maximum count of two visits and the species code, i.e. about 70-80k
point-year-species rows (estimate; `CWMP_MaxCount.csv`, 7.2 MB, not downloaded because Dryad blocks automated
downloads). The use is "to quantify the first-ever annual abundance indices and trends" over a rotating panel: trend
estimation, not prediction.

Zero mechanism, from the code only: the species not detected on either visit, zero-filled from an events matrix, with
region-species pairs under 5% occupancy dropped. It is the largest bird survey in this batch, so if the curator wants
a species-abundance task from habitat covariates, this is the one to reopen (grouped by wetland). Licence: CC0 (data),
MIT (code).

## Reference

Tozer D.C., Bracey A.M., Fiorino G.E., et al. (2023). Increasing marsh bird abundance in coastal wetlands of the
Great Lakes, 2011-2021, likely caused by increasing water levels. Ornithological Applications 126:duad062.
doi:10.1093/ornithapp/duad062. Data: doi:10.5061/dryad.vq83bk40k.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 35 (Great Lakes marsh birds).
