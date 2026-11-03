---
unique_name: perovskite_solar_cell_database
name: perovskite_db
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
collections:
- ChemPile
source_links:
- https://doi.org/10.1038/s41560-021-00941-3
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/perovskite_db ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/perovskite_db ; original: http://www.perovskitedatabase.com ; https://huggingface.co/datasets/kjappelbaum/pervoskite_db'
- https://arxiv.org/abs/2505.12534
- https://www.perovskitedatabase.com
- https://nomad-lab.eu/prod/v1/gui/search/perovskite-solar-cells-database
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Duplicate`, PROV-6): ChemPile's `perovskite_db` is a cut of the Perovskite Database Project, which `perovskite_database_solar_cells` records from its own release (NOMAD, Zenodo); the same source and the same task (the device's power conversion efficiency).
- Source: Jacobsson et al., "An open-access database and analysis tool for perovskite solar cells based on the FAIR data principles", Nat Energy 7:107, online 2021-12 (doi 10.1038/s41560-021-00941-3), perovskitedatabase.com and NOMAD. The ChemNLP builder names it: meta.yaml "url: http://www.perovskitedatabase.com, description: original data source", with Jacobsson 2021 as its BibTeX; transform.py loads Hugging Face kjappelbaum/pervoskite_db (created 2023-10-16, the card holds only the licence) and drops every row missing device_stack, pce, ff, jsc, voc, the three formulas or the bandgap, keeping 29,601 devices and 9 columns (targets bandgap, voc, jsc, ff, pce; inputs the formulas and the device stack as one string). The database holds over 42,000 devices with about 400 fields.
- Why a duplicate: the same original source (PROV-4), cut by rows and columns, with no distinct task (PROV-6): PCE, Voc, Jsc and FF are the database's own JV fields, and the full release keeps the process columns this cut drops. The record to keep is `perovskite_database_solar_cells` (screen batch 66); its screening decides the dataset. Note for it: Voc, Jsc and FF determine the PCE, so they are never inputs.
- Siblings and duplicates: `perovskite_database_solar_cells` (the full release, unscreened); the names are near-identical. External collections: ChemPile (ChemPile-LIFT `perovskite_db`), ChemNLP; the awesome-matchem-datasets list (Zotero item 191) names the database.
- Better data: no new search; a candidate of the benchmark ChemPile.
- Reject check (AI, 2026-10-31): stands. The builder names its origin ('url: http://www.perovskitedatabase.com / description: original data source', Jacobsson et al. 2021; https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/perovskite_db) and its transform only drops incomplete rows and columns, so this is a cut of the release `perovskite_database_solar_cells` records from NOMAD and Zenodo. Its extra targets (bandgap, Voc, Jsc, FF) are columns of that same release: a bandgap framing, if wanted, is built from the full release under the canonical record (PROV-8), so nothing is lost. Move the ChemPile tag to the canonical record.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534); the curator's Zotero collection, item 191: "blaiszik/awesome-matchem-datasets".
- as published: 29,601 devices (ChemNLP); the database has over 42,000 cells; in ChemPile-LIFT 207,200 text prompts over 1 config(s); target: power conversion efficiency (pce), open-circuit voltage (voc), short-circuit current (jsc), fill factor (ff), bandgap; access: open.
- Why: Predict the performance of a perovskite solar cell from its composition and device stack | real reported device results with process features
- Adds: | already proposed under this name in 2026-10-30_better_data_scouting (bench_chempile_lift); listed again for the merge
- Notes: The Perovskite Database Project, Jacobsson et al. 2021 (Nat Energy 7:107): every published perovskite solar cell with composition, device stack and measured performance. Features are categorical and string device descriptors plus the formula - a genuinely tabular materials table, measured not simulated, with a clear ...
