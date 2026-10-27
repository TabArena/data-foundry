---
unique_name: the_zimnat_insurance_assurance_challenge
name: The Zimnat Insurance Assurance Challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Needs extensive data wrangling
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
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://zindi.africa/competitions/the-zimnat-insurance-assurance-challenge
source_row: 1025
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 3: a real insurer's policy-lapse task with a clear temporal structure; the release is several tables and the public labels are lapse years 2017-2019, so the benchmark target has to be rebuilt (for example lapse in 2019 among policies active at the end of 2018).
- Source: Zindi #ZindiWeekendz hackathon with Zimnat (Zimbabwe), 22-24 May 2020 (https://zindi.africa/competitions/the-zimnat-insurance-assurance-challenge, read through Zindi's page API); as published: "51,685 life assurance policies", client_data.csv (location, branch, agent code, age), policy_data.csv ("multiple rows for each Policy ID since policies can cover more than one person"), payment_history.csv ("up to the end of 2018"), train.csv (Lapse = 1 and the year for lapses in 2017, 2018 or 2019; '?' for policies still active at the end of 2019, which form the test set for 2020); "Numerical quantities have been transformed, and many categories have been assigned unique IDs".
- Use case: the insurer scores active policies for lapse so "churn prediction can be used to offer targeted support and tailored services to certain customers vulnerable to churning" (Description); fit direct for a yearly scoring run. Regime temporal: lapses by year, payment history cut at a date.
- Siblings and duplicates: `zimnat_insurance_recommendation_challenge` (another Zimnat task, a product recommendation, `No` (AI)); `zimnat_loan_default_predictio` (another task). Not a duplicate. External collections: none found.
- Papers and pages: no paper; the winner interview is linked from the Description.
- Metric: log loss on the lapse probability ("The evaluation metric for this challenge is Log Loss", Evaluation tab); a leaderboard metric (MET-4); inputs none.
- Risks for /add-dataset: joins across three tables with many-to-one policy rows; the 2020 labels are not public, so the target and cut-off must be built from the lapse years with features only up to the cut-off (payment history ends 2018, which fits a 2019 target); transformed values; a lapse year is known only after it.
- Priority: gap + (insurance thin), use case + (named by the source), source 0 (a competition page), shape + (51k policies, mixed tables, temporal), risk - (joins and a rebuilt target).

A Zindi challenge (Zimnat, Zimbabwe) to predict when an insurance policy will lapse. Predicting policy lapse from customer/policy attributes is a standard tabular insurance classification (or possibly time-to-event) task that fits the benchmark scope. The 'when' framing may imply a temporal/duration target, so a human must confirm whether it is a clean binary lapse classification or a survival/temporal task, plus the modality, size, and split. Provisionally a plausible Yes.

---

predict when an insurance policy will lapse in Zimbabwe
