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
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Later'
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

**Assessment (AI, 2026-11-01):** added as `datasets/_dev/tabarena-v0pt2/wisconsin_local_government_property_insurance_fund/` by /add-dataset with the full review panel; the open questions are in its Review. Recommend shipping; the open call is the split (its issue 1: folds grouped by member as SPLIT-8 is written, or amend SPLIT-14 so the two yearly windows ship). Changes after the panel: the source's metric declared, `ordered_lorenz_gini` (Frees et al.'s Gini of the losses ordered against the fund's premium, new in the library), with `Premium` as base and scoring column; the target in dollars (its issue 2); `NoClaimCredit` missing for the 2,412 member-years without two earlier years in the file; `PolicyNum` the group and no feature. Corrections to the notes above: "R^2 0.25 on log1p among positives" was the builder's first split (0.10-0.22 in the yearly windows, -0.01 to 0.20 on the shipped splits); the test years hold 301 (2009) and 403 (2010) member-years with a claim, not "about 400 each". `year`, `required_split` and `tags` wait for your marks on the field rows. Priority 4: gap + (insurance thin among the accepted definitions), use case + (the fund's own ratemaking, named by the source), source + (a paper and the open textbook), shape + (5,639 member-years of 1,227 members), risk - (sorting by coverage alone beats the probed models on average; the split is open).

**Assessment (AI, 2026-11-02):** the leak test across the forced grouped split (SPLIT-8 as amended 2026-11-02; untuned LightGBM on the 9 shipped member folds) finds a shared period, so the split as implemented would be `No`; added to issue 1 of the record's Review, the split unchanged. (1) Shared rows: no exact copy of a test row's inputs in training; 17-20 near copies per fold agree on a claim at 0.55-0.82 against 0.58 by chance; no renumbered member (none of 23 candidate pairs within 1% coverage). (2) Shared period: predicting each test year without that year's training rows, against without as many random rows, costs ROC AUC 0.010 (8 of 9 splits), R^2 0.017 on log1p (9 of 9) and the shipped Gini 0.113 on average (5 of 9, -0.23 to +0.55) on the pooled fold, but AUC 0.002 and Gini 0.008 (SD 0.20) within one year: the training side carries each year's claim level (2010's claims 3.3 times 2009's), and dropping `Year` does not remove it. (3) Features from other rows: `NoClaimCredit` is the member's own two earlier years in 3,227 of 3,227 rows and no member is on both sides. Recommend scoring within each year (the mean of the yearly Ginis, `Year` as the metric's group, a library change), or the two yearly windows with a SPLIT-14 amendment; the curator has the call.

CC (2026-11-02, Andrej): split (issue 1, discuss on the review page): "We found that grouped splits leak, so I would recommend to use three splits, one for each year of 2008, 2009, 2010". Implemented: three expanding yearly windows, newest first, each training on every earlier policy year with no gap: test 2010 on 2006-2009 (80.3% of the rows; 1,110 test member-years, 403 with a claim), test 2009 on 2006-2008 (60.6%; 1,112, 301), test 2008 on 2006-2007 (40.6%; 1,125, 309). The 2008 window is below SPLIT-14's floor of half the rows, a departure on the curator's call; no gap is an exception to SPLIT-10 that serves SPLIT-14, as pricing_game_2016_french_fleet (splits.md Cases). `ForcedGroupedFromTemporal` dropped; `PolicyNum` is now an input (known members, USE-10). Untuned ordered_lorenz_gini (test 2008, 2009, 2010): Tweedie GLM 0.254, 0.251, 0.350; LightGBM Tweedie 0.146, 0.254, 0.327; coverage alone 0.019, 0.195, 0.540. No test year has a row on its training side.

CC (2026-11-02, Andrej): target (issue 2) `ok`: the claims stay in dollars as implemented. Metric `ok` (ordered_lorenz_gini against the premium). Field rows: `year` updated from 2016 to 2017 (the definition's, the textbook repository's first commit); `required_split` kept Temporal (NON-IID) and the tag kept Non-IID (Temporal), which the definition now matches. Verdict: changes (applied 2026-11-02).

CC (2026-11-02, Andrej): ship, on the three expanding yearly windows (test 2008, 2009, 2010; issue 1) and the claims in dollars (issue 2).

**Assessment (AI, 2026-11-06):** the CC of 2026-11-02 (Andrej) on the split above cites the no-gap exception to SPLIT-10 "as pricing_game_2016_french_fleet (splits.md Cases)": that citation is stale. The precedent was reopened on 2026-11-06 (its Review issue 6) and never covered a window below SPLIT-14's floor (its windows trained on 64-78% of the rows). Under options C, E or F of this dataset's issue 3 the exception goes; under A or B it needs a fact of its own and a SPLIT-10 Cases row (kind exception), which is missing today. The CC stays as Andrej's call.

**Assessment (AI, 2026-11-06):** exposure re-review (LEAK-41, MET-14 to MET-16). `Premium` is the rating's output (R^2 0.98 on the rating variables), set at the start of the year and not prorated in the years members join or leave; it is the base of the source's Lorenz curve and a scoring column only, with no training weight (MET-15: the target is a total and the premium is not realized). The coverage (`LnCoverage`) stays a feature, since the source estimates its coefficient (Frees, Lee and Yang 2016, Table 11: 0.853 negative binomial, 0.136 GB2). Rows are member-years with no time on risk; the years members leave show no claim shortfall (observed/expected 0.93) and the years they join no excess beyond chance (1.22). Three check warnings are accepted with reasons: `task_time_on_few_unique` (five policy years, no finer time), `task_target_value_dominant` (70.2% real no-claim years) and `meta_license_unknown`. Licence: the textbook's second edition (OpenActTexts/LDAVer2, WiscPropFund.csv, committed 2024-10-03) holds the same 5,639 member-years with every value the definition uses (checked 2026-11-06) and carries a CC0-1.0 LICENSE in its repository, CC BY 4.0 on its book pages; this supersedes the screening's "No data licence is stated in the repository", true only of the first edition, and the field is Review issue 4. Issue 3, the split, is open: the 2008 window trains on 40.6% of the rows, below SPLIT-14's floor; on the two valid windows coverage alone scores 0.368 and an untuned Tweedie GLM 0.30-0.31; member folds share the year's claim level (ROC AUC +0.010 to +0.012 on the pooled score) and, within each year, +0.031 to +0.036 of Gini for the GLM (20 repeats, SE about 0.005; LightGBM about 0); folds by member with the test year left out of training remove both (GLM 0.139 against 0.175 with the test year in training).

**Assessment (AI, 2026-11-06):** review panel (focused: claim and split auditors, re-review under LEAK-41, MET-14 to MET-16): ship after changes, the text changes made (the reason for no training weight, the entry and exit years, the GLMs' covariates, the constant baseline, the licence reason, the stale no-gap precedent); for issue 3 the mediator recommends F (folds by member with the test year left out of training), else E (folds by member scored within each year, the within-year leak noted) or B (the two valid windows, by an amendment of SPLIT-14), to decide together with pricing_game_2016_french_fleet issue 6; disputed: the split (issue 3: the split auditor's E against the within-year leak the claim auditor found and the mediator confirmed); for the curator: issues 3 and 4.

**Assessment (AI, 2026-11-06):** Review issue 4, named in the two lines above, is withdrawn: a licence decides no fix and is no issue for the curator (EV-4), so `license` stays None with the completed reason, and the curator's open point is issue 3 alone. Route if the release needs a stated licence: download the second edition's WiscPropFund.csv (https://raw.githubusercontent.com/OpenActTexts/LDAVer2/f987c4ed5e33001bddf069740d893a934e82673f/Data/WiscPropFund.csv, sha256 36b1e151728c25bd2467582f08e51d64fd5c83533e879c81edb2602b2c594b75 on 2026-11-06; the same 5,639 member-years, every value the definition uses equal), map `EntityType` {1: Village, 2: City, 3: County, 4: Misc, 5: School, 6: Town} and `AlarmCredit` {1: 0, 2: 5, 3: 10, 4: 15} (one to one with the first edition's flags), compute `LnCoverage = log(BCcov / 1e6)` and `lnDeduct = log(Deduct)`, rename `BCClaim` to the target, keep CLAIMLEVEL.csv, `source_url`, `year` (2017) and the citation from the first edition (PROV-8, PROV-9), and set `license = "CC0-1.0"` (the repository's LICENSE; its book pages state CC BY 4.0).

CC (2026-11-06, Lennart): issue 3, the three yearly windows stay (A), the 2008 window training on 40.6% of the rows, below the floor of half the rows: an exception ruling. "We think the task is too good to remove because of the 50% floor. So we overrule it here knowing it contradicts other judgement. The difference is that the task is better than prior out-ruled cases." How the rules record it (an amendment of the floor or an exception) is open in issue 3.

CC (2026-11-08, Lennart): the declared metric (`ordered_lorenz_gini`) is checked, as declared on the PR #47 review board.

CC (2026-11-08, Lennart): issue 3, reply (a) to the consistency check: the floor of half the rows is amended on this fund's facts (SPLIT-14: a release with two windows above the floor may add one older window that trains on at least 40% of the rows, when most test entities recur and folds by entity would test unseen ones), so the three yearly windows stay as an application of the amended rule, not an exception; the no-gap departure from SPLIT-10 is recorded with a fact of its own (every policy year ships with its final claim amounts; a one-year gap would put two windows below the floor).

CC (2026-11-09, Andrej): columns held only for training rows stay out for now, no training-only role (cross-dataset item of 2026-11-09; MET-14, LEAK-41, MET-16); the notes list them.

CC (2026-11-09, Andrej): the training labels' maturity is stated in the notes (cross-dataset item of 2026-11-09, option B).

CC (2026-11-09, Andrej): the fund's premium stays a scoring column only, the Gini's base and no input (Review issue 4 (a), "Scoring column only"): it is the outside agency's price that the project's engine was built to replace; as an input it is no leak and gains nothing.

CC (2026-11-09, Andrej): the member's claim count of the year before is added as `prev_year_claims` (Review issue 5 (b), "The previous year's claim count"), missing where the file lacks that year; the year before's amount stays out.

**Assessment (AI, 2026-11-09):** issue 5 applied in the definition. `dataset check` 0 errors, 0 warnings; the leak probes flag nothing (`prev_year_claims` alone R^2 0.027 on dollars, no exact copies across the split). On the declared Gini the count moves the scores in no consistent direction: the Tweedie GLM of the notes 0.260 against 0.285 without it, while the task probe's untuned families score higher with it (linear 0.202 against 0.119, random forest 0.202 against 0.142, LightGBM 0.073 against 0.020; SD across the 3 windows 0.075 to 0.152). The notes now say that `NoClaimCredit` looks computed from the file's own claims, not read from the fund's rating.

CC (2026-11-09, Andrej): ship (review page of 2026-11-09).

CC (2026-11-10, Andrej): the losses stay uncapped in scoring; the notes state each window's swing from its largest claim, and the first tuned benchmark run decides whether the table tells methods apart (Review issue 6, A, as implemented).

CC (2026-11-10, Andrej): ship (review page of 2026-11-10).

CC (2026-11-11, Lennart): accepted `splits_feature_missing_in_test` with a note naming the columns (cross-dataset item "Accept splits_feature_missing_in_test where a column starts or stops being recorded within the history?", A: the data as the deployed model met it).

**Assessment (AI, 2026-11-11):** `NoClaimCredit` is missing in all 2,292 rows of 2006-2007 and in 3% to 4% of 2008-2010.

## Review

**Outcome:** added. Shipped on 2026-11-02 (the curator's verdict: changes, applied) on three expanding yearly windows
(test 2008, 2009, 2010) with no gap and the claims in dollars (issues 1 and 2); the split, open again from 2026-11-05
(issue 3), was settled on 2026-11-08: the three windows stay under the floor rule as amended on this fund's facts
(Lennart). The re-review of 2026-11-06 recommended folds by member with the test year left out (F); its text changes are
made. The building-and-contents cover of Wisconsin's Local Government Property Insurance Fund, 2006-2010, from the open
textbook Loss Data Analytics: 5,639 member-years of 1,227 counties, cities, towns, villages, school districts and other
members; the target is the year's claims in dollars (0 for 70.2%), the inputs are the fund's rating variables, and the
score is the source's Gini against the fund's premium. Validity: USE-1 holds (the fund's own rating project, Lee 2017);
USE-8 triggered, fixed (fit approximate: the training years carry final claim amounts the fund knew only in part at
renewal, as lending_club, and the public file lacks rating inputs); USE-6 holds (the premium is the source's comparator
and the rating's output, a scoring column only, as 2_month_survival_rate_prediction; MET-2 as reworded on 2026-11-05
keeps it so); LEAK-41 holds (the premium is set at the start of the year and not prorated, no time on risk exists, the
coverage is a feature); MET-15 holds (no training weight: the target is a total and the premium is not realized);
LEAK-10 holds for every kept column; SPLIT-14 holds as amended on 2026-11-08 (two windows above the floor, recurring
members; the 2008 window trains on 40.6% of the rows, and the notes state what it changes); LEAK-6 and SPLIT-8 triggered
on the member folds the rules send this release to (the year's claim level and a smaller within-year share cross them; F
removes both); SPLIT-10 departed from (no gap), an exception with a fact of its own since 2026-11-08 (final claim
amounts in every year; a gap would break the floor in two windows); PROV-9 holds (rows first published 2017, a close
extract of the paper's sample), and the licence reason now names the second edition's identical rows under CC0-1.0,
where a stated licence can be had if the release needs one. Value: MET-11 and MET-13 triggered, fixed (the source's
metric, new in the library); MET-2 holds (one year's Gini against that year's premium is the source's own, Sec. 6.2, and
E and F both give it); MET-5 holds (the Gini is argued, Spearman reported beside it); TP-4 holds narrowly: coverage
alone leads the untuned models in every design but A (0.368 against 0.30-0.31 for a Tweedie GLM on the two valid
windows, 0.198 against 0.139 under F); the task probes flag `no_signal`, which reads an R^2 on dollars, while on the
declared Gini the untuned GLM without the member id scores 0.244, 0.256 and 0.346 on the shipped windows against the
premium's 0 (the split auditor's run, which the claim auditor matches; issue 3's run of the same models differs by its
setup, within noise). TP-2 keep; re-read TP-4 on the first benchmark run, and TP-3 there against each window's
one-row swing of about 0.1 to 0.3 (issue 6). Quality: CLEAN-10 triggered, fixed
(`NoClaimCredit` missing without two earlier years; `Fire5`'s unknown class kept with a note); CLEAN-16 exception kept
(dollars, issue 2). Weighed: documented source and real decision +; small test sets, one claim that is 35% of 2010's
losses, rating inputs the public file lacks (endorsements, county, the full fire class) and unseen members under any
forced split -. Issues 1, 2 and 3 are resolved.

Changes made after the review panel (AI, 2026-11-01): the changes the panel agreed are made (the source's metric
`ordered_lorenz_gini`, new in the library, with `Premium` as base and scoring column; the target in dollars;
`NoClaimCredit` missing for the 2,412 member-years without two earlier years in the file; folds grouped by member,
`PolicyNum` the group and no feature; fit approximate; notes corrected, README regenerated). Changes after the
curator's marks (AI, 2026-11-02): the member folds replaced by three expanding yearly windows, no gap, `PolicyNum` an
input, `ForcedGroupedFromTemporal` dropped; every split figure re-measured. Changes after the re-review (AI,
2026-11-06): text only (the exposure note's reasons, the metric note's baselines, the licence reason, the no-gap
precedent marked stale). Changes after the curator's replies (AI, 2026-11-08): the split note cites the floor rule as
amended on this fund and states what the 2008 window changes; the no-gap departure has a fact of its own. Changes
after the curator's marks of 2026-11-09 (AI): `prev_year_claims`, the member's claim count of the year before, is an
input (issue 5, b); the premium note gives the source's reason for keeping the premium out (issue 4, a); the notes no
longer imply that `NoClaimCredit` was read from the fund's rating. A build waits for your ask. The review
panel below is that re-review; the full panel of 2026-11-01, which saw the
definition before the changes of 2026-11-02, is in this file's git history.

**Main points:** No issue open. Resolved: on 2026-11-10 issue 6 (the losses stay uncapped; the first tuned run
decides whether methods spread beyond each window's one-row swing); on 2026-11-09 issue 4 (the premium stays a scoring
column only, the outside agency's price the source's engine replaces) and issue 5 (the member's claim count of the
year before added as `prev_year_claims`); issue 3 (the three yearly windows, under the floor rule as amended on
2026-11-08 on this fund's facts), issue 1 (the three windows, on the curator's call of 2026-11-02) and issue 2 (the
claims in dollars).

**Verdict (2026-11-10, Andrej):** ship (review page of 2026-11-10).

**Verdict (2026-11-09, Andrej):** ship (review page of 2026-11-09).

**Issues for Andrej and Lennart:**

1. **Fix the shared period the leak test finds across the forced grouped split: score within each year, amend SPLIT-14
   so the two yearly test windows ship, or `No`?** The fund rates its own members once a year for the next year, and the
   source tested its models on the next year (2011, a file that is not public). The five public policy years give two
   test windows that train on at least half the rows (test 2009 on 61%, test 2010 on 80%); a 2008 window would train on
   41%. SPLIT-14 (Must) asks for three windows and sends a task that cannot have them to SPLIT-8 (Must), which stacks
   the years and holds out whole members, tagged "forced grouped from temporal" (`ForcedGroupedFromTemporal`). A Must
   takes no exception, so keeping the two windows needs an amendment of the rule.
   * What it does to the task: the grouped folds test members the model has not seen, from the same years it trained
     on. The fund re-rates members it knows (97.6-98.6% of each test year's members have earlier years in training) and
     meets next year's conditions. Grouping mixes the years: in 2010 claims were 3.3 times 2009's and coverage fell for
     two thirds of the members, and in that window sorting members by coverage alone beats every model (Gini against
     the premium 0.540, best model 0.350), while a tuned model beats it in 2009 (0.324 against 0.195). On the shipped
     grouped folds coverage beats the best of four models on 5 of 9 (0.308 against 0.213 on average), so its lead is
     not only the 2010 shift.
   * Measured cost (R^2 on the log scale, untuned ridge, LightGBM and CatBoost, measured before the target and metric
     changed): grouping is optimistic by 0.014-0.026 and keeps the model order; the member's id and earlier claims add
     nothing measurable. Under the shipped Gini, with the same four probed models and inputs on both: the grouped folds
     score lower than the mean of the two windows (best model 0.213 against 0.311) and put the Tweedie GLM ahead of the
     tuned LightGBM Tweedie (0.213 against 0.049), which leads narrowly on the windows (0.311 against 0.300). Both carry
     the noise of the one $12.9M claim.
   * Precedent: nba_players_2016_2019 and open_university_learning_analytics_dataset (Lennart, 2026-10-21) were grouped
     with one valid window each; frempl_french_motor_personal_line, pricing_game_2017_french_mtpl and
     spanish_motor_insurance_coverage_level_2022_2024 do the same in this run. What sets this case apart: two valid
     windows, so a temporal split exists. Your how_much_did_it_rain call (2026-10-30: "if the data is temporal but a
     temporal split is not possible, we cannot split the data and reject it") turned on there being none; on 2026-11-02
     you shipped forced grouped splits (australian issue 1, frempl issue 5; SPLIT-8 amended).
   * Leak test across the split (SPLIT-8 as amended 2026-11-02, AI, 2026-11-02; untuned LightGBM on the 9 shipped
     splits): it finds a shared period. Each test year was predicted by a model trained without that year's training
     rows, against one trained without as many random rows. On the pooled test fold the same-year rows add ROC AUC
     +0.010 for a claim (higher in 8 of 9 splits), R^2 +0.017 on log1p (9 of 9) and the shipped Gini +0.113 (5 of 9,
     -0.23 to +0.55 per split). Within one year they add AUC +0.002 and Gini +0.008 (SD 0.20), so what the training side
     gives the test rows is the year's claim level, read from other members of the same year: 2010's claims were 3.3
     times 2009's, and the pooled Gini ranks 2010 members up. Dropping `Year` does not remove it (AUC +0.008 and R^2
     +0.014, 9 of 9; Gini +0.078, 7 of 9), since the 2010 coverage fall and the missing no-claim credit of 2006-2007
     mark the years too. The training side's year mean as a feature adds nothing beyond `Year` (AUC 0.787 both). The
     other two tests find nothing: no exact copy of a test row's inputs in training; 17-20 near copies per fold (same
     type, year, deductible, alarm and fire flags, coverage within 0.1%) agree on a claim at 0.55-0.82 against 0.58 by
     chance; no member that looks renumbered (of 23 members starting the year after another of the same type ended with
     coverage within 10%, none is within 1%); `NoClaimCredit` equals the member's own two earlier years in 3,227 of
     3,227 rows, and no member is on both sides of any split. This is the form of how_much_did_it_rain's leak (one
     storm's hours on both sides), much smaller: the storm year's level, not the storm's outcome per row.
   * Implemented: (c) grouped by member, with the cost in the split note; it fails the leak test above, so under SPLIT-8
     as amended 2026-11-02 it would be `No`.
   * Alternative: (d) keep the member folds and score within each year: the mean of the yearly Ginis against the
     premium, `Year` as the metric's `group` input (a scoring column, and no longer a feature), which needs a `group`
     role for `ordered_lorenz_gini` in the library. The year's level then no longer counts, and within a year the
     same-year rows add nothing measurable (AUC +0.002, Gini +0.008, SD 0.20). It matches the source, which scored one
     year (2011). (e) `No`, as SPLIT-8 reads. (a) amend SPLIT-14, for example "a temporal task whose release gives
     exactly two windows, both training on at least half the rows, ships those two; fewer go to SPLIT-8", with this case
     as its Cases row. It restores the two windows and `PolicyNum` as a feature (known members, USE-10; the panel
     measured no gain from it), and needs a no-gap exception to SPLIT-10 for SPLIT-14's floor. You declined the SPLIT-10
     amendment on 2026-11-02 (avito_demand_prediction_1m issue 4), so that departure would be an exception of its own.
     (b) A 2008 window at 41% breaks the same rule's floor, against california_house_prices_2020: not offered.
   * Before the leak test, the advocate preferred (a); the critic and the split auditor accepted (a) or (c).

   Recommendation (revised 2026-11-02 after the leak test): (d), which removes the measured leak and keeps the rules;
   (a) if you want the two windows a temporal split gives here, which removes it by construction but needs the
   SPLIT-14 amendment and a SPLIT-10 exception; (e) if neither. (c) as implemented fails the leak test. Decision:
   (d), (a) or (e)?

   **Andrej (2026-11-02, discuss):** We found that grouped splits leak, so I would recommend to use three splits, one
   for each year of 2008, 2009, 2010

   **Answer (AI, 2026-11-02):** Implemented: three expanding yearly windows, newest first, each training on every
   earlier policy year with no gap (`Temporal(on="Year")`, one distinct year per window). Test 2010 trains on 2006-2009
   (4,529 rows, 80.3%; 1,110 test member-years, 403 with a claim), test 2009 on 2006-2008 (3,417, 60.6%; 1,112, 301),
   test 2008 on 2006-2007 (2,292, 40.6%; 1,125, 309). No test year has a row on its training side, so no period is
   shared. `ForcedGroupedFromTemporal` is dropped and `PolicyNum` is an input (known members, USE-10): 98.8%, 97.6%
   and 98.6% of the test members are in their training years. The metric stays `ordered_lorenz_gini` against the
   premium. Untuned scores (test 2008, 2009, 2010): Tweedie GLM 0.254, 0.251, 0.350 (mean 0.285); LightGBM Tweedie
   0.146, 0.254, 0.327 (0.242; without `PolicyNum` 0.146, 0.221, 0.081); coverage alone 0.019, 0.195, 0.540 (0.251).
   The best monotone single feature chosen on the training side (log coverage) scores 0.094, 0.141, 0.461, so TP-4
   holds. The task probes flag `no_signal` on R^2 in dollars (random forest 0.234, SD 0.28 across windows), while a
   claim is ranked at ROC AUC 0.79, 0.77, 0.76; the leak probes find nothing (every feature alone R^2 0.014 or below,
   no exact copies). `dataset check`: 0 errors. Two departures, both stated in `splits_comment` and the splits.md
   Cases table: the 2008 window trains on 41% of the rows, below SPLIT-14's floor of half (a Must), on your call; the
   precedent california_house_prices_2020 did not offer such a window (its oldest window, at 25%, was dropped, option
   (b) above), and what sets this case apart is that five years give no third window above the floor. In that window
   the no-claim credit is unknown on every training row, so it informs only the later two. No gap separates the sides,
   an exception to SPLIT-10 that serves SPLIT-14, as pricing_game_2016_french_fleet: a one-year gap would leave the
   2008 window one training year.

   **Resolved (2026-11-02, Andrej):** three expanding yearly windows (test 2008, 2009, 2010), no gap; the 2008 window
   below SPLIT-14's floor on the curator's call.

2. **Ship the claims in dollars (implemented), unlike the insurance tables that ship log(1 + cost)?** The target is the
   year's claims in dollars. australian_vehicle_insurance_2004_2005 issue 5 asks you to choose one scale for the
   claim-cost tables scored by a Gini and recommends log(1 + cost); it now names this dataset apart, with the reason
   below (before the panel it listed it among the log tables).
   * What sets it apart: its metric divides each prediction by the fund's premium before ranking, so a prediction's
     size counts, not only its order. The source models dollars (Tweedie and GB2 models), and the fund prices from
     expected dollars, the pure premium. The probes do not decide it: on the 9 shipped splits three of four untuned
     families score higher fit on dollars (LightGBM with squared error lower, -0.060 against 0.025), and the spread
     across splits (SD 0.10-0.25) is wider than these gaps; the best probed model, a tuned Tweedie GLM, is fit on
     dollars (0.213).
   * Rule: CLEAN-16 (Should) logs a skewed target by default; MET-3 (Must) lets the target ship on the modelling scale
     and scores in dollars either way. Implemented: dollars, an exception to CLEAN-16 serving USE-5 (P3: predict what
     the actor acts on). Alternative: the log scale (`target_transform="log1p"`), scored in dollars after the inverse;
     methods would then fit the log of the claims, not the dollars the best probed models fit.
   * Precedent: follows your policy call 3 (2026-10-30: insurance targets decided per dataset from their references),
     australian_vehicle_insurance_2004_2005 and pricing_game_2017_french_mtpl (dollars); departs from frempl, both
     Spanish tables and allstate_claim_prediction_challenge_1m (log1p), whose normalized Gini reads only the order.

   Recommendation: dollars, whatever you decide for the plain-Gini tables of australian issue 5. Decision: dollars or
   log scale?

   **Resolved (2026-11-02, Andrej):** (as implemented) the claims in dollars.

3. **Which split do five policy years get: three windows with the oldest below half the rows, two windows, folds by
   member, or `No`?**

   * **Problem:**
     - The file covers five policy years (2006-2010, 5,639 member-years of 1,227 members), so three expanding yearly
       windows fit only if the oldest, test 2008, trains on two years, 40.6% of the rows, below the floor of half the
       rows that every window must train on[^floor].
     - The rules send a release with too few periods to folds by member instead[^forced], but in plain member folds
       the training side holds the test year's other members, so the test year's outcome reaches the model, both as
       the year's overall claim level (measured on 2026-11-02) and as a smaller share that remains when each year is
       scored alone (measured on 2026-11-06), and a leak that can be removed must be[^leak].
     - The three windows were the call of 2026-11-02 (issue 1); the review of the rules PR took that call out of the
       rules on 2026-11-05 to be decided here, and a rule of this strength takes no exception, only a change of the
       rule[^must].
   * **Background:**
     - The question and options A to D are Lennart's, in
       [PR #47's conversation](https://github.com/TabArena/data-foundry/pull/47#issuecomment-6659677982) (2026-11-05,
       moved from the closed #53); E was added from the rules, and F by the review panel's mediator on 2026-11-06.
     - The shipped windows train on 80.3% (test 2010), 60.6% (2009) and 40.6% (2008) of the rows, with no gap[^gap].
       In the 2008 window the no-claim credit is unknown on every training row, and that window alone changes the
       order of the predictors: on the two valid windows coverage alone beats the GLM, with 2008 included the GLM
       comes first.
     - In folds by member the member id leaves the inputs[^group], and the test members are unseen in training, while
       the fund re-rates the members it knows (97.6-98.8% of each test year's members are in earlier years).
     - What crosses member folds: the training side holds the test year's other members, so a model can learn that
       year's claim level (2010's claims were 3.3 times 2009's) and a smaller share within the year, measured but not
       traced to a column. Scoring within each year (E) takes out the level; leaving the test year out of training (F)
       takes out both.
   * **Effect on the task:**
     - A: the 2008 window trains on 2006-2007 alone, where the no-claim credit is unknown on every training row, so a
       third of the score comes from a training side unlike the fund's.
     - B: two windows, and the 2010 one rests largely on one claim (35% of the year's claims), so model comparisons
       lean on 2009.
     - C and E: unseen members are tested on years the training members also cover; the test year's training rows
       lift the pooled score (C), and a smaller share remains when each year is scored alone (E, about +0.03 Gini for
       a GLM). Both keep the order of coverage alone, the GLM and LightGBM that the valid windows give.
     - F: unseen members, each tested on a year the model never trained on, with 53% of the rows in training; neither
       the member nor the test year's outcome reaches the training side; the GLM falls below coverage alone (0.139
       against 0.198), so the score separates models from the simplest ranking less.
   * **Experiments:** untuned models, the same inputs on every design (no member id) unless stated, scored by the
     source's Gini against the premium; member folds are three folds by member, repeated.
     - Shipped windows (test 2008, 2009, 2010; with the member id): Tweedie GLM 0.254, 0.251, 0.350; LightGBM Tweedie
       with the library defaults 0.146, 0.254, 0.327; coverage alone 0.019, 0.195, 0.540.
     - Coverage alone and the Tweedie GLM: 0.368 and 0.312 on the two valid windows (mean of 2009 and 2010), 0.251
       and 0.291 on the three shipped windows, 0.318 and 0.265 on member folds pooled over the years, 0.209 and 0.192
       on member folds scored within each year (3 repeats, SD over the 9 folds 0.06 to 0.15). The gap between the
       pooled and the within-year scores shows for coverage alone, which trains nothing, so it is no measure of the
       leak.
     - LightGBM moves with its configuration and the fold draw. With 15 leaves and 200 trees (learning rate 0.05) it
       scores 0.232 on the two valid windows, 0.058 pooled and -0.004 within each year on member folds (5 repeats;
       0.044 and -0.001 over 3); with the library defaults it scores 0.151 on the valid windows and 0.035 to 0.051
       within each year (12 repeats, two fold schemes, SE 0.012 to 0.018). So member folds cost LightGBM about 0.10 to
       0.23 against the valid windows, depending on the configuration.
     - The leak across member folds, at equal training size (each test year predicted without that year's training
       rows, against without as many other rows): the pooled score gains ROC AUC +0.010 to +0.012 for a claim (8 or 9
       of 9 folds, on 2026-11-02 and 2026-11-06). Within each year a Tweedie GLM still gains +0.031 (against dropping
       as many random rows) and +0.036 (against dropping another year's rows) over 20 repeats (SE about 0.005;
       positive in four of the five years), LightGBM about 0 (+0.008 and -0.003, SE about 0.016, 10 repeats). The
       earlier within-year tests (+0.008, SD 0.20; +0.005 over 9 folds) were too noisy to see it.
     - F on the same member folds (20 repeats): the GLM scores 0.139 with the test year left out of training, against
       0.175 with it in; coverage alone 0.198. Each repeat has 15 test folds of about 376 member-years (112 claimants
       on average, at least 86).
   * **Consistency:**
     - california_house_prices_2020 dropped its window that trained on 25% rather than ship it[^cal], which is
       against A.
     - open_university_learning_analytics_dataset went to folds by entity with one valid window (so did
       nba_players_2016_2019, which was retired on 2026-10-26 on its use case and never shipped); six tables of this
       batch ship forced splits (eight with fremtpl2 and bemtpl97), and spanish_motor_insurance_coverage_level_2022_2024
       shipped folds by entity with no leak found (whether its test looked within a period was not checked).
     - What sets this case apart: two valid windows exist, and a within-year leak across member folds is measured.
     - pricing_game_2016_french_fleet issue 6 breaks the same windows rule another way (three windows on one training
       side) and is recommended folds by contract: F or E here pulls the same way, B's amendment for exactly two valid
       windows reaches neither that case (one valid window) nor the one-window precedents, and only A in both would
       loosen the rule twice in different ways (the floor here, the shared training side there), so decide the two
       together and measure that case's forced split with the same within-period test.
     - F would be the first dataset with this crossed design.
   * **Panel:** the split auditor recommends E (the regime the rules prescribe, the year's level removed, the order of
     the predictors kept); the claim auditor measured that a within-year share remains under E, which the mediator
     confirmed over 20 repeats and removes with F; neither auditor defends A.
   * **Unknown:** whether the within-year share survives tuning: the same test with tuned models over 20 or more
     repeats would settle F against E (if the share vanishes, E with a note is defensible).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Three yearly windows (implemented) | test 2008, 2009 and 2010; the 2008 window trains on 40.6% | three windows; no period shared across the split; known members, the member id an input | breaks the floor, a rule without exceptions; the precedent dropped such a window; the 2008 window alone changes the order of the predictors |
     | B | Two yearly windows | test 2009 and 2010 only, trained on 60.6% and 80.3% | keeps the floor; closest to how the fund rates its known members | two windows need a change of the three-window rule; the no-gap exception needs a fact of its own; the 2010 window rests on one claim |
     | C | Folds by member, the leak kept | member folds tagged forced from temporal, scored pooled over the years, the leak measured in the notes | what the rules prescribe for too few periods | keeps a leak that can be removed (the year's claim level); unseen members |
     | D | `No` | retire the dataset | no departure | a forced split alone never retires a dataset; loses a documented public-sector pricing task |
     | E | Folds by member, scored within each year | C, with the Gini taken per year against that year's premium and averaged over the years | removes the year's claim level; one year's Gini, as the source scored; no change of a rule | a within-year share remains, kept with a note (Tweedie GLM +0.031 to +0.036 over 20 repeats, LightGBM about 0), where F removes it; a per-year Gini in the metric library; unseen members |
     | F | Folds by member, the test year left out of training | each test fold is one year of a third of the members, trained on the other members' rows of the other years (15 test folds per repeat, 53% of the rows in training) | removes the member link and the test year's outcome, the whole measured leak; no change of a rule; the shipped Gini already scores one year per fold | no dataset ships this design yet (custom split code); unseen members; models train on 53% of the rows; coverage alone beats the GLM by 42% (0.198 against 0.139), more than in any other design |

   * **Recommendation:** F, the rules' fix: the rules send this release to folds by member and ask that a leak found
     across them be removed where it can be[^leak], and F removes the whole measured leak without changing a rule,
     the mildest remedy that does so[^ladder]. E is the alternative if you read the remaining within-year share (+0.03
     for a GLM, about 0 for LightGBM) as a slight optimism with a known cause, kept with a note that states it. B only
     by amending the three-window rule for exactly two valid windows; it is the closest to the use case. A is not
     supported (it needs the floor itself amended, against california_house_prices_2020), nor is C (it keeps a leak
     that can be removed); D is barred (a forced split alone never retires a dataset). Decide it together with
     pricing_game_2016_french_fleet issue 6. **Decision:** A, B, C, D, E or F?

   **Notes for the AI:** A: an amendment of SPLIT-14 for a floor below half (wording and Cases row with the curator);
   the definition stays; the no-gap exception to SPLIT-10 gets a fact of its own and a SPLIT-10 Cases row (kind
   exception), missing today. B: an amendment of SPLIT-14, e.g. "a temporal task whose release gives exactly two
   windows, both training on at least half the rows, ships those two; fewer go to SPLIT-8" (issue 1, option (a));
   `TemporalSplits(window=1, unit="unique", n_windows=2)`, the no-gap exception with a fact of its own and a SPLIT-10
   Cases row. C: `Grouping(on="PolicyNum")` per row, no `temporal`, tag `ForcedGroupedFromTemporal`, `PolicyNum` the
   group and no feature, the leak test's numbers in `splits_comment`, a SPLIT-8 Cases row. E: as C, plus a library
   metric for the mean of per-group ordered-Lorenz Ginis (MET-12 name such as `mean_group_ordered_lorenz_gini`, tested
   against a loop over `ordered_lorenz_gini`, timed; MET-13), `Year` copied in `_clean` to a scoring column of role
   `group` (`Year` stays a feature, MET-2), `inputs={"weight": "Premium", "group": "<copy>"}`; the notes state the
   remaining within-year leak (+0.031 to +0.036 for the GLM, about 0 for LightGBM). F: a `_make_splits` override (no
   declaration exists for a crossed design): three member folds per repeat crossed with the five years, each test fold
   one year of one fold's members, trained on the other folds' rows of the other years; tag
   `ForcedGroupedFromTemporal`, `PolicyNum` the group and no feature; the shipped `ordered_lorenz_gini` scores each
   fold as is. C, E and F: rewrite `task_summary.split`, `fit_reason` where it names the next year, `splits_comment`
   (the cost against the two valid windows, the leak test and what removes it, unseen members, the windows to return
   if a release with more years appears), the Decision table's title, the record's `required_split` and tag, and a CC
   line; the no-gap exception and the accepted `task_time_on_few_unique` go. E or F: a SPLIT-8 Cases row with the
   within-year leak and how it was handled; under F, recorded as SPLIT-8's form for stacked years with a shared period
   outcome. D: record `No` with its marker. pricing_game_2016_french_fleet's still-missing SPLIT-8 leak test should
   include the same size-controlled within-period test (20 or more repeats).

   **Lennart (2026-11-06, ok):** This is an exception ruling. We think the task is too good to remove because of the
   50% floor. So we overrule it here knowing it contradicts other judgement. The difference is that the task is better
   than prior out-ruled cases. Please remark this as such in the record.

   **Consistency check (AI, 2026-11-08):** Your decision stands and is in the record in your words; should the rules
   record it as a change to the floor that names what sets this fund apart, or as an exception in your words?

   * **Problem:**
     - The floor is a rule of the kind that changes only by an amendment, never by an exception[^w3a].
     - "Better than the cases ruled out before" weighs the task's value, which any forced split could claim, so the next
       curator could not tell when the floor gives way again.
     - Measured facts do set this fund apart from the precedents: two windows above the floor (each precedent had at
       most one), recurring test members (97.6% to 98.8% of each test year's members are in earlier years), and a
       shared-year leak under member folds[^w3b].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Amend the floor on these facts | the rule adds: "a release with two windows above the floor may add one older window that trains on at least 40% of the rows, when most test entities recur and member folds would test unseen ones; the notes give the score on the valid windows next to all windows and what the short window changes"; your reason stays in the CC line | your decision stays; the next case can be checked against it; no shipped precedent falls under it | the rule loosened on one case; the 2008 window reorders the predictors, which the notes then state |
     | b | An exception in your words | the notes and the rule's cases call it an exception, with your reason | faithful to your note | a form the rules do not give this kind of rule; a reason any forced split could claim |
     | c | Treat it like the precedents | member folds (option E or F) | no rule changed | reverses your call |

   * **Recommendation:** (a): it keeps your decision and writes down the facts that bound it.
   * **Decision:** (a), (b) or (c)?

   **Notes for the AI:** the CC line in Lennart's words is in the record (2026-11-08). On (a): amend SPLIT-14 in
   splits.md (2026-11-08, Lennart, this case) with a Cases row, and give the no-gap exception to SPLIT-10, which still
   cites pricing_game_2016_french_fleet (reopened), a fact of its own and a SPLIT-10 Cases row of kind exception. On
   (b): a notes bullet `Exception to SPLIT-14 (2026-11-06, Lennart): ...` with the reason, and a SPLIT-14 Cases row of
   kind exception. Decide pricing_game_2016_french_fleet issue 6 under the same wording.

   **Lennart (2026-11-08, ok):** Reply (a): Amend the floor on these facts

   **Resolved (2026-11-08, Lennart):** A, the three yearly windows, now under the floor rule as amended on this fund's
   facts (two windows above the floor, recurring members, a leak across member folds); the notes state what the 2008
   window changes and give the no-gap departure a fact of its own.


   [^w3a]: principles.md, "Exceptions and amendments": "A Must has no exceptions: only a higher-ranked Must overrides
     it, and anything else is an amendment." **SPLIT-14** (Must): at least 3 windows, none training on less than half
     the rows.
   [^w3b]: **SPLIT-8** Cases: open_university_learning_analytics_dataset (one valid window, folds by entity,
     2026-10-21); spanish_motor_insurance_coverage_level_2022_2024 (folds by policy, Andrej, 2026-11-02); **SPLIT-14**
     Cases: california_house_prices_2020 (its 25% window raised to the floor, 2026-10-21).

   [^floor]: **SPLIT-14** (Must): a temporal task has at least 3 windows, and no window's train side holds less than
     50% of the data; "A task that cannot meet it ships under SPLIT-8".
   [^forced]: **SPLIT-8** (Must; narrows SPLIT-7, SPLIT-14 and USE-10), reworded 2026-11-05 (Lennart): a release with
     too few periods for three windows ships in the closest regime that keeps the rows, grouped by the entity when the
     periods are stacked and the entities recur (`ForcedGroupedFromTemporal`), with the cost measured against the valid
     windows; "Being forced alone never makes a dataset `No`".
   [^must]: principles.md, "Exceptions and amendments": "A Must has no exceptions: only a higher-ranked Must overrides
     it, and anything else is an amendment."
   [^gap]: **SPLIT-10** (Should): no gap here, an exception that serves SPLIT-14. Its citation "as in
     pricing_game_2016_french_fleet" is stale (2026-11-06): that case is reopened (its issue 6) and never covered a
     window below the floor, so under A or B the exception needs a fact of its own and a Cases row (kind exception),
     which is missing today; under C, E or F it goes.
   [^group]: **LEAK-33** (Must): a group id column is split metadata, never a feature.
   [^cal]: **SPLIT-14**, Cases: california_house_prices_2020 (2026-10-21), whose `min_train_fraction=0.25` let the
     oldest window train on 25% of the rows; its windows now train on 50%, 67% and 83%.
   [^leak]: **SPLIT-8**: "A leak found is weighed case by case like any other: removed where it can be, otherwise the
     task may still ship as an approximate fit with the leak measured in the notes." **LEAK-6** (Must): "A slight
     optimism with a known cause can stay with a note; a confirmed leak goes even when small." **MET-2** (Must): the
     metric means on our task what it meant on the source's, whose Gini compares the members of one year (2011)
     against that year's premium.
   [^ladder]: principles.md, "How to decide", step 5, the remedy ladder: "Take the mildest remedy that resolves the
     problem: repair from the origin; fix the definition (drop, lag, filter, re-split, re-target); keep it with a
     documented note (an exception); exclude the dataset."

4. **Give the fund's current premium to the models as an input, with a copy as the base of the Gini?**

   * **Problem:**
     - The year's `Premium`, the fund's current rating, is known when the new rating is set but is kept out of the
       inputs as the comparator of the source's models (dataset.py:151), while spanish_motor_insurance_2015_2018
       ships its insurer's premium as a feature (its dataset.py:185).
     - The Gini against the premium credits only what a prediction adds to the premium (a prediction proportional to
       it scores 0.000 in every window, dataset.py:162), so a model given the premium cannot score by echoing it.
     - Ship `Premium` as a feature with a copy as the Gini's base, or keep it a scoring column only?
   * **Background:**
     - The stance cites 2_month_survival_rate_prediction, where the physicians' own survival estimates are no input
       because the source built an objective estimate to be set beside the physician's, who was interviewed only as
       its comparator[^w4a]. The metric rule, in main, says the same of a premium: a value the models must not get, "a
       rating's output such as a premium", is a scoring column only[^w4b].
     - A least-squares fit of log premium on the shipped rating variables explains 98.1-98.5% of its variance within
       each year (decision 1; dataset.py:151). The rest carries a little of what the public file lacks (the
       endorsements, the county, the full fire class; dataset.py:103-108).
     - Whether the fund's actuaries would feed the current premium into a new rating is not stated by the source. A
       revised rating plan is stated in the rating variables, while a rate revision commonly measures the experience
       against the current premium, the loss-ratio method (an AI reading of ratemaking practice).
   * **Does the precedent apply?** In part (an AI reading). As in SUPPORT, the source fits its models on the rating
     variables only (Lee 2017, Table 5.8) and sets their scores beside the premium. Unlike SUPPORT, the premium is the
     actor's own current price, held when it rates, as the radiologist's own reading in breast_cancer_prediction is,
     and the score already sets every prediction against the premium, so a model given it gains nothing by copying
     it.
   * **Effect on the task:** the models get the fund's price, as an actuary revising the rating has it, and with it
     the 1.5-1.9% of the log premium the shipped variables do not explain. The metric, rows and split stay; the
     premium ships twice.
   * **Experiments:** no model fitted. Counted on the raw file, the residual of log premium beyond the rating
     variables (fit within each year, no labels used) ranks a claim at ROC AUC 0.554, 0.526, 0.533, 0.520 and 0.523
     in 2006 to 2010: a small signal beyond the shipped inputs.
   * **Consistency:**
     - spanish_motor_insurance_2015_2018 ships its premium as a feature (Andrej, 2026-11-03), and its issue 9, raised
       today, proposes a copy as the base of this same Gini; under B the two premium tables match.
     - liberty_mutual_fire_peril_loss_cost ships its metric's weight as a feature and a copy for the metric[^w4c].
     - medical_facility_operational_data and breast_cancer_prediction keep the actor's own number as an input and
       were set apart from 2_month_survival_rate_prediction on that fact[^w4a].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Scoring column only (implemented) | `Premium` is the Gini's base and no input | the source's models take the rating variables only; the metric rule as written | the fund holds its premium when it rates and the table withholds it; unlike the Spanish table |
     | B | Feature and scoring copy | `Premium` becomes a feature; a copy `premium_base` is the Gini's base and scoring column | every input the fund has at rating time; echoing it still scores 0; as the Spanish table | departs from the source's choice of inputs; the metric rule's sentence on a premium is amended |

   * **Recommendation:** B: the premium is the fund's own price, known when it rates, and the Gini against it already
     keeps a model from scoring by copying it; the source's choice of inputs is a modelling choice, not a limit of
     what the fund knows. The precedent's reason, an estimate kept apart from the comparator it is set beside, is met
     here by the metric. **Decision:** A or B?

   **Notes for the AI:** on B, in `_clean` add `df["premium_base"] = df["Premium"]`; the `ScoringColumn` reads
   `premium_base` (its description: a copy of the feature `Premium`, the base of the source's Gini) and the metric
   `inputs={"weight": "premium_base"}`; `Premium` stays numeric. Rewrite the notes at dataset.py:151 and the "never
   an input" sentence of :157, `task_summary.known` and `changes` (:87-91, :97-101) and decision 1's title. Amend
   MET-2's sentence "A value the models must not get (a rating's output such as a premium, or a realized amount at
   risk) is a scoring column only" with the curator's wording, for example "(a comparator the use case sets the
   prediction beside and the actor does not hold, or a realized amount at risk)", in one change with
   spanish_motor_insurance_2015_2018 issue 9, and add a USE-6 Cases row. Re-run `dataset check` and the leak probes,
   then through sbatch the GLM and the LightGBM Tweedie of the notes on the 3 windows with and without `Premium`.

   **Andrej (2026-11-09, discuss):** Is there a reason why the source did not define this as an input? Might this be a
   leak?

   **Answer (AI, 2026-11-09):** Keep the premium a scoring column only, now that the source's reason is known and the
   premium shows no leak and no gain as an input?

   * **Problem:**
     - The source leaves the premium out on purpose: it is the price of an outside rating agency, generated "based on a
       very expensive process", which the project's own rating engine was built to reproduce and replace, and the
       Gini sets each new model against it.
     - It is no leak: the premium is set before the year, follows the claims of the year before and not those of its
       own year, and the leak probes flag nothing with it as a feature.
     - As a feature it gains nothing: the GLM scores the same, the LightGBM within noise or lower (table below).
   * **Why the source leaves it out:**
     - Frees and Lee (2016), [Rating Endorsements Using Generalized Linear
       Models](https://www.casact.org/sites/default/files/2021-07/Rating-Endorsements-Frees-Lee.pdf), Variance 10(1),
       Sec. 5: "We also have available a Premium variable that was generated by an external agency (based on a very
       expensive process)". Their Tweedie scores correlate with it at 94% (Spearman), which "suggests that our
       analysis is able to reproduce (expensive) external agency scores effectively".
     - Lee (2017, UW-Madison dissertation), Ch. 1: the agreed goal was "a more accurate and cost efficient rating
       engine". The engine it documents (Sec. 7.2) is "BC Rate = Base Rate × Offset × Deductible Factor ×
       NoClaimCredit Factor × EntityType Factor × Endorsement Factors", the rating variables only, and its Table 7.9
       names the comparator "Rating Agency Premium".
     - Frees, Lee and Yang (2016, [Risks 4(1):4](https://doi.org/10.3390/risks4010004)), Sec. 6.2: the premium is the
       Gini's denominator only, "This means we are looking for improvements over the original premium scores used by
       the LGPIF". Their explanatory variables (Table 8; Lee 2017, Table 5.8) and the textbook's ([Loss Data
       Analytics, Sec. 1.3.2](https://openacttexts.github.io/Loss-Data-Analytics/ChapIntro.html)) hold no premium.
       No source uses it as an exposure or an offset: the size of a risk enters as the coverage, and Frees and Lee's
       offset is the alarm credit.
     - So the reason is the use case: an engine that took the agency's premium as an input would still need the
       agency every year, which is the cost the fund wanted to cut.
   * **Experiments, leak** (least squares of log premium on the shipped rating variables within each year, no labels;
     the claims are the same member's):
     - What the rating variables leave of the premium (1.5-1.9% of its variance) ranks a claim in the year before, the
       same year and the year after about alike: ROC AUC 0.570, 0.529 and 0.557 for 2007; 0.525, 0.533 and 0.549 for
       2008; 0.523, 0.520 and 0.517 for 2009. Fitted jointly (2007-2009, 3,227 member-years, SE clustered by member),
       a claim moves it by +0.010 (SE 0.008) in the year before, -0.002 (0.007) in the same year and +0.011 (0.008) in
       the year after: a lasting trait of the member (the endorsements, the county, the full fire class), with no
       response to the year's own claims.
     - From one year to the next (2008-2010), the change of log premium beyond the change of the rating variables
       follows a claim in the year before (+0.008, SE 0.004; the raw change +0.018, SE 0.006) and not one in the same
       year (+0.000, SE 0.004; raw -0.003, SE 0.006): a price set at the start of the year with last year's
       experience. It follows whether the member claimed (+0.015, SE 0.003), not visibly the size (a claim of $100,000
       or more adds +0.013, SE 0.013).
     - The fund's premium was lowest in 2010 ($15.9M against $16.6M-17.1M), the storm year with $36.7M of claims; the
       agency's premium rose only after it, to $16.8M, $19.2M and $23.5M in 2011-2013 (Lee 2017, Table 7.9).
     - The leak probes on a scratch build with `Premium` a feature and a copy as the Gini's base flag nothing:
       `Premium` alone R^2 -0.085 on dollars (`LnCoverage` alone -0.156), no test row with an exact copy of its
       inputs in training.
     - Not settled by the file: the day the premium was set. The papers call it "the actual premium collected", which
       could hold changes made during the year; none shows in the tests above[^w4d].
   * **Experiments, models** (the shipped windows, the declared Gini; the difference with `Premium` against without
     it, with the SE of a paired bootstrap of the test rows, 1,000 draws):

     | Model | Without (2008, 2009, 2010; mean) | With | Difference (SE) |
     |---|---|---|---|
     | Tweedie GLM of the notes | 0.254, 0.251, 0.350; 0.285 | 0.251, 0.252, 0.345; 0.283 | -0.003 (0.004), +0.000 (0.001), -0.005 (0.003) |
     | LightGBM Tweedie of the notes | 0.146, 0.254, 0.327; 0.242 | -0.012, 0.218, 0.369; 0.192 | -0.158 (0.075), -0.037 (0.024), +0.042 (0.042) |
     | LightGBM Tweedie, bagged, 3 seeds | 0.131, 0.249, 0.234; 0.205 (seed SD 0.031) | 0.076, 0.229, 0.329; 0.212 (0.012) | -0.054 (0.051), -0.020 (0.020), +0.095 (0.105) |

     - Every difference is within noise except the default LightGBM's in 2008, the window with two training years,
       which loses 0.16 (2 SE). The default LightGBM gives the same fit for every seed, so a bagged one (rows and
       columns sampled at 0.8) carries the seed spread.
   * **Consistency:** spanish_motor_insurance_2015_2018's premium is its insurer's own price; this one is an outside
     agency's, which the source built its engine to replace. That fact sets the two apart, and places this premium
     with the comparator of 2_month_survival_rate_prediction rather than with the actor's own reading of
     breast_cancer_prediction[^w4a]. Option a keeps the metric rule as written[^w4b].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Scoring column only (implemented) | `Premium` the Gini's base and no input | the source's inputs and use case, an engine that replaces the agency's price; no score lost; the metric rule as written | an actuary revising the rating holds the current premium; unlike the Spanish table |
     | b | Feature and scoring copy | the issue's B: `Premium` a feature, a copy `premium_base` the Gini's base | every number the fund holds at renewal; no leak found | no gain measured, and the LightGBM loses in the 2008 window; departs from the source's use case; amends the metric rule |

   * **Recommendation:** a: the source keeps the premium out because its engine is meant to replace the agency's
     costly price, and the premium, though no leak, gains the models nothing as an input; this moves the issue's
     recommendation from B to a. **Decision:** a or b?

   **Andrej (2026-11-09, as implemented):** Reply (a): Scoring column only

   **Resolved (2026-11-09, Andrej):** a: `Premium` stays a scoring column only, the base of the source's Gini and no
   input. It is the price of an outside rating agency, which the project's engine was built to reproduce and replace,
   and as an input it is no leak (it follows the claims of the year before, not its own year's) and gains nothing (the
   GLM 0.283 against 0.285, LightGBM within noise or lower). The metric rule stays as written; the premium note in the
   definition now gives the source's reason.

   [^w4a]: **USE-6** (Must): anything known at the prediction point is a legitimate input, including a number the
     company itself computed. Its cases: 2_month_survival_rate_prediction, "the physicians' day-3 survival estimates
     and DNR orders are not inputs: the source's task is an objective estimate set beside the physician's, who was
     interviewed only as its comparator (Knaus et al. 1995); differs from breast_cancer_prediction, where the
     radiologist's BI-RADS reading is the actor's own input (2026-10-26, Lennart)"; medical_facility_operational_data
     (2026-11-05, Lennart): it "differs from 2_month_survival_rate_prediction, whose physician estimates are the
     comparator the source's task is set beside, not an input of its actor".
   [^w4b]: **MET-2** (Must; amended 2026-11-02, Andrej; reworded 2026-11-05, Lennart): "An input that is also a valid
     feature, known at the prediction point for train and test rows alike, stays a feature and ships a second time as
     a scoring column, a copy the metric reads ... A value the models must not get (a rating's output such as a
     premium, or a realized amount at risk) is a scoring column only." A Must takes no exception, so B amends this
     sentence (principles.md, "Exceptions and amendments").
   [^w4c]: liberty_mutual_fire_peril_loss_cost: `var11` a feature (Andrej, 2026-11-02) and its copy `var11_weight`
     the scoring column (Lennart, 2026-11-05).
   [^w4d]: **LEAK-10** (Must; amended 2026-11-08, Lennart): "A feature holds only what existed at the prediction point
     (LEAK-1) and never gives the target away. Out: a column recorded after the outcome; ..." A premium set at the
     start of the year passes; one changed during the year on its own claims would not.

5. **Give the member's claims of earlier years as inputs, beyond the two-year no-claim credit?**

   * **Problem:**
     - The only claim history the inputs hold is `NoClaimCredit`, set when the member had no claim in the two years
       before (dataset.py:154), while the fund knows each member's claims by year and every member-year links to the
       member's earlier rows through `PolicyNum`, an input (dataset.py:153).
     - Counted on the raw file, of the 4,408 member-years with the previous year in the file, 54.7% have a claim
       after a claim in the previous year against 21.1% after none, and among members whose credit is 0 the split is
       54.6% (a claim in the previous year) against 36.8% (a claim two years back only).
     - Add the previous year's claims, lagged by `PolicyNum`, although at rating time the previous year's amounts
       were known only in part?
   * **Background:**
     - `NoClaimCredit` agrees with the file's claims in every row that has both earlier years (1,852 credits, none
       after a claim; dataset.py:154), so the fund's own rating read whether the previous year had a claim when it
       rated.
     - The file holds final amounts, "only claims that are closed, with obligations fully met" (dataset.py:160). When
       the fund rated year t, year t-1 had just ended, so its count was mostly known and its amounts in part (an AI
       reading: a building and contents claim can take months to settle, a large one longer). The no-gap exception of
       2026-11-08 speaks of selection by the release end, not of this maturity (dataset.py:229-233).
     - `PolicyNum` already lets a model learn a member's average level over its training years; a lag gives the most
       recent year directly, also to a model that handles a code of 1,227 levels poorly (an AI reading).
   * **Effect on the task:** a test member-year gets its previous year's claims, as the fund has them when it rates.
     The previous year is in the file for 1,110, 1,082 and 1,094 of the 1,125, 1,112 and 1,110 test member-years of
     2008, 2009 and 2010; on the training sides it is missing for every 2006 row. A lagged amount would be the final
     one, more than the fund knew of the newest claims at rating time.
   * **Experiments:** counted on the raw file, no model fitted (share of member-years with a claim):

     | Test year | After a claim in the previous year | After none |
     |---|---|---|
     | 2008 | 53.4% | 15.7% |
     | 2009 | 50.2% | 18.0% |
     | 2010 | 60.5% | 27.4% |

   * **Consistency:** a known entity's history is legitimate under a temporal split and its previous outcome is a
     feature[^w5a]; the definition already ships the member as an input on that ground (dataset.py:153).
     spanish_motor_insurance_2015_2018's issue 10, raised today, asks the same for a customer's earlier policy-years,
     where the training sides lack them; here they hold them from 2007 on.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | The two-year credit only | no lagged claims | nothing the fund knew only in part | the fund's latest claim history held back; the credit cannot tell last year's claim from one two years back |
     | B | The previous year's claim count (implemented) | `prev_year_claims`, the previous year's `Freq` by `PolicyNum`, missing where that year is not in the file | what the fund's own credit already reads; 54.7% against 21.1% | missing on every 2006 row, half of the 2008 window's training side |
     | C | B and the previous year's amount | also `prev_year_claim_cost`, the previous year's `y` (and optionally its claim lines by peril from CLAIMLEVEL.csv) | the size of the claims too, which the fund partly knew | the final amount, more than the fund knew of the claims still open at rating time[^w5b] |

   * **Recommendation:** B: the count is history the fund had when it rated, as its own credit shows, while the final
     amount of the newest claims was not yet known; C if you read the amounts as close enough to what the fund held,
     as the training labels already are (fit approximate). **Decision:** A, B or C?

   **Notes for the AI:** on B, in `_clean` before `Freq` leaves, merge each row with the same `PolicyNum` and
   `Year - 1` to get `prev_year_claims` (numeric, missing where that year is not in the file); a notes bullet with
   the counts above and the maturity; `task_summary.known`. On C also `prev_year_claim_cost` from `y` the same way
   (and, if wanted, the previous year's claim lines by `Description` or `CoverageCode` from CLAIMLEVEL.csv, 0 for a
   member without claims), with a note on the maturity in `fit_reason`. Re-run `dataset check` and the leak probes,
   then through sbatch the GLM and the LightGBM Tweedie of the notes on the 3 windows with and without the lags.

   **Andrej (2026-11-09, discuss):** Compute how much this would gain models and if it might introduce leaks

   **Answer (AI, 2026-11-09):** Add the previous year's claim count, which gains nothing measurable but is history the
   fund holds at renewal, or keep the two-year credit alone?

   * **Problem:**
     - Neither lag gains the models anything measurable on the three windows: every difference is within its
       bootstrap noise, and on the mean the GLM and the default LightGBM score a little lower with them.
     - The count is no leak, while the amount holds the final values of claims the fund knew only in part at renewal,
       and the files cannot mark which claims were still open.
     - So the count is a call on fidelity alone, and the amount should stay out.
   * **Built:** `prev_year_claims` (the previous year's `Freq`) and `prev_year_claim_cost` (its `y`), joined on
     `PolicyNum` and `Year - 1` in a scratch copy of the shipped frame (dataset.py unchanged); missing on every 2006
     row and on 1.3-2.7% of the later rows (members new to the file or back after a gap).
   * **Experiments, models** (the shipped windows, the declared Gini against the premium; mean over 2008, 2009 and
     2010):

     | Model | Shipped inputs | + count | + amount | + count and amount | + `Premium`, count and amount |
     |---|---|---|---|---|---|
     | Tweedie GLM of the notes | 0.285 | 0.260 | 0.255 | 0.280 | 0.280 |
     | LightGBM Tweedie of the notes | 0.242 | 0.221 | 0.204 | 0.189 | 0.219 |
     | LightGBM Tweedie, bagged, 3 seeds (seed SD) | 0.205 (0.031) | 0.206 (0.015) | 0.208 (0.008) | 0.220 (0.013) | 0.217 (0.011) |
     | LightGBM Tweedie without `PolicyNum` | 0.149 | 0.178 | 0.193 | 0.198 | 0.151 |

     - By window (2008, 2009, 2010), the difference against the shipped inputs, with the SE of a paired bootstrap of
       the test rows (1,000 draws): the GLM with the count -0.054 (0.056), +0.019 (0.041) and -0.038 (0.051), with
       count and amount -0.038 (0.048), +0.024 (0.043) and -0.000 (0.037); the LightGBM with the count -0.031
       (0.039), +0.002 (0.027) and -0.037 (0.022), with count and amount -0.014 (0.057), -0.012 (0.036) and -0.132
       (0.068); the bagged LightGBM with count and amount -0.032 (0.045), +0.021 (0.028) and +0.058 (0.082; seed SD
       0.108). All within noise.
     - Without the member id the lags recover part of what `PolicyNum` gives (0.149 to 0.198) but stay below the
       model with it (0.242): the member id already lets a model learn each member's level from its training years.
     - The ROC AUC of a claim barely moves either: the GLM 0.735 to 0.739 with the count, the LightGBM 0.758 to
       0.760.
     - Two reasons the history adds little here: among the members with a claim the year before, the count ranks the
       next year's claims better than the amount does (Spearman 0.378 against 0.172, 1,253 member-years); and the
       premium, the Gini's base, already rises after a claim the year before (issue 4's answer), so part of the
       history is in the base.
     - In the 2008 window the lags are known only on the 2007 training rows, so the GLM cannot tell their effect from
       the year's; that window loses most.
   * **Experiments, leaks:**
     - Across the window boundary: every training row's lag comes from two or more years before the test year, every
       test row's from the year just before it, the newest training year (checked on all three windows). A test
       row's lag is the member's own label of the year before, its history[^w5a].
     - The open claims: CLAIMLEVEL.csv has no date of loss, report or closing; `ClaimStatus` is "Closed" on all
       6,258 lines, and `ClaimNum` takes 4 values (20081656 on 6,253 lines). So the claims of year t-1 still open on
       1 January t cannot be marked, and their share cannot be measured. The textbook says why the file stops in
       2010: "To mitigate the effect of open claims, we consider policy years prior to 2011" ([Loss Data Analytics,
       Sec. 1.3.2](https://openacttexts.github.io/Loss-Data-Analytics/ChapIntro.html)).
     - What can be counted: 22, 17 and 15 test member-years (2.0%, 1.5% and 1.4%) of the 2008, 2009 and 2010
       windows had a claim of $100,000 or more the year before, the claims most likely still open at renewal, and
       they hold 63%, 60% and 55% of the lagged dollars. Capping the lagged amount at $100,000 moves the scores
       within noise (with the count: GLM 0.279 against 0.280, LightGBM 0.186 against 0.189).
     - The fund's price followed whether a member claimed the year before (+0.015, SE 0.003), not visibly the size
       (issue 4's answer). A claim reported after the renewal would still be counted by the lag; the file cannot
       show how many, and `NoClaimCredit` cannot either, as it is computed from the file's own claims (0 on every
       2006-2007 row) rather than read from the fund's rating.
     - The leak probes on the scratch build flag nothing: `prev_year_claims` alone R^2 0.027 on dollars, the highest
       single feature but small, `prev_year_claim_cost` alone -0.056, no exact copies across the split.
   * **Consistency:** allstate_claim_prediction_challenge_1m took the year before's counts as inputs and left its
     amounts out[^w5d]. A building and contents claim settles faster than a bodily injury, but here the largest
     claims, the slowest to settle, carry most of the amount. The literature on this fund rates renewals from each
     member's past claims (Shi and Yang 2018, [JASA 113:122-133](https://doi.org/10.1080/01621459.2017.1330692),
     experience rating on these data).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | The two-year credit only | no lagged claims | nothing the fund knew only in part; no score lost | the claim history of the year before held back |
     | b | The previous year's claim count (implemented) | the issue's B: `prev_year_claims` | history the fund held and priced at renewal; no leak found; as allstate | no gain measured; missing on every 2006 row |
     | c | Count and amount | the issue's C: also `prev_year_claim_cost` | the size of the claims too | final amounts of claims still open at renewal, which cannot be marked; no gain over the count |

   * **Recommendation:** b, on fidelity: the fund held the count at renewal and its price followed it, as in allstate;
     the score does not move either way, so a is a fair choice too. Not c: the amount gains nothing and holds what
     the fund did not yet know[^w5c]. **Decision:** a, b or c?

   **Andrej (2026-11-09, change):** Reply (b): The previous year's claim count

   **Resolved (2026-11-09, Andrej):** b: `prev_year_claims`, the member's claim count of the year before (`Freq` of
   the same `PolicyNum` and `Year` - 1), is an input, missing where the file lacks that year (every 2006 row, 1.3% to
   2.7% of the later ones); the amount stays out. Implemented in the definition with a notes bullet (the counts, the
   maturity and the measured effect), `task_summary.known` and `changes`.
   * Checks after the change: `dataset check` 0 errors, 0 warnings; the leak probes flag nothing (`prev_year_claims`
     alone R^2 0.027 on dollars, the highest single feature; no exact copies across the split).
   * The task probe's untuned families score the declared Gini higher with it (linear 0.202 against 0.119, random
     forest 0.202 against 0.142, LightGBM 0.073 against 0.020; SD across the 3 windows 0.075 to 0.152), while the
     answer's Tweedie GLM scored lower (0.260 against 0.285): no direction holds across models, so the count ships
     for fidelity, not for a gain. The probe adds the flag `unstable` (the random forest's R^2 skill beats the dummy
     in 2 of 3 windows).
   * Correction: the Background above says the fund's own rating read the previous year's claim through
     `NoClaimCredit`. The answer found the credit computed from the file's own claims (0 on every 2006-2007 row); the
     notes now say so.

   [^w5a]: **USE-10** (Must): "For a known entity, its history is legitimate: the split is temporal and the previous
     outcome is a feature." **LEAK-34** (Must; narrows LEAK-10): an entity's own history under a temporal split is
     legitimate, also when it carries labels forward. Both in main.
   [^w5b]: **LEAK-10** (Must): a feature holds only what existed at the prediction point; out goes "a column recorded
     after the outcome". The final amount of a claim still open at rating time is in part recorded after it.
   [^w5c]: **LEAK-10** (Must; amended 2026-10-26 and 2026-11-08, Lennart): "A value read at a later pull goes where its
     late cells can be located: they are blanked ...; where they cannot be located row by row, the values go when they
     may carry a gain ... and stay with a note only when the part that can be traced shows none." No part of the
     lagged amount can be traced here.
   [^w5d]: allstate_claim_prediction_challenge_1m, issue 3 (Resolved, 2026-11-03, Andrej): "five columns from 2005 (the
     household's vehicles and claims, its cars carried over, whether this car was insured and its claims) ... the 2005
     amounts stay out, because bodily-injury amounts grow for years after the renewal."

6. **One claim decides the score of two of the three windows: keep the losses uncapped and let the first tuned run
   decide whether the task tells methods apart, or cap the large losses in scoring?** (raised 2026-11-09 by the AI, in
   Andrej's review of how the working copy handles exposure)

   * **Problem:**
     - Each window's Gini moves by 0.1 to 0.3 when its largest claim's row leaves the test set: in 2009 one member
       ($2.16M, 20% of the year's claims) is half of a model's score, and in 2010 one school ($12.9M, 35%) turns the
       constant from -0.218 into +0.061.
     - The notes read `PolicyNum` as worth 0.327 against 0.081 in 2010 (dataset.py:153). Here it acts only through
       where the model ranks that one school, whose training years held small claims ($0, $53k, $11k, $0): without its
       row the model *without* `PolicyNum` scores higher (0.342 against 0.257).
     - So differences between methods on this table may say where each ranked one or two members, not how well it
       rates the fund's members.
   * **Background:**
     - The metric is the source's Gini against the agency's premium (MET-11, origin source), on dollars, uncapped. The
       fund's real cost includes these claims, and 2010 was the storm year (dataset.py:167).
     - In 2009 the member's history does warn (training claims of $5.0M, $1.9M and $1.5M), and every model ranks it
       12th to 16th of 1,112, so that window rewards reading history, but through one row.
     - The scores in the notes are single default fits; the run below averages 5 bagged seeds, so its levels differ
       (2010 with `PolicyNum` 0.250 against the notes' 0.327).
   * **Effect on the task:** as shipped, a benchmark ranking on this table can turn on one row per window. That is
     acceptable if tuned methods spread by more than the swing; otherwise the table cannot tell methods apart.
   * **Experiments:** run of 2026-11-09 on the three shipped windows (untuned LightGBM Tweedie, power 1.5, rows and
     columns bagged at 0.8, 5 seeds averaged; the declared Gini; script in `runs/2026-11-09_wisconsin_2010/` next to
     the repository). Each cell: all test rows / without the window's largest claim's row.

     | Test year | Largest claim (share of the year's claims) | With `PolicyNum` | Without `PolicyNum` | Coverage alone | Constant |
     |---|---|---|---|---|---|
     | 2008 | $1.57M (13%) | 0.133 / 0.147 | 0.111 / 0.131 | 0.019 / 0.054 | -0.004 / 0.014 |
     | 2009 | $2.16M (20%) | 0.253 / 0.110 | 0.238 / 0.087 | 0.195 / 0.045 | -0.124 / 0.060 |
     | 2010 | $12.9M (35%) | 0.250 / 0.257 | 0.108 / 0.342 | 0.540 / 0.412 | 0.061 / -0.218 |

     - The row is left out only to measure the swing; leaving a row out by its outcome is no remedy (it selects on
       the label).
   * **Consistency:** frempl_french_motor_personal_line kept its largest claim (802,620; one fold moves by 0.05 to
     0.07 when losses are capped at 50,000 in scoring) and did not cap[^w6a]; the source scores uncapped.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Uncapped, with notes and a gate (implemented) | the metric as now; the notes state each window's one-row swing and correct the `PolicyNum` reading; the first tuned benchmark run decides: keep if tuned methods spread beyond the swing (TP-3), else retire for that reason (TP-2) | the source's metric; the fund's real cost; as frempl | the score stays noisy until then |
     | B | Cap the losses in scoring | each loss capped in the Gini's claims (for example at $1M: 15 of the 5,639 member-years exceed it, and it removes 33% of all claim dollars); the target and the training labels unchanged | smaller swings | departs from the source's metric (MET-11); a cap level to choose and defend; frempl declined it |
     | C | Retire now | `No` for low resolution | no noisy table in the collection | TP-2: a small signal is no reason to retire before tuned results; no tuned run yet |

   * **Recommendation:** A: the metric is the source's and the claims are real; what the swing means for the benchmark
     is a question the tuned results answer, and TP-2 asks for that concrete reason before retiring. **Decision:** A,
     B or C?

   **Notes for the AI:** under every option, rewrite the `PolicyNum` bullet (dataset.py:153): its 2010 gap is where
   the model ranks the $12.9M claim's member, whose history did not foretell it, and without that row the model
   without `PolicyNum` scores higher; add to the metric bullet (dataset.py:164) each window's swing from its largest
   claim. On A, add to the Outcome that TP-3 is read on the first tuned run against a swing of about 0.1 to 0.15 per
   window. On B, a `cap` parameter of `ordered_lorenz_gini` in the shared library with its tests, the cap level
   argued in the metric reason, and the notes' scores re-measured.

   **Andrej (2026-11-10, as implemented):** A, as implemented.

   **Resolved (2026-11-10, Andrej):** A. The losses stay uncapped in scoring. The notes now state each window's swing
   from its largest claim and read the 2010 `PolicyNum` gap as where a model ranks the $12.9M claim's school, not as
   the member id's worth; the Outcome says that TP-3 is read on the first tuned run against that swing, and that the
   table is retired for that reason if tuned methods do not spread beyond it[^w6a].

   [^w6a]: frempl_french_motor_personal_line, review issue 4, "Not proposed: capping the losses at 50,000 ... It
     changes the recorded target, and unusual values stay, so the 802,620 claim is kept"; its notes: "The scores keep
     every loss uncapped." **TP-2** (Should): "A small but real signal is no reason to retire ... Retire, fix or keep a
     task for a concrete reason found in the task itself; until one is found, the task stays." **TP-3** (Must): "If
     tuned methods spread, keep the dataset." Both in main.

**Review panel:** ship after changes (mediator). Tier focused, a re-review of 2026-11-06 under LEAK-41 and MET-14 to
MET-16, after the notes gained an exposure paragraph and issue 3 moved here from PR #47's conversation: the claim
auditor, the split auditor and the mediator ran, with no blind reviewer, task gamer, advocate or critic in this tier.
Claims: 23; 17 hold (4 of them with wording now fixed: the reason for no training weight, the GLMs' covariates, the
entry and exit years, the constant baseline), 2 partly refuted (the licence reason, completed; issue 3's precedents,
corrected), 2 refuted and 1 not established (issue 3's LightGBM figures, its reading of the gap between pooled and
within-year scores, and that E removes the leak; issue 3 rewritten), 1 untested (the source's own Tweedie score on
2011, a year that is not public). Blind review: not run in this tier. Agreed: the exposure paragraph's calls (the
premium the Lorenz base and a scoring column only, no training weight, the coverage a feature, no time on risk); two of
the three accepted warnings as written and the licence reason completed; the 2008 window breaks the floor of half the
rows, so A has no route but an amendment of the floor; plain member folds leak the year's claim level; D is barred.
Disputed: the split (issue 3): the split auditor recommends E, the claim auditor finds a within-year leak under E,
which the mediator confirms over 20 repeats and removes with F, its recommendation. The full panel of 2026-11-01 is in
this file's git history.

<details><summary>Mediator</summary>

**Mediator report: wisconsin_local_government_property_insurance_fund (focused re-review, 2026-11-06)**

Sources: PANEL_COMMON.md, CHANGES.md, both auditor reports and their scripts, dataset.py, REVIEW.md, the record, principles.md, SPLIT-8/10/14 and LEAK-6, and pricing_game_2016_french_fleet's split auditor and precedent checker reports. I ran three decisive checks. Scripts and CSVs are in the run folder (common.py, leak_glm.py + leak_glm.csv, leak_models.py + leak_models.csv, lgbm_cost.py, fold_scheme.py, f_design.py).

**1. Recommendation (judgment record)**

Verdict: ship after changes.

Validity:
- USE-1 holds. USE-8 triggered, fixed (fit approximate). USE-6 holds.
- LEAK-41 holds: Premium is a scoring column only, set at the start of the year, not prorated; there is no time on risk.
- MET-15 holds: no training weight. The stated reason should be reworded (change 1).
- LEAK-10 holds.
- SPLIT-14 is broken. The 2008 window trains on 40.6% of the rows, and SPLIT-14 is a Must, so this cannot be an exception. Fix it by re-splitting under SPLIT-8 (issue 3).
- LEAK-6 and SPLIT-8 are triggered on member folds:
  - Scoring within each year (E) removes the year's claim level.
  - A confirmed share remains within the year: the Tweedie GLM gains +0.031 to +0.036 (SE about 0.005).
  - Only leaving the test year out of training removes that share (F, below).
- SPLIT-10: the no-gap exception's precedent (pricing_game_2016_french_fleet) is reopened. This is moot under E or F.
- PROV-9 holds. The licence reason is incomplete.

Value:
- MET-2 holds. A one-year Gini is the source's own (Sec. 6.2, 2011 only), and E and F both give it.
- TP-4 holds narrowly. Coverage alone leads on the mean in every design (0.368 on the valid windows, about 0.19 within-year); re-read TP-4 at the first benchmark run.
- TP-2: keep.

Quality: CLEAN-10 fixed; CLEAN-16 exception kept (dollars).

Weighed: source + and use case +; small test sets -, one 2010 claim at 35% of that year -, unseen members under any forced split -.

For the curator:
- Issue 3, a rule call: F or E under SPLIT-8 with no amendment, or B through an amendment of SPLIT-14. Decide it together with pricing_game_2016_french_fleet issue 6.
- The licence field, a provenance call.

My reading of issue 3:
- A is out without an amendment of the floor. Neither auditor defends A, and california_house_prices_2020 dropped such a window.
- D is barred: SPLIT-8 says being forced alone never makes a dataset `No`, and the leak can be fixed.
- By the remedy ladder (fix the definition before keeping a note), F is the mildest option that removes the whole measured leak without changing a rule.
- E is next, if the curator reads the remaining +0.03 as "slight optimism with a known cause" (LEAK-6's first clause, SPLIT-8's "otherwise ... measured in the notes").
- B is the alternative by amendment, and the closest to the use case.

**2. Changes to make now (no decision needed)**

1. MET-15. Exposure bullet, the reason for no row weight. "ordered_lorenz_gini takes totals ..., so the premium is no row weight" is an API fact, not a reason: the Gini on totals equals a premium-weighted Gini of the loss ratio (0.3456607658 both ways). Reword to: "the target is a total and the premium is set at the start of the year (not realized), so MET-15 asks for no training weight; an unweighted fit of the total estimates E[y|x], which the Lorenz curve then divides by the premium."
2. LEAK-41 and EV-1. "whether a member joined or left during a year cannot be checked" is too strong. Replace with: "cannot be located row by row; the exit years show no claim shortfall (observed/expected 0.93, z -0.46; permanent exits 0.86, z -0.85), the entry years no excess beyond chance (1.22, z 1.07), and the premium is not prorated in either."
3. EV-1. "simple GLMs give 1.14 and 0.67": name the covariates (coverage, deductible, entity type, no-claim credit, Fire5, alarm credit, year). Coverage alone gives 1.01 for the claim count and 0.77-0.82 for the Tweedie total.
4. PROV (house). Add to meta_license_unknown's reason: the second edition named in download_description (OpenActTexts/LDAVer2, WiscPropFund.csv, the same rows with fewer columns) has LICENSE CC0-1.0 in its repository (committed 2024-10-03), and its book pages state CC BY 4.0. The shipped first-edition file and its pages state none. The field value itself is issue B below.
5. Metric note (MET-2, clarity): "a prediction that adds nothing to the premium scores 0" is right for the premium itself (0.000 in every window). Add that a constant prediction is a different baseline: 0.061, -0.124 and -0.004 for test 2010, 2009 and 2008.
6. REVIEW.md issue 3 text (EV-1), in five places:
   - (a) LightGBM figures. Say which configuration was used: 0.232, 0.044 and -0.001 come from a 15-leaf, 200-tree configuration. Replace the one-draw numbers with repeat-averaged ones [section 4, LightGBM]. Drop "LightGBM near 0 against 0.23" as a general claim: the gap is 0.10 to 0.23, depending on the configuration.
   - (b) Effect, C and E. Remove "the year-level leak lifts the pooled score". The pooled-versus-within gap shows for coverage alone, which involves no training (0.318 against 0.209). Cite only the controlled leak test.
   - (c) E's Pro. Change it to "removes the year's claim level; a within-year share remains (Tweedie GLM +0.031 to +0.036 over 20 repeats, SE about 0.005; LightGBM about 0)".
   - (d) Consistency. nba_players_2016_2019 was retired on 2026-10-26 on its use case, so it did not ship. The batch's forced splits number 6 (8 with fremtpl2 and bemtpl97), not 7.
   - (e) Add option F [F in section 3].
7. Stale text after the reopening of pricing_game_2016_french_fleet. splits_comment, REVIEW.md's Outcome paragraph and the record's CC line cite the no-gap exception "as in pricing_game_2016_french_fleet". That precedent is reopened (its issue 6) and never covered a window below the floor. Mark it stale now; it goes under E or F, and needs its own fact plus a SPLIT-10 Cases row (kind exception) under A or B. The Cases row is missing today, a process gap the pg16 precedent checker also found.
8. Record line. Add "Assessment (AI, 2026-11-06)". It records:
   - the exposure paragraph (Premium is the Lorenz base and a scoring column only; coverage is a feature; no time on risk);
   - the three accepted warnings;
   - the second-edition licence fact, which supersedes the screening's "No data licence is stated";
   - issue 3 open, with this panel's numbers.

**3. Issues for the curator (ranked)**

A. Issue 3, the split (P4, Must: SPLIT-14, SPLIT-8, LEAK-6). Validity. [issue 3]

Problem: the shipped split A breaks SPLIT-14's floor. Its 2008 window trains on 2006-2007 alone, where the no-claim credit is unknown on every training row. It is also the window that changes the predictors' order: on the valid windows coverage beats the GLM; with 2008 included the GLM comes first.

Effect of each option (untuned, no member id; within-year Gini against the premium):
- A, three windows (shipped): breaks the floor. It needs an amendment of SPLIT-14 itself, against the california_house_prices_2020 precedent.
- B, two windows (test 2009 and 2010):
  - No period is shared.
  - Known members and PolicyNum as an input stay, which fits USE-10, the fund re-rating its own members.
  - Valid-window scores: coverage 0.368, GLM 0.30-0.31, LightGBM 0.15-0.23 depending on the configuration.
  - It needs an amendment of SPLIT-14's three-window count, for example "a release that gives exactly two windows, both training on at least half the rows, ships those two; fewer go to SPLIT-8".
  - The no-gap exception to SPLIT-10 would then need its own fact.
  - The 2010 window rests on one claim, so comparisons lean on 2009.
- C, member folds, pooled Gini: the leak is kept although it can be removed. LEAK-6 and SPLIT-8 rule it out.
- D, `No`: barred by SPLIT-8 and the remedy ladder.
- E, member folds, Gini within each year:
  - No amendment is needed.
  - It needs a library metric (mean of per-year ordered-Lorenz Ginis, MET-12 and MET-13).
  - Year goes to a scoring column with role `group`.
  - Scores: coverage 0.188, GLM 0.16-0.18, LightGBM 0.00-0.05.
  - A confirmed within-year leak remains for the GLM: +0.031 to +0.036.
- F, new from the mediator, not proposed by either auditor. Member folds crossed with leave-the-test-year-out:
  - Each test fold is one year of one third of the members.
  - It trains on the other members' rows of the other years.
  - This removes both the member link and the test year's own outcome.
  - Each test fold is a single year, so the shipped ordered_lorenz_gini already scores per year: no new library metric.
  - It needs a custom `_make_splits` override (no declaration exists for a crossed design) and a ForcedGroupedFromTemporal tag.
  - Fold size: 15 test folds per repeat, about 376 member-years each (86-134 claimants), training on 53% of the rows.
  - Scores: GLM 0.139 against 0.175 on the same folds with the test year in training; coverage 0.198 (training-free).
  - No precedent ships this design.

Best evidence for E (split auditor): it is the regime SPLIT-8 prescribes, and the year-level leak is gone. My controlled test confirms that the pooled AUC (+0.012, 9 of 9) and pooled Gini gains disappear into the year level. It keeps the order of the three predictors.

Best evidence against E (claim auditor, confirmed here): the test year's training rows still add within-year Gini for a GLM.
- Both size controls agree over 20 repeats: random-drop +0.031, drop-another-year +0.036; SE about 0.005.
- By year: 2006 +0.07, 2007 -0.02, 2008 +0.03 to +0.04, 2009 +0.04 to +0.06, 2010 +0.02 to +0.05.
- The split auditor's +0.005 was 9-fold noise.
- LightGBM shows about 0 (+0.008 and -0.003, SE about 0.016).
- The claim auditor's +0.086 and +0.099 for 2009 and 2010 were noisy highs.

Rule: LEAK-6 (Must, part 3), "a confirmed leak goes even when small"; SPLIT-8 (Must, part 4), "removed where it can be, otherwise ... measured in the notes". F shows the leak can be removed, so by the ladder F comes before E with a note.

Decision needed:
- F (the rules' fix);
- E (the residual is read as slight optimism with a known cause and kept with a note; then the notes state +0.03 GLM and about 0 LightGBM);
- or B (amend SPLIT-14 for exactly two valid windows).

A needs an amendment of the floor. C and D are not supported.

What would settle F against E for good: the same controlled test with tuned models, 20 or more repeats. If the residual vanishes for tuned models, E with a note is defensible.

B. Licence field (P5 and house, Should). Value. [no numbered issue: a licence decides no fix (EV-4); the second-edition route is a note in the record]
- Keep `license = None`: the shipped file is the first edition's, which has more columns and states no licence.
- Or take the rows through the second edition: WiscPropFund.csv, CC0-1.0 in the repository, CC BY 4.0 on the pages. That would need a column check of what the second-edition file lacks.

Decision: keep None with the corrected reason (change 4), or switch the source.

**4. Agreed facts**
- Rows and members: 5,639 member-years, 1,227 members. Members present in 1 to 5 years: 48 / 54 / 55 / 32 / 1,038. Years 2006-2010, no finer time. CLAIMLEVEL's ClaimNum year prefix is a placeholder.
- Target: 70.2% zeros; Freq is 0 exactly where y is 0.
- Train shares of windows starting in 2008, 2009 and 2010: 40.6%, 60.6% and 80.3%. Only two windows meet the 50% floor.
- Known members: 97.6-98.8% of each test year's members appear in earlier years.
- No-claim credit known on 0%, 32.1% and 47.8% of the training rows of the 2008, 2009 and 2010 windows.
- Coverage alone on the shipped windows: 0.019, 0.195 and 0.540.
- Premium:
  - The rating's output (R^2 0.98), set at the start of the year and not prorated.
  - It scores 0 as a prediction.
  - It is no input and no training weight.
  - Its rating residual ranks this year's claims no better than last year's.
- Coverage is set before the year's claims: change into year t is +0.059 with a claim against +0.061 without.
- The source estimates the coverage coefficient rather than fixing it at 1 (Table 11: 0.853 NB, 0.136 GB2).
- The source scores one year (2011) against that year's premium (Sec. 6.2).
- Member folds: the year-level leak is real on the pooled score (AUC +0.010 to +0.012, 8-9 of 9) and goes with per-year scoring.
- The pooled-versus-within gap appears for coverage alone, so it does not measure the leak.
- LightGBM member-fold scores move a lot with the fold draw. Default configuration, 12 draws: pooled 0.075-0.083, within-year 0.035-0.051 (SE about 0.015). The claim auditor's 0.112 and 0.101 come from a favourable 3-draw sample. On the valid windows LightGBM scores 0.12-0.23, depending on leaves (15 against 31) more than on trees or encoding.
- Accepted warnings: task_time_on_few_unique and task_target_value_dominant hold. The meta_license_unknown reason is incomplete.

**5. Consistency**

pricing_game_2016_french_fleet issue 6:
- Its split auditor recommends C: forced grouped by contract under SPLIT-8, one valid window, A and B only by amendment.
- Its precedent checker says an amendment below three windows would reopen spanish coverage, nba, open_university and cauca.
- Mine (F or E) pulls the same way: both datasets drop the window that breaks SPLIT-14 and ship forced grouped under SPLIT-8, with no amendment.
- If the curator picks B here, the amendment for exactly two valid windows reaches neither pg16 (one valid window) nor the one-window precedents, so the two still do not pull against each other.
- The pair that would pull opposite ways is A in both datasets. That needs two different loosenings of SPLIT-14 (the floor here, the shared training side there), so decide the two together.
- Measure both alike: pg16's still-missing SPLIT-8 leak test should include the same size-controlled within-period test with at least 20 repeats.

Other precedents:
- spanish_motor_insurance_coverage_level_2022_2024 shipped forced grouped with "no leak found". I did not check whether its test looked within a period.
- What sets this case apart from it and from nba and open_university: two valid windows exist, and a within-year residual is measured.
- california_house_prices_2020 is against A.
- If E or F is chosen, add a SPLIT-8 Cases row stating the within-year leak and how it was handled. Option F would be the first crossed design: if adopted, record it as SPLIT-8's form for stacked years with a shared period outcome.

</details>

<details><summary>Claim audit</summary>

**Claim audit (focused re-review, 2026-11-06): wisconsin_local_government_property_insurance_fund**

Definition: the dataset's dataset.py, README.md and REVIEW.md.

Scripts and outputs in the run folder (t1_facts.py, t2_exit.py, t3_scores.py, t4_member_folds.py, t5_member_folds_control.py, t6_lgbm.py, t7_lgbm_default.py; the paper, Frees, Lee and Yang 2016, from the ANU open repository). The container was loaded through load_definition (not built).

Verdict: the exposure paragraph holds, and so do its rule calls: Premium is the Lorenz base, a scoring column and no
sample weight (MET-15), coverage is a feature (LEAK-41 does not apply), and no time on risk exists. Two of its
wordings are weaker than the facts. Two of the three accepted warnings hold. The licence warning's reason is
incomplete: the second edition, which the definition itself names, is CC0 (repository) and CC BY 4.0 (book pages). Issue 3 has two refuted
facts that bear on the decision: (1) "LightGBM near 0 on the member folds against 0.23 on the valid windows" does not
reproduce. LightGBM with the library defaults reproduces the notes' own no-member numbers exactly, and it gives 0.151
on the two valid windows against 0.112 pooled and 0.101 within-year on member folds. (2) "E removes the year-level
leak" is not established. In a test that holds the training size equal, the test year's own training rows still add
+0.040 within-year Gini (SD 0.11, 45 fold-years), +0.086 in 2009 and +0.099 in 2010. Also, the pooled-vs-within gap
that the issue reads as the leak appears for coverage alone, which involves no training at all.

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | Premium is the rating's output, not an amount at risk | dataset.py notes, Exposure bullet | regress log premium on the rating variables, pooled with year dummies; check whether entry and exit years are prorated | holds | R^2 0.983. The residual in entry years (n 73) is +0.174 and in exit years (n 117) +0.048, against -0.002 on the other rows, so part years are not prorated | MET-15, LEAK-41 |
| 2 | ordered_lorenz_gini takes totals, not per-unit values, "so the premium is no row weight" (MET-15) | Exposure bullet | score one fold on totals, then as per_unit rates y/P, p/P weighted by P | holds as the API says; the reason is weak | 0.3456607658 both ways (fold test 2010): the metric is identical to a premium-weighted Gini of the loss ratio. MET-15 still asks for no sample weight, but on other grounds: the target is a total, not a rate, and the premium is set at the start, not realized (claim 1). row_weight_column returns None; bundle checks give 0 warnings | MET-15 |
| 3 | No training weight is declared | dataset.py | sample_weight(c), check output | holds | None; task_metric_weight_without_sample_weight does not fire (the bundle check: 0 warnings) | MET-15 |
| 4 | Premium is a scoring column only, never an input | Exposure bullet, scoring_columns | feature_columns(c) | holds | features: PolicyNum, Year, LnCoverage, lnDeduct, Fire5, NoClaimCredit, EntityType, AlarmCredit | MET-2, USE-6 |
| 5 | Premium is set at the prediction point (implied by LEAK-41) | implied | Spearman of the premium's rating residual with a claim this year against a claim last year (rows with the year before in the file) | holds | 0.048 against 0.053 (n 4,408): the premium carries no more about this year's claims than about last year's. A constant prediction (= 1/Premium order, the LEAK-41 "ceiling") scores 0.061 / -0.124 / -0.004 (test 2010/2009/2008) | LEAK-41, LEAK-10 |
| 6 | LnCoverage is the BC sum insured, set for the year at renewal | Exposure + coverage bullets | change in log coverage into year t by the claim status of t, and into t+1 after a claim | holds | into t: +0.0586 with a claim, +0.0614 without, +0.052 top 10%; into t+1: +0.062 / +0.060 / +0.057. Median yearly change 2007-09 is 5.6%, 5.2%, 5.2%; 67.7% fell in 2010 | LEAK-41, LEAK-10 |
| 7 | The source estimates the coverage coefficient rather than fixing it at 1; its offset definition is in Sec. 2.2 p. 5; Table 11 p. 19 gives 0.853 (NB) and 0.136 (GB2), about 0.99 before the zero-one inflation | Exposure bullet | read the paper (ANU copy) | holds | Sec. 2.2 "Modeling Frequency Using GLMs", p. 5: "restrict the corresponding regression coefficient to be 1; this term is known as an offset". Table 11: lnCoverageBC 0.136 (GB2), 0.853 (NB); 0.853 + 0.136 = 0.989. The Zero part's CoverageBC is -0.408, which pushes the elasticity up after inflation (the hedge is right) | MET-14 |
| 8 | Simple GLMs give 1.14 (claim count) and 0.67 (Tweedie total) | Exposure bullet | Poisson and Tweedie (p 1.5, 1.7) with coverage, deductible, entity, NCC, Fire5, AC and year | holds, depends on the specification | 1.139; 0.672 (p 1.5), 0.676 (p 1.7). Coverage alone: 1.009 and 0.822 / 0.774. "Simple GLMs" should name the covariates | MET-14 |
| 9 | No time at risk; "whether a member joined or left during a year cannot be checked" | Exposure bullet | observed against cross-fitted expected claims (logistic on rating variables + year) in entry and exit years; premium proration (claim 1) | holds in substance; wording too strong | exit years (n 121): claims O/E 0.93, z -0.46 (permanent exits 0.86, z -0.85); entry years (n 77): O/E 1.22, z 1.07; other rows 1.00. No proration of premium. So a check is possible and finds nothing at this power | LEAK-41, MET-14 |
| 10 | 48/54/55/32/1,038 members in 1-5 years | Exposure bullet | count | holds | {1:48, 2:54, 3:55, 4:32, 5:1038}, 1,227 members, 5,639 rows | - |
| 11 | task_time_on_few_unique: five policy years, windows train on 2-4 years, no finer time | accepted_check_warnings | unique years; CLAIMLEVEL columns | holds | years 2006-2010. CLAIMLEVEL has no date column, and its ClaimNum prefix is "2008" on 6,257 of 6,258 lines (it matches Year on 17.5%), so it is a placeholder | SPLIT-14 |
| 12 | meta_license_unknown: "the textbook's repository has no licence file, and the book's pages state none" | accepted_check_warnings | GitHub API on both editions; the book pages | partly refuted | first edition (OpenActTexts/Loss-Data-Analytics): license null, and the book page states none (true). But the second edition, which download_description names as holding the same rows (WiscPropFund.csv), has LICENSE = CC0-1.0 (GitHub API; LICENSE committed 2024-10-03), and its chapters state "licensed under a Creative Commons Attribution 4.0 International License" | PROV (licence), house |
| 13 | task_target_value_dominant: 70.2% zeros, Freq 0 exactly where y 0, real no-claim years; accepted on the same ground as the batch (Andrej, 2026-11-03) | accepted_check_warnings | count; CHANGELOG 2026-11-03 | holds | 0.7023; Freq==0 <=> y==0 on every row. The CHANGELOG entry accepts it for five batch tables with Andrej's quote. The source's Table 9 gives a 0 proportion of 0.702 | CLEAN, TP |
| 14 | Issue 3: train shares 40.6/60.6/80.3; test rows and claimants per window; the credit is unknown on every 2008 training row | REVIEW issue 3, splits_comment | shipped splits | holds | 0.406/0.606/0.803; 1,125/1,112/1,110 test rows; 309/301/403 claimants; NCC known on 0.000/0.321/0.478 of training rows | SPLIT-14 |
| 15 | Issue 3: on the shipped windows coverage scores 0.019/0.195/0.540, and on the two valid windows (no member id) coverage 0.368 and the GLM 0.312 | REVIEW issue 3 Experiments | scorer per window; Tweedie GLM p 1.5 | holds (coverage exactly; GLM approximately) | coverage 0.019/0.195/0.540 (mean of 2009-10: 0.368). My GLM without the member: 0.244/0.256/0.346, mean of 2009-10 0.301 (claimed 0.312); with the member 0.220/0.276/0.345 (claimed 0.254/0.251/0.350): differences in the specification | MET-2 |
| 16 | Issue 3: LightGBM (no member id) 0.232 on the two valid windows and 0.215 on the three; 0.044 pooled and -0.001 within-year on member folds; "LightGBM near 0 against 0.23 on the valid windows" (the con of C and E, and in the Recommendation) | REVIEW issue 3 Experiments, Options, Recommendation | default LGBMRegressor(objective="tweedie"), the shipped windows; member folds 3x3 GroupKFold | refuted (not reproducible, and contradicts the notes) | the defaults reproduce the notes' "without PolicyNum: 0.146, 0.221, 0.081" exactly. Mean of 2009-10 is 0.151, of all three 0.149. Member folds: pooled 0.112 (SD 0.116), within-year 0.101 (SD 0.093). With 200 trees at lr 0.05: windows 0.180/0.212/0.024, folds 0.117/0.097. The fold-vs-window gap for LightGBM is about 0.04, not 0.23. The issue's numbers also conflict with the definition's own (0.215 against 0.149 on the same three windows) | SPLIT-8 (cost against the valid windows), EV-1 |
| 17 | Issue 3: C and E: "the year-level leak lifts the pooled score" (pooled 0.318/0.265/0.044 against within-year 0.209/0.192/-0.001) | REVIEW issue 3 Effect | compare a training-free sort (coverage) pooled against within-year on member folds | refuted as an inference | the issue's own coverage numbers show the gap with no model trained (0.318 against 0.209), and so do mine (0.248 against 0.170; the GLM 0.258 against 0.197). Pooling over years changes the score whatever the leak; the gap does not measure it | SPLIT-8, LEAK-6, MET-2 |
| 18 | Issue 3, option E: scoring within each year "removes the year-level leak" | REVIEW issue 3 Options, Recommendation, its leak footnote | member folds (3x3), Tweedie GLM without Year. Within-year Gini when training drops the test year's rows, against when it drops one other year (equal size, mean over the 4 others) | not established, leaning refuted | the same-year training rows add +0.040 (SD 0.112, 45 fold-years, positive in 51%). By year: 2006 +0.019, 2007 -0.025, 2008 +0.021, 2009 +0.086, 2010 +0.099. Without the size control: +0.047. Within-year scoring removes the level, but a shared within-year shock (the 2010 storms) still crosses member folds, of the order of the pooled leak measured on 11-02 (+0.113). The earlier within-year test (+0.008, SD 0.20) could not have found it | LEAK-6 (Must), SPLIT-8 |
| 19 | Issue 3: the source's Gini compares one year's members (2011) against that year's premium; E is "one year's Gini, as the source scored" | REVIEW issue 3 its leak footnote, Options | paper Sec. 6.2 | holds | "computed using relativities computed with the actual premium collected by the LGPIF in 2011 as the denominator"; out-of-sample 2011, 1,098 observations | MET-2 |
| 20 | Issue 3 precedents: california's windows now 50/67/83; open_university forced-grouped with one valid window; "nba_players_2016_2019 ... shipped folds by entity"; "seven insurance tables of this batch ship forced splits" | REVIEW issue 3 Consistency | definitions, SPLIT-8 text, records | california and open_university hold; nba and the count are imprecise | nba_players_2016_2019 is suggestion 'No' and has no folder ("retired on 2026-10-26 on its use case, not its split", SPLIT-8). Forced tags among the 15 folders of batch commit 65ac698b: 6 (allstate, australian, frempl, liberty, pricing_game_2017, spanish_coverage). With fremtpl2 and bemtpl97: 8. Not 7 | PROV, house |
| 21 | SPLIT-14, SPLIT-8, LEAK-33 as quoted in the footnotes | REVIEW issue 3 footnotes | splits.md, leak_checks.md | holds | the quotes match the current text | - |
| 22 | Metric: the source's ordered-Lorenz Gini with Premium as base, not normalized; "a prediction that adds nothing to the premium scores 0" | Metric.source, README | paper Sec. 6.2; score the premium as prediction per window | holds | premium scores 0.000 on every window; an oracle scores 0.85-0.89; every window holds 301-403 claimants. Note: a constant prediction does not score 0 (0.061/-0.124/-0.004), so "a constant" and "the premium" are different baselines | MET-2, MET-4/5 |
| 23 | (context, not today's change) Our Tweedie GLM scores far above the source's | paper Sec. 6.2 | - | untested | the source's Tweedie BC scored -1.74% on 2011 and the dependent model 22.77%. Ours scores 0.24-0.35 on 2008-2010. 2011 is not public, so this cannot be checked; worth one sentence of context under MET-2 | MET-2 |

**Refuted and untested, ranked**

1. Claim 18, LEAK-6 (Must) via SPLIT-8: option E's premise "removes the year-level leak" (the recommended option).
   A size-controlled test finds the test year's training rows still add +0.040 within-year Gini, +0.09 to +0.10 in
   2009-2010. What changes: E does not by itself meet "removed where it can be". If E is chosen, the notes must
   measure and state the remaining within-year leak (SPLIT-8, approximate fit). This also weakens the case for E over
   B. Mildest remedy: rewrite E's Pro as "removes the year's claim level; a within-year share remains (+0.04, +0.09 to
   +0.10 in 2009-10, measured)" and rerun the 11-02 within-year leak test with the size control and enough repeats to
   beat its SD of 0.20.
2. Claim 16, the cost figure in C/E's Con and the Recommendation ("LightGBM near 0 against 0.23"). It does not
   reproduce, and it contradicts the definition's own no-member numbers (0.146/0.221/0.081). Library-default LightGBM:
   0.151 on the two valid windows against 0.10-0.11 on member folds. What changes: the measured cost of member folds
   (SPLIT-8's "cost measured against the valid windows") is about 0.04 for LightGBM and about 0.07-0.10 for the GLM,
   not 0.23. That makes C/E look less costly, and the issue's tie-break toward B rests on a wrong number. Mildest
   remedy: replace the LightGBM figures with ones that reproduce the notes (state the config), give the per-fold SD,
   and drop "near 0".
3. Claim 17, the inference "the year-level leak lifts the pooled score" from pooled against within-year. A
   training-free coverage sort shows the same gap. What changes: the pooled-vs-within numbers in issue 3 are no
   evidence of the leak. Only the 11-02 with/without-same-year test is. Mildest remedy: cite the coverage gap next
   to the model gaps, and quote the leak by the controlled test (claim 18) only.
4. Claim 12, meta_license_unknown's reason (house/provenance, Should). It omits that the second edition (named in
   download_description) is CC0-1.0 in its repository and CC BY 4.0 on its book pages. What changes: the licence may
   be stated rather than unknown, at least for the columns WiscPropFund.csv shares. Mildest remedy: add the fact to
   the reason and the record, and let the curator decide between keeping `None` (the shipped first-edition file has
   more columns and no licence) and `CC BY 4.0` via the second edition.
5. Claim 2, the stated reason for "no row weight". The Lorenz on totals equals a premium-weighted Gini of the loss
   ratio (0.3456607658 both ways), so "takes totals ... not per unit" is an API fact, not the reason. The conclusion
   (no sample weight) holds because the target is a total and the premium is set at the start (claims 1, 5). Mildest
   remedy: reword to "the target is a total and the premium is fixed at the start of the year (not realized), so
   MET-15 asks for no training weight; an unweighted fit of the total estimates E[y|x], which the Lorenz then divides
   by the premium".
6. Claim 9, "cannot be checked" (wording, Should). A check is possible and finds nothing: exit-year claims O/E 0.86-0.93
   (|z| < 1) and no proration of the premium. Mildest remedy: "cannot be located row by row; the exit years (117
   members) show no claim shortfall (O/E 0.86, z -0.85) and no prorated premium".
7. Claim 20 (house): nba_players_2016_2019 did not ship (retired 2026-10-26 on its use case). Forced splits in the
   batch number 6 (8 with fremtpl2 and bemtpl97), not 7. Mildest remedy: "nba_players_2016_2019 (retired on its use
   case) and open_university ..." and the right count.
8. Claim 8 (minor): "simple GLMs" should name the covariates. Coverage alone gives 1.01 and 0.77-0.82.
9. Untested: claim 23 (the source's Tweedie at -1.74% on 2011 against our 0.24-0.35 on 2008-2010). 2011 is not public.
   A context sentence, no change.

</details>

<details><summary>Split audit</summary>

**The split auditor's report: wisconsin_local_government_property_insurance_fund (exposure re-review, 2026-11-06)**

REVIEW.md issue 3: which split the five policy years get (options A-E)

Verdict: the shipped split (A, three expanding yearly windows, the 2008 window at 40.6%) is WRONG under the rules as
written. The rules support E (folds by member, ForcedGroupedFromTemporal, the premium-base Gini taken within each year
and averaged). C is the fallback only if the per-year Gini cannot be had; A and B each need an amendment of a Must
(the curator's to make, not an exception); D is barred.

**1. The facts** (re-measured; scripts and CSVs in the run folder)

Time column: `Year`, the policy year, 2006-2010; no finer time in the file. Train shares of a window starting at
2008/2009/2010: 40.6% / 60.6% / 80.3%. So exactly two yearly windows meet the 50% floor; a third does not exist.

Use case: the fund re-rates members it knows (97.6-98.8% of each test year's members are in earlier years): by USE-10
a known entity, i.e. temporal by nature.

Same inputs on every design (no member id; Year, coverage, deductible, Fire5, no-claim credit, type, alarm), untuned
Tweedie GLM (power 1.5) and LightGBM Tweedie, ordered_lorenz_gini against Premium (compare.py, designs.csv):

```text
                                        coverage alone   Tweedie GLM   LightGBM
  windows 2008 / 2009 / 2010            0.019/0.195/0.540  0.244/0.256/0.346  0.181/0.251/0.205
  two valid windows (2009, 2010), mean  0.368              0.301              0.228
  three windows (A), mean               0.251              0.282              0.213
  member folds (3x3), pooled (C)        0.291 (SD 0.215)   0.243 (0.172)      0.027 (0.150)
  member folds, within each year (E)    0.188 (SD 0.170)   0.162 (0.125)     -0.008 (0.133)
```

These reproduce REVIEW.md's figures (0.368/0.312/0.232 valid windows; 0.209/0.192/-0.001 within-year) within the
seed and setup noise.
- The order of the three predictors on the two valid windows (coverage > GLM > LightGBM) is kept by C and by E. A is
  the design that changes it: the 2008 window (coverage 0.019 against GLM 0.244) puts the GLM above coverage alone.
  The window SPLIT-14's floor bars is exactly the one that moves the comparison; it trains on 2006-2007 alone, where
  the no-claim credit is unknown on every training row, so its training side is the least like the fund's.

Leak across the member folds (leak.py, leak.csv; 9 folds; each test year predicted by a model trained without that
year's training rows, against one trained without as many random training rows; gain = random-drop minus year-drop):

```text
  ROC AUC for a claim, pooled:   GLM +0.0119 (9/9 positive, SD 0.007), LightGBM +0.0076 (8/9)
  Gini, pooled (option C):       GLM +0.030 (7/9, SD 0.105), LightGBM +0.038 (5/9, SD 0.178)
  Gini, within each year (E):    GLM +0.005 (5/9, SD 0.046), LightGBM -0.008 (4/9, SD 0.053)
```

The leak is confirmed (AUC 9/9, as on 2026-11-02) and it is the year's claim level: it reaches the pooled score and
vanishes once the Gini is taken within each year. My pooled Gini gain is smaller than REVIEW.md's +0.113 (5 of 9);
both are noisy; the AUC and the within-year null are the robust parts, and they agree with the earlier run.

**2. The options against the rules** (ranked by principles.md: P3 > P4; within P4, Must before Should)

Governing text. SPLIT-14 (Must): >= 3 windows AND every train side >= 50%; "A task that cannot meet it ships under
SPLIT-8". SPLIT-8 (Must; narrows SPLIT-7, SPLIT-14 and USE-10): too few periods -> the closest regime that keeps the
rows, IID or grouped by the entity when the periods are stacked and entities recur (ForcedGroupedFromTemporal), cost
measured against the valid windows; a leak across the forced split is "removed where it can be"; "Being forced alone
never makes a dataset `No`". principles.md: "A Must has no exceptions: only a higher-ranked Must overrides it, and
anything else is an amendment." USE-10 (P3, Must) would ask for a temporal split for known members, but SPLIT-8 states
that it narrows USE-10, so within its scope (a release that cannot give SPLIT-14's windows) SPLIT-8 decides. No
higher-ranked Must overrides SPLIT-14 here.

**A (three windows, shipped) - NOT SUPPORTED.**

  Rule: breaks SPLIT-14's floor (Must). The 2026-11-02 call is recorded as a departure "on the curator's call"; a Must
  takes no exception, so it is either an amendment of SPLIT-14 or it falls. Precedent against it: SPLIT-14 Cases,
  california_house_prices_2020 (applied): the 25% window was removed, not shipped. Evidence: the 2008 window is the one
  that changes the predictor order (above), and its training side has no known no-claim credit: the very "too unlike
  the real application" SPLIT-14 gives as its reason. The no-gap exception to SPLIT-10 the definition cites "as in
  pricing_game_2016_french_fleet" no longer stands on that precedent: that row (SPLIT-14 amended 2026-11-02, Andrej)
  was reopened today under LEAK-41 (its three windows again share one training side, its issue 6, open), and its
  windows were above the floor (64-78%) in any case, so it never licensed a window below it. Also, with any gap A
  loses a second window (a one-year gap leaves test 2009 on 40.6%).

**B (two windows, 2009 and 2010) - NOT SUPPORTED AS WRITTEN; the amendment the facts would best support.**

  Rule: breaks SPLIT-14's three-window count (Must). Lennart's framing in PR #47 ("ships as forced (SPLIT-8) with two
  folds") does not fit SPLIT-8 either: SPLIT-8's closest regimes are IID or grouped, not a shorter temporal split, so B
  needs an amendment of SPLIT-14 or SPLIT-8 (e.g. REVIEW.md issue 1's wording: "a temporal task whose release gives
  exactly two windows, both training on at least half the rows, ships those two; fewer go to SPLIT-8"). It also keeps
  the no-gap departure from SPLIT-10 (Should): a one-year gap would put test 2009 on 40.6%; that exception would need
  its own fact, now that pricing_game is reopened. Facts for it: it is the regime of the use case (USE-10, known
  members, PolicyNum an input), and on these numbers it ranks the predictors as E does. Against it: two test years,
  the 2010 one dominated by one $12.9M claim (35% of the year's claims), so model comparisons lean on 2009.

**C (member folds, pooled Gini, leak measured) - FALLBACK ONLY.**

  Rule: the regime SPLIT-8 prescribes, but a confirmed leak (AUC +0.012, 9/9) reaches its score, and SPLIT-8 says
  "removed where it can be" with LEAK-6 (Must: "a confirmed leak goes even when small"). It can be removed (E), so
  shipping C with a note is the weaker remedy and is allowed only if E cannot be built.

**D (`No`) - BARRED.**

  SPLIT-8: being forced alone never makes a dataset `No`; principles.md step 5: exclusion is for a Must that cannot be
  fixed, and this one can (E).

**E (member folds, Gini within each year, averaged) - SUPPORTED.**

  Rule: SPLIT-8's regime (grouped by the recorded member key PolicyNum, a true entity id under SPLIT-24; all of a
  member's years on one side; ForcedGroupedFromTemporal). The leak is removed where it reaches the declared metric:
  within-year Gini gain +0.005 / -0.008 (SD 0.05), against +0.03-0.04 pooled and AUC +0.012. MET-2 (Must) also points
  here: the source's Gini compares the members of one year (2011) against that year's premium (Frees, Lee and Yang
  2016, Sec. 6.2), so a per-year Gini is the source's metric and a pooled multi-year Gini is not. Grouping by member
  also removes the SPLIT-9 question A and B leave open (a member's own earlier claim amounts, final only after its next
  rating, reaching its test row through PolicyNum).

  Cost, stated as SPLIT-8 asks (valid windows -> E): coverage 0.368 -> 0.188, GLM 0.301 -> 0.162, LightGBM 0.228 ->
  -0.008; the order of the three is kept. SPLIT-21 bars choosing the design from such a comparison, and I do not: the
  choice is the rules'; the numbers are the cost for the notes.

  What it costs the task: unseen members (cold start) while the fund re-rates known ones, so PolicyNum leaves the inputs
  (LEAK-33) and the gain it carried in the windows (LightGBM 2010: 0.327 with it, 0.081 without) is not testable; the
  splits_comment must say so (USE-10) and that the temporal windows should return if a release with more years (the
  source's 2011 test year) appears. Training sides contain later years than some test rows; within-year scoring makes
  the year level irrelevant and the measured within-year gain is null.

**3. Problems in the shipped definition, ranked (all P4)**

1. SPLIT-14 (Must) broken: the 2008 window trains on 40.6% (evidence above). Mildest remedy that keeps the rules:
   re-split to E. If the curator prefers the temporal regime, the alternative is an amendment (B's wording), with the
   2008 window dropped in either case; A as shipped has no route other than amending the floor itself, against the
   california_house_prices_2020 precedent.
2. LEAK-6 / SPLIT-8 (Must): if folds by member ship, the year-level leak must be removed, not noted: the per-year
   metric (E). Remedy: a library metric for the mean of per-group ordered-Lorenz Ginis (MET-12 name, e.g.
   `mean_group_ordered_lorenz_gini`, tested against a loop over `ordered_lorenz_gini`, MET-13), `Year` copied to a
   scoring column of role `group`, `inputs={"weight": "Premium", "group": <copy>}`; `Year` may stay a feature.
3. SPLIT-10 (Should): the shipped no-gap exception cites pricing_game_2016_french_fleet "as" precedent; that row was
   reopened today and never covered a below-floor window. Moot under E; under B it needs its own fact.
4. Text to change with E: `task_summary.split`, `splits_comment` (cost against the two valid windows, the leak test
   and its removal, the unseen-member caveat), the `Temporal` declaration replaced by `Grouping(on="PolicyNum")`,
   PolicyNum out of the inputs, the accepted warning `task_time_on_few_unique` dropped (it no longer fires), the
   Decision table "Three yearly windows ..." retitled, a SPLIT-8 Cases row, the record's required_split/tag.

Not a problem: LEAK-41 does not bite this split (no time on risk; Premium is a scoring column only, never an input; no
window or fold admits rows by a realized weight). No hidden group beyond the member (no member looks renumbered; near
copies agree on a claim at chance, from the 2026-11-02 test).

</details>

## Reference

Frees, E.W., Lee, G., Yang, L. (2016). Multivariate Frequency-Severity Regression Models in Insurance. Risks 4(1):4.
https://doi.org/10.3390/risks4010004

Frees, E.W. (ed.), Loss Data Analytics, Ch. 1 (Case Study: Wisconsin Property Fund). OpenActTexts.
https://github.com/OpenActTexts/Loss-Data-Analytics

Lead: curator's list of exposure-scaled insurance tables (Chubb comparison), 2026-10-20; not in the v4 workbook.
