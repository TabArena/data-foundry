# spanish_homeowners_motor_insurance_2010_2014

**Outcome:** added; shipped on your verdict of 2026-11-02. The AI recommended shipping after text changes. The authors' release (Mendeley Data vfchtm5y7j, CC BY
4.0): 122,935 customer-years of 40,284 Spanish customers who held a motor and a home policy with one insurer in 2010,
followed until they lapsed either one, 2010-2014. The target is the year's home claim cost (0 for 98.2%), shipped as
log1p and scored on the amount by the normalized Gini; the inputs are 13 rating fields and the customer's earlier home
and motor claims; three yearly test windows, 2014, 2013 and 2012, each trained on all earlier years. Validity: SEL-1,
SEL-2, USE-1, USE-5, LEAK-34, PROV-1 hold; USE-8 approximate (no current premium, closed 2010 cohort); the split rules
SPLIT-9, SPLIT-11 and SPLIT-14 hold; LEAK-10 fixed (the year's own outcomes dropped); the rating fields read once are
kept with a note (issue 1); SPLIT-10 departed from, no gap (issue 2). Value: TP-9 holds (240 / 310 / 448 claimants per
window); TP-2, a small real signal (untuned models 0.11-0.32 against 0 for a constant). Quality: CLEAN-10 not triggered
(`age_of_car_M` zeros kept with a note); CLEAN-11 notes (microcar powers, 84% "rural"); CLEAN-19 `past_*` kept as
counts; aging the frozen ages open (issue 4). Weighed: the original release +, a real renewal decision +, the claim
history signal +; frozen rating fields -, a closed 2010 cohort -, noisy windows -.

Changes made (2026-11-02), no decision needed: the text of `use_case`, `fit_reason`, `splits_comment`, the metric reason
and the notes was corrected after the panel (wording and numbers only; see the mediator's list). The split is unchanged
(train 89.2 / 75.3 / 57.0%, 240 / 310 / 448 positives).

**Main points:** Shipped (Andrej, 2026-11-02). Every issue is resolved as implemented: the 13 rating fields kept after
a nine-test leak check (1), no gap (2), the Gini (3), the frozen ages (4), two warnings accepted (5).

**Issues for Andrej:**

1. **Keep the 13 rating fields that were read once, the two payment methods included?** Every rating field (age,
   seniority, car, payment methods, insured values, apartment) holds one value per customer in all five years, and the
   age never grows: the insurer read them once, on a date the sources do not give. A field read after the claims could
   carry them (a customer who switches to monthly payment after a claim).
   * What it does to the task: if the read was in 2010, every input is what the renewal knew; if later, a few fields may
     hint at claims the model should not see yet.
   * Evidence for a read in 2010: the data article selects the sample "in 2010"; no field's link to a home claim moves
     across 2010-2014 (ROC AUC range at most 0.045) or towards a lapse (at most 0.07, no trend); the annual-payment
     share is 3-9 points lower with a home claim in every year, with no trend; 10 customers are under 23, impossible for
     a read in 2015 (they would have been under 18 when the 2010 sample was drawn; these 10 also have odd seniority
     values, so this is circumstantial).
   * Against: a flat pattern cannot rule out a late read after a switch. Dropping both payment fields lowers the mean
     Gini from 0.219 to 0.206 (LightGBM) and 0.279 to 0.269 (ridge), within the noise.
   * Rule: LEAK-10 (Must), its later-pull clause, which is your case-by-case call (Lennart, 2026-10-26): a value that
     may have been read after the prediction point, where we cannot tell which rows it affects, stays with a note only
     if the rows we can check show no gain from it.
   * Precedent: spanish_motor_insurance_2015_2018 (AI draft, open) drops its `Payment`, described there as "Last payment
     method" (half-yearly payment 40% in first claim years against 26% otherwise). What sets this table apart: no "last"
     wording, a sample selected in 2010, and an annual-payment gap with a home claim that shows no trend by year.
     Whichever you decide here should also settle the sibling.
   * Implemented: (a) keep all 13 with the note, the distinguishing facts recorded. Alternatives: (b) drop the two
     payment fields (mean Gini 0.219 to 0.206, within noise), and drop `Payment` in the sibling the same way; (c) keep
     here and ask the authors (Guillen, Bolancé) for the read date, then revisit; (d) amend LEAK-10's later-pull clause
     for once-read fields whose link to the target is flat over the panel.

   Recommendation: (a). Decision: (a), (b), (c) or (d)?

   **Andrej (2026-11-02, discuss):** You should do an extensive leakage check and then suggest what to do. Asking the
   authors is not an option

   **Answer (AI, 2026-11-02):** Nine tests on the 13 fields find no gain that a late read could have carried into the
   target. (1) Read date: seniority's floor is 5.002 years in every exit cohort, so every customer was read on one date,
   not at exit; whether that date is 2010 or later stays unknown. (2, 3) Each field's link to a home or motor claim by
   year: 2 of 26 slopes are significant, both in fields no claim can change (gender, apartment); the payment slopes are
   about +0.003 a year. (4) Renewing rows against lapse rows, where no update after a claim was possible: the payment
   fields differ by +0.004 on home claims, below the +0.009 of fields no claim can change. (5) The sibling's design
   (spanish_motor_insurance_2015_2018): no pattern on home claims (annual payment 5.9 points rarer after a claim for
   renewers, 8.1 for 2010 lapsers), but `Policy_PaymentMethodA`, the motor payment, does show it on motor claims (9.6
   against 0.6 points). (6) Dropping the payment pair moves the mean Gini by -0.013 (null SD of the 3-window mean
   0.045); dropping A alone by +0.002. (7) The pair's gain on renewing rows minus lapse rows: -0.006 [-0.018, 0.006].
   (8) The fields alone rank home claims at ROC AUC 0.656-0.672 in every year 2011-2014, flat. (9) On customers who
   never had a motor claim the pair still adds +0.019. Suggestion: (a), keep all 13 under LEAK-10's later-pull clause
   (the traced part shows no gain), with `Policy_PaymentMethodA` noted as a potential leak kept on purpose (LEAK-37, as
   digicow_farmer_training_adoption_challenge): its motor pattern does not reach the home target. The note is now in the
   definition. The cautious alternative (b), dropping A alone, costs nothing measurable (+0.002). (c) is withdrawn. The
   sibling's drop stays apart: its pattern sits on its own target. Decision: (a) or (b)?

   **Andrej (2026-11-02, ok):** I go with a)

   **Resolved (2026-11-02, Andrej):** (a), all 13 rating fields kept under LEAK-10's later-pull clause,
   `Policy_PaymentMethodA` with its potential-leak note (LEAK-37).

2. **Accept no gap between training and test years (an exception to SPLIT-10)?** At a renewal the previous year's claims
   are not all known: the last weeks' claims are missing, and if `year` runs from each customer's renewal date (the
   sources do not say), the newest training year can overlap the test year by up to a year.
   * What it does to the task: models train on, and read as inputs, slightly more complete claims than the insurer had.
     The effect is within noise: hiding 30 or 90 days of the newest year's claims gives a mean Gini of 0.226 and 0.203
     against 0.219; dropping the whole newest training year gives 0.200.
   * Implemented: no gap; the exception is written in `splits_comment`. Alternative: a one-year gap, the smallest the
     yearly column allows. It leaves the 2012 window a training side of 33%, so only two windows meet SPLIT-14 (at least
     50% training rows).
   * Rule: SPLIT-14 (Must) wins over SPLIT-10 (Should); SPLIT-9 holds: no measured gain comes from the incomplete last
     year. Follows pricing_game_2016_french_fleet (2026-11-02) and your CC on avito_demand_prediction declining the
     amendment.

   Recommendation: accept, recorded as `Exception to SPLIT-10`. Decision: accept?

   **Resolved (2026-11-02, Andrej):** accepted: no gap, an exception to SPLIT-10 that serves SPLIT-14, as in
   pricing_game_2016_french_fleet; recorded in the record.

3. **Confirm the normalized Gini for this table?** Neither paper scores predictions, so the metric comes from the
   insurance context (MET-11). Decided on this table alone (MET-10, amended 2026-11-02): RMSE on the amount follows the
   20 largest claims (83-94% of the squares; every model R^2 at or below 0); the source's own model family, a Tweedie
   deviance on the amount, ranks the training mean above every fitted model in every window, including a Tweedie
   LightGBM. Under the Gini every model beats the constant (0.11-0.32 against 0). The Gini's limit: it ignores the price
   level, and the 20 largest claims still carry 40-58% of each year's loss, so one window's standard error is 0.07-0.10;
   models are compared on the mean of the three windows. Confirming also lets Claude strike the record's stale screening
   proposal of `rmse` (as in australian_vehicle_insurance_2004_2005).

   Implemented: `normalized_gini` on the amount, from context, target shipped as log1p. Alternatives: a mean Tweedie
   deviance on the amount (the source's own model family; a constant beats every fitted model in every window, so it
   would rank models by calibration of a few large claims); RMSE on the amount (driven by the 20 largest claims, R^2 at
   or below 0).

   Recommendation: confirm. Decision: confirm?

   **Resolved (2026-11-02, Andrej):** confirmed: `normalized_gini` on the amount from context, decided for this table;
   the record's screening proposal of `rmse` is superseded.

4. **Age the frozen ages by the year?** `Age_client`, `Client_Seniority` and `age_of_car_M` show the 2014 rows the
   values of the read date. Adding `policy_year - 2010` would give each year's value if the read was in 2010.
   * What it does to the task: nothing measurable. The year is already an input, so ridge scores the same (0.279), and
     LightGBM moves within noise (0.219 to 0.223).
   * For: fixing a value ranks above noting it (principles, remedy ladder). Against: it rests on a read date the sources
     do not give; read earlier, the aged values are still wrong.
   * Rule: none decides it; a cleaning fix is made when cheap and safe (principles, step 3), and the safety is the open
     point.
   * Implemented: the frozen values as released, with the note. Alternative: add `policy_year - 2010` to the three
     fields, exact only if the read was in 2010.

   Recommendation: keep the frozen values with the note. Decision: keep or age?

   **Resolved (2026-11-02, Andrej):** kept: the frozen values as released, with the note.

5. **Accept two check warnings?** `task_time_on_few_unique` warns that the time column has few distinct values: here 5
   years, so the 3 test windows train on only 2-4 earlier years. `task_target_value_dominant` warns that one value fills
   most of the target: here 98.2% of customer-years cost 0, a real no-claim year and not a placeholder. Implemented:
   neither is in `accepted_check_warnings` yet. Accepting adds both with these reasons. The alternative is to leave them
   as open warnings. Precedent: `task_target_value_dominant` is accepted in frempl_french_motor_personal_line,
   australian_vehicle_insurance_2004_2005 and the two pricing games (pricing_game_2016_french_fleet,
   pricing_game_2017_french_mtpl). No definition accepts `task_time_on_few_unique` yet
   (wisconsin_local_government_property_insurance_fund proposes it, open), so this becomes the precedent.

   Recommendation: accept both. Decision: accept?

   **Resolved (2026-11-02, Andrej):** both accepted; `accepted_check_warnings` now holds them with these reasons
   (dataset check: 0 errors, 0 warnings).

**Review panel:** ship after changes (mediator). Claim audit: 33 claims, 26 hold, 3 partly refuted and 1 refuted (all
wording, fixed), 1 stale, 2 untested. Blind review (which assumed RMSE on log1p, not the shipped Gini): include with
changes; main concerns the metric on the zero-heavy target and the frozen covariates; its suggestion to keep `PolID` as
a group column is answered by the split audit (known customers are the renewal use case). Agreed: the split without a
gap, the Gini on the amount (the deviance check settled it), the `past_*` counts with a note, the text changes. Disputed
and left to the curator: the payment-method pair (issue 1) and aging the frozen ages (issue 4).

<details><summary>Mediator</summary>

**Mediator (AI, 2026-11-02): spanish_homeowners_motor_insurance_2010_2014**

**Recommendation**

```text
Verdict: ship after changes (text only; no re-split, no column change unless the curator picks otherwise in issues 1 or 4).
Validity: SEL-1, SEL-2, SEL-16 hold; USE-1 holds (reword the Sec. 3.5 quote); USE-8 approximate (add: no current premium,
survivor drift, lapse-row claim share); USE-5 holds (lapsers keep every year; lapse rows claim more, 2.21% vs 1.65%);
LEAK-10 triggered, fixed (same-year outcomes dropped); LEAK-10 later-pull clause: 13 rating fields read once, kept with a
note, the curator's case call (issue 1); LEAK-34 holds (history from earlier rows only, verified twice); SPLIT-6, 11, 12,
14 hold; SPLIT-9 holds (no measurable shortcut); SPLIT-10 departed, exception serving SPLIT-14 (issue 2); PROV-1 holds
(Table 1 matched).
Value: TP-9 holds (240-448 positives per window; null SD of the Gini 0.066-0.101); TP-2, a small real signal (keep);
MET-3 holds (log1p shipped, scored on the amount); MET-11 context origin holds on this table's own evidence (a Tweedie
deviance ranks a constant above every fitted model); MET-10 decided per table, not for the family (issue 3).
Quality: CLEAN-10 not triggered (age_of_car_M zeros kept); CLEAN-11 notes (microcar powers, metro share); CLEAN-19
past_* kept as counts (settled below); aging repair of the frozen ages open (issue 4).
Weighed: original release +, real renewal decision +, claim history signal +; frozen fields -, closed 2010 cohort -,
noisy windows -.
For the curator: issue 1 (Must, the rating-field keep and the payment-method pair), issue 2 (accept the no-gap
exception), issue 3 (confirm the Gini for this table), issue 4 (aging repair, a weighing), issue 5 (warnings).
```

**Agreed facts** (every panel member who measured them agrees; the claim auditor recomputed each)

* 122,935 customer-years of 40,284 customers; yearly 40,284 / 29,818 / 22,505 / 17,044 / 13,284; all start in 2010, years
  consecutive, no new entrants; claimants 660 / 531 / 448 / 310 / 240 and their mean costs match the data article's
  Table 1; SHA-256 unchanged.
* 98.2% of rows cost 0; `NClaims2` is the home count (the "motor" wording is a typo); `Types` and `Retention` encode
  the year's outcomes and are dropped; the history columns use earlier rows only.
* All 13 rating fields hold one value per customer; `Age_client` never grows.
* Lapse rows have the higher home claim share: 2.21% against 1.65% pooled (2.01-2.69% vs 1.51-1.77% by year). The
  column auditor's table has the two groups swapped; its "partial lapse years" reading is withdrawn by the facts.
  Claim years end in a lapse more often (30.7% vs 24.5%).
* Splits: train 89.2 / 75.3 / 57.0%, test 13,284 / 17,044 / 22,505 rows with 240 / 310 / 448 positives; every test
  year wholly on the test side; 91% of test rows match the same customer's earlier row (known entity, not a copy).
* A one-year gap leaves 2012 a 32.8% train side (SPLIT-14 fails); late-claim simulation (calendar-year reading): mean
  Gini 0.219, 0.226 at 30 days, 0.203 at 90 days.
* Mean Tweedie deviance (power 1.5) on the amount: the train-mean constant beats every fitted model in every window,
  including LightGBM with the Tweedie objective (critic 27.1 / 18.2 / 22.2 against 21.8 / 18.0 / 20.3; advocate the
  same with bootstrap SEs). Under the Gini the same models score 0.11-0.32 against 0 for the constant.
* The 20 largest claims hold 83-94% of each test year's sum of squares and 40-58% of its total loss.
* Ages: 4 customers are 18 and 10 under 23 (one value each), so `Age_client` was not read in 2015.

**Decisive experiments (mine)**, scripts and logs in the run folder (`variants.py`, `gap_shipped.py`,
`age_floor.log`): untuned LightGBM on log1p (3 seeds) and ridge on log1p, the 3 shipped windows, normalized Gini on the
amount.

| variant | LGBM 2012 / 2013 / 2014 | LGBM mean | ridge mean |
|---|---|---|---|
| shipped | 0.182 / 0.315 / 0.161 | 0.219 | 0.279 |
| payment fields dropped | 0.202 / 0.315 / 0.099 | 0.206 | 0.269 |
| Age, Seniority, age_of_car + (year - 2010) | 0.221 / 0.324 / 0.124 | 0.223 | 0.279 |
| Age only aged | 0.197 / 0.294 / 0.124 | 0.205 | 0.279 |
| past_* as per-year rates | 0.182 / 0.313 / 0.150 | 0.215 | 0.268 |
| past_* dropped | 0.182 / 0.317 / 0.133 | 0.211 | 0.267 |

Reading: every difference sits inside the noise (LightGBM moves by 0.02 between two re-parametrisations that carry the
same information; the null SD of one window is 0.07-0.10). Ridge is exactly unchanged by the aging repair, because
`policy_year` is already an input. None of the three open points is decided by score; each is decided on meaning.

Policy-year bound on the shipped frame (newest training year dropped): 2014 0.161 to 0.148, 2013 0.315 to 0.244, 2012
0.182 to 0.207 (train 32.8%); mean 0.219 to 0.200. The builder's `exp_gap.txt` numbers (0.317/0.244, 0.133/0.145) came
from a frame without `past_*`; these replace them.

The age floor is weaker than both debaters read it: all 10 customers under 23 are among the 76 whose seniority exceeds
age minus 18 (an 18-year-old with 13.6 years' seniority), so these rows are odd in both fields. It still rules out a
read in 2015 (EV-6: circumstantial, not proof of a 2010 read).

**Disputed points**

1. *`past_*` counts or per-year rates (P7, CLEAN-19 Should).* Split auditor: a rate, or a note, because the span grows
   (mean 0.029 in 2011 to 0.121 in 2014). Advocate and critic (rebuttals): counts with a note. Rule: CLEAN-19 builds the
   input the actor reads at the prediction point; at a 2014 renewal the insurer reads the 4-year count, and in every
   training year it read the count of that year's span, so the drift is the real one and the split does not invent it.
   The rate is our own construct and scores lower (ridge 0.268 vs 0.279; LightGBM 0.215 vs 0.219). **Settled: keep the
   counts, add the note.** Not a curator issue.
2. *The payment-method pair (P4, LEAK-10 later-pull clause, Must).* Not a conflict of rules: one rule, applied as "a
   case-by-case judgment of the curator" (Lennart, 2026-10-26). It goes to the curator (issue 1). Best evidence for the
   keep: no "last" wording; the sample was selected in 2010; the annual-payment gap with a home claim shows no trend by
   year (7.0 / 7.3 / 3.7 / 3.3 / 8.7 points) or by years before a lapse; `Age_client` was not read in 2015. Against: the
   flatness cannot rule out a late read after a switch (precedent checker); the fields carry a small score (dropping both
   moves the mean Gini 0.219 to 0.206 LightGBM, 0.279 to 0.269 ridge, inside the noise); the sibling drops its
   `Payment`. What would settle it: the read date from the authors (Guillen, Bolancé). Recommendation (a), keep with the
   distinguishing facts; the sibling's drop is an open AI draft, not a curator precedent.
3. *Aging repair of the frozen ages (P7; remedy ladder against an unstated read date).* Advocate: optional, as a lower
   bound. Critic: only if the curator accepts the 2010 read. Rules leave it open: a repair ranks above a note, but a
   cleaning fix must be "cheap and safe" (principles, step 3), and safety rests on a read date the sources do not give
   (all fields frozen together; the youngest ages are the seniority anomalies). It changes no score (ridge identical,
   LightGBM within noise). To the curator (issue 4). Recommendation: no repair; the frozen value is what the release
   says, the note names it. `age_of_car_M`'s zeros are a separate point and not open: CLEAN-10 applies only when the code
   can be inferred, so they stay with the note.
4. *The metric (P6).* Settled in the debate by the deviance experiment (both sides). Gini stays on this table's own
   evidence (MET-11 context; MET-10 per table, not in doubt, so the diversity factor does not arise). The curator's CC
   is still needed to confirm it and strike the record's stale `rmse` fallback (issue 3).
5. *No gap (P4).* Agreed: SPLIT-14 (Must) wins over SPLIT-10 (Should) by strength within P4, the tension row
   "unmatured training labels against the training floor"; SPLIT-9 is met because no shortcut can be measured. Only
   the text was disputed and both sides accept the rewrite. The curator accepts the exception (issue 2).

**Changes to make now** (no decision needed)

1. `use_case` and the first `curation_comments` bullet: "The model paper prices the next period's home premium for such
   customers (Frees et al. 2021, Sec. 3.5, Table 8)"; the paper argues the premium should allow for lapse, so do not
   present "assuming the insured will renew" as its position (USE-1).
2. `fit_reason` and the Rows bullet: no current premium, so the task ranks renewal risk; the test book drifts towards
   claim-free survivors (30.7% of claim years end in a lapse, 24.5% of claim-free years); lapse rows claim more (2.21% vs
   1.65%), so nothing points to cut lapse years (USE-8, USE-5).
3. `splits_comment` rewritten (SPLIT-10 exception, principles "Strengths"): name both readings of `year`; calendar-year
   bound from the 30/90-day simulation (0.226 / 0.203 against 0.219); policy-year upper bound from the dropped-year run
   on the shipped frame (mean 0.219 to 0.200; 2013 0.315 to 0.244, about one standard error); the null SD 0.066-0.101
   and "compare models on the mean over the 3 windows" (TP-9); cite pricing_game_2016_french_fleet and the CC of
   2026-11-02 on avito_demand_prediction. **No re-split.** The split must still reproduce: test 2014 / 2013 / 2012, train
   89.2 / 75.3 / 57.0%, test rows 13,284 / 17,044 / 22,505, positives 240 / 310 / 448.
4. Metric reason and the log1p bullet: drop "family's convention", "as in the sibling claim tables" and the siblings as
   "the same choice"; give the per-table reason (CLEAN-16 default, the scale test, MET-3); add the 40-58% loss share,
   the null SD, and the deviance result (MET-10 amended, MET-11).
5. Frozen-field note: "no field moves by more than 0.045 by year, and at most 0.07, without a trend, by years before a
   lapse" (EV-1); add the read-date evidence (Specifications Table 2010; no age implies a 2015 read; no "last" wording)
   (LEAK-10).
6. Anomaly bullets: `Car_power_M` 4-15 "unusual (microcar range)", not implausible (CLEAN-11); `age_of_car_M` above age
   minus 18 for 161 customers (likely the car's age); judgment line "CLEAN-10 not triggered (code not inferable)";
   `metro_code` 84% "rural" (PROV-13); `Client_Seniority` >= 5 with both readings, the sample's selection or a read at
   the window's end (PROV-13); insured-value medians are over rows.
7. Added-columns bullet: `past_*` span grows with the year (mean 0.029 in 2011 to 0.121 in 2014), kept as the counts the
   insurer reads; rates scored lower (CLEAN-19).
8. Then `dataset check`, regenerate the README, ruff and the dataset test.

**Consistency with precedent** (precedent checker's report, plus my checks)

* No gap: follows pricing_game_2016_french_fleet (Andrej, 2026-11-02) and the declined SPLIT-10 amendment (CC on
  avito_demand_prediction, 2026-11-02); no new amendment prompt is due.
* Metric: follows the MET-10 amendment once the family wording goes. Not matched to the sibling Ginis, which are AI
  drafts (australian issue 4 open).
* Target scale log1p: follows the curator's per-file call (australian issue 5, 2026-11-02).
* Payment pair: departs from spanish_motor_insurance_2015_2018's `Payment` drop (AI draft). Distinguishing facts named
  in issue 1; becomes a consistency question, not a silent departure.
* History features: opposite of pricing_game_2016 (not added) on different facts (signal 6.0% vs 1.7% here; none
  there).
* `age_of_car_M` zeros: differs from wisconsin (structural zero, exact) and australian (impossible value) in kind.
* `task_time_on_few_unique`: first acceptance in the working copy; record it as the precedent.
* Fit approximate: as spanish_motor_insurance_2015_2018 and wisconsin; differs from pricing_game_2016 (`direct`) on the
  facts in `fit_reason`.

</details>

<details><summary>Claim audit</summary>

**Claim auditor: spanish_homeowners_motor_insurance_2010_2014 (AI, 2026-11-02)**

**Verdict.** No validity claim was refuted. Every fact about the data that I could recompute holds: the counts, the closed cohort, the frozen rating fields, the target, the drops, the history columns, the splits and the metric's computability. Two refutations bear on the metric. (1) The builder treats the metric as a call for the family ("Decision: confirm (family consistency)"). That framing contradicts the curator's MET-10 amendment of 2026-11-02, under which each table's metric is decided on its own. (2) The reason argues against RMSE because "RMSE follows a few large claims" and leaves the Gini looking immune. On the amount, the Gini also gives 40% to 58% of each test year's weight to the 20 largest claims, and a random prediction scores within ±0.07 to ±0.10 (1 SD). Three statements in the notes are slightly wrong (listed below). One interpretation is untested.

Scripts and output: `a1.py` (run folder), `a2.py`, `a3.py` (raw file, the definition through `dataset_io`, and `data_foundry.v2.metrics.scorer`).

**Claims table**

| claim | source | test | result | evidence | rule |
|---|---|---|---|---|---|
| 122,935 customer-years, 40,284 customers; yearly 40,284 / 29,818 / 22,505 / 17,044 / 13,284 | task_summary.row, builder 1 | count raw | holds | exact | PROV-1 |
| Every customer starts in year 1, years consecutive, no new entrants (contra Specifications Table) | curation_comments Rows, builder 2 | first year per PolID; asserts in `_clean` | holds | all 40,284 start in year 1 | USE-5 |
| 10,988 (27%) still hold both after 2014; lapsers keep every year | Rows | Retention of the year-5 rows | holds | 10,988 = 27.3% | USE-5 |
| Retention is 0 exactly on each lapser's last row | Dropped bullet, builder 10 | crosstab of year, last row and Retention | holds | 0 on a non-last row in 0 cases; 2,296 lapses in 2014. Table 1 of the article says 3,780 lapses in 2013, the file 3,760 (a typo in the source) | LEAK-10 |
| Year 1 = 2010 | Time bullet | Table 1 of the article | holds | article Table 1 has columns 2010 to 2014 | PROV-1 |
| 98.2% zeros; positive 2.06 to 27,280, median 169; positives 660/531/448/310/240 and their means match Table 1 | Target bullet | raw against Table 1 | holds | 98.22%; means 447.9/501.6/410.7/348.1/508.9 = Table 1 | PROV-1 |
| Cost > 0 only where NClaims2 > 0; 1,742 claims with 0 cost "closed without payment" | Dropped bullet | crosstab; zero-cost claims per year | holds (the cause is untested) | 0 rows with a cost and no count. The zero-cost share of the year's claims is flat, 0.78 to 0.81 by year, so 2014 shows no rise from late costing | LEAK-24 |
| NClaims2 is the home count (the description's "motor" is a typo) | Dropped bullet, builder 9 | Types against the counts; motor claimants against Table 1 | holds | Types=3 (home, no motor) has NClaims2>0 and NClaims1=0 in all 2,123 rows; Claims1>0 per year is 769/547/318/209/124 = Table 1's motor row | PROV-13 |
| Every rating field is constant per customer; age does not grow | Note bullet, builder 4 | `nunique` per PolID (assert in `_clean`) | holds | 0 customers change | LEAK-10 |
| Rating fields: AUC flat over 2010-2014 and over the years before lapse; "no field moves by more than 0.045" | Note bullet, builder 5 | AUC of each field for a home claim, by year and by years before the last row (lapsers only) | **partly refuted** | By year the largest range is 0.045 (Age_client); holds. By years before lapse it is 0.070 (Insuredcapital_content_re), 0.067 (Car_power_M) and 0.066 (age_of_car_M). These moves are not monotone, and the 3-years-before bin has only 95 positives (AUC SE about 0.03), so they read as noise. appartment stays at 0.629 to 0.639. The conclusion holds; the number does not | LEAK-10, EV-1 |
| Client_Seniority ≥ 5.0 is "the sample's selection" | Anomaly bullet; builder "survivors of a book with at least 5 years' seniority" | min seniority per lapse cohort | **untested** (an equal alternative remains) | The minimum is exactly 5.0 in every lapse cohort (years 1 to 5). The article says "There was a window of observation until 2015". A reading in 2015 of the tenure since the first contract gives the same floor of 5. Both readings hold the value fixed per customer, so neither one leaks | PROV-13, EV-7 |
| Previous-year home claim lifts the claim share from 1.7% to 6.0% (2,477 rows); 2 of 98 repeat the amount | Added bullet | recompute | holds | 6.02% vs 1.72%, 2,477 rows | USE-10, LEAK-34 |
| History columns use earlier rows only, missing in 2010 | Added bullet | code (`shift(1)` within PolID); NaN share | holds | NaN in 32.8% of rows = 2010 | LEAK-29 |
| Insured values on a log scale; exp medians 31,647 / 104,457; 403 equal; 9.7% content above building | Note bullet | recompute | holds | The medians are over rows (over customers: 31,313 and 103,101). 403 customers have equal values (1,176 rows) | CLEAN-12 |
| num_policiesC 0 (19%) and 1 (81%) | Anomaly | recompute | holds over rows (18.9/81.1); over customers 17.7/82.3 | | PROV-13 |
| age_of_car_M = 0 for 8,050 customers (20%); 65 vs 58 years old, 15.3 vs 9.1 years seniority | Anomaly | builder exp_gap.txt and recompute | holds | | CLEAN-10 |
| 76 customers have seniority > age minus 18; Car_power_M 4 to 15 in 103 rows | Anomaly | recompute | holds | 103 rows = 31 customers | CLEAN-10 |
| Splits: test 2014, 2013, 2012; train 89/75/57%; test 13,284/17,044/22,505 rows with 240/310/448 positives; each trained on all earlier years | splits_comment, builder 19 | `to_container`, split years | holds | train years {2010-13}, {2010-12}, {2010-11} | SPLIT-6, SPLIT-11, SPLIT-14 |
| One window's Gini has bootstrap SE 0.06 to 0.11 | splits_comment | 300 random predictions per window under the declared Gini | holds | null SD 0.075 (2012), 0.066 (2013), 0.101 (2014) | TP-9 |
| No gap: dropping the newest training year moves 2013 0.317 to 0.244, 2014 0.133 to 0.145, "inside one window's noise" | splits_comment | against the null SD | holds (borderline) | -0.073 on 2013 is 1.1 null SD | SPLIT-10 exception |
| No test row is a copy across the split | implied; builder "0.0% exact copies" | hash of all features except the year | holds as framed | 91.5/91.1/90.9% of test rows equal a training row in every feature except the year: the same customer a year earlier with no new claim. This is a known entity by design, not a copy | LEAK-34, USE-10 |
| Every feature is known at the renewal | implied | review of the columns | holds with the stated note | The same-year outcomes are dropped. Previous-year claims are as finally recorded (noted). The frozen fields are read at an unknown date (noted) | LEAK-10, SPLIT-9 |
| Lapse years are full years (stated as unknown) | fit_reason | home claim share on lapse rows vs renewing rows | untested directly; no sign of truncation | Lapse rows show a share of 2.21% vs 1.65% (a higher share, where a cut exposure would lower it). There is no exposure column, so the time-on-risk rule (LEAK-10/LEAK-7, 2026-11-02) does not trigger | LEAK-10, USE-5 |
| Metric `normalized_gini` from context, on the amount (`target_transform="log1p"`) | dataset.py `metric`, README Metric block | I read the article (Sec. 2) and the model paper (Secs. 3.3-3.5), checked the definition against the code and scored dummies on every fold | holds as computable (MET-2); the origin can be contested (see below) | The source scores no predictions (confirmed: Tweedie and logistic fits, p chosen by maximum likelihood). Constant = 0 (±1e-15) on all 3 folds, oracle 1.0, negated oracle -1.0. Positives per fold are 240/310/448. The definition text matches `_gini` | MET-1, MET-2, MET-11, MET-13 |
| Reason: "RMSE on the amount follows a few large claims: the 20 largest of each test year hold 83% to 94% of its sum of squares" (implying the Gini does not) | metric reason | the 20 largest claims' share of each test year's total loss (the Gini's weight) | **partly refuted** | The SS shares hold (0.884/0.829/0.942). The 20 largest claims also carry 43.3%, 39.8% and 58.1% of each year's total loss. The Gini on the amount has a null SD of 0.066 to 0.101. On log1p it would be 0.030 to 0.039 | MET-3, MET-10, TP-9 |
| "Frees, Meyers and Cummings (2011, JASA 106:1085-1098)", Allstate 2011 row Gini | metric reason | citation; the sibling allstate definition | holds | | EV-4 |
| Metric "same choice and scale as" four siblings; REVIEW issue 5 "Decision: confirm (family consistency)" | builder report, issue 5 | metrics.md MET-10 register row | **refuted** | MET-10 amendment (2026-11-02, Andrej): "no family call on the metric: each table's metric is decided on its own, and in doubt for diversity" | MET-10 (amendment) |
| Use case: the model paper prices the next period's premium "assuming they renew" (Sec. 3.5) | task_summary.use_case | ESWA Sec. 3.5 text | **partly refuted (wording)** | Sec. 3.5 says the usual premium assumes renewal, "However ... the premium should be obtained by considering ... that the insured may or may not renew". Its Table 8 is the quotient of premiums with and without the claim-lapse correlation. The renewal decision is still the source's, so USE-1 holds | USE-1 |
| Footnote 1: insurers reward a claim-free year at renewal | Added bullet | ESWA footnote 1 | holds | "Most companies reward customers with a price rebate when they renew ... if they have not reported claims in the year previous" | USE-10 |
| "random sample ... who held both policies in 2010, followed until they lapsed either policy" | row | DiB Specifications and Sec. 1 | holds | "Random sample of real insurance portfolio"; "If the customer does not renew one of those two policies or both, we do not have more information" | PROV-1 |
| Warnings to accept: `task_time_on_few_unique` (2 to 4 train years), `task_target_value_dominant` (98.2% real zeros) | builder | splits; zeros | holds | | — |
| CC BY 4.0; SHA-256 904906d5...4eeb | download_description | `sha256sum` | holds (hash); licence not re-fetched | hash identical | PROV-10 |
| Record screening: "Proposed fallback `rmse` in euros" | record, screening Metric bullet | compare with dataset.py | **stale** | dataset.py declares normalized_gini. In the australian precedent the curator struck the rmse fallback from the record | MET-11, EV-7 |

**Refuted and untested claims, ranked (principles.md: validity first)**

1. **P6, MET-10 (refuted): the family-consistency framing of the metric.** The builder report and draft issue 5 ask the curator to confirm the Gini "as the four siblings". The curator's amendment of 2026-11-02 rules out a family call. *Changes:* the curator must decide the metric for this table alone, and in doubt for diversity. The source fits Tweedie GLMs and chooses p by maximum likelihood (DiB Sec. 2), so a deviance on the amount, such as `mean_poisson_deviance`, which exists in the library, is the source-anchored alternative. The context origin (MET-11: "only when the context is clear") then needs a per-table argument. *Mildest remedy:* reword issue 5 without "family consistency"; the reason in dataset.py is already per-table. Give the curator the Gini-vs-deviance choice with the numbers below.
2. **P6, MET-3/TP-9 (partly refuted): the reason's contrast with RMSE.** The Gini on the amount also follows the large claims: the 20 largest carry 40% to 58% of each test year's loss, and a random prediction scores within a null SD of 0.07 to 0.10. The best untuned models score 0.13 to 0.32, so the model gaps between families (ridge 0.280 vs LightGBM 0.219) sit inside one window's SE. *Changes:* nothing in the data; the strength of the metric's claim and the value (P6) are weaker than they read. *Mildest remedy:* add the loss-share and null-SD numbers to the reason or the splits_comment. Also put to the curator in the TP-9 issue that the Gini on the log1p scale halves the noise (null SD 0.03 to 0.04) but departs from MET-3.
3. **P4, LEAK-10 (partly refuted, number only): "no field moves by more than 0.045".** This holds over calendar years. Over the years before a lapse, three fields move by 0.066 to 0.070 without a trend, in bins with 95 to 350 positives. *Changes:* nothing to the keep decision. *Remedy:* say "by more than 0.045 by year, and 0.07 at most, without a trend, by years before lapse".
4. **P3, USE-1 (wording): "assuming they renew".** Sec. 3.5 argues that the premium should include the renewal probability. *Remedy:* "The model paper prices the next period's home premium for such customers (Sec. 3.5, Table 8)".
5. **P5, PROV-13 (untested): Client_Seniority ≥ 5 as "the sample's selection".** A reading at the end of the observation window (2015) gives the same floor of 5.0 in every lapse cohort. *Changes:* the builder's description of the test book ("survivors of a book with at least 5 years' seniority") and the note. Leakage is unaffected (the value is constant per customer). *Remedy:* name both readings in the anomaly bullet.
6. **Record (stale):** the screening's "Proposed fallback `rmse`" contradicts the declared Gini. *Remedy:* the curator's CC line settles the metric, as in australian_vehicle_insurance_2004_2005.
7. **Untested, low rank:** whether the zero-cost claims are closed without payment or not yet costed (the flat share by year argues for closed), and whether lapse years are full (the claim share on lapse rows is higher, not lower). Neither can be settled from the release; the notes already say so.

</details>

<details><summary>Column audit</summary>

**Column audit: spanish_homeowners_motor_insurance_2010_2014 (AI, column-auditor, 2026-11-02)**

**Verdict:** no leak in the shipped columns. The same-year outcomes (`NClaims2`, `Types`, `NClaims1`, `Claims1`, `Retention`) are dropped, and the added history is built correctly from earlier rows only. I checked it independently with a merge on (PolID, year+1): `prev_home_claims` sums to 2,616 and `prev_home_claim_cost` to 582,693.7 both ways, and `past_home_claims` to 5,377 both ways. Two points for the curator, neither a column leak: (1) a measured hint that lapse-year targets are partial years, which is a question about what the target means (P3); (2) `metro_code` labels whose shares look odd. The rest are P7 notes, and on one of them I disagree with the builder's wording: the low `Car_power_M` values can be real microcars.

Prediction point (first `curation_comments` bullet): the customer's yearly renewal, with both policies in force. Known then: the rating fields and the claims of the earlier years. Not known: the year's claims and the end-of-year renewal.

Frame checked: rebuilt from the definition through `dataset_io.load(..., built=False)`, 122,935 x 21 (20 inputs, of which `policy_year` is the time column, plus the target). No scoring columns. Raw file: the release's `data_ex.csv`. Scripts: `{a,b,c}.py` (run folder).

**Column table**

| column | meaning (source) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `gender` | 1 male, 0 female (DiB Sec. 1; ESWA Table 4) | yes; one value per customer | category male/female (78/22%) | fine | CLEAN-12, CLEAN-14 |
| `Age_client` | customer's age in years | yes, read once at an unstated date (does not grow) | int, 18-95 | fine, with the builder's frozen-field note | LEAK-10 later-pull clause (kept) |
| `age_of_car_M` | "years since the vehicle was bought by the customer" | yes (frozen) | int 0-68; 0 for 20% of customers; for 161 customers it exceeds age minus 18 | cleaning note: the 0s are a possible proxy-missing code (builder's note stands). The values above age minus 18 suggest the field is the car's age, not the time since the customer bought it. | CLEAN-10, CLEAN-11 (keep, note) |
| `Car_power_M` | power of the car (unit unstated, probably hp) | yes (frozen) | float 4-560; 57 customers below 20, 20 of them at 5.4 | fine. Not impossible: Spanish licence-free microcars (quadricycles) run at about 5-8 kW, so "implausible" in the comment is too strong. | CLEAN-11 (values only unusual stay) |
| `Car_2ndDriver_M` | 1 if an occasional second driver is declared | yes (frozen) | category no/yes | fine | CLEAN-14 |
| `num_policiesC` | "total number of policies held by the customer" | yes (frozen) | int 0/1 (19/81%), kept numeric as a count | fine for the dtype (CLEAN-14: a count stays numeric). Its meaning is unknown because every customer holds at least 2 policies; it is not tied to lapse (2010 lapse AUC 0.512). | CLEAN-14; PROV-13 note |
| `metro_code` | 1 urban or metropolitan, 0 rural | yes (frozen) | category; "rural" 84% of rows | question: 84% "rural" is odd for a Spanish bundle book. Apartments make up 62% of the "rural" customers against 69% of the "urban" ones (customer level), so the code barely separates settings. The labels follow both papers and cannot be inferred otherwise; keep them, but add a note on the share. | CLEAN-12; PROV-13 |
| `Policy_PaymentMethodA` | 1 annual, 0 monthly (motor) | yes (frozen) | category | fine. 0 may also cover other frequencies; the source gives only these two labels. | CLEAN-12 |
| `Policy_PaymentMethodH` | 1 annual, 0 monthly (home) | yes (frozen) | category | fine | CLEAN-12 |
| `Insuredcapital_content_re` | insured value of the contents | yes (frozen) | float 2.4-14.4, on a log scale (inferred) | fine, kept as recorded with the note. The source scaled it per customer, not over all rows, so LEAK-30 does not apply. | CLEAN-21 note |
| `Insuredcapital_continent_re` | insured value of the building | yes (frozen) | float 5.7-15.4, on a log scale (inferred) | fine, as above | CLEAN-21 note |
| `appartment` | 1 apartment, 0 house or semi-attached (ESWA Table 4) | yes (frozen) | category | fine; the strongest single field (AUC 0.63-0.65 in every year) | CLEAN-14 |
| `Client_Seniority` | years with the company | yes (frozen; at least 5.0 for everyone) | float 5.0-44.7 | fine. It does not encode the lapse time: the median is 7.9-8.1 and the minimum 5.0 for customers seen 1 to 5 years; AUC 0.52 for staying all 5 years; 2010 lapse AUC 0.48. That fits one common read date, so it is not the tenure up to each customer's lapse. | LEAK-10 later-pull clause (kept) |
| `prev_home_claims` | added: last year's home claim count (`NClaims2` lagged 1) | yes; final, not as of the renewal (noted) | float, NaN in 2010 | fine; verified | LEAK-34, USE-10, CLEAN-19 |
| `prev_home_claim_cost` | added: last year's home cost (`Claims2` lagged 1) | yes, with the development caveat | float euros, NaN in 2010 | fine; verified | LEAK-34, CLEAN-19 |
| `prev_motor_claims` | added: last year's at-fault motor count | yes (same caveat) | float, NaN in 2010 | fine | LEAK-34 |
| `prev_motor_claim_cost` | added: last year's motor cost | yes (same caveat) | float, NaN in 2010 | fine | LEAK-34 |
| `past_home_claims` | added: home claim count of all earlier years in the release | yes | float, NaN in 2010; equals `prev_home_claims` in 2011 | fine; verified | LEAK-34, CLEAN-19 |
| `past_motor_claims` | added: motor claim count of all earlier years | yes | float, NaN in 2010 | fine | LEAK-34 |
| `policy_year` | `year` 1-5 mapped to 2010-2014 (DiB Table 1) | yes | int; time column and feature | fine. Calendar year or policy year is unstated (noted). ESWA uses Year as a covariate. | CLEAN-3 (a time index kept in its meaning) |
| `log1p_home_claim_cost` (target) | log1p(`Claims2`), the year's home claim cost in euros | outcome | float; 98.2% zeros | question on lapse-year exposure (problem 1) | USE-5, USE-8 |
| dropped: `NClaims2`, `Types`, `NClaims1`, `Claims1`, `Retention` | the year's own outcomes | no | removed | correct. `Types` is coded on costs above 0, not on counts (0 rows with `Types`=1 and a positive cost), so it is a direct encoding of the target. | LEAK-10, LEAK-2 |
| dropped: `PolID`, `Unnamed: 0`, `year` | customer id, row number, raw year | n/a | removed (`year` turned into `policy_year`) | correct | LEAK-33, CLEAN-3 |

Missingness: only the history columns have missing values, and exactly the 40,284 rows of 2010. That is caused by the year, not the outcome. No feature is an exact copy of another (CLEAN-5).

**Problems, ranked (principles.md)**

1. **P3 (USE-5, USE-8), question for the curator: lapse-year targets may be partial years.** The home-claim share of each customer's lapse year is about a quarter below that of their renewed years in every year: 1.51% against 2.01% (2010), 1.64/2.23, 1.77/2.69, 1.75/2.07, 1.73/2.18 (`c.py`). ESWA Table 3 counts "customers that cancel at least one policy per period", so a lapse falls within the period. Its footnote 1 and Sec. 4 say claims push towards lapsing, which would raise the share, not lower it. A lower share fits a lapse year with exposure cut short. This is not a leak: at the renewal the insurer does not know who will lapse, and the cost until the lapse is what it bears. But it is the "whether a lapse year is a full year" caveat in `fit_reason`, now with a measured sign. The 2014 test window holds 2,296 lapse rows out of 13,284. Mildest remedy: add the numbers to the existing note and keep fit approximate. Do not drop the lapse rows: that would select on a future outcome (USE-5).
2. **P5/P7 (PROV-13, CLEAN-12), question: `metro_code` shares.** 84% of rows are "rural". Apartments make up 62% of rural against 69% of urban customers. The labels follow DiB Sec. 1 and ESWA Table 4, so they cannot be reversed without evidence. Remedy: a one-line anomaly note giving the share. Leave the labels as they are.
3. **P7 (CLEAN-11), wording: `Car_power_M` 4-17.** These are unusual but possible (licence-free microcars; the 5.4 value is shared by 20 customers). The comment calls them "implausible". Remedy: say "unusual (microcar range)", or drop that sentence. Keep the values.
4. **P7 (CLEAN-10/CLEAN-11), note: `age_of_car_M`.** I agree with the builder on the 0s (20% of customers; the code cannot be inferred; keep with the note). A new fact for the note: for 161 customers the value exceeds age minus 18. So the field probably counts the car's age, not the years since this customer bought it. Remedy: add one clause to the existing anomaly bullet.
5. **P7, fine as noted:** `num_policiesC` (0/1 for a "total number of policies"; numeric is right under CLEAN-14), the insured values on an inferred log scale, `Client_Seniority` above age minus 18 for 76 customers. No change.

Claims checked and confirmed: the 13 rating fields are constant per customer (the asserts pass); 98.2% zeros; the yearly row counts; the history is built from earlier rows only; `Types` and `Retention` are outcomes; `Types` 1 holds 1,715 rows with a home claim count but no home cost (1,696 + 19 in the crosstab), and `Types` 2 another 27: 1,742 in all, as stated. LEAK-10 later-pull clause for the frozen fields: I add evidence that `Client_Seniority` does not move with the lapse year (problem table above), which supports keeping them with the note.

</details>

<details><summary>Split audit</summary>

**Split auditor: spanish_homeowners_motor_insurance_2010_2014 (AI, 2026-11-02)**

**Verdict: right with notes.** The temporal regime fits the use case: a known customer's yearly renewal, priced by a model refit on the years already seen (SPLIT-1, SPLIT-6, SPLIT-13, USE-10). The split is a true temporal split, not a forced one. The SPLIT-8 leak test (amended 2026-11-02) does not apply, and the wisconsin mechanism, where training rows of the test year carry that year's claim level, cannot happen here: every test year sits wholly on the test side. The no-gap exception to SPLIT-10 holds on the same facts as pricing_game_2016_french_fleet. The splits_comment backs it with the wrong experiment, though, and should carry the late-claim simulation instead.

Script: `sim.py` (run folder), which loads through `dataset_io.from_definition`. Model: untuned LightGBM on log1p (300 trees, 15 leaves), scored by normalized Gini on the amount, threads capped.

**What I checked, with numbers**

* Windows (verified on the definition's split plan). Test 2014: train 2010-2013, 109,651 rows (89.2%), 13,284 test rows, 240 positives. Test 2013: train 2010-2012, 92,607 (75.3%), 17,044 test rows, 310 positives. Test 2012: train 2010-2011, 70,102 (57.0%), 22,505 test rows, 448 positives. In every window the last training year comes before the test year. SPLIT-11 (expanding train side) and SPLIT-14 (3 windows, every train side at or above 50%) hold. The windows are whole years, so no window is cut to a season (SPLIT-20). The one-year horizon is the renewal cycle (SPLIT-12). The splits_comment numbers match.
* Regime. All test customers are known: every customer starts in 2010 and the years are consecutive, so the same customers' earlier years are in training. This matches the renewal use case. The hidden-group probe finds that 91% of test rows equal a training row on every column except the year. That is the same customer, mostly claim-free, one year earlier: known-entity history (USE-10, LEAK-34), not a copy across the split. The leak probes' 1-NN finds no signal. A grouped split (new customers) would test new-business pricing. That is not this use case, and the release has no new customer after 2010, so I did not fit it as an alternative.
* Leak across the split (the curator's wisconsin concern). A year-level leak would need rows of the test year in training. There are none. The only cross-year link is the customer's own earlier claims, which a renewal knows.

**Problems, ranked**

1. **P4, SPLIT-9 / SPLIT-10 (Should, exception): no gap, and the splits_comment simulates the wrong delay.** Training for year t includes year t-1, whose claims the refit only partly knows. The test rows' `prev_home_*` inputs are year t-1 claims as finally recorded. How large the delay is depends on what `year` means, and the sources do not say (curation_comments).
   * Calendar years: the delay is the reporting and pricing lag, a few weeks. I simulated it as the pricing_game precedent did. In the newest training year, a home claim's cost is set to 0 with probability 30/365 or 90/365, and the test rows' previous-year home claim is hidden with the same probability (3 repeats). Mean Gini over the 3 windows: 0.219 without the simulation, 0.226 with 30 days, 0.203 with 90 days. By window (2014 / 2013 / 2012): 0.161 / 0.315 / 0.182 base, 0.181 / 0.298 / 0.199 at 30 days, 0.152 / 0.263 / 0.195 at 90 days. All of this is inside one window's bootstrap SE (0.06 to 0.11).
   * Policy years from each customer's renewal date: the newest training year can overlap the test year by up to a year. Then the builder's run that drops the newest training year is the right bound: 2013 falls from 0.317 to 0.244, 2014 moves from 0.133 to 0.145.
   * What the gap would cost: a one-year gap, the smallest the yearly time column allows, leaves 2012 a 33% train side, so only two windows meet SPLIT-14. The exception serves SPLIT-14, as for pricing_game_2016_french_fleet (Andrej, 2026-11-02).
   * Mildest remedy: keep gap 0 and accept the exception. Rewrite the splits_comment: name the two readings of `year`, give the 30- and 90-day simulation (0.226 and 0.203 against 0.219) as the bound for calendar years, and give the dropped-year run as the bound for policy years. The current wording calls a fall of 0.073 at 2013 "inside one window's noise". That is about one SE, so say "about one standard error". The builder's `exp_gap.py` also omits `past_home_claims` and `past_motor_claims` and keeps the raw year number. Its numbers differ a little from the shipped features (my 2014 base is 0.161 against its 0.133). Rerun it on the shipped frame before quoting it.
2. **P3/P4, USE-8 and SPLIT-13 (approximate fit, a note): the closed 2010 cohort.**
   * The test years hold only the customers who renewed both policies every year since 2010. Customers with a home claim lapse more often: 30.7% of claim years end in a lapse, against 24.5% of claim-free years (2010-2013). The test book therefore drifts toward claim-free survivors, and no new customer ever enters. That is a renewal book, but an aging, closed one. The score stands for renewal pricing of a long-standing book, not a book with new entrants. fit="approximate" and the curation_comments already say this. Add one line with the lapse numbers to the fit reason or the comments; nothing to re-split.
   * The 2010 rows carry no history (all `prev_*` and `past_*` missing). They are 57% of the 2012 window's training side and 37% of the 2014 window's. Training without 2010 moves the mean Gini from 0.219 to 0.209 (2014: 0.164, 2013: 0.283, 2012: 0.179). That is information only: SPLIT-21 forbids choosing the history from a few windows, and SPLIT-11 keeps everything before the window. Keep.
   * `past_home_claims` counts over a span that grows with the year: its mean is 0.029 in 2011, 0.060 in 2012, 0.091 in 2013 and 0.121 in 2014. So each test year's counts cover one more year than any training row's. The split causes this drift and cannot remove it. The mildest remedy is a P7 feature change: a per-year rate, or a count capped at the previous 1-2 years. Otherwise keep it with a note in curation_comments.
3. **P6, TP-9 / SPLIT-14: noisy windows.** There are 240 to 448 positives per window, and the bootstrap SE is 0.06 to 0.11 per window. The per-window Gini moves by up to 0.15 between windows, from 0.16 at 2014 to 0.32 at 2013. That is not a split flaw: no wider window can exist with 5 years. State in splits_comment that comparisons should use the mean over the 3 windows.

**Claims checked**

* Confirmed: train shares 89% / 75% / 57%; test rows and positives per window; no new customers; 91% of test rows match a training row of the same customer.
* Corrected: the gap claim. The drop-a-year run is the bound only under the policy-year reading. Under the calendar-year reading the relevant number is the 30/90-day simulation, which the builder did not run.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner (AI, 2026-11-02): a Spanish insurer's pricing actuary setting the home premium of a bundled home+motor customer at renewal**

**Verdict.** Fit **approximate**, as declared (USE-8): the rows are real yearly renewals of one insurer's bundle customers and the target is the home loss cost I price, but the rating fields are one frozen reading per customer, the file has none of the policy terms I always price with (premium, cover, deductible, exposure), and the book is a closed 2010 cohort. The metric scores my decision **partly**: the normalized Gini scores the risk ranking that sets my relativities, at the unit I act on, but not the premium level. I would keep it (reasons below). Ship after the curator's calls; nothing I found changes the task enough to reject it (USE-12).

**1. The inputs at the moment I price the renewal**

* I have them: age, gender and years with us; the car's age, power and second driver; urban or rural; payment method of each policy; insured values of contents and building; apartment or house; the customer's earlier home and motor claims (USE-6, USE-10). The added claim history is what I use at renewal. The model paper's footnote 1 says the insurer gives a rebate to a customer with no claims in the year before renewal.
* I would have them, but not exactly as they ship:
  * *Previous year's claims.* In Spain the insurer must give notice of non-renewal at least two months before the term ends (Ley 50/1980 art. 22), so I set the renewal price one to two months early. The last weeks' claims and the costs still developing are not in my data then. The shipped `prev_*` columns are the final figures. I measured what this can be worth: LightGBM on log1p gives a mean Gini of 0.205 on the rating fields only and 0.232 with the history added (windows 2012/13/14: 0.198/0.299/0.118 against 0.212/0.329/0.157). The history is worth about 0.03 Gini, and the part that comes from late claims is a fraction of that. The SPLIT-10 exception is acceptable: it matches pricing_game_2016_french_fleet.
  * *Frozen rating fields.* I always have the customer's current age, and here `Age_client` never moves. The error is a few years of age on a weak rating factor. The builder's AUC-by-year table shows no field drifting with claims. Kept under LEAK-10. I agree it is a gap in the fit and not a leak.
* Missing, though I would always have them:
  1. **The current premium and the tariff it came from.** This matters most. At renewal I reprice an existing premium: I change the current tariff, I do not price from scratch. Without the premium the task cannot be "improve on the current price", which is how Frees, Meyers and Cummings (2011) define the ordered Lorenz Gini.
  2. **Cover, deductible and sum-insured options.** The insured values ship, but the peril cover and the deductible do not.
  3. **Exposure.** Policy start and end dates, and whether a lapse year is a full year. The data article says "dates of renewal" were combined, but the file has no date column. A rough check: lapse-year rows have a *higher* home claim share than renewed rows (2.2% vs 1.6%, years 1-4). That fits claims driving lapse (model paper, Sec. 3.3) and gives no sign of heavily truncated last years, but it does not prove full exposure.
  4. **Better location and building details.** A postcode or risk zone instead of urban/rural, plus construction year, floor area and security devices.
  5. **Claim history before 2010.** Every customer has at least 5 years' seniority, but 2010 rows ship with no history.

**2. The target**

The target, the home claim cost of the coming year in euros, is the pure premium I act on: the expected cost, with the 98.2% claim-free years included. I want a number (an expected cost), not a class. The hurdle check shows that only the claim part can be learned: claim AUC 0.68-0.69, while severity has R^2 below 0 on claimants. In practice that makes the model a frequency model with a flat severity, which is how home tariffs often look for a small book. Shipping log1p is a modelling choice and the score is on the amount (MET-3). One caveat: a model fit on log1p and back-transformed predicts something closer to a median than a mean, so its *level* is not a premium. The Gini does not see this.

**3. Rows and test data**

One row is one customer-year, which is one renewal decision for one customer, so the unit matches. The test year (renewals of known customers, trained on all earlier years) is what I face next year for my in-force renewal book (USE-10). It does not cover new business. The book is closed, so customers in the later test years have survived 2-4 renewals. That is still my renewal book, only older and more loyal than a real one with new customers coming in (USE-5 holds: lapsers keep all their years). The test years are small: 448 / 310 / 240 claimants, with a bootstrap SE of 0.06-0.11 per window. I would not trust a model ranking on one year. The mean over three windows is the minimum.

**4. Would I use it?**

I would use it as a segmentation tool next to my GLM tariff, not as the tariff. I would trust it if it beat the one-variable tariff (apartment or house alone, Gini 0.177) in every window, and the builder shows every family does. Things that would make me distrust it:
* the frozen ages;
* no premium or exposure, so it cannot be tested against my current price or turned into a rate per policy-year;
* a book of 2010 survivors;
* a window noise of about ±0.1 Gini, which can hide the difference between two decent models.

**5. The metric (MET-1, MET-6 to MET-9)**

`normalized_gini` on the amount, every row weighted 1, from context. **Partly.**

* For it:
  * Gini and lift are how pricing teams compare loss-cost models. Frees et al. 2011 and Frees et al. 2014 (Frees is an author of this release) use the ordered Lorenz Gini.
  * Property loss-cost competitions scored it: Liberty Mutual's Fire Peril Loss Cost on Kaggle (2014) used a weighted normalized Gini on a loss cost with almost all zeros. That is a closer analogue to home cover than the motor precedents.
  * The Gini scores the ranking that differentiates my premiums, at the customer-year I act on.
  * It does not depend on a threshold or a k, and none exists here (MET-6, MET-7 do not apply).
  * RMSE on the amount is driven by the 20 largest claims of each year (83-94% of the sum of squares), so it would pick models by noise.
* What it misses:
  * The premium level and calibration. My base rate is a separate step (the off-balance), which is why "partly" and not "no".
  * Exposure weighting. The Fire Peril Gini was weighted; nothing here can serve as the weight.
* The metric I would consider instead is the mean **Tweedie deviance** on the amount (power about 1.5), the scoring function consistent for the mean that I would fit a pure-premium GLM by. It scores level and ranking together and is less dominated by the largest claims than squared error. I would still not declare it here:
  * with 240-448 claimants and severity that cannot be learned, it is close to squared error on a few large claims;
  * on a log1p-shipped target it would penalise the back-transform bias of every log-scale model, not the risk ranking.
  * So the Gini stays. MET-10's diversity tie-break would point to Tweedie deviance only if the curator wants one insurance table in the family scored on level.
* MET-11 origin "context" is right: neither paper scores held-out predictions. The reason text should say "Kaggle (Allstate 2011; Liberty Mutual Fire Peril 2014)" if the curator wants the property precedent.

**Gaps ranked by how much they change the task**

1. No current premium or tariff: the task is "rank renewal risk" and not "improve the current price" (USE-8; it limits MET-1).
2. Rating fields frozen at an unknown date (`Age_client` constant): a known-wrong input I would always have correct (USE-3/LEAK-10, kept).
3. No exposure or dates; lapse-year exposure unknown (USE-5). The claim share in lapse years gives no sign of truncation.
4. Closed 2010 cohort with at least 5 years' seniority: the test book is all survivors, and there is no new business (USE-8).
5. Previous-year claims as final figures, not as known one to two months before renewal: worth at most part of the 0.03 Gini the history adds (SPLIT-10 exception).
6. No cover or deductible, and a coarse location (urban/rural): weaker inputs than any real home tariff has. This lowers the ceiling but does not change the task.

**What an expert would change**

* Ask the authors (Guillen, Bolancé) for the read date of the rating fields and the renewal dates the data article mentions. Dates would give exposure and a cutoff for claims known at quote time.
* State in `fit_reason` that there is no current premium, so the task ranks risk rather than repricing (the text already says "no premium"; this is wording only).
* Optionally, compute the history features from claims "known by month 10" if dates ever ship. Without dates, keep the exception.
* Keep log1p plus Gini. Optionally name Liberty Mutual Fire Peril as the property-line precedent for the Gini.

**Sources**

* Guillen, Bolancé, Frees, Valdez (2021), Data in Brief 39:107639 (run folder `papers/dib.txt`: Specifications Table, Sec. 1).
* Frees, Bolancé, Guillen, Valdez (2021), ESWA 185:115552 (`papers/eswa.txt`: footnote 1, Sec. 3.3, Sec. 3.5, Tables 4-8).
* Ley 50/1980 de Contrato de Seguro, art. 22: [congreso.es](https://www.congreso.es/constitucion/ficheros/leyes_espa/l_050_1980.pdf), [BOE 1980](https://boe.es/boe/dias/1980/10/17/pdfs/A23126-23133.pdf).
* Liberty Mutual Fire Peril Loss Cost (weighted Gini), secondary sources only: [CAS RPM 2015 handout](https://casact.org/sites/default/files/presentation/rpm_2015_handouts_paper_3897_handout_2469_0.pdf), [NYC Data Science case study](https://nycdatascience.com/blog/student-works/property-casualty-loss-cost-data-type-case-study).
* Frees, Meyers, Cummings (2011), JASA 106:1085-1098, as cited in the dataset.

**My probes**

All in the run folder:
* `hist.py`: history ablation, LightGBM on log1p, 3 shipped windows.
* `lapse.py`: claim share by renewal outcome.

</details>

<details><summary>Blind review</summary>

**Verdict: include with changes.** The data is real and the prediction makes sense (a renewal pure premium for home insurance). As prepared, though, the RMSE on log1p(cost) is about 98% noise from zero rows, and every row carries covariates frozen in 2010. I would reframe the target or metric before using it.

**Task.** The source is Guillen, Bolancé, Frees and Valdez, "Case study data for joint modeling of insurance claims and lapsation" (Data in Brief 39, 107639; Mendeley DOI 10.17632/vfchtm5y7j.1, CC BY 4.0). It covers 40,284 Spanish customers who held both a motor and a home policy with the same insurer, followed from 2010 to 2014, for a total of 122,935 rows. In the prepared task, each customer-year predicts log1p of that year's homeowners claim cost (Claims2). The features are the customer and policy covariates, plus lagged home and motor claim counts and costs built from the customer's earlier years. An insurer would make this prediction at renewal to price or tier the home policy. The use is real.

Concerns, from most to least serious:

1. **The target and metric give a scoring signal that is barely above noise.** 98.2% of targets are 0. Among the 2,189 positive rows, the median claim is 169 EUR and the maximum is 27,280 EUR. On the expanding-window splits (test years 2012, 2013 and 2014), LightGBM beats the train-mean constant by an R² of only 0.0056, 0.0053 and 0.0062 (RMSE 0.7258 against 0.7280 in 2014). Ridge regression scores 0.7251 in 2014, against 0.7258 for LightGBM. In a paired bootstrap, the SD of the RMSE difference between the two is 0.0008, about the size of the gap itself. The 1% of test rows with the largest squared error carry 69% of the SSE. The ranking signal is real (AUC of the predictions for claim > 0 is 0.67 to 0.70), but RMSE on log1p cost will hardly separate methods. RMSE on log1p cost is also not an actuarial loss. **Change:** pick one of these.
   - Model claim occurrence (home claim > 0) as binary classification with AUC or log-loss.
   - Keep the raw cost and score it with Poisson or Tweedie deviance.
   - Pool all five years and benchmark claim count with Poisson deviance.

2. **Covariates are frozen at the 2010 snapshot, and customers repeat across years.** I linked rows on (gender, Client_Seniority, appartment, Insuredcapital_continent_re). This gives 40,268 groups, close to the 40,284 PolIDs, and the lagged cost matched the previous year's target in 100% of 82,628 linked rows. Within a customer, Age_client changes in only 0.1% of groups. age_of_car_M, Car_power_M, insured capitals, num_policiesC, metro_code and payment method never change. Client_Seniority has the same quantiles in every year (min 5.00, median about 8.05, max 44.71). So "age" and "seniority" in 2014 are really 2010 values. This is not leakage, since 2010 values are known later. But the covariates are mislabelled for later years, and Age_client and Client_Seniority could be shifted by (policy_year − 2010). Every test customer also appears in training with the same fingerprint. The temporal split makes this a legitimate "known customer, next year" setting, not a copy leak. Still, the group structure is unrecorded. **Change:** keep PolID as a group column for evaluation, or document the repeat. Optionally age the time-varying covariates.

3. **The lag features and the split are mostly sound, but some points need documenting.**
   - The prev_* and past_* columns are NaN for all 40,284 rows of 2010 and only for those rows. This is structural, since there is no history before 2010.
   - past_* includes the previous year and is never below prev_*. Same-year motor claims are correctly excluded.
   - In practice, renewal quotes are issued before the prior year has fully run off, so a complete year-(t−1) cost is slightly optimistic. This is minor.
   - The source says that "only at-fault claims are included for motor insurance". For home, it gives no comparable definition of which claims are included.
   - There are 1,126 rows with prev_home_claims > 0 but zero cost. These are claims with a count but no cost (possibly reported or rejected claims). They are plausible, but worth a note.

4. **Sample selection and survivorship.** Rows fall from 40,284 to 13,284 by 2014 because of non-renewal. The source calls the dataset one for "joint modeling of insurance claims and lapsation". Later test years contain only customers who stayed, and all customers have seniority of at least 5 years. The test windows therefore reflect retained long-tenure customers, not new business. This is acceptable for a renewal task but should be stated. The Retention column was correctly dropped, since it would be future information.

5. **Preparation details (fine).** Binary codes were decoded to readable categories. Insuredcapital_*_re look like log euros (exp gives a mean contents value of about 39.5k EUR), and the documentation should say so. No duplicates, no missing values beyond the structural 2010 NaNs, and no implausible values. Car_power_M ranges from 4 to 560 and age_of_car_M reaches 68; both are odd at the extremes but rare. policy_year is kept as a feature, which is harmless under a temporal split.

**Could not check:**
- I could not read the article's full text: PMC showed a captcha, ScienceDirect returned 403, and the UB repository returned 404. So I could not confirm what "_re" means, the exact home-claim definition, or whether costs are net of deductibles.
- The raw Mendeley file was not compared row by row. The NClaims1/NClaims2 documentation ambiguity reported on the Mendeley page could not be resolved.
- Customer linkage was inferred from a fingerprint, not from PolID.

</details>

<details><summary>Precedent check</summary>

**Precedent checker (AI, 2026-11-02): spanish_homeowners_motor_insurance_2010_2014**

**Verdict:** most of the definition's choices follow precedent, or depart for a reason they state. There are two real
departures without a stated reason, and both need a curator call:

1. The metric is argued as "the family's convention". The curator dropped family calls on the metric on 2026-11-02
   (MET-10 amended).
2. The two payment-method fields are kept, while the sibling `spanish_motor_insurance_2015_2018` drops its
   "Last payment method" for the same mechanism.

The no-gap split is an exception with a stated reason. It matches `pricing_game_2016_french_fleet` (Andrej,
2026-11-02) and the curator's decline of the SPLIT-10 amendment. Its note should add one fact: whether `year` is a
policy year.

Sources read: `principles.md` (Consistent judgement, Exceptions and amendments, Tensions); `splits.md`, `metrics.md`,
`leak_checks.md` and `cleaning_features.md` (rules and Cases); the six sibling definitions, their `REVIEW.md` files
and their records' CC lines; `curation/records/avito_demand_prediction.md`; the builder report and its probes. One
measurement of my own is described under decision 3 (script in `pay.py` (run folder)).

A note on how much weight the sibling decisions carry. Of the six siblings named in the brief, only these are curator
decisions:
* `pricing_game_2016_french_fleet`: split, gap, target and metric (Andrej, 2026-11-02).
* The forced splits of frempl, the 2022-2024 Spanish table and australian (SPLIT-8 amended, Andrej, 2026-11-02).
* The exposure (LEAK-10) and target-scale calls (Andrej, 2026-11-02).

Everything else in `spanish_motor_insurance_2015_2018`, wisconsin and the context-Gini declarations is an AI draft that
is still open. That includes australian issue 4, "Confirm the normalized Gini ... for the four", which has no answer
yet. Matching an AI draft is not following a precedent.

**1. Target shipped as log1p, scored on the amount (`target_transform="log1p"`)**

Consistent with the curator's own call on the scale. On 2026-11-02 Andrej decided "the target scale as each file
implements it: this table ships the claim cost in dollars, the log1p tables keep log1p"
(`curation/records/australian_vehicle_insurance_2004_2005.md`, issue 5). The choice also follows CLEAN-16's default
and MET-3 (scored on the amount). It is backed by this table's own numbers: LightGBM's Gini is 0.219 fit on log1p and
0.213 with a Tweedie loss, and R^2 on the amount is -0.003 against -0.041.

Wording to fix: "log1p keeps the family's convention" (`curation_comments`, the MET-3 bullet). The scale is a
per-dataset call. The family is split: australian, pricing_game_2016 and wisconsin ship the raw amount; frempl and the
two Spanish motor tables ship log1p. Suggested text: "log1p, the scale CLEAN-16 defaults to and the one the scale test
here does not change", with no appeal to the family.

**2. Normalized Gini from context (`Metric.from_context`); RMSE rejected**

The outcome is defensible on this table's own numbers: the 20 largest claims hold 83-94% of each test year's sum of
squares, and every model scores R^2 between -0.07 and 0.00 on the amount. The reasoning, however, departs from the
curator's newest decision.

The comparison case is MET-10 as amended (Andrej, 2026-11-02, Cases row "no family call on the metric: each table's
metric is decided on its own, and in doubt for diversity"). It came from `pricing_game_2016_french_fleet` issue 4 and
was applied the same day to frempl issue 4 and `spanish_motor_insurance_coverage_level_2022_2024` issue 3 ("not
matched to frempl").

The builder's issue 5 asks "Decision: confirm (family consistency)". The `task_metric` reason lists the four siblings
as "the same choice and scale". What the amended rule asks for is different:
* the call made on this table's evidence alone;
* the question of whether the call is in doubt;
* if it is, the diversity factor.

Diversity matters here. This would be the 9th normalized Gini in the working copy (allstate_1m, australian, frempl,
loan_default, pricing_game_2016, pricing_game_2017, and the two Spanish motor tables). Only one dataset scores a
deviance (`nantucket_sound_sea_duck_aerial_survey_counts`, `mean_poisson_deviance`). `pricing_game_2017_french_mtpl`
issue 2 (open) measured a Tweedie deviance following the game's profit better than the Gini across a mixed field
(Kendall tau 0.58-0.79 against 0.12-0.59).

The builder did not weigh a deviance against the Gini here. It compared only against RMSE. The context Gini on a
regression target is also not yet confirmed by any curator (australian issue 4 is open), so "same as the four
siblings" rests on AI drafts.

```text
**Consistency check (AI, 2026-11-02):** the draft confirms the normalized Gini for
spanish_homeowners_motor_insurance_2010_2014 as "family consistency" (issue 5), while you decided on 2026-11-02
(MET-10 amended, from pricing_game_2016_french_fleet) that no metric is a family call and that diversity wins when in
doubt. What decides this table's metric?
(a) Its own evidence, not in doubt: RMSE follows 20 claims (83-94% of the squares) and every model scores R^2 <= 0, while
the Gini separates every model family from a constant in every window; the reason and issue 5 are reworded to drop
the family, and the Gini stays.
(b) In doubt, so diversity: measure the mean Tweedie deviance on the amount (pricing_game_2017_french_mtpl issue 2)
on the 3 windows and declare it if it orders the models sensibly.
(c) Reopen the four sibling tables to settle the context Gini together (australian issue 4).
(d) Amend MET-10 back to a family call for the insurance tables.
```

**3. Rating fields kept although recorded once (LEAK-10, later-pull clause)**

Mostly consistent. The clause says late values stay "with a note only when the part that can be traced shows none",
and it is decided case by case by the curator (Lennart, 2026-10-26). The precedents that match are:
* `onlinenewspopularity`: kept on a traced test.
* `spanish_motor_insurance_2015_2018`'s `Value_vehicle`: kept, because the residual after the vehicle's attributes
  ranks claims at ROC AUC 0.497. This is an AI draft; its issue 3 is open.

Here the test is that each field's ROC AUC for a home claim stays flat across 2010-2014 and across the years before a
lapse. The builder rightly lists it as draft issue 1 for the curator.

There is one real pair decided the other way. `spanish_motor_insurance_2015_2018` drops `Payment` ("Last payment
method of the reference policy", one value per policy; AI draft, its consistency check 3 of 2026-11-01). Its reason:
"it shows a pattern that cannot be traced: ... 40% of the first years with a claim are paid half-yearly, against 26%".
"Removing it changes no score" is no reason to keep it (zillow_prize, melbourne_housing_market, Lennart, 2026-10-21).

This table keeps `Policy_PaymentMethodA` and `Policy_PaymentMethodH`, frozen the same way. They show the same kind of
raw pattern. I measured it on `data_ex.csv`:
* Motor policy paid annually: 75.0% of customer-years without a home claim and 68.0% with one in 2010. The gap is 7.0,
  7.3, 3.7, 3.3 and 8.7 points over 2010-2014, with no trend.
* The gap is similar in a lapser's last year: 72.6% against 67.6%.

The flatness is what sets the case apart, and the builder states it. But the test cannot rule out a value read at the
end of the panel after a switch in any year: that would also give a flat gap. The facts that really distinguish the
two cases are documentary:
* this release has no "last" wording;
* the Specifications Table selects the sample in 2010;
* in the Spanish table, the "last" wording points to a late read.

That makes this a curator call on the pair.

```text
**Consistency check (AI, 2026-11-02):** the draft keeps Policy_PaymentMethodA/H (one value per customer, read once at an
unstated date) on a flat year-by-year ROC AUC; spanish_motor_insurance_2015_2018 (AI draft, 2026-11-01) drops its
`Payment` (one value per policy, "Last payment method") for an untraceable claim pattern (40% against 26%). Here the
annual-payment share is 7.0 / 7.3 / 3.7 / 3.3 / 8.7 points lower with a home claim, 2010-2014. What sets them apart?
(a) The documentation: no "last" wording here, and the sample was selected and described in 2010, so the read most
likely precedes the claims; the gap does not grow over the years, as a switch after claims would make it.
Recorded as the case's distinguishing fact.
(b) Treat it like the Spanish table: drop both payment fields.
(c) Reopen the Spanish table and keep its `Payment` with a note.
(d) Amend LEAK-10's later-pull clause: a once-read rating attribute whose link to the outcome is flat over the panel
stays with a note.
```

`Age_client` not growing over the years is staleness, not a leak, and `fit_reason` names it. A possible repair, if the
curator accepts the 2010 reading, is the age at each year (`Age_client + policy_year - 2010`). This is an option, not
a precedent finding. The remedy ladder ranks repair above keeping with a note, but the read date is not known.

**4. Lagged prior-year claim features (built by us)**

Consistent with LEAK-34 (Must) and USE-10 under a true temporal split. Precedents:
* `ieee_fraud_detection`'s `uid` (LEAK-34 Cases).
* `basque_offshore_ctd_chlorophyll`'s last survey (this run).
* `wisconsin_local_government_property_insurance_fund`'s `NoClaimCredit`, the source's own two-year lag (kept).

The one sibling with the opposite outcome is `pricing_game_2016_french_fleet` (Andrej, 2026-11-02): previous-year
claims "not added ... it carries nothing here" (ROC AUC 0.667 against 0.668). Its reason is the measured absence of
signal, not the rule. Here the history carries signal: the home claim share is 6.0% against 1.7%. The same reasoning
gives the opposite result on different facts.

`spanish_motor_insurance_2015_2018` kept first years only because of a carry-over of claims between years. Here the
remnant test (2 of 98 consecutive costs repeat) and flat yearly claim shares (1.64-1.99%) show no carry-over. That is
the distinguishing fact, and it is stated.

Precedent also asks for one note. The lags use the finally recorded claims, and the note says so (LEAK-24, as in
`pricing_game_2016_french_fleet`'s delay note). Nothing more is needed.

**5. Same-year outcomes dropped (`NClaims2`, `Types`, `NClaims1`, `Claims1`, `Retention`)**

Consistent with LEAK-10 and the family:
* `spanish_motor_insurance_2015_2018` drops `N_claims_year`, `Lapse` and `Date_lapse`.
* `spanish_motor_insurance_coverage_level_2022_2024` drops the cover-level claims and `policy_status` (+0.007-0.027
  Gini when added back).
* wisconsin drops `Freq`, `lny` and `yAvg`.

The year's motor claims fall in the outcome's period ("falls in the outcome's period, still goes", the LEAK-10 clause
of 2026-10-26). No departure.

**6. Fit `approximate`**

Consistent:
* `spanish_motor_insurance_2015_2018`: true temporal split, approximate (frozen or late fields, no claims history).
* Wisconsin was moved from `direct` to approximate after its precedent check against lending_club.

`pricing_game_2016_french_fleet` ships `direct` (Andrej, 2026-11-02). The facts that set this table apart are named in
`fit_reason`: rating fields frozen at an unstated date, no premium or cover, a closed 2010 cohort, unstated exposure of
lapse years.

**7. Split: yearly expanding windows 2014/2013/2012, no gap (SPLIT-10 exception for SPLIT-14)**

The windows are consistent:
* SPLIT-11 (expanding).
* SPLIT-14: 3 windows training on 57%, 75% and 89%. Each window has its own train side, as SPLIT-14 was amended on
  2026-11-02 (Andrej, pricing_game_2016).
* SPLIT-12 (a yearly renewal, horizon of one year).

Wisconsin's five policy years gave only two windows because its panel is nearly balanced, which is why it was forced
to a grouped split (SPLIT-8, its issue 1 still open). Here attrition shrinks the later years, so 2012 still trains on
57%. That is the distinguishing fact. The true temporal split also avoids wisconsin's measured leak, the year's claim
level shared across the forced folds, because each window is scored within one year. SPLIT-8, including its
2026-11-02 amendment, does not apply: the split is not forced.

The gap is a departure with a stated reason, reasonable under the ranking. It matches
`pricing_game_2016_french_fleet` ("no gap ... an exception to SPLIT-10 that serves SPLIT-14", Andrej, 2026-11-02,
splits.md Cases). It also follows the tension row "Unmatured training labels against the training floor" in
principles.md. That row puts SPLIT-9 (Must) as met when no shortcut can be measured, and the diffuse rest as a SPLIT-10
exception.

On the count of exceptions: this is another no-gap departure for SPLIT-14's floor, after:
* alfa_battle_2_0_task_2 and lending_club (Lennart, 2026-10-21);
* pricing_game_2016 (Andrej, 2026-11-02);
* avito_demand_prediction_1m and wisconsin (proposed).

The amendment came due at the third and was declined: "SPLIT-10 stays as written, and each no-gap departure for
SPLIT-14's floor ... is decided as an exception of its own" (CC 2026-11-02, Andrej,
`curation/records/avito_demand_prediction.md`). No new amendment prompt is due. Draft issue 2 should cite that CC
beside pricing_game_2016.

The closest contrary case is `spanish_motor_insurance_2015_2018` (AI draft, 2026-11-01): a 12-month gap with monthly
windows. That gap exists because contracts start in any month, so a training policy-year can end up to a year after
the window starts. The fact that sets this table apart holds only if `year` is a calendar year shared by all
customers; then only the reporting delay of the last weeks' claims is missing.

The data article says the source held "dates of renewal for the two types of policies" (dib.txt, Sec. 1), and the
builder lists "whether `year` is a calendar or a policy year" as not checkable. If years run from each customer's
renewal date, the delay is up to a year, the same mechanism as the Spanish table. The exception would still hold,
because a one-year gap leaves two windows, but `splits_comment` ("the previous year's claims are not final at a
renewal") would understate it.

Text change suggested in `splits_comment`, with no prompt (the stated reason covers both readings): "if a year runs
from each customer's renewal date, the newest training year can end up to a year into the test year".

The gap simulation is coarser than pricing_game_2016's and moves more: 2013 goes from 0.317 to 0.244, against 0.002
to 0.004 there. Dropping a whole year also removes training data, so that 0.073 is an upper bound, close to one SE
(0.06-0.11). Say "an upper bound" rather than "inside one window's noise".

**8. Builder's draft issues, other points**

* Issue 4, TP-2 keep despite `no_signal` and `drift_baseline` under R^2. Consistent with
  `spanish_motor_insurance_2015_2018` (Gini 0.116, two windows near 0, kept) and wisconsin (kept, R^2 flags read
  through the declared metric).
* Issue 6, `age_of_car_M` = 0 kept. This applies CLEAN-10 ("when the encoding can be inferred"); it is not a
  departure. Two related cases differ in kind:
  * Wisconsin set `NoClaimCredit` = 0 to missing on a structural, exact fact (0 in all 2,292 rows without two
    earlier years).
  * Australian set vehicle value 0 to missing as impossible (CLEAN-11).

  Here a car age of 0 is possible and the evidence is circumstantial (8,050 against 406 at 1, older customers). The
  judgment record's "CLEAN-10 departure kept with a note" should read "CLEAN-10 not triggered (code not inferable),
  kept with a note".
* Issue 7, kept as recorded (`num_policiesC`, log insured values, seniority). Consistent with CLEAN-11 (unusual values
  stay) and frempl's licence-age anomalies.
* Issue 8, warnings:
  * `task_target_value_dominant`: accepted in 9 sibling definitions (frempl, australian, pricing_game_2016 and 2017,
    allstate_1m, liberty, avito_1m, crms, noaa_storm). Consistent.
  * `task_time_on_few_unique`: no definition in the working copy accepts it. Wisconsin's draft did while it was
    temporal (its precedent check, item 15: "No precedent"). This is a first acceptance, so it becomes the precedent;
    the curator's acceptance should be recorded as such.
* Screening CC (Andrej, 2026-11-02): "consistent with spanish_motor_insurance_2015_2018 and wisconsin". The added
  dataset's measured facts supersede the screening on these points: the closed cohort, the frozen fields, and the
  `rmse` fallback replaced. None of these changes the verdict, and none contradicts a curator decision.

**Drift:** none found. Andrej's 2026-11-02 calls are mutually consistent:
* SPLIT-10: an exception where the gap breaks the floor, and the amendment declined.
* SPLIT-14: the window count amended.
* MET-10: per dataset.
* Target scale: per file.
* LEAK-10 exposure: a fix where located, kept where not.

The two findings above are AI drafts lagging the curator's newest rule (MET-10), and two AI drafts disagreeing with
each other (the payment method). Neither is the curator drifting.

**Files**
* Definition: `datasets/_dev/tabarena-v0pt2/spanish_homeowners_motor_insurance_2010_2014/dataset.py`
* Sibling decisions:
  * `datasets/_dev/tabarena-v0pt2/pricing_game_2016_french_fleet/REVIEW.md` (issues 2-4)
  * `datasets/_dev/tabarena-v0pt2/spanish_motor_insurance_2015_2018/REVIEW.md` (issue 3, consistency checks 1-3)
  * `datasets/_dev/tabarena-v0pt2/australian_vehicle_insurance_2004_2005/REVIEW.md` (issues 4-5)
  * `datasets/_dev/tabarena-v0pt2/wisconsin_local_government_property_insurance_fund/REVIEW.md` (issue 1)
  * `datasets/_dev/tabarena-v0pt2/frempl_french_motor_personal_line/REVIEW.md` (issue 4)
* Curator's decision declining the SPLIT-10 amendment: `curation/records/avito_demand_prediction.md` (CC 2026-11-02)
* Rules:
  * `.claude/skills/knowledge-curation/references/metrics.md` (MET-10 and its Cases row)
  * `.claude/skills/knowledge-curation/references/splits.md` (SPLIT-8, SPLIT-10, SPLIT-14, Cases)
  * `.claude/skills/knowledge-curation/references/leak_checks.md` (LEAK-10 clauses, LEAK-34)
* My measurement: `pay.py` in the run folder

</details>

<details><summary>Advocate</summary>

**Advocate (AI, 2026-11-02): ship spanish_homeowners_motor_insurance_2010_2014 as defined, with wording fixes**

**Position.** Ship after changes, and none of them touches the data or the split. Every evidence agent finds no validity failure (P1-P5) that needs a fix in the definition. The real problems are wording: the metric reason and issue 5 appeal to the family (MET-10 amendment), the splits_comment's gap numbers, and four note numbers. The open calls go to the curator: the metric under MET-10, and the payment-method pair. Neither is a reason to hold the dataset back. One new fact (point 3) removes the column auditor's top problem.

New measurement: `lapse.py` (run folder) (raw `data_ex.csv`; "lapse row" = a customer's last row with `Retention` = 0).

**1. A real renewal task that every reviewer accepts (P3; USE-1, USE-8 Must, held as `approximate`).**
* Evidence: real yearly renewals of one insurer's bundle customers; the target is the home loss cost the actuary prices (domain practitioner: "Ship after the curator's calls; nothing I found changes the task enough to reject it"). The blind reviewer, with no notes, reached the same use case: "The data is real ... The use is real." The model paper prices the next period's home premium for these customers (ESWA Sec. 3.5, Table 8).
* The gaps are real and already declared in `fit_reason`: no premium, cover or exposure; rating fields frozen; a closed 2010 cohort. USE-8 asks to write the fit, not to reach `direct`. These gaps are the tension row "a real task against imperfect cleaning" (P3 over P7): keep the task, note the rest.
* Concede: two wording fixes. "assuming they renew" becomes "prices the next period's home premium for such customers (Sec. 3.5, Table 8)" (claim auditor 4). `fit_reason` says outright that the task ranks risk without a current premium (domain practitioner).

**2. No leak: the columns hold only what the renewal knows (P4; LEAK-10 Must, LEAK-34 Must narrowing it).**
* Same-year outcomes are dropped: `NClaims2`, `Types`, `NClaims1`, `Claims1`, `Retention`. The column auditor shows `Types` encodes the target, so dropping it was right.
* The history is built from earlier rows only. The column auditor checked this independently with a (PolID, year+1) merge: `prev_home_claims` sums to 2,616 and `prev_home_claim_cost` to 582,693.7 both ways. The claim auditor confirmed it too.
* The 91% of test rows that match a training row except for the year are the same customer a year earlier. That is known-entity history, legitimate under LEAK-34 (split auditor, claim auditor). The leak probes' 1-NN finds no signal.
* The frozen rating fields meet LEAK-10's later-pull clause. Each field's AUC for a home claim is flat by year (range at most 0.045). By years before lapse the range is at most 0.07, with no trend, in bins of 95 to 350 positives (claim auditor). `Client_Seniority` does not move with the lapse cohort (min 5.0, median 7.9-8.1; column auditor). Remedy: correct the "0.045" sentence to give both ranges (claim auditor 3).
* The blind reviewer's "keep PolID as a group column" is not needed. The split is temporal and the repeat is the use case (SPLIT-3: one regime, the one the use case implies). The repeat is documented in splits_comment ("the test customers are all known").

**3. New fact: lapse years show more home claims, not fewer, so there is no sign of truncated exposure (P3; USE-5).**
* The column auditor's problem 1 says lapse-year targets "may be partial years", because "the home-claim share of each customer's lapse year is about a quarter below that of their renewed years: 1.51% against 2.01% (2010), 1.64/2.23, 1.77/2.69, 1.75/2.07, 1.73/2.18". I recomputed it. Those exact numbers are real, but the columns are swapped: **renewed rows 1.51 / 1.64 / 1.77 / 1.75 / 1.73%, lapse rows 2.01 / 2.23 / 2.69 / 2.07 / 2.18%**. Pooled, it is 1.65% against 2.21%. Claim counts give the same picture: 3.02% against 3.78%.
* Within the lapse cohort alone, the lapse year is also higher than the same customers' earlier years in every cohort: 2.23 vs 1.71, 2.69 vs 1.91, 2.07 vs 1.85, 2.18 vs 1.59.
* This agrees with the claim auditor (2.21% vs 1.65%) and the domain practitioner (2.2% vs 1.6%). It fits the model paper: claims push customers to lapse (Sec. 3.3, footnote 1). It cannot prove full exposure, since the release has no dates. But the measured sign is the opposite of a truncation signature (EV-1: a measurement settles the fact). The existing `fit_reason` caveat is enough. Optional: add "lapse years show a higher claim share (2.2% vs 1.6%)" to it.

**4. The split is the application's, and the no-gap exception follows the curator's own precedent (P4; SPLIT-11, SPLIT-14 Must; SPLIT-10 Should, exception).**
* True temporal split. There are 3 expanding yearly windows that train on 89%, 75% and 57%, and each test year sits wholly on the test side, so wisconsin's year-level leak cannot occur (split auditor; SPLIT-8 does not apply).
* A one-year gap would leave 2012 with 33% of the rows and only two windows, which breaks SPLIT-14 (Must). The tension row "unmatured training labels against the training floor" decides this: SPLIT-10 gives way to SPLIT-14 and the exception is recorded. This is the ruling of `pricing_game_2016_french_fleet` (Andrej, 2026-11-02). The curator declined the amendment and asked that each such case be decided as an exception of its own (CC 2026-11-02, avito_demand_prediction), and the precedent checker sees no drift.
* The effect is small. In the split auditor's simulation of late claims (calendar-year reading), the mean Gini is 0.219 without delay, 0.226 at 30 days and 0.203 at 90 days. Every result is inside one window's SE of 0.06 to 0.11. The domain practitioner finds the whole history worth about 0.03 Gini, and the unmatured part is only a fraction of that.
* Concede the wording: the splits_comment quotes the wrong bound and calls a 0.073 drop "inside one window's noise". Remedy (split auditor, precedent checker): name both readings of `year`; give the 30/90-day simulation as the bound for calendar years and the drop-a-year run as an upper bound for policy years ("about one standard error"); rerun `exp_gap.py` on the shipped frame before quoting it; cite the avito CC beside pricing_game_2016.

**5. Faithful data, checked against the source to the row (P5; PROV-1, PROV-13).**
* Every number checked holds, and all of them match the data article's Table 1 exactly:
  * 122,935 rows and 40,284 customers, with the yearly counts;
  * claimants 660 / 531 / 448 / 310 / 240 and their mean costs;
  * the motor row 769 / 547 / 318 / 209 / 124.
  The SHA-256 is identical (claim auditor).
* The description's "motor" label for `NClaims2` is shown to be a typo by `Types` = 3 (2,123 rows).
* The only untested reading is `Client_Seniority` >= 5. Remedy: name both readings in the anomaly bullet. Neither leaks, because the value is constant per customer (claim auditor 5).

**6. The normalized Gini on the amount stands on this table's own evidence (P6; MET-3 Must, MET-11 Must, MET-10 Weigh).**
* Concede: issue 5's "Decision: confirm (family consistency)" and the "same choice and scale as" siblings contradict the MET-10 amendment, and must be reworded per table (claim auditor 1, precedent checker 2). The same holds for "log1p keeps the family's convention" (precedent checker 1).
* The current reason is already argued per table: it uses this table's numbers and names no sibling for the Gini. That is the precedent checker's option (a).
* RMSE on the amount fails here. The 20 largest claims hold 83-94% of each test year's sum of squares, every model scores R^2 between -0.07 and 0.00, and even an oracle claim indicator explains 16-22% of the variance.
* The Gini separates every model family from a constant in every window. Claim AUC is 0.67-0.70 (blind reviewer).
* A Tweedie deviance is the only rival with a source anchor (the source fits Tweedie GLMs). The domain practitioner, who proposed it, still advises against declaring it here:
  * severity cannot be learned (R^2 < 0 on claimants);
  * with 240-448 claimants it is close to squared error on a few claims;
  * scored on `expm1` of log-scale predictions, it penalises the back-transform bias of every log model, not the ranking.
* So the call is not "in doubt" in MET-10's sense. Diversity is one Weigh factor and applies only when the call stays in doubt.
* The blind reviewer's top concern, "RMSE on log1p(cost) is about 98% noise", is about a metric that is not declared. The clean room did not carry the metric. Under the declared Gini its own evidence (AUC 0.67-0.70) is the signal.
* Concede: the Gini also leans on large claims, which carry 40-58% of each year's loss, and its null SD is 0.07-0.10 (claim auditor 2). Remedy: put those numbers in the reason and state that comparisons use the mean over 3 windows. Strike the record's stale `rmse` fallback by a CC line, as in australian.
* If the curator still chooses a deviance for diversity, the fix is a one-line metric change (fix the definition), not a hold.

**7. Worth benchmarking, and scorable in every fold (P6; TP-9 Must, TP-2 Should).**
* Every window has 240-448 positives, and the dummies score as they should on all 3 folds: a constant gets 0, the oracle 1 and the negated oracle -1 (claim auditor).
* Every model family beats the one-variable tariff (apartment alone, Gini 0.177) in every window (domain practitioner). That is a small real signal, which TP-2 says is no reason to retire, as for spanish_motor_insurance_2015_2018 (Gini 0.116) and wisconsin.
* The window noise is real. Remedy: say "use the mean over 3 windows" in the splits_comment. No wider window can exist with 5 years (split auditor 3).

**Open for the curator (not reasons to hold the dataset)**
* The payment-method pair (precedent checker, LEAK-10 later-pull clause). I argue for option (a), keep with the note, on three facts:
  * this release has no "last" wording, while the sibling's `Payment` is "Last payment method";
  * the sample was selected and described in 2010;
  * the gap shows no trend (7.0 / 7.3 / 3.7 / 3.3 / 8.7 points), where a switch after claims would make it grow.
  The sibling's drop is itself an open AI draft, not a curator precedent. If the curator picks (b), dropping two columns is the mildest fix and the dataset stays.
* P7 notes, all keep-with-note:
  * `metro_code`: 84% of rows are "rural"; add a one-line share note;
  * `Car_power_M` 4-17: say "unusual (microcar range)", not "implausible";
  * `age_of_car_M`: a value above age minus 18 for 161 customers, so the field is likely the car's age; and "CLEAN-10 not triggered" in place of "departure";
  * `past_*`: a span that grows with the year; keep, with a note.
* Record the first acceptance of `task_time_on_few_unique` as the precedent.

```text
Verdict: ship after changes (wording only).
Validity: USE-1 holds (approximate, USE-8); LEAK-10 holds (same-year outcomes dropped; frozen fields kept under the
later-pull clause, flat AUC); LEAK-34 holds (history from earlier rows); SPLIT-11/14 hold; SPLIT-10 exception for
SPLIT-14 (pricing_game_2016 precedent); PROV-1 holds (Table 1 matched).
Value: TP-9 holds (240-448 positives per window); TP-2, a small real signal (keep); MET-3 holds; MET-10 per table, Gini
on own evidence (reword the reason and issue 5).
Quality: CLEAN-10/11/12 notes (metro share, microcars, car age).
Weighed: real source +, history signal +, frozen fields -, small windows -, closed cohort -.
For the curator: the metric under MET-10 (Gini vs deviance); the payment-method pair (LEAK-10 consistency check).
```

</details>

<details><summary>Critic</summary>

**Critic, opening brief (AI, 2026-11-02): spanish_homeowners_motor_insurance_2010_2014**

**Verdict: ship only after changes.** I found no Must violation that cannot be fixed, so I do not ask for exclusion.
The task is real: renewal pricing of a known customer, a true temporal split, and the year's own outcomes dropped. But
three statements that carry the decisions are wrong or unsupported as written: the reason for the no-gap exception, the
case for the metric, and one quote in the use case. The metric was argued for the family, not for this table. Points
are in rank order. Each says what I ask for, using the mildest remedy that works.

**Measured by me (`data_ex.csv`, one-off runs, no script kept), and used below:**
* **Home claim share by `Retention`.**
  * Lapse rows (`Retention` 0): 2.01 / 2.23 / 2.69 / 2.07 / 2.18% in years 1 to 5.
  * Renewed rows: 1.51 / 1.64 / 1.77 / 1.75 / 1.73%.
  * The lapse year therefore has the *higher* share. The column auditor's problem 1 ("lapse years a quarter lower, so
    partial years") has the two groups swapped. The claim auditor and the domain practitioner have the sign right.
* **`Age_client` read date.** 10 customers are under 23. If the field had been read in 2015, every customer of a 2010
  car-and-home sample would be 23 or older, so the field was read in 2010 or earlier.
* **Motor payment method against a home claim, by years before the lapse.** The annual share is 72.2/66.9,
  73.2/68.5, 74.2/67.4 and 74.8/70.2% (no claim / claim). The gap does not trend towards the lapse.

**1. P3, USE-1 (Must) and USE-8 (Must): the use case misquotes its source, and the fit reason misses measured facts.**
* *Problem.* `use_case` says the model paper prices the next home premium "assuming they renew" (Sec. 3.5). That
  section argues the opposite: the usual premium assumes renewal, "However ... the premium should be obtained by
  considering ... that the insured may or may not renew". Its Table 8 compares premiums with and without the
  claim-lapse dependence (claim auditor, point 4).
* *Also missing from `fit_reason`:*
  * The book is "rank renewal risk", not "reprice against a current premium". The release has no premium (domain
    practitioner, gap 1).
  * The test years drift towards claim-free survivors: 30.7% of claim years end in a lapse, against 24.5% of claim-free
    years (split auditor, point 2).
* *Effect.* USE-1 still holds: the renewal pricing decision is the source's own. But a reader of the summary is told
  that the source supports a premium that ignores lapse, and it does not. The fit is approximate for more reasons than
  the text names.
* *Remedy (fix the text).*
  * Reword to "The model paper prices the next period's home premium for such customers (Sec. 3.5, Table 8)".
  * Add to `fit_reason` and the Rows bullet: the model ranks renewal risk and has no current premium to beat; the 30.7%
    against 24.5% lapse rates; and lapse rows with a higher claim share (2.2% against 1.6%), so nothing points to cut
    lapse years.
  * Keep `fit="approximate"`.

**2. P4, SPLIT-10 (Should, the exception) under SPLIT-9 (Must): the no-gap exception rests on the wrong experiment and
an overstated claim.**
* *Problem.* `splits_comment` justifies gap 0 by dropping the newest training year. It calls a fall from 0.317 to
  0.244 at 2013 "inside one window's noise".
  * That fall is about one standard error (null SD 0.066 at 2013; claim auditor), not clearly noise.
  * The experiment measures the wrong delay when `year` is a calendar year. The split auditor ran the delay the
    pricing_game_2016 precedent uses (30 or 90 days of late claims): 0.226 and 0.203, against 0.219.
  * The comment never says that the delay can be up to a year when `year` runs from each customer's renewal date
    (precedent checker, point 7). The data article says the source held "dates of renewal".
  * The split auditor also found that the builder's `exp_gap.py` omits `past_*` and keeps the raw year. Its numbers
    (2014 base 0.133) differ from the shipped frame (0.161).
* *Effect.* An exception to a Should must name the fact that sets the case apart (principles.md, Strengths). The stated
  fact is half the story. The exception itself is sound: a one-year gap leaves 2012 at 33% training, so SPLIT-14 wins,
  as in pricing_game_2016 and the CC on avito_demand_prediction declining the amendment.
* *Remedy (fix the text, keep gap 0).*
  * Name both readings of `year`.
  * Give the 30/90-day simulation as the calendar-year bound and the dropped-year run as the policy-year upper bound,
    both rerun on the shipped frame.
  * Replace "inside one window's noise" with "about one standard error".
  * Cite the avito CC beside pricing_game_2016.

**3. P4, LEAK-10 later-pull clause (Must, the curator decides each case): the frozen fields are kept on a test with a
wrong number, and the precedent conflict over payment method is not addressed.**
* *Problem.* The note says "no field moves by more than 0.045". That holds by calendar year. Over the years before a
  lapse, three fields move by 0.066 to 0.070, with no trend, in thin bins (claim auditor, point 3).
* The sibling `spanish_motor_insurance_2015_2018` drops its frozen `Payment`, because its claim pattern cannot be
  traced. This table keeps `Policy_PaymentMethodA/H`, which show a 4 to 9 point annual-payment gap against a home claim
  (precedent checker, point 3). The definition does not state what sets the two cases apart.
* *Effect.* The keep is likely right. The evidence I measured supports a read in 2010: ages under 23 exist, and the
  payment gap does not grow towards the lapse. But the clause allows a keep "only when the part that can be traced
  shows none", and the curator has to see that test stated correctly, with the pair resolved.
* *Remedy (a note and a curator call).*
  * Correct the number: "0.045 by year; at most 0.07, without a trend, by years before the lapse".
  * Add the read-date evidence: the age floor; the Specifications Table selecting the sample in 2010; no "last" wording
    here, unlike the sibling.
  * Put the precedent checker's consistency check (option a) to the curator.

**4. P6, MET-10 (Weigh) and MET-11 (Must, context origin "only when the context is clear"): the metric was argued for
the family and only against RMSE.**
* *Problem.* The builder's issue 5 asks the curator to confirm the Gini for "family consistency". The task reason
  lists the siblings as "the same choice and scale". On 2026-11-02 the curator amended MET-10: the metric is chosen per
  dataset, and in doubt diversity wins.
  * The only alternative weighed was RMSE.
  * The source fits Tweedie GLMs and chooses the power by maximum likelihood (DiB Sec. 2). That makes a Tweedie or
    Poisson deviance on the amount the source-anchored candidate, and the domain practitioner names it as the metric
    he would consider.
  * This would be the 9th normalized Gini in the working copy, against one deviance.
  * The reason implies the Gini is immune to the large claims, and it is not: the 20 largest claims carry 40 to 58% of
    each test year's loss (claim auditor, point 2).
* *Effect.* Two metrics are plausible here, so the context is not "clear" until the alternative has been measured. A
  family call is exactly what the curator ruled out.
* *Remedy (fix the definition's reasoning, not necessarily the metric).*
  * Measure the mean Tweedie deviance on the amount (power from a Tweedie fit on training data) on the 3 windows, for
    the same model families. Report whether it separates them from a constant and from apartment-alone.
  * Drop "family" from issue 5 and from the reason. Add the loss-share fact.
  * Give the curator the choice between the Gini and the deviance. The practitioner's point that a deviance penalises
    the back-transform bias of log1p models goes on the Gini side.

**5. P6, TP-9 (Must, holds): the windows are noisy and the definition does not say so where scores are read.**
* *Problem.* There are 240 / 310 / 448 positives per window, and the null SD of the Gini is 0.066 to 0.101. The
  per-window Gini of one model moves by up to 0.15 between windows. The gaps between model families (ridge 0.280,
  LightGBM 0.219) sit inside one window's SE.
* *Effect.* TP-9 is met: these are hundreds of positives, not a handful. But single-window comparisons mislead. This is
  a value point, not a reason to exclude.
* *Remedy (a note).* In `splits_comment`, state the null SD and that models should be compared on the mean over the 3
  windows.

**6. P7, CLEAN-19 / CLEAN-10 / CLEAN-11 (quality): small feature and wording repairs.**
* `past_home_claims` and `past_motor_claims` count over a span that grows with the year. The mean of
  `past_home_claims` is 0.029 in 2011 and 0.121 in 2014, so each test year sits outside the range of every training
  year (split auditor). *Remedy:* a per-year rate, or a note.
* `Age_client` and `Client_Seniority` are 2010 values on 2014 rows. If the curator accepts the 2010 read (point 3),
  the repair `Age_client + policy_year - 2010` is cheap. Otherwise keep the note.
* Wording:
  * "log1p keeps the family's convention" should become a per-file reason (precedent checker, point 1).
  * `Car_power_M` 4 to 15 is "unusual (microcar range)", not "implausible" (column auditor).
  * The judgment line "CLEAN-10 departure" should read "CLEAN-10 not triggered".
  * Add `age_of_car_M` above age minus 18 for 161 customers, and `metro_code` at 84% rural.
* Quality only. None of this argues against shipping.

**7. Record (EV-7, the record must not contradict the definition): the screening still proposes `rmse`.**
* *Problem.* The record's screening bullet still proposes the `rmse` fallback. The definition declares the Gini.
* *Remedy:* the curator's CC line on the metric settles it, as in australian_vehicle_insurance_2004_2005.

**Not raised.** The blind reviewer's ask to keep `PolID` as a group column: under a true temporal split the known
customer is the use case (USE-10, LEAK-34), and I find no rule that asks for it.

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate, rebuttal (AI, 2026-11-02): spanish_homeowners_motor_insurance_2010_2014**

**Where we stand.** The critic and I agree on the verdict ("ship after changes"), on the lapse-year sign (critic measured the same 2.01-2.69% vs 1.51-1.77% I did), and on no exclusion. The real disagreement is point 4, the metric, so I ran its decisive experiment. It settles the critic's question in favour of the Gini.

New check: `tweedie.py` (run folder) (loads the definition through `dataset_io`, the 3 shipped windows, untuned LightGBM as in the split auditor, mean Tweedie deviance on the amount at power 1.5 and 1.8, predictions clipped at 1e-3, 200-draw paired bootstrap against the train-mean constant).

**1. Use case quote and fit reason (P3, USE-1/USE-8): concede.** Same remedy I proposed in my point 1: reword to "prices the next period's home premium for such customers (Sec. 3.5, Table 8)"; add to `fit_reason` the absent premium (ranks risk), the survivor drift (30.7% vs 24.5% lapse after a claim year) and the higher claim share of lapse rows (2.2% vs 1.6%). `fit="approximate"` stays. Nothing follows beyond the text.

**2. No-gap exception (P4, SPLIT-10 under SPLIT-9): concede the text, the exception stands.** We agree the exception is sound (SPLIT-14 Must wins; pricing_game_2016; avito CC). Remedy as both briefs say: both readings of `year`, the 30/90-day bound (0.226 / 0.203 vs 0.219) and the dropped-year upper bound, rerun on the shipped frame, "about one standard error", the avito CC cited.

**3. Frozen fields and payment method (P4, LEAK-10 later-pull clause): concede the number; the critic's new evidence strengthens the keep.** I checked the critic's age argument on the raw file: 4 customers are 18 and 10 under 23 (one row per customer). A customer who held motor and home in 2010 was at least 18 then, so an age of 18 means the field was read in 2010 or before. That is the traced part showing a read before the outcomes, which is what the clause asks. With the flat payment gap by years before lapse (critic: 72.2/66.9 to 74.8/70.2, no trend) and no "last" wording, it gives the precedent checker's option (a) a documentary *and* a measured distinguishing fact. Remedy: correct "0.045" to "0.045 by year; at most 0.07, without a trend, by years before the lapse", add the age floor, put the consistency check to the curator.

**4. Metric (P6, MET-10 Weigh, MET-11 Must): concede the family framing; contest that the context is unclear. The decisive check is now run.**
* Conceded: "family consistency" in issue 5 and "same choice and scale" in the reason go; the 40-58% loss share goes into the reason.
* Measured (power 1.5; deviance difference to the constant, with bootstrap SE):

| window | apartment alone | LightGBM log1p (expm1) | same, rescaled to train mean | LightGBM Tweedie objective | Gini: apartment / log1p / Tweedie |
|---|---|---|---|---|---|
| 2014 | -0.17 (0.34) | +129.7 (32.4) | +25.3 (24.1) | +5.3 (3.7) | 0.112 / 0.161 / 0.129 |
| 2013 | -0.37 (0.10) | +64.0 (8.9) | +5.6 (4.2) | +0.24 (0.95) | 0.220 / 0.315 / 0.264 |
| 2012 | -0.29 (0.08) | +101.6 (17.1) | +8.2 (5.4) | +1.9 (1.1) | 0.198 / 0.182 / 0.246 |

  At power 1.8 the picture is the same or worse: every learned model is 30 to 300 deviance units worse than the constant.
* What it means. Under the deviance, no learned model beats the constant in any window. That includes a model trained on the Tweedie loss itself. Only the two-value apartment tariff edges ahead. The log1p models lose by a factor of 3 to 8 because they predict near-zero costs for some rows that then claim. That is the back-transform the domain practitioner warned of, and it scores calibration in the tail, not the risk ranking the renewal acts on. Under the Gini, the same models separate from the constant in every window (0.13 to 0.32).
* Rule. MET-10's factors are the resolution on our folds and the ceiling. A metric that puts every model below a constant cannot tell methods apart here, so the call is not in doubt, and the diversity factor ("when the call stays in doubt") does not arise. MET-11's context origin is then clear on this table's own evidence, not the family's.
* Caveat, stated honestly: these are untuned models with a clip at 1e-3. A tuned, calibrated model might beat the constant. That is the curator's to weigh, but the bar a deviance sets on 240-448 claimants is "calibration of the tail", which is the RMSE problem in another form.
* Remedy: add one sentence and these numbers to the reason ("a Tweedie deviance on the amount, the source's model family, puts every untuned model below the train-mean constant on all 3 windows"), and drop "family".

**5. Noisy windows (P6, TP-9 holds): concede the note.** State the null SD (0.066-0.101) and "compare on the mean over the 3 windows" in `splits_comment`. One correction to my own brief, from the same run: "every family beats apartment-alone in every window" (my point 7, after the domain practitioner) does not hold for untuned LightGBM on log1p at 2012 (0.182 vs 0.198). It holds on the 3-window mean (0.219 vs 0.177). That is the critic's noise point in a concrete case. TP-2 still keeps it: a small real signal.

**6. P7 repairs: concede the notes, narrow two.**
* Wording fixes (log1p per file, microcars, "CLEAN-10 not triggered", the car-age and metro notes): agreed.
* `Age_client + policy_year - 2010`: point 3 makes a 2010-or-earlier read measured, so the repair is now safe as a lower bound. The remedy ladder ranks repair above a note (P5 over P7). I support it as optional, for the curator, with the same shift for `Client_Seniority`. If the read was before 2010, the repaired age is still closer to the truth than the frozen one.
* `past_*` growing span: narrow it to a note. The drift comes from the release starting in 2010, not from leakage. `prev_*` carries the measured signal (6.0% vs 1.7%), and a per-year rate is our own invention. That falls under "a fix of our own invention does not replace the source" (P5 over P6 tension), so I prefer the note. A per-year rate is acceptable if the curator wants it.

**7. Record's stale `rmse` (EV-7): concede.** The curator's CC on the metric strikes it, as in australian.

**Net.** The changes are text, plus two optional cheap repairs (aged `Age_client`/`Client_Seniority`; `past_*` as a rate). The one decisive dispute, the metric, now has a measurement. The Gini resolves the models and a Tweedie deviance does not, so the Gini stands on this table's own evidence.

</details>

<details><summary>Critic rebuttal</summary>

**Critic, rebuttal (AI, 2026-11-02): spanish_homeowners_motor_insurance_2010_2014**

**Where I stand now: ship after text changes only.** The advocate and I disagree on almost nothing. I ran one check, on
the metric, and it settles that point for the advocate: I withdraw my request to put a Gini-or-deviance choice to the
curator. What I still ask for is wording and notes, listed at the end.

**New fact: the Tweedie deviance does not work as a metric here.**
* Script: `dev.py` (run folder). It uses the shipped frame and splits through `dataset_io`, untuned LightGBM
  and ridge, and scores the mean Tweedie deviance (power 1.5) on the amount.
* A constant (the training mean) beats every fitted model on the deviance, in every window. That includes LightGBM
  trained with the Tweedie objective itself:

| model | 2014 | 2013 | 2012 |
|---|---|---|---|
| constant (training mean) | 21.8 | 18.0 | 20.3 |
| LightGBM, Tweedie objective | 27.1 | 18.2 | 22.2 |
| models fit on log1p | 140 to 898 | 217 to 277 | 265 to 27,669 |

* The log1p models score so badly because a near-zero prediction on a row with a claim costs a great deal under this
  deviance.
* Only apartment-alone edges past the constant (21.6 / 17.6 / 20.0).
* The Gini of the same models runs from 0.11 to 0.32, with every one above the constant's 0.

**Point by point**

**1. A real renewal task (USE-1, USE-8): concede.** The advocate accepts both rewordings I asked for. One narrow ask
remains. Two facts should go into `fit_reason` or the Rows bullet, not into an optional note:
* the drift towards survivors: 30.7% of claim years end in a lapse, against 24.5% of claim-free years (split auditor);
* lapse rows have the higher claim share, 2.2% against 1.6%.

USE-8 asks for the known gaps to be named. A test book that drifts towards survivors without claims is one of those
gaps, not cleaning.

**2. No leak (LEAK-10, LEAK-34): concede.**
* The same-year outcomes are dropped. The history is built from earlier rows only, and two auditors verified that
  independently.
* My point 3 asked for a corrected number and a curator call on the payment-method pair. The advocate makes the same
  two requests.
* I add one fact for option (a) on that pair. Ten customers are under 23, which a read in 2015 could not produce.
  Together with the gap showing no trend towards the lapse (my opening brief), this supports a read in 2010.

**3. Lapse years have more claims (USE-5): concede.** This is the same fact I measured: the column auditor's columns
are swapped. Only the ask from point 1 above remains.

**4. The split and the no-gap exception (SPLIT-10 under SPLIT-14): concede.** The advocate accepts every text change I
asked for: both readings of `year`, the 30/90-day bound, "about one standard error", a rerun on the shipped frame, and
the avito CC.

**5. Faithful data (PROV-1, PROV-13): concede.** No dispute.

**6. The metric (MET-10, MET-11): concede, after my check.**
* My point 4 argued that the context was not "clear" (MET-11) while a deviance anchored in the source was unmeasured.
  It is measured now: the deviance ranks a constant above every model, so it cannot be the metric this task would use.
* The call is not in doubt, so MET-10's diversity factor does not apply. The Gini stands on this table's own evidence.
* Remaining asks, all text:
  * Drop "family" from issue 5 and from "log1p keeps the family's convention".
  * Add to the reason that the 20 largest claims carry 40-58% of each year's loss and that the null SD is 0.07-0.10.
  * Add one line on the deviance result above, so the context origin rests on a measured comparison and not on RMSE
    alone.

**7. Worth benchmarking (TP-9, TP-2): concede.** It matches my point 5: state the null SD and compare models on the mean
over the 3 windows.

**Open items and P7.**
* I agree with the advocate's list.
* `Age_client + policy_year - 2010` is an option for the curator only if the curator accepts the 2010 read. I do not
  make it a condition.
* The `past_*` span that grows with the year stays with a note.
* My point 7 (the record's stale `rmse`) is covered by the advocate's CC-line remedy.

**Judgment record (critic, final)**

```text
Verdict: ship after changes (text only).
Validity: USE-1 holds (reword the Sec. 3.5 quote); USE-8 approximate (add the survivor drift and the lapse claim share);
LEAK-10 holds (correct the 0.045 sentence; payment-method pair to the curator, option (a) supported by the age floor);
LEAK-34 holds; SPLIT-10 exception for SPLIT-14 holds (rewrite splits_comment).
Value: TP-9 holds (note the null SD, compare on the mean of 3 windows); MET-11 context holds once the reason records that
the Tweedie deviance ranks a constant above every model; MET-10 per table (drop "family").
Quality: CLEAN-10/11/12 and the past_* note, as listed by both sides.
```

</details>
