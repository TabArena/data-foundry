---
unique_name: australian_vehicle_insurance_2004_2005
name: dataCar (insuranceData) / ausprivauto0405 (CASdatasets) / Car (de Jong and Heller 2008)
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 3
tags:
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
v2_path: datasets/_dev/tabarena-v0pt2/australian_vehicle_insurance_2004_2005/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (v4 of 2026-10-19, a list of 69 candidates, not in the repository), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> Yes`, priority 3: a documented textbook table of 67,856 one-year Australian car
policies with an observed claim-cost target; few, coarse rating factors and a weak signal.
- Source: de Jong and Heller (2008), Generalized Linear Models for Insurance Data (Cambridge University Press), data on
  the book's site (acst.mq.edu.au/GLMsforInsuranceData, the source insuranceData cites). As published (insuranceData
  `dataCar`): "This data set is based on one-year vehicle insurance policies taken out in 2004 or 2005", 67,856 x 11:
  `veh_value`, `exposure`, `clm`, `numclaims`, `claimcst0` ("claim amount (0 if no claim)"), `veh_body`, `veh_age`,
  `gender`, `area`, `agecat`, `X_OBSTAT_`; one table. CASdatasets `ausprivauto0405` holds the same rows (compared row by
  row by the earlier triage).
- Use case: for example, an insurer pricing a one-year car policy at underwriting from its rating factors; the package
  pages name no decision and the book was not read; fit direct for that use. Regime IID: one policy-year per row, no
  dates, no ids.
- Siblings and duplicates: both R-package copies share this record (merged 2026-10-19); no other Australian motor
  record. OpenML: none by name; external collections: insuranceData, CASdatasets.
- Papers and pages: the book (doi:10.1017/CBO9780511755408), not read; the insuranceData `dataCar` help page.
- Metric: none found (the insuranceData and CASdatasets pages; the book not read), so the fallback (`rmse`) (MET-1,
  MET-11).
- Earlier AI triage, 2026-10-19, measured: `claimcst0` is 0 exactly where `clm` = 0 (93.2%); no cost below 200 and 15%
  of the claims exactly 200; untuned LightGBM: AUC 0.64 for a claim, R^2 0.006 on log1p cost.
- Risks for /add-dataset: drop `clm`, `numclaims` (target copies) and `X_OBSTAT_` (constant); whether the pile at 200 is
  a recording floor (a coded value in the positive part); `exposure` as a feature (the `fremtpl2` precedent: kept as a
  feature, capped at 1) or a weight, the family's open insurance-conventions question; 378 exact duplicate rows.
- Priority: gap 0 (insurance has 4 accepted datasets, one above the thin line), use case 0 (no decision named in what
  was read), source + (the book and its documented data), shape + (67,856 policies, mixed types), risk 0.

**Assessment (AI, 2026-10-30):** suggested call for policy question 3 of the zero-inflated review, where Andrej asked
for a call per dataset from its references and the domain's practice instead of one convention for the family (the
shared reasoning: a time exposure or a sum insured is a feature, and a rating-cell table weights the metric by its
exposure; negative amounts that are recoveries become 0; the source's metric first, else the normalized Gini as a
context metric, since RMSE on raw amounts follows a few large claims and a Tweedie or Poisson deviance needs positive
predictions; MET-10 as amended on 2026-11-02 (Andrej) later declined a family-wide metric, so each table's metric is
decided on its own); the curator
has the call.
- Target: `claimcst0`, the claim cost of the policy-year, as published; the pile at 200 stays as recorded.
- Exposure (0-1 policy-years): a feature, as in the `fremtpl2` call, since the contracted period is known when the
  policy is priced. Actuarial GLMs use it as an offset; a model given the feature can learn that effect.
- Negative amounts: none.
- Metric: normalized Gini as a context metric (MET-11): no source metric was found (the book was not read), and RMSE on
  the raw cost follows the few large claims (probe R^2 -0.02 on the raw cost). Fallback `rmse` if the curator prefers
  the default.
- Drop `clm`, `numclaims` and `X_OBSTAT_`; IID split (no dates, no ids).

CC (2026-10-30, Andrej): `Yes`, priority 5 (the AI screening had `TBD -> Yes`, priority 3; zero-inflated screening
review page).

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

**Assessment (AI, 2026-11-01):** added as `datasets/_dev/tabarena-v0pt2/australian_vehicle_insurance_2004_2005/` by /add-dataset with the full review panel; the open questions are in its `REVIEW.md`. Recommend shipping after the panel's text changes (made); only the forced random split (SPLIT-8, against your how_much_did_it_rain call) could still turn it to `No`. Measured, correcting the notes above: `exposure` is the observed share of a one-year contract, and some claims cut it short, so it is not the contracted term known at pricing; it stays as a feature under LEAK-11 with a note (the counterfactual Gini and the offset test are in the definition). Only chapter 1 and the contents of de Jong and Heller (2008) were read. The claim cost ships in dollars, scored by the normalized Gini as a context metric (MET-11); raw dollars or log1p is decided once for the insurance tables (its issue 5). Priority 3 (your 5 of 2026-10-30 was set before the measurements): gap + (insurance), use case 0 ("for example" actor, fit approximate), source +, shape +, risk - (issue 1 can turn it to `No`).

CC (2026-11-02, Andrej): the forced IID split ships (issue 1 (a)): "Forced group splits should be fine. Regarding forced IID, did you make sure there are no leaks? Whenever there are no leaks we can ship." Recorded in SPLIT-8 (amended 2026-11-02: a forced grouped split ships; a forced IID split ships only when the leak test across the random split finds none).

**Assessment (AI, 2026-11-02):** the leak test across the random split finds none: every row is a distinct policy and no row shares its outcome with another across the split (no policy split into two rows: 116 pairs of identical rating factors sum to 365 days against 102 for other sums; a split keeping identical rows together scores as the random one); the hidden-group probe finds no group; the claim indicator shows no dependence along the file order (lag-1 correlation 0.005), and training on earlier quarters of the file to test the next shows no drop. how_much_did_it_rain's `No` named a measured leak (hours of one storm on both sides); none is found here.

CC (2026-11-02, Andrej): `exposure` kept as a feature with its note (issue 2); recorded as the LEAK-10 case for time on risk cut short by the outcome (leak_checks.md, Mechanisms table): the cut is removed or fixed where the data locates it, kept with its measured size where it cannot. Here the cut cannot be located (no dates), and the traced part lowers the Gini (offset-only 0.1833 against 0.1824 free; uncut write-offs 0.31).

CC (2026-11-02, Andrej): the target scale as each file implements it (issue 5): this table ships the claim cost in dollars, the log1p tables keep log1p.

**Assessment (AI, 2026-11-02):** supersedes "the book not read" and "only chapter 1 and the contents were read" above. Andrej read the book (printed pages, 2026-11-02): Table 1.6 (pp. 15-16) confirms 67,856 policies, 4,624 with claims, `area` the area of residence (A-F unexplained), age the policyholder's; Sec. 7.3-7.4 fit claim occurrence by logistic regression with exposure (time at risk) in the link, and Sec. 7.6 compares by ROC AUC (0.662 against 0.548 without exposure) on the same data, a classification with no held-out split; Sec. 10.4 fits a zero-adjusted inverse Gaussian model to the raw claim amount with its zeros, selected by AIC; Sec. 8.3 and 10.5 explain Tweedie and multiple-claim models without fitting them here. So no source metric for this claim-cost regression was established, and the Gini's case stays Ye et al. (2022) and pricing practice, apart from the book's AUC. The book leaves open the 200 floor, paid or incurred costs and why exposures end early. Corrected in the definition and REVIEW.md (issue 3, resolved).

CC (2026-11-02, Andrej): the metric (issue 4): "Use Gini". `normalized_gini` on the claim cost as a context metric (MET-11), decided for this table (MET-10 as amended 2026-11-02); the screening's `rmse` fallback is struck. All issues of the REVIEW are now resolved.

CC (2026-11-02, Andrej): ship. Every issue of the REVIEW is resolved: the forced IID split after its leak test (issue 1), `exposure` kept (2), the book's claims corrected (3), the Gini for this table (4), the claim cost in dollars (5).

CC (2026-11-06, Lennart): decision D8 of the exposure study of 2026-11-05 (issue 6): the target is the claim cost per year insured (`claimcst0` / `exposure`, in dollars, identity scale), `exposure` the weight scoring column, the `weight` input of `normalized_weighted_gini` and the task's `sample_weight`, and never a feature (LEAK-41, MET-14, MET-15); the metric stays a context Gini, now weighted on the rate; the 7 rows at 1M dollars or more a year are kept. Supersedes Andrej's call of 2026-11-02 (issue 2: `exposure` kept as a feature with its note, the LEAK-10 case for time on risk cut short by the outcome) and changes the form of his Gini of the same day (issue 4: unweighted on the cost, now weighted on the rate). What sets the case apart is a measurement made after the call: the deviance on the claim counts shows the leak the slice Gini hid (47 to 82% of a free model's gain over a constant rate is leak); on the weighted Gini of the cost per year a free GLM scores 0.238 against 0.125 for honest quotes, and on the shipped splits `exposure` as a feature lifts an honest LightGBM from 0.059 to 0.149 (9 of 9). The alternative, the claim frequency with an exposure-weighted deviance, was not chosen.

**Assessment (AI, 2026-11-06):** supersedes the statements above that `exposure` is a feature known when the policy is priced (the 2026-10-30 body paragraph and assessment), that it stays a feature under LEAK-11 (the 2026-11-01 assessment), and that the target is `claimcst0`, the claim cost (the 2026-10-30 body paragraph and assessment, the 2026-11-01 assessment); see the CC of 2026-11-06 (D8, issue 6): the target is the claim cost per year insured, and `exposure` is only its weight, never a feature (LEAK-41).

**Assessment (AI, 2026-11-06):** review panel (full, re-review under LEAK-41, MET-14 to MET-16): ship after changes (text only, made; rows, features, target, weight, split and metric unchanged); disputed: `gender` kept while bemtpl97 dropped `sex` (issue 7), a hold or an exception under MET-14's per-contract clause, to be settled once with spanish_motor_insurance_2015_2018 issue 7 (issue 8), the age bands as numbers or ordered categories (issue 9); for the curator: issues 7, 8 and 9.

CC (2026-11-08, Lennart): issue 9 of the folder's REVIEW.md, "Ordered categories": the two age bands ship as ordered categories, youngest first, `vehicle_age_band` with levels 1 to 4 and `driver_age_band` with levels 1 to 6; the codes stay the levels, as the band limits are published nowhere (CLEAN-14: bands of a quantity). Until now they shipped as integers, which no curator had decided.

**Assessment (AI, 2026-11-08):** applied in `_feature_types` (`ordinal`); rows, target, weight, split and metric unchanged. `dataset check`: 0 errors, 0 warnings; the dtype probe flags 0 of 6 columns.

CC (2026-11-08, Lennart): issue 7 of the folder's REVIEW.md, "Option C: Drop gender, as bemtpl97", then (a) on the consistency check: "A stance for the family; as if we were to simulate the case in europe always". `gender` leaves the features: sex is no rating factor of any insurance pricing task of this collection, whatever the actor's jurisdiction, as under EU law (Test-Achats, CJEU C-236/09, in force for new contracts from 21 December 2012); the Tensions row on rating factors in principles.md is amended so (2026-11-08, Lennart, this case). Supersedes Andrej's ship of 2026-11-02 (CC of that day), which kept `gender` among the six rating factors.

CC (2026-11-08, Lennart): issue 8 of the folder's REVIEW.md, (a) on the answer: "Keep the current target, the clause amended". The target stays the claim cost per year insured, `exposure` its weight, scored by the exposure-weighted Gini: decision D8 of 2026-11-06 stands. MET-14's per-contract clause is amended in one change with spanish_motor_insurance_2015_2018's issue 7: a per-contract target needs the data to record each contract to its end; this extract records 98.1% of its one-year contracts only in part (0.469 of a year per contract on average), so the rate ships.

**Assessment (AI, 2026-11-08):** both applied in the definition (target, weight, metric and split design unchanged). `gender` is dropped in `_clean`; five rating factors remain. It carried little: a Tweedie GLM scores 0.124 with it and 0.119 without (+0.004, SE 0.002, higher with it on 7 of 9 shipped splits), a regularised LightGBM 0.103 either way. Dropping a column changes the rows' content order and so the shipped splits; on the new splits the Tweedie GLM scores 0.119, the 300-round Tweedie LightGBM 0.075 and the L2 LightGBM 0.076, each above the weighted constant on 9 of 9; `exposure` as a feature adds +0.071 to +0.119 (9 of 9), 1/exposure alone 0.206. Task probe: linear 0.117 against the dummy's 0 (5 of 5 splits), `no_signal` on the R^2-type skill as before. Leak probe: no single feature or shallow tree scores; 56.3% of the test rows have an exact copy of their five factors in train (coarse rating cells; grouped by them the GLM scores 0.133, the LightGBM 0.077). Probe 22: the factors predict the exposure at R^2 0.076; the exposure as a feature gains +0.078 (L2) and +0.062 (Tweedie); no factor gains through it above noise. Hidden groups: none. Issue 8 on the new splits: a model of the window scores 0.056 Gini on the cost per contract (the GLM 0.124) and -0.034 on the cost per year; on the claims per year the GLMs and a regularised LightGBM tie (-0.0003, GLM ahead on 4 of 9); on the weighted Gini of the cost per year the GLM leads it by +0.016 (8 of 9; +0.031 on the old splits). `dataset check`: 0 errors, 0 warnings.

CC (2026-11-08, Lennart): the declared metric (`normalized_weighted_gini` on the cost per year insured, weighted by `exposure`) is checked, as declared on the PR #47 review board; the target kept in issue 8 (a).

CC (2026-11-09, Andrej): columns held only for training rows stay out for now, no training-only role (cross-dataset item of 2026-11-09; MET-14, LEAK-41, MET-16); the notes list them.

CC (2026-11-09, Andrej): the training labels' maturity is stated in the notes (cross-dataset item of 2026-11-09, option B).

CC (2026-11-09, Andrej): `gender` ships again as a rating factor (issue 10 of the folder's REVIEW.md; the cross-dataset item of the information audit, option a: "If the EU bans it today, we treat it as if it also has been banned before. For non-banned countries, we use it.", then "I go with a."). Sex leaves an insurance pricing task when the law of the country the data come from bars it today, as if the ban had always applied, and stays where that law allows it; Australian law allows it (Sex Discrimination Act 1984 (Cth), s41). The Tensions row on rating factors in principles.md is amended so. Supersedes Lennart's CC of 2026-11-08 on issue 7, which dropped `gender` under the family stance.

**Assessment (AI, 2026-11-09):** applied in the definition: `gender` is back among the six rating factors (target, weight, metric and split design unchanged; adding the column changes the rows' content order and so the shipped splits). s41(1) of the Sex Discrimination Act 1984 (Cth), compilation of 1 November 2025, read: discrimination on the client's sex in the terms of an insurance policy is not unlawful when it is based on actuarial or statistical data from a source on which it is reasonable for the insurer to rely and is reasonable having regard to the data. On the new splits, every fit weighted, `gender` adds +0.004 to a Tweedie GLM (0.133 against 0.130, SE 0.001, higher with it on 7 of 9) and nothing above noise to boosting (-0.007 to +0.002 over four LightGBM settings, the regularised ones over 3 seeds). `dataset check`: 0 errors, 0 warnings; the leak probes, the weight-proxy and shared-unit probes, the hidden-group and dtype probes find nothing; the task probe's linear family scores 0.122 on the declared metric against the dummy's 0 (5 of 5 splits).

## Reference

De Jong P., Heller G.Z. (2008). Generalized Linear Models for Insurance Data. Cambridge University Press.
doi:10.1017/CBO9780511755408. Distributed as `dataCar` in the R package insuranceData (Wolny-Dominiak A., Trzesiok M.,
2014) and as `ausprivauto0405` in CASdatasets (Dutang C., Charpentier A.).

Lead: the two-regime-zero workbook (v4, 2026-10-19), Master rows 61 (dataCar / insuranceData) and 30 (Insurance
ausprivauto0405).
