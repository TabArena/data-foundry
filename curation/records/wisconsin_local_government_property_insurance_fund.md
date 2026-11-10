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

**Assessment (AI, 2026-11-06):** the CC of 2026-11-02 (Andrej) on the split above cites the no-gap exception to SPLIT-10 "as pricing_game_2016_french_fleet (splits.md Cases)": that citation is stale. The precedent was reopened on 2026-11-06 (its REVIEW.md issue 6) and never covered a window below SPLIT-14's floor (its windows trained on 64-78% of the rows). Under options C, E or F of this dataset's issue 3 the exception goes; under A or B it needs a fact of its own and a SPLIT-10 Cases row (kind exception), which is missing today. The CC stays as Andrej's call.

**Assessment (AI, 2026-11-06):** exposure re-review (LEAK-41, MET-14 to MET-16). `Premium` is the rating's output (R^2 0.98 on the rating variables), set at the start of the year and not prorated in the years members join or leave; it is the base of the source's Lorenz curve and a scoring column only, with no training weight (MET-15: the target is a total and the premium is not realized). The coverage (`LnCoverage`) stays a feature, since the source estimates its coefficient (Frees, Lee and Yang 2016, Table 11: 0.853 negative binomial, 0.136 GB2). Rows are member-years with no time on risk; the years members leave show no claim shortfall (observed/expected 0.93) and the years they join no excess beyond chance (1.22). Three check warnings are accepted with reasons: `task_time_on_few_unique` (five policy years, no finer time), `task_target_value_dominant` (70.2% real no-claim years) and `meta_license_unknown`. Licence: the textbook's second edition (OpenActTexts/LDAVer2, WiscPropFund.csv, committed 2024-10-03) holds the same 5,639 member-years with every value the definition uses (checked 2026-11-06) and carries a CC0-1.0 LICENSE in its repository, CC BY 4.0 on its book pages; this supersedes the screening's "No data licence is stated in the repository", true only of the first edition, and the field is REVIEW.md issue 4. Issue 3, the split, is open: the 2008 window trains on 40.6% of the rows, below SPLIT-14's floor; on the two valid windows coverage alone scores 0.368 and an untuned Tweedie GLM 0.30-0.31; member folds share the year's claim level (ROC AUC +0.010 to +0.012 on the pooled score) and, within each year, +0.031 to +0.036 of Gini for the GLM (20 repeats, SE about 0.005; LightGBM about 0); folds by member with the test year left out of training remove both (GLM 0.139 against 0.175 with the test year in training).

**Assessment (AI, 2026-11-06):** review panel (focused: claim and split auditors, re-review under LEAK-41, MET-14 to MET-16): ship after changes, the text changes made (the reason for no training weight, the entry and exit years, the GLMs' covariates, the constant baseline, the licence reason, the stale no-gap precedent); for issue 3 the mediator recommends F (folds by member with the test year left out of training), else E (folds by member scored within each year, the within-year leak noted) or B (the two valid windows, by an amendment of SPLIT-14), to decide together with pricing_game_2016_french_fleet issue 6; disputed: the split (issue 3: the split auditor's E against the within-year leak the claim auditor found and the mediator confirmed); for the curator: issues 3 and 4.

**Assessment (AI, 2026-11-06):** REVIEW.md issue 4, named in the two lines above, is withdrawn: a licence decides no fix and is no issue for the curator (EV-4), so `license` stays None with the completed reason, and the curator's open point is issue 3 alone. Route if the release needs a stated licence: download the second edition's WiscPropFund.csv (https://raw.githubusercontent.com/OpenActTexts/LDAVer2/f987c4ed5e33001bddf069740d893a934e82673f/Data/WiscPropFund.csv, sha256 36b1e151728c25bd2467582f08e51d64fd5c83533e879c81edb2602b2c594b75 on 2026-11-06; the same 5,639 member-years, every value the definition uses equal), map `EntityType` {1: Village, 2: City, 3: County, 4: Misc, 5: School, 6: Town} and `AlarmCredit` {1: 0, 2: 5, 3: 10, 4: 15} (one to one with the first edition's flags), compute `LnCoverage = log(BCcov / 1e6)` and `lnDeduct = log(Deduct)`, rename `BCClaim` to the target, keep CLAIMLEVEL.csv, `source_url`, `year` (2017) and the citation from the first edition (PROV-8, PROV-9), and set `license = "CC0-1.0"` (the repository's LICENSE; its book pages state CC BY 4.0).

CC (2026-11-06, Lennart): issue 3, the three yearly windows stay (A), the 2008 window training on 40.6% of the rows, below the floor of half the rows: an exception ruling. "We think the task is too good to remove because of the 50% floor. So we overrule it here knowing it contradicts other judgement. The difference is that the task is better than prior out-ruled cases." How the rules record it (an amendment of the floor or an exception) is open in issue 3.

CC (2026-11-08, Lennart): the declared metric (`ordered_lorenz_gini`) is checked, as declared on the PR #47 review board.

CC (2026-11-08, Lennart): issue 3, reply (a) to the consistency check: the floor of half the rows is amended on this fund's facts (SPLIT-14: a release with two windows above the floor may add one older window that trains on at least 40% of the rows, when most test entities recur and folds by entity would test unseen ones), so the three yearly windows stay as an application of the amended rule, not an exception; the no-gap departure from SPLIT-10 is recorded with a fact of its own (every policy year ships with its final claim amounts; a one-year gap would put two windows below the floor).

CC (2026-11-09, Andrej): columns held only for training rows stay out for now, no training-only role (cross-dataset item of 2026-11-09; MET-14, LEAK-41, MET-16); the notes list them.

CC (2026-11-09, Andrej): the training labels' maturity is stated in the notes (cross-dataset item of 2026-11-09, option B).

CC (2026-11-09, Andrej): the fund's premium stays a scoring column only, the Gini's base and no input (REVIEW.md issue 4 (a), "Scoring column only"): it is the outside agency's price that the project's engine was built to replace; as an input it is no leak and gains nothing.

CC (2026-11-09, Andrej): the member's claim count of the year before is added as `prev_year_claims` (REVIEW.md issue 5 (b), "The previous year's claim count"), missing where the file lacks that year; the year before's amount stays out.

**Assessment (AI, 2026-11-09):** issue 5 applied in the definition. `dataset check` 0 errors, 0 warnings; the leak probes flag nothing (`prev_year_claims` alone R^2 0.027 on dollars, no exact copies across the split). On the declared Gini the count moves the scores in no consistent direction: the Tweedie GLM of the notes 0.260 against 0.285 without it, while the task probe's untuned families score higher with it (linear 0.202 against 0.119, random forest 0.202 against 0.142, LightGBM 0.073 against 0.020; SD across the 3 windows 0.075 to 0.152). The notes now say that `NoClaimCredit` looks computed from the file's own claims, not read from the fund's rating.

CC (2026-11-09, Andrej): ship (review page of 2026-11-09).

CC (2026-11-10, Andrej): the losses stay uncapped in scoring; the notes state each window's swing from its largest claim, and the first tuned benchmark run decides whether the table tells methods apart (REVIEW.md issue 6, A, as implemented).

CC (2026-11-10, Andrej): ship (review page of 2026-11-10).

## Reference

Frees, E.W., Lee, G., Yang, L. (2016). Multivariate Frequency-Severity Regression Models in Insurance. Risks 4(1):4.
https://doi.org/10.3390/risks4010004

Frees, E.W. (ed.), Loss Data Analytics, Ch. 1 (Case Study: Wisconsin Property Fund). OpenActTexts.
https://github.com/OpenActTexts/Loss-Data-Analytics

Lead: curator's list of exposure-scaled insurance tables (Chubb comparison), 2026-10-20; not in the v4 workbook.
