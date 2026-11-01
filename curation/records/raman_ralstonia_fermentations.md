---
unique_name: raman_ralstonia_fermentations
name: R. eutropha Copolymer Fermentations
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- AI-Filled (Verify)
collections:
- RamanBench
source_links:
- https://arxiv.org/abs/2605.02003
- https://huggingface.co/datasets/HTW-KI-Werkstatt/RamanSpectraRalstoniaFermentations
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`AHDS (Artifical/Handmade/Deterministic/Simulated)`, SEL-16; PROV-3): the data owners state that the 82 spectra mix real and synthetic ones, and nothing in the release says which rows are which.
- Source: released with RamanBench (arXiv 2605.02003, 2026) by its authors on Hugging Face (HTW-KI-Werkstatt/RamanSpectraRalstoniaFermentations, created 2026-01-14, CC BY 4.0), citing Lange, Thiele, Santolin, Riedel, Borisyak, Neubauer and Cruz-Bournazou, "Data Augmentation Scheme for Raman Spectra with Highly Correlated Annotations", ESCAPE 34, Computer Aided Chemical Engineering 53:3055-3060, 2024 (https://doi.org/10.1016/B978-0-443-28824-1.50510-X; arXiv 2402.00851). As published: 82 rows (train 57, validation 12, test 13) x 2,776 bins (405-3180 cm-1) + 6 targets (cell dry weight, fructose by HPLC, HHx, HB, residual CDW, urea), 1-5 missing per target; Tec5 Multi-Spec Raman at 785 nm. No column marks a row as measured or generated (Hugging Face dataset-server: the schema and the target columns of all 82 rows read).
- The decisive words: the dataset card, "This dataset contains Raman spectra (both real and synthetic) recorded during the batch cultivation of Ralstonia eutropha" and "The dataset utilizes a combination of experimental observations and high-fidelity synthetic data"; RamanBench's NEW_DATASETS.md, "The dataset combines experimental and high-fidelity synthetic spectra to address multicollinearity between correlated process variables"; raman-data, "Includes a hybrid mix of experimental and high-fidelity synthetic data". The cited paper builds spectra from NMF components of two real cultivations with concentrations "obtained from synthetic cultivations that are generated with the help of mechanistic models" (arXiv 2402.00851), and its abstract shows "the efficacy of the method on synthetic spectra of Ralstonia eutropha batch cultivations".
- Why no fix: SEL-16 excludes generated data. The mildest remedy, dropping the generated rows, needs to know which they are, and the release does not say (PROV-3); only the authors could tell (`Data Requested`, if the curator wants it). Even then the measured spectra come from "four independent batch cultivations" (NEW_DATASETS.md), so a monitoring task scored on new cultivations has four units (TP-5).
- Use case, had the data been measured: the operator of a PHA fermentation reads biomass, substrate and copolymer from an in-line spectrum instead of HPLC and gravimetry; regime grouped by cultivation.
- Siblings and duplicates: no duplicate (grep over the records for Ralstonia, eutropha, the DOI). Other bioprocess-monitoring records: `raman_ecoli_fermentation`, `raman_kaiser_ecoli_fermentation`, `raman_yeast_fermentation`, `raman_streptococcus_thermophilus_fermentation_kaiser`. External collections: RamanBench.
- Better data: a candidate of the benchmark RamanBench; no new search (run brief).
- Reject check (AI, 2026-10-31): stands. The data owners' card: 'This dataset contains Raman spectra (both real and synthetic)' and 'The dataset utilizes a combination of experimental observations and high-fidelity synthetic data' (https://huggingface.co/datasets/HTW-KI-Werkstatt/RamanSpectraRalstoniaFermentations). No column marks the generated rows, so they cannot be dropped. Even if the authors named them, the measured rows come from 'four independent batch cultivations' (https://github.com/ml-lab-htw/RamanBench/blob/main/NEW_DATASETS.md), Too Small (TP-5) for a task scored on new cultivations.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 82 spectra x 2,776 wavenumber features; 6 target(s) (raman-data id: ralstonia_fermentations); target: cell dry weight, substrate, copolymer fractions (6 targets).
- Why: Monitor P(HB-co-HHx) copolymer production in R. eutropha batch cultivations from in-line Raman spectra
- Notes: Raw Raman spectral bins (2,776 wavenumber points, 405-3180 cm-1) as features; SEL-15 judges such signals case by case. New with RamanBench (study: https://doi.org/10.1016/B978-0-443-28824-1.50510-X). Paper says it combines experimental and synthetic (augmented) spectra: check which rows are generated. HF mirror: ...
