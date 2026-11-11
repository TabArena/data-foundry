---
unique_name: kickstarter
name: kickstarter
checked_by:
- Lennart
- Alex
- Mustafa
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
priority: 2
tags:
- Non-IID (Temporal)
- Free Text (Sentences)
collections:
- TexTabBench
- TabSTAR
- AutoML_MM
original_source: Company
year: '2026'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/yashkantharia/kickstarter-campaigns
- https://webrobots.io/terms-and-conditions/
- https://webrobots.io/kickstarter-datasets/
- https://www.kaggle.com/datasets/codename007/funding-successful-projects
- https://www.openml.org/search?type=data&id=46668
notebook_path: datasets/beyond_iid/temporal/kickstarter/kickstarter.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/kickstarter/dataset.py
source_row: 736
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Leak fixed: dropped the creator's project profile (profile blurb) and staff_pick; the task is predicting at launch.** The raw `profile` JSON is the project's profile page (state, blurb, colours, link text such as "Follow along!"); its blurb is present for 34,032 successful and 0 of 69,970 failed projects, in every year 2009-2025. LightGBM AUC on the temporal splits 0.924 -> 0.904 (leak audit 2026-09-24). Other kept features are known at launch (goal, deadline, launched_at, category, location, name, blurb, prelaunch_activated, creator), except `staff_pick`: "Projects We Love" can be awarded during the campaign; 92.4% of staff picks succeed (27,514 of 29,793) vs 57% otherwise; dropped too (~0.02 AUC): the task simulates predicting at launch.

Scraped Kickstarter results, 2014–Feb 2019, needs to be shuffled since all successful campaigns come first; we should get the newest data from the website; likely need to adjust currency for inflation and time drift and currency; we could try to make the data time-independent by some slight preprocessing to create an IID task; might need to remove length-columns?; might need to change date preprocessing and use proper date preprocessing/encoding from skrub; TODO check raw data again

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Web Robots publishes a scraped snapshot with no task; the Kaggle copy is a dataset, not a competition, so no metric is defined.

**Assessment (AI, 2026-10-31):** the benchmark MulTaBench (https://arxiv.org/abs/2605.10616) carries a related version, "Kickstarter", not this record's data, so no collection tag: Text-tabular; AutoML Multimodal kick_starter_funding (OpenML 46668); the record links a different Kaggle snapshot (yashkantharia).

**Assessment (AI, 2026-10-31):** the benchmark STRABLE (https://arxiv.org/abs/2605.12292) carries a related version, "Kickstarter Projects", not this record's data, so no collection tag: Raw file Kickstarter_projects_Feb19.csv from TextTabBench (webrobots.io scrape); the paper links the kemical Kaggle set instead. Subsampled by STRABLE to 75,000 rows.

**Assessment (AI, 2026-11-01):** MulTaBench's "Kickstarter" now has its own record, `kick_starter_funding` (`No`, `Data Quality Issue`: its label is pledged >= 1.05 x goal, not goal met), and STRABLE's "Kickstarter Projects" its own, `kickstarter_projects_webrobots` (`No`, `Duplicate`). The reject check of 2026-11-01 corrects the note above for STRABLE: its file is the Feb 2019 Kaggle file of this record's first link, an older snapshot of this record's own Web Robots source with the same target (PROV-6). 79,399 of that file's projects are missing from the 2026 scrape this record pins, so merging older Web Robots scrapes could add them.

**Assessment (AI, 2026-11-10):** priority for the review of the test windows and horizons, which this record never had. Priority 2: gap 0, use case 0, source + (Web Robots' monthly scrapes), shape +, risk - (issue 2: the scrape cuts the newest year's outcomes).

CC (2026-11-11, Lennart): Review issue 2, B ("Option B: Launch date, cut at 60 days before the scrape."): the windows are dated by launch (`launched_at`) with a 60-day gap, the longest campaign, and the 1,673 projects launched from 13 November 2025 11:00 on, 60 days before the scrape's newest deadline, are dropped, so the newest year is cut where its outcomes are complete.

CC (2026-11-11, Lennart): Review issue 1, C ("Option C: All six years.") with reply (b) to the consistency check ("Reply (b): Nine years, 2017 to 2025"): the test windows are the nine launch years 2025 back to 2017, in place of the three newest years by creation; SPLIT-14 as amended on 2026-11-11 admits the three oldest, signed off here: 2019, 2018 and 2017 train on 47.0%, 40.2% and 32.4% of the projects (three windows under half, six at or above it).

CC (2026-11-11, Lennart): the declared horizon (one calendar year of launches, a 60-day gap, windows starting 2025, 2024, 2023, 2022, 2021, 2020, 2019, 2018 and 2017) is checked, as no source gives a horizon or a refit cadence, and a year holds every season and loses the least of its newest window to the scrape (Review horizon, ok).

**Assessment (AI, 2026-11-11):** applied issue 2 (B) and issue 1 (C, reply b): `_clean` drops the 1,673 projects launched from 2025-11-13 11:00 on (74.2% successful; 60 days before the scrape's newest deadline, 2026-01-12 11:00), leaving 185,444 projects (62.50% successful); `temporal` declares one-year windows by `launched_at` from 2025 back to 2017 with a 60-day gap. Test 23,096 (1 January to 13 November 2025), 20,466, 12,096, 10,790, 9,523, 9,432, 11,187, 12,312 and 14,286 projects; train 159,342, 140,261, 128,277, 117,767, 108,032, 98,615, 87,250, 74,581 and 60,168 (85.9%, 75.6%, 69.2%, 63.5%, 58.3%, 53.2%, 47.0%, 40.2% and 32.4% of the projects). Success in the test years runs from 55.0% (2017) to 71.1% (2025), on the train sides from 58.3% to 61.3% (`dataset windows`); at most one training project per window (3 over the nine train sides, campaigns longer than 60 days) had not ended when its window starts. `task_summary`, the notes and `splits_comment` give the windows, the gap and the dating by launch, and drop the reason "not enough data per month" (1,500 to 2,200 projects a month). `dataset check`: 0 errors, 0 warnings, with `splits_train_under_half` accepted on the CC line above.

## Review

**Outcome:** added. On 2026-11-11 you dated the projects by launch with a 60-day gap and dropped the launches of the
scrape's last 60 days (issue 2, B), chose the nine launch years 2017 to 2025 as test windows, the three oldest training
on 47.0%, 40.2% and 32.4% of the projects (issue 1, C with reply b), and kept the one-year horizon (H, A).

**Main points:** Settled on 2026-11-11: nine one-year windows by launch date, 2025 back to 2017, with a 60-day gap, on
185,444 projects (issues 1 and 2); the one-year length holds, a convention no source contradicts (H). Nothing is left
to decide.

**Horizon:**

* **Verdict:** keep the one-year windows (medium confidence): no source gives a horizon or a refit cadence, a year holds
  every season, and a shorter newest window would be largely cut off by the scrape; the dating by creation is the weak
  point (Gap, Time frame).
* **Length:** declared as one calendar year of creation dates. Web Robots publishes monthly scrapes without a task
  (https://webrobots.io/kickstarter-datasets/), and the Kaggle copy is a dataset, not a competition: no horizon and no
  refit cadence found (Web Robots, the Kaggle page, Kickstarter's help pages). The stated reason, "data from just one
  month is not enough to create a robust test set" (`splits_comment`), does not hold: 1,500 to 2,200 projects were
  created in every month of 2024 and January to September 2025. What a year does give: every season (success by month
  of creation ranges from 58.7% in July to 64.7% in March), and a newest window that the scrape cuts by about a fifth
  rather than by half. The year is a convention, not a sourced horizon.
* **Gap:** none. A campaign runs at most 60 days by Kickstarter's rule
  (https://help.kickstarter.com/hc/en-us/articles/115005128434-What-is-the-maximum-project-duration; 3,586 projects in
  the data run longer, up to 121 days), but the windows are dated by creation, and creation to deadline takes 52 days
  at the median, 154 at the 90th percentile and 736 at the 99th. So 1.9% to 3.2% of each train side (2,133 to 5,333
  projects) were still running when the window starts; they succeed at 60% to 73%. 12.5% of the 2025 test projects
  have a creator with such a project, and in 92% of those it had ended before the test project launched. Dated by
  launch, the prediction point, 0.5% to 0.9% (634 to 1,389) would still run past the window's start.
* **Time frame:** projects created from April 2009 to December 2025 in the scrape of 12 January 2026; the six years
  2020 to 2025 keep half the projects for training (2020: 54.2%). The scrape holds only projects that had ended, so
  the newest year misses those still running or not yet launched: 2,727 projects created in 2025 Q4 against 5,198 in
  2024 Q4 and 5,673 to 6,244 in each earlier quarter of 2025. Had 2024 been cut the same way (its projects moved a
  year forward against the scrape date), 20% of them (4,310) would be missing, and those succeed at 73.9% against
  66.9% for the rest, so the 2025 window's 69.8% probably understates its year by about 1.4 points. Dropping the
  launches of the last 60 days before the scrape (1,673 projects, 74.2% successful) and dating by launch would leave
  only the few campaigns longer than 60 days missing; that is a change of the time column, not of the window length.
* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | A | One year (implemented) | calendar years of creation, no gap: 6 candidates above the floor, 2020 to 2025 | 6 windows of 9,581 to 21,400 projects (issue 1's C; today's three: 13,056 to 21,400) | every season (success by month of creation 58.7% to 64.7%); the scrape cuts the newest window by about a fifth rather than by half | no source; dated by creation, so 1.9% to 3.2% of each train side was still running when the window starts |
  | B | Six months | 13 candidates from 2019 H2 | 13 candidates of 4,373 to 12,425 projects | nine windows across years and seasons | no source for a shorter cadence; the newest half holds 8,400 projects against about 12,000 in a full half |
  | C | A quarter | 26 candidates from 2019 Q3 | 26 candidates of 2,023 to 6,244 projects | nine windows across years and seasons | no source for a shorter cadence; 2025 Q4 holds less than half a usual quarter |

* **Recommendation:** A: a year holds every season and loses the least of its newest window to the scrape, and no source
  supports a shorter cadence. **Decision:** A, B or C?

**Lennart (2026-11-11, ok):** As implemented (A).

**Resolved (2026-11-11, Lennart):** A: one-year windows, kept. With issue 2 (B) they are dated by launch instead of
creation, with a 60-day gap (Kickstarter's longest campaign), and the launches of the scrape's last 60 days are
dropped, so the newest window (1 January to 13 November 2025) is complete but for campaigns longer than 60 days; at
most one training project per window had not ended when its window starts. `splits_comment` gives this block's reason
for the length (no source gives a horizon or a refit cadence; a year holds every season and loses the least of its
newest window to the scrape) and drops "not enough data per month", which this block found false (1,500 to 2,200
projects a month). The record has the horizon CC line. `dataset check`: 0 errors, 0 warnings.

**Issues for Lennart:**

1. **Which years should the test windows be, and how many?**

   * **Problem:**
     - The three test windows are the newest three years of creation dates (2023, 2024 and 2025), while six years (2020
       to 2025) keep half the projects for training.
     - Since 2026-11-10 the newest window always stays, the others are chosen from the use case and statistics of the
       data with other years first, and a task gets about as many windows as a random split of its size would get
       train-test splits[^ks-split15].
     - A random split of 187,117 projects gets three repeats of three folds, nine splits, more than the six one-year
       windows above the floor[^ks-split14].
   * **Background:** The share of successful projects rises from 63.7% (2020) to 69.8% (2025), while every train side
     sits at 58.7% to 61.7%. Pre-launch pages spread over these years (41% of the projects created in 2020 had one, 61%
     in 2025), which is the largest drift in every window; the category mix shifts most in 2024 and 2025. The scrape
     holds 9,600 to 13,100 projects a year in 2020-2023 and about 21,000 in 2024 and 2025. 2020 is the first pandemic
     year. The 2025 window lacks about a fifth of its projects, those still running at the scrape (Horizon). PSI, the
     population stability index, compares a feature's distribution in the window with its train side; above 0.25 is
     usually read as a large shift.
   * **Statistics:** from the candidate table (100,000-row samples of each side for the drift).

     | Year created | In | Projects | Successful, test | Successful, train side | Train share | Median PSI | Largest PSI |
     |---|---|---|---|---|---|---|---|
     | 2025 | A, B, C | 20,825 | 69.8% | 61.7% | 88.9% | 0.66 | 0.69 (`prelaunch_activated`) |
     | 2024 | A, C | 21,400 | 68.3% | 60.8% | 77.4% | 0.52 | 0.87 (`prelaunch_activated`) |
     | 2023 | A, B, C | 13,056 | 65.5% | 60.2% | 70.5% | 0.26 | 0.87 (`prelaunch_activated`) |
     | 2022 | C | 11,170 | 65.4% | 59.7% | 64.5% | 0.17 | 0.97 (`prelaunch_activated`) |
     | 2021 | B, C | 9,581 | 67.5% | 59.2% | 59.4% | 0.18 | 1.13 (`prelaunch_activated`) |
     | 2020 | C | 9,639 | 63.7% | 58.7% | 54.2% | 0.20 | 1.43 (`prelaunch_activated`) |

   * **Effect on the task:** A ranks models on 2023 to 2025 only (55,281 test projects), the years with the most
     pre-launch pages. C adds 2020 to 2022, with the pandemic year and the years
     in which pre-launch pages spread, and tests 85,671 projects; B spreads three windows over the six years but tests
     the fewest projects (43,462).
   * **Consistency:** numerai_v5_2_1m tests three one-year windows, but with over six million rows a random split of
     it gets three folds, and it keeps its newest years for a reason kickstarter lacks (features built on the older
     eras). No CC in the record decides the windows; they come from the BeyondArena notebook.
   * **Sources:** the definition `datasets/_dev/tabarena-v0pt2/kickstarter/dataset.py` (`splits_comment`, `temporal`);
     the record `curation/records/kickstarter.md`; the candidate table `.venv/bin/python -m
     data_foundry.curation.cli dataset windows kickstarter --root datasets/_dev/tabarena-v0pt2` (6 years); the
     counts per month, the creation-to-deadline times and the cut at the scrape counted on the definition's frame.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Newest three years (implemented) | tests 2025, 2024 and 2023 | the years closest to deployment; the most training data (oldest 70.5%) | walks back from the newest; three of six eligible years; fewer windows than the table's size calls for |
     | B | Every other year | tests 2025, 2023 and 2021 | spread over the six years | three windows only; the fewest test projects (43,462) |
     | C | All six years | tests every year from 2025 back to 2020 | every eligible year, the closest to the nine splits of a random split this size; the pandemic year and the spread of pre-launch pages | six fits instead of three; the oldest trains on 54.2% |

   * **Recommendation:** C: with only six years above the floor and a table that gets nine splits when split at
     random, taking every eligible year is the default the rule asks for, and it covers the most different years.
     **Decision:** A, B or C?

   **Notes for the AI:** on C, `temporal = Temporal(on="created_at", splits=TemporalSplits(window=1, unit="years",
   cutoffs=(2025, 2024, 2023, 2022, 2021, 2020)))`: test 20,825, 21,400, 13,056, 11,170, 9,581 and 9,639 projects,
   train 166,292, 144,892, 131,836, 120,666, 111,085 and 101,446 (88.9%, 77.4%, 70.5%, 64.5%, 59.4%, 54.2%). On B,
   `cutoffs=(2025, 2023, 2021)`: test 20,825, 13,056 and 9,581, train 166,292, 131,836 and 111,085 (88.9%, 70.5%,
   59.4%). Then rewrite `task_summary.split`, `splits_comment` (drop the "not enough data per month" reason; the
   windows, the reasons and the numbers above), add a CC line to the record and a dated CHANGELOG entry, and run
   `dataset check` (SPLIT-15). The dating by launch from the Horizon block is a separate change, made only on the
   curator's word: `on="launched_at"` and the launches from 2025-11-13 11:00 on dropped in `_clean` (1,673 rows);
   then the windows by launch year train on 85.9%, 75.6%, 69.2%, 63.5%, 58.3% and 53.2% with a 60-day gap, and the
   statistics are to be recomputed with `dataset windows`.

   [^ks-split15]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): "The newest window is always a test window ... Prefer windows in other years, then other seasons, then
     other months, weeks or days, over the windows just before the newest ... as many windows as an IID or grouped task
     of that size would get folds, then check that they are still meaningful (SPLIT-16 to SPLIT-18)."
   [^ks-split14]: **SPLIT-14** (Must): at least 3 windows, and no window's train side holds less than 50% of the data.

   **Lennart (2026-11-11, change):** Option C: All six years.

   **Consistency check (AI, 2026-11-11):** Does "all six years" mean 2020 to 2025, or every year the amended floor opens,
   2017 to 2025?

   * **Problem:**
     - Option C was every eligible year, which meant six when every train side had to keep half, chosen to come closest to
       the nine splits a table of this size gets[^ks1-15].
     - Under today's amended floor, with issue 2's launch dates and 60-day gap, 2019, 2018 and 2017 train on 47.0%, 40.2%
       and 32.4%, so they can join as three windows under half beside six above it[^ks1-14].
     - anes_voting_2026 and mercedes_benz_greener_manufacturing keep nine windows this round, four and three under half.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Six years, 2020 to 2025 | C as written: 9,432 to 23,096 projects a window, train sides 53.2% to 85.9% | every train side keeps half | six windows where the count is nine |
     | b | Nine years, 2017 to 2025 | adds 2019, 2018 and 2017 (11,187, 12,312 and 14,286 projects) | the count this size gets; every year now open, as C meant | three train sides under half, named in the splits comment |

   * **Recommendation:** b: C asked for every eligible year to approach nine windows, and the amended floor makes it
     exactly nine. **Decision:** a or b?

   [^ks1-15]: **SPLIT-15** (Should for the other windows): "as many windows as an IID or grouped task of that size would
     get folds" (185,444 rows: 3 x 3).
   [^ks1-14]: **SPLIT-14** (Must; amended 2026-11-11, Lennart): the two tiers, 50% and 30%.

   **Lennart (2026-11-11, change):** Reply (b): Nine years, 2017 to 2025

   **Resolved (2026-11-11, Lennart):** C with reply b: the test windows are the nine launch years 2025 back to 2017
   (`cutoffs=(2025, 2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017)`, dated by launch with issue 2's 60-day gap). On
   the definition's frame of 185,444 projects they test 23,096 (1 January to 13 November 2025), 20,466, 12,096,
   10,790, 9,523, 9,432, 11,187, 12,312 and 14,286 projects and train on 159,342 down to 60,168 (85.9%, 75.6%, 69.2%,
   63.5%, 58.3%, 53.2%, 47.0%, 40.2% and 32.4%), as the consistency check gave. The three under half, 2019 (47.0%),
   2018 (40.2%) and 2017 (32.4%), are signed off with this mark: the record's CC line names them and the definition
   accepts `splits_train_under_half` with them. `task_summary.split` and `splits_comment` name the nine years, the
   counts, the three under half with their shares, and why nine (every year the floor admits, the count a random
   split of this size gets). `dataset check`: 0 errors, 0 warnings.

2. **Date the projects by launch and leave out the launches of the scrape's last 60 days?**

   * **Problem:**
     - The windows are dated by creation, but the use case predicts at launch, and a project is created a median of 52
       days before its deadline (154 days at the 90th percentile), so 1.9% to 3.2% of each train side was still running
       when its window starts.
     - The scrape of 12 January 2026 holds only projects that had ended, so the newest year misses the projects still
       running then: 2025 Q4 holds 2,727 projects against 5,198 in 2024 Q4.
     - The missing projects succeed more often, so the newest window's success rate is biased down, by about 1.4 points
       when 2024 is cut the same way.
   * **Background:**
     - A label cut by the download date in the newest periods is cut where follow-up is complete[^ks2-leak24]; for a
       campaign of at most 60 days (Kickstarter's rule; 3,586 projects in the data run longer, up to 121 days), that is
       60 days before the scrape.
     - Dated by launch, the prediction point[^ks2-use3], only 0.5% to 0.9% of a train side (634 to 1,389 projects)
       would still run past the window's start, and a 60-day gap leaves none whose outcome a refit could not know.
     - Dropping the launches from 13 November 2025 11:00 on removes 1,673 projects (74.2% successful), all from the
       newest window.
   * **Statistics:** one-year windows by launch year with a 60-day gap train on 85.9%, 75.6%, 69.2%, 63.5%, 58.3% and
     53.2% of the projects (2025 to 2020); by creation year without a gap on 88.9%, 77.4%, 70.5%, 64.5%, 59.4% and
     54.2%.
   * **Effect on the task:** A scores the newest year on a sample tilted toward projects that ended early, which fail
     more often, and trains on outcomes a refit at the window's start would not know; B scores each year on whole
     campaigns known when the window starts.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Creation date, every project (implemented) | windows by `created_at`; the newest year as scraped | no change | the newest year misses a fifth of its projects, biased down; train sides hold outcomes not yet known |
     | B | Launch date, cut at 60 days before the scrape | `on="launched_at"`, a 60-day gap, the 1,673 launches from 13 November 2025 dropped | the prediction point; every outcome known when used; the newest year complete | 1,673 projects fewer; the windows of issue 1 shift slightly (53.2% for 2020) |

   * **Recommendation:** B: it dates each project at the moment the use case predicts and cuts the newest year where
     its outcomes are complete. **Decision:** A or B?

   **Notes for the AI:** on B, `temporal = Temporal(on="launched_at", splits=TemporalSplits(window=1, unit="years",
   cutoffs=(...), gap=60, gap_unit="days"))` with the cutoffs of issue 1's choice, and in `_clean` drop the rows with
   `launched_at >= 2025-11-13 11:00` (1,673), with a curation note on the scrape's cut; recompute the statistics with
   `dataset windows kickstarter` and check the counts of issue 1's chosen option; then `task_summary.split`,
   `splits_comment`, a CC line in the record, a dated CHANGELOG entry and `dataset check`.

   [^ks2-leak24]: **LEAK-24** (Must): "A target right-censored in the newest periods (a duration or a final status cut
     by the download date) is cut where follow-up is complete, or re-sourced from an archive with settled labels".
   [^ks2-use3]: **USE-3** (Must): "Name the prediction point: when the model is used and what is known then."

   **Lennart (2026-11-11, change):** Option B: Launch date, cut at 60 days before the scrape.

   **Resolved (2026-11-11, Lennart):** B: `temporal` dates the windows by `launched_at` with a 60-day gap
   (`gap=60, gap_unit="days"`), and `_clean` drops the projects launched from 2025-11-13 11:00 on, 60 days before the
   scrape's newest deadline (12 January 2026 11:00): 1,673 projects, 74.2% successful, all from the newest window.
   185,444 projects remain, 62.50% successful. With the gap at most one training project per window (3 over the nine
   train sides, campaigns longer than 60 days) had not ended when its window starts, against 1.9% to 3.2% of each
   train side dated by creation. The curation notes give the scrape's cut, `task_summary` (row, predicted, split,
   changes, fit reason) and `splits_comment` the dating by launch and the gap; the record has the CC line.
   `dataset windows kickstarter` recomputed: success in the test years 55.0% (2017) to 71.1% (2025), on the train
   sides 58.3% to 61.3%. `dataset check`: 0 errors, 0 warnings.

## Reference

Webrobots Website
