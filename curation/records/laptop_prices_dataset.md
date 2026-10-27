---
unique_name: laptop_prices_dataset
name: Laptop_Prices_Dataset
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- No Good Target / Scientific Discovery
tags:
- 2nd Tier / Scientific Discovery
- AI-Filled (Verify)
collections:
- TabArena Reject
original_source: Kaggle
year: '2023'
domain: technology & internet
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/talhabarkaatahmad/laptop-prices-dataset-october-2023
source_row: 815
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: a one-off scrape of Amazon laptop listings with a price target; real data, but no decision and messy text fields; follows the curators' call on `laptops`.
- Source: Kaggle upload by talhabarkaatahmad, 2023-10-09, "scraped from Amazon.com"; as published: about 4.5K listings x 14 columns (brand, model, screen size, colour, disk, CPU, RAM, OS, special features, graphics, CPU rating, rating, price in USD "as of October 2023"), one file `amazon_laptop_prices_v01.csv`, CC0.
- Use case: a seller or buyer judges a listing's price from its specification; nobody named in the source, fit approximate; regime IID (one snapshot).
- Siblings and duplicates: `laptops` (Lennart, Mustafa: `TBD -> 2nd Tier`, `No Good Target / Scientific Discovery`, another Kaggle scrape, "requires a lot of preprocessing to figure out a task") is the precedent; not the same rows. Other product-price records such as 1000_cameras (Lennart, 2nd Tier). External collections: none found.
- Papers and pages: the Kaggle page only (https://www.kaggle.com/datasets/talhabarkaatahmad/laptop-prices-dataset-october-2023).
- Metric: none found (Kaggle dataset page, no competition), so the fallback `rmse` (MET-1, MET-8).
- Risks for /add-dataset: repeated listings of the same model (the CC note), free-text fields (title-like model, special features) to parse (CLEAN, SEL-12), `rating` measured after listing. The old `Data Quality Issue` marker is dropped: no irreversible damage is shown; duplicates can be removed.
- Priority: gap - (technology & internet not thin), use case -, source - (an anonymous scrape with a data dictionary), shape + (4.5K rows, mixed types), risk - (duplicates and text parsing).

Roughly 4.5k crawled Amazon/Kaggle laptop listings from October 2023 where the nominal task is predicting price. As the curator notes, this is crawled e-commerce data likely with duplicate listings and is more of an analytics/outlier-detection exercise than a genuine predictive task, since price is largely defined by the observed spec features. Already tagged 2nd Tier / TabArena Reject. The data-quality concerns (dedup, scraping artifacts) and weak target make it a poor benchmark candidate. A human should confirm row count after dedup and whether any meaningful price-prediction signal survives, but on current evidence this is a No.

---

CC: "4.5k Amazon laptop listings. Crawled data. Predict price. Likely many duplicate listings and other weird stuff. Also not necessarily a meaningful task - maybe for finding outliers/unreasonable prices?"

## Reference

Kaggle
