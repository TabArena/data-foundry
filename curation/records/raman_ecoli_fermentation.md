---
unique_name: raman_ecoli_fermentation
name: E. coli Fermentation
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
- Multi-target
- Many features
- Non-IID (Grouped)
- Spectral Data
collections:
- RamanBench
original_source: Other
year: '2025'
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.1002/bit.70006
- https://huggingface.co/datasets/chlange/RamanSpectraEcoliFermentation
- https://arxiv.org/abs/2605.02003
- https://git.tu-berlin.de/bvt-htbd/kiwi/tf3/raman-kiwi-experiments
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: at-line Raman spectra of cell-free supernatant from 24 high-throughput E. coli fed-batch cultivations with analyzer reference values, built to feed glucose and acetate predictions into the feeding control; the open points are the spectra (SEL-15) and the cultivation id, which does not ship.
- Source: Lange, Seidel, Altmann, Stors, Kemmer, Cai, Born, Neubauer and Cruz Bournazou, "A Setup for Automatic Raman Measurements in High-Throughput Experimentation", Biotechnology and Bioengineering 122(10):2751-2769, online 2025-07-11 (https://doi.org/10.1002/bit.70006, CC BY 4.0, PMC12417782), with the data in the paper's repository "Raman Kiwi Experiments" (https://git.tu-berlin.de/bvt-htbd/kiwi/tf3/raman-kiwi-experiments, public, created 2025-04-09, named in the Data Availability Statement), so 2025. As published: folders `train/`, `val/`, `test/` with one `data.csv` each (the test file: 122 rows, 838 spectral columns from 300.78 cm-1, then `Glucose`, `Acetate`; header read by a range request). The Hugging Face copy chlange/RamanSpectraEcoliFermentation (created 2025-10-07, CC BY 4.0) has 379 rows (139/118/122) x 1,870 bins (391-3385 cm-1) + 2 targets, glucose missing in 6 rows. "We measured Raman spectra in 24 E. coli fermentations"; samples about hourly over a 4 h batch and a 4 h glucose-limited feed phase, two 10 s spectra per sample; reference glucose and acetate by a Cedex Bio HT analyzer.
- Use case: in a high-throughput bioprocess facility the platform predicts glucose and acetate for each at-line sample, and "the predictions are written to the database to allow other models to use them for adjusting feeding strategies" (Sec. 2.3); fit direct. Regime grouped by cultivation: "we divided the experiments into three groups at random" of 8 cultivations for training, validation and test (Sec. 2.6.4), and the three folders are those groups, so three folds over whole cultivations can be built exactly from the source (SPLIT-19, SPLIT-24); the two spectra of a sample share their target values.
- Siblings and duplicates: no duplicate (grep for the DOI and the HF id). Same platform and lab: `raman_ecoli_metabolites` (pipetted mixtures), `raman_bioprocess_analytes_anton_532` (the eight-instrument set the paper adds to its training data), `raman_bioprocess_substrates`. The same task on other runs: `raman_kaiser_ecoli_fermentation` (Kögler 2018, 14 samples of one run), `raman_yeast_fermentation` (screened `TBD -> 2nd Tier`, 2), `raman_ralstonia_fermentations`. External collections: RamanBench (arXiv 2605.02003, A.18.2 and Table 36, an existing dataset [97]).
- Better data: a candidate of the benchmark RamanBench; no new search (run brief).
- Papers and pages: the paper (a 1-D CNN tuned by Bayesian optimisation with Hyperband, 2,261 extra spectra from eight spectrometers in training; Sec. 2.6, 3.3); the HF card; RamanBench A.18.2.
- Metric: `mae` per analyte: "the mean absolute error of 0.27 g L-1 for glucose and 0.06 g L-1 for the acetate predictions" (Sec. 3.3) is the one error the paper reports on its test cultivations, so the source's metric (MET-5), on glucose or per target; inputs none.
- Risks for /add-dataset: no cultivation id in either copy: build the folds from the source's three groups (SPLIT-19) or ask the authors for the run ids (SPLIT-25 if neither works); the two copies differ in their spectral axis (838 columns from 300.78 cm-1 against 1,870 from 391 cm-1): take the repository's files and check which is raw (PROV-8, PROV-13); two targets: glucose, or both declared (CLEAN-18); raw spectral bins (SEL-15, weighed against), though calibrating on spectra is exactly the use case.
- Priority: gap 0 (regression, grouped not thin; domain unset), use case + (the source names the feeding decision), source + (paper, repository and card by the authors), shape 0 (about 190 samples in 24 cultivations, one feature type), risk - (no cultivation id, spectral bins).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 379 spectra x 1,870 wavenumber features; 2 target(s) (raman-data id: ecoli_fermentation); target: glucose, acetate concentrations (2 targets).
- Why: Predict glucose and acetate in E. coli fed-batch supernatant from at-line Raman spectra
- Notes: Raw Raman spectral bins (1,870 wavenumber points, 391-3385 cm-1) as features; SEL-15 judges such signals case by case. Multi-target. HF mirror: https://huggingface.co/datasets/HTW-KI-Werkstatt/RamanBench/tree/main/ecoli_fermentation
