---
unique_name: pump_it_up_tanzania_water_points
name: 'Pump it Up: Data Mining the Water Table (Tanzania water points)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
original_source: Other
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://www.drivendata.org/competitions/7/pump-it-up-data-mining-the-water-table/
- https://www.drivendata.org/competitions/7/pump-it-up-data-mining-the-water-table/page/25/
- https://data.waterpointdata.org/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: DrivenData's long-running competition on the Tanzanian water-point register (59,400 labelled points, 39 mixed features, three status classes) with a stated maintenance use; quantity and water quality are read at the same visit as the status, and many columns are near copies.
- Source: DrivenData competition 7, "Pump it Up: Data Mining the Water Table" (https://www.drivendata.org/competitions/7/pump-it-up-data-mining-the-water-table/): "Using data from Taarifa and the Tanzanian Ministry of Water"; the About page: the data "comes from the Taarifa waterpoints dashboard, which aggregates data from the Tanzania Ministry of Water". As published (problem description, read): 39 features with one-line definitions (amount_tsh, date_recorded, funder, gps_height, installer, coordinates, wpt_name, num_private, basin, subvillage, region and its code, district code, lga, ward, population, public_meeting, recorded_by, scheme management and name, permit, construction_year, extraction type in three granularities, management, payment, water quality, quantity, source and waterpoint type in two or three); target status_group: functional, functional needs repair, non functional; 59,400 labelled and 14,850 test points per the run's Assessment (not on the pages read).
- Use case: "A smart understanding of which waterpoints will fail can improve maintenance operations and ensure that clean, potable water is available to communities across Tanzania" (competition summary): the water authority sends repair crews to the points likely broken or in need of repair; fit direct for triage between visits, approximate where the status was read at the same visit as the features; regime temporal by date_recorded (mostly 2011-2013 per the Assessment) or grouped by ward or LGA (SPLIT-3, to decide).
- Siblings and duplicates: none (grep: pump it up, waterpoint, DrivenData competition 7); the Water Point Data Exchange (https://data.waterpointdata.org/, 838k points reported to 2025 per the run's Assessment) is a larger relative from another source (PROV-4), not searched this round. External collections: none in our vocabulary.
- Better data: no new search; found through the gap scout for multiclass tasks (the Assessment names WPdx).
- Papers and pages: the DrivenData summary, problem description and About pages (read); the Taarifa dashboard.
- Metric: the leaderboard's classification rate (accuracy), from memory of the competition: the pages read do not show it (the rules say it "will be displayed on the Competition Website" and the leaderboard did not render), so to verify; a competition's metric on hard labels is kept (MET-4). Inputs: none.
- Risks for /add-dataset: quantity ("dry") and water quality are observed at the visit that records the status, a near-label for non functional (LEAK: drop, or keep with a note on the prediction point); near-identical column groups (extraction_type*, payment*, quantity*, source*, waterpoint_type*, region and region_code) to reduce (CLEAN); construction_year and gps_height of 0 as missing; high-cardinality funder, installer, wpt_name, subvillage and scheme_name; the test labels are not public, so only the 59,400 labelled rows ship.
- Priority: gap + (multiclass is thin), use case + (the competition names the maintenance decision), source + (a competition with a feature dictionary over a ministry's register), shape + (59,400 points, mixed types, dates and regions), risk - (same-visit quantity and quality columns).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the gap scout for multiclass tasks.
- as published: 59,400 labelled water points x 39 features plus 14,850 unlabelled test points; date_recorded mostly 2011-2013, construction years from 1960; funder, installer, gps height, lat/lon, basin, region, ...; target: status_group: functional, functional needs repair, non functional; access: registration.
- Why: A real government register with a three-class status and a stated maintenance use case; known risks: redundant column pairs, and quantity/water quality are read at the same visit as the status (drop or justify). The WPdx global water-point exchange (838k points, report dates to 2025) is a larger relative, but its ...
- Adds: Multiclass with many high-cardinality categoricals, a temporal (recording date) and spatial grouping (region, LGA, ward); infrastructure maintenance in a low-income country
