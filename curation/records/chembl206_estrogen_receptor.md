---
unique_name: chembl206_estrogen_receptor
name: CHEMBL206 (Oestrogen receptor bioactivity)
checked_by:
- AI (UNVERIFIED)
- Andrej
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
- https://www.ebi.ac.uk/chembl/explore/target/CHEMBL206
- https://arxiv.org/abs/2609.07441
- https://github.com/not-a-feature/TabBench-Bio
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-25):** `TBD -> 2nd Tier`, priority 2: 4,544 compounds with a pChEMBL potency on human
oestrogen receptor alpha, the same kind of task as the shipped `qsar_tid_11`, but one per-target cut of ChEMBL among
many, and `papyrus_bioactivity` (accepted since) holds the same quantity far wider. Verdict and priority unchanged;
under the catalogue rule (SPLIT-37) the split now reads as the entry date rather than the scaffold.
- Source: the ChEMBL database (EMBL-EBI), target CHEMBL206 "Estrogen receptor", SINGLE PROTEIN, Homo sapiens; the API
  returns 7,966 activities carrying a pChEMBL value for it (re-checked 2026-11-25, ChEMBL_37 released 2026-05-01), of
  which 423 (5.3%) sit in documents with no year (deposited data sets such as CHEMBL1201862). The task table is
  TabBench-Bio's build: "Human single-protein estrogen receptor endpoint, pinned to ChEMBL 37. Exact unflagged
  pChEMBL measurements are canonicalised to parent structures, exact molecules receive their median target, and
  molecules become 2048-bit ECFP4 features grouped by Bemis-Murcko scaffold" (the registry
  `src/tabbench_bio/bio/data/bio_datasets.json`, re-read 2026-11-25); as published by the benchmark: 4,544 molecules
  x 2,048 fingerprint bits, target `pchembl_value` (paper Table 4). ChEMBL itself publishes activities, assays and
  structures as a relational database, not this table.
- Use case: a medicinal chemist, before a compound is made or ordered into an assay, ranks candidates by predicted
  potency on the target; ChEMBL names no actor and no decision, so the use case is ours and the fit is approximate
  (pChEMBL pools IC50, Ki and EC50 from many laboratories and assay formats). Collection: the activities enter with
  the papers that report them, each carrying its document's year (`Samples: Over Time`, `Time: Dated`:
  `document_year` on the activity record, checked on the API 2026-11-25), a molecule's median is rewritten when a
  later paper measures it again (`Target: Revised Later`), and the source holds several activities per molecule
  (`Entities: Recur`; the build takes the median per parent structure, so the table has one row each); type
  `Expanding Science Catalogue` (a bioactivity database's releases, SPLIT-34).
- Split: leaf L-CAT.entry-date (Temporal · entry date) because [CAT.next-items] yes (ChEMBL states no aim or scope of
  its own, SPLIT-37 step 3, and the chemist's question reaches compounds not yet made), [CAT.entry-date] yes (each
  activity carries its document year, so a molecule's entry year is rebuildable from the parent source; as the median
  is revised, the key is the year the molecule's last measurement arrives, the decision `papyrus_bioactivity` took on
  2026-11-24, not its first), [CAT.arrival] yes on the measurement for this very task on `qsar_tid_11` (close
  training analogs first published in the test compound's own year for 71-93% of its scaffold folds; predicting each
  period from the earlier ones raises RMSE from 0.80-1.04 to 0.89-1.50), and [CAT.windows] the document years run
  from 1999 to the release over 7,966 activities; open: the (4b) measurement on this target's own years, the window
  length and gap, where the 423 undated activities go (`papyrus_bioactivity` gave its undated rows the earliest
  year), and the fallback L-FAMILY.key (the Bemis-Murcko scaffold, which the benchmark ships) if (4b) reads flat
  here. `required_split` changes from Grouped to Temporal with the leaf.
- Siblings and duplicates: `qsar_tid_11` (MetaQSAR, ChEMBL 17, target CHEMBL204, 1,024-bit FCFP, shipped in TabArena
  v0.1) and `qsar_tid_10980` (CHEMBL279) are the same task on other targets; the curator's note on the second is
  "Same as above, but different drug target. Should only include one of these datasets", which bears on this record
  and on `chembl2034_glucocorticoid_receptor` (the same build, 3,127 compounds). Not duplicates under PROV-4 and
  PROV-5: different targets and a different ChEMBL release. `papyrus_bioactivity` (ChEMBL 34 plus other sources,
  about 6,900 proteins; `Yes` since this record was first screened) and `chembl36_kinase_bioactivity` (ChEMBL 36, 507
  kinases) hold the same quantity on newer or wider cuts, a PROV-6 overlap for the curator to settle.
  `astrazeneca_chembl_logd74` is another ChEMBL deposition but a physicochemical endpoint, a distinct task (PROV-7).
  External collections: TabBench-Bio (`CHEMBL206`).
- Better data: `papyrus_bioactivity` (`Yes`, added as a v2 folder and built): the same pChEMBL quantity on 1.27
  million compounds and about 6,900 proteins, with this target's activities among them, split on the entry year
  since 2026-11-24. It does not settle this record, for two reasons its own definition gives: the task it ships is
  protein-conditioned, the protein being an input, which it argues under PROV-7 differs from fixed-target QSAR ("no
  legacy QSAR task is changed"), and its measured ChEMBL overlap is 1,616 ids over 2,257 rows with the sibling
  overlap left unverified. It also sits on ChEMBL 34 while this cut is ChEMBL 37, so the newest entries, the ones a
  temporal split tests on, are here and not there. What would settle it is measurable: how many of these 4,544
  compounds already sit in its rows, and what the three later releases add. No new hit in a quick look this round.
- Papers and pages: the ChEMBL target page https://www.ebi.ac.uk/chembl/explore/target/CHEMBL206; TabBench-Bio
  (Kreuer et al., arXiv 2609.07441), Sec. 3.1 "For the ChEMBL tasks, we use exact, unflagged activity measurements"
  with "Bemis-Murcko scaffolds as split groups", Table 4 row CHEMBL206.
- Metric: none found at the source: ChEMBL defines no task and no metric (its target page and API return data only,
  checked 2026-10-31 and 2026-11-25). The only metric this table has is the benchmark's own, "RMSE is the primary
  regression metric" (TabBench-Bio Sec. 3.5), which agrees with our fallback `rmse` on pChEMBL (MET-5, MET-8).
  Inputs: the entry year the temporal split orders on, which this table does not ship and a rebuild takes from
  ChEMBL; it is no model input.
- Risks for /add-dataset: the fingerprints are the benchmark's own ECFP4 build, so rebuild from ChEMBL and keep the
  structures (CLEAN-24, as on `astrazeneca_chembl_logd74`) and the document years with them; check what "exact
  unflagged" and the median-per-parent rule drop, and how much IC50/Ki/EC50 mixing survives in the target (MET-2); a
  median that later papers revise must be final at a temporal cut (SPLIT-9); activity cliffs and stereoisomers
  collapsing onto one 2D fingerprint (LEAK-17); ChEMBL's licence is CC BY-SA 3.0 and the registry marks the built
  table `redistributable: false` (no verdict reason, EV-4).
- Priority: gap 0 (chemistry & material science has 15 accepted datasets and regression 85, neither thin), use case 0
  (ChEMBL names no decision), source + (a documented database, a pinned release, per-activity provenance), shape +
  (4,544 molecules), risk - (`qsar_tid_11`, shipped, is the same kind of task on another target, thrombin, and
  `papyrus_bioactivity`, added and built, holds the quantity far wider, though on an older release and as a
  protein-conditioned task).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 4,544 x 2,048; target: pchembl_value.
- Why: Potency (pChEMBL) of compounds against human estrogen receptor alpha from 2048-bit ECFP4 fingerprints (ChEMBL 37, exact unflagged values, median per parent molecule)
- Notes: Built by the authors from ChEMBL 37 (CC BY-SA 3.0); scaffold-grouped CV. Same kind of task as qsar_tid_11 / qsar_tid_10980 (MetaQSAR, ChEMBL 17, 1,024-bit FCFP); whether either is the same target was not settled.

**CC (2026-11-26, Andrej):** the better-data line is corrected.
- `papyrus_bioactivity` is added as a v2 folder and built, not only recorded, but it does not cover this cut: its
  task is protein-conditioned and its own definition argues under PROV-7 that this differs from fixed-target QSAR,
  its measured ChEMBL overlap is 1,616 ids over 2,257 rows, and it sits on ChEMBL 34 against this cut's ChEMBL 37.
- The priority line had called `qsar_tid_11` "the same task"; it is the same kind of task on another target,
  thrombin (CHEMBL204).
- Verdict and priority unchanged. What would settle the record is one measurement: how many of these 4,544
  compounds are already in the wider set's rows, and what the three later releases add.
