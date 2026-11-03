---
unique_name: mkphoto2023_bots
name: MkPhoto Bots
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
- https://link.springer.com/article/10.1007/s13278-023-01038-3
- https://www.kaggle.com/datasets/guardeec/mkphoto2023
- https://arxiv.org/abs/2605.10616
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`No Good Target / Scientific Discovery`, `Image`, SEL-3): MKPHOTO2023 was published "to research the types of profile photos used by different types of malicious social bots"; MulTaBench's target, a Turing-test trust score, is a property of the bot offer that every bot of the offer shares (65 values over 13,748 rows), and the per-photo inputs are outputs of image detectors.
- Source: Kolomeets, Wu, Shi & van Moorsel, "The Face of Deception: The Impact of AI-Generated Photos on Malicious Social Bots", IEEE Trans. Comput. Soc. Syst. (online 2024-10-09, doi:10.1109/TCSS.2024.3461328), data on Kaggle guardeec/mkphoto2023 (files of 2024-05-18, MIT), with bot metrics from MKMETRIC2022 (Kolomeets & Chechulin, "Social bot metrics", Soc. Netw. Anal. Min. 13:36, 2023, doi:10.1007/s13278-023-01038-3). As published: `dataset.csv`, 13,748 rows x 13 columns (`id`, `gan`, `dtm`, `person`, `n_faces`, `celebs`, `dataset` = the bot offer, `TrustNZ_IDNNZ`, `SR`, `price`, `BTT`, `speed`, `NBQ`), the raw detector outputs and the profile photos. The page: "For this classification, we utilized various detectors" (YOLO, a celebrity detector, GAN and diffusion detectors). The MKMETRIC2022 README (https://github.com/guardeec/datasets): "bots from the same bot offer have the same metrics"; Trust is "6 variations of Trust measure that reflect how well users recognize the bot", from a Turing test.
- Measured on the published `dataset.csv`: `TrustNZ_IDNNZ` is constant within each of the 65 offers (1 to 4,388 rows per offer); the offer-level inputs `BTT`, `speed` and `NBQ` form 11 combinations that narrow the offer down.
- Use case: none; the paper's aim is "a qualitative comparison of these bots using metrics such as price, survival rate, quality, speed, and human trust" (abstract), a study looking back. MulTaBench (core, https://huggingface.co/datasets/multabench/core-img-reg-mkphoto-bots) keeps `gan`, `dtm`, `person`, `n_faces`, `celebs`, `BTT`, `speed`, `NBQ` and the photo.
- Siblings and duplicates: none (grep for mkphoto, vkontakte, social bot and the Kaggle slug); `twitter_bots_accounts` (this run, bot or human accounts) is another task. External collections: MulTaBench (core image set).
- Better data: a candidate of the benchmark MulTaBench; no further search for this run's finds.
- Papers and pages: the TCSS paper (abstract read; the open copy at doi:10.25405/ncl.34508847 not read); the SNAM paper (closed access, not read); MulTaBench, Arazi et al. 2026 (https://arxiv.org/abs/2605.10616), Appendix B.1, Table 3 (13,748 rows; 8 structured, 1 image), Table 11 (frozen R² 0.341, task-aware 0.361).
- Metric: not needed for a reject.
- Why `No`: SEL-3 (Must) with USE-2: a table published for a comparison of bot types, whose target is an offer-level score that no decision acts on per photo; the per-row inputs are detector outputs on the photo (SEL-13), and the offer-level inputs identify groups of offers, so a model learns the offer rather than the bot.
- Reject check (AI, 2026-10-31): stands. The page: 'designed to research the types of profile photos used by different types of malicious social bots', with the per-photo columns made by 'various detectors' (YOLO, CelebDetector, GAN and DTM detectors) and the bot metrics added from MKMETRIC2022 (https://www.kaggle.com/datasets/guardeec/mkphoto2023), where 'bots from the same bot offer have the same metrics'. The trust target has 65 values over 13,748 rows (screener's count), so every non-image column is offer-level and no re-target leaves a tabular task.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 13,748 rows; 8 structured, 0 text, 1 image features (MulTaBench Table 3); target: Trust score (estimated probability the post is genuine).
- Why: Predict a trust score of a VKontakte profile photo from the photo and detector outputs
- Notes: Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. MKPHOTO2023 (Kaggle 2024, MIT), photos used by VKontakte bots; first publication taken from the Kaggle page's paper link, not checked. Several features (GAN, deepfake, ...
