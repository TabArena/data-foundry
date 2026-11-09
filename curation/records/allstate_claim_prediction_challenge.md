---
unique_name: allstate_claim_prediction_challenge
name: Allstate Claim Prediction Challenge (Kaggle 2011, ClaimPredictionChallenge)
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Andrej
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

**Assessment (AI, 2026-11-01):** added as `datasets/_dev/tabarena-v0pt2/allstate_claim_prediction_challenge_1m/` by /add-dataset with the full review panel; the open questions are in its Review. Recommend shipping after the panel's changes; only issue 1, the forced grouped split by household (open against how_much_did_it_rain, with five siblings), could turn it to `No`. Changes after the panel: 2007 dropped (LEAK-24, its large claims missing; MET-2), `household_vehicles` and Cat10 to Cat12 dropped, `OrdCat` categorical. What shipped supersedes the text below the CC: not "split temporal by `Calendar_Year`" over 2005-2007 but 2005-2006 only (1.5M rows of whole households), split by household, so a household's own claim history is not used; Gini 0.053 / 0.054 / 0.022 by fold (random predictions 0.019-0.025, the third within chance), not 0.093; "the Kaggle winner 0.20 on 2009" is no like-for-like reference, as Allstate blinded model codes separately per file (26% of test rows carry codes absent from training). `required_split` and `tags` wait for your marks on the field rows (issue 1), as do issues 2 to 4. Priority 3: gap + (insurance thin), use case 0 (fit approximate), source + (Allstate's pages, Huangfu's report), shape + (1.5M rows, grouped), risk - (split open; one fold at chance; undisclosed adjustment).

CC (2026-11-02, Andrej): the forced grouped split ships (issue 1 (a) in allstate_claim_prediction_challenge_1m; the record takes `Grouped (NON-IID)` and `Non-IID (Grouped)` as the issue says): "Forced group splits should be fine. Regarding forced IID, did you make sure there are no leaks? Whenever there are no leaks we can ship." Recorded in SPLIT-8 (amended 2026-11-02: a forced grouped split ships; a forced IID split ships only when the leak test across the random split finds none).

**Assessment (AI, 2026-11-02):** the leak test across the forced grouped split finds none (SPLIT-8). Shared rows: 84% of the test rows have an exact feature copy in another household on the training side (one vehicle type and policy profile), but the copies' claim rate (0.68%) is the test rows' (0.66-0.69%), a lookup of their mean target scores a normalized Gini of -0.008 / -0.008 / -0.002 against the model's 0.053 / 0.054 / 0.022, and none of the 10,761 test claims has a training row with the same features and amount; the 6,090-6,224 test rows per fold whose whole multi-vehicle household-year (vehicles and policy columns) recurs under another household in training claim no more when that household claimed (0.54% / 0% / 0.76% against 0.54% / 0.75% / 0.61%), so no household hides under two ids. Shared period (the calendar year): adding the training side's mean target of the year changes no score, a year-only predictor scores 0.001 to 0.026, and taking the test year's rows out of training never costs more than taking out as many random rows (6 of 6 fold-years score higher without the same year: 2005 0.084 / 0.072 / 0.026 against 0.061 / 0.040 / -0.051, 2006 0.073 / 0.054 / 0.028 against -0.007 / 0.027 / 0.025). No feature is built from other rows' outcomes once `household_vehicles` and `Vehicle` are gone; NVVar1 to NVVar4 belong to the row's own household and are no count of the year's claims (claim rate 0.85-1.25% above their minimum against 0.67-0.71%), and they change as often after a claim of the previous year as with one of the same year. how_much_did_it_rain's `No` named a measured shared-period leak; none is found here.

CC (2026-11-03, Andrej): 2007 stays dropped (issue 2 (A) in allstate_claim_prediction_challenge_1m; `Calendar_Year` stays a feature): "We can drop 2007 because we still have 1 million of samples and the current limit is 1M. We might reconsider this decision for a future version."

CC (2026-11-03, Andrej): rebuilt as the 2006 renewal book with the 2005 history, counts only (issue 3 (B) in allstate_claim_prediction_challenge_1m): "I go with your recommendation of 2006 renewal book with the 2005 history (counts)". The rows are the 4.4M vehicle-years of 2006 (1.5M of whole households sampled); 2005 gives the household's vehicle and claim counts, the cars carried over and the car's own claims; `Calendar_Year` goes (one value), so the 2007 decision above no longer keeps it.

CC (2026-11-03, Andrej): the competition's normalized Gini on the amount stays, the regression on log1p (issue 4 (A)): "Let's go with A".

CC (2026-11-03, Andrej): ship (verdict). Issue 5 (A): households drawn at random and dealt to folds at random, the natural claim rate (claim households dealt evenly gave no steadier folds); the metric, the competition's normalized Gini on the amount, checked.

CC (2026-11-08, Lennart): the declared metric (`normalized_gini`) is checked, as declared; the record ships, with no open issue on the PR #47 review board.

**Assessment (AI, 2026-11-08):** ships by default (no open issue on the PR #47 board), but the definition's changes of 2026-11-06 (the exposure paragraph) have not passed `dataset check`, and the re-review panel under LEAK-41 and MET-14 to MET-16 has not run: both wait for the competition files, which download only after the Kaggle competition rules are accepted. No container is built before both pass.

**Assessment (AI, 2026-11-08):** the competition's files are in the warehouse: `dataset check` of the definition with the exposure paragraph passes (0 errors, 0 warnings) and the re-review panel ran (next line), so the Assessment of 2026-11-08 above (check and panel waiting for the files) is superseded. Superseded too, the part-year statement of 2026-10-30 ("vehicles of the next model year ... claim at 0.20% against 0.73%"): about 38% of the 2006 rows are cars that joined during the year (27.4% new households, 10.7% cars added by a household of 2005), on risk for about half of it (per row they claim in 2006 at 0.45 to 0.59 times their own 2007 rate in every band of model-year age, against 0.91 to 1.11 for the cars carried from 2005, and 2007 repeats the pattern); the cars of the next model year (1.37% of the rows) are the latest of them. The notes now say so, name the group of the exposure paragraph's 1.40% / 0.73% (cars insured since 2005 whose household continued into 2007: 1.39% against 0.72%; over all 2006 cars 0.96% against 0.60%), bound the share cut short by claims (at most 32.5% of the 2006 cars not seen in 2007) and say that the new households' 0.50% and part of the history's lift measure the shorter term.

**Assessment (AI, 2026-11-08):** review panel (focused: claim auditor, column auditor, mediator; re-review under LEAK-41, MET-14 to MET-16): ship after changes, once the population is decided; the mediator recommends keeping only the cars on the policy at the start of 2006 (MET-14 departed from for the 38% part years, whose start is not released: `vehicle_insured_2005` alone scores 0.046-0.052 of the full model's 0.058-0.102, and trained and tested on the carried rows untuned LightGBM scores 0.063 / 0.057 / 0.003, to be measured again after a rebuild); LEAK-41, LEAK-10, SPLIT-8 (probe 23's flag an artifact of drawing rows), MET-15, MET-16 and MET-1 to MET-4 hold; disputed: whether the target per row holds for the rows that joined during 2006 (issue 6: the column auditor no, the claim auditor yes; the mediator's test settled the 38% for the column auditor); for the curator: issues 6 (the renewal book or all rows as an exception) and 7 (the target per contract where a claim ends the cover) in the record's Review.

CC (2026-11-08, Lennart): the rows are the 2006 renewal book, only the cars on the policy at the start of 2006, those insured in 2005 too (issue 6 (B) in allstate_claim_prediction_challenge_1m): "Option B: The renewal book." It confirms Andrej's "2006 renewal book" framing of issue 3 (B) (CC of 2026-11-03) and supersedes the rows that CC gives ("the 4.4M vehicle-years of 2006"): the cars that joined during 2006 (38.1% of its vehicle-years, on risk for part of the year, MET-14) leave, selected on a fact of 2005, never on presence in 2007 (LEAK-41), and the flag `vehicle_insured_2005` leaves as constant.

CC (2026-11-08, Lennart): the target stays per contract where a claim ends a car's cover (issue 7 (A) in allstate_claim_prediction_challenge_1m, `ok`): confirmed under MET-14's per-contract clause (amended 2026-11-08) as the case where the claim causes the cut, distinct from spanish_motor_insurance_2015_2018's lapses. The cut cars claim more per contract (1.39% against 0.72% for the book's cars of households that continued into 2007), no feature carries the cut, and no rate can be built without an exposure.

**Assessment (AI, 2026-11-08):** rebuilt on the renewal book (issue 6 (B)); `dataset check` 0 errors, 0 warnings. Rows: 2,754,936 of the 4,447,729 vehicle-years of 2006 stay (61.9%; 1,942,447 households, 22,632 claims, 0.82%), the 1,692,793 cars that joined during 2006 (claim rate 0.54%) leave; the 1.5M sample holds 0.82% claims, 4,006 to 4,210 per test fold, and the history is never missing. Signal (TP-2): untuned LightGBM on the shipped folds scores a normalized Gini of 0.106 / 0.091 / 0.061 against 0 for the dummy (random predictions SD 0.023 to 0.025 per fold), and 0.022 to 0.106 over nine folds of three random household splits (mean 0.069, SD 0.024); the task probe (sides capped at 200,000 rows) puts LightGBM above the dummy on 3 of 3 splits (+0.037, SE 0.004), its linear model and random forest at chance, and flags `no_signal` and `unstable`, which read its R^2-type skill (EV-3). The panel's 0.063 / 0.057 / 0.003 trained on about 0.62M carried rows; on the rebuilt 1M-row training sides the renewal book scores as all rows did (0.058 to 0.102). The 2005 history adds +0.005 to +0.012 on the amount and +0.001 to +0.003 on claim yes/no; `household_vehicles_carried` adds +0.001 to +0.009 on 3 of 3 folds (on all rows it had lowered the score), so it stays. Leak probes: no feature scores alone, all features -0.072 R^2 on log1p, 74.4% of the test rows have an exact feature copy in training; probe 23: no period gain (-0.016, SE 0.030) and no shared-unit gain (0 households shared; the exact profile -0.005, SE 0.024). Residual: 38,728 rows of the book (1.41%) share a vehicle key with more rows in 2006 than in 2005 (claiming at 0.69% against 0.82%), so a few same-type cars added in 2006 stay; dropping them would select on the cars added later in the year. The Assessment of the review panel above is superseded where it gives the shipped rows as all of 2006 and the signal on the carried rows as 0.003 to 0.063.

CC (2026-11-09, Andrej): the folds keep testing on all rows of the 2006 renewal book, the gaps kept as missing (review issue 8, A, as implemented).

CC (2026-11-09, Andrej): the split stays by household (review issue 9, A, as implemented); the splits comment now gives the 2005-to-2006 score of 0.064 as above the household folds of that build and names the training side's year and the maturity of its amounts.

CC (2026-11-09, Andrej): columns held only for training rows stay out for now, no training-only role (cross-dataset item of 2026-11-09; MET-14, LEAK-41, MET-16); the notes list them.

CC (2026-11-09, Andrej): the training labels' maturity is stated in the notes (cross-dataset item of 2026-11-09, option B).

## Review

**Outcome:** added as `allstate_claim_prediction_challenge_1m`. The AI recommends shipping it: on Lennart's marks of
2026-11-08 the rows are the 2006 renewal book, the cars on the policy at the start of the year (issue 6, B), and the
target stays per contract where a claim ends the cover (issue 7, A). The source is Allstate's Kaggle competition (2011):
one row per insured vehicle and calendar year, the target its bodily-injury liability claim payments of 2006, adjusted
by Allstate for non-vehicle effects by an undisclosed rule (0 for 99.18% of the rows), shipped as log1p and scored by
the competition's normalized Gini on the amount. The inputs are the vehicle's and the policy's anonymised
characteristics and the household's and the car's record of 2005 as counts; 1.5M of the 2.75M vehicle-years of the
renewal book (61.9% of 2006; the cars that joined during 2006 are left out) are sampled as whole households, split by
household and tagged as forced from temporal. Validity: USE-1 holds (approximate fit); LEAK-41 holds: no column is set
or cut after the rating, and the rows are selected on a fact of 2005, never on presence in 2007; LEAK-10 holds for the
four 2005-history columns; LEAK-24 triggered by the 2007 claims, fixed by dropping 2007 (issue 2); SPLIT-8 holds (no
household on both sides of a fold; probe 23 on the rebuilt folds finds no period gain and no shared-unit gain, -0.005
with SE 0.024 for the profile lookup); MET-14 holds: the part years of the cars that joined during 2006 are left out
(issue 6), and the per-contract clause is confirmed where a claim ends the cover (issue 7); MET-15 and MET-16 hold (no
weight; the competition's Gini is unweighted); MET-1 to MET-4 hold (the scorer equals the Gini on the amount, a constant
scores 0). Value: TP-2, a small signal: untuned LightGBM scores 0.106 / 0.091 / 0.061 on the shipped folds against 0 for
the dummy (random predictions SD 0.023 to 0.025), 0.022 to 0.106 over nine folds; the task probe flags `no_signal` and
`unstable`, which read an R^2-type skill (EV-3), and on the declared Gini its LightGBM beats the dummy on 3 of 3 splits
(+0.037, SE 0.004, sides capped at 200,000 rows). Quality: the notes' wrong statements are fixed; `OrdCat` stays
categorical (settled). Weighed: Allstate's own competition +, a real pricing task +, 2.75M renewal rows (above the row
budget) +, an undisclosed adjustment -, a weak signal -, no exposure and no dates -, new business untested -. Nothing is
left to decide.

Changes made after the review panel (AI, 2026-11-01):

- The 2007 rows are dropped; `Calendar_Year` stays a feature (two years; the model's pooled score exceeds its score
  within each year by at most 0.001 on the rebuilt folds).
- `household_vehicles` is dropped, and `Vehicle` stays dropped.
- Cat10, Cat11 and Cat12 are dropped: the same vehicle keeps its value from one year to the next only as often as a
  random redraw would, and they relate to no other column or the claim (Cramér's V at most 0.0024).
- `OrdCat` is categorical; its claim rates over the levels (0.11% to 0.82%) show no risk order.
- `fit_reason` and the notes name what the folds do not test: next year's book (53% of it known households, whose
  claim history matters), new vehicle series, and complete rows only (the application has no missing values; 73% of
  the shipped rows have one). They also say that no exposure is published and some rows are part years.
- The notes are corrected where the data contradicted them (the LEAK-30 evidence, the level counts, the share of
  repeated feature rows) and every score is restated from the rebuilt folds, with the test that missingness carries
  no outcome beyond the vehicle type.
- Record, at hand-over (no mark needed): the Assessment's "Exposure: none (rows are vehicle-years)" now says none is
  published and some rows are part years.

Changed on Andrej's marks of 2026-11-03: the rows are the vehicle-years of 2006 with the 2005 history as counts (issue
3, B, "2006 renewal book"), so 2005 no longer ships as rows and `Calendar_Year` left with its single value; 2007 stays
dropped (issue 2), the Gini regression stays (issue 4), households are drawn and dealt to the folds at random (issue 5).

Changes made on 2026-11-06 (AI, under the exposure rules; no re-review panel): an exposure paragraph in the notes (the
release has no exposure; the vehicle-years are partly cut by claims; the in-year vehicle count, which the outcome cuts,
stays dropped; the competition's Gini is unweighted, so no weight is declared). The re-review panel waited for the
competition's files, which download only after its rules are accepted on Kaggle
(https://www.kaggle.com/competitions/ClaimPredictionChallenge/rules); it ran on 2026-11-08 (below).

Changes made after the re-review panel (AI, 2026-11-08), text only (rows, features, target, split and metric
unchanged; the task summary's `row`, `known` and `fit_reason` wait for issue 6): the notes give the part years as
measured, about 38% of the rows (the cars that joined during 2006: 27.4% new households, 10.7% cars added by a household
of 2005), which claim per row at about half their own 2007 rate at every model-year age, with 2007 showing the same,
where they had said 1.4% (the cars of model year 2007, now named as the latest of them); the exposure paragraph names
the group of its 1.40% / 0.73% figure (cars insured since 2005 whose household continued into 2007: 1.39% against
0.72%) next to the figure for all 2006 cars (0.96% against 0.60%), bounds the share cut short (at most 32.5% of the
2006 cars are not seen in 2007, 9.0% left a household that stayed, 13.3% of the carried cars of continuing households
are gone) and says why the target stays per contract for these cuts; the history bullet and decision 1 say that the
new households' 0.50% and part of the history's lift measure the shorter term, not the claim record alone. `dataset
check`: 0 errors, 0 warnings. The record marks its part-year statement of 2026-10-30 superseded.

Changed on Lennart's marks of 2026-11-08: the rows are the 2006 renewal book, the 2,754,936 cars insured in 2005 too
(61.9% of the 4,447,729 vehicle-years of 2006; issue 6, B), filtered in `_clean` after the history is built and before
the sampling; `vehicle_insured_2005` left as constant and the history is never missing. `row`, `known`, `changes`,
`fit_reason`, the question, the notes, decision 1 (now with the same cars' 2007 rate) and the splits comment restate the
book's numbers. `household_vehicles_carried`, which had lowered the score on all rows, now adds +0.001 to +0.009 on 3 of
3 folds and stays. The exposure paragraph gives the cuts by claims on the book and names the confirmation of issue 7
(A). `dataset check`: 0 errors, 0 warnings.

Changed on Andrej's marks of 2026-11-09 (issues 8 and 9, both A, as implemented), text only: the splits comment gives
the 2005-to-2006 score of 0.064 as above the household folds of that build and adds the training side's year and the
maturity of its amounts; the notes carry both decisions as CC lines and list the columns held only for training rows,
which stay out (the cross-dataset item of 2026-11-09). `dataset check`: 0 errors, 0 warnings.

**Main points:** Nothing open. Resolved on 2026-11-09 (Andrej), from the information audit of that day: the folds keep
testing on all rows, gaps kept as missing (8), and the split stays by household, the training side's year and maturity
named in the splits comment (9). Resolved on 2026-11-08 (Lennart): the rows are the 2006 renewal book,
only the cars on the policy at the start of the year (6), and the target stays per contract where a claim ends the cover
(7). Resolved on 2026-11-03: 2007 stays dropped (2), the 2006 renewal book with the 2005 history (3), the Gini
regression (4), households at random (5); verdict ship (2026-11-03).

**Issues for Andrej and Lennart:**

2. **Drop the 2007 rows, or keep them and drop only `Calendar_Year`?**

   * **Problem:**
     - Bodily-injury claims are paid over years, and the release gives no date at which the amounts were read.
     - In 2007, the newest year, the claim rate and the median claim match the earlier years but the large claims are
       missing, as with unsettled claims.
     - Drop 2007, or keep it?
   * **Background:** claims above 2,000 are 0.43% of claims in 2007 against 1.31% and 1.26% in 2005 and 2006, in
     every vehicle-age band and each of the three largest makes, and the shortfall grows toward the tail (2007
     against 2005: 1.01 at the median, 0.59 at the 99.9th percentile). A target cut short in the newest period is cut
     where follow-up is complete[^2a].
   * **Effect on the task:** the test folds mixed three years, so a model gained by learning each year's claim level
     from other households of the same year. Before the drop, a predictor that knew only the year scored 0.055 to
     0.058, as much as the probe model on two of three folds. The metric has to match the real task: the competition
     scored one year at a time, and a rating for next year has no year to rank[^2b].
   * **Experiments:** on the rebuilt folds the model's pooled score exceeds its score within each year by -0.000 to
     +0.001, so the bonus is gone; a year-only predictor scores 0.001 to 0.026, within about one spread of random
     predictions. Dropping only `Calendar_Year` left +0.001 to +0.003, positive in 8 of 9 runs, as the year stays
     readable through other columns. The drop costs no rows of the budget (8.5M rows remain for the 1.5M sample),
     and in the mediator's sample no measurable score. On the rebuilt folds the score fell to 0.053 / 0.054 / 0.022,
     of which the drop of issue 3 explains 0.015 to 0.020 and fold-to-fold noise the rest (issue 4). In the
     mediator's experiment (same changes, its own 1.5M sample) the model scored 0.050 / 0.089 / 0.050 after the drop
     against 0.072 / 0.052 / 0.040 with 2007 kept and the year column dropped.
   * **Panel:** against the drop, the critic notes that Allstate scored 2008 and 2009, years younger than 2007 is
     here, and that a step at 2007 with no change between 2005 and 2006 fits a change in Allstate's adjustment as
     well. The domain practitioner would keep 2007 with a year factor.
   * **Unknown:** whether the step is unsettled claims or a change in Allstate's adjustment; no date can settle it.
   * **Consistency:** follows sf_permit_time (cut where follow-up is complete). It departs from the reading
     recommended for frempl issue 3 (keep amounts of unknown valuation date); what sets it apart is a shortfall
     measured across years and a cut that costs no rows of the budget, where frempl has one year.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Drop 2007, keep `Calendar_Year` (implemented) | rows of 2005-2006 only; the year stays a feature | the test folds no longer reward knowing each year's claim level; cut where follow-up looks complete; no rows of the budget lost | the newest labelled year is lost |
     | B | Keep 2007, drop `Calendar_Year` | rows of all three years; the year column dropped; the tail figures in `fit_reason` | keeps the newest year; fits the critic's reading of the step | knowing the year still adds a little (+0.001 to +0.003); 2007's large claims stay short |

   * **Recommendation:** A, keep the drop: the shortfall is measured across years and the cut costs no rows of the
     budget. **Decision:** drop 2007 (A), or keep it without `Calendar_Year` (B)?

   **Notes for the AI:** on B, keep 2007, drop `Calendar_Year`, and record "LEAK-24 not shown violated" with the tail
   figures in `fit_reason`.

   **Andrej (2026-11-03, ok):** We can drop 2007 because we still have 1 million of samples and the current limit is
   1M. We might reconsider this decision for a future version.

   **Resolved (2026-11-03, Andrej):** (A), 2007 stays dropped and `Calendar_Year` stays a feature; to reconsider in a
   future version. The drop rests on the unsettled 2007 claims and the year bonus, not on the row limit: 2007 can
   come back with settled amounts (re-sourced) or a test that shows the shortfall gone, as keeping it without
   `Calendar_Year` still left +0.001 to +0.003 from knowing the year. Recorded in the record's CC line.

   [^2a]: **LEAK-24** (Must): a target right-censored in the newest periods (a duration or a final status cut by the
     download date) is cut where follow-up is complete, or re-sourced from an archive with settled labels.
   [^2b]: **MET-2** (Must): match the data, the metric and the real task; the metric's unit of evaluation has to
     exist in our data.

3. **Drop `household_vehicles`, or replace it by the household's vehicle count of the previous year?**

   * **Problem:**
     - Our feature `household_vehicles` counts the household's vehicles insured at any time in the calendar year, so it
       includes cars added after the rating, among them replacements after the row's own crash.
     - Drop it, or use the household's count of the previous year?
   * **Background:** we built `household_vehicles` to replace the source's `Vehicle`: the household's vehicles
     insured in the calendar year. But the file lists every vehicle insured at any time in the year. Vehicles already
     insured the year before claim at 1.17% in a year when the household's count rose, and at 0.72% otherwise; in
     years with a short-lived extra car the rate is 0.98% against 0.72%. A feature may hold only what existed at the
     prediction point[^3a], and late values that cannot be located row by row go when they may carry a gain, a
     case-by-case call of yours[^3b].
   * **Effect on the task:** on the earlier folds the column added 0.015 to 0.020 Gini, about a quarter of the score.
   * **Experiments:** the drop takes part of the signal: the third rebuilt fold now scores within the noise of chance
     (issue 4), and the mediator's sample with the same changes scored 0.050 to 0.089, so fold-to-fold noise does the
     rest. The previous year's count kept +0.006 to +0.013 on three years.
   * **Consistency:** the pricing_game_2017 count it cited comes from a start-of-year policy file, so that precedent
     does not carry. The drop follows kick and 2_month_survival_rate_prediction.
   * **Panel:** the advocate and the critic accept either.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Drop (implemented) | `household_vehicles` dropped; `Vehicle` stays dropped, as it carries the same count | no count from after the rating | takes part of the signal; the third fold is within the noise of chance |
     | B | The previous year's count | the household's vehicle count of the previous year as a feature | known at the rating, built without labels; kept +0.006 to +0.013 on three years | with 2007 dropped, missing for every 2005 row (47.5%) and every new household |

   * **Recommendation:** A, keep the drop: the count includes cars added after the rating, and the previous year's
     count would be missing for 47.5% of the rows. **Decision:** drop (A), or the previous year's count (B)?

   [^3a]: **LEAK-10** (Must): a feature holds only what existed at the prediction point and never gives the target
     away.
   [^3b]: **LEAK-10**, clause amended 2026-10-26 (Lennart), a case-by-case judgment of the curator, never a default:
     a value read at a later pull goes where its late cells can be located (they are blanked); where they cannot be
     located row by row, the values go when they may carry a gain, and stay with a note only when the part that can
     be traced shows none.

   **Andrej (2026-11-03, discuss):** Can't we just make the assumption that the added cars are known at rating time?
   Or can we find out added cars somehow?

   **Answer (AI, 2026-11-03):**

   * **Problem:**
     - The count can't be assumed known at rating, because it rises after the household's own crashes.
     - Cars added during the year can't be found either, since the file has no dates within a year.
     - What can be found is which cars were already insured the year before, and that is known at rating.
   * **Background:**
     - The assumption would hold for the cars on the policy at the renewal. But the whole-year count also counts
       cars added later, and those include replacements after the row's own crash.
     - Measured on 2006: a car already insured in 2005 claims at 1.05% in a year when its household's count rose,
       and at 0.77% when it did not. So the count carries part of the outcome, and assuming it known would ship
       that link[^3c].
     - `Vehicle` numbers are not stable across years (data page), but a car can be matched to the year before by
       household, model year and submodel: 61.9% of the 2006 rows are cars insured in 2005 too.
     - 2005 is the first year of the file, so its rows (47.5% of the shipped rows) have no year before.
   * **Experiments:** rows of 2006, households split in half, untuned LightGBM, one split (random predictions: SD
     0.013), normalized Gini on the amount:

     | Features | Gini |
     |---|---|
     | shipped | 0.075 |
     | + the whole-year count and `Vehicle` (your assumption) | 0.080 |
     | + the previous year's count and the count of cars carried over from it | 0.086 |

     The counts known at rating carry at least as much as the whole-year count, without the link to the outcome.
     The earlier panel measured +0.006 to +0.013 for the previous year's count on three years.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Drop (implemented) | no household count | nothing from after the rating | loses a signal an insurer has at renewal |
     | B | Counts known at rating | the household's count of the previous year and the count of its cars carried over from it, as features | known at the renewal, built without labels; +0.011 here | missing for every 2005 row (no year before) and every new household |
     | C | Assume the whole-year count known | `household_vehicles` back as a feature | what Kaggle's players had | the count rises after the household's crashes, so it carries part of the outcome |

   * **Recommendation:** B: it keeps what an insurer knows at the renewal and leaves out what happens after it. A
     new household with no count is also the real case for new business. **Decision:** A, B or C?

   **Notes for the AI:** on B, build `prev_year_vehicles` (rows of the household in the previous calendar year) and
   `carried_vehicles` (this year's cars of the household matched to the previous year on household, model year and
   submodel) in `_clean` from the raw file before the sampling, missing where no previous year exists; a bullet with
   the 1.05% against 0.77% figure; re-run `dataset check` and the leak probe.

   [^3c]: **LEAK-10** (Must): a feature holds only what existed at the prediction point and never gives the target
     away.

   **Andrej (2026-11-03, discuss):** If the count is missing for every 2005 row, would it make sense to only use 2006
   households because we would also be able to sample 1.5 million samples from this year?

   **Answer (AI, 2026-11-03):**

   * **Problem:**
     - Yes: 2006 alone has 4.45 million vehicle-years, so the 1.5 million rows can all come from 2006, with 2005 as
       the history an insurer holds at the 2006 renewal.
     - Every row then has the history features (missing only for the 27% of rows whose household is new, the real
       case for new business), and the year column goes.
     - This also answers issue 4 (the claim history) and your general note (what an insurer knows at the rating).
   * **What an insurer knows at the 2006 renewal, from this file:**
     - The vehicle's and the policy's characteristics (as now).
     - Whether the household was insured in 2005, its vehicle count in 2005, and how many of this year's cars were
       already insured then; whether this car was insured in 2005.
     - The household's and this car's claim counts of 2005, and the 2005 claim amounts as paid so far.
     - Not usable: the whole-year count of 2006 (it rises after the household's own crashes, issue 3), and the 2005
       amounts as the file gives them, read years later, so larger than what the insurer saw at the renewal[^3d].
   * **Experiments:** rows of 2006, 1.5 million rows of whole households drawn at random, three folds by household,
     untuned LightGBM on log1p (random predictions: SD 0.019 to 0.032 per fold):

     | Features | Gini on the amount | Claim yes/no ranking |
     |---|---|---|
     | vehicle and policy only | 0.104 / 0.053 / 0.025 | 0.116 / 0.112 / 0.117 |
     | + the 2005 history, counts | 0.101 / 0.046 / 0.021 | 0.126 / 0.134 / 0.137 |
     | + the 2005 history, counts and amounts | 0.105 / 0.060 / 0.026 | 0.127 / 0.135 / 0.142 |

     - The history ranks claims better on every fold (+0.010 to +0.022).
     - On the amount the change stays within the noise: a few large claims decide that score (issue 4).
     - The 2006 claim rate is 1.50% for a household that claimed in 2005, 0.78% for a known household without a
       claim and 0.50% for a new household.
   * **Unknown:** the rating date within the year is not published, so a 2005 claim reported after an early 2006
     renewal counts as known; the share of such claims cannot be measured.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | 2005 and 2006, no history (implemented) | as now | two years of rows | no history; the insurer's main renewal signal untested |
     | B | 2006 renewal book with the 2005 history (counts) | rows of 2006 only; the six history features above; `Calendar_Year` goes | every input known at the renewal; history for 73% of rows | one year of rows; the 2006 renewal date unknown |
     | C | B plus the 2005 claim amounts | B, and the household's 2005 claim amount | slightly higher scores | the amounts were read years after the renewal; an insurer saw less |

   * **Recommendation:** B: it is the task as an insurer meets it at renewal, and it leaves out the 2005 amounts,
     which the file gives at a later valuation than the insurer had. **Decision:** A, B or C?

   **Notes for the AI:** script and log `renewal_2006.py` / `.log` in the run folder of 2026-11-03 (allstate/). On B:
   the history built in `_clean` from the 2005 rows before the sampling (vehicles matched on household, model year
   and submodel), missing where the household is new; `required_split` and tag unchanged (still forced from
   temporal: one labelled target year); rewrite the task summary, the notes and the decisions; re-run `dataset check`
   and the leak probe.

   [^3d]: **LEAK-10** (Must): a feature holds only what existed at the prediction point; a value read at a later pull
     goes where it may carry a gain.

   **Andrej (2026-11-03, change):** I go with your recommendation of 2006 renewal book with the 2005 history (counts)

   **Resolved (2026-11-03, Andrej):** B. The rows are the 4.4 million vehicle-years of 2006, 1.5 million of whole
   households sampled; five columns from 2005 (the household's vehicles and claims, its cars carried over, whether
   this car was insured and its claims), the 0/1 flag categorical; `Calendar_Year` goes; the 2005 amounts stay out,
   because bodily-injury amounts grow for years after the renewal. The split stays by household, forced from
   temporal with one target year. `dataset check` gives 0 errors and 0 warnings; the leak probe on the shipped folds
   finds no feature that scores alone (all at or below the mean on log1p R^2), and 33.9% of the test rows have an
   exact feature copy in training, against 84% before the history set households apart.

4. **Keep the regression scored by the competition's Gini, although one of the three folds scores within the noise of
   a random prediction?**

   * **Problem:**
     - After the drops of issues 2 and 3, untuned LightGBM scores a normalized Gini of 0.053 / 0.054 / 0.022 on the
       three folds, and the third is about one standard deviation above random predictions.
     - Keep the competition's Gini regression, or switch to a claim classification scored by ROC AUC?
   * **Background:** the normalized Gini scores how well the predictions order the vehicle-years by claim amount (1
     a perfect order, 0 a random one). On the rebuilt folds random predictions average -0.002 to 0.004 with a
     standard deviation of 0.019 to 0.025 over draws, so the third fold is about one standard deviation above chance
     and the other two more than two. The panel judged the signal on stronger numbers (0.096 / 0.051 / 0.058 before
     the changes); dropping `household_vehicles` (issue 3) and 2007 (issue 2) lowered it.
   * **Effect on the task:** with a standard error of 0.022 to 0.029 per fold, two methods must differ by about 0.03
     before three folds tell them apart[^4a], and on a fold like the third a method's score is mostly noise.
   * **Experiments:** the signal is real, and a small but real signal is no reason to retire[^4b]: a regularised
     classifier of whether a claim occurs ranks the amounts above chance on every fold (0.065 / 0.060 / 0.039);
     trained on 2005 and scored on 2006, the rebuilt rows reach 0.064; the three folds' mean, 0.043, is three to four
     times the spread of a random three-fold mean.
   * **Unknown:** no tuned results exist yet, and a flag is checked against the benchmark's tuned methods before
     acting on it[^4c].
   * **Consistency:** pricing_game_2016_french_fleet became a claim classification scored by ROC AUC on 2026-10-30,
     on your question, because its claim amounts carried no signal. Here too the amount among claimants carried none
     (R^2 below 0 on the folds before the changes), and a claim classifier ranks the amounts better than the
     regression on every rebuilt fold. What sets this one apart: Allstate fixed the Gini on the amount for its
     competition, and a competition's metric is declared[^4d]; pricing_game_2016's source fixed no metric.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Gini regression (implemented) | target the claim amount as log1p, scored by the Gini on the amount; the noise stated in the notes | the competition's metric; keeps the claim size | one fold within the noise of chance; methods must differ by about 0.03 |
     | B | Claim classification by ROC AUC | target: whether a claim occurs (yes/no), scored by ROC AUC | standard error about 0.005 per fold (the blind reviewer's estimate; its proposal) | drops the claim size the competition scored; departs from the competition's metric |

   * **Recommendation:** A, as the competition's own metric on a signal that is real, and revisit when tuned results
     exist (reframe if tuned methods do not beat a random prediction on every fold). **Decision:** keep the Gini regression (A), or a claim classification (B)?

   **Notes for the AI:** the revisit is under TP-1, once tuned results exist; B departs from MET-4.

   [^4a]: **MET-10** (Weigh): the factors on a borderline call between the source's metric and the fallback, among
     them the source's track record (a competition first) and the metric's resolution on our folds.
   [^4b]: **TP-2** (Should): a small but real signal is no reason to retire, and neither is a cutoff on the best
     skill.
   [^4c]: **TP-1** (Must): a flag is a question, not a verdict; the probes fit untuned models, so every flag is
     checked against the benchmark's tuned methods before acting on it.
   [^4d]: **MET-4** (Should): a competition's leaderboard metric is the source's metric and is declared; it is
     overruled only by MET-2 or on evidence that it is biased or wrong for the use case.

   **Andrej (2026-11-03, discuss):** I am leaning towards A, but first explain to me why the reported competition
   results on the kaggle leaderboard are so much better than the ones that you report here

   **Answer (AI, 2026-11-03):**

   * **Problem:**
     - The final leaderboard reads 0.2016 (Matt C), 0.1955 (Owen) and 0.1698 (third), with the tenth at 0.1385, against
       0.022 to 0.054 on our folds.
     - Most of the gap is likely the claim amounts of Kaggle's test years, not better models: the Gini on the amount
       drops sharply when a few large claims dominate.
     - Kaggle's test years were newer than 2007, whose large claims were already missing.
   * **Background:**
     - The Gini on the amount weighs each claim by its size. One large claim the model did not rank high costs as
       much as many small ones ranked well.
     - Kaggle scored 2009 (the private board), two years newer than 2007. On 2007, the newest labelled year, the
       claims above 2,000 were a third as frequent as in 2005-2006 (issue 2). If 2009's amounts were read as early,
       their tail was shorter still, and the score moves toward that of a claim yes/no ranking.
     - Kaggle's players also had information our folds leave out: the household's claims of earlier years (53% of
       the test households were in the training file) and the household's whole-year vehicle count (issue 3).
     - Huangfu (2015), with a temporal holdout on 2007 and no ensembles, reached 0.080: our level, not Kaggle's.
   * **Experiments:** rows of 2006, households split in half, one untuned LightGBM, one split (random predictions:
     SD 0.013). The same predictions, scored against different versions of the target:

     | Features | Amount | Amount capped at the 99th / 90th / 50th percentile of claims | Claim yes/no |
     |---|---|---|---|
     | shipped | 0.075 | 0.083 / 0.103 / 0.131 | 0.147 |
     | + Kaggle's extra information (whole-year counts, claim history) | 0.091 | 0.101 / 0.118 / 0.149 | 0.170 |

     - The extra information adds 0.016.
     - A shorter tail adds up to 0.07: on a target of claims without their size, the same model scores 0.147.
     - Tuning and ensembles are the rest (the top teams blended many models). Our folds are lower again (0.022 to
       0.054) because they train on 1M rows, not 2.2M.
   * **Unknown:** the 2008 and 2009 amounts were never published, so how short their tail was cannot be
     measured; the explanation rests on the 2007 shortfall and this experiment.
   * **Effect on the decision:** the Gini on the amount is the competition's metric, but on settled amounts it is
     noisier than Kaggle's numbers suggest. That is the weakness option B answers: a claim yes/no target scores
     about twice as high and much more stably. A still scores what Allstate asked for.
   * **Recommendation:** unchanged, A, as you lean, and revisit when tuned results exist. **Decision:** A (Gini on the
     amount) or B (claim yes/no by ROC AUC)?

   **Notes for the AI:** the experiment's script is in the run folder of 2026-11-03 (kaggle_gap.py, kaggle_tail.py);
   on A, add the leaderboard comparison to `fit_reason` in two sentences.

   **Andrej (2026-11-03, discuss):** If the household's claims of earlier years play such a big role, why do we not
   use it? I feel like you did not think this task through.

   **Answer (AI, 2026-11-03):**

   * **Problem:**
     - You are right: the claim history is what an insurer prices a renewal on, and we left it out because the 2005
       rows had no year before, instead of making 2006 the year we predict.
     - Issue 3's option B now builds the history from 2005 for rows of 2006: the household's and the car's claim
       counts, whether each was insured, and the vehicle counts.
     - It ranks claims better on every fold, but on the amount the gain stays within the noise.
   * **Experiments:** see issue 3 (claim yes/no ranking 0.112-0.117 without the history, 0.126-0.137 with it; the
     Gini on the amount 0.025-0.104 either way).
   * **Effect on this issue:** the Gini on the amount stays noisy with or without the history (one fold at 0.021 to
     0.026 again), because a few large claims decide it. Issue 5 asks whether sampling more claims should fix that.
   * **Recommendation:** unchanged, A (the competition's Gini on the amount), now on issue 3's B. **Decision:** A or
     B?

   **Andrej (2026-11-03, discuss):** Let's go with A

   **Resolved (2026-11-03, Andrej):** A, the competition's normalized Gini on the amount, the regression on log1p.
   `fit_reason` and the notes now give the leaderboard comparison; the revisit once tuned results exist stays.

5. **Sample more households with claims than random sampling gives?**

   * **Problem:**
     - Of the 4.45 million vehicle-years of 2006 we can ship 1.5 million, and a random draw of households keeps
       0.71% claims, about 3,500 per test fold.
     - A draw that takes every household with a claim first triples the claims, but the test folds then stand for a
       book with three times the real claim rate.
   * **Effect on the task:** the Gini on the amount is the share of the claim cost each prediction ranks at the top;
     with more claims among fewer zeros it weighs the order among claims more and the order of claims above
     no-claims less, so its value means something other than on the book[^5a].
   * **Experiments:** rows of 2006, 1.5 million rows, three folds by household, untuned LightGBM:

     | Sample | Claims per test fold | Random predictions SD | Gini, vehicle and policy only | Gini, + history counts |
     |---|---|---|---|---|
     | households at random | 3,505-3,572 (0.71%) | 0.019-0.032 | 0.104 / 0.053 / 0.025 | 0.101 / 0.046 / 0.021 |
     | every claim household, then random ones | 10,491-10,621 (2.11%) | 0.011-0.014 | 0.064 / 0.053 / 0.075 | 0.073 / 0.065 / 0.091 |

     - The enriched folds are about twice as stable, and the history's gain shows above their noise.
     - The enriched sample takes whole claim households, so a household with a claim also brings its cars without
       one: the no-claim rows over-represent households that claimed.
   * **Consistency:** every sub-sampled version so far keeps the natural rate (whole groups at random, or rows
     stratified on the target), so the test folds stand for the source's population[^5b].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Households at random (implemented) | the natural claim rate in train and test | the scores stand for the real book; as every other sub-sampled version | about 3,500 claims per test fold; noisy Gini on the amount |
     | B | Every claim household first | all 31,690 claims of 2006, then random households to 1.5 million rows | three times the claims; half the noise | test folds at three times the real claim rate; no-claim rows biased toward claim households; the metric means something else |

   * **Recommendation:** A: a benchmark's test folds should stand for the population the model is used on, and a
     model that wants more weight on claims can reweight its own training rows. B's gain in stability is real, so it
     is the option if you value telling methods apart above the natural rate. **Decision:** A or B?

   **Notes for the AI:** the second half of the note is answered by issue 3's answer (option B). The experiment is
   `renewal_2006.py` in the run folder of 2026-11-03. On B: a custom sampling, not `subsample_frame`; state it in
   `version_comment`.

   [^5a]: **MET-2** (Must): match the data, the metric and the real task; the metric means on our task what it meant
     on the source's: same target, same classes, same class balance.
   [^5b]: definitions.md, "Larger than the row budget": a larger frame is sub-sampled to 1.5M rows, rows stratified
     on the target or whole groups.

   **Andrej (2026-11-03, discuss, on the dataset):** One independent point, if we have so much data and do sampling
   here, would it make sense to sample more of the samples with claims than we get with random sampling? I believe
   you did not think this task through. Make it as realistic as possible using all available information that an
   insurance company would have at train and test time points.

   **Andrej (2026-11-03, discuss):** I would suggest the following:
   - Use three splits
   - First do three fold CV on households with claims such that they are randomly distributed across the three folds.
   - Then do 3-fold CV where we randomly distribute the non-claimed households

   **Answer (AI, 2026-11-03):**

   * **Problem:**
     - Dealing the claim households evenly over the three folds, then the others at random, keeps the natural claim
       rate and changes only which fold a household lands in.
     - Measured on the 2006 renewal book, it does not make the folds steadier, because a random deal already gives
       every fold about the same number of claims and the same share of the claim cost.
     - If you meant it together with taking every claim household first (option B above), the stability comes from B's
       sample, and the even deal adds nothing to it.
   * **Experiments:** 1.5 million rows of 2006 drawn as shipped (10,687 claims), the 2005 history as features,
     untuned LightGBM, three seeds of three folds each, normalized Gini on the amount:

     | How households go to the folds | Claims per test fold | Share of the claim cost | Gini over 9 folds: mean, spread (SD), range |
     |---|---|---|---|
     | at random (implemented) | 3,456-3,669 | 0.320-0.356 | 0.070, 0.019, 0.046-0.103 |
     | claim households spread evenly (your proposal) | 3,510-3,630 | 0.313-0.347 | 0.064, 0.025, 0.028-0.101 |
     | spread evenly by claim size (none, small, medium, top 10%) | 3,488-3,681 | 0.309-0.360 | 0.067, 0.017, 0.049-0.099 |

     - All three spreads are the same within their own noise, so the Gini's noise comes from how the model ranks a
       few large claims, not from how many claims a fold holds.
   * **Effect on the task:** stratifying needs a household label built from the target in the frame, which may not ship
     as a feature; the library would need a way to stratify on a column it then drops[^5c].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Households at random (implemented) | natural claim rate; households dealt to folds at random | the scores stand for the real book; as every other sub-sampled version | about 3,500 claims per test fold; noisy Gini |
     | B | Natural sample, claim households dealt evenly | your proposal on the shipped sample | claims per fold equal by design | no steadier folds (spread 0.025 against 0.019); needs a library change |
     | C | Every claim household first, dealt evenly | all 31,690 claims of 2006, then other households to 1.5 million rows | half the noise (random predictions 0.011-0.014 against 0.019-0.032) | test folds at three times the real claim rate; no-claim rows biased toward claim households |

   * **Recommendation:** A: the even deal brings no stability on the real book, and C buys its stability with a book
     three times as claim-prone as Allstate's. **Decision:** A, B or C?

   **Notes for the AI:** script and log `stratified_folds.py` / `.log` in the run folder of 2026-11-03 (allstate/).
   On B or C: `stratify_on` takes a column of the frame, and `feature_columns` would ship it; add a non-shipped
   stratification key to the library first.

   [^5c]: **LEAK-10** (Must): a feature never gives the target away; the house check `task_stratify_*` takes only the
     target or a discrete feature.

   **Resolved (2026-11-03, Andrej):** A, households drawn at random and dealt to the folds at random, as implemented.
   Verdict: ship.

6. **Keep only the cars on the policy at the start of 2006, or all rows as an exception?**

   * **Problem:**
     - About 38% of the 2006 rows are cars that joined during the year (a new household's car, or a car a household of
       2005 added), so they were on risk for about half of it, and the target, the year's payments per row, prices
       that part year.
     - Their start date is not released and neither is any time on risk, so no rate per year insured can be built,
       and the flag `vehicle_insured_2005` (0 for these cars) stands in for how long a row was on risk.
     - Keep only the cars already insured in 2005, the renewal book the prediction point describes, or keep all rows
       as an exception to the rule that a target per row needs the same planned term on every row?
   * **Background:**
     - The cars that joined in 2006 and stayed into 2007 claim per row in 2006 at 0.45 to 0.59 times their own 2007
       rate, in every band of model-year age (0.31 to 0.35 for model year 2007); the cars carried from 2005 claim at
       0.91 to 1.11 times theirs.
     - In 2007 the same cars claim more than the carried ones, so they are not lower risks, and one year later the
       shares and rates come back (2007: 64.0% carried at 0.81%, 10.5% added at 0.63%, 25.4% new households at 0.53%).
     - A target per row is right only when the planned term is the same on every row and known at the prediction
       point; otherwise the amount ships as a rate per year on risk, weighted by that time[^6a]. That rate needs an
       exposure this release does not have, so the mildest remedy left is a filter of the rows, before a documented
       exception[^6b].
     - The notes had put the part years at 1.4% of the rows (the cars of model year 2007 alone); they now give the
       38%.
   * **Effect on the task:** about half of the score comes from guessing how long a row was on risk, which an insurer
     knows when it writes the cover; a model is rewarded for reading `vehicle_insured_2005` and the missing 2005
     history as a short year, not as a lower risk.
   * **Experiments:** the shipped folds, untuned LightGBM (L2 on log1p), the declared Gini, by fold (column auditor):

     | Features and rows | Fold 0 | Fold 1 | Fold 2 |
     |---|---|---|---|
     | `vehicle_insured_2005` alone, all rows | 0.046 | 0.050 | 0.052 |
     | all features, all rows (as shipped) | 0.087 | 0.102 | 0.058 |
     | the same model, scored on the carried test rows only | 0.065 | 0.062 | 0.018 |
     | trained and tested on the carried rows | 0.063 | 0.057 | 0.003 |

     - The last row trained on about 0.62M carried rows of the current sample; a rebuilt sample would hold about 1.5M,
       so the renewal book's signal has to be measured again after the change, tuned models included.
     - The ratios of the background are the mediator's test on the full file of 2005 to 2007, by band of model-year
       age; the column auditor's own run on the cars that continue gives the same (0.46 new households, 0.54 added
       cars, 0.98 carried).
   * **Consistency:** spanish_motor_insurance_2015_2018 kept a target per contract because every planned term was one
     year, known when the contract was written; here 38% of the rows have no such term, so that case does not cover A.
     australian_vehicle_insurance_2004_2005 shipped the rate weighted by the time observed, which this release cannot
     give. Rows may not be selected by the realized time on risk, such as full-year rows only[^6c]; B selects on a fact
     of 2005 known at the rating, and never on whether the car is seen in 2007.
   * **Panel:** the column auditor recommends B, as it matches the declared prediction point and the rule for a target
     per row; the claim auditor found no feature carrying a realized term and no weight due, so it judged the ship to
     stand, but it did not test the 38%, which the mediator's test settled for the column auditor.
   * **Unknown:** the renewal book's signal once rebuilt and tuned; one untuned run gave 0.003 on one fold, and a
     small but real signal is no reason to retire[^6d].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | All rows (implemented) | as now, with an exception recorded (no exposure or start date is released, so no rate can be built); `row`, `known` and `fit_reason` say that 38% of the rows are new business of unknown start | keeps new business and the larger pool; no rebuild | about half the score is the term marker; the target prices part years for 38% of the rows; the use case says renewal |
     | B | The renewal book | only the cars insured in 2005 too (about 2.75M rows, 1.5M sampled); `vehicle_insured_2005` dropped as constant; the 2005 history never missing; task summary, notes and decision 1 rewritten; rebuilt and probed again | every row a full year from the 2006 renewal, as the prediction point says; meets the rule for a target per row; matches your "2006 renewal book" of 2026-11-03 | a smaller signal (0.003 to 0.063 in one untuned run); new business untested; a rebuild |

   * **Recommendation:** B, the mildest remedy that works: it makes the rows what the task already says they are, and
     its smaller signal is measured again rather than kept up by the part years. **Decision:** all rows as an
     exception (A), or the renewal book (B)?

   **Notes for the AI:** the mediator's issue 1 of the re-review of 2026-11-08 (MET-14, Should, applies USE-5, Must);
   its option (a) is B here, its (b) is A. On B: in `_clean`, after the history is built and before the sampling, keep
   `vehicle_insured_2005 == 1` (never presence in 2007); drop `vehicle_insured_2005` (constant) from the frame and
   `_feature_types`; rewrite `task_summary` (`row`, `known`, `changes`, `fit_reason`), the history and part-year
   bullets, decision 1 (its table and text) and the splits comment's numbers; re-run `dataset check`, the task probe
   and the leak probes on the rebuilt folds; re-measure `household_vehicles_carried`, which lowered the Gini on 3 of 3
   folds (-0.004 to -0.009) in the claim auditor's run. On A: `**Exception to MET-14 (2026-11-08, <curator>):** no
   exposure and no start date are released, so no rate per year can be built for the 38% of rows that joined during
   2006. Serves USE-5: an insurer acts on a calendar-year cost that includes new business of unknown start.` into the
   record and the notes, a Cases row of kind `exception` under MET-14 (the main session's), and the 38% with the flag's
   score alone (0.046 to 0.052) in `row`, `known` and `fit_reason`. Scripts in the run folder 2026-11-06_exposure_review
   (allstate panel): decisive.py (mediator), term.py and gain.py (column auditor).

   [^6a]: **MET-14** (Should; applies USE-5, Must; amended 2026-11-08, Lennart): a count or amount accrued over a
     varying time on risk ships as the rate per unit, weighted by that time; a per-contract target stays when the
     planned term is constant and known at the prediction point and the data record each contract to its end.
   [^6b]: principles.md, the remedy ladder: repair from the origin; fix the definition (drop, lag, filter, re-split,
     re-target); keep it with a documented note (an exception, which departs from a Should for one dataset and names
     the fact that sets the case apart and the higher principle it serves); exclude.
   [^6c]: **LEAK-41** (Must; 2026-11-06, Lennart): no model is trained or scored on rows selected by the realized
     weight (such as full-year rows only).
   [^6d]: **TP-2** (Should): a small but real signal is no reason to retire, and neither is a cutoff on the best skill.

   **Lennart (2026-11-08, change):** Option B: The renewal book.

   **Resolved (2026-11-08, Lennart):** B, the renewal book: only the cars insured in 2005 too stay (2,754,936 of the
   4,447,729 vehicle-years of 2006, 1.5M of whole households sampled), selected on a fact of 2005 and never on presence
   in 2007, and `vehicle_insured_2005` left as constant. Rebuilt and probed again: untuned LightGBM scores 0.106 / 0.091
   / 0.061 on the shipped folds against 0 for the dummy (random predictions SD 0.023 to 0.025),
   `household_vehicles_carried` now adds on 3 of 3 folds and stays, the leak probes and probe 23 find nothing, and
   `dataset check` gives 0 errors and 0 warnings.

7. **Keep the target per contract for the cars a claim takes off the cover?**

   * **Problem:**
     - When a claim ends a car's cover (a write-off or a replacement), the car claims more per contract than a car that
       stays (1.39% against 0.72% for cars insured since 2005 whose household continued into 2007), not like the full
       contracts, as the rule for keeping a target per contract asks.
     - Without dates a cut cannot be told from a non-renewal, so the share cut short is only bounded: at most 32.5% of
       the 2006 cars are not seen in 2007, and 13.3% of the carried cars of households that continued are gone.
     - Confirm that the target stays per contract here, record an exception, or amend the rule to cover cuts a claim
       causes?
   * **Background:**
     - Counted per contract, the claim that ended the cover is counted once, which is the insurer's cost of the cover
       it wrote; a rate per year in force would raise these rows further, and none can be built without an exposure.
     - No feature carries the cut: the in-year vehicle count stays dropped, `household_vehicles_carried` counts the
       cars on the policy from 2005 whatever their claims (carried cars claim 0.81% when it equals the 2005 count,
       0.88% when lower, 0.87% when higher), and the vehicle attributes are fixed across years[^7b].
     - The rule keeps a per-contract target for a cut known only at the policy's end when no feature carries the cut
       and the cut contracts claim like the full ones[^7a]; here the first part holds and the second fails, because the
       claim causes the cut.
     - Over all 2006 cars, those gone by 2007 claimed at 0.96% against 0.60%, and 9.0% of the 2006 cars left a
       household that stayed; the notes now give these bounds and the reason for the per-contract form.
   * **Effect on the task:** none under any option: the rows, the target and the score stay; the choice sets how the
     notes and the rule read for this case. Under either answer to issue 6 the carried rows hold these cuts.
   * **Consistency:** spanish_motor_insurance_2015_2018 met the rule with lapses (2,055 of 37,090 contracts cut, a
     claim in 35.4% of cut and full years alike); here the claim itself causes the cut, the fact that sets this case
     apart. australian_vehicle_insurance_2004_2005's cuts came from the extract window, and its rate weighted by the
     time observed needs an exposure this release lacks.
   * **Panel:** both auditors read the per-contract target as right and only the rule's words as unmet; the mediator
     asks you to confirm the reading.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Confirm (implemented) | the notes give the bounds and why the target stays per contract (done); recorded as the case where a claim causes the cut | no change to the task; the target is the insurer's cost of the cover it wrote | the rule's words stay unmet for this case |
     | B | Record an exception | the clause read as unmet; an exception in the record, the notes and the rule's cases, naming the claim that causes the cut | the rule stays as written | an exception for a case the rule's intent seems to cover |
     | C | Amend the rule | the clause covers cuts a claim causes: the target stays per contract when the claim itself ends the cover and no feature carries the cut | settles like cases at once | a rule change on one table's facts |

   * **Recommendation:** A, the reading both auditors share: a claim that ends the cover is the insurer's cost of that
     cover, counted once, and no rate can be built; if a second table shows the same case, C. **Decision:** confirm
     (A), an exception (B), or amend the rule (C)?

   **Notes for the AI:** the mediator's issue 2 of the re-review of 2026-11-08 (MET-14, Should, the per-contract clause
   amended 2026-11-08; the LEAK-10 / LEAK-41 Cases row on a time on risk cut short by the outcome). On A: a CC line in
   the record and a Cases row under MET-14 (allstate: the cut caused by a claim, distinct from
   spanish_motor_insurance_2015_2018's lapses), the main session's. On B: `**Exception to MET-14 (<date>,
   <curator>):** a claim ends the cover, so the cut cars claim more per contract (1.39% against 0.72%); no dates or
   exposure are released, so no rate can be built. Serves USE-5: the target is the insurer's cost of the cover it
   wrote.` into the record and the notes, and a Cases row of kind `exception`. On C: the amendment's text into
   metrics.md (the main session's), and the notes cite it.

   [^7a]: **MET-14** (Should), its clause amended 2026-11-08 (Lennart): "A cut known only at the policy's end leaves
     the target per contract when no feature set after the quote carries it and the cut contracts claim per contract
     like the full ones; the notes give the share cut short and the most a price per year in force would differ."
   [^7b]: **LEAK-10** (Must) with **LEAK-41** (Must), the Cases row on a time on risk cut short by the outcome: where
     the cut cannot be located and is no denominator, LEAK-10's second clause applies; no column here carries it.

   **Resolved (2026-11-08, Lennart):** A, confirmed as implemented: the target stays per contract where a claim ends the
   cover, the insurer's cost of the cover it wrote, counted once. On the renewal book the notes give the bounds (at most
   39.3% of its cars not seen in 2007; 15.8% of the cars of households that continued are gone and claimed at 1.39%
   against 0.72%) and name the confirmation; the record's CC line records it, and the Cases row under MET-14 (the cut
   caused by a claim, distinct from spanish_motor_insurance_2015_2018's lapses) is the main session's.

8. **Test only on the rows without a missing value, as the competition's test file was, or keep testing on all rows?**

   * **Problem:**
     - 73.0% of the renewal book's rows have a missing value (dataset.py:151), while Allstate removed such records from
       its test file and said that "when the model is applied, all of the features will be collected" (forum thread
       826, quoted in the definition).
     - So most test rows have gaps the application never has, though in the panel's test the gaps carried no outcome
       beyond the vehicle type (dataset.py:151).
     - Test on the complete rows only, training on all rows as now, or keep testing on every row?
   * **Background:**
     - Counted on the raw file (the 2,754,936 rows of the book, matched to 2005 on household, model year and submodel
       as the definition does): 27.0% of the rows and 22.1% of the households are complete; complete rows claim at
       0.90% and the others at 0.79%, with the same mean amount (1.53 against 1.54).
     - The complete rows are no closer to the book a deployed rating scores: 91.9% of the cars built before 2000 have
       a missing value against 55.4% of the newer ones, so cars before 2000 are 48.3% of the book but 14.5% of its
       complete rows (counted on the raw file).
     - The complete rows hold 29% of the book's claims, so a test fold would keep about 1,200 of its 4,006 to 4,210
       claims; the Gini, which already moves from 0.022 to 0.106 over nine folds (dataset.py:148), would get about 1.8
       times noisier by the square root of the claims (an AI estimate).
   * **Effect on the task:** testing on complete rows asks how the model ranks newer, fully recorded cars, as the
     competition's test did; testing on all rows ranks every car of the book, most with gaps a deployed rating would
     not have.
   * **Experiments:** repo (review panel, on the 2005-2006 build): missingness carried no outcome beyond the vehicle
     type in a leave-one-out test, random draws in place of the missing values scored no better, and training on
     complete rows only scored worse (dataset.py:151); a test on complete rows only was not run.
   * **Consistency:** the rules keep the missing values of an input as missing and drop only a row that lacks the
     input the prediction acts on[^8a], and they ask the notes to name what the folds do not test, which these notes
     do[^8b]; no shipped dataset restricts its test rows to complete records.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | All rows (implemented) | train and test on the book's rows, gaps kept as missing; the notes name the mismatch | the whole book; about 4,100 claims per test fold; the gaps measured to carry no outcome | 73% of the test rows have gaps the application never has |
     | B | Test on complete rows | training as now; each test fold keeps only its rows without a missing value (about 135,000 of 500,000) | the competition's test population; complete records, as the application has | about 1,200 claims per test fold and a noisier Gini; mostly newer cars, so the test population shifts in another way; the splits rebuilt |

   * **Recommendation:** A: the gaps carry no outcome beyond the vehicle type, and B spends 70% of the test claims on a
     population of mostly newer cars, which is no closer to a book where every car's features are collected.
     **Decision:** A or B?

   **Notes for the AI:** on B, check whether the v2 split API takes a test mask; otherwise a custom `_make_splits` that
   keeps the household folds and drops the incomplete rows from each test fold (the training sides unchanged), or a
   test budget filled with complete rows from more households (the book holds about 744,000). Then `splits_comment`,
   the missing-values bullet, `fit_reason` and the record's notes; re-run `dataset check` and the task probe on the
   cluster; a CC line and a CHANGELOG entry. The counts above: a chunked read of `train_set.csv` (Calendar_Year 2006,
   a 2005 row of the same household, model year and submodel; "?" in any shipped categorical column).

   **Andrej (2026-11-09, as implemented):** A, as implemented.

   **Resolved (2026-11-09, Andrej):** A: the folds train and test on all rows of the renewal book, the gaps kept as
   missing, and the notes keep naming the mismatch with the competition's complete test rows.

   [^8a]: **USE-7** (Must): "A row that lacks the input the prediction acts on is no task row: drop it rather than
     keep it as missing. Missing values of the other inputs stay missing."
   [^8b]: **USE-8** (Must): write how closely the data mirrors the use case, its fit; an approximate fit names its
     known gap.

9. **Keep the split by household, or train on an earlier year as Allstate rating the 2006 renewal would have?**

   * **Problem:**
     - The folds train on other households' 2006 rows with claim amounts read years later, while Allstate rating at
       the 2006 renewal would have trained on 2005 and earlier, with the amounts as known then.
     - Before the 2005 history was built, a model trained on 2005 and scored on 2006 reached a Gini of 0.064, above the
       household folds of that build (0.022 to 0.054) and inside the nine folds of the renewal book (0.022 to 0.106)
       (dataset.py:183), so the forced split shows no cost at this noise.
     - Each temporal design collides with a settled call, as 2005 rows have no 2004 history for the features the
       2006 rows carry (issue 3), and 2006 to 2007 needs the 2007 rows, dropped for their unsettled large claims
       (issue 2).
   * **Background:**
     - The rows are calendar vehicle-years of 2005 to 2007 with no dates; the competition trained on 2005-2007 and
       scored 2008 and 2009, whose claims were never published.
     - Both sides of every fold hold amounts read at one extract, so inside the benchmark no training label is more
       developed than a test label; the excess is against Allstate's position on the renewal date.
     - One year to train and one to test is one window where the windows rule asks for three, so either temporal
       design would also need an amendment of that rule[^9a].
   * **Effect on the task:** the folds test households new to the model with a model fit on the same year's other
     households at the same label maturity; Allstate would have fit on older, less developed amounts, and the
     household's own 2005 record reaches the model through the history counts in both cases.
   * **Consistency:** spanish_motor_insurance_coverage_level_2022_2024 and pricing_game_2016_french_fleet, with more
     years, are asked whether one window should replace their forced split (their issues 10 and 14); here no window
     keeps both settled calls.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Split by household, with a note (implemented) | folds by household over the 2006 book; the notes add the training side's year and maturity | keeps the 2005 history and the drop of 2007; no cost measurable | trains on the test year with matured amounts |
     | B | Train on 2005, test on 2006 | 2005 vehicle-years train, the 2006 book tests, without the history counts | the year order Allstate had | drops the household's record (issue 3); the amounts are still read years later; one window, an amendment |
     | C | Train on 2006, test on 2007 | the 2006 book with its history trains, 2007's renewal book tests | the year order with the record | brings back 2007, dropped for its unsettled large claims (issue 2); one window, an amendment |

   * **Recommendation:** A, with a sentence in the notes: no temporal design here keeps both settled calls, the forced
     split's cost is not measurable at this noise, and the amounts' maturity is the same on both sides of the folds.
     A low-stakes issue. **Decision:** A, B or C?

   **Notes for the AI:** on A, the splits comment says the 2005 to 2006 score of 0.064 was "inside the range of the
   folds by household (0.022 to 0.054 then ...)": it was above that range and inside only the renewal book's; reword,
   and add that the training rows are the test year's, their amounts read at the release (about 2011, the file's
   date), more developed than at a 2006 renewal. On B or C, the main session first weighs the SPLIT-14 amendment with
   spanish coverage's issue 10 and pricing_game_2016's issue 14; C also reopens issue 2 (LEAK-24).

   **Andrej (2026-11-09, as implemented):** A, as implemented.

   **Resolved (2026-11-09, Andrej):** A: the split stays by household over the 2006 book. The splits comment now gives
   the 2005-to-2006 score of 0.064 as above the household folds of that build (0.022 to 0.054) and inside the nine
   folds of the renewal book, and says that the training rows are the test year's, their amounts read at the release
   (about 2011), more developed than at a 2006 renewal.

   [^9a]: **SPLIT-14** (Must; amended 2026-11-08, Lennart): "A temporal task has at least 3 windows ... A task that
     cannot meet it ships under SPLIT-8." **SPLIT-8** (Must): the closest regime that keeps the rows, grouped by the
     entity when the periods are stacked. Andrej, 2026-11-03, issue 2: "We can drop 2007 because we still have 1
     million of samples and the current limit is 1M."

**Review panel:** ship after changes, once issue 6 is decided (mediator). Tier focused, re-review of 2026-11-08 under
LEAK-41, MET-14 to MET-16, after the raw data arrived: the claim auditor, the column auditor and the mediator ran, with
no blind reviewer, task gamer, advocate or critic in this tier. Claims: 10; 8 hold (one of them, the 1.4% of the rows of
model year 2007, holds as a count but not as the share of part years, which the mediator's test puts at about 38%), 1
refuted as worded (the 1.40% / 0.73% figure names a narrower group than its sentence; fixed), 1 untested (the share cut
short, which cannot be located without dates; bounded in the notes). Blind review: not run in this tier. Agreed: no
column is set or cut after the rating; no weight is due and the Gini is unweighted; the scorer and the household folds
hold (probe 23's flag was an artifact of drawing rows); the cuts by claims need notes only. Disputed: whether the target
per row holds for the 38% of rows that joined during 2006 (issue 6): the column auditor says no and recommends the
renewal book, the claim auditor that the ship stands; the mediator's test settles the fact for the column auditor and
leaves the population to the curator. For the curator also: how the per-contract clause reads when a claim ends the
cover (issue 7). The mediator's issues 1 and 2 are issues 6 and 7 here. The full panel of 2026-11-01 is in this file's
git history.

<details><summary>Mediator</summary>

**Mediator: allstate_claim_prediction_challenge_1m (record allstate_claim_prediction_challenge), focused re-review
2026-11-08**

Inputs: the change note, the claim auditor's and the column auditor's reports, the probes (probe 23 in its fixed form),
dataset.py and REVIEW.md, the rules. Decisive test: decisive.py on the full train_set.csv.

**Judgment record**

- Verdict: ship after changes. One issue needs the curator first: which rows the task holds (issue 1).
- Validity:
  - LEAK-41 holds (no column set or cut after the rating; both auditors). LEAK-10 holds for the five 2005-history
    columns.
  - SPLIT-8 holds (0 households shared; probe 23's +0.035 was the row-drawn artifact, the fixed probe gives +0.018, SE
    0.013).
  - MET-14 (Should, applies USE-5) departed from: about 38% of the 2006 rows joined during the year and are about half
    a year on risk, the per-row target is kept, and no rate can be built because no exposure is released. Proposed
    fix: keep only the cars on the policy at the start of 2006 (issue 1).
  - MET-15 and MET-16 hold: there is no rate target and no weight, and the Kaggle Gini is unweighted.
  - MET-1 to MET-4 hold: the scorer matches the Gini on the amount; a constant scores 0.
- Value: TP-2. The signal is small on all rows (0.058-0.102). On the carried rows alone it is 0.003-0.063, from one
  untuned model trained on the carried rows of the current sample (issue 1). It has to be measured again after any
  change.
- Quality: the notes contain wrong statements. They are fixed under "Changes now".
- Weighed: Allstate's own competition +, a real pricing task +, 2.75M renewal rows (above the budget) +, an undisclosed
  adjustment of the amounts -, a weak signal -, no exposure and no dates -.
- For the curator: issue 1 (Should, value against the declared prediction point): keep only the cars on the policy at
  the start of 2006, or keep all rows with an exception to MET-14. Issue 2: confirm how MET-14's per-contract clause
  reads when a claim ends the cover.

**The disputed fact, settled (EV-1, EV-2)**

The question: are the 2006 rows of cars not insured in 2005 shorter terms, or just lower-risk cars? The column auditor
says shorter terms, about 38% of the rows. The claim auditor says part years are 1.4%.

The test: take the cars seen in both 2006 and 2007 and compare each group's claim rate per row in 2006 with its rate in
2007. Do it by age band of the car. A shorter term predicts a ratio of about 0.5 in every band. A new-car or
new-customer effect predicts something else. Then repeat the shares and rates one year later, in 2007.

| Ratio 2006/2007 by age band | -1 | 0 | 1 | 2-3 | 4-10 | 11+ |
|---|---|---|---|---|---|---|
| carried from 2005 | - | 1.11 | 1.08 | 1.05 | 0.96 | 0.91 |
| car added, known household | 0.35 | 0.54 | 0.58 | 0.59 | 0.54 | 0.55 |
| new household | 0.31 | 0.45 | 0.51 | 0.45 | 0.46 | 0.50 |

- 2006, all rows: carried 61.9% of rows at 0.822%; added 10.7% at 0.622%; new household 27.4% at 0.501%.
- 2007, all rows: carried from 2006 64.0% at 0.807%; added 10.5% at 0.626%; new household 25.4% at 0.528%.

Reading:

- Cars that joined in 2006 claim at about half their own 2007 rate per row, at every age, 11 years and older included.
- In 2007 they claim more than the carried cars, so they are not better risks.
- Carried cars claim the same in both years.
- The same shares and rates come back one year later.

So about 38% of the rows are cars that joined during the year, on risk for about half of it. The column auditor's fact
holds. The claim auditor's 1.37% is correct only as the share of model-year-2007 cars, which can only have joined late
in the year. As a statement about the share of part years it is refuted. The claim auditor did not test the 38%. Its own
finding, that no column is set after the rating, stands and does not conflict with this.

**Disputed points, by rule**

A. Whether the shipped target is right (MET-14 Should, applies USE-5 Must; column auditor) against "the ship stands"
(claim auditor).

This is not a clash between two rules. It is one failure. LEAK-41 (Must) holds: a start date known at the rating may
ship as a feature. That clears the columns; it does not clear the target.

MET-14 keeps a per-row target only when the planned term is constant and known at the prediction point. For 38% of the
rows it is neither: the start date is not released, and the column `vehicle_insured_2005` stands in for it.

- That flag alone scores 0.046-0.052 Gini, against 0.058-0.102 for the full model. Half or more of the benchmark's
  signal is guessing how long the row was on risk.
- The rule's own remedy (a rate weighted by time on risk, as in australian_vehicle_insurance_2004_2005) cannot be
  built.

The remedy ladder:

- Repair from the origin: impossible, no exposure is released.
- Fix the definition: keep only the cars on the policy at the start of 2006 (`vehicle_insured_2005 == 1`). This is the
  mildest remedy that works.
- Keep with a note: an exception to a Should. It needs a fact that sets this case apart and the higher principle it
  serves.

The filter selects on a fact from 2005, not on the realized weight, so LEAK-41's ban on "full-year rows only" does not
apply. The flag `in07` must not be used. The filter also makes the rows match what the definition and the record already
say: "rated at the 2006 renewal", and Andrej's CC of 2026-11-03, "2006 renewal book with the 2005 history".

Cost: the signal falls (0.063/0.057/0.003 in the column auditor's run). TP-2 says a small signal is no reason to retire
(the tension "the right split against the score" goes the same way).

Mediator: by the rules (a). The curator decides, because the population changes and the value has to be measured again.

B. Cuts by claims inside the carried rows (MET-14's clause amended 2026-11-08). Both auditors agree on the facts and on
the remedy (the notes only).

The clause asks that "the cut contracts claim per contract like the full ones". Here they do not: cars gone by 2007
claimed 1.39% against 0.72%, because the claim ends the cover (a write-off or a replacement). No feature carries the
cut, so LEAK-10's clause for a cut that cannot be located and is no denominator applies (the LEAK-10/LEAK-41 Cases
row).

Mediator: the per-contract target is the insurer's cost of the cover it wrote, but the clause's words are not met. The
curator confirms the reading (issue 2).

C. Minor points, with no dispute between the auditors:

- `household_vehicles_carried` lowers the Gini on 3 of 3 folds (-0.004 to -0.009). This is a value point, not
  validity. It is not a leak, so no change; under (a) it is re-measured.
- The NV columns change between years +1.6 points (about 5 SE) more often with the later year's claim. They gain
  nothing measurable (+0.003/-0.006/+0.003). LEAK-38, weak. An optional half sentence in the notes.
- `OrdCat` dtype: settled, no change.

**Changes now** (no decision needed; the wording follows the curator's answer on issue 1)

1. Exposure paragraph (EV-2, writing): the 1.40%/0.73% figure names the wrong group. It holds for cars insured in 2005
   and 2006 whose household continues into 2007 (1.39% when the car is gone by 2007, 0.72% when it stays). Over all
   2006 cars it is 0.96% against 0.60%.
2. Part years (EV-2, MET-14): replace "1.4% of the rows" with the measured share, about 38% (new households 27.4%, cars
   added 10.7%). Say that they claim at about half their next-year rate per row at every model-year age, and that 2007
   shows the same pattern. The model-year-2007 cars (1.37%, at 0.25%) are the latest of them.
3. Decision 1 and the history bullet (EV-2): the 0.50% claim rate of new households, and part of the history's lift
   (0.112-0.117 to 0.126-0.137), measure the shorter term, not the claim record alone. Say so.
4. MET-14's clause (the notes): give the share cut short as far as it can be bounded, and say why the per-contract form
   stays. Without dates a cut cannot be told from a non-renewal. At most 32.5% of the 2006 cars are not seen in 2007;
   9.0% left a household that stayed; 13.3% of the carried rows of continuing households are gone. Without an exposure,
   the most a price per year would differ cannot be bounded.
5. `task_summary.row` and `known`, and `fit_reason`: under (b), say that 38% of the rows are new business with an
   unknown start date. Under (a), say the rows are the renewal book, and drop `vehicle_insured_2005`, which becomes
   constant.

**Issues for the curator, ranked**

1. [P3/P6 via MET-14 Should, applies USE-5 (Must); the largest effect] Which rows the task holds.
   - Problem: about 38% of the rows joined during 2006. They are on risk for about half the year, and the per-row
     target prices the part of the year they were on risk.
   - Effect: `vehicle_insured_2005` alone scores 0.046-0.052 of the full model's 0.058-0.102. On the carried test rows
     the same model scores 0.065/0.062/0.018, and trained on carried rows 0.063/0.057/0.003.
   - Column auditor's best evidence: the ratio table above (about 0.5 at every age, about 1 for carried cars, the same
     again in 2007); the score of the flag alone.
   - Claim auditor's best evidence: no feature carries a realized term (LEAK-41 holds), and no weight is due.
   - Options:
     - (a) Keep the cars on the policy at the start of 2006 (about 2.75M rows; the 1.5M sample is still possible; the
       history is never missing; the flag is dropped). This is the mediator's recommendation: it meets MET-14, matches
       the declared prediction point and Andrej's "renewal book", and it is the mildest remedy that works.
     - (b) Keep all rows as an exception to MET-14. It needs the fact that sets the case apart (no exposure is
       released, so no rate can be built), plus the curator's view that USE-5 still holds, that is, an insurer acts on
       a calendar-year cost that includes new business of unknown start. The mediator finds that view weak, because the
       use case says renewal.
   - What would settle it: the curator's call on the use case. Then, for (a), a rebuild and the task probe on the
     carried rows; the sample would hold about 1.5M carried rows, where the column auditor's run trained on about
     0.62M.
   - Decision: (a) or (b)?
2. [P6, MET-14 Should, clause amended 2026-11-08]
   - Question: under either option, does a per-contract target stay when a claim ends the cover, so that cut contracts
     claim more per contract (1.39% against 0.72%), not "like the full ones"?
   - Both auditors' reading: yes. It is the insurer's cost of the written cover; a rate per year would raise these rows
     further. The cut cannot be located without dates.
   - Options: (a) confirm, notes only (change 4), recorded as the case where a claim causes the cut, distinct from
     spanish_motor_insurance_2015_2018's lapses; (b) treat the clause as unmet and record an exception; (c) amend the
     clause to cover cuts caused by claims.

**Agreed facts** (both auditors, or not disputed)

- No column is set or cut after the rating (LEAK-41).
- The in-year vehicle count stays dropped.
- `household_vehicles_carried` does not react to 2006 claims.
- The vehicle attributes are fixed across years (0.01% change).
- The NV columns are constant within a household-year.
- No weight; the Kaggle Gini is unweighted. The scorer matches the Gini on the amount; a constant scores below 3e-15.
- 1.5M rows; claim rate 0.71%; 3,548/3,562/3,551 claims per test fold; 0 households shared between train and test.
- Probe 23 (fixed): the shared-unit lookup gains +0.018 (SE 0.013); the period test -0.015 (SE 0.016). Both are within
  noise.
- 32,324 duplicate rows within households; one exact copy dropped.
- Cars gone by 2007 claim more in 2006: the claim ends the cover.
- No dates are released, so a cut within the year cannot be told from a non-renewal.
- Settled here: about 38% of the 2006 rows joined during the year (the decisive test).

**Consistency with precedent** (the rules' Cases tables)

- spanish_motor_insurance_2015_2018 kept a per-contract target: every planned term was one year, known when the
  contract was written. Here 38% of the rows have no constant planned term. That fact sets this case apart, so (b) is
  not covered by that precedent.
- australian_vehicle_insurance_2004_2005 had terms cut by its extract window and shipped the rate weighted by time
  observed. Here no time is released, so the same remedy is impossible. That is why the ladder lands on the filter (a).
- frempl_french_motor_personal_line and pricing_game_2016_french_fleet keep a start-known length as a feature. Here
  only proxies exist, which is consistent with LEAK-41: the columns are fine; the target is the issue.
- LEAK-41 forbids selection by the realized weight (full-year rows). Option (a) selects by a fact from 2005 and is not
  caught. The source-made 30-day floor of pricing_game_2016 is a different case (the source's selection, sized in the
  notes).
- The task gamer did not run (focused tier). There is no new exploit; the probe 23 flag is the known artifact.

</details>

<details><summary>Claim audit</summary>

**Claim auditor: allstate_claim_prediction_challenge_1m (record allstate_claim_prediction_challenge), focused re-review
2026-11-08**

Under LEAK-41, MET-14 (amended 2026-11-08), MET-15, MET-16. Raw file: the full train_set.csv (13,184,290 rows);
container: the shipped 1.5M build, 3 grouped folds.

**Verdict:** ship stands. No feature carries a realized term or a claim-cut (LEAK-41 holds), no weight is needed
(MET-15/16 hold), and the metric and folds hold. Two things are refuted or open, both in the notes and neither about
validity: the exposure paragraph's 1.40%/0.73% figure is true only of a narrower group than the sentence names, and the
per-contract clause of MET-14 (amended 2026-11-08) asks for two numbers the notes do not give.

**Table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | "vehicles gone by 2007 had claimed at 1.40% in 2006, against 0.73% for the others" | curation_comments, Exposure paragraph (also the change note) | 2006 claim rate by whether the car (key Household_ID, Model_Year, Blind_Submodel, the definition's VEHICLE_KEY) appears in 2007, on the full file | REFUTED as worded (direction holds) | all 2006 cars: gone 0.956% (1,444,231 rows) vs kept 0.596% (3,003,499). Gone from a household that continues into 2007: 1.469% (401,104) vs the rest 0.638%. The figure reproduces only for cars insured in both 2005 and 2006, in a household that continues: gone 1.388% (313,605) vs cars present in all three years 0.720% (1,670,918). With Vehicle as the key instead: 0.769% vs 0.679%. | P7, EV-1 |
| 2 | MET-14's per-contract clause (amended 2026-11-08): the target stays per contract and "the notes give the share cut short and the most a price per year in force would differ" | MET-14; the notes give neither | look for the share in the data | UNTESTED (cannot be located) / gap in the notes | No dates, so a cut within the year cannot be told from a non-renewal at year end. The best bounds: 32.5% of the 2006 cars (1,444,231) are not seen in 2007 (an upper bound on cuts plus non-renewals); 9.0% (401,104) left a household that stayed; late starts (Model_Year 2007) are 1.37% (60,712), claiming at 0.247%. The cars that leave claim more per contract (0.96% vs 0.60%), so the claim ends the car's year (a total loss or a replacement). A short term alone would lower the count, so this rise is the claim ending the year, not exposure dilution. The clause's test that "cut contracts claim per contract like the full ones" cannot be run as the spanish_motor_insurance_2015_2018 case runs it. | MET-14 (Should), USE-5 |
| 3 | No feature carries the cut or a realized term (implied by "The in-year vehicle count ... is already dropped ... no weight is declared") | Exposure paragraph; LEAK-41 | (a) do the vehicle attributes of the same car change from 2005 to 2006, and does that track a 2006 claim? (b) are the policy attributes NVCat and NVVar1-4 constant within a household-year? (c) does a 2005->2006 change of the NV values track the 2006 claim more than a placebo claim does? (d) the gain of the NV features on the declared metric | HOLDS (one weak open point) | (a) one or more of the 20 attributes changed for 0.01% of the cars, whether or not they claimed in 2006 (2,666,101 / 22,124 cars), so they are fixed vehicle-type values. (b) No household with two or more rows has two values of any NV column in 2006 (0.0000). (c) Households in all three years: NV changed 05->06 for 16.2% with no claim, 23.4% with a claim only in 2005, 25.0% with a claim only in 2006, 23.4% with a claim only in 2007. The 2007 placebo comes after both snapshots, so most of the link is household risk, not timing. A +1.6-point excess for the claim of the later snapshot's own year shows in both year pairs (06->07: 25.2% for a 2007 claim vs 23.5%), about 5 SE. That is either a change made at the renewal (a new driver who then claims, known at the start) or a snapshot taken at year end; without dates the two cannot be separated (LEAK-38). (d) Dropping all five NV columns: 0.0834/0.1083/0.0548 against 0.0865/0.1020/0.0579 with them, a gain of +0.003/-0.006/+0.003, within noise. Whatever their timing, they carry no measurable score. | LEAK-41, LEAK-10, LEAK-38 |
| 4 | household_vehicles_carried is "the household's cars of 2006 insured in 2005, all on the policy at the renewal" (known at the renewal) | curation_comments (2005 history); _clean step 3 | logic (a carried car has a 2006 row whatever its claim) and a feature-drop on the 3 folds | HOLDS on timing; value note | Dropping it RAISES the Gini on 3 of 3 folds: +0.0044 / +0.0079 / +0.0085 (all features 0.0865/0.1020/0.0579; without it 0.0908/0.1099/0.0665; untuned LightGBM, L2, 300 trees). It is not a leak, but the notes call the history a lift, and this column lowers the score. All five history columns together: +0.0088 (SD 0.017; -0.007/+0.027/+0.007), within noise, as the notes say. | LEAK-10; TP (value) |
| 5 | No weight declared: "the Kaggle metric is an unweighted Gini" | Exposure paragraph; metric | container check | HOLDS | sample_weight None, scoring_columns [], MetricSpec inputs {}. There is no weight column, so MET-15 has nothing to weigh, and no design/survey weight exists (MET-16). | MET-15, MET-16 |
| 6 | Metric normalized_gini, source, on the amount via target_transform="log1p" | metric = Metric.source(...) | (i) the scorer against my own Kaggle-style Gini on expm1(y); (ii) a constant prediction on each fold; (iii) the units per fold; (iv) the source | HOLDS | (i) the scorer equals the Gini on the amount exactly on 3/3 folds (-0.01543/0.01502/0.03789) and differs from the Gini on the log scale (-0.01358/0.01691/-0.00436), so the inverse transform is applied (MET-3). (ii) A constant prediction scores below 3e-15 in absolute value on every fold (MET-13 ties). (iii) 3,548/3,562/3,551 claims per 500k test fold. (iv) The Kaggle evaluation page is JavaScript and could not be fetched; secondary sources (WPI thesis, Packt) name the normalized Gini, scored per year (2008 public, 2009 final), unweighted. The earlier panel's check stands. | MET-1, MET-2, MET-3, MET-4 |
| 7 | The forced household split shares no outcome across folds (SPLIT-8; probe 23) | splits_comment; probe 23 (fixed) | the household overlap per fold; my own household-safe lookup (the training side out of fold by GroupKFold(5) on Household_ID) of the exact 32-feature profile, added to LightGBM, on the full folds | HOLDS | overlap 0 households on 3/3 folds. 70.4% of the test rows have their profile in training. The lookup gains +0.0087/+0.0163/-0.0018 (mean +0.0078, SD 0.0091), within noise. That agrees with the fixed probe 23 (+0.018, SE 0.013 in all; the test rows that have the unit +0.029, SE 0.027) and its period test (pooled -0.015, SE 0.016). The +0.035 flag of the leak probe was the row-drawn artifact. | SPLIT-8, LEAK-17, LEAK-18 |
| 8 | "vehicles of model year 2007 ... 1.4% of the rows, claiming at 0.25% against 0.71% overall" | Exposure/part-year note | full 2006 rows | HOLDS | 60,712 / 4,447,730 = 1.37%, at 0.247%. Model_Year marks this late start, which is known at the car's own rating (the part known at the start, LEAK-41 allows it). | LEAK-41, USE-5 |
| 9 | "32,324 rows of 2006 (0.73%) repeat another row of the same household in every column" | curation_comments | full 2006 rows after the definition's drops | HOLDS | 32,324 without the target (31,891 if the claim amount must match too). One exact copy dropped: confirmed (1). | LEAK-18 |
| 10 | 1.5M rows, 0.71% claim rate, 99.29% zero | task_summary, splits_comment | container | HOLDS | 1,500,000 rows; zero share 0.9929; claim rate 0.0071 | - |

**Refuted and untested, ranked** (principles.md: validity first, Must first)

No Must is refuted. Validity holds: LEAK-41 (no realized term or claim-cut in a feature), MET-15/16 (no weight is due),
SPLIT-8 (no shared outcome across folds).

1. [Should, MET-14 per-contract clause; untested, gap] The notes do not give the share cut short or the most a price
   per year would differ. Changes: nothing in the data. The amended clause asks for the two numbers, and here they can
   only be bounded. Mildest remedy: one sentence in the Exposure paragraph. The cut cannot be located without dates; at
   most 32.5% of the 2006 cars are not seen in 2007 (9.0% leaving a household that stays); late starts are 1.4%; cars
   that leave claim more per contract (0.96% vs 0.60%), so a claim ends their year. The most a price per year would
   differ cannot be bounded without an exposure.
2. [P7 accuracy; refuted] The 1.40%/0.73% figure is true only for cars insured in 2005 and 2006 whose household
   continues into 2007 (1.39% vs 0.72%), not for "vehicles gone by 2007" against "the others" (0.96% vs 0.60% for all
   2006 cars; 1.47% vs 0.64% for cars leaving a household that continues). Changes: wording only; the direction and the
   conclusion stand. Mildest remedy: name the group ("cars insured since 2005 whose household stayed: 1.39% when the car
   was gone by 2007, 0.72% when it stayed") or switch to the all-cars figure.
3. [weak, LEAK-38; open] The NV policy attributes change from 05 to 06 slightly more often (+1.6 points, about 5 SE)
   when the claim falls in the later snapshot's own year, beyond a 2007-claim placebo. Their timing cannot be told
   without dates, and they gain nothing measurable (+0.003 / -0.006 / +0.003). Changes: nothing. Mildest remedy,
   optionally, half a sentence in the existing NV note ("their values change between years with the household's
   claims, as much with a later year's claim, so household risk rather than a recording after the claim; no gain on the
   declared metric").
4. [value, not validity] household_vehicles_carried lowers the score on 3 of 3 folds (-0.004 to -0.009). Timing holds.
   Mildest remedy: none required; if kept, the notes' "the history lifts" sentence should not credit this column (it
   was measured on the claim yes/no Gini).

Sources: https://digital.wpi.edu/downloads/zs25x859f?locale=en ;
https://subscription.packtpub.com/book/data/9781804611210/1/ch01lvl1sec03/understanding-the-evaluation-metric

</details>

<details><summary>Column audit</summary>

**Column audit (focused re-review under LEAK-41, MET-14 to MET-16): allstate_claim_prediction_challenge_1m**

column-auditor, 2026-11-08. Definition: the PR #47 worktree. Scripts: exposure.py, term.py, gain.py and a dtype probe.

**Verdict:** ship after a curator decision on the target's population. No feature is set or cut after the prediction
point (LEAK-41 holds for every column), but the per-row target fails MET-14's per-contract clause: about 38% of the 2006
rows are vehicles that joined during 2006 (new households 27.4%, cars added by known households 10.7%), whose year is
roughly half a year on risk, and `vehicle_insured_2005` marks them. That flag alone scores 0.046 to 0.052 normalized
Gini, against 0.058 to 0.102 for untuned LightGBM on all features. The notes put the part years at 1.4% of rows (model
year 2007) and read the new households' low claim rate as history signal. Neither holds.

**What is new since the last column audit (2026-11-01)**

The five history columns built on 2026-11-03 (household_vehicles_2005, household_claims_2005, vehicle_claims_2005,
vehicle_insured_2005, household_vehicles_carried) had no column audit under LEAK-41. Calendar_Year left the frame. The
raw data arrived today, so this is the first audit of the exposure paragraph against the data.

**Column table** (32 features, group, target)

| Column | Meaning | Known at prediction? | Dtype and cleaning | Verdict | Rule |
|---|---|---|---|---|---|
| Household_ID | "allows year-to-year tracking of each household" | yes | group column only | fine | LEAK-33 |
| Model_Year | "model year of vehicle (not blinded)" | yes, at the car's own rating. Age -1 (model 2007) occurs only on cars that joined during 2006 (0 carried rows), so it marks a start-time part of the term | int | fine as a column; its part-year signal is the target's issue (problem 1) | LEAK-41 (part known at the start), MET-14 |
| Blind_Make/Model/Submodel | blinded make, model, submodel | yes | category, "?" to missing, levels sorted | fine (unchanged) | CLEAN-14 |
| Cat1-Cat9 | "categorical vehicle variable" | yes (vehicle-type constants; Cat2 missing by model year) | category, "?" to missing | fine (unchanged) | CLEAN-10, LEAK-38 |
| OrdCat | "ordered categorical vehicle variable", 1-7 | yes | category (nominal); the dtype probe flags numeric_levels. The 2006 rates show no risk order (0.21/0.80/0.57/0.70/0.63/0.57/0.14%; rank corr -0.29) | fine, settled earlier (PR #37 board resolved). The source calls it ordered, so `ordinal` would be the lossless type, but the curator settled this. No change today | CLEAN-14 |
| Var1-Var8 | "continuous vehicle variable" | yes | float | fine; LEAK-30 note stands | LEAK-30 |
| NVCat, NVVar1-4 | policy (non-vehicle) characteristics | probably, cannot be timed | category / float | fine (unchanged) | LEAK-38 |
| household_vehicles_2005 | built: the household's 2005 vehicle-rows | yes (2005 history). Missing marks a new household, which mostly means a part year in 2006 (problem 1) | float, NaN = new household | fine as a column, by timing | LEAK-10, LEAK-41 |
| household_claims_2005 | built: 2005 vehicle-rows with a claim | yes (late-reported 2005 claims already noted) | float | fine | LEAK-10 |
| vehicle_claims_2005 | built: this car's 2005 rows with a claim | yes. Missing marks a car not insured in 2005 | float | fine | LEAK-10 |
| vehicle_insured_2005 | built: the car (household, model year, submodel) was insured in 2005 | yes. 0 = the car joined in 2006, at a renewal or mid-year, so its term is mostly short | category 0/1 | fine by timing. It is the term marker of problem 1 | LEAK-41, MET-14 |
| household_vehicles_carried | built: count of the household's 2006 cars that were insured in 2005 | yes: it counts cars on the policy from 2005, and a car that leaves in 2006 still counts. It is not cut by a 2006 claim (tests below) | int | fine | LEAK-41 |
| log1p_claim_amount (target) | log1p of the adjusted claim payments of the vehicle in the calendar year | - | float; scored on the amount | per-row form fails MET-14 for the 38% of rows that joined in 2006 (problem 1) | MET-14 |
| Row_ID, Vehicle, Calendar_Year, Cat10-12, in-year vehicle count | dropped | - | - | fine (stay dropped) | CLEAN-3, LEAK-10, PROV-3 |

**Problems, ranked**

**1. The target is per row, but rows that start mid-year carry a planned term of about half a year (P3/P4; MET-14
Should, USE-5; not a LEAK-41 leak).**

Evidence (full 2006 file, vehicles followed by (household, model year, submodel); term.py, exposure.py). For vehicles
that continue into 2007, I compare the claim rate per row in 2006 with the same vehicles' rate in 2007:

| Group | Rows | Claim/row 2006 | Claim/row 2007 | Ratio |
|---|---|---|---|---|
| carried from 2005 (known household) | 1,634,780 | 0.720% | 0.734% | 0.98 |
| added in 2006 (known household) | 334,037 | 0.506% | 0.940% | 0.54 |
| new household in 2006 | 972,970 | 0.411% | 0.888% | 0.46 |
| age -1 (model 2007), new / added | | | | 0.31 / 0.35 |

So the vehicles that joined during 2006 were on risk for about half of 2006. In 2007 the same vehicles claim more than
the carried ones, not less. Shares of the 2006 rows: new household 27.4%, added car of a known household 10.7% (38.1%),
model year 2007 1.37%. In the shipped 1.5M rows, 61.9% are carried (claim 0.821%) and 38.1% are not (0.532%).

Score through the term (gain.py, the shipped 3 folds, untuned LightGBM L2 on log1p, the declared Gini):

| Fold | vehicle_insured_2005 alone | LGBM all rows | Same model, carried test rows | Trained and tested on carried |
|---|---|---|---|---|
| 0 | 0.046 | 0.087 | 0.065 | 0.063 |
| 1 | 0.050 | 0.102 | 0.062 | 0.057 |
| 2 | 0.052 | 0.058 | 0.018 | 0.003 |

The term marker alone gives half or more of the shipped score. On the full-year renewal book the signal is
0.003-0.063.

Wrong statements in the definition:

- The notes give the part years as "1.4% of the rows" (model year 2007).
- Decision 1's "new household at 0.50%" is read as history signal. It is mostly the shorter term.
- The history's lift (0.112-0.117 to 0.126-0.137 on claim ranking) partly measures this term.
- The prediction point "rated at the 2006 renewal" does not describe 38% of the rows, which had no 2006 renewal.

Timing: a car's or household's start date is known when it is rated, and the planned term to 31 December is a part
known at the start. LEAK-41 lets that ship as a feature, so the columns are not leaks. The fault is the target: MET-14
keeps a per-contract target only when the planned term is constant and known, and here it is not. The rate per year
cannot be built, because no exposure is released.

Remedies, mildest first (curator's call):

- (a) Restrict the task to the vehicles on the policy at the start of 2006, i.e. vehicle_insured_2005 == 1. That is the
  renewal book the prediction point describes. The selection is a start-of-year fact, not the realized weight, so
  LEAK-41's ban on full-year-only rows does not apply (in07 must NOT be used). About 2.75M rows remain, above the 1.5M
  budget. vehicle_insured_2005 becomes constant and leaves; the history is then never missing. Cost: the signal is near
  noise on one fold (0.003 to 0.063), a TP-2 question.
- (b) Keep all rows and correct the notes, the fit_reason and decision 1 with the numbers above. The notes would give
  the share joining mid-year (38%), the about 2x gap a price per year would show for them (ratio 0.46-0.54), and the
  term marker's score alone (0.046-0.052). The benchmark then rewards predicting the term for 38% of the rows.

I recommend (a): it matches the declared prediction point and MET-14's per-contract clause.

**2. Cuts by claims within the carried rows: per-contract target right, clause wording not literally met (P3; MET-14 as
amended 2026-11-08; a question for the curator).**

Of the carried rows in households present in 2007, 13.3% were gone by 2007 (plus 1.2% that both joined and left). They
claim 1.39% against 0.72% for the rows that stayed. This is the 1.40% the notes cite.

The cut follows the claim (a write-off or a lapse), so the cut contracts do NOT "claim per contract like the full ones".
Per contract, the claim that ended the cover is counted once, which is the insurer's cost of the written cover. A rate
per year in force would raise these rows further.

No feature set after the quote carries the cut:

- The in-year count stays dropped.
- household_vehicles_carried does not react. Carried cars claim 0.81% when it equals the 2005 count, 0.88% when lower
  and 0.87% when higher. Rows whose key appears more often in 2006 than in 2005 claim 0.69%, against 0.82%.
- The composition signal (carried cars claim 1.05% when the household added a car in 2006, 0.76% otherwise) stays out
  of the features.

Remedy: notes only. Give the share cut (about 13%) and say why the per-contract form is kept, as MET-14's clause asks.
Confirm the reading with the curator.

**3. No weight, MET-15 and MET-16 (fine).** The Kaggle metric is the unweighted row Gini, and no exposure or survey
weight exists, so no sample weight is declared. MET-16 does not apply.

**4. OrdCat dtype (P7; CLEAN-14; settled, no change).** It is the only dtype flag. It is nominal by the earlier
decision, while the source says "ordered".

Not re-tested: missingness (cleared 2026-11-01), LEAK-30, the profile-lookup flag of probe 23 (natural repeats, LEAK-18,
another agent's lane).

</details>

## Reference

Kaggle (2011). Allstate Claim Prediction Challenge. https://www.kaggle.com/competitions/ClaimPredictionChallenge

Huangfu D. (2015). Data Mining for Car Insurance Claims Prediction. MSc project report, Worcester Polytechnic
Institute. https://digital.wpi.edu/downloads/zs25x859f

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).
