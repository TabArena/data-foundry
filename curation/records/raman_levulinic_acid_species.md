---
unique_name: raman_levulinic_acid_species
name: Levulinic Concentration
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
- Tiny Data
- Multi-target
- Many features
- Spectral Data
collections:
- RamanBench
original_source: Other
year: '2024'
domain: chemistry & material science
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.1177/0003702820973275
- https://publications.rwth-aachen.de/record/978266
- https://arxiv.org/abs/2605.02003
- https://doi.org/10.18154/RWTH-2024-01177
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: 36 in-line Raman spectra along one levulinic-acid titration with the measured pH and the added base, one slice of the seven-acid RWTH release (the record also covers the 70-spectrum succinic-acid series); a tiny single series.
- Source: the release of `raman_formic_acid_species`: Echtermeyer, Marks, Mitsos and Viell, RWTH Aachen University, 2024 (https://doi.org/10.18154/RWTH-2024-01177, record 978266; CC0 per raman-data), the data to the Applied Spectroscopy paper 75(5):506-519 (https://doi.org/10.1177/0003702820973275), whose abstract names itaconic, formic, acetic and citric acid but not levulinic or succinic. As published: per acid a folder of SPC spectra and a "Data Table ... Acid Titration.xlsx". RamanBench copy (parquet schemas by range request): levulinic 36 spectra x 11,084 bins + `pH` (2.2-12.7) and `Mass of NaOH` (0-35.4); succinic 70 x 11,567 bins from two titrations (`20221019_V489`, `20221104_V490`) with the same two columns. raman-data takes these two columns with the note "TODO are these two really of interest?", so the xlsx may hold species fractions too.
- Use case: a process engineer reads the pH or the dissociation state of an acid in a process from the in-line spectrum (the paper's "process analytical technology"); fit approximate: a lab titration stands in for the process, and the mass of NaOH is the titration's own dose, not a process quantity. Regime: one series per titration (succinic has two, the only grouping available).
- Siblings and duplicates: no duplicate. The release is split over `raman_acetic_acid_species` (acetic, citric, itaconic), `raman_formic_acid_species` and this record (levulinic, succinic): the curator decides between one dataset per acid, one pooled dataset, or one acid (PROV-6, PROV-7). External collections: RamanBench (Tables 54, 58).
- Better data: a candidate of the benchmark RamanBench; no new search (run brief).
- Papers and pages: the paper (SAGE full text not read); the DataCite record; RamanBench A.18.4; raman-data `RWTHLoader._load_acid_species`.
- Metric: none found for levulinic or succinic acid (the paper's abstract does not cover them), so the fallback `rmse` on pH (MET-1); inputs none.
- Risks for /add-dataset: 36 rows of one titration (`Too Small` and `Trivial` questions, TP-4, TP-5); pick the target from the xlsx (pH, or species fractions if present; USE-5); `Mass of NaOH` orders the series and is no use-case target; 11,084 raw bins (SEL-15).
- Priority: gap 0, use case 0 (approximate), source + (data DOI and paper by the authors), shape 0 (36 spectra), risk - (one series, a target to choose).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 36 spectra x 11,084 wavenumber features; 2 target(s) (raman-data id: levulinic_acid_species); target: pH, mass of NaOH added (2 targets).
- Why: Quantify dissociated levulinic acid species during titration from in-line Raman spectra (process monitoring) | Quantify dissociated succinic acid species during titration from in-line Raman spectra (process monitoring)
- Notes: Raw Raman spectral bins (11,084 wavenumber points, 100-3425 cm-1) as features; SEL-15 judges such signals case by case. One of 6 acids from the same titration study (RWTH, CC0). Tiny (N < 50). HF mirror: https://huggingface.co/datasets/HTW-KI-Werkstatt/RamanBench/tree/main/levulinic_acid_species | Raw Raman spectral ...
