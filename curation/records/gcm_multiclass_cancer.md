---
unique_name: gcm_multiclass_cancer
name: OpenML-1106 GCM
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Too Small
- Selection Bias
tags:
- AI-Filled (Verify)
- Many features
- Tiny Data
collections:
- TabBench-Bio
original_source: Other
year: '2001'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.1073/pnas.211566398
- https://www.openml.org/d/1106
- https://arxiv.org/abs/2609.07441
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: the Global Cancer Map, 190 tumours of 14 types on 16,063 microarray probes — a real tissue-of-origin diagnosis, but almost certainly `Too Small` (10 samples in the shortest class, about 2 per test fold) and covered by a larger recorded cohort.
- Source: Ramaswamy, Tamayo, Rifkin, Mukherjee, Yeang, Angelo, Ladd, Reich, Latulippe, Mesirov, Poggio, Gerald, Loda, Lander and Golub, "Multiclass cancer diagnosis using tumor gene expression signatures", PNAS 98(26):15149-15154, 18 December 2001 (doi 10.1073/pnas.211566398, read on PMC64998): "we subjected 218 tumor samples, spanning 14 common tumor types, and 90 normal tissue samples to oligonucleotide microarray gene expression analysis. The expression levels of 16,063 genes and expressed sequence tags were used to evaluate the accuracy of a multiclass classifier based on a support vector machine algorithm." The copy the benchmark uses is OpenML 1106 ("GCM", uploaded 2014-10-07, "Source: Unknown - Date unknown"): 190 rows x 16,064 columns, no missing values, target `class` over Bladder, Breast, CNS, Colorectal, Leukemia, Lung, Lymphoma, Melanoma, Mesothelioma, Ovary, Pancreas, Prostate, Renal and Uterus__Adeno; majority class 30 rows, minority class 10 (OpenML qualities and features API, read 2026-10-31). OpenML adds "Original split: 144 first instances for training, remainder for testing", the paper's 144-sample training set with 46 of its test samples. One table; the paper's 90 normal tissues are not in this cut.
- Use case: a pathologist or oncologist facing a tumour whose origin the histology cannot settle decides the tissue of origin, which sets the treatment: "The optimal treatment of patients with cancer depends on establishing accurate diagnoses by using a complex combination of clinical and histopathological data. In some instances, this task is difficult or impossible because of atypical clinical presentation or histopathology" (abstract). Fit approximate: the rows are mostly well-differentiated tumours of known type, while the decision is made on the undifferentiated ones the paper itself could not classify ("Poorly differentiated cancers resulted in low-confidence predictions and could not be accurately classified according to their tissue of origin"), a selection the real setting does not share (USE-8, `Selection Bias`). Regime IID: one sample per patient, the source's own random design.
- Siblings and duplicates: `expo_tumor_tissue_of_origin` (GEO GSE2109, 2,158 tumours with the primary site, a candidate of this run) is the same tissue-of-origin task on a much larger and newer cohort; `ova_breast` (`TBD -> Yes`) holds the GEMLeR one-vs-all cuts of that expO data. The precedents for small microarray sets are `colon_tumor` (`No`, `Too Small`, Lennart: "Only 62 samples, too small to be a reasonable non-few-shot task with cross-validation") and `srbct_prediction` (`No`, `Trivial`); `brca_breast_cancer`, `ov_ovarian_cancer` and `gse10893_breast_cancer_subtype` carry clustering-derived subtypes (SEL-4), a different problem. No duplicate record of GCM (grep over the records on "Ramaswamy", "Global Cancer Map" and "openml.org/d/1106"). External collections: TabBench-Bio (`OpenML-1106`).
- Better data: a candidate of the benchmark TabBench-Bio; no new search this round. Already among the records: `expo_tumor_tissue_of_origin` for the same task.
- Papers and pages: the PNAS paper (PMC64998); OpenML 1106 (https://www.openml.org/d/1106); TabBench-Bio (arXiv 2609.07441), Table 4 row OpenML-1106.
- Metric: the paper reports accuracy — "Overall classification accuracy was 78%, far exceeding the accuracy of random classification (9%)" — with no threshold, cost or k fixed, the habit of its field rather than a deliberate choice (MET-6), so the fallback `log_loss` for a multiclass task (MET-8). The benchmark's own metric is Macro-F1 ("Macro-F1 is the primary classification metric, weighting classes equally without designating a positive class", Sec. 3.5), its choice and not the source's. Inputs: none.
- Risks for /add-dataset: `Too Small` is the first check (TP-5, TP-8): 190 rows over 14 classes, 10 in the shortest, about 2 per class per test fold, against the `colon_tumor` precedent at 62 rows. OpenML's copy names no preprocessing ("Source: Unknown"), so the probe-level scaling and gene filtering of the 1999-2001 Affymetrix Hu6800/Hu35K arrays cannot be checked from it (PROV-2, LEAK-30): rebuild from the Broad's original release if it is kept. The class names mix organ sites and lineages (Leukemia, Lymphoma against Bladder, Breast), which is the paper's own label set.
- Priority: gap + (multiclass classification is thin, 24 of 173 accepted datasets), use case 0 (real, but the fit is approximate: the hard cases are not in the data), source + (a PNAS paper that documents the design), shape 0 (190 rows), risk - (`Too Small` is likely and `expo_tumor_tissue_of_origin` holds the task on 2,158 tumours).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 190 x 16,063; target: class (14 tumour types).
- Why: Tumour type from microarray expression (Global Cancer Map, Ramaswamy et al. 2001)
- Notes: 2001 microarray data.
