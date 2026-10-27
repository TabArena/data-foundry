---
unique_name: outsmarting_outbreaks_challenge
name: outsmarting-outbreaks-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Needs extensive data wrangling
- TBD
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2024'
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://zindi.africa/competitions/outsmarting-outbreaks-challenge/data
- https://zindi.africa/competitions/outsmarting-outbreaks-challenge
source_row: 870
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: monthly counts of waterborne-disease cases per hospital in a Tanzanian region, a panel that may be forecasting (SEL-10 / SEL-11, TP-10 decides).
- Source: Zindi "SUA Outsmarting Outbreaks Challenge" (Sokoine University of Agriculture with IRCAI and AWS, 2024-12-06 to 2025-01-31, 816 participants, CC-BY-SA 4.0); as published: Train.csv (2019-2022) and Test.csv (2023) with ID per hospital, month, year and disease (typhoid, amoebiasis, diarrhoea, schistosomiasis, intestinal worms), target `Target`, plus waste_management.csv, toilets.csv, water_sources.csv (locations, masked) and a climate table 2019-2024 (ASDI); rows not checked (Train.csv 4.1 MB).
- Use case: the source says the model "will enable governments and health organisations to implement timely, targeted interventions and optimize resource allocation"; actor a district health office, moment before a month, decision where to send supplies; fit approximate (the climate table covers the test months, which a planner would not have ahead of time); regime temporal: "The train set contains information from 2019 to 2022, the test set is 2023".
- Siblings and duplicates: none found in `curation/records/` (grep outbreak, waterborne); external collections: none known.
- Papers and pages: the competition pages (Description, Data, Evaluation) read through the Zindi API; no paper; winners @Yisakberhanu, @AhmedElFazouani, @JuliusFx (solutions not read).
- Metric: Mean Absolute Error, Zindi Evaluation page ("The evaluation metric for this competition is Mean Absolute Error"); deliberate (a leaderboard metric, MET-4); inputs none beyond the target.
- Risks for /add-dataset: the task is "to predict the total number of disease outbreaks per hospital for each month of 2023" from 2019-2022, the future values of a count series per hospital: run TP-10 (a model on the features against each hospital's naive profile) before anything else, else `Time-series (Forecasting)` (SEL-10); top solutions may use lagged targets (not checked); the location tables join by masked coordinates (heavy joins); climate for the target month is a future value at a monthly prediction point (LEAK); the counts are skewed with many zeros.
- Priority: gap 0 (medical, temporal not thin), use case + (the source names the actors and the decision), source 0 (a competition page, no codebook beyond VariableDefinitions.txt), shape + (a hospital-month panel with side tables), risk - (forecasting-like panel, joins).

A Zindi disease-outbreak challenge provided as multiple to-be-joined tables with temporal structure. Depending on framing it could be a legitimate temporal-split predictive task (e.g. predicting case counts/outbreak risk for a location-period) or a forecasting task, which would be out of scope. It needs substantial wrangling to join tables and define a fixed predictive target. Suggest TBD -> 2nd Tier; a human must verify whether the task is a fixed predictive classification/regression with a temporal split versus a forecasting-over-horizon problem, and assess size after joins.
