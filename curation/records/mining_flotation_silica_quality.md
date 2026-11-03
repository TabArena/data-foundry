---
unique_name: mining_flotation_silica_quality
name: Quality Prediction in a Mining Process (iron ore froth flotation plant)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: Kaggle
year: '2017'
domain: industry & manufacturing
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/edumagalhaes/quality-prediction-in-a-mining-process
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: a real flotation plant's process log with the lab's hourly silica in the concentrate, a soft-sensor task whose uploader names the engineers and their corrective action; about 4,000 usable hours from an unnamed plant, with held or interpolated feed values and a two-week gap.
- Source: Kaggle upload by Eduardo Magalhães Oliveira (`edumagalhaes`), "Quality Prediction in a Mining Process" (dataset id 6294, CC0; public by early January 2018, when the first notebook on it ran; the current file is of 2019-09-25), "Real industrial flotation process (mining plant)", the plant not named (PROV-2). As published: one CSV, `MiningProcess_Flotation_Plant_Database.csv` (184 MB), 737,453 rows x 24 columns (the run's count), March to September 2017; "Some columns were sampled every 20 second. Others were sampled on a hourly base"; columns 2-3 the feed's % iron and % silica, 4-8 reagent and pulp flows, 9-22 levels and air flows of the flotation columns, the last two the lab's % iron and % silica in the concentrate: "Target is to predict the last column" (Kaggle description).
- Use case: the uploader's: "if we can predict how much silica (impurity) is in the ore concentrate, we can help the engineers, giving them early information to take actions" and "take corrective actions in advance" (Kaggle, Context); actor the process engineer, moment each hour before the lab result, decision the reagent and air settings; fit direct for a soft sensor of the current hour. Regime temporal: one plant, one six-month stream, and the 20-second rows of an hour share one lab value, so a random row split puts the same target in train and test.
- Siblings and duplicates: `sulfur_debutanizer` (`TBD -> Yes`, markers `Wrong Domain / Source Modality`, `Time-series (Regression)`; Fortuna et al.'s soft-sensor data) is the same kind of task on another plant, no duplicate (PROV-4); no other record names this upload (searched by slug, name and "flotation"). External collections: none among the records; the web was not searched (search budget used up).
- Better data: found as a related task next to `sulfur_debutanizer`; no further search this run.
- Papers and pages: the Kaggle page, which lists Pu, Szmigiel & Apel, "Purities prediction in a manufacturing froth flotation plant: the deep learning techniques", Neural Comput Appl 2020 (https://doi.org/10.1007/s00521-020-04773-2, paywalled, not read), a ResearchGate paper and a master thesis on DiVA (diva2:1386720, server unreachable); public notebooks read: mkoerner1/iron-mining-production-prediction, ginsaputra/gangue-forecast-in-flotation-concentrate, aditya100/quality-prediction-in-iron-ore.
- Metric: none on the Kaggle page (a dataset without an evaluation); notebooks report MAE and RMSE, and the ginsaputra notebook cites the owner calling "MAE and RMSE of 1±0.2" satisfactory (the comment itself not read): no single deliberate metric, so the fallback `rmse` (MET-1, MET-8); inputs none.
- Risks for /add-dataset: the unit: one row per hour, since the target is hourly (about 4,400 hours less the 318 missing from 2017-03-16 to 2017-03-29, per the ginsaputra notebook), not 180 copies of each label (USE-5, SPLIT-23); `% Iron Concentrate` comes from the same lab analysis as the target and goes (USE-3; the uploader asks for predictions "without using % Iron Concentrate column"); the feed's % iron and % silica stay constant for weeks (May 13 to June 13, ginsaputra) and the mkoerner1 notebook finds interpolated stretches (PROV-13: mark or drop, never fill); a one-hour-ahead framing invites the lagged target, so check TP-10 against a persistence baseline; the timestamp has hourly resolution, so the order within an hour rests on the file order (SPLIT-22).
- Priority: gap 0 (industry & manufacturing, regression, temporal not thin), use case + (the uploader names the engineers and the corrective action), source 0 (an identified uploader's description, the plant unnamed, no paper of the publisher), shape + (about 4,000 hourly rows, 21 process features, a time axis), risk - (hourly targets repeated over 20-second rows, held or interpolated feed values, a co-measured output): 2.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `sulfur_debutanizer`.
- as published: 737,453 rows x 24 columns (MiningProcess_Flotation_Plant_Database.csv, 184 MB): March to September 2017, process variables every 20 s, feed quality and lab results hourly (about 4,000 hourly lab ...; target: % silica (impurity) in the iron ore concentrate, measured hourly by the lab; access: open.
- Why: A soft-sensor task like debutanizer/SRU (infer a lab-measured quality variable from process measurements known earlier), with a clear actor and decision; widely used in soft-sensor papers
- Adds: A larger, newer real plant dataset for the soft-sensor use case (thousands of lab measurements vs 2,394 debutanizer rows), with timestamps for a temporal split. Risks: first publication is the Kaggle upload of an unnamed plant (provenance to check); % Iron Concentrate is a co-measured lab output and must be dropped; ...
