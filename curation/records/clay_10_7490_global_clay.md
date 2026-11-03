---
unique_name: clay_10_7490_global_clay
name: CLAY/10/7490 global clay database (ISSMGE TC304 304dB)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: Other
year: '2014'
domain: environmental science & climate
problem_type: Regression
source_links:
- http://140.112.12.21/issmge/Database/CLAY_10_7490_TC304/CLAY_10_7490_TC304.zip
- http://140.112.12.21/issmge/database_20100.htm
- https://doi.org/10.1139/cgj-2013-0262
- https://www.tc304.org/multivariate_databases.html
- https://www.tc304.org/attachments/database/multivariate/CLAY_10_7490/CLAY_10_7490.zip
- https://arxiv.org/abs/2509.03191
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: the TC304 global clay database (7,490 records from 251 studies, 10 parameters), the data behind the field's transformation models for undrained strength; real laboratory and CPT values compiled from the literature, but only partially multivariate, so the usable rows per target are unknown.
- Source: Ching and Phoon, "Transformations and correlations among some clay parameters — the global database", Canadian Geotechnical Journal 51(6):663-685 (2014, doi 10.1139/cgj-2013-0262); the data on the ISSMGE TC304 page "Multivariate databases" (tc304.org) and the NTU mirror. As published (TC304 page): CLAY/10/7490 with LL, PI, LI, sigma'v/Pa, sigma'p/Pa, su/sigma'v, St, qt1, qtu, Bq; "Partially multivariate | 251 studies | OCR 1~10 | Insensitive to quick clays"; one zip (`CLAY_10_7490.zip`, not opened). Abstract (Crossref summary): compiled from 251 studies in about 30 regions or countries, used to calibrate the bias and transformation uncertainty of existing transformation models; a companion paper builds a 10-dimensional multivariate distribution from it. Terms: "Use of this data requires acknowledgement", and the data "may not be used for direct profit, e.g., within proprietary software" without the owner's agreement (a term to note, not a criterion, EV-4).
- Use case: a geotechnical engineer at a site with index tests (LL, PI, LI) and CPT soundings but few strength tests estimates the undrained shear strength (or the preconsolidation stress) for design, which is what the transformation models calibrated on this database do (the paper's own framing); fit direct for the estimate, with rows from many studies and test standards. Regime grouped by study or site (a new site is the use case); whether the file carries a study id was not checked (SPLIT-24).
- Siblings and duplicates: the TC304 series has other records of this run: `tc304_clay_compression_index` (CLAY-Cc/6/6203, 429 studies, compression index), `tc304_rock_compressive_strength` and `tc304_rock_mass_deformation_modulus` (rock databases); site databases `tokyo_clay_airport_soil_properties` (GEOAI benchmark, Tokyo airport landfill) and `sz_clay_shenzhen` (84 projects); other parameters or sources, distinct tasks (PROV-7), but the curator should pick among the clay-strength records. The TC304 page lists more clay sets (CLAY/6/535, SH-CLAY/11/4051, FI-CLAY/14/856 and others) that may share source studies; none has a record. External collections: the run names this database as the global indirect database of the GEOAI papers; not verified (arXiv 2509.03191's abstract names only a "big indirect database").
- Better data: from the curator's Zotero collection (items 149 and 26); no further search this round.
- Papers and pages: Ching and Phoon 2014 (the data; paywalled, abstract only); the companion multivariate paper (not read); Saito, Otake and Wu 2025, "Tabular foundation model for GEOAI benchmark problems BM/AirportSoilProperties/2/2025" (arXiv 2509.03191: TabPFN with the indirect database as context, RMSE and calibration reported); "TabPFN Extensions for Interpretable Geotechnical Modelling" (Zotero item 149, not read).
- Metric: the source calibrates transformation models by their bias and transformation uncertainty (the mean and spread of the ratio of measured to predicted values, per the abstract; the text was not read, PROV-17); not a standard score and multiplicative, so the add stage should weigh `rmse` on the log scale of the target (MET-3) against the plain fallback `rmse`; the GEOAI paper reports RMSE. Inputs none.
- Risks for /add-dataset: count the rows that hold the target and enough inputs (many blanks); the normalised columns share sigma'v (su/sigma'v, sigma'p/Pa, sigma'v/Pa, qt1, qtu), so check that no target is computable from the inputs (SEL-5, LEAK-10); OCR is sigma'p over sigma'v, both in the table; rows of one study are correlated (grouped split); overlap of source studies with the other TC304 and site records.
- Priority: gap 0 (environmental science, regression and grouped are covered), use case + (the transformation-model practice the source calibrates), source + (journal paper, TC304), shape 0 (7,490 records, but partially multivariate), risk - (blanks and shared normalisers; study id not checked).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 149: "TabPFN Extensions for Interpretable Geotechnical Modelling"; the curator's Zotero collection, item 26: "Tabular foundation model for GEOAI benchmark problems BM/AirportSoilProperties/2/2025".
- as published: Clay records: 7,490 records from 251 studies worldwide, 10 parameters (LL, PI, LI, sigma_v/Pa, sigma_p/Pa, su/sigma_v, St, qt1, qtu, Bq), only partially multivariate (many blanks); zip of 817 KB, ...; target: Normalised undrained shear strength su/sigma'v (or preconsolidation stress); access: open.
- Why: The standard global database behind the field's transformation models, and the Global-BID of item 26. Open download under acknowledgement terms. | The global database behind the field's transformation models and the Global-BID of the GEOAI papers. Same dataset as item 26's clay_10_7490_global_clay (zotero_03).
- Adds: A cross-study clay table. It is older and compiled from the literature, so weaker than Tokyo-CLAY; take it only if the curator wants a global variant. | Undrained strength across 251 studies. Caveats: TC304 profit restriction; each record has only some of the 10 parameters; normalized columns share sigma_v.
