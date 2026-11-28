---
unique_name: tcga_brca_tumor_vs_normal_rnaseq
name: TCGA-TCGA-BRCA_Gene-Expression-Quantification (TCGA Breast, RNA-seq)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
- AI-Filled (Verify)
- Many features
- 'Samples: No Time Dimension'
- 'Entities: Recur'
- Experimental Results
collections:
- TabBench-Bio
original_source: GOV Website
year: '2012'
domain: medical & healthcare
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

**Screening (AI, 2026-11-25):** `No` (`No Good Target / Scientific Discovery`, USE-1, USE-2): primary breast tumour against non-neoplastic breast tissue taken at least 2 cm from it (GDC `Solid Tissue Normal`; the form: 'Adjacent (< 2cm) Normal Tissue is not accepted for this tissue type') from TCGA-BRCA RNA-seq; both labels are the sample type TCGA's protocol fixes when the tissue is procured, before any RNA is sequenced, so a model can only cross-check a known label, the mechanism `tcga_hnsc_tumor_vs_normal_rnaseq` was rejected on (changed from `TBD -> 2nd Tier`, priority 2, for consistency).
- Source: TCGA Network, "Comprehensive molecular portraits of human breast tumours", Nature 490:61-70, 2012 (doi 10.1038/nature11412), a characterisation study; data on the NCI GDC (TCGA-BRCA), STAR-Counts per sample (TPM, GENCODE v36). GDC API, 2026-10-31: 1,231 open files, 1,111 primary tumour, 113 solid tissue normal, 7 metastatic, over 1,098 cases. TabBench-Bio: 1,231 x 60,660, target `sample_type`, metastatic counted as tumour.
- Use case: none found. TCGA's Breast Case Quality Control Form (V4.04): "A normal control must be present to qualify", the tumour a "primary untreated malignant biospecimen", the normal control blood or buffy coat by default, and "Non-neoplastic Control Tissue may only be submitted with NCI approval"; a tissue normal must be "Distal (> 2cm) from the primary tumor" (item 48) and comes with its "Normal Slide ID#" (item 49), so it is pathology-reviewed too; the label is the procurement record, not a question a clinician asks of these specimens. The steelman (a molecular check that a margin or biobank specimen holds tumour, where pathology decides today) is not what these rows mirror, and the source names no such use; fit None (USE-8). Collection: banked specimens measured once (`Samples: No Time Dimension`), tumour and normal of one patient (`Entities: Recur`, 1,231 files on 1,098 cases); type Experimental Results (SPLIT-34 rule 5).
- Split: none (no task); had it one, grouped by patient (leaf L-EXP.item).
- Siblings and duplicates: `tcga_hnsc_tumor_vs_normal_rnaseq` (`No`, same mechanism); `tcga_lung_histology`, `tcga_pancancer_tumor_type` (other tasks on TCGA, PROV-7); `brca_breast_cancer` (`No`, SEL-4); precedents `glioma_grading_clinical_and_mutation_features` and `lung_cancer`'s histology (`No`, USE-1). External collections: TabBench-Bio (Table 4).
- Better data: not searched (no task).
- Metric: none for this target; TabBench-Bio's macro-F1 is its default (MET-6); expected near-perfectly separable (TP-4), not measured.
- Reject check (AI, 2026-11-25): stands on USE-1 ("A label read from the same specimen the features measure, and settled before they are taken, leaves only a cross-check of a known label and fits no decision"). Steelmen tried: margin assessment (these normals are planned controls at least 2 cm away; margins are read on frozen section), tumour purity (a continuous quantity, set by pathology nuclei counts and ABSOLUTE), sample mix-up QC (done by genotype concordance); no source names any of them (USE-9).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 1,231 x 60,660; target: sample_type (~1,118 tumour / 113 normal).
- Why: Primary tumour vs solid normal tissue from RNA-seq (STAR counts, TPM, GENCODE v36)
- Notes: GDC open access. Related: brca_breast_cancer (TCGA BRCA multi-omics via ACGT, PAM50 target, 'No') and tcga_coad_molecular_subtype (GDC); neither has this tumour-vs-normal target.

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: consistency: should get the same call as the rejected `tcga_hnsc_tumor_vs_normal_rnaseq` (tumour or normal is fixed when the tissue is taken; USE-2).
