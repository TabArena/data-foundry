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

CC (2026-11-11, Lennart): REVIEW.md issue 2, B ("Option B: Launch date, cut at 60 days before the scrape."): the windows are dated by launch (`launched_at`) with a 60-day gap, the longest campaign, and the 1,673 projects launched from 13 November 2025 11:00 on, 60 days before the scrape's newest deadline, are dropped, so the newest year is cut where its outcomes are complete.

CC (2026-11-11, Lennart): REVIEW.md issue 1, C ("Option C: All six years.") with reply (b) to the consistency check ("Reply (b): Nine years, 2017 to 2025"): the test windows are the nine launch years 2025 back to 2017, in place of the three newest years by creation; SPLIT-14 as amended on 2026-11-11 admits the three oldest, signed off here: 2019, 2018 and 2017 train on 47.0%, 40.2% and 32.4% of the projects (three windows under half, six at or above it).

CC (2026-11-11, Lennart): the declared horizon (one calendar year of launches, a 60-day gap, windows starting 2025, 2024, 2023, 2022, 2021, 2020, 2019, 2018 and 2017) is checked, as no source gives a horizon or a refit cadence, and a year holds every season and loses the least of its newest window to the scrape (REVIEW.md horizon, ok).

**Assessment (AI, 2026-11-11):** applied issue 2 (B) and issue 1 (C, reply b): `_clean` drops the 1,673 projects launched from 2025-11-13 11:00 on (74.2% successful; 60 days before the scrape's newest deadline, 2026-01-12 11:00), leaving 185,444 projects (62.50% successful); `temporal` declares one-year windows by `launched_at` from 2025 back to 2017 with a 60-day gap. Test 23,096 (1 January to 13 November 2025), 20,466, 12,096, 10,790, 9,523, 9,432, 11,187, 12,312 and 14,286 projects; train 159,342, 140,261, 128,277, 117,767, 108,032, 98,615, 87,250, 74,581 and 60,168 (85.9%, 75.6%, 69.2%, 63.5%, 58.3%, 53.2%, 47.0%, 40.2% and 32.4% of the projects). Success in the test years runs from 55.0% (2017) to 71.1% (2025), on the train sides from 58.3% to 61.3% (`dataset windows`); at most one training project per window (3 over the nine train sides, campaigns longer than 60 days) had not ended when its window starts. `task_summary`, the notes and `splits_comment` give the windows, the gap and the dating by launch, and drop the reason "not enough data per month" (1,500 to 2,200 projects a month). `dataset check`: 0 errors, 0 warnings, with `splits_train_under_half` accepted on the CC line above.

## Reference

Webrobots Website
