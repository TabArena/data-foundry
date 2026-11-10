---
unique_name: raman_sugar_mixtures_high_snr
name: Sugar Mixtures (High SNR)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
- Many features
- Multi-target
- Spectral Data
collections:
- RamanBench
original_source: Other
year: '2024'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
source_links:
- https://doi.org/10.1073/pnas.2407439121
- https://doi.org/10.5281/zenodo.10779223
- https://arxiv.org/abs/2605.02003
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: a designed library of 240 aqueous sugar mixtures from a PNAS unmixing study, real measurements with known concentrations, but a method benchmark of four pure sugars in water rather than an application, likely near-trivial for supervised calibration.
- Source: Georgiev, Fernández-Galiana, Vilms Pedersen, Papadopoulos, Xie, Stevens and Barahona, "Hyperspectral unmixing for Raman spectroscopy via physics-constrained autoencoders", PNAS 121(45), 2024-10-29 (https://doi.org/10.1073/pnas.2407439121; full text PMC11551349); data "Research data supporting ..." on Zenodo (https://doi.org/10.5281/zenodo.10779223, 2024-10-16, CC BY 4.0; one `Raw data.zip` of 5.3 GB, "Experimental and synthetic Raman data"). As published: "a library of 240 sugar mixtures prepared in-house with four types of sugar (glucose, sucrose, fructose, maltose) at different concentrations ... high SNR (1,920 spectra) and low SNR (7,680 spectra) measurements ... at integration times of 5s and 0.5s"; "The ground truth is defined by the experimental concentrations". RamanBench's cuts: high SNR 1,960 and low SNR 7,840 spectra x 2,000 bins (142-3685 cm-1), 4 concentration targets; the extra 40 and 160 rows match the five pure-solution wells (8 and 32 spectra each).
- Original task (SEL-8): unsupervised unmixing, scored against the known fractions; RamanBench recasts it as supervised regression of each concentration, the ordinary chemometric calibration task, a predictive regression in scope. Use case: quantifying solutes in a mixture from its spectrum, here as a method benchmark ("We used these experimental datasets with ground truth to systematically evaluate unmixing algorithms"); no actor or decision named; fit approximate (pure sugars in water, no food or process matrix). Regime grouped by mixture (8 spectra per mixture in the high-SNR set).
- Siblings and duplicates: alias `raman_sugar_mixtures_low_snr` (the same 240 mixtures at 0.5 s, 7,840 spectra): one dataset under PROV-6, ship one SNR. Other lab-mixture calibration records: `raman_bioprocess_substrates`, `raman_ecoli_metabolites` (other sources). External collections: RamanBench (its scores are no evidence for our task, EV-4).
- Better data: a candidate of the benchmark RamanBench; no new search (run brief).
- Papers and pages: Georgiev et al. 2024 (full text read: Results, Methods, data statement); RamanBench Tables 4, 12.
- Metric: the paper scores abundances by "the MSE between ground-truth and predicted fractional abundances" (Methods; SAD for the endmembers), its one measure for the quantity predicted: `rmse` on the fractions is the source metric (it ranks models as MSE does, MET-11), on concentrations a stand-in. Inputs: the mixture id for the grouped split.
- Risks for /add-dataset: near-trivial (TP-4 to probe: a linear mix of four pure spectra, which the paper's NNLS baseline already models); the low-SNR cut is the harder and larger variant of the same task and may be the one to ship (PROV-6, the curator's call); four targets (one, or the fractions as the paper scores them, CLEAN-18); the mixture id must come from the Zenodo files; pure-solution spectra to drop or keep; the concentrations are a calibration design, the spectra measured (not AHDS); raw spectral bins weigh against (SEL-15).
- Priority: gap 0 (regression, chemistry not thin), use case 0 (a method benchmark), source + (PNAS and Zenodo), shape 0 (240 mixtures), risk - (near-trivial, two SNR cuts).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 1,960 spectra x 2,000 wavenumber features; 4 target(s) (raman-data id: sugar_mixtures_high_snr); target: sucrose, fructose, maltose, glucose concentrations (4 targets).
- Why: Quantify sugars in a combinatorial library of aqueous mixtures from Raman spectra (unmixing benchmark)
- Notes: Raw Raman spectral bins (2,000 wavenumber points, 142-3685 cm-1) as features; SEL-15 judges such signals case by case. Designed lab mixtures (240 compositions, many spectra each: grouped by composition). High and low SNR variants of the same library. HF mirror: ...
