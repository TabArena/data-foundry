---
unique_name: mercari_japan_item_prices
name: Mercari Japanese Item Sales Dataset
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- AI-Filled (Verify)
original_source: Kaggle
domain: business & marketing
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/hyamamoto2000/mercari-jp-dataset
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: about 867,700 items sold on Mercari Japan, scraped by one Kaggle user and laid out like the 2017 Price Suggestion Challenge; the task of the shipped `mercari_price_suggestion`, with a date and a seller id, but a private scrape, Japanese text as the main signal, and sellers the card says can be found again.
- Source: Kaggle user hyamamoto2000, "Mercari Japanese Dataset" (dataset id 4874371; one file `items.tsv`, 721 MB, current version 2026-10-20; licence "other", "Non-commercial use only"): "List of sold items on Mercari Japanese website", "Source: In-house web scraper via official web interface", "about 867,700 (one item per row)"; columns id, is_shop, name, item_description, price ("Listed price (yen)"), brand_name, item_condition, shipping, shipping_from_area, shipping_duration, seller_id, category_name, updated_date ("Last updated date (rounded by 4 hours)"). "intentionally structured similar to that of the official Price Suggestion Challenge ... held 7 years ago", so first uploaded about 2024 (the creation date was not shown). Kaggle is the first publication (PROV-8), the uploader is identifiable, the scrape's window and selection are not stated (PROV-2).
- Use case: Mercari suggests a price to a seller when an item is listed (the 2017 competition's framing); fit approximate: this card names "price prediction" without an actor, and a scrape of sold items may differ from the listings a suggestion serves (USE-8). Regime temporal by `updated_date` or grouped by `seller_id` (SPLIT-3).
- Siblings and duplicates: `mercari_price_suggestion` (`Yes`, BeyondArena; the 2017 competition, about 1.48M listings, RMSLE): the same task from another source (PROV-4), not a duplicate; `airbnb`, `amazon_bestseller_price` and `painting_price` only mention Mercari. External collections: none found.
- Better data: found as better data for `mercari_price_suggestion`; no further search this round.
- Papers and pages: the Kaggle card only; no paper or competition uses this data.
- Metric: none found for this data (Kaggle card), so the fallback `rmse`, or the sibling competition's RMSLE on the yen price if the curator treats the two as one task (MET-3, MET-4); not decided here.
- Risks for /add-dataset: the signal is mostly Japanese free text (`name`, `item_description`; SEL-12 judged per dataset, as on the sibling); "Sellers and items are obfuscated but still identifiable by manually searching it on the original website" (card), and whether the scrape respected the site's terms is not stated (SEL-1 to weigh, not a fast reject); `updated_date` is the last update, not the listing or sale date (SPLIT-7); the data was not previewed (721 MB).
- Priority: gap 0 (regression and business are not thin), use case 0 (not named for this data), source 0 (a single uploader's scrape), shape + (867,700 rows, text, categorical and numeric, a date and a seller id), risk - (re-identifiable sellers, a text-led task already in the benchmark).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `mercari_price_suggestion`.
- as published: about 867,700 sold items x 13 columns (id, is_shop, name, item_description, price in yen, brand_name, item_condition, shipping, shipping_from_area, shipping_duration, seller_id, category_name, ...; target: price (yen) of an item sold on Mercari; access: open (non-commercial, educational use).
- Why: The card says it is 'intentionally structured similar to that of the official Price Suggestion Challenge' with the same text, brand, condition, category and shipping columns; same platform and target.
- Adds: Newer data with a date, a seller id and a shop flag, so a temporal or seller-grouped split is possible (the record notes it is 'likely temporal'), and two more shipping features. Fewer rows than the 1.48M of 2017, Japanese text, a single uploader's scrape, non-commercial licence ('other').
