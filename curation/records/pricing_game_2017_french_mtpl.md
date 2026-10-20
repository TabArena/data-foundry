---
unique_name: pricing_game_2017_french_mtpl
name: pg17trainpol / pg17trainclaim (CASdatasets, 2017 French pricing game) / AIcrowd Insurance Pricing Game 2020-21 (training.csv)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
- Non-IID (Temporal)
year: '2017'
domain: insurance
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://github.com/dutangc/CASdatasets/blob/master/man/pricingame.Rd
- https://github.com/dutangc/CASdatasets/tree/master/data
- https://actinfo.hypotheses.org/86
- https://www.aicrowd.com/challenges/insurance-pricing-game
- https://github.com/JuliaComputing/ScoringEngineDemo.jl/blob/main/assets/training_data.csv
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

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

## Reference

CASdatasets (Dutang C., Charpentier A.), `pg17trainpol`, `pg17trainclaim`, `pg17testyear1`-`pg17testyear4`,
"French Motor Third-Part Liability datasets used for 100 percent Data Science game", third pricing game of the French
Institute of Actuaries (16 November 2017). https://github.com/dutangc/CASdatasets/blob/master/man/pricingame.Rd

AIcrowd (2020-21). Insurance Pricing Game (Imperial College London). https://www.aicrowd.com/challenges/insurance-pricing-game

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook). Merged with the AIcrowd lead `aicrowd_insurance_pricing_game_2021` (same portfolio).
