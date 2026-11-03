---
unique_name: pokemon_height
name: Pokemon Height
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- No Good Target (yet)
tags:
- AI-Filled (Verify)
collections:
- MulTaBench
year: '2024'
source_links:
- https://www.kaggle.com/datasets/divyanshusingh369/complete-pokemon-library-32k-images-and-csv
- https://arxiv.org/abs/2605.10616
- '# upstream of the CSV''s values (Kaggle page: ''All data and images are collected from the PokémonDB database'')'
- https://pokemondb.net/pokedex/all
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: about a thousand Pokémon entries with the games' designed attributes, scraped from PokémonDB, with no task in the source; MulTaBench made a target of the height in deciles. Kept as second tier on the precedent of `hs_cards_data`, with the call between it and `fifa_players` left to the curator (Consistency check below).
- Proposed reject (refuted): `No` (`AHDS (Artifical/Handmade/Deterministic/Simulated)`, SEL-16; USE-2): every value is set by the games' designers and copied from PokémonDB, so the data is handmade, and a height decile serves no decision. Reject check (AI, 2026-10-31): refuted. SEL-16's "handmade" applied to designed game entries is a call the curator has made both ways: `hs_cards_data` (Lennart, `TBD -> 2nd Tier` with `AHDS` and `No Good Target (yet)`: "actual original source is the game") against `fifa_players` and `football_manager_important_matches` (`No`, `AHDS`). No fact sets Pokémon apart from Hearthstone cards: both are the designed objects themselves, with a designed attribute as target. A precedent with the same facts is followed unless a fact sets the case apart (principles.md), so `No` is the curator's call, not a clear Must failure.
- Source: Kaggle "Dataset of 32000 Pokemon Images & CSV, JSON" by `divyanshusingh369` (files dated 2024-03-28, Apache 2.0): "All data and images are collected from the PokémonDB database" (https://pokemondb.net/pokedex/all), "The images are sourced from Google"; a CSV and a JSON with name, type, species, height, weight, abilities, EV yield, catch rate, base friendship, base exp, growth rate, egg groups, gender, egg cycles and base stats, plus about 32,000 sprites. The page names no task. As used by MulTaBench (extended release, App. F.1): 1,077 rows, 27 structured, 4 text and 1 image features (Table 9); "The 10-class target is the height decile, obtained after capping height at 10 meters"; structured features "the base, minimum, and maximum battle statistics together with weight, catch rate, base friendship and experience, growth rate, egg groups, and gender ratio".
- Use case: none in either source; no actor decides on a Pokémon's height outside the game (USE-1 open). Regime IID as one snapshot of the Pokédex; forms and evolution lines of one species share stats, a grouping to check.
- Siblings and duplicates: no Pokémon record (grep for pokemon, pokémon, the Kaggle slug). Game-data precedents: `hs_cards_data` (Lennart, `TBD -> 2nd Tier`), `csgo_skin_price` (this run, `TBD -> 2nd Tier`, priority 1), `minecraft_screenshots_mobs` (this run, `No`, SEL-13: screenshots, not the objects), `fifa_players` (Lennart and Mustafa, `No`, `AHDS`), `football_manager_important_matches` (Lennart, `No`, `AHDS`), `fifa` (`No`, `AHDS`, `Duplicate`). External collections: MulTaBench, extended release, as "Pokemon Height" (Table 8: structured AUC 0.849, image 0.709, joint 0.853).
- Better data: a candidate of the benchmark MulTaBench; no further search this round.
- Papers and pages: the Kaggle page (read through the Kaggle API's dataset metadata); PokémonDB; MulTaBench (Arazi et al. 2026, https://arxiv.org/abs/2605.10616), App. F.1, Tables 8 and 9.
- Metric: none found (the Kaggle page names no task; MulTaBench's AUC is its benchmark-wide convention, MET-5), so the fallback, `rmse` on the height if it ships as the source's number.
- Risks for /add-dataset: a use case (USE-1), or the record goes; the height as the source's number rather than MulTaBench's decile (TP-7); the minimum and maximum stats, which follow from the base stats by the games' stat formula (SEL-5, drop); about 1,000 rows (the CSV's own count not checked; MulTaBench keeps 1,077); the sprite dropped (SEL-12).
- Priority: gap 0, use case 0 (none), source 0 (a Kaggle scrape of a fan database), shape + (about 1,000 entries, some 20 game fields of mixed types), risk - (designed attributes, no task, a benchmark-made target).

**Consistency check (AI, 2026-10-31):** designed game data has been decided both ways: `hs_cards_data` kept as `TBD -> 2nd Tier` with `AHDS` (Lennart) against `fifa_players` and `football_manager_important_matches` rejected with `AHDS` (Lennart; Mustafa on `fifa_players`). This record and `csgo_skin_price` follow `hs_cards_data` for now. What sets them apart? (a) The AI's best guess: FIFA and Football Manager ratings stand in for real players, while Hearthstone cards, Pokémon and skins are the designed objects themselves; keep this record as second tier on that fact. (b) Reject this record like `fifa_players`, and reopen `hs_cards_data` and `csgo_skin_price` to match. (c) Amend SEL-16 to say which game data counts as handmade.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 1,077 rows; 27 structured, 4 text, 1 image features (MulTaBench Table 9); target: Height decile, capped at 10 m (10 classes).
- Why: Predict a Pokemon's height band from its sprite and game statistics
- Notes: Extended release (admitted on Joint Signal only), not one of the 40 benchmark datasets. Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. Target binned by MulTaBench, not the source's own target. Designed game data ...
