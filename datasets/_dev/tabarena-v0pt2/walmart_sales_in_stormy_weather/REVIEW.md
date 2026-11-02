# walmart_sales_in_stormy_weather

**Outcome:** added; the record is `TBD -> Yes` on your call of 2026-11-02 (issue 2: TP-10 is the only reason it waits).
Before that the AI recommended `TBD -> 2nd Tier` (as m5_forecasting_accuracy), since you kept TP-10 as written,
then `No` (`Time-series (Forecasting)`) unless a tuned model passes leg 1: the leg-1
test, now run over three seeds, stays below crms_phragmites_cover's proposed line of 2 standard errors against both
forecasts built from each pair's own sales. The data are Walmart's second Kaggle recruiting competition (2015): daily
units of 231 store-product pairs that sold before the test weeks, in 45 stores, January 2012 to March 2013 (104,041
rows, 41.1% zeros), scored by the competition's RMSLE. The split is temporal: nine one-week windows, 2013-01-28 to
2013-03-31, at pairs already carried. The data is faithful and nothing leaks the sales; what fails is the test that a
set of per-pair daily series is a tabular task and not forecasting (TP-10, Must). Its second leg fails as written: the
1st and 5th place modelled each pair's own series. Its first leg holds against the naive forecasts TP-10's method names
(25% or more lower), but not clearly against the best forecast built from each pair's own past sales: 1.1-1.5% lower,
1.2-1.4 standard errors, and 1.3-1.7%, 1.8 standard errors, with trailing summaries of those sales added.

Changed after the panel, no decision needed:
* the 16 observed weather columns dropped (LEAK-10, Must: a day's observed weather does not exist at the start of the
  week; they added nothing, and with trailing summaries they made the model worse). This follows aeolus_1m and
  rain_in_australia. The panel's advocate and critic had agreed to keep them with a note, but LEAK-10 keeps a late
  value with a note only where its cells cannot be located, and here every one can. The computed sunrise and sunset
  and the station id stay, so the frame has 6 features;
* a one-day planning gap (SPLIT-10, as rossmann_store_sales): the order for a day goes out a day ahead;
* the use case reworded to every day of the coming week, storms included, which is what the windows score (USE-1; 15.5%
  of test rows, 2,254 of 14,553, lie within 3 days of a storm at the store's station by the definition's storm rule; the
  claim audit's 14.9% left out the storms of the three days after the cut); `fit_reason` rewritten: fit approximate for
  the unmarked stock-out zeros, the missing inventory, prices and product names, and the every-day score (USE-8);
* notes corrected or added where the claim, column and split audits found errors or gaps (scored days, late-winter
  season, product 93, leaderboard not comparable, the recurring 5,568-unit spike kept under CLEAN-11), with the TP-10
  numbers measured again on the changed definition.

Validity: SEL-10/SEL-11 via TP-10 (Must) not met: leg 2 fails as written, leg 1 is not clear against the best own-series
forecast; TP-10 stays as written (2026-11-02). USE-1 triggered, fixed; LEAK-10 triggered, fixed; SPLIT-10 fixed; USE-10,
SPLIT-1, SPLIT-13, SPLIT-21 hold; SPLIT-19 departed from for the scored days (labels never released), noted. SPLIT-20:
windows kept contiguous, departing from perth_house_prices and rain_in_australia (spreading them would test Thanksgiving
and Christmas weeks with no earlier year), noted. Value: MET-2, MET-3, MET-4 hold; not trivial (TP-4). Quality: CLEAN-11
kept with the fact. Weighed: source +, named actor +, size +; no input beyond the ids and the calendar carries signal -.

**Main points:** The record is `TBD -> Yes` (2026-11-02): TP-10, the time-series question, is the only reason it does
not ship, and the folder stays (issue 2). Whether m5_forecasting_accuracy, grocery_store_product_forecasting_challenge
and crms_phragmites_cover, held back by the same TP-10 result, move too is open (issue 2's answer).

**Issues for Andrej:**

2. **Keep the folder while the record holds at `TBD -> 2nd Tier`, or remove it?** Issue 1 is settled: TP-10 stays as
   written (2026-11-02), so the record is `TBD -> 2nd Tier` with `Time-series (Forecasting)`, as
   m5_forecasting_accuracy. No other `TBD -> 2nd Tier` record has a folder in the working copy; m5 has none.
   * What it changes: a kept folder lets a tuned model be tried against the forecasts built from each pair's own
     sales (the one candidate left untried), and a pass needs the trailing-summary columns in the definition. A
     removed folder clears `v2_path`; a later test would rebuild it from the record.
   * Implemented: the folder kept, unbuilt. Alternative: remove it now and keep the record at `TBD -> 2nd Tier`.

   Recommendation: remove it, since no tuned run is planned and a 2nd Tier record holds no folder elsewhere. Decision:
   keep or remove?

   **Andrej (2026-11-02, discuss):** Does this mean the task is good and valid but we don't ship it atm because of the
   time-series nature? If that's the only reason, we should rather switch to tbd yes

   **Answer (AI, 2026-11-02):** Yes. The data is faithful to Walmart's release, nothing leaks the sales, the split and
   the competition's RMSLE hold, and the task is not trivial. The one reason it does not ship is TP-10: whether a set of
   per-pair daily series is a tabular task or forecasting (leg 2 fails as written, leg 1 is not clear against the best
   forecast from each pair's own sales). The only weighed minus, that no input beyond the ids and the calendar carries
   signal, is the same point. So the record is now `TBD -> Yes`, `Time-series (Forecasting)` kept as the reason it
   waits, and the folder stays (this issue). Consistency: three records sit on the same TP-10 result with another
   verdict: m5_forecasting_accuracy and grocery_store_product_forecasting_challenge at `TBD -> 2nd Tier`, and
   crms_phragmites_cover at `No` (its model came within 1.1% of a shrunk last value, walmart's within 1.1-1.5% of the
   best own-series forecast). Nothing sets walmart apart from them on this point; if the reason is the time-series
   nature alone, they would move to `TBD -> Yes` too. Say if they should.

   **Resolved (2026-11-02, Andrej):** keep the folder; the record moves to `TBD -> Yes` (TP-10 the only open reason).

   **Andrej (2026-11-02, dataset verdict: don't ship):** Don't ship for now, but keep it as tbd yes

**Review panel:** don't ship now: `TBD -> 2nd Tier` as m5_forecasting_accuracy, then `No` (`Time-series (Forecasting)`)
unless the TP-10 test passes (mediator). The mediator's leg-1 numbers (one seed, 1.8-1.9 standard errors) predate the
three-seed runs in issue 1 (1.2-1.4 on the shipped features, 1.8 with trailing summaries). Claim audit: 55 claims, 45
hold, 1 weakened (TP-10 leg 1), 6 refuted (numbers and citations in the notes, fixed), 3 untested. Blind review: include
with changes; main concern a task that mostly learns each pair's level from two ids, with same-day observed weather (now
dropped). Debate: agreed on the one-day gap, the season and product 93 notes and the stock-out zeros; the weather was
settled by the mediator (dropped, LEAK-10); disputed: hold or `No` (issue 1).

<details><summary>Mediator</summary>

**Mediator (mediator, 2026-11-01): walmart_sales_in_stormy_weather**

**Recommendation**

```text
Verdict: don't ship now. TBD -> 2nd Tier, as m5_forecasting_accuracy, with the changes below made; No
  (Time-series (Forecasting)) once this run's TP-10 decision lands, unless the test under issue 1 passes.
Validity: SEL-10/SEL-11 via TP-10 (Must) not met. Leg 1: on the changed definition the model leads the pair's own
  forecast by 1.4-1.8% at 1.8-1.9 paired SE (2.0-2.1 SE with trailing summaries, one seed), whichever bar of
  crms_phragmites_cover's issue 1 is used. Leg 2: the top-solution clause fails (1st and 5th place model each pair's
  series); no column lags the target. No definition change fixes either. USE-1 triggered, fixed (use case reworded
  to every day of the coming week; fit approximate, USE-8). LEAK-10 triggered (16 observed weather columns from days
  after the prediction point), fixed (dropped). SPLIT-10 triggered, fixed (gap=1). USE-10, SPLIT-1, SPLIT-13,
  SPLIT-21 hold. SPLIT-19: departed from for the scored days (labels never released), noted. PROV holds.
Value: MET-2, MET-3, MET-4 hold, with a note that the score is not comparable to the leaderboard; TP-4 not trivial.
Quality: CLEAN-11 spike kept with the Thanksgiving fact; SPLIT-20 notes (late winter, item 93); notes corrected.
Weighed: source +, named actor +, size +, pooled model beats models per store and per product 9/9 +; no input
  beyond ids and calendar carries signal -.
For the curator: issue 1, the scope call (hold, No, or amend TP-10 and keep) and the test that would move it to Yes.
```

**Agreed facts**

* The data is faithful: units match the CTU mirror on 100% of rows for 3 stores, the weather on all 8,948
  station-days, no duplicate keys (blind reviewer). No feature comes from the sales; the pair filter reads only days
  before 2013-01-28 (claim audit rows 9, 44).
* The period ends 2013-03-31 for a reason taken from counts: 778 of the 799 storm store-days after that date are in
  the encrypted test, and the competition's split cannot be rebuilt (0 of 4,747 test store-days in train.csv).
* RMSLE is the leaderboard metric; dropping the never-sold pairs keeps the ranking (MET-2).
* The weather adds nothing: -0.0001 RMSLE on all rows (SE 0.0031), worse near storms (+0.0059 to +0.0075); with
  trailing summaries it makes the model worse (0.5196 against 0.5177 at gap 0).
* 15.5% of test rows lie within 3 days of a storm; the model order is the same on those rows and on all rows.
* TP-10 leg 2's top-solution clause fails as written (1st place: a curve per pair then a lasso; 5th: a Gaussian
  process per pair; only the 3rd is our setup). Keeping the dataset needs an amendment, not an exception.
* TP-10's full method: one pooled model beats models per store (5.8%) and per product (6.7%) in 9 of 9 windows;
  seasonal naive forecasts are 28% or more worse.
* Leg 1 is not clear: against the own-series forecast picked on 9 validation weeks, the shipped model leads by 1.4% at
  1.2 SE with gap=1 (advocate); the best model found, 1.8-1.9% at about 2 SE.
* gap=1 (SPLIT-10, as rossmann_store_sales), the SPLIT-20 notes, the MET-2 note, the CLEAN-11 fact and the note
  corrections are agreed. The stock-out zeros are settled by policy call 2 (Andrej, 2026-10-30).

**Decisive experiment (mine).** The open fact was leg 1 on the definition as it will stand (gap=1, observed weather
dropped), and against which bar. I reused the advocate's gap-1 LightGBM runs (1,000 trees, seed 0) and recomputed the
critic's 24 own-series forecasts with the same one-day gap. Scripts and outputs in the run folder (not committed)
(`cal_gap1_vs_pick.py`, `own_series_gap1.py`, `trail_vs_hindsight.py` and their `.txt`).

| model (gap=1) | bar | RMSLE | lead | paired SE | windows ahead |
|---|---|---|---|---|---|
| calendar only (weather dropped) 0.5263 | picked on validation weeks (EWMA 10 days + half weekday) | 0.5358 | 1.79% | 1.94 | 7 of 9 |
| calendar only 0.5263 | best of the 24 unfitted forecasts, picked on the windows | 0.5337 | 1.40% | 1.76 | 8 of 9 |
| calendar + trailing summaries 0.5262 | validation pick | 0.5358 | 1.79% | 2.08 | 7 of 9 |
| calendar + trailing summaries 0.5262 | best unfitted, on the windows | 0.5337 | 1.40% | 2.03 | 7 of 9 |
| calendar + weather (as built, 2 seeds) 0.5272 | validation pick | 0.5358 | 1.61% | 1.39 | 6 of 9 |

Every model loses the week of 2013-02-11. Against the weaker forecasts the builder and the claim auditor used, the
lead is larger (calendar only: 2.4% at 2.6 SE against a 7-day EWMA, 3.6% at 3.6 SE against the 14-day mean), but those
are not the best forecast the series gives. So leg 1 sits at or just under 2 SE under either bar of
crms_phragmites_cover's issue 1 (fitted across pairs, or unfitted and picked on the windows).

**Changes to make now (no decision needed)**

1. Drop the 16 observed weather columns (`tmax` to `avgspeed`, `codesum`); keep `sunrise`, `sunset` (computed in
   advance) and `station_nbr`. Rule: LEAK-10 (Must). Reproduces: 104,041 rows, 6 features (date, store_nbr, item_nbr,
   station_nbr, sunrise, sunset); calendar-only LightGBM about 0.526 RMSLE at gap=1. `clean_weather` stays only for the
   storm counts of the decision tables; fix its `TRACE` docstring citation (the units and forum topic 13200, EV-2).
2. `TemporalSplits(window=7, unit="days", n_windows=9, gap=1)`, with one sentence on the order lead time. Rule:
   SPLIT-10 (Should), rossmann_store_sales. Reproduces: test windows unchanged (1,617 rows each); each train side 231
   rows shorter (89,257 to 102,193).
3. Reword `question` and `use_case` to each day of the coming week, storms included (about 15% of test rows lie within
   3 days of a storm), to set orders for carried products; drop "given the weather that day" and the weather from
   `known`. Rule: USE-1 (Must); fit stays approximate (USE-8).
4. `fit_reason`: the gaps are the unmarked stock-out zeros and the missing inventory, price and product identity; the
   competition scored only days around storms, we score every day. No weather gap (the weather is gone).
5. `splits_comment`: the scored days differ from the competition's (labels of the storm weeks never released;
   storm-only windows would hold 62 to 616 rows, the oldest from 2 stores); the windows are late winter (40% of their
   storm store-days snow, about 6% over the year; no summer storm tested); item 93 stops selling on 2013-02-21 (203
   zero rows, 12.6%, in each of the five newest windows). Rules: SPLIT-19, SPLIT-20 (Should).
6. Metric notes: the leaderboard's RMSLE covered only storm windows over all 4,995 pairs, 95% trivial zeros; ours is
   not comparable. Rule: MET-2 (Must), MET-11.
7. TP-10 notes (EV-7, EV-8): replace leg 1 with the table above (unclipped, both bars, validation weeks
   2012-11-26 to 2013-01-27), add the full method (models per store and per product, seasonal naive), drop "best of
   13" and the weather bullet; leg 2 bullet stays.
8. Anomaly bullet: add that store 37 also sold 3,369 units of product 5 on 2013-11-21, the same Thursday before
   Thanksgiving; drop "the host did not answer". Drop the station 5 bullet (no weather left). Rule: CLEAN-11.
9. `changes` and the `COMPLETE_PERIOD_END` docstring: "the only period none of whose days are in the competition's test
   file" (197 store-days are in neither file). `download_description`: the Walmart Recruiting Survey unlocks the zip.
   Rule: EV-7.
10. Record (no mark needed): the older paragraph and the screening's sibling line cite m5 as `No`; it is
    `TBD -> 2nd Tier` (Andrej, 2026-10-30).

**Changes that need the curator**

Issue 1 below: the verdict. Everything else is in the list above.

**Disputed points**

*1. `TBD -> 2nd Tier` against `No` (`Time-series (Forecasting)`). Goes to the curator.*
* Critic: either; the rules as written give `No`. Advocate: hold, not `No`, because whether the Must can be met is
  still open (a tuned model, this run's TP-10 decision) and m5 was held on the same question.
* Rules: TP-10 is a Must; a Must that the definition cannot fix gives `No` with the marker (principles.md, Strengths);
  exclusion is the last step of the remedy ladder. Leg 2's clause cannot be fixed in the definition, only by an
  amendment, and amendments are the curator's (principles.md, Exceptions and amendments). Leg 1 is not met by any
  definition change measured (table above).
* Not a conflict: no higher Must is served by keeping it. The use case is real (P3), but every Must holds on its own
  (principles.md, How to decide, 4).
* Why the hold: the amendment of TP-10 is on the table in this run (crms_phragmites_cover issue 1;
  basque_offshore_bivalve_biotoxins), and the curator held m5, the same Walmart question, at `TBD -> 2nd Tier`
  ("would just need more evidence to decide how to treat the time series aspect"). Treat like cases alike.
* What settles it: the curator's TP-10 decision of this run, and the test below.

*2. Does rewording the use case fix USE-1, or make the task SEL-10's own example? Settled: it does both, and both are
right.*
* The reword states what the windows score, so USE-1 holds. It names the task as daily sales over a week, SEL-10's
  example; that is the fact, and SEL-11 sends it to TP-10.
* The storm-only filter would not change the scope answer: on the near-storm rows the weather makes models worse and
  the model order is the same, so either population scores a forecast of each pair's sales. The filter also thins the
  oldest window to 62 rows from 2 stores. The reword is the milder remedy.
* USE-9's counter-factor ("a use case rephrased only to excuse a gap") weighs against a direct fit. The fit stays
  approximate, so it does not apply.

*3. The weather: kept with a note, or dropped. Settled: dropped (change 1).*
* Both sides ended on "kept with a note" (LEAK-6, LEAK-38's format), the advocate adding that a drop now has a
  measured reason.
* LEAK-10 (Must) is triggered for every window day: a day's observed totals do not exist at the start of the week.
  LEAK-6's note-and-keep for late values applies only where the late cells cannot be located row by row (LEAK-10,
  second clause); here every one is located. LEAK-38 covers only fields whose timing cannot be tested. "Removing it
  changes no score" is no reason to keep (LEAK-10, 2026-10-21).
* USE-8's "one snapshot standing in for a forecast" names a fit; it does not admit a value from after the prediction
  point, and USE-8 holds with the weather dropped. Not a conflict.
* The source's "perfect weather forecast" is the source's framing, not deployment data (LEAK-38's reasoning on a
  host's test file).
* Precedents: aeolus_1m blanked weather read after departure; rain_in_australia lagged its readings after 9 am.
  Dropping follows both. The cost: the task loses its storm premise. The measurement says the premise carried nothing
  (EV-2), and this bears on issue 1, where it is stated.

*4. What would move it back to `Yes`. The test (to the curator with issue 1).* Both legs:
* Leg 2: an amendment of the top-solution clause in general words: the source's top solutions count only when the
  source's test looks forward in time; when it interpolates between known days (here: test days inside the training
  period), leg 1 carries the test. This alone does not move walmart.
* Leg 1, on the changed definition: a model whose mean paired gain over the best own-series forecast exceeds 2 standard
  errors across the nine windows, ahead in at least 7 of 9, over 3 seeds. The bar is the one chosen in
  crms_phragmites_cover's issue 1: the forecast picked on validation weeks (0.5358 now) if fitted forecasts count, the
  best unfitted forecast (0.5337) if not. Now: 1.76-1.94 SE; 2.03-2.08 SE with trailing summaries on one seed. The
  untested candidate is a model tuned on the validation weeks, with trailing summaries (allowed by leg 2).

**Consistency**

* m5_forecasting_accuracy (`TBD -> 2nd Tier`, Andrej, 2026-10-30): followed.
* rossmann_store_sales (Yes, not reopened, policy call 6): not reopened here. The fact that sets it apart: rossmann's
  inputs hold drivers known in advance (promotions, holidays, store type, competitors); walmart's, after the weather
  drop, hold ids and the calendar only.
* auto_intermittent_demand, car_parts_intermittent_demand, raf_aerospace_parts_demand (`No`, 2026-10-30): the hold
  departs from them. The fact: walmart was probed and is borderline (pooled across pairs beats models per store and per
  product 9 of 9; leg 1 at about 2 SE), and it is a store-sales panel, the line the curator held open with m5. A `No`
  follows them.
* ashrae, g_research_crypto_forecasting, rain_in_australia (in scope): their margins (7.6-10.9%; every interval above
  the baseline; 9 of 9) are far above walmart's.
* crms_phragmites_cover: same bar question and same 2 SE line; walmart fails under either bar.
  basque_offshore_bivalve_biotoxins: there leg 2 holds; here it needs an amendment.
* aeolus_1m, rain_in_australia (LEAK-10): followed by the drop.
* rossmann gap=1 (SPLIT-10): followed.
* perth_house_prices, rain_in_australia (spread windows, SPLIT-20): not followed. The fact: spreading back puts
  Thanksgiving and Christmas weeks with no earlier year into the test, and a 4-week step breaks SPLIT-14's floor; the
  newest weeks are not atypical, which was perth's reason. A note instead.
* mercedes_benz_greener_manufacturing (CLEAN-11, spike dropped): departed from on a fact: the spike recurs on the same
  Thursday before Thanksgiving a year later.
* The curator's `Yes` of 2026-10-30 ("Do yes and then we can see what happens") asked for the measurement; the probed
  finding supersedes the screening call (principles.md, Precedence: stages), so the verdict is the curator's again.

</details>

<details><summary>Claim audit</summary>

**Claim audit: walmart_sales_in_stormy_weather** (claim-auditor, 2026-11-01)

**Verdict.** No validity claim is refuted. Of 55 claims, 45 hold, 1 is weakened, 6 are refuted and 3 are untested. The
refuted ones are numbers or citations in the notes, and none changes the definition. The weakened one bears on the
scope call. Against a stronger forecast built from each pair's own series (an exponentially weighted level with a 7-day
half-life plus the weekday offset), LightGBM's lead falls from the stated 3.5% to 2.6% RMSLE (paired SE 0.0057, ahead
in 7 of 9 windows). That is still a lead, but a narrower one for TP-10 leg 1 (Must). The metric holds on MET-2, MET-3
and MET-4. The claim "the weather adds nothing" holds even when the model is also given the weather of the 3 days
before and after.

How I tested: I rebuilt the container from `dataset.py` with `dataset_io`, scored dummy predictions on every fold with
`data_foundry.v2.metrics.scorer`, recounted the raw files (train, weather, key, sampleSubmission), read the NOAA QCLCD
PDF, the saved Kaggle pages and forum topics 13200, 13319, 14358 and 14452, and pulled the Kaggle leaderboard. I also
ran a TP-10 robustness experiment (6 forecasts from each pair's own series; LightGBM with 1,000 trees and 3 seeds on
calendar, calendar + same-day weather, and calendar + weather + days t-3 to t+3). Scripts and outputs are in
the run folder (not committed) (`raw_checks.py`, `frame_checks.py`, `tp10_attack.py`, `tp10_attack.csv`, `*.txt`).
I did not re-run `dataset check`, because it rewrites README.md.

**Claims**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | Question: daily units of a weather-sensitive product for the coming week, given that day's weather | task_summary.question | read against the data page and the frame | holds | target is per store-product-day; weather is a same-day feature | USE-1 |
| 2 | Use case: replenishment manager stocking milk, bread, umbrellas around a storm ("the competition's description") | task_summary.use_case | Description page | holds | "difficult for replenishment managers to correctly predict the level of inventory needed to avoid being out-of-stock or overstock during and after that storm"; "(like umbrellas, bread, and milk)" | USE-1 |
| 3 | 231 store-product pairs, 45 stores, Jan 2012 to Mar 2013 | task_summary.row | rebuilt frame | holds | 231 pairs, 45 stores, 97 items, 2012-01-01 to 2013-03-31, 104,041 rows | EV-7 |
| 4 | Units sold, scored on a log scale as in the competition | task_summary.predicted | expm1 of the target; scorer | holds | expm1(log1p_units) is an integer on every row (max 5,568); scorer = RMSE on log1p (fold 0: 1.7240 both ways) | MET-3 |
| 5 | Known: store, product, station, date, observed weather as a stand-in for a perfect forecast | task_summary.known, notes bullet 1 | data page; feature list | holds | "it's as though you have a perfect weather forecast at your disposal"; 22 features, none from sales | LEAK-10, USE-1 |
| 6 | Nine one-week windows, newest first, each trained on all earlier days; every day is in a window, storms included | task_summary.split | rebuilt splits | holds | each test fold is 1,617 rows = 231 x 7; train ends the day before; storm rows 4/60/0/40/136/33/24/40/14 (351) | SPLIT-6 |
| 7 | Jan 2012 to Mar 2013 is "the only period whose days are all in the training file" (also COMPLETE_PERIOD_END docstring: "with every store-day") | task_summary.changes, dataset.py l.21 | store-days of the period missing from train.csv | refuted (wording) | 197 store-days of the period are in neither file: store 35's 153 (none before 2012-06-01) and 2012-12-25 for all stores. 0 of 4,747 test store-days fall before 2013-04-01, so the intended claim (no day in the encrypted test) holds. The notes disclose both gaps | EV-7 |
| 8 | Fit approximate; "The weather adds nothing measurable over the calendar" | task_summary.fit_reason | LightGBM (1,000 trees, 3 seeds) with and without weather, and with storm flags, rain and snow for days t-3 to t+3 | holds (stronger than stated) | all rows: weather - calendar -0.0001 (SE 0.0031); + neighbouring days +0.0002 (SE 0.0041). Rows within 3 days of a storm: +0.0059 (SE 0.0089) and +0.0083 (SE 0.0110), i.e. worse with weather | USE-8, EV-1 |
| 9 | No sale after the window start is an input | notes bullet 1 | code; pair filter | holds | no sales feature; the pair filter reads only dates < 2013-01-28 (`_clean` step 2), which is before every window | LEAK-10 |
| 10 | Data-page quote; 4,656 of 4,747 test store-days within 3 days of a storm; 778 of 799 storm store-days after April 2013 missing from train; 11 storm rows in autumn 2014 | notes bullet 2, decision 1 | recount on the raw files and tp10_designA.csv | holds | 4,656/4,747; storms after April 2013: 799, 21 in train, 778 in test; design A windows 0/0/11/0/0/0/0/0/0 | EV-7 |
| 11 | 231 of 4,995 pairs; 1st place "Exclude item/stores whose units are all zeros"; 3rd and 30th the same; 1 pair first sells in the test weeks; store 35 from 2012-06-01; 2012-12-25 absent (closed) | notes bullet 3, decision 2 | raw counts; topics 14452, 14358 | holds | quotes verbatim (3rd: "zero out all the stores/items in the training data with zero item counts"; 30th: "always predict 0 for the remaining"). "Closed" is supported: 2013-12-25 is present with 2 units over 4,884 rows | CLEAN-1 |
| 12 | Zeros 41.1%; data-page quote; 44% of zeros in runs of 28 days or more; the winner zeroed long zero runs using both sides | notes bullet 4 | frame; topic 14452 | holds | 0.4107; 0.444; winner: "Mark dates as 'too much zeros' where both sides are many successive zeros" | USE-5 |
| 13a | TP-10 leg 1 numbers: best naive 0.5389; LightGBM 100 trees 0.5381 (4/9); 1,000 trees 0.5201, 3.5% lower, paired SE 0.0067, 7/9; 0.5209 without weather (8/9) | notes bullet 5, builder report | recomputed from tp10_designB.csv | holds | -0.0189 (SE 0.0067, 7/9, -3.50%); 100 trees -0.0009 (SE 0.0064, 4/9); no weather -0.0180 (SE 0.0045, 8/9) | TP-10 |
| 13b | "the best of 13 forecasts from each pair's own series" | notes bullet 5, builder report | count in tp10.py and the summary JSON | refuted | 11 forecasts (10 without the all-zero one) | EV-7 |
| 13c | Leg 1 holds (narrowly): LightGBM clearly beats each pair's naive forecast | builder report; notes bullet 5 | stronger own-series forecasts on the shipped splits: EWMA level (half-life 7 or 14 days) + weekday offset, a weekday-adjusted EWMA, a blend | weakened | best own-series forecast: EWMA 7d + weekday, 0.5353 (vs mean14+weekday 0.5404 unclipped). LightGBM (3 seeds, mean 0.5212) is ahead by 0.0142 (SE 0.0057), 2.65%, 7/9; it loses in the weeks of 2013-02-11 and 2013-02-18. For comparison, ashrae's lead was 7-11% per window (TP-10 Cases) | TP-10 (Must), SEL-11, EV-9 |
| 14 | Leg 2: 1st place fit a PPR curve per pair, then a lasso with three weather flags; 5th place a GP per pair on time; 3rd place bagged xgboost, no sales lag | notes bullet 6 | topics 14452, 14358; leaderboard | holds | 1st: "G : weather features (is preciptotal > 0.2, depart > 8, depart < -8)". Leaderboard: 1 threecourse, 3 Timothy Scharf, 5 Daniel Korzekwa. The GP post is addressed "@Daniel", so "5th" is no longer only an inference | TP-10 |
| 15 | Storm rows (351) 0.653 with vs 0.640 without weather; autumn 2014 0.375 vs 0.370 vs naive 0.395 | notes bullet 7 | tp10 CSVs | holds | means of per-window RMSLE over the 8 windows with storms; pooled over the 351 rows 0.654 vs 0.647; design A 0.375/0.370/0.395 | EV-8 |
| 16a | M missing, or not reported by the station; "-" no sunrise/sunset; sunrise/sunset HHMM in local standard time | notes bullet 8 | NOAA PDF p.3; data | holds | "M = Missing Data, or data that are not normally reported for the station"; "- = values not available for sunrise/sunset"; "SUNRISE (Calculated, not observed)". LST is not stated for sunrise but fits the data (sunset at most 19:49 in summer) | CLEAN-10 |
| 16b | "T (a trace, less than 0.01 inch of rain or 0.1 inch of snow; NOAA QCLCD documentation)"; also the TRACE docstring | notes bullet 8, dataset.py l.31 | NOAA PDF pp.2-3 | refuted (citation) | the PDF says only "T = TRACE". It gives the units ("INCHES AND TENTHS", "INCHES & HUNDREDTHS"), from which the threshold follows; the threshold itself is stated in forum topic 13200. Counts hold: 12,551 rain rows and 1,326 snow rows | EV-2 |
| 16c | codesum "missing when blank (no phenomenon)" | notes bullet 8, clean_weather docstring | blanks against the other columns | refuted | blank codesum on 2,178 of the 2,191 shipped rows with no numeric weather (station not reporting) and on 1,337 rows with measurable rain (> trace; 244 above 0.1 inch). So missing means "no phenomenon, or not reported", on at least 6% of the 58,785 missing values | CLEAN-10 |
| 17a | Store 37, product 5, 2012-11-15: 5,568 units, about 17x the 99.9th percentile; in every training side | notes bullet 9 | frame | holds | 5,568; p99.9 of positive units 332.7 (ratio 16.7); the date is before the first window | CLEAN-11 |
| 17b | Topic 13319 asked whether it is an error "and the host did not answer" | notes bullet 9 | saved topic JSON; Kaggle page | untested | the saved JSON has no author names. One reply (votes -3), author unknown: "Nothing is a 'mistake' in real world data". The Kaggle page needs JavaScript | EV-7 |
| 18 | "station 5 ... reports nothing but M on 822 of its 852 days, so store 35's 2,121 rows have no weather" | notes bullet 10 | count of M per column for station 5 | refuted (number); the conclusion holds | 822 is the count for temperature, precipitation, snowfall and average wind. Dew point, sea-level pressure and resultant wind are reported on about 406 days, sunrise/sunset on 821; all 15 numeric columns are M on 442 days. Over 2012-06-01 to 2013-03-31 every numeric column is M, so store 35's 2,121 rows carry only the calculated sunrise/sunset (present on all 2,121) | EV-7, CLEAN-10 |
| 19 | Ids are categories with no further information; stores of one station are near each other | notes bullet 11 | data page | holds | "You will not be provided with more information about the products, store locations..."; "some of the stores are nearby and share a weather station" | CLEAN-20 |
| 20 | Target log1p; metric RMSLE on units after the inverse | notes bullet 12, Metric | scorer code and run | holds | `score()` applies expm1 to y and p, then sklearn `root_mean_squared_log_error` | MET-3 |
| 21 | Windows 2013-01-28 to 2013-03-31, newest first, from 2012-01-01, no gap | splits_comment | rebuilt splits | holds | repeat 0 tests 03-25..03-31 on train to 03-24; repeat 8 tests 01-28..02-03 | SPLIT-6 |
| 22 | A week matches the competition's test unit (3 days either side of a storm), a weekly replenishment cycle and a forecast's range | splits_comment | data page | holds for the first part; the rest is unsourced | "predict the units sold for a window of +-3 days surrounding each storm". The other two reasons are inference | EV-2 |
| 23 | The competition's own test cannot be rebuilt | splits_comment | test file; overlap with train | holds | test.csv.zip is encrypted; 0 of 4,747 test store-days are in train.csv | SPLIT-5 |
| 24 | Metric.source `rmsle`; original RMSLE; reference = Evaluation page | Metric | saved Evaluation page | holds | "Submissions are evaluated one the Root Mean Squared Logarithmic Error (RMSLE)", with sqrt(1/n sum(log(p+1) - log(a+1))^2), n = rows of the test set | MET-4, MET-11 |
| 25 | Shipped on log1p, scored on units (`target_transform="log1p"`) | Metric | scorer | holds | scorer = RMSE on log1p (1.7240/1.7240 on fold 0) | MET-3 |
| 26 | Computable on every fold | Metric (implied) | dummy predictions through `scorer` on all 9 folds | holds | unit = row; no inputs or scoring columns; 1,617 rows and 231 pairs per fold; train mean 1.724-1.817, zero 2.343-2.519; negative log predictions are scored (sklearn 1.7.2 only rejects values <= -1) | MET-2 |
| 27 | Same meaning after dropping never-sold pairs | Metric (implied) | share of competition test rows in the 255 active pairs | holds | 26,168 of 526,917 rows (4.97%). Anyone predicting 0 for the dead pairs gets competition RMSLE^2 = 0.0497 x MSE on active rows, so models rank the same. The winner's 0.0934 implies about 0.42 on active rows, against about 0.52 for our forecast windows | MET-2 |
| 28 | The windows score every day, while the competition scored only days near storms (disclosed gap) | fit_reason | count of window rows within 3 days of a storm at the store's station | holds (disclosed) | 2,169 of 14,553 rows (14.9%), 62-616 in every window. Scoring only those rows is computable, but it would need a scoring column and a custom subset metric. Model order on those rows: calendar LightGBM 0.545, + weather 0.549, own series 0.562 | MET-2, MET-13 |
| 29 | Screening: 111 items, 45 stores, 20 stations, 2012-01-01 to 2014-10-31, 4,617,600 rows, 97.4% zeros, 4,740 of 4,995 pairs never sell, 255 hold 236,038 rows with 49.7% zeros | record, screening block and summary | raw recount | holds | all numbers reproduced; no missing or negative units | EV-7 |
| 30 | Description, data-page and Evaluation quotes in the record | record | saved pages | holds | verbatim | EV-2 |
| 31 | Winner: "Weather data has little effect, so I believe any method will be the same" | record | topic 14452 | holds (by inference) | the line answers "@threecourse: How did you deal with missing data from weather file?"; the author field is empty | EV-2 |
| 32 | 30th place zeroed the dead pairs and ran kNN on the date per pair | record | topic 14358 | holds | "apply the knn method (with n=7,14,21) (with date as the only feature)" | EV-2 |
| 33 | Earlier probe: R^2 0.858 / 0.856 / 0.798, ROC AUC 0.971 / 0.971 / 0.953 | record, screening | none | untested | a screening probe on another split, superseded by the add-stage TP-10 | EV-2, EV-8 |
| 34 | Closed 2015-05-25 | record, Reference | rules page | holds | "End Date: 5/25/2015 11:59 PM UTC" | |
| 35 | Policy quote "We don't care. We want to add any relevant predictive task..." | record, Assessment | inputs file | holds | `curation/inputs/two_regime_zero_triage_summary.md` l.263 | |
| 36 | metro_manila asked for TP-10 first (TBD -> Yes); m5 stays 2nd Tier | record, Consistency check | sibling records | holds (as of 2026-10-30) | metro_manila's next CC the same day moved it to `TBD -> 2nd Tier`; m5 is `TBD -> 2nd Tier`, priority 5, leg 2 failed | |
| 37 | dataset check: 0 errors, 0 warnings | builder report | README front matter; container rebuild | holds (not re-run) | `bundle_checks.ok: true`; the container rebuilds to 104,041 x 23 | EV-7 |
| 38 | Probes: no task flag (LightGBM R^2 0.910, item_nbr alone 0.854), no leak, test pairs 100% seen, no generated marks | builder report | probe outputs | holds | task_probes.txt, leak_probes.txt, hidden_groups.txt, generated_probes.txt | EV-3, TP-4 |
| 39 | Licence text | dataset.py `license` | rules page | holds | "use the Data solely for the purpose and duration of the Competition"; "not ... redistribute ... to any party not participating" | EV-4 |
| 40 | Download recipe; "needs an account that accepted the competition's rules" | download_description | zip listing; rules page | recipe holds; the survey requirement is untested | the zip holds key/train/weather/sampleSubmission `.csv.zip` and test.csv.zip. The rules say "Walmart Recruiting Survey must be filled in to unlock the competition data zip file", and the description omits this. The 2026 download worked | |
| 41 | (implied) Every feature is known at the prediction point | definition | features against the prediction point; neighbouring-day weather | holds as a declared stand-in | the same-day weather is future data at the week start, as the source intends; weather of any day adds nothing (row 8), so it gives no advantage | LEAK-10, USE-1 |
| 42 | (implied) The split is the one the use case needs | definition | use case against the regime | holds | a weekly forward window fits a replenishment decision; the competition's interpolated test would read future sales (the winner's centred moving average) | SPLIT-1, SPLIT-5 |
| 43 | (implied) No row is copied across the split | definition | exact feature copies, newest window | holds | 0.0% (even without `date`); every row is a unique pair-day | LEAK-16 |
| 44 | (implied) The pair filter uses no future data | dataset.py `_clean` | code | holds | it reads `date < FIRST_TEST_DAY` only | LEAK-10 |
| 45 | (implied) The TP-10 probe scores the way the benchmark does | scripts/tp10.py | probe code against `scorer` | refuted (small) | the probe clips predictions at 0 and the shipped scorer does not: mean14+weekday 0.5389 clipped, 0.5404 unclipped | EV-8 |
| 46 | The test weeks hold storm days (351 storm rows over the 9 windows) | decision 3 | frame | holds | 351; the week of 2013-03-11 holds none | EV-7 |
| 47 | 2012 storms: 488 of 490 storm store-days in train | decision 1 | raw | holds | the two missing ones are 2012-12-25 (stores 17 and 36) | EV-7 |
| 48 | The weather join: one station per store; codes resolved | notes bullet 8 | key.csv; parse with errors="raise" | holds | each of 45 stores maps to 1 of 20 stations; T appears only in preciptotal (2,410) and snowfall (311) | CLEAN-10 |
| 49 | Station days: every station has 1,035 days except station 5 (852, from 2012-06-01) | implied by bullet 10 | raw | holds | station 5 starts on store 35's first day | |
| 50 | Out-of-stock zeros cannot be told apart from no demand | fit_reason, notes bullet 4 | data page | holds | "sales number 0 doesn't necessarily mean there was no demand ... out of stock, or discontinued" | USE-5 |

**Refuted, weakened and untested claims, ranked (principles.md: validity first, Must first)**

1. **TP-10 leg 1 margin (row 13c), weakened. P2 through TP-10 and SEL-11, Must.** The stated 3.5% lead is over a
   moving-mean baseline. A 7-day-half-life EWMA plus the pair's weekday offset scores 0.5353 against LightGBM's 0.5212
   (3 seeds): a 2.65% lead, paired SE 0.0057 (2.5 SE), ahead in 7 of 9 windows, behind in 2. *What it changes:* the
   evidence behind the curator's scope call (builder draft issue 1). The lead holds but is small; ashrae, the closest
   in-scope precedent, led by 7-11% per window. *Mildest remedy:* replace the leg-1 numbers in notes bullet 5 with the
   stronger own-series forecast, and put 2.6% into the scope issue. The definition does not change.
2. **Probe scoring differs from the shipped scorer (row 45). EV-8, Should.** The probe clips at 0; the benchmark does
   not. *Changes:* the reported numbers by about 0.0015, not the conclusions. *Remedy:* say "clipped at 0" next to the
   TP-10 numbers, or re-run them unclipped.
3. **codesum blanks (row 16c). P7, CLEAN-10.** A blank also stands for a station that did not report (2,178 rows) and
   for days with measurable rain but no code (1,337). *Changes:* what NaN means in `codesum` for about 6% of its missing
   values. *Remedy:* reword to "missing when blank (no phenomenon, or the station did not report)". The data stays.
4. **Station 5 count (row 18). EV-7, P7.** "Nothing but M on 822 of its 852 days" is wrong: 822 is the count of the
   temperature and precipitation columns. *Changes:* nothing in the data; store 35's rows carry no observed weather in
   the period. *Remedy:* "station 5 reports no temperature, precipitation or snowfall on 822 of its 852 days, and no
   numeric weather on any day before April 2013; store 35's 2,121 rows have only the calculated sunrise and sunset."
5. **Trace citation (row 16b). EV-2.** The NOAA PDF gives "T = TRACE" and the units, not the threshold. *Remedy:* cite
   the units (inches and tenths, inches and hundredths) and forum topic 13200 in the note and the `TRACE` docstring.
6. **"All days in the training file" (row 7). EV-7, writing.** 197 store-days of the period are in neither file.
   *Remedy:* "the only period none of whose days are in the competition's test file" in `changes` and in the
   `COMPLETE_PERIOD_END` docstring.
7. **"13 forecasts" (row 13b). EV-7.** There are 11. *Remedy:* fix the count, or give the new count once the EWMA
   forecasts are added (item 1).
8. **Untested: the survey requirement (row 40).** The rules page says the Walmart Recruiting Survey unlocks the zip.
   *Remedy:* add that line to `download_description`.
9. **Untested: "the host did not answer" (row 17b).** It changes nothing (the outlier stays under CLEAN-11 either way).
   *Remedy:* drop the clause, or write "no answer from the host is visible in the thread".
10. **Untested: the screening probe numbers (row 33).** These are superseded by the add-stage TP-10 (EV-2). No action.

**Metric, in short.** The source names RMSLE on units, with n = test rows, on its Evaluation page (MET-4, MET-11). The
definition declares `rmsle` with `target_transform="log1p"`, which the scorer applies (MET-3). It is computable on all
9 folds: per row, no inputs, 1,617 rows each (MET-2). Dropping the never-sold pairs keeps the ranking exactly: 4.97% of
the competition's test rows were active, and the dead rows score 0 for anyone who zeroes them. The one change of
meaning is disclosed: we score every day, the competition only days near storms. Those days are 14.9% of our test rows,
present in every window, and give the same model order, so a subset metric would change little.

**Side note for the precedent checker.** The record carries `suggestion: Yes` (the curator's CC) and
`decision_markers: Time-series (Forecasting)` from the screening. The marker is the open scope question, not a
contradiction to fix here.

</details>

<details><summary>Column audit</summary>

**Column audit (column-auditor, 2026-11-01): walmart_sales_in_stormy_weather**

**Verdict:** no column leaks the sales, and the cleaning is close to the expert state. There is one consistency question
for the curator: the observed weather of days after the window start, with `aeolus_1m` as the precedent (P4). There are
also two small fixes, one in cleaning and one in wording (P7 and notes).

What I read: `dataset.py`, the generated `README.md`, the record, the builder report, the probe outputs, the data page
and forum topics under `pages/`, and the NOAA QCLCD documentation PDF shipped with the data. I loaded the frame with
`dataset_io.from_definition` (104,041 x 23). Scripts and numbers are in the run folder (not committed) (`load.py`,
`raw_codes.py`, `checks.py` to `checks4.py`).

Prediction point (first `curation_comments` bullet): at the start of a week, the manager predicts each store-product's
daily units for the next 7 days. The inputs are the store, the product, the date and that day's weather, which the data
page hands over as observed ("it's as though you have a perfect weather forecast at your disposal").

**Column table**

| column | meaning (source) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `date` | "the day of sales or weather" (data page) | yes, calendar | datetime64; rows sorted by it; 2012-01-01 to 2013-03-31. 2012-12-25 is absent for all 45 stores; no other store-day is missing after a store's first row | fine | CLEAN-14, CLEAN-23, CLEAN-2 |
| `store_nbr` | "an id representing one of the 45 stores" (data page) | yes | categorical, 45 levels | fine: a known entity under a temporal split | CLEAN-3, CLEAN-14, LEAK-34 |
| `item_nbr` | "an id representing one of the 111 products"; the same product in every store (forum topic 13233, a participant's reply, not the host) | yes | categorical, 97 of 111 items in the kept pairs. Alone it scores R^2 0.858 against 0.896 for all features (probe 2): the product's level, legitimate | fine | CLEAN-14, LEAK-34, TP-4 |
| `station_nbr` | the weather station covering the store (`key.csv`) | yes | categorical, 20 levels. A function of `store_nbr` (one station per store, 1 to 6 stores per station), so not a copy; it groups nearby stores | fine (it is no group column: the split is temporal) | CLEAN-3, CLEAN-5 |
| `tmax` | daily maximum temperature, F (QCLCD daily col. 2) | observed that day, so up to 6 days after the window start; declared stand-in for a perfect forecast | float; M becomes missing (2.2%); -1 to 114 F; no `tmin > tmax` | fine as a declared approximation; see problem 1 | USE-8; LEAK-10 (question) |
| `tmin` | daily minimum temperature, F (col. 3) | as `tmax` | float; M becomes missing (2.2%); -11 to 88 F | as `tmax` | USE-8 |
| `tavg` | daily average temperature, F (col. 4) | as `tmax` | float; M becomes missing (4.1%). Equals (tmax + tmin) / 2 rounded half up on 100% of station-days with all three | fine: a derived column the source ships. CLEAN-5 covers exact copies only | CLEAN-5 |
| `depart` | departure from normal, F (col. 5) | as `tmax` | float; M becomes missing (66.1%): 12 of 20 stations never report it, and the rate is the same before and inside the windows (66.0% / 66.6%). The normal is NOAA's published normal, a fixed scale, not computed over our rows | fine | LEAK-30 (fixed published scales are fine), CLEAN-10 |
| `dewpoint` | average dew point, F (col. 6) | as `tmax` | float; M becomes missing (3.0%); no dew point above `tmax` | fine | USE-8 |
| `wetbulb` | average wet-bulb temperature, F (col. 7) | as `tmax` | float; M becomes missing (3.6%); no wet bulb above `tmax` | fine | USE-8 |
| `heat` | heating degree days, base 65 F (col. 8) | as `tmax` | float; equals max(65 - tavg, 0) on 100% of station-days; missing exactly when `tavg` is | fine (derived; `heat - cool = 65 - tavg`) | CLEAN-5 |
| `cool` | cooling degree days, base 65 F (col. 9) | as `tmax` | float; equals max(tavg - 65, 0) on 100% | fine (derived) | CLEAN-5 |
| `sunrise` | "SUNRISE (Calculated, not observed)", local standard time (col. 10) | yes: computed in advance | HHMM converted to minutes after midnight (246 to 460). `-` becomes missing (57.3%): 9 of 20 stations have no computed value (1, 7, 8, 9, 12, 13, 16, 17, 20); station 5 has it on all of store 35's rows | fine: restores the meaning of HHMM | CLEAN-12, CLEAN-10 |
| `sunset` | "SUNSET (Calculated, not observed)" (col. 11) | yes | as `sunrise` (971 to 1,189) | fine | CLEAN-12 |
| `codesum` | significant weather types (col. 12): 28 distinct codes (BR, RA, HZ, TSRA, SN, FG+ ...) in 293 combinations | observed that day | string; a blank becomes missing (56.5%). A blank means "no phenomenon" at 19 stations (blank on only 1.8% of station-days with 0.1 inch of rain or more) but "not reported" at station 5, which is blank on all 852 of its days | cleaning nit: two meanings are merged into one missing value (problem 2). The string dtype is fine: 100% of test values were seen in train, and the top solutions discarded the column (3rd place: "Discard CodeSum") | CLEAN-10, CLEAN-14 |
| `snowfall` | snowfall, inches and tenths, the 24 hours to 2400 LST (col. 15); "Not all stations report snow totals" | observed | float; T becomes 0.05 (1,326 rows), M becomes missing (38.8%: 6 stations never report it) | fine: T stays a value between 0 and the reporting unit (the winner: "Replaced with a small value or zero") | CLEAN-10 |
| `preciptotal` | water equivalent, rain plus melted snow, inches and hundredths, the 24 hours to 2400 LST (col. 16) | observed; defines the competition's storm (more than 1 inch) | float; T becomes 0.005 (12,551 rows), M becomes missing (2.2%); maximum 7.36 | fine | CLEAN-10 |
| `stnpressure` | average station pressure, inches Hg (col. 17) | observed | float; 23.75 to 30.55 (station 13 at altitude, median 24.24). Two station-days lie 0.01 to 0.03 above sea-level pressure, at stations 10 and 12, which are near sea level: rounding | fine | CLEAN-11 |
| `sealevel` | average sea-level pressure, inches Hg (col. 18) | observed | float; 29.22 to 30.70; no value beyond 6 SD of its station | fine | CLEAN-11 |
| `resultspeed` | resultant wind speed, mph, "the vector sum of wind speeds and directions" (col. 19) | observed | float. On 79 station-days it exceeds `avgspeed` by 0.1 to 1.9 mph (median 0.3), probably because the two come from different samplings: unusual, not impossible | fine | CLEAN-11 |
| `resultdir` | resultant direction, tens of degrees (col. 20) | observed | float, 1 to 36; a circular quantity kept as shipped | fine: encoding it is the pipeline's job | CLEAN-2 |
| `avgspeed` | average wind speed, mph (col. 21) | observed | float, 0.1 to 28.7 | fine | USE-8 |
| `log1p_units` (target) | log1p of "the quantity sold of an item on a given day" (data page) | the outcome | float; whole units underneath; 41.1% zeros. The maximum is 5,568 (store 37, item 5, 2012-11-15), kept | fine; the outlier is kept with good reason (see note c) | CLEAN-16, CLEAN-11, MET-3 |

Not in the frame: `units`, which became the target. All 20 columns of `weather.csv` are there, with `station_nbr` and
`date` as the join keys. `train.csv` has no row id. Nothing is computed over all rows: the pair filter reads only the
sales before 2013-01-28, the oldest test day, and the trace values are fixed constants (LEAK-29, CLEAN-7 hold).

**Leak checks beyond the probes**

* No column is recorded after the sales or caused by them. The weather does not depend on a store's sales, and the ids
  encode no label (LEAK-10).
* Is weather missingness driven by the outcome? I took the 19 stations that normally report each field. On their
  station-days with `preciptotal` missing (129 rows) or `tmax` missing (173 rows), the pair-demeaned zero share is
  -0.038 and -0.023, and the pair-demeaned log1p units +0.051 and +0.005. That is no sign of outcome-driven missingness
  (LEAK-10, probe 3 conditioned on the pair). The missing rates are station-level and stable over time: `depart` 66.0%
  before the windows and 66.6% inside them, `snowfall` 38.6% and 40.2%.
* Are rows missing because of the outcome? No: the only gaps in the period are 2012-12-25 for every store and store
  35's days before its first row.
* 44 rows come from 7 store-days on which every kept pair sold 0. Four stores did so on 2012-11-22 (Thanksgiving), and
  stores 35 and 45 on 2013-02-09, inside the windows (12 rows). These are plausible closures, real zeros for a
  replenishment manager, so they stay.

**Problems, ranked by principles.md**

1. **P4, question for the curator (LEAK-10 and LEAK-6 against USE-6 and USE-8; consistency with `aeolus_1m`).** 16
   weather columns hold what was observed on each day of the window: every weather column except `sunrise` and
   `sunset`, which are computed in advance. That is up to 6 days after the prediction point. The definition declares
   them a stand-in for a perfect forecast, in the source's own words, and sets the fit to approximate. That is a
   defensible reading of USE-8 ("one snapshot standing in for a forecast").
   - Precedent: the curator decided the other way on similar facts. `aeolus_1m`, CC 2026-10-26 (Lennart), issue 7:
     "mask": the weather read after the scheduled departure is set missing (LEAK-6).
   - What sets this case apart: (a) the source hands over the observed weather as the forecast on purpose, and its
     question is the sales given the weather; (b) the measured gain is nil, where the aeolus mask removed "a confirmed
     small leak". The builder's numbers, which I did not rerun: all windows RMSLE 0.5201 with the weather and 0.5209
     without; the 351 storm rows of the windows 0.653 with and 0.640 without; autumn 2014 0.375 with and 0.370 without.
     The weather makes the storm rows worse.
   - Against keeping: LEAK-6 says "a confirmed leak goes even when small", and LEAK-10's clause of 2026-10-21 says a
     "removing it changes no score" test alone is no reason to keep.
   - Strength: weak. The weather is outside the store's control, and it buys no score.
   - Mildest remedy: keep it. Write a `Potential leak, kept on purpose:` note in LEAK-38's format (the mechanism, the
     numbers above, why it stays, when to revisit: if a model ever gains from the weather) that names the aeolus
     distinction, and record the curator's answer as an exception or as a reason to treat both alike.
   - Next remedy: drop the 16 observed columns and keep `sunrise` and `sunset`. By the numbers this costs nothing, but
     it leaves ids and the calendar only, which makes the builder's issue 1 (SEL-10 and TP-10, forecasting) lean
     further toward No. Decide the two together.
2. **P7, cleaning, a cheap fix (CLEAN-10).** `codesum`: blank becomes missing, which merges "no phenomenon" (19
   stations) with "not reported" (station 5, 2,121 rows, about 2% of the frame). Under CLEAN-10, a code that means
   something is kept. Fix: map a blank to a literal such as `none` at the stations that report weather types, and leave
   station 5 missing. Otherwise keep the column and correct the note (see note d). The effect is negligible:
   `codesum` as text alone scores R^2 -0.005, and the weather adds nothing.
3. **Notes that need a correction or a fact (writing; no rank).**
   - a. The station 5 bullet says the station "reports nothing but M on 822 of its 852 days, so store 35's 2,121 rows
     have no weather". Over the whole file, station 5 reports dew point, sea-level pressure and resultant wind on 406
     days, all outside our period. Inside the period, store 35's rows have no observed weather, but the computed
     sunrise and sunset are present on all 2,121 rows. Say "no observed weather in our period (the computed sunrise
     and sunset are present)".
   - b. The weather bullet attributes the trace thresholds ("less than 0.01 inch of rain or 0.1 inch of snow") to the
     NOAA QCLCD documentation. The PDF says only "T = TRACE", next to the reporting units: hundredths for
     precipitation, tenths for snowfall. Cite forum topic 13200, or say the thresholds follow from the units.
   - c. The anomaly bullet (store 37, item 5, 5,568 units on 2012-11-15, kept under CLEAN-11) can gain one fact: the
     same store and item sold 3,369 units on 2013-11-21, outside the period. Both days are the Thursday one week before
     Thanksgiving (2012-11-22 and 2013-11-28). The pair's median is 43 units and its 99th percentile 122, so this looks
     like a recurring event, not a typo, which supports the keep. The forum post (topic 13319) notes that "both outliers
     were at the same store".
   - d. If problem 2 is not fixed, the weather bullet's "missing when blank (no phenomenon)" should add "or not
     reported (station 5)".

**Checked and left alone**

* `tavg`, `heat` and `cool` are exact functions of `tmax`, `tmin` and `tavg`. They are not copies under CLEAN-5, and the
  source ships them, so they stay.
* `depart` rests on NOAA's published normals (LEAK-30: a fixed scale).
* There are no history (lag) features. This matches the top solutions, which used none (the 1st and 3rd place), and
  `rossmann_store_sales`, which builds none. CLEAN-19 asks for nothing here unless the curator reframes the task as
  forecasting.
* The dtypes follow CLEAN-14: the ids are categorical, `codesum` is a string, `date` is a datetime, the measured
  quantities are numeric.

**Judgment record (columns only)**

```text
Verdict: ship after small changes (columns).
Validity: LEAK-10 holds for every column (no column records the sales or is caused by them; weather missingness shows
no outcome signal); LEAK-29/CLEAN-7 hold (pair filter on the history before 2013-01-28); USE-8 approximation for the
16 observed weather columns, open as a consistency question against aeolus_1m (LEAK-6).
Quality: CLEAN-10 codesum blank merges "none" with "not reported" (cheap fix); CLEAN-11 outliers kept, supported;
CLEAN-12 sunrise/sunset restored; CLEAN-14 dtypes by meaning hold.
For the curator: problem 1, a consistency call tied to builder issue 1 (keep the perfect-forecast weather with a note,
or drop it and accept a calendar-only series).
```

</details>

<details><summary>Split audit</summary>

**Split audit (split-auditor, 2026-11-01): walmart_sales_in_stormy_weather**

**Verdict: right with notes.** The regime fits the use case: known store-products in a daily stream, so temporal. The windows, the expanding train side, the training history and the cut at 2013-03-31 hold. Four notes, all fixable in the definition or the text: (1) the test scores every day, but the source's task and our own use_case sentence are the days around storms; (2) there is no planning gap, unlike rossmann_store_sales; (3) all nine windows fall in late winter; (4) the largest product is discontinued inside the five newest windows.

```text
Validity: USE-10 holds (known entity, temporal); SPLIT-1/USE-1 triggered: the test population (every day) differs from the
  source's task and the stated use case (days around storms), fix by a test filter or an exception to SPLIT-19 plus a
  rewritten use_case; SPLIT-9 holds; SPLIT-10 departure without a recorded fact (no planning gap; rossmann has gap=1);
  SPLIT-11, SPLIT-12, SPLIT-14, SPLIT-15, SPLIT-17, SPLIT-18 hold; SPLIT-19 departure justified for the split itself
  (labels never released) but not for the scored population; SPLIT-20 two notes (late-winter windows; item 93's
  discontinuation in the newest windows); SPLIT-21 holds (period chosen from counts).
For the curator: issue A (test population: filter or exception), issue B (gap=1, as rossmann).
```

**How I checked.** I loaded the frame and splits through `dataset_io.from_definition` (9 x 1 splits, as declared; the README's train and test ranges match). I re-read train.csv, weather.csv, key.csv and the test ids in sampleSubmission.csv. I fit LightGBM (1,000 trees, the builder's settings, ids as categories as shipped, 2 threads) on every shipped window and on the variants below. Scoring was RMSLE on units, the same as RMSE on log1p units. Scripts and outputs are in the run folder (not committed).

**What holds, with numbers**

* Regime (USE-10, SPLIT-3, SPLIT-13). The actor is a replenishment manager stocking products the store already carries, so every prediction is for a known store-product, made forward in time. That makes the split temporal, as declared. All 231 pairs in each test window also appear in its train side (hidden-group probe: test rows seen 100% for `item_nbr`, `store_nbr` and `station_nbr`). A new store or a new product (cold start) is not the use case.
* Time column. `date` is the sales day. Units come from the till and are known by the day's end, so there is no label delay. SPLIT-9 holds: the pair filter (a sale before 2013-01-28) reads only days that are inside every training side, and 1 pair is left out for first selling inside the windows.
* Windows (SPLIT-11, SPLIT-12, SPLIT-14, SPLIT-15, SPLIT-17, SPLIT-18). There are nine windows of 7 days, Monday to Sunday, from 2013-01-28 to 2013-03-31, newest first. Each holds 1,617 rows (231 pairs x 7 days, none missing). Train sides hold 89,488 to 102,424 rows (86-98% of the data). Nine splits is what an IID task of 104k rows would get (3 x 3). One week matches the source's test unit ("a window of ±3 days surrounding each storm", data page) and SPLIT-18's one-to-two-week limit for weather.
* The cut at 2013-03-31 (SPLIT-19, SPLIT-21). train.csv is complete up to 2013-03 (every store-day from June 2012; store 35 has no rows before 2012-06-01; 2012-12-25 is closed). After that, 69-93% of store-days are present per month. The encrypted test runs from 2013-04-01 to 2014-10-26, and 4,656 of its 4,747 store-days lie within 3 days of a storm. The alternative design (all of train.csv, windows 2014-08-30 to 2014-10-31) would test on 2,239 of 2,835 store-days (79%). The missing 21% are exactly the days around storms, so its test set would be selected on the weather, the opposite of the use case. The definition chose its period from these counts (decision table), not from scores. Right.
* Training history (SPLIT-20). Every window trains from 2012-01-01, so 2012-01-28 to 2012-03-31, the same season a year earlier, is in every train side. The history has no break apart from item launches and store 35's opening.
* Hidden groups and near copies. Rows that differ only in `store_nbr` (s_id 0.704) are stores sharing a station, with the same item on the same date. A temporal split always keeps them on the same side. Near copies seen in train: 0.2%.

**Problems, ranked by principles.md**

**A. The test scores every day; the source's task and the stated use case are the days around storms (USE-1 and SPLIT-1, Must; SPLIT-19, Should).**
* Evidence. Data page: "The competition task is to predict the amount of each product sold around the time of major weather events ... You are asked to predict the units sold for a window of ±3 days surrounding each storm". Our `use_case` repeats this ("sets the stock ... for the days around a storm"). But `question`, `split` and the windows score every day. Of the 14,553 test rows, 2,254 (15.5%) lie within 3 days of a storm at the store's station, and 351 (2.4%) are storm days. `fit_reason` names the gap, but the text contradicts itself: the use case is storms, while the score is daily demand.
* Measured under both populations (9 windows, paired over windows):

| test rows | LightGBM, weather | LightGBM, no weather | best naive (14-day mean + weekday) | weather minus no weather |
|---|---|---|---|---|
| every day (shipped), 1,617 per window | 0.5211 (-0.0178, SE 0.0072; ahead 7/9) | 0.5204 (8/9) | 0.5389 | +0.0007 |
| within 3 days of a storm, 62-616 per window (195, 300, 69, 187, 616, 476, 167, 182, 62, newest first) | 0.5505 (-0.0190, SE 0.0094; ahead 6/9) | 0.5430 (-0.0265, SE 0.0084; 8/9) | 0.5695 | +0.0075 (SE 0.0079) |

  The reading is the same under either population: the model beats the naive forecast by about 3%, and the weather adds nothing. The choice changes what the score stands for, not the TP-10 reading.
* Mildest remedy, in the order of the remedy ladder:
  1. Fix the definition. Filter each window's test side to the store-days within 3 days of a storm at the store's station (override `_make_splits`; the train side keeps every earlier day). This follows the source's scored population (SPLIT-19) and the use case as written. Every window keeps at least 50 rows (SPLIT-17), though the two smallest hold only 62 and 69.
  2. Keep every day and record an exception to SPLIT-19. The fact that sets the case apart: the storm windows exist to measure the weather, which carries no measurable signal here; every day is a stocking decision; and there are 6.5 times as many test rows. Then rewrite `use_case` to "for each day of the coming week, storms included" so it matches the score.
  
  This is the curator's call. Note that option 2 moves the task closer to plain daily demand forecasting, which bears on the open scope question (SEL-10, TP-10; builder issue 1).

**B. No planning gap, unlike the closest precedent (SPLIT-10, Should; "treat like cases alike").**
* Evidence. The windows train up to the evening before the week starts. Stock for Monday has to be ordered and delivered before Monday. rossmann_store_sales (store-day sales, a manager's horizon from the competition) ships `TemporalSplits(window=42, unit="days", n_windows=3, gap=1)` "as a planning gap", and the record cites rossmann as a sibling. `splits_comment` gives no fact that sets this case apart. Measured: a 2-day gap raises LightGBM's RMSLE by 0.0083 (SE 0.0024), worse in 8 of 9 windows, and by 0.0125 on the storm-neighbourhood rows. The last days before a window carry real information, so the gap is not cosmetic.
* Mildest remedy: `TemporalSplits(window=7, unit="days", n_windows=9, gap=1)`, with one sentence on the order lead time. Alternatively, record why this case differs from rossmann: a consistency question, not an override.

**C. All nine windows are late winter (SPLIT-20, Should: a season-shaped test).**
* Evidence. The 65 storm store-days in the windows are 40% snow (26). Outside the windows the share is 6.1% of 1,224. April to September holds 877 of the 1,289 storm store-days (68%), and none of them are snow. The competition tested April 2013 to October 2014, all seasons. The windows cannot move. After March 2013 the storm days are missing. Spacing the windows back by 2-4 weeks would put 3 windows in November-December 2012, where Thanksgiving and Christmas have no earlier year in train. At a 4-week step the oldest train side drops to 48.9% of the rows, below SPLIT-14's floor.
* Mildest remedy: a note. Add one sentence to `splits_comment` saying that the test weeks are late winter, that their storms are 40% snow against about 6% over the year, and that summer rain storms are not tested.

**D. The largest product is discontinued inside the five newest windows (SPLIT-20, Should: a break; for the target, USE-5).**
* Evidence. Item 93 holds 13,043 rows (12.5%) in 29 stores. It sells for the last time on 2013-02-21: 20 of 29 stores' last sale falls between 2013-02-18 and 2013-02-21. It never sells again up to 2014-10-31. So 1,102 test rows (7.6% of the test pool) are zeros of a discontinued product: 203 per window (12.6%) in the five windows from 2013-02-25, and 87 in the window that contains the stop. The data page calls this kind of zero "discontinued and not available"; it is a fact the replenishment manager knows. In the newest window, 51 pairs (22% of its rows, 29 of them item 93) had no sale in the 28 days before. In the older windows the share is 13-24 pairs (6-10%). Without those rows every score rises by about 0.014 (LightGBM 0.5349, naive 0.5533), but the comparison is unchanged (-0.0184, SE 0.0061, ahead in 8 of 9).
* Mildest remedy: a note in `splits_comment` and in the zeros bullet. Dropping a pair's rows after its last sale would read the future (the label after the period), so it is a target question for the column and claim auditors (USE-5), not a split fix.

**Side note for the task-probe and claim auditors (EV-8).** I reproduce the builder's leg-1 numbers (0.5201 with weather, 0.5209 without) only with the ids as categories: 0.5211 and 0.5204. With the same model reading `store_nbr` and `item_nbr` as integers, the weather model scores 0.5346 and is ahead of the naive forecast in only 4 of 9 windows (0.5249 and 7 of 9 without weather). Leg 1's margin depends on how a model encodes the ids. The shipped feature types are categorical, so the stated numbers stand for that encoding.

**Split claims checked**
* `task_summary.split`: "Nine one-week windows from late January to March 2013, newest first, each trained on all earlier days; the windows hold every day, storms included". True (2013-01-28 to 2013-03-31; 1,617 rows each).
* `splits_comment`: "each trains on every earlier day from 2012-01-01, with no gap". True. "A week matches the competition's test unit (the 7 days from 3 before to 3 after a storm)". True (data page). "The windows end on 2013-03-31 because later days around storms were never released with their sales". True (778 of 799 storm store-days from April 2013 are in the encrypted test). "The competition's own test ... cannot be rebuilt". True (test.csv is encrypted and holds no units). Missing from the comment: the reason for no gap (issue B), the late-winter season (C), item 93 (D), and the scored population against the source's (A).
* Builder's "hidden groups none (test pairs seen 100%, SPLIT-13)": true, and the right reading for a known-entity task.

**Files** (scratch, not repository files): the run folder (not committed) holds `load.py` (frame and splits via dataset_io), `raw_checks.py` (coverage, storms, near-storm rows), `counts.py` (dead pairs, storm types, design A coverage, spaced windows), `dead.py`, `models_cat.py` and `models_cat.csv` (shipped, near-storm, 2-day gap, without item 93, ids as categories), `models.py`, `models.csv` and `item93.py` (ids as integers), and `models_seed.py` (seed check).

</details>

<details><summary>Domain practitioner</summary>

**Role: domain practitioner.** I play a Walmart replenishment manager. I set the store-item orders for weather-sensitive grocery and general merchandise (milk, bread, umbrellas) for the coming week, and I adjust them when a storm is forecast. Read-only review. My probe is in the run folder (not committed) (`practitioner_probe.py`, `probe.json`). It rebuilds the shipped frame from `dataset.py` and fits LightGBM with 1,000 trees on the nine shipped windows.

**Verdict: the fit is approximate (USE-8), and I agree with the definition.** Observed weather stands in for my forecast, a zero can be a stock-out I cannot see, and the windows mostly test a routine week-ahead forecast of carried items, not the storm decision the use case names. The wording of the use case should say what the windows test (issue 1 below). The metric scores my decision **partly** (MET-1, MET-2). Keep `rmsle` (MET-4) and add a note.

**How the decision is made today**
- Walmart's Description: replenishment managers find it hard "to correctly predict the level of inventory needed to avoid being out-of-stock or overstock during and after that storm". Walmart "relies on a variety of vendor tools ... an ad-hoc and time-consuming process".
- The well-known case is Hurricane Frances (NYT, 2004; forum topic 13299). A week before landfall, Walmart's CIO had analysts forecast from what sold during Hurricane Charley, an earlier storm of the same kind. Strawberry Pop-Tarts sold at about 7 times their normal rate.
- Weather-demand vendors (Planalytics) adjust store-item-day forecasts with the coming weather. They set this against the recent sales trend: "the recent sales trend is important, it is distorted by the weather conditions that have occurred".
- So at the start of a week I hold:
  - each store-item's sales up to yesterday;
  - on-hand inventory and in-stock status;
  - price and rollbacks;
  - what the item is and where the store is;
  - a weather forecast whose skill falls with lead time.

**1. Inputs at the prediction point (USE-3, USE-6, USE-10)**
- *Shipped and known to me*:
  - store, item, the store's station, the date and calendar.
  - These ids are anonymous ("You will not be provided with more information about the products, store locations"), so I cannot tell milk from umbrellas.
- *Shipped but not known to me*:
  - The observed weather of days 2 to 7 of the week. I would have a forecast, and a forecast of more than an inch of rain several days out has little skill.
  - It is declared as a perfect-forecast stand-in (USE-8) and it carries no signal. All rows: RMSLE 0.5253 with the weather, 0.5250 without. Days within 3 of a storm: 0.5767 with, 0.5759 without. So the optimistic input does not flatter models here.
- *Missing, and I would always have them*:
  - (a) In-stock status or inventory. This is the one that matters most, because it is what separates a demand zero from a stock-out zero.
  - (b) Price, promotions and the product's identity. The source anonymised them, so this cannot be fixed.
  - (c) The pair's recent sales as a feature. Under USE-10 a known entity's history is a legitimate input. Measured with summaries lagged 7 days or more (the same weekday 1 to 4 weeks back, a 28-day and an 84-day mean, the zero share), which are valid for any day of a 7-day window: RMSLE 0.5222 against 0.5253 (0.6% lower), weekly WAPE per pair 0.1638 against 0.1774 (7.7% lower).
  - On the declared metric the history adds little, because the ids and the date already carry each pair's level. Leaving it out follows the competition's inputs and the house precedent: `rossmann_store_sales` (direct) and `ashrae_great_energy_predictor_iii_1m` ship no lags.

**2. The target (USE-5)**
- I act on demand, and I order in units against a service level. The target is units sold, which is a censored proxy for demand.
- The data page says a 0 may mean "out of stock, or discontinued and not available". 41.7% of the test rows are zeros, and the builder found 44% of all zeros in runs of 28 days or more.
- The risk for me is a feedback loop. A model trained on unmarked stock-outs learns to forecast 0 for an out-of-stock item, I order nothing, and the item stays out.
- The curator's policy (2026-10-30, "We don't care") keeps the zeros, and `fit_reason` names the gap. That is the right place for it.
- What I want is a number, and better a quantile or a distribution for safety stock. RMSLE asks for a centre on the log scale, which lies below the mean: every model in my probe forecast 5 to 7% fewer units than were sold (ratios 0.931 to 0.949).

**3. Does a row match a decision, and does the test match what I face (USE-1, USE-10)**
- One store-item-day row matches my automated daily replenishment, and a 7-day window matches my weekly cycle and the range of a usable forecast.
- The test entities are the same carried pairs next week, which is what I face (a known entity, USE-10).
- The mismatch is with the stated use case. It says "for the days around a storm", but only 2,254 of the 14,553 test rows (15.5%) lie within 3 days of a storm at the store's station. Per window that is 62 to 616 rows from 2 to 27 stores, so the oldest window has 62 rows from 2 stores.
- The windows cover one winter: late January to March 2013, 20 station-days with more than an inch of rain and 21 with more than two inches of snow. The competition's test sat mostly in April to October: 438,228 of its 526,917 rows, the thunderstorm and hurricane season of the Pop-Tart story.
- Both limits are forced, because later storm days sit in the encrypted test.csv. They still bound what the shipped task can say about storm stocking.

**4. Would I use the model**
- For routine forecasts of carried items, yes, as a cross-check. LightGBM beats my 14-day mean plus weekday rule by about 3.5% RMSLE (builder: 0.5201 against 0.5389, ahead in 7 of 9 windows).
- For the storm decision, no. In this sample the weather does not move sales: the 1st place wrote "weather features are not effective almost at all ... people go shopping as usual however much it rains", and forum topic 14113 found the same.
- I would keep my analog-storm playbook for storms.
- It would earn my trust if it beat my naive rule in every window and its volume bias were corrected. I would distrust it because it forecasts zeros after a stock-out run and under-forecasts volume.

**5. Does the metric score my decision: partly (MET-1, MET-2, MET-4)**
- *For keeping RMSLE*:
  - It is the host's choice for this decision (MET-4). It is computed correctly on the units after the inverse of log1p (MET-3).
  - It works at the unit I act on, the store-item-day.
  - A second grocer chose the same family: Favorita's NWRMSLE, with perishables weighted 1.25.
  - A relative error is defensible across items selling from 1 to 5,568 units a day.
- *Against it*:
  - (a) MET-2, a changed population. The competition scored only the days within 3 of a storm, over all 4,995 store-item pairs. 95% of its 526,917 test rows came from pairs that never sold and were trivially 0 (only 26,168 rows were active pairs). Our RMSLE scores every day of 231 carried pairs. It is the same formula with a different meaning, and our numbers (about 0.52) cannot be compared with the leaderboard's.
  - (b) It weights items unlike a planner. The bottom half of pairs by volume sells 1.4% of the test units but holds 42% of the squared log error. Rows with zero sales hold 29% of it.
  - (c) It rewards forecasting below the mean (section 2).
- *The metric I would choose*: WAPE on each store-item's weekly units, because it is weighted by volume and I review my orders by the week. For a hard order-up-to decision I would use a pinball loss at my service level, but no source fixes a service level, and MET-7 forbids inventing one.
- Under weekly WAPE the ranking moves. My 14-day plus weekday rule (0.1761) edges out LightGBM with the weather (0.1774). LightGBM without the weather (0.1736) and with lags (0.1638) stay ahead. So the TP-10 leg-1 margin depends on the metric. These models were fitted on log1p, so the comparison only hints at what a planner would see.
- This is a weighting preference, not evidence that RMSLE is biased or wrong for the use case, so I do not ask to overrule MET-4. A RMSLE restricted to the days within 3 of a storm would restore the competition's population, but at 62 rows from 2 stores in the thinnest window it is too thin to be the primary metric.

**Gaps between the dataset and the real decision, ranked by how much they change the task**
1. **The scope of the test (USE-1, USE-9, MET-2).** The use case is storm stocking. The windows are 84.5% non-storm days, and the weather carries no signal even near storms, so the shipped task is a routine week-ahead forecast from ids and the calendar. That is a real use case of its own (USE-9), but its fit stays approximate because of gaps 2 and 3. Rewording is not "rephrasing to excuse a gap" here: it describes what is scored.
2. **Censored demand (USE-5).** Unmarked stock-out and discontinued zeros make up 41.7% of the test rows. I would mask them with in-stock data I always have, but the release does not hold that data.
3. **Missing inputs I always have (USE-6, USE-10).** Inventory, price and promotions, and the product's identity are missing because of the anonymisation. The pair's recent sales are missing too, but measured worth only 0.6% RMSLE.
4. **A season and a sample (USE-8).** The test is one winter of nine weeks. The competition's test was spring to autumn, hurricanes included.
5. **The metric's weighting (MET-1).** RMSLE weighs slow movers and zeros heavily and rewards forecasting below the mean (section 5).
6. **Observed weather as a forecast (USE-3, USE-8).** It is declared, and it does no harm on these numbers because the models gain nothing from it.

**What an expert would change**
- **Reword `use_case` and `question` to what the windows test** (USE-1). For example: "A Walmart replenishment manager forecasts each carried product's daily units at a store for the coming week, storms included (about 15% of the test rows lie within 3 days of a storm), to set orders that avoid running out or overstocking (the competition's description names the days around storms)." Keep `fit="approximate"`, and add to `fit_reason` that the windows mostly test routine days.
- **Add to the metric notes** (MET-2, MET-11) that the competition's RMSLE scored only storm days within ±3 over all 4,995 pairs, 95% of them never-sold zeros. Our RMSLE scores every day of 231 carried pairs, so it cannot be compared with the leaderboard.
- **Optional, low priority (USE-10, TP-10 leg 2 allows trailing summaries).** Ship summaries of each pair's units lagged 7 days or more. I would not push it: the gain on the declared metric is small, and the house keeps the competition's input set (rossmann, ashrae).
- **Leave the zeros as recorded** (the curator's policy). An expert would mark long zero runs, but that reads the sales on both sides of a day, as the 1st place did, so it can be neither a feature nor a filter without selecting on the label.

**Sources**
- Kaggle Description, Data and Evaluation pages, saved by the builder in `pages_text.txt` in the run folder (not committed).
- Forum topics, saved in `pages/`: 14452 (1st place), 14113 (weather effect), 13299 (Pop-Tarts), 13322 (scope of the test windows), 13233 (item ids).
- C. Hays, "What Wal-Mart knows about customers' habits", NYT, 2004-11-14. Read through a course copy (https://www.bauer.uh.edu/cox/Documents/1.%20First%20Quiz/Chapter%204/Wal-Mart%20Data.docx) and AOL (https://www.aol.com/2019-09-09-the-strange-item-walmart-stocks-up-on-before-storms-23808315.html), not the original.
- Planalytics on weather-driven replenishment: https://www.planalytics.com/predictive-weather-driven-demand-retail-forecasts-inventory-replenishment/ (vendor material).
- Makridakis et al., "The M5 uncertainty competition", IJF 38(4) 2022: revenue-weighted scaled pinball loss for Walmart's quantile forecasts (https://doi.org/10.1016/j.ijforecast.2021.10.009).
- Walmart Recruiting I scored a WMAE with holiday weeks weighted 5, from secondary sources (https://github.com/arnab000007/Walmart-Store-Sales-Forecasting).
- Favorita's NWRMSLE, perishables weighted 1.25 (WaveNet paper, https://ar5iv.labs.arxiv.org/html/1803.04037).
- Builder report and `tp10_designB_summary.json` in the run folder (not committed).
- My probe: `probe.json` in the run folder (not committed).

</details>

<details><summary>Blind review</summary>

**Verdict: include with changes.** The data is real and copied exactly from the Kaggle "Walmart Recruiting II: Sales in Stormy Weather" source, and I found no leakage or duplicates. But as prepared, the task is mostly about learning each store-item's sales level from two integer IDs. It uses same-day observed weather and has no sales-history features, and a few columns are encoded loosely.

**What the task is.** The table has daily unit sales, as `log1p_units`, for 231 active store-item pairs (45 stores, 97 items) over 2012-01-01 to 2013-03-31. Each row is joined to that day's observations from the store's nearest weather station (20 stations). The real user would be a Walmart replenishment or demand planner deciding how much milk, bread or umbrellas to stock at a store around weather events. Using RMSE on log1p is the same as the competition's RMSLE metric. The temporal split matches how such a model would be used: score future days of known series.

**What I verified (passed)**
- Provenance and values. The Kaggle pages are behind a login and JavaScript, so I checked against the CTU Relational Repository mirror of the same Kaggle tables (train, weather, key), which has public guest access. The mirror's train table has 4,617,600 rows, which matches the Habr write-up's count for Kaggle train.csv. For stores 1, 22 and 35, all reconstructed units (expm1 of the target) match the source exactly, 100% of rows. All weather columns match for all 8,948 station-days. The one difference is trace precipitation: it is coded 0.005 here and 0.05 in the CTU copy. Here's coding is better because it keeps trace separate from a real 0.05 in (77 rows). The store-to-station key matches for all 45 stores.
- Why it stops at 2013-03-31. In the source, Kaggle removed the test (storm) windows from train only from 2013-04-01 onward. Every store has all 455 dates up to 2013-03-31; store 1, for example, then has gaps. So the cut keeps the complete prefix and avoids a sample with storm days systematically missing. That is a sensible choice.
- No duplicated (store, item, date) keys and no fully duplicated rows. 2012-12-25 is missing for every store (stores closed). Store 35 starts on 2012-06-01, which is also true in the source.
- The target comes from integer counts. 41% of rows are zero, the median is 2 units and the maximum is 5,568. The values are plausible. Weather ranges are plausible too (tmax -1 to 114 F, station pressure 23.75 to 30.55 inHg for high-altitude stations).

**Concerns, from most to least serious**

1. **Store-item identity dominates, and there are no sales-history features, so the benchmark mostly measures memorising series levels.**
   - Evidence:
     - A per-pair mean explains 90% of the variance in-sample (R^2 = 0.897); adding pair x month raises that only to 0.921.
     - Out of sample on temporal splits, the global mean has RMSE 1.78-1.80. The per-pair mean looked up from training has 0.62-0.65, and the pair x weekday mean has 0.617 / 0.642.
     - LightGBM with every column reaches only 0.605-0.637 on two 3-month windows.
     - On the March-2013 window, the plain mean of each pair over the last 28 training days (0.550) beats every LightGBM variant (0.556-0.593).
     - Adding lagged-sales features with a 35-day gap (mean of the pair's log sales over the 28 days ending 35 days earlier) lowered LightGBM's RMSE from 0.646 to 0.597 (Jan 2013) and from 0.556 to 0.528 (Mar 2013), with no gain in Oct 2012.
     - So the signal a real forecaster would use most, recent sales, is missing. What separates methods is how well they recover per-series levels and drift from `store_nbr` and `item_nbr`.
   - Change: Either add rolling lagged-target features whose gap is at least the longest test window (so no test target can feed a test row), or keep the table as is but describe it explicitly as "conditional demand given IDs, calendar and weather", not as forecasting. Also add an explicit pair key.

2. **Weather is the observed weather of the same day, not a forecast.**
   - Evidence:
     - Columns such as `preciptotal`, `snowfall`, `tmax`, `codesum` and `avgspeed` are totals or summaries over the whole calendar day of the sale. They are known only after the day ends.
     - A planner choosing stock would only have a forecast.
     - This matches the Kaggle setup (it gave observed weather for the test days), so it is not a construction error. It does make the weather columns "oracle" inputs.
     - The practical effect is small. With IDs and calendar features, adding weather moved LightGBM's RMSE from 0.640 to 0.607, from 0.651 to 0.637, and from 0.562 to 0.561. Part of that gain is temperature standing in for seasonality, which the model cannot learn from 15 months.
     - Habr's 15th-place write-up reports the same thing: weather "added little beyond noise", with pressure the most useful weather variable.
   - Change: Document the weather columns as realised same-day observations. If the benchmark wants a forecasting framing, shift weather by one day or more, or treat these columns as perfect forecasts and say so.

3. **Several columns have the wrong declared type or a loose encoding.**
   - `store_nbr` and `item_nbr` are int16 numerics, but they are nominal codes.
     - The competition text, as quoted in the Habr write-up, says a similar product may have different IDs in different stores. 69 of the 97 items are sold at only one store.
     - `station_nbr` (int64) is a deterministic function of `store_nbr`, so it is redundant.
     - In my runs, LightGBM actually did slightly better with numeric codes (0.640 vs 0.666). The point is to declare the semantics correctly, not that categorical encoding always wins.
   - `codesum`:
     - In the raw data, a blank `codesum` means "no notable weather". 11,051 of 20,517 raw station-days are blank, not missing.
     - Here those blanks became NA (58,785 of 104,041 rows are NA). That mixes "clear day" with truly missing data, which is real only for station 5.
     - It is also a free-text field with 293 distinct multi-token strings (BR, RA, SN, HZ, TSRA, FG+, ...).
   - `sunrise` and `sunset` are stored as minutes after midnight. That is fine, but 57% of rows are NA because only some stations report them.
   - Change:
     - Mark `store_nbr`, `item_nbr` and a new `store_item` key as categorical, and drop or flag `station_nbr`.
     - Code blank `codesum` as "none" and split it into binary token flags (RA, SN, TS, FG, BR, HZ, DZ, FZ, ...).

4. **Store 35 has no weather at all.** Station 5, which serves only store 35, is 100% missing on every weather column in this window: 2,121 rows over 7 pairs. In the source, station 5 has real readings only in September 2013. Change: keep the rows (tree models cope), but document this, or drop store 35 if weather is meant to be a core input.

5. **Choosing which store-item pairs to include used the whole window, including test periods.**
   - Evidence:
     - The 231 pairs are exactly the pairs with at least one sale in the window, minus pair (3,102), whose only 2 sales fall in March 2013. So the cutoff is probably slightly earlier than the end of the window, but it still lies inside the later test windows.
     - 18 pairs make their first sale after 2012-07-01 and 9 after 2012-10-01, for example (39,103) first sold on 2012-12-21. They are included because of sales that happen later.
     - In operations a store knows its own assortment, so this is a mild leak. It mainly adds pre-launch zero rows that the model is implicitly told belong to an active series.
   - Change: define the active-pair filter on data before the first test window, or document the filter.

6. **The history is short, and the "stormy" framing is diluted.**
   - With only 15 months, annual seasonality and holidays appear once (Thanksgiving 2012-11-22 is the main day on which whole stores show zero sales). The source runs to 2014-10-31, but storm-window gaps start in April 2013.
   - Only 2.6% of station-days are weather events by the competition's definition (more than 1 in of rain or 2 in of snow): 236 station-days.
   - The Kaggle task scored only the days around storms. Here every day is scored, so this is a general store-item daily demand task with weather covariates.
   - Change: keep the name, but don't present it as a weather-impact benchmark. Optionally add a storm-window flag for a sub-score, or extend to the full train period and accept the gaps.

**Is it worth benchmarking?** Yes, with the changes above. The table has 104,041 rows, and a 1-month window still holds about 7,000 test rows. Even the best models leave RMSE of about 0.55-0.65 in log units, so the task is far from trivial. Different reasonable models spread over roughly 0.55-0.67, so methods can be told apart. There is no class-imbalance style problem; the 41% zeros are a natural part of count demand.

**What I could not check**
- The Kaggle competition and data pages themselves, which need a login and JavaScript. I relied on the CTU mirror of Kaggle's train, weather and key tables and on the Habr write-up for the competition framing. I could not quote the official Kaggle description directly.
- The 9 test-window boundaries. task.md says only "temporal on date, 9 windows". With 455 days, that probably means windows of roughly one month in the second half of the period, but I could not confirm it.
- Whether the weather values match the original NOAA station records. I only compared against the CTU copy of the Kaggle file.
- I spot-checked units for 3 of the 45 stores (all 100% equal), not all of them.

**Sources:** https://www.kaggle.com/competitions/walmart-recruiting-sales-in-stormy-weather ; https://relational.fel.cvut.cz/dataset/Walmart ; https://habr.com/en/articles/264653

</details>

<details><summary>Precedent check</summary>

**Precedent check (precedent-checker, 2026-11-01)**

**Verdict:** most choices follow precedent. No precedent settles the scope call (SEL-10 and SEL-11 through TP-10, Must), and each of the builder's two options rests on a precedent that does not support it, so the call goes to the curator (issue 1). Two smaller choices depart from curator precedents without a written reason that settles them: the weather of days after the prediction point (LEAK-10, issue 2) and all nine windows in one season (SPLIT-20, issue 3). One choice keeps a value that a precedent dropped, for a reason the data shows but the notes do not state (the 5,568-unit spike, CLEAN-11, issue 4). There is no drift in the curator's decisions and no third exception of one kind.

Read: the decision register of this run (`register.md`, `register.json`), the records named below, the Cases tables of `task_probes.md`, `splits.md`, `cleaning_features.md` and `leak_checks.md`, and the policy calls of 2026-10-30 (`curation/inputs/two_regime_zero_triage_summary.md`). Measured here: storm days by month, the SPLIT-14 floor, the spike's pair history and the target's value shares (scratch script `storms_by_month.py` in the run folder (not committed)).

**Per decision**

| Decision | Status | Closest precedents |
|---|---|---|
| Scope: one tabular task, not forecasting (SEL-10, SEL-11, TP-10) | open: no precedent settles it, and both draft options misread the precedent they rest on (issue 1) | ashrae_great_energy_predictor_iii (in, 2026-10-15); g_research_crypto_forecasting (in, rule amended, 2026-10-22); rain_in_australia (in, rule amended, 2026-10-26); stock, appliances_energy_prediction (out, 2026-10-22); rossmann_store_sales (Yes, not reopened 2026-10-30); m5_forecasting_accuracy (2nd Tier, 2026-10-30); auto_intermittent_demand, car_parts_intermittent_demand, raf_aerospace_parts_demand (No, 2026-10-30) |
| Target `log1p_units`; `Metric.source("rmsle", target_transform="log1p")` (CLEAN-16, MET-3, MET-4) | consistent | ashrae (the same metric declaration, 2026-10-21), nyc_taxi_trip_duration_1m, mercari_price_suggestion; the metric tension row (a competition's metric is kept, zillow_prize) |
| Temporal regime, test pairs all seen in training (SPLIT-6, SPLIT-13) | consistent | ashrae (temporal, not grouped: the same buildings after the cutoff, Lennart 2026-10-15) |
| Windows of 7 days, 9 of them, no gap (SPLIT-12, SPLIT-14, SPLIT-18) | consistent | SPLIT-12 case (each task keeps its source's horizon, Lennart 2026-10-21); climate_model_weather_forecasting (weather windows of 1-2 weeks); train sides hold 86% or more of the rows |
| Window placement: nine contiguous weeks, 2013-01-28 to 2013-03-31 (SPLIT-15, SPLIT-20) | follows SPLIT-15's default; the SPLIT-20 season check is not written, and recent precedents spread their windows (issue 3) | perth_house_prices (`step=3`, Lennart 2026-10-26); rain_in_australia (windows over the last year, Lennart 2026-10-26); aeolus (one window of three in the holiday peak, 2026-10-12) |
| Period ends 2013-03-31 (SPLIT-15, SPLIT-19, SPLIT-20) | departs with a stated reason; a reasonable one | sf_permit_time (LEAK-24: cut where the data is complete); perth (chosen from counts, not scores); unreleased competition test labels mean windows from the training file (ashrae, rossmann) |
| Rows: pairs that sold before the oldest window (USE-7, CLEAN-1, CLEAN-7, CLEAN-20) | consistent | rossmann (closed days, all zero, dropped as trivial); CLEAN-7 case (a statistic taken from the history before the oldest window, Lennart 2026-10-19); the 1st place's rule, moved to history only |
| Zeros kept as recorded sales; stock-outs not marked (USE-5) | consistent | policy call 2 (Andrej, 2026-10-30, which names stock-outs: a cleaning choice, no reason for a No); remedy ladder (keep with a note); named in `fit_reason` |
| Each day's observed weather kept (LEAK-10, USE-8) | departs with a stated reason (the source's "perfect weather forecast"); whether that reason holds under the ranking is open (issue 2) | aeolus_1m (weather read after departure blanked); rain_in_australia (same-day readings after 9 am lagged); ashrae (observed weather kept, fit direct, because its use case is measured after the fact) |
| Trace "T" as half the reporting unit (CLEAN-10) | consistent within this run; no curator precedent | crms_phragmites_cover ("<1" cover as 0.5, same run, AI). ashrae kept ISD-Lite's trace code -1, but there the code was already a number; here it is a text token in a numeric column |
| Store 35's rows without weather kept (USE-7) | consistent | USE-7's second sentence (other inputs stay missing). bias_correction dropped rows without the forecast it corrects; here a station failed, and a manager still stocks the store |
| 5,568-unit spike kept (CLEAN-11) | departs from mercedes on a fact the data shows but the notes do not state (issue 4) | mercedes_benz_greener_manufacturing (a single extreme target in training, dropped, Lennart 2026-10-21) |
| Ids categorical, `codesum` string, sunrise and sunset in minutes (CLEAN-14, CLEAN-12) | consistent | ashrae (`building_id`, `site_id`), rossmann (`Store`); `codesum` holds 449 distinct code combinations |
| Tag `Two-Regime Zeros` (policy call 4, Andrej 2026-10-30) | consistent | 0 is 41.1% of the rows, 1 is 7.2%, 2 is 4.9%; the median positive is 24 |
| Record marker `Time-series (Forecasting)` next to `Yes` | follows from issue 1 | ashrae, g_research and rain carry no such marker once in scope; a `No` keeps it |

**Issue 1. The scope call (P2: SEL-10 and SEL-11 through TP-10, Must)**

| | Leg 1 (declared metric) | Leg 2: the source's top solutions | Leg 2: the columns | Inputs besides ids and date | Curator's call |
|---|---|---|---|---|---|
| walmart | LightGBM with 1,000 trees 3.5% below the best own-series forecast (that forecast picked on the windows), ahead in 7 of 9 windows, about 2.8 paired SE; with 100 trees a tie (4 of 9) | 1st place: a curve per pair over time, then a lasso; 5th: a Gaussian process per pair; 3rd: pooled xgboost with no lags. The competition's test days sat inside the training period | no lag of the target | weather, which adds nothing (0.5201 against 0.5209 without it) | `Yes` with TP-10 still to run (Andrej, 2026-10-30) |
| ashrae | 7.6-10.9% below a seasonal naive forecast, every window; the default model loses | top five pooled, with no lagged readings | none | building metadata, weather | in (Lennart, 2026-10-15) |
| g_research | every 95% interval above the coin's mean | top three: LightGBM on trailing returns | trailing returns | 18 market features | in, TP-10 amended (Lennart, 2026-10-22) |
| rain_in_australia | ROC AUC 0.849 against 0.752, 9 of 9 windows | no competition | the last observation, kept by an amendment | weather observations | in, TP-10 amended (Lennart, 2026-10-26) |
| rossmann | not run | not read | none | promotions, holidays, store type and assortment, competitor | Yes; "not reopened" (policy call 6, Andrej 2026-10-30) |
| m5 | 4.5% against Croston's method (the AI called this "thin") | recursive lags of the target (the organisers' report) | n/a | prices, events | 2nd Tier: "would just need more evidence to decide how to treat the time series aspect" (Andrej, 2026-10-30) |
| auto, car_parts, raf | not run | n/a | n/a | none | No (Andrej, 2026-10-30) |

* Draft issue 1's "forecasting like M5" does not support a `No`. The curator overruled the AI's `No` on M5 and set `TBD -> 2nd Tier`. M5 also fails on another fact: its winners lagged the target recursively, which TP-10 excludes by name. Neither walmart's top solutions nor its columns lag the target.
* "Like ashrae" does not support a `Yes` on its own. ashrae passed both legs as written. walmart's leg 1 margin is the narrowest of any case kept in scope, and its leg 2 top-solution clause fails for the 1st and 5th place. In this run crms_phragmites_cover (5.8%, ahead in 8 of 9, against unfitted forecasts) leaves the bar to the curator.
* TP-10 is a Must, so keeping walmart cannot be an exception. It needs either a written reading under which leg 2 holds, or an amendment. That would be the third change to TP-10's leg 2 in ten days, each made to keep one panel, so the wording should be general.
* Retiring it departs from rossmann_store_sales, a store-day sales panel with a forecasting use case ("forecast their daily sales up to six weeks ahead") that has never had TP-10 run. The fact that sets them apart: rossmann's inputs include drivers known in advance, while walmart's only non-id input carries nothing measurable. Without the weather, walmart's inputs hold what the intermittent-demand series hold (a series id and a date), and those were retired on 2026-10-30. Lennart's phrase for stock and appliances ("context and data state") was applied to datasets that were not probed again; walmart has been probed.
* Drift: none. Andrej's calls of 2026-10-30 follow one line: pure series out, store-sales panels kept open until the evidence is in (m5, walmart, and metro_manila: "Test the leg, then decide.").
* SPLIT-21 guard: leg 1 is clearer on the period that does not ship (autumn 2014: 0.375 against 0.395, ahead in 9 of 9). The period (draft issue 2) is chosen from the use case, never from this difference (aeolus, Lennart 2026-10-12).
* Method gap: TP-10's method also asks whether models split by entity type beat one pooled model (ashrae ran models per site and per building). The builder reports only the pooled model.

**Consistency check (AI, 2026-11-01):** your `Yes` on walmart (2026-10-30, "Do yes and then we can see what happens") now meets TP-10's result. Leg 1 holds by 3.5% (ahead in 7 of 9 windows), a thinner margin than ashrae, g_research or rain had. Leg 2's top-solution clause fails for the 1st and 5th place (curves per pair) and holds for the 3rd. Keeping it departs from TP-10 as written, a Must; retiring it departs from rossmann_store_sales (Yes, not reopened on 2026-10-30). What decides it?
(a) The competition tested days inside its training period, so the winners' curves per pair read the sales on both sides of each test day. In forward windows the best own-series forecast loses to the pooled model, and nothing lags the target. Keep it, amend TP-10's leg 2 in words (the top solutions count when the source's test looks ahead; otherwise leg 1 carries the test), and add walmart as a Cases row.
(b) Treat walmart like stock, appliances_energy_prediction and the intermittent-demand series: `No` + `Time-series (Forecasting)`, with the fact that sets rossmann apart (drivers known in advance, against a weather that carries nothing) written in both records.
(c) Reopen rossmann_store_sales for TP-10, so that both store-sales panels are judged by the same test.
(d) `TBD -> 2nd Tier`, like m5_forecasting_accuracy, until the store-sales panels share one reading of leg 2.

**Issue 2. The weather of days after the prediction point (P4: LEAK-10, Must; USE-8)**

The prediction point is the start of a week, but each row holds its own day's observed weather, up to six days later. On this mechanism the precedents removed the late values: aeolus_1m blanked weather that the release had read after departure (LEAK-10's clause, amended 2026-10-26), and rain_in_australia lagged the same-day readings taken after 9 am (with them ROC AUC was 0.902, without 0.849). ashrae kept observed weather, but its use case (measuring retrofit savings) comes after the fact, so the weather existed at the prediction point (fit direct). walmart's use case looks ahead. The definition calls the weather a stand-in for a perfect forecast (the source's own words) and lists that as a gap of the fit. Two facts set walmart apart: the join is the source's declared design, not a late read, and the weather carries no signal (0.5201 against 0.5209 on all windows; 0.653 against 0.640 on the storm rows). USE-8 says a potential leak kept on purpose is named as kept, not as a gap of the fit. What is open is the label, not the score.

**Consistency check (AI, 2026-11-01):** walmart keeps each day's observed weather for a prediction made at the start of the week. aeolus_1m blanked weather from after its prediction point, and rain_in_australia lagged its readings from after 9 am (LEAK-10). What sets walmart apart?
(a) The source hands the weather over as "a perfect weather forecast", and it carries no measurable signal. It stays, with a `Potential leak, kept on purpose:` note and the fit gap reworded.
(b) Treat it like aeolus: drop the weather columns (no score is lost) or move the prediction point to the day itself.
(c) Reopen aeolus or rain: not apt, since both measured a gain.
(d) Amend LEAK-10: a perfect forecast of an outside driver, declared by the source, may stay if named.

**Issue 3. All nine windows in one season (P4: SPLIT-20, Should)**

The windows (2013-01-28 to 2013-03-31) hold 65 of the complete period's 490 storm store-days (13%). 40% of those 65 are snow, against 9.6% over the period. Storms peak with summer rain (85 store-days in June 2012, 74 in August). SPLIT-14's 50% floor allows windows back to 2012-08-17, and August 2012 to March 2013 holds 226 storm store-days. The definition cuts the period to keep storms in the windows. Its `splits_comment` gives reasons for the windows' length and end date, but none for their placement. Precedents: perth_house_prices spaced its windows so most fall outside an atypical period, chosen from counts and not scores (Lennart, 2026-10-26); rain_in_australia spread its windows over the last year (2026-10-26).

**Consistency check (AI, 2026-11-01):** walmart's windows are nine contiguous late-winter weeks, while perth_house_prices and rain_in_australia spread theirs (SPLIT-20). What sets walmart apart?
(a) A weekly replenishment model is refit every week, and these are the newest complete weeks (SPLIT-15's default). Keep them, and name the season and the storm mix in `splits_comment`.
(b) Treat it like perth: nine 7-day windows stepped back from 2013-03-31, the oldest no earlier than 2012-08-17, chosen from counts only (SPLIT-21).
(c) Not apt.
(d) Amend SPLIT-20 to say when windows are spread.

**Issue 4. The 5,568-unit spike kept (P7: CLEAN-11, Should)**

mercedes_benz_greener_manufacturing (Lennart, 2026-10-21) dropped a single extreme target that sat in every training side, where the host was silent and the community had pointed it out. As the notes describe walmart's spike, it has the same facts, yet it stays. One fact the notes leave out sets it apart: store 37 and product 5 also sold 3,369 units on 2013-11-21. Both dates are the Thursday one week before Thanksgiving (2012-11-22 and 2013-11-28), and the pair's next highest values are 154 and 129. The same day before the same holiday reads as a recurring order, not a typing error. The forum post's "two of them" are these two spikes. The second falls after 2013-03-31 and does not ship. Recommendation: add this fact to the anomaly bullet as the reason to depart from mercedes. If the curator prefers mercedes's treatment, drop the row (CLEAN-11 allows it).

**Side notes for the panel**

* The notes and the builder's report give the leg 1 baseline as "the best of 13" own-series forecasts, but `tp10.py` in the run folder (not committed) and `tp10_designB_summary.json` in the run folder (not committed) hold 11 (10 plus the zero forecast). This is for the claim auditor.
* The record's older paragraph ("No as forecasting, as for m5_forecasting_accuracy") and the screening's sibling line ("proposed `No`") were written before the curator's call on M5. Cite M5 as `TBD -> 2nd Tier`.

</details>

<details><summary>Advocate</summary>

**Advocate, opening brief (advocate, 2026-11-01): walmart_sales_in_stormy_weather**

**Position: ship after changes.** The changes are fixes to the text, two small changes to the definition (a one-day gap
and the `codesum` blanks), and the curator's reading of TP-10's leg 2. The evidence agents found no validity problem
that the definition or the notes cannot fix. One new fact from me: TP-10 leg 1 still holds with a one-day planning
gap (script and output in the run folder (not committed), `gap1.py` and `gap1.csv`).

**1. The task is valid at P3 to P5, and the metric is the source's.**
- *Claim:* the use case is real, the data is faithful, no feature comes from the sales, and the metric is the
  competition's.
- *Evidence:*
  - The host names the actor and the decision: "difficult for replenishment managers to correctly predict the level
    of inventory needed to avoid being out-of-stock or overstock" (claim audit row 2).
  - The blind reviewer checked the data against the CTU mirror. Units match on 100% of rows for 3 stores, the weather
    matches on all 8,948 station-days, and there are no duplicate keys.
  - No feature comes from the sales. The pair filter reads only days before 2013-01-28 (rows 9 and 44), and no rows
    are copied across the split (0.0%, row 43).
  - RMSLE is the leaderboard metric (row 24) and can be computed on all 9 folds (row 26). After the never-sold pairs
    are dropped it ranks models exactly as the competition did, since those pairs are 95% of the competition's test
    rows and score 0 for anyone who predicts 0 (row 27).
  - 45 of 55 claims hold, and no validity claim is refuted.
- *Rules:* USE-1 (Must); P5 (PROV); LEAK-10, LEAK-29 and CLEAN-7 (Must); MET-2 (Must); MET-4 (Should; the
  metric tension row keeps a competition's metric, as for zillow_prize). The Kaggle licence is "no reason and no
  marker" (selection.md, Ethics, licence).
- *Why it outranks the objections:* every objection below is either a reading of P2, a P4 fix in the definition, or
  P7. None of them removes this base.

**2. TP-10 leg 1 holds on the shipped windows in every run: without the weather, on the near-storm rows, and with a
planning gap.**
- *Claim:* a pooled model on the features clearly beats each pair's own-series forecast, measured by the declared
  metric.
- *Evidence:* RMSLE over the 9 shipped windows, with SE paired over the windows.

| run | model | best own-series forecast | lead | windows ahead |
|---|---|---|---|---|
| builder, LightGBM 1,000 trees | 0.5201 | 0.5389 (14-day mean + weekday) | 3.5%, 2.8 SE | 7 of 9 |
| claim auditor, against the strongest own-series forecast (7-day EWMA + weekday), 3 seeds | 0.5212 | 0.5353 | 2.65%, 2.5 SE | 7 of 9 |
| claim auditor, calendar only (no weather) | 0.5213 | 0.5353 | 2.6%, 3.4 SE | 7 of 9 |
| split auditor, only the rows within 3 days of a storm | 0.5505 | 0.5695 | 3.3%, 2.0 SE | 6 of 9 |
| mine, a one-day gap on both sides, calendar only | 0.5263 | 0.5391 (EWMA, gapped) | 2.4%, 2.6 SE | 8 of 9 |
| mine, a one-day gap, with weather, 2 seeds | 0.5272 | 0.5391 | 2.2%, 1.95 SE | 7 of 9 |

- *Rules:* TP-10 (Must), through SEL-11 (Must; narrows SEL-10). Leg 1 is measured "on the shipped windows" and "by the
  task's declared metric".
- *The objections it answers:*
  - (a) "The margin is thin." It is narrower than ashrae's (7-11%), and I concede that. But "clearly" holds at 2 to
    3.4 paired SE and 7 or 8 of 9 windows, against all 17 own-series forecasts tried (11 by the builder, 6 by the
    claim auditor). ashrae shows the same pattern: the default LightGBM loses and the model with 1,000 trees wins
    (TP-10 Cases). Here 100 trees tie (4 of 9) and 1,000 trees win.
  - (b) "Under weekly WAPE the naive rule wins" (practitioner). WAPE is not the declared metric, and the leg names
    the declared metric.
  - (c) "With integer ids the lead falls to 4 of 9" (split auditor). The definition declares the ids categorical
    (CLEAN-14), and that is what the benchmark feeds the models.
  - (d) "On a March window a 28-day mean beats LightGBM" (blind reviewer). That used 1- to 3-month windows, not the
    shipped 7-day windows.

**3. Leg 2: no column lags the target, and the source's best pooled solution is our setup. Where the top solutions
read the series, they read both sides of each test day.**
- *Concession:* as written, the top-solution clause is not met for the 1st and 5th places. They fit a curve per pair
  over time and a Gaussian process per pair, and the 1st place also flagged days "where both sides are many successive
  zeros". TP-10 is a Must, so this cannot be an exception. It needs the curator's written reading or an amendment.
- *Evidence for the reading:*
  - The columns hold no lag of the target, so that half of leg 2 is met as written.
  - The 3rd place used bagged xgboost on store, product, date parts and weather, with no lag (claim audit row 14).
    That is exactly our setup.
  - The competition's test days sat inside its training period (the record; `splits_comment`), so the per-pair curves
    interpolated between known days. In forward windows, the own-series forecasts that stand in for those methods lose
    (point 2).
  - The amended rule already says "Leg 1 then carries the test: the model must clearly beat the forecasts built from
    the series itself", and "such 'tabular forecasting' tasks exist where people want to generalise across entities".
    Here one pooled model beats the 231 pairs' own series.
- *Treat like cases alike:*
  - rossmann_store_sales is `Yes`, not reopened (policy call 6). It is a store-day sales panel with no lags, and it
    was never probed. Retiring the panel that was probed and passed leg 1, while keeping the unprobed one, puts a
    reading ahead of a measurement (EV-2; under Precedence, a later stage's measured finding supersedes an earlier
    reading).
  - m5 does not bind: its winners lagged the target recursively, which TP-10 excludes by name (precedent checker).
  - The intermittent-demand series were retired by context, without a probe.
  - The curator's CC of 2026-10-30 says "Do yes and then we can see what happens". What happened is that leg 1
    passed.
- *Mildest remedy:* the precedent checker's option (a). Keep the dataset, write leg 2's reading in general words (the
  top solutions count when the source's test looks forward; otherwise leg 1 carries the test), add walmart as a Cases
  row, and drop the `Time-series (Forecasting)` marker.

**4. The observed weather stays with a note. If the curator prefers the aeolus treatment, dropping it costs nothing
and the dataset stays.**
- *Evidence:*
  - The source hands the weather over as a forecast on purpose: "it's as though you have a perfect weather forecast at
    your disposal".
  - Weather is an outside driver. It does not depend on the day's sales, so it is not "a same-day value that depends
    on the day's outcome" (LEAK-10's list).
  - It gains nothing measurable, and sometimes loses: -0.0001 RMSLE on all rows (SE 0.0031); +0.0059 (worse) within 3
    days of a storm; nothing more when the weather of days t-3 to t+3 is added (claim audit row 8).
  - Weather missingness carries no outcome signal (column auditor).
- *Rules:*
  - LEAK-10's first sentence (Must) is triggered for days 2 to 7 of each week.
  - LEAK-6 (Must): "a slight optimism with a known cause can stay with a note; a confirmed leak goes even when small".
    Nothing is confirmed here. aeolus_1m was a late read with "a confirmed small leak".
  - USE-8 (Must) names such a keep "as kept, not as a gap".
- *Mildest remedy (the remedy ladder puts a note before a drop):* a `Potential leak, kept on purpose:` note in
  LEAK-38's format that names the difference from aeolus, and a reworded `fit_reason` that lists the weather as kept.
- *Next remedy:* drop the 16 observed weather columns and keep `sunrise` and `sunset`. That does not weaken point 2:
  calendar-only LightGBM leads by 2.6% (3.4 SE). The tension row "a real task against a leak" says to fix the leak and
  keep the task.

**5. The split is right. The mismatch in the scored rows is fixed in the text.**
- *Evidence:*
  - The entities are known store-products in a daily stream (USE-10, Must). All test pairs are seen in training
    (SPLIT-13).
  - The period was chosen from counts, not scores (SPLIT-21, Must, holds). From April 2013, 778 of the 799 storm
    store-days are in the encrypted test. The design that uses the whole file would test on only 79% of store-days,
    selected by the weather.
  - The source's own split cannot be rebuilt: 0 of its 4,747 test store-days are in train.csv. So the departure from
    SPLIT-19 is forced.
- *Issue A (split auditor; USE-1 and SPLIT-1, Must):* the use case says "days around a storm", but the windows score
  every day, and only 15.5% of test rows are near a storm. The model order is the same on both populations:
  - every day: model 0.5211, naive 0.5389;
  - near-storm rows only: model 0.5505, naive 0.5695.

  Filtering to the near-storm rows would leave windows of 62 and 69 rows from 2 stores, which the practitioner finds
  too thin for the primary metric.
- *Mildest remedy:* reword `use_case` and `question` to "each day of the coming week, storms included". Under USE-9
  (Should), weekly replenishment of carried items is a use case practitioners have, and the practitioner says this
  wording "describes what is scored". The fit stays approximate because of the stock-out zeros. Record an exception
  to SPLIT-19 with the facts: the labels were never released, and storm-only windows are too thin.
- *Why it outranks the filter:* both fix USE-1. The rewording keeps 6.5 times the test rows and changes no reading.

**6. The gap, the season, the discontinued item and the zeros are Should-level questions, fixed in the definition or
the notes.**
- *Gap (SPLIT-10, Should: "a planning gap the use case has ... is a gap too"; rossmann ships `gap=1`):* accept
  `gap=1`. Leg 1 still holds with it (point 2, my runs).
- *Season (SPLIT-20, Should):*
  - The windows are the newest complete weeks (the default of SPLIT-11 and SPLIT-15), and they cannot move later.
  - A spread design is possible within SPLIT-14's floor (precedent checker, option b), but it puts holiday weeks with
    no earlier year into the test (split auditor).
  - The milder remedy is a sentence in `splits_comment`: the windows are late winter, and 40% of their storms are snow,
    against about 6% over the year.
- *Item 93 (discontinued 2013-02-21):* these are real zeros that a manager faces. Dropping a pair's rows after its
  last sale would read the future. Note it.
- *Stock-out zeros (USE-5):* the curator's policy call 2 (Andrej, 2026-10-30) settles this, and `fit_reason` names
  the gap. A curator's decision outranks an AI assessment (Precedence).

**7. The cleaning and the notes are P7 and writing: cheap fixes, and none touches the verdict.**
- *`codesum`:* write a blank as the literal `none` at the stations that report weather types, and leave station 5
  missing (CLEAN-10, Should).
- *Corrections to the notes:*
  - the station 5 count;
  - cite the trace threshold to the units and forum topic 13200;
  - "13 forecasts" becomes 11;
  - "all days in the training file" becomes "none in the competition's test file";
  - the leg-1 numbers: against the strongest own-series forecast (2.6%), and unclipped;
  - add the survey requirement to `download_description`;
  - drop "the host did not answer".
- *The 5,568-unit spike:* add that the same store and item sold 3,369 units on 2013-11-21. Both days are the Thursday
  a week before Thanksgiving. That fact sets it apart from mercedes (CLEAN-11, Should).
- *Blind reviewer points the definition already meets:* the ids are declared categorical, and the pair filter reads
  only the history.
- *Lag features:* optional. TP-10 allows trailing summaries, but the practitioner measured a gain of only 0.6%, and
  rossmann and ashrae ship none.
- *Rule:* the tension row "a real task against imperfect cleaning (P3 over P7): keep the task; fix what is cheap and
  safe".

**Judgment record (advocate)**

```text
Verdict: ship after changes.
Validity: USE-1 holds once use_case says every day (USE-9); LEAK-10 triggered by the weather of days 2-7, kept with a
  note (no measured gain, LEAK-6) or dropped at no cost; SEL-10/SEL-11 through TP-10: leg 1 holds (2.2-3.5%,
  2-3.4 SE, 7-8 of 9 windows, also without weather and with a one-day gap), leg 2 needs the curator's reading (a);
  USE-10, SPLIT-1, SPLIT-21 hold; SPLIT-19 exception (labels never released).
Value: MET-2, MET-3, MET-4 hold.
Quality: CLEAN-10 codesum fix; CLEAN-11 spike kept with the Thanksgiving fact; notes corrected.
Definition changes: gap=1 (SPLIT-10). Notes: season and item 93 (SPLIT-20).
For the curator: the reading of TP-10 leg 2 (an amendment in general words); keep the weather with a note or drop it.
```

</details>

<details><summary>Critic</summary>

**Critic, opening brief (critic, 2026-11-01): walmart_sales_in_stormy_weather**

**Verdict: do not ship now.** Read as written, TP-10 is failed: leg 2 fails, and leg 1 holds only narrowly. The task
the windows score is daily store-item sales over a 7-day horizon, predicted from two ids, the date and a weather that
adds nothing. That is SEL-10's own example. The mildest course that breaks no Must is `TBD -> 2nd Tier`, the treatment
m5_forecasting_accuracy got on the same question. The other course is `No` + `Time-series (Forecasting)`. If the
curator amends TP-10 and keeps the dataset, it should ship only after points 2 to 6. I checked the leg-1 numbers
against the claim auditor's `tp10_attack.csv` and the split auditor's `models.csv`. Everything else below comes from
the phase A reports.

**1. Scope: TP-10 does not clearly pass (P2: SEL-10, and SEL-11 through TP-10; Must)**
- *Problem.* SEL-10 puts "demand, sales ... over a horizon" out of scope. SEL-11 lets a panel in only when both legs
  of TP-10 hold.
- *Leg 1 (a model on the features clearly beats each pair's own-series forecast on the shipped windows, scored with
  RMSLE).*
  - The claim auditor found a stronger own-series forecast: an EWMA level with a 7-day half-life plus the weekday
    offset. It scores 0.5353, against 0.5212 for LightGBM (1,000 trees, 3 seeds). That is a 2.65% lead, paired SE
    0.0057. The model is ahead in 7 of 9 windows and behind in the weeks of 2013-02-11 (+0.008) and 2013-02-18
    (+0.013) (claim-auditor row 13c; I recomputed this).
  - Default LightGBM (100 trees) ties the builder's baseline: 0.5381 against 0.5389, ahead in 4 of 9.
  - Read the ids as integers and the weather model is ahead in only 4 of 9 windows (split-auditor, side note).
  - Every panel kept in scope cleared a far higher bar. ashrae led by 7.6-10.9% in every window. rain_in_australia
    won 9 of 9 windows (0.849 against 0.752). g_research had every 95% interval above the baseline.
  - Fairly stated: the own-series forecasts were picked on the windows, which flatters them a little. Even the
    builder's pick gives only 3.5%, still the narrowest margin of any case kept.
- *Leg 2 (the top solutions are tabular models on point-in-time features).*
  - It fails for the 1st place: a curve of log1p units against the day for each pair, then a lasso on calendar terms
    ("weather features are not effective almost at all", topic 14452).
  - It fails for the 5th place: a Gaussian process per pair on time.
  - It holds only for the 3rd place (claim-auditor row 14).
- *Method not complete.* TP-10's method also asks for models per entity type and for a naive forecast from the same
  season a year earlier. Neither was run (task_probes.md, "A forecasting-like task"; precedent-checker).
- *Precedents.* Without the weather, the inputs are a series id and a date. That is what auto_intermittent_demand,
  car_parts_intermittent_demand and raf_aerospace_parts_demand held, and all three were set to `No` (Andrej,
  2026-10-30). m5 (Walmart again, the same question) is `TBD -> 2nd Tier`. rossmann differs: its drivers (promotions,
  holidays, store type) are known in advance.
- *Effect.* The score would mostly measure how well a model recovers each pair's level and weekday pattern from two
  ids. That is forecasting skill.
- *Rule.* TP-10 is a Must. Keeping the dataset cannot be an exception, only an amendment (principles.md, "Exceptions
  and amendments").
- *Remedy.* No change to the definition fixes this. Trailing summaries, which leg 2 allows, were worth 0.6% RMSLE
  (domain-practitioner) and leave leg 2 as it is.
  - Hold at `TBD -> 2nd Tier`, as m5, until one reading of leg 2 covers the store-sales panels. Rossmann should be
    reopened for the same test (precedent-checker, options c and d).
  - Or set `No` + `Time-series (Forecasting)`.
  - If the curator amends leg 2 (the source's test days sat inside the training period, so curves per pair could read
    both sides of each test day), leg 1 alone carries the test. Then the curator must weigh 2.6%, with 2 windows lost,
    against the word "clearly".

**2. The score does not measure the decision the use case names (P3 and P4: USE-1 and SPLIT-1, Must; SPLIT-19,
Should; MET-2, Must)**
- *Problem.* The `use_case` says the manager "sets the stock ... for the days around a storm", and the source scored
  "a window of ±3 days surrounding each storm". Our windows score every day. Only 2,254 of 14,553 test rows (15.5%) lie
  within 3 days of a storm at the store's station, and 351 (2.4%) are storm days (split-auditor A; the claim auditor
  counts 14.9%).
- *Effect.* About 85% of the score is a routine week-ahead forecast. The text of the task contradicts what is scored.
  The model order is the same under both populations (split-auditor A), so this changes what the score means, not the
  TP-10 reading.
- *Remedy: fix the definition, one of two ways (the curator's call).*
  - (a) Score only the store-days within 3 days of a storm in each window. This is the source's population and
    SPLIT-19's default. It gives 62 to 616 rows per window; the oldest window has 62 rows from 2 stores.
  - (b) Rewrite `question`, `use_case` and `split` to "every day of the coming week, storms included", and record an
    exception to SPLIT-19 with the fact that sets this case apart. Option (b) drops the one feature of the task that
    separates it from a plain sales series, which bears on point 1.
  - Either way, add to the metric notes that the leaderboard's RMSLE cannot be compared with ours: it covered only
    storm days, over all 4,995 pairs, 95% of them trivial zeros (domain-practitioner; MET-2).

**3. Weather from days after the prediction point (P4: LEAK-10, Must, weak; LEAK-6; USE-8)**
- *Problem.* The prediction point is the start of the week, but 16 weather columns hold each day's observation, up to
  6 days later. Only `sunrise` and `sunset` are computed in advance (column-auditor problem 1).
- *Effect.* None measurable. Weather minus calendar is -0.0001 (SE 0.0031) on all rows, and the weather makes the
  rows near storms worse (+0.0059, SE 0.0089) (claim-auditor row 8). Still, it did not exist at the prediction point.
  rain_in_australia lagged its same-day readings from after the prediction point (Lennart, 2026-10-26).
- *Rule.* LEAK-6 lets a slight optimism with a known cause stay with a note. USE-8 says a potential leak kept on
  purpose is named as kept, not as a gap of the fit. The definition does neither: `fit_reason` lists the weather as a
  gap, and there is no `Potential leak, kept on purpose:` note.
- *Remedy.* Add the note in LEAK-38's format: the mechanism, the numbers above, why it stays (the source's "perfect
  weather forecast", and no gain) and when to revisit. Reword `fit_reason` to match. Put the consistency question
  against rain_in_australia and aeolus_1m to the curator. Dropping the columns costs no score, but it leaves only ids
  and the calendar, which settles point 1.

**4. No planning gap (P4: SPLIT-10, Should)**
- *Problem.* The train side ends the evening before the week starts, but stock for Monday is ordered before Monday.
  SPLIT-10: "A planning gap the use case has (a forecast made a day ahead) is a gap too."
- *Evidence.* rossmann_store_sales ships `gap=1` "as a planning gap" (its dataset.py, l.95). A 2-day gap raises
  LightGBM's RMSLE by 0.0083 (SE 0.0024) and makes it worse in 8 of 9 windows (split-auditor B). So the last days
  before a window carry real information.
- *Remedy.* `TemporalSplits(window=7, unit="days", n_windows=9, gap=1)` and one sentence on the order lead time. Or
  write down the fact that sets this case apart from rossmann.

**5. The test season, and a break inside the windows (P4: SPLIT-20, Should)**
- *Season.* All nine windows are late winter. 40% of their storm store-days are snow, against 6.1% outside the
  windows. April to September holds 68% of the storm store-days, and none of them is tested (split-auditor C). The
  competition put 438,228 of its 526,917 test rows in April to October (domain-practitioner).
- *Break.* Item 93 (12.5% of rows) sells for the last time on 2013-02-21. In each of the five newest windows, 203 rows
  (12.6%) are zeros of a discontinued product (split-auditor D).
- *Effect.* A storm benchmark that tests no summer storm, and newest windows that partly score guessing when a product
  ends.
- *Remedy.* Notes in `splits_comment` and in the zeros bullet. Spreading the windows like perth_house_prices is the
  curator's consistency call (precedent-checker issue 3), to be chosen from counts, never from scores (SPLIT-21).

**6. Cleaning and wrong notes (P7 and EV; quality, no reason to exclude)**
- `codesum`: a blank becomes missing. That merges "no phenomenon" with "not reported" (station 5's 2,121 rows) and
  also covers 1,337 rows with measurable rain but no code (CLEAN-10, Should; column-auditor 2, claim-auditor 16c).
  Map a blank to `none` at the stations that report weather types, and leave station 5 missing.
- TP-10 notes (EV-7, EV-8):
  - "best of 13" should be 11;
  - the probe clips at 0 and the scorer does not (0.5389 clipped, 0.5404 unclipped);
  - add the EWMA baseline and the 2.6% margin.
- The station 5 bullet is wrong: the 822 days are the count for the temperature and precipitation columns. In our
  period, store 35's rows have only the computed sunrise and sunset (EV-7).
- The trace thresholds are cited to the NOAA PDF, which says only "T = TRACE". Cite topic 13200 or the units (EV-2).
- "the only period whose days are all in the training file" is wrong: 197 store-days are in neither file. Write
  "none of whose days are in the test file" (EV-7).
- The 5,568-unit spike: add that the pair also sold 3,369 units on 2013-11-21, the same Thursday before Thanksgiving
  week. That is the fact that sets it apart from mercedes_benz_greener_manufacturing (CLEAN-11; precedent-checker
  issue 4). Drop "the host did not answer", which no one could check.
- `download_description`: the rules say the Walmart Recruiting Survey unlocks the zip.
- Record: the older paragraph still cites m5 as `No`. Its status is `TBD -> 2nd Tier`.

**Judgment record**

```text
Verdict: do not ship now; TBD -> 2nd Tier (as m5) or No + Time-series (Forecasting). If TP-10 is amended and the
  dataset kept, ship after points 2-6.
Validity: SEL-10/SEL-11 via TP-10 (Must) fails as written: leg 2 fails (1st and 5th place model each pair's series);
  leg 1 narrow (2.65% under an EWMA own-series forecast, 7/9; default model ties; 4/9 with integer ids). USE-1/SPLIT-1
  triggered (storm use case, every-day score, 15.5% near storms): fix by a test filter, or by a rewrite plus a
  SPLIT-19 exception. LEAK-10 weak: keep with a note (no gain). SPLIT-10 departure with no fact given (rossmann
  gap=1). SPLIT-20 notes (late winter; item 93).
Value: TP-10 leg 1 as above; MET-2 holds with a note (not comparable to the leaderboard).
Quality: CLEAN-10 codesum; notes to correct (EV-7, EV-2, EV-8); CLEAN-11 fact to add.
Weighed: source +, named actor +, size +; signal beyond ids and calendar -; storm premise untestable -.
For the curator: point 1, the scope call (amend TP-10 or not); point 2, filter or rewrite.
```

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate, rebuttal (advocate, 2026-11-01): walmart_sales_in_stormy_weather**

**Position: changed. I no longer argue for `Yes` now. I accept the critic's hold, `TBD -> 2nd Tier` as m5, with the
agreed changes made, and I argue against `No`.** Two new checks decided this. I finished TP-10's method, which the
critic said was incomplete. I also gave the model the trailing summaries that leg 2 allows and scored it against the
critic's own-series forecast picked on validation weeks, at `gap=0` and at the agreed `gap=1`. Scripts and outputs are
in the run folder (not committed): `method.py`, `method_0-1-2-3-4.csv` and `method_5-6-7-8.csv`; `trailing.py`,
`trailing_gap0.csv` and `trailing_gap1.csv`; `compare_trailing.py` and `compare_trailing.txt`. As a harness check, my
`cal_weather` run at `gap=0` gives 0.5211, the critic's figure, and my recomputed validation pick equals the critic's
`own_series_test.csv` in every window.

**New fact 1: TP-10's full method (pooled LightGBM, 1,000 trees, seed 0; RMSLE over the 9 shipped windows).**

| forecast | RMSLE | pooled model ahead |
|---|---|---|
| pooled LightGBM, calendar + weather | 0.5211 | |
| one LightGBM per store | 0.5535 | 9 of 9 (pooled 5.8% better, 5.4 SE) |
| one LightGBM per product | 0.5587 | 9 of 9 (6.7%, 10.5 SE) |
| same season a year earlier, plus the change in level | 0.7262 | 9 of 9 (28%) |
| same season a year earlier | 0.7865 | 9 of 9 |
| last same weekday / last value | 0.6989 / 0.7220 | 9 of 9 |
| critic's validation pick (EWMA 10 days + half the weekday offset) | 0.5323 | 6 of 9 (2.1%, 1.8 SE) |

**New fact 2: leg 1 with trailing summaries, against the validation pick, gapped the same way.**

| definition | model | RMSLE | lead | paired SE | windows ahead |
|---|---|---|---|---|---|
| gap 0 (validation pick 0.5323) | calendar + weather (as shipped) | 0.5211 | 2.1% | 1.8 | 6 of 9 |
| | calendar + weather + trailing | 0.5196 | 2.4% | 2.4 | 6 of 9 |
| | calendar + trailing | 0.5177 | 2.75% | 3.1 | 7 of 9 |
| gap 1 (validation pick 0.5358) | calendar + weather (as shipped) | 0.5285 | 1.4% | 1.2 | 6 of 9 |
| | calendar + weather + trailing | 0.5257 | 1.9% | 1.9 | 6 of 9 |
| | calendar + trailing | 0.5262 | 1.8% | 2.1 | 7 of 9 |

The model loses the weeks of 2013-02-11 and 2013-02-18 in every run. The gap-1 runs use one seed.

**Numbers of mine that no longer stand.** My opening brief gave leads of 2.6% to 3.5% at 2.5 to 3.4 SE. Those were
measured against own-series forecasts picked on the test windows. I also gave 2.2% at 1.95 SE for `gap=1` with
weather. That was against the weaker EWMA at 7 days. Against the gapped validation pick it is 1.4% at 1.2 SE (table
above). The critic's rebuttal is right on both.

**Critic 1 (scope: TP-10 does not clearly pass). Concede leg 1 and leg 2. Contest `No`.**
- *Leg 2:* conceded, as in my opening brief. Keeping the dataset needs an amendment, not an exception.
- *Leg 1:* conceded. On the definition both sides now agree on (`gap=1`, weather kept), the shipped model leads by
  1.4% at 1.2 SE. The best model I found leads by 1.8% to 1.9% at about 2 SE. That is not "clearly beats" (TP-10,
  Must) next to ashrae (7.6% to 10.9%), rain_in_australia (9 of 9 windows) or g_research (every interval above the
  baseline). EV-1: the decisive experiment has been run, and it goes against me.
- *"Method not complete":* answered by new fact 1. Seasonal naive forecasts are 28% to 34% worse. One pooled model beats
  the models per store and per product in 9 of 9 windows. So the panel does reward generalising across entities, which
  is the reason TP-10 gives for tabular forecasting. But leg 1 compares against each pair's own-series forecast, and
  there the margin is about 2 SE. New fact 1 explains why a hold is better than `No`. It does not meet leg 1.
- *Precedents:* the critic is right that walmart's inputs, without the weather, are the fact set of the three
  intermittent-demand datasets set to `No`. One fact still sets walmart apart: it was probed, and the probe is
  borderline, not failed. A pooled model wins in 6 or 7 of 9 windows, and in 9 of 9 against models per entity. m5,
  with the same question, was held at `TBD -> 2nd Tier`. Treat like cases alike: follow m5, not the three `No`s.
- *Remedy:* the remedy ladder makes exclusion the step for "a Must that cannot be fixed". It is still open whether this
  one can be fixed: a model tuned on validation weeks (the critic's own "what would change my view"), the rossmann
  probe (precedent checker, option c), and the curator's reading of leg 2. So `TBD -> 2nd Tier` is the mildest course
  that breaks no Must. `No` + `Time-series (Forecasting)` is premature.

**Critic 2 (the score does not measure the storm decision). Concede.**
- The rewrite ("each day of the coming week, storms included") is milder than the filter, and it fixes USE-1. I agree
  it goes to the curator together with the scope call, because the reworded task is SEL-10's example. I withdraw "it
  changes no reading".
- I agree to the MET-2 note: the leaderboard's RMSLE covered only the storm windows, over all 4,995 pairs, 95% of them
  trivial zeros. It cannot be compared with ours.

**Critic 3 (weather from days after the prediction point). Concede. One new fact narrows it.**
- We agree on the note in LEAK-38's format and on rewording `fit_reason` (LEAK-6, USE-8).
- New fact: with trailing summaries, adding the weather makes the model worse, not better: 0.5196 against 0.5177 at
  gap 0, and 6 against 7 windows ahead. Its gain is not just zero. If the dataset ships, dropping the 16 observed
  columns now has a measured reason, and it brings walmart in line with rain_in_australia and aeolus_1m. I concede
  that the drop leaves only ids, the calendar and the series, which is the critic's point 1. The scope call has to be
  made with that fact in view.

**Critic 4 (no planning gap). Concede.** `gap=1` (SPLIT-10, rossmann's precedent). New fact 2 shows what it costs leg
1. That cost belongs in point 1.

**Critic 5 (the test season and item 93). Concede.** Notes in `splits_comment` and in the zeros bullet (SPLIT-20). If
the curator spreads the windows, choose them from counts (SPLIT-21). I add nothing.

**Critic 6 (cleaning and wrong notes). Concede all of it.** Same list as my point 7, plus the record's older
paragraph, which still gives m5 as `No`. If the dataset is held, the TP-10 notes should carry new facts 1 and 2: the
validation pick, `gap=1` and 1.4% at 1.2 SE as shipped.

**Judgment record (advocate, after rebuttal)**

```text
Verdict: do not ship now; TBD -> 2nd Tier (as m5), with the agreed changes applied; not No.
Validity: SEL-10/SEL-11 via TP-10 (Must): leg 2 fails as written (conceded); leg 1 not clear: against the
  validation-picked own-series forecast, 1.4% at 1.2 SE (gap=1, as shipped), at best 1.8-1.9% at about 2 SE with
  trailing summaries, 6-7 of 9 windows. TP-10 method done: pooled beats models per store and per product 9/9 (5.8%,
  6.7%) and seasonal naive forecasts by 28% or more. USE-1: rewrite (USE-9), decided with the scope call. LEAK-10:
  note, or drop (the weather now measurably hurts). SPLIT-10 gap=1; SPLIT-20 notes; SPLIT-21 holds.
Value: MET-2 holds with the note that the score is not comparable to the leaderboard.
Quality: CLEAN-10 codesum; CLEAN-11 Thanksgiving fact; notes corrected (EV-7, EV-2, EV-8).
For the curator: amend leg 2 or not, knowing leg 1 is about 2 SE at best; reopen rossmann for the same test; a model
  tuned on validation weeks is the open check that could lift the hold.
```

</details>

<details><summary>Critic rebuttal</summary>

**Critic, rebuttal (critic, 2026-11-01): walmart_sales_in_stormy_weather**

**Position: unchanged. Do not ship now; `TBD -> 2nd Tier`, as m5.** I agree with the advocate's remedies for points 4
to 7. The disagreement is TP-10 leg 1, and one new check decides it.

**The new fact (TP-10 leg 1, against a forecast picked without hindsight).**
- Every own-series forecast so far was picked on the test windows themselves.
- I picked one on the 9 weeks before the oldest test window (2012-11-26 to 2013-01-27), from 24 candidates: EWMA level
  with a half-life of 3, 5, 7 or 10 days, plus the weekday offset at full or half weight, with and without a zero rule
  and a same-season-last-year adjustment.
- The winner: a 10-day EWMA plus half the weekday offset. On the 9 shipped windows it scores 0.5323.
- The shipped model is LightGBM, 1,000 trees, with weather; I took its numbers from the claim auditor's 3 seeds.
  Against the winner:

| model | RMSLE | lead | paired SE | windows ahead |
|---|---|---|---|---|
| with weather (as shipped) | 0.5211 | 2.1% | 0.0058 (1.9 SE) | 6 of 9 (loses 02-04, 02-11, 02-18) |
| calendar only | 0.5213 | 2.1% | 0.0043 (2.6 SE) | 7 of 9 |
| with weather, against the best of the 24 on the test windows (0.5299, hindsight) | 0.5211 | 1.65% | 0.0056 (1.6 SE) | 6 of 9 |

- Script and outputs: `own_series.py` in the run folder (not committed), `own_series_val.csv` and `own_series_test.csv`.
- One caveat: the validation weeks hold Thanksgiving and Christmas.
- The lead has shrunk with each stronger baseline: 3.5% (builder), 2.65% (claim auditor), 2.1% (picked on
  validation).

**Advocate 1 (valid at P3 to P5; the source's metric). Concede, narrowed.**
- The actor is real, the data is faithful, no feature comes from the sales, and dropping the never-sold pairs keeps
  the ranking (MET-2).
- None of this bears on P2. Scope is a separate Must, and principles.md, "How to decide", item 4, says independent
  failures are not rescued by passes elsewhere.

**Advocate 2 (leg 1 holds in every run). Contest.**
- TP-10 (Must) asks that the model "clearly beats" each entity's own forecast on the shipped windows.
- As shipped, with the weather, the lead is 2.1% at 1.9 SE, 6 of 9 windows, against a forecast picked without
  hindsight (new fact above).
- On the definition the advocate proposes (`gap=1`, weather kept), the advocate's own run already falls below 2 SE:
  2.2% at 1.95 SE (`gap1.csv`). That run used the weaker unshrunk EWMA.
- Every case kept in scope cleared a far higher bar (TP-10 Cases). ashrae's 1,000-tree model won every window by 7.6%
  to 10.9%. rain_in_australia won 9 of 9 windows. g_research had every interval above the baseline. "Default loses,
  1,000 trees win" matches ashrae in form, not in size.
- I concede (b), (c) and (d):
  - WAPE is not the declared metric, and I did not rely on it.
  - The shipped ids are categorical. I cite integer ids only as fragility, not as the test.
  - The blind reviewer's windows are not the shipped ones.
- What would change my view: a lead that holds against a forecast picked on validation weeks, in most windows, at
  well over 2 SE. A tuned model might give one; nobody has measured it.

**Advocate 3 (a reading of leg 2). Concede the premise, contest the conclusion.**
- Conceded:
  - As written, leg 2 fails, so keeping the dataset needs an amendment.
  - The competition's test interpolated, so the per-pair curves of the 1st and 5th place say little about forward
    windows.
  - m5 differs (recursive lags).
- Contested:
  - The proposed reading makes leg 1 carry the whole test, and leg 1 is now 1.9 SE as shipped. The amendment would not
    settle the call; it would rest it on a margin inside noise.
  - Leg 2 says "the source's top solutions". Only 1 of the 3 described (the 3rd place) is our setup.
  - The precedent checker notes this would be the third change to leg 2 in ten days. Each was made to keep one panel.
  - rossmann: treating like cases alike means probing rossmann (precedent-checker option c), not reading a borderline
    measurement as a pass. A fact also sets rossmann apart: drivers known in advance (promotions, holidays,
    assortment, competition). walmart has no such driver, since the weather adds nothing.
  - The curator's "Do yes and then we can see what happens" asked for the measurement. The measurement is borderline,
    so the call goes back to the curator. It does not stand as a `Yes`.

**Advocate 4 (weather kept with a note). Concede the remedy, narrow one claim.**
- We agree on the note in LEAK-38's format and on rewording `fit_reason` (LEAK-6, USE-8).
- I contest "dropping costs nothing and the dataset stays". Without the weather, the inputs are a series id and a
  date. That is the fact set of auto_intermittent_demand, car_parts_intermittent_demand and raf_aerospace_parts_demand
  (`No`, Andrej, 2026-10-30). That they were judged without a probe does not change their facts.

**Advocate 5 (split right; rewrite the use case). Concede the split; narrow the rewrite.**
- Conceded: the regime (USE-10), the period chosen from counts (SPLIT-21), and the forced departure from SPLIT-19 for
  the split.
- Also conceded: the rewrite fixes USE-1, and it is milder than the filter.
- But it does not "change no reading". The reworded use case, each carried product's daily units for the coming week,
  is SEL-10's own example ("future values of a series (demand, sales ...) over a horizon").
- USE-9's counter-factor also applies: "a use case rephrased only to excuse a gap".
- So the rewrite is acceptable only if it is decided together with the scope call, not before it.

**Advocate 6 (gap, season, item 93, zeros). Concede.**
- `gap=1` is agreed (SPLIT-10). It cuts leg 1 to 1.95 SE (above), which belongs in point 1, not here.
- Notes for the season and item 93 are agreed (SPLIT-20).
- The zeros are settled by the curator's policy call 2; I did not raise them.

**Advocate 7 (cleaning and notes). Concede.** It is the same list as my point 6.

**Judgment record (after rebuttal)**

```text
Verdict: do not ship now; TBD -> 2nd Tier (as m5), or No + Time-series (Forecasting). If the curator amends TP-10 and
  keeps the dataset, ship after the agreed changes.
Validity: SEL-10/SEL-11 via TP-10 (Must): leg 2 fails as written (conceded by both sides); leg 1 not clear: 2.1% at
  1.9 SE, 6/9, as shipped, against an own-series forecast picked on validation weeks; 2.2% at 1.95 SE with gap=1.
  USE-1: rewrite or filter, decided together with the scope call. LEAK-10: weak, kept with a note (agreed).
  SPLIT-10: gap=1 (agreed). SPLIT-20: notes (agreed).
Quality: CLEAN-10 codesum; notes corrected; CLEAN-11 fact added (agreed).
For the curator: amend TP-10 leg 2 or not, knowing leg 1 is within about 2 SE; or reopen rossmann for the same test.
```

</details>
