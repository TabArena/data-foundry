---
unique_name: financial_inclusion_in_africa_for_botswana
name: financial-inclusion-in-africa-for-botswana
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2019'
domain: finance
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/financial-inclusion-in-africa
- https://zindi.africa/competitions/financial-inclusion-in-africa-for-botswana/data
- https://zindi.africa/competitions/zindi-mentorship-1-financial-inclusion-in-africa
- https://zindi.africa/competitions/nust-2022
- https://zindi.africa/competitions/dedan-kimathi-university-of-technology-dsaic-hackathon
- https://zindi.africa/competitions/indabax-malawi-2021
- https://zindi.africa/competitions/indabax-sudan-2021
- https://zindi.africa/competitions/indabax-tunisia-2021-beginner
- https://zindi.africa/competitions/pyladies-financial-inclusion-in-africa
- https://zindi.africa/competitions/dsea-financial-inclusion-in-africa
source_row: 986
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 2: a real 33.6k-person survey task, but the label is the respondent's own account status from the same interview (SEL-7 doubt).
- Source: the Zindi knowledge competition "Zindi Financial Inclusion in Africa" (opened 2019-07-29, 10,679 participants); the Botswana hackathon (2023-10-21 to 10-29, WiMLDS Gaborone) is a re-run with the same description, files and metric (Zindi API, parent `financial-inclusion-in-africa`). As published: "approximately 33,600 individuals" from FinAccess Kenya 2018, FinScope Rwanda 2016, Tanzania 2017, Uganda 2018, demographic and household columns plus `VariableDefinitions.csv`; target `bank_account` (Yes/No); one table, Train/Test 70/30; the ID is `uniqueid x country` (uniqueid alone is not unique).
- Use case: the source wants a model "to predict which individuals are most likely to have or use a bank account", for "an indication of the state of financial inclusion"; no actor or decision is named, so a bank or NGO targeting the unbanked is our reading. Fit approximate; regime IID (cross-sectional survey snapshot; four countries, a grouped-by-country split is not what the task asks).
- Siblings and duplicates: this record is the only one for this data; the nine Zindi links in `source_links` are re-runs of the same files, now led by the 2019 original. The old `Duplicate` marker is dropped: no other record holds the dataset (this one should stand for it). Related but distinct: `ix_mobile_banking_prediction_challenge`, `indabax_tanzania_mobile_banking_prediction_challenge` (mobile-banking use, other data), `mobile_money_and_financial_inclusion_in_tanzania_challenge` (FinScope Tanzania 2017 alone; check for overlap of rows with the Tanzania part here, PROV-6). External collections: none found.
- Papers and pages: Zindi description, evaluation and data pages (read through the Zindi API); FinScope and FinAccess survey reports are the upstream documentation; no paper on the competition data found.
- Metric: Zindi's Evaluation page: "The evaluation metric for this challenge is Mean Absolute error, where 1 indicates that the individual does have a bank account and 0 indicates that they do not"; a leaderboard metric (MET-4), on hard 0/1 submissions it equals the error rate; inputs none.
- Risks for /add-dataset: SEL-7, the respondent knows whether they have an account and answers in the same interview as the features, so the task needs a use case where the account status of non-surveyed people is predicted from demographics; FinScope sampling weights not shipped (whether the release is a weighted sample is unknown); check the overlap with the Tanzania records (PROV-6); columns such as `cellphone_access` are answers from the same interview, fine as features if the use case holds.
- Priority: gap 0 (finance not thin), use case 0 (no actor or decision named), source + (national FinScope/FinAccess surveys, Zindi variable definitions), shape + (33.6k rows, mixed categorical features), risk - (SEL-7 label known to the respondent).

Zindi 'Financial Inclusion in Africa' task: predict whether an individual has/uses a bank account from demographic and household survey features, a genuine real-world binary classification problem in finance/social science. It is a strong tabular task, but the many listed source links show the same Financial Inclusion in Africa dataset reused across numerous Zindi competitions, so this 'Botswana' variant may be a subset or re-upload of the canonical FSD/FinScope survey data and risks duplication with other candidates. A human must confirm whether the Botswana data is distinct, check the survey-weighting/sampling concerns, the row count, and the target column.

---

Predict whether a person has a bank account
