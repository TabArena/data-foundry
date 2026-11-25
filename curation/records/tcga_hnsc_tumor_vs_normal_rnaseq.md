---
unique_name: tcga_hnsc_tumor_vs_normal_rnaseq
name: TCGA-TCGA-HNSC_Gene-Expression-Quantification (TCGA Head & Neck, RNA-seq)
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Andrej
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
- AI-Filled (Verify)
- 'Samples: No Time Dimension'
- 'Entities: Recur'
- Experimental Results
collections:
- TabBench-Bio
source_links:
- https://doi.org/10.1038/nature14129
- https://portal.gdc.cancer.gov/projects/TCGA-HNSC
- https://arxiv.org/abs/2609.07441
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-25):** `No` (`No Good Target / Scientific Discovery`, USE-1, USE-2): the target is TCGA's sample type, tumour or the matched normal control, both fixed by the protocol when the tissue is procured, before any RNA is sequenced; a model can only cross-check a known label, as on `glioma_grading_clinical_and_mutation_features`.
- Source: The Cancer Genome Atlas, TCGA-HNSC; marker paper TCGA Network, "Comprehensive genomic characterization of head and neck squamous cell carcinomas", Nature 517:576, 2015 (doi 10.1038/nature14129), a discovery study with no predictive task. As published on the GDC (STAR - Counts, GENCODE v36, 60,660 genes; API 2026-10-31): 566 files, 520 primary tumour, 44 solid tissue normal, 2 metastatic; 43 of the 44 normals from a patient whose tumour is also in the data.
- Use case: none found. TCGA's Head & Neck Case Quality Control Form (V4.20): "A normal control must be present to qualify", procured "for matching normal DNA" and only "Distal (> or = 2cm) from the primary tumor"; the tumour "a primary untreated malignant biospecimen". Both labels exist before sequencing, and the normal is a germline control taken away from the tumour, not an ambiguous specimen. Fit None (USE-8). Collection: banked specimens measured once (`Samples: No Time Dimension`), tumour and normal of one patient (`Entities: Recur`); type Experimental Results (SPLIT-34 rule 5).
- Split: none (no task); had it one, grouped by patient (leaf L-EXP.item).
- Siblings and duplicates: `tcga_brca_tumor_vs_normal_rnaseq` (the same task on TCGA-BRCA; proposed `No` alike in this run); precedents `glioma_grading_clinical_and_mutation_features` (`No`, USE-1), `lung_cancer` (histology retired, USE-1), `brca_breast_cancer`, `glioblastoma`, `ov_ovarian_cancer` (`No`, SEL-4). External collections: TabBench-Bio.
- Better data: not searched (no task).
- Metric: the TCGA paper defines none; TabBench-Bio's macro-F1 is a benchmark-wide default (MET-6). Its leaderboard has ROC AUC 0.99 or more for 24 of 30 models on row-wise folds: likely `Trivial` too (TP-4), not measured here.
- Reject check (AI, 2026-11-25): stands. USE-1: "A label read from the same specimen the features measure, and settled before they are taken, leaves only a cross-check of a known label and fits no decision"; the normal is taken "Distal (> or = 2cm) from the primary tumor" (HNSC form V4.20), and no source names a decision on these rows.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 566 x 60,660; target: sample_type.
- Why: Head and neck squamous cell carcinoma tumour vs solid normal tissue from RNA-seq
- Notes: GDC open access; same build as TCGA-BRCA.
