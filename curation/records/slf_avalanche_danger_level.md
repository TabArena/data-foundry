---
unique_name: slf_avalanche_danger_level
name: Weather, snowpack and danger ratings data for automated avalanche danger level predictions (SLF, Switzerland)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
original_source: Other
year: '2022'
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.16904/envidat.330
- https://doi.org/10.5194/nhess-22-2031-2022
- https://renkulab.io/gitlab/deapsnow/predictions_avalanche_danger-level_switzerland
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: SLF's published station-day table (IMIS weather and SNOWPACK-derived snowpack features, winters 1997/98 to 2019/20) with the bulletin's dry-snow danger level in four classes, an NHESS task with a test on later winters and an operational decision-support use; the label is a human forecast, and the snowpack features are model output driven by the measured weather.
- Source: Pérez-Guillén, Techel, Hendrick, Volpi, van Herwijnen, Olevski, Obozinski, Pérez-Cruz, Schweizer (WSL Institute for Snow and Avalanche Research SLF and the Swiss Data Science Center), "Weather, snowpack and danger ratings data for automated avalanche danger level predictions", EnviDat 2022 (https://doi.org/10.16904/envidat.330; WSL Data Policy; data_rf1_forecast.csv 186 MB and data_rf2_tidy.csv 17 MB, read through the EnviDat API), with the paper "Data-driven automated predictions of the avalanche danger level for dry-snow conditions in Switzerland", NHESS 22:2031-2056 (2022, https://doi.org/10.5194/nhess-22-2031-2022); code on RenkuLab. As published: D_forecast 256,398 station-days after filtering (500,545 before), D_tidy 25,541 with quality-checked labels; per IMIS station "the meteorological variables (resampled 24-hour averages) and the profile variables extracted from the simulated profiles" (EnviDat), 47 features after correlation pruning and 30 selected; target the danger level 1 Low to 4 High (5 merged into 4; about 41% Moderate, 36% Considerable, 2% High).
- Use case: the avalanche forecaster sets the danger level of the bulletin, with the models as "decision support tools for avalanche forecasters" (Sec. 6.6); both ran in real time in winter 2020/21 (Sec. 6.5); fit direct (the model reproduces the published level); regime temporal: training winters 1997/98 to 2017/18, test 2018/19 and 2019/20, tuning on blocks of consecutive winters (SPLIT-3), with the station as a group to weigh.
- Siblings and duplicates: none (grep: avalanche, snowpack, danger level). External collections: none found.
- Better data: no new search; found through the gap scout for multiclass tasks.
- Papers and pages: Pérez-Guillén et al. 2022 (NHESS full text: Sec. 3 data, Sec. 4.1 model selection, Sec. 6.5 operational testing); the EnviDat record.
- Metric: macro-F1, the paper's deliberate selection criterion (Sec. 4.1: "we used cross-validation maximizing the macro-F1 score"; accuracy is the abstract's headline, per-class precision, recall and F1 reported too); a threshold metric on hard labels, and the forecaster publishes one level, so `f1_macro` is the source's metric if the curator accepts the hard decision (MET-5, MET-6), otherwise the fallback `log_loss` (MET-8). Inputs: none.
- Risks for /add-dataset: the SNOWPACK features are simulated from the measured weather, the field's standard input (rows and target are real, so not SEL-16; say so in the notes); the 24-hour windows against the time the forecast is issued (the bulletin is issued the evening before, from memory: the prediction point to check in the CSV, LEAK); the label's noise (the paper compares its accuracy with the agreement rate between forecast and nowcast assessments, "estimated to be 76 %"); which set ships (D_forecast or D_tidy); class 4 at about 2%; serial correlation of station-days (split by winter).
- Priority: gap + (multiclass is thin; natural hazards are absent), use case + (the paper names the forecaster's decision, tested in operation), source + (SLF data on EnviDat with an NHESS paper), shape + (256,398 station-days, about 50 features, 23 winters, stations), risk - (a noisy human label; the window timing to check).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the gap scout for multiclass tasks.
- as published: 256,398 station-days (D_forecast, after filtering; 25,541 in the quality-checked D_tidy) at the IMIS automatic weather stations (about 120 snow stations), winters 1997/98 to 2019/20; 24-hour, 3-day ...; target: dry-snow avalanche danger level from the official bulletin at the station's location: 1 Low, 2 Moderate, 3 Considerable, 4 High (4 and 5 merged); access: open.
- Why: Real station measurements and a human-set danger level with an operational use and a paper-defined temporal test (2018/19, 2019/20); the snow-profile variables come from the SNOWPACK model driven by the measured weather, the field's standard input (rows and target are real, so not SEL-16 simulated data, but say so in ...
- Adds: A 4-class ordinal task with a temporal (23 winters) and grouped (station, region) structure; natural hazards and geophysics are absent
