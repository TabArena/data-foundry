---
unique_name: tdc_ames
name: TDC-AMES (Ames Mutagenicity)
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
- https://doi.org/10.1021/ci900161g
- https://dataverse.harvard.edu/api/access/datafile/4259564
- https://arxiv.org/abs/2609.07441
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Duplicate`, PROV-4): TabBench-Bio's 2,048-bit ECFP4 build of TDC's AMES file (Harvard Dataverse 4259564, 7,255 compounds), the same file `ames_mutagenicity` records with its first publication; fingerprints of the same rows add no distinct task.
- Source: Xu et al. 2012, "In silico Prediction of Chemical Ames Mutagenicity", J Chem Inf Model 52(11):2840 (doi 10.1021/ci300400a), served by TDC as AMES ("7,255 drugs", reference Xu et al. 2012, tdcommons.ai/single_pred_tasks/tox). TDC downloads `ames` from Dataverse file 4259564 (tdc/metadata.py: `"ames": 4259564`, `"ames": 7255`); header previewed: `Drug_ID`, `Drug` (SMILES), `Y`. TabBench-Bio registry (github.com/not-a-feature/TabBench-Bio, src/tabbench_bio/bio/data/bio_datasets.json, read 2026-10-31), `TDC-AMES`: "Validated official Harvard Dataverse file 4259564. Canonical parent structures, exact-molecule deduplication, 2048-bit ECFP4, grouped by Bemis-Murcko scaffold. Quality pass: 7255 molecules, 2048 features, 3008 groups". The registry cites Hansen et al. 2009 (doi 10.1021/ci900161g, this record's first link), but the 7,255-row file is TDC's Xu 2012 compilation; Hansen's 6,512-compound benchmark is `ames_mutagenicity_hansen`.
- Use case: as on `ames_mutagenicity`: a toxicologist or medicinal chemist decides, before the Ames assay is run, which new compounds to test or drop; regime grouped on the Bemis-Murcko scaffold (SPLIT-31), as here.
- Siblings and duplicates: `ames_mutagenicity` (ChemPile; `TBD -> Yes`, priority 4) takes the same TDC file, and its screening already names this record "a processed copy of this source (PROV-4, PROV-6)"; it keeps the SMILES that CLEAN-24 turns into descriptors and names the first publication (PROV-8), so it is the survivor. `ames_mutagenicity_hansen` (Hansen 2009) is the overlapping earlier compilation, a PROV-6 question held on `ames_mutagenicity`. External collections: TabBench-Bio (Kreuer et al., arXiv 2609.07441v2, 2026-09-26, Table 4), TDC ADMET benchmark group, ChemPile.
- Better data: a candidate of the benchmark TabBench-Bio; no further search this round.
- Papers and pages: Xu et al. 2012; TDC's tox page and ADMET benchmark group; the TabBench-Bio paper and registry.
- Metric: TDC's ADMET group scores AMES by AUROC on a scaffold split (tdcommons.ai/benchmark/admet_group/overview); TabBench-Bio scores every classification task by "Macro-F1 is the primary classification metric" (Sec. 3.5), a benchmark-wide default with no threshold fixed (MET-6), with AUROC as a re-ranking in its Appendix E. The metric decision stays with `ames_mutagenicity`.
- Reject check (AI, 2026-10-31): stands. Registry: 'Validated official Harvard Dataverse file 4259564' with fetch_id 'ames' (https://raw.githubusercontent.com/not-a-feature/TabBench-Bio/main/src/tabbench_bio/bio/data/bio_datasets.json); TDC's tdc/metadata.py maps 'ames': 4259564 (https://raw.githubusercontent.com/mims-harvard/TDC/main/tdc/metadata.py, checked): the TDC AMES file `ames_mutagenicity` records with its first publication. ECFP4 bits of the same rows and label add no task. The registry's Hansen 2009 citation does not change the file.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 7,255 x 2,048; target: Y.
- Why: Ames mutagenicity of a compound from 2048-bit ECFP4 fingerprints
- Notes: TDC Tox task (Hansen et al. 2009); scaffold-grouped CV.
