---
unique_name: aqsoldb
name: 'AqSolDB: a curated reference set of aqueous solubility and 2D descriptors'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: Other
year: '2019'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.7910/DVN/OVHAW8
- https://doi.org/10.1038/s41597-019-0151-1
- https://tdcommons.ai/single_pred_tasks/adme/
- http://arxiv.org/abs/2608.18982
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and papers, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: AqSolDB, 9,982 compounds with a measured aqueous solubility (LogS) merged from nine datasets, with reliability groups and 17 published 2D descriptors; the reference solubility set, which TDC scores by MAE on a scaffold split.
- Source: Sorkun, Khetan and Er 2019, "AqSolDB, a curated reference set of aqueous solubility and 2D descriptors for a diverse set of compounds", Sci Data 6:143 (doi 10.1038/s41597-019-0151-1, 2019-08-08); data on Harvard Dataverse (doi 10.7910/DVN/OVHAW8). The abstract: "we generated a new database of compounds, AqSolDB, by merging a total of nine different aqueous solubility datasets, curating the merged data, standardizing and validating the compound representation formats, marking with reliability labels, and providing 2D descriptors of compounds". As published (from the run's note, not re-checked): one table `curated-solubility-dataset.tab` (3.8 MB) with name, InChI, InChIKey, SMILES, LogS (mol/L), SD and count of repeated values, reliability group G1-G5 and 17 RDKit 2D descriptors.
- Use case: the paper names fields, not an actor or decision ("the aqueous solubility of compounds has a key role in various domains, including but not limited to drug discovery, paint, coating, and battery materials design"); the drug-discovery use (a medicinal chemist estimating LogS before a compound is made) is ours to state, as TDC frames it in its ADMET group; fit direct for that screen. Regime grouped on the Bemis-Murcko scaffold (SPLIT-31), as TDC splits.
- Siblings and duplicates: `tdc_aqsoldb` (TabBench-Bio's ECFP4 build of TDC's Solubility_AqSolDB file) is screened `No` (`Duplicate`, PROV-4) with this record as the survivor. Other compilations, not duplicates (PROV-4, another source): `somas_aqueous_solubility` (11,696 neutral organics, shares sources such as eChemPortal and Yalkowsky; the curator picks one of the two); `bigsoldb_2` and `drug_solubility_binary_solvent_mixtures` (other solvents, other tasks, PROV-7). ESOL (Delaney 2004, 1,128 compounds) is one of the nine sources per the run's note, so an ESOL record would be a cut of this one (PROV-6); none exists. External collections: TDC (Solubility_AqSolDB, ADMET benchmark group), TabBench-Bio (as `tdc_aqsoldb`), awesome-chemistry-datasets.
- Better data: from the awesome-chemistry-datasets list and the curator's Zotero collection (items 106, 247, 50, 71); no further search this round.
- Papers and pages: Sorkun et al. 2019 (the data, PMC6687799); TDC's ADME page and ADMET benchmark group; the arXiv paper in source_links (2608.18982) as a user, not read.
- Metric: TDC's ADMET benchmark group scores Solubility_AqSolDB by MAE on a scaffold split with 20% held out ("MAE is used for majority of benchmarks", tdcommons.ai/benchmark/admet_group/overview): the task definer's deliberate choice (MET-1, MET-5), `mae` on LogS; the paper defines no ML metric; inputs none.
- Risks for /add-dataset: SD, the count of measurements and the reliability group describe the label and are no features (they may filter rows, a choice to record); the 17 descriptors are computed from the structure (CLEAN-24); salts, inorganics and stereoisomers that collapse onto one 2D structure (LEAK-17); values merged across temperatures and methods (label noise, not a leak).
- Priority: gap 0 (chemistry & material science and regression are not thin), use case 0 (the paper names fields, not a decision), source +, shape + (9,982 compounds, 17 descriptors), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the awesome-chemistry-datasets list (github.com/kjappelbaum/awesome-chemistry-datasets); the curator's Zotero collection, item 106: "Critical Assessment of ML models for ADMET Prediction in TDC leaderboards"; the curator's Zotero collection, item 247: "Monroe: A Molecular Foundation Model for In-Context Probabilistic Inference"; the curator's Zotero collection, item 50: "An Ensemble Model for Molecular Solubility Prediction Across Aqueous and Organic Solvents"; the curator's Zotero collection, item 71: "ICE-ID: A Novel Historical Census Data Benchmark Comparing NARS against LLMs, \& a ML ...".
- as published: 9,982 unique compounds in one table (curated-solubility-dataset.tab, 3.8 MB): identifiers, SMILES, LogS, SD and count of repeated measurements, reliability group G1-G5, 17 RDKit 2D descriptors; ...; target: experimental aqueous solubility LogS (mol/L) at about 25 C; access: open.
- Why: measured target, the de facto reference set (TDC Solubility_AqSolDB); reliability groups document repeat agreement | The standard curated aqueous solubility set (also TDC Solubility_AqSolDB); real measurements with a direct drug-discovery use. | The standard curated solubility set, documented merge and selection ...
- Adds: supersedes ESOL (item 76, its dataset G); covers salts and inorganics, unlike SOMAS. Reliability group and SD are not features | Covers ESOL (Delaney 2004, 1,128 compounds; one of its nine sources) at nearly 9x the size. Risks: the descriptors are computed from the structure, and the same compounds appear across the ...
