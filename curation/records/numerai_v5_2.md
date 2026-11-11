---
unique_name: numerai_v5_2
name: numerai v5.2
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 2
decision_markers:
- Needs extensive data wrangling
- Anonymized
tags:
- Non-IID (Temporal)
- Review Prio 1 (Atlas)
collections:
- New (BeyondArena)
original_source: Company
year: '2025'
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://github.com/numerai/example-scripts/tree/master/numerai
v2_path: datasets/_dev/tabarena-v0pt2/numerai_v5_2_1m/dataset.py
source_row: 706
type_adapter_id: curation-record-v1
---

## Comments

temporal split on era, likely need to add feature neutralization: https://github.com/numerai/example-scripts/blob/master/numerai/feature_neutralization.ipynb?

**Assessment (AI, 2026-10-07):** Added as `numerai_v5_2_1m`: eras 1-1235 (6.88M stock-weeks), target `target_ender_20` (the `target` of v5.2), Numerai's 780 `medium` features, three 52-era test windows after Numerai's 4-era embargo. The signal is real but tiny: a LightGBM shaped like Numerai's example model correlates 0.006-0.018 per era with the target (t = 3-9), yet its R² stays at or below 0.0003, so RMSE mostly ranks shrinkage towards 0.5. The 75 Faith features were designed over two test windows (+0.002-0.004 per era; noted). Feature neutralization post-processes predictions, not data. Licence: Numerai's Terms of Service §4.2 allow use "solely for the purpose of participating in Tournaments" and forbid redistribution. numerai28_6 is an older, era-less release.

**Assessment (AI, 2026-10-20):** priority 2 for the review of the added dataset: gap -, use case -, source +, shape +, risk - (Issue 3: 75 Faith features designed with test-era targets, kept as a potential leak). Large anonymised temporal finance panel with real but tiny signal; RMSE mostly ranks shrinkage.

**Correction (AI, 2026-10-20):** the assessment of 2026-10-07 says the Faith features were designed over two test windows; their design period (eras 1080-1191) covers all of the oldest window, all of the middle one and eras 1184-1191 of the newest, so parts of all three. Its gain of +0.002-0.004 per era is also superseded: on the shipped splits ridge gains +0.0043, +0.0013 and +0.0056 (eras 1184-1191), +0.0010 after the release.

**Assessment (AI, 2026-10-20):** re-check by the full review panel: ship after changes (mediator). The split holds (the 4-era gap covers the 3-era overlap of the 20-day targets), and the task is a ranking of the stocks within each week, not forecasting (the id changes every era; a stock's newest known target correlates about 0 with its target). The signal is small but real on the shipped splits (per-era correlation 0.0071 / 0.0142 / 0.0154, t 3.3 / 7.7 / 8.1), fragile on the newest window; tuned methods must beat the constant 0.5 window by window or the dataset goes to `TBD -> 2nd Tier`. Under RMSE the model ranking agrees with Numerai's per-era correlation at Kendall tau -0.11 to 0.39, pooled `pearsonr` at 0.89-0.93, so the panel recommends `pearsonr` (TP-6). The 75 Faith features gain about 28% of the signal in eras 1080-1131; the panel recommends dropping them (LEAK-31). Open for the curator in the folder's REVIEW.md: the metric, the Faith features, `medium` against `all`, v5.2 against v5.3. Priority 2: gap -, use case - (fit approximate: the Faith features and the metric gap), source +, shape +, risk - (the Faith features designed with test-era targets, a measured leak open in issue 3).

CC (2026-10-21, Lennart): the declared metric documents the original use case's metric; overrule it only when it is biased or wrong (evidence from the paper); keep the note of the original metric (TP-6 amended).

**Assessment (AI, 2026-10-21):** metric of numerai_v5_2_1m set to `pearsonr` (was RMSE): Numerai's per-era CORR is no listed metric name; pooled Pearson tracks it within 0.0002 per model on the shipped windows (every era's target mean is 0.5) and agrees with its model ranking at Kendall tau 0.89-0.93, RMSE at -0.11 to 0.39. Needs a rebuild to reach the container.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source mean_group_pearsonr {"method": "numerai_corr"} — Numerai's CORR, the per-era numerai_corr averaged over eras (docs.numer.ai, Correlation (CORR)), with `era` (the time column) as its group input; scored metric changed from pooled pearsonr.

CC (2026-10-26, Lennart): issue 3: "ok, follow your recommendation": drop the Faith features (LEAK-31).

CC (2026-10-26, Lennart): issue 4: "yes ship all": Numerai's `all` set without its 372 Faith features, 2,376 features (exactly v5.0's `all`).

CC (2026-10-26, Lennart): issue 7: "Create the v6 data record, keep v5.2 as a frozen release, and search for community mirrors if any exist, otherwise we can keep our local versions".

**Assessment (AI, 2026-10-26):** applied: `all` without the 372 Faith features (2,376 features; `dataset check` clean, 2,025,745 rows); the download notes say Numerai retired v5 on 2026-10-16 and that no community mirror matches our files (the Hugging Face upload Mcdonald82/numerai-v5.2 has the same train.parquet but validation only to era 1206), so our local files stay the only exact copy; task probes (3 windows, scored by R²) flag no_signal, drift_baseline and unstable as before, while Numerai's example LightGBM reaches per-era CORR 0.0094-0.0127 on the 2,376 features; the new record numerai_classic_v6 holds the v6.0 facts. No open issue is left, so the folder's REVIEW.md is removed.

CC (2026-10-26, Lennart): verdict ship.

**Assessment (AI, 2026-11-05):** the shared `mean_group_pearsonr` changed on 2026-11-05 (Lennart, huesken_sirna_efficacy issue 6): an era whose target varies but whose predictions are all equal scores 0 instead of being left out; an era with a constant target stays out. Scores of non-constant predictions are unchanged; `numerai_tools` gives NaN for such an era, so a constant prediction is the one case where the two differ.

CC (2026-11-10, Lennart): test windows (`numerai_v5_2_1m`, issue 12), marked discuss: "does this mean our horizon was a full year? that is way too much no?". The horizon audit keeps 52 eras, so by his instruction ("if the current time horizon makes sense and is justifiable keep it and resolve them") the issue resolves as A: the three newest years, eras 1184-1235, 1132-1183 and 1080-1131.

CC (2026-11-10, Lennart): the declared horizon (52 weekly eras, a 4-era gap, windows starting at eras 1184, 1132 and 1080) is checked, as Numerai ranks a model by its one-year average score and advises retraining at major data releases, so a model fit before the window predicts 52 weekly eras.

**Assessment (AI, 2026-11-10):** applied: `temporal` unchanged; `splits_comment` now gives Numerai's ranking as the reason for one year per window in place of the example notebooks' long validation period (eras 575 on), and the reason for walking back from the newest: the 2,376 features are v5.0's set of July 2024 (about era 1125), so the three newest years lie as close to that date as three one-year windows allow, though not after it (45 of the 52 eras of the oldest window, 1080-1131, come before it); windows above the floor reach back to era 716 (51.4%). Horizon audit (model-free): "Your model's reputation is just its 1 year average score", which "directly determines the rank of models on the model leaderboard" (https://docs.numer.ai/numerai-tournament/scoring); "it's usually best to re-train your models when major versions are released" (https://docs.numer.ai/numerai-tournament/data; v5.0 in July 2024, v6.0 on 2026-10-16); participants refit from weekly to once per release (https://forum.numer.ai/t/how-often-do-you-re-train-your-model/8164). A target resolves about five weeks later, so the 4-era gap holds. 13-era windows give 41 candidates, 26-era 20, 104-era 5.

## Reference

Website https://numer.ai/data/v5.2
