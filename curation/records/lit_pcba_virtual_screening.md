---
unique_name: lit_pcba_virtual_screening
name: 'LIT-PCBA: an unbiased data set for machine learning and virtual screening'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Selection Bias
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: Website
year: '2020'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
source_links:
- https://doi.org/10.1021/acs.jcim.0c00155
- https://drugdesign.unistra.fr/LIT-PCBA/
- https://arxiv.org/abs/2507.21404
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: 15 PubChem target sets of confirmed actives and inactives from dose-response assays, a real virtual-screening task, but built as a benchmark: compounds pruned to matched property ranges, targets kept only where existing methods enriched, and a 2025 audit finds duplicates and analogs across the published splits.
- Source: Tran-Nguyen, Jacquemard and Rognan, "LIT-PCBA: An Unbiased Data Set for Machine Learning and Virtual Screening", J. Chem. Inf. Model. 60(9):4263-4273, 2020 (doi 10.1021/acs.jcim.0c00155; PubMed abstract read): 149 dose-response PubChem bioassays processed to "7844 confirmed active and 407,381 confirmed inactive compounds"; actives and inactives kept in similar property ranges; of 21 targets, the 15 kept were those where 2D fingerprints, 3D shape or docking enriched the top 1% "by at least a factor of 2"; training and validation sets debiased by AVE. The site (https://drugdesign.unistra.fr/LIT-PCBA/) says "15 target sets, 7761 actives and 382674 unique inactives" (`full_data.tgz`, `AVE_unbiased.tgz`); its table, garbled in the fetch, reads for example ADRB2 17 actives, ESR agonists 13, OPRK1 24, PPARG 24, IDH1 39, FEN1 360, PKM2 546, VDR 655, ALDH1 5,363 (about 102,000 inactives).
- Use case: a medicinal chemist ranks a library to choose which compounds to test against a target; fit approximate: the property-matched pruning and the choice of targets make the sets unlike a real library, as for MUV. Regime grouped on the Bemis-Murcko scaffold (SPLIT-31) rather than the published AVE splits.
- Siblings and duplicates: `muv_maximum_unbiased_validation` (AI `TBD -> 2nd Tier`, priority 1, `Selection Bias`: a designed PubChem benchmark), `butkiewicz_pubchem_hts` (AI `TBD -> Yes`, priority 3: raw PubChem HTS campaigns of other assays), `drug_discovery_virtual_screening_dataset` (Lennart `No`, AHDS: generated). The 15 targets are distinct tasks of one source (PROV-7), one record each if kept; the AIDs on the site do not overlap Butkiewicz's. External collections: awesome-chemistry-datasets. The record's Zotero match (item 95, "Sleep Deprivation & Cognitive Performance") looks like a mismatch.
- Better data: found as better data for `drug_discovery_virtual_screening_dataset`; no further search this round.
- Papers and pages: the JCIM paper (abstract); Huang, Knight and Naprienko, "Data Leakage and Redundancy in the LIT-PCBA Benchmark", arXiv 2507.21404 (2025; abstract read): "2D-identical ligands within and across partitions", "323 active training -- validation analog pairs" for ALDH1, 2,491 identical inactives in both training and validation, and "a trivial memorization-based baseline with no learnable parameters" that matches published models.
- Metric: the paper's target filter and the field use the enrichment factor in the top 1% (EF1%), which within one fold ranks models as the precision in the top 1% does (`precision_at_k`, k = 1% of the fold, MET-7), coarse with a handful of actives per fold (MET-10); otherwise the fallback `roc_auc`. The paper's own result metrics were not read. Inputs none.
- Risks for /add-dataset: most sets have under 100 actives (ADRB2 17, ESR agonists 13), so only the larger ones (ALDH1, FEN1, GBA, KAT2A, MAPK1, PKM2, VDR by the site's table) can be scored per fold (TP-5); remove the duplicates the audit found and split by scaffold (LEAK-17, SPLIT-31); SMILES only, the structure as RDKit 2D descriptors as for `apistox`; the property-matched selection (`Selection Bias`, as for MUV).
- Priority: gap 0 (chemistry and binary not thin), use case 0 (a designed benchmark, fit approximate), source + (journal paper and site), shape + (sets of about 60,000 to 350,000 compounds, hundreds of actives in the larger ones), risk - (designed selection, split leakage, few actives in most sets).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `drug_discovery_virtual_screening_dataset`; the awesome-chemistry-datasets list (github.com/kjappelbaum/awesome-chemistry-datasets); the curator's Zotero collection, item 95: "Sleep Deprivation & Cognitive Performance".
- as published: 15 target sets built from PubChem confirmatory dose-response assays: 7,761 actives and 382,674 unique inactives in total; per set from 13-17 actives (ESR agonists, ADRB2) up to 5,363 actives and ...; target: active or inactive on one target in the PubChem assay; access: open.
- Why: real screening outcomes for exactly the task the rejected synthetic record drug_discovery_virtual_screening_dataset imitates; confirmatory dose-response, not single-shot primary screening
- Adds: real labels where the recorded candidate is generated. Risks: extreme imbalance on most sets (ALDH1, FEN1, PKM2 are usable); arXiv 2507.21404 (2025) reports duplicates and leakage across the published splits; the field scores this task by enrichment at the top of the ranking, which needs a metric decision
