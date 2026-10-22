---
unique_name: autoinland_vehicle_insurance_claim_challenge
name: autoinland-vehicle-insurance-claim-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2021'
domain: insurance
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/autoinland-vehicle-insurance-claim-challenge
- https://zindi.africa/competitions/the-smart-cube-hackathon/data
- https://zindi.africa/competitions/women-in-data-2022/data
- https://zindi.africa/competitions/indabax-ghana-autoinland-vehicle-insurance-claim
- https://zindi.africa/competitions/vehicle-insurance-claim-hackathon
source_row: 908
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 3: a real claim-in-3-months task from an insurer, thin domain, but likely the same data as the AXA Mansard hackathon of 2020.
- Source: Zindi, "AutoInland Vehicle Insurance Claim Challenge", 2021-03-26 to 2021-06-27 (AutoInland, "an Insurance company in west Africa with a focus on Auto Insurance", Nigeria); as published: "~12,000 policies sold by AutoInland for car insurance. Information on the car type, make, customer age and start of policy are in the data"; Train.csv (target), Test.csv, VariableDefinitions.csv, NigerianStateNames.csv (lookup). Columns and the class balance not checked (the data needs a Zindi login).
- Use case: the insurer, at the customer's first transaction, flags who will "submit a claim within 3 months from their first transaction", to "anticipate future demands in terms of claims request volume" and "better manage their resources" (Zindi Description); fit direct; regime temporal (policy start dates ship; a later cohort of policies is what the model meets), to confirm on the dates.
- Siblings and duplicates: `axa_vehicle_insurance_claim_challenge` (UmojaHack Nigeria, 2020-11-28: the Description and Data Description are word for word the same with "AXA Mansard" for "AutoInland", ~17,000 policies) is probably the first publication of the same data, and AutoInland a pseudonymised, smaller re-release; PROV-4/PROV-5 need a row and column comparison of both releases before one is marked `Duplicate` (keep the one that is first and complete, PROV-8). Re-runs listed in `source_links` are Zindi children of this competition (the API's `parent`): the-smart-cube-hackathon (2022), women-in-data-2022, indabax-ghana-autoinland-vehicle-insurance-claim (2021), vehicle-insurance-claim-hackathon (2021), all with the same text and files: copies, not separate datasets. Other insurance records (allstate_claims_severity, fremtpl2, porto_seguro, monthly_insurance_claim_prediction_challenge) are different data. External collections: none found.
- Papers and pages: no paper; the competition page (https://zindi.africa/competitions/autoinland-vehicle-insurance-claim-challenge, read through the Zindi API); top solutions not read.
- Metric: F1 on hard 0/1 labels, the Zindi Evaluation page ("The error metric for this competition is the F1 score"); deliberate (a leaderboard metric, MET-4); the threshold is the participant's, not fixed by the source (MET-6, MET-7: decide at /add-dataset between F1 with a threshold rule and the fallback `roc_auc`); inputs none.
- Risks for /add-dataset: Test.csv lacks "the target-related columns", so check Train.csv for claim-side columns and for `Policy End Date`-like fields known only later (LEAK rules); the policy-to-customer relation (several policies per customer would need grouping); NigerianStateNames is a lookup join; the duplicate question above (PROV-4).
- Priority: gap + (insurance is thin), use case + (the source names the insurer and the planning decision), source 0 (a competition page and a variable list, no codebook or paper), shape + (~12k rows, mixed categorical, numeric and date columns), risk - (likely duplicate of the AXA release, leak check on target-related columns).


Zindi AutoInland challenge: predict whether a vehicle-insurance customer will submit a claim within the next 3 months, a clear real-world binary classification task with a defined target. Insurance claim prediction on policyholder records is a representative tabular ML problem. Because the target is a future-window event, a temporal split is likely the right protocol. A human must verify the cleaned row count, class balance (claims are typically rare), and that features are policyholder/vehicle attributes rather than leakage from the claim itself.

---

predict if a customer will submit a claim within next 3 months
