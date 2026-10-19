---
unique_name: autoclaim_sas_motor_insurance
name: AutoClaim (cplm) / auto (HDtweedie) / SAS Enterprise Miner motor insurance data (Yip and Yau 2005)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- Missing source information
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
- Non-IID (Temporal)
original_source: Company
year: '2005'
domain: insurance
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://cran.r-project.org/package=cplm
- https://cran.r-project.org/package=HDtweedie
- https://doi.org/10.1016/j.insmatheco.2004.11.002
- https://doi.org/10.1080/10618600.2015.1005213
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

Motor insurance policies "retrieved from the SAS Enterprise Miner database" (cplm documentation): 10,296 policies with
effective dates from April 1993 to July 1999 and 29 columns (driver, household, vehicle, claim history). Target:
`CLM_AMT`, the claim amount in the current insured period. HDtweedie's `auto` (workbook Master row 55) is the 2,812
policies flagged `IN_YY` here (the subset Yip and Yau 2005 used), re-coded into 56 dummy predictors (Qian et al.
2016), so it is a cut of this table and is merged into this record.

Zero mechanism, confirmed from the data: `CLM_AMT` is 0 for exactly the 7,556 policies with `CLM_FLAG` = "No"
(73.4%), i.e. no claim in the period; the share is 72-75% in every policy year. `CLM_FLAG` is a target copy and has to
go; `CLM_FREQ5` and `CLM_AMT5` (claims in the past five years) are history known at the policy date. A quick
untuned LightGBM (3-fold random CV, `CLM_FLAG`, `POLICYNO` and `IN_YY` dropped) gives ROC AUC 0.82 for a claim and
R^2 0.25 on the log1p amount (0.02 on the raw amount).

Provenance is the open question. No insurer is named, the same table circulates as Kaggle's `car_insurance_claim`,
and the data section of Yip and Yau (2005) is paywalled and was not read. Quick generated-data checks: income follows
job class and education (median 22,640 below high school, 126,858 PhD), home value follows income (Spearman 0.57),
motor-vehicle-record points raise the claim rate from 19% to 69%, and no numeric column is uniform; but the positive
claim amounts carry no rounding (10.1% are multiples of 10, the share random digits give), the "Unknown" job class has
the highest median income (109,953), and rural policies claim at 6.5% against 31.7% urban. Hence 2nd tier with
`Missing source information` until the curator settles where SAS took the data from. Split: policy dates span six
years, so pricing new policies from older ones means a temporal split on `PLCYDATE` (the literature uses random
splits). Licence: GPL (>= 2) (cplm), GPL-2 (HDtweedie).

## Reference

Yip K.C.H., Yau K.K.W. (2005). On modeling claim frequency data in general insurance with extra zeros. Insurance:
Mathematics and Economics 36(2):153-163. doi:10.1016/j.insmatheco.2004.11.002. Data: `AutoClaim` in the R package
cplm (Zhang Y.); `auto` in the R package HDtweedie, built as in Qian W., Yang Y., Zou H. (2016). Tweedie's compound
Poisson model with grouped elastic net. Journal of Computational and Graphical Statistics 25:606-625.
doi:10.1080/10618600.2015.1005213.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master rows 56 (AutoClaim / cplm motor insurance) and 55
(HDtweedie auto insurance).
