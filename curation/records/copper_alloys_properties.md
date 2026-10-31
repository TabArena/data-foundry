---
unique_name: copper_alloys_properties
name: Dataset of mechanical properties and electrical conductivity of copper-based alloys
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Other
year: '2023'
domain: chemistry & material science
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.6084/m9.figshare.c.6475600.v1
- https://doi.org/10.1038/s41597-023-02411-9
- https://arxiv.org/abs/2603.12567
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 1,831 records of copper alloys from about 50 articles (Sci Data 2023, CC0), composition and processing with hardness, yield and tensile strength and electrical conductivity; a documented materials-property table with a DOI per record for a grouped split, multi-target and unequally filled.
- Source: Gorsse, Gouné, Lin and Girard, "Dataset of mechanical properties and electrical conductivity of copper-based alloys", Sci Data 10:504 (online 2023-07-29, doi 10.1038/s41597-023-02411-9, PMC10387069); figshare collection doi 10.6084/m9.figshare.c.6475600.v1 (2023-07-28; three articles holding one file, CC0). As published (`Cu_alloys_database_2023_06_06.csv`, 326 kB, semicolon-separated; header and 5 rows previewed): `Alloy formula`, `Alloy class`, 27 element columns in mass percent (Cu, Al, Ag, B, Be, Ca, Co, Ce, Cr, Fe, Hf, La, Mg, Mn, Mo, Nb, Nd, Ni, P, Pb, Pr, Si, Sn, Ti, V, Zn, Zr), `Tss (K)`, `tss (h)`, `CR reduction (%)`, `Aging`, `Tag (K)`, `tag (h)`, `Secondary thermo-mechanical process`, the targets `Hardness (HV)`, `Yield strength (MPa)`, `Ultimate tensile strength (MPa)`, `Electrical conductivity (%IACS)`, and the source `DOI`. Paper: 1,831 records from about 50 articles on about 150 alloys; fields "not equally populated"; "To extract data from plots, we utilized Plotdigitize"; "Each data point was independently extracted by two members of our team"; the database is updated regularly.
- Use case: an alloy designer looking for more sustainable alternatives to Cu-Be alloys (the paper's stated aim) screens compositions and heat treatments by predicted hardness and conductivity before making samples; the paper says the data "can be helpful as training data for data mining and machine learning applications"; fit direct (the inputs are what the designer sets). Regime grouped by source article (the `DOI` column ships) or by alloy: the rows of one article are mostly an ageing-time series of one alloy (the rows previewed), so a random split leaks.
- Siblings and duplicates: no alloy or metallurgy record (grep by copper, alloy). External collections: none found on the pages read.
- Better data: from the curator's Zotero collection (item 129); no further search this round.
- Papers and pages: Sci Data 2023 (the data); "Accelerating materials discovery using foundation model based In-context active learning" (arXiv 2603.12567, not read).
- Metric: none from the source (no ML baseline); the fallback `rmse` on the chosen property (MET-1, MET-8); inputs none.
- Risks for /add-dataset: pick one target (count each property's rows; hardness is likely the best filled) and keep the other properties out of the features (measured on the same processed sample; LEAK-10, CLEAN-18); about 50 articles give a grouped split with few, uneven groups; values digitised from plots carry reading error; `Alloy formula` restates the element columns; whether a newer release exists than the 2023-06-06 file (PROV-6).
- Priority: gap 0 (chemistry and material science, regression and grouped are covered), use case + (the source's design aim), source + (Sci Data descriptor, CC0), shape + (1,831 records, 35 inputs of mixed types, article groups), risk - (multi-target with unequal filling, few groups).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 129: "Accelerating materials discovery using foundation model based In-context active learning".
- as published: 1,831 records of about 150 Cu alloys (Cu-Be, Cu-Ti, Cu-Ni-Ti, low-alloyed Cu) from articles since 1993; 20 element mass fractions plus thermal and thermomechanical treatment; targets hardness ...; target: Hardness (also yield strength, UTS, electrical conductivity), regression; access: open.
- Why: Curated, CC0, published as a data descriptor for ML; real measurements compiled from the literature
- Adds: A metallurgy property task; no alloy record. Risk: rows of one alloy or article share compositions, so a grouped split by alloy or source article is needed; some values were digitised from plots.
