---
unique_name: ix_mobile_banking_prediction_challenge
name: ix-mobile-banking-prediction-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2021'
domain: finance
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/ix-mobile-banking-prediction-challenge/data
- https://zindi.africa/competitions/ix-mobile-banking-prediction-challenge
source_row: 907
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: a large survey table with an unnamed source and a survey answer as the target; the curator should decide whether "uses mobile or internet banking" is a target anyone predicts.
- Source: Zindi "iX Mobile Banking Prediction Challenge", sponsor iXperience, 17 May to 13 June 2021 (https://zindi.africa/competitions/ix-mobile-banking-prediction-challenge); as published: "~100 000" train and "~45 000" test "survey responses from around Africa and the world", Train.csv / Test.csv / VariableDefinitions.csv, survey columns FQ1-FQ37 coded "1 - Yes, 2 - No, 3 - Don't Know 4 - refused to answer", binary target (uses mobile or internet banking). The survey behind it is not named on the page (a Global Findex-style multi-country survey is a guess, not confirmed).
- Use case: the page says "Banks and financial service providers value knowing what habits their clients follow ... tailor products and services"; a provider would not hold these survey answers for its clients, so the fit is approximate at best; regime IID (one row per respondent, no time), though a country column, if present, may call for a grouped check.
- Siblings and duplicates: `indabax_tanzania_mobile_banking_prediction_challenge` (June 2021) ships the same files (Train.csv 11,296,855 bytes, Test.csv 4,748,025 bytes in both Zindi APIs) and the same text, so it is the later duplicate and this record is the first publication; the FinScope "Financial Inclusion in Africa" records (`financial_inclusion_in_africa_for_botswana`, `mobile_money_and_financial_inclusion_in_tanzania_challenge`) are other surveys with other targets (has a bank account), not duplicates (PROV-7). External collections: none found.
- Papers and pages: no paper; competition page only; no public top solution found.
- Metric: ROC AUC, Zindi Evaluation page ("The error metric for this competition is the Area Under the Curve (AUC). Do not set thresholds"); a deliberate leaderboard choice (MET-4); inputs none (MET-1, MET-5, MET-6).
- Risks for /add-dataset: the target is a respondent's own answer in the same interview as the features (SEL-7 / SEL-3 doubt: who predicts it?); FQ columns may hold other account- or payment-usage answers that nearly give the target away (LEAK); the survey's origin, year and weights need tracing (PROV-1, PROV-2).
- Priority: gap 0 (finance, binary, IID not thin), use case 0 (approximate, written for a sponsor), source 0 (survey unnamed), shape + (about 145k rows, many categorical answers), risk - (survey-answer target, likely leaking FQ columns): 1.

Based on the name this is a mobile-banking adoption/usage prediction challenge on Zindi, most likely a financial-inclusion binary classification on demographic/survey tabular features, but the record has no comments. Such tasks are genuine real-world tabular prediction problems, so missing info alone is not a rejection reason. A human must confirm the actual target, check size after cleaning, and verify it does not duplicate the IndabaX Tanzania mobile-banking or broader financial-inclusion datasets.
