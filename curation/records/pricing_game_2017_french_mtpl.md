---
unique_name: pricing_game_2017_french_mtpl
name: pg17trainpol / pg17trainclaim (CASdatasets, 2017 French pricing game)
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
- 'Samples: One Moment'
- 'Target: Later'
year: '2017'
domain: insurance
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://github.com/dutangc/CASdatasets/blob/master/man/pricingame.Rd
- https://github.com/dutangc/CASdatasets/tree/master/data
- https://actinfo.hypotheses.org/86
- https://www.aicrowd.com/challenges/insurance-pricing-game
- https://github.com/JuliaComputing/ScoringEngineDemo.jl/blob/main/assets/training_data.csv
v2_path: datasets/_dev/tabarena-v0pt2/pricing_game_2017_french_mtpl/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> Yes`, priority 3: the third actuaries' pricing game (2017), a French motor
portfolio with rich vehicle features, reused with three more claim years by AIcrowd (2020-21), which scored RMSE; which
release to ship is open.
- Source: the 2017 game (Arthur Charpentier, with the ACTINFO chair and the French Institute of Actuaries;
  actinfo.hypotheses.org/86, 10 January 2017; the game day 16 November 2017). CASdatasets `pg17trainpol` (100,000
  policies, Year 0) and `pg17trainclaim` (14,243 claims), "Datasets from unknown private insurers", every column
  documented; `pg17testyear1`-`4` hold "new policies (drivers willing to purchase insurance for Year t)", without
  claims. AIcrowd Insurance Pricing Game (Imperial College, 18 December 2020 to 7 March 2021): "The dataset contains a
  total of 100K real historical car insurance policies over 5 years in the recent past", "provided by a large car
  insurance provider in a European country".
- Use case: an insurer pricing next year's contracts (both games); fit direct. Regime temporal on the AIcrowd years
  (years 1-3 -> 4), a policy's own history fair (SPLIT-13); the CASdatasets release alone has claims for Year 0 only, so
  IID grouped by client.
- Siblings and duplicates: the AIcrowd lead is merged here (earlier triage linked 4,644 policies by a unique amount:
  AIcrowd year k = pg17 Year k-1); `pricing_game_2015_french_mtpl` and `pricing_game_2016_french_fleet` are other
  portfolios of the series (PROV-7); `fremtpl2` and `frempl_french_motor_personal_line` are other French portfolios.
  OpenML: none by name.
- Papers and pages: CASdatasets `pricingame.Rd`; the AIcrowd challenge page; a copy of AIcrowd's `training.csv` in
  JuliaComputing/ScoringEngineDemo.jl (no data licence stated).
- Metric: AIcrowd's RMSE leaderboard ("measures how well you can estimate the risk of policy IDs"); its final ranking
  was "competitive profit" in a simulated market, which needs the other players' prices. `rmse` on the claim amount is
  the computable leaderboard metric (MET-4, MET-11). The 2017 game's scoring is in a rules PDF not read.
- Earlier AI triage, 2026-10-20, measured: 87.8% zeros in pg17 Year 0, 89.8% in AIcrowd; AIcrowd noised the features
  (driver age off by a median 3 years, vehicle value by 2,945, make and model hashed) and set 1,116 negative Year-0
  totals to 0; untuned LightGBM: AUC 0.61-0.63 for a claim, R^2 about 0.
- Risks for /add-dataset: which release (AIcrowd: four claim years, noised features, an account; CASdatasets: clean
  features, one claim year); negative amounts (legal recourse), the family's insurance-conventions question; four
  AIcrowd years give at most two windows above the 50% floor (SPLIT-14, else SPLIT-8); `pol_insee_code` has about 18,000
  levels.
- Priority: gap 0, use case + (the games' pricing task), source + (column-level documentation, two organisers' pages),
  shape + (100,000 policies, about 25 mixed features, years), risk - (the release choice, noised features, negative
  amounts).

**Assessment (AI, 2026-10-30):** suggested call for policy question 3 of the zero-inflated review, where Andrej asked
for a call per dataset from its references and the domain's practice instead of one convention for the family (the
shared reasoning: a time exposure or a sum insured is a feature, and a rating-cell table weights the metric by its
exposure; negative amounts that are recoveries become 0; the source's metric first, else the normalized Gini as a
context metric, since RMSE on raw amounts follows a few large claims and a Tweedie or Poisson deviance needs positive
predictions; MET-10 as amended on 2026-11-02 (Andrej) later declined a family-wide metric, so each table's metric is
decided on its own); the curator
has the call.
- Release: CASdatasets Year 0 (`pg17trainpol` with `pg17trainclaim`), split grouped by client: GPL terms, every column
  documented and the features untouched. The AIcrowd table adds three claim years for a next-year split, but its
  features are noised and its terms are an account's; it is the alternative if the curator wants the temporal task.
- Target: the claim total of the policy-year, negative totals (1,116 in Year 0, legal recourse) set to 0 as AIcrowd did.
- Exposure: none in either release; rows are whole policy-years.
- Metric: normalized Gini as the stand-in for the game's market (MET-11); with the AIcrowd table,
  its leaderboard `rmse` (MET-4).
- `pol_department` (the commune's department, 96 values) as the category; `pol_insee_code` (17,794 communes) as text.

CC (2026-10-30, Andrej): `Yes`, priority 3 (the AI screening had `TBD -> Yes`, priority 3; zero-inflated screening
review page).

Motor policies of an unnamed French insurer ("Datasets from unknown private insurers", CASdatasets
`pricingame.Rd`) from the French Institute of Actuaries' pricing game of 16 November 2017: 100,000 policies of 91,488
clients over Years 0-4, with claims only for Year 0 (`pg17trainclaim`, 14,243 claims); `pg17testyear1`-`4` have no
claims. The AIcrowd Insurance Pricing Game (Imperial College with UQAM and actuarial bodies, 2020-21) reuses this
portfolio, so the AIcrowd lead is merged here. Measured 2026-10-20 on its `training.csv` (228,216 rows, 57,054 policies
x 4 years): all 6,280 positive year-1 amounts equal a pg17 Year-0 policy total, and on 4,644 policies linked by a
unique amount, policy age, coverage and usage agree, with AIcrowd year k = pg17 Year k-1. AIcrowd adds the claims of
Years 1-3 but noised the features (driver age off by a median 3 years, vehicle value by 2,945, make and model hashed)
and set the 1,116 negative Year-0 totals (legal recourse) to 0. Zeros, confirmed: no claim in the year, 87.8% of pg17
Year-0 policies (88.9% with the negative totals) and 89.8% of AIcrowd rows.

Untuned LightGBM: pg17 Year 0, 3 folds grouped by client, AUC 0.61 for a claim, R^2 -0.03 on log1p among positives;
AIcrowd years 1-3 -> 4, AUC 0.63 (0.635 with past claims), R^2 0.00. A weak signal, as in the rest of the family.
Suggested task: the AIcrowd table split by year (the game's next-year pricing; a policy's own claim history is fair
under that split), or pg17 Year 0 as an IID task with clean features. Licence: GPL (>= 2) for CASdatasets; AIcrowd
needs an account, and a copy of `training.csv` sits in JuliaComputing/ScoringEngineDemo.jl (no data licence stated).
To check: which release, the AIcrowd noise, the negative amounts. Schema and years differ from
`pricing_game_2015_french_mtpl`, `fremtpl2`, `frempl_french_motor_personal_line` and `bemtpl97`.

**Assessment (AI, 2026-11-01):** added as `datasets/_dev/tabarena-v0pt2/pricing_game_2017_french_mtpl/` by /add-dataset with the full review panel; the open questions are in its Review. Recommend shipping; only issue 1, the forced grouped split of one claim year (open against how_much_did_it_rain, with frempl, australian, rand and spanish 2022-2024), could turn it to `No`. Changes after the panel: impossible licence ages and one 7,901 kg weight made missing, `vh_model` joined to the make, the commune typed as text, the split and metric reasons restated with measured figures (rows, target and folds unchanged). Corrections to the notes above: the screening's `rmse` (MET-4, MET-11) gives way to the normalized Gini as the stand-in for the game's profit (Gini 0.20-0.37 per split; a Tweedie GLM best, 0.319); the AIcrowd challenge and the JuliaComputing `training_data.csv` links are related tables, not the source, and the name no longer cites AIcrowd. `required_split` and `tags` wait for your marks on the field rows (issue 1), as do the metric (issue 2), the target scale (3) and the name (4). Priority 3: gap + (insurance thin), use case 0 (fit approximate), source + (the organiser's copy, every column documented), shape + (100,000 policies, grouped), risk - (the forced split is open; weak signal).

CC (2026-11-02, Andrej): the forced grouped split ships (issue 1 (a); the record takes `Grouped (NON-IID)` and `Non-IID (Grouped)` as the issue says): "Forced group splits should be fine. Regarding forced IID, did you make sure there are no leaks? Whenever there are no leaks we can ship." Recorded in SPLIT-8 (amended 2026-11-02: a forced grouped split ships; a forced IID split ships only when the leak test across the random split finds none). The amended SPLIT-8 covers the grouping by client of one year, so no separate amendment of the grouped branch is made.

**Assessment (AI, 2026-11-02):** the leak test across the forced grouped split (SPLIT-8 as amended 2026-11-02) finds none, on the 9 shipped splits with untuned LightGBM (Tweedie), base Gini 0.223 +- 0.016. (1) Shared rows and hidden groups: no test row has an exact copy on the training side, nor a near copy (every feature but commune, value and weight); keys that link rows of different clients carry nothing: a household proxy (commune and first driver's age, sex and licence age) links 4.2% of test rows and a vehicle proxy (commune, model, age, value) 0.85%, and their training-side mean target as a feature changes the Gini by -0.000 +- 0.004 and +0.003 +- 0.004; the client's own other vehicles, removed from training on random folds, change it by -0.002 +- 0.003 (split audit). (2) Shared period: the file is one year, so every split shares it; the training side's same-year mean target of the test row's department or commune (out of fold) changes the Gini by -0.005 +- 0.010 and -0.005 +- 0.005, and removing from training the rows of half the test communes, against as many random rows, changes it by +0.008 +- 0.029: no shared local shock. (3) Features from other rows' outcomes: only `client_n_vehicles` (a count of policies, no outcome; drop-one -0.000 +- 0.009) and `pol_bonus` (start-of-year value, column audit) span rows; the bonus of a policy without a claim tells whether a sibling claimed at AUC 0.516. how_much_did_it_rain's `No` named a measured leak; none is found here.

CC (2026-11-03, Andrej): the metric is the mean Tweedie deviance (power 1.5, predictions floored at 1 EUR) as the stand-in for the game's profit, not the normalized Gini (issue 2 (B) in pricing_game_2017_french_mtpl): "Use mean_tweedie_deviance and implement it in the library". Added to the metric library under scikit-learn's name.

CC (2026-11-03, Andrej): the name `pricing_game_2017_french_mtpl` stays (issue 4 (A)): the source's own title; the notes say the target sums every guarantee of the cover.

CC (2026-11-03, Andrej): ship (verdict). The target stays in euros (issue 3 (A)), an exception to CLEAN-16: the deviance scores the predicted cost's level in euros, where a Gini scores only the order; the metric, the mean Tweedie deviance, checked.

**Assessment (AI, 2026-11-06):** exposure re-review (LEAK-41, MET-14 to MET-16), changes made in the definition's notes and metric reason: no exposure column and no weight; the target stays the policy's claims of the year, scored unweighted (MET-15: no realized denominator, so LEAK-41 and probe 22 have nothing to act on). The "rows are whole policy-years" of the 2026-10-30 assessment holds, on the rules (a yearly premium, Sec. 1 and 4.9) and on a test of the newest policies, not on the later year files: pg17testyear1 to 4 are the organiser's ageing of Year 0 (from Year 0 to Year 1 both durations rise by 1 for all 100,000 policies, with no change of cover, use, vehicle or second driver, while 37,314 Year-0 policies had a situation change in the year before). Share cut short (MET-14): none can be located; the 8,743 policies at duration 1 claim as their risk predicts (1,198 claims against 1,184.4 expected by a LightGBM claim model without the two durations, 5 folds by client, z 0.43), so at most about 9% of them could be half years (95% lower bound 0.954); for older policies it is not observable (no cancellation date). The 1 EUR floor of the CC of 2026-11-03 sits 1.2 orders below the smallest plausible mean policy cost, 16.8 EUR (Mini, WorkPrivate, bonus-malus above 0.5 up to 0.7, first driver aged 26 to 40: 553 policies, the cheapest cell of cover x use x bonus band x age band with at least 500; 14 to 20 EUR under other band edges), where MET-13 as amended on 2026-11-06 asks for two orders; on repeat 0, folds 0 to 2, the floor decides whether an untuned ridge regression beats the constant (61.61 against 63.31 at 1 EUR, 66.33 at 0.1 EUR), while the random forest stays at 60.57 to 60.59: Review issue 5.

**Assessment (AI, 2026-11-06):** review panel (focused: claim auditor and mediator, re-review under LEAK-41, MET-14 to MET-16): ship after changes, text only and made (the line above; rows, target, split, metric and floor unchanged); disputed: none between agents (the claim auditor's remedy of keeping 1 EUR as a recorded exception is ruled out by the mediator, since MET-13 is a Must, so 1 EUR can stay only by an amendment); for the curator: issue 5 (A keep 1 EUR and amend MET-13, which would reopen the 1e-4 floors of fremtpl2 and bemtpl97; B lower the floor to 0.1 EUR, recommended; Andrej set the 1 EUR and should be told).

**Assessment (AI, 2026-11-06):** correction to the review-panel line above: option A of Review issue 5, an amendment of MET-13 worded for a unit of the scored currency, leaves the 1e-4 claims-per-year floors of fremtpl2 and bemtpl97 as they are (they are checked against the new wording, not reopened); what A gives up is the "two orders" bar across the family.

CC (2026-11-08, Lennart): the deviance's floor is 0.1 EUR (Review issue 5 (B), "Lower the floor to 0.1 EUR"): a prediction below 0.1 EUR counts as 0.1 EUR. This follows the collection's rule for a deviance floor, two orders of magnitude below the smallest plausible mean (MET-13 as amended on 2026-11-06; 16.8 EUR here), a convention of the collection that can change later, not a property of the source. It supersedes Andrej's floor of 1 EUR (CC of 2026-11-03, issue 2 (B): "predictions floored at 1 EUR"), which sat 1.2 orders below that mean.

CC (2026-11-08, Lennart): `pol_pay_freq` is an ordered category, fewest payments a year first: Yearly < Biannual < Quarterly < Monthly (Review issue 8 (C) of spanish_motor_insurance_coverage_level_2022_2024, "Ordered in all three"), the same order as in that table and in pricing_game_2016_french_fleet.

**Assessment (AI, 2026-11-08):** both CC lines above applied in the definition (`min_prediction=0.1`; the metric reason and the notes' floor bullet name the rule and the curator's framing; `pol_pay_freq` in `ORDINAL`, its four levels in the data: 37,733 Yearly, 29,702 Biannual, 2,547 Quarterly, 30,018 Monthly). Task probe at the new floor (5 of 9 splits): the random forest 62.22 against the constant's 63.10 (0.1% of its predictions at the floor), the linear model 81.97 (6.7%) and LightGBM 90.30 (3.8%), against 66.28 and 70.90 at the 1 EUR floor; the best family does not move. `dataset check`: 0 errors, 0 warnings.

CC (2026-11-08, Lennart): the declared metric (`mean_tweedie_deviance`, with the floor of 0.1 EUR set in issue 5) is checked, as declared on the PR #47 review board.

CC (2026-11-08, Lennart, in chat): `pol_coverage` is an ordered category, Mini < Median1 < Median2 < Maxi, the order in which the game's rules list the covers, as `pol_pay_freq` is ordered for the family (spanish coverage issue 8); it was an unordered category.

CC (2026-11-08, Lennart): `drv_sex1` and `drv_sex2` leave the features, on the stance Lennart set in australian_vehicle_insurance_2004_2005's issue 7 ("A stance for the family; as if we were to simulate the case in europe always"): sex is no rating factor of any insurance pricing task of this collection, whatever the actor's jurisdiction or the data's year, as under EU law (Test-Achats, CJEU C-236/09, in force for new contracts from 21 December 2012); the Tensions row on rating factors in principles.md says so. Supersedes the note that kept them as a legal rating factor in the data's year (AI, 2026-11-01), which shipped with Andrej's verdict of 2026-11-03.

**Assessment (AI, 2026-11-08):** applied in the definition: both columns are dropped in `_clean` (27 features); `known` and `changes` say so, and the notes' drop bullet says that the notes' other model scores, the metric reason's and the splits comment's were measured with them in. Task probe without them, on the same 5 of 9 splits (the dummy's loss per split is unchanged, so the split sets are the same): the random forest scores 62.30 against the constant's 63.10 (62.22 with them), the linear model 80.04 (81.97) and LightGBM 88.84 (90.30); 0.1%, 6.6% and 3.9% of their predictions sit at the 0.1 EUR floor. `dataset check`: 0 errors, 0 warnings.

CC (2026-11-09, Andrej): columns held only for training rows stay out for now, no training-only role (cross-dataset item of 2026-11-09; MET-14, LEAK-41, MET-16); the notes list them.

CC (2026-11-09, Andrej): the training labels' maturity is stated in the notes (cross-dataset item of 2026-11-09, option B).

CC (2026-11-10, Andrej): the task stays on Year 0 split by client, with the yearly drift of the claim level in `splits_comment` (Review issue 6 (a), "Keep, with the drift sentence"); no rebuild on the AIcrowd years.

CC (2026-11-10, Andrej): the metric floor stays at 0.1 EUR (Review issue 7 (b), "0.1 EUR"), its reason restated under MET-13 as amended on 2026-11-09.

**Assessment (AI, 2026-11-10):** on the AIcrowd copy the mean cost per policy is 119.3, 119.0, 112.3 and 106.2 EUR in years 1 to 4 (0% to 6% a year). No fact favours a floor above 0.1 EUR: no minimum premium is published and the source records claim amounts down to 0.02 EUR (8 of 12,391 positive claims below 1 EUR); between 0.1 and 1 EUR only squared-error fits move (ridge 66.33 against 61.61, squared-error LightGBM 102.83 against 74.94; repeat 0, folds 0 to 2).

CC (2026-11-10, Andrej): ship (review page of 2026-11-10).

## Review

**Outcome:** added. The AI recommends shipping it; the metric's floor was lowered to 0.1 EUR on 2026-11-08 (issue 5,
Lennart), the collection's rule for a deviance floor. Year 0 of the 2017
French actuarial pricing game, from the R package CASdatasets (the organiser's copy; the game's own files are gone):
100,000 car policies of 91,488 clients of an unnamed French insurer, about 2010-11. The target is the policy's claim
total for the year in euros (0 for 88.9%), predicted when the premium is set, with no exposure column and no weight; all
policies of a client stay on one side of the split, tagged as forced from temporal; the score is the mean Tweedie
deviance (power 1.5, predictions floored at 0.1 EUR) as a stand-in for the game's market profit. Validity: SEL-1 holds;
USE-6 and the Tensions row on rating factors as amended on 2026-11-09 (Andrej): the drivers' sex is dropped, as French
law under EU law bars it today and the rule treats the ban as if it had always applied; USE-1 holds, fit
approximate (USE-8: next year's renewals with their claim history are the real task); USE-5 holds (negative totals from
legal recourse set to 0, +4.8% on total cost); LEAK-10 holds for all 27 features; SPLIT-1 and SPLIT-4 hold (grouped by
client); SPLIT-8: the forced split ships on Andrej's call of 2026-11-02, its cost stated, and the leak test across it
found none; PROV-8 and PROV-13 hold. The re-review of 2026-11-06 under the exposure rules finds nothing to weight: no
time on risk is realized, so MET-15 scores each policy unweighted, LEAK-41 has no weight to guard and MET-16 no survey
weight to act on; MET-14 holds by its per-contract clause (every policy is priced for a year; no year cut short can be
located, and the newest policies claim as their risk predicts, so at most about 9% of the policies in their first year
could be half years). Value: the task probe flags no_signal (TP-1, TP-2), which reads an R²-type skill (best R² 0.003);
on the declared deviance the random forest scores 62.44 against the constant's 63.10 (skill 0.011, 5 of 9 splits, task
probe) and 60.57 against 63.31 (skill 0.043, 3 folds, mediator), a small real signal (EV-3); at the 0.1 EUR floor
and without the drivers' sex the task probe's random forest scores 62.30 against 63.10 (62.22 with them); MET-11
holds (the deviance follows the game's profit at a
Kendall tau of 0.58 to 0.79 in simulated markets); MET-13 holds: the floor is 0.1 EUR (issue 5, 2026-11-08), kept under the
rule as amended on 2026-11-09 on the curator's call, since no fact favours a higher value and the floor ranks only
squared-error fits (issue 7, 2026-11-10). Quality: impossible values masked (CLEAN-11), make and model joined (CLEAN-12), the commune typed as text
(CLEAN-14), `pol_pay_freq` ordered by payments a year (2026-11-08, as in the two other pricing tables), the target in
euros as an exception to CLEAN-16 (2026-11-03). Weighed: the organiser's copy with documented columns (+), a canonical
pricing task (+), one claim year and a weak signal (-). Nothing is left open.

Changes made after the review panel of 2026-11-06 (AI), text only; rows, target, split, metric and floor unchanged: the
exposure paragraph rests the policy-year on the rules and on a risk-adjusted claim test of the newest policies, not on
the later year files (the organiser aged them from Year 0), and gives the share cut short; the yearly premium is cited
at the rules' Sec. 1 and 4.9; the notes and the metric reason state the smallest plausible mean (16.8 EUR) and the task
probe's share of predictions at the floor.

Changed on Lennart's marks of 2026-11-08 (rows, target and split unchanged; a build waits for your ask): the metric's
floor is 0.1 EUR (issue 5) and `pol_pay_freq` is an ordered category, Yearly < Biannual < Quarterly < Monthly; the
task probe was re-run at the new floor.

Changed on 2026-11-08 on Lennart's stance of australian_vehicle_insurance_2004_2005's issue 7 (rows, target, split and
metric unchanged): `drv_sex1` and `drv_sex2` are dropped, since sex is no rating factor of any insurance pricing task
of this collection; the task probe was re-run without them (random forest 62.30 against the constant's 63.10, 62.22
with them). The notes' other model scores were measured with the two columns in and say so.

**Main points:** Retag `DelayedTarget` instead of `ForcedGroupedFromTemporal` (issue 8)? Before that, no issue was open. Resolved on 2026-11-10 (Andrej): issue 6, the task stays on Year 0 split by client,
with a sentence on the yearly drift of the claim level (0% to 6% a year on the AIcrowd copy); issue 7, the floor stays
at 0.1 EUR, its reason restated under MET-13 as amended on 2026-11-09 (no fact favours a higher value; the floor ranks
only squared-error fits). Resolved on 2026-11-03: the
deviance is in (2), euros stay (3) and the name stays (4); verdict ship (Andrej). On 2026-11-08 the floor was lowered
from Andrej's 1 EUR to 0.1 EUR, following the collection's rule for a deviance floor, a convention that can change later
(5, Lennart); `pol_pay_freq` is ordered by payments a year (from issue 8 of
spanish_motor_insurance_coverage_level_2022_2024). The drivers' sex left the features on 2026-11-08, on Lennart's stance
that sex is no rating factor of any insurance pricing task (australian_vehicle_insurance_2004_2005's issue 7).

**Verdict (2026-11-10, Andrej):** ship (review page of 2026-11-10).

**Issues for Andrej and Lennart:**

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

5. **Keep the metric's floor at 1 EUR by amending the rule, or lower it to 0.1 EUR?**

   * **Problem:**
     - The deviance counts a prediction below 1 EUR as 1 EUR (Andrej, 2026-11-03)[^f3], while the rule as amended on
       2026-11-06 puts the floor two orders of magnitude (a factor of 100) below the smallest plausible mean, the
       average claim cost of the cheapest sizeable group of policies[^f1].
     - That mean is 16.8 EUR, so the rule asks for about 0.17 EUR, and 1 EUR is only 1.2 orders of magnitude (a factor
       of 17) below it.
     - The rule admits no exception[^f2], so 1 EUR can stay only if the rule changes: amend the rule, or lower the
       floor?
   * **Background:**
     - The floor is the lowest prediction the score takes: a prediction below it counts as the floor. For a policy that
       claims y euros the deviance at power 1.5 grows like 4y/sqrt(mu) as the prediction mu falls, without bound; for a
       policy without a claim it is 4 sqrt(mu), which stays small. So a lower floor costs only a model that prices a
       claiming policy near zero or below, and a model that never predicts below 1 EUR scores the same at every floor.
     - The smallest plausible mean is the mean claim cost of the cheapest rating cell (cover x use x bonus-malus band x
       first driver's age band) with at least 500 policies: Mini cover, WorkPrivate use, bonus-malus above 0.5 up to
       0.7, aged 26 to 40, 553 policies, 16.8 EUR. The next cells are 20.3 and 21.1 EUR, and other band edges give 14 to
       20 EUR (18.4 EUR on 922 policies when the band includes the bonus-malus of 0.5, where 78% of the policies sit),
       so 0.1 EUR is two orders below every one of them; 0.2 EUR would be 1.9 orders below 16.8 EUR. The portfolio mean
       is 123 EUR.
     - Where 1 EUR comes from: option B of issue 2 as the panel drafted it ("floor 1 EUR"). Andrej chose that option;
       the record gives no reason for the value itself, only that a floor must be stated.
   * **Effect on the task:** no insurer quotes a premium near 0 EUR, so both floors sit below any real premium; what the
     floor sets is how hard the benchmark punishes a model whose raw output is near zero or negative on a policy that
     then claims, and so whether such a model beats the constant prediction. At 1 EUR an untuned ridge regression beats
     the constant and ranks second of five; at 0.2 EUR and below it falls behind the constant, and the two LightGBMs
     swap places. The best family, the random forest, does not move.
   * **Experiments:** mean Tweedie deviance on the shipped repeat 0, folds 0 to 2, untuned models, lower is better (the
     mediator; re-run with the same numbers):

     | Model | Predictions below 1 EUR | Floor 1 EUR | Floor 0.2 EUR | Floor 0.1 EUR | Floor 0.01 EUR |
     |---|---|---|---|---|---|
     | Constant (training mean) | 0% | 63.31 | 63.31 | 63.31 | 63.31 |
     | Random forest | 0% | 60.57 | 60.59 | 60.59 | 60.59 |
     | Ridge | 4.3% | 61.61 | 64.31 | 66.33 | 81.37 |
     | LightGBM, squared-error loss | 4.6% | 74.94 | 90.92 | 102.83 | 190.85 |
     | LightGBM, Tweedie loss | 4.3% | 75.51 | 77.58 | 78.11 | 78.48 |

     - Each step from 1 to 0.2 to 0.1 EUR moves ridge by about as much as the random forest gains over the constant
       (2.7).
     - In the task probe (5 of 9 splits), 6.9% of the linear model's predictions, 4.3% of LightGBM's and 0.2% of the
       random forest's sit at the 1 EUR floor.
   * **Consistency:**
     - fremtpl2 and bemtpl97 got their floors under the same amendment (Lennart, 2026-11-06): 1e-4 claims per year, two
       orders below the smallest plausible rate and about 1/740 of the portfolio rate; the same ratio here gives 0.17
       EUR. Lowering the floor follows them.
     - Keeping 1 EUR departs from them with no fact that sets this case apart, other than that a currency has a round
       unit, so it takes an amendment[^f4]; worded for a unit of the scored currency, it leaves their claims-per-year
       floors as they are.
     - The deviance itself stays as decided in issue 2; only its floor is reopened, by the newer rule.
   * **Panel:** the claim auditor offered keeping 1 EUR as a recorded exception; the mediator ruled that out, since the
     rule admits none, which leaves an amendment (A).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep 1 EUR and amend the rule (implemented) | the definition stays; the rule allows a round unit of the scored currency; fremtpl2 and bemtpl97 are checked against the new wording | Andrej's value stays; a round number in euros; spares models that predict negative costs | a rule changed for one dataset; the 'two orders' bar no longer holds across the family, though a currency-unit wording leaves the claims-per-year floors of fremtpl2 and bemtpl97 as they are |
     | B | Lower the floor to 0.1 EUR | a prediction below 0.1 EUR counts as 0.1 EUR; models that predict below 1 EUR score worse | two orders below every cheapest rating cell, as the rule asks; follows fremtpl2 and bemtpl97; the best model does not move | changes Andrej's value; ridge falls behind the constant |

   * **Recommendation:** B, lower the floor to 0.1 EUR (rounded down from 0.17, so it is at least two orders of
     magnitude below every cheapest group, where 0.2 EUR would be 1.9): the amended rule asks for it, it treats this
     dataset like fremtpl2 and bemtpl97, and the best model's score does not move. Andrej set the 1 EUR, so he should be
     told of the change. **Decision:** A (keep 1 EUR, amend the rule) or B (0.1 EUR)?

   **Notes for the AI:** the mediator's options (a) and (b) are B and A here. On B: `params={"power": 1.5,
   "min_prediction": 0.1}` in `dataset.py`; the metric reason's "a prediction below 1 EUR counts as 1 EUR, 1.2 orders
   below the smallest plausible mean" becomes "a prediction below 0.1 EUR counts as 0.1 EUR, two orders below the
   smallest plausible mean", and the notes' "Metric floor" bullet gets the new value, the curator's call and the share
   at the new floor; re-run the task probe for that share (MET-13) and `dataset check`; append the curator's CC to the
   record; a MET-13 Cases row in `metrics.md` (main session). On A: amend MET-13 in `metrics.md` with the curator's
   wording (the mediator's example: "or a round unit of the scored currency"), the date and the curator, and check
   fremtpl2's and bemtpl97's 1e-4 floors against the new wording (a currency-unit wording leaves them as they are); the
   notes' bullet then cites the amendment. Either way, tell Andrej: under B his value of 2026-11-03 changes, under A his
   value enters the rule. Evidence: the claim auditor's a5.py and the mediator's floor.py in the panel folder of the
   exposure review of 2026-11-06 (floor.py re-run by the writer, same numbers); the 16.8 EUR cell comes from bonus-malus
   bands that are open at 0.5 (right-closed `pd.cut`), so they leave out the policies at exactly 0.5.

   [^f1]: **MET-13** (Must, amended 2026-11-06, Lennart): a metric undefined at the edge of its prediction domain floors
     the predictions; "The floor is a parameter the definition states ...: two orders below the smallest plausible mean,
     on the scale the metric scores (amended 2026-11-06, Lennart: 1e-4 claims per year on fremtpl2 and bemtpl97), and
     the task probe reports the share of predictions at the floor."
   [^f2]: Principles, "Exceptions and amendments": "A Must has no exceptions: only a higher-ranked Must overrides it,
     and anything else is an amendment."
   [^f3]: Issue 2 above, resolved on 2026-11-03 (Andrej): "(B), the mean Tweedie deviance (power 1.5, floor 1 EUR) as
     the stand-in for the game's profit"; the record's CC of 2026-11-03: "predictions floored at 1 EUR".
   [^f4]: Principles, "Consistent judgement": a decision that departs from a precedent with similar facts and names no
     fact that sets it apart goes back to the curator; one that would break a Must is offered as an amendment of the
     rule, not as an exception.

   **Lennart (2026-11-08, change):** Lower the floor to 0.1 EUR. highlight this mostly as us following a rule that we
   can change in the future

   **Resolved (2026-11-08, Lennart):** B, `min_prediction` is 0.1 EUR; the metric reason and the notes present it as
   the collection's rule for a deviance floor (two orders below the smallest plausible mean, MET-13 as amended on
   2026-11-06), a convention that can change later and not a property of the source, and the CC line names Andrej's
   1 EUR of 2026-11-03 as superseded. Task probe at the new floor (5 of 9 splits): the random forest 62.22 against the
   constant's 63.10, the linear model 81.97 and LightGBM 90.30 (66.28 and 70.90 at 1 EUR), with 0.1%, 6.7% and 3.8% of
   their predictions at the floor.

6. **Keep training and testing on Year 0 without the policies' claim history, measure what that hides, or rebuild on the AIcrowd years?**

   * **Problem:**
     - The insurer, like the game's players, fit its tariff on Year 0 and priced Year 1 knowing each policy's Year 0
       claims, while the benchmark trains and tests on Year 0, held out by client, so a model learns the test year's
       claim level and sees no claim history (dataset.py:198-203).
     - The plain Tweedie deviance scores the level as well as the order, so the same-year training gives every model
       a level a real tariff would have had to forecast, and the leak test across the split ran on the Gini, which
       cannot see a level (dataset.py:206-209).
     - On the AIcrowd copy of this portfolio the policy's past claims lift the Gini of next year's policies from 0.277
       to 0.305 (dataset.py:201-203), a record CASdatasets does not hold.
   * **Background:**
     - CASdatasets holds claims for Year 0 only; Years 1 to 4 ship without claims, and the bonus-malus `pol_bonus`,
       set at the start of the year, carries part of a policy's past (dataset.py:132, 140).
     - The AIcrowd Insurance Pricing Game (2020-21) reused the portfolio with claims for four years of 57,054 policies
       (228,216 rows), but noised the features (driver age off by a median 3 years, vehicle value by 2,945, make and
       model hashed), needs an account, and the copy on GitHub states no data licence (the record).
     - Four claim years give at most two windows that train on half the rows or more (years 3 and 4; year 2 would
       train on 25%), so a rebuild would still fall short of the three windows the rules ask for[^6a].
   * **Effect on the task:** the benchmark is easier on the level than Year 1 pricing, since the level comes from the
     test year itself, and harder on the ranking, since the model lacks the claim record; the skill against the
     constant, which learns the same level, is free of the first.
   * **Consistency:**
     - frempl_french_motor_personal_line, also one claim year, ships the same way.
     - pricing_game_2016_french_fleet and spanish_motor_insurance_coverage_level_2022_2024 are asked whether to add
       their units' records (their issues 13 and 9); there the record is in the release, here only in the AIcrowd copy.
   * **Unknown:** how much the claim level moves from one year to the next; on the AIcrowd copy, the mean cost per
     policy of each year and the deviance of a model fit on one year and scored on the next, against one fit on the
     scored year, would size it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep, with the note (implemented) | Year 0 split by client, as now; the notes give the AIcrowd figures (0.268, 0.277, 0.305) | the organiser's copy with clean, documented features under GPL; no change | the level comes from the test year; no claim record |
     | B | Keep, and size the year-to-year shift | A, plus the shift of the mean cost per policy between years and its effect on the deviance, measured on the AIcrowd copy and stated in the notes and the fit | says what the free level is worth; no rebuild | measured on noised features and part of the policies; a cluster run for the fits |
     | C | Rebuild on the AIcrowd years | years 1 to 3 train and year 4 tests, each policy's earlier claims as features | the next-year task with its record | noised features; an account and no stated licence; 57,054 policies; two windows at most, so forced again or an amendment; a new definition |

   * **Recommendation:** B: the claim record is not in this release, and the AIcrowd years bring it only with noised
     features, an unclear licence and a split that still falls short of the windows rule, so the task stays as
     defined; what the same-year level is worth should be measured and stated rather than assumed. **Decision:** A, B
     or C?

   **Notes for the AI:** on B, fetch AIcrowd's `training.csv` (the JuliaComputing/ScoringEngineDemo.jl copy behind the
   earlier measurement) into its own empty folder and read it with `python -I`; the mean claim per policy and the
   share with a claim per year are light pandas; the paired fits (year k to k+1 against k+1 on itself, the same
   policies, the deviance at power 1.5 and floor 0.1) run on the cluster (sbatch). Then state both in
   `splits_comment` and `fit_reason`, with a CC line and a CHANGELOG entry. On C, a new record and definition: check
   AIcrowd's terms, test the noise under PROV-3 (values perturbed for privacy are kept when no test measures damage),
   and the windows under SPLIT-14 and SPLIT-8.

   **Andrej (2026-11-09, discuss):** Can we do a split where we first do the grouped split, and then move the earlier
   points from groups with two entries to train? Or do we have year 0 and 1 for all clients?

   **Answer (AI, 2026-11-09):** Not on the shipped table, whose groups hold no earlier points. On the AIcrowd years the
   design can be built: it gives every test policy its own earlier years, and it also trains on the test year's claims
   of the other policies, which a split by year does not. Counted on the raw files, no model fitted.

   * **The shipped table (`pg17trainpol.csv`, `pg17trainclaim.csv`):**
     - Every row and every claim is of Year 0 (`id_year` has one value in both files); the split's group is the
       client.
     - 91,488 clients: 83,576 with one row, 7,385 with two, 470 with three and 57 with four to nine; the 7,912 clients
       with two rows or more hold 16,424 rows (16.4%).
     - A client's rows are its vehicles (16,424 distinct), each insured over the same Year 0. For 6,560 of the 7,912
       clients the policies started in different years (`pol_duration` differs), but the older policy's claims fall in
       the same year as the newer one's, so no row is an earlier point of another.
     - Moving each client's older policies to training (7,050 rows; 1,352 clients have all their policies of one age,
       so no order) would give 6,626 test rows, over the three folds of a repeat, a sibling vehicle's claims of the
       same year: the one part of the test year the grouping keeps out, as a client's other claims of the year are not
       known when its premiums are set. The split audit of 2026-11-01 found that part worth nothing: removing the test
       clients' siblings from training moved the random forest's Gini by -0.002 +- 0.003 (6 splits), and 11.5% of the
       vehicles have a claim when a sibling has one, 9.4% otherwise.
   * **Year 1 for all clients:** CASdatasets' `pg17testyear1` holds the same 100,000 policies of all 91,488 clients,
     but no claims, so Year 1 has no target and cannot hold a test row; it is the organiser's ageing of Year 0
     (dataset.py:148).
   * **The AIcrowd copy (the public `training.csv` of the split audit):** 57,054 policies, 57% of the 100,000, each
     with claims in four years (AIcrowd year k is pg17 Year k-1), so Years 0 and 1 have claims for those policies. It
     has no client key, so a client's vehicles cannot be kept together, and the features are noised (Background).
   * **Your design on AIcrowd:** 3 folds by policy; each test policy's years 1 to 3 go to training and its year 4 is
     tested. Per fold: 19,018 test rows, each with its three earlier years in training (26.8% with a claim there; a
     policy claims in year 4 at 7.7% after no earlier claim, 12.3% after one, 27.7% after three), and 209,198
     training rows.
   * **What it brings into training from the test year:** the year-4 rows of the other 38,036 policies, 18.2% of the
     training side. The level moves between years: the mean claim cost per policy is 119.3, 119.0, 112.3 and 106.2
     EUR in years 1 to 4 (a claim in 11.0%, 10.6%, 10.1% and 9.2% of the policies). A model learns year 4's level
     from those rows, where a tariff for year 4 would forecast it from years 1 to 3, and the deviance scores the level
     (problem, second bullet). The organisers may have built the later years, so the drift may be theirs (split
     audit's caveat).
   * **The clean form is a split by year:** year 4 trained on years 1 to 3 of all policies (75% of the rows) and year
     3 on years 1 and 2 (50%), the earlier claims as features: the same history for every test row and nothing of the
     test year in training. Year 2 on year 1 trains on 25%, so two windows, one short of the rules' three[^6a]; that
     is option C.
   * **What your design would need from the rules:** the forced split has two forms, IID or grouped with all of an
     entity's rows on one side; a test entity's earlier periods in training is a third form, so an amendment or an
     exception, and its leak test across the split would have to measure what the test year's rows in training give
     (wisconsin's member folds leaked the year's level, pricing_game_2016_french_fleet's contract folds did not)[^6b].
     The history itself is legitimate[^6a], and as features it needs no row moved: every year of a policy stays on
     one side and each row carries its own policy's earlier claims, as spanish_motor_insurance_coverage_level_2022_2024
     (issue 9) and pricing_game_2016_french_fleet (issue 13) propose.
   * **For this issue:** no new option. On CASdatasets the design moves only same-year siblings; on AIcrowd it is C
     with the test year's other policies added to training. B stays the recommendation; if you take C, its split by
     year, or the split by policy with the history as features, rather than this design.

   **Andrej (2026-11-09, discuss):** I don't want to read this amount of text. Distill to me what I can do and
   revisit what the right decision is

   **Answer (AI, 2026-11-09):** Keep the task as it is (A) and add one sentence on how far the claim level moves from
   year to year; no rebuild and no cluster run.

   * The claim history is not in this release: CASdatasets holds claims for Year 0 only, and Year 1 has no target.
   * Learning the test year's level helps every model and the constant alike, so the skill against the constant is
     untouched; the drift it hides is already counted on the AIcrowd years: the mean cost per policy is 119.3, 119.0,
     112.3 and 106.2 EUR, so 0% to 6% a year.
   * The only way to the history is the AIcrowd rebuild, which brings noised features, no stated licence, 57% of the
     policies and two windows, one short of the rule.

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep, with the drift sentence (implemented) | as now; the notes add the yearly level from the AIcrowd years | no change; the free level is sized | no claim history |
     | b | Rebuild on the AIcrowd years (C) | years 1-3 train, year 4 tests, past claims as features | the next-year task with the claim record | noised features, no licence, a forced split or an amendment |

   * **Recommendation:** a. **Decision:** a or b?

   **Andrej (2026-11-10, change):** Reply (a): Keep, with the drift sentence

   **Resolved (2026-11-10, Andrej):** a. The task stays on Year 0 split by client; `splits_comment` now says that
   training on the test year gives every model, the constant included, that year's claim level, which drifts by 0% to
   6% a year on the AIcrowd copy (mean cost per policy 119.3, 119.0, 112.3 and 106.2 EUR in years 1 to 4). No rebuild
   on the AIcrowd years[^6a].

   [^6a]: **SPLIT-14** (Must; amended 2026-11-08, Lennart): "A temporal task has at least 3 windows, and no window's
     train side holds less than 50% of the data", with one older window on at least 40% when two windows are above
     the floor; otherwise **SPLIT-8** (Must): the closest regime that keeps the rows, tagged forced from temporal.
     **USE-10** (Must): "For a known entity, its history is legitimate: the split is temporal and the previous outcome
     is a feature." Andrej, 2026-11-02: "Forced group splits should be fine" (the split comment).
   [^6b]: **SPLIT-8** (Must): "The closest regime is IID (tag `ForcedIIDFromTemporal`), or grouped by the entity when
     the periods are stacked and the entities recur across them (tag `ForcedGroupedFromTemporal`)", and "A forced
     split, grouped or IID, gets a leak test across the split and the leak probes: does a row share its outcome, its
     unit's outcome or its period's outcome with the other side". **SPLIT-14** (Must): "each window trains on what is
     known before it starts". splits.md's Cases: wisconsin_local_government_property_insurance_fund (member folds
     leaked the year's claim level, so yearly windows) and pricing_game_2016_french_fleet (the contract folds pass the
     test, so forced by contract).

7. **Set the metric's floor back to 1 EUR, where an insurer would clip, now that the 0.1 EUR floor decides how model families rank?**

   * **Problem:**
     - The floor went from 1 EUR to 0.1 EUR on 2026-11-08 by the collection's convention, two orders below the smallest plausible mean, which Lennart named "us following a rule that we can change in the future"[^7a].
     - Between the two floors the best model does not move, but untuned LightGBM fitted by squared error goes from 74.9 to 102.8 against the constant's 63.3, and ridge from ahead of the constant to behind it.
     - No insurer quotes a premium of 0.1 EUR or of 1 EUR, so what the lower floor adds to the score is how a model behaves on prices nobody charges: keep 0.1 EUR, or clip at 1 EUR?
   * **Background:**
     - A prediction below the floor is scored as the floor; at power 1.5 the cost of a low prediction on a policy that claims y euros grows like 4y/sqrt(mu), so dividing the floor by 10 multiplies that cost by about 3.2, while a policy without a claim costs almost nothing either way.
     - The floor's first reason was practice: "in pratice we would also clip to a reasonable number" (Lennart, 2026-11-04)[^7a].
     - The smallest plausible mean is 16.8 EUR (the cheapest rating cell with at least 500 policies), the portfolio mean 123 EUR; 1 EUR is 1.2 orders of magnitude below the former.
     - The game's rules and CASdatasets' page give no minimum premium (not checked further; the Unknown bullet).
   * **Effect on the task:** at 0.1 EUR the benchmark ranks the methods that fit squared error partly by their share of near-zero predictions (3.9% to 6.6% of the probe's linear and LightGBM predictions sit at the floor); at 1 EUR those predictions count as a minimum price, which is what an insurer would do with them.
   * **Experiments:** issue 5's run (the mediator, 2026-11-06; shipped repeat 0, folds 0 to 2, untuned, mean Tweedie deviance, lower is better):

     | Model | Floor 1 EUR | Floor 0.2 EUR | Floor 0.1 EUR | Floor 0.01 EUR |
     |---|---|---|---|---|
     | Constant (training mean) | 63.31 | 63.31 | 63.31 | 63.31 |
     | Random forest | 60.57 | 60.59 | 60.59 | 60.59 |
     | Ridge | 61.61 | 64.31 | 66.33 | 81.37 |
     | LightGBM, squared-error loss | 74.94 | 90.92 | 102.83 | 190.85 |
     | LightGBM, Tweedie loss | 75.51 | 77.58 | 78.11 | 78.48 |

   * **Consistency:**
     - The rule itself is the cross-dataset item "Set a deviance's floor where the actor would clip"; noaa_storm_events_damage asks the same for its $1 (its issue 14).
     - pricing_game_2016_french_fleet's 0.1 per vehicle-year is never reached by its GLM or a regularised LightGBM, so it has no such issue.
   * **Unknown:** the lowest premium the game accepted or a French insurer quotes for third-party cover; and how the benchmark's tuned methods rank at each floor, which a cluster run on the 9 shipped splits at 0.1, 1 and 5 EUR would show.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | 0.1 EUR (implemented) | as since 2026-11-08 | follows the collection's rule as it stands | ranks squared-error fits by outputs no insurer would charge |
     | B | 1 EUR | Andrej's value of 2026-11-03, as the clip an insurer applies | a near-zero prediction counts as a minimum price; the best model does not move | needs the rule changed (the cross-dataset item, B); 1 EUR is a round number, not a quoted minimum |
     | C | Measure first | the cluster run of the Unknown bullet, then A or B | the call on tuned methods, not untuned ones | the decision waits |

   * **Recommendation:** B, with the rule changed by the cross-dataset item: a price of 0.1 EUR and one of 1 EUR are the same decision for an insurer, so the score should not tell them apart; C if you want the tuned methods first. **Decision:** A, B or C?

   **Notes for the AI:** On B (after the cross-dataset item's B): `params={"power": 1.5, "min_prediction": 1.0}` in `dataset.py`; the notes' "Metric floor" bullet and the metric reason say the floor is the clip an insurer applies, with the fact and the curator's call, and keep the probe's share at the floor; re-run the task probe and `dataset check`; a CC line naming the 0.1 EUR of 2026-11-08 as superseded; a MET-13 Cases row; CHANGELOG entry. On C: `sbatch` on gpua100*, the benchmark's tuned LightGBM, CatBoost and RealMLP (squared error as configured) on the 9 splits at the three floors; then put A or B again with the table.

   **Andrej (2026-11-09, discuss):** Wait, this shouldn't matter at all, your pro and con arguments for one or the
   other don't make any sense, are there actual reasons for anything?

   **Answer (AI, 2026-11-09):** You are right for every model fitted with a cost-shaped loss: the floor moves only
   squared-error fits. Set 1 EUR, since the rule you accepted today puts the floor where the insurer would clip, and
   the old reason for 0.1 EUR (two orders below the smallest mean) is gone.

   * Between 1 and 0.1 EUR the random forest (60.57, 60.59), the Tweedie-loss LightGBM (75.51, 78.11) and the
     constant (63.31) keep their order.
   * Only ridge (61.61 to 66.33, ahead of the constant, then behind it) and squared-error LightGBM (74.94 to 102.83)
     change, through their 4-5% of predictions near zero or negative.
   * No fact picks 1 EUR over 0.1 EUR: no minimum premium is published. 1 EUR is your value of 2026-11-03 and lies
     far below the cheapest rating cell's mean (16.8 EUR), so it is a clip an insurer would apply to any price that
     low.

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | 1 EUR | the clip of 2026-11-03 back | the reason of the rule accepted today; a near-zero or negative output counts as a minimum price | 1 EUR is a round value, not a quoted minimum |
     | b | 0.1 EUR (implemented) | as now | no change | its only reason, the two-orders formula, was dropped today |

   * **Recommendation:** a. **Decision:** a or b?

   **Andrej (2026-11-10, change):** Reply (b): 0.1 EUR

   **Resolved (2026-11-10, Andrej):** b. The floor stays at 0.1 EUR; its reason in the notes and the metric reason is
   restated under MET-13 as amended on 2026-11-09[^7b]: no fact favours a higher value (neither the rules nor
   CASdatasets give a minimum premium; the source records claim amounts down to 0.02 EUR, 8 of the 12,391 positive
   claims below 1 EUR), and between 0.1 and 1 EUR the floor ranks only fits by squared error (ridge 66.33 against
   61.61, squared-error LightGBM 102.83 against 74.94), while the random forest, the Tweedie-loss LightGBM and the
   constant keep their scores and order.

   [^7a]: **MET-13** (Must, in main; amended 2026-11-06, Lennart): "The floor is a parameter the definition states, as practice clips a model's output before scoring (Lennart, 2026-11-04, on bemtpl97: "in pratice we would also clip to a reasonable number"): two orders below the smallest plausible mean". Issue 5 (Lennart, 2026-11-08): "Lower the floor to 0.1 EUR. highlight this mostly as us following a rule that we can change in the future".
   [^7b]: **MET-13** (Must; amended 2026-11-09, Andrej; not yet in main): the floor is "the lowest value the use
     case's actor acts on (a minimum premium, the smallest amount the source records), stated with its fact, and never
     above the smallest plausible mean on the scale the metric scores". 0.1 EUR lies below the cheapest cell's mean
     (16.8 EUR).

8. **Retag `DelayedTarget` instead of `ForcedGroupedFromTemporal`, now that a one-moment release is forced only when its target is of that moment?**

   * **Problem:**
     - The definition is tagged `ForcedGroupedFromTemporal` (Andrej, 2026-11-02), from when every release with too few periods was forced[^8a-pg].
     - Every row is predicted at one shared moment, the start of the policy year, when each premium is set, and the target arrives after it, with the year's claims, a window that has closed for every policy, which is a `DelayedTarget`[^32a-pg].
     - The tag alone changes: the split stays grouped by client.
   * **Background:** the policies are Year 0 of the pricing game, and every age and duration is counted from the beginning of that year; Years 1 to 4 of the panel carry no claims.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedGroupedFromTemporal` (implemented) | the tag and its line stay | the decision of 2026-11-02 stands | the tag says time was lost, which the one shared moment contradicts |
     | B | `DelayedTarget` | the tag and its `Time basis:` line name the shared moment and the target's window | follows the record's facts and the sharpened rule; no cost: the shared moment leaves nothing for a later window to test | changes a decided tag |

   * **Recommendation:** B. **Decision:** A or B?

   **Notes for the AI:** on B, swap the tag in `data_tags` and write the `Time basis:` line as SPLIT-32 asks for a `DelayedTarget` (the moment, the window, closed for every row, what the split cannot test: the next moment); add a CC line; the split code does not change.

   [^8a-pg]: **SPLIT-8** (Must, sharpened 2026-11-13): a release that is one moment, every row predicted at the same point, is forced only when its use case looks forward from a target of that moment or of unknown timing; otherwise SPLIT-32 gives it `Retrospective` or `DelayedTarget`.
   [^32a-pg]: **SPLIT-32** (Should): `DelayedTarget` is one shared prediction moment with the target arriving after it, in a window closed for every row; a random or grouped split then draws train and test from that one moment and window.

**Review panel:** ship after changes (mediator). A focused re-review of 2026-11-06 under LEAK-41 and MET-14 to MET-16,
by a claim auditor and a mediator. Claims: 13; 9 hold (one with an off citation, now fixed), 1 holds only as a
conclusion (a row is a whole policy-year: the organiser's later year files cannot show it, so it now rests on a
risk-adjusted claim test), 1 not met (the share cut short, now given), 1 untested and not testable on this release (a
year of an older policy cut short), 1 refuted against the rule as amended on 2026-11-06 (the 1 EUR floor, issue 5).
Blind review: not part of this tier. Agreed: no exposure column, no weight and no scoring column, each policy scored
unweighted; the per-contract target; all 9 folds can be scored; the stand-in's reason. Disputed: no agent disputes (no
advocate or critic in this tier); the mediator ruled out the claim auditor's remedy of keeping 1 EUR as a recorded
exception, which leaves an amendment (issue 5, option A). For the curator: issue 5 (the mediator's issue 1; its options
(a) and (b) are issue 5's B and A). This block replaces the panel of 2026-11-01, which issues 2 to 4 cite.

<details><summary>Mediator</summary>

**Mediator (2026-11-06): pricing_game_2017_french_mtpl, exposure re-review (focused tier: claim auditor only)**

Inputs: the claim auditor's report with its scripts (a1 to a5), the task probe, principles.md, MET-13 to MET-16 in
metrics.md, the definition, REVIEW.md issue 2 (where the 1 EUR floor was set) and the record. This tier has no advocate,
critic, task gamer or precedent checker, so I took precedent from the Cases table in metrics.md. I ran one decisive
experiment.

**1. Judgment record**

Verdict: ship after changes.

Validity: none of the four rules has anything to act on, because there is no realized denominator. LEAK-41 is not
triggered and needs no weight. MET-15 holds: scored unweighted, sample_weight None, no scoring columns. Probe 22 does
not apply. SPLIT holds (settled earlier, not reopened).

Value: MET-13 (Must) is violated. The 1 EUR floor is 1.2 to 1.3 orders below the smallest plausible mean (16.8 EUR); the
amended rule asks for two. Fix it in the definition: floor 0.1 EUR. MET-14 (Should): a per-contract target is right, but
the notes do not give the share cut short. Fix it in the notes. MET-11 and MET-2 hold: the stand-in reason is right and
all 9 folds can be scored.

Quality: the reason behind "a row is a whole policy-year" is unsupported (EV-1). Replace it with the risk-adjusted test,
which supports the conclusion. The citation "rules, Sec. 4" is off (writing).

Weighed: none.

For the curator: issue 1. It changes Andrej's floor of 2026-11-03 under Lennart's rule of 2026-11-06. MET-13 is a Must,
so "an exception with Andrej's reason" cannot be recorded. The only way to keep 1 EUR is to amend MET-13.

**2. Agreed facts (claim auditor's measurements, none contested)**

- Row count: 100,000 Year-0 policies. Each appears once in each of the year files pg17testyear1-4. The outer merge of
  Year 0 with Year 1 leaves 0 rows unmatched on either side.
- The later year files are built by the organiser by mechanical ageing, Year 0 to Year 1 and Year 1 to Year 2:
  - pol_duration and pol_sit_duration go up by 1 for all 100,000 policies; vh_age for 99,999;
  - there are 0 changes of coverage, payd, usage, vehicle or second driver;
  - yet 37,314 Year-0 policies had a situation change in the year before Year 0.
  So these files say nothing about cancellations or late starts in Year 0.
- pol_duration runs from 1 to 41, with 8,743 policies at 1. The rules count it "from the beginning of the current year"
  (Sec. 4.7).
- Raw claim share: 13.70% at duration 1, 13.15% at 2-5, 12.32% at 6 and above.
- Risk-adjusted test: a LightGBM claim-indicator model without the two durations, 5 folds by client.
  - Observed over expected: 1.011 at duration 1 (1,198 against 1,184.4, z 0.43); 0.994 at 2; 1.017 at 2-5; 0.995 at 6
    and above.
  - The 95% lower bound at duration 1 is 0.954. If cut years averaged half a year, at most about 9% of the duration-1
    policies could be part years.
- Older policies: a cut short in Year 0 cannot be located (no cancellation date, no Year-0 exposure). It is untested and
  cannot be tested on this release.
- Pay-as-you-drive: 4,152 policies (Yes) against 95,848 (No). None of the 31 columns is a mileage. Under a Tweedie model
  without pol_payd, observed over expected is 0.953 for payd rows and 1.247 for the others, so the pol_payd feature
  carries the lower usage.
- Container: metric inputs {}, scoring_columns [], sample_weight None. All 9 folds can be scored: the train-mean
  constant scores 60.86 to 64.75; predicting 1 EUR everywhere scores 433.5 to 493.4.
- Citations in the rules:
  - "annual premium for policy i" is in Sec. 1, and the "yearly cotation" in Sec. 4.9;
  - Sec. 4 holds "present once in each file", not anything about annual premiums.
- Floor against the smallest plausible mean:
  - The smallest cell means (cover x usage x bonus band x age band, at least 500 policies) are 16.8 EUR (Mini,
    WorkPrivate, bonus 0.5-0.7, age 25-40, n 553), 20.3 and 21.1.
  - Two orders below 16.8 EUR is 0.17 EUR.
  - The portfolio mean is about 123 EUR. fremtpl2's floor sits 1/738 below its portfolio rate (1e-4 against 0.0738), and
    the same ratio here gives 0.17 EUR.
- How a lower floor changes the score: for y > 0 the deviance at power 1.5 rises with 4y/sqrt(mu) as mu falls; for y = 0
  it is 4 sqrt(mu), which is bounded. So a lower floor penalises near-zero or negative predictions made on claimants.
- Andrej's reason for 1 EUR: the record has none of his own. He picked option B as the domain practitioner drafted it
  ("floored at a stated 1 EUR"); the only reason given was that the floor must be stated (REVIEW.md issue 2).

Decisive experiment (mine). Does the floor change the outcome? Shipped repeat 0, folds 0-2, untuned models, mean Tweedie
deviance:

| model | below 1 EUR | floor 1 | floor 0.2 | floor 0.1 | floor 0.01 |
|---|---|---|---|---|---|
| dummy | 0% | 63.31 | 63.31 | 63.31 | 63.31 |
| random forest | 0% | 60.57 | 60.59 | 60.59 | 60.59 |
| ridge | 4.3% | 61.61 | 64.31 | 66.33 | 81.37 |
| LightGBM, L2 loss | 4.6% | 74.94 | 90.92 | 102.83 | 190.85 |
| LightGBM, Tweedie loss | 4.3% | 75.51 | 77.58 | 78.11 | 78.48 |

At floor 1, ridge beats the dummy and ranks second. At 0.2 and below it loses to the dummy, and the two LightGBMs swap
places. The random forest, the best family, does not move. So the floor decides whether a model that predicts negative
or near-zero costs beats the constant. Each step from 1 to 0.2 to 0.1 moves ridge by about as much as the random forest
gains over the dummy (2.7). This matches the auditor's 1.4 per order.

**3. Changes to make now (no decision needed)**

1. Exposure paragraph, the "so" clause (EV-1, MET-14). The organiser's later year files cannot show whole Year-0 years,
   so give the conclusion the risk-adjusted test as its reason. Proposed text:
   "Exposure: no exposure column, and none is needed. Each policy is quoted a yearly premium (rules, Sec. 1 and 4.9) and
   is present once in every year's file (Sec. 4), so a row is a policy-year by design. The later years' files are the
   organiser's ageing of Year 0, so they cannot show that no Year-0 year was cut short. The shortest pol_duration is 1,
   so no policy was written during Year 0. The newest policies claim as often as their risk predicts: a claim model
   without the two durations expects 1,184 claims at duration 1 and sees 1,198 (1.011, z 0.43), where part years would
   claim less. At the 95% lower bound (0.954), at most about 9% of them could be half years."
   Keep the raw 13.7% against 12.3% only as background.
2. MET-14 (Should): the share cut short, in one clause: "Share cut short: none can be located; for new policies, bounded
   by the test above; for older ones, not observable (no cancellation date)." This follows
   spanish_motor_insurance_2015_2018, which gives the share (2,055 of 37,090). What sets this case apart: here the share
   cannot be counted.
3. Citation (writing): "annual premiums (rules, Sec. 4)" becomes "(rules, Sec. 1 and 4.9)". "Present once in every
   year's file" stays with Sec. 4.
4. Whichever floor issue 1 settles, the notes and the metric reason state the smallest plausible mean (16.8 EUR, the
   cells above) and the task probe's share at the floor (MET-13).

**4. Issues for the curator, ranked**

Issue 1 (P6, Must). MET-13: the Tweedie floor of 1 EUR.

- Problem: MET-13 as amended on 2026-11-06 asks for a floor two orders below the smallest plausible mean. That mean is
  about 17 EUR, so the floor should be about 0.17 EUR. 1 EUR is 1.2 to 1.3 orders below.
- Effect: the floor decides whether ridge beats the dummy (61.61 against 63.31 at 1 EUR; 64.31 at 0.2; 66.33 at 0.1). It
  also swaps the two LightGBMs. The best family, the random forest, does not move.
- Is it a conflict? No. This is MET-13 failing on its own; no higher rule asks for 1 EUR. principles.md says a Must has
  no exceptions, so "record an exception with Andrej's reason" is not open. The record also has no reason of Andrej's
  for the value itself, only for stating a floor.
- Best evidence, lower it: the amended rule; the 16.8 EUR cell mean; the same ratio to the portfolio mean as fremtpl2
  and bemtpl97.
- Best evidence, keep 1 EUR: Andrej's call of 2026-11-03. A higher floor spares models that predict negative costs
  (LightGBM-MSE was "punished hard" at 71.6 in issue 2). It is a round number in the scored unit.
- Options:
  - (a) Lower min_prediction to 0.1 EUR. This is the remedy ladder's "fix the definition", and my recommendation: the
    strict reading of "two orders below 16.8". 0.2 EUR would be 1.92 orders below.
  - (b) Keep 1 EUR by amending MET-13, for example "or a round unit of the scored currency". This would then also reopen
    the 1e-4 floors of fremtpl2 and bemtpl97 for consistency.
- Decision needed: (a) or (b). Andrej should be told, since it changes his value.

Issue 2: none. The other points (the inference, the MET-14 share, the citation) need no decision and are in section 3.

Not settled by the rules and out of scope today: the task probe flags no_signal (TP-1, TP-2). The random forest's
deviance gain over the dummy is 0.66 in the probe and 2.7 on my three folds. That point was settled earlier and today's
change does not reopen it. A lower floor does not change the random forest.

**5. Disputed points**

None between agents: this is a focused tier. I settled the facts as above. The auditor's floor finding stands, and my
run extends it from one LightGBM to the probe families. The auditor's proposed remedy "or keep 1 EUR as a recorded
exception" is not available, because MET-13 is a Must (principles.md, Exceptions); it becomes option (b), an amendment.

**6. Consistency with precedent**

- fremtpl2 and bemtpl97 (MET-13, 2026-11-06, Lennart): floor 1e-4 claims per year, two orders below the smallest
  plausible rate, about 1/740 of the portfolio rate. Option (a) follows them (0.1 to 0.17 EUR). Option (b) departs, with
  no fact that sets this case apart except that a currency has a round unit. That is consistency flag 1, so the route is
  an amendment, not an exception.
- spanish_motor_insurance_2015_2018 (MET-14): per-contract target kept, share cut short given. This case follows it; the
  share is "none locatable, bounded for new policies" because the release has no cancellation date.
- MET-15 and LEAK-41 cases (fremtpl2, bemtpl97, australian, frempl, pg16, spanish coverage): all have a realized
  denominator. This one has none, so not declaring a weight is consistent.
- REVIEW.md issue 2 (2026-11-03, Andrej): the Tweedie deviance stays. Only the floor parameter is reopened, and only by
  the amended rule of 2026-11-06 (a newer rule beats an older call).

</details>

<details><summary>Claim audit</summary>

**Claim auditor (2026-11-06): pricing_game_2017_french_mtpl, exposure re-review (focused tier)**

The definition's notes ("Exposure") were tested on the data. Scripts in the panel folder: a1.py counts, a3.py duration
O/E, a4.py year continuity, a5.py floor and payd, a2.py folds; the rules are the text of the archived
3rdPricingGame.pdf; pg17testyear1-4 were fetched from CASdatasets 227fb56 for the tests.

**Verdict:** the exposure paragraph holds on the data; no weight is right (MET-14, MET-15, LEAK-41 have nothing to act
on). One inference in it is unsupported (the year files are built by the organiser, so they cannot show whole Year-0
years) and should rest on the test below instead; MET-14 asks for the share cut short, which the notes do not give as a
number. Outside the four named rules: the 1 EUR floor sits about 1.3 orders, not two, below the smallest credible mean
(MET-13 as amended today).

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | "The 100,000 policies are each present once in every year's file" | comments, Exposure | Y0 vs pg17testyear1..4 ids; rules Sec. 4 intro | HOLDS | outer merge Y0-Y1: 100,000 both, 0 left/right only; rules: "Every file contains exactly 100,000 policies ... present once in each file" | - |
| 2 | "... with annual premiums (rules, Sec. 4)" | comments, Exposure | read rules | HOLDS, citation off | "annual premium for policy i" is Sec. 1 (p. 1); Sec. 4.9: "you must provide a yearly cotation". Sec. 4 itself says nothing about annual premiums | NOTE |
| 3 | "so a row is a whole policy-year" (inferred from 1 and 2) | comments, Exposure | is the year-file continuity evidence on Year-0 time on risk? Y0->Y1 and Y1->Y2 field changes | INFERENCE UNSUPPORTED (the conclusion holds by test 5) | Y0->Y1: pol_duration +1 and pol_sit_duration +1 for 100,000 of 100,000, 0 coverage, payd, usage, vehicle or second-driver changes, vh_age +1 for 99,999; Y1->Y2 the same (sit +1 for 100%, 0 coverage changes). Yet 37,314 Year-0 policies (28,571 of them older than 1 year) had a situation change in the year before Year 0. The later years are aged mechanically by the organiser ("drivers willing to purchase insurance for Year t", pricingame.Rd), so their presence says nothing about cancellations or late starts in Year 0. The README hedges ("the release does not say so") | EV-1, MET-14 |
| 4 | "The shortest pol_duration is 1, so no policy was written during Year 0" | comments, Exposure | min/max; rules Sec. 4.7 | HOLDS | min 1, max 41, 8,743 at 1; Sec. 4.7: duration "accounted from the beginning of the current year". The rules say oldest 45 years, data 41 (minor doc mismatch); whether the count floors or ceils is not stated, test 5 covers the consequence | - |
| 5 | "the newest policies claim more often, not less (13.7% at duration 1 against 12.3% from 6 on), where part years would claim less" | comments, Exposure | recount; then the decisive test: a claim-indicator model WITHOUT pol_duration/pol_sit_duration (LightGBM, 5 folds by client), observed over expected claims by duration | HOLDS | any claim row: 13.70% (dur 1), 13.15% (2-5), 12.32% (>=6), 12.65% overall (positive target: 11.75% / 11.10%, the 11.7% of the blind review of 2026-11-01). Risk-adjusted O/E: dur 1 1.011 (1,198 vs 1,184.4, z 0.43); dur 2 0.994; 2-5 1.017; >=6 0.995. The raw comparison was confounded by risk mix; the adjusted one could have refuted and did not. 95% lower bound 0.954: if cut years averaged half a year, at most about 9% of duration-1 policies could be part years | MET-14, EV-1 |
| 6 | "nothing points to a year cut short" (all policies) | comments, Exposure | cancellations or lapses of older policies in Year 0 | UNTESTED | no cancellation date, no Year-0 exposure, and the later year files are constructed (row 3), so a mid-year end of an older policy cannot be located; O/E for duration >= 6 is 0.995 but older policies have no full-year reference group | MET-14 |
| 7 | "For the 4,152 pay-as-you-drive policies the real exposure, the distance driven, is not released" | comments, Exposure | count; column list; rules Sec. 4.10; pricingame.Rd | HOLDS | 4,152 Yes / 95,848 No; none of the 31 columns is a mileage; neither source names one. payd claims 9.4% vs 12.8%, cost 79.6 vs 124.8 EUR; under a Tweedie LightGBM without pol_payd the payd rows come in 24% below the others relative to prediction (O/E 0.953 vs 1.247): the shipped pol_payd feature carries the lower usage; payd does not change between years (0 of 100,000) | MET-14 |
| 8 | "The target is the policy's claims of the year, scored unweighted ... (MET-14, MET-15)"; no weight | comments, Exposure; metric | container spec; MET-14 per-contract clause; MET-15 | HOLDS | spec inputs {}, scoring_columns [], sample_weight None; the target is a per-contract total with a constant planned term (one year, quoted yearly, Sec. 1 and 4.9), which MET-14 keeps; no realized denominator exists, so MET-15 and LEAK-41 have no weight to place; probe 22 not applicable | MET-14, MET-15, LEAK-41 |
| 9 | MET-14's per-contract clause: "the notes give the share cut short" (implied obligation) | metrics.md MET-14 | do the notes give it? | NOT MET (wording) | the notes say "nothing points to a year cut short" without a share or a bound; the bound exists (row 5) | MET-14 |
| 10 | metric original: profit over Years 1-4, 10-player markets, three cheapest, 170% bankruptcy | metric.original | rules Sec. 1 | HOLDS | Rule 2 (k = 10, 1/2, 1/4, 1/4 among the 3 cheapest, per client), Rule 3 (1.7 x), objective (2) sums t = 1..4 (text says "over five years"; the formula is what the original quotes) | MET-1, MET-11 |
| 11 | stand-in: the profit cannot be computed on the release | metric.reason | release contents | HOLDS | pg17testyear1-4 have 31 columns, no claim; no other players' premiums | MET-2, MET-11 |
| 12 | metric computable on every fold | implied (MET-2) | scorer(c) on a train-mean constant and on the floor per fold | HOLDS | 9 folds, 33,307-33,369 rows, 30,496 test clients each, 0 client overlap, 3,599-3,829 positive rows; constant 60.86-64.75; all-1 EUR 433.5-493.4 (finite) | MET-2 |
| 13 | "a prediction below 1 EUR counts as 1 EUR" (min_prediction = 1.0) against MET-13 as amended 2026-11-06: the floor two orders below the smallest plausible mean | metric.params | smallest credible mean: cells cover x usage x bonus band x age band with n >= 500; floor sensitivity of an untuned Tweedie LightGBM (5 folds by client) | REFUTED against the amended rule (the 1 EUR was Andrej's call of 2026-11-03, before it) | smallest cell means 16.8 EUR (Mini, WorkPrivate, bonus 0.5-0.7, age 25-40, n = 553), 20.3, 21.1; two orders below is about 0.2 EUR, 1 EUR is 1.2-1.3 orders below. Its OOF predictions run down to 0.01 EUR, 2.6% below 1 EUR; mean deviance 68.30 (floor 0.1), 66.91 (1), 65.27 (5), constant 63.29: the floor moves this model by 1.4 per order, twice the random forest's gain over the dummy in the task probe (63.10 to 62.44). Task probe share at the floor: linear 6.9%, LightGBM 4.3% | MET-13 |

**Ranked: refuted, unmet and untested (principles: validity first, Must first)**

1. MET-13 floor (Must, amended today; outside the four rules named for this audit). The 1 EUR floor is about 1.3 orders
   below the smallest credible mean policy cost (about 17-21 EUR), not two. It matters: the floor changes an untuned
   Tweedie learner's score by more than the best family's gain over the constant. Mildest remedy: the curator either
   lowers min_prediction to 0.1 or 0.2 EUR (two orders below about 17 EUR), or keeps 1 EUR as a recorded exception with
   Andrej's reason; either way the notes state the smallest plausible mean.
2. The "so a row is a whole policy-year" inference (EV-1; MET-14, Should). True as a conclusion, but the given reason
   cannot carry it: the Year 1-4 files are the organiser's mechanical ageing of the Year-0 portfolio (every duration and
   situation +1, no endorsement in 100,000 policy-years). Mildest remedy: replace the sentence's "so" clause and the raw
   13.7% vs 12.3% with the risk-adjusted test: duration-1 policies claim at 1.011 times (z 0.43) what a model without
   the durations expects, where part years would claim less; at most about 9% of them could be half years.
3. MET-14's share cut short not given (Should). Mildest remedy: one clause, "share cut short: none locatable; for new
   policies bounded by the O/E above; for older ones not observable".
4. Untested: mid-year ends of older policies (row 6). No data can test it in this release; the remedy is the clause in
   3, not a change.
5. Citation (NOTE): "annual premiums (rules, Sec. 4)" should read rules Sec. 1 and Sec. 4.9; Sec. 4 holds "present once
   in each file".

Held: 4,152 payd and no mileage; no weight, MET-15 and LEAK-41 not engaged; the metric's original, stand-in reason and
computability on all 9 folds.

</details>

## Reference

CASdatasets (Dutang C., Charpentier A.), `pg17trainpol`, `pg17trainclaim`, `pg17testyear1`-`pg17testyear4`,
"French Motor Third-Part Liability datasets used for 100 percent Data Science game", third pricing game of the French
Institute of Actuaries (16 November 2017). https://github.com/dutangc/CASdatasets/blob/master/man/pricingame.Rd

AIcrowd (2020-21). Insurance Pricing Game (Imperial College London). https://www.aicrowd.com/challenges/insurance-pricing-game

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook). Merged with the AIcrowd lead `aicrowd_insurance_pricing_game_2021` (same portfolio).
