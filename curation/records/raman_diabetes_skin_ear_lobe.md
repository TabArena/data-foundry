---
unique_name: raman_diabetes_skin_ear_lobe
name: Diabetes Skin (Ear Lobe)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- TBD
- Selection Bias
tags:
- AI-Filled (Verify)
- Tiny Data
- Many features
- Spectral Data
collections:
- RamanBench
original_source: Kaggle
year: '2018'
domain: medical & healthcare
problem_type: Binary Classification
source_links:
- https://doi.org/10.1364/BOE.9.004998
- https://www.kaggle.com/datasets/codina/raman-spectroscopy-of-diabetes
- https://arxiv.org/abs/2605.02003
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: in vivo skin Raman spectra of 20 people (11 with type 2 diabetes, 9 controls) at four skin sites; a real screening aim, but tiny and confounded by age: in the source's own age-grouped analysis the accuracy fell to about 50%.
- Source: Guevara, Torres-Galván, Ramírez-Elías, Luevano-Contreras and González, "Use of Raman spectroscopy to screen diabetes mellitus with machine learning tools", Biomedical Optics Express 9(10):4998-5010, 2018 (https://doi.org/10.1364/BOE.9.004998, PMC6179393). The data first appeared on Kaggle from the first author (codina/raman-spectroscopy-of-diabetes, dataset id 42075, licence "copyright-authors"; the author's GitHub repository raman-diabetes, created 2018-08-09, points to it), so the source is Kaggle, 2018 (PROV-8, PROV-9; the first version's date is not shown, the files are dated 2019-11-04). As published: `earLobe.csv`, `innerArm.csv`, `thumbNail.csv`, `vein.csv` (per person and site "the average of five Raman spectroscopy scans", Kaggle) and `AGEs.csv` (reference spectra of advanced glycation end products). Sec. 2.1: "DM2, 7 females, Age: 49.5 ± 6.7 years", "Ctrl, 7 females, Age: 33.2 ± 4.9 years"; portable PEK-785 spectrometer, 785 nm. RamanBench copy: 20 rows x 3,160 bins (0-3159 cm-1) per site, target 11/9 (parquet schema read by a range request).
- Use case: a clinic screens for type 2 diabetes with a portable spectrometer instead of a blood test; fit approximate: "all DM2 patients have been previously diagnosed by their physicians" (Sec. 2.1), so the positives are known, mostly treated diabetics (HbA1c 6.9 ± 1.6%) rather than people a screen would find (the boundary of SEL-7), and the controls are 16 years younger. Regime IID with one row per person and site; with the four sites stacked as rows it is grouped by person.
- Siblings and duplicates: no duplicate (grep for the DOI and the Kaggle slug). The record already merges the four site variants of the same 20 people (`diabetes_skin_ear_lobe`, `_inner_arm`, `_thumbnail`, `_vein`): one dataset, with the sites as columns or one site chosen (PROV-6). External collections: RamanBench (arXiv 2605.02003, Table 39, four datasets, one per site); the Kaggle upload.
- Better data: a candidate of the benchmark RamanBench; no new search (run brief).
- Papers and pages: the paper (PCA with an ANN and with an SVM; 10 subject-level partitions of two people, 1000 repetitions, Sec. 2.8; ANN accuracy 88.9-90.9%, linear SVM 76.0-82.5%, AUC 0.82-0.96 in Table 1); a comment by Bratchenko et al. (Biomed. Opt. Express 10:4489, 2019, not read) and the authors' reply (10:4492-4495), which concedes that the ANN-SVM comparison was not fair; the Kaggle page; MATLAB File Exchange 68938.
- Metric: the paper defines sensitivity, specificity, G-mean, PPV, NPV, F-measure, accuracy and ROC AUC (Sec. 2.9) and leads with accuracy, with no threshold fixed: several, so the fallback `roc_auc` (MET-5, MET-6, MET-8); inputs none.
- Risks for /add-dataset: age confounds the label: grouping the subjects by age, "a statistically significant age difference between groups (p<0.001) was found" and "The classification accuracy of all classifiers diminished to ~50%" (Sec. 3), hence `Selection Bias` (cases and controls collected apart), and the spectral signal may be age; 9 controls, about 2 per test fold of a 5-fold split, as in `parkinsons` (8 healthy people, retired), so `Too Small` is likely (TP-5); four sites of the same people make one dataset (PROV-6); raw spectral bins (SEL-15, weighed against). RamanBench's best macro-F1 per site, 0.41-0.69 (Table 3), is a third party's score, no evidence (PROV-15).
- Priority: gap 0 (medical, binary), use case 0 (approximate fit), source + (paper and the author's own upload), shape 0 (20 people), risk - (age confound, likely too small).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 20 spectra x 3,160 wavenumber features; 2 classes (raman-data id: diabetes_skin_ear_lobe); target: type 2 diabetes vs healthy control.
- Why: Screen for type 2 diabetes from in vivo skin Raman spectra at the ear lobe site | Screen for type 2 diabetes from in vivo skin Raman spectra at the inner arm site | Screen for type 2 diabetes from in vivo skin Raman spectra at the thumbnail site | Screen for type 2 diabetes from in vivo skin Raman spectra at the vein ...
- Notes: Raw Raman spectral bins (3,160 wavenumber points, 0-3159 cm-1) as features; SEL-15 judges such signals case by case. One of 4 anatomical-site variants of the same 20 subjects. Licence Optica OAPA. Tiny (N < 50). HF mirror: https://huggingface.co/datasets/HTW-KI-Werkstatt/RamanBench/tree/main/diabetes_skin_ear_lobe | ...
