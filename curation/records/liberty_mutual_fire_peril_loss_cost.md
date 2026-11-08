---
unique_name: liberty_mutual_fire_peril_loss_cost
name: 'Liberty Mutual Group: Fire Peril Loss Cost (Kaggle 2014)'
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
tags:
- Two-Regime Zeros
- Larger IID Data
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

**Assessment (AI, 2026-11-01):** added as `datasets/_dev/tabarena-v0pt2/liberty_mutual_fire_peril_loss_cost/` by /add-dataset with the full review panel; the open questions are in its `REVIEW.md`. Recommend shipping after the panel's changes and the unweighted Gini of issue 2 (not yet made); only issue 1, the forced random split (open against how_much_did_it_rain, with five siblings), could turn it to `No`. Changes after the panel: the target ships as `log1p_transformed_loss_ratio`, scored on the published scale (log1p ahead on 2 of 3 folds, 0.313 against 0.298), and the notes give the measured checks of timing, repeated risks and copies. The definition departs from three readings of the 2026-10-30 Assessment and the text below the CC: "Regime IID, as the competition split" is now tagged `ForcedIIDFromTemporal` (issue 1); `var11`, "a scoring column and not a feature", stays a feature and the metric's weight, which MET-2 bars as written (issue 2); the target "as published" ships as log1p. `required_split` Random (IID) matches the definition. Priority 3: gap + (insurance thin), use case 0 (fit approximate, transform undisclosed), source + (the insurer's own data and metric), shape + (452,061 policies, 299 features), risk - (split and metric open; 1,188 losses).

CC (2026-11-02, Andrej): the forced IID split ships (issue 1 (a)): "Forced group splits should be fine. Regarding forced IID, did you make sure there are no leaks? Whenever there are no leaks we can ship." Recorded in SPLIT-8 (amended 2026-11-02: a forced grouped split ships; a forced IID split ships only when the leak test across the random split finds none).

**Assessment (AI, 2026-11-02):** the leak test across the random split finds none: rows share a risk across the split (17-54% of each test fold, by how loosely a risk is matched) but not its outcome: a risk's loss in training ranks its test terms at AUC 0.50-0.52 (0.5 is chance), only 6 to 14 of the 1,188 losses share a risk with another loss, and taking a test risk's other terms out of training costs no more than dropping as many random rows (on all 6 pairs of fold and key). The host split at random itself. how_much_did_it_rain's `No` named a measured leak; none is found here.

CC (2026-11-02, Andrej): `var11` is the metric's weight and stays a feature (issue 2 (a)): "I want to score with the feature and also keep it as a feature assuming it to be known during train and test time as input for the model." The competition's weighted normalized Gini with `var11` as weight, and `var11` a feature; recorded in MET-2 (amended 2026-11-02: a weight known at the prediction point for train and test rows alike stays a feature and is also the metric's weight). All issues of the REVIEW are now resolved.

CC (2026-11-02, Andrej): ship, with `var11` a feature and the weight of the competition's normalized Gini (issue 2 (a), MET-2 amended).

CC (2026-11-06, Lennart): `var11` stays a feature and a copy, `var11_weight`, ships as the scoring column the weighted Gini reads (MET-2 as reworded on 2026-11-05; asked in PR #47's review); no training weight, since the weight is a function of the features (MET-15). Issue 3 of the folder's REVIEW.md.

CC (2026-11-08, Lennart): the declared metric (`normalized_weighted_gini`) is checked, as declared; the record ships, with no open issue on the PR #47 review board.

**Assessment (AI, 2026-11-08):** ships by default (no open issue on the PR #47 board), but the definition's changes of 2026-11-06 (the `var11_weight` scoring column the metric reads and the exposure paragraph) have not passed `dataset check`, and the re-review panel under LEAK-41 and MET-14 to MET-16 has not run: both wait for the competition files, which download only after the Kaggle competition rules are accepted. No container is built before both pass.

**Assessment (AI, 2026-11-08):** review panel (focused: claim auditor, column auditor, mediator; re-review under LEAK-41, MET-14 to MET-16, after the raw data arrived): ship after changes (two sentences in the notes, made: the `var11` bullet gives its shipped-fold gains, +0.0004 with an L2 fit and +0.0032 with the fit weighted by `var11`, the score of 1/`var11` alone, 0.071, and that `var11` changes no more often going into a loss term, a planned amount under LEAK-41; the target bullet says no term length is recorded, so the target stays per contract under MET-14); disputed: none; for the curator: issue 4 (the type of `var1`, `var3`, `var7`, `var8`: unordered as shipped, ordered by code, or numbers; the Kaggle data page settles it). This supersedes the earlier Assessment of 2026-11-08: the competition's files are in the warehouse, `dataset check` passes on them (0 errors, 0 warnings) and the re-review panel has run.

## Reference

Kaggle (2014). Liberty Mutual Group: Fire Peril Loss Cost. https://www.kaggle.com/competitions/liberty-mutual-fire-peril

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).
