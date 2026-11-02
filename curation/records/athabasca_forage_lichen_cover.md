---
unique_name: athabasca_forage_lichen_cover
name: Lichen percent cover / forage-lichen plots for caribou habitat mapping (Keim et al. 2017)
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- Not Available (from Paper))
- Image
tags:
- Two-Regime Zeros
original_source: Other
year: '2017'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
source_links:
- https://doi.org/10.1002/ece3.2625
- https://pmc.ncbi.nlm.nih.gov/articles/PMC5243790/
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 1: forage-lichen cover at 438 plots in the Athabasca oil
sands, mapped from satellite, LiDAR and groundwater covariates for caribou habitat reclamation; the family's open
species-abundance question applies, and the table was never released, so a request to the authors is the next step.
- Source: Keim, DeWitt, Fitzpatrick and Jenni 2017 (Ecology and Evolution 7:486-493, read via PMC5243790). Results:
  "Field crews sampled 438 vegetation plots (251 fixed and 187 opportunistic plots)" and "A large number of survey plots
  contained zero lichen cover (n = 98)". As published: no data statement; the supplementary material is three Word
  appendices (`ECE3-7-486-s001.docx` to `s003.docx`); Dryad (search "Keim lichen caribou": 0 hits) and Zenodo hold no
  deposit.
- Use case: the first objective is to "delineate the geographic distribution and abundance of terrestrial forage
  lichens" (Introduction), with estimates "interpolated on a map at fine resolution across a caribou range to support
  ecological conservation and reclamation" (Abstract), where "there is a need for cost-effective and timely management
  tools that can be used to maintain and recover woodland caribou habitat" (Sec. 2). For example a reclamation planner
  choosing where lichen can be restored; fit approximate. Regime grouped by space (survey transects, SPLIT-3).
- Siblings and duplicates: `boreal_postfire_lichen_biomass` is another study (post-fire chronosequence, data on
  Dryad); `korea_bee_sting_injuries_district_year` (this run) is the same situation, an unreleased table with a request
  route, kept as 2nd Tier. External collections: none found.
- Papers and pages: the paper only.
- Metric: the paper reports the R2 of field against fitted values ("R 2 = .74", Abstract) and selects covariates by
  AIC; no held-out score is named as the criterion (MET-5), so the fallback `rmse`.
- Risks for /add-dataset: (1) ask the corresponding author (Keim, Matrix Solutions Inc.) for the 438-plot table, then
  `Data Requested`; (2) SEL-13: the final model uses QuickBird blue and near-infrared reflectance and seasonal NDVI
  change beside LiDAR height and groundwater depth; (3) the Sphagnum covariate was modelled from the same plots ("we
  used our data to develop a spatial covariate for Sphagnum moss cover", Methods, Supporting Information 3; LEAK-27,
  LEAK-10); (4) preferential sampling: opportunistic plots were taken only "if crews encountered a lichen patch with
  >10% lichen cover" (Methods), so keep the 251 fixed-grid plots or note `Not Representative`; (5) a spatial grouped
  split and TP-5 on its folds. Open question: species-abundance mapping from habitat covariates.
  `Not Available (from Paper))` stays as the marker of the current state (not public, request not yet made), as on
  `korea_bee_sting_injuries_district_year`.
- Priority: gap 0 (biology, regression and grouped are not thin), use case 0 (an example, no actor named), source + (a
  peer-reviewed paper documents the plots and covariates), shape 0 (438 plots), risk - (no released table, reflectance
  covariates, preferential sample).
- Reject check (AI, 2026-10-27): does not stand. No Must rule fails: the marker has no rule, SEL-3 does not reach a
  mapping aim and the source is known; unlike Lennart's churn-paper rejects ("too old to request / no request form"),
  this 2017 paper names a corresponding author and funders, so the request route is open.

**Assessment (AI, 2026-10-30):** The family's question on species-abundance mapping is settled without a new rule
(Andrej, 2026-10-30, policy question 1 of the zero-inflated review: "I don't think there is new rule to build here.
These are per dataset judgement calls and if a dataset is useful for a predictive application although the data was
collected for something else, then this is fine"), as SEL-2 already reads the scope rules: this record is judged on its
own use case. The verdict and priority stay.

**Consistency check (AI, 2026-10-30):** the review page sets `No` (no note). The curator's own rule of the same day
sends data that must be requested to 2nd Tier (`heritage_health_prize`, `shaoxing_hourly_precipitation_fusion`), and
`korea_bee_sting_injuries_district_year`, the same situation (a paper's table, request route open), stayed 2nd Tier. Is
there another reason for `No`: the reflectance covariates (SEL-13), the Sphagnum covariate modelled from the same plots
(LEAK-27), the opportunistic plots? If so it is recorded; otherwise 2nd Tier like korea.

CC (2026-10-30, Andrej): `No` (the AI screening had `TBD -> 2nd Tier`, priority 1; zero-inflated screening review page,
after the AI's consistency check). "I assume the actual task is image data and therefore out of scope" Marker `Image`
set by the AI for this reason: the covariates are QuickBird, Landsat and SPOT reflectance and LiDAR height (SEL-13,
remote-sensing spectra).

Forage-lichen cover in 2 x 2 m plots with QuickBird, Landsat and SPOT reflectance, LiDAR height, groundwater depth and
Sphagnum cover as covariates; the objective is to "delineate the geographic distribution and abundance of
terrestrial forage lichens" (Introduction). Results: "Field crews sampled 438 vegetation plots (251 fixed and 187
opportunistic plots)", 98 of them with zero cover. No table is released: the three DOCX appendices hold site
conditions, caribou feeding sites and a Sphagnum model, and the paper has no data statement. So `No` with
`Not Available (from Paper))`, as the workbook's access queue already suspects.

Zero mechanism, from the paper only: no lichen in the plot, but the zero share is set by the design, since
opportunistic plots were taken only "if crews encountered a lichen patch with >10% lichen cover" (Methods). Not the
same study as the post-fire lichen biomass releases (`boreal_postfire_lichen_biomass`).

## Reference

Keim J.L., DeWitt P.D., Fitzpatrick J.J., Jenni N.S. (2017). Estimating plant abundance using inflated beta
distributions: applied learnings from a lichen-caribou ecosystem. Ecology and Evolution 7:486-493.
doi:10.1002/ece3.2625.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 19 (Lichen percent cover).
