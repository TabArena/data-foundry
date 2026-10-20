---
unique_name: nfip_redacted_flood_claims
name: NFIP redacted flood insurance claims (OpenFEMA NfipClaims v3, formerly FimaNfipClaims v2)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
tags:
- AI-Filled (Verify)
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
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

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
