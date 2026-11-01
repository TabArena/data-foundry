---
unique_name: caco2_permeability_merged
name: caco2_wang
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
collections:
- ChemPile
original_source: Other
year: '2022'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.1021/acs.jcim.5b00642
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/caco2_wang ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/caco2_wang ; original: https://tdcommons.ai/single_pred_tasks/adme/#caco-2-cell-effective-permeability-wang-et-al'
- https://arxiv.org/abs/2505.12534
- https://doi.org/10.3390/pharmaceutics14101998
- https://doi.org/10.1039/D0RA08209K
- https://doi.org/10.1021/acs.jcim.0c00568
- '# supplementary data (the modelling and validation tables, XLSX in the zip)'
- https://www.mdpi.com/article/10.3390/pharmaceutics14101998/s1
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: 4,913 molecules with a measured Caco-2 permeability, curated and merged by one group in 2022, the kind of molecular regression `qsar_bioconcentration` and `apistox` already ship.
- Source: Falcon-Cano, Molina, Cabrera-Perez, "Reliable Prediction of Caco-2 Permeability by Supervised Recursive Machine Learning Approaches", Pharmaceutics 14(10):1998, Sep 2022 (https://doi.org/10.3390/pharmaceutics14101998, read on PMC9610902); as published: a modelling set of 4,913 molecules plus a 100-drug external set, merged from Wang et al. 2016 (1,272), Wang and Chen 2020 (1,827) and Wang X. et al. 2020 (4,464), curated to 1,267 / 1,863 / 4,462 and de-duplicated in 2D ("the 2D duplicate analysis yielded 5000 unique molecules", 87 removed for overlap with the external set); one supplementary XLSX with SMILES, the experimental log Papp (values "converted to 10-6 cm/s and log10-transformed"), a computed log Papp and RDKit descriptors.
- Use case: a medicinal chemist triaging compounds before synthesis or before running the assay: the paper offers "a free tool for virtual screening of Caco-2 permeability in large compound libraries" to "identify the most promising compounds with high intestinal permeability during the early stages of drug discovery"; fit approximate (values pooled from many labs and protocols); regime grouped on the Bemis-Murcko scaffold (SPLIT-31: exact structures ship and a new candidate comes from a series not yet measured).
- Siblings and duplicates: no Caco-2 record existed ('caco' matched only `lucas_topsoil`); `pampa_ncats` (PAMPA assay), `human_intestinal_absorption_hou` (the human endpoint, 578 drugs) and `b3db_blood_brain_barrier` are other permeability endpoints, distinct tasks (PROV-7). The TDC cut `Caco2_Wang` (906 of Wang's 1,272 drugs) has no record and is a subset of these rows, so this record should stay the one (PROV-6). External collections: ChemPile-LIFT config `caco2_wang` and the TDC ADMET leaderboard carry the Wang cut.
- Better data: found as better data for the Caco-2 set of ChemPile-LIFT (`caco2_wang`, TDC Caco2_Wang, 906 drugs, Wang et al. 2016), which has no record of its own; this record is that hit, so no further search (the data-scouting run of 2026-10-30/31).
- Papers and pages: the paper above with its KNIME workflow; the merged sources Wang et al. 2016 (https://doi.org/10.1021/acs.jcim.5b00642), Wang and Chen 2020 (https://doi.org/10.1039/D0RA08209K), Wang X. et al. 2020 (https://doi.org/10.1021/acs.jcim.0c00568); the curator's Zotero item 106 (the TDC ADMET audit) named this set as the larger alternative.
- Metric: none found as one deliberate choice: the paper reports r2, RMSE, MAE and the share within 0.5 log units side by side and only remarks that "a measure of dispersion such as the RMSE is a more useful indicator of model accuracy than r2", so the fallback `rmse` on log Papp (MET-5, MET-8); TDC's ADMET leaderboard scores Caco2 by MAE, but on the 906-drug Wang cut, not on this set. Inputs none.
- Risks for /add-dataset: the file ships a computed log Papp next to the experimental one (a model's own prediction: drop it, LEAK-27 if kept) and the authors selected descriptors on the labelled set (LEAK-31); duplicates across the three sources were averaged and agree only to RMSE 0.23-0.52 log units, with "RMSE intraset = 0.49" for set C, so the target carries assay noise (USE-5); SMILES to RDKit descriptors is ours (CLEAN-24) and stereoisomers then become copies (LEAK-16, LEAK-17); the authors' "reliable" (n = 728) against "UNCLEAN" (n = 4,185) division is their claim, not a split (SPLIT-5).
- Priority: gap 0 (chemistry 12 accepted, regression and grouped not thin), use case + (the paper names the screening user), source +, shape + (4,913 molecules with descriptors), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the awesome-chemistry-datasets list (github.com/kjappelbaum/awesome-chemistry-datasets); the benchmark ChemPile (https://arxiv.org/abs/2505.12534); the curator's Zotero collection, item 106: "Critical Assessment of ML models for ADMET Prediction in TDC leaderboards".
- as published: 906 drugs (TDC Caco2_Wang; ChemNLP 910); in ChemPile-LIFT 17,290 text prompts over 1 config(s); target: log effective permeability (cm/s); access: open.
- Why: Predict a drug's permeability through a Caco-2 monolayer, the in-vitro stand-in for intestinal absorption | measured target; about four times the Wang 2016 set behind TDC Caco2_Wang (906 of 1,272); the paper reports how well the sources agree (RMSE 0.23-0.52 log units between duplicate values)
- Adds: | better data for the Caco-2 task the ChemPile-LIFT scouting proposed as caco2_permeability_wang; no permeability task in the benchmark yet. Risks: values pooled from many labs and protocols (intra-source RMSE up to 0.49), SMILES-only features, scaffold grouping needed
- Notes: Wang et al. 2016. Small. Features: SMILES string only, so a container keeps the string and adds computed descriptors, as the apistox record does. No record ('caco' matches only lucas_topsoil).
