---
unique_name: spanish_wine_quality_dataset
name: Spanish Wine Quality Dataset
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- No Good Target  / Scientific Discovery
- Not Representative
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Kaggle
year: '2022'
domain: Other
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/fedesoriano/spanish-wine-quality-dataset/data
source_row: 833
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: a scraped list of Spanish red wines with the average user rating as target; 5,452 of 7,500 rows are exact duplicates and the ratings start at 4.2, so a selected sample with no named decision.
- Source: Kaggle upload by fedesoriano, April 2022 (citation request on the page), "collected by me using web scraping from different sources (from wine specialized pages to supermarkets)", the sources not named; as published: one CSV `wines_SPA.csv`, 7,500 x 11 (winery, wine, year, rating, num_reviews, country, region, price, type, body, acidity). Preview of 2026-10-22: 5,452 exact duplicate rows (about 2,048 unique), `type` missing in 545 rows, `body` and `acidity` in 1,169; rating takes only 4.2 to 4.9 (4.2 in 5,679 rows).
- Use case: the page says "predict either the quality of wine or the prices", with no actor; a retailer pricing a wine, or a buyer screening one, is our reading (approximate fit). The rating is an aggregate of app users' scores, and the 4.2 floor says the scrape kept only top-rated wines (`Not Representative`). Regime IID (one row per wine and vintage; a grouped split by winery is worth a look).
- Siblings and duplicates: `winevivino` (Lennart, `TBD -> 2nd Tier`, "Wine in Spain", a different Kaggle scrape of Vivino) may overlap: body and acidity scores of 1-5 are Vivino's fields, so check by rows before adding; `wine_quality` (Cortez et al., physicochemical tests) is a different task. The old `Duplicate` marker named no original, so it is dropped (PROV-4 needs one). External collections: none found.
- Papers and pages: https://www.kaggle.com/datasets/fedesoriano/spanish-wine-quality-dataset ; no paper.
- Metric: none found (the Kaggle page names "classification or regression tasks" only), so the fallback `rmse` for the rating.
- Risks for /add-dataset: deduplicate first (PROV-13); `num_reviews` and `rating` are scraped at one date (a later state than a new wine's listing); with price as target, the rating is a consequence of the same listing; winery and wine names are high-cardinality strings.
- Priority: gap - (no thin domain), use case - (none named), source - (unnamed scraped sources), shape + (about 2,000 unique rows, mixed types), risk - (73% duplicate rows, a truncated target).

A Kaggle 'Spanish Wine Quality' dataset (fedesoriano) with attributes such as winery, region, type, price and a quality/rating column. The curator already flagged it as likely a duplicate of the many wine datasets and questionable as a real predictive task; quality ratings here are aggregated review scores rather than a natural deployment target. It is a plausible small tabular regression but overlaps heavily with the well-known wine-quality family and is tagged 2nd-tier/scientific-discovery. A human should verify uniqueness vs other wine datasets, the true target (quality vs price), and size after cleaning.

---

Likely a duplicate with other wine datasets and anyhow not a real predictive task?
