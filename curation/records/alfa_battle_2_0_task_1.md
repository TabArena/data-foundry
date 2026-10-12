---
unique_name: alfa_battle_2_0_task_1
name: Alfa Battle 2.0 ( Task 1)
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Needs extensive data wrangling
tags:
- Larger IID Data
- Non-IID (Grouped)
- Review Prio 1 (Atlas)
collections:
- New (BeyondArena)
original_source: Other
year: '2020'
domain: business & marketing
required_split:
- '?'
problem_type: TBD
original_data_state: One Table
source_links:
- https://boosters.pro/championship/alfabattle2/overview
- https://www.kaggle.com/datasets/mrmorj/alfabattle-20?select=alfabattle2_alpha_sample.csv
source_row: 661
type_adapter_id: curation-record-v1
---

## Comments

"Solve two problems predicting customer behavior in a mobile app"
"The dataset consists of user events in the mobile app (balance views, payments, transfers, chat requests, etc.) over 270 days. The output is to build a predictive model of the client's most likely action upon launching the app."
F1 score

**Assessment (AI, 2026-10-07):** The task-1 files (`alfabattle2_abattle_clickstream.zip`, `alfabattle2_abattle_train_target.csv`, `alfabattle2_prediction_session_timestamp.csv`) were only hosted on boosters.pro. The Boosters API still lists them, but every link, the sandbox copies included, redirects to a 404 page, and the Wayback Machine has no copy. The AlfaBattle 2.0 uploads on Kaggle (the record's `mrmorj/alfabattle-20` among them), Hugging Face and ODS.ai hold only the task-2 card transactions. Not added. The task predicts the action of a client's next app session (10 classes, macro F1) from earlier sessions and click events, so a tabular version would be our own featurisation of a sequence. Revisit if Alfa-Bank or a participant shares the files.

**Assessment (AI, 2026-10-07), second search:** After a long search we could not find the task-1 files anywhere, so the dataset stays not added. Revisit only if someone shares the files. What was searched:
- Boosters: its championship API (`boosters.pro/api/champ/champ?champname=alfabattle2`) still lists the four files, but the whole public file store is gone (files of other championships also redirect to 404), the sandbox copies (`alfabattle2_sand_...`) too, and neither the Wayback Machine nor Common Crawl captured any of the files.
- Alfa-Bank's own releases: ODS.ai (2022) and the Alfa-Bank ML Lab on Hugging Face (huggingface.co/mllab, `alfa_ct`, CC-BY-4.0) hold task 2 only; the lab's 2025 collection of its open competition datasets leaves the clickstream out.
- Kaggle (datasets, notebooks and competitions, several dozen search terms), Hugging Face, Zenodo, Figshare, OpenML, Mendeley Data and Google Dataset Search: task 2 or other Alfa-Bank contests only.
- GitHub and GitLab: 13 task-1 repositories with their history, branches, releases and forks. All read local files, private Kaggle datasets or the dead Boosters links. `v010ch/AlfaBattle20_task1` (branch `after_deadline`) holds submissions only (`client_pin,prediction`, 79,268 clients, no features or labels).
- Russian-language web (Habr, ODS, Telegram, theses) and papers: every paper citing AlfaBattle uses task 2. The research-use permission in Habr 551130 refers to the task-2 data.
- Licence (noted only): the championship rules (Sec. 3.10 and 5.6) forbid participants from passing on or publishing the data, which fits with no public copy existing.

Who held the files, if someone asks: the pytorch-lifestream team (Sber AI Lab; commit efb4bcc of January 2022 lists the four files on their server), the Alfa-Bank ML Lab (the organizer), and the Top-6 solution's author (github.com/Aindstorm, private Kaggle datasets `alfabattle1` and `alfabattle-1-stat`).

CC (2026-10-07, Lennart): No: the task-1 data cannot be found anywhere (see the second search above).

## Reference

Booster
