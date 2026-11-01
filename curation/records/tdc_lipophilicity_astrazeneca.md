---
unique_name: tdc_lipophilicity_astrazeneca
name: TDC-Lipophilicity-AstraZeneca
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
- https://doi.org/10.6019/CHEMBL3301361
- https://dataverse.harvard.edu/api/access/datafile/4259595
- https://arxiv.org/abs/2609.07441
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Duplicate`, PROV-4): TabBench-Bio's 2,048-bit ECFP4 build of TDC's Lipophilicity_AstraZeneca file (Harvard Dataverse 4259595), the same 4,200 compounds of AstraZeneca's ChEMBL deposition that `astrazeneca_chembl_logd74` already records; fingerprints of the same rows add no distinct task.
- Source: AstraZeneca's deposition in ChEMBL, document CHEMBL3301361, "Experimental in vitro DMPK and physicochemical data on a set of publicly disclosed compounds" (doi 10.6019/CHEMBL3301361, 2015), assay CHEMBL3301363 (logD7.4 by shake flask); served by MoleculeNet as Lipophilicity and by TDC as Lipophilicity_AstraZeneca ("4,200 drugs", tdcommons.ai/single_pred_tasks/adme) from Dataverse file 4259595 (tdc/metadata.py); header previewed: `Drug_ID` (ChEMBL id), `Drug` (SMILES), `Y` (logD). TabBench-Bio registry (github.com/not-a-feature/TabBench-Bio, src/tabbench_bio/bio/data/bio_datasets.json, read 2026-10-31), `TDC-Lipophilicity-AstraZeneca`: "Validated official Harvard Dataverse file 4259595. Canonical parent structures, 2048-bit ECFP4, grouped by Bemis-Murcko scaffold. Quality pass: 4200 molecules, 2048 features, 2447 groups; no invalid or duplicate structures".
- Use case: as on `astrazeneca_chembl_logd74`: a DMPK scientist or medicinal chemist estimates logD7.4 before a compound is made or progressed; regime grouped on the Bemis-Murcko scaffold (SPLIT-31).
- Siblings and duplicates: `astrazeneca_chembl_logd74` (ChemPile; `TBD -> Yes`, priority 3) records the same 4,200 compounds, and its screening already calls this record "a processed copy of this source (PROV-4, PROV-6): one of the two records stays, and the SMILES route is the one CLEAN-24 asks for": it is the survivor. `hepatocyte_clearance_astrazeneca` is another assay of the same deposition, a distinct task (PROV-7). External collections: TabBench-Bio (Kreuer et al., arXiv 2609.07441v2, 2026-09-26, Table 4), TDC ADMET benchmark group, MoleculeNet, ChemPile.
- Better data: a candidate of the benchmark TabBench-Bio; no further search this round.
- Papers and pages: the ChEMBL document report card CHEMBL3301361; MoleculeNet (Wu et al. 2018); TDC's ADME page and ADMET benchmark group; the TabBench-Bio paper and registry.
- Metric: TDC's ADMET group scores Lipophilicity_AstraZeneca by MAE on a scaffold split, MoleculeNet by RMSE on a random split (Table 1); TabBench-Bio scores every regression task by RMSE ("RMSE is the primary regression metric", Sec. 3.5). The metric decision stays with `astrazeneca_chembl_logd74` (fallback `rmse` proposed there).
- Reject check (AI, 2026-10-31): stands. Registry: 'Validated official Harvard Dataverse file 4259595 ... 4200 molecules' (https://raw.githubusercontent.com/not-a-feature/TabBench-Bio/main/src/tabbench_bio/bio/data/bio_datasets.json); TDC maps 'lipophilicity_astrazeneca': 4259595 (tdc/metadata.py, checked), the same 4,200 compounds of ChEMBL CHEMBL3301363 that `astrazeneca_chembl_logd74` records with the AstraZeneca deposition as source.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 4,200 x 2,048; target: Y.
- Why: Octanol/water distribution coefficient (logD7.4) from 2048-bit ECFP4 fingerprints
- Notes: AstraZeneca deposition in ChEMBL (2015), via MoleculeNet/TDC; scaffold-grouped CV.
