---
unique_name: tdc_bbb_martins
name: TDC-BBB-Martins (Blood-Brain Barrier Penetration)
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
- https://doi.org/10.1021/ci300124c
- https://dataverse.harvard.edu/api/access/datafile/4259566
- https://arxiv.org/abs/2609.07441
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-25):** `No` (`Duplicate`, PROV-4): TabBench-Bio's 2,048-bit ECFP4 build of TDC's BBB_Martins
file (Harvard Dataverse 4259566), 1,954 distinct structures of that file's 2,039 rows, which `bbbp_martins` already
records with Martins et al. 2012; a processed cut of the same rows (PROV-6). Re-checked under the 2026-11-24 rules:
the split rules changed, the provenance did not, so the reject stands.
- Source: Martins, Teixeira, Pinheiro and Falcao 2012, "A Bayesian Approach to in Silico Blood-Brain Barrier
  Penetration Modeling", J Chem Inf Model (doi 10.1021/ci300124c, online 2012-06-06), served by TDC as BBB_Martins
  ("1,975 drugs", references Martins et al. 2012 and MoleculeNet, tdcommons.ai/single_pred_tasks/adme) from Dataverse
  file 4259566 (`tdc/metadata.py`, size 1,975, re-checked 2026-11-25); the file re-downloaded 2026-11-25 holds 2,039
  rows of `Drug_ID`, `Drug` (SMILES), `Y` — 1 unparseable, 73 repeats of a structure already in the file, and 11
  structures reported with both labels, which leaves the build's 1,954. TabBench-Bio registry (re-read 2026-11-25),
  `TDC-BBB-Martins`: "Validated official Harvard Dataverse file 4259566. Canonical parent structures, exact-molecule
  deduplication, 2048-bit ECFP4, grouped by Bemis-Murcko scaffold. Quality pass: 1954 molecules, 2048 features, 1187
  groups; 1 invalid structure and 11 conflicting molecules dropped".
- Use case: as on `bbbp_martins` — a medicinal chemist developing a CNS drug predicts, before synthesis, whether the
  compound crosses the barrier. Collection: a compilation of published penetration measurements, a property of the
  molecule with no date per compound (`Samples: No Time Dimension`); 73 of the file's 2,039 rows repeat a structure
  already in it, 11 of them with the opposite label (`Entities: Recur`); type `Experimental Results` (a closed set of
  molecules measured by laboratory protocols, SPLIT-34).
- Split: none decided here (the task is recorded on `bbbp_martins`); had it one, leaf L-EXP.kind (Grouped ·
  `UnseenGroup`, the Bemis-Murcko scaffold) because [EXP.meets] is a chemical series the data does not contain and
  [EXP.kind-key] yes — on this build too: the loader computes the scaffold from the SMILES before it encodes them and
  returns it as a `murcko_scaffold` group column (`loaders/tdc.py`, `_scaffold`), which is where the registry's 1,187
  groups come from, so the leaf is the same on both and the fingerprint build loses no split. What it loses is the
  structures: 47 of its 1,954 molecules share their 2,048-bit row with a different molecule (6 of those rows carry
  different labels), which the survivor's SMILES keep apart — the CLEAN-24 reason the structure release is the copy
  that stays, not a split argument.
- Siblings and duplicates: `bbbp_martins` (ChemPile; `TBD -> Yes`, priority 3, `Selection Bias`) names TDC's
  BBB_Martins among its copies and is the survivor (first publication, SMILES for CLEAN-24).
  `b3db_blood_brain_barrier` (Meng et al. 2021, 7,807 compounds) is the larger compilation of the same task from other
  sources, its own record. External collections: TabBench-Bio (Kreuer et al., arXiv 2609.07441v2, Table 4), TDC ADMET
  benchmark group, MoleculeNet, ChemPile.
- Better data: a candidate of the benchmark TabBench-Bio; no further search this round (`b3db_blood_brain_barrier` is
  recorded and held on the survivor).
- Papers and pages: Martins et al. 2012; MoleculeNet (Wu et al. 2018); TDC's ADME page and ADMET benchmark group; the
  TabBench-Bio paper and registry.
- Metric: TDC's ADMET group scores BBB_Martins by AUROC on a scaffold split
  (tdcommons.ai/benchmark/admet_group/overview); TabBench-Bio scores every classification task by "Macro-F1 is the
  primary classification metric" (Sec. 3.5), a benchmark-wide default with no threshold fixed (MET-6), with AUROC as a
  re-ranking in its Appendix E. The metric decision stays with `bbbp_martins`.
- Reject check (AI, 2026-11-25): stands, on the file rather than on the registry's word. Dataverse 4259566
  re-downloaded 2026-11-25 hashes to the registry's `download_sha256` (eb32676c…bd5e98), and TabBench-Bio's own
  pipeline re-run on it returns 1,954 molecules in 1,187 scaffold groups, the registry's numbers exactly, including
  its 1 invalid and 11 conflicting molecules: the build is this file's 2,039 rows deduplicated on the canonical parent
  structure and ECFP4-encoded, with no compound, no label and no question added (PROV-4, PROV-6), and the encoding is
  one RDKit call on the survivor's SMILES. `bbbp_martins` records the Martins data with its first publication, keeps
  the SMILES and stands (`TBD -> Yes`, priority 3, `Selection Bias`), so the better copy survives; the 73 repeat
  structures, the 11 label conflicts and the 47 molecules that collide in the bits go to its add stage, which its own
  record already asks for (LEAK-16, CLEAN-24). Correction to the 2026-10-31 block: the Dataverse file has 2,039 rows,
  not the 1,975 of TDC's size table, which is already a deduplicated count.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 1,954 x 2,048; target: Y.
- Why: Whether a molecule penetrates the blood-brain barrier, from 2048-bit ECFP4 fingerprints
- Notes: TDC ADMET task; fingerprints computed by the authors from SMILES; CV grouped by Bemis-Murcko scaffold.
