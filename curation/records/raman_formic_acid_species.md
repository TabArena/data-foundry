---
unique_name: raman_formic_acid_species
name: Formic Concentration
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

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: 24 in-line Raman spectra along one formic-acid titration with the species mole fractions, one slice of a seven-acid RWTH release; a real process-analytics calibration, but a single tiny series.
- Source: Echtermeyer, Marks, Mitsos and Viell, "Dataset to 'Inline Raman Spectroscopy and Indirect Hard Modeling for Concentration Monitoring of Dissociated Acid Species'", RWTH Aachen University, 2024 (https://doi.org/10.18154/RWTH-2024-01177, record 978266; CC0 per raman-data): "Raman spectra assigned to composition data from sample preparation and titration experiments" for acetic, citric, formic, itaconic, levulinic, oxalic and succinic acid (DataCite). Paper: Applied Spectroscopy 75(5):506-519, online 2020-12-04 (https://doi.org/10.1177/0003702820973275), which analyses itaconic acid in detail and applies the method "to formic, acetic, and citric acid in water" (abstract). As published: per acid a folder of SPC spectra and an xlsx data table. RamanBench copy (parquet schema by range request): 24 spectra x 11,084 bins (100-3425 cm-1) + `Formic acid (FA)`, `Formiate (FA-)`, `water` in mol/mol (formic acid 0-0.018, water 0.981-1.0).
- Use case: a process engineer monitors the dissociation state of a carboxylic acid in a fermentation or downstream process from an in-line spectrum (the abstract: "a process analytical technology for quantitative monitoring of processes containing carboxylic acids"); fit approximate: a lab titration of one acid in water stands in for the process. Regime: one titration series ordered by the added base, no replicates (raman-data's check); a random split interpolates along one curve.
- Siblings and duplicates: no duplicate. The release is split over three records: `raman_acetic_acid_species` (acetic, with citric and itaconic as aliases), this one, and `raman_levulinic_acid_species` (with succinic); oxalic is not loaded by raman-data. One release with distinct analytes (PROV-7 keeps them apart; PROV-6 applies if the curator sees one task): the curator decides between one dataset per acid, one pooled dataset, or one acid. External collections: RamanBench (Table 51).
- Better data: a candidate of the benchmark RamanBench; no new search (run brief).
- Papers and pages: the paper (indirect hard modeling and MCR against PLS: "With only four calibration samples, IHM yields more accurate results than partial least squares regression", abstract; SAGE full text not read); RamanBench A.18.4.
- Metric: the paper compares methods by the hard-model error in mol/mol (abstract), definition not read, so the fallback `rmse` on one species (MET-1, MET-5); inputs none.
- Risks for /add-dataset: 24 rows of one series (`Too Small` and `Trivial` questions, TP-4, TP-5; RamanBench's best mean R2 of 0.72 is a third party's score, PROV-15); the mole fractions are likely computed from the titration with known pKa ("calibrated with calculated ideal dissociation equilibria", method A), not measured, and water is about one minus the rest: three framings of one signal (CLEAN-18); 11,084 raw bins (SEL-15).
- Priority: gap 0, use case 0 (approximate), source + (data DOI and paper by the authors), shape 0 (24 spectra), risk - (one series, computed targets).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 24 spectra x 11,084 wavenumber features; 3 target(s) (raman-data id: formic_acid_species); target: formic acid, formate, water (3 targets).
- Why: Quantify dissociated formic acid species during titration from in-line Raman spectra (process monitoring)
- Notes: Raw Raman spectral bins (11,084 wavenumber points, 100-3425 cm-1) as features; SEL-15 judges such signals case by case. One of 6 acids from the same titration study (RWTH, CC0). Tiny (N < 50). HF mirror: https://huggingface.co/datasets/HTW-KI-Werkstatt/RamanBench/tree/main/formic_acid_species
