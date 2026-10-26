# diabetes_3

**Outcome:** added. The 442 patients of Efron, Hastie, Johnstone and Tibshirani (2004), from the authors' own
unstandardised file with their column names, as a regression of "a quantitative measure of disease progression one
year after baseline" on a random split of patients (RMSE). Not built yet. Verdict (mediator): ship once you rule
on USE-5 (ruled 2026-10-21: USE-5 amended, ship as approximate). Validity: SEL-1 and SEL-2 hold; USE-1 and USE-2 hold; USE-8 met with `fit="approximate"` (a
stand-in, the gap named); USE-5 met under its amendment of 2026-10-21 (no source says what the label measures, and no
measurement shows it is wrong; shipped approximate with the gap named); the LEAK rules hold; SPLIT-1 holds (one row per patient, random split); PROV-1 not
triggered (a named paper and the authors' page), PROV-2 keeps the doubt about the cohort with a note; PROV-13 and
LEAK-30 met by shipping the authors' file instead of the copies on OpenML and in scikit-learn, which are scaled over
all 442 rows. Value: not trivial (TP-4), a tiny-data task (TP-5). Quality: renames only; `sex` codes 1 and 2 kept as
categories; target on its raw scale. Weighed: source and signal for; label, cohort, size and a familiar teaching
dataset against.

**Main points:** The USE-5 question (the panel's issue 1) is settled by rule (2026-10-21, Lennart: USE-5 amended, the
label ships as approximate with its note; recorded as a CC line). Left: the two record fields below.

**Record fields that disagree with the definition:**

- `source_links`: record `OpenML 44223, NCSU copy`, definition `DOI of the paper, the authors' LARS page`.
- `decision_markers`: record `Trivial`, definition `none (not trivial on 60 of 60 splits)`.

**Record judgment:** valid. The data trace to a peer-reviewed paper and the authors' page, which
has served the same file since 2003; what the label measures, the clinic, the units and the inclusion rule are
documented nowhere, which USE-5 as amended on 2026-10-21 admits with fit approximate. The record's `source_links` name a scaled re-upload (OpenML 44223) and a later copy; under
PROV-8 (Must) the DOI and the LARS page come first, and OpenML 44223 moves to the comments as the copy scaled over all
rows, as for nyc_taxi_trip_duration and melbourne_housing_market. The `Trivial` marker has no proof under TP-4 (Must):
the best single feature, chosen on the training side, stays below least squares, ridge and a random forest on all 60
shipped splits (mean R^2 0.31 against 0.48, by at least 0.08), as in the kept cases aps_failure, california_house_prices_2020
and sepsis_survival_minimal_clinical_records.

**Review panel:** ship after changes, once the curator rules on USE-5 (mediator). Claim audit: most claims hold;
three wordings were corrected (the counts of the naming check, the margin over the best single feature, a section
number); what the label measures is untested, as no source defines it. Column and split audits: no leak, the random split is
right. Practitioner: approximate, not direct. Blind review: include with changes; main concern the undefined target.
Debate: agreed on everything but USE-5 (the reports' issue 1, settled by rule on 2026-10-21); their issue 2 (`Trivial`) is
the `decision_markers` row; their issues 5 (`sex` codes) and 6 (raw target) are agreed as implemented and left out.

<details><summary>Claim audit</summary>

Sources downloaded: the Wayback captures of 2002, 2021 and 2026, the NCSU copy, the OpenML arff and the arXiv TeX of Efron et al. 2004; models run on the 60 shipped splits. Licence never used as evidence (EV-4).

**Table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1-2 | Question / use case: baseline prediction of progression one year later, for future patients | DP task_summary | Paper TeX Sec. 1 | holds | "accurate baseline predictions of response for future patients" (Sec. 1); the decision ("plan follow-up") is ours, not the paper's | USE-1 |
| 3 | One patient per row, 442 patients | DP | Shape, duplicates | holds | 442 rows, 0 duplicate rows, 0 duplicate feature rows; no id to test "one per patient" further | SPLIT-1 |
| 4 | Target 25-346, undocumented measure | DP | Range; paper grep | holds | 25-346; paper: "a quantitative measure of disease progression one year after baseline", nothing more | USE-5 |
| 5 | Known: 10 baseline measures | DP | Paper Table 1 + Sec. 1 | holds | "Ten baseline variables ... average blood pressure and six blood serum measurements" | LEAK-1 |
| 6 | Split: random patients | DP | 60 splits, nn distance | holds | 20x3; min standardised test-to-train distance 0.46 vs median 1.44 (train-train 1.44): no copies | SPLIT-1, LEAK-16 |
| 7 | fit = direct | DP | none possible on data | untested | fit_reason itself says measure, clinic and units undocumented; a judgment (approximate is defensible) | USE-8 |
| 8 | Glucose looks low | DP | Value counts | holds | max 124, tail smooth (109:8 ... 124:3), no pile-up at a cutoff | PROV-1 |
| 9 | Year 2002, DOI source_url | DP | Wayback CDX | holds | first capture 2002-11-08 (www-stat.stanford.edu) | PROV-8 |
| 11 | Paper names Hastie's page (Sec. 7) | DP | TeX | holds | Sec. 7 "Computations": "www-stat.stanford.edu/~hastie/Papers/; the diabetes data also appears there" | PROV-8 |
| 12 | Host refuses; Wayback live 2026-08-04, same file | DP | curl; CDX | holds | hastie.su.domains: no connection today (code 000); capture 20260804203454 status 200, digest SICPCB... | PROV-9 |
| 13 | 2021 capture = 2010 = 2026 = NCSU, md5 af0c... | DP | Download + md5, CDX digests | holds | 2021, 2026, NCSU and local file all af0c583c...; CDX 20100815 same digest; 63 captures with that digest since 2003-06-24 | PROV-9 |
| 14 | Citation | DP | TeX header | holds | authors, Ann. Statist. 32(2) | - |
| 15, 29, 33 | Names spell out the 2002 headers; "the 2002 version of the same file" | DP, REC | Downloaded the 2002-11-08 capture | holds, with a fact the definition does not state | 2002 header `age sex bmi map tc ldl hdl tch tg glu y` confirmed; but the 2002 file is not the same file: `tg` is raw triglycerides (whole numbers 26-449) and `sex` is 0/1; every other column equal on 442/442 rows; ln(tg_2002) = S5 within 5e-5 on 442/442 | PROV-2, PROV-13 |
| 16 | 442 patients, headers AGE..Y | DP | read | holds | 442 x 11 | - |
| 17 | Prediction point baseline, no column dropped | DP | Paper Sec. 1 | holds | all ten are "baseline variables" | LEAK-1 |
| 18 | OpenML 44223, sklearn default, lars ship scaled | DP | arff download; sklearn | holds (OpenML, sklearn); lars untested | arff row 1: 0.038, 0.0507, ... 151.0; sklearn scaled = raw standardised / sqrt(442) (max diff 2e-16); `load_diabetes(scaled=False)` equals our file exactly | PROV-13 |
| 19 | "The data confirms them row by row" | DP comments | Recompute | refuted as worded (minor) | Friedewald 438/442 (devs 0.2, 0.4, 0.4, 0.2); S4 = rounded S1/S3 on 429/442: 11 misses sit at the .5 boundary, 2 are far off (row 115: 7 vs 6.38; row 216: 8 vs 7.36); BP thirds 442/442. "S5 = ln(tg)" is now proven directly from the 2002 file, 442/442 | writing.md, EV-6 |
| 20 | LDL and ratio computed from others | DP | as 19 | holds | see 19 | CLEAN |
| 21 | Sex coding undocumented | DP | TeX grep | holds | paper gives none | CLEAN |
| 22 | Ratio decimals 62, BP thirds 42 | DP | count | holds | 62 and 42 (crosstab 39 both, 23 ratio only, 3 BP only) | - |
| 23, 34, 38 | Glucose 58-124, mean 91, 0 >= 126, 94 in 100-125, 348 < 100; median BMI 25.7, tg 102 | DP, REC, REVIEW | count | holds | 58-124, 91.3, 0, 94, 348; BMI 25.7; tg 101.5 | PROV-1 |
| 24 | Target skew 0.44, RMSE matches least squares | DP | skew | holds | 0.441 (bias-corrected), log -0.331 | EV-5 |
| 25 | IID: no trend in file order, no missing, no duplicates | DP | Spearman, quarter means | holds | Spearman 0.048 (p 0.32); quarter means 146, 151, 149, 162; 0 missing, 0 duplicates | SPLIT-1 |
| 26, 36 | On all 60 splits best of OLS/ridge/RF (0.49) beats best single feature (0.30) by >= 0.097 | DP, REC | Own run: single feature chosen by 5-fold CV on train (linear and LightGBM), vs OLS, RidgeCV, RF | holds (conclusion); margin is method-dependent | 60/60; mean 0.484 vs 0.307; min gap 0.082 (not 0.097); LightGBM all-features 0.430, RF 0.442 | TP-1 to TP-4, EV-8 |
| 27 | 20 x 3 IID | README | from_definition | holds | 20 repeats, 60 splits | SPLIT-1 |
| 28, 10 | Licence none stated | DP | - | not evidence | EV-4 | EV-4 |
| 30 | Format R^2 0.0009 | DP decision 2 | recompute | holds | 0.00091 (ratio), 0.00042 (BP) | LEAK-27 |
| 31-32 | Record front matter and CC | REC | read | holds | as listed | - |
| 35 | No source gives clinic, units, response | REC | TeX grep (mg, clinic, hospital, units, glucose) | holds | no hit except "original units" of the coefficients | PROV-1 |
| 37 | Priority 1 | REC | - | untested (judgment) | - | - |
| 39 | Paper's in-sample R^2 about 0.50 (Sec. 3.4) | REVIEW issue 2 | TeX; OLS fit | refuted (section, minor) | the "R^2 =. 0.50" is in Sec. 3.3 (LARS-OLS hybrid, under "Other LARS modifications"); full OLS in-sample R^2 0.518 | writing.md |
| 40 | Code 1 HDL 54.4 vs 44.6; 2002 codes 0/1 | REVIEW issue 5 | groupby; 2002 file | holds | 54.4/44.6, BP 91.5/98.2; 2002 sex 0 = code 1 (235), 1 = code 2 (207) | CLEAN |
| 41 | AIC 5221.9 lognormal vs 5343.0 exponential | REVIEW issue 6 | Reproduced with the check's code; proper fits | holds as a printout, numbers are artefacts | `dataset_checks.py` L299-305 fit `loc` then drop it; with loc=0 lognormal 5057.7, exponential 5171.2, normal 5098.3, gamma 5042.1. The hint is weak support for logging | EV-9 |

**Unwritten claims**

| Claim | Test | Result |
|---|---|---|
| Every feature known at prediction point | paper Sec. 1 | holds (all baseline; derived LDL and ratio are same-visit labs) |
| Split the use case needs | no dates or sites in the file | holds as the best available (IID) |
| Target is the real-world target | no source defines y | untested: cannot be settled from data or paper (PROV-1, USE-5) |
| No copy across the split | exact and nn distances | holds |

**Refuted and untested, ranked (principles.md: validity first, Must first)**

1. Untested, validity (USE-5 / PROV-1): what y measures and who the cohort is. No data test exists. Changes nothing new
   (existing issue 1). Mildest remedy: keep the note; ask Efron/Hastie, or retire if the curator weighs 4E.
2. Untested, validity (USE-8): `fit="direct"` while the target is undocumented. Mildest remedy: `approximate`, or
   keep with the reason. For the critic and the mediator.
3. New fact, quality (PROV-2 / CLEAN): the first publication (2002-11-08) carries raw triglycerides in whole mg/dL and
   sex 0/1; the shipped file (since 2003-06-24) has ln(tg) to 4 decimals and 1/2. Lossless (exp recovers the
   integers), so no validity effect. Mildest remedy: a sentence in curation_comments citing the direct check
   (ln(tg_2002) = S5 on 442/442); optionally ship `triglycerides` = round(exp(S5)).
4. Refuted wording (writing.md): "confirms them row by row" -> "on 438/442 (LDL), 429/442 (ratio) and 442/442 (BP)
   rows; S5 = ln(tg) on 442/442 against the 2002 file".
5. Refuted citation (writing.md): REVIEW issue 2 cites Sec. 3.4; it is Sec. 3.3.
6. Numbers soft (EV-8): "at least 0.097" is one method's margin; an independent run gives 0.082. Remedy: "at least
   0.08".
7. Code issue outside this folder (EV-9): the distribution hint's AIC drops the fitted loc; REVIEW issue 6 numbers
   should be read as the check's printout, not fitted AICs.

</details>

<details><summary>Column audit</summary>

Prediction point (first `curation_comments` bullet, `task_summary`): the baseline visit; the target is a quantitative
measure of disease progression one year later (Efron et al. 2004, Sec. 1: "Ten baseline variables ... were obtained for
each of n = 442 diabetes patients, as well as the response of interest"). There is no codebook beyond that sentence,
Table 1 and the 2002 headers `age sex bmi map tc ldl hdl tch tg glu y`; units are documented nowhere.

Data: the frame through `dataset_io.load(..., built=True)` (origin `rebuilt`, IID, 60 splits, 442 x 11), and the raw
`diabetes.data` (md5 af0c583c...).

**Column table**

| column | meaning | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| age | age in years (19-79) | yes, baseline (paper Sec. 1) | int64, whole numbers, no missing | fine | LEAK-10, CLEAN-14 |
| sex | sex, codes 1/2 (235/207); which is which undocumented. Code 1 has HDL 54.4 vs 44.6 mg/dL, so 1 = female is likely (inference) | yes, baseline | category (2 levels), no missing | fine; labelling the codes is a question for the curator (REVIEW issue 5) | CLEAN-14, CLEAN-12 |
| bmi | body mass index, kg/m^2 (18.0-42.2) | yes, baseline | float64; 378 rows with one decimal, 64 whole (a format batch; target R^2 0.0021, p 0.27) | fine | CLEAN-14, LEAK-13 (no class difference) |
| mean_arterial_pressure | average blood pressure (`map`, "BP"), mmHg (62-133) | yes, baseline | float64; 400 whole, 42 in thirds (.33/.67), as (SBP + 2 DBP)/3; format vs target R^2 0.0004 | fine | CLEAN-14, LEAK-13 |
| total_cholesterol | serum total cholesterol (`tc`, S1), mg/dL by value (97-301) | yes, baseline | int64 | fine | CLEAN-14 |
| ldl_cholesterol | LDL (`ldl`, S2), the Friedewald estimate tc - hdl - tg/5 (438/442 within 0.1; the 4 others within 0.4) | yes, computed per row from baseline values | float64; one decimal, whole exactly when tg is a multiple of 5 (89/93 rows) | fine; a derived column, not a copy of one column, and one of the paper's ten covariates | CLEAN-5 (not triggered), LEAK-30 (per-row transform, fine) |
| hdl_cholesterol | HDL (`hdl`, S3), mg/dL (22-99) | yes, baseline | float64, 441 whole and one row 42.5; could be int but a float is harmless | fine | CLEAN-14 |
| total_cholesterol_hdl_ratio | total cholesterol / HDL (`tch`, S4) | yes, per row from baseline values | float64; 380 rows whole, 62 with 1-2 decimals. Of the 13 rows the naming check misses, 8 are whole-number roundings of ratios at x.47-x.50 (consistent with HDL rounded after the ratio was taken), 3 are one-decimal truncations, 2 (rows 115, 216 of the raw file) off by more | fine; mixed precision is a source format with no target signal (R^2 0.0009), kept as written | CLEAN-21 (one scale: holds), LEAK-13 |
| log_triglycerides | natural log of serum triglycerides (`tg`, S5); exp gives whole mg/dL values 26-449 on 442/442 rows | yes, baseline | float64, 2-4 decimals; a per-row log the source applied | fine (could be shipped as triglycerides in mg/dL, but the log is the source's own variable and per-row) | LEAK-30 (per-row, fine), CLEAN-12 (not needed) |
| glucose | blood glucose (`glu`, S6), mg/dL by value (58-124); fasting or not undocumented | yes, baseline | int64 | fine as a column; the range (none >= 126) questions the cohort, not the column | CLEAN-14; cohort: PROV-1, USE-8 (REVIEW issue 1) |
| disease_progression_one_year (target) | "a quantitative measure of disease progression one year after baseline" (25-346); what it measures is undocumented | the outcome, one year after the prediction point | int64, no missing, not capped (max 346 once), skew 0.44, raw scale | fine as a target; meaning undocumented (REVIEW issue 1); log scale is a weighing call (REVIEW issue 6) | USE-5, CLEAN-16, LEAK-26 (no cap) |

**Leak and cleaning sweep**

* No column is recorded after the baseline visit; no missing values, so no outcome-driven missingness; no id column; no
  window column (LEAK-1, LEAK-2, LEAK-10 hold).
* Scaling over all rows (LEAK-30, probe 16): none. The definition uses the unstandardised file; no column has mean 0 and
  SD 1 or min 0 and max 1. The only transforms are per row (log of triglycerides, the ratio, Friedewald LDL), which
  LEAK-30 calls fine. Our `_clean` is a rename only, so LEAK-29 / CLEAN-7 hold.
* Number formats (probe 9 style, regression): BMI whole, BP in thirds, ratio with decimals, LDL whole: each target
  R^2 <= 0.0021, all four together 0.0052 in sample. No artefact carries the target (LEAK-13).
* Leak probe: all features R^2 0.406, best single 0.273 (bmi), shallow tree 0.343; drop-one costs at most 0.09 (bmi).
  No single column near the full model.
* Impossible or proxy values: none found (CLEAN-10, CLEAN-11). All ranges are physiologically plausible except that
  glucose looks non-diabetic, which is a cohort question.
* Row order: the shipped frame is shuffled (not in raw order), as CLEAN-23 asks.
* Derived columns: `ldl_cholesterol` and `total_cholesterol_hdl_ratio` are functions of other columns; kept as the
  paper's covariates (CLEAN-5 covers exact copies only; CLEAN-22 says width is no reason to drop).

**Problems, ranked (principles.md)**

1. **P3/P5, cohort and target meaning undocumented (PROV-1, USE-5, USE-8; already REVIEW issue 1).** Not a column
   defect: every column is a plausible baseline value, but `glucose` 58-124 mg/dL (none >= 126) and the undocumented
   response mean the data's population and target cannot be checked. Mildest remedy: keep with the existing
   `Anomaly, cohort:` note; the curator's call (keep or retire). The column audit adds nothing that changes it.
2. **Procedure (writing.md), "confirms them row by row" overstates the naming check.** The decision table gives 438/442
   (LDL) and 429/442 (ratio); the misses are rounding consequences (8 of 13 ratio misses at x.47-x.50, 3 truncations),
   with 2 ratio rows off by more. Remedy: reword the bullet to "on 438 and 429 of the 442 rows; the rest are rounding".
3. **P7, `sex` coding undocumented (CLEAN-12, CLEAN-14; REVIEW issue 5).** Categorical 1/2 is the safe form. HDL
   (54.4 vs 44.6) and lower BP for code 1 point to 1 = female, but that is an inference. Mildest remedy: keep the codes;
   optionally note the inference in the bullet. Labelling them is a question for the curator.
4. **P7, minor, no action.** `total_cholesterol_hdl_ratio` mixes whole and two-decimal precision; `hdl_cholesterol` is
   float with one non-whole value. Neither carries the target; keep as written (already noted for the ratio).

No leak found. Verdict on the columns: ship as defined; the open points are the cohort question and a wording fix.

</details>

<details><summary>Split audit</summary>

Data loaded through `dataset_io.load` (origin `rebuilt`). Probes read: hidden groups and task probes.

**Verdict: right, with notes**

**Regime against the use case (SPLIT-1, SPLIT-2, SPLIT-4)**

Use case: a physician predicts one-year progression for a new patient at the baseline visit. One row = one patient,
one prediction per row (SPLIT-23 trivially). A new patient is a new entity, but each entity has exactly one row, so a
random split already tests on unseen patients. IID declared; IID is right.

Temporal check (SPLIT-7, SPLIT-8): no dates, no visit order in the source; this is a cross-sectional cohort extract
(baseline + one fixed outcome), not a stream of signals, so not forced IID from temporal. File order vs y: Spearman
0.048 (p 0.32); no feature has an order trend at p < 0.01; y mean by file decile 134-174 with no drift. Under the
file order the score barely moves: ridge R^2 0.475 (3 contiguous blocks) and 0.462 (expanding, 3 windows) vs 0.480 on
the shipped splits; RF 0.411 / 0.375 vs 0.446. No label-delay question (one fixed horizon, all labels known).

**Folds (default protocol)**

20 repeats x 3 folds = 60 splits; train 294-295, test 147-148 rows; each repeat covers all 442 rows once; train and
test disjoint in all 60. Test-fold mean y 139-162 (overall 152). Fine for a tiny-data task (P6 judged elsewhere).

**Hidden groups and near copies (SPLIT-29, SPLIT-30, LEAK-16 to LEAK-21)**

hidden_groups probe: hits none; top candidate `glucose` gap +0.107 (fold sd 0.125), s_identity -0.017: a smooth
numeric, not an entity. Near copies: 0 clusters at similarity 0.7-0.9; 0 duplicate (feature) rows; nearest-neighbour
distance in standardised space min 0.48, median 1.36. Nothing to group on.

**Problems, ranked**

1. P4, note (SPLIT-30, SPLIT-31; minor). The two number formats (65 rows with a decimal cholesterol ratio or a blood
   pressure in thirds; spread over the file, 19.6% / 13.6% / 10.9% per third) may mark a second recording batch or
   site. Holding it out: ridge RMSE 59.3 (R^2 0.30, but the batch has lower y sd, 71 vs 78) against 55.2 on random
   65-row hold-outs; 16% of random hold-outs do as badly, so no evidence of a batch effect. It is not an entity new
   patients would lack. Remedy: none; mention at most as a candidate site-shift variant if the source ever names
   the sites.
2. Procedure, note (USE-8 context). `split` in task_summary says "new patients of the same clinic", but no clinic is
   documented (cohort issue 1 in REVIEW.md). Mildest remedy: "new patients from the same (undocumented) cohort".
   The split itself does not change.

No re-split, gap or filter needed.

</details>

<details><summary>Domain practitioner</summary>

Actor played: a diabetologist / diabetes-clinic physician at a patient's baseline visit, who would use a one-year
progression forecast to set the follow-up interval and how hard to intensify treatment (the definition's own
"for example to plan follow-up").

**Fit: approximate (not direct)**

One sentence: the moment (baseline) and the horizon (one year) match the paper's stated aim of "accurate baseline
predictions of response for future patients" (Efron et al. 2004, Sec. 1), but the label is an unnamed score on an
unnamed cohort, so it stands in for a clinical outcome nobody can name or act on, a known gap of the kind USE-8 calls
approximate (compare alfa_battle_2_0_task_2, a label without a stated definition/horizon; coffee_rating_prediction, a
stand-in label).

Not None: the source states a prediction aim for future patients, so USE-2 / SEL-3 (study only looking back) does not
apply. Not direct: USE-8 direct needs the rows, features, label timing and split to mirror the use case; here only the
label timing is documented. USE-9 offers no other well-defined use case for this data (no practitioner predicts "y" on
this scale), and the weighed factor "a use case rephrased only to excuse a gap" argues against keeping `direct`. The
definition's own fit_reason lists the undocumented measure, clinic and units, which is the text of an approximate fit.

**1. Inputs at the prediction point (USE-3, USE-6)**

Have, at baseline: age, sex, BMI, blood pressure, lipid panel (TC, LDL, HDL, TG) and glucose. All are baseline
measurements; no leak (checklist: leak probes pass). LDL (Friedewald) and TC/HDL are derived, as a lab report gives
them; harmless.

Missing, that I would always have at a diabetes visit:
- HbA1c: the measure diabetes care is run on; its absence is the largest input gap.
- Diabetes duration, type (1 or 2), current medication (metformin, sulfonylurea, insulin), which drive progression.
- Kidney function (creatinine/eGFR, urine albumin), smoking, previous HbA1c values (a known patient, USE-10).
Missing inputs do not make the task wrong (the source chose ten covariates) but they make the shipped task a weaker
model than the one I would build, so its errors are not the errors I would face.

Puzzling: `glucose` 58-124 with none >= 126 (record, REVIEW issue 1). If these are mg/dL fasting values, these are not
diabetics, or they are well controlled on treatment, or the unit/sample type is not what I assume. I cannot tell which
population the model applies to.

**2. The target (USE-5)**

"A quantitative measure of disease progression one year after baseline", 25-346, unit and construction unstated in
any source. USE-5 says "check how the source built its label before accepting it": it cannot be checked. I act on
something concrete: HbA1c above target (e.g. >= 7%), need for treatment intensification, onset of a complication.
For that I would want a probability of a named event, or a forecast of HbA1c with an interval; a number on an unknown
scale gives me no threshold to act on. The target is therefore a proxy of unknown relation to the decision. A log
target (REVIEW issue 6) does not change this.

**3. Rows and test data (USE-10, USE-11, splits)**

One row = one patient at baseline, one decision per patient: matches. Random IID split = new patients of the same
unknown clinic and period. In practice I would deploy on next year's patients or at another clinic; with no dates or
site the random split is the best available and consistent with the source, but by the weighed factor in use_case.md
("a random split of undated applications stays approximate") it is a stand-in for the forward deployment. Minor next to
the target.

**4. Would I use this model?**

No, not clinically. R^2 about 0.48 (task probe linear skill +0.485) on an outcome I cannot interpret, from an
undocumented cohort that may not be diabetic, without HbA1c. I would trust it only with: the definition of y, the
inclusion criteria and units, HbA1c and medication as inputs, and validation on a later or external cohort.
As a benchmark task it is honest about what it is: a real, non-trivial (not `Trivial`, checklist P6) tiny tabular
regression with real lab structure (Friedewald holds on 438/442 rows), a familiar textbook problem rather than a
simulation of a decision.

**Gaps ranked by how much they change the task**

1. Target undocumented (USE-5): what "progression" measures and on which scale is unknown, so no action maps to it.
   Changes the task from "predict a clinical outcome" to "predict an unnamed score". Largest.
2. Cohort undocumented and doubtful (USE-8 row population; PROV): glucose never reaches the diabetes threshold; clinic,
   period, inclusion rule unknown. Who the test data stands for is unknown.
3. Inputs a clinician always has are absent (HbA1c, duration, medication, kidney function, history; USE-3, USE-10).
4. Split: random patients of one unknown clinic instead of later or other-site patients (weighed factor, USE-8).
5. Minor: `sex` coding undocumented (HDL by code suggests 1 = female; REVIEW issue 5); output is a point value scored
   by RMSE where I would want a probability or interval.

**What a domain expert would change**

- Set `fit="approximate"` with a fit_reason that names the gap: "the horizon and baseline inputs follow the paper, but
  the response, its scale, the clinic and the inclusion rule are undocumented and the glucose values do not look like
  a diabetic cohort; the label stands in for an unnamed clinical outcome" (USE-8).
- Keep the use_case marked as "for example" (USE-1 Methods: the source states the aim, not the decision); do not
  strengthen it.
- Nothing in the data can be redefined to a real target (USE-5 remedy unavailable without the original study).
- Whether an undocumented-label toy earns a place is a curator call (record assessment 2026-10-20: "adds little beyond a
  familiar toy benchmark"; retire is the stated alternative). From the practitioner side: keepable as approximate,
  not as direct.

**Sources**

- Efron, Hastie, Johnstone, Tibshirani (2004), Least Angle Regression, Ann. Statist. 32(2), Sec. 1
  (https://arxiv.org/abs/math/0406456; DOI 10.1214/009053604000000067): 442 diabetes patients, ten baseline variables,
  "a quantitative measure of disease progression one year after baseline", aim of baseline predictions for future
  patients; no clinic, units or response definition.
- scikit-learn diabetes description (https://api.openml.org/d/44187 mirror of sklearn's diabetes.rst): s6 = glu,
  blood sugar; features scaled; no further provenance.
- hsstan R docs (https://search.r-project.org/CRAN/refmans/hsstan/html/diabetes.html): cite the same paper and file.
- Diabetes progression practice: one-year progression defined by HbA1c and treatment intensification
  (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10588137/); baseline HbA1c and intensification drive glycaemic course
  (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6618330/).

</details>

<details><summary>Blind review</summary>

**Verdict: include with changes.** This is a real, small clinical regression dataset with modest signal. Keep it as a small-n regression case, but encode `sex` as categorical and document that the target is an undefined score.

**Task**
The table has 442 diabetes patients, each with 10 baseline variables. The target is "a quantitative measure of disease progression one year after baseline" (Efron, Hastie, Johnstone, Tibshirani, Ann. Stat. 2004, quoted on the NCSU page). A clinician could use such a prediction at the baseline visit to judge a patient's risk. In practice this is a statistics teaching set, not a model anyone deploys.

**Concerns (most to least serious)**
1. **The target is undefined.** No source says how "disease progression" was measured (it is an integer from 25 to 346, mean 152). Its clinical meaning cannot be checked. Change: state this in the documentation.
2. **The set is small and the signal is modest.** There are 442 rows. With 3-fold CV, R2 is 0.48 for RidgeCV and 0.44 for a random forest. The relationship is mostly linear, so the set mainly tells apart how methods do on small, noisy, near-linear data. With 20x3 repeated splits the scores are stable enough. Keep it, but count it as one of many small-data tasks.
3. **`sex` is stored as int64 with values 1/2.** It should be categorical or boolean. Change the type. There is no codebook saying which of 1 and 2 is male.
4. **Column names come from guesses.** The source labels S1 to S6 tc, ldl, hdl, tch, ltg, glu. The prepared names, including `total_cholesterol_hdl_ratio` for S4/tch, match the value ranges (S4 is about 2 to 9), but the original paper does not confirm them.
5. **The source is widely known.** It is the sklearn `load_diabetes` data (that copy is standardized; this one has the raw units), so it may already sit in the pretraining data of foundation models.

**Leakage, split, quality**
- All features are measured at baseline and the target is at one year, so I see no leakage.
- Random IID rows fit, since there is one row per patient.
- There are no duplicate rows, no duplicate feature vectors and no missing values. The values are plausible (BMI 18 to 42, MAP up to 133, age 19 to 79).

**Not checked**
- The OpenML page did not render, so I could not read its metadata.
- I could not check how patients were recruited, the time frame, or what the target instrument is.

</details>

<details><summary>Precedent check</summary>

Sources read: `principles.md`; the decision register (808 decisions, 4 flags); the Cases tables of provenance.md, use_case.md, task_probes.md, leak_checks.md, cleaning_features.md and selection.md; sibling records and definitions. The register links no diabetes_3 decision to any of its 4 flags. Flags 3 (scaling drift) and 4 (trivial outcomes) touch the mechanisms below and are discussed there.

The record has no dated curator decision (`CC`). Its curator lines are undated workbook comments: "Let us use the version of the data without normalization and the correct headers" and "Unclear in general, but should be fine as it is used so much". The rest are AI assessments (2026-10-07 and 2026-10-20) and the draft REVIEW.md issues 1, 2, 5 and 6.

**D1. Issue 1: keep despite the undocumented cohort, units and response (PROV-1, PROV-2 and USE-5, P5 and P3)**

**Status:** follows the precedents on the source; on the label it departs without a stated reason, and it may not be reasonable under the ranking because USE-5 is a Must.

**Source (PROV-1, PROV-2).**
- **PROV-1 "No" cases** (provenance.md Cases, undated): water_quality_and_potability, 3d_estimation_using_rssi..., calendardow. In all three every link ends at an anonymous re-upload. diabetes_3 differs on that very fact: it traces to a named paper (Efron et al. 2004, Annals of Statistics) and to the authors' own page, which has served byte-identical files since 2002. So PROV-1 does not fire.
- **PROV-2 keep:** bad_customer_detection (2026-10-14, Lennart), "a plausible source unclear in a detail: kept, with a note". The keep follows PROV-2 and this precedent. The `Anomaly, cohort:` bullet is the note.
- The draft issue's label "PROV-1 (criterion 4E)" overstates the rule that applies. The source question is a PROV-2 matter; what remains is a label question.

**Label (USE-5, Must: "Check how the source built its label before accepting it").**
- **blood_tests_drink_prediction** (UCI/BUPA; workbook era, undated; `Yes (Disagreement)`, shipped): men of unknown population; "how the number was recorded is not stated". It was kept with `fit="approximate"` and the markers Not Representative and No Good Target (yet). There the quantity is known (drinks per day) and only how it was recorded is unknown. In diabetes_3 the quantity itself is unknown ("a quantitative measure of disease progression"). No kept dataset has a label of unknown quantity.
- **mobile_churn** (open, REVIEW.md D1, 2026-10-20): the churn definition and the source are both unknown. That report found "no precedent has both gaps". diabetes_3 has only the label gap, but it is the same USE-5 question, so the two should be decided alike.
- **churn_telco_south_asia** (CC 2026-10-15, Lennart): kept with the churn timing as a stated risk. The label's meaning was known there, so it is only a partial precedent.
- **churn_telco_europa** (CC 2026-10-12, Lennart), "No: the data are not what the name says". This is the closest case of data not matching its claimed population. It is set apart by positive evidence: Chilean national ids, personal data, and actives and churners measured differently. For diabetes_3 the mismatch rests on reading `glucose` as fasting mg/dL, which is an inference (EV-2). No measurement contradicts the paper.

**Stated reason.** "used so much" is not a fact any rule accepts. The newer rulings (Lennart, 2026-10-12 and 2026-10-15, in the PROV-15 Cases) set aside reputation-type evidence: pretraining exposure, and other benchmarks' scores. bank_customer_churn ("Given the heavy usage ... we keep") is the only other keep resting on popularity. That makes two cases, not a third exception, but it is a drift candidate against those newer rulings. A rule-based ground exists for the source (PROV-2). None exists yet for the label.

**Third exception.** Keeps of a label whose construction is undocumented: blood_tests_drink (kept), diabetes_3 (draft keep), mobile_churn (pending). USE-5 is a Must, so these cannot be recorded as exceptions. If diabetes_3 and mobile_churn are both kept, an amendment of USE-5 is due. For example: "a label from a known publication whose construction is undocumented may ship with `fit="approximate"` and a note".

> **Consistency check (AI, 2026-10-20):** your call on diabetes_3 (keep, recorded as "should be fine as it is used so much") departs from USE-5 (Must): no source says what y measures. Two cases decide the same question: mobile_churn (open, churn definition unknown) and blood_tests_drink_prediction (kept, but its label's quantity is known). What sets diabetes_3 apart?
> (a) The label comes from a peer-reviewed paper by named authors who publish the rows, so its construction is undocumented but not anonymous. Recorded as the ground for keeping under PROV-2, with fit `approximate`.
> (b) Treat it like a USE-5 failure and retire it, or ask Efron/Hastie first.
> (c) Decide mobile_churn the same way.
> (d) Amend USE-5 to allow undocumented labels from known publications, with a note.

**D2. `fit="direct"` in the task_summary (USE-8, Must)**

**Status:** departs without a stated reason. This is an AI draft, not a curator decision.

**Precedents:**
- **blood_tests_drink_prediction:** `approximate`, because the population is unknown and the label's origin is unstated.
- **body_density_prediction:** `direct`, because the label is the costly test the use case replaces and is documented (underwater weighing).
- **USE-8 Cases:** direct for airfoil_self_noise, superconductivity and 2_month_survival_rate_prediction; approximate for account_debt, kick, alfa_battle_2_0_task_2 ("a label without a stated horizon") and coffee_rating_prediction.

**Comparison.** USE-8 calls a fit direct when "the rows ... and the label's timing ... mirror the use case". diabetes_3's own fit_reason says the measure, the clinic and the units are undocumented and the glucose values look low for diabetics. Those are the gaps blood_tests_drink was graded `approximate` for. The panel's checklist (P3 row) raises the same point.

> **Consistency check (AI, 2026-10-20):** diabetes_3 has `fit="direct"`, while blood_tests_drink_prediction, whose population and label origin are also undocumented, has `approximate`. What sets diabetes_3 apart?
> (a) The paper states the horizon (one year after baseline) and the prediction point. Recorded as the reason for `direct`.
> (b) Set it to `approximate` like blood_tests_drink, with the gap named ("an undocumented response measure and cohort stand in for a clinic's progression score").
> (c) Revisit blood_tests_drink.
> (d) Amend USE-8 to say where an undocumented label falls.

**D3. Issue 2: drop the `Trivial` marker (TP-4, Must)**

**Status:** consistent.

**Precedents:**
- **TP-4 Cases:** fitness_club (2026-10-05, retired; the single feature beat all 37 configurations); aps_failure, california_house_prices_2020 and sepsis_survival_minimal_clinical_records (2026-10-06, kept: the single feature stays below the methods). None of the kept three carries a `Trivial` marker today.
- **selection.md, "Reading decision markers":** a `Yes` with a concern marker is a provisional guess. The record's own line ("Unclear if too trivial?") is that kind of guess.

**Comparison.** The best single feature never matches the methods: 0 of 60 splits (R^2 0.30 against 0.49), and today's probe gives +0.24 against +0.48. So diabetes_3 falls with the kept cases, and dropping the marker follows them.

**Register flag 4** (aps_failure kept against anneal, haberman, fitness_club and churn_telco_south_asia_duplicate excluded) does not reach diabetes_3. anneal was solved perfectly; haberman is covered in D7.

**D4. Unscaled file instead of OpenML 44223 or scikit-learn (LEAK-30, PROV-13)**

**Status:** consistent. It takes the highest rung of the remedy ladder.

**Precedents:**
- **LEAK-30** (Lennart, 2026-10-19): "Rebuild from the unprocessed values when the source has them (PROV-13); otherwise keep with a note." Rebuilt: coad_colon_adenocarcinoma (retired 2026-10-16, replaced by tcga_coad_molecular_subtype) and sarcoma's methylation. Kept with a note (no unscaled original): bioresponse, taiwanese_bankruptcy_prediction, credit_card_customers, cooking_time_1m, delivery_eta_1m, maps_router_eta_1m and lung_cancer_epithelial_genexp (all 2026-10-19).

**Comparison.** The setting-apart fact is that the authors' unstandardised file exists. scikit-learn and OpenML centre and scale over all 442 rows; the definition avoids that. `log_triglycerides` (S5) and the cholesterol ratio (S4) are per-row transforms, which LEAK-30 explicitly allows. The curator's workbook note ("version without normalization") agrees and predates the rule.

**Register flag 3** (coad excluded on 2026-10-16 against the keeps of 2026-10-19) concerns the keep-or-exclude rung. diabetes_3 sits on the repair rung, so it is consistent with both sides.

**D5. Issue 5: `sex` codes 1/2 kept as categories without labels (CLEAN-12, CLEAN-14, EV-2)**

**Status:** consistent. There is no direct precedent.

- No record or definition in the working copy has an undocumented sex coding. heart_disease_cleveland's coding is documented by UCI.
- CLEAN-12 reverses codes "with their labels". Here the labels exist only as an inference (the HDL and blood-pressure pattern), and EV-2 ranks inference last. Keeping the codes avoids writing an inference as fact. The choice changes nothing for a model, since the column is categorical either way.
- No prompt.

**D6. Issue 6: target on its raw scale (CLEAN-16, Should, "case by case")**

**Status:** consistent.

- **Logged:** heavy-tailed prices, durations and counts, such as house_sales, nyc_taxi_trip_duration, mercari_price_suggestion and blood_tests_drink_prediction (log1p of drinks).
- **Raw:** bounded measurement scales, such as body_density_prediction, concrete_compressive_strength, airfoil_self_noise, wine_quality and the qsar regressions.
- y (25-346, skewness 0.44) is not a price, duration or count, and the paper fits it by least squares.
- No prompt.

**D7. A classic tiny medical teaching dataset as such (TP-5, the "Tiny but real" tension, USE-2)**

**Status:** consistent with the keeps. One opposite outcome is set apart by stated facts.

**Keeps:**
- heart_disease_cleveland (CC 2026-10-06, kept; 303 patients, `Outdated` marker).
- south_africa_coronary_heart_disease (CC 2026-10-01, kept; ESL data, `Outdated`).
- body_density_prediction and blood_tests_drink_prediction (workbook era, shipped as `Yes (Disagreement)` with Not Representative, Outdated and similar markers).
- musk (2026-10-06, TP-5: a tiny-data task).

**Excludes:**
- **haberman_survival** (CC 2026-07-27, Lennart): No, with Trivial, Outdated and Not Representative: "essentially two features plus a temporal component", "no longer represents a real-world problem". diabetes_3 is set apart by 10 baseline features, a stated one-year horizon, and methods that spread (linear +0.485 against a single feature +0.24). It shares with haberman only a thin use case ("for example to plan follow-up"), which ties into D1.
- **titanic** (AI unverified, No): no decision fits, which does not apply here.

**Note, not a departure.** Its era siblings (heart_disease_cleveland, south_africa_chd, body_density, haberman) carry `Outdated`, and diabetes_3 does not. Markers are optional, so this is no departure; mention it only if the curator marks the siblings uniformly.

**D8. Uniqueness and sibling diabetes records (PROV-4 to PROV-7)**

**Status:** consistent.

- No other record uses the Efron/LARS data. I checked for 44223, Efron, LARS, load_diabetes and the NCSU link.
- The 13 other diabetes records are distinct cohorts and tasks:
  - diabetes (Pima: retired on ethics, CC 2026-07-27);
  - pima_indians_diabetes_database (Duplicate);
  - diabetes_duplicate (AHDS, Duplicate);
  - diabetes_prediction_dataset (Missing source information, Ethical Issue);
  - cdc_diabetes_health_indicators (No Good Target, CC 2026-10-15);
  - diabetes_2 and diabetes_us130 (Duplicate);
  - diabetes_130_us, early_stage_diabetes_risk_prediction and wids_diabetes_mellitus (Yes);
  - nhanes_undiagnosed_diabetes (candidate);
  - dare_to_women_tech_shecures_ai_for_diabetes_prediction (TBD -> Yes);
  - diabetic_retinopathy_debrecen (No, Image).

**D9. Record fields `source_links` and `year` (PROV-8, PROV-9, PROV-12)**

- **year 2002:** consistent with PROV-9 (first share of the rows, on the authors' page, before the 2004 paper). Compare airfoil_self_noise and first_principles_tully_fisher (2026-10-20, Lennart: year and source of first publication).
- **source_links:** departs from PROV-8 without a reason. They list OpenML 44223 (a scaled re-upload) and the NCSU copy, while the definition's source is the paper (DOI) and the LARS page. The same fix was made for nyc_taxi_trip_duration and melbourne_housing_market (2026-10-12: non-source links moved to the comments). This is mechanical; checklist draft issue 4.

> **Consistency check (AI, 2026-10-20):** the record of diabetes_3 lists OpenML 44223 and the NCSU copy as its source links, while PROV-8 (as applied to nyc_taxi_trip_duration and melbourne_housing_market, 2026-10-12) takes the first publication. What sets it apart?
> (a) Nothing; put the DOI and the LARS page first and move OpenML 44223 into the comments as the scaled copy.
> (b) Keep the links because the LARS host is down. The definition's download instructions already cover that, through Wayback and NCSU.
> (c) Change the rule (an amendment).

**Drift and amendments**

- **Drift candidate (Lennart, PROV-1/PROV-2):** popularity ("used so much"; bank_customer_churn "heavy usage") as a ground for keeping, against the 2026-10-12 and 2026-10-15 rulings that set aside reputation-type evidence. The keep rulings are undated, so drift cannot be measured. For diabetes_3, the keep can stand on PROV-2 instead.
- **Amendment watch (USE-5):** blood_tests_drink is kept, diabetes_3 is drafted as a keep, and mobile_churn is pending. A third keep of an undocumented label makes an amendment due (see D1 (d)).

</details>

<details><summary>Advocate</summary>

**1. The evaluation is honest: no leak, the right split, no copies (P4; LEAK-1, LEAK-10, LEAK-13, LEAK-30, SPLIT-1, SPLIT-29; all Must)**

- **Claim.** Every input is known at the prediction point. The split matches the use case.
- **Evidence.**
  - All ten features are "baseline variables" (paper Sec. 1; claim audit rows 5 and 17).
  - Leak probe: all features give R^2 0.406, the best single feature (bmi) 0.273. No column comes close to the full model (column audit).
  - The number formats carry nothing about the target: R^2 0.0009 for the ratio's format and at most 0.0052 for all four formats together.
  - One row per patient. 0 duplicate rows and 0 duplicate feature rows. The smallest test-to-train neighbour distance is 0.46, against a median of 1.44.
  - hidden_groups finds nothing.
  - File order against y: Spearman 0.048 (p 0.32). Contiguous-block splits score about the same as the shipped ones (ridge 0.475 against 0.480).
  - The split auditor's verdict: "right, with notes". No re-split, gap or filter is needed.
- **Why it outranks objections.** P4 is the principle that most often removes a dataset, and here every one of its Musts holds. The cohort question (point 4) is a separate P3/P5 matter. "Independent failures are not conflicts" cuts both ways: a doubt about the label does not make the evaluation dishonest.

**2. The data is faithful, from its first publication, and repaired from the origin (P5; PROV-3 Must, PROV-8/9, PROV-13 Must, LEAK-30 Must)**

- **Claim.** We ship the authors' own unstandardised file, not the scaled copies.
- **Evidence.**
  - The Wayback captures of 2010, 2021 and 2026 and the NCSU copy all have md5 af0c583c...
  - 63 Wayback captures since 2003-06-24 carry that digest.
  - The page was first captured on 2002-11-08 (claim audit rows 9-13).
  - The OpenML 44223 and scikit-learn copies are scaled over all 442 rows. `load_diabetes(scaled=False)` equals our file exactly.
  - It is real data: generated_probes raise no flag, and Friedewald LDL holds on 438 of 442 rows, as real lab data would.
  - It is unique: none of the 13 other diabetes records uses this data (precedents D8).
- **Rule and why it wins.** LEAK-30 (Lennart, 2026-10-19) says: "Rebuild from the unprocessed values when the source has them." This definition stands on the top rung of the remedy ladder (precedents D4, consistent). The critic cannot ask for a better version, because none exists.

**3. The source is known, so PROV-1 does not fire; PROV-2 keeps it with a note (P5; PROV-1 Must, PROV-2 Should, narrows PROV-1)**

- **Claim.** The doubt about the cohort is a detail of a known source, not a missing source.
- **Evidence.**
  - The data traces to a peer-reviewed paper (Efron et al. 2004, Ann. Statist.). Its Sec. 7 names the authors' page as the place of the data.
  - Every PROV-1 "No" case (water_quality, 3d_estimation, calendardow) ends at an anonymous re-upload. This one does not (precedents D1).
  - The glucose doubt rests on reading `glucose` as fasting mg/dL. No source gives the units. Under EV-2 that reading is inference, the lowest kind of evidence. No measurement contradicts the paper.
  - This sets it apart from churn_telco_europa, which was retired on positive evidence (national ids, actives and churners measured differently).
- **Rule and why it wins.** PROV-2 narrows PROV-1 within its scope: "a source that is plausible but unclear in a detail stays, with a note of what to clarify". The precedent is bad_customer_detection (Lennart, 2026-10-14). The `Anomaly, cohort:` bullet is that note.
- **Concession.** The workbook line "should be fine as it is used so much" is no ground; the newer rulings set reputation aside. The keep stands on PROV-2, not on popularity.
- **Small fix.** REVIEW issue 1 should cite PROV-2, not "PROV-1 (criterion 4E)".

**4. The use case is real, but the fit is approximate, not direct (P3; USE-1, USE-2, USE-5, USE-8; all Must)**

- **Claim.** An actor, a moment and an aim come from the source itself.
  - The paper asks for "accurate baseline predictions of response for future patients" (Sec. 1).
  - The horizon is fixed (one year after baseline). All inputs are baseline values.
  - USE-2 and SEL-3 (a study only looking back) do not apply. The practitioner calls the task keepable, and so does the blind reviewer ("include with changes").
- **Concession (USE-8).** `fit="direct"` is wrong by the definition's own fit_reason, which lists the undocumented measure, clinic and units.
  - The practitioner, the claim audit (row 7), the checklist (P3) and the precedents (D2, against blood_tests_drink_prediction) all agree on this.
  - Mildest remedy: set `fit="approximate"` and name the gap in the fit_reason: "an undocumented response measure and cohort stand in for a clinic's progression score". This is one field. The task does not change.
- **USE-5, the hard point.** I do not claim that USE-5 is met in full. We checked how the source built its label to the end of the search: one sentence, with no construction given (claim audit, "Unwritten claims"). Three things argue against exclusion:
  - (a) The USE-5 Cases that went against a dataset rest on a measured mismatch: corporate_credit_rating, where 17% of the checkable labels were wrong. Here nothing measured shows the label is wrong. The only fact is that it is undocumented.
  - (b) The kept precedent blood_tests_drink_prediction ships an undocumented label with `approximate` and markers. The precedent checker also notes that this makes an amendment of USE-5 due (D1, option (a) or (d)), and that mobile_churn should be decided the same way.
  - (c) The paper is the authors' own label, so there is no better label to redefine into.
- **Remedy ladder.** Keep with a documented note and `approximate`, and put the USE-5 reading to the curator as an amendment question. Retiring is the last rung and needs a Must that cannot be fixed. Whether an undocumented label from a named publication fails USE-5 is exactly the open question that the amendment settles.

**5. It is worth benchmarking: not trivial, methods spread, tiny but scorable (P6; TP-4 Must, TP-5 Must, TP-2/TP-3)**

- **Evidence.**
  - The best single feature, chosen on the training side, stays below OLS, ridge and RF on 60 of 60 splits: 0.307 against 0.484 on average, with a smallest gap of 0.082 (claim audit row 26).
  - Task probe: linear skill +0.485, RF +0.455, LightGBM +0.376, single feature +0.24.
  - Linear minus LightGBM is +0.109 (SE 0.009). Methods spread, and the gap is stable.
  - Folds have 147-148 test rows of a continuous target.
- **Rule.** TP-4 says `Trivial` needs proof, and the proof fails, as in the kept cases sepsis_survival, california and aps_failure (precedents D3). TP-5 and the "Tiny but real" tension say a small dataset is a tiny-data task (musk was kept). The parkinsons kind of failure (a handful of units per fold) cannot happen in a 442-row regression.
- **Fix.** Drop the `Trivial` marker from the record. Reword "at least 0.097" to "at least 0.08" (EV-8: the margin depends on the method).

**6. Cleaned to the expert state: a rename and nothing more (P7; CLEAN-7, CLEAN-12, CLEAN-16 Should, CLEAN-22, LEAK-29)**

- **Evidence.**
  - `_clean` is a rename. The names come from the authors' 2002 headers and are checked on the data: BP in thirds on 442 of 442 rows, Friedewald 438 of 442, ratio 429 of 442.
  - In the 2002 file, ln(tg) = S5 on 442 of 442 rows (claim audit row 15).
  - `sex` is categorical, not given a label from inference (EV-2; precedents D5).
  - The raw target matches the paper's least squares and the bounded-scale precedents (D6, consistent; skew 0.44). The AIC hint for a log target is an artefact of the check code (claim audit row 41, EV-9).
  - The derived LDL and ratio stay as the paper's covariates (CLEAN-22: width is no reason to drop).
  - The column audit's verdict: "ship as defined".
- **Fixes (quality rung, cheap, writing.md).** Each is a sentence:
  - "confirms them row by row" becomes "on 438 (LDL), 429 (ratio) and 442 (BP) of the 442 rows; the rest is rounding".
  - Add that the 2002 file had raw triglycerides and sex coded 0/1, a lossless conversion.
  - Change the task_summary's split text to "new patients of the same (undocumented) cohort".
  - REVIEW issue 2 should cite Sec. 3.3, not 3.4.

**7. The record's source_links are a mechanical fix, not a reason to hold the dataset (PROV-8; procedure)**

- **Evidence.** The record lists OpenML 44223 (scaled) and the NCSU copy. The definition already uses the DOI and the LARS page, with Wayback and NCSU as fallbacks.
- **Fix.** Put the DOI and the LARS page first and move OpenML into the comments. This is the same fix as nyc_taxi_trip_duration and melbourne_housing_market (2026-10-12; precedents D9, option (a)).
- **Why it does not weigh.** It is a record field, so it does not affect the folder.

**Judgment record (as I argue it)**

```text
Verdict: ship after changes.
Validity: SEL-1/2 hold; USE-1, USE-2 hold; USE-8 triggered, fixed (fit direct -> approximate, gap named); USE-5 open
  (label construction undocumented, no measured mismatch; amendment question with blood_tests_drink and mobile_churn);
  LEAK-* hold; SPLIT-1 holds (IID); PROV-1 not triggered, PROV-2 keep with the cohort note; PROV-13/LEAK-30 repaired
  from origin.
Value: TP-4 not trivial (0/60), TP-5 tiny but real; drop `Trivial`.
Quality: renames only; wording fixes (counts, 0.08 margin, split text, Sec. 3.3).
Weighed: source + (named paper, stable file since 2003), label -, cohort -, size -, gap - (familiar toy).
For the curator: the USE-5 reading for undocumented labels of known publications (keep as approximate or amend).
```

</details>

<details><summary>Critic</summary>

Position: do not ship as defined. Ship only after changes 1-2 (validity, Must) and the curator's recorded ground for
point 2; points 3-6 are cheap repairs. No point asks for exclusion unless the curator declines the ground in point 2.

**1. `fit="direct"` is wrong; it is approximate (P3, USE-8 Must)**

- Problem: USE-8 direct needs the rows, features, label timing and split to mirror the use case. Only the label timing
  (baseline, one year) is documented. The definition's own `fit_reason` lists the gaps: measure, clinic and units
  undocumented, glucose low for diabetics. That is the text of an approximate fit.
- Effect: the README tells the user the benchmark mirrors a clinical decision; it mirrors an unnamed score on an
  unnamed cohort.
- Evidence: practitioner.md ("keepable as approximate, not as direct"); precedents.md D2 (blood_tests_drink_prediction,
  same gaps, `approximate`; USE-8 Cases alfa_battle_2_0_task_2, coffee_rating_prediction); claim_audit #7 (untested,
  "approximate is defensible"); checklist P3 concern. USE-9 offers no other use case where y is a known label.
- Remedy (fix the definition): `fit="approximate"`, fit_reason naming the gap ("the horizon and baseline inputs follow
  the paper; the response, its scale, the clinic and the inclusion rule are undocumented, and the glucose values do not
  look like a diabetic cohort"). Also `split`: "new patients of the same clinic" -> "new patients from the same
  (undocumented) cohort" (split_audit note 2; no clinic is documented).

**2. The label cannot be checked, and the keep rests on popularity (P3, USE-5 Must)**

- Problem: USE-5 says "check how the source built its label before accepting it". The check was made and found
  nothing: no source says what y measures (claim_audit #4, #35; paper TeX grep). The only recorded curator ground,
  "should be fine as it is used so much", is reputation, which the 2026-10-12 and 2026-10-15 rulings set aside
  (precedents.md D1, Drift). No kept dataset has a label of unknown quantity (blood_tests_drink knows its quantity).
- Effect: the benchmark scores RMSE on a quantity nobody can name; a practitioner cannot map it to an action
  (practitioner.md section 2). A re-target is not possible (no other label in the data).
- Remedy, mildest that holds: the curator records a rule-based ground (precedents D1 (a): a label from a peer-reviewed
  paper by named authors who publish the rows, shipped as approximate with a note) and decides mobile_churn alike;
  with the third such keep, an amendment of USE-5 is due (D1 (d)). Asking Efron/Hastie is the repair rung. If the
  curator declines a ground, USE-5 is a Must that cannot be fixed and the remedy is `No` (`No Good Target`). Shipping
  with only the `Anomaly, cohort:` note is not an option under a Must.

**3. The task text states a cohort the data puts in doubt (P3/P5, USE-8 with PROV-2 Should; writing.md)**

- Problem: `question` and `row` say "a diabetes patient" as fact. Glucose 58-124, none >= 126, mean 91 (claim_audit
  #23; REVIEW_before issue 1). This is an inference on units (EV-2 ranks it last), so it is no exclusion ground, but
  PROV-2 asks for a note of what to clarify where the reader sees the task.
- Remedy (note): `row` "one patient the paper calls diabetic, at the baseline visit (clinic, units, period and
  inclusion rule not stated; glucose values below the diabetes threshold)". Relabel REVIEW issue 1 from "PROV-1
  (criterion 4E)" to PROV-2 / USE-5 (precedents D1: PROV-1 does not fire).

**4. Record `source_links` point to re-uploads (P5, PROV-8 Must)**

- Problem: the record lists OpenML 44223 (a scaled re-upload) and the NCSU copy; the source is the paper and the LARS
  page, as `source_url` already says.
- Evidence: precedents D9; checklist draft issue 4; nyc_taxi_trip_duration and melbourne_housing_market fixed the same
  way (2026-10-12).
- Remedy (repair the record): DOI and LARS page first; OpenML 44223 moved to the comments as the scaled copy.

**5. Comments overstate the checks (procedure, writing.md, EV-8)**

- "The data confirms them row by row": the decision table gives 438/442 (LDL), 429/442 (ratio), 442/442 (BP); 2 ratio
  rows (115, 216) are off by more than rounding (claim_audit #19, column_audit 2).
- "by at least 0.097": an independent run gives 0.082 (claim_audit #26).
- Remedy: reword to the counts and "at least 0.08".

**6. "The 2002 version of the same file" is not the same file (P5/P7, PROV-13; writing.md)**

- The 2002-11-08 capture has raw triglycerides (whole mg/dL) and sex 0/1; the shipped file has ln(tg) and 1/2.
  Lossless: ln(tg_2002) = S5 on 442/442 (claim_audit #15). No validity effect.
- Remedy (note): one sentence in `curation_comments` stating this and citing the direct check, which also replaces the
  Friedewald inference as proof that S5 is ln(tg).

**Not raised**

Leakage, split regime, copies, triviality (TP-4: 0/60 splits) and the raw-scale target all hold on the evidence; I
do not dispute them. Size (442 rows) is a tiny-data task (TP-5), not a reason to exclude.

</details>

<details><summary>Advocate rebuttal</summary>

**Critic 1: `fit="direct"` is wrong (USE-8 Must). Conceded.**
My brief already conceded this (point 4). I accept both remedies as worded:
- set `fit="approximate"` with the fit_reason the critic gives;
- change `split` to "new patients from the same (undocumented) cohort" (split_audit note 2).

What follows: USE-8 is triggered and fixed in the definition, and nothing else about the task changes.

**Critic 2: the label cannot be checked and the keep rests on popularity (USE-5 Must). Partly conceded, partly disputed.**

**What I concede:**
- "Used so much" is no ground, under the 2026-10-12 and 2026-10-15 rulings (precedents Drift). My brief did not rely on it.
- No kept dataset has a label whose quantity is unknown. blood_tests_drink_prediction knows its quantity (precedents D1), so it is a partial precedent, not a matching one.
- A rule-based ground has to be recorded by the curator, and mobile_churn must be decided the same way (principles, "Treat like cases alike").
- Asking Efron/Hastie is the repair rung and should be offered.

**What I dispute:** the claim that if the curator declines this ground, USE-5 is an established, unfixable Must failure, so the only remedy is `No`. Three reasons:
- **The ground is already there.** The critic's own mildest remedy is precedents D1 option (a): a label from a peer-reviewed paper whose named authors publish the rows, shipped as approximate with a note. That is what my brief proposes. The two remaining choices are recording (a) and amending USE-5 (d). Both are curator decisions on a weighing question, not a settled Must violation. The review-panel rule says "a weighing call goes to the curator", and the mediator should send it there rather than rule `No`.
- **What USE-5 has decided so far.** Its Cases reject a label on a measured mismatch: corporate_credit_rating, where 17% of the checkable labels were wrong. Its prescribed fix is to redefine the label, which is impossible here. No measurement shows that y is the wrong quantity for the paper's stated aim of "baseline predictions of response for future patients". Under EV-1 and EV-2, "undocumented" is not the same as "refuted". Whether USE-5 also excludes labels that cannot be checked is exactly the open reading the amendment watch names.
- **Independent failures are not conflicts.** I accept that this principle stops me from rescuing a USE-5 failure with P4 to P6 strengths. That is why I argue the reading of USE-5 itself, not a trade-off against those strengths.

What follows: the verdict is "ship after changes" if the curator records ground (a) or the amendment (d). If the curator declines both and Efron/Hastie give no answer, then I concede the outcome `No` (`No Good Target`).

**Critic 3: the task text states the cohort as fact (PROV-2, writing.md). Conceded, with one wording fix.**
`question` and `row` should not state "diabetes patient" as checked fact. The critic's replacement text, however, says "glucose values below the diabetes threshold" as a fact. That again rests on reading the units as mg/dL, which is inference and ranks last under EV-2.

My wording: "one patient the paper calls diabetic, at the baseline visit (clinic, units, period and inclusion rule not stated; read as mg/dL, no glucose value reaches the diabetes threshold)".

I also agree to relabel REVIEW issue 1 from PROV-1 to PROV-2 / USE-5. My brief made the same point (point 3).

**Critic 4: record `source_links` (PROV-8). Conceded.**
Same remedy as my point 7: put the DOI and the LARS page first, and move OpenML 44223 into the comments as the scaled copy.

**Critic 5: the comments overstate the checks (writing.md, EV-8). Conceded.**
Reword to the counts (438, 429 and 442 of the 442 rows) and change the margin to "at least 0.08". These are the fixes in my point 6. I add that rows 115 and 216, the two ratio misses beyond rounding, should be named in the note, since the critic is right that they are not rounding.

**Critic 6: the 2002 file is not the same file (PROV-13, writing.md). Conceded.**
Add one sentence to `curation_comments`: the 2002 capture carries raw triglycerides and sex coded 0/1, and ln(tg_2002) = S5 on 442 of 442 rows. That direct check replaces the Friedewald inference as the proof that S5 is ln(tg).

I would keep `log_triglycerides` as shipped. It is the source's own per-row variable (LEAK-30 is fine with it), and the critic does not ask for a change.

**Where we stand**
- **Agreed:** P4, P5 data integrity, P6 (not trivial: 0 of 60 splits) and P7. The critic's "Not raised" section concedes all of these.
- **Changes to the definition and record:** all six points above, which are cheap repairs.
- **Open:** one point only, critic 2. It is a curator weighing call or an amendment of USE-5, decided together with mobile_churn, not an exclusion ruled by rank.

</details>

<details><summary>Critic rebuttal</summary>

The two briefs now agree on almost everything. One point stays in dispute: whether the advocate's "ship after changes"
may assume the USE-5 outcome.

**Conceded**

- A1 (P4: no leak, IID split, no copies): conceded. I raised nothing against it.
- A2 (P5: authors' unstandardised file, first publication, unique, LEAK-30 top rung): conceded.
- A3, the source part: conceded. PROV-1 does not fire; PROV-2 keeps the cohort doubt about the *source* with a note,
  and REVIEW issue 1 should cite PROV-2. The advocate also drops the "used so much" ground, as my point 2 asked.
- A4, USE-8: agreed; `fit="approximate"` with the gap named (my point 1).
- A5 (P6: not trivial, tiny but real; drop `Trivial`; "at least 0.08"): conceded.
- A6 (P7 wording fixes, 2002 file sentence, split text, Sec. 3.3): agreed; these cover my points 5 and 6 and the split
  half of point 1.
- A7 (source_links): agreed on the fix. I accept that it is a record field and does not hold the folder; PROV-8
  is still a Must, so the record is fixed in the same change.

**Disputed**

**A4, USE-5: the verdict cannot be "ship" with USE-5 "open".**

- The advocate's argument (a): the USE-5 Cases that failed rested on a measured mismatch (corporate_credit_rating, 17%
  wrong). The rule's text is "check how the source built its label before accepting it" (use_case.md, USE-5 Must). A
  check that finds no construction at all is not a pass. Having no measured mismatch shows only that nothing could be
  measured (claim_audit, "Unwritten claims": "untested: cannot be settled from data or paper").
- The advocate's argument (b): blood_tests_drink_prediction is a precedent for keeping. precedents.md D1: its quantity
  is known (drinks per day) and only how it was recorded is not; "No kept dataset has a label of unknown quantity".
  It does not have the same facts, so it does not decide this case. A precedent also does not outrank a Must
  (principles.md, "Rules win over ... precedents").
- The advocate's claim 3 (PROV-2 carries the keep): PROV-2 narrows PROV-1, a rule about the source. It says nothing
  about the label. precedents.md D1: "A rule-based ground exists for the source (PROV-2). None exists yet for the
  label."
- What follows (principles.md, Strengths): a Must is not departed from by an exception. Either the curator reads USE-5
  as met for a label published by named authors, or USE-5 is amended (D1 (a)/(d)). Either way it is the curator's
  recorded decision, taken together with mobile_churn. Without that decision the dataset does not ship.
- Where we agree: the advocate and I ask for the same remedy, the curator's amendment question rather than
  exclusion. We differ only on the gate. The judgment record should read "Verdict: ship after changes, once the
  curator rules on USE-5", not "USE-5 open" under a ship verdict.

**A4 judgment record, "Weighed: source +".** Minor. A stable file and a named paper count for the source (PROV-2), but
they cannot offset the label under a Must ("no number of factors overrides a Must", principles.md).

No new facts.

</details>

<details><summary>Mediator</summary>

**Recommendation (judgment record)**

```text
Verdict: ship after changes, once the curator rules on USE-5 (issue 1). If the curator reads USE-5 as failed and the
  authors cannot clarify, then No (No Good Target).
Validity: SEL-1/SEL-2 hold; USE-1, USE-2 hold; USE-8 triggered, fixed (direct -> approximate, gap named);
  USE-5 undecided: the label's construction was checked and nothing documents what y measures, and no measurement
  shows it is wrong (curator: reading or amendment); LEAK-* hold; SPLIT-1 holds (IID 20x3); PROV-1 not triggered
  (named paper and the authors' page), PROV-2 keeps the cohort doubt with a note; PROV-13/LEAK-30 repaired from the
  origin (unscaled file); PROV-8 triggered on the record, fixed (source_links).
Value: TP-4 not trivial (0/60 splits; margin at least 0.08), TP-5 a tiny-data task; drop `Trivial`.
Quality: renames only; `sex` 1/2 kept as categories (EV-2); raw-scale target (CLEAN-16, D6); wording fixes.
Weighed: source + (peer-reviewed, named authors, same md5 since 2003), signal + (methods spread, linear - LightGBM
  +0.109, SE 0.009), label - (quantity undocumented), cohort - (inference only, EV-2), size -, gap - (familiar toy).
For the curator: issue 1, the USE-5 reading for a label from a named publication whose quantity is undocumented;
  decide it together with mobile_churn.
```

**Changes to make now (no decision needed)**

1. `fit="direct"` becomes `fit="approximate"`. The `fit_reason` names the gap: the horizon and baseline inputs follow the paper; the response, its scale, the clinic and the inclusion rule are undocumented; read as mg/dL, the glucose values do not look like a diabetic cohort. Rule: USE-8, Must. The definition's own fit_reason lists these gaps. Precedent: blood_tests_drink_prediction.
2. `split` reads "new patients from the same (undocumented) cohort", in place of "the same clinic". Rule: USE-8, plus writing.md: no clinic is documented.
3. `question` and `row` stop stating the cohort as fact. Use the advocate's wording: "one patient the paper calls diabetic, at the baseline visit (clinic, units, period and inclusion rule not stated; read as mg/dL, no glucose value reaches the diabetes threshold)". The question can say "a patient the paper calls diabetic". Rules: PROV-2 (Should, a note of what to clarify); EV-2 (the units are an inference). This is why the advocate's wording beats the critic's, which states the threshold as fact.
4. Record `source_links`: the DOI and the LARS page first. OpenML 44223 moves to the comments as the copy scaled over all rows. Rule: PROV-8, Must. Precedent: nyc_taxi_trip_duration and melbourne_housing_market (2026-10-12).
5. Remove the `Trivial` marker from the record. Rule: TP-4, Must: `Trivial` needs proof. The best single feature stays below the methods on 0 of 60 splits. Precedent: aps_failure, california, sepsis_survival.
6. Notes: replace "confirms them row by row" with the counts: 438 (LDL), 429 (ratio) and 442 (BP) of 442 rows. Rows 115 and 216, the two ratio misses beyond rounding, are named. Rule: writing.md, EV-8.
7. Notes: "by at least 0.097" becomes "at least 0.08". An independent run gave 0.082. Rule: EV-8.
8. `curation_comments`: the 2002 capture has raw triglycerides and sex coded 0/1. ln(tg_2002) = S5 holds on 442 of 442 rows, and this direct check replaces the Friedewald inference as the proof that S5 is ln(tg). Rule: PROV-13, writing.md.
9. REVIEW.md: issue 1 cites PROV-2 / USE-5, not "PROV-1 (criterion 4E)". Issue 2 cites Sec. 3.3, not 3.4. Drop "should be fine as it is used so much" as the ground for the keep. Reputation was set aside by the 2026-10-12 and 2026-10-15 rulings, and both briefs agree.

**Issues for the curator (ranked)**

**Issue 1 (P3, USE-5 Must, validity): the label's quantity is undocumented. Keep it, amend USE-5, ask the authors, or retire?**

- **Problem.** USE-5 says "check how the source built its label before accepting it". The check went to the end: paper, LARS page, NCSU copy and the 2002 capture. All any source says is "a quantitative measure of disease progression one year after baseline". No source gives the measure, the scale, the clinic or the inclusion rule. No other label exists in the data, so the mildest fix USE-5 offers (redefining the label) is not available.
- **Effect.** The benchmark scores RMSE on a quantity nobody can name, and a practitioner cannot map a prediction to an action. Evaluation honesty (P4) is not affected.
- **Why this is yours to decide, not mine by rank.** Neither side cites a rule that conflicts with USE-5. P4 to P6 strengths cannot rescue a Must failure (principles, step 4), and the advocate concedes this. So the question is only whether USE-5 is met. The rule's text and its Cases leave open whether a label that cannot be checked counts as a failure. corporate_credit_rating failed on a measured 17% mismatch; cirrhosis was a re-target. Settling that is a reading or an amendment of a Must, and that belongs to the curator.
- **Critic's best evidence.** A check that finds nothing is not a pass. No kept dataset has a label of unknown quantity: blood_tests_drink knows its quantity (drinks per day); only how it was recorded is unknown. PROV-2 covers the source, not the label. A Must takes no exceptions.
- **Advocate's best evidence.** "Undocumented" is not "refuted" (EV-1, EV-2). No measurement shows y is the wrong quantity for the paper's stated aim of "baseline predictions of response for future patients". The label is the named authors' own and comes with the rows. Retiring is the last rung of the remedy ladder, for a failure that is established and cannot be fixed.
- **Options.**
  - (a) Rule that USE-5 is met: the label comes from a peer-reviewed paper whose named authors publish the rows. Ship as approximate with the note.
  - (b) Amend USE-5, for example: "a label from a named publication whose construction is undocumented may ship with `fit="approximate"` and a note naming the gap". Decide whether it covers an unknown *quantity* (diabetes_3) or only an unknown *recording* (blood_tests_drink). This would be the third such keep, so an amendment is due.
  - (c) Ask Efron or Hastie what y is, holding the dataset meanwhile. This is the repair rung.
  - (d) Retire: `No`, `No Good Target`.
- **What would settle it.** A document or an author reply that defines y and the cohort.
- **Consistency.** Decide mobile_churn alike on USE-5. A keep under (a) or (b) does not by itself ship mobile_churn, though: it also has an independent PROV-1 failure (no traceable source), which diabetes_3 does not.

No other issue is open. REVIEW issues 5 (`sex` codes) and 6 (raw target) are agreed as implemented. Each is a Should with a precedent, so you can confirm them without a decision.

**Agreed facts**

- **Source.** Efron et al. 2004 (Ann. Statist.), Sec. 7, names the authors' LARS page. The first capture is 2002-11-08. The 2010, 2021 and 2026 captures and the NCSU copy all have md5 af0c583c..., and 63 captures since 2003 carry it. The shipped file equals `load_diabetes(scaled=False)`. OpenML 44223 and scikit-learn are scaled over all 442 rows.
- **Rows.** 442 rows, one per patient. 0 duplicate rows, 0 duplicate feature rows, no missing values.
- **No leak.** All features are baseline values. All features give R^2 0.406; the best single feature (bmi) gives 0.273. Number formats give R^2 at most 0.005. hidden_groups finds nothing. File order against y: Spearman about 0.05.
- **Not trivial.** The single feature stays below OLS, ridge and RF on 60 of 60 splits, by at least 0.08. Linear skill +0.485, RF +0.455, LightGBM +0.376, single feature +0.24.
- **Column names.** BP in thirds on 442 of 442 rows, Friedewald LDL on 438, ratio on 429 (rows 115 and 216 are off by more than rounding). ln(tg_2002) = S5 on 442 of 442.
- **Glucose (inference).** Glucose runs 58 to 124 with mean 91; none is at or above 126. Reading the values as mg/dL is an inference (EV-2), and no measurement contradicts the paper.
- **Target.** Range 25 to 346, skew 0.44. The raw scale matches the paper's least squares.
- **Undocumented.** No source documents y's construction, the units, the clinic or the inclusion rule.
- **Popularity.** "Used so much" is no ground.
- **Folder.** `fit="direct"` is wrong.

**Consistency with precedent**

- **Follows:**
  - bad_customer_detection (PROV-2 keep with a note);
  - LEAK-30 rebuild-from-origin cases (coad, sarcoma);
  - TP-4 kept cases (aps_failure, california, sepsis_survival);
  - "Tiny but real" (musk);
  - blood_tests_drink_prediction (`approximate`, D2);
  - nyc_taxi_trip_duration and melbourne_housing_market (source_links);
  - D5 and D6 for `sex` and the raw target.
- **Set apart:**
  - From the PROV-1 `No` cases (water_quality, 3d_estimation, calendardow): a named paper and the authors' page, not an anonymous re-upload.
  - From churn_telco_europa: there the population mismatch was measured; here it is an inference on units.
  - From haberman_survival: 10 baseline features, a stated horizon, and methods that spread.
- **Departs, without a distinguishing fact, from blood_tests_drink:** that dataset's label quantity is known; here it is not. That is why issue 1 goes to the curator, not to me.
- **Drift flag.** The popularity-based keeps (diabetes_3's workbook line, bank_customer_churn) run against the 2026-10-12 and 2026-10-15 rulings. This keep now does not rest on popularity.

</details>
