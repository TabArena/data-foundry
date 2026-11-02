---
unique_name: yambda_track_like_rate
name: 'Yambda-5B: A Large-Scale Multi-modal Dataset for Ranking And Retrieval (Yandex Music)'
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Out-of-scope Task (CTR/RecSys/Ranking)
tags:
- AI-Filled (Verify)
source_links:
- https://huggingface.co/datasets/yandex/yambda
- https://arxiv.org/abs/2505.22238
- https://yandex.com/company/news/28-05-2025
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Out-of-scope Task (CTR/RecSys/Ranking)`, SEL-9; SEL-8): Yandex's Yambda-5B is a recommender-system release ("A Large-Scale Multi-modal Dataset for Ranking And Retrieval", title; "Industrial-scale music recommendation dataset with organic/recommendation interactions and audio embeddings", Hugging Face card), 4.79 billion user-item events benchmarked with recommenders under a global temporal split; it defines no per-track target, and the like rate the run proposes is our aggregate of the same user-item like and listen events.
- Source: Ploshkin, Tytskiy, Pismenny, Baikalov, Taychinov, Permiakov, Burlakov, Krofto and Savushkin (Yandex), "Yambda-5B: A Large-Scale Multi-modal Dataset for Ranking And Retrieval", arXiv 2505.22238 (2025-05-28); data on Hugging Face (yandex/yambda, Apache 2.0, "published exclusively for scientific and research purposes"). As published: "4.79 billion user-item interactions from 1 million users across 9.39 million tracks" (abstract): 4,649,567,411 listens, 89,334,605 likes, 11,579,143 dislikes, plus unlikes and undislikes; 500M and 50M subsets; an organic-or-recommended flag per listen; audio embeddings; baselines ItemKNN, iALS, SANSA and SASRec under "an evaluation protocol based on a Global Temporal Split" (abstract).
- Why SEL-9 and SEL-8: the original task is recommending, ranking and retrieving tracks for users, in the source's own title and card; a track's likes per listen is a like-through rate over recommendation logs, the click-through kind of target SEL-9 names, and building it ourselves does not change the original task (SEL-8).
- What sets it apart from `hulkshare_recommendation_algorithm_challenge` (its proposed SEL-9 reject was refuted on 2026-10-22): there the source (Zindi) published one row per song with a likes-to-views target scored by RMSE; here the source publishes only user-item events and recommendation benchmarks.
- Siblings and duplicates: none (grep yambda; the other Yandex records, such as `shifts_weather_temperature` and `delivery_eta`, are other releases). External collections: none found.
- Better data: found as better data for `hulkshare_recommendation_algorithm_challenge`.
- Papers and pages: the arXiv paper (abstract read), the Hugging Face card, Yandex's announcement of 2025-05-28.
- Metric: the source scores recommendation rankings (metrics not named in the abstract); none for a per-track target.
- Reject check (AI, 2026-10-31): stands. The source's own words fix a recommender task: the title 'Yambda-5B -- A Large-Scale Multi-modal Dataset for Ranking And Retrieval', 'an evaluation protocol based on a Global Temporal Split, allowing recommendation algorithms to be assessed', and the aim to 'promote reproducible results in recommender systems' (abstract, https://arxiv.org/abs/2505.22238). No per-track target is published. Likes per listen would be our own aggregate of user-item events, a click-through kind of rate, and the listens are partly driven by the recommender (is_organic). That is the same set of facts as hm_article_buyer_age (stood). hulkshare's refutation rested on Zindi publishing a per-song target scored by RMSE, which this source does not. SEL-2: in practice a like probability is predicted per user-track pair inside the ranking system.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `hulkshare_recommendation_algorithm_challenge`.
- as published: event log over about ten months: 4.79 billion interactions of 1,000,000 users on 9,390,623 tracks (4,649,567,411 listens, 89,334,605 likes, 11,579,143 dislikes, plus unlikes and undislikes); subsets ...; target: not published as a column: a track's likes per listens (the same quantity as Hulkshare's likes-to-views ratio), to be aggregated per track from the like and ...; access: open (Hugging Face, Apache 2.0; 'published exclusively for scientific and research purposes').
- Why: same task as hulkshare_recommendation_algorithm_challenge: one row per song, target its like-to-listen ratio, inputs aggregated listening behaviour (Hulkshare: per-session play, pause, skip, rewind frames; Yambda: per-listen played ratio, organic flag, track length) known before the likes
- Adds: millions of tracks against Hulkshare's song set, a documented release with a paper, timestamps for a features-before-target window (features from a track's first weeks, like rate later) that removes the record's same-window leak doubt, audio embeddings, Apache 2.0 instead of Zindi's no-redistribution rules. Caveats: ...
