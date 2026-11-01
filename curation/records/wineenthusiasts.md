---
unique_name: wineenthusiasts
name: WineEnthusiasts
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
decision_markers:
- No Good Target (yet)
- Ethical Issue
tags:
- Many class
- Free Text (Sentences)
- Non-IID (Temporal)
collections:
- TabSTAR
- CARTE/TARTE
original_source: Kaggle
year: '2020'
source_links:
- https://www.kaggle.com/datasets/manyregression/updated-wine-enthusiast-review
- winemag and Kaggle
source_row: 514
type_adapter_id: curation-record-v1
---

## Comments

A dataset that is based on another dataset, contains description and sentences, but also contains names and Twitter handles of reviewers (so PII and thus an ethical problem). Could likely be fixed. Still unclear if this is a real predictive task (more so causal inference)

Grouped data based on the reviewer. Temporal based on time of review. Spatial because of origin of the wine

**Assessment (AI, 2026-10-31):** the benchmark MulTaBench (https://arxiv.org/abs/2605.10616) carries a related version, "Wine Review", not this record's data, so no collection tag: Text-tabular; AutoML Multimodal wine_reviews (OpenML 46653, from the zynicide Kaggle scrape of winemag.com). The record wineenthusiasts covers the same Wine Enthusiast reviews through a later Kaggle snapshot (manyregression); check whether it is the same release.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `wine_reviews_winemag_130k` (TBD -> 2nd Tier, priority 1). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-01):** MulTaBench's "Wine Review" is the record `wine_reviews_winemag_130k`, which carries the MulTaBench tag.
