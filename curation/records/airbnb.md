---
unique_name: airbnb
name: airbnb
checked_by:
- Lennart
- Mustafa
- AI (UNVERIFIED)
suggestion: TBD -> Yes
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

Re-opened for review (was `No`, reason `No Good Target / Scientific Discovery`). That reject only considered the **superhost** label, which is rule-based / deterministic — a poor target. But the insideairbnb / Kaggle listings carry a **nightly price** column, which supports a genuine **listing-price regression** task: predict a listing's price from its attributes (room type, location, capacity, amenities, review counts, free-text description, …). This is essentially the price-suggestion model Airbnb's own platform would build to recommend a price to a host — a *regression* task, **not** an out-of-scope ranking / RecSys task despite the informal 'price recommender' framing. To build / verify: construct the price target (strip currency symbols; consider **log-scaling** — nightly prices are heavy-tailed); confirm enough rows remain after cleaning; decide the split (likely IID on a single city snapshot, but watch for host-level **grouping** and for **temporal** structure if multiple insideairbnb snapshots are combined); and check that no column trivially leaks the price. Removed the `No Good Target` marker (the price target resolves it) and set `problem_type: Regression` on that basis.

Airbnb listings in Seattle (more to get from the reference)

There is also https://www.kaggle.com/datasets/airbnb/boston

I thought about predicting superhost but it seems to be a very clearly defined set of rules how to get it, so very deterministic?
