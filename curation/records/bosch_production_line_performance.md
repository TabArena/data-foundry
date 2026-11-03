---
unique_name: bosch_production_line_performance
name: Bosch Production Line Performance (Kaggle competition)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Anonymized
tags:
- AI-Filled (Verify)
- Many features
- Non-IID (Temporal)
original_source: Kaggle
year: '2016'
domain: industry & manufacturing
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/competitions/bosch-production-line-performance
- https://arxiv.org/abs/2606.26337
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: Bosch's own line data, 1.18M parts with the end-of-line quality result, a real manufacturing decision at scale; the features are anonymised and the forum knows a row-order leak.
- Source: Robert Bosch GmbH, Kaggle featured competition "Bosch Production Line Performance" (launched 2016-08-17, closed 2016-11-11, 1,370 teams, USD 30,000 prize), the first publication of the data (PROV-8). As published: train_numeric, train_categorical and train_date, and the same three for the test parts, joined by `Id`; per the run's assessment 1,183,747 training parts with 968 numeric, 2,140 categorical and 1,156 date columns (not recounted), named only by line, station and feature number (e.g. L3_S36_F3939), dates in a time unit of Bosch's choosing; target `Response` (the part fails quality control), about 0.58% positive; test labels never released. Access: Kaggle registration and the competition rules.
- Use case: a quality engineer flags parts likely to fail the quality control from the measurements taken along the line, to pull or inspect them early (the competition's subtitle: "Reduce manufacturing failures"); fit direct. Regime temporal: parts pass the line in time and the date columns order them; a model would be refit on past parts and used on the next ones (SPLIT-6).
- Siblings and duplicates: `mercedes_benz_greener_manufacturing` (`Yes`, `Anonymized`, test-bench time), `cylinder_bands` (`TBD -> 2nd Tier`, Outdated, 540 print jobs of 1995), `bosch_engine_test_bench_calibration` (this run: other Bosch data, an engine calibration task, not the same source). No duplicate (grep for bosch). External collections: none found; used in EMA-FS (arXiv 2606.26337: "extremely sparse data (Bosch, >90% missing)").
- Better data: from the run's search, found as better data for `cylinder_bands`, a related task next to `mercedes_benz_greener_manufacturing`, and in the curator's Zotero collection (item 220); no further search this round.
- Papers and pages: the competition pages; EMA-FS (above). Top solutions are claims (PROV-18) and were not read in this pass.
- Metric: Matthews correlation coefficient, the competition's leaderboard metric (Kaggle API `evaluationMetric`), a deliberate choice on hard labels (MET-4): methods pick their threshold on the training side; inputs none.
- Risks for /add-dataset: `Anonymized` (what a measurement is, and whether a station's test is part of the final quality check, cannot be told: LEAK-32, LEAK-38, USE-4); the forum's "magic" features from part `Id` order and neighbouring parts' start times, a row-order leak to keep out of the features and to check against the split (LEAK, SPLIT); only the training parts carry labels; 4,264 sparse columns and 1.18M rows need the row cap (`Many features`).
- Priority: gap 0 (industry & manufacturing, binary and temporal are not thin), use case + (the organiser names the decision), source + (the manufacturer's line data, a competition), shape + (1.18M parts with numeric, categorical and date columns), risk - (anonymised columns and a known row-order leak).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `cylinder_bands`; a related task next to `mercedes_benz_greener_manufacturing`; the curator's Zotero collection, item 220: "EMA-FS: Accelerating GBDT Training via Gain-Informed Feature Screening".
- as published: train 1,183,747 parts with 968 numeric, 2,140 categorical and 1,156 timestamp features (measurements by line and station); test the same size, without public labels; about 0.58% failures; target: Response: whether a part fails quality control; access: registration, registration (Kaggle, competition rules).
- Why: the same task family as cylinder_bands (predict a production defect from the process measurements of a job or part, so the plant can act before the defect costs time), as cylinder_bands' process-delay task is today; a real, documented industrial source | a real manufacturing test-line task in the same domain as the ...
- Adds: over a million parts from a 2016 production line against 540 print jobs from 1995 (Outdated, Tiny Data); timestamps per station, which allow a temporal split; risks: features are anonymised (Anonymized), only the train labels are public, and the scored metric was MCC | a second, much larger manufacturing quality task ...
