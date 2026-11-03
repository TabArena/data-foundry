---
unique_name: cns_tumor_methylation_classification
name: DNA methylation-based classification of human central nervous system tumors [reference set], GEO GSE90496
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
year: '2018'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Multiclass Classification
source_links:
- https://doi.org/10.1038/nature26000
- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE90496
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the DKFZ reference set behind the CNS tumour methylation classifier used in routine neuropathology, 2,801 samples in 91 classes. It is wide (450k probes, 9.2 GB of beta values), and part of its classes were defined by clustering the same profiles.
- Source: Capper et al., "DNA methylation-based classification of central nervous system tumours", Nature 555:469-474 (2018) (https://doi.org/10.1038/nature26000, read on PMC6093218). The data is GEO GSE90496 "[reference set]" (submitted 2016-11-25, public 2018-01-14), a sub-series of GSE109381, which also holds the prospective validation set; read 2026-10-31. As published: 2,801 Illumina 450k profiles ("from n=2801 patients"), a 9.2 GB matrix of beta values (`GSE90496_beta.txt.gz`), 23 GB of IDATs and a class description file. The label is the sample characteristic "methylation class": 82 tumour classes and 9 control classes, at least eight cases per group.
- Use case: a neuropathologist assigns a CNS tumour to a diagnostic class from its methylation profile after surgery. The authors offer "a free online classifier tool" and apply it "in a routine diagnostic setting", "resulting in a change of diagnosis in up to 12% of prospective cases" (abstract). Fit direct. Regime IID over patients (one sample each; the contributing centres were not checked).
- Siblings and duplicates: `sarcoma` (`Yes`, TCGA, 201 patients) is a related task; its use case cites the same lab's sarcoma classifier. `sarcoma_methylation_classification` (a new record of this run, Koelsche et al. 2021) applies the same method to sarcomas, a different task (PROV-7). `glioblastoma` (`No`, SEL-4) and `lgg_low_grade_glioma` (`No`) are TCGA cuts. No record of GSE90496 or GSE109381 existed before this run. External collections: not checked (web search budget used up).
- Better data: found next to `sarcoma` (a related task, the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: the Nature paper. Maros et al. (Nature Protocols 2020) compare classifiers on this set (not read here).
- Metric: Capper et al. assessed the cross-validated classifier "by the misclassification error, multiclass area under the curve (AUC) and the multiclass Brier score" (Methods, "Classifier performance measures"). These are three metrics side by side, none named as the criterion, so the fallback `log_loss` (MET-5, MET-8). The paper's calibrated-score threshold of 0.9 decides whether a sample gets a class at all, not which class, so MET-7 does not apply. Inputs none.
- Risks for /add-dataset: the label comes partly from unsupervised clustering. "All histopathological entities and variants were analysed by unsupervised clustering"; of the 82 tumour classes, "Twenty-nine of these were equivalent to a single WHO entity (category 1), 29 represented subclasses within a WHO entity (category 2)", and 11 cut across WHO boundaries (category 4). SEL-4 then calls for re-targeting to the WHO entity or to the eight methylation class families, or for keeping only the classes the clinic diagnoses; the curator decides. The 485k probes in a 9.2 GB file need a probe selection that must not see the test rows (LEAK-31). The smallest classes have about 8 samples, 2-3 per test fold (TP-5, TP-8). The control tissue classes are not tumours: keep or drop them (USE-8).
- Priority: gap + (multiclass is thin, 24 accepted), use case + (the source runs it in routine diagnostics), source + (Nature paper, GEO), shape 0 (2,801 samples, but one kind of feature and classes of about 8), risk - (clustering-defined classes, probe selection).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `sarcoma`.
- as published: 2,801 patients (2,682 tumours in 82 CNS tumour classes plus controls), Illumina 450k array per sample; the methylation class is a GEO sample characteristic; target: CNS tumour methylation class (multiclass); access: open (GEO).
- Why: the strongest public methylation-classification task: a real diagnostic tool in routine use, a documented label per sample, 14x the units of sarcoma; no record for it (glioblastoma, lgg_low_grade_glioma are MLOmics/TCGA cuts)
- Adds: a second wide-omics multiclass task at scale; risks as for the sarcoma reference set (some classes defined by methylation clustering, 450k probes wide)
