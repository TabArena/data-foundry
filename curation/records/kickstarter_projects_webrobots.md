---
unique_name: kickstarter_projects_webrobots
name: Kickstarter Projects (Web Robots scrape, February 2019)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
collections:
- STRABLE
source_links:
- https://webrobots.io/kickstarter-datasets/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/kickstarter-projects
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-01):** `No` (`Duplicate`, PROV-4, PROV-6): STRABLE's "Kickstarter Projects" is the file `Kickstarter_projects_Feb19.csv` of Kaggle yashkantharia/kickstarter-campaigns, Web Robots' Kickstarter scrapes up to February 2019 combined and pre-processed. That Kaggle page is the first source link of `kickstarter` (`Yes`, BeyondArena), which was rebuilt from Web Robots' own scrape of 2026-01-12, so this record is an older, processed version of a dataset that ships, with the same target, and adds no task.
- Source: Web Robots, Kickstarter datasets (https://webrobots.io/kickstarter-datasets/): "We have a scraper robot which crawls all Kickstarter projects and collects data in CSV and JSON formats"; "From March 2016 we run this data crawl once a month"; releases from 2014-04-22 to 2026-10-12, 2019-02-14 among them. Kaggle yashkantharia/kickstarter-campaigns (one file, `Kickstarter_projects_Feb19.csv`, 2019): "Kickstarter's web scarping data from webrobots.io (https://webrobots.io/kickstarter-datasets/) was combined, pre-processed and created into a simple and easy to understand dataset ... Data set includes projects from 2014 to February 2019." STRABLE's config: target `status`, source "webrobots.io"; its parquet (previewed): 75,000 rows x 19 columns (id, name, currency, main and sub category, launched_at, deadline, duration, goal_usd, city, state, country, blurb_length, name_length, status, start and end month and quarter), launched 2009-04-28 to 2019-02-07, 42,349 successful and 32,651 failed. STRABLE's paper names kemical/kickstarter-projects instead (App. C, row 67), but the file and the config are Web Robots'.
- Use case and regime: as `kickstarter` (Kickstarter or a creator at launch; temporal by creation date).
- Siblings and duplicates: `kickstarter` (`Yes`, `DF: Yes`, BeyondArena; its links are this Kaggle page and https://webrobots.io/kickstarter-datasets/, its older note "Scraped Kickstarter results, 2014–Feb 2019" describes this file, and its definition pins Web Robots' 2026-01-12 scrape, 187,117 projects created 2009-2025; collections TexTabBench, TabSTAR, AutoML_MM). `kick_starter_funding` (MulTaBench, HackerEarth's 2017 release, another crawl; proposed `No` on its label). External collections: STRABLE ("Kickstarter Projects"); TexTabBench (the same file, per the run's note).
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Metric: none (Web Robots publishes scrapes; `kickstarter` uses the fallback `roc_auc`).
- Reject check (AI, 2026-11-01): stands. Measured 2026-11-01: STRABLE's parquet (https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/kickstarter-projects; 75,000 rows, 74,594 unique ids) is a subsample of Kickstarter_projects_Feb19.csv from Kaggle yashkantharia/kickstarter-campaigns, with usd_pledged dropped: all 74,594 ids are in that file and status agrees in 100%. The Kaggle page (Kaggle API, v1 of 2019-03-03) says: "Kickstarter's web scarping data from webrobots.io (https://webrobots.io/kickstarter-datasets/) was combined, pre-processed ... Data set includes projects from 2014 to February 2019." 39,373 of the ids are in Web Robots' 2026-01-12 scrape that kickstarter pins, and Kickstarter's state equals status in all 39,373 (89,068 of the full file's 168,467, also 100%). So it is an older snapshot of kickstarter's own source with the same target and units: a version (PROV-6), with the shared source confirmed (PROV-4, PROV-5). It is a duplicate, not a separate source (selection.md, 'Small or dated'), and the curator has already picked the version: kickstarter links this Kaggle page, and its download_description says "There exists data from Kaggle ... We use data from the original source ... and downloaded the newest version". Precedents point the same way: airlines (an older cut of the BTS table, `Duplicate` of aeolus, CC 2026-10-26 Lennart), loan_data and melbourne_housing_snapshot. numerai28_6 was kept only because its target, features and rows differed, and none of that holds here. For kickstarter, not this record: 79,399 projects of the Feb19 file are missing from the pinned 2026 scrape, so merging older Web Robots scrapes could add them.

**Assessment (AI, 2026-11-01):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292) as "Kickstarter Projects"; split out on 2026-11-01 from the note on `kickstarter`, which holds a different snapshot.
- as published: 75,000 rows x 19 columns incl. target (STRABLE parquet); capped at 75,000 by STRABLE; target: status.
- Why: Predict whether a Kickstarter campaign succeeds
- Notes: Raw file Kickstarter_projects_Feb19.csv from TextTabBench (webrobots.io scrape); the paper links the kemical Kaggle set instead. Subsampled by STRABLE to 75,000 rows.
