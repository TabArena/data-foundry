---
unique_name: svalbard_reindeer_total_count_pixels
name: Svalbard reindeer total-count pixels / total count data for hurdle models (Le Moullec et al. 2019)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: Other
year: '2019'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.5061/dryad.7351kt1
- https://doi.org/10.1002/jwmg.21761
- https://doi.org/10.18710/KHQKWH
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

The workbook conflates two sources. Its DOI, 10.18710/KHQKWH, is a DataverseNO release of 2021 drone imagery of
Sassendalen (raw JPG archives of about 73 GB, an orthomosaic, tiles "used for the manual counting", DEMs), with no
count table and a manuscript "in preperation". The pixel table it describes is Le Moullec et al. (2019) on Dryad
(`Total count data for hurdle models.xlsx`, 0.63 MB; not downloaded, Dryad blocks automated downloads). There a row
is a 240 x 240 m pixel of 33 total-count sites (about 1,350 km2, 1,349 clusters with 3,898 animals, 2013-2016), the
target is reindeer per pixel, and the features are NDVI, past extirpation (0/1) and two UTM coordinates (pp. 4-5).
The aim (p. 2): "to estimate the current Svalbard reindeer distribution and abundance across the archipelago to
evaluate the success of the 1925 conservation action".

Zero mechanism, from the paper only: total counts "assume that all animals within a defined area are detected with
certainty" (p. 4), so a zero is a pixel without reindeer on the count day; about 23,400 pixels against 1,349 clusters
implies at least 94% zeros (an estimate from the paper's numbers). The counts were made in the field, not read off
images. A population estimate from four features, two of them coordinates, is not a prediction task. Licence: CC0.

## Reference

Le Moullec M., Pedersen A.O., Stien A., Rosvold J., Hansen B.B. (2019). A century of conservation: The ongoing
recovery of Svalbard reindeer. Journal of Wildlife Management 83(8):1676-1686. doi:10.1002/jwmg.21761. Data:
doi:10.5061/dryad.7351kt1. The workbook's link: Hann R. (2021), drone-based mapping of Sassendalen,
doi:10.18710/KHQKWH.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 59 (Svalbard reindeer total-count pixels).
