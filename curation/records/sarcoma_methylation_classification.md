---
unique_name: sarcoma_methylation_classification
name: 'Sarcoma classification by DNA methylation profiling: reference set (1,077) and validation set (428), GEO GSE140686'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Many features
original_source: Other
year: '2020'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Multiclass Classification
source_links:
- https://doi.org/10.1038/s41467-020-20603-4
- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE140686
- https://www.molecularsarcomapathology.org
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the DKFZ sarcoma reference set behind the online sarcoma methylation classifier, 1,077 tumours from as many patients in 62 tumour and 3 control classes. It is very wide, and its classes were designated by clustering the same profiles, though 48 of the 62 tumour classes match one WHO entity.
- Source: Koelsche et al., "Sarcoma classification by DNA methylation profiling", Nature Communications 12:498 (2021) (https://doi.org/10.1038/s41467-020-20603-4, read on Europe PMC, PMC7819999). Data: GEO GSE140686 (submitted 2019-11-19, public 2020-03-01), "DNA methylation classification reference set (1077) and validation set (428) of 1505 sarcoma samples" on 450k (GPL13534) and EPIC (GPL21145) arrays; a processed matrix and a signal-intensity matrix per platform, plus the IDATs (`GSE140686_RAW.tar`). The GEO sample characteristics carry no class ("tissue: sarcoma", "material preparation: FFPE"); "Supplementary Data 1 indicates the IDAT file names for each case", with age, sex and location. After the paper's probe filters, 428,230 probes remain.
- Use case: a pathologist confirms or revises the type of a soft-tissue or bone tumour from its methylation profile at diagnosis. The authors run "a free upload service" at molecularsarcomapathology.org; in the validation cohort, of 59 cases where histology and a confident prediction disagreed, "The initial diagnosis was revised in favour of the predicted methylation class in 29/59 cases". Fit direct for the reference classes. Regime IID by patient ("All samples of the reference and validation set are from individual/different patients"); the contributing centres were not checked.
- Siblings and duplicates: `sarcoma` (`Yes`, TCGA, 201 patients, 4 classes) is the same task from another source, so its own record and no duplicate (PROV-4). `cns_tumor_methylation_classification` (`TBD -> Yes`, the same lab's CNS reference set) and `srbct_prediction` (the small-round-cell differential, by expression) are related tasks. No other record of GSE140686. External collections: not checked (web search budget used up).
- Better data: found as better data for `sarcoma` (the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: the Nature Communications paper; molecularsarcomapathology.org.
- Metric: the paper reports for cross-validation "an estimated error rate of 1.95% for raw scores and 0.65% for calibrated scores and a multi-class area under receiver operating characteristic curve of 0.99 and a Brier score of 0.05" (Results, "Development of the sarcoma classifier"): three metrics side by side, none named as the criterion, so the fallback `log_loss` (MET-5, MET-8; as for `cns_tumor_methylation_classification`). The calibrated-score cut-off of 0.9 decides whether a case gets a class at all, not which one, so MET-7 does not apply. Inputs none.
- Risks for /add-dataset: the classes come from "Unsupervised clustering, respecting the minimal number of seven cases per group": 48 "corresponded to distinct WHO entities (category 1)", 9 are subsets of a WHO entity (category 2), 3 combine entities (category 3) and 2 are novel entities (category 4). SEL-4 asks to re-target the category 2 and 4 classes to the WHO entity or drop them; the curator decides. The paper corrected material and array type with `removeBatchEffect` over all samples: if the GEO processed matrix carries this, rebuild from the IDATs per sample or note it (LEAK-30). A probe selection must not see the test rows (LEAK-31). Classes of 7 cases leave 1-2 per test fold (TP-5, TP-8). The 3 control classes are not tumours (USE-8). The labels join by IDAT name; where the validation set's labels are published was not found.
- Priority: gap + (multiclass thin, 24 accepted), use case + (the source runs the classifier for diagnosis), source + (Nature Communications, GEO), shape 0 (1,077 samples, one kind of feature, classes of 7), risk - (clustering-designated classes, batch correction, probe selection).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `sarcoma`.
- as published: 1,505 sarcoma samples, one per patient: reference set 1,077 cases in 62 tumour + 3 control methylation classes, validation set 428; Illumina 450k (GPL13534) and EPIC (GPL21145) arrays, IDATs plus ...; target: methylation class / sarcoma type of the tumour (the same quantity as sarcoma's reviewed histological type, across 62 soft-tissue and bone types instead of 4); access: open (GEO; labels in the paper's Supplementary Data 1).
- Why: same task as sarcoma (type a sarcoma from its omic profile; the record's own use case cites Koelsche et al. 2021 as the real use) with the same kind of features (per-sample methylation beta values) known at diagnosis; also covers the small-blue-round-cell differential (Ewing, rhabdomyosarcoma, CIC/BCOR, an SBRCT ...
- Adds: 5x the patients (1,077 against 201), all sarcoma types instead of 5 TCGA types, per-sample IDATs so no all-patient preprocessing (the sarcoma record's kept leak); risks: very wide (450k/850k probes, two array types), category-4 classes were defined from methylation clusters (label partly derived from the features), ...
