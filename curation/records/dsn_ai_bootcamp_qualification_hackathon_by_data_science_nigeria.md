---
unique_name: dsn_ai_bootcamp_qualification_hackathon_by_data_science_nigeria
name: DSN AI Bootcamp Qualification Hackathon by Data Science Nigeria
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2020'
domain: finance
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/dsn-ai-bootcamp-qualification-hackathon/data
source_row: 1017
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 2: a credit-default classification at application with 80,000 rows and documented credit-bureau-style fields, but the lender is a scenario name and some fields describe post-default collections.
- Source: Zindi "DSN AI Bootcamp Qualification Hackathon", Data Science Nigeria, from 9 September 2020 (https://zindi.africa/competitions/dsn-ai-bootcamp-qualification-hackathon); as published: "a structure dataset pull from the Kowope Mart's database", train 56,000 and test 24,000 rows; `Applicant_ID`, `form_field1` to `form_field50` (risk scores, default severity, credit limits and utilisation, income, property value, tenures, missed payments, a financial stress index, `form_field47` the product applied for, Charge or Lending; `form_field48` and `form_field49` "Undefined Variable"), and `default_status`.
- Use case: Kowope Mart and its partner bank want "a system that profiles customers who are worthy of the card with minimum if not zero risk of defaulting": the card issuer decides at application; fit direct if the fields are known at application; regime IID (one row per applicant, no dates).
- Siblings and duplicates: `microsoft_x_data_science_nigeria_2024_ai_bootcamp_qualification_hackathon`, `dsn_free_ai_classes_in_every_city_2025` and `dsn_trail_ooo` are other DSN hackathons (not compared by files here); no other record carries Kowope Mart. External collections: none found.
- Papers and pages: competition page only; no paper.
- Metric: ROC AUC, Zindi Evaluation page ("The error metric is Area Under the Curve"); a leaderboard choice (MET-4); inputs none.
- Risks for /add-dataset: `form_field11` ("The amount of dues collected post-default") and the default-severity fields may describe the outcome itself (LEAK, check against the target); whether Kowope Mart and DSBank are real or a teaching scenario over another lender's data (PROV-2); the data description also says "You must predict growth_stage for the corresponding images", a copy-paste slip.
- Priority: gap 0 (finance, binary, IID not thin), use case + (card issuer at application, named by the source), source 0 (page only, provenance of the rows unclear), shape + (80,000 rows, 50 columns), risk - (post-default fields, unclear provenance): 2.

Zindi DSN AI Bootcamp qualification hackathon: predict which customers will default on a loan, using a structured table pulled from Kowope Mart's database. This is a clear real-world binary credit-default classification task, a strong fit for tabular ML in the finance domain. The split is plausibly IID unless an account/customer or application-date field forces a grouped/temporal protocol. A human must download the data to confirm row count, the exact target column, and whether a temporal/grouped split is warranted; data access on Zindi may require competition registration.

---

Predict customers who will default on a loan

data is a structured dataset pulled from the Kowope Mart's database
