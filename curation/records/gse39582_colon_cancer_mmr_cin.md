---
unique_name: gse39582_colon_cancer_mmr_cin
name: 'GSE39582: Gene expression classification of colon cancer (CIT cohort, Marisa et al. 2013)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Tiny Data
- Many features
original_source: Other
year: '2013'
domain: medical & healthcare
problem_type: Multiclass Classification
source_links:
- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE39582
- https://pubmed.ncbi.nlm.nih.gov/23700391/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: 566 colon cancers of the French CIT cohort with Affymetrix expression and lab-measured MMR (MSI by PCR) and CIN (array CGH) status, the DNA-defined subtype task the curator kept for `coad_colon_adenocarcinoma`; small and very wide, and the published matrix is normalised over the cohort, so it would be rebuilt from the CEL files.
- Source: Marisa et al. 2013, "Gene expression classification of colon cancer into molecular subtypes: characterization, validation, and prognostic value", PLoS Medicine 10(5):e1001453 (PMID 23700391), the CIT program of the Ligue Nationale Contre le Cancer; GEO GSE39582 (public 2013-05-22, SubSeries of GSE40967, platform GPL570, raw CEL files). As published (series matrix header, a preview): 585 samples, 443 discovery and 123 validation tumours ("Frozen tissue of primary colorectal Adenocarcinoma") and 19 non-tumoural mucosae; per sample sex, age, TNM, location, adjuvant chemotherapy, RFS and OS, `mmr.status` (pMMR 459, dMMR 77, N/A 49), `cin.status` (+ 369, - 112, N/A 104 with the mucosae), `cimp.status`, TP53, KRAS and BRAF mutations, `cit.molecularsubtype` (C1-C6) and the RNA extraction method. Paper: MMR from "a panel of five different microsatellite loci from the Bethesda reference panel" (MSI-high is dMMR); CIN+ when "at least 20% gain or loss of whole chromosomes or fractions of chromosomes" on array CGH.
- Use case: a molecular pathology lab assigns the DNA-defined class (dMMR, CIN+ pMMR, CIN- pMMR, close to TCGA's MSI, CIN, GS) from an expression profile; the source poses no such prediction (its six subtypes come from consensus clustering, SEL-4, and are not the target); the task follows the curator's call on `coad_colon_adenocarcinoma` (2026-10-12: "the realistic task is the DNA-defined subtype from expression and methylation"); fit approximate (MSI is tested directly by PCR or IHC in practice); regime IID (one cohort; the source's discovery and validation cut is an option).
- Siblings and duplicates: `coad_colon_adenocarcinoma` (`No`, retired 2026-10-16 for z-scores over all patients) and its rebuild `tcga_coad_molecular_subtype` (TCGA, about 480 tumours): the same task from another cohort and source, no duplicate (PROV-4); no other GSE39582 record. External collections: none known; the cohort is a common validation set in colorectal subtype papers (not read).
- Better data: no new search; found as better data for `coad_colon_adenocarcinoma`.
- Papers and pages: Marisa et al. 2013 (PLoS page read: normalisation, status definitions, sample counts); GEO (E-utilities summary and the series matrix header).
- Metric: none found for the MMR and CIN task (the paper trains only a 57-gene centroid predictor of its own subtypes, under 5% misclassification in 10-fold cross-validation, and no expression predictor of MMR or CIN); fallback `log_loss` or one-vs-rest `roc_auc` for the three classes, as for the TCGA sibling (MET-1, MET-8). Inputs: none.
- Risks for /add-dataset: the series matrix was "normalized independently in batches using the robust multi-array average method", and for the CIT set "residual technical batch effects were corrected using the ComBat method" (LEAK-30, the reason `coad_colon_adenocarcinoma` was retired): rebuild from the CEL files with a per-sample method (fRMA or SCAN), and batch effects by RNA extraction method remain; the three-class label needs both statuses, leaving roughly 450-480 tumours; 54,675 probe sets for under 500 rows; drop the 19 mucosae; the mutation and CIMP columns are lab results that may give the class away (BRAF and CIMP go with dMMR).
- Priority: gap + (multiclass is thin), use case 0 (the task is the curator's; the source poses none), source + (PLoS Medicine paper, GEO with raw files), shape 0 (under 1,000 tumours), risk - (a rebuild from CEL files to avoid the cohort-wide normalisation).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `coad_colon_adenocarcinoma`.
- as published: 585 samples (566 colon cancers + 19 non-tumoural mucosa), Affymetrix U133 Plus 2.0; per-sample mmr.status (dMMR/pMMR), cin.status (from CGH arrays, 463 tumours profiled), cimp.status, KRAS/BRAF/TP53 ...; target: DNA-defined molecular class: dMMR (MSI) / CIN+ / CIN- pMMR (close to the record's MSI / CIN / GS), each measured by a lab assay, not derived from expression; access: open.
- Why: Same task as coad_colon_adenocarcinoma and its rebuild tcga_coad_molecular_subtype (MSI / CIN / GS from expression), features of the same kind
- Adds: 566 tumours with lab-measured MMR and CIN labels, against 260 (MLOmics) or about 480 (TCGA rebuild); a second, independent cohort; the raw CEL files allow per-sample normalisation, avoiding the cohort-wide scaling that retired the record (the series matrix itself is cohort-normalised, so not that)
