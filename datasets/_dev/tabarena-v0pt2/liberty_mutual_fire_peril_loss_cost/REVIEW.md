# liberty_mutual_fire_peril_loss_cost

**Outcome:** added. The AI recommends shipping it; the panel's changes are made (below), and the forced split and
`var11` as the metric's weight and a feature (issue 2, MET-2 amended) are settled (2026-11-02). Liberty Mutual's Kaggle
competition of 2014 on commercial fire losses: 452,061 labelled policies with 299 anonymised features (policy, crime,
geodemographic and weather blocks); the target is the host's undisclosed transform of the loss over the total insured
value (0 for 99.74%, 1,188 losses), shipped as log1p and scored on the published scale by the competition's normalized
Gini weighted by `var11`; random 3-fold split tagged as forced from temporal. Validity: USE-1 holds, fit approximate
(USE-5: the transform is undisclosed, and 58% of the losses exceed 1, so the scale is not a plain loss ratio); LEAK-10
and LEAK-38 hold and are now measured (the weather block stays the same across a risk's terms, so it is the location's
climate; `var13` does not move at a loss); LEAK-24 holds as tested; LEAK-30 finds no leak (the host's normalising
constant comes from outside these records); SPLIT-8 is met, the split shipped on your call of 2026-11-02 (a forced IID
split ships when the leak test across the random split finds none; SPLIT-8 amended); SPLIT-9 holds: a test policy's
later terms sit in training, but they carry nothing of its outcome; LEAK-19 and LEAK-20: the exact copies stay. Value:
TP-4 holds (a regularised LightGBM scores 0.306-0.320 against 0.221-0.260 for `var13` alone, the strongest single
feature, on every fold); MET-4, the host's metric, verified against its test case (MET-13); MET-2 holds as amended on
your call of 2026-11-02: `var11`, known for train and test rows alike, is both a feature and the metric's weight (issue
2, resolved). Quality: the target ships as log1p (CLEAN-16), like the log1p siblings; an answer of 'dollars' for the
family in australian issue 5 reverses it; CLEAN-19 cited for `var4_group`. Weighed: the insurer's own policies, losses
and metric +, size +; 1,188 losses, so fold scores move by about 0.04 -, undisclosed target transform and anonymised
features -. Left for Andrej: none (issue 2 resolved 2026-11-02).

Changes made after the review panel (AI, 2026-11-01): the target ships as `log1p_transformed_loss_ratio` with
`target_transform="log1p"`, the Gini still on the published scale (log1p scored higher on 2 of 3 shipped folds, 0.313
against 0.298 on average; follows allstate_claim_prediction_challenge_1m; australian_vehicle_insurance_2004_2005 issue 5
names this table among the log1p tables); the normalisation note no longer calls it a potential leak; the
prediction-point note gives the measured checks; the split note gives how often risks recur on three keys, how many test
rows have a later term in training, and the test showing no gain from it, instead of the score gap; the copies note
gives its two kinds and 4.8-4.9% of test rows with a copy in training; `var13`'s range, the tie clause, `changes`,
`fit_reason` and the `var4_group` citation updated; the `task_target_value_dominant` warning accepted (real zeros); a
note on fold noise. Each row's fold is assigned from its content, so the new target values moved rows between folds:
every number below is re-measured on the shipped folds of the changed definition (the panel's reports, at the end,
describe the definition before the changes).

Changes made on 2026-11-06 (AI, under the exposure rules; no re-review panel): the metric reads `var11_weight`, a copy
of `var11` declared as its weight scoring column (MET-2 as reworded on 2026-11-05), and `var11` stays a feature; no
training weight is declared, and the warning `task_metric_weight_without_sample_weight` is accepted because the weight
is a function of the features (MET-15). Not checked on the data and not re-reviewed: the competition's files download
only after its rules are accepted on Kaggle (https://www.kaggle.com/competitions/liberty-mutual-fire-peril/rules), so
the panel of 2026-11-06 did not run; it runs once the data is in the warehouse.

**Main points:** All issues are resolved: `var11` stays a feature and is the weight of the competition's Gini, MET-2
amended (issue 2).

**Issues for Andrej:**

2. **Score without `var11`'s weight (the unweighted Gini as a stand-in), or keep `var11` as a feature and as the
   metric's weight through an amendment of MET-2?** The competition weights each policy by `var11` in its Gini.
   `var11` is also an input: it is the square root of a round sum insured ($250,000 floor), the host lists it among the
   "policy characteristics" and gave it to every team in the test file, and an underwriter always has the sum insured
   (USE-6, Must: an input known at the prediction point stays). MET-2 (Must) says a metric's input, a weight among
   them, "is never a feature". The record's suggested call of 2026-10-30 made it a scoring column only.
   * What it does to the task: keeping `var11` as a feature games nothing. On a weighted Gini the best order is by
     expected loss whatever the weights, and as a feature `var11` moved an untuned model's score by -0.010 on average
     (-0.060 to +0.084 over 6 random folds), within fold noise. australian's exposure is different: claims cut it short
     and it divides that table's cost per year, so as a feature it lifts the weighted per-year Gini to 0.238, above
     every honest model. `var11` is set at underwriting and moves no differently in a loss term. The stand-in (b)
     changes what is scored: a small policy counts as much as a large one, while the host weights by the square root of
     the sum insured, and the loss rate rises from 0.18% to 0.54% across `var11`'s deciles (blind review).
   * The rules as written: keeping both breaks MET-2. MET-2's own remedy, keeping `var11` a feature and declaring the
     unweighted Gini as a stand-in, meets both Musts and costs only MET-4 (Should: the competition's metric), so there
     is no conflict for USE-6 to win. A scoring-column copy of `var11` would meet MET-2's wording while models still
     read the weight, so it is the amendment under another name. Dropping `var11` as a feature breaks USE-6.
   * Evidence on the stand-in (3 shipped folds of the changed definition, one LightGBM configuration: 400 trees,
     learning rate 0.03, 15 leaves, at least 200 rows per leaf, row and column subsampling 0.8 and 0.5, L2 10; the more
     regularised model of the outcome scores 0.313): weighted, the model scores 0.322 against 0.235 for `var13` alone;
     unweighted, 0.288 against 0.247. On the definition before the changes, with other folds, the mediator found the
     stand-in reversed that order (0.232 against 0.248) and recommended the amendment for that reason. Both unweighted
     gaps (+0.041 now, -0.016 then) lie within about one fold standard deviation (0.04), and on one of today's folds the
     model still trails `var13` unweighted (0.262 against 0.266), so under the stand-in the order moves with the folds.
     The reversal no longer argues for (a), and today's order does not show that (b) changes nothing; the recommendation
     rests on the rules, not on the order.
   * Implemented: nothing yet. The definition keeps the source's weighted Gini with `var11` as a feature, so as it
     stands it breaks MET-2 and holds only under (a). (b) waits for your call because the mediator recommended (a) and
     (b) replaces the source's metric (one line in the definition; every score changes). Alternatives: (a) amend MET-2:
     "a weight the source ships to its participants as a policy characteristic stays a feature", aligning definitions.md
     (one line says "never a feature", the bundle check says "allowed"); (b) the unweighted normalized Gini as a
     stand-in, `var11` a feature; it loses MET-4 and the weighting by size; (c) `var11` a scoring column only, like
     g_research_crypto_forecasting_1m's `Weight`, which breaks USE-6.
   * Precedent: g_research_crypto_forecasting_1m (a weight that is no attribute of the row, a scoring column only). In
     this run, wisconsin_local_government_property_insurance_fund's `ordered_lorenz_gini` takes the fund's premium as
     its base and as a scoring column, not a feature. The premium is the output of the rating the task replaces (the
     rating variables explain 98% of its log), while the other features explain 70% of `var11`'s (column audit). frempl
     issue 4 and australian issue 4 offer an exposure-weighted Gini; if they keep exposure as a feature, they meet the
     same MET-2 question. So (a)'s wording decides them too, and it must exclude a weight that the outcome cuts short
     (australian's 0.238) and a weight that is the rating's output (wisconsin). Liberty would be the first weight that
     is also a feature; a Must takes no exception, hence the amendment under (a). The advocate and the critic agree on
     the facts and on (a) or (b); they differ only on whether (c) is an option.

   Recommendation: (b), since it meets both Musts as written and costs only a Should (MET-4, the competition's metric);
   the mediator's reason for (a), the reversed order, did not hold on the re-measure. (a) if you want the competition's
   metric and its weighting by size kept; that is an amendment, not an exception. Decision: (a), (b) or (c)?

   **Andrej (2026-11-02, change):** I want to score with the feature and also keep it as a feature assuming it to be
   known during train and test time as input for the model.

   **Answer (AI, 2026-11-02):** Implemented (a). The definition keeps the competition's `normalized_weighted_gini`
   with `inputs={"weight": "var11"}` and declares no scoring column, so `var11` stays a feature; its curation note now
   cites the amended MET-2. Checked on the in-memory container: `var11` is among the 299 columns
   `feature_columns(container)` returns, and `scorer(container)(y_test, y_pred, test_idx)` equals the Gini weighted by
   the test rows' `var11` on every shipped fold (`-var13` scores 0.260, 0.225, 0.221; unweighted 0.266, 0.222,
   0.254). MET-2 amended: "except a weight known at the prediction point for train and test rows alike, which stays a
   feature and is also the metric's weight (amended 2026-11-02, Andrej, liberty_mutual_fire_peril_loss_cost: the sum
   insured `var11`, which the host gave every team as a policy characteristic; [your note])", with a Cases row. The
   library already allowed a metric input that is not a scoring column (`task_metric_input_is_model_input`, info), so
   no code changed: the `MetricSpec.inputs` docstring and definitions.md's "never a feature" line now name the
   exception, and a test covers it (`test_weight_that_is_also_a_feature_stays_a_model_input_and_weighs_the_score`).
   `dataset check`: 0 errors, 0 warnings, 2 info; pytest passes.

   **Resolved (2026-11-02, Andrej):** (a), the weighted Gini with var11 as weight and feature; MET-2 amended.

3. **Ship `var11`'s copy as the scoring column the metric reads (MET-2 as reworded on 2026-11-05)?** The definition
   read the feature `var11` directly as the weight of `normalized_weighted_gini`; MET-2 as reworded in #44 says a
   feature the metric also needs stays a feature and ships a copy as a scoring column, so the scoring columns are the
   complete set of a metric's extra data. The check now warns `task_metric_input_is_feature`.
   * Implemented: `_clean` copies `var11` into `var11_weight`, a `ScoringColumn(role="weight")` the metric reads;
     `var11` stays a feature. No training weight is declared: the weight is a function of the features (MET-15), and
     the warning `task_metric_weight_without_sample_weight` is accepted with that reason. Scores do not change (the
     copy holds the same values).

   **Lennart (2026-11-05, PR #47):** MET-2 wants scoring copies: `var11` -> `var11_weight` (role weight); `var11`
   stays a feature.

   **Resolved (2026-11-06, Lennart):** the copy, as asked; `dataset check` waits for the raw data (Kaggle's rules for
   the competition are not accepted on the download account yet).

**Review panel:** ship after changes; issue 1 (the forced split) can still turn it to `No` (mediator). Claim audit: 29
claims, most hold; 1 refuted, 3 refuted in part and 1 incomplete, all in notes and numbers, now fixed. Blind review:
exclude as prepared, on squared-error scoring (no model beats the mean), but a genuine ranking signal under the
competition's weighted Gini, which the definition declares. Debate: agreed on the task, the metric, the copies, the
target scale and the note repairs; disputed: the forced split and the later terms in training (issue 1) and `var11` as
feature and weight (issue 2). On issue 2 the mediator recommended the MET-2 amendment, measured on the old folds; issue
2 now recommends the stand-in and says why. The reports below describe the definition before the panel's changes; their
fold numbers predate the log1p target, which moved rows between folds.

<details><summary>Mediator</summary>

**Mediator (2026-11-01): liberty_mutual_fire_peril_loss_cost**

**Recommendation**

```text
Verdict: ship after changes; issue 1 (the forced split) can still turn it to `No`.
Validity: SEL-1/SEL-2 hold; USE-1 holds, fit approximate (USE-5: undisclosed transform, 58% of losses above 1);
  LEAK-10 and LEAK-38 hold, now measured (weather static between terms, var13 does not move at a loss); LEAK-24 holds
  as tested; LEAK-30: no leak (an outside constant), note reworded; LEAK-19/LEAK-20: copies kept, reason corrected;
  SPLIT-8 met as `ForcedIIDFromTemporal`, open against how_much_did_it_rain and SPLIT-8's grouped branch (issue 1);
  SPLIT-9 holds (no measurable shortcut; the tension row, as in lending_club and avito_demand_prediction_1m);
  SPLIT-29 not triggered (the risk carries no label, AUC 0.504-0.525); PROV: all counts reproduce.
Value: TP-4 holds on average, noisy per fold (EV-8); MET-4 the host's weighted Gini; MET-13 verified (host test case,
  exact ties); MET-2 broken as written by `var11` as feature and weight (issue 2).
Quality: CLEAN-16 departure's reason refuted, fixed (log1p, scored on the published scale, MET-3); CLEAN-3/5/10 hold;
  CLEAN-19 citation added.
Weighed: the insurer's own policies, losses and metric +; 452,061 rows +; 1,188 losses, fold sd about 0.04 -;
  undisclosed target transform and anonymised features -.
For the curator: issue 1, ship the forced split or `No` (one SPLIT-8 call with frempl, australian, rand, spanish);
  issue 2, amend MET-2 for `var11` or declare the unweighted stand-in.
```

**Agreed facts**

* 452,061 policies (50.1% of the id range), 99.74% exact zeros, 1,188 losses from 0.006 to 25.9; 58% of losses exceed 1,
  so the scale is not a plain loss ratio. Skew 1.90 on the published scale, -0.16 logged.
* The host split at random ("The train and test sets are split randomly") and scored that split; how_much_did_it_rain's
  host refused a random split (thread 14245). The use case (next term's book) is temporal; the release has no dates and
  no risk id, so any split is forced (grouped as much as IID).
* Risks recur: 22.3% (exact narrow key, all but `var15`), 47.5% (`var11` free), 63.9-65.6% (`var11`, `var13` free) of
  rows. On the shipped folds 16.7-16.9 / 39.1-39.2 / 53.5-53.7% of test rows have their risk in training; 6.2-6.3 /
  18.1-18.2 / 24.8-25.0% a later term; 5.3-5.4% only later terms (narrow key).
* The risk carries no label: a risk's training loss ranks its test terms at AUC 0.504-0.525 on every key; 6-14 losses
  share a risk with another loss; taking a test risk's terms out of training costs no more than dropping as many random
  rows (split auditor, 9 folds; claim auditor, shipped folds). No policy variable changes more often after a loss.
* The narrow-key grouped split leaves 42.8-43.3% of test rows with their risk in training on the widest key (advocate);
  wider keys merge sparse rows by chance (groups up to 375 rows), which SPLIT-24 bars.
* Weather is the location's climate (unchanged in 94.6-96.9% of consecutive-term pairs); crime and geodem never change;
  `var13` changes at 23.1% of loss terms against 28.3% of zero terms. Newest term: 0.261% against 0.292% losses (p 0.47).
* The host's normalising constant is not these records' mean (177 of 213 columns lie more than 10 SE from 1).
* `var11` is the square root of a round sum insured ($250,000 floor), listed by the host among the policy
  characteristics and shipped in test.csv; a weighted Lorenz curve cannot be gamed through its weight.
* Exact copies: 28,965 rows; 47 of 49 loss groups also hold a zero; 11,433 of the 16,981 extra copies have `var15`
  missing, 5,548 share a `var15`; 4.8-4.9% of test rows have a copy in training (not 2.1%).
* Every fold scorable (369-410 losses; constant 0, oracle 1). log1p beats the published scale on 3 of 3 shipped folds
  (0.2536 / 0.2862 / 0.2750 against 0.2533 / 0.2620 / 0.2699).

**Decisive check (mediator)** (a script in the run folder, not committed; shipped folds, one regularised
LightGBM configuration, threads capped)

* The critic's narrow-key as-of filter keeps 291,058-291,172 of 301,374 training rows. It removes the narrow-key later
  terms (6.2% to 0) but leaves 12.6-12.7% (`var11` free) and 19.6-19.8% (widest) of test rows with a later term in
  training: the same residue as the grouped split. Score: 0.247 unfiltered against 0.238 filtered (per fold -0.010 /
  -0.043 / +0.028), fold noise.
* Weighted (declared) against unweighted (the MET-2 stand-in) normalized Gini, mean of 3 folds:

| scorer | weighted by `var11` | unweighted |
|---|---|---|
| `var13` alone | 0.237 | 0.248 |
| LightGBM, all features | 0.247 | 0.232 |
| LightGBM without `var11` | 0.261 | 0.241 |
| `var11` alone | -0.073 | -0.062 |

  The stand-in is not a neutral substitute: it reverses the order of the single-feature baseline and the model. With
  this configuration the model beats `var13` on 2 of 3 folds under the declared metric (the builder's on 3 of 3), so
  TP-4 holds on average and the noise note (EV-8) matters.

**Changes to make now (no decision needed)**

1. Target: `log1p_transformed_loss_ratio` with `target_transform="log1p"`, the metric on the published scale (CLEAN-16,
   MET-3; follows allstate_claim_prediction_challenge_1m). Reproduce: log1p ahead on 3 of 3 shipped folds (0.2536 /
   0.2862 / 0.2750 against 0.2533 / 0.2620 / 0.2699). Name Liberty in australian issue 5; a family answer of "the
   published scale" reverses this line.
2. The LEAK-30 bullet: normalised by an undisclosed outside constant (177 of 213 columns more than 10 SE from 1 on the
   train half), no test-row statistic; drop the `Potential leak, kept on purpose:` label (LEAK-30).
3. The prediction-point bullet: replace "cannot be checked" with the measured passes (weather 94.6-96.9% unchanged
   between terms, crime and geodem never; `var13` not moved at a loss; newest term not under-reported) (LEAK-10,
   LEAK-38, LEAK-24).
4. `splits_comment` and `task_summary.split`: the three key widths and their shares above, the AUC 0.504-0.525 lookup
   and the paired result as the reason for IID instead of the 0.232/0.260 gap (SPLIT-4); the narrow-key hold-out was
   partial; 5.3-5.4% of test rows have only later terms in training, no measured shortcut, so SPLIT-9 holds (tension
   row; lending_club, avito_demand_prediction_1m). Reproduce: the critic's as-of count, the advocate's grouped overlap and the mediator's decisive check (run folder).
5. The copies bullet: two kinds (11,433 with `var15` missing, 5,548 sharing `var15`, perhaps locations of one account);
   kept under LEAK-19 and LEAK-20's label-ambiguity clause; 4.8-4.9% of test rows have a copy in training. `row`: a row
   may be one location of an account.
6. `var13` range 0.215-0.259 (tie-averaged); re-run `dataset check` so the README metric carries the tie clause (TP-4,
   MET-13).
7. `task_summary.changes`: add the dropped `weatherVar115` and `var4_group`; the `var4_group` bullet cites the data
   page's hierarchy and thread 10194 (CLEAN-19).
8. `fit_reason`: 58% of losses exceed 1, so the scale is not a loss ratio (USE-5).
9. Accept `task_target_value_dominant` in `dataset.py` (real zeros: policies without a fire loss).
10. A noise note: fold sd 0.036-0.046 in weighted Gini with one repeat of 3 folds (EV-8); 3 repeats only if the house
    protocol takes an override.

**Changes that need the curator**

* Issue 1: the forced split (ship, `No`, or a SPLIT-8 amendment; under the "forced IID is a reject" amendment, a
  re-split grouped on the narrow key).
* Issue 2: `var11`: a MET-2 amendment (the draft stays) or the unweighted stand-in.

**Disputed points**

1. *SPLIT-8, forced IID (P4).* Advocate: SPLIT-8 (Must) ships it as `ForcedIIDFromTemporal`; the leak how_much named is
   measured absent; SPLIT-19 (Should), the host's own split. Critic: the curator's stance ("at all costs") sets no
   condition on leak size; SPLIT-5 (Must) makes the host's split a claim, not a fact; SPLIT-8's text points to grouped
   for stacked recurring entities. Ruling: not a conflict the ranking settles. SPLIT-8 as written allows the shipped
   regime; the curator's stance is a newer decision of the curator that SPLIT-8 does not yet carry, and only the
   curator can say whether it reaches this case or becomes an amendment. Both sides now agree the grouped split is
   forced too, so the stance decides ship or `No`. On IID against grouped within SPLIT-8: the narrow-key grouped split
   removes only the exact-key overlap (54% to 43% on the widest key) and turns renewal pricing, a warm start (USE-10),
   into a cold start; that is the fact that sets Liberty apart from allstate_claim_prediction_challenge_1m, which
   grouped on a published household id. Curator issue 1, with the four siblings' options.
2. *SPLIT-9, later terms in training (P4, Must).* Critic: a Must about what may be in training; the order is known, the
   filter cheap (3.4% of training rows). Advocate: the tension row asks to remove the measurable shortcut, and none is
   measurable; the filter is partial. Ruling: the tension row (SPLIT-9 against SPLIT-10/SPLIT-14) settles it: SPLIT-9 is
   met by removing a shortcut shown to tell a test row's outcome; four tests show none (AUC 0.50-0.52, two paired
   drops, the as-of run above). The diffuse rest has no window for SPLIT-10 to act on in a dateless forced split; the
   forced regime already trains beside later terms of other risks. Same ruling as lending_club and
   avito_demand_prediction_1m. No filter; the numbers go into `splits_comment` (change 4). Under option (a) of issue 1
   the curator can still ask for the filter on principle; it leaves 12.6-19.8% of test rows with a later term in
   training on the wider keys.
3. *MET-2, `var11` feature and weight (P6 against P3).* Advocate: P3 USE-6 (Must) outranks P6 MET-2. Critic: no conflict,
   since MET-2's stand-in meets both Musts at the cost of MET-4 (Should). Ruling: the critic is right on the rules as
   written (principles step 4: a conflict exists only when meeting one rule breaks the other; MET-4 itself yields "only
   to MET-2"). A `ScoringColumn` copy of `var11` meets MET-2's letter while the model still reads the weight, so it is
   the amendment by another name and adds a duplicate column; a `ScoringColumn` that removes `var11` from the features
   breaks USE-6. So the choice is the amendment (the curator's alone) or the stand-in. The decisive check shows the
   stand-in reorders the baseline and the model, so it changes what the benchmark measures. Curator issue 2,
   recommendation: amend.

**Consistency with precedent** (precedent checker's 14 decisions)

* Follows: the tag, the copies (hiva_agnostic, qsar_tid_11; no exception needed), the source metric (MET-4 cases,
  allstate_1m), exposure inside the ratio, zeros as published, drops of `id`/`dummy`/`weatherVar115`, `Z` as missing,
  `var13` kept (LEAK-38).
* Departures, now resolved: the target scale (log1p, as allstate_1m; change 1); `var4_group` cited (change 7); LEAK-30
  reworded (no longer a kept leak; its drift settled on the keep side in 2026-10-19 is not reached).
* Departures left to the curator: forced split against how_much_did_it_rain (issue 1, same options as frempl issue 5,
  australian issue 1, rand issue 1, spanish issue 1); IID against Allstate's grouping (the distinguishing fact: no
  published id, an exact key covering 22% of rows, the risk carries no outcome, renewals are a warm start; if not
  accepted, option (d) of issue 1); `var11` against MET-2 and g_research_crypto_forecasting_1m (issue 2, an amendment,
  not an exception: a Must has none). Liberty would be the first weight under definitions.md line 235's allowance; the
  amendment should align lines 222 and 235.
* Flag, not follow: porto_seguro and allstate_claims_severity ship dateless Kaggle insurance tables without a regime
  tag, against SPLIT-8.
* Third case: four tables of this run (australian, frempl, rand, spanish) plus Liberty ask one SPLIT-8 question; the
  answer should be one amendment, not five exceptions.

</details>

<details><summary>Claim audit</summary>

**Claim audit (claim-auditor, 2026-11-01): liberty_mutual_fire_peril_loss_cost**

**Verdict: ship after note changes.** Every validity claim I could test held up: the prediction point (now partly
measured), the IID split (a paired test on the shipped folds shows no gain from seeing the same risk), the target,
the dropped columns and the metric's source and code. What I refuted are numbers and stated mechanisms. The notes
understate how often a risk repeats (about 65% of rows, not 22%). The LEAK-30 note names a mechanism the data rules
out. A third of the exact copies are not "terms" as claimed. The var13 numbers and the README's metric definition
predate the tie handling now in `metrics.py`. The builder report's "2.1% of test rows with a copy in train" should
read 4.8-4.9%. Two calls stay with the curator: var11 as both weight and feature (MET-2 against USE-6), and the
SPLIT-8 regime.

**Claims and tests**

| # | claim | source | test | result | evidence | rule |
|---|---|---|---|---|---|---|
| 1 | 452,061 policies, "the competition's labelled half" | task_summary.row, curation bullet 1 | the id range of train.csv | holds | ids run 1-902,789: 452,061 of 902,789 (50.1%); data page "almost a million insurance records" | EV-2 |
| 2 | 99.74% exactly 0, 1,188 losses 0.006-25.9, none negative or missing | task_summary.predicted, bullet 3 | counted on the frame | holds | 450,873 zeros, min positive 0.00577, max 25.92, 0 negative, 0 missing | USE-5 |
| 3 | use case quoted from the competition | task_summary.use_case | Description page | holds | "more accurate identification of each policyholder's risk exposure and the ability to tailor the insurance coverage" | USE-1 |
| 4 | "a test policy's risk is often in training in another term" | task_summary.split | share of each shipped test fold whose risk key is on the training side | holds, understated | 16.7-16.9% on the narrow key (all but var15); 53.5-55.5% on the wide key (#20) | SPLIT-8 |
| 5 | changes: drop id and dummy, code Z as missing | task_summary.changes | against `_clean` | incomplete | `_clean` also drops weatherVar115 and adds var4_group | writing |
| 6 | prediction point: features anonymised, "their timing cannot be checked (whether the weather variables are the location's climate or the term's weather is not stated)" | bullet 2 | pairs of rows one var15 step apart, equal in every policy and location column except var10, var11 and var13: does the weather vector change? | the "cannot be checked" part is refuted. The check supports the claim | the weather vector is identical in 94.6% of 126,063 consecutive-term pairs (changes in 5.4%); crime and geodem vectors never change between terms. So the weather block is a static attribute of the location, not the term's weather | LEAK-10, LEAK-38 |
| 7 | var13 "like an underwriting grade, so it stays" | bullet 12 | conditional test: does var13 change at the term of a loss more than at a zero term? (a post-loss re-grade would show that) | holds; the test could have refuted it | var13 changes at 79 of 342 loss terms (23.1%) vs 28.3% of 128,745 zero terms (Fisher p 0.035, fewer, not more); mean change +0.002 vs +0.003 (MWU p 0.73); in the term after a loss 21.8% vs 28.3% | LEAK-38 (no LEAK-10 mechanism measured) |
| 8 | var11 known at the prediction point | bullet 8 | the same conditional test; the host's test file | holds; one weak signal | var11 changes at 57.0% of loss terms vs 55.5% of zero terms (p 0.59), as a sum insured re-declared at renewal would; mean increase +17.7 vs +10.4 (MWU p 0.03, one of six tests run, not a mechanism). It ships in test.csv: thread 9706's awk prints test.csv column 14 as var13, so id plus var1-var17 come first | USE-6 |
| 9 | id randomised by Kaggle; loss rate 0.25-0.28% per id decile | bullet 4, decision 1 | decile table, plus id order within risks | holds | within-risk rank correlation of id with var15 -0.006 (70,481 rows); the later term has the larger id in 49.7% of 24,426 pairs; id gaps of copy pairs match random pairs (median 264,907 vs 265,157). The id carries no time order either | CLEAN-3 |
| 10 | dummy is B exactly where var9 is Z | bullet 5, decision 2 | crosstab; thread 10101 | holds | 123,185 vs 0 off the diagonal; thread: "dummy = if var9=='Z' then 'B' else 'A'" | CLEAN-5 |
| 11 | Z means missing in var1-var9; var4's letter is its higher level | bullets 6-7 | data page; var4 levels | holds | every non-Z level of var4 is a letter followed by a digit | CLEAN |
| 12 | weatherVar115 is 0 wherever present | bullet 8 | raw values | holds | 448,201 non-missing, all 0 | CLEAN-5 |
| 13 | var11 is the weight and stays a feature; as a feature it moves the score by -0.002 (-0.058 to +0.037) | bullet 8, decision 3, builder issue 1 | the numbers; whether the dual role lets a model game the metric | numbers hold. The dual role is a departure from MET-2 (Must). The P3 argument holds | var11_experiment.txt. A row's slope on the weighted Lorenz curve is its y, so the best order is by E[y given x] whatever the weights: the dual role buys no gaming. But the record's Assessment and the 2026-10-30 policy table say "var11 a scoring column", and the curator's CC line has not decided it | MET-2, USE-6 |
| 14 | "213 of 289 numeric columns have a mean between 0.9 and 1.1, as if divided by a mean over all its records, test half included (LEAK-30)" | bullet 9 | dividing by the mean of the 902,789 records, with a random split, would leave the train half's mean within about sd/sqrt(904k) of 1. Count how many are | count holds; mechanism refuted | 213 in the band, but only 9 of them lie within 3 SE of 1 (using the more lenient sd/sqrt(n_train)), and 177 lie more than 10 SE away. Median distance from 1 is 0.091 for geodem and 0.049 for weather. The mean over distinct location vectors is not 1 either (geodem 0 of 37 within 0.01). The constant came from another population | LEAK-30 |
| 15 | copies kept: 28,965 rows, 16,981 extra, all 49 loss groups also hold a zero, 2 losses with a loss copy | bullet 10, decision 4 | recount | holds | identical counts; 50 losses in copy groups | LEAK-16, LEAK-20 |
| 16 | "They are terms of one risk, as the rows equal in all but var15 show" | bullet 10 | var15 among the copies | partly refuted | 11,433 of the 16,981 extra copies have var15 missing, so a term step cannot show. The other 5,548 (32.7%) share a non-missing var15: they are not terms that var15 separates. These are the 5,548 "steps equal to 0" in decision 5. 7 of the 49 loss groups have var15 | LEAK-18, LEAK-19 |
| 17 | "2.1% of test rows have an exact copy in train" | builder report (leak probe) | exact keys with NaN treated as equal, on the shipped folds | refuted | 4.8%, 4.9% and 4.8% of test rows; 2.4%, 2.0% and 4.4% of test losses. 70.7% of copy rows have var15 missing, which a NaN-unequal comparison misses | LEAK-16 |
| 18 | var13 alone 0.215-0.255; regularised LightGBM 0.253-0.270, higher on every fold | bullet 11 | rescored with the current library | holds in substance; numbers stale | var13 alone now scores 0.2353, 0.2151 and 0.2589. 21% of test rows tie at var13's lowest value; `metrics.py` (15:45) now treats tied predictions as one step, and the probes (13:36) used row order. The note's 0.2391/0.2149/0.2546 are the row-order values. LightGBM stays above on every fold, by 0.018, 0.047 and 0.011 | TP-4 |
| 19 | 2,588 geodem, 327 crime, 24,531 weather vectors | bullet 12 | distinct rows per block | holds | counting the all-missing vector as one (2,587, 326 and 24,530 without it) | - |
| 20 | "22.3% of the rows are equal in every column but var15", 36,708 steps of 1; "only 6 of the 1,188 losses share their risk with another loss" | splits_comment, decision 5 | widen the key to the columns that change between terms (dropping var15 and one column at a time) | literally true; as the extent of repeated risks, refuted | var11 changes in 57,408 consecutive-term pairs and var13 in 22,361. With var10, var11, var13 and var15 free, 65.6% of rows share a risk (63.9% without var10). Within those groups 83.1% of var15 steps are exactly 1 and 11.5% are 0, so these are terms and not chance merges. 14 losses share a risk with another loss | SPLIT-8, SPLIT-29 |
| 21 | holding out whole risks gives 0.232, geodem vectors 0.231, weather vectors 0.210, against 0.260 random | splits_comment | the files; what the risk key held out | numbers hold; the risk check is partial | grouped_check.txt, risk_key_check.txt. The narrow key leaves about two thirds of the repeated risks crossing the split | SPLIT-30 |
| 22 | IID split; "an insurer prices renewals of its own risks", so the risk is "not a group new data would lack" | splits_comment, data_tags | EV-1, paired on each shipped fold with one model (the builder's regularised LightGBM): A) full train side; B) without the train rows of the test fold's risks; C) without the same number of random train rows. All scored on the same test rows | holds: no measured gain from seeing the same risk | B minus C: narrow key +0.046, +0.036, +0.013; wide key -0.038, +0.005, +0.057 (B drops 38% of the train side). Under A, test rows whose risk is in train score 0.232/0.260/0.278 vs 0.272/0.273/0.264 for the rest. The risk does not carry the label, so SPLIT-29 does not trigger | SPLIT-4, SPLIT-29 |
| 23 | the newest losses are fully reported (builder: cannot verify) | builder report | the loss rate in the newest term of multi-term risks against their earlier terms | holds as far as tested | 84 of 32,135 (0.261%) vs 110 of 37,655 (0.292%); OR 0.89, Fisher p 0.47. Rows in repeated risks lose at 0.248% vs 0.267% for single rows | LEAK-24 |
| 24 | metric: normalized weighted Gini, weights var11, from the Evaluation page | `Metric.source`, README Metric block | the page text | holds | "evaluated on the normalized, weighted Gini coefficient. The weights used in the calculation are represented by var11". Read from the builder's capture of Kaggle's page API; the live page is JS-only and could not be re-fetched | MET-4, MET-11 |
| 25 | the implementation equals the host's corrected code (thread 9880) | builder report, spec definition | the host's test case; random inputs; ties | holds. The builder's "the tie-break by row order matches the host's R code" is refuted | test case -0.821428571428572 reproduced. No ties: max difference 9e-15 over 200 cases. With ties the library returns the exact mean over tie orderings (difference at most 4e-16 on 30 cases of 7 rows). The host's code scores a constant -0.009, +0.070 and -0.027 on the folds as stored (sd 0.05 over row orders); the library scores 0. The README's definition lacks the tie clause the spec now has | MET-13 |
| 26 | computable on every fold | MET-2 | `scorer` on a stand-in container (the definition's frame and task) | holds | constant 0.0000 and oracle 1.0000 on each fold; 369, 409 and 410 losses per test fold; var11 never missing | MET-2 |
| 27 | same scale and meaning as the source | MET-2, MET-3 | target transform; balance | holds | target as published (`identity`); both halves are random, so the same loss rate | MET-3 |
| 28 | warning `task_target_value_dominant`: real zeros | builder report | #23; the data page | holds | no newest-term deficit; target defined as a loss ratio | LEAK-24 |
| 29 | no sibling or duplicate | record screening | grep of records and datasets | holds | the only other mentions are precedent citations (frempl, australian_vehicle_insurance) | PROV-6 |

**Refuted and untested claims, ranked (validity first, Must first)**

1. **The extent of repeated risks (P4; SPLIT-8, SPLIT-29; #4, #20, #21).** The splits comment and decision 5 rest on
   the narrow key. Risks repeat across about 65% of rows, and 53.5-55.5% of each test fold's rows (44-48% of its
   losses) have their risk on the training side. The decisive test (#22) finds no gain from that overlap, so IID
   and `ForcedIIDFromTemporal` still hold. SPLIT-8's text ("grouped by the entity when the periods are stacked and the
   entities recur") still reads against IID. SPLIT-24 forbids grouping on a feature hash, and the true risk id was
   never published. That stays the curator's call (builder issue 2), now with the right numbers. *What it changes:*
   the numbers in splits_comment, the task_summary split line and decision 5. *Mildest remedy:* give the wide-key
   shares, say the narrow-key hold-out was partial, and add the paired result.
2. **The LEAK-30 mechanism (P4; LEAK-30; #14).** The constant is not a mean over these records, test half included:
   177 of the 213 columns sit more than 10 SE from 1. It is an undisclosed constant from another population, which is
   LEAK-30's fixed-scale reading (no leak). *What it changes:* the "Potential leak, kept on purpose" bullet loses its
   mechanism. *Mildest remedy:* reword it as "normalised by an undisclosed constant that is not these records' mean
   (177 of 213 columns lie more than 10 SE from 1 on the train half); no test-row statistic", or drop the
   potential-leak label.
3. **Why the copies are kept (P4; LEAK-18, LEAK-19; #16, #17).** "Terms of one risk" explains the 11,433 extra
   copies whose var15 is missing. It does not explain the 5,548 that share a var15. The keep decision still stands on
   LEAK-20's ambiguity clause (all 49 loss groups hold a zero) and on #22 (seeing same-risk rows, copies included,
   does not raise the score). *What it changes:* the reason in bullet 10 and the builder's 2.1% (it is 4.8-4.9% of
   test rows). *Mildest remedy:* split the reason into the two kinds of copy and give 4.8-4.9%.
4. **The prediction point, "timing cannot be checked" (P4; LEAK-10, LEAK-38; #6, #7, #23).** Refuted in the
   dataset's favour. The weather block is static between terms (94.6%), crime and geodem never change, and var13 does
   not change at the term of a loss. The newest term shows no reporting deficit. *What it changes:* three
   cannot-verify items in the builder's checklist (weather timing, var13 and LEAK-24) become measured passes.
   *Mildest remedy:* one sentence in bullet 2 and one for LEAK-24.
5. **Stale metric numbers and definition (P6; MET-13, TP-4; #18, #25).** The var13 range is now 0.215-0.259. The
   README's metric definition and the builder's tie statement predate the uncommitted change to `metrics.py` (ties
   averaged over their orderings, which I verified as exact). TP-4 still holds. *Mildest remedy:* re-run
   `dataset check` and update bullet 11's range.
6. **var11 as both weight and feature (P6 against P3; MET-2 against USE-6; #8, #13).** This is not refuted, but it
   breaks a Must as written and disagrees with the record's Assessment and the 2026-10-30 policy table. In its favour:
   it is known at the prediction point, re-declared at each term, ships in the host's test file, and its dual role
   cannot game a weighted Gini. *For the curator:* keep it as a feature with this reason (an exception or a MET-2
   amendment for weights that are also real attributes), or make it a `ScoringColumn` (measured cost -0.002, within
   noise).
7. **task_summary.changes is incomplete (P7; #5).** *Mildest remedy:* add "drop a constant weather column and add
   var4's letter as a column".

*Untested:* the tuned methods against var13 (TP-1; needs `tuned_results.py`). The undisclosed target transform
(USE-5; cannot be tested). A live re-read of the Evaluation page (JS-only; I used the builder's API capture). The
screening's AUC 0.70 and log1p R^2 0.16, superseded by the add-stage numbers. The winner's 0.332 (no evidence
under EV-4). The var11 increase at loss terms (p 0.03, one of six tests), left as a weak signal.

*Observation (EV-8, for whoever reads the scores):* the metric is noisy at about 400 losses per fold. In #22,
dropping 10% of the training rows at random moved a fold's score by 0.007-0.026, and dropping 38% by 0.02-0.09. The
builder's default LightGBM scored 0.18-0.20 on the shipped folds and 0.23-0.33 on other random 3-fold assignments.
One repeat of three folds resolves methods only coarsely.

**Files:** scripts and outputs in the run folder (not committed): the definition frame and splits; the target, id, scaling, copies and newest term; the columns that change between terms and the normalisation population; the wide keys, the overlap per fold and the change at the loss term; the host code, ties, dummy and oracle per fold; the paired same-risk experiment; the weather between terms.

</details>

<details><summary>Column audit</summary>

**Column audit: liberty_mutual_fire_peril_loss_cost** (column-auditor, 2026-11-01)

**Verdict:** no column has to go. Ship the columns as defined, with three note edits. One call goes to the curator:
`var11` as both a feature and the metric's weight.

```text
Verdict: ship (columns), note edits suggested.
Validity: LEAK-1/USE-3 prediction point written (underwriting, before the term). LEAK-10 holds for all 299 features:
  no post-outcome field found. The weather block stays fixed across a risk's terms (it changes in 1.0% of 107,547
  one-year steps). The four columns that change between terms (var11, var13, var15, var17) change no more often going
  into the loss term than in the same risks' other steps. No missingness encodes the outcome (conditional test, 10
  fields). The LEAK-38 keep of var13 holds and has now been partly tested. The LEAK-30 note holds for the 213 location
  columns; the policy block is per-row transforms, which LEAK-30 allows.
Value: USE-6 / LEAK-37 against MET-2 on var11: a call for the curator (problem 1).
Quality: CLEAN-3 (id), CLEAN-5 (dummy, weatherVar115), CLEAN-10 (Z), CLEAN-12/CLEAN-19 (var4_group), CLEAN-14 hold.
For the curator: var11 stays a feature, or becomes a ScoringColumn.
```

**How I checked.** I read the frame through `dataset_io.from_definition`: no build exists yet. It has 452,061 rows, the
target and 299 features (10 category, 289 float64). The codebook is the data page (saved in the run folder)
plus forum threads 9679, 9706, 9779, 9825, 10026, 10101, 10187 and 10194.

"Terms of a risk" means rows that are equal in every feature except the ones under test, with `var15` one higher. I
kept only groups with one row per `var15` value. This follows the builder's reading of `var15` as an age. Two facts
support it: `var11` rises by a median 1.8% between such rows, as an insured value indexed at renewal would, and the
dropped `id` is random against their order.

Scripts and outputs: in the run folder (not committed).

**Column table**

| column | meaning (codebook; decoded form where the data shows one) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `transformed_loss_ratio` | target: "The transformed ratio of loss to total insured value"; the transform is not disclosed | the term's outcome | float64 as published, renamed. 99.74% exactly 0; 1,188 losses from 0.006 to 25.9; none negative or missing. Not logged again, because the metric reads the published values | fine | USE-5 (fit approximate), CLEAN-15; departs from CLEAN-16 with reason (MET-3) |
| `var1` | policy characteristic, ordinal 1-5; meaning unknown | yes, per the host's test file; changes in 0.5% of a risk's one-year steps | category, Z -> missing (74.8%); level 5 has 46 rows | fine | CLEAN-10, CLEAN-14 |
| `var2` | nominal A-C; unknown | yes | category, Z -> missing (99.0%) | fine | CLEAN-10 |
| `var3` | ordinal 1-6; unknown | yes; 0.5% of steps | category, Z -> missing (87.4%) | fine | CLEAN-10, CLEAN-14 |
| `var4` | nominal: 42 hierarchical codes, the letter being the higher level; unknown | yes; changes in 4.2% of steps, 1.3% going into a loss term | category, Z -> missing (4.49%). Losses with var4 missing: 87, against 66.4 predicted from the other columns (p 0.018 on its own, about 0.18 across the 10 fields tested) | fine (a weak excess with no known cause) | LEAK-38, EV-6 |
| `var4_group` | built: the letter of var4. 18 levels, loss rate from 0.07% (K) to 0.69% (I) | as var4 | category; missing where var4 is | fine | CLEAN-12, CLEAN-19 |
| `var5`, `var6` | nominal A-F and A-C; unknown | yes | category, Z -> missing (92.0%, 94.1%) | fine | CLEAN-10 |
| `var7`, `var8` | ordinal 1-8 and 1-6; unknown | yes; 2.1% and 1.8% of steps | category, Z -> missing (0.19%, 1.65%). var8's missing rows hold 4 losses where the base rate gives 19.6, but the other columns predict 4.3 | fine | CLEAN-10, LEAK-38 |
| `var9` | nominal A/B; unknown | yes | category, Z -> missing (27.25%), exactly where the dropped `dummy` is B. Its missingness among the losses is predicted exactly (201 against 201) | fine | CLEAN-10 |
| `var10` | unknown. exp(var10²/2) is a whole number for all 106 values, from 1,100 to 10,001,000. Most are 1,000 plus a standard deductible step (2,000 is 35% of rows; then 6,000, 11,000, 1,500, 3,500, 26,000, 101,000), so it looks like a deductible amount (my inference) | yes; 2.5% of steps, 0.9% going into a loss term | float64, no missing; a per-row transform | fine | LEAK-30 (per-row is fine), CLEAN-14 |
| `var11` | "var11 is the weight used in the weighted gini score calculation", listed among the policy characteristics. var11² is a whole number in 93.9% of rows (46.6% are multiples of 1,000). Range 250,000 (1.04% of rows sit at this floor) to 198.9 million, median 884,000. So var11 is the square root of a dollar amount, like an insured value (my inference) | yes. It rises by a median 1.8% per one-year step (45.7% of steps unchanged, 95th percentile +5%). It rises in 54.7% of loss terms and 50.8% of the others. The other features explain R² 0.70 of log var11 (0.65 for the policy variables alone) | float64, no missing | question for the curator (feature and weight) | USE-6, LEAK-37 against MET-2 |
| `var12` | unknown; exp(var12²) − 1 is a whole number from 0 to 50,002,004 | yes; 0.4% of steps | float64, 78.5% missing. 302 zeros (no losses, 0.6 expected); 0 is no documented code, and the next smallest values are 1, 2 and 4 | fine | CLEAN-10 (no code can be inferred) |
| `var13` | unknown. exp(var13²) − 1 is a whole count from 0 to 4,362 (333 values; 20.6% are zero). The strongest single feature (weighted Gini 0.215-0.255) | yes, per the host. It changes in 27.4% of steps in loss-free risks, 21.6% going into a loss term and 21.4% coming out of one. No reset at a loss: it falls in 9.9% of loss terms against 12.0% elsewhere | float64, no missing | fine; keep with the note, reworded | LEAK-38 |
| `var14` | unknown; exp(var14²) − 1 is a whole count from 0 to 109 | yes; 0.7% of steps | float64, 64.3% missing, 27.6% zero | fine | CLEAN-14 |
| `var15` | unknown. Whole years in 97.9% of values (36 rows end in .5), from 0 to 440.5. It goes up by 1 between a risk's consecutive rows, so it reads as an age | yes (the age at the term) | float64, 21.9% missing (70.7% of the exact-copy rows). 518 rows are above 200 and 34 above 300 | fine (extremes kept: the meaning is not stated) | CLEAN-11 |
| `var16` | unknown; whole numbers 0-100, like a percentage | yes; 0.6% of steps | float64, 80.0% missing | fine | CLEAN-14 |
| `var17` | unknown; continuous 0-100 (24,598 values), 17.8% zero | yes. It changes in 21.4% of steps. Going into a loss term it changes in 27.6%, but in 26.2% of the same risks' other steps (p 0.62), so the higher rate belongs to the risk, not to the loss term | float64, no missing | fine | LEAK-10 |
| `crimeVar1`-`crimeVar9` | "normalized Crime Rate variables" of the location | yes (location); 327 vectors, exactly one per geodem vector | float64. 24.3% of rows lack the whole block (loss rate 0.259% against 0.263%). Row means 0.98-1.05 | fine (LEAK-30 note) | LEAK-30 |
| `geodemVar1`-`geodemVar37` | "normalized geodemographic variables" of the location; 2,588 vectors | yes (location) | float64. 0.44% of rows lack the block. 21 of 37 means lie in [0.9, 1.1]. Five columns have negative values (normalised). geodemVar24 holds 3 values (0.4894 × {0, 2, 3}) and stays numeric | fine | LEAK-30, CLEAN-14 (anonymised, so numeric) |
| `weatherVar1`-`weatherVar236` (235; 115 dropped) | "normalized weather station variables"; 24,531 vectors, each inside one geodem vector (with one exception) | yes. The vector changes in 1.0% of 107,547 one-year steps (0.7% going into a loss term), so it is a fixed attribute of the location, not the term's weather | float64. 0.41% of rows lack the block (2 losses against 3.0 predicted). Sub-blocks 181-198 (2.68% missing) and 210-226 (7.16%) share their missing masks. 183 of 235 means lie in [0.9, 1.1]. weatherVar145 and weatherVar152 take one value in 99.9% and 99.8% of rows; kept, since they are not constant. weatherVar224 holds 9.0976 × {0..4} and stays numeric | fine | LEAK-10, LEAK-30, CLEAN-5, CLEAN-14 |
| `id` (dropped) | "A unique identifier"; Kaggle "randomized the id column" (thread 10026) | not a time index either: within the 5,943 risks with 3 or more terms, Spearman(id, var15) is -0.001, and id rises in 49.3% of one-year steps | dropped | fine | CLEAN-3 |
| `dummy` (dropped) | "Nuisance variable used to control the model, but not working as a predictor"; B exactly where var9 is Z | n/a | dropped | fine | CLEAN-5 |
| `weatherVar115` (dropped) | 0 in all 448,201 rows where present (99.15%). Missing in 3,860 rows, a mask no other column has, with no signal (loss rate 0.233% against 0.263%) | n/a | dropped | fine | CLEAN-5 |

**Problems, ranked by principles.md**

1. **`var11` is both a feature and the metric's weight (P3 USE-6 and P4 LEAK-37 against P6 MET-2; a call for the
   curator).** Both rules are Musts:
   * MET-2 says a weight is never a feature.
   * USE-6, in a higher part, keeps any input known at the prediction point.

   Meeting MET-2 means dropping var11 as an input, so the two genuinely conflict. Under principles.md the higher Must
   wins. That is not an exception, because a Must has none.

   The column facts support the USE-6 side.
   * var11 is the square root of a whole-dollar amount: 93.9% of rows, 46.6% multiples of 1,000, a floor at 250,000,
     median 884,000.
   * Between a risk's consecutive terms it rises by a median 1.8%, like an indexed sum insured, and it moves no
     differently in a loss term (up in 54.7% against 50.8%, down in 2.5% against 3.5%). So it is not an earned exposure
     or a revision after the loss, and it is set at underwriting.

   This separates it from the closest sibling in the batch, wisconsin_local_government_property_insurance_fund. That
   dataset ships `Premium` as a ScoringColumn because the premium is the output of the rating the task replaces: the
   rating variables explain 98.1-98.5% of its log. Here the other features explain R² 0.70 of log var11 (0.65 for the
   policy variables alone).

   The host lists var11 among the "policy characteristics" and ships it in the test file. Thread 10194 found it "much
   better to use it as feature rather than as weight". Neither choice costs measurable signal: the builder's paired
   difference is -0.002 (-0.058 to +0.037 over 6 folds).

   Remedies:
   * keep var11 as a feature, recording that USE-6 outranks MET-2 and naming the fact that sets it apart from
     wisconsin: an exposure input, not the rating's output;
   * or, if the curator holds to MET-2's wording, declare `ScoringColumn("var11", role="weight")`, the mildest remedy.

2. **`var13` stays under LEAK-38, but the note's reason should say what the data shows (P4, LEAK-38, Should; a note
   edit).** The bullet calls var13 "like an underwriting grade". The data show a whole count: exp(var13²) − 1 runs from
   0 to 4,362 (333 values, 20.6% zero).

   LEAK-38 asks for a timing test where one can be run:
   * Across a risk's one-year steps the count changes in 27.4% of steps in loss-free risks, 21.6% going into a loss
     term (n 324) and 21.4% coming out of one (n 299).
   * In the same loss risks' other steps it changes in only 14.5% (n 352). Against the loss term that gives p 0.02, but
     it is one test of about a dozen, and the rate going into the loss term equals the rate coming out of it, which is
     history known at the next renewal.
   * It falls in 9.9% of loss terms against 12.0% elsewhere, so there is no reset at a loss, which a claims-free count
     would show.

   No post-outcome mechanism is measured, so the keep stands. Remedy: reword the reason to "a log-transformed whole
   count (0 to 4,362) that changes at about 27% of renewals, no more often going into a loss term (22%) than coming out
   of it (21%)". Revisit if its meaning is ever published.

3. **The weather block's timing can be measured: it belongs to the location, not the term (P4, LEAK-10 / LEAK-38; a
   note edit).** The prediction-point bullet ("whether the weather variables are the location's climate or the term's
   weather is not stated") and the builder's "cannot verify" list treat this as untestable. I left the 235 weather
   columns, var11, var13 and var15 out of the risk key and followed each risk's one-year steps:
   * the weather vector changes in 1.0% of 107,547 steps;
   * 0.7% of steps going into a loss term (n 295);
   * 1.1% coming out of one (n 277).

   The term's weather would change almost every year. So the block is a fixed attribute of the location, known at
   underwriting. Remedy: replace the parenthesis with this measurement. `fit_reason`'s "neither the scale of the loss nor
   the timing of each feature can be checked" could narrow to the policy variables.

4. **No missingness encodes the outcome (P4: LEAK-10, and LEAK-38's conditional test). Holds.** For each field, an
   out-of-fold LightGBM on the shipped folds predicts its missingness from the policy, crime and geodem columns. I then
   compared the predicted and observed missing counts among the 1,188 losses:

   | field | predicted | observed |
   |---|---|---|
   | var8 | 4.3 | 4 |
   | var9 | 201 | 201 |
   | var1 | 995 | 995 |
   | var15 | 178.8 | 164 |
   | var12 | 1006.9 | 1007 |
   | var14 | 839.3 | 852 |
   | var16 | 1013.6 | 1020 |
   | whole weather block | 3.0 | 2 |
   | weather 181-198 | 24.9 | 19 |
   | var4 | 66.4 | 87 |

   The var4 excess has p 0.018 on its own and about 0.18 across the ten fields. It is a "maybe", not a finding (EV-6):
   no mechanism shows, and var4 changes less often going into a loss term (1.3%) than in the same risks' other steps
   (2.8%, p 0.28). No action.

5. **The LEAK-30 note is correct but could say where the scaling sits (P4, LEAK-30, Should when weak; a note edit).**
   The 213 columns with a mean in [0.9, 1.1] are all location columns: crime 9 of 9, geodem 21 of 37, weather 183 of
   235, so 213 of the 281 location columns. The "normalized" policy variables are per-row transforms of whole numbers:
   var10 = sqrt(2 ln m), var11 = sqrt(m), var12-var14 = sqrt(ln(1 + k)). LEAK-30 allows those.

   The block means are not exactly 1, either over the rows or over the distinct location vectors, so the normaliser is
   not identified and "test half included" stays a suspicion. Remedy: write "213 of the 281 location columns; the
   policy variables are per-row transforms".

6. **`var15` explains most of the exact copies (P4, LEAK-16/18/19; supports the bullet).** 70.7% of the 28,965
   exact-copy rows have var15 missing, against 21.9% of all rows. For a risk with no recorded age, consecutive terms
   with unchanged var11, var13 and var17 come out as exact copies. That supports "They are terms of one risk". The
   other 8,494 copy rows repeat the same var15 value. No column action; the split call is the split auditor's.

7. **Cleaning nits, no action (P7).**
   * `var15` above 200 (518 rows) and above 300 (34 rows; max 440.5) would be implausible as a building's age, but the
     meaning is not stated, and CLEAN-11 needs a value that is impossible by its meaning.
   * `var12`'s 302 zeros are no documented code.
   * The ordinals var1, var3, var7 and var8 ship as unordered categories, as the data page lists them as categorical.
     Their loss rates are not monotone in the level anyway (var8: 0.33, 0.27, 0.22, 0.23, 0.20, 0.39%).
   * `geodemVar24` and `weatherVar224` are coded levels kept numeric (CLEAN-14, anonymised).
   * Exact inverses of var10-var14 back to whole numbers exist (CLEAN-12), but their meaning would be our guess and
     trees are indifferent to them. I don't recommend shipping them.

**A correction in my scratch output.** The two weather lines of `term_keys.txt` are wrong: that run left the weather
columns in the key. The corrected test is `term_changes2.txt`.

**Files:** scripts and outputs in the run folder (not committed): missingness, zeros and extremes per column; the conditional missingness test; the decoded policy variables; var11, var13 and var14 across terms; weather, var17 and the others across terms; risk-level or loss-term change; location statics, scaling, id against time, weatherVar115, copies by var15, var11 R^2.

</details>

<details><summary>Split audit</summary>

**Split audit (split-auditor, 2026-11-01): liberty_mutual_fire_peril_loss_cost**

**Verdict: right with notes.** Random policies tagged `ForcedIIDFromTemporal` is a defensible stand-in for "price next
term's book" on a release with no dates and no risk id. The repeated risks cross the split, but they carry almost no
label: a risk's training loss ranks its test terms at AUC 0.51-0.52. Taking a test risk's other terms out of training
costs no more than dropping as many random rows. The notes understate how often risks repeat, and they do not say
that training sometimes holds the *later* term of a test risk. Whether SPLIT-8's grouped branch applies is the curator's call
(the precedent checker's prompts 1 and 2); my evidence favours IID, on the facts below.

**What I checked** (frame and splits loaded through `dataset_io`; scripts and outputs in the run folder, not committed: the risk structure, the key sizes, the paired runs and the
alternative split)

* Shipped splits: 1 repeat x 3 folds (the house default above 250k rows), 301,374 train rows per fold, 369-410 losses
  per test fold. The data has no time column and the id is randomised (also no order within a risk, claim auditor #9),
  so there are no windows, gap or season to check.
* Regime the use case implies (USE-10): underwriting a commercial fire policy before the term. A renewal is a known
  entity (a temporal, warm-start task, where the risk's history is legitimate). New business is partly a cold start.
  The truth is a stream over time, so the split has to be forced (SPLIT-7, SPLIT-8). The declared regime and tag match.
* Risk keys (no id exists; built from equal values, SPLIT-24): narrow key = equal in every column but `var15`. It is
  exact: 22.3% of rows, 42,738 risks, groups of at most 12, and 83.8% of the `var15` steps are exactly 1, so these
  are terms. Wide keys with `var11` and then `var13` also free: 47.5% and 63.9% of rows. They behave like terms too
  (80.6% and 84.2% of steps are 1, and `var11` grows with `var15` in 95.7% of changed steps), but they are not exact.
  Groups reach 375 rows, and in groups of 21+ rows `var12` is missing in 98-99%, so sparse rows merge by chance.
* Overlap on the shipped folds (narrow key): 16.7-16.9% of test rows have their risk in train. 6.2-6.3% have a *later*
  term in train, 5.3-5.4% only later terms, and 4.8-4.9% an exact copy. On the wide key, 39.1-39.2% have their risk
  in train, and on the widest 53.6-53.7%.
* Label carried by the risk: among test rows whose risk is in train, "the risk had a training loss" scores AUC 0.517 /
  0.506 / 0.525 (narrow key), 0.509 / 0.504 / 0.515 (wide), 0.506 / 0.506 / 0.514 (widest). Only 6 / 10 / 12 losses share
  their risk with another loss.
* Paired training-side test (EV-1). Same test rows, regularised LightGBM, weighted Gini, wide key, 3 random 3-fold
  seeds (9 folds). Taking out every training term of the test risks (b) costs -0.045 on average (sd 0.035). Taking out
  as many random rows (d) costs -0.060. So b beats d by +0.015 (b higher in 6 of 9 folds): seeing the risk adds nothing
  beyond the row count. On the shipped folds, b minus d = -0.014 / +0.043 / +0.050.
* The alternative split, fitted: grouped 3-fold on the wide key against random 3-fold, 3 seeds each, same model.
  Grouped mean 0.265 (fold sd 0.046, range 0.177-0.324), random 0.295 (sd 0.036, 0.215-0.327). The gap of 0.030 is
  about 1.5 standard errors and smaller than one fold's spread. The builder's narrow-key check (0.232 against 0.260,
  sd 0.066) points the same way. SPLIT-4 bars deciding on the gap.
* Hidden-group probe: no hits (builder), consistent with the near-zero label carried by the risk.

**Problems, ranked by principles.md**

1. **Later terms of a test risk sit in training (P4; SPLIT-9 read through SPLIT-8).** 5.3-5.4% of test rows have only
   *later* terms of their risk in train (narrow key, more on the wide key): outcomes from after the test term's
   prediction point. Evidence that it does not act as a shortcut: the risk's training loss ranks at AUC 0.50-0.52. On
   the shipped folds, removing the later terms (variant c) moves the score by -0.027 / +0.007 / -0.014, which is fold
   noise. Mildest remedy: no re-split. Say it in `splits_comment` with these numbers. An as-of filter (drop the later
   terms of test risks from training, as alfa_battle_2_0_task_2 did for SPLIT-9) is available on the narrow key, but it
   removes no measured shortcut, and SPLIT-9 asks that a filter remove one.
2. **IID against SPLIT-8's grouped branch (P4; SPLIT-8, SPLIT-24, USE-10). The curator decides.** SPLIT-8's text
   ("grouped by the entity when the periods are stacked and the entities recur") and the run's Allstate draft point to
   `ForcedGroupedFromTemporal`. Facts that set Liberty apart:
   (a) no id. The only exact key (narrow) leaves about two thirds of the repeated risks crossing a "grouped" split, and
   the wider keys merge sparse rows by chance (SPLIT-24).
   (b) the use case is mostly pricing known risks (USE-10), which a grouped split, being a cold-start test, does not
   represent.
   (c) the risk carries no measurable label (the paired test above), so SPLIT-29 does not trigger.
   If the curator still wants grouped, the mildest remedy is `ForcedGroupedFromTemporal` on the narrow, exact key,
   stating that it is partial. Expect about 0.03 lower scores, within the fold noise.
3. **The notes understate the repetition (P4/P7 note accuracy; SPLIT-8).** `splits_comment` and `task_summary.split`
   give 22.3% and "only 6 of the 1,188 losses". These figures are exact for the narrow key but are lower bounds:
   47.5-63.9% of rows repeat on keys that free `var11` / `var13`, which change between terms. The 0.232 "whole risks"
   check used the narrow key, so about two thirds of the repeats still crossed it. Remedy: text only. Give the range of
   keys, the AUC 0.51 lookup and the paired result (b vs random drop) as the measured reason for IID, not the gap.
   Also add the later-term point (problem 1).
4. **Benchmark resolution (P4, minor).** One repeat of 3 folds with about 400 losses per test fold gives a fold
   standard deviation of 0.036-0.046 in weighted Gini on random folds (0.015-0.066 in the builder's runs). That is as
   large as most model differences on this task. Remedy: if the protocol allows an override, 3 repeats (the folds take
   about 30 s each for a GBM). Otherwise note the noise.
5. **Exact copies across the split (P4, minor; LEAK-16).** 4.8-4.9% of test rows have an exact copy in train. The
   builder report's "2.1%" counts NaN as unequal and is wrong (the claim auditor agrees). The copies carry no label:
   every loss-holding copy group also holds a zero, and only 2 losses have a copy with a loss. No re-split. Correct the
   report's figure.

**Not problems:** the weather and location blocks recur across almost every row (99.4% of rows share all location
blocks with another row). This is the insurer's own territory, and new business mostly lands where the book already
is, so a location-grouped split would test a use the task does not have (SPLIT-30; held out, 0.210-0.231). The host's
own random split (SPLIT-19) agrees with the regime.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner: liberty_mutual_fire_peril_loss_cost**

**Actor.** I am a commercial property underwriter or pricing actuary at Liberty Mutual. At new business or renewal I rank each business policy by its expected fire loss cost per dollar insured. That rank sets the underwriting tier and the schedule credit or debit, and picks the risks to refer or send to loss control. Commercial property is rated per $100 of insured value, so loss over insured value is the quantity my rates are built on. The definition's `use_case` names the actor (Liberty Mutual) and the moment ("when it underwrites"). Its decision, "tailor the coverage", is the host's wording and vague under USE-1.

**Fit: approximate (agree).** The decision, the policies and the losses are Liberty Mutual's own. But the target is an undisclosed transform that cannot be read as a loss ratio (USE-5). With no policy year, random policies stand in for next year's book (USE-8, the weighed factor against rephrasing under USE-9). USE-9 offers no direct reading: any use I would phrase still scores future policies.

**1. Inputs at the prediction point (USE-3, USE-6)**

- I have all four blocks when I quote or renew. The policy variables are anonymised, but they read like COPE and account data: `var4`'s two-level code (letter, then number) looks like an occupancy or industry class, `var13` like an underwriting grade, `var15` like an age that steps by 1 per term. Crime, geodemographic and weather scores are standard third-party add-ons by address (vendors sell COPE data and peril loss costs "for quote and renewal decisions").
- Weather is the location's climate, not the term's weather. This settles most of the open question in the first `curation_comments` bullet. I keyed rows equal in every policy variable except `var15` and in the geodemographic and crime blocks. Of the 31,239 such groups with more than one `var15` value, which I read as several terms of one risk, 30,257 (96.9%) keep one weather vector across their terms. A term's own weather would change from year to year.
- `var11` is a sum insured, so it is a legitimate feature. `var11` squared is a whole number for 93.9% of rows and a multiple of $1,000 for 43.8%. The minimum is exactly 250,000 (1.0% of rows sit at `var11` = 500), the median 884,000 and the maximum 199M. The commonest values are 250,000, 500,000, 300,000, 400,000, 600,000 and 1,000,000. So `var11` is the square root of a round dollar amount, most likely the insured value or limit, with a $250,000 floor. That is the exposure base: I always have it, and it sets the premium. Removing it as a feature would change the task to "price without the sum insured" (USE-6). This backs the builder's issue 1 (feature and weight), and it agrees with the policy reasoning of 2026-10-30 ("A sum insured is a feature too, the size of the risk") over that day's table line, which calls `var11` a scoring column.
- Inputs I would always have that are missing:
  - The current premium or manual rate. This gap matters most for the metric (point 5).
  - The account's loss history from earlier terms. For fire this matters little: 6 of the 1,188 losses share their risk with another loss.
  - The effective date and the term length. Without them nothing tells whether a term was a full year.
  - The deductible and the limit, unless they hide among `var1`-`var17`.
- Inputs I would not have: none found. `id` is dropped. The column scaling over all records (LEAK-30) is one constant per column and carries nothing of a test row.

**2. Target**

- The quantity is the right one: loss cost per unit of insured value, the pure-premium rate I act on (USE-5). I would want a number, an expected loss cost, and I would turn it into a relativity and then a tier.
- The scale is not checkable, and it is not a plain ratio. 58% of the 1,188 losses are above 1 (median 1.27, 90th percentile 8.0). A fire loss almost never exceeds the insured value, so the host at least rescaled the ratio, and it may have capped or compressed it too. I can rank with these predictions but not price with them. The definition's "fire loss as a ratio to its total insured value, transformed" is accurate. The gap could be named more sharply: values above 1 show the scale is not a loss ratio.

**3. Unit and test data (USE-10)**

- One row is one policy term, which is my unit of decision. One reservation: 6.4% of rows are exact copies, `var15` included, and in every copy group with a loss another copy has none. That fits several locations or buildings of one account in the same term better than copies of one policy. So a row may be a location within a policy rather than the policy itself. This is unresolved, and not a reason to drop the copies: each copy is its own exposure with its own outcome.
- What I face is next year's book: mostly renewals with their history, plus new business. The random split mixes years, so trend, rate changes and mix shift are never tested, and a test term can have a later term of its own risk in training. Only about one test row in six (16.9% expected under 3 random folds) has a same-risk row in training. Since that row is almost always lossless, it gives the model little to exploit. Whole risks held out score 0.232 against 0.260 at random, inside the fold spread (0.015-0.066).
- The task text says "a test policy's risk is often in training in another term, as when a renewal is priced". That overstates both points: it is one test row in six, not "often", and a renewal sees only earlier terms. Suggested wording: "about one test row in six has another term of its risk in training, earlier or later; a renewal sees only the earlier ones". `ForcedIIDFromTemporal` is the right tag.

**4. Would I use it?**

- As a tiering and referral score, yes, if it beats what I already have. `var13`, which reads like the grade I already use, scores 0.215-0.255 alone. A regularised LightGBM scores 0.253-0.270, higher on every fold, but the lift is only 0.015-0.04 of Gini.
- What would make me distrust it:
  - About 400 losses per test fold, so fold standard deviations of 0.04. Model differences of 0.01-0.02 are noise.
  - The 2014 leaderboard shake-up (thread 10194: public-board leaders fell on the private board).
  - The undisclosed transform.
- What would make me trust it:
  - A test on a later year.
  - Monotone lift by decile.
  - Lift over my current premium, not over a constant.

**5. Metric: scores the decision: yes**

- The declared metric is the normalized weighted Gini with weight `var11`. That is the competition's metric (MET-4), and Liberty defended it from the business side: after the forum found the weighted version is not maximised by the true order, Kaggle reported that Liberty "decided that the metric makes sense from a client/business perspective" (thread 9819).
- It scores the decision I make, a ranking of the book weighted by size (MET-1). It is the exposure-weighted Lorenz-curve Gini that actuaries use to compare risk scores (Frees, Meyers and Cummings 2011). The unit is the policy, weighted by the square root of its insured value: large risks count more, but less than in proportion to size.
- No threshold or k is fixed by the source, and tiers cut the whole ranking, so a hard-label or top-k metric would invent a decision (MET-6, MET-7). AUPRC does not come up (MET-9).
- MET-8 would prefer a proper scoring rule, here a weighted Tweedie or Poisson deviance on the dollar scale. That needs the disclosed transform and strictly positive predictions, and the dataset has neither.
- What it misses:
  - The price level. A model off by a constant factor scores the same, and pricing sets the level separately.
  - The ideal base. With the premium as base (Frees's ordered Lorenz curve, as `wisconsin_local_government_property_insurance_fund` would use), the Gini would measure lift over my current rates. Here no premium ships, so it measures lift over a constant.
- The metric I would choose is the declared one. MET-2 holds: `var11` ships, and every test fold has 369-410 losses.

**Gaps between the dataset and the real decision, ranked by how much they change the task**

1. Undisclosed target transform: values above 1 for 58% of losses (USE-5). Scores can rank but not price, and the transform decides which losses the Lorenz curve accumulates.
2. No policy year: random policies stand in for next year's book, and later terms of the same risk can be in training (USE-8, USE-10). The measured effect is small: 0.232 grouped by risk against 0.260 random, within the spread.
3. No current premium or manual rate. The model cannot be judged against my existing rating plan, which is how I would actually accept it.
4. Unit unclear: the identical copies suggest some rows are locations or buildings of one account in one term.
5. No account loss history and no term length. These matter little for fire.
6. Anonymised features: their timing cannot be checked. Weather is shown static across terms, so the remaining doubt is small.

**What an expert would change (recommendations; the curator decides)**

- Keep `var11` as a feature and as the weight (builder's issue 1, USE-6). Add the evidence to the `var11` bullet: its square is a whole-dollar amount in 93.9% of rows, with a floor of exactly $250,000 and common values of $250k, $500k and $1M.
- Add to the prediction-point bullet that 96.9% of re-appearing risks keep one weather vector across terms, so weather is the location's climate and known at underwriting.
- Name in the target bullet and in `fit_reason` that 58% of losses exceed 1, so the scale is not a loss ratio.
- Reword the split sentence of `task_summary` and `splits_comment`: about one test row in six, earlier or later terms, a renewal sees only earlier ones.
- Sharpen the `use_case` decision to fit USE-1 while staying with the source: "ranks the policy by expected fire loss per insured value to set its underwriting tier and price and to target loss control (the competition: identify each policyholder's risk exposure and tailor the coverage)". Add a line to `row` that some rows may be locations of one account.
- No change to the metric. If a later release held the premium, the ordered-Lorenz Gini with the premium as base would be the better original.

**Sources**

- The competition pages in the run folder (Description, Evaluation, data-description). Forum threads 9706 (`-var13`), 9819 (Liberty keeps NWG "from a client/business perspective"), 9880 (corrected code), 10026, 10101, 10194 (solutions; `var11` "much better to use it as feature").
- The builder's probes (run folder): the var15 key, the grouped checks, the risk key check, var13, the var11 experiment, the exploration and the copies.
- My checks: scripts in the run folder (terms, var11, shares).
- Frees, Meyers and Cummings 2011, JASA 106:1085-1098, DOI 10.1198/jasa.2011.tm10506 (abstract): https://academicnewsletter.sufe.edu.cn/info/445125. The cplm `gini` documentation: https://rdrr.io/cran/cplm/man/gini.html
- NYC Data Science Academy case study (Poisson objective; CV Gini 0.35 against private 0.25-0.30): https://nycdatascience.com/blog/student-works/property-casualty-loss-cost-data-type-case-study
- Moody's property underwriting (COPE and peril loss costs at quote and renewal): https://www.moodys.com/web/en/us/solutions/underwriting/property-underwriting.html
- CAS RPM 2011, Walling (underwriting scores and tiers, loss control survey inputs): https://casact.org/sites/default/files/presentation/rpm_2011_handouts_cl5-walling.pdf
- CAS RPM 2015 handouts on this competition: search snippets only, the PDFs redirected to the CAS homepage.
- Rate basis per $100 of insured value: hyperexponential property pricing factors, https://www.hyperexponential.com/lob-pricing-factors/property
- Rules: USE-1, USE-3, USE-5, USE-6, USE-8, USE-9, USE-10; MET-1, MET-2, MET-4, MET-6, MET-7, MET-8, MET-9.

</details>

<details><summary>Blind review</summary>

**Dataset:** Liberty Mutual Fire Peril Loss Cost (Kaggle 2014), target `transformed_loss_ratio`, scored as regression, IID 3-fold. I looked at the 300,000-row sample in the clean room.

**Verdict: exclude as prepared.** As a squared-error regression task the target has no learnable signal: no model I tried beats predicting the mean (R² between -0.004 and +0.0004). The data are real and the ranking signal is genuine (weighted Gini about 0.28, AUC for "any loss" about 0.69). So the dataset could come back as "include with changes" if it is reframed, either as binary classification of loss vs no loss, or scored with the competition's own weighted Gini.

**What the task is.** An insurer (Liberty Mutual) estimates expected fire loss cost per policy (loss divided by total insured value) when it underwrites or renews a policy. The estimate is used for pricing and risk selection. This is a real and common actuarial use. The data are real policy records released by the sponsor and anonymised (normalised var1-17, crimeVar1-9, geodemVar1-37, weatherVar1-236). Secondary sources describe the target as "a transformed ratio of loss to total insured value" and say the organisers scored with "the weighted Gini coefficient, where the weights are given by the var11 variable" (synthesized.io data card). The NYC Data Science post reports "only 0.26% positive response" and 1,188 positive rows in the full training set.

**Concerns, most serious first**

1. **The target is unfit for RMSE/R² scoring (fatal as prepared).**
   - 99.734% of rows are exactly 0: 798 positives out of 300,000. The positives range from 0.006 to 25.9, with median 1.27.
   - 50 rows (0.017% of the data) carry 50% of the total sum of squares, and the top 100 rows carry 73%. Each 100k test fold has 244-294 positives, and its RMSE is driven by about 15-20 large losses.
   - LightGBM 3-fold CV on the same split scheme:

     | Model | R² per fold |
     |---|---|
     | L2 objective | -0.0014 / -0.0037 / -0.0017 |
     | Tweedie objective | -0.0004 / -0.0004 / -0.0003 |
     | Heavily regularised L2 | +0.0003 / +0.0003 / +0.0002 |
     | Heavily regularised Tweedie | +0.0003 / +0.0004 / +0.0002 |
     | Huber | -0.0003 (all folds) |

     In every case RMSE is equal to the mean baseline to the fourth decimal.
   - The same models rank risk well:
     - Normalised var11-weighted Gini of the Tweedie model: 0.21 / 0.27 / 0.35 (mean 0.28). The L2 model averages 0.26.
     - A binary loss/no-loss LightGBM reaches AUC 0.70 / 0.66 / 0.69, with log loss 0.0179 against a base rate of 0.0184.
     - These figures match the public record. NYC Data Science reports private-leaderboard Gini of about 0.25-0.30, and the winners were in a similar range.
   - The signal is real but squared error cannot see it. A regression benchmark would rank methods on noise and on how closely they shrink toward the mean.
   - **Change:** drop the regression framing. Either reframe as binary `transformed_loss_ratio > 0` (about 1,200 positives in the full 452k rows, AUC about 0.69), or keep the continuous target only if the benchmark can score it with Tweedie deviance or the original weighted normalised Gini.

2. **Too few positives for stable scores, made worse by subsampling.**
   - The 300k sample keeps 798 of the roughly 1,200 positives.
   - Fold-to-fold Gini varies from 0.21 to 0.35 within one model. That spread is far larger than typical gaps between methods.
   - **Change:** use all 452,061 rows, stratify the folds on the positive indicator, and use more repeats (for example 3x3 or 5x2).

3. **The original weighting is dropped.**
   - The competition weighted rows by var11. Its common values are square roots of round amounts: 500 = sqrt(250,000), 547.7 = sqrt(300,000), 632.5 = sqrt(400,000), 707.1 = sqrt(500,000). That looks like sqrt of an insured-value or exposure amount.
   - Unweighted scoring changes the task: the positive rate rises from 0.18% in the lowest var11 decile to 0.54% in the highest.
   - **Change:** keep var11 as a feature (it was a feature in the original data too). If the continuous target is kept, document that the original metric was weighted, or use var11 as the sample weight.

4. **Repeated entities and exact duplicates (minor).**
   - 14,590 rows (4.9%) fall into 6,185 groups with identical feature vectors, up to 27 copies per group. These include continuous fields such as var10, var11 and var13.
   - Only 26 positives fall in these groups, and only 1 group has more than one positive. So the duplicates do not leak the target. They are probably several buildings or coverages at one site.
   - Location blocks are shared across folds:
     - weather vectors: 23,325 unique (about 12.9 rows each, largest block 1,239)
     - geodem vectors: 2,536 unique
     - crime vectors: 326 unique
   - Sharing locations across folds is realistic for territorial pricing, so a random split is acceptable.
   - **Change:** none required. Optionally deduplicate exact repeats or note them.

5. **The deployment is temporal, but the split is random.**
   - In practice the model prices next year's policies, and there is no policy-year column. As far as I recall, the Kaggle page says the train and test sets were split randomly, so IID matches the original setup. Row order shows no drift: the positive rate per index decile stays between 0.23% and 0.30%.
   - I cannot tell whether the "weather station" variables cover the period before the policy or the policy period itself. If they cover the policy period, they would not be known at pricing time.
   - **Change:** none possible with this data. State the caveat.

6. **Preparation details.**
   - `var4_group` is a curator-derived column. It equals the first character of `var4` in 100% of non-missing rows, so it is redundant. It still ranks second in LightGBM gain (4.4%). Drop it or document it.
   - `var1`, `var3`, `var7`, `var8` are ordinal integer codes stored as categoricals, so their order is lost. Consider storing them as numeric.
   - `id` and `dummy` were dropped. That is correct: `dummy` is described in the competition material as a nuisance variable "not a predictor".
   - `weatherVar115` is absent with no explanation. Document why.
   - The "Z" missing codes appear correctly converted to NaN. Missingness: var2 99%, var6 94%, var5 92%, var3 87%, var16 80%, var12 79%, var1 75%, var14 64%, crime block about 24%, weather 0.4-7%, geodem 0.5%.
   - There is heavy collinearity in the weather block (34 pairs with |r| > 0.99), which is harmless for trees.
   - Values look plausible: var17 lies in 0-100, var15 in 1-440, the target is non-negative, and nothing looks synthetic.

**What I could not check**
- **The official Kaggle data and evaluation pages.** They render in JavaScript and returned only the page title, the Kaggle API needs authentication, and the archive is blocked. So the following rest on secondary sources (synthesized.io, the NYC Data Science blog, search snippets of a DataRobot/CAS deck) and on my recollection of the competition page:
  - the column dictionary
  - the "Z = missing" coding
  - var11 being the weight
  - the statement that the split was random
  - the transformation applied to the target
- The 152,061 rows not in the sample.
- Why weatherVar115 was removed.
- Whether rows are policy-years, and whether weather variables are contemporaneous with the policy.
- I did not open any file outside the clean room.

</details>

<details><summary>Precedent check</summary>

**Precedent check (precedent-checker, 2026-11-01): liberty_mutual_fire_peril_loss_cost**

**Verdict.** I checked 14 decisions. Nine follow their precedents and one departs with a fact that sets it apart (the exact copies). Four depart without a reason that holds against the closest case, in rank order:
1. The split is IID, not grouped by risk (P4, SPLIT-8). The builder's reason, that renewals are priced on the insurer's own book, was equally true of Allstate's households, and those are grouped. The other reason, no measured shortcut, sets Liberty apart from frempl, not from Allstate or nba / open_university.
2. Shipping a forced split at all (P4). Andrej sent how_much_did_it_rain to `No` on 2026-10-30. The fact australian relies on (no unit shared across the split) does not hold here: 22% to 48% of rows are terms of a risk that recurs.
3. `var11` is both a feature and the metric's weight (P6, MET-2, a Must). This departs from the rule's text and from the AI's suggested call of 2026-10-30 in this record. The facts that set Liberty apart are real, but a Must takes no exception, so this is an amendment.
4. The target ships on the published scale (P7 CLEAN-16, with MET-3). The stated reason ("the transform is not disclosed, so we do not log it again") is contradicted by the data and by the builder's own probe, and the family's log1p question (australian issue 5) does not list this table.

`var4_group` (CLEAN-19) has a supporting fact the notes do not cite. The only curator decision on this dataset so far is the `Yes` (Andrej, 2026-10-30), given on a record that read "Regime IID, as the competition split". Everything below checks the builder's draft, not a curator call.

What the evidence is: the run's register (1,620 decisions). Its 14 flags touch none of the rules used here, apart from LEAK-30's drift, which was settled on the keep side from 2026-10-19. The CLEAN-19 amendment flag concerns per-entity histories kept as rows, which is not this reason. I also read the sibling definitions and the REVIEW.md files of this run (australian_vehicle_insurance_2004_2005, frempl_french_motor_personal_line), the records of how_much_did_it_rain and the insurance siblings, the triage summary's "Policy calls of 2026-10-30", and the Cases tables of splits.md, leak_checks.md and metrics.md. Two checks of my own (no model) are in the run folder:
* after_loss_change: risk keys that also let one policy variable vary, and whether a variable changes after a loss;
* target_scale: the skew of the losses.

**Per decision**

| # | Decision (rule) | Standing | Closest precedents | What sets it apart, or not |
|---|---|---|---|---|
| 1 | Random policies, not grouped by risk (SPLIT-8, SPLIT-24, SPLIT-4) | departs; the stated reason does not set it apart from Allstate or nba / open_university | SPLIT-8 as written (Must; Lennart, 2026-10-12, amended 2026-10-21): "grouped by the entity when the periods are stacked and the entities recur across them". nba_players_2016_2019 and open_university (grouped, R^2 0.745 against 0.744 on the valid window; Lennart, 2026-10-21). Same run, AI drafts: allstate_claim_prediction_challenge_1m (by household; 53% of the test households recur in new data; "the grouping stands for the time order"), frempl (by policy chain, an exact but partial key, SPLIT-9 measured), pricing_game_2017_french_mtpl (by client), spanish_motor_insurance_coverage_level_2022_2024 (by policy). The key: the composite-key pattern in splits.md (concrete_compressive_strength, 2026-10-14: "rows identical in every column but one are one entity at another age"); barred: maternal_health_risk (a feature-vector hash standing in for an unknown entity) | For: losses rarely recur (6 of 1,188 share a risk). My check found no frempl-type counter: no policy variable changes more often after a loss than after none (var11 0.585 against 0.623, var13 0.305 against 0.379, all others at most 0.019). That sets it apart from frempl (SPLIT-9). Against: the renewal argument (SPLIT-4) asks whether risks are new. SPLIT-8's grouped branch stands for the time order (a random split trains on a test term's later terms), as Allstate's note says, and Allstate's households recur in new data too. The gap-based reasons (0.232 against 0.260) are barred by SPLIT-4 and SPLIT-30. The key is buildable under the composite-key pattern: `var15` steps by exactly 1 in 36,708 pairs. It is wider than written: with `var11` also free (it changes between 62% of consecutive terms, like a revalued sum insured), 214,816 rows (47.5%) fall in risk groups, not 22.3%. Prompt 1. |
| 2 | A forced split at all, `ForcedIIDFromTemporal` (SPLIT-8) | open family question; Liberty is weaker than australian on the fact that matters | how_much_did_it_rain CC (Andrej, 2026-10-30): `No`, "forced IID would introduce leaks for this task"; in chat: "Forced IID is to be avoided at all costs" (SPLIT-8 left unchanged). australian issue 1 and frempl issue 5 (same run, open) ask the same question. SPLIT-8 cases (account_debt_south_africa, mobile_churn and the churn snapshots; Lennart, 2026-10-12 and 2026-10-21) | australian's fact against how_much is that every row is a distinct policy and no outcome is shared across the split. That does not hold here: 22.3-47.5% of rows are terms of a recurring risk, and 2.1% of test rows have an exact copy in train. What does hold: the outcome is barely shared (the next term's loss rate is 0.81-0.95% after a loss against 0.27-0.28% after none, on 105-248 consecutive-term pairs with a loss, so 1-2 repeat losses), and the host split randomly ("The train and test sets are split randomly"). Prompt 2. |
| 3 | The tag `ForcedIIDFromTemporal` itself (SPLIT-8) | consistent | the tagged competition releases without dates: home_credit_default_risk and santander_transaction_value (Kaggle), expresso_churn_prediction_1m (Zindi); australian (same run) | porto_seguro (Kaggle insurance, anonymised, no dates, fit "direct") and allstate_claims_severity carry no regime tag. Those two contradict SPLIT-8 as written: flag them; do not follow them. |
| 4 | Exact copies kept: 28,965 rows, 6.4%, 49 groups that hold both a loss and a zero (LEAK-18, LEAK-19, LEAK-20) | departs from LEAK-18's default, with a fact that sets it apart | hiva_agnostic and qsar_tid_11 (Lennart, 2026-10-21: distinct units the features cannot tell apart stay, reason in the notes; "IF the copies dont make any sense from a task use case, we should drop them"); frempl (same run: 45 copies over 20 columns *with dates* dropped as artefacts, while 49 profiles with another amount are kept); allstate_claim_prediction_challenge_1m (70% natural repeats kept); australian (378 kept); mortgage (LEAK-20 exception, Lennart, 2026-10-22, another reason) | The labels disagree in 47 of the 49 groups with a loss. A record copied twice would carry its label twice, so these are distinct policies (terms of one risk). The release also has no dates, while frempl's dropped copies matched on their dates. This falls within LEAK-19's "distinct units" wording and LEAK-20's "genuine label ambiguity", so no exception is needed. If it is recorded as a LEAK-20 exception, it is the second, for another reason than mortgage's, so no amendment is due. Note: grouping by risk (decision 1) would put every copy group on one side. |
| 5 | `var11` both a feature and the metric's weight (MET-2, USE-6) | not reasonable under the ranking as written; an amendment is the way | MET-2 (Must): "every input it needs ships as a column and is never a feature (a group, a time, a weight ...)". This record's Assessment (AI, 2026-10-30): "`var11`: the competition's weight, so a scoring column and not a feature". g_research_crypto_forecasting_1m (`Weight` a scoring column, not a feature, 2026-10-21). frempl issue 4 and australian issues 2 and 4 (open): an exposure weight "never a feature"; australian measured that the time as a feature games the weighted Gini (0.238, above every honest model). For the builder: the family reasoning of 2026-10-30, "A sum insured is a feature too, the size of the risk" (wisconsin coverage, nfip coverage); the bundle check `task_metric_input_is_model_input` ("which is allowed") and four definitions whose metric inputs reach the models (sepsis_prediction_1m, numerai_v5_2_1m, micro_mass, sat11_hand_algo_runtime: group, order or time columns, not weights) | The facts are real and set it apart from australian's exposure. The host lists `var11` among the "policy characteristics" and ships it in the test file. Teams used it as an input (thread 10194: "much better to use it as feature rather than as weight"; another team divided predictions by log1p(`var11`)). As a feature it shows no gain (-0.002), so nothing is gamed, unlike australian's 0.238. It does not change more often after a loss (0.585 against 0.623, my check). But P3 over P6 overrides MET-2 only if meeting MET-2 breaks USE-6, and MET-2's own remedy keeps both Musts: `var11` stays a feature and the metric becomes a stand-in (the unweighted Gini), at the cost of MET-4, a Should. Keeping both the feature and the weighted metric makes a Must yield to a Should, so it needs MET-2 amended. definitions.md line 222 ("never a feature") and line 235 ("allowed") already disagree. Prompt 3. |
| 6 | Metric `Metric.source("normalized_weighted_gini")` (MET-4, MET-12, MET-13) | consistent | MET-4 cases (zillow_prize, g_research_crypto_forecasting_1m, rossmann_store_sales; Lennart, 2026-10-21); allstate_claim_prediction_challenge_1m (`normalized_gini`, source, same run); the 2026-10-30 suggestion table ("weighted normalized Gini (source)") | It is the exposure-weighted Gini on a rate target that frempl issue 4 recommends for the family; here the source already chose it. |
| 7 | Exposure: none beyond the ratio target | consistent | the AI's call of 2026-10-30, made per dataset at Andrej's request: "A target that is already a ratio to the insured value (Liberty Mutual) holds its exposure" | none |
| 8 | Zeros as published; `task_target_value_dominant` proposed for acceptance | consistent | Andrej's answer 2 (2026-10-30: "We don't care ... independent if it is zero inflated or not"); the accepted warnings of australian and frempl (same run) | Liberty's zeros are policies without a fire loss; the acceptance line is not yet in `dataset.py`. |
| 9 | Target on the published scale, no `target_transform` (CLEAN-16, MET-3) | departs; the stated reason is contradicted by the data | log1p with `target_transform="log1p"`, scored on the amount: allstate_claim_prediction_challenge_1m (also an undisclosed adjustment, "in no currency"), frempl, spanish_motor_insurance_coverage_level_2022_2024, spanish_motor_insurance_2015_2018, wisconsin_local_government_property_insurance_fund (all AI, this run). Raw, with a measured reason: pricing_game_2017_french_mtpl. Open: australian issue 5 ("decided once for the insurance tables scored by the Gini", seven tables named, Liberty not among them). MET-3 (Lennart, 2026-10-21: "ship the target on the modelling scale, score on the original scale") | The losses are log-normal-like on the published scale: skew 1.90 on that scale against -0.16 on the log scale, median 1.27, maximum 25.9. So the host's transform did not log them. The builder's own probe (shipped-folds models) has log1p better on 3 of 3 shipped folds: 0.2536 / 0.2862 / 0.2750 against 0.2533 / 0.2620 / 0.2699. A competitor listed "transform target variable into log scale" among the steps that "consistently gave me better results" (thread 10194). The Gini is the same under either scale; only what models fit changes. Prompt 4. |
| 10 | Drop `id`, `dummy`, `weatherVar115`; `Z` made missing (CLEAN-3, CLEAN-5, CLEAN-10) | consistent | `Row_ID` dropped (allstate_claim_prediction_challenge_1m), the index dropped (porto_seguro); a column that recodes another (CLEAN-5); "?" made missing (allstate_claim_prediction_challenge_1m), -1 made missing (porto_seguro) | The source's documented codes and statements (data page, threads 10026 and 10101). |
| 11 | `var4_group` added, the letter of `var4` (CLEAN-19) | departs, no CLEAN-19 bullet named (P7, minor) | allstate_claim_prediction_challenge_1m `household_vehicles` (reason written: CLEAN-3, the identifier processed into its meaning, as `client_n_vehicles` in pricing_game_2017_french_mtpl); porto_seguro ("we do not copy these" engineered features) | A fact exists but is not cited. The data page calls the letter the higher level, and two competitors split `var4` that way (thread 10194: "I split var4 into two values"; "transformed var4 to binary dummies but ignored the numbering after the letter"). A top team's GLMM used `var4` as a random effect instead (thread 10187). Prompt 5. |
| 12 | Host normalisation kept, `Potential leak, kept on purpose:` (LEAK-30) | consistent | LEAK-30 tension row (Lennart, 2026-10-19); allstate_claim_prediction_challenge_1m (same run, same note) | none |
| 13 | `var13` kept as a dominant feature (TP-4, LEAK-38) | consistent | TP-4 baselines in frempl (the record's length alone) and australian (the observed time alone); homesite_quote_conversion (LEAK-38, anonymised field kept) | A model beats `var13` on 3 of 3 shipped folds. The note reads it as an underwriting grade, not a possible post-outcome field, so a plain `Note:` fits; homesite's label was for a suspected status code. |
| 14 | `Spatial` tag | minor reading | definitions.md: "geographic information (ZIP, latitude and longitude, region, store location)"; pricing_game_2016/2017 (region codes, tagged); porto_seguro (`ps_reg_*`, untagged) | Liberty holds attributes of the location (crime, geodemographics, weather), not a location field. Either reading is defensible; it changes no score. |

**Drift and amendments**

* **Andrej on SPLIT-8.** On one day (2026-10-30) Andrej said `Yes` to Liberty, australian and frempl on records that read "Random (IID)", sent how_much_did_it_rain to `No` for forced IID, and said forced IID is to be avoided "at all costs". This is not drift over time. The forced framing of the three insurance tables appeared only at /add-dataset. Lennart's SPLIT-8 cases (2026-10-12, 2026-10-21) shipped forced IID, so the two curators read SPLIT-8 differently (already noted in how_much_did_it_rain's record).
* **Third case.** Three tables of this run ask the same SPLIT-8 question against how_much_did_it_rain: australian (issue 1), frempl (issue 5) and Liberty. If all three ship against the "at all costs" stance, they are three departures for one reason. Propose australian's option (d), an amendment of SPLIT-8, rather than three exceptions.
* **MET-2 against the house docs.** The bundle check and definitions.md line 235 allow a metric input that is also a feature; MET-2 and definitions.md line 222 do not. Four shipped definitions already rely on the allowance (for group and time columns). Liberty would be the first weight. Settling decision 5 settles this text.
* **Target scale.** Liberty should be named in australian issue 5, so that one call covers all eight tables scored by a Gini.

**Facts for the split auditor and the claim auditor** (my check)

* The "Terms of one risk" table and `splits_comment` give 22.3% of rows and 36,708 consecutive-term pairs. That is a lower bound. With `var11` also free, 214,816 rows (47.5%) are in risk groups, with 92,029 pairs where `var15` steps by 1. With `var11` and `var13` free, the figures are 289,039 rows (63.9%) and 126,031 pairs.
* No policy variable changes more often after a loss than after no loss. The next term has a loss at 0.81-0.95% after a loss, against 0.27-0.28% otherwise, on 105-248 pairs: about 1-2 repeat losses.

**Reflection prompts**

1. **Consistency check (AI, 2026-11-01):** the draft splits random policies (`ForcedIIDFromTemporal`) though about a quarter to a half of its rows are consecutive terms of the same risk. That differs from allstate_claim_prediction_challenge_1m (same run: grouped by household, "the grouping stands for the time order", though 53% of households recur in new data) and from nba_players_2016_2019 / open_university (Lennart, 2026-10-21: stacked periods grouped by entity at no measured cost), which follow SPLIT-8's grouped branch. What sets Liberty apart?
   (a) No id: the entity is rebuilt from equal values in every other column. SPLIT-24 bars a feature-vector hash standing in for an unknown entity (maternal_health_risk), and outcomes do not travel between terms (1-2 repeat losses; no variable moves after a loss). Recorded as the reason IID is the closest regime.
   (b) Treat it like Allstate: group on risks equal in every column but `var15` (and `var11`), `ForcedGroupedFromTemporal`, a key justified by the composite-key pattern (concrete_compressive_strength). Exact copies then stay on one side.
   (c) Reopen Allstate, nba and open_university to IID where no shortcut is measured.
   (d) Amend SPLIT-8 ("grouped only where an id or an exact entity key exists, or a shortcut is measured").
2. **Consistency check (AI, 2026-11-01):** the draft ships a forced split. That differs from how_much_did_it_rain (`No`, 2026-10-30, you: "forced IID would introduce leaks for this task"; "Forced IID is to be avoided at all costs"). australian's distinguishing fact (no shared unit) does not hold here. What sets Liberty apart?
   (a) The host itself split at random and scored on that split. Units recur across the split, but their outcomes barely do (1-2 repeat losses), unlike storm-correlated gauge hours. Recorded as the fact.
   (b) Treat it like how_much_did_it_rain: `No`.
   (c) Reopen how_much_did_it_rain to SPLIT-8 as written.
   (d) Amend SPLIT-8, decided together with australian issue 1 and frempl issue 5.
3. **Consistency check (AI, 2026-11-01):** the draft keeps `var11` as a feature and as the metric's weight. That differs from MET-2 ("never a feature"), from this record's suggested call (AI, 2026-10-30: a scoring column) and from g_research_crypto_forecasting_1m (`Weight` a scoring column). What sets Liberty apart?
   (a) The host lists `var11` among the policy characteristics and gave it to every team as an input. Teams used it as a feature (thread 10194), and it shows no gain (-0.002). MET-2 is a Must, so this can only be recorded through (d).
   (b) Treat it like g_research: `ScoringColumn("var11", role="weight")`, not a feature (measured cost about 0).
   (c) Keep it a feature and declare the unweighted normalized Gini as a stand-in (MET-2's remedy; it drops the source's metric).
   (d) Amend MET-2: "a weight the source ships to its participants as a feature stays a feature", and align definitions.md lines 222 and 235.
4. **Consistency check (AI, 2026-11-01):** the draft ships the target on the published scale ("the transform is not disclosed, so we do not log it again"). That differs from allstate_claim_prediction_challenge_1m (also an undisclosed adjustment, shipped log1p) and four other Gini-scored siblings of this run. The losses are log-normal on the published scale (skew 1.90, -0.16 logged), and log1p scored higher on 3 of 3 shipped folds. What sets Liberty apart?
   (a) The competition scored this scale and the host already transformed it, with a light tail (the top 1% of losses hold 5.9% of the sum). Recorded in the notes.
   (b) Treat it like Allstate: `log1p_transformed_loss_ratio` with `target_transform="log1p"`.
   (c) Reopen the log1p siblings to their published scale.
   (d) Decide it once for the family in australian issue 5, with Liberty named.
5. **Consistency check (AI, 2026-11-01):** the draft adds `var4_group` without naming the CLEAN-19 bullet it meets. That differs from allstate_claim_prediction_challenge_1m's `household_vehicles`, whose reason is written down. What sets it apart?
   (a) The data page documents the letter as the higher level of a hierarchical code, and competitors split `var4` that way (thread 10194). Cite both in the bullet.
   (b) Drop it and leave `var4` as published (P7 minimal).
   (c) No precedent to reopen.
   (d) No amendment needed.

**Builder's draft issues against precedent**

1. `var11` feature and weight: departs from a Must; an amendment, not an exception (decision 5).
2. Terms of one risk, kept IID: departs from SPLIT-8's grouped branch and from Allstate. The key covers up to 47.5% of rows, not 22.3% (decisions 1 and 2).
3. Exact copies: consistent with hiva_agnostic and qsar_tid_11 on the label-disagreement fact; no exception needed (decision 4).
4. `var13`: consistent (decision 13).

</details>

<details><summary>Advocate</summary>

**Advocate, opening brief (2026-11-01): liberty_mutual_fire_peril_loss_cost**

**Position: ship as defined, after note changes.** No evidence agent found a validity failure. The open items are one
regime question for the curator (forced IID), one Must-against-Must call (`var11`), and note fixes. Each has a remedy
that keeps the dataset.

```text
Verdict: ship after note changes.
Validity: USE-1 holds (approximate fit, USE-5); LEAK-10/LEAK-38 hold, now measured; SPLIT-8 met as IID, tag
  ForcedIIDFromTemporal, the leak the curator feared measured absent (EV-1); LEAK-19/20 copies kept.
Value: TP-4 holds (model beats var13 on 3/3 folds); MET-4 source metric, MET-13 verified; noisy folds (EV-8).
Quality: CLEAN-3/5/10 hold; CLEAN-16 reason refuted (log1p is an available, cheap fix); CLEAN-19 needs its citation.
For the curator: forced IID against how_much_did_it_rain (point 1); var11 feature and weight (point 4).
```

**1. Forced IID: Liberty is not how_much_did_it_rain, on the two facts the curator's `No` rested on (P4; SPLIT-8
Must, SPLIT-19 Should, EV-1).**
* *The claim.* The curator rejected how_much_did_it_rain because "forced IID would introduce leaks for this task".
  Here the leak has been tested and is absent:
  * paired test on the training side (split auditor, 9 folds): taking a test risk's other terms out of training costs
    -0.045, taking as many random rows costs -0.060. Seeing the same risk adds nothing beyond the row count. The claim
    auditor's run on the shipped folds agrees (B minus C between -0.038 and +0.057, no sign);
  * a risk's training loss ranks its test terms at AUC 0.504-0.525 on every key. Only 6-14 of 1,188 losses share a
    risk with another loss;
  * no policy variable changes more often after a loss (precedent checker; claim auditor #7, #8). The newest term
    shows no reporting deficit (0.261% vs 0.292%, p 0.47; LEAK-24);
  * removing the later terms of test risks from training (the SPLIT-9 worry) moves the score by -0.027/+0.007/-0.014,
    which is fold noise.
* *The second fact.* how_much's host refused to split at random ("We can not randomly sample days from both years ...
  because the weather on consecutive days tends to be highly correlated") and tested on a later year. Liberty's host
  split at random ("The train and test sets are split randomly") and scored that split. So our split is the source's
  split (SPLIT-19), not one we forced onto a task whose source refused it. The tag only states honestly that the
  application is temporal (USE-10).
* *The curator's own call.* The `Yes` of 2026-10-30 was given on a record that reads "Regime IID, as the competition
  split". "At all costs" was said in chat on the same day; SPLIT-8 was left unchanged, and 17 datasets of the working
  copy ship under it. The curator decides (Precedence: who decides). My case is that the fact the stance targets, a
  leak from the split, has been measured here and does not exist.
* *Why it outranks the objection.* Facts first (EV-1): a measured null on the decisive experiment beats an analogy to a
  dataset whose leak was never bounded. If the curator still wants a rule, the right instrument is one SPLIT-8
  amendment decided with australian issue 1 and frempl issue 5 (precedent checker, prompt 2 (d)), not a `No` by
  analogy.
* *Concession.* If the curator makes "no forced split, ever" the rule, Liberty fails it, and so would the grouped
  alternative (`ForcedGroupedFromTemporal` is forced too). I do not dispute the tag: the use case is temporal.

**2. The prediction point holds and is now measured, not assumed (P4; LEAK-10 Must, LEAK-38 Should, USE-6).**
* The weather block belongs to the location, not to the term: it changes in 1.0% of 107,547 one-year steps (column
  auditor). The claim auditor gets 94.6% unchanged on 126,063 pairs, the practitioner 96.9%. Crime and geodem vectors
  never change between terms.
* `var13` does not move at a loss term: it changes in 23.1% of loss terms against 28.3% of zero terms (fewer, not
  more), and it falls in 9.9% against 12.0%, so there is no claims-free reset.
* No missingness encodes the outcome: predicted against observed missing counts among losses match for 10 fields (for
  example var9 201/201 and var1 995/995). The var4 excess (p 0.018, about 0.18 across ten tests) is a "maybe" under EV-6.
* `id` carries no time order (Spearman with var15 -0.006). LEAK-30: the normaliser is a fixed constant from another
  population (177 of 213 columns lie more than 10 SE from 1), which is the reading LEAK-30 allows. That is weaker than
  the note's own "test half included".
* *Remedy:* three note edits turn the builder's "cannot verify" items into measured passes. No column changes.

**3. A real task, scored by the source's metric, which the blind reviewer's "exclude" does not touch (P3 USE-1;
P6 MET-4, MET-1, MET-13).**
* Actor, moment and decision: a commercial property underwriter ranks policies by fire loss cost per insured value at
  quote or renewal to set tier, schedule credits and loss-control referrals (practitioner). The fit is approximate only
  because the transform is undisclosed (USE-5), and the definition says so.
* The metric is the competition's normalized weighted Gini, which Liberty defended "from a client/business perspective"
  (thread 9819). It is the exposure-weighted Lorenz Gini actuaries use (Frees, Meyers and Cummings 2011). The
  implementation reproduces the host's test case (-0.821428571428572) and gives the exact tie average.
* The blind reviewer's verdict ("exclude as prepared") is aimed at RMSE/R² scoring, which the definition never
  declares. Its own fallback ("scored with the competition's own weighted Gini") is what ships, and its own numbers
  confirm the signal (Gini about 0.28, AUC 0.69). This is not a conflict: the objection is answered by the existing
  definition.

**4. `var11` as both feature and weight: either remedy keeps the dataset (P3 USE-6 Must against P6 MET-2 Must).**
* Facts: `var11` is the square root of a whole-dollar insured value (93.9% of rows; floor 250,000; median 884,000). It
  rises by a median 1.8% per term and does not move differently at a loss term (54.7% vs 50.8%). The host lists it
  among the "policy characteristics" and ships it in test.csv. Teams used it as an input (thread 10194). On a weighted
  Lorenz curve a row's slope is its y, so the feature cannot game the weight. The measured effect is -0.002 (-0.058 to
  +0.037), unlike australian's 0.238.
* Rule: P3 outranks P6. Removing an input known at the prediction point changes the task to "price without the sum
  insured" (USE-6). The precedent checker answers that MET-2's own remedy, an unweighted stand-in metric, meets both
  Musts. That remedy drops a deliberate source metric that the domain expert would choose (MET-4). So the cleanest
  record is the amendment of prompt 3 (d): "a weight the source ships to its participants as a policy characteristic
  stays a feature". It also settles the contradiction between definitions.md lines 222 and 235.
* *Fallback, also shipping:* `ScoringColumn("var11", role="weight")`, which costs about nothing (-0.002). The curator
  picks; neither choice blocks shipping.

**5. Worth benchmarking: a real, hard ranking signal on 452k rows, every fold scorable (P6; TP-4, MET-2, TP-2).**
* There are 369-410 losses per test fold. A constant scores 0.0000 and the oracle 1.0000 on each fold. `var11` is never
  missing.
* The regularised LightGBM beats the strongest single feature (`var13`) on 3 of 3 folds, by 0.018, 0.047 and 0.011.
  The winner reached 0.332 on the private board, so there is headroom.
* *Concession (EV-8):* fold sd is about 0.04 with one repeat of three folds. *Remedy:* 3 repeats if the protocol allows
  an override (about 30 s per GBM fold); otherwise state the noise in the notes. A noisy metric is a note, not a
  rejection: P4 over P6 (forest_fires, "the split follows what the task does in reality").

**6. The data is faithful, and the copies are kept for the right reason (P5; P4 LEAK-19, LEAK-20).**
* All counts reproduce: 452,061 rows (50.1% of the id range), 99.74% zeros, 1,188 losses from 0.006 to 25.9. `dummy`
  recodes `var9` (123,185 vs 0), and `weatherVar115` is 0 wherever present.
* The copies: 47 of the 49 loss groups also hold a zero, so these are distinct units the features cannot separate
  (hiva_agnostic, qsar_tid_11). LEAK-20's label-ambiguity clause applies without an exception. They put 4.8-4.9% of
  test rows next to a train copy, and they carry no label (the precedent checker finds this decision consistent).
* *Remedy for the refuted reason:* split bullet 10 into the 11,433 copies with `var15` missing (terms) and the 5,548
  that share a `var15` (perhaps locations of one account, as the practitioner reads them). Correct the 2.1% to 4.8-4.9%.

**7. What was refuted is note text, fixed at the lowest rung of the remedy ladder (P7; writing; Principles step 5).**
* The repetition numbers: give the wide-key shares (47.5-65.6% of rows; 39-55% of test rows with their risk in
  train), say the narrow-key hold-out was partial, and use the paired result as the reason for IID instead of the gap
  (SPLIT-4).
* Reword the LEAK-30 mechanism (point 2). Bring the var13 range up to date (0.215-0.259). Add the tie clause to the
  README metric. Complete `changes` (weatherVar115, var4_group). Cite CLEAN-19 for var4_group (data page: the letter is
  the higher level; thread 10194).
* *Target scale (CLEAN-16, MET-3): concede.* The stated reason is contradicted (skew 1.90 on the published scale,
  -0.16 logged; log1p better on 3/3 shipped folds). The mild fix is `target_transform="log1p"`, scored on the
  published scale, so the metric and the task stay the same. Or decide it once with australian issue 5, Liberty named.
  This is a P7 quality item: it changes what models fit, not what is scored.

*Independent failures are not conflicts:* I do not claim any of points 2-7 rescues point 1. Point 1 stands on its own
evidence: the measured absence of the leak, and the source's own random split.

</details>

<details><summary>Critic</summary>

**Critic, opening brief (2026-11-01): liberty_mutual_fire_peril_loss_cost**

**Verdict: do not ship as defined.** It can ship after two changes: a split that does not train on a test risk's later terms, and an explicit ruling on `var11` under MET-2. The rest is note repair. The real task is not in doubt: Liberty Mutual's own underwriting decision, its own policies, and the host's metric. What is in doubt is whether the split matches the stance the curator took the day he accepted the record, and whether a Must is being broken without saying so.

**1. Forced IID on stacked terms of recurring risks, against the curator's stance and SPLIT-8's grouped branch (P4; SPLIT-8, Must; SPLIT-24, Must).**
- *Problem.* The task is temporal: price next term's book. The release has no dates. The definition picks the IID branch of SPLIT-8 (`ForcedIIDFromTemporal`), but the data has stacked terms of the same risks. About 65% of rows share a risk with another row (wide key, claim auditor #20). 53.5-55.5% of each shipped test fold has its risk on the training side (claim auditor #4). SPLIT-8 assigns that case to "grouped by the entity when the periods are stacked and the entities recur across them".
- *The curator's stance.* On 2026-10-30 Andrej sent how_much_did_it_rain to `No`: "if the data is temporal but a temporal spliot is not possible, we cannot split the data and reject it". In chat: "Forced IID is to be avoided at all costs" (how_much_did_it_rain.md lines 62-68). He said `Yes` to this record the same day, but the record then read "Regime IID, as the competition split". The forced framing first appeared at /add-dataset, so his `Yes` did not rule on it (precedent checker, drift section). australian's distinguishing fact, no unit shared across the split, does not hold here (precedent checker #2).
- *Effect on the real task.* The scores come from a test set that mixes terms of risks the model has already seen, earlier and later. The use case scores next term only.
- *What the advocate will cite, and why it is not enough.* The risk carries almost no label: AUC 0.51-0.52, and the paired drop shows no gain (split auditor; claim auditor #22). That is a measured small leak. The curator's stance does not depend on the size of the leak, though, and SPLIT-4 bars deciding a split on the size of the gap. Allstate in the same run is grouped by household on the same renewal argument (precedent checker #1).
- *Remedy (mildest that works).* Re-split as `ForcedGroupedFromTemporal` on the exact narrow key: rows equal in every column but `var15`, with `var15` stepping by 1. That is the composite-key pattern of concrete_compressive_strength, which SPLIT-24 allows. State in the notes that the key is partial, and that wider keys merge sparse rows by chance (groups of up to 375 rows, split auditor). Expected cost is about 0.03 Gini, within fold noise (split auditor). If the curator holds that no forced split ships, then the verdict is `No` with the how_much_did_it_rain reason, and australian issue 1 and frempl issue 5 get the same call. Either way it should be decided once, as a SPLIT-8 amendment (precedent checker prompt 2d), not as a third silent exception.

**2. Training holds later terms of test risks (P4; SPLIT-9, Must).**
- *Problem.* 6.2-6.3% of test rows have a later term of their risk in training, and 5.3-5.4% have only later terms there (narrow key, split auditor problem 1). Those rows carry outcomes from after the test row's prediction point. The order is known here (`var15` steps by 1 within a risk), so this is not just the unavoidable blindness of a dateless release.
- *Effect.* The model is trained on the future of the policy it prices. The measured shift is fold noise (-0.027 / +0.007 / -0.014), but SPLIT-9 is a Must about what may be in training, not about the size of the effect.
- *Remedy.* Point 1's grouped split removes the problem. If IID is kept, use the as-of filter on the narrow key (drop the later terms of each test risk from that fold's training side, as alfa_battle_2_0_task_2 did), and give the numbers in `splits_comment`.

**3. The split facts the curator would decide on are misstated (P4 basis; SPLIT-8, SPLIT-29; EV-2).**
- *Problem.* `splits_comment`, `task_summary.split` and decision 5 give 22.3% of rows and "only 6 of the 1,188 losses". These are lower bounds from the narrow key. On keys that let `var11` and `var13` vary as they do between terms, the figures are 47.5-65.6% of rows and 14 losses (claim auditor #20, split auditor, precedent checker). The "whole risks" check at 0.232 held out only about a third of the repeats (claim auditor #21). The builder's "2.1% of test rows with an exact copy in train" is 4.8-4.9% (claim auditor #17, split auditor problem 5). "They are terms of one risk" does not explain 5,548 of the 16,981 extra copies, which share a `var15` value (claim auditor #16). The domain practitioner reads such copies as several locations of one account. That leaves the row's unit open.
- *Effect.* A call on point 1 made from these notes would rest on the smaller numbers.
- *Remedy.* Rewrite with the range of keys, the AUC 0.51 lookup, the paired result, the later-term shares and 4.8-4.9%. Split the reason for the copies into its two kinds, and add a line to `row` that a row may be a location of one account.

**4. `var11` is both the metric's weight and a feature, against a Must (P6; MET-2, Must).**
- *Problem.* MET-2: every metric input "ships as a column and is never a feature (a group, a time, a weight ...)". The definition keeps `var11` as a feature. The record's own Assessment (AI, 2026-10-30) reads "a scoring column and not a feature (MET-2)", and the curator's CC line does not overrule it.
- *Why the USE-6 override does not hold as written.* P3 outranks P6 only where meeting MET-2 breaks USE-6. MET-2's own remedy keeps both Musts: `var11` stays a feature and the metric becomes the unweighted Gini as a stand-in, at the cost of MET-4, a Should (precedent checker #5). The draft lets a Must yield to a Should. definitions.md lines 222 and 235 already disagree with each other.
- *What I concede.* The facts favour the draft. `var11` is the square root of a round sum insured with a $250,000 floor (domain practitioner). The host lists it among the policy characteristics and ships it in test.csv. As a feature it moves the score by only -0.002. A weighted Gini cannot be gamed through its weight, because the best order is by E[y|x] (claim auditor #13).
- *Remedy.* No change to the data. The curator rules explicitly: either amend MET-2 ("a weight the source ships to participants as a policy characteristic stays a feature", and align definitions.md), or declare the stand-in. Liberty would be the first weight under that allowance, so it should not ship on a silent departure.

**5. The "potential leak" note names a mechanism the data rules out (P4 note; LEAK-30, Should).**
- *Problem.* The note says the host's normalisation divided by a mean "over all its records, test half included". If so, the train half's column means would sit within a few standard errors of 1. Only 9 of the 213 columns in the band do, and 177 sit more than 10 SE away (claim auditor #14). The constant came from another population.
- *Effect.* A reader is warned of a test-row statistic that is not there.
- *Remedy.* Reword as normalisation by an undisclosed outside constant, no test-row statistic, and drop the "Potential leak" label.

**6. The target ships raw for a reason the data contradicts (P7; CLEAN-16, Should; MET-3).**
- *Problem.* "The transform is not disclosed, so we do not log it again" assumes the host logged the losses. The losses are skewed on the published scale and symmetric once logged: skew 1.90 against -0.16 (precedent checker #9). The builder's own probe has log1p ahead on 3 of 3 shipped folds (0.2536 / 0.2862 / 0.2750 against 0.2533 / 0.2620 / 0.2699). allstate_claim_prediction_challenge_1m, also an undisclosed adjustment, ships log1p.
- *Effect.* Quality only. The Gini is scored on the original scale either way. This is not a reason to exclude.
- *Remedy.* `log1p_transformed_loss_ratio` with `target_transform="log1p"`. Or, if the curator prefers, name Liberty in australian issue 5 and decide it once for the eight Gini-scored tables.

**7. Coarse resolution and stale text (P6/P7; EV-8, TP-4, MET-13, writing).**
- *Resolution.* About 400 losses per test fold and one repeat of 3 folds give a fold sd of 0.036-0.046 (split auditor problem 4). The builder's default LightGBM scored 0.18-0.20 on the shipped folds and 0.23-0.33 on other random assignments (claim auditor). Typical method gaps are inside that noise. *Remedy:* 3 repeats if the protocol allows; otherwise a note.
- *Stale numbers.* The `var13` range in the notes predates the tie handling now in `metrics.py` (now 0.215-0.259, claim auditor #18). The README's metric definition lacks the tie clause (#25). *Remedy:* re-run `dataset check`.
- *Incomplete text.* `task_summary.changes` omits `weatherVar115` and `var4_group` (#5). The `var4_group` bullet does not cite the data page's hierarchy or thread 10194 (precedent checker #11). `fit_reason` should say that 58% of losses exceed 1, so the scale is not a loss ratio (domain practitioner). The `task_target_value_dominant` acceptance is not yet in `dataset.py`. *Remedy:* edit the text.

**Dropped.** The blind reviewer's "exclude as prepared" rests on RMSE/R² scoring. The declared metric is the host's weighted Gini, so that point does not apply to this definition. The weather-timing doubt has been resolved in the dataset's favour: the weather vector stays fixed across terms in 94.6-96.9% of cases.

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate, rebuttal (2026-11-01): liberty_mutual_fire_peril_loss_cost**

The critic and I agree on the task, the metric, and points 3 and 5-7. We disagree on the split (points 1 and 2). One
new fact decides much of that disagreement: the grouped split the critic proposes leaves most of the overlap in place.

**New fact (check run for this rebuttal).** I assigned whole narrow-key risks (rows equal in every column but `var15`)
to 3 random folds and counted, on each test fold, the rows whose risk on the wider keys still has a term in training.
Script and output: in the run folder (not committed).

| split | narrow key: risk in train | var11 free: risk in train / a later term in train | var11 and var13 free: risk in train / a later term in train |
|---|---|---|---|
| shipped IID folds | 16.7-16.9% | 39.1-39.2% / 18.1-18.2% | 53.5-53.7% / 24.8-25.0% |
| grouped on the narrow key | 0% | 26.4-26.8% / 12.7-12.8% | 42.8-43.3% / 19.7-19.9% |

The wide keys are not exact: sparse rows merge by chance (split auditor). Even so, 80-84% of their steps are exactly 1,
so most of what they hold are terms.

**1. Forced IID against SPLIT-8's grouped branch and the curator's stance: contest, with a narrowed fallback.**
* *The curator's stance.* The critic's remedy does not meet it. "If the data is temporal but a temporal split is not
  possible, we cannot split the data and reject it" applies to `ForcedGroupedFromTemporal` as much as to forced IID.
  The critic says so too ("If the curator holds that no forced split ships, then the verdict is `No`"). So the stance
  decides between shipping and `No`. It does not decide between IID and grouped. On shipping against `No`, my point 1
  stands. The reason the curator gave for how_much was the leak ("forced IID would introduce leaks"). Here that leak was
  measured and is absent (EV-1). The source split at random (SPLIT-19), while how_much's source refused to. The critic
  calls the leak "small"; the measurements show none. The paired drop beats the random drop by +0.015 (6 of 9 folds),
  and the risk's training loss gives AUC 0.504-0.525. SPLIT-4 bars choosing a split on a score gap, and I do not:
  these are tests of whether information crosses the split, not gaps.
* *SPLIT-8's text.* I concede that "stacked periods, recurring entities" points to grouped. Three facts weigh against
  following it here:
  * The new fact above: the exact key the critic proposes removes only a fifth of the overlap on the widest key (53.6%
    to 43.0%) and of the later terms (25% to 20%). The re-split would cost about 0.03 Gini and still not deliver "no
    test risk in training". A wider key would cut more, but SPLIT-24 bars it (chance merges, groups of up to 375 rows).
  * The distinction from Allstate is the key. Allstate grouped on a household id the source published, so its entity is
    exact. Liberty has no id, and its entity can only be rebuilt from feature equality, which SPLIT-24 bars beyond the
    exact composite key (maternal_health_risk).
  * The use case is mostly renewal pricing, a warm-start task (USE-10). A grouped split tests a cold start. The tension
    row "Temporal against grouped" says one regime, the one the use case implies.
* *What follows.* IID stays my recommendation. If the curator reads SPLIT-8 literally, narrow-key
  `ForcedGroupedFromTemporal` is an acceptable fallback that keeps the dataset. Its notes must then say it removes
  about a fifth of the overlap, not all of it. I agree with the critic that it should be decided once, as the SPLIT-8
  amendment with australian and frempl (prompt 2 (d)).

**2. Later terms in training (SPLIT-9): narrow.**
* SPLIT-9 is a Must, and a later term's label is unknown at the test row's prediction point, so the rule is triggered.
  I concede that.
* The rule's own test is "check that the filter removes the shortcut". The tension row (SPLIT-9 against SPLIT-14,
  alfa_battle_2_0_task_2, lending_club) says SPLIT-9 is met by removing the *measurable* shortcut, and the diffuse rest
  falls under SPLIT-10 (Should). Here no shortcut is measurable. Removing the later terms moves the score by
  -0.027/+0.007/-0.014. The risk's training loss ranks its test terms at AUC 0.50-0.52. No variable changes after a
  loss.
* Neither remedy removes the later terms anyway. With the narrow-key as-of filter, or the critic's grouped split, 12.7%
  (`var11` free) to 19.7% (`var11` and `var13` free) of test rows still have a later term in training (new fact above).
  A filter that leaves four fifths of what it targets is not a remedy that "resolves the problem" (Principles step 5).
* *What follows.* State the later-term shares and the null effect in `splits_comment`. The narrow-key as-of filter is
  cheap and harmless if the curator wants it on principle, but its notes must call it partial.

**3. Misstated split facts: concede.** The rewrite should use the critic's list plus the table above. Add the `row` line
that a row may be a location of one account.

**4. `var11`: concede the procedure, keep the substance.** I agree it cannot ship on a silent departure. My opening
already asked for an explicit ruling, with the amendment (prompt 3 (d)) preferred and the ScoringColumn as the fallback
(cost -0.002). The critic and I name the same two options, and the facts the critic concedes favour the amendment.
Neither option blocks shipping.

**5. LEAK-30 note: concede.** Reword it as normalisation by an undisclosed outside constant and drop the "Potential leak"
label. This matches my point 2.

**6. Target scale: concede.** Use `target_transform="log1p"`, or decide it with australian issue 5. This is quality only;
the critic agrees it is no reason to exclude.

**7. Resolution and stale text: concede.** Add repeats if the protocol allows, otherwise a note. Re-run `dataset
check`, and make the text edits as listed. Add the `task_target_value_dominant` acceptance.

**Where the panel stands.** The one real dispute is the regime. The curator's stance decides between shipping and `No`.
The split choice (IID or narrow-key grouped) is a weighing call between SPLIT-8's text and USE-10 plus SPLIT-24. That
call matters less than either brief implied: the grouped split cuts the overlap only from 54% to 43%.

</details>

<details><summary>Critic rebuttal</summary>

**Critic, rebuttal (2026-11-01): liberty_mutual_fire_peril_loss_cost**

**Where I stand now.** I concede advocate points 2, 3, 5 and 6, and point 7 except for one scale detail. I narrow point 1: the split is a call for the curator, and I no longer claim the grouped split satisfies his stance. I dispute two things. First, the later terms in training: SPLIT-9 is a Must, and a new check shows the fix is cheap. Second, the advocate's fallback on `var11` contradicts its own argument. Updated verdict: ship after (a) the curator's explicit SPLIT-8 ruling, (b) the as-of filter if IID stays, (c) an explicit MET-2 ruling, and (d) the note repairs both briefs list.

**Advocate 1 (forced IID is not how_much_did_it_rain): narrowed. I concede two facts and dispute one inference.**
- *Conceded: the host's split.* The host split at random and scored that split. how_much's host refused to: thread 14245, "We can not randomly sample days from both years ... because the weather on consecutive days tends to be highly correlated", quoted in how_much_did_it_rain.md line 37. I verified the quote. This sets the case apart from the one the curator rejected.
- *Conceded: the grouped remedy does not meet the stance.* `ForcedGroupedFromTemporal` is forced too. The how_much CC reads "if the data is temporal but a temporal spliot is not possible, we cannot split the data and reject it", which covers grouping as well. My point 1 remedy therefore does not satisfy the curator's stance. It stays only as SPLIT-8's grouped branch, an option and not a demand. The split auditor's case against grouping holds: the key is partial, wider keys merge rows by chance (SPLIT-24), and renewals are priced on known risks (SPLIT-4).
- *Disputed: that the stance targets only a measured leak.* The chat line, "Forced IID is to be avoided at all costs", sets no condition on the size of a leak. The CC's general clause does not either. The record's `Yes` was given on "Regime IID, as the competition split", before the forced framing existed. So the measured null is the right fact to put before the curator, but it does not answer his stance for him.
- *Disputed: SPLIT-19 as a reason that wins.* The host's split is a Should. SPLIT-5 (Must) says a prescribed split "is a claim to check against the task design, not a fact". The advocate itself tags the task temporal.
- *Common ground.* One SPLIT-8 ruling, decided together with australian issue 1 and frempl issue 5 (precedent checker, prompt 2d). Liberty should not ship before that ruling.

**Advocate 1, fourth bullet (later terms are fold noise): disputed (P4; SPLIT-9, Must). New check.**
- *What SPLIT-9 says.* "A training row whose label is not yet known at the prediction point must not be in train." The rule asks that the filter remove the shortcut. It does not say that rows from after the prediction point may stay as long as no shortcut is measured. Here the order is known within a risk, because `var15` steps by 1, so this is not the unavoidable blindness of a dateless release.
- *Which run the advocate cites.* The -0.027 / +0.007 / -0.014 come from variant c on the widest key (split auditor, `paired_key2.txt`). That key merges rows by chance.
- *New check.* A script in the run folder counts what the as-of filter would drop on the exact narrow key: the training rows that are later terms of a test risk. It drops 10,202-10,316 of 301,374 training rows per fold (3.4%), with 24-34 of 778-819 training losses. On the wider keys it would drop 11.1% and 15.6%.
- *Remedy.* If IID stays, apply the narrow-key as-of filter (the alfa_battle_2_0_task_2 pattern) and note it. The cost is small, and a Must is met that the draft now breaks.

**Advocate 2 (prediction point measured): conceded.** This matches the "Dropped" note of my brief and my point 5. The note edits are the remedy.

**Advocate 3 (real task, the source's metric, the blind reviewer's exclude does not apply): conceded.** I dropped the blind reviewer's point for the same reason.

**Advocate 4 (`var11`): narrowed to the remedy. I dispute the advocate's fallback.**
- *Common ground.* The facts favour keeping `var11` as a feature, and an amendment is the clean instrument (precedent checker, prompt 3d).
- *Disputed: "P3 outranks P6" as the ground.* That ranking decides only real conflicts. MET-2's stand-in meets both Musts, so as written there is no conflict, only a Must against a Should (MET-4). That is why it takes an amendment and not an override.
- *Disputed: the fallback.* The advocate's fallback, `ScoringColumn("var11", role="weight")`, takes `var11` out of the features. By the advocate's own USE-6 argument, that changes the task to "price without the sum insured". So it is not a shipping option on the advocate's reasoning. Only two choices fit the rules: the MET-2 amendment, or the unweighted stand-in.
- *Remedy.* The curator rules on the amendment before shipping. No change to the data.

**Advocate 5 (worth benchmarking): conceded.** Every fold is scorable, and the task beats TP-4. The noise is a note, plus 3 repeats if the protocol allows. Same as my point 7.

**Advocate 6 (faithful data, copies kept): conceded.** LEAK-19 and LEAK-20 apply without an exception. The remedy is the reason split in two and 4.8-4.9% in place of 2.1%, as in my point 3.

**Advocate 7 (note repairs; log1p conceded): conceded, with one correction.**
- The advocate writes that log1p is "scored on the published scale, so the metric and the task stay the same". That is right under MET-3, with `target_transform="log1p"`. The new column name should follow CLEAN-16 (`log1p_transformed_loss_ratio`).
- The other repairs match my points 3, 5 and 7.

**Files.** The as-of count: a script in the run folder (not committed).

</details>
