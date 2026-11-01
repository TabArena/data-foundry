---
unique_name: minnesota_well_arsenic
name: Groundwater arsenic data and ASCII grids for predicting elevated arsenic in northwestern and central Minnesota using boosted regression tree methods
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: GOV Website
year: '2019'
domain: environmental science & climate
problem_type: Binary Classification
source_links:
- https://doi.org/10.5066/F77H1HH8
- https://doi.org/10.1029/2018WR023106
- https://www.sciencebase.gov/catalog/item/59a71705e4b0fd9b77cf6bfb
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: a USGS data release of 3,283 Minnesota drinking-water wells with a measured arsenic exceedance and 127 site and well attributes, published with its paper; the run's larger USGS glacial-aquifer release of the same team and target (`glacial_aquifer_well_arsenic_manganese`) may contain these wells.
- Source: Elliott & Christenson, "Groundwater arsenic data and ASCII grids for predicting elevated arsenic in northwestern and central Minnesota using boosted regression tree methods", USGS data release, https://doi.org/10.5066/F77H1HH8 (DataCite: issued 2019, registered 2019-01-28), cited by Erickson, Elliott, Christenson & Krall, "Predicting geogenic arsenic in drinking water wells in glacial aquifers, north-central USA: accounting for depth-dependent features", Water Resour Res 2018 (online 2018-11-30, https://doi.org/10.1029/2018WR023106, CC BY-NC-ND). As published (DataCite description): "The response variable was the presence or absence of arsenic > 10 microgram/L, the U.S. Environmental Protection Agency's maximum contaminant level for arsenic, in 3,283 wells located throughout both study regions (1,363 in the Northwest region and 1,920 in the Central). The original database used to develop the BRT model consisted of 127 predictor variables which included well characteristics, land use, soil properties, aquifer properties, depth to water table, and predicted nitrate. After optimization steps, a final database of 33 predictor variables was used"; the release also holds the prediction grids.
- Use case: the abstract maps the hazard "for depths typical of drinking water supply and with well construction attributes common for domestic wells", finds screen length and the distance to the overlying aquitard influential, and aims to "help identify safer groundwater supply options"; actor a well owner, driller or the state's well programme, moment before a new well is drilled or tested, decision where and how deep to screen it or whom to test first (our reading; the abstract names no actor); fit approximate. Regime: IID by well as in a BRT hold-out (to check in the paper), spatial autocorrelation an open question; the two regions are too few groups.
- Siblings and duplicates: `glacial_aquifer_well_arsenic_manganese` (this run, unscreened here; USGS release https://doi.org/10.5066/P94FCZJ2 with Erickson et al. 2021, 25 states, 1988-2018, 10,001 arsenic samples) has the same team and target over a wider area; whether its wells include these 3,283 is to check before both enter (PROV-4, PROV-6). `water_quality_and_potability` (`No`, generated) is the record this was found next to; `arsenic_male_bladder` and `arsenic_male_lung` hold exposure and cancer outcomes, another task. External collections: none among the records; the web was not searched (search budget used up).
- Better data: found as a related task next to `water_quality_and_potability`; no further search this run. The larger glacial-aquifer release above is the run's own record of the same task.
- Papers and pages: the DataCite record of the release (ScienceBase item 59a71705e4b0fd9b77cf6bfb refuses scripted fetches); Erickson et al. 2018, abstract read through OpenAlex; Wiley refused the full text, so the paper's split, metric and well sources are unread (PROV-17: ask the curator for the PDF if they decide).
- Metric: not established, since the paper's text could not be read; without it, the fallback `roc_auc` (MET-1, MET-8); inputs none.
- Risks for /add-dataset: "predicted nitrate" is another model's output: check what that model was trained on (LEAK-27 only if it saw these wells' outcomes); the 33 final variables come from the authors' optimisation, likely on all wells, so ship from the 127; the wells' sampling years and the origin of the arsenic tests (state new-well testing or USGS sampling) are to read in the release's metadata (SPLIT-7); download through a browser (ScienceBase blocks scripts); the overlap with the glacial-aquifer release.
- Priority: gap 0 (environmental science & climate, binary, IID not thin), use case 0 (the abstract names a purpose, not an actor), source + (a USGS data release with metadata and a peer-reviewed paper), shape + (3,283 wells, 127 mixed predictors), risk - (a larger release of the same task is its own record): 2.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `water_quality_and_potability`.
- as published: 3,283 drinking-water wells (1,363 Northwest, 1,920 Central Minnesota); 127 candidate predictors (well construction such as screen length and depth, land use, soil properties, aquifer properties, ...; target: presence or absence of arsenic above 10 ug/L (the EPA maximum contaminant level) in the well water; access: open.
- Why: no real dataset with the record's features (a sample's physico-chemical measurements and a potability verdict) was found; the real decision 'is this drinking water safe' for private wells is predicting an exceedance before testing, which this USGS release holds with real measurements
- Adds: real wells with lab-measured arsenic and a public-domain federal source, instead of a file whose first upload says 'Synthetically generated'. Caveats: features are site and well attributes, not water chemistry; one contaminant; spatial grouping needed; ScienceBase blocks scripted fetches (a browser download works)
