---
unique_name: which_justin_instagram
name: Justin Instagram
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
- Image
tags:
- AI-Filled (Verify)
collections:
- MulTaBench
source_links:
- https://www.kaggle.com/datasets/aldiandyainf/which-justin-posted-that
- https://arxiv.org/abs/2605.10616
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`No Good Target / Scientific Discovery`, `Image`; USE-2, SEL-3, SEL-12): a practice dataset whose target is which of five celebrities named Justin posted an Instagram image; no decision rests on it, the identity sits in the image, and the six structured columns are counts taken from the caption.
- Source: Kaggle "Which Justin posted that?" by `aldiandyainf` (dataset.csv, 2022-03-23, CC0), subtitle "Practice using tabular, text or image to predict which Justin posted that": "The data was gathered using Python by the Instagram GraphQL API (non-documented). All of the images are publicly available. The reason for this project was to create a fun project where you can practice Computer Vision, Natural Language Processing, and normal tabular machine learning and perhaps combine those models together." About ten thousand posts, with a thumbnail for photo, video and carousel posts. MulTaBench core (Table 3; App. F.1): 10,319 rows; n_hashtags, n_characters, n_words, n_emojis, n_mentions, is_video and the thumbnail; target the username (Bieber, Trudeau, Timberlake, Long, Hartley).
- Use case: none. The poster of every post is known to Instagram and to its readers, and the source states a practice purpose (USE-2; SEL-3 asks for a task "simulating a decision someone makes with the prediction"). Fit none (USE-8).
- Modality: the five accounts differ by who and what is in the picture; the structured columns are counts computed from the caption text plus a video flag, so without the image and the caption little task remains, and with them it is face and scene recognition (SEL-12).
- Siblings and duplicates: no other Instagram record. External collections: MulTaBench core (one of its 20 image-tabular datasets).
- Better data: a candidate of the benchmark MulTaBench (the run searched no further).
- Papers and pages: the Kaggle page; MulTaBench (Arazi et al. 2026, arXiv 2605.10616, App. F.1).
- Metric: none found (the Kaggle page names none; MulTaBench reports AUC as a benchmark convention).
- Not the reason: the scrape of public posts through an undocumented API; no objection by the subjects was found (SEL-1 not triggered).
- Reject check (AI, 2026-10-31): stands. The uploader: 'The reason for this project was to create a fun project where you can practice Computer Vision, Natural Language Processing, and normal tabular machine learning' (https://www.kaggle.com/datasets/aldiandyainf/which-justin-posted-that): a practice target no one decides on (the poster is known to Instagram and the reader), and the structured part is six caption counts and a video flag (MulTaBench App. F.1).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 10,319 rows; 6 structured, 0 text, 1 image features (MulTaBench Table 3); target: Poster identity (5 classes).
- Why: Identify which of five celebrities named Justin posted an Instagram image
- Notes: Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. Kaggle 2022, gathered via the undocumented Instagram GraphQL API as a 'fun project'; no use case stated.
