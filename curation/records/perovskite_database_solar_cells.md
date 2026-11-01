---
unique_name: perovskite_database_solar_cells
name: 'The Perovskite Database Project: perovskite solar-cell devices from the literature'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Many features
collections:
- ChemPile
original_source: Website
domain: chemistry & material science
problem_type: Regression
original_data_state: One Table
source_links:
- https://nomad-lab.eu/prod/v1/gui/search/perovskite-solar-cells-database
- https://doi.org/10.1038/s41560-021-00941-3
- https://doi.org/10.5281/zenodo.5837035
- https://www.perovskitedatabase.com/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: the Perovskite Database, about 42,000 perovskite solar cells extracted by hand from more than 16,000 papers up to February 2020, each with its composition, device stack, processing and measured efficiency; a large real materials table with a data paper, with leak columns and publication bias to handle.
- Source: Jacobsson et al. (94 authors), "An open-access database and analysis tool for perovskite solar cells based on the FAIR data principles", Nat. Energy 7:107 (online 2021-12, doi 10.1038/s41560-021-00941-3); perovskitedatabase.com (the initial phase covered "over 16,000 perovskite papers published through February 2020", data extracted manually; later entries uploaded by authors; hosted by MaterialsZone 2020-2026, now on NOMAD); a CSV snapshot on Zenodo ("The Perovskite Database (Archive)", v1.0.1, 2022-01-11, CC BY 4.0, doi 10.5281/zenodo.5837035, a 3.3 MB zip of GitHub Jesperkemist/perovskitedatabase_data). As published, per the run's notes and the ChemPile screening (not counted here): about 42,000 to 43,400 devices x about 410 fields (cell stack, perovskite composition and deposition, each layer's processing, JV metrics, stability, EQE).
- Use case: a researcher or process engineer chooses the composition, stack and deposition route of a perovskite cell before making it, predicting its power conversion efficiency; fit approximate (literature data; the source names no decision). Regime grouped by paper, since the devices of one paper share a lab and a recipe (SPLIT-29), or temporal by publication date; the curator picks one.
- Siblings and duplicates: `perovskite_solar_cell_database` (`No`, `Duplicate`, PROV-6: the ChemPile/ChemNLP cut of 29,601 devices and 9 columns) names this record as the one to keep, and its reject check asked to move the ChemPile tag here (added). `experimental_band_gap_zhuo` (`TBD -> Yes`) and `pasion_horizontal_pv_power_12_sites` (`TBD -> Yes`) are other materials and PV tasks. External collections: ChemPile (`perovskite_db`), ChemNLP; the awesome-matchem-datasets list.
- Better data: from the curator's Zotero collection, item 99 (and item 191); no new search this run.
- Papers and pages: the Nat. Energy paper (not read here), perovskitedatabase.com, the Zenodo record.
- Metric: none found (the project page and the Zenodo record; the paper presents the database and its analysis tool), so the fallback `rmse` on the efficiency (MET-1, MET-8); inputs none.
- Risks for /add-dataset: Voc, Jsc and FF determine the efficiency, and every post-fabrication measurement (the JV metrics, stability, EQE) goes (LEAK-10); publication bias toward high efficiencies (`Selection Bias` to weigh); about 410 fields with heavy missingness and layer descriptions as strings; the same device reported in several papers; which snapshot to build from (Zenodo 2022 or the current NOMAD export).
- Priority: gap 0 (chemistry & material science and regression are not thin), use case 0 (approximate, no decision named), source + (Nat. Energy data paper, CC BY, maintained on NOMAD), shape + (about 42,000 devices, mixed categorical and numeric), risk - (leak columns among about 410 fields, publication bias).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 99: "blaiszik/awesome-matchem-datasets".
- as published: About 43,000 devices x about 410 fields, extracted by hand from more than 16,000 papers published up to February 2020: 43,398 x 410 per the awesome list, 43,108 public NOMAD entries per the first ...; target: Power conversion efficiency of the device (JV default PCE, regression). Alternative: stability (e.g. T80), with many missing values.; access: open.
- Why: Real measured devices with a peer-reviewed data paper, open under CC BY 4.0 and maintained on NOMAD. It is a wide table of mixed categorical and numeric columns.
- Adds: A photovoltaics and materials-processing domain; no record covers solar cells. Caveats: Voc, Jsc and FF determine PCE, so they and all other post-fabrication measurements must be dropped; publication bias (Selection Bias); heavy missingness and free-text fields. zotero_27 (item 191) names it ...
