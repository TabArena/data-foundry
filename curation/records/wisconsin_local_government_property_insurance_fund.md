---
unique_name: wisconsin_local_government_property_insurance_fund
name: 'Wisconsin Local Government Property Insurance Fund (LGPIF), building and contents, 2006-2010 (Frees, Loss Data Analytics: PropertyFundInsample.csv)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
- Non-IID (Temporal)
original_source: Github
year: '2016'
domain: insurance
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://github.com/OpenActTexts/Loss-Data-Analytics/blob/master/Data/PropertyFundInsample.csv
- https://users.ssc.wisc.edu/~ewfrees/loss-data-analytics/introduction-to-loss-data-analytics/1-4-case-study-wisconsin-property-fund
- https://doi.org/10.3390/risks4010004
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a lead list of exposure-scaled insurance tables, the source pages and papers, and the downloaded data where the notes say so. A human must verify the suggestion, the metadata and the notes before relying on them.**

Building-and-contents (BC) cover of Wisconsin's Local Government Property Insurance Fund, a state pool for counties,
cities, towns, villages, school districts and other local entities (Frees, Lee and Yang 2016, Sec. 5). The public
file is `PropertyFundInsample.csv` of the open textbook Loss Data Analytics (OpenActTexts on GitHub; `WiscPropFund.csv`
holds the same rows with fewer columns): 5,639 entity-years of 1,227 entities, 2006-2010. Coverage `BCcov` runs from
$8,937 to $2.44B (median $11.4M). The features are the deductible, entity type, alarm credit, `Fire5` and
`NoClaimCredit`; `Premium` is the fund's own rate. `Freq`, `yAvg` and `lny` restate the target `y` (total BC claims in
the year) and must be dropped. Measured 2026-10-20: 70.2% zeros, no negatives, positives from about $1.5k to $12.9M.

The book starts in 2006 "because there was a shift in claim coding in 2005" and stops before 2011 "to mitigate the
effect of open claims" (Ch. 1, Fund Rating Variables). The paper validates on 2011 (Sec. 6.1: "The out of sample
validation is performed on the 2011 held-out data, where there are 1098 observations"), but no 2011 file turned up in
the OpenActTexts or ewfrees repositories or on the fund's project site, so the public task is 2006-2010 split by year.
Untuned LightGBM, 2006-09 -> 2010 (1,110 rows, 403 with a claim): AUC 0.78 for a claim, R^2 0.25 on log1p among
positives. Log coverage alone gives AUC 0.74 and a linear R^2 of 0.27, so coverage carries most of the signal. In
Sec. 6.2 a Tweedie score does not beat the fund's premium on Gini (-1.74%) and the copula frequency-severity model
does (22.77%).

TBD -> Yes: a documented entity-level pricing table, the closest public match to the Chubb setup (commercial-type
property, coverage over five orders of magnitude, deductible and entity type). It is small: after the 50% floor the
test years are 2009 and 2010, about 400 positives each. No data licence is stated in the repository. To check: whether
the authors share the 2011 file; whether `Premium` stays as a feature or serves only as the Gini baseline;
`CLAIMLEVEL.csv` (6,258 BC claims, 2006-2010) to check the totals.

## Reference

Frees, E.W., Lee, G., Yang, L. (2016). Multivariate Frequency-Severity Regression Models in Insurance. Risks 4(1):4.
https://doi.org/10.3390/risks4010004

Frees, E.W. (ed.), Loss Data Analytics, Ch. 1 (Case Study: Wisconsin Property Fund). OpenActTexts.
https://github.com/OpenActTexts/Loss-Data-Analytics

Lead: curator's list of exposure-scaled insurance tables (Chubb comparison), 2026-10-20; not in the v4 workbook.
