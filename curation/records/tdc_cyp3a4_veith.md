---
unique_name: tdc_cyp3a4_veith
name: TDC-CYP3A4-Veith (CYP3A4 Inhibition)
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
- https://doi.org/10.1038/nbt.1581
- https://dataverse.harvard.edu/api/access/datafile/4259582
- https://arxiv.org/abs/2609.07441
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-25):** `No` (`Duplicate`, PROV-4): TabBench-Bio's 2,048-bit ECFP4 build of TDC's CYP3A4_Veith
file (Harvard Dataverse 4259582), the 3A4 cut of PubChem AID 1851 (Veith et al. 2009), which
`cyp450_inhibition_aid1851` already records with all five isozymes; one isozyme of the same deposit adds no distinct
task (PROV-6). Re-checked under the 2026-11-24 rules: the split rules changed, the provenance did not, so the reject
stands.
- Source: Veith, Southall, Huang et al. 2009, "Comprehensive characterization of cytochrome P450 isozyme selectivity
  across chemical libraries", Nat Biotechnol 27:1050 (doi 10.1038/nbt.1581, online 2009-10-25), deposited as PubChem
  AID 1851; served by TDC as CYP3A4_Veith ("12,328 drugs", tdcommons.ai/single_pred_tasks/adme) from Dataverse file
  4259582 (`tdc/metadata.py`, re-checked 2026-11-25); the file re-downloaded 2026-11-25 holds 12,328 rows of `Drug_ID`
  (PubChem CID), `Drug` (SMILES), `Y`, of which 26 repeat a structure already in the file. TabBench-Bio registry
  (re-read 2026-11-25), `TDC-CYP3A4-Veith`: "Validated official Harvard Dataverse file 4259582. Canonical parent
  structures, exact-molecule deduplication, 2048-bit ECFP4, grouped by Bemis-Murcko scaffold. Quality pass: 12300
  molecules, 2048 features, 7867 groups; 1 invalid and 1 conflicting molecule dropped".
- Use case: as on `cyp450_inhibition_aid1851` — a medicinal chemist flags a compound's drug-drug-interaction liability
  before synthesis or the in-vitro CYP panel. Collection: one qHTS screen of a compound library run at one centre and
  deposited once, each result a property of the molecule with no date per compound (`Samples: No Time Dimension`); 26
  of the file's 12,328 rows repeat a structure already in it, 1 of them with the opposite label (`Entities: Recur`);
  type `Experimental Results` (a designed screen of a closed compound library, SPLIT-34 — AID 1851 is one 2009 deposit
  that has not changed since, so it is not the growing programme rule 4 reserves the catalogue type for; Tox21, the
  sibling rejects of this round, is such a programme and is typed as a catalogue).
- Split: none decided here (the task is recorded on `cyp450_inhibition_aid1851`); had it one, leaf L-EXP.kind (Grouped
  · `UnseenGroup`, the Bemis-Murcko scaffold) because [EXP.meets] is a chemical series the data does not contain and
  [EXP.kind-key] yes — on this build too: the loader computes the scaffold from the SMILES before it encodes them and
  returns it as a `murcko_scaffold` group column (`loaders/tdc.py`, `_scaffold`), which is where the registry's 7,867
  groups come from, so the leaf is the same on both and the fingerprint build loses no split. What it loses is the
  structures: 398 of its 12,300 molecules share their 2,048-bit row with a different molecule (16 of those rows carry
  different labels), which the survivor's SMILES keep apart — the CLEAN-24 reason the structure release is the copy
  that stays, not a split argument.
- Siblings and duplicates: `cyp450_inhibition_aid1851` (ChemPile; `TBD -> Yes`, priority 4) covers the five isozymes
  of AID 1851, 3A4 included, and names the first publication: the survivor. Which isozyme ships is that record's open
  point. `cyp_substrates_carbon_mangels` (substrates, not inhibitors) is distinct (PROV-7). External collections:
  TabBench-Bio (Kreuer et al., arXiv 2609.07441v2, Table 4), TDC ADMET benchmark group, ChemPile.
- Better data: a candidate of the benchmark TabBench-Bio; no further search this round (the survivor holds the
  question).
- Papers and pages: Veith et al. 2009 (PMC2783980); PubChem AID 1851; TDC's ADME page and ADMET benchmark group; the
  TabBench-Bio paper and registry.
- Metric: TDC's ADMET group scores CYP3A4_Veith by AUPRC on a scaffold split
  (tdcommons.ai/benchmark/admet_group/overview, "AUPRC is used when the number of positive samples are much smaller
  than negative samples", the imbalance argument MET-9 rejects); TabBench-Bio scores every classification task by
  "Macro-F1 is the primary classification metric" (Sec. 3.5), a benchmark-wide default with no threshold fixed
  (MET-6). The metric decision stays with `cyp450_inhibition_aid1851` (fallback `roc_auc` proposed there).
- Reject check (AI, 2026-11-25): stands, on the file rather than on the registry's word. Dataverse 4259582
  re-downloaded 2026-11-25 hashes to the registry's `download_sha256` (4c85a4ce…85565a), and TabBench-Bio's own
  pipeline re-run on it returns 12,300 molecules in 7,867 scaffold groups, the registry's numbers exactly: the build
  is this file's 12,328 rows deduplicated on the canonical parent structure and ECFP4-encoded, with no compound, no
  label and no question added, and the file is TDC's binarised 3A4 cut of the deposit `cyp450_inhibition_aid1851`
  already records for all five isozymes (PROV-6). That record names the first publication, keeps the SMILES and stands
  (`TBD -> Yes`, priority 4), so the better copy survives; which isozyme ships stays its open point, and this build
  adds nothing to it — the AC50 curves and the four other isozymes are in AID 1851, not in a 3A4 fingerprint table.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 12,300 x 2,048; target: Y.
- Why: Whether a compound inhibits CYP3A4 (PubChem AID 1851 screen) from 2048-bit ECFP4 fingerprints
- Notes: TDC ADMET task; scaffold-grouped CV.
