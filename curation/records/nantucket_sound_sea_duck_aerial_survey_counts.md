---
unique_name: nantucket_sound_sea_duck_aerial_survey_counts
name: Nantucket Sound sea-duck abundance / aerial strip-transect counts of long-tailed ducks, scoters and eiders, 2003-2006
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
- Non-IID (Temporal)
original_source: Other
year: '2019'
domain: biology & life sciences
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Other
source_links:
- https://doi.org/10.5061/dryad.1vm20t6
- https://doi.org/10.1002/ece3.4738
- https://arxiv.org/abs/1705.00644
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

Aerial survey counts of wintering sea ducks in Nantucket Sound with boosted GAMLSS hurdle models (Smith et al. 2019;
paper read via PMC6405508). A row is one 2.25 km2 segment in one survey: 504 segments, 30 surveys over the winters
2003/04-2005/06 (Methods, "Survey design"), at most 15,120 rows per species. Covariates (Table 1): bathymetry, grain
size, seafloor SAR, tidal velocity, stratification, chlorophyll-a, CDOM, bottom and surface temperature, NAO,
distance to land, coordinates, day of season, year and observation effort. The framing is predictive ("Our predictive
approach incorporates five distinct methodological steps", Methods), for marine spatial planning, but validation is
in-sample only ("Since additional test data were not available for our study area, we used a pseudo R2").

Zero mechanism, from the paper only: no ducks seen in the 91 m strip of a segment during one survey; the authors
"assumed our survey design led to a low incidence of false zeros", and "no eiders were detected in 75% of segment
observations". The 990 MB `NanSound_Ecol&Evol.zip` holds "Raw survey data, fitted models, and code"; most of the
workbook's 4.52 GB is fitted models. Not downloaded (Dryad, and over 200 MB). The one candidate of this batch's
wildlife surveys that could go beyond No: download the zip by hand, check for a segment x survey table with the
covariates, then decide whether a single-region distribution model counts as a prediction task (the ecology
precedents went No). Split: later winters from earlier ones. Licence: CC0.

## Reference

Smith A.D., Hofner B., Lamb J.S., Osenkowski J., Allison T., Sadoti G., et al. (2019). Modeling spatiotemporal
abundance of mobile wildlife in highly variable environments using boosted GAMLSS hurdle models. Ecology and
Evolution 9. doi:10.1002/ece3.4738. Data: doi:10.5061/dryad.1vm20t6.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 58 (Nantucket Sound sea-duck abundance).
