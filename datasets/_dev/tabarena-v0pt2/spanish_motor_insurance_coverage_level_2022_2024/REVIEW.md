# spanish_motor_insurance_coverage_level_2022_2024

**Outcome:** added. The AI recommends shipping it: the annualised premiums are now rounded to the cent (issue 7,
Lennart, 2026-11-08), since the re-review panel of 2026-11-06 under the exposure rules (LEAK-41, MET-14 to MET-16) found
that their decimals told a year cut short from a full one. Like every container with a
`sample_weight`, it enters no run before the collection's training-weight gate (`BENCHMARK_CHANGES_TODO.md`, "Training
weights", "The gate"). The motor portfolio of an unnamed Spanish insurer (Espinosa, Lledó and Atance, Data in Brief
66:112883, 2026; Mendeley, CC BY 4.0): 354,091 policy-years of 185,677 policies, 2022 to 2024, with the premium of each
cover. The target is the year's claim cost over all seven covers, paid plus reserved (0 for 88.1%), per year on risk,
shipped as log1p and scored on the cost per year by the normalized Gini weighted by the time on risk (a context metric);
the time on risk is also each policy-year's training weight, and all years of a policy stay on one side of the split.
Validity: SEL-1 and SEL-2 hold; USE-1, USE-5 and USE-6 hold, fit approximate on the forced split (USE-8); LEAK-10
triggered and fixed (`policy_status` and the target's parts dropped); LEAK-41 holds for the weight (`actual_exposure` is
the rate's denominator, the metric's weight and the `sample_weight`, never a feature; `total_exposure` dropped; every
premium annualised and rounded to the cent; probe 22, re-run on 2026-11-08, fits the time on risk from the features at
R^2 0.340 and finds no feature whose gain goes through it under weighted Tweedie or L2; 1/time on risk alone scores
0.075) and was triggered by the unrounded premiums' decimals, which ranked the located cancellations at ROC AUC 0.965
and gained +0.0035 under weighted Tweedie when a model read them, fixed by the cent rounding (issue 7: 0.565 and
+0.0001 after, at no measurable cost); LEAK-41's report now covers
`business_type`, read from the year's last record (no gain against its 1 January value); the two weaker late values stay
with notes (issue 4), and the premiums' gain through any cancellation, +0.0010 under Tweedie with 10 seeds (SE 0.0006),
keeps option A of issue 6; SPLIT-8 ships the three years as `ForcedGroupedFromTemporal` (Andrej, 2026-11-02), its cost
and leak test re-measured: the 2024 window scores 0.300 to 0.316 against means of 0.309 and 0.311 on the folds' 2024
rows, and a model that sees the test year's own training rows gains +0.0045 to +0.010 pooled, within each year and
carried by no column; SPLIT-24 holds (no policy on both sides of any split); PROV-6 and PROV-7: distinct from
spanish_motor_insurance_2015_2018 (other years, schema and task, no shared policyholders found); PROV-16 holds once the
metric reason's citations were corrected. Value: TP-2, a small real signal: untuned LightGBM weighted by the time on
risk scores 0.3166 (L2 on log1p) and 0.3165 (Tweedie) on the declared metric against the dummy's 0, and the task probe
raises no flag (its R^2-type skill is +0.048); TP-4 holds: the model beats the insurer's annual premium alone (0.298) on
9 of 9 splits with L2 and 8 of 9 with Tweedie; MET-11 (context), MET-14 and MET-15 hold; MET-16 does not apply (no
survey weight). Quality: CLEAN-11 holds (impossible values made missing, including 23 zero premiums of the compulsory
liability cover); CLEAN-14 departed from and fixed (`bonus_score` and `payment_frequency` are now ordered, the second
on issue 8);
CLEAN-16 holds (the log1p scale kept on Lennart's call of 2026-11-06, at no measured cost). Weighed: recent real insurer
data with costs and premiums per cover +, a data article with a variable table +, size +; core rating factors absent
(vehicle age, postcode) -, low signal -, unnamed insurer -. Nothing is left open: issues 7 and 8 were settled on
2026-11-08 (Lennart).

Changes made after the review panel (AI, 2026-11-01): the full-year fix now also covers the 13,842 cancelled
new-business years of policies already in force on 1 January (they had a row the year before), which lowers no score
(the Gini rises from 0.408 to 0.412, 9 splits); the 23 zero liability premiums are missing; the texts that called 69% of
the rows new customers now say 52.4% are a policy's first year; `power_to_weight_ratio` renamed `weight_to_power_ratio`
(it holds kg per horsepower); a note that nearly every claim amount sits on a grid of 0.0115 (a cent times 1.15) except
the flat amounts of 2022 and 2024, maybe a scaling from the anonymisation, which the Gini ignores. Every number in the
notes was re-measured on the changed definition (the reports of that panel, replaced below by the re-review's, quoted
the definition before these changes). The record's "left out rows with negative incurred amounts" and its screening
metric line are corrected at hand-over. Changed on 2026-11-06 (issue 6, D10): `actual_exposure` became the training
weight as well as the metric's, every earned premium is annualised, `total_exposure` left the features, and `_clean`
checks that the cost per year times the time on risk gives back the cost.

Changed after the re-review panel (AI, 2026-11-06), no decision needed (rows, target, weight, split and metric
unchanged; a build waits for your ask): `bonus_score` is an ordered category (bad < neutral < good); the texts that said
no premium carries the time on risk now name the decimals' mark (issue 7), Lennart's CC of D10 staying as written with a
dated AI note; `business_type` has its leak note; `splits_comment` and the metric reason are re-measured and re-cited.

Changed on Lennart's marks of 2026-11-08 (rows, target, weight, split and metric unchanged; a build waits for your
ask): the annualised premiums are rounded to the cent (issue 7) and `payment_frequency` is ordered annual < semiannual
< quarterly, as in the two pricing games (issue 8); the dated AI note after D10's CC gave way to Lennart's CC; the
decimal check, probe 22 and the task probe were re-run (issue 7's resolved turn).

**Main points:** Nothing open. Resolved: 3, 4 and 5 on 2026-11-02, 6 on 2026-11-06, 7 (the annualised premiums rounded
to the cent, which changes the wording of Andrej's issue 4 call and of D10's CC) and 8 (`payment_frequency` ordered here
and in the two pricing games) on 2026-11-08.

**Verdict (2026-11-02, Andrej):** ship. The metric is marked as declared (`normalized_weighted_gini` on the cost per
year on risk, weighted by `actual_exposure`). The dataset joins the accepted set; a build waits for your ask.

**Issues for Andrej and Lennart:**

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
   question is now this table's alone: the row Gini or the exposure-weighted Gini for this table, on its own evidence,
   not matched to frempl; when in doubt, the form the collection has fewer of.

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
   models no sample weight (`actual_exposure` is scoring-only, on your call), so a plain model scores about the
   insurer's price, and only a model that weighs by the corrected time on risk itself (a feature) beats it.
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
       they gain +0.0010 under Tweedie (SE 0.0006, 7/9) and +0.0005 under L2 with 10 seeds (re-measured by the
       re-review of 2026-11-06; 3 seeds gave +0.0020), under two SEs and 3% of the free-exposure gain.
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
     | A | D10 (implemented) | `actual_exposure` the training weight; premiums annualised; `total_exposure` dropped | no input carries the time on risk in its level (the premiums' decimals still do, found by the re-review of 2026-11-06: issue 7); both weighted fits beat the premium alone | loses the planned time on risk of late starts (0.018 under Tweedie) |
     | B | As on 2026-11-02 | corrected `total_exposure` a feature; earned premiums; no training weight | Tweedie scores 0.011 higher | breaks a Must; an untuned L2 fit scores below the premium |
     | C | A, flat covers as flags | A, with the occupants and legal protection premiums as cover held or not | the premium mark mostly gone (ROC AUC 0.81 to 0.68) | costs 0.010 to 0.012; the mark does not pay |

   * **Recommendation:** A: no column's level carries a cancellation signal that pays on the declared metric (the
     premiums' decimals, read as features, gain +0.0035: found by the re-review of 2026-11-06, issue 7), and C removes
     legitimate signal for a mark that does not pay. **Decision:** A, B or C?

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

7. **Round the annualised premiums to the cent?**

   * **Problem:**
     - The annual tariffs sit on a 5-decimal grid, so dividing a part-year's earned premium by its time on risk puts
       it back on that grid while a full year, a blend of two prices, keeps 11 to 15 decimals: the count of decimals
       tells a year cut short from a full one.
     - Among the policy-years in force from 1 January the decimals alone rank the 32,626 cancelled ones at ROC AUC
       0.965, and a model that reads them gains +0.0035 under weighted Tweedie (about 2 SEs, ahead on 8 of 9
       splits), a mark the rules exclude whatever it scores[^7a].
     - Rounding every annualised premium to the cent removes the mark at no measurable cost, but it changes Andrej's
       call of 2026-11-02 to leave the premiums unrounded (issue 4), which the D10 call repeats (issue 6), so it needs
       your yes[^7b].
   * **Background:**
     - `total_premium` has at most 5 decimals on 39.5% of the located cancellations against 1.0% of the active full
       years in force from 1 January; on a 1e-6 grid the shares are 83.8% and 2.8%, and every cover premium shows it,
       in all three years.
     - The located cancellations had the mark before 2026-11-06, since their premiums were annualised by the earlier
       fix; D10's annualising gave it to the late starts as well (0.5% of them on the short grid before the division,
       44% after), where it does not tell a cut from a late start (AUC 0.484).
     - Probe 22 and the task gamer did not see it: the probe's trees fit the premiums' values, not their decimals, and
       the gamer tested the decimals against the target, not against the cut.
     - On 2026-11-02 Andrej weighed rounding to whole euros against the same cause, a cancelled year that shows one
       price where a full year blends two, as a model reads it from the premiums' values (ROC AUC 0.77); the decimals,
       which read it at 0.965, were not known then[^7c]. Rounding to the cent removes the decimals channel and keeps the
       values, and with them the mark he chose to keep.
   * **Effect on the task:** a model that reads a test row's premiums as text, or counts their decimals, learns that
     the row's year was cut short, which an insurer pricing the year cannot know; a tree on the values does not read
     it, so the default models' scores barely move.
   * **Experiments:** untuned LightGBM weighted by the time on risk (the claim and column auditors; the mediator on the
     9 shipped splits x 10 seeds):
     - Precision features alone (decimal counts and cent-grid flags of the eight premiums, folds grouped by policy,
       the rows in force from 1 January): ROC AUC 0.965 for the located cancellations as shipped, 0.565 rounded to the
       cent, 0.607 rounded to 4 decimals; after cent rounding no grid from 0.1 to 1e-4 separates them (no AUC more
       than 0.009 from 0.5).
     - The eight decimal counts as features: +0.0035 under weighted Tweedie (SE 0.0017, ahead on 8 of 9, 2 seeds) and
       -0.0052 under weighted L2 (1 of 9); the time on risk as a free feature gains +0.0331 in the same run.
     - Rounding to the cent changes the score by -0.0005 under Tweedie and +0.0005 under L2 (SE 0.0006 each; the
       column auditor: -0.0017 and +0.0101 on 3 splits x 2 seeds), within noise.
     - The premiums' gain through any cancellation is +0.0010 unrounded and +0.0013 rounded under Tweedie (SE 0.0006
       and 0.0008, ahead on 7 and 5 of 9), below the panel's bar of two SEs on 7 of 9 splits, so option A of issue 6
       stands either way.
   * **Consistency:** the check against Andrej's call: B departs from his call to leave the premiums unrounded (issue 4,
     2026-11-02, kept in D10) on a fact found after it: the mark is also readable from the premiums' decimals, a channel
     he did not weigh[^7c]; it follows frempl_french_motor_personal_line, where his rounding of the length to whole
     months removed a mark of the cut at no cost[^7d].
   * **Panel:** the panel agrees on cent rounding; the mediator sent it to you because it changes a curator's call.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Leave unrounded (implemented) | the annualised premiums keep their 11 to 15 decimals | follows the calls of 2026-11-02 and 2026-11-06 as worded | breaks a rule that allows no exception; the decimals rank the located cancellations at AUC 0.965 |
     | B | Round to the cent | `_clean` rounds each annualised premium to 2 decimals; a CC line corrects D10's | removes the mark (AUC 0.565); keeps every price to the cent; no measurable score change | changes the wording of Andrej's issue 4 and of D10's CC; a rebuild |
     | C | Round coarser | whole euros or bands | removes the mark too | discards the price information Andrej kept on 2026-11-02 |
     | D | Amend the rule | the leak rule lets a precision mark that does not pay through the values stay with a note | nothing changes here | a deliberate rule change; reaches frempl_french_motor_personal_line's month rounding too |

   * **Recommendation:** B: it removes a mark the rules name, keeps every price to the cent and costs nothing
     measurable, and it keeps the premiums' values, which Andrej's reason against rounding protected. **Decision:** A,
     B, C or D?

   **Notes for the AI:** the mediator's issue 1 of the re-review of 2026-11-06 (LEAK-41, Must; its option (a) is B here,
   and "keep it with a note" is not available under a Must). On B: in `_clean` step 5,
   `df[premiums] = df[premiums].div(df["actual_exposure"], axis=0).round(2)`; restate the step-5 comment, the "Premiums
   annualised" bullet and the decision "Every earned premium is annualised" with the before and after (AUC 0.965 to
   0.565; -0.0005 under Tweedie and +0.0005 under L2, SE 0.0006) and drop "waits for the curator"; re-run the claim
   auditor's precision test (AUC and the decimal-count gain) on the rebuilt frame, `dataset check` and the task probe;
   append through the store API a CC line in the curator's name, for example "CC (<date>, Lennart): the annualised
   premiums are rounded to the cent (REVIEW.md issue 7 (B)): their decimals marked a part-year (ROC AUC 0.965 for the
   located cancellations, 0.565 rounded; score -0.0005 / +0.0005, SE 0.0006). This corrects the CC of 2026-11-06 ('no
   remaining column whose cancellation signal pays'; 'the premiums stay unrounded') and changes Andrej's 'do not round
   the premiums' (issue 4, 2026-11-02) on that fact; his reason concerned the values, which cent rounding keeps." Then
   replace the dated AI note after the CC in the notes, and tell Andrej (below). For the main session:
   frempl_french_motor_personal_line issue 9 cites these premiums' unrounded precision under Consistency, and the Cases
   rows of LEAK-41 (leak_checks.md) and MET-15 (metrics.md) quote this table's premium mark; on B they need a line. On
   C: as B with whole euros or bands, and the price information's cost re-measured. On D: an amendment of LEAK-41's
   precision clause (main session). Whatever the answer, tell Andrej, the record's curator, that D10 (issue 6)
   superseded his calls of 2026-11-02 and that this issue changes his issue 4 call (the record is claimed by Lennart).

   [^7a]: **LEAK-41** (Must; 2026-11-06, Lennart): a column the task uses as a weight whose value is set or cut after
     the prediction point is never a model input, "whatever it scores, and neither is a column that encodes it: an
     earned premium (ship it annualised to the planned term, or not at all), a length corrected on some rows and
     realized on others, a sum of a group's exposures, a value whose precision marks the cut". A Must takes no
     exception (principles.md, "Strengths").
   [^7b]: principles.md, "Precedence in the process", who decides: "the curator's decision (a `CC` line, a review
     mark) > an AI assessment [...] The AI argues (a counter-argument) and never overrides." A decision that would
     break a Must goes back to the curator as a question ("Consistent judgement", case 1). Andrej, 2026-11-02, issue
     4: "Keep both with explicit potential-leak notes; do not round the premiums." Lennart, CC of 2026-11-06 (D10):
     "while the premiums stay unrounded and the year's last record stays with its note".
   [^7c]: principles.md, "Consistent judgement, the curator's included": a decision that departs from a precedent
     names the fact that sets the case apart. Andrej, 2026-11-02, issue 4: "The 0.002 Gini change from rounding is not
     an upper bound on leakage, since rounding also removes legitimate information and leaves cancellation partly
     readable."
   [^7d]: frempl_french_motor_personal_line, issue 2 (a) (Andrej, 2026-11-02): "every `Exposure` rounded to months",
     which hid the decimals of the realized length that told a continued record from an open one (AUC 0.92 to 0.71,
     and 0.91 to 0.61).

   **Resolved (2026-11-08, Lennart):** B, `_clean` rounds each annualised premium to the cent; on the rebuilt frame
   the premiums' decimal counts and cent-grid flags rank the located cancellations at ROC AUC 0.565 (0.965 before),
   the decimal counts as features gain +0.0001 under weighted Tweedie and -0.0012 under weighted L2 (9 splits x 2
   seeds; +0.0035 and -0.0052 before), probe 22 finds no feature whose gain goes through the time on risk under either
   fit (R^2 0.340), and the task probe raises no flag (LightGBM 0.3187 against 0.3165 before). The CC line corrects
   D10's "while the premiums stay unrounded" and changes the wording of Andrej's issue 4 call on the decimals' mark,
   with his prices kept to the cent; the notes, the decision table and the task summary say so, and the dated AI note
   after D10's CC gave way to this CC.

8. **Order `payment_frequency` as annual < semiannual < quarterly?**

   * **Problem:**
     - `payment_frequency` is the policy's billing frequency, annual, semiannual or quarterly (1, 2 or 4 instalments a
       year), and ships as an unordered category.
     - Its levels have an order by the number of instalments, and the rules decide an ordinal scale (a grade, a stage,
       binned ranges, answers on a survey scale) case by case, categorical by default, and make it an ordered category
       in the order its codebook gives, but they name no billing frequency among such scales, so both forms comply[^8a].
     - The two other pricing tables with a payment frequency ship it unordered, so an order here would differ from
       them unless they change too[^8b].
   * **Background:** `bonus_score` became an ordered category after the re-review (bad < neutral < good): it is a scale
     of the claims history whose levels the variable sheet names in words (a poor, a neutral or a favourable claims
     history), and the rules make an ordinal scale an ordered category in the order its codebook gives[^8a], as for
     bemtpl97's `coverage` (TPL < TPL+ < TPL++) in this family.
   * **Effect on the task:** small: a model that reads the order can split quarterly from annual payers, with
     semiannual between them, in one cut; a model that one-hot encodes the levels sees no difference.
   * **Consistency:** pricing_game_2016_french_fleet ships its payment frequency (annual, semi-annual, quarterly)
     unordered, its column audit of 2026-11-06 having offered the order as optional, and pricing_game_2017_french_mtpl
     ships `pol_pay_freq` (yearly, biannual, quarterly, monthly) unordered.
   * **Panel:** the column auditor raised it as optional, the advocate leaves it to you and the critic did not raise
     it; the mediator ranks it low.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Unordered (implemented) | `payment_frequency` stays a category without order | no change; matches the two pricing games | the order of instalments is not stated |
     | B | Ordered here | an ordered category, annual < semiannual < quarterly | keeps the order the levels carry | differs from the two pricing games |
     | C | Ordered in all three | B here, and the same order in pricing_game_2016_french_fleet and pricing_game_2017_french_mtpl | one form for the family | two more definitions change |

   * **Recommendation:** A, as in the two pricing games; if the order should be kept, C rather than B, so the three
     tables stay alike. **Decision:** A, B or C?

   **Notes for the AI:** the mediator's issue 2 of the re-review of 2026-11-06 (CLEAN-14, Should; low). On B or C: add
   `"payment_frequency": ["annual", "semiannual", "quarterly"]` to `ORDINAL` in `dataset.py` (the comprehension then
   drops it from `CATEGORICAL`), restate the codes bullet and re-run `dataset check`. On C, the main session also
   orders `payment_frequency` in pricing_game_2016_french_fleet (annual, semi-annual, quarterly) and `pol_pay_freq` in
   pricing_game_2017_french_mtpl (Yearly < Biannual < Quarterly < Monthly), each with a CHANGELOG entry.

   [^8a]: **CLEAN-14** (Should; amended 2026-10-30 and 2026-11-01, Lennart): "An ordinal scale (a grade, a stage,
     binned ranges, answers on a survey scale) is no measured quantity: it is decided case by case, categorical by
     default", and "An ordinal scale is an ordered category, in the order its codebook gives"; Lennart, 2026-10-30:
     "ordinal scales are case-by-case, they could be either but generally we know they are not numeric so categorical
     might be the safer bet".
   [^8b]: principles.md, "Consistent judgement, the curator's included", case 2: a precedent with similar facts decided
     the other way is a question for the curator.

   **Resolved (2026-11-08, Lennart):** C, `payment_frequency` is an ordered category here, annual < semiannual <
   quarterly, and the same order by payments a year is applied in pricing_game_2016_french_fleet (annual < semi-annual
   < quarterly) and pricing_game_2017_french_mtpl (Yearly < Biannual < Quarterly < Monthly, its four levels in the
   data), each with its notes and a CC line; `dataset check` 0 errors, 0 warnings on all three.

**Review panel:** ship after changes (mediator). Tier full, re-review of 2026-11-06 under LEAK-41, MET-14 to MET-16,
after decision D10 (issue 6): 12 reports. Claims: 16 audited, 10 hold (one a tautology the rules ask for, one except the
premiums' decimals), 2 refuted (the decimals of the annualised premiums mark the cut, so "no premium carries the time on
risk" and "no proxy of the cancellation gains beyond noise" are false: issue 7, the AI's texts corrected), 2 refuted in
part (the metric reason's citation and the stale figures of `splits_comment`, both rewritten) and 2 untested (the pandas
2.3 checksum; comparisons with the old definition). Blind review: include with changes; its main concern, the log1p
target under the weighted fit, is the scale Lennart kept on 2026-11-06, at no measured cost (0.3077 for squared error on
log1p against 0.3064 for a Tweedie fit). Task gamer: the features are clean; only the weight as a feature and the
renewal pattern rebuilt from `insured_id` beat the noise (+0.03 to +0.04), both outside `feature_columns()`, and its "no
signal in the decimals" tested the target, not the cut. Agreed: the verdict; D10's weight, annualising and drop of
`total_exposure`; the split; cent rounding as the fix, asked of you; the `business_type` note; `bonus_score` ordered;
every text change (made). Disputed, settled by the mediator: whether the premiums' gain through any cancellation sends
option A of issue 6 back (no: +0.0013 under Tweedie after rounding, 10 seeds, below the bar); whether `business_type`
needs its note before shipping or is a weak keep (the note now, the column stays). The mediator's issues 1 and 2 are
issues 7 and 8 here; its process note (tell Andrej about D10) is in issue 7's Notes for the AI, and if
pricing_game_2016_french_fleet issue 6 goes to B (one temporal window), the precedent checker would ask whether this
table keeps its forced grouped split; the prompt is in that issue's Notes for the AI.

<details><summary>Mediator</summary>

**Mediator report: spanish_motor_insurance_coverage_level_2022_2024 (exposure re-review, full tier, 2026-11-06)**

My experiments reuse the re-measure's scripts, frame and splits: untuned LightGBM fitted with `actual_exposure` as the
row weight, 9 shipped splits x 10 seeds.

**1. Judgment record**

Verdict: ship after changes.
Validity:
- USE-5 and USE-8 hold (approximate fit; the practitioner agrees).
- LEAK-41 is triggered by the annualised premiums' decimal precision, which marks the cut (located cancellations ROC AUC
  0.965). The fix is in the definition: round to the cent (AUC 0.565). It needs the curator's yes because it changes a
  standing "do not round" call (issue 1).
- Otherwise LEAK-41 holds:
  - The weight is no feature, and MET-15's wiring holds.
  - Probe 22 finds no mediated gain on either fit.
  - After rounding, the premiums' gain through any cancellation is +0.0013 (SE 0.0008, 5/9). That is not above noise, so
    A stands over C.
- LEAK-41's reporting clause is not met for `business_type`. A note is due now. The column itself stays under LEAK-10's
  second clause, because the traceable part shows no gain (measured today).
- SPLIT-8 and SPLIT-24 hold. SPLIT-8's measured clauses are stale and are rewritten with today's numbers. Value: TP-4
  holds (0.317 against the premium alone at 0.298); TP-2 holds. MET-14 and MET-15 hold. MET-11/PROV-16: the citation is
  fixed (Should). Quality: CLEAN-14 departure fixed (`bonus_score` ordinal). The CLEAN-16 log1p scale is kept (settled
  by Lennart, 2026-11-06; measured cost zero). Weighed: nothing left open that changes the verdict. For the curator:
  issue 1 (confirm cent rounding: a Must fix that touches Andrej's issue 4 and the D10 CC); issue 2 (optional,
  payment_frequency ordinal); notify Andrej of D10.

**2. Changes to make now (no decision needed)**

1. Correct the four false sentences now, whatever the curator decides in issue 1. Rule: LEAK-41 and EV ("a number quoted
   as current must be measured").
   - Which sentences:
     - the `_clean` step-5 comment;
     - the "Premiums annualised" bullet ("so no premium carries the time on risk");
     - the Decision text in REVIEW issue 6;
     - the CC's "no remaining column whose cancellation signal pays".
   - Each says no premium carries the time on risk. That is false while the premiums are unrounded: precision features
     alone give AUC 0.965, and an engineered decimal-count feature gains +0.0035 under weighted Tweedie (SE 0.0017, 8/9;
     precision_gain.out).
   - Once the rounding is confirmed, state the before and after:
     - AUC 0.965 to 0.565;
     - score change from rounding (10 seeds, mine): Tweedie -0.0005 (SE 0.0006), L2 +0.0005 (SE 0.0006);
     - the column auditor got -0.0017 / +0.0101 on 3 splits x 2 seeds.
   - Note: the CC is the curator's line. Change it only as a correction the curator signs together with issue 1. Until
     then, add a dated AI Assessment that flags it.
2. `business_type` note, added to the last-record bullet. Rule: LEAK-41's reporting clause (Must) for a suspect column,
   and LEAK-10's second clause for the keep. Content:
   - it is read from the year's last record and flips from new business to portfolio during a second calendar year;
   - cancelled second years are new business 3-10 pp more often;
   - probe 22: R^2 0.350 for the weight fit, `business_type` 41% of that fit's gain, mediated gain -0.0040 (Tweedie) and
     -0.0118 (L2), 1/weight alone 0.089 (0.075 over the 9 splits);
   - new today: setting it back to its 1 January value on the 76,597 carried rows (the previous year's last record)
     changes the score by +0.0002 (Tweedie, SE 0.0004, 5/9) and -0.0014 (L2, SE 0.0007, 3/9). Through any cancellation
     it changes by -0.0002 and -0.0010.
3. Update the "through any cancellation" figure in the premium note and in REVIEW issue 6. Rule: EV-1.
   - The quoted +0.0020 (SE 0.0011, 7/9) was a 3-seed estimate. With 10 seeds the unrounded value is +0.0010 (SE 0.0006,
     7/9) under Tweedie and +0.0005 under L2.
   - After cent rounding it is +0.0013 (SE 0.0008, 5/9) and -0.0002 (SE 0.0011).
   - Seed SD is 0.007. The rounded value is 4% of the free-exposure reference (+0.0325).
4. Rewrite `splits_comment`'s measured clauses. Rule: SPLIT-8 (Must: the forced split states its measured cost and its
   leak test).
   - Today's numbers:
     - 2024 window 0.300-0.307 (L2) and 0.305-0.316 (Tweedie), SE 0.011-0.012;
     - the folds' 2024 rows 0.274-0.333 / 0.292-0.332 (means 0.309 / 0.311);
     - random against grouped 0.318 / 0.315.
   - The wisconsin-form leak test: +0.006 to +0.010 pooled. Include the per-year maximum, 2022 at +0.029 under L2 (7/9):
     SPLIT-8 asks for the cost as measured.
   - Label any older number "row Gini, before 2026-11-02".
5. Metric reason. Rule: MET-11/PROV-16 (Should).
   - Cite Frees, Meyers and Cummings 2011 for the ordered Lorenz Gini, and CAS Monograph 5 and Liberty Mutual 2014 for
     the exposure-weighted form.
   - Say the weight here is the time on risk by the curator's call.
   - Add the ceiling (1/time on risk 0.075) and the premium alone (0.298).
6. `bonus_score` becomes ordinal: `ordinal={"bonus_score": ["bad", "neutral", "good"]}`, and it is removed from the
   categorical list. Rule: CLEAN-14 (Should); bemtpl97's `coverage` is the precedent. Both sides agree.
7. Move "policies starting during the year lack their planned time on risk" from `fit_reason` to the notes. Rule: USE-8
   text, Should. Both sides agree.
8. Optional, not a defect: sharpen the step-9 assertion against the raw `total_incurred` and `total_exposure`. Rule:
   MET-14 holds as written.

**3. Issues for the curator (ranked)**

Issue 1 (validity, P4, Must; a confirmation, not a weighing call). Round the annualised premiums to the cent?
- Problem:
  - Annual tariffs sit on a 5-decimal grid. Dividing a pro-rata earned premium by its time on risk puts it back on that
    grid, while a full year's blended premium keeps 11-15 decimals.
  - `total_premium` has ≤5 decimals on 39.5% of located cancellations against 1.0% of active full years. On the 1e-6
    grid it is 83.8% against 2.8%.
  - D10's annualisation made this hold for the late starts too (0.5% to 44%).
- Effect:
  - It is a mark of the cut that a participant can engineer: +0.0035 under weighted Tweedie (2.1 SE, 8/9) and -0.0052
    under L2.
  - Probe 22 and the task gamer cannot see it: trees fit on values, and the gamer tested decimals against the target,
    not against the cut.
- Rule: LEAK-41 (Must), "neither is a column that encodes it: ... a value whose precision marks the cut", "whatever it
  scores". A Must has no exceptions, so a note cannot keep it (principles, Strengths).
- Mildest fix (remedy ladder, rung 2): `df[premiums].div(df["actual_exposure"], axis=0).round(2)`.
  - Afterwards no grid from 0.1 to 1e-4 separates the cancellations (largest |AUC-0.5| 0.009; auditor AUC 0.565).
  - Rounding to 4 or 5 decimals is not enough (0.607).
- Why it needs a yes:
  - Andrej's issue 4 (2026-11-02) says "do not round the premiums", and Lennart's D10 CC repeats "the premiums stay
    unrounded". The AI never overrides a CC ("Who decides").
  - Keeping the unrounded premiums would break a Must, so this is consistency case 1: a question, not an exception.
- Best evidence, both sides:
  - Both sides agree on the fix and on asking.
  - Andrej's reason (rounding to whole euros or 3 significant digits "removes legitimate information and leaves
    cancellation partly readable") was aimed at the flat-amount mark. Cent rounding keeps every price to the cent,
    removes this mark, and costs nothing measurable (±0.0005, SE 0.0006).
- Options:
  - (a) Round to the cent and correct the CC (recommended).
  - (b) A coarser fix (whole euros, bands): it also removes the mark but discards price information Andrej wanted kept.
  - (c) Amend LEAK-41 so a precision mark that does not pay may stay. This is a deliberate rule change, and it would
    also reach frempl's rounding (see section 5).
  - Not available: keep it with a note.

Issue 2 (quality, P7, Should; low). `payment_frequency` as ordinal?
- Annual < semiannual < quarterly is an ordered billing frequency. Unordered also complies.
- The advocate leaves it to you; the critic did not raise it.
- Rule: CLEAN-14 and the 2026-11-01 ordinal marks.
- What settles it: whether the 2026-11-01 marks treat a frequency scale as ordered (the bemtpl97 family precedent).

Process note (not a dataset defect). Andrej is the record's curator and has had no consistency check on D10 (precedent
checker 2a). Notify him, together with issue 1, since issue 1 touches his issue-4 wording. Check the claims board for
his claim on this record first.

**4. Disputed points, settled**

A. Cent rounding: change now, or the curator's yes?
- Both rest on LEAK-41 (Must). There is no conflict between rules; the question is who decides.
- A Must is fixed in the definition when it can be. But the fix contradicts a standing curator decision, and under "Who
  decides" the AI argues and does not override.
- Ruling: it goes to the curator as a confirmation (issue 1). The text corrections that are false either way are made
  now (change 1).

B. "Through any cancellation": does it send A against C back?
- The critic rests on LEAK-41 ("decides on the worse" fit) and EV-1. The advocate rests on LEAK-41's timing clause
  (USE-6), LEAK-7, and "Who decides".
- Decisive experiment, run today: 10 seeds after cent rounding, the gain is +0.0013 under Tweedie (SE 0.0008, 1.6 SE,
  5/9, seed SD 0.007) and -0.0002 under L2.
- The 3-seed +0.0020 does not hold: unrounded with 10 seeds it is +0.0010 (SE 0.0006).
- Threshold I apply: the panel's convention for "above noise", at least 2 SE over the splits and ahead on at least 7/9
  on the worse fit.
  - The result is under both sides' bars: the critic's "near 2 SE" and the advocate's "beyond 2 SE and a seed SD".
  - What would have sent it back: a rounded-definition gain of at least 2 SE and at least 7/9 under weighted Tweedie.
    Then the call is whether the price's renewal blend is start-known (USE-6) or a post-cut mark (LEAK-41), and C's cost
    of 0.010-0.012 is weighed against that gain.
- Ruling: A stands; no curator decision is needed. Quote the number (change 3).
- Probe 22's rule also says a gain only flags and timing decides. The annual price is set at writing, and the
  renewal-blend part is the settled keep (issue 4 / D10 option A).

C. `business_type`: a Must, or a weak LEAK-10 note?
- Both are partly right. There is no conflict, because the two parts are independent:
  - the duty to report the column's gains on both fits comes from LEAK-41's reporting clause (Must, P4). `business_type`
    is a suspect column (41% of the weight fit), so the note is required before shipping, not optional;
  - whether the column stays is judged by timing under LEAK-10's second clause: it stays with a note only if the
    traceable part shows no gain.
- I measured the traceable part today: reverting to the 1 January value gives +0.0002 / -0.0014, and through any
  cancellation -0.0002 / -0.0010. No gain, so the keep is allowed.
- LEAK-10's ban on keeping "a column the task uses as a weight" with a note does not apply: `business_type` is not the
  weight.
- Ruling: the note is a change to make now (change 2). The column stays.

D. Everything else: the opening briefs and rebuttals concede it. The blind reviewer's log1p objection is CLEAN-16 as
amended, settled by Lennart on 2026-11-06, with a measured cost of zero (0.3077 against 0.3064). Not reopened.

Task gamer's exploits, mapped to rules and notes:

| # | Exploit | Gain | Rule | Note in the definition | New or known |
|---|---|---|---|---|---|
| 1-2c | `actual_exposure` (or parts of it: portfolio-only, NB-only, full-year flag) as a feature | +0.031 Tweedie (-0.031 log1p) | LEAK-41, MET-15 | Exposure bullet: free feature +0.0325, 1/weight 0.075 | Known. The gain matches the note, and no feature carries it. Not an issue. |
| 3, 3a | has_next / lapse rebuilt from `insured_id` | +0.007 to +0.009, 9/9 | LEAK-33 (the group column is never a feature); a harness duty | "insured_id ... the group column, never a feature" | Known by rule. The renewal gain is newly measured but needs a column outside `feature_columns()`. Not a definition issue. |
| 3b, 1 | Combinations of the above | +0.036 to +0.042 | As above | As above | Known |
| 4 | `insured_id` as a feature (entry order) | +0.003, noise | LEAK-33 | As above | Known, noise |

The gamer's "no signal in decimals" tested the target, not the cut. The precision channel (issue 1) is new and comes
from the claim and column auditors.

There are no `Potential leak, kept on purpose:` notes on the weight. The two kept notes (premium blend, last record)
were not exploited above their noted sizes. The accepted warning `task_target_value_dominant` (Andrej, 2026-11-03) is
not touched.

**5. Agreed facts**

- Wiring: `sample_weight` = the metric weight = `actual_exposure`. None of the 23 features is an exposure column,
  `policy_status` or a claim part. Constant predictions score 0 and perfect ones 1 on all 9 folds. The scorer matches an
  independent Liberty Mutual Gini to 1e-6.
- Probe 22: the features fit the weight at R^2 0.350. No top feature gains through the weight (-0.0028 to -0.0147
  Tweedie; -0.0118 to +0.0003 L2). 1/weight alone scores 0.089 (0.075 over 9 splits).
- Annualisation is pro rata. Spearman of the annual premium with the time on risk is 0.034 / 0.024 / -0.053, against
  0.74-0.83 for the earned premium.
- Annualisation made the decimal precision mark the cut (see issue 1). Cent rounding removes it at no measurable cost.
- Scores: definition 0.3166 (L2) / 0.3165 (Tweedie). Rounded, 10 seeds: 0.3178 / 0.3167. Premium alone 0.2975. Dropping
  `total_exposure` costs 0.0176 (Tweedie), the planned time of late starts, which cannot be shipped without the cut.
- Split: 0 shared `insured_id` in 9/9 splits. The forced split is within the 2024 window's SE. The leak test finds a
  +0.006 to +0.010 pooled within-year gain (2022 +0.029 under L2), and no column carries it. No immature 2024 labels.
- `business_type` is read from the last record and carries a weak cancellation mark with no measured gain.
- `bonus_score` is an ordered scale.
- The metric citation misattributes the weighted form.

**6. Consistency with precedent**

- D10 is consistent with all seven LEAK-41 tables of 2026-11-06 (fremtpl2, bemtpl97, australian D8, frempl D9,
  pricing_game_2016 D11). Each reversal of Andrej's 2026-11-02 calls rests on a rule adopted after it (precedent checker
  §1-2). No drift.
- Dropping `total_exposure` departs from frempl and pricing_game_2016, which keep a start-known length. The fact that
  sets this case apart is stated: the release has no start date.
- Cent rounding follows frempl's rounding of `Exposure` to months (Andrej, 2026-11-02): a coarsening that removed a mark
  of the cut at no cost. It departs from Andrej's issue-4 wording only on a new fact (a precision channel, not the
  flat-amount mark). Hence issue 1, with the consistency prompt below.
- Option A over C follows Andrej's issue 4, LEAK-7, onlinenewspopularity and house_sales. Today's re-measure keeps it
  that way.
- Consistency check prompt for issue 1:

  **Consistency check (AI, 2026-11-06):** rounding the annualised premiums to the cent departs from "do not round the
  premiums" (Andrej, issue 4, 2026-11-02; kept in D10). What sets it apart? (a) A new fact: cent rounding removes a
  precision mark of the cut (AUC 0.965 to 0.565) that LEAK-41 names, and keeps every price to the cent, at ±0.0005;
  recorded as a correction of the CC. (b) Keep unrounded: this breaks LEAK-41 (Must), so it needs (d). (c) Coarser
  rounding, as Andrej declined. (d) Amend LEAK-41's precision clause.

- Conditional prompt from the precedent checker (§5), only if pricing_game_2016_french_fleet issue 6 goes to B (one
  temporal window under an amended SPLIT-14). This dataset also has one valid window (2024 trained on 2022-2023, 52.5%
  of the rows) and ships forced grouped (Andrej, 2026-11-02). The options:
  - (a) Keep it forced grouped, the distinguishing fact being that its rows carry only a calendar year, written into the
    amendment's scope (recommended if the amendment is written for daily-dated releases).
  - (b) Treat it like pricing_game_2016: one window.
  - (c) Reopen pricing_game_2016 to match this one.
  - (d) Word the SPLIT-14 amendment so it decides both (recommended otherwise). pricing_game_2016's text says this
    table's window is "below the floor". That is inaccurate: it is above the floor, and only the count of windows fails.
- Precedent checker's further note: wisconsin's forced split was refused for a year-level leak (+0.113). Here the leak
  test finds none at the year level. Re-quoting the leak test with today's numbers (change 4) keeps that distinction
  current.

</details>

<details><summary>Claim audit</summary>

**Claim audit: spanish_motor_insurance_coverage_level_2022_2024 (exposure re-review, 2026-11-06, full tier)**

Read: dataset.py, README.md, REVIEW.md issue 6 and the record. Untuned LightGBM, weighted by actual_exposure, scored
with my own Liberty Mutual WG (equal to the shipped scorer to 1e-6).

VERDICT: one Must refuted. The annualised premiums carry the time on risk in their decimal precision, which LEAK-41
names ("a value whose precision marks the cut"). The located cancellations are told apart at ROC AUC 0.965 from
decimal counts alone. This is a new channel: it is not the flat-amount mark the notes measure at 0.81. Its gain under
weighted Tweedie is +0.0035 (SE 0.0017, 8/9 splits), about 11% of the free-exposure reference. Rounding the
annualised premiums to the cent removes it (AUC 0.565). Everything else of D10 holds on the data: the weight wiring,
the metric, the annualisation's level, the counts and the re-measure numbers. The splits comment still quotes
row-Gini numbers from before 2026-11-02 as current.

**Table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | "Each premium is divided by the recorded time on risk ... so no premium carries the time on risk" / "Each premium is divided by the time on risk, so no premium carries it (LEAK-41)" | dataset.py notes "Premiums annualised", Decision "Every earned premium is annualised", CHANGES.md, CC line | I counted the decimals (%.15g) of each shipped annualised premium. Among policy-years in force from 1 January (portfolio, or a row the year before; 169,919 rows, 32,626 located cancellations) I fitted LightGBM on precision features only (decimal counts and cent-grid flags of the 8 premiums), with GroupKFold(3) by insured_id, and then added the 8 decimal counts to the model on the 9 shipped splits x 2 seeds | REFUTED | The annualised total premium has <=5 decimals on 39.5% of the located cancellations, 43.7% of the late starts and 42.5% of the first-year cancellations. It has <=5 decimals on 1.0% of the active full years in force from 1 Jan and 2.5% of the first-year full years. Before the division (the raw earned premium) the share is 0.5% for every part-year group. Annualising a pro-rata premium gives back the tariff's short decimal, while a full year's premium (a blend of two prices) keeps 11-12 decimals. Located-cancellation ROC AUC from the precision features alone is 0.9647-0.9668 (decimal counts alone 0.9637), against 0.81 from the shipped features in the notes. Across all rows, the total premium's short-decimal flag ranks e<1 at AUC 0.70. Gain on the declared metric from the 8 decimal-count features: weighted Tweedie +0.0035 (SE 0.0017, ahead 8/9; base 0.3128, seed SD 0.0045); weighted L2 on log1p -0.0052 (1/9). The free-exposure reference in the same run is +0.0331 Tweedie (9/9) and -0.0335 L2. | LEAK-41 (Must: "neither is a column that encodes it: ... a value whose precision marks the cut"; "whatever it scores"; decide on the worse fit = Tweedie +0.0035) |
| 2 | CHANGES.md: "no proxy of the cancellation gains beyond noise" (premium mark 0-6% of the leak reference) | CHANGES.md, CC line, notes | Same run as row 1 | REFUTED (marginally) | The precision channel gains +0.0035 (2.1 SE, 8/9), 10.6% of the reference under Tweedie. It is about the size of the seed SD, so it is no clear score leak, but it is above the 0-6% the notes report, and a participant can engineer it (the task gamer's move). The probe 22 arms do not see it: they fit on values, and trees do not read decimals. | LEAK-41, EV-1 |
| 3 | Earned premiums are pro rata (earned total follows e: Spearman 0.83/0.74/0.78; the annual total does not: 0.034/0.024/-0.053; median 340-355 per band, flat by payment frequency) | notes, REVIEW issue 6 | Recomputed from the raw file (exposure>0) | HOLDS | active part-years n=168,330: earned rho 0.827, annual 0.034; first-year cancellations n=5,653: 0.740 / 0.025; located n=32,626: 0.784 / -0.053. Median annual premium is level across bands within each payment frequency (active A 329-343, S 358-369, Q 518-573). Cancelled years are dearer per year (A 371-378, Q 650-673): risk selection, which the notes report as the premium mark. | LEAK-41, MET-14 |
| 4 | sample_weight = "actual_exposure" is the metric's weight; actual_exposure and total_exposure are no features | dataset.py, CHANGES.md | Loaded the container: sample_weight(c), spec.inputs, feature_columns(c) | HOLDS | sample_weight=actual_exposure; MetricSpec inputs {'weight':'actual_exposure'}, target_transform log1p, origin context; actual_exposure not among the 23 features; no total_exposure/liability_exposure/policy_status/claim parts in the frame. | MET-15, MET-2, LEAK-41 |
| 5 | The metric is computable and means the stated thing: policy-years sorted by the predicted cost per year, the observed cost per year weighted by e | metric reason | The shipped scorer on each of the 9 test folds against an independent Liberty Mutual WG on expm1(y) and on y; constant, perfect and noisy predictions; units per fold | HOLDS | Each test fold has 117,797-118,268 rows, 13,817-14,344 positive and 0 shared policies. Constant scores 0.0 and perfect 1.0 on every fold. A noisy prediction scores 0.98384-0.98583, equal to my reference on the rate to 6 decimals and not to the reference on log1p (0.996): the scorer inverts log1p, so the Lorenz curve is cumulative cost (rate x e). | MET-2, MET-3, MET-15 |
| 6 | Metric origin: context; the article reports no model or evaluation; "an actuary weighs each policy by its time on risk and orders by the cost per year (Frees, Meyers and Cummings 2011 ...; Liberty Mutual ... var11)" | metric reason | PMC page blocked by a captcha (could not re-read the article). Searched Frees et al. 2011 | MOSTLY HOLDS; citation PARTLY REFUTED | Frees, Meyers and Cummings 2011 order by the relativity (score over premium) and accumulate premium on the x-axis. They do not weight by time on risk or order by cost per year. The exposure-weighted, cost-per-year form is Liberty Mutual's WG (weight var11, a sum insured, not a time on risk). The choice itself is the curator's (Andrej, 2026-11-02) and stands as context (MET-11). The record's screening line "Metric: none ... fallback (rmse)" is superseded by its 2026-11-01 Assessment, which is consistent. | MET-1, MET-11, PROV-16 (quote what the source says) |
| 7 | _clean "checks that cost per year x time on risk rebuilds the cost" | dataset.py step 9, CHANGES.md | Read the assertion | HOLDS, but it is a tautology | It recomputes expm1(log1p(cost/e))*e from the arrays it has just built, so only float error can fail it. It cannot catch a wrong denominator column. MET-14 asks for exactly this assertion, so it is compliant. A sharper version would assert against raw total_incurred and raw total_exposure. | MET-14 |
| 8 | Counts behind the exposure call: 89,817/89,882 active portfolio years full; 47,403/47,411 active NB years after a row full; 18,784/18,849 and 13,842/13,850 below-a-year cancelled; 32,626 located; 5,653 first-year; claims per exposure-year 0.50/0.55/0.30/0.27; 49 rows e=0 all cancelled (one claim 180.11); no cancelled year has a later year; on a 1/365 grid in all three years | notes, Decision 3 | Recomputed from the raw file | HOLDS | All exact (0.498, 0.548, 0.300, 0.273). Every exposure x365 is an integer in 2022, 2023 and 2024, with a maximum of 365 days in leap 2024 too. One of the 5,653 first-year cancellations has a full year. | LEAK-41 |
| 9 | Re-measure: new definition 0.3166 (L2) / 0.3165 (Tweedie); premium alone 0.2975; ahead 9/9 and 8/9; exposure free +0.0325 Tweedie / -0.035 L2; 1/e alone 0.075 | notes, CHANGES.md, REVIEW issue 6 | 9 shipped splits, weighted LightGBM, seed 0 (models.csv), and 2 seeds with subsampling (precision_gain.csv) | HOLDS (within seed noise) | L2 0.3169 / 0.3139; Tweedie 0.3125 / 0.3128 (seed SD 0.0045); premium alone 0.2975 exactly; L2 ahead of the premium 9/9 (+0.0194), Tweedie 8/9 (+0.015); exposure free +0.0288 / +0.0331 Tweedie (9/9), -0.0371 / -0.0335 L2 (0/9); 1/e alone 0.0771. Probe 22: Tweedie arm +0.026, L2 arm -0.026, 1/e 0.089 (50k caps, 3 splits). The task probe has LightGBM 0.3165. | LEAK-41, TP-4 |
| 10 | CLEAN-16 note: weighted mean log1p(rate) rises from 0.117 (<0.1 y) to 1.074 (full) among active years, while the cost per year stays 221-336 | notes | Recomputed | HOLDS | 0.117 / 0.241 / 0.479 / 0.693 / 0.956 / 1.074; cost per year 336 / 257 / 221 / 264 / 264 / 274. The rule text's 0.085 is the unweighted mean of the same band (consistent). | CLEAN-16 |
| 11 | Shape and target facts: 354,091 rows, 185,677 policies, 88.1% zeros, 69% NB, 52.4% first years, 8,543 claims at zero cost, 5.5% below 0.1 y holding 0.8% of the cost, max rate 3.72M (571,128 over 0.153), 7,576 of 42,263 positives flat (882 / 1,012 / 1,114) | task_summary, notes | Recomputed | HOLDS | All exact (0.8806, 0.6931, 0.5244, 8,543, 0.0552 / 0.0080, 3,722,533, 7,576 / 42,263). | EV |
| 12 | Splits comment: "On that window untuned LightGBM reaches a normalized Gini of 0.385 ..., against 0.375 to 0.405 on the 2024 rows of the first three folds"; "The pooled score (0.393 to 0.445 over the 9 splits)"; "Random policy-years score about the same as the grouped folds (Gini 0.415 against 0.412)" | dataset.py splits_comment, README | Trained on 2022-2023 and tested on 2024 under the current definition and metric; the 2024 rows of repeat 0's folds | NUMBERS REFUTED, CONCLUSION HOLDS | The 2024 window scores 0.2998 (L2) / 0.3056 (Tweedie), against 0.273-0.331 / 0.279-0.332 on the folds' 2024 rows. The pooled score over the 9 splits is 0.291-0.343 (L2) and 0.272-0.335 (Tweedie). The quoted numbers are the row Gini on the year's cost with total_exposure as a feature, before 2026-11-02, and the text does not say so (the metric reason labels the same numbers as old). The forced split is still no more optimistic than the window. The group probe gives IID 0.047 vs grouped 0.046 R^2. | EV (numbers re-measured on the shipped definition), SPLIT-8, SPLIT-4 |
| 13 | No feature copies across the split; groups disjoint | splits comment ("30 exact copies"), notes (26 repeats) | Probe 5 output; group overlap per fold | HOLDS | 0.0% of 1,062,273 test evaluations have a copy; 0 shared insured_id on every fold. | LEAK-17, LEAK-18 |
| 14 | Every feature is known at the prediction point (implied) | features list | Probe 22 (both arms) and row 1 | HOLDS EXCEPT ROW 1 | Probe 22 predicts the weight from the features at R^2 0.350 (business_type 41%, occupants premium 28%), and no top feature's gain goes through the weight above noise in either arm (largest /mediated/ 0.0147, SD 0.013). The flat-cover mark and the year's last record are kept with notes on Andrej's call (issue 4) and are not reopened here. | LEAK-41, USE-6 |
| 15 | float_precision="round_trip" gives the same checksum under pandas 2.3 and 3 | CHANGES.md, step comment | Not run (no pandas 2.3 env) | UNTESTED | The venv's pandas raises Pandas4Warning: "'float_precision' argument is deprecated". A later pandas may remove it and break _load_raw. | PROV, reproducibility |
| 16 | Dropping total_exposure costs 0.0176 (Tweedie), the new score is 0.011 below the old; the 5,653 cuts gain -0.0002 (-0.0012 net); premium-mark, last-record and first-year numbers (AUC 0.81/0.62/0.79/0.68/0.67, -0.0006 etc.) | notes, CHANGES.md | Not rerun: the old definition is not built, and these were outside the D10 deltas | UNTESTED | Plausible: the probe 22 arms agree in sign and size with the reference numbers. | LEAK-41 |

**Ranked: refuted and untested**


1. (Must, validity; LEAK-41) The annualised premiums encode the cut through their decimal precision (row 1, with row
   2). This changes the D10 premise "no premium carries the time on risk" and the CC's "no remaining column whose
   cancellation signal pays". The located cancellations are readable at AUC 0.965 from precision alone, and the gain
   under weighted Tweedie is +0.0035 (8/9; about 1 seed SD, 11% of the leak reference). LEAK-41 excludes such a column
   "whatever it scores". The late-start part also comes from D10's annualisation (0.5% short decimals before the
   division, 44% after). The located cancellations already had it before 2026-11-06. Mildest remedy: in _clean, round
   every annualised premium to the cent (np.round(x, 2)) right after the division. On my test the precision AUC falls
   to 0.565 (residual trailing zeros), and sub-cent changes should leave the scores alone (untested). This is not the
   rounding Andrej declined on 2026-11-02 (3 significant digits or whole euros, aimed at the flat-amount mark), but it
   touches his "do not round" wording, so it needs the curator's yes. Then re-run row 1's AUC and gain test and quote
   them in the "Premiums annualised" note. Alternative if cents still leave a mark: round to whole euros (curator's
   call, it reopens issue 4's wording).
2. (Should, evidence) The splits comment's numbers are from the old metric and target (row 12). The conclusion
   stands. Remedy: replace with 0.300 / 0.306 on the 2024 window against 0.273-0.332 on the folds' 2024 rows, pooled
   0.27-0.34, or label them "row Gini on the year's cost, before 2026-11-02".
3. (Should, provenance) The metric reason credits Frees, Meyers and Cummings 2011 with exposure weighting and
   cost-per-year ordering (row 6). Remedy: cite Frees et al. for the ordered Lorenz curve and Gini, Liberty Mutual
   2014 for the weighted form, and say that this table's weight is a time on risk (the curator's call).
4. (Could) The _clean rebuild assertion is a tautology (row 7). It complies with MET-14. Optional: assert against raw
   total_incurred and total_exposure.
5. Untested: the pandas 2.3 checksum (row 15; also the deprecation warning) and the old-definition comparison numbers
   (row 16).

Sources: Frees, Meyers & Cummings 2011 summary (https://academicnewsletter.sufe.edu.cn/info/445125); cplm gini docs
(https://rdrr.io/cran/cplm/man/gini.html). PMC13234478 could not be fetched (captcha).

</details>

<details><summary>Column audit</summary>

**Column auditor (AI, 2026-11-06): spanish_motor_insurance_coverage_level_2022_2024, exposure re-review (full tier)**

VERDICT: ship after one small change. There is one new LEAK-41 (Must) finding. Annualising made the premiums' decimal
precision mark the rows cut short. It is not measured to gain anything, and rounding to the cent removes it. The
other cancellation marks are D10's settled keeps, or weak and kept with a note. The `business_type` keep needs a
note it does not have yet. One CLEAN-14 typing fix (`bonus_score` is ordinal).

How the numbers were made: the frame was loaded with dataset_io.from_definition (raw=True, traced by the column) from
the PR #47 worktree, with thread caps. dtype_probes.py flagged 0 of 23 columns ("no codebook"; I read the variable
sheet "Descriptive of variables.xlsx" by hand). The gains are untuned LightGBM (200 trees, subsample/colsample 0.8),
fitted with actual_exposure as the row weight, by Tweedie on the cost per year and by L2 on log1p. They are scored by
the declared metric (data_foundry.v2.metrics.score) on the first 3 shipped splits x 2 seeds.

Row kinds used below (the frame's 354,091 rows; "in force 1 Jan" = portfolio, or a row of the same policy the year
before):
- in force 1 Jan, active 137,293 (73 part-year)
- in force 1 Jan, cancelled (located) 32,626 (all part-year)
- first year, active 178,519 (168,257 part-year: late starts)
- first year, cancelled 5,653

**Column table** (prediction point: when the policy is written or renewed for the year; row = the policy's last record
in the calendar year)

| column | meaning (codebook) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| insured_id | recoded policy number, "sequential ID based on the first appearance" | n/a (group) | int64, group column, not among the 23 features | fine; it encodes the entry order but is never an input | LEAK-33 |
| year | calendar year | yes | int64 numeric | fine (carries the year's CICOS flat amount; explains 6% of probe 22's weight fit through 2022's second calendar years) | - |
| policy_type | cover structure TP/TPG/CC/COMP_E/COMP_N | yes; last record's value | category, 5, unordered (partial order: CC need not include glass) | fine, kept with the settled last-record note | LEAK-10 (weak, settled issue 4) |
| business_type | "business origin": new business / portfolio | partly NO: last record's value. In a second calendar year it flips during the year, so for a cancelled year it is read at the cancellation date | category, labelled | weak cancellation mark, no gain; the note is missing (problem 2) | LEAK-41/LEAK-10 (weak) |
| payment_frequency | annual / semiannual / quarterly billing | yes | category, labelled, unordered | fine (it predicts first-year cancellation through selection, USE-6); optional ordinal (problem 4) | USE-6; CLEAN-14 |
| bonus_score | past claims experience: favourable / neutral / poor | yes; last record (worsens 0.28% vs 0.03%, settled) | category, unordered | cleaning problem: an ordinal scale with words for every level, so ordered (problem 3) | CLEAN-14 |
| driver_age | main driver's age, years | yes | int64 18-90 | fine | - |
| years_licensed | source vehicle_age; driver_age = it + age_at_licence on 99.92% | yes | float64, 36 masked | fine (rename holds) | CLEAN-12, CLEAN-11 |
| age_at_licence | source age_driving_licence (the sheet says "calendar year of issuance"; values 15-80 are ages) | yes | float64, below 15 masked (34) | fine | CLEAN-11 |
| fuel_type | diesel / gasoline, "only two categories are kept" | yes | category, 1,287 missing kept | fine | CLEAN-10 |
| vehicle_value | declared insured value | yes; last record | float64, 513 missing | fine; no precision mark (5-dp grid share 0.83-0.88 in all four row kinds) | LEAK-10 (weak, settled) |
| seats | number of seats | yes | int64 count, numeric | fine | CLEAN-14 |
| weight_to_power_ratio | kg per hp (renamed from power_to_weight_ratio) | yes | float64, 3 zeros masked | fine | CLEAN-11 |
| vehicle_brand | brand | yes; last record | category, 68 | fine (settled note) | LEAK-10 (weak) |
| municipality_type | inland/coastal/islands | yes | category | fine | - |
| circulation_area | urban/rural | yes | category | fine | - |
| total_premium | sum of the 7 cover premiums; earned in the release, here divided by actual_exposure | the price at writing is known, but an active year blends in the renewal price set at the anniversary; the annualising makes its precision mark the cut | float64 | LEAK-41 precision mark (problem 1); blend mark kept by D10 | LEAK-41 Must; USE-6 |
| liability_premium | TPL premium, annualised | as total | float64, 23 zeros masked | as total_premium | LEAK-41; CLEAN-11 |
| property_damage_premium | own-damage premium, annualised | as total | float64, 0 = cover absent | as total_premium | LEAK-41 |
| theft_premium, fire_premium, glass_premium | cover premiums, annualised | as total | float64, 0 = absent | as total_premium | LEAK-41 |
| legal_protection_premium | legal protection premium, annualised | as total; a flat-tariff cover (blend mark, D10) | float64 | as total_premium | LEAK-41 |
| occupants_premium | occupants' injury premium, annualised | as total; a flat-tariff cover (blend mark, D10); 28% of probe 22's weight-fit gain | float64 | as total_premium | LEAK-41 |
| log1p_incurred_per_exposure_year | target: log1p(total_incurred / actual_exposure) | target | float64; _clean asserts that cost per year x exposure rebuilds the cost | fine | MET-3, CLEAN-16, MET-14 |
| actual_exposure (scoring column, weight) | total_exposure: days in force / 365 | realized (cut by cancellation) | float64 0.00274-1, 1/365 grid; ScoringColumn(role="weight"), sample_weight; not among the features | fine (MET-15). The 49 zero rows are dropped under USE-7, which LEAK-41 allows | LEAK-41, MET-15 |
| dropped: total_exposure, liability_exposure, policy_status, 10 claim counts, 9 incurred parts | - | post-outcome, a copy of the weight, or parts of the target | - | right | LEAK-41, LEAK-10 |

The weight (probe 22, both arms). The features fit actual_exposure at R^2 0.350 (Spearman 0.639). Gain shares:
business_type 41%, occupants_premium 28%, year 6%, legal_protection_premium 5%, payment_frequency 3%. Leak reference,
the weight as a feature: +0.0264 under Tweedie, -0.0261 under L2. 1/weight alone scores 0.089 against the honest
0.272/0.269. Weight-mediated gain of every top feature:
- Tweedie: -0.0028 to -0.0147.
- L2: -0.0118 to +0.0003.
So none is above noise, and the worse arm finds nothing either. Most of the R^2 is start-known: first-year rows are
NB and mostly late starts (168,257 of 178,519 below a year), which the insurer knows when it writes them (USE-6).
Within each row kind, occupants_premium has no rank correlation with the exposure (Spearman -0.11 to 0.01). Its 28%
comes from telling single-tariff rows from blended ones. That is the flat-amount mark D10 kept, plus the start-known
first-year split.

**Problems, ranked by principles.md (validity first, Must first)**

1. P4, LEAK-41 (Must; new): the annualised premiums' precision marks the cut.
   - The mechanism. The source holds the annual tariffs on a 5-decimal grid. An earned premium (annual x days/365)
     has 12-15 decimals. Divided back by actual_exposure, a part-year row returns to the grid, up to float error. A
     full year keeps its long decimals, either because exposure is 1 or because it blends two tariffs.
   - Measured at 1e-4 of a 1e-6 grid unit:
     total_premium sits on the 1e-6 grid on 83.8% of the located cancellations, against 2.8% of active
     in-force-1-Jan years. Among in-force-1-Jan rows the flag ranks the cancellation at ROC AUC 0.905; across all
     rows it ranks part-year against full-year at 0.924. Every cover premium shows the same, in all three years
     (78-84% of located cancellations).
   - Within first-year part-years the flag does not separate cuts from late starts (AUC 0.484). Among the rows in
     force on 1 January, where a short year means a cancellation, it gives the cut away.
   - LEAK-41 names this case: "neither is a column that encodes it: ... a value whose precision marks the cut". The
     rule applies whatever the column scores. The earned premiums had no such mark (1e-6 grid share 2.1% for
     part-year rows, 2.8% for full years), so annualising created it.
   - Strength: nothing measured. The flag added as an explicit feature changes the declared metric by -0.0024 (SD
     0.0078) under Tweedie and -0.0109 (SD 0.011) under L2. A perfect part-year flag would give +0.0091 and -0.0111.
     Trees cannot read decimals, but a model that reads values as text could.
   - The claims "no premium carries the time on risk" (dataset.py _clean step 5 comment; Premiums-annualised bullet;
     CHANGES.md; REVIEW.md issue 6 option A "no input carries the time on risk") are false as written.
   - Mildest remedy: round every premium to the cent after annualising, in _clean step 5:
     `df[premiums] = df[premiums].div(df["actual_exposure"], axis=0).round(2)`
     After this, no decimal grid from 0.1 to 1e-4 separates the located cancellations: the largest |AUC - 0.5| is
     0.009 (occupants at 0.1 is 0.491; at 1e-3 after round(4) it is 0.481). Score: -0.0017 (SD 0.0085) under Tweedie,
     +0.0101 (SD 0.009) under L2, both within noise. Rounding to 5 decimals is not enough: legal_protection at 1e-4
     keeps AUC 0.533.
   - Rounding to the cent keeps every price. It differs from what Andrej declined on 2026-11-02 (whole euros or 3
     significant digits, to blunt the flat-amount mark, which cent rounding does not touch). Lennart's D10 kept the
     premiums unrounded without knowing about this mark. So it is the curator's call to confirm, on the new fact.
   - The texts to fix: the step-5 comment and the bullet ("annualised and rounded to the cent, since an annualised
     part-year falls back on the tariff's 5-decimal grid"), plus the leak_checks.md case row if it quotes the claim.

2. P4, LEAK-41 / LEAK-10 (weak, kept; a note is missing): business_type is read from the last record and carries
   whether the year was cut.
   - In a policy's second calendar year the NB flag flips to portfolio during the year, at a date tied to the start.
     By the year before's exposure band, the share still NB at year end is 0.89 for Oct-Dec starters and 0.21-0.23
     for Jan-Mar starters.
   - A cancelled year's last record comes before the flip more often. Within every start band, cancelled second
     years are NB 3-10 pp more often (0.92/0.74/0.53/0.30 against 0.89/0.65/0.44/0.21 in 2023, the same in 2024;
     0.51 against 0.43 overall). Among in-force-1-Jan rows, NB years are cancelled at 0.22-0.23, portfolio years at
     0.16-0.17.
   - Its value at the prediction point (NB on 1 January) is not what ships.
   - Strength: probe 22 gives it 41% of the weight fit, but its weight-mediated gain is -0.0040 (Tweedie) and -0.0118
     (L2). Through the weight it gains nothing; its tie to the weight is mainly the start-known first year.
   - The definition's last-record bullet lists type, brand, bonus class, vehicle, payment and area, not
     business_type. LEAK-41 asks the definition to report each suspect column's gain on both fits.
   - Mildest remedy: add business_type and these numbers to the last-record bullet, with probe 22's line (R^2 0.35,
     shares, no gain through the weight on either arm, 1/weight 0.089).
   - An alternative for the curator: a start-known stand-in, "the policy's year in the file" (a row the year before),
     instead of the flag. It is known on 1 January from 2023 on, but undefined in 2022. Question 4 of the 2026-11-01
     column audit asked for one sentence; it did not reach the definition.

3. P7, CLEAN-14 ordinal clause (Should): bonus_score is typed unordered.
   - The sheet gives words for every level ("G: Positive reflects a favourable claims history", "N: neutral
     profile", "B: ... poor claims history"). Under the 2026-11-01 marks that makes it an ordered category.
   - Remedy: `FeatureTypes(categorical=[...without bonus_score], ordinal={"bonus_score": ["bad", "neutral", "good"]})`.
     The order comes from the meaning, not the target. bemtpl97's `coverage` ordinal is the house precedent in this
     family.

4. P7, CLEAN-14 (optional): payment_frequency is a frequency, so it can be ordered as annual < semiannual < quarterly
   (1, 2, 4 instalments). "Categorical by default" also holds, so this is the curator's call. policy_type rightly
   stays unordered: CC need not include glass, so the order is partial.

Settled and not reopened (D10, 2026-11-06):
- The blend mark of the flat-tariff covers (ROC AUC 0.81; option C declined).
- The year's last record for the other attributes.
- First-year cancellation from the payment frequency and the year (known at writing).
On the brief's timing question: the blend mark is not known at writing or renewal. An active year's annual premium
includes the renewal price set at the anniversary, after 1 January and after part of the year's claims. It is
missing exactly when the year ends before the anniversary. So the keep is a curator's call against LEAK-41's
"whatever it scores", resting on USE-6 and the measured zero gain, not a timing pass. fit_reason and the
potential-leak bullet already say this.

Checks that hold:
- 23 features, no exposure column among them.
- actual_exposure is the weight scoring column and the sample_weight.
- The premiums' Spearman with the exposure is about 0 within each row kind (total: 0.04, 0.03, -0.01, -0.05).
- vehicle_value and weight_to_power_ratio carry no precision mark.
- The renames, masks and labels are as the 2026-11-01 audit found them.

</details>

<details><summary>Split audit</summary>

**Split auditor (AI, 2026-11-06, exposure re-review, full tier): spanish_motor_insurance_coverage_level_2022_2024**

VERDICT: right with notes. The forced grouped split by `insured_id` (ForcedGroupedFromTemporal, Andrej 2026-11-02)
still stands under the new definition (rate target, time on risk as the training and metric weight, annualised
premiums). Measured against the one valid window, it is within noise of it. SPLIT-8's leak test in wisconsin's form
finds a small shared-period gain of 0.005 to 0.010 Gini on the pooled score, about 2-3% of the score. It comes from
within each year, not from a year's claim level. The time on risk is cut by the calendar year, the release end the
same as every other year end, and no split selects rows by it. LEAK-41's no-selection clause holds. What needs
changing is text: every number in `splits_comment` is from the old target and the row Gini, and the leak test should
give its new result.

Setup: definition rebuilt through dataset_io.from_definition (354,091 rows, 23 features, `actual_exposure` a scoring
column and the training weight). Untuned LightGBM (200 trees, lr 0.05, 31 leaves, subsample/colsample 0.8, 4 threads),
fitted with the time on risk as the row weight, both as L2 on log1p and as Tweedie (p 1.5) on the cost per year.
Scored by the library's _normalized_weighted_gini (cost per year, weight `actual_exposure`). Seed 0 unless stated.

**What holds (numbers)**
- Regime (USE-10, SPLIT-8, SPLIT-14). The use case is renewal pricing of a stream of years. 62.7% of the 2024 rows are
  known policies. The release has years only: a 2024 window trains on 52.5% of the rows, and a 2023 window on 19.0%
  (below SPLIT-14's floor). So there is one valid window where SPLIT-14 asks for three, and SPLIT-8 sends the task to
  the grouped regime because policies recur. That has not changed. Record: `Grouped (NON-IID)` / `Non-IID (Grouped)`,
  as the 2026-11-02 call asked.
- Group integrity (SPLIT-24). `insured_id` is the authors' sequential policy number, a true id. In 9 of 9 shipped
  splits no policy is on both sides. Test folds hold 117,797 to 118,268 rows, 18.9-19.1% / 33.5-33.7% / 47.3-47.5% by
  year. One prediction is one policy-year from its own row; the id is not a feature.
- Forced split against the valid window (train 2022-2023, test 2024; 3 seeds; bootstrap SE over 200 resamples):
    - L2 on log1p: window 0.302 / 0.300 / 0.307 (SE 0.012); grouped folds' 2024 rows 0.274-0.333, mean 0.309
    - Tweedie: window 0.305 / 0.316 / 0.312 (SE 0.011); grouped folds' 2024 rows 0.292-0.332, mean 0.311
  The forced split is 0.006 (L2) and 0.000 (Tweedie) above the window on the newest year, well inside the window's SE.
  The two fits keep their order on both designs: Tweedie ahead by 0.0015 pooled on the folds and by 0.008 on the window.
- Pooling the years: the pooled score minus the mean of the three within-year scores is -0.017 to +0.012 per split
  (mean -0.002 L2, -0.003 Tweedie). The years' cost per exposure-year is flat (293 / 285 / 302 EUR), so a ranking across
  years gains nothing. Within-year means: L2 0.317 / 0.326 / 0.309, Tweedie 0.315 / 0.329 / 0.311 (2022 / 2023 / 2024).
- Hidden groups and copies (SPLIT-29, SPLIT-30, LEAK-16). Random policy-years (3x3 KFold) against the grouped folds,
  pooled: L2 0.3178 against 0.3150 (+0.003), Tweedie 0.3143 against 0.3165 (-0.002). Group probe: R^2 0.047 IID
  against 0.046 grouped. Leak probe: 0.0% of test rows have an exact feature copy in training. The earlier bound on
  cross-id entities (about 750 related pairs, about 100 rewritten policies a year) still applies. No action.
- Label delay (SPLIT-10, LEAK-24). Claims per exposure-year 0.302 / 0.305 / 0.312 and cost per exposure-year 293 / 285 /
  302 (2022 / 2023 / 2024). Active first-year rows with at most 0.25 years on risk, the policies written last before the
  release end: 0.247 / 0.252 / 0.277 claims per exposure-year. No sign of immature 2024 labels, so no gap.

**Time on risk, the release end and LEAK-41's no-selection clause**
- Every row is a calendar-year slice, so its time on risk ends on 31 December at the latest. The release end
  (31 December 2024) cuts the 2024 rows exactly as 31 December cut 2022 and 2023. A 2025 cancellation does not shorten
  a 2024 row. The distributions agree:
    * active first-year time on risk, quartiles: 2023 0.236 / 0.452 / 0.641; 2024 0.227 / 0.479 / 0.723;
    * cancelled share of renewal years: 19.9% in 2023, 18.8% in 2024 (status read from the raw file, for this check
      only).
  The release end therefore admits no row by its realized end. Unlike pricing_game_2016_french_fleet (SPLIT-9,
  LEAK-41), no training side admits periods by when they ended:
    * the folds admit rows by policy;
    * the valid window takes the complete years 2022-2023;
    * my leak test drops rows by calendar year.
- No model is trained or scored on rows selected by `actual_exposure`. All 354,091 rows are in every split. The 49 rows
  with zero time on risk are dropped under USE-7 (their one claim of 180.11 is counted in the notes), which the clause
  allows.
- The release start is the one asymmetry. The 2022 rows are all a policy's first year in the file: 83.2% part-years,
  mean time on risk 0.62, 6.0% cancelled, against 11.3% and 12.3% in 2023 and 2024. Some are a policy's second calendar
  year (the notes already say so for the 5,653 first-year cuts). This explains why 2022 is the year that most needs its
  own training rows (below). It is not a selection by the weight.

**Problems, ranked (principles.md)**
1. P4, SPLIT-8 (Must: a leak test across a forced split, its result weighed). A small shared period crosses the split.
   It is measured, it sits within the window's noise, and it is not in the notes yet.
   - Did spanish's earlier test look within a year? No.
     * The 2026-11-02 test (record Assessment) ran wisconsin's drop-the-year form on the pooled row Gini of the old
       target: +0.005, SE 0.005, 4 of 9.
     * Its other year tests add the training side's year mean as a feature (+0.0000; year x area +0.0009). On
       wisconsin that form found nothing where the drop test found +0.113, so it is not decisive.
     * The 2026-11-01 split audit scored within years, which rules out a cross-year ranking gain only.
     * Nothing was re-run after the 2026-11-06 change of target, weight and features.
   - Today's run, in wisconsin's form. For each shipped split and test year, one model is trained without that year's
     training rows (B) and one without as many random training rows (C). Each test row is predicted by the model of its
     own year. Gain = C - B, 9 splits:
       - L2 on log1p: pooled +0.0101 (SE 0.0020, 9 of 9); 2022 +0.029 (SE 0.010, 7 of 9);
                     2023 -0.003 (1 of 9); 2024 +0.011 (SE 0.0025, 9 of 9)
       - Tweedie: pooled +0.0045 (SE 0.0032, 6 of 9); 2022 +0.002; 2023 +0.006; 2024 -0.001 (5 of 9)
     Without the `year` feature: L2 pooled +0.0064 (SE 0.0020, 7 of 9), Tweedie +0.0077 (SE 0.0022, 8 of 9).
     Size alone (full training side A against C): +0.001 L2, +0.005 Tweedie, pooled.
   - Reading. What crosses is within each year: the pooled gain equals the within-year gains, and the years' cost
     levels are flat. So this is not wisconsin's year claim level (+0.113 pooled, +0.008 within a year there). It is
     the year's own mapping from premiums and factors to cost (tariff and inflation drift), plus the release-start
     cohort for 2022. A model priced for 2024 could not have seen 2024's outcomes, so this is the forced split's
     optimism. It is about 2-3% of the 0.315 score. It agrees with the direct comparison on 2024 (+0.006 L2, 0.000
     Tweedie against the window), and the window's own SE is 0.011-0.012. Weighed as SPLIT-8 asks: no leak to remove
     (no column carries it; dropping `year` leaves it), and too small to reopen the 2026-11-02 call.
   - Mildest remedy: text only. In `splits_comment`, replace the leak-test sentence with these numbers, for example:
     "a model trained without the test year's own training rows scores 0.006 to 0.010 Gini lower than one trained
     without as many random rows (pooled, 9 splits; within each year, since the years' cost per exposure-year is flat
     at 285-302), the forced split's optimism over a model that cannot see its year."

2. P4 (text), SPLIT-8 ("the cost measured"). Every number in `splits_comment` is stale: it comes from the old target
   (the year's cost), the row Gini and the unweighted fit. Stale against measured:
     * window 0.385 (SE 0.021) against 0.375-0.405 on the folds' 2024 rows -> now 0.303 L2 / 0.311 Tweedie (SE
       0.011-0.012) against 0.274-0.333 / 0.292-0.332 (means 0.309 / 0.311);
     * pooled 0.393 to 0.445 -> now 0.279-0.344 L2 and 0.280-0.337 Tweedie (seed 0); CHANGES.md: 0.317 over 3 seeds;
     * random policy-years 0.415 against 0.412 -> now 0.318 against 0.315 (L2), 0.314 against 0.317 (Tweedie);
     * renewal gain from last year's claims (+0.001 to +0.007) and the year-mean leak test (+0.0000, +0.0009): old
       metric, not re-run;
     * "2022 and 2023 rows rank more easily than 2024 rows": now holds weakly. 2023 is above 2024 by 0.017-0.018;
       2022 is above 2024 by 0.008 (L2) and 0.004 (Tweedie).
   The metric reason's "0.177 to 0.221 against 0.393 to 0.445" is labelled as the earlier row Gini, so it can stay.
   Remedy: rewrite the measured clauses of `splits_comment` with the numbers above (README regenerates with it). The
   conclusions do not change: the forced split is no more optimistic than the window for the newest year, and IID
   scores as grouped.

3. Weigh, for the notes. The 2022 rows are the release-start cohort (first year in the file, 6.0% cancelled against
   11-12% later, mean time on risk 0.62). They are the year most helped by their own training rows under L2 (+0.029,
   7 of 9). This is an approximate-fit fact of the forced split (USE-8), not a selection by the weight. Optional one
   clause; no remedy.

Nothing found that makes the split wrong. No re-split, gap or filter is needed.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner: spanish_motor_insurance_coverage_level_2022_2024 (exposure re-review, 2026-11-06, full tier)**

I play the pricing actuary of a Spanish motor insurer. When a policy is written or renewed, the tariff gives it a
premium per year insured. Once a year I review the tariff against the latest claims and look for segments where it is
wrong. This review covers only what decision D10 changed: `actual_exposure` is now the training weight and the metric's
weight, every premium is annualised, and `total_exposure` is out of the features. The earlier practitioner block in
REVIEW.md (fit approximate, missing rating factors, the calendar-year slice) still stands, and I do not repeat it.

**Verdict**
- Fit: approximate. I agree with the definition. The rows are real policy-years with the insurer's own rating factors
  and prices, and the target is the loss cost I price. But held-out policies from the same three years stand in for
  next year's book, which is mostly renewals (USE-8, SPLIT-8 forced). D10 does not widen that gap.
- Metric: yes. The exposure-weighted Gini of the cost per year, ordered by the predicted cost per year, is the
  actuary's model-lift Gini (cumulative earned car-years on x, cumulative incurred loss on y). It satisfies MET-14 and
  MET-15. The premium-base Gini of Frees et al. is a useful second view; I would not replace the declared metric with
  it. Details in 5.
- D10 is right from the pricing side. I would make the same three changes.

**1. Inputs at the prediction point**
- The annualised premiums: yes, I have them. When I write or renew a policy I know the annual price of each cover for
  the term. The release gives premiums earned pro rata. The notes show this: the median premium per year on risk is
  340 to 355 in every band of time on risk, cancelled years included. That matches pro-rata refunds when a vehicle is
  sold or written off. So dividing by the recorded days in force gives back the annual price. USE-6 keeps the
  premiums as my own estimate, which the model refines.
- Two caveats, both already in the notes as kept potential leaks. Neither is a reason to change the task:
  (a) When a renewing policy's anniversary falls mid-year, the row's annualised premium blends last term's price
      with the renewal price. The renewal price can react to claims made earlier in the same calendar year. On
      renewal years without a prior claim, the premium per year moves +1.4% when the year has a claim and +0.4% when
      it does not. This year's premium is worth +0.012 more than last year's under both weighted fits, and the
      release cannot say how much of that is reaction to this year's claims. This is the largest open timing question
      that remains. Bonus-malus here barely reacts to claims (in the earlier block, 94.4% stay "good" after a claim),
      which argues it is small. A record from the anniversary (the authors' first record of each year) would settle
      it.
  (b) The two flat-priced covers (occupants, legal protection) mark a located cancellation at ROC AUC 0.81. The notes
      measure no gain from this on the declared metric (-0.0006 Tweedie, -0.0010 L2). I agree with option A over C:
      turning those covers into flags would discard real price information (0.010 to 0.012) to remove a mark that
      gains nothing.
- The time on risk as an input: I would not have the realized time on risk when I price, since a cancellation or a
  total loss cuts it later. A rating plan also never uses a policy's in-year length as a rating factor. The rate is per
  year insured, and the length belongs in the weight. So dropping `total_exposure` is right (LEAK-41). The 0.0176
  that the corrected copy gained under weighted Tweedie is the planned time of policies starting mid-year. I would
  know the start date, but I would not price on it. It is not a loss to my decision.
- What I always have and the data lacks is unchanged: vehicle age, postcode or province, make-model group, the
  SINCO/TIREA claim file, sales channel, and last year's claims at renewal. The start date is now also gone as an
  input, but see above.

**2. The target**
- The year's claim cost (paid plus reserved) divided by the years insured is the pure premium, or loss cost: the
  quantity I price (USE-5, MET-14). `_clean` checks that rate times time on risk gives back the cost. I want a number,
  the expected cost per year insured, right in level and in relativity.
- log1p is a shipping scale, not what I act on. The Gini inverts it and is unaffected by rank-preserving transforms,
  so the metric does not care. The fits do: on 3 shipped splits (my check), weighted L2 on log1p predicts on average
  0.8% of the actual cost (level ratio 0.008). Weighted Tweedie on the rate predicts 0.81 of it. On the declared metric
  both rank about the same (0.313 against 0.306). Nobody should read the L2 predictions as prices. The definition's
  metric reason already says that pricing sets the level separately.

**3. Weighting policy-years by their realized time on risk**
- Yes. Earned exposure is the standard weight for a pricing model. Either Tweedie on the pure premium weighted by
  exposure, or frequency with log(exposure) as offset times severity (MET-14: the compound-Poisson convention). A year
  cut short by a total loss keeps its full claim cost and its short exposure. Weighted, it contributes exactly its
  cost to the book, which is how my experience studies count it. Scoring and training on the same weight is right
  (MET-15: a declared sample weight is the metric's row weight).
- Weighted L2 on log1p has no actuarial meaning: it estimates an exposure-weighted mean of log1p(rate). It ranks fine
  only because the time on risk is not an input. The notes measure this: given exposure as a feature, the weighted L2
  fit loses 0.035. That is a benchmark compromise, not a gap in the task.
- One row is still a calendar-year slice from the year's last record, not the 12-month term I price. Exposure
  weighting partly bridges this: two slices of one term add up to the term's exposure.

**4. Would I use the model?**
- As a challenger to my tariff, yes. On my 3 splits the premium alone scores 0.297 on the declared metric, and the
  weighted fits score 0.306 to 0.313. On the premium-base Gini, which measures only what the model adds beyond my
  price, they score 0.109 (L2) and 0.111 (Tweedie). This is a real refinement of the tariff (TP-4).
- What would make me trust it: a double-lift chart against the premium on a later year, and the anniversary-date
  record that removes caveat (a).
- What would make me distrust it as a tariff: the core rating factors are missing, so the model ranks mostly through
  my own price (0.297 of 0.313). It is also an unnamed insurer and a young book.

**5. The metric**
Does `normalized_weighted_gini` (weight `actual_exposure`, target_transform log1p) score my decision? Yes.
- It sorts the policy-years by predicted cost per year and accumulates losses against earned years insured. This is
  the model-lift Gini that CAS ratemaking material uses: sort the holdout by predicted loss cost, cumulative earned
  car-years on x, cumulative incurred loss on y. The decision is "rank the risk per year insured", and the unit is the
  year insured (MET-1, MET-14, MET-15). The defect of the row Gini, where time on risk alone scored 0.177 to 0.221, is
  gone. 1/time on risk now scores 0.075 on 9 splits and 0.089 in probe 22, against 0.27 to 0.32 for the honest fit.
- My check: the premium-base Gini of Frees, Meyers and Cummings (2011). It orders by relativity (predicted rate over
  annual premium), uses earned premium as the base and actual cost as the loss. I used `_ordered_lorenz_gini`, with
  base = total_premium x actual_exposure. Results on shipped splits 0-2, weighted LightGBM, 300 trees:

  | split | model | declared | premium-base Gini |
  |---|---|---|---|
  | 0 | Tweedie | 0.3361 | 0.1401 |
  | 0 | L2 log1p | 0.3295 | 0.1165 |
  | 0 | premium | 0.3138 | 0.0000 |
  | 1 | Tweedie | 0.2831 | 0.0841 |
  | 1 | L2 log1p | 0.3037 | 0.1026 |
  | 1 | premium | 0.2882 | 0.0000 |
  | 2 | Tweedie | 0.2995 | 0.1079 |
  | 2 | L2 log1p | 0.3046 | 0.1083 |
  | 2 | premium | 0.2903 | 0.0000 |

  The two metrics order the two fits the same way on 3 of 3 splits (split 2 is close to a tie on the premium base). The
  declared metric carries a large shared part, the premium's 0.29 to 0.31, so the gaps between models look smaller.
  It does not reorder them. So I would not switch.
  If the curator wants the tariff-review reading, the premium-base Gini is the one to add. It needs the release's own
  earned total premium (the raw `total_premium`) as a scoring column, never a feature, alongside the annualised feature.
  That is a curator's call, not a defect.
- What neither Gini scores is the level and spread of the prices. A weighted Tweedie or Poisson-gamma deviance would
  (a strictly proper score for the mean; MET-8 prefers a proper rule when one fits). But the benchmark's default
  models fit squared error on log1p, which gives the 0.8% level above. A deviance would rank the target scale, not the
  model, and it needs a clipping rule for predictions of zero. Pricing calibrates the level afterwards anyway. So the
  Gini is the right benchmark choice.
- MET-6, MET-7 and MET-9 do not apply: pricing acts on a number for every policy, with no threshold, no cost matrix and
  no top k.

**Gaps between the dataset and the real decision, ranked by how much they change the task**
1. Held-out policies from the same years stand in for next year's book of renewals (the approximate fit, SPLIT-8).
   Unchanged.
2. The core rating factors I always have are missing (vehicle age, area, make-model, SINCO, channel, last year's
   claims), so the task is "refine the insurer's price" more than "build a tariff". Unchanged.
3. The calendar-year blended premium of a renewing policy can contain a renewal price that reacted to this year's
   claims. Kept on purpose; this year's premium is worth +0.012 more than last year's, and the release cannot say how
   much of that is reaction. This is the largest remaining open point, and it is not new.
4. Each row is the year's last record and a calendar-year slice, not a 12-month term. Exposure weighting now bridges
   part of this. Unchanged.
5. New with D10, and minor: the planned time of mid-year starts is gone as an input (-0.0176 under Tweedie). It is not
   a rating factor I would use, so it is no gap in my decision.

**What an expert in the domain would change (text only; no change to the task)**
- `fit_reason`: "policies starting during the year lack their planned time on risk" is listed as a gap. To a pricing
  actuary it is not one: the rate is per year insured, the planned length is not a rating factor, and it now sits
  correctly in the weight. The approximate fit rests on the split. I would cut that clause or move it to the notes.
- Metric reason: it credits the exposure-ordered, exposure-weighted form to Frees, Meyers and Cummings (2011). Their
  Gini is the premium-base, relativity-ordered form. The exposure-base model-lift Gini is CAS ratemaking practice
  (Goldburd, Khare, Tevet, CAS Monograph 5) and the form of the Liberty Mutual competition. I would cite it that way.
  I would also state the current ceiling (1/time on risk alone 0.075) and the premium alone (0.298) next to it.
- Optional, for the curator: the premium-base Gini as a recorded second view, with the raw earned `total_premium` as a
  scoring column (numbers above).
- Keep option A over C, and keep the premiums unrounded.


**Sources**
- Definition, README and REVIEW.md (issues 3 to 6, earlier practitioner block); CHANGES.md and the probes (probe22.txt,
  task.txt, leak.txt).
- Rules: use_case.md USE-5, USE-6, USE-8, USE-10; metrics.md MET-1, MET-6 to MET-9, MET-14, MET-15; leak_checks.md
  LEAK-41.
- Data article: Espinosa, Lledó and Atance 2026, Data in Brief 66:112883 (as quoted in the definition).
- Frees, Meyers and Cummings 2011, JASA 106:1085-1098 (premium-base ordered Lorenz Gini).
- CAS ratemaking material on the model-lift Gini, through a web search; I could not open the PDFs, so this is from
  search summaries only: https://www.casact.org/monograph/cas-monograph-no-5 (Goldburd, Khare, Tevet; Gini index
  section), https://www.casact.org/education/rpm/2016/presentations/PM-LM-4.pdf,
  https://casact.org/sites/default/files/presentation/annual_2015_presentations_p-6.pdf.
- My check: weighted LightGBM, 300 trees, shipped splits 0-2 of repeat 0, seed 0.

</details>

<details><summary>Blind review</summary>

**Blind review: spanish_motor_insurance_coverage_level_2022_2024**
Clean room: a sample of 200,000 of the 354,091 rows and the task sheet.

VERDICT: Include with changes. It is a real motor-insurance pricing task with honest features and a sensible
exposure weight, but the target (log1p of the incurred cost per exposure-year) is not a quantity an actuary
prices on. It should be redefined, or at least justified, and the year drift should be handled explicitly.

**Task**
An insurer's pricing or underwriting team predicts the expected loss cost per policy-year (pure premium) from
policyholder, vehicle and tariff variables, at underwriting or renewal time, to set or review the tariff.
This is a real and common use. Source (Mendeley, CC BY 4.0, Espinosa/Lledo/Atance): "anonymised microdata on
automobile insurance policies", Jan 2022 to Dec 2024, ~354,140 records x 47 variables, "each row corresponds to a
policy transaction". Each (insured_id, year) appears once in the sample: 87k insureds have 1 row, 43k have 2,
9k have 3.

**Concerns (most to least serious)**

1. The target transform does not match the weight or the business quantity (moderate to serious).
   - Target = log1p(incurred / exposure). 88.0% of rows are zero (85.7% exposure-weighted). The incurred
     cost recovered from it (expm1(y)*exposure) has median 932 and p99 15.6k, up to 347k. The annualised
     rate goes up to 838k.
   - Dividing by a small exposure and then taking the log inflates short-exposure claims. Mean positive y is
     9.54 for exposure <= 0.1 and 6.65 for exposure = 1. Positive rate per exposure-year falls only mildly:
     0.29 -> 0.16.
   - So E[y | x] depends on exposure, which is not a feature. Adding exposure as a feature lifts weighted R2
     from ~0.046 to ~0.058.
   - The exposure weight is the standard actuarial choice for a rate target (Buhlmann/Tweedie). It is right
     in spirit, and it does keep short-exposure rows harmless: rows with exposure < 0.25 hold only 1.3% of
     the weighted sum of squares.
   - But weighted MSE on log1p(rate) estimates a weighted mean of a log. That is neither the pure premium
     nor a quantity with clear variance-per-exposure behaviour. Back-transforming it gives a biased,
     geometric-mean-like quantity.
   - Change: use target = incurred / exposure (pure premium), weight = exposure, and a Tweedie/Poisson-deviance
     or weighted RMSE/Gini-style metric. Or, if the benchmark only supports squared error, keep the log target
     but state plainly that it is a heavy-tail stabiliser, and keep exposure as the weight (do not drop it).
     A clean alternative task: binary claim/no-claim, with exposure as an offset or weight.
   - On the question asked: using actual_exposure as the training weight and score weight is right for a
     per-exposure target. It must not be a feature: realised exposure includes mid-term cancellation, which is
     unknown at pricing time.

2. Weak signal (moderate).
   - Grouped 3-fold LightGBM, exposure-weighted R2: 0.042 / 0.048 / 0.048. Without premiums: 0.033-0.039.
     Premiums alone: 0.038-0.045. Unweighted fit: about the same.
   - This is typical for claim-cost data, and with 354k rows the scores are stable (fold spread ~0.006).
   - Still, most methods will cluster near the mean, so the benchmark will separate them weakly.
   - The Tweedie or binary reframing in concern 1 would give a more discriminative score (Gini/AUC).

3. Premium columns are the insurer's own tariff output (moderate, mostly framing).
   - total_premium equals the sum of the 7 coverage premiums exactly (ratio 1.000 on every row): 8 columns
     carry 7 degrees of freedom.
   - Premiums are known at underwriting, so this is not leakage. Correlation with exposure is -0.003, so they
     are annualised written premiums, not earned.
   - But a model that uses them learns "loss given the current tariff" (tariff review / loss-ratio
     modelling), not stand-alone pricing.
   - Change: either keep them and describe the task as tariff review, or drop total_premium as redundant.
     Optionally offer a no-premium variant.

4. Split ignores time; claim development is unchecked (moderate).
   - Rows span 2022 (37.8k), 2023 (67.2k) and 2024 (95.0k). The mix shifts: 2022 is 98% new business and
     2024 is 43% portfolio. Full-year exposure share rises from 16% to 49%.
   - Weighted mean target by year: 0.894 / 0.966 / 0.997.
   - Grouping by insured_id is right: it prevents the same policyholder's other years from leaking.
   - In practice, though, one would train on past years and score the next. A temporal check (train
     2022-23, test 2024) gives R2 0.049, similar to the grouped split, so the grouped split is not
     optimistic here.
   - Incurred costs for 2024 are probably less developed (open claims, IBNR). I could not verify this from
     the source.
   - Change: keep year as a feature and consider a temporal holdout. At minimum, document the development
     cut-off.

5. Minor data quality points (low).
   - years_licensed != driver_age - age_at_licence by more than 1 year in 141 rows (range -41 to +31).
     age_at_licence < 18 in 41 rows (Spanish B licence age is 18). age_at_licence looks derived, so it is
     redundant.
   - 8 rows have incurred < 1 EUR (minimum 6.5e-14): float residue, effectively zero.
   - Missing values are small and fine to leave as NaN: fuel_type 701, vehicle_value 310, liability_premium
     11, years_licensed/age_at_licence 22 (per 200k).
   - vehicle_brand has 66 levels with a long tail. Some categories have 0 rows in the sample (unused levels
     from subsampling), which is harmless.
   - Only 7 rows are exact duplicates once insured_id is removed, so there is no meaningful duplication.
   - Data looks real: plausible premium splits, about 16% annual claim incidence, a realistic heavy tail.

**Could not check**
- The data paper (PMC / ScienceDirect) was behind a bot check, so I could not read the variable
  definitions: what "incurred" includes (reserves, coverage scope, development date), how actual_exposure is
  computed, or what anonymisation or perturbation was applied.
- How 354,140 transactions became 354,091 rows, and whether several transactions per policy-year were merged.
- Whether claims in the target are restricted to coverages the policy holds (the "coverage level" in the
  dataset name).

</details>

<details><summary>Task gamer</summary>

**Task gamer report: spanish_motor_insurance_coverage_level_2022_2024** (target log1p_incurred_per_exposure_year,
grouped by insured_id, 3x3 splits, normalized weighted Gini weighted by actual_exposure)

Verdict: the features are clean. The task can be gamed by about +0.03 to +0.04 Gini, and only by bringing in two things
a model must not have: the scoring weight (actual_exposure) as a feature, and the next-year renewal pattern rebuilt from
the group column insured_id. Neither is in features(). The gain shows up only with a rate-scale objective. With the
log1p objective, the exposure feature lowers the score.

Honest baselines (LightGBM, sample_weight = actual_exposure, all 9 splits, mean of 9):
  A. log1p target, objective=regression (300 trees, lr 0.05, 63 leaves, min_child 100): 0.3077 (0.2805..0.3308)
  B. same features, Tweedie(1.5) on expm1(target) = incurred per exposure-year, prediction mapped back with log1p
     (400 trees, lr 0.03): 0.3064 (0.2667..0.3308)
  A and B are the same within noise: per-split difference -0.022..+0.019, mean -0.001.
  Noise: a column of random numbers added to the model moves the per-split score by -0.010..+0.013
  (mean +0.0014 on B; -0.005..+0.014, mean +0.003 on A).

| # | Exploit | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|
| 1 | Exposure + renewal/lapse flags + insured_id together (Tweedie) | 0.3064 (B) / 0.3077 (A) | 0.3487 (Tweedie) / 0.2886 (log1p) | +0.042 [+0.026,+0.055], 9/9 vs B; -0.019 with log1p | No | the fixes for #2 and #3 |
| 2 | The weight: actual_exposure as a feature (Tweedie) | 0.3064 (B) | 0.3373 | +0.031 [+0.020,+0.047], 9/9 | No: cancellations cut it short after the outcome (partly known for new business, see below) | keep the weight out of every model input; the harness must pass it only as sample_weight and to the scorer |
| 2a | of which: exposure of portfolio rows only (= cancelled during the year) | 0.3064 | 0.3247 | +0.018 [+0.009,+0.030], 9/9 | No | as #2 |
| 2b | of which: exposure of new-business rows only | 0.3064 | 0.3180 | +0.012 [+0.003,+0.019], 9/9 | Partly (start date known, cancellation not) | as #2 |
| 2c | full-year flag (exposure == 1) | 0.3064 | 0.3166 | +0.010 [+0.002,+0.015], 9/9 | No | as #2 |
| 3 | has_next: the same insured_id appears in year+1 (renewed), from the group column | 0.3064 / 0.3077 | 0.3158 / 0.3148 | +0.009 [+0.004,+0.021] Tweedie; +0.007 [-0.000,+0.015] log1p | No: renewal happens after the year's claims | the harness never gives insured_id or counts derived from it to the model; optionally ship the group column as an opaque per-split code |
| 3a | lapse = no year+1 row and year < 2024 | 0.3064 | 0.3136 | +0.007 [+0.002,+0.014] | No | as #3 |
| 3b | has_next + exposure | 0.3064 | 0.3420 | +0.036 [+0.019,+0.047], 9/9 | No | #2 + #3 |
| 4 | insured_id itself as a feature (sequential by first appearance, so it encodes the entry date) | 0.3064 / 0.3077 | 0.3092 / 0.2940 | +0.003 [-0.003,+0.006] Tweedie (noise); -0.014 log1p | Entry date: yes; the id itself: no | none needed beyond #3 |

Flaws that hurt an honest model: none found that an honest choice beats. The only candidate is the objective. A
log1p-MSE fit and a Tweedie fit on the rate score the same (0.3077 vs 0.3064), so the target transform does not penalise
the obvious honest model.

Findings

1/2. The weight (actual_exposure). The rows are calendar-year slices of a policy. Exposure is below 1 when the policy
started during the year (new business; the start date is known when the policy is priced) or when it was cancelled
before year end (not known in advance, and often caused by the claim itself: a total loss ends the policy). Short
exposure goes with much higher incurred per exposure-year:
  - incurred per exposure-year 707 in the lowest exposure decile vs 255 for full-year rows;
  - portfolio rows (in force on Jan 1): 547 when exposure < 1, i.e. cancelled, vs 282 at full year;
  - rows with no next-year record and exposure < 1: 742 (2022) and 616 (2023), vs 244 for rows that renewed.
Under the Tweedie objective, adding exposure gives +0.031 on all 9 splits, three times the noise range. The
portfolio-only version, which is pure cancellation, gives +0.018. The new-business-only version, a mix of start date
and cancellation, gives +0.012. The source has no start or end dates, so the known start-date part cannot be separated
from the cancellation part. The deciding fact is the policy's effect date: if the kit carried it, the planned exposure
(Dec 31 minus effect date) would be a legitimate feature.
With the log1p objective, exposure costs -0.031 on 9/9 splits. Short rows have claims less often, so the mean of
log1p(rate) falls even though the per-exposure rate rises. A participant has to switch to a rate-scale objective to
cash this leak.
The prep already dropped policy_status (active/cancelled) and the per-coverage exposure columns, which is right. The
remaining risk is only the weight itself. It is not in features(), so the leak needs a deliberate cheat or a harness
that hands the weight to models as a column.
Mildest fix: keep actual_exposure out of the model inputs; pass it only as sample_weight and to the scorer. If the
benchmark wants deployable pricing, it could also ship a planned exposure (effect date to year end) as a feature,
which would let honest models use the legitimate part.

3. Renewal from the group column. insured_id is shipped in data.parquet. "Has a row in year+1" and "lapsed" follow
directly from it, and they are outcomes of the year being predicted: a claim raises the chance of cancellation or
non-renewal. Gain: +0.007 to +0.009 with either objective. That is close to the top of the noise range, but positive
on 9/9 splits (8/9 for log1p). Combined with exposure: +0.036 to +0.042.
Fix: the group column must stay out of model inputs (the task already says so). If the kit wants to stop even
deliberate use, it could replace the ids with per-split codes. Row counts per group would still leak, though, so the
practical fix is to keep it hidden in the harness.

Attacks that found nothing
- Formats: no target signal in decimals, whole-number shares or missingness. vehicle_value missing in 0.14% of rows
  (claim rate 0.094 vs 0.119). Zero theft/fire/property premiums only mark policy_type. total_premium equals the sum of
  the coverage premiums in every row (max deviation 1e-11). years_licensed and age_at_licence are whole numbers.
  Exposure is on a 1/365 grid in 100% of rows.
- Premiums vs exposure: total_premium is not pro-rated (median 335/338/342 across annual-payment exposure quintiles;
  Spearman with exposure 0.011), so no premium column tracks the weight.
- Row order: Spearman of row position vs target -0.001; row position vs insured_id 0.001.
- Copies across the split: exact feature duplicates in 0.014% of rows. Rebuilt entity (birth year, licence year, brand,
  power/weight, seats, fuel, municipality, area): 7.9% of test rows match a training row of another insured. The
  matched label correlates with the own label at only r = 0.03 (claim rate 0.126 vs 0.112). Adding vehicle_value
  gives 3.0% matched, r = 0.03. No real cross-split copies.
- Split hygiene: no insured_id on both sides; claim rate and exposure balanced train/test (0.120/0.118,
  0.707/0.708); year mix identical.
- Single-column Gini: total_premium alone scores 0.297 against a full model at about 0.307, but it is
  the insurer's own written price, known at pricing time: signal, not leakage. bonus_score alone scores -0.001.
- has_prev, n_years with log1p: -0.006 and +0.004, within noise.
- Transforms over all rows: no standardised, ranked or min-max scaled columns.
- Web: the dataset was published in 2026 (Mendeley sw4jmdb2sm, Data in Brief 112883). There is no competition, forum
  or leak thread. The paper confirms that exposure includes cancellations and that policy_status (A/C) exists in the
  source; the kit drops it. Looking rows up in the published file: not tried, not ranked.

What the prep changed (from the paper): 354,140 -> 354,091 rows (49 dropped). Dropped columns: policy_status,
vehicle_age, the claim counts, the incurred amounts and the per-coverage exposures. age_driving_licence turned into
years_licensed and age_at_licence. The target is total_incurred / total_exposure.

Could not check: the published file itself (not downloaded), so I could not compare it with the kit row by row; the
policy effect dates, which would decide how much of the exposure is known at pricing; whether the 2024 incurred
amounts carry less development (IBNR) than 2022 (claim rate rises 0.107 -> 0.116 -> 0.127, so no visible
under-reporting).

</details>

<details><summary>Precedent check</summary>

**Precedent check: spanish_motor_insurance_coverage_level_2022_2024 (full tier, exposure re-review 2026-11-06).**

**Verdict:** D10 is consistent with the other insurance tables decided on 2026-11-06. Each of Andrej's 2026-11-02 calls
it reverses has a written reason, and that reason came after his call. The panel recommends A in issue 6 and Lennart
resolved it as A. Under the precedents, option C (the two flat covers as presence flags) would be the departure, not A.
I found no departure without a reason, so no reflection prompt is required. I drafted one conditional prompt for a pair
that pricing_game_2016's open issue 6 could create (§5).

**Register.** The decision register, run read-only on the ten insurance tables, raises no flag on this dataset. Its six
flags (SPLIT-10 and SPLIT-14 amendment due, exceptions to a Must, `trivial`) involve pricing_game_2016,
spanish_homeowners and spanish_2015_2018, not D10.

**1. D10, part by part: consistent**

| Part | Verdict | Closest precedents |
|---|---|---|
| `actual_exposure` is the metric weight and the `sample_weight` | Consistent | fremtpl2 (Lennart, CC 2026-11-06, option A of #51), bemtpl97 (Lennart, 2026-11-06), australian D8 (Lennart, 2026-11-06), frempl D9, pricing_game_2016 D11. MET-15 (Must). |
| `total_exposure` dropped | Departs from frempl and pricing_game_2016, with a stated reason | Those two keep the start-known length (to 31 December) as a feature. LEAK-41 (Must) names "a length corrected on some rows and realized on others", and LEAK-41 says a part known at the start ships as its own column. What sets this case apart is in the notes (`dataset.py:164`): the release has no start date, so the 5,653 first-year cuts cannot be told from late starts. The 0.0176 the column carried was the planned time of late starts, which cannot be shipped without the cut. The revisit condition is written down. Under the remedy ladder this is "fix the definition". |
| Every premium annualised | Consistent | LEAK-41 names this case: "an earned premium (ship it annualised to the planned term, or not at all)". It is pro rata as measured (Spearman of the annual premium with the time on risk 0.034 / 0.024 / -0.053). The study's sweep lists it as the only form allowed. |
| 49 zero-exposure rows dropped | Consistent | LEAK-41: "a row with no amount at risk may go under USE-7, its claims counted in the notes". The notes count the claim (`dataset.py:159`, one claim of 180.11). |
| Log1p scale kept with the weighted Gini | Consistent | CLEAN-16 as amended ("a rate scored by a Gini keeps the scale the curator chose", notes say what the weighted fit estimates, `dataset.py:154`). MET-10: case by case, australian ships the identity scale. |
| Premium mark and last record kept with notes | Consistent | LEAK-10's second clause (Lennart's onlinenewspopularity, "go with (a)"; house_sales) and Andrej's issue-4 keep of 2026-11-02. Probe 22 agrees: `occupants_premium` and `legal_protection_premium` are the second and fourth predictors of the weight (28% and 5% of gain, weight R^2 0.35). Their gain that goes through the weight is ≤ 0 under both fits (-0.0028 / -0.0039 Tweedie; -0.0028 / -0.0018 L2), within noise. |

**Drift:** none. Lennart decided LEAK-41 the same way on all seven tables of the day. Where a table keeps a start-known
length (frempl, pricing_game_2016), the start date exists. Where it is lost (here), it does not.

**2. Does D10 reverse Andrej's calls with a fact that sets them apart? Yes, each one**

| Andrej, 2026-11-02 | D10 | Fact | Assessment |
|---|---|---|---|
| Issue 3: "Keep corrected total_exposure as the model feature" | dropped | LEAK-41's partial-correction clause, a Must adopted 2026-11-06, after the call | A rule outranks a precedent (principles, "Conflicts"). |
| Issue 2: the 5,653 first-year cuts an approved limitation | moot: the feature is gone and the cuts are only in the weight | MET-14 / MET-15 / LEAK-41 Mechanisms row ("cannot be located, a denominator: the weight, never a feature") | Consistent. |
| Issue 4: "Keep both ... do not round the premiums" | the premiums are annualised, still unrounded; the last record still kept | LEAK-41's earned-premium clause | Andrej's operative words still hold: unrounded, notes, his "no consistent score gain detected" wording, and the revisit condition (`dataset.py:167-168`). |
| Issue 5: keep, no training weight | `sample_weight` declared | The training-weight API now exists; issue 5 option (b) rested only on its absence | Consistent. |

The same pattern ran on every table that day: australian (Andrej, 2026-11-02, `exposure` a feature), fremtpl2 (Andrej,
2026-10-20), bemtpl97 (Myunghwan, 2026-10-23) and frempl (Andrej, 2026-11-03) were all reversed by LEAK-41 and MET-15.
This is a deliberate rule change, not drift.

Three precision points:
- **(a) Andrej has not been asked.** The study planned D10 as Andrej's decision (the exposure study's report), and
  Andrej is the record's curator (record line 5). Study §7.7 says "Each reversal goes to its curator as a consistency
  check". The record holds Lennart's CC (line 119) but no `Consistency check` line to Andrej. Under "who decides" a
  newer curator decision stands; the main session may still want to tell Andrej, and check the claims board for his
  claim on this record.
- **(b) The study's reversal table gives a stale reason.** The exposure study's report says "the cuts pay under weighted
  Tweedie (+0.0032, 7/9)". The re-measure refuted that (-0.0012 net, SE 0.0006, 3/9). The CC correctly rests on the
  clause, not a score.
- **(c) Andrej's own condition was met.** The study's table gives it: "if a proxy gains, LEAK-41 needs a remedy such as
  banded premiums, not a note". The re-measure found no gain through the located cancellation or the time on risk.
  - One borderline number remains: "through any cancellation" the premiums gain +0.0020 under weighted Tweedie (SE
    0.0011, 7/9). LEAK-41 says the worse fit decides, and that is this one.
  - No one measured whether C would remove this channel. C's reported effects cover only the located cancellation and
    the time on risk.

**3. Issue 6, option C against the precedents**

- **Against C:**
  - Andrej, issue 4 (2026-11-02): no rounding, because "rounding also removes legitimate information and leaves
    cancellation partly readable". C is a coarser form of the same remedy.
  - LEAK-7: the smallest fix that keeps a valid signal.
  - LEAK-10's second clause: onlinenewspopularity (Lennart, keep with a note when the part that can be traced shows no
    gain) and house_sales.
  - LEAK-41's own test, and probe 22. The flat covers' 0.0097 / 0.0117 gain over presence flags goes through neither the
    cancellation nor the time on risk.
- **For C:**
  - frempl's rounding of `Exposure` to months (Andrej, 2026-11-02): a coarsening that removed a mark of the cut (AUC
    0.91 to 0.61) at no cost.
  - Andrej's banded-premium condition in the study.
  - LEAK-41's "a value whose precision marks the cut".
- **What sets frempl apart, so A stands:**
  - frempl coarsened the realized length itself, which is now the weight. Here the column is the insurer's price, known
    at the quote (USE-6).
  - frempl's coarsening cost nothing. C costs 0.010-0.012, about a quarter of the premiums' 0.043-0.052.
  - The 11-02 fact that set this case apart ("rounding does not remove the trace here") no longer holds for C (0.81 to
    0.68, close to the 0.67 of last year's premiums). Even so, the cost and the absence of a gain still set it apart.
- **Conclusion:** choosing C now would depart from Andrej's issue-4 call and from LEAK-7 without a measured gain. It
  would be justified only by reading LEAK-41's "whatever it scores ... neither is a column that encodes it" as covering
  a mark of the cancellation that does not pay.
  - LEAK-41 then says "for each suspect column ... decides on the worse". Lennart wrote the rule and chose A the same
    day, so his reading is clear.
  - A clarifying amendment could prevent a different reading later, for example: a suspect column is judged by its
    measured gain through the weight; "whatever it scores" binds the weight and its exact encodings.

**4. Sibling tables**

- **spanish_motor_insurance_2015_2018** (per contract, no weight, MET-14's per-contract clause; open issue 7: A, B or
  C).
  - Facts that set this dataset apart, evident from the data and stated:
    - Its rows are calendar-year slices, 49% part-years.
    - The new-business first years start during the year, with no start date in the release, so the planned term is
      neither constant nor known.
    - The premiums in the release are earned, not written annual.
  - Point to keep in mind when issue 7 is settled: this table's renewal rows (in force from 1 January, a planned full
    year cut only by a cancellation) look like 2015_2018's rows, yet they are weighted by the cut. What sets them apart
    is that one target form must serve the late-start rows of the same table. That is evident but not written in the
    notes; one sentence in the exposure note would make it checkable.
  - Whichever option issue 7 takes, D10 stays consistent: C aligns the two; A or B are distinguished by "constant
    planned term".
- **pricing_game_2016_french_fleet, issue 6 (open; recommendation C, forced grouped "as the three siblings").**
  - Its text says this dataset has "one valid yearly window, below the floor". That is inaccurate: our 2024 window
    trains on 2022-2023, 52.5% of the rows (`dataset.py:232`, "2024, 47.5% of the rows"). The floor is met; only the
    count of windows (1 of 3) fails.
  - So pg16's distinguishing fact "its one valid window is above the floor" does not distinguish. Only "its dates are
    daily" does.
  - If the curator picks pg16's B (one window, with SPLIT-14 amended), this dataset becomes a like case decided the
    other way (prompt below).
- **wisconsin, issues 1 and 3.**
  - Andrej turned down its forced grouped split because the leak test across the split found a year-level leak (+0.113
    pooled Gini, 2010 claims 3.3 times 2009's).
  - Here the test found none (the year's training-side mean +0.0000, year x area +0.0009). That is a measured fact that
    sets this case apart, and wisconsin has two valid windows against one here.
  - Wisconsin's possible amendment ("exactly two windows ship; fewer go to SPLIT-8") keeps this dataset forced.
  - Caveat (EV-8): the forced-split cost and the leak test across the split in `splits_comment` (0.393-0.445, 0.385,
    0.415 against 0.412, +0.0011, 0.0000) were measured under the row Gini of the earlier definition. They were not
    re-run under the weighted Gini with weighted fits. A re-run on the current definition would keep the distinction
    from wisconsin current.

**5. Conditional prompt (only if pricing_game_2016 issue 6 goes to B)**

**Ship spanish_motor_insurance_coverage_level_2022_2024 with its one valid window, as pricing_game_2016_french_fleet
would under B?**

* **Problem:**
  - pricing_game_2016's B ships one temporal window whose training side holds more than half the rows, under an amended
    SPLIT-14[^s14].
  - This dataset has the same fact: one valid window, 2024 trained on 2022-2023 with 52.5% of the rows. It ships forced
    grouped by policy (Andrej, 2026-11-02, "Forced group splits should be fine")[^s8].
  - Two like cases would then be decided differently unless a fact sets them apart.
* **Options:**

  | | Option | Pro | Con |
  |---|---|---|---|
  | a | Keep it forced grouped. Distinguishing fact: the rows have only a calendar year (no finer date), and the windows rule counts years here, so B's amendment covers releases whose dates are daily; recorded as the amendment's scope | No rebuild; the forced split scores 2024 as the valid window does (0.375-0.405 against 0.385, row Gini) | Rests on a scope line in the amendment |
  | b | Treat it like pricing_game_2016: one window, 2024 on 2022-2023 | Same rule for both; renewals are known policies (+0.001 to +0.007 on renewal rows) | One test year; summary, record and split change |
  | c | Reopen pricing_game_2016 to match this one (C there) | Matches the panel's recommendation for pg16 | — |
  | d | Word the SPLIT-14 amendment so it decides both explicitly | Rule changed on purpose, not by drift | — |

* **Recommendation:** (a) if the amendment is written for daily-dated releases, otherwise (d).

[^s14]: **SPLIT-14** (Must; amended 2026-11-02 by Andrej, reframed 2026-11-05 by Lennart): at least 3 windows, each with
  its own training side holding at least 50% of the rows.
[^s8]: **SPLIT-8** (Must; narrows SPLIT-14): a release with too few periods ships forced, grouped by the entity when the
  periods are stacked.

</details>

<details><summary>Advocate</summary>

**Advocate's opening brief: spanish_motor_insurance_coverage_level_2022_2024 (exposure re-review, full tier,
2026-11-06)**

Position: ship as defined under D10, with one one-line definition fix that I concede (point 3) and some text
corrections. No finding from phase A calls for excluding the dataset or changing the task, the split or the metric.

1. The weight is wired the way LEAK-41 and MET-15 require, and nothing a model is given leaks through it. (P4, LEAK-41
   Must; MET-15 Must)
   - Evidence, claim auditor rows 4 and 5:
     - sample_weight is actual_exposure, and so is the metric's weight input.
     - None of the 23 features is an exposure column, policy_status or a claim part.
     - Constant predictions score 0 and perfect ones score 1 on all 9 folds.
     - The shipped scorer matches an independent Liberty Mutual weighted Gini to 1e-6.
   - Probe 22 on both arms:
     - The features predict the weight at R^2 0.350.
     - No top feature gains through the weight above noise. The mediated gains are -0.0028 to -0.0147 under Tweedie and
       -0.0118 to +0.0003 under L2.
     - 1/weight alone scores 0.089 (0.075 over 9 splits). The honest fit scores 0.27-0.32.
   - The task gamer found only two exploits worth +0.03 to +0.04: putting the weight in as a feature, and rebuilding
     renewal from insured_id. Neither is in features(). Both need a deliberate cheat or a broken harness.
   - Why this wins: LEAK-41 judges by timing, and the columns it says must not be features are not features here. Every
     gain above noise needs a column outside features().

2. D10 is right on the merits and consistent with the house's decisions. (LEAK-41 Must; principles "Who decides" and
   "Conflicts")
   - Dropping total_exposure: the release has no start date, so the planned part of the length (worth 0.0176) cannot be
     shipped without the cut. LEAK-41's Must ("a length corrected on some rows and realized on others") outranks the
     0.011 score loss, because a Must outranks value (P4 over P6).
   - Annualising the premiums is the only form LEAK-41 allows for an earned premium. After annualising, Spearman with
     the time on risk is 0.034 / 0.024 / -0.053, against 0.74-0.83 before.
   - The precedent checker found no departure without a stated reason:
     - the same LEAK-41 call on all seven tables of the day;
     - each of Andrej's 2026-11-02 calls reversed by a rule adopted after it;
     - option C would be the real departure from LEAK-7 and from Andrej's issue 4, at a cost of 0.010-0.012 for no
       measured gain.
   - The domain practitioner "would make the same three changes". He calls the planned length "not a rating factor I
     would use".
   - The curator decided this (D10, resolved). Under "who decides", a newer curator decision stands; the panel argues
     and does not override.

3. CONCESSION: the annualised premiums' decimal precision marks the cut. Fix it in the definition by rounding to the
   cent. (LEAK-41 Must, "a value whose precision marks the cut"; remedy ladder, rung 2)
   - The problem is real:
     - Decimal counts alone identify the located cancellations at ROC AUC 0.965.
     - total_premium sits on the 1e-6 grid on 83.8% of located cancellations, against 2.8% of active full years.
     - It gains +0.0035 under weighted Tweedie (2.1 SE, 8/9 splits) and -0.0052 under L2.
     - The column auditor measured -0.0024 from an explicit flag.
     - LEAK-41 applies "whatever it scores", so this is a Must. The texts that say "no premium carries the time on risk"
       are false as written.
   - The mildest fix keeps the dataset: `.round(2)` after the division in _clean step 5.
     - Afterwards no decimal grid from 0.1 to 1e-4 separates the cancellations (largest |AUC-0.5| is 0.009; the claim
       auditor gets 0.565).
     - The score moves within noise: -0.0017 (SD 0.0085) under Tweedie, +0.0101 (SD 0.009) under L2.
   - This does not reopen Andrej's "do not round". He declined rounding to whole euros or 3 significant digits, aimed at
     the flat-amount mark. Cent rounding keeps every price and leaves that mark alone. It still needs the curator's yes
     on the new fact.
   - Why this outranks exclusion: the remedy ladder takes "fix the definition" before "exclude", and exclusion is only
     for a Must that cannot be fixed. This one is fixed by one line.

4. The forced grouped split still holds. Its leak test needs new text only. (P4, SPLIT-8 Must; SPLIT-24, SPLIT-14)
   - Group integrity: 0 shared insured_id in 9/9 splits.
   - Against the one valid window (train 2022-23, test 2024):
     - window 0.303 (L2) and 0.311 (Tweedie), SE 0.011-0.012;
     - the folds' 2024 rows have means of 0.309 and 0.311.
     - So the forced split is +0.006 / +0.000 above the window, inside its SE.
   - Wisconsin-form leak test: +0.006 to +0.010 pooled. It is within-year drift, not a year level (the cost per
     exposure-year is flat at 285-302). No column carries it, and dropping `year` leaves it.
   - Random policy-years score the same as the grouped folds (0.318 against 0.315). Label delay shows no sign (claims
     per exposure-year 0.302 / 0.305 / 0.312).
   - The release end cuts 2024 exactly as 31 December cut the other years, so LEAK-41's no-selection clause holds.
   - Concession on the text: every measured number in splits_comment is from the old target and the row Gini (claim
     auditor row 12; split auditor problem 2). Rewrite them with the numbers above. The conclusion does not change (EV).

5. The metric is the one this decision uses, and the task is worth benchmarking. (P6, MET-14, MET-15, MET-11 context;
   TP-4)
   - The practitioner calls the exposure-weighted Gini of the cost per year, ordered by predicted cost per year, "the
     actuary's model-lift Gini" (CAS Monograph 5, the Liberty Mutual form).
   - His premium-base Gini, a second view, orders the two fits the same way on 3/3 splits.
   - The model refines the insurer's own price:
     - premium alone 0.2975, against 0.313-0.317 for the model;
     - L2 is ahead of the premium on 9/9 splits and Tweedie on 8/9;
     - the premium-base Gini is 0.11.
   - There are 354,091 rows, test folds of about 118k rows, and the fold spread is about 0.006.
   - The blind reviewer's "weak signal" (R^2 0.046) is the R^2 view of a zero-heavy claims table. The declared metric is
     a Gini, and on it the signal is clear. The "right split against the score" tension also says a small real signal is
     no reason to retire.
   - Concession on the text: the metric reason should cite Frees et al. for the ordered Lorenz curve, and CAS / Liberty
     Mutual for the exposure-weighted form (PROV-16, Should).

6. The blind reviewer's objection to log1p is a P7 scale choice the rules already settle, and the data shows it costs
   nothing. (CLEAN-16 as amended, MET-10)
   - CLEAN-16: "a rate scored by a Gini keeps the scale the curator chose."
   - The scorer inverts log1p, and the Gini depends only on rank.
   - Measured:
     - the task gamer's log1p-MSE 0.3077 against Tweedie 0.3064, per split -0.022 to +0.019;
     - the claim auditor's 0.3169 against 0.3125-0.3128.
     - So the transform does not penalise the obvious honest model.
   - The reviewer's own preferred design (exposure as the weight, never a feature) is what ships.
   - Its other points are already handled:
     - IBNR: the split auditor finds no immature 2024 labels.
     - Year drift: covered by point 4.
     - Premiums as the tariff's output: the task is framed as refining the price (USE-6).
   - Why this outranks the objection: it is a quality-level point (P7) against a measured zero cost. P7 fixes are made
     only when cheap and safe and otherwise kept with a note, and the notes already say what the weighted fit estimates.

7. The remaining items are cheap fixes or notes, not reasons to hold the dataset. (P7 and Should-level text; independent
   failures are not conflicts)
   - business_type is read from the year's last record and carries a weak cancellation mark.
     - Its mediated gain is -0.0040 (Tweedie) and -0.0118 (L2): no gain.
     - Fix: add it and these numbers to the last-record bullet (LEAK-10's second clause, keep with a note; LEAK-41's
       per-column report).
   - bonus_score should be ordinal bad < neutral < good (CLEAN-14, Should). It is a one-line FeatureTypes change, with
     bemtpl97's `coverage` as the house precedent.
   - payment_frequency as ordinal: the curator's call. Unordered also complies.
   - The pandas deprecation warning on float_precision is a maintenance note for the future; the checksum is unaffected
     today.
   - The _clean assertion is a tautology but complies with MET-14. Optionally check it against the raw total_incurred.
   - Settled points not reopened by any new fact:
     - the renewal-price blend (practitioner gap 3);
     - the flat-cover mark at AUC 0.81 (option A over C);
     - the last-record attributes.
     - All were kept by the curator with notes. Their measured gains are -0.0006 / -0.0010, and probe 22 agrees.
   - Process note: Andrej is the record's curator and has not had a consistency check on D10 (precedent checker 2a).
     That is a notification, not a defect of the dataset.

Judgment record as I would write it: Verdict: ship after changes (one definition line, plus text). Validity: USE-5 and
USE-8 hold (approximate fit). LEAK-41 triggered on the premiums' precision; fix the definition by rounding to the cent
(curator's yes). Otherwise LEAK-41 holds (the weight is no feature; probe 22 finds no mediated gain on either arm).
SPLIT-8 and SPLIT-24 hold; the leak-test text is to be re-measured. Value: TP-4, a real refinement over the premium
(0.298 to 0.317). MET-14 and MET-15 hold. Quality: CLEAN-14 bonus_score ordinal (cheap fix); CLEAN-16 log1p kept. For
the curator: confirm cent rounding (it touches the wording of issue 4); add the business_type note; tell Andrej about
D10.

</details>

<details><summary>Critic</summary>

**Critic's opening brief: spanish_motor_insurance_coverage_level_2022_2024 (exposure re-review, 2026-11-06, full tier)**

Position: ship only after changes. The task is real and D10's main parts hold: the weight wiring, dropping
`total_exposure`, annualising the premiums and the weighted Gini. I do not argue for exclusion. But D10 itself created
one Must violation under LEAK-41: annualising made the premiums' decimal precision mark the cut. The definition says the
opposite, and it is not fixed. The other points are reporting duties of a Must, stale evidence, and smaller quality
fixes.

Judgment record (proposed): Verdict: ship after changes. Validity: LEAK-41 triggered, fixable (round the annualised
premiums to the cent); LEAK-41's reporting clause incomplete (business_type); SPLIT-8 holds, but its measured cost and
leak test are stale. Value: MET-11 holds; the citation needs fixing. Quality: CLEAN-14 (bonus_score ordinal).

1. P4, LEAK-41 (Must): the annualised premiums' decimal precision gives the cancellation away.
   - Problem: the release's annual tariffs sit on a 5-decimal grid. An earned premium (annual x days/365) has 12-15
     decimals. Dividing a part-year row by its time on risk puts it back on the grid. A full year keeps long decimals,
     because it blends two tariffs or has exposure 1. So the number of decimals tells a short year from a full one. This
     is new with D10's annualisation for the late starts (0.5% short decimals before the division, 44% after). The
     located cancellations already had it.
   - Evidence:
     - claim auditor row 1: precision features alone rank the 32,626 located cancellations among rows in force from 1
       January at ROC AUC 0.965. The shipped features' known mark is 0.81. total_premium has <=5 decimals on 39.5% of
       located cancellations against 1.0% of active full years.
     - column auditor problem 1: on the 1e-6 grid, 83.8% of located cancellations against 2.8% of active in-force years
       (AUC 0.905). Every cover premium shows it, in all three years.
     - Gain on the declared metric: +0.0035 under weighted Tweedie (SE 0.0017, ahead 8/9; precision_gain.out), the worse
       fit, about 11% of the free-exposure reference (+0.0331). Under L2 it is -0.0052. The column auditor's single-flag
       version is within noise (-0.0024).
     - Probe 22 cannot see this: it fits on values, and trees do not read decimals (claim auditor row 2). The task
       gamer's "no signal in decimals" tested the target, not the cut.
   - Rule: LEAK-41 names this case verbatim: "neither is a column that encodes it: ... a value whose precision marks the
     cut", and the column is out "whatever it scores". It is a Must, so no note can keep it. Also false as written: the
     step-5 comment, the "Premiums annualised" bullet, the Decision "Every earned premium is annualised" ("no premium
     carries it"), and the CC's "no remaining column whose cancellation signal pays".
   - Remedy (fix the definition, the mildest that works): in `_clean` step 5,
     `df[premiums] = df[premiums].div(df["actual_exposure"], axis=0).round(2)`.
     - Measured: precision AUC falls to 0.565 (remedy.out). No grid from 0.1 to 1e-4 separates the cancellations
       (max |AUC-0.5| 0.009).
     - Score change within noise: -0.0017 Tweedie, +0.0101 L2 (column auditor).
     - Rounding to 4 or 5 decimals is not enough (0.607; legal_protection 0.533).
     - This is not the rounding Andrej declined on 2026-11-02 (3 significant digits or whole euros, aimed at the
       flat-amount mark). Cents keep every price. Since it touches his "do not round" wording, the curator confirms it
       on this new fact.
     - Then correct the four texts and quote the before/after AUC and gain in the note.

2. P4, LEAK-41 (Must, reporting clause): `business_type`, the weight's top predictor, has no note.
   - Problem: it is read from the year's last record. In a policy's second calendar year it flips from NB to portfolio
     mid-year. A cancelled year's last record more often comes before the flip:
     - NB share 3-10 pp higher within every start band (0.51 against 0.43 overall; column auditor problem 2);
     - among in-force rows, NB years are cancelled at 0.22-0.23, portfolio years at 0.16-0.17.
     So the shipped value is not its 1 January value, and it carries part of the cut.
   - Evidence: probe 22 gives it 41% of the weight fit (R^2 0.350). Its weight-mediated gain is -0.0040 (Tweedie, SD
     0.010) and -0.0118 (L2, SD 0.012), so no gain is measured. The last-record bullet lists type, brand, bonus class,
     vehicle, payment and area, not business_type. The 2026-11-01 column audit's question 4 asked for this sentence, and
     it never reached the definition.
   - Rule: LEAK-41: "for each suspect column the definition reports its gain on the declared metric with an L2 fit ...
     and with the weighted actuarial fit, and decides on the worse". Also LEAK-10 (weak, kept with a note).
   - Remedy (a note): add business_type and these numbers to the last-record bullet, with probe 22's line (R^2 0.35,
     shares, mediated gains on both arms, 1/weight 0.089). Optionally, for the curator: a start-known stand-in ("has a
     row the year before").

3. P4, LEAK-41 (Must, worse-fit clause): the premiums' gain through any cancellation is borderline and unmeasured under
   option C.
   - Problem: the CC rests on "no remaining column whose cancellation signal pays". But REVIEW.md issue 6 (lines
     184-185) records that the premiums gain +0.0020 through any cancellation under weighted Tweedie (SE 0.0011, ahead
     7/9), the fit LEAK-41 says decides. Point 1's precision channel adds +0.0035 (8/9) on top. No one measured whether
     option C, or the cent rounding of point 1, removes this +0.0020 (precedent checker section 2(c)).
   - Rule: LEAK-41 ("decides on the worse"); EV-1 (settle the fact with the decisive experiment).
   - Remedy (a measurement and a note, no change of option by default): after point 1's rounding, re-run the "through
     any cancellation" test on both fits and quote it. If it stays positive at about 2 SE, the A-versus-C call goes back
     to the curator with that number. A stays the default.

4. P4, SPLIT-8 (Must: a forced split states its measured cost and the leak test across it): every number in
   `splits_comment` is stale.
   - Problem: these numbers come from the old target (the year's cost), the row Gini and unweighted fits, and the text
     presents them as current:
     - the 2024 window 0.385 against 0.375-0.405;
     - pooled 0.393-0.445;
     - random against grouped 0.415 / 0.412;
     - the leak test +0.0011 / 0.0000 / +0.0009.
   - Evidence: re-measured today (split auditor; claim auditor row 12):
     - window 0.300-0.307 (L2) and 0.305-0.316 (Tweedie), SE 0.011-0.012, against the folds' 2024 rows 0.274-0.333 /
       0.292-0.332;
     - pooled 0.27-0.34;
     - random against grouped 0.318 / 0.315. The wisconsin-form leak test is new: a shared within-year period gain of
       +0.0101 pooled under L2 (SE 0.0020, 9/9) and +0.0045 under Tweedie (6/9), +0.029 on 2022 under L2 (7/9). It is
       small and does not reopen the split, but it has to be stated. The conclusions hold: the forced split is no more
       optimistic than the window.
   - Rule: SPLIT-8 (Must), EV (a number quoted as current must be measured on the shipped definition).
   - Remedy (text): rewrite the measured clauses with today's numbers and the new leak-test result. Label any older
     number as row Gini before 2026-11-02.

5. P6, MET-11 with PROV-16 (Should): the metric reason misattributes the weighted form.
   - Problem: it credits Frees, Meyers and Cummings 2011 with weighting by time on risk and ordering by cost per year.
     Their Gini orders by relativity and accumulates premium. The exposure-weighted, cost-per-year form comes from CAS
     ratemaking practice (Goldburd, Khare and Tevet, CAS Monograph 5) and Liberty Mutual's 2014 competition, whose
     weight was a sum insured, not a time on risk.
   - Evidence: claim auditor row 6; domain practitioner section 5 and "What an expert would change".
   - Remedy (text): cite Frees et al. for the ordered Lorenz Gini, and CAS Monograph 5 and Liberty Mutual for the
     weighted form. Say that the weight here is a time on risk, by the curator's call. Optionally add the current
     ceiling (1/time on risk 0.075) and the premium alone (0.298) next to it.

6. P7, CLEAN-14 (Should, ordinal clause): `bonus_score` is typed unordered.
   - Problem: the variable sheet gives a word for every level (favourable / neutral / poor claims history), so it is an
     ordered scale. Under the 2026-11-01 marks that makes it an ordinal category.
   - Evidence: column auditor problem 3. bemtpl97's ordinal `coverage` is the house precedent in this family.
   - Remedy (cheap, safe): `ordinal={"bonus_score": ["bad", "neutral", "good"]}`, and remove it from `CATEGORICAL`. This
     is a quality point only, not a reason to hold the task.

7. P3/EV (Should, text): the `fit_reason` and the `_clean` rebuild check overstate what they show.
   - `fit_reason` lists "policies starting during the year lack their planned time on risk" as a gap in the fit. To the
     pricing actuary it is not one: the rate is per year insured, and the planned length is no rating factor (domain
     practitioner). The approximate fit rests on the split. Remedy: move the clause to the notes.
   - The step-9 assertion (cost per year x time on risk rebuilds the cost) recomputes from the arrays it has just built,
     so only float error can fail it (claim auditor row 7). It complies with MET-14. Optional sharpening: assert against
     the raw `total_incurred` and `total_exposure`.

Not raised, on purpose:
- The log1p target under a weighted L2 fit (blind reviewer concern 1): settled by Lennart on 2026-11-06 under the
  amended CLEAN-16.
- Option C as such: settled as A, with point 3 asking only for the missing number.
- The renewal pattern from `insured_id` (task gamer, +0.009): it is the group column, never a feature, so it is a
  harness duty, not a definition fault.
- Andrej not being asked: under "who decides" the newer curator decision stands.
- The pandas `float_precision` deprecation: untested.

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate's rebuttal: spanish_motor_insurance_coverage_level_2022_2024 (exposure re-review, 2026-11-06)**

The critic and I agree on the verdict, "ship after changes", and on every remedy except one. I concede points 1, 4, 5, 6
and 7 in full and point 2 except its framing. I dispute point 3's conditional reopening of option A against option C.

1. Precision mark (LEAK-41 Must): CONCEDED. This was already my point 3.
   - Follows: round the premiums to the cent in _clean step 5, as `.div(...).round(2)`.
     - Measured after rounding: AUC 0.565 and no separating grid (|AUC-0.5| at most 0.009).
     - The score moves within noise.
   - Then correct the four texts and quote the before/after AUC and gain in the note.
   - The curator confirms it, because it touches the wording of Andrej's issue 4. It is the second rung of the remedy
     ladder (fix the definition), so the dataset stays.

2. business_type note: the remedy is CONCEDED, the "Must violation" framing is DISPUTED.
   - Follows: add business_type to the last-record bullet with probe 22's numbers:
     - R^2 0.35 and a 41% share of the weight fit;
     - mediated gain -0.0040 (Tweedie) and -0.0118 (L2);
     - 1/weight alone 0.089.
     This is cheap and in line with LEAK-41's reporting clause.
   - What I dispute: the critic's own evidence says no gain is measured on either fit. LEAK-41 judges a column by its
     timing:
     - the 1 January value is known at writing;
     - the last-record drift is LEAK-10's weak case, which its second clause keeps with a note when the part that can be
       traced shows no gain (onlinenewspopularity);
     - most of its tie to the weight is the start-known first year (USE-6).
   - So this is a missing note, not a column to remove. The definition is not out of compliance on timing, only on
     reporting.

3. "Through any cancellation" +0.0020: the re-measure is CONCEDED, reopening A against C on it is DISPUTED.
   - Conceded: re-running the test after the cent rounding is cheap and settles a fact (EV-1). The number goes into the
     note.
   - Disputed, for three reasons: a. Size. REVIEW.md issue 6 gives +0.0020 at SE 0.0011, 7/9, under two SEs and 6% of
     the free-exposure gain. One run's seed SD is 0.004-0.010 by the same text, so the gain is below a seed's noise.
        - The located channel is -0.0006 / -0.0010 and the time-on-risk channel 0.0000 / +0.0009. Only the unlocated mix
          crosses zero. b. Timing decides under LEAK-41: "a feature known at the prediction point that predicts the
          weight through risk selection stays (USE-6)."
        - The annual price is set at writing.
        - Cancelled years are dearer per year: annual payers 371-378 against 329-343, claim auditor row 3. That is
          selection the insurer prices, and it is not information from after the cut.
        - The part that is not start-known (the renewal blend in the flat covers) is the curator's settled keep: Andrej
          issue 4, and D10 option A. c. Precedent and ladder. Option C costs 0.010-0.012 of real price information,
          about a quarter of the premiums' 0.043-0.052. A noise-level number does not overturn LEAK-7 ("the smallest fix
          that keeps a valid signal") or a curator decision of the same day (Who decides: a newer curator decision
          stands).
   - Follows: quote the re-measured number. Send A against C back to the curator only if the number is clearly above
     noise: well beyond 2 SE and at least about one seed SD. Do not send it back at "about 2 SE".
   - Point 1's +0.0035 is a different channel (decimals). The cent rounding removes it, so it should not be added onto
     this +0.0020.

4. Stale splits_comment numbers and the new leak test (SPLIT-8, EV): CONCEDED, as in my point 4.
   - Follows: rewrite the measured clauses with today's numbers:
     - window 0.303 / 0.311 (SE 0.011-0.012) against the folds' 2024 rows 0.274-0.333 / 0.292-0.332;
     - pooled 0.27-0.34;
     - random against grouped 0.318 / 0.315.
   - State the within-year leak test: +0.006 to +0.010 pooled, the forced split's optimism, with no column carrying it.
   - The split itself stands. The critic agrees.

5. Metric citation (MET-11, PROV-16 Should): CONCEDED.
   - Follows: cite Frees et al. for the ordered Lorenz Gini, and CAS Monograph 5 and Liberty Mutual 2014 for the
     exposure-weighted form.
   - Say the weight here is a time on risk by the curator's call, and add the ceiling (1/time on risk 0.075) and the
     premium alone (0.298).

6. bonus_score ordinal (CLEAN-14 Should): CONCEDED.
   - Follows: `ordinal={"bonus_score": ["bad", "neutral", "good"]}`, removed from the categorical list.
   - bemtpl97's `coverage` is the precedent. It is a P7 fix, cheap and safe.

7. fit_reason clause and the rebuild assertion: CONCEDED as text.
   - Follows: move "policies starting during the year lack their planned time on risk" from the fit gaps to the notes.
     The practitioner says it is not a rating factor, and the approximate fit rests on the split (USE-8).
   - The step-9 assertion complies with MET-14. Sharpening it against the raw total_incurred and total_exposure is
     optional. It is not a defect.

Net judgment record (the critic's, with one amendment):
Verdict: ship after changes.
Validity:
- LEAK-41 triggered on the premiums' precision; fixed by cent rounding (the curator confirms).
- LEAK-41 reporting completed for business_type: a weak LEAK-10 case kept with a note.
- The "any cancellation" number re-measured after rounding and quoted; A stays unless it is clearly above noise.
- SPLIT-8 holds; text re-measured.
Value: MET-11 holds; citation fixed.
Quality: CLEAN-14 bonus_score ordinal.

Evidence: REVIEW.md issue 6, lines 175-195; the panel reports and probes; LEAK-41, LEAK-10 and LEAK-7.

</details>

<details><summary>Critic rebuttal</summary>

**Critic's rebuttal: spanish_motor_insurance_coverage_level_2022_2024 (exposure re-review, 2026-11-06)**

The advocate and I now agree on the verdict: ship after changes, no exclusion, the same one-line fix in the definition
(round the annualised premiums to the cent) and the same text rewrites. Three points remain in dispute. They are about
what the changes must include, not whether the dataset ships.

Advocate 1 (the weight is wired right, nothing leaks through it): concede in part, dispute in part.
- Conceded:
  - The wiring holds: `sample_weight` and the metric's weight are both `actual_exposure`, and no exposure column,
    `policy_status` or claim part is among the features (claim auditor rows 4-5). MET-15 holds.
  - Probe 22 finds no gain above noise through the weight on either fit.
- Disputed: "every gain above noise needs a column outside features()" is false for the definition as it stands.
  - The annualised premiums are in features(). Through their decimals they rank the located cancellations at AUC 0.965
    and gain +0.0035 under weighted Tweedie (SE 0.0017, 8/9; precision_gain.out). The advocate's own point 3 concedes
    this.
  - Probe 22 cannot see this channel, because it fits on values (claim auditor row 2). So probe 22's clean result is no
    evidence against it.
  - Rule: LEAK-41 (Must): "a value whose precision marks the cut", "whatever it scores".
- Not addressed by the advocate: REVIEW.md issue 6 records a gain for the premiums through any cancellation of +0.0020
  under weighted Tweedie (SE 0.0011, 7/9). LEAK-41 says the worse fit decides, and that fit is Tweedie.
  - My point 3 stands as a measurement duty (EV-1): re-run that test after the cent rounding and quote the result on
    both fits.
  - Option A stays the default. Only a result that stays near 2 SE goes back to the curator.

Advocate 2 (D10 is right and the curator decided it): concede on the merits, dispute that the CC stands unchanged.
- Conceded: dropping `total_exposure`, annualising, and the consistency with the precedents (precedent checker section
  1). I do not ask to reverse any part of D10.
- Disputed: the CC says D10 was "applied after the weighted re-measure ... found no remaining column whose cancellation
  signal pays", and the annualisation note says "no premium carries the time on risk". The precision channel was not
  known when Lennart decided.
  - Under principles, "Consistent judgement" case 1: a decision that would break a Must goes back to the curator as a
    question, not an override.
  - The remedy is the same as the advocate's point 3, but the CC line and the issue 6 text must be corrected and
    re-confirmed on the new fact, not left as written.

Advocate 3 (concession, cent rounding): agreed in full. One addition: the before-and-after numbers (AUC 0.965 to 0.565;
score -0.0017 / +0.0101) go into the "Premiums annualised" note. The four false sentences are replaced: the step-5
comment, the bullet, the Decision text and the CC.

Advocate 4 (the split holds, text only): concede.
- The split stands, and only the text changes (SPLIT-8, SPLIT-24).
- One precision for the rewrite: also state the per-year result where it is largest, 2022 at +0.029 under L2 (SE 0.010,
  7/9; split auditor problem 1). Not only the pooled +0.006 to +0.010. SPLIT-8 asks for the cost as measured.

Advocate 5 (the metric and value): concede. TP-4 and MET-14/15 hold. The citation fix is agreed (PROV-16, Should).

Advocate 6 (log1p): concede. Settled under the amended CLEAN-16 (Lennart, 2026-11-06), with a measured zero cost (0.3077
against 0.3064). I did not raise it.

Advocate 7 (the rest are cheap fixes or notes): concede on bonus_score, the assertion and the settled marks. Dispute the
strength of the business_type item.
- The advocate files it under P7 and Should-level text. It falls under LEAK-41, which is a Must in P4: "for each suspect
  column the definition reports its gain ... with an L2 fit ... and with the weighted actuarial fit, and decides on the
  worse".
  - business_type is the top predictor of the weight (41% of probe 22's gain).
  - It is read after the prediction point (it flips mid-year; cancelled second years are NB 3-10 pp more often; column
    auditor problem 2).
  - It has no note.
- The remedy stays a note with the numbers (-0.0040 / -0.0118 mediated, R^2 0.35, 1/weight 0.089). But under the Must
  the note is required before shipping, not optional.
- Not addressed by the advocate (my point 7): the `fit_reason` clause on the planned time on risk. It stays a
  Should-level text point. I do not press it further.

Agreed judgment record, as I would amend it:
- Verdict: ship after changes.
- Validity:
  - LEAK-41 triggered on the premiums' precision. Fix: round to the cent (the curator's yes, on the new fact; the CC and
    issue 6 corrected).
  - LEAK-41 reporting clause: the business_type note is required, and the "through any cancellation" gain is re-measured
    after the rounding on both fits.
  - SPLIT-8 holds, its text rewritten with today's numbers, the per-year 2022 gain included.
- Value: TP-4, MET-14 and MET-15 hold; the metric citation fixed (PROV-16).
- Quality: CLEAN-14 bonus_score ordinal; CLEAN-16 log1p kept.
- For the curator: confirm cent rounding; re-confirm D10's CC on the precision fact; tell Andrej.

</details>
