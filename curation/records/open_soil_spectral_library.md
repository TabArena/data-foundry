---
unique_name: open_soil_spectral_library
name: Open Soil Spectral Library (OSSL) / KSSL MIR soil spectra
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
decision_markers:
- Wrong Domain / Source Modality
tags:
- AI-Filled (Verify)
- Many features
- Multi-target
- Non-IID (Grouped)
collections:
- New (BeyondArena)
original_source: Website
year: '2021'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.1371/journal.pone.0296545
- https://doi.org/10.5281/zenodo.7599269
- https://docs.soilspectroscopy.org/
- https://github.com/soilspectroscopy/ossl-models
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 4: a well documented open library of lab spectra with wet-chemistry reference values, built to calibrate the models that predict soil properties from a scan, in a spatially grouped regime; the open point is whether spectra are in scope (SEL-15).
- Source: Soil Spectroscopy for Global Good, Open Soil Spectral Library; data on Zenodo (doi 10.5281/zenodo.7599269, v1.2), paper Safanelli et al., PLOS ONE 20(1): e0296545, 2025. As published: 135,651 entries harmonised from KSSL, LUCAS, AfSIS1/2, ICRAF-ISRIC and smaller libraries; MIR and VisNIR scans plus about 40 soil properties (SOC, clay/silt/sand, pH, CEC, extractable cations, ...); 87,707 entries with coordinates; separate tables for site, lab values and each spectral range, joined by sample id. Licences differ per library (LUCAS under a JRC agreement; noted only, EV-4).
- Use case: the paper: users "need to predict soil properties from spectra collected on any spectrometer", and the OSSL Engine returns predictions for uploaded spectra; the actor is a soil lab or survey that scans a sample instead of running wet chemistry; fit direct. Regime grouped by location or profile (several layers per site); the paper's own 10-fold CV does not say it was grouped (SPLIT-3).
- Siblings and duplicates: `open_soil_data` (Lennart `No`: 96% of its values are spectroscopy-model predictions; this is a measured parent), `lucas_topsoil` (AI `TBD -> Yes`; LUCAS VisNIR spectra are inside OSSL), `africa_soil_property_prediction_challenge` (AfSIS MIR is inside OSSL), `bloodsai_blood_spectroscopy_classification_challenge` (the same spectroscopy question). Precedent for spectra: `micro_mass` (MALDI-TOF spectra, `Yes`, Lennart and Andrej). External collections: none found.
- Papers and pages: the PLOS ONE paper (Cubist ranked best; SNV and the first 120 principal components), docs.soilspectroscopy.org, github.com/soilspectroscopy/ossl-models.
- Metric: the paper reports RMSE, bias, R2, Lin's CCC and RPIQ and ranks models by CCC together with RPIQ, several side by side, so the fallback `rmse` on one property (MET-5, MET-11). Inputs: none.
- Risks for /add-dataset: pick one spectral range and one library cut (KSSL MIR is the largest single-instrument set) to avoid overlap with `lucas_topsoil` and the AfSIS records (PROV-6); one target, or a declared multi-target (CLEAN-18); some KSSL coordinates are county centroids, so group by profile or site, not by coordinate; about 1,700 MIR bins (raw spectral bins weigh -, SEL-15).
- Priority: gap + (Grouped thin), use case + (the paper names the users and the decision), source + (paper, Zenodo, docs), shape + (tens of thousands of samples, grouped), risk - (joins across tables, overlap with sibling libraries, the spectra question).

Safanelli et al., PLOS One 20(1):e0296545, 2025. Compilation of soil spectra with laboratory reference values, v1.2 on Zenodo (CC BY 4.0, 2021-12-26): "MIR (91,631) and VisNIR (65,063) spectral scans + soil calibration data (>60,000 unique locations)"; "from more than 135,000 entries in the OSSL, 87,707 samples have spatial coordinates". Table 1: KSSL (USA) 21,857 MIR + 10,521 VisNIR, CC; LUCAS (EU) 21,711 VisNIR under a "JRC license agreement" with geographic restrictions; AFSIS1 1,457 MIR (ODbL); AFSIS2 3,573 MIR (CC); ICRAF-ISRIC 1,841 MIR; CAF 715; Schiedung 422; Garrett 263; Serbia 410 (shared internally, not redistributable). Reference properties: >40 harmonised (SOC, clay/silt/sand, pH, CEC, extractable K/Ca/Mg/Na/P/B/Zn/Mn, EC, bulk density, ...). Own models: "Cubist was adopted as many studies have found it to be one of the top performing models", SNV preprocessing, "first 120 principal components" of each range; 10-fold CV Lin's CCC 0.95 for SOC (MIR), 0.84 pH, 0.74 clay.

Why it is the dataset to settle the spectroscopy question on: the incumbent models in this field are Cubist, PLSR and memory-based learning, i.e. tabular-style learners on ~1,700 wavenumber bins, so "modality-specific models clearly superior" (criterion 4A) is not obvious here; the `Wrong Domain / Source Modality` marker is the provisional flag, not a verdict. Same call would settle `bloodsai_blood_spectroscopy_classification_challenge`. Licence mix (LUCAS under a JRC agreement, Serbia internal) is noted, not a factor. Points to decide: one spectral range (MIR), spatially grouped split by site (many layers per location), and the library "spatially over-represents USA and European Union". Data not inspected.

Drafted 2026-09-23 as a follow-up to `open_soil_data` (iSDA), whose 49k rows are 96% spectroscopy-model predictions; this is one of the measured-data parents of that family (`open_soil_spectral_library`, `africa_soil_property_prediction_challenge`, `africa_soil_profiles_database`, `lucas_topsoil`, `wosis_soil_profiles`).

## Reference

Safanelli JL, Hengl T, Parente LL, Minarik R, Bloom DE, Todd-Brown K, et al. (2025). Open Soil Spectral Library (OSSL): Building reproducible soil calibration models through open development and community engagement. PLoS ONE 20(1): e0296545.
