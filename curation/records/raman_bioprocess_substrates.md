---
unique_name: raman_bioprocess_substrates
name: Bioprocess Monitoring
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
- Many features
- Multi-target
collections:
- RamanBench
original_source: Other
year: '2025'
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.1016/j.measurement.2025.118884
- https://huggingface.co/datasets/chlange/SubstrateMixRaman
- https://arxiv.org/abs/2605.02003
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages, the release file listings and a two-column preview of the data, NOT from a build. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: the largest regression set of the batch (6,960 spectra of about 3,430 robot-prepared mixtures, 8 substrate targets, the authors' grouped split), but designed calibration mixtures rather than process samples, and eight targets to choose from.
- Source: Lange et al., "Deep learning for Raman spectroscopy: Benchmarking models for upstream bioprocess monitoring", Measurement (doi 10.1016/j.measurement.2025.118884, Crossref issue 2026-01); data chlange/SubstrateMixRaman on Hugging Face, created 2025-07-14, CC BY 4.0, train/val/test CSVs (4,849/1,409/702 rows). As published: 1,870 bins (391-3385 cm-1) and eight targets (Glucose, Glycerol, Acetate, EnPump, Nitrate, Yeast_Extract, total_phosphate, total_sulfate); "Concentrations for each substance were randomly sampled from a uniform distribution within ranges relevant for bacterial fermentations", "Lower concentrations were deliberately oversampled", with "varying concentrations of mineral salt medium and antifoam" (card). Read on the target columns: 3,433 distinct target tuples (3,409 with 2 spectra, 23 with 6, 1 with 4), no tuple in two split files, 1,394 rows with a missing target.
- Use case: the card offers "a calibration resource" for "models used in high-throughput bioprocess development, particularly for bacterial fermentations": a bioprocess lab predicts substrate concentrations from in-line spectra. Fit approximate: independent, uniformly drawn concentrations in prepared mixtures stand for broth whose components co-vary. Regime grouped by sample (two spectra per mixture; the authors' split already groups them; the group id is built from identical target tuples, SPLIT-24).
- Siblings and duplicates: no other record of these data; same group: `raman_bioprocess_analytes_anton_532` (eight spectrometers, three analytes), `raman_ecoli_fermentation`, `raman_kaiser_ecoli_fermentation`, `raman_ecoli_metabolites` (fermentation data, their own tasks, PROV-7). External collections: RamanBench ("Bioprocess Monitoring").
- Better data: a candidate of the benchmark RamanBench (arXiv 2605.02003); no further search in this run.
- Papers and pages: the Hugging Face card; the paper (no abstract in Crossref or Europe PMC, not read).
- Metric: none found (the card names none; the paper not read), so the fallback rmse on the chosen target. Inputs none.
- Risks for /add-dataset: eight targets: pick one (glucose is the usual process target) or declare multi-target (CLEAN-18), and drop the rows missing it (USE-7); group by the target tuple, as no sample id ships; the deliberate oversampling of low concentrations shapes the target's distribution (note it); raw spectral bins (SEL-15).
- Priority: gap - (regression, not thin), use case - (a calibration set, fit approximate), source + (paper and the authors' card), shape + (about 3,430 samples, grouped), risk - (target choice, no sample id).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 6,960 spectra x 1,870 wavenumber features; 8 target(s) (raman-data id: bioprocess_substrates); target: glucose, glycerol, acetate, nitrate, phosphate, sulfate, yeast extract, antifoam concentrations (8 targets).
- Why: Quantify eight fermentation substrates in robot-prepared aqueous mixtures from Raman spectra
- Notes: Raw Raman spectral bins (1,870 wavenumber points, 391-3385 cm-1) as features; SEL-15 judges such signals case by case. Concentrations sampled independently by design (lab-prepared mixtures, not a process). Multi-target. HF mirror: ...
