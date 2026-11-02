---
unique_name: reddit_memes_subreddit
name: Reddit Memes
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Image
- No Good Target (yet)
tags:
- AI-Filled (Verify)
collections:
- MulTaBench
original_source: Kaggle
year: '2025'
source_links:
- https://www.kaggle.com/datasets/musadiqpashak/reddit-memes-dataset
- https://arxiv.org/abs/2605.10616
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: 4,821 memes from seven meme subreddits (MulTaBench's cut of a 2025 Reddit API scrape); the subreddit target fits no decision and lives mostly in the image, but the source names a virality target that might, so this is no fast reject.
- Source: Kaggle "The Ultimate Reddit Meme Dataset" by `musadiqpashak` (data.csv and a memes/ folder, 2025-04-05, CC BY-SA 4.0): "memes scraped from seven popular meme subreddits on Reddit using the Reddit API ... meme images, metadata, and text extracted from the images using OCR ... to support tasks like meme classification, virality prediction, OCR-based analysis, and temporal meme trend studies" (r/Animemes, r/FunnyMemes, r/okbuddyretard, r/ProgrammerHumor, r/dankmemes, r/engineeringmemes, r/shitposting); columns: title, author and karma, post timestamp and time of day, upvotes, upvote ratio, comments, image file and URL, OCR text, subreddit. MulTaBench (App. F.1): 4,821 rows, target the subreddit (7 classes) from total and comment karma, cake day, upvote ratio, number of comments, time of day and the image; "the title, extracted caption, author, and upvote count are dropped".
- Use case: none for the subreddit: every post's subreddit is known once it exists, and suggesting one to a poster is a recommendation (SEL-9); a meme's community is set mainly by its content, the image and its caption (SEL-12 concern). The source's virality target (upvotes at a fixed age after posting, for a poster deciding what and when to post) could be a task if the post's age at the scrape can be rebuilt from its timestamp. Fit none for the shipped target, hence `No Good Target (yet)`; regime open (temporal for a virality target).
- Why not a fast reject: "no decision" is our reading, not the source's words, MulTaBench's Joint Signal test found that the structured columns add to the image, and the source names a second target.
- Siblings and duplicates: no other record of this data; `hateful_memes` (a MulTaBench candidate) is another dataset and task. External collections: MulTaBench, extended release (admitted on Joint Signal only), as "Reddit Memes".
- Better data: a candidate of the benchmark MulTaBench (the run searched no further).
- Papers and pages: the Kaggle page; MulTaBench (Arazi et al. 2026, arXiv 2605.10616, App. F.1).
- Metric: none found (the Kaggle page names none; MulTaBench scores AUC as a benchmark convention), so the fallback `log_loss` for the 7-class target (MET-8).
- Risks for /add-dataset: upvote ratio and comment count are measured after posting, at an unknown post age (LEAK-10); author names and karma describe individual Reddit users (drop the author); a virality target needs the post timestamp and the scrape time; the image and the OCR text carry most of the signal (SEL-12, SEL-13).
- Priority: gap + (multiclass is thin), use case 0 (none), source 0 (an individual's scrape), shape + (4,821 rows; numeric, date and categorical columns), risk - (a target no decision fits).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 4,821 rows; 6 structured, 0 text, 1 image features (MulTaBench Table 9); target: Subreddit (7 classes).
- Why: Predict the subreddit a meme was posted to from image and poster/engagement stats
- Notes: Extended release (admitted on Joint Signal only), not one of the 40 benchmark datasets. Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. Kaggle 2025 scrape via the Reddit API (CC BY-SA).
