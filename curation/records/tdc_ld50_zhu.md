---
unique_name: tdc_ld50_zhu
name: TDC-LD50-Zhu (Acute Toxicity LD50)
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
- https://doi.org/10.1021/tx900189p
- https://dataverse.harvard.edu/api/access/datafile/4267146
- https://arxiv.org/abs/2609.07441
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-25):** `No` (`Duplicate`, PROV-4): TabBench-Bio's 2,048-bit ECFP4 build of TDC's LD50_Zhu
file (Harvard Dataverse 4267146), 7,341 of TDC's 7,385 compounds, which `ld50_zhu` already records with Zhu et al.
2009; a processed cut of the same rows (PROV-6). Re-checked under the 2026-11-24 rules: the split rules changed, the
provenance did not, so the reject stands.
- Source: Zhu, Martin, Ye, Sedykh, Young and Tropsha 2009, "Quantitative Structure-Activity Relationship Modeling of
  Rat Acute Toxicity by Oral Exposure", Chem Res Toxicol 22(12):1913 (doi 10.1021/tx900189p, online 2009-10-21),
  served by TDC as LD50_Zhu ("7,385 drugs", tdcommons.ai/single_pred_tasks/tox) from Dataverse file 4267146
  (`tdc/metadata.py`, re-checked 2026-11-25); the file re-downloaded 2026-11-25 holds 7,385 rows of `ID` (name), `X`
  (SMILES), `Y` (-log(mol/kg)), of which 1 is unparseable and 43 repeat a structure already in the file. TabBench-Bio
  registry (re-read 2026-11-25), `TDC-LD50-Zhu`: "Validated official Harvard Dataverse file 4267146. Canonical parent
  structures, median target for exact duplicates, 2048-bit ECFP4, grouped by Bemis-Murcko scaffold. Quality pass: 7341
  molecules, 2048 features, 3605 groups; 1 invalid structure dropped".
- Use case: as on `ld50_zhu` — a toxicologist or regulator assigns an acute-toxicity hazard category to a chemical
  without an animal study. Collection: a compilation of published rat oral LD50 values, a property of the compound
  with no date per row (`Samples: No Time Dimension`); 43 of the file's 7,385 rows repeat a structure already in it
  and the build takes their median (`Entities: Recur`); type `Experimental Results` (a closed set of chemicals
  measured by one assay protocol, SPLIT-34).
- Split: none decided here (the task is recorded on `ld50_zhu`); had it one, leaf L-EXP.kind (Grouped · `UnseenGroup`,
  the Bemis-Murcko scaffold) because [EXP.meets] is a chemical series the data does not contain and [EXP.kind-key] yes
  — on this build too: the loader computes the scaffold from the SMILES before it encodes them and returns it as a
  `murcko_scaffold` group column (`loaders/tdc.py`, `_scaffold`), which is where the registry's 3,605 groups come
  from, so the leaf is the same on both and the fingerprint build loses no split. What it loses is the structures: 169
  of its 7,341 molecules share their 2,048-bit row with a different molecule, every one of those rows with a different
  LD50 — a noise floor the survivor's SMILES do not have (CLEAN-24, the reason the structure release is the copy that
  stays, not a split argument). An item's repeated measurements stay on one side either way (SPLIT-24).
- Siblings and duplicates: `ld50_zhu` (ChemPile; `TBD -> 2nd Tier`, priority 3) takes the same TDC file and is the
  survivor. `qsar_oral_toxicity` (shipped, `Yes`, CATMoS, binary very-toxic label) is the same endpoint from a larger
  compilation, a distinct framing (PROV-7) whose overlap is held on `ld50_zhu`. External collections: TabBench-Bio
  (Kreuer et al., arXiv 2609.07441v2, Table 4), TDC ADMET benchmark group, ChemPile.
- Better data: a candidate of the benchmark TabBench-Bio; no further search this round (the survivor holds the CATMoS
  question).
- Papers and pages: Zhu et al. 2009; TDC's tox page and ADMET benchmark group; the TabBench-Bio paper and registry.
- Metric: TDC's ADMET group scores LD50_Zhu by MAE on a scaffold split (tdcommons.ai/benchmark/admet_group/overview);
  TabBench-Bio scores every regression task by RMSE ("RMSE is the primary regression metric", Sec. 3.5). The metric
  decision stays with `ld50_zhu`.
- Reject check (AI, 2026-11-25): stands, on the file rather than on the registry's word. Dataverse 4267146
  re-downloaded 2026-11-25 hashes to the registry's `download_sha256` (fdae7cfe…f5ff16), and TabBench-Bio's own
  pipeline re-run on it returns 7,341 molecules in 3,605 scaffold groups, the registry's numbers exactly: the build is
  this file's 7,385 rows with 1 unparseable structure dropped and 43 repeats merged by their median, then
  ECFP4-encoded — no compound, no label and no question added (PROV-4, PROV-6), and the encoding is one RDKit call on
  the survivor's SMILES. `ld50_zhu` holds the same file with the SMILES and stands (`TBD -> 2nd Tier`, priority 3), so
  the better copy survives: 2nd Tier is a keep, and the open CATMoS overlap with the shipped `qsar_oral_toxicity` is
  held there, where the structures needed to measure it are. The 43 repeats and the 169 molecules that collide in the
  bits go to its add stage.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 7,341 x 2,048; target: Y.
- Why: Rat oral acute toxicity (-log mol/kg LD50) from 2048-bit ECFP4 fingerprints
- Notes: Related, not the same: qsar_oral_toxicity (UCI, binary very-toxic label on 8,992 chemicals, 1,024-bit fingerprints).
