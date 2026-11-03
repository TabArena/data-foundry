---
unique_name: tdc_ld50_zhu
name: TDC-LD50-Zhu (Acute Toxicity LD50)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
collections:
- TabBench-Bio
source_links:
- https://doi.org/10.1021/tx900189p
- https://dataverse.harvard.edu/api/access/datafile/4267146
- https://arxiv.org/abs/2609.07441
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Duplicate`, PROV-4): TabBench-Bio's 2,048-bit ECFP4 build of TDC's LD50_Zhu file (Harvard Dataverse 4267146), 7,341 of TDC's 7,385 compounds, which `ld50_zhu` already records with Zhu et al. 2009; a processed cut of the same rows (PROV-6).
- Source: Zhu, Martin, Ye, Sedykh, Young and Tropsha 2009, "Quantitative Structure-Activity Relationship Modeling of Rat Acute Toxicity by Oral Exposure", Chem Res Toxicol 22(12):1913 (doi 10.1021/tx900189p, online 2009-10-21), served by TDC as LD50_Zhu ("7,385 drugs", tdcommons.ai/single_pred_tasks/tox) from Dataverse file 4267146 (tdc/metadata.py); header previewed: `ID` (name), `X` (SMILES), `Y` (-log(mol/kg)). TabBench-Bio registry (github.com/not-a-feature/TabBench-Bio, src/tabbench_bio/bio/data/bio_datasets.json, read 2026-10-31), `TDC-LD50-Zhu`: "Validated official Harvard Dataverse file 4267146. Canonical parent structures, median target for exact duplicates, 2048-bit ECFP4, grouped by Bemis-Murcko scaffold. Quality pass: 7341 molecules, 2048 features, 3605 groups; 1 invalid structure dropped".
- Use case: as on `ld50_zhu`: a toxicologist or regulator assigns an acute-toxicity hazard category to a chemical without an animal study; regime grouped on the Bemis-Murcko scaffold (SPLIT-31).
- Siblings and duplicates: `ld50_zhu` (ChemPile; `TBD -> 2nd Tier`, priority 3) takes the same TDC file, and its screening already says the two records "are versions of one dataset and one of them should carry `Duplicate` (PROV-6); the SMILES route here is the richer one": it is the survivor. `qsar_oral_toxicity` (shipped, `Yes`, CATMoS, binary very-toxic label) is the same endpoint from a larger compilation, a distinct framing (PROV-7) whose overlap is held on `ld50_zhu`. External collections: TabBench-Bio (Kreuer et al., arXiv 2609.07441v2, 2026-09-26, Table 4), TDC ADMET benchmark group, ChemPile.
- Better data: a candidate of the benchmark TabBench-Bio; no further search this round.
- Papers and pages: Zhu et al. 2009; TDC's tox page and ADMET benchmark group; the TabBench-Bio paper and registry.
- Metric: TDC's ADMET group scores LD50_Zhu by MAE on a scaffold split (tdcommons.ai/benchmark/admet_group/overview); TabBench-Bio scores every regression task by RMSE ("RMSE is the primary regression metric", Sec. 3.5). The metric decision stays with `ld50_zhu`.
- Reject check (AI, 2026-10-31): stands. Registry: 'Validated official Harvard Dataverse file 4267146', citation Zhu et al. 2009 (https://raw.githubusercontent.com/not-a-feature/TabBench-Bio/main/src/tabbench_bio/bio/data/bio_datasets.json); TDC maps 'ld50_zhu': 4267146 (tdc/metadata.py, checked), the LD50_Zhu file `ld50_zhu` records (its screening names this record a version of it). 7,341 of 7,385 compounds is a cut (PROV-6).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 7,341 x 2,048; target: Y.
- Why: Rat oral acute toxicity (-log mol/kg LD50) from 2048-bit ECFP4 fingerprints
- Notes: Related, not the same: qsar_oral_toxicity (UCI, binary very-toxic label on 8,992 chemicals, 1,024-bit fingerprints).
