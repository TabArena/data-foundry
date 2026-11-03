---
unique_name: twitter_bots_accounts
name: Twitter Bots Accounts (FDB twitterbot)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- AI-Filled (Verify)
original_source: Kaggle
year: '2020'
domain: technology & internet
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/davidmartngutirrez/twitter-bots-accounts
- https://arxiv.org/abs/2208.14417
- https://doi.org/10.1109/ACCESS.2021.3068659
- https://botometer.iuni.iu.edu/bot-repository/datasets.html
- https://github.com/amazon-science/fraud-dataset-benchmark
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: 37,438 Twitter accounts labelled bot or human from collections of the Bot Repository, with profile metadata fetched in 2020; a real platform-abuse task, but the labels follow separately collected bot and human sets, the features were fetched years after the labelling, and the current Kaggle version holds only ids and labels.
- Source: David Martín-Gutiérrez, Kaggle "Twitter Bots Accounts" (https://www.kaggle.com/datasets/davidmartngutirrez/twitter-bots-accounts, CC0). Kaggle API on 2026-10-31: one file, twitter_human_bots_dataset.csv, 658,688 bytes, dated 2020-11-06, holding only id and account_type for 37,438 accounts (25,013 human, 12,425 bot); version 2 (file dated 2020-08-19, the version the Fraud Dataset Benchmark loads) holds 19 columns: created_at, default_profile, default_profile_image, description, favourites_count, followers_count, friends_count, geo_enabled, id, lang, location, profile_background_image_url, profile_image_url, screen_name, statuses_count, verified, average_tweets_per_day, account_age_days, account_type (preview of the header and label counts; the local copy was deleted after the look, as it holds personal data). The card says the accounts come from the Bot Repository (https://botometer.iuni.iu.edu/bot-repository/datasets.html, which did not resolve on 2026-10-31). The author's paper: Martín-Gutiérrez, Hernández-Peñaloza, Belmonte Hernández, Lozano-Diez, Álvarez, "A Deep Learning Approach for Robust Detection of Bots in Twitter Using Transformers", IEEE Access 9:54591-54601 (2021, https://doi.org/10.1109/ACCESS.2021.3068659; not read: the pages answered 403 or empty).
- Use case: a platform's trust-and-safety team flags or restricts suspicious accounts (the card: "automatically notify or restrict the access to those accounts that look suspicious"); fit approximate: the accounts were pooled from separately labelled collections and their profiles fetched later (account_age_days runs to 2020, created_at 2006-2019); regime IID (one snapshot), with the source collection as a grouping that the file does not carry.
- Siblings and duplicates: no record holds the Bot Repository or this upload (grep by twitter, bot, botometer, cresci, fraud-dataset-benchmark); `mkphoto2023_bots` (`No`, `Image`, MulTaBench) and `facebook_recruiting_human_or_robot` (auction bidders) are other bot tasks. External collections: the Fraud Dataset Benchmark (Grover et al. 2022, https://arxiv.org/abs/2208.14417; key `twitterbot`, 29,950 train and 7,488 test, 16 features: 6 categorical, 6 numeric, 4 text).
- Better data: from the curator's Zotero collection (item 111, the FDB paper); no further search this round.
- Papers and pages: the FDB README and loader (https://github.com/amazon-science/fraud-dataset-benchmark: Kaggle version 2, an 80% random split, AUC-ROC 0.934 to 0.943 for its AutoML baselines, also recall at 1% FPR); the IEEE Access paper (not read).
- Metric: FDB reports AUC-ROC as a benchmark, not the data's source; the data's paper was not read; fallback `roc_auc` (MET-1, MET-8); inputs none.
- Risks for /add-dataset: the labels follow the source collections (verified accounts: 7,235 human, 316 bot), so the features may tell the collection rather than the behaviour (`Selection Bias` to weigh; LEAK-13 probe); counts and account_age_days were measured when the profiles were fetched in 2020, not when the accounts were labelled (USE-3); id, screen_name and the image URLs are identifiers and go, description and location are free text of real people (SEL-12, personal data: keep it local); only version 2 holds the features, and its uploader replaced it with ids only (ask why, and whether the platform's terms let the profiles ship, EV-4).
- Priority: gap 0 (technology & internet has 4), use case 0 (approximate fit), source 0 (the card documents two columns, the paper not read), shape + (37,438 accounts, numeric, boolean and text columns), risk - (collection-confounded labels, features fetched after the labelling).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 111: "Fraud Dataset Benchmark and Applications".
- as published: Twitter user accounts, 37,438 rows; FDB lists 16 features (6 categorical, 6 numeric, 4 text: creation date, follower/friend/status counts, description, profile-image flags, verified, location, ...; target: account_type: bot vs human; access: open.
- Why: Real labelled accounts with tabular profile metadata; a bot-attack task FDB groups with fraud. No record covers social-bot detection.
- Adds: An abuse and bot detection task with mixed feature types. Risks: labels pooled from several Bot Repository collections, so bots and humans were collected apart (selection bias). The Kaggle card still describes only id and label, so check that version 2 holds the features. Text columns.
