---
unique_name: chemtastesdb_taste_class
name: 'ChemTastesDB: curated database of molecular tastants'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Other
year: '2021'
domain: chemistry & material science
problem_type: Multiclass Classification
source_links:
- https://zenodo.org/records/15051366
- https://doi.org/10.1016/j.fochms.2022.100090
- https://michem.unimib.it/download/data/
- https://doi.org/10.5281/zenodo.5747392
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 4,075 tastant molecules with a literature taste class (ChemTastesDB v2.1, CC BY 4.0), a documented multiclass molecule-property task; the labels were merged from many sources by majority vote, and several classes are tiny.
- Source: Rojas, Ballabio, Pacheco Sarmiento, Pacheco Jaramillo, Mendoza and García, "ChemTastesDB: A curated database of molecular tastants", Food Chemistry: Molecular Sciences 4:100090 (online 2022-02-21; PMC8991844); first deposited on Zenodo as v1.0 on 2021-12-01 (concept doi 10.5281/zenodo.5747392), then v1.1 (2022-02-27), v1.2 (2022-05-08), v2.0 (2025-03-03) and v2.1 (2025-03-19, doi 10.5281/zenodo.15051366, which "adds 1,131 newly curated compounds from 52 new bibliographic references"). As published (v2.1 page): 4,075 molecules with name, PubChem CID, CAS, canonical SMILES, taste class and source reference (`ChemTastesDB_database.xlsx`, 367 kB; the references in a second xlsx; HyperChem .hin structures in a .rar); classes sweet 1,313, bitter 1,615, umami 220, sour 49, salty 16, multitaste 179, tasteless 232, non-sweet 304, non-bitter 28, miscellaneous 119. The 2022 paper (Table 1) had 2,944 molecules in nine classes.
- How the labels were made (paper, Sec. 2): "Data was collected on 4580 molecular tastants from several scientific sources" (37 papers and databases, 3 books, 53 chapters); duplicates merged by name, CAS, CID or canonical SMILES (stereoisomers kept apart); a molecule with several reported tastes was "assigned to the most frequent taste class with a majority voting approach", ties going to miscellaneous together with astringent, cooling, pungent and similar sensations.
- Use case: a flavour or sweetener chemist screens candidate molecules in silico before synthesis or a sensory panel; the paper: the database is to "assist in silico studies for the taste prediction of unevaluated and as yet unsynthetized compounds" (abstract) and "provides support for decision-making to rationally design new tastants" (Sec. 3.1); fit approximate (no actor or threshold named; a literature compilation rather than one panel). Regime IID, one row per molecule, as the QSAR records.
- Siblings and duplicates: no taste record (grep by taste, sweet, bitter, ChemTastesDB). External collections: none found on the pages read.
- Better data: from the curator's Zotero collection (item 137); no further search this round. v2.1 is the newest release of the same source (PROV-6): take it rather than v1.
- Papers and pages: the 2022 paper (the database only: t-SNE on MACCS fingerprints, no supervised model); Rojas et al. 2025, "ChemTastesPredictor", Chemometrics and Intelligent Laboratory Systems 261:105380 (doi 10.1016/j.chemolab.2025.105380; QSPR models on this database; not read).
- Metric: none from the data's paper (no supervised model); ChemTastesPredictor 2025 not read, so the fallback `log_loss` for the multiclass task, or `roc_auc` if the add stage takes a binary framing such as sweet against bitter (MET-1, MET-5, MET-8); inputs none.
- Risks for /add-dataset: the class design (USE-5): salty 16, non-bitter 28 and sour 49 molecules are too few per test fold (TP-5, TP-8), "miscellaneous" mixes ties with other sensations, and "non-sweet", "non-bitter" and "tasteless" overlap the basic classes by definition; merge or drop classes, or ship a framing such as sweet / bitter / other, with the reason. Only identifiers and SMILES ship, so the features are computed from the structure (CLEAN-24). Labels come from heterogeneous sources (tasting protocols and concentrations differ); stereoisomers are separate rows with near-identical descriptors.
- Priority: gap + (multiclass is thin), use case 0 (approximate), source + (paper, versioned Zenodo deposit, a reference per molecule), shape + (4,075 molecules, as the QSAR records), risk - (tiny and overlapping classes, majority-vote labels).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 137: "Data".
- as published: molecules, 4,075 rows (name, CID, CAS, SMILES, taste class); target: taste class (sweet, bitter, umami, sour, salty, tasteless, non-sweet, multitaste), multiclass; access: open.
- Why: curated, CC BY, experimental taste annotations, mid-size
- Adds: a food-chemistry classification task; features from RDKit descriptors (CLEAN-24)
