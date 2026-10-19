---
unique_name: swedish_motorcycle_insurance_wasa
name: swmotorcycle (CASdatasets) / dataOhlsson (insuranceData) / mccase (Ohlsson and Johansson 2010, Wasa motorcycle insurance 1994-1998)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: Website
year: '2010'
domain: insurance
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://dutangc.github.io/CASdatasets/reference/swmotorcycle.html
- https://github.com/dutangc/CASdatasets/blob/master/data/swmotorcycle.rda
- https://staff.math.su.se/esbj/GLMbook/
- https://doi.org/10.1007/978-3-642-10791-7
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

Partial casco motorcycle insurance of the former Swedish insurer Wasa, the case-study data of Ohlsson and Johansson
(2010). CASdatasets ships it as `swmotorcycle`, insuranceData as `dataOhlsson` (same 64,548 rows, compared on
2026-10-19). The documentation says it "contains aggregated data on all insurance policies and claims during
1994-1998": a row is one combination of owner age, gender, zone, EV-ratio class, vehicle age and bonus class (all
64,548 feature vectors are distinct), with its policy years (`Exposure`, median 0.83, 2,074 rows at 0), claim count
and summed claim cost.

Zero mechanism, confirmed from the data: `ClaimAmount` is 0 for exactly the cells with no claim, 63,878 of 64,548
(98.96%); 670 cells carry a claim. Nothing is zero-filled. A quick untuned LightGBM (3-fold random CV) reaches ROC
AUC 0.75 for a claim, while R^2 on the cost stays at 0 (-0.01 on log1p).

2nd tier rather than Yes: the target is a five-year cell total with one claim in a hundred rows, about 220 claims per
test fold of a 3-fold split, and the cells are rating-factor aggregates, not policies. Workbook pushback: it reports
62,036 rows and 656 with claims; the file has 64,548 rows (62,474 with positive exposure) and 670 with claims (666
with positive exposure). Licence: GPL (>= 2) (CASdatasets), GPL-2 (insuranceData). To check: drop or keep the
zero-exposure rows, and whether the cost per policy year is the better target.

## Reference

Ohlsson E., Johansson B. (2010). Non-Life Insurance Pricing with Generalized Linear Models. EAA Lecture Notes,
Springer. doi:10.1007/978-3-642-10791-7. Data: `swmotorcycle` in CASdatasets (Dutang C., Charpentier A.);
`dataOhlsson` in the R package insuranceData.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 62 (swmotorcycle / CASdatasets).
