---
unique_name: global_findex_2025
name: 'The Global Findex Database 2025: Connectivity and Financial Inclusion in the Digital Economy (microdata)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
original_source: GOV Website
year: '2025'
domain: finance
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.48529/bk9n-8r43
- https://microdata.worldbank.org/index.php/catalog/7860
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: the World Bank's 2024 survey of about 145,000 adults in 141 economies with weights and a codebook; account ownership is a well-measured target, but the release is a survey for measurement with no predictive task, and the label is the respondent's own answer in the same interview (SEL-3 and SEL-7 doubts, as on its Zindi siblings).
- Source: World Bank Development Research Group, "The Global Findex Database 2025: Connectivity and Financial Inclusion in the Digital Economy", fieldwork by Gallup (World Poll) from 2024-05-01 to 2024-12-31, microdata version 02 of 2025-09-24 (https://doi.org/10.48529/bk9n-8r43, catalog 7860, reference WLD_2024_FINDEX_v02_M). As published: one row per adult aged 15 and over, "about 145,000 adults in 141 economies", weighted to be nationally representative (the weight combines "a base sampling weight and a poststratification weight"); the sibling record reads the main file as 144,090 cases x 199 variables (not checked here). Access under the Microdata Library's terms of use with a required citation (no criterion, EV-4). Target: account ownership (an account at a financial institution, or any account including mobile money).
- Use case: the source names none: the survey is "an indispensable resource for policy makers in the fields of digital connectivity and financial inclusion"; the record's reading is a bank, mobile-money provider or NGO targeting people likely to be unbanked from demographics; fit approximate (the respondent states the label in the same interview, SEL-7 to weigh: a provider would predict it for people it has not surveyed); regime IID (one cross-section; a grouping by economy is possible).
- Siblings and duplicates: `global_findex_2025_mobile_banking` (the same file with mobile or internet use of an account as target: a swapped target of the same respondents, PROV-6 to weigh, so at most one Findex framing should enter); `financial_inclusion_in_africa_for_botswana` (`TBD -> Yes`, priority 2, FinScope and FinAccess, the same target with the same SEL-7 doubt) and `mobile_money_and_financial_inclusion_in_tanzania_challenge` (`TBD -> Yes`, priority 2): other surveys, no duplicates (PROV-4); `dont_overfit_by_uofk_fmsi` (`No`, SEL-7, a Findex 2017 extract with a stated-ability target; AI screening with a reject check) and the curator's `No` on the FinScope `dataorg_financial_health_prediction_challenge` (2026-10-22: "it is survey data"). These should be decided together. External collections: none known.
- Better data: no new search; found as better data for `financial_inclusion_in_africa_for_botswana` and `mobile_money_and_financial_inclusion_in_tanzania_challenge`.
- Papers and pages: the Microdata Library catalog page (read); the Global Findex 2025 report (https://www.worldbank.org/en/publication/globalfindex, not read).
- Metric: none found (the catalog page poses no prediction; the report not read); fallback `roc_auc` (MET-1, MET-8). Inputs: the survey weight ships and could weight the score. The Zindi siblings' MAE on hard labels belongs to their own competitions.
- Risks for /add-dataset: SEL-3 and SEL-7 (a survey table; a label the respondent knows); many questions are asked only of account holders or presuppose an account (use of the account, digital payments, saving at an institution), so the inputs must be limited to demographics, income quintile, education, employment, and phone and internet access (LEAK); the account definition (financial institution or any account) is ours to pick; columns not inspected.
- Priority: gap 0 (finance, binary and IID are not thin), use case 0 (no actor or decision named), source + (World Bank and Gallup, codebook, weights, DOI), shape + (about 145,000 adults, mixed types, 141 economies), risk - (the SEL-7 doubt, answers that presuppose the label).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `financial_inclusion_in_africa_for_botswana`, `mobile_money_and_financial_inclusion_in_tanzania_challenge`.
- as published: about 145,000 adults in 141 economies, one row per respondent, nationally representative with sampling weights; codebook and questionnaire published (columns not inspected); target: account ownership (account at a financial institution, or any account including mobile money); access: registration.
- Why: the Zindi data are FinScope/FinAccess interviews with target bank_account; Findex asks the same account question with the same kind of demographic inputs (age, gender, education, income quintile, employment, urban/rural) | the same kind of target (financial-service usage group) predicted from the same kind of ...
- Adds: 4 times the respondents, 141 economies instead of 4 East African ones, 2024 instead of 2016-2018, with survey weights. The record's SEL-7 doubt applies alike (the respondent's own answer in the same interview; dont_overfit_by_uofk_fmsi, another Findex target, was rejected on SEL-7), so the two should be decided ...

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: two targets of one survey file (`global_findex_2025_mobile_banking`; PROV-7, weigh). The curator keeps one, or both as distinct tasks.
