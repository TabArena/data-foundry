---
unique_name: gcm_multiclass_cancer
name: OpenML-1106 GCM
checked_by:
- AI (UNVERIFIED)
- Andrej
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Too Small
- Selection Bias
tags:
- AI-Filled (Verify)
- Many features
- Tiny Data
- 'Samples: No Time Dimension'
- Experimental Results
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

**Screening (AI, 2026-11-25):** `TBD -> 2nd Tier`, priority 2: the Global Cancer Map, 190 tumours of 14 types on 16,063 microarray probes, a real tissue-of-origin task, but almost certainly `Too Small` (10 samples in the shortest class, about 2 per test fold) and held on far more tumours by `expo_tumor_tissue_of_origin` and `tcga_pancancer_tumor_type`.
- Source: Ramaswamy, Tamayo, Rifkin et al., "Multiclass cancer diagnosis using tumor gene expression signatures", PNAS 98(26):15149-15154, 2001 (doi 10.1073/pnas.211566398, read on PMC64998): "218 tumor samples, spanning 14 common tumor types, and 90 normal tissue samples ... The expression levels of 16,063 genes and expressed sequence tags were used". The benchmark's copy is OpenML 1106 ("GCM", uploaded 2014-10-07, "Source: Unknown - Date unknown"): 190 x 16,064, target `class` over 14 types, majority 30, minority 10; "Original split: 144 first instances for training, remainder for testing". One table; the normals are not in this cut.
- Use case: a pathologist facing a tumour whose origin histology cannot settle decides the tissue of origin, which sets the treatment (abstract: "In some instances, this task is difficult or impossible because of atypical clinical presentation or histopathology"); the actor's tool today is an expression tissue-of-origin test as a second opinion, the case USE-1 was amended on (`lung_adenocarcinoma_metastasis`). Fit approximate: the rows are mostly tumours of known type, while the decision is made on the undifferentiated ones the paper could not classify ("Poorly differentiated cancers resulted in low-confidence predictions", `Selection Bias`, USE-8); the label rests on the clinical work-up, and whether a primary's type is "settled on the specimen" (a cross-check, as `tcga_lung_histology`) or ground truth for a tissue-of-origin test (as `expo_tumor_tissue_of_origin`) is the USE-1 question for the curator. Collection: banked tumour specimens measured once, no date (`Samples: No Time Dimension`); one array per tumour. Type Experimental Results (SPLIT-34 rule 5).
- Split: leaf L-EXP.random (Random · `Timeless`) because [EXP.meets] is a new tumour of the kinds the data contains and [EXP.repeated] is no (one array per tumour); open: whether the 2001 arrays' scan batches (not in the OpenML copy) follow the class.
- Siblings and duplicates: `expo_tumor_tissue_of_origin` (GEO GSE2109, 2,158 tumours), `ova_breast` (GEMLeR cuts of expO), `tcga_pancancer_tumor_type` (about 10,000 TCGA tumours of 33 types) hold the same task; small microarray precedents `colon_tumor` (`No`, `Too Small`) and `srbct_prediction` (`No`); `rsctc2010_burkitt_lymphoma`'s variousCancers set is another tumour-type cut. No duplicate of GCM. External collections: TabBench-Bio (`OpenML-1106`).
- Better data: `expo_tumor_tissue_of_origin` (2,158 tumours, 2004-2010 deposits, one U133 Plus 2.0 platform), a record with no definition yet, and `tcga_pancancer_tumor_type` (TCGA, RNA-seq), whose definition is written and built at 9,724 tumours over 33 cancer types against the 190 rows and 14 types here: more tumours, more types and newer platforms for the same task, and the second of the two is no longer only a record.
- Papers and pages: the PNAS paper (PMC64998); https://www.openml.org/d/1106; TabBench-Bio (Table 4).
- Metric: the paper reports accuracy ("Overall classification accuracy was 78%"), no threshold, cost or k fixed, a habit of its field (MET-6), so the fallback `log_loss` (MET-8). Inputs: none.
- Risks for /add-dataset: `Too Small` first (TP-5, TP-8: 14 classes, 10 in the shortest, against `colon_tumor` at 62 rows); OpenML's copy names no preprocessing ("Source: Unknown"), so the scaling and gene filtering of the Hu6800/Hu35K arrays cannot be checked (PROV-2, LEAK-30): rebuild from the Broad's release if kept; class names mix organ sites and lineages (the paper's own label set); `Outdated` 2001 arrays (SEL-18, a note).
- Priority: gap + (multiclass thin), use case 0 (named by the source, fit approximate), source + (a PNAS paper), shape 0 (190 rows), risk - (`Too Small` likely; better data recorded).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 190 x 16,063; target: class (14 tumour types).
- Why: Tumour type from microarray expression (Global Cancer Map, Ramaswamy et al. 2001)
- Notes: 2001 microarray data.

**CC (2026-11-26, Andrej):** the better-data line is corrected.
- `tcga_pancancer_tumor_type` is no longer only a record: its definition is written and built, 9,724 tumours over
  33 cancer types against the 190 rows and 14 types here. `expo_tumor_tissue_of_origin` still has no definition.
- Verdict and priority unchanged; the reject grounds already in the record (`Too Small`, 10 samples in the shortest
  class) are untouched, and the better data is now a built dataset rather than a plan.
