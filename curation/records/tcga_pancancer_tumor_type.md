---
unique_name: tcga_pancancer_tumor_type
name: 'TCGA PanCancer Atlas: Cell-of-Origin Patterns Dominate the Molecular Classification of 10,000 Tumors from 33 Types of Cancer'
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
decision_markers:
- Class-dependent Recording
tags:
- AI-Filled (Verify)
original_source: GOV Website
year: '2018'
domain: medical & healthcare
problem_type: Multiclass Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.1016/j.cell.2018.03.022
- https://gdc.cancer.gov/about-data/publications/pancanatlas
- https://portal.gdc.cancer.gov/
v2_path: datasets/_dev/tabarena-v0pt2/tcga_pancancer_tumor_type/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the TCGA PanCanAtlas, about 10,000 primary tumours of 33 cancer types with RNA-seq, for the tissue-of-origin task of `ova_breast` and `expo_tumor_tissue_of_origin` from another source; the published pan-cancer matrix is batch-adjusted over all samples, so build from the GDC's per-sample files.
- Source: Hoadley et al., "Cell-of-Origin Patterns Dominate the Molecular Classification of 10,000 Tumors from 33 Types of Cancer", Cell 173:291 (2018, 10.1016/j.cell.2018.03.022), the PanCanAtlas flagship; files on the GDC PanCanAtlas page (RNA: EBPlusPlusAdjustPANCAN_IlluminaHiSeq_RNASeqV2.geneExp.tsv; clinical: TCGA-CDR-SupplementalTableS1.xlsx, clinical_PANCAN_patient_with_followup.tsv; merged_sample_quality_annotations.tsv). The harmonised GDC files today (API, 2026-10-31): 11,505 open STAR-Counts files over the 33 TCGA projects, 10,157 primary tumours (plus 151 LAML blood samples), 740 normals, 394 metastatic (most melanomas are metastatic: 103 primary SKCM files). The cancer type is the TCGA project, assigned by pathology at the tissue source site, not a cluster, so SEL-4 does not apply to it.
- Use case: as `expo_tumor_tissue_of_origin`: an oncologist or pathologist identifies the tissue of origin of a cancer of unknown primary from its expression profile to choose a site-specific treatment; the source names no such use (its question is the molecular classification itself); fit approximate, since primary tumours of known origin stand in for metastases of unknown origin. Regime IID (one primary tumour per patient), with the tissue source site checked as a batch.
- Siblings and duplicates: `ova_breast` (`TBD -> Yes`; GEMLeR's one-vs-rest cut of expO) is the record it was found for; `expo_tumor_tissue_of_origin` (`TBD -> Yes`, priority 2) is the same task on expO arrays, another source (PROV-4 does not apply); `gcm_multiclass_cancer` (`TBD -> 2nd Tier`). TCGA cuts of the same tumours for other targets: `tcga_lung_histology`, `tcga_brca_tumor_vs_normal_rnaseq`, `tcga_coad_molecular_subtype`, `tcga_kidney_cancers` (distinct tasks, PROV-7). `treehouse_pediatric_tumor_type` re-processes 9,806 TCGA samples (73% of its compendium), so the two overlap if both ship a tumour-type task over all samples. External collections: none checked.
- Better data: found as better data for `ova_breast`.
- Papers and pages: Hoadley et al. 2018 (PubMed 29625048); https://gdc.cancer.gov/about-data/publications/pancanatlas.
- Metric: none found (the paper clusters with consensus clustering and iCluster and trains no classifier, per its abstract), so the fallback `log_loss`; inputs none.
- Risks for /add-dataset: the EB++ matrix is adjusted over all samples (LEAK-30; build from per-sample GDC files as `tcga_coad_molecular_subtype` does); tissue source site and plate nearly coincide with the cancer type (a batch shortcut to check); the smallest types near the floor (GDC primary tumour files: CHOL 35, DLBC 48, UCS 57; TP-5, TP-8); sex separates the sex-specific types (known at prediction time, to note); expected high accuracy (a TP-4 check); about 60,000 genes.
- Priority: gap + (multiclass is thin), use case 0 (the curation's, as for expO), source + (TCGA, the Cell paper and the GDC), shape + (10,157 primary tumours, 33 classes, clinical fields to join), risk - (adjusted matrix, site batch).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `ova_breast`.
- as published: about 10,000 tumour specimens of 33 cancer types (Cell abstract); RNA-seq of about 20,500 genes per sample (PanCanAtlas file EBPlusPlusAdjustPANCAN_IlluminaHiSeq_RNASeqV2.geneExp.tsv; sample count ...; target: cancer type / tissue of origin (33 classes); access: open (gene expression is open-access tier at GDC).
- Why: Same task as ova_breast (tissue of origin of a tumour from its gene-expression profile); RNA-seq measures the same quantity as the U133 arrays
- Adds: About 5x the samples (vs 1,545), 33 cancer types instead of 9, a newer platform, curated clinical data. Caveats: the tcga_coad_molecular_subtype record warns that the PanCanAtlas batch-corrected matrix uses statistics over all tumours (a leak), so build from GDC per-sample files; tissue source sites may confound the ...

**Assessment (AI, 2026-11-08):** size check for the large-datasets review: 10,308 primary-tumour RNA-seq files of 10,122 patients x 60,660 genes (GDC STAR-Counts, per sample), 33 cancer types; the call stands at priority 3. Treehouse holds 9,806 of the same TCGA samples.
- As published: (1) The PanCanAtlas matrix `EBPlusPlusAdjustPANCAN_IlluminaHiSeq_RNASeqV2.geneExp.tsv` (https://api.gdc.cancer.gov/data/3586c0da-64d0-4b74-a449-5ff4d9136611; 1,882,540,959 bytes by a range request). Its header has 11,069 sample columns from 10,274 patients: sample type 01 (primary solid) 9,706, 03 (primary blood) 173, 06 (metastatic) 395, 11 (normal) 737, 02 46, 05 11, 07 1. The 9,879 primary columns come from 9,875 patients. The gene rows were not counted. The matrix is batch-adjusted over all samples (LEAK-30). (2) The GDC harmonised STAR-Counts (API, 2026-11-08): 11,505 open files over the 33 TCGA projects, 48.74 GB in total. Sample types: Primary Tumor 10,157, Primary Blood Derived Cancer - Peripheral Blood 151 (LAML), Solid Tissue Normal 740, Metastatic 394, Recurrent Tumor 51, Additional - New Primary 11, Additional Metastatic 1. One file (TCGA-CHOL, 4.2 MB) holds 60,660 genes of GENCODE v36 (19,962 protein coding, 16,901 lncRNA) with unstranded and stranded counts, TPM, FPKM and FPKM-UQ per gene, all computed per sample. The clinical table is TCGA-CDR (PanCanAtlas page). The target is the TCGA project.
- The task's table: 10,308 primary files (10,157 solid + 151 blood) of 10,122 patients (computed from the API listing). 147 patients have more than one primary file (several portions or aliquots), so there is one row per patient or a group by patient. Inputs: 60,660 genes (stated in the file; 19,962 protein-coding). Classes: 33 projects; the smallest by patients are CHOL 35, DLBC 48, UCS 57, KICH 66, ACC 79 and UVM 80, the largest BRCA 1,095. SKCM has only 103 primary files, because most TCGA melanomas are metastatic.
- Access: the GDC open-access tier, no login (GDC Data Portal or API). About 44 GB for the primary files (computed from about 4.2 MB per file); the EB++ matrix is 1.9 GB but adjusted over all samples.
- Changes the call: (1) Overlap with `treehouse_pediatric_tumor_type`: Treehouse's compendium holds 9,806 TCGA datasets from 9,733 TCGA patients (TCGA sample codes 01 9,185, 06 392, 03 173, 02 44, 05 11, 07 1; counted in its GEO clinical table), re-quantified with TOIL/RSEM. A pan-cancer type task built on Treehouse would be a version of this one (PROV-6). Treehouse's paediatric cut shares 366 TCGA tumours with this one, under another label (PROV-7). (2) The other TCGA records (`sarcoma`, `tcga_lung_histology`, `tcga_kidney_cancers` and others) are the same tumours with other targets (PROV-7), as the screening said. The priority stays 3.
- Not checked: the EB++ gene count (1.9 GB, only the header was read); the TCGA-CDR join; tissue source site and plate per class (the batch check); the text of the GDC data-use terms.

CC (2026-11-08, Lennart): accepted for adding (`Yes`) in the screening review of the large candidates (most rows, most features).

**Assessment (AI, 2026-11-08):** distinct from treehouse_pediatric_tumor_type, whose paediatric cut holds 366 TCGA tumours: 33 adult TCGA projects against 111 paediatric diagnoses (PROV-7). A tumour-type task over the whole Treehouse compendium would be a version of this one (PROV-6), so only Treehouse's paediatric cut ships.

**Assessment (AI, 2026-11-09):** review panel (full): ship after changes (colon and rectum merged into one colorectal class, the plate batch, the route and the provenance written; no leak, copy or shortcut found; the hidden-group, task and full-width leak probes did not finish, 2,000-gene stand-ins used); disputed: LEAK-13/15/39 (the four BCGSC-only classes); for the curator: issues 1-4. Priority 3: gap + (multiclass thin), use case 0 (the source names cancers of unknown primary only as a potential use; fit approximate), source + (TCGA, GDC, Cell 2018), shape + (9,724 patients x 58,383 genes), risk - (site, plate and sequencing-route batches follow the class).
