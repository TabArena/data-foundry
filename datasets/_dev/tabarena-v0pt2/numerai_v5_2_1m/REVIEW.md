# numerai_v5_2

**Outcome:** added as `numerai_v5_2_1m`. Under the rule on choosing test windows, rewritten on 2026-11-10, the AI
recommends keeping the three one-year windows, eras 1184-1235, 1132-1183 and 1080-1131 (issue 12): the eras further
back are the years whose targets Numerai could use to build the features we ship. `dataset.py` is unchanged until
you decide.

**Main points:** Keep the three newest years of eras as the test windows, or spread them over 2016-2026 (issue 12)?

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
