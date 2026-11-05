---
unique_name: wisconsin_local_government_property_insurance_fund
name: 'Wisconsin Local Government Property Insurance Fund (LGPIF), building and contents, 2006-2010 (Frees, Loss Data Analytics: PropertyFundInsample.csv)'
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 4
tags:
- Two-Regime Zeros
- Non-IID (Temporal)
original_source: Github
year: '2017'
domain: insurance
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://github.com/OpenActTexts/Loss-Data-Analytics/blob/master/Data/PropertyFundInsample.csv
- https://users.ssc.wisc.edu/~ewfrees/loss-data-analytics/introduction-to-loss-data-analytics/1-4-case-study-wisconsin-property-fund
- https://doi.org/10.3390/risks4010004
v2_path: datasets/_dev/tabarena-v0pt2/wisconsin_local_government_property_insurance_fund/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a lead list of exposure-scaled insurance tables, the source pages and papers, and the downloaded data where the notes say so. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> Yes`, priority 3: the documented building-and-contents claims of Wisconsin's
property fund for local governments, 2006-2010, studied for the fund's own ratemaking; small, and five years give two
windows.
- Source: Frees, Lee and Yang (2016), "Multivariate Frequency-Severity Regression Models in Insurance", Risks 4(1):4, on
  the Local Government Property Insurance Fund (LGPIF). Public file: `PropertyFundInsample.csv` of the open textbook
  Loss Data Analytics (OpenActTexts, Ch. 1 case study): 5,639 entity-years of 1,227 entities; header previewed:
  `PolicyNum`, `Year`, `LnCoverage`, `BCcov`, `Premium`, `Freq`, `Deduct`, `y`, `lny`, `yAvg`, `lnDeduct`, `Fire5`,
  `NoClaimCredit`, six entity-type and four alarm-credit dummies. Whether the file was public with the 2016 paper was
  not checked.
- Use case: the fund's own. Lee (2017, UW-Madison dissertation advised by Frees, Ch. 1): "implementing a more accurate
  and cost efficient rating engine was mutually agreed to be the primary goal of the project", the ratemaking of the
  building-and-contents line; the fund rates each entity for the next year; fit direct. Regime temporal by year,
  entities recurring (SPLIT-13).
- Siblings and duplicates: none in the log (grep for LGPIF, Wisconsin, PropertyFund); OpenML: none by name.
- Papers and pages: Frees, Lee and Yang (2016, doi:10.3390/risks4010004; MDPI refused the fetch, not read); Lee (2017),
  whose Ch. 5 holds the same LGPIF case study (read from the UW library copy); Loss Data Analytics Ch. 1.
- Metric: Lee (2017) Sec. 5.1.6 and 5.1.7 validate on the 2011 hold-out by Spearman correlation and by a Gini index
  "calculated using relativities computed with the actual premium collected by the LGPIF in 2011 as the denominator";
  Sec. 2.3 argues for the Gini because "for many insurance data sets, there are large masses at zero, meaning that these
  traditional metrics are less helpful". An argued choice reported beside a second statistic (MET-5, borderline); it
  needs `Premium` as its base, which ships and would then be a scoring column, not a feature (MET-2), and it is not in
  the library (MET-13). Otherwise the fallback (`rmse`).
- Earlier AI triage, 2026-10-20, measured: 70.2% zeros, no negatives; untuned LightGBM 2006-09 -> 2010 (1,110 rows, 403
  with a claim): AUC 0.78 for a claim, R^2 0.25 on log1p among positives; log coverage alone AUC 0.74.
- Risks for /add-dataset: drop `Freq`, `lny` and `yAvg` (restate the target `y`); `Premium` as a feature (the fund's own
  rate, USE-6) or as the Gini's base; five years give two windows above the 50% floor (2009, 2010), short of SPLIT-14's
  three, so SPLIT-8 (forced grouped by entity) unless the curator accepts two; the 2011 hold-out is not public; the
  coverage `BCcov` is the exposure (the family's insurance-conventions question).
- Priority: gap 0, use case + (the fund's ratemaking, named by the source), source + (a paper, a dissertation and a
  textbook chapter), shape + (5,639 entity-years, mixed types, dated and grouped), risk - (two windows, the premium's
  role).

**Assessment (AI, 2026-10-30):** suggested call for policy question 3 of the zero-inflated review, where Andrej asked
for a call per dataset from its references and the domain's practice instead of one convention for the family (the
shared reasoning: a time exposure or a sum insured is a feature, and a rating-cell table weights the metric by its
exposure; negative amounts that are recoveries become 0; the source's metric first, else the normalized Gini as a
context metric, since RMSE on raw amounts follows a few large claims and a Tweedie or Poisson deviance needs positive
predictions; MET-10 as amended on 2026-11-02 (Andrej) later declined a family-wide metric, so each table's metric is
decided on its own); the curator
has the call.
- Target: `y`, the building-and-contents claims of the entity-year; drop `Freq`, `lny` and `yAvg`.
- Exposure: the coverage `BCcov` (as log coverage) is a feature, the size of the risk as the paper uses it; rows are
  whole entity-years.
- Negative amounts: none.
- Metric: the source's, the Gini index with the fund's `Premium` as the base (Frees, Lee and Yang 2016, Sec. 6.2; Lee
  2017, Sec. 5.1.6-5.1.7), a custom metric (MET-13) with `Premium` as a scoring column, not a feature (MET-2), since the
  task is the rating engine that would replace that premium. Simpler alternative: the plain normalized Gini with
  `Premium` as a feature (USE-6).
- Test years 2009 and 2010 (two windows; the SPLIT-8 call stays).

CC (2026-10-30, Andrej): `Yes`, priority 3 (the AI screening had `TBD -> Yes`, priority 3; zero-inflated screening
review page).

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

**Assessment (AI, 2026-11-01):** added as `datasets/_dev/tabarena-v0pt2/wisconsin_local_government_property_insurance_fund/` by /add-dataset with the full review panel; the open questions are in its `REVIEW.md`. Recommend shipping; the open call is the split (its issue 1: folds grouped by member as SPLIT-8 is written, or amend SPLIT-14 so the two yearly windows ship). Changes after the panel: the source's metric declared, `ordered_lorenz_gini` (Frees et al.'s Gini of the losses ordered against the fund's premium, new in the library), with `Premium` as base and scoring column; the target in dollars (its issue 2); `NoClaimCredit` missing for the 2,412 member-years without two earlier years in the file; `PolicyNum` the group and no feature. Corrections to the notes above: "R^2 0.25 on log1p among positives" was the builder's first split (0.10-0.22 in the yearly windows, -0.01 to 0.20 on the shipped splits); the test years hold 301 (2009) and 403 (2010) member-years with a claim, not "about 400 each". `year`, `required_split` and `tags` wait for your marks on the field rows. Priority 4: gap + (insurance thin among the accepted definitions), use case + (the fund's own ratemaking, named by the source), source + (a paper and the open textbook), shape + (5,639 member-years of 1,227 members), risk - (sorting by coverage alone beats the probed models on average; the split is open).

**Assessment (AI, 2026-11-02):** the leak test across the forced grouped split (SPLIT-8 as amended 2026-11-02; untuned LightGBM on the 9 shipped member folds) finds a shared period, so the split as implemented would be `No`; added to issue 1 of the folder's `REVIEW.md`, the split unchanged. (1) Shared rows: no exact copy of a test row's inputs in training; 17-20 near copies per fold agree on a claim at 0.55-0.82 against 0.58 by chance; no renumbered member (none of 23 candidate pairs within 1% coverage). (2) Shared period: predicting each test year without that year's training rows, against without as many random rows, costs ROC AUC 0.010 (8 of 9 splits), R^2 0.017 on log1p (9 of 9) and the shipped Gini 0.113 on average (5 of 9, -0.23 to +0.55) on the pooled fold, but AUC 0.002 and Gini 0.008 (SD 0.20) within one year: the training side carries each year's claim level (2010's claims 3.3 times 2009's), and dropping `Year` does not remove it. (3) Features from other rows: `NoClaimCredit` is the member's own two earlier years in 3,227 of 3,227 rows and no member is on both sides. Recommend scoring within each year (the mean of the yearly Ginis, `Year` as the metric's group, a library change), or the two yearly windows with a SPLIT-14 amendment; the curator has the call.

CC (2026-11-02, Andrej): split (issue 1, discuss on the review page): "We found that grouped splits leak, so I would recommend to use three splits, one for each year of 2008, 2009, 2010". Implemented: three expanding yearly windows, newest first, each training on every earlier policy year with no gap: test 2010 on 2006-2009 (80.3% of the rows; 1,110 test member-years, 403 with a claim), test 2009 on 2006-2008 (60.6%; 1,112, 301), test 2008 on 2006-2007 (40.6%; 1,125, 309). The 2008 window is below SPLIT-14's floor of half the rows, a departure on the curator's call; no gap is an exception to SPLIT-10 that serves SPLIT-14, as pricing_game_2016_french_fleet (splits.md Cases). `ForcedGroupedFromTemporal` dropped; `PolicyNum` is now an input (known members, USE-10). Untuned ordered_lorenz_gini (test 2008, 2009, 2010): Tweedie GLM 0.254, 0.251, 0.350; LightGBM Tweedie 0.146, 0.254, 0.327; coverage alone 0.019, 0.195, 0.540. No test year has a row on its training side.

CC (2026-11-02, Andrej): target (issue 2) `ok`: the claims stay in dollars as implemented. Metric `ok` (ordered_lorenz_gini against the premium). Field rows: `year` updated from 2016 to 2017 (the definition's, the textbook repository's first commit); `required_split` kept Temporal (NON-IID) and the tag kept Non-IID (Temporal), which the definition now matches. Verdict: changes (applied 2026-11-02).

CC (2026-11-02, Andrej): ship, on the three expanding yearly windows (test 2008, 2009, 2010; issue 1) and the claims in dollars (issue 2).

## Reference

Frees, E.W., Lee, G., Yang, L. (2016). Multivariate Frequency-Severity Regression Models in Insurance. Risks 4(1):4.
https://doi.org/10.3390/risks4010004

Frees, E.W. (ed.), Loss Data Analytics, Ch. 1 (Case Study: Wisconsin Property Fund). OpenActTexts.
https://github.com/OpenActTexts/Loss-Data-Analytics

Lead: curator's list of exposure-scaled insurance tables (Chubb comparison), 2026-10-20; not in the v4 workbook.
