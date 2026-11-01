---
unique_name: csgo_skin_price
name: CS:GO Skins
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- No Good Target (yet)
tags:
- Tiny Data
- AI-Filled (Verify)
collections:
- MulTaBench
original_source: Other
year: '2023'
source_links:
- https://arxiv.org/abs/2302.02978
- https://figshare.com/articles/dataset/21454413
- https://arxiv.org/abs/2605.10616
- https://github.com/lujiaying/MUG-Bench
- https://huggingface.co/datasets/multabench/core-img-cls-csgo-skin
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: 956 Counter-Strike weapon skins scraped from a fan database for the MuG benchmark, whose own task was the rarity tier the game assigns; MulTaBench made a target of the scraped price range, cut into deciles. Game-designed attributes and no decision, as in `hs_cards_data`.
- Source: MuG, Lu, Qian, Zhao, Xi and Yang, "MuG: A Multimodal Classification Benchmark on Game Data with Tabular, Textual, and Visual Fields", Findings of EMNLP 2023 (https://arxiv.org/abs/2302.02978, first version 2023-02-06); data on figshare (file `CSGO-Skin-quality.zip`) and https://github.com/lujiaying/MUG-Bench. The paper: "CS:GO data is collected from https://www.csgodatabase.com/", gathered by October 2022; 956 skins (766 train, 49 validation, 141 test), tabular `id`, `availability`, `skinCategory`, `minPrice`, `maxPrice`, text `skinName`, an image; target "the skin quality according to its rarity" (6 classes). As used by MulTaBench (core image-tabular; https://huggingface.co/datasets/multabench/core-img-cls-csgo-skin): `Skin Name`, `Skin Quality`, `Availability`, `Skin Category`, the image, target `Price_Category`, "10 equal-frequency bins" of the market price (Appendix D.2).
- Use case: none in either source. The rarity tier is set by the game's maker, so no one predicts it; the market price could serve a trader valuing a new skin, but neither source names one; fit none to approximate. Regime IID (one snapshot of the database).
- Siblings and duplicates: none (grep over the records for csgo, cs:go, counter-strike, the figshare id). Game-data siblings: `hs_cards_data` (`TBD -> 2nd Tier` with `AHDS` and `No Good Target (yet)`, checked by Lennart; its note: "Card data extracted from the Hearthstone game, so actual original source is the game"), `pokemon_height` and `minecraft_screenshots_mobs` (this run). External collections: MuG (as `csg_sq`), MulTaBench (core image-tabular).
- Better data: a candidate of the benchmark MulTaBench; no further search for this run's finds.
- Papers and pages: Lu et al. 2023 (Table 1 and the appendix, read through the arXiv HTML); MulTaBench (https://arxiv.org/abs/2605.10616), Table 3, Appendix D.2, Table 11 (no significant task-aware gain from the image, 0.871 against 0.870).
- Metric: for the price none found (MulTaBench's AUROC on its own bins is benchmark-wide, MET-5; MuG's metric for its rarity task not read), so the fallback `rmse` on the price, log-scaled and scored on the price scale (MET-3); which of `minPrice` and `maxPrice` is the target is open.
- Risks for /add-dataset: the target is MulTaBench's, not a source's (TP-7); game-designed attributes (`AHDS`, as read for `hs_cards_data`; SEL-16); 956 rows (`Tiny Data`); the price is a fan site's market snapshot (PROV-2); without the image (SEL-12) three columns and the name remain.
- Priority: gap 0, use case 0, source + (a peer-reviewed benchmark paper documents the scrape), shape 0 (956 rows, three columns besides the name), risk - (no task, designed attributes, a benchmark-made target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 956 rows; 3 structured, 1 text, 1 image features (MulTaBench Table 3); target: Market price in 10 equal-frequency bins.
- Why: Predict the market price band of a Counter-Strike weapon skin from its image, name and rarity metadata
- Notes: Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. Target binned by MulTaBench, not the source's own target. From the MuG benchmark (Lu et al., EMNLP Findings 2023; figshare 21454413, CC BY-NC-SA), whose own task was ...
