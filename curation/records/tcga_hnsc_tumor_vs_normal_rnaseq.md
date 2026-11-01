---
unique_name: tcga_hnsc_tumor_vs_normal_rnaseq
name: TCGA-TCGA-HNSC_Gene-Expression-Quantification (TCGA Head & Neck, RNA-seq)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
- AI-Filled (Verify)
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

**Screening (AI, 2026-10-31):** `No` (`No Good Target / Scientific Discovery`, USE-2): the target is TCGA's sample type, tumour or the matched normal control, both fixed by the surgeon and the pathologist when the tissue is procured, before any RNA is sequenced; a model can only cross-check a known label, the case `glioma_grading_clinical_and_mutation_features` was retired on (USE-1, 2026-10-26).
- Source: The Cancer Genome Atlas, head and neck squamous cell carcinoma (TCGA-HNSC); marker paper The Cancer Genome Atlas Network, "Comprehensive genomic characterization of head and neck squamous cell carcinomas", Nature 517:576 (doi 10.1038/nature14129, online 2015-01-28), which profiled 279 tumours "to provide a comprehensive landscape of somatic genomic alterations" (abstract), a discovery study with no predictive task. As published on the GDC (STAR - Counts gene expression quantification, GENCODE v36, 60,660 genes; API query 2026-10-31): 566 files, 520 primary tumour, 44 solid tissue normal, 2 metastatic; 43 of the 44 normals come from a patient whose tumour is also in the data. TabBench-Bio's registry: "HNSC RNA-seq (STAR-Counts tpm_unstranded). Target: tumor vs normal. HDLSS; capped at build"; its Table 4: 566 x 60,660, target `sample_type`; classes under ten samples dropped (Sec. 3.1), so 564 rows.
- Use case: none found. TCGA's Head & Neck Case Quality Control Form (V4.20) requires "A normal control must be present to qualify", procured "for matching normal DNA" and only "Distal (> or = 2cm) from the primary tumor", and the tumour to be "a primary untreated malignant biospecimen" whose diagnosis the BCR may confirm "through histopathology examination in the BCR laboratory". Both labels exist before sequencing, and the normal is a germline control taken away from the tumour, not an ambiguous specimen a clinician needs classified. TabBench-Bio names no decision (Ethics: "The benchmark does not establish clinical validity, and no ranking reported here supports use in patient care"). Fit None (USE-8). Steelman: molecular tumour detection is studied for margins or ambiguous biopsies, but these rows do not mirror that setting, and the source names none.
- Siblings and duplicates: `tcga_brca_tumor_vs_normal_rnaseq` (TabBench-Bio, the same task on TCGA-BRCA, screened in another batch) has the same mechanism and should be decided alike. Precedents: `glioma_grading_clinical_and_mutation_features` (`No`, USE-1: a grade known before sequencing); `brca_breast_cancer`, `glioblastoma`, `ov_ovarian_cancer` (`No`, SEL-4, other TCGA labels); `sarcoma` (`Yes`, a typing decision with a source). No duplicate. External collections: TabBench-Bio.
- Better data: a candidate of the benchmark TabBench-Bio; no further search this round.
- Papers and pages: the TCGA HNSC paper (PMC4311405); the GDC project page (portal.gdc.cancer.gov/projects/TCGA-HNSC) and the TCGA Head & Neck Case Quality Control Form; the TabBench-Bio paper, registry and leaderboard.
- Metric: the TCGA paper defines none (a discovery study); TabBench-Bio: "Macro-F1 is the primary classification metric" (Sec. 3.5), a benchmark-wide default with no threshold fixed (MET-6), with MCC, balanced accuracy and ROC AUC on its leaderboard. Its leaderboard (snapshot 2026-10-23, the 10,000-feature cell without a sample cap) has ROC AUC 0.99 or more for 24 of 30 models (logistic regression 0.996, random forest 0.998; the constant baseline and a TabICL run at 0.5), on row-wise folds that keep a patient's tumour and normal apart only by chance: likely `Trivial` too (TP-4), not measured on our splits.
- Reject check (AI, 2026-10-31): stands. TCGA's HNSC Case Quality Control Form V4.20 (text read from the PDF, https://gdc.cancer.gov/system/files/public/file/Head%20and%20Neck%20Case%20Quality%20Control%20Form.pdf): 'A normal control must be present to qualify', procured 'for matching normal DNA', 'Distal (> or = 2cm) from the primary tumor', and the tumour 'a primary untreated malignant biospecimen'. Both labels exist before sequencing; the normal is a germline control, not an ambiguous specimen. Same mechanism as glioma_grading_clinical_and_mutation_features (Lennart 2026-10-26: cross-check of a known label). Consistency: tcga_brca_tumor_vs_normal_rnaseq was screened `TBD -> 2nd Tier` in this run on the same facts; it should get the same call.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 566 x 60,660; target: sample_type.
- Why: Head and neck squamous cell carcinoma tumour vs solid normal tissue from RNA-seq
- Notes: GDC open access; same build as TCGA-BRCA.
