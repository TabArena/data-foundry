# pricing_game_2016_french_fleet

**Outcome:** added. The AI recommends shipping it. Shipped on Andrej's verdict of 2026-11-02, changed on 2026-11-06
by D11 of the exposure review (issue 5): the target is the claim charge per realized vehicle-year, each period weighted
by its vehicle-years; and changed on 2026-11-08 by Lennart's calls: the periods split by contract, forced from temporal
(issue 6), the three contracts that share a registration joined in one group (issue 9), and scored by the uniformly
rescaled weighted Tweedie deviance (issue 8). The full re-review of 2026-11-06
under the exposure rules (LEAK-41, MET-14 to MET-16) finds D11's target, weight and features sound. The organisers' own
files of the 2016 actuarial pricing game: 87,228 periods of cover of fleet vehicles of a French insurer, 2011-2013; the
target is the period's claim charges summed, net IDA recoveries set to 0, per realized vehicle-year (0 for 95.7% of the
periods), each period weighted by its vehicle-years in training and scoring; the features are the rating classes and
the length of cover to the year's end, known at the period's start; grouped 3 x 3 folds by contract over 2011-2013
(the three contracts that share a vehicle as one group), forced from temporal; scored by the uniformly rescaled, exposure-weighted Tweedie deviance (power 1.5) as a stand-in for
the game's market. Like every container with a `sample_weight`, it enters no run before the collection's
training-weight gate (`BENCHMARK_CHANGES_TODO.md`, "Training weights", "The gate").
Validity: SEL-1, SEL-2, USE-1 (fit approximate since 2026-11-08: held-out fleets of the same years stand in for next
year's book), USE-5, LEAK-7, LEAK-37, MET-15, SPLIT-1, SPLIT-9, SPLIT-13 hold; LEAK-10 fixed by LEAK-7 (2026-11-02);
LEAK-41 holds for the features and the weight (probe 22 on the shipped folds under the declared metric: in either arm
no feature's gain goes through the weight above noise, and the weight as a feature gains 0.31, SD 0.94, in the Tweedie
arm); LEAK-41's last clause, as amended on 2026-11-08 (issue 7), takes the source's floor as the task's population: the
organisers left out every period shorter than 30 days, about 1.5% of the vehicle-years; SPLIT-8 holds (forced from
temporal by contract on 2026-11-08, issue 6: the leak test across the folds passes, and on the 2013 periods the forced
split scores no better than the valid window); the exception to SPLIT-10 lapsed with the windows. Probe 23's
shared-unit flag of 2026-11-08 (a lookup of the exact profile across the contract folds, +0.117) read as LEAK-18's
natural repeats and an artefact of the probe's row folds, not a leak (issue 9: with the lookup out of fold by contract,
-0.047; the probe, its folds drawn by group since, finds -0.23 on the shipped folds); LEAK-17 and SPLIT-24 hold: the
three contracts that share a registration are one group since 2026-11-08 (issue 9).
Value: TP-4 holds on the declared metric for a fit that keeps its relativities in check (on the shipped folds a Tweedie
GLM beats the weighted constant by 1.06, bootstrap standard error 0.65, on all 9 folds; a regularised Tweedie LightGBM
by 0.65, 0.56), while untuned models score worse than the constant (an untuned LightGBM 86.21 against 82.64; the task
probe's families, flag `no_signal`), as the market punished relativities that run too steep (EV-3); TP-9 holds (1,216
to 1,271 positive charges per test fold); MET-11: the stand-in since 2026-11-08 follows the game's market more closely
than the Gini it replaces (76 of 84 two-player markets against 44 on the windows of 2013, 217 of 252 against 136 on
the shipped folds).
Quality: CLEAN-14, the four bands of a quantity (the contract's and the vehicle's age, the deductible, the insured
value) are ordered categories now (they land with the next rebuild), and so is `payment_frequency` (annual <
semi-annual < quarterly, 2026-11-08, as in the two other pricing tables); LEAK-18 repeated rows natural; the text corrected
where the panel found it overstated.
Weighed: the original files +, a real fleet-pricing task +, the family's only commercial-fleet damage table +; weak,
anonymised covariates -, held-out fleets of the same years standing in for next year's book -.
Left for Andrej and Lennart: nothing. The split (issue 6), the organisers' floor of 30 days (issue 7), the stand-in
metric (issue 8) and the group of the three contracts that share a registration (issue 9) were settled on 2026-11-08;
the build is stale until a rebuild (the split and its group column, the metric, the ordered bands).

Changes made after the review panel (AI, 2026-11-01 and 2026-11-02): `exposure` is the length of cover to 31 December
for every period; the metric is a stand-in for the game's market; the statements the claim audit refuted are corrected;
the windows train on an expanding side; the target is the claim charge, not the claim indicator; every window figure is
re-measured. On 2026-11-06 (issue 5): the target is the charge per realized vehicle-year, the source's realized length
is back as `exposure`, the weight of the metric and of training, the length to 31 December is the feature
`exposure_to_year_end`, the metric is the normalized weighted Gini, and every window trains on 2011-2012.

Changes made after the re-review (AI, 2026-11-06), no decision needed: the four bands are ordered categories (the build
stays stale until you ask for a rebuild); the notes cite both fits of the weight-proxy probe and mark two effects as
within seed noise (fitting without the weight, the time features); "a cut nobody scheduled" reads "a cut not known at
the start, a quarter of them on a month's end"; the metric reason says that the market rewarded the relative prices, of
which the Gini scores the order, drops the argument that the deviance scores the level and gives the measured closeness;
the floor of 30 days is a note under the rule on rows selected by their realized length, with its evidence and size; the
pro-rata premium cites the sources checked; a line gives the trend of the charge per vehicle-year. The record marks the
stale reason of the exception to SPLIT-10. Rows, split and metric are unchanged. The panel's reports describe the
definition of D11, before these changes; the panel of 2026-11-01 is in this file's git history.

Changes made on 2026-11-08 (AI, Lennart's calls on issues 6 and 8): `contract_id` is the group column of the default
3 x 3 grouped splits, tagged ForcedGroupedFromTemporal, in place of the three windows; the metric is
`rescaled_mean_tweedie_deviance` (power 1.5, floor 0.1 per vehicle-year), a new metric of the shared library; the
summary's split and fit (approximate), the notes on late claims, the splits comment, Decision 2 and the notes'
measurements are rewritten on the contract folds; the record's split fields follow. The panel's reports describe the
definition before these changes.

Changes made on 2026-11-08 (AI, Lennart's call on issue 9): the group column is `fleet_group`, the contract with the
contracts that share a registration joined (6168, 6169 and 6170, the only shared registration), 18,035 groups, in
place of `contract_id`, which leaves the frame with the registration; the grouping definition, the summary's split and
changes, the splits comment, Decision 2 and the notes' "Dropped:" bullet follow; the bullet on repeated rows says why
probe 23's flag was no leak; every fold number of the notes, the metric reason and the splits comment is measured again
on the reshuffled folds (the CC lines keep the numbers of their day).

**Main points:** No issue is open. Issues 1 to 5 are resolved, 2 and 4 superseded by 5; issues 6 to 9 on 2026-11-08
(the split by contract, forced from temporal; the rule amended for a selection the source made before release; the
uniformly rescaled weighted Tweedie deviance as the stand-in; the three contracts that share a registration joined in
one group, the shared rating profiles across the folds natural repeats). To note before the rebuild: under the new
metric untuned models and the task probe's families score worse than the weighted constant, and only fits that keep
the relativities in check (a Tweedie GLM, a regularised LightGBM, a frequency model) beat it; on the reshuffled folds
the GLM's margin over the constant is 1.06 (standard error 0.65) where the folds before gave 1.39 (0.46), so the draw
of the folds moves it by about a standard error.

**Issues for Andrej and Lennart:**

1. **Give each period that ends early the length known at its start (implemented), as in frempl?** `exposure` is a
   period's length in vehicle-years. 57.4% of the periods (58.2% in 2013) end before 31 December at a cut nobody
   scheduled; only 0.8% end at a contract anniversary. Their length is known only once they end. With
   `period_start` a feature, the realised length also gave back the end date the definition dropped.
   * What it did to the task: a model saw time on risk that the insurer cannot know when it prices. The realised length
     adds ROC AUC +0.040 / +0.055 / +0.052 over the length known at the start, which is a quarter to a third of the
     skill above chance. The early ends also go with claims: the rate ratio is 1.22 [1.12, 1.33] once the rating
     classes are accounted for, and vehicles that leave for good have 0.137 claims per vehicle-year against 0.111.
   * The definition's evidence for the keep was a 31-December flag. That flag is fixed by the start and the length on
     99.5% of rows, so the test could not fail.
   * Implemented: (a) every early end gets the length to 31 December (/366 in 2012). Periods that end at a contract
     anniversary keep theirs. Cost: LightGBM falls from 0.672 to 0.623 (window mean), and the covariates still beat the
     length alone on every window.
   * What the fix leaves: the target still counts claims over the cover actually earned. A model can therefore gain a
     little by guessing how long a vehicle stays, a fair expectation at pricing. The actuary's rate times the scheduled
     length scores 0.610 and the direct model 0.623, so the stay is about a tenth of the skill.
   * Alternative: (b) keep the realised length. Under LEAK-10 (Must) that is an amendment for time on risk in
     insurance tables, not a kept-leak note. It would reach frempl (issue 2),
     spanish_motor_insurance_coverage_level_2022_2024, australian_vehicle_insurance_2004_2005 (issue 2) and fremtpl2
     together.
     * For (b): fleet premiums are revised at the period's end for the vehicles that came in and went out, so actuaries
       condition on earned vehicle-years. The game's own 2014 file gives realised lengths, and a simulation shows the
       gain is the time at risk, not outcome information.
     * Against (b): LEAK-38 (Lennart, 2026-10-22, kick) rejects the host's test file as a reason. LEAK-10's clause of
       2026-10-26 blanks late values that can be located. The practice supports the time at risk in the scoring, not
       as an input.
   * The advocate argued (b), then conceded; the critic, the column audit and the precedent check argue (a). The
     domain practitioner accepted the keep as a named leak, before its gain was measured.
   * Precedent: the fix follows frempl's fix and spanish's. It departs from your fremtpl2 call (2026-10-20: "The
     contracted period is known at pricing (a mid-year cancellation also shortens it)"). Two facts set this case apart:
     the dates locate every early end here, and LEAK-10's clause of 2026-10-26 is newer than that call. The policy row
     of 2026-10-30 ("exposure: feature") still holds, because the length known at pricing stays a feature.

   Recommendation: (a), decided together with frempl's issue 2. Decision: (a) confirm, or (b) amend LEAK-10 for the
   insurance family?

   *Restored on 2026-11-03 from the panel's draft: the issue was removed when settled, before the rule that settled issues stay (2026-11-02).*

   **Resolved (2026-11-02, Andrej):** the `exposure` fix confirmed (issue 1 (a)): every period gets its length from
   the start to 31 December; recorded as the LEAK-10 case for time on risk cut short by the outcome (leak_checks.md,
   Mechanisms table): the cut is removed or fixed where the data locates it, kept with its measured size where it
   cannot.

2. **Count three windows of 2013 on one training side as SPLIT-14's windows?** SPLIT-14 (Must) asks a temporal task
   for at least 3 windows, each training on at least 50% of the rows. The three windows are September-December,
   May-August and January-April 2013, newest first. All three train on the same closed years 2011-2012 (64.4%). The
   letter is met, but the windows are three slices of one test year, not three refits walking back in time. No dataset
   has done this before.
   * What it does to the task: rows are cut at 31 December, so a period that starts in September lasts at most four
     months. Each window therefore holds one cohort of period lengths, and its score ranks within that cohort. After
     the `exposure` fix the window mean runs below the pooled 2013 score (untuned LightGBM 0.626 against 0.669), and
     the newest window holds 7% of the vehicle-years and 123 positives (standard error about 0.027), yet counts for a
     third. The game's 2014 file has the same three cohorts, so the windows mirror the year the game priced.
   * Implemented: (a) the three windows with the SPLIT-11 exception, and a first Cases row under SPLIT-14.
   * Alternatives: (b) SPLIT-8, `ForcedGroupedFromTemporal` by contract. After the fix it scores 0.666-0.667 against
     0.669 for the pooled test year, no more optimistic, but it mixes the training and test years. It also falls under
     your how_much_did_it_rain call ("if the data is temporal but a temporal split is not possible ... reject it");
     on 2026-11-02 you shipped forced grouped splits (SPLIT-8 amended), so (b) would ship. (c)
     Amend SPLIT-14 to require distinct training sides; this dataset then goes to (b).
     wisconsin_local_government_property_insurance_fund's issue 1 proposes a SPLIT-14 amendment the other way (two
     yearly windows ship); decide the two readings together.
   * For (a):
     * the start dates are daily, and SPLIT-8 applies only when "the release cannot give the windows SPLIT-14 asks
       for";
     * a tariff is fit once a year, and the game priced a whole year from the closed years (SPLIT-12, SPLIT-19). That
       fact supports the fixed training side, recorded as an exception to SPLIT-11 (Should, expanding windows);
     * a training side growing into 2013 would add only the short 2013 periods already closed, selected by their early
       end, and its scores are not decisive (after the fix 0.621 against 0.613 for May-August, 0.584 against 0.589 for
       September-December).
   * For (b): spanish coverage, pricing_game_2017_french_mtpl and frempl, each with one valid annual window, went to
     SPLIT-8. Three windows on one refit are one evaluation of one year.

   Recommendation: (a). Decision: (a), (b) or (c)?

   **Andrej (2026-11-02, discuss):** I don't want to have the same training data and different test sets. We assume
   that whenever we have different test sets, we would be retraining. Given one test period we test the same model.

   **Answer (AI, 2026-11-02):** Your note rules out (a). It is a general rule, so it reads as (c): an amendment to
   SPLIT-14 ("windows that share one training side count as one window"); with one valid window this dataset would go
   to (b), the forced grouped split by contract.

   **Andrej (2026-11-02, discuss):** Why don't you employ a rolling window approach, e.g. with three splits with a
   forecasting horizon of four months each and all training data from before, possibly with a planning gap

   **Answer (AI, 2026-11-02):** It works; the objection above was overstated. (d) Expanding windows (SPLIT-11): each
   four-month window trains on every period closed before it starts (78%, 71%, 64% of the rows). The closed 2013
   periods are the ones cut short, as a refit on that day would see them; scores barely move (0.621 against 0.613 for
   May-August, 0.584 against 0.589 for September-December). A planning gap fits only the two later windows: any gap
   before January drops the periods that run to 31 December 2012 (a day leaves 50.2% of the rows, a month 48.7%).
   Each window tests only the four months to the next refit, not all later data: the test sets stay disjoint and each
   period is scored by the model in use when it starts.

   **Andrej (2026-11-02, discuss):** Do (d)

   **Resolved (2026-11-02, Andrej):** (d), expanding four-month windows without a gap, with SPLIT-14 amended (windows
   that share one train side count as one window). Implemented and re-measured; record CC of 2026-11-02.
   *Superseded on 2026-11-06 by issue 5: every window trains on 2011-2012; issue 6 asks how the windows then count.*

3. **Train without a gap for late-reported claims (implemented), an exception to SPLIT-10?** A claim enters the data
   only once it is reported, and the files give no report dates. A 2013 tariff fit at the start of the year would have
   missed some claims of late 2012. SPLIT-10 (Should) asks for a gap of about that delay between the training and test
   sides; the split has none.
   * What it does to the task: the training labels of late-2012 periods are slightly more complete than a real
     insurer's, a possible slight optimism.
   * Evidence: rows are cut at 31 December, so even a 1-day gap removes the 12,417 periods that run to 31 December
     2012 and leaves 50.2% of the rows in training, at the floor; a 1-month gap, nearer a claim's reporting delay,
     leaves 48.7%, below SPLIT-14's floor. After the fix, simulated reporting delays of 30 and 90 days lower the window
     mean from 0.626 to 0.624 and 0.622, and a tariff fit on the periods closed by 1 October 2012 scores 0.620 against
     0.626 (simulations: there are no report dates). Claims per vehicle-year are flat across the years (LEAK-24
     holds).
   * Rule: the tension row "unmatured training labels against the training floor" departs from SPLIT-10 for SPLIT-14's
     floor and records an exception. After alfa_battle_2_0_task_2 and lending_club (Lennart, 2026-10-21),
     avito_demand_prediction_1m (its issue 2) and wisconsin (its issue 1 (a)) propose the same in this run, so the
     amendment principles.md asks for at the third was due. You declined the SPLIT-10 amendment on 2026-11-02
     (avito_demand_prediction_1m issue 4), so this is an exception of its own. spanish_motor_insurance_2015_2018 now has
     a gap and does not count toward it.
   * Implemented: (a) no gap, the bound stated in the notes, and an exception to SPLIT-10 that serves SPLIT-14.
   * Alternative: (b) set a gap: the training side falls below the floor, SPLIT-8 applies, and the dataset meets issue
     2's (b).

   Recommendation: (a), as an exception to SPLIT-10 that serves SPLIT-14.
   Decision: (a) or (b)?

   **Resolved (2026-11-02, Andrej):** (a), no gap, an exception to SPLIT-10 that serves SPLIT-14 (splits.md Cases);
   the simulated delay bound is in the notes.

4. **Confirm the claim charge per period as the target (implemented)?** The record chose the claim indicator on
   2026-10-30; on 2026-11-02 you followed the AI's suggestion to switch, after a measurement.
   * Implemented: `claim_charge`, the period's charges summed, the 537 net negative totals (IDA recoveries) set to 0,
     raw (not log1p), regression scored by the normalized Gini, as pricing_game_2017_french_mtpl and the family's
     amount targets.
   * Evidence, normalized Gini per window (newest first): the length alone 0.101 / 0.150 / 0.066, a Tweedie GLM 0.167 /
     0.270 / 0.268, a regularised Tweedie LightGBM 0.155 / 0.245 / 0.276 (bootstrap standard errors 0.071 / 0.043 /
     0.023). On the newest window (103 positive charges) the models beat the length by about one standard error.
   * All the signal is claim frequency: a Poisson model of the claim count ranks the charges at 0.202 / 0.271 / 0.279,
     and the log charge among claimants has R^2 -0.06 to -0.02. The charge is the frequency task with severity noise
     on top.
   * Alternative: (b) back to the claim indicator (ROC AUC 0.597 / 0.622 / 0.652 against 0.550 / 0.568 / 0.529 for the
     length), with the measured reason in the notes: the charge adds only noise.

   Recommendation: (a), as implemented. Decision: (a) or (b)?

   **Resolved (2026-11-02, Andrej):** (a), the claim charge as implemented; the metric kept as declared, decided for
   this dataset alone (MET-10 as amended: no family call on the metric, in doubt for diversity). Verdict: ship.
   *Superseded on 2026-11-06 by issue 5: the target is the charge per realized vehicle-year.*

5. **Score the charge per realized vehicle-year, with the vehicle-years as weight, and train on 2011-2012?**

   * **Problem:**
     - The target summed the claim charges over the realized period of cover, so a model gained by guessing how long
       a vehicle stays in the fleet, which the insurer does not know when it prices the period.
     - Each window trained on the periods closed before it starts, so from 2013 on it admitted only the 2013 periods
       that ended early, and those claim more than the 2013 periods it left out.
     - The exposure study of 2026-11-05 measured both after Andrej's calls of 2026-11-02 (issues 2 and 4), and the
       rules adopted on 2026-11-06 bar both[^rate][^select].
   * **Background:** `Exposition_au_risque` ("Véhicules année") is the period's realized vehicle-years: of the 87,228
     periods of 68,485 vehicles (2011-2013), 57.4% end before 31 December at a cut nobody scheduled. Issue 1 replaced it
     as a feature by the length to 31 December, known at the start, so the features were leak-free, but the target
     still summed over the realized period. Rows are cut at 31 December, and claims carry no dates.
   * **Effect on the task:**
     - With the total as the target, about 0.03 of the row Gini rewarded predicting the stay: the direct model of the
       total scored 0.210, its rate times the length to 31 December 0.182 (the study's rough attribution).
     - The 2013 periods the expanding windows admitted held 10.8% and 4.0% of the training vehicle-years of the
       September and May windows, at 0.127 and 0.131 claims per vehicle-year, against 0.115 and 0.116 for the 2013
       periods still running at the window's start and 0.118 for 2011-2012.
   * **Experiments:**
     - The study, unnormalised weighted Gini of the rate on the old windows (3 seeds): the rate model fitted with the
       weight 0.153, the model of the total 0.138, the rate model fitted without the weight 0.147.
     - The new definition's shipped windows, normalized weighted Gini (newest first; regularised Tweedie LightGBM fitted
       with the weight, 5 seeds): 0.114, 0.158 and 0.190 against 0 for the weighted constant; the model of the total
       ranks the rate at 0.136 on average against 0.154; fitting without the weight costs 0.010 (SD 0.009), within seed
       noise (0.005, lower on 2 of 3 seeds, in the re-review of 2026-11-06).
     - The realized vehicle-years as a feature would add 0.013 to the Tweedie fit (5 of 5 seeds), and 1/vehicle-years
       alone scores 0.029, the ceiling of a proxy; the length to 31 December and the start add 0.007 (SD 0.009), within
       seed noise (0.003 in the re-review), and stay, as they are known at the start.
     - The weight-proxy probe with both of its fits (added by the re-review of 2026-11-06; the probe's text had cited
       only its squared-error fit): the features predict the realized vehicle-years at R^2 0.38, mostly through the
       fleet management and the length to 31 December, both known at the start. The squared-error fit cannot see the
       weight itself (-0.001, SD 0.052); in the weighted Tweedie fit the weight as a feature gains +0.007 (SD 0.028),
       and no feature's gain goes through the weight by more than one SD.
   * **Consistency:** fremtpl2 and bemtpl97 ship their claims per year insured with the years as the weight of the
     metric and of training (Lennart, 2026-11-06); frempl_french_motor_personal_line fixes its located cuts to the
     length known at the start. This dataset now does both: the realized length is the weight, the length to 31
     December a feature.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Rate with its weight, training on 2011-2012 (implemented) | the charge per realized vehicle-year, `exposure` the weight of the metric and of training, the normalized weighted Gini; every window trains on 2011-2012 | no reward for guessing the stay; no training row admitted by its end; the rate a fleet tariff charges | the three windows share one training side (issue 6) |
     | B | As on 2026-11-02 | the charge per period and the row Gini; each window trains on the periods closed before it starts | Andrej's calls; three training sides | the stay rewarded; the 2013 training rows selected by their early end |
     | C | Rate with its weight, expanding windows | as A, with the training sides of B | three training sides | the selection stays |

   * **Recommendation:** A, the curator's decision D11 of the exposure review. **Decision:** A, B or C?

   [^rate]: **MET-14** (Should), **MET-15** (Must) and **LEAK-41** (Must), adopted on 2026-11-06: a count or amount
     over a realized time on risk ships as the rate per unit, with the time on risk as the metric's row weight and the
     training weight, never a feature; a part known at the start ships as its own column (**LEAK-7**, **LEAK-37**).
     **CLEAN-16** as amended: a rate scored by a Gini keeps the scale the curator chose.
   [^select]: **LEAK-41**: "No model is trained or scored on rows selected by the realized weight (such as full-year
     rows only)".

   **Resolved (2026-11-06, Lennart):** A (D11 of the exposure review, derived from the rules adopted the same day). The
   target is `claim_charge_per_vehicle_year`, the period's summed charge (net negative totals at 0) divided by
   `exposure`, the source's realized vehicle-years, restored; `exposure` is the weight scoring column, the `weight` input
   of `normalized_weighted_gini` and the task's `sample_weight`, never a feature (MET-14, MET-15, LEAK-41); the length to
   31 December stays a feature as `exposure_to_year_end` (LEAK-7, LEAK-37); the metric stays a stand-in for the game's
   market, its reason updated; the scale stays the identity (CLEAN-16 as amended). Every window trains on the 56,178
   periods of 2011-2012 (24,674 vehicle-years, 64.4% of the rows), all closed by 31 December 2012, where the windows
   trained on 67,886, 61,797 and 56,178 periods before (27,653, 25,694 and 24,674 vehicle-years); the test windows are
   unchanged (5,312, 6,509 and 19,229 periods; 987, 2,218 and 10,659 vehicle-years). On the shipped windows a
   regularised Tweedie LightGBM fitted with the weight scores 0.114, 0.158 and 0.190 (bootstrap standard errors 0.068,
   0.054 and 0.023; 0.137, 0.160 and 0.190 on the old training sides), the weighted constant 0. The exception to
   SPLIT-10 (no gap before the January window) stays on new grounds: a gap inside 2012 would admit the 2012 periods by
   their realized end, and a gap of a whole year leaves 2011 alone (30.4% of the rows). Supersedes Andrej's calls of
   2026-11-02 on the target (issue 4) and the expanding windows (issue 2 (d)); CC lines in the record. `dataset check`:
   0 errors, 0 warnings (the four acceptances kept, their texts updated; `task_feature_looks_like_exposure` is gone with
   the weight declared).

6. **Three windows on one training side: re-split grouped by contract, or amend the windows rule for the family?**

   * **Problem:**
     - Since D11 (issue 5) the three windows of 2013 train on the same 56,178 periods of 2011-2012, and the windows rule
       counts windows that share a training side as one evaluation, not three[^windows].
     - The rule's remedy for a release with one valid window is a forced split grouped by the entity (each contract's
       periods all on one side, the years mixed), after a leak test across the split, and that test now passes[^forced].
     - Keeping the three windows (A) or one window (B) is open only as an amendment of the windows rule for the whole
       family, and the expanding windows (D) stay out, as they train on 2013 periods selected by their early
       end[^early].
   * **Background:**
     - Rows are cut at 31 December and claims carry no dates, so between two year ends a training side can grow only by
       the periods that ended early: no training rule that admits no period by its realized end and keeps every label
       known at a window's start can give the windows their own training sides.
     - 2013 on 2011-2012 is the one valid window (64.4% of the rows in training); 2012 on 2011 would train on 30.4%,
       below the floor.
     - On issue 2 (2026-11-02) Andrej asked for a retrained model for every test period[^andrej], then took the
       expanding windows, which issue 5 ruled out.
     - The forced split (C) groups by `contract_id`, the source's contract key: 18,037 contracts, the largest with 81
       periods (0.05% of the vehicle-years), vehicles nested in contracts, 10,757 contracts present in two or three of
       the years; it stays the group column, never a feature.
   * **Effect on the task:**
     - As shipped, one model is scored on three cohorts of period lengths (a period's start caps its length) and the
       benchmark counts it three times: the newest window holds 7% of the test vehicle-years and 103 positive charges
       (bootstrap standard error 0.068), yet counts for a third, and the mean of the windows (0.154) runs below the same
       model pooled over 2013 (0.171).
     - Under C the model also meets fleets it has never seen, while the year's tariff prices known fleets (76-81% of the
       2013 test periods have their contract in training); the cost of that cold start, measured below, is small.
   * **Experiments:** a regularised Tweedie LightGBM fitted with the weight, scored by the normalized weighted Gini.
     - A, the three windows: 0.114, 0.158 and 0.190 (newest first, 5 seeds), mean 0.154; re-measured at 0.110, 0.157 and
       0.189 (3 seeds).
     - B, one window over 2013: 0.171 (seed SD 0.004).
     - C against the valid window, paired on the same 2013 rows of each fold (3 repeats x 3 folds by contract): the
       forced model 0.174 (SD 0.029), the valid window's model 0.169 (SD 0.044), a difference of +0.005 (SD 0.022 over 9
       folds), so the forced split is no more optimistic on 2013 beyond noise. The valid window's model without the test
       fleets' history, a new fleet's cold start, loses 0.004 (SD 0.013). On its whole test folds C scores 0.182, mostly
       because a fold ranks all start cohorts together. The earlier text of this issue compared 0.174 with 0.171, which
       were scored on different test rows.
     - The leak test across the contract folds, as on wisconsin: each test year scored by a model trained without that
       year's training rows, against one trained without as many random rows (9 folds). With the start as a date, which
       lets a model read the year, the same-year rows gain -0.001 pooled (SD 0.020, positive on 2 of 9 folds) and
       -0.0035 within a year; with the start as its day of the year, +0.008 pooled (SD 0.015) and +0.006 within a year,
       about 1.7 standard errors of structure within the year. Wisconsin's mark of a year-level leak, a pooled gain far
       above the within-year one (+0.113 against +0.008), is absent, as the flat claims per vehicle-year suggested
       (0.117, 0.119 and 0.119 in 2011 to 2013): no year-level leak crosses the contract folds.
     - D, the old expanding training sides: 0.137, 0.160 and 0.190.
   * **Consistency:**
     - spanish_motor_insurance_coverage_level_2022_2024 has the same facts: three stacked years, one valid window above
       the floor (52.5% of the rows in training; the earlier text of this issue had it below) and recurring entities; it
       shipped forced grouped by policy on Andrej's call of 2026-11-02[^spanish].
     - pricing_game_2017_french_mtpl and frempl_french_motor_personal_line (one year each), and nba_players_2016_2019
       and open_university_learning_analytics_dataset (too few periods), went grouped by their entity too.
     - The one fact left that sets this case apart is its daily dates, which allow sub-windows of 2013 on one training
       side, and that is the cut Andrej's amendment counts as one window; no shipped dataset has windows that share a
       training side.
     - wisconsin_local_government_property_insurance_fund (its issue 3, open) found a year-level leak across its forced
       folds; the leak test above sets this case apart, so C needs no wait for wisconsin, while an amendment (A or B)
       would be decided together with wisconsin's issue 3.
   * **Panel:**
     - The domain practitioner ranks the fidelity to the use case B > A > C: the tariff is fit once a year and judged on
       the whole 2013 book, while C tests fleets never insured, with the years mixed.
     - The advocate withdrew its preference for A in rebuttal: C costs that fidelity almost nothing (+0.005 paired,
       0.004 for the cold start), and no history feature ships.
     - The critic: an amendment that fits only this dataset works as an exception to a rule that admits none, and it
       would reverse Andrej's amendment of 2026-11-02, made on this dataset, and Lennart's reframing of 2026-11-05.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Three windows on 2011-2012 (implemented) | the three four-month windows of 2013 on one training side, with the windows rule amended for the whole family | what the curator set in D11 (issue 5); the temporal regime of the use case; the game's tariff, fit once for the year | one evaluation counted three times; an amendment that fits only this dataset; reverses Andrej's amendment of 2026-11-02 and Lennart's reframing of 2026-11-05 |
     | B | One window | 2013 on 2011-2012, 31,050 test periods, with the windows rule amended below three windows | one evaluation counted once; the game's design; the practitioner's first choice | an amendment for the whole family; reopens spanish coverage, nba, open_university and distribution_transformers_at_cauca_department |
     | C | Forced grouped by contract | 3 x 3 folds by `contract_id` over 2011-2013, tagged forced from temporal; the no-gap exception goes | the rule's own remedy; the same as spanish coverage, pricing_game_2017_french_mtpl, frempl, nba and open_university; the leak test passes; scores 2013 as the valid window does (+0.005 paired) | mixes the years; tests fleets the model never saw (the cold start costs 0.004); the summary, the notes and the record change, and a rebuild |
     | D | Expanding windows, as before | each window trains on the periods closed before it starts | three training sides | trains on the 2013 periods selected by their early end, which issue 5 ruled out and the rule on realized lengths bars |

   * **Recommendation:** C: the windows rule and its remedy decide this case as they decided spanish coverage, which has
     the same facts; the leak test across the contract folds passes, and on 2013 the forced split scores as the valid
     window does. A or B only as a deliberate amendment of the windows rule for the family, decided with wisconsin's
     issue 3. **Decision:** C, or an amendment (A or B)?

   **Notes for the AI:**
   - C: in `dataset.py`, take `contract_id` out of `drop_columns` and make it the group column (never a feature; rewrite
     the notes' "Dropped:" bullet), replace `temporal` and `_make_splits` with a `Grouping` on `contract_id` and the
     default 3 x 3 splits, add `ForcedGroupedFromTemporal` to `data_tags`; rewrite `task_summary.split`, `fit_reason`,
     the notes on the gap (the SPLIT-10 exception goes, and the record's exception line with it), `splits_comment` (what
     the dates would change, the cold-start cost of 0.004) and Decision 2 with its table; the record's `required_split`
     (`Grouped (NON-IID)`) and tag (`Non-IID (Grouped)` for `Non-IID (Temporal)`); a CC line naming the case;
     splits.md's SPLIT-14 Cases row for this dataset replaced (the main session's); after the rebuild, the leak probes
     on the grouped split (`probes/group.txt`). The leak test above is the mediator's (`leaktest.py`, re-review of
     2026-11-06).
   - A or B: draft the SPLIT-14 amendment for the family with this case, decide it with wisconsin's issue 3, replace
     splits.md's Cases row for this dataset, and restate the exception to SPLIT-10 on its new ground (LEAK-41 plus the
     floor, the January window only).
   - B: ask whether spanish_motor_insurance_coverage_level_2022_2024, which has the same facts and ships forced
     grouped by policy, moves to its one valid window too (the precedent checker's conditional prompt of that
     dataset's re-review of 2026-11-06).

   **Lennart (2026-11-08, discuss):** Re-open this investigation, would we maybe just need to remove the weight,
   which we would not know as in other cases and then we could use expanding windows? this is might be the result of
   an old decisions which our new rules would overule

   **Answer (AI, 2026-11-08):** Removing the weight does not open the four-month windows: ship the forced split by
   contract, or two yearly windows by amending the windows rule as wisconsin needs?

   * **Problem:**
     - You ask whether a target per period, with no realized length as its denominator or weight, would make the
       expanding four-month windows valid, and whether the shared training side comes from an older call that the
       newer rules overrule.
     - It would not: inside 2013 a window can add only the periods that had already ended, a choice of rows by their
       realized end that stays whatever the target, and a target per period brings back a score won by guessing how
       long a vehicle stays.
     - The only windows with training sides of their own and no such choice are whole years (2012 trained on 2011,
       2013 on 2011-2012), two windows with the older on 30.4% of the rows, so the choice is between the rules'
       forced split by contract and an amendment of the windows rule like the one wisconsin needs.
   * **Background:**
     - Where the shared side comes from: rows are cut at 31 December, and the claims carry no dates (the claim file
       holds the period's dates, the IDA flags, the year the claim closed, the charge, the contract and the
       registration), so a running period's claims to date cannot be counted at a window's start. The rule against
       training on rows chosen by their realized length[^a6a] and the windows rule's clause that windows sharing a
       training side are one evaluation[^a6b] then leave one training side. No newer rule overrules either clause,
       and the weight comes from the rate rules of 2026-11-06, newer than the windows clause.
     - The added rows' labels were known at the window's start, so the rule on labels not yet known does not bar
       them[^a6c]; what bars them is the choice of rows. Your amendment of 2026-11-08 covers a choice the source made
       before release on both sides alike, not one a split makes on its training side alone.
     - The weight is information the actor has: a past period's vehicle-years are known once it ends, and the rate
       rules use them only as the training weight and as the score's weight, which the score reads after the fact as
       it reads the label. Only the period being priced has an unknown length, and there it is no input[^a6d].
     - What a target per period would ask: the fleet tariff charges a rate per vehicle-year earned pro rata, and the
       game's players had each 2014 period's vehicle-years in their file, so neither priced the stay. The rules keep a
       target per contract only where the planned term is the same for every row and known; here the length to 31
       December varies and the realized one is cut short after claims (a rate ratio of 1.22 given the rating
       classes)[^a6e].
     - Under a target per period, an actor refitting in May could use only the ended 2013 periods too, since a running
       period has no final label; so the expanding windows would mirror a refit, but only for a target nobody prices.
     - Wisconsin: on 2026-11-06 you kept its three yearly windows with the oldest on 40.6% of the rows ("the task is
       too good to remove because of the 50% floor"), where its forced folds leaked the year's claim level; here the
       forced folds pass the same leak test (the experiments of issue 6 above).
   * **Experiments:** on the definition as committed (its four bands now ordered; the scores differ from issue 6's, run before).
     - The rows an expanding window adds, against the 31,050 periods of 2013:

       | Window starts | 2013 periods added | Their share of 2013 periods / vehicle-years | Claims per realized vehicle-year | Claims per period | Claims per vehicle-year to 31 Dec |
       |---|---|---|---|---|---|
       | 1 May | 5,619 | 18.1% / 7.4% | 0.131 (still running: 0.116) | 0.024 (0.082) | 0.025 (0.089) |
       | 1 September | 11,708 | 37.7% / 21.5% | 0.127 (still running: 0.115) | 0.032 (0.081) | 0.036 (0.105) |
       | all of 2013 | 31,050 | | 0.119 | 0.053 | 0.073 |

     - Under the rate target the added rows claim 7% to 10% more per vehicle-year than 2013 as a whole; under a target
       per period, set against the length to 31 December that such a model reads, they claim a third to a half as
       much. Removing the weight turns the bias around; it does not remove it.
     - Scores, regularised Tweedie LightGBM fitted with the weight, normalized weighted Gini, 5 seeds:

       | Design | Sep-Dec | May-Aug | Jan-Apr | 2012 | 2013 | Mean |
       |---|---|---|---|---|---|---|
       | a: three windows on 2011-2012 | 0.103 | 0.155 | 0.204 | | | 0.154 |
       | Andrej's expanding windows, with the weight | 0.118 | 0.160 | 0.204 | | | 0.160 |
       | b: forced by contract, 3 x 3 | | | | | 0.173 (its 2013 rows) | 0.185 (all rows) |
       | c: yearly windows | | | | 0.171 | 0.181 | 0.176 |
       | d: lagged training sides | 0.103 | 0.146 | 0.199 | | | 0.150 |

     - The expanding sides move the window mean by +0.006 (SD 0.015 over seeds, higher on 3 of 5), within noise: the
       rule bars them for the choice of rows, not for a measured gain.
     - With the weight removed (the charge per period, the length to 31 December a feature, no weight), the row Gini of
       the charge per period is 0.117, 0.233 and 0.285 on the shared training side and 0.123, 0.229 and 0.285 on the
       expanding sides, while the realized vehicle-years alone, the stay known only at the end, score 0.178, 0.332 and
       0.292, above the model on every window. Turned into a rate by the length, that model scores 0.137 on the
       declared metric against 0.154 for the rate model.
     - The yearly windows train on whole closed years, every period ended by 31 December, so no row is chosen by its
       end; they score 0.171 and 0.181 (mean 0.176, SD 0.004 over seeds). 67% of the 2012 test
       periods and 80% of the 2013 ones belong to a contract in training (1,464 and 1,543 periods with a claim).
     - The lagged training sides (each four-month window trained on the periods that started at least 8 months before
       it: 51.1%, 58.3% and 64.4% of the rows) are the only four-month windows with sides of their own, every label
       known and no row chosen by its end; their sides differ only because data known at each window's start is held
       back, since all of 2012 is known on 1 January 2013, and the rules ask each window to train on all that came
       before it[^a6b].
   * **Consistency:**
     - spanish_motor_insurance_coverage_level_2022_2024 has the same facts (stacked years, one valid yearly window,
       recurring entities) and ships forced by policy[^a6f].
     - wisconsin_local_government_property_insurance_fund keeps yearly windows below the floor; c would go further
       (two windows, the older on 30.4% against 40.6%), and the forced folds pass here the leak test they failed
       there, the fact that sets the two apart. california_house_prices_2020 dropped a window that trained on 25%.
   * **Prior calls:** your D11 (the rate, the weight, the length to 31 December) stands under a to d; e reverses its
     target and weight and restores Andrej's charge per period (issue 4) and expanding windows (issue 2 (d)). b ends
     the three windows and the exception for no gap; c keeps D11's training side for 2013, adds 2012 on 2011 and keeps
     the exception for both windows; a and d keep the January window's exception.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Three windows on 2011-2012 (implemented) | the three four-month windows of 2013 on one training side | D11 as shipped; the temporal regime | one evaluation counted three times; needs the clause on shared training sides amended |
     | b | Forced by contract | 3 x 3 folds by `contract_id` over 2011-2013, tagged forced from temporal; rate and weight unchanged | the windows rule's own remedy; the leak test passes; as spanish coverage | mixes the years; tests fleets never insured (cold start 0.004); a rebuild |
     | c | Two yearly windows | 2012 trained on 2011, 2013 trained on 2011-2012; rate and weight unchanged | each window its own training side; no row chosen by its end; the yearly tariff on known fleets; expanding, with the weight | two windows, the older on 30.4%; needs the windows rule amended further than wisconsin's departure |
     | d | Lagged training sides | each four-month window trained on the periods that started at least 8 months before it (51%, 58%, 64%) | meets the windows rule's text; no row chosen by its end | holds back data known at each window's start; models nobody would fit; departs from training on all earlier data |
     | e | Weight removed, expanding windows | the charge per period, no weight; each window trained on the periods closed before it | three training sides; what you asked | the choice of rows stays, its bias turned around; the stay outscores the model; departs from the rate rules; reverses D11 |

   * **Recommendation:** b: the windows rule sends a release with one valid window to the forced split, the leak test
     across it passes, it scores 2013 as the valid window does, and spanish coverage, with the same facts, ships it.
     c if you extend wisconsin's departure to this table, as one amendment of the windows rule written for both; it
     is the expanding design you asked for, valid with the weight kept. Not e: the weight is not what bars the
     windows. **Decision:** a, b, c, d or e?

   **Notes for the AI:**
   - b: as issue 6's notes for C: `contract_id` out of `drop_columns` and the group column (never a feature; the
     notes' "Dropped:" bullet), a `Grouping` on it with the default 3 x 3 splits in place of `temporal` and
     `_make_splits`, `ForcedGroupedFromTemporal` in `data_tags`; rewrite `task_summary.split`, `fit_reason`, the gap
     bullet (the SPLIT-10 exception and its record line go), `splits_comment` (what the dates would change, the cold
     start 0.004, the yearly windows' scores as the cost against the valid windows) and Decision 2 with its table; the
     record's `required_split` and tag; a CC line naming D11's three windows as replaced; the SPLIT-14 Cases row for
     this dataset replaced and a SPLIT-8 row (the main session's); after the rebuild, the leak probes on the grouped
     split.
   - c: the main session first drafts the SPLIT-14 amendment together with wisconsin's departure (a Must takes no
     exception, so wisconsin's call is an amendment too), worded to cover a release of yearly periods with whole
     closed years: for example, "a release whose periods close at a year end, with fewer years than three valid
     windows, ships its yearly expanding windows when each trains on whole closed years; the oldest may train on less
     than half the rows (wisconsin 40.6%, this dataset 30.4%)". Then in `dataset.py`: `WINDOWS` becomes the years
     (2013 on starts before 2013, then 2012 on starts before 2012, newest first), `_make_splits` builds the two
     splits, `temporal` gets a one-year horizon; rewrite `task_summary.split`, `fit_reason`, `splits_comment` (the
     scores, the known contracts 67% and 80%, the cohorts now pooled per year), the gap bullet (the exception now for
     both windows, on the ground of the rule on realized lengths plus the floor) and Decision 2 with its table; a CC
     line; the Cases rows of SPLIT-14 and SPLIT-10 (kind `exception`) replaced.
   - d: `_make_splits` with each window's training side `start < window start - 8 months`; the record and the notes
     carry an exception to SPLIT-11 (the fact: rows cut at 31 December, claims undated; serves SPLIT-14) and a Cases
     row of kind `exception`; `splits_comment` says that the sides differ only by data held back.
   - e (not recommended): `TARGET` the charge per period, no `sample_weight`, the metric back to the row Gini, the
     expanding sides of 2026-11-02; an exception to MET-14 with a fact, which the measurements do not give; a CC line
     reversing D11.
   - a: the SPLIT-14 amendment reversing the clause on shared training sides for this case, decided with wisconsin's.

   **Lennart (2026-11-08, discuss):** Reply (b): Forced by contract

   **Resolved (2026-11-08, Lennart):** (b), the forced split by contract: `contract_id` is the group column of the
   default 3 x 3 grouped splits, never a feature, tagged ForcedGroupedFromTemporal; the three windows and the exception
   to SPLIT-10 go, which supersedes D11's three windows on one training side (issue 5) and Andrej's expanding windows
   (issue 2). On the shipped folds the forced split scores the 2013 periods as the valid window does (+0.06 on the
   declared metric, SD 0.52; -0.005 on the Gini), a new fleet's cold start costs 1.10 (SD 0.86), and the leak test
   passes (the test year's own training periods gain -0.12 and -0.18 on the declared metric); the record's
   `required_split` and tag follow, and its CC and Assessment lines of 2026-11-08 give the numbers.

   [^a6a]: **LEAK-41** (Must; 2026-11-06, last clause amended 2026-11-08 on this dataset's issue 7): "No model is
     trained or scored on rows selected by the realized weight (such as full-year rows only); a row with no amount at
     risk may go under USE-7, its claims counted in the notes; a selection the source made before release, the same
     in train and test, that cannot be undone, defines the task's population and is sized in the notes."
   [^a6b]: **SPLIT-14** (Must; amended 2026-11-02, Andrej; reframed 2026-11-05, Lennart): "A temporal task has at
     least 3 windows, and no window's train side holds less than 50% of the data. ... Each window has its own train
     side: windows that share one train side test one model on several test periods, which is one evaluation, not
     several. As time moves on, a refit sees the data that arrived since, so each window trains on what is known
     before it starts." **SPLIT-11** (Should): train on everything before the window.
   [^a6c]: **SPLIT-9** (Must): a training row whose label tells a test row's outcome and was not yet known at the
     prediction point must not be in train.
   [^a6d]: **MET-15** (Must): a realized denominator is the metric's row weight and the task's `sample_weight`, never
     a feature; **LEAK-41**: such a column is never a model input.
   [^a6e]: **MET-14** (Should): an amount over a varying time on risk ships as the rate per unit when the decision
     prices per unit; "A per-contract target stays when the planned term is constant and known at the prediction
     point".
   [^a6f]: **SPLIT-8** (Must): a release that cannot give the windows the windows rule asks for ships in the closest
     regime that keeps the rows, grouped by the entity when the periods are stacked and the entities recur, after a
     leak test across the split. Andrej, 2026-11-02, on spanish coverage: "Forced group splits should be fine".


   [^windows]: **SPLIT-14** (Must), amended 2026-11-02 (Andrej) and reframed 2026-11-05 (Lennart): "Each window has its
     own train side: windows that share one train side test one model on several test periods, which is one evaluation,
     not several." Its Cases row for this dataset still records the expanding windows of issue 2.
   [^forced]: **SPLIT-8** (Must; narrows **SPLIT-14** and **USE-10**): a release with too few periods for three windows
     ships "in the closest regime that keeps the rows, tagged as forced from temporal, with the cost measured against
     the valid windows where the data has any"; "a forced split, grouped or IID, gets a leak test across the split and
     the leak probes". **LEAK-41** (Part 3) outranks **SPLIT-14** (Part 4) only where meeting one rule means breaking
     the other; **SPLIT-8** meets both, so rank does not decide for A (principles.md, How to decide, 4). "A Must has no
     exceptions: only a higher-ranked Must overrides it, and anything else is an amendment" (principles.md).
   [^early]: **LEAK-41** (Must, 2026-11-06): "No model is trained or scored on rows selected by the realized weight".
   [^andrej]: Andrej, 2026-11-02, issue 2: "I don't want to have the same training data and different test sets. We
     assume that whenever we have different test sets, we would be retraining. Given one test period we test the same
     model."
   [^spanish]: Andrej, 2026-11-02, spanish coverage: "Forced group splits should be fine".

7. **The source left out every period under 30 days: amend the rule for such a selection, or bar the dataset?**

   * **Problem:**
     - No model may be trained or scored on rows selected by their realized length[^floor], and every row here passed
       such a selection: before release, the organisers left out every period of cover shorter than 30 days.
     - The cut periods and their claims are not published, so neither a repair nor a change of the definition can undo
       it.
     - The rule admits no exception, so keeping the dataset takes an amendment for a selection the source made before
       release, and without one the rule bars it[^must].
   * **Background:**
     - The lengths stop at an edge, not a taper: no period of 29 days, 909 of 30, 2,074 of 31 and about 700 a day at 32
       to 40 days.
     - A vehicle's consecutive periods leave 1,558 gaps of 1 to 29 days, flat at about 45 a day, where the dropped
       periods would sit, and no period starts after 2 December, since a later start could not run 30 days within the
       year.
     - The 2014 file the game priced has the same floor, so the game's own population was the periods of cover of a
       month or more.
   * **Effect on the task:**
     - The dropped periods are many by rows and few by weight: some 15% of the rows (about 13,000 periods) and about
       1.5% of the vehicle-years, as a period under 30 days holds at most 0.08 vehicle-years (the density at 30 to 59
       days extrapolated down to one day).
     - Short periods claim more per vehicle-year (early ends of 30 to 59 days 0.143 to 0.160, against 0.124 for 180 days
       or more), so the dropped ones likely did too: the task leaves out a riskier slice that the insurer does price.
     - The selection is the same on the training and test sides but uneven across the shipped windows (roughly 11%, 3%
       and 1.6% of their vehicle-years, newest first, by a rougher extrapolation that assumes a flat density); that
       falls away under the forced split of issue 6, where every year carries the same cut.
   * **Consistency:** No precedent: the rule dates from 2026-11-06 and no selection by length made by a source has been
     ruled on; frempl_french_motor_personal_line and the other insurance tables with a minimum length would be checked
     under an amendment.
   * **Panel:**
     - The advocate first asked to accept the floor with a note as the source's population, then conceded that the form
       is an amendment.
     - The critic: a note cannot settle a rule that admits no exception, and without an amendment the next dataset with
       a floor set by its source is decided without a rule.
   * **Unknown:** How far the floor moves the scores and the order of models; a sensitivity run that adds a second floor
     (say 60 days) on both sides would size it (optional).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep with the note (implemented) | the notes name the floor as the source's selection, with its evidence and size, and no ruling is made | nothing changes | a note cannot settle a rule that admits no exception; the next dataset with such a floor is decided without a rule |
     | B | Amend the rule | a selection the source made before release, the same in train and test, that cannot be undone, defines the task's population and is sized in the notes; a Cases row for this dataset; frempl and the siblings checked for a minimum length | keeps a real task whose selection is small by weight and the same on both sides; one ruling for every source with such a floor | the task's population is the periods of a month or more, not every period the insurer prices |
     | C | Read the rule as barring the dataset | selections a source made count too, so the dataset goes `No`, and so does any sibling with such a floor | the rule's letter, without an amendment | loses the family's only commercial-fleet damage table over about 1.5% of its vehicle-years |

   * **Recommendation:** B: the selection is the organisers', made before release, small by weight, the same on both
     sides and in the game's own 2014 file, and it cannot be undone. **Decision:** B (amend the rule) or C (the dataset
     goes `No`)? A, the note alone, is not open: the rule admits no exception.

   **Notes for the AI:** on B, the amendment replaces LEAK-41's last clause in leak_checks.md in place, with the date,
   the curator and this case (the main session's edit): "No model is trained or scored on rows selected by the realized
   weight (such as full-year rows only); a row with no amount at risk may go under USE-7, its claims counted in the
   notes; a selection the source made before release, the same in train and test, that cannot be undone, defines the
   task's population and is sized in the notes." Add a LEAK-41 Cases row for this dataset (the floor of 30 days, about
   1.5% of the vehicle-years), check frempl_french_motor_personal_line and the other insurance siblings for a minimum
   length, and write a CC line; the note in `curation_comments` is written (2026-11-06). Optional: the sensitivity run
   with a second floor of 60 days. On C: the record's `suggestion` goes `No`, and the siblings with a floor are
   reopened.

   [^floor]: **LEAK-41** (Must, 2026-11-06), last clause: "No model is trained or scored on rows selected by the
     realized weight (such as full-year rows only); a row with no amount at risk may go under USE-7, its claims counted
     in the notes."
   [^must]: principles.md, "Exceptions and amendments": "A Must has no exceptions: only a higher-ranked Must overrides
     it, and anything else is an amendment." The remedy ladder: "Exclusion is for a Must that cannot be fixed."

   **Resolved (2026-11-08, Lennart):** B, LEAK-41's last clause is amended for a selection the source made before
   release, the same in train and test, that cannot be undone: it defines the task's population and is sized in the
   notes (the rule's wording and its Cases row are the main session's edit of leak_checks.md); the notes' floor bullet
   cites the amendment, and the task covers the periods of cover of a month or more, about 1.5% of the vehicle-years
   cut. The siblings checked on their released lengths: no other insurance table of PR #47 has a minimum set by its
   source (frempl_french_motor_personal_line, spanish_motor_insurance_coverage_level_2022_2024,
   australian_vehicle_insurance_2004_2005, fremtpl2 and bemtpl97 start at one day or less and run on without an edge;
   spanish_motor_insurance_2015_2018 has a planned year whose lapses cut it from one day on; pricing_game_2017_french_mtpl
   has no length column).

8. **Keep the Gini as the stand-in for the game's market, or score the uniformly rescaled weighted Tweedie deviance?**

   * **Problem:**
     - The game's market cannot be computed, so the closest computable metric stands in for it, its closeness measured
       on the shipped splits where possible[^standin], and that closeness is now measured.
     - The game scaled every player's premiums by one uniform factor and sent each insured to the cheapest premium, so
       it rewarded the relative prices, their order and their spread, while the Gini scores only their order.
     - In a simulation of the game's market on the shipped windows the uniformly rescaled weighted Tweedie deviance
       picks the market's winner more often than the Gini, but it would leave the family's stand-in and need a new
       library metric[^newmetric].
   * **Background:**
     - The rescaled deviance multiplies each model's predictions by one factor so that its premiums total the window's
       claims, as the game set every player's total to 2.5 million euros ("un facteur d'inflation appliqué
       uniformément", rules Sec. 4), then scores the exposure-weighted Tweedie deviance (power 1.5) of the rate; any
       common total gives the same market.
     - The Gini gives a tariff and the same tariff with its relativities doubled on the log scale the same score (0.173
       for the Tweedie GLM).
   * **Experiments:**
     - The market simulated on the three shipped windows (the mediator's run): 8 tariffs (two LightGBMs, the Tweedie
       GLM, the GLM's relativities raised to the power 0.5, 1.5 and 2, the LightGBM's to 0.5, and the constant), each
       rescaled to the window's claim total, each period going to the cheaper premium, in every two-player market (84
       pairs over the windows).
     - The rescaled deviance picks the market's winner in 76 of 84 pairs; the Gini in 44, and it ties on 21, as it
       cannot see a change of spread; among the fitted tariffs alone (two LightGBMs, the GLM, the constant; 18 pairs)
       the two are close, 16 for the deviance and 15 for the Gini.
     - Window means: by the rescaled deviance (lower is better) the GLM 89.63, the constant 90.82, the LightGBM 91.34
       and the GLM with doubled relativities 94.27; by the Gini the GLM 0.173 (doubled too), the LightGBM 0.157 and the
       constant 0. The LightGBM's relativities run too steep (actual over expected by predicted fifth from 1.4 to 2.0 in
       the cheapest fifth down to 0.5 to 0.9 in the dearest), and the rescaled deviance puts it behind a flat tariff.
     - Limit: two-player markets of synthetic tariffs; the real game had many players and broke ties among the cheapest
       at random.
   * **Consistency:**
     - Keeping the Gini follows australian_vehicle_insurance_2004_2005 (D8) and
       spanish_motor_insurance_coverage_level_2022_2024, which kept it as a stand-in; neither measured its closeness to
       a market that rescaled uniformly.
     - pricing_game_2017_french_mtpl scores a Tweedie deviance on its own facts: its game kept the price level and
       ruined a player at 170% losses.
     - Switching departs from australian and spanish coverage on a fact that sets this case apart: its original is a
       market that rescaled uniformly, and the closeness to it is measured.
   * **Panel:**
     - The advocate: the Gini follows australian and spanish coverage; the rescaled deviance takes its scale from the
       test total, is noisier on the newest window and needs a new library metric; both metrics rank the GLM above the
       LightGBM.
     - The critic and the domain practitioner: the game rescaled uniformly and rewarded the relative prices, and only
       the rescaled deviance ranks the over-steep tariffs below a flat one, as the market did.
     - The mediator: by the letter of the stand-in rule the measurement favours the rescaled deviance; how large a gap
       justifies leaving the family's Gini, against its costs, is a weighing call.
   * **Unknown:** Whether the rescaled deviance separates the models on the newest window; bootstrap standard errors of
     its differences per window (the GLM against the constant, the LightGBM against the GLM) would settle it, and if the
     newest window cannot separate the GLM from the constant, keeping the Gini has the stronger case.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the Gini (implemented) | the normalized weighted Gini of the rate stays the stand-in, its reason stating the measured shortfall (44 against 76 of 84 two-player markets) | the stand-in of australian and spanish coverage; no new metric; level-free, as the game was | blind to the spread of the relativities, which the market priced; a tariff and its doubled relativities tie; not the closest stand-in as measured |
     | B | The rescaled weighted Tweedie deviance | each model's predictions rescaled to the window's claim total, then the exposure-weighted Tweedie deviance (power 1.5) of the rate | the closest to the market as measured (76 of 84 pairs); level-free, as the game was; a proper score of the relative prices | a new library metric with its tests; its scale factor uses the test window's claim total, which no insurer knows when it prices; noisier on the newest window; leaves the family's stand-in |

   * **Recommendation:** B, after the bootstrap of its differences per window: the stand-in rule asks for the closest
     computable metric, and B is the closer as measured (76 against 44 of 84 markets); if the newest window cannot
     separate the GLM from the constant, A. How much closeness is worth the new metric's costs is still yours to weigh.
     **Decision:** A (keep the Gini) or B (the rescaled deviance)?

   **Notes for the AI:** on A, a CC line; the metric reason already states the shortfall (2026-11-06). On B, first the
   bootstrap standard errors of the rescaled deviance's differences per window (above); then the new metric in the
   shared library (MET-13: a reference implementation, tested against a direct computation on random inputs and on a
   hand case, timed on 1M rows), its scale factor sum(weight x y) / sum(weight x prediction) over the scored rows,
   stated as the oracle scale; `Metric.stand_in` with the closeness in the reason; a CC line naming the fact that sets
   the case apart from australian and spanish coverage (a market that rescaled uniformly, the closeness measured); a
   MET-11 Cases row (the main session's).

   **Lennart (2026-11-08, discuss):** This owuld mean the metric could only be used for testing, not validaiton, as we
   ues info from test, right?

   **Answer (AI, 2026-11-08):** No: the factor uses only the labels of the rows being scored, as every metric does, so
   the rescaled deviance works on a validation fold the same way.

   * What was asked: whether the rescaling takes information from the test rows, so the metric could score a test
     window but not guide validation, early stopping or tuning.
   * What the metric does, on any set of scored rows: it multiplies the model's predictions by one factor, the rows'
     weighted claim total over their weighted predicted total, then takes the weighted Tweedie deviance. The labels
     enter the factor exactly as they enter the deviance; the model never sees them, and its predictions are fixed
     before scoring.
   * In validation: each validation fold is rescaled to its own claim total. Early stopping or tuning on it then
     prefers the tariff with the best relative prices, which the game rewarded; nothing from the test rows is used.
   * What the issue's con meant by "no insurer knows the test total when it prices": the score takes the price level
     out, as the Gini does, so it cannot reward a model for the right level. The game did the same: it set every
     player's premiums to one total before the market ran.
   * One practical cost: no library ships it as an early-stopping metric, so a learner that stops on the validation
     score needs it as a custom evaluation function (the factor computed per evaluation set). The benchmark's TODO on
     dataset-specific metrics already covers custom metrics in validation.
   * The bootstrap of its differences per window, which the recommendation waits for, runs once issue 6 settles the
     split, since the split decides which sets are scored. The decision (A or B) stays open.

   **Lennart (2026-11-08, discuss):** Agree. GO with the change in metric and use it going forward

   **Resolved (2026-11-08, Lennart):** B, the uniformly rescaled, exposure-weighted Tweedie deviance at power 1.5 as
   the stand-in for the game's market: the new library metric `rescaled_mean_tweedie_deviance` (tested against the
   formula written out, invariant to a common scale of the predictions, 1M rows in 0.03 s), with a floor of 0.1 per
   vehicle-year, two orders below the cheapest cells' 26 to 31. On the contract folds it separates the GLM from the
   constant (1.39, bootstrap standard error 0.46, on all 9 folds), the regularised LightGBM less clearly (0.59, 0.58),
   and an untuned LightGBM scores worse than the constant; it picks the market's winner in 225 of 252 two-player
   markets against 128 for the Gini. It is the stand-in for later pricing games whose market rescales uniformly (the
   MET-11 Cases row is the main session's).


   [^standin]: **MET-11** (Must): a stand-in applies when the source's metric cannot be computed, "and the closest
     computable metric replaces it; it names the original and why the original cannot be computed, and the closeness is
     measured on the shipped splits where possible". The mediator and the critic read the choice under this rule, not as
     a weighing between the source's metric and the fallback (**MET-10**, Weigh), since the original cannot be computed.
   [^newmetric]: **MET-13** (Must): a custom metric ships as a reference implementation in the shared metric library, in
     the same change, tested against the official implementation and timed on 1M rows.

9. **Shared rating profiles across the contract folds: keep the split as shipped, or also join the three contracts that share a registration?**

   * **Problem:**
     - The leak test across the forced split flags a lookup: 4.3% of the test periods have the same rating classes and
       start date as training periods of another contract, and giving a model those training periods' mean outcome
       improves the declared metric by 0.117 (standard error 0.021, on 9 of 9 splits)[^p23].
     - Two readings were open: one client insured under several contract numbers, whose outcome would then cross the
       split and call for a wider group, or different fleets in the same common rating cell, whose repeats are natural
       and need nothing[^unit].
     - The follow-up finds no client link and no shared outcome (the matches are common cells, nearly all on 1 January,
       and the gain comes from how the probe builds the lookup on the training side), so what is left to decide is the
       one link between contracts the data states, a registration under three contracts with one period each and no
       claim.
   * **Background:**
     - The probe's lookup: for each test period, the weighted mean charge per vehicle-year of the training periods with
       the same 16 inputs (the fleet's classes, the vehicle's two classes, the start date and the length to 31 December)
       joins the inputs of a regularised Tweedie LightGBM; the training periods get the same column out of fold, from 5
       random folds of the training periods, so a training period also reads the other vehicles of its own fleet, which
       a test period never can.
     - 37.6% of all periods start on 1 January, the cut every vehicle in force gets at the year's start, and 54% on the
       1st of a month; the vehicles of one fleet in one period share every input but their own two classes.
     - The contract numbers appear to run in the order of subscription, so a profile, which holds the contract's age
       class and the year, also fixes a cohort of contract numbers.
     - Registration 32348 (the anonymised `vehicle_id`) has one period under each of contracts 6168, 6169 and 6170, in
       three zones, two of them overlapping in 2013; every other vehicle of the 68,485 keeps one contract. The notes say
       "one of 68,485 has two": it has three.
   * **Effect on the task:**
     - None measured from the shared profiles: a model gains nothing from another fleet's outcome in the same cell beyond
       what the classes give it.
     - The registration's three periods land on different sides of a fold in every repeat, with no claim to carry.
   * **Experiments:** the counts on the whole table or the 9 shipped splits; every lookup on those 9 splits x 3 seeds,
     each side capped at 50,000 periods and scored by the declared metric, as the probe runs.
     - Where the matches fall: 94.3% of the matched test periods start on 1 January (37.6% of all test periods) and
       98.4% on the 1st of a month, the rest on quarter starts (1 April, 1 July, 1 October); 86% of the shared profiles
       are held by two contracts (at most six), and 95% of the 2,704 contract pairs with a shared profile share it in one
       year only.
     - No client: 29 of the 2,704 pairs (1.1%) are numbered within 2 of each other, against 0.4% of the pairs that share
       only the fleet's classes and start and 0.07% of random pairs of one subscription cohort; a lookup restricted to
       contracts numbered within 20 reaches 0.3% of the test periods and gains nothing.
     - No shared claim: none of the 24 matched pairs with a claim on both sides has the same charge, and the charges that
       recur in the claim file are flat amounts (130, 150 and 2,200 before the release's scaling).
     - No shared outcome: a claim on one period of a matched pair goes with a claim on the other 1.45 times as often as
       on average (phi 0.031, 3,905 pairs), against 1.20 times (phi 0.014) for the same cell in another year, a gap
       within noise (standard error of phi about 0.016).
     - No event: a lookup of the same cell, with the start and the length to 31 December left out, over periods started
       within 7 or 31 days but not the same day gains -0.015 (SE 0.019) and +0.013 (SE 0.023) with the probe's folds
       (-0.002 and -0.050 with folds by contract); over the same calendar date in another year -0.002 (SE 0.028).
     - Where the gain comes from: per period, the test periods with a lookup lose 0.012 and those without one gain 0.129,
       so the lookup does not predict the matched periods; with the probe's random row folds 19.2% of the training
       periods get a lookup, 78% of its weight from their own fleet, against 4.3% of the test periods.
     - The lookup built for the training periods as the test periods see it, out of fold by contract, gains nothing in
       any form, and on the matched periods it loses 0.047 (SE 0.023): a test that would have kept the gain had another
       fleet's outcome reached the test periods[^proof].

       | Lookup over the training periods with | Test periods with one | Gain, the probe's row folds | Gain, folds by contract |
       |---|---|---|---|
       | the same 16 inputs | 4.3% | +0.117 (SE 0.021, 9 of 9) | -0.047 (SE 0.042, 4 of 9) |
       | the same 16 inputs, the match alone (no outcome) | 4.3% | +0.029 (SE 0.029) | -0.053 (SE 0.033) |
       | the same inputs but the start | 8.6% | +0.047 (SE 0.033) | -0.016 (SE 0.041) |
       | the same inputs but the start, in the same year | 4.5% | +0.080 (SE 0.024) | -0.042 (SE 0.033) |
       | the same 16 inputs, a contract numbered within 20 | 0.3% | 0 | 0 |

   * **Consistency:**
     - Natural repeats of coarse inputs are kept with a note, as in sepsis_survival_minimal_clinical_records and
       ai4d_lab_tanzania_tourism_classification_challenge[^leak18]; this table's notes already keep its 13.5% of repeated
       periods on that ground.
     - frempl_french_motor_personal_line widened its group to records the data links by their dates[^frempl]; here the
       data links contracts only through the one registration, and a client guessed from contract numbers and classes is
       the kind of key the grouping rule bars[^unit].
   * **Panel:** none; raised by probe 23 on 2026-11-08.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | The split by contract, with a note (implemented) | the notes say the shared profiles are natural repeats and why the probe's flag is no leak; rows, split and score unchanged | what the evidence supports; no fold changes | the registration under three contracts stays on several sides (three periods, no claim) |
     | B | Also join the contracts that share a registration | the note as in A; the group becomes the contract with the contracts that share a vehicle joined (6168, 6169 and 6170 in one group, 18,035 groups) | every vehicle on one side; a key the data states exactly | a derived group column; every fold reshuffles, so the notes' fold numbers are measured again; no score can move |
     | C | Group by a guessed client | contracts numbered next to each other with the same fleet classes joined | would catch a client with several contracts | a guess, not a key the data states; the matched pairs show no such link, and their lookup gains nothing |
     | D | A protocol line | the benchmark's instructions bar looking up other rows' outcomes | none found | no leak to bar; the benchmark cannot check it |

   * **Recommendation:** B: the flag needs only the note, since no fleet's outcome reaches another fleet's test periods,
     and the one exact link between contracts costs little to honour as the rule on repeated entities asks; A if three
     periods without a claim do not seem worth reshuffling the folds. **Decision:** A or B?

   **Notes for the AI:**
   - A and B: in `curation_comments`, the bullet on repeated rows (LEAK-18) gets after "8.6% without the start)": "Probe
     23 (2026-11-08) flagged a lookup of that profile across the folds (+0.117 on the declared metric, SE 0.021, 9 of 9
     splits). It comes from the probe's row folds, which let 19% of the training periods read their own fleet (78% of
     the lookup's weight): built out of fold by contract, as a test period sees it, the lookup gains -0.047 (SE 0.042);
     the matches are common cells, 94% on 1 January, with no shared claim and no client link (REVIEW.md issue 9)." The
     vehicle with "two" contracts has three: fix "one of 68,485 has two" in the grouping definition, `splits_comment` and
     the comment of `_clean` step 7 (A: "a vehicle keeps its contract, but for one of 68,485, with one period under
     each of three contracts and no claim").
   - B: in `_clean`, before `vehicle_id` is dropped, a group column (say `fleet_group`): `contract_id`, with the
     contracts that share a `vehicle_id` joined under the smallest number (connected components of the contract and
     vehicle pairs; assert that it joins exactly 6168, 6169 and 6170); `contract_id` dropped, `GROUP` the new column;
     rewrite the grouping definition ("a vehicle keeps its group"), `task_summary.split` and `changes`, `splits_comment`,
     Decision 2 and the notes' "Dropped:" bullet; re-run the fold measurements (`issues6_8/folds.py` of the exposure
     review's run folder) and the leak probes with probe 23, and update every fold number in the notes; a CC line naming
     the case (LEAK-17, SPLIT-24); `dataset check` and ruff.
   - Either way, for the main session: probe 23's shared-unit test draws the training side's lookup folds by row; on a
     grouped split it should draw them by group, as the test side sees the lookup, and report the gain on the test rows
     with a lookup apart from the rest. The probe-23 row of leak_checks.md's probe table cites this dataset's +0.117:
     it then reads as the probe's artefact (folds by contract: -0.047, SE 0.042). The run: the exposure review's run
     folder, `pricing_game_2016_french_fleet/apply_2026-11-08/probe23_units/` (`describe.py`, `describe2.py`,
     `lookups.py`, `lookups2.py`, `near_pairs.py`, `consecutive.py`, `shared_vehicle.py`, with their logs).

   **Lennart (2026-11-08, change):** Option B: Also join the contracts that share a registration.

   **Resolved (2026-11-08, Lennart):** B: the group column is `fleet_group`, the contract with the contracts that share
   a registration joined under the smallest number (6168, 6169 and 6170, the only shared registration in the data;
   18,035 groups), and the notes say the shared profiles are common cells and probe 23's flag an artefact of its old row
   folds. Every fold reshuffled and its numbers are measured again: the GLM beats the constant by 1.06 (standard error
   0.65, on all 9 folds), the rescaled deviance picks the market's winner in 217 of 252 pairs against 136 for the Gini,
   and probe 23, its lookup folds drawn by group, finds no leak (-0.23 on the test periods with a shared profile, SE
   0.17).

   [^p23]: **SPLIT-8** (Must): a forced split "gets a leak test across the split and the leak probes: does a row share
     its outcome, its unit's outcome or its period's outcome with the other side"; "a leak found is weighed case by
     case". Probe 23 (b), leak_checks.md: a gain above 2 standard errors reads as "the unit's outcome reaches the test
     rows through training; for a profile it can also be natural repeats (LEAK-18), and whether the copies are one
     entity decides (LEAK-17)".
   [^unit]: **LEAK-17** (Must): "Repeated entities in different rows (the same patient, house, molecule or object) leak
     the target across the split even when the rows differ: keep one row per entity when the use case is that row
     (USE-11), or group (SPLIT-24, SPLIT-29)." **SPLIT-24** (Must): "Group on a true group id, or on one constructed
     exactly from the data ... Never on a similarity-threshold cluster, and never on a hash of the feature vector
     standing in for an unknown entity."
   [^leak18]: **LEAK-18** (Should): "Few features and plausible repeats: natural, keep them and say so." Its cases:
     sepsis_survival_minimal_clinical_records, ai4d_lab_tanzania_tourism_classification_challenge (Lennart, 2026-11-05).
   [^frempl]: **SPLIT-24**'s Cases row for frempl_french_motor_personal_line: "a policy component joins records where one
     may continue another (starting the day the other ends, ages advanced) ... (Andrej, 2026-11-03), widened to a
     successor with one profile column changed and no counter lower (Lennart, 2026-11-08)".
   [^proof]: **EV-6** (Should): "A claim is proven by a test that could have refuted it."

**Review panel:** ship after changes (mediator). Tier full, a re-review of 2026-11-06 under LEAK-41 and MET-14 to MET-16
after D11 (issue 5): the claim, column and split auditors, the domain practitioner, the precedent checker, the blind
reviewer, the task gamer, the advocate and the critic with one rebuttal each, and the mediator, who ran two experiments
(the leak test across the contract folds, which passes, and the game's market simulated on the shipped windows). Claims:
35 audited, 32 hold (two effects within seed noise; probe 22's cited L2 arm without power, its Tweedie arm agreeing), 1
refuted (the implied claim that no row is selected by its realized length: the organisers' floor of 30 days, issue 7), 1
breach confirmed and already open (three windows on one training side, issue 6), 1 wording wrong (the run's change note
on option C); 6 settled numbers untested. Blind review: include with changes; its main concern is the weak, heavy-tailed
signal and the metric (a deviance or a Gini, not RMSE); its points on integer codes and on the clipping do not apply to
the shipped frame. Task gamer: no exploit above noise (the realized vehicle-years as a feature gain nothing under
Tweedie and +0.030 inside the noise under L2). Agreed: D11's target, weight, features and training side; probe 22 cited
with both arms; the four bands ordered; the text fixes (all made); the forced split grouped by contract as the fix
within the rules (the advocate withdrew its preference for the three windows); an amendment, not a note, for the floor.
Disputed, settled by the mediator and left to the curators: whether keeping the three windows stands on a par with the
forced split (issue 6: only by an amendment for the family; the practitioner ranks fidelity one window, then three
windows, then the forced split), whether the floor can be kept with a note (issue 7: no, an amendment), and whether the
metric is a weighing call or a stand-in whose closeness must be measured (issue 8: the latter; the pick between the two
measured candidates is the curators'). The mediator's issues 1 to 3 are issues 6 to 8 of this file; the panel of
2026-11-01 is in this file's git history.

<details><summary>Mediator</summary>

**Mediator report: pricing_game_2016_french_fleet (exposure re-review, 2026-11-06, full tier)**

My two experiments are the leak test (`leaktest.py`, `leaktest.out`, `leaktest.csv`) and the market simulation (`market.py`, `market.out`), in the run folder. Probe 22's actuarial arm has now landed, and I use it below.

**1. Recommendation (judgment record)**

Verdict: ship after changes.

Validity:
- SEL-2 holds. USE-1 and USE-8 hold (direct fit), and USE-5 holds.
- LEAK-7 and LEAK-37 hold (`exposure_to_year_end` is known at the start).
- LEAK-41 holds for the features and the weight. Probe 22 Tweedie arm: the weight as a feature gains +0.007 (SD 0.028). 1/weight alone scores 0.029 against the honest 0.143. No feature's gain goes through the weight above noise.
- LEAK-41's last clause is triggered by the source's 30-day floor. This is issue 2 for the curator: an amendment, not a note.
- SPLIT-9 holds.
- SPLIT-14 is broken as shipped (three windows on one training side). The fix is a re-split to SPLIT-8's grouped split by contract (option C). Its precondition, the leak test across the split, I ran: it passes (section 4).
- If C is taken, the exception to SPLIT-10 lapses.

Value:
- TP-4 holds: 0.110 / 0.157 / 0.189 against 0 for the weighted constant; 0.182 under C.
- TP-9 holds: 103 / 232 / 1,026 positive charges.
- MET-11: the stand-in's closeness to the game's market is now measured. The choice of metric is issue 3 for the curator.

Quality:
- CLEAN-14: four band columns should be ordinal. Cheap and safe, so fix it.
- The text corrections in section 2.

Weighed: original files +, real fleet-pricing task +, the family's only commercial-fleet table +; weak anonymised covariates −, a noisy newest window − (this drops out under C).

For the curator:
- issue 1, the split (C recommended; no fact left open);
- issue 2, the source's 30-day floor (an amendment of LEAK-41's last clause);
- issue 3, the stand-in metric (Gini, or the uniformly rescaled weighted Tweedie deviance).

**2. Changes to make now (no decision needed)**

1. **Probe 22 reporting (LEAK-41 Must, reporting clause; EV-1).** The notes' probe 22 sentence and REVIEW issue 5 cite only the L2 arm. probe22.txt and probe22_l2.txt are byte-identical, and in that arm the weight itself gains −0.0014 (SD 0.052): no power. Cite both arms and decide on the worse:
   - L2: as above, no power.
   - Tweedie (probe22_actuarial.txt): weight R² 0.378; the weight as a feature +0.007 (SD 0.028); 1/weight 0.029. Weight-mediated gains: exposure_to_year_end +0.017 (SD 0.029), distribution_channel +0.011 (SD 0.036), client_activity +0.008, fleet_size_class +0.005, fleet_management −0.004. All are under 1 SD.
   - The claim auditor's 3-seed Tweedie arm agrees: +0.0118 (SD 0.0067).
   - The notes' "would add 0.013 (5 of 5 seeds)" can stay, with this added.
2. **Effects within seed noise (EV-1).**
   - "A fit that ignores the weight loses 0.010 (SD 0.009, 4 of 5 seeds)": the claim auditor gets +0.005, 2 of 3 seeds.
   - "The time features add 0.007": the claim auditor gets +0.003.
   - Mark both "within seed noise".
3. **"A cut nobody scheduled" (EV-2).** 25.9% of early ends fall on a month's last day. Reword to "a cut not known at the start, a quarter of them on a month's end". It appears in task_summary.known, the Exposure bullet, the weight ScoringColumn description and Decision 1.
4. **Metric reason (MET-11 Must, which asks for the closeness to be measured).** Three edits:
   - Replace "the market rewarded the ranking of the risks" with "it rewarded the relative prices; the Gini scores their order, not their spread". The GLM and the same GLM with doubled relativities both score 0.173.
   - Drop the argument that the deviance "also scores the year's level". The uniformly rescaled form removes the level, as the game did.
   - Add the closeness measured in section 4, whichever metric issue 3 keeps.
5. **The 30-day floor bullet (LEAK-41).** Rewrite the "Anomaly: no period is shorter than 30 days" bullet as a LEAK-41 matter, whatever issue 2 decides:
   - the length histogram: 0 rows at 29 days, 909 at 30, about 700 a day at 32-40;
   - 1,558 gaps of 1-29 days between a vehicle's consecutive periods;
   - no start after 2 December;
   - the size: about 1.5% of vehicle-years overall (column auditor). Per window the claim auditor's rough figures are 11% / 3% / 1.6% of vehicle-years, newest first, assuming a flat density;
   - short periods claim more per vehicle-year (0.143-0.160 against 0.124);
   - it cannot be undone.
6. **REVIEW issue 6 text (EV-2).**
   - spanish_motor_insurance_coverage_level_2022_2024's valid window is above the floor (52.5%), not below it. Rewrite "What sets this case apart".
   - Replace the unpaired C comparison (0.174 against 0.171) with the split auditor's paired one: +0.005 (SD 0.022, 9 folds); a new fleet's cold start costs −0.004 (SD 0.013).
   - Add the leak test of section 4.
7. **CHANGES.md.** "0.182 overall, no more optimistic than the valid window" holds only for C's 2013 rows: 0.174, paired +0.005.
8. **Record, Exception to SPLIT-10 (2026-11-02, Andrej).** "Serves SPLIT-14: three windows on distinct training sides" is stale. If A survives, the ground is LEAK-41 plus the floor, for the January window only. Under C the exception is removed.
9. **splits.md Cases (principles, Exceptions).**
   - The SPLIT-14 row for pg16 still says "applied" for the expanding windows. Replace it with the outcome of issue 6.
   - Add the missing SPLIT-10 rows of kind `exception` for pg16 (unless C removes it), spanish_homeowners_motor_insurance_2010_2014 and wisconsin_local_government_property_insurance_fund (all 2026-11-02).
10. **The pro-rata claim (EV-2).** "AMRAE ... not checked": cite the sources the claim auditor and practitioner checked (the French fleet guide on pro-rata temporis regularisation; AXA Belgium's regularisable / non-regularisable fleet premiums).
11. **CLEAN-14 (Should, P7, cheap and safe).** Declare these as ordinal, with the column auditor's level lists, and update the Dtypes bullet: contract_age_class, vehicle_age_class, deductible_class, insured_value_class. The 2026-11-01 column table calls deductible_class ordered; the shipped dtype is not. This lands with the next rebuild, which the curator asks for.
12. **Optional, practitioner.**
    - A one-line note: insurers may keep the unexpired premium after a covered total loss, so the rate per realized vehicle-year slightly overstates the break-even rate. This is an inference, unchecked.
    - A line on trend: 167 per vehicle-year in training against 180-205 in 2013.

**3. Issues for the curator, ranked**

**Issue 1 (P4, SPLIT-14 Must; REVIEW issue 6): three windows on one training side. Recommended: C.**
- **Problem:** all three splits train on the same 56,178 rows, which SPLIT-14 counts as one evaluation. The newest window holds 7% of the test vehicle-years and 103 positive charges, has a bootstrap SE of 0.068, and gets a third of the score. The window mean (0.154) runs below the same model pooled over 2013 (0.171).
- **Which rule wins:**
  - This is not a conflict that rank settles. LEAK-41 (Part 3) does not force A, because C meets LEAK-41 and SPLIT-14 together (principles, How to decide 4). No higher Must stands behind A.
  - The practitioner's USE-10 objection (C tests unseen fleets; on fidelity B > A > C) meets SPLIT-8, which says it narrows USE-10. Its cases (spanish coverage, pg17, frempl, nba, open_university) applied it to recurring known entities.
  - The measured cost is small: on the same 2013 rows C is +0.005 (SD 0.022) against the valid window, and a new fleet's cold start costs −0.004. No history feature ships, and the record found the previous year's history adds nothing (0.667 against 0.668 ROC AUC).
  - On the rules as written, C is the remedy (fix the definition by re-splitting). A or B is open only as a deliberate amendment of SPLIT-14.
- **Advocate's best:** A or B keeps the use case: one tariff for the year, judged on the 2013 book. In its rebuttal it withdrew its preference for A and accepts C.
- **Critic's best:**
  - The A amendment drafted in issue 6 reaches only this dataset. That makes it an exception to a Must in effect, which the principles bar.
  - It would reverse Andrej's amendment of 2026-11-02, made on this very dataset, and Lennart's reframing of 2026-11-05.
  - B would reopen spanish coverage, nba, open_university and distribution_transformers_at_cauca_department.
- **The precondition both sides named is now met** (section 4, experiment 1). No year-level leak crosses the contract folds.
- **Options:**
  - (C) Re-split, grouped 3 × 3 by `contract_id`. Recommended. contract_id becomes the group column, never a feature. Tag it `ForcedGroupedFromTemporal` and drop `temporal`. The SPLIT-10 exception goes. Rewrite task_summary.split, the fit text and the splits_comment, saying what the dates would change and the −0.004 cold-start cost. Update the record's required_split and tags. After the rebuild, run the leak probes on the grouped split (probes/group.txt).
  - (A) Keep A by amending SPLIT-14 for the whole family.
  - (B) Keep one window by amending SPLIT-14 below three windows.
  - (D) The expanding windows: out, because LEAK-41 bars them.
- **Decision needed:** C, or an amendment (A or B). Only an amendment needs deciding together with wisconsin issue 3. C does not, since the leak test sets pg16 apart from wisconsin.

**Issue 2 (P4, LEAK-41 Must, last clause): the source selected every row by its realized length (no period under 30 days).**
- **Problem:** "No model is trained or scored on rows selected by the realized weight." The organisers dropped periods shorter than 30 days before release. The evidence:
  - the histogram has a sharp edge at 30 days (0 rows at 29, 909 at 30);
  - 1,558 gaps of 1-29 days between a vehicle's consecutive periods sit where the dropped periods would be;
  - no period starts after 2 December.
  The cut periods and their claims are not published, so neither repair nor a definition fix is possible.
- **Effect:**
  - About 1.5% of vehicle-years overall.
  - The short periods claim more per vehicle-year.
  - The selection is the same on both sides and was in the game's own 2014 file.
  - It is uneven across A's windows (rough estimate: 11% of the newest window's vehicle-years). That point falls away under C, where every year carries the same cut.
- **Advocate's best:** the source made this selection before release; it is small by weight and the same on both sides. The advocate concedes that the form is an amendment.
- **Critic's best:** a Must has no exceptions, so "accept it with a note" is not available. Without a rule, the next dataset with a source-side floor is decided ad hoc.
- **What is settled:** the form. Both sides now ask for an amendment.
- **What is left:** the curator's ruling. A Must that cannot be fixed means `No` unless the rule is amended.
- **Options:**
  - (a) Amend LEAK-41's last clause. Draft: "a selection the source made before release, the same in train and test, that cannot be undone, defines the task's population and is sized in the notes". Add a Cases row for pg16, and check frempl and the other siblings for a minimum length. Recommended.
  - (b) Read the clause as covering source selections too: the dataset goes `No`, and so do the siblings with such a floor.
- **What would size it further:** a sensitivity run that adds a second floor (say 60 days) on both sides and reports how the scores and the ranking of models move. Optional.

**Issue 3 (P6, MET-11 Must): which stand-in is closest to the game's market.**
- **The rule:** the critic is right that MET-11 governs, not MET-10. MET-10 weighs the source's metric against the fallback; here the original, a market, cannot be computed, so a stand-in must be "the closest computable metric", with its closeness "measured on the shipped splits where possible".
- **Now measured** (section 4, experiment 2). I simulated the game's rule on the shipped windows: every tariff rescaled uniformly to one total, each period going to the cheaper premium.
  - Across all two-player markets, the rescaled weighted Tweedie deviance (p = 1.5) picks the market's winner in 76 of 84 pairs. The Gini picks it in 44 and ties in 21, because it cannot see a change of spread.
  - Among the fitted tariffs alone (two LightGBMs, the GLM, the constant; 18 pairs) the two are close: deviance 16 of 18, Gini 15 of 18. Over the 7 non-constant tariffs, the gap comes from the tariffs that differ in spread.
- **Advocate's best:**
  - The Gini follows australian (D8) and spanish coverage.
  - The deviance takes its scale from the test total, is noisier on the newest window, and needs a new library metric (MET-13).
  - Both metrics rank the GLM above the LightGBM.
- **Critic and practitioner's best:**
  - The game rescaled uniformly and rewarded relative prices. The Gini gives a tariff and the same tariff with doubled relativities the same score (0.173).
  - The rescaled deviance ranks the over-steep tariffs below a flat one: GLM doubled 94.27, LightGBM 91.34, constant 90.82, GLM 89.63.
- **My reading:** by the letter of MET-11 the measurement favours the rescaled deviance. How large a closeness gap justifies leaving the family's Gini, against the costs above, is a weighing call, so it is the curator's.
- **Options:**
  - (a) Uniformly rescaled weighted Tweedie deviance as the stand-in. A new library metric; state the oracle scale.
  - (b) Keep the Gini, with the measured shortfall in the reason.
- **What would settle it:** bootstrap SEs of the rescaled deviance's differences (GLM against the constant, LightGBM against the GLM) per window. If the newest window cannot separate the GLM from the constant, (b) has the stronger case.

Disputed framings, settled:
- (i) A is not symmetric with C under the current rules. A needs an amendment, and C is the rule's own remedy (issue 1).
- (ii) The floor cannot be accepted by a note. LEAK-41 is a Must, so it takes an amendment (issue 2). The 11% per-window figure is a rough extrapolation. It does not decide anything and is moot under C.
- (iii) The metric is a MET-11 question, not a MET-10 weighing. The pick between two measured candidates is then the curator's (issue 3).
- The critic's factual correction stands: n_vehicles and insured_value_class are kept (D4; "ND" made missing), not dropped. No change follows.

Task gamer's exploits, mapped. The definition has no `Potential leak, kept on purpose:` note. Its accepted warnings cover duplicate rows (LEAK-18).

| # | Exploit | Rule | Status | Gain measured | What the notes say |
|---|---|---|---|---|---|
| 1 | The realized exposure as a feature | LEAK-41 (the weight is never an input) | Known (notes, probe 22) | Tweedie: 0.1985 against honest 0.2061 (none). L2: +0.030, inside the L2 noise of 0.08-0.14. Probe 22 Tweedie: +0.007 (SD 0.028) | +0.013, consistent. Not an issue |
| 2 | Exposure over planned exposure (the cut-short ratio) | LEAK-41 (a column that encodes the weight) | Known in substance (the 1/weight ceiling of 0.029) | +0.006, noise | Not an issue |
| 3 | A same-key successor row exists (built from future rows over all rows) | LEAK-10 (set after the prediction point), built transductively | New | +0.002, noise; vehicles cannot be chained without the dropped ids | Not an issue |

The gamer found no flaw that hurts an honest model. Settlement of 2012 claims could not be checked, which is the delay already simulated in the notes.

**4. Agreed facts, and my two experiments**

Agreed by both sides and every auditor:
- 87,228 periods, 68,485 vehicles, 18,037 contracts.
- The target reproduces from the source: all 4,568 claims match, total 6,675,926.40.
- `exposure` is the source's realized vehicle-years. It is the weight scoring column and `sample_weight`, never a feature (16 features).
- exposure ≤ exposure_to_year_end on every row.
- The metric matches Kaggle's weighted Gini to 1e-12.
- Weighted Tweedie LightGBM 0.110 / 0.157 / 0.189, newest first; the constant scores 0; the newest window beats it by 1.7 SE.
- The old expanding sides admitted early-ended 2013 periods at 0.127 / 0.131 claims per vehicle-year, against 0.115 / 0.116 for the periods still running. D11's training side is the honest one (LEAK-41 over SPLIT-11).
- The three splits share 56,178 training rows (64.4%). 2012 trained on 2011 alone would hold 30.4%, below the floor.
- 76-81% of test periods have their contract in training.
- Claims per vehicle-year are 0.117 / 0.119 / 0.119 in 2011-2013.
- No period is shorter than 30 days.
- probe22.txt and probe22_l2.txt are the same L2 run.
- No exploit above noise.

Experiment 1: SPLIT-8's leak test across the contract folds, the wisconsin way.
- Setup:
  - folds: 3 × 3 GroupKFold by Num_contrat over 2011-2013 (the split auditor's folds);
  - model: regularised Tweedie LightGBM fitted with the weight, scored by the declared scorer;
  - each test year was predicted by a model trained without that year's training rows, against one trained without as many random rows;
  - period_start encoded two ways: the day of the year, or the date, which lets the model read the year.
- Charge per vehicle-year by year: 159.6 / 173.7 / 184.3.
- Results (mean over 9 folds):

  | Encoding | Pooled gain of the same-year rows | Within-year gain |
  |---|---|---|
  | Date (year readable) | −0.001 (SD 0.020), positive in 2 of 9 | −0.0035 (SD 0.021) |
  | Day of year | +0.008 (SD 0.015), positive in 7 of 9 | +0.006 (SD 0.016) |

- Reading:
  - Wisconsin's signature is absent: there the pooled gain was +0.113 against +0.008 within a year. Here the pooled gain is no larger than the within-year gain, and nothing crosses when the year is readable.
  - The small day-of-year effect is within-year structure, about 1.7 SE, at the noise level.
  - The test passes.

Experiment 2: the game's market, simulated on the three shipped windows.
- Tariffs: the regularised LightGBM, a deeper LightGBM (63 leaves), the Tweedie GLM, the GLM's relativities raised to the power 0.5, 1.5 and 2, the LightGBM's raised to 0.5, and the constant.
- Each tariff was rescaled to the window's claim total. Any common total gives the same allocation; the game's fixed 2.5 million euros changes only the profit levels. Each period went to the cheapest premium.
- Results: given above in issue 3.
- Limit: these are synthetic two-player markets. The real game had many players and random ties among the cheapest.

**5. Consistency with precedent**

- **D11 (target, weight, metric):** consistent with fremtpl2, bemtpl97, australian D8, frempl D9 and spanish D10 (precedent checker).
- **D11's reversal of Andrej's expanding windows:** set apart by a new measurement and a newer Must. Not drift. hotel_booking_demand (SPLIT-9) supports it.
- **Issue 1:**
  - C follows spanish coverage, which has the same facts: three stacked years, one valid window above the floor, recurring entities. It also follows pg17, frempl, nba and open_university.
  - The fact that sets pg16 apart from wisconsin is now measured: the leak test passes (pooled −0.001 with the year readable, against wisconsin's +0.113). pg16 can therefore be decided without waiting for wisconsin issue 3, unless the curator prefers an amendment.
  - The precedent checker's reflection prompt still applies to the implemented state:
    **Consistency check (AI, 2026-11-06):** three windows of 2013 on one training side differ from spanish_motor_insurance_coverage_level_2022_2024 (forced grouped, 2026-11-02), which has the same facts. What sets this case apart?
    (a) Amend SPLIT-14 for the family. The only candidate fact, daily dates that allow sub-windows on one side, is the cut Andrej's amendment rules out.
    (b) Treat pg16 like spanish: C, grouped by `contract_id`. The leak test now passes.
    (c) Reopen spanish: does not apply, since it has no dates within a year.
    (d) Amend SPLIT-14 below three windows: reopens spanish, nba, open_university and cauca; decide with wisconsin issue 3.
    Recommended: (b).
- **Issue 2:** no precedent; a new tension. An amendment of LEAK-41 should add a Cases row and check frempl and the other siblings for a minimum length.
- **Issue 3:**
  - Keeping the Gini follows australian (D8) and spanish.
  - Switching to the rescaled deviance departs from them. The fact that sets pg16 apart: its original is a market that rescaled uniformly, and its closeness to that market is measured. pg17 scores a Tweedie deviance on its own facts (a game that kept the price level).
  - **Consistency check (AI, 2026-11-06):** if you switch, record that fact. If you keep the Gini, the reason must state the measured shortfall (76 against 44 of 84 two-player markets).

</details>

<details><summary>Claim audit</summary>

**Claim audit: pricing_game_2016_french_fleet (exposure re-review, 2026-11-06, full tier)**

Verdict: today's change (D11) holds on the data. Every number I re-measured reproduces: the target, the weight, the
splits, the metric's implementation, the leak figures and the model scores. I refuted no number. Two findings are new:
(1) the source's 30-day floor selects every row by its realized length, and the newest window most of all, which
LEAK-41 bars and the notes do not connect to it; (2) probe 22's "none above noise" rests on an L2 arm that cannot see
even the weight itself; the Tweedie arm, which I ran, agrees. SPLIT-14 (issue 6) stays open as written.

Scripts (read-only on the repository; definition loaded in memory, no build): audit_facts.py, audit_facts2.py, audit_models.py and audit_p22_tweedie.py in the run folder; the rules PDF from its Wayback copy (id_), read with pypdf.

Model: the builder's regularised LightGBM (Tweedie 1.5, weighted by `exposure`), 3 seeds, scored with
data_foundry.v2.metrics.scorer on the shipped splits.

**Claims table** (claim, source, test, result, evidence, rule)

*Today's changes first (D11).*

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | Target = clipped summed charge / `exposure`; target x exposure gives the charge back | dataset.py _clean, notes | recompute from raw rows via lineage | HOLDS | asserts pass; 537 negative totals clipped (min -1,863.27); clip raises total charge +4.26% | MET-14 |
| 2 | `exposure` is the source's realized Exposition_au_risque = (end-start+1)/365\|366 x vehicles, 0.08 to 1 | notes, scoring column | recompute; range | HOLDS | assert passes; range 0.08-1.00; n_vehicles = 2 on 2 rows | LEAK-41 |
| 3 | `exposure` is never a feature; it is the metric's weight and the sample weight | dataset.py, README | feature_columns(c), sample_weight(c), metric inputs | HOLDS | 16 features, `exposure` not among them; sample_weight = exposure; metric inputs {"weight": "exposure"} | MET-15, LEAK-41 |
| 4 | `exposure_to_year_end` is known at the start and is never below the realized length | notes | compare row by row | HOLDS | exposure <= exposure_to_year_end on 100% of rows; equal on 42.3% (periods that run to 31 Dec); max 1.82 on the 2-vehicle rows | LEAK-7, LEAK-37 |
| 5 | 57.4% of periods end before 31 Dec at an unscheduled cut, 0.8% at an anniversary | notes, scoring column, Decision 1 | share of end != 31 Dec | HOLDS | 58.2% end before 31 Dec (57.8/58.1/58.6% in 2011/12/13) = 57.4% + 0.8% | - |
| 6 | Every window trains on 2011-2012: 56,178 periods (64.4%), 24,674 of 38,538 vehicle-years, all closed by 31 Dec 2012 | splits_comment, CC | splits + raw end dates | HOLDS | train 56,178 (0.644), VY 24,674, total VY 38,538; max training end 2012-12-31; 0 rows in both train and test | SPLIT-14 floor, LEAK-41 |
| 7 | Test windows: 5,312 / 6,509 / 19,229 periods; 987 / 2,218 / 10,659 vehicle-years | splits_comment | count | HOLDS | exact | - |
| 8 | Old expanding sides admitted 11,708 / 5,619 early-ended 2013 periods at 0.127 / 0.131 claims per VY vs 0.115 / 0.116 for those still running; 10.8% / 4.0% of training VY | splits_comment, CC, Decision 2 | recompute | HOLDS | exact | LEAK-41 |
| 9 | Weighted Tweedie LightGBM 0.114 / 0.158 / 0.190 (newest first); weighted constant 0 | notes, metric reason, CHANGES | refit, 3 seeds | HOLDS | 0.110 / 0.157 / 0.189; constant -0.0 on every window | TP-4 |
| 10 | The realized weight as a feature adds 0.013 (5 of 5 seeds) | notes, CHANGES | refit with `exposure` added | HOLDS | +0.012 (seeds: +0.019, +0.007, +0.009; 3 of 3) | LEAK-41 |
| 11 | 1/weight alone scores 0.029 | notes, CHANGES | score 1/exposure | HOLDS | 0.052 / -0.042 / 0.077, mean 0.029. The weight itself scores -0.052 / +0.042 / -0.077, so the "ceiling" sign flips by window: a weak, unstable proxy | LEAK-41 |
| 12 | Ignoring the weight loses 0.010 (SD 0.009, 4 of 5 seeds) | notes, REVIEW 5 | refit unweighted | HOLDS, within noise | +0.005 (seeds -0.002, +0.012, +0.004; 2 of 3). "Little" is right; the sign is not settled at 3-5 seeds | MET-15 |
| 13 | Time features add 0.007 (SD 0.009) | notes | refit without period_start and exposure_to_year_end | HOLDS, indistinguishable from 0 | +0.003 (seeds -0.004, +0.015, -0.002) | USE-6 |
| 14 | Probe 22: weight R^2 0.38 from features, mostly fleet_management and exposure_to_year_end; no feature's gain goes through the weight above noise | notes, CHANGES | read probes; ran the Tweedie arm per feature | HOLDS, BUT THE CITED TEST HAS NO POWER | probe22.txt and probe22_l2.txt are byte-identical, both "objective L2"; in that L2 arm the realized weight itself gains -0.0014 (SD 0.052), so the probe could not have flagged any proxy. Tweedie arm (mine, 3 seeds): weight as a feature +0.0118 (SD 0.0067); mediated share: time features +0.006 (SD 0.014), distribution_channel +0.003 (0.008), client_activity +0.002 (0.010), fleet_management -0.003 (0.012); none above noise | LEAK-41 (report both arms, decide on the worse), EV-1 |
| 15 | fleet_management and exposure_to_year_end are known at the start (USE-6) | notes | check variation and timing | HOLDS (timing not refutable here) | fleet_management varies within 313 of 18,037 contracts, which fits a contract term that changes at a cut; N periods end early 71.3%, P 33.5% (realized/planned 0.57 vs 0.82): risk selection by a contract term | USE-6 |
| 16 | Pooled 2013 scores above the window mean (0.171 vs 0.154) | splits_comment | refit, pool the three test sides | HOLDS | 0.170 vs 0.152 | SPLIT-15 note |
| 17 | Three windows on one training side | splits_comment, REVIEW 6 | read SPLIT-14 | CONFIRMED VIOLATION (already open) | SPLIT-14 (Must): "windows that share one train side ... one evaluation, not several"; the three splits have identical train indices | SPLIT-14, SPLIT-8 |
| 18 | CHANGES.md: option C "0.182 overall, no more optimistic than the valid window" | CHANGES.md | read REVIEW 6 / builder log | WORDING WRONG | 0.182 overall is above 0.171; the "no more optimistic" holds only for its 2013 rows (0.174); REVIEW.md says it right | EV (process) |

*The metric (MET-1, MET-2, MET-3, MET-11, MET-13, MET-15).*

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 19 | The original is the 2014 market: insureds sent at random among the cheapest premiums, premiums scaled uniformly to 2.5 million euros; no other metric named | metric original/reason | read the rules PDF (Sec. 2, 4); one more web search for the game's results | HOLDS | Sec. 4: "agrégateur de prix ... sélection aléatoire parmi les primes les moins chères ... la somme des primes ... égalisée à 2,5 millions d'euros (par un facteur d'inflation appliqué uniformément)". No scoring formula and no published results found | MET-1, MET-11 |
| 20 | stand_in, not source: the market cannot be computed | metric | rules + data | HOLDS | needs other players' premiums and the 2014 claims; test_contrats.csv has no claims | MET-11 |
| 21 | Rules Sec. 2 write 37,772 where the file holds 32,772 | notes | rules PDF | HOLDS | Sec. 2: "37 772 contrats" twice; Sec. 1: "32 772 polices" | - |
| 22 | Implementation = Liberty Mutual's weighted Gini, ties by the mean over orderings | README Metric definition | compare with the Kaggle code on untied predictions; hand case; constant; row permutation | HOLDS | max \|diff\| 1.0e-12 over 15 random predictions; hand case 1.0; constant 0 on every window; permutation-invariant; perfect order 1.0 | MET-13 |
| 23 | The metric reads `exposure` as its row weight and every test fold holds what it reads | scoring column | scorer vs manual weighted vs unweighted | HOLDS | scorer = manual with exposure (-0.01565); unweighted differs (-0.03317); positive charges per window 103 / 232 / 1,026; all weights > 0 | MET-2, MET-15 |
| 24 | Meaning vs the source (MET-2): the game priced each period's total ("prime pure" per contract line; its 2014 file gave the realized end); we score the rate | metric reason, notes | read the rules | HOLDS AS A STATED DEPARTURE | the reason gives MET-15 and LEAK-38 for it; the market compared totals | MET-2, LEAK-38 |
| 25 | A fleet premium is revised pro rata as vehicles come and go ("AMRAE ... not checked") | notes | web search | HOLDS IN GENERAL | a French fleet guide: "La prime est régularisée en fin d'année sur la base du parc réel (pro-rata temporis)"; AXA Belgium separates a "prime régularisable" (flotte globale) from a non-régularisable one (flotte classique), so not every fleet contract is pro rata | MET-15, USE-5 |

*Earlier claims checked again on the new frame.*

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 26 | 87,228 periods, 68,485 vehicles, 18,037 contracts | task summary | count | HOLDS | exact (68,487 contract-vehicle pairs) | - |
| 27 | 95.7% zeros; 4,250 with a claim, 286 with 2+, max 7; 3,711 positive; median 1,339, max 13,992; max rate 75,929 | notes | count | HOLDS | exact | - |
| 28 | No period shorter than 30 days; no start after 2 December | notes (anomaly) | lengths, starts | HOLDS | min length 30; latest December start day 2 | - |
| 29 | 11,807 repeats (10,828 same target, 979 other); no copy crosses the split with period_start | notes, accepted warnings | duplicated(keep="first"); hash match test vs train | HOLDS | 11,807 / 10,828 / 979; 0.0% test rows with a full-feature copy in train on all 3 windows | LEAK-18 |
| 30 | Window rates 0.129 / 0.122 / 0.117 claims per VY; 2.3 / 3.9 / 6.0% with a claim; 123 claims, 103 positive charges in the newest window; charge per VY 180-205 in 2013 vs 167 | splits_comment, notes | recompute | HOLDS | 0.129 / 0.122 / 0.117; 2.3 / 3.9 / 6.0%; 123 / 103; 204.6 / 197.0 / 179.7 vs 167.0 | TP-9 |
| 31 | 76-81% of test periods have their contract in training, 23-26% their vehicle | splits_comment | isin | HOLDS | 76.4 / 77.1 / 81.1%; 22.6 / 24.9 / 26.0% | SPLIT-13 |
| 32 | Claims per VY 0.117 / 0.119 / 0.119 in 2011-2013 | notes | recompute | HOLDS | exact | LEAK-24 |
| 33 | Commonest start 1 January (12,028 in 2013) | splits_comment | count | HOLDS | 12,028 | - |
| 34 | Newest window beats the constant by about 1.7 SE | notes | 0.114 / 0.068 | HOLDS | 1.68 | TP-4 |
| 35 | Implied: the task's rows are not selected by their realized length | (implied by "No training row is now admitted by its realized end" and LEAK-41 cited as holding) | length histogram; gaps between consecutive periods of a vehicle | REFUTED FOR THE SOURCE (see finding 1) | lengths: 0 below 30 days, 909 at 30, 2,074 at 31, about 700 a day at 32-40; 1,558 gaps of 1 to 29 days between a vehicle's consecutive periods, flat at about 45 a day, where dropped short periods would sit | LEAK-41 |

Untested (no new data, or settled and not reopened by today's change): the claim-delay simulation (0.190 -> 0.192 /
0.187; 0.151 / 0.119 when fit once on 1 January); the old-side scores 0.137 / 0.160 / 0.190 and option C's 0.182 /
0.174 (the builder's log shows them, not refit); the GLM 0.159 / 0.171 / 0.200 and the Tweedie-deviance ordering;
the scaling constant 1.077841; CASdatasets' DirectComp mismatch (1,064); the 0.8% anniversary split of claim 5.

**Refuted and untested, ranked (validity first, Must first)**

1. P4 / LEAK-41 (Must): the source selected every row by its realized length, the newest window most of all. (New.)
   Test: period lengths stop at 30 days with no taper (0 rows at 29 days, 909 at 30, about 700 a day at 32-40). A
   vehicle's consecutive periods leave 1,558 gaps of 1 to 29 days, flat at about 45 a day. Both fit a filter that
   removed the periods shorter than 30 days. Extrapolating the 30-39 day density down to day 1 (rough, and it assumes
   a flat density), the filter removed about 2,800 periods from the Sep-Dec window (about 35% of its would-be periods,
   about 11% of its vehicle-years), about 1,800 from May-Aug (22%, 3%) and about 4,200 from Jan-Apr (18%, 1.6%).
   Every period that would have started after 2 December is gone.
   What it changes: LEAK-41 bars training or scoring "on rows selected by the realized weight". The definition
   honours that for its own choices: no row is admitted by its early end. The data was selected before we got it,
   though, and the selection is uneven across windows: the newest window's test rows are the periods that survived 30
   days from a late start. The claims of the removed periods are also missing, so no one can say how the selection
   moves the rate. The anomaly note ("the task covers periods of a month or more") states it but does not cite
   LEAK-41, does not size it per window, and is not mentioned in issue 6, where the newest window's weight is
   debated.
   Mildest remedy: no fix in the data is possible. Add one sentence to the anomaly note: the source's selection by the
   realized length (LEAK-41, a property of the release), with the gap and histogram evidence and the per-window
   estimate. Add one line to issue 6: the newest window is the noisiest and also the most selected, which counts for
   options B and C. The "fit direct" stays.

2. P4 / SPLIT-14 (Must): three windows on one training side count as one evaluation. Confirmed, already open (issue
   6). The three splits have identical training indices (56,178 rows). Nothing new; the split auditor and the judge
   have it.

3. EV-1 / LEAK-41 (Must on the reporting): probe 22 had no power. probe22.txt and probe22_l2.txt are the same file,
   both from the L2 arm. In that arm the realized weight, the leak itself, gains -0.0014 (SD 0.052), so "no feature
   above noise" could not have come out otherwise. LEAK-41 asks for the L2 arm and the weighted actuarial arm and a
   decision on the worse. I ran the Tweedie arm (3 seeds): the weight as a feature +0.0118 (SD 0.0067); weight-mediated
   gains of the time features +0.006 (SD 0.014), fleet_management -0.003 (0.012), distribution_channel +0.003 (0.008),
   client_activity +0.002 (0.010). The conclusion stands; the evidence the notes cite does not carry it.
   Mildest remedy: cite the Tweedie arm's numbers in the probe 22 sentence (notes and REVIEW 5), and re-run probe 22
   with the actuarial objective, so the two output files differ.

4. Quality / wording: two effects are stated with more certainty than the seeds give. "A fit that ignores the weight
   loses 0.010 (SD 0.009, 4 of 5 seeds)": my 3 seeds give +0.005 (2 of 3). "The time features add 0.007 (SD 0.009)":
   mine give +0.003. Both are within noise. The notes' "little" is right, but these numbers should not be used as a
   finding that the weight or the time features matter on this metric. Remedy: none needed beyond "within seed noise"
   where they are quoted.

5. Process: CHANGES.md says option C scores "0.182 overall, no more optimistic than the valid window". 0.182 is above
   0.171; it is the 2013 rows (0.174) that are no more optimistic. REVIEW.md issue 6 states it correctly. Remedy:
   reword CHANGES.md if it is reused.

6. Untested, low stakes: the pro-rata premium that MET-15's weighting rests on ("AMRAE ... not checked"). French fleet
   practice regularises the premium pro rata temporis on the real fleet, but AXA Belgium's terms keep some fleet
   premiums non-régularisable (flotte classique). The general claim holds, so the weighting stands; the notes could
   cite a checked source in place of "not checked".

**Sources consulted on the web:**
- Rules PDF (Wayback): http://web.archive.org/web/20210422004748/https://freakonometrics.hypotheses.org/files/2016/08/pricing-game-2016-FR.pdf
- https://www.r-bloggers.com/pricing-game/ (search result; no results or scoring published)
- https://www.echangesassurances.org/assurance-pro/protection-biens-locaux/assurance-flotte-automobile-entreprise/
- https://axa.be/axa-documents/ibp/000039-4186051-20190601.pdf
- https://www.amrae.fr/flottes-automobiles-lauto-assurance-opportunite-ou-risque-pour-votre-entreprise

</details>

<details><summary>Column audit</summary>

**Column audit: pricing_game_2016_french_fleet (exposure re-review, 2026-11-06, full tier)**

Verdict: ship. No feature is set or cut after the prediction point; `exposure` is the weight scoring column and the
sample weight only (feature_columns() has 16 features, `exposure` not among them). One new P4 question under LEAK-41's
last clause (the source's 30-day floor selects rows by their realized length), and one open P7 typing gap (four band
columns are unordered categories).

Frame: the definition of D11 (branch zi-datasets), 87,228 rows, 18 columns (16 features, weight, target); raw files train_contrats.csv / train_sinistres.csv from the warehouse. Codebook: the rules PDF Sec. 1 (as quoted in RENAME and REVIEW.md). Dtype probe: 8 of 15 flagged.

Prediction point (first curation_comments bullet): the start of a vehicle's period of cover, priced with the year's
tariff fit on the closed years.

**Column table**

| Column | Meaning | Known at prediction? | Dtype and cleaning | Verdict | Rule |
|---|---|---|---|---|---|
| period_start | "Date de début de situation" | yes, it is the prediction point | datetime; temporal key | fine | CLEAN-14 |
| contract_age_class | "Classe age du contrat", bands of contract age | yes: a period value, steps up with time (of 6,029 contracts in 2011 and 2013, every one moves up or stays at "> 5 ans") | category, UNORDERED, lexical level order ['1 - 2 ans', ..., '<= 1 ans', '> 5 ans']; probe: ordinal_like, open_end | cleaning problem: bands with an open end are an ordered category, lowest first | CLEAN-14 (Should) |
| new_company | "Indicateur de création entreprise (à 2 si création)" | yes; constant per contract (0 contracts vary): a subscription attribute | category No/Yes from 1/2 | fine | CLEAN-12 |
| fleet_management | "Mode de gestion de la flotte", N/P, meaning not stated | yes: a contract term recorded per period (242 changes between consecutive periods of a vehicle, 28 of them next-day, so not an extract snapshot) | category N/P | fine; probe 22's top feature (49% of gain), judged below | USE-6, LEAK-41 |
| zone | "Zone géographique", anonymised 1-6 | yes | category of codes | fine (probe numeric_levels: a code with no words stays a category) | CLEAN-12, CLEAN-14 |
| fleet_size_class | "Taille de la flotte", anonymised 1/2 | yes | category of codes | fine; which code is the larger fleet is not documented, two levels so no order question in practice | CLEAN-14 |
| payment_frequency | "Fractionnement de paiement de la prime" | yes; constant per contract | category annual / semi-annual / quarterly from A/S/T | fine; optional: an order by instalments exists (1, 2, 4 a year) | CLEAN-12 (nit) |
| exposure | "Véhicules année (exposition au risque)", realized vehicle-years, 0.08 to 1.00 | NO for 58.2% of periods (end before 31 Dec) | float; weight scoring column + sample_weight, never a feature; values = (end-start+1)/365 (366 in 2012) x n_vehicles rounded to 0.01 (asserted); never above exposure_to_year_end (0 rows) | fine as the weight (MET-14, MET-15, LEAK-41); nit on the rounding below | LEAK-41 |
| vehicle_age_class | "Classe d'âge du véhicule", '<= 5 ans' / '> 5 ans' | yes: a period value (1.9% of vehicles move up) | category, unordered; probe: open_end | cleaning nit: two-level band, ordered by the rule; no effect on models | CLEAN-14 (Should) |
| deductible_class | "Classe de franchise de la garantie DTA", '1. 0' ... '6. > 600' | yes, changes only at a cut | category, UNORDERED (cat.ordered False; the lexical order happens to match the bands). The 2026-11-01 column audit's "6 ordered labels" is wrong for the shipped dtype | cleaning problem: bands of an amount, open end | CLEAN-14 (Should) |
| n_vehicles | "Nombre de véhicule" | yes | int; 1 on 87,226 rows, 2 on 2 | fine (settled D4) | CLEAN-5 |
| insured_value_class | "Valeur assurée", bands '<= 7.6K' ... '137K - 380K' | yes; non-ND rows spread over 2011/2012/2013 (40/44/51), so ND is no time artefact | category, UNORDERED; "ND" made missing (87,093) | cleaning problem (tiny: 135 rows): bands of a value, ordered category | CLEAN-10 ok; CLEAN-14 (Should) |
| formula | "Formule souscrite", anonymised 2-5 | yes (changes at cuts) | category of codes | fine | CLEAN-14 |
| client_activity | "Activité du client (niveau contrat)", anonymised 1-8 | yes | category of codes | fine | CLEAN-14 |
| distribution_channel | "Type d'apporteur (agents ou courtiers ou autres)", 1-3, map not published | yes; constant per contract | category of codes | fine | CLEAN-14 |
| power_value_class | "Combiné puissance valeur du véhicule", 1-11 | yes; constant per vehicle (99.9%) | category; a combined power x value grid, no documented order | fine (a grid of two dimensions is no single line; keep unordered with the note it has) | CLEAN-14 |
| exposure_to_year_end | our build: (31 Dec - start + 1)/365 (366 in 2012) x n_vehicles, rounded 0.01; 0.08 to 1.82 | yes, a function of the start and the vehicle count | float | fine; probe 22's second feature (38%), judged below | LEAK-7, LEAK-37, CLEAN-19 |
| claim_charge_per_vehicle_year (target) | period's summed CHARGE_SINISTRE, net negatives to 0, / exposure | outcome | float, identity scale, 0 on 95.7% | fine (MET-14; CLEAN-16 as amended: Gini, scale stated) | MET-14, CLEAN-16 |
| dropped: contract_id, vehicle_id, year, period_end, vehicle_category, claim_count, claim_total and the join columns, row index | ids (subscription order), copy of start's year, realized end, constant, parts of the target | - | dropped | fine (settled) | CLEAN-3, CLEAN-5, LEAK-10, LEAK-41 |

**Probe 22: the features that predict the weight, judged by timing (LEAK-41)**

Weight from the features: R^2 0.378 (SD 0.15), Spearman 0.589. The weight as a feature gains -0.001 (SD 0.052) on the
probe's L2 fit; 1/weight alone 0.029 against the honest 0.113. No feature's weight-mediated gain is above noise.
- fleet_management (49%): N periods end early in 71.3% of cases against 33.5% for P (N: 1.13 periods per vehicle-year,
  P: 1.03 in each year). It is a contract term known at the start and recorded per period (it changes between
  consecutive periods 242 times), not a value written at the realized end. Risk selection / administration mode:
  stays (USE-6; LEAK-41's "a feature known at the prediction point that predicts the weight through risk selection
  stays"). Weight-mediated -0.013 (SD 0.053).
- exposure_to_year_end (38%): a deterministic function of the start and n_vehicles; the start-known part of the
  weight that LEAK-41 asks to ship as its own column. Stays (LEAK-7, LEAK-37). Weight-mediated -0.017 (SD 0.055).
- fleet_size_class, distribution_channel, client_activity (2% each): contract classes, constant or changing only at
  cuts; known at the start. Stay. Weight-mediated +0.013, +0.030, +0.046, each under 1 SD.
No column encodes the realized length: exposure_to_year_end never falls below exposure; no group sum of exposures;
the rounding precision of exposure_to_year_end is uniform (0.01 on every row) and does not mark the cut.

**Problems ranked (principles.md)**

1. P4, LEAK-41 (Must), last clause, NEW under today's rule: the source's rows are selected by their realized length.
   Question for the curator.
   Evidence: no period is shorter than 30 days in either file, with a sharp edge, not a taper: early-ended periods
   starting Jan-Sep number 717 at 30 days, 1,434 at 31, 565 at 32, 471 a day on average over 30-59 days against 288 over
   60-89 and 259 over 90-119, so the density rises toward the cut. Extrapolating at least 470 a day below 30 days, the
   organisers left out roughly 13,000 or more periods (some 15% of the rows), but at most about 0.04 vehicle-years each,
   about 500-600 vehicle-years in all, near 1.5% of the 38,538. Short periods claim more per vehicle-year (early ends of
   30-44 days 0.143, 45-59 days 0.160, against 0.124 at 180+ days), so the left-out ones likely do too. The same floor
   explains "no period starts after 2 December": a period that starts 2 Nov to 2 Dec is in the file only if it ran 30
   days (4,251 such periods in 2011-2013). LEAK-41: "No model is trained or scored on rows selected by the realized
   weight." Here the selection is the organisers', the same in train and test (and in the game's 2014 file), and
   cannot be undone: the cut periods and their claims are not published. The curation notes it as an "anomaly"
   (bullet "no period is shorter than 30 days"), which today's rule makes a LEAK-41 matter, not a provenance remark.
   Strength: weak by weight (about 1.5% of vehicle-years, so the weighted Gini and the weighted fit barely see it),
   large by rows; no train/test asymmetry.
   Mildest remedy: keep, and rewrite the anomaly bullet as a LEAK-41 note (the source's selection by realized length,
   not removable, the estimate above, the population is "periods that last a month or more", which the insurer cannot
   know at the start); the curator records it as an exception to LEAK-41's last clause or accepts it as the source's
   population (USE-7). No definition change can fix it. The same check applies to frempl and the other family members
   with a minimum length.

2. P7, CLEAN-14 (Should): four band columns ship as unordered categories.
   Evidence: dtype probe flags contract_age_class (ordinal_like, open_end), insured_value_class (ordinal_like,
   open_end), vehicle_age_class (open_end); deductible_class is the same kind (bands of an amount with "> 600") and
   ships cat.ordered False. CLEAN-14 (amended 2026-10-30, "going forward for all relevant datasets"; open ends
   2026-11-01): bands of a quantity, the cut end a level of its own, are an ordered category lowest first. Raised by
   the blind reviewer on 2026-11-01 (REVIEW.md, "Unordered age classes") and not acted on; the 2026-11-01 column table
   called deductible_class ordered, which the shipped dtype is not.
   Remedy: FeatureTypes(categorical=[the rest], ordinal={
     "contract_age_class": ["<= 1 ans", "1 - 2 ans", "2 - 3 ans", "3 - 4 ans", "4 - 5 ans", "> 5 ans"],
     "vehicle_age_class": ["<= 5 ans", "> 5 ans"],
     "deductible_class": ["1. 0", "2. 1 - 200", "3. 201 - 300", "4. 301 - 400", "5. 401 - 600", "6. > 600"],
     "insured_value_class": ["<= 7.6K", "7.6K - 38K", "38K - 76K", "76K - 137K", "137K - 380K"]},
   datetime=["period_start"]), and the Dtypes bullet updated. Unknowns are already missing (ND). Optional:
   payment_frequency ordered annual < semi-annual < quarterly. Cheap and safe; a rebuild is the curator's call.

3. P7, nit: the weight is the source's value rounded to 0.01. Relative error up to 5.8% on 30-day periods, above 2% on
   16.1% of periods. The exact vehicle-years from the dates are already computed in _clean (`realized` before
   .round(2)). Effect on the task is nil in practice: weight x target equals the charge either way, so the weighted
   Gini's numerator and the weighted fit's loss terms move only by the weight sums. Keep with the source's value (it
   is the documented column); no action needed, or note it in the Exposure bullet.

4. P3/P7 wording: "a cut nobody scheduled". 25.9% of the early ends fall on a month's last day and 14.5% on the last
   day of March, June or September; lengths of 31 and 59-60 days spike (1,434 and 758/545 against about 450 a day
   around them), and 53.7% of periods start on the 1st. Some cuts follow monthly or quarterly administration. None of
   this is known at the start for a given vehicle, so the weight treatment stands; the phrase overstates. Remedy: "at a
   cut not known at the start, a quarter of them on a month's end".

**Not problems (checked):**

- Every feature is known at the period's start; the rating classes are period values, not extract snapshots
  (contract_age_class steps up across years; vehicle_age_class moves for 1.9% of vehicles; fleet_management changes
  between consecutive periods).
- No missingness caused by the outcome: insured_value_class is the only column with missing values (ND), spread
  evenly over the years, 5 claims among its 135 known rows.
- The target is not given away by any feature (leak probe: every feature alone at R^2 0.001 or below).
- Issue 6 (shared training side) is the split auditor's; nothing in the columns bears on it.

</details>

<details><summary>Split audit</summary>

**Split audit: pricing_game_2016_french_fleet (exposure re-review, 2026-11-06, full tier)**

Scope: REVIEW.md issue 6 (three windows on one training side). Read: dataset.py, REVIEW.md, CHANGES.md, the run's
measure_shipped.py and out_shipped/alternatives.csv, splits.md (SPLIT-8/9/10/11/14 and Cases), leak_checks.md
(LEAK-12, LEAK-41), principles.md. Own run: audit.py -> paired.csv, in the run folder.


**Verdict:** the split as implemented (option A) is WRONG under the rules as written: it breaks SPLIT-14 (Must), which
has no exceptions. The rules support option C, the forced split grouped by contract (SPLIT-8). A or B are open only
as an amendment of SPLIT-14, a deliberate change the curator (and Andrej, who wrote the clause on this very dataset)
would have to make.

1. Why A fails (P4, SPLIT-14 Must)
   - SPLIT-14 as amended 2026-11-02 / reframed 2026-11-05: "Each window has its own train side: windows that share
     one train side test one model on several test periods, which is one evaluation, not several ... each window
     trains on what is known before it starts." The shipped splits: all three windows train on the same 56,178 rows
     (64.4%); checked on the container (train share 0.644 for windows 0, 1, 2). Its own Cases row was written for this
     dataset in exactly this configuration ("three four-month windows of 2013 that all trained on 2011-2012 do not
     count as three windows").
   - So A is one window counted three times: the newest window (103 positive charges, bootstrap SE 0.068) gets a third
     of the weight; the mean of the windows (0.154) is one model on three start cohorts, below the pooled 2013 score
     of the same model (0.171).
   - Does LEAK-41 (Part 3, outranks Part 4) override SPLIT-14 here? No. Rank settles a conflict only where meeting one
     rule means breaking the other (principles.md, How to decide 4: independent failures are not conflicts). SPLIT-8
     (Must, narrows SPLIT-14) gives a regime that meets both LEAK-41 and SPLIT-14: ship forced. The REVIEW footnote
     [^forced] says the same; I agree.
   - "A Must has no exceptions: only a higher-ranked Must overrides it, and anything else is an amendment"
     (principles.md). A therefore needs SPLIT-14 amended; it cannot ride on an exception or on D11's wording.

2. Why D fails (P4, LEAK-41 Must, Part 3)
   - LEAK-41: "No model is trained or scored on rows selected by the realized weight". The expanding sides admitted
     the 2013 periods closed before the window, i.e. selected by their early end (realized exposure): 0.127 / 0.131
     claims per vehicle-year against 0.115 / 0.116 for the 2013 periods left out (REVIEW issue 5). Excluded; SPLIT-11
     (Should) cannot outrank it.

3. Is SPLIT-8 really triggered (no rule-conforming three windows)? Yes; I checked the alternatives the issue does not
   list.
   - Windows across years: 2012 on 2011 trains on 30.4% of the rows, below SPLIT-14's floor; only 2013 on 2011-2012 is
     valid. One valid window = "too few periods for three windows" in SPLIT-8.
   - Admitting every 2013 period started before a window, whatever its end (no selection, so LEAK-41 holds): its
     final label holds claims after the window's start, including the test months themselves, so it is not "what is
     known before it starts" (SPLIT-14's own last sentence, and SPLIT-10); claims carry no dates, so it cannot be cut
     at the window start; and a fleet's own later labels would reach its test periods (SPLIT-9, Must; 79% of 2013 test
     rows have their contract in training). Not a valid route; I did not fit it.
   - So no training rule meets LEAK-41, SPLIT-9 and SPLIT-14 together on this release; the REVIEW's claim holds.

4. Is C a sound forced split? Yes, with the SPLIT-8 checks still to run.
   - True group id: Num_contrat, the source's contract key (not a cluster or hash). 18,037 contracts; vehicles nest in
     contracts (1 of 68,485 vehicles appears under two contracts); largest contract 81 rows (0.09% of rows, 0.05% of
     vehicle-years); contracts present in 1 / 2 / 3 years: 7,280 / 6,064 / 4,693, so entities recur across the
     stacked years, which is SPLIT-8's condition for ForcedGroupedFromTemporal rather than ForcedIIDFromTemporal.
   - Grouping by contract (not by vehicle) keeps a fleet's later labels away from its earlier rows (the SPLIT-9
     own-entity link) and keeps the 13.5% within-fleet feature copies on one side.
   - LEAK-41 under C: every period of 2011-2013 is admitted, none by its realized end. Holds.
   - Cost against the valid window (SPLIT-8 asks for it), re-run PAIRED, which the issue's comparison was not
     (0.174 on each fold's 2013 rows against 0.171 on all of 2013 compares different test sets). Regularised Tweedie
     LightGBM fitted with the weight (the run's REG params), declared scorer, 3 repeats x 3 folds grouped by contract;
     on each fold's 2013 test rows (10,022-10,658):
     ```text
       valid window model (trained on all 2011-2012):            0.169 (SD 0.044 over 9 folds)
       forced model (the fold's training side, all years):       0.174 (SD 0.029)   difference +0.005 (SD 0.022)
       valid window without the test fleets' history (new fleet): -0.004 (SD 0.013) against the valid window
       forced model on its whole test fold (all years):          0.182, as reported
     ```
     The forced split is no more optimistic on 2013 than the valid window beyond noise (+0.005, SE about 0.007); the
     cold start of a new fleet costs about 0.004, consistent with the record's finding that a fleet's previous-year
     history adds nothing (0.667 vs 0.668 ROC AUC). The higher overall 0.182 against A's 0.154 is mostly pooling: a
     fold ranks all start cohorts together, as the pooled 2013 window does (0.171).
   - Still required by SPLIT-8 before C ships: the leak test across the split and the leak probes on the grouped
     split (no probes/group.txt exists for this dataset yet); the ForcedGroupedFromTemporal tag; contract_id kept as
     the group column, never a feature; temporal removed, the SPLIT-10 exception dropped; splits_comment saying what
     the dates would change (the tariff prices known fleets, USE-10/SPLIT-13: the cold start costs ~0.004 here).

5. B (one window)
   - Breaks SPLIT-14's "at least 3 windows" just as A breaks its own-train-side clause: an amendment all the same. B
     is honest about what A measures (one evaluation, 0.171), and it is C's yardstick under SPLIT-8, not a shipping
     option under the current rules.

6. Consistency (principles.md, Consistent judgement)
   - C follows the three siblings shipped forced grouped with one valid window (pricing_game_2017_french_mtpl,
     frempl_french_motor_personal_line, spanish_motor_insurance_coverage_level_2022_2024) and SPLIT-8's
     nba/open_university precedent (grouped by a recorded entity).
   - A with the amendment the REVIEW drafts ("windows may share a training side when the data's annual cut leaves no
     training side free of a selection by the outcome") would not reopen the siblings (none has a valid window above
     the floor with daily dates), but it reverses the substance of Andrej's 2026-11-02 call on this dataset ("Given one
     test period we test the same model"). That is a deliberate rule change for both curators, not a consistency fix.


**Ranked problems (by principles.md)**

- P4 / SPLIT-14 (Must): three windows on one training side = one evaluation counted three times. Evidence: identical
  train index sets (0.644 each); per-window mean 0.154 vs pooled 0.171. Mildest remedy: re-split as SPLIT-8
  prescribes (C, grouped 3x3 by contract, ForcedGroupedFromTemporal). Alternative only by amendment (A or B).
- P4 / SPLIT-8 (Must, procedural, for C): leak test across the grouped split and leak probes not yet run. Remedy: run
  them before shipping C.
- P4 / evidence (EV): the issue's C-vs-valid number (0.174 vs 0.171) is unpaired; replace with the paired +0.005
  (SD 0.022, 9 folds) and the cold-start cost -0.004 above.
- Housekeeping: splits.md Cases row "SPLIT-14 ... pricing_game_2016_french_fleet" still describes the expanding
  windows with kind "applied"; replace it with the outcome of issue 6.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner: pricing_game_2016_french_fleet (exposure re-review, 2026-11-06, full tier)**

Actor: the pricing actuary of a French insurer who sets the a priori material-damage (DTA) tariff per vehicle for small
commercial fleets. Once a year I set the rate per vehicle-year by rating cell, fitting it on the closed years. The
premium is that rate times the time each vehicle stays in the fleet, settled pro rata as vehicles come in and go out.
Scope: what D11 changed (the target is now a rate, `exposure` is the weight, training is on 2011-2012), issue 6, and
the metric. What earlier panels settled (the `exposure` fix of 2026-11-02, IDA, the claim wording) is not repeated.
My probes: probe.py, probe2.py and the cohort table, with their outputs, in the run folder. They run
on the shipped windows. The models are a weighted Tweedie GLM (one-hot, alpha 1e-3) and a weighted Tweedie LightGBM
(15 leaves, 300 rounds at 0.03, min_child_samples 200, lambda 5, mean of 3 seeds). The day of the year of
`period_start` is the date's encoding.

**Verdict**

- Fit: direct (USE-8, agree with fit="direct"). Each row is a vehicle-period I rate at its start, and the inputs are
  the rating classes I hold then. The target is the pure premium per vehicle-year that my tariff charges, weighted by
  the vehicle-years it is earned over. The test year 2013 follows the closed years 2011-2012, on the fleets I already
  insure.
- Metric: partly. The weighted Gini scores the order of my risks. The game's uniform rescaling removed the price level,
  so that is the right core. The game's market sent each insured to the cheapest premium, though, so it also rewarded
  how far apart the prices are (the spread of the relativities), and the Gini cannot see that spread. Measured below.
  As context, or as the stand-in if the curator accepts its noise, I would choose the exposure-weighted Tweedie
  deviance (p = 1.5) after the game's own uniform rescaling to the window's total.

**1. DO I HAVE THESE INPUTS WHEN A VEHICLE'S PERIOD STARTS? (USE-3, USE-6, LEAK-41)**

- Rating classes (contract age, activity, zone, fleet size and management, new-company flag, channel, payment
  frequency, formula, deductible, insured value, vehicle age, power-value): yes. All are on the contract or on the
  vehicle's declaration when the period opens.
- period_start and exposure_to_year_end: yes. Both are fixed by the start (LEAK-7, LEAK-37). For a rate target they are
  not exposure. They carry the season and the cohort a period falls in, a legitimate rating fact at the start.
- exposure (realized vehicle-years): I would not have it, and I do not need it as an input. I need it to earn the
  premium, and it does exactly that as the weight of training and scoring, never a feature (MET-15, LEAK-41). This is
  how a fleet book is billed: a provisional premium, then pro-rata regularisation for vehicles added and removed
  (City Drop's fleet conditions, AXA Belgium's regularisable fleet premium, Matmut's duty to declare additions and
  removals). D11 matches practice.
- Inputs I would always have that are missing (unchanged from the first panel; disclosure control, cannot be fixed):
  - the fleet's own loss ratio over 3 years: the builder measured it to add nothing here;
  - the current tariff's premium, which I would refine (USE-6);
  - finer vehicle data (make/SRA group, use).
  None of these changes the task.

**2. IS THE TARGET WHAT I ACT ON? (USE-5, MET-14)**

- Yes. The claim charge per vehicle-year is the pure premium rate I put in the tariff. I want a number, the expected
  charge per vehicle-year by cell. The weighted fit estimates E[charge | x] / E[vehicle-years | x], the rate that
  breaks even when the premium is earned pro rata. Under D11 this is the quantity I act on. Before, the charge per
  period mixed my rate with a guess of how long the vehicle stays, which I never price.
- One nuance, an inference I have not checked against these contracts: when a covered claim ends a vehicle's cover (a
  total loss), French insurers often keep the rest of the premium. Code des assurances L121-9 refunds the unexpired
  premium only when the loss comes from an event the policy does not cover. If so, the premium earned on claim-ended
  periods is larger than their realized vehicle-years, and the break-even rate per realized vehicle-year slightly
  overstates the rate I need. Early ends claim 1.22 times as often given the classes, so the effect is second order.
  A note in the curation_comments would cover it, with no change to the data.

**3. DOES ONE ROW MATCH ONE DECISION? IS THE TEST WHAT I WOULD FACE? (USE-10, SPLIT-13)**

- Row: one vehicle over one period with unchanged terms is the unit my tariff rates. Yes.
- Training only on the periods that started before 2013: yes, that is my practice. The 2013 tariff is fitted once on
  the closed years and applied to every period that opens in 2013. I would never refit in May on the 2013 vehicles
  that had already left. They are a selection by outcome: 0.127 and 0.131 claims per vehicle-year against 0.115 and
  0.116 for those still running. The new training side is the honest one. In practice I fit in autumn 2012 on claims
  not yet developed. Here the labels are developed to the 2014 extract, a small optimism the notes already simulate.
- Issue 6 (open), from practice:
  - My decision is one tariff for the year, judged on the whole 2013 book, weighted by vehicle-years.
  - Option B (one window over 2013, 0.171) and option A (three windows on one training side) both test that tariff.
  - Option C (grouped by contract over 2011-2013) tests fleets I have never insured, with years mixed. My tariff
    prices known fleets (76-81% of the test periods are on contracts already in training). On fidelity to the use
    case: B > A > C.
  - A's three equal thirds overweight a small and unstable cohort. The Sep-Dec window holds 987 of 13,864 test
    vehicle-years (7%) and 103 positive charges, yet counts a third.
  - Its level jumps: the charge per vehicle-year by start cohort (2011 / 2012 / 2013) is 141.9 / 159.1 / 204.6 for
    Sep-Dec, against 157.3 / 172.5 / 179.7 for Jan-Apr and 178.3 / 185.7 / 197.0 for May-Aug.
  - The amendment or the forced split is the curator's call under SPLIT-14 and SPLIT-8. My point is that C moves the
    task away from the decision (USE-10). A or B keeps it.

**4. WOULD I USE THIS MODEL? WHAT WOULD MAKE ME TRUST OR DISTRUST IT?**

- I would use a model trained this way as the a priori tariff for small fleets if:
  - (a) it balances overall and by segment;
  - (b) its relativities are neither steeper nor flatter than the data supports, checked by actual over expected by
    predicted quintile;
  - (c) it beats the current tariff on a double-lift chart.
- What makes me distrust the tree model as specified: its relativities are too steep. Actual over expected by
  predicted quintile, lowest to highest, after rescaling each window's predictions to the window total:
  ```text
    Sep-Dec  1.98 1.47 1.06 1.25 0.49
    May-Aug  1.88 1.03 1.14 0.90 0.79
    Jan-Apr  1.39 1.23 1.03 0.90 0.88
  ```
  It prices its cheapest fifth at about half the cost and its dearest at about twice. In a cheapest-wins market I
  would win the risks I underprice. It still scores a weighted Gini of 0.157 (window mean), close to the GLM's 0.173.
- Level: every model trained on 2011-2012 (167 per vehicle-year) underprices 2013 (180-205). The constant's actual
  over expected is 1.08 / 1.18 / 1.23 (newest last). That is trend, which I would load separately. The game's uniform
  rescaling took it away, and so does the Gini.

**5. DOES THE DECLARED METRIC SCORE MY DECISION? (MET-1, MET-6 to MET-9, MET-14, MET-15)**

- Unit and weight: right. Each period counts by its vehicle-years, the unit I earn premium on (MET-15). No threshold
  or cost is fixed (MET-6, MET-7) and no top k is followed up (MET-9), so a ranking or a proper score is the right
  family (MET-8).
- What the Gini misses, measured (window means; lower deviance is better):
  ```text
    model                                     w. Gini   w. Tweedie dev   same, rescaled to window total
    constant (training rate)                  0.000     91.17            90.82
    Tweedie GLM                               0.173     89.92            89.63
    GLM, relativities halved (x^0.5)          0.173     90.04            89.58
    GLM, relativities doubled (x^2)           0.173     93.66            94.27
    Tweedie LightGBM                          0.157     95.06            91.34
  ```
  - The Gini gives the same score to a tariff and to the same tariff with its relativities doubled.
  - The rescaled deviance ranks the doubled tariff and the LightGBM below a flat tariff, which is what the game's
    market would have done to them.
  - Raw deviance mixes in the drift of the level. Rescaling uniformly, as the game did ("un facteur d'inflation
    appliqué uniformément"), removes it.
- The metric I would choose: the exposure-weighted Tweedie deviance of the rate (p = 1.5, MET-14's compound-Poisson
  weighting), after multiplying each model's predictions by one factor so that its premium total equals the window's
  claim total. Why:
  - it is a strictly proper score of the relative prices (MET-8);
  - it is level-free as the game was (MET-11, closest to the original);
  - it sees the spread that a cheapest-wins market prices.
- Costs: it uses the test total, an oracle scale, just as the game fixed its total at 2.5 million euros. It is noisier
  than the Gini on the newest window, and it would be a new library metric (MET-13).
- If the curator keeps the Gini as the stand-in, the reason should stop saying the market "rewarded the ranking of the
  risks" alone. It rewarded the relative prices, of which the ranking is the part the Gini scores.

**Gaps between the dataset and my decision, ranked by how much they change the task**

1. The metric cannot see the spread of the relativities, which a cheapest-wins market rewards (above). It changes
   which models win: the GLM over a steep tree model by deviance, nearly tied by the Gini.
2. Issue 6: the three equal-weight windows overweight a 7% cohort whose level jumped. Option C would test unseen fleets
   on mixed years, against USE-10.
3. Labels developed to the 2014 extract, where a real 2013 tariff sees immature 2012 claims (noted and simulated).
4. Missing in practice: fleet experience, the current premium, finer vehicle data (disclosure control; no effect
   measured).
5. Possible premium kept after covered total losses, which would bias the per-realized-vehicle-year rate slightly
   upward (inference; a note only).

**What an expert would change**

- Score with the uniformly rescaled weighted Tweedie deviance (or ship it as context), or at least reword the stand-in
  reason.
- Prefer one 2013 window or the three on one training side over the grouped split.
- Add a line on trend (the training rate 167 against 180-205 in 2013) and on the cohort level jump.
- Optionally, note the total-loss earning convention.

**Sources**

- The definition and REVIEW.md (issues 5, 6; the first panel's practitioner block) in
  `datasets/_dev/tabarena-v0pt2/pricing_game_2016_french_fleet/`
- Game rules: http://web.archive.org/web/20210422004748/https://freakonometrics.hypotheses.org/files/2016/08/pricing-game-2016-FR.pdf
  (Sec. 4, the market and its uniform factor), as quoted in the definition.
- Fleet billing: https://www.city-drop.com/files/conditions-particulieres-assurance.pdf (provisional premium,
  pro-rata for vehicle movements); https://www.axa.be/axa-documents/ibp/000039-4186051-20200601.pdf (regularisable
  fleet premium); https://www.matmut.fr/services-en-ligne/doc/IPID/IPIDMRSQFLOTTE.pdf (declaring additions and
  removals); https://www.amrae.fr/flottes-automobiles-lauto-assurance-opportunite-ou-risque-pour-votre-entreprise
- Code des assurances L121-9 (refund after a loss from an uncovered event): from memory, not fetched.
- Rules: use_case.md USE-3, USE-5, USE-6, USE-8, USE-10; metrics.md MET-1, MET-6 to MET-9, MET-11, MET-13 to MET-15;
  leak_checks.md LEAK-7, LEAK-37, LEAK-41; splits SPLIT-8, SPLIT-13, SPLIT-14.
- Probes: probe.py, probe.out, probe2.py, probe2.out and cohorts.out, in the run folder.

</details>

<details><summary>Blind review</summary>

**Blind review: pricing_game_2016_french_fleet (target claim_charge_per_vehicle_year, regression, exposure as weight)**

**Verdict:** Include with changes. This is a real motor-insurance pure-premium task with an honest temporal split and the right use of the exposure weight. It needs nominal codes recast as categories, near-empty or constant columns dropped, the negative-charge clipping documented, and a deviance-type score instead of (R)MSE.

**What the task is**

Source: 2016 Pricing Game of the French Institute of Actuaries (train_contrats + train_sinistres; CASdatasets pg16trainpol/pg16trainclaim).
Each row is one "situation" (a coverage spell of one vehicle in a fleet or business policy, within one calendar year, 2011-2013).
The target is the claim charge per vehicle-year for material damage. The organisers' brief: "Le but est de proposer une prime pure" (the goal is to propose a pure premium).
Who would use it, when, and for what: an insurer pricing or renewing a commercial motor policy at the start of the period. The decision is the premium. This is a real, standard actuarial use.

**How I verified it**

I downloaded the CASdatasets .rda files and rebuilt the target from them:
 - Joining the claims on (PolicyID, LicNb, BeginDate, EndDate) matches all 4,568 claims, which equals sum(ClaimNb).
 - target = max(0, sum of ClaimCharge in the row) / Exposure reproduces the prepared total exactly (6,675,926.40).
 - `exposure` is identical in distribution to the CASdatasets Exposure ((EndDate - BeginDate)/365, range 0.08-1.00, mean 0.4418).
 - Every categorical column maps one-to-one to a source column with identical counts (e.g. Area A3 = 32,071 = zone 3).
The data is real, not generated, and the target is what it claims to be.

**The training weight (`exposure`)**

The use is correct. The target is a rate per vehicle-year and the weight is the vehicle-years that produced it. A weighted fit is then equivalent to modelling the total charge with an exposure offset under a Poisson or Tweedie loss, and the weighted mean of the target equals total charge / total exposure.
Exposure depends on EndDate, which is not known at pricing time. It is used only as a weight, never as a feature, so there is no leakage. It is also correct to weight the test score by it, which is standard actuarial practice.
 - Minor: the 2 rows with n_vehicles=2 should arguably carry vehicle-years of 2 x duration. This is negligible.
 - Without the weight, test deviance is worse (e.g. 96.7 unweighted vs 93.5 weighted in the 2012H2 window).

**Concerns, most serious first**


1. Weak signal and noisy, heavy-tailed scoring. The metric choice decides whether results mean anything.
   Evidence:
   - 95.7% of rows have a zero target.
   - The top 1% of rows carry 54% of the total charge.
   - The target reaches 75,929 because charges are divided by exposures as short as 0.08.
   - With a temporal split by year, a regularised LightGBM Tweedie model beats the exposure-weighted constant by only 1-2% in Tweedie deviance:
     ```text
       2012: 82.1 vs 83.0
       2013: 83.4 vs 85.0
     ```
   - The claim-indicator AUC is 0.65-0.66.
   - With half-year windows, the test sets have only about 210-1,150 rows with a claim. In 2 of 3 windows (2012H2 and 2013H2), my LightGBM did not beat the constant on deviance, and weighted MSE was essentially equal to the constant's (2.36e6 vs 2.36e6).
   - The pure premium also drifts upward about 9-10% per year (159.6 / 173.7 / 184.3), and no tree model can extrapolate that.
   Change:
   - Score with exposure-weighted Tweedie deviance (power around 1.5) or Poisson deviance, or a Gini / lift metric. Do not use RMSE.
   - Prefer test windows that are whole years (or that include a Q1 renewal block). Q1 holds about 60% of the rows because 37.5% of situations start on 1 January, so H2 windows are small.
   - Report the variance across splits.

2. Nominal codes stored as integers.
   Evidence:
   - These source labels were turned into int64: zone (A1-A6), client_activity (BusinessType B1-B8), distribution_channel (ChannelDist D1-D3) and formula (PolicyCateg C2-C5).
   - The source says levels are confidential ("most categorical levels have unknown meaning"), so no order is known.
   - power_value_class (P1-P11, "Combiné puissance valeur") may be ordinal. Keeping it numeric is defensible.
   Change: cast zone, client_activity, distribution_channel and formula to category.

3. Negative claim charges were clipped to 0 at the row level, and this is not documented.
   Evidence:
   - 597 of 4,568 claims are negative (minimum -1,254.8). These are IDA direct-compensation recoveries.
   - 537 rows had a negative net charge and now have target 0.
   - The total charge rose 4.3% (6.403M -> 6.676M).
   This is defensible: Tweedie needs y >= 0, and the gross cost is arguably what a pricer wants. But it changes the target's meaning.
   Change: state the clipping in task.md, or use the net charge floored at the portfolio level.

4. Columns that are useless or redundant.
   - insured_value_class is 99.85% missing (87,093 / 87,228 rows were "Unknown" in the source). Drop it, or keep "Unknown" as an explicit level rather than NaN.
   - n_vehicles equals 1 in all but 2 rows. Drop it.
   - exposure_to_year_end is n_vehicles x (year end - period_start)/365. This explains the maximum of 1.82 (two 2-vehicle rows). It is known at the start of the period, so there is no leakage, but it is a deterministic transform of period_start. Rename or drop it. If kept, cap it per vehicle.
   - period_start as a feature hurt in 2 of 3 windows (deviance 93.5 vs 93.6 and 100.3 vs 95.7 without it). It is legitimate, but tree models cannot extrapolate time.
   - Fine: VehiclCateg (constant V1), PolicyID, LicNb and ClaimNb were correctly dropped.

5. Repeated entities across splits.
   Evidence:
   - The 87,228 rows come from 18,037 policies (fleets), 4.8 rows per policy on average and up to 81.
   - 79% of the 2013 rows belong to a policy seen in 2011-2012, and 25% to the same vehicle.
   - There are 11,807 exact duplicate feature rows, including the date (vehicles in the same fleet share contract attributes).
   For renewal pricing, this overlap is realistic, not leakage. The policy ID is removed, so experience rating is impossible. That is acceptable but limits the attainable signal.
   No change is needed. Optionally, note it.

6. Situations that end before year end have a higher claim cost per exposure. This is informative truncation.
   Evidence: pure premium 193.6 (ended early) vs 159.9 (ran to year end), and claim rows per exposure 0.106 vs 0.090. Contract changes or cancellations after a claim probably shorten situations.
   This is inherent to the data and standard in insurance, so no change is needed. Be aware it makes the per-exposure target noisier for short rows.

7. Claim development and capping.
   Evidence:
   - 41 claims have SettlYear 0 (still open). The others settle in 2011-2014, so 2013 claims are the least developed. Yet the 2013 pure premium is not lower, so no visible under-reserving.
   - The maximum single claim charge is 8,565. The data may be capped or scaled for anonymity; the source does not say.
   No change is needed.

8. Labels and encodings. The categorical labels are in French ("> 5 ans", "<= 5 ans") and the deductible levels carry numeric prefixes ("1. 0", "2. 1 - 200"). This is harmless as categories. Missing values: only insured_value_class has any.

**What I could not check**

 - The exact boundaries of the 3 test windows and the benchmark's metric (task.md gives neither). I used my own half-year and year windows.
 - The original freakonometrics CSVs (the site did not respond). I verified against the CASdatasets copies instead; the French labels in the prepared data suggest a different but equivalent copy.
 - Whether the claim charges were scaled or capped by the organisers.
 - The real meaning of the anonymised levels.

</details>

<details><summary>Task gamer</summary>

**Task gamer: pricing_game_2016_french_fleet (claim_charge_per_vehicle_year, normalized weighted Gini, weight = exposure)**

Verdict: I found no exploit that beats the noise floor. The task cannot be gamed in any way I could measure. The training weight (the realised exposure, which the outcome can cut short) carries no usable signal under this metric.

Setup. Three splits share one training set (2011-01-01 to 2012-12-02, 56,178 rows). The test windows are 2013 Jan-Apr (19,229 rows), May-Aug (6,509) and Sep-Dec (5,312). Every model is LightGBM fitted with sample_weight = exposure, as the task asks. Scores are listed per split in the order r0 (Sep-Dec), r1 (May-Aug), r2 (Jan-Apr), then the mean.
- Untuned L2 baseline (baseline.py): 0.035 / 0.085 / 0.105, mean 0.075.
- Better honest model, Tweedie 1.5 bagged over 5 seeds (weight_attack.py): 0.224 / 0.214 / 0.180, mean 0.206.
- Noise floor: the same models refitted with one random column added (baseline.py, noise_bagged.py).
  - Untuned L2: mean ranges from 0.044 to 0.110.
  - Bagged L2: mean ranges from 0.082 to 0.140.
  - Bagged Tweedie: mean ranges from 0.172 to 0.196; single splits vary by up to about 0.05.
- With about 3,700 positive rows overall and a heavy-tailed target, any gain below about 0.03 in the mean is noise.

**Exploits ranked by gain**

| # | Exploit | Script | Honest | Exploited | Gain (per split) | Deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Realised exposure (the weight) as a feature, L2 | weight_attack.py | 0.1035 (L2 bagged) | 0.1338 | +0.067 / -0.015 / +0.039 | No: a period can be cut short by cancellation or change after it starts | none needed; the gain is inside the L2 noise range (0.08-0.14) |
| 2 | Exposure / planned exposure (cut-short ratio), Tweedie | weight_attack.py | 0.2061 | 0.2121 | +0.004 / -0.007 / +0.022 | No | none needed (noise) |
| 3 | Has a successor row with the same static key (future rows), Tweedie | order_and_test.py | 0.2061 | 0.2083 | +0.018 / +0.004 / -0.016 | No | none needed (noise) |

None of these is a real gain. With Tweedie, the exposure columns do nothing: exposure 0.1985, 1/exposure 0.2003, cut-short flag 0.2101, against the honest 0.2061. Exposure alone used as a ranking scores 0.029, close to zero.

Mechanism of the weight. Exposure is EndDate minus BeginDate, and EndDate can come before the year end. The kit's feature exposure_to_year_end equals (Dec 31 - period_start + 1) / 365 rounded to 2 decimals on all but 2 rows, so it is the planned exposure and is known at the prediction point. For 50,337 rows the realised exposure falls short of the planned one. These cut-short rows have a lower share of rows with a claim (3.3% against 5.6%) but a slightly higher charge per vehicle-year (220 against 171), because the target is already divided by exposure. Both the metric (L = cumulative exposure * y = cumulative charge) and the training weight remove the exposure effect, so a model has almost nothing left to learn from it. The weight is an outcome-dependent quantity a deployed model would not have. It could leak in principle; here it does not.

**Flaws that hurt an honest model**

None found. All the training-set choices below scored within noise of the weighted Tweedie (0.2061, honest_side.py):
- unweighted fit: 0.2064
- training on 2012 only: 0.2007
- dropping rows with exposure < 0.1: 0.2047
- dropping period_start: 0.1882 for Tweedie, 0.1148 for L2

Dropping period_start helps the untuned unbagged L2 (0.075 to 0.131), but that is a weakness of the model when it extrapolates in time, not a flaw of the task.

**Attacks that found nothing**

- Order and ids.
  - The data is sorted by period_start. Neighbouring rows agree on the label 0.9190 of the time, against 0.9185 by chance (correlation 0.005).
  - The rank of a row within its start day predicts a claim with AUC 0.502. As a feature it scores 0.2079.
  - The row position within 2012 has AUC 0.41, but that is period_start itself: later starts mean less exposure left in the year.
- Copies and entities across the split.
  - Ten static columns form 19,518 keys, which is not unique enough to identify vehicles.
  - Only 6-10% of rows have a same-key row starting the day after they end, so the vehicle chains cannot be rebuilt.
  - The successor flag scores 0.2083 (see #3).
- Statistics over the test rows.
  - Number of rows with the same key over all rows: 0.2098.
  - Number of rows starting on the same day: 0.2032.
- Formats. The features are categorical classes or 2-decimal derived values, so there are no digit patterns to exploit.
  - insured_value_class is missing on 87,093 of 87,228 rows (99.8%). Rows that have it show a claim in 2.2% of cases against 4.3% for the rest. That is 135 rows, too few to matter.
  - exposure_to_year_end is above 1 (1.82 and 1.26) on 2 rows, an artefact without effect.
- Columns from after the prediction point. None among the features. exposure_to_year_end is planned, not realised. EndDate, Exposure, ClaimNb and the other claim fields of the source are not in the features.
- Transforms over all rows. No column is standardised or ranked over the full table.
- Web search: I found no competition forum or leak thread for the 2016 game. The CASdatasets documentation (saved in the kit as pricingame.Rd) lists the source columns. Compared with the kit, the preparation dropped PolicyID, LicNb, EndDate, Year, VehiclCateg and BusinessType, as well as ClaimNb, DirectComp, CompRate and SettlYear. Without PolicyID and LicNb, vehicles cannot be followed across years. Looking rows up in the public pg16trainpol/pg16trainclaim files would recover the labels; that is not a flaw of the task.

**Could not check**

- Whether 2012 claim charges were fully settled when the data was extracted. SettlYear was dropped, so labels of recent training rows could be incomplete; the claim rate is flat across 2011-2013 (about 4.2-4.5%), so there is no sign of it.
- Whether a deployed fleet pricer would use claims history per vehicle. That needs PolicyID, which the kit does not have.

</details>

<details><summary>Precedent check</summary>

**Precedent check: pricing_game_2016_french_fleet, exposure re-review of 2026-11-06 (full tier)**

**Verdict**

- **D11's target, weight, feature and metric parts follow the precedents.**
- **D11's training-side part reverses Andrej's 2026-11-02 call (issue 2 (d)), and it states a fact that sets it apart.** The fact is a new measurement plus a newer Must.
- **What is implemented now (three windows on one training side) breaks SPLIT-14 (Must) with no fact that sets it apart.** LEAK-41 does not force it, because option C meets both rules. Issue 6 is the right place to settle this. Below is the reflection prompt for it, and two corrections to issue 6's own text.

**Sources read**

All in the repository (branch zi-datasets):

- `datasets/_dev/tabarena-v0pt2/pricing_game_2016_french_fleet/REVIEW.md` (issues 1-6), its `dataset.py` (split code and `splits_comment`), and `curation/records/pricing_game_2016_french_fleet.md` (CC lines of 2026-11-02 and 2026-11-06).
- `.claude/skills/knowledge-curation/references/splits.md`: SPLIT-8, 9, 10, 11 and 14, and the Cases table.
- `.claude/skills/knowledge-curation/references/leak_checks.md`: LEAK-41 and the Mechanisms row on time on risk.
- `.claude/skills/knowledge-curation/references/principles.md`.
- The REVIEW.md of the siblings, same folder layout: `wisconsin_local_government_property_insurance_fund` (issues 1 and 3), `spanish_motor_insurance_coverage_level_2022_2024`, `pricing_game_2017_french_mtpl`, `frempl_french_motor_personal_line`.
- Every sibling's change note of this run (`CHANGES.md`), the decision register (`register.json`, `register.log`) and `probes/probe22_l2.txt`, in the run folder.

**Decision 1: D11, the target, weight, feature and metric (Lennart, 2026-11-06, issue 5)**

**Consistent.**

- **Realized time on risk is the weight and never a feature; the rate is the target.** This follows the four other 2026-11-06 decisions:
  - fremtpl2 and bemtpl97 (option A of #51).
  - australian_vehicle_insurance_2004_2005 (D8).
  - frempl_french_motor_personal_line (D9).
  - spanish_motor_insurance_coverage_level_2022_2024 (D10, `actual_exposure` the `sample_weight`).
  - The rule is LEAK-41's Cases row, plus MET-14 and MET-15.
- **The length to 31 December kept as `exposure_to_year_end`** follows frempl's `length_to_year_end` (LEAK-7, LEAK-37). Andrej's fix of 2026-11-02 (issue 1, the Mechanisms row) still holds as a feature.
  - Probe 22 gives R² 0.38 through fleet_management (49% of the gain) and exposure_to_year_end (38%). Both are known at the start, so they stay under LEAK-41's timing clause.
  - frempl is the precedent: R² 0.34, 86% through `length_to_year_end`, kept.
- **frempl's open issue 7 does not carry over.** That issue exists because frempl ships on the log1p scale. pg16 ships the rate on the identity scale (CLEAN-16 as amended), so the squared-error problem does not arise.
- **`normalized_weighted_gini` as a stand-in** matches australian (D8) and spanish coverage, and MET-10 (Andrej, 2026-11-02: no family call, diversity when in doubt). pg17 moved to the Tweedie deviance (Andrej, 2026-11-03). That is case by case under MET-10, not a conflict.
- **D11 supersedes Andrej's 2026-11-02 target call (issue 4) with a stated measurement**: the stay is worth about 0.03 of the row Gini, and the rate model scores 0.154 against 0.136. australian's D8 and spanish's D10 superseded Andrej's calls of the same day in the same way. Same pattern, no drift.

**Decision 2: D11, every window trains on 2011-2012**

This reverses Andrej's issue 2 (d) of 2026-11-02 (CC line in the record; splits.md Cases row "SPLIT-14 (amended 2026-11-02, Andrej), SPLIT-11").

**It departs with a stated reason.** The fact that sets it apart is real and new:

- **New measurement.** The exposure study of 2026-11-05 measured the 2013 periods the expanding sides admitted. They claim more per vehicle-year: 0.127 and 0.131 against 0.115 and 0.116. They make up 10.8% and 4.0% of the training vehicle-years of the September and May windows.
- **This was not known on 2026-11-02.** The Assessment that day saw only the per-period claim share ("3.2% and 2.4% with a claim"), which looked lower. The answer to Andrej framed the closed periods as "as a refit on that day would see them".
- **New rule.** LEAK-41 (Must, 2026-11-06) bars training "on rows selected by the realized weight". Admitting a 2013 period because it ended before the window start selects it by its realized length.
- **Precedence allows the reversal.** Principles say a newer curator decision and a later measured finding win.

**It also matches an older precedent.** hotel_booking_demand (SPLIT-9) is the closest older case: rows in training because their outcome came early, plus a time feature that turns the selection into a shortcut. pg16 has `period_start` as a datetime feature, so the expanding sides taught "2013 start, higher rate". This supports the reversal under SPLIT-9 and SPLIT-10 even without LEAK-41.

**One open point (not a departure).** No one measured whether the admitted early-ended 2013 periods belong to the same vehicle or contract as later periods in the test window. That would make the selection a SPLIT-9 shortcut (alfa_battle_2_0_task_2) rather than the diffuse kind (lt_vehicle_loan_default_prediction). It changes nothing for D11, which removes the rows anyway.

**What it leaves broken.** D11's wording keeps three windows on one shared training side. That is the setup Andrej's SPLIT-14 amendment counts as one window. Lennart reframed SPLIT-14 on 2026-11-05 ("each window trains on what is known before it starts"), so this also contradicts Lennart's own wording of the day before. D11 rightly leaves this to issue 6, so it is not drift yet. It becomes drift if A is taken without an amendment. See decision 4.

**Decision 3: the no-gap exception to SPLIT-10 (Andrej, 2026-11-02, issue 3), kept "on new grounds"**

**Still reasonable, but its stated reason is now stale.**

- **The record line is out of date.** It still reads "Serves SPLIT-14: three windows on distinct training sides above the floor". Under D11 the training sides are no longer distinct.
- **The new ground is better than the old one.** REVIEW.md gives it: a gap inside 2012 would admit 2012 periods by their realized end (LEAK-41, a Must), and a one-year gap leaves 2011 alone (30.4%). The departure from SPLIT-10 (Should) now yields to LEAK-41 (Must), plus SPLIT-14's floor. The exception should be re-recorded with this reason.
- **It now covers one window only.** The May and September windows start 4 and 8 months after the training side ends, so only the January window lacks a gap.
- **The register's amendment-due flags are not new drift.** These are flag 17 (SPLIT-10, 9 datasets) and flags 18-24. Andrej declined the SPLIT-10 amendment on purpose on 2026-11-02 (avito_demand_prediction issue 4: "each no-gap departure for SPLIT-14's floor ... stays an exception").
- **The "exception_to_must: SPLIT-14" flags are misattributions.** They are SPLIT-10 exceptions that serve SPLIT-14. spanish coverage's earlier precedent check said the same.
- **Process gap.** splits.md has no SPLIT-10 Cases row for pg16, spanish_homeowners_motor_insurance_2010_2014 or wisconsin. The no-gap exceptions of 2026-11-02 for all three exist only in the records, while principles.md asks for a Cases row of kind `exception` for each.
- **If issue 6 goes to C,** the exception disappears (the Notes for the AI say so), and pg16 drops out of the count.

**Decision 4: issue 6 (open) against the SPLIT-14 precedent**

**The closest precedent is spanish_motor_insurance_coverage_level_2022_2024**, not pg17 or frempl. Its facts:

- Three stacked calendar years and recurring entities.
- One valid annual window above the floor: 2024 trained on 2022-2023, 52.5% of the rows. The second window would train on 19.0%.
- Result: forced grouped by `insured_id`, `ForcedGroupedFromTemporal` (Andrej, 2026-11-02: "Forced group splits should be fine"). The leak test found none.

pg16 has the same structure: 2013 on 2011-2012 is 64.4%; 2012 on 2011 is 30.4%.

**Correction 1 to issue 6's text.** Its Consistency bullet calls spanish coverage "one valid yearly window, below the floor" and names "its one valid window is above the floor" as what sets pg16 apart. Both are wrong: spanish's valid window is above the floor too (52.53%, its split audit and claim 34). The only remaining distinguishing fact is that pg16's dates are daily, so 2013 can be cut into sub-windows. Andrej's amendment exists precisely to say such a cut on one training side counts as one window. Under SPLIT-14 as it stands, pg16 has the same facts as spanish and gets C.

**Other precedents for C:**
- nba_players_2016_2019 and open_university_learning_analytics_dataset (Lennart, 2026-10-21): too few periods, one valid window, grouped by entity, cost measured against the valid window. These cases created SPLIT-8's "too few periods" clause.
- pricing_game_2017_french_mtpl and frempl (one year each) and distribution_transformers_at_cauca_department (one window, forced IID) were forced too.
- No shipped dataset has windows that share a training side. I searched every definition, REVIEW.md, record and knowledge file.

**Option A, with an amendment.** No precedent supports it, and it reverses a Must amended four days earlier.
- The amendment issue 6 drafts ("when the annual cut leaves no other training side free of a selection by the outcome") would reach only pg16. spanish coverage and pg17 have no dates within a year; frempl has a single year.
- An amendment written to fit one dataset works like an exception to a Must, which principles.md bars ("A Must has no exceptions").
- It would also run against Lennart's 2026-11-05 reframing.

**Option B, one window.** It needs an amendment below three windows. That amendment would reopen spanish coverage, nba and open_university (each has one valid window), and distribution_transformers_at_cauca_department (two label years, one window, shipped forced IID). It would also reach the AIcrowd question for pg17 and wisconsin's option B. B departs from five precedents. It is a family-wide change, not a pg16 call.

**Correction 2: option C has an unchecked precondition from wisconsin.**
- Wisconsin's forced member folds shared each year's claim level across the split. Its 2026-11-02 leak test measured +0.010 claim AUC (8 of 9 folds) and +0.113 Gini pooled.
- That finding moved Andrej to temporal windows below the floor. The decision was reopened as wisconsin issue 3 (open, 2026-11-06).
- pg16's C evidence (0.182 pooled; 0.174 on its 2013 rows against 0.171 for the valid window) is close to a leak check but is not the SPLIT-8 test. That test is listed under "Notes for the AI" and has not been run.
- The likely distinguishing fact: pg16's claims per vehicle-year are flat across 2011-2013 (issue 3: LEAK-24 holds), while wisconsin has a storm year. It should be measured the wisconsin way (test year's training rows in or out) before C is recommended as "the rule's own fallback" without qualification.

**Decide together.** pg16 issue 6 and wisconsin issue 3 are both open SPLIT-14 readings, with the same curator on the same day. Deciding them apart risks two amendments that pull opposite ways: A loosens "own training side", while wisconsin A/B loosens "the floor / three windows". pg17's consistency check also hangs on wisconsin.

**Reflection prompt (issue 6; the implemented state has no fact that sets it apart)**

**Consistency check (AI, 2026-11-06):** three windows of 2013 on one training side differ from spanish_motor_insurance_coverage_level_2022_2024 (forced grouped, 2026-11-02), which has the same facts. What sets this case apart?

**Problem:**
- D11 (2026-11-06) trains all three windows of 2013 on the periods of 2011-2012. SPLIT-14 as amended on 2026-11-02 (Andrej), and reframed on 2026-11-05 (Lennart), counts that as one window[^14].
- spanish_motor_insurance_coverage_level_2022_2024 has three stacked years, one valid window above the floor (52.5%) and recurring entities, and shipped forced grouped by policy[^8]. pg16 has three stacked years, one valid window above the floor (64.4%) and recurring contracts.
- The fact issue 6 offers as the difference ("one valid window above the floor") is false: spanish's is above the floor too. The daily dates are the only fact left, and Andrej's amendment rules out exactly that kind of cut.
- LEAK-41 does not force three windows on one side, because a forced grouped split meets LEAK-41 and SPLIT-14 together[^41]. So keeping them would break a Must without a higher-ranked Must behind it.

| | Option | Pro | Con |
|---|---|---|---|
| a | Record as an amendment to SPLIT-14 the fact the AI guesses sets pg16 apart: rows cut at 31 December and undated claims leave no selection-free training side between year ends, and the game's tariff is fit once a year (SPLIT-12) | keeps the temporal regime the use case implies, and the game's own design | an amendment that fits only this dataset; it reverses Andrej's amendment of 2026-11-02 and your reframing of 2026-11-05; one evaluation still counts three times |
| b | Treat pg16 like spanish coverage: forced grouped by `contract_id`, `ForcedGroupedFromTemporal` (issue 6 C) | the rule's own fallback; the same as spanish, nba, open_university, pg17 and frempl; scores 2013 like the valid window (0.174 against 0.171); the SPLIT-10 exception goes away | mixes the years; tests unseen fleets; the SPLIT-8 leak test across the split is not run yet (wisconsin found a year-level leak there) |
| c | Reopen spanish coverage to match pg16 | none: spanish has no dates within a year, so it cannot be cut into sub-windows | does not apply |
| d | Amend SPLIT-14 to allow fewer than three windows when only one or two are valid (issue 6 B), decided with wisconsin issue 3 | one evaluation counted once; would also settle wisconsin B and pg17's AIcrowd question | reopens spanish coverage, nba, open_university and distribution_transformers_at_cauca_department; a family-wide change of a Must |

**Recommendation:** (b), after the SPLIT-8 leak test across the contract folds (test year's training rows in or out, as on wisconsin) confirms what the flat claims per vehicle-year suggest. Take (d) only if you want the change for the whole family, decided together with wisconsin issue 3.

[^14]: **SPLIT-14** (Must), amended 2026-11-02 (Andrej), reframed 2026-11-05 (Lennart). Cases row: pricing_game_2016_french_fleet, reopened 2026-11-06.
[^8]: **SPLIT-8** (Must; narrows SPLIT-14), "a release with too few periods for three windows". Cases: nba_players_2016_2019 and open_university_learning_analytics_dataset (2026-10-21). Siblings shipped on Andrej's call of 2026-11-02: spanish_motor_insurance_coverage_level_2022_2024, pricing_game_2017_french_mtpl, frempl_french_motor_personal_line.
[^41]: **LEAK-41** (Must, 2026-11-06): "No model is trained or scored on rows selected by the realized weight". principles.md, "Exceptions and amendments": "A Must has no exceptions: only a higher-ranked Must overrides it, and anything else is an amendment."

**Text fixes (no decision needed)**

1. **REVIEW.md issue 6, Consistency bullet.** spanish coverage's valid window is above the floor (52.5%), so the "What sets this case apart" sentence needs rewriting.
2. **Record, "Exception to SPLIT-10 (2026-11-02, Andrej)".** "Serves SPLIT-14: three windows on distinct training sides above the floor" is stale. The new ground is LEAK-41 plus the floor, with the January window only.
3. **splits.md.** SPLIT-10 Cases rows of kind `exception` are missing for pg16, spanish_homeowners_motor_insurance_2010_2014 and wisconsin (all 2026-11-02).
4. **Optional.** Add hotel_booking_demand (SPLIT-9) as a supporting precedent in D11's CC line: rows in training because their outcome came early, with `period_start` a feature.

</details>

<details><summary>Advocate</summary>

**Advocate, opening brief: pricing_game_2016_french_fleet (exposure re-review, 2026-11-06, full tier)**

Position: ship. D11's target, weight, features and training side are right, and no agent refuted a number. The one Must the dataset breaks as defined is SPLIT-14 (issue 6). Fixing it changes the split (or the rule), not whether the dataset ships. Everything else needs a note, a cheap retype or a text fix.

1. A real pricing task, and the numbers reproduce (P2, P3: SEL-2, USE-1, USE-5, USE-8 Must; MET-14).
   - Evidence: the domain practitioner, a fleet pricing actuary, calls the fit direct. The target is "the pure premium rate I put in the tariff", and the weighted fit estimates "the rate that breaks even when the premium is earned pro rata".
   - The blind reviewer rebuilt the target from the CASdatasets copies on their own: all 4,568 claims match and the total is exact (6,675,926.40). They called it "a real, standard actuarial use".
   - The claim auditor re-measured 35 claims and refuted only claim 35, the implied one that the rows are not selected by their length (point 6). No figure in the notes was wrong, and the metric matches Kaggle's weighted Gini to 1e-12.
   - Why it outranks: P2 and P3 are the top validity principles. Every objection below is at P4 or lower and is fixable (Tensions row "a real task against a leak": fix the leak, keep the task).

2. No leak through the weight, and D11 follows LEAK-41 and MET-15 (P4; LEAK-41 Must, MET-15 Must, LEAK-7, LEAK-37).
   - `exposure` is the metric's weight and `sample_weight` only. It is not among the 16 features (claim 3, column audit).
   - Every feature is known at the period's start. `exposure_to_year_end` is never below the realized length (0 rows).
   - The task gamer found no exploit above noise. With Tweedie, the realized weight as a feature scores 0.1985 against the honest 0.2061. 1/exposure alone scores 0.029.
   - The claim auditor's Tweedie arm gives the weight as a feature +0.0118 (SD 0.0067). No weight-mediated gain of any feature is above noise.
   - Concession (EV-1): probe22.txt and probe22_l2.txt are the same L2 run. That arm cannot see the weight itself (-0.0014, SD 0.052), so the cited probe had no power. The conclusion stands on the auditor's Tweedie arm.
   - Mildest remedy: cite the Tweedie numbers in the notes and in REVIEW issue 5, and re-run probe 22 with the actuarial objective. That is a note fix, not a definition change.
   - Precedent: frempl (D9), spanish coverage (D10), australian (D8) and fremtpl2/bemtpl97 all made the same call (precedent checker: "consistent").

3. The new training side is the honest one (P4; LEAK-41 Must outranks SPLIT-11 Should).
   - The old expanding sides admitted 2013 periods because they ended early. Those periods claim 0.127 and 0.131 per vehicle-year, against 0.115 and 0.116 for the 2013 periods still running (claim 8, exact).
   - With `period_start` a feature, that is a selection-by-outcome shortcut. hotel_booking_demand under SPLIT-9 is the precedent the precedent checker found.
   - The practitioner: "I would never refit in May on the 2013 vehicles that had already left."
   - The reversal of Andrej's 2026-11-02 call rests on a new measurement and a newer Must. Principles allow that ("a later measured finding wins").

4. Worth benchmarking (P6; TP-4 Must, TP-9 Must).
   - The weighted Tweedie LightGBM scores 0.110 / 0.157 / 0.189 (re-measured) against 0 for the weighted constant. The newest window beats the constant by 1.7 SE. The GLM scores 0.159 / 0.171 / 0.200.
   - The gamer's bagged Tweedie scores 0.206 mean, against a noise band of 0.172-0.196.
   - The test windows hold 103 / 232 / 1,026 positive charges, so none is a handful (TP-9).
   - The blind reviewer's "weak signal" is real but is a property of a sparse pure-premium table. It is no reason to drop the dataset: Tensions row "the right split against the score: a small signal under it is no reason to retire" (forest_fires).

5. Issue 6, the shared training side: I concede SPLIT-14 (Must) is broken as defined. The dataset survives it by a re-split or an amendment, not by exclusion (remedy ladder).
   - Concession: the three splits have identical training indices (56,178 rows). SPLIT-14 as amended on 2026-11-02 counts that as one evaluation. A Must has no exceptions, so the defined state (option A) cannot ship on a note.
   - Fix within the current rules, (C): SPLIT-8's own fallback, ForcedGroupedFromTemporal by `contract_id`. The split auditor's paired comparison on the same 2013 rows: forced 0.174 against the valid window's 0.169, difference +0.005 (SD 0.022, 9 folds), no more optimistic beyond noise. The cold start of a new fleet costs about 0.004. C has the same facts as spanish coverage, nba and open_university.
   - Precondition for C: SPLIT-8's leak test across the contract folds has not been run. Wisconsin found a year-level leak there. Here claims per vehicle-year are flat at 0.117 / 0.119 / 0.119 across 2011-2013 (LEAK-24 holds), where wisconsin had a storm year, so I expect the test to pass. It still has to run first.
   - If the curators prefer A, it needs an amendment. The practitioner supports A on P3: the tariff is fit once a year and judged on the whole book (SPLIT-12), and 76-81% of the test periods are on known contracts (USE-10, Must, Part 2). The practitioner ranks fidelity B > A > C.
   - I do not claim USE-10 forces A. The measured cold-start cost (0.004) and the absence of any history feature mean C does not break USE-10 in substance. So there is no conflict for rank to settle (principles, How to decide 4). A is a curator's choice to amend, decided together with wisconsin issue 3, as the precedent checker asks.
   - Either way the dataset ships. The only open question is which split it ships with.

6. The source's 30-day floor is a property of the source's population that both sides share. It needs a LEAK-41 note, not exclusion (LEAK-41 Must, last clause; USE-7; remedy ladder).
   - Concession: no period is shorter than 30 days, and the floor is a sharp edge, not a taper. There are 1,558 gaps of 1-29 days between a vehicle's consecutive periods. So the organisers selected rows by their realized length, and our notes call it an "anomaly" without citing LEAK-41.
   - Why it does not sink the dataset:
     - The selection is the organisers', made before release. It is the same on the training and test sides, and the game's own 2014 file had it too. Nothing we choose adds a selection.
     - The removed periods and their claims are not published, so no definition change can undo it.
     - By weight it is small: the column auditor estimates about 1.5% of vehicle-years overall. The claim auditor estimates up to about 11% of the September-December window's vehicle-years.
   - The task's population is "periods of cover of a month or more". The game priced that population.
   - Mildest remedy: rewrite the anomaly bullet as a LEAK-41 note with the per-window estimates, and have the curator accept it as the source's population.
   - The uneven selection across windows also counts against A's equal thirds, which I accept as an input to issue 6.

7. The rest is quality work and text fixes, below validity (P7 and process; CLEAN-14 Should, MET-10 Weigh, MET-11).
   - CLEAN-14: four band columns ship unordered (`contract_age_class`, `vehicle_age_class`, `deductible_class`, `insured_value_class`). The column auditor gives the exact ordinal lists. The fix is cheap and safe, so take it at the next rebuild.
   - Metric: the practitioner shows the Gini cannot see how steep the relativities are. A tariff and the same tariff with doubled relativities both score 0.173. The Gini stand-in still follows australian (D8) and spanish coverage under MET-10, a Weigh call with no family rule (Andrej, 2026-11-02).
   - Metric remedy: reword the stand-in reason. The market rewarded relative prices, and the ranking is the part the Gini scores. Optionally add the rescaled weighted Tweedie deviance as context. Neither changes the verdict.
   - The blind reviewer's concern about integer-coded categories does not apply to the shipped frame: the column auditor finds them typed as categories. Dropping `n_vehicles` and `insured_value_class` was settled (D4, CLEAN-5). The IDA clipping is already in the notes (claim 1).
   - Text fixes that need no decision:
     - CHANGES.md: the "0.182 ... no more optimistic" wording.
     - Issue 6 says spanish coverage's valid window is below the floor; it is above it at 52.5%.
     - The record's stale "Exception to SPLIT-10" reason.
     - The missing SPLIT-10 Cases rows.
     - The outdated SPLIT-14 Cases row for this dataset.
     - The "unchecked" pro-rata claim, which the claim auditor and the practitioner have since sourced.

Judgment record as I would write it:

```text
Verdict: ship after changes.
Validity: SEL-2, USE-1 (direct), USE-5, LEAK-7/37, LEAK-41 (weight), MET-15, SPLIT-9 hold. SPLIT-14 broken as defined: fix by re-split (C, after SPLIT-8's leak test) or an amendment (A), issue 6. LEAK-41's last clause: the source's 30-day floor, kept with a note (it cannot be undone and is the same on both sides).
Value: TP-4 holds (0.110 / 0.157 / 0.189 against 0), TP-9 holds.
Quality: CLEAN-14 retype of the four bands (cheap); metric reason reworded.
For the curator: issue 6 (C, or A by amendment, decided with wisconsin issue 3), and accepting the 30-day floor as the source's population.
```

Sources: the phase A reports of this panel (claim, column and split audits, the domain practitioner, the precedent check, the blind review, the task gamer); the rules in `.claude/skills/knowledge-curation/references/` (principles.md, splits.md, leak_checks.md, use_case.md, metrics.md); REVIEW.md in `datasets/_dev/tabarena-v0pt2/pricing_game_2016_french_fleet/`.

</details>

<details><summary>Critic</summary>

**Critic's opening brief: pricing_game_2016_french_fleet (exposure re-review, 2026-11-06, full tier)**

Position: do not ship as defined. Ship after changes. The task is real (USE-8, direct fit). D11's target, weight and feature handling holds on every measurement (claim auditor, items 1-4 and 9-10; column auditor; blind reviewer; task gamer), and I do not contest it. Three things fail as defined. The split breaks a Must. A source-side selection by the realized weight falls under LEAK-41's letter and has no ruling. The evidence cited for probe 22 has no power. Two lesser points follow on the metric reason and the record text, then one quality point.

1. The three windows share one training side (P4, SPLIT-14 Must; issue 6, open).
- Problem: all three splits have the same 56,178 training rows (64.4%), confirmed on the container by the split auditor and claim auditor item 17. SPLIT-14 as written says: "windows that share one train side test one model on several test periods, which is one evaluation, not several". Its Cases row was written for this dataset in exactly this configuration.
- Effect on the task: one evaluation is counted three times. The Sep-Dec window holds 7% of the test vehicle-years (987 of 13,864) and 103 positive charges, yet gets a third of the weight. Its SE is 0.068 and it beats the constant by only 1.7 SE. The task gamer puts single-split noise at up to about 0.05. The window mean (0.154) is below the same model's pooled 2013 score (0.171), so the reported number is mostly the cohort mix and noise.
- No higher Must forces A. LEAK-41 and SPLIT-14 are independent here, because a forced split grouped by contract meets both (split auditor section 1; principles.md "How to decide" 4). "A Must has no exceptions" (principles.md), so A can stand only through an amendment. That amendment would reverse Andrej's 2026-11-02 call on this very dataset and Lennart's 2026-11-05 reframing. It would also fit one dataset only (precedent checker, Decision 4).
- Same facts as a precedent: spanish_motor_insurance_coverage_level_2022_2024 has three stacked years, one valid window above the floor (52.5%) and recurring entities, and it shipped ForcedGroupedFromTemporal. Issue 6's consistency bullet says spanish's valid window is "below the floor". That is false, so issue 6 names no fact that sets this case apart.
- The practitioner's USE-10 objection (C tests unseen fleets) does not decide this. SPLIT-8 is a Must that "narrows ... USE-10". The cost is measured and small. Paired on the same 2013 rows, C's model scores +0.005 against the valid window (SD 0.022, 9 folds). Removing the test fleets' history costs -0.004 (split auditor section 4).
- Remedy (re-split): option C. Group by `contract_id` (the source's Num_contrat), `ForcedGroupedFromTemporal`, contract_id the group column and never a feature. Drop the SPLIT-10 exception. The splits_comment should say what the dates would change. One condition before C ships: SPLIT-8's leak test across the grouped split and the leak probes on it. No probes/group.txt exists, and wisconsin found a year-level leak in the same setup (+0.113 Gini pooled). If the curator prefers A or B, it has to be a deliberate amendment of SPLIT-14, decided together with wisconsin issue 3, never a dataset-level exception.

2. The source selects rows by their realized length, unevenly across windows (P4, LEAK-41 Must, last clause; new).
- Problem: LEAK-41 says "No model is trained or scored on rows selected by the realized weight". Every row here passed the organisers' 30-day floor.
  - The length histogram stops sharply at 30 days with no taper: 0 rows at 29 days, 909 at 30, about 700 a day at 32-40.
  - Between a vehicle's consecutive periods there are 1,558 gaps of 1-29 days, at a flat rate of about 45 a day, which is where the dropped short periods would sit.
  - No period starts after 2 December.
  - Sources: claim auditor finding 1 and item 35; column auditor problem 1.
- Effect: the short periods that were left out claim more per vehicle-year (0.143-0.160 for early ends of 30-59 days against 0.124 for 180+ days), and their claims are gone.
  - Overall it is small by weight: about 1.5% of vehicle-years (column auditor).
  - It is concentrated in the newest test window: about 35% of its would-be periods and about 11% of its vehicle-years (claim auditor, rough extrapolation). That is the same window that already carries a third of the score under A.
- The definition calls this an "Anomaly ... periods of a month or more" and cites no rule. A Must cannot be settled by a provenance remark.
- Remedy: no repair is possible, because the cut rows are not published. I do not ask for exclusion: the selection is the same in train and test and small by weight. I ask for two things.
  - (a) An explicit curator ruling, recorded as an amendment to LEAK-41's last clause. It would say that a selection the source made uniformly, which cannot be undone, defines the population (USE-7) and is sized in the notes. It is not a dataset exception, because a Must has none. It applies to frempl and to any sibling with a minimum length.
  - (b) A rewrite of the anomaly bullet as a LEAK-41 note, with the histogram and gap evidence and the per-window estimate, plus one line in issue 6: the newest window is the noisiest and also the most selected, which counts for C.

3. The cited evidence for probe 22 cannot detect a proxy (LEAK-41 Must on the reporting; EV-1).
- Problem: probe22.txt and probe22_l2.txt are byte-identical (I ran cmp), and both are the L2 arm ("LightGBM objective L2"). In that arm the realized weight itself, the leak, gains -0.0014 (SD 0.052). "No feature's gain goes through the weight above noise" could not have come out any other way.
- LEAK-41 asks for the gain "with an L2 fit on the shipped scale and with the weighted actuarial fit", and for a decision on the worse of the two.
- The conclusion survives: the claim auditor ran the Tweedie arm (3 seeds), and the weight as a feature gains +0.0118 (SD 0.0067). The weight-mediated gains are all under 1 SD:
  - time features +0.006 (SD 0.014)
  - distribution_channel +0.003
  - client_activity +0.002
  - fleet_management -0.003
- So the evidence the notes cite does not carry the claim.
- Remedy (fix the definition's notes): re-run probe 22 with the weighted Tweedie objective so the two files differ. Cite both arms in the Exposure / probe 22 bullet and in REVIEW issue 5.

4. The stand-in metric's reason misstates what the original rewarded, and closeness is not measured (P6, MET-11 Must, MET-2).
- Problem: the reason says the uniform rescaling meant "the market rewarded the ranking of the risks". In a cheapest-wins market after a uniform rescaling, a player wins on relative prices: both the order and the spread of the relativities. The Gini sees only the order.
  - Measured by the domain practitioner, means over the windows: the GLM and the same GLM with its relativities doubled both score Gini 0.173.
  - The exposure-weighted Tweedie deviance after the game's own uniform rescaling to the window total gives: GLM 89.63, GLM doubled 94.27, LightGBM 91.34, constant 90.82. It ranks the over-steep tariffs below a flat one, which is what the market would have done.
  - The reason dismisses deviance because it "also scores the year's level". The rescaled form removes the level the same way the game did, so the reason argues against a version nobody proposes.
  - MET-11 asks that "the closeness is measured on the shipped splits where possible". It is possible here and was not done.
- Effect: the metric changes which models win. By rescaled deviance the GLM beats the steep tree model; by the Gini they nearly tie (0.173 against 0.157).
- Remedy (mildest first):
  - (a) Reword the reason: the market rewarded relative prices, of which the Gini scores the ranking. State what it misses.
  - (b) Measure the uniformly rescaled weighted Tweedie deviance against the Gini as a candidate stand-in and give the curator the call (MET-4/MET-11 tension row). Its costs are an oracle scale (the test total, as the game fixed 2.5 million euros) and more noise on the newest window.

5. Several statements in the record and the review file are stale or wrong (EV, writing; Should).
- The SPLIT-10 exception line still reads "Serves SPLIT-14: three windows on distinct training sides above the floor". Under D11 the training sides are no longer distinct. The real ground is LEAK-41 plus the floor, and it covers the January window only (precedent checker, Decision 3). splits.md also lacks the SPLIT-10 Cases row of kind `exception` for it.
- REVIEW issue 6 says spanish coverage's valid window is "below the floor". It is 52.5% (point 1).
- splits.md's Cases row for SPLIT-14 on this dataset still describes the expanding windows as "applied".
- Two effects are stated more firmly than the seeds allow, though both are within noise:
  - "a fit that ignores the weight loses 0.010 (4 of 5 seeds)": the auditor's 3 seeds give +0.005 (2 of 3).
  - "the time features add 0.007": the auditor's 3 seeds give +0.003.
- "A cut nobody scheduled" overstates the case: 25.9% of early ends fall on a month's last day (column auditor problem 4).
- CHANGES.md says option C's "0.182 overall" is "no more optimistic". That holds only for its 2013 rows (0.174, or paired +0.005).
- Remedy: correct these lines and mark the two effects "within seed noise".

6. Four band columns ship as unordered categories (P7, CLEAN-14 Should; quality, not a reason to exclude).
- Problem: contract_age_class, vehicle_age_class, deductible_class and insured_value_class are bands of a quantity with an open end. CLEAN-14 and its cleaning table ("a count or band the source cuts at an end") make these an ordered category, lowest first.
- The 2026-11-01 blind review raised this and nothing changed. The 2026-11-01 column table calls deductible_class ordered, but the shipped dtype has cat.ordered False. `_feature_types` declares only `categorical=CATEGORICAL, datetime=["period_start"]`.
- Effect: small; models that use the order lose it.
- Remedy (cheap and safe): declare the four as ordinal, with the level lists in column auditor problem 2, and update the Dtypes bullet.

Not raised, because the evidence does not hold:
- The blind reviewer's points on integer-coded nominals and on undocumented clipping are stale. The shipped columns are categories, and the clip is documented with its counts.
- The task gamer found no exploit above the noise floor, and the column auditor found no feature set after the prediction point.

Judgment record, as I would write it:

```text
- Verdict: ship after changes.
- Validity:
  - USE-8 holds (direct fit).
  - LEAK-41 holds for the features and the weight.
  - LEAK-41's selection clause is triggered by the source's 30-day floor: an amendment or ruling is needed, plus a note (point 2).
  - LEAK-41's reporting is incomplete (point 3).
  - SPLIT-14 is broken: re-split as SPLIT-8 (C) after its leak test, or a deliberate amendment (point 1).
- Value: TP-4 holds, weakly on the newest window. MET-11's reason is to be corrected and its closeness measured (point 4).
- Quality: CLEAN-14 ordinal bands (point 6); text fixes (point 5).
```

Sources:
- Panel reports: the claim, column and split audits, the domain practitioner, the precedent check, the blind review, the task gamer; probes/probe22.txt and probes/probe22_l2.txt.
- Definition: `datasets/_dev/tabarena-v0pt2/pricing_game_2016_french_fleet/dataset.py`
- Rules in `.claude/skills/knowledge-curation/references/`: principles.md, splits.md (SPLIT-8, SPLIT-14), leak_checks.md (LEAK-41), metrics.md (MET-2, MET-11), cleaning_features.md (CLEAN-14).

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate, rebuttal: pricing_game_2016_french_fleet (exposure re-review, 2026-11-06, full tier)**

The critic and I agree on the verdict: ship after changes, not exclusion. We also agree that D11's target, weight and features hold. I concede five of the six points in full. On point 2 I concede the remedy and dispute only how much weight one estimate carries. On point 4 I concede both remedies and dispute only the effect claim and the strength of the issue.

1. The windows share one training side (SPLIT-14). Conceded.
   - The three splits have identical training indices (56,178 rows), and SPLIT-14 (Must) as written counts that as one evaluation.
   - No higher Must forces option A, because C meets both LEAK-41 and SPLIT-14 (principles, How to decide 4).
   - Issue 6's spanish "below the floor" bullet is false: spanish's valid window holds 52.5% of the rows.
   - SPLIT-8 narrows USE-10, and the measured cost of C is small: +0.005 (SD 0.022) paired, about 0.004 for the cold start of a new fleet. That answers the practitioner's USE-10 objection, as I already said in my point 5.
   - What follows: re-split to C (ForcedGroupedFromTemporal by `contract_id`, which stays the group column and is never a feature; the SPLIT-10 exception dropped). Before C ships, run SPLIT-8's leak test across the grouped split and the leak probes, the wisconsin way: the test year's training rows in and out.
   - A or B only by a deliberate amendment of SPLIT-14, decided together with wisconsin issue 3, never by an exception.
   - I withdraw my preference for A. Its only support is fidelity to the use case (USE-10, SPLIT-12), and the measurements show C costs that fidelity almost nothing.

2. The source's 30-day floor selects rows by their realized length (LEAK-41, last clause). Remedy conceded, one effect estimate disputed.
   - Conceded: a Must has no exceptions, so "accept it as the source's population" has to be recorded the way the critic says. That is a curator ruling written as an amendment of LEAK-41's last clause:
     - the amendment: a selection the source made uniformly on both sides, which cannot be undone, defines the population (USE-7) and is sized in the notes;
     - its reach: frempl and any sibling with a minimum length;
     - the anomaly bullet rewritten as a LEAK-41 note.
   - In my opening I called it a note plus acceptance. The amendment is the correct form.
   - Disputed: how much the "about 11% of the newest window's vehicle-years" figure can carry.
     - It is the claim auditor's own "rough" extrapolation, and it assumes a flat density below 30 days. The column auditor's estimate is about 1.5% of vehicle-years overall.
     - The left-out periods are at most about 0.08 vehicle-years each (under 30 days), so their weight in a vehicle-year-weighted fit and Gini is small even where their count is large.
     - It does count for C in issue 6, as the critic says, but only as a supporting line. It does not change any verdict.

3. Probe 22's cited evidence has no power. Conceded.
   - probe22.txt and probe22_l2.txt are both the L2 arm. In that arm the realized weight itself gains -0.0014 (SD 0.052), so the probe could not have flagged a proxy.
   - LEAK-41 asks for both arms and a decision on the worse. The conclusion stands on the claim auditor's Tweedie arm: the weight as a feature +0.0118 (SD 0.0067), every weight-mediated gain under 1 SD.
   - What follows: re-run probe 22 with the weighted Tweedie objective, and cite both arms in the Exposure bullet and in REVIEW issue 5.

4. The stand-in metric's reason (MET-11, MET-2). Both remedies conceded; the effect claim and the strength disputed.
   - Conceded (a): the reason's "the market rewarded the ranking of the risks" is incomplete. A cheapest-wins market after a uniform rescaling rewards relative prices, and the Gini scores only their order. The practitioner's doubled-relativities GLM (Gini 0.173 for both) shows it. Reword the reason.
   - Conceded (b): MET-11 asks for the closeness "measured on the shipped splits where possible". The notes compare only the raw Tweedie deviance (89.9 against 91.2), the version that scores the 2013 level. Measuring the uniformly rescaled weighted deviance is cheap (EV-1) and belongs in the notes for the curator.
   - Disputed: "the metric changes which models win".
     - Both metrics put the GLM above the LightGBM: Gini 0.173 against 0.157 (practitioner); 0.159 / 0.171 / 0.200 against 0.114 / 0.158 / 0.190 in the notes.
     - What differs is the margin, and whether the steep tree model falls below a flat tariff (rescaled deviance 91.34 against 90.82).
     - That is a real difference in what the metric rewards. It is not a reversal between the two models measured.
   - Disputed: the strength of this issue.
     - Choosing between stand-ins is a Weigh call under MET-10, and the Gini stand-in follows australian (D8) and spanish coverage.
     - The rescaled deviance has costs the critic also names: it takes its scale from the test total (an oracle), and it is noisier on the newest window.
     - So it is a curator's call for the record. It is not a MET-11 failure that blocks shipping.

5. Stale or wrong statements in the record, the review file and CHANGES.md. Conceded in full.
   - The SPLIT-10 exception line, which still names "distinct training sides".
   - The missing SPLIT-10 Cases rows.
   - The outdated SPLIT-14 Cases row for this dataset.
   - Issue 6's spanish floor statement.
   - "Loses 0.010 (4 of 5 seeds)" and "time features add 0.007": both to be marked "within seed noise".
   - "A cut nobody scheduled", to read "a cut not known at the start, a quarter of them on a month's end".
   - CHANGES.md's option C wording.
   - All of these are text fixes with no decision. My opening's point 7 listed most of them.

6. Four band columns ship unordered (CLEAN-14, Should). Conceded.
   - Declare `contract_age_class`, `vehicle_age_class`, `deductible_class` and `insured_value_class` as ordinal, with the column auditor's level lists, and update the Dtypes bullet. It is cheap and safe, and it lands with the rebuild that C needs anyway.

Judgment record, with the critic's and my points merged:

```text
Verdict: ship after changes.
Validity: USE-1/USE-8 (direct), USE-5, LEAK-7/37 and LEAK-41 for the features and the weight hold. SPLIT-14 broken: re-split to C after SPLIT-8's leak test (A or B only by amendment, with wisconsin issue 3). LEAK-41's selection clause triggered by the source's 30-day floor: curator ruling as an amendment plus a sized note. LEAK-41 reporting: re-run probe 22 with the Tweedie arm.
Value: TP-4 holds, weakly on the newest window (1.7 SE). TP-9 holds. MET-11: reword the reason and measure the rescaled deviance's closeness; the choice of stand-in is the curator's (MET-10).
Quality: CLEAN-14 ordinal bands; the text fixes.
For the curator: the issue 6 split, the LEAK-41 amendment for source floors (family-wide), and Gini against rescaled deviance as the stand-in.
```

Sources:
- The critic's opening brief and the phase A reports of this panel.
- Rules in `.claude/skills/knowledge-curation/references/`: metrics.md (MET-10, MET-11), splits.md (SPLIT-8, SPLIT-14), leak_checks.md (LEAK-41), principles.md.
- Definition: `datasets/_dev/tabarena-v0pt2/pricing_game_2016_french_fleet/dataset.py` (lines 170-174 for the notes' metric comparison; around line 202 for the stand-in reason).

</details>

<details><summary>Critic rebuttal</summary>

**Critic's rebuttal: pricing_game_2016_french_fleet (exposure re-review, 2026-11-06)**

We agree on the verdict: ship after changes, not as defined. I concede points 1 to 4. On 5 to 7 I dispute three framings. Each would let a Must be settled with less than the rule requires. I also correct one statement of fact.

Point 1 (real task, numbers reproduce): conceded. USE-8 direct fit, target rebuilt from the source, metric implementation matches to 1e-12. I raised no point against P2 or P3.

Point 2 (no leak through the weight): conceded on the substance. The advocate concedes my point 3: probe22.txt and probe22_l2.txt are one L2 run, and that arm has no power (weight itself -0.0014, SD 0.052). The conclusion rests on the claim auditor's Tweedie arm, and we agree on the remedy. One nit: LEAK-41 requires the definition to report both arms and decide on the worse. Citing the Tweedie numbers is therefore needed for the definition to meet the rule, not an optional note fix. Fixing the text is enough; I do not ask for a definition change.

Point 3 (the training side 2011-2012 is the honest one): conceded. LEAK-41 (Must) outranks SPLIT-11 (Should). The 0.127 / 0.131 against 0.115 / 0.116 measurement and the hotel_booking_demand precedent carry it.

Point 4 (worth benchmarking): conceded. TP-4 and TP-9 hold: 103 / 232 / 1,026 positive charges, every window above the constant. The newest window clears the constant by only 1.7 SE, yet option A gives it a third of the score. That weighs on issue 6 (my point 1), not on whether the dataset is worth benchmarking.

Point 5 (SPLIT-14): I concede that the defined state breaks a Must and that C is the fix within the rules. I dispute two framings.
- (a) The advocate presents A-by-amendment and C as two equal paths ("either way the dataset ships; the only open question is which split"). They are not equal.
  - principles.md: "A Must has no exceptions: only a higher-ranked Must overrides it, and anything else is an amendment".
  - The amendment issue 6 drafts would reach only this dataset. Spanish coverage and pg17 have no dates within a year, and frempl has a single year (precedent checker, Decision 4). An amendment written to fit one dataset works as an exception to a Must, which the rule bars.
  - It would also reverse Andrej's 2026-11-02 amendment, written on this very dataset, and Lennart's 2026-11-05 reframing. That is consistency case 3, drift of the same curator on the same rule.
  - So C is the remedy the rules give. A is open only as a change to SPLIT-14 for the whole family, decided with wisconsin issue 3, with the reasoning written as a general rule.
- (b) The advocate cites USE-10 as a "Must, Part 2" behind the practitioner's B > A > C ranking. SPLIT-8 is a Must that "narrows SPLIT-7, SPLIT-14 and USE-10", so within its scope USE-10 does not decide the regime. The advocate's own number agrees: the cold-start cost of C is about 0.004 (split auditor).
- We agree on the precondition: SPLIT-8's leak test across the contract folds, plus probes/group.txt, must run before C ships. The flat claims per vehicle-year (0.117 / 0.119 / 0.119) make a pass likely, but likely is not measured (EV-1).

Point 6 (the source's 30-day floor): I concede the facts and that exclusion is wrong. I dispute the remedy.
- The advocate's remedy is "a LEAK-41 note ... the curator accepts it as the source's population". Keeping a departure with a note is the exception route, and the exception route exists only for Should rules. LEAK-41 is a Must: "No model is trained or scored on rows selected by the realized weight". The rows here were selected by realized length.
- A curator's acceptance has to take the form of an amendment of LEAK-41's last clause, for example: "a selection the source made before release, the same in train and test, that cannot be undone, defines the population (USE-7) and is sized per window in the notes". It is recorded in leak_checks.md with this case.
- It applies equally to frempl and to any sibling with a minimum length. Otherwise the next dataset with a source-side floor gets decided without a rule.
- "The same on both sides" holds for train against test, not across windows. The claim auditor estimates about 11% of the Sep-Dec window's vehicle-years removed against about 1.6% for Jan-Apr. The advocate accepts this as input to issue 6. It is one more reason for C or for pooling, not for A.

Point 7 (the rest is quality): I concede CLEAN-14 (my point 6) and the text fixes (my point 5). I dispute the metric framing and correct one fact.
- (a) The metric. The advocate files the Gini under MET-10 (Weigh). MET-10 weighs "a borderline call between the source's metric and the fallback". That is not this case. Here the source's metric, the market, cannot be computed, so this is a stand-in under MET-11, a Must. MET-11 says "the closest computable metric replaces it ... the closeness is measured on the shipped splits where possible".
  - The practitioner measured where the two candidates part ways. The Gini gives 0.173 to a tariff and to the same tariff with doubled relativities. The uniformly rescaled weighted Tweedie deviance gives GLM 89.63, GLM doubled 94.27, LightGBM 91.34, constant 90.82, and the game applied the same uniform rescaling.
  - So whether the Gini is the closest computable stand-in has been put in doubt by a measurement and not settled. Rewording the reason is necessary but not sufficient.
  - My remedy stays mild: reword the reason, report the rescaled deviance against the Gini on the shipped windows, and give the curator the choice under MET-11 / MET-4. I do not ask to switch the metric unilaterally. The D8 and spanish coverage precedents chose the Gini on the family call. Neither measured closeness to a market that rescaled uniformly, which is the fact that sets this case apart.
- (b) Correction of fact. The advocate says "Dropping n_vehicles and insured_value_class was settled (D4, CLEAN-5)". Both ship as features. `n_vehicles` is kept as the source ships it (D4; column auditor: "fine (settled D4)"). `insured_value_class` is kept with "ND" made missing on 87,093 rows (column auditor; CLEAN-10). The settled call is to keep them, not to drop them. This changes no verdict.

Where we stand:
- Agreed: ship after changes. Re-split by SPLIT-8 (C) once its leak test passes. Cite both arms of probe 22. Rewrite the 30-day floor as a LEAK-41 matter. CLEAN-14 retype. Text fixes.
- Disputed, for the mediator:
  - (i) Whether A is a symmetric option. I say it is an amendment of a Must for the whole family, with C the rule's own remedy.
  - (ii) Whether the 30-day floor can be "accepted" by a note. I say it needs an amendment of LEAK-41's last clause.
  - (iii) Whether the stand-in metric is a MET-10 weighing call or a MET-11 Must that needs its closeness measured. I say MET-11.

Sources:
- The advocate's opening brief and the phase A reports of this panel.
- Rules in `.claude/skills/knowledge-curation/references/`: principles.md (Exceptions and amendments), splits.md (SPLIT-8, SPLIT-14), leak_checks.md (LEAK-41), metrics.md (MET-10, MET-11).

</details>
