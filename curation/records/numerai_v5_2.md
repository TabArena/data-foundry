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
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Later'
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

**Assessment (AI, 2026-10-20):** re-check by the full review panel: ship after changes (mediator). The split holds (the 4-era gap covers the 3-era overlap of the 20-day targets), and the task is a ranking of the stocks within each week, not forecasting (the id changes every era; a stock's newest known target correlates about 0 with its target). The signal is small but real on the shipped splits (per-era correlation 0.0071 / 0.0142 / 0.0154, t 3.3 / 7.7 / 8.1), fragile on the newest window; tuned methods must beat the constant 0.5 window by window or the dataset goes to `TBD -> 2nd Tier`. Under RMSE the model ranking agrees with Numerai's per-era correlation at Kendall tau -0.11 to 0.39, pooled `pearsonr` at 0.89-0.93, so the panel recommends `pearsonr` (TP-6). The 75 Faith features gain about 28% of the signal in eras 1080-1131; the panel recommends dropping them (LEAK-31). Open for the curator in the record's Review: the metric, the Faith features, `medium` against `all`, v5.2 against v5.3. Priority 2: gap -, use case - (fit approximate: the Faith features and the metric gap), source +, shape +, risk - (the Faith features designed with test-era targets, a measured leak open in issue 3).

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

## Review

**Outcome:** added as `numerai_v5_2_1m`. Resolved on 2026-11-10: the test windows stay the three newest years, eras
1184-1235, 1132-1183 and 1080-1131 (issue 12), one year of 52 weekly eras each, as Numerai ranks a model by its
one-year average score; `splits_comment` now gives that reason and why the windows walk back from the newest.

**Main points:** Open: none. Resolved on 2026-11-10: the three newest years stay the test windows, one year each
(issue 12).

**Horizon:**

* **Verdict:** keep the 52-era windows (high confidence): Numerai ranks a model by its one-year average score and
  advises retraining at major data releases, so a model fit before the window predicts 52 weekly eras.
* **Length:** "Your model's reputation is just its 1 year average score" and "This directly determines the rank of
  models on the model leaderboard" (https://docs.numer.ai/numerai-tournament/scoring); "it's usually best to re-train
  your models when major versions are released" (https://docs.numer.ai/numerai-tournament/data). Participants refit
  anywhere from weekly to once per release (https://forum.numer.ai/t/how-often-do-you-re-train-your-model/8164). The
  splits comment's earlier reason (the example notebooks validate from era 575 on) was weak and is replaced by these.
* **Gap:** 4 eras: a target resolves about a month later, so at era T the newest known target is era T-5.
* **Time frame:** eras 1 to 1235 (about 2003 to August 2026); which years to test is issue 12.
* **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | A | 52 eras, a 4-era gap (implemented) | one year per window: eras 1184-1235, 1132-1183 and 1080-1131 | the year Numerai ranks a model on; every season in each window | a participant who refits within the year is scored as if frozen |
  | B | 13 eras | 41 candidates | models participants who retrain more often | a 20-day target spans 4 eras, so a window holds only about three separate target periods; not what Numerai ranks on |
  | C | 26 eras | 20 candidates | models participants who retrain more often | no source; not what Numerai ranks on |
  | D | 104 eras | 5 candidates | two years of markets per window | twice the host's year |

* **Recommendation:** A: one year is how Numerai ranks a model, and a model fit before the window predicts all 52
  eras. **Decision:** A, B, C or D?

**Resolved (2026-11-10, Lennart):** A, kept by the horizon audit, as instructed ("if the current time horizon makes
sense and is justifiable keep it and resolve them"); issue 12's answer gives why a full year, the record's CC line
says the declared horizon is checked, and `splits_comment` gives Numerai's ranking by the one-year score and its
advice to retrain at major releases as the reason.

**Issues for Lennart:**

12. **Keep the three newest years of eras, or spread the windows over the ten eligible years?**

   * **Problem:**
     - The newest window (eras 1184-1235, about September 2025 to August 2026) always stays, and since 2026-11-10 the
       other two are chosen from the use case and statistics of the data, and walking back from the newest needs its
       own reason[^nu-split15].
     - Windows of 52 eras that keep at least half the rows for training reach back to era 716 (about September 2016),
       so the eligible history spans ten years and several market regimes, while today's windows cover the three
       newest years.
     - Numerai builds its features to predict the target over the eras it already has, and the 2,376 features we
       ship are v5.0's set of July 2024 (about era 1125), so the older a window, the more of its targets were known
       when the features were built and chosen.
   * **Background:**
     - Dates: Numerai publishes none for v5.2. Eras are weekly Fridays; era 1240 is the Friday before our download of
       5 October 2026, and v6 dates its weekly eras from 3 January 2003 (record `numerai_classic_v6`), so era N is
       about 3 January 2003 plus N-1 weeks. The notes' "v5.0 rebuild (July 2024, about era 1125)" fits this
       reading (era 1125 is 19 July 2024).
     - Each window is 52 eras, a year, so every window covers all seasons, and today's three windows are already
       three different years. The length and the 4-era gap stay as they are[^nu-split12].
     - The target is ranked and binned within each era, so its distribution is the same in every window (mean 0.499
       to 0.501, p10 0.25, median 0.5, p90 0.75): no target statistic tells the windows apart. No feature is missing
       in any candidate window, and every window holds 5,900 to 7,000 stocks per era.
     - B spreads the windows evenly over the ten eligible years (the 1st, 5th and 10th candidate); the year of the
       2020 crash, eras 872-923 (65.1% train share), is a candidate too.
   * **Statistics:** from the candidate table (100,000-row samples of each side for the drift; rows and stocks from
     all rows). PSI, the population stability index, compares a feature's distribution in the window with its train
     side; the median is over the 2,376 features.

     | Eras | About | In | Test rows | Stocks per era | Train share | Median PSI | Largest PSI |
     |---|---|---|---|---|---|---|---|
     | 1184-1235 | Sep 2025-Aug 2026 | A, B | 361,712 | 6,956 | 94.4% | 0.021 | 1.30 |
     | 1132-1183 | Sep 2024-Aug 2025 | A | 333,081 | 6,405 | 89.5% | 0.021 | 1.38 |
     | 1080-1131 | Sep 2023-Aug 2024 | A | 327,025 | 6,288 | 84.8% | 0.022 | 1.45 |
     | 976-1027 | Sep 2021-Sep 2022 | B | 353,103 | 6,790 | 74.9% | 0.026 | 1.70 |
     | 716-767 | Sep 2016-Sep 2017 | B | 305,065 | 5,866 | 51.4% | 0.042 | 2.61 |

   * **Effect on the task:** Under A the score covers September 2023 to August 2026, two of its three years after
     the feature set was fixed. Under B it also covers the 2022 sell-off and 2016-2017, but in eras whose targets
     Numerai had when it built many of the features, so a model can score there with help that a model deployed on
     new weeks never gets.
   * **Unknown:** Which feature families Numerai built after 2016-2022, and how much they gain on those eras: v5.2
     does not date its families, and measuring it is a separate leak check, not part of choosing the windows.
   * **Consistency:**
     - You dropped the 372 Faith features on 2026-10-26 because Numerai chose them with the targets of our test
       eras[^nu-leak31]; v5.0's feature set is the same kind of choice by the host, and A keeps the windows as close
       to its date as three one-year windows allow (the oldest, 1080-1131, lies mostly before it, as `fit_reason`
       says).
     - aeolus_rebuilt_1m has the window question open under the rewritten rule; there the proposal moves windows to
       other seasons, which numerai's one-year windows already cover.
   * **Sources:** the definition `datasets/_dev/tabarena-v0pt2/numerai_v5_2_1m/dataset.py` (`temporal`,
     `splits_comment`, `fit_reason`, the Faith and Features bullets of `curation_comments`); the records
     `curation/records/numerai_v5_2.md` (CC 2026-10-26) and `curation/records/numerai_classic_v6.md` (the dates of
     v6); the candidate table `.venv/bin/python -m data_foundry.curation.cli dataset windows numerai_v5_2_1m --root
     datasets/_dev/tabarena-v0pt2` (11 windows: the tool counts eras for the floor, and by rows the oldest, from era
     664, trains on 47.1%, so 10 are eligible, from era 716 to era 1184).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Three newest years (implemented) | tests eras 1184-1235, 1132-1183 and 1080-1131 | the years closest to deployment; two of three after the feature set was fixed; three different years, each with all seasons | three adjacent years; no window in the 2020 crash or the 2022 sell-off |
     | B | Spread over ten years | tests eras 1184-1235, 976-1027 and 716-767 | adds the 2022 sell-off and 2016-2017; spread evenly over the eligible years | two windows in eras whose targets Numerai had when it built many of the features; the oldest trains on 51.4% of the rows |

   * **Recommendation:** A: walking back has its reason here, since the eras before July 2024 are the ones Numerai
     could use to build the features, so the three newest years are the cleanest test the data allows, and one-year
     windows already cover every season in three different years. **Decision:** A or B?

   **Notes for the AI:** on A, write the reason into `splits_comment`: the newest window always stays; the two
   before it because the 2,376 features are v5.0's set of July 2024 (about era 1125) and Numerai builds features
   with the targets of the eras it has, so older windows would test on eras that shaped the features (LEAK-31); one
   year per window covers every season; the candidates reach back to era 716 (51.4% train share). Add a CC line to
   the record and a dated CHANGELOG entry (SPLIT-15). On B, `temporal = Temporal(on="era",
   splits=TemporalSplits(window=52, unit="unique", gap=4, cutoffs=(1184, 976, 716)), horizon=52,
   horizon_unit="weeks", gap=4, gap_unit="weeks", time_unit="weeks")`. Built with `TemporalSplits.splits` on the
   definition's frame: test 361,712, 353,103 and 305,065 rows (all kept, under the 500k budget), train 6,492,875,
   5,154,231 and 3,537,616 (94.4%, 74.9%, 51.4%); the default 1M sample takes eras 1021-1179, 813-971 and 536-711.
   Then rewrite `task_summary.split`, `fit_reason` ("within the oldest test window"), `splits_comment`, the History
   and row-budget bullets; a CC line, a CHANGELOG entry and `dataset check`.

   [^nu-split15]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): "The newest window is always a test window ... Prefer windows in other years, then other seasons, then
     other months, weeks or days, over the windows just before the newest. Walking back from the newest is one choice
     among others and needs its reason too, such as a history too short for others, or a use case that only cares
     about the weeks after a refit."
   [^nu-split12]: **SPLIT-12** (Should): the horizon is a human judgment from the source, such as the refit cadence.
   [^nu-leak31]: **LEAK-31** (Should): supervised feature selection on the full labelled set: measure it; keep with a
     note when small, remove it when we can; a selection the source published (a feature set the host released) is
     decided case by case. Cases: numerai_v5_2_1m (the 372 Faith features, chosen with the targets of test eras
     1080-1191, dropped; 2026-10-26).

   **Lennart (2026-11-10, discuss):** does this mean our horizon was a full year? that is way too much no?

   **Answer (AI, 2026-11-10):**
   - Yes: each window is a year of 52 weekly eras, and a model fit before the window predicts all 52 without a refit.
   - The year holds because it is how Numerai judges a model: it ranks a model by its one-year average score ("Your
     model's reputation is just its 1 year average score", https://docs.numer.ai/numerai-tournament/scoring) and
     advises retraining at major data releases ("it's usually best to re-train your models when major versions are
     released", https://docs.numer.ai/numerai-tournament/data). Participants refit anywhere from weekly to once per
     release (https://forum.numer.ai/t/how-often-do-you-re-train-your-model/8164).
   - 13 or 26 eras would model participants who retrain more often, down to weekly, and score them over a quarter or a
     half year, which is not what Numerai ranks on.

   **Resolved (2026-11-10, Lennart):** A, as implemented, by the instruction "if the current time horizon makes sense
   and is justifiable keep it and resolve them": the three newest years stay, eras 1184-1235, 1132-1183 and 1080-1131
   (test 361,712, 333,081 and 327,025 rows; train 94.4%, 89.5%, 84.8%), 52 eras each with the 4-era gap. `temporal` is
   unchanged. `splits_comment` gives Numerai's ranking by the one-year score and its advice to retrain at major
   releases as the reason for the length, in place of the example notebooks' validation period, and the reason for
   walking back: the three newest years lie as close to v5.0's feature date (July 2024, about era 1125) as three
   one-year windows allow, though not after it (45 of the 52 eras of the oldest window come before it);
   `task_summary.split` names the ranking. The record has the decision and the horizon sign-off as CC lines. `dataset
   check`: 0 errors; its 2 warnings come from checks of the data that are not about the windows (a feature name read
   as an exposure, the target's middle bin at 50% of the rows) and are not settled here.

## Reference

Website https://numer.ai/data/v5.2
