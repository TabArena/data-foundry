---
unique_name: la_paz_shorebird_abundance_disturbance
name: Non-breeding shorebirds in a subtropical wetland / shorebird counts and human disturbance, Ensenada de La Paz
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
- Too Small
tags:
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
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `No` (`No Good Target / Scientific Discovery`, SEL-3, USE-2): an observational study
of the effect of human and raptor disturbance on shorebird abundance at 12 units of one wetland in one season; no
prediction task in the source, and no decision acts on a per-survey prediction.
- Source: Palacios, Vargas, Fernández and Reiter 2022, "Impact of human disturbance on the abundance of non-breeding
  shorebirds in a subtropical wetland", Biotropica 54(5):1160-1169 (doi:10.1111/btp.13139, checked on Crossref); Dryad
  doi:10.5061/dryad.cjsxksn85 (22 Jun 2022, CC0), one Apple Numbers file of about 1 MB; R code on Zenodo 6685707. As
  published: 12 sampling units in Ensenada de La Paz, each surveyed 15 times from September 2014 to April 2015, with
  the counts per species and, per survey, the habitat, flooding, human disturbances and raptors (Dryad Methods); about
  3,800 survey-species rows by the earlier AI triage's estimate from the code (2026-10-19). Not downloaded.
- Deciding words: "We conducted an observational cross-sectional study with repeated surveys to determine effects of
  potential raptor and human disturbance on abundance of shorebirds" (Dryad, Methods, checked 2026-10-27); "we studied
  the influence of human disturbance on shorebird community dynamics during migration and winter", "Twelve sampling
  units were surveyed twice a month ... from September 2014 to April 2015", with mixed models "to quantify
  associations" (Dryad, as quoted by the reject check).
- Use case: none (USE-1, USE-2). Disturbance rates are counted on the same visit as the birds, so no prediction point
  precedes the count, and a manager restricting access acts on the effect estimate, not on a prediction per unit and
  survey.
- Siblings and duplicates: no other record of this study. In this batch the multi-site surveys
  `plains_wanderer_spotlight_counts` and `morocco_forest_bird_transect_counts` went to `TBD -> 2nd Tier`; this one is
  a single-site effect study. External collections: none found.
- Metric: none (no task; a zero-inflated negative binomial mixed model with random effects for unit and species, Dryad
  usage notes).
- `Too Small` stays only as a provisional marker from the earlier pass: never measured (TP-5 needs the task's splits)
  and no part of the reason.
- Reject check (AI, 2026-10-27): stands. SEL-3 (Must). A single-site effect study: 12 units of one wetland, Ensenada
  de La Paz, surveyed "to determine effects of potential raptor and human disturbance on abundance of shorebirds"
  (https://doi.org/10.5061/dryad.cjsxksn85).

CC (2026-10-30, Andrej): `No`, as screened (verified on the zero-inflated screening review page).

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
