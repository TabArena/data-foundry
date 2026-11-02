# allstate_claim_prediction_challenge

**Outcome:** added as `allstate_claim_prediction_challenge_1m`. The AI recommends shipping it after the panel's changes,
listed below; the forced split is settled (2026-11-02). The source is Allstate's Kaggle competition (2011): one row per
insured vehicle and calendar year, the target its bodily-injury liability claim payments, adjusted by Allstate for
non-vehicle effects by an undisclosed rule (0 for 99.27% of rows), shipped as log1p and scored by the competition's
normalized Gini on the amount. After the changes it holds 2005-2006 only (8.5M rows, 1.5M of whole households sampled),
split by household and tagged as forced from temporal. Validity: USE-1 holds (approximate fit; a pricing actuary on the
panel agrees); LEAK-24 is triggered by the 2007 claims, whose large claims are missing at a stable claim rate and
median, and fixed by dropping 2007 (issue 2), which also removes a bonus the pooled test folds gave for knowing each
year's claim level (MET-2); LEAK-10 is triggered by our `household_vehicles`, fixed by dropping it (issue 3); SPLIT-8
holds, the split shipped on your call of 2026-11-02 (forced grouped splits ship; SPLIT-8 amended); Cat10 to Cat12 behave
like random draws and are dropped (PROV-3). Value: TP-2 holds, narrowly (issue 4). On the rebuilt folds untuned LightGBM
scores 0.053 / 0.054 / 0.022 against a spread of 0.019 to 0.025 for random predictions, so the third fold is within the
noise of chance. The signal still counts as real: a claim classifier ranks the amounts above chance on every fold (0.065
/ 0.060 / 0.039). The changes took part of the signal the panel saw (0.096 / 0.051 / 0.058 before them). MET-4 holds;
three folds tell methods apart only when they differ by about 0.03 (MET-10). Quality: `OrdCat` categorical as in the
insurance siblings (CLEAN-14); the target scale follows your answer to australian_vehicle_insurance_2004_2005 issue 5
(log1p scores higher than the raw amount on all three rebuilt folds, 0.022 to 0.054 against 0.001 to 0.035, the raw
scores within the noise of chance; no winner in the mediator's sample). If dollars are chosen there, this is the fact
that sets this table apart. Weighed: Allstate's own competition +, a real pricing task +, an undisclosed adjustment -,
weak signal, one fold within the noise of chance -, new vehicle series and known households untested -. Left for Andrej:
issues 2 to 4.

Changes made after the review panel (AI, 2026-11-01):

- The 2007 rows are dropped; `Calendar_Year` stays a feature (two years; the model's pooled score exceeds its score
  within each year by at most 0.001 on the rebuilt folds).
- `household_vehicles` is dropped, and `Vehicle` stays dropped.
- Cat10, Cat11 and Cat12 are dropped: the same vehicle keeps its value from one year to the next only as often as a
  random redraw would, and they relate to no other column or the claim (Cramér's V at most 0.0024).
- `OrdCat` is categorical; its claim rates over the levels (0.11% to 0.82%) show no risk order.
- `fit_reason` and the notes name what the folds do not test: next year's book (53% of it known households, whose
  claim history matters), new vehicle series, and complete rows only (the application has no missing values; 73% of
  the shipped rows have one). They also say that no exposure is published and some rows are part years.
- The notes are corrected where the data contradicted them (the LEAK-30 evidence, the level counts, the share of
  repeated feature rows) and every score is restated from the rebuilt folds, with the test that missingness carries
  no outcome beyond the vehicle type.
- Record, at hand-over (no mark needed): the Assessment's "Exposure: none (rows are vehicle-years)" now says none is
  published and some rows are part years.

**Main points:** Confirm dropping 2007 (2) and `household_vehicles`
(3), and keep the Gini regression although one fold is within the noise of chance (4).

**Issues for Andrej:**

2. **Drop the 2007 rows (implemented), or keep them and drop only `Calendar_Year`?** Bodily-injury claims are paid over
   years, and the release gives no date at which the amounts were read. In 2007 the claim rate and the median claim
   match the earlier years, but the large claims are missing: claims above 2,000 are 0.43% of claims against 1.31% and
   1.26% in 2005 and 2006, in every vehicle-age band and each of the three largest makes, and the shortfall grows
   toward the tail (2007 against 2005: 1.01 at the median, 0.59 at the 99.9th percentile). That is what unsettled
   claims look like (LEAK-24, Must: a target cut short in the newest period is cut where follow-up is complete).
   * What it did to the benchmark: the test folds mixed three years, so a model gained by learning each year's claim
     level from other households of the same year. Before the drop, a predictor that knew only the year scored 0.055
     to 0.058, as much as the probe model on two of three folds (MET-2, Must: the competition scored one year at a
     time, and a rating for next year has no year to rank).
   * Evidence for the drop: on the rebuilt folds the model's pooled score exceeds its score within each year by
     -0.000 to +0.001, so the bonus is gone; a year-only predictor scores 0.001 to 0.026, within about one spread of
     random predictions. Dropping only `Calendar_Year` left +0.001 to +0.003, positive in 8 of 9 runs, as the year
     stays readable through other columns. The drop costs no rows of the budget (8.5M rows remain for the 1.5M
     sample), and in the mediator's sample no measurable score; on the rebuilt folds the score fell to 0.053 / 0.054 /
     0.022, of which the drop of issue 3 explains 0.015 to 0.020 and fold-to-fold noise the rest (issue 4). In the
     mediator's experiment (same changes, its own 1.5M
     sample) the model scored 0.050 / 0.089 / 0.050 after the drop against 0.072 / 0.052 / 0.040 with 2007 kept and the
     year column dropped.
   * Against: the newest labelled year is lost. The critic notes that Allstate scored 2008 and 2009, years younger than
     2007 is here, and that a step at 2007 with no change between 2005 and 2006 fits a change in Allstate's adjustment
     as well; no date can settle it. The domain practitioner would keep 2007 with a year factor.
   * Precedent: follows sf_permit_time (cut where follow-up is complete). It departs from the reading recommended for
     frempl issue 3 (keep amounts of unknown valuation date); what sets it apart is a shortfall measured across years
     and a cut that costs no rows of the budget, where frempl has one year.
   * Implemented: 2007 dropped, `Calendar_Year` kept. Alternative: keep 2007, drop `Calendar_Year`, and record
     "LEAK-24 not shown violated" with the tail figures in `fit_reason` (a small year bonus remains).

   Recommendation: keep the drop. Decision: drop 2007, or keep it without `Calendar_Year`?

3. **Drop `household_vehicles` (implemented), or replace it by the household's vehicle count of the previous year?**
   We built the column to replace the source's `Vehicle`: the household's vehicles insured in the calendar year. But the
   file lists every vehicle insured at any time in the year, so the count includes cars added after the rating, among
   them replacements after the row's own crash. Vehicles already insured the year before claim at 1.17% in a year when
   the household's count rose, and at 0.72% otherwise; in years with a short-lived extra car the rate is 0.98% against
   0.72%. On the earlier folds the column added 0.015 to 0.020 Gini, about a quarter of the score (LEAK-10, Must; its
   2026-10-26 clause: late values that cannot be located row by row go when they may carry a gain, a case-by-case call
   of yours). The pricing_game_2017 count it cited comes from a start-of-year policy file, so that precedent does not
   carry.
   * Implemented: dropped; `Vehicle` stays dropped, as it carries the same count. The drop takes part of the signal: the
     third rebuilt fold now scores within the noise of chance (issue 4), and the mediator's sample with the same changes
     scored 0.050 to 0.089, so fold-to-fold noise does the rest. Alternative: the previous year's count, known at the
     rating and built without labels, which kept +0.006 to +0.013 on three years; with 2007 dropped it is missing for
     every 2005 row (47.5%) and every new household.
   * The advocate and the critic accept either; the drop follows kick and 2_month_survival_rate_prediction.

   Recommendation: keep the drop. Decision: drop, or the previous year's count?

4. **Keep the regression scored by the competition's Gini, although one of the three folds scores within the noise of
   a random prediction?** The normalized Gini scores how well the predictions order the vehicle-years by claim amount
   (1 a perfect order, 0 a random one). On the rebuilt folds untuned LightGBM scores 0.053 / 0.054 / 0.022; random
   predictions average -0.002 to 0.004 with a standard deviation of 0.019 to 0.025 over draws, so the third fold is
   about one standard deviation above chance and the other two more than two. The panel judged the signal on stronger
   numbers (0.096 / 0.051 / 0.058 before the changes); dropping `household_vehicles` (issue 3) and 2007 (issue 2)
   lowered it.
   * What it does to the benchmark: with a standard error of 0.022 to 0.029 per fold, two methods must differ by about
     0.03 before three folds tell them apart (MET-10), and on a fold like the third a method's score is mostly noise.
   * Evidence that the signal is real (TP-2, Should: a small but real signal is no reason to retire): a regularised
     classifier of whether a claim occurs ranks the amounts above chance on every fold (0.065 / 0.060 / 0.039);
     trained on 2005 and scored on 2006, the rebuilt rows reach 0.064; the three folds' mean, 0.043, is three to four
     times the spread of a random three-fold mean. No tuned results exist yet (TP-1, Must: a flag is checked against
     the benchmark's tuned methods).
   * Precedent: pricing_game_2016_french_fleet became a claim classification scored by ROC AUC on 2026-10-30, on your
     question, because its claim amounts carried no signal. Here too the amount among claimants carried none (R^2
     below 0 on the folds before the changes) and a claim classifier ranks the amounts better than the regression on
     every rebuilt fold. What sets this one apart: Allstate fixed the Gini on the amount for its competition (MET-4,
     Should); pricing_game_2016's source fixed no metric.
   * Implemented: the regression on log1p, scored by the Gini on the amount, with the noise in the notes. Alternative:
     a claim classification scored by ROC AUC (standard error about 0.005 per fold by the blind reviewer's estimate,
     its proposal), which drops the claim size the competition scored and departs from MET-4.

   Recommendation: keep, and revisit under TP-1 when tuned results exist (reframe if tuned methods do not beat a
   random prediction on every fold). Decision: keep the Gini regression, or a claim classification?

**Review panel:** ship after changes (mediator). Claim audit: 33 claims, 19 hold, 8 refuted in whole or part (7 fixed
in the definition, the eighth was the builder's report), 1 mixed, 1 record disagreement, 4 untested. Blind review:
would exclude as prepared; its main concern is how little a log1p regression learns; it proposes a claim yes/no target
scored by AUC, and calls the Gini on the amount (what ships) unstable at this size (issue 4). Debate: agreed on shipping after changes, on dropping `household_vehicles` or replacing it,
on dropping Cat10 to Cat12, `OrdCat` categorical and the number fixes; disputed: drop 2007 or only `Calendar_Year`
(issue 2) and how the forced split goes to the curator (issue 1).

<details><summary>Mediator</summary>

**Mediator (2026-11-01): allstate_claim_prediction_challenge_1m**

**Recommendation**

```text
Verdict: ship after changes.
Validity: SEL-2 holds; USE-1 holds (approximate fit; the domain practitioner agrees); LEAK-24 triggered on measured
evidence (the 2007 claims lose their tail at a stable rate and median), fixed (2007 dropped; issue 2); MET-2 triggered
(the pooled folds reward the year's claim level), fixed by the same drop; LEAK-10 triggered (`household_vehicles`
counts vehicles added after the rating), fixed (dropped; issue 3, LEAK-10's case-by-case clause); SPLIT-14 fails, so
SPLIT-8 applies (ForcedGroupedFromTemporal), open against how_much_did_it_rain (issue 1); SPLIT-24 and SPLIT-29 hold;
PROV-3 at column level: Cat10-Cat12 behave like random draws, dropped.
Value: TP-2, a small real signal after the changes (Gini 0.040-0.089 per fold against a null SD of 0.020-0.031);
MET-4 holds (the competition's normalized Gini; the library equals Kaggle's code to 4 decimals); MET-10 weak
separation of methods, noted.
Quality: CLEAN-14 `OrdCat` categorical (aligned with liberty and pricing_game_2017); CLEAN-16 log1p follows
australian_vehicle_insurance_2004_2005 issue 5; notes restated from the rebuilt folds (EV-8).
Weighed: Allstate's own competition +, a real pricing task +, 8.5M rows left after the drop +, undisclosed target
adjustment -, weak signal and wide fold noise -, new vehicle series and known households untested -.
For the curator: issue 1 (the family's forced-split call), issue 2 (2007), issue 3 (`household_vehicles`).
```

**Agreed facts**

- 13,184,290 rows, 95,605 claims (99.27% zeros), none negative; 4,309,042 households; 71.3% of the 2007 households are
  in 2005-2006; 53.3% of the competition's test households are in train (claim auditor, split auditor).
- The years: 2005 30.5%, 2006 33.7%, 2007 35.7% of rows. Only the 2007 window keeps half the rows for training, so
  SPLIT-14 fails and SPLIT-8 applies. Without 2007: 8,473,402 rows, 61,838 claims, 3,445,943 households, and 2005 is
  47.5% of the rows, so no valid window remains at all (mediator, raw file).
- No household is on both sides of any shipped fold; random-row folds score 0.050-0.080 against 0.051-0.096 grouped
  (split auditor).
- The 2007 tail: claims above 2,000 are 0.43% of claims against 1.31% and 1.26%, in every vehicle-age band and each of
  the three largest makes; the 2007/2005 quantile ratio is 1.01 at the median, 0.65 at p99 and 0.59 at p99.9. No
  valuation date exists (claim auditor).
- A year-only predictor scores 0.055-0.058 on the shipped folds; dropping `Calendar_Year` leaves a bonus of +0.001 to
  +0.003 (positive in 8 of 9 runs); dropping 2007 leaves none (advocate's check, split auditor).
- `household_vehicles` counts every vehicle insured in the calendar year; swap years claim at 0.98% against 0.72%; it
  adds 0.015-0.020 Gini against its absence (column auditor). `Vehicle` carries the same composition.
- Cat10-Cat12 keep their value for the same vehicle at exactly the chance rate; Cramér's V against every column and the
  claim is at most 0.0024 (column auditor).
- Missingness carries no outcome beyond the vehicle type (leave-one-out test, column auditor); scores on complete and
  incomplete test rows show no consistent gap (claim auditor).
- Untuned LightGBM on the shipped folds: Gini 0.096 / 0.051 / 0.058, bootstrap SE about 0.02. The library metric equals
  Kaggle's reference code to 4 decimals; it matches 4 of thread 703's 10 test vectors, the other 6 differ by its stated
  tie rule (claim auditor; the builder's "all 10 reproduce" is wrong as written).
- Only 0.07-0.10% of test rows have an unseen model or submodel; folds grouped by `Blind_Model` score 0.085 without the
  codes (domain practitioner).

**Decisive experiment (mediator).** The definition after the agreed changes (`household_vehicles`, `Vehicle`, `Row_ID`
and Cat10-Cat12 out, `OrdCat` categorical), 1.5M rows of whole households drawn at random, 3 folds by household,
untuned LightGBM, the declared Gini on the amount.

| option | test claims per fold | log1p model | raw L2 model | year bonus |
|---|---|---|---|---|
| B: drop 2007 (`Calendar_Year` kept) | 3,719-3,742 | 0.050 / 0.089 / 0.050 | 0.068 / 0.063 / 0.038 | -0.002 to +0.001 |
| A: keep 2007, drop `Calendar_Year` | 3,604-3,648 | 0.072 / 0.052 / 0.040 | 0.065 / 0.045 / 0.052 | -0.000 to +0.003 (4 of 6 positive) |

Random predictions on B's folds (30 draws each): mean 0.001-0.005, SD 0.020-0.031. So the signal survives both options,
dropping 2007 costs nothing measurable (means 0.063 against 0.055 for log1p), and neither target scale wins.

**Changes to make now** (no decision needed; each with its rule and what the rebuild should reproduce)

1. `_clean`: keep `Calendar_Year <= 2006` (LEAK-24 Must, MET-2 Must; the cut of sf_permit_time). Reproduce: 8,473,402
   rows before sampling, 2005 = 47.5%; about 3,700 test claims per fold; year bonus within ±0.002. Issue 2 asks the
   curator to confirm. `Calendar_Year` stays a feature (two years, year-only Gini -0.021 to +0.010).
2. Drop `household_vehicles`; `Vehicle` stays dropped (LEAK-10 Must, second clause: late values that cannot be located
   go when they may carry a gain). Update `known`, `changes`, the bullet, and remove decision 4. Issue 3.
3. Drop Cat10, Cat11, Cat12 (PROV-3 at column level: not the vehicle characteristics the dictionary names; CLEAN-22 lets
   columns leave for what they are). A bullet with the chance-rate and Cramér's V numbers.
4. `OrdCat` categorical (CLEAN-14; liberty's ordinals and pricing_game_2017's `pol_coverage`); its claim rates show no
   risk order (0.26-0.81%). Remove the "so the order stays" comments.
5. `fit_reason` and notes (USE-5, USE-8): drop "the 2007 claims look less settled"; add that held-out households stand in
   for next year's book, so the 53% known households and their claim history (1.44% against 0.77% after a prior claim)
   are untested; that the folds test vehicle types seen in training (a new series is untested); that no exposure is
   published and some rows are part years (age -1 vehicles claim at 0.20%); that 71.7% of rows carry a missing value,
   which the application never has (thread 826).
6. Decision 2 and the anomaly bullet: 2007 dropped, with the tail table as the reason. Decision 3 and the missing-values
   bullet: add the leave-one-out test; restate shares on 2005-2006 (pre-2000 vehicles 47.9% of rows against 8.6% of
   the test file).
7. LEAK-30 note: NVVar1-4 do not rise; the Var rise follows the fleet's model-year mix; the means (-0.065 to +0.019)
   and SDs (0.97-1.04) show scaling over an unknown population, so "may have taken in the test years" (LEAK-30, weak).
8. `splits_comment` (SPLIT-8, EV-8): no window keeps half the rows once 2007 is gone (2006 trains on 47.5%); keep the
   cost measured on the full release as the SPLIT-8 evidence (window 2005-06 to 2007: 0.084 on 4.7M rows; on the
   shipped rows 0.063, about one SE below the grouped folds' 2007 rows, so no cost measurable at this noise); restate
   the grouped and random-row numbers from the rebuilt folds; say a release with dates should get a temporal split.
9. Number fixes (EV-8): level counts 74 / 1,302 / 2,739; the feature-repeat share re-measured on the shipped features
   (55.9% before the changes); `changes` names the dropped exact copy (in 2006, it stays relevant); the log1p bullet
   quotes the rebuilt folds (about 0.05-0.09 log1p against 0.04-0.07 raw).
10. Add `accepted_check_warnings` for `splits_rows_never_tested`, `groups_labels_constant` and
    `task_target_value_dominant`, with re-measured counts (as sepsis_prediction_1m).
11. Record, no mark needed: the Assessment's "Exposure: none (rows are vehicle-years)" becomes "none published; some
    rows are part years".

**Changes that need the curator**

1. The forced grouped split against how_much_did_it_rain (P4, SPLIT-8 Must; options as in rand issue 1). Recommend (a).
2. Drop 2007 (implemented) or keep it and drop `Calendar_Year` (P4, LEAK-24 Must; P6, MET-2 Must). Recommend the drop.
3. Drop `household_vehicles` (implemented) or replace it by the previous year's count (P4, LEAK-10 Must, a
   case-by-case clause). Recommend the drop.

The target scale is not raised here: it follows the answer to australian issue 5 (no winner measured here).

**Disputed points**

- 2007 against `Calendar_Year`. The critic now rests on LEAK-24 "not shown" and a weighing (the source scored younger
  years); the advocate on LEAK-24 and MET-2 (Musts). Both remedies sit on the same rung (fix the definition), so the
  one that resolves both Musts wins: dropping 2007 removes the bonus entirely, while dropping `Calendar_Year` leaves a
  small systematic residual (year readable at AUC 0.58 through the Var drift). The shape of the shortfall (tail only,
  median ratio 1.01) fits late development; a changed adjustment that rescales amounts would move the median too, and
  the missing 2005-2006 gradient fits both. The Tensions row on suspected leaks says "fix it when we can", and here the
  fix costs nothing (8.5M rows against a 1.5M budget; the experiment above). The critic's fact does not carry: the
  source scored one year at a time, so a young year's level never entered its ranking. Settled by rank for the drop;
  issue 2 asks the curator to confirm because it departs from the reading recommended for frempl issue 3.
- The forced split. Not mine to settle: SPLIT-8 holds as written, but the `Yes` was given on notes that said "Split
  temporal by `Calendar_Year`", and the curator's newer how_much_did_it_rain call may cover it (who decides). Issue 1.
- `household_vehicles`: lag or drop. Both accept either. The drop is the change: with 2007 gone, the previous year's
  count is missing for every 2005 row (47.5%) and every new household, it is our construction, and no fix of the same
  quantity exists (no dates within a year; LEAK-7). The lag stays the alternative in issue 3.
- `OrdCat`. The column auditor kept it numeric on the reading that liberty's ordinals are letters; liberty types them
  categorical as its data page lists them, so the reason does not hold. CLEAN-14 decides by the source's own word,
  "ordered categorical", and the data show no risk order.
- The blind reviewer's "exclude". It scored log1p RMSE and R^2, which the definition does not score; its own
  alternative (a Gini on the amount) is what ships. A small real signal under the right split is no reason to retire
  (TP-2, forest_fires). Not a ground.
- The domain practitioner. New series untested, no exposure and test-only missing values are fit gaps (USE-5, USE-8),
  so notes, not changes: a split by model would be another task (P4 follows the use case), no exposure can be rebuilt,
  and missingness carries no outcome while training on complete rows only scores worse (0.037-0.066). His Tweedie
  context metric is not adopted: policy call 3 (2026-10-30) rules it out as a benchmark metric without a clipping rule.

**Consistency with precedent**

- Forced grouped split: follows SPLIT-8's case open_university_learning_analytics_dataset; departs from Andrej's
  how_much_did_it_rain statement, with facts that may set it apart (households held out whole, no shared outcome across
  the split, random rows score alike, the window measured). Decided in one call with frempl issue 5, australian issue
  1, rand issue 1, spanish_motor_insurance_coverage_level_2022_2024 issue 1 and pricing_game_2017_french_mtpl issue 1.
  spanish's option "ship the one window" does not exist here once 2007 is dropped.
- 2007: now follows LEAK-24's remedy and sf_permit_time. It departs from the reading recommended for frempl issue 3
  (keep amounts of unknown valuation date). The fact that sets it apart: here the shortfall is measured across years,
  in every vehicle-age band, in the tail only, and the cut costs no rows of the budget; frempl has one year and no
  later period to compare. frempl issue 3 is an AI recommendation, not yet a curator decision.
- `household_vehicles`: the cited pricing_game_2017 `client_n_vehicles` comes from a start-of-year policy file, so it
  does not carry; the drop follows kick and 2_month_survival_rate_prediction (LEAK-10).
- `OrdCat`: now aligned with liberty_mutual_fire_peril_loss_cost and pricing_game_2017_french_mtpl.
- log1p: as frempl and both Spanish tables; one call in australian issue 5. If dollars are chosen there, CLEAN-16
  reaches its third departure and should be amended.
- Subsample, missing values, LEAK-30 keep, row copies, `Calendar_Year` as a feature: consistent (precedent checker
  items 1, 5, 8-11). None of the register's 14 flags concerns this dataset.

</details>

<details><summary>Claim audit</summary>

**Claim auditor: allstate_claim_prediction_challenge_1m (2026-11-01)**

Verdict: ship after changes. Most of the definition's claims hold on the data. One does not: that keeping 2007 is harmless because "every fold holds 2007, and `Calendar_Year` is a feature". The test folds pool three calendar years, and the 2007 rows have lighter claims. A predictor that knows only the year scores as well as untuned LightGBM on 2 of 3 shipped folds. The source scored one year per leaderboard, so its Gini could never reward that. Dropping 2007 removes the effect.

Every number below comes from the shipped frame and folds, rebuilt from `dataset.py`, or from the raw `train_set` (13,184,290 rows) and the published `test_set.csv`. The models are untuned LightGBM (default parameters, 2 threads), scored with `data_foundry.v2.metrics` on the amount.

**Table**

| claim | source | test | result | evidence | rule |
|---|---|---|---|---|---|
| Kept with 2007: "every fold holds 2007, and `Calendar_Year` is a feature", so the lighter 2007 tail does no harm | curation_comments (Anomaly bullet); decision 2 ("Kept; Calendar_Year is a feature") | On the shipped folds, score a predictor that knows only the year: the training side's mean amount per year. Also score LightGBM times that year factor, and both with 2007 removed | **refuted** | Year only: Gini 0.055 / 0.058 / 0.056 (SE 0.019-0.022). Untuned LightGBM: 0.0955 / 0.0513 / 0.0583, so the year predictor matches it on 2 of 3 folds. LightGBM times the year factor gains +0.013 to +0.015 on every fold (0.110 / 0.066 / 0.071). The raw-amount model learns the year: its mean predictions are 1.52 / 1.46 / 1.23 for 2005 / 2006 / 2007, and its pooled Gini beats its mean within-year Gini by 0.008-0.014. With 2007 removed, the year predictor scores -0.021 / -0.010 / +0.010. Other features still tell 2007 apart at AUC 0.58 without `Calendar_Year` | LEAK-24 (Must), MET-2 (Must), P4 |
| The metric means on our task what it meant at the source | metric declaration (`original`: "public leaderboard on 2008 and the final ranking on 2009") | Evaluation page; the year effect above | **refuted in part** | The Evaluation page scores 2008 alone (public leaderboard) and 2009 alone (private leaderboard). Our test folds mix 2005-2007, about 152k / 168k / 179k rows of each year. So the declared Gini also ranks years, which neither the source nor the use case (rating one coming year) does | MET-2 (Must) |
| `household_vehicles` is "known when a vehicle is rated" | curation_comments; task_summary.known; decision 4 | Look at the 2006 claim rate of households seen in all three years, by their vehicle-count pattern (2005, 2006, 2007) | **refuted in part (maybe a leak, circumstantial)** | The count covers every car insured in the calendar year, including cars added after the rating point. Where a car was swapped during 2006 (pattern 1,2,1), the 2006 claim rate is 0.979% per vehicle-year (1,161 claims), although each car was insured for only part of the year. When the added car stays (1,2,2) it is 0.717%, and for (1,1,1) 0.710%. Pattern (2,2,1) shows 0.993%, so the excess goes with a car leaving after a claim year, consistent with a totalled car being replaced within the year. Effect on the score: with minus without the feature, +0.019 / -0.008 / +0.007 | LEAK-10 (Must; the 2026-10-26 window clause), EV-6 |
| Potential leak, LEAK-30: Var1-8 and NVVar1-4 "yearly means rise from about -0.15 to +0.03 ... so the host's statistics probably took in the test years" | curation_comments (Potential leak bullet) | Yearly means. Means re-weighted to the 2007 model-year mix. Overall mean and SD of the training file, alone and pooled with the published test file | **refuted (the evidence); the conclusion untested** | NVVar1-4 do not rise: 0.010-0.034 in 2005, 0.006-0.015 in 2007. The Var1-8 rise is the fleet's mix of model years: at the 2007 mix, 2006 sits at -0.006 to +0.015 against 2007's 0.001 to 0.028, and within model years 2000-2004 Var2 and Var4 move by at most 0.02. The training file's means (-0.065 to +0.019) and SDs (0.97-1.04) are not 0 and 1, so the host standardised over some other population. Pooling with the test file (complete rows only) does not bring them closer, so which population it was cannot be settled | LEAK-30 (Should, weak), EV-6 |
| Normalized Gini, Kaggle's Evaluation page, on the amount | metric (`Metric.source`, `target_transform="log1p"`) | Read the Evaluation page, and score dummies on every shipped fold through `scorer` | holds | The page names "normalized Gini coefficient" for the leaderboard and the final ranking, with predictions sorted from largest to smallest. Dummy scores: a constant gives 0 (at most 2e-15), random predictions 0.008 / 0.008 / 0.003, the true values 1.0, a monotone transform of the true values 1.0. Each test fold holds 3,652-3,696 claims; the top 10 claims carry 6.3-7.1% of the loss | MET-1, MET-2, MET-3, MET-4 |
| The library metric equals Kaggle's apart from ties ("tied p averaged ...; the Kaggle code takes row order") | metric `definition` | Kaggle's reference code (thread 703, ties broken by row order) against ours, on LightGBM's test predictions | holds | Equal to 4 decimals on all 3 folds (0.0955 / 0.0513 / 0.0583), although 61-74% of the predictions are duplicated | MET-11, MET-13 |
| "all 10 cases of Kaggle thread 703 reproduce" | builder report, checklist | Run the 10 official test vectors through `_normalized_gini` | **refuted as written** | 4 of 10 match. The 6 vectors with tied predictions differ, by design: [1,2,3] against [0,0,0] gives -1 officially and 0 for us; [40,0,20,0,10] against [1e6,40,40,5,5] gives 0.6 officially and 0.75 for us. Kaggle's reference code itself reproduces all 10 | EV-7 |
| The rows with missing values do not change what the score means (kept; the competition's test file had none) | curation_comments (Missing values bullet); decision 3 | Score the same model on the complete test rows and on the rows with a missing value. Train on complete rows only and score the complete test rows | holds | Complete rows: 0.054 / 0.073 / 0.063. Rows with a missing value: 0.111 / 0.046 / 0.061, no consistent gap. Trained on complete rows only: 0.037 / 0.036 / 0.066 on complete test rows, so the incomplete rows help training | MET-2, thread 826 |
| Missingness carries no signal | curation_comments (random draws 0.047 against 0.042) | Builder's E3 log, plus the raw claim rate with and without a missing value | holds | Missing indicators alone give a Gini of 0.008 (E3). Claim rate 0.714% with a missing value against 0.754% without | LEAK-10 (missingness), thread 826 |
| 13,184,290 rows; 95,605 claims, none negative; 99.27% zeros; 4,309,042 households with 1 to 37 rows (3.1 on average); 71% of the 2007 households appear in 2005-06 | curation_comments; group definition; splits_comment | Counts on the raw file | holds | 13,184,290; 95,605; 0 negative; 99.275% zeros; 4,309,042 households, 1-37 rows, 3.06 on average; 2,146,910 of 3,010,009 = 71.3% | EV-2 |
| 4,314,865 test rows; the test file has no "?"; pre-2000 vehicles 45% of the training file, 8.6% of the test file; 53% of the test households appear in training | curation_comments; group definition | `test_set.csv`; thread 708 | holds | 2,118,739 + 2,196,126 rows; 0 "?"; 44.9% against 8.6%; 1,243,704 of 2,335,027 = 53.3% | EV-2 |
| 71.7% of rows have a missing value; complete rows keep 28.3%; Cat2 missing by model year | curation_comments | Raw file | holds | 71.74% / 28.26%. Cat2 is missing for 97.7-100% of model years before 1995 and 0% from 2000 | |
| One exact copy dropped; three vehicle-years twice with differing values | curation_comments | Duplicates on every column but `Row_ID`; duplicates of (household, vehicle, year) | holds | 1 copy (household 6365215, vehicle 4, 2006); 4 duplicated vehicle-years, the copy plus 3 that differ | LEAK-19 |
| `Vehicle`'s claim rate is flat | curation_comments | Raw claim rate by `Vehicle` | holds | 0.66-0.75% for vehicles 1 to 8 and above | CLEAN-3 |
| `household_vehicles`' claim rate "rises from 0.69% to 0.99%"; scores like `Vehicle` | curation_comments; decision 4 | Decision 4 table; with and without the feature on the shipped folds | holds, loosely | 0.69% at 1 vehicle, 0.98% at 5, then 0.87%, 1.24% and 0.79% for 6, 7 and 8 or more (not monotone). Paired difference -0.008 to +0.019 | |
| The 2007 tail: claims above 2,000 are 0.43% against 1.31% and 1.26%, at a stable claim rate and median | curation_comments; decision 2 | Quantiles of the claims by year | holds (the cause untested) | Median 47.2 / 46.6 / 47.7; 99.9th percentile 4,925 / 4,963 / 2,921; maximum 8,204 / 11,441 / 7,667. The 2007/2005 quantile ratio is 1.01 at the median, 0.85 at p90, 0.65 at p99 and 0.59 at p99.9: a falling tail, as late development would give. No valuation date exists | LEAK-24, EV-6 |
| "70% of the rows share every feature with a row of another household" | curation_comments | Hash the 32 shipped features; count the rows whose vector occurs in another household | **refuted (the number)** | 55.9% on the 32 shipped features; 80.1% without `Calendar_Year` and `household_vehicles`. The builder's 70.2% (explore2) used the raw columns without `household_vehicles` and counted any other row, the same household included. The reading (natural repeats) holds: 22.6% of test rows have an exact copy in training, and the copies' training claim rate does not follow the test label (0.82% / 0.60% / 0.63% where the test row has a claim, 0.68% / 0.68% / 0.62% where it has none) | LEAK-18 |
| Make, model and submodel have "75, 1,303 and 2,740 levels" | curation_comments (Dtypes) | Distinct values on the raw file | **refuted (minor)** | 74 / 1,302 / 2,739 once "?" is missing (the data dictionary gives the same counts); 75 / 1,303 / 2,740 count "?" | |
| Folds by household "scored 0.069 to 0.094 on their 2007 rows and 0.021 to 0.073 on all their rows"; the grouped split "costs little" against the window's 0.084 | splits_comment | Gini on the shipped folds, all rows and 2007 rows | the numbers are not the shipped folds'; the conclusion holds | The quoted numbers come from the builder's experiment 1 (GroupKFold on its own 1.5M-row sample). The shipped folds score 0.051-0.096 on all rows and 0.059 / 0.086 / 0.115 on their 2007 rows, still close to 0.084 | EV-8 |
| On the shipped folds: Gini 0.051-0.096, bootstrap SE about 0.02, random 0.003-0.008, R^2 -0.003; claim AUC 0.56-0.57; severity R^2 below 0 | curation_comments | Rerun on the shipped folds | holds (but see row 1) | 0.0955 / 0.0513 / 0.0583; random 0.0083 / 0.0083 / 0.0032 (builder's `shipped_check.json` gives the rest). Against a year-only predictor's 0.055-0.058 (EV-9), the "small real signal" lives within years: 0.032-0.115 per year | TP-2, EV-9 |
| Temporal windows fail SPLIT-14 (2005 is 31% of the rows), so the split is forced and grouped (SPLIT-8) | splits_comment; decision 1 | Arithmetic; check the split | holds | 2005 = 4,025,672 rows (30.5%). No household is on both sides in any fold. 157 rows are never tested and none is tested twice; the trims remove whole households (0 households cut) | SPLIT-8, SPLIT-14 |
| Warnings: `splits_rows_never_tested` (157), `groups_labels_constant`, `task_target_value_dominant` | builder report | As above, plus the expected share of mixed-label households if claims were independent | hold | 157 / 0. Mixed labels in 9,884 of 364,263 multi-row households (2.71%), against 2.73% expected from independence. Zero-inflation is written in the notes | |
| Claim rate of the sample stays that of the release (households drawn at random) | version_comment; splits_comment | Shipped frame | holds | 0.735% against 0.725% (in rows per household: 3.07 against 3.06) | |
| NVCat and NVVar1-4: the host "expected no 'main effects'" | curation_comments (Note) | Claim rate and mean amount by NVCat | the quote holds; the expectation fails on frequency | Claim rate runs from 0.53% (M, 5.8M rows) to 1.33% (D), but the mean adjusted amount only from 1.29 to 1.95: the adjustment seems to rescale amounts, not claim counts | USE-5 (note) |
| Huangfu 2015, p. 6: "only 95,605 non-zero values (about 0.73%) among the 13,184,290 records"; best 0.080 on 2007 (Sec. 5.0 d, p. 30) | curation_comments; record | Read `huangfu2015.txt` | holds | Page 6, Sec. 2.0, verbatim. Page 30: "on the test set is 0.080135" (test set = 2007) | PROV-16 |
| Thread quotes: 826 ("When the model is applied, all of the features will be collected") and 928 ("isn't actually in units of any major currency") | curation_comments | Thread JSON | holds | Verbatim; 826 also says "we do not want models to be able to take advantage of" missingness | |
| Record: no OpenML copy | record, screening | All ~24k OpenML datasets, searched by name and by row count 13,184,290 | holds | Only `Allstate_Claims_Severity` (2016; ids 42571, 44045, 44060, 45046) | PROV-7 |
| Record (screening): 3M rows of 2005-06, scored on 2007: claim AUC 0.59, Gini 0.093 | record comments | Rerun with raw columns | holds approximately | AUC 0.581, Gini 0.094 (claim probability 0.092) | |
| Record: `required_split: Temporal (NON-IID)`, tag `Non-IID (Temporal)`, "Split temporal by Calendar_Year" | record frontmatter and comments | Compare with the definition | **disagrees with the definition** (builder issue 10) | The definition ships a forced grouped split (SPLIT-8). The record is stale until the curator confirms | SPLIT-8, pipeline |
| Large bodily-injury claims are paid over years, so the 2007 payments are incomplete | curation_comments; decision 2 | None possible: no valuation date or second extract | untested | Inference (EV-2 rank 5). The undisclosed adjustment is the other explanation. Row 1 does not depend on which one holds | LEAK-24, EV-2 |
| The features are known when the year is priced (NVCat, NVVar, Cat, Var) | task_summary.fit_reason | Anonymised; the leak probes are clean | untested | Timing cannot be checked (LEAK-38). Builder probes: all R^2 at or below 0 | LEAK-38 |
| Kaggle threads 710 ("some makes/models removed from training"), 752 ("Selection bias?"), 736, 707, 720, 726, 702 | not cited | Read them | untested | Kaggle pages render in JavaScript, and the API needs a key, which the brief rules out. 710 bears on provenance and is worth a look by a human | PROV-18 |
| Tuned results (TP-1) | builder report | — | untested | No tuned results exist yet | TP-1 |

**Refuted and untested claims, ranked (validity first, Must first)**

1. **The 2007 anomaly kept, scored over pooled years (P4/P6; LEAK-24 Must, MET-2 Must).**
   * What it changes: the declared Gini rewards ranking the calendar years. A year-only predictor scores 0.055-0.058, as high as untuned LightGBM on 2 of 3 folds, and adds +0.013 to +0.015 to it on every fold.
   * That reward favours some method families over others. Models trained on the raw amount learn the 2007 level; models trained on log1p barely do (mean predictions 0.0295 against 0.0285). The builder's raw-against-log1p comparison inherits 0.008-0.014 of it.
   * The source never rewarded this: it scored one year per leaderboard. Rating a coming year has no year to rank either. The stated mitigation, `Calendar_Year` as a feature, is what lets models cash in on it.
   * Mildest remedy: drop 2007, the builder's alternative and LEAK-24's own fix ("cut where follow-up is complete"). With 2007 out, the year-only Gini is -0.021 to +0.010. That leaves 8.47M rows, so the 1.5M sample and the 1M/500k folds stay as they are; untuned LightGBM scores 0.030-0.069 on 2005-06 rows (about 2,400 claims per fold in this check, about 3,650 once the 1.5M rows are all from 2005-06).
   * Weaker options: dropping `Calendar_Year` alone leaves the year readable at AUC 0.58. A per-year Gini (`Calendar_Year` as a scoring column instead of a feature) needs a new library metric (MET-13) and still scores the 2007 amounts.
   * Since this does not depend on why 2007 is light, it settles builder issue 1 without the circumstantial tail evidence.
2. **`household_vehicles` "known when a vehicle is rated" (P4; LEAK-10 Must, window clause; maybe a leak, EV-6).**
   * What it changes: the count includes cars added during the year. In swap years (1,2,1) the claim rate is 0.98% against 0.72% for a lasting addition, consistent with a totalled car being replaced within the year. The evidence is circumstantial, and the effect on the score is nil (paired -0.008 to +0.019).
   * Mildest remedy: drop the feature, which shows no measured gain, or keep it with a `Potential leak, kept on purpose:` note carrying these numbers. It is the curator's case-by-case call under the 2026-10-26 window clause.
3. **The LEAK-30 note's evidence (P4; LEAK-30 Should, weak).**
   * What it changes: the note cites a yearly rise in NVVar1-4 that does not exist. The rise in Var1-8 is the fleet's model-year mix, so it says nothing about the test years.
   * Mildest remedy: rewrite the note to the measured fact. The training file's means (-0.065 to +0.019) and SDs (0.97-1.04) are not 0 and 1, so the variables were scaled over a population we cannot identify (one shift and one scale per column). Keep it as a weak note, or drop it.
4. **The 2007 cause (LEAK-24; untested).** No valuation date exists. The cause no longer decides anything if item 1 is taken.
5. **The builder's "all 10 cases of thread 703 reproduce" (EV-7).**
   * What it changes: nothing in the definition. The library matches the 4 official vectors without ties and averages the 6 with ties, as its `definition` says. On the shipped folds it equals Kaggle's code to 4 decimals.
   * Remedy: correct the checklist line to say the reference code reproduces all 10 and the library the untied 4.
6. **Number slips in the notes (P7; EV-8).**
   * "70% ... of another household" measures 55.9% on the shipped features.
   * The level counts are 74 / 1,302 / 2,739 once "?" is missing.
   * The splits_comment's "0.021 to 0.073" and "0.069 to 0.094" come from experiment-1 folds, not the shipped folds (0.051-0.096 on all rows; 0.059-0.115 on the 2007 rows).
   * The `household_vehicles` claim rate does not rise monotonically.
   * `changes` omits the dropped exact copy.
   * Remedy: restate each with its source.
7. **Record against definition (builder issue 10).** `required_split` Temporal and the `Non-IID (Temporal)` tag are stale once the curator confirms SPLIT-8. Update them when the definition settles.
8. **Untested, for a human:**
   * Kaggle thread 710 ("some makes/models removed from training") and 752 ("Selection bias?") were not read.
   * Feature timing of the anonymised fields (LEAK-38).
   * Tuned results (TP-1). With an SE of 0.02 per fold against scores of 0.05-0.10, the three folds will separate methods poorly (MET-10).

Consistency note for the precedent checker: the severity stage here carries no signal (R^2 on claimants -0.04 to -0.10), and a claim-probability model ranks amounts as well as the regression (Gini 0.098 / 0.060 / 0.073 against 0.096 / 0.051 / 0.058). These are the facts that turned `pricing_game_2016_french_fleet` into a classification task on 2026-10-30. What sets this case apart is the competition's own metric on the amount (MET-4).

</details>

<details><summary>Column audit</summary>

**Column audit: allstate_claim_prediction_challenge_1m (column-auditor, 2026-11-01)**

**Verdict:** ship after changes. One built column, `household_vehicles`, partly counts vehicles that join the
household after the rating, including replacements that follow the row's own crash (LEAK-10, CLEAN-19). Three host
columns, Cat10 to Cat12, behave like random values drawn fresh for every row (a PROV-3 question for the curator).
Missingness is cleared by a conditional test. All other columns are fine. Two USE-5 facts about the target belong in
the notes.

**How I tested:** the prediction point is the first `curation_comments` bullet: when a vehicle's year of
bodily-injury cover is rated. Meanings come from the data page (as saved in the run) and the data
dictionary (as downloaded with the data). I did not rebuild the frame through `dataset_io.py`: that reads the 2.7 GB CSV
while other panel agents were using the machine's memory. Instead I used two inputs. Dtypes and categories come from
the clean-room sample (300,000 rows of the shipped frame). The tests ran on the builder's `train.parquet` (the raw
file, 13,184,290 rows) with the definition's cleaning replicated. The leak probes score R^2 on a target that is 99.27%
zeros, so they cannot flag a column ("each feature alone: 0.0"). Every test below uses claim rates, ROC AUC on
claim > 0, or the declared normalized Gini.

**Column table**

| column | meaning (codebook) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `Household_ID` | "allows year-to-year tracking of each household" (data page) | yes | int64; group column, never a feature | fine | LEAK-33 |
| `Calendar_Year` | "year during which vehicle was insured (not blinded)" | yes | int64, 2005-2007 | fine (it lets a model fit the lighter 2007 tail; that is the target's LEAK-24 issue, not this column's) | USE-6 |
| `Model_Year` | "model year of vehicle (not blinded)" | yes | int64, 1981-2009. Two rows have model year 2009 in calendar 2007 (age -2): impossible. The 155,989 rows of age -1 are plausible (next model year sold in the autumn) | fine. The 2 impossible values → missing, if sampled (trivial) | CLEAN-11 |
| `Blind_Make` | coded make, "ACME, coded A"; 74 levels in the dictionary | yes | category; "?" (8,431 rows, always with Model and Submodel) → missing; levels sorted | fine | CLEAN-10, CLEAN-14 |
| `Blind_Model` | coded model "A.1"; starts with the make in 100% of rows | yes | category, 1,302 levels | fine (categorical at this cardinality, as zillow's 3,030-level `census_tract`) | CLEAN-14 |
| `Blind_Submodel` | coded submodel, ".0" = base model | yes | category, 2,739 levels | fine | CLEAN-14 |
| `Cat1`, `Cat4`-`Cat9` | "categorical vehicle variable" | yes: constant within submodel x model year for 99.7-99.9% of rows (Cat9 97.8%), so attributes of the vehicle type | category; "?" → missing | fine | CLEAN-10 |
| `Cat2` | same; missing for model years up to 1998 (85-100%), 2.6% in 1999, 0% from 2000 | yes; missingness is set by the vehicle type (next section) | category | fine | LEAK-38 test passed |
| `Cat3` | same; varies within a vehicle type (47% of rows) but never changes for the same vehicle across years (100% kept) | yes (vehicle-level attribute) | category | fine | |
| `Cat10`, `Cat11`, `Cat12` | dictionary: "categorical vehicle variable". On the data: values that look randomly drawn for every row (next section) | moot: no vehicle characteristic is measured | category; Cat12 alone codes missing as a blank, not "?" (28,882 rows, every one with Cat11 = "?") | question for the curator | PROV-3, CLEAN-22 |
| `OrdCat` | "ordered categorical vehicle variable", 1-7 | yes (same vehicle across years: kept in 99.99%) | float64; "?" → NaN; a number keeps the stated order | fine. Builder issue 8: liberty's ordinal codes are letters, so the sets differ in fact, not in rule | CLEAN-14 |
| `Var1`, `Var3`, `Var5`-`Var8` | "continuous vehicle variable, mean 0 stdev 1" | yes: vehicle-type constants (vary within submodel x model year for 0.5-2.6% of rows) | float64. Var8 reaches 47 SD, but these are type constants of 53 submodels (BA.8.0 = 14.6): unusual, not impossible | fine; LEAK-30 note kept (wording below) | LEAK-30, CLEAN-11 |
| `Var2`, `Var4` | same; vary within a vehicle type (57%) but are fixed for the same vehicle (99.99%): trim-level attributes | yes | float64 | fine; LEAK-30 note | LEAK-30 |
| `NVCat` | "categorical non-vehicle variable", 15 levels | probably (a policy attribute): identical across a household's vehicles in every multi-vehicle household-year; 88.3% kept 2005→2006. Timing cannot be tested | category | fine; the note needs the numbers below | LEAK-38, USE-5 |
| `NVVar1`-`NVVar4` | "continuous non-vehicle variable, mean 0 stdev 1"; 91-93% at the minimum, 19-31 discrete values (count-like) | probably: policy-level (identical across the household's vehicles), change between years for 5-6% of households. Claim rate 0.68-0.72% at the minimum, 0.8-1.4% above it: a modest risk factor. A count of the year's own claims would put the claim rate near 100% | float64 | fine; LEAK-30 note | LEAK-38, LEAK-30 |
| `household_vehicles` | built: the household's rows in the calendar year | **partly no**: the calendar-year file holds every vehicle insured at any time in the year | int64 | **leak**: likely, circumstantial; weak to moderate (+0.017 Gini) | LEAK-10, CLEAN-19 |
| `log1p_claim_amount` | log1p of the adjusted "dollar amount of claims experienced for that vehicle in that year" | (target) | float64; 0 for 99.27%; smallest positive 0.00015; 3.1% of claims below 1 | fine (MET-3 noted); the two USE-5 facts below | USE-5 |
| `Row_ID` (dropped) | the file's row number; the file is sorted by household, then vehicle | no information | dropped | fine | CLEAN-3 |
| `Vehicle` (dropped) | number within the household; "may not apply to the same vehicle from year to year" | carries the same within-year composition as `household_vehicles` (its maximum equals the count in 67.5% of household-years) | dropped | fine; must stay dropped under the remedy below | CLEAN-3, LEAK-10 |

**Problems, in rank order**

**1. `household_vehicles` counts vehicles added after the rating, including replacements after the row's own crash
(P4; LEAK-10 Must, CLEAN-19 Should).** The definition calls it "known when a vehicle is rated". But a row is a vehicle
insured at any time in a calendar year, not the policy as it stood at the rating.

* The file holds partial years. Vehicles one model year ahead of the calendar year (age -1, bought in the autumn)
  claim at 0.20%, age 0 at 0.54%, ages 1-10 at 0.75-0.83%. So a household's yearly count includes vehicles that
  arrived during the year.
* A claim goes with the vehicle leaving. I followed each vehicle by (household, model year, submodel) over the
  1,390,937 households present in all three years. Among 2006 vehicles already insured in 2005, those gone by 2007 had
  claimed in 2006 at 1.40%; those that stayed, at 0.73%. At ages 1-10 the rates are 1.57% and 0.78%. The pattern fits
  a write-off followed by a replacement, or a lapse.
* The same-year count rises with the row's claim. Vehicles insured since 2005 were on the policy at the 2006 rating.
  When the household's 2006 count exceeds its 2005 count, their 2006 claim rate is 1.17%; otherwise it is 0.72%
  (one-vehicle households). For 2, 3 and 4+ vehicles: 1.03 against 0.74, 1.15 against 0.84, 1.28 against 0.93.
* The association runs through replacement. Vehicles that stay to 2007 claim at 0.82% when the household gained a
  vehicle and at 0.71% when it did not (+16%). Vehicles that leave claim at 1.39% and 1.41%: no difference.
* 9.8% of the 2006 household-years of these households have more vehicles than both 2005 and 2007: a transient extra
  vehicle.
* Model gain. Untuned LightGBM on 1,499,997 rows of whole households (10,801 claims), 3 folds by household (my
  folds, not the shipped seed), regression on log1p, the declared Gini on the amount:

  | features | fold 0 | fold 1 | fold 2 | mean |
  |---|---|---|---|---|
  | without `household_vehicles` | 0.062 | 0.062 | 0.038 | 0.054 |
  | with the previous-year count instead | 0.072 | 0.065 | 0.046 | 0.061 |
  | shipped (with `household_vehicles`) | 0.078 | 0.077 | 0.059 | 0.071 |

  The column adds 0.015 to 0.020 Gini on every fold, about a quarter of the score. Over the count known at the
  rating it still adds 0.006 to 0.013. Claim ROC AUC barely moves (-0.003 to +0.000). The builder's "0.042 against
  0.040" compared the column with `Vehicle`, which carries the same composition, so it never measured the column
  against its absence.
* What is not shown: the rows have no dates. So a car added at the renewal (a new driver's, known at the rating)
  cannot be told apart from one added mid-year, and the replacement reading is circumstantial (EV-6: "maybe a leak").
  The closest rule is LEAK-10's second clause: late values that cannot be located row by row go when they may carry a
  gain. This column carries one.
* Precedents. In pricing_game_2017's `client_n_vehicles`, the rows are the policies of a portfolio priced together,
  so the count is fixed at quote time; that fact sets it apart. african_credit_scoring's `earlier_loans` (strictly
  earlier days) and rain_in_australia (only values known by then) set the "known by then" standard of CLEAN-19.
* Remedy, mildest first (LEAK-7):
  * (a) Replace the column with the household's vehicle count in the previous calendar year: missing for 2005 rows
    and for new households, built without labels, and it keeps +0.007 of the signal.
  * (b) Drop it.

  Either way `Vehicle` stays dropped. Then update `task_summary.known` and `changes`, the bullet, and decision 4.

**2. Cat10, Cat11 and Cat12 look like random draws, not vehicle characteristics (P5; PROV-3 Must, a question for the
curator).**

* The same vehicle keeps its value from 2005 to 2006 exactly as often as random redraws would: Cat10 0.516 (random:
  0.516), Cat11 0.351 (0.351), Cat12 0.266 (0.265). Cat3 keeps its value in 100% of cases.
* A two-vehicle household's vehicles agree only at the chance rate.
* Cramér's V against every other column (calendar year, model year, make, Cat1, Cat3, Cat6, Cat8, Cat9, OrdCat,
  NVCat, Var1 deciles) and against a claim is 0.0005-0.0024. For Cat3 and Cat6 it is 0.007-0.58. Claim rates are flat
  across levels (Cat10 0.722-0.733%).
* The only structure is shared missingness: every blank of Cat12 sits on a "?" of Cat11.
* The host may have added them as decoys, or scrambled them for anonymity; nothing published says which.
* They carry no leak and no signal.
* Options:
  * (a) Drop them: the definition fix, and it loses nothing measurable. The fact that sets them apart from columns
    CLEAN-22 protects is that they are not what the dictionary says.
  * (b) Keep them as published, with a note giving these numbers.

  The curator decides. This is no reason for `No`: the other 29 features show real structure.

**3. Two facts about the target belong in the notes (P3; USE-5, no change to the task).**

* (i) The adjustment can be seen in the data. NVCat's claim rate runs from 0.53% (M, 44% of rows) to 1.33% (D). The
  mean amount per claim runs the other way, from 244 (M) to 119 (B). So the mean amount per row stays between 1.29 and
  1.95. Allstate appears to have divided each claim by a non-vehicle factor. The host's "no main effects" holds for
  the amount per row, not for the claim rate or the claim size. Suggested addition to the NVCat note: "NVCat's claim
  rate ranges from 0.53% to 1.33% and its mean claim from 244 to 119, so the mean amount per row stays at 1.29 to
  1.95: the adjustment seems to divide each claim by a non-vehicle factor."
* (ii) The rows are calendar-year records, some of them partial years (age -1: 0.20% claims). The record's
  Assessment line "Exposure: none (rows are vehicle-years)" is therefore inexact: the exposure varies and is not
  published. There is nothing to fix; a note in the target bullet would cover it.

**4. LEAK-30 wording (P4; weak, keep agreed).** Var1, Var3 and Var5 to Var8 are constants of the vehicle type. A
standardisation over a vehicle catalogue would produce the same rise in yearly means as one over all five years: the
fleet gets newer. The full-file means are -0.065 to +0.003 and the SDs 0.97 to 1.02. "Probably took in the test years"
should read "may have taken in the test years". The keep and the note stand (the Tensions row for weak LEAK-30 keeps).

**5. Missingness is cleared, and the notes can say so (P4; LEAK-38 and LEAK-10 conditional test, no problem).** For
Cat2, Cat4, Cat5 and Cat7, whether a value is missing is set by the vehicle type: it varies inside a submodel x model
year x calendar year cell for only 0.0-0.7% of rows. Among claimants, the observed missing share equals the share
their cells predict (leave-one-out): Cat2 0.355 against 0.355, Cat4 0.4017 against 0.4017, Cat5 0.402 against 0.402,
Cat7 0.5252 against 0.5251. Missingness cannot encode the outcome beyond the vehicle type. This is stronger support for
decision 3 than the random-fill test, and could replace or join it in the bullet.

**6. Small cleaning and wording fixes (P7).**

* `Model_Year`: the 2 rows with model year 2009 in calendar 2007 → missing (CLEAN-11), if they fall in the sample.
* The Dtypes bullet's "75, 1,303 and 2,740 levels" counts "?" as a level. The dictionary's counts, and the shipped
  categories, are 74, 1,302 and 2,739.

**Agreed with the definition:** dropping `Row_ID` and `Vehicle`; "?" and Cat12's blanks as missing; categories
sorted; OrdCat as a number; `Household_ID` as the group only; keeping the NV columns (LEAK-38); the LEAK-30 keep;
dropping the one exact copy and keeping the three vehicle-years that differ (not re-tested here).

</details>

<details><summary>Split audit</summary>

**Split audit (split-auditor, 2026-11-01): allstate_claim_prediction_challenge_1m**

**Verdict: right with notes.** The forced grouped split by household follows SPLIT-8 as amended and the precedents
nba_players_2016_2019 and open_university_learning_analytics_dataset. The group id is the source's own, and no hidden
group inflates a random split. One problem is measured: the pooled three-year test fold rewards a model for knowing
each calendar year's claim level, which is mostly the lighter 2007 tail (LEAK-24). A deployment that rates one year at
a time cannot use that, and neither could the competition, which scored one year at a time. The `splits_comment` also
quotes cost numbers from a different sample than the shipped one.

```text
Verdict: right with notes.
Validity: USE-10 / SPLIT-3 temporal by use case (known and new households); SPLIT-14 verified (one valid yearly
window); SPLIT-8 applied (ForcedGroupedFromTemporal), its cost measured only within one year: issue 1; SPLIT-24 holds
(Household_ID, the source's id); SPLIT-29 / SPLIT-30 hold (random rows score like grouped folds).
Procedure: EV-8 concern (splits_comment numbers from the builder's own sample, not the shipped folds): issue 2.
For the curator: issue 1, how the pooled fold should treat the year level (score within year, drop Calendar_Year, or a note).
```

All numbers below are mine unless marked. They come from the exact shipped frame and folds, which I rebuilt through
`dataset_io.from_definition`: fold sizes 999,843 / 1,000,000 / 1,000,000 train and 500,000 / 499,950 / 499,893 test,
with 3,683 / 3,652 / 3,696 test claims, as in the README and the builder's `shipped_check`. The model is untuned
LightGBM (default parameters, 2 threads), scored by the declared `normalized_gini` on the amount. I fit no tuned
models.

**Checks**

| Check | Result | Evidence |
|---|---|---|
| Regime implied by the use case | pass | Rating a vehicle when its policy year starts is a stream over years: temporal (SPLIT-6, SPLIT-7). The rated book mixes known and new households. In `test_set.csv`, 53.3% of the 2,335,027 test households are in train (58.4% of the test rows: 68.9% of the 2008 rows, 48.3% of the 2009 rows). This confirms thread 708's "1.1m are new, 1.2m are both". |
| Time column, windows | pass | `Calendar_Year` is "the year that the vehicle was insured" (data page), at year resolution only. Rows: 2005 30.53%, 2006 33.74%, 2007 35.73%. The 2006 window would train on 30.5% (below the SPLIT-14 floor); only the 2007 window (64.3%) is valid. Unlike pricing_game_2016_french_fleet, which cuts its test year into thirds by period date, this release cannot cut 2007 by time. |
| Gap against the label delay | n/a under the grouped split | The release has no dates finer than the year, so no gap can be set. The delay shows up as the 2007 tail (pure premium 1.17 against 1.51 in 2005 and 1.43 in 2006; claims above 2,000 are 0.43% of claims against 1.31% and 1.26%, at a stable claim rate). Its effect on the split is issue 1. |
| Training history | pass | Every fold's train and test sides hold all three years in the same proportions (test 30.4-30.5% / 33.7-33.8% / 35.7-35.8%). |
| Group id (SPLIT-24) | pass | `Household_ID`: "a household identification number that allows year-to-year tracking of each household" (data page). 4,309,042 households of 1 to 37 rows (mean 3.06). The sample holds 489,277 households, with no household on both sides of any fold and 163,037 to 163,092 test households per fold. |
| One prediction (SPLIT-23) | pass | One vehicle-year per row, `labels="per_sample"`: the competition scored each test row. `household_vehicles` carries what is known about the household that year. |
| Grouping context | note | `context="none"` is the safe call. Allstate's group spans years, so `all_rows`, as in pricing_game_2017_french_mtpl, whose group is one year, would expose a household's later years. The use-case reading would be `past_rows` with `time_on="Calendar_Year"` (USE-10). Since no history feature ships, it changes nothing today. |
| Hidden groups / IID (SPLIT-29) | pass | On the shipped 1.5M rows, random-row folds score 0.057 / 0.050 / 0.080 against 0.096 / 0.051 / 0.058 grouped. The group probe gives R^2 -0.009 IID against -0.008 grouped (builder). Only 4.3% of rows have their exact vehicle-and-policy profile in another year of the same household (full file). So the grouping is a use-case choice (SPLIT-4), not a measured leak. |
| Claims in `grouping` / `splits_comment` | pass, one concern | 71.3% of the 2007 households are in 2005-2006 (74.6% of the 2007 rows): pass. Test households 53% known: pass, now measured. The cost numbers are issue 2. |

**Issues, in rank order**

**1. P4, SPLIT-1 / SPLIT-8 (Should-level; the Musts hold): the pooled test fold rewards the calendar year's level,
which a one-year deployment cannot use.** SPLIT-8 asks for the cost of the forced regime "measured against the valid
windows". The builder measured it within 2007. The shipped metric, however, ranks the rows of three years together.
In the application, as in the competition (2008 for the public leaderboard, 2009 for the final ranking), every scored
row belongs to one year, so the year adds nothing to the ranking. Measured on the shipped folds:

| Predictor (shipped folds 0 / 1 / 2) | Pooled Gini (as shipped) | Mean of the within-year Ginis | Bonus from the year level |
|---|---|---|---|
| Training fold's mean amount per `Calendar_Year`, nothing else | 0.055 / 0.058 / 0.056 | 0 / 0 / 0 | all of it |
| LightGBM, log1p target (the builder's probe model) | 0.096 / 0.051 / 0.058 | 0.095 / 0.052 / 0.057 | about 0 |
| The same predictions times the training fold's level of the row's year | 0.110 / 0.066 / 0.071 | unchanged | +0.013 to +0.015 |
| LightGBM, amount (L2) | 0.079 / 0.087 / 0.073 | 0.071 / 0.075 / 0.064 | +0.008 to +0.013 |
| LightGBM, Tweedie | 0.069 / 0.071 / 0.054 | 0.061 / 0.068 / 0.046 | +0.004 to +0.009 |
| LightGBM, amount (L2), without `Calendar_Year` | 0.073 / 0.075 / 0.068 | 0.071 / 0.072 / 0.066 | +0.001 to +0.003 |
| LightGBM, Tweedie, without `Calendar_Year` | 0.070 / 0.056 / 0.040 | 0.068 / 0.055 / 0.039 | +0.001 to +0.002 |

A predictor that knows only the year scores what the probe model scores on two of the three folds. Any model that gets
the year's level right gains 0.004 to 0.015 in every fold. The bonus has the same sign on every fold and comes from
paired comparisons on the same test rows, so it is not noise, even though each Gini has a bootstrap SE of about 0.02.
A log1p model happens to miss the level, but the benchmark's tuned methods and models trained on the amount will not.
The level is mostly 2007's: pure premium 1.17 against 1.51 and 1.43. The model learns it from other households' rows
of the same year, an outcome-level fact about the test year that a model rating next year would not have. Decision 2
says "Kept: every fold holds 2007, and `Calendar_Year` is a feature". That presents as the mitigation what is in fact
the mechanism. Dropping `Calendar_Year` costs nothing within a year (log1p 0.096 / 0.049 / 0.057 against 0.095 /
0.052 / 0.057). The year is only weakly visible from the other features: 2007 against earlier years scores ROC AUC
0.58, through the Var drift of LEAK-30.

Remedies, mildest that resolves first:
* (a) Score within the year: the normalized Gini per `Calendar_Year`, averaged with row weights, with `Calendar_Year`
  as a scoring column (so also no feature). This mirrors the competition's one-year scoring and removes the residual
  too. It needs a per-group Gini in `data_foundry.v2.metrics` (MET-13), so it touches the metric declaration and the
  metric auditor's lane.
* (b) Drop `Calendar_Year` from the features. Cheaper, with no metric change; it removes most of the bonus (+0.001 to
  +0.003 remains) and costs nothing measurable within a year.
* (c) At least say it in `splits_comment` and fix decision 2's wording: the pooled fold rewards the year level by
  about +0.01 for models that learn it, and a year-only predictor scores 0.055 to 0.058.
* Dropping 2007, the LEAK-24 alternative, would shrink the level to the 5% gap between 2005 and 2006. That is a
  bigger change, owned by the leak and target reviewers.

**2. EV-8 (Should): the cost numbers in `splits_comment` come from the builder's own sample, not the shipped folds.**
"folds by household scored 0.069 to 0.094 on their 2007 rows and 0.021 to 0.073 on all their rows" and "folds of
random rows scored 0.050 to 0.056 on the same 1.5M rows" come from `experiment1.py`. That script drew its own 1.5M
rows of households (490,287) and used sklearn `GroupKFold` without shuffling. On the shipped folds the same model
scores:
* grouped folds: 0.051 to 0.096 on all rows (the curation comments already quote this) and 0.059 to 0.115 on their
  2007 rows;
* random-row folds: 0.050 to 0.080;
* temporal window on the same 1.5M rows (train on the 2005-2006 rows, 963,383 or 64.2%; score the 536,617 rows of
  2007): 0.063 overall, 0.056 on known households (74.7%) and 0.077 on new ones, and 0.099 / 0.063 / 0.026 over the
  three household thirds of 2007.

On the shipped rows the temporal window scores about 0.02 below the grouped folds' 2007 rows (one SE). The builder's
full-file run went slightly the other way (0.084 against 0.069 to 0.094). So "costs little" holds only as "no cost
measurable at this noise". SPLIT-21 bars reading more into it. Remedy: restate the sentence with the shipped-fold
numbers and that reading. Optionally reword "The grouping stands for the time order, not for rows that resemble their
household" as "The grouping keeps a household's other years out of training; random-row folds score alike, so it
guards the time order rather than a measured gain from look-alike rows".

**3. Note (USE-10, SPLIT-13; covered by `fit="approximate"`): the forced grouping tests only new households, and the
household's claim history is lost.** Of the rated households, 53% are known (above). Their history carries signal.
In 2007, vehicle-years of households with a 2005-2006 claim claim at 1.44%, those without one at 0.77%, and new
households at 0.53% (full file, 76,286 / 3,436,983 / 1,197,619 rows). The record calls that history fair under a
temporal split. The forced grouped split cannot use it, and no history feature ships, so nothing leaks. The cost
belongs in the stand-in that `fit_reason` already names. No change needed; listed so the curator sees what the forced
regime gives up.

**4. Housekeeping: the record disagrees with the definition** (builder's issue 10). The record has `required_split:
Temporal (NON-IID)` and the tag `Non-IID (Temporal)`, while the definition ships grouped, tagged
`ForcedGroupedFromTemporal`. The main session's sync should bring the record in line.

**Alternative split, considered and not recommended under the rules as written.** A single temporal window: train on
2005-2006 (64%), score 2007 cut into three household thirds. It mirrors the competition, scores one year (no year
bonus) and has 75% known households (the real test had 53-58%). But it scores against the less mature 2007 claims,
and one window cut three ways does not meet SPLIT-14's three windows (a Must). Choosing it would need an amendment
(the builder's draft issue 2), not an exception. Remedy (a) or (b) of issue 1 fixes the main distortion without one.

</details>

<details><summary>Domain practitioner</summary>

**Role:** domain practitioner. I am a personal-auto pricing actuary setting the vehicle part of the bodily-injury (BI) liability tariff: how much more or less a given make, model, submodel and model year costs in BI claims than the average vehicle, once the driver, territory and policy factors are held fixed. This is the job ISO's liability symbols do for the industry, and carriers do it in house. The symbols are assigned from the series' own loss experience plus a predicted relativity from vehicle attributes such as curb weight and chassis type, so that new and thin series get a rate (Verisk FAQ and product pages).

**Verdict: fit approximate (agree with `fit="approximate"`).** The target ("adjusted to control for known non-vehicle effects", data page) is close to what I fit a vehicle factor to: the residual of the rest of the tariff. The features are attributes I have when I rate. But I cannot check the adjustment or the exposure, and the shipped test rows are mostly vehicle types the model has already seen. My hardest case, a series with little or no experience, is not tested. Metric: **partly**. The normalized Gini scores the ranking half of my decision, and actuaries really use it for that (Frees, Meyers and Cummings 2011). It does not score the level of the relativities. Keep it (MET-4) and add Tweedie deviance as a context metric.

**1. Do I have these inputs at the prediction point? (USE-3, USE-6)**
- I have: `Calendar_Year`, `Model_Year`, the make/model/submodel codes, Var1-8, Cat1-12, OrdCat (all vehicle attributes, VIN-decodable), and NVCat/NVVar1-4 (policy attributes, known at renewal). The LEAK-30 standardisation over the test years is a harmless shift and scale for me.
- `household_vehicles`: I know the vehicles on the policy at inception, not the count over the calendar year. The claim-auditor shows that the count includes vehicles added after inception and replacement cars (pattern 1,2,1: 0.98% claim rate against 0.71%). In practice I would rate on the vehicles listed at the term start. This is a small look-ahead (LEAK-10). I agree with the claim-auditor that it is worth a question to the curator.
- Missing values: I would never price a row with a missing vehicle attribute. Allstate says "when the model is applied, all of the features will be collected" (thread 826) and removed such rows from its test file. In the shipped test folds, 71.7% of rows have one, so the test is not what I face (see gap 3).
- Missing although I always have it: (a) **earned exposure**. Every pricing dataset I have used carries the car-years each record was insured. Here a row is "one year's worth information" (data page), but nothing says whether a car added in October contributes a full year. Under a Poisson/Tweedie GLM, an unweighted row overstates the risk of part-year cars. (b) The non-vehicle rating factors (driver age, territory, prior claims). They are deliberately absorbed by the adjustment, which is consistent with a vehicle-factor task, so this is not a gap for this use case. (c) The household's own prior claims. They are available (households recur), but they are a driver factor, never a vehicle factor, so leaving them out is right for this use case (USE-10: for vehicle rating, the entity that matters is the vehicle type, not the household).

**2. Is the target what I act on? (USE-5)**
Mostly yes. A vehicle factor is fitted to losses after the other rating factors are offset, and "adjusted to control for known non-vehicle effects" reads like exactly that (the 0.00015 to 11,440 range in thread 928 fits a loss divided by a non-vehicle relativity). The method is undisclosed, so USE-5's "approximate with a note" applies, as the definition says. What I want predicted is a number, the expected loss cost per car-year (a pure premium). I do not want a class. The log1p shipping is a modelling convenience. The ranking metric is invariant to it (MET-3 is handled correctly). One real-world nuance confirms LEAK-24: BI claims take years to settle. An actuary develops each accident year to ultimate before fitting. The lighter 2007 tail (0.43% of claims above 2,000, against 1.31% and 1.26%) is what an immature year looks like. Keeping `Calendar_Year` as a feature is what I would do with undeveloped data. I would not drop 2007.

**3. Does one row match one decision, and is the test data what I would face? (USE-8, USE-10)**
One row is one vehicle-year. That is the experience record I fit on, and each vehicle's premium is set per vehicle per term, so the unit matches. The test set does not match what I face. Next year's book differs from a held-out household of the same years in three ways:
- New and thin vehicle series. Probe of mine on the shipped folds: only 0.07% to 0.10% of test rows have a Blind_Model or Blind_Submodel absent from the fold's training side. In real practice, every model year brings new series, and a symbol must be given before any experience exists (Verisk: a predicted relativity from attributes). Same rows, folds grouped by Blind_Model (every test submodel unseen), untuned LightGBM, normalized Gini on the amount:

| split | all features | without model/submodel codes |
|---|---|---|
| shipped household folds (per fold) | 0.096 / 0.051 / 0.058 | 0.133 / 0.065 / 0.089 |
| shipped, pooled | 0.068 | 0.094 |
| grouped by Blind_Model (per fold) | 0.014 / 0.037 / 0.013 | 0.047 / 0.117 / 0.091 |
| grouped by Blind_Model, pooled | 0.007 | 0.085 |

  Two readings. (a) The signal is in the vehicle attributes, and it carries over to unseen series (0.085), which is what a symbol model needs. (b) The raw 1,303- and 2,740-level codes hurt an untuned model even on the shipped folds (0.068 against 0.094). An actuary would credibility-weight them, never feed them raw. This makes the dataset a fair test of high-cardinality categorical handling, but the shipped split does not show how a model behaves on a new series.
- Next calendar year. Discussed in the splits_comment (SPLIT-8, ForcedGroupedFromTemporal). I accept the reasoning. The one valid window (2005-06 to 2007) scored 0.084, close to the grouped folds.
- Complete rows only at application (thread 826).
- Caution on the previous scratch work: the competition's 2008-09 test file has 26% of rows with a Blind_Model absent from train. This is **not** new vehicles. 14.8% of test rows are model years 2004 or earlier with such a code, and within a make the big codes swap (make AO: AO.7, 169k train rows, is absent from test; AO.2, 277k test rows, is absent from train). So the model codes were blinded separately in the two files. This does not affect the shipped data (train file only), but the Kaggle 0.20 is not a like-for-like reference.

**4. Would I use this model?**
As a benchmark of vehicle-factor modelling, yes. As a production tariff, no. I would distrust: the undisclosed adjustment and the missing exposure; a Gini of 0.05 to 0.10 with a bootstrap SE of about 0.02 per fold (on 3 folds, two models must differ by about 0.03 before I believe one is better: MET-10); and the immature 2007. I would trust it more if the score held on unseen series (the by-model row above) and if the relativities were stable across years.

**5. Does the metric score my decision? (MET-1, MET-4, MET-8)** Partly.
- What fits: Allstate's competition metric (MET-4), at the unit I act on (the vehicle-year, MET-2). An ordered Lorenz curve / Gini is the standard way actuaries compare rating scores (Frees, Meyers and Cummings 2011, JASA 106:1085). With an undisclosed currency scale, only the ordering and the relative sizes are usable anyway. RMSE on the amount, the fallback (MET-8), would be dominated by the zeros and the 11,440 tail and would rank models worse for my purpose.
- What it misses: the Gini ignores the level and spread of the predictions. A vehicle factor that ranks right but is 2x too steep scores the same. Also, Kaggle's version weights each row 1 instead of by exposure (exposure is not available anyway).
- What I would choose: keep `normalized_gini` as the declared metric. If a second, context metric is allowed, I would add the **Tweedie deviance** (power about 1.5, log link) on the amount. It is strictly consistent for the mean of a zero-inflated, right-skewed loss cost, it is how GLM/GBM pricing models are fitted and compared, and it scores the relativity level the Gini ignores. A hard-decision metric does not apply: I set a continuous factor, with no threshold or k (MET-6, MET-7, MET-9 do not apply).

**Gaps between the dataset and the real decision, ranked by how much they change the task**
1. The test rows are seen vehicle types. My hard case, a new or thin series, is untested (probe above: Gini 0.007 with the codes, 0.085 without, when the series is unseen). This is a known gap, not a defect. Name it in `fit_reason` or a note (USE-8).
2. No exposure column, and no statement that each row is a full car-year (USE-5). Name it in the notes.
3. The test folds hold rows with missing values that never occur at application (thread 826; 71.7% of rows). Already discussed, and the builder's measurement (random fill costs nothing) makes it minor.
4. The undisclosed non-vehicle adjustment (USE-5). Already in `fit_reason`.
5. The immature 2007 losses (LEAK-24). Kept with `Calendar_Year`, as an actuary would do with undeveloped data.
6. `household_vehicles` counts the whole calendar year, not the policy at inception (LEAK-10, the claim-auditor's point).

**What an expert would change**
- Add a note that no exposure is given and that rows may be part-year (USE-5).
- Add to `fit_reason` that the household split tests vehicle types seen in training, while a vehicle rating must also price new series. Optionally report the by-model numbers as a context probe. I would not change the split: P4 and the use case's temporal reading come first, and a by-model split would be a different task.
- Either redefine `household_vehicles` as the count in the previous year or at the household's first row of the year (not possible from the data: there are no dates within a year), or drop it, since it scores alike with `Vehicle` (0.042 against 0.040) and with versus without it differs by -0.008 to +0.019.
- Optionally declare Tweedie deviance as a context metric next to the Gini.

**Sources**
- Kaggle competition pages (Description, Data, Evaluation) and forum threads 826, 928, 708, 973, as saved in the run.
- Huangfu (2015), WPI MSc report, p. 6 and p. 30.
- Frees, Meyers & Cummings (2011), "Summarizing Insurance Scores Using a Gini Index", JASA 106:1085-1098, doi:10.1198/jasa.2011.tm10506 (abstract via https://academicnewsletter.sufe.edu.cn/info/445125; cplm `gini` docs https://rdrr.io/cran/cplm/man/gini.html).
- Verisk/ISO on liability symbols from loss experience plus attribute-based predicted relativity: https://www.verisk.com/insurance/about/faq/iso-s-symbols-for-individual-makes-and-models-of-cars/, https://www.verisk.com/products/iso-symbols/, https://verisk.com/company/newsroom/iso-risk-analyzer-expands-its-personal-auto-offering-with-new-tool-for-determining-vehicle-liability-risk; Insurance Journal 2004 on separate BI/PD liability symbols: https://amp.insurancejournal.com/news/national/2004/04/01/40773.htm.
- Panel cross-reference: `claim-auditor.md` (household_vehicles look-ahead, 55.9% copy share).

</details>

<details><summary>Blind review</summary>

**Dataset:** Allstate Claim Prediction Challenge (Kaggle 2011), prepared as a regression on `log1p_claim_amount`. The full table has 1.5M rows; I worked from the 300k-row sample. The split is 3-fold, grouped by `Household_ID`.

**Verdict:** Exclude as prepared. The data are real, the split is honest and the claim rate is preserved. But the target as framed (log1p of a disguised bodily-injury claim amount, 99.27% zeros, scored as regression) carries almost no learnable signal. A benchmark score would mostly measure how well each method shrinks toward the mean. A reframed version could be reconsidered: claim yes/no or a Tweedie/Gini metric, all 1.5M rows, a 2005-06 to 2007 temporal split.

**What the task is**

Allstate posted the data so that people would "predict Bodily Injury Liability Insurance claim payments based on the characteristics of the insured's vehicle" (Kaggle competition text, quoted by KDnuggets, July 2011). Each row is one insured vehicle in one calendar year (2005-2007). The features are blinded vehicle attributes (make, model, submodel, Cat1-12, Var1-8, OrdCat) plus a few policy attributes (NVCat, NVVar1-4). This is a real use: an insurer pricing or relativity-setting by vehicle at renewal. Two caveats: the claim amount "has been adjusted to disguise its actual value" (Huangfu, WPI MS report 2015, p.5), and the drivers' own risk factors are deliberately absent.

**Concerns, ranked**

1. **Almost no signal for the target as framed (most serious).**
   - Evidence: 2,181 of 300,000 rows are nonzero (0.727%). The source reports 0.73% (95,605 of 13,184,290), so the sample is faithful.
   - Evidence: with household-grouped 3-fold CV on the sample, a default-ish LightGBM with early stopping stops after 1-8 trees. Its mean R² is -0.00004, with RMSE 0.35997 against 0.35998 for predicting the training mean.
   - Evidence: a heavily regularized LightGBM (7 leaves, min_child_samples=1000) reaches R² of 0.00022, 0.00047 and 0.00017 per fold. On fold 0 the MSE gain over the constant is 3.7e-5, with a household-bootstrap SE of 2.4e-5, so the gain is about 1.5 SE.
   - Evidence: the learning curve rises slowly. Training on 50k, 100k and 200k rows gives R² of -0.00045, -0.00009 and +0.00022, and AUC of 0.545, 0.562 and 0.575. On the full 1.5M I would expect R² on the order of 1e-3, not more.
   - Evidence: there is no severity signal. Predicting log amount among claimants gives R² of -0.015 (n=2,181).
   - Evidence: the source agrees. "none of the covariates is even modestly correlated with the response" (WPI p.8). Allstate's own internal benchmark had a normalized Gini of 0.059 (WPI p.24).
   - Why it matters: method rankings on log1p-RMSE would be decided at the 4th-5th decimal, mostly by regularization toward a constant. Fold-to-fold variation (R² 0.00017-0.00047) is as large as the effect being measured. With only 1 repeat x 3 folds this is noise.
   - Change: do not use log1p-RMSE regression. If the dataset is kept, use binary claim occurrence scored with AUC or log-loss. On the sample, AUC is about 0.58-0.60 (classifier folds 0.582, 0.597, 0.595). At 1.5M rows each test fold has about 3.6k positives, so the AUC SE is about 0.005 and differences of 0.01-0.02 are resolvable. The alternative is Tweedie deviance on the raw amount, the insurance-standard loss. Raw-amount normalized Gini (the competition metric) is very unstable at this size: -0.04 to 0.13 across folds on the sample. Use all 1.5M rows and more repeats.

2. **The split does not match the deployment direction.**
   - Evidence: the competition trained on 2005-2007 and scored on later years ("training (from 2005-2007) and test data (2008-9)"). The WPI author used 2005-06 for training and 2007 for testing.
   - Evidence: the household-grouped random split mixes years, so models learn from 2007 to predict 2005.
   - Evidence: claim frequency is stable by year (0.70%, 0.74%, 0.74%), but severity drifts. In the sample the mean raw nonzero claim is 192, 235 and 161 for 2005-2007; the source reports 201 for 2005-06 against 163 for 2007 (WPI Tables 5.7-5.8).
   - Evidence: a temporal split on the sample gave nearly the same R² (0.00026) and AUC (0.574), so this is not a leak that inflates scores. It is a fidelity issue.
   - Change: train on 2005-2006 and test on 2007, keeping household grouping or at least no household overlap. A grouped split alone is acceptable if a temporal one cannot be run.

3. **Target construction is partly arbitrary.**
   - Evidence: the amount is a disguised transform of dollars (WPI p.5). The smallest nonzero claim is 0.0028, 1% of claims are below 0.33 and 5% are below 1.8.
   - Evidence: log1p depends on scale, so these tiny claims sit almost on top of zero, while the largest claims go up to log1p 9.05 (8,507 units).
   - Why it matters: an unknown rescaling makes "log1p" an arbitrary choice of compression.
   - Change: use a scale-free framing (binary target, or a Tweedie/Gini metric on raw amounts), or document that log1p is applied to disguised units.

4. **An engineered column (`household_vehicles`) is undocumented.**
   - Evidence: it is not in the source (the source has `Vehicle`, a within-household index, which was dropped). It is constant within household-year in all 271,712 household-years in the sample.
   - Evidence: the sampled row counts are consistent with it being the full count of vehicles in that household-year. P(2 sampled rows | value=2) is 0.111, which implies 20% row sampling of complete household-years. So it was not computed on the 300k sample.
   - Evidence: it is legitimate at prediction time (the policy's vehicle count is known at renewal) and mildly informative (claim rate 0.69% at 1 vehicle, 0.92% at 5).
   - Change: document how it was derived and on which table.

5. **The ID column sits in the table.**
   - Evidence: `Household_ID` is int64 and is the grouping key. On its own it gives AUC 0.487, so it is near-harmless, but it is an arbitrary identifier.
   - Change: make sure the harness drops it from the feature set.

6. **Duplicates are expected and handled.**
   - Evidence: there are 20 exact duplicate rows, all within the same household and year (presumably two identical vehicles). 1,890 rows match another row of the same household on every column except year: the same vehicle in another year.
   - Evidence: the household-grouped split keeps all of these on one side, so there is no train/test copy leakage.
   - Evidence: 63,357 rows share the full feature vector with a row from another household. These are distinct policies with the same car configuration, not leakage, but they show that the features mostly identify a car model rather than a risk.
   - Evidence: claims cluster slightly within household-year: 4 household-years with 2 or more claims among 26,155 multi-row household-years, against about 1.5 expected under independence. Grouping handles this.

**Checks that passed**

- **Real data:** feature means match the source's 13.2M-row summary. For example, Var1 mean is -0.0076 against -0.0101, Var8 -0.0596 against -0.0586, and NVVar1-4 minimums are identical (-0.2315, -0.2661, -0.2723, -0.2514).
- **Missingness matches the source:** Cat2 37.0% (the source table shows 4,874,164 rows, about 37%), Cat4 and Cat5 42.6% against 42.7%, Cat7 54.2% against 54.4%, and Blind_Make 0.07% against 0.064%.
- **Column types are sensible:** the "?" missing code has become NaN, categoricals are typed as category, and OrdCat is a 1-7 ordinal stored as float.
- **High-cardinality columns:** Blind_Model and Blind_Submodel have 1,118 and 2,305 levels in the sample. They are legitimate but invite overfitting: unregularized LightGBM put 71% of its gain on Blind_Model and still did worse than the constant.
- **No post-outcome columns:** all features are vehicle or policy attributes known at underwriting. Model_Year goes up to 2008 for calendar year 2007, which is plausible.

**What I could not check**

- I could not read the Kaggle pages: they need JavaScript or a login, so the official data dictionary and leaderboard were unavailable. I relied on the WPI report and press quotes. The winning normalized Gini is not quoted here.
- I did not have the full 1.5M prepared rows or the original 13.2M, so the signal at full size is extrapolated from a learning curve.
- The nature of the amount-disguising transform is unknown.
- I could not see whether each row is a full policy year. There is no exposure column, and partial-year exposure would confound frequency.
- I could not confirm how the 1.5M rows were drawn from the 13.2M (inferred: whole household-years, unenriched).


**Sources**

- Kaggle competition page: https://www.kaggle.com/competitions/ClaimPredictionChallenge (could not be read)
- D. Huangfu, "Data Mining for Car Insurance Claims Prediction", WPI MS project report, 2015: https://digital.wpi.edu/downloads/zs25x859f
- KDnuggets, "Kaggle: Claim Prediction Challenge", July 2011: https://www.kdnuggets.com/2011/07/kaggle-claim-prediction-challenge.html
- KDnuggets, "Allstate claim prediction challenge insights", October 2011: https://www.kdnuggets.com/2011/10/allstate-claim-prediction-challenge-insights.html

</details>

<details><summary>Precedent check</summary>

**Precedent checker (AI, 2026-11-01): allstate_claim_prediction_challenge_1m**

**Verdict:** most choices follow their precedents. Three do not: 2007 is kept against LEAK-24's remedy, `OrdCat` is typed as a number unlike two insurance siblings, and `household_vehicles` rests on a precedent whose key fact differs. Two choices are open questions for the whole insurance family and should be decided together with the siblings: the forced grouped split (against how_much_did_it_rain) and the log1p scale (australian issue 5). None of the register's 14 flags is about this dataset. Flags 11-14 ("exception to SPLIT-14") are false positives: those are SPLIT-10 exceptions that serve SPLIT-14.

Precedent status: every insurance sibling of this run (liberty_mutual_fire_peril_loss_cost, pricing_game_2017_french_mtpl, frempl, both Spanish tables, australian, wisconsin, pricing_game_2016) is an AI draft. The curator has given only the `Yes` (CC 2026-10-30, Andrej) and policy call 3 ("judgement calls based on the references for each dataset", no family convention). Where a pair below is two AI drafts, the point is to align them before the curator reads them, not that a curator decision was crossed.

**Per decision**

1. **1M subsample of whole households, drawn at random, not stratified.** Consistent. It follows sepsis_prediction_1m (2026-10-01), amex_non_iid_1m and fraud_detection_in_electricity_and_gas_consumption_1m: grouped folds over 1.5M rows, with a few hundred rows trimmed when whole groups overshoot the 500k test cap. One gap in form: those three record the `splits_rows_never_tested` acceptance in the definition (`accepted_check_warnings`, for example sepsis_prediction_1m's `dataset.py`). This definition only proposes it. Add the dict once the warnings are accepted.

2. **Grouped by household, `ForcedGroupedFromTemporal`.**
   - SPLIT-8 as amended (Lennart, 2026-10-21: "too few periods ... stacked and grouped") covers this as written. The closest curator case is open_university_learning_analytics_dataset (Lennart, 2026-10-21): one valid window, cost measured against it. nba_players_2016_2019 was retired on its use case, not its split.
   - The closest sibling is spanish_motor_insurance_coverage_level_2022_2024. The facts are nearly the same: three calendar years, one valid window (its 2023 window trains on 19% of rows, here the 2006 window on 30.5%), whole entities held out, the window's cost measured.
   - It differs from wisconsin_local_government_property_insurance_fund, which has two valid windows. So wisconsin's proposed SPLIT-14 amendment ("exactly two windows, both at least 50%, ship those") would not reach this dataset; it would stay under SPLIT-8.
   - Against: Andrej's how_much_did_it_rain call (CC 2026-10-30: "if the data is temporal but a temporal split is not possible, we cannot split the data and reject it"; "Forced IID is to be avoided at all costs"). Also, the record's notes, on which the `Yes` was given, say "Split temporal by `Calendar_Year`". Builder issue 10 covers the record mismatch.
   - Status: departs from the curator's latest statement, with facts that may set it apart: a grouped split rather than random rows; how_much_did_it_rain's leak (hours of one storm on both sides) is absent here because households never straddle the split; the one valid window is measured (Gini 0.084, against 0.069-0.094 on the grouped folds' 2007 rows).
   - Decide together with frempl issue 5, australian issue 1, spanish 2022-2024 issue 1 and wisconsin issue 1.

   ```text
   **Consistency check (AI, 2026-11-01):** shipping allstate as a forced grouped split (SPLIT-8, the open_university
   case) differs from how_much_did_it_rain (`No`, 2026-10-30, Andrej: "if the data is temporal but a temporal split is
   not possible ... reject it"). What sets allstate apart?
   (a) households are held out whole, so no unit shares outcomes across the split (how_much_did_it_rain's leak), and the
   one valid window (train 2005-06, test 2007) is measured and scores no lower than the grouped folds' 2007 rows,
   recorded as the fact under SPLIT-8, decided with spanish_motor_insurance_coverage_level_2022_2024 issue 1;
   (b) treat it like how_much_did_it_rain (`No`, and spanish 2022-2024 follows);
   (c) reopen how_much_did_it_rain under SPLIT-8 as written;
   (d) amend SPLIT-8 or SPLIT-14 (for example, allow a single valid window; wisconsin's two-window wording would not
   cover allstate).
   ```

3. **2007 kept despite the lighter tail (LEAK-24, Must).** Departs. The stated reason is a mitigation, not a fact that sets the case apart. If LEAK-24 is triggered, keeping 2007 is not reasonable under the ranking.
   - LEAK-24 (leak_checks.md line 157): "A target right-censored in the newest periods ... is cut where follow-up is complete". Cases: sf_permit_time (cut to permits filed before 2024) and consumer_complaints (re-sourced from an archive).
   - The reason given ("every fold holds 2007, and `Calendar_Year` is a feature") serves no higher-ranked Must. The split auditor reads it as the very mechanism by which models learn the 2007 level.
   - Sibling contrast:
     - spanish 2022-2024 measured its newest year as mature (0.302 / 0.305 / 0.312 claims per year on risk), so LEAK-24 was not triggered there.
     - frempl issue 3 kept amounts of unknown valuation date because the evidence was circumstantial within one year and fit another explanation (contracts ended by the claim).
     - Here the evidence is measured across years and holds within every vehicle-age band and each of the three largest makes: claims above 2,000 are 0.43% of 2007 claims against 1.31% and 1.26% in the earlier years. That is stronger than frempl's.
   - One counter-fact the notes do not state: 2005 and 2006 hardly differ (1.31 against 1.26). Development would usually show a gradient over the years; a step at 2007 fits a change in Allstate's adjustment as well. This is the best candidate for a distinguishing fact.
   - The remedy is cheap: without 2007, 8.5M rows remain against a 1.5M budget.

   ```text
   **Consistency check (AI, 2026-11-01):** keeping 2007 departs from LEAK-24's remedy (sf_permit_time: cut where
   follow-up is complete) on a measured lighter tail at a stable claim rate and median. What sets allstate apart?
   (a) the tail drops as a step at 2007 with no 2005-to-2006 gradient, so censoring is not shown (an adjustment change is
   as likely); recorded as "LEAK-24 not shown violated", as recommended for frempl issue 3;
   (b) treat it like sf_permit_time: drop 2007 (8.5M rows remain, still above the budget);
   (c) reopen frempl issue 3 to match whichever reading is chosen here;
   (d) amend LEAK-24 to say what evidence of an unmatured amount target (no valuation date) triggers it.
   ```

4. **log1p target, scored by the competition's `normalized_gini` on the amount.**
   - The metric is consistent: MET-4 (a competition's metric), policy call 3's table (`allstate_claim_prediction_challenge`: "normalized Gini (source)", 2026-10-30), the same metric name as the context-Gini siblings, and liberty's weighted form from its own competition. With no exposure column, frempl issue 4's weighted alternative does not arise here; this is the row Gini the family borrows.
   - The target scale departs with a stated reason ("raw not consistently better"). It follows frempl, both Spanish tables and CLEAN-16's default.
   - It does not follow pricing_game_2017_french_mtpl's reasoning: "a small edge, so the estimand decides", hence the raw amount. On that test this dataset's own probes lean raw:
     - shipped folds: raw 0.079 / 0.087 / 0.073 against log1p 0.096 / 0.051 / 0.058 (raw ahead on 2 of 3, mean +0.011);
     - builder's experiment folds: raw ahead on 3 of 3 (+0.029, paired SE about 0.02);
     - only the 2007 window favours log1p (+0.010, 2 of 3).
   - australian issue 5 already asks for one call for the Gini-scored tables and lists this dataset. Decide it there; no separate mark is needed here.
   - Third-exception watch: if the curator picks dollars, australian, pricing_game_2017 and wisconsin (already written as an exception to CLEAN-16) would make three departures from CLEAN-16 on claim costs. Amend CLEAN-16 then, rather than recording three exceptions.

5. **Missing values kept, `?` and Cat12 blanks set to missing.** Consistent.
   - It follows CLEAN-10 (proxy codes to missing), CLEAN-11 (rows stay) and liberty's identical choice (level `Z` set to missing, rows kept).
   - The LEAK-10 mechanism of kick and expresso (drop a field whose missingness differs by outcome while the host's test file carries it the same way) does not match: here the host removed such records from its test file. The builder measured the missingness indicators alone at a Gini of -0.015, -0.016 and 0.054, about what the years alone give.
   - The source's request (thread 826) is recorded in the notes, as the 2026-10-30 assessment asked.

6. **`household_vehicles` added (cites pricing_game_2017's `client_n_vehicles`, CLEAN-3).** Departs from the cited precedent on the fact that matters: when the count is known.
   - pricing_game_2017 counts the 100,000 policies of one start-of-year underwriting file: whole policy-years, the same policies in every year's file, so the count is known when the premium is set.
   - Here the count runs over a calendar-year file. The column auditor finds that file holds vehicles added during the year, replacements after the row's own crash among them.
   - So the precedent does not carry the claim "known when a vehicle is rated". LEAK-10 (Must) decides. The remedies already used are a drop (kick, 2026-10-22; 2_month_survival_rate_prediction, Lennart 2026-10-26: fields measured to differ by outcome) and LEAK-11's keep with a note (a late value that weakens the signal).

   ```text
   **Consistency check (AI, 2026-11-01):** `household_vehicles` is justified by pricing_game_2017's `client_n_vehicles`,
   but that count comes from a start-of-year policy file and this one from a calendar-year file that includes vehicles
   added after the rating. What sets it apart?
   (a) a count of the vehicles in force at the year's start (a vehicle's first appearance in an earlier year, or the
   household's vehicles also present the year before) restores pricing_game_2017's timing, recorded as the fix;
   (b) treat it like kick: drop the count (Vehicle stays dropped; the builder measured no loss, 0.042 against 0.040);
   (c) keep it under LEAK-11 with a `Potential leak, kept on purpose:` note, if the leak is shown to weaken the signal;
   (d) amend CLEAN-19 or LEAK-10 for household counts built from period files.
   ```

7. **`OrdCat` shipped as a number.** Departs from two siblings in this run, with a reason ("so the order stays") that holds for them too.
   - liberty types its ordinal codes `var1`, `var3`, `var7` and `var8` (digits 1-5 and 1-6, the data page's "ordinal", missing level `Z`) as categorical.
   - pricing_game_2017 keeps `pol_coverage`, "ordered Mini to Maxi in the rules", as a category.
   - CLEAN-14 as amended (Lennart, 2026-10-21) makes a fixed, finite set categorical "if we know from the context they are indeed such". The source calls `OrdCat` an "ordered categorical vehicle variable" (1-7).
   - Elsewhere in the working copy the practice is split: ames_housing's text-coded ordinals are categorical; homesite_quote_conversion keeps ordinals numeric, following TabRed; wids_diabetes_mellitus keeps medical scales as integers.
   - The data give no order in risk: claim rates by level are 0.35, 0.81, 0.60, 0.71, 0.64, 0.58 and 0.26%.
   - All three are AI drafts. Align them, or ask once.

   ```text
   **Consistency check (AI, 2026-11-01):** `OrdCat` (the source's "ordered categorical", 1-7) ships as a number, while
   liberty_mutual_fire_peril_loss_cost's ordinal codes (var1, var3, var7, var8, digits) and pricing_game_2017's
   `pol_coverage` ship as categories. What sets OrdCat apart?
   (a) none found that liberty lacks (the AI's best guess, a stated order, holds for both); so retype OrdCat as
   categorical (one line in `_feature_types`);
   (b) keep it numeric and retype liberty's four ordinals as numbers;
   (c) keep both as they are, with the difference recorded as a per-dataset call;
   (d) amend CLEAN-14 to say how a source-stated ordinal coded by digits is typed (the working copy is split:
   ames_housing categorical, homesite_quote_conversion numeric).
   ```

8. **`Row_ID` and `Vehicle` dropped.** Consistent with CLEAN-3 and with pricing_game_2017, which drops `id_vehicle` ("their rank should not represent anything valuable").

9. **LEAK-30 kept with a note (yearly means of the standardised columns).** Consistent with the Tensions row (Lennart, 2026-10-19: scaling over all rows kept with a `Potential leak, kept on purpose:` note) and liberty's identical note.

10. **One exact copy dropped; feature-equal rows of other households kept (LEAK-18).** Consistent with LEAK-16 to LEAK-21 (a row copy leaves) and liberty, which keeps feature-equal rows of distinct risks.

11. **`Calendar_Year` kept as a feature under the grouped split.** Consistent with spanish 2022-2024 ("The year stays a feature"). Whether it should stay while 2007 differs is the LEAK-24 question in decision 3, not a precedent question.

12. **Record fields (`required_split: Temporal`, tag `Non-IID (Temporal)`).** Same pattern as wisconsin, spanish 2022-2024 and frempl: they follow the answer to decision 2's prompt.

**Drift and amendments due:**
- No drift of one curator yet. Andrej's how_much_did_it_rain statement (2026-10-30) is the first SPLIT-8 call by him, and it differs from Lennart's SPLIT-8 amendment (2026-10-21). The five forced splits of this run will settle whether this is a rule change.
- No third exception of one kind comes from this dataset. CLEAN-16 becomes due if dollars are chosen in australian issue 5. SPLIT-10 is already flagged in the register (5 datasets) and is untouched here.

</details>

<details><summary>Advocate</summary>

**Advocate, opening brief (AI, 2026-11-01): allstate_claim_prediction_challenge_1m**

**Position: ship after changes.** Every real problem the panel found has a fix in the definition, and none of those fixes costs the task. The changes I accept: drop `Calendar_Year` as a feature (or drop 2007), replace or drop `household_vehicles`, drop or note Cat10-Cat12, and correct the number slips. The one open question is the family's forced-split call. On that call the facts here are the most favourable of the five open cases.

**1. A real task, a curator `Yes`, and the source's own metric at the unit of the decision (P3, P6; USE-1, MET-4 Should, MET-2 Must).**
- Evidence: CC 2026-10-30 (Andrej): `Yes`, priority 2. The domain practitioner (a BI pricing actuary) agrees with `fit="approximate"`. One row is the vehicle-year he rates, and the target is "close to what I fit a vehicle factor to: the residual of the rest of the tariff". The normalized Gini is Allstate's leaderboard metric. It is also the actuaries' standard way to compare rating scores (Frees, Meyers and Cummings 2011, JASA 106:1085). The library equals Kaggle's reference code to 4 decimals on all 3 shipped folds (claim auditor).
- The data are real and faithful: the blind reviewer's feature means and missing shares match the source's 13.2M summary, and 21 of the claim auditor's count checks hold.
- Why it outranks the blind reviewer's "Exclude": that verdict rests on "log1p-RMSE regression" carrying no signal. The definition does not score RMSE. It scores the Gini on the amount, which is the alternative the reviewer itself proposes ("a Tweedie/Gini metric"). The reviewer also saw a 300k sample and could not read the Kaggle pages.

**2. A small real signal, which the right split does not trade away (P6 under P4; TP-2, the Tension "the right split against the score").**
- Evidence: on the shipped folds untuned LightGBM scores Gini 0.096 / 0.051 / 0.058, against 0.008 / 0.008 / 0.003 for random predictions. Each test fold holds 3,652-3,696 claims. Without the model codes it reaches 0.094 pooled, and 0.085 on folds grouped by Blind_Model (domain practitioner). So the signal sits in the vehicle attributes and carries over to vehicle series the model has not seen. Huangfu (2015) reports 0.080 on 2007; Allstate's internal benchmark was 0.059.
- Concession: one Gini has a bootstrap SE of about 0.02 per fold, so 3 folds separate methods poorly (MET-10). This is a value weakness, not a validity failure, and the Tension row says a small signal under the right split is no reason to retire (forest_fires). The pricing_game_2016 reframing to classification does not carry over: there the source had no amount metric, while here the competition fixed one (MET-4).

**3. The forced grouped split is what SPLIT-8 (Must) prescribes, and the reason for the how_much_did_it_rain `No` is absent here (P4; SPLIT-8, SPLIT-14).**
- Evidence that the split is forced: three labelled years, and the 2006 window would train on 30.5% of rows, below SPLIT-14's floor (Must). SPLIT-8, as amended on 2026-10-21, names this exact case: "too few periods for three windows ... grouped by the entity when the periods are stacked and the entities recur (`ForcedGroupedFromTemporal`)". The split auditor's verdict is "right with notes". The precedent is open_university (Lennart).
- What sets this case apart from how_much_did_it_rain: the curator's stated reason there was "forced IID would introduce leaks for this task", and "Forced IID is to be avoided at all costs". This split is not IID:
  - no household is on both sides of any fold (split auditor, claim auditor);
  - random-row folds score 0.050-0.080 against grouped 0.051-0.096, so no hidden group inflates the score (SPLIT-29);
  - the one valid window (train 2005-06, test all 4.7M rows of 2007) scored 0.084 on the full file, inside the grouped folds' 2007 rows (0.059 / 0.086 / 0.115).
- Concession: on the shipped 1.5M rows the window scores 0.063, about one SE below. So "costs little" must be restated as "no cost measurable at this noise" (EV-8, SPLIT-21).
- Rank: rules win over precedents, and SPLIT-8 is unchanged (CC note: "SPLIT-8 itself is unchanged for now"). A `No` here would be an amendment of SPLIT-8, to be made for the family (frempl 5, australian 1, rand 1, spanish 2022-2024 issue 1), not an exception for this dataset. I support the precedent checker's option (a).

**4. The year-level bonus is real; the mildest fix is to drop `Calendar_Year`, and the dataset stays (P4; MET-2 Must, LEAK-24 Must, remedy ladder).**
- Concession: a predictor that knows only the year scores 0.055-0.058. Learning the year's level adds 0.013-0.015 to every fold, a paired effect with the same sign each time. The source scored one year at a time, and a one-year deployment cannot use the year's level. Decision 2's "Kept: ... `Calendar_Year` is a feature" names the mechanism of the bonus, not a mitigation.
- Mildest fix: drop `Calendar_Year` from the features (one line). Within a year this costs nothing (log1p 0.096 / 0.049 / 0.057 against 0.095 / 0.052 / 0.057), and only +0.001 to +0.003 of the bonus remains (split auditor). That resolves the measured MET-2 problem.
- LEAK-24: the evidence is circumstantial (EV-6). There is no valuation date. The tail drops as a step at 2007, while 2005 and 2006 hardly differ (1.31% against 1.26% of claims above 2,000), and a change in Allstate's adjustment fits that as well. The actuary would keep 2007. I propose recording "LEAK-24 not shown violated", consistent with frempl issue 3. If the curator reads LEAK-24 as triggered, dropping 2007 still leaves 8.47M rows against the 1.5M budget, so the folds stay the same size. Either way the result is a changed definition, not exclusion.

**5. `household_vehicles`: the leak is likely, and the fix is a lag (P4; LEAK-10 Must, window clause, case by case; LEAK-7 Should).**
- Concession: the count covers the whole calendar year. Swap years claim at 0.98% against 0.72%, and the column adds 0.015-0.020 Gini against its absence on the column auditor's folds. The builder's "0.042 against 0.040" compared it with `Vehicle`, which carries the same information. The pricing_game_2017 precedent does not carry over: that count comes from a start-of-year policy file.
- Mildest fix (LEAK-7, and the precedent checker's option (a)): replace it with the household's vehicle count in the previous year. That count is built without labels, is known at the rating, and keeps +0.006 to +0.013 of the signal. Otherwise drop it. `Vehicle` stays dropped either way. A fixed leak is no reason to reject a real task (Tension: "fix the leak and keep the task").

**6. The log1p scale is a family call, and either answer ships (P7; CLEAN-16 Should, MET-3).**
- Evidence: the metric scores the amount whatever the training scale. Raw-amount models lead log1p by about +0.011 on the shipped folds, but 0.008-0.013 of that lead is the year bonus of point 4. Without `Calendar_Year`, raw scores 0.073 / 0.075 / 0.068 and log1p 0.096 / 0.049 / 0.057: a mean gap of 0.005, well inside one SE.
- Rank: a Should at P7 with no measured winner once point 4 is fixed. Decide it once, in australian issue 5. Switching scales is a one-line change.

**7. The remaining findings are wording and cleaning fixes (P5 question, P7; PROV-3, CLEAN-11, CLEAN-14, EV-8).**
- Cat10-Cat12 behave like random draws: the same vehicle keeps its value at exactly the chance rate, and Cramér's V is at most 0.0024. The other 29 features show real structure, so this does not put the whole table in question under PROV-3 (the column auditor: "no reason for `No`"). Drop the three columns, since that loses nothing measurable, or keep them with a note.
- The 2 rows with model year 2009 in calendar 2007 become missing.
- `OrdCat`: align with liberty and pricing_game_2017. Its claim rates are not monotone (0.26-0.81%), so typing it categorical costs nothing.
- Corrections:
  - the LEAK-30 note: NVVar1-4 do not rise, and the Var rise is the fleet's mix of model years;
  - "70%" becomes 55.9%;
  - the level counts become 74 / 1,302 / 2,739;
  - the splits_comment numbers come from the shipped folds;
  - add a note that no exposure is given and some rows are part-year (USE-5).
- Bring the record's `required_split` and tag in line with the definition.

```text
Verdict: ship after changes.
Validity: USE-1 holds (approximate fit, actuary agrees); SPLIT-14 fails, so SPLIT-8 applies (ForcedGroupedFromTemporal,
no household straddles, random rows score alike, window 0.084 full file); MET-2 year-level bonus, fixed (drop
Calendar_Year); LEAK-24 not shown (step at 2007, no valuation date) or fixed (drop 2007); LEAK-10 household_vehicles,
fixed (previous-year count or drop).
Value: TP-2, a small real signal (Gini 0.05-0.10 against random 0.003-0.008), MET-4 the competition's metric; MET-10 noise noted.
Quality: Cat10-12 drop or note; OrdCat aligned; number slips corrected.
For the curator: the family's forced-grouped call (option (a): grouped, not IID, cost measured); log1p in australian issue 5.
```

</details>

<details><summary>Critic</summary>

**Critic, opening brief (2026-11-01): allstate_claim_prediction_challenge_1m**

**Verdict: do not ship as defined.** Ship only after point 1 is decided by the curator and the definition is changed for points 2 and 3. Points 4 to 7 are notes and small repairs, not reasons to exclude. The task itself is real (USE-1, approximate fit agreed by the domain practitioner). My case is against the split's standing, the pooled scoring of an immature year, and one built feature.

**1. The split contradicts the premise of the `Yes` and the curator's newest stance on forced splits (P4; SPLIT-8 Must against the curator's 2026-10-30 call; "who decides" in principles.md).**
* Problem: the task is temporal by its use case (rating next year's vehicles; the competition scored 2008 and 2009). Three labelled years give one valid window, so it ships stacked and grouped by household (`ForcedGroupedFromTemporal`).
* Effect on the task: the test stands for new households of the same years, not next year. The 53% of rated households that are known (test_set.csv, split auditor) and their claim history (1.44% claim rate after a prior claim against 0.77%) are not tested.
* Evidence: the record's `Yes` (CC 2026-10-30, Andrej) was given on notes saying "Split temporal by `Calendar_Year`", and the record still has `required_split: Temporal`. The same day Andrej rejected how_much_did_it_rain: "if the data is temporal but a temporal split is not possible, we cannot split the data and reject it", and in chat "Forced IID is to be avoided at all costs". SPLIT-8 as written (Lennart, 2026-10-21) covers this case, and the open_university precedent supports it. But a newer curator decision beats an older one, and the `Yes` does not cover a split the curator never saw.
* What may set it apart (precedent checker): it is grouped, not IID; no household straddles the split, so how_much_did_it_rain's storm leak is absent; the one valid window is measured (Gini 0.084 against 0.069 to 0.094 on the grouped folds' 2007 rows, builder's sample). On the shipped rows that window scores about 0.02 below the grouped folds' 2007 rows (split auditor), which is one SE, so "costs little" only means "no cost measurable".
* Remedy: no ship until the curator decides the family question (frempl issue 5, australian issue 1, rand issue 1, spanish 2022-2024 issue 1) for this dataset by name, choosing (a) SPLIT-8 holds for grouped splits, recorded with the facts above, or (b) `No`. Then bring the record in line.

**2. Pooled three-year test folds reward knowing the calendar year's claim level, and that level is mostly the immature 2007 (P4; LEAK-24 Must; P6, MET-2 Must).**
* Problem: the 2007 claims have a lighter tail at the same claim rate (claims above 2,000 are 0.43% of claims against 1.31% and 1.26%, in every vehicle-age band). That is what undeveloped bodily-injury claims look like (domain practitioner). The definition keeps 2007 and lists `Calendar_Year` as a feature as if that mitigated it.
* Effect on the task: the declared Gini ranks rows of three years together. Neither the competition (one year per leaderboard) nor a deployment (rating one year) has a year to rank.
* Evidence (split and claim auditors, shipped folds): a predictor that knows only the training mean per year scores 0.055 / 0.058 / 0.056, as high as untuned LightGBM on 2 of 3 folds (0.096 / 0.051 / 0.058). Any model that gets the year level right gains 0.004 to 0.015 on every fold, paired on the same rows. Models trained on the raw amount learn the level; log1p models barely do. So the bonus picks between method families. Within a year, dropping `Calendar_Year` costs nothing (0.096 / 0.049 / 0.057).
* Rule: LEAK-24's remedy is "cut where follow-up is complete" (sf_permit_time). MET-2 keeps the source's metric only when its meaning survives the change: Kaggle's Gini was computed within one year, here it is pooled over three. Decision 2's reason serves no higher Must.
* Remedy, mildest that resolves both: drop the 2007 rows. 8.47M rows remain, so the 1.5M sample and the 1M / 500k folds stand, and the year-only Gini falls to -0.021 to +0.010. If the curator reads the step at 2007 (no 2005 to 2006 gradient) as an adjustment change rather than censoring, so LEAK-24 is not shown, the minimum is to drop `Calendar_Year` from the features (bonus down to +0.001 to +0.003) and correct decision 2's wording.

**3. `household_vehicles` counts vehicles added after the rating, including replacements after the row's own crash (P4; LEAK-10 Must, the 2026-10-26 clause on late values that cannot be located row by row).**
* Problem: the definition says the count is "known when a vehicle is rated". It counts every vehicle the household insured at any time in the calendar year.
* Evidence (column auditor, full file): age -1 vehicles claim at 0.20%, so rows include part years. Vehicles insured since 2005 claim in 2006 at 1.17% when the household's 2006 count rose, at 0.72% otherwise (one-vehicle households; the same pattern for 2, 3 and 4+). 9.8% of household-years have a transient extra vehicle. Its gain on the column auditor's folds is 0.015 to 0.020 Gini on every fold, about a quarter of the score; over the previous-year count it still adds 0.006 to 0.013. The builder's "0.042 against 0.040" compared it with `Vehicle`, which carries the same composition, not with its absence. The precedent cited, pricing_game_2017's `client_n_vehicles`, counts a start-of-year policy file, so its key fact differs (precedent checker).
* Rule: LEAK-10's clause says such values "go when they may carry a gain" (distribution_transformers_at_cauca_department). No dates exist to locate the late vehicles.
* Remedy: replace the column with the household's vehicle count in the previous calendar year (missing for 2005 and for new households; built without labels; keeps about +0.007), or drop it. Update `known`, `changes`, the bullet and decision 4.

**4. Cat10, Cat11 and Cat12 behave like random draws, not vehicle characteristics (P5; PROV-3 Must, column-level).**
* Evidence (column auditor): the same vehicle keeps its value from 2005 to 2006 exactly as often as fresh random draws would (Cat10 0.516 against 0.516; Cat11 0.351 against 0.351; Cat12 0.266 against 0.265; Cat3 keeps it 100%). Cramér's V against every other column and the claim is 0.0005 to 0.0024. Claim rates are flat across levels.
* Effect: no leak and no signal. They are not what the dictionary says they are. This is not a reason for `No`, since the other 29 features show real structure.
* Remedy: drop the three columns. The fact that sets them apart from columns CLEAN-22 protects is that they are not what the source says. Or keep them with a note giving these numbers.

**5. The log1p target rests on a claim the shipped probes do not support (P6/P7; MET-3 holds, CLEAN-16 Should; open as australian issue 5).**
* Evidence: the scoring is right (`target_transform="log1p"`, MET-3). But the stated reason, "trained on the amount instead, untuned LightGBM is not consistently better", does not match the precedent's test (pricing_game_2017: a small edge, so the estimand decides). Shipped folds: raw 0.079 / 0.087 / 0.073 against log1p 0.096 / 0.051 / 0.058, raw ahead on 2 of 3. Builder's folds: raw ahead on 3 of 3 (+0.029). Part of the raw advantage is the year bonus of point 2 (+0.008 to +0.013). Without `Calendar_Year`, raw is still ahead on 2 of 3 (0.073 / 0.075 / 0.068 against 0.096 / 0.049 / 0.057).
* Remedy: no separate change. Decide it with australian issue 5, after point 2 is settled, and restate the bullet's comparison on the shipped folds.

**6. The test data differs from what the rater faces in ways the notes do not name (P3; USE-5, USE-8 Should).**
* Evidence: there is no exposure column, and rows include part years (column auditor, domain practitioner), so the record's "Exposure: none (rows are vehicle-years)" is inexact. Only 0.07% to 0.10% of test rows have a model or submodel unseen in training, while a vehicle rating must price new series. Grouped by `Blind_Model`, untuned LightGBM scores 0.007 pooled with the codes and 0.085 without (domain practitioner). 71.7% of test rows have a missing value, where the source says all features are collected at application (thread 826). The column auditor's leave-one-out test clears the missingness itself.
* Remedy: notes only. Add exposure and part years to the target bullet; add to `fit_reason` that the folds test seen vehicle types; add the column auditor's missingness test to decision 3.

**7. Several stated numbers and notes are wrong or come from another sample (procedure; EV-8 Should; P7).**
* Evidence: the `splits_comment` cost numbers ("0.069 to 0.094", "0.021 to 0.073", "0.050 to 0.056") come from the builder's own sample, not the shipped folds (0.059 to 0.115 on 2007 rows, 0.051 to 0.096 on all, random rows 0.050 to 0.080). The LEAK-30 note cites a yearly rise in NVVar1-4 that does not exist. The Var rise fits the fleet's model-year mix, so "probably took in the test years" should be "may have". "70% of the rows share every feature" measures 55.9%. The level counts are 74 / 1,302 / 2,739, not 75 / 1,303 / 2,740. The `household_vehicles` claim rate does not rise monotonically. `changes` omits the dropped copy. `OrdCat` ships numeric, while liberty's ordinals and pricing_game_2017's `pol_coverage` ship categorical with the same reason available (CLEAN-14). The data show no risk order (0.35% to 0.81% to 0.26% across levels).
* Remedy: restate each figure from the shipped folds. Align the `OrdCat` typing with the siblings or ask once. Add `accepted_check_warnings` when the warnings are accepted.

**Not argued:** low signal as a reason to exclude (the blind reviewer's verdict). TP-2 and the forest_fires Tensions row say a small real signal under the right split is no reason to retire. The Gini of 0.05 to 0.10 beats a random prediction (0.003 to 0.008) on every fold. The weak separation of methods (bootstrap SE about 0.02 per fold, MET-10) belongs in a note.

```text
Verdict: ship after changes (not as defined).
Validity: SPLIT-8 applied, against the curator's newest stance: issue 1 (curator's call); LEAK-24 / MET-2 triggered,
fix by dropping 2007 (or at least `Calendar_Year`): issue 2; LEAK-10 triggered (`household_vehicles`), fix by the
previous-year count or a drop: issue 3; PROV-3 column-level (Cat10-12): drop or note.
Value: TP-2, a small real signal (keep); log1p decided with australian issue 5.
Quality: notes for exposure, seen vehicle types, missingness; EV-8 number fixes; CLEAN-14 OrdCat alignment.
```

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate, rebuttal (AI, 2026-11-01): allstate_claim_prediction_challenge_1m**

The critic and I agree on the verdict ("ship after changes") and on five of the seven points. We disagree on two things: whether point 1 bars shipping or only waits on the curator, and which remedy point 2 takes. I ran one new check, on the second.

**New check: dropping 2007 against dropping `Calendar_Year`** (the exact shipped folds, untuned LightGBM, the declared Gini on the amount). The bonus is the pooled Gini minus the row-weighted mean of the Ginis within each year.

| remedy | model | pooled Gini (folds 0 / 1 / 2) | year bonus left |
|---|---|---|---|
| as shipped (split auditor) | log1p / raw L2 / Tweedie | 0.096 / 0.051 / 0.058; 0.079 / 0.087 / 0.073; 0.069 / 0.071 / 0.054 | about 0; +0.008 to +0.013; +0.004 to +0.009 |
| A: drop `Calendar_Year` | log1p | 0.096 / 0.048 / 0.059 | -0.001 to +0.002 |
| A | raw L2 | 0.073 / 0.075 / 0.068 | +0.001 to +0.003 |
| A | Tweedie | 0.070 / 0.056 / 0.040 | +0.001 to +0.002 |
| B: drop 2007, keep `Calendar_Year` | log1p | 0.061 / 0.030 / 0.069 | -0.000 to +0.001 |
| B | raw L2 | 0.036 / 0.061 / 0.055 | -0.000 to +0.001 |
| B | Tweedie | 0.053 / 0.035 / 0.053 | -0.000 to +0.001 |
| C: drop 2007 and `Calendar_Year` | all three | 0.036-0.093 | -0.000 to +0.001 |

Reading:
- Both remedies cut the bonus to well under one SE (about 0.02).
- What A leaves is small but systematic: positive in 8 of 9 runs. B leaves none, about zero in all 9 runs.
- B also takes the possibly immature 2007 amounts out of the targets, which A leaves in.
- In this check B scores fewer claims (about 2,400 per fold), because it filters the 1.5M-row sample. A rebuild draws 1.5M rows from the 8.47M rows of 2005-06, so it restores about 3,650 claims per fold.

**1. The split against the curator's newest stance: narrowed. The curator decides first; this is not a reason the definition is wrong.**
- Conceded: the `Yes` was given on notes that said "Split temporal by `Calendar_Year`". A newer curator decision beats an older one, and "who decides" puts the curator above both of us. So the curator has to decide this dataset by name before it ships, and the record follows that decision. I accept the critic's remedy as written.
- Disputed: that the split contradicts a rule. SPLIT-8 (Must) is unchanged, and the how_much_did_it_rain record says so ("SPLIT-8 itself is unchanged for now"). That `No` gave a fact that is absent here: "forced IID would introduce leaks for this task". Here no household is on both sides, and random-row folds score like grouped ones (0.050-0.080 against 0.051-0.096), so there is no grouping leak to begin with. I recommend option (a). A `No` would need SPLIT-8 amended for the family, since a Must has no exceptions.
- New fact from point 2: after dropping 2007, the split is still forced. 2005 is 4.03M of the 8.47M rows of 2005-06 (47.5%), so even one window is below SPLIT-14's floor. The cost against a valid window was measured on the full file before the drop (0.084 against the grouped folds' 2007 rows, 0.059 / 0.086 / 0.115). That measurement should stay in `splits_comment` as the SPLIT-8 cost measurement.
- Also conceded: the 53% of known households and their claim history (1.44% against 0.77%) go untested. This belongs in `fit_reason`, as the split auditor proposes.

**2. Pooled years and the immature 2007: conceded, and I move to the critic's remedy (drop 2007).**
- My brief offered dropping `Calendar_Year` as the mildest fix. The check shows that dropping 2007 is just as cheap and does more.
- Dropping 2007 removes the year bonus entirely. Dropping `Calendar_Year` leaves +0.001 to +0.003, positive in 8 of 9 runs, and still favours raw-amount models a little (MET-2).
- Dropping 2007 also settles LEAK-24 without a ruling on the cause. The cause cannot be settled anyway, since the data has no valuation date. So the Must holds whatever the curator thinks of the step at 2007.
- Both remedies sit on the same rung of the ladder ("fix the definition"). The row budget and fold sizes stay the same.
- The cost I name: the newest labelled year is lost. The domain practitioner would have kept it with a year factor, but no one can use a year factor when rating one coming year. Dropping `Calendar_Year` stays the fallback if the curator wants 2007 kept.
- What follows in the definition:
  - filter `Calendar_Year < 2007` in `_clean`;
  - keep `Calendar_Year` as a feature (no bonus is left; C shows that dropping it as well changes nothing);
  - rewrite decision 2 and the anomaly bullet;
  - update the row counts and the 45%/8.6% pre-2000 figures.

**3. `household_vehicles`: conceded.** LEAK-10 (Must), the 2026-10-26 window clause. Replace the column with the previous-year count. With 2007 dropped, that count exists only for 2006 rows of households seen in 2005, so its coverage shrinks. That makes dropping the column the simpler fix. The gain the critic cites (+0.015 to +0.020) is the column auditor's measurement against the column's absence, and it outranks the builder's comparison with `Vehicle`.

**4. Cat10 to Cat12: conceded.** Drop them (PROV-3 at column level, nothing measurable lost), or keep them with the column auditor's numbers in a note.

**5. log1p: conceded that the bullet's comparison must be restated; the decision stays with australian issue 5.**
- Under either remedy neither scale wins:
  - after dropping 2007: log1p 0.061 / 0.030 / 0.069 (mean 0.053) against raw 0.036 / 0.061 / 0.055 (mean 0.051), 1 of 3 to raw;
  - after dropping `Calendar_Year`: log1p mean 0.068 against raw 0.072, 2 of 3 to raw.
- Both gaps are a fraction of one SE. The critic's "raw ahead" holds only with the year bonus in. Once point 2 is fixed, CLEAN-16's default has no measured counter-fact here, but the family call still decides.

**6. Notes on exposure, seen vehicle types and missingness: conceded** (USE-5, USE-8). These are the same notes my brief listed. The column auditor's leave-one-out missingness test should go into decision 3.

**7. Number slips, the LEAK-30 wording and `OrdCat`: conceded** (EV-8, CLEAN-14). With 2007 dropped, the splits_comment numbers have to be re-measured on the rebuilt folds anyway. `OrdCat` becomes categorical, since its claim rates show no risk order.

```text
Verdict: ship after changes.
Validity: SPLIT-8 applies (ForcedGroupedFromTemporal; still forced after the 2007 drop, 2005 = 47.5% of 2005-06),
pending the curator's call by name (issue 1, option (a)); LEAK-24 and MET-2, fixed by dropping 2007 (year bonus
-0.000 to +0.001, against +0.001 to +0.003 when only Calendar_Year is dropped); LEAK-10, fixed by dropping
household_vehicles (or the previous-year count); PROV-3 column-level, Cat10-12 dropped or noted.
Value: TP-2, a small real signal (keep); log1p: no measured winner after the fix, decided with australian issue 5.
Quality: exposure, seen-types and missingness notes; EV-8 numbers re-measured on the rebuilt folds; OrdCat categorical.
For the curator: issue 1 (forced grouped split, by name); issue 2 (drop 2007, or keep it and drop Calendar_Year).
```

</details>

<details><summary>Critic rebuttal</summary>

**Critic, rebuttal (2026-11-01): allstate_claim_prediction_challenge_1m**

**Where we stand.** The advocate and I agree on the verdict, ship after changes, and on most of the changes: replace or drop `household_vehicles`, drop or note Cat10 to Cat12, fix the numbers, add the exposure note, align `OrdCat`, sync the record. Two points stay open. First, whether dropping `Calendar_Year` is enough or 2007 has to go; one new fact narrows my position here. Second, what the forced split needs from the curator.

**Advocate 1 (real task, `Yes`, source metric at the decision's unit): concede.** I never argued exclusion on these grounds, and my brief set aside the blind reviewer's "Exclude" in the same way. Its "no signal" rests on log1p-RMSE, which the definition does not score.

**Advocate 2 (small real signal; TP-2): concede.** TP-2 and the forest_fires Tensions row decide it. The MET-10 weakness (SE about 0.02 per fold, one repeat of three folds) goes into a note.

**Advocate 3 (SPLIT-8 prescribes the forced grouped split; a `No` would be an amendment): narrowed, not dropped.**
* Conceded: under the rules as written, SPLIT-14 fails, SPLIT-8 applies, and the facts favour this case (grouped, no household straddles a fold, random-row folds score alike, one window measured). A `No` here would amend SPLIT-8 for the family, not make an exception for one dataset (principles.md, exceptions and amendments).
* Still standing: the curator's `Yes` (CC 2026-10-30) was given on notes saying "Split temporal by `Calendar_Year`", and the record still says `required_split: Temporal`. Under "who decides", a newer curator call beats an older rule application. The how_much_did_it_rain call came the same day and was worded for any temporal task without a temporal split ("we cannot split the data and reject it"), not only for IID. The advocate reads it as limited to IID because of the chat line. The record does not settle which reading is right, and only the curator can.
* Remedy, unchanged: the curator confirms SPLIT-8 for this dataset by name inside the family call (frempl 5, australian 1, rand 1, spanish 2022-2024 issue 1), not by silence. I agree with the advocate that option (a) is the one to put first.

**Advocate 4 (drop `Calendar_Year`; record "LEAK-24 not shown"): MET-2 conceded, LEAK-24 narrowed.**
* MET-2: conceded. Dropping `Calendar_Year` cuts the pooled year bonus from +0.004 to +0.015 down to +0.001 to +0.003 and costs nothing within a year (split auditor). That is the mildest remedy that resolves the measured scoring problem. The year stays faintly readable through the Var drift (ROC AUC 0.58, claim auditor), which the residual already reflects.
* LEAK-24, a new fact from the source pages (data page, Evaluation page): the competition scored 2008 on the public leaderboard and 2009 for the final ranking, and both were labelled by the time it ran (until 12 October 2011). Whatever the valuation date, Allstate scored years at least as young as 2007 is in this file. So the source's own task accepts the newest year at short development, and that weakens LEAK-24 as a reason to cut.
* LEAK-24, what stands: the evidence of immaturity is a fact about the data, not just a possibility. In tail_check.txt, claims above 5,000 make up 0.01% of 2007 claims against 0.10% in both 2005 and 2006, and the q99 is 1,455 to 1,594 in 2007 against 2,019 to 2,429 in every vehicle-age band. The step with no 2005 to 2006 gradient is the advocate's best counter, and neither of us can test it without a valuation date (EV-6).
* My position now: with `Calendar_Year` dropped, keeping 2007 is a defensible reading, recorded as "LEAK-24 not shown violated (step at 2007, no valuation date; the source scored younger years)", with the light 2007 tail kept in `fit_reason` and decision 2 reworded. Dropping 2007 remains the safer option at no cost in size (8.47M rows), but it leaves the source's newest labelled year out. This is a weighing call for the curator, consistent with frempl issue 3. I no longer ask for it as a Must fix.

**Advocate 5 (`household_vehicles`: lag it or drop it): concede.** We agree on the rule (LEAK-10's late-value clause), the evidence and the remedy. The previous-year count keeps +0.006 to +0.013 without the leak.

**Advocate 6 (log1p is a family call; no measured winner once `Calendar_Year` goes): concede.** Without the year, the mean gap is 0.005, well inside one SE, so the bullet's "not consistently better" holds on the shipped folds. Decide it in australian issue 5. The bullet should quote the shipped-fold numbers without `Calendar_Year`.

**Advocate 7 (wording and cleaning fixes): concede, one preference.** For Cat10 to Cat12, I prefer dropping them to keeping them with a note. They are not what the dictionary says, and they carry neither signal nor leak, so a drop loses nothing measurable (column auditor). Either way it is not a `No`.

```text
Verdict: ship after changes.
Validity: SPLIT-8 applies as written; the curator confirms it by name in the family call (the `Yes` premise was a
temporal split): issue 1. MET-2 year bonus fixed by dropping Calendar_Year. LEAK-24 not shown violated (step at 2007,
source scored younger years), or drop 2007: the curator's weighing call. LEAK-10 fixed (previous-year household count, or drop).
Value: TP-2 keep; log1p in australian issue 5.
Quality: Cat10-12 dropped (preferred) or noted; OrdCat aligned; EV-8 numbers restated; exposure note.
```

</details>
