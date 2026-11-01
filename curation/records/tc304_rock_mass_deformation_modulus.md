---
unique_name: tc304_rock_mass_deformation_modulus
name: 'ROCKMass/9/5876: multivariate rock-mass database (ISSMGE TC304)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: Other
year: '? (2020)'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- http://140.112.12.21/issmge/Database/RM_9.xlsx
- http://140.112.12.21/issmge/Database/DEF/Def_ROCKMass_9_5876.htm
- https://doi.org/10.1139/cgj-2020-0168
- http://140.112.12.21/issmge/database_20100.htm
- https://www.tc304.org/multivariate_databases.html
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the TC304 rock-mass database (ROCKMass/9/5876, 225 studies), the deformation modulus of a rock mass from classification indices; open after all (the NTU mirror serves the file), with a paper index for grouping, but two other moduli of the same rock mass sit beside the target.
- Source: Ching, Phoon, Ho and Weng, "Quasi-site-specific prediction for deformation modulus of rock mass", Canadian Geotechnical Journal 58:936-951 (2021, doi 10.1139/cgj-2020-0168; the NTU page lists it as "in press" in 2020; abstract via Crossref: "A generic rock mass database consisting of nine parameters is compiled from 225 studies. ... This generic database, labeled as ROCKMass/9/5876, consists of 5876 rock mass cases."). Access correction: the tc304.org file returns 404, but the NTU 304dB page (http://140.112.12.21/issmge/database_20100.htm) links the data as `Database/RM_9.xlsx` (HTTP 200 today, 280,836 bytes), so it is open. NTU definitions: Em "deformation modulus of rock mass", Eem "elastic modulus of rock mass", Edm "dynamic modulus of rock mass". As published (preview of RM_9.xlsx): 6,236 rows x 17 columns: From Paper Index (232 values), Country (67), City/Location, Rock Classification (1,181 blank), Rock Type, Lithology, RQD (1,581 filled), RMR-76 (204), RMR-89 (3,262), Q (1,957), GSI (882), intact Ei (592), Em (3,281), Eem (1,396), Edm (472), intact σci (2,087), and the Em test type (plate loading 1,011, borehole test 983, borehole dilatometer 449, flat jack 323, plate jacking 293, others; 2,945 blank). 2,863 rows hold Em and one index or more, 1,135 two or more. The file has more rows and papers than the paper's 5,876 cases and 225 studies: a later state of the database or other rows (PROV-6 question). TC304 terms forbid "direct profit, e.g., within proprietary software" without the owner's agreement (a term, EV-4).
- Use case: an engineer designing a tunnel, dam or foundation estimates the rock-mass deformation modulus from classification indices (RMR, Q, GSI, RQD) and intact-rock tests, because in situ tests (plate loading, dilatometer) are costly; the paper's task (a transformation model "such as deformation modulus versus rock mass rating" made "more unbiased and more precise for a specific site"); fit direct. Regime grouped by study or site, because a new project is the use case; From Paper Index ships as the group (SPLIT-24).
- Siblings and duplicates: the TC304 family of this run (`tc304_rock_compressive_strength`, the intact-rock database of the same compiler, whose UCS and modulus appear here as inputs; `tc304_clay_compression_index`; `clay_10_7490_global_clay`). Another target, so no duplicate (PROV-7). External collections: none found.
- Better data: found through the dead-link check of the curator's Zotero collection; no further search this round.
- Papers and pages: Ching, Phoon, Ho and Weng 2021 (the data; paywalled, abstract only: four methods compared on two case studies in Turkey, the hierarchical Bayesian model the most effective).
- Metric: none found for a model score (the paper compares transformation models and Bayesian updates, abstract only). So the fallback `rmse`, with Em weighed on a log scale (MET-3). Inputs none.
- Risks for /add-dataset: Eem and Edm are other moduli of the same rock mass, often from the same campaign or test, so they are no inputs for Em (LEAK-10); the Em test type is how the target was measured (known before the test, but check what it encodes); two RMR versions (RMR-76, RMR-89); sparse indices; the file's 6,236 rows and 232 papers against the paper's 5,876 and 225 (PROV-6); rock classification blank on 1,181 rows.
- Priority: gap 0 (environmental science & climate, regression and grouped are covered), use case + (the paper's site-specific Em prediction), source + (journal paper, TC304), shape + (3,281 Em values, 2,863 with an index, 232 paper groups), risk - (moduli measured with the target, counts that differ from the paper).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the dead-link check of the curator's Zotero collection.
- as published: 5,876 rock-mass cases from 225 studies in 67 countries/regions; 9 parameters (RQD, RMR, Q, GSI, Em, Eem, Edm, Ei, sigma_ci); 20% without rock class; target: deformation modulus of the rock mass (Em); access: request (the tc304.org file returns 404 with no Wayback copy; 304dB lists the compiler as contact).
- Why: real measurements with a costly target predicted from cheap indices; a thin domain
- Adds: a rock-mechanics regression beside the first-pass TC304 hits (clay, intact rock UCS). Caveats: compiled from the literature, with many missing values by design.
