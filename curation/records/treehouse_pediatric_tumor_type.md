---
unique_name: treehouse_pediatric_tumor_type
name: 'Treehouse Tumor Compendium v25.01 PolyA: consistently processed RNA-seq from 13,359 tumours, GEO GSE294351'
checked_by:
- Lennart
data_foundry_status:
- WIP (Triage)
claimed_by: Lennart
suggestion: 'Yes'
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

**Assessment (AI, 2026-11-08):** size check for the large-datasets review: the paediatric and young-adult cut, 3,477 RNA-seq datasets of 3,229 donors x 58,581 genes (log2 TPM+1) plus age and sex, with 111 diagnoses, 27 of them with 10 or more donors; the call stands at priority 3. 366 of the cut's datasets are TCGA tumours.
- As published: GEO GSE294351 (public 2025-04-18; https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE294351): "13359 consistently processed gene expression datasets from 42 studies", quantified with TOIL (RSEM 1.2.25, STAR 2.4.2a, GRCh38, GENCODE 23; overall design). The files are `GSE294351_Tumor-25.01-Polya_hugo_log2tpm_58581genes_2025-02-27.tsv.gz` (1.3 GB; 58,581 HUGO genes, log2(TPM+1)), `GSE294351_Tumor-25.01-Polya_ensembl_counts_60498genes_2025-03-03.tsv.gz` (1.2 GB; 60,498 Ensembl genes, RSEM expected counts) and the clinical TSV (169 KB, read in full): 13,359 rows x 12 columns (`th_dataset_id`, `age_at_dx`, `disease`, `icd_disease`, `organism`, `pedaya`, `sex`, `study_accession`, `study_dataset_id`, `study_donor_id`, `study_id`, `source_name`). The sources are TCGA 9,806, TARGET 1,340, Sequence Read Archive 713, St. Jude Cloud 708, EGA 202 and unavailable 452. `pedaya` is yes for 3,477, no for 9,621 and unknown for 261. The join is the expression columns to `th_dataset_id`. No QC subset of genes is named.
- The task's table: the `pedaya` cut has 3,477 rows (datasets) from 3,229 donors. The donor is `study_id` + `study_donor_id`, or the TH prefix where the donor id is unavailable (computed). 220 donors have more than one dataset (up to 7), so group by donor. Inputs: 58,581 genes + `age_at_dx` + `sex` (sex unavailable for 326) = 58,583. Classes: 111 diagnoses. 16 have 30 or more donors (3,060 datasets) and 27 have 10 or more (3,264 datasets; the smallest of these are hepatocellular carcinoma 17, dysembryoplastic neuroepithelial tumour 13, hepatoblastoma 12, synovial sarcoma 11 and breast invasive carcinoma 10). 71 diagnoses have fewer than 5 datasets. The largest are acute lymphoblastic leukaemia 880, acute myeloid leukaemia 452, glioma 348, osteosarcoma 220 and neuroblastoma 217 (all computed from the clinical table).
- Access: open on GEO, no login. GEO says the authors "released the expression values and metadata without access restrictions"; no licence is named. 1.3 GB for the TPM matrix of all 13,359 datasets; the paediatric columns are cut after the download.
- Changes the call: (1) Overlap with TCGA: 9,806 of the 13,359 datasets are TCGA (9,733 patients), the same tumours as `tcga_pancancer_tumor_type`. The paediatric cut holds 366 TCGA datasets (among them glioma 88, thyroid carcinoma 67, testicular germ cell tumour 61, cervical 22, pheochromocytoma and paraganglioma 22, melanoma 21) and 1,337 TARGET datasets; TARGET is also the source of `target_pediatric_relapse_transcriptome`, another target. These are distinct tasks (PROV-7). A tumour-type task over the whole compendium would be a version of the TCGA one (PROV-6). (2) Study confounding: of the 16 diagnoses with 30 or more donors, 5 come 90% or more from one study (Wilms tumour 0.91, thyroid carcinoma 0.94, rhabdoid tumour 0.96, testicular germ cell tumour 0.98, acute megakaryoblastic leukaemia 0.99). A split by study would remove these classes from training. Grouping by donor is the minimum (SPLIT-3), and the study grouping is the curator's call, as the screening said. The priority stays 3.
- Not checked: the TPM matrix itself (1.3 GB, not downloaded; the gene count comes from its file name); whether the 9,806 TCGA datasets are de-duplicated against TCGA aliquots as the descriptor says; the harmonised disease merges (USE-5).

CC (2026-11-08, Lennart): accepted for adding (`Yes`) in the screening review of the large candidates (most rows, most features).

**Assessment (AI, 2026-11-08):** distinct from tcga_pancancer_tumor_type (PROV-7): only the paediatric cut ships (3,477 datasets, 366 of them TCGA tumours); the whole compendium would be a version of the TCGA task (PROV-6).
