---
unique_name: svalbard_reindeer_total_count_pixels
name: Svalbard reindeer total-count pixels / total count data for hurdle models (Le Moullec et al. 2019)
checked_by:
- Andrej
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target / Scientific Discovery
tags:
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
- '# Workbook link, another release: drone imagery of Sassendalen (Hann 2021), no count table'
- https://doi.org/10.18710/KHQKWH
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 2: reindeer counts per 240 m pixel from field total counts
at 33 Svalbard sites, which the source used to map abundance over the archipelago for a status estimate; an
abundance-mapping use, but four features, two of them coordinates.
- Source: Le Moullec, Pedersen, Stien, Rosvold and Hansen, Journal of Wildlife Management 83(8):1676-1686 (2019),
  doi:10.1002/jwmg.21761; data on Dryad, doi:10.5061/dryad.7351kt1 (CC0): two distance-sampling tables and `Total count
  data for hurdle models.xlsx` (0.63 MB, a data sheet and a legend sheet); "A script and prediction tables are available
  on request" (Dryad usage notes). The workbook's DOI, 10.18710/KHQKWH, is another release: "a series of drone-based
  aerial images that were collected for the purpose of counting reindeer" in Sassendalen, 2021 (DataverseNO description;
  raw image archives of 6-24 GB each, no count table); it stays in `source_links` with a note.
- As published (earlier AI triage, 2026-10-19, read on pp. 4-5 of the paper; not re-read, the publisher answers 403, and
  the xlsx not downloaded, Dryad answers 401): a row is a pixel of 33 total-count sites (about 1,350 km2, 1,349 groups,
  2013-2016), the target reindeer per pixel, the features NDVI, past extirpation (0/1) and two UTM coordinates; at least
  94% zeros estimated from the paper's numbers, not measured.
- Use case: the source's aim is a status estimate: "An assessment of the current distribution and abundance is therefore
  urgently needed", and "These incompletely recovered areas are potential targets for increased monitoring frequency and
  maintaining strict conservation" (Dryad abstract). For example Svalbard's management estimating abundance in areas
  without a count; no actor is named, fit approximate. Regime grouped by count site (neighbouring pixels share a site).
- Doubt: the earlier pass set `No` ("a population estimate from four features ... is not a prediction task"), a
  reading; the open species-abundance-mapping question applies. Unlike the other records of the batch, the source
  itself predicts: it estimates "the Svalbard reindeer distribution and abundance across its entire range" from
  counts covering part of it (Dryad abstract), with "prediction tables" on request.
- Siblings and duplicates: none in the log (searched reindeer, Svalbard, Rangifer). External collections: none found.
- Papers and pages: the paper; the Dryad abstract; the MOSJ environmental-monitoring indicator for Svalbard reindeer
  (mosj.no).
- Metric: none verified (the paper's text was not read in this pass); fallback `rmse`.
- Risks for /add-dataset: four features, two of them coordinates, so a split by site leaves NDVI and the extirpation
  flag; NDVI is a satellite index used by the field as a productivity covariate (SEL-15 rather than SEL-13, to confirm);
  the legend sheet and the zero share to check on the file.
- Priority: gap 0, use case 0 (no actor named), source + (paper, Dryad legend sheet), shape 0 (about 23,400 pixels but
  four features), no known risk.

**Assessment (AI, 2026-10-30):** The family's question on species-abundance mapping is settled without a new rule
(Andrej, 2026-10-30, policy question 1 of the zero-inflated review: "I don't think there is new rule to build here.
These are per dataset judgement calls and if a dataset is useful for a predictive application although the data was
collected for something else, then this is fine"), as SEL-2 already reads the scope rules: this record is judged on its
own use case. The verdict and priority stay.

**Consistency check (AI, 2026-10-30):** the review page sets `No` ("Actually an image task I guess"). By the record, the
target comes from field counts and the features are NDVI, an extirpation flag and two coordinates; the drone imagery is
another release. If NDVI per pixel counts as image-derived (SEL-13), the marker is `Image`; if the reason is that four
features, two of them coordinates, make no real task, it is `No Good Target / Scientific Discovery`. Which one, or 2nd
Tier?

CC (2026-10-30, Andrej): `TBD -> 2nd Tier`, priority 2 (the AI screening had `TBD -> 2nd Tier`, priority 2;
zero-inflated screening review page, after the AI's consistency check).

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
