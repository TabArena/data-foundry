# spanish_homeowners_motor_insurance_2010_2014

**Outcome:** added; shipped on Andrej's verdict of 2026-11-02. The re-review of 2026-11-06 under the exposure rules
(LEAK-41, MET-14 to MET-16) leaves nothing to decide: its text changes are made. The authors' release (Mendeley Data
vfchtm5y7j, CC BY 4.0): 122,935 customer-years of 40,284 Spanish customers who held a motor and a home policy with one
insurer in 2010, followed until they lapsed either one, 2010-2014. The target is the year's home claim cost (0 for
98.2%), shipped as log1p and scored unweighted on the amount by the normalized Gini; the inputs are 13 rating fields
and the customer's earlier home and motor claims; three yearly test windows, 2014, 2013 and 2012, each trained on all
earlier years. Validity: SEL-1, SEL-2, USE-1, USE-5, LEAK-34, PROV-1 hold; USE-8 approximate (no current premium,
closed 2010 cohort); the split rules SPLIT-9, SPLIT-11 and SPLIT-14 hold; LEAK-10 fixed (the year's own outcomes
dropped); the rating fields read once kept with a note (issue 1; a new test finds no update of the insured values after
a claim); LEAK-41 not triggered (no weight, time on risk or earned amount; the year-end lapse added as a feature gains
no Gini); SPLIT-10 departed from, no gap (issue 2). Value: TP-9 holds (240 / 310 / 448 claimants per window); TP-2, a
small real signal (EV-3): the task probe's flags `no_signal` and `drift_baseline` read squared error on the log1p scale
(best family R^2 0.008), while on the declared Gini its fitted families score 0.21 to 0.28 against 0 for a constant
(LightGBM 0.168 / 0.280 / 0.179 by window in the claim audit); MET-15 holds on its unweighted branch (per contract, no
realized denominator); MET-14 holds with a bound (a yearly renewal term, known at the renewal; the release has no
dates, so at most the 23.8% of rows that end in a lapse can be cut short (a policy year ended by a cancellation before its end), and they claim more often, not less).
Quality: CLEAN-10 not triggered (`age_of_car_M` zeros kept with a note); CLEAN-11 notes (microcar powers, 84%
"rural"); CLEAN-19 `past_*` kept as counts; the frozen ages kept as released (issue 4). Weighed: the original
release +, a real renewal decision +, the claim history signal +; frozen rating fields -, a closed 2010 cohort -, noisy
windows -.

Changes made (2026-11-02), no decision needed: the text of `use_case`, `fit_reason`, `splits_comment`, the metric reason
and the notes was corrected after the panel (wording and numbers only). The split is unchanged (train 89.2 / 75.3 /
57.0%, 240 / 310 / 448 positives).

Changes made (2026-11-06), no decision needed: the notes gained an Exposure bullet (no exposure column; the insured
values are rating factors, not an amount at risk). After the re-review it also gives the bound on the years a lapse
could cut short (at most the 29,296 lapse rows, 23.8%, since the release has no dates), the elasticity of the cost to
the insured values (0.13 contents, 0.15 building, against 1 for an amount at risk) and the rules that apply (MET-14,
MET-15, LEAK-41). Text only: rows, columns, split and metric unchanged.

**Main points:** No open issue. Shipped (Andrej, 2026-11-02), every issue resolved as implemented: the 13 rating fields
kept after a nine-test leak check (1), no gap (2), the Gini (3), the frozen ages (4), two warnings accepted (5). The
exposure re-review of 2026-11-06 adds none: no column is a weight or a time on risk, and the notes now bound the lapse
years that could be cut short.

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

**Review panel:** ship after changes (mediator). Focused re-review of 2026-11-06 under LEAK-41 and MET-14 to MET-16,
after the notes gained an Exposure bullet: the claim auditor and the mediator ran, with no blind reviewer, task gamer,
advocate or critic in this tier. The changes are text only and made. Claim audit: 9 claims, 8 hold, 1 partly holds (the
share of years cut short that MET-14 asks the notes to give was missing; now given as a bound, since the release has no
dates), none refuted. Agreed: no LEAK-41 suspect (no weight, time on risk or earned
amount; the year-end lapse added as a feature gains no Gini); MET-15's unweighted branch; the insured values stay
features (elasticity of the cost 0.13 and 0.15, against 1 for an amount at risk); their read date stays unknown, kept
under LEAK-10's later-pull clause (issue 1), and a new test finds no update after a claim. Disputed: none, so no new
issue. The full panel of 2026-11-02, which settled issues 1 to 5, is in this file's git history.

<details><summary>Mediator</summary>

**Mediator (AI, 2026-11-06): spanish_homeowners_motor_insurance_2010_2014, focused exposure re-review (claim auditor
only)**

Sources: the change note, the claim auditor's report and its scratch (t1 to t4 outputs, run folder), principles.md,
MET-14/15/16 and LEAK-10/41, and the dataset's dataset.py, README.md (line 210) and REVIEW.md. This tier had no
advocate, critic, task gamer or precedent checker, so nothing was disputed. I did the precedent check myself from the
Cases tables.

**1. Judgment record**

Verdict: ship after changes (text only). The dataset stays shipped (Andrej, 2026-11-02). No data, column, split or
metric change.

Validity:

- LEAK-41 is not triggered. The task declares no weight (`scoring_columns` [], `sample_weight` None, metric inputs
  {}). No feature is a time on risk or an earned amount, and none encodes one.
- Adding the lapse marker as a feature gains no Gini (0.168 -> 0.129, 0.280 -> 0.265, 0.179 -> 0.168). The lapse
  marker alone scores 0.054 / 0.023 / 0.124.
- LEAK-10: the insured values are still kept under the later-pull clause, as the curator decided (issue 1,
  2026-11-02). A new difference-in-differences test finds no update after a claim: the claim gap is the same for
  stayers and lapsers (contents -0.056 vs -0.055, building -0.118 vs -0.150).
- LEAK-10's last sentence (a weight or denominator column is never kept with a note) does not apply, because the
  insured values are not the task's weight.
- USE-5 holds: the target is the per-contract yearly cost.

Value:

- MET-15 holds on its unweighted branch (per contract, no realized denominator).
- MET-14: the planned term is constant (a yearly renewal) and known at the renewal. The Should part, "the notes give
  the share cut short", is not met yet; it is a text gap, fixed below.
- The scorer behaves: a constant scores 0.000, the oracle 1.000, a random prediction -0.004 / -0.102 / -0.064.

Quality: nothing new. Weighed: nothing new.

For the curator: nothing to decide. The changes below follow from MET-14 as written.

**2. Changes to make now** (no decision needed)

- a. MET-14 (Should): add the bound on the share that could be cut short to the Exposure bullet. Edit the
  `curation_comments` in dataset.py, then regenerate README.md line 210. Suggested clause: "If a lapse can fall within
  the year, at most the 29,296 lapse rows (23.8%; 17.3 / 22.1 / 24.3% of the test years 2014 / 2013 / 2012) are cut
  short. They claim more often, not less (2.21% against 1.65% of rows), and the year-end lapse as a feature adds no
  Gini (0.168 / 0.280 / 0.179 without, 0.129 / 0.265 / 0.168 with)." I checked the counts in t2.out:
  - 29,296 lapse rows, 0.2383 of all rows.
  - Per test window: 2,296 of 13,284, 3,760 of 17,044 and 5,461 of 22,505. These match the cohort sizes.
  - Retention==0 falls exactly on each lapser's last row. The 1.87% of rows where "last row and not year 5" fails are
    the 2,296 lapses in 2014, so this is no contradiction.

  The bullet must call this a bound, not a measured share: the release has no dates.
- b. EV (the evidence should carry the claim): add the elasticity to the "rating factor, not an amount at risk"
  sentence. The quintile cost figures are point estimates whose 95% intervals overlap (contents Q1 [6.23, 10.15], Q5
  [7.89, 14.52]). The claim "not proportional" rests on the elasticity: 0.13 for contents and 0.15 for building
  (marginal), against 1 for an amount at risk. Every 95% interval excludes 1, and the highest upper bound is 0.48.
  Suggested clause: "the elasticity of the cost per row to the insured value is 0.13 (contents) and 0.15 (building),
  against 1 for an amount at risk." This is optional wording, but it is cheap.
- c. Rule citations in the same bullet: "stay features (MET-14)" should read "(MET-14; scored unweighted per contract,
  MET-15; no LEAK-41 suspect)". This is wording only.
- d. `CHANGELOG.md` entry of the working copy for the text edit (house rule).

**3. Changes that need the curator**

None. One point stays open but needs no decision:

- Is a lapse a non-renewal at the year's end, or can it be a mid-year cancellation?
  - The data article says "does not renew". ESWA Table 3's "cancel at least one policy per period" leaves it open;
    the auditor could not open ESWA.
  - The decisive test is already run: a perfect proxy of the lapse year gains nothing on the declared metric.
  - Change 2a covers it with the bound. Reading ESWA would settle the wording only.

**4. Agreed facts** (claim auditor; I re-read t1, t2 and t4)

- The 20 features are 13 rating fields, 6 history columns and `policy_year`. There is no exposure, duration or earned
  amount.
- Insured values, cost per row by quintile:
  - Contents: 8.16 / 6.37 / 6.77 / 7.57 / 10.82 euros. Q5/Q1 ratio 1.34 [0.92, 2.01] for a 5.1x value ratio.
  - Building: 8.03 / 7.56 / 7.18 / 6.68 / 10.25 euros. Q5/Q1 ratio 1.24 [0.82, 1.88] for a 7.2x value ratio.
  - In the top building quintile the claim frequency halves (0.97% vs 1.94%) and severity is 2.5 times higher
    (1,053 vs 413 euros). The value acts as a rating factor, not a denominator.
- Elasticity of cost to insured value:
  - Marginal: contents 0.13 [-0.13, 0.31], building 0.15 [-0.06, 0.32].
  - Conditional: contents 0.05 [-0.15, 0.23], building 0.30 [0.17, 0.48].
- Insured values by years in the release: cohort means are flat (contents 10.30-10.34, building 11.44-11.50). There
  is no sign of an update after a claim (difference-in-differences above).
- Lapse rows, against renewal rows:
  - Home claim share 2.21% vs 1.65%. Motor claim share 2.75% vs 1.24%. Mean severity 461 vs 439 euros.
  - Within lapsers the claim share rises towards the lapse: 1.39% four years before, then 1.57%, 1.84%, 1.86% and
    2.33% in the lapse year.
  - Lapse rows show no truncation signature; claims drive lapse.
- `Client_Seniority` has a minimum of 5.002 in every cohort, and its Spearman correlation with years in the release
  is 0.045. It reflects one common read date, not tenure up to each exit.
- Features predict lapse at AUC 0.58 / 0.64 / 0.66. The top single features are `Age_client` and `age_of_car_M`, both
  known at the start.
- History columns: built with shift(1) from earlier rows only. The `past_*` span is set by the calendar. `prev_*` is
  missing in 0 test rows.
- Earlier panel's P3 (lapse years "a quarter below") had the columns swapped. The settled text already corrects it.

**5. Disputed points**

None. A single-agent tier has no opposing brief, and the auditor refuted no claim.

**6. Consistency with precedent**

- spanish_motor_insurance_2015_2018 (MET-14, 2026-11-06): the per-contract target was kept with the cut-short share
  stated (2,055 of 37,090). This case follows it once change 2a is made. Here only an upper bound can be given (no
  dates), and the bullet says so.
- liberty_mutual_fire_peril_loss_cost (MET-2/MET-4): var11, a sum insured set at underwriting, stays a feature. Same
  as here. What sets this case apart is that liberty's competition metric was weighted, so a copy of var11 also ships
  as the weight. No source here weights by the insured value, so MET-15's unweighted branch applies.
- fremtpl2, bemtpl97, australian_vehicle_insurance_2004_2005, frempl_french_motor_personal_line,
  pricing_game_2016_french_fleet and spanish_motor_insurance_coverage_level_2022_2024 (MET-14/15, LEAK-41): each has a
  realized time on risk or earned amount, which became the weight or was dropped. This release has no such column, so
  the same rules lead to no weight. That is consistent.
- The curator's own call of 2026-11-02 (issue 1, the rating fields kept under LEAK-10's later-pull clause after the
  nine-test check) still holds. Today's change does not reopen it, and test 5a adds evidence for it.
- No departure from a rule or precedent, so no consistency question for the curator.

</details>

<details><summary>Claim audit</summary>

**Claim auditor (AI, 2026-11-06): spanish_homeowners_motor_insurance_2010_2014, focused re-review**

Scope: the new Exposure paragraph (`curation_comments`, dataset.py; README.md line 210) and every claim that LEAK-41,
MET-14 or MET-15 bears on. Scratch scripts and outputs: t1 to t4 (.py/.out), run folder.

**Verdict:** nothing refuted. Every claim in the exposure paragraph holds on the data. No column is a realized amount
at risk or encodes one, and the task declares no weight, so LEAK-41 and MET-15 do not apply. One Should-level text gap
under MET-14: the notes do not give the share of rows that could be cut short.

**Claims table**

| # | claim | source | test | result | evidence | rule |
|---|---|---|---|---|---|---|
| 1 | "no exposure column, and none is needed" | Exposure bullet | container: scoring columns, sample_weight, features; is there any column with a time on risk or amount at risk | HOLDS | scoring_columns [], sample_weight None, metric inputs {}; the 20 features are 13 rating fields, 6 history columns and policy_year; none is a duration or an earned amount | MET-14, MET-15 |
| 2 | "a lapse year is a whole year as far as the sources say" (data article Sec. 1: "does not renew") | Exposure bullet | re-read the source; look for a truncation signature on lapse rows (Retention==0) | HOLDS as worded, can't be proven (the release has no dates) | ANU copy of the data article: "If the customer does not renew one of those two policies or both ...", and renewal dates were combined. Measured sign against truncation: home claim share on lapse rows 2.21% vs 1.65% (by year 2.01-2.69 vs 1.51-1.77, matches the notes); motor claim share 2.75% vs 1.24%; severity 461 vs 439 euros (mean), 173 vs 167 (median). Within lapsers the share rises towards the lapse (4 years before 1.39%, then 1.57, 1.84, 1.86, 2.33% in the lapse year): claims drive lapse, as the model paper says. The earlier panel's P3 (the column audit of 2026-11-02, lapse years "a quarter below") had the columns swapped, and the settled text already corrects it | MET-14, USE-5 |
| 3 | Insured values are "sums insured, rating factors and not an amount at risk the cost grows with in proportion" | Exposure bullet | quintile cost per row (recompute + customer-clustered bootstrap, 200 reps); log-link elasticity (the fields are log values, so a coefficient of 1 means proportional), marginal and conditional on the other 12 rating fields + year, Tweedie 1.5, 60 bootstrap reps | HOLDS | every number reproduces exactly: contents 8.16 / 6.37 / 6.77 / 7.57 / 10.82 euros per row, quintile medians 13,126 ... 66,766; building 8.03 / 7.56 / 7.18 / 6.68 / 10.25, medians 35,868 ... 258,136; overall medians 31,647 and 104,457. Q5/Q1 cost ratio 1.34 [0.92, 2.01] for a 5.1x value ratio (contents), 1.24 [0.82, 1.88] for 7.2x (building). Elasticity, marginal: contents 0.13 [-0.13, 0.31], building 0.15 [-0.06, 0.32]; conditional: contents 0.05 [-0.15, 0.23], building 0.30 [0.17, 0.48]. Every CI excludes 1. The top building quintile halves the claim frequency (0.97% vs 1.94%) and multiplies severity by 2.5 (1,053 vs 413 euros), so the value acts as a rating factor, not a denominator | MET-14 |
| 4 | "so they take neither an offset nor a weight and stay features" | Exposure bullet | follows from 3; a sum insured is set at the contract, so its value is known at the start (LEAK-41's timing test), and the field is constant per customer (asserted in `_clean`) | HOLDS | as 3; the assert passes in the build | MET-14, MET-15, LEAK-41 |
| 5 | "Their read date is unknown, so their timing is mixed: kept under LEAK-10's later-pull clause after the leak check of nine tests" | Exposure bullet + Note | (a) does the value move with a claim, as an update after a claim would? difference-in-differences: customers who stayed all 5 years (an update after a claim was possible) against lapsers, split by a home claim before the last year; (b) does the value differ by lapse cohort | HOLDS (unknown date; no sign of a post-claim update) | contents: claim-minus-no-claim gap -0.056 for stayers, -0.055 for lapsers; building -0.118 for stayers, -0.150 for lapsers, the same sign and size. A post-claim update would show only among stayers. Cohort means are flat (contents 10.30-10.34, building 11.44-11.50 for 1-5 years in the release) | LEAK-10 |
| 6 | (implied by LEAK-41) No column encodes a realized amount at risk | (implied) | Client_Seniority against years in the release; any feature as a proxy of the only possible cut marker, the lapse at the year's end: LightGBM features -> lapse_row, and the leak reference (lapse_row added as a feature, plus lapse alone) on the declared Gini, 3 seeds, shipped splits | HOLDS | seniority min 5.002 in every cohort (1 to 5 years), Spearman with years 0.045, AUC 0.52 for staying 5 years: one common read date, not the tenure up to each exit. Features -> lapse AUC 0.58 / 0.64 / 0.66 (2014 / 2013 / 2012); the strongest single features are Age_client (0.43-0.46) and age_of_car_M (0.42-0.45), both known at the start. Lapse added as a feature: Gini 0.168 -> 0.129, 0.280 -> 0.265, 0.179 -> 0.168 (no gain); lapse alone 0.054 / 0.023 / 0.124 against honest 0.168 / 0.280 / 0.179. A perfect proxy of a cut year gains nothing, so no feature can carry a cut-exposure leak | LEAK-41, LEAK-10 |
| 7 | (implied) The history columns are no outcome-set span | dataset.py `_with_history`; Added bullet | span of `past_*` by test year; missingness in test | HOLDS | `past_*` span year-1 years, the same for every row of a year (the calendar sets it, not the outcome); `prev_*` missing in 0 test rows of the 3 windows; built from earlier rows only (shift(1)) | LEAK-10, Cases row "span ... the outcome defines" |
| 8 | Metric: normalized_gini, unweighted, from context, on the amount (target_transform log1p) | metric block | MET-15 needs a weight only when a rate's denominator is realized: there is none. Score a constant, a random and an oracle prediction on each fold | HOLDS | constant 0.000 on all 3 folds; random -0.004 / -0.102 / -0.064; oracle 1.000; positives 240 / 310 / 448; metric inputs {} (no weight read). MET-15's unweighted branch (per contract) applies | MET-15, MET-2 |
| 9 | (implied by MET-14) "A per-contract target stays when the planned term is constant and known at the prediction point; the notes give the share cut short" | MET-14 | is the planned term constant and known; do the notes give the share | PARTLY HOLDS: the term is a yearly renewal (constant, known at the renewal), but the notes give no share of the rows that could be cut short | lapse rows 29,296 of 122,935 (23.8%); in the test windows 2,296 of 13,284 (17.3%, 2014), 3,760 of 17,044 (22.1%, 2013), 5,461 of 22,505 (24.3%, 2012). The real cut share is unknown (no dates) | MET-14 (Should) |

**Refuted:** none.

**Untested, or text gaps, ranked**

1. MET-14 (Should), text only. The exposure bullet says lapse years are whole years "as far as the sources say", but
   it doesn't give the share MET-14 asks for. What it changes: nothing in the data or the split. A reader learns how
   many rows would be part-years if a lapse could fall mid-year. Mildest remedy: one clause in the Exposure bullet,
   e.g. "if a lapse can fall within the year, at most the 29,296 lapse rows (23.8%; 17.3 / 22.1 / 24.3% of the test
   years 2014 / 2013 / 2012) are cut short; they claim more, not less (2.21% against 1.65%), and the lapse at the
   year's end as a feature adds no Gini (0.168 / 0.280 / 0.179 without, 0.129 / 0.265 / 0.168 with)".
2. Is a lapse a mid-year cancellation or a non-renewal? Untested: the data article (ANU copy, read through a summary
   only; I could not render the PDF) says "does not renew". An earlier panel member cites ESWA Table 3, "customers
   that cancel at least one policy per period", which leaves it open. I couldn't open ESWA here. What it changes:
   nothing measurable (test 6: a perfect proxy gains nothing). Remedy: none needed beyond item 1.
3. Optional precision: the Exposure bullet's quintile figures are point estimates whose 95% intervals overlap
   (contents Q1 [6.23, 10.15], Q5 [7.89, 14.52]). The claim needs only "not proportional", which the elasticity
   intervals settle (all below 0.5). An optional clause would make the evidence clearer: "elasticity of the cost per
   row to the insured value 0.13 (contents) and 0.15 (building), against 1 for an amount at risk".

What the auditor confirms for the curator: no LEAK-41 suspect column (no weight, no time on risk, no earned premium,
nothing a realized cut sets); MET-15's unweighted branch is the right one; the read-date wording (unknown, kept under
LEAK-10's later-pull clause) stands, with a new test (5a) that shows no post-claim update of the insured values.

</details>
