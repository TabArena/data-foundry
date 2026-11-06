# spanish_motor_insurance_coverage_level_2022_2024

**Outcome:** added. The AI recommends shipping it after the panel's changes (made, below); the forced split is settled
(2026-11-02), and the time on risk became the training weight and left the features on 2026-11-06 (issue 6). The motor
portfolio of an unnamed Spanish insurer (Espinosa, Lledó and Atance, Data in Brief 66:112883, 2026; Mendeley, CC BY
4.0): 354,091 policy-years of 185,677 policies, 2022 to 2024, with the premium of each cover. The target is the year's
claim cost over all seven covers, paid plus reserved (0 for 88.1%), per year on risk, shipped as log1p and scored on the
cost per year by the normalized Gini weighted by the time on risk (a context metric); all years of a policy stay on one
side of the split. Validity: SEL-1 and SEL-2 hold; USE-1, USE-5 and USE-6 hold, fit approximate on the forced split
(USE-8); LEAK-10 is triggered: `policy_status` and the target's parts are dropped; the time on risk, which a
cancellation cuts short, is the weight of the metric and of training and no input, and every premium is annualised
(LEAK-41, issue 6); two late values that cannot be located are kept with notes, re-measured without a gain (issue 4);
SPLIT-8 ships the three years as `ForcedGroupedFromTemporal`, shipped on your call of 2026-11-02 (forced grouped splits
ship; SPLIT-8 amended); PROV-16 was broken by a cut quote on negative costs, now quoted in full; PROV-6 and PROV-7:
distinct from spanish_motor_insurance_2015_2018 (other years, schema and task, no shared policyholders found). Value: a
small real signal (TP-2: a claim is ranked at ROC AUC 0.70-0.71, claim sizes barely learnable); the model beats the
insurer's annual premium alone (TP-4: untuned LightGBM weighted by the time on risk scores 0.317 against 0.298 on the
declared metric, ahead on 9 of 9 splits with L2 on log1p and 8 of 9 with Tweedie); the weighted Gini is this table's own
call (issue 3). Quality: impossible values made missing, including 23 zero premiums of the compulsory liability cover
(CLEAN-11); the ten claim costs below 1 EUR are kept (recorded amounts on the release's own grid). Weighed: recent real
insurer data with costs and premiums per cover +, a data article with a variable table +, size +; core rating factors
absent (vehicle age, postcode) -, low signal -, unnamed insurer -. Left for Andrej: issues 3 and 4, and the acceptance
of the warning `task_target_value_dominant`, with the proposed reason "a two-part target: 0 is a policy-year without
claim cost; 8,543 of them have a claim recorded at zero cost, some maybe negative cover amounts left out of the sum
(35.8% of third-party property claims)".

Changes made after the review panel (AI, 2026-11-01): the full-year fix now also covers the 13,842 cancelled
new-business years of policies already in force on 1 January (they had a row the year before), which lowers no score
(the Gini rises from 0.408 to 0.412, 9 splits); the 23 zero liability premiums are missing; the texts that called 69% of
the rows new customers now say 52.4% are a policy's first year; `power_to_weight_ratio` renamed `weight_to_power_ratio`
(it holds kg per horsepower); a note that nearly every claim amount sits on a grid of 0.0115 (a cent times 1.15) except
the flat amounts of 2022 and 2024, maybe a scaling from the anonymisation, which the Gini ignores. Every number in the
notes and below was re-measured on the changed definition (the panel's reports quote the definition before these
changes). The record's "left out rows with negative incurred amounts" and its screening metric line are corrected at
hand-over.

**Main points:** Issues 3, 4 and 5 are settled (2026-11-02); issue 6 (2026-11-06) makes the time on risk the training
weight, annualises the premiums and drops `total_exposure`.

**Verdict (2026-11-02, Andrej):** ship. The metric is marked as declared (`normalized_weighted_gini` on the cost per
year on risk, weighted by `actual_exposure`). The dataset joins the accepted set; a build waits for your ask.

**Issues for Andrej:**

3. **Score this table with the same Gini form as the rest of the insurance family?** The declared normalized Gini orders
   the policy-years by predicted cost and counts each once, whatever its time on risk; 49% of the rows are part-years.
   Time on risk alone scores 0.177-0.221 (9 splits), about half of the model's 0.393-0.445 (82-83% in australian and
   frempl). An actuary would weight by exposure and order by the cost per year on risk; that form keeps the order of the
   tested models here (log1p ahead of Tweedie ahead of the premium alone, 3 of 3 folds). The Gini against the insurer's
   premium (Frees, Meyers and Cummings 2011; `ordered_lorenz_gini`, added on 2026-11-01 for
   wisconsin_local_government_property_insurance_fund) gives no stable order (log1p ahead of Tweedie on 2 of 3 folds,
   behind on 1, on the final definition; on the definition the panel read, Tweedie led on 3 of 3).
   * Rule: MET-11 (Must, context origin, as diamonds) and MET-2 (Must, the unit of evaluation); which form is a
     weighing.
   * What it does to the task: under the row form a model earns about half its score by telling short policy-years from
     full ones, which says nothing about risk, so models are ranked partly on reading the time on risk.
   * Implemented: the row Gini, its reason corrected. Alternative: the exposure-weighted Gini on the cost per year
     (`ordered_lorenz_gini` with the time on risk as the weight), for the whole family. Its cost here: a scoring column
     is never a feature (MET-2), and `total_exposure` is one, so the weighted form needs a scoring copy of the time on
     risk or loses the feature. The target scale (log1p here) is decided with australian issue 5.

   Recommendation: the same form as frempl issue 4 (row or exposure-weighted), decided once for the family; australian
   issue 4 (the Gini itself against `rmse`) also covers this table. Decision: the same form as frempl, or a different
   one here?

   **Answer (AI, 2026-11-02):** No family decision on the metric (Andrej, 2026-11-02, while reviewing
   pricing_game_2016_french_fleet: "It is case by case and when in doubt we go for diversity"; MET-10 as amended). The
   question is now this table's alone: the row Gini or the exposure-weighted Gini for this table, on its own evidence, not
   matched to frempl; when in doubt, the form the collection has fewer of.

   **Andrej (2026-11-02, discuss):** Use exposure-weighted Gini on annualised claim costs for this dataset. Preserve
   original actual exposure in a scoring-only column for annualising observed costs and weighting the metric. Keep
   corrected total_exposure as the model feature; do not also expose original exposure to the model. Retain the
   existing cancellation corrections and the approved limitation for the 5,653 ambiguous first-year cancellations.
   Ensure predictions and observed costs are compared on the same annualised scale.

   **Resolved (2026-11-02, Andrej):** implemented as written:
   * `actual_exposure`: the recorded time on risk, kept before the cancellation fix, a scoring column (role weight),
     never a feature. `total_exposure` (corrected) stays the feature. The cancellation fix and the 5,653 first-year
     cuts are unchanged.
   * The target is the cost per year on risk, `log1p(total_incurred / actual_exposure)` as
     `log1p_incurred_per_exposure_year`. So the models predict a cost per year and are scored against the observed
     cost per year: the same annualised scale.
   * The metric is `normalized_weighted_gini` (Liberty Mutual's form, in the library) with `actual_exposure` as the
     weight, context origin. Policy-years are sorted by predicted cost per year, and each counts with its time on risk.
     The consistency check finds it consistent: australian's reasons for the row Gini do not hold here, since the
     located cut is fixed in the feature; it adds diversity under MET-10. It is recorded as a Cases row in metrics.md.

   Measured on the 9 splits (untuned):
   * The time on risk alone now scores -0.035 to 0.010, against 0.177 to 0.221 under the row Gini.
   * The short years carry 0.8% of the cost the Gini counts: 5.5% of the rows have under 0.1 years on risk, and the
     largest rate is 3.7 million per year.
   * One change matters: the model no longer beats the premium without the time on risk as a training weight
     (issue 5).

4. **Keep two weaker late values with notes (implemented): the year's last record and the trace of the annualised
   premiums?** LEAK-10's second clause (Must) makes each such keep your case-by-case call.
   * The year's last record: each row shows the policy as it stood at the end of the year, so a change made after a
     claim can show (the policy type changes in 2.6% of years with a claim against 1.7%). Giving the 8,115 renewal years
     whose type, brand or bonus class changed last year's values scores 0.429 / 0.412 / 0.392 against 0.426 / 0.412 /
     0.397 shipped (first three splits), within fold noise, as in house_sales (Lennart, 2026-10-21).
   * The premium trace: an active year's earned premium blends the old price with the renewal price, while a cancelled
     portfolio year, annualised by the fix, shows one price. So cancellation stays readable among portfolio years (ROC
     AUC 0.77; 0.62 without premiums). It is worth at most about 0.002 Gini, what rounding to whole euros costs, and
     rounding leaves it readable (0.685).
   * What it does to the task: a test row can carry a little of its own year's outcome; measured, it adds no score.
   * Implemented: both kept, with `Potential leak, kept on purpose:` notes. Alternatives: round every premium to whole
     euros (as frempl rounded `Exposure`; -0.002 Gini, the trace still readable), or the authors' first record of each
     year (issue 2 (d)).
   * The advocate and the critic both keep; the critic left the rounding to you.

   Recommendation: keep both. Decision: keep, or round the premiums?

   **Andrej (2026-11-02, as implemented):** Keep both with explicit potential-leak notes; do not round the premiums.
   Describe the evidence as "no consistent score gain detected in the tested comparisons," rather than proof of no
   leakage. The 0.002 Gini change from rounding is not an upper bound on leakage, since rounding also removes
   legitimate information and leaves cancellation partly readable. Revisit if records from the actual prediction point
   become available.

   **Resolved (2026-11-02, Andrej):** both kept, premiums unrounded. The three potential-leak notes in `dataset.py` now
   use your wording, drop the bound, name the revisit condition, and say which numbers come from the earlier target
   and the row Gini.
   * Re-measured on the new target and metric: giving the located cancellation status to the model outright changes
     the Gini by -0.004 / -0.006 / -0.012 (untuned LightGBM, 3 seeds, first three splits). Cancellation stays
     readable from the premiums and the corrected time on risk (ROC AUC 0.79 among the full-year rows).
   * The consistency check finds both keeps consistent (onlinenewspopularity, house_sales). Not rounding differs from
     frempl's rounded `Exposure` on a fact: there rounding removed the trace, here it does not.

5. **The model no longer beats the insurer's premium on the new metric: keep the task as it is?** This arose from the
   change of issue 3. On the exposure-weighted Gini of the cost per year (the 9 shipped splits):
   * The premium per year on risk alone scores 0.277 to 0.316 (mean 0.298).
   * Untuned LightGBM on the log1p target scores 0.269 to 0.324 (mean 0.288). On the first three splits it is below
     the premium each time (0.310 / 0.287 / 0.267 against 0.314 / 0.288 / 0.290, 3 seeds).
   * LightGBM with a Tweedie loss fit with the time on risk as sample weight scores 0.292 to 0.341 (mean 0.320),
     above the premium. Without the weight, Tweedie scores 0.300.
   * Under the earlier row Gini, LightGBM beat the premium on each split (0.426 against 0.397 on the first).

   What it changes: a model that treats a 0.1-year row like a full year learns a noisy rate. The benchmark gives the
   models no sample weight (`actual_exposure` is scoring-only, on your call), so a plain model scores about the insurer's
   price, and only a model that weighs by the corrected time on risk itself (a feature) beats it.
   * For keeping: TP-4 asks whether the task is a lookup, and it is not. The premium is a strong real baseline, the
     insurer's own price, which a good model should refine. The gap between models is the signal the benchmark
     measures (Tweedie fit with weights against log1p: +0.032).
   * Against: an untuned default model scores below a single feature it is given. TP-2 (Should) keeps a small real
     signal, so no rule asks for a change; the cost is that default models look no better than the price.
   * Rule: TP-2 and TP-4; MET-2 keeps `actual_exposure` out of the inputs.
   * Implemented: as above, nothing changed.
   * Alternatives:
     * (b) Ship `actual_exposure` as a sample weight for training only. A weight used in training says nothing about a
       test row, but Data Foundry has no training-weight column yet: the API, the container and the benchmark would
       need one.
     * (c) Go back to the row Gini on the year's cost.

   Recommendation: keep. Decision: keep, (b), or (c)?

   **Resolved (2026-11-02, Andrej):** keep, as implemented (marked as implemented, no note).

6. **Make `actual_exposure` the training weight, annualise every premium and drop `total_exposure`?**

   * **Problem:**
     - `total_exposure`, a model input, is the time on risk set to a full year for the 32,626 located cancellations
       but still cut short on the 5,653 cancellations in a new policy's first year.
     - The earned premiums of part-years scale with the time on risk, and the models train unweighted while the Gini
       weights each policy-year by its time on risk.
     - The change is safe only if no remaining column tells the models which policies were cancelled in a way that pays.
   * **Background:** The exposure study of 2026-11-05 proposed the change as its decision D10, on the condition that a
     re-measure with weighted fits finds no such column. On 2026-11-06 a new rule took a realized weight, and any column
     that encodes it or is corrected on some rows only, out of the features[^leak41]; another made the realized
     denominator the training weight as well[^met15]; and `sample_weight` entered the API. Andrej's calls of 2026-11-02
     had kept the corrected `total_exposure`, the earned premiums and no training weight[^calls].
   * **Effect on the task:** Every model trains and is scored with each policy-year counted by its time on risk, and
     sees annual premiums and no time on risk. It loses the planned time on risk of a policy that starts during the
     year (the old column gained 0.0176 under weighted Tweedie), which the release cannot separate from a cut.
   * **Experiments:** untuned LightGBM fitted with `actual_exposure` as the row weight, by Tweedie on the cost per year
     and by L2 on log1p, scored by the declared metric on the 9 shipped splits x 3 seeds; each number is the mean
     difference, its SE over the splits and the splits ahead (one run's seed SD is 0.004 to 0.010):
     - Leak references: the recorded time on risk as a free feature gains 0.0325 (SE 0.0023, 9/9) under Tweedie and
       loses 0.035 under L2; the cancellation flag gains 0.019 and 0.011 (9/9); 1/time on risk alone scores 0.075,
       against 0.317 for the model.
     - (a) The premiums of the located cancellations: they mark a cancellation at ROC AUC 0.81 among the years in force
       from 1 January (0.62 without the premiums), mostly through the occupants and legal protection premiums, which
       repeat a few flat amounts a year and show one of them when a year ends before its anniversary. Against the year
       before's premiums, this year's premiums gain -0.0006 (Tweedie) and -0.0010 (L2) through the located
       cancellation and 0.0000 and +0.0009 through the time on risk: the mark does not pay. Through any cancellation
       they gain +0.0020 under Tweedie (SE 0.0011, 7/9), under two SEs and 6% of the free-exposure gain.
     - (b) The year's last record: setting the 11,875 renewal years with a changed attribute back to the year before's
       values moves the score by -0.0006 (Tweedie, SE 0.0009; the last record ahead on 6/9) and +0.0001 (L2), at most
       2% of the free-exposure gain.
     - (c) First-year cancellation: the features rank it at ROC AUC 0.77 without the premiums (0.80 with them), mostly
       from the payment frequency and the year, both known at the quote; leaving either out costs the same with the
       cancellation flag among the features as without (+0.0008 and -0.0020 under Tweedie, within 0.0007 under L2),
       at most 3% of the free-exposure gain.
     - The old corrected `total_exposure` gains 0.0176 under Tweedie (9/9) and loses 0.0216 under L2 (0/9). Replacing
       its 5,653 cuts by an estimate of the uncut time (from the policy number, for this check only) changes it by
       -0.0012 net of a control (SE 0.0006, 3/9): the exposure study's +0.0032 (7 of 9 of its own folds) does not hold
       on the shipped splits.
     - Scores: the new definition 0.3166 (L2) and 0.3165 (Tweedie), ahead of the annual premium alone (0.2975) on 9 and
       8 of 9 splits; the old definition under the same fits 0.2911 and 0.3277.
   * **Consistency:** As fremtpl2 issue 6 and bemtpl97 issue 1 (the time insured is the weight of training and scoring,
     never a feature). It departs from Andrej's calls of 2026-11-02 on facts that came after them: the new rules, the
     training-weight API and the measurements above.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | D10 (implemented) | `actual_exposure` the training weight; premiums annualised; `total_exposure` dropped | no input carries the time on risk; both weighted fits beat the premium alone | loses the planned time on risk of late starts (0.018 under Tweedie) |
     | B | As on 2026-11-02 | corrected `total_exposure` a feature; earned premiums; no training weight | Tweedie scores 0.011 higher | breaks a Must; an untuned L2 fit scores below the premium |
     | C | A, flat covers as flags | A, with the occupants and legal protection premiums as cover held or not | the premium mark mostly gone (ROC AUC 0.81 to 0.68) | costs 0.010 to 0.012; the mark does not pay |

   * **Recommendation:** A: no column's cancellation signal pays on the declared metric, and C removes legitimate
     signal for a mark that does not pay. **Decision:** A, B or C?

   [^leak41]: **LEAK-41** (Must, 2026-11-06, Lennart): a column the task uses as a weight whose value is set or cut
     after the prediction point is never a model input, and neither is a column that encodes it ("an earned premium
     (ship it annualised to the planned term, or not at all), a length corrected on some rows and realized on
     others"); a suspect's gain is measured with an L2 fit on the shipped scale and with the weighted actuarial fit,
     and the worse decides.
   [^met15]: **MET-15** (Must, 2026-11-06, Lennart): a rate's realized denominator is the metric's row weight and the
     task's `sample_weight`, never a feature.
   [^calls]: Andrej, 2026-11-02: issue 2 (the 5,653 first-year cuts kept), issue 3 ("Keep corrected total_exposure as
     the model feature [...] Retain the existing cancellation corrections and the approved limitation for the 5,653
     ambiguous first-year cancellations"), issue 4 ("Keep both with explicit potential-leak notes; do not round the
     premiums") and issue 5 (kept without a training weight).

   **Resolved (2026-11-06, Lennart):** A, decision D10 of the exposure study, applied after the weighted re-measure
   above found no column whose cancellation signal pays. `sample_weight = "actual_exposure"`, the metric's row weight,
   so every model trains with the weight it is scored by. Every earned premium is divided by the recorded time on risk
   (days in force over 365, on a 1/365 grid in all three years): the premiums are earned pro rata, cancelled years
   included (Spearman with the time on risk 0.74 to 0.83 for the earned total premium, 0.034, 0.024 and -0.053 for the
   annual one among active part-years, first-year and located cancellations; median annual premium 340 to 355 in every
   band of the time on risk). `total_exposure` leaves the features (LEAK-41's partial-correction clause). The log1p
   target and the weighted Gini stay; `_clean` checks that the cost per year times the time on risk gives back the cost.
   The notes give the three marks with these numbers, and the CC line supersedes Andrej's calls of 2026-11-02, each on
   the fact that sets it apart: the partial-correction clause, adopted after the call, for the corrected
   `total_exposure` (the study's +0.0032 for the cuts did not hold on the shipped splits, so the clause decides, not a
   score); annualising removes the cut from the premiums, for "keep both ... do not round the premiums" (they stay
   unrounded, and the last record stays with its note); the training-weight API, for issue 5. `_load_raw` now parses
   the 15-digit decimals exactly (`float_precision="round_trip"`), so pandas 2.3 and 3.1 give the same frame and
   checksum. `dataset check`: 0 errors, 0 warnings (`task_metric_weight_without_sample_weight` fixed).

**Review panel:** ship after changes (mediator). Claim audit: 45 claims, 29 hold, 5 hold but are incomplete or inexact,
7 refuted (2 in part), 4 untested; the refuted ones are fixed in the definition or reworded (the record's line at
hand-over). Blind review: include with changes; its main concern was the exposure rule, applied to portfolio years only
(since widened; the 5,653 remain, issue 2). Split audit: right with notes. Domain practitioner: fit approximate, metric
partly right (prefers an exposure-weighted or premium-base Gini, issue 3). Precedent check: three departures (issues 1
and 2; `fit_reason`, fixed). Debate: agreed on the verdict, the widened cancellation fix and every text fix; the
mediator settled the ten small targets (kept: recorded amounts on the release's 0.0115 grid) and SPLIT-8's dated-window
sentence (added); left to Andrej: the forced split (issue 1), the 5,653 first-year cuts (issue 2), the Gini form (issue
3) and the two weaker keeps (issue 4). The reports quote the definition before the panel's changes; the issues above
quote the re-measured numbers.

<details><summary>Mediator</summary>

**Mediator (AI, 2026-11-01): spanish_motor_insurance_coverage_level_2022_2024**

**Recommendation**

```text
Verdict: ship after changes.
Validity: SEL-1 holds (consent at contracting, anonymised; Ethics Statement); SEL-2 holds; USE-1, USE-5, USE-6 hold,
  fit approximate on the forced split (USE-8; fit_reason listed kept leaks as gaps, reworded); USE-10 texts overstated
  the new-customer share (52.4% first years, not 69%), reworded, regime unchanged; LEAK-10 triggered: policy_status and
  the target's parts dropped, the cut time on risk removed where it can be located (18,784 portfolio years, now also
  the 13,842 carried-over new-business years, LEAK-7); three late values that cannot be located kept with notes under
  LEAK-10's second clause, the curator's case-by-case call (issue 2); LEAK-24 not triggered (2024 claims mature);
  SPLIT-8 holds (ForcedGroupedFromTemporal, one window of three, cost measured) but departs from how_much_did_it_rain
  (issue 1); SPLIT-24 holds; PROV-16 broken by a cut quote on negative costs, fixed in text; PROV-6/PROV-7: distinct
  from spanish_motor_insurance_2015_2018 (other years, schema and task; no shared policyholders found).
Value: TP-4 holds (all features beat the premium alone on 3 of 3 splits); TP-2, a small real signal (claim AUC
  0.70-0.71, severity R^2 0.024); MET-2, MET-3, MET-11 hold once the metric reason is corrected; the Gini form is the
  family's call (issue 3).
Quality: CLEAN-11: 34 + 3 impossible values and 23 zero liability premiums made missing; one column renamed to the
  codebook's meaning; the ten sub-euro claim amounts kept (recorded amounts, not float residue).
Weighed: recent real insurer data with premiums and costs per cover +, a data article with a variable table +, size +;
  core rating factors absent (vehicle age, postcode) -, low signal -, unnamed insurer -.
For the curator: issue 1 (forced split against how_much_did_it_rain), issue 2 (keep the 5,653 first-year cuts:
  clause call or a LEAK-10 entry for the family), issue 3 (Gini form, with frempl issue 4).
```

The advocate and the critic agree on the verdict and on every change below. Of the three points the main session left
open, two are settled here (the small targets by measurement, the dated-window sentence by SPLIT-8's text); the third
is the curator's by the rule's own wording, and a new measurement backs the keep.

**Agreed facts** (all on the definition's frame and the shipped splits; untuned LightGBM, 200 trees; normalized Gini
on the amount)

- 354,091 policy-years of 185,677 policies; 88.1% cost 0; 8,543 report a claim at zero cost.
- 52.4% of the rows are a policy's first year; the new-business flag (69.3%) stays on in a policy's second calendar
  year (61,253 rows); 62.7% of the 2024 rows had a row the year before.
- A policy with a row the year before is in force from 1 January: 47,403 of 47,411 active carried-over new-business
  years and 89,817 of 89,882 active portfolio years have exposure 1. All 13,842 cancelled carried-over new-business
  years and 18,784 of the 18,849 portfolio years below a year are cancelled. Cancelled years claim 0.50 per
  exposure-year against 0.28-0.31.
- Widening the fix to the 13,842 rows: pooled Gini 0.4072 shipped against 0.4122 fixed (9 splits, SE 0.003); on those
  rows 0.322 against 0.351. The portfolio cut left as published would add +0.008 (SE 0.002, 8 of 9).
- 5,653 cancellations fall in a policy's first calendar year, where a cut cannot be told from a late start (no start
  date). Cancellation there is ranked at ROC AUC 0.86 from the features, 0.77 without exposure and premiums. Removing
  the cut everywhere (exposure dropped, premiums annualised) scores 0.364 / 0.339 / 0.341 against 0.428 / 0.417 /
  0.379.
- The one valid window (train 2022-2023, test 2024) scores 0.379 (SE 0.022) against 0.405 / 0.374 / 0.377 on the
  folds' 2024 rows; random policy-years score as grouped (0.408 against 0.408); no policy on both sides in 9 of 9
  splits; claims per exposure-year 0.302 / 0.305 / 0.312 by year.
- The year's last record: masking type, brand and bonus changes scores 0.4309 / 0.4181 / 0.3754 against 0.4277 /
  0.4173 / 0.3787; reverting the vehicle cells 0.4090 against 0.4079 (no gain).
- The annualised premiums mark cancelled portfolio years (AUC 0.772-0.778; 0.62 without premiums; 0.685 rounded to
  euros); rounding costs 0.001 Gini.
- Time on risk alone scores 0.168-0.228 (9 folds) against the model's 0.379-0.428; the exposure-weighted Gini keeps the
  order log1p > Tweedie > premium on 3 of 3 folds; the premium-base Gini puts Tweedie ahead by 0.003-0.007 on 3 of 3.
- Experimental Design: negative incurred values "were therefore excluded from the aggregation of total_incurred"; the
  last-record step alone gave 354,140 rows, so no row was removed for a negative value. A zero cost with a claim sits
  on third-party property in 35.8% of its claims, at most 1.5% on other covers.

**Decisive checks run here** (scripts in the run folder)

- *The ten small targets* (`small_targets.py`, `grid.py`, `grid2.py`, `grid3.py`). Of the 11 positive costs below 1
  EUR, one is 6.5e-14 (float residue); the other ten are 0.0115, 0.023, 0.0345, 0.115 and 0.529, each with a recorded
  claim. Every incurred amount of every cover sits on a grid of 0.0115 (one cent times 1.15): 100% of the non-flat
  amounts of six covers and 91.7% of third-party property, against 4-22% on a cent grid. Off the grid are the flat
  CICOS amounts of 2022 (882) and 2024 (1,114) and their multiples; 2023's 1,012 is 880 x 1.15 and sits on it. So the
  ten are 1 to 46 cents on the release's own grid: recorded amounts. Settled: CLEAN-11 keeps values that are only
  unusual; no change (the critic's position). New fact for the notes: the amounts may carry an undisclosed factor of
  1.15 from the anonymisation, not applied to two years' flat amounts (maybe, EV-6); the Gini ignores a common factor.
- *A gain on the 5,653 first-year cuts?* (`remainder_gain.py`, 9 splits, on the agreed frame F). For the check only,
  the uncut time is estimated from the policy number, which follows first appearance (isotonic fit on the active
  first-year rows, R^2 0.54-0.58; never a fix: our own reconstruction). G replaces the 5,653 cuts by
  max(observed, estimate); control H gives 5,653 random active first-year rows the same treatment.

  | comparison | pooled Gini | first-year NB rows | splits with the cut ahead |
  |---|---|---|---|
  | F - G (cut kept minus cut replaced) | -0.0080 (SE 0.0014) | -0.0233 (SE 0.0037) | 0 of 9 |
  | F - H (cost of the estimate itself) | -0.0015 (SE 0.0007) | -0.0003 (SE 0.0010) | 3 of 9 |
  | H - G (gain on the cut, net) | -0.0065 (SE 0.0012) | -0.0230 (SE 0.0032) | 0 of 9 |

  The cut lowers the declared metric, as on the carried-over rows: the model reads a short year as a late start. No
  gain sits on it by this measure.

**Changes to make now** (no decision; agreed by both sides or settled by a rule)

1. LEAK-10 (Must), LEAK-7: in `_clean` step 4, `carried = df.groupby("insured_id")["year"].transform("min") <
   df["year"]` and `late = df["policy_status"].eq("C") & (df["business_type"].eq("P") | carried)`. Update `known`,
   `changes` ("cancelled years of policies in force from 1 January"), decision 3 (text, table by first year or not)
   and the kept-leak bullet (now the 5,653 rows, with the numbers of issue 2).
2. USE-8 (Must): `fit_reason`: approximate because held-out policies of the same years stand in for next year's book;
   the year's last record, the first-year cut and the blended premiums named as kept potential leaks.
3. USE-10, SPLIT-8: `split` and `grouping.definition`: 52.4% of the policy-years are a policy's first year (the flag
   stays on into the second calendar year); `row` keeps "69% are new business" as the flag's share.
4. SPLIT-8 (Must, "say what the timestamp or a dated window would change"): in `splits_comment`, under a dated window
   a renewal is a known policy whose last-year claims are a feature (+0.007 to +0.013 Gini on renewal rows), and the
   score is the 2024 window's 0.379, where the pooled mean 0.408 mixes years (2022-2023 rows rank more easily, not
   shared policies); and what sets it apart from how_much_did_it_rain (not IID; window cost measured). Settled: SPLIT-8
   requires it, and the advocate's rebuttal adopts it.
5. LEAK-10 second clause, notes: last-record bullet with the masking numbers instead of the drop-`bonus_score` test,
   and the vehicle columns named (value changes 3.06% against 2.07%); a new `Potential leak, kept on purpose:` bullet
   for the premium trace (AUC 0.77 against 0.62; about 0.001 Gini); "the values known when the year started" reworded
   (an active year blends in the renewal price).
6. PROV-16 (Must): quote the negatives sentence in full with its reason (claim reversals, overprovisioning); drop "the
   release holds no negative cost and no recoveries" and any implication that rows were removed; the target is the sum
   of the covers' non-negative costs. Warning reason: "claims recorded at zero cost; some may be negative cover amounts
   left out of the sum (maybe: 35.8% of third-party property claims)". Record: an Assessment line correcting "left out
   rows with negative incurred amounts" (the curator's CC text stays).
7. MET-11, MET-2 (Must): metric reason: Frees et al. order by the relativity to the premium, Liberty Mutual weighted by
   `var11`, only Allstate 2011 scored this row form and on whole vehicle-years; time on risk alone scores 0.168-0.228;
   the Gini sees neither level nor spread; the R^2 range of the raw-amount fit is -0.010 to -0.003.
8. EV-8: re-run on the final frame or label the frame: the status gain (measure3), the portfolio gain (now +0.008, SE
   0.002, 8 of 9), the premium move after a claim (+0.6% / -0.1% did not reproduce).
9. Who decides (principles.md): "the family's call of 2026-10-30" (twice) becomes "the AI's suggested call of
   2026-10-30".
10. CLEAN-11 (Should): mask the 23 zero `liability_premium` values (a compulsory cover; Experimental Design: premiums
    "verified to ensure strictly positive numeric values").
11. CLEAN-1 (Should): rename `power_to_weight_ratio` to `weight_to_power_ratio` (Table 2: "Weight-to-power ratio of the
    vehicle (kg per horsepower)").
12. EV-2: an `Anomaly:` bullet on the 0.0115 grid (above), with the sub-euro amounts kept.
13. Record: `required_split` and the regime tag go to REVIEW.md as field rows (records.md: once a definition exists
    the field holds its regime); an Assessment line supersedes the screening's "fallback (`rmse`)" metric line.

**Changes that need the curator** (in REVIEW.md, rank order)

1. P4, SPLIT-8 (Must) against a curator precedent: ship the forced grouped split, or treat it like
   how_much_did_it_rain (`No`)? Recommendation: ship; the fact that sets it apart is written down (below).
2. P4, LEAK-10 second clause (Must; "each a case-by-case judgment of the curator, never a default"): keep the 5,653
   first-year cuts as published with a note (recommended), record the keep as a LEAK-10 entry for time on risk in
   insurance pricing (also recommended, for the family), or remove the cut everywhere. The same mark covers the two
   weaker kept values (last record, premium trace).
3. P6, MET-11 / MET-2 (Must; a weighing of forms): the row Gini or an exposure-weighted Gini, decided once with frempl
   issue 4 and australian issue 4; the target scale with australian issue 5.

**Disputed points**

- *The 5,653 first-year cuts.* Critic (opening): the traced portfolio part gains +0.004 to +0.010, so the clause's
  "keep only when the traced part shows none" is not met; the cut lifts the claim AUC 0.03-0.04. Advocate: removal
  costs 0.04-0.08 and strips the time on risk of about 168,000 late starts; the carried-over analog loses. After the
  rebuttals both recommend the keep as the curator's call; the critic withdrew because the portfolio rows are read
  through a flag the 5,653 lack. Rule: LEAK-10's second clause, which makes the keep the curator's call whatever the
  numbers. Settled as far as facts go: the closest traces show a loss on the declared metric (the carried-over cut on
  its own rows, 8 of 9 splits; the 5,653's own cut against an estimate, pooled, 9 of 9); the claim AUC is not the
  declared metric.
  What would settle it fully: a start date or contracted term, which the raw rows (on request; policy call 8: no
  requests) may hold.
- *The ten small targets.* Advocate: float residue, set to 0. Critic: recorded amounts, keep. Settled by measurement
  for the critic (above): on the release's 0.0115 grid. CLEAN-11 keeps them. Not an issue.
- *SPLIT-8's dated-window sentence.* Critic: the advocate's fix left it out. The advocate's rebuttal adds it. SPLIT-8
  (Must) requires it. Change 4. Not an issue.
- *Negative costs as a target-meaning question (Tensions, P3/P5)*. Critic: some zeros may be net-negative claims set to
  0. Advocate: under either reading a zero is no net cost to that cover; the values cannot change. Settled for the
  advocate: no repair is possible without the raw rows, and the target is the sum of non-negative cover costs, as frempl
  sets its negatives to 0; a PROV-16 text fix (change 6).
- *Rounding the premiums.* Both: keep with a note, rounding the curator's option. The remedy ladder: rounding leaves the
  trace readable (0.685 against 0.62 without premiums) and costs what the trace is worth (0.001), so it does not resolve
  the problem; keep with the note, inside issue 2.

**Consistency with precedent** (from the precedent checker)

- Followed: the total over seven covers (fremtpl2 CC); log1p scored on the amount (allstate_claims_severity, MET-3);
  the context Gini (diamonds, MET-11); exposure as a feature (fremtpl2 CC); the CICOS flat amounts kept (fremtpl2's
  IRSA amounts); zero-cost claims kept (policy call 2); the 26 feature copies kept (LEAK-18); `policy_status` and the
  target's parts dropped (LEAK-10 Cases); the last-record keep once the masking test replaces the drop test
  (house_sales, onlinenewspopularity); `fit_reason` wording (USE-8 as amended: kick, homesite_quote_conversion,
  house_sales); distinct from the 2015-2018 sibling (Tensions: a shared source with distinct tasks).
- Departs, with the fact: removing the located cut departs from fremtpl2 CC ("a mid-year cancellation also shortens
  it"). Fact: here the cut is located row by row (the flag and the policy's previous row), which fremtpl2's data cannot
  do; LEAK-10 as amended 2026-10-26 outranks the precedent, which should be flagged against the rule. Same reasoning as
  frempl issue 2; if that issue is answered (b), revisit here.
- Departs, a question: the forced grouped split against how_much_did_it_rain (`No`, 2026-10-30). Best guess at the
  fact: not IID (whole policies held out), the valid window measured at 0.379 against 0.374-0.405, Andrej's `Yes` given
  on a block naming this split; SPLIT-8's case open_university_learning_analytics_dataset. Issue 1, with frempl issue 5
  and australian issue 1.
- A recurring reason: a realised time on risk kept although cut after the prediction point (fremtpl2 CC, australian,
  frempl's continued records, here: the fourth). LEAK-10 is a Must, so not exceptions; one Cases row or amendment would
  settle all four (issue 2 (b)).
- Between AI drafts only: the 49 zero-exposure rows dropped here (USE-7) while spanish_motor_insurance_2015_2018 keeps
  its never-started years; whichever answer its prompt 2 gets applies here (49 rows, one claim of 180.11).

</details>

<details><summary>Claim audit</summary>

**Claim audit (claim-auditor, 2026-11-01): spanish_motor_insurance_coverage_level_2022_2024**

Verdict: ship after changes. Tested 45 claims: 29 hold, 5 hold but are incomplete or inexact (#6, #20, #29, #32, #41), 7 are refuted (#23 and #28 only in part), 4 are untested (#9, #39, #40, #45).
The refutation that matters is a Must: the definition's own fix for cancelled portfolio years leaves out 13,842
cancelled new-business years whose policy was already in force on 1 January. Their cut exposure and earned premiums are
year-end values, and the rows can be found one by one (LEAK-10). The rest are wording and documentation:
the "69% new customers" figure, a truncated quote about negative costs, and the metric's reason.

Data: the definition's frame and shipped splits (`dataset_io.from_definition` / `to_container`), plus the raw CSV
(SHA-256 as in the definition). Models: untuned LightGBM (200 trees, lr 0.05, 31 leaves), the first three shipped splits
unless a cell says otherwise (EV-8). Scripts and outputs are in the run folder (`raw_facts.py`,
`nb_prior.py`, `metric_and_leak.py`, `fix_signature.py`, `cover_premiums.py`, `premium_coarsen.py`, `extend_fix.py`,
`copies_reentry.py`, each with its `.out` file).

**Claims**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | 354,091 policy-years of 185,677 policies; 69% new business | task_summary.row | counts on the frame | holds | 354,091 rows, 185,677 ids, 245,425 NB (69.3%) | - |
| 2 | 0 for 88.1% of the policy-years | task_summary.predicted | count | holds | 88.06% (42,263 positive) | - |
| 3 | Known: "a full year for a policy carried over from the year before" | task_summary.known | exposure of rows whose policy has a row the year before, by business type and status | **refuted** for 13,842 rows | 61,253 NB rows have a row the year before, active at its end. 47,403 of the 47,411 active ones have a full year, and 13,842 of the 13,850 below a year are cancelled. The fix (`late = C & business_type == "P"`) skips them, so they ship with their cut exposure | LEAK-10 |
| 4 | "most of them new customers"; "69% of the policy-years are new business, a customer the insurer has not seen before" | task_summary.split; grouping.definition | rows whose policy is in the file the year before | **refuted** (the number) | 61,253 NB rows (25.0% of NB, 17.3% of all rows) are a policy's second or third year in the file. A policy's first row is 52.4% of the rows (185,677), not 69% | USE-10, SPLIT-8 (the argument) |
| 5 | Changes: status, claim parts, 49 rows, cancelled renewals, the rename | task_summary.changes | `_clean` read against the frame | holds | each step is in the code and in the frame | - |
| 6 | "a cancelled new policy's time on risk and premiums are cut at the cancellation" | fit_reason | as #3 | holds, incomplete | also true of the 13,842 carried-over NB years, which the definition calls fixed | - |
| 7 | Prediction point; "Each observation corresponds to an insured individual for a given year" | notes | article text | holds | Sec. 3, Data Description, word for word | PROV-16 |
| 8 | "observations presenting negative incurred values were therefore excluded"; "the release holds no negative cost and no recoveries" | notes; record CC prose and Assessment ("left out rows with negative incurred amounts") | full sentence and row counts | **refuted** | Sec. 4 reads "...were therefore excluded *from the aggregation of total_incurred*". The same section says the last-record step alone gave 354,140 rows, which is the size of the release, so no row was dropped for a negative value or as an outlier. Every incurred column has a minimum of 0, so the negatives were most likely zeroed or left out of the sums inside rows that stayed (inference). "No recoveries" is unsupported | PROV-16, EV-2 |
| 9 | Target = sum of the seven covers; 8,543 (2.4%) "report a claim closed at no cost" | notes; the reason of the proposed warning | sums; zero-cost claims by cover | sum holds; "closed at no cost" **untested** (doubtful) | Largest difference from the cover sum is 5.8e-11. A zero cost with a claim is concentrated in one cover: 10,778 of the 30,099 rows with a third-party property claim (35.8%), against at most 1.5% on every other cover. That is where CICOS recoveries can exceed payments, so some of these zeros may be net-negative claims set to 0 (maybe; EV-6) | EV-6 |
| 10 | Largest claim 571,128 = 0.8% of the cost; the top 50 hold 75% of the sum of squares; Gini of log1p / raw / Tweedie fits | notes (log1p) | recompute; refit | holds | 0.77%; 75.1%. Refit: 0.4277/0.4173/0.3787 (log1p), 0.4183/0.4091/0.3746 (Tweedie) | MET-3 |
| 11 | Hurdle: AUC 0.70-0.71, severity R^2 0.024, oracle 5-9%, hurdle Gini 0.348-0.380 | notes | measure_final.out, reproduced in part | holds | AUC 0.702-0.707, oracle 4.8-8.9% | - |
| 12 | Claim counts and cover costs are parts of the target | notes | identities on every row | holds | `total_claims` = the sum of the cover counts on all 354,140 rows; `total_incurred` = the sum of the cover costs | LEAK-10 |
| 13 | `policy_status` at year end ("at calendar year"; "at the time of analysis"); no cancelled year continues; 13.9% at 0.53 vs 11.7% at 0.73; +0.005 to 0.028 Gini | notes; decision 1 | article, variable sheet, counts | holds | Table 1 and the xlsx quoted correctly. 0 cancelled years have a later year. Rates as stated. The +0.005-0.028 comes from measure3, a frame before the final cleaning (EV-8) | LEAK-10 |
| 14 | `liability_exposure` equals `total_exposure` | notes | `Series.equals` | holds | True | - |
| 15 | 49 zero-exposure rows: premium 0, all cancelled, one claim of 180.11 | notes | count | holds | 49, all C, maximum premium 0, [180.113] | USE-7 |
| 16 | `vehicle_age` is years licensed: identity on 99.92%; +1 for 68% / 0 for 32%; the second unchanged for 88%; 18-28 for most | notes; decision 2 | recompute | holds | 99.925%; 67.5% / 32.4%; 87.8%; 84.9% in 18-28 | CLEAN-1 |
| 17 | 34 licences before 15, 3 weight ratios of 0 | notes | count | holds | 34 and 3 (2 rows were already missing, hence 36 missing) | CLEAN-11 |
| 18 | 68 brands, 513 missing values, 1,287 missing fuels | notes | count | holds | as stated | - |
| 19 | Cancelled years claim 0.50 per exposure-year against 0.28-0.31 | notes (exposure) | recompute | holds | NB 0.498 / 0.280, P 0.515 / 0.307 | - |
| 20 | Cancelled portfolio years: exposure 1 on 89,817 of 89,882 active P years; 18,784 of 18,849 below a year cancelled; the fix restores "the values known when the year started"; as published +0.004-0.010 Gini | notes; decision 3 | counts; can the shipped features still tell a cancelled P year? Premiums rounded to 2 significant digits as the control | counts hold; "values known when the year started" holds in effect but is **imprecise** | On P rows, cancellation is ranked from the shipped features at AUC 0.772-0.778 (`occupants_premium` 42% of the gain), and at 0.713-0.723 with the premiums rounded. 33.8% of the fixed rows sit on the 20 commonest occupants tariff values, against 3.9% of active P rows: a full active calendar year mixes two contract prices, a year cancelled before renewal has one. The Gini on P test rows does not move (0.382/0.354/0.392 shipped, 0.378/0.354/0.393 rounded). The +0.004-0.010 comes from measure2 (an earlier frame) | LEAK-10 (maybe; EV-6) |
| 21 | "for new business ... a cut cannot be told from a late start, since the release has no start date" (19,495 years) | notes (Potential leak, kept on purpose); decision 3 | as #3; extend the fix to these rows and refit | **refuted** for 13,842 of the 19,495 | Their policy was active at the end of the year before, so a late start is impossible. Only the 5,653 first-year NB cancellations are ambiguous. With the fix extended: overall Gini 0.426/0.412/0.399 against 0.428/0.417/0.379 shipped; on the carried NB test rows 0.346/0.376/0.321 against 0.333/0.376/0.248, and 0.351/0.368/0.314 with the premiums rounded. The cut value hurts the ranking of these rows rather than inflating it, and extending the fix adds no premium-digit signal | LEAK-10 (amended clause: late cells that can be located go); LEAK-11 |
| 22 | Premiums are earned (median about 350 per exposure-year in every band); total premium alone 0.396/0.388/0.344, beaten on 3 of 3 | notes (premiums) | by band and status; refit | holds | Active rows 340-363 by band (cancelled 383-433); premium-alone Gini as stated | USE-6, TP-4 |
| 23 | Last record of the year: type 2.6% vs 1.7%, brand 2.2% vs 1.6%, bonus 0.28% vs 0.03%, premium +0.6% vs -0.1%; dropping `bonus_score` moves the Gini by less than 0.001 | notes (Potential leak) | recompute | rates hold; the premium figure is **not reproduced**; "<0.001" **refuted** in detail | 2.57/1.67, 2.21/1.55, 0.28/0.03. Mean relative change of premium per exposure-year: +1.4% against +0.4% (same direction). Bonus drop: -0.0018 on fold 2 (measure1, a frame before the fix) | EV-8 |
| 24 | 26 policy-years repeat every feature of another policy's row of the same year | notes | feature-key duplicates | holds | 26 repeats, 24 keys, each across two or more policies | LEAK-18 |
| 25 | CICOS: 7,576 of 42,263 positive costs (17.9%) at 882 / 1,012 / 1,114, one amount per year, a few twice that | notes | exact matches | holds | 1,356 / 2,447 / 3,773 (2 rows of 1,012 in 2024 not counted); 241 at twice the amount; all on third-party property | - |
| 26 | `insured_id` "constant across the analysed years" | notes | article | holds | Sec. 3 (i) | PROV-16 |
| 27 | The article reports no model or evaluation; the Mendeley record defines no task | metric reason | full article text; mendeley.json | holds | no model, no metric; the record has a description only | MET-1 |
| 28 | Models are compared "by the Gini index of the ordered Lorenz curve of losses (Frees, Meyers and Cummings 2011)", "the metric the insurers' own Kaggle competitions chose (Allstate 2011, Liberty Mutual 2014)" | metric reason | the metric library's references; web | **partly refuted** (wording) | Frees et al. order by the relativity to the premium and accumulate premium. Liberty Mutual scored a Gini weighted by `var11` (`normalized_weighted_gini`, as liberty_mutual_fire_peril_loss_cost declares). Only Allstate 2011 scored this row Gini, on rows of whole vehicle-years. The reasons of frempl and australian say exactly this | MET-11 |
| 29 | Squared-error LightGBM scores R^2 -0.011 to -0.003 on the amount; claim AUC 0.70; oracle 5-9% | metric reason | measure_final.out | holds (the range mixes two fits) | The raw-amount fit gives -0.0098 to -0.0030; -0.011 is the log1p fit (-0.0113 to -0.0064) | EV-8 |
| 30 | Computable on our folds | MET-2 | scorer on all 9 test folds | holds | 117,797-118,268 rows, 13,817-14,344 positives, 61,892-61,893 policies, all three years in each fold. A constant scores 0.000 on 9 of 9 folds (the Kaggle row-order code gives -0.017 to +0.023); the true values score 1.000 | MET-2 |
| 31 | Shipped as log1p, scored on the amount | MET-3 | scorer | holds | the inverse is applied to y_true; ranks are unchanged in the predictions | MET-3 |
| 32 | The metric means here what it meant at the source | MET-2 | exposure floor; an exposure-based Gini (ordered by predicted cost per exposure-year, exposure accumulated) | holds in effect; reason incomplete | 53.0% of shipped rows are below a full year. Exposure alone scores 0.168-0.228 (9 folds), about half of the model's 0.379-0.428, which the reason does not say. The exposure-based Gini ranks the predictors the same on 3 of 3 folds: log1p 0.347/0.326/0.335 > Tweedie 0.333/0.320/0.325 > premium 0.308/0.282/0.284 | MET-2, MET-10 |
| 33 | "The Gini ignores the price level" | metric reason | definition | holds | a rank metric | - |
| 34 | 2024 holds 47.5% of the rows | splits_comment | count | holds | 47.47% (train 52.53%) | SPLIT-14 |
| 35 | Valid window 0.379 against 0.374-0.405 on the 2024 rows of the grouped folds | splits_comment | measure_final.out | holds | 0.3791 vs 0.4052 / 0.3738 / 0.3774 (mean 0.385, within fold noise) | SPLIT-8 |
| 36 | Random policy-years score about the same (0.068 vs 0.066) | splits_comment | group probe | holds | 200,000-row sample (EV-8) | SPLIT-4 |
| 37 | A policy is the entity; holders with several ids cannot be joined | grouping | re-entry under a new id: 2023-ended policies against new 2024 policies, matched on driver (+1 year) and vehicle | holds (small) | 223 matches at +1 year against 111-118 at other shifts: about 100 of 13,528 ended policies (0.8%) come back under a new id | SPLIT-24 |
| 38 | Screening: 354,140 rows, 47 variables, 185,678 insureds, 67,172 / 118,835 / 168,133 by year; one window above the floor | record | counts | holds | as stated | - |
| 39 | "R^2 -0.03 on log1p among positives" (2022-23 -> 2024) | record (earlier triage) | - | untested | another split; the shipped grouped folds give +0.024; superseded by the add stage (EV-2) | EV-2 |
| 40 | Own damage zero in 96.0% (86.8% on comprehensive) | record | - | untested | not the shipped target; changes nothing | - |
| 41 | Warning `task_target_value_dominant`: "a two-part target, not a cap or a placeholder" | builder (to be accepted) | zeros against claims | holds; the reason's "closed at no cost" is unverified (#9) | 0 rows with a cost and no claim, no negative values | - |
| 42 | Every feature is known at the prediction point | implied | #3, #20, #21 | **refuted** (#3/#21); maybe (#20) | as above | LEAK-10 |
| 43 | No row is a copy across the split | implied | leak probe; copy keys | holds | 0.004% exact copies; the 26 cross-policy copies split across train and test 28 times over 3 folds | LEAK-16 |
| 44 | The target is settled in every year (no immature 2024) | implied | frequency and severity by year | holds | claims per exposure-year 0.302 / 0.305 / 0.312; zero-cost share of claims 17.7 / 16.9 / 16.4%; cost per exposure-year 293 / 285 / 302 | LEAK-24 |
| 45 | Spain's youngest licence is at 15 | notes | - | untested | inference, low stakes | - |

**Refuted and untested, ranked (principles.md: validity first, Must first)**

1. **Cancelled carried-over new-business years keep their cut exposure and earned premiums (P4, LEAK-10, Must; #3, #21, #42).**
   What it changes: 13,842 rows (3.9%) hold a value known only when the policy ends. The task summary and the notes say
   the opposite ("a full year for a policy carried over"; "a cut cannot be told from a late start"). The value does not
   inflate the score: extending the fix raises the Gini on these rows (fold 3: 0.248 to 0.321) and leaves it level
   overall (-0.002, -0.006, +0.020). The remedy ladder still applies: the rows can be found one by one, by the same
   evidence the definition used for portfolio rows. Mildest remedy: in `_clean` step 4, widen
   `late = df["policy_status"].eq("C") & df["business_type"].eq("P")` to cancelled rows whose policy has a row the year
   before (P, or NB with a row in year - 1). Then rewrite the "Potential leak, kept on purpose" note to cover only the
   5,653 first-year NB cancellations, and add the carried rows to decision 3's table. The alternative is LEAK-11 (it
   weakens the signal, so keep it with a corrected note). That is the curator's call, and it departs from the
   definition's own treatment of the portfolio rows.
2. **"69% are new customers" (P3/P4 argument, USE-10; #4).** 25.0% of NB rows are a policy's second or third year in the
   file, so 52.4% of the rows are a policy's first year. The grouped split's use-case argument rests on this figure
   (whether the split stands is the split auditor's question). Remedy: correct the figure in `task_summary.split` and
   `grouping.definition`.
3. **The fix's annualised premiums are readable (P4, LEAK-10, weak, "maybe"; #20).** From the shipped features,
   cancellation among portfolio rows is ranked at AUC 0.77-0.78, and at 0.71-0.72 once the premiums are rounded. The
   Gini on those rows does not move. Active rows blend two contract prices, the fixed rows show one. Remedy: a
   `Potential leak, kept on purpose:` note with these numbers. Rounding the premiums is not worth it (overall Gini
   -0.003 to -0.008, from the other rows).
4. **Negative costs (P5, PROV-16, Must for the quote; #8, #9, #41).** The quote is truncated, and rows were not removed
   (354,140 before and after the validation). The record's CC prose and Assessment repeat "left out rows". What it
   changes: the description of the zeros (notes, the warning's reason, the record), not the data. Some zeros may be
   net-negative claims set to 0. Remedy: quote the full sentence and give the 35.8% third-party property figure as
   "maybe". frempl treats its negative amounts set to 0 the same way.
5. **The metric's reason (P6, MET-11; #28, #32).** The citation to Frees et al. and Liberty Mutual describes weighted
   Ginis, and the reason leaves out that the time on risk alone scores 0.168-0.228 of the model's 0.38-0.43, with 53% of
   rows below a year. The metric stays: an exposure-based Gini ranks the same predictors the same way on 3 of 3 folds.
   Remedy: reword as frempl and australian do, and name the exposure floor.
6. **Numbers from other frames (EV-8; #13, #20, #23, #29).** These come from measure1-3, which ran before the final
   cleaning: the +0.005-0.028 for status, the +0.004-0.010 for the portfolio fix and the bonus drop (-0.0018 on one fold,
   not "<0.001"). The premium move (+0.6% vs -0.1%) did not reproduce (+1.4% vs +0.4%), and the R^2 range mixes two
   fits. Remedy: re-run on the shipped frame, or label the version.
7. **Untested:** #39 and #40, screening numbers superseded or not load-bearing; #45 Spain's licence age, an inference;
   tuned results (TP-1); whether this is the same insurer as the 2015-2018 sibling (only the builder's sibling check
   exists).

</details>

<details><summary>Column audit</summary>

**Column auditor (AI, 2026-11-01): spanish_motor_insurance_coverage_level_2022_2024**

Verdict: ship after changes. One leak fix stops short of rows it should cover. Everything else is fine, or weak and
fine to keep with a corrected note.

```text
Validity: LEAK-10/LEAK-7 triggered, partly fixed: the full-year exposure fix covers portfolio years but not the 13,842
  cancelled years of new-business policies carried over from the year before, located the same way (issue 1);
  LEAK-10 weak: the annualised premiums mark the cancelled years they were meant to hide (issue 2); LEAK-10 weak,
  kept: last-record vehicle columns, traced part shows no gain (issue 3); LEAK-33 holds (insured_id).
Quality: CLEAN-11, 23 zero liability premiums (issue 5); naming: power_to_weight_ratio holds kg per hp (issue 6).
For the curator: issue 1 (extend the fix; the note's reason is false for 71% of the rows it covers), issue 2 (keep
  with a note, or round premiums to euros as frempl rounded its exposure).
```

How the numbers were made: I loaded the frame with `dataset_io.from_definition` and joined the raw file on
(`insured_id`, `year`). The model is untuned LightGBM (200 trees, as in the builder's runs) on the shipped grouped splits,
scored by normalized Gini on the amount. The scripts are in the run folder
(`exp1.py` to `exp5.py`). Codebook: Tables 1-4 and Sec. 3-4 of the Data in Brief article and the
variable sheet "Descriptive of variables.xlsx".

**Column table** (prediction point: when the policy is written or renewed for the year; row = the policy's last
record in a calendar year)

| column | meaning (codebook) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `insured_id` | recoded policy number, sequential by first appearance (Table 1) | n/a | int64, group column | fine: it encodes the entry order, but it is never a feature | LEAK-33 |
| `year` | calendar year 2022-2024 | yes | int64 numeric | fine (it carries the CICOS flat amount of each year) | CLEAN-14 |
| `policy_type` | cover structure TP, TPG, CC, COMP_E, COMP_N | yes, but it is the last record's value | categorical, 5 levels; the premium zeros match it (TP/TPG never have own-damage, theft or fire premiums) | fine, kept with a note: changes in 2.57% of consecutive years with a claim in the second year against 1.67% without (builder's figure confirmed) | LEAK-10 (weak) |
| `business_type` | NB new business, P portfolio | yes, last record's value | categorical, labelled | fine; a question (issue 4): in a policy's second calendar year NB and P both occur at every start date, and NB years are cancelled more often | LEAK-10 (question) |
| `payment_frequency` | annual, semiannual, quarterly | yes | categorical, labelled | fine (changes in 0.09% of years with a claim vs 0.07% without) | - |
| `bonus_score` | claim-history class G/N/B | yes, last record's value | categorical, labelled | fine, kept with a note: worsens in 0.28% of second years with a claim vs 0.03% without (the claim in the year before gives 1.43%, which is legitimate history) | LEAK-10 (weak) |
| `driver_age` | age of the main driver | yes | int64, 18-90 | fine | - |
| `years_licensed` | source `vehicle_age`; Table 2 calls it the vehicle's age, but it is the years since licensing | yes | float64; renamed; 36 values masked with their age at licence | fine: the rename holds (driver age = sum within 1 year on 99.92%; 261 rows off by 2 or more, kept) | CLEAN-12, CLEAN-11 |
| `age_at_licence` | source `age_driving_licence` (Table 2: "year in which", text: "years since") | yes | float64; values below 15 made missing (34 rows, raw values 0-14) | fine | CLEAN-11 |
| `fuel_type` | diesel/gasoline; "only two categories are kept" | yes | categorical; 1,287 missing kept missing | fine (claim share is 18.4% when missing vs 11.9%, but missingness is a vehicle attribute known at pricing, likely the other fuels) | CLEAN-10 |
| `vehicle_value` | declared insured value | yes, but the last record can show a replaced vehicle | float64, 1,630-374,034 (plausible: Ferrari, Bentley at the top); 513 missing | fine, kept with a note: changes in 3.06% of years with a claim vs 2.07% (issue 3) | LEAK-10 (weak) |
| `seats` | number of seats | yes, last record | int64, 2-9, a count | fine (issue 3) | CLEAN-14 |
| `power_to_weight_ratio` | "weight-to-power ratio (kg per horsepower)" (Table 2) | yes, last record | float64, 2.47-64.81; 3 zeros made missing; 64.81 = microcars (AIXAM, MICROCAR, GRECAV), plausible | fine, but the name is the inverse of the content (issue 6) | CLEAN-11; naming |
| `vehicle_brand` | brand, normalised by the authors | yes, last record | categorical, 68 levels | fine, kept with a note: changes in 2.21% vs 1.55% (2.59% vs 1.69% in years with an own-damage claim) | LEAK-10 (weak) |
| `municipality_type` | inland, coastal, islands | yes | categorical, labelled | fine | - |
| `circulation_area` | urban, rural (others coded NA; none occur) | yes | categorical, labelled | fine | - |
| `total_premium` | sum of the 7 cover premiums (exact on every row) | earned premium of the calendar year; see issue 2 | float64; cancelled portfolio years annualised | fine as the insurer's price (USE-6); the annualisation leaves a trace (issue 2) | USE-6, LEAK-10 (weak) |
| `liability_premium` | third-party liability premium | as above | float64; **0 on 23 rows** whose policies have other covers (exposure median 0.54, totals up to 1,068) | cleaning problem: compulsory cover, and the article says premiums were "strictly positive" (issue 5) | CLEAN-11 |
| `property_damage_premium` | own-damage premium | as above | float64; 0 = cover absent (all TP/TPG and most CC rows); 0 on 7 COMP rows | fine | - |
| `theft_premium`, `fire_premium`, `glass_premium` | cover premiums | as above | float64; 0 = cover absent, matching the policy type except on 16, 19 and 33 rows | fine | - |
| `legal_protection_premium` | legal defence premium | as above | float64 | fine; with `occupants_premium` it carries most of the trace in issue 2 | LEAK-10 (weak) |
| `occupants_premium` | occupants' injury premium | as above | float64 | as above: for cancelled years the annualised value sits on one tariff value | LEAK-10 (weak) |
| `total_exposure` | time on risk in the calendar year (Table 4) | the contracted period is known; a cut at cancellation is not | float64, 0.003-1; 49 zero rows dropped; set to 1 for cancelled portfolio years | **leak only partly fixed**: still cut on 13,842 cancelled years carried over from the year before (issue 1) | LEAK-10, LEAK-7 |
| `log1p_total_incurred` | log1p of paid + reserved cost, all 7 covers | target | float64; metric inverts it | fine | CLEAN-16, MET-3 |

Dropped and checked: `policy_status` is set at year end or "at the time of analysis" (variable sheet), so dropping it
is right (LEAK-10). The ten claim counts and the per-cover incurred costs are parts of the target, so dropping them is
right. `liability_exposure` equals `total_exposure` on every row, so dropping it is right (CLEAN-5).

**Problems, ranked by `principles.md`**

**1. P4, LEAK-10 / LEAK-7 (Must where the late values can be located): the exposure fix stops at `business_type ==
"P"`. It misses 13,842 cancelled years of new-business policies that were already in force on 1 January.**
- The code's marker for "in force from 1 January" is the portfolio flag. But 61,253 new-business years have a row of
  the same policy in the year before. These are policies written in the previous year that are still flagged NB in
  their second calendar year: 27,615 in 2023 and 33,638 in 2024, all following an active NB year.
  - Their time on risk behaves exactly like the portfolio years. Of the 47,411 active ones, 47,403 have exposure 1.
  - All 13,842 cancelled ones are below a year. So below a year means cancelled on 99.94% of these rows, the same
    marker the builder fixed for portfolio years (18,784 of 18,849).
  - 82.9% of them end within two days of the first anniversary, so most are non-renewals.
  - They claim 0.478 times per exposure-year, against 0.285 for the active carried-over years.
- With the shipped features, a classifier separates cancelled from active within these rows at ROC AUC 1.000
  (3 splits).
- Three claims in the definition are false as a result:
  - `task_summary.known`: "a full year for a policy carried over from the year before".
  - The "Potential leak, kept on purpose" bullet says "a cut cannot be told from a late start, since the release has
    no start date". That is true only for the 5,653 cancellations in a policy's first calendar year, 29% of the 19,495
    it covers.
  - `fit_reason` describes all cancelled new policies as cut.
- Measured over the 9 shipped splits, the extended fix raises the Gini from 0.4072 to 0.4122 (+0.005, SE 0.003, higher
  on 6 of 9). The cut values mislead untuned LightGBM more than they help it, because it cannot tell them from late
  starts. frempl's located early ends behaved the same way (its fix raised the Gini from 0.281 to 0.332), and frempl
  fixed them anyway. LEAK-11 (a late value that weakens the signal stays) is the only argument for keeping them.
  Against it: nothing sets these rows apart from the portfolio rows the definition already fixes, and LEAK-10's second
  clause says located late cells are blanked.
- Mildest remedy (fix the definition): in `_clean` step 4, widen the mask to rows that have a row of the same policy
  in the year before:
  ```python
  carried = pd.MultiIndex.from_arrays([df["insured_id"], df["year"] - 1]).isin(
      pd.MultiIndex.from_arrays([df["insured_id"], df["year"]]))
  late = df["policy_status"].eq("C") & (df["business_type"].eq("P") | carried)
  ```
  Then correct the three texts above, the `changes` line ("cancelled renewals") and the third Decision. The
  unlocatable remainder is the 5,653 first-year cancellations.

**2. P4, LEAK-10 (weak, Should): the annualised premiums mark the cancelled years they were meant to hide.**
- An active year's earned premium blends two tariffs: the one before the anniversary and the one set at it.
- A cancelled year, annualised by premium / exposure, shows a single tariff.
  - 2023 cancelled portfolio years: `occupants_premium` is exactly 2.52 on 28.3%, against 6.1% of active years. The
    20 most common values hold 56.5% against 29.7%.
  - Cancelled carried-over NB years: the premium per exposure-year equals the previous year's on 90.6%, against 5.9%
    of active ones.
- Status read from the shipped features, within portfolio rows:
  - ROC AUC 0.772-0.778 with all premiums (most of the gain from `occupants_premium`, `liability_premium` and
    `legal_protection_premium`).
  - 0.62 without any premiums.
  - 0.685 with every premium rounded to whole euros.
- After the issue-1 fix, carried-over NB rows read at 0.86, and 0.70 rounded.
- The note's phrase "the values known when the year started" also overstates. The active years include the renewal
  tariff, set after 1 January. That tariff moves with claims earlier in the year: premium per exposure-year +0.65% vs
  -0.07%.
- What the trace is worth: rounding costs 0.001 Gini (0.4122 to 0.4111, 9 splits). So the trace carries at most about
  that much, against +0.013 for the status itself given to the model.
- Mildest remedy: keep it, with the note corrected (mechanism, the AUC, the 0.001). Alternative, a cheap fix: round
  every premium to whole euros. That follows frempl, which rounded `Exposure` to months because "the rounding costs
  nothing and stops the decimals from marking a record that continued". Curator's call.

**3. P4, LEAK-10 (weak, kept: the traced part shows no gain): the last-record note should name the vehicle columns
(LEAK-2 sweep).**
- The bullet names policy type, brand, bonus and premium. But a vehicle replaced after a write-off or theft moves every
  vehicle column. Comparing years with a claim in the second year against years without (no claim in the first):
  - value changes in 3.06% vs 2.07%;
  - power/weight in 2.93% vs 1.99%;
  - fuel in 0.90% vs 0.66%;
  - seats in 0.60% vs 0.44%;
  - in years with an own-damage claim, value changes in 3.83% vs 2.29%.
- Traced part, on the first 3 splits:
  - reverting the 12,855 changed vehicle cells to the previous year's values: Gini 0.4090, against 0.4079 shipped;
  - also reverting policy type, bonus and payment (19,597 cells): 0.4072.
- No gain, so under LEAK-10's second clause they stay. Remedy: add the vehicle columns and these numbers to the
  bullet.

**4. P4, question (weak): `business_type` in a policy's second calendar year.**
- The flag is not a function of the start date: NB and P both occur in every start band, judged by the first year's
  exposure.
- NB second years are cancelled more often in every band (21-26% vs 16-18%). Most of these are non-renewals at the
  first anniversary that stayed NB. So the last record's flag may partly follow the non-renewal.
- Claim shares are not higher for NB (0.149-0.193 vs 0.177-0.192), so no outcome signal is visible.
- Remedy: none needed now. One sentence in the notes, or ask the authors what sets the flag.

**5. P7, CLEAN-11 (Should): `liability_premium` = 0 on 23 rows (COMP_E 15, COMP_N 4, CC 2, TPG 2).**
- Third-party liability is compulsory and part of every policy type. The rows are not short (median exposure 0.54,
  totals up to 1,068), and the article says premiums were verified "strictly positive".
- So the 0 is a missing component, not an absent cover. Remedy: make them missing (one `mask`), or note them.
- The few zero cover premiums that contradict the policy type (7 property-damage, 16 theft, 19 fire, 33 glass) are
  borderline. Keeping them is fine.

**6. P7, naming: `power_to_weight_ratio` holds kilograms per horsepower.**
- That is Table 2's "weight-to-power ratio", and the data agrees: supercars about 2.5, microcars 64.8.
- The definition renames the two mislabelled age columns for this very reason, but keeps this inverted name. The
  summary already says "weight per horsepower". Remedy: rename to `weight_per_hp` or `weight_to_power_ratio`, or say
  so in the dtype bullet.

**Claims checked and holding:**
- 49 zero-exposure rows.
- 18,784 / 18,849 cancelled portfolio years, and 89,817 of 89,882 active ones at exposure 1.
- The age identity: 99.92%; +1 for 68% of policies; 88% unchanged.
- 34 + 3 impossible values.
- The premium sum is exact.
- 26 feature copies (50 rows in copy groups).
- The bonus, brand and policy-type change shares.
- `policy_status` timing.
- The shipped Gini of 0.428 / 0.417 / 0.379.

</details>

<details><summary>Split audit</summary>

**Split auditor (AI, 2026-11-01): spanish_motor_insurance_coverage_level_2022_2024**

**Verdict on the split: right with notes.** The split is grouped by `insured_id`, 3 repeats x 3 folds, tagged
`ForcedGroupedFromTemporal`. That is the regime SPLIT-8 prescribes here: three stacked calendar years give one valid
window, and policies recur across the years. The forced split is no more optimistic than the valid window for the
newest year, and an IID split would score the same. Separately, I found one validity problem that is not about the
split itself but came out of the group structure: the cancellation fix misses 13,842 policy-years (LEAK-10, issue 1).
The other points are text corrections and notes.

```text
Validity: LEAK-10 triggered, partly fixed (cancelled carried-over new-business years keep the cut exposure; issue 1).
          USE-10 / SPLIT-23: the "new customer" share is overstated in the texts (issue 2); the regime stands.
          SPLIT-8 holds (one valid window; ForcedGroupedFromTemporal); SPLIT-14 cannot be met; SPLIT-24 holds (a true
          policy id); SPLIT-29/30: hidden cross-id entities are bounded and need no action (issue 4).
Value:    not assessed here (the Gini is noisy: bootstrap SE 0.022 on the 168,085-row 2024 window).
Quality:  splits_comment could say three more things (issue 3); the record's split fields (issue 5).
```

**What I checked, with numbers** (loaded through `dataset_io.from_definition`; untuned LightGBM with the builder's
parameters, 200 trees; Gini = the library's `normalized_gini` on the amount; scripts listed at the end)

- Splits as shipped: 9 splits, test folds of 117,797 to 118,268 rows. In none of the 9 splits is a policy on both
  sides. Each test fold holds 19.0% / 33.5-33.7% / 47.3-47.5% of its rows in 2022 / 2023 / 2024, 69.2-69.5% new
  business, and 11.8-12.1% rows with a claim cost.
- Regime the use case implies: a tariff fit on past years and applied to next year's policies, so the task is
  temporal (a stream of years). The release has years only, and they form clean runs: every year pattern of a policy
  is consecutive, never 2022 and 2024 without 2023. A 2024 window trains on 2022-2023, 52.5% of the rows. A 2023
  window would train on 2022 alone, 19.0%, under SPLIT-14's 50% floor. So there is one window where SPLIT-14 asks for
  three, and SPLIT-8 applies. 117,926 of the 185,677 policies recur, so grouping by the entity is the closest regime
  (SPLIT-8: "grouped by the entity when the periods are stacked and the entities recur across them"). This matches the
  precedents open_university and nba (2026-10-21) and the family's frempl and pricing_game_2017.
- Group id (SPLIT-24): the variable sheet defines `insured_id` as "Unique identifier assigned to each policy number.
  It assigns a sequential ID based on the first appearance of each policy number". That is a true id, not a cluster
  or a hash. One prediction is one policy-year from its own row (`prediction_unit="row"`, `context="none"`), which
  fits pricing each year. The id is not among the features.
- Cost of the forced split against the valid window: the window (train 2022-2023, test 2024) scores Gini 0.379, with a
  bootstrap SE of 0.022. The 2024 test rows of the grouped folds score 0.405 / 0.374 / 0.377. This reproduces the
  splits_comment exactly.
- Alternative split, IID by row: 3 random folds score Gini 0.427 / 0.383 / 0.415 (mean 0.408); the grouped folds score
  0.428 / 0.417 / 0.379 (mean 0.408). The group probe agrees (R^2 on log1p 0.068 IID against 0.066 grouped). No
  hidden-group optimism.
- Per year inside the grouped folds:

  | fold | 2022 | 2023 | 2024 | 2024 new business | 2024 portfolio | pooled |
  |---|---|---|---|---|---|---|
  | 0 | 0.427 | 0.460 | 0.405 | 0.415 | 0.355 | 0.428 |
  | 1 | 0.488 | 0.441 | 0.374 | 0.392 | 0.347 | 0.417 |
  | 2 | 0.395 | 0.369 | 0.377 | 0.311 | 0.415 | 0.379 |

  The pooled score is never above the mean of the three within-year scores (0.430 / 0.434 / 0.381). So scoring all
  years together gains nothing from ranking across years.
- Label delay: `total_incurred` is paid plus reserves at an extraction date after 31 December 2024. I looked for
  immature 2024 labels and found none:
  - claims per exposure-year are 0.302 / 0.305 / 0.312 in 2022 / 2023 / 2024;
  - for new policies started in October-December (active, exposure up to 0.25), they are 0.248 / 0.252 / 0.277;
  - cost per claim is 969 / 934 / 970;
  - claims closed at no cost are 17.7% / 16.9% / 16.4% of the claim rows.
  So nothing points to LEAK-24, and the grouped split needs no gap.
- Training history and season: whole calendar years, so there is no season-shaped window. The book starts in 2022
  (97.9% of the 2022 rows are new business) and grows to 168,085 rows in 2024. That is a ramp-up, not a break.

**Problems, ranked by principles.md**

1. **LEAK-10 (P4, Must when strong). The cancellation fix misses carried-over new-business years.** I found this
   through the group structure; it is a feature problem, so the column and claim auditors should check it too.
   - What the data shows: `_clean` gives cancelled years a full year and annual premiums only when
     `business_type == "P"`. But the new-business flag carries into a policy's second calendar year when its first
     year was partial. 61,253 new-business rows (25% of them) are not the policy's first year in the release; their
     previous year has median exposure 0.38 and is never a full year.
   - Those rows are in force from 1 January exactly as portfolio rows are. All 47,411 active ones have exposure 1.000;
     all 13,842 cancelled ones (6,434 in 2023, 7,408 in 2024) are below a year (mean 0.562). The cancelled ones make
     0.478 claims per exposure-year against 0.285 for the active ones.
   - So on these rows a time on risk below a year gives the cancellation away. The curation note says "a cut cannot
     be told from a late start, since the release has no start date". That holds for 5,653 of the 19,495 cancelled
     new-business years, not for all of them.
   - Decisive experiment (3 grouped folds): applying the same fix to the 13,842 rows lowers the claim ROC AUC of the
     model's output on those rows from 0.695 / 0.681 / 0.691 to 0.654 / 0.640 / 0.662. The cut carries about 0.03 to
     0.04 AUC there. The pooled Gini moves by +0.002 / +0.006 / -0.020, which is within its noise (SE about 0.02), as
     the builder's +0.004 to +0.010 for the portfolio rows was.
   - Mildest remedy, a filter fix in the definition: extend the mask to every cancelled year that has the policy's
     previous year in the release (years are consecutive, so a year after the policy's first one always has its
     previous year):

     ```python
     carried = df.groupby("insured_id")["year"].transform("min") < df["year"]
     late = df["policy_status"].eq("C") & (df["business_type"].eq("P") | carried)
     ```

     Then update the "Potential leak, kept on purpose" bullet to cover the 5,653 first-year cancellations only, and
     split the `_decisions` table by first year. A like case is treated alike: same mechanism, same fix.

2. **USE-10 / SPLIT-23 (P3-P4, Must; what the test stands for). The texts overstate how many test rows are new
   customers.**
   - The grouping definition says "69% of the policy-years are new business, a customer the insurer has not seen
     before", and `task_summary.split` says "most of them new customers". As issue 1 shows, a quarter of the
     new-business rows are a policy's second calendar year.
   - 52.4% of the policy-years are a policy's first year in the release.
   - In the newest year, 62.7% of the rows have their policy in 2022-2023: 99.97% of the portfolio rows and 34.9% of
     the new-business rows. So in deployment most rows are known policies.
   - The regime still stands. SPLIT-8 picks grouped for recurring entities. No feature carries a policy's own past
     outcome other than the insurer's `bonus_score`. And recognising a policy is worth nothing measurable (IID = grouped
     above). I could not measure a cold version of the window: removing the 2024 policies' earlier years leaves 8.5% of
     the rows for training (Gini 0.315).
   - Mildest remedy, text: "52% of the policy-years are a policy's first year; new business includes the second
     calendar year of a policy written mid-year", and in `split`, "about half of them a policy's first year". The
     `row` field's "69% are new business" is correct as the flag's share.

3. **SPLIT-8 (Must: "say what the timestamp or a dated window would change"); three notes for `splits_comment`.**
   - (a) The benchmark score pools the three years. It is 0.379 to 0.428 by fold (mean 0.408), against 0.379 for the
     window. The difference comes from the mix of years (2022-2023 rows score higher within the same folds), not from
     sharing policies. A sentence would stop a reader comparing the two numbers directly.
   - (b) Under a temporal design, the tariff for year t+1 is fit before year t's claims are known. A one-year gap
     would leave 19% of the rows for training. That is a second reason the window cannot be had, and worth one
     clause.
   - (c) "No finer date" is true only roughly. The sequential id follows the policy's inception: within the first
     year it explains 54-58% of the variance of an active new policy's remaining-year exposure (isotonic, median error
     about 0.13 years), and ids 1-74k, 74k-130k and 130k-167k are first seen in 2022, 2023 and 2024. It is no time
     index for windows, because every carried-over row starts on 1 January. It is a weak hint at the start of the
     5,653 ambiguous cancellations (observed exposure 0.64 / 0.39 / 0.37 against 0.75 / 0.57 / 0.58 implied by the
     id). A reconstruction from it would be our own invention; I do not recommend one.
   - Remedy: text only.

4. **SPLIT-29 / SPLIT-30 (Must; hidden groups across ids): bounded, no action.**
   - The definition already says one holder with several cars has several ids. I matched rows on brand, weight per
     horsepower, seats, fuel, declared vehicle value, age at licence, area and birth year (within a year), and set the
     counts against a baseline of the same keys with birth years shifted.
   - A policy's last year in t matched to a new id in t+1: 418 pairs against 258 to 354, so about 100 extra pairs.
     These are re-written policies: a claim on the old id predicts one on the new id (0.213 against 0.076; baseline
     0.074 against 0.067).
   - Twins in the same year under two ids: 3,591 pairs against 2,956 to 3,175, so roughly 400 to 650 extra pairs
     (the 26 full copies, fleets, holders with two cars).
   - At most about 750 related pairs in 354,091 rows, and an IID split scoring the same as the grouped one bounds
     what they can add.
   - Remedy: none (SPLIT-30, a probe hit is a question). Optionally one clause in the grouping definition with these
     counts.

5. **Record and family consistency (Weigh; for the curator and the precedent checker).**
   - The record has `required_split: Temporal (NON-IID)` and the tag `Non-IID (Temporal)`; the definition is
     `ForcedGroupedFromTemporal`. The forced-grouped siblings disagree among themselves: frempl's record says
     `Random (IID)` and pricing_game_2017's says `Temporal (NON-IID)`. One convention for the family's forced splits
     would settle it; I would not change this record alone.
   - wisconsin_local_government_property_insurance_fund ships two yearly temporal windows, short of SPLIT-14's three.
     The fact that sets this dataset apart is one window against two: a single window gives no spread at all. The
     calls are consistent, but the wisconsin departure should be recorded as such.

**Claims audited** (splits_comment, grouping definition, task_summary.split)

- One valid window, 2024 against 2022-2023, 47.5% of the rows: pass (168,085 of 354,091; a 2023 window trains on 19.0%).
- Gini 0.379 on the window, against 0.374 to 0.405 on the folds' 2024 rows: pass (reproduced to four decimals).
- "Random policy-years would score about the same" (R^2 0.068 against 0.066): pass, and confirmed in Gini (mean
  0.408 against 0.408).
- Policy counts 67,751 / 67,438 / 50,488 and 185,677: pass.
- "A test policy is one the model has seen in no year": pass (9 of 9 splits).
- "69% ... a customer the insurer has not seen before" and "most of them new customers": concern (issue 2).
- "The release holds three calendar years and no finer date": pass with a note (issue 3c).
- "For new business a cut cannot be told from a late start" (curation notes, bears on P4): concern, true for 5,653
  of 19,495 (issue 1).

**Files** (in the run folder; read-only work, no repository file edited)

- `load.py` (frame and splits through dataset_io)
- a1_structure.py (years, patterns, fold composition, group integrity, id order)
- a2_maturity.py (label maturity by year and start quarter)
- a4_hidden2.py (cross-id key twins against shifted baselines)
- a5_models.py (grouped per-year, IID and temporal-window Gini, test rows seen)
- a6_nb.py, a7_nb2.py (the new-business flag across years; exposure by status)
- a8_fix.py (the decisive experiment for issue 1)
- a9_id.py (the id as an inception order)

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner: spanish_motor_insurance_coverage_level_2022_2024**

I play the pricing actuary of a Spanish motor insurer. At renewal or new business I set the premium for each policy from the tariff, and once a year I review the tariff against the claims of the last years. The use case in `task_summary` names this actor ("A Spanish motor insurer pricing a policy"), and the data article names actuarial pricing as the reuse (abstract, "Value of the Data").

**Verdict.** Fit: **approximate** (agree with the definition). These are real policy-years with the insurer's own rating factors and premiums, and the target is the pure premium the tariff charges. But the test rows are held-out policies of the same three years, standing in for next year's book (USE-8; SPLIT-8 forced). Metric: **partly**. The normalized Gini is how I compare pricing scores, and the insurers' competitions chose it (MET-1, MET-11 context). But computed per row it also ranks time on risk, and it cannot see the level or the spread of the prices the tariff takes from the model. I would pick an exposure-weighted Gini of the loss per exposure-year, or the ordered-Lorenz Gini against my current premium (Frees, Meyers and Cummings 2011), as below.

**1. Inputs at the prediction point**

- Things I have that the data also has: the policy type and the premium of each cover, how the premium is paid, new business or renewal, the claim-history class, the driver's age, years licensed and age at licence, the vehicle's value, seats, weight per horsepower, brand and fuel, a coarse area code, and the year. The premium is my own price, set before the year's claims. Keeping it as an input is right under USE-6: the task becomes "refine my tariff", which is a real tariff-review job. It is also the only carrier of the rating factors the release withholds (see below). Without the premiums, untuned LightGBM ranks at a row Gini of 0.396 / 0.384 / 0.352 (first three shipped splits). With them it ranks at 0.428 / 0.417 / 0.379, and the premium alone scores 0.396 / 0.388 / 0.344.
- Things I always have that the data lacks:
  - the vehicle's age (the column the source calls `vehicle_age` is years licensed, as the notes show);
  - the postcode or province (only inland / coastal / islands and urban / rural are given);
  - the make and model or vehicle group;
  - the SINCO claim-history file run by TIREA, which Spanish insurers query when they write a policy (Rastreator, Mapfre, Acierto pages);
  - the sales channel (withheld for confidentiality, Limitations);
  - at renewal, the policy's own claims of last year.
  
  That last one is the only gap I can measure. On the 47.6% of rows that have a policy-year the year before, a claim then raises this year's claim rate from 14.6% to 22.7% and the mean cost from 253 to 434. Yet `bonus_score` barely moves (good for 94.4% after a claim, against 97.4% without). Adding the prior-year outcome as a feature lifts the Gini on those rows by only +0.007 to +0.013 (0.363 → 0.376, 0.360 → 0.366, 0.339 → 0.350). So the cold-start framing the grouped split imposes costs little (USE-10).
- Things I would not have: `policy_status` at year end (dropped, LEAK-10, right). I also would not have a time on risk that has been cut by a cancellation. That fix is only partly applied, as the next bullet shows.
- **The 1-January rule misses 13,850 rows.** The definition annualises cancelled portfolio years because "a policy carried over from the year before is in force from 1 January". It applies this only where `business_type` is portfolio. In this book, though, a policy stays "new business" through its second calendar year: 61,253 NB rows have a policy-year the year before (patterns NB-NB, NB-NB-P). 13,850 of them fall below a full year, 99.9% of those are cancelled, and they claim 0.478 per exposure-year against 0.285 for the full-year ones. So the note "for new business a cut cannot be told from a late start, since the release has no start date" is wrong for about 71% of the cancelled NB years: the policy's row the year before dates the start. The `known` text "a full year for a policy carried over from the year before" is wrong for these rows too. The measured effect is noise-level: annualising them changes the untuned LightGBM Gini by +0.001 / -0.003 / +0.019. The rule should therefore read "has a row the year before", for consistency and so the texts stay true. That is the same logic frempl applied when it located early ends row by row (LEAK-10, LEAK-7).

**2. The target**

- `total_incurred` (paid plus case reserves, all seven covers, per policy-year) is the pure premium I compare with the premium. It is what I act on (USE-5). In practice I would model each cover separately, by frequency and severity, and sum them. A single Tweedie model on the total pure premium is also common practice, so the total is a fair target. The name "coverage_level" describes the source, not the task: the target is not per cover.
- I would want a number: the expected cost per exposure-year, right in level and in relativity, because the tariff multiplies a base level by the model's relativities. The shipped log1p target trained by squared error does not give that number. Inverted, the predictions average 0.9% of the actual mean cost (3 of 3 splits), and their top-to-bottom decile ratio is 67-73 against an actual 18-25. Ranking is all the benchmark asks of them, so this is fine for a benchmark (the Gini is invariant to the inverse). But nobody should read the predictions as prices.
- The incurred figure has no IBNR and no development. 2024 shows no sign of immaturity: claim frequency is 0.312 per exposure-year against 0.302 / 0.305 for 2022 and 2023, and the pure premium is 302 against 293 / 285. Large claims are not capped, as I would cap them for a tariff, but the largest is 0.8% of the total cost. The CICOS amounts (882 / 1,012 / 1,114) are the fixed compensation amounts under the CIDE/ASCIDE agreements, which is the cost the insurer actually bears for those claims. Keeping them as recorded is right.

**3. One row against one decision; the test data**

- I price a 12-month term from its start or anniversary at an exposure of 1. A row is a calendar-year slice showing the year's last record, so a renewing policy's row blends two terms and two premiums. Calendar-year exposure slices are the usual way to fit a tariff (freMTPL, freMPL), so this is a small gap. It deserves one line in `fit_reason` next to the split.
- The extract is a young book, not a mature portfolio. 97.9% of the 2022 rows are new business and 83.2% of them are part-year, so the file follows the policies written from 2022 on. Only 52.4% of the rows are a policy's first row (185,677 of 354,091), yet the grouping definition says "69% of the policy-years are new business, a customer the insurer has not seen before". A quarter of those NB rows are the second calendar year of a policy already in the book. My next year's book would be mostly renewals.
- The test data stands for unseen policies of the same years, where I would face next year's book. The builder's one valid window (train 2022-2023, test 2024) scores 0.379, against 0.374-0.405 on the 2024 rows of the grouped folds. The Gini within each year (0.430 / 0.434 / 0.381) is no higher than pooled over years (0.428 / 0.417 / 0.379), so mixing years does not inflate it. The forced split (SPLIT-8, ForcedGroupedFromTemporal) is the honest choice with three years.

**4. Would I use it?**

- As a challenger to my tariff, yes. Against my own premium the model finds mispriced policies: on the ordered-Lorenz Gini with the premium as base, untuned LightGBM scores 0.144 / 0.132 / 0.148 with the premiums as inputs and 0.116 / 0.111 / 0.131 without them. The premium itself scores about 0 and the time on risk alone about 0 (-0.027 / -0.003 / -0.004).
- I would trust it more after a double-lift chart against the premium on a later year (2025). It is real insurer data, recent, with the cover structure and the premiums.
- I would distrust it as a tariff for four reasons. The core rating factors are missing (vehicle age, area, claim-history file), so it ranks through the premium. Each row is the year's last record: the notes show a policy-type change after a claim in 2.6% against 1.7% of cases, a weak kept leak. The insurer is unnamed. And the log1p fit gives no usable price level.

**5. The metric**

Partly. The normalized Gini is the actuarial way to compare scores (Frees, Meyers and Cummings 2011, 2014). The insurers' Kaggle competitions used it (Allstate 2011; Liberty Mutual 2014 weighted it by `var11`), and the family call of 2026-10-30 suggested it as context. So MET-1 and MET-11 are met in kind. The family call notes that the Tweedie deviance, the loss I would fit, needs strictly positive predictions, so it is no benchmark metric without a clipping rule. My objections are about the unit and what the Gini cannot see:
- **The row Gini ranks time on risk.** I price an exposure-year. On the declared row Gini, `total_exposure` alone scores 0.202 / 0.213 / 0.168, and the builder's run gave 0.21 / 0.20 / 0.16. Weighted by exposure and ordered by predicted loss per exposure-year, the same model scores 0.347 / 0.326 / 0.335 against the row Gini's 0.428 / 0.417 / 0.379, and exposure alone scores 0. frempl's metric reason names this ("the length alone scores 0.277"), and this definition's reason should too (MET-1, MET-2: the unit of evaluation).
- **It ignores my current price.** The actuary's Gini orders policies by relativity (score / premium) along the cumulative premium (Frees et al. 2011). That is exactly the tariff-review question, and it cancels the time on risk, because the earned premium already scales with exposure. The library does not have it yet. The Wisconsin LGPIF definition waits for the same metric (MET-13). Under the house convention a scoring column is never a feature, so declaring `total_premium` as the base would remove it from the inputs. Keeping the premium as an input (USE-6) would need a copy as the scoring column. That is the curator's call.
- **It sees neither level nor relativities.** The definition says the Gini "ignores the price level, which pricing sets separately". It also ignores the spread (see 2), and the spread is what the tariff takes from the model. This is a known limit of a ranking metric, so it is something to name, not a reason to reject.
- **The choice of Gini changes which fit wins.** On the row Gini, log1p beats Tweedie (0.428 / 0.417 / 0.379 against 0.418 / 0.409 / 0.375). On the premium-base Gini, Tweedie beats log1p on 3 of 3 splits (0.147 / 0.137 / 0.155 against 0.144 / 0.132 / 0.148). On the exposure-weighted Gini, log1p wins again (0.347 against 0.333). The margins are small, but they show that this choice matters.

What I would declare: an exposure-weighted normalized Gini on the loss per exposure-year. The library's `normalized_weighted_gini` would need the target shipped as a rate, or a variant that orders by prediction / weight, which is a new metric (MET-12, MET-13). Alternatively the ordered-Lorenz Gini against the premium, once it ships for LGPIF. If the curator keeps the row Gini for consistency with frempl and australian, the metric reason should state the exposure-only score and the limit on level and spread. On these numbers MET-6, MET-7 and MET-9 do not apply: the task acts on no threshold or top k, and pricing acts on a number for every policy.

**Gaps, ranked by how much they change the task**

1. Held-out policies of the same years stand in for next year's book (the approximate fit). The measured cost is small (0.379 on the valid window against 0.374-0.405).
2. Core rating factors I always have are missing (vehicle age, postcode or province, model, SINCO history, channel, prior-year claims at renewal). The task becomes "refine the insurer's price" more than "build a tariff". The only one measurable is prior-year claims: +0.007 to +0.013.
3. The metric's unit: the row Gini credits time on risk (exposure alone 0.17-0.21; 0.33-0.35 weighted against 0.38-0.43).
4. Each row is a calendar-year slice of the year's last record from a young book (52.4% first rows, 97.9% NB in 2022), not the 12-month term I price in a mature book.
5. The 1-January rule is applied by business type: 13,850 second-year NB cancellations keep their cut exposure and premiums, and two texts misstate this (measured effect -0.003 to +0.019).
6. The target is the total, not per cover. Incurred has no IBNR and no large-loss cap (minor; 2024 frequency is stable).

**What an expert in the domain would change**

- Annualise exposure and premiums for every policy-year that has a row the year before, not by `business_type`. Then correct the `known` text, the note "a cut cannot be told from a late start", and the grouping definition's "69% ... a customer the insurer has not seen before" (52.4% are first rows).
- Reword `fit_reason` under USE-8. The year's last record and the NB cancellation cut are potential leaks kept on purpose: name them as kept, not as gaps. The approximate fit rests on the split. One line on the calendar-year slice is optional.
- In the metric reason, state that `total_exposure` alone scores 0.17-0.21 on the row Gini (as frempl does), and that the Gini scores neither level nor spread. Put the exposure-weighted or premium-base Gini to the curator as the actuary's alternative.
- Optional (USE-10): give renewal rows last year's claim outcome as a feature. It is known at renewal and legitimate under the grouped split, but it adds only about +0.01.

**Sources**

- Definition, README, record, builder report and `measure_final.out` in the run folder; the data article (Espinosa, Lledó and Atance 2026, Data in Brief 66:112883, PMC13234478): Data Description, Experimental Design, Limitations.
- Rules: `use_case.md` (USE-1, USE-5, USE-6, USE-8, USE-10) and `metrics.md` (MET-1, MET-2, MET-6 to MET-9, MET-11 to MET-13). Precedents: the zero-inflated triage summary (no longer in the repository; each call is in its record's Assessment of 2026-10-30) (policy calls of 2026-10-30); the frempl and wisconsin_local_government_property_insurance_fund definitions.
- Web: Frees, Meyers and Cummings 2011, JASA 106:1085-1098, and 2014, JRI 81:335-366 (abstracts via [SUFE newsletter](https://academicnewsletter.sufe.edu.cn/info/445125) and [CAS](https://casact.org/abstract/insurance-ratemaking-and-gini-index)); [cplm `gini` documentation](https://rdrr.io/cran/cplm/man/gini.html); [Henckaerts et al., arXiv 1904.10890](https://arxiv.org/abs/1904.10890) (abstract only); SINCO/TIREA ([Rastreator](https://www.rastreator.com/seguros-de-coche/guias/fichero-sinco), [Mapfre](https://www.mapfre.es/particulares/seguros-de-coche/articulos/que-es-fichero-sinco/), [Acierto](https://www.acierto.com/seguros-coche/fichero-sinco/)); CIDE/ASCIDE/CICOS ([tuteorica](https://tuteorica.com/blog/normativa-seguros/convenios-de-aseguradoras-en-accidentes-de-trafico/), [CNMC](https://www.cnmc.es/sites/default/files/501990_0.pdf)). The Kaggle Liberty Mutual evaluation page did not render, so its `var11` weighting is taken from the family call.
- My scripts and outputs, in the run folder (`raw_checks.py/.out`, `nb_prev.py/.out`, `metric_checks.py/.out`, `base_gini.py/.out`, `nb_fix.py/.out`). All model numbers are untuned LightGBM (200 trees) on the first three shipped splits.

</details>

<details><summary>Blind review</summary>

**Verdict: include with changes.** The data are real Spanish motor insurance policy-years. The main leaks have been removed, and the split is reasonable. The changes needed are small: make the exposure rule consistent and document it, keep `insured_id` out of the features, and accept or state that this is a low-signal task.

**What the task is.** Each row is one policy in one calendar year (2022 to 2024) at a single unnamed Spanish insurer. The target is log1p of the total incurred claim cost for that year (paid plus reserved). The features are the driver, the vehicle, the cover and the earned premium per cover. An insurer would make this prediction at inception or renewal, to price the policy, check whether the premium is adequate, or set underwriting and portfolio rules. That is a real and standard actuarial use. One caveat: an actuary would model expected cost (Tweedie or Poisson-gamma with an exposure offset), not RMSE on log1p.

**How I checked.** I downloaded the public Mendeley CSV (354,140 x 47, sha256 6a47d19d...) and the variable dictionary. I joined the CSV to `data.parquet` on (insured_id, year): all 300,000 rows matched, and the target equals log1p(raw total_incurred) on every row. The 49 rows dropped from the full table are exactly the rows with exposure 0 and premium 0, all cancelled. Every categorical recoding maps 1:1 to the raw codes. The preparer removed all claim counts, the incurred cost per cover, `policy_status` and `liability_exposure` (identical to `total_exposure` in 100% of raw rows). The models were LightGBM and Ridge with 3-fold GroupKFold by `insured_id` on the 300k sample.

**Concerns, most to least serious**

1. **The exposure and premium handling is inconsistent and undocumented, and some cancellation information remains.**
   - Evidence: `total_exposure` differs from the source in 15,874 rows (5.3%). Every one is a cancelled portfolio policy. Its exposure was set to 1.0 and all eight premiums were divided by the realised exposure (ratio from 1.003 to 365).
   - That fix is defensible: for a renewal, the full year is what is known in advance. But it was not applied to the 16,543 cancelled new-business rows. Those keep their realised, cut-short exposure and pro-rated premium.
   - Cancellation is linked to claims. Among new business, 15.3% of cancelled rows have a claim against 9.8% of active rows. In the source, claims per exposure-year for short cancelled policies are 1.36, against 0.27 for active ones.
   - Cancellation can still be predicted from the prepared features: AUC 0.83 within new business and 0.76 within portfolio. Some of that is genuine churn signal.
   - Size of the effect is small. Adding the true `policy_status` lifts R2 only from 0.0607 to 0.0646. Using the raw exposure and premiums instead of the fixed ones gives 0.0633.
   - Change: document the rule in task.md. Either apply one rule to all rows, or state that `total_exposure` means planned exposure for renewals and realised exposure for new business. Planned exposure cannot be rebuilt for new business because the source has no start dates.

2. **Little signal, and the gaps between methods are narrow.**
   - Evidence: the target is zero in 88.1% of rows; positive values run up to 571k EUR. Predicting the mean gives RMSE 2.1986.
   - Default LightGBM reaches RMSE 2.1308 (R2 0.061, AUC 0.70 for any claim). One-hot Ridge is almost as good: the paired gap per fold is 0.0002 to 0.0027 RMSE, while the spread between folds is about 0.02.
   - LightGBM tuned with early stopping reaches 2.1243 (R2 0.070) on the same fold where Ridge gets 2.1318. Better methods do pull ahead, but only slightly.
   - This is what personal-lines claims data looks like, so it is not a reason to exclude. But the dataset will mostly test robustness to noise, and much of the RMSE comes from the claim / no-claim split.
   - Change: none required. Consider also reporting a Tweedie or Poisson deviance on raw `total_incurred` with exposure, which matches how the prediction would be used. Expect near-ties in the rankings.

3. **The premium features are the insurer's own price, and they are earned premium.**
   - Evidence: the median annualised premium is about 350 in every exposure bucket (350, 353, 350, 359, 352). So `total_premium` is roughly the tariff times the exposure.
   - Premiums carry the largest share of gain importance (property_damage_premium 19%, total_premium 11%). Dropping all eight lowers R2 from 0.061 to 0.053.
   - This is not a leak, because the price is set before the risk period. It does mean the task is "refine the insurer's price" (loss-ratio or adequacy monitoring), not "set the price", where the premium could not be an input.
   - The source says only that premiums are "the net amount paid by insured individuals for their policy during the corresponding year". It does not say whether a mid-term change after a claim alters the premium.
   - Change: state this framing in task.md. Optionally provide a version without premiums for a pure pricing task.

4. **The split is grouped but not temporal.**
   - Evidence: 74% of the sampled rows share an `insured_id` with another row, so grouping is correct.
   - Leakage without grouping turned out small: an overfit-prone LightGBM got R2 0.0434 on a random split and 0.0458 on the grouped split.
   - In real use the model would be trained on past years and applied to the next one. Training on 2022-23 and testing on 2024 gives R2 0.060, against 0.064 on the same 2024 rows under the grouped random split. So the grouped split is only slightly optimistic.
   - The portfolio grows strongly over the years (67k, 119k, 168k rows), and the CICOS flat amounts change each year (see the data-checks paragraph below).
   - Change: acceptable as is. A temporal split (train 2022-23, test 2024) would be the more faithful option.

5. **`insured_id` is in the table.**
   - It is a sequential ID assigned at first appearance (dictionary: "It assigns a sequential ID based on the first appearance of each policy number"), so it encodes when the policy joined.
   - Used as a feature, it lifts R2 from 0.0607 to 0.0615.
   - Change: use it only to form the groups and drop it from the model inputs.

6. **The renamed licence columns contradict the source dictionary, though the renaming is correct.**
   - The raw column `vehicle_age` is actually years licensed: driver_age - vehicle_age equals age_driving_licence in 91.1% of rows and is off by one in 8.8%.
   - Its values (mean 25.9 years, max 68) are not plausible as vehicle ages.
   - The raw `age_driving_licence` is the age at licensing (sharp floor at 18: 58k rows at 18 and 19 rows at 15). It is not the calendar year the dictionary claims.
   - The preparer's `years_licensed` and `age_at_licence` are therefore right, but the dataset contains no real vehicle age, and `age_at_licence` is almost exactly driver_age - years_licensed.
   - Change: record this in task.md so nobody "fixes" it back.

7. **Minor data-quality items.**
   - 11 positive targets are below 1 EUR (minimum 6.5e-14), which looks like floating-point residue. Set them to 0.
   - In the raw table, `age_at_licence` is below 16 in 57 rows and above 70 in 8 rows, and `power_to_weight_ratio` is 0 in 3 rows.
   - Missing values: fuel_type 0.36%, vehicle_value 0.14%, licence columns 0.01%.
   - 37 rows have exact duplicate feature vectors (18 of those groups span different insureds).
   - All negligible. The column types (pandas category for the categoricals) are sensible, and `vehicle_brand` has 67 levels with a long tail.

**Is it real?** Yes, with strong evidence.
- Liability property-damage incurred amounts pile onto one flat value that changes each year: 882 EUR in 2022 (1,765 of 3,383 claims), 1,012 in 2023 (3,268 of 6,254) and 1,114 in 2024 (5,027 of 9,684), plus their double values (1,764 / 2,024 / 2,228). This matches the source's note that CICOS direct-settlement claims "may show clustering because of pre-agreed settlement amounts". I could not confirm the yearly amounts against an official CICOS source.
- Cover and claims are consistent: property claims without a property premium occur in 2 of 12,526 cases, glass claims without glass cover in 0, theft in 0.
- The totals are plausible for Spanish motor: loss ratio 0.66 / 0.66 / 0.75, frequency about 0.30 claims per exposure-year, average cost per claim about 950 EUR.

**Other checks.**
- `bonus_score` timing: downgrades from G to B track prior-year claims (0.52% against 0.013%) far more than same-year claims (0.24% against 0.04%). The feature has 0.3% of gain importance. No meaningful leak.
- Source quirks:
  - 2022 is almost all new business (65,764 NB against 1,407 portfolio), so this is essentially a cohort written from 2022 onward.
  - 61k rows are labelled new business even though the insured appears in the previous year.
  - The abstract's ">185,000 unique insured policies per year" is wrong; 185,677 is the number of distinct insureds over all three years.

**What I could not check.**
- The 653,943-row raw extract. In particular, I could not tell whether claims and exposure from earlier contract versions were summed or lost when the authors kept "the last record per insured and year", or whether the last record's vehicle or premium reflects a change made after a claim.
- How developed the reserves are for claims late in 2024 (IBNR). I saw no drop in 2024 loss cost per exposure (302 against 293 and 285).
- The identity of the insurer.
- Whether the benchmark harness drops `insured_id` from the features.
- The exact 3x3 split protocol. I used 3-fold GroupKFold on the 300k sample.

**Process notes.**
- I downloaded the source files into a new, empty folder of my own.
- By accident I first downloaded into a folder that held another dataset's files. I did not open or use them.

Sources: https://doi.org/10.17632/sw4jmdb2sm.1 (Mendeley data and dictionary), https://pmc.ncbi.nlm.nih.gov/articles/PMC13234478/ (Data in Brief article).

</details>

<details><summary>Precedent check</summary>

**Precedent check (precedent-checker, 2026-11-01): spanish_motor_insurance_coverage_level_2022_2024**

**Verdict.** Most choices follow their precedents. That covers the total over the seven covers, one row per
policy-year, the drops, the cleaning, log1p scored on the amount, the context Gini, exposure as a feature, and the
portfolio fix. Three real departures need the curator; the third is wording:

1. the forced grouped split sits against Andrej's `No` on how_much_did_it_rain. The facts that set it apart are clear
   but not written down (prompt 1);
2. the kept cut time on risk of cancelled new business departs from LEAK-10's clause of 2026-10-26 as written.
   australian's LEAK-11 fact does not transfer, and the builder's option (c) would not remove the cut (prompt 2);
3. `fit_reason` lists two kept leaks as gaps (USE-8 as amended; prompt 3).

Two notes need fixing, with no decision:

* "the family's call of 2026-10-30" (twice) presents an AI suggestion as a decision;
* the last-record note rests on a drop-a-column test. The masking test I ran supports the keep.

**What counts as a precedent here.** Curator decisions:

* fremtpl2 CC (Andrej, 2026-10-20);
* how_much_did_it_rain CC (Andrej, 2026-10-30);
* the policy calls of 2026-10-30 (Andrej): no insurance convention, calls per dataset; coded zeros no reason for a
  `No`; no cap for a family; no data requests;
* this record's CC (Andrej, 2026-10-30, `Yes`, priority 4);
* the Cases rows and amendments by Lennart cited below.

Every other insurance definition of this run is an AI draft with no curator decision yet: frempl, australian,
spanish_motor_insurance_2015_2018, allstate_claim_prediction_challenge_1m, pricing_game_2017_french_mtpl, wisconsin
and rand. So is the suggestion table of 2026-10-30, an AI reading that Andrej asked for per dataset. The register's 14
flags touch none of this dataset's rules. The two SPLIT-14 "exceptions" it lists (alfa_battle_2_0_task_2,
lending_club) are SPLIT-10 exceptions that serve SPLIT-14's floor, not this split.

**Per decision**

| Decision (rule) | Standing | Closest precedents | What sets it apart, or not |
|---|---|---|---|
| Target `total_incurred` over all seven covers. One row per policy-year, not per cover and not own damage (USE-5, PROV-6, PROV-7) | consistent | fremtpl2 CC (Andrej, 2026-10-20): aggregate claim amount per policy, "not both (same policies, swapped target)". frempl (all guarantees), allstate, pricing_game_2015 (sum of two covers): drafts and the AI table | A per-cover target would be the same rows with a swapped target |
| All policy-years kept, unlike the sibling's first-year-only rows (USE-5) | consistent. The fact is measured but not in the notes | spanish_motor_insurance_2015_2018 (draft, same research group): later rows held a remnant of the first year's claims (0.7% claim after a claim-free year) | No remnant here. After a claim-free year, 14.6% of 149,929 next years have a claim, against 22.7% of 18,485 after a claim year. Claims per exposure-year are 0.302 / 0.305 / 0.312 by year. The sibling's precedent checker measured the same. One sentence in the notes would answer the sibling |
| Grouped by `insured_id`, tagged `ForcedGroupedFromTemporal` (SPLIT-8, SPLIT-14, SPLIT-4) | consistent with SPLIT-8 and its cases. Against how_much_did_it_rain, no fact is written down | SPLIT-8 cases nba_players_2016_2019 and open_university_learning_analytics_dataset (Lennart, 2026-10-21): 3 or 4 periods stacked and grouped, one valid window measured. how_much_did_it_rain (Andrej, 2026-10-30): `No`, "Forced IID is to be avoided at all costs". Drafts: allstate_1m (3 years, by household), frempl (its issue 5), pricing_game_2017, australian (forced IID, its issue 1) | Evident: not IID, so no test row shares an outcome with a training row. On the one valid window the Gini is 0.379, against 0.374-0.405 on the folds' 2024 rows. Andrej's `Yes` was given on a screening block that read "SPLIT-8 (forced grouped by insured)". Prompt 1 |
| log1p shipped, Gini on the amount (MET-3, CLEAN-16) | consistent, reason stated | allstate_claims_severity (Lennart, 2026-10-21: "ship the target on the modelling scale, score on the original scale"). Drafts: frempl, 2015-2018, wisconsin and allstate_1m ship log1p; australian ships raw with no reason; pricing_game_2017 ships raw with a reason | The family question is australian's issue 5, which names this dataset. Builder issue 5 should point there |
| `normalized_gini` as a context metric, row form (MET-11, MET-2, MET-10) | consistent with the drafts. No curator precedent yet | diamonds (MET-11 context origin, Lennart, 2026-10-21). australian issue 4: the Gini for four tables, this one included. frempl issue 4: row or exposure-weighted, which names this one | Not stated here: exposure alone ranks at 0.212 / 0.201 / 0.161, against 0.428 / 0.417 / 0.379 for the model (builder's `measure_final.out`), about half the score. Exposure alone gets 83% of the model's score in frempl and 82% in australian; both state it. The notes give only the premium-alone baseline, and the premiums are earned, so they carry the time too. Add the number; the form is decided once in frempl issue 4 |
| `total_exposure` a feature | consistent | fremtpl2 CC (Andrej, 2026-10-20): "a feature, not a divisor" | |
| Cancelled portfolio years get exposure 1 and annual premiums (LEAK-10, LEAK-7) | departs from fremtpl2, with a fact stated. Reasonable: the rule outranks the precedent | fremtpl2 CC ("a mid-year cancellation also shortens it"). frempl (draft) followed this fix in its issue 2. australian (draft) cannot locate its cut-short years | The cut is located row by row: portfolio policies run from 1 January (89,817 of 89,882 active years at 1), and 18,784 of the 18,849 portfolio years below a year are cancelled. As published it adds 0.004-0.010 Gini. Decide with frempl issue 2. fremtpl2 then sits against LEAK-10 as amended and should be flagged (principles.md: a precedent against a rule) |
| Cancelled new-business years kept as published, `Potential leak, kept on purpose:` (LEAK-10 clause of 2026-10-26, LEAK-11) | departs from the clause as written. Not an exception (LEAK-10 is a Must): it needs the curator's case-by-case call or an amendment | onlinenewspopularity (Lennart, 2026-10-26): kept, the traced part shows no gain. distribution_transformers_at_cauca_department (Lennart, 2026-10-21): dropped, a gain may sit there. zillow_prize, melbourne_housing_market: located cells blanked. australian (draft): kept under LEAK-11, because an offset model scores the same (0.1833 against 0.1824). fremtpl2 CC: kept | The traced analog, the portfolio cancellations, gains 0.004-0.010. The offset test run here: free 0.418 / 0.409 / 0.375 against offset 0.414 / 0.384 / 0.355 (Tweedie, 3/3); mixed on new-business rows (0.419 / 0.423 / 0.337 against 0.426 / 0.408 / 0.333). So australian's fact does not transfer. Blanking marks the cancellation: 0.451 / 0.431 / 0.410. Option (c), dropping `total_exposure` only, leaves the cut in the earned premiums. Full removal scores 0.364 / 0.339 / 0.341 (-0.04 to -0.08): it strips the time on risk of 168,265 late-starting new-business years to remove a cut on 19,494. Prompt 2 |
| Year's-last-record attributes kept with a note (LEAK-10 late-pull clause) | consistent once the test is replaced. The test the note runs is the one the rule rejects | house_sales (Lennart, 2026-10-21): kept, RMSE 0.2147 masked against 0.2132. onlinenewspopularity (-0.0004 masked). zillow_prize, melbourne_housing_market (Lennart, 2026-10-21): "removing it changes no score" is no reason alone. The same point was raised on 2015-2018's `Payment` | The note's evidence is dropping `bonus_score` (< 0.001). Masking test (8,115 renewal years whose type, brand or bonus class differs from last year's record, given last year's values): 0.4309 / 0.4181 / 0.3754 against shipped 0.4277 / 0.4173 / 0.3787. With the premiums masked too: 0.4267 / 0.4151 / 0.3766, the shipped frame higher by 0.001-0.002, part of it the renewal's own repricing. Put these numbers in the note |
| `fit_reason` lists the two kept leaks after "But" (USE-8) | departs, no reason given | USE-8 as amended (Lennart, 2026-10-21; kick, homesite_quote_conversion, house_sales). australian's corrected wording ("... is a kept potential leak"). frempl and 2015-2018 (drafts) have the same slip | The fit stays approximate on the forced split alone. Prompt 3 |
| "the family's call of 2026-10-30" (negatives, exposure) | departs from the record, no reason given | Policy call 3 (Andrej, 2026-10-30): "suggest judgement calls ... for each dataset", no family convention. frempl reworded it to "the AI's suggested call of 2026-10-30" | Who decides (principles.md): an AI suggestion is not a curator's call. Reword; no decision needed |
| `policy_status` dropped (LEAK-10) | consistent | LEAK-10 Cases: "a current-status column". 2015-2018's `Lapse` and `Date_lapse` (draft) | |
| Claim counts and per-cover costs dropped (LEAK-10, parts of the target) | consistent | fremtpl2 CC (`ClaimNb`). 2015-2018, australian, frempl | |
| 49 years with zero exposure dropped (USE-7) | departs from the sibling, reason stated. The fact offered to set the two apart does not hold | spanish_motor_insurance_2015_2018 (draft) keeps 5,069 first years whose cover never started. Its precedent check, prompt 2, offers as (a) "a renewal premium, unlike the sibling's zero-premium rows" | Here the premiums are earned (annual times exposure), so a premium of 0 at exposure 0 is mechanical. In both, the cover never ran. Negligible here (49 rows, one claim of 180.11). Apply the answer to the sibling's prompt 2 here |
| `vehicle_age` and `age_driving_licence` renamed | consistent (no Cases row) | 2015-2018 derives `years_licensed` | Measured (99.92%) |
| Impossible values made missing (CLEAN-11) | consistent | 2015-2018 (licence after start, power 0). australian (value 0). churn_telco_south_asia (Tensions table) | |
| Codes labelled and categorical; ages numeric (CLEAN-12, CLEAN-14) | consistent | CLEAN-14 as amended (Lennart, 2026-10-21). 2015-2018, australian | |
| Premiums kept (USE-6, TP-4) | consistent | california_house_prices_2020 (Lennart, 2026-10-06: a natural core). 2015-2018 `Premium`. wisconsin | The model beats the premium on 3 of 3 splits |
| CICOS flat amounts kept | consistent | fremtpl2 CC (IRSA-IDA amounts kept as point masses). 2015-2018 (882). australian (200 floor). Policy call 2 | |
| 8,543 claims at zero cost kept as 0 | consistent | Policy call 2 (Andrej: "We don't care"). Apart from fremtpl2's dropped false zeros | fremtpl2's false zeros were claims with no severity row (a missing join). Here the source records 0 with the claim. Its share is flat by year (17.7%, 16.9%, 16.4% of years with claims), so no sign of unsettled 2024 claims |
| Negative-cost rows removed by the authors, nothing set | consistent | The 2026-10-30 table (AI). Policy call 8 (no requests) | |
| 26 feature copies kept (LEAK-18) | consistent | 2015-2018 (three pairs). fremtpl2 (38% repeated vectors). australian | |
| `year` a feature | consistent | 2015-2018 (`period_start`) | |
| Distinct from spanish_motor_insurance_2015_2018 (PROV-6, PROV-7) | consistent | Tensions row: a shared source with distinct tasks is not a duplicate. numerai28_6 (Lennart, 2026-10-22). Policy call 5 (no cap) | Different periods, schema and task. No shared policyholders found |
| `task_target_value_dominant` proposed, not filled in | consistent | add-dataset SKILL step 6: "stays empty: the curator fills it". frempl and australian ship it filled (their departure) | |

**Drift and amendments**

* **Andrej.** He took a temporal split on an inferred year over IID for fremtpl2 (2026-10-20). On 2026-10-30 he gave
  how_much_did_it_rain a `No` for forced IID and gave this record a `Yes` on a block that named the forced grouped
  split. No drift: his calls reject forced IID with a leak.
* **Lennart.** His SPLIT-8 cases (2026-10-21) and LEAK-10 clauses (2026-10-26) are uniform.
* **A recurring reason.** A realised time on risk is kept although it is cut after the prediction point: fremtpl2
  (CC), australian, frempl's continued records, and here. LEAK-10 is a Must, so these cannot be exceptions. One
  LEAK-10 Cases row or amendment, confirmed once, would settle all four (prompt 2 (d); the frempl and australian
  checks propose the same).

**Reflection prompts**

1. **Consistency check (AI, 2026-11-01):** the draft ships spanish_motor_insurance_coverage_level_2022_2024 grouped by
   policy, tagged `ForcedGroupedFromTemporal`: three years give one valid window, and SPLIT-14 asks for three. That
   differs from how_much_did_it_rain (`No`, 2026-10-30). You said: "if the data is temporal but a temporal split is
   not possible, we cannot split the data and reject it", and "Forced IID is to be avoided at all costs". What sets
   this case apart?
   (a) It is not forced IID. Whole policies are held out, so no test row shares an outcome with a training row. The
   valid window is measured: the Gini is 0.379, against 0.374-0.405 on the folds' 2024 rows. The split matches
   Lennart's SPLIT-8 cases (nba_players_2016_2019, open_university_learning_analytics_dataset). Your `Yes` was given
   on a block that named this split. Recorded in `splits_comment`. (b) Treat it like how_much_did_it_rain: `No`. (c)
   Reopen how_much_did_it_rain under SPLIT-8 as written. (d) Amend SPLIT-8 or SPLIT-14: ship the one valid window
   (train 2022-2023, test 2024), or make forced-from-temporal a reject. Either reaches frempl (issue 5), australian
   (issue 1), allstate_1m, pricing_game_2017 and rand.
2. **Consistency check (AI, 2026-11-01):** the draft keeps the time on risk and the earned premiums of 19,494
   cancelled new-business years as published. That differs from LEAK-10's clause of 2026-10-26 (Lennart): a late value
   stays only when its traced part shows no gain (onlinenewspopularity), and goes when a gain may sit on it
   (distribution_transformers_at_cauca_department). Here the traced part, the portfolio cancellations, gains
   0.004-0.010. A free time on risk beats an offset on 3 of 3 splits, so australian's LEAK-11 fact does not transfer.
   The keep follows your fremtpl2 call ("a mid-year cancellation also shortens it"). What sets it apart?
   (a) The cut cannot go without the legitimate time on risk. There is no start date, and blanking marks the
   cancellation (0.451 against 0.437). Full removal (exposure dropped and premiums annualised) costs 0.04-0.08 Gini
   and strips 168,265 late starts to remove a cut on 19,494. Recorded as your case-by-case call under the clause, with
   these numbers. (b) Treat it like distribution_transformers: no feature carries the realised time (0.364 / 0.339 /
   0.341). Dropping `total_exposure` alone does not do it. (c) Reopen fremtpl2 against the clause. (d) Amend LEAK-10
   for time on risk in insurance pricing: repair where the cut is located and a start value is known, else keep with
   the measured size. Decide it once with frempl issue 2 and australian issue 2.
3. **Consistency check (AI, 2026-11-01):** `fit_reason` lists the two kept leaks (the year's last record; the cut time
   on risk of new business) among the gaps. That differs from USE-8 as amended (Lennart, 2026-10-21; kick,
   homesite_quote_conversion, house_sales: a kept leak is named as kept, not as a gap) and from australian's corrected
   wording. What sets it apart?
   (a) The new-business cut is an input gap of the release (no start date), not a kept leak. Then it stays a gap, the
   last-record leak is reworded as kept, and the note label changes. (b) Reword both as kept; the fit stays
   approximate on the split. frempl and 2015-2018 would follow. (c) Reopen the USE-8 cases. (d) Amend USE-8.

**What I ran** (untuned LightGBM with the builder's settings, first three shipped splits, in
the run folder):

* `m1.py`, `m1.out`: the remnant test, zero-cost claims by year and the exposure-alone Gini;
* `m2.py`, `m2.out`: masking the last-record attributes;
* `m3.py`, `m3.out`: the offset test;
* `m4.py`, `m4.out`: option (c), as measured and with the premiums annualised.

</details>

<details><summary>Advocate</summary>

**Advocate, opening brief (AI, 2026-11-01): spanish_motor_insurance_coverage_level_2022_2024**

My position: ship this dataset. One definition fix and some text corrections are needed first. Nothing the six evidence
agents found calls for an exclusion or a changed task. The claim and column auditors say "ship after changes" and
the blind reviewer "include with changes". The split auditor calls the split "right with notes". The domain
practitioner agrees with the definition's `approximate` fit. The precedent checker finds most choices consistent and
leaves three calls to the curator. I concede the one real validity problem (point 3). Its fix is one line and costs no
score.

```text
Verdict: ship after changes.
Validity: SEL-2, USE-1, USE-5, USE-6 hold; SPLIT-8 holds (forced grouped, cost measured); LEAK-10 triggered on 13,842
  located rows, fixed by widening the mask; the unlocatable remainder (5,653 rows) and the last-record attributes are
  kept with notes under LEAK-10's clauses and LEAK-11.
Value: TP-4 holds (the model beats the premium on 3 of 3 splits); TP-2, a small real signal; MET-2, MET-3 and MET-11
  hold. The metric's reason needs rewording.
Quality: CLEAN-11, 23 zero liability premiums; one column name.
For the curator: the remainder keep (LEAK-10 clause, case by case); the row Gini or an exposure-weighted Gini
  (decide once, with frempl issue 4).
```

**1. It is a real pricing task on real insurer data, and it is worth benchmarking (P2, P3, P5, P6).**
- Use case: the article names the reuse: "This structure supports reuse in actuarial pricing, risk modelling and
  insurance research" (abstract). The actor is a Spanish motor insurer. The target is the year's claim cost, the pure
  premium the tariff charges (USE-1, USE-5, both Must). The domain practitioner: "the target is the pure premium the
  tariff charges ... it is what I act on".
- Real data: the blind reviewer, working without our notes, found strong evidence:
  - the CICOS flat amounts change each year (882 / 1,012 / 1,114, and their doubles);
  - loss ratios are 0.66 / 0.66 / 0.75;
  - property claims without a property premium occur in 2 of 12,526 cases.
  Andrej's CC (2026-10-30) is `Yes`, priority 4.
- Value:
  - Not trivial (TP-4, Must). The total premium alone ranks at 0.396 / 0.388 / 0.344. Untuned LightGBM on all features
    ranks at 0.428 / 0.417 / 0.379 and beats it on 3 of 3 splits.
  - It refines the tariff. Against the insurer's own premium, the model's ordered-Lorenz Gini is 0.13-0.15, while the
    premium itself scores about 0 (domain practitioner).
  - Every fold can be scored (MET-2). Each test fold has 13,817-14,344 positive rows. A constant scores 0.000 and the
    truth 1.000 on 9 of 9 folds.
- Objections it answers:
  - "Low signal; near-ties expected" (blind reviewer #2). TP-2 (Should) says a small but real signal is no reason to
    retire. A claim is ranked at AUC 0.70-0.71, which is what personal-lines data looks like.
  - "It ranks through the premium" (domain practitioner). USE-6 (Must, P3) says the company's own price is a
    legitimate input that the model refines.

**2. The split is the one the rules prescribe, and its cost is measured (P4; SPLIT-8, Must, narrows SPLIT-14 and USE-10).**
- One window only. Training on 2022-2023 to test 2024 keeps 52.5% of the rows for training. A 2023 window trains on
  19.0%, under SPLIT-14's floor of 50%. 117,926 of the 185,677 policies recur, so SPLIT-8 names the regime: "grouped by
  the entity when the periods are stacked and the entities recur across them".
- The split auditor reproduced the cost:
  - the valid window scores 0.379 (SE 0.022), against 0.405 / 0.374 / 0.377 on the folds' 2024 rows;
  - an IID split scores the same as the grouped one (mean 0.408 against 0.408);
  - the pooled Gini is never above the mean of the within-year Ginis;
  - 2024 labels are mature (0.302 / 0.305 / 0.312 claims per exposure-year).
- Precedent: SPLIT-8's case open_university_learning_analytics_dataset (Lennart, 2026-10-21; too few periods).
  Andrej gave his `Yes` on a block that named "SPLIT-8 (forced grouped by insured)".
- Against how_much_did_it_rain (`No`): that case was forced IID, which Andrej rejected ("Forced IID is to be avoided at
  all costs"). Here whole policies are held out, so no test row shares an outcome with a training row. Option (a) of
  the precedent checker's prompt 1 states this, and it should go into `splits_comment`.
- I concede that "69% ... a customer the insurer has not seen before" is wrong: 52.4% of the rows are a policy's first
  year. The fix is the text only (`split`, `grouping.definition`). The regime still stands, for two reasons:
  - SPLIT-8 narrows USE-10, so with one window the forced grouped split is the rule's answer;
  - the history that a known-entity framing would add, last year's claim, is worth only +0.007 to +0.013 Gini on
    renewal rows (domain practitioner).
- A one-window temporal split, which the blind reviewer suggested, fails SPLIT-14 (Must). Independent failures are not
  conflicts.

**3. I concede the located leak (P4, LEAK-10 Must; LEAK-7). The fix keeps the dataset and costs nothing.**
- 13,842 cancelled new-business years (3.9% of the rows) belong to policies already in force on 1 January. Of the
  47,411 active carried-over years, 47,403 have exposure 1. Below a year therefore means cancelled, exactly as for the
  portfolio rows the definition already fixes. Three auditors and the practitioner found this independently.
- Mildest remedy (fix the definition, LEAK-7): widen `late` in `_clean` step 4 to cancelled rows whose policy has a
  row the year before. The column and split auditors give the code; years are consecutive, so the two masks agree.
  Then correct `known`, `changes`, `fit_reason`, the "Potential leak, kept on purpose" bullet and decision 3.
- What the fix costs: overall Gini 0.426 / 0.412 / 0.399 against 0.428 / 0.417 / 0.379 shipped (claim auditor). Over
  9 splits it goes from 0.4072 to 0.4122 (column auditor).
- Tensions table, "a real task against a leak": fix the leak and keep the task. Nothing here is an irreversible
  transform (LEAK-27), so exclusion is off the ladder.

**4. The leaks that remain after the fix are weak, and LEAK-10's own clauses keep them (P4; LEAK-10 clauses of 2026-10-26, LEAK-11 Should).**
- Last record of the year. The clause keeps values that cannot be located when the traced part shows no gain. Here it
  shows none:
  - reverting the 12,855 changed vehicle cells to the previous year's values scores 0.4090, against 0.4079 shipped
    (column auditor);
  - masking type, brand and bonus on 8,115 renewal years scores 0.4309 / 0.4181 / 0.3754, against 0.4277 / 0.4173 /
    0.3787 (precedent checker). With the premiums masked too, the shipped frame is higher by 0.001-0.002, part of
    which is the renewal's own repricing.
  - Precedents: onlinenewspopularity, house_sales. Remedy: replace the note's drop-`bonus_score` test with these
    masking numbers and name the vehicle columns.
- The 5,653 first-year new-business cancellations (1.6% of the rows). They cannot be located: 168,265 new-business
  years start late, and nothing tells a late start from a cut.
  - Removing the cut means dropping the exposure and annualising the premiums of every one of those years. That costs
    0.04-0.08 Gini (0.364 / 0.339 / 0.341) and strips a period known at pricing from 168,265 rows. Andrej's fremtpl2
    call says exposure is "a feature, not a divisor".
  - Blanking marks the cancellation (0.451 / 0.431 / 0.410).
  - On the traceable analog, the 13,842 carried-over rows, the cut lowers the declared metric: the Gini on those rows
    is 0.333 / 0.376 / 0.248 with the cut and 0.346 / 0.376 / 0.321 without it. That fits LEAK-11.
  - I concede two numbers on the other side. The cut lifts the claim AUC on those rows by 0.03-0.04 (split auditor).
    The portfolio cut added 0.004-0.010, measured on an earlier frame (EV-8).
  - So the clause makes this the curator's case-by-case call. The evidence favours option (a) of the precedent
    checker's prompt 2, recorded with these numbers.
- The annualised premiums leave a trace: cancellation is ranked at AUC 0.77 among portfolio rows. That trace is worth
  about 0.001 Gini, and the Gini on portfolio rows does not move when the premiums are rounded. Remedy: a
  `Potential leak, kept on purpose:` note. Rounding to whole euros, as frempl rounded its exposure, is the cheap
  alternative.

**5. The metric holds; only its reason needs rewording (P6; MET-11 Must, MET-3 Must, MET-2 Must).**
- The source defines no metric (the article was read in full; claim #27). The task makes one obvious: insurers' own
  competitions ranked risks by the normalized Gini, and Allstate 2011 used this row form. So `context` is the right
  origin (diamonds).
- The target ships as log1p and is scored on the amount. That is Lennart's MET-3 rule ("ship the target on the
  modelling scale, score on the original scale").
- The domain practitioner prefers an exposure-weighted Gini. On 3 of 3 folds it ranks the predictors in the same
  order (log1p, then Tweedie, then the premium; claim #32). The library has no such metric (MET-12, MET-13). Frempl
  and australian face the same choice: decide it once in frempl issue 4, and treat like cases alike.
- I concede the reason's wording. Frees et al. and Liberty Mutual used weighted Ginis. The reason should also state
  that exposure alone scores 0.17-0.23, as frempl and australian state it. Remedy: reword (MET-11). The metric stays.

**6. The cleaning is what an expert would ship, and the leftovers are cheap (P7; CLEAN-11 Should, Tensions "P3 over P7").**
- Every auditor confirmed the age rename (the driver age is the sum on 99.92% of rows). Without it the release would
  call the years licensed a vehicle age.
- Also confirmed:
  - the parts of the target and `policy_status` are dropped;
  - 34 + 3 impossible values are made missing;
  - the CICOS amounts are kept (fremtpl2's IRSA amounts);
  - the 26 feature copies are kept (LEAK-18);
  - `insured_id` is used only as the group (LEAK-33).
- Leftovers, each a one-line change:
  - mask the 23 zero liability premiums (a compulsory cover);
  - rename `power_to_weight_ratio`, which holds kg per hp;
  - optionally set to 0 the 11 positive targets below 1 EUR (the smallest is 6.5e-14, the blind reviewer's float
    residue).
- None of these changes what the target means, so they are quality items, fixed when cheap (principles, step 3).

**7. The rest is wording. It changes no data and no verdict (PROV-16 Must for the quote; USE-8; EV-8; who decides).**
- Quote the negative-cost sentence in full: "excluded from the aggregation of total_incurred". No rows were removed.
  Reword the warning's reason: "closed at no cost" becomes "maybe net-negative claims set to 0", with the 35.8%
  third-party property figure. Policy call 2 makes coded zeros no reason for a `No`.
- `fit_reason`: name the two kept leaks as kept. The fit stays `approximate` because of the split (USE-8).
- "The family's call of 2026-10-30" becomes "the AI's suggested call".
- Re-run or label the numbers from measure1-3 (EV-8).
- Set the record's `required_split` to grouped.
- Each of these is a text fix of the lowest kind. None is a reason to hold the dataset back.

</details>

<details><summary>Critic</summary>

**Critic, opening brief (critic, 2026-11-01): spanish_motor_insurance_coverage_level_2022_2024**

Verdict: **ship after changes**. I do not ask for exclusion. The task is real (USE-1, USE-6). The split is the one
SPLIT-8 prescribes, and every Must below can be fixed in the definition or its texts. But one leak fix stops short of
rows that the definition's own evidence locates, and several statements the dataset makes about itself are false.

```text
Verdict: ship after changes.
Validity: USE-10 split stands, texts misstate it (fix text); USE-8 wording departs (fix text); LEAK-10 triggered,
  partly fixed, 13,842 rows left (fix the definition); LEAK-10 second clause: three kept-leak notes rest on the wrong
  test or overstate, one curator call; PROV-16 quote cut (fix notes, record, warning reason).
Value: MET-11 / MET-2 reason miscited and incomplete (fix the reason; the form is decided with frempl issue 4).
Quality: EV-8 stale numbers; an AI suggestion written as a decision; CLEAN-11 23 zero liability premiums; a
  reversed column name.
```

I recounted the load-bearing counts on the raw file (inline run): 61,253 carried-over NB rows,
13,842 of them cancelled and all below a year, 47,403 of 47,411 active ones at exposure 1, 5,653 first-year NB
cancellations, 52.4% first rows, 62.7% of 2024 rows with an earlier year, 23 zero liability premiums.

**1. The test does not stand for "most of them new customers" (P3, USE-10 Must; SPLIT-8 Must, its "say what a dated
window would change").**
- Problem: `task_summary.split` says "most of them new customers". `grouping.definition` says "69% of the
  policy-years are new business, a customer the insurer has not seen before". The NB flag stays on through a policy's
  second calendar year.
- Evidence: 25% of NB rows (61,253) follow a row of the same policy. 52.4% of rows are a policy's first row. In 2024,
  62.7% of rows are policies already in the book (claim auditor #4, split auditor issue 2, domain practitioner).
- Effect: the insurer's next-year book is mostly renewals, for which it holds last year's claims, while the shipped
  task is cold start for every row. The measured cost is small: last year's outcome adds +0.007 to +0.013 Gini on
  renewal rows (domain practitioner). The regime stands: SPLIT-8 narrows USE-10, and IID scores the same as grouped
  (0.408 vs 0.408).
- Remedy (text): correct both figures. In `splits_comment`, say what a dated window would change: renewals would
  carry last year's claims, and the pooled score (mean 0.408) mixes years, where the one valid window scores 0.379
  (split auditor 3a). Write down what sets this apart from how_much_did_it_rain (`No`, 2026-10-30, "Forced IID is to
  be avoided at all costs"): it is not IID, whole policies are held out, and the window cost is measured (precedent
  checker, prompt 1).

**2. `fit_reason` counts kept leaks as gaps (P3, USE-8 Must, as amended 2026-10-21).**
- Problem: after "But", it lists the year's last record and the cut time on risk of cancelled new policies as the
  gaps.
- Evidence: under USE-8 a potential leak kept on purpose is named "in `fit_reason` as kept, not as a gap" (kick,
  homesite_quote_conversion, house_sales; australian's corrected wording; precedent checker, prompt 3). After point 3,
  the second clause is also wrong for 13,842 rows.
- Remedy (text): the fit is approximate because held-out policies of the same years stand in for next year's book.
  Name the last record and the first-year NB cut as kept potential leaks.

**3. The cancellation fix misses 13,842 policy-years that the same evidence locates (P4, LEAK-10 Must, its
located-cells clause; LEAK-7; LEAK-5).**
- Problem: `_clean` step 4 restores a full year and the annual premiums only where `business_type == "P"`. But a
  policy in its second calendar year is in force from 1 January whatever its flag.
- Evidence: among the 61,253 carried-over NB rows, 47,403 of the 47,411 active ones have exposure 1, and all 13,842
  cancelled ones (6,434 in 2023, 7,408 in 2024) are below a year. They claim 0.478 times per exposure-year, against
  0.285. Within these rows the shipped features separate cancelled from active at ROC AUC 1.000 (column auditor). The
  claim, column and split auditors and the domain practitioner found this independently; the blind reviewer flagged
  the same inconsistency.
- Effect: 3.9% of rows ship a value known only when the policy ends. Three texts are false: `known` ("a full year for
  a policy carried over from the year before"), the note "a cut cannot be told from a late start" (true for 5,653 of
  19,495) and `fit_reason`. The pooled score barely moves (9 splits: 0.4072 shipped, 0.4122 fixed; column auditor).
  But on its own rows the cut carries claim signal: claim AUC 0.695 / 0.681 / 0.691 shipped against 0.654 / 0.640 /
  0.662 fixed (split auditor).
- Rule: LEAK-10's second clause (2026-10-26): late cells that can be located go. The zillow_prize and
  melbourne_housing_market row: a value is "not kept merely because removing it changes no score (no LEAK-11 keep)".
  LEAK-5: never "models would predict the same". LEAK-11 (a Should) does not save it either: whether the cut weakens
  the signal is mixed (the Gini on these rows rises with the fix, 0.248 to 0.321 on one fold; the claim AUC falls).
  Treat like cases alike: the definition already fixes the portfolio rows on the same mechanism.
- Remedy (fix the definition): `carried = df.groupby("insured_id")["year"].transform("min") < df["year"]` and
  `late = df["policy_status"].eq("C") & (df["business_type"].eq("P") | carried)`. Then update `known`, `changes`
  ("cancelled renewals"), the note, decision 3's table (split by first year) and `fit_reason`.

**4. The kept potential leaks need the right test, the right numbers and one curator call (P4, LEAK-10 second clause,
case by case; LEAK-6).**
- (a) The 5,653 first-year NB cancellations cannot be located. The clause keeps such values "only when the part that
  can be traced shows none" (no gain). The traced part does show some: the portfolio rows add +0.004 to +0.010 as
  published (from an earlier frame, see point 7), and the carried NB rows 0.03-0.04 claim AUC. Full removal costs 0.04
  to 0.08 Gini and strips the time on risk of 168,265 legitimate late starts (precedent checker, m3 and m4). So the
  keep needs the curator's case-by-case call with these numbers; an AI "kept on purpose" is not enough. The same reason
  now recurs in fremtpl2, australian, frempl and here: one LEAK-10 Cases row or amendment would settle all four.
- (b) The annualised premiums still mark cancelled portfolio years. From the shipped features, cancellation is ranked
  at ROC AUC 0.772-0.778, against 0.62 without premiums and 0.685 with them rounded to euros. The trace is worth about
  0.001 Gini (column auditor issue 2, claim auditor #20). "The values known when the year started" overstates: an
  active year blends in the renewal tariff, which moves with claims (+0.65% vs -0.07%). Remedy: a corrected
  `Potential leak, kept on purpose:` note with these numbers. Rounding to euros (as frempl rounded its exposure) is
  the curator's option.
- (c) The last-record note rests on dropping `bonus_score` ("less than 0.001"; refuted, -0.0018 on one fold of an
  earlier frame). The clause rejects that test on its own. Masking the changed cells shows no gain: 0.4309 / 0.4181 /
  0.3754 masked against 0.4277 / 0.4173 / 0.3787 shipped (precedent checker, m2), and 0.4090 against 0.4079 for the
  vehicle cells (column auditor issue 3). Remedy: replace the evidence with the masking numbers, and name the vehicle
  columns (the value changes in 3.06% of years with a claim against 2.07%).

**5. The negative-cost quote is cut, and no rows were removed (P5, PROV-16 Must).**
- Problem: the notes quote "observations presenting negative incurred values were therefore excluded" and conclude
  "the release holds no negative cost and no recoveries". The record's Assessment and prose say the authors "left out
  rows with negative incurred amounts".
- Evidence: Experimental Design (read in the article's text) continues "...excluded from the aggregation of
  total_incurred". The last-record step alone "reduced [the rows] to 354,140", the release size. A zero cost with a
  claim sits on one cover: 10,778 of the 30,099 third-party property claims (35.8%), against at most 1.5% on the
  others. That is where CICOS recoveries can exceed payments (claim auditor #8, #9; a maybe, EV-6).
- Effect: some target zeros may be net-negative claims set to 0, not "claims closed at no cost". It is small, but it
  concerns what the target's zeros mean (Tensions: a cleaning gap that changes the target's meaning is P3/P5). We
  cannot repair it: the raw rows are on request, and the policy calls make no data requests.
- Remedy (a note): quote the full sentence and drop "no rows" and "no recoveries"; give the 35.8% as a maybe. In the
  proposed warning reason, "claims closed at no cost" becomes "claims recorded at zero cost". Correct the record's
  Assessment line.

**6. The metric's reason miscites its context and leaves out the exposure floor (P6, MET-11 Must; MET-2 Must, third
bullet).**
- Problem: the reason says insurers compare models "by the Gini index of the ordered Lorenz curve of losses (Frees,
  Meyers and Cummings 2011)", "the metric the insurers' own Kaggle competitions chose (Allstate 2011, Liberty Mutual
  2014)".
- Evidence: Frees et al. order by the relativity to the premium and accumulate premium. Liberty Mutual scored a Gini
  weighted by `var11`. Only Allstate 2011 scored this row Gini, on whole vehicle-years (claim auditor #28). Here 53%
  of the rows are below a full year, and exposure alone scores 0.168-0.228 over 9 folds, about half the model's
  0.379-0.428 (claim auditor #32). frempl and australian state their exposure-only score.
- Effect: in its context the metric scored full years. On this data the row Gini also pays for predicting time on
  risk. The exposure-weighted Gini ranks the tested predictors the same on 3 of 3 folds (claim auditor). But the
  premium-base Gini flips log1p against Tweedie on 3 of 3 (domain practitioner), so the form matters.
- Remedy (fix the reason): reword as frempl and australian do. State the exposure-only score, and that the Gini scores
  neither the level nor the spread. Decide the form (row, exposure-weighted, premium base) once with frempl issue 4. I
  do not ask for a different metric here.

**7. Numbers from earlier frames, an AI suggestion written as a decision, two cheap cleanings (EV-8; principles.md,
"Who decides"; P7, CLEAN-11 Should).**
- EV-8: three numbers come from measure1-3, frames before the final cleaning: +0.005 to 0.028 (status), +0.004 to
  0.010 (the portfolio fix) and the bonus drop. The premium move (+0.6% vs -0.1%) did not reproduce (+1.4% vs +0.4%).
  The R^2 range -0.011 to -0.003 mixes two fits (claim auditor #13, #20, #23, #29). Remedy: re-run them on the shipped
  frame, or name the frame.
- "the family's call of 2026-10-30" (twice) presents an AI suggestion as a decision. Andrej asked for a call per
  dataset (policy call 3; precedent checker). Remedy: "the AI's suggested call of 2026-10-30", as frempl has it.
- CLEAN-11: `liability_premium` is 0 on 23 rows of policies with other covers. The cover is compulsory, and the
  article says the premiums were checked "strictly positive". Remedy: mask them to missing. `power_to_weight_ratio`
  holds kg per hp (Table 2: "weight-to-power ratio"): rename it, or say so (column auditor 6).
- These are quality points. None is a reason to hold the dataset.

**Not argued.** Exclusion. The forced grouped split itself (SPLIT-8; IID = grouped; the window cost is measured). The
total over seven covers (fremtpl2 CC). log1p shipped and scored on the amount (MET-3). Exposure as a feature
(fremtpl2 CC). The premiums as inputs (USE-6; the model beats them on 3 of 3, TP-4). The weak severity signal (TP-2).

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate, rebuttal (AI, 2026-11-01): spanish_motor_insurance_coverage_level_2022_2024**

The critic and I agree on the verdict: ship after changes, no exclusion. We also agree on every remedy. I concede
points 1, 2, 3, 4(b), 4(c), 6 and 7. I narrow point 5. On point 4(a) I ran the check that decides it, and it goes
against my opening brief. I withdraw my claim that the kept new-business cut "fits LEAK-11".

The check: untuned LightGBM (200 trees, lr 0.05, 31 leaves), log1p target, `normalized_gini` on the amount, all 9
shipped splits. The frame is the shipped definition's, cached by the column auditor after the last edit of
`dataset.py`. Scripts and outputs are in the run folder (`traced_gain.py/.out`,
`firstyear_readable.py/.out`).

| frame | portfolio cancelled years (18,784) | carried-over NB cancelled years (13,842) | mean Gini, 9 splits |
|---|---|---|---|
| F, the critic's fix | fixed | fixed | 0.4122 |
| S, shipped | fixed | as published | 0.4072 |
| P | as published | fixed | 0.4205 |
| N | as published | as published | 0.4142 |

**1. "Most of them new customers" (USE-10, SPLIT-8). Concede.** The figure is wrong: 52.4% of the rows are a
policy's first year, and 62.7% of 2024's rows were in the book before. The regime still stands, and we agree on why:
SPLIT-8 narrows USE-10, and IID scores the same as grouped. What follows is text only:
- correct the figure in `split` and `grouping.definition`;
- in `splits_comment`, say that renewals would carry last year's claims under a dated window, and that the pooled
  0.408 mixes years where the window scores 0.379;
- write down what sets this apart from how_much_did_it_rain.

**2. `fit_reason` (USE-8). Concede.** The fit is `approximate` because of the split alone. Name the last record and
the first-year cut as kept potential leaks. If the curator removes the cut instead (see 4(a)), that is "a task changed
a lot to avoid a leak", so the fit stays `approximate` either way.

**3. The 13,842 located rows (LEAK-10 Must, LEAK-7). Concede, as in my opening.** No LEAK-11 keep is possible for
located cells; the zillow_prize and melbourne_housing_market row says so. My run confirms the fix on the shipped frame:
- 0.4072 shipped against 0.4122 fixed (S - F = -0.0050, SE 0.0029; F is higher on 6 of 9 splits);
- on the traced rows, the frame with the cut scores 0.033 lower.

Adopt the critic's mask and the five text updates.

**4(a). The 5,653 unlocatable first-year cancellations (LEAK-10 second clause, LEAK-6). Concede the rule point;
narrow the weight.** The new facts:
- The traced portfolio part shows a gain on the shipped frame. Leaving those cells as published raises the Gini from
  0.4122 to 0.4205 (P - F = +0.0083, SE 0.0019, higher on 8 of 9 splits). This replaces the builder's +0.004 to
  +0.010 from measure2 (EV-8).
- The remainder's cut is partly readable. Among the 184,172 first-year new-business rows, cancellation is ranked at
  AUC 0.857-0.867 with all features, 0.760-0.773 without exposure and premiums, and 0.75-0.76 from exposure alone.
  The published portfolio cut reads at 1.000.

So "keep only when the traceable part shows none" is not met, and the keep cannot be written as a default under the
clause. It needs the curator's case-by-case call, or the LEAK-10 amendment for time on risk that the critic and the
precedent checker propose. That amendment would settle fremtpl2, australian, frempl and this dataset at once.

Where I narrow:
- Not every traced part gains. The carried-over NB cut, which the model cannot tell from a late start, loses 0.005
  (S - F). The remainder is also cut new business with no flag that singles it out.
- Its readability (0.86 against 0.77 without exposure and premiums) is well below the portfolio's 1.000.
- It covers 1.6% of the rows, against the portfolio's 5.3%.
- Inference, not measured: any gain that sits on it should be well below the portfolio's +0.008.
- The only full removal costs 0.04-0.08 Gini (0.364 / 0.339 / 0.341). It takes a period known at pricing from
  168,265 late starts, against the fremtpl2 call that exposure is "a feature, not a divisor".

By the remedy ladder, the choice is between a keep with these numbers (the curator's call) and that large change.
Exclusion is not on the table. I still recommend the keep, but as the curator's decision, not the AI's.

**4(b). Annualised premiums. Concede.** This is the same remedy I proposed: a corrected `Potential leak, kept on
purpose:` note with AUC 0.772-0.778 against 0.685 rounded, and "values known when the year started" reworded.
Rounding to euros is the curator's option.

**4(c). Last-record note. Concede.** Replace the drop-`bonus_score` test with the masking numbers and name the vehicle
columns. This is my opening point 4.

**5. Negative costs (PROV-16 Must). Concede the quote and the texts; narrow the "target's meaning" claim.**
- Quote the full sentence ("...excluded from the aggregation of total_incurred"). Drop "no rows" and "no recoveries".
  Correct the record's Assessment and prose, and change "closed at no cost" to "recorded at zero cost" in the
  warning's reason.
- I dispute that this is a P3/P5 question (the Tensions row on a cleaning gap that changes what the target means).
  Under both readings, a zero means no net claim cost to the insurer in that year for that cover:
  - a claim closed at 0;
  - a recovery that exceeded the payment, left out of the sum.
  frempl does exactly this with its negative amounts ("no net claim cost to the period"), and so does the 2026-10-30
  suggestion table ("set to 0 where they are recoveries").
- The values are identical either way, so the target and the Gini do not change. The 35.8% figure is a maybe (EV-6).
- What follows is a PROV-16 text fix, with no change to the data.

**6. The metric's reason (MET-11, MET-2). Concede.** Reword it as frempl and australian do, and state the
exposure-only score (0.168-0.228) and that the Gini scores neither the level nor the spread. Decide the form once,
with frempl issue 4. One narrowing on weight: the premium-base flip between log1p and Tweedie is 0.003-0.007 per
split, and the exposure-weighted Gini keeps the order on 3 of 3 folds. Neither of us asks for another metric here.

**7. EV-8, "the family's call", CLEAN-11, the column name. Concede all.** One stale number is now replaced on the
shipped frame: the portfolio fix's +0.0083 (point 4(a) above). The others should be re-run or labelled with their
frame.

**What is left for the curator:** one call, the 5,653-row keep under LEAK-10's second clause (or an amendment), with
both sides' numbers above. Everything else is a fix to the definition or its text that the critic and I both accept.

</details>

<details><summary>Critic rebuttal</summary>

**Critic, rebuttal (critic, 2026-11-01): spanish_motor_insurance_coverage_level_2022_2024**

My verdict stands: **ship after changes**. The advocate and I now agree on the verdict, on the one definition fix and
on nearly every text fix. One new check (below) settles the point where we differed, the 5,653 unlocatable
cancellations: I concede it. I dispute two small items of the advocate's (the 11 "float residue" targets, and the
omission of SPLIT-8's dated-window sentence), and I add three text items the advocate's list leaves out.

**New fact: what the cut time on risk is worth where it can be traced.** I scored all 9 shipped splits (untuned
LightGBM with the builder's settings, normalized Gini on the amount). The variants were the proposed fix (F, portfolio
and carried-over NB cancellations annualised), the shipped definition (S, portfolio only) and both traced groups as
published (U). Script and output, in the run folder: `traced_gain.py` and `traced_gain.out`.

| cut left in | pooled Gini change | on its own rows | splits up |
|---|---|---|---|
| carried-over NB cancellations (S - F) | -0.0050 (SE 0.0029) | -0.0294 (SE 0.0094): 0.3219 vs 0.3512 | 3 of 9 pooled, 1 of 9 on its rows |
| portfolio cancellations (U - S) | +0.0071 (SE 0.0015) | - | 8 of 9 |

So the two traced cuts behave differently. A portfolio row starts on 1 January by its flag, so a cut there tells the
model the policy was cancelled, and the model gains from it. Among NB rows a short exposure looks like a late start,
so the cut misleads the model, and the model loses by it.

**Advocate 1 (a real pricing task, worth benchmarking): concede.** I never disputed it. USE-1, USE-5 and USE-6 hold,
and the task is not trivial (TP-4, the model beats the premium on 3 of 3 splits). The weak severity signal is no
reason to retire (TP-2).

**Advocate 2 (the split): concede the regime; narrow the text fix.**
- Agreed: forced grouped under SPLIT-8, the "69%" text corrected, and the how_much_did_it_rain distinction written
  into `splits_comment`.
- Held: SPLIT-8 (Must) also says to "say what the timestamp or a dated window would change". The advocate's fix
  leaves that out. Two clauses would cover it:
  - renewals would carry last year's claims (+0.007 to +0.013 Gini on those rows, domain practitioner);
  - the pooled score (mean 0.408) mixes years, while the valid window scores 0.379 (split auditor 3a).
  This is text only.

**Advocate 3 (the located leak): concede; we agree.** My check backs "costs nothing": with the fix the pooled Gini is
0.4122 against 0.4072 shipped (+0.005, SE 0.003). The fix holds under LEAK-10's located-cells clause whatever the
score does (LEAK-5).

**Advocate 4 (the remaining leaks): concede, with the numbers it needs.**
- The 5,653 first-year NB cancellations: concede option (a), keep with a note, as the curator's case-by-case call.
  - Why: LEAK-10's second clause compares a value that cannot be located with the part that can be traced. The closest
    traced part is the carried-over NB rows: the same flag, and to the model the same look as a late start. There the
    cut loses on the declared metric (-0.029 on its rows, 8 of 9 splits down).
  - This withdraws my point 4(a). That point leaned on the portfolio gain, which is real (+0.007, 8 of 9) but rests on
    a flag the 5,653 rows do not have. It also leaned on the claim AUC, which is not the declared metric.
  - What the note needs: both rows of the table above, and the cost of full removal (0.04 to 0.08 Gini; it strips
    the time on risk of 168,265 late starts).
  - Optional, for the curator: one LEAK-10 Cases row would settle the same time-on-risk question in fremtpl2,
    australian and frempl (precedent checker).
- The last record: agreed. Replace the note's drop-`bonus_score` test with the masking numbers, and name the vehicle
  columns.
- The annualised premiums: agreed (a `Potential leak, kept on purpose:` note; rounding to euros is the curator's
  option). Held as a text fix: "the values known when the year started" overstates. An active year blends in the
  renewal tariff, which moves with claims (+0.65% against -0.07%, column auditor 2).

**Advocate 5 (the metric): concede the metric; narrow "MET-2 holds".**
- I asked for no metric change, and both briefs send the form to frempl issue 4.
- The advocate's "Allstate 2011 used this row form" is true only on rows of whole vehicle-years (claim auditor #28).
  Here 53% of rows are part-years, and exposure alone scores 0.168-0.228 over 9 folds.
- So MET-2's third bullet (the metric means here what it meant at the source) holds only once the reason says so.
  The advocate already concedes stating the exposure-only score. The reason should also say that the row form was
  scored on full years.

**Advocate 6 (cleaning): concede, except the 11 targets.**
- Agreed: mask the 23 zero liability premiums (CLEAN-11) and rename `power_to_weight_ratio`.
- Disputed: "set to 0 the 11 positive targets below 1 EUR (float residue)". I read the 11 rows in the raw file:
  - one is 6.5e-14, which is residue;
  - the other ten are 0.0115, 0.023, 0.0345, 0.115 and 0.529, nine of them multiples of 0.0115, all with a recorded
    claim.
  These are recorded amounts, small but not impossible, and CLEAN-11 keeps values that are "only unusual". At most the
  one 6.5e-14 row may go to 0. It changes no score, so I would leave it.

**Advocate 7 (wording): concede, with three additions.**
- The record's `required_split` and tag become grouped: concede. records.md says that once a definition exists the
  field "holds its regime" and the tags agree with it. That house rule settles the split auditor's hesitation.
- The warning's reason: agreed in substance. Suggested wording: "claims recorded at zero cost; some may be
  net-negative claims set to 0 (maybe; 35.8% of third-party property claims)".
- Additions the advocate's list leaves out:
  - the record's Assessment line and prose repeat "left out rows with negative incurred amounts" (PROV-16, Must) and
    need the same correction as the notes;
  - EV-8: the portfolio gain is now measured on the shipped frame (+0.0071, SE 0.0015, 8 of 9). That number can
    replace the "+0.004 to 0.010" of measure2;
  - the "values known when the year started" fix above.

**Agreed changes, for the mediator:**
1. Widen the mask in `_clean` step 4 (LEAK-10), and correct `known`, `changes`, the note, decision 3 and `fit_reason`
   (USE-8).
2. Correct the "69%" texts. Add SPLIT-8's dated-window sentence and the how_much_did_it_rain distinction.
3. Rewrite the kept-leak notes with the measured numbers: the masking test, the premium trace, and the table above for
   the 5,653 rows (the curator's call).
4. Quote PROV-16 in full in the notes, the warning's reason and the record.
5. Reword the metric's reason (MET-11, MET-2).
6. EV-8 re-runs; "the AI's suggested call"; the 23 premiums; the rename; `required_split`.

**Left for the curator:** the 5,653 keep (the evidence favours (a)); rounding the premiums; the metric form, decided
with frempl issue 4.

</details>
