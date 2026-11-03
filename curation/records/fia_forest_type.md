---
unique_name: fia_forest_type
name: 'Forest Inventory and Analysis Database (FIADB), US Forest Service: plot and condition tables'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: environmental science & climate
problem_type: Multiclass Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://research.fs.usda.gov/products/dataandtools/fia-datamart
- https://research.fs.usda.gov/understory/forest-inventory-and-analysis-database-user-guide-nfi
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the USDA Forest Service's national plot inventory records the forest type of every forested condition, with site features of the `covertype` kind, across all US forest land; the feature set needs care, since most condition fields describe the trees that define the type.
- Source: USDA Forest Service, Forest Inventory and Analysis Database (FIADB), served by the FIA DataMart (CSV per state and nationwide, SQLite); user guide v9.4 (published 2025-08-25, "Last updated May 28, 2026"). The national grid has one plot "in each theoretical hexagonal polygon, which is approximately 6,000 acres in size" (user guide). As published: the COND table, one row per condition and inventory (ENTIRE_COND.csv 796 MB, last modified 2026-10-30; header read through a range request: CN, PLT_CN, INVYR, STATECD, ..., FORTYPCD, FLDTYPCD, STDAGE, STDSZCD, SITECLCD, SICOND, SISP, SLOPE, ASPECT, PHYSCLCD, ..., about 150 columns), joined to PLOT (elevation, fuzzed coordinates, ecological subsection) on PLT_CN. Rows not counted.
- Target: FORTYPCD, "primarily derived using a computer algorithm" from the tallied trees, or FLDTYPCD, "assigned by the field crew, based on the tree species or species groups forming a plurality of all live stocking" (user guide 2.5.15, 2.5.16); the codes of appendix D, also as forest-type groups.
- Use case: a land manager or a mapping programme predicting the forest type of a location without an inventory plot, from map-derived site features (elevation, slope, aspect, physiographic class, ecoregion), as for `covertype`; written by us, fit approximate (forest-type maps also use satellite imagery). Regime grouped by plot (plots are remeasured on a 5- to 10-year cycle) or temporal by inventory year; to decide (SPLIT-3, USE-10).
- Siblings and duplicates: `covertype` (`Yes`, DF: Yes, BeyondArena, `Outdated`; 581,012 cells of four wilderness areas in one Colorado forest, cover types from 1998 maps): another source, so its own record (PROV-4). No other FIA record. External collections: none found.
- Better data: found as better data for `covertype`; no further search this round.
- Papers and pages: the FIADB user guide and the DataMart (links above), the national field guide; papers not searched (the session's web search budget ran out).
- Metric: none found (FIADB is an inventory database, no task), so the fallback `log_loss` (MET-1, MET-8); inputs none.
- Risks for /add-dataset: most COND fields describe the trees that set the type (stand age, size class, live basal area, stocking, site-index species SISP, carbon pools, the NVCS vegetation classes, FORTYPCDCALC, the regional dominant-species columns): keep only site features (LEAK, SEL-5); public coordinates are fuzzed within 1 mile and some private plots swapped within their county (user guide), so location is noisy; nonstocked conditions (code 999) and periodic against annual inventories; the PLOT join; types or type groups (a long tail of rare types).
- Priority: gap + (multiclass thin), use case 0 (written by us), source + (FIADB user guide), shape + (national, grouped and temporal), risk - (tree-derived fields to exclude, joins).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `covertype`.
- as published: national grid of permanent field plots, about one plot per 6,000 acres, each state measuring a share of its plots every year on a 5- to 10-year rotation; one row per forested condition of a plot ...; target: forest type or forest-type group of the condition as recorded by field crews (FORTYPCD in the COND table; column names to check in the user guide); access: open.
- Why: same target (forest cover type from field data) and the same kind of site features known from maps (elevation, slope, aspect, a moisture/physiographic class, ecoregion), not column for column (no hydrology distances or soil-type indicators)
- Adds: all US forest land instead of four wilderness areas of one national forest in Colorado; field-recorded types over two decades instead of 1998 cover maps; remeasured plots give a grouped (by plot) or temporal split. Caveats: multi-table extract and a careful choice of features (stand age, size class and site class ...
