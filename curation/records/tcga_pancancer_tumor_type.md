---
unique_name: tcga_pancancer_tumor_type
name: 'TCGA PanCancer Atlas: Cell-of-Origin Patterns Dominate the Molecular Classification of 10,000 Tumors from 33 Types of Cancer'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
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
needs_review:
- ai_unverified
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
