---
unique_name: chembl2034_glucocorticoid_receptor
name: CHEMBL2034 (Glucocorticoid Receptor Bioactivity)
checked_by:
- AI (UNVERIFIED)
- Andrej
data_foundry_status:
- WIP (Triage)
claimed_by: Andrej
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
- Many features
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Revised Later'
- 'Entities: Recur'
- Expanding Science Catalogue
collections:
- TabBench-Bio
original_source: Other
domain: chemistry & material science
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.ebi.ac.uk/chembl/explore/target/CHEMBL2034
- https://arxiv.org/abs/2609.07441
- https://github.com/not-a-feature/TabBench-Bio
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-25):** `TBD -> 2nd Tier`, priority 2: 3,127 compounds with a pChEMBL potency on the human
glucocorticoid receptor, the same build and the same open question as `chembl206_estrogen_receptor` — one of many
per-target cuts of ChEMBL. Verdict and priority unchanged; under the catalogue rule (SPLIT-37) the split now reads as
the entry date rather than the scaffold.
- Source: the ChEMBL database (EMBL-EBI), target CHEMBL2034 "Glucocorticoid receptor", SINGLE PROTEIN, Homo sapiens;
  the API returns 6,155 activities carrying a pChEMBL value for it (re-checked 2026-11-25, ChEMBL_37 released
  2026-05-01). The task table is TabBench-Bio's build: "Human single-protein glucocorticoid receptor endpoint, pinned
  to ChEMBL 37. Exact unflagged pChEMBL measurements are canonicalised to parent structures, exact molecules receive
  their median target, and molecules become 2048-bit ECFP4 features grouped by Bemis-Murcko scaffold" (the registry
  `src/tabbench_bio/bio/data/bio_datasets.json`, re-read 2026-11-25); as published by the benchmark: 3,127 molecules
  x 2,048 fingerprint bits, target `pchembl_value` (paper Table 4). ChEMBL itself publishes activities, assays and
  structures as a relational database, not this table.
- Use case: a medicinal chemist, before a compound is made or ordered into an assay, ranks candidates by predicted
  potency on the target; ChEMBL names no actor and no decision, so the use case is ours and the fit is approximate
  (pChEMBL pools IC50, Ki and EC50 from many laboratories and assay formats). Collection: as on
  `chembl206_estrogen_receptor` — the activities enter with the papers that report them, each carrying its document's
  year (`Samples: Over Time`, `Time: Dated`; the first returned activity of this target is a 2003 Ki measurement,
  checked 2026-11-25), a molecule's median is rewritten when a later paper measures it again (`Target: Revised
  Later`), and the source holds several activities per molecule (`Entities: Recur`); type `Expanding Science
  Catalogue` (a bioactivity database's releases, SPLIT-34).
- Split: leaf L-CAT.entry-date (Temporal · entry date) because [CAT.next-items] yes (ChEMBL states no aim or scope of
  its own, SPLIT-37 step 3, and the chemist's question reaches compounds not yet made), [CAT.entry-date] yes (the
  document year dates each activity, and the revised median keys on the year a molecule's last measurement arrives,
  as `papyrus_bioactivity` decided on 2026-11-24), [CAT.arrival] yes on the `qsar_tid_11` measurement of the same
  task (close training analogs first published in the test compound's own year for 71-93% of its scaffold folds), and
  [CAT.windows] 6,155 activities spread over the literature years; open: the (4b) measurement on this target's own
  years, the window length and gap, the share of undated deposited activities (5.3% on CHEMBL206, not counted here),
  and the fallback L-FAMILY.key (the scaffold the benchmark ships) if (4b) reads flat. `required_split` changes from
  Grouped to Temporal with the leaf.
- Siblings and duplicates: `chembl206_estrogen_receptor` is the same build on another target — the curator's note on
  `qsar_tid_10980` ("Same as above, but different drug target. Should only include one of these datasets") says one
  of the two, at most, should enter. `qsar_tid_11` (CHEMBL204, shipped in TabArena v0.1) and `qsar_tid_10980`
  (CHEMBL279) are the same task from ChEMBL 17. Not duplicates under PROV-4 and PROV-5 (different targets, a
  different release); `papyrus_bioactivity` (`Yes`) and `chembl36_kinase_bioactivity` cover the quantity on newer or
  wider cuts (a PROV-6 overlap for the curator). External collections: TabBench-Bio (`CHEMBL2034`).
- Better data: `papyrus_bioactivity` (`Yes`, added as a v2 folder and built): the same pChEMBL quantity over about
  6,900 proteins and 1.27 million compounds. As on `chembl206_estrogen_receptor` it does not settle this record: its
  task is protein-conditioned and its own definition argues under PROV-7 that this differs from fixed-target QSAR,
  its measured ChEMBL overlap is 1,616 ids over 2,257 rows with the sibling overlap unverified, and it sits on
  ChEMBL 34 against this cut's ChEMBL 37. No new hit in a quick look this round.
- Papers and pages: the ChEMBL target page https://www.ebi.ac.uk/chembl/explore/target/CHEMBL2034; TabBench-Bio
  (Kreuer et al., arXiv 2609.07441), Sec. 3.1 and Table 4 row CHEMBL2034.
- Metric: none found at the source: ChEMBL defines no task and no metric (checked 2026-10-31 and 2026-11-25). The
  benchmark's own is "RMSE is the primary regression metric" (Sec. 3.5), which agrees with our fallback `rmse` on
  pChEMBL (MET-5, MET-8). Inputs: the entry year the temporal split orders on, taken from ChEMBL and no model input.
- Risks for /add-dataset: as on `chembl206_estrogen_receptor` — rebuild from ChEMBL keeping the structures and the
  document years rather than taking the benchmark's fingerprints (CLEAN-24); check the "exact unflagged" filter and
  the median-per-parent rule (MET-2); a median later papers revise must be final at a temporal cut (SPLIT-9); mixed
  assay types behind one pChEMBL column; activity cliffs and stereochemistry (LEAK-17); 3,127 rows is the smaller of
  the two cuts; CC BY-SA 3.0, `redistributable: false` in the registry (no verdict reason, EV-4).
- Priority: gap 0 (chemistry & material science has 15 accepted datasets and regression 85, neither thin), use case 0
  (ChEMBL names no decision), source + (a documented database with a pinned release), shape + (3,127 molecules), risk
  - (the near-identical `chembl206_estrogen_receptor`; `qsar_tid_11`, shipped, is the same kind of task on another
  target; `papyrus_bioactivity`, added and built, holds the quantity far wider but on an older release and as a
  protein-conditioned task).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 3,127 x 2,048; target: pchembl_value.
- Why: Potency (pChEMBL) of compounds against the human glucocorticoid receptor from 2048-bit ECFP4 fingerprints (ChEMBL 37)
- Notes: Same build as CHEMBL206.

**CC (2026-11-26, Andrej):** the better-data line is corrected, as on `chembl206_estrogen_receptor`.
- `papyrus_bioactivity` is added as a v2 folder and built, and still does not cover this cut: a protein-conditioned
  task its own definition separates from fixed-target QSAR under PROV-7, on ChEMBL 34 against this cut's ChEMBL 37.
- The priority line had called `qsar_tid_11` and the wider set covering "the task"; both are qualified now.
- Verdict and priority unchanged.

**Assessment (AI, 2026-11-26):** `No` (`Duplicate`, PROV-6): the overlap with the built wider set was measured, and the case for a third fixed-target cut of ChEMBL does not survive it.
- What was measured, on 2026-11-26. The cut was rebuilt from the ChEMBL web service: exact, unflagged activities with a pChEMBL value on glucocorticoid receptor give 3,130 distinct parent molecules, against the 3,127 the benchmark ships, so the reconstruction is the same table. Papyrus2024.2's combined set was filtered to this target's accession (P04150): 6,410 rows, 2,652 of them high quality with an exact relation, carrying 1,725 distinct ChEMBL molecule ids.
- The overlap: 1,382 of the cut's molecules (44.2%) are already in those rows, and 343 molecules are in them and not in the cut.
- What the later releases add: of the 1,748 molecules the cut holds and the wider set does not, only 55 carry their earliest exact measurement in a document of 2024 or later. The rest are compounds the wider set's own standardization dropped, not entries three ChEMBL releases added, so the newer release is worth about 55 molecules here and not a dataset.
- Why `Duplicate` and not a task argument: the wider set's definition separates its protein-conditioned task from fixed-target QSAR under PROV-7, and that stands. The reject is the other call, the one the curator already wrote on `qsar_tid_10980` ("Same as above, but different drug target. Should only include one of these datasets"): these are per-target cuts of one database (PROV-6), the collection already ships one as `qsar_tid_11` and has added the wide set, and a third and fourth cut buy half a table that is already there plus 55 molecules.
- Not checked: whether some of the 1,748 are the same compounds under another id, since the wider set standardizes without stereochemistry while the cut takes a median per parent. That check can only lower the 1,748, never raise it, so it does not change the direction.
