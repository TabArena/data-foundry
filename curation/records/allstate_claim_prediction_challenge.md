---
unique_name: allstate_claim_prediction_challenge
name: Allstate Claim Prediction Challenge (Kaggle 2011, ClaimPredictionChallenge)
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
tags:
- Two-Regime Zeros
- Non-IID (Grouped)
original_source: Kaggle
year: '2011'
domain: insurance
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/ClaimPredictionChallenge
- https://digital.wpi.edu/downloads/zs25x859f
v2_path: datasets/_dev/tabarena-v0pt2/allstate_claim_prediction_challenge_1m/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 2: Allstate's own bodily-injury claim payments per
vehicle-year, with a scored leaderboard and dated years, but the target was adjusted by an undisclosed rule and 99.27%
of rows are zero.
- Source: Allstate's Kaggle competition (2011). Description page: "The goal of this competition is to predict Bodily
  Injury Liability Insurance claim payments based on the characteristics of the insured's vehicle". As published:
  `train_set`, 13,184,290 vehicle-years of 2005-2007 (household id, vehicle, model year, blinded make, model and
  submodel, anonymised vehicle and policy variables), target `Claim_Amount`; the 2008 and 2009 test rows were never
  labelled publicly. Allstate in thread 928, quoting the data page: the response "has been adjusted to control for known
  non-vehicle effects".
- Use case: for example, an insurer rating a vehicle for bodily-injury liability at policy start (a vehicle factor in
  the tariff); the page names the target and the features, not the decision. Fit approximate: what the adjustment
  removed is undisclosed (USE-5, USE-8). Regime temporal by `Calendar_Year`, as the competition scored (train 2005-2007,
  public 2008, private 2009), with households recurring (SPLIT-13).
- Siblings and duplicates: `allstate_claims_severity` (Yes; a 2016 competition on positive losses only) is other data,
  no duplicate (PROV-7). OpenML: none by name; external collections: none found.
- Papers and pages: the Kaggle description and Evaluation pages; Huangfu (2015), WPI MSc report (in `source_links`); the
  winner's method was never posted (thread 1073).
- Metric: normalized Gini on the claim amount, Kaggle Evaluation page: "The metric (for both the leaderboard and final
  winners) used to score entries will be 'normalized Gini coefficient'"; deliberate (a leaderboard metric, MET-4);
  inputs none. On a continuous target it is not 2 x ROC AUC - 1, so it needs a custom metric in the library (MET-12,
  MET-13).
- Earlier AI triage, 2026-10-20, measured: 99.27% zeros (95,605 positives, no negatives); 71% of the 2007 households
  already present in 2005-2006; untuned LightGBM 2005-06 -> 2007: AUC 0.59 for a claim, normalized Gini 0.093, R^2 -0.03
  on log1p among positives.
- Risks for /add-dataset: the undisclosed adjustment (USE-5); missing values occur only in train and Allstate asked that
  models not use missingness (thread 826, per the earlier triage); three labelled years give at most two windows and the
  2006 one trains on 2005 alone, likely under the 50% floor (SPLIT-14, else SPLIT-8); the size needs a 1M cut (about
  7,300 positives). Family question: insurance conventions (no negative amounts were measured).
- Priority: gap 0 (insurance has 4 accepted datasets, one above the thin line of the snapshot), use case 0 (decision not
  named, fit approximate), source + (Allstate's pages), shape + (13M rows, mixed types, dated and grouped), risk - (an
  undisclosed target adjustment).

**Assessment (AI, 2026-10-30):** suggested call for policy question 3 of the zero-inflated review, where Andrej asked
for a call per dataset from its references and the domain's practice instead of one convention for the family (the
shared reasoning: a time exposure or a sum insured is a feature, and a rating-cell table weights the metric by its
exposure; negative amounts that are recoveries become 0; the source's metric first, else the normalized Gini as a
context metric, since RMSE on raw amounts follows a few large claims and a Tweedie or Poisson deviance needs positive
predictions; MET-10 as amended on 2026-11-02 (Andrej) later declined a family-wide metric, so each table's metric is
decided on its own); the curator
has the call.
- Target: `Claim_Amount` as published; Allstate's undisclosed adjustment stays the open point (USE-5).
- Exposure: none published; some rows are part years (vehicles of the next model year, insured for part of the calendar year, claim at 0.20% against 0.73%). Negative amounts: none.
- Metric: the competition's normalized Gini (MET-4), a custom metric for the library (MET-13); the other tables of the
  family that take the Gini as a context metric reuse it.
- Missingness occurs only in the training file and Allstate asked that models not use it (thread 826); the README says
  so, as a benchmark cannot enforce it.

CC (2026-10-30, Andrej): `Yes`, priority 2 (the AI screening had `TBD -> 2nd Tier`, priority 2; zero-inflated screening
review page).

Allstate's Kaggle competition: one row per insured vehicle and calendar year, 13,184,290 rows for 2005-2007 with
`Household_ID`, `Vehicle`, model year, blinded make, model and submodel and anonymised vehicle and policy variables;
the 2008 and 2009 test rows were never labelled publicly. The target, bodily-injury liability payments, "has been
adjusted to control for known non-vehicle effects" (data page), so it "isn't actually in units of any major currency"
(Allstate, thread 928). Not `allstate_claims_severity` (2016, positive losses only). Measured on the downloaded
`train_set` (2026-10-20): 99.27% exact zeros, 95,605 positives, no negatives, matching Huangfu (2015, Sec. 2.0, p. 6:
"only 95,605 non-zero values (about 0.73%) among the 13,184,290 records"); 4,309,042 households, 71% of the 2007
households already present in 2005-2006.

Split temporal by `Calendar_Year`, as the competition did (trained on 2005-2007, scored on 2008 and 2009). Drop
`Row_ID`; `Household_ID` is a group id (a household's own claim history is fair under the temporal split). Missing
values (37-54% of `Cat2`, `Cat4`, `Cat5`, `Cat7`) occur only in the training file, and Allstate asked that models not
use missingness (thread 826). Untuned LightGBM, 3M sampled rows of 2005-2006 -> 2007: AUC 0.59 for a claim, normalized
Gini 0.093, R^2 -0.03 on log1p among positives; Huangfu's best model reached 0.080 on 2007 (Sec. 5.0 d, p. 30), the
Kaggle winner 0.20 on 2009. A small real signal behind an undisclosed adjustment, at a size that needs subsampling (a
1M-row cut holds about 7,300 positives): 2nd tier. Terms: Kaggle competition rules (a 2022 licence question in the
forum is unanswered). To check: whether a target adjusted for non-vehicle effects and a vehicle-only feature set count
as a representative pricing task.

**Assessment (AI, 2026-11-01):** added as `datasets/_dev/tabarena-v0pt2/allstate_claim_prediction_challenge_1m/` by /add-dataset with the full review panel; the open questions are in its `REVIEW.md`. Recommend shipping after the panel's changes; only issue 1, the forced grouped split by household (open against how_much_did_it_rain, with five siblings), could turn it to `No`. Changes after the panel: 2007 dropped (LEAK-24, its large claims missing; MET-2), `household_vehicles` and Cat10 to Cat12 dropped, `OrdCat` categorical. What shipped supersedes the text below the CC: not "split temporal by `Calendar_Year`" over 2005-2007 but 2005-2006 only (1.5M rows of whole households), split by household, so a household's own claim history is not used; Gini 0.053 / 0.054 / 0.022 by fold (random predictions 0.019-0.025, the third within chance), not 0.093; "the Kaggle winner 0.20 on 2009" is no like-for-like reference, as Allstate blinded model codes separately per file (26% of test rows carry codes absent from training). `required_split` and `tags` wait for your marks on the field rows (issue 1), as do issues 2 to 4. Priority 3: gap + (insurance thin), use case 0 (fit approximate), source + (Allstate's pages, Huangfu's report), shape + (1.5M rows, grouped), risk - (split open; one fold at chance; undisclosed adjustment).

CC (2026-11-02, Andrej): the forced grouped split ships (issue 1 (a) in allstate_claim_prediction_challenge_1m; the record takes `Grouped (NON-IID)` and `Non-IID (Grouped)` as the issue says): "Forced group splits should be fine. Regarding forced IID, did you make sure there are no leaks? Whenever there are no leaks we can ship." Recorded in SPLIT-8 (amended 2026-11-02: a forced grouped split ships; a forced IID split ships only when the leak test across the random split finds none).

**Assessment (AI, 2026-11-02):** the leak test across the forced grouped split finds none (SPLIT-8). Shared rows: 84% of the test rows have an exact feature copy in another household on the training side (one vehicle type and policy profile), but the copies' claim rate (0.68%) is the test rows' (0.66-0.69%), a lookup of their mean target scores a normalized Gini of -0.008 / -0.008 / -0.002 against the model's 0.053 / 0.054 / 0.022, and none of the 10,761 test claims has a training row with the same features and amount; the 6,090-6,224 test rows per fold whose whole multi-vehicle household-year (vehicles and policy columns) recurs under another household in training claim no more when that household claimed (0.54% / 0% / 0.76% against 0.54% / 0.75% / 0.61%), so no household hides under two ids. Shared period (the calendar year): adding the training side's mean target of the year changes no score, a year-only predictor scores 0.001 to 0.026, and taking the test year's rows out of training never costs more than taking out as many random rows (6 of 6 fold-years score higher without the same year: 2005 0.084 / 0.072 / 0.026 against 0.061 / 0.040 / -0.051, 2006 0.073 / 0.054 / 0.028 against -0.007 / 0.027 / 0.025). No feature is built from other rows' outcomes once `household_vehicles` and `Vehicle` are gone; NVVar1 to NVVar4 belong to the row's own household and are no count of the year's claims (claim rate 0.85-1.25% above their minimum against 0.67-0.71%), and they change as often after a claim of the previous year as with one of the same year. how_much_did_it_rain's `No` named a measured shared-period leak; none is found here.

CC (2026-11-03, Andrej): 2007 stays dropped (issue 2 (A) in allstate_claim_prediction_challenge_1m; `Calendar_Year` stays a feature): "We can drop 2007 because we still have 1 million of samples and the current limit is 1M. We might reconsider this decision for a future version."

CC (2026-11-03, Andrej): rebuilt as the 2006 renewal book with the 2005 history, counts only (issue 3 (B) in allstate_claim_prediction_challenge_1m): "I go with your recommendation of 2006 renewal book with the 2005 history (counts)". The rows are the 4.4M vehicle-years of 2006 (1.5M of whole households sampled); 2005 gives the household's vehicle and claim counts, the cars carried over and the car's own claims; `Calendar_Year` goes (one value), so the 2007 decision above no longer keeps it.

CC (2026-11-03, Andrej): the competition's normalized Gini on the amount stays, the regression on log1p (issue 4 (A)): "Let's go with A".

CC (2026-11-03, Andrej): ship (verdict). Issue 5 (A): households drawn at random and dealt to folds at random, the natural claim rate (claim households dealt evenly gave no steadier folds); the metric, the competition's normalized Gini on the amount, checked.

CC (2026-11-08, Lennart): the declared metric (`normalized_gini`) is checked, as declared; the record ships, with no open issue on the PR #47 review board.

**Assessment (AI, 2026-11-08):** ships by default (no open issue on the PR #47 board), but the definition's changes of 2026-11-06 (the exposure paragraph) have not passed `dataset check`, and the re-review panel under LEAK-41 and MET-14 to MET-16 has not run: both wait for the competition files, which download only after the Kaggle competition rules are accepted. No container is built before both pass.

## Reference

Kaggle (2011). Allstate Claim Prediction Challenge. https://www.kaggle.com/competitions/ClaimPredictionChallenge

Huangfu D. (2015). Data Mining for Car Insurance Claims Prediction. MSc project report, Worcester Polytechnic
Institute. https://digital.wpi.edu/downloads/zs25x859f

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).
