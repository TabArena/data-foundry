---
unique_name: ld50_zhu
name: ld50_zhu
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
collections:
- ChemPile
original_source: Other
year: '2009'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.1021/tx900189p
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/ld50_zhu ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/ld50_zhu ; original: https://tdcommons.ai/single_pred_tasks/tox/#acute-toxicity-ld50'
- https://arxiv.org/abs/2505.12534
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: 7,385 rat oral LD50 values with a benchmark metric and split, but the shipped `qsar_oral_toxicity` already covers the endpoint on a larger, newer compilation, and `tdc_ld50_zhu` is a second record of this same file.
- Source: Zhu, Martin, Ye, Sedykh, Young, Tropsha, "Quantitative structure-activity relationship modeling of rat acute toxicity by oral exposure", Chem Res Toxicol 22(12):1913 (2009), doi 10.1021/tx900189p; TDC serves it as LD50_Zhu, "**Dataset Statistics:** 7,385 drugs", regression from SMILES ("Acute toxicity LD50 measures the most conservative dose that can lead to lethal adverse effects", tdcommons.ai/single_pred_tasks/tox). As published: one table, SMILES and the LD50 on the -log(mol/kg) scale.
- Use case: a toxicologist or regulator assigning an acute-toxicity hazard category to a chemical that was never tested in an animal study, so that a test is avoided or prioritised; fit approximate, the same gap the shipped `qsar_oral_toxicity` records (random test chemicals sit much closer to the training set than the untested chemicals a screener faces); regime grouped on the Bemis-Murcko scaffold (SPLIT-31 as amended; `qsar_oral_toxicity` was re-split that way on 2026-10-26, and TDC uses a scaffold split).
- Siblings and duplicates: `tdc_ld50_zhu` (a record of the same run, from TabBench-Bio) is the same TDC dataset served as 7,341 x 2,048 ECFP4 fingerprints - the same underlying file, so the two records are versions of one dataset and one of them should carry `Duplicate` (PROV-6); the SMILES route here is the richer one. `qsar_oral_toxicity` (shipped, `Yes`, 11,105 chemicals) is the same endpoint from the ICCVAM/CATMoS project with a binary "very toxic" label: a distinct framing (PROV-7) on a larger, newer compilation that very likely contains many of these compounds. External collections: ChemPile-LIFT configs `ld50_zhu` and `ld50_catmos` (arXiv 2505.12534), TDC ADMET Benchmark Group.
- Better data: a candidate of the benchmark ChemPile (this run searched no further); the CATMoS-based `qsar_oral_toxicity` is the larger compilation of the same endpoint and is already shipped.
- Papers and pages: Zhu et al. 2009 (paywalled, not read here); the TDC tox page and the ADMET Benchmark Group leaderboard; `qsar_oral_toxicity`'s record for the CATMoS lineage.
- Metric: the TDC ADMET Benchmark Group ranks LD50_Zhu by MAE on a scaffold split (tdcommons.ai/benchmark/admet_group/overview; "MAE is used for majority of benchmarks"), a deliberate choice of the benchmark that defined the task (MET-1, MET-5); inputs none. The target ships on the -log(mol/kg) scale the field models and scores on, so no back-transform (MET-3).
- Risks for /add-dataset: the overlap with the shipped `qsar_oral_toxicity` has to be measured by InChIKey before a curator decides which stays (PROV-6 is a real possibility if the CATMoS compilation absorbed this one); the LD50 values are pooled from registry data with mixed protocols and species conventions; the duplicate record `tdc_ld50_zhu` has to be resolved; features are the SMILES only.
- Priority: gap 0 (chemistry not thin), use case + (a hazard category a regulator assigns), source + (a journal paper plus a benchmark that defines the task), shape + (7,385 compounds), risk - (a shipped record covers the endpoint on a larger compilation, and a second record holds the same file).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 7,385 compounds (TDC LD50_Zhu); in ChemPile-LIFT 140,315 text prompts over 1 config(s); target: acute toxicity LD50 (log(1/(mol/kg))).
- Why: Predict the rat oral LD50 of a compound
- Notes: Zhu et al. 2009 (Chem Res Toxicol 22:1913). Same endpoint as the ld50_catmos config and as the existing qsar_oral_toxicity record, on a smaller and older compilation; CATMoS supersedes it. Features: SMILES string only, so a container keeps the string and adds computed descriptors, as the apistox record does.

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: the same TDC LD50 (Zhu) file, once as SMILES and once as TabBench-Bio's fingerprint build (`tdc_ld50_zhu`; PROV-6). The curator keeps one, or both as distinct tasks.
