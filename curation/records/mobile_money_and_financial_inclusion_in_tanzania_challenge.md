---
unique_name: mobile_money_and_financial_inclusion_in_tanzania_challenge
name: mobile-money-and-financial-inclusion-in-tanzania-challenge
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
domain: finance
required_split:
- '?'
problem_type: Multiclass Classification
source_links:
- https://zindi.africa/competitions/mobile-money-and-financial-inclusion-in-tanzania-challenge/data
source_row: 925
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 2: FinScope Tanzania 2017 respondents classified into four mutually exclusive groups of financial-service use, with a targeting use the page states; survey data, a risk the curator weighed on a FinScope sibling.
- Source: Zindi competition "Mobile Money and Financial Inclusion in Tanzania Challenge", 26 Mar to 1 Jul 2019, sponsored by HDIF, Data Lab Tanzania and Esri (https://zindi.africa/competitions/mobile-money-and-financial-inclusion-in-tanzania-challenge, read through Zindi's page API); the data "was extracted from the FSDT Finscope 2017 survey and prepared specifically for this challenge": "demographic information and what financial services are used by approximately 10,000 individuals across Tanzania" (training.csv, test.csv, Variable_Codebook.docx), plus FSDT's Financial Access Map (GPS of cash outlets) as an optional layer. Target: `no_financial_services`, `other_only`, `mm_only`, `mm_plus`. Rows and columns not counted (the download needs a Zindi login).
- Use case: "This model can help mobile money providers target new clients and markets across Tanzania more effectively, and also help financial services providers cross-sell other financial services (savings, credit, and insurance)" (Description); fit approximate: the features come from the interview that also records the usage, so this is a look-alike targeting model on demographics, not one a provider feeds with its own data (SEL-7 to weigh: the respondent knows the label, the provider does not). Regime IID (one cross-sectional survey); a grouping by region or enumeration area is to check.
- Siblings and duplicates: `dataorg_financial_health_prediction_challenge` (FinScope MSME surveys, `No`; CC 2026-10-22: "Too risky a dataset: we have no information on the target ... and it is survey data"); here the page defines the target. `indabax_tanzania_mobile_banking_prediction_challenge`, `ix_mobile_banking_prediction_challenge`, `financial_inclusion_in_africa_for_botswana` (other Zindi financial-inclusion surveys): check that none reuses FinScope Tanzania 2017. External collections: none found.
- Papers and pages: FSDT's FinScope Tanzania 2017 survey (not read); the Zindi winners' post linked from the page; no paper on this task.
- Metric: multiclass log loss on the four class probabilities ("The evaluation metric for this challenge is the Log Loss", Evaluation tab; the Rules page's "accuracy score" is Zindi boilerplate); MET-4; inputs none.
- Risks for /add-dataset: the codebook decides which columns describe the usage itself (questions on savings, credit, insurance or mobile money would leak the class, LEAK rules); the four classes are a rule over usage flags (SEL-5: drop the flags if they ship); survey weights; the outlet map is a spatial join.
- Priority: gap 0 (finance has 17 accepted), use case 0 (actor and decision named, fit approximate), source + (FSDT's FinScope survey, a codebook ships), shape + (about 10,000 respondents, mixed demographic features), risk - (survey data, usage questions as leaks, the curator's FinScope precedent).

A Zindi competition on mobile money and financial inclusion in Tanzania, with no description in the record. Financial-inclusion challenges are typically tabular classification (e.g., predicting account ownership or mobile-money usage from survey/demographic features), which would be in scope, but the exact target is unknown. There is too little info to reject, so this is a TBD. A human must open the competition to confirm the target, problem type, size, and split regime.
