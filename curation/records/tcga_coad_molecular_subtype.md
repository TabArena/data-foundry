---
unique_name: tcga_coad_molecular_subtype
name: TCGA colon adenocarcinoma molecular subtype (GDC)
tags:
- Tiny Data
- Many features
original_source: GOV Website
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://portal.gdc.cancer.gov/projects/TCGA-COAD
- https://gdc.cancer.gov/about-data/publications/pancanatlas
- https://doi.org/10.1016/j.ccell.2018.03.010
needs_review:
- suggestion
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-10-16, Lennart): new record to rebuild `coad_colon_adenocarcinoma` from the source, after that record was retired for the MLOmics release's scaling over all patients. Its task decisions carry over: multiclass CIN / MSI / GS with the 4 HM-SNV tumours dropped, no copy-number block (it defines CIN against GS), and every relevant feature kept however wide.

**Assessment (AI, 2026-10-16):** what a rebuild needs; the verdict is the curator's.
- Features: the GDC's open-access TCGA-COAD files, each normalised within its own sample only, so no value depends on another patient: RNA-seq `STAR - Counts` (TPM and FPKM per gene; 481 primary-tumour files), miRNA-seq `BCGSC miRNA Profiling` (reads per million; 455) and methylation beta values (`SeSAMe Methylation Beta Estimation`; 478, HumanMethylation450 and 27k). Counts from the GDC API on 2026-10-16.
- Not the PanCancer Atlas matrices: their batch correction is fit over all tumours, the same leak as the MLOmics z-scores. Feature filters must not use statistics over the cohort either (no variance filter).
- Labels: the PanCancer Atlas subtypes of Liu et al. 2018 (`Subtype_Selected`: GI.CIN, GI.MSI, GI.GS, GI.HM-SNV), matched by patient barcode.
- Open for `/add-dataset`: one primary-tumour sample per patient (which aliquot when there are several); patients missing an assay (keep with missing blocks, or require all three); the 27k-array samples (fewer probes); methylation per probe (about 485,000) or averaged over each gene's promoter within the sample, as MLOmics did.
- Previous version: `coad_colon_adenocarcinoma` (MLOmics, 256 patients, 36,355 features), definition in git at commit 2475ea2.

**Assessment (AI, 2026-10-31):** a newer release of this record's own source was found by the data-scouting run (PROV-6; the curator decides which one enters): TCGA gastrointestinal adenocarcinoma molecular subtypes (Liu et al. 2018) extended to rectal adenocarcinoma (TCGA-READ) (https://doi.org/10.1016/j.ccell.2018.03.010, https://portal.gdc.cancer.gov/projects/TCGA-READ). As published: Liu et al. label 921 GI adenocarcinomas (esophagus, stomach, colon, rectum); GDC API 2026-10-30: TCGA-COAD 461 cases, TCGA-READ 172 cases, both with the same STAR-Counts, miRNA and methylation files. about 1.35x the patients (COAD + READ, about 630 cases before the per-assay filters) with no new pipeline; a GDC site/project grouped split becomes possible. Version of the same source (PROV-6): the curator decides whether the rebuild takes

## Reference

Liu Y, Sethi NS, Hinoue T, et al. Comparative Molecular Analysis of Gastrointestinal Adenocarcinomas. Cancer Cell. 2018;33(4):721-735. doi:10.1016/j.ccell.2018.03.010
