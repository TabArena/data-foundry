---
unique_name: raman_alzheimer
name: Saliva Alzheimer
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- TBD
- Too Small
tags:
- AI-Filled (Verify)
- Tiny Data
- Many features
- Non-IID (Grouped)
collections:
- RamanBench
original_source: Github
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
source_links:
- https://doi.org/10.1016/j.compbiomed.2024.108028
- '# 404 on 2026-10-31 (as is github.com/MIND-Lab/Raman-Spectra-Data); RamanBench''s copies are the last two links'
- https://github.com/piazzam/Robust-SVM-Raman
- https://arxiv.org/abs/2605.02003
- https://github.com/ml-lab-htw/rb_data_fallback/releases/tag/v1.0
- https://huggingface.co/datasets/HTW-KI-Werkstatt/RamanBench/tree/main/alzheimer
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages, the release file listings and a two-column preview of the data, NOT from a build. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: dried-saliva Raman spectra with a subject id, but the named Alzheimer cut has 10 AD subjects (2 per grouped test fold, `Too Small`) recruited at another institute than the controls; the Parkinson cut of the same release (24 PD, 36 controls) is the only task it could ship.
- Source: the cohort of Carlomagno et al., "Identification of the Raman Salivary Fingerprint of Parkinson's Disease Through the Spectroscopic-Computational Combinatory Approach", Frontiers in Neuroscience 15:704963, 2021-10-26 (PMC8576466): 23 PD, 10 AD and 33 healthy controls, "at least 20 spectra per subject", raw data "will be made available by the authors"; released with Bertazioli et al., "An integrated computational pipeline for machine learning-driven diagnosis based on Raman spectra of saliva samples", Computers in Biology and Medicine 171:108028, 2024 (epub 2024-02-01; full text paywalled, not read), MIND Lab (Univ. Milano-Bicocca) with Fondazione Don Gnocchi. The repositories named as the source (github.com/piazzam/Robust-SVM-Raman, github.com/MIND-Lab/Raman-Spectra-Data) return 404 today; the data survive in RamanBench's fallback release (ml-lab-htw/rb_data_fallback v1.0, 2026-05-15) and its Hugging Face mirror, so the release year is left empty. As published (mirror, the group and target columns read): one folder per subject with spectra.csv, raman_shift.csv and user_information.csv; 885 bins (401-1598 cm-1); AD cut 1,151 spectra of 46 subjects (10 AD, 36 CTRL); PD cut 1,476 spectra of 60 subjects (24 PD, 36 CTRL, the same controls).
- Use case: the source offers a minimally invasive saliva test to "determine the PD onset, progression and to monitor therapies" for "clinicians and researchers", and calls itself a pilot needing multi-centre validation; a neurologist would screen a patient with motor or cognitive signs. Fit approximate (a case-control pilot; the label is a clinical diagnosis). Regime grouped by subject: the paper's patient-level model uses leave-one-patient-out with a majority vote over a subject's spectra, so one prediction is a subject (SPLIT-23).
- Siblings and duplicates: `raman_covid19_salvia` (same lab, protocol and release; another cohort and task, PROV-7); "Saliva Parkinson" is an alias of this record, not a record of its own; `parkinsons_biomedical_voice_measurements` (`No (Retired)`, `Too Small`: 8 healthy people, 2-3 per test fold) is the precedent for the AD cut. External collections: RamanBench ("Saliva Alzheimer", "Saliva Parkinson").
- Better data: a candidate of the benchmark RamanBench (arXiv 2605.02003); no further search in this run.
- Papers and pages: Frontiers 2021 (read through a page summary), the 2024 paper (abstract only, PubMed 38335817).
- Metric: the 2021 paper reports sensitivity, specificity, accuracy, MCC, error rate and AUC per spectrum, and sensitivity, specificity and accuracy per patient, side by side: no single deliberate metric, so the fallback roc_auc per subject (MET-5, MET-8). Inputs: the subject id (the folder) as group and scoring unit.
- Risks for /add-dataset: the AD cut is `Too Small` (10 AD subjects in total; TP-5, parkinsons precedent), and per the 2021 paper its AD participants came from IRCCS Istituto Auxologico Italiano while PD and controls came from Fondazione Don Gnocchi (site confounded with the label: `Selection Bias`, a LEAK-13 recording risk); ship PD vs controls (24 vs 36 subjects, about 5 PD per test fold, still tiny) and let the record's name follow; the first-party repository is gone and the licence reads "Authors contacted" (noted only, EV-4); check what user_information.csv holds before using any of it as a feature.
- Priority: gap - (binary, medical, grouped not thin), use case - (a pilot, no decision fixed), source + (peer-reviewed cohort papers), shape - (46-70 subjects), risk - (AD cut too small, site confound, repository gone).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 1,151 spectra x 885 wavenumber features; 2 classes (raman-data id: alzheimer); target: Alzheimer's disease vs healthy control.
- Why: Screen for Alzheimer's disease from Raman spectra of dried saliva drops | Screen for Parkinson's disease from Raman spectra of dried saliva drops
- Notes: Raw Raman spectral bins (885 wavenumber points, 401-1598 cm-1) as features; SEL-15 judges such signals case by case. Licence unclear ('authors contacted'). Replicate spectra per subject (grouped). HF mirror: https://huggingface.co/datasets/HTW-KI-Werkstatt/RamanBench/tree/main/alzheimer | Raw Raman spectral bins (885 ...
