---
unique_name: raman_microgel_size_lf_fingerprint
name: Microgel Size (Raw, Global)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
- Tiny Data
- Many features
collections:
- RamanBench
original_source: Other
year: '2024'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
source_links:
- https://doi.org/10.1002/aic.18494
- https://publications.rwth-aachen.de/record/959137
- https://arxiv.org/abs/2605.02003
- https://doi.org/10.18154/RWTH-2023-05604
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: a documented process-analytics task (microgel diameter from Raman spectra, DLS reference) from RWTH Aachen, but 47 samples, and this record stands for 14 preprocessing cuts of the same spectra.
- Source: Koronaki, Kaven, Faust, Kevrekidis and Mitsos, "Nonlinear manifold learning determines microgel size from Raman spectroscopy", AIChE Journal, online 2024-06-28 (https://doi.org/10.1002/aic.18494; preprint arXiv 2403.08376); data "Dataset to: Nonlinear Manifold Learning Determines Microgel Size from Raman Spectroscopy" (Kaven and Mitsos, RWTH Aachen, 2024, https://doi.org/10.18154/RWTH-2023-05604, record 959137, CC BY-NC 3.0): "off-line Raman spectroscopy measurements and predicted microgel sizes from Dynamic Light Scattering (DLS). The microgels are synthesized in a continuous flow reactor" (DataCite). As published, the abstract: "Raman spectra with associated size measured via dynamic light scattering of 47 microgel (cross-linked polymer) samples in a diameter range of 208–483 nm"; raw and pretreated spectra over a global and a fingerprint range ("raw and pretreated Raman spectra", preprint). RamanBench's cuts: 235 spectra x 11,084 bins (global, 100-3425 cm-1) or 3,500 (fingerprint, 800-1850 cm-1). raman-data cites a Small paper (doi 10.1002/smll.202311920, which returns 404); the AIChE paper is the one the data belongs to.
- Use case: the operator or control loop of a microgel synthesis reads the particle size from a Raman spectrum instead of DLS: "online reaction monitoring for closed-loop control is enabled" (preprint); fit approximate, the paper's spectra are off-line ("we acquire additional off-line Raman measurements of the same samples but at 20 °C"). Regime grouped by microgel sample (several spectra per sample; raman-data finds 45 replicate groups).
- Siblings and duplicates: this record carries the 14 RamanBench variants as aliases (`raman_microgel_size_{raw,lf,rb,mm_lf,mm_rb,snv_lf,snv_rb}_{global,fingerprint}`): processing cuts of the same 235 spectra, one dataset under PROV-6; RamanBench v1 keeps only `microgel_size_raw_global` (configs/v1), the cut the record's name describes. Same group, other experiments: `raman_flow_microgel_synthesis` (Kaven et al. 2024, CEJ, in-line, 86 spectra) and `raman_microgel_synthesis` (Kaven et al. 2021). External collections: RamanBench (App. A.10, Table 12; its scores are no evidence for our task, EV-4).
- Better data: a candidate of the benchmark RamanBench; no new search (run brief).
- Papers and pages: arXiv 2403.08376 (HTML read: "Out of the 47 pairs of microgel size and Raman spectra, we take 40 for training and 7 for testing"; "Each sample is measured three times via Raman spectroscopy"); the AIChE version (Wiley, not read); RamanBench App. A.10, Table 12.
- Metric: the paper reports R2, RMSE and MAPE side by side ("Overall, case (i) is the best-performing one for the available data set for R2 and MAPE"), no single criterion, so the fallback `rmse` (MET-5); RamanBench scores RMSE as a benchmark-wide convention. Inputs: the sample id for the grouped split.
- Risks for /add-dataset: build one cut, the raw spectra over the global range, from the RWTH files, and treat the 13 others as duplicates (PROV-6); the sample id must be recovered from the files, and 235 rows against "measured three times" for 47 samples needs a look (SPLIT-24); 47 units, about 9 per test fold (Tiny Data); the paper calls its own result a first "promising prediction", so the signal may be weak (TP-2 keeps a small real signal); 11,084 raw spectral bins (SEL-15); the record's unique name says `lf_fingerprint` while its name and size describe the raw global cut.
- Priority: gap 0 (chemistry and regression not thin), use case 0 (named, but the fit is approximate), source + (paper, preprint and RWTH deposit), shape 0 (47 samples), risk - (14 cuts, sample id to recover).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 235 spectra x 11,084 wavenumber features; 1 target(s) (raman-data id: microgel_size_raw_global); target: particle diameter (208-483 nm).
- Why: Predict NIPAM microgel particle diameter (DLS) from offline Raman spectra
- Notes: Raw Raman spectral bins (11,084 wavenumber points, 100-3425 cm-1) as features; SEL-15 judges such signals case by case. One of 14 preprocessing x spectral-range variants of the same 235 spectra (duplicates of one dataset). Licence CC BY-NC 3.0. raman-data cites https://doi.org/10.1002/smll.202311920; the paper cites ...
