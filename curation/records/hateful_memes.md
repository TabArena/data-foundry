---
unique_name: hateful_memes
name: Hateful Meme
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Image
- NLP (Text)
tags:
- AI-Filled (Verify)
collections:
- MulTaBench
source_links:
- https://arxiv.org/abs/2005.04790
- https://www.kaggle.com/datasets/parthplc/facebook-hateful-meme-dataset
- https://arxiv.org/abs/2605.10616
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Image`, `NLP (Text)`, SEL-12): a vision-language challenge "constructed such that unimodal models struggle and only multimodal models can succeed"; MulTaBench's 20 structured columns are embedding dimensions of the meme's caption, not tabular features.
- Source: Kiela et al., "The Hateful Memes Challenge: Detecting Hate Speech in Multimodal Memes", NeurIPS 2020 (<https://arxiv.org/abs/2005.04790>, Facebook AI), with the DrivenData challenge (2020): "This work proposes a new challenge set for multimodal classification, focusing on detecting hate speech in multimodal memes." As MulTaBench ships it (core, Table 3, from the Kaggle mirror parthplc/facebook-hateful-meme-dataset): 9,000 rows (likely the 8,500 training and 500 dev memes; not verified), `dim_e5_1` to `dim_e5_20` ("The text field is pre-embedded into continuous variables") and the image; target `label`.
- Use case: a platform's moderators flag hateful memes; the content is an image with overlaid text, and the benign confounders were added so that no single modality suffices; regime IID.
- Siblings and duplicates: `reddit_memes_subreddit` (another MulTaBench meme record from another source, screened in another batch). External collections: MulTaBench (core image-tabular).
- Better data: a candidate of the benchmark MulTaBench (not searched in this run, by its brief).
- Papers and pages: Kiela et al. 2020; the DrivenData challenge pages; MulTaBench (arXiv 2605.10616, Appendix B.1; Table 11: AUROC 0.745 frozen, 0.760 target-aware).
- Metric: "Model performance and leaderboard rankings will be determined using the AUC ROC" (DrivenData, evaluation page), accuracy shown for information; MulTaBench scores AUROC too.
- Risks for /add-dataset: not applicable; the dataset's own licence terms are no criterion (EV-4).
- Reject check (AI, 2026-10-31): stands. Kiela et al.: 'a new challenge set for multimodal classification, focusing on detecting hate speech in multimodal memes', 'constructed such that unimodal models struggle and only multimodal models can succeed' (https://arxiv.org/abs/2005.04790); MulTaBench's 20 structured columns are embedding dimensions of the caption, so no tabular attribute remains. The marker field carries both markers, as the block does.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 9,000 rows; 20 structured, 0 text, 1 image features (MulTaBench Table 3); target: Hateful (binary).
- Why: Flag a meme as hateful from its image and its (embedded) caption text
- Notes: Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. Kiela et al. NeurIPS 2020 (Facebook Hateful Memes Challenge). The 20 structured columns are pre-computed text embeddings of the caption, not tabular features; memes ...
