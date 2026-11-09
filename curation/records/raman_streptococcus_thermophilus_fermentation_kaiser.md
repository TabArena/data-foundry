---
unique_name: raman_streptococcus_thermophilus_fermentation_kaiser
name: Streptococcus Thermophilus Fermentation (Kaiser)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Too Small
tags:
- AI-Filled (Verify)
- Spectral Data
collections:
- RamanBench
source_links:
- https://arxiv.org/abs/2605.02003
- https://huggingface.co/datasets/chlange/streptococcus_thermophilus_fermentation_kaiser
- https://huggingface.co/datasets/chlange/streptococcus_thermophilus_fermentation_timegate
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Too Small`, TP-5): 14 offline samples from two shake-flask runs, the same samples measured on two spectrometers (the merged time-gated variant); a monitoring model is scored on new runs, and the release holds two.
- Source: the data owners' release with RamanBench (arXiv 2605.02003, 2026) on Hugging Face: chlange/streptococcus_thermophilus_fermentation_kaiser and chlange/streptococcus_thermophilus_fermentation_timegate (Christoph Lange, created 2026-03-24, CC BY 4.0); the card's "Paper: [Link to paper if available]", no earlier publication. As published: "The dataset includes two distinct fermentation runs conducted in shake flasks over a 24-hour period, paired with reference analytical measurements (HPLC and spectrophotometry)" (card); 14 spectra x 1,501 bins (Kaiser RXN1, 300-1800 cm-1) or 117 bins (time-gated, 487-1423 cm-1); 4 targets: lactose, galactose, lactate (HPLC) and OD600.
- The decisive words: "It is in the tiny-data regime (N = 14) and targets lactose, galactose, lactate, and OD600" and "The dataset covers two independent 24-hour fermentation runs" (RamanBench NEW_DATASETS.md, written with the data owners); the time-gated set holds "the same Streptococcus thermophilus batch cultivations as above".
- Why: TP-5 counts the units a fold is scored on, per test fold and in total. The prediction is for a new fermentation, so the unit is the run: two in total, one per fold of a grouped split; read as 14 samples, a 5-fold test fold holds 2-3 (fewer than the 8 healthy people of `parkinsons_biomedical_voice_measurements`, retired under TP-5). The source has no more data, and the second spectrometer adds no units (PROV-6).
- Use case: the operator of a lactic-acid fermentation reads lactose, lactate and biomass from an offline spectrum instead of HPLC; the card: "intended for researchers developing chemometric models and machine learning pipelines for bioprocess monitoring". Fit direct; regime grouped by run.
- Siblings and duplicates: alias `raman_streptococcus_thermophilus_fermentation_timegate` (the same samples on a time-gated instrument); `raman_kaiser_ecoli_fermentation` (the same lab and instrument pair, 12-14 samples); `raman_yeast_fermentation`, `raman_ralstonia_fermentations`, `raman_ecoli_fermentation` (other processes). External collections: RamanBench.
- Better data: a candidate of the benchmark RamanBench; no new search (run brief).
- Metric: none from the source (no paper); RamanBench's RMSE per target is a benchmark-wide convention.
- Reject check (AI, 2026-10-31): stands. The card: 'two distinct fermentation runs conducted in shake flasks over a 24-hour period' (https://huggingface.co/datasets/chlange/streptococcus_thermophilus_fermentation_kaiser); NEW_DATASETS.md: 'It is in the tiny-data regime (N = 14)'. A monitoring model is scored on new runs, and two runs leave one per grouped test fold: the same call as raman_wheat_lines (batch 02). TP-5 is a part-6 rule outside step 4's parts 1, 2 and 5, but the count is in the owners' own words.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 14 spectra x 1,501 wavenumber features; 4 target(s) (raman-data id: streptococcus_thermophilus_fermentation_kaiser); target: lactose, galactose, lactate, OD600 (4 targets).
- Why: Monitor S. thermophilus shake-flask batch cultivations from offline Raman spectra
- Notes: Raw Raman spectral bins (1,501 wavenumber points, 300-1800 cm-1) as features; SEL-15 judges such signals case by case. New with RamanBench; no prior paper. Tiny (N < 50). HF mirror: https://huggingface.co/datasets/HTW-KI-Werkstatt/RamanBench/tree/main/streptococcus_thermophilus_fermentation_kaiser | Raw Raman ...
