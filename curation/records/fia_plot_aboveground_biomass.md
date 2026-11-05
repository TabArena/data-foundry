---
unique_name: fia_plot_aboveground_biomass
name: US FIA forest biomass / USDA Forest Inventory and Analysis (FIADB, DataMart) plot aboveground biomass
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- Needs extensive data wrangling
- No Good Target (yet)
tags:
- Two-Regime Zeros
original_source: GOV Website
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://research.fs.usda.gov/products/dataandtools/fia-datamart
- https://arxiv.org/abs/2503.22103
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (v4 of 2026-10-19, a list of 69 candidates, not in the repository), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 2: the US national forest inventory, where plot biomass
predicted from covariates is an established mapping task (the Forest Service's own biomass maps), but there is no task
table: the target is an allometric sum over the tree tally that must be built, and public plot coordinates are
perturbed.
- Source: USDA Forest Service, Forest Inventory and Analysis DataMart (FIADB): per-state multi-table CSV and SQLite
  downloads (PLOT, COND, TREE, ...), public domain, tens of GB (earlier AI triage, 2026-10-19; not downloaded).
- Use case: mapping aboveground forest biomass where no plot was measured. Blackard et al. 2008 (Remote Sensing of
  Environment 112:1658-1677) built the Forest Service's biomass map of the conterminous US from FIA plots with MODIS,
  NLCD, topography and climate predictors and checked it on held-out plots; White et al. (arXiv:2503.22103v3, Sec.
  2.2) fit unit-level models, but "our primary inferential target is the average biomass density at the county level".
  The actor is the inventory estimating an area, not a decision on one plot, so the fit is approximate. Regime grouped
  (spatial blocks or counties), or temporal across remeasurement cycles.
- Siblings and duplicates: none among the records (searched for FIA, forest inventory, aboveground biomass); `covertype`
  is another Forest Service table with another task. External collections: none found.
- Papers and pages: White et al. 2025 (v3 read: Sec. 2.1, "11,848 and 7,094 FIA plots for Nevada and Washington",
  five auxiliary rasters at 90 m; the earlier note quoted a data-availability line on confidential coordinates that v3
  does not contain, earlier versions not checked); Blackard et al. 2008 (abstract and the USFS raster page only).
- Metric: White et al. score unit-level predictions in 10-fold cross-validation by RMSPE, with bias and coverage (Sec.
  2.8.2): several criteria (MET-5), so the fallback `rmse`, which is their RMSPE on biomass in Mg/ha.
- Risks for /add-dataset: the target and the joins. Plot biomass sums per-tree allometric estimates, so the tree tally
  and the condition fields computed from those trees (forest type, stand size, stand age, stocking) are the label's
  inputs and go (SEL-5). This is not generated data (SEL-16): the plots are a probability sample of real stands, and
  allometric biomass is the field's standard measurement. Without them the plot table holds few features, so
  covariates must come from rasters joined on public coordinates that FIA perturbs (about 805 m, USFS Treesearch 14404)
  and partly swaps on private land; reflectance covariates would raise SEL-13. Which states and which cycle. Open
  question: abundance (here biomass) mapping from covariates.
- Priority: gap 0, use case 0 (approximate), source + (USDA FIA, a documented database), shape + (thousands of plots
  per state, spatial and temporal structure), risk - (target to build, perturbed coordinates, heavy joins).

**Assessment (AI, 2026-10-30):** The family's question on species-abundance mapping is settled without a new rule
(Andrej, 2026-10-30, policy question 1 of the zero-inflated review: "I don't think there is new rule to build here.
These are per dataset judgement calls and if a dataset is useful for a predictive application although the data was
collected for something else, then this is fine"), as SEL-2 already reads the scope rules: this record is judged on its
own use case. The verdict and priority stay.

**Assessment (AI, 2026-10-30):** to the curator's request ("Try to find and download the task table and if you fail
assess how easy we can get it"). No public table gives live aboveground biomass for every FIA plot, nonforest plots
included, with covariates. The closest: the R package saeczi (CRAN 0.2.0, MIT, White et al. 2024) ships `samp`, 1,494
Oregon plots of 2010-2019 with eight covariates (tree canopy cover, elevation, precipitation, temperature, terrain
ruggedness, climatic deficit, a tree/non-tree class) and the target `DRYBIO_AG_TPA_live_ADJ` (50.5% zeros), and `pop`,
the same covariates for 10,060 Oregon plots without the target; Doser et al. 2025 (Zenodo 10.5281/zenodo.16995883) has
forested plots only and per-species targets. Building it is easy and was tested: from the FIADB DataMart CSVs (PLOT,
COND, TREE, PLOTGEOM; public domain) keep annual-design plots (`DESIGNCD` 1, `PLOT_STATUS_CD` 1 or 2), sum `DRYBIO_AG` x
`TPA_UNADJ` over live trees on forest conditions per `PLT_CN` (x 0.0011209 for Mg/ha, 0 where there are none) and keep
the latest visit per location. Rhode Island: 276 plots, 45.7% zeros, positive median 122 Mg/ha; Connecticut: 527, 35.7%,
152; Nevada: 11,888 (White et al. used 11,848), 84.6%, 21. Effort: about 2 hours for a few states (Nevada 72 MB,
Washington 360 MB; nationally the TREE file is 13.7 GB), plus half a day to a day for raster covariates at the public
coordinates; the quickest White-style table is saeczi `pop` with a target built from `OR_TREE` by plot CN (about 2
hours). FIADB itself has few features not derived from the trees (perturbed coordinates, `ELEV`, ecological subsection,
ownership), so the covariates must come from rasters. Risks: condition status, land cover, canopy cover, forest type,
stand age and the other tree-derived condition fields must not be features (SEL-5), and the missingness of slope and
aspect tracks forest status; the public coordinates are fuzzed by up to about 1 km (saeczi's elevation matches a DEM at
the public coordinates, median 2.6 m, but differs from FIADB `ELEV` by a median of 16 m), so every raster covariate is
blurred; canopy cover is a Landsat product (SEL-13, milder than raw reflectance); visits per location must be grouped
and the split spatial.

CC (2026-10-30, Andrej): `No` (the AI screening had `TBD -> 2nd Tier`, priority 2; zero-inflated screening review page,
after the AI's answer to the curator's question). "Seems to risky." The record's markers (`Needs extensive data
wrangling`, `No Good Target (yet)`) stand with the risks of the Assessment above (leaky condition fields, fuzzed
coordinates).

The US national forest inventory: per-state multi-table CSV and SQLite downloads (PLOT, COND, TREE, ...), public
domain, tens of GB in all. No fixed task table exists. The study the workbook most likely means (White et al. 2025)
uses "confidential plot data, which can not be shared publicly" (Data availability) for small-area estimation: "our
primary inferential target is the average biomass per hectare at the county level" (Sec. 2.3), with 90 m raster
covariates. Public plot coordinates are perturbed by about 805 m and some private plots are swapped, so joining
rasters to public plots blurs the covariates. A plot-level target built from DataMart would be an allometric sum over
the measured tree tally, and the condition fields derived from those trees (forest type, stand size, stand age,
stocking) would leak it. Not downloaded.

Zero mechanism, from the paper only: nonforest plots and conditions without live trees, "a mixture of continuous
positive values and true zeroes" (Sec. 1). Workbook pushback: there is no released analytic sample, and the study is
county-level estimation, not row-level prediction. Reopen only if a source releases a plot-level biomass table with
covariates. The FIADB biomass computation was not re-read for this note.

## Reference

USDA Forest Service, Forest Inventory and Analysis DataMart, https://research.fs.usda.gov/products/dataandtools/fia-datamart.
White G.W., Finley A.O., Yamamoto J.K., Green J.L., Frescino T.S., MacFarlane D.W., Andersen H.-E. (2025).
Hierarchical models for small area estimation using zero-inflated forest inventory variables. arXiv:2503.22103.

Lead: the two-regime-zero workbook (v4, 2026-10-19), Master row 3 (US FIA forest biomass).
