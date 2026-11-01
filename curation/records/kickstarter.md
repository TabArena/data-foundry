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

## Reference

Webrobots Website
