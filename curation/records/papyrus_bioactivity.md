---
unique_name: papyrus_bioactivity
name: 'Papyrus: a large-scale curated dataset aimed at bioactivity predictions'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: Other
domain: chemistry & material science
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.1186/s13321-022-00672-x
- https://doi.org/10.4121/16896406.v3
- https://doi.org/10.5281/zenodo.13987985
- https://doi.org/10.5281/zenodo.10944245
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: a curated compound-protein bioactivity collection (59.8 million data points, 1.27 million compounds, 6,926 proteins; the current release on ChEMBL 34) from which per-target potency sets are cut; the QSAR-TID task on newer data, but a collection to split, and its ChEMBL rows overlap the other ChEMBL records.
- Source: Bequignon, Bongers, Jespers, IJzerman, van de Water and van Westen (Leiden University), "Papyrus: a large-scale curated dataset aimed at bioactivity predictions", J. Cheminform. 15:3 (2023, PMC9824924, read through Europe PMC): ChEMBL 30 combined with ExCAPE-DB and smaller high-quality sets, standardised and normalised; 59,775,087 activity values, 1,270,570 unique 2D structures, 6,926 proteins of 499 organisms; 1,238,835 high-quality points (exact values on a single protein or complex subunit). Data on 4TU.ResearchData (doi 10.4121/16896406.v3) and Zenodo; the release "Papyrus 2024" (version 2024.2, files 05.7, 2024-10-24, Zenodo 13987985, CC BY-SA 4.0) moves to ChEMBL 34, adds IUPHAR/BPS and an MMP-12 set and narrows Papyrus++; 16 files, 13.6 GB: activity tables with and without stereochemistry, a Papyrus++ table, precomputed molecular descriptors (ECFP6, Mordred, Mold2, CDDD, E3FP) and protein descriptors.
- Use case: a medicinal chemist ranks candidate compounds by predicted potency on a target before synthesis or assay (ours; the paper aims at "bioactivity predictions" and a benchmark, without an actor); fit approximate (pChEMBL pools assay types and laboratories). Regime: the paper's benchmark uses random and temporal splits ("data points associated with the year 2013 and above constituted the test set") and says the temporal one "better assesses the prediction performance of the models"; the house rule for molecules is a scaffold split (SPLIT-31 as amended); one regime to pick (USE-10).
- Siblings and duplicates: `qsar_tid_11` (`Yes`, shipped) and `qsar_tid_10980` (Lennart `TBD -> Yes`: "Should only include one of these datasets") are MetaQSAR per-target cuts of ChEMBL 17 as FCFP bits; `chembl206_estrogen_receptor` and `chembl2034_glucocorticoid_receptor` (AI `TBD -> 2nd Tier`, TabBench-Bio cuts of ChEMBL 37) and `chembl36_kinase_bioactivity` (AI `TBD -> Yes`) are other cuts of ChEMBL; `drug_discovery_virtual_screening_dataset` is a generated table. Papyrus shares ChEMBL as the underlying source with all of them: per-target sets are versions or cuts (PROV-6), and the curator decides which target enters once, not a duplicate by itself. External collections: none of our vocabulary.
- Better data: found as better data for `drug_discovery_virtual_screening_dataset`, `qsar_tid_10980` and `qsar_tid_11` (and in the curator's Zotero collection, item 87); no further search this round.
- Papers and pages: the paper and the data DOIs above.
- Metric: the paper reports MCC for classifiers and Pearson r and RMSE for regressors side by side, with no single criterion, so the fallback `rmse` for a pChEMBL regression (MET-5, MET-8); inputs none.
- Risks for /add-dataset: choose the targets (one record or a few, after the curator's note on QSAR-TID), the quality level and the stereochemistry variant; the year the temporal split needs is used by the paper, to confirm as a column in the README; a target already shipped through another ChEMBL cut must not ship twice (PROV-6); 13.6 GB of compressed files to cut down.
- Priority: gap 0 (chemistry, regression not thin), use case 0 (ours), source + (paper, versioned releases with a README), shape + (thousands of compounds for well-covered targets, a year for a temporal split), risk - (a collection to cut, overlap with the ChEMBL records).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `drug_discovery_virtual_screening_dataset`, `qsar_tid_10980`, `qsar_tid_11`; the awesome-chemistry-datasets list (github.com/kjappelbaum/awesome-chemistry-datasets); the curator's Zotero collection, item 87: "JLZml/Credit-Scoring-Data-Sets".
- as published: about 1.2M compounds and about 6,900 protein targets, standardised pChEMBL values per compound-target pair, with precomputed descriptors and a high-quality subset; target: bioactivity (pChEMBL) of a compound on one protein target, the quantity of the QSAR-TID records; access: open.
- Why: already found by the 2026-10-30 better-data scouting (scout_41, scout_51) and still without a record; the awesome-chemistry list points at the same source, so the merge should keep one candidate | same task as qsar_tid_10980 and qsar_tid_11: potency of compounds on one drug target from molecular fingerprints; the ...
- Adds: see scout_41: ChEMBL 34 instead of ChEMBL 17, with structures and quality flags | per-target sets from ChEMBL 34 (2024) instead of 17, plus other sources, with standardised structures, quality flags and the SMILES (the MetaQSAR files have only 1024-bit FCFP fingerprints); more compounds per target and the choice of ...
