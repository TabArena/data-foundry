---
unique_name: raman_yeast_fermentation
name: Yeast Fermentation
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
- Tiny Data
- Multi-target
- Many features
collections:
- RamanBench
original_source: Other
year: '2026'
problem_type: Regression
original_data_state: One Table
source_links:
- https://arxiv.org/abs/2605.02003
- https://huggingface.co/datasets/HTW-KI-Werkstatt/RamanSpectraEthanolicYeastFermentations
- https://doi.org/10.1002/bit.27112
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: a real soft-sensor task (an online Raman spectrum in, HPLC sugar, glycerol and ethanol concentrations out) released by the data owners, but only 58 spectra from continuous runs, shipped without a time or run column, as raw spectral bins.
- Source: Legner, Wirtz, Koza, Tetzlaff, Nickisch-Hartfiel and Jaeger, "Application of green analytical chemistry to a green chemistry process: Magnetic resonance and Raman spectroscopic process monitoring of continuous ethanolic fermentation", Biotechnology and Bioengineering 116(11), online 2019-07-21 (https://doi.org/10.1002/bit.27112), "originally published ... without providing access to the dataset" (RamanBench App. A.17.5). The data first appeared on Hugging Face (HTW-KI-Werkstatt/RamanSpectraEthanolicYeastFermentations, created 2026-02-03, CC BY 4.0) and in RamanBench (arXiv 2605.02003, 2026; Table 16 marks it "released for the first time with this paper"; Legner is a co-author), so the year is 2026 (PROV-9). As published: 58 spectra (files train 34, val 12, test 12) x 1,900 bins (401-2300 cm-1) + 4 targets in mol/L (glucose, fructose, glycerol, ethanol; "Reference concentrations ... were determined by HPLC", A.17.5); no time, run or setup column (Hugging Face dataset-server schema, 1,904 columns).
- Use case: the operator, or the feedback loop, of a continuous ethanol fermentation reads the metabolite concentrations from an online spectrum instead of waiting for HPLC: "suitable for real-time control realized as a feedback loop" (Legner 2019, abstract), "soft-sensor development, and real-time bioprocess control" (HF card). Fit direct: each row is one spectrum with its reference sample. Regime temporal by nature (spectra along the runs: a one-stage run of about 15 h and a two-stage run of 50 h per the HF card), but no timestamp ships, so SPLIT-7 and SPLIT-8 apply (forced IID, or grouped by run if the run can be recovered). Predicting the current concentration from the current spectrum is no forecast (SEL-10 does not apply).
- Siblings and duplicates: no duplicate (grep over the records for bit.27112, the HF id, "ethanolic"). The same task on other processes among the RamanBench records, all unscreened: `raman_ecoli_fermentation` (379 spectra), `raman_ralstonia_fermentations` (82), `raman_kaiser_ecoli_fermentation` (14), `raman_streptococcus_thermophilus_fermentation_kaiser` (14), `raman_bioprocess_substrates` (6,960 lab mixtures, not a process). raman-data also carries `yeast_bioreactor_fermentation` (Klaverdijk et al. 2025, https://doi.org/10.4121/4fbcf35e-1954-48a4-a2a3-693e19c753e7, about 65 samples in 5 batches with batch ids, glucose, ethanol and biomass), which has no record. External collections: RamanBench (best R2 per target 0.58 glucose to 0.90 ethanol, Table 4).
- Better data: a candidate of the benchmark RamanBench; no new search (run brief).
- Papers and pages: Legner et al. 2019 (PLS2 models; full text paywalled, not read); RamanBench App. A.17.5 and Table 23 (instrument, setup, HPLC reference); the HF card.
- Metric: none found from the source: the Legner 2019 abstract names none and the full text was not reachable (Wiley 403); RamanBench scores RMSE per target as a benchmark-wide convention (Sec. 4), not a choice for this task. So the fallback `rmse` on one target (MET-1, MET-5); inputs none.
- Risks for /add-dataset: the time order and the run are missing: recover them (the HF split files, the authors) or ship forced from temporal (SPLIT-7, SPLIT-8; SPLIT-25 if the runs matter and cannot be recovered). The HF card names a 3 L and a 2 L reactor and RamanBench a BIOSTAT B with 1 L working volume: clarify how many runs the 58 spectra come from (PROV-2). Four targets: pick one (ethanol, the product) or declare a multi-target (CLEAN-18). 58 rows (Tiny Data; TP-9 counts the target's spread per window). Raw spectral bins weigh against (SEL-15, weighed factor), though in RamanBench tabular foundation models and RamanNet lead on it.
- Priority: gap 0 (biology, regression and temporal not thin), use case + (the source names real-time feedback control), source + (paper, card and the benchmark's appendix by the data owners), shape 0 (58 rows of one feature type), risk - (time and run lost).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 58 spectra x 1,900 wavenumber features; 4 target(s) (raman-data id: yeast_fermentation); target: glucose, fructose, glycerol, ethanol (4 targets, HPLC reference).
- Why: Monitor continuous ethanolic fermentation of sucrose by immobilised S. cerevisiae from online handheld Raman spectra
- Notes: Raw Raman spectral bins (1,900 wavenumber points, 401-2300 cm-1) as features; SEL-15 judges such signals case by case. New with RamanBench; study Legner et al. 2019 (https://doi.org/10.1002/bit.27112) published without data. Time-ordered process data. HF mirror: ...
