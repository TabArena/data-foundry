---
unique_name: csisa_lds_rice_yield_india_2018
name: 'CSISA Landscape Diagnostic Survey: rice production practices applied by farmers on their largest plot during 2018 in India'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
original_source: Other
year: '2022'
domain: environmental science & climate
problem_type: Regression
original_data_state: One Table
source_links:
- https://hdl.handle.net/11529/10548656
- https://doi.org/10.1016/j.dib.2022.108625
- https://pmc.ncbi.nlm.nih.gov/articles/PMC9679526/
- https://data.cimmyt.org/dataverse/csisadvn
- https://hdl.handle.net/11529/10548605
- https://hdl.handle.net/11529/10548507
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: a well-documented random survey of 8,355 Indian rice plots with a farmer-reported yield, but the same kind of farm-practice survey as `digital_green_crop_yield_estimate_challenge`, which the curator called "rather a predictive discovery task".
- Source: CIMMYT / CSISA Landscape Diagnostic Survey, CIMMYT Dataverse hdl:11529/10548656 (published 2022-03-31, version 3 of 2022-08-26; "No license or custom terms chosen"), data paper Ajay et al., "Large survey dataset of rice production practices applied by farmers on their largest farm plot during 2018 in India", Data in Brief 45:108625 (2022-09-20). As published: one CSV, 8,355 farmers x 218 columns (header preview), 8 states, 49 districts, kharif 2018, with codebook, variable details and survey guideline; target `L-tonPerHectare` (also `L-quintalPerAcre`), yields "as reported by surveyed farmers" (Sec. 1), no crop cut. Sampling: "Single stage cluster sampling" of 30 villages per district by PPS and seven households per village (Sec. 2).
- Use case: the paper says the data "can then be reused in developing algorithms for yield predictions" (Value of the Data) but names no actor; an extension programme estimating a plot's yield from its management before harvest is ours; fit approximate. Regime grouped by district (a new district) or IID; one season, so no temporal split within this release.
- Siblings and duplicates: `digital_green_crop_yield_estimate_challenge` (`TBD -> 2nd Tier`, Zindi 2023, about 5,000 Bihar farms): its column names (from memory: `NursDetFactor`, `TransDetFactor`, `RcNursEstDate`, `1tdUrea`) follow the LDS codebook (`D-q418_nursDetFactor`, `D-q419_transDetFactor`, `D-q414_rcNursEstDate`, `F-q5216_1tdUrea`), so it likely comes from the same instrument, perhaps another LDS round: trace before deciding (PROV-4, PROV-6). Sibling LDS releases on the same Dataverse: rice 2017 (hdl:11529/10548605), wheat 2018 (hdl:11529/10548507); pooled seasons would allow a temporal split. `cy_bench_subnational_crop_yield` is regional yield, another task (PROV-7). External collections: none found.
- Better data: found as better data for `digital_green_crop_yield_estimate_challenge`; no further search this round.
- Papers and pages: Ajay et al. 2022 (Data in Brief, PMC9679526); the Dataverse codebook and LDS guideline.
- Metric: none found (data paper, Dataverse page); the Zindi sibling scored RMSE on related data, not on this release. Fallback `rmse` (MET-1, MET-8); inputs none.
- Risks for /add-dataset: post-harvest columns go at a pre-harvest prediction point: `L-q601_harvestDate`, `L-q602_harvestMethod`, `L-q603_residueBurnt`, `L-q604_threshing`, `L-q605_totalGrainYieldQUINTAL`, `L-q606_largestPlotYieldQUNITAL`, `L-q607_farmGatePrice`, `collectionDate` (USE-3, LEAK); in-season stress columns (drought, flood, lodging, pest severity) are known only late in the season, so the prediction point decides them (USE-3); a recalled yield is a noisy target (CLEAN); the curator's SEL-3 doubt on the Zindi sibling applies here too (USE-2).
- Priority: gap 0 (environmental science & climate, regression, grouped or IID not thin), use case 0 (no actor named), source + (data paper, codebook, sampling design), shape + (8,355 plots, 218 mixed columns), risk - (post-harvest columns; the curator's "predictive discovery" doubt on the same kind of survey): 2.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `digital_green_crop_yield_estimate_challenge`.
- as published: 8,355 farmers (their largest rice plot) x about 225 variables, 8 states, 49 districts (up to 210 random interviews per district), kharif 2018; sibling releases on the same Dataverse: rice 2017 ...; target: farmer-reported rice grain yield (t/ha) of the plot; access: open (CIMMYT Dataverse; dataset licence not read).
- Why: same target (yield per area of a smallholder rice plot) and the same kind of features (a farm survey of land preparation, crop establishment, seedlings, irrigation, basal and top-dress fertilizer, harvest) in the same region (eastern India); the Zindi variable names (from memory, to verify) look like the LDS ...
- Adds: a first publication with a data paper, a random sampling design and the questionnaire; 8,355 plots in 8 states against about 5,000 rows from a few Bihar districts; more seasons and the wheat survey for a temporal or by-state grouped split. Same leak risk as the Zindi set: harvest and threshing columns are ...
