---
unique_name: great_lakes_marsh_bird_point_counts
name: Great Lakes marsh birds / Great Lakes Coastal Wetland Monitoring Program maximum counts, 2011-2021
checked_by:
- Andrej
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target / Scientific Discovery
tags:
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
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (v4 of 2026-10-19, a list of 69 candidates, not in the repository), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 2: a basin-wide marsh-bird monitoring table that ships its
own habitat covariates but was published for trends; whether abundance mapped from habitat counts as a prediction task
is the family's open species-abundance question, and this is one of the two cases named to settle it.
- Source: Great Lakes Coastal Wetland Monitoring Program point counts, published with Tozer et al. 2023
  (Ornithological Applications 126:duad062; Dryad doi:10.5061/dryad.vq83bk40k, 7 Dec 2023, CC0; code Zenodo 10161723).
  As published: one flat file `CWMP_MaxCount.csv` (7.24 MB), one row per point, year and species: the "Maximum number of
  individuals observed during either of the 2 surveys" for 1 of 18 species, with site, point, year, coordinates,
  wetland type, lake basin, region, wetland area, watershed id, "Percent local wetland cover within 250 m",
  "Detrended, standardized Great Lakes water level" and watershed % urban and % agricultural cover (Dryad README).
  "The dataset consisted of 8,120 surveys completed at 1,962 point-count locations in 792 coastal wetlands", 2011-2021
  (Methods). About 70-80k rows by the earlier AI triage's estimate from the code (2026-10-19). Not downloaded: Dryad
  files were not fetched, so this rests on the README and the paper.
- Aim, in the source's words: "Our objective was to quantify annual abundance indices and trends of 18 marsh-breeding
  bird species" (Introduction). Not a fast reject: a broad survey whose release carries habitat covariates falls
  under the open species-abundance question.
- Use case: none named for a prediction. For example, a wetland agency estimating a species' abundance at coastal
  wetlands it has not surveyed, from wetland and watershed cover, to rank them for protection or restoration (the lay
  summary asks for "protection and restoration of coastal wetlands"); fit approximate, a use case the curation wrote.
  Regime grouped by wetland, as the use maps wetlands without a survey (SPLIT-3); points repeat over years (SPLIT-13).
- Zeros: a species not detected on either visit, zero-filled against the survey events, with region-species pairs
  under 5% occupancy dropped (earlier AI triage, 2026-10-19, read in the code): an observed non-detection.
- Siblings and duplicates: no other record of this program or DOI. Family records on the same open question:
  `nantucket_sound_sea_duck_aerial_survey_counts`, `wadden_sea_sibes_macoma_abundance`,
  `noaa_afsc_bottom_trawl_survey_cpue` (AI drafts, no curator call yet). External collections: none found.
- Papers and pages: Tozer et al. 2023 (read on academic.oup.com); the program's survey data are also "available by
  request at https://www.greatlakeswetlands.org" (README).
- Metric: none found for a prediction (the paper estimates indices and trends with a Bayesian INLA model, Methods;
  Dryad README), so the fallback `rmse`; a count deviance would be a family-level choice for the curator.
- Risks for /add-dataset: the open species-abundance question (SEL-3, USE-1; settled by Andrej on 2026-10-30, policy
  question 1 of the zero-inflated review: no new rule, each survey judged on its own use case);
  which of the 18 species is the target; the water level is detrended and standardized over all years, one value per
  lake and year (LEAK-30, weak); the maximum of two visits mixes detection with abundance, and the occupancy filter
  shapes the zero share.
- Priority: gap 0 (biology & life sciences 4; regression and grouped not thin), use case 0 (none named for a
  prediction), source + (paper, README, code), shape + (about 70-80k point-years at 1,962 points in 792 wetlands, mixed
  covariates, grouped and temporal structure), risk - (target and task unsettled).

**Assessment (AI, 2026-10-30):** The family's question on species-abundance mapping is settled without a new rule
(Andrej, 2026-10-30, policy question 1 of the zero-inflated review: "I don't think there is new rule to build here.
These are per dataset judgement calls and if a dataset is useful for a predictive application although the data was
collected for something else, then this is fine"), as SEL-2 already reads the scope rules: this record is judged on its
own use case. The verdict and priority stay.

CC (2026-10-30, Andrej): `TBD -> 2nd Tier`, priority 2, as screened (verified on the zero-inflated screening review
page).

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

Lead: the two-regime-zero workbook (v4, 2026-10-19), Master row 35 (Great Lakes marsh birds).
