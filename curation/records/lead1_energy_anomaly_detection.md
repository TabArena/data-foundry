---
unique_name: lead1_energy_anomaly_detection
name: 'LEAD1.0: A Large-scale Annotated Dataset for Energy Anomaly Detection in Commercial Buildings'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: Github
year: '2022'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.1145/3538637.3539761
- https://arxiv.org/abs/2203.17256
- https://github.com/samy101/lead-dataset
- https://www.kaggle.com/competitions/energy-anomaly-detection
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: hand-annotated anomaly flags on real hourly meter readings of ASHRAE GEPIII buildings, with a Kaggle competition scored by ROC AUC; but the public labels cover 200 buildings, not the paper's 1,413 meters, and the label was drawn with the whole year in view.
- Source: Gulati and Arjunan, "LEAD1.0: A Large-scale Annotated Dataset for Energy Anomaly Detection in Commercial Buildings", arXiv 2203.17256 (2022-03-30; ACM e-Energy 2022 by its DOI 10.1145/3538637.3539761), data and annotation tool on GitHub samy101/lead-dataset. Paper Sec. 2: "we had 199,640 anomalous instances present across 12,060,910 data points logged by 1,413 energy meters", annotated in a web tool, "approximately 100 man-hours". Public release: the Kaggle competition "Large-scale Energy Anomaly Detection (LEAD)" (2022-04-27 to 2022-07-31, Community, 62 teams): train.csv with `building_id`, `timestamp`, `meter_reading`, `anomaly` for 200 buildings, test.csv for 206 other buildings without public labels, and train/test_features.csv (the ASHRAE winners' features, 582 and 608 MB). The GitHub `data/lead1.0-small.zip` holds one CSV of 57,680,722 bytes, the size of Kaggle's train.csv (zip directory read). "A final complete version with annotated meter readings from all buildings will be released later" (Kaggle acknowledgements); not found.
- Use case: the paper: detection techniques "identify anomalous events of energy consumption and report them to building managers for further action" (Sec. 1); fit approximate: the annotators marked a "disturbance in this pattern" and days far from "its nearby days" on a plot of the year (Sec. 2), so a label can rest on readings after the hour it flags, while an operator flags with the past only. Regime grouped by building (the competition tests on unseen buildings; SPLIT-19), with time inside each building.
- Siblings and duplicates: `smart_meter_electricity_consumption_dataset` (Lennart `No`, AHDS and `Missing source information`: "looks very fake"); `ashrae_great_energy_predictor_iii` (`Yes`, DF: Yes): the same 2016 electricity readings with the reading as the target, a shared source with a distinct task (PROV-7). External collections: none found.
- Better data: found as better data for `smart_meter_electricity_consumption_dataset`; no further search this round.
- Papers and pages: the arXiv paper (read); the Kaggle pages (data description, evaluation, rules, read through the API); the ASHRAE GEPIII competition and its winners' feature pipeline.
- Metric: Kaggle's "Area Under Receiver Operating Characteristic Curve (AUC-ROC)" over the test readings (Evaluation page), a competition's choice (MET-4), so `roc_auc`; the paper reported precision, recall and F1 on 24-hour windows (Sec. 3), several metrics on another unit. Inputs none.
- Risks for /add-dataset: a point anomaly in a series: the features are the series itself (lags, rolling profiles, the building's usual week), built per building from the past only, or the label's hindsight is accepted and noted (LEAK; `Time-series (Classification)` to weigh, SEL-12); about 1.7% anomalies; missing hours; only the 200 training buildings have public labels (about 1.75M readings), so ask the authors for the full release; read the features files for columns computed over the whole series before using them.
- Priority: gap 0 (environmental science, binary and grouped are not thin), use case 0 (an actor named, fit approximate), source + (paper, repository, competition), shape + (about 1.75M readings of 200 buildings, grouped and temporal), risk - (series features and hindsight labels).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `smart_meter_electricity_consumption_dataset`.
- as published: 1,413 electricity meters x 8,784 hourly readings (2016), 12,060,910 logged readings, 199,640 labelled anomalous (about 1.7%); the Kaggle competition uses 200 buildings for training and 206 for testing; target: Anomaly flag per hourly meter reading, annotated by hand with a web tool (point and collective anomalies, about 100 person-hours); access: open.
- Why: Same task as the Kaggle record: an anomaly label on smart-meter readings with weather and past consumption as features; there the label comes from an Isolation Forest on generated data, here people labelled real meters
- Adds: Real readings and human labels, 12 million points against a sourceless generated table. Meter data come from ASHRAE GEPIII (record ashrae_great_energy_predictor_iii, a different target), so its own record. Time-series anomaly task: lag features and a split by building or by time are needed. No licence in the GitHub ...
