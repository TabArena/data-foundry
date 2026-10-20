---
unique_name: fema_ihp_valid_registrations
name: FEMA Individuals and Households Program - Valid Registrations (OpenFEMA v2), IHP award amount
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
- Non-IID (Grouped)
original_source: GOV Website
domain: social science
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.fema.gov/openfema-data-page/individuals-and-households-program-valid-registrations-v2
- https://www.fema.gov/api/open/v2/IndividualsAndHouseholdsProgramValidRegistrations
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

FEMA's Individuals and Households Program registrations on OpenFEMA: 26,245,246 rows (2026-10-20; disasters since
DR-1439, 2002), award 0 for 54.0%, with household, income, insurance, self-reported damage and needs, then FEMA's
inspection, eligibility and award fields. Sample of six disasters of 2020-2023 (DR-4562, 4630, 4663, 4697, 4699,
4724): 97,717 rows, `ihpAmount` 0 for 66.3% (45-87% by disaster), median award $3,912. The award follows program
rules: it equals HA + ONA in 100% of rows, HA is repair + replacement + rental in 99.6%, `ihpEligible` is true exactly
when the award is positive, and a depth-3 tree on the inspection results gives AUC 0.934 for any award and R^2 0.60 on
log1p among awards (criterion 3). Without the post-registration columns: leave-one-disaster-out ROC AUC 0.848
(0.755-0.909) for any award, but R^2 only 0.05 (-0.27 to 0.39) for the amount.

2nd tier: about half of the zeros are process outcomes, not missing damage (among zeros, "did not respond ... or
voluntarily withdrew" 28.7%, "needs to submit documentation" 20.8%, insured 14.4%, no eligible damage 7.2%, no reason
27.1%), and no source frames a prediction made at registration. Split if kept: grouped by disaster, later disasters
in test, since the rules change (the dictionary's separate HA and ONA maximums start with disasters declared after
1 Aug 2017); drop disasters of the last 18 months, which FEMA still refreshes weekly. To check: whether predicting
disaster aid from income and household data is an ethical concern. Licence: OpenFEMA terms (not re-read).

## Reference

Federal Emergency Management Agency (2026). OpenFEMA Dataset: Individuals and Households Program - Valid Registrations -
v2. Retrieved 2026-10-20 from https://www.fema.gov/openfema-data-page/individuals-and-households-program-valid-registrations-v2.

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).
