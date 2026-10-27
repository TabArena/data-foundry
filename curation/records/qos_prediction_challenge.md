---
unique_name: qos_prediction_challenge
name: qos-prediction-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2022'
domain: technology & internet
required_split:
- '?'
problem_type: Regression
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/qos-prediction-challenge/data
- https://ieee-dataport.org/open-access/berlin-v2x
- https://arxiv.org/abs/2212.10343
source_row: 897
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 3: predict the achieved LTE downlink throughput of a driving car from physical-layer, cell, GPS and traffic/weather information; a real measurement campaign, but a stream of readings with scheduler fields that may nearly determine the target.
- Source: first published as Berlin V2X (Hernangómez et al., "Berlin V2X: A Machine Learning Dataset from Multiple Vehicles and Radio Access Technologies", arXiv:2212.10343, December 2022, IEEE VTC2023-Spring; data on IEEE DataPort, doi:10.21227/8cj7-q373, open access, Parquet files for cellular and sidelink; up to four cars over three days in Berlin, two operators). The Zindi QoS Prediction Challenge (ITU AI/ML in 5G Challenge, 2023-06-02 to 2023-07-15, 261 participants) uses it: "leverage the Berlin V2X dataset to predict QoS ... features from the primary and secondary cells of two commercial LTE mobile network operators ... alongside GPS and context information to predict the achieved throughput in the downlink". As published on Zindi: Train.csv (10.4 MB), Test.csv (5.2 MB), itu-ffs.zip, VariableDefinitions.csv.
- Use case: a network or V2X application anticipates the QoS of a link to manage radio resources "proactively" (the page); fit approximate, because the features are measured at the same moment as the throughput, not before it; regime not settled: grouped by drive, car or operator ("multi-domain setup (i.e., across operators, devices and/or link directions)") or temporal along the drives; `required_split` stays `?`.
- Siblings and duplicates: `row_1040` (the ITU challenge archive that lists this challenge, "QoS Prediction Challenge by ITU AIML in 5G Challenge" and "Multi-environment automotive QoS prediction"); `5g_energy_consumption` (another ITU challenge, `Yes`) is unrelated data. External collections: none found.
- Papers and pages: https://arxiv.org/abs/2212.10343, https://ieee-dataport.org/open-access/berlin-v2x, https://zindi.africa/competitions/qos-prediction-challenge.
- Metric: `rmse` (Zindi Evaluation: "The evaluation metric for this competition is Root Mean Squared Error"), a leaderboard metric (MET-4); inputs none. The target is in bit/s (sample values 16,500,000), a scale question (MET-3).
- Risks for /add-dataset: build from Berlin V2X (the first publication, PROV-8) or from the Zindi files; scheduler fields (MCS, assigned resource blocks, carrier aggregation) may make throughput near-deterministic (TP-4 check); per-second readings along drives (SPLIT-7, `Time-series (Regression)` question). The old `Data Quality Issue` marker stood for a "no-distribution license"; a licence is no reason for a marker (EV-4), so it is dropped; the DataPort page states open access.
- Priority: gap 0, use case 0, source +, shape +, risk - (stream, scheduler fields).

Zindi competition to predict quality-of-service for a wireless vehicle network, a plausible real-world tabular regression task. The record explicitly notes a 'no-distribution license', which is a hard blocker for redistribution in a public benchmark and the main reason this is not a clear Yes. A human must confirm the licensing terms (whether redistribution/use is actually permitted), the exact target and units, dataset size, and whether the split should be random or temporal (vehicular networks may have temporal structure).

---

predict quality-of-service for a wireless vehicle network

no-distribution license
