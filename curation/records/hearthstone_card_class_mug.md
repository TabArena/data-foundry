---
unique_name: hearthstone_card_class_mug
name: Hearthstone card class (MuG)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- No Good Target (yet)
tags:
- AI-Filled (Verify)
collections:
- MulTaBench
original_source: Other
year: '2023'
problem_type: Multiclass Classification
source_links:
- https://arxiv.org/abs/2302.02978
- https://figshare.com/articles/dataset/21454413
- https://huggingface.co/datasets/multabench/extended-img-cls-hearthstone-class
- https://arxiv.org/abs/2605.10616
- https://github.com/lujiaying/MUG-Bench
- '# upstream of MuG''s Hearthstone data (MuG: ''Hearthstone data is collected from https://hearthstonejson.com/'')'
- https://hearthstonejson.com/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-01):** `TBD -> 2nd Tier`, priority 3: the Hearthstone card database as MuG collected it from HearthstoneJSON in 2022, with a card's hero class as target. It has the same origin and target as `hs_cards_data` (an older HearthstoneJSON extract without art), so at most one of the two enters (PROV-6), and like it this is designed game data whose class no one predicts (`hs_cards_data`, `csgo_skin_price`, `pokemon_height`).
- Source: MuG, Lu, Qian, Zhao, Xi and Yang, "MuG: A Multimodal Classification Benchmark on Game Data with Tabular, Textual, and Visual Fields", Findings of EMNLP 2023 (https://arxiv.org/abs/2302.02978; data on figshare 21454413 and https://github.com/lujiaying/MUG-Bench): "Hearthstone data is collected from https://hearthstonejson.com/" (CC0), "gathered from publicly accessible web content by October 2022"; task hs_ac, the class of all cards, 14 classes, 8,569/536/1,605 cards for train/validation/test, 12 tabular fields (health, attack, cost, type, rarity, collectible, spellSchool, race, durability, overload, spellDamage, set), 5 text fields (name, id, artist, text, mechanics) and an image. As used by MulTaBench (extended image-tabular release, https://huggingface.co/datasets/multabench/extended-img-cls-hearthstone-class): 4,281 rows, target `cardClass` (11 classes), 15 columns and an image path; how 10,710 cards became 4,281 is not stated in what was read.
- Use case: none in either source. Blizzard's designers set a card's class when they make it, so no one predicts it (USE-1 open); fit none. Regime IID (one snapshot of the card database); reprints and tokens of one card share text and stats, a grouping to check.
- Siblings and duplicates: `hs_cards_data` (Lennart, `TBD -> 2nd Tier` with `AHDS` and `No Good Target (yet)`: "Card data extracted from the Hearthstone game, so actual original source is the game") links Kaggle jeradrose/hearthstone-cards, whose page says "The data in this dataset was extracted from hearthstonejson.com": the same origin and target, so this record is a newer version of that dataset with card art added (PROV-4, PROV-6), and the curator picks at most one. MuG's other Hearthstone tasks (set, minion race, spell school) are other targets on the same cards. Game-data precedents: `csgo_skin_price` (MuG, `TBD -> 2nd Tier`, priority 1), `pokemon_height` (`TBD -> 2nd Tier`, priority 1, an `AHDS` reject refuted on the `hs_cards_data` precedent), `fifa_players` and `football_manager_important_matches` (`No`, `AHDS`). External collections: MuG (hs_ac), MulTaBench (extended release, "Hearthstone Class": AUROC 0.905 structured, 0.812 image, 0.914 joint); MulTaBench's curation tables also list a text-tabular "Hearthstone Cards".
- Better data: a candidate of the benchmark MulTaBench; no further search this round.
- Papers and pages: MuG (Table 1 and the data section, read through the arXiv HTML); HearthstoneJSON (https://hearthstonejson.com/); MulTaBench (https://arxiv.org/abs/2605.10616), App. F.1.
- Metric: MuG reports two metrics for every task ("We choose the log-loss and accuracy to evaluate model performance"), and MulTaBench's AUROC is benchmark-wide (MET-5), so the fallback `log_loss`; inputs none.
- Risks for /add-dataset: designed attributes (`AHDS`, SEL-16, as read for `hs_cards_data`) and no decision (USE-1); the image is dropped (SEL-12), and whether it is the bare art or a rendered card with its class frame was not checked; `text` and `mechanics` name class-specific keywords and `id` and `set` may encode the class (to check); which version enters, this one or `hs_cards_data` (PROV-6).
- Priority: gap + (multiclass thin), use case 0 (none), source + (the MuG paper documents the collection; HearthstoneJSON documents the fields), shape + (4,281 cards here, 10,710 in MuG; numeric, categorical and text), risk - (designed attributes with no decision; one of two versions).

**Assessment (AI, 2026-11-01):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616) as "Hearthstone Class"; split out on 2026-11-01 from the note on `hs_cards_data`, a text-only release of the same cards.
- as published: 4,281 rows; 11 structured, 4 text, 1 image features (MulTaBench Table 9); target: Card class (11 classes).
- Why: Predict a Hearthstone card's hero class from card art, stats and rules text
- Notes: Extended release (admitted on Joint Signal only), not one of the 40 benchmark datasets. Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. From the MuG benchmark (Lu et al. 2023). Closest record hs_cards_data has the same game cards and class target but from a text-only Kaggle release (jeradrose); MuG adds the card art. Designed game data.
