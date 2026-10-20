---
unique_name: spanish_motor_insurance_coverage_level_2022_2024
name: A detailed dataset of motor insurance policies with coverage-specific financial information (Spanish insurer, 2022-2024, Mendeley)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
- Non-IID (Temporal)
original_source: Other
year: '2026'
domain: insurance
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.17632/sw4jmdb2sm.1
- https://doi.org/10.1016/j.dib.2026.112883
- https://pmc.ncbi.nlm.nih.gov/articles/PMC13234478/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a lead list of exposure-scaled insurance tables, the source pages and papers, and the downloaded data where the notes say so. A human must verify the suggestion, the metadata and the notes before relying on them.**

Anonymised motor portfolio of an unnamed Spanish insurer, 1 January 2022 to 31 December 2024 (Espinosa, Lledó and
Atance, Data in Brief 66:112883, 2026; CC BY 4.0 on Mendeley). It has 354,140 rows for 185,678 insureds (67,172,
118,835 and 168,133 by year), with premiums, claim counts and incurred cost (paid plus reserved) for each of seven
covers. Data Description: "Each observation corresponds to an insured individual for a given year". The authors kept
the last record per insured and year out of 653,943 raw rows and left out rows with negative incurred amounts
(Experimental Design).

Zeros, measured 2026-10-20: `total_incurred` is 0 in 88.1% of rows. Own damage (property + theft + fire) is 0 in
96.0%, and in 86.8% of the comprehensive policies (`COMP_E`, `COMP_N`, the only types with property-damage cover).
8,543 rows report claims at zero cost. Untuned LightGBM, 2022-23 -> 2024 (168,133 rows): AUC 0.69 for any claim
(exposure alone 0.60), R^2 -0.03 on log1p among positives. Own damage on comprehensive policies: AUC 0.68 (0.70 with
the premiums), R^2 -0.07. The severity signal is weak, as in the rest of the family, and the article warns that the
fixed amounts of the CICOS agreement cluster indemnities (Limitations).

Fixes needed. `vehicle_age` is not the vehicle's age: `driver_age` = `vehicle_age` + `age_driving_licence` within a
year on 99.9% of rows, so it is years since licensing, and `age_driving_licence` is the age at licensing (Table 2 and
the text disagree on that column). `policy_status` is set at year end and must go: 13.9% of cancelled insured-years
have a claim at a mean exposure of 0.53, against 11.7% at 0.73 for active ones. For the Chubb-style target, use
`total_exposure` x `vehicle_value` with own-damage, theft and fire incurred on the comprehensive policies; liability
losses do not scale with vehicle value. A separate release by Lledó and Pavía (Mendeley 5cxyb5fp4f, November 2015 to
December 2018, 105,555 rows) is not in the log either, and whether it comes from the same insurer is open.

## Reference

Espinosa, P., Lledó, J., Atance, D. (2026). A detailed dataset of motor insurance policies with coverage-specific
financial information. Data in Brief 66:112883. https://doi.org/10.1016/j.dib.2026.112883
Data: Mendeley Data, https://doi.org/10.17632/sw4jmdb2sm.1 (CC BY 4.0).

Lead: curator's list of exposure-scaled insurance tables (Chubb comparison), 2026-10-20; not in the v4 workbook.
