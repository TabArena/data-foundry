---
unique_name: australian_vehicle_insurance_2004_2005
name: dataCar (insuranceData) / ausprivauto0405 (CASdatasets) / Car (de Jong and Heller 2008)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: Website
year: '2008'
domain: insurance
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://search.r-project.org/CRAN/refmans/insuranceData/html/dataCar.html
- https://cran.r-project.org/package=insuranceData
- https://dutangc.github.io/CASdatasets/reference/ausprivauto.html
- https://github.com/dutangc/CASdatasets/blob/master/data/ausprivauto0405.rda
- https://doi.org/10.1017/cbo9780511755408
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

One-year Australian vehicle policies taken out in 2004 or 2005, the "Car" data of de Jong and Heller (2008): 67,856
policies, 4,624 (6.8%) with at least one claim. The same table ships as `dataCar` in the R package insuranceData and as
`ausprivauto0405` in CASdatasets (workbook Master rows 61 and 30). Both were downloaded on 2026-10-19 and agree row by
row on exposure, vehicle value and claim cost, so they get one record here. Features: vehicle value, body type, vehicle
age band, driver gender, area, driver age band and exposure (0-1 policy years). Target: `claimcst0`, the claim cost.

Zero mechanism, confirmed from the data: `claimcst0` is 0 for exactly the 63,232 policies with `clm` = 0 (93.2% of
rows), i.e. no claim within the exposure period. Occurrence and amount are both recorded, nothing is zero-filled. The
positive part has quirks: no cost is below 200, 695 of the 4,624 claims (15%) are exactly 200, and 219 claims share the
value 353.77, so small claims look floored at 200. A quick untuned LightGBM (3-fold random CV, target copies
dropped) separates claimants at ROC AUC 0.64 and reaches R^2 0.006 on log1p cost (-0.02 on the raw cost), against
0.97 for an oracle that knows which policies claimed: as in `forest_fires`, the zeros carry the variance and the
signal is small, which the task-probe rules accept.

Split IID: one policy year, no dates and no policy ids. Drop `clm` and `numclaims` (target copies) and `X_OBSTAT_`
(constant); 378 rows are exact duplicates. Licence: GPL-2 (insuranceData), GPL (>= 2) (CASdatasets). To check: whether
the 200 floor is the source's recording convention, and whether to model the cost with exposure as a feature or the
cost per policy year with exposure as a weight.

## Reference

De Jong P., Heller G.Z. (2008). Generalized Linear Models for Insurance Data. Cambridge University Press.
doi:10.1017/CBO9780511755408. Distributed as `dataCar` in the R package insuranceData (Wolny-Dominiak A., Trzesiok M.,
2014) and as `ausprivauto0405` in CASdatasets (Dutang C., Charpentier A.).

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master rows 61 (dataCar / insuranceData) and 30 (Insurance
ausprivauto0405).
