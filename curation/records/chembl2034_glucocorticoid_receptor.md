---
unique_name: chembl2034_glucocorticoid_receptor
name: CHEMBL2034 (Glucocorticoid Receptor Bioactivity)
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Andrej
suggestion: TBD -> 2nd Tier
priority: 2
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
- Better data: `papyrus_bioactivity` (recorded, `Yes`): the same pChEMBL quantity over about 6,900 proteins and 1.27
  million compounds. No new hit in a quick look this round.
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
  - (the near-identical `chembl206_estrogen_receptor`, the shipped `qsar_tid_11`, and the accepted
  `papyrus_bioactivity` cover the task).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 3,127 x 2,048; target: pchembl_value.
- Why: Potency (pChEMBL) of compounds against the human glucocorticoid receptor from 2048-bit ECFP4 fingerprints (ChEMBL 37)
- Notes: Same build as CHEMBL206.
