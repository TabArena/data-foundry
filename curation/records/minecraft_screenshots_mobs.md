---
unique_name: minecraft_screenshots_mobs
name: Minecraft Mobs
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Image
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- AI-Filled (Verify)
collections:
- MulTaBench
source_links:
- https://doi.org/10.36227/techrxiv.174002528.84035428/v1
- https://www.kaggle.com/datasets/sqdartemy/minecraft-screenshots-dataset-with-features
- https://arxiv.org/abs/2605.10616
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Image`, `AHDS (Artifical/Handmade/Deterministic/Simulated)`, SEL-13): 6,089 Minecraft gameplay screenshots with a CSV of the game state shown in each; MulTaBench's target, the mob in the screenshot, is recognising an object in a picture of a video game, and the other columns describe the same picture.
- Source: Kaggle upload by sqdartemy, "Minecraft Screenshots Dataset with Features" (2024-11-22, CC BY-NC 4.0), "used for this paper: https://doi.org/10.36227/techrxiv.174002528.84035428/v1" (TechRxiv; not readable here, HTTP 403). As published: `features_and_decisions.csv`, 6,089 rows x 10 columns (`screenshot_title` such as "archering (100).png", `activity`, `hearts`, `light_lvl`, `in_hand_item`, `target_mob` and four `decision_*` columns) and the screenshots; `target_mob`: no_mob 2,508, other 1,349, skeleton 691, zombie 676, spider 383, ender 283, creeper 199. The page: "Minecraft gameplay screenshots accompanied by a detailed .csv file containing metadata and decision-making annotations for each image"; "The decision fields are derived from the input variables based on specific rules" (for example "creeper → go_back"). MulTaBench (extended, https://huggingface.co/datasets/multabench/extended-img-cls-minecraft) drops `decision_mob`, which restates the mob, and keeps the rest with the screenshot.
- Use case: none outside the game; the page names game AI, behaviour studies and teaching. No actor takes a real-world decision on the mob's identity.
- Siblings and duplicates: none (grep for minecraft and the Kaggle slug). Game-data precedents: `hs_cards_data` (`TBD -> 2nd Tier`, `AHDS`), `csgo_skin_price` (this run, `TBD -> 2nd Tier`, `AHDS`), `fifa` (`No`, `AHDS`). External collections: MulTaBench (extended image release).
- Better data: a candidate of the benchmark MulTaBench; no further search for this run's finds.
- Papers and pages: the Kaggle page; the TechRxiv preprint (not read); MulTaBench, Arazi et al. 2026 (https://arxiv.org/abs/2605.10616), Appendix F.1, Table 8 (structured AUC 0.940, image 0.957, joint 0.988), Table 9.
- Metric: not needed for a reject.
- Why `No`: SEL-13 (Must): the activity, hearts, light level and held item are read off the screenshot (the game's display shows them), and the target is the object it shows, so the inputs are descriptions of an image; SEL-16 (Must): a video-game world photographed by a player, with decisions from fixed rules, is handmade and simulated rather than a real random draw; USE-2: no decision outside the game. Unlike `hs_cards_data` and `csgo_skin_price`, kept as 2nd Tier for their game-designed attributes, the task here is recognising a picture.
- Reject check (AI, 2026-10-31): stands. The page: 'Minecraft gameplay screenshots accompanied by a detailed .csv file containing metadata and decision-making annotations for each image'; the inputs are 'observed game state variables' with coarse values (light_lvl 'high, mid, low') and target_mob is 'The type of mob the player is interacting with', i.e. annotations of what the screenshot shows (SEL-13), while 'The decision fields are derived from the input variables based on specific rules' (https://www.kaggle.com/datasets/sqdartemy/minecraft-screenshots-dataset-with-features). What sets it apart from hs_cards_data and pokemon_height: those rows are the designed game objects; these are one player's staged screenshots, and no decision outside the game fits.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 6,089 rows; 7 structured, 0 text, 1 image features (MulTaBench Table 9); target: Mob type (7 classes).
- Why: Identify the mob the player faces from a Minecraft screenshot and game state
- Notes: Extended release (admitted on Joint Signal only), not one of the 40 benchmark datasets. Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. Kaggle 2024 (CC BY-NC) with a TechRxiv preprint; game screenshots with ...
