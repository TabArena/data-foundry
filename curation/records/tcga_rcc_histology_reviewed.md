---
unique_name: tcga_rcc_histology_reviewed
name: 'The Cancer Genome Atlas Comprehensive Molecular Characterization of Renal Cell Carcinoma (Ricketts et al. 2018): pathology-reviewed TCGA-RCC cohort'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
year: '2018'
domain: medical & healthcare
problem_type: Multiclass Classification
source_links:
- https://doi.org/10.1016/j.celrep.2018.03.075
- https://pmc.ncbi.nlm.nih.gov/articles/PMC6075733/
- https://portal.gdc.cancer.gov/projects/TCGA-KIRC
- https://portal.gdc.cancer.gov/projects/TCGA-KIRP
- https://portal.gdc.cancer.gov/projects/TCGA-KICH
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: the TCGA kidney cohort with its histology re-reviewed by expert pathologists (843 tumours: 488 ccRCC, 274 PRCC, 81 ChRCC, the PRCC split further), a better-measured label for the task of `tcga_kidney_cancers`; but the three main subtypes are likely near-perfectly separable from expression, and RNA-seq is not how the subtype is diagnosed.
- Source: Ricketts, De Cubas, Fan et al., "The Cancer Genome Atlas Comprehensive Molecular Characterization of Renal Cell Carcinoma", Cell Reports 23(1):313-326.e5, 2018 (doi 10.1016/j.celrep.2018.03.075; author manuscript PMC6075733, read 2026-10-31). Results, "Evaluation of RCC Histologic Subtypes": "In total, 894 samples of kidney cancer were initially submitted to TCGA and were available for analysis, including 537 ccRCC, 291 PRCC, and 66 ChRCC"; samples were "re-evaluated by histologic review and removed if considered inappropriate and 15 samples originally submitted as ccRCC were reclassified as ChRCC. This resulted in a final cohort of 843 TCGA-RCC"; the PRCC divided into "160 type 1 PRCC, 70 type 2 PRCC, 34 unclassified PRCC, and 10 CpG island methylator phenotype-associated (CIMP)-RCC (Table S1)". STAR Methods: the six groups are "based on the original pathology reports or re-evaluation by a panel of expert urologic pathologists". As published: Table S1 (per-sample clinical and genomic annotations); expression in the GDC projects TCGA-KIRC, TCGA-KIRP and TCGA-KICH.
- Use case: a pathologist with a renal tumour of ambiguous histology (eosinophilic ccRCC against ChRCC, PRCC type 1 against type 2) settles the subtype from a molecular profile, which sets prognosis and therapy ("several histologically defined cancers with different genetic drivers, clinical courses, and therapeutic responses", Summary); fit approximate: the source trains no classifier, and the subtype is diagnosed on H&E and immunohistochemistry. Regime IID (one primary tumour per patient), with the tissue source site checked as a batch.
- Siblings and duplicates: `tcga_kidney_cancers` (`TBD -> 2nd Tier`, `Needs extensive data wrangling`; UCI's TCGA kidney set labelled by project code), the record this was found for: a later, re-reviewed labelling of the same tumours (PROV-6), so one of the two enters, the curator decides. `tcga_pancancer_tumor_type` (`TBD -> Yes`) holds the same tumours among 33 types, another task (PROV-7). External collections: not searched (web search budget used up).
- Better data: found as better data for `tcga_kidney_cancers` (the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: Ricketts et al. 2018 (Results, STAR Methods); the GDC project pages; Chen et al. 2016 (the earlier pan-kidney sample set, cited by Ricketts, not read).
- Metric: none found (the paper characterises the subtypes and their survival and trains no classifier), so the fallback `log_loss` for the multiclass target (MET-1, MET-8); inputs none.
- Risks for /add-dataset: the three-class task is likely near-perfect from expression (a TP-4 probe); the six-group label is the harder task, with 34 unclassified PRCC (TP-8); CIMP-RCC is a methylation phenotype rather than a histologic call (SEL-4 to check): merge it into PRCC or drop it; build expression from the GDC per-sample files, not a matrix normalised over all samples (LEAK-30), and join Table S1 by barcode; drop normals and repeat aliquots (LEAK-17); `Needs extensive data wrangling`.
- Priority: gap + (multiclass is thin), use case 0 (approximate), source + (Cell Reports, TCGA), shape 0 (843 tumours, one feature type), risk − (likely near-perfect three-class task).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `tcga_kidney_cancers`.
- as published: 843 primary renal cell carcinomas (488 ccRCC, 274 PRCC, 81 ChRCC) kept from the 894 submitted to TCGA after re-review by an expert pathology panel; Table S1 per-sample clinical and genetic ...; target: histological subtype ccRCC / PRCC / ChRCC (PRCC further split into type 1, type 2, unclassified, CIMP); access: open.
- Why: same units (TCGA kidney tumours), same features (RNA-seq) and the same target as tcga_kidney_cancers, whose labels are the TCGA project codes KICH/KIRC/KIRP as submitted
- Adds: the target measured better: the TCGA kidney marker paper's pathology review reclassified 15 tumours submitted as ccRCC to ChRCC and removed 51 as inappropriate (prior therapy, inconsistent histology); fewer rows (843 vs UCI's 1,024, which may hold normals or repeat aliquots, not checked). Also gives the cohort the ...
- A newer release of the same source as the record(s) named above (PROV-6): the curator decides which one enters.
