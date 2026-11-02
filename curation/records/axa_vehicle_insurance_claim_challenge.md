---
unique_name: axa_vehicle_insurance_claim_challenge
name: AXA Vehicle Insurance Claim Challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2020'
domain: insurance
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/umojahack-nigeria
source_row: 1020
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 3: the first release (2020) of the claim-in-3-months task that the AutoInland challenge re-ran; real insurer, thin domain.
- Source: Zindi, "UmojaHack Nigeria: AXA Vehicle Insurance Claim Challenge", one-day private hackathon of 2020-11-28 (UmojaHack Africa with AXA Mansard, Data Science Nigeria, H2O.ai, AI6), open to university students in Nigeria; as published: "~17,000 policies sold by AXA for car insurance. Information on the car type, make, customer age and start of policy are in the data"; Train.csv, Test.csv, VariableDescription.csv. Columns and class balance not checked (Zindi login; the hackathon was restricted to its participants, so access is a question for the curator).
- Use case: AXA Mansard, at the customer's first transaction, predicts a claim "within 3 months from their first transaction" to "anticipate future demands in terms of claims request volume" and "streamline financial planning" (Zindi Description); fit direct; regime temporal (policy start dates ship), to confirm on the dates.
- Siblings and duplicates: `autoinland_vehicle_insurance_claim_challenge` (2021) has the same Description and Data Description word for word with "AutoInland" for "AXA Mansard" and ~12,000 policies: probably a pseudonymised subset of this release. If the rows match, this record is the first publication (PROV-8) and the AutoInland one (with its four Zindi re-runs) the `Duplicate`; confirm on the data first (PROV-5). External collections: none found.
- Papers and pages: no paper; https://zindi.africa/competitions/umojahack-nigeria (read through the Zindi API).
- Metric: F1 on hard 0/1 labels, the Zindi Evaluation page ("The error metric for this competition is the F1 score"); deliberate (leaderboard, MET-4); threshold not fixed by the source (MET-6, MET-7); inputs none.
- Risks for /add-dataset: data access (private hackathon); Test.csv lacks "the target-related columns", so check for columns known only after the claim window (LEAK rules); several policies per customer (grouping); the duplicate question with AutoInland.
- Priority: gap + (insurance is thin), use case + (the source names the insurer and the decision), source 0 (competition page and a variable list only), shape + (~17k rows, mixed types with dates), risk - (overlap with AutoInland, possible leak columns, restricted access).


Zindi AXA/UmojaHack challenge: predict whether a client will submit a vehicle-insurance claim in the next 3 months, a clear real-world binary classification with a defined target. Insurance claim prediction on policyholder records is representative tabular ML. The future-window target suggests a temporal split. A human must verify cleaned size, class imbalance (rare claims), absence of target leakage, and whether this overlaps/duplicates the AutoInland claim challenge.

---

predict if a client will submit a vehicle insurance claim in the next 3 months
