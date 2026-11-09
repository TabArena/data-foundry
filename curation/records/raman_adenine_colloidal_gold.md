---
unique_name: raman_adenine_colloidal_gold
name: Adenine Colloidal (Gold)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- TBD
- Not Representative
tags:
- AI-Filled (Verify)
- Many features
- Spectral Data
collections:
- RamanBench
original_source: Other
year: '2019'
domain: chemistry & material science
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.1021/acs.analchem.9b05658
- https://doi.org/10.5281/zenodo.3572359
- https://arxiv.org/abs/2605.02003
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages, the release file listings and a two-column preview of the data, NOT from a build. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: a documented 15-laboratory SERS study (3,516 spectra with lab, substrate and laser columns), but adenine in buffer is a model analyte of a method-reproducibility study, the concentrations are a few designed levels, and this record's cut (colloidal gold, 225 spectra) is the smallest of four.
- Source: Fornasaro et al., "Surface Enhanced Raman Spectroscopy for Quantitative Analysis: Results of a Large-Scale European Multi-Instrument Interlaboratory Study", Analytical Chemistry, online 2020-02-21 (PMC7997108); data on Zenodo, doi 10.5281/zenodo.3572359, 2019-12-16, CC BY 4.0, "isSupplementTo" the paper. As published: "all the 3516 spectra uploaded by all participants" in one CSV whose rows carry "labcode", "substrate", "laser", "method", "sample", "type", "conc", "batch", "replica" and the intensities 400-2000 cm-1 (NA outside a lab's range), plus one TXT per spectrum. Six methods (cAg@532, cAg@785, cAu@785, sAg@532, sAg@785, sAu@785) in 15 labs; calibration and test samples prepared centrally (the levels are in the Supporting Information, not read). RamanBench cuts it by substrate: colloidal gold 225, colloidal silver 630, solid gold 810, solid silver 1,851 spectra (534 bins).
- Use case: the study aimed "to define a methodology to assess the reproducibility and trueness of a quantitative SERS method and to compare different methods" (Abstract), and "this study is more about methodology than performance" (Limitations); nobody acts on an adenine concentration. Fit approximate at best (a lab quantifying an analyte by SERS): each lab fit its own linear calibration on the band 715-750 cm-1 and predicted its own test samples. Regime grouped by lab and batch: a new lab or substrate batch is the interlaboratory question.
- Siblings and duplicates: no other record of these data (grep by DOI, Zenodo id, "adenine"); the other three substrate cuts are aliases of this record (PROV-6: cuts by substrate add no task; one dataset over all 3,516 spectra with the method columns as features, or the largest cut, replaces them). Other SERS records of the run: `raman_hair_dyes_sers`, `raman_cancer_cell_cooh`, `raman_serum_prostate_cancer`. External collections: RamanBench (four "Adenine" datasets).
- Better data: a candidate of the benchmark RamanBench (arXiv 2605.02003); no further search in this run.
- Papers and pages: the paper (PMC7997108, read through a page summary), the Zenodo record.
- Metric: RMSEP, the study's accuracy figure that combines precision and trueness ("RMSEP² ≅ SEP² + BIAS²", Table 1), compared across methods in Table 3 after range normalisation: a deliberate choice (MET-5), so rmse on the concentration. Inputs none.
- Risks for /add-dataset: few distinct concentration levels (TP-5 on the target's spread); a model analyte with no decision (`Not Representative`, USE-2 borderline); the source calibrates per lab, while pooling labs makes a transfer task (decide the regime from the use case, SPLIT-23); labs cover different spectral ranges (NA padding); raw spectral bins (SEL-15).
- Priority: gap - (regression, chemistry not thin), use case - (a method study, no decision), source + (paper, Zenodo with full metadata), shape + (3,516 spectra over the source with categorical method columns, grouped by lab), risk - (few target levels, model analyte).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 225 spectra x 534 wavenumber features; 1 target(s) (raman-data id: adenine_colloidal_gold); target: adenine concentration.
- Why: Quantify adenine from SERS spectra on colloidal gold substrates measured in many European labs (interlaboratory study) | Quantify adenine from SERS spectra on colloidal silver substrates measured in many European labs (interlaboratory study) | Quantify adenine from SERS spectra on solid gold substrates measured in ...
- Notes: Raw Raman spectral bins (534 wavenumber points, 400-1999 cm-1) as features; SEL-15 judges such signals case by case. Paper marks Adenine as newly released, but raman-data loads it from the 2019 Zenodo record of Fornasaro et al. Few concentration levels; laboratory is a natural group. HF mirror: ...
