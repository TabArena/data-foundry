---
unique_name: tcga_lung_histology
name: TCGA lung adenocarcinoma and lung squamous cell carcinoma RNA-seq (GDC, TCGA-LUAD and TCGA-LUSC)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: medical & healthcare
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://portal.gdc.cancer.gov/projects/TCGA-LUAD
- https://portal.gdc.cancer.gov/projects/TCGA-LUSC
- https://doi.org/10.1038/nature13385
- https://doi.org/10.1038/nature11404
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: TCGA lung adenocarcinoma and squamous cell carcinoma RNA-seq on the GDC (1,051 primary tumours and 110 normal lung samples from 1,019 patients), the pathology-assigned histological type as target; about five times the tumours of `lung_cancer` on a current platform, with an expected near-separable task.
- Source: The Cancer Genome Atlas Research Network, "Comprehensive genomic characterization of squamous cell lung cancers", Nature 489:519 (2012, 10.1038/nature11404), and "Comprehensive molecular profiling of lung adenocarcinoma", Nature 511:543 (2014, 10.1038/nature13385); the data harmonised on the NCI GDC (TCGA-LUAD, TCGA-LUSC), one STAR-Counts expression file per aliquot (about 60,660 genes). GDC API, 2026-10-31, open files: LUAD 540 primary tumours, 59 solid tissue normal, 2 recurrent; LUSC 511 primary, 51 normal; 1,163 files from 1,019 cases. Clinical tables (age, sex, smoking, stage) join per case.
- Use case: a pathologist types a non-small-cell lung cancer as adenocarcinoma or squamous carcinoma, which sets the treatment and the molecular tests; on small or poorly differentiated biopsies an expression classifier can help; fit approximate, since resected tumours of settled histology stand in for the ambiguous biopsy, and pathology with immunostains decides today (USE-8). Regime: grouped by patient when the normal samples stay (most pair with a tumour of the same patient); with tumours only, nearly one sample per patient.
- Siblings and duplicates: `lung_cancer` (`Yes`, shipped; Bhattacharjee 2001, 203 samples, five classes including normal lung) is the record it was found for. `tcga_brca_tumor_vs_normal_rnaseq` (`TBD -> 2nd Tier`) and `tcga_hnsc_tumor_vs_normal_rnaseq` (a proposed `No` under USE-2: tumour against normal tissue is fixed at procurement, no decision fits) bear on whether the normal class belongs here. `tcga_pancancer_tumor_type` holds these tumours among 33 types (another task, PROV-7), `treehouse_pediatric_tumor_type` re-processes them, and `tcga_coad_molecular_subtype` is the precedent for a per-sample GDC build. External collections: none found for this cut.
- Better data: found as better data for `lung_cancer`.
- Papers and pages: the two TCGA papers; https://portal.gdc.cancer.gov/projects/TCGA-LUAD and https://portal.gdc.cancer.gov/projects/TCGA-LUSC.
- Metric: none found (the GDC project pages; the two TCGA papers characterise the tumours and build no histology classifier, not read in full), so the fallback `roc_auc` for adenocarcinoma against squamous, `log_loss` if the normal class stays; inputs: the patient barcode as the group, never a feature.
- Risks for /add-dataset: the framing: adenocarcinoma against squamous (binary, the decision) or with normal lung as a third class (as `lung_cancer`; the HNSC call argues against it, USE-2), so `problem_type` is left open; expected near-trivial, since the markers pathology stains for (TTF-1 from NKX2-1, p40 from TP63) separate the two (compare one gene with the methods, TP-4); tissue source sites and plates differ between the two projects, a batch shortcut to check; per-sample values, no matrix normalised over all samples (LEAK-30); about 60,660 columns (width is no reason to drop, CLEAN-22).
- Priority: gap 0 (binary in the recommended framing; multiclass would add one), use case 0 (the curation's), source + (TCGA papers and the GDC), shape + (1,163 samples of 1,019 patients, expression plus clinical fields), risk - (expected near-trivial, project batch).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `lung_cancer`.
- as published: STAR-Counts gene expression files (GDC API, 2026-10-30): LUAD 540 primary tumours + 59 normal lung, LUSC 511 primary tumours + 51 normal, 1,161 samples; about 60,000 genes, each file normalised ...; target: Histological type: adenocarcinoma / squamous cell carcinoma / normal lung (pathology-assigned); access: open.
- Why: Same target (histological lung tumour type from mRNA expression) and same kind of features as lung_cancer (203 samples, 2001, five classes)
- Adds: About 6x the samples, RNA-seq instead of an early Affymetrix chip, per-sample normalised files (no cohort-wide scaling, as in the tcga_coad_molecular_subtype rebuild), patient barcodes for grouping; caveat: no carcinoid or small-cell class

**Assessment (AI, 2026-11-10):** lung_cancer, the dataset this record was found to improve on, was retired on 2026-11-10 (`No Good Target / Scientific Discovery`): the histology of resected tumours is settled by the slide, so no decision rests on predicting it from expression; molecular typing matters on ambiguous small biopsies and tumours of unknown origin. The same question applies to this record's rows (TCGA resections with a pathology diagnosis); unless it holds such cases or another target with a decision behind it, the same verdict would follow. The record's verdict stays the curator's.

**Assessment (AI, 2026-11-11):** lung_cancer's arrays ship on as `lung_adenocarcinoma_metastasis`, with the study's flag of a possible metastasis from another organ (written in the tumour's pathology note but resting on an earlier cancer outside the specimen); lung_cancer's histology stays retired, so the question above still applies to this record's histology label. The record's verdict stays the curator's.
