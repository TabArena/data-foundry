---
unique_name: tc304_clay_compression_index
name: 'TC304 304dB CLAY-Cc/6/6203: compression index of clays'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: Other
year: '2022'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.tc304.org/multivariate_databases.html
- https://www.tc304.org/attachments/database/multivariate/CLAY_Cc_6_6203/CLAY_Cc_6_6203.xlsx
- http://doi.org/10.1139/cgj-2021-0658
- https://doi.org/10.17632/64mwjbfcpy.1
- http://140.112.12.21/issmge/Database/CLAY_Cc_6_6203/CLAY_Cc_6_6203.xlsx
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the TC304 compression-index database (CLAY-Cc/6/6203, 429 studies), the data behind the field's Cc transformation models; Cc is filled on every record, the four index inputs (LL, PI, w, e) only in part, and a site id ships on most rows.
- Source: Ching, Phoon and Wu, "Data-centric quasi-site-specific prediction for compressibility of clays", Canadian Geotechnical Journal 59(12):2033-2049 (2022, doi 10.1139/cgj-2021-0658; abstract via Crossref: "A generic clay database consisting of six parameters, including compression index (Cc) and unloading–reloading index (Cur), is compiled from 429 studies. This database, labeled as CLAY-Cc/6/6203, contains 6203 records."). The file is on the ISSMGE TC304 page "Multivariate databases" (tc304.org, HTTP 200 today, 468,710 bytes), on the NTU 304dB mirror (same size), and on Mendeley Data under CC BY 4.0 (doi 10.17632/64mwjbfcpy.1, 2024-11-15: "6203 clay records compiled from 429 studies, covering 55 countries/regions in 6 continents"). As published (preview of the xlsx, sheet `CLAY_Cc_6`): 6,402 non-empty rows x 12 columns: Site (a numeric id 1-371, filled on 4,044 rows), Country (58 values), City/Location (505), LL (3,716 filled), PI (3,306), w (3,836), e (3,721), Cc (6,240; 0.008 to 14.5, median 0.51), Cur (2,275), "Remolded clay?" (YES on 910), the Cc test type (incremental-loading or constant-rate-of-strain oedometer, or unknown) and the Cc type (Cc1, Cc3 or unknown). 1,859 rows hold Cc and all four inputs, 3,863 hold Cc and two or more. A second sheet (`bolton data`, 41 rows of E/su against OCR) is unrelated. The row count differs from the name (6,240 with Cc against 6,203). TC304 terms: "this data may not be used for direct profit, e.g., within proprietary software, without explicit agreement between the database owner and the entity" (a term, not a criterion, EV-4; the Mendeley copy is CC BY 4.0).
- Use case: a geotechnical engineer at a site with index tests but few oedometer tests estimates the compression index for a settlement calculation, which is the paper's task ("predicting Cc and Cur for a target site by combining sparse site-specific data with CLAY-Cc/6/6203"); fit direct for the estimate from index properties, approximate against the paper, which also uses the target site's own Cc values. Regime grouped by site, because a new site is the use case and the paper models "inter-site and intra-site variabilities": group on Site, with City/Location for the 2,358 rows without a site id (SPLIT-24).
- Siblings and duplicates: the TC304 family of this run: `clay_10_7490_global_clay` (CLAY/10/7490, 251 studies, undrained strength; `TBD -> Yes`, priority 2), `tc304_rock_compressive_strength`, `tc304_rock_mass_deformation_modulus`; the site databases `tokyo_clay_airport_soil_properties` (its 11-parameter table also has Cc) and `sz_clay_shenzhen`. Another target or other data, so distinct tasks (PROV-7), but the clay databases may share source studies; FI-CLAY/14/856 (TC304, Finnish clays, has Cc) has no record. External collections: none found.
- Better data: from the curator's Zotero collection (item 149); no further search this round.
- Papers and pages: Ching, Phoon and Wu 2022 (the data; paywalled, abstract only, PROV-17); Saito, Otake, Mizutani and Wu, "TabPFN Extensions for Interpretable Geotechnical Modelling" (arXiv 2603.21033, Georisk 2026; it imputes Cc on the GEOAI airport data, not on this database; moved here from the links, PROV-12); Díaz and Spagnoli 2024, Applied Clay Science (a super-learner for Cc from LL, PI, w and e on their own global compilation of over 1,000 points; the same task on other data, abstract only).
- Metric: none found for a model score: the paper judges transformation models by bias and transformation uncertainty and the hierarchical Bayesian model by its posterior (abstract; text not read). So the fallback `rmse`; Cc spans three orders of magnitude, so the add stage should weigh shipping it on a log scale (MET-3). Inputs none.
- Risks for /add-dataset: inputs missing by design (partially multivariate), so decide the minimum inputs per row; remolded (910) and undisturbed clays mixed (a feature or a filter); Cur comes from the same oedometer test as Cc and is no input (LEAK-10); the Cc type (which slope was read) defines the target and may call for a filter; site ids missing on 2,358 rows (SPLIT-24); the row count against the published 6,203 (PROV-6).
- Priority: gap 0 (environmental science & climate, regression and grouped are covered), use case + (the paper's site-specific Cc prediction), source + (journal paper, TC304, Mendeley), shape + (6,240 targets, 3,863 with two or more inputs, about 370 sites), risk - (partial inputs, mixed specimen states, overlap with the other clay records).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 149: "TabPFN Extensions for Interpretable Geotechnical Modelling".
- as published: 6,203 clay specimens x 6 parameters (LL, PI, w, e, Cc, Cur) from 429 studies; 85% undisturbed, 15% reconstituted; partially multivariate; one xlsx 469 KB (HTTP 200 today); target: Compression index Cc (regression); Cur is a second candidate; access: open.
- Why: Real laboratory measurements with a documented compilation; the Cc target of the GEOAI benchmark the paper uses; a domain the benchmark lacks.
- Adds: A public, multi-study soil-mechanics regression. Caveats: the TC304 terms forbid use 'for direct profit, e.g. within proprietary software' without the owner's agreement; rows compiled from many studies.
