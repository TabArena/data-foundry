---
unique_name: infrared_thermography_temperature
name: Infrared Thermography Temperature
checked_by:
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: Disagreement
priority: 4
tags:
- New IID
collections:
- New (BeyondArena)
original_source: Website
year: '2023'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.13026/9ay4-2c37
- https://physionet.org/content/face-oral-temp-data/1.0.0/
v2_path: datasets/_dev/tabarena-v0pt2/infrared_thermography_temperature/dataset.py
source_row: 665
type_adapter_id: curation-record-v1
---

## Comments

Two targets. Need to carefully check which features make sense to include in the predictive task. Some might be unreasonable. Some features were extracted from infrared images, but those are not given

Discussion: I think this is grouped, subject ID is not unique but counts up with -1,-2,...

**Assessment (AI, 2026-10-07):** Added as a regression of `aveOralM` (oral temperature, monitor mode, the reference of both papers); `aveOralF`, the same readings in fast mode, is dropped as a second measurement of the target. Data: PhysioNet's FLIR_groups1and2.csv, 1,018 subjects (CC0). SubjectID is yymmdd-n and unique per row, so each subject is one row; holding out whole measurement days changes R² by less than 0.004, so the split stays IID, with temporal and day-grouped splits as alternatives. The 17 subjects without a complete round-1 image keep their later image. Random forest R² 0.707 (RMSE 0.274 against 0.509 for the mean), and an additive model beats the source's one-feature calibration on 28 of 30 splits. Is the modality marker an exception here?

**Assessment (AI, 2026-10-20):** priority 4 for the review of the added dataset: gap -, use case +, source +, shape +, no known risk. Well-documented FDA fever-screening regression with a direct use case; the open question is mainly the image-derived modality marker.

**Assessment (AI, 2026-10-20):** review panel (full): ship after changes; the 17 subjects without a complete round-1 image are dropped (their next image follows the oral thermometer; USE-7), 1,018 to 1,001 rows, which supersedes "the 17 keep their later image" above; the use case is rewritten to the clinic triage station of the source (fit direct), the split reason rests on the new person (IID; temporal open as a variant) and the "exception" note now gives the SEL-15 reason (scope open for the curator). The 2026-10-07 measurement (SubjectID unique) supersedes "subject ID is not unique"; the reference is Sensors 22(1):215, 2022. Priority 4: gap - (no thin domain, problem type or regime), use case + (the source's calibration, fit direct), source + (PhysioNet and two papers), shape + (1,001 people, 35 features, categorical), risk 0 (no leak left, recommended to ship).

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: Cosmetics.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source rmse — root-mean-square difference A_rms (with clinical bias and its SD) (Wang et al. 2022, Sensors 22(1):215, Sec. 2.5-2.6 (PMC8749858)).

CC (2026-10-21, Lennart): split: "IID is okay for now, but document the discussion. I think here we want to approximate and learn a function that is independent of time (like the measurements should be the same between two different days given other inputs are the same) -> no real signal across time". IID kept; the measured year-to-year shift (a first-year calibration over-predicts the second year by 0.06-0.09 °C; past-only training +0.5% to +6.7% RMSE in 6 expanding windows) is recorded in the definition, temporal a candidate variant (SPLIT-31).

CC (2026-10-21, Lennart): scope: "Yes, go with (a)". The facial temperatures read through the thermal camera are measurements (SEL-15), not image descriptors (SEL-13); SEL-15 is amended: a physical quantity measured through an imaging device at defined sites (a temperature, a volume, an angle), used by the field as the instrument's reading, is a measurement, with satimage and wilt as the counter-cases. The marker `Wrong Domain / Source Modality` is removed with this decision.

## Reference

Infrared Thermography for Measuring Elevated Body Temperature: Clinical Accuracy, Calibration, and Evaluation
By Quanzeng Wang, Yangling Zhou, Pejman Ghassemi, David McBride, J. Casamento, T. Pfefer. 2021

Published in Italian National Conference on Sensors
