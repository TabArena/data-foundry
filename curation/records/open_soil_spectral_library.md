---
unique_name: open_soil_spectral_library
name: Open Soil Spectral Library (OSSL) / KSSL MIR soil spectra
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
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

Safanelli et al., PLOS One 20(1):e0296545, 2025. Compilation of soil spectra with laboratory reference values, v1.2 on Zenodo (CC BY 4.0, 2021-12-26): "MIR (91,631) and VisNIR (65,063) spectral scans + soil calibration data (>60,000 unique locations)"; "from more than 135,000 entries in the OSSL, 87,707 samples have spatial coordinates". Table 1: KSSL (USA) 21,857 MIR + 10,521 VisNIR, CC; LUCAS (EU) 21,711 VisNIR under a "JRC license agreement" with geographic restrictions; AFSIS1 1,457 MIR (ODbL); AFSIS2 3,573 MIR (CC); ICRAF-ISRIC 1,841 MIR; CAF 715; Schiedung 422; Garrett 263; Serbia 410 (shared internally, not redistributable). Reference properties: >40 harmonised (SOC, clay/silt/sand, pH, CEC, extractable K/Ca/Mg/Na/P/B/Zn/Mn, EC, bulk density, ...). Own models: "Cubist was adopted as many studies have found it to be one of the top performing models", SNV preprocessing, "first 120 principal components" of each range; 10-fold CV Lin's CCC 0.95 for SOC (MIR), 0.84 pH, 0.74 clay.

Why it is the dataset to settle the spectroscopy question on: the incumbent models in this field are Cubist, PLSR and memory-based learning, i.e. tabular-style learners on ~1,700 wavenumber bins, so "modality-specific models clearly superior" (criterion 4A) is not obvious here; the `Wrong Domain / Source Modality` marker is the provisional flag, not a verdict. Same call would settle `bloodsai_blood_spectroscopy_classification_challenge`. Licence mix (LUCAS under a JRC agreement, Serbia internal) is noted, not a factor. Points to decide: one spectral range (MIR), spatially grouped split by site (many layers per location), and the library "spatially over-represents USA and European Union". Data not inspected.

Drafted 2026-09-23 as a follow-up to `open_soil_data` (iSDA), whose 49k rows are 96% spectroscopy-model predictions; this is one of the measured-data parents of that family (`open_soil_spectral_library`, `africa_soil_property_prediction_challenge`, `africa_soil_profiles_database`, `lucas_topsoil`, `wosis_soil_profiles`).

## Reference

Safanelli JL, Hengl T, Parente LL, Minarik R, Bloom DE, Todd-Brown K, et al. (2025). Open Soil Spectral Library (OSSL): Building reproducible soil calibration models through open development and community engagement. PLoS ONE 20(1): e0296545.
