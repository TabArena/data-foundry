---
unique_name: tdc_aqsoldb
name: TDC-AqSolDB (Aqueous Solubility)
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
- 'Entities: Recur'
- Experimental Results
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

**Screening (AI, 2026-11-25):** `No` (`Duplicate`, PROV-4): TabBench-Bio's 2,048-bit ECFP4 build of TDC's
Solubility_AqSolDB file (Harvard Dataverse 4259610), which is AqSolDB (Sorkun et al. 2019), already recorded as
`aqsoldb`; 9,562 of the 9,982 compounds after exact duplicates were merged, a cut of the same rows (PROV-6).
Re-checked under the 2026-11-24 rules: the split rules changed, the provenance did not, so the reject stands.
- Source: Sorkun, Khetan and Er 2019, "AqSolDB, a curated reference set of aqueous solubility and 2D descriptors for a
  diverse set of compounds", Sci Data 6:143 (doi 10.1038/s41597-019-0151-1, online 2019-08-08; data doi
  10.7910/DVN/OVHAW8), served by TDC as Solubility_AqSolDB ("9,982 drugs", tdcommons.ai/single_pred_tasks/adme) from
  Dataverse file 4259610 (`tdc/metadata.py`, re-checked 2026-11-25); header previewed: `Drug_ID` (name), `Drug`
  (SMILES), `Y` (LogS). TabBench-Bio registry (re-read 2026-11-25), `TDC-AqSolDB`: "Validated official Harvard
  Dataverse file 4259610. Canonical parent structures, median target for exact duplicates, 2048-bit ECFP4, grouped by
  Bemis-Murcko scaffold. Quality pass: 9562 molecules, 2048 features, 4620 groups; 2 invalid structures dropped".
- Use case: as on `aqsoldb` — a medicinal chemist estimates the aqueous solubility (LogS) of a compound before it is
  made or assayed. Collection: a curated compilation of measured solubilities, a fixed property of the molecule with
  no date per compound (`Samples: No Time Dimension`); AqSolDB pools nine source sets and keeps several measurements
  of one compound — 418 of its 9,982 rows repeat a structure already in the file, which the build merges by their
  median (`Entities: Recur`); type `Experimental Results` (a closed set of molecules measured by laboratory protocols,
  SPLIT-34 — not a catalogue, which rule 4 keeps for the growing database itself).
- Split: none decided here (the task is recorded on `aqsoldb`); had it one, leaf L-EXP.kind (Grouped · `UnseenGroup`,
  the Bemis-Murcko scaffold) because [EXP.meets] is a chemical series the data does not contain and [EXP.kind-key] yes
  — on this build too: the loader computes the scaffold from the SMILES before it encodes them and returns it as a
  `murcko_scaffold` group column (`loaders/tdc.py`, `_scaffold`), which is where the registry's 4,620 groups come
  from, so the leaf is the same on both and the fingerprint build loses no split. What it loses is the structures:
  1,037 of its 9,562 molecules share their 2,048-bit row with a different molecule, and 995 of those rows carry a
  different LogS — a noise floor the survivor's SMILES do not have (CLEAN-24, the reason the structure release is the
  copy that stays, not a split argument). An item's repeated measurements stay on one side either way (SPLIT-24).
- Siblings and duplicates: `aqsoldb` (Zotero and awesome-chemistry-datasets; links the AqSolDB Dataverse deposit, the
  Sci Data paper and TDC's Solubility_AqSolDB) is the same source with its published descriptors and reliability
  groups, so it is the survivor (PROV-8, CLEAN-24). Related, not duplicates: `somas_aqueous_solubility`, `bigsoldb_2`,
  `drug_solubility_binary_solvent_mixtures` (other compilations or solvents). External collections: TabBench-Bio
  (Kreuer et al., arXiv 2609.07441v2, Table 4), TDC ADMET benchmark group.
- Better data: a candidate of the benchmark TabBench-Bio; no further search this round (the survivor holds the
  question).
- Papers and pages: Sorkun et al. 2019; TDC's ADME page and ADMET benchmark group; the TabBench-Bio paper and
  registry.
- Metric: TDC's ADMET group scores Solubility_AqSolDB by MAE on a scaffold split
  (tdcommons.ai/benchmark/admet_group/overview, "MAE is used for majority of benchmarks"); TabBench-Bio scores every
  regression task by RMSE ("RMSE is the primary regression metric", Sec. 3.5). The metric decision stays with
  `aqsoldb`.
- Reject check (AI, 2026-11-25): stands, on the file rather than on the registry's word. Dataverse 4259610
  re-downloaded 2026-11-25 hashes to the registry's `download_sha256` (0b593f7b…41c9a4), and TabBench-Bio's own
  pipeline re-run on it returns 9,562 molecules in 4,620 scaffold groups, the registry's numbers exactly: the build is
  this file's 9,982 rows with 2 unparseable structures dropped and 418 repeat structures merged by their median LogS,
  then ECFP4-encoded — no compound, no label and no question added (PROV-4, PROV-6), and the encoding is one RDKit
  call on the survivor's SMILES. `aqsoldb` holds AqSolDB from its own Dataverse deposit with the published descriptors
  and reliability groups and stands (`TBD -> Yes`, priority 3), so the better copy survives; the 418 repeats and the
  995 rows that collide in the bits with a different LogS go to its add stage.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 9,562 x 2,048; target: Y.
- Why: Aqueous solubility (log mol/L) of a compound from 2048-bit ECFP4 fingerprints
- Notes: TDC ADMET task; scaffold-grouped CV.
