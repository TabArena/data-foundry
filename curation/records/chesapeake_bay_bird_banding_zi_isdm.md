---
unique_name: chesapeake_bay_bird_banding_zi_isdm
name: Species abundance from occurrence + presence-only data / zero-inflated integrated SDM, Chesapeake Bay birds (Gonnerman et al. 2026)
checked_by:
- Andrej
suggestion: TBD -> Yes
priority: 1
decision_markers:
- No Good Target / Scientific Discovery
- Needs extensive data wrangling
- Available on Request
tags:
- Two-Regime Zeros
original_source: Other
year: '2026'
domain: biology & life sciences
required_split:
- '?'
problem_type: Regression
original_data_state: Other
source_links:
- https://doi.org/10.5061/dryad.pnvx0k729
- https://doi.org/10.1016/j.ecolmodel.2026.111712
- https://pubs.usgs.gov/publication/70276934
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (v4 of 2026-10-19, a list of 69 candidates, not in the repository), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 1: a species-distribution methods paper whose public
release holds only presence-only banding records (counts of at least one); the eBird checklists that carry the zeros
are not distributed, so any task would be a rebuild from eBird.
- Source: Gonnerman, Mullinax, Sullivan, Kent and Prosser 2026, Ecological Modelling 521:111712 (USGS publication
  70276934); Dryad doi:10.5061/dryad.pnvx0k729 (27 Jul 2026, CC0, 1.79 GB). As published: `ModValData_PO.csv`
  (433.55 KB, Bird Banding Lab presence-only observations with covariates), a prediction grid `PredPoints` (shapefile,
  1.53 GB attribute table; habitat covariates such as distance to water and roads and land-cover counts within 1 km
  and 10 km; no response), the study area (counties around Chesapeake Bay and their neighbours) and R scripts. README:
  "eBird data is referenced as ModValData_OC.csv in code, but is not available for distribution". Not downloaded:
  judged from the Dryad page and README; the paper itself was not read.
- Aim, in the source's words: "We present a novel zero-inflated extension of an integrated SDM framework for a Poisson
  regression (ZI-iSDM)", tested on simulations and then "applied this model to real survey data for multiple wild bird
  species"; modelling tools for species distributions are "becoming increasingly valuable for conservation planning
  and response" (Abstract, on the USGS page). A species distribution model falls under the family's open
  species-abundance question, so this is not a fast reject.
- Use case: for example a wildlife agency mapping the relative abundance of a bird species over the counties for
  conservation planning or disease response; the source names no actor or decision; fit approximate. Regime grouped
  by location (cells without a survey) if rebuilt.
- Zeros: none in the release. The observed zeros are non-detections on eBird checklists, which the authors could not
  redistribute; the eBird Basic Dataset is available on request (a licence note, not a reason, EV-4).
- Siblings and duplicates: no record of this DOI, of eBird or of banding data. Family records on the same open
  question: `great_lakes_marsh_bird_point_counts`, `nantucket_sound_sea_duck_aerial_survey_counts`. External
  collections: none found.
- Papers and pages: the paper (not read; the earlier pass got 403 from ScienceDirect); the USGS publication page; the
  Dryad README.
- Metric: none found (abstract, USGS page, README; the scripts ModVal-1 to -3 select model structures by a criterion
  not read), so the fallback `rmse`.
- Risks for /add-dataset: the target cannot be formed from the release; a rebuild needs the eBird Basic Dataset and
  the paper's filters, which makes eBird its origin and a record of its own (PROV-11); which species (not named in the
  abstract); the open species-abundance question (SEL-3, USE-1; settled by Andrej on 2026-10-30, policy question 1 of
  the zero-inflated review: no new rule, each survey judged on its own use case).
- Priority: gap 0 (biology & life sciences 4; regression not thin), use case 0 (none named), source + (paper, README,
  code), shape 0 (no zeros and no checklists in the release), risk - (no target without a rebuild).

**Assessment (AI, 2026-10-30):** The family's question on species-abundance mapping is settled without a new rule
(Andrej, 2026-10-30, policy question 1 of the zero-inflated review: "I don't think there is new rule to build here.
These are per dataset judgement calls and if a dataset is useful for a predictive application although the data was
collected for something else, then this is fine"), as SEL-2 already reads the scope rules: this record is judged on its
own use case. The verdict and priority stay.

**Consistency check (AI, 2026-10-30):** the review page sets `Yes`, priority 1. The release cannot form a target by
itself: its zeros come from eBird data, "not available for distribution", obtained through eBird's request form. By the
curator's request rule of the same day that is 2nd Tier (`heritage_health_prize`,
`shaoxing_hourly_precipitation_fusion`). What may set it apart: eBird's form is routinely approved and the release ships
the covariate grid. Options: `Yes` with that fact, or 2nd Tier.

CC (2026-10-30, Andrej): `TBD -> 2nd Tier`, priority 1 (the AI screening had `TBD -> 2nd Tier`, priority 1;
zero-inflated screening review page, after the AI's consistency check). "Data needs request"

CC (2026-10-30, Andrej), in chat: `TBD -> Yes`, priority 1: "Data on request shall be a TBD then for the cases where it
mattered." The verdict rests on the merits; `Available on Request` records that the request is still to be made (EV-4:
access alone decides no verdict).

A methods paper on a zero-inflated integrated species distribution model, validated on simulations and applied to
birds of the counties around Chesapeake Bay. The public part is `ModValData_PO.csv` (0.43 MB): Bird Banding Lab
presence-only captures with counts of at least one and covariates. The Dryad README: "eBird data is referenced as
ModValData_OC.csv in code, but is not available for distribution". `PredPoints` (1.8 GB) is a prediction grid without
a response. Not downloaded (Dryad blocks automated downloads).

Zero mechanism: none in the public part. Banding records are presence-only, and the real zeros (non-detections on
eBird checklists) are withheld. Rebuilding them needs the eBird Basic Dataset (a request form, so only a licence
note) and the paper's filters, which were not read (ScienceDirect 403), and would give a table we assembled
ourselves. Agrees with the workbook's "partial release" and goes further: the release cannot form a target with real
zeros at all. Licence: CC0 (Dryad).

## Reference

Gonnerman M., Mullinax J., Sullivan J., Kent C., Prosser D. (2026). Improved estimates of relative occurrence and
abundance using opportunistic surveys and presence-only observations: A zero-inflated integrated species
distribution model. Ecological Modelling 521:111712. doi:10.1016/j.ecolmodel.2026.111712. Data:
doi:10.5061/dryad.pnvx0k729.

Lead: the two-regime-zero workbook (v4, 2026-10-19), Master row 45 (Species abundance from occurrence +
presence-only data).
