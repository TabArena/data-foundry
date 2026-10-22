---
unique_name: airbnb
name: airbnb
checked_by:
- Lennart
- Mustafa
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- Free Text (Sentences)
- AI-Filled (Verify)
collections:
- TexTabBench
domain: business & marketing
problem_type: Regression
source_links:
- https://www.kaggle.com/datasets/airbnb/seattle
- https://insideairbnb.com/get-the-data/
- https://insideairbnb.com/get-the-data/
source_row: 15
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Assessment (AI, 2026-10-22):** recommend `TBD -> 2nd Tier` over the current `TBD -> Yes`, priority 2: a listing-price regression is possible, but the source defines no task, the curators rejected the sibling `melbourne_airbnb_open_data` for that reason, and the asking price is the host's choice with price-derived columns beside it; the curator has the call.
- Source: Inside Airbnb (insideairbnb.com, independent scrapes of Airbnb listings per city); the Kaggle copy "Seattle Airbnb Open Data" (airbnb/seattle, CC0, Kaggle dataset id 393) "is part of Airbnb Inside, and the original source can be found here" (Kaggle metadata, read 2026-10-22). As published: listings.csv (16.9 MB), calendar.csv (36.7 MB, listing id, price and availability per day), reviews.csv (36.6 MB, free-text comments); listing and calendar join on the listing id; row and column counts not verified here.
- Use case: none in the source: the Kaggle "Inspiration" asks for neighbourhood vibes, busy seasons and trends (exploration). A price suggestion for a new host at listing time is the candidate (the same framing as `mercari_price_suggestion`); fit approximate, since the target is the host's asking price, not a realised booking price; regime IID on one city snapshot, grouped by host when several listings share one, temporal when snapshots are combined.
- Siblings and duplicates: `melbourne_airbnb_open_data` (`No`, `No Good Target  / Scientific Discovery`, Lennart and Mustafa: "One of many https://insideairbnb.com/ datasets ... no predictive task connected so far"); this record's own human verdict was the same `No` before the AI re-opened it (git history, 2026-07-27). Any Inside Airbnb city is the same source at another place (PROV-6). External collections: TexTabBench (the record's tag; the task it uses was not checked).
- Papers and pages: Inside Airbnb data pages; the Kaggle dataset page.
- Metric: none found (the Kaggle page and Inside Airbnb define no task), so the fallback (rmse; a log target if the price is shipped log-scaled, MET-3).
- Risks for /add-dataset: price-derived columns (`weekly_price`, `monthly_price`, `cleaning_fee`, calendar prices) and post-listing columns (review counts and scores, availability) leak or are unknown at listing time (LEAK); free text dominates part of the signal; the target is a choice of the host (USE). Consistency: re-opening this record but not `melbourne_airbnb_open_data` treats two cuts of one source differently; settle both together.
- Priority: gap 0, use case 0 (written by the curation, not the source), source + (Inside Airbnb documents its scrape), shape + (thousands of listings, mixed types and text), risk - (price-derived and post-listing columns, a host-set target).

Re-opened for review (was `No`, reason `No Good Target / Scientific Discovery`). That reject only considered the **superhost** label, which is rule-based / deterministic — a poor target. But the insideairbnb / Kaggle listings carry a **nightly price** column, which supports a genuine **listing-price regression** task: predict a listing's price from its attributes (room type, location, capacity, amenities, review counts, free-text description, …). This is essentially the price-suggestion model Airbnb's own platform would build to recommend a price to a host — a *regression* task, **not** an out-of-scope ranking / RecSys task despite the informal 'price recommender' framing. To build / verify: construct the price target (strip currency symbols; consider **log-scaling** — nightly prices are heavy-tailed); confirm enough rows remain after cleaning; decide the split (likely IID on a single city snapshot, but watch for host-level **grouping** and for **temporal** structure if multiple insideairbnb snapshots are combined); and check that no column trivially leaks the price. Removed the `No Good Target` marker (the price target resolves it) and set `problem_type: Regression` on that basis.

Airbnb listings in Seattle (more to get from the reference)

There is also https://www.kaggle.com/datasets/airbnb/boston

I thought about predicting superhost but it seems to be a very clearly defined set of rules how to get it, so very deterministic?
