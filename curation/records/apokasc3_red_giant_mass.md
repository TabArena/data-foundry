---
unique_name: apokasc3_red_giant_mass
name: 'APOKASC-3: joint APOGEE spectroscopic and Kepler asteroseismic catalog of evolved stars'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Selection Bias
tags:
- AI-Filled (Verify)
original_source: Other
year: '2024'
domain: physics & astronomy
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.3847/1538-4365/ad9fef
- https://arxiv.org/abs/2410.00102
- https://doi.org/10.5281/zenodo.13308665
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 12,418 Kepler red giants with asteroseismic masses (the target, measured from oscillations) and APOGEE spectroscopic parameters (the features, another instrument), a set the paper itself offers as a training set for other surveys; physics and astronomy has no accepted dataset, but the mass comes from scaling relations whose inputs partly overlap the features.
- Source: Pinsonneault, Zinn, Tayar, Serenelli, García, Mathur, Johnson et al. (173 authors), "APOKASC-3: The Third Joint Spectroscopic and Asteroseismic catalog for Evolved Stars in the Kepler Fields", ApJS 276(2):69, 2025 (arXiv:2410.00102, 2024-09-30); the SDSS internal version of the catalogue on Zenodo (doi 10.5281/zenodo.13308665, 2024-08-12, CC BY 4.0, `APOKASC_cat_v7.4.0` as FITS and text, 299 MB, with a column header file; it holds every APOGEE DR17 star in the Kepler field, and where file and journal disagree "the journal values are the version of record"). As published (abstract): 15,808 evolved stars; evolutionary state, seismic log g, mass, radius and age with the measurements used to derive them for 12,418 stars (10,036 high precision), 1,624 more with limited data. Table 4, "Catalog of Recommended Stellar Properties" (arXiv HTML): KIC, Gaia and 2MASS ids; EvolState, ESSource, CatTab; Numax, Dnu, Loggseis; Teff, Loggspec, FeH, AlpFe, CFe, NFe, Vsini, alpha class; Mass, Radius, InvRGaia, RecAge, AgeRGB, AgeRC, each with an uncertainty column. Year 2024: the Zenodo file is the first release of rows.
- Use case: a spectroscopic survey (APOGEE, Milky Way Mapper, 4MOST) assigns masses and ages to giants that have a spectrum but no asteroseismology, for Galactic archaeology; the paper calls its gold sample "an excellent training set for inferring ages in other surveys" (arXiv HTML, catalogue section), and Martig et al. 2016 (MNRAS 456:3655) fit the [C/N] mass relation on 1,475 APOKASC giants and applied it to about 52,000 APOGEE DR12 giants. No decision beyond a catalogue value, so the fit is approximate; the Kepler-field stars were picked for seismic monitoring while the use case predicts for giants elsewhere (`Selection Bias`, the `sdss_17` clause). Regime IID over stars (no grouping in the source).
- Siblings and duplicates: no other APOKASC record (searched APOKASC, APOGEE, asteroseismology, red giant); `kepler_koi_disposition` and `kepler_dr24_tce_vetting` are planet-vetting tasks; `cosmicflows4_tully_fisher` (`TBD -> 2nd Tier`: its target is computed from its own columns, here the target comes from another instrument); `sdss_17` (`Yes`). The earlier releases APOKASC-1 and APOKASC-2 have no record; APOKASC-3 is the newest (PROV-6). External collections: none found.
- Better data: from the gap scout for physics and astronomy; no further search this round.
- Papers and pages: the ApJS paper (arXiv abstract and HTML); the Zenodo record; Martig et al. 2016 (search snippets: masses with "fractional rms errors of about 14 per cent", ages 40%); Ness et al. 2016 (The Cannon) and Ting et al. 2018 (red-clump selection), named by the scout, not read.
- Metric: none found in the source (APOKASC-3 defines no prediction task; read: the arXiv abstract and HTML); Martig et al. report an rms error, so the fallback `rmse` on the mass (MET-1, MET-8); inputs none.
- Risks for /add-dataset: drop every seismic and derived column (Numax, Dnu, Loggseis, Radius, InvRGaia, the ages), from which the mass follows by the scaling relations; Loggspec is calibrated to the seismic log g (the paper: the spectroscopic log g scale is tied to asteroseismic surface gravities) and Teff enters the scaling relation, so part of the signal may be by construction (LEAK, TP-4 to probe); no Gaia radius (with log g it gives the mass by formula); mass rather than age (ages are model-dependent); `ESSource` marks states taken from spectroscopy (for a state target); prefer the journal's Table 4 to the Zenodo internal file; the sample is the Kepler field only.
- Priority: gap + (physics and astronomy has no accepted dataset), use case 0 (a calibration use the paper names, no decision), source + (ApJS paper, Zenodo with a column header), shape + (12,418 stars, about ten spectroscopic features and the state), risk - (a target built by scaling relations from inputs partly shared with the features).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the gap scout for physics and astronomy.
- as published: Red giants in the Kepler field: 15,808 stars; evolutionary state, mass, radius and age for 12,418 (10,036 high precision), limited data for 1,624 more; machine-readable Table 4 with KIC, Gaia and ...; target: Asteroseismic stellar mass (or age) from spectroscopic parameters; alternatively evolutionary state, red giant branch vs red clump; access: open.
- Why: A published calibration task (Martig et al. 2016 masses from [C/N]; Ness et al. 2016; Ting et al. 2018 red-clump selection) whose target is measured by a different instrument (Kepler oscillations) than the features (APOGEE spectra); strong source
- Adds: A measurement-substitution regression or binary task in astronomy (like infrared_thermography_temperature). Risks: drop the seismic columns (numax, dnu, radius, seismic log g give mass by scaling relation); ESSource marks rows whose state comes from spectroscopy (drop for the state task); ages are model-dependent, ...
