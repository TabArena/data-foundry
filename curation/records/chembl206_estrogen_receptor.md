---
unique_name: chembl206_estrogen_receptor
name: CHEMBL206 (Oestrogen receptor bioactivity)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
- Many features
collections:
- TabBench-Bio
original_source: Other
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
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

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: 4,544 compounds with a pChEMBL potency on human oestrogen receptor alpha, the same kind of task as the shipped `qsar_tid_11`, but one per-target cut of ChEMBL among many and overlapped by two newer candidates of this run.
- Source: the ChEMBL database (EMBL-EBI), target CHEMBL206 "Estrogen receptor", SINGLE PROTEIN, Homo sapiens; the API returns 7,966 activities carrying a pChEMBL value for it (read 2026-10-31, ChEMBL_37, released 2026-05-01). The task table is TabBench-Bio's build: "Human single-protein estrogen receptor endpoint, pinned to ChEMBL 37. Exact unflagged pChEMBL measurements are canonicalised to parent structures, exact molecules receive their median target, and molecules become 2048-bit ECFP4 features grouped by Bemis-Murcko scaffold" (the registry `src/tabbench_bio/bio/data/bio_datasets.json`, read 2026-10-31); as published by the benchmark: 4,544 molecules x 2,048 fingerprint bits, target `pchembl_value` (paper Table 4). ChEMBL itself publishes activities, assays and structures as a relational database, not this table.
- Use case: a medicinal chemist, before a compound is made or ordered into an assay, ranks candidates by predicted potency on the target; ChEMBL names no actor and no decision, so the use case is ours and the fit is approximate (pChEMBL pools IC50, Ki and EC50 from many laboratories and assay formats). Regime grouped on the Bemis-Murcko scaffold (SPLIT-31 as amended 2026-10-26; the benchmark groups the same way).
- Siblings and duplicates: `qsar_tid_11` (MetaQSAR, ChEMBL 17, target CHEMBL204, 1,024-bit FCFP, shipped in TabArena v0.1) and `qsar_tid_10980` (CHEMBL279) are the same task on other targets; the curator's note on the second is "Same as above, but different drug target. Should only include one of these datasets", which bears on this record and on `chembl2034_glucocorticoid_receptor` (the same build, 3,127 compounds). Not duplicates under PROV-4 and PROV-5: different targets and a different ChEMBL release. `papyrus_bioactivity` (ChEMBL 34 plus other sources, about 6,900 targets, with structures and quality flags) and `chembl36_kinase_bioactivity` (ChEMBL 36, 507 kinases), both candidates of this run, hold the same quantity on newer or wider cuts, a PROV-6 overlap for the curator to settle. `astrazeneca_chembl_logd74` is another ChEMBL deposition but a physicochemical endpoint, a distinct task (PROV-7). External collections: TabBench-Bio (`CHEMBL206`).
- Better data: a candidate of the benchmark TabBench-Bio; no new search this round.
- Papers and pages: the ChEMBL target page https://www.ebi.ac.uk/chembl/explore/target/CHEMBL206; TabBench-Bio (Kreuer et al., arXiv 2609.07441), Sec. 3.1 "For the ChEMBL tasks, we use exact, unflagged activity measurements" with "Bemis-Murcko scaffolds as split groups", Table 4 row CHEMBL206.
- Metric: none found at the source: ChEMBL defines no task and no metric (its target page and API return data only, checked 2026-10-31). The only metric this table has is the benchmark's own, "RMSE is the primary regression metric" (TabBench-Bio Sec. 3.5), which agrees with our fallback `rmse` on pChEMBL (MET-5, MET-8). Inputs: none beyond the scaffold group a grouped split needs (the benchmark ships it; a rebuild computes it from the SMILES).
- Risks for /add-dataset: the fingerprints are the benchmark's own ECFP4 build, so rebuild from ChEMBL and keep the structures (CLEAN-24, as on `astrazeneca_chembl_logd74`); check what "exact unflagged" and the median-per-parent rule drop, and how much IC50/Ki/EC50 mixing survives in the target (MET-2); activity cliffs and stereoisomers collapsing onto one 2D fingerprint (LEAK-17); ChEMBL's licence is CC BY-SA 3.0 and the registry marks the built table `redistributable: false` (no verdict reason, EV-4).
- Priority: gap 0 (chemistry & material science and regression are not thin), use case 0 (ChEMBL names no decision), source + (a documented database, a pinned release, per-activity provenance), shape + (4,544 molecules), risk - (the same task is already in the benchmark as `qsar_tid_11`, and two newer candidates of this run cover it).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 4,544 x 2,048; target: pchembl_value.
- Why: Potency (pChEMBL) of compounds against human estrogen receptor alpha from 2048-bit ECFP4 fingerprints (ChEMBL 37, exact unflagged values, median per parent molecule)
- Notes: Built by the authors from ChEMBL 37 (CC BY-SA 3.0); scaffold-grouped CV. Same kind of task as qsar_tid_11 / qsar_tid_10980 (MetaQSAR, ChEMBL 17, 1,024-bit FCFP); whether either is the same target was not settled.
