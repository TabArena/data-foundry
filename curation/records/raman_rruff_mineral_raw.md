---
unique_name: raman_rruff_mineral_raw
name: RRUFF Minerals (Raw)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
- Many features
- Many class
- Spectral Data
collections:
- RamanBench
original_source: Website
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Multiclass Classification
source_links:
- https://doi.org/10.1515/9783110417104-003
- https://rruff.info/
- https://arxiv.org/abs/2605.02003
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: the standard public reference library of mineral Raman spectra, but RamanBench's cut is a third-party bundle with about 15 spectra per species and no specimen id; a rebuild from rruff.info is the route.
- Source: the RRUFF Project (University of Arizona), https://rruff.info/, cited as Lafuente, Downs, Yang and Stone, "The power of databases: the RRUFF project", in Highlights in Mineralogical Crystallography, De Gruyter, 2015 (https://doi.org/10.1515/9783110417104-003). As published: spectra per specimen (an RRUFF id) for over 1,000 species, "measured under varying experimental conditions (e.g., 532 nm and 785 nm)" (raman-data card). RamanBench's cut: 1,162 spectra x 1,142 bins (303-853 cm-1, the range all spectra share after alignment), 79 species after dropping those with fewer than 10 spectra ("RRUFF with 79 mineral classes after rare-class filtering", App. A.3). raman-data does not read rruff.info: `GoogleDriveLoader._load_onewarmheart` takes `RRUFF_database/xy_raw.npy` and `yclass.npy` from a third-party `public_dataset.zip` on Google Drive, with preprocessing per github.com/onewarmheart/Raman.
- Use case: a mineralogist or gemmologist identifies an unknown specimen by its spectrum against the reference library; fit approximate: the library is built for search, and a 79-class classifier stands in for the search. Regime grouped by specimen (RRUFF id), since spectra of one specimen at several lasers and orientations are near copies; the bundle ships no id (SPLIT-24, SPLIT-25).
- Siblings and duplicates: `raman_mlrod` (Mars-analogue minerals, another source); the preprocessed RRUFF variant, left out of RamanBench, has no record; no duplicate (grep over the records for RRUFF, rruff.info, the DOI). External collections: RamanBench (a time-series classifier, Arsenal, tops its own splits at macro-F1 0.953 against 0.892 for TabPFN v2.5; another benchmark's score, no evidence, EV-4).
- Better data: a candidate of the benchmark RamanBench; no new search (run brief).
- Papers and pages: Lafuente et al. 2015 (chapter closed, abstract elided by the publisher); rruff.info and rruff.net returned 403; RamanBench Tables 3, 11, 16; raman-data `GoogleDriveLoader`.
- Metric: none found (a database, not a task; rruff.info and the chapter not readable here): fallback `log_loss` (MET-1, MET-5); RamanBench scores macro-F1.
- Risks for /add-dataset: rebuild from rruff.info with the RRUFF id as the group and one laser (PROV-13: the bundle's provenance and filtering cannot be checked); about 15 spectra per species leave a handful per class per grouped test fold (TP-5, TP-8); the aligned range 303-853 cm-1 drops most of each spectrum; whether modality models win (SEL-12) is for our probes; raw spectral bins weigh against (SEL-15).
- Priority: gap + (multiclass thin), use case 0 (the source's own words on the use not read), source + (the RRUFF project and its chapter), shape 0 (1,162 spectra, about 15 per class), risk - (third-party cut without a specimen id, few spectra per class).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 1,162 spectra x 1,142 wavenumber features; 79 classes (raman-data id: rruff_mineral_raw); target: mineral species.
- Why: Identify the mineral species from its reference Raman spectrum
- Notes: Raw Raman spectral bins (1,142 wavenumber points, 303-853 cm-1) as features; SEL-15 judges such signals case by case. Reference library; 79 of ~1,685 classes kept after dropping classes with < 10 spectra. Preprocessed variant excluded by the benchmark. HF mirror: ...
