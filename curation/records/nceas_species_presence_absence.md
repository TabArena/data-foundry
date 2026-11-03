---
unique_name: nceas_species_presence_absence
name: 'disdat: presence-only and presence-absence data for comparing species distribution modelling methods (NCEAS)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- Non-IID (Grouped)
- AI-Filled (Verify)
original_source: Other
year: '2020'
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.17161/bi.v15i2.13384
- https://cran.r-project.org/package=disdat
- https://github.com/rspatial/disdat
- https://arxiv.org/abs/2507.10993
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: the NCEAS species-distribution benchmark (Elith et al. 2020): 226 anonymised species in six regions, with presence-only training records and independent presence-absence surveys (19,120 New Zealand plots for 52 plant species, 14,571 Ontario sites for 20 birds, 10,103 Swiss sites for 30 trees) and 11-13 documented environmental covariates; real absences, but the species and the framing are ours to choose.
- Source: Elith, Graham, Valavi, ..., Zimmermann, "Presence-only and presence-absence data for comparing species distribution modeling methods", Biodiversity Informatics 15(2):69-80 (2020), doi 10.17161/bi.v15i2.13384 (abstract read): "As a benchmark, and to facilitate future comparisons of approaches, here we publish that dataset", grown from a 2006 collaborative comparison; the data on OSF and as the R package `disdat` (CRAN, GPL >= 3; v1.1-0 of 2026-04-13; github.com/rspatial/disdat). As published per region (AWT, CAN, NSW, NZ, SA, SWI): `po` (presence-only training records), `bg` (10,000 random background sites, "not implying absence"), `env` and `pa` (test sites with coordinates, covariates and one presence-absence column per species). From the package docs (man/NZ.Rd, CAN.Rd, SWI.Rd, NSW.Rd, read): NZ 19,120 sites, 52 species, 13 covariates (2 categorical); CAN 14,571 sites, 20 birds, 11 covariates (vegetation class categorical); SWI 10,103 sites, 30 trees, 13 covariates; NSW 570 to 2,075 sites per biological group, 54 species in 8 groups; AWT and SA smaller (not counted).
- Use case: a conservation or land-use agency decides where to survey, protect or expect a species from mapped environmental conditions (written by the curation; the paper's stated purpose is comparing modelling methods); fit approximate; regime grouped (spatial blocks), since nearby sites share conditions; the coordinates ship.
- Siblings and duplicates: no other species-distribution record (grep: disdat, species distribution, presence-absence, Elith); no duplicate. External collections: none in our vocabulary; the paper is the SDM community's own benchmark.
- Better data: from the curator's Zotero collection (item 65, a CNN-plus-tabular habitat paper, arXiv 2507.10993, whose abstract does not name this data); no further search this round.
- Papers and pages: the Biodiversity Informatics paper (abstract only; the full text was not read); the `disdat` documentation (read); the 2006 comparison and later benchmark studies on this data were not read.
- Metric: none found for a supervised presence-absence task (the abstract names none; the vignette and the full text were not read), so the fallback `roc_auc` for one species (MET-8); inputs: a spatial block or site group for the split, from the coordinates.
- Risks for /add-dataset: the original task trains on presence-only records with background points and evaluates on the presence-absence sites (SEL-8): a dataset trained and tested on the presence-absence sites alone is our framing, to argue; the target is one species of the 20 to 54 per region (choose a species with enough presences per fold, one dataset per region; `Multi-target` if several ship together); species are anonymised, labels only, while the covariates are documented, so no `Anonymized` marker; the SWI coordinates carry "a constant shift"; the NSW groups come from separate surveys. Domain left empty: environmental science & climate or biology & life sciences, the curator's call.
- Priority: gap 0 (either domain, binary and grouped are not thin), use case 0 (written by the curation), source + (a data paper and a maintained package), shape + (NZ 19,120 sites, 13 covariates with categoricals, spatial structure), risk - (the framing departs from the presence-only design, and the species is to choose).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 65: "Modeling Habitat Shifts: Integrating Convolutional Neural Networks and Tabular Data for ...".
- as published: survey sites x environmental covariates; 6 regions (AWT, CAN, NSW, NZ, SA, SWI), 226 anonymised species (birds, plants, reptiles, bats); independent presence-absence evaluation sites per region (NZ ...; target: presence or absence of a species at a surveyed site (binary per species; the presence-absence surveys give real absences); access: open.
- Why: real presence-absence survey labels, unlike the paper's generated pseudo-absences; the standard open SDM benchmark, with tabular environmental covariates
- Adds: an ecology / species-distribution task, a domain gap; needs choices on species and a spatial (grouped) split; the presence-only training part uses background points and is better left out
