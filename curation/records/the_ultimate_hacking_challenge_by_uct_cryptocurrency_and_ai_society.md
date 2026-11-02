---
unique_name: the_ultimate_hacking_challenge_by_uct_cryptocurrency_and_ai_society
name: The Ultimate Hacking Challenge by UCT Cryptocurrency and AI Society
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2019'
domain: insurance
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://zindi.africa/competitions/uct-datathon-the-ultimate-hacking-challenge/data
- '# first publication: Zindi Insurance Prediction Challenge (DSN Bootcamp 2019); this record''s link is a 2020 private re-run'
- https://zindi.africa/competitions/insurance-prediction-challenge
source_row: 1016
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 2: a building-insurance claim classification (at least one claim over the insured period), first published as Zindi's 2019 DSN "Insurance Prediction Challenge"; this record is a later private re-run of it, and the data's origin is undocumented.
- Source: first publication Zindi "Insurance Prediction Challenge", "A learning competition designed for DSN Bootcamp 2019", from 19 Nov 2019 (https://zindi.africa/competitions/insurance-prediction-challenge); the same brief re-hosted as the DSN AI+ Unilorin hackathon (June 2020, https://zindi.africa/competitions/insurance-prediction) and this UCT Cryptocurrency and AI Society hackathon (19 Sept 2020, https://zindi.africa/competitions/uct-datathon-the-ultimate-hacking-challenge, private, 25 participants); all read through Zindi's page API. As published: train_data.csv, test_data.csv, VariableDescription.csv; target `Claim` "1 if the building has at least a claim over the insured period"; "The model will be based on the building characteristics". Rows and columns not counted (login).
- Use case: "Olusola Insurance Company offers a building insurance policy ... You have been appointed as the Lead Data Analyst to build a predictive model" (Description): an insurer prices or underwrites a building policy; a role-play scenario, no named real insurer; fit approximate. Regime: likely temporal if a year-of-observation column ships (check), else IID; the record's `Random (IID)` is kept for now.
- Siblings and duplicates: no record for the 2019 original or the Unilorin re-host; the record should point to the 2019 competition (rename or note). Other building/vehicle-claim records: `autoinland_vehicle_insurance_claim_challenge`, `axa_vehicle_insurance_claim_challenge`, `monthly_insurance_claim_prediction_challenge` (different data). External collections: none found.
- Papers and pages: no paper; Zindi pages only.
- Metric: ROC AUC ("The evaluation metric for this competition is the Area Under the ROC curve (AUC)", Evaluation tab of all three hosts); a leaderboard metric (MET-4); inputs none.
- Risks for /add-dataset: provenance: who supplied the data to DSN is not stated (PROV-2); an insured-period column may be partly known only after the period (LEAK); the year of observation decides the split.
- Priority: gap + (insurance thin), use case 0 (a scenario, not a named actor), source 0 (no codebook or publisher), shape + (building characteristics of mixed types), risk - (undocumented origin, several re-hosts).

A UCT student datathon on Zindi whose stated task is to predict whether a building will have an insurance claim. This is a clear binary classification problem on what is most likely tabular building/insurance features, which fits the benchmark scope. The record lacks field-level details, so a human should confirm the modality is tabular, the dataset size after cleaning is adequate, and the appropriate split regime. Provisionally a plausible Yes.

---

predict if a building will have an insurance claim
