---
unique_name: raman_microgel_synthesis
name: Microgel Synthesis Flow vs. Batch
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
- Tiny Data
- Many features
collections:
- RamanBench
original_source: Other
year: '2021'
domain: chemistry & material science
problem_type: Regression
source_links:
- https://doi.org/10.18154/RWTH-2021-09666
- https://publications.rwth-aachen.de/record/834113
- https://arxiv.org/abs/2605.02003
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: an RWTH deposit of in-line Raman measurements in a microgel flow reactor, but it documents spectra and indirect hard models for calibration and composition monitoring, names no size measurement, and RamanBench's cut is 14 spectra of one synthesis experiment with a target read from file names.
- Source: Kaven et al., "In-line Monitoring of Microgel Synthesis: Flow versus Batch Reactor", Organic Process Research & Development 25(9):2039-2051, 2021 (citation per raman-data; the paper not read); data "Dataset to: In-line Monitoring of Microgel Synthesis: Flow versus Batch Reactor" (Kaven, Wolff, Wille, Wessling, Mitsos and Viell, RWTH Aachen, 2021, https://doi.org/10.18154/RWTH-2021-09666, record 834113, CC BY 4.0; `Raman_spectra_and_Indirect_Hard_Models.zip`). As published (DataCite): "The measurements include a systematic accuracy analysis, where different aspects of the flowing analyte are considered: solvent flow, flowing monomer solution, and flowing microgel solution. In addition, measurements for different calibration strategies are included. Lastly, this data set contains measurements of the microgel synthesis at varying residence times inside the tubular flow reactor." RamanBench's cut: 14 spectra x 11,084 bins (100-3425 cm-1); the raman-data loader reads one folder, `3_Synthesis experiments/20190606_70°C_Exp3`, and takes the target from characters 19-24 of each file name, with the comment "TODO how to get the real target? from filename? somewhere else?"; RamanBench calls the target "microgel hydrodynamic radius" and raman-data finds replicate spectra per condition.
- Use case: the operator of a flow reactor follows the synthesis in line from Raman spectra (title, deposit); the deposit is built for calibration and composition (indirect hard models), so what a task from these files predicts is unclear: a size, a residence time from a file name, or a concentration (USE-5, PROV-2). Regime grouped by condition (replicate spectra per residence time).
- Siblings and duplicates: `raman_flow_microgel_synthesis` (Kaven et al. 2024, Chemical Engineering Journal, the same group's later flow-synthesis deposit, 86 in-line spectra with a DLS radius, data https://doi.org/10.18154/RWTH-2023-05551): the larger record of the in-line size task; `raman_microgel_size_lf_fingerprint` (off-line size of 47 samples, same group). No duplicate (grep over the records for microgel and the DOI). External collections: RamanBench (its scores are no evidence for our task, EV-4).
- Better data: a candidate of the benchmark RamanBench; no new search (run brief).
- Papers and pages: the deposit's DataCite metadata; raman-data `RWTHLoader._load_microgel_synthesis`; RamanBench (the cut's size: "11,084 points across 14 spectra, a 792:1 feature-to-sample ratio"). The OPRD paper and the RWTH record page were not read (the page answers with a bot challenge).
- Metric: none found (the paper not read); for a size or concentration regression the fallback `rmse` (MET-1).
- Risks for /add-dataset: settle the target first, from the zip's file names and any DLS or conversion table (USE-5, PROV-2); 14 spectra of one experiment are a handful of units, `Too Small` (TP-5) unless the source holds more synthesis spectra with a measured target; the calibration and accuracy measurements make another task (monomer concentration); raw spectral bins weigh against (SEL-15).
- Priority: gap 0 (chemistry and regression not thin), use case 0 (the target is unclear), source + (RWTH deposit with a paper), shape 0 (14 spectra in the known cut), risk - (unclear target, tiny).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 14 spectra x 11,084 wavenumber features; 1 target(s) (raman-data id: microgel_synthesis); target: microgel hydrodynamic radius.
- Why: Monitor microgel size during synthesis in a tubular flow reactor from in-line Raman spectra
- Notes: Raw Raman spectral bins (11,084 wavenumber points, 100-3425 cm-1) as features; SEL-15 judges such signals case by case. Paper: Kaven et al. 2021, Org. Process Res. Dev. 25(9). Tiny (N < 50). HF mirror: https://huggingface.co/datasets/HTW-KI-Werkstatt/RamanBench/tree/main/microgel_synthesis
