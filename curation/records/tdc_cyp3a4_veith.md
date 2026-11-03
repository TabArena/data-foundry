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

**Screening (AI, 2026-10-31):** `No` (`Duplicate`, PROV-4): TabBench-Bio's 2,048-bit ECFP4 build of TDC's CYP3A4_Veith file (Harvard Dataverse 4259582), the 3A4 cut of PubChem AID 1851 (Veith et al. 2009), which `cyp450_inhibition_aid1851` already records with all five isozymes; one isozyme of the same deposit adds no distinct task (PROV-6).
- Source: Veith, Southall, Huang et al. 2009, "Comprehensive characterization of cytochrome P450 isozyme selectivity across chemical libraries", Nat Biotechnol 27:1050 (doi 10.1038/nbt.1581, online 2009-10-25), deposited as PubChem AID 1851; served by TDC as CYP3A4_Veith ("12,328 drugs", tdcommons.ai/single_pred_tasks/adme) from Dataverse file 4259582 (tdc/metadata.py); header previewed: `Drug_ID` (PubChem CID), `Drug` (SMILES), `Y`. TabBench-Bio registry (github.com/not-a-feature/TabBench-Bio, src/tabbench_bio/bio/data/bio_datasets.json, read 2026-10-31), `TDC-CYP3A4-Veith`: "Validated official Harvard Dataverse file 4259582. Canonical parent structures, exact-molecule deduplication, 2048-bit ECFP4, grouped by Bemis-Murcko scaffold. Quality pass: 12300 molecules, 2048 features, 7867 groups; 1 invalid and 1 conflicting molecule dropped".
- Use case: as on `cyp450_inhibition_aid1851`: a medicinal chemist flags a compound's drug-drug-interaction liability before synthesis or the in-vitro CYP panel; regime grouped on the Bemis-Murcko scaffold (SPLIT-31).
- Siblings and duplicates: `cyp450_inhibition_aid1851` (ChemPile; `TBD -> Yes`, priority 4) covers the five isozymes of AID 1851, 3A4 included (config `cyp_p450_3a4_inhibition_veith_et_al`, TDC 3A4 12,328), and its screening already says this record "is the same screen reached through TDC, so both records end at AID 1851 and one of them is a `Duplicate` (PROV-4, PROV-5)", with itself as the one that names the first publication: the survivor. Which isozyme ships is that record's open point. `cyp_substrates_carbon_mangels` (substrates, not inhibitors) is distinct (PROV-7). External collections: TabBench-Bio (Kreuer et al., arXiv 2609.07441v2, 2026-09-26, Table 4), TDC ADMET benchmark group, ChemPile.
- Better data: a candidate of the benchmark TabBench-Bio; no further search this round.
- Papers and pages: Veith et al. 2009 (PMC2783980); PubChem AID 1851; TDC's ADME page and ADMET benchmark group; the TabBench-Bio paper and registry.
- Metric: TDC's ADMET group scores CYP3A4_Veith by AUPRC on a scaffold split (tdcommons.ai/benchmark/admet_group/overview, "AUPRC is used when the number of positive samples are much smaller than negative samples", the imbalance argument MET-9 rejects); TabBench-Bio scores every classification task by "Macro-F1 is the primary classification metric" (Sec. 3.5), a benchmark-wide default with no threshold fixed (MET-6), with AUROC as a re-ranking in its Appendix E. The metric decision stays with `cyp450_inhibition_aid1851` (fallback `roc_auc` proposed there).
- Reject check (AI, 2026-10-31): stands. Registry: 'Validated official Harvard Dataverse file 4259582', citation Veith et al. 2009 (https://raw.githubusercontent.com/not-a-feature/TabBench-Bio/main/src/tabbench_bio/bio/data/bio_datasets.json); TDC maps 'cyp3a4_veith': 4259582 (tdc/metadata.py, checked). `cyp450_inhibition_aid1851` already holds this isozyme as config cyp_p450_3a4_inhibition_veith_et_al of AID 1851, so the 3A4 task is recorded there, not lost; which isozymes ship is that record's open point.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 12,300 x 2,048; target: Y.
- Why: Whether a compound inhibits CYP3A4 (PubChem AID 1851 screen) from 2048-bit ECFP4 fingerprints
- Notes: TDC ADMET task; scaffold-grouped CV.
