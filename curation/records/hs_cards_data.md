---
unique_name: hs_cards_data
name: HS_cards_data
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- No Good Target (yet)
tags:
- Free Text (Sentences)
- Larger IID Data
collections:
- TexTabBench
source_links:
- https://www.kaggle.com/datasets/jeradrose/hearthstone-cards?resource=download&select=cards_flat.csv
- https://hearthstonejson.com/
source_row: 476
type_adapter_id: curation-record-v1
---

## Comments

Card data extracted from the Hearthstone game, so actual original source is the game. Mapping card text and stats to player class

**Assessment (AI, 2026-10-31):** the benchmark MulTaBench (https://arxiv.org/abs/2605.10616) carries a related version, "Hearthstone Class", not this record's data, so no collection tag: Extended release (admitted on Joint Signal only), not one of the 40 benchmark datasets. Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. From the MuG benchmark (Lu et al. 2023). Closest record hs_cards_data has the same game cards and class target but from a text-only Kaggle release (jeradrose); MuG adds the card art.
