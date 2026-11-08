---
unique_name: perovskite_database_solar_cells
name: 'The Perovskite Database Project: perovskite solar-cell devices from the literature'
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Lennart
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

**Assessment (AI, 2026-11-08):** size check for the large-datasets review: the task's table is the 41,519 devices with an efficiency (of 42,443) x the 249 fields that describe the device. Only 116 of those fields hold a value other than "Unknown" in at least 1% of the devices, and 63 in at least 5%; the other 161 of the 410 fields are measurements, measurement conditions and references. The call stands at priority 2.
- As published: Zenodo 10.5281/zenodo.5837035, "The Perovskite Database (Archive)" v1.0.1 of 2022-01-11, CC BY 4.0: `perovskitedatabase_data-v1.0.1.zip` (3,317,874 bytes) with `data/Perovskite_database_content_all_data.csv` (84,659,951 bytes), 42,443 rows x 410 columns (counted). The paper (Nat. Energy 7:107, open access): "We collect data from over 42,400 photovoltaic devices with up to 100 parameters per device"; the team went through "every paper found in the Web of Science with the search phrase 'perovskite solar' up to the end of February 2020 (that is, over 15,000 papers)" and "found original experimental device data in close to half of them, that is, around 7,400". Counted: 7,402 distinct DOIs; `Ref_publication_date` from 2009-04-14 to 2021-05-20; 169 rows entered by the authors of the papers, 39 outside the initial dataset. NOMAD (API, 2026-11-08) holds 43,108 `PerovskiteSolarCell` entries in two uploads (42,448 and 660), none uploaded since 2023: 665 entries more than the Zenodo file, and no newer extraction. The 410 columns by prefix: Ref 12, Cell 11, Module 5, Substrate 9, ETL 29, Perovskite 69, HTL 29, Backcontact 29, Add (additional layers) 62, Encapsulation 6, JV 53, Stabilised 8, Stability 44, EQE 4, Outdoor 40.
- The task's table: one row per device with `JV_default_PCE`, 41,519 rows (counted; median 12.73%, max 36.2%), grouped by paper (7,402 DOIs) or ordered by publication date. The inputs are the 249 device fields (cell, module, substrate, ETL, perovskite, HTL, back contact, additional layers, encapsulation): 188 strings (layer stacks, solvents and additives as `|`-separated lists) and 61 numeric. 116 of the 249 hold a value other than "Unknown" in at least 1% of the devices and take more than one value; 63 do at 5%; 52 of the 62 additional-layer fields hold a single value. Four perovskite fields are measured on the film after it is made (`Perovskite_band_gap`, `Perovskite_band_gap_graded`, `Perovskite_band_gap_estimation_basis`, `Perovskite_pl_max`); they are inputs only if the prediction point comes after the film is characterised. The outcomes: of the 53 JV fields, 25 are results (Voc, Jsc, FF, PCE, Vmp, Jmp and the series and shunt resistances of the reverse and forward scans, the four default values with their scan directions, the hysteresis index), 27 describe the measurement (light source and intensity, scan speed and steps, mask, preconditioning, storage before the test, certification) and one links raw data. The 8 stabilised, 44 stability, 4 EQE and 40 outdoor fields are later tests, and the 12 Ref fields are bookkeeping. The 27 measurement fields are known before the measurement and set how the efficiency was measured, not how the cell was made; whether they enter is a choice for /add-dataset.
- Access: open, a 3.3 MB zip, CC BY 4.0, no login; NOMAD's API is open as well.
- Changes the call: the width, with no change to the priority (2: gap 0, use case 0, source +, shape +, risk -). The "about 410 fields" are 249 device fields, of which 63 to 116 carry information, mostly as strings that need parsing into layers and components (CLEAN). The table is wide only in its sparse tail. The record's "more than 16,000 papers" is the website's figure; the paper says over 15,000 papers were read and about 7,400 had device data.
- Not checked: the same device reported in several papers; the 660 NOMAD entries outside the main upload; the field descriptions on perovskitedatabase.com (Resources) for each of the 249 fields, to separate design from measurement field by field.
