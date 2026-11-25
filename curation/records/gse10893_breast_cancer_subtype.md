---
unique_name: gse10893_breast_cancer_subtype
name: GEO-GSE10893 Breast Cancer Subtypes
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
- Experimental Results
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

**Screening (AI, 2026-11-25):** `No` (`No Good Target / Scientific Discovery`, SEL-4): the target is the PAM50 intrinsic subtype with the claudin-low call, a taxonomy from clustering expression profiles assigned by centroid predictors, the label rejected on `brca_breast_cancer` and `glioblastoma`; and the GPL8864 samples the benchmark pins are DNA copy number, not expression.
- Source: Weigman, Chao, Shabalin et al., "Basal-like Breast cancer DNA copy number losses identify genes involved in genomic instability, response to therapy, and patient survival", Breast Cancer Res Treat 133(3):865-880, 2011 (https://doi.org/10.1007/s10549-011-1846-y, read on PMC3387500); data GEO GSE10893 (UNC, Perou lab), 504 samples on 7 platforms. The 180 GPL8864 samples are tumour genomic DNA on the "Infinium Human-1 109K BeadChip", 109,315 copy-number rows each, labelled only with `subtype`; TabBench-Bio keeps 165 and calls them gene expression, which they are not.
- The label: "We classified each tumor into one of five previously defined expression subtypes" using "the published intrinsic subtypes (i.e., PAM50) and Claudin-low subtype predictors" (Results). Predicting the call from copy number instead of expression leaves the label what it is (SEL-4).
- Use case: none (USE-2). Collection: banked tumour specimens measured once, no date (`Samples: No Time Dimension`); type Experimental Results (SPLIT-34 rule 5). The 185 GPL1390 expression samples carry ER, PR, HER2, grade, node status and relapse and survival events: a relapse or survival task there would be a distinct candidate (PROV-7), not this cut.
- Split: none (no task); had it one, leaf L-EXP.random (one array per tumour).
- Siblings and duplicates: `brca_breast_cancer` and `glioblastoma` (`No`, SEL-4) set the precedent; `tcga_brca_tumor_vs_normal_rnaseq` another TabBench-Bio record with another task. External collections: TabBench-Bio (Table 4).
- Better data: not searched (no task).
- Metric: none (no task).
- Reject check (AI, 2026-11-25): stands. The GPL8864 matrix read again: 180 samples, all `genomic DNA` from "Breast Tumor", paired with "Normal DNA from Normal Breast", `subtype` the only characteristic; SEL-4 names PAM50 verbatim.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 165 x 109,315; target: subtype (~7 classes).
- Why: Intrinsic breast cancer subtype from microarray expression (pinned to platform GPL8864)
- Notes: Weigman et al. 2012 (GEO series of 504 samples on 7 platforms). The intrinsic subtype is the clustering-derived label Lennart rejected on brca_breast_cancer ('labels that come from unsupervised learning').
