---
unique_name: raman_bioprocess_analytes_anton_532
name: Bioprocess Analytes (Anton 532)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
- Tiny Data
- Many features
- Multi-target
- Spectral Data
collections:
- RamanBench
original_source: Other
problem_type: Regression
source_links:
- https://doi.org/10.1016/j.saa.2025.125861
- https://huggingface.co/datasets/chlange/RamanSpectraBioprocessAnalystesAnton532
- https://arxiv.org/abs/2605.02003
- https://huggingface.co/datasets/chlange/RamanSpectraBioprocessAnalystesAnton785
- https://huggingface.co/datasets/chlange/RamanSpectraBioprocessAnalystesKaiser
- https://huggingface.co/datasets/chlange/RamanSpectraBioprocessAnalystesMetrohm
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages, the release file listings and a two-column preview of the data, NOT from a build. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: real Raman spectra of glucose, acetate and magnesium sulfate mixtures with assay reference values, but about 54 samples (5 scans each) per instrument, and the eight instrument datasets measure nearly the same samples.
- Source: Lange et al. (TU Berlin bioprocess group), "Comparing machine learning methods on Raman spectra from eight different spectrometers", Spectrochimica Acta A 334:125861, online 2025-02-11; data on Hugging Face, one dataset per instrument (chlange/RamanSpectraBioprocessAnalystesAnton532 and seven more, CC BY 4.0, this one uploaded 2026-02-09, with the authors' train/val/test files; whether the paper released the data earlier was not checked, so the year is left empty). As published: "we created samples with known concentrations of glucose, sodium acetate and magnesium sulfate and measured more than 2200 spectra of these samples with eight different spectrometers" (Abstract); the Anton Paar Cora 5001 at 532 nm: 270 spectra (165/55/50) x 1,601 bins (300-3500 cm-1), "Number of Samples: 54", "Scans per Sample: 5", reference values from a Cedex Bio HT analyzer (card). Read on the target columns: 53 distinct target triples (two samples share one), and the authors' split keeps a sample's scans together.
- Use case: process analytical technology for E. coli fermentations ("concentration ranges typically found in E. coli fermentation processes", card): a bioprocess lab reads substrate concentrations from a spectrum instead of an offline assay; the paper's point is one model for "laboratories with data from more than one spectrometer". Fit approximate (aqueous mixtures stand in for broth). Regime grouped by sample (5 scans each, SPLIT-29); the same samples recur across instruments.
- Siblings and duplicates: the seven other instruments are aliases of this record (Anton 785, Kaiser, Metrohm, Mettler Toledo, Tec5, Timegate, Tornado; 133-399 spectra each): versions of one sample set (PROV-6), so one dataset at most, the largest cut or all eight with the instrument as a column (the paper's own joint task; the wavenumber axes differ). Same group, other tasks: `raman_bioprocess_substrates`, `raman_ecoli_fermentation`, `raman_kaiser_ecoli_fermentation`, `raman_streptococcus_thermophilus_fermentation_kaiser`, `raman_ecoli_metabolites`. External collections: RamanBench ("Bioprocess Analytes", 8 datasets, 2,261 spectra).
- Better data: a candidate of the benchmark RamanBench (arXiv 2605.02003); no further search in this run.
- Papers and pages: the paper (abstract through Europe PMC; full text paywalled, not read), the Hugging Face cards.
- Metric: none found (the abstract compares a CNN with PLS without naming the metric; the card names none; full text not read), so the fallback rmse per target. Inputs none.
- Risks for /add-dataset: about 54 samples per instrument (TP-5 on a regression's units); three targets: pick one or declare multi-target (CLEAN-18); PROV-6 across the eight cuts; raw spectral bins (SEL-15).
- Priority: gap - (regression, not thin), use case - (fit approximate: mixtures for broth), source + (paper, authors' release), shape - (54 samples), risk - (eight cuts of one sample set, tiny).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 270 spectra x 1,601 wavenumber features; 3 target(s) (raman-data id: bioprocess_analytes_anton_532); target: glucose, sodium acetate, magnesium sulfate concentrations (3 targets).
- Why: Quantify bioprocess analytes in aqueous solutions from Raman spectra; the same solutions measured on eight spectrometers
- Notes: Raw Raman spectral bins (1,601 wavenumber points, 300-3500 cm-1) as features; SEL-15 judges such signals case by case. One of 8 instrument variants of the same solutions (Lange et al. 2025). Multi-target. HF mirror: https://huggingface.co/datasets/HTW-KI-Werkstatt/RamanBench/tree/main/bioprocess_analytes_anton_532 | ...
