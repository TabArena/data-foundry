---
unique_name: bosch_engine_test_bench_calibration
name: 'Bosch PEngine: static test-bench measurements of a gasoline engine prototype (engine1, engine2)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- AI-Filled (Verify)
original_source: Github
domain: industry & manufacturing
problem_type: Regression
source_links:
- https://github.com/boschresearch/Bosch-Engine-Datasets/tree/master/pengines
- https://arxiv.org/abs/2402.14402
- https://github.com/cenyou/TransferSafeSequentialLearning
- https://arxiv.org/abs/2203.14849
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: two standardised test-bench tables of one gasoline engine under two conditions (796 and 786 operating points, 4 inputs, 7 outputs), published by Bosch Research for safe active and transfer learning of Gaussian processes; small, low-dimensional, the units hidden.
- Source: Bosch Research, github.com/boschresearch/Bosch-Engine-Datasets (repository created 2022-02-10, CC BY-SA 4.0), folder `pengines`: "measurements of the same system under different conditions ... Each column is standardized to zero-mean and unit-variance" (README); used in Li, Rakitsch and Zimmer, "Safe Active Learning for Multi-Output Gaussian Processes", AISTATS 2022 (arXiv 2203.14849), and Li, Duennbier, Toussaint, Rakitsch and Zimmer, "Global Safe Sequential Learning via Efficient Knowledge Transfer", TMLR 2025 (arXiv 2402.14402). As published (xlsx files previewed 2026-10-31): engine1_normalized.xlsx with 796 rows and engine2_normalized.xlsx with 786 rows, each an index, the inputs engine_speed, engine_load, intake_valve_opening, air_fuel_ratio and the outputs specific_fuel_consumption, temperature_exhaust_manifold, temperature_in_catalyst, engine_roughness_v, engine_roughness_s, HC, NOx; a sheet of quantiles; a suggested safety constraint file. The repository's gengine1 and gengine2 are dynamic 10 Hz trajectories, another task and not this record.
- Use case: a calibration engineer models an engine output (roughness, emissions, temperatures) over the operating point to set calibration maps inside safe limits; the source's task is to learn that model from few safe measurements (active learning), not to predict for new rows; fit approximate; regime IID over operating points of one condition, or engine1 to engine2 as the source's transfer design (two groups only).
- Siblings and duplicates: `bosch_production_line_performance` is another Bosch dataset (a Kaggle competition, another task); no other record (grep bosch, pengine). External collections: none found.
- Better data: from the curator's Zotero collection (item 198); no further search this round.
- Papers and pages: the two papers above (abstracts read; their dataset sections not read).
- Metric: none found for a prediction task (the README names none; the papers' abstracts score the safe-learning procedures); so the fallback `rmse` on the chosen output; inputs none.
- Risks for /add-dataset: every column was standardised over the file (LEAK-30, weak; the physical units cannot be recovered); pick one output (the README "mainly" uses engine_roughness_s) and drop the other outputs, measured at the same time (LEAK-10); about 800 rows and 4 inputs from a designed sweep of one engine may be close to a smooth function (TP-4, to probe).
- Priority: gap 0 (industry & manufacturing, regression not thin), use case 0, source +, shape - (about 800 rows, 4 inputs), risk - (standardised, units hidden).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 198: "boschresearch/Bosch-Engine-Datasets".
- as published: two xlsx files of one engine under different conditions; 4 inputs (engine speed, relative cylinder air charge, intake valve opening / camshaft phaser position, air-fuel ratio) and 7 outputs ...; target: one measured output per definition, e.g. engine roughness (std of indicated cylinder pressure) or HC / NOx emission (regression); access: open.
- Why: real measured test-bench data with a clear engineering decision; the inputs are the operating point set before measuring; open licence (CC BY-SA 4.0)
- Adds: an automotive calibration surrogate task like airfoil_self_noise or concrete_compressive_strength; two conditions give a possible transfer split. Small and low-dimensional (4 features), values standardised (units hidden), two of the inputs recorded with noise: low priority
