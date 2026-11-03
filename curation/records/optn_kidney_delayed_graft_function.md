---
unique_name: optn_kidney_delayed_graft_function
name: 'QUOD deceased-donor kidney retrieval biopsies: RNA-seq and donor/recipient data, delayed graft function'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- AI-Filled (Verify)
- Tiny Data
- Many features
original_source: Other
year: '2024'
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE215108
- https://doi.org/10.1016/j.kint.2024.03.028
- https://github.com/TxDataIncubator/BulkFormer_with_TabPFN_RNA-Seq_Kidney_Transcriptomics
- https://doi.org/10.1038/s41598-026-68541-3
- https://doi.org/10.21203/rs.3.rs-9242336/v1
- '# not this dataset: the OPTN/SRTR registry files the run named as registry-scale data for the same target (see the screening block)'
- https://srtr.hrsa.gov/requesting-data/about-srtr-standard-analysis-files-safs/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: 271 deceased-donor kidneys profiled by RNA-seq at retrieval (Cambridge, UK QUOD biobank) with delayed graft function after transplant; a real outcome, but tiny, p >> n, and the retrieval-biopsy transcriptome is a research assay, so the fit to an organ-offer decision is approximate.
- Record fix: the record is the QUOD cohort (its `name`, its links and the run's alias `quod_kidney_biopsy_delayed_graft_function`). The `unique_name` and the SRTR link come from the run's note on registry-scale data for the same target (the OPTN/SRTR kidney files), which has no record of its own. The name stays (records.md); the SRTR link now carries a note.
- Source: Zhang, Trotter, ..., Clatworthy, "Assessment of biological organ age using molecular pathology in pre-transplant kidney biopsies", Kidney Int. 106(2):302-316 (2024, doi 10.1016/j.kint.2024.03.028, PMID 38692408; erratum 2025): "we profiled the transcriptomes of 271 kidneys from deceased donors at retrieval" and assessed pathways "that associated with delayed, and sub-optimal one-year graft function". GEO GSE215108 (public 2024-08-16): 303 samples, raw and normalised count matrices, and per sample only the tissue, "delayed graft function" (98 Yes, 173 NO, 32 Unknown) and a "person id" that repeats across samples. The donor and recipient table sits in the TxDataIncubator repository (github.com/TxDataIncubator/BulkFormer_with_TabPFN_RNA-Seq_Kidney_Transcriptomics, MIT; "All of the data is as provided by the authors of the above manuscripts"): `QUOD_retrieval_biopsy_samples_metadata.csv`, 271 rows (all DCD donors; `DGFyn` 98 Yes, 173 NO), with donor type, side, donor age, BMI, sex, cause of death, terminal creatinine, cardiac disease, diabetes, hypertension and smoking, recipient age, BMI and sex, cold ischaemia time, HLA mismatch group, Remuzzi score, eGFR at 3 and 12 months, rejection counts, DGF days and DGF yes/no; plus a 21 MB raw count matrix.
- Use case: at a kidney offer, after the retrieval biopsy, the transplant team weighs the risk of delayed graft function when deciding whether to use the kidney, for which recipient, and whether to perfuse it (the paper: "Methods of accurately stratifying marginal donor organs by clinical and histological assessment are lacking"); fit approximate, since retrieval-biopsy RNA-seq is not routine and the recipient columns are known only once the kidney is allocated. Regime: grouped by donor if the GEO `person id` marks the two kidneys of one donor (to check; the repository's `Donor_ID` is unique per row), else IID.
- Siblings and duplicates: no other QUOD or GSE215108 record (grep: graft, transplant, GSE215108); `optn_liver_waitlist_90day_mortality` (`TBD -> Yes`) is the OPTN liver task; `transplant` (`No`) is unrelated; `lung_cancer_epithelial_genexp` is the wide-table precedent. External collections: none.
- Better data: from the curator's Zotero collection, item 288; no new search this run. The run's note names the OPTN/SRTR registry files (https://srtr.hrsa.gov/requesting-data/about-srtr-standard-analysis-files-safs/) as registry-scale data for the same target, with clinical columns of the same kind and no transcriptome; no record holds that task.
- Papers and pages: the Kidney Int. paper (abstract read); "Combining BulkFormer and TabPFN to predict post-transplant function from kidney biopsies", Sci. Rep. 2026 (doi 10.1038/s41598-026-68541-3; the page redirects to a login) and its Research Square preprint (doi 10.21203/rs.3.rs-9242336/v1), whose supplementary table reports 263 QUOD patients and a c-statistic near 0.54 for a transcriptome model (from a search snippet, not read).
- Metric: the c-statistic (ROC AUC), by which the preprint ranks its top models (supplementary figure and table, seen only in a search snippet), so `roc_auc` (MET-5, MET-8); inputs none.
- Risks for /add-dataset: the post-transplant columns go (eGFR at 3 and 12 months, rejection counts, DGF days; LEAK-10); the Remuzzi score is a pathologist's grading of the biopsy, kept only if it is a clinical input in practice (SEL-13, SEL-14); paired kidneys of one donor (SPLIT-29); about 98 positives in 271, so about 20 per test fold (TP-5); the clinical table comes from a third party's repository rather than the paper's supplement, so check it against the paper (PROV-8, PROV-15); the counts differ between sources (263 with outcome in the preprint, 271 profiled, 303 GEO samples).
- Priority: gap 0 (medical & healthcare and binary are not thin), use case 0 (approximate: a research assay at retrieval), source + (Kidney Int. paper and GEO), shape 0 (271 kidneys, p >> n), risk - (leak columns, a third-party clinical table, possible donor pairs).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 288: "Combining BulkFormer and TabPFN to predict post-transplant function from kidney biopsies ...".
- as published: 263 kidneys with outcome (73 DGF, 27.8%) of the 271 profiled (GEO lists 303 samples). The metadata has about 28 columns: donor type (DCD/DBD), side, donor age, BMI, sex, cause of death, terminal ...; target: delayed graft function (dialysis in the first week after transplant, not counting dialysis only in the first 24 h), yes/no; alternative: eGFR at 12 months; access: open, request.
- Why: Real deceased-donor cohort with a hard outcome, public counts plus clinical metadata, and a published prediction study on it (Sci Rep 2026); a wide-table regime (p >> n) like lung_cancer_epithelial_genexp. | Better data for the target of item 288. It works at registry scale, with features of the same kind as the QUOD ...
- Adds: A transplant-organ task with clinical and transcriptome columns. Tiny and p >> n: the transcriptome alone reached a c-statistic of only 0.59 in the paper, so the donor and recipient columns will carry most signal. Caveats: post-transplant columns (eGFR3, eGFR12, rejection counts, DGF_days) must go (LEAK). Remuzzi is ...
