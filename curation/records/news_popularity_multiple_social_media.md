---
unique_name: news_popularity_multiple_social_media
name: News Popularity in Multiple Social Media Platforms (UCI 432)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: UCI
year: '2018'
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.24432/C5H029
- https://archive.ics.uci.edu/dataset/432/news+popularity+in+multiple+social+media+platforms
- https://arxiv.org/abs/1801.07055
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: 93,239 news items from Google News and Yahoo! News (November 2015 to July 2016) with outlet, topic, time, title and headline text, and their Facebook shares, Google+ +1s and LinkedIn shares two days later; a documented, larger and newer source for news popularity, with the raw text `onlinenewspopularity` lacks, but besides the text the features at publication are thin.
- Source: Moniz and Torgo, "Multi-Source Social Feedback of Online News Feeds", arXiv:1801.07055 (January 2018); UCI 432, "News Popularity in Multiple Social Media Platforms" (doi 10.24432/C5H029, donated 2018-02-19, CC BY 4.0). As published: News_Final.csv (IDLink, Title, Headline, Source, Topic, PublishDate, SentimentTitle, SentimentHeadline, Facebook, GooglePlus, LinkedIn) and one file per platform and topic with TS1-TS144, the popularity in 20-minute slices up to two days. Section 4: Facebook is "the number of shares concerning each unique URL", Google+ the +1s; -1 marks a value that could not be obtained (mostly items picked up after their two days). Section 3.1: "The total amount of news retrieved in both official media sources is 93,239", from queries every 20 minutes for the top 100 news of four topics (economy, microsoft, obama, palestine), 10 November 2015 to 7 July 2016.
- Use case: a news aggregator or an outlet decides at publication which items to promote; the source names none (Section 2: "evaluative comparisons in predictive analytics tasks", also "recommendation and/or learning to rank"), so the fit is approximate; regime temporal by publication time.
- Siblings and duplicates: `news_popularity_multiple_social_platforms` is the same UCI record, created twice in this run (proposed `No`, `Duplicate`, PROV-4, in favour of this record); `onlinenewspopularity` (`Yes`, DF: Yes; Mashable 2013-2014 shares, no raw text, whose comments wish for the text) and `facebook_comment_volume` (`TBD -> Yes`, comments on Facebook page posts): other sources, related tasks. External collections: none found.
- Better data: found as better data for `onlinenewspopularity`, and (as `news_popularity_multiple_social_platforms`) for `facebook_comment_volume`; no further search this round.
- Papers and pages: the arXiv paper (read through ar5iv, Sections 2 to 4); the UCI page.
- Metric: none found (the paper reports no models and no metric; UCI lists "Regression"), so the fallback, `rmse` on log1p of the count as on `onlinenewspopularity` (MET-1, MET-8); inputs none.
- Risks for /add-dataset: the slices TS1-TS144 are the target's own series, so early slices as features make it a forecast of the series (SEL-10) and close to the target: the in-scope task is at publication; drop the -1 rows per platform rather than impute them (USE-7); at publication the title and headline carry most of the signal (`NLP (Text)` as on `onlinenewspopularity`, SEL-12 judged on the data); only four query topics; heavy-tailed counts with many zeros; one platform as the target (Facebook) and the others dropped as framings of one signal (CLEAN-18); the authors removed repeats by title, headline and outlet (Section 4), check the rest.
- Priority: gap 0 (technology & internet holds 4, regression and temporal are not thin), use case 0, source + (a paper and UCI), shape + (93,239 items; text, categorical and time columns), risk - (text-driven, the target's series in the files).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `onlinenewspopularity`.
- as published: 93,239 news items (UCI page), November 2015 to July 2016, four query topics (economy, microsoft, obama, palestine), many outlets; news table: IDLink, Title, Headline, Source, Topic, PublishDate, ...; target: Final popularity of a news item on Facebook (also Google+ and LinkedIn), the count after two days; -1 marks items not tracked on a platform; access: open.
- Why: The same task as onlinenewspopularity: social share count of a news item predicted at publication from what is known about the item then; the record's comments regret that the Mashable release has no raw text, and this one ships the title and headline text next to the sentiment scores
- Adds: 2.4x the items (93,239 against 39,644), newer (2015-2016 against 2013-2014), many outlets instead of one site, three platforms, raw title and headline text, and early-popularity slices for an early-prediction variant. Risks: only four query topics; the -1 rows; text-heavy features (the record's NLP marker would apply ...
