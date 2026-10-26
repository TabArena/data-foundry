---
unique_name: dont_overfit_by_uofk_fmsi
name: dont-overfit-by-uofk-fmsi
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/dont-overfit-by-uofk-fmsi/data
source_row: 971
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`No Good Target / Scientific Discovery`, SEL-7): the target is a respondent's own answer in the World Bank's Global Findex 2017 survey ("if you were in an emergency and needed to make a payment within the next month, can you?"), asked in the same interview as the feature answers Q1-Q28; nobody predicts what the respondent states, and no provider holds these answers for its clients.
- Source: first published as Zindi "UmojaHack Africa 2021 #3: Financial Resilience Challenge (BEGINNER)", 27-28 March 2021 (https://zindi.africa/competitions/umojahack-africa-2021-3-financial-health-challenge-beginner); this record's "Don't Overfit! By UofK FMSI" (from 9 March 2023, https://zindi.africa/competitions/dont-overfit-by-uofk-fmsi) is a re-run with the same files (Train.csv 15,557,583 bytes, Test.csv 6,576,155, VariableDefinitions.csv 2,017, the same R starter notebook). The rows are Global Findex 2017 (Demirgüç-Kunt et al. 2018, World Bank, WLD_2017_FINDEX_v02_M), cited on the page.
- As published: "~100 000" train and "~45 000" test "survey responses from around Africa and the world"; columns Q1-Q28 coded "1 - Yes, 2 - No, 3 - Don't Know 4 - refused to answer"; binary target.
- Use case claimed by the page: "help financial services providers including insurance companies and banks tailor their services"; a provider does not hold Findex answers, so the fit is a look back at survey answers (SEL-3, SEL-7; precedents cdc_diabetes_health_indicators, and the curator's `No` on the FinScope survey `dataorg_financial_health_prediction_challenge`, 2026-10-22).
- The old markers `Too Small` and `AHDS` are refuted: real World Bank survey answers, about 145,000 rows; the "Don't Overfit" name is the hackathon's title, not the Kaggle challenge.
- Siblings: `ix_mobile_banking_prediction_challenge` (another Findex-style survey answer as target) was screened today as `TBD -> 2nd Tier`, priority 1, with the same SEL-7 doubt; the two should be decided alike. No record carries the UmojaHack 2021 #3 original.
- Metric: ROC AUC (Zindi: "Do not set thresholds ... Zindi will need the raw probabilities").
- If the reject-checker refutes it: `TBD -> 2nd Tier`, priority 1 (gap 0, use case 0, source + (World Bank Findex), shape +, risk - (survey-answer target)).
- Reject check (AI, 2026-10-22): stands. The target is a Global Findex 2017 respondent's own answer in the same interview: "if you were in an emergency and needed to make a payment within the next month, can you?" (https://zindi.africa/competitions/dont-overfit-by-uofk-fmsi). That is SEL-7 word for word (a label the respondent already knows). Same files as the UmojaHack 2021 #3 parent (Train 15,557,583 / Test 6,576,155 bytes, same in the API), so no other record would be lost. Consistency: ix_mobile_banking_prediction_challenge (TBD -> 2nd Tier) has the same SEL-7 shape and should be aligned with this one; the curator's 2026-10-22 No on dataorg_financial_health_prediction_challenge (survey data, unclear target) points the same way.

Zindi 'Don't Overfit' competition (UofK FMSI), modeled on the well-known Kaggle 'Don't Overfit!' challenges, which deliberately provide a tiny training set with many anonymized continuous features to stress-test overfitting. Such datasets are typically very small and often artificial/anonymized, putting them at risk under criterion 4B (artificial) and 'Too Small'. They can still be interesting tabular benchmarks but are unrepresentative edge cases. A human must verify the training-set size, whether features are real or synthetic/anonymized, and the target before any promotion; 2nd Tier at most.
