---
unique_name: metabric_breast_cancer_clinical
name: METABRIC breast cancer cohort, clinical data (Curtis et al. 2012; cBioPortal brca_metabric)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: Other
year: '2012'
domain: medical & healthcare
problem_type: Binary Classification
source_links:
- https://doi.org/10.1038/nature10983
- https://www.cbioportal.org/study/summary?id=brca_metabric
- https://doi.org/10.1038/ncomms11479
- https://doi.org/10.1038/s41586-019-1007-8
- '# the curator''s Zotero item 67: TCGA BRCA clinical data, not METABRIC; related work (PROV-12)'
- https://arxiv.org/abs/2507.06243
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: the clinical records of the METABRIC cohort (2,509 primary breast tumours on cBioPortal, with overall and relapse-free survival and cause of death), framed as death within five years of diagnosis from what is known after surgery; a well-documented cohort, with expression-derived subtype columns and treatment columns to settle.
- Source: Curtis et al., "The genomic and transcriptomic architecture of 2,000 breast tumours reveals novel subgroups", Nature 486, 2012 (doi 10.1038/nature10983); extended by Pereira et al., Nat Commun 7:11479, 2016 ("2,433 primary breast tumours that have copy number aberration (CNA), gene expression and long-term clinical follow-up data") and Rueda et al., Nature 2019 (doi 10.1038/s41586-019-1007-8, relapse). As served: cBioPortal study `brca_metabric` ("Targeted sequencing of 2509 primary breast tumors with 548 matched normals", public; allSampleCount 2509), 36 clinical attributes, among them age at diagnosis, breast surgery, cellularity, chemotherapy, hormone and radio therapy, ER (IHC) and status, PR, HER2, grade, histological subtype, inferred menopausal state, laterality, positive lymph nodes, NPI, tumour size and stage, `COHORT`, `OS_MONTHS`, `OS_STATUS`, `RFS_MONTHS`, `RFS_STATUS`, `VITAL_STATUS`, and the expression-derived `CLAUDIN_SUBTYPE`, `INTCLUST`, `THREEGENE` (cBioPortal API).
- Use case: an oncologist, after surgery and pathology, estimates the prognosis to decide on adjuvant therapy; fit approximate: the METABRIC papers are discovery studies and name no decision (USE-8). Target: death within 60 months of diagnosis from `OS_MONTHS` and `OS_STATUS`, dropping patients censored earlier; death of disease from `VITAL_STATUS` is the alternative (USE-5, the curator's choice). Regime IID (one patient per row), or grouped by `COHORT` (the contributing tumour banks; SPLIT-26), to decide at /add-dataset.
- Siblings and duplicates: `haberman_survival` (`No`: Trivial, Outdated, 306 patients) and `ljubljana_breast_cancer` (`Yes`, BeyondArena, recurrence after surgery, 286 patients), the tasks this would extend; `rotterdam_breast_cancer`, `seer_breast_cancer_5y_survival` and `seer_breast_cancer_survival` (no verdict yet) are other sources of the same task (PROV-4); `brca_breast_cancer` (`No`: PAM50 labels from clustering, SEL-4) is the precedent for the subtype columns. No other record links `brca_metabric` or nature10983. External collections: pycox (`metabric`, 1,904 patients, a survival benchmark; its README).
- Better data: found as better data for `haberman_survival` and `ljubljana_breast_cancer`, and in the curator's Zotero collection (item 67); no further search this round. Item 67 (arXiv 2507.06243, Hasan et al. 2025) is about other data: "This study utilizes The Cancer Genome Atlas (TCGA) breast cancer clinical dataset to develop ML models for predicting the likelihood of undergoing chemotherapy or hormonal therapy" (abstract), so its link is marked as related work (PROV-12).
- Papers and pages: Pereira et al. 2016 (abstract via Crossref); Curtis et al. 2012 and Rueda et al. 2019 (not read); the cBioPortal study page and API (read).
- Metric: none found for a five-year classification (the source papers are discovery studies; pycox scores survival models by concordance, another problem type), so the fallback `roc_auc` (MET-1, MET-8); inputs none.
- Risks for /add-dataset: `CLAUDIN_SUBTYPE` (PAM50 and claudin-low), `INTCLUST` (integrative clusters) and `THREEGENE` come from expression clustering or classifiers (SEL-4 is about such labels as targets; as features, keep or drop them by what is measured at the prediction point, USE-3); `NPI` is a fixed formula of size, grade and nodes (a redundant feature); chemotherapy, hormone and radio therapy are chosen after the prognosis the task makes (USE-4: drop, unless the task is the prognosis under the planned treatment); censoring before 60 months (LEAK-22 to LEAK-26); the full METABRIC data is controlled access, but the clinical table is public on cBioPortal.
- Priority: gap 0 (medical and binary are not thin), use case 0 (no decision named by the source), source + (Nature papers and a public portal), shape + (about 2,500 patients, mixed clinical features, a cohort column), risk - (expression-derived and post-decision columns, a target to build under censoring).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `haberman_survival`, `ljubljana_breast_cancer`; the curator's Zotero collection, item 67: "A Machine Learning Framework for Breast Cancer Treatment Classification Using a Novel ...".
- as published: 2,509 primary breast tumours on cBioPortal (study API: allSampleCount 2509, 1,980 with expression). Clinical columns: age at diagnosis, tumour size and stage, grade, positive lymph nodes, ...; target: death (or death of disease) within 5 years of diagnosis, from overall survival months and status, with patients censored before 5 years dropped; access: open.
- Why: Same task as haberman_survival (5-year survival after breast cancer surgery). Age and positive nodes are among the features, and all clinical features are known at surgery. | the same target as ljubljana_breast_cancer (recurrence events after breast-cancer surgery) with features of the same kind, nearly column for ...
- Adds: About 1,900-2,500 patients against 306, and more recent diagnoses. Adds receptor status, grade, size and treatment. Also has a cause of death, so breast-cancer death can be told apart from other deaths. Could replace or sit beside the Rotterdam hit, which is closer in setting. Leave the PAM50 and expression-derived ...
