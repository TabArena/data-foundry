---
unique_name: fema_ihp_valid_registrations
name: FEMA Individuals and Households Program - Valid Registrations (OpenFEMA v2), IHP award amount
checked_by:
- Andrej
suggestion: TBD -> 2nd Tier
priority: 3
tags:
- Two-Regime Zeros
- Non-IID (Grouped)
original_source: GOV Website
year: '2020'
domain: social science
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.fema.gov/openfema-data-page/individuals-and-households-program-valid-registrations-v2
- https://www.fema.gov/api/open/v2/IndividualsAndHouseholdsProgramValidRegistrations
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 3: FEMA's registrations for disaster aid in a thin domain,
with a measured zero regime, but no source frames a prediction at registration and about half of the zero awards are
process outcomes such as withdrawals and missing documents (earlier AI triage, 2026-10-20, measured).
- Source: FEMA, OpenFEMA "Individuals and Households Program - Valid Registrations", v1 2020-01 ("[New]", changelog;
  `year` set from it), v2 2025-05 ("Many new fields have been added"). As published: one table, one row per valid
  registration for major disasters from DR-1439 (2002), declared more than 30 days ago; `ihpAmount` is "the total
  approved IHP award for Housing Assistance and/or Other Needs Assistance", `ihpEligible` true for applicants who
  received an award (v2 page); 26,245,246 rows, award 0 for 54.0% (earlier AI triage).
- Use case: for example, FEMA estimates the aid of a new disaster's registrants to plan staff and funds (no source names
  it); fit approximate. Regime: later disasters in test, since program rules change (separate HA and ONA maximums from 1
  Aug 2017, earlier AI triage); whether the split is grouped by disaster or temporal by declaration is for SPLIT-3 and
  the use case; FEMA still refreshes the last 18 months weekly (v2 page), so they are cut.
- Siblings and duplicates: none among the records (by name, API entity and source); `nfip_redacted_flood_claims` is
  FEMA's flood insurance claims, another task. External collections: none found.
- Papers and pages: the OpenFEMA page and data dictionary; no paper that predicts the award was found (short search).
- Metric: none found (OpenFEMA page), so the fallback `rmse`; inputs: the disaster number as the group, which ships.
- Risks for /add-dataset: inspection, eligibility and the HA and ONA components are recorded after registration and
  rebuild the award (award = HA + ONA in 100% of rows, earlier AI triage; LEAK-10); open family question: coded and
  censored zeros (a withdrawal or missing documents is a process zero, not an observed absence of damage); a SEL-1
  question for the curator: whether predicting aid from income and household data is a harmful use; 26M rows.
- Priority: gap + (social science, 1 accepted), use case 0 (none named), source + (FEMA's dictionary), shape +
  (disasters as groups, mixed features), risk - (process zeros, post-registration fields).

**Assessment (AI, 2026-10-30):** The family's open question on coded and censored zeros is settled (Andrej, 2026-10-30,
policy question 2 of the zero-inflated review: "We don't care. We want to add any relevant predictive task, independent
if it is zero inflated or not"), so how the source codes its zeros is no reason for a No or a lower priority. The
process zeros (withdrawn, missing documents) are a cleaning or target choice at /add-dataset. The verdict and priority
stay on the screening's other points.

CC (2026-10-30, Andrej): `TBD -> 2nd Tier`, priority 3, as screened (verified on the zero-inflated screening review
page).

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
