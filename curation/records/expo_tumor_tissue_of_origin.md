---
unique_name: expo_tumor_tissue_of_origin
name: Expression Project for Oncology (expO), GEO series GSE2109
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Many features
original_source: Other
year: '2005'
domain: medical & healthcare
problem_type: Multiclass Classification
source_links:
- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE2109
- '# Stiglic and Kokol 2010 (GEMLeR), which names GSE2109 as the source of its sets'
- https://pmc.ncbi.nlm.nih.gov/articles/PMC2896709/
- https://ftp.ncbi.nlm.nih.gov/geo/series/GSE2nnn/GSE2109/matrix/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: IGC's expO series (GEO GSE2109), the origin of GEMLeR's OVA and AP sets: 2,158 tumours on one array platform with clinical annotation, for the single multiclass tissue-of-origin task the curator asked about in `ova_breast` instead of nine one-vs-rest copies; a version of the same source (PROV-6).
- Source: International Genomics Consortium (IGC), Expression Project for Oncology (expO), GEO series GSE2109 (submitted 2004-12-23, public 2005-01-15, last update 2019-03-25; samples deposited in 16 batches, 2004-2008). GEO summary: "The goal of expO and its consortium supporters is to procure tissue samples under standard conditions and perform gene expression analyses on a clinically annotated set of deidentified tumor samples. The tumor data is updated with clinical outcomes and is released into the public domain without intellectual property restriction." As published: 2,158 samples on Affymetrix HG-U133 Plus 2.0 (GPL570, 54,675 probes), a series matrix and the raw CEL files; per sample, free-text annotation lines (read from a preview of the series matrix): age band, gender, ethnic background, tobacco and alcohol use, family history, days from diagnosis to excision, pathological TNM, stage and grade, and "Primary Site"; sample titles name the site ("Breast - 13491", "Corpus Uteri - 2045").
- Use case: a pathologist or oncologist, for a metastatic cancer of unknown primary, identifies the tissue of origin from the tumour's expression profile to choose a site-specific treatment (the use of commercial tissue-of-origin tests); fit approximate: expO holds tumours of known primary site at excision, standing in for the unknown-primary case; regime IID (one sample per tumour; the deposit batch is to check).
- Siblings and duplicates: `ova_breast` (`TBD -> Yes` with `Missing source information`, `Data Quality Issue` and `Needs extensive data wrangling`; GEMLeR's one-vs-rest cut of these samples, 1,545 samples and about 10,935 probes after a variance filter, the record this was found for) and GEMLeR's other OVA and AP cuts on OpenML (OVA_Colon, OVA_Endometrium, OVA_Kidney, OVA_Lung, OVA_Omentum, OVA_Ovary, OVA_Prostate, OVA_Uterus; AP_* pairs), versions of this source (PROV-6: the curator decides which one enters); `tcga_pancancer_tumor_type` (the same task from TCGA RNA-seq, about 10,000 tumours, another source, PROV-7); `treehouse_pediatric_tumor_type` (paediatric tumours). External collections: TabSTAR, TabBench-Bio and TabArena Reject through the OVA cut (`ova_breast`); OpenML (GEMLeR uploads).
- Better data: found as better data for `ova_breast` (the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: Stiglic and Kokol, "Stability of Ranked Gene Lists in Large Microarray Analysis Studies", J Biomed Biotechnol 2010:616358 (PMC2896709), Sect. 2: "The original data were obtained from the Expression Project for Oncology (expO) data set from The International Genomics Consortium ... accession number GSE2109", "normalized using MAS5", and "prefiltering using maximal variance of signal where 20% of probes with the highest variance were retained".
- Metric: none found for the multiclass task (the GEMLeR paper studies gene-list stability and reports accuracy and AUC on two-class cuts), so the fallback `log_loss` (or multiclass `roc_auc`); inputs none.
- Risks for /add-dataset: the label is parsed from free-text annotation (site names to harmonise, such as "Corpus Uteri" and "Uterus"; metastatic samples to check); rare sites with few samples (TP-5, TP-8: merge or drop below a floor); deposit batches 2004-2008 may line up with tissue (check batch against site); take per-array values (MAS5 per array, or re-normalise each CEL file), never a normalisation or filter fit over all samples (LEAK-30); the clinical lines (stage, metastatic sites) can name the site (LEAK-10); 54,675 features (width is no reason to drop, CLEAN-22).
- Priority: gap + (multiclass thin), use case 0 (no decision named by the source), source + (IGC deposit with per-sample annotation, GEO), shape 0 (2,158 samples, one feature type), risk - (labels from free text, rare sites, batches).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `ova_breast`.
- as published: 2,158 tumour samples on Affymetrix HG-U133 Plus 2.0 (GPL570, 54,675 probes), with per-sample clinical annotation including the tissue / primary site (GEO esummary, read 2026-10-30); target: tumour tissue of origin (multiclass); GEMLeR's OVA_* sets are one-vs-rest cuts of 9 of these tissues; access: open.
- Why: The record says the original source is lost. Stiglic and Kokol 2010 (Sec. 2, Methods and Data Sets): 'The original data were obtained from the Expression Project for Oncology (expO) ... deposited at Gene Expression Omnibus (GEO) ..., accession number GSE2109. Samples from this collection represent an integral part of ...
- Adds: All 2,158 samples (GEMLeR OVA: 1,545) and all tissues, all 54,675 probes instead of the ~10,935 left after GEMLeR's unsupervised filter, the clinical annotations, and the single multiclass task the curator asked for instead of nine OVA copies. Version of the same source (PROV-6)
- A newer release of the same source as the record(s) named above (PROV-6): the curator decides which one enters.
