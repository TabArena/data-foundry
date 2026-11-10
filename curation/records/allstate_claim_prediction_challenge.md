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

**Assessment (AI, 2026-11-01):** added as `datasets/_dev/tabarena-v0pt2/allstate_claim_prediction_challenge_1m/` by /add-dataset with the full review panel; the open questions are in its `REVIEW.md`. Recommend shipping after the panel's changes; only issue 1, the forced grouped split by household (open against how_much_did_it_rain, with five siblings), could turn it to `No`. Changes after the panel: 2007 dropped (LEAK-24, its large claims missing; MET-2), `household_vehicles` and Cat10 to Cat12 dropped, `OrdCat` categorical. What shipped supersedes the text below the CC: not "split temporal by `Calendar_Year`" over 2005-2007 but 2005-2006 only (1.5M rows of whole households), split by household, so a household's own claim history is not used; Gini 0.053 / 0.054 / 0.022 by fold (random predictions 0.019-0.025, the third within chance), not 0.093; "the Kaggle winner 0.20 on 2009" is no like-for-like reference, as Allstate blinded model codes separately per file (26% of test rows carry codes absent from training). `required_split` and `tags` wait for your marks on the field rows (issue 1), as do issues 2 to 4. Priority 3: gap + (insurance thin), use case 0 (fit approximate), source + (Allstate's pages, Huangfu's report), shape + (1.5M rows, grouped), risk - (split open; one fold at chance; undisclosed adjustment).

CC (2026-11-02, Andrej): the forced grouped split ships (issue 1 (a) in allstate_claim_prediction_challenge_1m; the record takes `Grouped (NON-IID)` and `Non-IID (Grouped)` as the issue says): "Forced group splits should be fine. Regarding forced IID, did you make sure there are no leaks? Whenever there are no leaks we can ship." Recorded in SPLIT-8 (amended 2026-11-02: a forced grouped split ships; a forced IID split ships only when the leak test across the random split finds none).

**Assessment (AI, 2026-11-02):** the leak test across the forced grouped split finds none (SPLIT-8). Shared rows: 84% of the test rows have an exact feature copy in another household on the training side (one vehicle type and policy profile), but the copies' claim rate (0.68%) is the test rows' (0.66-0.69%), a lookup of their mean target scores a normalized Gini of -0.008 / -0.008 / -0.002 against the model's 0.053 / 0.054 / 0.022, and none of the 10,761 test claims has a training row with the same features and amount; the 6,090-6,224 test rows per fold whose whole multi-vehicle household-year (vehicles and policy columns) recurs under another household in training claim no more when that household claimed (0.54% / 0% / 0.76% against 0.54% / 0.75% / 0.61%), so no household hides under two ids. Shared period (the calendar year): adding the training side's mean target of the year changes no score, a year-only predictor scores 0.001 to 0.026, and taking the test year's rows out of training never costs more than taking out as many random rows (6 of 6 fold-years score higher without the same year: 2005 0.084 / 0.072 / 0.026 against 0.061 / 0.040 / -0.051, 2006 0.073 / 0.054 / 0.028 against -0.007 / 0.027 / 0.025). No feature is built from other rows' outcomes once `household_vehicles` and `Vehicle` are gone; NVVar1 to NVVar4 belong to the row's own household and are no count of the year's claims (claim rate 0.85-1.25% above their minimum against 0.67-0.71%), and they change as often after a claim of the previous year as with one of the same year. how_much_did_it_rain's `No` named a measured shared-period leak; none is found here.

CC (2026-11-03, Andrej): 2007 stays dropped (issue 2 (A) in allstate_claim_prediction_challenge_1m; `Calendar_Year` stays a feature): "We can drop 2007 because we still have 1 million of samples and the current limit is 1M. We might reconsider this decision for a future version."

CC (2026-11-03, Andrej): rebuilt as the 2006 renewal book with the 2005 history, counts only (issue 3 (B) in allstate_claim_prediction_challenge_1m): "I go with your recommendation of 2006 renewal book with the 2005 history (counts)". The rows are the 4.4M vehicle-years of 2006 (1.5M of whole households sampled); 2005 gives the household's vehicle and claim counts, the cars carried over and the car's own claims; `Calendar_Year` goes (one value), so the 2007 decision above no longer keeps it.

CC (2026-11-03, Andrej): the competition's normalized Gini on the amount stays, the regression on log1p (issue 4 (A)): "Let's go with A".

CC (2026-11-03, Andrej): ship (verdict). Issue 5 (A): households drawn at random and dealt to folds at random, the natural claim rate (claim households dealt evenly gave no steadier folds); the metric, the competition's normalized Gini on the amount, checked.

CC (2026-11-08, Lennart): the declared metric (`normalized_gini`) is checked, as declared; the record ships, with no open issue on the PR #47 review board.

**Assessment (AI, 2026-11-08):** ships by default (no open issue on the PR #47 board), but the definition's changes of 2026-11-06 (the exposure paragraph) have not passed `dataset check`, and the re-review panel under LEAK-41 and MET-14 to MET-16 has not run: both wait for the competition files, which download only after the Kaggle competition rules are accepted. No container is built before both pass.

**Assessment (AI, 2026-11-08):** the competition's files are in the warehouse: `dataset check` of the definition with the exposure paragraph passes (0 errors, 0 warnings) and the re-review panel ran (next line), so the Assessment of 2026-11-08 above (check and panel waiting for the files) is superseded. Superseded too, the part-year statement of 2026-10-30 ("vehicles of the next model year ... claim at 0.20% against 0.73%"): about 38% of the 2006 rows are cars that joined during the year (27.4% new households, 10.7% cars added by a household of 2005), on risk for about half of it (per row they claim in 2006 at 0.45 to 0.59 times their own 2007 rate in every band of model-year age, against 0.91 to 1.11 for the cars carried from 2005, and 2007 repeats the pattern); the cars of the next model year (1.37% of the rows) are the latest of them. The notes now say so, name the group of the exposure paragraph's 1.40% / 0.73% (cars insured since 2005 whose household continued into 2007: 1.39% against 0.72%; over all 2006 cars 0.96% against 0.60%), bound the share cut short by claims (at most 32.5% of the 2006 cars not seen in 2007) and say that the new households' 0.50% and part of the history's lift measure the shorter term.

**Assessment (AI, 2026-11-08):** review panel (focused: claim auditor, column auditor, mediator; re-review under LEAK-41, MET-14 to MET-16): ship after changes, once the population is decided; the mediator recommends keeping only the cars on the policy at the start of 2006 (MET-14 departed from for the 38% part years, whose start is not released: `vehicle_insured_2005` alone scores 0.046-0.052 of the full model's 0.058-0.102, and trained and tested on the carried rows untuned LightGBM scores 0.063 / 0.057 / 0.003, to be measured again after a rebuild); LEAK-41, LEAK-10, SPLIT-8 (probe 23's flag an artifact of drawing rows), MET-15, MET-16 and MET-1 to MET-4 hold; disputed: whether the target per row holds for the rows that joined during 2006 (issue 6: the column auditor no, the claim auditor yes; the mediator's test settled the 38% for the column auditor); for the curator: issues 6 (the renewal book or all rows as an exception) and 7 (the target per contract where a claim ends the cover) in the folder's REVIEW.md.

CC (2026-11-08, Lennart): the rows are the 2006 renewal book, only the cars on the policy at the start of 2006, those insured in 2005 too (issue 6 (B) in allstate_claim_prediction_challenge_1m): "Option B: The renewal book." It confirms Andrej's "2006 renewal book" framing of issue 3 (B) (CC of 2026-11-03) and supersedes the rows that CC gives ("the 4.4M vehicle-years of 2006"): the cars that joined during 2006 (38.1% of its vehicle-years, on risk for part of the year, MET-14) leave, selected on a fact of 2005, never on presence in 2007 (LEAK-41), and the flag `vehicle_insured_2005` leaves as constant.

CC (2026-11-08, Lennart): the target stays per contract where a claim ends a car's cover (issue 7 (A) in allstate_claim_prediction_challenge_1m, `ok`): confirmed under MET-14's per-contract clause (amended 2026-11-08) as the case where the claim causes the cut, distinct from spanish_motor_insurance_2015_2018's lapses. The cut cars claim more per contract (1.39% against 0.72% for the book's cars of households that continued into 2007), no feature carries the cut, and no rate can be built without an exposure.

**Assessment (AI, 2026-11-08):** rebuilt on the renewal book (issue 6 (B)); `dataset check` 0 errors, 0 warnings. Rows: 2,754,936 of the 4,447,729 vehicle-years of 2006 stay (61.9%; 1,942,447 households, 22,632 claims, 0.82%), the 1,692,793 cars that joined during 2006 (claim rate 0.54%) leave; the 1.5M sample holds 0.82% claims, 4,006 to 4,210 per test fold, and the history is never missing. Signal (TP-2): untuned LightGBM on the shipped folds scores a normalized Gini of 0.106 / 0.091 / 0.061 against 0 for the dummy (random predictions SD 0.023 to 0.025 per fold), and 0.022 to 0.106 over nine folds of three random household splits (mean 0.069, SD 0.024); the task probe (sides capped at 200,000 rows) puts LightGBM above the dummy on 3 of 3 splits (+0.037, SE 0.004), its linear model and random forest at chance, and flags `no_signal` and `unstable`, which read its R^2-type skill (EV-3). The panel's 0.063 / 0.057 / 0.003 trained on about 0.62M carried rows; on the rebuilt 1M-row training sides the renewal book scores as all rows did (0.058 to 0.102). The 2005 history adds +0.005 to +0.012 on the amount and +0.001 to +0.003 on claim yes/no; `household_vehicles_carried` adds +0.001 to +0.009 on 3 of 3 folds (on all rows it had lowered the score), so it stays. Leak probes: no feature scores alone, all features -0.072 R^2 on log1p, 74.4% of the test rows have an exact feature copy in training; probe 23: no period gain (-0.016, SE 0.030) and no shared-unit gain (0 households shared; the exact profile -0.005, SE 0.024). Residual: 38,728 rows of the book (1.41%) share a vehicle key with more rows in 2006 than in 2005 (claiming at 0.69% against 0.82%), so a few same-type cars added in 2006 stay; dropping them would select on the cars added later in the year. The Assessment of the review panel above is superseded where it gives the shipped rows as all of 2006 and the signal on the carried rows as 0.003 to 0.063.

CC (2026-11-09, Andrej): the folds keep testing on all rows of the 2006 renewal book, the gaps kept as missing (review issue 8, A, as implemented).

CC (2026-11-09, Andrej): the split stays by household (review issue 9, A, as implemented); the splits comment now gives the 2005-to-2006 score of 0.064 as above the household folds of that build and names the training side's year and the maturity of its amounts.

CC (2026-11-09, Andrej): columns held only for training rows stay out for now, no training-only role (cross-dataset item of 2026-11-09; MET-14, LEAK-41, MET-16); the notes list them.

CC (2026-11-09, Andrej): the training labels' maturity is stated in the notes (cross-dataset item of 2026-11-09, option B).

## Reference

Kaggle (2011). Allstate Claim Prediction Challenge. https://www.kaggle.com/competitions/ClaimPredictionChallenge

Huangfu D. (2015). Data Mining for Car Insurance Claims Prediction. MSc project report, Worcester Polytechnic
Institute. https://digital.wpi.edu/downloads/zs25x859f

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).
