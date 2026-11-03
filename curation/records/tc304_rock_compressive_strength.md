---
unique_name: tc304_rock_compressive_strength
name: 'TC304 304dB ROCK/9/4069: intact rock properties (uniaxial compressive strength)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: Other
year: '2018'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.tc304.org/multivariate_databases.html
- https://www.tc304.org/attachments/database/multivariate/ROCK_9_4069/ROCK_9_4069.xlsx
- https://doi.org/10.1139/cgj-2017-0537
- http://140.112.12.21/issmge/Database/ROCK_9_4069_TC304/ROCK_9_4069_TC304.xlsx
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the TC304 intact-rock database (ROCK/9/4069, 184 studies), uniaxial compressive strength from cheap index tests; UCS is filled on 3,226 rows and rock class and type on all, but each index input on only 6% to 46% of the rows, and no study id ships.
- Source: Ching, Li, Phoon and Weng, "Generic transformation models for some intact rock properties", Canadian Geotechnical Journal 55(12):1702-1741 (2018, doi 10.1139/cgj-2017-0537; abstract via Crossref: "A global intact rock database of nine parameters, including uniaxial compressive strength and Young's modulus, is compiled from 184 studies. This database, labeled as "ROCK/9/4069", consists of 27.5% igneous rock, 59.4% sedimentary rock, and 13.1% metamorphic rock."). The file is on tc304.org (HTTP 200 today, 217,713 bytes) and on the NTU 304dB mirror (same size). As published (preview, sheet `database`): 4,069 rows x 16 columns: Country (45), City/Location (409 values, filled on 3,442), Rock Class (every row: sedimentary 2,416, igneous 1,118, metamorphic 535), Rock Type (82), unit weight (1,288 filled), dry unit weight (1,171), water content (231), porosity (1,371), effective porosity (728), Schmidt hammer hardness RL (812), Shore scleroscope hardness Sh (333), Is50 (1,303), P-wave velocity (1,858), Brazilian tensile strength (854), UCS (3,226), Young's modulus E (1,495). 2,902 rows hold UCS and one numeric input or more, 2,481 two or more. Corrections to the assessment: the nine parameters are n, γ, RL (Schmidt hammer), Sh (Shore hardness), σbt, Is50, Vp, σci and Ei (NTU 304dB page and the file header), not Los Angeles abrasion or BPI, and rock class is filled on every row (the "20% without rock class" belongs to ROCKMass/9/5876). TC304 terms forbid "direct profit, e.g., within proprietary software" without the owner's agreement (a term, EV-4).
- Use case: a rock engineer estimates UCS from index tests (point load, Schmidt hammer, P-wave velocity, porosity) where laboratory UCS tests are few, with the transformation models the paper calibrates and selects as generic models for use without site data (abstract); fit direct. Regime grouped by study or site, because rows of one study share a rock and a lab; the file has no study id, only Country and City/Location (missing on 627 rows), so the group has to be built from these (SPLIT-24).
- Siblings and duplicates: the TC304 family of this run (`tc304_clay_compression_index`, `tc304_rock_mass_deformation_modulus`, `clay_10_7490_global_clay`); ROCK/10/4025 (Muzamhindo and Ferentinou 2023, Probabilistic Engineering Mechanics 71:103400, 95 case studies in 23 countries, the same parameters plus mi; file on tc304.org, HTTP 200) has no record and may share source studies with this one. Distinct targets, so no duplicate (PROV-7). External collections: none found.
- Better data: from the curator's Zotero collection (item 149); no further search this round.
- Papers and pages: Ching, Li, Phoon and Weng 2018 (the data; paywalled, abstract only, PROV-17).
- Metric: none found for a model score: the paper ranks transformation models by bias and transformation uncertainty (abstract). So the fallback `rmse`, with UCS weighed on a log scale (MET-3). Inputs none.
- Risks for /add-dataset: sparse inputs (decide the minimum per row); Young's modulus is usually read from the same UCS test, so it is not known before the test and is no input (LEAK-10), and the Brazilian test is a lab test of similar cost (which inputs count as cheap is a use-case call, USE-1); no study id (SPLIT-24); overlap with ROCK/10/4025.
- Priority: gap 0 (environmental science & climate, regression and grouped are covered), use case + (the paper's transformation models from index tests), source + (journal paper, TC304), shape + (3,226 UCS values, 2,481 with two inputs or more, rock class and type on every row), risk - (sparse inputs, the modulus from the same test, no study id).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 149: "TabPFN Extensions for Interpretable Geotechnical Modelling".
- as published: 4,069 intact rock specimens x 9 parameters (porosity, unit weight, LA abrasion, BPI, Brazilian tensile, Is50, Vp, UCS, Young's modulus) from 184 studies; partially multivariate; xlsx 218 KB (the ...; target: Uniaxial compressive strength sigma_ci (or Young's modulus Ei); access: open.
- Why: A classic transformation-model regression with real measurements and a documented compilation.
- Adds: Rock mechanics. Caveats: TC304 profit restriction; missing values across parameters; rock class missing for 20% of rows; ROCK/10/4025 (95 studies) is a sibling.
