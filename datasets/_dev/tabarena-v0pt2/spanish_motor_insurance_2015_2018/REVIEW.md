# spanish_motor_insurance_2015_2018

**Outcome:** added. The AI recommends shipping it as built; issue 1 (the changed task) could still turn it to `No`. A
sample of a Spanish non-life insurer's motor portfolio (Mendeley Data 5cxyb5fp4f version 2, CC BY 4.0; Segura-Gisbert,
Lledó and Pavía 2025). One row is a policy's first year of cover in the release, for a customer with one policy in
force (25,665 rows), and the target is that year's claim cost (payments plus reserves). It is shipped as log1p and
scored on the amount by the normalized Gini, a context metric. The split is temporal: 5 monthly test windows of new
contracts, August to December 2017, each trained on the years that had ended by the window's start.
Validity:
- SEL-1 and SEL-2 hold.
- USE-1 holds for new-business pricing, fit approximate (USE-8; issue 1).
- USE-5 was triggered three times, each fixed by a filter that reads no label: the later yearly rows (issue 1), the
  years without cover (dropped; USE-7), and claims shared with the customer's other policies (issue 2).
- USE-6 holds for `Premium`.
- LEAK-10 was triggered: the end-of-policy columns, `Seniority` and `Payment` are dropped, and `Value_vehicle` is kept
  (issue 3).
- SPLIT-9 and SPLIT-10 were triggered (training years not yet ended at the window's start), fixed by a 12-month gap;
  SPLIT-14 holds. The no-gap exception is gone, so this dataset does not count toward avito_demand_prediction_1m's
  SPLIT-10 amendment (its issue 4).
- PROV-6 and PROV-7 hold against `spanish_motor_insurance_coverage_level_2022_2024`: not a duplicate (other years,
  schema and task).
- PROV-13 is open (issue 4).

Value: a small real signal (TP-2). `Trivial` against the premium is not proven (TP-4; issue 5). Every window can be
scored (MET-2). The metric and the target scale are decided for the insurance family in
australian_vehicle_insurance_2004_2005, issue 4 (the normalized Gini) and issue 5 (log1p or dollars; here, untuned
LightGBM scores 0.116 fit on log1p, 0.121 with a Tweedie loss on the amount and 0.073 with squared error on the
amount). This table has no exposure column, so an exposure-weighted Gini (frempl issue 4) would need a time at risk
built from `Date_lapse` as a scoring column.
Quality: the ages are fixed (CLEAN-1) and the fill values noted (CLEAN-10).
Weighed: documented source, licence and real decision +; thin signal beyond the premium, noisy monthly windows, and
two weak windows for every model -.
Left for Andrej: issues 1 to 5.

Changes made after the review panel (AI, 2026-11-01), no decision needed: the 5,069 renewals never in force are
dropped (14 claims; as the 2022-2024 sibling); `Payment`, the "last" payment method, is dropped (zillow_prize); the
split is re-made with a 12-month gap (5 monthly windows, August to December 2017, 58-79% of the rows train; the 3,127
rows starting December 2016 to July 2017 are in no split); the ages are computed by the calendar; `use_case`,
`fit_reason`, the metric reason and the notes are rewritten and every number re-measured.

The record's screening and Assessment lines still describe renewal pricing. They are updated once issue 1 is decided.

**Main points:** Confirm new-business pricing on first years and the filter to customers with one policy (the debate's
open point); keep `Value_vehicle`; ask the authors for their raw data; ship before tuned results settle `Trivial`.

**Issues for Andrej:**

1. **Confirm the task as built: pricing a new contract from its first year (implemented), not renewal pricing over all
   policy-years?**
   Your `Yes` (2026-10-30) was given on the screening's task: at renewal, an insurer sets next year's premium, with one
   row per policy-year. The release does not support that task. A policy's later yearly rows do not record that year's
   claims. They record a shrinking remnant of earlier ones:
   - after a claim-free year, only 0.9% of the next years have a claim (133 of 14,980 years with cover), against about
     a third of first years;
   - after a year with claims, the count falls in 99.9% of cases;
   - last year's count alone ranks the later rows at a Gini of 0.86.

   A model trained on these rows would learn last year's claims, not next year's risk. The 2022-2024 release of the same
   research group shows 17.4% after a claim-free year, so the defect belongs to this release. That figure counts claims
   as here: a next year with a recorded claim after a year with none (of 145,964 years). The 2022-2024 file's precedent
   check counts claim cost instead, a next year with a cost above 0 after a year without one, and finds 14.6% (of
   149,929 years); that release records some claims at zero cost. In this release the two counts coincide, since a
   year's cost is 0 exactly when its claim count is.
   * Rule: USE-5 (Must). Rows whose label is found from the data to be another quantity are dropped (rain_in_australia
     and ames_housing; Lennart, 2026-10-26). corporate_credit_rating was retired only because its bad labels could not
     be located; here they can be. Your `Yes` decides which task is built, so the changed task needs your
     confirmation. The fit is approximate (USE-8).
   * Implemented: each policy's first year only, so every test row is a new contract. Training also holds older
     contracts' first year in the release (a renewal, November 2015 to November 2016). The blind reviewer flagged the
     mix; the panel kept those rows for training, since the test rows are the ones the use case names. `use_case`: the
     insurer refines its quoted premium for a new contract (USE-6). The data article names "pricing mechanisms for new
     business" among the uses (Sec. 1).
   * Alternative: retire with `Data Quality Issue` until the authors' raw data (issue 4) restores the renewal years.

   Recommendation: confirm. Decision: confirm, or retire?

2. **Keep only customers with no other policy at the insurer (implemented), or keep every first year with a note?**
   A policy's claims move with the claims of the same customer's other policies running at the same time:
   - Among first years that have such a policy in the sample, 80% have a claim when that policy has one and 6% when it
     does not (2,493 rows; 35% across all first years).
   - Of the 1,532 such pairs (a first year and the same customer's other policy, overlapping by more than 180 days),
     1,519 insure different vehicles.
   - The link grows with the number of days the two years overlap. The same customer's years more than 180 days apart
     show only a mild link (21% against 12%).
   - For customers with no other policy in the sample, claims per row grow in proportion to `Policies_in_force`, the
     customer's number of policies: 0.65, 1.15, 1.61, 2.01 and 2.46 for 1 to 5 or more (over all first rows, the
     README's table gives 0.64 to 3.15).
   - The costs are not copies. Within a pair they are unrelated, and at every count each claimant row carries a
     full-size cost (863 to 1,002 on average).

   The release cannot say whether claims are booked to every policy of the customer, or whether such customers really
   claim together. Only the authors can (issue 4).
   * Effect: if claims are booked across policies, rows with two or more policies carry the other policies' claims.
     These are 31% of the rows and 45% of the test rows, and a model scores them by `Policies_in_force`. With every
     first year kept, almost all of a model's gain over the premium comes from that count (logistic regression, the
     mediator's run):

     | inputs | Gini |
     |---|---|
     | premium alone | 0.162 |
     | all features but the count | 0.168 |
     | premium and the count only | 0.228 |
     | all features | 0.233 |

     A tariff learned from these rows would charge customers with several policies for the way claims are booked.
   * Rule: USE-5 (Must). The critic: a label checked and found to be another quantity still fails, so those rows go.
     The advocate: the rule that assigns claims to policies is undocumented and each policy's money is its own, so the
     label ships `approximate` with a note (as diabetes_3). The mediator sided with the critic, for four reasons:
     - the check was made;
     - the pattern is the same kind as in issue 1: found from the data, mechanism unknown, rows dropped;
     - the remedy ladder puts a fix of the definition before a note;
     - PROV-13 asks for the origin to be checked before a suspected damage is kept.
   * Implemented: keep the rows with `Policies_in_force == 1` (25,665 rows; 2,385 test rows, 117-195 claims per window)
     and drop the column, which is then constant. `use_case` names customers with no other policy.
     - Cost: 31% of the rows and 45% of the test rows go, and the premium alone then ranks as well as any method tried
       (issue 5).
     - The count covers the calendar year, so customers who add a policy later in the year go too. They claim at the
       same rate as the rest (31.2% against 31.2%).
   * Alternative: keep all 37,090 first years.
     - The `Policies_in_force` note says the count also tracks claims that occur together on a customer's policies.
     - The count loses the 2,865 policies written later in the year that can be found in the sample (LEAK-10 fixes a
       late value it can locate); the later policies outside the sample stay, under a `Potential leak, kept on
       purpose:` note.
     - `fit_reason` names the gap.

   Recommendation: the filter; revisit it if the authors show that claims are booked per policy. Decision: filter, or
   note?

3. **Keep `Value_vehicle`, a valuation of 31 December 2019 (implemented)?**
   The variable sheet gives the "Market value of the vehicle on 31/12/2019", a date after every year in the data. It
   is one value per policy, a property of the vehicle, and it does not move with the claims (measured on the shipped
   rows):
   - the type, age, power, size and weight explain 97% of its log;
   - what is left of it after those characteristics ranks the policies with a claim at ROC AUC 0.497, no better than
     chance (0.492 for a cost over 2,000);
   - no vehicle was registered after its row's start.
   * Rule: LEAK-10 (Must), its clause on attributes looked up later "unless the data shows they did not change". You
     decide that clause case by case (amended 2026-10-26). This follows onlinenewspopularity (kept on a traced test).
   * Implemented: kept, with a `Potential leak, kept on purpose:` note and a condition to revisit it (a release with the
     value at each renewal). `fit_reason` names it as kept, not as a gap (USE-8).
   * Alternative: drop it. It costs nothing measurable: untuned LightGBM ranks the 5 windows at 0.140 without it and
     0.116 with it, inside one window's noise (bootstrap SE 0.08-0.11).

   Recommendation: keep. Decision: keep, or drop?

4. **Ask the authors for their pre-cleaned raw data?**
   The article offers "the pre-cleaned raw data" (Sec. 1). It would show how claims are assigned to years and to a
   customer's policies. That settles issue 2, and it could bring back the renewal years of issue 1 and the customers
   with several policies. The 2022-2024 sibling's REVIEW.md asks nothing that this request would settle; ask about it
   too only if it turns out to be the same insurer, which neither article says. An agent cannot send it.
   * Rule: PROV-13 (Must): check the origin before keeping a damage or retiring a dataset. With the filters above, the
     damaged rows are dropped, not kept, so the request does not block shipping. It is required before the note of
     issue 2's alternative.
   * Implemented: nothing sent; the dataset ships on the filters of issues 1 and 2. Alternative: no request; the
     filters then stay for good and the renewal years stay out.
   * No precedent. In the zero-inflated review (policy question 8, 2026-10-30) you sent no requests for records whose
     data is only on request; this asks for the rows behind a table already released.

   Recommendation: send it, and ship in the meantime. Decision: send it, or not?

5. **Ship now and re-check `Trivial` on the first benchmark run (implemented), or hold until tuned results exist?**
   `Trivial` (TP-4) means that one raw input matches or beats the methods in every test window. Here that input is
   `Premium`, the insurer's own price and the natural core of a pricing task (USE-6).
   - On the shipped design (normalized Gini, mean of the 5 windows), the premium alone ranks at 0.234, ridge and
     logistic models at 0.230, and a LightGBM tuned on an inner time split at 0.176. The premium leads the best method
     in 3 of 5 windows and loses October and August.
   - With every first year kept, it leads in 1 of 5 (0.162 against 0.235), but there the gain comes from
     `Policies_in_force` (issue 2).
   - These models are proxies. The benchmark's tuned methods have not run (TP-1).
   * Rule: TP-4 and TP-1 (Must), TP-2 (Should). `Trivial` is not proven on either design. This reads TP-4 as
     wisconsin_local_government_property_insurance_fund (this run) and sepsis_survival did. The critic would call the
     dataset `Trivial` unless tuned methods beat the premium in every window, which reverses TP-4's burden of proof.
     Both sides asked for tuned results before shipping.
   * Implemented: ship. On the first benchmark run, retire it as `Trivial` if the premium alone matches or beats the
     tuned methods in every window.
   * Alternative: keep it out of the collection until the benchmark's tuned methods have run on this dataset alone.
   * For your weighing: whichever design ships, the dataset mostly tests how well a model uses the insurer's own
     premium. The other rating factors add little beyond it.

   Recommendation: ship and re-check. Decision: ship and re-check, or hold?

**Review panel:** ship after changes (mediator). Claim audit: 43 claims, 27 hold, 14 refuted in whole or in part (the
years without cover, the claims shared across a customer's policies, the late part of `Policies_in_force` and text
slips; fixed, or in issues 1 and 2), 2 untested. Blind review: would include with changes; its main concern was the
renewals never in force, labelled as claim-free years (now dropped). Debate: agreed on dropping the years without cover
and `Payment`, the 12-month gap with 5 monthly windows and the cleaning and text fixes; disputed: the filter to
customers with one policy (issue 2, settled for the critic by the mediator) and `Trivial` against the premium (issue 5).
The reports describe the definition before the panel's changes (42,159 rows, 9 windows without a gap); the issues
quote the re-measured numbers.

<details><summary>Mediator</summary>

**Mediator (2026-11-01): spanish_motor_insurance_2015_2018**

```text
Verdict: ship after changes.
Validity: SEL-1 and SEL-2 hold. USE-1 holds for new-business pricing, fit approximate (USE-8); the task moved away from
  the renewal pricing the CC `Yes` named, so the curator confirms it (issue 1). USE-5 triggered three times: the later
  yearly rows (fixed: first rows only), the years without cover (fixed: dropped, with USE-7 and LEAK-25), and claims
  that move with the customer's other policies (settled for the critic's filter `Policies_in_force == 1`, issue 2).
  USE-6 holds (`Premium`). LEAK-10 triggered: the end-of-policy columns, `Seniority` and `Payment` dropped;
  `Value_vehicle` kept on a traced test (issue 3). SPLIT-9 and SPLIT-10 triggered, fixed by a 12-month gap with 5
  monthly windows (SPLIT-14 holds). PROV-13 open, not blocking (issue 4).
Value: TP-4 not proven on either design: the premium alone matches or beats the best method in 1 of 5 windows with
  the note, 3 of 5 with the filter, and TP-4 needs every window. TP-2 keep; re-read TP-4 on the first benchmark run
  (TP-1, issue 5). MET-2 holds (117-195 claims per window after the filter). MET-11 holds once the reason names the
  Kaggle form of the Gini.
Quality: CLEAN-1 (`contract_years` and two ages) fixed; CLEAN-10 notes added; text slips fixed.
Weighed: documented source +, licence +, real decision +; thin signal beyond the premium -, window noise (one
  window's SE 0.05-0.11) -, two windows near zero for every model -.
For the curator: issues 1-5. Issue 2 is the point the debate left open.
```

**Decisive experiment (mine)**

Scripts and outputs are in the run folder (`decisive.py`, `decisive2.py`). All
runs use the agreed design: no-cover rows and `Payment` dropped, a 12-month gap, windows August to December 2017,
normalized Gini on the amount. "Tuned" LightGBM picks one of 12 settings on the last 15% of each training side; it is
a proxy, not the benchmark's tuned methods.

| design | rows / test rows | premium alone | ridge on log1p | logistic (claim) | LightGBM tuned | LightGBM untuned | CatBoost default | premium at or above the best method |
|---|---|---|---|---|---|---|---|---|
| A: note (all first years) | 37,090 / 4,362 | 0.162 | 0.235 | 0.233 | 0.195 | 0.172 | 0.101 | 1 of 5 windows |
| C: `Policies_in_force == 1` | 25,665 / 2,385 | 0.234 | 0.230 | 0.230 | 0.163 | 0.127 | 0.035 | 3 of 5 windows |

On design A, the logistic model shows where the gain over the premium comes from:

| inputs | mean Gini |
|---|---|
| premium alone | 0.162 |
| all features except `Policies_in_force` | 0.168 |
| `Policies_in_force` alone (ties broken by the premium) | 0.218 |
| premium and `Policies_in_force` only | 0.228 |
| all features | 0.233 |
| all features, scored on the test rows with one policy only (premium alone: 0.234) | 0.228 |

For customers with no other ID in the release, by `Policies_in_force` (1, 2, 3, 4, 5 or more):

| measure | 1 | 2 | 3 | 4 | 5+ |
|---|---|---|---|---|---|
| claim share | 0.33 | 0.49 | 0.59 | 0.58 | 0.65 |
| claims per row | 0.65 | 1.15 | 1.61 | 2.01 | 2.46 |
| cost per row | 296 | 461 | 506 | 580 | 586 |
| cost per claimant | 895 | 943 | 863 | 1,002 | 906 |

Reading:
- The extra claimant rows at higher counts carry claims of full size, since the cost per claimant stays flat. So the
  amounts are not one claim split across policies. That supports the advocate's "not a copy". It does not show that
  the claims belong to the row's own vehicle.
- On design A, all of a model's gain over the premium is `Policies_in_force`, the feature tied to the disputed label.
  On the rows with one policy, and on design C, the rating factors add nothing on average beyond the premium.

**Agreed facts**

1. The data is a real sample of a Spanish insurer's portfolio, CC BY 4.0, and the hashes match. v2 differs from v1
   only in 3,416 `Distribution_channel` cells.
2. The later yearly rows hold a remnant of earlier claims, not the year's claims. After a claim-free year, 0.7% of the
   next years have a claim (0.9% without the no-cover rows), and after a year with claims the count falls in 99.9% of
   cases. The 2022-2024 sibling shows 17.4%, so the defect is this release's. The build keeps first rows only.
3. The six end-of-policy columns and `Seniority` are rightly dropped. As published they lift the Gini from 0.73 to
   0.89, and the `Seniority` rebuild leaks.
4. 5,069 first rows (12.0%) end on or before the day they start. They hold 14 claims, and all but 17 are in training.
5. `Premium` is the annual written premium, known at the quote (USE-6).
6. `Value_vehicle` beyond the vehicle's own characteristics ranks claims at ROC AUC 0.508.
7. `Payment` is one value per policy, and it shows a pattern that cannot be traced: 40% of renewed first years with a
   claim are half-yearly, against 26% without one.
8. `Policies_in_force` counts the calendar year: 68% of 2,723 pairs already count a policy written later. That late
   part carries no gain (Gini 0.229 with it, 0.243 without).
9. A customer's concurrent policies claim together. Among 2,493 first rows that have a concurrent policy in the
   sample, 80% claim when that policy claims and 6% when it does not, and 1,519 of 1,532 such pairs insure different
   vehicles. The costs are not copies (Spearman 0.08 in pairs where both claim, 1.4% equal). The release cannot tell
   booking from a customer effect (EV-1). The advocate's customer filter does not remove the effect (0.84 against
   0.09), and it is withdrawn.
10. Without a gap, 22-65% of the training rows had not ended at the window's start, and 579 test rows have a running
    policy of the same customer in training (claim share 58.7% against 7.1%). A 12-month gap meets SPLIT-14 in 5
    monthly windows, August to December 2017 (52.9-72.9% of the rows train after the no-cover drop), and removes both
    problems.
11. November and December 2017 rank near 0 for every model, with no sign of run-off, and they stay (SPLIT-21). One
    window's Gini has a bootstrap SE of 0.05-0.11.
12. `contract_years` is a year too low for 5,608 rows, `driver_age` for 30 and `years_licensed` for 42.
13. With the agreed fixes and a note, untuned learners about tie the premium (0.172 against 0.162). No tuned results
    exist.
14. The CC `Yes` (Andrej, 2026-10-30) was given on renewal pricing. The build is new-business pricing.
15. The text slips found by the claim auditor, the column auditor and the critic stand (list under "Changes to make
    now").

**Changes to make now (no decision needed)**

1. Drop the years without cover: keep `Date_lapse.isna() | (Date_lapse > Date_last_renewal)` before step 3. This
   leaves 37,090 rows. Rules: USE-7 (Must) and LEAK-25's recovered case; it follows the 2022-2024 sibling. Then rewrite
   the reason for accepting the warning: its "observed claim-free years" was not true of these rows.
2. Drop `Payment`. Rule: LEAK-10 (Must, as amended): a removal test alone is no reason to keep a column (zillow_prize,
   melbourne_housing_market; cauca dropped).
3. Re-split as `TemporalSplits(window=1, unit="months", gap=12, min_train_fraction=0.5)`, which gives 5 windows from
   August to December 2017. Rules: SPLIT-10 (Should), SPLIT-9 (Must, by its Tensions row), SPLIT-14 (holds).
   - Remove the no-gap exception and the "as for lending_club and alfa_battle_2_0_task_2".
   - `splits_comment` and `task_summary.split` say "trained on the policy-years that had ended by the window's start".
   - Say that November and December are near zero for every model and stay (SPLIT-21).
4. Compute `contract_years`, `driver_age` and `years_licensed` by calendar arithmetic (the column auditor's
   `_whole_years`). Rule: CLEAN-1 (Should).
5. Fix the text:
   - `use_case`: refine the quoted premium for a new contract (USE-6, USE-8).
   - `fit_reason` (USE-8): name the missing cover, claims history and territory, the undocumented carry-over between
     years, the 2,055 first years cut short (kept unweighted, the cut known only at the end) and the undescribed
     sample design. Move `Value_vehicle` to "kept".
   - Metric reason: name the Kaggle form of the Gini (losses ordered by the prediction, each policy weighted 1), with
     Frees, Meyers and Cummings as background (MET-11).
   - Notes: `Power` 0 and missing `Type_fuel` are one block of 652 rows without vehicle data (CLEAN-10). `Length` is
     also missing for 423 cars and vans. "24% of the policies" means 24% of the policies with several rows. `ID` is the
     policyholder-and-product key. Add an `Anomaly:` note for the three fill blocks of farm vehicles (CLEAN-10).
   - Older-contract first rows also start after November 2016 (48 rows).
   - Re-run `dataset check` so the README drops "ties in row order".
   - Re-measure every count, share and score in the notes and the task summary after the changes.
6. The mediator settled this one, and it is implemented as the default; the curator confirms it in issue 2. Keep only
   `Policies_in_force == 1` and drop the column, now constant. The task then covers new contracts of customers with no
   other policy at the insurer.

**Changes that need the curator (ranked)**

1. Confirm the task: new-business pricing on each policy's first year in the release, instead of the renewal pricing
   the CC named (P3; USE-5, USE-8, who decides).
2. The filter to customers with one policy in force, or a note (P3; USE-5). This is the disputed point below.
3. Keep `Value_vehicle` under LEAK-10's lookup clause (P4). The curator decides this clause case by case and never by
   default.
4. Ask the authors for the pre-cleaned raw data (P5; PROV-13). One request serves this record and the 2022-2024
   sibling's issue 3. It does not block shipping.
5. Ship now and re-read TP-4 on the first benchmark run, or hold until tuned results exist (P6; TP-1, TP-4).

**Disputed point 1: claims shared across a customer's concurrent policies (P3, USE-5 Must)**

- The critic rests on USE-5's last sentence: a label checked and found to be another quantity fails, so the rows go
  (`Policies_in_force == 1`). The advocate rests on its middle clause: a label whose construction is undocumented
  ships `approximate` with a note (diabetes_3).
- Both sides cite the same rule at the same rank and strength. So this is not a conflict between rules, and not an
  independent failure. The question is which clause the facts meet.
- Settled for the critic:
  - The check was made, and its result concerns the part of the target that carries the score: whether a claim occurs
    (severity models reach R^2 of about 0). On different vehicles, a row claims at 80% when the customer's concurrent
    policy claims and at 6% when it does not, against 35% across all first years. The spread grows with the days the two years
    overlap (0.42 against 0.08 at 90 days or less, 0.90 against 0.04 at 350 or more). The same customer's years more
    than 180 days apart give only 0.21 against 0.12, which measures the customer effect. A different vehicle claiming
    at 4-6% when its sibling is claim-free is the same kind of pattern as issue 1's 0.7%. That is "checked and found",
    not "cannot be checked".
  - The advocate's evidence concerns the amounts. The costs are distinct, and each is full size (my table). That shows
    the amounts are not copies. It does not show the claim belongs to the row. The motorbike and farm counts are
    small (9 and 1 pairs with a claiming sibling).
  - Like cases are treated alike. The whole panel dropped the later yearly rows on the same kind of evidence: a
    carry-over measured in the data, with its mechanism undocumented (as rain_in_australia, Lennart, 2026-10-26).
    Shipping this carry-over as `approximate` would need a fact that sets it apart, and none was shown.
  - The remedy ladder puts a definition fix that reads no label before a note. PROV-13 (Must) asks for the origin to
    be checked before a suspected damage is kept, and the note would keep it.
- Cost of the filter:
  - 31% of the rows and 45% of the test rows go (2,385 test rows, 117-195 claims per window), and the use case
    narrows.
  - The count is per calendar year, so the filter also drops customers who add a policy later in the year. Those rows
    claim at the same rate (31.2% against 31.2%), so the filter does not select on the outcome.
  - After the filter, the premium alone ranks as well as any method tried (disputed point 2).
- What would overturn it: the authors showing that claims are booked per policy (issue 4). Then the advocate's
  design stands. `Policies_in_force` returns with the 2,865 located later additions subtracted (LEAK-10, LEAK-7), a
  `Potential leak, kept on purpose:` note, and the gap named in `fit_reason`.
- It still goes to the curator: it narrows the task the curator approved, and the mechanism is not proven.

**Disputed point 2: `Trivial` against the premium (P6, TP-4 Must, TP-1 Must)**

- The critic's condition: if tuned methods do not beat the premium window by window, the dataset is `Trivial`. That
  reverses TP-4's burden. TP-4 says "`Trivial` needs proof": the raw feature has to match or beat the methods fold by
  fold. The methods do not have to beat the feature in every window.
- On the present evidence it is not met under either design:
  - design A: the premium leads the best method in 1 of 5 windows;
  - design C: it leads in 3 of 5, and the ridge and logistic models win October (0.462 against 0.408) and August
    (0.269 against 0.199).
- The wisconsin_local_government_property_insurance_fund mediator (this run) read TP-4 the same way, as did
  sepsis_survival (kept). TP-1 asks for the benchmark's tuned methods, and none have run. So: keep under TP-2, and
  re-read TP-4 on the first benchmark run.
- The methods spread widely (CatBoost 0.035 to logistic 0.230 on design C). If tuned methods spread like this, TP-3
  keeps the dataset.
- Left to the curator as a weighing factor, not a verdict: whichever design is shipped, the dataset mostly tests how
  well a model uses the insurer's own premium.

**Consistency with precedent**

- First rows only follows rain_in_australia and ames_housing (Lennart, 2026-10-26): rows located by a rule whose label
  is found to be another quantity are dropped. corporate_credit_rating was retired because its rows could not be
  located; here they can be.
- The no-cover drop follows the 2022-2024 sibling (USE-7; an AI draft of the same run, a like case).
- The `Payment` drop follows zillow_prize and melbourne_housing_market (2026-10-21) and cauca.
- The gap follows Lennart's SPLIT-10 calls (brazilian_ecommerce, sf_permit_time, zillow_prize, house_sales) and
  pricing_game_2016_french_fleet (closed years only). The lending_club and alfa_battle_2_0_task_2 exceptions rested on
  the floor, which holds here. The builder's "third exception" goes, and this case no longer counts toward
  avito_demand_prediction_1m's amendment. wisconsin still ships without a gap for the same mechanism; that is settled
  in its own REVIEW.md.
- The filter follows the dataset's own drop of the later rows and rain_in_australia. It departs from diabetes_3 and
  blood_tests_drink_prediction (`approximate`). What sets it apart: their labels could not be checked, and this one
  was.
- TP-4 follows wisconsin (same run) and sepsis_survival.
- `Value_vehicle` follows onlinenewspopularity and account_debt_south_africa. Those are the LEAK-10 clauses, the
  curator's call each time.
- PROV-13 has no precedent. Policy question 8 (2026-10-30) left unreleased data on request alone. This is a repair of
  a released table.
- PROV-6 and PROV-7 against the 2022-2024 sibling: not a duplicate under the Tensions row (a shared source with
  distinct tasks). The periods and schemas differ, and the two releases record later years differently (0.7% against
  17.4%). No issue.
- Quarterly windows (builder issue 5) are moot: with the gap, only 2017-Q4 meets the floor, and SPLIT-21 bars choosing
  windows by score.

</details>

<details><summary>Claim audit</summary>

**Claim audit: spanish_motor_insurance_2015_2018 (claim-auditor, 2026-11-01)**

Verdict: ship after changes. Two claims about the target are refuted, and each has a fix in the definition that is a filter by a rule that never reads the label. The metric claim holds.

```text
Validity: USE-5 (Must) triggered twice, both fixable by a filter: (1) the claims carry over between a customer's
  policies, not only within a policy; (2) 5,069 rows are years whose contract ended on or before the start.
  LEAK-10 (amended clause, case by case): Policies_in_force counts policies written later in the year; the data
  shows the later part does not help, so keep it with a note. SPLIT-9 / LEAK-17: the same customer's training labels
  tell 15% of test rows' outcomes; filter (1) removes this.
Value: TP-2 holds (a small real signal). MET-2 holds. MET-10 factor: one window's Gini has a bootstrap SE of 0.06-0.10.
Quality: six text slips and a stale README metric line.
```

Scripts and outputs are in the run folder (t1-t17). Untuned LightGBM (300 trees, lr 0.05) on the 9 shipped windows. Gini means normalized Gini on the amount, computed with the current scorer (ties averaged). A "customer" is an exact match on `Date_birth` + `Date_driving_licence` (47,870 keys for 53,502 policies). Where a key is matched to a later policy, that policy has `Policies_in_force` >= 2 in 88% of cases (90% with the same `Area` added).

**Refuted claims, ranked (validity first, Must first)**

1. **The carry-over is per customer, not only per policy (P3, USE-5 Must; P4, LEAK-17, SPLIT-9).** The definition implies that "each policy's first year in the release" is a year of the policy's own claims, and that the test rows are "the new contracts of a coming month" (task_summary `row`, `split`; notes bullet 3). The decisive test was the claim share of a policy's first row when the same customer already had an earlier policy in the release, split by whether that earlier policy's first year had a claim.
   - Claim share is 4.3-7.9% when the customer's first policy had no claim in its first year, and 47-53% when it had one. The baseline for customer-first rows is 36.5% (2,620 such rows with cover; t7). Real claim-free years cannot cut the next policy's claim rate by a factor of 5-8. This is the same pattern as the policy-level remnant (0.7% against 26-38%).
   - In the test windows, 1,097 of 7,573 rows (14.5%) are such later policies. They claim at 0.200 against 0.363 for the other test rows. Untuned LightGBM predicts them a mean cost of 15.8 against 8.3, because `Policies_in_force` is >= 2. The artifact makes the model rank these rows the wrong way (t8).
   - 1,138 test rows have a policy of the same customer on the train side. That policy's claim indicator ranks the test row's claim at ROC AUC 0.65-0.82 per window. The model reaches 0.60-0.66 on all features. In 43-65 rows per window, the train-side year was still running at the window's start, so its label is partly future (t2). Untuned LightGBM does not exploit this (the leak probe's near-neighbour R^2 is -0.96).
   - Remedy (fix the definition, a filter): keep each customer's first year in the release. Drop a first row when the same customer key has an earlier first row with cover. This rule reads the keys and dates, never the label, and the insurer knows at writing whether the customer already holds a policy.
   - Effect, together with item 2: 34,470 rows remain, test windows hold 546-828 rows, and train shares are 81-98% (SPLIT-14 holds). Mean Gini rises from 0.235 to 0.274, and claim ROC AUC from 0.632 to 0.672. On the same remaining test rows, the shipped model scores 0.264 and the fixed one 0.274 (t8).
   - What changes: `row`, `split`, `changes` and `fit_reason` in the task summary, and notes bullet 3 (the remnant spans the customer's policies). The curator may instead want the authors' raw data first (PROV-13; the builder's issue 1).

2. **5,069 shipped zeros are years without cover (P3, USE-5 Must; the record's "no exposure" risk).** The warning acceptance says "68.8% zeros, exactly the rows with N_claims_year = 0: observed claim-free years". `predicted` says "the year's claim cost". The test was claims by `Date_lapse` relative to the row's start (t5, t6).
   - 5,069 older-contract first rows (12.0% of the rows, 17.5% of the zeros) have `Date_lapse` on the year's start (4,971) or before it (98). Their claim share is 0.3%. 98% of them have `Lapse` >= 1, and every one is its policy's last row. The renewal never took effect, so these rows are not claim-free years.
   - They are train-side only (2015-11 to 2016-11), plus 17 rows in the test windows. With them, the older-contract claim share is 25-27% per month; without them it is 32-35%. Notes bullet 3 relies on the 25-27% figure. Its conclusion (stable by month) survives, but the number has to change.
   - Remedy (filter): drop rows with `Date_lapse <= Date_last_renewal`. This is known when the year starts. Dropping them from training alone moves the mean Gini from 0.235 to 0.248 on the same test rows (t8). After both filters the zero share is 63.5%, and the warning's reason has to be rewritten.
   - Lapses within the year (1-364 days; 7,025 rows, 466 in test) do not show fewer claims (31-53% against 33-48%), so I propose no filter for them. This is consistent with frempl_french_motor_personal_line, which kept early-ending records.

3. **`Policies_in_force` is not measured at the prediction point (P4, LEAK-10, the amended window clause; maybe a weak leak).** Notes bullet 12 says it "is measured per year, and it is no consequence of the year's claims". The codebook says "during the reference period".
   - Test (t9): take 2,723 pairs where a new sampled contract b of the same customer was written during policy a's first year. In 1,861 of them (68%), `Policies_in_force` of b equals that of a, so a's count already includes b, written after a's start.
   - The later part moves with the outcome. Among customer-first rows with a count of 2, those that add a policy later in the year claim at 0.24 against 0.48 (t10). But it does not help a model: replacing the count with the count minus sampled later additions raises the mean Gini from 0.229 to 0.243 (2 seeds, 9 windows; t15).
   - Remedy: keep it, with a `Potential leak, kept on purpose:` note that it is counted over the year. Additions of sampled policies can be subtracted (2,865 rows), but additions outside the sample cannot be located. The R^2 figures in the notes hold (0.042 all features, 0.019 without; leak probe JSON).

4. **Metric resolution (P6, MET-10 Weigh): a fact, not a refutation.**
   - Bootstrap SE of one window's Gini is 0.055-0.097. Random predictions score from -0.22 to +0.09 on single windows. The top 5 claims hold 20-43% of a window's cost.
   - Premium alone (0.187) against LightGBM (0.239) is within one window's SE.
   - This supports the builder's issue 5 (quarterly windows) as a weighing call.

5. **Text slips (P7 and house rules).**
   - The README metric definition reads "(ties in row order)". The scorer in the working tree averages tied predictions, so a constant scores 0, and the spec now says so. Re-run `dataset check`.
   - `row` says older contracts are "renewed from November 2015 to November 2016", and `splits_comment` says their first years "start before December 2016". In fact 48 older-contract first rows start from December 2016 to December 2017, 40 of them in test windows. These are the same 40 rows the splits comment counts.
   - "`Type_fuel` for 18% of the motorbikes": `Type_fuel` is missing on exactly the 652 rows with power 0 (610 motorbikes, 42 farm vehicles), a vehicle record without data.
   - "`Length` missing for every motorbike and 97% of the farm vehicles": true, but it is also missing for 318 cars and 105 vans.
   - "changes ... for 24% of the policies": 24.4% of policies with several rows, 15% of all policies.
   - "28-38% for those of 2017": January 2017 is 38.6%.

**Untested or cannot verify (EV-7)**

- The paper's quotes (Sec. 1 "pricing mechanisms for new business", "the pre-cleaned raw data"; the Sec. 3 quotes; "reports no model and no evaluation"): cannot verify. Springer and RODERIC return bot checks; the copy in the run folder is a 7 KB bot page, and I did not work around it. What I could read names no task and no metric: the Semantic Scholar abstract (risk profiling, claim behaviour, research and teaching) and the Mendeley description ("Each row signifies a policy transaction"). The use-case sentence of `use_case` therefore rests on the builder's reading.
- Same insurer as spanish_motor_insurance_coverage_level_2022_2024 (PROV-6, PROV-7): not tested.
- The mechanism of the carry-over: unknown. For complete years of new customers, claims per claimant fall steadily from 2.56 (2015Q4) to 1.75 (2017Q4), while mean cost per claimant stays at about 800-1,100 (t17). `N_claims_year` may count something that develops (movements), but this is inference. The target (the cost) looks stable.

**All claims**

| claim | source | test | result | evidence | rule |
|---|---|---|---|---|---|
| Use case: new-business pricing, named in the article | task_summary `use_case`; record | read the article | cannot verify | full text behind bot checks; abstract and Mendeley name no such use | USE-1, PROV-16 |
| One policy's first year; 42,159 rows; older contracts renewed Nov 2015-Nov 2016 | `row` | recount from raw | count holds, dates refuted (minor) | 42,159; 48 older-contract first rows start Dec 2016-Dec 2017 | P7 |
| The year's claim cost, 0 for 69% | `predicted` | claims by `Date_lapse`; claims of customers' later policies | refuted | 68.84% zeros, but 5,069 have no cover; 2,620 rows carry the customer's carry-over | USE-5 |
| Features known at the year's start | `known` | `Policies_in_force` of a against a later-written b | refuted (weak) | 68% of 2,723 pairs already counted b; Gini 0.229 -> 0.243 without the later part | LEAK-10 |
| Test = new contracts of a coming month | `split` | customer key against earlier policies | partly refuted | 1,097 of 7,573 test rows are known customers' later policies, claim share 0.200 against 0.363 | USE-5, SPLIT-13 |
| Fit approximate, the four gaps | `fit_reason` | the tests above | holds, incomplete | the two USE-5 gaps above are not named | USE-8 |
| Rows of a policy are consecutive years | notes 1 | the `_clean` assert on all rows | holds | assert passes | - |
| v1 2023-08-10, same rows, 3,416 cells "00/01/1900" -> 0 | notes 2 | cell diff v1 against v2 | holds | only `Distribution_channel` differs, 3,416 cells; "00/01/1900" is Excel's display of 0 | PROV-1 |
| Later rows hold almost no new claim (133/18,630; 8,942/8,951; 96.5%; Gini 0.86) | notes 3 | recount, also without no-cover rows | holds | 0.71% (0.89% without no-cover); 99.90% (99.87%) | USE-5 |
| Older contracts' first rows claim 25-27% every month | notes 3 | split by cover | holds, but includes 5,069 no-cover rows | with cover 32-35% every month | USE-5 |
| The remnant is per policy | notes 3 (implied) | a customer's later policies | refuted | 4-8% against 47-53% by the first policy's claim | USE-5 |
| 2018 dropped: 35,815 rows, 11,343 first rows, 32-36% -> 0.5% | notes 4 | recount | holds | same numbers | LEAK-24 |
| log1p target, min 40.05, zeros = `N_claims_year` 0 | notes 5 | recount, asserts | holds | 40.05; asserts pass | MET-3 |
| log1p 0.215, raw 0.059, Tweedie 0.190 | notes 6 | probe file; my LightGBM | holds | shipped_experiments; mine 0.229-0.239 on log1p | MET-3 |
| Hurdle: AUC 0.60-0.66, severity R^2 about 0 | notes 7 | probe file | holds (not re-run) | shipped_experiments | TP-2 |
| `N_claims_year` is part of the target | notes 8 | assert | holds | 0 exactly where the cost is 0 | LEAK-10 |
| History, lapse and max columns are after the prediction point; 0.73 -> 0.89 | notes 9 | codebook; probe file | holds | codebook wording; design_comparison | LEAK-10 |
| `Seniority` one value per policy, years to the last renewal for 92% | notes 10 | recount | holds | 100% constant; 92.4% of 26,524 | LEAK-10 |
| `Policies_in_force` per year, no consequence; R^2 0.042/0.019 | notes 11 | t9, t10, t15; leak JSON | R^2 holds; timing refuted | see item 3 | LEAK-10 |
| Impossible values: 22, 26, 652 (610 + 42) | notes 13 | recount | holds | same | CLEAN-11 |
| `Length` and `Type_fuel` missingness | notes 14 | recount | minor slip | fuel missing on exactly the 652 power-0 rows; `Length` also missing for 423 cars and vans | P7 |
| Premium alone 0.187, model ahead 6 of 9; premium change +0.5% / +0.5% / +2.0% | notes 15 | probe file; recount | holds | same; mine 0.187 against 0.239 | TP-4 |
| `Value_vehicle` residual AUC 0.508; drop 0.215 -> 0.205 | notes 16 | probe files | holds (not re-run) | value_vehicle.txt | LEAK-10 |
| `Payment`: dropping it changes the Gini by < 0.001 | notes 17 | probe file | holds | 0.2151 against 0.2152 | LEAK-10 |
| 3 pairs share every feature, kept | notes 18; info | recount; their split side | holds | 6 rows, Jan-Apr 2016, train only | LEAK-18 |
| 882 flat amount: 1,726 (8.8%), 91 at 1,764, 258 of 264 negligence | notes 19 | recount | holds | same | - |
| New-contract claim share 40-45% / 28-38% | notes 20 | recount | holds (rounding) | Nov 2015 39.5%, Jan 2017 38.6% | - |
| Travel assistance 56% of 7,366 | notes 21 | recount | holds | 4,156 of 7,366 | - |
| 9 monthly windows, 82-98%, 632-974 rows, 40 rows not starting on the contract date (31 within nine months) | splits | recount | holds | same | SPLIT-15 |
| Older first years start before Dec 2016 | splits | recount | refuted (minor) | 48 start later | P7 |
| 12-month gap leaves 28% | splits | recount | holds | 0.283 | SPLIT-14 |
| No shortcut from unmatured labels | splits | same-customer training labels | holds for LightGBM, refuted as a label link | sibling AUC 0.65-0.82 on 1,138 test rows; removed by fix 1 | SPLIT-9, LEAK-17 |
| Metric origin context: the source has no metric | `metric.reason` | abstract, Mendeley record | holds as far as readable | no task or metric; full text unreadable | MET-1, MET-11 |
| Gini is insurance pricing's model metric (Frees et al. 2011; Allstate 2011; Liberty Mutual 2014) | `metric.reason` | citations; sibling definitions | holds | frempl and coverage_level_2022_2024 declare the same | MET-11 |
| Largest first-year cost 260,853 = 2.3% | `metric.reason` | recount | holds | 2.27% | - |
| Computable per fold | MET-2 | `scorer` on each fold | holds | constant 0.000 on 9 of 9 folds; 177-371 claims per fold; no scoring columns needed | MET-2 |
| Scored on the amount | `target_transform` | score on log1p against expm1 predictions | holds | 0.4598 both; y_true inverted | MET-3 |
| Ties in row order | README metric block | current `metrics.py` | refuted (stale) | ties now averaged | house |
| `task_target_value_dominant`: observed claim-free years | warning | no-cover rows | refuted | 5,069 of 29,024 zeros | USE-5 |
| Screening: 81.4% zeros, 105,555 x 30, 32,923 multi-row policies | record | recount | holds | 81.39% | - |
| Assessment: keep complete years or build exposure | record | the definition | partly followed | 2018 cut; lapse at the start not handled | USE-5 |
| Same insurer as 2022-2024 | builder issue 4 | none | untested | - | PROV-6, PROV-7 |
| Raw SHA-256 values | `download_description` | sha256sum | holds | three hashes match | PROV-1 |

</details>

<details><summary>Column audit</summary>

**Column auditor (AI, 2026-11-01): spanish_motor_insurance_2015_2018**

```text
Verdict: ship after changes.
Validity: USE-7 triggered: 5,069 rows (12.0%) are years that never had cover; drop them, as the 2022-2024 sibling
  dropped its zero-exposure years. USE-5 open: a row's claim count moves with the claims of the same customer's other
  policies in force at the same time (question 2). LEAK-10 triggered for Policies_in_force: it is a count per calendar
  year and includes policies written after the row starts. The late part shows no outcome signal, so keep it with a
  note. The Value_vehicle and Payment keeps are agreed. Every dropped column is correctly dropped.
Quality: CLEAN-1: contract_years is a year too low for 5,608 rows (fix the arithmetic). CLEAN-10: fill values in the
  farm-vehicle rows (note them).
For the curator: question 2, what the target counts (a USE-5 call), and question 1, the drop.
```

Frame audited: the definition's own frame, loaded through `dataset_io.from_definition` (42,159 rows, 20 columns, the
9 shipped monthly windows). I also used the raw Mendeley v2 CSV and v1, the variable sheet, and the article's
Secs. 1-4 on the publisher's open-access page. The paper copies in the run folder are bot-check pages, so I fetched
the article myself. To link a customer's policies I used a customer key built from (`Date_birth`,
`Date_driving_licence`): 47,870 customers over 53,502 IDs. Scripts and outputs are in the run folder.

**Column table (the shipped frame)**

| column | meaning (source) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `period_start` | `Date_last_renewal`: when the row's year of cover starts. That is the contract date for a new contract and the renewal date for an older one. | yes: it is the prediction point | datetime. Every row is 365 or 366 days long (`Date_next_renewal` is start + 1 year in all 105,555 rows). Rows are sorted. It is the time column and also a feature. | fine | CLEAN-14, CLEAN-23 |
| `Distribution_channel` | 0 agent, 1 broker (sheet) | yes: one value per policy, set when the contract is written | category with labels. v1 had "00/01/1900" in 3,416 cells (2,455 policies) and v2 sets these to 0. The v1 file supports that: the same policy's other rows read "0" in 63% of those policies, and the channel is constant within a policy. | fine | CLEAN-12, CLEAN-14 |
| `Policies_in_force` | "policies held by the insured in the insurance entity during the reference period" (sheet); "the number of policies held by each policyholder within the company" (paper) | **partly**. The count covers the calendar year of the row's start, so it includes policies written later that year (problem 3). | int64, a count, correctly numeric | potential leak, keep with a note. Its meaning is tied to how the target is counted (problem 2). | LEAK-10, USE-5 |
| `Payment` | "Last payment method of the reference policy": 0 annual, 1 half-yearly (sheet) | uncertain: the last value, one per policy | category with labels | keep with the existing note, plus one pattern (problem 4) | LEAK-10 (second clause) |
| `Premium` | "Net premium amount associated with the policy during the current year" (sheet). The paper says "the amount received by the insurer in connection to a policy during the current year after deducting taxes", expenses included. | **yes**. The data shows an annual tariff, not an amount received or earned. A year that ends in a lapse keeps a full year's premium: the median ratio to the previous year is 1.015 for half-yearly payers who lapse at 170-200 days (639 rows), against 1.005 with no lapse. | float64, minimum 40.14, no zeros | fine. The evidence above strengthens the `Note:` bullet, because the paper's "received" wording suggested otherwise. | USE-6, LEAK-37 |
| `Type_risk` | 1 motorbike, 2 van, 3 passenger car, 4 agricultural (sheet) | yes | category with labels | fine | CLEAN-12 |
| `Area` | 0 rural, 1 urban (over 30,000 inhabitants) (sheet) | yes, but it is one value per policy (possibly the last one) | category with labels | fine. The bullet already says it is one value per policy. | LEAK-10 |
| `Second_driver` | 1 when several regular drivers are declared (sheet) | yes, but one value per policy | category with labels | fine (as `Area`) | LEAK-10 |
| `Power` | horsepower | yes | float64. The 652 zeros become missing. These 652 rows are exactly the rows where `Type_fuel` is missing, which the paper calls "fuel type is not available", so this is a block of vehicles without catalogue data. | fine. The bullet should call it a block without vehicle data (CLEAN-10), not an impossible value. | CLEAN-10, CLEAN-11 |
| `Cylinder_capacity` | engine size. No unit is given; the values read as cc. | yes | int64. Farm vehicles have fill blocks (problem 6). | fine, apart from the farm note | CLEAN-10 |
| `Value_vehicle` | "Market value of the vehicle on 31/12/2019" (sheet) | no (valued after every year), but it is a property of the vehicle | float64, minimum 270.46, no zeros and none missing, so a total loss does not reset it. One value per policy. No vehicle in the release was registered after a row's start year (0 of 105,555 rows). The residual has AUC 0.508 (builder). | potential leak, kept: agreed | LEAK-10 (lookup that the data shows did not change) |
| `N_doors` | number of doors | yes | int64. It is 0 for all 3,349 motorbikes, which is true. It is also 0 for 282 of the 309 farm vehicles, and 274 of those also have no `Length`, so the 0 looks like "not recorded". | question (low) | CLEAN-10 |
| `Type_fuel` | P petrol, D diesel | yes | category with labels. 652 missing, the same rows as `Power` = 0. | fine | CLEAN-14 |
| `Length` | length in metres | yes | float64. Missing for every motorbike, 301 farm vehicles, and also 105 vans and 318 cars. Missingness carries no claim signal (33.8% claim share against 32.9%). | fine. The bullet names only the motorbikes and farm vehicles. | CLEAN-10 |
| `Weight` | weight in kg | yes | int64. Farm-vehicle fill blocks (problem 6). | fine, apart from the farm note | CLEAN-10 |
| `contract_years` | whole years from `Date_start_contract` to `period_start` (built) | yes | float64. 26 contracts dated after the start become missing, which is correct. But the formula `days // 365.25` gives **one year too few for 5,608 of 23,948 older-contract rows** (problem 5). | cleaning problem | CLEAN-1 |
| `driver_age` | whole years since `Date_birth`, which is the birth date "of the insured declared in the policy". The insured is not necessarily the driver. The authors bounded birth dates to 1918-2000. | yes | int64, 18-98. 30 rows are a year low (the same formula, start date on the birthday). | fine (minor fix) | CLEAN-1 |
| `years_licensed` | whole years since `Date_driving_licence`. Every licence was issued at age 18.0 or later; the paper gives 18 as Spain's minimum age. There is no spike at the 18th birthday (119 rows), so no sign of imputation. | yes | float64. 22 licences dated after the start become missing, which is correct. 42 rows are a year low. | fine (minor fix) | CLEAN-1, CLEAN-11 |
| `vehicle_age` | the start's calendar year minus `Year_matriculation` | yes | int64, 0-67, never negative | fine | CLEAN-12 |
| `log1p_cost_claims_year` | target: log1p of `Cost_claims_year` (payments plus reserves, Sec. 3) | target | float64, no negative amounts | 5,069 rows have no cover (problem 1). What the count includes is open (problem 2). | USE-7, USE-5 |

Dropped columns, all correctly dropped: `N_claims_year` is part of the target. `N_claims_history`,
`R_Claims_history`, `Lapse`, `Date_lapse`, `Max_policies`, `Max_products` and `Seniority` are measured after the
prediction point (LEAK-10). `Date_next_renewal` is always start + 1 year. The four source dates became ages. `ID`
also goes: the paper says it identifies "the combination of policyholder and product", so the bullet's "the policy
number" is loose. `Date_lapse` should stay out of the features but is needed as the filter in problem 1. That filter
reads no label.

**Problems, ranked (principles.md: rank, then strength, then size)**

**1. P3, USE-7 (Must), with LEAK-22 and LEAK-36: 5,069 rows are years that never had cover.** These rows have
`Date_lapse` on the year's start date (4,971 rows) or before it (98). Only 14 of them have a claim (0.3%), against
35% for rows without a lapse in their year. Every one is an older contract's first row in the release, and also
that policy's last row: a renewal that was not taken up. They make up 21% of the older-contract first rows and 17.4%
of the zero-cost rows. They sit in the training rows of every window (5,052-5,068) and only 17 fall in the 9 test
windows.

The features pick them out at ROC AUC 0.64 among older contracts. Dropping them from training and test changes the
mean Gini of untuned LightGBM from 0.2230 to 0.2345 on the same test rows (paired +0.012, SE 0.012, better in 5 of
9 windows, 3 seeds). So this is no score shortcut, but these rows are not years a policy is priced for.

Precedent: `spanish_motor_insurance_coverage_level_2022_2024` drops its 49 policy-years with zero exposure ("they are
no year a policy is priced for (USE-7)"). Like cases should be treated alike.

Remedy (fix the definition): before step 3, keep only rows where `Date_lapse.isna() | (Date_lapse > Date_last_renewal)`.
The rule reads no label (LEAK-25's recovered case). The result is 37,090 rows (7,556 in the test windows). Claims to
update afterwards:
- the row count;
- the zero share: 68.8% becomes 64.6%;
- the justification of the `task_target_value_dominant` warning ("observed claim-free years"): 17% of the zeros are
  years without cover;
- the older-contract claim share: 26% becomes 33% (32-35% in each month instead of 25-27%).

The remnant argument for keeping first rows only still holds without these rows: 0.9% of the years after a
claim-free year have a claim (14,980 rows), against 0.7% with them.

The opposite view: the renewal is priced before the customer turns it down, so a non-renewal could count as an event
after the prediction point (LEAK-22's competing-event clause, framingham). It does not apply here, because no premium
is earned on these rows either. A pure premium is a cost per year at risk.

**2. P3, USE-5 (Must), a question for the curator: a row's claims move with the claims of the customer's other
policies.**

The evidence comes from pairs of rows of one customer on different policies (complete years, rows with cover only).
The claim chance on policy B, given a claim on policy A, rises with how long their years overlap:

| overlap of the two years | P(claim on B, given a claim on A) | P(claim on B, given none on A) |
|---|---|---|
| 90 days or less | 0.42 | 0.08 |
| 180-270 days | 0.68 | 0.07 |
| 350 days or more | 0.90 | 0.04 |

Where either row has a claim, the claim counts are equal in 1% of the short-overlap pairs and 69% of the full-overlap
pairs. The costs are almost never equal (0-2%). As a control, the same customer's years more than 180 days apart give
0.21 against 0.12: a mild customer effect. Of the 1,532 first-row pairs that overlap by more than 180 days, 1,519
insure different vehicles, so a shared vehicle does not explain it.

This fits the article's "the number of claims that the insured has made during the current year": a count at least
partly per insured, across the insured's policies. It also explains the builder's own customer-level table:
claims per policy-year grow almost in proportion to `Policies_in_force`, at about 0.40-0.56 per policy in force for
counts 1-6. The `Policies_in_force` bullet's explanation ("customers with more policies ... have more claims per
policy") is therefore at best incomplete. In part the count scales a claim count that spans the customer's policies.

This is no cross-split shortcut: dropping the training rows of customers who also have a test row leaves the Gini
unchanged (0.229 against 0.223 for a random drop of the same size; difference +0.006, SE 0.008). But it does bear on
what the target is, and 45% of the test rows have `Policies_in_force` of 2 or more (29% of all rows). Options:
- (a) state it in a note and rewrite the `Policies_in_force` bullet and `fit_reason`. The fit is already
  approximate. This is the mildest option.
- (b) keep only `Policies_in_force == 1`, where the count can only be the policy's own. That leaves 25,665 rows after
  problem 1's filter.
- (c) ask the authors how `N_claims_year` is counted (PROV-13; they offer the pre-cleaned raw data).

**3. P4, LEAK-10 (Must; window clause, the curator decides case by case): `Policies_in_force` is a count per
calendar year.**

Take rows of policy A where the same customer's policy B was written strictly inside A's year (797 rows that have a
previous and a next row):
- B written in the same calendar year as A's start: the count rises at A's row in 80% of cases and at A's next row
  in 10%.
- B written in the next calendar year: 17% and 84%.
- Base rate of a rise by one: 5.0% (from the previous row) and 5.8% (to the next row).

A policy that lapses later in the same calendar year is still counted, and drops at the next row in 70% of cases. So
the value is "policies held at some time in the calendar year in which the row starts". For a row that starts in
March, that includes policies written up to December. The bullet's "changes from one row to the next ... so it is
measured per year" is true, but the year is the calendar year, not the year of cover.

The late part carries no outcome signal. 1,772 first rows have a sibling policy written later within their year, and
their claim share equals that of the other rows (31.2% against 31.2%). At a given count it is lower (27% against 36%
at a count of 2; 26% against 43% at 3), because the inflated count brings no matching risk. 870 first rows (2.1%) and
236 test rows have such a sibling in the sample; more come from policies outside the sample.

The value cannot be rebuilt as of the start, because the other policies are mostly not in the release. Remedy: keep
it, and turn the bullet into a `Potential leak, kept on purpose:` note with these numbers. Also say "in the calendar
year" in `task_summary.known`.

**4. P4, LEAK-10 (second clause, weak): `Payment` is a last value.** This adds to the existing note and needs no
change in code. Among first rows that started before November 2017:
- in policies that renewed, 26% of claim-free first years are half-yearly, against 40% of those with a claim;
- in policies that lapsed in their first year (one row, so the recorded value is presumably that year's), 78%
  against 82%.

Two explanations fit: a later switch to half-yearly payment after a claim, or survival selection (half-yearly payers
without a claim lapse, for non-payment at six months, more often). The data cannot tell them apart. Dropping the
column costs nothing (Gini 0.215 either way, builder). Keeping it with the note is consistent with LEAK-10's second
clause. Add the pattern to the note, or drop the column. `Area`, `Second_driver` and `Distribution_channel` are also
one value per policy. They show no such pattern worth acting on.

**5. P7, CLEAN-1 (Should; cheap and safe): `contract_years` is a year too low for 5,608 older-contract rows (23%).**
A renewal falls exactly on the contract's anniversary. At that point `days // 365.25` loses a year unless the span
holds enough 29 Februaries. As a result:
- all 2,185 one-year-old contracts renewed in 2015-Q4 and 62% of those in 2016-Q1 read 0, the value of a new
  contract;
- none from 2016-Q2 on does, so the error is confounded with `period_start`;
- at higher ages, 1,210 rows read 1 instead of 2, 594 read 2 instead of 3, and so on.

The same formula puts `driver_age` a year low in 30 rows and `years_licensed` in 42 (a start date on the birthday or
licence anniversary). The test rows are new contracts with the correct value 0, so the score barely moves. But the
column contradicts the bullet's "ages at the year's start, in whole years". Remedy: calendar arithmetic for all
three ages:

```python
def _whole_years(since: pd.Series, at: pd.Series) -> pd.Series:
    """Completed years from `since` to `at`."""
    before = (at.dt.month < since.dt.month) | ((at.dt.month == since.dt.month) & (at.dt.day < since.dt.day))
    return at.dt.year - since.dt.year - before.astype(int)
```

**6. P7, CLEAN-10 (Should; a question, low): fill values in the farm-vehicle rows.** 150 of the 309 farm vehicles
fall in three blocks. Within each block the engine size, weight and value are identical, but the power varies and
the vehicles range from 6 to 66 years old:
- 76 rows: 4,525 cc, 4,525 kg, value 42,920;
- 42 rows: 4,400 cc, 4,800 kg, value 42,185;
- 32 rows: 2,970 cc, 1,850 kg, value 25,520.

The paper says the authors "amend the presence of zero values with respect to the absolute frequency of each
variable", which may be where these come from. In addition, `N_doors` is 0 for 282 farm vehicles. Only 2 test rows
fall in the blocks; 32 of the 37 test farm vehicles have 0 doors. Mildest remedy: an `Anomaly:` note. Setting the
blocks and the farm-vehicle 0 doors to missing is the alternative.

**7. P7, notes only.** Say that `Power` = 0 and missing `Type_fuel` are the same 652 rows (the paper's "fuel type is
not available"). Say that `Length` is also missing for 423 cars and vans. Describe `ID` as the policyholder-product
identifier, in the paper's words.

**Checked and agreed:** the `Premium` keep (USE-6), with the evidence that it is not earned or prorated. The
`Value_vehicle` keep. Every dropped column. The v2 channel correction. The label coding of all six categoricals.

</details>

<details><summary>Split audit</summary>

**Split audit (split-auditor, 2026-11-01): spanish_motor_insurance_2015_2018**

**Verdict: right with notes. One change is recommended (a 12-month gap with 5 monthly windows); the curator decides.**
The regime, the time column, the test population and the expanding train side all fit the use case. The gap does
not. The definition trains with no gap and proposes an exception to SPLIT-10 "as for lending_club and
alfa_battle_2_0_task_2". Those two exceptions rest on one fact: with the label's delay as the gap, no window keeps 50%
of the rows for training. Here that fact does not hold. A 12-month gap (a year's claims are known when the year ends)
leaves 5 monthly windows, August to December 2017, that keep 56-76% of the rows. So the exception would serve
SPLIT-15 (the number of windows, a Should). At equal strength the earlier rule wins, and that rule is SPLIT-10. In
measured score the gap costs about nothing.

Numbers are from my own runs on 2026-11-01, unless the line says otherwise. The frame and the 9 shipped splits were
rebuilt from the definition through `dataset_io.load(..., built=False)`; the folder is not built yet. The model is
untuned LightGBM with the builder's parameters from `shipped_experiments.py`. My mean Gini on the shipped windows is
0.239, while the builder's run gives 0.215. Single windows differ too (April 2017: 0.460 against 0.392). That
difference is itself a sign of the per-window noise (EV-8). The scripts are in the run folder.

**Regime and time column (pass)**

- The use case is new-business pricing ("pricing mechanisms for new business", Sec. 1). A new contract is always a
  new policy, and a refit tariff is applied to the contracts that follow. That makes the split temporal (SPLIT-1,
  SPLIT-6). One row per policy leaves no policy on both sides of the split.
- The time column `period_start` is `Date_last_renewal`, the start of the year of cover. For a new contract this is
  the day it is written. In the test windows, 7,533 of 7,573 rows start on the contract date. Of the other 40, 31
  start within 263 days after the contract date, and 9 have a contract dated after the year's start. These numbers
  are verified as written in `splits_comment`.
- The 9 windows are calendar months, April to December 2017, newest first. They hold 632 to 974 test rows and 177 to
  371 claims each. The train side is expanding and holds 82.0-97.7% of the rows. This matches the README table.
  SPLIT-11, SPLIT-14 and SPLIT-17 hold.
- All 23,948 first rows of older contracts (56.8% of the rows) are renewals and train only. The test rows are new
  business, which is the population the use case names. The time column stays a feature, so the drift in claim share
  from 2016 to 2017 is visible to the models.

**1. The no-gap exception to SPLIT-10 rests on a fact that does not hold here (P4; SPLIT-10, Should; SPLIT-9's
tension row; SPLIT-14, SPLIT-15)**

- How many training labels are unknown at the prediction point (SPLIT-9): these are the training rows whose year had
  not ended by the window's start. There are 9,033 of 41,185 in the December window (21.9%), and the share rises
  window by window to 22,307 of 34,586 in April (64.5%). In 4 of the 9 windows they are more than 44% of the training
  side.
- Which windows meet the floor with a 12-month gap (built with the package's own
  `TemporalSplits(window=1, unit="months", gap=12, min_train_fraction=0.5)`): 5 windows, August to December 2017. They
  train on 23,472 to 32,092 rows (55.7% to 76.1%), with the training side ending on 2016-11-30 for the December
  window, and hold 4,373 test rows. July would fall to 47.8%. So SPLIT-14 (at least 3 windows, at least 50% for
  training) is met.
- The splits comment says "a twelve-month gap leaves 28% of the rows for training in the oldest window". That is true
  only for April 2017, which is the 9-window layout.
- What the gap costs in score:

  | Design | Mean Gini | Claim AUC |
  |---|---|---|
  | August-December, 12-month gap | 0.181 | 0.621 |
  | Same windows, no gap | 0.185 | 0.635 |
  | 9 windows, 12-month gap (floor broken) | 0.209 | not run |
  | 9 shipped windows, no gap | 0.239 | 0.635 |

  The builder's 6-month gap gave 0.223 against 0.215. Neither the builder's runs nor mine show a shortcut from the
  unmatured labels, and the gap costs about nothing. So the choice is about an honest protocol, not about the score.
- Precedents: lending_club (12-month gap: 33-46% for training) and alfa_battle_2_0_task_2 (6-month gap: 35-53%) had
  no window layout that met the floor. Their exceptions record "Serves SPLIT-14". Here the floor is met, so these
  precedents do not fit.
- The builder's issue 2 calls this "the third exception for this reason, amendment due". That does not hold either:
  the reason differs, so it does not count toward an amendment.
- The siblings in the family train only on finished years:
  - frempl_french_motor_personal_line trained "only on records whose period had ended by the cutoff". When that broke
    the floor, it went ForcedGroupedFromTemporal; it did not drop the gap.
  - spanish_motor_insurance_coverage_level_2022_2024 tests 2024 against the complete years 2022-2023.
  - wisconsin_local_government_property_insurance_fund tests a policy year against the finished years before it.
- This is a consistency flag (principles.md, case 2).
- Remedy, the mildest first:
  - (a) Re-split as
    `TemporalSplits(window=1, unit="months", gap=12, min_train_fraction=0.5)`: 5 windows, August-December 2017.
    Update `splits_comment` and `task_summary.split` to say "trained on the policy-years that had ended by the
    window's start". This also meets SPLIT-9 with no further filter (item 2).
  - (b) Keep the 9 windows and record an exception to SPLIT-10 whose fact is true: the window count and the test pool
    (7,573 rows against 4,373), that is SPLIT-15. This would be a new reason that departs for a later Should. If the
    curator takes (b), also apply the filter in item 2, as for alfa_battle_2_0_task_2.

**2. A customer's concurrent policies share outcomes across the cutoff; a model cannot reach this through the shipped
features (P4; SPLIT-9, Must: holds; SPLIT-24; precedent alfa_battle_2_0_task_2)**

- The customer key is birth date plus licence date, built exactly from two raw columns (SPLIT-24). It is no cluster.
  It gives 38,885 keys over 42,159 rows. Within keys of two or more rows, channel and area are constant in 98.3%,
  `Max_products` in 98.5% and `Max_policies` in 94.3%.
- 1,138 of the 7,573 test rows (15.0%; 92 to 153 per window) have a same-customer policy on the training side.
  For 579 of them, that policy's year had not ended at the window's start.
- The training label tells the test row's outcome:

  | Earlier policy of the same customer | Test rows | Claim share |
  |---|---|---|
  | Year overlapping the test row's, with a claim | 184 | 58.7% |
  | Year overlapping the test row's, claim-free | 352 | 7.1% |
  | Year ended before the test row starts, with a claim | 208 | 26.9% |
  | Year ended before the test row starts, claim-free | 418 | 9.1% |
  | No earlier policy | 6,435 | 36.8% |

  These rows come from all policies earlier in the release (1,162 test rows in all).
- It is not two covers on one vehicle: only 166 of 2,028 pairs share all 7 vehicle columns. Overlapping pairs on
  different vehicles still show 61.3% against 7.0%.
- A model cannot reach the link through the features:
  - A lookup on area, channel, `Policies_in_force`, `Payment`, `Second_driver` and birth and licence year (±1) among
    the unmatured training rows finds a median of 5 candidates. It finds the true customer for only 210 of about 570
    rows. The test claim share is 30.8% when a candidate claimed and 32.3% when none did.
  - The alfa-style filter drops the 106-182 training rows per window that belong to customers with a test-window
    policy. LightGBM's mean Gini moves from 0.239 to 0.234 and its claim AUC from 0.6355 to 0.6378.
- So SPLIT-9's measurable shortcut is not shown, and the rule holds.
- Remedy: none is needed if the 12-month gap of item 1 is taken, since it removes every unmatured training row. If
  the curator keeps no gap, drop those 106-182 training rows per window (0.3-0.4% of the training side). This treats
  the case like alfa_battle_2_0_task_2, which was filtered at a score effect of 0.002-0.009. The key has to be built in
  `_clean` before the dates are dropped.

**3. The two newest windows rank near zero: keep them (P4; SPLIT-21, Must; SPLIT-20, Should; LEAK-24 checked)**

- November and December 2017: my LightGBM scores 0.034 and 0.007, and the premium alone 0.075 and 0.054. Claim AUC is
  still 0.641 and 0.609.
- I found no sign of run-off in their labels. Every measure sits within the range of the 2017 months:

  | Measure | November | December | 2017 months |
  |---|---|---|---|
  | Claim share | 36.5% | 38.1% | 28-39% |
  | Share of positive costs on the 10 most common values | 0.193 | 0.189 | 0.164-0.244 |
  | 99th percentile of positive costs | 8,257 | 7,464 | 3,275-12,447 |
  | Spearman rank correlation of premium and severity | 0.138 | 0.080 | 0.047-0.226 |

- Each month's Gini is noisy. Over 300 bootstrap resamples of the test rows, its standard error is 0.049-0.111 (mean
  0.079). Quarterly windows halve it (0.043-0.057), but with a 12-month gap only 2017-Q4 keeps 50% for training (67.5%).
- Reading: window noise from heavy-tailed costs, maybe added to by the reserves of the least developed claims (Sec. 3:
  "the most recent claims exhibit a run-off with pending developments"). Only the claims by date would settle it, and
  the release has none.
- Do not cut these months or shift the windows because of their scores (SPLIT-21). Under remedy (a), 2 of the 5
  windows are these months. Say so in `splits_comment`.
- Season (SPLIT-20): the 5 gap windows run from August to December, when motorbikes are 4-9% of new contracts,
  against 12-14% in June and July 2017. A cover lasts a year, so claim seasonality averages out. This is a minor note,
  no change.

**4. Customers recur across the cutoff; this is part of the task (P4; SPLIT-13, Should; USE-10)**

- 15.0% of the test rows have a same-customer policy in training. The use case prices a new contract, and the
  customer may be one the insurer already knows. That makes the recurrence part of the task, not a reason to group.
- For a known customer, the history that had matured by the prediction point is legitimate (USE-10): a claim-free
  earlier year goes with a 9.1% claim share, one with a claim with 26.9%.
- The release drops `N_claims_history`, because it covers the whole duration. A rebuilt history would be a feature the
  use case has: the customer's claims on policy-years that ended before the row's start. This is a column question for
  the column-auditor, not a split change.

**5. Wording (P4; EV-7)**

- `splits_comment`: "the older contracts' first years in the release start before December 2016". Strictly, 48 start
  later: the 40 test rows already disclosed, and 8 more from December 2016 to March 2017. A small fix.
- "as for lending_club and alfa_battle_2_0_task_2" should go, or be reworded, whatever the curator decides on item 1.

**Outside the split, a higher rank, for the claim, column and domain reviewers (P3; USE-5; PROV-13; maybe)**

The co-occurrence in item 2 extends the builder's issue 1 (later rows hold a remnant of the claims) to first rows.

- Concurrent policies of one customer on different vehicles claim together far more than independent risks would:
  61.3% against 7.0%.
- Among the 510 overlapping pairs with a claim on both policies:
  - the claim counts are equal in 43.7% (9.8% for pairs that do not overlap);
  - the costs are not copied: they are equal in 1.8%, against 0.8% for random pairs of claimants;
  - the claim-type sample shares an identical type and cost entry for one customer only.
- So claims may be counted at the customer level, or this is a strong customer effect. The release cannot tell them
  apart.
- If claims are counted at the customer level, the label of a first row of a customer with several policies is not
  the policy's own year (about 15% of the test rows). The authors' "pre-cleaned raw data" with claim dates would
  settle it.

**Checks that pass (one line each, EV-7)**

- Near copies across the split (hidden-group probe): 1.9% of the rows are in clusters at similarity 0.85, and 1.5% of
  the test rows are seen in training. The 3 pairs of identical policies are kept under LEAK-18.
- Hidden groups among the columns: none (temporal: no hits; best composite key 0.1%).
- Grouped regime: not applicable. The policy is the entity and has one row, so no group id is needed.
- IID alternative: not run. The use case leaves no doubt that the task is temporal (SPLIT-1).
- Horizon (SPLIT-12): the source states none. A monthly refit is written down as the reasoning, and is acceptable.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner (2026-11-01): spanish_motor_insurance_2015_2018**

**The actor.** I am the pricing actuary of a Spanish non-life insurer. The definition names the decision: when a new motor contract is quoted, I estimate its first-year claim cost to rank the risk and set the premium (USE-1). The data article lists "pricing mechanisms for new business" next to renewal pricing, risk selection and underwriting standards (Segura-Gisbert, Lledó and Pavía 2025, Sec. 1). Renewal pricing cannot be served here, because the later yearly rows record almost no new claims. New business is the only use left, and the test windows hold new contracts, which is the right population.

**Fit: approximate (agree).** These are real new contracts, with the insurer's own rating factors and premium, taken at the quote and tested on the next months' new business. But the claim attribution across years is undocumented and leaves only the first year usable (USE-5). The rows carry no exposure, and 4,971 training rows have none at all. The cover bought is missing too. USE-9 gives no way out: even a reframed underwriting-review use case keeps the unverified label definition, which USE-8 counts as a known gap. One wording point under USE-8: `fit_reason` lists the 31/12/2019 vehicle value as a gap. The definition itself keeps it as a potential leak on purpose, so it should be named as kept, not counted toward the fit.

**1. Inputs at the moment of the quote**

- I have every shipped input when I quote a new contract:
  - the vehicle: type, age, power, engine size, doors, fuel, length, weight, all from the vehicle database;
  - the driver's age and years licensed, and a second driver;
  - rural or urban area;
  - the channel and the payment frequency;
  - the customer's other policies with us;
  - the contract's age (0 for new business);
  - the calendar date.
- `Premium` is my own quoted price. I checked that it is the annual written premium, not the amount collected in the year, even though the article says "the amount received ... during the current year". On the 2,055 first rows whose policy lapsed inside the year (median 183 days; 1,632 of them half-yearly payers who stopped paying), the median premium is not lower than on full years, for every vehicle type, and its Spearman correlation with the share of the year in force is 0.05. So it is known at the quote, and USE-6 allows it.
- Two inputs carry later information: `Value_vehicle` (valued 31/12/2019) and `Payment` (the "last" payment method). At the quote I would have the value on that day, which ranks vehicles almost the same way. The builder measured both as negligible (residual AUC 0.508; less than 0.001 Gini). Keeping them is fine.
- Inputs I always have and that are missing, ranked by weight:
  1. The cover bought: third-party only, extended third-party, or comprehensive with or without excess. This is the largest driver of cost; the 2022-2024 sibling ships it as `policy_type`.
  2. The driver's history from the industry claims file. Spanish insurers query SINCO/SIHSA (run by TIREA, five years of contracts and claims) for a new customer, and it sets the bonus level.
  3. The postcode or province (here only rural/urban).
  4. The make, model and use of the vehicle.
- Gender is rightly absent: EU pricing has been unisex since 21 December 2012 (Test-Achats, CJEU C-236/09).
- The premium stands in for the missing four. Premium alone ranks at a Gini of 0.187, against 0.215 for an untuned model on everything. This changes the task: it is "where is my quoted premium wrong", not "build the tariff". That is a real actuarial task (tariff refinement, underwriting review of the month's new business), but the use case should say so.

**2. The target**

- I act on the expected claim cost of a policy-year, the pure premium. I want a number, built in practice as frequency times severity per cover. The shipped target is the first year's incurred cost (payments plus reserves), which is the right quantity in kind. The gaps:
- **Claim attribution across years is undocumented (USE-5, the biggest gap).**
  - The builder's remnant finding holds after the fix below. On later rows in force at their start, a claim follows a claim-free year in 0.9% of cases (15,114 rows), and after a year with claims the count falls in 99.9% of cases.
  - So only the first release year is a claims year. For older contracts it may still mix in claims open from before November 2015.
  - One pattern I cannot explain: claims per claimant among new contracts fall from 2.57 (written 2015Q4) to 1.88 (2017Q4). Policies of 2015Q4 still in force 3-4 years show 2.84-2.93, against 1.98 for those that ended after one year. Late reporting explains part of it. Some later claims may also be counted on the first row.
  - The authors' pre-cleaned raw data would settle it (PROV-13).
- **Rows that are no year of cover.**
  - 4,971 shipped rows (11.8% of the dataset, 20.8% of the older contracts' first rows) start on the policy's own lapse date. The policy was not renewed at that date.
  - These rows have 14 claims (0.28%), against 33.1% for the older contracts' first rows that were in force.
  - Nobody prices a year that is not in force, so these rows should go (USE-7). This is the sibling's precedent: `spanish_motor_insurance_coverage_level_2022_2024` dropped its 49 policy-years with exposure 0 as "no year a policy is priced for".
  - The rows sit in training (16 of the 7,573 test rows), so the score hardly moves. My untuned LightGBM on log1p over the 9 shipped windows: mean normalized Gini 0.237 with them, 0.243 without, better in 3 of 9.
  - They do skew the definition's statements. The claim share of older contracts' first rows is 32-35% in every renewal month from November 2015 to November 2016, not 25-27%. The zero share is 64.7%, not 68.8%.
- **No exposure.** The 2,055 first rows cut short inside the year (about 6% of the test rows) count as full years. In my practice they would carry earned exposure as a weight. Their cut is only known when the policy ends (LEAK-10), so keeping them unweighted, as the price of an annual contract, is defensible. It should be named.
- **The covers are mixed.**
  - In the claim-type sample, travel assistance is 56% of the claims (4,156 of 7,366) but 10% of the cost (median 70 EUR). At-fault liability ("negligence") is 10% of the claims and 46% of the cost, median exactly 882: the CICOS module, the flat amount at which Spanish insurers settle agreed claims between them.
  - The claim indicator therefore mostly measures assistance use. This is why claim AUC 0.60-0.66 turns into a cost Gini near 0.2. It is the insurer's real cost, so keep it as recorded.

**3. Row and test data**

- One row is one policy's first year, which is one quote: it matches my decision.
- The test windows hold the next month's new contracts, trained on everything earlier. That is what I face.
- No gap: training uses full-year outcomes of contracts written in the 12 months before the window, which I would not yet have at a refit. The builder's six-month-gap check (0.223 against 0.215) shows no shortcut, so the SPLIT-10 exception is acceptable.
- One month is not how I judge a tariff. Each window has 632-974 contracts and about 300 claimants, and the Gini per window runs from -0.01 to 0.39. I revise and judge a tariff quarterly or yearly.
- November and December 2017 rank near 0 for every model, the premium included. These are the least developed months: years ending at the 2018 claims cut-off, with run-off pending. I would not trust them as a test of a model.

**4. Would I use it?**

As a benchmark of how well a learner refines a quoted premium from a small set of rating factors, yes: the signal level is typical of motor pricing. As a tariff, no: the cover, the claims history and the territory are missing.

- I would trust it more if:
  - the not-in-force rows were dropped;
  - the use case named the premium's role;
  - the windows were quarterly;
  - the authors confirmed how claims are assigned to rows.
- I distrust:
  - the undocumented label;
  - the two immature months;
  - a target in which the frequency is mostly roadside assistance.

**5. Metric: partly (close to yes)**

- `normalized_gini` on the amount, each policy weighted equally, scores how well a model ranks risks. That is what I compare pricing models on. It is also what the insurers' own Kaggle competitions chose: Allstate 2011, and Liberty Mutual 2014, whose Gini was weighted by a column the competition did not label (likely exposure or insured value).
- Its unit is the contract I price (MET-1).
- It ignores the price level, which I rebase anyway. It is scale-free, so the log1p shipping cannot hurt it (MET-3).
- It does not score the size of the relativities, and a premium charges those. A model that ranks correctly but flattens the differences between risks would price wrongly and still keep its Gini. The Gini is strictly consistent only among auto-calibrated models (Wüthrich 2023, European Actuarial Journal).
- To pick a tariff model I would use it together with a Tweedie deviance (power about 1.5) on the amount, the strictly consistent score for a mean cost (the regression analogue of MET-8), and a double-lift check against the current premium.
- I would still not switch the single declared metric:
  - Tweedie deviance would need the target shipped raw, or predictions corrected for the bias of inverting log1p.
  - Frees, Meyers and Cummings' premium-based Gini would need `Premium` as a scoring column, and it is a feature (MET-2).
  - Gini keeps the family consistent.
- MET-6/MET-7 do not apply: no threshold, k or cost matrix is fixed by the source.
- The metric reason should be corrected. It cites Frees, Meyers and Cummings (2011), whose Gini orders policies by the ratio of score to premium and puts premium shares on the x-axis. The declared metric is the Kaggle form: losses ordered by the prediction, every policy weight 1.
- Quarterly windows would also make the score less noisy (MET-10, resolution).

**What an expert would change (recommendations; the curator decides)**

1. Drop the rows whose year starts on the policy's lapse date (`Date_lapse == Date_last_renewal`; 4,971 rows, 16 in test) under USE-7. Re-measure the comments' numbers: the older contracts' claim share, the zero share, and the 26% contrast in the remnant bullet.
2. Reword `use_case`: underwriting review or tariff refinement of the month's new business, given the quoted premium (USE-6), rather than setting the premium from the rating factors alone. Name the missing cover, history and territory in `fit_reason`. Move `Value_vehicle` there from the gaps to "kept" (USE-8).
3. Name the cut-short first years in the notes (about 2,055 rows; median 183 days; mostly half-yearly payers who stopped paying): kept unweighted, with the cut known only at the end.
4. Weigh quarterly test windows (3 x 2,300-2,800 rows). They match the tariff cycle and steady the score (MET-10). Flag November-December 2017 as immature.
5. Ask the authors for the pre-cleaned raw data (PROV-13). It would settle the label and could open renewal pricing with the policy's own claim history (USE-10).
6. In the metric reason, name the Kaggle form of the Gini and keep Frees et al. as the background.

**Sources**

- Segura-Gisbert, Lledó, Pavía (2025), European Actuarial Journal 15:241-253, Secs. 1 and 3 (publisher page: https://link.springer.com/article/10.1007/s13385-024-00398-0).
- The Mendeley files (portfolio, variable sheet, "sample type claim.csv").
- SINCO/SIHSA: https://www.mapfre.es/particulares/seguros-de-coche/articulos/que-es-fichero-sinco/ and Reale's FHSA notice https://www.reale.es/es/Documents/INFORMACI%C3%93N%20AL%20ASEGURADO%20FICHERO%20HISTORICO%20DE%20SEGUROS%20DEL%20AUTOMOVIL%20(FHSA).pdf.
- CICOS module (coste medio sectorial): https://documentacion.fundacionmapfre.org/documentacion/es/media/group/1066013.do.
- Frees, Meyers, Cummings (2011), JASA 106:1085-1098 (abstract via the cplm documentation: https://search.r-project.org/CRAN/refmans/cplm/html/gini.html).
- Wüthrich (2023), "Model selection with Gini indices under auto-calibration": https://arxiv.org/abs/2207.14372.
- Liberty Mutual 2014 weighted Gini: https://casact.org/sites/default/files/presentation/rpm_2015_handouts_paper_3897_handout_2469_0.pdf.
- Sibling definitions `spanish_motor_insurance_coverage_level_2022_2024`, `frempl_french_motor_personal_line` and `australian_vehicle_insurance_2004_2005`.
- My probes, in the run folder (exposure and lapse, rows not in force, the remnant without them, severity by cohort, claims per claimant by survival, Gini with and without the rows not in force).

</details>

<details><summary>Blind review</summary>

**Verdict: include with changes.** This is real, openly licensed motor insurance data, and the leaky columns have been removed. But 11.8% of rows are policies that ended on their renewal date (zero exposure) yet carry a cost of 0. And keeping one row per policy turns every 2017 row into new business. Both must be fixed before the temporal scores mean anything.

**The task.** A Spanish non-life insurer sets the price of a motor policy at its annual renewal, or when a new contract is written. The prediction is the claims cost for that policy-year (log1p of euros), made from the policyholder, the vehicle and the contract. This is a core pricing and underwriting task. The source names "pricing exercises" and "underwriting and risk selection" as intended uses (Segura-Gisbert, Lledó & Pavía, European Actuarial Journal 15, 2025).

**How the table was built (reconstructed from the public file).**
- I downloaded `Motor vehicle insurance data.csv` from Mendeley v2. Its sha256 (00061a64...293a) matches the hash Mendeley lists. It has 105,555 rows and 53,502 IDs.
- The prepared table is exactly the first row of each ID by `Date_last_renewal`, minus the IDs first seen in 2018. Per-year counts match exactly: 4,559 / 28,095 / 9,505 = 42,159.
- `period_start` = `Date_last_renewal`. The target = log1p(`Cost_claims_year`).
- These columns were dropped, and correctly so, since each is the outcome or measured after the period: ID, Seniority, Max_policies, Max_products, Lapse, Date_lapse, N_claims_year, N_claims_history and R_Claims_history.
- Derived columns: driver_age, years_licensed, vehicle_age and contract_years.

**Concerns, most to least serious**

1. **Zero-exposure rows are labelled as zero-cost policy-years (most serious).**
   - Evidence: 4,971 rows (11.8%) have `Date_lapse == Date_last_renewal` in the source, so the contract ended on the day the annuity would start.
     - All of them are single-row IDs, and 0.28% have any claim, against 35.3% for full-year rows.
     - The source defines Lapse as "Number of policies that the customer has cancelled or has been cancelled for nonpayment in the current year". These are non-renewals, not insured years.
   - Their share depends on time: 16.4%, 16.0%, 16.5%, 14.8% and 10.6% in 2015Q4 to 2016Q4, then 0.1–0.2% in every 2017 quarter.
   - The features partly identify them: 5-fold AUC of 0.72 within 2015–16, mostly through contract_years. So models learn a rule ("old contract, may be a structural zero") from training data that does not hold in the 2017 test rows.
   - Another 2,055 rows (4.9%) are only partly exposed (they lapse mid-year), and there is no exposure column.
   - Change: drop the zero-exposure rows using the source `Date_lapse == Date_last_renewal`. Optionally add exposure as a sample weight, or use cost per exposure as the target. Do not give exposure to models as a feature.

2. **Keeping one row per policy makes the later test windows a different population.**
   - Rows from Nov 2015 to Oct 2016 cover one full renewal cycle of the book. That is about 2,300–3,300 rows per month, of which 24–27% are new business.
   - From Nov 2016 on, every renewing policy has already appeared, so the 2017 rows are 99.5% new business. contract_years is 0 in 100% of 2017 rows, against 24–48% per quarter before.
   - Other shifts in 2017:
     - Monthly volume drops to 550–970.
     - Mean Policies_in_force rises from 1.32 to 1.73.
     - The share of rows with any claim rises from about 30% to 34–36%.
   - So any test window after Oct 2016 measures transfer from the existing book to new business. That mix comes from the deduplication, not from how an insurer would use the model, since a real insurer scores renewals and new business together.
   - I emulated 9 equal-count expanding windows over the last 45% of rows with LightGBM:
     - R² was 0.047–0.077 in the 2016 windows and 0.039–0.061 in the 2017 windows.
     - Predicting the training mean gives R² down to −0.022.
     - Trained on 2015–16 and tested on 2017, the model's mean prediction is 2.28 against an actual 1.99.
   - Change: keep only the first cycle (`period_start < 2016-11-01`, which is 31,243 rows, or 26,317 after dropping zero-exposure rows) and split by time inside it. On that design LightGBM R² is about 0.06 on Jul–Oct 2016. Alternatively, publish the 2017 new business as a separate, labelled task. Using every policy-year with prior-year claims as features would be more realistic, but concern 4 makes that risky.

3. **The target scale is awkward and the signal is weak.**
   - log1p cost under squared error estimates something like a geometric mean, not the expected cost that pricing needs.
   - 68.8% of rows are zero, and the tail reaches 260,853 euros.
   - LightGBM reaches R² of about 0.05 (0.046 without Premium), and AUC 0.64 for "any claim". That is realistic for policy-level claims, but differences between methods on windows of about 4k rows will be small next to the noise.
   - Costs include reserves, not only settled payments:
     - 882.00 occurs 1,161 times (8.8% of non-zero targets), and 1,764 = 2×882 occurs 62 times. These look like standard reserve amounts.
     - The paper says "the most recent claims exhibit a run-off with pending developments".
   - This is acceptable for a regression benchmark if the scale is stated. Excluding 2018 starts, as was done, is the right call because of run-off.

4. **The source has an unexplained pattern in how claims are attributed to years.**
   - In the full source, the share of rows with any claim falls with the row's position inside an ID, even within one calendar year:
     - 2016: 30.2% for first rows vs 12.2% for second rows.
     - 2017: 34.6%, 11.7% and 7.4% for first, second and third rows.
     - The 892 fourth rows (2018) have 0.1%.
   - Claims run-off cannot explain this, because the comparison is within one calendar year. Cumulative attribution cannot explain it either: the first-row claim share falls with contract age, from 30% at 0 years to 18% at 10+ years.
   - The prepared table uses only first rows, so it is internally consistent. But its target is "cost in the first annuity seen in the extract", and 31% of its rows are non-zero against 18.6% in the source.
   - I could not resolve this. It is worth asking the authors before treating the target as a clean annual cost.

5. **Some features are timed loosely (minor).**
   - Value_vehicle is the "Market value of the vehicle on 31/12/2019", taken after every period. It is a vehicle attribute, not driven by the outcome, but it is lower than the value known when the quote was made.
   - Policies_in_force is defined "during the reference period", and Payment is the "Last payment method". Both could reflect changes during the year.
   - Policies_in_force tracks claims strongly, which I could not explain:
     - The share of rows with any claim is 28% at 1 policy and 61–65% at 6–7 policies.
     - Among claimants, the mean claim count rises from 2.0 to 5.3 with Policies_in_force.
     - Claim costs are not copied across a person's IDs: only 12 of 1,355 matched.
   - Premium is the insurer's own tariff. It is legitimately known at renewal and not prorated: zero-exposure rows still carry the full premium, median 309 euros. It is the top feature by gain (16.5%), so the benchmark partly measures learning what the tariff misses.

6. **Preparation details (minor).**
   - `period_start` is a datetime column. It should serve only as the split key, or be explicitly flagged as not a feature.
   - Missing values are structural and correctly left as NaN:
     - Power and Type_fuel: 652 (610 motorbikes, 42 agricultural vehicles).
     - Length: 4,073 (all 3,349 motorbikes plus 724 others).
     - N_doors = 0 and Weight < 300 kg for motorbikes.
     - contract_years NaN in 26 rows where the start date is after the renewal date; years_licensed NaN in 22 rows.
   - Categorical codes are decoded correctly.
   - Duplicates are negligible: 2 exact duplicate rows and 3 duplicated feature vectors. 420 rows (1%) share a person and vehicle with another ID, mostly contracts re-issued after a lapse.
   - Values are plausible: driver age 18–98, every licence obtained at age 18 or older, vehicle age up to 67 (mostly motorbikes).

**What is fine.** The data is real (an anonymised sample from a Spanish insurer, published as a peer-reviewed data paper), licensed CC BY 4.0, and matches the published hash. Every column that is the outcome or measured after the period has been removed. At 42k rows and 18 features it is large enough to score, and the task is a genuine actuarial use.

**What I could not check.**
- The exact boundaries of the 9 test windows (task.md gives only the count).
- Tables 1–2 of the paper (the page I fetched did not include them).
- Whether Premium and Policies_in_force are snapshots taken at the start of the period.
- The cause of concern 4.
- How claims have developed since the 2019 extraction.

</details>

<details><summary>Precedent check</summary>

**Precedent check (precedent-checker, 2026-11-01): spanish_motor_insurance_2015_2018**

```text
Verdict: of 22 decisions, 17 follow their precedents, one has no precedent (PROV-13), one departs with a
  stated reason and a negligible effect (a full copy kept), and three depart in ways the curator should settle:
  1. No gap (SPLIT-10). The stated reason, SPLIT-14's floor, holds only for the nine-window layout. A 12-month gap
     meets the floor in the five newest monthly windows (Aug-Dec 2017, 56-76% of the rows train). What the departure
     keeps is SPLIT-15's window count, a later Should of the same part, so it is not a reasonable exception under the
     ranking. Its "third exception" also collides with three other no-gap proposals of this run.
  2. 5,069 first years whose contract ended on or before the day they start (14 claims) are kept as claim-free years.
     The 2022-2024 sibling drafted in this run drops its years with no time on risk (USE-7). The definition does not
     address this.
  3. `Payment` ("last payment method") is kept on a "dropping changes nothing" test. Lennart said on 2026-10-21
     (zillow_prize, melbourne_housing_market) that such a test is no reason to keep a lookup. Effect < 0.001 Gini.
Validity: USE-5 first-years-only follows rain_in_australia and ames_housing (rows whose label is another quantity are
  dropped, Lennart, 2026-10-26). The remnant is particular to this release: it does not show in the 2022-2024
  sibling (measured). LEAK-24, the LEAK-10 drops, Seniority, Policies_in_force and Value_vehicle are consistent.
  SPLIT-6 (a real temporal split) is consistent. PROV-13: no precedent decides on asking the authors.
Value: MET-3 log1p is consistent with four siblings and reasoned. MET-11 context Gini follows the family. Both family
  calls are open in australian_vehicle_insurance_2004_2005 (issues 4 and 5).
Quality: CLEAN-11, CLEAN-14 and the flat 882 amounts are consistent. Of the LEAK-18 pairs, one full copy is kept
  against LEAK-19 (one zero-cost row).
Drift: none. Amendment: SPLIT-10's floor reason is already past its third exception (avito_demand_prediction_1m's
  proposal of 2026-11-01), and this case does not meet that proposal's condition.
For the curator: prompts 1-3 below.
```

**How I checked.** For each choice I looked at four sources:
* the same rule ID in the run's decision register (`register.json`, 1,620 decisions; of its 14 flags only
  `amendment_due: SPLIT-10` touches this dataset);
* the Cases tables of `splits.md`, `leak_checks.md`, `use_case.md` and `provenance.md`;
* the curator's calls on the insurance family: [fremtpl2](../../../../curation/records/fremtpl2.md) (Andrej,
  2026-10-20), how_much_did_it_rain (Andrej, 2026-10-30), the "Policy calls of 2026-10-30" in
  [two_regime_zero_triage_summary.md](../../../../curation/inputs/two_regime_zero_triage_summary.md) (AI suggestions
  the curator asked for, not decisions);
* the sibling definitions of this run. Their drafts are by the AI and not yet decided, so they count as like cases to
  settle together, not as precedents with a curator's authority.

My own measurements (scripts and outputs in the run folder): the training shares under gaps
(`gap_floor.txt`), the years without cover (`lapse_at_start.txt`, `nocover_share.txt`), whether the premium is cut for
lapses (`lapse_premium.txt`), the full copies (`copies.txt`) and the remnant test on the 2022-2024 sibling
(`sibling_remnant.txt`).

**Per decision**

| Decision (rule) | Standing | Closest precedents | What sets it apart, or not |
|---|---|---|---|
| Only each policy's first year in the release (USE-5; builder issue 1) | consistent with the USE-5 cases. Departs from the record's suggested call ("per renewal year") with a measured reason | rain_in_australia (Lennart, 2026-10-26: rows whose label covers 48 hours or more dropped, "another quantity than the 24-hour call", found from the data); ames_housing (Lennart, 2026-10-26: allocation sales dropped, USE-5); diabetes_3 (USE-5 amended, Lennart, 2026-10-21: a label checked and found to be another quantity still fails); corporate_credit_rating (retired 2026-10-16: 17% of labels wrong, not locatable row by row) | Like rain_in_australia, the bad rows can be located by a rule (their position in the policy) and their defect is measured (0.7% claims after a claim-free year). So a filter is the milder remedy, unlike corporate_credit_rating's retirement. The defect belongs to this release: in the [2022-2024 sibling](../spanish_motor_insurance_coverage_level_2022_2024/dataset.py), 17.4% of 145,931 years after a claim-free year have a claim (25.2% after a year with claims). So keeping every policy-year there and first years here is not an inconsistency. The CC `Yes` (Andrej, 2026-10-30) was given on renewal pricing over all policy-years, and the test windows now hold only new contracts. The use case has changed since the CC (as with australian's reframed split), so the curator confirms it, as builder issue 1 asks. |
| Repair from the origin not tried (PROV-13, Must) | open; no precedent decides it | [aeolus](../../../../curation/records/aeolus.md) (Lennart, 2026-10-26: rebuilt from its public origin, BTS and Meteostat); policy question 8 (Andrej, 2026-10-30: no requests sent for four records whose data is only on request) | aeolus's origin was public. Question 8 concerned unreleased data, not the repair of a released table. The 2022-2024 draft also proposes asking the same research group for raw rows (its issue 3), so one answer serves both. |
| Years that start in 2018 dropped (LEAK-24) | consistent | LEAK-24 Cases: sf_permit_time, consumer_complaints (cut where follow-up is complete); the record's Assessment (2026-10-30) | The claim share per test month stays between 28% and 38% up to December 2017 (`window_concentration.txt`), so no later cut is called for. |
| Target `log1p_cost_claims_year`, metric on the amount (MET-3) | consistent, with a reason | frempl_french_motor_personal_line, spanish_motor_insurance_coverage_level_2022_2024, wisconsin_local_government_property_insurance_fund, allstate_claim_prediction_challenge_1m (same run, log1p); MET-3 (Lennart, 2026-10-21: ship on the modelling scale, score on the original); australian_vehicle_insurance_2004_2005 (raw, no reason), pricing_game_2017_french_mtpl (raw, with a reason) | The definition gives a measured reason (Gini 0.215 on log1p, 0.059 on the raw amount, 0.190 with a Tweedie loss). The family's split is australian's issue 5, and this dataset follows whatever is decided there. |
| Normalized Gini, context origin (MET-11) | consistent with the family; no curator confirmation yet | australian issue 4 and frempl issue 4 (open); allstate (source Gini) and liberty_mutual_fire_peril_loss_cost (weighted, source); porto_seguro (`roc_auc` for a binary Gini, 2026-10-21) | No exposure ships, so frempl's alternative (an exposure-weighted Gini on the cost per year) cannot apply here. Whichever form the family takes, this table scores the row Gini. |
| No exposure; complete years only (USE-5) | consistent | the suggestion of 2026-10-30 ("none; complete years kept"); pricing_game_2017_french_mtpl (whole years); the start-known fixes of coverage_level (exposure 1 for cancelled portfolio years, LEAK-7) and frempl (the length known at the start) | 2,054 first years end early through a lapse during the year. They stay as full priced years with no length shown, which is the start-known value the siblings chose. The years that never start are the next row. |
| First years without cover kept as claim-free years (USE-5, USE-7) | departs without a stated reason | coverage_level_2022_2024 (same run, same research group, AI draft): 49 policy-years with no time on risk dropped as "no year a policy is priced for" (USE-7) | 5,069 shipped rows end on or before the day they start: 4,971 on the renewal day and 98 before it. They hold 14 claims (0.3%), against 28% to 48% in the other lapse groups of more than 300 rows. All are older contracts and 17 fall in test months, so they sit almost entirely in training (15% of the rows before the oldest window). They are 17.4% of the zeros, so the accepted warning's "observed claim-free years" does not hold for them. Prompt 2. |
| `N_claims_year` dropped (a part of the target) | consistent | fremtpl2 CC (Andrej, 2026-10-20: `ClaimNb` dropped); australian `clm`, `numclaims`; frempl `ClaimInd`; coverage_level's claim counts | |
| `N_claims_history`, `R_Claims_history`, `Lapse`, `Date_lapse`, `Max_policies`, `Max_products` dropped (LEAK-10) | consistent | the record's screening and Assessment (2026-10-20, 2026-10-30); [distribution_transformers_at_cauca_department](../../../../curation/records/distribution_transformers_at_cauca_department.md) (Lennart, 2026-10-21: attributes recorded after the outcome dropped); coverage_level `policy_status` | Each has one value per policy, set at its end; as published they lift the Gini from 0.73 to 0.89. |
| `Seniority` dropped, not rebuilt (LEAK-10, LEAK-7) | consistent | LEAK-7 (the smallest fix first); cauca (drop where a gain may sit on the late values) | The rebuild, the record's alternative, was tried and leaks (65% against 32% claim share), so a drop is the next remedy. |
| `Policies_in_force` kept (LEAK-6, LEAK-10) | consistent | LEAK-6 (measure before acting); account_debt_south_africa (LEAK-10's first clause, Lennart, 2026-10-26: kept where the data shows it does not move with the outcome) | It changes within 24% of policies, and next year's count ranks this year's claims about as well as this year's count does (ROC AUC 0.532 against 0.538). |
| `Value_vehicle` kept, `Potential leak, kept on purpose` (LEAK-10 clauses) | consistent; the curator's case-by-case call | [onlinenewspopularity](../../../../curation/records/onlinenewspopularity.md) (LEAK-10 as amended 2026-10-26, Lennart: late values that cannot be located stay when the traceable part shows no gain); account_debt_south_africa | The traced part is the value beyond the vehicle's own characteristics (residual ROC AUC 0.508), and a revisit condition is given. LEAK-10 calls these clauses never a default, so builder issue 3 rightly asks the curator. |
| `Payment` kept (LEAK-10 second clause) | departs; the reason is not one the rule accepts | zillow_prize, melbourne_housing_market (Lennart, 2026-10-21: "a lookup is not kept merely because removing it changes no score"); cauca (dropped, 2026-10-21); onlinenewspopularity (kept on a traced test) | "Last payment method" is read at the end and no part of it can be traced. The keep rests on a removal test (< 0.001) and an unmeasured reading ("chosen with the contract"). The note gives no revisit condition (definitions.md, "Recording decisions"). Prompt 3. |
| `Premium` kept (USE-6, TP-4) | consistent | [california_house_prices_2020](../../../../curation/records/california_house_prices_2020.md) (Lennart, 2026-10-06: the listing price, a natural core); coverage_level (premiums kept, USE-6); wisconsin (Gini against the premium) | The model beats the premium alone in 6 of 9 windows. Not an earned premium: first years that lapse within the year carry a higher median premium than the rest (older contracts 310.66 against 295.54, new 319.14 against 279.77), so a lapse is not given away, unlike in the 2022-2024 sibling. |
| Impossible values set to missing (CLEAN-11) | consistent | churn_telco_south_asia (Tensions table); australian `veh_value` 0; frempl's licence-age threshold | |
| Ages from dates; codes labelled and categorical (CLEAN-12, CLEAN-14) | consistent | CLEAN-14 as amended (Lennart, 2026-10-21); coverage_level, australian | |
| 1,726 costs of exactly 882 kept (USE-5, CLEAN-11) | consistent | fremtpl2 CC (Andrej, 2026-10-20: the IRSA-IDA fixed amounts stay as point masses); policy question 2 (Andrej, 2026-10-30); coverage_level's CICOS amounts; australian's 200 floor | |
| Three pairs with identical features kept (LEAK-18) | two consistent; one departs, with a reason given | LEAK-19: audiology_diagnosis (copies on different ids dropped), frempl (45 exact copies dropped, same run); australian (378 repeats kept, few features) | Policies 22000 and 47844 match in all 30 source columns in each of three years (birth and licence dates, premiums to the cent, cost 0), and one of their rows ships. The stated reason (a fleet, or two policies of one holder) is possible. The effect is one zero-cost training row, so there is no prompt. |
| Temporal split on `period_start` (SPLIT-6, SPLIT-13, USE-10) | consistent | fremtpl2 CC (Andrej, 2026-10-20: temporal on an inferred year rather than IID); how_much_did_it_rain (Andrej, 2026-10-30: "Forced IID is to be avoided at all costs"); coverage_level (forced grouped, three calendar years) | Dated renewals over 26 months give real windows, and one row per policy removes the grouped structure. It is the one insurance table of the run with neither forced tag. |
| No gap (SPLIT-10, exception proposed; builder issue 2) | the stated reason does not hold as stated; not reasonable as an exception under the ranking | [lending_club](../../../../curation/records/lending_club.md), [alfa_battle_2_0_task_2](../../../../curation/records/alfa_battle_2_0_task_2.md) (Lennart, 2026-10-21; alfa gap 0, 2026-10-26); brazilian_ecommerce (2026-10-15), sf_permit_time, zillow_prize, house_sales (gaps applied); the Tensions row on unmatured labels; same run: pricing_game_2016_french_fleet, avito_demand_prediction_1m, wisconsin, loan_default_prediction_imperial_college | See the next section and prompt 1. |
| Nine monthly windows (SPLIT-12, SPLIT-15; builder issue 5) | consistent with SPLIT-12's case | SPLIT-12 case (Lennart, 2026-10-21: no window length for a family, each keeps its source's horizon or refit cadence); perth_house_prices (every third month, 2026-10-26); wisconsin and pricing_game_2016 (one-year horizon) | The monthly refit is the builder's reading; the source names no cadence. This interacts with prompt 1: under a 12-month gap only monthly windows from August 2017 fit, and of the quarterly windows only Q4 2017 meets the floor. |
| Warning `task_target_value_dominant` accepted | consistent (coverage_level proposes the same) | | Its text depends on the answer to prompt 2. |

**The gap, against its precedents**

* Training share by monthly window, newest first (`gap_floor.txt`):
  * no gap: 98% down to 82%;
  * 6-month gap: 85% down to 68%;
  * 12-month gap: 76.1%, 74.1%, 67.5%, 61.3%, 55.7% for December to August 2017, then 47.8%, 40.9%, 34.6%, 28.3% for
    July to April.

  So the full delay meets SPLIT-14 in five windows. The definition cites only the oldest of the nine (28%).
* In each confirmed exception of this reason, no layout of three windows met the floor with a gap of the delay:
  * lending_club: "a 36-month gap leaves 5-9% ..., a 12-month gap 33-46%";
  * alfa_battle_2_0_task_2: 13-27% at 12 months;
  * avito_demand_prediction_1m (proposed): "at every window width".

  That fact is what sets those cases apart, and it is missing here.
* Lennart's other SPLIT-10 calls put a gap wherever one fit:
  * brazilian_ecommerce, 1 month;
  * sf_permit_time, 6 months;
  * zillow_prize, 1 month;
  * house_sales, 1 week.

  He went without a gap only for the floor (lending, alfa) or for a delay shorter than the time resolution
  (ames_housing, perth_house_prices). melbourne_housing_market (no gap, no selection measured) is a recording delay of
  a label fixed at the sale. Here the label itself, a year's claims, does not exist yet at the window's start: the case
  SPLIT-9 and the Tensions row on unmatured labels describe, which allow a departure only "for SPLIT-14's 50% floor".
* What the departure keeps: nine windows instead of five and 7,573 test rows instead of 4,373. SPLIT-15 asks for the
  nine, but it is a Should placed after SPLIT-10 in the same part, and at equal strength the earlier rule wins. The cost
  of the gap on those five windows is a mean Gini of 0.154 with it against 0.170 without (untuned LightGBM, single fits,
  the builder's `shipped_experiments.txt`). The windows vary far more than that.
* The count. The builder calls this "the third exception for this reason". avito_demand_prediction_1m's REVIEW.md,
  written the same day, calls itself the third and proposes an amendment text (cases alfa, lending, avito).
  loan_default_prediction_imperial_college (no gap "as for lending_club", delay unsized) and
  wisconsin_local_government_property_insurance_fund (no gap "as lending_club, serving SPLIT-14") also depart. So the
  amendment is due however the four are ordered, and is best decided once, in avito's issue 2. As written, its
  condition ("a gap of the label's delay would leave a window's train side under SPLIT-14's floor at any window width")
  does not cover this case.
* Three insurance tables of this run share one mechanism, a policy year's claims known only when it ends, and treat it
  three ways:
  * pricing_game_2016_french_fleet trains on closed years only, invoking SPLIT-9, with three windows;
  * wisconsin goes without a gap;
  * this table goes without a gap and keeps nine windows.

**Drift and amendments**

* Andrej: fremtpl2 (temporal, 2026-10-20), how_much_did_it_rain (no forced IID, 2026-10-30) and the `Yes` here
  (2026-10-30) point the same way. The temporal split matches them, so I see no drift.
* Lennart's SPLIT-10 calls form a steady pattern (a gap where it fits). This draft would be the first no-gap split
  where a gap of the full delay fits.
* Third exception: SPLIT-10's floor reason is past its third exception; see the count above.
* Cases rows due once the curator answers:
  * USE-5: later policy-years that hold the first year's claims, a defect particular to the release, located by row
    position;
  * LEAK-10: a late valuation of a stable attribute kept on a traced residual test (Value_vehicle);
  * SPLIT-10: the case or the amendment.

**Reflection prompts**

1. **Consistency check (AI, 2026-11-01):** the draft ships no gap as an exception to SPLIT-10 that "serves SPLIT-14",
   as lending_club and alfa_battle_2_0_task_2 do (Lennart, 2026-10-21). In those, no three-window layout met the 50%
   floor with a gap of the delay. Here a 12-month gap meets it in the five newest monthly windows (Aug-Dec 2017, 56-76%
   of the rows train). Elsewhere you put a gap wherever it fit (brazilian_ecommerce, sf_permit_time, zillow_prize).
   What sets this case apart?
   (a) No shortcut from the unmatured labels shows (6-month gap 0.223 against 0.215 without). The gap would cut nine
   windows to five, two of which no model can rank (November and December 2017), so an exception would serve P6
   (folds that can be scored). P6 ranks below P4, so this holds only as (d).
   (b) Treat it like brazilian_ecommerce and the sibling pricing_game_2016_french_fleet: a 12-month gap with the five
   newest monthly windows (4,373 test rows; Gini 0.154 against 0.170 without the gap, single fits).
   (c) Reopen pricing_game_2016_french_fleet's closed-year training to match this split.
   (d) Amend SPLIT-10: no gap when no shortcut is measured and a gap would cost windows below SPLIT-15's count. Decide
   it with avito_demand_prediction_1m's amendment (its issue 2), whose wording does not cover this case.
2. **Consistency check (AI, 2026-11-01):** the draft keeps as claim-free years 5,069 first years whose contract ended
   on or before the day they start (14 claims, 0.3%). That is 17.4% of the zeros, almost all in training. The
   2022-2024 sibling of the same research group (same run, AI draft) drops its 49 policy-years with no time on risk as
   "no year a policy is priced for" (USE-7). What sets this case apart?
   (a) These rows carry a renewal premium (median 308.88, none zero), so the insurer priced the year and the customer
   declined it, unlike the sibling's zero-premium rows. They stay, with a note that corrects "observed claim-free
   years".
   (b) Treat it like the sibling and drop them (USE-5, USE-7). The zero share falls from 68.8% to 64.6%, and the older
   contracts' first years then claim at 33.2% instead of 26.3%.
   (c) Reopen the sibling to keep its years with no time on risk.
   (d) Add a rule line for policy-years without cover in insurance tables.
3. **Consistency check (AI, 2026-11-01):** the draft keeps `Payment` ("Last payment method of the reference policy",
   one value per policy) because dropping it changes the Gini by less than 0.001. That differs from zillow_prize and
   melbourne_housing_market (Lennart, 2026-10-21: a lookup is not kept merely because removing it changes no score)
   and from distribution_transformers_at_cauca_department (dropped). What sets `Payment` apart?
   (a) The payment frequency is fixed by the contract and never differs between a policy's rows, so the "last" value
   is the only one recorded. It stays, with a revisit condition (a release with the method at each renewal).
   (b) Treat it like cauca and drop it (costs < 0.001 Gini).
   (c) Reopen zillow_prize and melbourne_housing_market.
   (d) Amend LEAK-10 to keep a late attribute that carries no measurable gain.

**Builder's draft issues against precedent**

1. USE-5 and PROV-13: the first-years filter follows rain_in_australia and ames_housing, and the remedy ladder puts it
   ahead of a retirement like corporate_credit_rating's. Whether to ask the authors (PROV-13) has no precedent:
   decide it with the 2022-2024 sibling's issue 3.
2. SPLIT-10: the count is off. avito_demand_prediction_1m claims third too, and loan_default and wisconsin also depart.
   The floor reason does not hold as stated (prompt 1).
3. LEAK-10: `Value_vehicle` is consistent (an onlinenewspopularity-style traced test). `Payment` departs (prompt 3).
4. PROV-6 and PROV-7: consistent with the Tensions row (a shared source with distinct tasks is not a duplicate) and
   with Andrej's question 5 answer (each French portfolio judged on its own record). One measured fact adds to it: the
   two releases record later years differently (0.7% against 17.4% claims after a claim-free year).
5. SPLIT-15 and quarterly windows: consistent with SPLIT-12's case, but tied to prompt 1. Quarterly windows work only
   without a gap; with a 12-month gap only monthly windows from August 2017 fit.

</details>

<details><summary>Advocate</summary>

**Advocate, opening brief (2026-11-01): spanish_motor_insurance_2015_2018**

```text
Verdict: ship after changes. Every problem the panel found is fixed by a row filter, a re-split or a dropped column;
  none calls for exclusion (remedy ladder).
Validity: SEL holds; USE-1 and USE-6 hold (new-business pricing with the insurer's own premium); USE-5 triggered
  twice, fixed by two filters that read no label (first year of each customer, years with cover); LEAK-10 drops all
  agreed, Payment conceded (drop); SPLIT-10 triggered, fixed by a 12-month gap with 5 monthly windows (SPLIT-14 holds,
  measured after the filters).
Value: TP-2, TP-4 hold: with the fixes, untuned LightGBM 0.241 against the premium alone 0.167 (5 windows, gap).
Quality: CLEAN-1 (contract_years arithmetic) and text slips, cheap and safe.
Weighed: source +, size +, signal small but real, window noise -.
```

New measurements (mine, in the run folder: `gap_after_filters.py`, `fixed_design.py`): untuned LightGBM on
log1p with the builder's parameters, 2 seeds, normalized Gini on the amount. "Both filters" means the column auditor's
no-cover filter and the claim auditor's customer filter (34,470 rows).

| design | windows | mean Gini | premium alone | ahead of premium | claim AUC |
|---|---|---|---|---|---|
| as defined | 9, no gap | 0.229 | 0.187 | 5 of 9 | 0.632 |
| both filters, `Payment` dropped | 9, no gap | 0.275 | 0.190 | 8 of 9 | 0.672 |
| both filters, `Payment` dropped | 5 (Aug-Dec 2017), 12-month gap | 0.241 | 0.167 | 3 of 5 | 0.657 |
| as defined | 5 (Aug-Dec 2017), 12-month gap | 0.167 | 0.160 | 3 of 5 | 0.627 |

**1. The core is a valid pricing task, and no finding reaches P1 or P2 (SEL, USE-1, USE-6 Must, LEAK-10 Must).**
- The claim: these are real policies of a real Spanish insurer, released with a peer-reviewed data paper under CC BY
  4.0. The task is the article's "pricing mechanisms for new business" (Sec. 1). The domain practitioner and the column
  auditor read Sec. 1 on the publisher's page; the claim auditor could not get past the bot check (EV-7).
- The evidence: all six agents agree that every column measured after the year has been dropped. As published, those
  columns lift the Gini from 0.73 to 0.89.
- `Premium` is the annual written premium, known at the quote. Three agents measured this independently. Lapsed
  half-yearly payers keep a full-year premium (ratio 1.015 against 1.005). The Spearman correlation with the share of
  the year in force is 0.05. First years that lapse carry a higher median premium than the rest. That makes it a
  legitimate input under USE-6.
- Why it outranks the objections: every validity finding below is located row by row or column by column, so it is
  fixed in the definition. Exclusion is for a Must that cannot be fixed (How to decide, 5).
- One honest caveat: the curator's `Yes` (Andrej, 2026-10-30) was given on renewal pricing. The curator confirms the
  new-business framing (builder issue 1).

**2. First rows only, extended to the customer, removes the label defect (USE-5 Must; precedents rain_in_australia,
ames_housing).**
- The policy-level remnant is reproduced by four agents and found blind by a fifth. After a claim-free year, 0.7-0.9%
  of the next years have a claim, against 26-38% for first rows.
- The 2022-2024 sibling shows 17.4%, so the defect belongs to this release.
- I concede the customer-level finding (claim auditor item 1). A known customer's later policy claims at 4-8% when the
  first policy was claim-free and at 47-53% when it had a claim. In the test windows, 1,097 such rows claim at 0.200
  against 0.363, and the model ranks them the wrong way.
- That is USE-5's last sentence for those rows: "a label checked and found to be another quantity still fails". The
  same rule that already drops later years applies, as in rain_in_australia (rows located by a rule and dropped,
  Lennart, 2026-10-26).
- The fix: keep each customer's first year in the release (key: birth date and licence date). The filter reads keys
  and dates, never the label.
- With it, the task gets better: 0.275 against the premium's 0.190, ahead in 8 of 9 windows (table).
- Why a filter and not retirement: corporate_credit_rating was retired because its bad labels could not be located.
  Here they can, and a fixed definition comes before exclusion on the ladder.
- The mechanism stays undocumented. USE-5 lets such a label ship with `fit="approximate"` and the gap named
  (diabetes_3). The target cost per claimant is stable across cohorts (800-1,100, claim auditor t17).
- PROV-13: the filters drop the damaged rows rather than keep them. Asking the authors for the pre-cleaned raw data is
  one request that serves both Spanish records (the 2022-2024 sibling's issue 3). It would restore renewal rows, and
  it does not block these rows.

**3. The years without cover go (USE-7 Must, as the 2022-2024 sibling; conceded).**
- 5,069 rows end on or before the day they start. They hold 14 claims (0.3%). All are on the train side but 17.
- Five agents and the sibling's precedent ("no year a policy is priced for") agree. I do not take the precedent
  checker's option (a), that a renewal premium was quoted for these years. A pure premium is a cost per year at risk,
  and these years carry no risk.
- The fix: keep `Date_lapse.isna() | (Date_lapse > Date_last_renewal)`. This is known at the year's start and reads no
  label. The score effect is +0.006 to +0.013.
- Then update the counts:
  - the zero share becomes 63.5% after both filters;
  - the older contracts' claim share becomes 32-35% per month;
  - the warning's "observed claim-free years" becomes true again.
- This also removes the shortcut the blind reviewer saw: a rule for "old contract, structural zero" learned in
  2015-16 that does not hold in the 2017 test rows.

**4. The split regime is right; the gap is conceded, and a re-split keeps the dataset (SPLIT-9 Must, SPLIT-10
Should, SPLIT-14 Must).**
- The regime: the split auditor passes the temporal regime, the test population (new contracts, the use case's
  actor) and the expanding train side (SPLIT-1, SPLIT-6, SPLIT-11, USE-10).
- On the blind reviewer's concern 2: the move to new business in 2017 is the use case, not an artifact. Renewal rows
  cannot serve as tests, because later years hold remnants (point 2).
- The gap: the no-gap exception's fact (SPLIT-14's floor) does not hold. SPLIT-10 comes before SPLIT-15, so the
  exception is not reasonable.
- My new fact: after both row filters, a 12-month gap still keeps 5 monthly windows, August to December 2017, with
  55.1-74.9% of the rows for training. So the floor case of lending_club and alfa_battle_2_0_task_2 does not arise
  after the fixes either.
- The fix: re-split as `TemporalSplits(window=1, unit="months", gap=12, min_train_fraction=0.5)`. This follows
  brazilian_ecommerce, sf_permit_time and pricing_game_2016_french_fleet. It also meets SPLIT-9 for the customer link,
  with no further filter.
- The design scores 0.241 against the premium's 0.167 on 3,690 test rows, with 243-335 claims per window.
- Without the row filters, the gap design sits at the premium's level (0.167 against 0.160). So the filters and the
  gap belong together.

**5. The kept features hold, except `Payment` (LEAK-10 Must, its 2026-10-26 clauses).**
- `Value_vehicle` stays. The residual beyond the vehicle's own characteristics has ROC AUC 0.508, and every agent
  agrees. This is the lookup clause's "unless the data shows they did not change".
- `Policies_in_force` stays, with a `Potential leak, kept on purpose:` note. It is a calendar-year count that includes
  policies written later in the year (68-80% of the traced pairs). The traced late part shows no gain: the claim share
  is 31.2% against 31.2%, and removing the late part raises the Gini from 0.229 to 0.243. That is onlinenewspopularity's
  test under the second clause.
- `Payment`: conceded. A "removing it changes no score" test alone is no reason to keep it (zillow_prize,
  melbourne_housing_market, 2026-10-21). The column auditor found an untraceable pattern: 40% of renewed first years
  with a claim are half-yearly, against 26% without one. So it goes, like cauca's attributes. It costs less than 0.001
  Gini, and my fixed-design runs already drop it.

**6. Worth benchmarking: a small real signal, scorable in every fold (TP-2 Should, TP-4 Must, MET-2, MET-11).**
- `Trivial` needs proof (TP-4), and the evidence runs the other way. With the fixes, the model beats the premium
  alone in the mean (0.241 against 0.167) and ranks a claim at AUC 0.63-0.68.
- Every fold has 160-335 claims, and a constant scores 0 (MET-2). The row Gini is the family's context metric
  (MET-11).
- Window noise (bootstrap SE 0.05-0.11) is a MET-10 factor, a Weigh. It cannot override TP-2. "The split follows the
  application; a small signal under it is no reason to retire" (Tensions row P4 over P6, forest_fires).
- November and December 2017 stay, whatever their scores (SPLIT-21 Must). With the gap, quarterly windows would leave
  only 2017-Q4, so monthly windows it is.
- The metric reason should name the Kaggle form of the Gini, with Frees et al. as the background (domain
  practitioner). That is a text fix.

**7. The cleaning issues are cheap and safe, and none holds the dataset back (CLEAN-1 Should, CLEAN-10; How to
decide, 3).**
- `contract_years`: use calendar arithmetic. It is a year low for 5,608 rows, confounded with `period_start`; the
  column auditor's `_whole_years` fixes it and the two minor age slips.
- `Anomaly:` notes for the farm-vehicle fill blocks, and for `Power` 0 = missing `Type_fuel` (one block without
  vehicle data).
- Text slips to correct:
  - the 48 older-contract first rows after November 2016;
  - the `Length` and `Type_fuel` scope;
  - 24% of the policies with several rows;
  - the stale README "ties in row order" (re-run `dataset check`).
- `fit_reason`: move `Value_vehicle` from the gaps to "kept" (USE-8), and add the customer-level attribution gap.
- `use_case`: name the premium's role, refining the quoted price (USE-6, domain practitioner).
- Under P7, a very real task carries imperfections that are written down. These ones are simply fixed.

</details>

<details><summary>Critic</summary>

**Critic, opening brief (2026-11-01): spanish_motor_insurance_2015_2018**

```text
Verdict: ship after changes. No exclusion: every Must below can be fixed in the definition.
Validity: USE-5 triggered twice (rows without cover; claims shared across a customer's policies), both fixed by
  filters that do not read the label. USE-8: the use case and fit are rewritten, and the curator re-confirms the
  changed task. LEAK-10: `Payment` dropped, `Policies_in_force` noted or removed with point 2. SPLIT-9/SPLIT-10:
  a 12-month gap with 5 monthly windows.
Value: TP-2 holds (a small real signal). MET-10 factor: 5 windows of 400-1,000 rows score noisily. This is the
  cost of the gap, and P4 outranks P6.
Quality: CLEAN-1: `contract_years` is a year too low for 5,608 rows. Some numbers in the notes and the README are
  refuted.
```

My own checks are in the run folder (check.py to check4.py, with a .txt output for each). The customer key
is the evidence agents' key: `Date_birth` + `Date_driving_licence`.

**1. 5,069 rows are years that never had cover, and they ship as claim-free years (P3, USE-5 Must; LEAK-25 Must, the recovered case)**

- **Problem.** These rows have `Date_lapse` on the year's start (4,971 rows) or before it (98).
  - They hold 14 claims (0.28%), against 35.4% for the other first rows.
  - Every one is an older contract's first row in the release and also that policy's last row: a renewal that was not taken up.
  - They are 17.4% of the zeros.
  - Five agents found this independently (claim-auditor, column-auditor, domain-practitioner, blind-reviewer, precedent-checker). I re-counted it (check.txt).
- **Effect.**
  - For these rows the target "the year's claim cost" has no year behind it: the zero means no exposure, not no claim.
  - They sit in training (17 rows fall in test months). The features pick them out at ROC AUC 0.64-0.72, mostly through `contract_years` (column-auditor, blind-reviewer). So a model learns a structural-zero rule that the 2017 test rows do not have.
  - The score effect is small: +0.006 to +0.013 mean Gini when they are dropped.
  - Several of the definition's own statements rest on these rows:
    - older contracts claim in 25-27% of each month (32-35% for the rows with cover);
    - 68.8% of the targets are zero (64.6% without these rows);
    - the reason given for accepting the warning, "observed claim-free years".
- **Rule.**
  - USE-5 (Must): a label checked and found to be another quantity fails.
  - LEAK-25 (Must): "no event" mixed with "not recorded" counts as recovered when the rows are located by a rule that does not read the label, and dropped.
  - Like cases are treated alike: the 2022-2024 sibling drops its 49 years with no time at risk as "no year a policy is priced for" (USE-7).
  - The other reading fails. That reading says the insurer priced the renewal and the customer declined it, a competing event under LEAK-22. But no day at risk means no claim cost to predict, and a pure premium is a cost per year at risk (column-auditor).
- **Remedy (fix the definition).**
  - Before step 3, keep only rows where `Date_lapse.isna() | (Date_lapse > Date_last_renewal)`. That leaves 37,090 rows.
  - Then re-measure the shares in notes 3 and 5 and rewrite the warning's reason.

**2. A row's claims move with the claims of the customer's other policies in force (P3, USE-5 Must)**

- **Problem.** For two policies of one customer whose years overlap:
  - P(claim on B | claim on A) is 0.90 at full overlap, against 0.04 when A has no claim (column-auditor). As a control, the same customer's years more than 180 days apart give 0.21 against 0.12.
  - The claim counts are equal in 69% of full-overlap pairs, but the costs almost never are.
  - Shared vehicles do not explain it: 1,519 of the 1,532 pairs insure different vehicles.
- **My checks.**
  - The link runs both ways. A customer's first policy claims in 83.9% of cases when its later concurrent policy claims, against 9.4% when that policy has no claim (baseline 36.9%, 1,227 rows).
  - The link goes with `Policies_in_force`:
    - rows with a count of 2 or more: 0.795 against 0.057 (2,493 rows);
    - rows with a count of 1 that still have a concurrent sampled policy: 0.48 against 0.31 (213 rows), close to the mild customer effect.
  - Among customers with no other ID in the release, claims per row grow almost in proportion to the count: 0.65, 1.15, 1.61, 2.01 and 2.46 for counts 1 to 5 (check2.txt, check4.txt).
- **Effect.**
  - For rows with `Policies_in_force` >= 2 (about 30% of the rows, 45% of the test rows), the label is at least partly the customer's claims across policies, not the policy's own year.
  - `Policies_in_force` is the strongest feature (R^2 0.042 with it, 0.019 without), so it partly scales a count. The note reads that as risk ("customers with more policies ... have more claims per policy").
  - A tariff built on this would surcharge customers with several policies because of how claims are booked.
- **Rule.**
  - USE-5 (Must): "A label checked and found to be another quantity than the one the actor acts on still fails." The clause that allows `approximate` covers a label that cannot be checked. This one has been checked.
  - EV-1: the release cannot tell customer-level counting from a strong customer effect. The authors' pre-cleaned raw data could (PROV-13, a repair).
- **Remedy (fix the definition; the mildest that works).**
  - Keep only rows with `Policies_in_force == 1`, where the count can only be the policy's own. That leaves 25,665 rows after point 1, with 360-569 test rows and 87-195 claims per month.
  - The column then becomes constant and goes, so its LEAK-10 question goes too.
  - The count includes policies added later in the year (point 4). But rows with such a later policy claim at the same share as the rest (31.2% against 31.2%, column-auditor), so the filter does not select on the outcome.
  - The claim-auditor's filter (keep each customer's first policy) does not work: the kept first rows move with their siblings just as strongly (0.839 against 0.094).
  - A note alone would leave the artefact in both the label and the strongest feature.
  - If the curator wants to ask the authors first, the dataset waits for the answer. Asking ranks above a filter on the remedy ladder (PROV-13). But on 2026-10-30 Andrej sent no requests for the records that are only on request (policy question 8), so the filter is the default.

**3. The task as built is not the one the curator said Yes to, and its fit does not name its gaps (P3, USE-8 Must; who decides)**

- **Problem.**
  - The CC `Yes` (Andrej, 2026-10-30) was given on "Target `Cost_claims_year` per renewal year", that is, renewal pricing over all policy-years. The build ships new-business pricing on first years only, and every test row is a new contract.
  - Three inputs a pricing actuary always has are missing: the cover bought, the claims history from SINCO/SIHSA, and the territory. Premium alone ranks at 0.187 and a model at 0.215 (domain-practitioner). So the task is to find where the quoted premium is wrong (tariff refinement), not to set the premium from the rating factors.
  - `fit_reason` counts `Value_vehicle` as a gap, although the definition keeps it as a potential leak.
  - `fit_reason` also omits the missing cover, the 2,055 first years cut short with no exposure, and the gap of point 2 if it stays.
- **Effect.**
  - The curator has not decided on the task as it was built.
  - `use_case` misstates what a model is asked to do.
- **Rule.**
  - USE-8 (Must): name the gaps. A leak kept on purpose is named as kept, not as a gap.
  - Principles, "Who decides": the CC is the curator's decision, and the AI does not override it. Builder issue 1 asks the same question.
- **Remedy (fix the text; the curator confirms).**
  - Rewrite `use_case` as refining the quoted premium for new business. USE-6 keeps the premium. Say "customers with no other policy" if point 2 is taken.
  - Make `fit_reason` name the missing cover, history and territory, the undocumented carry-over between years, and the cut-short years.
  - Move `Value_vehicle` to "kept".
  - Raise an issue for the curator to confirm the new-business framing.

**4. Two values read late (P4, LEAK-10 Must, second clause)**

- **`Payment` ("Last payment method of the reference policy", one value per policy).**
  - Problem: it is kept because dropping it changes the Gini by less than 0.001. LEAK-10 as amended says "a 'removing it changes no score' test alone is still no reason to keep", and late values that cannot be located go "when they may carry a gain".
  - Evidence of a possible gain: among policies that renewed, 26% of claim-free first years are half-yearly payers, against 40% of first years with a claim (column-auditor). This could be a switch after a claim or survival selection, and the data cannot tell which.
  - Precedents: zillow_prize and melbourne_housing_market (the rule's 2026-10-21 cases), and distribution_transformers_at_cauca_department (dropped).
  - Remedy: drop the column. It costs less than 0.001 Gini.
- **`Policies_in_force`.**
  - Problem: it counts the policies held at any time in the calendar year in which the row starts. 68% of 2,723 pairs already count a policy that was written later in the year (claim-auditor). The definition says it is "measured per year".
  - The late part carries no gain: subtracting the later additions that are in the sample raises the Gini from 0.229 to 0.243.
  - Remedy: it goes with point 2. If point 2 is not taken, subtract the located in-sample additions (2,865 rows; LEAK-10 fixes late cells that can be located). Then turn the bullet into a `Potential leak, kept on purpose:` note, and say "in the calendar year" in `known`.

**5. No gap, on a reason that does not hold here (P4, SPLIT-9 Must by its Tensions row; SPLIT-10 Should)**

- **Problem.**
  - In each window, 22-65% of the training rows are years that had not ended at the window's start (split-auditor).
  - The exception says it "serves SPLIT-14", as in lending_club and alfa_battle_2_0_task_2. But a 12-month gap meets the 50% floor in the five newest monthly windows: August to December 2017 train on 55.7-76.1% of the rows (split-auditor, precedent-checker).
  - I re-ran the shares after the proposed filters: 52.9-72.9% after point 1, and 57.8-78.5% after points 1 and 2 (check3.txt).
  - So the departure keeps only SPLIT-15's window count. That is a later Should of the same part, not a higher principle, so it is not a reasonable exception (principles: Strengths, and Consistency case 1).
  - Precedents point the other way:
    - Lennart put a gap wherever one fit (brazilian_ecommerce, sf_permit_time, zillow_prize, house_sales);
    - the sibling pricing_game_2016_french_fleet trains on closed years only.
- **A label link that can be measured.**
  - 579 test rows have a policy of the same customer on the training side whose year was still running.
  - That policy's label tells the test row's outcome: 58.7% of test rows claim after an overlapping year with a claim, 7.1% after a claim-free one (split-auditor). Per window, this ranks the test rows' claims at ROC AUC 0.65-0.82 (claim-auditor).
  - The Tensions row says "a shortcut that can be measured is always removed, whatever it costs the floor". alfa_battle_2_0_task_2 was filtered at a score effect of 0.002-0.009. That no model reaches the link through the features (split-auditor) does not lift the rule.
- **Effect.** The benchmark trains on outcomes that an insurer refitting at the window's start would not yet have. SPLIT-10 counts the gap as part of the task.
- **Remedy (re-split).**
  - Use `TemporalSplits(window=1, unit="months", gap=12, min_train_fraction=0.5)`: 5 windows, August to December 2017, trained on the years that had ended by each window's start. This removes every unmatured training row, and the label link with it.
  - The cost, stated plainly:
    - 4,373 test rows, or 2,385 after point 2;
    - two of the five windows (November and December) rank near 0 for every model;
    - a mean Gini of 0.181 against 0.185 without the gap on the same windows.
  - P4 outranks P6 (Tensions row: the right split against the score).
  - If the curator keeps the 9 windows: record an exception with its true fact (SPLIT-15), and drop the training rows of customers who have a test-window policy (the alfa filter, 106-182 rows per window).

**6. `contract_years` is a year too low for 5,608 rows (P7, CLEAN-1 Should)**

- **Problem.** The formula `days // 365.25` loses a year on contract anniversaries.
  - All 2,185 one-year-old contracts renewed in 2015-Q4 read 0, the value of a new contract, and so do 62% of those renewed in 2016-Q1.
  - None from 2016-Q2 on does, so the error is confounded with `period_start`.
  - The same formula puts `driver_age` a year low in 30 rows and `years_licensed` in 42 (column-auditor).
- **Effect.** The score barely moves, because the test rows are new contracts with the correct value 0. But the note "ages at the year's start, in whole years" is false.
- **Remedy (cheap and safe).** Use calendar arithmetic, the column-auditor's `_whole_years`. This is a quality point and no reason to exclude.

**7. Numbers and texts that do not hold (P7; MET-11 Must; house rules)**

- The README metric block says "(ties in row order)", but the scorer averages ties. Re-run `dataset check`.
- `row` and `splits_comment` say the older contracts' first years start before December 2016. 48 start later, 40 of them in test windows.
- `metric.reason` cites Frees, Meyers and Cummings (2011), whose Gini orders policies by the score relative to the premium. The declared metric is the Kaggle form, and MET-11 asks to name the original when the declared metric is not exactly it.
- Notes to correct:
  - `Power` 0 and missing `Type_fuel` are the same 652 rows: a block without vehicle data (CLEAN-10).
  - `Length` is also missing for 423 cars and vans.
  - "24% of the policies" is 24% of the policies with several rows.
  - `ID` is the key of the policyholder and product.
  - The 150 farm vehicles with identical engine size, weight and value need an `Anomaly:` note.
- After points 1-5, re-measure every count in the notes and the task summary.

**Dropped from my case**

- The blind reviewer's "first cycle only" redesign. The use case is new business, so the test population is right (split-auditor, domain-practitioner); P3 decides.
- Quarterly windows. With a 12-month gap only 2017-Q4 meets the floor, and SPLIT-21 forbids choosing windows from scores.
- PROV-6/PROV-7 (same insurer as the 2022-2024 sibling). Untested, and the periods and schemas differ.

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate, rebuttal (2026-11-01): spanish_motor_insurance_2015_2018**

```text
Verdict: ship after changes (unchanged). I concede points 1, 3, 4, 5, 6 and 7. On point 2 I concede that my customer
  filter fails, and I dispute the critic's filter. New checks show the label follows the row's own vehicle and the
  costs are not shared, so USE-5's undocumented-label clause applies (a note, fit approximate), not its
  "another quantity" clause.
Correction to my opening: its 0.241 against 0.167 rested on the withdrawn filter. With the agreed fixes the model only
  ties the premium (0.172 against 0.162).
Left for the mediator: point 2's remedy, a note or Policies_in_force == 1.
```

My checks are in the run folder: `own_risk.py`, `own_risk2.py`, `pair_types.py`, `filter_options.py` and
`premium_vs_methods.py`, each with a `.txt` output. They use first rows with cover only, so the no-cover filter is
already applied. The customer key is the panel's (birth date plus licence date). "Concurrent" means the two years
overlap by more than 180 days.

**Critic 1, years without cover: conceded.** This is the same fix as my point 3: keep
`Date_lapse.isna() | (Date_lapse > Date_last_renewal)`. LEAK-25's recovered case is the closer rule (no event mixed
with no time at risk, located by a rule that does not read the label), and USE-7 and the sibling's precedent point
the same way.

**Critic 2, claims that move with the customer's other policies: narrowed. My filter is withdrawn, and the critic's
filter is disputed.**
- **Conceded:** keeping each customer's first policy does not remove the co-movement. The critic's 0.839 against 0.094
  for the kept first rows stands. I withdraw that filter. The 12-month gap already removes its other reason, the
  label link across the split. With the filter go my opening numbers for it (0.275 and 0.241).
- **Disputed:** the claim that "the label is at least partly the customer's claims across policies". If a row carried
  the customer's claims, a motorbike or farm policy of a multi-policy customer would inherit its siblings' claims. It
  does not:
  - **Concurrent pairs on different vehicle types** (364 pairs). When the sibling has a claim, cars claim in 0.761 of
    cases and vans in 0.798, but motorbikes in 0 of 9 and farm vehicles in 0 of 1. In 22 motorbike-and-car pairs both
    never claim together, and when only one claims it is the car 9 times out of 11.
  - **`Policies_in_force` of 2 or more.** Farm vehicles claim in 0 of 151 rows. The type gradient is intact:
    motorbike against car is 0.171 against 0.440 (ratio 0.39), against 0.140 and 0.339 (ratio 0.41) with one policy.
  - **Costs are not shared.** In the 278 concurrent pairs where both claim, the two costs have a Spearman correlation
    of 0.076 (random pairs of claimants: -0.002, sd 0.056), and 1.4% are equal. That is neither a copy nor a split of
    one amount.
- What the data shows, then: claims occur together on a customer's concurrent car and van policies, and each policy
  carries its own booked cost. A tariff that charges multi-policy customers more would recover costs the insurer
  booked on those policies, not the same cost counted twice. Why the claims occur together is undocumented. The
  critic agrees the release cannot tell (EV-1). The claim-type sample cannot settle it either: it holds both members
  of only 1 of the 278 pairs.
- **Rule.** USE-5's last sentence needs a label "checked and found to be another quantity". What has been checked is
  an undocumented way of booking claims, and the target still follows the row's vehicle. That falls under USE-5's
  middle clause: ship with `fit="approximate"` and a note naming the gap (diabetes_3). A note settles an
  undocumented-label gap, so the remedy ladder does not require a filter. The PROV-13 request to the authors serves
  this and the 2022-2024 sibling at once.
- **The cost of the critic's filter** (my runs with the 12-month gap, `Payment` dropped, 3 seeds):

  | option | rows | test rows (5 windows) | best untuned learner, mean Gini | premium alone | premium at or above the best learner |
  |---|---|---|---|---|---|
  | A: note only | 37,090 | 4,362 | 0.172 | 0.162 | 3 of 5 |
  | C: `Policies_in_force == 1` | 25,665 | 2,385 | 0.124 | 0.234 | 4 of 5 |

  Under C the premium alone beats every learner in 4 of 5 windows (log1p, Tweedie and claim classifier). That would
  trade a documented label gap for an open TP-4 question. This is a P6 consideration: it cannot rescue a USE-5
  failure. It counts only if the curator reads the facts above as I do.
- **Conceded within point 2:** the `Policies_in_force` bullet reads the count as risk alone. It should say that the
  count also tracks claims that occur together on a customer's car and van policies. `fit_reason` names this gap.

**Critic 3, the task differs from the curator's `Yes`, and the fit does not name its gaps: conceded.**
- Rewrite `use_case` as refining the quoted premium for new business (USE-6).
- `fit_reason` names:
  - the missing cover, claims history and territory;
  - the undocumented attribution across years and across a customer's policies;
  - the 2,055 first years cut short.
- `Value_vehicle` moves to "kept" (USE-8).
- An issue asks the curator to confirm the new-business framing.

**Critic 4, values read late: conceded.**
- `Payment` goes (LEAK-10, zillow_prize).
- `Policies_in_force`: subtracting the in-sample additions that can be located (2,865 rows) is LEAK-10's "late cells
  that can be located" clause, and the smallest fix (LEAK-7). I accept it. The part outside the sample stays under a
  `Potential leak, kept on purpose:` note (onlinenewspopularity), and `known` says "in the calendar year".

**Critic 5, the gap: conceded, as in my point 4.** Under option A the 12-month gap keeps 5 windows with 52.9-72.9% of
the rows for training (SPLIT-14 holds), 4,362 test rows and 261-371 claims per window.

**Critic 6, `contract_years`: conceded.** Use calendar arithmetic (CLEAN-1).

**Critic 7, numbers and texts: conceded.** Re-measure every count after the fixes.

**One new fact, against my own case, for the curator.** With the agreed fixes (no-cover rows and `Payment` dropped,
the 12-month gap, a note for point 2), untuned learners only tie the premium alone: 0.172 against 0.162, with the premium at or above the
best learner in 3 of 5 windows. TP-4 is not met as proof: learners win 2 of 5 windows, and the TabArena methods,
tuned, have not been run. TP-2 keeps a small real signal, and the Tensions row P4 over P6 keeps the split. Before
the dataset ships, run the standard methods on the final design to settle TP-3 and TP-4.

</details>

<details><summary>Critic rebuttal</summary>

**Critic, rebuttal (2026-11-01): spanish_motor_insurance_2015_2018**

```text
Verdict: ship after changes, now with a condition. The advocate and I agree on the no-cover filter, dropping
  `Payment`, the 12-month gap with 5 monthly windows, and every cleaning and text fix. One dispute is left: the
  remedy for the shared claims (point 2).
New fact: the advocate's value claim (0.241 against the premium's 0.167) rests on `Policies_in_force`, the feature
  tied to the shared label. That count alone ranks the same windows at 0.306. Without it the model falls below the
  premium (0.137). On the clean rows (`Policies_in_force == 1`), no model I tried beats the premium.
Condition: TP-4 (Must) has to be checked with the benchmark's tuned methods on the fixed design (TP-1). If they do not
  beat the premium window by window, the verdict is `Trivial`. The exception is an answer from the authors (PROV-13)
  showing that claims are booked per policy; then the advocate's design stands.
```

My new checks are in the run folder. `rebut.py`/`rebut.txt` test the advocate's kept rows and my design.
`rebut2.py`/`rebut2.txt` split the advocate design's score by policy count. `rebut3.py`/`rebut3.txt` test four
models against the premium on the clean rows. All use 2 seeds, the advocate's LightGBM parameters, a 12-month gap,
the windows August to December 2017, and normalized Gini on the amount.

**A1. The core is a valid pricing task (SEL, USE-1, USE-6, LEAK-10).** Conceded. `Premium` is the written premium,
known at the quote. Every agreed drop stands, and so does the caveat that the curator re-confirms the new-business
framing. I narrow one point: "every validity finding is located row by row" holds only if the remedy in A2 actually
removes the defect. It does not.

**A2. First rows extended to the customer (USE-5 Must).** The trigger is conceded on both sides. I dispute the
remedy, and the evidence below decides it.

- **The customer filter leaves the shared label in the rows it keeps.** I checked this on the advocate's own 34,470
  rows (rebut.txt):
  - 1,269 kept rows have a dropped policy of the same customer that runs concurrently. A kept row claims at 0.832
    when that dropped policy claims, and at 0.105 when it does not (baseline 0.365).
  - The filter drops only the sibling that is in the sample. The link goes with the count of policies in force:
    - among the kept rows, the claim share rises from 0.33 (one policy) to 0.58 (four or more);
    - among customers with no other ID in the release, claims per row are 0.65, 1.15, 1.61, 2.01 and 2.46 for
      counts 1 to 5 (check4.txt). Their other policies are outside the sample, so no customer filter can see them.
  - 36.7% of the kept test rows have a count of 2 or more.
- **The score gain is the artefact.** On the advocate's 5-window design (rebut2.txt):
  - `Policies_in_force` alone (ties broken by the premium) ranks the windows at 0.306. The full model scores 0.246
    and the premium 0.167.
  - With the count dropped, the model scores 0.137, below the premium.
  - On the test rows with one policy, the model scores 0.139 against the premium's 0.248.
  - So "the task gets better" (0.275, ahead in 8 of 9) measures how well a model reads the booking of shared claims,
    not the policy's risk. P3 outranks P6: a score cannot validate a label.
- **The rule is cited the wrong way round.** USE-5 names diabetes_3 as the case where "a label checked and found to
  be another quantity ... still fails". It is not a licence to ship such a label as `approximate`. The approximate
  clause covers a label that cannot be checked. This one was checked, and the check gives 0.795 against 0.057 for
  rows with two or more policies (check2.txt).
- **What stands.** My remedy is to keep only `Policies_in_force == 1`. On those rows the link nearly vanishes: 0.48
  against 0.31, about the size of the mild customer effect.
- **PROV-13.** I agree that the request should not block. But it is now the decisive experiment (EV-1):
  - if the authors show that claims are booked per policy, the co-movement is a real customer effect, the count is a
    legitimate signal, and the advocate's design stands;
  - otherwise my filter stands.

**A3. Years without cover go.** Agreed: same filter, same counts. The rule we cite differs (the advocate cites USE-7;
I cite USE-5 and LEAK-25), but the remedy is the same.

**A4. Split.** Agreed: the temporal regime, test rows of new contracts, and `TemporalSplits(window=1, unit="months",
gap=12, min_train_fraction=0.5)` with 5 windows. The gap also removes the label link between customers, so SPLIT-9 is
met with no further filter. The floor holds under either set of filters: 55.1-74.9% of the rows train under the
advocate's filters, 57.8-78.5% under mine (check3.txt). One point narrowed: "without the filters the gap design sits
at the premium's level" fits A2. The edge the filters add comes from the policy count.

**A5. Kept features.**
- `Value_vehicle` stays: conceded.
- `Payment` goes: agreed.
- `Policies_in_force`: disputed. The calendar-year timing is the small issue, and onlinenewspopularity's test covers
  it. That test does not reach the larger one: the feature ranks at 0.306 on its own because the label is shared
  (A2). A `Potential leak, kept on purpose:` note can name a timing remnant. It cannot license a feature whose power
  is another quantity's label (USE-5 outranks the LEAK-10 clause by part).
- Under my remedy the column becomes constant and goes. If the curator rejects that remedy, my fallback stands:
  subtract the 2,865 located later additions, add the note, and name the shared count as a gap in `fit_reason`.

**A6. Worth benchmarking.**
- Conceded: MET-2 (every fold can be scored; 117-195 claims per window even on the clean rows), MET-10 as a Weigh
  only, SPLIT-21 (November and December stay), monthly windows, and the text fix to the metric reason.
- Disputed: "TP-4 holds". The advocate's evidence is the 0.241 against 0.167 shown in A2 to rest on the count.
- On the clean design (no-cover dropped, `Policies_in_force == 1`, `Payment` dropped, gap 12, 5 windows; 25,665
  rows), the premium ranks at 0.234 (rebut3.txt):

  | method | mean Gini | ahead of the premium |
  |---|---|---|
  | ridge on log1p with log premium | 0.229 | 2 of 5 windows |
  | logistic model of a claim | 0.234 | 2 of 5 windows |
  | LightGBM on log1p | 0.121 | 1 of 5 windows |
  | LightGBM with a Tweedie loss | 0.125 | 1 of 5 windows |

- This is a TP-4 flag, not a verdict. TP-1 (Must) asks for the benchmark's tuned methods before acting on it.
- The remedy is to run the tuned methods on the fixed design before shipping. If none beats the premium window by
  window, the dataset is `Trivial` (TP-4), unless the authors' answer in A2 restores the count or the renewal rows.
- TP-2 does not save a task that the premium already solves: TP-4 is the Must that comes after it.

**A7. Cleaning and texts.** Conceded, all of it. One adjustment follows from A2: if `Policies_in_force == 1` is taken,
`use_case` says "new business from customers with no other policy". The gap `fit_reason` names is then the narrower
one, the undocumented booking of claims, not the shared count.

</details>
