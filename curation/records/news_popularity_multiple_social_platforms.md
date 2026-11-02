---
unique_name: news_popularity_multiple_social_platforms
name: News Popularity in Multiple Social Media Platforms
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
source_links:
- https://arxiv.org/abs/1801.07055
- https://doi.org/10.24432/C5H029
- https://archive.ics.uci.edu/dataset/432/news+popularity+in+multiple+social+media+platforms
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Duplicate`, PROV-4): the same dataset as `news_popularity_multiple_social_media`; both records were created in this run from one UCI record (UCI 432, "News Popularity in Multiple Social Media Platforms", doi 10.24432/C5H029; Moniz and Torgo, arXiv:1801.07055), once as better data for `onlinenewspopularity` and once for `facebook_comment_volume`, and both list the same three links.
- Source: Moniz and Torgo 2018; UCI 432, 93,239 news items, donated 2018-02-19, CC BY 4.0.
- Siblings and duplicates: the canonical record is `news_popularity_multiple_social_media` (screened `TBD -> Yes`, priority 2), whose block names both records the dataset was found for.
- Better data: found as better data for `facebook_comment_volume`; carried on the canonical record.
- Reject check (AI, 2026-10-31): stands. The same UCI 432 record ('News Popularity in Multiple Social Media Platforms', 93,239 items, https://doi.org/10.24432/C5H029) with the same three links as news_popularity_multiple_social_media, created twice in this run. Its one different angle, predicting from early popularity slices (TS1-TS144) as for facebook_comment_volume, is a prediction point on the same target. The kept record already lists it under Adds and Risks.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `facebook_comment_volume`.
- as published: 93,239 news items (UCI) from Google News and Yahoo! News on four topics (economy, microsoft, obama, palestine), November 2015 to July 2016; 11 news variables (title, headline, source, topic, publish ...; target: Final popularity of the item on Facebook after 2 days (the popularity measure as defined in the paper; not checked whether shares or likes); access: open.
- Why: The same quantity as facebook_comment_volume (how much Facebook engagement an item will reach, predicted from what is known at a base time early in its life), with an explicit time axis: each feature slice is known at a chosen prediction point, so the base time and the temporal split need no reverse engineering.
- Adds: More than twice the units (93,239 against 40,949 rows), a documented feature set with dates and slices instead of anonymous columns and augmented training variants, three platforms. Differences: news items rather than Facebook page posts, and popularity counts rather than comments; free-text title and headline ...
