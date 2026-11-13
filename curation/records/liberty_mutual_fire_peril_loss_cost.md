---
unique_name: liberty_mutual_fire_peril_loss_cost
name: 'Liberty Mutual Group: Fire Peril Loss Cost (Kaggle 2014)'
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 3
tags:
- Two-Regime Zeros
- Larger IID Data
- 'Samples: Over Time'
- 'Time: Lost'
- 'Target: Later'
- 'Entities: Recur'
original_source: Kaggle
year: '2014'
domain: insurance
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/liberty-mutual-fire-peril
- https://nycdatascience.com/blog/student-works/property-casualty-loss-cost-data-type-case-study
v2_path: datasets/_dev/tabarena-v0pt2/liberty_mutual_fire_peril_loss_cost/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 2: Liberty Mutual's commercial fire losses with a scored
leaderboard and 452,061 labelled policies, but the target is an undisclosed transform of the loss ratio and holds 1,188
positives.
- Source: Liberty Mutual's Kaggle competition (2014, deadline 2 September 2014). Description: "your task is to predict
  the target, a transformed ratio of loss to total insured value"; "This will enable more accurate identification of
  each policyholder's risk exposure and the ability to tailor the insurance coverage for their specific operation." As
  published: `train.csv`, 452,061 policies x 300 normalized, anonymised features in four blocks (policy, crime,
  geodemographic, weather) plus `dummy`, with `var11` the scoring weight; the test half was never labelled publicly.
- Use case: Liberty Mutual underwriting a business policy's fire cover ("tailor the insurance coverage"); fit
  approximate, the transform of the target is undisclosed (USE-5). Regime IID, as the competition split ("The train and
  test sets are split randomly", data page, quoted by the earlier triage).
- Siblings and duplicates: none in the log (grep for Liberty Mutual and fire peril); OpenML: none by name; external
  collections: none found.
- Papers and pages: the Kaggle description and Evaluation pages; threads 9880 (the corrected metric code), 10026 (ids
  randomised), 10101 (`dummy` recodes `var9`), 10187 and 10194 (leaderboard shake-up, solutions); no write-up of the
  winning model from the host.
- Metric: normalized weighted Gini, Kaggle Evaluation: "Submissions are evaluated on the normalized, weighted Gini
  coefficient. The weights used in the calculation are represented by var11 in the dataset." Deliberate (MET-4); inputs
  `var11`, which ships but is also a feature (MET-2: a weight is a scoring column, never a feature). A custom metric for
  the library (MET-12, MET-13), with the host's test case in thread 9880 (-0.821428571428572).
- Earlier AI triage, 2026-10-20, measured: 99.74% zeros, 1,188 positives (0.006 to 25.9); untuned LightGBM, 3-fold: AUC
  0.70 for a loss, normalized weighted Gini 0.27 (the winner 0.332 on the private board), R^2 0.16 on log1p among
  positives; loss rate flat over id deciles.
- Risks for /add-dataset: `var11` as weight and feature (MET-2); about 400 positives per test fold; drop `id` and
  `dummy`; whether the 2,588 distinct geodemographic vectors (locations) call for a grouped check (SPLIT-30). Family
  question: none applies directly (no exposure column, no negative values).
- Priority: gap 0, use case 0 (fit approximate), source + (the host's pages), shape + (452,061 policies, 300 features),
  risk - (an undisclosed target transform, few positives).

**Assessment (AI, 2026-10-30):** suggested call for policy question 3 of the zero-inflated review, where Andrej asked
for a call per dataset from its references and the domain's practice instead of one convention for the family (the
shared reasoning: a time exposure or a sum insured is a feature, and a rating-cell table weights the metric by its
exposure; negative amounts that are recoveries become 0; the source's metric first, else the normalized Gini as a
context metric, since RMSE on raw amounts follows a few large claims and a Tweedie or Poisson deviance needs positive
predictions; MET-10 as amended on 2026-11-02 (Andrej) later declined a family-wide metric, so each table's metric is
decided on its own); the curator
has the call.
- Target: as published, a transformed ratio of loss to total insured value; the exposure is inside the target.
- `var11`: the competition's weight, so a scoring column and not a feature (MET-2).
- Negative amounts: none.
- Metric: the normalized weighted Gini with `var11` (MET-4), a custom metric (MET-13) checked against the host's test
  case (thread 9880).
- Drop `id` and `dummy`.

CC (2026-10-30, Andrej): `Yes`, priority 4 (the AI screening had `TBD -> 2nd Tier`, priority 2; zero-inflated screening
review page).

Liberty Mutual's Kaggle competition on commercial fire losses: 452,061 labelled policies (the test half was
never labelled publicly) with 300 normalized, anonymised features in four blocks (17 policy, 9 crime, 37
geodemographic, 236 weather variables) plus `dummy`, a declared "nuisance variable" that recodes `var9`. The target is
"the transformed ratio of loss to total insured value" (data page; the transform is not disclosed), and `var11` is the
weight of the competition's normalized weighted Gini. Measured on the downloaded `train.csv` (2026-10-20): 99.74%
exact zeros, 1,188 positives (0.006 to 25.9), no negatives or missing targets. The blocks are coarse (2,588 distinct
geodemographic vectors, 327 crime vectors) and full of near copies (KazAnova's post in thread 10194).

Split random, as in the competition ("The train and test sets are split randomly"). A 2014 thread suspected a leak in
`id`; Kaggle had randomised the ids (Will Cukierski, thread 10026), and the loss rate is flat over id deciles (0.25-0.28%).
Drop `id` and `dummy`. Untuned LightGBM, 3-fold stratified random CV: AUC 0.70 for a loss, normalized weighted Gini
0.27 (0.20-0.31 by fold; the winner scored 0.332 on the private board), R^2 0.16 on log1p among the ~400 test positives
per fold. The signal is real, but everything the target holds sits in 1,188 positives under an unknown transform, so
the regression is close to rare-event ranking and the 2014 leaderboard reshuffled strongly (thread 10187: "With only
1188 non-zero training examples (<0.3%), overfitting seems inevitable"). Hence 2nd tier. Terms: Kaggle competition
rules. To check: classification of any loss versus weighted regression with `var11`, and whether the geodemographic
vectors (locations) call for a grouped split.

**Assessment (AI, 2026-11-01):** added as `datasets/_dev/tabarena-v0pt2/liberty_mutual_fire_peril_loss_cost/` by /add-dataset with the full review panel; the open questions are in its Review. Recommend shipping after the panel's changes and the unweighted Gini of issue 2 (not yet made); only issue 1, the forced random split (open against how_much_did_it_rain, with five siblings), could turn it to `No`. Changes after the panel: the target ships as `log1p_transformed_loss_ratio`, scored on the published scale (log1p ahead on 2 of 3 folds, 0.313 against 0.298), and the notes give the measured checks of timing, repeated risks and copies. The definition departs from three readings of the 2026-10-30 Assessment and the text below the CC: "Regime IID, as the competition split" is now tagged `ForcedIIDFromTemporal` (issue 1); `var11`, "a scoring column and not a feature", stays a feature and the metric's weight, which MET-2 bars as written (issue 2); the target "as published" ships as log1p. `required_split` Random (IID) matches the definition. Priority 3: gap + (insurance thin), use case 0 (fit approximate, transform undisclosed), source + (the insurer's own data and metric), shape + (452,061 policies, 299 features), risk - (split and metric open; 1,188 losses).

CC (2026-11-02, Andrej): the forced IID split ships (issue 1 (a)): "Forced group splits should be fine. Regarding forced IID, did you make sure there are no leaks? Whenever there are no leaks we can ship." Recorded in SPLIT-8 (amended 2026-11-02: a forced grouped split ships; a forced IID split ships only when the leak test across the random split finds none).

**Assessment (AI, 2026-11-02):** the leak test across the random split finds none: rows share a risk across the split (17-54% of each test fold, by how loosely a risk is matched) but not its outcome: a risk's loss in training ranks its test terms at AUC 0.50-0.52 (0.5 is chance), only 6 to 14 of the 1,188 losses share a risk with another loss, and taking a test risk's other terms out of training costs no more than dropping as many random rows (on all 6 pairs of fold and key). The host split at random itself. how_much_did_it_rain's `No` named a measured leak; none is found here.

CC (2026-11-02, Andrej): `var11` is the metric's weight and stays a feature (issue 2 (a)): "I want to score with the feature and also keep it as a feature assuming it to be known during train and test time as input for the model." The competition's weighted normalized Gini with `var11` as weight, and `var11` a feature; recorded in MET-2 (amended 2026-11-02: a weight known at the prediction point for train and test rows alike stays a feature and is also the metric's weight). All issues of the REVIEW are now resolved.

CC (2026-11-02, Andrej): ship, with `var11` a feature and the weight of the competition's normalized Gini (issue 2 (a), MET-2 amended).

CC (2026-11-06, Lennart): `var11` stays a feature and a copy, `var11_weight`, ships as the scoring column the weighted Gini reads (MET-2 as reworded on 2026-11-05; asked in PR #47's review); no training weight, since the weight is a function of the features (MET-15). Issue 3 of the record's Review.

CC (2026-11-08, Lennart): the declared metric (`normalized_weighted_gini`) is checked, as declared; the record ships, with no open issue on the PR #47 review board.

**Assessment (AI, 2026-11-08):** ships by default (no open issue on the PR #47 board), but the definition's changes of 2026-11-06 (the `var11_weight` scoring column the metric reads and the exposure paragraph) have not passed `dataset check`, and the re-review panel under LEAK-41 and MET-14 to MET-16 has not run: both wait for the competition files, which download only after the Kaggle competition rules are accepted. No container is built before both pass.

**Assessment (AI, 2026-11-08):** review panel (focused: claim auditor, column auditor, mediator; re-review under LEAK-41, MET-14 to MET-16, after the raw data arrived): ship after changes (two sentences in the notes, made: the `var11` bullet gives its shipped-fold gains, +0.0004 with an L2 fit and +0.0032 with the fit weighted by `var11`, the score of 1/`var11` alone, 0.071, and that `var11` changes no more often going into a loss term, a planned amount under LEAK-41; the target bullet says no term length is recorded, so the target stays per contract under MET-14); disputed: none; for the curator: issue 4 (the type of `var1`, `var3`, `var7`, `var8`: unordered as shipped, ordered by code, or numbers; the Kaggle data page settles it). This supersedes the earlier Assessment of 2026-11-08: the competition's files are in the warehouse, `dataset check` passes on them (0 errors, 0 warnings) and the re-review panel has run.

CC (2026-11-08, Lennart): issue 4, A (as implemented): `var1`, `var3`, `var7` and `var8` ship as unordered categories; the comment that called them ordinal is reworded.

CC (2026-11-09, Andrej): the training labels' maturity is stated in the notes (cross-dataset item of 2026-11-09, option B).

## Review

**Outcome:** added. The AI recommends shipping it: the focused re-review of 2026-11-08 under the exposure rules, run
once the raw data arrived, finds no leak in `var11` or any other column and changed two sentences of the notes, now
made; one question on the type of four anonymised codes is open (issue 4) and does not decide whether it ships.
Liberty Mutual's Kaggle competition of 2014 on commercial fire losses: 452,061 labelled policies with 299 anonymised
features (policy, crime, geodemographic and weather blocks); the target is the host's undisclosed transform of the loss
over the total insured value (0 for 99.74%, 1,188 losses), shipped as log1p and scored on the published scale by the
competition's normalized Gini weighted by `var11`, which the metric reads from its copy `var11_weight` (a scoring
column) while `var11` stays a feature; no training weight; random 3-fold split tagged as forced from temporal.
Validity: USE-1 holds, fit approximate (USE-5: the transform is undisclosed, and 58% of the losses exceed 1, so the
scale is not a plain loss ratio); LEAK-41 holds: `var11` is a planned amount, the square root of a round sum insured
set at underwriting and indexed by a median 1-2% a term, and it changes no more often going into a loss term (63.7%
against 62.4% of the steps, Fisher p 0.70); no column records a term length, a date or an earned amount, and `var17` is
no share of a year, so no feature encodes a realized term or a cut; LEAK-10 and LEAK-38 hold and are measured (the
weather block stays the same across a risk's terms, so it is the location's climate; `var13` does not move at a loss);
LEAK-24 holds as tested; LEAK-30 finds no leak (the host's normalising constant comes from outside these records);
SPLIT-8 is met, the split shipped on your call of 2026-11-02 (a forced IID split ships when the leak test across the
random split finds none; SPLIT-8 amended); SPLIT-9 holds: a test policy's later terms sit in training, but they carry
nothing of its outcome (the new leak test across the forced split agrees, with low power: a lookup of the training
target of the 4.8-4.9% of test rows with an exact copy in training gains +0.0011, SE 0.0011); LEAK-19 and LEAK-20: the
exact copies stay. Value: TP-4 holds (a regularised LightGBM scores 0.306-0.320 against 0.221-0.260 for `var13` alone,
the strongest single feature, on every fold); the task probe flags `no_signal` and `unstable`, which read an R²-type
skill on the log1p target; on the declared weighted Gini its LightGBM beats the constant on 3 of 3 splits by +0.233
(SE 0.006) (EV-3); MET-4, the host's metric, equals the host's formula to 7e-12 (MET-13); MET-2 holds as amended on
your call of 2026-11-02 and reworded on 2026-11-05: `var11` is a feature and its copy `var11_weight` the metric's weight
(issues 2 and 3, resolved); `var11` as a feature gains +0.0004 (L2 fit) and +0.0032 (fit weighted by `var11`) on the
shipped folds, and 1/`var11` alone scores 0.071 (0.038 to 0.119), through risk selection (USE-6); MET-15 holds: no
training weight, since the metric weight is a function of the features, and a fit weighted by `var11` scores 0.0053
lower (worse on 2 of 3 folds); MET-16 does not apply (no survey or design weight); MET-14: the target stays per
contract, since no term length is recorded and no feature carries a cut, now stated in the notes. Quality: the target
ships as log1p (CLEAN-16), like the log1p siblings, settled for the family in australian issue 5 (2026-11-02: the log1p
tables keep log1p); CLEAN-19 cited for `var4_group`; CLEAN-14: the type of `var1`, `var3`, `var7`, `var8` is open
(issue 4). Weighed: the insurer's own policies, losses and metric +, size +; 1,188 losses, so fold scores move by about
0.04 -, undisclosed target transform and anonymised features -. Left for the curator: issue 4.

Changes made after the review panel (AI, 2026-11-01): the target ships as `log1p_transformed_loss_ratio` with
`target_transform="log1p"`, the Gini still on the published scale (log1p scored higher on 2 of 3 shipped folds, 0.313
against 0.298 on average; follows allstate_claim_prediction_challenge_1m; australian_vehicle_insurance_2004_2005 issue 5
names this table among the log1p tables); the normalisation note no longer calls it a potential leak; the
prediction-point note gives the measured checks; the split note gives how often risks recur on three keys, how many test
rows have a later term in training, and the test showing no gain from it, instead of the score gap; the copies note
gives its two kinds and 4.8-4.9% of test rows with a copy in training; `var13`'s range, the tie clause, `changes`,
`fit_reason` and the `var4_group` citation updated; the `task_target_value_dominant` warning accepted (real zeros); a
note on fold noise. Each row's fold is assigned from its content, so the new target values moved rows between folds:
every number in this file is measured on the shipped folds of the changed definition (the first panel's reports
described the definition before the changes; the re-review's reports below describe the current one).

Changes made on 2026-11-06 (AI, under the exposure rules): the metric reads `var11_weight`, a copy of `var11` declared
as its weight scoring column (MET-2 as reworded on 2026-11-05), and `var11` stays a feature; no training weight is
declared, and the warning `task_metric_weight_without_sample_weight` is accepted because the weight is a function of the
features (MET-15). They were checked on the data once the competition's files arrived on 2026-11-08 (`dataset check`: 0
errors, 0 warnings).

Changes made after the re-review panel (AI, 2026-11-08): the `var11` bullet of the notes replaces the gain over 6
random folds with the shipped-fold numbers (+0.0004 with an L2 fit, +0.0032 with the fit weighted by `var11`, both
within the fold standard deviation of about 0.04), states 1/`var11` alone (0.071, 0.038 to 0.119) and that `var11`
changes no more often going into a loss term (LEAK-41's reporting clause); the target bullet says that the release
records no term length, so the share of terms cut short cannot be given, that no feature carries a cut, and that the
target stays per contract (MET-14). No change to the data, the split, the metric or the features.

**Main points:** Open: none. Resolved: `var1`, `var3`, `var7` and `var8` ship as unordered categories (4, 2026-11-08);
`var11` a feature and the Gini's weight, MET-2 amended (2, 2026-11-02); its copy `var11_weight` the scoring column the
metric reads (3, 2026-11-06).

**Issues for Andrej and Lennart:**

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

4. **Type `var1`, `var3`, `var7` and `var8` as unordered categories, ordered categories or numbers?**

   * **Problem:**
     - The four policy variables are anonymised codes 1 to k (k from 5 to 8, the host's missing level `Z` already made
       missing), and they ship as unordered categories because the data page lists `var1` to `var9` as categorical.
     - The comment above `CATEGORICAL` in `dataset.py` calls these four "ordinal", but neither the record nor the
       README quotes a source for that word, and no agent of the panel could read the Kaggle data page, which shows
       its text only in a browser with JavaScript.
     - If the data page calls them ordinal, the house rules type them as ordered categories or as numbers; if it does
       not, they stay unordered and the comment is reworded.
   * **Background:**
     - `var1` has the levels 1 to 5 (74.8% missing), `var3` 1 to 6 (87.4% missing), `var7` 1 to 8 (0.19% missing) and
       `var8` 1 to 6 (1.65% missing), from the column audit of 2026-11-02; the dtype probe flags all four as
       categories whose levels are numbers.
     - An unordered category tells a model nothing about the levels; an ordered category tells it their order but no
       spacing; a number gives them an order and equal steps.
     - The loss rate is not monotone in the level (`var8`: 0.33, 0.27, 0.22, 0.23, 0.20 and 0.39% from level 1 to 6),
       but an order may come only from what the source says the codes mean, never from the loss rates[^4a].
   * **Effect on the task:** small. The four are known at underwriting whatever their type, so validity does not
     depend on it; the type changes only what a model may assume about the levels (no order, an order, or an order
     with equal steps).
   * **Consistency:**
     - The house rule for an ordinal scale whose levels have no words (a rating or a quality score in numbers) is a
       number, as shipped; an ordinal scale of unknown meaning is categorical by default[^4b].
     - miami_housing's unlabelled 1 to 5 `structure_quality` was ordered by its codes on 2026-10-31 and has been a
       number since the mark of 2026-11-01, so it now points to C if the four are ordinal (the mediator read it as
       ordered by its codes, which is the earlier state)[^4c].
     - The first panel's blind reviewer (2026-11-01) suggested numbers; the column audit of 2026-11-02 kept the four
       unordered, as the data page lists them as categorical.
   * **Unknown:** what the data page says about the four (one look, logged in to Kaggle:
     https://www.kaggle.com/competitions/liberty-mutual-fire-peril/data).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Unordered categories (implemented) | the four stay categories without an order; the comment above `CATEGORICAL` is reworded to "the nine policy variables the data page lists as categorical" | the data page lists `var1` to `var9` as categorical; the default for a scale of unknown meaning; no order assumed that the source may not give | a model gets no order if the codes have one |
     | B | Ordered categories in code order | `FeatureTypes(ordinal=...)` with the levels 1 to k, lowest first | keeps an order the data page may state; no spacing assumed | rests on the word "ordinal" alone, with no words per level; the house rule types such a scale as a number |
     | C | Numbers | the codes 1 to k as numbers, `Z` missing as now | lossless (digits plus the missing code); the house rule for a scale with no words per level, as miami_housing | assumes equal steps between levels of unknown meaning; departs from the data page if it lists them only as categorical |

   * **Recommendation:** A with the comment reworded, unless the data page calls the four ordinal; then C, as the rule
     for a scale with no words per level and miami_housing give (the mediator left B or C to you, reading
     miami_housing as ordered by its codes). **Decision:** A, B or C, after a look at the data page?

   **Notes for the AI:** on A, only the comment above `CATEGORICAL` changes ("# The policy variables the data page
   lists as categorical, each with "Z" for a missing value."). On B, `_feature_types` returns
   `FeatureTypes(categorical=[var2, var4, var5, var6, var9, var4_group], ordinal={c: levels})` with each column's
   levels read from the data as the strings "1" to "k" in numeric order; the notes' bullet "These nine are
   categorical" names the four as ordered by their codes, with the data page's wording. On C, convert the four to
   float after `Z` becomes missing and take them out of `CATEGORICAL`; the same bullet says so. On B or C: `dataset
   check`, the dtype probe, a CLEAN-14 Cases row, a `CC` line in the record, the working copy's `CHANGELOG.md`.

   **Resolved (2026-11-08, Lennart):** A, as implemented: `var1`, `var3`, `var7` and `var8` ship as unordered categories; the code comment that called them ordinal is reworded.


   [^4a]: **CLEAN-14** (Should), 2026-10-31, Lennart: "we keep the ordinal from the context and logic, not from target
     information".
   [^4b]: **CLEAN-14** (Should): an ordinal scale is decided case by case, categorical by default; amended 2026-11-01,
     Lennart: a scale the source ships as numbers with no words per level "is a number, as shipped" ("if we can
     replace the numbers with a description that is obviously not continous then orderd categorical makes sense,
     otherwie in some cases the numeric version would make more sense").
   [^4c]: **CLEAN-14** Cases: miami_housing, `structure_quality` ordered by its codes (2026-10-31), then among the
     "scores and ratings with no words per level, or words only at their ends, are numbers again" (2026-11-01,
     Lennart); its `dataset.py` lists it in `SCORES`, shipped as a number.

**Review panel:** ship after changes (mediator), two sentences in the notes, now made. Tier focused, a re-review of
2026-11-08 under LEAK-41, MET-14 to MET-16, after the raw data arrived: the claim auditor, the column auditor and the
mediator; no blind review, task gamer, advocate or critic in this tier. Claims: 14; 13 hold (the leak test across the
forced split with low power, "no realized term" as far as anonymised columns can be tested), none refuted, 1 untested
in the definition and measured by the panel (1/`var11` alone, now in the notes). Blind review: none in this tier.
Agreed: `var11` is a planned amount set at underwriting, so LEAK-41 finds no leak; no feature encodes a realized term
or a cut; no training weight (MET-15); no survey or design weight (MET-16); the target stays per contract (MET-14).
Disputed: nothing; issue 4 (the type of `var1`, `var3`, `var7`, `var8`) is a fact to look up on the data page, put to
you.

<details><summary>Mediator</summary>

The mediator's issue 1 is issue 4 of this file. Its miami_housing precedent has been a number since 2026-11-01 (issue
4, Consistency).

**Mediator, liberty_mutual_fire_peril_loss_cost: focused re-review under LEAK-41, MET-14 to MET-16 (2026-11-08)**

Inputs: the change note, the claim and column audits, the probes (task, leak, probe 23; probe 22 empty), dataset.py,
README.md, REVIEW.md, the record and the rules. No experiment re-run: the two auditors measured every disputed number
independently and agree to rounding.

**Judgment record**

```text
Verdict: ship after changes (two sentences in curation_comments; no change to data, split, metric or features).
Validity: USE-1 holds (fit approximate, unchanged). LEAK-41 holds: var11 is a planned amount (set at underwriting,
  indexed about +2% a term, no more likely to fall or change going into a loss term: Fisher p 0.70); no feature
  encodes a realized term or a cut (var17 is no share of a year; var10/12/13/14/16 do not move at loss terms); its
  reporting clause is not met in the notes (change 1). LEAK-10 holds. SPLIT-8/SPLIT-9 hold (probe 23: shared-unit
  lookup +0.0011, SE 0.0011; low power, the earlier paired same-risk test agrees).
Value: TP-4 holds (LightGBM 0.306-0.320 vs var13 alone 0.221-0.260). MET-4 holds (scorer equals the host's formula to
  1e-11). MET-2 holds (var11_weight is an exact copy, not a feature). MET-15 holds: no sample weight; the rule's text
  names this dataset; a weighted fit is worse on 2 of 3 folds (-0.0053). MET-16 does not apply. MET-14: target stays
  per contract; the notes do not say so (change 2).
Quality: CLEAN-14, the type of var1/var3/var7/var8 is open (issue 1, a fact the data page settles).
Weighed: unchanged from REVIEW.md (insurer's own data and metric +, size +; 1,188 losses, fold SD about 0.04 -;
  undisclosed transform, anonymised features -).
For the curator: issue 1, the type of four anonymised codes the code comment calls ordinal.
Library, not this dataset: the log1p inverse overflow of a rank-only metric (below).
```

**Changes to make now (no decision needed)**

1. **LEAK-41** (Must, reporting clause as amended 2026-11-08). var11 is the metric's weight and its timing was the
   question, so it is the suspect column the clause covers; the notes give only an untuned gain on 6 random folds.
   In the var11 bullet, replace the gain sentence with the shipped-fold numbers: "On the shipped folds var11 as a
   feature gains +0.0004 (L2 on log1p) and +0.0032 (weighted by var11), within the fold SD of about 0.04; 1/var11
   alone scores 0.071 (0.038 to 0.119), through risk selection (USE-6); var11 is indexed by a median 1-2% a term and
   does not change more often going into a loss term (63.7% against 62.4% of steps, Fisher p 0.70)." Nothing else
   changes; the decision ("decides on the worse") is keep, as both gains are far below noise. Precedents
   frempl_french_motor_personal_line and australian_vehicle_insurance_2004_2005 state the same score.
2. **MET-14** (Should, documentation). One sentence in the target bullet: "The release records no term length, so the
   share of terms cut short is unknown and cannot be given; no feature carries a cut (var17 is no share of a year,
   var11 does not fall at loss terms), and the target is a ratio over the insured value, so it stays per contract
   (MET-14)." This departs from nothing: MET-14's 'notes give the share cut' clause cannot be met without a term
   length, and the note says so. What sets it apart from spanish_motor_insurance_2015_2018 (share 2,055 of 37,090
   given): no term length or dates in the release.

Both are text in curation_comments; they need the README regenerated and a CHANGELOG.md entry of the working copy.

**Issues for the curator, ranked**

1. **var1, var3, var7, var8: nominal categories, ordered categories, or numbers?** (P7, CLEAN-14, Should; quality.)
   - Problem: the comment above CATEGORICAL in dataset.py calls them "ordinal"; they ship unordered. Neither the
     record nor the README quotes a source for "ordinal"; the record and curation_comments say only that the data
     page lists var1-var9 as categorical. Neither auditor (nor I) could read the Kaggle data page (JavaScript).
   - Effect: small. Anonymised codes 1..k (k 5-8), Z already missing; loss rates are not monotone in the level
     (var8: 0.33, 0.27, 0.22, 0.23, 0.20, 0.39%). No validity question; the order changes what a model may assume.
   - Side for unordered (as shipped): data page lists them categorical (record); the 2026-11-02 column audit kept
     them; CLEAN-14 "categorical by default" for an ordinal scale of unknown meaning.
   - Side for ordered by code: the comment's word "ordinal", if the data page says it; precedent miami_housing's
     unlabelled 1-5 structure_quality ordered by its codes (CLEAN-14 Cases). The order may come only from the
     source's word, never from the loss rates (CLEAN-14, 2026-10-31).
   - Side for numbers: CLEAN-14's 2026-11-01 mark, a scale with no words per level "is a number, as shipped"; the
     2026-10-31 blind reviewer suggested numeric. The values are digits 1..k plus Z, so a number is lossless.
   - What settles it: the data page's wording (one look, logged in to Kaggle). Options: (a) the page says ordinal:
     FeatureTypes(ordinal=...) levels 1..k in code order, or numbers under the 2026-11-01 mark (your call between
     the two, as miami_housing and the mark point different ways); (b) it does not: keep unordered, reword the comment
     to "the nine policy variables the data page lists as categorical"; (c) unverifiable: same as (b).

**Agreed facts (both auditors, with the probes)**

- 452,061 rows, 299 features, 3 shipped folds of 150,687 test rows; var11 in features, var11_weight out, equal to
  var11 on every row; sample_weight None.
- var11^2 integer on 94-100% of rows (key differences in rounding), floor 250,000; across consecutive terms the ratio
  has median 1.01-1.02; it falls going into a loss term in 2.7% of steps against 2.7-4.5% otherwise.
- No column for term length, dates, earned amount or cancellation; var17 has 17.8% zeros and denominators not
  dividing 12; var15 steps by 1 (age).
- 1/var11 alone 0.038 / 0.118-0.119 / 0.056 (mean 0.071); var11 alone the negative; models 0.27-0.32.
- Gain of var11 as a feature: +0.0004 (L2), +0.0032 (weighted); weighted fit -0.0053 vs unweighted.
- Scorer equals the host's R formula to 7e-12; constant scores 0; 387-402 losses per test fold.
- Probe 23: 4.8-4.9% of test rows have an exact-profile copy in training; lookup gain +0.0011 (SE 0.0011); honest
  capped fit only 0.040, so low power. Task probe: LightGBM beats the dummy on 3 of 3 splits by +0.233.
- Library: with target_transform="log1p" the scorer applies expm1 to y_pred before ranking; a log-scale prediction
  above about 709.8 becomes inf and raises (_require_finite, metrics.py about line 2005). Gini depends only on order.
  No real prediction approaches it (published max log1p 3.29). Not a dataset issue: for the metric maintainers,
  rank-only metrics could skip the inverse of y_pred (expm1 is monotone) or clip before it; it applies to every
  log-transformed target scored by a rank metric. No REVIEW.md issue for this dataset.

No disputed fact: the auditors differ only in the key used for terms (with or without var13) and in rounding; both
readings give the same conclusion. No conflict between rules: every Must holds on its own.

**Consistency with precedent**

- LEAK-41 weight-alone score: follows frempl_french_motor_personal_line (0.184) and
  australian_vehicle_insurance_2004_2005 (0.205), which state it. Here it is stated for a planned weight, not a
  realized one; the clause's wording does not exempt that, so stating it is the consistent reading.
- MET-15 no sample weight: follows the rule's own named cases (this dataset, g_research_crypto_forecasting_1m,
  boreal_postfire_lichen_biomass).
- MET-14 per-contract target: follows spanish_motor_insurance_2015_2018 in outcome; the share cut cannot be given
  (no term length), which the note states.
- USE-6 risk selection by a feature known at the quote (var11 predicting losses): follows
  spanish_motor_insurance_2015_2018 (Premium predicting the cut, kept).
- CLEAN-14: miami_housing (unlabelled scale ordered by codes) and the 2026-11-01 mark (no words per level, a number)
  point different ways for anonymised codes; hence issue 1 goes to the curator, not settled here.

</details>

<details><summary>Claim audit</summary>

**Claim audit, liberty_mutual_fire_peril_loss_cost: focused re-review under LEAK-41 and MET-14 to MET-16
(2026-11-08)**

**Verdict:** ship as defined. Every claim that today's change makes or reopens held against a test that could have
refuted it. Nothing refuted. One note gap (LEAK-41's 1/weight-alone score is not stated) and one library-level
robustness point (MET-13) are below; neither blocks shipping. Settled points of REVIEW.md (forced split, copies,
var13, the weather block, the log1p scale) are not repeated unless today's change touches them.

**How I tested:** the definition loaded through load_definition(...).to_container() (452,061 rows, 299 features, 3
shipped folds of 150,687 test rows); scorer(c) for every score; LightGBM (500 trees, lr 0.03, 15 leaves, min_child
300, colsample 0.5, lambda 10, seed 0) on the shipped folds.

**Claims and tests**

| # | claim | source | test | result | evidence | rule |
|---|---|---|---|---|---|---|
| 1 | var11 is "the square root of a round sum insured, set at underwriting" | ScoringColumn description; README scoring table; accepted warning | var11^2 roundness; floor | holds | var11^2 is an integer on 100% of rows, a multiple of 100 on 100%, of 1,000 on 95.2%; min var11 = 500 (250,000); top values 250k, 500k, 300k, 400k, 600k, 1M | LEAK-41, MET-2 |
| 2 | var11 is a planned amount, not set or cut after the prediction point (the LEAK-41 question of the change note) | accepted warning "the size of the risk set at underwriting"; curation_comments var11 bullet | consecutive terms of a risk (key: every column but var15 and var11; var15 steps by 1): does var11 change more into a loss term? | holds | 92,029 steps: changes into a loss term 167/262 = 63.7% vs 62.4% into a no-loss term (Fisher p 0.70); median new/old ratio 1.0100 in both, share reduced 2.7% in both. Key also without var13: 57.1% vs 55.8% (p 0.66). It is indexed about +2% a year in sum insured and does not move at the loss. No realized term in it | LEAK-41, LEAK-10 |
| 3 | var11_weight is an exact copy of var11; the weight is a function of the features | dataset.py _clean; MET-15 reason | equality, NaN | holds | equal on 452,061/452,061 rows, 0 NaN | MET-2, MET-15 |
| 4 | var11 stays a feature; var11_weight never is; no sample_weight | dataset.py; README | feature_columns(c), sample_weight(c) | holds | 299 features, var11 in, var11_weight out; sample_weight None | MET-2, MET-15 |
| 5 | As a feature, var11 changes the score within fold noise (-0.010 on 6 random folds) | curation_comments | shipped folds, with/without var11, L2 on log1p and the var11-weighted fit | holds | gain +0.0004 (L2; -0.022/+0.031/-0.008) and +0.0032 (weighted; -0.010/+0.020/-0.000); fold SD about 0.04 (notes) | MET-2 amended, LEAK-41 |
| 6 | No training weight is needed (MET-15: metric weight is a function of the features) | accepted warning | weighted (sample_weight = var11) vs unweighted fit, with var11 | holds (also on value) | weighted minus unweighted -0.0053 on average (+0.006/-0.010/-0.012, worse on 2 of 3); nothing argues for a sample weight | MET-15 |
| 7 | The metric is the competition's normalized weighted Gini with weights var11, scored on the published scale | Metric.source(...); README Metric block | (a) our scorer vs the host's R formula (forum 9880 / evaluation page) on random predictions, y on the published scale; (b) the source | holds | (a) differences 3e-13 to 7e-12 on the 3 folds; target_transform inverts log1p (max published 25.92). (b) Kaggle pages render only their title for me; the record quotes the Evaluation page ("The weights used in the calculation are represented by var11"), secondary sources agree (synthesized.io, NYC DS blog); Lennart checked the declared metric 2026-11-08 | MET-1, MET-3, MET-4, MET-13 |
| 8 | Computable on every fold (MET-2): unit per row, weight shipped, enough losses | implied | dummy constant, ties, losses per fold | holds | 402/399/387 losses per test fold; constant prediction scores 0 on each; coarse tied predictions score the same in two row orders (0.0410/0.0231/-0.0503 both); oracle 1.0 | MET-2, MET-13 |
| 9 | Means on our task what it meant on the source's | implied | same target (log1p only for modelling, scored back on the published scale), same rows (labelled half), same weight | holds | the Gini reads expm1(y) and var11 as Kaggle did; class balance 0.26% losses as published | MET-2 |
| 10 | The test rows' var11_weight values are for the scorer only (X1, 2026-11-08) | README scoring section | can a model gain from var11_weight beyond var11? | holds, trivially | var11_weight equals var11, which is already a feature, so reading it gives nothing new; the README line is a protocol statement, correct as written | MET-2, LEAK-9 |
| 11 | No feature encodes a realized term (the change note's question) | implied | which columns could be realized amounts: var11 (row 2); var15 (age, steps by 1 between terms); target not rebuildable from var11 (pub x var11^2 integer on 1.5% of losses only) | holds as far as tested | no time-on-risk, earned, or cancellation column exists; var13 tested by the earlier panel (LEAK-38). The anonymised var1-17 can't be checked further | LEAK-41, LEAK-10 |
| 12 | Forced split: no shortcut through shared units (probe 23) | splits_comment; the change note | probe 23 fixed rerun | holds, low power | exact-profile units: 4.8-4.9% of test rows; lookup gain on those rows -0.0013 (SE 0.0013), overall +0.0011 (SE 0.0011, above 0 on 1 of 3). The probe's capped honest fit is only 0.040, so the test is weak; the earlier panel's paired same-risk experiment (REVIEW.md) is the stronger evidence and agrees. Period outcome: not run (no time column) | SPLIT-8, SPLIT-9 |
| 13 | 4.8-4.9% of a test fold has an exact copy in training | curation_comments | probe 4 / probe 23 | holds | 4.8% to 4.9% per split | LEAK-19, LEAK-20 |
| 14 | 1/weight alone: LEAK-41 asks for it for each suspect column with a Gini | leak_checks.md LEAK-41 (not in the definition) | score 1/var11 and var11 as the prediction | untested in the definition; measured here | 1/var11 alone 0.038/0.118/0.056 (mean 0.071; var11 itself the negative); the model about 0.27-0.31. Not a leak: var11 is planned (row 2) and predicts the loss ratio through risk selection (larger risks have more losses but lower loss/TIV), which LEAK-41 keeps (USE-6) | LEAK-41 |

**Refuted:** none.

**Untested or gaps, ranked (validity first, Must first)**

1. LEAK-41 (Must) reporting clause, Should-level in effect here: the definition does not state 1/weight alone or the
   gain under the weighted fit; it gives only the L2 gain over random folds. What it changes: nothing in the task;
   var11 is set at underwriting (row 2), so it is no suspect column in LEAK-41's sense, and the clause may not bind.
   Mildest remedy: one clause in the var11 bullet of curation_comments: "on the shipped folds, var11 as a feature
   gains +0.0004 (L2) and +0.0032 (weighted by var11); 1/var11 alone scores 0.071 (0.038 to 0.118), through risk
   selection; var11 does not move at a loss term (63.7% against 62.4% of the steps change it, Fisher p 0.70)".
2. MET-13 (Must, library level, not this definition): with target_transform="log1p" the scorer inverts predictions
   before ranking, so a log-scale prediction above about 709 overflows and raises ("y_pred holds 1 NaN or infinite
   value(s) after the inverse"), although a Gini depends only on the order of predictions. No real model predicts
   that (the published maximum is log1p(25.9) = 3.29), so it changes no score here. Mildest remedy: in the library,
   rank-only metrics skip the inverse transform of y_pred, or clip before expm1; a note for the metric maintainers,
   not a REVIEW issue for this dataset.
3. MET-1: the Kaggle Evaluation and data pages were not readable in my session (JavaScript); the metric's wording rests
   on the record's quote, the earlier panel's check against the host's code, secondary sources and Lennart's check of
   2026-11-08. Nothing to change.
4. Probe 23's shared-unit test has low power on this table (honest fit 0.040 on 50,000-row caps). Covered by the
   earlier paired same-risk experiment; nothing to change.

**Sources:** https://www.synthesized.io/data-template-pages/business-property-insurance-risk,
https://nycdatascience.com/blog/student-works/property-casualty-loss-cost-data-type-case-study

**Files:** scripts and outputs in the run folder (not committed): the definition checks, the terms of a risk, the
fits with and without `var11` and with a training weight.

</details>

<details><summary>Column audit</summary>

**Column audit, liberty_mutual_fire_peril_loss_cost: focused re-review under LEAK-41, MET-14 to MET-16 (2026-11-08)**

**Verdict:** ships. No column is a realized amount at risk or encodes a realized term or a cut; var11 is a planned
amount (LEAK-41 does not fire). One documentation gap under the amended LEAK-41 (the 1/weight score is not stated),
one MET-14 note to add, and one older typing question (ordinal codes) that the exposure rules do not touch.

Frame: 452,061 rows, 301 columns; feature_columns = 299 (var11 in, var11_weight out); sample_weight(c) = None.

**Column table** (only what is new or changed under the new rules; the full per-column table of the 2026-11-02 column
audit stands and is not repeated)

| column | meaning | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| var11 | weight of the host's Gini (data page); sqrt of a sum insured: var11^2 is a whole number on 94.0% of rows, floor 250,000 (1.0% of rows) | yes, planned: set at underwriting and indexed at renewal (see F1) | float64, no missing | fine (feature), not a realized weight | LEAK-41, MET-15, USE-6 |
| var11_weight | copy of var11, ScoringColumn role weight read by normalized_weighted_gini | n/a (scoring only) | float64 | fine; not a feature, no sample weight (MET-15 names this dataset as the case) | MET-2, MET-15 |
| log1p_transformed_loss_ratio | host's transformed loss / total insured value, log1p | outcome | float64 | fine; a per-contract ratio over the insured value, not per time on risk (see F3) | MET-3, MET-14 |
| var17 | unknown; 0-100, 24,598 values | yes | float64 | fine: not a share of a term in force (F2) | LEAK-41 |
| var15 | unknown; whole numbers stepping by 1 per term, read as an age | yes | float64, 21.9% missing | fine, unchanged (not a term length) | LEAK-41 |
| var10, var12, var13, var14, var16 | unknown (deductible-like, counts, grade, percentage) | yes | unchanged | fine; none changes more at a loss term (F2) | LEAK-41, LEAK-10 |
| var1, var3, var7, var8 | code comment calls them ordinal; shipped nominal | yes | category, levels 1..k; dtype probe flags all four numeric_levels | question for the curator (F5) | CLEAN ordinal rule (2026-10-30) |
| all other columns | as in the 2026-11-02 column audit | yes | unchanged | fine | - |

**Findings, ranked**

**F1 (LEAK-41, Must; result: no leak).** var11 is a planned amount, not a realized one.
- Across a risk's consecutive terms (key: all columns but var15, var11, var13; var15 +1; 126,031 steps), var11^2 is
  unchanged in 44.2% and its ratio has median 1.02, quartiles 1.00 / 1.04: an annual indexation of a sum insured.
- Going into a loss term it falls in 2.7% of 337 steps against 4.5% of 125,694 without a loss (falls by >20%: 0.9%
  against 1.6%); after a loss it is unchanged in 48.4% (310) against 44.2%. A value cut by the outcome would fall
  more at loss terms, not less.
- Precision: the 6.0% of rows whose var11^2 is not whole carry a loss rate of 0.300% against 0.260% (Fisher p 0.22),
  so precision marks no cut. Round sums insured have a higher loss rate (multiple of 50,000: 0.319% against 0.252%,
  p 0.0016), the opposite of what pro-rating after a loss would leave; read as risk selection (declared round
  values), USE-6, kept.
- Remedy: none. Optionally one clause in the var11 bullet ("indexed by a median 2% a term, not lower at loss terms").

**F2 (LEAK-41, "a column that encodes it"; result: none).** No feature encodes a realized term or a cut.
- var17 (the only fractional 0-100 column) is not a share of a 12-month term: of its 239,039 values strictly between
  0 and 100, only 3.7% have a denominator dividing 12 (most common small denominators 11, 13, 7, 5, 23); 17.8% are 0,
  impossible for a time in force. It changes at 31.5% of loss steps against 25.1% of others (n 463 loss steps; the
  2026-11-02 audit showed the excess belongs to the risk, p 0.62).
- var10, var12, var14, var16 change at loss steps no more than at others (2.4/1.3/1.5/0.2% against 4.4/1.2/1.8/0.9%).
- The source has no term length, start/end date or earned column; nothing to annualise.

**F3 (MET-14, Should; documentation).** The target is a ratio over the insured value, not over time on risk. The term
length and any cuts are not recorded (task_summary.row says so). MET-14 keeps a per-contract target when no feature
set after the quote carries the cut (F2), and asks the notes to say so. The notes now say nothing on this.
- Remedy: one sentence in the var11 or the target bullet: "The release records no term length; whether some terms
  were cut short is unknown, and no feature carries a cut (var17 is no share of a year; var11 does not fall at loss
  terms), so the target stays per contract (MET-14)."

**F4 (LEAK-41 amended 2026-11-08; documentation, mild).** LEAK-41 asks the definition to give the score of 1/weight
alone for a Gini metric next to the weight's gain as a feature. The notes give only the gain (-0.010). On the shipped
folds 1/var11 alone scores 0.038 / 0.119 / 0.056 (mean 0.071) against the regularised LightGBM's 0.306-0.320 (var11
alone: -0.038 / -0.119 / -0.056). var11 is not a suspect column by timing, so this is a note, not a decision.
- Remedy: add "1/var11 alone scores 0.038-0.119 on the shipped folds" to the var11 bullet.
- Probe 22 was not run (no output): no sample weight is declared and the weight is itself a feature, so the proxy fit
  adds nothing; the 1/weight score above is the part of probe 22 that applies.

**F5 (pre-existing, not changed by the exposure rules; question for the curator).** The dtype probe flags var1, var3,
var7, var8 (numeric_levels). The comment above CATEGORICAL in dataset.py calls them "ordinal", yet they ship as
nominal categories; the 2026-11-02 audit kept them so because the data page lists them as categorical, and their loss
rates are not monotone. Since 2026-10-30 an ordinal scale ships as FeatureTypes(ordinal=...). Either the data page
names them ordinal (then declare them ordinal, levels 1..k in code order: the only order available for anonymised
codes, Z already missing) or it does not (then reword the comment). I could not open the Kaggle data page (renders no
text) to settle which.

**Checked and fine:** var11_weight is not in feature_columns; no sample_weight (MET-15 accepted warning consistent
with the rule text, which cites this dataset); MET-16 does not apply (no survey or design weight); probe 23 shared
units: 4.8% of test rows have an exact-profile copy in training, lookup gain +0.0011 (SE 0.0011), no leak.

**Files:** scripts and outputs in the run folder (not committed): var11 across terms and at loss terms, var17 and the
other policy variables at loss terms, the precision of var11, the dtype probe.

</details>

## Reference

Kaggle (2014). Liberty Mutual Group: Fire Peril Loss Cost. https://www.kaggle.com/competitions/liberty-mutual-fire-peril

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).
