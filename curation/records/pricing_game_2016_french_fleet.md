---
unique_name: pricing_game_2016_french_fleet
name: 'Pricing Game 2016 of the Institut des Actuaires: French fleet vehicles, claim charge per vehicle-year, 2011-2013 (organisers'' train_contrats / train_sinistres; CASdatasets pg16 a copy)'
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 4
tags:
- Non-IID (Grouped)
- Two-Regime Zeros
year: '2016'
domain: insurance
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://github.com/dutangc/CASdatasets/blob/master/man/pricingame.Rd
- https://github.com/dutangc/CASdatasets/tree/master/data
- https://actinfo.hypotheses.org/69
- http://freakonometrics.free.fr/pricinggame/
- http://web.archive.org/web/20210422004748/https://freakonometrics.hypotheses.org/files/2016/08/pricing-game-2016-FR.pdf
v2_path: datasets/_dev/tabarena-v0pt2/pricing_game_2016_french_fleet/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**AI-FILLED, UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from the source pages, papers and data previews named below (measured where the notes say so). A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-20):** `TBD -> Yes`, priority 3: a commercial fleet portfolio (material damage only) from the
second actuaries' pricing game; the two tables join cleanly and pass the generated-data checks that sank pg15, but the
covariates add little beyond exposure.
- Source: the second pricing game of Arthur Charpentier, Romuald Elie and Jérémie Jakubowicz, data given to players on
  15 July 2016, results at the French Institute of Actuaries' "100% Data Science" day of 8 November 2016
  (actinfo.hypotheses.org/69: train_contrats 87,228 x 22, train_sinistres 4,568 x 9, test_contrats 32,772); kept in
  CASdatasets as `pg16trainpol`, `pg16trainclaim`, `pg16test` ("Datasets from unknown private insurers"; "Policies are
  guaranteed for all kinds of material damages, but not bodily injuries"). The documentation says "private motor
  insurance", but the columns describe fleets (`FleetMgt`, `FleetSizeCateg`, `CompanyCreation`, a policy holding up to
  30 vehicles). Rows are vehicle-periods: 68,485 vehicles (`LicNb`) in 18,037 policies, 2011-2013, cut at year end,
  `Exposure` = days / 365; `pg16test` holds 2014 without claims.
- Target and zeros (measured 2026-10-20 on the copies downloaded earlier): every claim joins one policy row on policy,
  vehicle, year and period dates, and `ClaimNb` equals the joined count on all rows. The claim charge per
  vehicle-period is 0 in 95.1% of rows (an observed claim-free period; 88.5% per policy-year), net negative in 537
  (recourse under the IDA convention, down to -1,255 per claim) and positive in 3,711. Single charges stop at 8,565
  with no pile at the top: a thin tail for material damage, unexplained. Two regimes: a claim or not, then the charge.
- Generated-data checks (PROV-3, tests 4 and 6), each one that could have failed: policy-level fields are constant
  within a policy-year (`CompanyCreation`, `ChannelDist`, `PayFreq` 100%; `Area`, `FleetMgt`, `FleetSizeCateg`,
  `BusinessType` 99% or more); a vehicle never goes back from ">5 years" to "0-5 years" (0 of 1,326 changes), keeps
  its power (99.9%) and its policy; policy age never falls from one year to the next; S2 fleets hold more vehicles
  than S1 (mean 3.3 against 1.9); features are dependent (Cramér's V up to 0.70, median 0.09). This refutes the
  row-wise resampling that sank pg15 (proof for that mechanism). That the values are untouched is not shown: levels
  are anonymised and the tail of the charges is unexplained (circumstantial either way, EV-6).
- Use case: the game's own: an insurer prices next year's fleet contracts (a premium for each of the 32,772 contracts
  of 2014); fit direct. Regime temporal (2011-2012 -> 2013, as the 2014 claims were never published), with vehicles
  and policies repeating (SPLIT-13).
- Siblings and duplicates: `pricing_game_2015_french_mtpl` (No, AHDS, AI draft) and `pricing_game_2017_french_mtpl`
  (TBD -> Yes) are other portfolios (schema, years and cover differ). No copy outside CASdatasets found.
- Risks for /add-dataset: the negative totals need a rule (policy question 3 of the zero-inflated review); every
  feature but exposure is an anonymised bin. Untuned LightGBM, 2011-12 -> 2013: AUC 0.69 for a claim against 0.67 for
  exposure alone, R^2 -0.15 on log cost among claimants, so the covariates carry little (TP-2).
- Priority: gap 0, use case + (the game's pricing task), source + (organisers' page and documentation), shape +
  (87,228 rows, 14 features, three years), risk - (negative amounts, an unexplained short tail).

**Assessment (AI, 2026-10-30):** suggested call for policy question 3 of the zero-inflated review, where Andrej asked
for a call per dataset from its references and the domain's practice instead of one convention for the family (the
shared reasoning: a time exposure or a sum insured is a feature, and a rating-cell table weights the metric by its
exposure; negative amounts that are recoveries become 0; the source's metric first, else the normalized Gini as a
context metric, since RMSE on raw amounts follows a few large claims and a Tweedie or Poisson deviance needs positive
predictions; MET-10 as amended on 2026-11-02 (Andrej) later declined a family-wide metric, so each table's metric is
decided on its own); the curator
has the call.
- Target: the claim charge per vehicle-period (rows as published), with the 537 net negative charges (IDA recourse) set
  to 0: the convention recovers a flat amount between insurers, not this vehicle's loss, and AIcrowd zeroed such totals
  on the 2017 game's portfolio. Alternative: keep the net charge as the insurer's actual cost, then a target with
  negative values.
- `Exposure` (days / 365, rows cut at year end): a feature.
- Metric: as in `pricing_game_2015_french_mtpl`, the market cannot be computed; normalized Gini as the stand-in
  (MET-11).
- Split 2011-12 -> 2013 with vehicles and policies recurring (SPLIT-13).

**Assessment (AI, 2026-10-30):** to the curator's question ("Might make more sense to add this as a classification task,
what do you think?"): agreed. The claim charges carry no signal (R^2 -0.15 on log cost among claimants), have an
unexplained short tail and include 537 net negative charges from IDA recourse; a claim in the vehicle-period is the
observed outcome without any of that, and claim frequency is half of every pricing model. Suggested: binary target
`ClaimNb` > 0 per vehicle-period, `Exposure` a feature, `roc_auc` (the fallback, MET-8), split 2011-12 -> 2013. The
concern that stays is the weak covariates (TP-4): AUC 0.69 against 0.67 for exposure alone.

CC (2026-10-30, Andrej): `TBD -> Yes`, priority 3 (the AI screening had `TBD -> Yes`, priority 3; zero-inflated
screening review page, after the AI's answer to the curator's question). "Do an additional test if this data is
generated, if yes its a no otherwise a yes"

**Assessment (AI, 2026-11-01):** the additional generated-data test the curator asked for, pg16 as the dataset under
test, calibrated against pg17, freMTPL2 and the Australian `dataCar`. Real, by tests that could have failed (proof
against generation, EV-6); the values are anonymised (binned categories, amounts scaled by one constant, 1.077841),
which is disclosure control. Test 1: the tables match the organisers' sizes and every claim joins one policy row. Test
4: divided by the constant, 6.1% of charges are whole euros (0.1% for smooth amounts), with piles at 130, 150, 1,000 and
2,200 EUR; `Exposure` heaps at 1, 0.5 and 0.25 years with `PayFreq`. Test 6: policy periods start on business days and
often on the 1st of a month; policy age never falls and steps up at the anniversary (1,946 of 1,946); vehicle age moves
only from 0-5 to >5 years; policy fields are constant within a policy-year; net negative IDA charges never occur at 100%
responsibility; settlement years end in 2014, as an extract of 2014 would; 72% of covariate pairs are dependent (median
Cramer's V 0.066; calibration 76-98%, 0.05-0.08), none independent of all others. Test 2: no row-counter effect at one
row per policy or vehicle; test 5: nothing label-linked; signal 6.3% of log loss explained (calibration 2.6-6.7%);
`check_frame` no flags.

CC (2026-11-01, Andrej): `Yes`, priority 3, by the curator's rule on the page ("Do an additional test if this data is
generated, if yes its a no otherwise a yes"): not generated (Assessment above).

**Assessment (AI, 2026-11-01):** added as `datasets/_dev/tabarena-v0pt2/pricing_game_2016_french_fleet/` by /add-dataset with the full review panel; the open questions are in its `REVIEW.md`. Recommend shipping; only a forced split (its issue 2, (b) or (c)) can turn it to `No`. Built from the organisers' own files, not CASdatasets' copy (whose `DirectComp` is 0 for 1,064 of the 1,190 IDA claims): 87,228 periods of cover, target a claim in the period (4.9%), trained on 2011-2012 and tested on three four-month windows of 2013, scored by ROC AUC as a stand-in for the game's market. Changes after the panel: `exposure` is the length of cover to 31 December for every period, not the realised length (LEAK-10, its issue 1). The `Two-Regime Zeros` tag goes (a binary target); `name` and the links now point to the organisers' files and rules. `problem_type` waits for your mark (Binary Classification). Priority 4: gap + (insurance thin), use case + (the insurer's tariff, fit direct), source + (the organisers' files and rules), shape + (87,228 periods), risk - (weak anonymised covariates, ROC AUC 0.60-0.65, a GLM ties LightGBM).

CC (2026-11-02, Andrej): the `exposure` fix confirmed (issue 1 (a)): every period gets its length from the start to 31 December; recorded as the LEAK-10 case for time on risk cut short by the outcome (leak_checks.md, Mechanisms table): the cut is removed or fixed where the data locates it, kept with its measured size where it cannot.

CC (2026-11-02, Andrej): split (issue 2, after discussion on the review page): "I don't want to have the same training
data and different test sets. We assume that whenever we have different test sets, we would be retraining." Three
four-month windows of 2013, each trained on every period closed before the window starts (an expanding train side,
SPLIT-11), test only the four months to the next refit. Amendment to SPLIT-14: windows that share one train side count
as one window (splits.md).

**Exception to SPLIT-10 (2026-11-02, Andrej):** no gap for late-reported claims (issue 3 (a)). The files give no report
dates, and rows are cut at 31 December, so even a 1-day gap before the January window leaves 50.2% of the rows in
training and a month 48.7%. Serves SPLIT-14: three windows on distinct training sides above the floor.

**Assessment (AI, 2026-11-02):** the expanding windows measured: training sides 67,886 / 61,797 / 56,178 periods (78%,
71%, 64%); the added 2013 periods are the ones cut short (3.2% and 2.4% with a claim). ROC AUC per window, newest
first: length alone 0.550 / 0.568 / 0.529, logistic regression 0.602 / 0.621 / 0.649, regularised LightGBM 0.597 /
0.622 / 0.652 (at most 0.002 from the fixed 2011-2012 side; untuned LightGBM loses 0.014 on the newest window). Task
probes: no flag, best family linear 0.624. Leak probes: all features 0.602, no single feature above 0.570. Simulated
reporting delays of 30 and 90 days: mean 0.604 to 0.603 and 0.595 (untuned). The `problem_type` field waits for the
amount-against-claim check (target question of 2026-11-02).

CC (2026-11-02, Andrej): target switched from the claim indicator to the claim charge per period ("I follow your
suggestion", after the measurement below): the charge is what the insurer prices and what the game asked for (a pure
premium), and the family's amount targets keep it. Net negative totals (IDA recoveries) set to 0, as in pg17 and
frempl; raw charge, scored by the normalized Gini as a stand-in for the game's market, as in pg17. `problem_type` stays
`Regression` (the earlier "update" mark on that field is superseded); `Two-Regime Zeros` back.

**Assessment (AI, 2026-11-02):** the charge target measured (record `_runs/2026-11-02_pg16_amount_check` and
`_runs/2026-11-02_pg16_expanding`). On the expanding windows (newest first), normalized Gini: the length alone 0.101 /
0.150 / 0.066, a Tweedie GLM 0.167 / 0.270 / 0.268, a regularised Tweedie LightGBM 0.155 / 0.245 / 0.276 (bootstrap SE
0.071 / 0.043 / 0.023). TP-4 holds, on the newest window (103 positive charges) only by about one SE. All the signal is
frequency: a Poisson model of the claim count ranks the charges at 0.202 / 0.271 / 0.279, and the log charge among
claimants has R^2 -0.06 to -0.02. 95.7% of the targets are 0; the clip of 537 net negative totals raises the total cost
by 4.3%.

CC (2026-11-02, Andrej): ship. The claim charge as target confirmed as implemented (issue 4 (a)); the metric checked
and kept as declared (`normalized_gini`, a stand-in for the game's market, as pricing_game_2017_french_mtpl). The metric
is this dataset's own call, not a family one ("It is case by case and when in doubt we go for diversity", MET-10).

CC (2026-11-06, Lennart): the target is the claim charge per vehicle-year over the realized period, `exposure` (the source's Exposition_au_risque, restored) its denominator, the weight scoring column and the `sample_weight`, never a feature (MET-14, MET-15, LEAK-41; issue 5, D11 of the exposure review); the length to 31 December stays a feature as `exposure_to_year_end` (LEAK-7, LEAK-37); the metric is the normalized weighted Gini of the rate, still a stand-in for the game's market; the scale stays the identity (CLEAN-16 as amended). Supersedes Andrej's call of 2026-11-02 on the target (the claim charge per period, issue 4): the exposure study measured later that the total over the realized period rewards predicting how long a vehicle stays (about 0.03 of the row Gini) and that the rate model ranks the rate better under the weighted Gini (0.153 against 0.138 for the model of the total; 0.154 against 0.136 on the shipped windows).

CC (2026-11-06, Lennart): every window trains on the periods that started before 2013 (56,178 periods of 2011-2012, 24,674 vehicle-years), all closed by 31 December 2012, so no training row is admitted by its realized end (LEAK-41; issue 5, D11 of the exposure review). Supersedes Andrej's expanding training sides of 2026-11-02 (issue 2 (d)): the exposure study's red team measured later that the 2013 periods they admitted, those that ended early, claim more (0.127 and 0.131 claims per vehicle-year against 0.115 and 0.116 for the 2013 periods they left out; 10.8% and 4.0% of the training vehicle-years of the September and May windows), and LEAK-41 (2026-11-06) bars training on rows selected by their realized end.

**Assessment (AI, 2026-11-06):** the reason of the exception to SPLIT-10 of 2026-11-02 (Andrej, above) is stale. "Serves SPLIT-14: three windows on distinct training sides above the floor" no longer holds, since D11 (CC of 2026-11-06) trains the three windows on one side. The no-gap departure now rests on another ground and covers the January window only (the May and September windows start four and eight months after the training side ends): a gap inside 2012 would admit the 2012 periods by their realized end (LEAK-41), and a gap of a whole year leaves 2011 alone, 30.4% of the rows, below SPLIT-14's floor. The exception lapses if REVIEW.md issue 6 goes to C (the forced split grouped by contract); if the three windows or one window are kept by an amendment of SPLIT-14, it is to be restated on this ground (review panel of 2026-11-06).

**Assessment (AI, 2026-11-06):** review panel (full, re-review under LEAK-41, MET-14 to MET-16): ship after changes (D11's target, weight, features and training side hold; the changes needing no decision are made: the four bands of a quantity ordered, landing with the next rebuild, probe 22 cited with both arms, two effects marked within seed noise, the metric reason with the measured closeness to the game's market, the source's floor of 30 days as a LEAK-41 note, the pro-rata premium sourced, a trend line, the stale reason of the exception to SPLIT-10 marked above; the leak test across the contract folds passes, the test year's training rows gaining -0.001 pooled with the year readable against wisconsin's +0.113, so the forced split grouped by contract needs no wait for wisconsin); disputed: whether keeping the three windows is an option on a par with the forced split (issue 6; the mediator: only by an amendment of SPLIT-14 for the family), whether the floor can be kept with a note (issue 7; the mediator: an amendment of LEAK-41's last clause), whether the metric is a weighing call or a stand-in whose closeness must be measured (issue 8; the mediator: MET-11, the pick is the curator's); for the curator: issues 6 (C recommended), 7 (the amendment recommended) and 8.

CC (2026-11-08, Lennart): the source's floor of 30 days stays, under LEAK-41's last clause as amended this day (REVIEW.md issue 7 (B), "Amend the rule"): a selection the source made before release, the same in train and test, that cannot be undone, defines the task's population and is sized in the notes. Here the organisers left out every period of cover shorter than 30 days, in the training file and in the game's 2014 file alike, about 1.5% of the vehicle-years; the task covers the periods of a month or more.

CC (2026-11-08, Lennart): `payment_frequency` is an ordered category, fewest payments a year first: annual < semi-annual < quarterly (REVIEW.md issue 8 (C) of spanish_motor_insurance_coverage_level_2022_2024, "Ordered in all three"), the same order as in that table and in pricing_game_2017_french_mtpl.

**Assessment (AI, 2026-11-08):** the check issue 7 asks for, on the lengths as released (each definition's raw loader, in days; the run folder of the exposure review, `pricing_game_2016_french_fleet/apply_2026-11-08/min_lengths.out`): no other insurance table of PR #47 has a minimum period length set by its source. frempl_french_motor_personal_line (`Exposure` from 0.365 days, about 300 to 400 rows a day below 30 days, 9.2% of the rows under 30; RecordEnd - RecordBeg from 1 day), spanish_motor_insurance_coverage_level_2022_2024 (from 1 day, about 500 a day; 49 rows at 0, dropped under USE-7), australian_vehicle_insurance_2004_2005 (from 1 day, about 210 a day), fremtpl2 (from 1 day, on a grid of 1/100 year above 3.65 days, 16.9% under 30 days) and bemtpl97 (from 1 day, about 60 a day) run down to a day without an edge. spanish_motor_insurance_2015_2018 has a planned term of 365 or 366 days on every row, and the lapses cut its kept first years from 1 day on (24 of 37,090 under 30 days). pricing_game_2017_french_mtpl has no length column (`pol_duration` counts years from 1). Only this table stops at an edge: no period of 29 days, 909 of 30. `dataset check`: 0 errors, 0 warnings.

CC (2026-11-08, Lennart): the periods are split by contract, forced from temporal (REVIEW.md issue 6, reply (b), "Forced by contract"): `contract_id` is the group column of the default 3 x 3 grouped splits, never a feature, tagged ForcedGroupedFromTemporal (SPLIT-8); `required_split` `Grouped (NON-IID)` and the tag `Non-IID (Grouped)` for `Non-IID (Temporal)`. Supersedes Andrej's expanding windows of 2026-11-02 (issue 2 (d), the CC of 2026-11-02 above, already replaced on 2026-11-06) and D11's three four-month windows of 2013 on one training side (the CC of 2026-11-06 above): windows that share a training side are one evaluation (SPLIT-14 as amended on 2026-11-02), and the expanding ones train on the 2013 periods chosen by their realized end (LEAK-41). The exception to SPLIT-10 goes with the windows.

**Assessment (AI, 2026-11-08):** the exception to SPLIT-10 of 2026-11-02 (Andrej, "Exception to SPLIT-10" above; its ground restated in the Assessment of 2026-11-06) is superseded: the split by contract mixes the years, every period carries its claims as of the one extract, and no window is left whose training side a gap would shorten. Measured on the shipped contract folds (3 x 3; regularised Tweedie LightGBM fitted with the weight, 3 seeds; run folder of the exposure review, `pricing_game_2016_french_fleet/apply_2026-11-08/issues6_8/`): on the folds' 2013 periods the forced model scores 84.32 on the declared metric against 84.27 for the valid window's model trained on all of 2011-2012 (+0.06, SD 0.52 over the folds) and 0.172 against 0.178 on the normalized weighted Gini (-0.005, SD 0.012), so the forced split is no more optimistic on 2013; a new fleet's cold start costs 1.10 on the declared metric (SD 0.86) and 0.015 of the Gini (SD 0.021; 0.004 on the review panel's folds). The leak test across the contract folds passes: the test year's own training periods gain -0.12 (SD 0.60) and -0.18 (SD 0.61) on the declared metric with the start as its day of the year and as a date, -0.007 and +0.008 on the Gini, against wisconsin's +0.113. Leak probes on the folds: all features at weighted R^2 -0.012, every feature alone at 0.002 or below; 4.3% of the test periods have a copy of their features and start in training, from another fleet (LEAK-18). Group probes: IID and grouped folds alike (weighted R^2 -0.008 in both). Probe 22 on the folds under the declared metric: no feature's gain goes through the weight above noise in either arm. `dataset check`: 0 errors, 0 warnings.

CC (2026-11-08, Lennart): the metric is `rescaled_mean_tweedie_deviance`, a new metric of the shared library (each scored set's predictions multiplied by sum(w y) / sum(w p), then the exposure-weighted Tweedie deviance; power 1.5, `min_prediction` 0.1 per vehicle-year, weighted by `exposure`), the stand-in for the game's market in place of the normalized weighted Gini (REVIEW.md issue 8 (B), "Agree. GO with the change in metric and use it going forward"). What sets this table apart from australian_vehicle_insurance_2004_2005 (D8) and spanish_motor_insurance_coverage_level_2022_2024, which keep the Gini as their stand-in: its original is a market that rescaled every tariff uniformly, and the closeness to it is measured (76 of 84 two-player markets against 44 for the Gini on the windows of 2013). Supersedes the metric of Andrej's call of 2026-11-02 (the normalized Gini kept as declared, issue 4) and of D11 (the normalized weighted Gini, the CC of 2026-11-06). "Use it going forward": the stand-in for a pricing game whose market rescales uniformly, for later datasets of that kind (MET-11).

**Assessment (AI, 2026-11-08):** the new metric measured. Floor: 0.1 per vehicle-year, two orders below the smallest plausible mean (MET-13), about 26 to 31 for the cheapest cells of two or three rating classes with at least 500 periods (25.7 for vehicles over 5 years in contracts aged 4 to 5 years in zone 2, 844 periods; 30.7 for fleet management N and power-value class 2, 689 periods; the portfolio 173), rounded down to a power of ten; no fitted model's prediction falls below it. On the 9 contract folds (predictions averaged over 3 seeds; bootstrap by contract, 1,000 resamples): a Tweedie GLM 81.24, a regularised Tweedie LightGBM 82.04, the weighted constant 82.63; the GLM beats the constant by 1.39 (standard error 0.46; on all 9 folds, beyond 2 standard errors on 8), the LightGBM by 0.59 (0.58; on 7 of 9, beyond 2 on 2), and the GLM beats the LightGBM by 0.80 (0.43; on all 9, beyond 2 on 4). The metric separates the GLM from the constant, the condition issue 8 set; it punishes relativities that run too steep: an untuned and a deeper LightGBM score worse than the constant on every fold (86.84, 86.51), and the task probe's untuned families lose to the weighted dummy (flag `no_signal`). The frequency model (a Poisson LightGBM times the mean charge per claim) scores 81.04. Closeness on the contract folds: 225 of 252 two-player markets against 128 for the Gini (63 ties). Library: tested against the formula written out on random inputs at powers 1, 1.5 and 1.8 (to 1e-9) and on hand cases, invariant to a common scale of the predictions, equal to the plain weighted Tweedie deviance of a balanced prediction; 1M rows in 0.03 s; the stability checks pass.

CC (2026-11-08, Lennart): the declared metric (`rescaled_mean_tweedie_deviance`, power 1.5, floor 0.1 per vehicle-year, weighted by `exposure`) is checked: his choice in issue 8 ("GO with the change in metric and use it going forward").

**Assessment (AI, 2026-11-08):** probe 23's flag on the forced split followed up (its shared-unit test: a lookup of the exact profile of the 16 inputs, the start included, reaches 4.3% of the test periods and gains +0.117 on the declared metric, SE 0.021, 9 of 9 splits; run folder of the exposure review, `pricing_game_2016_french_fleet/apply_2026-11-08/probe23_units/`). Neither one client under several contract numbers (LEAK-17) nor an outcome shared by date: the matches are common rating cells (LEAK-18). 94.3% of the matched test periods start on 1 January (37.6% of all) and 98.4% on the 1st of a month; 86% of the shared profiles are held by two contracts, and 95% of the 2,704 contract pairs share one year only. 29 of those pairs (1.1%) are numbered within 2, against 0.4% of pairs sharing only the fleet's classes and start and 0.07% of random pairs of one cohort, and a lookup restricted to contracts numbered within 20 gains nothing; no claim record is shared (no identical charge among the 24 matched pairs with a claim on both sides); a claim on one side goes with one on the other 1.45 times as often (phi 0.031) against 1.20 (0.014) for the same cell in another year, within noise; lookups over starts within 7 or 31 days (not the same day) or the same date in another year gain nothing. The gain comes from the probe's row folds: 19.2% of the training periods get a lookup, 78% of its weight from their own contract, and the gain sits on the test periods without a lookup (+0.129; those with one -0.012). With the training lookup out of fold by contract, as the test side sees it, the exact profile gains -0.047 (SE 0.042), without the start -0.016 (0.041), and no variant gains above noise (EV-6: a test that could have kept the gain). The one exact link between contracts: registration 32348 has one period under each of contracts 6168, 6169 and 6170 (no claim; the notes say a vehicle with two contracts). Open as REVIEW.md issue 9 (A: the split as shipped with a note; B, recommended: also join the contracts that share a registration).

CC (2026-11-08, Lennart): the contracts that share a registration are one group (REVIEW.md issue 9 (B), "Also join the contracts that share a registration"): the group column is `fleet_group`, the contract with the contracts that share a vehicle's registration joined under the smallest number, an exact key of the source's two ids (LEAK-17, SPLIT-24). Registration 32348 is the only one under more than one contract (6168, 6169 and 6170, one period each, no claim), so 18,035 groups of 18,037 contracts. It widens the group of his call on issue 6 of the same day (`contract_id`; the split by contract, forced from temporal, stays). The shared rating profiles that probe 23 flagged across the folds are common cells (LEAK-18), and the flag was an artefact of the probe's old row folds.

**Assessment (AI, 2026-11-08):** issue 9 (B) applied and measured (run folder of the exposure review, `pricing_game_2016_french_fleet/apply_2026-11-08b/`). Every registration of train_contrats.csv checked: 32348 is the only one under more than one contract (its one period under each of 6168, 2013, zone 2; 6169, 2011, zone 1; 6170, 2013, zone 4); the connected components of the contract and registration pairs give 18,035 groups (7,277 present in one year, 6,065 in two, 4,693 in three; 79.5% of the 2013 periods in a group insured earlier, as by contract). The folds reshuffled: test folds of 6,011 or 6,012 groups, 28,625 to 29,517 periods, 1,216 to 1,271 with a positive charge, no group on both sides. On them (9 folds, predictions averaged over 3 seeds, bootstrap of the test groups): a Tweedie GLM 81.58, a regularised Tweedie LightGBM 81.99, the weighted constant 82.64; the GLM beats the constant by 1.06 (standard error 0.65; on all 9 folds, beyond 2 standard errors on 5; on the folds before the join 1.39, 0.46, beyond 2 on 8), the LightGBM beats it by 0.65 (0.56; 7 of 9), the GLM the LightGBM by 0.41 (0.59; 7 of 9); an untuned and a deeper LightGBM score worse than the constant on every fold (86.21, 86.59); the frequency model 81.06, better than the LightGBM by 0.92 (0.34, every fold); a fit without the weight 0.68 worse (9 of 9). Closeness to the market: 217 of 252 two-player markets against 136 for the Gini (63 ties; among the fitted tariffs 50 of 54 against 43). On the folds' 2013 periods the forced model scores 84.27 against the valid window's 84.11 (+0.16, SD 0.45) and 0.172 against 0.184 on the Gini; the cold start loses 1.13 (SD 0.73). The leak test across the folds: the year's own training periods gain -0.33 (SD 0.33) and -0.43 (SD 0.52) pooled. Probes: the task probe flags `no_signal` (dummy 82.68; linear 83.97, random forest 99.69, LightGBM 112.95, best single feature 83.91); the leak probes find nothing (all features at weighted R^2 -0.015); probe 22's Tweedie arm: the weight as a feature +0.31 (SD 0.94), no feature's gain through the weight above noise, its L2 arm -14.9 (SD 16); the group probes IID -0.010, grouped -0.008; probe 23 (`--forced-split`, its lookup folds drawn by group): the year's own training periods gain -0.38 pooled (SE 0.25), the exact profile's lookup -0.23 on the 4.3% of the test periods with one (SE 0.17, 3 of 9 splits), without the start -0.66 on 8.6% (SE 0.14); no flag. The notes' "no fitted model's prediction falls below" the floor was slightly off: the untuned LightGBM puts 6 of 261,684 predictions at it (2 on the folds before); the notes say so now. `dataset check`: 0 errors, 0 warnings.

## Reference

CASdatasets (Dutang C., Charpentier A.), `pg16trainpol`, `pg16trainclaim`, `pg16test`, second pricing game (Charpentier A., Elie R., Jakubowicz J.), French Institute of Actuaries, 8 November 2016. https://github.com/dutangc/CASdatasets/blob/master/man/pricingame.Rd; https://actinfo.hypotheses.org/69

Lead: zero-inflated screening review, policy question 6 (curator's go, Andrej, 2026-10-20); sibling of `pricing_game_2015_french_mtpl`.
