---
unique_name: kick_starter_funding
name: Kickstarter funding (AutoML Multimodal kick_starter_funding, OpenML 46668)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Data Quality Issue
tags:
- AI-Filled (Verify)
collections:
- MulTaBench
source_links:
- https://www.openml.org/search?type=data&id=46668
- https://huggingface.co/datasets/multabench/core-text-cls-kickstarter-funding
- https://arxiv.org/abs/2605.10616
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-01):** `No` (`Data Quality Issue`, PROV-3): HackerEarth's 2017 Kickstarter challenge data, as the AutoML multimodal benchmark, OpenML 46668 and MulTaBench serve it, carries a label that is not the outcome its source defines. Of the 24,293 projects also in Web Robots' scrape of 2026-01-12 (the data of `kickstarter`), all 4,518 that Kickstarter records as successful with 100% to 105% of the goal pledged are labelled not funded, and all 10,004 with 105% or more are labelled funded, while the source says a project succeeds when it meets its goal. The same task ships as `kickstarter`, with Kickstarter's own state for 2009-2025.
- Source: HackerEarth machine learning challenge "Funding Successful Projects" (2017), copied to Kaggle codename007/funding-successful-projects: "Recently, Kickstarter released its public data repository ... In this challenge, you have to predict if a project will get successfully funded or not"; "if a projects's goal is $500. Even if it gets funded till $499, the project won't be a success"; "The train data consists of sample projects from the May 2009 to May 2015. The test data consists of projects from June 2015 to March 2017." Shi, Mueller, Erickson, Li and Smola, "Benchmarking Multimodal AutoML for Tabular Data with Text Fields" (NeurIPS 2021 Datasets and Benchmarks, arXiv 2111.02705), Table 2: "kick 86,502 21,626 ... binary roc-auc whether proposed Kickstarter project will achieve funding goal", from the codename007 copy; OpenML 46668 (2025) and MulTaBench (86,502 rows) copy its training part: name, desc, keywords (the URL slug), goal, disable_communication, country, currency, deadline, created_at; target final_status, 27,649 funded of 86,502.
- Measured (2026-11-01; OpenML 46668 parquet against the 84 CSV files of Web Robots' 2026-01-12 scrape in the local warehouse, matched on name and deadline, goal equal in every match): 24,293 of 86,502 projects match (28%); pledged over goal splits the label exactly at 1.05 (label 0 up to 1.0499, label 1 from 1.05); 1,050 cancelled projects are labelled 0; no project Kickstarter records as failed is labelled 1. The 72% that do not match cannot be relabelled from the release, which has no pledged amount.
- Use case: as `kickstarter` (Kickstarter or a creator at launch estimating whether a campaign reaches its goal); the released label is a 105% threshold no source names. Regime temporal (the challenge split by date).
- Siblings and duplicates: `kickstarter` (`Yes`, BeyondArena; Web Robots' monthly scrapes, 187,117 projects created 2009-2025, target Kickstarter's state; its source links already include OpenML 46668 and the codename007 page, carried from the curation sheet with the `AutoML_MM` collection). By provenance this is another crawl (HackerEarth's, origin unstated; 28% of its projects in the pinned 2026 scrape), so it duplicates `kickstarter` by task only, a PROV-6 reading left to the curator. `kickstarter_projects_webrobots` (STRABLE, Web Robots' February 2019 file, proposed `Duplicate` of `kickstarter`). External collections: AutoML multimodal benchmark ("kick"), OpenML 46668, MulTaBench (core text-tabular, "Kickstarter").
- Better data: a candidate of the benchmark MulTaBench; no further search this round. `kickstarter` holds the same task with more and newer projects.
- Metric: the challenge's metric not found (HackerEarth's page did not come up in searches); the AutoML benchmark's roc-auc and MulTaBench's AUROC are fixed per task type (MET-5), so the fallback `roc_auc`.
- If the reject check refutes this: `TBD -> 2nd Tier`, priority 1, markers `Data Quality Issue` (the 105% label) and the note that `kickstarter` holds the task.
- Reject check (AI, 2026-11-01): stands. Reproduced 2026-11-01 (a measurement, EV-2 rank 1). Of OpenML 46668's rows, 24,129 match Web Robots' 2026-01-12 scrape on name and deadline, goal equal in all. Label 1 holds exactly when pledged/goal >= 1.05: the lowest ratio labelled 1 is 1.0500, the highest ratio of a Kickstarter-successful project labelled 0 is 1.0499, and 4,484 successful projects are labelled 0. The challenge's own train.csv (codename007, 108,129 rows) shows the same: 30,236 matches, backers_count equal in 100%, 5,604 successful projects at 100-105% of goal all labelled 0, and 12,483 at 105% or more all labelled 1. The source defines success as meeting the goal: "if a projects's goal is $500. Even if it gets funded till $499, the project won't be a success ... Will a project get fully funded?" (https://www.kaggle.com/datasets/codename007/funding-successful-projects, Kaggle API description). The 5% may be Kickstarter's fee, but no source names that rule. This cannot be fixed by a new target. OpenML 46668 ships 10 columns (https://www.openml.org/api/v1/json/data/features/46668: name, desc, goal, keywords, disable_communication, country, currency, deadline, created_at, final_status). The challenge's train.csv adds only project_id (not Kickstarter's id: 0 of the 32,239 id hits agree on name), state_changed_at, launched_at and backers_count. Neither has a pledged amount. A repair from Web Robots reaches 28% of the rows in the pinned scrape and would turn them into a cut of kickstarter's source (PROV-6). USE-5: "A label checked and found to be another quantity than the one the actor acts on still fails" (diabetes_3).

**Assessment (AI, 2026-11-01):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616) as "Kickstarter"; split out on 2026-11-01 from the note on `kickstarter`, which holds a different snapshot.
- as published: 86,502 rows; 6 structured, 3 text, 0 image features (MulTaBench Table 3); target: Goal reached (binary).
- Why: Predict whether a Kickstarter campaign reaches its funding goal
- Notes: Text-tabular; AutoML Multimodal kick_starter_funding (OpenML 46668); the record links a different Kaggle snapshot (yashkantharia).
