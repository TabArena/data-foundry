---
unique_name: chempile_reaction_and_generated_tasks
name: ord_predictions, ord_rxn_smiles_procedure, rhea_db_masked, rhea_db_predictions, uspto, odd_one_out, RedDB
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- NLP (Text)
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- AI-Filled (Verify)
collections:
- ChemPile
source_links:
- https://doi.org/10.1021/jacs.1c09820 (ORD); https://doi.org/10.1093/nar/gkab1016 (Rhea); https://doi.org/10.1038/s41597-022-01832-2 (RedDB)
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/<config> (configs: ord_predictions, ord_rxn_smiles_procedure, rhea_db_masked, rhea_db_predictions, uspto, odd_one_out, RedDB) ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/ord_predictions ; original: ORD https://github.com/open-reaction-database/ord-data ; Rhea https://www.rhea-db.org ; USPTO figshare 5104873 ; ZINC via TDC ; RedDB https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/F3QFSQ'
- https://arxiv.org/abs/2505.12534
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`NLP (Text)` and `AHDS (Artifical/Handmade/Deterministic/Simulated)`, SEL-3 with SEL-5 and SEL-16): seven ChemPile-LIFT configs over five sources, each out of scope on its own target.
- Source and the deciding words, from the ChemNLP `meta.yaml` of each config: `ord_predictions` (Open Reaction Database, Kearnes et al. 2021, https://doi.org/10.1021/jacs.1c09820) has the target `product_string`, "reaction products", `type: text` (2,263,057 rows); `ord_rxn_smiles_procedure` has the written procedure; `uspto` (Lowe's patent reactions, figshare 5104873) has `masked_rxn_smiles`, "reaction SMILES with one element masked", `type: text`; `rhea_db_masked` and `rhea_db_predictions` (Rhea, Bansal et al. 2021, https://doi.org/10.1093/nar/gkab1016) have `missing_component`, "masked element", `type: text`; `odd_one_out` is "Tanimoto distance between Morgan fingerprints of SMILES in the ZINC dataset" with the odd molecule as the answer, a label computed from the features themselves (SEL-5, TP-4); `RedDB` (https://doi.org/10.1038/s41597-022-01832-2) is "a computational database that contains 30861 molecules" whose properties come from "molecular property prediction based on quantum chemical calculations" and "aqueous solubility prediction using machine learning" (SEL-16, PROV-3).
- Use case: none of the seven is a decision taken on a tabular prediction: a molecule, a masked component or a paragraph is generated, the odd-one-out is computed, and RedDB's molecules are hypothetical.
- Siblings and duplicates: the reaction records with a numeric target are `ord_reaction_yields` (the ORD yield configs, 28 and 30 rows) and `uspto_reaction_yields`; the measured high-throughput yield records are `buchwald_hartwig_yields`, `suzuki_miyaura_hte_yields`, `amide_coupling_hte_47k`, `cn_coupling_hte_50k` and `pfizer_hte_39k`. The other simulated-label records of this run are `qmof_gcmc`, `qmof_quantum`, `qm8`, `qm9`, `oqmd`, `materials_project_properties`, `mp_formation_energies`, `nomad_structure` and `core_mof_gas_uptake`.
- Better data: a candidate of the benchmark ChemPile; no new search in this run.
- Papers and pages: ORD (Kearnes et al. 2021), Rhea (Bansal et al. 2021), Lowe's USPTO reactions (figshare 5104873), ZINC20 (Irwin et al. 2020) behind `odd_one_out`, RedDB (Sorkun et al. 2022).
- Metric: none; in ChemPile-LIFT every config is scored as text generation (MET-1).
- Risks for /add-dataset: none, nothing to add. For the curator: ORD itself keeps growing as a reaction-condition table with yields and would be worth its own look later, as `ord_reaction_yields` notes; this record is not that.
- Reject check (AI, 2026-10-31): stands. All seven builders read (https://github.com/OpenBioML/chemnlp/blob/main/data/tabular/): the ORD, Rhea and USPTO configs have text targets only (`product_string` 'reaction products', `procedure`, `missing_component` 'masked element', `masked_rxn_smiles`; `ord_predictions` is named `ord_rxn_smiles_yield_pred` but holds no yield), `odd_one_out` targets Tanimoto similarities computed from its own input SMILES, and RedDB is 'a computational database' built by 'chemical library generation' and 'quantum chemical calculations'. The measured yields are in other records (`ord_reaction_yields`, the HTE sets).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: ord_predictions 2,263,057; ord_rxn_smiles_procedure 76,648; rhea_db_masked and rhea_db_predictions 31,348 each; uspto 150,774; odd_one_out 98,715; RedDB 30,861; in ChemPile-LIFT 14,591,854 text ...; target: product SMILES / masked component / procedure text / odd-one-out molecule / computed quantum properties.
- Why: Sequence-to-sequence chemistry tasks: predict the product of a reaction, the missing reagent of a masked reaction, or the written procedure; pick the odd molecule out of four by fingerprint similarity; RedDB computed redox properties
- Notes: Grouped as out of scope for one reason each: the ORD/Rhea/USPTO product and procedure configs have a molecule or a paragraph as the target (generation, not a tabular label); odd_one_out is derived by the ChemNLP authors from Tanimoto distances over ZINC, so the label is computed from the features; RedDB is a ...
