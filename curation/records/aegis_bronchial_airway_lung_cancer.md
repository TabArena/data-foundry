---
unique_name: aegis_bronchial_airway_lung_cancer
name: 'AEGIS-1 and AEGIS-2 bronchial airway gene expression (GEO GSE66499): validation of an airway gene-expression classifier for lung cancer'
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Lennart
suggestion: TBD -> Yes
priority: 3
tags:
- Many features
- AI-Filled (Verify)
original_source: Other
year: '2015'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://doi.org/10.1056/NEJMoa1504601
- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE66499
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: bronchial-airway gene expression of 639 smokers with suspected lung cancer from two prospective multicentre trials (AEGIS-1 and AEGIS-2, NEJM 2015), the task of `lung_cancer_epithelial_genexp` (Spira 2007, 187 patients) with 3.4 times the patients.
- Source: Silvestri et al., "A Bronchial Genomic Classifier for the Diagnostic Evaluation of Lung Cancer", NEJM 373(3), 2015 (PMID 25981554); data on GEO GSE66499 (submitted by Veracyte, public 2015-05-17). As published: "680 CEL files from 639 BEC specimens, 152 benign and 487 malignant samples" on the Affymetrix Human Gene 1.0 ST array (GPL6244, 33,297 probe sets per sample), processed by "RMA normalization"; sample characteristics only tissue, gender and cancer_yes_no; sample titles such as A1_0001_1 carry the cohort, the patient and the replicate. The diagnosis comes from bronchoscopy or 12 months of follow-up.
- Use case: the pulmonologist, after a non-diagnostic bronchoscopy, decides between further invasive testing and a more conservative approach ("a gene-expression classification of 'low-risk' warrants consideration of a more conservative diagnostic approach", the paper's abstract on GEO); fit direct; regime IID over patients with the replicate arrays of one specimen kept together; AEGIS-1 against AEGIS-2 (two cohorts, 28 centres) is the alternative the curator may prefer.
- Siblings and duplicates: `lung_cancer_epithelial_genexp` (GSE4115, Spira 2007; Yes, BeyondArena) is the earlier cohort of the same research line: other patients and another array, so its own record (PROV-4), with the same task; the curator decides whether both enter. No other record of GSE66499 (grep: GSE66499, AEGIS, bronchial). External collections: none found.
- Better data: found as better data for `lung_cancer_epithelial_genexp`; no further search this round.
- Papers and pages: the NEJM paper (abstract on Europe PMC: AUC 0.78 in AEGIS-1 and 0.74 in AEGIS-2, sensitivity 88-89%, specificity 47%, NPV 91% at intermediate pre-test risk); the classifier's derivation in AEGIS-1 (Whitney et al. 2015, BMC Medical Genomics; not read).
- Metric: the paper reports AUC, sensitivity, specificity and NPV side by side for a classifier at its own cut-off, with no single criterion for our task (MET-5, MET-6), so the fallback `roc_auc`, also the paper's discrimination measure; inputs none.
- Risks for /add-dataset: 41 replicate arrays must be collapsed or grouped by the patient parsed from the titles (LEAK-17); the processed values are RMA over the arrays processed together, a weak transductive leak (LEAK-30), repairable from the CEL files, as noted on the sibling; 76% cancer, selected by referral for bronchoscopy, which is the population of the use case (no `Selection Bias`); 33,297 features for 639 patients; no age, smoking history or lesion size ship, though the clinical decision uses them.
- Priority: gap 0 (medical & healthcare and binary not thin), use case +, source +, shape 0 (639 patients, below about 1,000), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `lung_cancer_epithelial_genexp`.
- as published: 639 current or former smokers undergoing bronchoscopy for suspected lung cancer (AEGIS-1: 298, AEGIS-2: 341; 1,357 enrolled), 487 cancer and 152 benign; 680 CEL files (replicates) on Affymetrix ...; target: lung cancer diagnosis (cancer_yes_no), from bronchoscopy or 12 months of follow-up; access: open.
- Why: the same task as SMK_CAN_187 (Spira et al. 2007: bronchial airway epithelium expression of smokers with suspect lung cancer, cancer or not), by the same research line, prospective and multicentre
- Adds: 639 against 187 patients, prospective trials, 2015 against 2007, newer array. Caveats: 41 replicate arrays need grouping by specimen; ComBat batch adjustment over all arrays (like the RMA note on the record); a different cohort, so its own record, not a version

**Assessment (AI, 2026-11-08):** size check for the large-datasets review: 639 patients x 33,297 probe sets (RMA) plus sex, cancer 487 against benign 152; the call stands at priority 3. The classifier's AEGIS-1 training set (299 patients) is not in this deposit.
- As published: GEO GSE66499 (public 2015-05-17; https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE66499). The series matrix (115 MB, downloaded) has 680 arrays x 33,297 probe sets (GPL6244, HuGene 1.0 ST transcript clusters), with no missing cell and the processing "RMA normalization". The characteristics are `tissue`, `gender` and `cancer_yes_no`; the titles (A1_ or A2_, patient, replicate) carry the cohort and the patient. The CEL files are in `GSE66499_RAW.tar` (2.8 GB). GEO's GPL6244 annotation (2016) gives a gene symbol for 22,195 of the 33,297 probe sets; the others are control or unannotated clusters. The source names no QC subset.
- The task's table: 639 patients (computed from the titles): AEGIS-1 298 (220 cancer, 78 benign) and AEGIS-2 341 (267, 74), 487 against 152 in total, matching the summary ("298 patients from AEGIS 1 and 341 from AEGIS 2"). 23 patients have 2 to 4 arrays (41 extra arrays), and the label agrees within each patient: collapse to one row per patient or group by patient (LEAK-17). Inputs: 33,297 probe sets + `gender` (22,195 probe sets if only the annotated ones are kept).
- Access: open on GEO, no login, no licence stated; 115 MB processed, 2.8 GB of CEL files.
- Changes the call: (1) The classifier's training set is not in this deposit. Whitney et al. 2015 (BMC Medical Genomics 8:18, PMC4434538) derived it on "A set of 299 patients from AEGIS 1 consisting of 223 patients diagnosed with lung cancer and 76 patients diagnosed with benign disease" (Results). GSE66499's AEGIS-1 part is 298 patients with 220/78, so other patients, and the paper's text names no deposit for the 299, so the task's table stays at 639. (2) The earlier note of a "ComBat batch adjustment over all arrays" has no support on GEO, whose processing field says only "RMA normalization". RMA over the deposited arrays together is the weak LEAK-30, repairable from the CEL files per sample. (3) As the screening said, no age, smoking or lesion fields ship. The priority stays 3.
- Not checked: whether RMA ran over all 680 arrays at once or per batch; the NEJM supplement; better data (the AEGIS nasal series and others were not looked up in this pass).
