---
unique_name: raman_head_neck_cancer
name: Head & Neck Cancer
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- TBD
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Tiny Data
- Many features
- Spectral Data
collections:
- RamanBench
original_source: Other
year: '2022'
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: Other
source_links:
- https://doi.org/10.1038/s41598-022-22197-x
- https://doi.org/10.5281/zenodo.7044324
- https://arxiv.org/abs/2605.02003
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: Raman spectra of plasma and saliva from about 53 patients with head and neck squamous cell carcinoma or a benign condition, a real liquid-biopsy question with histopathology labels and patient ids in the raw files, but only 19 benign patients, and the RamanBench copy puts the biofluid into the label.
- Source: Koster, Guillen-Perez, Gomez-Diaz, Navas-Moreno, Birkeland and Carney, "Fused Raman spectroscopic analysis of blood and saliva delivers high accuracy for head and neck cancer diagnostics", Scientific Reports 12:18464, 2022-11-02 (https://doi.org/10.1038/s41598-022-22197-x, PMC9630497); data "Raw datasets and media accompanying the manuscript" on Zenodo, 2022-09-02, CC BY 4.0 (https://doi.org/10.5281/zenodo.7044324), so 2022. As published: `Raw data.zip` (13 MB) of text spectra in figure folders (zip directory read by a range request): native and dry plasma and saliva, 53 files each (`Data/Fig 2/...`; file names start with a three-digit patient id, e.g. `305_plasma_dry_..._spotcombined.txt`); the same by diagnosis under `Fig 4` (plasma 39 cancer and 20 non-cancer, saliva 34 and 19); fused per patient under `Fig 5` (32 and 19); `Staging and demographics for clinical samples.xlsx`. Paper: 34 SCC patients and 19 benign controls (surgery for benign conditions such as tonsillectomy or a benign mass), diagnosis by histopathology, 785 nm confocal Raman. RamanBench copy: 111 rows x 1,004 points labelled 789-910 (a wavelength in nm at 785 nm excitation, not cm-1), 4 classes (plasma or saliva x cancer or not).
- Use case: a clinician with a patient's head or neck mass uses a blood and saliva test to tell cancer from a benign lesion before or beside a biopsy; fit direct for the patient-level task (the controls are the differential-diagnosis population). Regime: one row per patient (plasma and saliva fused, the paper's best model) is IID; one row per spectrum is grouped by patient id.
- Siblings and duplicates: no duplicate (grep for the DOI, the Zenodo id, "head and neck"; `radcure_head_neck_survival` and `tcga_hnsc_tumor_vs_normal_rnaseq` are other data). External collections: RamanBench (A.18.3, Table 40).
- Better data: a candidate of the benchmark RamanBench; no new search (run brief).
- Papers and pages: the paper (PCA, then LDA or QDA on PC1-PC5, individuals held out in turn; Results, "Diagnostic model performance": fused sensitivity 96.3%, specificity 85.7%, accuracy 91.7%; GC-TOF-MS on 28 patients); RamanBench A.18.3.
- Metric: the paper reports sensitivity, specificity and accuracy side by side (Results; no Raman AUC), with no threshold fixed: several, so the fallback `roc_auc` on the binary patient-level task (MET-5, MET-8); inputs none at patient level, the patient id as the group otherwise.
- Risks for /add-dataset: rebuild from the Zenodo files, not from RamanBench, whose 4-class label puts the biofluid into the target and the same patient into two rows (USE-5, SPLIT-24); 19 benign patients, about 4 per test fold (a `Too Small` question, TP-5); 59 distinct ids across the folders against 53 in the paper (plasma 59, saliva 53): settle which patients have both fluids (PROV-2); the spectra are spot-averaged and preprocessed (baseline, smoothing, normalisation; LEAK-30 if done over all rows); raw spectral bins (SEL-15).
- Priority: gap 0 (medical, binary), use case + (the source names the diagnostic decision; clinic controls), source + (paper and raw files with patient ids and demographics), shape 0 (about 53 patients), risk - (19 benign patients, a label to rebuild).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 111 spectra x 1,004 wavenumber features; 4 classes (raman-data id: head_neck_cancer); target: cancer vs control (table lists 4 classes, likely biofluid x diagnosis).
- Why: Diagnose head and neck squamous cell carcinoma from Raman spectra of blood plasma and saliva (liquid biopsy)
- Notes: Raw Raman spectral bins (1,004 wavenumber points, 789-910 cm-1) as features; SEL-15 judges such signals case by case. 53-person cohort; several spectra per patient (grouped). Class count unclear: paper text says binary, table says 4. HF mirror: ...
