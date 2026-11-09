---
unique_name: raman_acetic_acid_species
name: Acetic Concentration
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
- Multi-target
- Spectral Data
collections:
- RamanBench
domain: chemistry & material science
problem_type: Regression
source_links:
- https://doi.org/10.1177/0003702820973275
- https://publications.rwth-aachen.de/record/978266
- https://arxiv.org/abs/2605.02003
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages, the release file listings and a two-column preview of the data, NOT from a build. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: real inline Raman spectra of one acetic acid titration, but 42 spectra (about 14 titration points) with species concentrations calculated from ideal dissociation equilibria: a calibration study, not a sample of units.
- Source: Echtermeyer, Marks, Mitsos, Viell (RWTH Aachen), "Inline Raman Spectroscopy and Indirect Hard Modeling for Concentration Monitoring of Dissociated Acid Species", Applied Spectroscopy 75(5):506-519, online 2020-12-04; data in the RWTH record 978266 (file Data_RWTH-2024-01177.zip, CC0 per the raman-data loader; the record page sits behind a browser check and was not read, so the year of the data release is left empty). As published: per acid a folder of .spc spectra and a "Data Table <acid> Acid Titration.xlsx"; acetic: 42 spectra x 11,084 bins (100-3425 cm-1), targets acetic acid and acetate (RamanBench); the raman-data loader finds 14 groups of up to 3 spectra with the same target values.
- Use case: process analytical technology "for quantitative monitoring of processes containing carboxylic acids" (Abstract): an engineer reads the dissociated species in-line instead of sampling. Fit approximate: one titration of a pure acid in water stands for a process stream, and the reference values are "calibrated with calculated ideal dissociation equilibria" (method A, Abstract), computed rather than assayed. Regime grouped by titration point (replicate spectra); the rows are consecutive points of one run.
- Siblings and duplicates: the same study's other acids: `raman_formic_acid_species` and `raman_levulinic_acid_species` (with succinic, whose targets are pH and the mass of NaOH) are their own records; citric (45 spectra) and itaconic (21 spectra) are aliases of this record. Each acid is one titration; different acids are different chemical systems, but none is large enough to be a task alone (PROV-6, PROV-7). External collections: RamanBench ("Acetic Concentration", "Citric Concentration", "Itaconic Concentration").
- Better data: a candidate of the benchmark RamanBench (arXiv 2605.02003); no further search in this run.
- Papers and pages: the paper (abstract read through Europe PMC; full text paywalled, not read).
- Metric: the abstract reports hard-model errors "< 2.87 × 10-4 mol mol-1" and that IHM "yields more accurate results than partial least squares regression"; the error's definition is in the full text, not read (PROV-17), so the fallback rmse per target. Inputs none.
- Risks for /add-dataset: too small to score (about 14 distinct titration states, about 3 per grouped test fold; TP-5); the two targets carry one degree of freedom (acid and acetate add up to the diluted total), so one target (CLEAN-18); computed reference values (USE-5); 11,084 raw spectral bins for 42 rows (SEL-15).
- Priority: gap - (regression, chemistry not thin), use case - (a hard-model calibration, no decision named), source + (paper, institutional data record), shape - (42 spectra), risk - (tiny, computed targets).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 42 spectra x 11,084 wavenumber features; 2 target(s) (raman-data id: acetic_acid_species); target: acetic acid, acetate concentrations (2 targets).
- Why: Quantify dissociated acetic acid species during titration from in-line Raman spectra (process monitoring) | Quantify dissociated citric acid species during titration from in-line Raman spectra (process monitoring) | Quantify dissociated itaconic acid species during titration from in-line Raman spectra (process ...
- Notes: Raw Raman spectral bins (11,084 wavenumber points, 100-3425 cm-1) as features; SEL-15 judges such signals case by case. One of 6 acids from the same titration study (RWTH, CC0). Tiny (N < 50). HF mirror: https://huggingface.co/datasets/HTW-KI-Werkstatt/RamanBench/tree/main/acetic_acid_species | Raw Raman spectral ...
