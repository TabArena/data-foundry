---
unique_name: nfip_redacted_flood_claims
name: NFIP redacted flood insurance claims (OpenFEMA NfipClaims v3, formerly FimaNfipClaims v2)
checked_by:
- Andrej
suggestion: TBD -> Yes
priority: 2
tags:
- Two-Regime Zeros
- Non-IID (Temporal)
original_source: GOV Website
domain: insurance
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.fema.gov/openfema-data-page/nfip-redacted-claims-v3
- https://www.fema.gov/api/open/v3/NfipClaims
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> Yes`, priority 2: FEMA's own register of flood insurance claims with an observed
zero regime (17.0% of 2021-2023 claims closed without payment, earlier AI triage, 2026-10-20, measured), but the
prediction point and the target are still to be chosen and the adjuster's fields leak.
- Source: FEMA, OpenFEMA "FIMA NFIP Redacted Claims", first released in the summer of 2019 (Dombrowski, Ratnadiwakara
  and Slawson, Journal of Real Estate Literature 28(2):190-212, abstract; FEMA's changelog lists v1 as a new API in
  2020-07, so `year` is left empty), v3 since 2026-07 ("new fields added, some field names and datatypes have changed",
  changelog; v2 "slated for removal by October 15, 2026", v2 page). As published: one table, one row per "flood
  insurance claims transaction" (v3 page); 2,725,989 claims x 84 columns, losses 1978-2026 (earlier AI triage). Payouts
  `amountPaidOnBuildingClaim`, `amountPaidOnContentsClaim`, `amountPaidOnIncreasedCostOfComplianceClaim`, with
  `nonPaymentReasonBuilding` and `nonPaymentReasonContents` (the "Claim Closed Without Payment Reason", v3 page).
- Use case: for example, the NFIP sets a case reserve for a claim when it is filed (no source names a predictive use);
  fit approximate. Regime temporal by loss date, since the next floods are new events (SPLIT-6); repeat claims of one
  building cannot be grouped (no building id).
- Siblings and duplicates: none among the records (by name, link and source); `fema_ihp_valid_registrations` is FEMA's
  household-aid table, another task. External collections: none found.
- Papers and pages: Wing et al. 2020 (Nat. Commun. 11:1444) fit depth-damage relations on claims obtained from FEMA
  (earlier AI triage); Saha and Ravela 2022 (arXiv 2212.08660) and DELUGE (arXiv 2607.16050) model paid amounts from
  rainfall (search abstracts only, texts not read).
- Metric: none found (the OpenFEMA pages state no task; the papers above not read for one), so the fallback `rmse`;
  inputs none.
- Risks for /add-dataset: the prediction point (at filing; the adjuster's water depth and duration fit only a
  post-inspection point) and the target (building, contents or total); the adjuster's damage and value fields, net and
  ICC payments, non-payment reasons and payment dates are post-outcome (LEAK-10; AUC 0.983 with the damage amounts,
  earlier AI triage); open family question: coded and censored zeros (a null and a 0 payout both mean closed without
  payment, nulls without a reason look like open claims in the newest year).
- Priority: gap 0 (insurance 4, regression and temporal not thin), use case 0 (none named), source + (FEMA's data
  dictionary), shape + (millions of claims, mixed features, 48 years), risk - (leaking adjuster fields, target and
  prediction point open).

**Assessment (AI, 2026-10-30):** suggested call for policy question 3 of the zero-inflated review, where Andrej asked
for a call per dataset from its references and the domain's practice instead of one convention for the family (the
shared reasoning is in `curation/inputs/two_regime_zero_triage_summary.md`, "Policy calls of 2026-10-30"); the curator
has the call.
- Target: the total paid on building and contents at filing (ICC left out); a null payout with a non-payment reason
  counts as 0 and the open claims of the newest year are dropped, since the family's open question on coded and censored
  zeros is settled (Andrej, 2026-10-30, policy question 2 of the zero-inflated review: "We don't care. We want to add
  any relevant predictive task, independent if it is zero inflated or not"), so how the source codes its zeros is no
  reason for a No or a lower priority.
- Exposure: building and contents coverage, with the deductibles, as features (they cap the payout).
- Negative amounts: none found.
- Metric: `rmse` (fallback): the use is a case reserve, set in dollars per claim, where the error in dollars matters; no
  source names a metric.

**Assessment (AI, 2026-10-30):** to the curator's question ("If you can fix the leak it should be fine, isnt it?"): yes.
The leak is the adjuster's post-inspection fields (damage amounts, property values, water depth and duration, net and
ICC payments, non-payment reasons, payment dates); at a prediction point at filing they are dropped, and what remains
still carries a weak but real signal (AUC 0.58 for a payout, R^2 0.15 on log1p among positives; train 2021-22, test
2023). Left for /add-dataset: the target (building + contents, as suggested above) and the cut of the newest, still open
year.

CC (2026-10-30, Andrej): `TBD -> Yes`, priority 2, as screened (verified on the zero-inflated screening review page).
"If you can fix the leak it should be fine, isnt it?"

FEMA's National Flood Insurance Program claims, redacted, on OpenFEMA (v3; v2 retired 2026-10-15): 2,725,989 claims x
84 columns, losses 1978-2026, with policy, building, flood zone, elevation, coverage, location, loss date and flood
event. The zeros are claims closed without payment: the building payout is null for 567,072 claims and 0 for 150,854,
and 519,140 of the nulls carry a "Claim Closed Without Payment Reason", so null means 0. Codes 98 and 99 (deleted,
erroneous assignment) are clerical, 6.8% of an API sample of the 128,651 claims of 2021-2023; nulls without a reason
look like open claims (808 of 6,157 for 2026 losses, 722 of 35,312 for 2019), so the newest year is cut. Then the
total payout is 0 for 17.0%. Split: temporal by loss date (new flood events). Probe (train 2021-22, test 2023) on
fields known at filing: ROC AUC 0.578, R^2 0.152 on log1p among positives; the adjuster's water depth and duration
raise this to 0.772 and 0.220.

Leaks: the adjuster's damage amounts (AUC 0.983, R^2 0.959 with them), net and ICC payments, non-payment reasons,
`replacementCostBasis`, the adjuster's property values, recoveries, payment dates, handling cause codes B-D. Depth
fits only a post-inspection prediction point, the depth-damage use (Wing et al. 2020, Results: "We analyzed 2,085,015
NFIP flood damage claims (1972-2014) from a database obtained directly from FEMA"). To decide: prediction point,
target (building or total), years to keep. No building id, so repeat claims cannot be grouped. Licence: OpenFEMA
terms (not re-read).

## Reference

Federal Emergency Management Agency (2026). OpenFEMA Dataset: FIMA NFIP Redacted Claims - v3. Retrieved 2026-10-20 from
https://www.fema.gov/openfema-data-page/nfip-redacted-claims-v3.

Wing O.E.J., Pinter N., Bates P.D., Kousky C. (2020). New insights into US flood vulnerability revealed from flood
insurance big data. Nature Communications 11:1444. doi:10.1038/s41467-020-15264-2.

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).
