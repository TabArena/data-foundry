---
unique_name: sz_clay_shenzhen
name: SZ-CLAY/10/7965 (Shenzhen clay database)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: Other
year: '2025'
domain: environmental science & climate
problem_type: Regression
original_data_state: One Table
source_links:
- https://data.mendeley.com/datasets/28k4ywgrtf/1
- https://doi.org/10.1016/j.geoai.2025.100027
- '# earlier versions of the same deposit (PROV-6): SZ-CLAY-10-7964 and SZ-CLAY-10-8037'
- https://doi.org/10.17632/y94jyms83b.1
- https://doi.org/10.17632/97rjmn4wh4.1
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages, papers and a preview of the files, NOT from a full inspection of the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: 7,965 clay test records from Shenzhen site investigations (a 2025 Geodata and AI data paper, CC BY 4.0 on Mendeley Data) with depth, index and mechanical parameters in 11 columns; strength (cohesion and friction angle from direct shear) from index properties is the field's transformation-model task, but the file has no project id, and one column is computed from two others.
- Source: Sun, Cao, Pan, Su, Qian and Phoon, "Introduction to SZ-CLAY/10/7965 database", Geodata and AI (2025-09, doi 10.1016/j.geoai.2025.100027; no abstract on Crossref, the publisher page refused access, not read, PROV-17). Data: Mendeley Data "SZ-CLAY-10-7965" (doi 10.17632/28k4ywgrtf.1, 2025-06-16, Guangcan Sun, Central South University, CC BY 4.0), one file `SZ-CLAY-10-7965.xlsx` (484 KB, previewed 2026-10-31): 7,965 rows x 11 columns `Depth` (an interval string such as "5.80-6.00"), `e` (void ratio), `Sr` (degree of saturation), `LL`, `PL`, `α1-2` (coefficient of compressibility), `Es` (compression modulus), `φq`, `cq` (quick direct shear), `φqc`, `cqc` (consolidated quick direct shear); filled: e 7,774, LL 7,893, α1-2 6,017, Es 6,006, cq 4,226, φq 4,236, cqc 1,602, φqc 1,601. The earlier deposit SZ-CLAY-10-8037 (doi 10.17632/97rjmn4wh4.1) says: "SZ-CLAY/10/8037 contains site investigation data from 84 engineering projects in Shenzhen. Each record in the database contains four physical parameters and six mechanical parameters."
- Use case: a geotechnical engineer at a Shenzhen site with index tests (void ratio, Atterberg limits) and few shear tests estimates the design strength parameters, the transformation-model practice behind Phoon's multivariate databases; ours to state for this deposit (the Mendeley page says only "supporting the analysis and prediction of soil behavior"); fit direct for the estimate. Regime grouped by project (84 projects; a new site is the use case), but no project column ships, so IID unless the authors give the grouping (SPLIT-24).
- Siblings and duplicates: SZ-CLAY-10-8037 (2025-04-22) and SZ-CLAY-10-7964 (doi 10.17632/y94jyms83b.1, 2025-04-23) are earlier versions of the same deposit (PROV-6), kept as links here; 7965 matches the data paper. `clay_10_7490_global_clay` (`TBD -> Yes`, 2; TC304's global database, undrained strength), `tc304_clay_compression_index`, `tokyo_clay_airport_soil_properties` (the GEOAI benchmark site), `tc304_rock_compressive_strength`: other sources or parameters (PROV-7); the curator should pick among the clay records. Related Shenzhen databases of the same group (SZ-CLAY/11/5130 from 52 projects; SZ-SOIL/8/11369 from 75 projects) have no record and may share projects. External collections: none found.
- Better data: from the curator's Zotero collection (item 26, the GEOAI benchmark paper); no further search this round.
- Papers and pages: Sun et al. 2025 (the data paper); the three Mendeley deposits; Saito, Otake and Wu 2025 (arXiv 2509.03191, TabPFN on the GEOAI benchmark, a Tokyo airport site, not this one).
- Metric: none found (the data paper was not read; the Mendeley pages name none), so the fallback `rmse` on the chosen strength parameter (MET-1, MET-8); TC304 practice judges transformation models by the bias and spread of measured over predicted values, a question for the add stage as for `clay_10_7490_global_clay`; inputs none.
- Risks for /add-dataset: `Es` equals (1 + e) / α1-2 within 2% in 5,020 of the 5,790 rows that hold all three (the oedometer definition), so never predict one of the three from the other two (SEL-5, LEAK-10); `Sr` exceeds 100% in 19 rows (up to 165), impossible values to set missing (CLEAN); four strength targets with different fill: choose one test type (USE-5); no project or borehole id, so rows of one site can fall on both sides of a random split (SPLIT-24); `Depth` is an interval string to parse.
- Priority: gap 0 (regression and the likely domain are not thin), use case 0 (the deposit names no decision; the data paper was not read), source + (a data paper and a CC BY deposit), shape + (about 4,200 rows with a quick-shear strength and five or six inputs), risk - (no grouping column, a derived column, impossible values).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 26: "Tabular foundation model for GEOAI benchmark problems BM/AirportSoilProperties/2/2025".
- as published: Clay test records: 7,965 records from site investigations of 84 engineering projects in Shenzhen, 10 parameters (4 physical, 6 mechanical: cohesion and friction angle from consolidated quick direct ...; target: A mechanical parameter (cohesion, friction angle) from physical and index properties; access: open.
- Why: Real records from 84 projects with a data paper, open under CC BY 4.0, and part of the same database series as the GEOAI benchmark.
- Adds: A second independent geotechnical source with a natural project grouping. Two earlier deposits, SZ-CLAY-10-8037 (2025-04-22) and SZ-CLAY-10-7964 (2025-04-23), are versions of the same source (PROV-6); 7965 matches the data paper.
