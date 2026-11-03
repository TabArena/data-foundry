# pricing_game_2017_french_mtpl

**Outcome:** added. The AI recommends shipping it; the forced split of one claim year is settled (2026-11-02). Year 0 of
the 2017 French actuarial pricing game, from the R package CASdatasets (the organiser's copy; the game's own files are
gone): 100,000 car policies of 91,488 clients of an unnamed French insurer, about 2010-11. The target is the policy's
claim total for the year in euros (0 for 88.9%), predicted when the premium is set; all policies of a client stay on one
side of the split, tagged as forced from temporal; the score is the normalized Gini as a stand-in for the game's market
profit. Validity: SEL-1 holds (driver sex kept with a note: a legal rating factor in the data's year, as frempl and
australian); USE-1 holds, fit approximate (USE-8: next year's renewals with their claim history are the real task);
USE-5 holds (negative totals from legal recourse set to 0, +4.8% on total cost, now explained); LEAK-10 holds for all 29
features; SPLIT-1 and SPLIT-4 hold (grouped by client); SPLIT-8: the cost of the forced split is now stated; its grouped
branch, written for periods that recur, is applied to one period, and the split is shipped on your call of 2026-11-02
(forced grouped splits ship; SPLIT-8 amended); PROV-8 and PROV-13 hold. Value: TP-2, a small real signal (Gini 0.20 to
0.37 per split for every model family; a Tweedie GLM is best at 0.319); MET-11: the metric reason now states its
measured closeness to the game's profit, and the choice of metric is open (issue 2). Quality: impossible values masked
(CLEAN-11), make and model joined (CLEAN-12), the commune typed as text (CLEAN-14), the target scale open with the
metric (issue 3). Weighed: the organiser's copy with documented columns +, a canonical pricing task +, one claim year
and a weak signal -. Left for Andrej: issues 2 to 4. The model numbers below were measured again on the 9 shipped splits
after the changes, with the commune left out of the models as text.

Changes made after the review panel (AI, 2026-11-01), rows, target values and folds unchanged: `splits_comment` gives
the reason for grouping and the forced split's measured cost; the metric reason states that the Gini is blind to any
monotone transform and gives its measured closeness to the game's profit; the clip's reason is the non-negative target
of Tweedie and Poisson losses (+4.8% on total cost); the notes say the target sums every guarantee of the cover and name
the IRSA flat amounts; licence ages implying a licence before 16 and one 7,901 kg weight made missing, `vh_model` joined
to the make, the commune typed as text; counts and citations corrected.

**Main points:** all issues resolved on 2026-11-03: the deviance is in (2), euros stay (3) and the name stays (4).
Verdict: ship.

**Issues for Andrej:**

2. **Keep the normalized Gini as the stand-in for the game's profit, or score the mean Tweedie deviance?**

   * **Problem:**
     - The game scored each player's profit in simulated markets, which needs the other players' premiums and later
       claims, so a stand-in is declared.
     - Which one: the normalized Gini, which scores only how the predictions order policies by claim cost, or the
       Tweedie deviance, which scores order and level?
   * **Background:** the stand-in is the closest computable metric, with its closeness measured on the shipped splits
     where possible[^s1]. The Gini ignores every monotone change of the predictions, so a book priced a third too low
     or with relativities twice too steep scores like the best tariff. The Tweedie deviance (power 1.5) scores both
     the order and the level of the expected cost, the actuarial loss for pure premiums.
   * **Experiments:** simulated markets under the game's Rule 2 on the shipped splits, built by the claim auditor and
     the domain practitioner, run again after the changes. Across a mixed field of models the Gini follows profit at a
     rank correlation (Kendall tau) of 0.12 to 0.59, a deviance at 0.58 to 0.79 (means per market variant). Among six
     strong, comparable learners the Gini leads, 0.91 against 0.69. A steeper copy of the best model ties the top Gini
     (0.317) and earns less than a flat premium (-6.55 against -6.40 EUR per policy offered).
   * **Effect on the task:** under the Gini a miscalibrated model can win (LightGBM with a Tweedie loss prices
     held-out clients at 0.64 to 0.75 of their claims and still beats squared-error LightGBM, 0.258 against 0.248).
     Under the deviance such a model loses; the deviance needs predictions floored at a stated value (1 EUR), a
     parameter of the metric.
   * **Cost:** the library has no Tweedie or Poisson deviance today; adding `mean_tweedie_deviance` (scikit-learn's
     name) is one metric for the family[^s2]. The objection in the policy calls of 2026-10-30 (positive predictions
     needed) was the AI's suggested reasoning; the floor answers it[^s3].
   * **Consistency:** frempl issue 4 (row or exposure-weighted Gini, for the family) does not move this dataset: every
     row is a whole policy-year, so the two forms coincide (an inference; the release does not say so). The deviance
     departs from australian's issue 4 recommendation (confirm the Gini for the context tables). What sets this one
     apart: it is a stand-in for a profit that could be simulated and measured, where the context tables have no
     original to measure against.
   * **Panel:** the advocate keeps the Gini on the strong-learner result; the critic and the domain practitioner prefer
     the deviance.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Normalized Gini (implemented) | scores the order only; its reason corrected with the measured closeness | leads among strong learners (0.91 against 0.69); in the library | follows profit at 0.12 to 0.59 in a mixed field; a miscalibrated model can win |
     | B | Mean Tweedie deviance (p = 1.5, floor 1 EUR) | scores order and level; also fixes issue 3 to euros | follows profit at 0.58 to 0.79 in a mixed field; the actuarial loss | not in the library yet; a floor parameter |

   * **Recommendation:** B for this dataset: a benchmark meets a mixed field of models, and there the deviance follows
     profit more closely (0.58 to 0.79 against 0.12 to 0.59).
     Shipping does not wait: the Gini stays until `mean_tweedie_deviance` is in the library. **Decision:** A (Gini) or
     B (Tweedie deviance)?

   **Notes for the AI:** on B, add `mean_tweedie_deviance` (power 1.5, the 1 EUR floor as a parameter) to the metric
   library (MET-12, MET-13), switch the definition's metric, and keep the target in euros (issue 3).

   [^s1]: **MET-11** (Must), origin "stand-in": the source has a metric that cannot be computed on our data, and "the
     closest computable metric" replaces it, its closeness "measured on the shipped splits where possible".
   [^s2]: **MET-12** (Must): standard metrics carry their scikit-learn style names, one spelling across the
     collection. **MET-13** (Must): a custom metric ships in the shared metric library with the dataset that needs it.
   [^s3]: Policy calls of 2026-10-30 (Andrej), call 3 on insurance targets: the AI's suggested reasoning said the
     Tweedie or Poisson deviance needs strictly positive predictions.

   **Andrej (2026-11-03, change):** Use mean_tweedie_deviance and implement it in the library

   **Answer (AI, 2026-11-03):**

   * Implemented (B). `mean_tweedie_deviance` is in the metric library under scikit-learn's name, as a standard
     metric: the power is a required param, and `min_prediction` optionally floors the predictions, as the Poisson
     deviance already allowed. It is tested against scikit-learn (by hand at power 1.5, on zero-heavy costs, and at
     power 1, where it equals the Poisson deviance).
   * The definition declares it as the stand-in, with power 1.5 and a floor of 1 EUR. The metric's reason now
     states why order and level both matter for the game's profit, and the measured closeness (0.58 to 0.79 against
     0.12 to 0.59 for the Gini).
   * The target stays in euros, which the deviance needs; issue 3 below asks you to confirm that.
   * `dataset check`: 0 errors, 0 warnings; the README is regenerated.

   **Resolved (2026-11-03, Andrej):** (B), the mean Tweedie deviance (power 1.5, floor 1 EUR) as the stand-in for the
   game's profit; added to the metric library.

3. **Train on euros or on log1p (follows issue 2)?**

   * **Problem:**
     - The target ships in euros.
     - A skewed positive target is logged by default[^t1], and frempl, both Spanish tables, allstate_1m and
       liberty_mutual_fire_peril_loss_cost ship log1p with the Gini on the amount.
     - The scale changes only what a model is trained on.
   * **Experiments:** on the 9 splits, random forest 0.298 on euros against 0.297 on log1p (euros ahead on 6 of 9),
     LightGBM 0.248 against 0.251 (log1p ahead on 3 of 9), so no fact specific to this dataset favours euros under the
     Gini. Under a deviance, euros are needed: a log1p fit transformed back prices policies at about 1% of their cost
     (deviance skill -5.1, where skill is the share of a constant prediction's deviance a model removes and below 0
     means worse than the constant).
   * **Consistency:** australian's issue 5 recommends log1p for the family, with this dataset following. If issue 2
     keeps the Gini and this stays in euros, it is a departure from the log default without a fact of its own (the
     pure-premium reason holds for the whole family); with australian also in dollars (its issue 5), an amendment of
     that rule would be due. wisconsin's dollars rest on a different fact (its metric divides by the premium).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Euros (implemented) | the target stays the amount in euros | needed under a deviance; the scale it scores | under the Gini, a departure from the log default with no fact of its own |
     | B | log1p | trained on log1p of the amount | the log default and the family's choice | under a deviance, prices policies at about 1% of their cost |

   * **Recommendation:** A with the deviance (the metric scores the level in euros[^t2]); B if the Gini stays.
     **Decision:** A (euros) or B (log1p)?

   **Notes for the AI:** on B, `target_transform="log1p"` (one line). On A with the deviance, record an exception to
   CLEAN-16: the metric scores the level in euros (MET-3). On A with the Gini, an amendment of CLEAN-16 would be due.

   [^t1]: **CLEAN-16** (Should): log a skewed positive target (prices, durations, counts) when the source has not,
     case by case.
   [^t2]: **MET-3** (Must): the declared metric is on the scale the task means, the source's; the target may ship on
     the scale a practitioner models it on.

   **Andrej (2026-11-03, discuss):** How does the recommendation change now that we score deviance?

   **Answer (AI, 2026-11-03):**

   * **Problem:**
     - With the deviance chosen in issue 2, the question is whether the target ships in euros or as log1p.
     - The recommendation does not change: it was already A (euros) under a deviance, and euros is what ships.
   * **Background:** the deviance scores the predicted claim cost in euros, its level included. A model trained on
     log1p learns the average of the logged cost; transformed back, that is far below the average cost, since about
     89% of the policies have no claim. Under the Gini the scale did not matter, because the Gini looks only at the
     order.
   * **Experiments:** a log1p fit transformed back prices policies at about 1% of their cost and scores worse than
     a constant prediction (deviance skill -5.1); a fit in euros scores above the constant on all 9 splits (skill
     about +0.05, mediator).
   * **Consistency:** the other insurance tables ship log1p with a Gini, where the scale changes nothing that is
     scored. This one differs because its metric scores the level in euros, which sets it apart from the default
     to log a skewed target[^t3].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Euros (implemented) | the target stays the claim cost in euros | what the deviance scores; a model trained on it can be scored as is | departs from the default to log a skewed target, with a stated reason |
     | B | log1p | trained on log1p, scored after the inverse | the default for skewed targets, as in the family | the back-transformed prediction prices policies at about 1% of their cost; worse than a constant |

   * **Recommendation:** A, keep euros: the metric scores the level in euros, and a log1p fit loses it.
     **Decision:** confirm euros (A), or log1p (B)?

   **Notes for the AI:** on A, record it under the outcome of the cross-dataset item zi-target-scale (2026-11-03
   answer): under the amended CLEAN-16 there, or as an exception (the fact: the metric scores the level in euros,
   MET-3), with a Cases row in cleaning_features.md.

   [^t3]: **CLEAN-16** (Should), see [^t1]; departing from a Should for one dataset is an exception recorded with the
     fact that sets the case apart (principles.md, "Exceptions and amendments").

   **Resolved (2026-11-03, Andrej):** A, euros. Recorded as an exception to CLEAN-16 in cleaning_features.md
   ("Cases"): the deviance scores the predicted cost's level in euros, where a Gini scores only the order.

4. **Keep the name `pricing_game_2017_french_mtpl`?**

   * **Problem:**
     - "MTPL" (motor third-party liability) comes from the CASdatasets title, but the target sums every guarantee of the
       cover, and only 8.6% of policies are liability alone.
     - A weighing: the source's own title and the cost of a rename against a name that misdescribes most policies.
   * **Background:** only the Mini cover (8.6% of policies) is liability alone, and Maxi (64.5% of policies, 83.4% of
     the claim cost) includes damage, theft and glass. The task summary describes it correctly as "a French car
     insurance policy".
   * **Consistency:** rand_health_insurance_experiment_doctor_visits issue 3 asks the same kind of question (a name
     that misdescribes the target, there taken from the screening's first target, here from the source's title); answer
     both the same way unless a fact differs.
   * **Panel:** the advocate keeps it; the domain practitioner would rename; the critic leaves it to you.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the name (implemented) | no rename; the notes say what the target covers | the source's own title; no rename | misdescribes most policies |
     | B | Rename to `pricing_game_2017_french_motor` | record, folder and links change | names what the target covers | the cost of a rename |

   * **Recommendation:** A, keep the name: it is the source's own title, and the notes say what the target covers.
     **Decision:** A (keep) or B (rename)?

   **Resolved (2026-11-03, Andrej):** (A), the name stays `pricing_game_2017_french_mtpl`, the source's own title; the
   notes say what the target covers.

**Review panel:** ship after changes (mediator). Claim audit: 32 claims, 27 hold (one with a caveat, now fixed); 1
refuted (the licence anomaly counts, fixed), 3 overstated or partly refuted (the 14,243 claims in the rules, "the
family's call", the metric's closeness: all fixed in the notes), 1 untested (whether the commune and department help).
Blind review: include with changes; its main concern is squared error on an uncapped claim cost. Debate: agreed on the
facts, the clip, keeping driver sex, grouping by client and the corrected metric reason; disputed: whether the forced
split ships (issue 1), Gini or deviance (issue 2), the scale (issue 3) and the name (issue 4).

<details><summary>Mediator</summary>

**Mediator (AI, 2026-11-01): pricing_game_2017_french_mtpl**

**Recommendation**

```text
Verdict: ship after changes.
Validity: SEL-1 holds (drv_sex kept with a note: legal in the data's year, as frempl and australian); USE-1 holds, fit
  approximate (USE-8, USE-10: the policy's claim history is missing); USE-5 holds (clip kept; its reason, its +4.8% and
  the whole-cover, IRSA nature of the amounts go into the notes); LEAK-10, LEAK-33 hold; SPLIT-1, SPLIT-4 hold (grouped
  by client); SPLIT-8 triggered: the cost line is missing, fixed in splits_comment; grouped is the closer regime
  (SPLIT-1 outranks SPLIT-8's typical-case wording), a Cases row due; the forced split itself is open against
  how_much_did_it_rain (issue 1); PROV-8, PROV-13 hold (CASdatasets, the organiser's copy; the toolbox is gone).
Value: TP-2, a small real signal (Gini 0.20-0.34, Tweedie deviance skill +0.05 on 9 of 9; keep); MET-2 holds; MET-11
  triggered (closeness was measurable and goes partly against the Gini): reason fixed now, the stand-in open (issue 2).
Quality: CLEAN-11 (licence ages implying a licence below 16, a 7,901 kg weight) and CLEAN-12 (vh_model as make plus
  model) fixed; CLEAN-14 followed (commune as string, department as category); CLEAN-16 open, tied to the metric
  (issue 3).
Weighed: the organiser's own copy with documented columns +; a canonical pricing task +; one claim year and a weak
  signal -.
For the curator: issue 1 (SPLIT-8, family-wide), 2 (Gini or Tweedie deviance), 3 (euros or log1p, follows 2), 4 (the
  name).
```

No fact was in dispute, so I ran no new experiment. I checked two statements the debate rests on: the library has no
Tweedie or Poisson deviance (`src/data_foundry/v2/metrics.py` has only `normalized_gini`, `normalized_weighted_gini` and
`ordered_lorenz_gini` for this purpose; scikit-learn's `mean_tweedie_deviance` would be the standard name, MET-12); and
the validator refuses `ForcedIIDFromTemporal` with a `grouping` (`src/data_foundry/v2/dataset.py`, line 1297), so the
alternative to the shipped split is random folds, not another tag.

**Agreed facts**

- Counts reproduced: 100,000 policies, 91,488 clients, 14,243 claims; 1,116 negative totals clipped (+4.8% total cost;
  Mini 12.5%, Maxi 4.3%; 1.1% of rows); 88.9% zeros. Blind rebuild from the `.rda` files matches 100% (target,
  `client_n_vehicles`, `pol_department`).
- No leak in the 29 features; `pol_bonus` is the start-of-year value (rises 24-25% to Year 1 for 1,230 policies with a
  Year-0 claim; alone AUC 0.518).
- Split: 0 shared clients on 9 folds; grouped and random folds tie (LightGBM Tweedie 0.257 against 0.254; paired
  sibling test -0.002 +- 0.003). Cost on the AIcrowd copy (Gini, LightGBM Tweedie): same year held out 0.268, next year
  held out 0.277, next year seen policies 0.289, with own claims 0.305. The stand-in underrates the game's task by
  0.01-0.04. AIcrowd's four years give two windows above SPLIT-14's floor, so it would ship forced too.
- Signal: Gini 0.20-0.34 for every family; Tweedie GLM best (0.319); `no_signal` comes from RMSE on a heavy tail.
- Metric closeness (two independent simulated Rule-2 markets): Gini follows profit at Kendall tau 0.08-0.64 in broad
  fields, a Poisson or Tweedie deviance at 0.57-0.82; among six strong learners the Gini leads (0.87 against 0.73). A
  steeper copy of the best GLM ties the top Gini (0.317) and earns less than a flat premium.
- Scale: random forest 0.302 euros against 0.294 log1p (6 of 9); LightGBM 0.244 against 0.248; log1p fits
  back-transformed price at about 1% of cost (deviance skill -5.1).
- Notes wrong or overstated: 55 first drivers (not 57), youngest 5; the rules give no claim count; "the family's call"
  is an AI suggestion; the `client_n_vehicles` probe was on log1p; `pol_department`'s probe went down (0.256 to 0.243).
- Target sums every guarantee of the cover (Mini, liability only, is 9% of policies); IRSA flat amounts (843 claims at
  1,236.00, 75 at 618.00); evaluation date not stated. Year 0 dates to about 2010-11 by vehicle launches (an inference).
- Dropping `drv_sex1`/`drv_sex2` raises LightGBM-Tweedie's Gini by 0.005 +- 0.001 (9 of 9).

**Changes to make now (no decision needed)**

1. `splits_comment` (SPLIT-8, Must, an independent failure, not a conflict): state why the folds are grouped (a
   sibling's same-year claims are unknown when premiums are set; grouped and random folds tie, 0.257 against 0.254);
   the measured cost on the AIcrowd copy (0.268 same year, 0.277 next year, 0.305 with the policy's own claims); that a
   later claim year adds the claim history and should be recovered, and that AIcrowd's years give two windows. Data
   unchanged.
2. Metric reason (MET-11, MET-1, Must): replace "ignores the price level" with "is blind to any monotone transform of
   the predictions (level and steepness)"; add the measured closeness (tau 0.08-0.64 broad fields, 0.87 among strong
   learners; deviance 0.57-0.82) with its source (simulated Rule-2 markets on the shipped splits). This holds until
   issue 2 is decided.
3. Clip (USE-5, notes): keep it; reason "Tweedie and Poisson losses need a non-negative target"; give +4.8% (Mini
   12.5%); write "as the AI suggested (record, 2026-10-30) and as frempl does". Same wording in the `_decisions` text.
4. Target bullet and `task_summary.predicted` (USE-5, USE-8): the total sums every guarantee of the cover (liability only
   for Mini); IRSA flat amounts behind the mass points and the negatives; evaluation date not stated. Add the fact that
   sets it apart from pg16's claim indicator (euros with a full tail, largest 141,828; pg16's charges scaled and capped
   at 8,565), precedent prompt D (a).
5. CLEAN-11: mask `drv_age_lic1`/`drv_age_lic2` where age minus licence years is below 16 (follows caracas). Should
   reproduce: 8 first and 2 second values masked; the anomaly bullet then reads 47 first and 6 second drivers licensed at
   16 or 17, kept (licences from abroad). Add the row to the placeholder decision table.
6. CLEAN-11: `vh_weight` 7,901 kg (one Peugeot 205) to missing; reproduce: 3,745 weights missing in all.
7. CLEAN-12, CLEAN-1: `vh_model` as make plus model (rules Sec. 4.25); reproduce: 1,076 levels instead of 1,023.
8. CLEAN-14: `pol_insee_code` as string, `pol_department` stays categorical (rule text; california_house_prices_2020).
   Both sides accept it; keeping the category would be an exception needing a fact. Reproduce: 13 category columns
   (id_client included) and one string.
9. Notes (EV-1): cite "at most 6 claims per vehicle (Sec. 4.31)" for the rules' cross-check, not 14,243; say the
   `client_n_vehicles` probe was on log1p and give the `pol_department` probe too (or drop both numbers); cite CLEAN-19
   beside CLEAN-3; mention the one missing `vh_age`; date Year 0 as about 2010-11 (estimate from vehicle launches) in
   `row` and in the sex note.
10. Record (house rule, at hand-over): mark the AIcrowd and Julia links as related tables; drop the stale screening
    `rmse` line and "as for pg15 and pg16"; `name` lists the AIcrowd file.

Rows, target values and folds stay the same; the checksum changes. Accept `task_target_value_dominant`.

**Changes that need the curator** (ranked)

1. SPLIT-8 (P4, Must): ship the forced grouped split of one year, or treat it like how_much_did_it_rain. Family-wide
   with frempl issue 5, australian issue 1, rand issue 1, spanish 2022-2024 issue 1. Recommend (a).
2. MET-11 (P6, Must): keep the Gini with its measured closeness, or declare a Tweedie deviance stand-in (needs the
   metric added, MET-13). Recommend the deviance for this dataset.
3. CLEAN-16 (P7, Should): euros or log1p; follows issue 2.
4. The name `..._french_mtpl` (P7, weighing): keep, or rename to `..._french_motor`.

**Disputed points**

1. *SPLIT-8: grouped or IID, and the how_much_did_it_rain call.* Two questions, settled differently.
   - Which regime is closer. The advocate rests on SPLIT-1 and SPLIT-4 (Must): the split mirrors what is known at the
     prediction point, and a sibling's same-year claims are not. The critic rests on SPLIT-8's wording (grouped only
     "when the periods are stacked and the entities recur"). Both are P4 Musts; SPLIT-1 comes first in the file, and
     SPLIT-8 asks for "the closest regime that keeps the rows" and names IID and stacked-grouped as its cases, not as
     the only ones. So grouped wins by position, and the measured cost of grouping is nil. Not a conflict that needs an
     exception: a Cases row under SPLIT-8 ("one period, grouped by the entity whose rows share it") records the reading.
     Settled: grouped.
   - Whether a forced split ships at all. SPLIT-8 (Lennart, Must) allows it; the curator's newest call (Andrej,
     2026-10-30) reads "if the data is temporal but a temporal split is not possible, we cannot split the data and
     reject it" and "Forced IID is to be avoided at all costs". The critic reads the first sentence as general and
     covering pg17; the advocate reads the call as about forced IID with shared storm hours. A curator precedent that
     contradicts a rule is flagged, not followed, and the meaning of the curator's own words is his to give. This goes
     to the curator, once for the family. The facts that may set pg17 apart: no outcome crosses the split, and the split
     is not optimistic (0.268 against 0.277-0.305). The fact against: 91.4% of clients have one vehicle, so in
     substance the split is close to random policies; under option (c) the curator should say whether that counts as
     forced IID.
2. *MET-11/MET-1: Gini or deviance.* Both sides agree the reason must change (done in change 2) and that this never
   excludes the dataset (P6). Which metric is closer depends on which field of models the benchmark meets: a weighing,
   so it goes to the curator. My lean: the deviance. MET-11's stand-in clause asks for the closest computable metric to
   an original that exists here (the game's profit), and both measurements put a deviance closer across a mixed field,
   which is what a benchmark meets. The floor on predictions is a numerical guard and a parameter (MET-12), not an
   invented cost (MET-7). The policy call of 2026-10-30 that set the deviance aside is the AI's suggested reasoning, not
   the curator's words.
3. *CLEAN-16: euros or log1p.* Neither side names a pg17-specific fact for euros under the Gini; the reason (USE-5, pure
   premium in euros) is the family's, and australian issue 5 recommends log1p with pg17 following. Under a deviance,
   euros are required in practice (a log1p fit back-transformed prices at 1% of cost) and become an exception with that
   fact (MET-3). So the scale follows issue 2.
4. *`drv_sex`.* Settled, no issue: SEL-1 holds; Year 0 is about 2010-11, when sex was a legal rating factor, so the
   actor could use it; frempl (`Gender`) and australian keep it with a note. A gain from dropping a column known at the
   prediction point is no reason to drop it. Keep, and date the note (change 9).
5. *Target not MTPL alone.* Notes fixed (changes 3, 4). The rename is a weighing with costs (issue 4).

**Consistency with precedent**

- Clip of negative totals: follows frempl and AIcrowd (precedent check 2).
- Amount, not a claim indicator: follows fremtpl2 (Andrej, 2026-10-20); departs from pg16, the fact now written (change
  4).
- Grouping by client: follows allstate_1m and spanish 2022-2024. The tag departs from SPLIT-8's wording; a Cases row is
  due (frempl differs: its chains recur across periods).
- Forced split: departs from how_much_did_it_rain; carried as issue 1 with the same options as the four sibling files.
- Commune as string: follows CLEAN-14 and california_house_prices_2020 (zillow kept a 3,030-level tract but dropped finer
  codes; the commune has median 2 policies).
- Metric: the Gini follows the family; my deviance lean departs from australian issue 4's recommendation (confirm the
  Gini). The fact that sets pg17 apart: it is a stand-in for a profit that was simulated and measured on the shipped
  splits, where the others are context metrics with no original to measure against.
- Scale: if the Gini stays, log1p follows australian issue 5; if euros stay under the Gini, that is a third exception for
  the pure-premium reason (wisconsin, australian, pg17) and an amendment of CLEAN-16 is due.
- Licence ages and weight masked: follow caracas_cervical_cancer (CLEAN-11).

</details>

<details><summary>Claim audit</summary>

**Claim audit (claim-auditor, 2026-11-01): pricing_game_2017_french_mtpl**

```text
Verdict: the data claims hold almost to the digit; one count bullet is wrong (P7), one provenance phrase overstates
  (P7), and the metric's reason fails MET-11's "closeness measured where possible": a simulated Rule-2 market on the
  shipped splits measures it, and the Gini is not the closest proxy across a broad field of models (P6).
Validity: target, prediction point, split and no-copy claims hold (LEAK-10, SPLIT-1/4, USE-5).
Value: MET-11 stand-in reason refuted in part (mechanism claim untested in the notes; measurable; a deviance tracks
  profit better in 3 of 4 market variants). MET-2 holds (every fold scores; constant 0, perfect 1).
Quality/notes: the anomaly counts (57 first drivers, youngest 8) are wrong: 55 and 5.
```

How I tested: recomputed every count from the raw CSVs and from the definition's frame (`dataset_io.from_definition`);
read the archived rules PDF (text extracted with pypdf in the scratchpad) for every quoted section; compared Year 0
with `pg17testyear1` and with AIcrowd's `training.csv` (JuliaComputing copy); scored dummies with the declared metric
on all 9 test folds; simulated the game's Year-1 market (Rule 2: clients sum their policies' premiums, take the
cheapest of 10 players with p = 1/2, the 2nd and 3rd with 1/4) with 10 players (LightGBM raw / log1p / Tweedie,
regularised variants, random forest, claim probability x mean severity, tariffs, constant, noised copies) and ranked
them by expected profit, by Gini, by RMSE and by Poisson deviance. Scripts and outputs are in the run's local folder.

**Claims table**

| claim | source | test | result | evidence | rule |
|---|---|---|---|---|---|
| 100,000 policies, 91,488 clients, 14,243 claims, all Year 0 | curation_comments "Year and source"; row | count raw | holds | 100,000 / 91,488 / 14,243; id_year one value | PROV-8 |
| CASdatasets "matches the rules' counts" including 14,243 claims | curation_comments "Year and source" | grep the rules | partly refuted | rules give 100,000 policies, last client A00091488 and "maximum is 6" claims per vehicle in Year 0 (Sec. 4.31: data max 6, a real cross-check); 14,243 is not in the rules | PROV-8, NOTE |
| files released 10 January 2017; toolbox gone | download_description, comments | rules p.1 | holds | "On January 10th, datasets with 100,000 insured is provided" | PROV-8 |
| prediction point: premium set before the year's claims; ages "from the beginning of the current year" | comments "Prediction point" | rules p.1, Sec. 4.7, 4.14, 4.18 | holds | "ℓ_i,1 ... unknown by players when submitting their premiums" | LEAK-10 |
| 12,654 policies with a claim, at most 6; 1,263 negative and 589 zero claims | comments "Target" | recount | holds | 12,654; max 6; 1,263; 589 | - |
| 1,116 negative totals, -1,864 to -0.02; 213 mixed, 80 net below 0; 88.9% zeros | comments; task_summary.changes, predicted | recount | holds | 1,116; -1,863.92 to -0.02; 213 / 80; 0.88898 | USE-5 |
| AIcrowd set the negative totals to 0 | comments; Decision 1 | AIcrowd year 1 vs pg17 | holds | AIcrowd year 1: min 0, 0 negatives where 637 were expected; zero share 0.8899 = pg17 clipped share (0.8890), not the no-claim share (0.8735), so set to 0, not dropped; all 6,280 positive totals match | USE-5 |
| "the family's call of 2026-10-30" | comments, clipping bullet | record, register | overstated | the record's Assessment is an AI suggestion; the CC line approves the dataset, not the clip (precedent-checker agrees) | NOTE, CC |
| clipping, not netting, is harmless to the comparison | implied by Decision 1 | Gini of 5 models on clipped vs net target | holds | Kendall tau of model order 1.0, 1.0, 0.8 on 3 folds; Gini drops 0.015-0.02 uniformly | USE-5 |
| raw amount: RF 0.302 vs 0.294 (raw ahead 6 of 9, +0.008 +- 0.004); LightGBM 0.244 vs 0.248 (log1p 5 of 9) | comments "Raw amount" | probe `scale_all_splits` | holds | 0.3018 / 0.2943, log1p wins 3/9, -0.0076 se 0.0038; 0.2441 / 0.2476, 5/9, +0.0035 se 0.0085 | MET-3 |
| claim AUC 0.611; severity R^2 -0.036 (-0.018 log); oracle 0.158 | comments "Only the claim part" | probe `hurdle_shipped` | holds | 0.6110; -0.0363 / -0.0184; 0.1583 | TP-1 |
| largest total 141,828 = 1.2% of claim cost | comments | recount | holds | 1.15% of clipped cost, 1.21% of net | - |
| `pol_bonus` at start of year; +24-25% to Year 1 for 1,230 with a claim, 373 without; AUC 0.518 | comments "pol_bonus" | Year 0 vs pg17testyear1 | holds | band 1.235-1.255: 1,230 / 373; 86,859 of 87,346 claim-free follow the 0.95 rule; AUC 0.518 | LEAK-10 |
| made missing: 66,814 absent-driver zeros; 111-year licences 24 + 768, 2 more; 3,744 weights, 2 values of 0 | comments, Decision 2 | recount | holds | 66,814; 24; 768; 2; 3,744; 2 | CLEAN-11 |
| the 5 zero-cylinder vehicles are electric (`vh_fuel` Hybrid) | comments | list them | holds | Peugeot Partner, 106, Citroen Saxo, Goupil: all sold as electric versions; fuel label "Hybrid" | CLEAN-11 |
| 57 first and 8 second drivers licensed before 18, youngest at 8 | comments "Anomaly" | recount after cleaning | refuted | 55 first (ages at licence 5 to 17; 57 adds the 2 rows already masked as licence > age) and 8 second; youngest first driver 5, second 8 (column-auditor finds the same) | NOTE |
| `client_n_vehicles`: 1 for 91.4%, max 9; Gini 0.263 with, 0.256 without | comments | recount; probe `explore_models` | holds, with a caveat | 91.35%, 9; 0.2628 / 0.2559, but measured on the log1p target, not the shipped raw one | CLEAN-3 |
| `pol_department`: 96 values, 2A/2B | comments | recount; rules Sec. 4.12 | holds | 96; rules: "first 2 digits ... (they are 96)" | CLEAN-12 |
| `pol_department` and `pol_insee_code` help (implied by keeping/adding them) | implied | probe `explore_models` | untested in the notes; the probe points the other way | log1p LightGBM: + dept 0.2432 vs 0.2559 base; - insee 0.2653 (untuned; categorical overfit) | CLEAN-14, TP |
| 17,794 communes, 6,775 singletons | comments | recount | holds | 17,794 / 6,775 | - |
| one identical pair, one client, no claim | comments | feature-identical rows | holds | 2 rows, 1 client, targets (0, 0) | SPLIT-23 |
| no client crosses the split | splits_comment | client overlap per fold | holds | 0 on all 9 folds; 30,496 test clients each | SPLIT-1 |
| calendar year not given | row | date the portfolio from vehicle launches | holds; can be narrowed | no model launched in 2011 or later (208, 508, DS4, DS5, Up, Captur absent); 2010 launches present at vh_age 1: Year 0 is about 2010-2011 | PROV-8 |
| sex barred from EU prices since 21 Dec 2012; rules offer it (Sec. 4.16) | comments "Note" | rules; CJEU C-236/09 | holds | quote matches; with Year 0 near 2010-11, sex was still a legal rating factor in the data's year | ETH |
| no exposure; every year holds the same 100,000 policies | comments "Note" | rules Sec. 4; Year 1 file | holds | "Every file contains exactly 100,000 policies ... present once in each file"; same id_policy set | - |
| metric original: profit over Years 1-4, 10-player markets, 3 cheapest, 170% bankruptcy | metric.original | rules Rules 2-4, objective (2) | holds | all four elements in the PDF; note also the 1.3 x removal threshold and that Rule 4 says Year 2 has "no normalization" (Year 1 premiums were normalised) | MET-11 |
| the profit cannot be computed on the release | metric.reason | release contents | holds | no other players' premiums; no claims for Years 1-4 | MET-2 |
| "its profit rests on ranking the risks; the normalized Gini scores that ranking" (the closeness) | metric.reason; builder: "closeness unmeasurable" | simulated Rule-2 market, 9 splits | refuted in part | see the metric section | MET-11 |
| Frees, Meyers and Cummings 2011, JASA 106:1085-1098; Allstate 2011, Liberty Mutual 2014 Gini | metric.reason | citation check | holds | JASA 106(495):1085-1098; both Kaggle contests scored a normalized Gini (Liberty Mutual weighted) | - |
| RMSE R^2 -0.09 to -0.005 on 9 splits | metric.reason | probe | holds | -0.088 to -0.005; the top 10 rows (0.01%) hold 67% of the mean prediction's squared error | MET-1 |
| metric computable on every fold | implied (MET-2) | scorer on dummies | holds | constant 0.0000, perfect 1.0000, random -0.027 to +0.032 on all 9 folds; 3,599-3,829 positives per fold | MET-2 |
| `task_target_value_dominant` (88.9% zeros, a true zero) | builder, proposed acceptance | recount | holds | 87.3% no claim, 1.6% net <= 0 | TP |

**The metric (MET-1, MET-2, MET-11)**

The original is right and the stand-in origin is right. What fails is the reason's central sentence, and the builder's
"closeness unmeasurable". MET-11 asks that the closeness be "measured on the shipped splits where possible", and here
it is possible: Rule 2 is fully specified, so a Year-1 market can be played on each test fold with the models as
players. Year 1 had premium normalisation (Rule 4 says Year 2 has "no normalization"), so the main scenario scales
every player's premiums to the same total. Kendall tau between the profit order and each metric's order:

| market variant | Gini | -RMSE | -Poisson deviance |
|---|---|---|---|
| 10 players incl. tariffs, constant, noised copies; level normalised; 9 splits | 0.28 (min 0.07) | 0.69 (calibrated 0.75) | 0.69-0.82 (3 splits) |
| same, each player at its own level; 9 splits | 0.08 | 0.75 | 0.60-0.73 |
| 10 players with regularised learners, loading 1.0 / 1.15 / 1.3; repeat 0 | 0.64 / 0.61 / 0.56 | 0.64 / 0.67 / 0.73 | 0.72 / 0.75 / 0.78 |
| 6 strong learners only | 0.87 | 0.60 | 0.73 |

So the Gini is the closest proxy among comparable, well-regularised learners. Across a broader field, where models
differ in spread and calibration, it is the weakest of the three. That is what a benchmark meets: TabArena's field
includes miscalibrated and over-dispersed models. A deviance on calibrated predictions is the most stable proxy.
The domain-practitioner's Tweedie run reaches the same order: Gini tau 0.33-0.55, Tweedie deviance 0.57-0.79. The
registry has no Poisson or Tweedie deviance today, so switching needs a new metric (MET-13). The second-best option
is RMSE, which follows profit better than the Gini but is run by a handful of rows (top 0.01% hold 67% of the
squared error).

**Refuted and untested, ranked (principles.md: validity first, Must first)**

1. MET-11 closeness (Must; P6 Value). The reason asserts that profit rests on the ranking but never measures it.
   Measured, the Gini follows profit at tau 0.08-0.64 in broad fields, against 0.60-0.82 for a deviance.
   What it changes: which models win on this dataset, since miscalibrated or steep models are not penalised.
   Mildest remedy: keep `normalized_gini`, and add the measured closeness and its limit to the reason (MET-11 asks
   for it). Stronger: declare a Tweedie (p = 1.5) or Poisson deviance stand-in as a new metric, with the Gini as a
   reported second number. This is the curator's call, together with the family's australian issue 4.
2. Anomaly counts (P7 notes). "57 first ... the youngest at 8" should read "55 first and 8 second drivers ... (the
   youngest at 5 and 8)". Remedy: edit the bullet.
3. "the family's call of 2026-10-30" (P7 provenance of a decision). The clip is an AI suggestion that the curator
   has not marked. Remedy: say "as suggested in the family's review (curation/inputs/two_regime_zero_triage_summary.md)"
   until the curator rules. The clip itself is harmless to model order (tau 1.0, 1.0, 0.8).
4. "matches the rules' counts ... 14,243 claims" (P7). The rules do not give the claim count. Remedy: cite what they
   do give, "at most 6 claims per vehicle in Year 0 (Sec. 4.31)", which matches.
5. Untested: whether `pol_department` and the 17,794-level `pol_insee_code` help. An untuned probe says each costs
   about 0.01 Gini. Remedy: none needed for validity (CLEAN-12 allows the addition); mention it under CLEAN-14's
   category-or-string question. The `client_n_vehicles` gain was measured on log1p, not the shipped target: re-run
   it on the raw amount or say so.
6. Narrowable: the calendar year. Vehicle launches date Year 0 to about 2010-2011. Remedy (optional): add it to the
   row line as an estimate, which also dates the sex note.

</details>

<details><summary>Column audit</summary>

**Column audit (column-auditor, 2026-11-01): pricing_game_2017_french_mtpl**

**Verdict:** no leak in any of the 29 features; ship after four small, cheap cleaning fixes (all P7) and one dtype
question for the curator.

```text
Validity: LEAK-10 holds for all 29 features (the rules count every age and duration "from the beginning of the current
  year", and the data shows pol_bonus is the value before the Year-0 claims); LEAK-33 holds (id_client is the group
  column only); no outcome-driven missingness (probe 3).
Quality: CLEAN-14 question (pol_insee_code: category or string); CLEAN-1/CLEAN-12 (vh_model collides across makes);
  CLEAN-11 (10 licence ages that imply a licence at 5-15; one Peugeot 205 weighing 7,901 kg).
Notes: the anomaly bullet's counts are wrong (55 first drivers after cleaning, not 57; the youngest is 5, not 8).
```

How I checked: I read the rules PDF (3rdPricingGame.pdf, Sec. 4.1-4.33, Wayback copy) and CASdatasets
`pricingame.Rd`. I loaded the cleaned frame through `dataset_io.from_definition` (100,000 x 31, the 9 shipped splits),
and the raw join through the definition's own `_load_raw`. I compared Year 0 with `pg17testyear1` column by column.
Scripts are in the run's local folder.

**Column table**

| column | meaning (source) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `id_client` | the client's id, `A` + 8 digits (Sec. 4.1) | yes | categorical; group column, never a feature; its number vs the claim flag: Spearman -0.004 | fine | LEAK-33 |
| `pol_bonus` | the bonus-malus coefficient, 0.5 to 3.5, attached to the driver (Sec. 4.5) | yes, start of year: from Year 0 to Year 1 it rises x1.24-1.25 for 1,230 policies with a Year-0 claim and 373 without (reproduced); on its own it ranks Year-0 claims at AUC 0.518 | float, 80 values, 0.5 to 2.16 | fine | LEAK-10, USE-6 |
| `pol_coverage` | Mini, Median1, Median2, Maxi "in this order"; Mini covers third-party liability only (Sec. 4.6) | yes (a contract term) | categorical; order not encoded (the source ships labels, not codes); claim rate 2.5% Mini to 13.4% Maxi | fine | CLEAN-14 |
| `pol_duration` | the policy's age in years, counted from the start of the year (Sec. 4.7) | yes | int, 1 to 41; 39 policies are older than their first driver's years since 18 (a change of driver), kept as unusual | fine | CLEAN-11 |
| `pol_sit_duration` | the age of the current policy terms (Sec. 4.8) | yes by the rules; no sign of a post-claim endorsement: 28,571 older policies have a value of 1, and within strata of duration, vehicle age and cover they claim at 13.9% against 13.2% | int, 1 to 25, never above `pol_duration` | fine | LEAK-10 |
| `pol_pay_freq` | payment frequency (Sec. 4.9) | yes | categorical, 4 levels | fine | CLEAN-14 |
| `pol_payd` | pay-as-you-drive, Yes/No (Sec. 4.10) | yes | categorical yes/no flag | fine | CLEAN-14 |
| `pol_usage` | WorkPrivate, Retired, Professional, AllTrips (Sec. 4.11) | yes | categorical; AllTrips has 91 rows | fine | CLEAN-14 |
| `pol_insee_code` | the INSEE code of the policyholder's commune (Sec. 4.12) | yes (1,214 policies have moved by Year 1) | read as text, so leading zeros survive (`06088`); length 5 asserted; categorical with 17,794 levels, 6,775 of them with one policy; 12.0% of test rows (11.8-12.3% on the 9 splits) are in a commune unseen in training | question: CLEAN-14 reads "string for ... high-cardinality values" | CLEAN-14 |
| `pol_department` | added: the code's first two characters, which Sec. 4.12 names as the department | yes | categorical, 96 levels (2A and 2B: 377 rows); no test level is unseen in training | fine; the note leaves out a probe number (problem 5) | CLEAN-12 |
| `drv_drv2` | a second driver is present (Sec. 4.13) | yes | categorical; `drv_age2` and `drv_sex2` are missing exactly when it is No (0 exceptions) | fine | CLEAN-14 |
| `drv_age1` | first driver's age in whole years from the start of the year (Sec. 4.14) | yes | int, 19 to 103 (7 above 98, unusual, kept) | fine | CLEAN-11 |
| `drv_age2` | second driver's age; "When not, this age is 0" (Sec. 4.15) | yes | float; the 66,814 zeros of an absent driver made missing | fine | CLEAN-10 |
| `drv_sex1` | first driver's sex, offered "as discriminatory variable in this pricing game" (Sec. 4.16) | yes | categorical M/F | fine, note kept (as frempl and australian_vehicle_insurance do) | USE-6 |
| `drv_sex2` | second driver's sex (Sec. 4.17) | yes | categorical; missing when there is no second driver | fine, note kept | USE-6 |
| `drv_age_lic1` | years the first driver has held the licence (Sec. 4.18) | yes | float; 111 (24 drivers aged 46-90) and two values above the driver's age made missing; 8 values imply a licence at age 5, 8, 11, 14, 14, 14, 15 or 15 | cleaning problem | CLEAN-11 |
| `drv_age_lic2` | years the second driver has held the licence; "some outliers" (Sec. 4.19) | yes | float; the 0 of an absent driver and 768 values of 111 made missing; 2 values imply a licence at age 8 and 10 | cleaning problem | CLEAN-11 |
| `vh_age` | the vehicle's age, from its year of release (Sec. 4.20) | yes | float because of 1 missing value in the source (one BMW 318 I), not in the notes; 8,604 cars (8.6%) are 2 or more years younger than the end of their model's marketing, so the sale columns seem to describe the model's catalogue entry; unusual, kept | fine | CLEAN-11 |
| `vh_cyl` | engine capacity in ml (Sec. 4.21) | yes | int; 0 for 5 vehicles, all electric models labelled Hybrid (Peugeot 106 and Partner, Citroen Saxo, Goupil): kept, as the notes say | fine | CLEAN-11 |
| `vh_din` | engine power (Sec. 4.22) | yes | int, 13 to 555 (BMW X6, M6 at the top) | fine | |
| `vh_fuel` | Diesel, Gasoline, Hybrid (Sec. 4.23) | yes | categorical; Hybrid has 80 rows, the 5 electric ones included | fine | CLEAN-14 |
| `vh_make` | the make (Sec. 4.24) | yes | categorical, 101 levels | fine | CLEAN-14 |
| `vh_model` | the model name; "consider concatenating vh_make and vh_model" (Sec. 4.25) | yes | categorical, 1,023 levels; 45 names occur under more than one make (`308` is Peugeot and Mercedes; `MINI` is Mini, Austin and Morris; `COUPE` has four makes), and 384 rows are not of the name's main make | cleaning problem | CLEAN-1, CLEAN-12 |
| `vh_sale_begin` | years since the model's marketing began (Sec. 4.26) | yes | int, 1 to 74 | fine | |
| `vh_sale_end` | years since the model's marketing ended (Sec. 4.26) | yes | int; 1 for 13,897 rows, and 4,919 of those are still 1 in Year 1, so 1 also means "still on sale"; kept as published | fine | |
| `vh_speed` | top speed in km/h (Sec. 4.27) | yes | int, 25 to 310; the 25 and 45 are utility vehicles (VD 4 ROUES, Goupil) | fine | CLEAN-11 |
| `vh_type` | Tourism or Commercial (Sec. 4.28) | yes | categorical | fine | CLEAN-14 |
| `vh_value` | replacement value in euros, "without inflation" (Sec. 4.29) | yes (no change from Year 0 to Year 1) | float; the 2 zeros made missing | fine | CLEAN-11 |
| `vh_weight` | weight in kg (Sec. 4.30) | yes | float; 3,744 zeros made missing (claim rate 10.2% against 11.1%, so the missingness does not follow the outcome); one Peugeot 205 weighs 7,901 kg, while the other 1,384 weigh 740 to 1,300 (median 850) | cleaning problem | CLEAN-11 |
| `claim_amount` | target: the sum of the policy's Year-0 claims (Sec. 4.33), with negative totals set to 0 | no (it is the outcome) | float, 88.9% zero; the claim aggregates it was built from are dropped | fine (the family's call on negative totals) | USE-5 |
| `client_n_vehicles` | added: the client's number of policies, 1 to 9 | yes (the insurer's own portfolio; Rule 2 matches clients) | int; a count over the client's own rows that reads no label, and all those rows sit on one side of the split; claim rate 11.4% for one vehicle, 7.2% for four | fine | CLEAN-19 (african_credit_scoring precedent), CLEAN-3 |

Dropped columns: `id_policy` (`id_client` and `id_vehicle` joined, asserted), `id_vehicle` (the rules: "their rank
should not represent anything valuable") and `id_year` (constant). All three drops are right (CLEAN-3, CLEAN-5). Every
object column is typed categorical (CLEAN-9). The one duplicated feature row (client A00072341, two policies, no claim)
is confirmed.

**Problems, ranked (principles.md: no P1-P5 problem found; all of these are P7, Should, ordered by effect)**

1. **`pol_insee_code`: category or string (CLEAN-14, Should; question for the curator).** The column has 17,794
   levels, 6,775 of them with a single policy, and 12.0% of test rows fall in a commune unseen in training
   (11.8-12.3% on the 9 shipped splits). CLEAN-14 types high-cardinality values as string. The precedents differ:
   - california_house_prices_2020 ships ZIP codes as strings and adds a coarser region category. That is this
     definition with `pol_insee_code` as string and `pol_department` as the category.
   - zillow_prize keeps the census tract as a category (3,030 levels, 0.2% of test rows unseen) and dropped the block
     group and the block (8,334 and 55,601 levels, 19-30% unseen) as near-identifiers.

   The builder's untuned LightGBM scores higher without the code (Gini 0.256 with it, 0.265 without, 3 folds). That is
   how one model handles categories, not a reason to drop it (CLEAN-22, EV-4), but it shows the category adds nothing
   for that model. Mildest remedy: `FeatureTypes(string=["pol_insee_code"])` with `pol_department` kept categorical.
   Alternative: keep the category as an exception to CLEAN-14, on the fact that communes are a fixed, finite INSEE list
   and the rules offer the code for joins (Sec. 4.12).
2. **`vh_model` collides across makes (CLEAN-1, CLEAN-12, Should).** 45 model names occur under more than one make,
   and 384 rows are not of the name's main make (Mercedes `308`, Austin `MINI`). The data owners say "Should you use
   them, consider concatenating vh_make and vh_model" (Sec. 4.25). Remedy: set `vh_model` to make plus model (1,076
   levels instead of 1,023). This loses nothing, since `vh_make` stays.
3. **Licence ages that imply a licence at 5 to 15 (CLEAN-11, Should).** 8 first drivers (5, 8, 11, 14, 14, 14, 15, 15)
   and 2 second drivers (8, 10) have such values. The note keeps them "since the ages are whole years", but rounding
   cannot produce an age below 18. Both ages count whole years from the start of the year, so a licence taken at 18 or
   later always gives `drv_age - drv_age_lic` of at least 18, whether the ages are floored or are year differences.
   Values of 16 and 17 (47 first and 6 second drivers) can be licences from abroad (UK 17, US 16); values of 15 and
   below have no explanation. Remedy: mask `drv_age_lic*` where the age at licence is below 16, as is already done
   where the licence age exceeds the age (10 values). Then correct the anomaly bullet: after cleaning, 55 first drivers
   are below 18, not 57 (the 57 included the 2 already made missing), and the youngest first driver is 5, not 8.
4. **`vh_weight` of 7,901 kg for a Peugeot 205 (CLEAN-11, Should).** The other 1,384 Peugeot 205s weigh 740 to 1,300
   kg (median 850). Remedy: make this one value missing alongside the zeros, and add it to the decision table.
5. **Notes (writing, EV-1).**
   - (a) The `client_n_vehicles` bullet gives its probe gain (Gini 0.263 against 0.256), but the `pol_department`
     bullet leaves out that the same probe went down when the department was added: 0.256 to 0.243 with the code kept,
     0.265 to 0.252 without it (the builder's model probe). Give both numbers or neither. Keep the column either way:
     the rules invite this reconstruction (CLEAN-12, CLEAN-22).
   - (b) `vh_age` has 1 missing value in the source (one BMW 318 I). Worth one clause in the notes.
   - (c) The `drv_sex` note: the rules hint that Year 0 is about six years before 2017 ("6 years ago, the hybrid market
     was still at its beginning", Sec. 4.23; "In those early ages of Year 0, Pay As You Drive was not that current",
     Sec. 4.10). That would put the data before the EU ban of 21 December 2012, as frempl's note does for its 2004
     data. This is an inference from the rules' wording (EV-2), so it belongs with the claim auditor, not as a fact in
     `task_summary`.

**Facts for the other auditors (no change to any column verdict)**

- The Year-1 file is aged mechanically in its ages and durations: `pol_duration`, `pol_sit_duration`, `drv_age_lic1`,
  `vh_sale_begin` and `vh_age` all rise by 1 for every policy, and vehicle and cover never change. But it is not
  purely mechanical: `pol_bonus` moves, `pol_pay_freq` changes for 1,798 policies, `pol_insee_code` for 1,214,
  `drv_sex1` for 7, and 3 `drv_age1` values jump (-4, +12, +27). This bears on the builder's draft issue 1 (the later
  years may be constructed).
- 402 policies get a higher bonus in Year 1 without a Year-0 claim of their own, and only 6 of them have a claim on
  another vehicle of the same client. So the bonus also responds to something the claims file does not hold. This does
  not touch the Year-0 feature, which the measured rise after Year-0 claims shows to be the value before them.

</details>

<details><summary>Split audit</summary>

**Split audit (split-auditor, 2026-11-01): pricing_game_2017_french_mtpl**

**Verdict: right with notes.** The split is grouped by `id_client`, 3 x 3 folds, tagged `ForcedGroupedFromTemporal`, and it is the right split for the one claim year that CASdatasets holds. By its use case the task is temporal: the game priced the same policies in Year 1. The release cannot give windows, and holding out whole clients keeps a sibling vehicle's claims of the same year out of training. The measurements show the forced split is not optimistic: on the AIcrowd copy of the same portfolio it scores a little below the game's next-year task. There are two notes. First, the branch of SPLIT-8 that the definition cites is written for another case. Second, `splits_comment` does not give the measured cost that SPLIT-8 asks for.

**Judgment record**

```text
Verdict: right with notes (no data change).
Validity: USE-10 read (a known entity by the use case; the claim history is not in the release, as fit_reason says);
  SPLIT-8 holds (forced, tagged; the cost line is missing: a note); SPLIT-1 and SPLIT-4 hold (grouping by client
  mirrors what is known when a premium is set); SPLIT-23 and SPLIT-24 hold (source id, one policy per prediction);
  SPLIT-29 and SPLIT-30: no other hidden group; SPLIT-9, -10, -14, -20 do not apply (no time column); SPLIT-28 not
  triggered.
Weighed: grouped against IID scores the same, so the use case decides (SPLIT-4).
For the curator: a wording call on SPLIT-8 (grouped without stacked periods); the record's `required_split`.
```

**What the use case implies (USE-10, SPLIT-3).** From the rules (archived 3rdPricingGame.pdf, p. 1): players received U0 and C0 for Year 0, and "An underwriting dataset (U1) with (the same) 100,000 policies (drivers willing to purchase insurance for Year 1) is provided. Players must provide prices for those 100,000 insured", and the losses were "unknown by players when submitting their premiums". So the real prediction is for known policies in the next year, with each policy's Year-0 claims as history: a temporal task on known entities (USE-10). That history carries signal. On the AIcrowd copy (AIcrowd year k = pg17 Year k-1, per the record), a policy that claimed one year claims the next at 16.3%, 15.7% and 13.8% (years 1 to 2, 2 to 3, 3 to 4). A policy that did not claim does so at 9.9%, 9.4% and 8.7%. A policy with 3 earlier claims claims in year 4 at 27.7%, one with none at 7.7%. CASdatasets has claims for Year 0 only (pg17testyear1 to 4 have no claim file; man page), so there is no window and SPLIT-8 applies. `fit="approximate"`, with the gap named in `fit_reason` and `task_summary.split`, is right, and the declared regime matches what the release allows.

**Findings, in rank order**

1. **The forced split's cost is not stated (P4, SPLIT-8, Must; holds, a note).** SPLIT-8 ships the forced regime "with the cost measured against the valid windows where the data has any". The shipped release has no valid window. The AIcrowd copy of the same portfolio does: the public copy of `training.csv` in JuliaComputing/ScoringEngineDemo.jl, 57,054 policies x 4 claim years, with noised features. I fetched it from GitHub without any identity. Setup: untuned LightGBM Tweedie; the policies cut into 3 folds; training on year k of the training policies, for k = 1, 2, 3 (9 fits per design). Normalized Gini (mean +- s.e.), with the claim AUC in brackets:
   - same year, held-out policies (the shipped design): 0.268 +- 0.009 (0.612)
   - next year, held-out policies: 0.277 +- 0.007 (0.614)
   - next year, policies seen in training: 0.289 +- 0.010 (0.617)
   - next year, seen policies plus their own earlier claims (k = 2, 3): 0.305 +- 0.012 (0.623)

   For pg17 Year 0 itself (k = 1) the first three designs give 0.249, 0.265 and 0.274. So the stand-in underrates the game's task, by about 0.01 (one year's shift) to 0.04 (the claim history); it does not overrate it.

   Remedy: one sentence in `splits_comment` with these numbers, saying that a release with later claim years would add the policy's own claims. spanish_motor_insurance_coverage_level_2022_2024 states its valid-window comparison the same way. Caveat: the organisers may have constructed the later AIcrowd years (builder issue 1). The persistence above looks like real data, but that is unverified.

2. **Grouped by client, while SPLIT-8's grouped branch is written for stacked periods (P4, SPLIT-8 and SPLIT-1, Must; a wording call for the curator).** SPLIT-8 ships grouped "when the periods are stacked and the entities recur across them". Here there is one period, and the group is a client's other vehicles, not the same entity in other periods. By the letter of the rule the closest regime is IID with `ForcedIIDFromTemporal`, as distribution_transformers_at_cauca_department and australian_vehicle_insurance_2004_2005 ship.

   The case for grouped, as the definition argues it: when the year's premiums are set, the claims of the client's other vehicles in that year are not known. The game also matched clients on the sum of their policies' premiums (Rule 2). A split that puts those vehicles in training shows labels from the same period. In addition, a definition with a `grouping` cannot declare `ForcedIIDFromTemporal` (the validator in `src/data_foundry/v2/dataset.py`), so the tag follows the regime. Measured (EV-1):
   - Size of the effect: 7,912 clients hold 16,424 rows (16.4%). Under random folds, 3,734 to 3,849 test rows per fold (11.3%) have a sibling in training; under the shipped folds, none do.
   - What a sibling's claim tells: little. A vehicle claims at 11.5% when another vehicle of its client claims and 9.4% otherwise, and the Spearman correlation of the amounts is 0.024. Siblings share driver and commune for only 52.6% of multi-vehicle clients. Under random folds, a lookup on driver and commune scores AUC 0.503 on the test rows it matches.
   - Untuned scores on both splits: LightGBM Tweedie reaches 0.257 +- 0.004 on the 9 shipped folds and 0.254 +- 0.006 on 9 random folds. A random forest (leaf 50) reaches 0.281 +- 0.019 grouped and 0.299 +- 0.015 random (3 folds each, unpaired).
   - Paired test on the same random test folds: removing the test clients' siblings from training, against removing as many other multi-vehicle training rows. The random forest's Gini changes by -0.002 +- 0.003 overall and +0.003 +- 0.008 on the test rows with a sibling (6 splits). Without the matched control, the same removal had shown +0.018 on those rows; that came from losing a third of the multi-vehicle training rows, not from the siblings.
   - Group probe: an R^2 gap of 0.014, within the fold spread (-0.001 on log1p).

   So the two regimes score the same and the use case decides (SPLIT-4): grouping mirrors what is known when a premium is set, and costs nothing. I recommend keeping it. Mildest remedy: write the reason and the tie into `splits_comment`, which today only cites SPLIT-8 (the grouping `definition` already has the reason). Also offer the curator a SPLIT-8 amendment, since a Must takes no exception: "or grouped by the entity whose rows share the period, when the use case does not know the other rows' outcomes of that period (pricing_game_2017_french_mtpl: a client's vehicles)". The nearest precedent is frempl_french_motor_personal_line (one year, grouped by policy chain, `ForcedGroupedFromTemporal`). There the chains are later records of the same policy and a lookup gain was measured (Gini 0.303 to 0.395), so that case fits the present wording and this one does not.

3. **Record fields (house rule, a note).** The record has `required_split` `Temporal (NON-IID)` and the tag `Non-IID (Temporal)`, while the definition ships grouped, forced from temporal. The screening block and the Assessment already say "grouped by client". Remedy: sync the field to Grouped once the curator settles finding 2 (the builder flagged this too).

**Checks that hold**
- Group id (SPLIT-24): `id_client` is the source's client id ("First client ID is A00000001 and last is A00091488", rules Sec. 4.1), and `id_policy` is `id_client` plus `id_vehicle` (asserted in `_clean`). It is not a cluster or a hash.
- One prediction (SPLIT-23): one policy, `prediction_unit="row"`. The game priced per policy ("Premiums are per policy", p. 2). `context="all_rows"` fits, since the insurer knows a client's vehicles when quoting; the only cross-row feature is `client_n_vehicles`. No aggregation.
- Hidden groups beyond the client (SPLIT-29, SPLIT-30):
  - Exact feature copies across the split: 0.0% (leak probe). The one identical pair belongs to one client and stays together.
  - A driver-and-commune key is unique to one client for 94.1% of rows (1.03 clients per key value).
  - The bonus-malus is not shared across a client's vehicles. From Year 0 to Year 1 it rose 25% for 5 of the 1,710 policies whose only claim was a sibling's (0.3%), against 0.4% for policies with no claim at all (pg17testyear1).
  - Client-id order carries nothing: Spearman 0.001 with `pol_duration`, -0.003 with a claim.
  - `hidden_groups.py` was not run: it skips grouped tasks, and the direct checks above cover the client.
- Temporal checks: there is no time column (`id_year` is constant and dropped), so no window, gap, late label, training history or season applies. Every feature is counted from the start of the year (rules Sec. 4.7, 4.14), and `pol_bonus` is the start-of-year value. Cannot verify: the date at which the Year-0 claims were valued (late-reported or reserved amounts). It would affect every fold alike.
- Signal under the split (SPLIT-28): the split did not cause the `no_signal` flag (R^2). Random folds score the same: R^2 -0.044 IID against -0.058 grouped on the amount, 0.016 against 0.016 on log1p. Under the shipped metric every family ranks the risks (Gini 0.20 to 0.34 on the 9 splits). SPLIT-28 does not trigger.
- Folds can be scored: each test fold holds 33,307 to 33,369 rows and 3,599 to 3,829 claims, and the largest claim is at most 3.4% of a fold's claim total. 12% of test rows have a commune that is not on the training side (17,794 communes, 6,775 with one policy). The commune is a feature that new rows keep (SPLIT-4), and `pol_department` also covers it.
- The release choice, seen from the split (builder issue 1): the AIcrowd copy would not give SPLIT-14's windows either. A test year 3 trains on 50% of the rows, a test year 4 on 75% and a test year 2 on 25%, so only two windows are valid. It too would ship forced (stacked years grouped by policy). What it adds is the policy's own claim history, about +0.03 Gini (finding 1). The split does not decide the release.

Scripts and outputs are in the run's local folder (no repository file touched).

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner: pricing_game_2017_french_mtpl**

**Actor.** A pricing actuary of a French motor insurer, or a player of the 2017 game in that role. At each annual renewal I
set every in-force policy's premium for the coming year from the rating factors on file. Then the market decides which
clients I keep, and my loss ratio decides whether I survive (the game's Rule 3: bankrupt above 170%).

**Fit: approximate, as the definition says (USE-8).** The rows, inputs and label are those of a real French motor
tariff fit: rating factors at the start of the year, the policy-year's claim cost. But I price next year's renewals
knowing each client's claims with me, and the data can only test other clients of the same year without that history.
USE-9 offers no direct use case instead. New-business pricing would need policies with no history, and every policy
here is at least one year old (`pol_duration` >= 1). A random hold-out of policies is how I validate a tariff, not a
decision I make (the weighed factor against rephrasing a use case).

**Metric: partly (MET-1).** The normalized Gini scores my ranking of the risks but not my price. It is blind to any
monotone transform, so a book priced a third too low or relativities twice too steep score like the best tariff. I
would choose the mean Tweedie deviance (power 1.5, predictions floored at 1 EUR), which follows the game's market
profit more closely on the shipped splits (section 5).

**How the decision is made today.** French insurers fit the pure premium per guarantee (liability, own damage, theft,
glass, assistance). They use policy-year tables over several years and GLMs (Poisson frequency times Gamma severity, or
a Tweedie pure premium), more and more often gradient boosting. The commune becomes a zoning. The bonus-malus
coefficient (CRM, Code des assurances art. A121-1) multiplies the reference premium by law; the rules use it "only
... as a possible feature" (Sec. 4.5). The relativities are rebalanced to a target loss ratio, then adjusted for
competitors and retention. A model is validated on held-out data by deviance, by Lorenz curves and the Gini, and by
lift charts and observed against predicted totals by segment (Denuit and Trufin; the CAS validation material; the
scikit-learn freMTPL example).

**1. Inputs at the prediction point**

* I have every shipped feature at the renewal date. The rules count every age and duration "from the beginning of the
  current year" (Sec. 4.7, 4.14, 4.18, 4.26), and `pol_bonus` is the start-of-year CRM. `client_n_vehicles` is known to
  me: it drives a multi-car discount. I see no leak (USE-3).
* I have but may not use `drv_sex1` and `drv_sex2`. Sex has been barred from insurance prices in the EU since 21 December
  2012 (CJEU Test-Achats, C-236/09). Measured on the 9 shipped splits: dropping both raises LightGBM-Tweedie's Gini by
  0.005 +- 0.001 (9 of 9) and its Tweedie deviance skill by 0.006 +- 0.002 (8 of 9). They carry no signal I would lose.
* Missing, and I would always have them:
  1. the policy's claim history with me (claims of the past years, liable or not; the CRM counts only liable claims, and
     it is capped and floored). This is the renewal input (USE-10). The record measured it on the AIcrowd release: AUC
     0.63 for a claim, 0.635 with past claims. It changes the framing more than the signal;
  2. the current premium (USE-6);
  3. the deductible of the cover, declared mileage (only 4,152 PAYD policies say anything about use), garaging and
     occupation;
  4. my zoning and the SRA vehicle group. The data has the raw commune instead (17,794 levels, 6,775 with one policy;
     the builder's probe: LightGBM's Gini 0.256 with it, 0.265 without) and make plus model (45 model names are shared
     by makes, 8,119 rows; the rules advise concatenating them, Sec. 4.25);
  5. the exposure. Every file holds the same 100,000 policies (Sec. 4), and the release gives no partial years.
  None of these changes the nature of the task.

**2. The target**

The expected claim cost of the policy-year, the pure premium, is what I price on. The realised annual total is the label I
fit it on: a number in euros, not a class (USE-5). A French pricing actuary would notice three things.

* **It is the whole policy, not liability.** Maxi covers "all claims, including Damage, Theft, Windshield Breaking,
  Assistance" (Sec. 4.6). Maxi holds 64.5% of the policies and 83.4% of the claim cost; its claim rate is 13.4%, Mini's
  (liability only) 2.5%. Small fixed amounts (56.19, 60.29, 106.14, 110.98 and 130.11 EUR, 613 claims) occur only on
  Median and Maxi covers, and 2,683.76 EUR (111 claims) only on Maxi. "MTPL" in the unique name, taken from the
  CASdatasets title, is wrong for the 91% of policies with more than liability cover. The `task_summary` ("a French car
  insurance policy") is right. I price per guarantee and this release cannot be split by guarantee. But the game asked
  for one premium per policy, so the task is faithful to its source.
* **The amounts are incurred and partly conventional.** 843 claims are exactly 1,236.00 EUR and 75 exactly 618.00 EUR.
  These match the IRSA inter-insurer flat rate for material damage under 6,500 EUR (a forfait of 1,236 EUR is reported
  around 2013-14) and its half for shared liability. Another 327 claims are 1,010.41 EUR. The negative claims are the
  other side of the same convention: my non-liable client's damage was below the forfait I recover (median -516 EUR;
  only 0.3% lie below -1,236). The evaluation date of the amounts (paid plus reserves, and late claims) is not stated.
  That is an approximate label (USE-5, USE-8), not a wrong one. The notes do not mention the convention, and a reader who
  sees the mass points needs it.
* **The clip of net negatives to 0.** I price net of recourse, so the IRSA gain lowers my pure premium. The clip raises the
  total claim cost by 4.8%: by cover, Mini 12.5%, Median2 7.1%, Median1 6.7%, Maxi 4.3%. It touches 1.1% of the rows.
  It barely moves a Gini, but it biases any score that sees the level. The note's reason ("a net recovery is no claim
  cost of the year") is not how I read it. A sounder reason is that Tweedie, Poisson and log-link models need
  non-negative targets. Keep the clip, but give that reason and the 4.8%.

**3. One row, one decision; the test data**

One row is one policy's annual premium. That is my decision: premiums are per policy (Sec. 4.3), and clients compare the
sum of their policies' premiums (Rule 2), so grouping by client is right. The test rows are other in-force clients of
the same year. I face next year's renewals of the same clients, with their Year-0 claims known, and with a shift in
price level (claims inflation, frequency trend). The split shows neither. The `fit_reason` and the `splits_comment` name
this gap (SPLIT-8, ForcedGroupedFromTemporal). Because the declared Gini is blind to the level, the missing year costs
less in the score than it would in a deployment.

**4. Would I use this model?**

The signal is normal for motor pricing: claim AUC 0.61 and Gini 0.24 to 0.32 on the shipped splits. Under the actuarial
loss the task has signal on every split: Tweedie deviance skill +0.057 for a Tweedie GLM and +0.048 for a random forest,
9 of 9 splits each. The builder's `no_signal` flag reads RMSE on a heavy-tailed amount. It does not describe the task as
I would score it (TP-2 keep is right). A plain Tweedie GLM on the rating factors, without commune, make or model, beat
the random forest and LightGBM on both the Gini (0.319 against 0.302, and 0.244 to 0.257 for LightGBM) and the
deviance on 9 of 9 splits.
That is familiar: on one year of 100,000 policies the simple tariff is hard to beat.

I would trust a model that is calibrated in total and by segment, monotone in the CRM, stable across folds, and
explainable for the tariff file. I would distrust one that leans on sex, on communes with one policy, or that quotes
negative premiums. LightGBM on squared error quotes negative premiums in the bottom decile on 9 of 9 splits (mean
prediction -0.09 to -0.65 times the decile's observed mean).

**5. Does the metric score my decision? Partly (MET-1)**

The normalized Gini scores the ranking of risks, the part of pricing that decides risk selection in a market. It is the
validation tool insurers use most, and the insurers' Kaggle competitions chose it. But it is invariant to every
monotone transform of the predictions, not only to a constant factor (the reason in `dataset.py` says only "the price
level"). It cannot see a premium that is too low for a whole book, or relativities that are too flat or too steep, and
the game's profit and bankruptcy rule both punish those. Wüthrich (2023) shows that the Gini is no strictly consistent
score: maximising it can select the wrong model, except among auto-calibrated models. Measured on the shipped splits:

* Two metrics, 5 honest models (Tweedie GLM, random forest, LightGBM on squared error, on log1p, and with a Tweedie
  loss), 9 splits. Both pick the GLM on 9 of 9 splits, and they rank the models at Kendall tau 0.4 to 1.0. On honest
  models the Gini is mostly in line.
* The two split on miscalibrated models. LightGBM-Tweedie prices the held-out clients at 0.61 to 0.74 of their claims
  on 9 of 9 splits, a book underpriced by a third: Gini 0.257, above LightGBM-MSE's 0.244, and Tweedie deviance skill
  -0.091. LightGBM on log1p, back-transformed, prices every policy at about 1% of its cost (level 0.009 to 0.011): its
  Gini of 0.248 matches LightGBM-MSE, and its deviance skill is -5.1. A flatter copy of LightGBM-Tweedie (power 0.3,
  same mean) keeps the Gini of 0.257 and moves the deviance skill from -0.091 to +0.037.
* A toy market under the game's rules: splits 0 to 2. Each model is a player, the premium is 1.10 times the
  prediction, clients compare their summed premiums and pick among the 3 cheapest with probability 1/2, 1/4, 1/4 (Rule
  2), 400 markets of 5 random players per split. Version B rescales every player to the same mean premium, so only the
  relativities differ: the case most favourable to the Gini. Profit is per policy offered; the mean claim is 123 EUR.

  | player | Gini | Tweedie deviance | test level | profit, as fitted | profit, level fixed |
  |---|---|---|---|---|---|
  | Tweedie GLM | 0.317 | 59.70 | 1.00 | +0.00 | -0.00 |
  | random forest (MSE) | 0.300 | 60.51 | 1.01 | -0.90 | -1.30 |
  | GLM^0.5 (flatter, same order) | 0.317 | 60.39 | 1.00 | -1.24 | -0.95 |
  | LightGBM (MSE) | 0.249 | 71.62 | 1.02 | -5.74 | -7.52 |
  | constant premium | 0 | 63.31 | 1.00 | -6.47 | -8.79 |
  | GLM^2 (steeper, same order) | 0.317 | 65.92 | 1.00 | -6.52 | -9.17 |
  | LightGBM (Tweedie) | 0.263 | 68.59 | 0.66 | -13.90 | -8.39 |
  | LightGBM (log1p, expm1) | 0.209 | 386.24 | 0.01 | -60.40 | -6.55 |

  The steeper copy of the best model ties for the top Gini and earns less than a flat premium in both versions. Against
  profit, the Gini ranks the players at Kendall tau 0.47, 0.47 and 0.55 (as fitted) and 0.40, 0.33 and 0.55 (level
  fixed); the deviance at 0.79, 0.79 and 0.79, and 0.79, 0.57 and 0.64. This market is a toy: one year instead of four,
  no retention rule, 8 players, a 10% loading. Its profit levels mean little; the order is the evidence. The deviance
  also has a weakness: it punishes the floored negative premiums of LightGBM-MSE hard (71.6), so the floor is part of
  the metric and must be stated.

What I would choose: the mean Tweedie deviance (power 1.5, predictions floored at a stated 1 EUR). It is a strictly
consistent score for the expected cost, so it rewards both the ranking and the level. Actuaries select pure-premium
models by it (Wüthrich and Merz 2023, Statistical Foundations of Actuarial Learning; the scikit-learn insurance example reports it with the Gini and checks the
totals). This is MET-1 and MET-8 (prefer a proper score for the same goal) and MET-11 (a stand-in should be the closest
computable metric to the original, here the market profit). The family's policy call of 2026-10-30 set the deviance
aside because it needs positive predictions. A floor stated in the metric's definition meets that objection; it is a
parameter like the power (MET-12), and a numerical guard, not a cost or a threshold of the decision (MET-7). This choice touches every insurance table that takes
the Gini as context or stand-in, so the curator would settle it once for the family. If the Gini stays, the metric
reason should say "any monotone transform", not "the price level".

**Gaps between the dataset and my decision, ranked by how much they change the task**

1. The metric ignores the level and the scale of the relativities (MET-1, MET-11). In a toy market under the game's
   rules, a steeper copy of the best model keeps the top Gini (0.317) and earns less than a flat premium. The Gini
   follows profit at Kendall tau 0.33 to 0.55, the Tweedie deviance at 0.57 to 0.79. The metric's rank is P6, so this
   is fixed in the definition and never excludes the dataset.
2. Same-year clients without history stand in for next year's renewals with their claims (USE-10, USE-8, SPLIT-8).
   This gap is already named. Its measured signal cost is small (AUC +0.005 with past claims on AIcrowd).
3. The target is the whole policy's incurred cost under the inter-insurer conventions, not liability claims at
   ultimate (USE-5). "MTPL" in the name misleads, and the notes do not name the IRSA amounts or the unknown evaluation
   date.
4. The net recourse gains are clipped (USE-5): +4.8% on the level, up to +12.5% for Mini, with a reason I would not give.
5. The inputs: sex is legally barred and empty of signal; the commune is used raw where I would use a zoning; my claim
   history, current premium, deductible and mileage are missing.
6. The population: one unnamed insurer, an in-force book only (no new business), and the selection of the 100,000
   policies is not stated.

**What an expert would change**

* Score by the Tweedie deviance (p = 1.5, floor 1 EUR), with the Gini as a second number, or keep the Gini and write
  that it is blind to any monotone transform (curator, family-wide; MET-1, MET-8, MET-11).
* Drop `drv_sex1` and `drv_sex2`. They cost nothing (measured above), and no French insurer may price on them since 2012.
  Otherwise keep them with the note as now (curator).
* Notes: say that the target sums every guarantee of the cover, so liability only for Mini; name the IRSA flat rate
  (1,236 and 618 EUR) behind the mass points and behind the negatives; say that the amounts are incurred at an unstated
  date. Give the clip's reason as the non-negative losses of Tweedie and Poisson models, with its 4.8% effect on the
  level.
* The unique name: `french_mtpl` describes 9% of the policies. A name such as `pricing_game_2017_french_motor` would
  be accurate (curator; a rename has costs).
* Leave `pol_insee_code` in place as a high-cardinality test, or add a coarser zone. I would not insist: the department
  is already there.

**Sources**

* The game's rules, 3rdPricingGame.pdf (Wayback copy): Rules 2-4, objective (2), Sec. 4.3-4.33.
* CASdatasets `pricingame.Rd`: "French Motor Third-Part Liability datasets", "unknown private insurers".
* The AIcrowd Insurance Pricing Game page (https://www.aicrowd.com/challenges/insurance-pricing-game): final ranking by
  "competitive profit"; the RMSE leaderboard carries "no explicit reward".
* M. V. Wüthrich (2023), "Model selection with Gini indices under auto-calibration", European Actuarial Journal,
  DOI 10.1007/s13385-022-00339-9 (https://arxiv.org/abs/2207.14372).
* Denuit and Trufin on Lorenz curves and the Gini as the dominant validation tools, and on autocalibration
  (https://research.dial.uclouvain.be/handle/2078.5/28248); CAS material on tests of fit, lift and stability
  (https://casact.org/sites/default/files/presentation/annual_2013_handouts_paper_2858_handout_1467_0.pdf).
* scikit-learn, "Tweedie regression on insurance claims"
  (https://scikit-learn.org/stable/auto_examples/linear_model/plot_tweedie_regression_insurance_claims.html): "any
  monotonic transformation of the predictions leaves the Gini index of the model unchanged".
* IRSA forfait of 1,236 EUR under 6,500 EUR, a policyholder's report on a thread last answered in March 2014
  (https://droit-finances.commentcamarche.com/forum/affich-6342462-assurance-convention-irsa-et-franchise); the
  amount is from one forum report, and the convention itself is described on insurer pages
  (https://www.lelynx.fr/assurance-auto/sinistre/indemnisation/convention-irsa/).
* CJEU C-236/09 (Test-Achats), 1 March 2011, effective 21 December 2012 (known law, not fetched); M. V. Wüthrich and
  M. Merz (2023), Statistical Foundations of Actuarial Learning and its Applications, Springer (not fetched).
* My scripts and outputs: in the run's local folder.

</details>

<details><summary>Blind review</summary>

**Verdict: include with changes.** The data is real, the features are honest and the client-grouped split is right. But as a plain squared-error regression on uncapped claim cost, the score is mostly noise: 4 of 100,000 policies carry 62% of the target's total sum of squares. Before including it, cap the target or score it with Tweedie deviance or Gini, drop `id_client` from the features, and fix the provenance notes.

**What the task is.** This is pure-premium (expected annual claim cost) prediction for a French private-motor portfolio. It is the "Year 0" training set of the 2017 French Institute of Actuaries pricing game (CASdatasets `pg17trainpol` + `pg17trainclaim`). An insurer's pricing actuary would make this prediction at quote or renewal time to set the premium. That is a real and canonical use. I rebuilt the table from the public `.rda` files and it matches exactly:

- Target = max(0, sum of the policy's claim records), 100% match on all 100,000 rows.
- `client_n_vehicles` = number of rows per client, 100% match.
- `pol_department` = first two characters of `pol_insee_code`, 100% match.
- `id_vehicle`, `id_policy` and `id_year` (constant) were dropped.

**Concerns, most serious first**

1. **Squared-error scoring is decided by a handful of rows.**
   - Shape of the target: 88.9% zeros. Positive amounts have median 632 and 99th percentile 6,083, but the maximum is 141,828.
   - Concentration: the top 1 row holds 23.6% of the total sum of squares, the top 4 hold 62.5%, the top 10 hold 67.3%.
   - Effect on scores: across the 9 grouped splits, the constant-mean RMSE ranges from 706 to 1,099, depending on which fold gets the four claims above 50k. LightGBM moves RMSE by only 1 to 3 units.
   - R² is essentially zero: 0.002 to 0.005 for Tweedie LightGBM without the high-cardinality columns, and negative on average for L2 LightGBM (-0.004).
   - Real ranking signal does exist: normalized Gini 0.27 to 0.32, AUC for claim > 0 of 0.61 to 0.62. Severity alone is nearly unpredictable (R² on log amount among positives: 0.001 to 0.012).
   - A squared-error leaderboard would therefore reward shrinking toward the mean and luck with the tail, not risk ranking.
   - Change: score with Tweedie/Poisson deviance or normalized Gini if the harness allows. Otherwise cap `claim_amount` at a stated large-loss threshold, which is standard actuarial practice. Capping at 10,000 (about the 99.96th percentile) only lifts R² to 0.0065 to 0.0098, so capping helps stability more than headroom. A third option is to recast the task as claim frequency (binary, 11.1% positive).

2. **The target construction is undocumented.**
   - The raw claim table has 14,243 records: 1,263 negative and 589 exactly zero. The source explains the negatives: "Yes, there are negative values, they come from claims where our driver's liability is not engaged".
   - The prepared target nets each policy's records and clips at zero. As a result, 1,552 policies that had claims end with target 0 (1,116 net negative, 436 net zero).
   - Clipping raises the portfolio total from 11.72M (net) to 12.29M (+4.8%).
   - This is defensible for a non-negative pure-premium target, but task.md should state it.

3. **`id_client` sits in the table as a 91,488-level categorical.** It is the group key and must be excluded from the features. Under the grouped split it never appears in test, so it cannot help. It can only slow down or mislead one-hot or target encoders. I found no ordering leak: Spearman correlation of the numeric id with the target is -0.004, and claim rate by id decile ranges only from 10.4% to 11.8%.

4. **There is no exposure column.** The source documents exposure for pg15 and pg16 but none for pg17. If some Year-0 policies were in force for only part of the year, cost would be confounded with exposure. Weak evidence that this is not happening: new policies (`pol_duration` = 1, 8,743 rows) have a claim rate of 11.7%, against 11.1% overall. I could not verify it.

5. **The name and the source links are partly wrong.**
   - The name says MTPL and the source says "14,243 claims of those 100,00 TPL policies". Yet cost depends strongly on cover: claim rate is 2.5% for Mini and 13.4% for Maxi (mean cost 28 vs 159). So the target is total claim cost under the chosen coverage, own damage included. That is fine because `pol_coverage` is a feature, but it should be described that way.
   - Two of the five links (the AIcrowd Insurance Pricing Game and the Julia `training_data.csv`) point to a different table. That table has `id_policy`, `year`, `pol_no_claims_discount`, hashed `vh_make_model`, `population` and `town_surface_area`, and 228,216 rows. Mark these links as related, not as the source.
   - The two tables likely come from the same portfolio: AIcrowd describes "100K real historical car insurance policies over 5 years", and pg17 has 100k policies in each of Years 0 to 4. Do not put both in one benchmark.

6. **High-cardinality categoricals.**
   - `pol_insee_code` has 17,794 levels (6,775 singletons; 14,278 with 5 rows or fewer). `vh_model` has 1,023 levels.
   - Both are legitimate rating factors and a fair test of how methods handle categoricals.
   - Naive native handling hurts: Tweedie LightGBM with both columns gets deviance 63.90, worse than the constant baseline at 63.29. Without them it gets 62.09.
   - I would keep them. The derived `pol_department` (96 levels) is a sensible coarse version.

7. **Minor value oddities** that remain after otherwise sensible cleaning:
   - What the preparer did, all reasonable: set the licence-years sentinel 111 to NaN (24 rows for driver 1, 768 for driver 2), set 2 licence values larger than the driver's age to NaN, and turned raw zeros in `vh_weight` (3,744) and `vh_value` (2) into NaN. Second-driver fields are NaN when `drv_drv2` = No (66,814 rows).
   - What is left: 25 rows where the driver was licensed before age 17 (minimum age at licence 5), 5 hybrids with `vh_cyl` = 0, and 148 rows where `vh_age` exceeds `vh_sale_begin` + 1.
   - The 768 rows with `drv_drv2` = Yes and a missing driver-2 licence age have a higher mean cost (329 vs 121). The NaN together with `drv_drv2` keeps that information.

**What checks out**

- **Leakage:** none found. All features are policy, driver and vehicle attributes known at underwriting.
  - `pol_bonus` is the start-of-year value: 75.3% of claimants sit at the 0.5 floor, against 78.5% of non-claimants. An at-fault claim in the year would have lifted it.
  - `client_n_vehicles` counts the client's vehicles in the same year.
- **Split:** grouping by client is right, since 7,912 clients have more than one vehicle (16,424 rows). A temporal split is impossible: `pg17testyear1` holds the same 91,488 clients with no claim columns.
- **Duplicates:** only 2 rows have identical features (1 pair also has the same target). Negligible.
- **Realness:** the claim amounts have conventional mass points (1,236.00 on 843 records, 1,010.41 on 327, 106.14 on 290), typical of flat-rate settlements between insurers rather than a generator. Frequency rises with bonus-malus (10.7% at 0.5, 13.8% at 0.8 to 1.0).
- **Size:** 100,000 rows with about 11,100 positives is plenty.

**What I could not check**

- Whether policies are full-year (no exposure field).
- The insurer's identity and any anonymization or perturbation applied by the organisers (CASdatasets says only that the source is a private insurer). The weak young-driver gradient (12.5% for ages 25 and under vs 10.0% for 70+) may come from portfolio selection or perturbation.
- The original game rules PDF (not retrieved).
- Whether the AIcrowd data truly overlaps with this portfolio.

My scripts and the raw downloads stayed in a local scratch folder. When I made my download folder, I noticed it already held pg16 files from an earlier download. I did not use them and re-downloaded into fresh folders.

Sources: [CASdatasets pricingame.Rd](https://github.com/dutangc/CASdatasets/blob/master/man/pricingame.Rd), [CASdatasets data](https://github.com/dutangc/CASdatasets/tree/master/data), [actinfo announcement](https://actinfo.hypotheses.org/86), [AIcrowd Insurance Pricing Game](https://www.aicrowd.com/challenges/insurance-pricing-game), [Julia demo CSV](https://github.com/JuliaComputing/ScoringEngineDemo.jl/blob/main/assets/training_data.csv).

</details>

<details><summary>Precedent check</summary>

**Precedent check (AI, precedent-checker, 2026-11-01): pricing_game_2017_french_mtpl**

```text
Verdict: most choices follow their precedents. Four need the curator (prompts A to D below); two of them (A, B) are
  questions the curator is already deciding for the insurance tables, in australian issues 1 and 5.
Validity: SPLIT-8: the forced grouped split follows the rule as written, but not your newest call
  (how_much_did_it_rain, Andrej, 2026-10-30), and no fact is written down to set it apart (prompt A). Here, unlike
  australian and frempl, a release with more claim years exists. The tag stretches SPLIT-8's wording (one period;
  clients do not recur across periods); that departure is reasoned, and a Cases row is due.
  PROV-8, PROV-13 (release): consistent (the origin is gone; CASdatasets is the organiser's own copy).
  USE-5 (negative totals set to 0): consistent with frempl and AIcrowd. "The family's call" is an AI suggestion.
Value: MET-11 stand-in: consistent with the rule text and the family (pg16's `fallback` is the outlier). The Gini
  itself waits for australian issue 4; frempl issue 4 (the weighting) does not change pg17 (whole policy-years).
  Target type: the amount, as in fremtpl2 (Andrej, 2026-10-20). It departs from pg16's claim indicator; the fact that
  sets it apart is in the data but not in the notes (prompt D).
Quality: CLEAN-16 (raw euros): departs from 4 of the 7 sibling tables. The stated reason holds for the whole family,
  not for pg17 alone (prompt B).
  CLEAN-14 (commune as a category): departs from the rule text and from california_house_prices_2020, at a finer level
  than the codes zillow_prize dropped; no reason written (prompt C).
  `client_n_vehicles`, `pol_department`: consistent (allstate_1m, california, zillow).
Drift: none shown. Amendment watch: CLEAN-16 for "the pure premium in euros" if wisconsin, australian and pg17 all ship
  raw (the third exception for one reason); SPLIT-8 against how_much_did_it_rain, now carried by 8 definitions of this
  run.
```

**How I checked.** I read the run's decision register (`register.json`, 1,620 decisions and 14 flags; none touches this
dataset, and its only entries for it are the AI's suggested call of 2026-10-30 and the curator's `Yes`, priority 3).
I also read:
- the Cases tables of `splits.md`, `metrics.md`, `cleaning_features.md` and `provenance.md`;
- the records of fremtpl2, pricing_game_2015/2016/2017, how_much_did_it_rain, zillow_prize and house_sales;
- "Policy calls of 2026-10-30" in `curation/inputs/two_regime_zero_triage_summary.md`;
- the definitions and REVIEW.md files of this run's insurance tables (australian, frempl, wisconsin, spanish ×2,
  allstate_1m, liberty, pg16);
- the precedent checks of the pg16, frempl and spanish panels, this panel's column audit, and the builder's probes.

Who decided matters (principles.md, "Precedence"):
- **Curator decisions on this family:** fremtpl2 (Andrej, 2026-10-20), how_much_did_it_rain (Andrej, 2026-10-30), the
  pg16 question and CCs (Andrej, 2026-10-30 and 2026-11-01), and the older SPLIT-8, CLEAN and MET cases (Lennart).
- **Not curator decisions:** the insurance table of 2026-10-30 holds *suggested* calls (Andrej: "I want you to suggest
  judgement calls ..."). The sibling definitions of this run are AI drafts waiting for review.

My only new measurement: the commune counts, on the raw `pg17trainpol.csv`. Median 2 policies per commune; 6.8% of
policies sit in a commune with one policy, 24.7% in one with fewer than 5.

**Decision by decision**

1. **Release: CASdatasets Year 0 (`pg17trainpol` with `pg17trainclaim`), not the AIcrowd table.** Consistent on
   provenance, with a stated reason; tied to the split question (prompt A).
   * **Precedents:** PROV-8 and PROV-13. The game's toolbox is gone (404, not archived), so the organiser's own
     package is the closest copy. pg16 used the organisers' files because they were still online, and named
     CASdatasets as a copy.
   * distribution_transformers_at_cauca_department (SPLIT-8 Cases, Lennart, 2026-10-21) shipped one labelled year and
     did not stack a second year of the same units with identical attributes, as this definition leaves out the aged
     later years.
   * **What the reason rests on:** AIcrowd's noised features, its account terms, and the builder's suspicion that the
     later years "may be constructed".
     * The noise alone would not bar AIcrowd: perturbation for disclosure control stays with a note (PROV-3,
       framingham_heart_study_fhs, Lennart, 2026-10-21).
     * The suspicion is untested, and the column audit weakens it. The Year-1 file is not purely aged: `pol_bonus`
       rises after Year-0 claims at the French rate, 1,214 communes and 1,798 payment frequencies change.
   * **The decisive experiment (EV-1)**, if prompt A leans to (b): the PROV-3 tests on AIcrowd's later claim years. A
     copy of AIcrowd's `training.csv` is reachable (JuliaComputing/ScoringEngineDemo.jl, measured in the record on
     2026-10-20).

2. **Negative policy totals set to 0 (1,116; the total is clipped, not each claim).** Consistent.
   * **The same mechanism, the same remedy:** frempl sets its 967 negative amounts to 0. Like these, they are
     not-at-fault claims whose recourse covered the payment (frempl REVIEW.md, "the negative amounts stay set to 0").
   * AIcrowd set these same 1,116 totals to 0 (measured in the record, 2026-10-20). pg16's suggested call was the same
     before its target changed.
   * **Wording:** the definition calls this "the family's call of 2026-10-30". That call is an AI suggestion, and the
     curator has not confirmed it. Write "as the AI suggested (record, 2026-10-30) and frempl does". frempl's precedent
     check flagged the same phrase.

3. **The claim amount as a regression target, not a claim indicator.** Departs from pricing_game_2016_french_fleet. The
   fact that sets pg17 apart is evident from the data but not written down (prompt D).
   * **Follows:** fremtpl2 (CC, Andrej, 2026-10-20: "aggregate claim amount per policy ... The claim count alone is the
     classic alternative target; not both"), and frempl, australian and both spanish tables.
   * **Against:** pg16 became a claim indicator on your question of 2026-10-30. The AI's reason there: the charges
     carry no signal among claimants (R^2 -0.15), have an unexplained short tail, and include IDA recoveries.
   * Two of those three facts hold here: claim sizes are not learnable (R^2 -0.036 on claimants, -0.018 on logs), and
     1,116 totals net negative from recourse.
   * The third does not, and pg16's precedent check names two more facts that set pg16 apart: its charges are scaled by
     one constant, and they stop at 8,565. pg17's amounts are euros with a full tail (largest total 141,828).

4. **Raw amount, not log1p (CLEAN-16, Should; MET-3, Must, allows either).** Departs with a stated reason, but the
   reason does not set pg17 apart (prompt B).
   * **The family now:**

     | Scale | Tables |
     |---|---|
     | log1p, scored on the amount | frempl, spanish_motor_insurance_2015_2018, spanish coverage 2022-2024, allstate_1m |
     | Raw | australian (no reason; its panel recommends log1p), liberty (a loss ratio; its precedent check found the reason contradicted), wisconsin (an exception to CLEAN-16 with its own fact: its metric divides by the premium, so a prediction's size counts), pg17 |

   * **The stated reason** ("the normalized Gini ranks by expected loss, which squared error on the amount estimates")
     holds for every plain-Gini table, frempl and spanish included.
   * **The measured edge is model-dependent** (the builder's scale probe on all 9 splits, after the Gini tie fix):
     * random forest 0.302 raw against 0.294 log1p (raw ahead on 6 of 9, SE 0.004);
     * LightGBM 0.244 against 0.248 (log1p ahead on 5 of 9, SE 0.009).
     * In other tables: allstate_1m measured "not consistently better" on the amount, and australian measured log1p
       lifting squared-error boosting by 0.028-0.034.
   * The definition cites australian as its precedent, but australian's own recommendation is to switch to log1p
     ("pricing_game_2017_french_mtpl would follow").
   * **Stale numbers in australian issue 5:** it quotes pg17's random forest as 0.301 against 0.291 (before the tie fix
     at 14:14) and lists wisconsin among the log1p tables, which wisconsin no longer is.

5. **Grouped by client (`id_client`), tagged `ForcedGroupedFromTemporal`.** The grouping is consistent. The tag departs
   from SPLIT-8's wording with a stated reason, and a Cases row is due. The forced split itself departs from
   how_much_did_it_rain with no fact written down (prompt A).
   * **The grouping follows:**
     * allstate_1m: a household's vehicles together, with the vehicle number replaced by a count, as here;
     * spanish coverage: "the grouping follows the use case, not a measured gap (SPLIT-4)".
   * The reason given is a prediction-point reason: the same-year claims of a client's other vehicles are unknown when
     the premiums are set. It costs nothing (random and grouped folds tie).
   * **The tag:** SPLIT-8 reserves the grouped regime for "periods ... stacked and the entities recur across them".
     pg17 has one period, and 91.4% of its clients have one vehicle.
     * The curator's cases for one undated period are IID with `ForcedIIDFromTemporal`: account_debt_south_africa
       (2026-10-12), mobile_churn and the churn snapshots (2026-10-21), and distribution_transformers (2026-10-21; one
       year of recurring units).
     * frempl's single year is grouped, but its chains are one policy's successive records, so its entities do recur
       across periods.
     * The library refuses `ForcedIIDFromTemporal` together with a grouping. The alternative is therefore IID random
       folds (builder issue 2), not a different tag on the same folds.
     * The departure serves P4 and breaks no Must. On a keep, add a SPLIT-8 Cases row ("one period, grouped by the
       entity whose rows share it").
   * **Against how_much_did_it_rain:**
     * On 2026-10-30 you sent it to `No`: "if the data is temporal but a temporal split is not possible, we cannot split
       the data and reject it".
     * In chat the same day: "Forced IID is to be avoided at all costs". SPLIT-8 was left unchanged.
     * The `splits_comment` cites SPLIT-8 but does not address that call. It is the same open question as australian
       issue 1, frempl issue 5 and wisconsin issue 1.
     * pg17 adds one fact the other three lack: a later release, AIcrowd, has four claim years for 57,054 of the
       policies. Those four years give at most two yearly windows above SPLIT-14's floor, so that release would itself
       be forced, unless wisconsin issue 1 (a) amends SPLIT-14 for two windows.
     * Your `Yes` of 2026-10-30 was given on a record that offered the AIcrowd temporal split first and "pg17 Year 0 as
       an IID task" second, so it does not settle the regime.

6. **`normalized_gini` as a stand-in for the game's market profit (MET-11, Must).** Consistent.
   * **It meets the rule's text:** the source has one metric (rules, objective (2)), which needs the other players'
     premiums and the claims of Years 1 to 4. The closeness cannot be measured, and MET-11 asks for it only "where
     possible" (numerai_v5_2_1m).
   * **Same metric in the run:** frempl, australian and both spanish tables (context), and allstate_1m (source).
     * pg16 labels the same kind of simulated market as `fallback`. That label is the outlier, not this one (pg16's
       precedent check, its prompt B).
   * **Not declared, rightly:** AIcrowd's RMSE leaderboard belongs to a later release, not to the data shipped (MET-4).
   * **Still open:**
     * No curator has yet confirmed a ranking metric on a regression target (australian issue 4); this dataset rides on
       that answer.
     * frempl issue 4 (a row Gini or an exposure-weighted one) does not move pg17: every row is a whole policy-year, so
       the two forms coincide. That rests on an inference ("the release does not say so").
   * **Stale lines in the record:** the screening's "`rmse` ... (MET-4, MET-11)" and the Assessment's "as for pg15 and
     pg16" (pg15 was retired as AHDS on 2026-10-30; pg16 ships `roc_auc`). Fix them at hand-over.

7. **`client_n_vehicles` added.** Consistent.
   * **Same mechanism:** allstate_1m's `household_vehicles` replaces the vehicle number within the household, as this
     feature replaces `id_vehicle`.
   * **Same rule:** CLEAN-19's fourth bullet, an input the actor reads at the prediction point from other rows of the
     release (rain_in_australia; african_credit_scoring_challenge's `earlier_loans`; Lennart, 2026-10-26).
   * **No contradiction with pg16:** pg16 left out a fleet count it measured as adding nothing, but it already ships the
     source's `n_vehicles`, and CLEAN-19 asks for no gain.
   * **Citation:** the bullet cites CLEAN-3 only; cite CLEAN-19 too, as liberty's precedent check asked for `var4_group`.

8. **`pol_department` added.** Consistent.
   * It follows CLEAN-12 (an id that encodes a group is split), california_house_prices_2020's `Zip Region` beside its
     ZIP, and zillow_prize's county beside the tract. On zillow, Lennart asked "would this not be multiple cat columns
     maybe?" (2026-10-26).
   * The column audit's probe, which went down with the department, is no reason to drop it (CLEAN-22, EV-4).

9. **`pol_insee_code` as a category of 17,794 communes.** Departs from CLEAN-14's text and from california; no reason
   is written down (prompt C).
   * **The rule:** CLEAN-14 says categorical "for a fixed, finite set" and "string for ... high-cardinality values". The
     commune is both.
   * **The precedents:**
     * california ships 1,132 ZIP codes as string, beside a region category.
     * zillow_prize (Lennart, 2026-10-26: "make it categorical") kept the 3,030-level census tract as a category. It
       dropped the block group (8,334 levels, about 18 rows each) and the block as near-identifiers.
     * pg17's commune is finer than what zillow dropped: median 2 policies per commune, and 12.0% of test rows fall in
       a commune unseen in training.
   * **What may set it apart:** zillow keeps latitude and longitude, so its finer codes added nothing. Here the commune
     is the only fine geography.
   * The record's line "`pol_insee_code` ... as a high-cardinality categorical" is the AI's suggestion, not a decision.

**Other choices checked, all consistent unless noted**

- **Placeholders made missing (CLEAN-10, CLEAN-11):** consistent.
  * A licence held longer than the driver's age follows caracas_cervical_cancer.
  * A weight of 0 follows heart_disease_va_long_beach (`chol` = 0) and australian (vehicle value 0).
  * The second driver's 0 age: `drv_drv2` keeps the meaning, so the change loses nothing and CLEAN-10 applies
    directly. No exception like house_sales' is needed (there, missing took over a code's meaning).
- **Licence ages of 5 to 15 kept: departs.** It departs from CLEAN-11 and caracas_cervical_cancer, where an event dated
  before it was possible becomes missing. The stated reason (whole-year ages) is refuted by the column audit (its
  problem 3). Follow caracas; this was the builder's choice, so no curator prompt is needed.
- **`drv_sex1` and `drv_sex2` kept with a note:** as frempl's `Gender` (SEL-1 holds).
- **Rows, identifiers and metadata:**
  * `id_vehicle` dropped, as allstate_1m's `Vehicle`.
  * One identical pair kept (LEAK-18), as pg16 and allstate_1m.
  * Source `Other`, year 2017 and GPL (>= 2), as pg16 and frempl (PROV-8, PROV-9).
  * Fit `approximate`, as the other forced-split tables (frempl, australian, wisconsin).

**Drift and amendments**

- **No drift.** Andrej's calls on this family agree with each other: fremtpl2 (amount target, and a temporal split on
  an inferred index rather than a forced one), how_much_did_it_rain, the pg16 question, and this record's `Yes` on a
  record that offered the temporal AIcrowd split. What diverges from the newest call are this run's definitions.
- **SPLIT-8 against how_much_did_it_rain.** principles.md flags a precedent that contradicts a rule; one of the two is
  wrong. Eight definitions of this run carry a forced tag: allstate_1m, australian, frempl, liberty, pg17, rand,
  spanish coverage and wisconsin. australian issue 1 (d) is the place to amend.
- **CLEAN-16, a possible third exception.** wisconsin's recorded exception rests on the pure premium in dollars (USE-5).
  pg17's reason is the same estimand, and australian's advocate argued the same. If all three ship raw, the third
  exception for one reason makes an amendment of CLEAN-16 due.

**Consistency check A (AI, 2026-11-01):** pg17 ships Year 0 with a forced grouped split (`ForcedGroupedFromTemporal`
under SPLIT-8; its use case is temporal). That differs from how_much_did_it_rain (`No`, Andrej, 2026-10-30: "if the data
is temporal but a temporal split is not possible, we cannot split the data and reject it"; "Forced IID is to be avoided
at all costs"). Unlike australian and frempl, a release with more claim years exists (AIcrowd). What sets pg17 apart?
(a) No outcome is shared across the split: the folds are grouped by client, and random and grouped folds score alike,
where how_much_did_it_rain's `No` named storm hours on both sides. The temporal alternative is no cleaner: AIcrowd's
features are noised, its terms are an account's, and its four years give two windows, so it would ship forced too unless
SPLIT-14 is amended. Recorded as the fact in `splits_comment`.
(b) Treat pg17 like how_much_did_it_rain: no CASdatasets build. Build the AIcrowd years as a temporal task if wisconsin
issue 1 (a) amends SPLIT-14 for two windows and AIcrowd's later claim years pass the PROV-3 tests; otherwise `No`.
(c) Reopen how_much_did_it_rain under SPLIT-8 as written.
(d) Change the rule (an amendment: australian issue 1 (d)), decided once for the 8 forced definitions of this run.

**Consistency check B (AI, 2026-11-01):** the target ships in euros, a departure from CLEAN-16's log default.
frempl, both spanish tables and allstate_1m ship log1p, with the Gini on the amount. The reason given (the Gini ranks
expected loss, which squared error on the amount estimates) applies to each of them. What sets pg17 apart?
(a) The random forest's edge on the amount on the shipped splits (0.302 against 0.294, 6 of 9; LightGBM ties). Recorded
as an exception to CLEAN-16 serving USE-5 (the insurer prices expected euros), like wisconsin's.
(b) Treat pg17 like frempl: log1p with `target_transform="log1p"` (one line).
(c) Reopen the four log1p tables to euros (australian issue 5's other option).
(d) Change the rule (an amendment of CLEAN-16 for claim amounts scored by a ranking metric). It is due anyway if
wisconsin, australian and pg17 all ship raw on the pure-premium reason.

**Consistency check C (AI, 2026-11-01):** `pol_insee_code` ships as a category of 17,794 communes (6,775 with one
policy; 12.0% of test rows unseen in training). CLEAN-14 says string for high-cardinality values, and
california_house_prices_2020 ships its 1,132 ZIP codes as string. zillow_prize (Lennart, 2026-10-26) kept the 3,030-level
tract as a category but dropped the 8,334-level block group as a near-identifier. What sets pg17 apart?
(a) The commune is a fixed INSEE list and the only fine geography in the table (zillow keeps latitude and longitude
beside its tract). It stays a category, like zillow's tract, recorded as an exception to CLEAN-14's high-cardinality
clause.
(b) Treat pg17 like california: string, with `pol_department` as the category (the column audit's mildest remedy).
(c) Reopen california's ZIP code as a category (zillow's line).
(d) Change the rule (an amendment of CLEAN-14 that says which clause wins for a high-cardinality code list).

**Consistency check D (AI, 2026-11-01):** pg17 keeps the claim amount as a regression target. pricing_game_2016_french_fleet,
the previous game, became a claim indicator on your question of 2026-10-30, for reasons that partly hold here: claim
sizes are not learnable (R^2 -0.036 on pg17's claimants), and recourse totals net negative. What sets pg17 apart?
(a) Its amounts are untouched euros with a full tail (largest total 141,828), where pg16's charges are scaled by one
constant and stop at 8,565 without explanation. The amount is the pure premium the game priced and fremtpl2's target
(Andrej, 2026-10-20). Written into the target bullet.
(b) Treat pg17 like pg16: a claim indicator with `roc_auc` (claim AUC 0.611 untuned).
(c) Reopen pg16 to its charges.
(d) Change the rule (a family rule for when a claim-cost table becomes a claim indicator).

</details>

<details><summary>Advocate</summary>

**Advocate, opening brief (2026-11-01): pricing_game_2017_french_mtpl**

Position: ship the CASdatasets Year-0 build as defined, grouped by client, after the cheap note and cleaning fixes the
auditors found. No phase A agent found a validity failure (P1-P5). The open items are a P6 metric question that the
whole insurance family shares, and P7 fixes. Under the remedy ladder, none of them is a reason to exclude.

**1. Validity holds, and every claim about the data was reproduced (P4, P5; LEAK-10, LEAK-33, USE-5, PROV-8: Must).**
- Evidence: the column audit finds no leak in any of the 29 features. The rules count every age and duration "from the
  beginning of the current year" (Sec. 4.7, 4.14). `pol_bonus` is shown to be the value from before the claims: to
  Year 1 it rises 24-25% for 1,230 policies with a Year-0 claim, and on its own it ranks Year-0 claims at AUC 0.518.
  `id_client` is used only as the group column. The blind reviewer rebuilt the table from the public `.rda` files with
  a 100% match on target, `client_n_vehicles` and `pol_department`. The claim auditor recomputed every count: 100,000 /
  91,488 / 14,243; 1,116 negative totals; 88.9% zeros.
- Why it outranks the objections: validity outranks value and quality ("validity, then value, then quality"). Every
  objection below sits at P6 or P7, or is a weighing call.

**2. The forced split is not the how_much_did_it_rain case. No outcome crosses the split, and the cost was measured
and goes the safe way (P4; SPLIT-8, Must, still in force; SPLIT-1, SPLIT-4).**
- The curator's `No` on how_much_did_it_rain gave its reason: "forced IID would introduce leaks for this task" (storm
  hours on both sides of the split). The chat line is about forced IID. pg17 is not IID: all of a client's policies
  stay on one side (0 shared clients on all 9 folds).
- Split audit, siblings: under random folds a sibling's claim tells almost nothing (Spearman 0.024; driver-and-commune
  lookup AUC 0.503). Random and grouped folds score the same (LightGBM Tweedie 0.254 against 0.257). The paired
  sibling-removal test gives -0.002 +- 0.003.
- Split audit, cost on the AIcrowd copy of the same portfolio: the shipped design scores 0.268. Next year on held-out
  policies scores 0.277, and next year with the policy's own claims 0.305. So the stand-in underrates the game's task
  by 0.01 to 0.04. It does not overrate it, and overrating is what the rain call guards against.
- Rejecting buys no temporal task. AIcrowd's four years give only two windows above SPLIT-14's floor, so that release
  would ship forced too, on noised features and an account's terms.
- Rule: the curator's call is a precedent, and principles.md follows a precedent "unless a fact sets the new case
  apart". The facts above are that fact (precedent check, prompt A (a)).
- Conceded: the grouped branch of SPLIT-8 is written for stacked periods. Mildest remedy: a SPLIT-8 Cases row ("one
  period, grouped by the entity whose rows share it"), plus one sentence in `splits_comment` with the measured cost
  and the reason for grouping. This is the wording question that frempl issue 5 and rand issue 1 also need settled. If
  the curator amends SPLIT-8 against all forced splits, pg17 should wait with that decision rather than be rejected
  alone.

**3. It is a real, canonical decision, and the task is faithful to its source (P3; USE-1, USE-8, USE-10).**
- Evidence: the domain practitioner (a pricing actuary) confirms the fit: rating factors known at renewal, the
  policy-year claim cost as the label, one premium per policy (Sec. 4.3). Clients compare the sum of their policies'
  premiums (Rule 2), so grouping by client mirrors the decision.
- `fit="approximate"` and `fit_reason` already name the missing claim history. The practitioner measures that gap as
  small (AUC +0.005 with past claims).
- Tension row "a real task against imperfect cleaning" (P3 over P7): keep the task, fix what is cheap.

**4. There is signal under the shipped split. The `no_signal` flag is an artefact of RMSE (P6; TP-2, SPLIT-28).**
- Evidence: Gini 0.20-0.34 for every model family on the 9 splits, claim AUC 0.611. Tweedie deviance skill is +0.057
  (GLM) and +0.048 (random forest) on 9 of 9 splits. The split did not cause the R^2 near 0: IID folds score the same.
- Every fold can be scored (3,599-3,829 claims per fold; constant 0, perfect 1; MET-2 holds).
- Tension row "the right split against the score": a small signal under the right split is no reason to retire.

**5. The metric needs work in the definition, which is no reason to exclude (P6; MET-11, Must, met by a fix; remedy
ladder).**
- Conceded: the closeness is measurable. In a simulated Rule-2 market the Gini tracks profit at tau 0.08-0.64 across a
  broad field, against 0.60-0.82 for a deviance. The reason's phrase "the price level" should say "any monotone
  transform".
- What still holds: among strong, well-regularised learners the Gini is the closest proxy (tau 0.87). It is the
  insurers' standard validation tool, and Allstate and Liberty Mutual chose it.
- The ladder's second rung fixes the definition: either keep `normalized_gini` and write the measured closeness and its
  limit into the reason (mildest), or adopt a Tweedie deviance stand-in. The second needs a new registry metric
  (MET-13) and is shared with australian issue 4 and the other insurance tables, so it should be decided once for all
  of them. The practitioner's own ranking puts this at P6, "fixed in the definition and never excludes the dataset".

**6. The release is the right one: the organiser's own copy, clean features, open terms (P5; PROV-8, PROV-13, PROV-3).**
- Evidence: the original toolbox returns 404 and is not archived. CASdatasets is co-authored by the game's organiser,
  is GPL (>= 2) and pinned to a commit with checksums. The archived rules confirm the structure (100,000 policies,
  client A00091488, at most 6 claims per vehicle).
- AIcrowd noised the features (driver age off by a median 3 years, make and model hashed) and sits behind an account.
- Conceded wording fixes: the rules do not state 14,243 (cite the "maximum is 6" cross-check instead), and the two
  AIcrowd links in the record are related tables, not the source.

**7. Every remaining finding is a cheap P7 fix or a family weighing call. Take the fixes; none decides the verdict
(P7; CLEAN-11, CLEAN-1, CLEAN-12, CLEAN-14, CLEAN-16; "independent failures are not conflicts" cuts both ways: none is
a Must failure).**
- Fixes to take, each a line or two:
  - anomaly counts to 55 first drivers, youngest 5;
  - mask licence ages that imply a licence below 16 (follows caracas);
  - the Peugeot 205 weighing 7,901 kg to missing;
  - `vh_model` as make plus model (the rules advise it, Sec. 4.25);
  - "the family's call" becomes "as suggested (record, 2026-10-30) and as frempl does";
  - give the clip's reason (non-negative losses) and its +4.8% effect, and name the IRSA flat amounts;
  - state that the `client_n_vehicles` probe was run on log1p.
- Weighing calls, each with a defensible default:
  - Raw euros (CLEAN-16): the estimand is the pure premium in euros (USE-5, as wisconsin's exception). Conceded: the
    reason is not specific to pg17, so this belongs with australian issue 5's family decision.
  - The amount, not a claim indicator: pg17 has true euros with a full tail, where pg16's charges are scaled and stop
    at 8,565. fremtpl2's CC (Andrej, 2026-10-20) took the amount.
  - Commune as category or string (CLEAN-14): either works, and `pol_department` stays.
  - Sex: SEL-1 holds. The rules offer the columns, and the vehicle launches date Year 0 to about 2010-11, before the
    2012 ban. Dropping them costs nothing if the curator prefers.
  - The name "MTPL": a rename has costs, and `task_summary` already describes the whole policy correctly.

</details>

<details><summary>Critic</summary>

**Critic, opening brief (AI, 2026-11-01): pricing_game_2017_french_mtpl**

```text
Verdict: do not ship as defined; ship after changes. No point below asks for exclusion on its own.
Validity: SPLIT-8 (Must) stretched past its wording and against the curator's newest call (how_much_did_it_rain, No,
  2026-10-30); its cost line and "what a later release would change" are missing.
Value: MET-11 (Must) closeness is measurable and was measured: the Gini is the weakest of three proxies for the game's
  profit across a broad field; the reason understates its blindness (MET-1).
Quality: CLEAN-16, CLEAN-14 departures without a fact that sets pg17 apart; CLEAN-11 values with a refuted reason;
  wrong counts and an overstated "family's call" in the notes.
```

**1. The forced split stands against SPLIT-8's wording and the curator's newest call (P4, SPLIT-8, Must).**
- Problem: SPLIT-8 allows `ForcedGroupedFromTemporal` only "when the periods are stacked and the entities recur across
  them". pg17 ships one period, and the groups are a client's other vehicles of that period, not one entity across
  periods (split-auditor finding 2; precedent-checker decision 5). By the letter the closest regime is IID with
  `ForcedIIDFromTemporal`, and the curator said on 2026-10-30 "Forced IID is to be avoided at all costs" and sent
  how_much_did_it_rain to `No`: "if the data is temporal but a temporal split is not possible, we cannot split the data
  and reject it". A Must takes no exception; the definition cites SPLIT-8 without addressing either point.
- Effect on the real task: the use case is next-year renewal pricing of known clients with their claim history
  (USE-10). The benchmark tests other clients of the same year without it.
- Evidence: rules p. 1 (U1 holds "(the same) 100,000 policies"); claim persistence on the AIcrowd copy, 16.3% after a
  claim against 9.9% (split-auditor). The record's `Yes` was given on a record that offered the AIcrowd temporal split
  first (precedent-checker), so it does not settle the regime.
- What I concede up front: the forced split is not optimistic (it scores 0.268 against 0.277-0.305 for next-year
  designs on AIcrowd), and grouped and random folds tie (0.257 against 0.254). These are the facts that could set pg17
  apart from how_much_did_it_rain (no outcome shared across the split), but they are not written down.
- Remedy: hold pg17 until the curator settles SPLIT-8 once for the forced definitions of this run (frempl issue 5,
  rand issue 1, australian issue 1 (d)). Mildest working form: the split-auditor's amendment ("or grouped by the entity
  whose rows share the period, when the use case does not know the other rows' outcomes of that period") plus a Cases
  row. If the curator instead applies how_much_did_it_rain as stated, this release is `No`, and the AIcrowd years are
  the only route (they too give two windows, so forced again unless SPLIT-14 is amended).

**2. The forced split's cost and the later release are not stated (P4, SPLIT-8, Must; a fix of the comment).**
- Problem: SPLIT-8 asks for "the cost measured against the valid windows where the data has any" and to "say what ...
  a dated window would change and that it should be recovered if a later release has it". `splits_comment` names the
  AIcrowd years but neither the cost nor what they would add.
- Evidence: split-auditor finding 1: same year held-out 0.268 +- 0.009; next year held-out 0.277; next year seen
  policies 0.289; with own claim history 0.305 (Gini, LightGBM Tweedie, AIcrowd copy). The stand-in underrates the task
  by about 0.01 to 0.04.
- Remedy: one sentence in `splits_comment` with these numbers and the policy's claim history as what a later claim
  year adds (as spanish_motor_insurance_coverage_level_2022_2024 does).

**3. The metric's closeness was measurable, and the measurement goes against the Gini (P6, MET-11 and MET-1, Must).**
- Problem: the reason says profit "rests on ranking the risks" and the builder called closeness unmeasurable. MET-11
  asks for closeness "measured on the shipped splits where possible", and Rule 2 is specified well enough to play a
  Year-1 market on each test fold. The reason also says the Gini "ignores the price level"; it ignores every monotone
  transform, so too-steep or too-flat relativities score like the best tariff, and the game's profit and bankruptcy
  rule punish both.
- Effect on the real task: a benchmark field holds miscalibrated and over-dispersed models; the Gini will rank them
  above tariffs that would earn more. A steeper copy of the best GLM ties the top Gini (0.317) and earns less than a
  flat premium (domain-practitioner, market table). LightGBM-Tweedie prices the book at 0.61-0.74 of its claims and
  still beats LightGBM-MSE on the Gini.
- Evidence: Kendall tau with simulated profit, claim-auditor: Gini 0.28 / 0.08 / 0.56-0.64 in broad fields, against a
  Poisson deviance 0.60-0.82 and RMSE 0.64-0.75; domain-practitioner: Gini 0.33-0.55, Tweedie deviance 0.57-0.79. The
  Gini wins only among six strong, comparable learners (0.87 against 0.73). Wüthrich (2023): the Gini is not strictly
  consistent outside auto-calibrated models.
- Remedy (the curator's call, family-wide with australian issue 4): declare the mean Tweedie deviance (p = 1.5, a
  stated floor on predictions, MET-12 parameters) as the stand-in, with the Gini as a second number; this needs the
  metric in the library (MET-13). Mildest acceptable if the Gini stays: the reason carries the measured closeness, its
  limit (broad fields) and "blind to any monotone transform", not "the price level".

**4. The target's level is changed and its nature undersold, with a reason a pricing actuary would not give (P3,
USE-5, Must holds; the fix is to the notes).**
- Problem: the clip of 1,116 net-negative totals raises total claim cost by 4.8% (Mini 12.5%, Maxi 4.3%). The note
  calls it "the family's call of 2026-10-30", but that call is an AI suggestion the curator has not marked (claim-auditor,
  precedent-checker). The amounts carry IRSA flat rates (843 claims at 1,236.00, 75 at 618.00), and the target sums
  every guarantee of the cover, so "MTPL" describes the 9% on Mini only.
- Effect: harmless under the Gini (model order tau 1.0, 1.0, 0.8 clipped against net), but it biases any level-aware
  metric, which point 3 asks for.
- Remedy: keep the clip; give its reason as the non-negative target that Tweedie and Poisson losses need, with the
  4.8%; write "as the AI suggested (record, 2026-10-30) and frempl does"; name the IRSA mass points and the unstated
  evaluation date; say the target is the whole cover. A rename to `..._french_motor` is the curator's call (it has costs).

**5. Two Should departures without a fact that sets pg17 apart (P7, CLEAN-16 and CLEAN-14, Should).**
- CLEAN-16: raw euros where frempl, both spanish tables and allstate_1m ship log1p with the Gini on the amount. The
  stated reason holds for all of them; the measured edge is model-dependent (RF +0.008 +- 0.004, LightGBM -0.004 +-
  0.009). The cited precedent, australian, recommends log1p itself (precedent-checker, check B). Remedy: record an
  exception with the fact (USE-5, the pure premium in euros; it becomes necessary if a deviance is declared), or ship
  log1p; a third exception for the same reason makes an amendment due.
- CLEAN-14: `pol_insee_code` a category of 17,794 communes, 6,775 singletons, 12.0% of test rows unseen; the rule says
  string for high-cardinality values, and california_house_prices_2020 ships ZIP as string beside a region category
  (column-auditor 1, precedent-checker check C). Remedy: `string` with `pol_department` as the category, or a written
  exception (the only fine geography, a fixed INSEE list).
- Not reasons to exclude: both are quality.

**6. Impossible values kept on a refuted reason (P7, CLEAN-11 and CLEAN-1/CLEAN-12, Should).**
- Licence ages implying a licence at 5 to 15 (8 first, 2 second drivers) are kept "since the ages are whole years";
  whole-year ages cannot produce an age at licence below 18 (column-auditor 3). caracas_cervical_cancer makes such
  values missing. One Peugeot 205 weighs 7,901 kg against 740-1,300 for the other 1,384.
- `vh_model` collides across makes (45 names, 384 rows off the name's main make); the rules say "consider
  concatenating vh_make and vh_model" (Sec. 4.25).
- Remedy: mask `drv_age_lic*` where the age at licence is below 16 and the 7,901 kg weight; set `vh_model` to make plus
  model. Cheap and safe.

**7. Wrong or incomplete statements in the notes and record (P7 notes; EV-1, record house rules).**
- "57 first and 8 second drivers ... the youngest at 8" is 55 and 8, youngest 5 and 8 (claim- and column-auditor).
- "matches the rules' counts ... 14,243 claims": the rules give no claim count; cite "at most 6 per vehicle" (Sec. 4.31).
- The `client_n_vehicles` gain was measured on log1p, not the shipped target; the `pol_department` bullet omits that the
  same probe went down (0.256 to 0.243). Give both numbers or neither.
- `vh_age` has one missing value (BMW 318 I), unmentioned. Year 0 dates to about 2010-11 from vehicle launches, which
  also dates the sex note (optional).
- Record: `required_split` says Temporal while the definition ships grouped; the screening's `rmse` and the
  Assessment's "as for pg15 and pg16" are stale (pg15 retired, pg16 ships `roc_auc`).
- Remedy: edit the bullets and the record fields at hand-over.

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate, rebuttal (2026-11-01): pricing_game_2017_french_mtpl**

The critic and I agree on the verdict ("ship after changes") and on every fact. We differ on one framing: whether pg17
is held pending the family's SPLIT-8 decision or ships with a recorded fact. I ran no new check, because no point
turns on a disputed fact. Every number below comes from the phase A reports.

**1. Forced split against SPLIT-8's wording and the curator's newest call: narrowed.**
- Conceded: the grouped branch of SPLIT-8 is written for stacked periods, and the definition addresses neither that nor
  the how_much_did_it_rain call. A Must takes no exception, so the wording needs a Cases row or an amendment.
- Disputed: that "by the letter the closest regime is IID". SPLIT-8 says "the closest regime that keeps the rows". In
  SPLIT-1 and SPLIT-4 (Must) the split mirrors what is known at the prediction point, and a sibling vehicle's claims of
  the same year are not known when the premium is set.
  - IID would break that in principle, even though its measured effect is nil (0.254 against 0.257).
  - The library also refuses `ForcedIIDFromTemporal` together with a grouping.
  - So grouped is the closest regime under the higher-placed rules. The amendment only writes that reading down.
- The critic concedes the facts that set pg17 apart: the split is not optimistic (0.268 against 0.277-0.305), and no
  outcome is shared across it. The rain `No` rested on shared storm hours ("forced IID would introduce leaks").
- What follows: I accept "hold until the curator settles SPLIT-8 once" as the process step, since frempl issue 5, rand
  issue 1 and australian issue 1 (d) are the same question. My recommendation within that decision is the
  split-auditor's amendment plus a Cases row, with the distinguishing fact written in `splits_comment`.
- The critic's fallback, `No` if the curator applies how_much_did_it_rain literally, would treat unlike facts alike.
  The newest call is about forced IID. Applied as written, it does not cover a grouped split with no shared outcome.

**2. Cost and later release not stated: conceded.** This was my point 2's remedy. Add one sentence to
`splits_comment`: 0.268 same year, 0.277 next year, 0.305 with the policy's own claims on the AIcrowd copy, and that a
later claim year adds the claim history and should be recovered (SPLIT-8).

**3. Metric closeness measured against the Gini: conceded on the facts; the remedy is the curator's.**
- Conceded: closeness was measurable, so "unmeasurable" is wrong. "The price level" must read "any monotone
  transform". The measured tau values and their limit (broad fields) go into the reason (MET-11, MET-1).
- Narrowed: this is P6 and is fixed in the definition, so it does not affect whether pg17 ships. The choice between the
  Gini with caveats and a Tweedie deviance needs a library metric (MET-13) and applies to the whole family (australian
  issue 4).
- One fact for the curator to weigh: among strong, comparable learners the Gini leads (tau 0.87 against 0.73), so the
  answer depends on which field the benchmark expects.

**4. Target level and nature: conceded as note fixes; the rename is contested lightly.**
- Agreed:
  - keep the clip;
  - give the non-negative-loss reason and the +4.8% (Mini 12.5%);
  - replace "the family's call" with "as the AI suggested (record, 2026-10-30) and frempl does";
  - name the IRSA mass points and the unstated evaluation date;
  - say the target covers every guarantee of the cover.
- The rename: `task_summary` already says "a French car insurance policy", and the name follows the source's own title
  (CASdatasets: "French Motor Third-Part Liability datasets"). That is a weighing call with costs, not a fix (P7).

**5. CLEAN-16 and CLEAN-14 departures: conceded that no pg17-specific fact is written; the choice is narrowed to the
curator.**
- CLEAN-16: the reason (USE-5, the pure premium in euros) is the family's, not pg17's. I accept either option: a
  recorded exception, which becomes the natural choice if a deviance is declared under point 3, or log1p like frempl.
  The two points should be decided together: under a Tweedie deviance a log1p fit needs back-transformation, and the
  practitioner measured log1p back-transformed at a level of 0.01 (deviance skill -5.1). That favours raw euros if the
  metric changes.
- CLEAN-14: string with `pol_department` as the category (the column audit's mildest remedy) is fine. So is a written
  exception (the only fine geography, a fixed INSEE list). Either works.

**6. Impossible values: conceded.** Mask the licence ages that imply a licence below 16 and the 7,901 kg weight, and
set `vh_model` to make plus model (Sec. 4.25). These are cheap and safe (CLEAN-11, CLEAN-1, CLEAN-12), and my point 7
listed them.

**7. Notes and record: conceded in full.**
- Fix the counts to 55 and 8, youngest 5 and 8.
- Replace the 14,243 claim with "at most 6 per vehicle".
- Give both probe numbers for `client_n_vehicles` and `pol_department`, or neither.
- Mention the missing `vh_age` value and the estimated 2010-11 dating.
- Sync `required_split` to Grouped and remove the stale `rmse` and "as for pg15 and pg16" lines.

**Where this leaves the call.**
- Ship after the P7 fixes in points 2, 4, 6 and 7.
- The metric (point 3, with CLEAN-16) and the SPLIT-8 wording (point 1) go to the curator as family-wide decisions.
- Nothing either side found asks for exclusion.

</details>

<details><summary>Critic rebuttal</summary>

**Critic, rebuttal (AI, 2026-11-01): pricing_game_2017_french_mtpl**

```text
Verdict unchanged: ship after changes; no point asks for exclusion on its own.
Conceded: advocate 1 (in part), 3, 4, 6 and 7, and the remedy rung of 5.
Disputed: advocate 2. The curator's how_much_did_it_rain CC has a second, general clause the advocate leaves out, and it
  covers pg17. So the split waits for the curator's SPLIT-8 decision; the advocate's own fallback agrees.
```

Check run: I read the curator's lines in `curation/records/how_much_did_it_rain.md` (lines 62-70) to settle point 2.

**Advocate 1 (validity holds): conceded in part.** LEAK-10, LEAK-33, PROV-8 and USE-5 hold; the counts and the rebuild
were reproduced, and I raised no leak. Disputed: "no phase A agent found a validity failure". SPLIT-8 is P4. The split
auditor calls the tag "a wording call ... since a Must takes no exception", and the advocate concedes in point 2 that
the grouped branch "is written for stacked periods". That is an open P4 question, not a P6 or P7 one.

**Advocate 2 (not the how_much_did_it_rain case): disputed, narrowed.**
- The advocate quotes only the first half of the curator's reason. The CC reads: "forced IID would introduce leaks for
  this task. What are you blabbing, if the data is temporal but a temporal spliot is not possible, we cannot split the
  data and reject it" (record, line 63). The second sentence is a general rule. It does not depend on leaks or on the
  IID regime, and pg17 meets its condition: the task is temporal by its use case (the advocate's point 3, USE-10), and
  the release cannot give a temporal split. Under the precedence rule, the curator's newest decision beats an AI reading
  of the rule. The "fact that sets the case apart" the advocate offers (no outcome crosses the split) answers the first
  sentence, not the second.
- Conceded facts: 0 shared clients; random and grouped folds tie (0.254 against 0.257; paired test -0.002 +- 0.003);
  the stand-in underrates the next-year task by 0.01 to 0.04. Also conceded: rejecting pg17 buys no temporal task,
  since AIcrowd gives two windows. These facts make an amendment reasonable. They do not license shipping against the
  curator's stated rule without asking.
- Where we agree: the advocate's own fallback, that "pg17 should wait with that decision rather than be rejected
  alone", is my remedy. A Cases row is not enough on its own: a Cases row records how a rule was applied, and this
  applies SPLIT-8 outside its wording, where principles.md says "anything else is an amendment". So I ask for the
  amendment (or a `No`), decided once with frempl issue 5 and rand issue 1, plus the cost sentence in `splits_comment`.
  On the cost sentence we agree.

**Advocate 3 (a real, canonical task): conceded.** USE-1 and USE-8 hold, and so does `fit="approximate"`. One
narrowing: the "AUC +0.005" for the claim history is the record's claim AUC on AIcrowd. Measured as the shipped metric,
the history adds about +0.03 Gini (0.305 against 0.277, split-auditor). That is still small, and it does not change the
fit.

**Advocate 4 (signal under the split): conceded.** TP-2 keep, SPLIT-28 not triggered, MET-2 holds. I raised none of
these.

**Advocate 5 (metric fixed in the definition): conceded on the rung, narrowed on the content.**
- I agree it never excludes the dataset (P6), and that it is decided once for the family with australian issue 4.
- On the content: the Gini's tau 0.87 holds only in the six-learner field. The question is which field a benchmark
  meets, and TabArena's field includes miscalibrated models. There the claim auditor measured 0.08-0.64 for the Gini.
  MET-11 asks for "the closest computable metric", and both measurements of closeness rank a deviance closer.
- So the mildest rung (keep the Gini) meets MET-11 only if the reason states the measured closeness, its limit, and
  "any monotone transform". Without those three, the reason makes a claim the measurement refutes.

**Advocate 6 (the right release): conceded.** PROV-8 and PROV-13 hold, and so does the wording fix for 14,243. Add the
record fix the blind reviewer named: mark the AIcrowd links as related tables.

**Advocate 7 (P7 fixes and family calls): conceded.** The fix list matches my points 4, 6 and 7. CLEAN-16 and CLEAN-14
go to the family decisions (australian issue 5; precedent prompts B and C), and I accept the advocate's defaults as
defensible if they are written as exceptions with their facts. Sex and the name: I raised neither as a condition. Two
items from my point 7 are missing from the advocate's list: the stale record lines (`required_split` Temporal, the
screening's `rmse`, "as for pg15 and pg16") and the `pol_department` probe number. Both are one-line fixes.

</details>
