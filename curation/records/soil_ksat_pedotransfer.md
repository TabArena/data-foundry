---
unique_name: soil_ksat_pedotransfer
name: 'SoilKsatDB: global compilation of soil saturated hydraulic conductivity measurements for geoscience applications'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: Other
year: '2020'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.5194/essd-13-1593-2021
- https://doi.org/10.5281/zenodo.3752721
- https://zenodo.org/records/4541586
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: 13,258 measured saturated hydraulic conductivities (Ksat) at 1,908 sites with texture, bulk density and organic carbon, the inputs of the pedotransfer functions that hydrological and climate models use; an ESSD data paper with a defined target and use, grouped by site.
- Source: Gupta, Hengl, Lehmann, Bonetti and Or, "SoilKsatDB: global database of soil saturated hydraulic conductivity measurements for geoscience applications", Earth System Science Data 13:1593-1612, 2021 (doi 10.5194/essd-13-1593-2021); data on Zenodo (concept doi 10.5281/zenodo.3752721; latest version v0.3, doi 10.5281/zenodo.4541586, publication date 2020-05-23, CC BY 4.0): `sol_ksat.pnts_horizons.csv.gz` (435 KB), the wider `sol_hydro.pnts_horizons` table, `sol_ksat.pnts_metadata_cl_pedo.csv` and a Readme.pdf; not opened. As published (abstract, Sec. 3.1): "13,258 Ksat measurements from 1,908 sites", with soil texture (11,584), bulk density (11,262), organic carbon (9,787), field capacity (7,382) and wilting point (7,411); 9,155 lab and 4,131 field measurements; 8,994 rows with bulk density, texture and organic carbon together; compiled from the literature and from UNSODA, SWIG, HYBRAS and other databases, with redundant records removed (Sec. 2.1).
- Use case: a hydrologist or land-surface modeller, or an engineer designing irrigation, needs Ksat where it was not measured and estimates it from routine soil properties; the paper names hydrological and climate models, rainfall partitioning, irrigation design and flood and landslide prediction (Introduction); fit direct for a pedotransfer function. Regime grouped by site (several layers and methods per site, SPLIT-29); the paper's 80/20 random split (Sec. 2.4) is a claim to check (SPLIT-5); spatial blocks are the alternative.
- Siblings and duplicates: `africa_soil_profiles_database` and `wosis_soil_profiles` (AI `TBD -> 2nd Tier`, priority 3: profile compilations without a defined target, both naming a pedotransfer framing as a candidate), `lucas_topsoil` (AI `TBD -> Yes`, EU topsoil survey), `soil_compaction_proctor_mdd` and the clay records (other targets). No other Ksat record: no duplicate. External collections: none found.
- Better data: found as a related task next to `africa_soil_profiles_database` and `wosis_soil_profiles`; no further search this round.
- Papers and pages: the ESSD paper and its Zenodo record (which "contains more than is described in the paper", Sec. 5).
- Metric: the paper fits a random forest on log10 Ksat and reports bias, RMSE and the concordance correlation coefficient side by side (Sec. 2.4, 3.3), so no single deliberate metric: the fallback `rmse` (MET-5, MET-8), on log10 Ksat, the scale the paper and the field use (MET-3: say so in the definition); inputs none.
- Risks for /add-dataset: the method (lab or field, and the instrument) changes Ksat strongly (the lab model applied to field data reached a CCC of 0.10, Sec. 3.3), so the method ships as a feature and mixing lab and field rows is a choice to state; the authors "advise to use these data with caution" for legacy records whose original authors could not be traced (Sec. 4.3); 1,103 Florida locations hold 6,532 of the 13,258 measurements (Sec. 3.1); texture is missing for 1,674 rows and the SWIG depth was assumed to be 0-20 cm (Sec. 2.3); 13,286 Ksat values against 13,258 rows where a study gave both a field and a lab value.
- Priority: gap 0 (environmental science, regression and grouped are not thin), use case + (the source names the models and designs that need Ksat), source + (an ESSD data paper with open data and code), shape + (13,258 rows, numeric and categorical inputs, site groups); no risk of the kinds that cost a point (leak, joins, an unclear target, better data).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `africa_soil_profiles_database`, `wosis_soil_profiles`.
- as published: 13,258 Ksat measurements from 1,908 sites; texture 11,584, bulk density 11,262, soil organic carbon 9,787, field capacity 7,382, wilting point 7,411; methods, pedologic unit and climate region in a ...; target: saturated hydraulic conductivity (Ksat) of the soil layer; access: open, open (CC BY 4.0).
- Why: the pedotransfer task the AfSP record names as a candidate, here with a defined target and measured inputs in one table; compiled from SWIG, UNSODA, HYBRAS and the literature | a measured, defined target with routine soil inputs: the pedotransfer framing the WoSIS record names as one candidate task, without WoSIS's ...
- Adds: a source-defined target and use case, global coverage, grouped by site; mixed measurement methods are documented per row | a ready task (target and inputs set by the source) where WoSIS defines none; grouped by site; CC BY 4.0
