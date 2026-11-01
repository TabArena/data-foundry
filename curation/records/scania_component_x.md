---
unique_name: scania_component_x
name: 'SCANIA Component X dataset: time-to-failure class of a truck engine component'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
decision_markers:
- Anonymized
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: Other
year: '2024'
domain: industry & manufacturing
required_split:
- Random (IID)
problem_type: Multiclass Classification
source_links:
- https://doi.org/10.5878/jvb5-d390
- https://doi.org/10.1038/s41597-025-04802-6
- https://researchdata.se/catalogue/dataset/2024-34/2
- https://arxiv.org/abs/2401.15199
- https://arxiv.org/html/2401.15199v2
- https://doi.org/10.5878/bnh5-ka77
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: Scania's real fleet data for an engine component, about 34,000 trucks with operational readouts and repair records, released for the IDA 2024 Industrial Challenge with a five-class time-to-failure label and a cost matrix set by the company's experts.
- Source: Kharazian, Lindgren, Magnússon, Steinert, Andersson Reyna, "SCANIA Component X dataset: a real-world multivariate time series dataset for predictive maintenance", Scientific Data 12:493 (2025) (https://doi.org/10.1038/s41597-025-04802-6; arXiv 2401.15199 v2, read 2026-10-31). Data on the Swedish National Data Service (publisher Scania CV AB, CC BY 4.0, version 3 of 2025-04-09, DOI 10.5878/bnh5-ka77; first version DOI 10.5878/jvb5-d390). As published: 23,550 training vehicles (1,122,452 readouts), 5,046 validation (196,227) and 5,045 test (198,140); per readout 14 anonymized operational variables (six histograms and eight counters, about 105 columns), and 8 categorical specifications per vehicle; `train_tte.csv` with the length of study and `in_study_repair`; `validation_labels.csv` and `test_labels.csv` with the class of one randomly selected last readout per vehicle: more than 48, 48-24, 24-12, 12-6 and 6-0 time steps before failure (classes 0-4; test 4,903 / 26 / 15 / 41 / 60).
- Use case: workshop mechanics and fleet managers decide whether to call a truck in for Component X now, given its latest readout. The cost table, set by the company's experts, weighs a missed failure (200-500) against a needless check (7-10). Fit direct. Regime IID by vehicle, one row per vehicle at its last readout (the time steps are relative, so no calendar split).
- Siblings and duplicates: `aps_failure` (`Yes`, Scania's APS data of the IDA 2016 challenge) shares the publisher but not the component or the task (PROV-7). `ai4i_2020_predictive_maintenance_dataset` (`TBD -> 2nd Tier`, synthetic) and `backblaze_hard_drive_failure` (`TBD -> Yes`) are other maintenance tasks. External collections: none known.
- Better data: found as better data for `ai4i_2020_predictive_maintenance_dataset` and `aps_failure`, and by the gap scout for multiclass tasks (the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: the Scientific Data paper; the SND record with `documentation/Scania_Component_X.pdf` and `2024_IDA_challenge_v2.pdf` (not read).
- Metric: the challenge's total cost over the paper's 5 x 5 table (Table 1), set by the company: `cost_matrix` as the mean cost per vehicle (MET-4, MET-7); inputs none.
- Risks for /add-dataset: the training vehicles carry a time-to-event, not a class, so the label has to be derived per vehicle the way the organisers did (a random last readout and its distance to the repair); a vehicle without a repair in the study is class 0 only when more than 48 steps of observation remain after the readout. The readout history must be cut at that readout and summarised (the counters are cumulative). The paper says "Repair frequencies and readout frequencies may have been modified" and that operational data was scaled: owner-side disclosure control, a note under PROV-3 unless a test measures damage. The variables are anonymized (`Anonymized`, as for `aps_failure`). Classes 1-4 hold 15-60 vehicles in the test file, so every fold holds them only if the files are pooled or the training vehicles get labels (TP-5, MET-2).
- Priority: gap + (multiclass thin), use case + (the company names the decision and the costs), source + (Scientific Data paper, SND DOI), shape + (about 34,000 vehicles, counters, histograms and specifications), risk - (the label framing from series, the owner's perturbation, few vehicles in the late classes).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `ai4i_2020_predictive_maintenance_dataset`, `aps_failure`; the gap scout for multiclass tasks.
- as published: more than 33,000 trucks: train 23,550 vehicles with time-to-event and repair flag, validation 5,046 and test about 5,045 vehicles with a class for the last readout (test: 198,140 readouts); 14 ...; target: class of the last readout: failure of Component X in more than 48, 48-24, 24-12, 12-6 or 6-0 time steps (classes 0-4); access: open, open (CC BY 4.0), open (SND download; dataset licence to confirm on the SND page).
- Why: Real fleet data from a manufacturer, published for predictive maintenance with a multiclass label and a cost function from the company (MET-6/MET-7 candidate). Sibling of the accepted aps_failure (Scania, another component and task, PROV-7). Each vehicle's readout history must be summarised to one row per vehicle at ...
- Adds: An industrial fault-timing multiclass task with a grouped (vehicle) and temporal structure, histogram features and categorical specifications | real fleet data with repair-record labels instead of a generator (PROV-3), about 34k units and 1.5M readouts, a documented publisher and DOI; also the successor of Scania's ...
