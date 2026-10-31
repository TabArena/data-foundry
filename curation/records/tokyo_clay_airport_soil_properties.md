---
unique_name: tokyo_clay_airport_soil_properties
name: GEOAI benchmark BM/AirportSoilProperties/2/2025 (public subset of Tokyo-CLAY/14/67760)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: Other
year: '2025'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Regression
source_links:
- https://doi.org/10.1016/j.geoai.2025.100012
- https://ars.els-cdn.com/content/image/1-s2.0-S3050483X25000115-mmc4.xlsx
- https://ars.els-cdn.com/content/image/1-s2.0-S3050483X25000115-mmc6.xlsx
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the public part of a large site investigation at an offshore airport near Tokyo, released as the GEOAI benchmark with fixed tasks, an RMSE metric and a 2026 special issue; 8,857 complete records over 558 boreholes for undrained strength, but only three index inputs besides location and depth.
- Source: Otake, Ching, Saito and Asano, "GEOAI benchmark problems BM/AirportSoilProperties/2/2025", Geodata and AI 2:100012 (2025, doi 10.1016/j.geoai.2025.100012; the article page refused our fetch, so the benchmark is described here from Saito, Otake and Wu, arXiv 2509.03191, Section 2.1, read through a fetch: a soil investigation "yielded the 'Tokyo-CLAY/14/67760' database", 2,922 boreholes and 67,760 records over 10 km x 10 km at "a large offshore airport underlain by soft clay of the Yurakucho Formation"; six index properties (degree of saturation, unit weight, void ratio, LL, PL, w) and five mechanical ones (su, E50, preconsolidation stress, Cc, Cv)). Public supplementary tables (preview): mmc4 `Local_BID_4_minus_fiveBHs`, 8,857 complete records x 10 (global_id, borehole_id, x, y, z_depth, elevation, LL, PL, w, su) over 558 boreholes; mmc6 `Local_BID_11_minus_Table1`, 2,766 complete records x 13 (borehole_id and the 11 parameters) over 267 boreholes, 2,718 of them also in mmc4; mmc5 (the verification site, 869 records, 46 boreholes), mmc2 (the five benchmark boreholes, 108 records) and mmc3 (`Global_BID_4_minus_fiveBHs`, 1,823 records over 160 sites with LL, PL, w, su and depth; its source was not stated in what we read). About 13% of the 67,760 records are public. Licence CC BY-NC 4.0 per the assessment, not verified (a term, EV-4).
- Use case: the benchmark's: an engineer characterising the site predicts the su depth profile (and the other mechanical parameters) at boreholes from index tests, location and depth, for design; fit direct for su from index properties at a new borehole, approximate against the benchmark's problem 1, which also gives the target borehole's own measured su. Regime grouped by borehole, because a new borehole is the use case and borehole_id ships (SPLIT-24); neighbouring boreholes are correlated through x and y, so a spatial block is the alternative to weigh.
- Siblings and duplicates: `clay_10_7490_global_clay` (the global database the GEOAI papers name as context), `sz_clay_shenzhen` (another site database of the series), `tc304_clay_compression_index` (Cc, global), `tc304_rock_*` (rock). Other sources or targets, so distinct (PROV-7); the curator picks among the clay-strength records. External collections: the GEOAI benchmark itself, with its special issue (Otake and Ching, "Benchmarking data-driven site characterization: Methodological insights from a shared benchmark", Geodata and AI 8:100109, 2026, doi 10.1016/j.geoai.2026.100109).
- Better data: from the curator's Zotero collection (items 149 and 26); no further search this round.
- Papers and pages: Otake et al. 2025 (the benchmark); Saito, Otake and Wu, arXiv 2509.03191 (TabPFN on both problems against a hierarchical Bayesian model, RMSE and calibration); Saito, Otake and Wu, "Applying a tabular foundation model to geotechnical site characterization", Geodata and AI 6:100040 (2026, doi 10.1016/j.geoai.2025.100040); Saito, Otake, Mizutani and Wu, arXiv 2603.21033 (Georisk 2026, imputation of su, Eu, σ'p, Cc and Cv scored by RMSE); Otake and Ching 2026 (the special issue summary). The arXiv and Geodata-and-AI papers were moved here from the links (PROV-12).
- Metric: the benchmark's "Root Mean Squared Error (RMSE) between predicted mean and true values", with "the coverage of 95% prediction intervals" for problem 1 and "RMSE and 95% interval coverage" for problem 2 (arXiv 2509.03191, Sections 2.1 and 2.4, describing the benchmark); a benchmark's declared score, so `rmse` (MET-4); interval coverage needs predictive intervals, which the benchmark asks for but we do not score; whether RMSE is taken on su or on ln su was not read (MET-3). Inputs none.
- Risks for /add-dataset: few inputs for su (LL, PL, w, depth, elevation, x, y; depth and elevation nearly collinear); the 11-parameter table is a second, smaller framing (pick one; the other mechanical parameters are measured with su and are no inputs for it, LEAK-10); local coordinates and spatial correlation (SPLIT-24); only the public 13%.
- Priority: gap 0 (environmental science & climate, regression and grouped are covered), use case + (the benchmark's named task), source + (benchmark paper, organisers, special issue), shape + (8,857 records over 558 boreholes), risk - (few inputs, a public subset only).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 149: "TabPFN Extensions for Interpretable Geotechnical Modelling"; the curator's Zotero collection, item 26: "Tabular foundation model for GEOAI benchmark problems BM/AirportSoilProperties/2/2025".
- as published: Soil test records (a sample at a depth in a borehole) at a 10 km x 10 km offshore-airport landfill near Tokyo. Public supplementary tables (CC BY-NC 4.0): mmc4 Local-BID, 8,857 complete records from ...; target: Undrained shear strength su (regression). Local-BID-11 also allows E50, Pc, Cc and Cv from index properties.; access: open.
- Why: Measured lab data from one large real site investigation, published as a benchmark with fixed tasks and a 2026 special issue of about 14 solutions, and already used with TabPFN. | A published benchmark from one large real site investigation, already used for TabPFN. Same dataset as item 26's ...
- Adds: A new domain (no geotechnical record exists) and a grouped, spatial regime. Correction to pass 1: only about 13% of the records are public (8,857 of 67,760), with only 3 index inputs plus location and depth for su. | A site-specific counterpart to the TC304 global databases. Changed: access confirmed (the ...
