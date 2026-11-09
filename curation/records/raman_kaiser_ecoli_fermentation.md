---
unique_name: raman_kaiser_ecoli_fermentation
name: Kaiser Ecoli Fermentation (broth)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
- Tiny Data
- Multi-target
- Many features
- Spectral Data
collections:
- RamanBench
original_source: Other
year: '2026'
problem_type: Regression
original_data_state: One Table
source_links:
- https://arxiv.org/abs/2605.02003
- https://huggingface.co/datasets/chlange/kaiser_raman_ecoli_fermentation
- https://huggingface.co/datasets/chlange/kaiser_raman_ecoli_fermentation_supernatant
- https://huggingface.co/datasets/chlange/tg_raman_ecoli_fermentation
- https://huggingface.co/datasets/chlange/tg_raman_ecoli_fermentation_supernatant
- https://doi.org/10.1002/btpr.2665
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: 14 offline Raman spectra from one E. coli fed-batch cultivation (broth and supernatant, continuous-wave and time-gated) with OD600, glucose and acetate; a real monitoring question, but one run of 14 samples, and RamanBench finds no signal on two of its targets.
- Source: first released on Hugging Face by the RamanBench authors (chlange/kaiser_raman_ecoli_fermentation, created 2026-03-25, CC BY 4.0, one `data.csv`; three sibling repositories for the supernatant and the time-gated spectra), marked new in RamanBench (Tables 16, 18); the samples come from Kögler, Paul, Anane, Birkholz, Bunker, Viitala, Maiwald, Junne and Neubauer, "Comparison of time-gated surface-enhanced Raman spectroscopy (TG-SERS) and classical SERS based monitoring of Escherichia coli cultivation samples", Biotechnology Progress 34(6):1533-1542, 2018 (https://doi.org/10.1002/btpr.2665); year 2026. As published (parquet schema by range request): 14 rows x 1,699 bins (301-1999 cm-1, Kaiser RXN1, 785 nm) + `time_h` (0-22), `OD600`, `Glucose` (10 of 14), `Acetate` (11 of 14); the time-gated variant 12 rows x 114 bins. One 3.7 L bioreactor run of E. coli W3110, a 10 h batch then pulse-based feeding (card); glucose by a hexokinase kit, metabolites by HPLC; samples frozen at -80 °C and measured offline (A.17.1).
- Use case: a bioprocess operator reads glucose, acetate and biomass from a sample's Raman spectrum instead of waiting for HPLC; fit approximate (offline frozen samples). Regime temporal within one run; with a single run there is no grouped split and no temporal one with 3 windows (SPLIT-14).
- Siblings and duplicates: no duplicate (grep for the DOI and the HF ids). The record merges four variants of the same samples (broth or supernatant x Kaiser or time-gated; PROV-6). The same task on more runs: `raman_ecoli_fermentation` (24 cultivations, 379 spectra); the same design: `raman_streptococcus_thermophilus_fermentation_kaiser` (14 spectra). External collections: RamanBench (Tables 18, 19).
- Better data: a candidate of the benchmark RamanBench; no new search (run brief).
- Papers and pages: Kögler et al. 2018 (abstract: "NIR-Raman provided a superior performance for the quantitative evaluation of analytes, both with and without SERS nanoparticles when using multivariate data analysis"; full text not read); the HF card; RamanBench A.17.1 and its learnability check, where the best R2 for OD600 and acetate is below zero ("biomass and metabolite concentrations appear largely decorrelated from single-snapshot Raman spectra in these datasets"; a third party's probe, PROV-15).
- Metric: none found (the 2018 abstract names none; full text not read), so the fallback `rmse` on one analyte (MET-1); inputs none.
- Risks for /add-dataset: 14 samples of one run (`Too Small`, TP-5, TP-9); `time_h` is the process clock, known when the sample is taken: a feature, not a target; glucose and acetate missing in 3-4 rows; four variants of the same samples (PROV-6); raw spectral bins (SEL-15).
- Priority: gap 0, use case 0 (approximate), source + (paper and the owners' release), shape 0 (14 samples), risk - (one run, no signal reported).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 14 spectra x 1,699 wavenumber features; 4 target(s) (raman-data id: kaiser_ecoli_fermentation); target: OD600, glucose, acetate, fermentation time (4 targets).
- Why: Monitor E. coli fed-batch fermentation (offline samples) from continuous-wave Raman spectra (Kaiser RXN1) | Monitor E. coli fed-batch fermentation (offline samples) from time-gated Raman spectra
- Notes: Raw Raman spectral bins (1,699 wavenumber points, 301-1999 cm-1) as features; SEL-15 judges such signals case by case. New with RamanBench; samples from Koegler et al. 2018 (https://doi.org/10.1002/btpr.2665). Tiny (N < 50). Fermentation time is not a measured quantity. HF mirror: ...
