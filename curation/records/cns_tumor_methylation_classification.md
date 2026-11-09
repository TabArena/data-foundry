---
unique_name: cns_tumor_methylation_classification
name: DNA methylation-based classification of human central nervous system tumors [reference set], GEO GSE90496
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 4
decision_markers:
- Needs extensive data wrangling
- Class-dependent Recording
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
v2_path: datasets/_dev/tabarena-v0pt2/cns_tumor_methylation_classification/dataset.py
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

**Assessment (AI, 2026-11-08):** size check for the large-datasets review: 2,801 tumours and controls (one per patient) x 428,799 probes after the paper's filters (485,577 on the array), 91 classes; the call stands at priority 3. Only the reference set has usable labels: the validation set's classes are the classifier's own calls.
- As published: GEO GSE90496 [reference set] (public 2018-01-14, a sub-series of GSE109381; https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE90496) holds 2,801 samples, "n=2801 patients" (overall design) and "2,801 biologically independent samples" (Extended Data Fig. 1). `GSE90496_beta.txt.gz` is 9.2 GB: a probe x (beta, detection p) table whose header has 5,603 columns (ID plus 2 x 2,801; previewed). GEO's processing is minfi `preprocessIllumina`, applied per sample. `GSE90496_RAW.tar` is 23 GB, with 5,602 IDATs (two per sample, `filelist.txt`), plus a 17 KB class-description xlsx. The 102 KB series matrix carries `methylation class` (91 values) and `material` (FFPE 1,878, Frozen 923). The validation set, GSE109379, has 1,104 samples, `GSE109379_processed_data.txt.gz` (373 MB), 9.0 GB of IDATs, `methylation class` (69 values, 16 of them with one sample) and `material` (DNA_FFPE 1,094, DNA_KRYO 10). The paper's QC subset is "removal of probes targeting the X and Y chromosomes (n=11,551), ... single-nucleotide polymorphism ... (n=7,998), probes not mapping uniquely ... (n=3,965), and probes not included on the Illumina EPIC array (n=32,260). In total, 428,799 probes targeting CpG sites were kept" (Methods). The classifier then used the 10,000 probes with the highest random-forest importance, a supervised selection that belongs inside the folds (LEAK-31).
- The task's table: 2,801 rows x 428,799 probes (stated; the filters use only the manifest and SNP annotation, no labels), plus `material`; 485,577 probes without the filters. Classes: 91 (82 tumour classes, 9 control classes with 119 samples). The smallest: 7 classes of 8 samples, 18 classes of 10 or fewer, 41 below 20 (counted in the series matrix). Under 5 folds an 8-sample class has 1-2 per test fold (TP-5, TP-8 to check). Without the controls: 2,682 rows and 82 classes.
- Access: open on GEO, no login, no licence stated; 9.2 GB of betas or 23 GB of IDATs.
- Changes the call: (1) The validation set's labels are model output. The paper assigned the 1,104 cases "as either 'matching to a defined DNA methylation class' (calibrated score ≥0.9) or as 'no match' cases (highest score <0.9)" (Results, "Clinical implementation"), yet GEO gives every one of the 1,104 a class, so the GEO class is the classifier's top call and not a diagnosis (USE-5). The pathology diagnosis of each validation case is in Supplementary Table 4 (not read). The task is the 2,801 reference samples. (2) Material is tied to class: 35 of 91 classes are FFPE only or frozen only (591 samples), and 47 have 90% or more of one material. The paper removed it per probe with `removeBatchEffect`, estimated inside the cross-validation. The GEO betas are per sample and do not carry that correction, so LEAK-30 does not apply, but material is a shortcut to check. It is known to the lab, so it is a fair input. (3) 35 reference arrays (and 5 validation arrays) are also in `sarcoma_methylation_classification`'s GSE140686. They share the same chip and position IDs in both file lists, and both give them the matching class: schwannoma 10, melanoma 8, solitary fibrous tumour 7, chordoma 7, Ewing sarcoma 3. The tasks are distinct (PROV-7), but if both ship, drop the shared tumours from one. (4) Better data: the Heidelberg classifier v12.8 is trained on 7,495 profiles in 184 subclasses (Sill et al., medRxiv 2025, seen in a search result); no public deposit was found. The priority stays 3.
- Not checked: Supplementary Table 2 (the reference cohort's centres and patient fields); the beta file's probe row count and missing values (9.2 GB, only the header was read); the v12.8 cohort beyond one search.

CC (2026-11-08, Lennart): accepted for adding (`Yes`) in the screening review of the large candidates (most rows, most features).

**Assessment (AI, 2026-11-08):** distinct from sarcoma_methylation_classification although 40 arrays are in both (35 of GSE90496, 5 of GSE109379): a CNS tumour classifier (91 classes) against a sarcoma classifier (65 classes), two tasks of one source line (PROV-7). /add-dataset decides whether the shared arrays leave one.

**Assessment (AI, 2026-11-09):** review panel (full): ship after changes (five text fixes made: the 27/29 count, the 10-15% chip optimism in splits_comment, the `Class-dependent Recording` marker for the material, the 35/40 shared-array note, the fit note; plus a LEAK-9 protocol line on test-batch rebalancing); keep the 91 classes until a class-by-class check against WHO 2021; disputed: SEL-4 (clustering-drawn subclasses), MET-5 (optional scoring column); for the curator: issues 1-3 (3: accept the stratification warning). Priority 4: gap + (multiclass thin), use case + (classifier in routine neuropathology), source + (Nature paper, GEO), shape + (2,801 patients, 428,800 features), risk - (open SEL-4 Must on part of the classes). Up from the screening's 3: shape moves from 0 to +, because the width is what the curator chose the large-candidates batch for (CC 2026-11-08).
