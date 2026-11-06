# pricing_game_2016_french_fleet

**Outcome:** added. Shipped (the curator's verdict of 2026-11-02). Settled on 2026-11-02: the `exposure` fix, the expanding windows
(SPLIT-11; SPLIT-14 amended so that windows sharing one train side count as one) with no gap (an exception to
SPLIT-10), and the switch of the target to the claim charge per period (issue 4).
The organisers' own files of the 2016 actuarial pricing game: 87,228 periods of cover of fleet vehicles of a French
insurer, 2011-2013; the target is the period's claim charges summed, net IDA recoveries set to 0 (0 for 95.7% of the
periods); the features are the rating classes and the length of cover known at the period's start; three four-month
windows of 2013, each trained on every period closed before it starts; scored by the normalized Gini as a stand-in for
the game's market, as in pricing_game_2017_french_mtpl. Validity: SEL-1, SEL-2, USE-1 (fit direct), LEAK-10 (fixed by
LEAK-7), SPLIT-1, SPLIT-9, SPLIT-11, SPLIT-13, SPLIT-14 hold; SPLIT-10 departed from (exception); SPLIT-15 departed from
(three windows, not nine). Value: TP-4 holds (a Tweedie GLM 0.167 / 0.270 / 0.268 against 0.101 / 0.150 / 0.066 for the
length alone; on the newest window by about one standard error), TP-9 holds (103 / 232 / 1,026 positive charges); the
task probes' `no_signal` reads R^2 on a heavy tail, as for pricing_game_2017_french_mtpl. Weighed: the original files
+, a real pricing task +, the family's only commercial-fleet damage table +; weak, anonymised covariates -, a noisy
newest window -.

Changes made after the review panel (AI, 2026-11-01 and 2026-11-02): `exposure` is the length of cover to 31 December
for every period; the metric is a stand-in for the game's market; the statements the claim audit refuted are
corrected; the windows train on an expanding side; the target is the claim charge, not the claim indicator; every
window figure is re-measured. The panel's sections describe the definition before these changes.

**Main points:** Nothing open; every issue below is resolved (2, 3, 4), and issue 1, the `exposure` fix, is in the record.

**Issues for Andrej:**

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

**Review panel:** ship after changes (mediator). Claim audit: 48 claims, 39 hold, 7 refuted (5 fixed in the definition:
the length called known at the start, the test that could not fail, Decision 1 and the metric origin; 2 record fields
for the hand-over), 2 untested. Blind review: include with changes; main concerns the windows against the cut at 31
December and an `exposure` partly known only after the fact. Debate: agreed on the `exposure` fix (the advocate withdrew
its keep in rebuttal), the windows with their notes, the stand-in origin and the text; nothing left disputed between the
two; for the curator: the `exposure` fix with frempl (issue 1), the first SPLIT-14 reading (issue 2) and training
without a gap (issue 3; the SPLIT-10 amendment is avito_demand_prediction_1m's issue 4).

<details><summary>Mediator</summary>

**Mediator (2026-11-01): pricing_game_2016_french_fleet**

**Recommendation**

```text
Verdict: ship after changes.
Validity: SEL-1, SEL-2 hold; USE-1 holds, fit direct (USE-8); USE-3 triggered (the realised length called known at
  the start), fixed in the text; LEAK-10 triggered by `exposure` (the realised length: 57.4% of periods end early at
  a cut nobody scheduled), fixed by LEAK-7 (the length known at the start); SPLIT-1, SPLIT-3, SPLIT-9, SPLIT-13 hold;
  SPLIT-14 met in letter by three windows on one train side, a first case (issue 2), with an exception to SPLIT-11
  (annual refit); SPLIT-10 departed from, its third exception for SPLIT-14's floor (issue 3); PROV-3, PROV-8, PROV-9
  hold; PROV-15 noted (CASdatasets' DirectComp).
Value: TP-2, a small real signal (keep); TP-4 holds after the fix (covariates 0.594 / 0.622 / 0.653 against
  0.551 / 0.567 / 0.531 for the start-known length alone); TP-9 holds (123 / 257 / 1,163 positives); MET-8 value
  `roc_auc` kept; MET-11 origin triggered, fixed (`stand_in`, as pricing_game_2017_french_mtpl).
Quality: CLEAN-3, CLEAN-5, CLEAN-10, CLEAN-12, CLEAN-14 hold; LEAK-18 repeated rows natural; text facts corrected.
Weighed: the organisers' original files +, a real pricing task +, the family's only commercial-fleet damage table +;
  weak and anonymised covariates -, a GLM ties LightGBM -.
For the curator: issue 1, confirm the `exposure` fix with frempl's issue 2 (or amend LEAK-10 for the family);
  issue 2, a first reading of SPLIT-14; issue 3, the third SPLIT-10 exception or an amendment.
```

The advocate withdrew its keep of the realised `exposure` in rebuttal, so the debate ends with no open dispute between
the two sides. What remains for the curator are a confirmation tied to a pending decision on a sibling (issue 1), a
first-case reading of a Must (issue 2) and a rule-maintenance call (issue 3).

**Agreed facts**

*Data and target*
- The definition reads the organisers' own 2016 files (sha256 pinned; Wayback copy byte-identical). The counts are
  87,228 periods, 68,485 vehicles, 18,037 contracts, 2011-2013, and every claim joins one period. The data is not
  generated (the curator's test, CC 2026-11-01). All 39 claims the claim audit could check against the files hold to
  the digit.
- The portfolio is commercial fleets under a material-damage cover (rules Sec. 1), not CASdatasets' "private motor".
  CASdatasets' DirectComp is 0 on 1,064 of the 1,190 IDA claims (a problem of that copy, PROV-15).
- Target `claim`: 4,250 positives (4.9%), 286 periods with 2-7 claims, 523 periods with only IDA claims. The curator
  chose this binary target (CC 2026-10-30). Under IRSA the insurer recovers a flat amount, not the cost, and 126 IDA
  claims are at 50% responsibility.

*`exposure`*
- `exposure` is the realised length. 41.8% of periods end on 31 December, 0.8% at a contract anniversary, and 57.4%
  (58.2% in 2013) at a cut nobody scheduled.
- The realised length adds ROC AUC +0.040 / +0.055 / +0.052 over the start-known length, which adds 0.000 (LightGBM,
  3 seeds, shipped windows).
- Early ends go with claims: rate ratio 1.22 [1.12, 1.33] given the start-known covariates in 2011-2012, and 1.175
  [1.05, 1.31] in 2013.
- The definition's "31 December flag" test could not fail: the flag is fixed by start and length on 99.5% of rows. The
  AUC test of the outcome link resolves about ±0.0013, so "no gain" does not mean "no link" (critic).
- The gain is the time at risk itself: where the end carries no information on claims, a simulation gives +0.050
  against +0.049 observed (advocate). It is still time at risk not known at pricing.
- After the fix: LightGBM 0.594 / 0.622 / 0.653 (mean 0.623, against 0.672 before).

*Split*
- Train side: 56,178 periods (64.4%), every one ending by 31 December 2012. Windows: 5,312 / 6,509 / 19,229 rows with
  123 / 257 / 1,163 positives.
- 76-81% of test periods have their contract in training; the game's own 2014 file has 82%.
- On the 2013 rows, the IID, grouped and temporal designs agree within 0.003.
- The per-window mean (LightGBM 0.672) sits below the pooled 2013 score (0.712) because windows are cohorts of period
  length. The newest window has an SE of about 0.027.
- Any gap on the train side breaks SPLIT-14's floor (1 day: 50.2% of rows; 1 month: 48.7%). Simulated reporting delays
  of 30 and 90 days move the mean AUC by 0.003 or less; a planning gap (fit on 1 October 2012) gives 0.671 against
  0.672.

*Metric*
- The game scored a price-aggregator market: each insured drawn among the cheapest premiums, every player's premiums
  scaled by a uniform factor to a total of 2.5 million euros (rules Sec. 4: "par un facteur d'inflation appliqué
  uniformément").
- The market needs the other players' premiums and the 2014 claims, neither published.
- pricing_game_2017_french_mtpl declares its market as `stand_in`.

*Text facts*
- The 2,099 "0.01 less" lengths are 2012 periods measured over 366 days.
- The row names of the train and test files run exactly from 1 to 120,000, so the file is likely a sample, and "up to
  12 vehicles" and "42.8% ... no later period" count the file, not the fleet.
- The newest claims are not censored (0.117 / 0.119 / 0.119 claims per vehicle-year).

*Mediator checks* (scripts in the run folder, thread caps, same LightGBM settings as the claim audit):
- `m1_anniversary`: the agreed fix reads an anniversary cut from the vehicle's next period, which exists only if the
  vehicle stays. That reading carries nothing measurable:
  - covariates and day of year score 0.6231;
  - with the agreed start-known length, 0.6229;
  - with a variant that locates the anniversary from the contract alone, 0.6244 (the two lengths differ on 2.6% of
    periods).

  The agreed form stands.
- `m2_retention`: what the fixed task scores. The target still counts claims over the cover actually earned, so a
  model told only the scheduled length can also gain by guessing how long a vehicle stays. The rating classes rank the
  unscheduled early ends at AUC 0.78 / 0.77 / 0.82. Window means:
  - the actuary's rate times the scheduled length: 0.610;
  - the direct post-fix model: 0.623;
  - the rate times a predicted stay: 0.629;
  - the rate times the realised length: 0.670.

  About a tenth of the post-fix skill above chance is the stay. Before the fix, more than a quarter was time at risk
  unknown at the start. The stay is an expectation at the prediction point, not a leak.

**Changes to make now (no decision needed)**

1. LEAK-10 (Must), fixed by LEAK-7 (Should): `exposure` becomes the length known at the start.
   - Every period that ends before 31 December gets (31 Dec - start + 1) / 365 (/366 in 2012).
   - Periods that end at a contract anniversary (the vehicle's next period starts the next day with a higher contract-age
     class; 0.8%) keep their realised length.
   - The two rows with `n_vehicles` = 2 keep vehicle-years.
   - Drop the "Potential leak, kept on purpose" label. In its place, say what was fixed and why: the realised length
     added +0.040 to +0.055, and early ends have a rate ratio of 1.22.
   - Re-run TP-4, the task probes and every window figure in the notes. Issue 1 asks the curator to confirm the fix.
2. USE-3 (Must): `task_summary.known`, `question` and the first bullet name "the length of cover to the year's end (or
   to the contract's anniversary), known at the start".
3. USE-8 (Must), EV-6:
   - `fit_reason` loses "measured to add no signal". It says the target counts claims over the cover actually earned,
     so the chance includes how long the vehicle stays (m2). Fit stays direct.
   - Decision 1 is retitled. Its table shows claims per vehicle-year by how the period ends (0.111 / 0.111 / 0.137 in
     2011-2012) in place of claim shares within length bands.
4. MET-11 (Must): `Metric.stand_in("roc_auc", original=<the 2014 price-aggregator market, rules Sec. 4>, ...)`, with
   `reference` set to the rules PDF. The reason adds:
   - the uniform scaling of every player's premiums, which removes the price level and leaves the ranking of risks;
   - ROC AUC = (normalized Gini + 1) / 2 on a binary target, the 2017 sibling's stand-in;
   - how much of the score the scheduled length carries after the fix.
5. USE-5 (Must) wording: `predicted` and the IDA bullet say "the insurer pays its client and recovers a flat amount
   from the other insurer", and that 126 IDA claims are at 50% responsibility.
6. EV-2 text facts:
   - the leap-year clause;
   - "up to 12 vehicles" and "42.8%" are counts of a likely sample; give the 57.4% (58.2% in 2013) of periods that end
     early at an unscheduled cut;
   - the target bullet's reason names this table's own facts (charges scaled by one constant, a short unexplained tail,
     537 net-negative IDA periods; precedent check, item 1).
7. P4 text in `splits_comment`:
   - cite SPLIT-15, not SPLIT-17;
   - say that window scores rank within start cohorts and that the newest window is the smallest and noisiest;
   - "suggested on 2026-10-30, accepted with the curator's Yes" in place of "the call of 2026-10-30";
   - the note's "cannot be measured" becomes the simulated bound, called a simulation.
8. Checks: `accepted_check_warnings` for `dataset_duplicate_rows`, `meta_time_horizon_mismatch` and
   `meta_license_unknown`, each with its reason (precedents in the precedent check, item 7).
9. Record at hand-over (records.md, PROV-8):
   - `name` and `source_links` point to the organisers' files, with CASdatasets named as a copy;
   - add `v2_path`;
   - drop the `Two-Regime Zeros` tag. The curator's definition (policy question 4) needs a low value in a continuous
     target, so it cannot apply to a binary one;
   - `problem_type` goes through the field row.
10. Optional, USE-6 context: one clause that most contracts are small (median 2 vehicles per contract-year, 18% with 4
    or more). Larger fleets are experience-rated in practice, and last year's claims were measured to add nothing.

**Changes that need the curator** (ranked; full text in the review draft)

1. P4, LEAK-10 (Must): confirm the fix, decided with frempl_french_motor_personal_line's issue 2. The alternative is an
   amendment of LEAK-10 for time at risk in insurance tables, which reaches frempl, spanish coverage, australian and
   fremtpl2 together.
2. P4, SPLIT-14 (Must): is a set of three windows inside one dated test year, all on one train side, a valid set of
   SPLIT-14 windows? If so, the exception to SPLIT-11 (annual refit) is recorded with it. The alternative is SPLIT-8,
   forced grouped by contract, which meets your how_much_did_it_rain call (frempl issue 5, australian issue 1).
3. P4, SPLIT-10 (Should): no gap. Record a third exception for SPLIT-14's floor, or amend SPLIT-10 (the precedent
   check's prompt C).

**Disputed points**

- **D1. `exposure`, realised or known at the start.**
  - The two positions: the advocate (opening) would keep it by an amendment, resting on P3 and USE-5 and on actuarial
    practice (an offset; fleet premiums revised on earned vehicle-years). The critic would fix it, resting on LEAK-10
    (Must) and its clause of 2026-10-26.
  - Not a conflict. USE-5 governs the target, which the fix leaves alone. The practice supports the time at risk in the
    scoring (MET-2), not as an input known at pricing. So LEAK-10 has to hold on its own (principles, step 4).
  - A Must takes no exception, and the mildest remedy that resolves it is the definition fix (LEAK-7).
  - The advocate conceded in rebuttal, so the point is agreed. It still goes to the curator because a decision on a
    sibling (frempl issue 2) would carry over here.
- **D2. Window design: pooled or exposure-weighted (practitioner), year-aligned or half-year windows (blind reviewer).**
  - Pooling 2013 is one window. A 2011 train side for a 2012 window holds 30.4% of rows. Both break SPLIT-14 (Must,
    P4).
  - The scoring unit is P6, and P4 outranks it ("the metric never changes the split against the use case", MET-2).
  - Settled: keep the shipped windows and add the cohort note (change 7).
- **D3. The metric's value: `log_loss` as context (practitioner) or `roc_auc`.**
  - Both debaters left this to the curator as a weighing call (MET-10). The rules settle it.
  - Under MET-11 a stand-in is the closest computable metric to the original. The game rescaled every player's
    premiums by one factor to the same total, so its market did not reward the price level, which is the
    practitioner's reason for log loss. It rewarded the ranking of risks.
  - ROC AUC scores that ranking (the normalized Gini identity), as in pricing_game_2017_french_mtpl and porto_seguro.
  - Settled: `roc_auc` stays, no issue.
- **D4. Drop `n_vehicles`, and drop `insured_value_class` or encode its "ND" as a level (blind reviewer).**
  - CLEAN-5 covers constants only. "ND" marks no single formula, so missing is right (CLEAN-10; column audit).
  - Quality, no change.
- **D5. The binary target is broad and its reason is not pg16-specific (blind reviewer, precedent check).**
  - The curator decided it (CC 2026-10-30). Only the reason text changes (change 6).

**Consistency with precedent** (precedent check)

- `exposure`:
  - Follows frempl (fix pending, its issue 2) and spanish_motor_insurance_coverage_level_2022_2024 (located
    cancellations reset).
  - Departs from fremtpl2 (CC, Andrej, 2026-10-20). Two facts set this case apart: the dates locate every early end
    here, and LEAK-10's located-values clause (Lennart, 2026-10-26) is newer than that call.
  - The 2026-10-30 policy row ("exposure: feature") still holds: the length known at pricing is a feature.
  - australian keeps under LEAK-11 because its late part lowers the score; here the late part raises it. Prompt A is
    answered with its option (b), and the confirmation is issue 1.
- Metric: `stand_in` follows pricing_game_2017_french_mtpl and this record's suggested call of 2026-10-30 (prompt B
  (b)). A label change; no score moves.
- Split, regime: the precedents with one valid annual window went to SPLIT-8. Daily start dates set this case apart:
  SPLIT-8 applies only when the release cannot give SPLIT-14's windows. Three windows on one train side have no
  precedent, so this becomes the first Cases row under SPLIT-14 once decided (issue 2).
- Split, refit: the fixed train side is a first exception to SPLIT-11 (annual refit, SPLIT-12 and SPLIT-19).
  spanish_motor_insurance_2015_2018 grows monthly because its source prices new business monthly; each follows its
  source.
- SPLIT-10: the third exception for SPLIT-14's floor after alfa_battle_2_0_task_2 and lending_club (Lennart,
  2026-10-21), with spanish 2015-2018 and wisconsin proposing the same. Principles ask for an amendment (issue 3).
- Columns, repeated rows, the IDA count, provenance and the warnings follow their precedents.
- No drift and no precedent that contradicts a rule.

</details>

<details><summary>Claim audit</summary>

**Claim audit: pricing_game_2016_french_fleet (claim-auditor, 2026-11-01)**

**Verdict:** 48 claims tested. 39 hold, 7 are refuted and 2 are untested. Every count, share and probe number in the definition matches the organisers' files to the last digit (sha256 matches the definition). Two refutations matter. (1) P4: the length (`exposure`) is not known at the prediction point, and the evidence the definition gives that it adds nothing is a test that could not have failed. Measured properly, the part of the length the insurer cannot know at the start adds ROC AUC +0.040 to +0.055. (2) P6, MET-11: the metric origin says the source defined no metric. It did: a price-aggregator market, which the 2017 sibling declares as a `stand_in` original. The other refutations are wording and stale record fields.

Scripts and outputs: six scripts, each with its output, in the run folder. The models are LightGBM with the builder's regularised parameters, 3 seeds, scored on the shipped windows, newest first.

**Claims table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | Fleet vehicles, material-damage claims | task_summary.question | rules PDF Sec. 1; pricingame.Rd | holds | rules: "Mode de gestion de la flotte", "Taille de la flotte", "garantie DTA"; Rd l.35 "all kinds of material damages" (Rd l.33 also says "private motor insurance") | USE-1, EV-2 |
| 2 | The task is the frequency part of the pure premium, per vehicle and period | task_summary.use_case | count multi-claim periods | holds (weigh) | the binary target merges 286 multi-claim periods (318 extra claims, 7% of 4,568); a rate per vehicle-year would be the strict frequency | USE-5 |
| 3 | 87,228 periods, 68,485 vehicles, 18,037 contracts, 2011-2013, cut at the year's end | task_summary.row | raw counts; periods crossing a year | holds | exact counts; 0 periods cross a year, in train and in the 2014 file | PROV-1 |
| 4 | 4.9% positive, IDA (not-at-fault) claims included | task_summary.predicted | raw | holds | 4,250 positive (0.0487); 1,190 IDA claims; 1,156 periods with an IDA claim | USE-5 |
| 5 | "Known at prediction time: ... the period's start date and its length" | task_summary.known (README "Known at prediction time") | does the period end on its scheduled date (31 Dec, or a contract anniversary: next period contiguous with a higher contract-age class)? | **refuted** | 57.4% of periods end before 31 Dec at a cut that is not scheduled (only 0.8% end at an anniversary); in the 2013 test year 58.2% end early. Their length is known only at their end, as the curation note itself says | LEAK-1, LEAK-10, USE-8 |
| 6 | Trained on 2011-12, tested in three 4-month windows of 2013; most fleets insured before | task_summary.split | shipped splits | holds | train 56,178 rows (last start 2012-12-02); 76-81% of test periods belong to a contract seen in training | SPLIT-13 |
| 7 | Changes: indicator only, identifiers, year and end dropped, ND made missing, two code sets relabelled | task_summary.changes | read `_clean` | holds | code matches; asserts pass in `dataset check` | CLEAN-1 |
| 8 | Fit direct; the length is "measured to add no signal beyond the length" | task_summary.fit / fit_reason | see #17 | fit holds; **"measured to add no signal" refuted** | USE-8 keeps a leak kept on purpose out of the fit (kick, +0.066), so "direct" can stand. But the sentence's evidence cannot support it (#17), and the right test gives +0.040 to +0.055 | USE-8, EV-6 |
| 9 | The game priced 32,772 periods of 2014 (the rules write 37,772) | curation_comments, prediction point | rules p.3; test file row count | holds | rules: "les 37 772 contrats"; test_contrats.csv has 32,772 rows | EV-2 |
| 10 | Page dated 17 July 2016; files Last-Modified 13 July 2016 | curation_comments, source | WebFetch of the page; `curl -I` | holds | page "17/07/2016", "entre le 15 juillet et le 15 septembre"; Last-Modified Wed, 13 Jul 2016 21:05:46 GMT | PROV-9 |
| 11 | CASdatasets has the same values, levels renamed one to one; its DirectComp is 0 on 1,064 of the 1,190 IDA claims | curation_comments, source | compare_orig_cas; recount | holds | IDA=1 with DirectComp FALSE: 1,064; DirectComp TRUE: 126; no false positive | PROV-15 |
| 12 | Commercial fleets; 1,190 of 4,568 claims are IDA; up to 12 vehicles at once | curation_comments, portfolio | count concurrent vehicles per contract | holds | at most 12 at once (median 2, p99 7); at most 30 distinct per contract-year, 47 over 3 years | EV-2 |
| 13 | Target = count > 0; 286 periods with 2 or more claims, at most 7; each claim joins one period; count = joined claims | curation_comments, target | raw join | holds | exact; asserted in `_load_raw` | LEAK-4 |
| 14 | The 523 positive periods without a positive charge are IDA claims | curation_comments | non-positive charges by IDA flag | holds | all 599 claims with charge ≤ 0 are IDA; all 523 periods have only IDA claims | USE-5 |
| 15 | `exposure` = (end - start + 1)/365 rounded for 97.6% of periods, 0.01 less for the rest | curation_comments, potential leak | recompute | holds; explanation missing | the 2,099 rows "0.01 less" are all from 2012, the leap year: days/366 matches 99.99% of 2012 rows. The 2014 file matches days/365 on 100% | CLEAN-1 (P7) |
| 16 | 42.8% of periods end before 31 Dec with no later period of the vehicle | curation_comments, potential leak | recompute | holds | 0.4276. Detail: in 27.5% of these (2011-12) a new vehicle id starts in the same contract the next day (0.4% at 31 days, the baseline), so some are replacements, not departures | EV-1 |
| 17 | "the end carries no signal beyond the length" (LightGBM 0.675 length alone, 0.670 with a 31-Dec flag; 0.708 on all features with or without the flag and the start's day of year) | curation_comments, potential leak; Decision 1 | (a) is the test able to fail? (b) the decisive test: covariates + start ± realised length, and ± the length known at the start | numbers hold; **conclusion refuted** | (a) Once the start is in the model, "ends 31 Dec" is a function of start and length on 99.5% of rows, so adding the flag could not change the score. history_probe ran the flag only together with the day of year, not "with or without" it. (b) Covariates + day of year: 0.5954 / 0.6218 / 0.6519 (mean 0.623). Adding the length known at the start changes nothing: 0.594 / 0.622 / 0.653. Adding the realised length: 0.6353 / 0.6763 / 0.7034 (mean 0.672), i.e. +0.040 / +0.055 / +0.052, about a quarter to a third of the skill above chance | LEAK-10, EV-1, EV-6 |
| 18 | Length alone 0.596/0.655/0.659; logistic 0.615/0.670/0.699; LightGBM 0.635/0.676/0.704 | curation_comments, TP-4 | re-run on the shipped windows | holds | 0.5963/0.6552/0.6590; LightGBM 0.6342/0.6755/0.7042 | TP-4 |
| 19 | Task probes: no flag; linear best at 0.661; the length chosen as the single feature on 3 of 3 windows, 0.629 | curation_comments | probes/task summary | holds | skill +0.323 (= 2 x 0.661 - 1), no flags | TP-1 |
| 20 | Previous-year history adds nothing (0.705 vs 0.708); vehicles in force at the start add nothing (0.708 both) | curation_comments, not added | history_probe, explore4 | holds; qualified | 0.7053 vs 0.708; 0.7083 vs 0.7082. Vehicle history is thin by construction: only 18.4% of the vehicles in force on 31 Dec keep their id in the next year, although the renewed contracts keep their size (1.83 → 1.82 vehicles); 17.6% of 2013 rows have vehicle history | USE-10 |
| 21 | `contract_id` follows subscription order (median 14,885 at most 1 year, 2,027 over 5 years) | curation_comments, dropped | median id by contract-age class | holds | exact, monotone across the six classes | LEAK-10 |
| 22 | ND on 87,093 rows (99.8%); five classes on the other 135 | curation_comments | value counts | holds | 56 + 31 + 30 + 15 + 3 = 135 | CLEAN |
| 23 | A/S/T = annual/semi-annual/quarterly; 2 = new company | curation_comments, labels | rules; CAS mapping | holds | rules "à 2 si création"; CAS maps the same codes one to one (year/semester/quarter; 2 = Yes) | CLEAN |
| 24 | Power-value class has 11 levels and no order; `n_vehicles` is 1 except on 2 rows | curation_comments, dtypes | value counts | holds | 11 levels; 87,226 rows at 1 and 2 at 2 | CLEAN |
| 25 | 9,373 rows (10.7%) repeat another row's features (8,577 with the same label, 796 with the other); natural, as fleet vehicles share every class | curation_comments; warning `dataset_duplicate_rows` | group the duplicate sets by contract | holds | 9,373 / 8,577 / 796 sets with both labels; 92.2% of the 7,446 sets fall within one contract (1,430 rows are in sets spanning contracts, coincident classes) | LEAK-18 |
| 26 | No period is shorter than 30 days, in either file; no period starts after 2 Dec | curation_comments, anomaly | raw | holds | minimum 30 days (0.08) in both files; latest start 12-02 | PROV |
| 27 | Levels anonymised, charges scaled by one constant | curation_comments, anomaly; record 11-01 | charges / 1.077841 | holds | 6.0% of charges are whole euros at tolerance 1e-3 (the record says 6.1%); piles at 130 (68), 150 (23), 2,200 (11), 1,000 (3) | PROV-3 |
| 28 | The newest periods lose no claims: 0.117/0.119/0.119 per vehicle-year, 0.115/0.114/0.117 for Q4 ends | curation_comments | recompute | holds | 0.1171/0.1194/0.1189; 0.1154/0.1139/0.1173 | LEAK-24 |
| 29 | Claims closed up to 2014, 41 still open; late reporting cannot be measured | curation_comments, note | ANNEE_CLOTURE | counts hold; lag **untested** | 41 with value 0; the latest closure year is 2014. The files hold no report date | LEAK-12, EV-7 |
| 30 | Train 56,178 (64%); windows of 5,312 (123), 6,509 (257) and 19,229 (1,163); 12,028 start on 1 Jan | splits_comment | shipped splits | holds | exact; train share 0.644 | SPLIT-14 |
| 31 | 2013 periods closed before a window start carry 2.4% and 3.2% claims | splits_comment | recompute | holds | 5,619 at 0.0238; 11,708 at 0.0315 | SPLIT-9 |
| 32 | 76-81% of test periods belong to a contract seen in training, 23-26% to a vehicle seen in training | splits_comment | builder tp4 output; cross-check on the 2014 file | holds | 0.764/0.771/0.811 and 0.226/0.249/0.260; 82% of 2014 rows have a contract in train | SPLIT-13 |
| 33 | "finer windows only cut the same test rows into noisier pieces (SPLIT-17)" | splits_comment | SPLIT-17's trigger | partly holds | SPLIT-14 (at least 3 windows) is met. SPLIT-17's trigger is fewer than about 50 test rows per window, and here the smallest window has 5,312 rows, so that rule does not carry the choice. The real limit is positives: 123 in the newest window. Left to the split auditor | SPLIT-14, SPLIT-17 |
| 34 | The game scored a price-aggregator market (random pick among the cheapest premiums; premiums scaled to €2.5M) that needs data never published; the page and the Rd name no other metric | metric reason | rules p.3 Sec. 4; page; Rd grep; one more web search | holds | rules: "agrégateur de prix", "sélection aléatoire parmi les primes les moins chères", "égalisée à 2,5 millions d'euros". The page links no results; the Rd has no metric; the search found no published ranking | MET-1 |
| 35 | origin = fallback, "the source defines no metric" (README Metric block) | `Metric.fallback` | MET-11's origins; the sibling | **refuted** | MET-11: "stand-in: the source has a unique metric that cannot be computed on our data (inputs not published, a task we changed)". Both apply, and the reason itself names them. pricing_game_2017_french_mtpl, the same organisers' market game, declares `Metric.stand_in("normalized_gini", original=<the market profit>)` | MET-11 (Must) |
| 36 | ROC AUC is computable on every fold | MET-2 | `scorer` on a definition-backed container; random probabilities | holds | per row; 123 / 257 / 1,163 positives; scores 0.468 / 0.503 / 0.508, all finite | MET-2 |
| 37 | The metric means the same on our task | MET-2 | target and balance | holds | the target was changed (pure premium to indicator), which is the stand-in case. AUC ranks like the normalized Gini (2 AUC - 1) the sibling uses. Window balance 2.3% / 4.0% / 6.1% (shorter periods later); AUC does not depend on prevalence | MET-2, MET-9 |
| 38 | Warning `meta_time_horizon_mismatch` is benign | builder | horizon against the windows | holds | the horizon is the tariff year; all test starts fall within 12 months of the last training start | SPLIT-12 |
| 39 | Warning `meta_license_unknown`; CASdatasets is GPL (>= 2) | builder; class comment | CASdatasets DESCRIPTION | holds | "License: GPL (>= 2)"; never evidence for a verdict | EV-4 |
| 40 | No copies across the split | builder ("with the date 0.0%") | reasoning | holds, trivially | `period_start` differs by year, so no exact copy can cross the split. Recurring contracts and vehicles are by design (#32) | LEAK-17, SPLIT-13 |
| 41 | "a vehicle's last period that ends early has about the claim rate of a period that runs to the year's end, a little higher among the shortest" | Decision 1 | claims per vehicle-year by how the period ends | **refuted** | 2011-12: 0.111 (ends 31 Dec), 0.111 (ends early, vehicle goes on), 0.137 (ends early for good): +23%. By length band (all years): +23%, +26%, -1%, +20%. The decision's table compares claim shares within 3-month bands, which hides the difference. These claims also cost more: 12.0% above the 90th percentile of charges against 9.2% for 31-Dec periods | LEAK-10, EV-1 |
| 42 | Decision 2 counts (4,250; 286; 1,156 with IDA; 523 without a positive charge) | Decision 2 | recount | holds | 1,156 recounted | USE-5 |
| 43 | Screening: tables 87,228 x 22, 4,568 x 9, 32,772; up to 30 vehicles; S2 3.3 against S1 1.9; net charge negative on 537 periods, positive on 3,711 | record, screening | raw | holds | 30 = maximum per contract-year; 3.27 / 1.89; 539 periods ≤ 0 (2 at zero); 4,250 - 539 = 3,711 | EV-2 |
| 44 | Assessment of 11-01: negative IDA charges never at 100% responsibility; 41 claims open; settlement years end in 2014 | record | raw | holds | Responsabilite_IDA on negative charges: 0 (570) or 50 (27) | PROV-3 |
| 45 | Assessment of 10-30: AUC 0.69 against 0.67 for exposure alone | record | history_probe | holds | 0.708 / 0.675 on all 2013 | TP-4 |
| 46 | Front matter `problem_type: Regression`, tag `Two-Regime Zeros` | record front matter | the definition | **refuted (stale)** | the definition is binary classification on the claim indicator (CC 2026-10-30) | records.md |
| 47 | Record `name` and `source_links` name only CASdatasets | record front matter | the definition's download | **refuted (stale)** | the definition downloads the organisers' files from freakonometrics.free.fr (PROV-8); builder issue 5 | PROV-8 |
| 48 | "DTA is the usual French abbreviation of an all-accident damage cover"; ND = not available | curation_comments | rules; CAS | **untested** (reading) | the rules do not expand DTA. CAS maps ND to "Unknown" (third party). Neither changes a decision | EV-2 (rank 5), EV-7 |

Refuted rows: #5, #8 (the sentence), #17 (the conclusion), #35, #41, #46, #47. Untested: #29 (the reporting lag) and #48.

**Refuted and untested claims, ranked (principles.md: validity first, Must first)**

1. **P4, LEAK-10 (Must; the case-by-case clause of 2026-10-26) with EV-6: the realised length (#5, #8, #17, #41).**
   - The definition says the length is "known at prediction time" and "measured to add no signal beyond the length". Neither holds.
   - 57.4% of periods (58.2% in 2013) end before their scheduled end, and only 0.8% at a contract anniversary.
   - The 31-Dec flag test could not have failed: given the start and the length, the flag is fixed on 99.5% of rows.
   - The decisive comparison: the part of the length the insurer cannot know at the start adds +0.040 / +0.055 / +0.052 ROC AUC. The part it can know adds 0.000.
   - Vehicles whose cover ends early for good have 23% more claims per vehicle-year, and those claims cost more (12.0% against 9.2% above the 90th percentile). That fits some claims ending a cover, but selection fits too; without claim dates the files cannot tell them apart.
   - Against the change: the game's own 2014 pricing file gives each period's realised end and length (100% match to days/365; 58% end before 31 Dec), and frequency models take exposure as given. So keeping the column is defensible, and USE-8 keeps the fit direct, as for kick (+0.066 kept).
   - What it changes: the README states a falsehood under "Known at prediction time", and the curator would decide the exposure question on evidence that cannot discriminate.
   - **Mildest remedy:** keep `exposure` and correct the text:
     - `task_summary.known`: "the period's start; its realised length (the time at risk), known only at the period's end for 57% of periods";
     - `fit_reason` and the "Potential leak" bullet: drop the 31-Dec-flag argument and give the +0.040 to +0.055 measurement;
     - Decision 1: show claims per vehicle-year by how the period ends.
   - **The curator's alternative:** drop `exposure`. The rest still predicts at 0.597 / 0.620 / 0.653 (mean 0.623), above the length known at the start (0.549), so the task stays learnable. It gives up the time at risk a pricing model uses.
   - This answers builder draft issue 1.
2. **P6, MET-11 (Must): the metric origin (#35).**
   - The source had a unique evaluation, the aggregator market, which cannot be computed (other players' premiums and the 2014 claims were never published, and our target changed). That is MET-11's stand-in case, not "the source defines no metric".
   - The sibling pricing_game_2017_french_mtpl declares the same kind of market as `Metric.stand_in(..., original=...)`.
   - What it changes: the README's origin line is wrong, and the two siblings are declared inconsistently. The score does not change.
   - **Mildest remedy:** `Metric.stand_in("roc_auc", original="each player's result in the 2014 price-aggregator market: each insured placed at random among the cheapest premiums, every player's premiums scaled to a total of 2.5 million euros (rules, Sec. 4)", reason=...)`. Keep the current reason and add that ROC AUC ranks models as the normalized Gini does (2 AUC - 1), the 2017 sibling's stand-in.
3. **Record (process; records.md, PROV-8): stale fields (#46, #47).** `problem_type: Regression`, the `Two-Regime Zeros` tag, and a name and source links that cite only CASdatasets. Remedy: update them when the curator settles the review (builder issue 5).
4. **P4, SPLIT-17 (Should; #33): the citation does not carry the choice.** Three windows meets SPLIT-14. SPLIT-17's trigger (fewer than about 50 test rows per window) is not met. Remedy: cite the positives instead (123 in the newest window, about 30 a month) or leave the choice to the split auditor's finding. Wording only.
5. **P7, quality (#15): the "0.01 less" rows are leap-year 2012** (days/366 on 99.99% of 2012 rows). Remedy: one clause in the note.
6. **Untested (#29, #48).** No report dates ship, so the reporting lag of late-2012 claims stays a stated possible optimism. DTA and ND are readings of French usage and of CAS. Neither changes a decision.

**Not refuted but worth the curator's eye:** vehicle ids rarely survive a year end. Only 18.4% of the vehicles in force on 31 Dec keep their id in a renewed contract, although fleet sizes hold (1.83 → 1.82). When a new id appears on 1 Jan, only a third share the old vehicle's age and power class, so these look like replacements rather than re-keying. The ids are dropped and the shipped data is unaffected. It does explain why vehicle history "carries nothing" (#20): few 2013 vehicles have any.

</details>

<details><summary>Column audit</summary>

**Column audit (column-auditor, 2026-11-01): pricing_game_2016_french_fleet**

```text
Verdict: ship after a curator call on `exposure` (issue 1); the other columns are fine.
Validity: LEAK-10 triggered by `exposure`. It is the realised length, and the early end moves with the outcome
  (adjusted rate ratio 1.22). It adds no ranking out of sample beyond the time at risk, but the time at risk that
  cannot be known at the start is worth 0.04-0.05 AUC. USE-3: the prediction-point bullet and task_summary.known
  say the length is known at the start.
Value: not re-judged (TP-4 would need a re-run if exposure changes).
Quality: CLEAN rules hold. Nits: n_vehicles, the N/P codes.
For the curator: issue 1, a consistency call with frempl_french_motor_personal_line (same run, same mechanism, fixed there).
```

Frame audited: `dataset_io.from_definition` (17 columns, 87,228 rows). Codebook: the rules PDF, Sec. 1 (its text extract),
and CASdatasets' `pricingame.Rd`. Scripts and numbers: in the run folder.

**Column table**

| column | meaning (codebook) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `period_start` | "Date de début de situation" | yes: it is the prediction point | datetime; also the time index | fine. With `exposure` it gives the end date back, so dropping `period_end` does not hide the end | CLEAN-14, CLEAN-23 |
| `contract_age_class` | "Classe age du contrat" | yes. Steps up at the anniversary (19.3% of next-day cuts change it) | category, 6 French labels ("<= 1 ans" ... "> 5 ans") | fine | CLEAN-14 |
| `new_company` | "Indicateur de création entreprise (à 2 si création)" | yes. Constant per contract across all years (0.000 vary) | category No/Yes from 1/2 | fine | CLEAN-12 |
| `fleet_management` | "Mode de gestion de la flotte" (N/P, meaning not stated) | yes. Varies in 0.5% of contract-years | category N/P | fine. P fleets run to 31 Dec in 66.5% of periods against 28.7% for N, so the column ties into how lengths are realised. Labels unknown | CLEAN-14 |
| `zone` | "Zone géographique", anonymised 1-6 | yes | category | fine | CLEAN-14 |
| `fleet_size_class` | "Taille de la flotte" (Segment 1/2) | yes. Varies in 0.5% of contract-years | category | fine | CLEAN-14 |
| `payment_frequency` | "Fractionnement de paiement de la prime" | yes. Never changes within a contract across years | category annual/semi-annual/quarterly from A/S/T | fine | CLEAN-12 |
| `exposure` | "Véhicules année (exposition au risque)" | **no for 58.2% of periods**: they end before 31 Dec, and that end is unknown at the start | float, vehicle-years | **leak** (issue 1) | LEAK-10, LEAK-7 |
| `vehicle_age_class` | "Classe d'âge du véhicule" | yes. Only moves from 0-5 to >5 | category, 2 levels | fine | CLEAN-14 |
| `deductible_class` | "Classe de franchise de la garantie DTA" | yes. Changes at a cut (12.9% of contract-years), and the new value is history for the next period | category, 6 ordered labels | fine | CLEAN-14 |
| `n_vehicles` | "Nombre de véhicule" | yes | int. 1 except 2 rows (both 2012, train) | fine (nit, issue 4) | CLEAN-5 (does not strictly apply) |
| `insured_value_class` | "Valeur assurée" | yes | category; "ND" made missing (87,093 rows) | fine. Non-ND rows sit in formulas 3, 4 and 5, so ND does not mark one formula ("not applicable" for one product); missing is right | CLEAN-10 |
| `formula` | "Formule souscrite", anonymised 2-5 | yes. Varies in 6.6% of contract-years (at cuts) | category | fine | CLEAN-14 |
| `client_activity` | "Activité du client (niveau contrat)", 1-8 | yes | category | fine | CLEAN-14 |
| `distribution_channel` | "Type d'apporteur (agents ou courtiers ou autres)", 1-3 | yes. Constant per contract | category; code-to-label map not published | fine | CLEAN-14 |
| `power_value_class` | "Combiné puissance valeur du véhicule", 1-11 | yes. Constant per vehicle (99.9%) | category | fine. The codes are not in claim order (claims per vehicle-year 0.068, 0.065, 0.128 ... 0.173, 0.131, 0.062 for codes 1, 2, 3 ... 9, 10, 11), so typing it categorical is right | CLEAN-14 |
| `claim` (target) | "nombre de sinistre" > 0 | outcome | category Yes/No; IDA claims included (curator's call) | fine. The count equals the joined claims (asserted) | USE-5 |
| dropped `contract_id` | "Numéro d'affaire" | yes, but numbered in subscription order | dropped | fine. An id that encodes when the contract was opened | CLEAN-3, LEAK-10 |
| dropped `vehicle_id` | "Immatriculation", anonymised | yes | dropped | fine. Spearman 0.9994 with `contract_id`, so the same order | CLEAN-3 |
| dropped `year`, `vehicle_category` | year of the start; one value | - | dropped | fine (copy; constant) | CLEAN-5 |
| dropped `period_end` | "Date de fin de situation" | no for early ends | dropped | fine as a copy, but the end it carries is still in `exposure` (issue 1) | LEAK-10 |
| unused claims-file columns (`CHARGE_SINISTRE`, `IDA`, `Responsabilite_IDA`, `ANNEE_CLOTURE`) | per claim | no (post-outcome) | used only for the join and the Decisions | fine | LEAK-10 |

**Problems, ranked**

**1. `exposure` is the realised length, and the early end goes with the claims (P4, LEAK-10 Must; a weak leak beyond the time at risk; a curator call).**

Evidence:
- 58.2% of the periods end before 31 December. An end like that cannot be foreseen at the start:
  - 76.5% of the next-day cuts change no released column;
  - 59.8% of the early ends are shared by another vehicle of the contract on the same day (contract-wide events);
  - the rest are exits, or continuations missing from the file (issue 3).
- The early end moves with the outcome once the covariates known at the start are accounted for. I fit a Poisson GLM of
  the claim count with offset log(exposure), on every class, the start month and a 1-January flag. Early-ending
  periods have a rate ratio of:
  - 1.22 [1.12, 1.33] in 2011-2012 (p = 2e-6), and 1.18 [1.05, 1.31] in 2013;
  - 1.26 to 1.30 when the vehicle ends alone, and 1.08 to 1.18 when the end is contract-wide.
- Among the periods that start on 1 January: 0.124 claims per vehicle-year when they end early, against 0.103 for full
  years. This is the textbook mechanism: a total loss, a vehicle sold after an accident, or a contract cancelled after
  claims ends the period.
- The traced part adds no ranking out of sample, on the 3 shipped windows:
  - Poisson offset model 0.669 without and 0.668 with the early-end flag;
  - LightGBM (the builder's parameters, 3 seeds) 0.671 shipped, 0.670 with an explicit exit flag.
- The time at risk itself, which nobody knows at the start for those 58%, is worth 0.04-0.05 AUC. Giving the early ends
  the length known at the start (to 31 December) gives:
  - LightGBM 0.671 -> 0.630 when only the periods without any later period are changed, and 0.622 when every early end
    is changed;
  - logistic 0.661 -> 0.630 and 0.626;
  - the length alone 0.596/0.655/0.659 -> 0.53-0.58.
- What the definition says against this:
  - The note says "the end carries no signal beyond the length", and fit_reason says "measured to add no signal". That
    holds for ROC AUC only. The frequency effect (+22%) is there.
  - Its test "0.708 with or without the flag" cannot see the effect, because a model that has `period_start` and
    `exposure` already computes the flag.
  - The Decision table text ("about the claim rate ... a little higher among the shortest") understates it: in the
    closed years, periods that end early with no later period have 0.137 claims per vehicle-year against 0.111 for
    year-end periods.
- Consistency check (principles, case 2):
  - `frempl_french_motor_personal_line`, in this same run, met the same mechanism. Its dates locate the early ends row by
    row, and it replaced their `Exposure` by the length known at the start under LEAK-10/LEAK-7. That was an AI change
    after its panel and is still pending in its REVIEW.md.
  - `spanish_motor_insurance_coverage_level_2022_2024` gave the cancelled portfolio years a full year.
  - `fremtpl2` and `australian_vehicle_insurance_2004_2005` kept the realised value because no dates locate the ends.
  - This dataset has the dates, so it sits with frempl, unless a fact sets it apart.

Mildest remedies, for the curator:
- (a) Fix the definition (LEAK-7). Give every period that ends before 31 December its length to 31 December,
  (31 Dec - start + 1) / 365. Use every early end rather than frempl's "no continuation", because here that split does
  not tell exits from cuts (issue 3). `exposure` then follows from `period_start`, so it can be dropped. Cost 0.671 ->
  0.622, and TP-4 needs a re-run.
- (b) Keep it as a recorded exception. Name the fact that sets it apart from frempl: the game's own 2014 pricing file
  gives realised dates and lengths, and the outcome-linked part adds no AUC here. Rewrite the note with the rate ratio
  instead of "no signal". Decide frempl the same way, or say why not.

My reading: (a) follows LEAK-10 as written and the run's precedent. (b) is defensible only as an explicit exception.

**2. The prediction point says the length is known at the start (P3/P4, USE-3 Must; a wording fix).** The first
curation_comments bullet ("Known then: ... the period's start and its length") and `task_summary.known` ("the period's
start date and its length") contradict fit_reason and the potential-leak bullet ("a period cut short is known only at
its end"). Remedy: under (a), say "the length to the year's end". Under (b), say "the realised length (a potential leak
kept on purpose)" in both places.

**3. The file is probably a 120,000-row sample, so "no later period" is not an exit (P5 facts that bear on the column
claims; circumstantial, EV-6; a question for the curator).**
- The row names of `train_contrats.csv` and `test_contrats.csv` together are exactly 1 to 120,000, a round total for four
  years of a portfolio.
- 43.7% of the contract-years hold a single vehicle in the file.
- Of the vehicles that run to 31 December in a contract that is present the next year, only 25.6% (2011) and 25.2% (2012)
  appear in that next year.
- 868 vehicles skip a whole year inside their contract (gaps of 366-367 days).

So these do not show what they say, and "A contract holds up to 12 vehicles at once" counts the file, not the fleet:
- the comment's "42.8% ... end before 31 December with no later period of the vehicle";
- the Decision table's "earlier, the last" column.

Remedy: a note. The comment should give 58.2% (every early end) as the share with an unforeseen end.

**4. Nits (P7; no action needed).**
- `n_vehicles`:
  - `exposure` is in vehicle-years. The two rows with 2 vehicles have doubled lengths (61 days -> 0.33, 33 days ->
    0.18), so they are two more exceptions to the exposure formula of the comment.
  - The column is 1 in every test window.
  - Keeping it is harmless; dropping it is also fine.
- `fleet_management` N/P: the meaning is not documented. The pattern of lengths fits N = individually listed
  ("nominative") vehicles, but that is unverified, so keep the codes.
- `contract_age_class` keeps French labels. This is consistent with the comment, and optional to translate.

</details>

<details><summary>Split audit</summary>

**Split audit (split-auditor, 2026-11-01): pricing_game_2016_french_fleet**

**Verdict: right with notes.** The regime fits the use case: a temporal split over known fleets, trained on the closed years 2011-2012 and tested on 2013. It mirrors the game's own design (2011-2013 used to price 2014), and the contracts recur in about the same share as in the game's 2014 pricing file. No training row has an unknown label, there are no copies across the split, and the training history shows no break. Neither an IID split nor a grouped split would score higher than the valid test year. Four points remain, none a defect of the split:
- the curator should confirm that three sub-windows of one test year, all on one train side, count as SPLIT-14's three windows. This is the first such case, and the batch's one-window siblings went to `ForcedGroupedFromTemporal`;
- the departures from SPLIT-11 and SPLIT-10 need recording as exceptions;
- the windows are cohorts of different period lengths, so the per-window scores sit well below a pooled score for the year;
- one rule citation is wrong (SPLIT-17 for SPLIT-15).

```text
Verdict: right with notes (no re-split).
Validity: SPLIT-1, SPLIT-3, USE-10 hold (known fleets, temporal; 2013 mirrors the game's 2014 file); SPLIT-9 holds
  (every training period ends by 31 Dec 2012); SPLIT-14 met in letter (3 windows, 64.4% train), a reading for the
  curator (one train side; precedents with one annual window went to SPLIT-8); SPLIT-11 departed from (annual refit,
  SPLIT-12/SPLIT-19), exception to record; SPLIT-10 departed from (no gap), exception to record, serves SPLIT-14,
  measured bound <= 0.003; SPLIT-13 part of the task; SPLIT-20 holds (two full years, no break); SPLIT-29/30 no hit.
Value: windows hold 123 / 257 / 1,163 positives (TP-9 fine); the newest window is the noisiest (SE about 0.027).
Quality: splits_comment cites SPLIT-17 where SPLIT-15 is the rule departed from; window-composition note missing.
For the curator: issue 1 (SPLIT-14 reading), issue 2 (record the SPLIT-11 and SPLIT-10 exceptions).
```

**What I checked, with numbers.** Data loaded through `dataset_io.from_definition` (rebuilt from the raw files), plus my own rebuild in raw order for the contract ids. The shipped splits were reproduced exactly. All models are my own untuned ones, with thread caps:
- LightGBM: regularised, 3 seeds.
- Logistic regression: one-hot features plus log exposure.

The scripts and outputs are in the run folder.

- **Regime (SPLIT-1, SPLIT-3, USE-10).**
  - The use case is a yearly tariff over the insurer's own portfolio, so the entity is mostly known and the stream runs over time. Temporal is right.
  - Of the 2013 rows, 79.5% have their contract in 2011-2012 (by window 76.4 / 77.1 / 81.1%). By vehicle id the shares are 25.2% (22.6 / 24.9 / 26.0%).
  - The game's own pricing file (`test_contrats.csv`, 32,772 periods of 2014) shows the same shape: 82.0% of its rows have their contract in 2011-2013, 29.6% their vehicle, and 70.4% their contract in 2013 alone (2013 against 2012: 70.1%).
  - The test year therefore stands for the population the game priced. The splits_comment's figures (76-81% and 23-26%) are correct.
  - The 20% new contracts are in the test in their natural share, as in a real tariff year.
- **Time column and prediction point.**
  - `period_start` is the start of the situation period, and its year equals `ANNEE` on every row (asserted in `_clean`).
  - The newest start is 2 December 2013, so the first window spans 93 days. Accepting `meta_time_horizon_mismatch` is right: the horizon is the tariff year, and the windows reach 8-12 months past the cutoff.
- **Train side and SPLIT-9.**
  - The train side holds 56,178 rows (64.4%), with starts from 1 January 2011 to 2 December 2012.
  - Every training period ends by 31 December 2012 (0 later), because rows are cut at the year's end. No training row has its label after the window start, apart from claims reported late (see issue 2).
- **Windows.**

  | window | rows | with a claim | share of 2013 rows | share of 2013 claims | mean / max exposure |
  |---|---|---|---|---|---|
  | Sep-Dec | 5,312 | 123 (2.3%) | 17.1% | 8.0% | 0.19 / 0.33 |
  | May-Aug | 6,509 | 257 (3.9%) | 21.0% | 16.7% | 0.34 / 0.67 |
  | Jan-Apr | 19,229 | 1,163 (6.0%) | 61.9% | 75.4% | 0.55 / 1.00 |

  12,028 periods start on 1 January 2013. Claims per vehicle-year are flat across the windows (0.129 / 0.122 / 0.117).
- **Training history (SPLIT-20).**
  - The train side covers two full years, so every season is in it.
  - Claims per vehicle-year by quarter range from 0.108 to 0.137 over 2011-2013; by year they are 0.117, 0.119 and 0.119.
  - The mixes of zone, fleet management and fleet size are stable. There is a slow drift towards formula 3 (74% to 82%) and towards higher deductibles. No break.
  - The test windows cover all of 2013, so no season is left out.
- **Hidden groups and copies.**
  - The hidden-group probe makes no hit. `exposure` is "seen" 100%, as a feature should be (SPLIT-4). The composite key is seen 0.0% and near copies 2.7%.
  - With `period_start` a feature, no test row copies a training row. The 9,373 repeated rows (vehicles of one fleet in one period) fall within a window, never across the split.
- **Alternative splits (the decisive comparison; not used to choose windows, SPLIT-21).** ROC AUC, untuned:

  | design | exposure alone | logistic | LightGBM |
  |---|---|---|---|
  | shipped: 3 windows, mean (per window) | 0.637 (0.596 / 0.655 / 0.659) | 0.672 (0.634 / 0.679 / 0.703) | 0.672 (0.636 / 0.677 / 0.703) |
  | one window: all of 2013, train 2011-2012 | 0.682 | 0.713 | 0.712 |
  | forced grouped by contract, 3 folds x 2 repeats, all rows | 0.680 | 0.710 / 0.710 | 0.711 / 0.708 |
  | same, scored on the 2013 rows of each test fold | 0.682 | 0.713 / 0.712 | 0.710 / 0.709 |
  | IID, 3 random folds | 0.680 | 0.710 | 0.711 |
  | planning gap: tariff fit 1 Oct 2012 on the periods ended by then (45.4% of rows), shipped windows | 0.637 | 0.669 | 0.671 |

  Read on the same 2013 rows, the IID, grouped and temporal designs agree within 0.003. Neither the fleets nor the passage of time makes a random split optimistic here. The temporal design is chosen for the use case, not for a gap (SPLIT-4). The shipped mean sits about 0.04 lower only because of how the windows are cut (issue 3).

**Problems, ranked (principles.md)**

**1. P4, SPLIT-14 (Must) and SPLIT-8 (Must): three windows on one train side. The letter is met; the curator should confirm the reading.**
- Evidence:
  - The three test windows hold real dated rows, strictly after a train side of 64.4%. That is what SPLIT-14 asks for.
  - But all three share one refit. With a yearly horizon, only one annual window clears the floor: 2013 trained on 2011-2012 (64.4%). A 2012 window trained on 2011 would hold 30.4% of the rows.
- Precedents with the same facts went the other way. In this batch, spanish_motor_insurance_coverage_level_2022_2024 had three calendar years and one valid annual window, and shipped `ForcedGroupedFromTemporal`. The same tag went to pricing_game_2017_french_mtpl and frempl_french_motor_personal_line (one year). The wisconsin split audit flagged two annual windows as a SPLIT-14 breach.
- What sets this case apart:
  - The periods carry daily start dates, so windows inside the test year exist and keep the train side above the floor.
  - SPLIT-8 applies only when "the release cannot give the windows SPLIT-14 asks for". The two siblings named had no date finer than the year. frempl's windows inside the year fell below the floor under as-of training.
- Cost of the rule-safe alternative (forced grouped by contract): LightGBM 0.708-0.711, against 0.712 for the valid test year pooled, with the same order of the families. The alternative is no more optimistic, but it mixes the training and test years. The temporal design is closer to the use case and to the game.
- Remedy: none to the split. The curator should confirm that sub-windows of one dated test year, on the train side the refit cadence gives, count as SPLIT-14's windows, and record it as a Cases row under SPLIT-14. If not, the fallback is `ForcedGroupedFromTemporal` grouped by `contract_id` (SPLIT-8), with the cost above.

**2. P4, SPLIT-11 (Should) and SPLIT-10 (Should): two departures that need recording as exceptions.**
- **SPLIT-11, the fixed train side.** I agree with the builder (draft issue 2).
  - The deciding fact is the refit cadence. A tariff is fit once for the year (SPLIT-12), and the game gave the closed years and priced the next one (SPLIT-19). So a model pricing any 2013 period was fit on 2011-2012.
  - The SPLIT-9 argument in the splits_comment is true but secondary. An as-of train side could add the 5,619 and 11,708 closed 2013 periods (2.4% and 3.2% with a claim). Those rows are selected by their early end, and their scores were not decisive (0.6695 against 0.6686; 0.6143 against 0.6259; SPLIT-21).
  - Remedy: record "Exception to SPLIT-11: the tariff is refit once a year, so every window trains on the closed years; serves P3 and P4" in the record and the notes.
- **SPLIT-10, no gap.** A claim is known only once it is reported, and no report date ships. The notes say the possible optimism "cannot be measured". It can be bounded:
  - Any gap on the train side removes the 12,417 periods that run to 31 December 2012. A 1-day gap leaves 50.2% of the rows and a 1-month gap 48.7%, under the SPLIT-14 floor.
  - Simulated reporting delays of 30 and 90 days hide 113 and 355 of the 2,707 training positives. (In the simulation a claim falls uniformly in its period and goes unreported when it falls in the last 30 or 90 days of 2012.) LightGBM's mean moves from 0.672 to 0.674 and 0.672.
  - A planning gap (fit on 1 October 2012) gives 0.671 against 0.672.
  - Remedy:
    - record "Exception to SPLIT-10 (serves SPLIT-14)", as for lending_club and alfa_battle_2_0_task_2. This repeats a reason the batch has used before; principles.md asks for an amendment proposal at the third exception;
    - replace "cannot be measured" with the simulated bound, called a simulation (no report dates), not proof.

**3. P4, SPLIT-15 (Should) and SPLIT-20 (Should): the windows are cohorts of different period lengths. A note, no re-split.**
- Evidence:
  - Periods are cut on 31 December, so a period's start date caps its length: an exposure of 0.33 at most from September, 1.00 from January. Each window is therefore its own population. Jan-Apr holds the full-year 1-January periods (75.4% of the 2013 claims); Sep-Dec holds only short mid-year periods (8.0% of the claims, 123 positives).
  - A per-window ROC AUC ranks within cohorts of similar length. LightGBM averages 0.672 over the windows against 0.712 on all of 2013, and the exposure-alone baseline 0.637 against 0.682.
  - The newest window comes first, as the convention puts it, but it is the least representative and the noisiest: Hanley-McNeil SE about 0.027, against about 0.009 for Jan-Apr. The SPLIT-11 rationale ("the newest window, the most representative") does not hold on a fixed train side.
  - The game's 2014 file has the same structure. By window, 63% / 0% / 0% of its periods start on 1 January, with mean exposure 0.55 / 0.34 / 0.19. So the windows mirror the year to be priced, and nothing here is a defect.
- Citation: "Three windows, not the nine of the convention ... (SPLIT-17)". SPLIT-17's trigger, windows under about 50 test rows, does not apply (5,312-19,229 rows). The rule departed from is SPLIT-15. Its reason, that finer windows on one train side only cut the same rows into noisier pieces, is sound, and finer windows would also narrow each cohort further.
- Remedy, in the splits_comment:
  - cite SPLIT-15;
  - say that the window scores rank within start cohorts and run below a pooled score for the year (0.672 against 0.712);
  - say that the first split is the smallest and the noisiest.

**4. Pointers for other auditors (not split defects).**
- The vehicle key rarely survives the year boundary:
  - only 9.7% of the periods ending 31 December 2012 continue on 1 January 2013 under the same `IMMAT`, while 53.1% of their contracts continue;
  - 53.4% of the contracts present in both years share no vehicle id across them;
  - the median gap between a vehicle's consecutive periods is 90 days, and only 30.4% are contiguous.

  Either fleets replace vehicles fast or the key, or the extract, does not follow a vehicle. This bears on the notes' "42.8% of the periods end before 31 December with no later period of the vehicle" (the realised-length argument for `exposure`) and on the vehicle-history measurement. The contract is the entity that recurs, so the split is unaffected. For the leak and column auditors.
- "(2011-2012 to 2013, the call of 2026-10-30)": the curator's CC lines of 2026-10-30 do not name the split. It came from the AI Assessments of that day, which the curator's `TBD -> Yes` followed. Write "suggested on 2026-10-30, accepted with the curator's Yes", or have the curator confirm. For the claim auditor.

**Files.** Scripts and outputs in the run folder: the shipped splits; recurrence and the vehicle key; the game's 2014 file and the window composition; the alternative splits; the training history; the reporting-delay simulation.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner: pricing_game_2016_french_fleet**

Actor: the pricing actuary of a French motor insurer who sets the a priori vehicle tariff for small commercial
multi-vehicle ("flotte") contracts for the coming year, from the closed years' rating data. The decision is the rate per
vehicle-year by rating cell, its frequency part here; the fleet's premium is that rate times each vehicle's time on
cover. My probes: two scripts with their outputs in the run folder,
shipped windows, untuned models, 3 LightGBM seeds.

**Verdict: fit direct (agree with `fit="direct"`, USE-8).** The rows are the vehicle-periods ("situations") an actuary
fits a frequency model on, the features are the rating classes known when the period is priced, and the test year
follows the training years. The realised period length is a potential leak kept on purpose and named as such, which
leaves the fit direct under USE-8. The binary target stands in for the claim count I act on, and at this frequency the
gap is small.

**Metric: partly.** ROC AUC ranks the realistic models in the same order as the actuarial criteria do. But about 79% of
its lift above 0.5 is the period length, which I never need predicted, and it ignores the level of the probabilities,
which a premium is. My pick would be `log_loss`; keeping `roc_auc` is defensible (details under 5).

**1. Do I have these inputs when I price?**

- Rating classes (contract age, activity, zone, fleet size and management, new-company flag, channel, payment
  frequency, formula, deductible, insured value, vehicle age, power-value): yes, all are on the contract when it is
  written or renewed. The start date: yes.
- `exposure`: the actuarial role is right, the timing is not exact. A fleet premium is settled at the period's end for
  the vehicles that came in and went out during the year (AMRAE: "révision en fin de période d'assurance" for "les
  différentes entrées et sorties au cours de l'année"). So the earned vehicle-years are the premium base, and I price a
  rate per vehicle-year. That makes the length a GLM offset, not a risk factor I forecast. The length as realised is
  known only at the end, and the definition says so ("Potential leak, kept on purpose"). My check of the kept leak, on
  the raw files for 2011-2012: periods that end early and are the vehicle's last have 0.137 claims per vehicle-year,
  against 0.111 for periods running to 31 December. They also have 6.9 claims above 5,000 (scaled units) per 1,000
  vehicle-years, against 4.2. That fits total losses, or claim-driven exits, that end a vehicle's cover. The builder's
  test (an ending flag adds no ROC AUC) shows the leak does not move the score. I agree it stays, as named. The
  Decision table's wording "about the claim rate ... a little higher among the shortest" is fair within the length
  bands (+30% in the shortest band, +1% to +9% in the others).
- Inputs I would normally have that are missing:
  - The fleet's own claims experience (the S/C ratio over three years), which sets the renewal premium of fleets of 4
    or more vehicles, where the bonus-malus does not apply (AMRAE). It matters little here: the median contract-year
    has 2 distinct vehicles, only 18.2% have 4 or more, and the builder measured last year's contract and vehicle
    claims to add nothing (0.705 against 0.708).
  - The current tariff's premium, which I would refine (USE-6) and benchmark against with a double-lift chart. Not in
    the release.
  - Finer vehicle and use details (make or SRA group, use, mileage). The release keeps a combined power-value class
    and two vehicle-age classes. This is the disclosure control of the release, so it cannot be fixed.

**2. Is the target what I act on?**

I act on the expected claim count per vehicle-year, the frequency part of the pure premium. I want a number (a
calibrated frequency, or a calibrated probability per period), never a class. `claim` (count > 0) is a close proxy:

- Multiple claims collapse into one. 286 periods hold 2 to 7 claims, so 318 of the 4,568 claims (7%) are lost. At 0.12
  claims per vehicle-year, P(N ≥ 1) is close to E[N], so the ranking barely changes.
- IDA claims count. A net-cost actuary might count only the claims that cost money. I measured the alternatives on all
  of 2013 (LightGBM, length a feature). Any claim (shipped): ROC AUC 0.712. A claim with a positive net charge: 0.706.
  A non-IDA claim: 0.702. The length alone scores 0.682 on all three. The choice does not change the task, and the
  shipped target is the broadest and has the most signal. Counting gross claims and leaving recoveries to the severity
  part is standard frequency-severity practice.
- Wording, for the claim auditor (USE-5 precision, not a fit issue). `predicted` says "the claims in which the insured
  was not at fault and the insurer recovered its cost", and bullet 5 says the insurer "recovers the cost". Under IRSA,
  the recovery below 6,500 EUR excl. tax is a flat forfait, not the cost, which is why it exceeds the payment on 599 of
  the 1,190 IDA claims (Assurland). Also, 126 of the IDA claims are at 50% responsibility, so they are not all
  not-at-fault. Suggested: "claims settled under the IDA convention, where the insurer pays its client and recovers a
  flat amount from the other insurer".

**3. Does one row match one decision? Is the test what I would face?**

- One row is one vehicle-period with unchanged terms. That is the unit of a rating dataset, and the tariff's rate
  applies per vehicle and period. Yes.
- Test 2013, train 2011-2012: a tariff for next year, with 76-81% of the test periods on contracts I already insure
  (USE-10, a known entity; SPLIT-13). This is what I would face.
- Two gaps, both small:
  - In practice a 2013 tariff is fit in autumn 2012, on immature 2012 claims. Here the labels are developed to the
    2014 extract (the builder's note on slight optimism).
  - The three windows weight the year unevenly against how I would judge a tariff. Measured on the 2013 periods:
    Jan-Apr holds 76.9% of the vehicle-years and 75.9% of the claims, May-Aug 16.0% and 16.4%, Sep-Dec 7.1% and 7.7%.
    Each window still counts for a third of the mean score. I would judge a tariff on the year's book, pooled or
    weighted by exposure. Within a window the range of lengths is cut, so the mean window AUC (0.674 for the best
    model) sits below the pooled 2013 AUC (0.712). That is the split auditor's call. I note it because it changes how
    much the mid-year additions weigh in "my" score.

**4. Would I use this model? What would make me trust or distrust it?**

I would use it as the frequency component of an a priori vehicle tariff for small contracts, on four conditions:

- (a) Its frequency is proportional to the time on cover, so a half-year costs half the annual rate. A tree model
  with the length as a free feature can learn a length effect that is not proportional. I would fit with the length
  as an offset or check that the effect is proportional.
- (b) It balances overall and by segment (actual over expected near 1).
- (c) Its relativities can be explained to the agents and brokers who sell it.
- (d) It beats the current tariff on a double-lift chart.

What makes me distrust it:

- The anonymised levels (zone 1-6, activity 1-8, channel, formula) stop me from checking that relativities make sense
  (a zone order, a vehicle-value gradient).
- The lift is modest. The rating factors add 0.015-0.045 ROC AUC over the length (the builder's TP-4). In my probe the
  exposure-weighted Gini of the predicted rate is 0.19-0.21 for the GLM and LightGBM, against 0.02 for a risk-blind
  rate. That segmentation is real but modest, which is plausible for commercial motor with coarse factors.

**5. Does the declared metric score my decision?**

Measured on the three shipped windows, means over the windows:

| model | ROC AUC | log loss | exposure-weighted rate Gini | mean predicted / observed |
|---|---|---|---|---|
| constant rate x length (no rating factor) | 0.637 | 0.1628 | 0.019 | 0.92 |
| logistic, rating factors, no length | 0.621 | 0.1667 | 0.160 | 1.26 |
| logistic, length a feature | 0.661 | 0.1608 | 0.187 | 1.02 |
| Poisson GLM, length an offset | 0.672 | 0.1601 | 0.195 | 0.93 |
| LightGBM Poisson, length an offset | 0.671 | 0.1601 | 0.195 | 0.94 |
| LightGBM binary, length a feature | 0.674 | 0.1600 | 0.207 | 1.02 |

What the numbers say:

- **Ranking among the models a benchmark would run: consistent.** ROC AUC, log loss and the exposure-weighted Gini of
  the rate rank the four models that use the length in the same order. On these folds ROC AUC would not pick a model I
  would reject (MET-8 holds: a ranking metric serves every threshold, and there is no threshold or cost to fix, MET-6
  and MET-7).
- **What it rewards: mostly the time on cover.** A tariff with no rating factor at all scores 0.637, which is 79% of
  the best model's lift above 0.5. A model that segments risk but ignores the length (rate Gini 0.160) scores 0.621,
  below the risk-blind model. The relativities, the part of the model I act on, are a slice of about 0.04 AUC. Log loss
  has the same compression (0.1628 against 0.1600). Only the exposure-weighted rate Gini isolates the segmentation.
- **What it ignores: the level.** A premium is a probability times a cost, so it must be calibrated (the balance
  property). ROC AUC does not see the logistic model without the length overpredicting by 26%, or the Poisson models
  underpredicting by 7%, the 2011-12 frequency applied to 2013. Log loss, the Bernoulli deviance, is strictly proper
  (Gneiting & Raftery, under MET-8) and scores rank and level together. It is the binary form of the deviance by which
  actuaries select frequency models.
- **The unit:** each row counts the same whatever its exposure, and each window counts a third (under 3).

The metric I would choose:

- As the actuary, the mean Poisson deviance of the claim count, with exposure, for model choice. This is the standard
  frequency loss (Noll, Salzmann & Wüthrich 2018 on freMTPL; scikit-learn's frequency example). Next to it, the Gini
  of the ordered Lorenz curve (claims accumulated against exposure, ordered by predicted rate; Frees, Meyers & Cummings
  2011) for the segmentation. Both need the count or the length as a scoring column (MET-2), and the shared library
  has no Poisson deviance (MET-13). That is too large a change for a binary definition the curator chose on 2026-10-30.
- On the shipped binary target: `log_loss` (MET-8, declared as `context` under MET-11: a premium acts on the
  probability's level, not only on its rank).
- For keeping `roc_auc`: it is the documented binary fallback (MET-8, MET-11). It ranks models as the actuarial
  criteria do on these folds. And it is the binary counterpart of the `normalized_gini` the sibling insurance
  definitions declare (the identity used for porto_seguro, MET-11). So `roc_auc` is defensible, and the choice is a
  weighing call for the curator. The metric reason should say that the length carries most of the ROC AUC (the
  builder's "length alone 0.596 / 0.655 / 0.659" is in the notes but not in the reason).

**Gaps between the dataset and the real decision, ranked by how much they change the task**

1. The metric scores the ranking of periods, which the time on cover dominates, not the rate per vehicle-year I
   decide, and not its level (MET-1, MET-8). It changes how methods are compared, not which one wins on these folds.
2. The windows weight Sep-Dec (7% of exposure, 123 claims) as much as Jan-Apr (77%), where I would judge the year's
   book (SPLIT-17 area; MET-2 unit of evaluation).
3. The realised length as a feature: a kept, named, weak leak (early-ending last periods have 23% more claims per
   vehicle-year; no ROC AUC gain from the ending, measured by the builder). No change (USE-8, LEAK-10 kept).
4. A binary target instead of the count: 7% of claims collapsed. No change at this frequency (USE-5).
5. Missing the fleet's own experience and the current premium (USE-6, USE-10). The first is measured to add nothing,
   and the second does not ship.
6. Wording on IDA recovery ("its cost", "not at fault"): a correction to the text, not to the task.

**What an expert would change**

- The metric: `log_loss` as `context` (MET-11), or keep `roc_auc` and add to the reason that the length alone scores
  0.60-0.66 of it. That is the curator's weighing call.
- Pool the 2013 test year or weight the windows by exposure, if the split auditor agrees. Otherwise say in the
  splits comment that the mean over windows weights the mid-year additions at a third.
- Reword `predicted` and bullet 5: IRSA recovers a flat forfait, and 126 IDA claims are at 50% responsibility.
- Add to `use_case` or the notes that most contracts are small (median 2 vehicles per contract-year, 18% with 4 or
  more). An a priori per-vehicle tariff is the real practice for them, and fleets of 4 or more are mostly
  experience-rated.
- No change to the rows, features, target or split direction.

**Sources**

- The game's rules, `pricing-game-2016-FR.pdf` (the organisers' PDF and its text extract): column descriptions,
  "une prime pure", the aggregator market of Sec. 4.
- Raw files `train_contrats.csv`, `train_sinistres.csv` (sha256 as in `dataset.py`); my probes in
  the run folder.
- AMRAE, "Flottes automobiles : l'auto-assurance, opportunité ou risque pour votre entreprise ?": fleet from 4
  vehicles, no bonus-malus, renewal on the fleet's S/C, end-of-period revision for entries and exits, IDA:
  https://www.amrae.fr/flottes-automobiles-lauto-assurance-opportunite-ou-risque-pour-votre-entreprise
- Assurland on the IRSA convention: flat recourse below 6,500 EUR, at real cost above:
  https://www.assurland.com/assurance-auto/sinistres/indemnisation-convention-irsa/
- Noll, Salzmann & Wüthrich (2018), "Case Study: French Motor Third-Party Liability Claims", SSRN 3164764 (Poisson
  deviance with exposure), as cited in scikit-learn's "Poisson regression and non-normal loss" example (frequency =
  claims / exposure, exposure as weight, mean Poisson deviance, exposure-ordered Lorenz curve):
  https://scikit-learn.org/stable/auto_examples/linear_model/plot_poisson_regression_non_normal_loss.html
- Frees, Meyers & Cummings (2011), JASA 106:1085-1098 (ordered Lorenz curve, Gini), as cited in the sibling
  australian_vehicle_insurance_2004_2005 definition.
- Rules: `use_case.md` (USE-5, USE-6, USE-8, USE-10), `metrics.md` (MET-1, MET-2, MET-6 to MET-9, MET-11, MET-13).

</details>

<details><summary>Blind review</summary>

**Verdict: include with changes.** This is a real, documented French fleet motor own-damage portfolio with an honest temporal structure and modest real signal. Before it goes in, the test windows should be aligned with the calendar-year structure, two dead columns dropped, and the nominal codes typed as categorical. Its main weakness as a benchmark is low headroom: a one-hot GLM ties LightGBM.

**What the task is**

- **Source.** The 2016 "Pricing Game" of the Institut des Actuaires (100% Data Science day, 8 Nov 2016), redistributed as `pg16trainpol` in CASdatasets.
- **What a row is.** One "situation" (a coverage period with constant characteristics) of one vehicle in a business fleet policy, 2011-01-01 to 2013-12-31.
- **Target.** `claim` = `ClaimNb > 0`: 4,250 of 87,228 rows (4.87%), covering 4,568 claims.
- **The decision.** An insurer prices own-damage cover for fleet vehicles at renewal or when a vehicle is added. The organisers' PDF names the deductible as "Classe de franchise de la garantie DTA" (Dommages Tous Accidents), and the game asked for a "prime pure" for the next year's contracts. This is a genuine, standard actuarial use: claim-frequency modelling for pricing.
- **Provenance check.** I decoded the CASdatasets `.rda` files myself. The prepared table is a one-to-one relabelling of `pg16trainpol`: a sorted multiset comparison on period start, exposure, zone, power, formula, activity, channel, fleet size and target matched exactly.
- **Column mapping.** Area→zone, VehiclPower→power_value_class, PolicyCateg→formula, BusinessType→client_activity, ChannelDist→distribution_channel, FleetSizeCateg→fleet_size_class.
- **Dropped columns.** Year, EndDate, PolicyID, LicNb, the constant VehiclCateg (all "V1"), and ClaimNb (which became the target).
- **Public test file unusable.** `pg16test` (2014, 32,772 rows) has no labels publicly, so 2011-2013 is all there is.

**Concerns, most to least serious**

1. **The test windows fight the calendar-year truncation, so late windows are small and shifted.**
   - **Evidence: truncation.** No period crosses 31 December (0 of 87,228 rows). Rows that start late in the year are therefore mechanically short. Positive rate by start quarter falls from 6.2% (2013Q1, mean exposure 0.57) to 2.1% (2013Q4, mean exposure 0.17), and the same pattern repeats every year.
   - **Evidence: no year-aligned option.** With only three years of labelled data, three expanding test windows cannot all sit on year boundaries, so at least some cutoffs fall mid-year.
   - **Evidence: small, noisy late windows.** On plausible windows, the late-2013 ones are small: [2013-07-01, 2014) has 8,898 rows and 246 positives; a last-10%-by-date window has 7,022 rows and 165 positives. LightGBM AUC there is 0.636-0.658, with a standard error of about 0.02 (Hanley-McNeil). Method differences of 0.01 are unresolvable.
   - **Evidence: label overlap.** Mid-year cutoffs leave 13-14k training rows (about 17%) whose outcome period runs past the cutoff. I tested this by retraining on strictly-ended rows only; the AUC change was at most 0.006, so it is not a material leak, but it is untidy.
   - **Change.** Use year-aligned windows where possible: train 2011 → test 2012, and train 2011-12 → test 2013. If three windows are required, use half-years (2012H2, 2013H1, 2013H2) and pool or weight by number of positives. Report log loss alongside AUC, because per-window base rates differ for structural reasons.
   - **Caveat.** I could not see the harness's actual window boundaries.

2. **`exposure` dominates, and it is partly an after-the-fact quantity.**
   - **Evidence: dominance.** Exposure takes 53% of LightGBM gain. Log-exposure alone reaches AUC 0.60-0.67; all features reach 0.66-0.71.
   - **Evidence: how it is defined.** Exposure is (EndDate − BeginDate + 1)/365. EndDate is the end of the situation, which is only known ex post when a vehicle leaves the fleet mid-year.
   - **Evidence: possible claim-triggered exits.** Situations that end before 31 December with no later row for that vehicle have 0.134 claims per vehicle-year. Situations ending 31 December with no later row have 0.112, and contiguous mid-year splits have 0.102. This is consistent with some exits being caused by claims (for example write-offs under own-damage cover). It could also be churn heterogeneity; I cannot separate the two without claim dates.
   - **Mitigating evidence.** The source game itself treats exposure as known at pricing: `test_contrats` ships with `Exposition_au_risque` and the situation dates, and exposure as an offset is standard actuarial practice. Contiguous mid-year splits show no claim excess (2.98% positive rate), so situations are not cut at claim dates.
   - **Change.** Keep exposure, since removing it makes the task incoherent. Document that the benchmark assumes the coverage period is known. Optionally also offer the count target with an exposure offset, which is the natural form of the problem.

3. **Low headroom: the task is essentially additive.**
   - **Evidence.** Trained on 2011-12 and tested on 2013 (31,050 rows, 1,543 positives):
     - One-hot logistic regression with log-exposure: AUC 0.7124, log loss 0.1840.
     - LightGBM: AUC 0.7122, log loss 0.1841.
     - Bootstrap 95% CI of the AUC difference: [−0.0036, 0.0035].
   - **Why.** There are 13 low-cardinality categorical features plus exposure. Fleet-level clustering further reduces the effective sample size: 18,037 fleets, up to 81 rows per fleet, and 8,577 exact duplicate rows (9.8%) from vehicles of the same fleet with identical profiles. The duplicates stay inside one window under the temporal split, so they are not a cross-split copy.
   - **Change.** It is fine as a representative "GLM-sufficient" insurance-frequency task. Do not expect it to separate strong learners. If the benchmark already has freMTPL-style frequency data, check whether this adds diversity; the fleet/commercial own-damage angle is the differentiator.

4. **Preparation: dead columns and wrong types.**
   - **Dead columns.**
     - `n_vehicles` equals 1 in 87,226 of 87,228 rows. Drop it.
     - `insured_value_class` is missing in 87,093 rows (99.85%; source level "Unknown"). Drop it, or encode "Unknown" as its own level rather than NaN.
   - **Nominal codes stored as integers.** `zone` (A1-A6), `client_activity` (B1-B8, "Activité du client"), `distribution_channel` (D1-D3, "agents ou courtiers ou autres"), `formula` (C2-C5) and `fleet_size_class` (S1/S2) are stored as int64. The Rd says "most categorical levels have unknown meaning", so these should be categorical.
   - **Possibly ordinal.** `power_value_class` (P1-P11, "Combiné puissance valeur du véhicule") may be ordinal and can stay numeric.
   - **Unordered age classes.** `contract_age_class` is an unordered category with lexicographic levels (`'1 - 2 ans', …, '<= 1 ans', '> 5 ans'`). Make it ordered, or map it to 0-5.
   - **No other missing values.** Apart from `insured_value_class`, there are no missing values.

5. **Target definition is broad and slightly lossy.**
   - **Evidence.** The target counts every reported claim, including recovered or not-at-fault ones: 599 of 4,568 claims have ClaimCharge ≤ 0, and 126 are IDA direct-compensation claims. The binarisation collapses 286 rows that have 2-7 claims.
   - **Is there IBNR under-reporting?** No. Claim frequency per vehicle-year is flat across years (0.117 / 0.119 / 0.119) and is 0.117 for periods ending 2013Q4. Claims settled up to 2014, and only 41 are still open (SettlYear = 0).
   - **Change.** No change is needed. Document that the target is "any material-damage claim reported in the situation".

6. **The source documentation is inconsistent.**
   - **Evidence.** The CASdatasets Rd calls `pg16trainpol` "policies for private motor insurance" and "TPL policies". It also says "pg16test is used for training", which is clearly a typo. The organisers' PDF, by contrast, lists "Mode de gestion de la flotte", "segment: Taille de la flotte" and the DTA deductible. The data are fleet (commercial) own-damage, and the prepared name "french_fleet" is right.
   - **Plausibility.** Data are "from unknown private insurers". The values look like real anonymised portfolio data: exposure granularity, claim frequency of about 0.12 per vehicle-year, and realistic churn. Claim charges carry many decimals, suggesting a perturbation, but they are not used here.
   - **Change.** Cite the organiser PDF for semantics, not the Rd text.

**What I could not check**

- The exact three test-window boundaries, and whether `period_start` is passed to models as a feature. Day-of-year added nothing in my tests: AUC changed by ±0.01 and was mostly lower.
- Claim occurrence dates, which would settle whether mid-year exits are claim-triggered.
- Labels for the 2014 `pg16test` file, which are not public.
- Any perturbation or anonymisation the insurer applied.
- The original CSVs on freakonometrics.free.fr. I verified against the CASdatasets `.rda` instead, and read the instructions PDF via the Wayback Machine, since the live link returns 404.

</details>

<details><summary>Precedent check</summary>

**Precedent check (precedent-checker, 2026-11-01): pricing_game_2016_french_fleet**

```text
Verdict: most choices follow their precedents. One keep is not allowed by the ranking as written (exposure), one Must
  label departs from its sibling (metric origin), and one amendment is due (SPLIT-10).
Validity: LEAK-10 (Must): `exposure` is kept as realised. That departs from frempl_french_motor_personal_line and
  spanish_motor_insurance_coverage_level_2022_2024, which fixed the early ends they could locate (LEAK-7). It also
  departs from LEAK-38's host-file clause (kick, expresso; Lennart, 2026-10-22). A keep would be an amendment, not an
  exception (prompt A).
  SPLIT-8 / SPLIT-14: temporal where the siblings were forced to grouped. Consistent: the daily dates set it apart.
  Three windows inside one test year on one train side is a first case and needs a Cases row.
  SPLIT-11: departed from with a stated reason (the tariff is refit once a year). An exception to record, the first of
  its kind.
  SPLIT-10 (no gap): the third exception for the reason "a gap would break SPLIT-14's 50% floor" (prompt C).
  SPLIT-15: departed from, but cited as SPLIT-17.
Value: `roc_auc` is consistent with porto_seguro and with the family's Gini (identity, MET-11). Origin `fallback`
  departs from pricing_game_2017_french_mtpl's `stand_in` with nothing to set it apart (MET-11, Must; prompt B).
  TP-4 reads as in frempl, australian and spanish.
Quality: ids, labels, missing codes and repeated rows are handled as the siblings handle them.
Target: the binary indicator is the curator's call for this dataset (CC 2026-10-30). Its stated reason also holds
  for siblings that kept the amount, so the notes should name what is specific to pg16. IDA claims counted: consistent.
Drift: none yet. A pair to avoid: keeping pg16's realised length while confirming frempl's fix (prompt A).
```

Sources read: the decision register of the run (it raises no flag for the insurance family), the
definitions and REVIEW.md files of the run's insurance tables, the records of fremtpl2, pricing_game_2015/2016/2017,
the zero-inflated triage summary (no longer in the repository; each call is in its record's Assessment of 2026-10-30) ("Policy calls of 2026-10-30"), the Cases tables of
`leak_checks.md`, `splits.md` and `metrics.md`, frempl's panel (precedent checker, mediator D2), and this panel's
claim, column, split and practitioner reports. Every number below comes from those reports. I ran no new probe.

**Decision by decision**

1. **Target `claim` (count > 0) and `binary_classification`.** Consistent with the curator's decision. Departs from the
   family's amount targets, with a stated reason that is only partly specific to pg16.
   * The curator's call: Andrej asked "Might make more sense to add this as a classification task, what do you think?".
     The AI agreed (Assessment 2026-10-30), and the CC of the same day gave `TBD -> Yes` after that answer. Andrej's
     answer to policy question 3 ("suggest judgement calls based on the references for each dataset") makes calls per
     dataset the rule here. A different target from fremtpl2's is therefore no drift.
   * The siblings kept the amount: fremtpl2 (CC, Andrej, 2026-10-20: "aggregate claim amount ... The claim count alone
     is the classic alternative target; not both"), frempl, pricing_game_2017_french_mtpl, australian,
     spanish_motor_insurance_2015_2018 and spanish coverage. australian's panel weighed and rejected a binary target
     ("drops the claim size the insurer prices", its issue 4).
   * Why the stated reason does not set pg16 apart: the notes give "the charges among claimants carry no signal". That
     holds for the siblings too: frempl R^2 -0.20 to -0.01 on claimants, pg17 -0.036, spanish 2015-2018 -0.03 to 0.03.
   * What does set pg16 apart, already in the record:
     * the charges are scaled by one constant;
     * single charges stop at 8,565 with no pile, a short tail that is unexplained for material damage;
     * 537 periods net negative from IDA flat recoveries.
   * Suggestion: give those facts as the reason in the target bullet. No consistency prompt; it is the curator's call.

2. **IDA claims count as claims (523 periods with no positive charge).** Consistent.
   * The family's call of 2026-10-30 ("a net recovery is no claim cost of the year") is about amount targets: frempl's
     negatives, pg17's recourse totals.
   * For a count, each dataset follows its source's own indicator. pg16's `nombre_de_sinistre` includes IDA claims;
     frempl's `ClaimInd` is 0 on its negative amounts. Both follow their source (USE-5).
   * The practitioner measured the alternatives: a positive-charge claim scores 0.706 and a non-IDA claim 0.702, against
     0.712 for any claim.

3. **`exposure`, the realised period length, kept with a `Potential leak, kept on purpose:` note.** Departs from the
   closest precedents. Of the two stated reasons, the rules reject one and the panel refuted the other. Not reasonable
   under the ranking as written: LEAK-10 is a Must, so a keep needs an amendment (prompt A).
   * Same mechanism, same facts:
     * frempl (AI fix after its panel, 2026-11-01; pending as issue 2 of [its REVIEW.md](../frempl_french_motor_personal_line/REVIEW.md)).
       Its dates locate the early ends row by row, and those ends carry 2.7 times the cost per exposure-year. Its
       mediator (D2) settled the point by rank: LEAK-10 holds; LEAK-6's narrowing covers only late values that cannot
       be located; LEAK-11 does not reach a value that raises the claim ranking. The fix was the start-known length.
     * spanish coverage (AI draft, 2026-11-01). It resets the cancellations it can locate to a full year (LEAK-7;
       0.50 against 0.28-0.31 claims per exposure-year). The part it cannot locate (new business) carries the kept-leak
       note.
     * pg16 has the dates too. 58.2% of 2013 periods end before 31 December. Given the covariates known at the start,
       early-ending periods have a rate ratio of 1.22 [1.12, 1.33] (column audit). The realised length adds ROC AUC
       +0.040 to +0.055 over the length known at the start (claim audit #17). Here the declared metric is that claim
       ranking.
   * Precedents that keep, and why they do not carry:
     * australian (pending, [its issue 2](../australian_vehicle_insurance_2004_2005/REVIEW.md)) keeps under LEAK-11
       because there the late part lowers the Gini (0.182 against 0.31). In pg16 it raises the declared metric, so
       LEAK-11 cannot apply.
     * fremtpl2 (CC, Andrej, 2026-10-20: "The contracted period is known at pricing (a mid-year cancellation also
       shortens it)") is the curator's own keep, and the 2026-10-30 policy row for pg16 ("feature") cites it. It was
       made before LEAK-38's scope amendment (2026-10-22) and LEAK-10's clauses (2026-10-26), on data that cannot
       locate an early end. australian's mediator read it as a precedent on practice (a feature, not a divisor), not
       on these facts.
   * The definition's two reasons against the rules and the panel:
     * "The game's pricing file gives each period's dates and length too." This is the argument LEAK-38 (as amended
       2026-10-22, Lennart) rejects: "even if the host's test file carries it the same way: that file is a holdout of
       the same snapshot, not deployment data". It was decided that way for kick (`WheelType`, `PRIMEUNIT`, `AUCGUART`)
       and expresso_churn_prediction (`REGION`); see `leak_checks.md`, Mechanisms table. test_contrats.csv is the 2014
       holdout of the same 2016 extract.
     * "The end carries no signal beyond the length." The 31-December flag is fixed by start and length on 99.5% of the
       rows, so that test could not fail (claim audit #17). LEAK-10's second clause also says that "removing it changes
       no score" alone is no reason to keep. A test that can fail, the Poisson offset model with an early-end flag
       (0.669 against 0.668), does show the outcome-linked part adds no ranking. But the time on risk unknown at the
       start is worth 0.04-0.05.
   * Weaker than frempl, by the closest comparable measures: +23% claims per vehicle-year for vehicles whose cover ends
     early for good (+30% in the shortest band, +1% to +9% in the others), against 2.7 times the cost per exposure-year
     in frempl. This is option (a) of prompt A. It is a fact about degree, not about kind.
   * Form: the label, the mechanism, the numbers and the revisit condition match what definitions.md asks for. frempl's
     precedent check had flagged a `Note:` there; pg16 is right on form.

4. **Split: temporal; train 2011-2012; three four-month windows of 2013, newest first.**
   * Temporal rather than `ForcedGroupedFromTemporal`: consistent.
     * pricing_game_2017_french_mtpl and frempl hold one year; spanish coverage holds three calendar years with no
       finer date. All three went to SPLIT-8.
     * pg16's daily start dates give windows that keep 64% of the rows in training. SPLIT-8 applies only when "the
       release cannot give the windows SPLIT-14 asks for".
     * wisconsin_local_government_property_insurance_fund, also annual rating with only a year column, ships two
       yearly windows (a SPLIT-14 question in its own panel). It does not bear on pg16.
   * Three windows inside one test year, on one train side: no precedent in the working copy. The custom split
     functions show no other fixed train side. It meets SPLIT-14 in letter. The curator confirms the reading, and it
     becomes the first Cases row under SPLIT-14 (split audit, issue 1).
   * Fixed train side, a departure from SPLIT-11 (Should), with a stated reason that sets it apart: the tariff is refit
     once a year, and the game priced a whole year from the closed years (SPLIT-12, SPLIT-19).
     * spanish_motor_insurance_2015_2018 grows its train side month by month. Its source names pricing for new
       business, written monthly. The two readings of the refit cadence differ, and each rests on its source.
     * To record: `Exception to SPLIT-11` in the record and the notes. It is the first of its reason.
   * Three windows, not nine, a departure from SPLIT-15 (Should), cited as SPLIT-17.
     * SPLIT-17's trigger (under about 50 test rows per window; coffee_rating_prediction) does not apply: the windows
       hold 5,312 to 19,229 rows.
     * The reason is sound under SPLIT-15: on one train side, finer windows only cut the same test rows.
       rain_in_australia (Lennart, 2026-10-26) went to more windows on an expanding train side, which is not this case.
     * Fix the citation.
   * No gap, a departure from SPLIT-10 (Should). The notes do not name it. The split audit gives the fact: rows are cut
     at 31 December, so a 1-day gap leaves 50.2% of the rows and a 1-month gap 48.7%, under SPLIT-14's floor. The
     simulated delays move the mean AUC by 0.003 or less.
     * The same reason has two recorded exceptions in `splits.md`: alfa_battle_2_0_task_2 and lending_club (Lennart,
       2026-10-21). In this run, spanish_motor_insurance_2015_2018 and wisconsin propose the same exception.
     * pg16's would be the third, or later, so the amendment is due (prompt C). The proposed amendment for
       ames_housing and perth_house_prices covers another reason and does not count.
   * Recurring fleets (SPLIT-13): consistent with the use case (known entities, USE-10) and with the game's 2014 file
     (82% of its rows have their contract in 2011-2013).
     * frempl had to group because a later record's claim counters carry the earlier claim. pg16 trains strictly
       earlier and ships no claim-history feature, so no grouping is needed.
     * Note: the "call of 2026-10-30" for the split was an AI suggestion accepted with the curator's `Yes`, not a CC
       of its own. Word it "suggested on 2026-10-30, accepted with the Yes", as australian does.

5. **Kept and dropped columns.** Consistent.
   * `contract_id` (subscription order) and `vehicle_id` dropped. This matches fremtpl2's `IDpol` (encodes year and
     file order; CC 2026-10-20), pg17's `id_vehicle` ("their rank should not represent anything valuable") and
     LEAK-10's pointing-id row (sdss_17).
   * `year` (a copy of the start) and `vehicle_category` (constant) dropped: CLEAN-5.
   * `period_start` kept as a datetime feature, like the time column of spanish_motor_insurance_2015_2018.
   * `period_end` dropped. Its end stays in start + `exposure` (column audit), so this belongs to decision 3. frempl
     dropped both dates for that reason, after fixing the length.
   * "ND" made missing (CLEAN-10), as pg17 made its placeholders missing. Two code sets mapped to labels (CLEAN-12), as
     ames_housing (Lennart, 2026-10-26).
   * Anonymised classes typed categorical (CLEAN-14). This follows the amex reading (Lennart, 2026-10-21): categorical
     when the context says so. frempl's `RiskArea` stays numeric because its source says "possibly ordered"; that is
     different documentation, not a conflict.
   * `n_vehicles` (1 on all but 2 rows) kept. CLEAN-5 covers only constant columns, and I found no precedent against
     keeping it.
   * History features measured and not added. LEAK-34 allows them and does not require them.
   * Repeated feature rows kept (LEAK-18), as frempl (391 after rounding), australian (707) and spanish (three pairs)
     did. frempl's drop of exact copies over every source column does not arise: the raw periods are unique on their
     keys (asserted).

6. **Metric `roc_auc`, origin `fallback` (MET-8).**
   * The value is consistent.
     * porto_seguro (binary claim indicator) declares `roc_auc` for the competition's normalized Gini, by MET-11's
       identity.
     * The family's ranking metric (policy question 3, 2026-10-30: the normalized Gini) is the same order on a binary
       target.
     * The practitioner's `log_loss` (context) would be a new call, against both. It is a weighing call (MET-10) for the
       curator, not a consistency fix.
   * The origin departs, with nothing to set it apart (prompt B). pricing_game_2017_french_mtpl declares
     `Metric.stand_in(..., original=<the market profit>)` for the same organiser's market game. The 2026-10-30 policy
     row for this record said "Gini (stand-in)". Under MET-11 (Must), stand-in is the case "the source has a unique
     metric that cannot be computed on our data (inputs not published, a task we changed)". The definition's own
     reason states both conditions. The second Assessment of 2026-10-30 ("the fallback, MET-8") was an AI line. The
     CC that followed decided the verdict, not the origin.

7. **Provenance, year and licence.** Consistent.
   * The organisers' files rather than CASdatasets (PROV-8), like diabetes_3 (Lennart, 2026-10-26: source_links to
     the authors' file, copies named as copies) and airfoil_self_noise. pg17 took CASdatasets only because the toolbox
     is gone (404).
   * CASdatasets' `DirectComp` noted as a problem of that copy (PROV-15), like OpenML 43838.
   * Year 2016 (PROV-9).
   * `license = None` when the copy used states none, as wisconsin does. pg17's GPL comes from CASdatasets, the copy
     it uses.
   * The three warnings proposed for acceptance have precedents: `dataset_duplicate_rows` (account_debt_south_africa,
     hotel_booking_demand), `meta_time_horizon_mismatch` (zillow_prize, perth_house_prices) and
     `meta_license_unknown` (diabetes_3). The definition does not yet carry `accepted_check_warnings`.

8. **Zeros and record fields.** Consistent once updated.
   * Andrej's definition of `Two-Regime Zeros` (policy question 4: a low value by far the most frequent and independent
     of the rest of the target) cannot apply to a binary target. The tag goes at hand-over, with
     `problem_type: Regression`, the CASdatasets-only `name` and `source_links`, and `v2_path`.
   * diabetes_3 (Lennart, 2026-10-26) is the precedent for setting the record fields as the definition has them.

9. **Fit `direct` with a kept leak; the "Known" text.**
   * `direct` with a named kept leak follows USE-8 as written (kick: a kept leak "does not by itself make a fit
     approximate").
   * `task_summary.known` and the first bullet say the length is known at the start. australian corrected the same
     error after its panel (2026-11-01, USE-3). The same rewording is due here, whatever prompt A decides.

**Consistency prompts**

**Consistency check A (AI, 2026-11-01):** if you keep pg16's realised `exposure` (a departure from LEAK-10, Must), the
call differs from frempl_french_motor_personal_line (fixed after its panel, 2026-11-01, pending your issue 2) and
spanish_motor_insurance_coverage_level_2022_2024 (located cancellations reset, 2026-11-01). The mechanism is the same:
time on risk cut short after the prediction point, located row by row by the dates, with the early ends claiming
more at the same length. The definition's reason "the game's pricing file carries the lengths too" is the one LEAK-38
rejected for kick and expresso (Lennart, 2026-10-22). Its "no signal beyond the length" test could not fail. What sets
pg16 apart?
(a) Two facts, which can only be recorded as a LEAK-10 amendment scoped to them, since a Must takes no exception:
fleet cover is billed on the vehicle-years actually earned (the premium is revised at the period's end for vehicles
in and out, AMRAE, cited by the practitioner); and the outcome-linked part of the early ends adds no ranking given the
covariates (0.669 against 0.668), with a weaker link than frempl's (+23% claims per vehicle-year against 2.7 times
the cost per exposure-year). The weakness: a personal policy cancelled mid-term also earns its premium pro rata
(inference, not checked), so the billing fact may not set pg16 apart from frempl. And the time on risk unknown at the
start still adds 0.04-0.05 AUC.
(b) Treat pg16 like frempl: give every early end its length to 31 December (LightGBM 0.671 to 0.622; 0.630 if only the
periods with no later period are changed). Drop `exposure` if it then follows from `period_start`, and re-run TP-4.
(c) Reopen frempl's and spanish's fixes to match pg16.
(d) Change the rule broadly, from fremtpl2's call: realised time on risk stays as a feature in insurance pricing. That
reaches frempl, spanish, australian and fremtpl2 together, and would end frempl's issue 2 and australian's issue 2 with
one answer.

**Consistency check B (AI, 2026-11-01):** the metric origin `fallback` differs from pricing_game_2017_french_mtpl
(`stand_in`, original the market profit, AI draft 2026-11-01) and from this record's suggested call of 2026-10-30
("Gini (stand-in)"). The facts are the same: one organiser's market game whose result needs other players' premiums
and unpublished claims, on a task we changed. What sets pg16 apart?
(a) The 2016 market placed each insured by a random draw among the cheapest premiums, so it gave no score to stand in
for. This is weak: MET-11 names "a task we changed" as stand-in, and the players' results were a score.
(b) Treat pg16 like pg17: `Metric.stand_in("roc_auc", original=<the 2014 price-aggregator market, rules Sec. 4>, ...)`,
the reason adding that ROC AUC ranks as the Gini does (2 x AUC - 1).
(c) Reopen pg17 to `fallback`.
(d) Amend MET-11.
Recommended: (b), a label change with no effect on any score.

**Consistency check C (AI, 2026-11-01):** shipping pg16 with no gap would be the third exception to SPLIT-10 for one
reason: a gap of the label's delay leaves a window's train side below SPLIT-14's 50% floor. The first two are
lending_club and alfa_battle_2_0_task_2 (Lennart, 2026-10-21). spanish_motor_insurance_2015_2018 and wisconsin propose
the same in this run. principles.md asks for an amendment at the third.
(a) Record it as an exception (the facts: rows cut at 31 December, 50.2% of the rows with a 1-day gap, 48.7% with a
month; the simulated delays move AUC by 0.003 or less).
(b) Set a gap. The train side then falls below the floor, so SPLIT-8 applies.
(c) Not applicable.
(d) Amend SPLIT-10: "When a gap of the label's delay would leave a window's train side below SPLIT-14's floor, the
windows train without it, and the delay is stated as a risk with its measured or simulated bound." The five cases then
apply the rule instead of departing from it.

**Cases rows due once the curator decides:**
* SPLIT-14: sub-windows of one dated test year on the train side the refit cadence gives.
* SPLIT-11: exception, annual refit.
* SPLIT-15: three windows on one train side.
* LEAK-10 or its amendment: time on risk in insurance tables, decided with frempl issue 2, spanish coverage and
  australian issue 2.
* MET-11: market games as stand-in, with pg17.

</details>

<details><summary>Advocate</summary>

**Advocate, opening brief (2026-11-01): pricing_game_2016_french_fleet**

```text
Verdict argued: ship after changes. The data, the use case, the split and the metric's value hold. The changes are
  text, labels and one curator call on `exposure`, and every option of that call keeps the dataset.
Validity: P5 holds (the organisers' files, not generated); USE-1, USE-5, USE-8 hold (fit direct); SPLIT-1, 3, 9, 13,
  14 hold; LEAK-10 triggered by the realised `exposure`: a keep needs the curator's amendment, otherwise the LEAK-7
  fix; USE-3 wording fix.
Value: TP-2, TP-4, TP-9 hold; MET-11 origin goes to stand-in (a label, no score changes).
Quality: CLEAN rules hold; the record's fields are stale (update them at hand-over).
```

**1. The data is real, from its first publication, and faithful (P5; PROV-3, PROV-8, EV-6).**
- Evidence:
  - The definition downloads the organisers' own CSVs (sha256 pinned, Wayback copy with the same bytes).
  - The claim audit re-derived every count, share and probe number to the last digit: 39 of 48 claims hold, and none
    of the 7 refuted is about the data's content.
  - The curator's extra test ("if generated, a no") passed on tests that could have failed: whole-euro piles once the
    scaling constant 1.077841 is removed (6.1% against 0.1% for smooth amounts), exposure heaping with payment
    frequency, starts on business days, the contract age stepping up at the anniversary (1,946 of 1,946). CC
    2026-11-01: `Yes`.
  - The blind reviewer decoded CASdatasets' `.rda` independently and found a one-to-one relabelling.
- Why it stands: no agent disputes it. It is the fact that sank the pg15 sibling (AHDS), and it is refuted here by
  proof, not by reading (EV-6).

**2. A real pricing task with a direct fit (P3; USE-1, USE-5, USE-8, all Must).**
- Evidence:
  - The practitioner: "fit direct (agree)". The rows are the vehicle-periods an actuary fits a frequency model on, and
    the features are the rating classes held at pricing. The blind reviewer: "a genuine, standard actuarial use".
  - The binary target is a close proxy of the count: at 0.12 claims per vehicle-year, P(N >= 1) is close to E[N].
    Only 7% of the claims are collapsed (286 periods).
  - Counting IDA claims is the broadest target with the most signal: 0.712 against 0.706 (positive charge only) and
    0.702 (non-IDA only). The curator chose the indicator (CC 2026-10-30).
- Real problem, mildest fix: `predicted` and bullet 5 should say the insurer recovers "a flat amount" under IRSA, and
  that 126 IDA claims are at 50% responsibility. This is wording (USE-5 precision); the task does not change.

**3. The split mirrors the application and meets every Must (P4; SPLIT-1, SPLIT-3, SPLIT-9, SPLIT-13, SPLIT-14).**
- Evidence:
  - The split auditor: "right with notes (no re-split)".
  - The 2013 test year has the shape of the game's own 2014 pricing file: 76-81% of its periods are on known
    contracts, against 82% in the file.
  - SPLIT-9: every training period ends by 31 December 2012. The training history shows no break (SPLIT-20).
  - On the same 2013 rows, the IID, grouped and temporal designs agree within 0.003, so the temporal choice follows the
    use case, not a score.
  - The daily start dates set this case apart from the siblings forced to grouped (SPLIT-8). The precedent checker
    calls it consistent.
- Against the alternatives:
  - The blind reviewer's year-aligned windows (train 2011, test 2012) leave 30.4% of the rows in training, which breaks
    SPLIT-14 (Must). Its worry about 13-14k overlapping training labels does not apply to the shipped fixed train
    side.
  - The practitioner's pooled 2013 is one window: under SPLIT-14 that sends the task to SPLIT-8, away from the use
    case. The three windows are how the Must is met, and they mirror the cohorts of the 2014 file (by window, 63%, 0%
    and 0% of its periods start on 1 January).
- Real problems, mildest fixes (all text):
  - a SPLIT-14 Cases row for sub-windows of one dated test year;
  - `Exception to SPLIT-11` (the tariff is refit once a year, SPLIT-12, SPLIT-19);
  - SPLIT-10, no gap: the simulated reporting delays move the AUC by 0.003 or less. It is the third exception of its
    kind, so the amendment of prompt C is due;
  - cite SPLIT-15, not SPLIT-17;
  - one sentence that per-window scores rank within start cohorts (0.672 against 0.712 pooled) and that the newest
    window is the noisiest.

**4. `exposure`: a real problem, and the dataset survives either remedy (P4, LEAK-10 Must; the remedy ladder; USE-8).**
- Conceded:
  - "Known at prediction time: ... its length" is false (USE-3): 58.2% of the 2013 periods end early.
  - The 31-December-flag test could not fail (EV-6).
  - The length unknown at the start adds ROC AUC +0.040 to +0.055.
  - LEAK-38 rejects "the host's test file carries it" as a reason on its own.
  - LEAK-10 is a Must, so a keep cannot be an exception. It needs the curator's amendment.
- The case for the keep (my recommendation):
  - The part that is linked to the outcome adds no ranking, by tests that could have failed: a Poisson offset model
    scores 0.669 without the early-end flag and 0.668 with it; LightGBM scores 0.671 as shipped and 0.670 with an exit
    flag (column audit).
  - What is left is the time at risk. The domain's own evaluation conditions on it: the Poisson deviance with exposure
    (Noll, Salzmann and Wüthrich 2018) and the exposure-ordered Lorenz curve (Frees et al. 2011). Fleet cover is billed
    on the vehicle-years earned ("révision en fin de période" for vehicles in and out, AMRAE, cited by the
    practitioner).
  - The fix answers a different question: a claim before an unknown end mixes frequency with retention, and that is
    not the quantity the actuary acts on (USE-5).
  - The only curator decision in the family keeps the realised exposure (fremtpl2, CC 2026-10-20, Andrej). The fixes
    in frempl and spanish coverage are AI changes still pending, which rank below a CC ("Who decides").
- Scope of the amendment: prompt A (d), decided with frempl, spanish coverage and australian. Keep realised time at
  risk when the outcome-linked part shows no gain given the covariates. That test separates pg16 (+23% claims per
  vehicle-year, no AUC gain) from frempl (2.7 times the cost per exposure-year). It does not rest on a billing fact,
  which may not set the two apart.
- If the curator declines: the LEAK-7 fix (the length to 31 December) keeps the dataset. The score falls from 0.671
  to 0.622, the covariates still beat the start-known length (0.623 against 0.549), and TP-4 is re-run.
- Either way, rewrite the text:
  - `known` and the first bullet;
  - `fit_reason`, without the flag argument;
  - the leak note, with the rate ratio 1.22 and the +0.04-0.055;
  - Decision 1, as claims per vehicle-year by how the period ends;
  - 58.2%, not 42.8% (the file looks like a sample).
- Why this does not lead to `No`: independent failures are not conflicts, so P3 does not excuse a Must. But the
  remedy ladder keeps exclusion for a Must that cannot be fixed, and this one can be fixed either way. The tension row
  says: fix the leak and keep the task.

**5. Worth benchmarking (P6; TP-2, TP-4, TP-9).**
- Evidence:
  - The models beat the length alone on every window (LightGBM 0.635 / 0.676 / 0.704 against 0.596 / 0.655 / 0.659).
    The task probes raise no flag.
  - The windows hold 123 / 257 / 1,163 positives (TP-9).
  - The exposure-weighted Gini of the rate is 0.19-0.21, against 0.02 for a risk-blind rate (practitioner), so the
    segmentation is real.
- Against "low headroom" (the blind reviewer: GLM ties LightGBM, CI [-0.0036, 0.0035]): TP-2 (Should) says a small
  signal and no spread are no reason to retire (rosbank1 and sf_permit_time were kept with no_spread). A GLM-sufficient
  insurance frequency task is representative. It is the family's only commercial fleet own-damage portfolio.

**6. The metric's value is right; its origin needs a one-line fix (P6; MET-8 Should, MET-11 Must).**
- Conceded (MET-11): the origin should be `stand_in`, with the original being the 2014 price-aggregator market
  (rules, Sec. 4). This follows pricing_game_2017_french_mtpl and this record's own call of 2026-10-30. No score
  changes.
- For `roc_auc`:
  - On these folds it ranks the models as log loss and the exposure-weighted Gini do (practitioner table).
  - 2 x AUC - 1 is the normalized Gini, the family's metric (porto_seguro).
  - `log_loss` as context is a weighing call (MET-10) that the practitioner calls defensible either way.
  - Add to the reason that the length alone carries most of the AUC.

**7. The cleaning is the expert state (P7; CLEAN-3, CLEAN-5, CLEAN-10, CLEAN-12, CLEAN-14; LEAK-18).**
- Evidence:
  - The column audit finds every column but `exposure` fine.
  - The blind reviewer's type points concern CASdatasets' integer codes. The definition already types zone, activity,
    channel, formula and fleet size as categorical.
  - "ND" made missing is right: it marks no single formula (CLEAN-10).
  - `n_vehicles` is harmless: CLEAN-5 covers only constants.
  - The repeated rows are natural and never cross the split (LEAK-18).
- Real problems, mildest fixes:
  - a leap-year clause for the 2,099 rows with "0.01 less";
  - at hand-over, update the stale record fields (`problem_type: Regression`, the `Two-Regime Zeros` tag, the
    CASdatasets-only name and links; records.md, PROV-8, as for diabetes_3);
  - accept the three warnings, each of which has a precedent.

</details>

<details><summary>Critic</summary>

**Critic, opening brief (2026-11-01): pricing_game_2016_french_fleet**

**Verdict: ship only after changes.** The task is real: an insurer's frequency tariff for fleet vehicles, the game's own task. Nothing below argues for exclusion. But as defined, the dataset gives models a feature that did not exist at the prediction point, and its text says the opposite. The fix belongs in the definition, and the task survives it. Points 1 and 2 are Musts that block shipping as it stands. Point 3 needs the curator's confirmation of a first-case reading. Point 4 is a label change. Point 5 is text and record fields.

```text
Verdict: ship after changes.
Validity: LEAK-10 triggered on `exposure` (Must), fix by LEAK-7 (point 1); USE-3 triggered, wording (point 2);
  SPLIT-14 met in letter, a first-case reading for the curator; SPLIT-10, SPLIT-11, SPLIT-15 departures to record
  (point 3). USE-1, USE-8, SPLIT-1, SPLIT-9, SPLIT-13, PROV-8 hold.
Value: MET-11 origin wrong, label change (point 4); TP-4 holds before and after the fix.
Quality: statements the data refutes and stale record fields (point 5); nits not counted.
```

**1. `exposure` is the realised length. Most periods' length is unknown at the start, and the early ends go with the claims (P4, LEAK-10, Must).**
- **Problem.**
  - `exposure` is the period's realised length. 58.2% of the 2013 periods end before their scheduled end, and across all years only 0.8% end at a contract anniversary. Their length is known only once they end.
  - `period_start` is also a feature, so `exposure` gives back the dropped `period_end`.
- **Effect on the task.**
  - Models rank periods partly on time at risk that the insurer cannot know when it prices.
  - The part of the length unknown at the start adds ROC AUC +0.040 / +0.055 / +0.052 on the three windows. That is about a quarter to a third of the skill above chance.
  - The comparison (claim audit #17), mean ROC AUC over the windows:

    | features | mean ROC AUC |
    |---|---|
    | covariates and the start's day of the year | 0.623 |
    | the same plus the length known at the start | 0.623 |
    | the same plus the realised length | 0.672 |

- **The clause that could keep it does not apply.** LEAK-10 keeps a window's value only when "the data shows the window's values do not move with the outcome given the covariates known at the prediction point". Here they move.
  - Given those covariates, early-ending periods claim at a rate ratio of 1.22 [1.12, 1.33] in 2011-2012 (p = 2e-6) and 1.18 in 2013. This is a Poisson GLM with an offset (column audit).
  - Vehicles whose cover ends early for good have 0.137 claims per vehicle-year, against 0.111 for periods that run to the year's end.
  - Their claims also cost more: 12.0% are above the 90th percentile of charges, against 9.2%.
- **The definition's two reasons fail.**
  - (a) "The end carries no signal beyond the length." This test could not fail. The 31 December flag is a function of start and length on 99.5% of rows (EV-6). And a "removing it changes no score" test alone is no reason to keep (LEAK-10, 2026-10-21).
  - (b) "The game's pricing file gives the lengths too." LEAK-38, as amended (Lennart, 2026-10-22: kick, expresso), rejects this argument once a conditional test measures the mechanism. The host's test file "is a holdout of the same snapshot, not deployment data". test_contrats.csv is the 2014 holdout of the same extract.
- **Precedents.**
  - frempl_french_motor_personal_line, in this run, has the same mechanism, and its dates locate the ends. It was fixed under LEAK-10 and LEAK-7. That fix is an AI fix pending the curator.
  - spanish_motor_insurance_coverage_level_2022_2024 reset the cancellations it could locate.
  - fremtpl2 kept the realised exposure (CC 2026-10-20). Its data cannot locate an early end, and the call came before LEAK-10's clauses of 2026-10-26.
  - The curator's "a feature" of 2026-10-30 came before the length was measured as realised (builder draft issue 1). A later measured finding supersedes an earlier reading (principles, Stages).
- **Remedy: fix the definition (LEAK-7).** Give every period that ends before 31 December the length known at its start, (31 Dec - start + 1) / 365 (/366 in 2012). Keep `exposure` as that column, described as the scheduled time at risk.
- **Use every early end, not only those with no later period.** Here "no later period" does not mark an exit:
  - only 18.4% of vehicle ids survive a year end, while fleet sizes hold (1.83 -> 1.82 vehicles);
  - 27.5% of "last" periods are followed the next day by a new id in the same contract;
  - the row names of the two files run exactly from 1 to 120,000, which suggests a sample (column audit, issue 3).

  frempl kept its continuing records because their changes are often planned, as at an anniversary. That does not hold here: 0.8% of periods end at an anniversary, and 76.5% of next-day cuts change no released column.
- **Cost.** LightGBM falls from 0.671 to 0.622, or to 0.630 if only the periods with no later period are changed.
- **The task survives the fix.** Covariates plus the start beat the start-known length alone on every window: 0.594 / 0.622 / 0.653 against 0.551 / 0.567 / 0.531. TP-4 holds; re-run the probes.
- **The only other way to keep the realised length** is to amend LEAK-10 for time on risk in insurance tables, decided together with frempl issue 2, spanish coverage and australian issue 2 (precedent check, prompt A (d)). A Must takes no exception.

**2. The README says the length is known at the prediction point (P3, USE-3, Must).**
- **Problem.** Two texts say the length is known at the start:
  - `task_summary.known`: "the period's start date and its length";
  - the first curation bullet: "Known then: ... the period's start and its length".

  Both contradict the definition's own potential-leak note and its fit_reason ("a period cut short is known only at its end").
- **Effect.** A user reads that every input is known at pricing, so the prediction point is misstated.
- **Evidence.** Claim audit #5; column audit, issue 2. australian_vehicle_insurance_2004_2005 corrected the same error after its panel (precedent check, item 9).
- **Remedy.**
  - After fix 1, write "the length to the year's end, known at the start".
  - If the curator amends LEAK-10 instead, write "the realised length (the time at risk), known only at the period's end for 58% of periods".
  - Either way, rewrite fit_reason and the potential-leak bullet.
  - Rewrite Decision 1. Its table compares claim shares within three-month bands of length, which hides the +23% (claim audit #41). Show claims per vehicle-year by how the period ends.

**3. Three windows inside one test year, on one train side: SPLIT-14 is met in letter only, and this is a first case (P4; SPLIT-14 and SPLIT-8 Must; SPLIT-10, SPLIT-11 and SPLIT-15 Should).**
- **Problem.**
  - The three windows share one refit.
  - They are cohorts of period length: rows are cut at 31 December, so a period that starts in September is at most 0.33 years long.
  - The precedents with one valid annual window went to `ForcedGroupedFromTemporal`: spanish coverage, pricing_game_2017_french_mtpl and frempl.
- **Effect.**
  - Each window's AUC ranks within one length cohort, so the mean runs below the year's pooled score (LightGBM 0.672 against 0.712).
  - The first and newest window, September to December, holds 7% of the exposure and 123 positives (SE about 0.027), yet weighs a third of the mean (split audit, issue 3; practitioner, gap 2).
- **Remedy: no re-split.**
  - The curator confirms that sub-windows of one dated test year, on the train side the annual refit gives, count as SPLIT-14's windows, and this is recorded as SPLIT-14's first Cases row. The daily dates set this case apart (split audit). If not confirmed, SPLIT-8 applies, grouped by contract (0.708 to 0.711).
- **In the splits_comment:**
  - Cite SPLIT-15, not SPLIT-17. SPLIT-17's trigger, under about 50 test rows per window, is not met: the windows hold 5,312 to 19,229 rows.
  - Record the exception to SPLIT-11: the tariff is refit once a year.
  - State the SPLIT-10 departure with its simulated bound in place of "cannot be measured". Simulated reporting delays of 30 and 90 days move the mean AUC by 0.003 or less, and a one-month gap would leave 48.7% of the rows in training. This is the third exception for that reason, so the amendment of prompt C is due.
  - Say that the window scores rank within start cohorts.
  - Reword "the call of 2026-10-30": the split was an AI suggestion, accepted with the curator's Yes.

**4. The metric origin is `fallback`, but the metric is a stand-in (P6, MET-11, Must).**
- **Problem.** The source had one evaluation, the 2014 price-aggregator market, and it cannot be computed: the other players' premiums and the 2014 claims were never published, and we changed the target. That is MET-11's stand-in case ("inputs not published, a task we changed"). The definition's own reason states both conditions.
- **Evidence.**
  - The rules, Sec. 4 (claim audit #34 and #35).
  - pricing_game_2017_french_mtpl, the same organisers' market game, declares `Metric.stand_in("normalized_gini", original=<the market profit>)`.
  - This record's suggested call of 2026-10-30 said "normalized Gini as the stand-in (MET-11)".
- **Effect.** No score changes. The README's origin line is wrong, and the two siblings are declared inconsistently.
- **Remedy.** `Metric.stand_in("roc_auc", original=<the 2014 market, rules Sec. 4>, reason=...)`. The reason should add two things:
  - ROC AUC ranks models as the normalized Gini does (2 AUC - 1);
  - how much of the score the period's length carries (the length alone scores 0.596 / 0.655 / 0.659 now; re-measure after fix 1).

  The practitioner's `log_loss` as a context metric is a weighing call for the curator, not part of this point.

**5. Statements the data refutes, and stale record fields (EV-2; USE-5 for `predicted`; records.md). Text and record only.**
- **"the insurer recovered its cost"** (`predicted` and the IDA bullet). Under IRSA, a recovery below 6,500 EUR is a flat amount, not the cost, and it exceeds the payment on 599 of the 1,190 IDA claims. 126 IDA claims are at 50% responsibility, so not all are not-at-fault (practitioner). Remedy: "claims settled under the IDA convention, where the insurer pays its client and recovers a flat amount from the other insurer".
- **"0.01 less for the rest".** All 2,099 of these rows are from 2012, the leap year: their length is days/366 (claim audit #15). The two rows with `n_vehicles` = 2 have doubled lengths.
- **"A contract holds up to 12 vehicles at once" and "42.8% ... no later period of the vehicle".** These count the file, which is likely a 120,000-row sample, not the fleet (column audit, issue 3).
- **The target bullet's reason, "the charges among claimants carry no signal".** It holds equally for the siblings that kept the amount (frempl, pricing_game_2017_french_mtpl, spanish_motor_insurance_2015_2018). Name what sets pg16 apart: charges scaled by one constant, an unexplained short tail, and 537 net-negative IDA periods (precedent check, item 1).
- **Record fields.** `problem_type: Regression`, the `Two-Regime Zeros` tag, and the CASdatasets-only `name` and `source_links` are stale (claim audit #46 and #47). The definition should also declare `accepted_check_warnings` for its three warnings.

**Not pressed (quality, P7, or no rule triggered; no reason against shipping):**
- `n_vehicles` is 1 on all but 2 rows; CLEAN-5 does not reach it.
- `insured_value_class` is 99.85% missing.
- The French labels are kept.
- The blind reviewer's typing concerns do not apply to the shipped frame: every class column is categorical there.
- Low headroom (one-hot GLM 0.7124 against LightGBM 0.7122, pooled) triggers no rule (TP-2, TP-3).

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate, rebuttal (2026-11-01): pricing_game_2016_french_fleet**

```text
Verdict: ship after changes. The critic and I now agree on the remedies. I withdraw my keep of the realised
  `exposure`: under LEAK-10 as written the LEAK-7 fix is the call, and an amendment stays the curator's
  family-wide option.
Conceded: points 1 (with one narrowing), 2, 3, 4, 5.
New fact (check r1): the realised length's gain is the time at risk itself. In a world where the end carries no
  information on the outcome it gains as much (+0.050 against +0.049 observed). This settles what the leak is, not
  whether it is one.
```

**Point 1, `exposure` (LEAK-10, Must): conceded, with one narrowing on what the leak is.**
- Why I concede:
  - LEAK-10 asks that a feature hold only what existed at the prediction point. The realised length of 58.2% of the
    2013 periods did not exist then.
  - The clause for window sums does not apply: the early ends move with the outcome (rate ratio 1.22).
  - My domain argument shows that actuaries use the realised exposure in scoring (the offset of the Poisson deviance,
    the exposure-weighted Lorenz curve), not as an input known at pricing. So it supports exposure as a scoring
    column (MET-2), not as a feature.
  - P3 does not excuse a Must. The tension row says: fix the leak and keep the task.
- The check (a script and its output in the run folder; the claim audit's features, windows and
  LightGBM parameters):
  - Method: draw claims as Poisson(rate from the covariates and the start x the realised length), 5 draws. In this
    world, how a period ends tells nothing about its claims.
  - Gain of the realised over the start-known length:

    | | Sep-Dec | May-Aug | Jan-Apr | mean |
    |---|---|---|---|---|
    | null world | +0.016 | +0.058 | +0.076 | +0.050 (sd 0.003) |
    | data | +0.041 | +0.054 | +0.051 | +0.049 |

- What follows from the check:
  - The +0.04-0.055 is the time at risk. It does not come from outcome information. The rate ratio of 1.22 does not
    raise the mean score (-0.001).
  - By window, the outcome link does show:
    - it lowers the gain in Jan-Apr: short periods there claim more than in proportion;
    - it raises the gain in Sep-Dec, outside all five draws, with 123 positives.

    So my "adds no ranking" holds for the mean only, not per window. That removes the scope test I proposed for an
    amendment.
- The leak note should name the mechanism as "the time at risk unknown at pricing", not "the claims ending periods".
- The 12.0% against 9.2% share of large charges bears on severity, not on this binary target.
- Narrowing of the remedy: use the claim audit's start-known length (`known_len`). Periods that end at a scheduled
  anniversary cut (0.8%) keep their realised length; every other early end gets its length to 31 December (/366 in
  2012). Otherwise `exposure` becomes a pure function of `period_start`, a copy (CLEAN-5's reasoning for `year`), and
  should then be dropped, as the column audit says.
- Agreed after the fix:
  - the cost: LightGBM 0.671 -> 0.622;
  - the task survives: covariates and the start score 0.594 / 0.622 / 0.653, against 0.551 / 0.567 / 0.531 for the
    start-known length;
  - re-run TP-4 and the window numbers in the notes.
- The amendment (prompt A (d)) stays the curator's to make, for frempl, spanish coverage, australian and pg16
  together. I no longer recommend it for pg16 alone.

**Point 2, the "known" text (USE-3, Must): conceded.**
- After the fix, write "the length to the year's end, known at the start" in `task_summary.known` and the first bullet.
- Rewrite `fit_reason`, the leak bullet (or remove it once the fix is in) and Decision 1, with claims per vehicle-year
  by how the period ends.

**Point 3, the windows (SPLIT-14 and SPLIT-8 Must; SPLIT-10, SPLIT-11, SPLIT-15 Should): conceded, no dispute left.**
- Same remedies as my point 3: a first SPLIT-14 Cases row for the curator, the SPLIT-11 exception, the SPLIT-10
  bound with prompt C's amendment, the SPLIT-15 citation, the cohort note, and the reworded "call of 2026-10-30".
- The check adds one fact to the cohort note: the windows differ in how the length acts (null gains +0.016 to
  +0.076). Per-window scores are therefore not comparable across windows. The cohort note should say so.

**Point 4, the metric origin (MET-11, Must): conceded.** Use `Metric.stand_in("roc_auc", original=<the 2014 market,
rules Sec. 4>)`. Add the Gini identity to the reason. Measure again, after the fix, how much of the score the period's
length carries.

**Point 5, statements and record fields: conceded, all of them.**
- IRSA's flat recovery and the 126 claims at 50% responsibility.
- The leap year 2012 (and the two rows with `n_vehicles` = 2).
- The "12 vehicles" and "42.8%" counts are counts of the file, which looks like a sample.
- A pg16-specific reason for the binary target: the charges are scaled, their tail is short and unexplained, and 537
  periods are net negative.
- The stale record fields, and `accepted_check_warnings` for the three warnings.

**What remains for the curator:** no dispute between us.
- The LEAK-7 fix, unless the curator chooses the family-wide LEAK-10 amendment (prompt A).
- The SPLIT-14 reading (first case).
- The SPLIT-10 amendment (prompt C).
- `log_loss` as context: a weighing call, MET-10.

</details>

<details><summary>Critic rebuttal</summary>

**Critic, rebuttal (2026-11-01): pricing_game_2016_french_fleet**

**Where we stand.** The advocate and I agree on the verdict (ship after changes), on the dataset staying, and on every text, label and record change. One dispute is left: what the panel recommends for `exposure`.
- The advocate recommends keeping the realised length by an amendment of LEAK-10.
- I recommend the LEAK-7 fix, because LEAK-10 as written decides it.

I ran one check, because it bears on the advocate's main argument for the keep. Script and output in the run folder.

**A1. The data is real and faithful (P5). Conceded.** One qualification: the row names of the train and test files run exactly from 1 to 120,000. This hints at a sample (column audit, issue 3). It means some statements count the file rather than the fleet ("up to 12 vehicles at once", "42.8% ... no later period"), which is my point 5. It does not touch the data's faithfulness.

**A2. A real pricing task, fit direct (P3; USE-1, USE-5, USE-8). Conceded.** The IDA wording ("a flat amount"; 126 claims at 50% responsibility) is the same fix as in my point 5. Fit stays direct under either remedy for `exposure`. The sentence in fit_reason, "measured to add no signal beyond the length", goes either way.

**A3. The split mirrors the application (P4). Conceded, narrowed on one word.**
- The advocate's record block says SPLIT-14 "holds". The split auditor and the precedent checker both say it is met in letter, as a first case, and needs the curator's confirmation and a Cases row. The advocate's own remedy list includes that Cases row.
- So the remedies are the same as in my point 3:
  - the SPLIT-14 Cases row;
  - the exception to SPLIT-11;
  - the SPLIT-10 departure with its simulated bound (amendment prompt C);
  - the citation of SPLIT-15 for SPLIT-17;
  - the cohort sentence.
- The advocate is right that the blind reviewer's windows aligned on years would break SPLIT-14 (30.4% train), and that its overlap worry does not apply to the fixed train side.

**A4. `exposure`. Contested on the keep; agreed on everything else.**

**What the advocate concedes.**
- The "known" text is false.
- The 31 December test could not fail.
- The part of the length unknown at the start adds +0.040 to +0.055.
- LEAK-38 rejects the argument from the host's test file.
- A keep needs an amendment, because a Must takes no exception.

What is left is which remedy the panel puts first. By the ranking it is the fix. Four of the advocate's reasons do not change that.

- **(i) "The outcome-linked part adds no ranking, by tests that could have failed."**
  - The LightGBM exit-flag test (0.671 against 0.670) could not fail, for the same reason as the 31 December test: the model has `period_start` and `exposure`, so it already holds the flag.
  - The Poisson offset test can fail, so I measured how much it can resolve. Same GLM as the column audit, trained on 2011-2012, early-end flag on and off:

    | | rate ratio of early ends [95% CI] | ROC AUC gain [contract-clustered 95% CI] | log loss |
    |---|---|---|---|
    | 2011-2012 (train) | 1.220 [1.123, 1.326] | | |
    | 2013 (refit) | 1.175 [1.051, 1.314] | | |
    | all 2013, out of sample | | +0.0009 [-0.0004, +0.0022] | lower in 93% of bootstrap draws |
    | per window, newest first | | -0.0055 / +0.0018 / +0.0009 | |

  - So the link holds in the test year. The early ends move with the outcome given the covariates known at the start, which is the condition under which LEAK-10's window clause would keep them: "unless the data shows the window's values do not move with the outcome". The AUC test can only resolve about ±0.0013, which is the size of gain this rate ratio predicts. "No measured gain" here means the test cannot see it, not that the link is absent (EV-6).
  - LEAK-10 also says that "a 'removing it changes no score' test alone is still no reason to keep" (2026-10-21).
- **(ii) "The domain's evaluation conditions on the time at risk."** Partly true, and it does not carry the keep.
  - In actuarial practice the earned exposure enters the score as an offset or weight: the Poisson deviance, or the x-axis of the Lorenz curve. The rate the actuary acts on is a function of the rating classes alone.
  - Here the realised length is a free model input under a metric that ranks periods. A risk-blind "rate times length" model already scores 0.637, which is 79% of the best model's lift. The practitioner says this is the part "I never need predicted".
  - The practice argues for the time at risk in the scoring. It does not argue for a test-time feature that did not exist when the period was priced.
- **(iii) "The fix answers a different question, frequency mixed with retention (USE-5)."** No conflict with USE-5.
  - The target does not change: it is the curator's per-period indicator (CC 2026-10-30), which already folds the period's length into the outcome. The practitioner accepted it as a close proxy of the rate.
  - The fix changes only what the model is told: the time at risk known at pricing. USE-5 is about the target, not the features, so the P3-over-P4 ranking is not triggered.
  - The retention blur is small and named. A feature unknown at the prediction point is a P4 Must.
- **(iv) "The only curator decision keeps it (fremtpl2, CC 2026-10-20); frempl and spanish are pending AI fixes."**
  - Conceded: frempl and spanish are not curator precedents.
  - But a newer curator decision covers this case. LEAK-10's second clause (Lennart, 2026-10-26) says late values "go where [they] can be located: they are blanked", and stay with a note only where they cannot be located.
  - fremtpl2 has no dates, so its early ends cannot be located. pg16's dates locate every one.
  - Principles: "A newer decision of the curator beats an older one", and rules win over precedents. The rule decides, not the AI fixes.

**The advocate's proposed amendment.** It would keep realised time at risk "when the outcome-linked part shows no gain".
- It rests on the test that my check shows cannot resolve the effect.
- It would replace the curator's measured condition ("do not move with the outcome") with a score test that LEAK-10 explicitly rejects.
- The +0.04 to +0.055 would still need the amendment to say outright that a time at risk unknown at pricing is an allowed feature in insurance tables (prompt A (d)). That would reach frempl, spanish, australian and fremtpl2 together.

That is a deliberate rule change for the curator. A panel does not recommend it as the remedy for one dataset.

**Recommendation, unchanged.**
- The LEAK-7 fix: the length to 31 December for every early end.
- Cost: LightGBM 0.671 to 0.622. TP-4 holds: covariates plus the start score 0.594 / 0.622 / 0.653, against 0.551 / 0.567 / 0.531 for the start-known length alone.
- The amendment is the curator's alternative.
- Agreed either way: rewrite `known`, the first bullet, fit_reason, the leak note (rate ratio 1.22, +0.04 to +0.055) and Decision 1 (claims per vehicle-year), and use 58.2%, not 42.8%.

**A5. Worth benchmarking (P6). Conceded.** Low headroom triggers no rule (TP-2, TP-3), as my brief said. TP-4 is re-run after the fix, and the numbers above show it holds.

**A6. The metric (P6). Conceded and agreed.** The origin becomes `stand_in` with the 2014 market as the original. `roc_auc` stays. The reason says how much of the score the length carries, re-measured after the fix. `log_loss` as a context metric is the curator's weighing call (MET-10).

**A7. The cleaning (P7). Conceded.** The remaining items are the leap-year clause, the stale record fields and `accepted_check_warnings` for the three warnings. They match my point 5.

```text
Verdict: ship after changes (agreed).
Disputed: `exposure`. LEAK-10 (Must) as written, with its 2026-10-26 clauses: fix by LEAK-7 (critic); keep only by a
  curator amendment of LEAK-10 for insurance time at risk (advocate). The early-end link replicates in 2013 (RR 1.175
  [1.05, 1.31]); the AUC test cannot resolve it (+0.0009 [-0.0004, +0.0022]).
Agreed: USE-3 wording; SPLIT-14 Cases row, SPLIT-11 exception, SPLIT-10 bound and prompt C, SPLIT-15 citation;
  MET-11 stand-in; IDA wording; record fields; warnings.
```

</details>
