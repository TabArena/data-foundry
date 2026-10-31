---
unique_name: pasion_horizontal_pv_power_12_sites
name: Northern Hemisphere Horizontal Photovoltaic Power Output Data for 12 Sites (Pasion et al.)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Other
year: '2019'
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.17632/hfhwmn8w24.5
- https://data.mendeley.com/datasets/hfhwmn8w24/5
- https://doi.org/10.3390/en13102570
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: power output of horizontal polycrystalline PV panels at 12 northern-hemisphere sites over 14 months with the weather at the sampling time (about 21,000 rows, 17 columns), from a documented release with a paper; the likely origin of `speoau_energy_data_hackathon`.
- Source: Jada Williams and Torrey Wagner (Air Force Institute of Technology), "Northern Hemisphere Horizontal Photovoltaic Power Output Data for 12 Sites", Mendeley Data v5, 2019-07-31, doi 10.17632/hfhwmn8w24.5, CC BY 4.0 (page read 2026-10-31): columns "location, date, time sampled, latitude, longitude, altitude, year and month, month, hour, season, humidity, ambient temperature, solar panel power output, wind speed, visibility, pressure, and cloud ceiling"; the sampling interval and the instruments are not stated on the page. Paper: Pasion, Wagner, Koschnick, Schuldt, Williams and Hallinan, "Machine Learning Modeling of Horizontal Photovoltaics Using Weather and Location Data", Energies 13(10):2570 (2020; abstract through Semantic Scholar, the MDPI page returned 403): output predicted without irradiation data; a distributed random forest on latitude, month, hour and weather reached R² 0.94, per-location models 0.91 to 0.97. About 21,000 rows (the scout's estimate from the 2.2 MB file, not counted).
- Use case: a grid operator or planner estimates horizontal-PV output at a site from weather and location where no irradiance is measured (the abstract's motivation, grid integration); the actor is named only in general; fit approximate. Regime grouped by site for a new location (12 sites) or temporal within sites; rows are time samples, so not IID; one regime to pick (USE-10).
- Siblings and duplicates: `speoau_energy_data_hackathon` (AI `TBD -> 2nd Tier`, `Missing source information`: 2,920 Zindi rows of PV output from the same kind of weather variables, possibly a cut of this table; check by rows, PROV-4). No other record of this release (grep: hfhwmn8w24, en13102570). External collections: none found.
- Better data: found as better data for `speoau_energy_data_hackathon`; no further search this round.
- Papers and pages: Pasion et al. 2020 (34 citations per Semantic Scholar).
- Metric: R² is the abstract's figure; the full text (whether it ranks models by R² alone or also reports MAE and RMSE) was not read, so the fallback `rmse` unless the paper names one deliberate criterion (MET-5, MET-8); inputs none.
- Risks for /add-dataset: the same-time weather makes this an estimate, not a forecast; keep it so (no lagged output; SEL-10, SEL-11, the `Time-series (Regression)` question); latitude, longitude and altitude identify the site, so under a site-grouped split they only describe it; the sampling and the units need the paper's methods.
- Priority: gap 0, use case 0 (general motivation, approximate fit), source + (Mendeley release and paper), shape + (about 21,000 rows, 12 sites, 14 months), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `speoau_energy_data_hackathon`.
- as published: Samples of power output from horizontal PV panels at 12 northern-hemisphere sites over 14 months; one CSV of 2.2 MB with 17 columns (location, date, time, latitude, longitude, altitude, year-month, ...; target: Power output of a horizontal polycrystalline PV panel (PolyPwr); access: open.
- Why: Same task as speoau_energy_data_hackathon: PV output from 'temperature, pressure, wind speed, humidity and other factors'; the record already names it as the possible origin of the 2,920 Zindi rows
- Adds: About 7x the rows, 12 sites instead of an unnamed one, a traceable first publication with a paper (the record's blocker is Missing source information), CC BY 4.0. If the Zindi data turns out to be a cut of it (check by rows), this is the original, and the Zindi record a PROV-4 duplicate. Risk: rows are time samples ...
