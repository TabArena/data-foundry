---
unique_name: tdc_lipophilicity_astrazeneca
name: TDC-Lipophilicity-AstraZeneca
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Andrej
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
- Many features
- 'Samples: No Time Dimension'
- Experimental Results
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

**Screening (AI, 2026-11-25):** `No` (`Duplicate`, PROV-4): TabBench-Bio's 2,048-bit ECFP4 build of TDC's
Lipophilicity_AstraZeneca file (Harvard Dataverse 4259595), the same 4,200 compounds of AstraZeneca's ChEMBL
deposition that `astrazeneca_chembl_logd74` already records; fingerprints of the same rows add no distinct task.
Re-checked under the 2026-11-24 rules: the split rules changed, the provenance did not, so the reject stands.
- Source: AstraZeneca's deposition in ChEMBL, document CHEMBL3301361, "Experimental in vitro DMPK and physicochemical
  data on a set of publicly disclosed compounds" (doi 10.6019/CHEMBL3301361, 2015), assay CHEMBL3301363 (logD7.4 by
  shake flask; the API returns 4,200 activities for it, re-checked 2026-11-25); served by MoleculeNet as Lipophilicity
  and by TDC as Lipophilicity_AstraZeneca from Dataverse file 4259595 (`tdc/metadata.py`, re-checked 2026-11-25); the
  file re-downloaded 2026-11-25 holds 4,200 rows of `Drug_ID` (ChEMBL id), `Drug` (SMILES), `Y` (logD), every one a
  distinct structure. TabBench-Bio registry (re-read 2026-11-25), `TDC-Lipophilicity-AstraZeneca`: "Validated official
  Harvard Dataverse file 4259595. Canonical parent structures, 2048-bit ECFP4, grouped by Bemis-Murcko scaffold.
  Quality pass: 4200 molecules, 2048 features, 2447 groups; no invalid or duplicate structures".
- Use case: as on `astrazeneca_chembl_logd74` — a DMPK scientist or medicinal chemist estimates logD7.4 before a
  compound is made or progressed. Collection: one deposit of a closed compound set measured under one shake-flask
  protocol, with no date per row (`Samples: No Time Dimension`; the deposit's ChEMBL document carries no year), one
  activity per compound and no duplicate structures; type `Experimental Results` (a company's own deposit measured by
  a laboratory protocol, not the growing database that serves it, SPLIT-34 rule 4).
- Split: none decided here (the task is recorded on `astrazeneca_chembl_logd74`, whose leaf is L-EXP.kind, Grouped ·
  `UnseenGroup` on the Bemis-Murcko scaffold); the leaf is the same on this build, which does not lose the split: the
  loader computes the scaffold from the SMILES before it encodes them and returns it as a `murcko_scaffold` group
  column (`loaders/tdc.py`, `_scaffold`), which is where the registry's 2,447 groups come from — the same 2,447 the
  survivor's record already quotes. What the build loses is the structures: 202 of its 4,200 molecules share their
  2,048-bit row with a different molecule, and 183 of those rows carry a different logD — a noise floor the survivor's
  SMILES do not have, and the CLEAN-24 reason the structure release is the copy that stays.
- Siblings and duplicates: `astrazeneca_chembl_logd74` (ChemPile; `TBD -> Yes`, priority 3) records the same 4,200
  compounds and is the survivor. `hepatocyte_clearance_astrazeneca` is another assay of the same deposition, a
  distinct task (PROV-7). External collections: TabBench-Bio (Kreuer et al., arXiv 2609.07441v2, Table 4), TDC ADMET
  benchmark group, MoleculeNet, ChemPile.
- Better data: none found for the endpoint (searched on the survivor 2026-11-25: the public logd74 set of 1,130
  compounds is smaller, and the larger public compilations measure logP, not logD7.4).
- Papers and pages: the ChEMBL document report card CHEMBL3301361; MoleculeNet (Wu et al. 2018); TDC's ADME page and
  ADMET benchmark group; the TabBench-Bio paper and registry.
- Metric: TDC's ADMET group scores Lipophilicity_AstraZeneca by MAE on a scaffold split, MoleculeNet by RMSE on a
  random split (Table 1); TabBench-Bio scores every regression task by RMSE (Sec. 3.5). The metric decision stays with
  `astrazeneca_chembl_logd74` (fallback `rmse` proposed there).
- Reject check (AI, 2026-11-25): stands, on the file rather than on the registry's word. Dataverse 4259595
  re-downloaded 2026-11-25 hashes to the registry's `download_sha256` (14add1ed…7f1d4c), and TabBench-Bio's own
  pipeline re-run on it returns 4,200 molecules in 2,447 scaffold groups with no invalid and no duplicate structure,
  the registry's numbers exactly: the build is this file's 4,200 rows ECFP4-encoded, row for row, and the file is the
  4,200 logD7.4 activities of assay CHEMBL3301363 that `astrazeneca_chembl_logd74` records from the deposition — the
  same rows, the same target, no question added (PROV-4, PROV-6), and the encoding is one RDKit call on the survivor's
  SMILES. That record stands (`TBD -> Yes`, priority 3) and keeps the ChEMBL ids this table drops, so the better copy
  survives; the 183 pairs that the bits cannot tell apart though their logD differs go to its add stage, beside the
  censoring check its own record already asks for.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 4,200 x 2,048; target: Y.
- Why: Octanol/water distribution coefficient (logD7.4) from 2048-bit ECFP4 fingerprints
- Notes: AstraZeneca deposition in ChEMBL (2015), via MoleculeNet/TDC; scaffold-grouped CV.
