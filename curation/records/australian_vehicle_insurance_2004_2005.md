---
unique_name: australian_vehicle_insurance_2004_2005
name: dataCar (insuranceData) / ausprivauto0405 (CASdatasets) / Car (de Jong and Heller 2008)
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
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

## Reference

De Jong P., Heller G.Z. (2008). Generalized Linear Models for Insurance Data. Cambridge University Press.
doi:10.1017/CBO9780511755408. Distributed as `dataCar` in the R package insuranceData (Wolny-Dominiak A., Trzesiok M.,
2014) and as `ausprivauto0405` in CASdatasets (Dutang C., Charpentier A.).

Lead: the two-regime-zero workbook (v4, 2026-10-19), Master rows 61 (dataCar / insuranceData) and 30 (Insurance
ausprivauto0405).
