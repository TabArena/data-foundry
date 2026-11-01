---
unique_name: tdc_bbb_martins
name: TDC-BBB-Martins (Blood-Brain Barrier Penetration)
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
- https://doi.org/10.1021/ci300124c
- https://dataverse.harvard.edu/api/access/datafile/4259566
- https://arxiv.org/abs/2609.07441
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Duplicate`, PROV-4): TabBench-Bio's 2,048-bit ECFP4 build of TDC's BBB_Martins file (Harvard Dataverse 4259566), 1,954 of TDC's 1,975 compounds, which `bbbp_martins` already records with Martins et al. 2012; a processed cut of the same rows (PROV-6).
- Source: Martins, Teixeira, Pinheiro and Falcao 2012, "A Bayesian Approach to in Silico Blood-Brain Barrier Penetration Modeling", J Chem Inf Model (doi 10.1021/ci300124c, online 2012-06-06), served by TDC as BBB_Martins ("1,975 drugs", references Martins et al. 2012 and MoleculeNet, tdcommons.ai/single_pred_tasks/adme). TDC downloads it from Dataverse file 4259566 (tdc/metadata.py); header previewed: `Drug_ID`, `Drug` (SMILES), `Y`. TabBench-Bio registry (github.com/not-a-feature/TabBench-Bio, src/tabbench_bio/bio/data/bio_datasets.json, read 2026-10-31), `TDC-BBB-Martins`: "Validated official Harvard Dataverse file 4259566. Canonical parent structures, exact-molecule deduplication, 2048-bit ECFP4, grouped by Bemis-Murcko scaffold. Quality pass: 1954 molecules, 2048 features, 1187 groups; 1 invalid structure and 11 conflicting molecules dropped".
- Use case: as on `bbbp_martins`: a medicinal chemist developing a CNS drug predicts, before synthesis, whether the compound crosses the barrier; regime grouped on the Bemis-Murcko scaffold (SPLIT-31).
- Siblings and duplicates: `bbbp_martins` (ChemPile; `TBD -> Yes`, priority 3, `Selection Bias`) names TDC's BBB_Martins among its copies, and its screening already calls this record "the same Martins data as 2,048-bit ECFP4 fingerprints, a processed copy (PROV-4, PROV-6)"; it is the survivor (first publication, SMILES for CLEAN-24). `b3db_blood_brain_barrier` (Meng et al. 2021, 7,807 compounds) is the larger compilation of the same task from other sources, its own record. External collections: TabBench-Bio (Kreuer et al., arXiv 2609.07441v2, 2026-09-26, Table 4), TDC ADMET benchmark group, MoleculeNet, ChemPile.
- Better data: a candidate of the benchmark TabBench-Bio; no further search this round.
- Papers and pages: Martins et al. 2012; MoleculeNet (Wu et al. 2018); TDC's ADME page and ADMET benchmark group; the TabBench-Bio paper and registry.
- Metric: TDC's ADMET group scores BBB_Martins by AUROC on a scaffold split (tdcommons.ai/benchmark/admet_group/overview); TabBench-Bio scores every classification task by "Macro-F1 is the primary classification metric" (Sec. 3.5), a benchmark-wide default with no threshold fixed (MET-6), with AUROC as a re-ranking in its Appendix E. The metric decision stays with `bbbp_martins`.
- Reject check (AI, 2026-10-31): stands. Registry: 'Validated official Harvard Dataverse file 4259566', citation Martins et al. 2012 (https://raw.githubusercontent.com/not-a-feature/TabBench-Bio/main/src/tabbench_bio/bio/data/bio_datasets.json); TDC maps 'bbb_martins': 4259566 (tdc/metadata.py, checked), the BBB_Martins file `bbbp_martins` names among its copies and already calls this record a processed copy. 1,954 of 1,975 compounds is a cut (PROV-6).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 1,954 x 2,048; target: Y.
- Why: Whether a molecule penetrates the blood-brain barrier, from 2048-bit ECFP4 fingerprints
- Notes: TDC ADMET task; fingerprints computed by the authors from SMILES; CV grouped by Bemis-Murcko scaffold.
