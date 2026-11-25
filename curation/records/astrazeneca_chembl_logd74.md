---
unique_name: astrazeneca_chembl_logd74
name: lipophilicity
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Andrej
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
- 'Samples: No Time Dimension'
- Experimental Results
collections:
- ChemPile
original_source: Other
year: '2015'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.6019/CHEMBL3301361
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/lipophilicity ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/lipophilicity ; original: https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/Lipophilicity.csv (MoleculeNet) ; https://tdcommons.ai/single_pred_tasks/adme/#lipophilicity-astrazeneca'
- https://arxiv.org/abs/2505.12534
- https://www.ebi.ac.uk/chembl/api/data/assay/CHEMBL3301363
- https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/Lipophilicity.csv
- https://www.ebi.ac.uk/chembl/document_report_card/CHEMBL3301361/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-25):** `TBD -> Yes`, priority 3: 4,200 logD7.4 values measured at one company under one
shake-flask protocol, the standard lipophilicity regression of molecular ML. Verdict and priority unchanged; the
deposit now reads as experimental results rather than a catalogue cut, and the scaffold hold-out is the tree's leaf.
- Source: AstraZeneca's deposition in ChEMBL, document CHEMBL3301361, "Experimental in vitro DMPK and physicochemical
  data on a set of publicly disclosed compounds" (Mark Wenlock and Nicholas Tomkinson; doc_type DATASET, ChEMBL_20,
  creation_date 2015-01-14, doi 10.6019/CHEMBL3301361). The assay is CHEMBL3301363: "ASTRAZENECA: Octan-1-ol/water
  (pH7.4) distribution coefficent measured by a shake flask method described in J. Biomol. Screen. 2011, 16, 348-355.
  Experimental range -1.5 to 4.5"; the ChEMBL API returns 4,200 activities of standard_type LogD7.4 for it, in
  document CHEMBL3301361, which carries no document year (re-checked 2026-11-25). The copy in use is MoleculeNet's
  Lipophilicity.csv (columns CMPD_CHEMBLID, exp, smiles; header previewed), also served by TDC as
  Lipophilicity_AstraZeneca (Harvard Dataverse file 4259595, 4,200 compounds in TDC's own size table). One table.
- Use case: a DMPK scientist or medicinal chemist, before a compound is made or progressed, estimates its logD7.4
  ("Lipophilicity is an important feature of drug molecules that affects both membrane permeability and solubility",
  MoleculeNet Sec. 3.1.6); the deposition itself names no actor or decision, so the use case is ours to state and the
  fit is approximate until the curator settles it. Collection: one deposit of a closed compound set measured under
  one protocol, each value a fixed property of the molecule and no date per row (`Samples: No Time Dimension`; the
  deposit's ChEMBL document has no year); one activity per compound, so no `Entities: Recur` (the TabBench-Bio build
  of the same file reports "no invalid or duplicate structures"); type `Experimental Results` — a company's own
  deposit of molecules measured by a laboratory protocol, not the growing database that serves it (SPLIT-34 rule 4).
- Split: leaf L-EXP.kind (Grouped · `UnseenGroup`, the Bemis-Murcko scaffold) because [EXP.meets] is a chemical
  series the data does not contain (the chemist asks for compounds of series this DMPK set never measured, the case
  SPLIT-31 was amended on) and [EXP.kind-key] yes (the SMILES compute the scaffold; 2,447 scaffold groups over the
  4,200 compounds in the TabBench-Bio build, enough to hold out whole); open: whether the use case is instead a new
  compound of the series the company already works on ([EXP.meets] → L-EXP.random), which is what MoleculeNet's
  random split assumes while TDC's scaffold split does not, and how the ring-less compounds are grouped (the
  `qsar_bioconcentration` amendment keeps them, and the bare benzene ring, apart).
- Siblings and duplicates: `tdc_lipophilicity_astrazeneca` (TabBench-Bio) is the same 4,200 compounds as 2,048-bit
  ECFP4 fingerprints, a processed copy of this source (PROV-4, PROV-6): one of the two records stays, and the SMILES
  route is the one CLEAN-24 asks for — the fingerprint table cannot even compute the scaffold its own split needs.
  `hepatocyte_clearance_astrazeneca` is another assay of the same deposition, a different target and task (PROV-7),
  not a duplicate; the deposit also holds solubility, pKa and plasma protein binding assays. External collections:
  ChemPile / ChemNLP (`lipophilicity`), MoleculeNet, TDC, TabBench-Bio.
- Better data: none found (searched 2026-11-25 for a larger public logD7.4 set): the hand-curated logd74 collection
  of 1,130 organic compounds is smaller, and the larger public lipophilicity compilations (SangsterLogP and the
  ChEMBL logP extractions used by D-MPNN) measure logP, not logD at pH 7.4, which cannot be pooled without a pH
  correction. The deposit's own sibling endpoints are other tasks, not better data.
- Papers and pages: the ChEMBL document report card CHEMBL3301361; MoleculeNet (Wu et al. 2018, Chem Sci, Table 1 and
  Sec. 3.1.6); TDC's ADMET benchmark group.
- Metric: the two task definers disagree. MoleculeNet's Table 1 gives "Lipophilicity SMILES 1 Regression 4200 Random
  RMSE" ("For each dataset, we propose a metric and a splitting pattern that best fit the properties of the
  dataset"); TDC's ADMET group gives MAE with a scaffold split. No unique source metric, so the fallback `rmse` on
  logD (MET-5, MET-8), which agrees with MoleculeNet; inputs none beyond the scaffold group the split needs, which a
  build computes from the SMILES.
- Risks for /add-dataset: the assay's stated range (-1.5 to 4.5) suggests censored values at the ends, so check for
  pile-ups at the bounds (CLEAN-11); take the ChEMBL route or the MoleculeNet CSV, both of which keep the compound
  id, and check salt forms, stereoisomers and near-duplicate structures that collapse onto the same 2D descriptors
  and can sit on both sides of a scaffold split (LEAK-17, LEAK-19, CLEAN-24); ChEMBL's licence is CC BY-SA 3.0 (no
  verdict reason, EV-4).
- Priority: gap 0 (chemistry & material science has 15 accepted datasets and regression 85, neither thin), use case 0
  (the deposition names no decision), source + (a documented assay with its protocol), shape + (4,200 compounds),
  risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the awesome-chemistry-datasets list (github.com/kjappelbaum/awesome-chemistry-datasets); the benchmark ChemPile (https://arxiv.org/abs/2505.12534); the curator's Zotero collection, item 52: "Automatic Auxiliary Task Selection and Adaptive Weighting Boost Molecular Property ..."; the curator's Zotero collection, item 82: "Amsterdam Medical Data Science".
- as published: 4,200 compounds (TDC / MoleculeNet); in ChemPile-LIFT 42,000 text prompts over 1 config(s); target: logD 7.4; access: open.
- Why: Predict the octanol/water distribution coefficient (logD at pH 7.4) of a compound | one company, one assay protocol, real project compounds: a consistent measurement, and the first publication is traceable in ChEMBL rather than through the DeepChem CSV the list links | One lab, one protocol, real measurements: ...
- Adds: | no lipophilicity or ADME task in the benchmark; sibling endpoints in the same deposition. The MoleculeNet and TDC copies drop the ChEMBL ids, the ChEMBL route keeps them | No lipophilicity or DMPK dataset is recorded. The deposit's other assays (solubility, PPB, clearance) are sibling tasks from the same source.
- Notes: AstraZeneca deposition in ChEMBL (CHEMBL3301361), curated by MoleculeNet. Licence CC BY-SA 3.0 (ChEMBL). Reported already in this run by bench_2609.07441 as tdc_lipophilicity_astrazeneca (TabBench-Bio uses an ECFP4 version). Features: SMILES string only, so a container keeps the string and adds computed descriptors, ...

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: the same data, once as SMILES and once as a fingerprint build (`tdc_lipophilicity_astrazeneca`; PROV-6). The curator keeps one, or both as distinct tasks.
