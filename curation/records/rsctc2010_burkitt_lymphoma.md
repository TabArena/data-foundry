---
unique_name: rsctc2010_burkitt_lymphoma
name: OpenML-1083 mouseType
checked_by:
- AI (UNVERIFIED)
- Andrej
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
- AI-Filled (Verify)
- Tiny Data
- Many features
- 'Samples: No Time Dimension'
- Experimental Results
collections:
- TabBench-Bio
original_source: Other
year: '2010'
domain: medical & healthcare
problem_type: Multiclass Classification
source_links:
- http://tunedit.org/challenge/RSCTC-2010-A
- https://www.openml.org/d/1083
- https://arxiv.org/abs/2609.07441
- https://www.openml.org/d/1084
- https://www.openml.org/d/1088
- https://doi.org/10.1007/978-3-642-13529-3_4
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-25):** `No` (`No Good Target / Scientific Discovery`, USE-2, SEL-5) for the Burkitt set this record is named after (OpenML 1084): its three classes are GEO GSE4475's `Molecular.Diagnosis` (mBL 44, intermediate 48, non-mBL 129), the output of a signature Hummel et al. built on the same arrays; the two other RSCTC sets this record bundles (OpenML 1083 mouseType, 1088 variousCancers_final) are not decided by this reject and stay open in it.
- Source: the RSCTC 2010 Discovery Challenge (Wojnarski et al. 2010, LNCS 6086, pp. 4-19; paywalled, not read; tunedit.org dead). OpenML (uploaded 2014-10-07, "Source: Unknown - Date unknown"): 1083 mouseType 214 x 45,101, 7 classes; 1084 BurkittLymphoma 220 x 22,283, 3 classes (128, 48, 44); 1088 variousCancers_final 383 x 54,675, 9 classes; values "normalized in some way".
- Burkitt, the label: GSE4475 (Hummel et al., NEJM 2006, PubMed 16760442): "A molecular signature for Burkitt's lymphoma was generated" from the U133A profiles of 220 lymphomas, and "We used the molecular signature for Burkitt's lymphoma to identify 44 cases"; the series matrix (read 2026-11-25) carries `Molecular.Diagnosis` mBL 44, intermediate 48, non-mBL 129 beside `BL.probability`, which the OpenML counts match up to one sample. The pathologist's diagnosis is a separate field (`Morphologic.diagnosis`), not this target.
- Use case: none for this label (USE-2: it stands in for what the features measure). A real task in the same series, for a record of its own: the morphological diagnosis or the outcome (`Survival.Status`, `FollowupTime`, `Relapse`, treatment response) of GSE4475, a distinct task (PROV-7). Collection: banked lymphoma specimens measured once (`Samples: No Time Dimension`); type Experimental Results.
- Split: none (no task); had it one, leaf L-EXP.random (one array per tumour).
- The other two sets: mouseType's classes and source series are unknown (PROV-1 after a search, then `Missing source information`); variousCancers_final is on HG-U133 Plus 2.0, the platform of expO (GSE2109), so it may be a cut of `expo_tumor_tissue_of_origin`'s data (PROV-4 check). Neither is decided by this reject.
- Siblings and duplicates: `gcm_multiclass_cancer`, `ova_breast`, `expo_tumor_tissue_of_origin` (tumour type); `brca_breast_cancer`, `glioblastoma` (`No`, SEL-4). External collections: TabBench-Bio (OpenML 1083, 1084, 1088).
- Better data: not searched (no task).
- Metric: the challenge's measure not confirmed (paper paywalled); no task.
- Reject check (AI, 2026-11-25): stands. Two further fields of the series matrix show the signature was fitted and applied on these same 221 arrays: `Training.Test` (Training 113, Test 108) and `core.BL` (yes 8, the WHO-typical seed cases), so the target is the output of a classifier trained on the shipped probes (SEL-5 with USE-2). The clinical steelman (Burkitt against diffuse large B-cell lymphoma decides the regimen) is decided by morphology, immunohistochemistry and MYC FISH, whose ground truth is `Morphologic.diagnosis` or the outcome, a task for its own record (PROV-7). SEL-4 does not apply: the signature was seeded on 8 core cases, so it is supervised, not clustering.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 214 x 45,101; target: Decision (7 classes).
- Why: Class from DNA microarray profiles (RSCTC 2010 Discovery Challenge set; class meaning not documented on OpenML) | Lymphoma class from DNA microarray profiles (RSCTC 2010 Discovery Challenge set) | Cancer type from DNA microarray profiles (RSCTC 2010 Discovery Challenge set)
- Notes: Source on OpenML: 'Data from the RSCTC 2010 Discovery Challenge' (Wojnarski et al., RSCTC 2010, LNCS 6086); the tunedit link is dead and the underlying GEO series is not named. | Same RSCTC 2010 provenance gap as mouseType; the underlying GEO series is not named on OpenML. | Same RSCTC 2010 provenance gap as mouseType.

**CC (2026-11-25, Andrej):** the record stays as it is: no split into separate records.
- OpenML 1083 (mouseType) and 1088 (variousCancers_final) stay in this record; the `No` decides the Burkitt set it is named after, and the block says the other two are not decided by it.
