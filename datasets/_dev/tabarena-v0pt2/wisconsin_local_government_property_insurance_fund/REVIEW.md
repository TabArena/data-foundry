# wisconsin_local_government_property_insurance_fund

**Outcome:** added. Settled on 2026-11-02 (the curator's verdict: changes, applied): three expanding yearly windows
(test 2008, 2009, 2010) in place of the member folds, whose leak test found the year's claim level shared across the
split; no gap; the 2008 window trains on 41% of the rows, below SPLIT-14's floor, on the curator's call (issue 1); the
claims in dollars (issue 2). The building-and-contents cover of Wisconsin's Local Government Property Insurance Fund,
2006-2010, from the open textbook Loss Data Analytics: 5,639 member-years of 1,227 counties, cities, towns, villages,
school districts and other members; the target is the year's claims in dollars (0 for 70.2%), the inputs are the fund's
rating variables, and the score is the source's Gini against the fund's premium. Validity: USE-1 holds (the fund's own
rating project, Lee 2017); USE-8 triggered, fixed (fit approximate: the training years carry final claim amounts the
fund knew only in part at renewal, as lending_club, and the public file lacks rating inputs); USE-6 holds (the premium
is the source's comparator, so it is a scoring column and never a feature, as 2_month_survival_rate_prediction; MET-2
bars a scoring column as a feature, and liberty_mutual_fire_peril_loss_cost issue 2 proposes a MET-2 amendment for a
weight that is also a feature, whose wording must keep this premium, the rating's output, a scoring column only);
LEAK-10 holds for every kept column; SPLIT-14 departed from on the curator's call (five policy years give three yearly
windows only if the 2008 window trains on 41%; issue 1), SPLIT-10 departed from (no gap, an exception serving SPLIT-14,
as pricing_game_2016_french_fleet); PROV-9 holds (rows first published 2017, a close extract of the paper's sample).
Value: MET-11 and MET-13 triggered, fixed (a stand-in for a computable metric replaced by the source's, a new library
metric); MET-5 holds (the Gini is argued, Spearman reported beside it); TP-4 holds (not `Trivial`), narrowly: on the
three yearly windows (test 2008, 2009, 2010) an untuned Tweedie GLM scores 0.254, 0.251 and 0.350 (mean 0.285) against
0.019, 0.195 and 0.540 for sorting by coverage alone (mean 0.251), which leads only in 2010, the storm year (re-measured
2026-11-02 on the shipped split; the panel's figures were on the member folds). TP-2 keep; re-read TP-4 on the first
benchmark run. Quality: CLEAN-10 triggered, fixed (`NoClaimCredit` missing without two earlier years; `Fire5`'s unknown
class kept with a note); dollars rather than CLEAN-16's log default (issue 2). Weighed: documented source and real
decision +; small test years, one claim that is 35% of 2010's losses, rating inputs the public file lacks (endorsements,
county, the full fire class), coverage alone ahead of the probed models in 2010, and a 2008 window that trains on 41% of
the rows -. Issues 1 and 2 are resolved; issue 3, the split (moved here from the rules PR on 2026-11-05), is open.

Changes made after the review panel (AI, 2026-11-01): the changes the panel agreed are made (the source's metric
`ordered_lorenz_gini`, new in the library, with `Premium` as base and scoring column; the target in dollars;
`NoClaimCredit` missing for the 2,412 member-years without two earlier years in the file; folds grouped by member,
`PolicyNum` the group and no feature; fit approximate; notes corrected, README regenerated). Changes after the
curator's marks (AI, 2026-11-02): the member folds replaced by three expanding yearly windows, no gap, `PolicyNum` an
input, `ForcedGroupedFromTemporal` dropped; every split figure re-measured. The panel's sections describe the
definition before these changes.

**Main points:** Open: issue 3, which split the five policy years get, moved here from the rules PR on 2026-11-05
(three windows with the 2008 window below SPLIT-14's floor, two windows, folds by member, or `No`). Issue 1 is resolved
by three expanding yearly windows (test 2008, 2009, 2010; train shares 40.6%, 60.6%, 80.3%), no gap, the 2008 window
below SPLIT-14's floor on the curator's call; issue 2 by the claims in dollars. The record's `year` is now 2017, and
its `required_split` (Temporal) and tag (Non-IID (Temporal)) match the definition.

**Issues for Andrej:**

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
       rows that every window must keep[^floor].
     - The rules send a release with too few periods to folds by member instead[^forced], but those folds share each
       year's claim level across the split, a leak measured on 2026-11-02.
     - The three windows were the call of 2026-11-02 (issue 1); the review of the rules PR took that call out of the
       rules on 2026-11-05 to be decided here, and a rule of this strength takes no exception, only a change of the
       rule[^must].
   * **Background:** The question and options A to D are Lennart's, in
     [PR #47's conversation](https://github.com/TabArena/data-foundry/pull/47#issuecomment-6659677982) (2026-11-05,
     moved from the closed #53); E is added from the rules (Recommendation). The shipped windows train on 80.3% (test
     2010), 60.6% (2009) and 40.6% (2008) of the rows, with no gap[^gap]. In folds by member the member id leaves the
     inputs[^group], and the test members are unseen in training, while the fund re-rates the members it knows.
   * **Effect on the task:**
     - A: the 2008 window trains on 2006-2007 alone, where the no-claim credit is unknown on every training row, so a
       third of the score comes from a training side unlike the fund's.
     - B: two windows, and the 2010 one rests largely on one claim (35% of the year's claims), so model comparisons
       lean on 2009.
     - C and E: unseen members are tested on the same years the training members cover; the year-level leak lifts the
       pooled score, and the folds rank LightGBM far below where the valid windows put it (Experiments).
   * **Experiments:**
     - On the shipped windows (test 2008, 2009, 2010; with the member id): untuned Tweedie GLM 0.254, 0.251, 0.350;
       LightGBM Tweedie 0.146, 0.254, 0.327; coverage alone 0.019, 0.195, 0.540.
     - The leak of the member folds (2026-11-02, untuned LightGBM, 9 folds): the test year's training rows add ROC AUC
       +0.010 for a claim (8 of 9 folds) and Gini +0.113 on the pooled folds (5 of 9); within one year only +0.002 and
       +0.008 (SD 0.20), so what crosses is the year's claim level, and dropping the year does not remove it.
     - The same inputs on every design (no member id; untuned; run for this issue): coverage alone, the Tweedie GLM
       and LightGBM score 0.368, 0.312 and 0.232 on the two valid windows (mean of 2009 and 2010), 0.251, 0.291 and
       0.215 on the three shipped windows, 0.318, 0.265 and 0.044 on the member folds pooled, and 0.209, 0.192 and
       -0.001 on the member folds scored within each year (SD over the 9 folds 0.06 to 0.17).
   * **Consistency:** california_house_prices_2020 dropped its window that trained on 25% rather than ship it[^cal].
     nba_players_2016_2019 and open_university_learning_analytics_dataset shipped folds by entity with one valid
     window each, and seven insurance tables of this batch ship forced splits. What sets this case apart: two valid
     windows exist, so a temporal split is possible with two windows instead of three.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Three yearly windows (implemented) | test 2008, 2009 and 2010; the 2008 window trains on 40.6% | three windows; no period shared across the split | breaks the floor, a rule without exceptions; the precedent dropped such a window |
     | B | Two yearly windows | test 2009 and 2010 only, trained on 60.6% and 80.3% | keeps the floor; closest to how the fund rates | two windows need a change of the three-window rule; the 2010 window rests on one claim |
     | C | Folds by member, the leak kept | member folds tagged forced from temporal; the year-level leak measured in the notes | what the rules prescribe for too few periods | a measured leak; unseen members; LightGBM near 0 against 0.23 on the valid windows |
     | D | `No` | retire the dataset | no departure | a forced split alone never retires a dataset; loses a documented public-sector pricing task |
     | E | Folds by member, scored within each year | C, with the Gini taken per year against that year's premium and averaged over the years | removes the year-level leak; one year's Gini, as the source scored | a per-year Gini in the metric library; LightGBM still near 0 |

   * **Recommendation:** E, the answer the rules give: a release with too few periods ships folds by member, and a
     leak found across them is removed where it can be[^leak], which scoring within each year does; C only if the
     per-year Gini cannot be had. A and B each need a change of the floor rule. If the cost of the member folds
     decides for you (LightGBM near 0 against 0.23 on the valid windows), B is the change the facts support, since two
     valid windows exist, while A has a precedent against it. D is not what the rules ask. **Decision:** A, B, C, D
     or E?

   [^floor]: **SPLIT-14** (Must): a temporal task has at least 3 windows, and no window's train side holds less than
     50% of the data; "A task that cannot meet it ships under SPLIT-8".
   [^forced]: **SPLIT-8** (Must; narrows SPLIT-14), reworded 2026-11-05 (Lennart): a release with too few periods for
     three windows ships in the closest regime that keeps the rows, grouped by the entity when the periods are stacked
     and the entities recur (`ForcedGroupedFromTemporal`), with the cost measured against the valid windows; "Being
     forced alone never makes a dataset `No`".
   [^must]: principles.md, "Exceptions and amendments": "A Must has no exceptions: only a higher-ranked Must overrides
     it, and anything else is an amendment."
   [^gap]: **SPLIT-10** (Should): no gap here, an exception that serves SPLIT-14, as in pricing_game_2016_french_fleet.
   [^group]: **LEAK-33** (Must): a group id column is split metadata, never a feature.
   [^cal]: **SPLIT-14**, Cases: california_house_prices_2020 (2026-10-21), whose `min_train_fraction=0.25` let the
     oldest window train on 25% of the rows; its windows now train on 50%, 67% and 83%.
   [^leak]: **SPLIT-8**: "A leak found is weighed case by case like any other: removed where it can be, otherwise the
     task may still ship as an approximate fit with the leak measured in the notes." **LEAK-6** (Must): "a confirmed
     leak goes even when small". **MET-2** (Must): the metric means on our task what it meant on the source's, whose
     Gini compares the members of one year (2011) against that year's premium.

   **Notes for the AI:** A: an amendment of SPLIT-14 for a floor below half (wording and Cases row with the curator);
   the definition stays. B: an amendment of SPLIT-14, e.g. "a temporal task whose release gives exactly two windows,
   both training on at least half the rows, ships those two; fewer go to SPLIT-8" (issue 1, option (a));
   `TemporalSplits(window=1, unit="unique", n_windows=2)`, the no-gap exception kept. C: `Grouping(on="PolicyNum")`
   per row, no `temporal`, tag `ForcedGroupedFromTemporal`, `PolicyNum` the group and no feature, the leak test's
   numbers in `splits_comment`, a SPLIT-8 Cases row; `task_time_on_few_unique` no longer fires. E: as C, plus a library
   metric for the mean of per-group ordered-Lorenz Ginis (MET-12 name such as `mean_group_ordered_lorenz_gini`, tested
   against a loop over `ordered_lorenz_gini`, timed; MET-13), `Year` copied in `_clean` to a scoring column of role
   `group` (`Year` stays a feature, MET-2), `inputs={"weight": "Premium", "group": "<copy>"}`. D: record `No` with its
   marker.

**Review panel:** ship after changes (mediator). Claim audit: 38 claims, 32 hold, 6 refuted or partly refuted (the
metric origin, `NoClaimCredit`'s zeros, the close extract and the stale README fixed here; TP-4 settled by the
mediator's check; the record's year and claimant count at hand-over), 3 untested. Blind review: include with changes;
main concerns `NoClaimCredit`'s zeros for missing history and `PolicyNum` as a feature, both changed. Debate: agreed on
the source's metric, the target in dollars, `NoClaimCredit` set missing, the fit approximate and the note corrections;
TP-4 settled by the mediator's check; disputed: the split (issue 1).

<details><summary>Mediator</summary>

**Mediator (2026-11-01): wisconsin_local_government_property_insurance_fund**

**Recommendation**

```text
Verdict: ship after changes.
Validity: USE-1 holds (the fund's own rating project, Lee 2017 Ch. 1); USE-8 triggered, fixed (fit approximate: the
  training years carry final claim amounts, as lending_club; under the re-split also held-out members of the same
  years for next year's renewals); USE-6 holds (the premium is the source's comparator: a scoring column, never a
  feature, as 2_month_survival_rate_prediction); LEAK-10 holds for every kept column; SPLIT-14 triggered (two
  windows), fixed as SPLIT-8 is written (grouped by member, ForcedGroupedFromTemporal); an amendment that keeps the two
  yearly windows is the curator's (issue 1); PROV-9 holds (first published 2017; a close extract of the paper's sample).
Value: MET-11 and MET-13 triggered, fixed (the source's premium-base Gini declared, Premium a scoring column, a library
  metric added); MET-1, MET-2 and MET-5 hold; TP-4 holds (decisive check below: a tuned model beats coverage alone in
  2009, so `Trivial` is not met fold by fold; coverage leads in 2010); TP-2 keep.
Quality: CLEAN-10 triggered, fixed (NoClaimCredit missing without two years of history in the file; Fire5's -99
  noted); CLEAN-16 departed from (dollars: the metric reads the predictions' scale; exception serving USE-5, issue 2).
Weighed: source + (paper, dissertation, textbook), use case +, gap 0; size - (test years of about 1,110 member-years),
  noise - (one 2010 claim is 35% of that year's losses; bootstrap SD of the premium Gini 0.05-0.11 per window), inputs -
  (endorsements, county and the full fire class are not public).
For the curator: issue 1, a rule call (keep the forced grouped split, or amend SPLIT-14), decided with australian
  issue 1 and frempl issue 5; issue 2, confirm dollars against the family scale question (australian issue 5).
```

**Agreed facts** (both sides and the evidence reports; numbers re-checked where marked)

- 5,639 member-years of 1,227 members (1,038 in all five years), 2006-2010; 70.2% zero claims, none negative, largest
  $12.9M (35.2% of 2010's claims); 2010 holds $36.7M against $11.0-20.5M in the other years.
- The rows are the textbook's file, pinned by sha256, first committed 2017-06-27; a close extract of the paper's sample
  (5,639 against 5,660 rows, 1,679 against 1,684 claimants); yearly totals match CLAIMLEVEL.csv within $1 for 5,633 of
  5,639; only closed claims are kept (LEAK-24, untested; 2010 shows no deficit).
- `Freq`, `lny`, `yAvg` restate the target; `BCcov`, `Deduct` are exact transforms of the log columns; the flag merges
  are lossless; no kept input moves with the year's claims (coverage, deductible, alarm credit).
- The premium is 98.1-98.5% explained by the rating variables; its residual ranks claims at ROC AUC 0.52-0.55; the
  source scores models against it (Frees, Lee and Yang 2016, Sec. 6.2) and fits on the rating variables only.
- `NoClaimCredit` equals "no claim in the two years before" wherever both years are in the file, and is 0 in all 2,412
  rows without them (all of 2006-2007); setting them missing moves untuned scores by -0.029 to +0.007 Gini.
  `Fire5` codes fire class -99 (unknown) as 1 for 48 claimant members; locatable only among claimants.
- Windows: test 2010 trains on 80.3%, test 2009 on 60.6%, a 2008 window would train on 40.6%; 403 and 301 claimants;
  98.6% and 97.6% of test members seen in training. Grouped by member instead: R^2 optimistic by 0.014-0.026, same model
  order; the member id and history features add nothing measurable. The label delay cannot be measured (no report
  dates).
- No registered library metric computes the source's Gini (checked below).
- Fit on dollars, models score higher under the premium base on the mean of the two windows for all four families; the
  source models dollars (Tweedie, GB2).

**Decisive check: TP-4** (scripts and outputs in the run folder; threads capped)

Shipped features with the agreed changes (target in dollars, `NoClaimCredit` missing without history). Methods:
LightGBM Tweedie with 36 configurations chosen on the year before the test year (grouped: on held-out training
members) by the premium-base Gini; Tweedie GLM with alpha chosen the same way; CatBoost Tweedie and LightGBM on log1p
at defaults. Raw feature as TP-4 asks: the best single feature on each training side as a monotone fit (it was
`LnCoverage` on every split), and coverage in dollars as the probes used it. These are tuned proxies; the benchmark has
no tuned results for this dataset yet (TP-1).

| split | coverage ($) | raw feature (train-chosen) | best method | premium-base Gini, best minus coverage (bootstrap P(method ahead)) |
|---|---|---|---|---|
| 2009 | 0.195 | 0.141 | LightGBM Tweedie tuned 0.327 | +0.138, SD 0.073 (0.98) |
| 2010 | 0.540 | 0.461 | Tweedie GLM 0.350 | -0.183, SD 0.051 (0.002) |
| grouped 3x3 | beats the best method on 2 of 9 | beats it on 2 of 9 | | |

Normalized Gini (the stand-in): 2009 LightGBM 0.753 against coverage 0.742 (P 0.79); 2010 coverage 0.760 against at
most 0.710. Methods spread widely under the premium base (2009: -0.04 to 0.33), partly because it reads the
predictions' scale.

Reading: TP-4 makes `Trivial` need the raw feature to match or beat the methods on every fold. It does not in 2009
(as sepsis_survival, kept at 0.704 against 0.707), nor on 7 of 9 grouped folds. So TP-4 holds and TP-2 keeps the task.
The 2010 lead is the storm year's shift (claims tripled, coverage fell for 68% of members); it goes into the metric
reason as the level a model must beat. Re-read TP-4 on the first benchmark run.

**Library check (MET-13).** `normalized_weighted_gini(y, p, weight=Premium)` sorts by the raw prediction and weights
the target by the premium: a different curve. Only with the inputs transformed (target y/P, prediction p/P, weight P)
does it equal the source's Gini times a per-fold constant (claim auditor, test 6), and a spec cannot express that
division. The unnormalized helper `_weighted_gini(y/P, P, p/P)` equals minus the source's Gini exactly (3 random
scores, to 6 decimals). Missing: a registered metric with a general name (`ordered_lorenz_gini`, MET-12) and a `base`
input role that sorts by prediction / base ascending, accumulates base share against loss share, groups ties (the
premium as its own score gives 0), and is not normalized (the source reports the raw index, Frees, Meyers and Cummings
2011); with the MET-13 tests (equal to an independent implementation of the 2011 definition or `cplm::gini` on random
inputs, one hand-computed case, timed on 1M rows). The same metric with the exposure as base is frempl issue 4's
alternative.

**Changes to make now (no decision needed)**

1. Metric (MET-1, MET-2, MET-11, MET-13, Must; MET-5): add `ordered_lorenz_gini` to the library as above; declare
   `Metric.source("ordered_lorenz_gini", inputs={"base": "Premium"})` with `Premium` a `ScoringColumn`, never a
   feature; the reason names Spearman (Sec. 6.1, Table 18) as the second reported measure, coverage's score as the
   floor, and the one 2010 claim's effect. Reword `task_summary.use_case` to the decision it scores (set each member's
   premium relativity; a rating is adopted when it moves premium toward members whose claims outrun it).
2. Target in dollars, `bc_claims`, `target_transform` identity (MET-3; departs from CLEAN-16, issue 2); the notes give
   this dataset's reason, not "the family's log1p".
3. `NoClaimCredit` missing for member-years without both earlier years in the file, 2,412 rows (CLEAN-10; house_sales);
   `task_summary.known` corrected; one sentence on `Fire5`'s -99 kept as published (LEAK-10 outranks CLEAN-10).
4. Split (SPLIT-14, SPLIT-8, Must): `Grouping(on="PolicyNum")` per row, tag `ForcedGroupedFromTemporal`, `PolicyNum`
   out of the features, `Year` kept; `splits_comment` states the two valid windows and the measured cost, that the
   grouped folds test members new to the model (1.4-2.4% of real test rows), and that a 2011 file would allow the
   temporal design. Issue 1 holds the alternative.
5. Fit `approximate` (USE-8, Must; lending_club): `fit_reason` names the forced split and the final training amounts;
   the absent endorsements, county and full fire class as limits of the public file.
6. Text (EV-7, PROV-9, LEAK-24, SPLIT-20): 97.6-98.6% of test members seen; coverage fell for 67.7% of members in 2010
   (median -2.6%); "a close extract of the paper's sample"; the book's closed-claims selection quoted; the test years
   are the lowest and highest claim years and one claim reorders models. Re-run `dataset check` (the README's metric
   text is stale). Record at hand-over: year 2017, 301 and 403 claimants, the screening's R^2 superseded.

**Changes that need the curator**

1. P4, SPLIT-14 / SPLIT-8 (Must): keep the forced grouped split (implemented) or amend SPLIT-14 so the two yearly
   windows ship. See the dispute below and issue 1 of the review draft.
2. P7, CLEAN-16 (Should) against MET-3 and USE-5: confirm dollars, an exception, while australian issue 5 asks for one
   scale for the insurance family and lists this dataset as log1p.

**Disputed points**

1. *Split.* The advocate rests on SPLIT-4 (Must: the split follows what the task does; the fund re-rates known members)
   with SPLIT-19 (Should: the source tested the next year). The critic rests on SPLIT-14 and SPLIT-8 (Must). Not a
   conflict that rank resolves for the advocate: SPLIT-14 fails on its own (two windows), and SPLIT-8 is the remedy it
   names. SPLIT-8 says it narrows SPLIT-14 and USE-10, the known-entity rule that SPLIT-4 applies here, and covers "a
   release with too few periods for three windows"; nba_players_2016_2019 (players who recur and are predicted again)
   was grouped under it. So the rules as written give the re-split, the "fix the definition" rung; nothing calls for
   exclusion. Keeping the two windows is an amendment, which only the curator makes. What sets the case apart from the
   SPLIT-8 cases is real (two windows above the floor, where each had one) but does not meet SPLIT-14's three. The
   choice matters beyond the usual scores: the grouped split hides the 2010 shift, under which coverage outranks every
   model, and the temporal windows show it. Recommendation: the re-split if Andrej ships forced regimes in australian
   issue 1 and frempl issue 5; the amendment if he rejects them there, since here a temporal split exists and his
   how_much_did_it_rain words ("a temporal split is not possible") do not reach it.
2. *TP-4.* Settled by the check above: not `Trivial` (2009 and 7 of 9 grouped folds); keep (TP-2).
3. *Fit (USE-8).* The critic's rebuttal still lists it, but the advocate's rebuttal conceded `approximate`. Settled:
   approximate, as lending_club; the short-tail argument is inference (EV-2) and the book's cut before 2011 "to mitigate
   the effect of open claims" points the other way.
4. *MET-5* (raised by the precedent checker as a weighing). Settled by the rule's text: a paper's metric is the source's
   when the paper "argues why it fits the decision". Frees, Lee and Yang argue the Gini ("measure the satisfaction of
   the fund manager"; zero masses make "traditional metrics less helpful"), and Lee 2017 concludes by it, as
   forest_fires and labour_inspection_compliance. Lennart's "multiple metrics ... fall back" covers papers that name no
   deciding metric (gallstone_disease). Origin `source`.
5. *`NoClaimCredit`.* The column auditor leaned to a note (the source's own form, no measured gain); the advocate and
   critic agree on the fix. CLEAN-10 keeps a code only "when it means something"; here the 0 means only that the history
   is not in the file, and a linear model reads it as "had a claim" (house_sales's reason). Fix.

**Consistency with precedent** (precedent checker's checks A-D)

- A, split: the re-split follows SPLIT-8's cases (nba_players_2016_2019, open_university, distribution_transformers;
  frempl, pricing_game_2017_french_mtpl and spanish_motor_insurance_coverage_level_2022_2024 in this batch). The
  amendment departs from them on the fact named above, recorded as an amendment, never an exception. Under the
  amendment the no-gap exception to SPLIT-10 returns as the third for SPLIT-14's floor (lending_club,
  alfa_battle_2_0_task_2), and the precedent checker's amendment wording becomes due.
- B, metric: the stand-in departed from MET-11 and MET-13; the change follows g_research_crypto_forecasting_1m,
  numerai_v5_2_1m, rossmann_store_sales and liberty_mutual_fire_peril_loss_cost (custom metric with its scoring column,
  added with the dataset).
- C, fit: approximate follows lending_club.
- D, target scale: dollars follows Andrej's policy call 3 (per dataset) and australian's implemented dollars; it departs
  from the log1p tables (frempl, both Spanish tables, allstate_claim_prediction_challenge_1m) on one fact: this metric
  divides each prediction by the premium, so the scale counts, while their normalized Gini reads only the order. Issue
  2, because australian issue 5's family call is open.
- Text elsewhere goes stale with these changes: australian issue 4 (lists this dataset as a stand-in) and issue 5 (as
  log1p), frempl issue 4 ("needs a general metric in the library").

</details>

<details><summary>Claim audit</summary>

**Claim auditor (2026-11-01): wisconsin_local_government_property_insurance_fund**

Verdict: ship after changes. Most of the data claims hold, re-measured on the shipped frame and the raw files. Four
claims fall: the metric declaration breaks MET-11 and MET-13 (Must); under that metric `LnCoverage` alone matches or
beats every model I tried, tuned ones included (TP-4, Must, still to be checked with the benchmark's tuned methods);
`NoClaimCredit` is 0 in every row of 2006-2007, which the notes and "known" do not say (CLEAN-10); and the file is a
close extract of the paper's sample, not the same one. The split's departure from SPLIT-14 and SPLIT-8 (Must) is
stated in the definition and is the split-auditor's to settle; I confirm its numbers.

Scripts and outputs are in the run folder (seven test scripts, and the source of the book's chapter). Every model number below comes from the shipped frame (`to_container()`) and its two splits (test 2009 and
test 2010), scored by `data_foundry.v2.metrics` unless marked "builder" (the builder's probe files, EV-8). All models
are untuned unless marked "tuned proxy": a grid chosen on the year before the test year by the declared metric. That
is not the benchmark's tuned methods (TP-1).

**Claims and tests**

| claim | source | test | result | evidence | rule |
|---|---|---|---|---|---|
| 5,639 member-years, 1,227 members, 1,038 in all five years | task_summary.row | counted on the shipped frame | holds | 5,639 / 1,227 / 1,038 | EV-7 |
| 0 for 70% of rows, none negative, up to $12.9M | task_summary.predicted, notes | expm1 of the target | holds | 70.23% zeros, 0 negative, max $12,922,217.84 | EV-7 |
| 2010: $36.7M against $11.0-20.5M; one water damage claim at a Milwaukee school is 35% of the year | notes (anomaly) | yearly sums; CLAIMLEVEL's largest line | holds | 20.46 / 17.25 / 12.07 / 11.05 / 36.66 $M; member 138300 (School), `waterdamagetoschool`, county Milwaukee, 35.25% of 2010 | EV-7 |
| 2010 was a year of severe weather (Lee 2017, Ch. 1) | notes | read Lee 2017 | holds | "in recent years due to severe weather events in 2010, the surplus ratio was approaching the target rapidly" | EV-2 |
| `Freq`, `lny`, `yAvg` restate the target | notes | the definition's own assert; explore1 | holds | `Freq == 0` exactly where `y == 0` (the assert passes in `_clean`) | LEAK-10 |
| `LnCoverage` = log coverage in millions within 5e-10; `lnDeduct` = log deductible | notes | max abs difference | holds | 5.0e-10 and 5.0e-9 | CLEAN-5 |
| One flag of each block per row, merge lossless | notes | the definition's asserts | holds | asserts pass (5,639 rows) | CLEAN-13 |
| First two digits of `PolicyNum` are the entity type | notes | prefix by entity crosstab | holds | 12 County, 13 School, 14 City, 15 Town, 16 Village, 18 Misc; no off-diagonal cell | CLEAN-3 |
| `NoClaimCredit` is 1 exactly when no claim in the two years before, wherever both are in the file; history known at rating, never the year's own claim | notes; task_summary.known ("whether it had a claim in the two years before") | crosstab against claims one and two years before; by year | partly refuted | the two-year rule is exact (1,852 / 0 and 0 / 1,375), and a one-year rule fails (1,302 rows with no prior-year claim lack the credit). But the credit is 0 in **every** row of 2006 and 2007 (share 0.000 and 0.000, then 0.548 / 0.549 / 0.565): 73.2% of the 1,122 rows of 2007 had no 2006 claim and none holds the credit. So for 2,292 rows (40.6%) the 0 means "history not in the file", not "had a claim". That is 67% of the 2009 window's training rows and 51% of the 2010 window's. Setting them missing changes untuned scores little (normalized Gini -0.029 to +0.007, R^2 on log1p -0.003 to +0.001). Lee 2017 Table 5.8 says "no BC claims in prior year", the book says "past two years"; the data side with the book | CLEAN-10, EV-2 |
| `Fire5` is 1 when the fire class (0 to 10) is below 5 | notes | CLAIMLEVEL's class column against the flag | holds, with a caveat | classes 0-4 give 1 and 5-9 give 0, no exception. The missing code -99 also gives 1 (102 claim lines, 66 member-years, 48 members), and codes 40/50/80/90 occur. Non-claimants cannot be checked or repaired (CLAIMLEVEL covers claimants only) | CLEAN-10 |
| The year's coverage is set before its claims: +0.059 with a claim, +0.061 without, +0.052 top 10% | notes | log-coverage change into year t by the claim in t | holds | +0.0586 / +0.0614 / +0.052; medians +0.052 / +0.051 | LEAK-10 |
| (implied) deductible and alarm credit are set before the year's claims | dataset.py inputs | change into t and t+1 against the claim in t, logit adjusted for size and type | holds | alarm change into t z = +1.34, into t+1 z = -0.83; deductible z = -0.17 and +0.39 | LEAK-10 |
| CLAIMLEVEL: 6,258 BC claims, all closed; totals match within $1 for 5,633 of 5,639; 4 of 6 others look duplicated | notes, decision 2 | join and inspect the 6 | holds in substance | 6,258 lines, all `Closed`; 5,633 match. Of the 6: 3 repeat one line exactly (120013/2007, 120015/2009, 140073/2006), 2 sum to exactly twice `y` (120013/2008, 120017/2009), 1 differs by $3. One line (160856/2008) has no member-year in the insample | PROV-13 |
| County named only for the 759 members with a claim, so not joined | notes | members in CLAIMLEVEL | holds | 759 members (758 with `y > 0`, plus 160856 whose only line is in a year missing from the insample) | LEAK-10 |
| Premium: linear R^2 0.981-0.985 on the rating variables within each year; with it, untuned models change by -0.02 to +0.06 | notes, decision 1 | the decision's table; the builder's metric probe | holds | 0.981-0.985; differences -0.016 to +0.055 | USE-6 |
| Premium held out as the comparator, as in 2_month_survival_rate_prediction | notes, changes | Frees, Lee and Yang (FLY) 2016 Sec. 6.2; USE-6 case table | holds | "This means we are looking for improvements over the original premium scores used by the LGPIF"; a rating engine cannot take its own output as a rating variable | USE-6 |
| The source models the log forms of coverage and deductible (Lee 2017, Table 5.8) | notes | read Table 5.8 | holds | `lnCoverageBC`, `lnDeductBC`, `NoClaimCreditBC`, `EntityType` | EV-2 |
| The rows are "the data Frees, Lee and Yang (2016, Sec. 5) model" | notes, first line | the paper's Table 1 and Lee's Tables 5.7-5.8 against the file | partly refuted (minor) | paper's BC sample: 5,660 rows, 1,684 with claims, 4,992 claims, mean coverage 37.050M. File: 5,639 rows, 1,679 with claims, Freq sum 6,255, mean 37.281M. The `NoClaimCredit` mean matches (0.328 / 0.3286). A close extract, not the same one | PROV-9, EV-2 |
| First published 2017-06-27 (first commit); files unchanged on master (32310ad); the 2011 hold-out is not public | download_description, notes, splits_comment | GitHub API (no login); both repos' Data folders; one web search; the fund's site | holds | commit 38859ed (2017-06-27T20:16:24Z, "first commit") adds both files, the only commit on either file; master head 32310ad. No 2011 file in either Data folder, none found by search, no data on the project site. sha256 of both raw files matches the definition | PROV-9 |
| Insample.csv byte-identical; WiscPropFund.csv (LDAVer2) holds the same rows | download_description | sha256; merge on keys | holds | identical hash; 5,639 of 5,639 keys; Premium, Deduct, BCcov, Freq, Fire5, NoClaimCredit equal; `BCClaim == y` | PROV-4 |
| No licence | `license = None` | GitHub API; book index | holds | `license: null`; the book calls itself "freely available", an OER, with no terms (not a factor: EV-4) | EV-4 |
| Split: test 2010 on 80%, test 2009 on 61%; a 2008 window would train on 41%; 98-99% of test members seen | splits_comment, decision 3 | shipped splits | holds | 0.803 / 0.606 / 0.406; seen 0.986 (2010) and 0.976 (2009); 403 and 301 positives | SPLIT-13, SPLIT-14 |
| Two windows, "not the three SPLIT-14 asks for" | splits_comment | rule text | holds as a fact; the shipped split breaks a Must | SPLIT-14 and SPLIT-8 are Must and have no exceptions (principles.md); the definition ships two windows pending the curator's call | SPLIT-14, SPLIT-8 |
| (implied) no row is a copy across the split | definition | leak probe; keys | holds | (PolicyNum, Year) unique; exact copy share 0.0. The near-key overlap (74.4%) is the same member, which the use case scores | LEAK-16, SPLIT-13 |
| Both parts carry signal: claim AUC 0.77-0.79 (coverage alone 0.74), claimants' log R^2 0.10-0.22 | notes | the builder's hurdle check | holds | 0.766-0.790; 0.736-0.745; 0.098-0.224 | TP-2 |
| Amount and log1p "trade places by year", so log1p stays | notes | the builder's scale probe, declared metric | holds loosely | on the amount, all 4 families score higher in 2010 and 2 of 4 in 2009 (6 of 8). The one large reverse is LightGBM in 2009 (0.633 log1p against 0.469). The scale is the definition's choice (MET-3) | MET-3 |
| Metric: the source's metric is the premium-base Gini (FLY Sec. 6.2; Frees, Meyers and Cummings 2011) | `metric.original`, `reference` | read FLY Secs. 3, 6.1, 6.2 and Lee 5.1.6-5.1.8 | holds, borderline; omission | the Gini is argued ("measure the satisfaction of the fund manager with each score"; Sec. 3: "large masses at zero ... traditional metrics are less helpful"), and Lee 5.1.8 concludes by it. But the source reports Spearman's correlation first (Sec. 6.1, Table 18; the premium at 42.59%), and the reason does not name it | MET-5, MET-11 |
| Constant-base Gini ranks models exactly as `normalized_gini` (tau 1.0) and was used by Frees and Lee on this fund | `metric.reason` | algebra; re-computed taus; FLY ref. [59] | holds | the constant-base ordered-Lorenz Gini is 2 x the raw Kaggle G, and `normalized_gini` divides G by a per-fold constant; tau 1.000 in 2008, 2009, 2010. FLY: "in [59] ... a constant premium is used as denominator" | MET-11 |
| The two bases rank the same 8 scores at tau -0.07 to 0.79 | `metric.reason` | re-computed from the builder's metric probe rows | holds | -0.071 / 0.000 / 0.786; against Spearman, the source's other measure, `normalized_gini` ranks them at -0.429 / -0.214 / -0.786 | MET-11 |
| Stand-in, because "the library has no ordered-Lorenz Gini with a base yet (MET-13)"; README: "a stand-in for the source's metric, which cannot be computed" | `metric.reason`, README Metric block | MET-11 and MET-13 text; implementation test | **refuted** | the reason itself says the original can be computed, which contradicts the stand-in origin (MET-11: stand-in only when the original cannot be computed on our data). MET-13 requires the custom metric in the same change, so it is no reason to postpone. The stand-in is also not close (taus above). Test 6: `normalized_weighted_gini(y/P, s/P, weight=P)` equals the source's Gini times a per-fold constant (1.177 in 2009, 1.122 in 2010; tau 1.0 over 40 random scores per window), so the original is a thin wrapper over tested library code | MET-11, MET-13 |
| Computable on every fold (MET-2) | declared metric | dummy and perfect predictions through `scorer` | holds | constant prediction 0.0000 in both windows, perfect 1.0000; 301 and 403 positives; no inputs needed | MET-2 |
| Metric on the amount (`target_transform="log1p"`) | `metric` | scorer against `normalized_gini` on `expm1` values | holds | identical values (coverage 0.742 / 0.760 both ways) | MET-3 |
| (implied) the task is not trivial under its metric | metric + notes | `LnCoverage` alone against untuned and tuned-proxy models, by window; paired bootstrap (500) | **refuted pending TP-1** | 2009: coverage 0.742; tuned proxy LightGBM 0.749, Tweedie GLM 0.746; best untuned a hurdle GLM 0.764 (+0.024, SE 0.018, P(> coverage) 0.91). 2010: coverage 0.760; tuned proxy LightGBM 0.683 and GLM 0.729; best of 72 LightGBM configs picked on the test year 0.695, best GLM 0.729; untuned Tweedie GLM -0.045 against coverage (SE 0.016, P 0.00). Without the $12.9M claim coverage still leads in 2010 (0.821 against 0.795). Under the original base the same happens in 2010 (builder: coverage 0.540, best model 0.385). Spearman puts models above coverage in both years (builder: 0.448 / 0.513 against 0.389 / 0.446). The notes do not give coverage's score, which the siblings give as "the level a useful model must beat" | TP-4, TP-1, MET-10 |
| README metric definition "(ties in row order)" | README Metric block | the container's spec now | refuted (house) | the library now groups ties ("a constant p scores 0"); metrics.py was changed after the README was generated (13:31 against 14:14). Scores of continuous predictions do not change | pipeline (generated README) |
| Use case real; the source built a rating engine; fit direct | task_summary | Lee 2017 Ch. 1 | holds | "implementing a more accurate and cost efficient rating engine was mutually agreed to be the primary goal"; the team presented one to the fund. The fund has since closed (its site: "Fund To Close"); the decision was real | USE-1, USE-8 |
| (implied) the member's history beyond `NoClaimCredit` adds nothing | known inputs | earlier claims built from earlier rows (last year's log claims, count and share of claim years, mean) | holds | R^2 on log1p +0.007 to +0.010; normalized Gini -0.095 to +0.051, mixed sign: no case for CLEAN-19 | CLEAN-19, USE-10 |
| Record: year 2016; "about 400 positives each"; positives R^2 0.25 | record (front matter, screening) | against the definition and the splits | refuted (minor) | the definition says 2017 (the builder's PROV-9 change is not in the record); 2009 has 301 positives; the R^2 is 0.10-0.22 now (a later stage supersedes it, EV-2) | PROV-9, EV-2 |
| Warnings proposed: `task_time_on_few_unique`, `meta_license_unknown`, `task_target_value_dominant` (70.2% real zeros) | builder report | as above | hold | 5 years; no licence; zeros are no-claim years (Freq = 0), not a cap or placeholder | TP-9, EV-4 |

**Untested claims**

| claim | why untested | bound |
|---|---|---|
| The target is the year's full claim cost | the book selects "only claims that are closed, with obligations fully met". Claims still open at extraction are missing from `y`, which would censor the newest year (LEAK-24). There is no extraction date and no second extract | 2010 has the highest claim share (36.3%) and total, so no deficit shows. The notes' "all closed" reads as completeness, not as a selection |
| `NoClaimCredit` of the test rows was known at rating time | no claim dates in CLAIMLEVEL | 10.4% (2009) and 12.5% (2010) of the test rows lose the credit only through a claim in the year just before; a late claim there is the only way it could differ from what the fund knew |
| `Fire5` for non-claimants with a missing class | the class is published for claimants only | at least 48 members carry -99 as `Fire5 = 1` |

**Refuted and untested, ranked (principles.md: validity first, Must first)**

1. P4, SPLIT-14 and SPLIT-8 (Must; stated in the definition, the builder's issue 1). Two windows. A Must has no
   exception, so this ships only after an amendment of SPLIT-14 for short panels of known members, or a re-split
   (`ForcedGroupedFromTemporal`). The facts hold: the 2008 window trains on 40.6%, and 97.6-98.6% of test members are
   seen. This changes the regime or a rule, not the data. Mildest remedy: the curator's amendment (option (a)), with
   this case as its Cases row.
2. P5/P7, CLEAN-10 (Should): `NoClaimCredit` is a placeholder 0 in all 2,292 rows of 2006-2007. "Known: whether it
   had a claim in the two years before" is false for those rows. For the 2009 window, two thirds of the training rows
   carry it. It changes what the feature means and little of the scores (Gini -0.029 to +0.007). Mildest remedy: set
   it missing for `Year < 2008`, or at least say in the notes that it is 0 for every 2006-2007 row because the file
   holds no earlier claims. Also say that the -99 fire class counts as `Fire5 = 1`.
3. P6, MET-11 and MET-13 (Must): a stand-in for an original that can be computed, with MET-13 cited backwards. The
   stand-in is close neither to the original (tau -0.07 to 0.79) nor to the source's Spearman (tau -0.79 to -0.21).
   This changes the metric declaration and adds one library metric. Mildest remedy: add a base-weighted
   ordered-Lorenz Gini (`ordered_lorenz_gini` with input role `base`, or a `base` input on the weighted Gini; test 6
   shows it reduces to `normalized_weighted_gini` on `y/base`, `p/base`, `weight=base`) with its MET-13 tests. Then ship
   `Premium` as a `ScoringColumn` and declare `Metric.source`. Name Spearman (Sec. 6.1) in the reason as the second
   reported measure. Caveat for the swap: the premium base is not rank-invariant, so log1p-trained models lose
   heavily (builder, 2010: LightGBM on log1p 0.079 against Tweedie 0.328). The shipped scale should be revisited with
   it (MET-3).
4. P6, TP-4 (Must, proof pending TP-1): under the declared metric, `LnCoverage` alone ties the tuned proxies in 2009
   (0.742 against 0.746-0.749) and beats every model in 2010 (0.760 against at most 0.729, even with the grid picked
   on the test year). The source's own base does not change 2010. Coverage is the natural core of claim cost (TP-4
   reads it first), so this does not make the dataset `Trivial` by itself. But it decides whether the benchmark
   resolves methods on two windows, one of them a catastrophe year. What it changes: the reason must state coverage's
   score. Mildest remedy: run `tuned_results.py --feature LnCoverage` on the two windows before shipping. If the tuned
   methods do not beat it fold by fold, the curator weighs keeping the source's Gini (a note) against a metric that
   separates models from exposure (Spearman, the source's first-reported measure, already in the library as
   `spearmanr`; MET-5 and MET-10).
5. P5, PROV-9 (minor): the file is a close extract of the paper's sample (5,639 against 5,660 rows; 1,679 against
   1,684 claimants). Mildest remedy: one clause in the first line of the notes ("close to, not identical with").
6. P3/P4, LEAK-24 (untested): closed claims only. Mildest remedy: one sentence in the notes quoting the book's
   selection.
7. House: the README's metric definition is stale. Re-run `dataset check`. Record: year 2016 against 2017, and "about
   400 positives each" against 301 in 2009. Fix both in the record when the curator applies the changes.

</details>

<details><summary>Column audit</summary>

**Column audit (column-auditor, 2026-11-01): wisconsin_local_government_property_insurance_fund**

```text
Verdict: ship after changes (two bullet corrections, one optional cheap fix).
Validity: LEAK-10 holds for every kept column. Coverage, deductible and alarm credit do not move with the year's
  claims; Freq, lny and yAvg are correctly dropped. LEAK-34 / USE-10 hold for PolicyNum and NoClaimCredit (own history
  under a temporal split). Premium is no leak; holding it out is the USE-6 call already in builder issue 2.
Quality: CLEAN-10 triggered twice. NoClaimCredit is 0 by construction in 2,412 rows: fix optional, cheap. Fire5 hides
  the fire class code -99: keep with a note, since it cannot be located without a leak. One claim needs correcting:
  coverage indexation in 2010.
For the curator: issue A (NoClaimCredit's structural zeros), a P7 call.
```

The prediction point is the start of the policy year, when the fund rates the member (first `curation_comments` bullet, `task_summary.known`). I read the column meanings in Frees, Lee and Yang (2016) Table 8, Lee (2017) Tables 5.8 and 7.1-7.3, and Loss Data Analytics Ch. 1 ("Fund Rating Variables", fetched 2026-11-01). The frame was loaded through `dataset_io.load(..., built=False)` (origin `rebuilt`, 5,639 x 9). Scripts and outputs are in the run folder.

**Column table (the cleaned frame)**

| column | meaning (codebook) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `PolicyNum` | the member's policy number. On the data, the first two digits are the entity type in every row (12 County, 13 School, 14 City, 15 Town, 16 Village, 18 Misc). The other four digits do not encode the county: a 2-digit block maps to one county in only 24% of blocks (checked against CLAIMLEVEL's `CountyCode`) | yes, the member being rated | category, 1,227 levels, parsed as string. Nothing more to extract (CLEAN-12). Dropping it costs untuned LightGBM (3 seeds) R^2 0.004 / 0.002 and normalized Gini 0.006 / 0.041 on test 2009 / 2010, so it carries member signal | fine | LEAK-34, USE-10, CLEAN-3 (ashrae `building_id` precedent) |
| `Year` | the policy year, 2006-2010 | yes | int64, time index and feature | fine | SPLIT (time column) |
| `LnCoverage` | "Total building and content coverage, in logarithmic millions of dollars" (book); log of the BC coverage (Lee Table 7.1) | yes. The coverage change into year t vs that year's log claims: slope 0.0013 (p 0.02). The change into t+1: 0.0014 (p 0.004). Prior-year claims: 0.0015. So growing members claim more; coverage does not react to the year's claims. The two largest 2010 claims (138300 at $12.9M, 136419 at $2.9M) saw coverage fall 3.4% and 4.0% in 2010, like most members that year (below) | float64, `log(BCcov/1e6)`; `BCcov` dropped as the same information. No impossible values (min $8,937). **2010 level shift:** coverage fell for 68% of members (median -2.6%), against 2-3% of members and a median of +5.2% to +5.6% in 2007-2009 | fine; the bullet needs correcting (problem B) | LEAK-10 holds; CLEAN-21 (no published conversion, real drift the fund saw) |
| `lnDeduct` | "Log of the BC deductible level, chosen by the entity" (Table 8) | yes. 193 members change it; a change into t does not follow the year's claim (logit p 0.74) | float64, 10 menu levels ($500-$100,000), a quantity so numeric. Matches CLAIMLEVEL's `Deduct` in 99.4% of claimant member-years. `Deduct` dropped as the same information | fine | CLEAN-14, CLEAN-5 |
| `Fire5` | "fire class is below 5. Fire class ranges from 0 to 10" (book) | yes. Constant within every member | category 0/1, a yes/no flag. CLAIMLEVEL holds the class behind it, constant per member: classes 0, 2-9 and the codes -99, 40, 50, 80, 90. 40 maps to 1 and 50/80/90 to 0 (read as class x10). **-99 (unknown) maps to Fire5 = 1** in 66 of 1,680 claimant member-years (48 of 759 claimant members). Class 0 covers 262 of 759 claimant members; neither class 1 nor class 10 appears | keep with a note (problem C) | CLEAN-10 (cannot be applied without breaking LEAK-10), CLEAN-14 |
| `NoClaimCredit` | "1 if the insured has no building and contents claim in two years" (Lee Table 7.1, the book). Frees, Lee and Yang Table 8 and Lee Table 5.8 say "in prior year" | the source built it from the earlier rows' claims: own history, known at rating under the temporal split | category 0/1. Where both earlier years are in the file it equals "no claim in t-1 and t-2" exactly (1,852 / 0 / 0 / 1,375). **0 in all 2,292 rows of 2006-2007**, against 55-56% ones in 2008-2010, and 0 in 119 of the 120 later rows that lack two earlier years in the file. These 2,412 zeros mean "history not in the file" | cleaning question (problem A) | LEAK-34 holds; CLEAN-10 |
| `EntityType` | Village, City, County, Misc, School, Town (book; Table 8) | yes | category, rebuilt from the six `Type*` flags, exactly one set in every row (asserted) | fine | CLEAN-12, CLEAN-13 |
| `AlarmCredit` | "automatic smoke alarms in main rooms", levels 0/5/10/15 (book). A 5/10/15% premium credit (Lee Table 7.2 offset) | yes. 337 members change level. Changes into year t: 9.2% with a claim that year vs 7.4% without; with controls for size, coverage change, entity and year the gap is not significant (logit p 0.22). Changes into t+1 after a claim: p 0.83 | category of 4 levels, rebuilt from `AC00`-`AC15`, exactly one set per row. Categorical as the book calls it; it is ordinal, and numeric would also be defensible | fine | CLEAN-13, CLEAN-14 |
| `log1p_bc_claims` (target) | log1p of `y`, the year's total BC claims, closed claims only (book) | the outcome | float64. Smallest positive y $176, none negative, 70.2% zero | fine | CLEAN-16, MET-3 |

**Raw columns not shipped, and why**

| column | verdict | rule |
|---|---|---|
| `Freq`, `lny`, `yAvg` | dropped correctly: the claim count (0 exactly where y = 0), log y, y / Freq | LEAK-10 (an encoding or a part of the target) |
| `BCcov`, `Deduct` | dropped correctly: exact inverses of the log columns the source models (asserted to 1e-8 / 1e-7) | CLEAN-5 |
| `Type*`, `AC*` flags | merged losslessly (above) | CLEAN-13 |
| `Premium` | **not a leak.** It is set at rating time. In each year I fit log premium on the shipped rating variables (R^2 0.98); the residual ranks that year's claims at ROC AUC 0.52-0.55, so the premium holds no sign of the outcome. Holding it out follows the 2_month_survival_rate_prediction precedent (a comparator of the source is no input). The call is the curator's (builder issue 2); I have nothing to add on the column side | USE-6 (P3 call), LEAK-37 |
| CLAIMLEVEL `county`, fire class, `Description`, `CoverageCode` | not joined, correctly. They exist only for the 759 members with a claim, so their presence would tell the outcome. Joining them per member would also bring in later claims. `ClaimNum` is a placeholder (6,253 of 6,258 lines share 20081656), so it holds no report dates | LEAK-10 (missingness that encodes the outcome) |

**Problems, ranked (P4 first, then P7)**

1. **P4, weak and not measurable: when NoClaimCredit's prior-year claims are known (LEAK-10, Should when weak).** The flag is computed from the final, closed claims of years t-1 and t-2. At the rating date for year t, the fund would not yet know claims of late t-1 reported after that date. The file has no report dates (`ClaimNum` is a placeholder), so the effect cannot be measured. The source's models use the flag this way. Mildest remedy: none; at most half a sentence in the NoClaimCredit bullet. No action needed.

2. **P7, problem A: NoClaimCredit is 0 by construction where the file holds no two-year history (CLEAN-10, Should).** Evidence:
   - It is 0 in 100% of the 2,292 rows of 2006-2007, against 54.8-56.5% ones in 2008-2010.
   - It is 0 in 119 of the 120 rows of 2008-2010 whose member lacks both earlier years in the file. The exception is 140844 in 2010, which has a gap year.
   - The source built it from the 2006-2010 window. Table 8's mean of 0.328 equals the file's 0.329, so the source's models used these zeros.
   - A 0 there means "history not in the file", not "had a claim". These rows are 67% of the 2009 window's training rows and 51% of the 2010 window's.
   - The current bullet ("wherever both are in the file") is true but hides the other 2,412 rows.
   - Measured: setting those rows to missing changes untuned LightGBM (3 seeds) R^2 on log1p by -0.001 / -0.006 and normalized Gini by -0.005 / -0.005 on test 2009 / 2010. Trees separate the rows through `Year`. The cost of the zeros falls on models that do not, such as a linear model, which reads them as "had a claim".

   Mildest remedy:
   - (a) write it into the bullet: "0 in every 2006-2007 row and for the 120 later member-years without two earlier years in the file, where the history is not in the file; the source's models use it so";
   - (b) optionally, the cheap CLEAN-10 fix: missing for rows without both earlier years in the file (one line in `_clean`, dtype stays categorical).

   Against (b): CLEAN-1 (the source's own form) and no measured gain. I lean to (a), with (b) the curator's call.

3. **P7, problem C: Fire5 hides an unknown fire class (CLEAN-10, kept with a note).**
   - CLAIMLEVEL shows fire class -99 behind Fire5 = 1 for 48 of the 759 claimant members (66 member-years). The class is constant per member.
   - The unknowns can be located only among members with a claim. Blanking them would make missingness depend on the outcome, which breaks LEAK-10 (a higher part than CLEAN-10), so Fire5 stays as published.
   - Class 0 (262 of 759 claimant members) is a documented value ("0 to 10"), but neither class 1 nor class 10 appears. Whether 0 means a real class or "not graded" is unknown; it is a question, with no action.

   Mildest remedy: one sentence in the Fire5 bullet giving the -99 share and why it stays.

4. **P7, problem B: a claim to correct: "mostly a yearly indexation of about 5%".**
   - The indexation holds for 2007-2009 (median +5.2% to +5.6%, 2-3% of members down).
   - In 2010, the newest test year, coverage fell for 67.7% of members (median -2.6%). The timing test still holds (row `LnCoverage` above).
   - This is real drift that the fund saw at rating time, and no published conversion exists, so there is no fix (CLEAN-21).
   - A model trained on 2006-2009 meets a coverage level about 7-8% below trend in 2010.

   Mildest remedy: correct the bullet ("about 5% a year in 2007-2009; in 2010 coverage fell for two thirds of the members, median -2.6%").

**Claims checked**

- Confirmed:
  - `Freq` = 0 exactly where y = 0.
  - One flag per block in every row.
  - The log columns are logs of the dollar columns.
  - NoClaimCredit 1,852 / 0 and 0 / 1,375 where both earlier years exist.
  - `Fire5` = class < 5 on CLAIMLEVEL, except -99 and the x10 codes.
  - The first two digits of `PolicyNum` are the entity type.
  - The coverage change by same-year claim, +0.059 / +0.061 (mine: 0.053-0.064 by prior and current claim).
  - Premium R^2 of 0.98.
  - County present only for 759 members.
- Corrected: the 5% indexation (problem B).
- For the provenance reviewer, not a column problem: Frees, Lee and Yang (2016) Table 1 / Table 7 count 5,660 BC observations and 1,684 with a claim for 2006-2010. The file holds 5,639 and 1,679, so 21 member-years fewer.
- On the source's definition of NoClaimCredit: Table 8 says "prior year", the book and Lee Table 7.1 say two years. The data agrees with two years, so the bullet is right.

</details>

<details><summary>Split audit</summary>

**Split audit (split-auditor, 2026-11-01): wisconsin_local_government_property_insurance_fund**

**Verdict: wrong as the rules stand, on one Must; otherwise right.** The temporal design is the one the use case and the source imply: the fund rates its own members every year, and the source held out the next year, 2011. But two windows break SPLIT-14 (Must), and SPLIT-14 sends such a task to SPLIT-8 (forced grouped). Two ways out: re-split to `ForcedGroupedFromTemporal`, which keeps to the rules and to five precedents, or have the curator amend SPLIT-14. A Must allows no exceptions. On the measured data the two splits differ little: R^2 shifts by 0.014-0.026 and the three model families keep the same order.

```text
Verdict: wrong as the rules stand (one Must); the temporal design is right for the use case.
Validity: SPLIT-1 / USE-10 hold (known members, temporal); SPLIT-19 followed as far as the data allows (the source's
  2011 hold-out shifted back one year); SPLIT-14 triggered (2 windows), not fixed: SPLIT-8 asks for the forced grouped
  split, or an amendment by the curator; SPLIT-9 holds (no measurable shortcut); SPLIT-10 departed from (no gap),
  exception serving SPLIT-14 as for lending_club; SPLIT-11, SPLIT-12, SPLIT-13 hold; SPLIT-20: both windows are
  extreme years and cannot be widened (note).
Value: two windows of about 1,110 rows; the Gini of one window moves 0.07-0.14 with its largest claim.
For the curator: issue 1 (SPLIT-14: amend, or re-split to forced grouped).
```

**What I checked, with numbers** (loaded through `dataset_io.load(..., built=False)`, i.e. rebuilt from the definition; untuned models, thread caps on)

- Shipped windows as declared: test 2010, trained on 2006-2009 (4,529 rows, 80.3%); test 2009, trained on 2006-2008 (3,417 rows, 60.6%). Every training year comes before every test year. Test rows 1,110 and 1,112, with 403 and 301 claimants (SPLIT-17 is met). The horizon is one year, the fund's yearly rating (SPLIT-12). The train side expands, newest window first (SPLIT-11). The history starts in 2006, after the 2005 change in claim coding the book names (SPLIT-20).
- Regime: the actor re-rates known members. Members seen in training: 2010, 1,094 of 1,110 (16 new; 1,038 with all four earlier years); 2009, 1,085 of 1,112 (27 new). The source trains on 2006-2010 and validates on "the 2011 held-out data, where there are 1098 observations" (Lee 2017, Sec. 5.1.6), so it uses the same regime one year later (SPLIT-19). USE-10 and SPLIT-13 hold. The hidden-group probe's composite key ("all but Year, LnCoverage", seen 74.4%) is the member's static rating profile, which known members are expected to repeat. It is not a defect.
- Time column: `Year` is the policy year. All rows are yearly, so no within-year season can enter a window.

**Problems, ranked (principles.md)**

**1. P4, SPLIT-14 (Must), sent to SPLIT-8 (Must): two windows, where three are required.**
- Evidence: five policy years give windows that train on 80.3% (2010), 60.6% (2009) and 40.6% (2008, under the floor). The file has no finer date, so no third window can be cut above the floor.
- Precedents: SPLIT-8, as amended on 2026-10-21, covers "a release with too few periods for three windows": stacked and grouped by entity, tagged `ForcedGroupedFromTemporal`, with the cost measured against the valid windows. That is how nba_players_2016_2019 and open_university were shipped. In this batch, frempl_french_motor_personal_line, spanish_motor_insurance_coverage_level_2022_2024 and pricing_game_2017_french_mtpl did the same. No dataset in the register ships two windows (no definition accepts `splits_too_few`).
- What sets this case apart: two windows sit above the floor, where every precedent had zero or one (spanish_motor_insurance_coverage_level_2022_2024: one window at 47.5%; nba: one). The source's own check is a temporal hold-out. 98% of real test rows are known members. nba also had known players and was still forced, so known members alone do not set the case apart.
- Cost of the rule-compliant alternative. I ran it (grouped by PolicyNum, 3 folds x 3 repeats, against the two shipped windows). Scores below are R^2 on log1p, then normalized Gini on the amount:

  | model | 2010 | 2009 | mean of the windows | grouped by member |
  |---|---|---|---|---|
  | ridge | 0.249 / 0.540 | 0.203 / 0.699 | 0.226 / 0.620 | 0.240 / 0.569 |
  | LightGBM | 0.209 / 0.495 | 0.173 / 0.613 | 0.191 / 0.554 | 0.217 / 0.563 |
  | CatBoost | 0.245 / 0.524 | 0.242 / 0.709 | 0.244 / 0.617 | 0.261 / 0.588 |

  - The grouped split is optimistic on R^2 by 0.014-0.026. It keeps the R^2 order CatBoost > ridge > LightGBM, which matches the mean of the windows and 2009 (in 2010, ridge leads CatBoost by 0.004). Grouped Gini varies across folds with SD 0.18-0.21, because the $12.9M claim falls into one fold per repeat.
  - The year effect leaks a little under grouping: `Year` adds +0.009 R^2 to LightGBM there (0.217 against 0.208 without it), since the same year's rows sit in both training and test. Under the temporal split it lowers 2010's score (0.209 against 0.239).
- Cold start: the grouped split tests new members, which are 1.4-2.4% of real test rows. That is the builder's argument against option (c). On these windows, though, the member's own history adds nothing measurable:
  - CatBoost with `PolicyNum` (ordered target statistics) scores R^2 0.236 / 0.238, against 0.245 / 0.242 without it.
  - History features built from the member's earlier training years (mean, claim share, count, last year's log1p claims) move ridge by -0.033 / +0.021 and LightGBM by +0.014 / -0.001.
  - So the warm start the temporal split preserves is not used by these models. Forcing to grouped loses little of what the task tests, and the regime matters less than the builder's issue 1 suggests. SPLIT-4 still holds: the size of the gap does not decide.
- Remedy (mildest first):
  - (c) Re-split: `Grouping(on="PolicyNum", labels="per_sample", prediction_unit="row", context="none")`, tag `ForcedGroupedFromTemporal`, keep `Year` as a feature (as spanish_motor_insurance_coverage_level_2022_2024 does), and state the cost from the table above. This is the fix the Must asks for, and it matches five precedents.
  - (a) The curator amends SPLIT-14, for example: "a temporal task of recurring known entities whose release gives two windows, both above the 50% floor, ships those two windows (`splits_too_few` accepted); fewer goes to SPLIT-8." This keeps the faithful design. It cannot be recorded as an exception.
  - (b) Add a 2008 window at 40.6%. This breaks the floor half of the same Must, so it also needs an amendment. It is not milder than (a).
- I lean to neither side on the rules. The measured cost of (c) is small, and (a) keeps the test closest to real use. This is a weighing call for the curator.

**2. P4, SPLIT-20 (Should), with a P6 effect: both windows are extreme years, one claim decides 2010's Gini ranking, and the windows cannot be widened.**
- 2009 is the lowest-claim year ($11.0M). 2010 is the highest ($36.7M; claim share 36.3% against 26.8-31.4% in other years; the severe weather the source names, Lee 2017 Ch. 1). The largest claim is 35.2% of 2010's losses and 19.6% of 2009's.
- Removing 2010's largest claim (one school, $12.9M) moves the Gini from 0.540 / 0.495 / 0.524 to 0.635 / 0.637 / 0.666 (ridge / LightGBM / CatBoost). The order reverses from ridge > CatBoost > LightGBM to CatBoost > LightGBM > ridge. Every model ranks that row below 31-38% of the test rows.
- Bootstrap SD of the Gini within a window: 0.07-0.13. Paired differences separate CatBoost from LightGBM (91-100% of 500 resamples) but not ridge from CatBoost (30-59%). R^2 on log1p is steadier (SD 0.02-0.04) and barely moves without the claim (0.249 -> 0.250).
- With yearly rows the windows cannot be widened. Option (b) would add a typical year (2008: $12.1M, 27.5% claimants), so that most windows are typical.
- Remedy: a sentence in `splits_comment`, for example: "the two test years are the lowest and the highest claim years; one 2010 claim is 35% of that year's losses and reorders models on the Gini." The metric's sensitivity is the metric reviewers' call (MET rules), not the split's.

**3. P4, SPLIT-9 (Must) / SPLIT-10 (Should): no gap. Defensible; record it as an exception.**
- Label delay: at a renewal the prior year's claims are partly open or not yet reported, and training uses their final amounts. The delay cannot be measured from the data: CLAIMLEVEL.csv has no loss or report date, all 6,258 claims are closed, and `ClaimNum` is a placeholder (6,253 of 6,258 rows share 20081656).
- Renewal dates seem to differ by member. Web search snippets mention an April 1 to March 31 policy for one town and a January 1 expiry for a county. I did not read them (the town's PDF did not parse), so this is unverified, rank-4 evidence.
- SPLIT-9: I found no measurable shortcut. History features from earlier training years add nothing (above). Only 10 claim lines ($10,480 in total) repeat with the same amount and description in consecutive years of one member. Under the tension row of principles.md (alfa_battle_2_0_task_2, lending_club), SPLIT-9 is met. The diffuse rest of unmatured labels falls under SPLIT-10.
- SPLIT-10: a one-year gap would leave the 2009 window at 40.6%, below the floor. Departing from SPLIT-10 to serve SPLIT-14 is consistent with lending_club.
- With the gap, the 2010 window's R^2 does not drop (ridge 0.266 against 0.249, LightGBM 0.215 against 0.209, CatBoost 0.253 against 0.245). So training on final labels shows no optimism on R^2. The tree models' Gini falls with the gap (0.495 -> 0.402 and 0.524 -> 0.473; without the largest claim, 0.637 -> 0.477 and 0.666 -> 0.614), while ridge stays (0.540 -> 0.543). That reflects recency or label maturity; the two cannot be told apart.
- Remedy: none to the data. When the curator accepts, record `**Exception to SPLIT-10 ...**` in the record and as a row in the Cases table of splits.md. Under option (c) the gap question disappears, because a forced grouped split trains on every year.

**4. P4 documentation (writing.md / EV-7): "98-99%" is wrong for 2009.**
- Measured: 97.6% (27 new members of 1,112) in 2009 and 98.6% in 2010. The README's own decision table shows 0.976. The claim appears in `task_summary.split`, in the `PolicyNum` bullet and in `splits_comment`.
- Remedy: write "98% (97.6-98.6%)".

**5. P7 / probe validity (EV-6), for the column auditor: the builder's "lightgbm + PolicyNum" rows test nothing.**
- In the builder's split-alternatives probe those rows equal "lightgbm" to three decimals in all five schemes. With default settings (`min_data_per_group=100`, at most 4 training rows per member) LightGBM makes 0 splits on `PolicyNum` (I checked the split importance).
- Forced to use it (`min_data_per_group=1`), it overfits: 2010 R^2 -0.039 against 0.209. CatBoost uses it harmlessly but gains nothing (above).
- So keeping `PolicyNum` (builder issue 4, CLEAN-3) rests on the use case, not on a measured gain. The column is a trap for a model with low category regularisation. It changes no split decision, but it weakens the "known members matter" argument in issue 1.

Scripts and outputs are in the run folder: the windows and members seen, the claim-number check,
the alternatives (history features, CatBoost with `PolicyNum`, grouped 3x3, the gap, 2010 without the largest
claim), and the bootstrap.

**Sources:** Lee (2017), Sec. 5.1.1, 5.1.6, Ch. 1, Ch. 7; search results, not read: [LAB report 19-22](https://legis.wisconsin.gov/LAB/media/2931/19-22full.pdf), [Town of St. Croix Falls resolution 16-08](https://townofstcroixfallswi.gov/wp-content/uploads/2016/12/res_16_08_lgpif_withdrawal.pdf), [OCI LGPIF overview](https://oci.wi.gov/Pages/Funds/LGPIFOverview.aspx).

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner (2026-11-01): wisconsin_local_government_property_insurance_fund**

**Verdict.** Fit **direct**. Each row is the building and contents (BC) premium I set for one member for one year. The inputs are the fund's own rating variables at renewal, nearly all of those in the engine the project adopted, and the test is next year's renewals of members I already insure. **Metric: partly.** The declared stand-in ranks members by the dollar claims they will have, which is mostly a ranking by size, and it cannot tell me whether a model improves on the premium I charge now. That comparison is the decision, and it is what the source scored. I would declare the source's ordered-Lorenz Gini with `Premium` as the base now (MET-1, MET-5, MET-13).

**Who I am.** I am the ratemaking actuary of Wisconsin's Local Government Property Insurance Fund (LGPIF), or the UW-Madison team it hired. Before each policy year I set every member's BC premium. The project began because the surplus ratio was falling toward its floor after the 2010 storms, and "implementing a more accurate and cost efficient rating engine was mutually agreed to be the primary goal" (Lee 2017, Ch. 1). The engine adopted was a GLM, `BC Rate = Base Rate x Offset x Deductible Factor x NoClaimCredit Factor x EntityType Factor x Endorsement Factors`, with log coverage in the base rate and the alarm credits as offsets (Lee 2017, Sec. 7.2.1, Tables 7.1-7.3; Frees and Lee 2017, Variance 10(1)). The law asks for rates "actuarially determined" to keep premiums written at least twice the surplus (Wis. Stat. 605.22). The fund itself is gone: 2017 Wisconsin Act 59 closed it and allowed no renewals after 2017-12-31 (OCI). Every public-entity pool and commercial property insurer makes the same decision, so the closure does not change the fit.

**1. Do I have these inputs when I rate?**

| input | at renewal | note |
|---|---|---|
| `LnCoverage` (the year's insured values) | yes | the member's schedule of values, indexed about 5% a year; the base rate of the engine |
| `lnDeduct` | yes | the member chooses it when it renews; in the engine |
| `EntityType` | yes | in the engine (Table 7.3) |
| `AlarmCredit` | yes | the engine's offset (5/10/15%) |
| `NoClaimCredit` | yes | "1 if the insured has no building and contents claim in two years" (Table 7.1); claim occurrence is known quickly, even while the amounts are open |
| `Fire5` | yes, but coarse | I hold the full protection class (0-10), and the file gives only "below 5". Proposals Y and H of the project used it; the adopted G did not |
| `PolicyNum` | yes | I rate my own members again (USE-10) |
| `Year` | yes | I would use a trend factor; a tree cannot extrapolate it, which does no harm |
| `Premium` (held out) | yes, but it is the output of the engine I am replacing | see below |

What I always have that the file lacks, ranked:
- **Endorsement coverages.** These are in the adopted engine (Table 7.6) and carry 2.99% of the BC premium under it (Table 7.9).
- **The member's county.** Proposals with county codes reached loss ratios of 127-129% on 2011-2013, against 160% for the adopted G (Table 7.9), though county was not adopted. The county appears in CLAIMLEVEL.csv only for the 759 claimants, so the builder was right not to join it. I checked whether `PolicyNum` encodes it: it does not (its digits 3-4 map to a single county for only 24% of the codes).
- **The full fire class.**

None of these can be recovered from the public file. Their absence lowers the ceiling of the task but does not turn it into a stand-in (USE-8).

*The premium.* I agree with holding it out. A rating plan is a function of rating variables, and a new engine that took the old premium as an input would be circular. The source treats the premium as the comparator, not an input: "we are looking for improvements over the original premium scores used by the LGPIF" (Frees, Lee and Yang 2016, Sec. 6.2). This follows USE-6 as read in the 2_month_survival_rate_prediction precedent. The premium is also 98.1-98.5% explained by the shipped variables (decision 1). Its proper place is as the metric's scoring column (MET-2).

*Member history (USE-10).* I would look at a member's past claims. The persistence is real: P(claim | claim last year) = 0.547 against 0.211 without one. But the shipped `NoClaimCredit` already encodes it the fund's way. I tested whether more history helps (lag-1 log claims, mean of past log claims, years with a claim, past loss rate per unit of coverage; untuned LightGBM, three seeds). The effect is mixed. Normalized Gini went from 0.625 to 0.663 (log1p fit) and from 0.664 to 0.707 (Tweedie) in 2009, but from 0.595 to 0.536 and from 0.713 to 0.625 in 2010. This is no case for adding derived features; the `PolicyNum` category is enough for a model that can use it.

*Timing.* When I rate a year, the year that just ended is immature: its claims are partly open. The training rows here carry final amounts (the splits_comment says so). BC property is a short-tailed line, so the optimism is small.

**2. Is the target what I act on?** Yes. The year's total BC claims in dollars is the loss cost, and its expectation is the pure premium I price from. It is checked against the claim-level file to within $1 for 5,633 of 5,639 member-years. I want a number (expected dollars), not a class. The premium is that number's relativity times a base rate that I set separately for adequacy, so a ranking metric that ignores the level is acceptable. One practice point: for relativities, ratemakers usually cap large losses and load catastrophe years separately. The $12.9M water claim at a Milwaukee school is 35% of 2010's losses. The source evaluates on uncapped claims, and I would not change the label. The curator should know that both Ginis move with where that one claim falls.

**3. Does a row match a decision, and is the test what I face?** One member-year is one BC premium for one member for one year: yes. The test is next year's renewals, and 98-99% of the test members are already in training, which matches my renewal book (a few new members join each year). What I would not accept for adopting an engine is the evidence base. There are two test years. One of them (2010) is the severe-weather year in which one claim is 35% of the losses, and each test year has 300-400 claimants. The project judged its proposals on three validation years, 2011-2013, by loss ratio (Table 7.9). The paper's hold-out year, 2011, is not public, so this cannot be fixed here.

**4. Would I use this model?** I would trust it for one reason: its inputs are my rating variables at renewal, and it is tested forward in time on my own members. I would distrust it for three:
- A difference of a few Gini points between models is noise at this size. Frees, Meyers and Cummings (2011, Thm. 5) give standard errors, and the CAS ratemaking material recommends bootstrapping a Gini difference.
- On the probes, sorting by coverage alone beats every untuned model under both Ginis in 2010 and under the stand-in in 2009. Stand-in: coverage 0.742 and 0.760, best probed model 0.707 and 0.732. Premium-base Gini in 2010: coverage 0.540, best probed model 0.39 (the builder's metric and scale probes). Until a model beats "sort by size", it adds nothing to my rating.
- I would want to see the model against my current premium (a double lift chart or the ordered Lorenz curve). That is the comparison CAS Monograph 5 (GLMs for Insurance Rating, Sec. 7) and the source use to adopt an engine.

**5. Does the declared metric score my decision? Partly.**
- *What it gets right.* The unit is the one I act on (a member-year), the losses are summed in dollars (`target_transform="log1p"` inverts the target, MET-3), and the score ignores the level, which I set separately.
- *What it misses.* With insured values spanning five orders of magnitude, a Gini on raw dollars with a constant base mostly rewards ranking members by size, which my current premium already does. On the probes the premium itself scores 0.742 and 0.650, and coverage alone 0.742 and 0.760. The stand-in cannot say whether a model would move premium toward the members whose losses outrun it, and that is the decision. The source scored exactly that, and for that reason: the Gini "measure[s] the satisfaction of the fund manager", computed "using relativities computed with the actual premium collected by the LGPIF ... as the denominator" (Sec. 6.2). It argued for the Gini over squared-error measures because "for many insurance data sets, there are large masses at zero" (Sec. 3). That is a deliberate choice under MET-5, even with Spearman reported beside it.
- *How far apart the two scores are.* The builder measured that the two bases rank the same 8 scores at Kendall tau -0.07 to 0.79, so the stand-in can pick a different winner.
- *Why it is a stand-in at all.* The original can be computed: `Premium` is in the raw file. The obstacle is only that the library lacks the metric. MET-11 reserves the stand-in origin for a metric that cannot be computed on our data, and MET-13 asks for the custom metric to ship with the dataset in the same change.
- *The metric I would use.* `ordered_lorenz_gini` (a general name, MET-12) with `Premium` as the base and as a scoring column (MET-2), never an input. Members are sorted by prediction / premium, with ties grouped (the premium as its own score must give exactly 0; ungrouped ties give -0.27 to +0.04 in the builder's metric probe). The score is the Gini of losses against cumulative premium, not normalized, as in Frees, Meyers and Cummings (2011) and Sec. 6.2.
- *Why not the fallback or a deviance.* `rmse` on dollars (MET-8) is no alternative: even the oracle bound reaches R^2 of only 0.007-0.04 on the amount. The Tweedie deviance, the actuarial proper score, needs strictly positive and calibrated predictions, which models fit on log1p do not give, so it needs a clipping rule. That matches the family's policy note of 2026-10-30.
- *What no candidate scores.* None of these metrics scores rate adequacy, the fund's original trigger. That is acceptable, since the base rate is set separately.

**Gaps between the dataset and the real decision, ranked by how much they change the task**
1. The metric's base (P6). A constant base scores a size ranking, not an improvement over the current premium, and the two pick different winners (tau -0.07 to 0.79). Fixable now: ship the source's metric (MET-1, MET-5, MET-13).
2. Two test years, one of them dominated by a single claim (P4). Model rankings will be noisy, and this cannot be fixed without the 2011 file.
3. Inputs the fund holds that the public file lacks: endorsements (in the adopted engine, 2.99% of the BC premium), county (tried in the project, not adopted), and the full fire class. This lowers the ceiling; the task is unchanged.
4. No large-loss or catastrophe treatment of the label. The ratemaking practice differs, but the source evaluates on uncapped claims, so the label stays; this is for the curator's awareness.
5. Training labels at final amounts, where the latest year would be immature at rating. Small for a short-tailed line, and already named in the splits_comment.
6. Member history reaches the model only through `NoClaimCredit` and the `PolicyNum` category (USE-10). Measured as a mixed effect; no change.

**What an expert in the domain would change**
- Declare `Metric.source` with the ordered-Lorenz Gini, `Premium` as its base and scoring column, and ties grouped, implemented and tested in the library in this change (MET-13). If that cannot be done, the stand-in's reason should say plainly that it scores a size ranking: coverage alone 0.742 and 0.760, beating every probed model.
- Reword `task_summary.use_case`. "rank the members by expected claims" describes the stand-in, not the decision. Something like: "set each member's premium relativity for the coming year; a new rating is adopted when it moves premium toward the members whose claims exceed what they pay (the source's Gini against the fund's premium)".
- Optionally, name the absent endorsement and county inputs in `fit_reason` as limits of the public file, not as an approximate gap (USE-8).
- Keep `Premium` out of the inputs, keep the label uncapped, keep `PolicyNum`, and add no history features.

**Rules cited.** USE-1, USE-3, USE-5, USE-6 (with the 2_month_survival_rate_prediction precedent), USE-8, USE-10; MET-1, MET-2, MET-3, MET-5, MET-8, MET-11, MET-12, MET-13.

**Sources**
- Frees, Lee and Yang (2016), Risks 4(1):4, Sec. 3, 5.1, 6.1, 6.2, https://doi.org/10.3390/risks4010004
- Lee (2017), UW-Madison dissertation, Ch. 1 and Ch. 7 (Tables 7.1-7.3, 7.6, 7.9)
- Frees, Meyers and Cummings (2011), JASA 106:1085-1098 (via the papers above)
- Loss Data Analytics, Ch. 1 case study page: https://users.ssc.wisc.edu/~ewfrees/loss-data-analytics/introduction-to-loss-data-analytics/1-4-case-study-wisconsin-property-fund
- OCI, LGPIF overview (closure under 2017 Act 59): https://oci.wi.gov/Pages/Funds/LGPIFOverview.aspx
- Wis. Stat. 605.22 (rates actuarially determined against the premium-to-surplus ratio), as quoted in search results; the page itself returned 403: https://docs.legis.wisconsin.gov/statutes/statutes/605
- CAS Monograph 5, GLMs for Insurance Rating, Sec. 7 (double lift and loss ratio charts, Gini against the current plan), contents and CAS slides via search: https://www.casact.org/monograph/cas-monograph-no-5
- Builder probes: the metric, scale, hurdle and split-alternative probes (run folder)
- My probes: the member-history and county checks (run folder)
- Not read: the Legislative Audit Bureau reports 12-7 and 19-22 (connection refused).

</details>

<details><summary>Blind review</summary>

**Verdict: include with changes.** The data is real and copied faithfully, and the temporal split is honest. Before use, fix how `NoClaimCredit` codes missing history, decide whether the `PolicyNum` identifier is a feature, and accept that the task has modest headroom.

**What the task is.** The data comes from the Wisconsin Local Government Property Insurance Fund (LGPIF). Each row is one local-government entity in one policy year, 2006-2010: 1,227 policies, 5,639 rows. The target is log1p of that year's total building-and-contents claims. The fund, or any property insurer of public entities, would make this prediction before the policy year when it sets a rate. The textbook's own framing: "Having a single price for all policyholders is nice but hardly seems fair", and "this claims history can be a good predictor of future claims". The use is real. It is the standard teaching and research dataset of Frees et al. (Loss Data Analytics; Risks 4(1):4, 2016).

**What I verified**
- The prepared table matches `PropertyFundInsample.csv` exactly. After a merge on (PolicyNum, Year), all 5,639 rows match, with none missing on either side. `LnCoverage`, `lnDeduct`, `Fire5` and `NoClaimCredit` are identical. `EntityType` and `AlarmCredit` are lossless collapses of the one-hot `Type*` and `AC*` columns. The target equals `log1p(y)` with a max absolute difference of 0.0.
- The source matches the textbook. 2010 has 1,110 policyholders and 1,377 claims (book: "in 2010 there were 1,110 policyholders ... a total of 1,377 claims"). The mean of `yAvg` over 2010 claimants is 56,332 (book: 56,330).
- The same-year outcome columns `Freq`, `y`, `lny` and `yAvg` were dropped, so I found no leakage. `Premium` and the raw `BCcov` and `Deduct` were also dropped. That is acceptable, since `Premium` is the fund's own rating output.
- The split is honest. With test years 2009 and 2010 (expanding train), 27 of 1,112 and 16 of 1,110 test rows come from policies never seen in training. Seeing the same policies again is the real use case (renewal pricing), not leakage.
- There are no exact copies. 18 rows repeat another row's features. In all but one case it is the same policy in consecutive years with unchanged coverage, which is harmless.
- There are no missing values. The dtypes are sensible: `EntityType` is categorical with 6 levels, and `AlarmCredit` is ordinal 0/5/10/15.

**Concerns, most to least serious**

1. **`NoClaimCredit` is a lag of the target built by the textbook authors, and it codes "no history" as 0.**
   - The book defines it as "Binary variable to indicate no claims in the past two years". In the data it equals exactly `(Freq[t-1]==0 & Freq[t-2]==0)` on all 3,233 rows that have two prior years: crosstab 1380/0/0/1853.
   - It is 0 for all 1,154 rows of 2006 and all 1,138 rows of 2007, because the data starts in 2006 after a 2005 claim-coding change. It is also 0 for 119 of the 120 later rows from new entrants.
   - So 2,411 of the 3,786 zeros mean "unknown", not "had a claim". That is 43% of all rows, and 67% of the 2006-2008 training rows for the 2009 window.
   - The meaning therefore differs between training and test rows: in the test years the flag is almost always defined.
   - It is not leakage, since it uses only past years.
   - Recoding barely moved scores in my runs (LGBM 3.704 to 3.699 in 2009, 3.964 to 3.996 in 2010, within noise). Still, the values are wrong as stated.
   - Change: set it to NaN where the policy lacks two consecutive prior years, or add a `history_available` flag. Optionally add explicit lag features (prior-year log claims, mean of past years) computed strictly from earlier years.

2. **`PolicyNum` is an identifier kept as a 1,227-level categorical feature.**
   - Its two-digit prefix encodes `EntityType` exactly (12=County, 13=School, 14=City, 15=Town, 16=Village, 18=Misc; a perfect crosstab), so that part is redundant.
   - The rest is a pure ID with about 3-4 training rows per level. It adds nothing in LGBM (RMSE 3.673 vs 3.674 in 2009; 4.007 vs 4.005 in 2010).
   - It also invites methods to be judged on how they handle a high-cardinality ID. Per-policy experience is legitimate in renewal pricing, but it should come in as explicit, honestly lagged history features, not as an ID.
   - Change: drop it from the features and keep it only as a group key, or declare it explicitly as an entity ID.

3. **The target and metric are a proxy for the pricing decision.**
   - About 70% of targets are zero (63.7-73.2% by year). Positive values range from 5.18 to 16.37 in log1p space, i.e. about $176 to $12.9M.
   - RMSE on log1p is driven mostly by telling claim years from no-claim years. A two-part (logistic times ridge severity) model wins: 3.589 vs 3.654 for ridge in 2009, 3.936 vs 4.003 in 2010.
   - The fund's premium needs E[y], the pure premium, which a log-scale mean does not give.
   - It is fine as a generic zero-inflated regression task. If decision fidelity matters, consider raw `y` scored with Tweedie deviance, or `Freq` as a count target.

4. **Headroom is modest and good methods are hard to tell apart.**
   - With only 7 informative columns, R² is about 0.22-0.25. The mean baseline RMSE is 4.152 / 4.635, against about 3.65 / 4.00 for ridge, random forest and LGBM.
   - Ridge and LGBM are indistinguishable. The bootstrap 95% CI of the RMSE gap (LGBM minus ridge) is [-0.046, 0.107] in 2009 and [-0.062, 0.064] in 2010.
   - An overfit GBM is clearly worse (4.261 / 4.514), so the task does separate broken methods from sound ones.
   - Each test window has only about 1,110 noisy rows. Expect small, often non-significant differences between reasonable methods. That is acceptable for a small real insurance task, but it should not be given heavy weight.

5. **One test window is a shock year.**
   - In 2010 the share of policies with a claim was 36.3%, against 26.8-31.4% in other years. Total losses were $36.7M, against $11-20M.
   - This is realistic temporal drift, not an error. Scores in the 2010 window will reflect it, and dropping `Year` helped LGBM there (3.966 vs 4.005).

6. **Minor points.**
   - 115 rows have 0 < y < deductible. Either y is gross of the deductible or deductibles changed during the year; I cannot resolve this from the public sources.
   - Only closed claims are included (book: "We also consider only claims that are closed, with obligations fully met"). Late years could be slightly understated, although 2010 is the highest-loss year.
   - The out-of-sample 2011 file used in the literature (`PropertyFundOutsample.csv`) returns 404 at the linked repo. A natural true holdout year is therefore unavailable.

**What I could not check**
- The full text of the Risks 2016 paper (MDPI returned 403, and the ANU mirror returned 503). I relied on the Loss Data Analytics chapter.
- Whether `NoClaimCredit` is the fund's actual rating credit or a variable the authors derived. The data strongly indicates it was derived.
- The exact test-window definitions: I assumed 2009 and 2010, each trained on all earlier years.
- How `Fire5` is cut from the underlying fire class, and whether coverage is measured at the start of the year.
- Anything about the 2011 holdout.

Sources: https://github.com/OpenActTexts/Loss-Data-Analytics/blob/master/Data/PropertyFundInsample.csv ; https://openacttexts.github.io/Loss-Data-Analytics/ChapIntro.html ; https://users.ssc.wisc.edu/~ewfrees/loss-data-analytics/introduction-to-loss-data-analytics/1-4-case-study-wisconsin-property-fund ; https://ideas.repec.org/a/gam/jrisks/v4y2016i1p4-d64467.html

</details>

<details><summary>Precedent check</summary>

**Precedent check (AI, precedent-checker, 2026-11-01): wisconsin_local_government_property_insurance_fund**

```text
Verdict: consistent with the precedents on 14 of 19 decisions; 5 depart. Two depart from a Must, and only an
amendment could carry them, not an exception: the two-window split (SPLIT-14) and the interim stand-in metric
(MET-11, MET-13). Two depart from a precedent or a curator's call without a stated reason: the fit `direct` while the
windows have no gap (lending_club is `approximate` for the same gap), and log1p kept "for family consistency" against
Andrej's per-dataset call for insurance targets. One departs with a fact evident from the data (the exact log/dollar
pairs dropped, item 6). One reason reaches its third exception: no gap because a gap would breach SPLIT-14's floor
(SPLIT-10), so an amendment is due.
Validity: SPLIT-14 departed (two windows; builder's option (a) is an amendment), SPLIT-8 cases not followed (nba,
  open_university, distribution_transformers had one valid window each; this release has two). SPLIT-10 exception
  follows lending_club and alfa_battle_2_0_task_2 and the principles' tension row; third exception of the reason.
  USE-6 follows 2_month_survival_rate_prediction (premium held out as the source's comparator). USE-8 fit `direct`
  departs from lending_club. LEAK-10, LEAK-34, PROV-9 consistent.
Value: MET-11/MET-13 the interim stand-in is the first one whose original is computable on our data; MET-5 is a
  weighing (Spearman and Gini reported, Gini argued). TP-4 open (log coverage alone matches the best untuned model).
Quality: CLEAN-12/13/14 consistent; CLEAN-5 reading (exact log/dollar pairs dropped) departs from expresso's derived
  column with an evident fact; CLEAN-16 followed, but the stated reason is the family, not the dataset.
Drift: none within one curator. Andrej (2026-10-30, forced IID) and Lennart (SPLIT-8 amended 2026-10-21) read forced
  regimes differently; the split question here depends on it.
For the curator: consistency checks A (split), B (metric), C (fit), D (target scale), and the SPLIT-10 amendment.
```

**How I checked.** For each choice of the definition and each draft issue of the builder: the same rule ID in the
decision register of this run (1,620 decisions, 14 flags; none of the flags touches this dataset or its rules), the
Cases tables of splits.md, metrics.md, use_case.md, leak_checks.md and cleaning_features.md, the records of the
precedents, and the definitions of the insurance tables of this run (australian_vehicle_insurance_2004_2005 and
frempl_french_motor_personal_line with their REVIEW.md; spanish_motor_insurance_coverage_level_2022_2024,
spanish_motor_insurance_2015_2018, pricing_game_2017_french_mtpl, pricing_game_2016_french_fleet and
liberty_mutual_fire_peril_loss_cost as definitions). I also searched the working copy for every definition with two
temporal windows, every accepted `splits_too_few`, `meta_license_unknown` and `task_target_value_dominant`, and every
`Metric.stand_in`. Who decided matters (principles.md, "Precedence"). Curator decisions on this dataset: only the CC of
2026-10-30 (Andrej: `Yes`, priority 3), given on a screening that left the split open ("SPLIT-8 (forced grouped by
entity) unless the curator accepts two"). The record's Assessment of 2026-10-30 and the insurance table of "Policy calls
of 2026-10-30" in the zero-inflated triage summary (no longer in the repository; each call is in its record's Assessment of 2026-10-30) are AI suggestions. Andrej's own words there are
the policy behind them: "I want you to suggest judgement calls based on the references for each dataset" (policy
question 3, "no family convention"). The insurance siblings are AI drafts of 2026-11-01 waiting for review: they show
how the batch decides, but carry no curator's authority.

**Per decision**

1. **Target: `y`, the year's building-and-contents claims; one row per member-year.** Consistent. It follows the
   aggregate amount per policy of fremtpl2 (CC 2026-10-20, Andrej), the record's Assessment of 2026-10-30, and the
   siblings frempl (`ClaimAmount`) and australian (`claim_cost`).
2. **Target shipped as log1p, scored on the amount (`target_transform="log1p"`).** Follows CLEAN-16 (Should) and MET-3
   (Lennart, 2026-10-21: "ship the target on the modelling scale, score on the original scale"), and the log1p tables of
   the batch (frempl, both Spanish tables, allstate_claim_prediction_challenge_1m). The stated reason departs, though.
   The notes keep it because "the family's log1p stays" and the builder "for family consistency", while Andrej
   declined a family convention for insurance targets on 2026-10-30 and asked for calls from each dataset's
   references. The family question itself is
   open (australian issue 5, frempl's consistency check B). This dataset's own facts point the other way:
   * its source models dollars (Frees, Lee and Yang 2016: Tweedie and GB2 severity on the amount). That is the fact
     offered as option (a) to set australian apart (a GLM textbook modelling the raw cost);
   * its probe (the builder's scale probe, the two shipped windows): the best model in both years is a Tweedie GLM on
     dollars (0.750 / 0.723). Fit on dollars, every family scores at least as well in 2010; ridge and extra trees do
     in both years. Only LightGBM gains clearly from log1p, and only in 2009 (0.633 against 0.469; random forest by
     0.004). frempl and spanish_motor_insurance_2015_2018 have the opposite measurement (log1p ahead of a Tweedie fit:
     0.286 against 0.275, 0.215 against 0.190).
   No departure from a rule, but a reason that the curator's policy call does not accept. Consistency check D.
3. **Exposure: coverage as a feature (`LnCoverage`); rows are whole member-years.** Consistent. It matches the record's
   Assessment and the AI's policy-call table ("a sum insured is a feature too, the size of the risk (LGPIF coverage)").
   pricing_game_2017_french_mtpl also has whole policy-years and no exposure column. No time on risk is cut short here,
   so the LEAK-10 question of frempl, australian and the Spanish tables (fremtpl2's call) does not arise.
4. **Zeros: 70.2% kept as the no-claim regime, no negatives, `task_target_value_dominant` accepted.** Consistent with
   Andrej's policy call 2 (2026-10-30: zero-inflation is no reason to gate) and with the same acceptance in frempl,
   australian, crms_phragmites_cover and avito_demand_prediction_1m. No curator has yet confirmed that acceptance; the
   first confirmation in this batch sets the precedent for all five.
5. **`Freq`, `lny`, `yAvg` dropped (restate the target).** Consistent with LEAK-10 and the family: fremtpl2 `ClaimNb`
   (CC 2026-10-20), frempl `ClaimInd`, australian `clm` and `numclaims`, spanish_motor_insurance_2015_2018
   `N_claims_year`.
6. **`BCcov` and `Deduct` dropped as exact transforms of `LnCoverage` and `lnDeduct`.** Departs from
   expresso_churn_prediction (CC 2026-10-22, Lennart: `ARPU_SEGMENT`, which is `REVENUE` / 3 rounded, kept as released,
   "CLEAN-5 not triggered, as `dzclass`"). The fact that sets this case apart is evident from the data and the code:
   these pairs are exact bijections (within 5e-10 and 1e-7, asserted in `_clean`), while `ARPU_SEGMENT` and `dzclass`
   are rounded or coarser derivatives. A reasonable reading of CLEAN-5's "exact copies" (P7). It is the AI's reading,
   written in no rule; no prompt needed.
7. **`Premium` held out of the inputs (the source's comparator).** Consistent with 2_month_survival_rate_prediction
   (CC 2026-10-26, Lennart, issue 5: the physicians' estimates stay out, because the source set its objective estimate
   beside them as a comparator; listed under USE-6 as applied). Frees, Lee and Yang (2016, Sec. 6.2) score each model
   relative to the 2011 premium, "looking for improvements over the original premium scores". Lee (2017, Table 5.8)
   fits on the rating variables only. A pair in the batch goes the other way:
   spanish_motor_insurance_2015_2018 and spanish_motor_insurance_coverage_level_2022_2024 keep the insurer's premium
   (USE-6: "the insurer's own price ... which a model refines"). The fact that sets Wisconsin apart is stated: its
   source scores against the premium, while the Spanish sources report no model. Andrej asked for per-dataset calls,
   so the two may differ. Note for the Spanish reviews, not this one: Wisconsin's second reason ("the premium is the
   output of the rating that the task replaces") would also read on their use cases ("to rank the risk and set the
   premium"). The drop holds whatever the metric: under the interim metric the premium is in neither the inputs nor
   the score, and the use case alone carries the drop, as in 2_month_survival.
8. **`EntityType` and `AlarmCredit` rebuilt from their one-hot blocks.** Consistent with CLEAN-12 and CLEAN-13
   (caracas_cervical_cancer, CC 2026-10-15; exactly one flag per row, asserted). `AlarmCredit` (a credit of 0, 5, 10
   or 15%) is typed categorical. CLEAN-14 as amended (Lennart, 2026-10-21) keeps a quantity numeric when the context
   says so. I found no precedent for a one-hot block of an ordered quantity either way (the column auditor's call).
9. **`Fire5` and `NoClaimCredit` categorical.** Consistent with CLEAN-14 (yes/no flags; frempl `HasKmLimit`).
10. **`PolicyNum` kept as a categorical feature.** Consistent with ashrae_great_energy_predictor_iii_1m (`building_id`
    a category, the test meters seen in train), LEAK-34 (ieee_fraud_detection's `uid`, 2026-10-01) and USE-10 for
    known members (98-99% of test rows). It depends on issue 1: under the grouped option the id must become the group
    column and leave the features.
11. **`Year` kept as a numeric feature.** Consistent with both Spanish tables ("the year stays a feature").
12. **`county` from CLAIMLEVEL.csv not joined; `y` kept as published where 6 member-years differ from the claim-level
    sums; the $12.9M claim kept.** Consistent: LEAK-10 (the county exists only for claimants, so its missingness tells
    the outcome); CLEAN-11 and the kept point masses of fremtpl2 (CC 2026-10-20) and australian's 200 floor; frempl's
    802,620 claim (CLEAN-11, qsar_tid_11: the training-period clause does not reach a claim in a test window, here
    2010).
13. **`year = "2017"` (first commit of the OpenActTexts repository).** Consistent with PROV-9 and
    2_month_survival_rate_prediction (CC 2026-10-26: the year of "the first publication of the rows we ship") and
    melbourne_housing_market (2026-10-22). The record's `year: '2016'` (the paper, which publishes no data) is superseded
    and should be corrected at hand-over.
14. **`license = None`, `meta_license_unknown` accepted.** Consistent with cape_floristic_region_family_cover (this run,
    the same "no licence file (GitHub API)" wording), bank_customer_churn (Lennart, 2026-10-14), diabetes_3 and
    mobile_churn.
15. **`task_time_on_few_unique` accepted (five policy years).** No precedent; no definition of the working copy accepts
    it yet. Nothing contradicts it.
16. **Split: temporal by year, two windows (test 2009 and 2010).** **Departs from SPLIT-14 (Must) and from the SPLIT-8
    cases. The stated reason (builder issue 1, option (a)) is an amendment, not an exception.**
    * The rule: SPLIT-14 asks for three windows above the 50% floor, "a task that cannot meet it ships under SPLIT-8"
      (Lennart, 2026-10-21). SPLIT-8 names the regime for stacked periods with recurring entities: grouped by the
      entity, `ForcedGroupedFromTemporal`. A Must has no exceptions.
    * The precedents, all decided 2026-10-21 by Lennart (SPLIT-8 amended for "too few periods"):
      nba_players_2016_2019 (3 seasons, grouped by player, players recur and are predicted again),
      open_university_learning_analytics_dataset (4 start dates, grouped by module-presentation) and
      distribution_transformers_at_cauca_department (2 label years, IID). In this batch the drafts
      spanish_motor_insurance_coverage_level_2022_2024, pricing_game_2017_french_mtpl and frempl ship
      `ForcedGroupedFromTemporal`.
    * What sets Wisconsin apart (evident from the data): it has two valid windows (train 61% and 80%), and every
      precedent had exactly one. 98-99% of its test rows are members already in training, where the Spanish coverage
      table has 69% new business. It would be the only definition of the working copy with two windows, and the first
      to accept `splits_too_few`.
    * The builder's argument against grouping (it tests new members, while the fund re-rates known ones) is USE-10.
      SPLIT-8 says it narrows USE-10, and nba was grouped by player although its players recur from season to season.
      So the argument supports changing the rule, not departing from it.
    * Andrej, 2026-10-30, on how_much_did_it_rain: `No`, "if the data is temporal but a temporal split is not possible,
      we cannot split the data and reject it", and "Forced IID is to be avoided at all costs". He has not ruled on
      forced grouped. australian issue 1 and frempl issue 5 put the same question to him. If his answer there is that
      forced regimes are rejects, option (a) is the only way this dataset ships. If he accepts forced grouped for
      frempl, then option (c) is the consistent call.
    * Option (b), adding a 2008 window that trains on 41%, departs from california_house_prices_2020 (SPLIT-14 case,
      2026-10-21: a 25% train side restored to the floor).
    Consistency check A.
17. **No gap between train and test (exception to SPLIT-10, serving SPLIT-14).** Consistent with lending_club
    (exception, 2026-10-21, Lennart) and alfa_battle_2_0_task_2 (exception 2026-10-21, gap 0 confirmed 2026-10-26),
    and with the principles' tension row "unmatured training labels against the training floor". It applies only
    under option (a). It is the third exception of this reason, and this batch proposes two more
    (avito_demand_prediction_1m and spanish_motor_insurance_2015_2018), so an amendment is due (below).
18. **Fit `direct`.** **Departs from lending_club without a stated reason.** lending_club ships the same exception
    with fit `approximate`, and its `fit_reason` names the gap: "the training side holds outcomes of loans issued just
    before each window, which a model refit then would not yet have" (CC 2026-10-21, Lennart). avito_demand_prediction_1m
    (draft, this batch) names its missing gap in `fit_reason` too. Here `splits_comment` says the training years'
    claims "are final amounts, which the fund would partly know only as open claims when it rates the next year", but
    `fit_reason` names only the missing 2011 hold-out. USE-8 (Must) lists "the label's timing" among what a direct fit
    mirrors. The delay cannot be measured from the files: CLAIMLEVEL.csv has no report or close dates. Every claim is
    `Closed`, and the 8-digit claim numbers do not encode the report year. I tested that: their first four digits are
    "2008" for all but one of the 6,258 claims, whatever the loss year. The book's own cut before 2011 "to mitigate the effect of open claims" says the newest
    year is not mature when the data is pulled. Consistency check C.
19. **Metric: interim `Metric.stand_in("normalized_gini", target_transform="log1p")`, the premium-based Gini named as
    the original.** **Departs from MET-11's stand-in origin and from MET-13 (both Must). No fact sets it apart.**
    * MET-11: a stand-in is for "a unique metric that cannot be computed on our data". The definition's reason says
      the original "can be computed on this data, since the source file holds the premium"; only the library lacks
      it.
    * Every other stand-in of the working copy rests on MET-2: inputs not published (5g_energy_consumption,
      asp_potassco_classification, pricing_game_2017_french_mtpl), a changed task (pva_revenue_prediction_kddcup98),
      or an original that loses its meaning on our folds (loan_default_prediction_imperial_college,
      home_credit_default_stability_1m; CC 2026-10-21). None stands in because the library lacks the metric.
    * MET-13 (Must): "A custom metric is shipped with the dataset that needs it ... in the same change." That is what
      g_research_crypto_forecasting_1m (`weighted_pearsonr` with `Weight` as a scoring column), numerai_v5_2_1m
      (`mean_group_pearsonr` on `era`) and rossmann_store_sales (`rmspe`) did, all 2026-10-21. In this batch,
      liberty_mutual_fire_peril_loss_cost declares its weighted Gini with `var11` as a scoring input
      (`Metric.source`).
    * The builder's proposal (a custom ordered-Lorenz Gini, `Premium` as its base and a scoring column, never a
      feature) follows those cases and MET-2.
    * MET-5 is a weighing, and the stand-in label already assumes it holds. The paper reports Spearman first (Sec. 6.1,
      Table 18) and the Gini "to further validate" (Sec. 6.2), as "the satisfaction of the fund manager". Lee (2017,
      Sec. 2.3) argues for the Gini. That is closest to forest_fires (two measures, one ranks: kept) and
      labour_inspection_compliance (an argued statistic: kept). Against it stand gallstone_disease and Lennart's "If
      papers report multiple metrics, they did not have a unique one and then we should fall back" (2026-10-21).
    * Neither outcome supports a stand-in. If the Gini against the premium is the source's metric, MET-13 asks for it
      now, with origin `source`. If it is not, the normalized Gini is a context metric, as frempl, australian and both
      Spanish tables declare it (`Metric.from_context`), and australian issue 4 asks Andrej to confirm it for the
      family.
    * MET-12 (one spelling across the collection): the builder's formula is to sort by `y_pred / base` and plot the
      cumulative base share against the cumulative loss share. With the realised exposure as the base, that is exactly
      the exposure-weighted Gini that frempl issue 4 offers as the family's alternative ("needs a general metric in the
      library; `normalized_weighted_gini` sorts by the raw prediction"). One general metric with a `base` input would
      serve both. Normalized or raw is then one choice for all of them.
    * TP-4, a fact still open rather than a precedent: under the interim Gini, log coverage alone (0.742 / 0.760) beats
      every untuned tree model and matches the Tweedie GLM (0.750 / 0.723). TP-4 calls a dominant natural core (a
      listed price) expected, and asks that the raw feature "match or beat the methods fold by fold" before `Trivial`.
      The precedents are california_house_prices_2020 (kept, CC 2026-10-06) and fitness_club (retired, CC
      2026-10-05). No tuned results exist yet.
    Consistency check B.

**The builder's draft issues against the precedents.**
1. Issue 1 (split): the recommendation (a) is an amendment of SPLIT-14 (Must), which the builder says. It departs from
   the SPLIT-8 cases on a fact they did not have: two valid windows. Decide it with australian issue 1 and frempl issue
   5 (check A).
2. Issue 2 (metric): the target state follows MET-13 and the liberty_mutual and g_research cases. The interim state
   is the departure (check B). Building the metric with a `base` input would also answer frempl issue 4.
3. Issue 3 (gap): consistent with lending_club and alfa. It brings the amendment due below, and the fit must follow
   lending_club (check C).
4. Issue 4 (`PolicyNum`): consistent with ashrae. It needs no issue of its own, only a line under issue 1, since the
   grouped option would move it to the group column.

**Drift and repeated reasons.**
* Drift: none by one curator on one rule. Andrej's decisions that reach this dataset are fremtpl2 (2026-10-20), the
  verdict CCs and policy calls of 2026-10-30, and how_much_did_it_rain (2026-10-30). Lennart's SPLIT-8, SPLIT-10 and
  SPLIT-14 decisions (2026-10-12 to 2026-10-26) are uniform. Between the two curators, Andrej's "Forced IID is to be
  avoided at all costs" and Lennart's SPLIT-8 amendment read forced regimes differently. That is raised in australian
  issue 1. This dataset's split choice depends on the answer.
* Third exception, SPLIT-10, the reason "a gap of the label's delay would take a window under SPLIT-14's floor":
  lending_club and alfa_battle_2_0_task_2 (decided, 2026-10-21) and this definition. avito_demand_prediction_1m and
  spanish_motor_insurance_2015_2018 propose the same in this batch. By principles.md ("Exceptions and amendments") the
  next pass proposes an amendment. A wording to consider: "When a gap of the label's delay would leave a window's
  train side under SPLIT-14's floor, the windows have no gap; the delay is stated in the splits comment and named in
  `fit_reason` (fit approximate)." It differs from the amendment already proposed for ames_housing and
  perth_house_prices (a delay shorter than the time column's resolution), which these cases do not meet.

**Consistency check A (AI, 2026-11-01):** shipping two temporal windows departs from SPLIT-14 (Must) and from
nba_players_2016_2019, open_university_learning_analytics_dataset and distribution_transformers_at_cauca_department
(CC 2026-10-21, Lennart: too few periods ship forced from temporal, grouped by the entity where entities recur), the
regime spanish_motor_insurance_coverage_level_2022_2024, pricing_game_2017_french_mtpl and frempl take in this batch.
What sets this case apart?
(a) Two valid windows above the floor (train 61% and 80%), where each precedent had one, and test rows that are 98-99%
known members re-rated each year. Recorded as an amendment of SPLIT-14 (a Must takes no exception), for example: "A
temporal task of recurring entities whose release gives two windows above the floor ships those two." It would reach
only releases with exactly two valid windows. (b) Treat it like nba and open_university: grouped by `PolicyNum`,
`ForcedGroupedFromTemporal`, with `PolicyNum` moved to the group column. That is consistent with SPLIT-8 as written,
but it is a forced regime of the kind australian issue 1 and frempl issue 5 put to you. (c) Add the 2008 window at 41%,
against california_house_prices_2020. (d) Decide it with australian issue 1: if forced regimes are rejects, only (a)
keeps the dataset.

**Consistency check B (AI, 2026-11-01):** the interim `Metric.stand_in` differs from every other stand-in of the
working copy, which stand in because the original cannot be computed or loses its meaning on our folds (MET-2), and
from the MET-13 cases g_research_crypto_forecasting_1m, numerai_v5_2_1m and rossmann_store_sales (2026-10-21), which
added their custom metric with the dataset. Here the original is computable; only the library lacks it. What sets
this case apart?
(a) The source's metric is borderline under MET-5 (Spearman and Gini reported, the Gini argued), so the interim avoids
building a metric you may reject. Recorded as a temporary state with a swap condition, the AI's best guess, which MET-13
as written does not allow. (b) Treat it like the MET-13 cases: add the ordered-Lorenz Gini with a `base` input now and
declare it as `Metric.source` with `Premium` as the scoring column. The same metric with the exposure as base would
serve frempl issue 4. (c) Treat it like the insurance siblings: MET-5 not met, `Metric.from_context("normalized_gini")`,
decided with australian issue 4. (d) Amend MET-11 or MET-13 to allow a stand-in while a source metric waits for the
library.

**Consistency check C (AI, 2026-11-01):** your call on this dataset (fit `direct`, no gap) differs from lending_club
(CC 2026-10-21, Lennart: the same exception to SPLIT-10, with fit `approximate` because the training side holds
outcomes a model refit then would not yet have). What sets this case apart?
(a) Property claims of a year are mostly reported and settled within months, so at the next rating the fund knows
most of the year before, unlike a loan's term of up to 36 months. This is unmeasured: CLAIMLEVEL.csv has no report or
close dates, and the book's cut before 2011 "to mitigate the effect of open claims" points the other way. Recorded as
the fact behind a direct fit. (b) Treat it like lending_club: fit `approximate`, with "the training years' claims are
final amounts, which the fund knew only partly when it rated the next year" in `fit_reason`. (c) Reopen lending_club to
match this case. (d) Amend USE-8 for no-gap exceptions (it fits the SPLIT-10 amendment above).

**Consistency check D (AI, 2026-11-01):** the target ships as log1p "for family consistency", while your policy call
3 (2026-10-30) asked for insurance targets to be decided per dataset from its references, not by a family convention.
This dataset's references and probe match the fact offered to set australian apart (its source models dollars with
Tweedie and GB2; on the shipped windows the best model is a Tweedie GLM on dollars, and fits on dollars score at least
as well in 2010). frempl and spanish_motor_insurance_2015_2018 measured the opposite. What sets this case apart from
australian?
(a) A per-dataset reason for log1p, the AI's best guess being CLEAN-16's default with LightGBM's 2009 gain (0.633
against 0.469), recorded with the probe. (b) Treat it like australian: dollars, as the source models them. That is
consistent with australian's check B option (a), if you take it. (c) Decide the scale once for the insurance tables
(australian issue 5), which your policy call declined. (d) Amend CLEAN-16 for zero-inflated insurance costs whose
source models dollars.

**Files.** The run's decision register (queried by rule ID and text). Precedent records (`curation/records/`):
lending_club, alfa_battle_2_0_task_2, nba_players_2016_2019, open_university_learning_analytics_dataset,
distribution_transformers_at_cauca_department, how_much_did_it_rain, 2_month_survival_rate_prediction,
expresso_churn_prediction, california_house_prices_2020, fitness_club. Sibling definitions and reviews:
frempl_french_motor_personal_line, australian_vehicle_insurance_2004_2005,
spanish_motor_insurance_coverage_level_2022_2024, spanish_motor_insurance_2015_2018, pricing_game_2017_french_mtpl,
liberty_mutual_fire_peril_loss_cost, avito_demand_prediction_1m. Probes read: the builder's scale, metric and
split-alternative probes; the paper's Sec. 6.1-6.2.

</details>

<details><summary>Advocate</summary>

**Advocate, opening brief (2026-11-01): wisconsin_local_government_property_insurance_fund**

```text
Verdict: ship after changes. The validity core holds on measurement: the use case (P3), clean inputs (P4) and the
  data (P5). The two Must problems are fixes in the definition and do not exclude the dataset: the split (SPLIT-14)
  and the metric's origin (MET-11, MET-13).
Validity: USE-1 and USE-8 hold (direct; one clause on label maturity); LEAK-10 holds for every kept column; USE-6
  holds as read in 2_month_survival_rate_prediction (premium held out); PROV-9 holds (2017); SPLIT-14 triggered,
  fixed by an amendment or a re-split.
Value: MET-11 and MET-13 triggered, fixed by declaring the source's Gini; TP-4 unproven (tuned run pending); TP-2 keep.
Quality: CLEAN-10 twice, notes and an optional one-line fix; the log1p reason needs a per-dataset fact.
```

I concede two things up front. The definition cannot ship unchanged on the metric declaration. It cannot ship
unchanged on the split either, unless the curator amends SPLIT-14. Both are on the "fix the definition" rung of the
remedy ladder (principles.md). Exclusion is for a Must that cannot be fixed, and both of these can be.

**1. A real decision with a direct fit: the fund's own rating engine (P3; USE-1, USE-8, Must).**
- **Use case.** The source names it: "implementing a more accurate and cost efficient rating engine was mutually
  agreed to be the primary goal" (Lee 2017, Ch. 1). The engine the fund adopted is a GLM on log coverage, deductible,
  `NoClaimCredit`, entity type and alarm offsets (Lee 2017, Tables 7.1-7.3), and those are the shipped inputs.
  `Fire5` was in the project's proposals Y and H.
- **Test and label.** The test is next year's renewals of known members: 97.6% (2009) and 98.6% (2010) are in
  training. The label is the loss cost, and it agrees with the claim-level file within $1 for 5,633 of 5,639
  member-years.
- **Practitioner.** The domain practitioner, writing as the fund's ratemaking actuary, calls the fit direct. The
  inputs the public file lacks (endorsements, 2.99% of the premium; county; the full fire class) lower the ceiling.
  Under USE-8 they do not make the data a stand-in.
- **Objection answered (precedent check C).** lending_club is `approximate` for the same lack of a gap. What sets this
  case apart is partly measured. With a one-year gap, the 2010 window's R^2 does not drop (ridge 0.266 against 0.249,
  LightGBM 0.215 against 0.209, CatBoost 0.253 against 0.245; split auditor), so final training labels show no
  optimism on R^2. BC property is a short-tailed line; a loan runs up to 36 months.
- **Conceded.** The tree models' Gini falls with the gap (0.495 to 0.402), and recency and label maturity cannot be
  told apart. Mildest fix: one clause in `fit_reason` saying the training years carry final amounts. Whether the word
  is "direct" or "approximate" changes no row and no split. It is a wording call under USE-8 for the curator.

**2. The inputs are clean at the prediction point, and the premium is held out on the source's own terms (P4,
LEAK-10, Must; P3, USE-6, Must, as applied in 2_month_survival_rate_prediction).**
- **No input reacts to the year's claims.**
  - Coverage change: slope 0.0013 into the year t and 0.0014 into t+1 (column auditor).
  - Deductible change after a claim: logit p 0.74.
  - Alarm credit: p 0.22 and 0.83; claim auditor z +1.34 and -0.83.
- **The restatements of the target and the outcome-shaped columns are out.** `Freq`, `lny` and `yAvg` are dropped
  (`Freq == 0` exactly where `y == 0`, asserted). The county is not joined: it exists only for the 759 claimants, so
  its missingness would tell the outcome. The exact-copy share across the split is 0.0.
- **The premium leaks nothing either way.** After a fit on the rating variables, its residual ranks the year's claims
  at ROC AUC 0.52-0.55. The shipped variables explain 98.1-98.5% of the variance of its log, and adding it moves
  untuned models by -0.016 to +0.055 normalized Gini.
- **Holding it out follows the source.** The source scores against it: "we are looking for improvements over the
  original premium scores used by the LGPIF" (Frees, Lee and Yang 2016, Sec. 6.2).
- **Objection answered (USE-6's text, the Spanish siblings that keep their premium).** The curator's applied reading
  of USE-6 holds out a comparator the source sets beside its own estimate (2_month_survival_rate_prediction, Lennart,
  2026-10-26). The Spanish sources report no model. A rating engine cannot take its own output as a rating variable,
  and the practitioner and the precedent checker agree. The premium comes back as the metric's scoring column
  (point 5).

**3. The data is faithful, pinned and cross-checked (P5; PROV-9, Must; PROV-13).**
- **Pinned.** The sha256 of both files matches the definition. The first commit (2017-06-27) is the only commit on
  either file. `Insample.csv` is byte-identical, and `WiscPropFund.csv` (LDAVer2) holds the same 5,639 keys with equal
  values.
- **Checked against the claim-level file.** CLAIMLEVEL sums match `y` within $1 for 5,633 member-years. The other 6
  are explained: 3 repeat a claim line, 2 sum to exactly twice `y`, 1 is $3 off.
- **Checked against the book.** The blind reviewer finds 1,110 policyholders and 1,377 claims in 2010, as the book
  says, and a 2010 mean `yAvg` of 56,332 against the book's 56,330.
- **Conceded.**
  - The file is a close extract of the paper's sample, not the same one (5,639 against 5,660 rows; 1,679 against
    1,684 claimants). That takes one clause in the first line of the notes.
  - Only closed claims are kept (LEAK-24, untested). 2010 is the highest claim year (36.3% of members with a claim),
    so no deficit shows. That takes one sentence quoting the book.

**4. A temporal split on known members is the right regime; SPLIT-14 is met by fixing the definition, not by
excluding the dataset (P4; USE-10, Must; SPLIT-4, Must; SPLIT-19, Should; against SPLIT-14 and SPLIT-8, Must).**
- **Conceded.** Two windows break SPLIT-14 as written, and a Must takes no exception.
- **The temporal design is right.**
  - The fund re-rates its members every year.
  - The source validated on the next year (2011, 1,098 member-years; Lee 2017, Sec. 5.1.6), and SPLIT-19 says to
    follow the source's split.
  - Both windows train above the floor (60.6% and 80.3%).
  - Each test year holds 301 and 403 claimants (TP-9 met).
  - Every SPLIT-8 precedent (nba, open_university, distribution_transformers) had one valid window or none. This is
    the first case with two.
- **Remedies that keep the dataset.**
  - (a) An amendment of SPLIT-14, for example: "recurring entities, exactly two windows above the floor, ship those
    two". It reaches only that narrow case.
  - (c) A re-split to `ForcedGroupedFromTemporal`, which keeps every row. Its measured cost is small: R^2 is
    optimistic by 0.014-0.026, and the model order is kept (split auditor).
- **Why (a) over (c).**
  - SPLIT-4: the split follows what the task does. The grouped split tests a cold start that is 1.4-2.4% of real test
    rows.
  - Under grouping, the year effect leaks (+0.009 R^2).
  - The $12.9M claim falls into one fold per repeat (the grouped Gini's fold SD is 0.18-0.21).
  - If the curator's answer on australian issue 1 is that forced regimes are rejects (Andrej, how_much_did_it_rain:
    forced IID "to be avoided at all costs"), then (a) is the only way this dataset ships.
- **Not (b).** A 2008 window at 40.6% goes against california_house_prices_2020.

**5. The source's metric can be computed and should be declared now. The stand-in label is wrong, and the fix is one
library metric (P6; MET-11, MET-13, Must; MET-5, Should; MET-2, Must).**
- **Conceded.**
  - MET-11 allows a stand-in only when the original cannot be computed, and the reason itself says it can.
  - MET-13 asks for the custom metric in the same change.
  - No other stand-in of the working copy rests on a gap in the library (precedent checker).
- **The fix is cheap.** Test 6 of the claim auditor: `normalized_weighted_gini(y/P, s/P, weight=P)` equals the
  source's Gini times a per-fold constant (Kendall tau 1.0 over 40 random scores per window). The original is a thin
  wrapper over tested library code.
- **MET-5 leans to the source.**
  - The Gini is argued: "measure the satisfaction of the fund manager"; "large masses at zero, meaning that these
    traditional metrics are less helpful" (Frees, Lee and Yang 2016, Secs. 3 and 6.2).
  - Lee 2017 (5.1.8) concludes by it.
  - That is closer to forest_fires and labour_inspection_compliance than to gallstone_disease.
- **MET-2 holds.** `Premium` ships, each test fold holds 301 or 403 claimants, and the stand-in scores 0 for a
  constant and 1 for a perfect prediction. Ties must be grouped for the source's version.
- **Remedy.**
  - Add an ordered-Lorenz Gini with a `base` input. Ship `Premium` as a `ScoringColumn`, declare `Metric.source`, and
    name Spearman in the reason as the second reported measure.
  - If the curator rejects MET-5, use `Metric.from_context("normalized_gini")`, as the insurance siblings do. That is
    again a change to the declaration.
- **Caveat conceded.** Under the premium base, models fit on log1p lose heavily (2010: LightGBM on log1p 0.079 against
  Tweedie 0.328), so the shipped scale is revisited with the swap (point 7).

**6. The task is worth benchmarking, and `Trivial` is not proven (P6; TP-1 and TP-4, Must; TP-2, Should).**
- **Both parts carry signal.** Whether a member has a claim is ranked at ROC AUC 0.77-0.79, against 0.74 for coverage
  alone. Among the claimants, the log claims reach R^2 0.10-0.22.
- **The task separates sound methods from broken ones.** Linear skill is 0.245 and beats the dummy in 2 of 2 windows.
  An overfit GBM scores clearly worse (RMSE 4.261 and 4.514 against about 3.65 and 4.00; blind reviewer).
- **Models beat coverage and the fund's premium on Spearman, the source's first-reported measure (Table 18).** Ridge
  scores 0.448 and 0.513, coverage 0.389 and 0.446, the premium 0.400 and 0.464 (the builder's metric probe).
- **Conceded.** Under both Ginis, coverage leads the untuned and tuned-proxy models in 2010.
  - Stand-in: 0.760 against at most 0.729.
  - Premium base: 0.540 against at most 0.40.
  - In 2009 coverage ties them (0.742 against 0.746-0.749).
  - The $12.9M claim alone reorders models in 2010.
- **Why this does not retire the task.**
  - TP-4 calls the natural core expected to dominate. Coverage is the exposure of a property cover, as a listed price
    is for a sale price (california_house_prices_2020 kept).
  - `Trivial` needs the benchmark's tuned methods, fold by fold (TP-1), and none has been run.
  - Until a concrete reason is found, the task stays (TP-2).
- **Mildest remedy.** Run `tuned_results.py --feature LnCoverage` on the two windows, and state coverage's score in
  the metric reason as the floor a model must beat.

**7. The cleaning gaps take notes or a one-line fix (P7; CLEAN-10 and CLEAN-16, Should; principles.md tension "a real
task against imperfect cleaning": keep the task, fix what is cheap).**
- **`NoClaimCredit`.** Conceded: it is 0 in 2,411 of the 2,412 rows without two earlier years in the file. The effect
  is small: normalized Gini moves by -0.029 to +0.007, and R^2 by -0.006 to +0.001. The source's models used the same
  zeros (mean 0.328 against the file's 0.329). Fix: state it in the bullet, and optionally set those rows missing.
- **`Fire5`.** It stays with a note: the -99 code can be located only among claimants, and LEAK-10 outranks CLEAN-10.
- **Text corrections.**
  - The coverage indexation of 2010: coverage fell for 68% of members, median -2.6%.
  - "98-99%" becomes "97.6-98.6%".
  - The record's year 2016 becomes 2017, and its "about 400 positives" becomes 301 and 403.
  - The README needs a fresh `dataset check`: its text on metric ties is stale.
- **Target scale (consistency check D).** Conceded: "the family's log1p" is no reason under Andrej's policy call 3.
  This dataset's own facts lean to dollars:
  - the source models dollars;
  - on the amount, 6 of 8 fits score higher (claim auditor);
  - the best model is a Tweedie GLM on dollars (0.750 and 0.723).

  The metric is computed on the amount either way (MET-3), so the scale changes how models are fit, not what is
  scored. If the premium-base Gini is adopted I would not defend log1p. It is the curator's call, and it is not a
  reason to hold the dataset.
- **`PolicyNum`.** It stays as known information about a known member (ashrae `building_id`, LEAK-34, USE-10).
  Conceded: no measured gain (LightGBM makes no split on it at its defaults).

**For the curator.** Two calls decide the shipped form: the split (amend SPLIT-14, or re-split forced grouped) and the
metric (the source's base Gini now, or a context metric). Neither touches the rows. The rest is wording, plus one
tuned-run check before the build.

</details>

<details><summary>Critic</summary>

**Critic, opening brief (2026-11-01): wisconsin_local_government_property_insurance_fund**

```text
Verdict: do not ship as defined; ship after changes. Nothing calls for exclusion: the use case is real (USE-1), the
  rows are the published file (PROV-9), and each Must below is fixed in the definition or by a deliberate amendment.
Validity: USE-8 broken (fit `direct` with untimed training labels); SPLIT-14 / SPLIT-8 broken (two windows).
Value: MET-11 and MET-13 broken (a stand-in for an original that can be computed), and with them MET-1 (the score
  cannot see the decision); TP-4 open until TP-1 is run (log coverage alone matches or beats the models).
Quality: log1p kept on a reason the curator's policy call rejects (CLEAN-16, MET-3); NoClaimCredit placeholder zeros
  (CLEAN-10); five sentences of the notes wrong or incomplete (EV-7).
```

All numbers come from the phase A reports, the builder's probes and my own re-count on the raw file
(run folder: NoClaimCredit share 0.000 in 2006 and 2007, 0.548-0.565 after; test members seen 97.57% in
2009 and 98.56% in 2010; coverage fell for 67.7% of members in 2010, median -2.6%).

**1. P3, USE-8 (Must): the fit is `direct`, but the label's timing does not mirror the use case.**
- Problem: the training rows carry final, closed claim amounts. At a renewal the fund knows the year just ended only
  in part. `splits_comment` says so itself ("final amounts, which the fund would partly know only as open claims when
  it rates the next year"), and the book stops before 2011 "to mitigate the effect of open claims". `fit_reason` names
  only the missing 2011 year. The test rows' `NoClaimCredit` has the same exposure: 10.4% (2009) and 12.5% (2010) of
  them lose the credit only through a claim in the year just before (claim auditor, untested bound).
- Effect: small, and it cannot be measured (CLAIMLEVEL.csv has no report dates; `ClaimNum` is one placeholder for
  6,253 of 6,258 lines). With a one-year gap, the 2010 tree models lose Gini (0.495 to 0.402, 0.524 to 0.473) while
  ridge does not. Recency and maturity cannot be told apart (split auditor, problem 3).
- Rule: USE-8 lists "the label's timing" among what a direct fit mirrors. lending_club ships the same SPLIT-10
  exception with fit `approximate` and names the gap in `fit_reason` (CC 2026-10-21, Lennart; precedent checker,
  item 18 and check C).
- Remedy (fix the definition): fit `approximate`, with the untimed training labels named in `fit_reason` as in
  lending_club. If the curator holds that BC property is short-tailed enough for `direct` (domain practitioner), record
  that as the fact that sets the case apart from lending_club. This is the third SPLIT-10 exception for the floor
  reason, so the amendment the precedent checker words is due.

**2. P4, SPLIT-14 and SPLIT-8 (Must): two temporal windows where three are required.**
- Problem: five policy years give windows that train on 80.3% and 60.6% of the rows. A 2008 window would train on
  40.6%. SPLIT-14 sends such a task to SPLIT-8, which groups by the entity when the entities recur. A Must takes no
  exception. This would be the first definition in the working copy to accept `splits_too_few`.
- Effect: the windows are as thin as the three-window rule fears. 2009 is the lowest claim year ($11.0M) and 2010 the
  highest ($36.7M), with one $12.9M claim at 35.2% of it. Removing that one row moves the 2010 Gini by 0.10-0.14 and
  reverses the model order. The bootstrap SD of the Gini within a window is 0.07-0.13 (split auditor, problem 2).
  SPLIT-20 (Should) asks to widen windows that fall in atypical years, and here that is impossible.
- Against the builder's reason for keeping the temporal split (USE-10, known members): SPLIT-8 says it narrows USE-10,
  and the warm start measures as nil. LightGBM makes 0 splits on `PolicyNum` at default settings. CatBoost with it
  scores R^2 0.236 / 0.238 against 0.245 / 0.242 without. History features move models by -0.033 to +0.021. The
  grouped split is optimistic on R^2 by 0.014-0.026 and keeps the model order (split auditor, problems 1 and 5).
  A grouped split does not cure the noise either: its Gini varies across folds with SD 0.18-0.21.
- Remedy (fix the definition): `Grouping(on="PolicyNum")`, tagged `ForcedGroupedFromTemporal`, with `PolicyNum` moved
  from the features to the group column, `Year` kept as a feature, and the cost against the two windows stated. This is
  what frempl, pricing_game_2017_french_mtpl and spanish_motor_insurance_coverage_level_2022_2024 do. The other way
  out is the curator's amendment of SPLIT-14 for releases with exactly two valid windows, recorded with this case as an
  amendment, never as an exception. Decide it with australian issue 1 and frempl issue 5: if Andrej rules that forced
  regimes are rejects, only the amendment keeps this dataset.

**3. P6, MET-11 and MET-13 (Must), and MET-1 (Must): a stand-in for an original that can be computed, and the score
cannot see the decision.**
- Problem: the definition's own reason says "the original can be computed on this data, since the source file holds
  the premium". MET-11 reserves the stand-in origin for an original that cannot be computed. "The library has no
  ordered-Lorenz Gini with a base yet (MET-13)" reads MET-13 backwards: it asks for the custom metric in the same
  change. Every other stand-in of the working copy rests on inputs that are not published or a task that was changed
  (precedent checker, item 19).
- Effect: the fund adopts a rating when it moves premium toward the members whose claims outrun what they pay. The
  source scores exactly that: "we are looking for improvements over the original premium scores used by the LGPIF"
  (Frees, Lee and Yang 2016, Sec. 6.2). The stand-in uses a constant base, which mostly scores a size ranking. Log
  coverage alone scores 0.742 / 0.760, and the fund's own premium 0.742 / 0.650 (the builder's metric probe). The
  two bases rank the same 8 scores at Kendall tau -0.07, 0.00 and 0.79, so they can pick different winners. The reason
  concedes it: "It does not measure an improvement over the fund's premium." With the premium held out of the inputs
  as the source's comparator, nothing in the shipped benchmark compares a model with the rating it would replace.
- Cost of the fix: small. `normalized_weighted_gini(y/P, s/P, weight=P)` equals the source's Gini times a per-fold
  constant (tau 1.0 over 40 random scores per window; claim auditor, test 6), so the original is a thin wrapper over
  tested library code.
- Remedy (fix the definition, with one library metric): add a base-weighted ordered-Lorenz Gini under a general name
  (MET-12), with ties grouped and the tests MET-13 asks for. One metric with a `base` input also answers frempl issue 4.
  Ship `Premium` as a `ScoringColumn`, never a feature (MET-2), declare `Metric.source`, and name Spearman (Sec. 6.1,
  Table 18) in the reason as the second reported measure. If the curator rules that Spearman beside the Gini fails
  MET-5, the origin becomes `context` or `fallback`. Either way the stand-in goes.

**4. P6, TP-4 with TP-1 (Must): log coverage alone matches or beats every model under the declared metric, and the
check against tuned methods is missing.**
- Evidence (claim auditor, t7): in 2009 coverage scores 0.742, against 0.749 and 0.746 for the tuned-proxy LightGBM and
  Tweedie GLM. The best untuned model, a hurdle GLM, scores 0.764 (P > coverage 0.91). In 2010 coverage scores 0.760,
  against at most 0.729, even with a 72-config grid picked on the test year (0.695). Without the $12.9M claim, coverage
  still leads in 2010 (0.821 against 0.795). Under the source's base in 2010, coverage scores 0.540 and the best model
  0.385 (builder). Spearman puts models above coverage in both years.
- Effect: coverage is the natural core of claim cost, and 2009 has a model above it, so `Trivial` is not proved. But on
  these two windows the benchmark may not rank any method above "sort by size", and the notes do not give coverage's
  score.
- Remedy (before shipping, under whatever metric point 3 settles): run the benchmark's tuned methods against
  `LnCoverage` on the shipped folds (TP-1), and state coverage's score in the metric's reason as the level a model must
  beat. If the tuned methods do not beat it fold by fold, the curator weighs the metric (MET-10: Spearman is the
  source's first-reported measure and is already in the library). This alone is no reason to exclude.

**5. P6/P7, CLEAN-16 and MET-3 (Should): log1p kept "for family consistency", a reason the curator's policy rejects;
under the source's metric the scale decides part of the score.**
- Evidence: the notes say "so the family's log1p stays", and the builder "log1p kept for family consistency". Andrej's
  policy call 3 (2026-10-30) asks for insurance targets to be decided per dataset from their references. The source
  models dollars (Tweedie, GB2). In the builder's scale probe the best model in both windows is a Tweedie GLM on dollars
  (0.750 / 0.723). Fit on dollars, every family scores at least as well in 2010, and only LightGBM in 2009 gains from
  log1p (0.633 against 0.469). The premium-base Gini sorts by prediction / premium, so it is not invariant to a monotone
  change of scale. In 2010, LightGBM on log1p scores 0.079 against 0.328 for LightGBM Tweedie on dollars
  (the builder's metric probe; precedent checker, check D).
- Remedy (fix the definition or its reason, together with point 3): ship dollars as the source models them
  (`target_transform` identity), or keep log1p with a reason of this dataset's own, measured under the final metric.

**6. P7, CLEAN-10 (Should): `NoClaimCredit` is a placeholder 0 wherever the file holds no two-year history.**
- Evidence: the share is 0.000 in 2006 and 2007 and 0.548-0.565 afterwards. It is 0 in 119 of the 120 later rows
  without both earlier years. That makes 2,411-2,412 rows (43% of all), 67% of the 2009 window's training rows and 51%
  of the 2010 window's (column auditor, claim auditor, blind reviewer agree). `task_summary.known` ("whether it had a
  claim in the two years before") is false for those rows. Scores move little (Gini -0.029 to +0.007), since trees
  separate the rows through `Year`. The cost falls on models that read a 0 as "had a claim", such as a linear model.
  `Fire5` also hides fire class -99 (unknown) as 1 for 48 of the 759 claimant members, which cannot be repaired without
  a leak (column auditor).
- Remedy (cheap and safe): set `NoClaimCredit` missing for member-years without both earlier years in the file (one
  line in `_clean`), or at least say it in the bullet and in `known`. Add one sentence on Fire5's -99.

**7. EV-7 (Must) and writing.md, PROV-9: five sentences of the notes are wrong or incomplete.**
- "98-99%" of test members seen: the figure is 97.6% in 2009. It appears in `task_summary.split`, the `PolicyNum`
  bullet and `splits_comment`.
- "mostly a yearly indexation of about 5%": this holds for 2007-2009. In 2010, the newest test year, coverage fell for
  67.7% of members (median -2.6%). The timing argument stands; the description of the test year is wrong.
- "the data Frees, Lee and Yang (2016) model": the file is a close extract, not the same sample (5,639 against 5,660
  rows, 1,679 against 1,684 with a claim).
- The book keeps "only claims that are closed, with obligations fully met". The notes' "all closed" reads as
  completeness, not as a selection (LEAK-24, untested; 2010 shows no deficit).
- The README's metric text "(ties in row order)" went stale with the metrics.py change. The record still gives year
  2016 and "about 400 positives each" (2009 has 301).
- Remedy (notes): correct the sentences, re-run `dataset check` to regenerate the README, and fix the record when the
  curator's changes are applied.

**Conceded up front.** The premium hold-out follows USE-6 as applied in 2_month_survival_rate_prediction. Dropping
`Freq`, `lny`, `yAvg`, `BCcov` and `Deduct`, the flag merges, leaving the county out, and keeping the $12.9M claim
all hold on the evidence. I raise none of them.

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate, rebuttal (2026-11-01): wisconsin_local_government_property_insurance_fund**

```text
Verdict: ship after changes. The critic and I agree that nothing calls for exclusion.
Conceded: 1 (fit approximate), 3 (the source's metric now, MET-1/11/13), 5 (the target scale), 6 (NoClaimCredit set
  missing), 7 (the five sentences).
Narrowed: 2 (both remedies keep the dataset; I keep the amendment as the better test, the re-split is the fix as
  written); 4 (Trivial is not met on the 2009 window under either Gini; in 2010 coverage clearly beats every probed
  model; the tuned run decides before the build).
```

One new check, run because it decides point 4: a bootstrap script and its output in the run folder. It
fits four untuned models per shipped window, as in the builder's scale probe, and draws 500 paired bootstrap
resamples of model minus log coverage. It scores both the premium-base Gini (ties grouped) and the declared
normalized Gini, with and without the window's largest claim.

**Critic 1 (USE-8, the fit): conceded.**
- My case for `direct` rested on two things:
  - a fact I could not measure: BC property is short-tailed, which is inference, the lowest rank of evidence (EV-2);
  - a gap test that is mixed: with a one-year gap R^2 held, but the tree models' Gini fell from 0.495 to 0.402.
- The book's own cut before 2011, "to mitigate the effect of open claims", points the other way.
- The test rows' `NoClaimCredit` carries the same timing risk (10.4% and 12.5% of them lose the credit only through a
  claim in the year just before).
- Treat like cases alike: lending_club ships the same exception to SPLIT-10 with fit `approximate`.
- What follows:
  - Set the fit to `approximate`, with the untimed training labels named in `fit_reason`.
  - Record the third exception to SPLIT-10 for the floor reason, and pass the amendment the precedent checker drafted to
    the curator.
  - No row or split changes.

**Critic 2 (SPLIT-14 and SPLIT-8): narrowed.**
- **Conceded.**
  - A Must takes no exception.
  - As the rules are written, the re-split to `ForcedGroupedFromTemporal` is the compliant fix.
  - The warm-start argument (USE-10) is weak on the data: LightGBM makes no split on `PolicyNum`, and history features
    move models by -0.033 to +0.021.
  - I drop it as a reason.
- **Contested: which test the curator should prefer.** The case for the amendment rests on SPLIT-4 (Must): the split
  follows what the task does, rating next year's book forward in time.
  - The year shift is the dominant fact of this task. It is not the warm start.
    - In 2010, coverage fell for 67.7% of members (the critic's own recount), and claims tripled.
    - Models trained on 2006-2009 rank worse than log coverage alone (point 4 below).
  - A grouped split puts 2010 rows into the training side of every fold, so it hides that shift.
    - Its R^2 is optimistic by 0.014-0.026.
    - `Year` gains +0.009 R^2 under grouping, against a loss under the temporal split (split auditor).
  - SPLIT-19 (Should) adds weight: the source's own check is a hold-out of the next year.
- **The guard.** The split must not be chosen to rescue the score. The principles' tension row says the split follows
  the application, P4 over P6.
  - If the curator picks the re-split, the TP-4 check of point 4 should still be read on the two temporal windows, the
    regime of the use case.
  - Both remedies keep the dataset, and the call is the curator's.
  - If forced regimes are ruled rejects (australian issue 1), only the amendment keeps it.

**Critic 3 (MET-11, MET-13, MET-1): conceded in full.**
- I conceded MET-11 and MET-13 in my opening. I add MET-1: under the constant base, nothing in the shipped benchmark
  compares a model with the premium it would replace, and that comparison is the fund's decision.
- What follows:
  - Add a base-weighted ordered-Lorenz Gini under a general name, with ties grouped and the MET-13 tests.
  - Ship `Premium` as a `ScoringColumn`, declare `Metric.source`, and name Spearman in the reason.
  - If the curator rules against MET-5, the origin becomes `context`. Either way the stand-in goes.

**Critic 4 (TP-4 with TP-1): narrowed. The new check concedes 2010 and holds 2009.**
- **2009: Trivial is not met under either Gini.** TP-4 needs the raw feature to "match or beat the methods fold by
  fold". sepsis_survival was kept with age at 0.704 against a best of 0.707.
  - Premium base: models score 0.218-0.276 against coverage's 0.195. Bootstrap P(model > coverage) is 0.62-0.89.
  - With the window's largest claim removed, Tweedie scores 0.167 against 0.045 (P 0.98).
  - Normalized Gini: Tweedie scores 0.750 against 0.742 (P 0.81). The claim auditor's hurdle GLM scores 0.764
    (P 0.91).
  - Coverage is below the best method in 2009 on both bases.
- **2010: conceded, and stronger than the probes said.** Coverage beats every probed model on both bases.
  - Premium base: 0.540 against at most 0.385 (Tweedie -0.155, P(model > coverage) 0.01).
  - Normalized Gini: 0.760 against at most 0.723 (P 0.00-0.01).
  - With the $12.9M claim removed, it still beats them (premium base 0.412 against at most 0.359; random forest is the
    closest, P 0.23).
  - This is the catastrophe year's shift, not a fault of the rows: in the year the storms hit large members, exposure
    outranks every model fit on calm years. TP-2 keeps a task until a concrete reason is found, and this is a reason
    to watch, not yet one to retire.
- **Agreed remedy.** Before the build, run the benchmark's tuned methods against `LnCoverage` on the two temporal
  windows under the metric point 3 settles (TP-1). State coverage's score in the reason as the floor.
  - If tuned methods also stay below coverage in 2009, the fitness_club test is met and the verdict is `Trivial`.
    I would not argue against that.
  - Switching to Spearman to escape it would let the score pick the metric. The metric follows the decision (MET-1),
    and I do not propose it.

**Critic 5 (CLEAN-16, MET-3, the target scale): conceded.**
- On the mean of the two windows, fits on dollars beat fits on log1p:
  - all 4 families under the premium base (for example random forest 0.289 against 0.169, LightGBM 0.191 against
    0.123);
  - 3 of 4 under the normalized Gini (the builder's scale probe).
- The source models dollars. Under the premium base the scale changes the ranking (2010: LightGBM 0.259 on dollars
  against 0.079 on log1p).
- What follows: ship dollars (`target_transform` identity), named `bc_claims`, as the source models it. The other way
  is a log1p reason measured under the final metric, and the data do not supply one.

**Critic 6 (CLEAN-10, `NoClaimCredit` and `Fire5`): conceded.**
- I called the fix optional. It is cheap and safe:
  - one line in `_clean` sets the credit missing for member-years without both earlier years in the file (2,412 rows);
  - it keeps the categorical dtype;
  - the measured score change is small (-0.029 to +0.007 Gini).
- It also removes a meaning that differs between training and test rows, which a linear model would misread.
- What follows:
  - Correct `known` to match.
  - Add one sentence on `Fire5`'s -99, which stays as published, since LEAK-10 outranks CLEAN-10.

**Critic 7 (EV-7 and writing.md, five sentences): conceded.**
- All five sentences are wrong or incomplete as stated. I had listed four of them in my opening point 7.
- What follows:
  - "97.6-98.6%" in three places.
  - The 2010 coverage fall in the indexation bullet.
  - "a close extract of the paper's sample".
  - The book's closed-claims selection quoted.
  - `dataset check` re-run.
  - The record's year 2017 and its 301 and 403 claimants, fixed at hand-over.

**What the curator decides.** Two calls change the shipped form, and neither drops a row:
- the split: amend SPLIT-14, or re-split forced grouped;
- the metric: the source's Gini now, or a context metric.

One check can still retire the dataset: tuned methods against log coverage in 2009 (TP-4). The rest is fixes to the
definition that the critic and I agree on.

</details>

<details><summary>Critic rebuttal</summary>

**Critic, rebuttal (2026-11-01): wisconsin_local_government_property_insurance_fund**

```text
Verdict: ship after changes. The advocate and I now agree on that, and on the metric, the data, the cleaning and the
  tuned check. One dispute is left: whether the fit stays `direct` (USE-8). One point is narrowed: the split, where
  either remedy works and the choice is the curator's.
Open for the curator: USE-8 (approximate, or record the short-tail fact); SPLIT-14 (amend, or re-split grouped).
```

No new run was needed. The points below turn on the rule texts, the book's own passage on open claims
(the source of the book's introduction chapter) and the builder's scale probe.

**Advocate 1 (use case and direct fit): concede the use case, contest the fit label.**
- Conceded: the actor, the moment and the decision are the fund's own rating engine (USE-1). The inputs are that
  engine's variables, and the missing inputs (endorsements, county, the full fire class) lower the ceiling without
  making the data a stand-in.
- Contested: "direct or approximate is a wording call". USE-8 is a Must, and its definition of direct includes "the
  label's timing". The advocate concedes that the training years carry final amounts the fund would not have at
  renewal. That is a known gap, and USE-8 names a known gap `approximate`.
- The advocate's measured reason fails on the metric we both want to ship. With the gap, R^2 does not drop. But on the
  Gini, the declared score, the 2010 tree models drop by 0.05-0.09 with the gap, and by 0.05-0.16 even without the
  $12.9M claim (split auditor, problem 3). Recency and maturity cannot be told apart, so the gap test decides nothing
  either way.
- The short-tail reason is not measured: CLAIMLEVEL.csv has no report dates. The source points the other way. The
  book drops the whole 2011 policy year "to mitigate the effect of open claims", and that is for this property line,
  read after that year had ended. At a renewal, the year just ended is a few months old at most.
- Rule that wins: treat like cases alike (principles.md, "Conflicts between rules"). lending_club ships the same
  SPLIT-10 exception as `approximate` (CC 2026-10-21, Lennart), and no measured fact sets this case apart.
- Remedy, unchanged: fit `approximate`, with the training labels' timing in `fit_reason`. If the curator accepts the
  short-tail fact, record it as what sets the case apart. I agree that neither label changes a row.

**Advocate 2 (clean inputs, premium held out): concede.** I raised none of it. LEAK-10 holds for every kept column,
and the hold-out follows USE-6 as applied in 2_month_survival_rate_prediction.

**Advocate 3 (faithful data): concede.** We ask for the same two sentences: the close extract (PROV-9) and the
closed-claims selection (LEAK-24, untested).

**Advocate 4 (split): narrow.**
- Agreed: two windows break SPLIT-14, a Must takes no exception, and the dataset does not ship as defined. Either (a),
  the curator's amendment, or (c), the forced grouped re-split, fixes it.
- Narrowed: I drop my preference for (c). The advocate's best reason is a real one. SPLIT-4 (Must) comes before
  SPLIT-8, and SPLIT-8 does not say that it narrows SPLIT-4. SPLIT-8 does narrow USE-10, the known-entity rule that
  SPLIT-4 applies here, and its 2026-10-21 amendment was written for recurring entities with too few periods
  (open_university). So the two rules meet on exactly this case. Settling that meeting is the curator's (a)/(c) call,
  and (a) must be recorded as an amendment with its scope, never as an exception.
- Contested: two of the advocate's reasons do not favour (a).
  - The $12.9M claim also dominates the shipped 2010 window: removing it moves that Gini by 0.10-0.14 and reverses the
    model order. Both regimes carry its noise.
  - The year effect under grouping (+0.009 R^2) is smaller than the bootstrap SD of either metric within a window.
  - What (a) preserves is the faithful design. It does not preserve measured signal: the warm start measures nil
    (CatBoost with `PolicyNum` 0.236 / 0.238 against 0.245 / 0.242 without it).
- Still asked under either remedy: say in `splits_comment` that the test years are the lowest and the highest claim
  years and that one 2010 claim reorders models (SPLIT-20, a note).

**Advocate 5 (metric): concede.** We ask for the same fix: a base-weighted ordered-Lorenz Gini under a general name
(MET-12, MET-13), with `Premium` as the `ScoringColumn` and `Metric.source`. If the curator rejects MET-5, the origin is
`context`. The stand-in goes either way.

**Advocate 6 (worth benchmarking): concede, with one fact that helps the advocate.**
- `Trivial` is not proved. Under the source's premium base, the metric we both want, several untuned models beat
  coverage in 2009 (2009: extra trees 0.272, Tweedie GLM 0.265, ridge 0.242; coverage 0.195; the builder's scale probe).
  TP-4's fold-by-fold test is not met there. Coverage still leads in 2010 (0.540 against at most 0.385).
- Narrowed: the "sound against broken methods" evidence is RMSE on log1p. It shows signal, not that the declared
  metric resolves methods.
- Remedy, agreed: run the tuned methods against `LnCoverage` before the build (TP-1), and state coverage's score in the
  metric's reason.

**Advocate 7 (cleaning): concede, and narrow one sentence on the scale.**
- `NoClaimCredit`, `Fire5`, `PolicyNum` and the text corrections: agreed as the advocate states them.
- Narrowed: "the scale changes how models are fit, not what is scored". That holds for the stand-in, which depends
  only on the ranking. It is false for the premium-base Gini we both ask for, which sorts by prediction / premium.
  On the builder's scale probe:

  | year | extra trees (log1p / raw) | LightGBM (log1p / raw) | random forest (log1p / raw) | ridge (log1p / raw) |
  |---|---|---|---|---|
  | 2010 | 0.082 / 0.282 | 0.079 / 0.259 | 0.158 / 0.362 | -0.044 / 0.241 |
  | 2009 | 0.272 / 0.218 | 0.166 / 0.123 | 0.179 / 0.215 | 0.242 / 0.086 |

  Under that metric the shipped scale moves scores by up to 0.29. Raw wins every family in 2010; log1p wins 3 of 4 in
  2009.
- Remedy: decide the scale together with point 5, under the final metric, with a reason specific to this dataset
  (CLEAN-16, MET-3). The advocate already says they would not defend log1p under the premium base, so we agree on the
  remedy.

**Changes I still ask for, in rank order:**
1. USE-8: fit `approximate`, or the curator records the short-tail fact.
2. SPLIT-14: the curator's amendment, or the re-split.
3. MET-11 and MET-13: `Metric.source` with the base Gini, and `Premium` as the scoring column.
4. TP-1: the tuned check against `LnCoverage`.
5. The target scale, decided under the final metric.
6. `NoClaimCredit` and `Fire5`: a note, or the one-line fix.
7. The note corrections, and a regenerated README.

</details>
