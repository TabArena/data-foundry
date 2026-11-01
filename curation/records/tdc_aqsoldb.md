---
unique_name: tdc_aqsoldb
name: TDC-AqSolDB (Aqueous Solubility)
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
- https://doi.org/10.1038/s41597-019-0151-1
- https://dataverse.harvard.edu/api/access/datafile/4259610
- https://arxiv.org/abs/2609.07441
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Duplicate`, PROV-4): TabBench-Bio's 2,048-bit ECFP4 build of TDC's Solubility_AqSolDB file (Harvard Dataverse 4259610), which is AqSolDB (Sorkun et al. 2019), already recorded as `aqsoldb`; 9,562 of the 9,982 compounds after TabBench-Bio merged exact duplicates, a cut of the same rows (PROV-6).
- Source: Sorkun, Khetan and Er 2019, "AqSolDB, a curated reference set of aqueous solubility and 2D descriptors for a diverse set of compounds", Sci Data 6:143 (doi 10.1038/s41597-019-0151-1, online 2019-08-08; data doi 10.7910/DVN/OVHAW8), served by TDC as Solubility_AqSolDB ("9,982 drugs", tdcommons.ai/single_pred_tasks/adme). TDC downloads it from Dataverse file 4259610 (tdc/metadata.py); header previewed: `Drug_ID` (name), `Drug` (SMILES), `Y` (LogS). TabBench-Bio registry (github.com/not-a-feature/TabBench-Bio, src/tabbench_bio/bio/data/bio_datasets.json, read 2026-10-31), `TDC-AqSolDB`: "Validated official Harvard Dataverse file 4259610. Canonical parent structures, median target for exact duplicates, 2048-bit ECFP4, grouped by Bemis-Murcko scaffold. Quality pass: 9562 molecules, 2048 features, 4620 groups; 2 invalid structures dropped".
- Use case: a medicinal chemist estimates the aqueous solubility (LogS) of a compound before it is made or assayed; regime grouped on the Bemis-Murcko scaffold (SPLIT-31). The use case and fit are settled on `aqsoldb`.
- Siblings and duplicates: `aqsoldb` (Zotero and awesome-chemistry-datasets; links the AqSolDB Dataverse deposit, the Sci Data paper and TDC's Solubility_AqSolDB) is the same source with its 17 published descriptors and reliability groups, so it is the survivor (PROV-8, CLEAN-24). Related, not duplicates: `somas_aqueous_solubility`, `bigsoldb_2`, `drug_solubility_binary_solvent_mixtures` (other compilations or solvents). External collections: TabBench-Bio (Kreuer et al., arXiv 2609.07441v2, 2026-09-26, Table 4), TDC ADMET benchmark group.
- Better data: a candidate of the benchmark TabBench-Bio; no further search this round.
- Papers and pages: Sorkun et al. 2019; TDC's ADME page and ADMET benchmark group; the TabBench-Bio paper and registry.
- Metric: TDC's ADMET group scores Solubility_AqSolDB by MAE on a scaffold split (tdcommons.ai/benchmark/admet_group/overview, "MAE is used for majority of benchmarks"); TabBench-Bio scores every regression task by RMSE ("RMSE is the primary regression metric", Sec. 3.5). The metric decision stays with `aqsoldb`.
- Reject check (AI, 2026-10-31): stands. Registry: 'Validated official Harvard Dataverse file 4259610', citation Sorkun et al. 2019 (https://raw.githubusercontent.com/not-a-feature/TabBench-Bio/main/src/tabbench_bio/bio/data/bio_datasets.json); TDC maps 'solubility_aqsoldb': 4259610 (tdc/metadata.py, checked), AqSolDB, which `aqsoldb` records from its Dataverse deposit (doi 10.7910/DVN/OVHAW8) and Sci Data paper. Median-merged duplicates are a cut of the same rows (PROV-6).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 9,562 x 2,048; target: Y.
- Why: Aqueous solubility (log mol/L) of a compound from 2048-bit ECFP4 fingerprints
- Notes: TDC ADMET task; scaffold-grouped CV.
