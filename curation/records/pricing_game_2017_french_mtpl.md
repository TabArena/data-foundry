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

**Assessment (AI, 2026-11-01):** added as `datasets/_dev/tabarena-v0pt2/pricing_game_2017_french_mtpl/` by /add-dataset with the full review panel; the open questions are in its `REVIEW.md`. Recommend shipping; only issue 1, the forced grouped split of one claim year (open against how_much_did_it_rain, with frempl, australian, rand and spanish 2022-2024), could turn it to `No`. Changes after the panel: impossible licence ages and one 7,901 kg weight made missing, `vh_model` joined to the make, the commune typed as text, the split and metric reasons restated with measured figures (rows, target and folds unchanged). Corrections to the notes above: the screening's `rmse` (MET-4, MET-11) gives way to the normalized Gini as the stand-in for the game's profit (Gini 0.20-0.37 per split; a Tweedie GLM best, 0.319); the AIcrowd challenge and the JuliaComputing `training_data.csv` links are related tables, not the source, and the name no longer cites AIcrowd. `required_split` and `tags` wait for your marks on the field rows (issue 1), as do the metric (issue 2), the target scale (3) and the name (4). Priority 3: gap + (insurance thin), use case 0 (fit approximate), source + (the organiser's copy, every column documented), shape + (100,000 policies, grouped), risk - (the forced split is open; weak signal).

CC (2026-11-02, Andrej): the forced grouped split ships (issue 1 (a); the record takes `Grouped (NON-IID)` and `Non-IID (Grouped)` as the issue says): "Forced group splits should be fine. Regarding forced IID, did you make sure there are no leaks? Whenever there are no leaks we can ship." Recorded in SPLIT-8 (amended 2026-11-02: a forced grouped split ships; a forced IID split ships only when the leak test across the random split finds none). The amended SPLIT-8 covers the grouping by client of one year, so no separate amendment of the grouped branch is made.

**Assessment (AI, 2026-11-02):** the leak test across the forced grouped split (SPLIT-8 as amended 2026-11-02) finds none, on the 9 shipped splits with untuned LightGBM (Tweedie), base Gini 0.223 +- 0.016. (1) Shared rows and hidden groups: no test row has an exact copy on the training side, nor a near copy (every feature but commune, value and weight); keys that link rows of different clients carry nothing: a household proxy (commune and first driver's age, sex and licence age) links 4.2% of test rows and a vehicle proxy (commune, model, age, value) 0.85%, and their training-side mean target as a feature changes the Gini by -0.000 +- 0.004 and +0.003 +- 0.004; the client's own other vehicles, removed from training on random folds, change it by -0.002 +- 0.003 (split audit). (2) Shared period: the file is one year, so every split shares it; the training side's same-year mean target of the test row's department or commune (out of fold) changes the Gini by -0.005 +- 0.010 and -0.005 +- 0.005, and removing from training the rows of half the test communes, against as many random rows, changes it by +0.008 +- 0.029: no shared local shock. (3) Features from other rows' outcomes: only `client_n_vehicles` (a count of policies, no outcome; drop-one -0.000 +- 0.009) and `pol_bonus` (start-of-year value, column audit) span rows; the bonus of a policy without a claim tells whether a sibling claimed at AUC 0.516. how_much_did_it_rain's `No` named a measured leak; none is found here.

CC (2026-11-03, Andrej): the metric is the mean Tweedie deviance (power 1.5, predictions floored at 1 EUR) as the stand-in for the game's profit, not the normalized Gini (issue 2 (B) in pricing_game_2017_french_mtpl): "Use mean_tweedie_deviance and implement it in the library". Added to the metric library under scikit-learn's name.

CC (2026-11-03, Andrej): the name `pricing_game_2017_french_mtpl` stays (issue 4 (A)): the source's own title; the notes say the target sums every guarantee of the cover.

CC (2026-11-03, Andrej): ship (verdict). The target stays in euros (issue 3 (A)), an exception to CLEAN-16: the deviance scores the predicted cost's level in euros, where a Gini scores only the order; the metric, the mean Tweedie deviance, checked.

## Reference

CASdatasets (Dutang C., Charpentier A.), `pg17trainpol`, `pg17trainclaim`, `pg17testyear1`-`pg17testyear4`,
"French Motor Third-Part Liability datasets used for 100 percent Data Science game", third pricing game of the French
Institute of Actuaries (16 November 2017). https://github.com/dutangc/CASdatasets/blob/master/man/pricingame.Rd

AIcrowd (2020-21). Insurance Pricing Game (Imperial College London). https://www.aicrowd.com/challenges/insurance-pricing-game

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook). Merged with the AIcrowd lead `aicrowd_insurance_pricing_game_2021` (same portfolio).
