---
unique_name: nantucket_sound_sea_duck_aerial_survey_counts
name: Nantucket Sound sea-duck abundance / aerial strip-transect counts of long-tailed ducks, scoters and eiders, 2003-2006
checked_by:
- Andrej
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- Two-Regime Zeros
- Non-IID (Grouped)
- Multi-target
original_source: Other
year: '2019'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Other
source_links:
- https://doi.org/10.5061/dryad.1vm20t6
- https://doi.org/10.1002/ece3.4738
- https://arxiv.org/abs/1705.00644
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (v4 of 2026-10-19, a list of 69 candidates, not in the repository), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 3: the one source of this batch that frames sea-duck
abundance as a prediction for a named decision (siting offshore wind farms and protected areas); whether the Dryad zip
holds the segment-by-survey table with its covariates is unknown, and the family's species-abundance question is open.
- Source: Mass Audubon aerial strip-transect surveys of Nantucket Sound for the Sea Duck Joint Venture (project 57),
  winters 2003/04-2005/06, published as data with Smith et al. 2019 (Ecology and Evolution 9, doi:10.1002/ece3.4738;
  preprint arXiv 1705.00644, "Spatiotemporal modelling of sea duck abundance: implications for marine spatial
  planning"; Dryad doi:10.5061/dryad.1vm20t6, 15 Feb 2019, CC0, 4.52 GB). As published: "30 (2003/2004:13,
  2004/2005:10, 2005/2006:7) standardized aerial strip-transect surveys" over "504 2.25 km2 segments" (Section 2.1.2,
  Fig. 2), so at most 15,120 segment-surveys per species group (common eider, long-tailed duck, scoters pooled), with
  the covariates of Table 1 (bathymetry, grain size, seafloor variation, FVCOM tidal velocity and temperature, MODIS
  chlorophyll-a and CDOM, NAO, distance to land, ferry routes, coordinates, day of season, year, effort). Dryad holds
  "Raw survey data, fitted models, and code" (Data Accessibility); the file `NanSound_Ecol&Evol` (about 990 MB) has no
  description. Not downloaded: judged from the Dryad metadata and the paper (PMC6405508).
- Use case: the source's own. Models are "crucial for the siting of proposed offshore wind farms" (Introduction) and
  "large-scale models can be used to inform the siting of lease areas or protected areas" (Section 4.2): marine spatial
  planners, before leasing, decide where turbines or protected areas go from the predicted distribution of the ducks.
  Fit direct for predicting the segment counts of later surveys, though "the proposed development was recently
  withdrawn" (Section 2.1.1). Regime temporal (later surveys from earlier ones, SPLIT-6), segments repeat
  (SPLIT-13); three winters only, so windows by survey date (SPLIT-14).
- Zeros: no duck of the group in a segment's strip during a survey; "no eiders were detected in 75% of segment
  observations", and the authors "assumed our survey design led to a low incidence of false zeros" (earlier AI triage,
  2026-10-19, read in the paper).
- Siblings and duplicates: no other record of these surveys. Family records on the same open question:
  `great_lakes_marsh_bird_point_counts`, `wadden_sea_sibes_macoma_abundance`, `noaa_afsc_bottom_trawl_survey_cpue`.
  External collections: none found.
- Papers and pages: Smith et al. 2019 (PMC6405508) and its arXiv preprint; the Sea Duck Joint Venture project page and
  Mass Audubon's interim reports (2003-2006) on the same surveys.
- Metric: the paper scores in-sample fit by a pseudo R2 ("Since additional test data were not available for our study
  area, we used a pseudo R2 measure of the explained variation", Section 2.5) and stops boosting on out-of-bag risk
  (Section 2.3.2); no held-out criterion, so the fallback `rmse` (R2 on a fixed test fold ranks models as RMSE does).
- Risks for /add-dataset: whether the zip holds a segment x survey table with the covariates or only sightings and
  model objects (covariates rebuilt from FVCOM and MODIS would be our construction, PROV-11); MODIS chlorophyll-a and
  CDOM are satellite products, to check as measurements (SEL-15) rather than image descriptors (SEL-13); monthly ocean
  fields and the NAO are known for a surveyed winter, not ahead of one (USE-3); the open species-abundance question
  (SEL-3, USE-1; settled by Andrej on 2026-10-30, policy question 1 of the zero-inflated review: no new rule, each
  survey judged on its own use case); which species group is the target.
- Priority: gap 0 (biology & life sciences 4; regression and temporal not thin), use case + (the source names the
  planners and the siting decision), source + (paper with a covariate table, Dryad, preprint), shape + (up to 15,120
  segment-surveys per group, mixed covariates, spatial and temporal structure), risk - (release contents unknown).

**Assessment (AI, 2026-10-30):** The family's question on species-abundance mapping is settled without a new rule
(Andrej, 2026-10-30, policy question 1 of the zero-inflated review: "I don't think there is new rule to build here.
These are per dataset judgement calls and if a dataset is useful for a predictive application although the data was
collected for something else, then this is fine"), as SEL-2 already reads the scope rules: this record is judged on its
own use case. The verdict and priority stay.

CC (2026-10-30, Andrej): `Yes`, priority 3 (the AI screening had `TBD -> 2nd Tier`, priority 3; zero-inflated screening
review page). "Just try to add it and if it turns out a bad task, then we drop it to no"

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

**Assessment (AI, 2026-11-01):** added as `datasets/_dev/tabarena-v0pt2/nantucket_sound_sea_duck_aerial_survey_counts/` by /add-dataset with the full review panel; the open questions are in its Review. Recommend shipping, scored by the Poisson deviance if you agree (issue 2; `rmse` stays declared and the build waits). Changes after the panel: re-split on 3 x 3 grid blocks (single segments kept same-day neighbours in training, about 30% of the score). Corrections to the notes above: 454 segments and 7,751 segment-days, not 504 and up to 15,120; the strip is about 180 m (two observers' 91 m sides), not 91 m; the "crucial" quote is about understanding the ducks' winter habitat use and distribution, not siting; the source's R^2 is Nagelkerke's pseudo-R^2 on its hurdle likelihood; the regime is grouped by grid blocks, not temporal (TP-10 leg 1 fails for a later winter); the fit is approximate, not direct. Your condition: a modest real signal (untuned LightGBM R^2 0.18 on log1p on the block splits), so it stays `Yes`. `required_split` and `tags` wait for your marks on the field rows. Priority 2: gap 0, use case 0 (fit approximate), source + (CC0 deposit and paper), shape + (60 blocks), risk - (weak signal; the metric is open).

CC (2026-11-02, Andrej): metric (Review issue 2, cross-dataset item zi-count-metric): "add `mean_poisson_deviance` to the library, nantucket declares it, wadden and pennsylvania keep theirs". The mean Poisson deviance on the count replaces RMSE, a stand-in for the source's out-of-bag likelihood.

**Assessment (AI, 2026-11-02):** applied. `mean_poisson_deviance` (scikit-learn's metric, with an optional `min_prediction` floor) is in `data_foundry.v2.metrics` with tests against scikit-learn; the definition declares `Metric.stand_in("mean_poisson_deviance", params={"min_prediction": 0.01}, target_transform="log1p")`: predictions are inverted from log1p to the count and floored at 0.01 ducks, the floor the review panel measured with, so a model predicting no ducks still scores (scikit-learn refuses a prediction of 0). On the block splits the Poisson fit was 9.8% below the training mean on 9 of 9 splits and the log1p tree fits 13-15% above it, where RMSE put both within 0.2% of the mean. `dataset check`: 0 errors. Set apart from wadden and pennsylvania, which keep RMSE: this source names one count-likelihood criterion.

CC (2026-11-03, Andrej): the split holds out whole transect columns, the field's practice (issue 1): "We should definitely use what the field uses. We should stay as realistic and close to the real application as possible." The zero warning is accepted (issue 4): "We accept since this is a totally valid zero-inflated regression task".

CC (2026-11-03, Andrej): the record takes the definition's `required_split` (Grouped (NON-IID)) and tag (Non-IID (Grouped)), after the split by transect columns.

CC (2026-11-03, Andrej): 2nd Tier, not shipped: "I realized that this is a multi-target task. Therefore I declare it 2nd tier and don't ship." Each segment-day holds three distinct counts (long-tailed duck, eider, scoters), which the source models one by one; the format ships one target per dataset. Tag `Multi-target` added. The v2 folder left the working copy; its last definition (transect-column split, Poisson deviance, TabPFN per species D^2 0.153 / 0.219 / 0.346) is in the run folder of 2026-11-03, the committed one in 902011b3.

## Reference

Smith A.D., Hofner B., Lamb J.S., Osenkowski J., Allison T., Sadoti G., et al. (2019). Modeling spatiotemporal
abundance of mobile wildlife in highly variable environments using boosted GAMLSS hurdle models. Ecology and
Evolution 9. doi:10.1002/ece3.4738. Data: doi:10.5061/dryad.1vm20t6.

Lead: the two-regime-zero workbook (v4, 2026-10-19), Master row 58 (Nantucket Sound sea-duck abundance).
