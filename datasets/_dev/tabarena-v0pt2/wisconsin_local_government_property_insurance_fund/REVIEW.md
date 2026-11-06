# wisconsin_local_government_property_insurance_fund

**Outcome:** added. Shipped on 2026-11-02 (the curator's verdict: changes, applied) on three expanding yearly windows
(test 2008, 2009, 2010) with no gap and the claims in dollars (issues 1 and 2); the split is open again since
2026-11-05 (issue 3). The re-review of 2026-11-06 recommends shipping after changes: its text changes are made, and for
issue 3 it recommends folds by member with the test year left out of training (F). The building-and-contents cover of
Wisconsin's Local Government Property Insurance Fund, 2006-2010, from the open textbook Loss Data Analytics: 5,639
member-years of 1,227 counties, cities, towns, villages, school districts and other members; the target is the year's
claims in dollars (0 for 70.2%), the inputs are the fund's rating variables, and the score is the source's Gini against
the fund's premium. Validity: USE-1 holds (the fund's own rating project, Lee 2017); USE-8 triggered, fixed (fit
approximate: the training years carry final claim amounts the fund knew only in part at renewal, as lending_club, and
the public file lacks rating inputs); USE-6 holds (the premium is the source's comparator and the rating's output, a
scoring column only, as 2_month_survival_rate_prediction; MET-2 as reworded on 2026-11-05 keeps it so); LEAK-41 holds
(the premium is set at the start of the year and not prorated, no time on risk exists, the coverage is a feature);
MET-15 holds (no training weight: the target is a total and the premium is not realized); LEAK-10 holds for every kept
column; SPLIT-14 broken: the 2008 window trains on 40.6% of the rows, and a Must takes no exception (issue 3); LEAK-6
and SPLIT-8 triggered on the member folds the rules send this release to (the year's claim level and a smaller
within-year share cross them; F removes both); SPLIT-10 departed from (no gap; its precedent "as
pricing_game_2016_french_fleet" is stale, since that case is reopened and never covered a window below the floor; moot
under C, E or F); PROV-9 holds (rows first published 2017, a close extract of the paper's sample), and the licence
reason now names the second edition's identical rows under CC0-1.0, where a stated licence can be had if the release
needs one. Value: MET-11 and MET-13 triggered, fixed (the source's metric, new in the library); MET-2 holds (one year's
Gini against that year's premium is the source's own, Sec. 6.2, and E and F both give it); MET-5 holds (the Gini is
argued, Spearman reported beside it); TP-4 holds narrowly: coverage alone leads the untuned models in every design but A
(0.368 against 0.30-0.31 for a Tweedie GLM on the two valid windows, 0.198 against 0.139 under F); the task probes flag
`no_signal`, which reads an R^2 on dollars, while on the declared Gini the untuned GLM without the member id scores
0.244, 0.256 and 0.346 on the shipped windows against the premium's 0 (the split auditor's run, which the claim auditor
matches; issue 3's run of the same models differs by its setup, within noise). TP-2 keep; re-read TP-4 on the first
benchmark run. Quality: CLEAN-10 triggered, fixed (`NoClaimCredit` missing without two earlier years; `Fire5`'s
unknown class kept with a note); CLEAN-16 exception kept (dollars, issue 2). Weighed: documented source and real
decision +; small test sets, one claim that is 35% of 2010's losses, rating inputs the public file lacks (endorsements,
county, the full fire class) and unseen members under any forced split -. Issues 1 and 2 are resolved; issue 3 (the
split, to decide together with pricing_game_2016_french_fleet issue 6) is open.

Changes made after the review panel (AI, 2026-11-01): the changes the panel agreed are made (the source's metric
`ordered_lorenz_gini`, new in the library, with `Premium` as base and scoring column; the target in dollars;
`NoClaimCredit` missing for the 2,412 member-years without two earlier years in the file; folds grouped by member,
`PolicyNum` the group and no feature; fit approximate; notes corrected, README regenerated). Changes after the
curator's marks (AI, 2026-11-02): the member folds replaced by three expanding yearly windows, no gap, `PolicyNum` an
input, `ForcedGroupedFromTemporal` dropped; every split figure re-measured. Changes after the re-review (AI,
2026-11-06): text only (the exposure note's reasons, the metric note's baselines, the licence reason, the no-gap
precedent marked stale). The review panel below is that re-review; the full panel of 2026-11-01, which saw the
definition before the changes of 2026-11-02, is in this file's git history.

**Main points:** Open: issue 3, which split the five policy years get: the three shipped windows (A) break the floor
of half the rows; recommended F, folds by member with the test year left out of training, else E (folds by member
scored within each year, a measured within-year leak kept with a note) or, by an amendment of the windows rule, B (the
two valid windows); decide it together with pricing_game_2016_french_fleet issue 6. Resolved: issue 1 (the three
windows, on the curator's call of 2026-11-02, reopened by issue 3) and issue 2 (the claims in dollars).

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
