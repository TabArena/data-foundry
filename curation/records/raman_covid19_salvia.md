---
unique_name: raman_covid19_salvia
name: Saliva COVID-19
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- TBD
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
problem_type: Multiclass Classification
source_links:
- https://doi.org/10.1016/j.compbiomed.2024.108028
- '# 404 on 2026-10-31 (as is github.com/MIND-Lab/Raman-Spectra-Data); RamanBench''s copies are the last two links'
- https://github.com/piazzam/Robust-SVM-Raman
- https://arxiv.org/abs/2605.02003
- https://github.com/ml-lab-htw/rb_data_fallback/releases/tag/v1.0
- https://huggingface.co/datasets/HTW-KI-Werkstatt/RamanBench/tree/main/covid19_salvia
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages, the release file listings and a two-column preview of the data, NOT from a build. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: dried-saliva Raman spectra of 101 subjects (current infection, recovered, healthy) with a subject id, from a documented study, but tiny in subjects and a case-control pilot; the first-party repository is gone and only RamanBench's copy remains.
- Source: the cohort of Carlomagno et al., "COVID-19 salivary Raman fingerprint: innovative approach for the detection of current and past SARS-CoV-2 infections", Scientific Reports 11:4943, 2021-03-02 (PMC7925543; NCT04583306; data "available from the corresponding authors on reasonable request"): 30 COVID-19 patients (COV+), 38 who tested negative after a documented past infection (COV-) and 33 age- and sex-matched healthy controls (Methods, "Patients and clinical data"); released with Bertazioli et al. 2024 (Computers in Biology and Medicine 171:108028; full text not read) in MIND Lab repositories that return 404 today (github.com/piazzam/Robust-SVM-Raman, github.com/MIND-Lab/Raman-Spectra-Data); copy in ml-lab-htw/rb_data_fallback v1.0 (2026-05-15) and the RamanBench Hugging Face mirror, so the release year is left empty. As published (mirror, the group and target columns read): 2,501 spectra x 885 bins (401-1598 cm-1) from 101 subjects, 30 COV+, 37 COV-, 34 CTRL (the paper: 30/38/33); one folder per subject with spectra.csv, raman_shift.csv, user_information.csv.
- Use case: "Early and fast identification of subjects with a current or past infection must be achieved to slow down the epidemiological widening" (Abstract): a point-of-care saliva test that tells a current infection from a past one or none; a testing site decides whether to isolate and confirm by RT-PCR. Fit approximate: a single-centre case-control pilot; COV- means recovered after a documented infection, not "negative symptomatic" as the run's Assessment below says. Regime grouped by subject: "at least 20 spectra" per sample, and the patient-level model uses leave-one-patient-out (SPLIT-23).
- Siblings and duplicates: `raman_alzheimer` (same lab, protocol and release; another cohort and task, PROV-7); no other record of these data. External collections: RamanBench ("Saliva COVID-19").
- Better data: a candidate of the benchmark RamanBench (arXiv 2605.02003); no further search in this run.
- Papers and pages: Sci Rep 2021 (read through a page summary), the 2024 paper (abstract only).
- Metric: the paper reports accuracy, precision, sensitivity, specificity, MCC and error rate per spectrum (ROC AUC 0.9), and accuracy, sensitivity and specificity per patient (Tables 3 and 4), side by side: the fallback log_loss per subject (MET-5, MET-8). Inputs: the subject id (the folder) for the grouping and the per-subject score.
- Risks for /add-dataset: 101 subjects, 6-7 per class in a grouped test fold (tiny; TP-5 borderline); check where and when each group was recruited (a class collected apart is `Selection Bias` and a recording risk, LEAK-13); check what user_information.csv holds; the first-party repository is gone and the licence reads "Authors contacted" (noted only, EV-4); raw spectral bins (SEL-15).
- Priority: gap + (multiclass thin), use case - (a pilot, fit approximate), source + (peer-reviewed cohort paper, trial registration), shape - (101 subjects), risk - (repository gone, case-control pilot).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 2,501 spectra x 885 wavenumber features; 3 classes (raman-data id: covid19_salvia); target: COVID-19 positive / negative symptomatic / healthy.
- Why: Screen for SARS-CoV-2 infection from Raman spectra of dried saliva drops
- Notes: Raw Raman spectral bins (885 wavenumber points, 401-1598 cm-1) as features; SEL-15 judges such signals case by case. 101 subjects, ~25 replicate spectra each (grouped). Licence unclear ('authors contacted'). HF mirror: https://huggingface.co/datasets/HTW-KI-Werkstatt/RamanBench/tree/main/covid19_salvia
