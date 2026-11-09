---
unique_name: raman_fuel_benchtop
name: Gasoline Properties (Benchtop)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
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
year: '2025'
problem_type: Regression
original_data_state: One Table
source_links:
- https://arxiv.org/abs/2605.02003
- https://huggingface.co/datasets/chlange/FuelRamanSpectraBenchtop
- https://huggingface.co/datasets/HTW-KI-Werkstatt/FuelRamanSpectraHandheld
- https://doi.org/10.1016/j.fuel.2018.09.006
- https://doi.org/10.1021/acs.energyfuels.9b02944
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: 179 commercial gasolines with engine-measured octane numbers and additive contents and Raman spectra from a benchtop and a handheld spectrometer, for octane testing without the CFR engine; small, raw spectral bins.
- Source: the spectra were first released by the data owners on Hugging Face (chlange/FuelRamanSpectraBenchtop, created 2025-12-12; HTW-KI-Werkstatt/FuelRamanSpectraHandheld, 2025-12-16; CC BY 4.0; RamanBench Table 16 marks both new), from the studies Voigt, Legner, Haefner, Friesen, Wirtz and Jaeger, Fuel 236:829-835, 2019 (https://doi.org/10.1016/j.fuel.2018.09.006), and Legner et al., Energy & Fuels 34(1), online 2019-12-04 (https://doi.org/10.1021/acs.energyfuels.9b02944); year 2025 (PROV-9). As published (parquet schemas by range request): 179 rows x 961 bins (98-3801 cm-1; NXR FT-Raman, 1,064 nm) and 179 x 1,901 bins (400-2300 cm-1; IDRaman mini 2.0, 785 nm), 12 targets: RON for all 179, MON for 22, the other ten (ethanol, ETBE, MTBE, density, water, oxygenates, oxygen, olefins, aromatics, benzene) for 164. The samples: "130 refinery samples spanning RON 95-102.2 ... together with additional samples from petrol stations" (RamanBench A.17.7); RON by CFR engine (ASTM D2699), MON by ASTM D2885.
- Use case: a fuel inspector or laboratory rates a gasoline's octane near the pump with a fieldable spectrometer instead of an engine test (Voigt 2019 abstract: "the feasibility of fast and simple near-pump RON determination"); fit direct for RON. Regime IID over fuel samples; the refinery or station origin, the paper's train-then-apply design, does not ship, and raman-data finds repeated target tuples that may be repeat measurements (check, SPLIT-24).
- Siblings and duplicates: no duplicate (grep for the DOIs, "octane", "gasoline"). The record merges the benchtop and handheld spectra of the same 179 samples (PROV-6: one dataset, one instrument or both as columns). External collections: RamanBench (Tables 25, 26).
- Better data: a candidate of the benchmark RamanBench; no new search (run brief).
- Papers and pages: Voigt et al. 2019 (PCA, support vector regression; handheld Raman and 1H NMR at 80 MHz against benchtop NIR); Legner et al. 2019 (data fusion, additives; abstract only); the HF cards; RamanBench A.17.7.
- Metric: Voigt 2019: "The goodness of the method is expressed both in terms of computational residual mean squared errors and the common experimental reproducibility and repeatability limits", "40-50% of the samples are predicted within 0.2 and 80-90% with 0.7 RON" (abstract): two criteria, so the fallback `rmse` on RON, which is the paper's computational one (MET-5); the share within the ASTM limits would be a custom metric the source does not name as its one criterion; inputs none.
- Risks for /add-dataset: the sample origin (refinery or station) and a sample id are missing (PROV-2; ask the owners); MON for 22 of 179: ship RON (CLEAN-18); two instruments on the same samples (PROV-6); raw spectral bins (SEL-15, weighed against); 179 rows (Tiny Data).
- Priority: gap 0 (regression, IID not thin; domain unset), use case + (the source names near-pump testing against the CFR engine), source + (two papers and the owners' release), shape 0 (179 samples, one feature type), risk - (origin missing, spectral bins).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 179 spectra x 961 wavenumber features; 12 target(s) (raman-data id: fuel_benchtop); target: RON, MON, ethanol, oxygenates (MTBE, ETBE), benzene and other properties (12 targets).
- Why: Predict octane numbers and additive contents of commercial gasoline from Raman spectra (Benchtop FT-Raman, 1064 nm) | Predict octane numbers and additive contents of commercial gasoline from Raman spectra (Handheld Raman, 785 nm)
- Notes: Raw Raman spectral bins (961 wavenumber points, 98-3801 cm-1) as features; SEL-15 judges such signals case by case. New with RamanBench; studies Voigt et al. 2019 (https://doi.org/10.1016/j.fuel.2018.09.006) and Legner et al. 2019 (https://doi.org/10.1021/acs.energyfuels.9b02944). Same 179 samples as the other ...
