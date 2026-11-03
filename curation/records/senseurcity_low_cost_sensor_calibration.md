---
unique_name: senseurcity_low_cost_sensor_calibration
name: 'SensEURCity: a multi-city air quality dataset collected using networks of open low-cost sensor systems'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Time-series (Regression)
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
- Multi-target
original_source: Other
year: '2023'
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://doi.org/10.5281/zenodo.7669644
- https://doi.org/10.1038/s41597-023-02135-w
- https://pmc.ncbi.nlm.nih.gov/articles/PMC10220078/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the open release (JRC, VITO, NILU and partners) of 85 AirSensEUR low-cost sensor systems in Antwerp, Oslo and Zagreb, April 2020 to April 2021, with raw sensor signals and co-located reference measurements at minute resolution: the calibration task of the Chemotronix record on a documented network.
- Source: Yatkin, Gerboles, Van Poppel, Schneider, Peters, Matheeussen et al., Zenodo, doi 10.5281/zenodo.7669644 (v2.0.0, 2023-02-24, CC BY 4.0, `senseurcity_data_v02.zip`, 4.9 GB); data paper Van Poppel et al., "SensEURCity: A multi-city air quality dataset collected for 2020/2021 using open low-cost sensor systems", Scientific Data 10:322 (2023) (read on Europe PMC, PMC10220078). As published: "85 sensor systems were deployed throughout a year in three European cities, namely Antwerp (Belgium)-34 systems, Oslo (Norway)-34 systems, and Zagreb (Croatia)-17 systems", with sensors for "NO, NO2, O3, CO, PM2.5, PM10, PM1, CO2 and meteorological parameters"; "two co-location campaigns in different seasons at an Air Quality Monitoring Station (AQMS) in each city and a deployment at various locations"; reference CO and CO2 only in Antwerp, during the co-locations; data files per system and site with minute data, and metadata on sites, deployments and instruments.
- Use case: a network operator calibrates each low-cost unit against the reference monitor during co-location and applies the model to the unit's later readings. The paper's aims are "to explore and evaluate calibration approaches" and to "develop and evaluate drift of calibration models". Fit direct. Regime temporal (calibrate on the first co-location, test on the second), with the sensor system as a group if new units are the target.
- Siblings and duplicates: `air_quality_prediction_from_low_cost_iot_devices` (`TBD -> 2nd Tier`, three Chemotronix prototypes, CO2), `airqo_low_cost_air_quality_monitor_calibration_challenge` (`TBD -> Yes`, PM2.5 in Kampala) and `epa_purpleair_pm25_correction` (`TBD -> Yes`, daily PM2.5 across the US) are the same kind of task from other sources; no record of SensEURCity. External collections: none known.
- Better data: found as better data for `air_quality_prediction_from_low_cost_iot_devices` (the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: the Scientific Data paper; the JRC code used for its quality filtering (github.com/ec-jrc/airsenseur-calibration).
- Metric: none found (the data paper defines no evaluation; its full text was searched), so the fallback `rmse` on the reference concentration (MET-1, MET-8); inputs none.
- Risks for /add-dataset: one pollutant per dataset (NO2, O3 and PM in all cities, CO2 and CO only in Antwerp), or several targets (`Multi-target`). Per-minute rows are strongly autocorrelated, so aggregate them and split by time (`Time-series (Regression)`). The reference values of other gases are no feature unless a deployed unit would have them. The 4.9 GB zip of per-system files needs sensor and reference joined by time and site.
- Priority: gap 0 (environmental science, regression and temporal are not thin), use case + (the paper names calibration and drift evaluation; the AirSensEUR is built "as a supplemental tool for reference air quality monitoring"), source + (Scientific Data paper, Zenodo, JRC), shape + (85 units, a year of data, grouped and temporal), risk - (the stream framing and the joins).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `air_quality_prediction_from_low_cost_iot_devices`.
- as published: 85 AirSensEUR systems (Antwerp 34, Oslo 33-34, Zagreb 17), April 2020 to April 2021, one row per minute; raw signals for NO, NO2, O3, CO, CO2, PM1/2.5/10 plus temperature, humidity, pressure; two ...; target: reference concentration at the co-location station (CO2 reference only in Antwerp, installed for the two co-locations; NO2, O3, CO, PM in all cities); access: open.
- Why: same task as the Chemotronix record: map a low-cost device's raw sensor reading to the reference meter's concentration at the same time, including CO2
- Adds: dozens of devices in three cities instead of three prototypes, a documented release with metadata, deployment dates and instrument details, open CC BY 4.0; also other gases
