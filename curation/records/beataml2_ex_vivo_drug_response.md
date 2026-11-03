---
unique_name: beataml2_ex_vivo_drug_response
name: 'Beat AML 2.0: ex vivo drug sensitivity of AML patient specimens with RNA-seq, mutations and clinical data'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- Non-IID (Grouped)
- Many features
- AI-Filled (Verify)
year: '2018'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://github.com/biodev/beataml2.0_data
- https://doi.org/10.1016/j.ccell.2022.07.002
- https://github.com/BoevaLab/GeneICL
- http://arxiv.org/abs/2610.08694
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: the ex vivo drug sensitivity (area under the dose-response curve) of AML patient specimens predicted from RNA-seq, mutations and clinical data, the task of the CTD-squared BeatAML DREAM Challenge (2020), on the open Beat AML 2.0 release; a few hundred specimens per drug, so one drug per dataset.
- Source: the Beat AML programme (OHSU Knight Cancer Institute, Leukemia & Lymphoma Society): first publication Tyner et al. 2018, Nature, "Functional genomic landscape of acute myeloid leukaemia" (waves 1-2; the DREAM page cites it as the data source); harmonised release Bottomly et al. 2022, Cancer Cell 40(8):850-864 (doi 10.1016/j.ccell.2022.07.002): "a cumulative cohort of 805 patients (942 specimens)" (abstract). As published: github.com/biodev/beataml2.0_data (CC BY 4.0; the files sit in Git LFS and download openly): clinical data (xlsx), normalised expression and counts, WES mutations, a sample mapping, drug families, the raw inhibitor readings (49 MB) and the probit curve fits per specimen and inhibitor (`beataml_probit_curve_fits_v4_dbgap.txt`, header previewed 2026-10-31: dbgap_subject_id, the DNA and RNA sample ids, inhibitor, type, status (`train/test` in the preview), paper_inclusion, ic10 to ic90, `auc`, curve_type). Per drug a few hundred specimens (GeneICL uses 277-492 per drug for 10 drugs, per the run's note, not verified).
- Use case: at diagnosis a haematologist or a trial team predicts from the leukaemia's sequencing which targeted drug its cells respond to, where the ex vivo screen needs fresh cells and days (the challenge's goal: "define patient subpopulations tailored to individual treatments", DREAM Overview); fit approximate (the ex vivo AUC stands in for the clinical response); regime grouped by patient (942 specimens of 805 patients; a new patient's specimen). The challenge validated on the then unpublished later waves, a temporal reading to weigh against the patient grouping at /add-dataset (SPLIT-19, SPLIT-23).
- Siblings and duplicates: none (grep beataml, biodev, drug response, drug sensitivity, gdsc, ccle, depmap, leukemia); `lung_cancer_epithelial_genexp` (`Yes`) is the precedent for a wide expression table. External collections: GeneICL's 80 tasks (arXiv 2610.08694); the DREAM challenge (Synapse syn20940518).
- Better data: from the curator's Zotero collection (item 300); no further search this round.
- Papers and pages: Tyner et al. 2018; Bottomly et al. 2022 (abstract via Europe PMC; the full text did not load); the DREAM pages (syn20940518: Overview, Questions, Data, read through the Synapse API); Bohl et al. 2026, GeneICL (abstract).
- Metric: the challenge's SC1 metric: "Each drug will be evaluated using a Spearman correlation ([-1, 1]), and the Spearman correlations will be averaged to produce a final metric" (Questions page, Subchallenge 1; Pearson secondary), a leaderboard metric (MET-4); for a one-drug dataset the Spearman correlation on the test fold; inputs none (the average over drugs needs the inhibitor as a scoring column if several drugs ship in one dataset).
- Risks for /add-dataset: pick the drugs: one task per inhibitor, and several drugs from one cohort are cuts (PROV-6) unless each is shipped as its own task (PROV-7); the release is several tables joined on dbGaP subject and sample ids; about 20k genes on a few hundred rows (width is no reason to drop features, CLEAN-22); the clinical file may hold post-diagnosis fields (response, survival, later treatment) to drop (LEAK-10); several specimens per patient need the patient as the group (SPLIT-24); check what `status` and `paper_inclusion` mean before shipping.
- Priority: gap 0 (medical, regression, grouped not thin), use case 0 (approximate: an ex vivo surrogate), source +, shape 0 (a few hundred specimens per drug), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 300: "GeneICL: A Tabular Foundation Model for Bulk Transcriptomics".
- as published: patient specimens (waves 1-4): GeneICL uses 277-492 specimens per drug for 10 drugs. The repo holds normalised expression and counts, probit curve fits, raw inhibitor data (49 MB), WES mutations and ...; target: ex vivo drug sensitivity of the patient's leukaemia cells (area under the dose-response curve) for one inhibitor, regression; one task per drug; access: open.
- Why: Real measured responses from a large clinical cohort, open under CC BY 4.0 with a Cancer Cell data paper, and a standard drug-response benchmark (used in GeneICL).
- Adds: A first drug-response (precision oncology) task. Wide data (about 20k genes, a few hundred rows) like lung_cancer_epithelial_genexp; mutations and clinical variables allow a narrower feature set. Choose one or a few drugs.
