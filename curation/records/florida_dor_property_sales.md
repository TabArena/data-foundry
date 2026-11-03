---
unique_name: florida_dor_property_sales
name: 'Florida Department of Revenue property tax data files: NAL (Name-Address-Legal assessment roll) and SDF (Sale Data File), per county and year'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
original_source: GOV Website
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://floridarevenue.com/property/Pages/DataPortal_RequestAssessmentRollGISData.aspx
- https://floridarevenue.com/property/dataportal/Documents/PTO%20Data%20Portal/User%20Guides/2026%20Users%20guide%20and%20quick%20reference/2026_NAL_SDF_NAP_Users_Guide.pdf
- https://www.geoplan.ufl.edu/agol/archived_content/Parcels/2015_NAL_SDF_NAP_Users_Guide.pdf
- https://www.geoplan.ufl.edu/agol/archived_content/Parcels/2010_NAL_SDF_NAP_UserGuide_091510.pdf
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: the Florida Department of Revenue's statewide parcel rolls (NAL) and sale files (SDF), the likely upstream of `miami_housing` (whose columns are NAL field names), with every county and many years for a temporal split; a newer, wider release of the same source, so the curator picks it or `miami_housing`, and the build from agency files is ours.
- Source: Florida Department of Revenue, Property Tax Oversight, Data Portal (floridarevenue.com), from the 67 county property appraisers' rolls; "2026 NAL, SDF and NAP User's Guide" (47 pages, read): comma-delimited files with field names in the header row; preliminary rolls on 1 July, initial final rolls in October, final rolls after certification; "The SDF includes only parcels that transferred ownership during the year immediately preceding the January 1 assessment date and the sales that occurred after the January 1 assessment date up to the required submission date"; qualification codes mark arm's-length sales ("01 Transfers qualified as arm's length because of examination of the deed ...") against disqualified ones. NAL fields include JV (just value, "the property appraiser's opinion of market value"), LND_SQFOOT, IMP_QUAL, CONST_CLASS, EFF_YR_BLT, ACT_YR_BLT, TOT_LVG_AREA, NO_BULDNG, NO_RES_UNTS, SPEC_FEAT_VAL and two sales (SALE_PRC1, SALE_YR1, SALE_MO1, QUAL_CD1, ...). Only the current rolls are online; older years by request (NAL from 2002, sale files from 2009, GIS from 2005; portal page). No row counts were read.
- Use case: as `miami_housing`: an appraiser, lender or buyer values a single-family home at the sale from its characteristics and location (mass appraisal); the DOR uses qualified sales for its sales-ratio studies of assessment levels, not as a prediction. Fit direct once the features come from the roll before the sale. Regime temporal by sale year and month (SPLIT-6), where `miami_housing` splits one year at random.
- Siblings and duplicates: `miami_housing` (Yes, shipped: 13,932 Miami-Dade sales of 2016, OpenML 43093 by Bourassa; LND_SQFOOT, TOT_LVG_AREA, SPEC_FEAT_VAL and SALE_PRC are NAL/SDF names, confirmed in the guide); `miami_housing_dataset` (No); `cook_county_residential_sales` and `king_county_home_sales_1999_2025` (assessor data of this run). A newer release of the same source as `miami_housing` (PROV-6): the curator decides which one enters. External collections: none found.
- Better data: found as better data for `miami_housing`; no further search this round.
- Papers and pages: the user guides (2026; archived 2010 and 2015 at geoplan.ufl.edu); Mayer, Bourassa, Hoesli, Scognamiglio 2021 (SSRN 3924412) for `miami_housing`. arXiv 2607.02791 (Cheng 2026, Florida condominium prices around the Surfside collapse, "statewide administrative transaction data" 2020-2024, source not named) is related work, moved here from `source_links` (PROV-12).
- Metric: none found (the DOR publishes rolls, no task; the guide checked), so as `miami_housing`: `rmsle` on the price from the context, the target shipped as log (MET-3, MET-11); inputs none.
- Risks for /add-dataset: JV and the land and building values of a roll whose 1 January date follows the sale may use that sale as evidence (LEAK-10): take attributes and values from the roll before the sale; join SDF sales to NAL parcels by parcel id and roll year; keep qualified single-family sales (QUAL_CD, the DOR use code) (USE-5); back years only by request; the distance and noise features of `miami_housing` would have to be rebuilt from parcel GIS or left out; repeat sales of one parcel across windows (LEAK-17).
- Priority: gap 0 (business & marketing, regression and temporal well covered), use case 0 (the curation's, as on `miami_housing`), source + (the DOR's documented rolls), shape + (statewide sales over many years, mixed features), risk - (as-of-roll joins and requested back years; a version of a shipped dataset).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `miami_housing`.
- as published: one NAL row per real-property parcel for each of Florida's 67 counties (Miami-Dade is one county file), and an SDF listing every recorded sale of the preceding year and the current year up to about ...; target: sale price of a parcel (SDF / NAL sale fields), restricted to qualified arm's-length single-family sales as in the old record; access: open (DOR Property Tax Data Portal downloads; older rolls by public-records request, form PT-105).
- Why: miami_housing (13,932 Miami-Dade single-family sales of 2016) is 'publicly available information' plus distances that Bourassa added (OpenML 43093 description). Its column names LND_SQFOOT, TOT_LVG_AREA, SPEC_FEAT_VAL and SALE_PRC look like NAL/SDF field names (not checked against the guide), so the DOR files appear ...
- Adds: Many years instead of one (2016 only), so a temporal split by sale date; all of Miami-Dade's sales instead of a 13,932-row extract, and the other 66 counties if wanted; recent years (to 2026). The distance and noise features (ocean, CBD, highway, rail, aviation noise) are not in the files and would have to be rebuilt ...
- A newer release of the same source as the record(s) named above (PROV-6): the curator decides which one enters.
