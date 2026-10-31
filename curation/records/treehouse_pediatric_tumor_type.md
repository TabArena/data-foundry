---
unique_name: treehouse_pediatric_tumor_type
name: 'Treehouse Tumor Compendium v25.01 PolyA: consistently processed RNA-seq from 13,359 tumours, GEO GSE294351'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Other
year: '2025'
domain: medical & healthcare
problem_type: Multiclass Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.1038/s41597-025-05376-z
- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE294351
- https://treehousegenomics.soe.ucsc.edu/public-data
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: UCSC Treehouse's PolyA tumour compendium v25.01 (13,359 RNA-seq datasets, 136 harmonised diagnoses, log2(TPM+1) per sample, GEO GSE294351), whose 3,477 paediatric and young-adult tumours give a diagnosis task for childhood cancers; 73% of the compendium is TCGA, which the TCGA records cover.
- Source: Beale et al. (UCSC Treehouse Childhood Cancer Initiative), "Consistently processed RNA sequencing data from 50 sources enriched for pediatric data", Scientific Data 12:1134 (2025, 10.1038/s41597-025-05376-z); GEO GSE294351 (expected counts, log2 TPM over 58,581 genes, a clinical table). The clinical table (read in full, 13,359 rows): `th_dataset_id`, `age_at_dx`, `disease` (136 values here, 192 across the five compendia), `icd_disease`, `pedaya`, `sex`, `study_id`, `study_donor_id`, `source_name`; TCGA 9,806 and TARGET 1,340 datasets, 42 studies, 13,224 donors (up to 7 datasets per donor). The descriptor de-duplicates technical replicates and gives expression "in units of log2(TPM + 1)".
- Use case: a molecular tumour board or pathologist confirms or revises a childhood tumour's diagnosis from its expression profile (the descriptor: the compendia have been used "to infer molecular diagnosis"; Comitani et al., Nat Med 29:656, 2023, built such a classifier); fit approximate, since tumours of settled diagnosis stand in for the uncertain case. Regime grouped: each diagnosis comes mostly from one or two studies (neuroblastoma 169 of 217 paediatric from TARGET, Ewing sarcoma 62 of 89 from one study), so the study is a batch to check and the donor a group (SPLIT-3).
- Siblings and duplicates: `srbct_prediction` (`No`, `Trivial` and `Too Small`; Khan 2001, 83 samples) is the record it was found for; its classes here: neuroblastoma 221, Ewing sarcoma 101, rhabdomyosarcoma 193 (embryonal 95, alveolar 73, others 25), and no Burkitt lymphoma, so the four-class task cannot be rebuilt as it was. The TCGA part re-processes the tumours of `tcga_pancancer_tumor_type` and `tcga_lung_histology` (PROV-6 if both ship the same task); the paediatric cut (`pedaya` yes: 3,477 tumours, 111 diagnoses, 16 with at least 30) is a distinct task (PROV-7). Related: `target_pediatric_relapse_transcriptome` (TARGET, another target), `cns_tumor_methylation_classification` (diagnosis from methylation). External collections: none found.
- Better data: found as better data for `srbct_prediction`.
- Papers and pages: Beale et al. 2025 (PMC12222803); https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE294351; treehousegenomics.soe.ucsc.edu/public-data; Comitani et al. 2023.
- Metric: none found (the descriptor releases data and trains no classifier), so the fallback `log_loss`; inputs: `study_id` and `study_donor_id` as groups, never features.
- Risks for /add-dataset: diagnosis confounded with study (a batch shortcut, and a split by study removes whole classes from training: the grouping is a curator call); rare diagnoses below the floor (merge or drop, TP-5, TP-8); labels harmonised over 42 studies (check the merged classes, USE-5); per-sample log2(TPM+1), so no cohort-wide scaling (LEAK-30 holds); about 58,600 genes; overlap with the TCGA records if the whole compendium ships.
- Priority: gap + (multiclass is thin), use case 0 (named for research, no actor and decision), source + (a data descriptor and a GEO deposit), shape + (3,477 paediatric tumours with age, sex and study ids, grouped), risk - (study confounding, overlap with the TCGA records).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `srbct_prediction`.
- as published: 13,359 tumour RNA-seq datasets from 42 studies (TARGET, TCGA, Treehouse clinical sites, others), 58,581 genes as log2(TPM+1); metadata per sample: harmonized disease (192 values), ICD-O code, age at ...; target: tumour diagnosis (disease); for the SRBCT task, the subset neuroblastoma / Ewing sarcoma / rhabdomyosarcoma (embryonal, alveolar) / Burkitt lymphoma, or all ...; access: open (GEO, no access restrictions).
- Why: same task as srbct_prediction (diagnostic category of a pediatric tumour from its gene-expression profile), same feature kind (per-gene expression per sample), uniformly processed and traceable to a data descriptor
- Adds: RNA-seq instead of a 2001 cDNA array, open GEO deposit instead of an OpenML copy without original deposition, and far more tumours (counts per SRBCT class not verified: they are in the 169 KB clinical TSV, not downloaded); risks: study and site batch effects (group by study_id), TPM per sample so no cohort-wide scaling
