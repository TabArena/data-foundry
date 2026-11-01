---
unique_name: chembl_antimicrobial_activity
name: Antimicrobial binary ML tasks from ChEMBL (Ersilia chembl-antimicrobial-tasks)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: Other
domain: chemistry & material science
problem_type: Binary Classification
source_links:
- https://github.com/ersilia-os/chembl-antimicrobial-tasks
- https://github.com/ersilia-os/chembl-binary-tasks
- https://www.ebi.ac.uk/chembl/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: a GitHub pipeline (Ersilia) that cuts ChEMBL into per-pathogen, per-assay binary activity sets for 15 pathogens; real measured bioactivity, but a collection to cut rather than one task, with sets selected and pooled by the pipeline's own models, no paper and no stated sizes.
- Source: the data is ChEMBL (EMBL-EBI), each activity from the assay of a primary publication; the cut is the Ersilia Open Source Initiative's `chembl-antimicrobial-tasks` (GitHub, GPL-3.0, 235 commits; no paper and no ChEMBL release named in the README), the successor of `chembl-binary-tasks` ("IMPORTANT: THIS REPOSITORY IS THE OLD VERSION OF chembl-antimicrobial-tasks"). README: "For each pathogen it selects high-quality assays, binarizes measurements against expert-defined cutoffs", "pools related datasets to maximise usable chemical space" and "trains baseline models to assess dataset quality". As published (`docs/dataset_access_guide.md`): files `{assay_id}_{activity_type}_{type}_{cutoff}.csv.gz` with the columns `smiles`, `bin`, `compound_chembl_id`, zipped by type (quantitative, qualitative, mixed) plus merged sets; a selection table `18_final_datasets.csv` with `activity_type`, `unit`, `target_type`, `cutoff`, `auroc`, `cpds`, `positives`, `selected`; the files come through Ersilia's `eosvc` tool or a rerun of the pipeline (stage 1 "~4–5 h"). The old repository's floors: `MIN_SIZE_ASSAY_TASK = 1000` for organism assays, `MIN_COUNT_POSITIVE_CASES = 30`. Pathogens: A. baumannii, C. albicans, Campylobacter, E. coli, E. faecium, Enterobacter, H. pylori, K. pneumoniae, M. tuberculosis, N. gonorrhoeae, P. aeruginosa, P. falciparum, S. aureus, S. mansoni, S. pneumoniae. Sizes per set are not stated.
- Use case: a medicinal chemist in an antibacterial or antimalarial programme ranks candidate compounds by predicted whole-cell activity before ordering or testing them; the pipeline names the ML use, not the actor or the decision, so the fit is approximate, and direct only for a single primary whole-cell screen. Regime IID as the QSAR records (one row per compound), with scaffold structure to note at the add stage.
- Siblings and duplicates: no record holds an antimicrobial ChEMBL cut (grep by ChEMBL, Ersilia and the pathogen names). Other ChEMBL cuts: `chembl36_kinase_bioactivity` (TBD -> Yes, kinase potencies), `papyrus_bioactivity` (run candidate), the QSAR-TID records (`qsar_tid_11` and siblings, shipped), `nura_nuclear_receptor_activity`: other targets, distinct tasks (PROV-7). Related: `nci_aids_antiviral_screen` (a primary screen with an expert conclusion, the shape to follow), `mycobacterium_tuberculosis_drug_data` (No), and the resistance records `cryptic_mtb_drug_resistance`, `driams_antimicrobial_resistance`, `amr_uti_antibiotic_resistance` (resistance of isolates, not compound activity). External collections: none found on the pages read.
- Better data: from the curator's Zotero collection (item 192, "ChEMBL Binary Tasks"); no further search this round. The run's note stands: a record should take one primary ChEMBL assay (a large M. tuberculosis or P. falciparum whole-cell screen) as its source (PROV-8).
- Papers and pages: the READMEs of both Ersilia repositories and the dataset access guide; no paper found for either.
- Metric: no task source; the pipeline scores its baseline models by AUROC (the `auroc` column of the selection table, used to judge "dataset quality"), which is also the fallback, so `roc_auc` (MET-1, MET-5, MET-8); inputs none.
- Risks for /add-dataset: which set to take; the pipeline keeps sets by its own models (the `selected` flag; the criteria are not stated), a selection on learnability that inflates any benchmark score; merged sets pool assays with different protocols and cutoffs; the cutoffs (10, 5 and 50 in the guide's examples) are the pipeline's, binarising a measured value we could ship as a regression instead (USE-5); only SMILES ship, so the features are computed (CLEAN-24); the selection table's `auroc` is a pipeline output, never a feature. Prefer rebuilding one primary assay from ChEMBL directly (PROV-8, PROV-11).
- Priority: gap 0 (chemistry, binary and IID are covered), use case 0 (the pipeline names the ML use, not the decision), source + (ChEMBL and its primary assays), shape 0 (sizes not stated), risk - (sets selected and pooled by the pipeline's own models).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 192: "ChEMBL Binary Tasks".
- as published: per-pathogen datasets for 15 pathogens (smiles, bin, compound_chembl_id; whole-cell and protein assays); row counts not stated in the README; target: compound active against the pathogen, from measured activity (e.g. MIC, IC50) binarised at expert cutoffs (default 10 uM); access: open.
- Why: real measured bioactivity for neglected and AMR pathogens, a task Ersilia builds models for
- Adds: no antimicrobial QSAR record. Caveats: the pipeline keeps datasets on its own model's AUROC > 0.70 and pools assays by fit (selection bias), so a record should take one primary ChEMBL assay (e.g. a large M. tuberculosis or P. falciparum whole-cell screen) as its source (PROV-8)
