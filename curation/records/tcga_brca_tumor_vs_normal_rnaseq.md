---
unique_name: tcga_brca_tumor_vs_normal_rnaseq
name: TCGA-TCGA-BRCA_Gene-Expression-Quantification (TCGA Breast, RNA-seq)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
- Many features
collections:
- TabBench-Bio
original_source: GOV Website
year: '2012'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
source_links:
- https://doi.org/10.1038/nature11412
- https://portal.gdc.cancer.gov/projects/TCGA-BRCA
- https://arxiv.org/abs/2609.07441
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: primary breast tumour against adjacent normal tissue from TCGA-BRCA RNA-seq on the GDC (1,231 samples of 1,098 patients); a strong source, but the target is the specimen's sample type, which the sampler sets, and the task is expected to be near-perfectly separable.
- Source: The Cancer Genome Atlas Network, "Comprehensive molecular portraits of human breast tumours", Nature 490:61-70 (2012; doi 10.1038/nature11412); data on the NCI GDC (TCGA-BRCA), harmonised STAR-Counts per sample (TPM, GENCODE v36). GDC API, 2026-10-31: 1,231 open STAR-Counts files, 1,111 primary tumour, 113 solid tissue normal and 7 metastatic, over 1,098 cases. As TabBench-Bio ships it: 1,231 x 60,660 TPM values, target `sample_type` with the metastatic samples counted as tumour (about 1,118 / 113).
- Use case: unclear. The sample type records where the surgeon took the tissue, and nobody predicts it. A steelman is a molecular check that a specimen holds tumour (a margin or biobank check), where pathology decides today; the normals are tissue next to a tumour of the same patients, not healthy breasts. The data was collected for molecular characterisation (SEL-8). Fit approximate at best (USE-8); regime grouped by patient, since the normals mostly have a tumour sample of the same patient (1,231 files on 1,098 cases).
- Siblings and duplicates: `tcga_hnsc_tumor_vs_normal_rnaseq` (the same build for head and neck, screened in another batch; the two should get the same call), `tcga_lung_histology` (normal lung as a third class), `tcga_pancancer_tumor_type` (tissue of origin; shares the BRCA tumours, another task, PROV-7), `brca_breast_cancer` (`No`, PAM50 subtype, SEL-4), `tcga_coad_molecular_subtype` (the GDC per-sample build). External collections: TabBench-Bio (Table 4).
- Better data: a candidate of the benchmark TabBench-Bio (the run searched no further).
- Papers and pages: TCGA Network 2012; https://portal.gdc.cancer.gov/projects/TCGA-BRCA; TabBench-Bio (Kreuer et al. 2026, arXiv 2609.07441, Table 4).
- Metric: none found for this target (the TCGA paper builds no tumour-against-normal classifier); TabBench-Bio ranks by macro-F1 (Sec. 3.5), a threshold metric without a fixed threshold (MET-6). Fallback `roc_auc`; inputs: the patient barcode as the group, never a feature.
- Risks for /add-dataset: a target no decision may fit (USE-2, SEL-3; settle it first, together with the HNSC record); expected trivial (TP-4: test one marker gene against the methods); patient grouping (SPLIT-24) and the 7 metastatic samples; tissue source site and plate may differ between normals and tumours (a batch shortcut, check); 60,660 genes in per-sample TPM, so no cohort-wide scaling (LEAK-30 holds).
- Priority: gap 0, use case 0, source + (TCGA and the GDC), shape + (1,231 samples, grouped by patient), risk - (an unclear target, expected trivial).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 1,231 x 60,660; target: sample_type (~1,118 tumour / 113 normal).
- Why: Primary tumour vs solid normal tissue from RNA-seq (STAR counts, TPM, GENCODE v36)
- Notes: GDC open access. Related: brca_breast_cancer (TCGA BRCA multi-omics via ACGT, PAM50 target, 'No') and tcga_coad_molecular_subtype (GDC); neither has this tumour-vs-normal target.

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: consistency: should get the same call as the rejected `tcga_hnsc_tumor_vs_normal_rnaseq` (tumour or normal is fixed when the tissue is taken; USE-2).
