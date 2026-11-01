---
unique_name: raman_flow_microgel_synthesis
name: Microgel Synthesis in Flow
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- TBD
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Tiny Data
- Many features
- Non-IID (Grouped)
collections:
- RamanBench
original_source: Other
year: '2023'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.1016/j.cej.2023.147567
- https://publications.rwth-aachen.de/record/959050
- https://arxiv.org/abs/2605.02003
- https://doi.org/10.18154/RWTH-2023-05551
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: in-line Raman spectra from 43 conditions of a Bayesian-optimised microgel flow synthesis with DLS particle sizes, a real monitoring task, but tiny, and the RamanBench copy's target is the run label, not the size.
- Source: Kaven, Schweidtmann, Keil, Israel, Wolter and Mitsos, "Dataset to 'Data-driven Product-Process Optimization of N-isopropylacrylamide Microgel Synthesis in Flow'", RWTH Aachen University, 2023 (https://doi.org/10.18154/RWTH-2023-05551, record 959050; CC BY 4.0 per raman-data's Croissant file): "in-line Raman spectroscopy measurements and predicted microgel sizes from Dynamic Light Scattering (DLS)" (DataCite). Paper: Kaven et al., Chemical Engineering Journal 479:147567, 2024 (https://doi.org/10.1016/j.cej.2023.147567). As published: a zip of SPC spectra (`Raman_Spectroscopy_Measurements.zip`) and two DLS tables (`Dynamic_Light_Scattering_size_predictions_at_20°C.xlsx` and `..._at_50°C.xlsx`, column "hydrodynamic radius [nm]"), joined by the run label in the spectrum's file name (raman-data's RWTH loader; the record page itself did not render). RamanBench copy: 86 spectra x 11,084 bins (100-3425 cm-1), target 0-42 = the index of 43 run labels V20-1 ... V31-5 (its metadata.json), so about two spectra per condition.
- Use case: the operator or the optimisation loop of a continuous microgel synthesis reads the particle size from the in-line spectrum instead of offline DLS; the study is a TS-EMO Bayesian optimisation "to simultaneously maximize product flow and achieve a targeted hydrodynamic radius of 100 nm" with initiator flow, monomer flow, CTAB and reactor temperature (60-80 °C) as its inputs (RamanBench A.18.4); fit approximate until the paper shows Raman used for size. Regime grouped by condition (two spectra per run label).
- Siblings and duplicates: no duplicate (grep for the DOIs and the record id). The same lab's microgel family: `raman_microgel_synthesis` (Kaven et al. 2021, flow against batch, 14 spectra) and `raman_microgel_size_lf_fingerprint` (235 microgels with DLS diameters, 14 preprocessing variants; whether its samples include these runs is unchecked, PROV-6). External collections: RamanBench (Table 57).
- Better data: a candidate of the benchmark RamanBench; no new search (run brief).
- Papers and pages: Kaven et al. 2024 (Elsevier, not reachable, no abstract in Crossref or Semantic Scholar); the DataCite record; RamanBench A.18.4; raman-data `RWTHLoader._load_flow_microgel_synthesis`.
- Metric: none found (paper not reachable; DataCite names none; RamanBench's RMSE is its benchmark-wide convention), so the fallback `rmse` on the radius in nm (MET-1); inputs none.
- Risks for /add-dataset: the RamanBench copy is wrong (PROV-15, to report to its maintainers): its loader returns the encoded run labels ("TODO how to get the real target?") and computes the DLS radii without using them, so its regression target is a run index and its R2 0.98 (Table 12) scores no size; rebuild from the RWTH files and join the radius by run label (20 °C or 50 °C: A.18.4 names both); 43 conditions (Tiny Data; TP-5 counts the radius's spread over groups); the process settings, known before the spectrum, may ship and would be features; 11,084 raw bins (SEL-15).
- Priority: gap 0, use case 0 (not verified in the paper), source + (data DOI and paper by the authors), shape 0 (43 conditions), risk - (the copy's target, a join to rebuild).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 86 spectra x 11,084 wavenumber features; 1 target(s) (raman-data id: flow_microgel_synthesis); target: hydrodynamic radius (DLS).
- Why: Monitor microgel size during continuous-flow synthesis (Bayesian-optimisation runs) from in-line Raman spectra
- Notes: Raw Raman spectral bins (11,084 wavenumber points, 100-3425 cm-1) as features; SEL-15 judges such signals case by case. Data DOI https://doi.org/10.18154/RWTH-2023-05551. HF mirror: https://huggingface.co/datasets/HTW-KI-Werkstatt/RamanBench/tree/main/flow_microgel_synthesis
