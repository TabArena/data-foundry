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
- Many features
- 'Samples: No Time Dimension'
- 'Entities: Recur'
- Experimental Results
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

**Screening (AI, 2026-11-25):** `No` (`Duplicate`, PROV-4): TabBench-Bio's 2,048-bit ECFP4 build of TDC's AMES file
(Harvard Dataverse 4259564), the same file `ames_mutagenicity` records with its first publication; fingerprints of the
same rows and the same label add no distinct task. Re-checked under the 2026-11-24 rules: the split rules changed, the
provenance did not, so the reject stands.
- Source: Xu et al. 2012, "In silico Prediction of Chemical Ames Mutagenicity", J Chem Inf Model 52(11):2840 (doi
  10.1021/ci300400a), served by TDC as AMES ("7,255 drugs", tdcommons.ai/single_pred_tasks/tox) from Dataverse file
  4259564 (`tdc/metadata.py`: `ames` -> 4259564, size 7,255, re-checked 2026-11-25); the file re-downloaded 2026-11-25
  holds 7,278 rows of `Drug_ID`, `Drug` (SMILES), `Y`, of which 7,255 are distinct canonical parent structures (23
  repeat rows, none with conflicting labels) — TDC's stated size is that deduplicated count. TabBench-Bio registry
  (re-read 2026-11-25), `TDC-AMES`: "Validated official Harvard Dataverse file 4259564. Canonical parent structures,
  exact-molecule deduplication, 2048-bit ECFP4, grouped by Bemis-Murcko scaffold. Quality pass: 7255 molecules, 2048
  features, 3008 groups". The registry cites Hansen et al. 2009 (doi 10.1021/ci900161g, this record's first link), but
  the file is TDC's Xu 2012 compilation; Hansen's 6,512-compound benchmark is `ames_mutagenicity_hansen`.
- Use case: as on `ames_mutagenicity` — a toxicologist or medicinal chemist decides, before the bacterial
  reverse-mutation assay is run, which new compounds to test or drop. Collection: a closed compilation of assay
  results, each a fixed property of the molecule, with no date per compound (`Samples: No Time Dimension`); the TDC
  file lists 23 structures twice (`Entities: Recur`), which the build merges; type `Experimental Results` (a closed
  set of molecules measured by a laboratory protocol, SPLIT-34; not a catalogue, which rule 4 keeps for the growing
  database or programme itself).
- Split: none decided here (the task is recorded on `ames_mutagenicity`); had it one, leaf L-EXP.kind (Grouped ·
  `UnseenGroup`, the Bemis-Murcko scaffold) because [EXP.meets] is a chemical series the data does not contain and
  [EXP.kind-key] yes — on this build too, not only on the survivor's SMILES: the loader computes the scaffold from the
  SMILES before it encodes them and returns it as a `murcko_scaffold` group column (`loaders/tdc.py`, `_scaffold`),
  which is where the registry's 3,008 groups come from, so the leaf is the same on both and the fingerprint build
  loses no split. What it loses is the structures: 1,206 of its 7,255 molecules share their 2,048-bit row with a
  different molecule (13 of those rows carry different labels), which the survivor's SMILES keep apart — the CLEAN-24
  reason the structure release is the copy that stays, not a split argument.
- Siblings and duplicates: `ames_mutagenicity` (ChemPile; `TBD -> Yes`, priority 4) takes the same TDC file and is the
  survivor (first publication, SMILES, PROV-8). `ames_mutagenicity_hansen` (Hansen 2009) is the overlapping earlier
  compilation, a PROV-6 question held on `ames_mutagenicity`. External collections: TabBench-Bio (Kreuer et al., arXiv
  2609.07441v2, Table 4), TDC ADMET benchmark group, ChemPile.
- Better data: a candidate of the benchmark TabBench-Bio; no further search this round (the survivor holds the
  question).
- Papers and pages: Xu et al. 2012; TDC's tox page and ADMET benchmark group; the TabBench-Bio paper and registry.
- Metric: TDC's ADMET group scores AMES by AUROC on a scaffold split (tdcommons.ai/benchmark/admet_group/overview);
  TabBench-Bio scores every classification task by "Macro-F1 is the primary classification metric" (Sec. 3.5), a
  benchmark-wide default with no threshold fixed (MET-6), with AUROC as a re-ranking in its Appendix E. The metric
  decision stays with `ames_mutagenicity`.
- Reject check (AI, 2026-11-25): stands, on the file rather than on the registry's word. Dataverse 4259564
  re-downloaded 2026-11-25 hashes to the registry's `download_sha256` (825c2b4c…6f3e16), and TabBench-Bio's own
  pipeline re-run on it returns 7,255 molecules in 3,008 scaffold groups, the registry's numbers exactly: the build is
  this file's 7,278 rows deduplicated on the canonical parent structure and ECFP4-encoded, with no compound, no label
  and no question added (PROV-4, PROV-6) and the encoding reproducible from the survivor's SMILES in one RDKit call.
  `ames_mutagenicity` holds the file with its first publication and stands (`TBD -> Yes`, priority 4), so the better
  copy survives; the 23 repeat structures and the 1,206 molecules that collide in the bits go to its add stage. The
  registry's Hansen 2009 citation names the wrong paper for the file and does not change it.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 7,255 x 2,048; target: Y.
- Why: Ames mutagenicity of a compound from 2048-bit ECFP4 fingerprints
- Notes: TDC Tox task (Hansen et al. 2009); scaffold-grouped CV.
