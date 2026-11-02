---
unique_name: tunisian_fraud_detection_challenge
name: Tunisian Fraud Detection Challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2019'
domain: finance
required_split:
- '?'
problem_type: Regression
source_links:
- https://zindi.africa/competitions/tunisian-fraud-detection
- https://zindi.africa/competitions/supcom-tunisian-fraud-detection-challenge
source_row: 1015
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 3: taxpayer-year data of the Tunisian Ministry of Finance, the target the tax liability an inspection adjusted; a real audit-selection task, scored by RMSE.
- Source: Zindi "Tunisian Fraud Detection Challenge" (`tunisian-fraud-detection`, opened 2019-09-20, a knowledge competition, 1,529 participants), data "provided by the Tunisian Ministry of Finance includes variables about tax analysis, taxpayer inspection, and VAT returns"; "a subset of over 25,000 samples aggregated by year", "an anonymized dataset containing a large number of numeric variables"; "The "TARGET" column ... equals the amount of the tax liability that the taxpayer has to adjust". Files: Train.csv (9,679,520 B), Test.csv, VariableDescription.csv ("Full list of variables and their explanations"). The linked `supcom-tunisian-fraud-detection-challenge` (2020-09, a private Sup'Com student hackathon, 71 participants, "over 21,295 samples") ships files of the same sizes: the same data, a later re-run. Both read through the Zindi API.
- Use case: the tax authority, after returns are filed, picks taxpayers to inspect ("a supervised machine learning technique that detects potential fraudulent taxpayers will increase the operational efficiency of the tax supervision process"); fit direct when the features are return-time data, approximate if inspection-stage variables are in. Regime: grouped by taxpayer or temporal by year, to be read from the columns (rows are "aggregated by year"; whether an id or year ships is not checked); `required_split` left at `?`.
- Siblings and duplicates: none among `curation/records/` (grep tax, Tunisia: `fraud_detection_in_electricity_and_gas_consumption` is STEG electricity fraud, another task; `indabax_tunisia_2023` another hackathon). External collections: none found.
- Papers and pages: the two Zindi pages; no paper found.
- Metric: RMSE on the adjustment amount (Zindi Evaluation page: "The evaluation metric for this challenge is Root Mean Square Error"), the competition's choice (MET-4); inputs none. The old `problem_type` `Binary Classification` (AI-filled) is contradicted by the source: the target is an amount, so `Regression`.
- Risks for /add-dataset: "taxpayer inspection" variables may be recorded during or after the inspection that set the target (USE-4, LEAK checks); anonymized numeric columns, so the meaning rests on VariableDescription.csv; a likely zero-inflated, heavy-tailed target (check MET-3 for the scale); taxpayer-years of one taxpayer across folds if no id ships (SPLIT checks); download needs a Zindi login and the rules forbid redistribution (no criterion, EV-4).
- Priority: gap 0 (finance not thin; grouped would be thin but the regime is not confirmed), use case + (actor and decision named by the source), source + (a ministry's data with a variable description file), shape + (about 25,000 rows, many columns), risk - (inspection-stage variables, unknown grouping).

A Zindi competition to detect tax fraud using the Tunisian Ministry of Finance's data — a real-world, high-value tabular classification task with a clear binary target (fraud / not fraud). This maps well to the benchmark criteria: unique original source, predictive task, representative tabular ML. A human must verify dataset size after cleaning, the exact feature schema, whether a temporal or grouped (per-taxpayer) split is required, and class balance / potential leakage, and confirm data accessibility from Zindi.

---

Detect tax fraud using the Ministry of Finance of Tunisia's data
