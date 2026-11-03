---
unique_name: thailand_road_accident_register_2019_2022
name: Thailand road accidents 2019-2022 (Ministry of Transport) / thailand-road-accident-2019-2022 (Kaggle)
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
- Non-IID (Temporal)
original_source: GOV Website
domain: social science
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- '# First publication: Ministry of Transport (TRAMS), one record file per year, 2019-2026'
- https://datagov.mot.go.th/dataset/roadaccident
- '# Kaggle copy of 2019-2022, translated to English (thaweewatboy, 2023)'
- https://www.kaggle.com/datasets/thaweewatboy/thailand-road-accident-2019-2022
type_adapter_id: curation-record-v1
---

## Comments

**AI-FILLED, UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from the source pages, papers and data previews named below (measured where the notes say so). A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-20):** `TBD -> Yes`, priority 3: the Ministry of Transport's crash register, with road,
vehicle, cause, weather and coordinates for each crash, is the richer version of the 2015 table, and deaths per crash
are a two-regime target.
- Source: Ministry of Transport, Office of the Permanent Secretary (ICT Centre), dataset `roadaccident` on
  datagov.mot.go.th, "accidents on the ministry's road network: highways, rural roads and expressways" (translated),
  from its TRAMS reporting system; record-level data, one CSV and XLSX per year from 2019 (posted 12 October 2020) to
  2026, Open Data Common licence. The Kaggle upload (thaweewatboy, August 2023, CC0) is an English translation of
  2019-2022; its data card links a Ministry of Tourism and Sports page by mistake. As published on Kaggle: 81,735
  crashes x 18 columns (time, report time, province, agency, route, vehicle type, presumed cause, accident type,
  vehicles, deaths, injuries, weather, coordinates, road and slope). Measured 2026-10-20: the Kaggle 2019 rows match
  the ministry's 2019 file (19,194 crashes, 3,223 deaths); the 2025 file has 38 columns (serious and minor injuries,
  vehicles by type, pedestrians).
- Target and zeros: `number_of_fatalities` per crash, 0 in 87.6% of 2019-2022 and in 89.9% of 2025. The zero is
  observed: a recorded crash without a recorded death. Whether anyone dies is one mechanism (severity), how many
  another (vehicles, occupants), as in the 2015 sibling. Whether deaths after the report are counted is not stated;
  the report follows the crash by a median of 49 days.
- Use case: for example a highway agency ranking sites for treatment, or a dispatcher triaging a reported crash; the
  source names no actor (its objective: "to serve the public"), so the fit is approximate. Regime temporal: every
  crash is dated and a model serves later crashes (SPLIT-6); routes repeat (SPLIT-13).
- Siblings and duplicates: `thailand_road_accident_fatalities_2015` (DDPM, Ministry of Interior, 2015; 2nd Tier for
  six coarse covariates) is another agency and year, not a duplicate. `nhtsa_crss_crash_severity` and
  `chicago_traffic_crashes` (TBD -> Yes, AI drafts) hold the same crash-severity task. `us_accidents` is `No`
  (Lennart: "Just survey data for insights, not a predictive task"; its Severity is a delay code): the curator should
  confirm that a police-style crash register supports a prediction task. No external collection found.
- Papers and pages: no paper on the register found; the Kaggle copy has no discussions or notebooks.
- Risks for /add-dataset: build from the ministry's files and pin a snapshot, which also sets the year (PROV-8,
  PROV-9); the yearly schemas differ. Drop `number_of_injuries` and the report time when predicting deaths (LEAK-10).
  `presumed_cause` and `accident_type` are the reporting officer's reading, known at the report but not at the first
  call (USE-3). Untuned LightGBM, 2019-2021 -> 2022: AUC 0.83 for any death (0.81 without cause and accident type),
  Poisson D^2 0.26 (the 2015 table: 0.71 and 0.12).
- Priority: gap 0, use case 0 (no actor named), source + (the ministry's own release, no codebook), shape + (81,735
  crashes, 14 mixed features, dated).

CC (2026-10-30, Andrej): `Yes`, priority 5 (the AI screening had `TBD -> Yes`, priority 3; zero-inflated screening
review page).

**Assessment (AI, 2026-11-01):** added as `datasets/_dev/tabarena-v0pt2/thailand_road_accident_register_2019_2022/` by /add-dataset with the full review panel; the open questions are in its `REVIEW.md`. Recommend shipping after the panel's text changes (made). The task is read as the severity part of road-network screening (the Highway Safety Manual's relative severity index), which its issue 3 asks you to accept as what sets it apart from glioma_grading_clinical_and_mutation_features. Corrections to the screening above: a paper on the register exists (EECSS 2024, now the metric's context); the measured ROC AUC for any death is 0.840/0.833, not 0.83/0.81. `Two-Regime Zeros` removed under your definition of 2026-10-30: a count model given the features predicts 89.2% zeros against 89.0% observed, so the zero is the first step of the count, as for how_much_did_it_rain_ii (a CC restores it). Priority 3 (your 5 of 2026-10-30 was set before the measurements): gap + (social science), use case 0 (fit approximate), source +, shape +, risk - (issue 3 is a validity call that can retire it).

CC (2026-11-03, Andrej): don't ship (review page verdict): issue 3 (C) of thailand_road_accident_register_2019_2022, `No` (`No Good Target / Scientific Discovery`), as glioma_grading_clinical_and_mutation_features: once a crash is in the register its deaths are in the same record, so the model predicts a count already on file, and the severity-screen reading was not accepted ("We do C"). Issues 1 and 2 and the metric are moot ("Doesn't matter since we don't ship"). The folder leaves the working copy; the definition is in commit 902011b3.

## Reference

Ministry of Transport, Office of the Permanent Secretary, ICT Centre. Accidents on the road network of the Ministry of Transport (TRAMS), yearly files 2019-2026, Open Data Common. https://datagov.mot.go.th/dataset/roadaccident
Kaggle copy of 2019-2022: thaweewatboy (2023), Thailand Road Accident [2019-2022], CC0.

Lead: zero-inflated screening review, policy question 6 (curator's go, Andrej, 2026-10-20); sibling of `thailand_road_accident_fatalities_2015`.
