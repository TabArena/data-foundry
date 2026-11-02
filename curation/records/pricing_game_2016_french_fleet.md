---
unique_name: pricing_game_2016_french_fleet
name: 'Pricing Game 2016 of the Institut des Actuaires: French fleet vehicles, claim charge per period of cover, 2011-2013 (organisers'' train_contrats / train_sinistres; CASdatasets pg16 a copy)'
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 4
tags:
- Non-IID (Temporal)
- Two-Regime Zeros
year: '2016'
domain: insurance
required_split:
- Temporal (NON-IID)
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
shared reasoning is in `curation/inputs/two_regime_zero_triage_summary.md`, "Policy calls of 2026-10-30"); the curator
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

## Reference

CASdatasets (Dutang C., Charpentier A.), `pg16trainpol`, `pg16trainclaim`, `pg16test`, second pricing game (Charpentier A., Elie R., Jakubowicz J.), French Institute of Actuaries, 8 November 2016. https://github.com/dutangc/CASdatasets/blob/master/man/pricingame.Rd; https://actinfo.hypotheses.org/69

Lead: zero-inflated screening review, policy question 6 (curator's go, Andrej, 2026-10-20); sibling of `pricing_game_2015_french_mtpl`.
