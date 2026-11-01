---
unique_name: gse10893_breast_cancer_subtype
name: GEO-GSE10893 Breast Cancer Subtypes
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
- https://doi.org/10.1007/s10549-011-1846-y
- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE10893
- https://arxiv.org/abs/2609.07441
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`No Good Target / Scientific Discovery`, SEL-4): the target is the PAM50 intrinsic subtype with the claudin-low call, a taxonomy from clustering expression profiles assigned by centroid predictors, the label rejected on `brca_breast_cancer` and `glioblastoma`; and the GPL8864 data the benchmark pins are DNA copy number, not expression.
- Source: Weigman, Chao, Shabalin et al., "Basal-like Breast cancer DNA copy number losses identify genes involved in genomic instability, response to therapy, and patient survival", Breast Cancer Res Treat 133(3):865-880, online 2011-11-03 (https://doi.org/10.1007/s10549-011-1846-y, read on PMC3387500); data GEO GSE10893 (UNC, Perou lab), public 2011-11-06: 504 samples on 7 platforms. The 180 GPL8864 samples are tumour genomic DNA on the "Infinium Human-1 109K BeadChip" (Methods), 109,315 copy-number rows each (GEO: "Sample_type = genomic", "PairedSample Analysis"), labelled only with `subtype` (LumA 52, Basal 40, LumB 40, Her2 21, Normal-like 12, Claudin-low 9, Claudin 6); TabBench-Bio keeps 165 and its registry (`GEO-GSE10893`) calls them gene expression, which they are not.
- The label: "We classified each tumor into one of five previously defined expression subtypes" using "the published intrinsic subtypes (i.e., PAM50) and Claudin-low subtype predictors" (Results, "Identifying subtype-specific regions of copy number aberration"); the series' expression samples carry it as "pam50 predictions plus claudin-low classification (cell line predictor)". SEL-4 names this label: "a molecular subtype defined by clustering (PAM50, expression subtypes, NMF clusters)"; CC (2026-10-12, Lennart) on `brca_breast_cancer`: "we do not benchmark labels that come from unsupervised learning". Predicting the call from copy number instead of expression leaves the label what it is.
- Use case: none (USE-2). The 185 expression samples on GPL1390 carry ER, PR, HER2, grade, node status, size and relapse and survival events: a relapse or survival task there would be another candidate, not this cut, and is not screened here.
- Siblings and duplicates: `brca_breast_cancer` (`No`, SEL-4) and `glioblastoma` (`No`) set the precedent; `tcga_brca_tumor_vs_normal_rnaseq` is another TabBench-Bio record with a different task. External collections: TabBench-Bio (arXiv 2609.07441, Table 4).
- Better data: a candidate of the benchmark TabBench-Bio; no new search in this run.
- Metric: none (no task).
- Reject check (AI, 2026-10-31): stands. GEO: 'we first classified tumors according to gene expression intrinsic subtype' (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE10893); the paper used 'the published intrinsic subtypes (i.e., PAM50) and Claudin-low subtype predictors' (https://pmc.ncbi.nlm.nih.gov/articles/PMC3387500/). This is the clustering label of Lennart's CC on brca_breast_cancer, and the GPL8864 copy-number samples carry no other label. The GPL1390 expression samples with relapse and survival are a distinct task (PROV-7) for a record of their own, not a reason to keep this cut.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 165 x 109,315; target: subtype (~7 classes).
- Why: Intrinsic breast cancer subtype from microarray expression (pinned to platform GPL8864)
- Notes: Weigman et al. 2012 (GEO series of 504 samples on 7 platforms). The intrinsic subtype is the clustering-derived label Lennart rejected on brca_breast_cancer ('labels that come from unsupervised learning').
