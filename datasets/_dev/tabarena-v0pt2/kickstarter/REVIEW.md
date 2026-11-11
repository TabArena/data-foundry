# kickstarter

**Outcome:** added. Under the rule on choosing test windows, rewritten on 2026-11-10, the AI recommends testing all
six years that keep half the projects for training (2020 to 2025) instead of the newest three, since a table of this
size gets nine train-test splits when split at random (issue 1). The one-year horizon is kept, but the Horizon block
notes that the windows are dated by creation, not by the launch the use case predicts at, and that the newest year
misses about a fifth of its projects, those still running when the data was scraped. `dataset.py` is unchanged until
you decide.

**Main points:** Test all six years from 2020 to 2025 instead of 2023 to 2025 (issue 1)? Date the projects by launch
and leave out the launches of the scrape's last 60 days, so the newest year is complete (issue 2)? Sign off the
one-year horizon.

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

