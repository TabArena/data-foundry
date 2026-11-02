---
unique_name: raman_serum_prostate_cancer
name: Prostate Cancer SERS Serum
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
decision_markers:
- Selection Bias
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
- Tiny Data
- Many features
collections:
- RamanBench
original_source: Other
year: '2024'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Multiclass Classification
source_links:
- https://doi.org/10.1016/j.xcrm.2024.101579
- https://figshare.com/articles/dataset/ComFilE_for_PCa/28107395
- https://arxiv.org/abs/2605.02003
- https://doi.org/10.6084/m9.figshare.28107395.v1
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: a clinical liquid-biopsy task (prostate cancer against benign hyperplasia and controls from serum SERS spectra) from a Cell Reports Medicine study, but the public release holds 62 of the 424 participants, about 200 spectra each, the controls came from a check-up centre while the patients came from urology, and the groups may have been measured in different batches.
- Source: Bi, Wang, Xue, He, Liu, Chen et al., "SERSomes for metabolic phenotyping and prostate cancer diagnosis", Cell Reports Medicine 5(6), 2024 (https://doi.org/10.1016/j.xcrm.2024.101579; full text PMC11228451). The spectra are on figshare as "ComFilE for PCa" by Bingsen Xue (https://doi.org/10.6084/m9.figshare.28107395.v1, 2024-12-30, CC BY 4.0; description only "The SERS serum spectra of Prostate Cancer, Benign Prostatic Hyperplasia and Control"), released with the ComFilE paper (Xue et al., Nature Machine Intelligence 2025, https://doi.org/10.1038/s42256-025-01027-5). As published on figshare (file list read): 63 PyTorch tensor files of about 581 kB, one per serum sample, prefixed [1] (24 files), [2] (23) and [3] (16); raman-data reads 62 distinct samples ("1Ag125 ships both baseline-corrected and not"), about 200 spectra x 724 points (600-1800 cm-1) each, 12,601 spectra in RamanBench (whose axis is an index 0-724). The paper's cohort is larger: "A total of 424 clinical samples were collected for this study"; data statement: "All data is available from the lead contact upon request" and "the model weight and partial test dataset have been deposited". The file counts (24/23/16) are close to the internal test cohort (24/23/21 PCa/BPH/control), so the release is probably part of it (inference).
- Use case: a urologist decides on biopsy for a man with suspected prostate disease, with a serum test the paper says "dramatically improves the diagnosis of PCa ... compared to conventional biomarkers, like prostate-specific antigen (PSA)"; "Each BPH and PCa patient has been confirmed by transrectal prostate biopsy". Fit direct for PCa against BPH, approximate for the controls. Regime grouped by participant (200 spectra per serum sample; "All the samples were from distinct participants").
- Siblings and duplicates: `raman_comfile_stroke` (the same lab's ComFilE releases for Alzheimer's disease and stroke, same SERSome protocol, other participants); `prostate_cancer_detection` (NCI-FDA serum proteomics, retired) is another assay and source. No duplicate (grep over the records for SERSome, ComFilE, the DOIs). External collections: RamanBench (raman-data groups by participant; its macro-F1 near 1.0 on its own splits is no evidence for our task, EV-4).
- Better data: a candidate of the benchmark RamanBench; no new search (run brief).
- Papers and pages: Bi et al. 2024 (full text read: cohorts, methods, data availability); Xue et al. 2025 (title only); RamanBench Tables 3, 11; raman-data `FigshareLoader`.
- Metric: the paper reports accuracy as its headline ("a diagnosis accuracy of 80.8% on the internal test set and 73% on the external validation set") and "A ROC analysis and AUC were used to evaluate model performance for diagnosis", several side by side with no threshold fixed, so the fallback `log_loss` (MET-5, MET-6); RamanBench scores macro-F1. Inputs: the participant id as the group (in the file names).
- Risks for /add-dataset: `Selection Bias`: "104 samples (training: 73 controls, validation: 10 controls, test: 21 controls) were collected from the Physical Examination Center", the patients "from the urology department", cases and controls collected apart; class-dependent recording to check (LEAK-13 to LEAK-15): controls drawn at another site, and file-name patterns that differ across the groups (names of letters only occur under [3]), so a measurement batch may follow the class; the paper reaches 80.8% per participant, a reference for a probe that scores far higher; 62 participants and 16 in the smallest group, so 3-5 per class per grouped test fold (TP-5, TP-8); which prefix is which class is unverified; a binary PCa-against-BPH task would match the clinical decision better (USE-5); the full 424-participant cohort is "available ... upon request" (`Data Requested` if the curator asks); raw spectral bins weigh against (SEL-15).
- Priority: gap + (multiclass thin), use case + (diagnosis and the PSA comparison named by the source), source + (paper with full methods, figshare), shape 0 (62 participants), risk - (controls from another centre, a possible batch by class, a public subset).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 12,601 spectra x 725 wavenumber features; 3 classes (raman-data id: serum_prostate_cancer); target: diagnosis (PCa / BPH / control).
- Why: Classify prostate cancer, benign prostatic hyperplasia or healthy control from serum SERS spectra
- Notes: Raw Raman spectral bins (725 wavenumber points, 0-724 cm-1) as features; SEL-15 judges such signals case by case. 424 serum samples, ~200 spectra per sample (SERSome): grouped by patient. HF mirror: https://huggingface.co/datasets/HTW-KI-Werkstatt/RamanBench/tree/main/serum_prostate_cancer
