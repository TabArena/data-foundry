---
unique_name: monthly_insurance_claim_prediction_challenge
name: Monthly Insurance Claim Prediction Challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- TBD
- Time-series (Forecasting)
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2022'
domain: insurance
required_split:
- '?'
problem_type: Regression
source_links:
- https://zindi.africa/competitions/umojahack-africa-2022-intermediate-challenge
source_row: 1010
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: Zimnat's claim values per client, "per month for a whole year", from a two-day UmojaHack; a real insurer's cost task in a thin domain, but what one row is (a claim, or a client-month) and whether the test months lie after the training months is not stated.
- Source: Zindi hackathon "UmojaHack Africa 2022: Monthly Insurance Claim Prediction Challenge (INTERMEDIATE)", 19-20 March 2022, data from Zimnat (Zimbabwe) (https://zindi.africa/competitions/umojahack-africa-2022-intermediate-challenge, read through Zindi's page API); as published: train.csv, test.csv, policies.csv ("extra information regarding the policies"), DataDictionary.csv, a starter notebook; "The target column is the claim column which indicates the value of a claim. Policy terms are annual and as a result a policy is renewed every 12 months from the date of inception"; submissions keyed by `claim_id`. Rows and columns not counted (login).
- Use case: "Zimnat Insurance wants to predict the value of future claims per client, in order to better forecast annual costs ... help Zimnat in being better prepared to address claims" (Description); the actor and the aim are named, the decision (reserving, budgeting) only implied; fit approximate until the row unit is known. Regime likely temporal (claims over months); grouped by client if a client has several rows.
- Siblings and duplicates: other Zimnat and insurance Zindi records (`autoinland_vehicle_insurance_claim_challenge`, `axa_vehicle_insurance_claim_challenge`; the 2020 "Zimnat Insurance Assurance Challenge" is a different task, policy lapse); the UmojaHack 2022 siblings `african_snake_antivenom_binding_challenge`, `faulty_air_quality_sensor_challenge` are other tasks. No duplicate found. External collections: none found.
- Papers and pages: the Zindi winners' post: the winners "concatenated the two different data sets" (train and policies), built "date-time features", log-transformed the labels, used LightGBM and CatBoost.
- Metric: MAE on the claim value ("The error metric for this competition is the Mean Absolute Error", Evaluation tab); MET-4; inputs none.
- Risks for /add-dataset: the row unit and the test design from the data dictionary (a panel of client-months is forecasting-like: SEL-10 against SEL-11 and TP-10); the policies join (one to many?); many zero claims (a hurdle shape); dates after the prediction point.
- Markers: `Time-series (Forecasting)` kept as a concern ("per month for a whole year"); not a fail from the page, which Zindi tags "Prediction".
- Priority: gap + (insurance has 4 accepted), use case 0 (actor named, fit unclear), source 0 (a hackathon page with a data dictionary, no paper), shape 0 (size not counted; mixed types and a policy table), risk - (unclear row unit and target timing, a join).

A Zindi UmojaHack 2022 challenge to predict how much will be claimed per month. Predicting monthly claim amounts could be a fixed regression task on policy/customer features, but 'per month' phrasing raises the possibility of a temporal forecasting framing, which would be out of scope. The record lacks data details. Because it is plausibly a valid insurance regression task but may be forecasting, this is TBD -> 2nd Tier. A human must open the competition to confirm whether it is a fixed predictive task vs horizon forecasting, the target, size, and split.

---

predict how much will be claimed per month
