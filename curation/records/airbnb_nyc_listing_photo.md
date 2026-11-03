---
unique_name: airbnb_nyc_listing_photo
name: Airbnb NYC
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
collections:
- MulTaBench
original_source: Website
domain: business & marketing
problem_type: Regression
source_links:
- https://insideairbnb.com/get-the-data/
- https://www.kaggle.com/datasets/dominoweir/inside-airbnb-nyc
- https://arxiv.org/abs/2605.10616
- https://huggingface.co/datasets/multabench/extended-img-reg-airbnb-nyc
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: a third Inside Airbnb city next to `airbnb` (Seattle) and `melbourne_airbnb_open_data` (`No`); the tabular columns carry the signal (MulTaBench Table 8: structured R² 0.701, photo and text 0.309, joint 0.721), so the photo can be dropped, but no source defines a task and at most one Inside Airbnb city should enter.
- Source: Inside Airbnb (insideairbnb.com), per-city scrapes of Airbnb listings with a data dictionary, CC BY 4.0; the Kaggle copy dominoweir/inside-airbnb-nyc ("Inside AirBnB: NYC", files created 2022-09-09, source http://insideairbnb.com/get-the-data) holds one New York snapshot: `listings.csv`, a detailed `listings 2.csv` (89 MB), `reviews.csv`, `reviews 2.csv`, `neighbourhoods.csv`. Its description: "Inside Airbnb is a mission driven project that provides data and advocacy about Airbnb's impact on residential communities." As used by MulTaBench (extended release, admitted on Joint Signal only; https://huggingface.co/datasets/multabench/extended-img-reg-airbnb-nyc): 16,780 listings, 46 structured and 3 text columns (host, property and room type, capacity, minimum and maximum nights, availability, review counts and scores, host listing counts), the primary listing photo, target `price` (nightly); host prose, scrape ids and coordinates dropped.
- Use case: none in the source (advocacy and exploration). The candidate is a price suggestion for a host at listing time, as for `airbnb`; fit approximate: the target is the host's asking price, and the review, availability and host-count columns describe the listing after it went live. Regime IID on one snapshot, or grouped by host (`calculated_host_listings_count` shows multi-listing hosts); temporal only if several snapshots are combined.
- Siblings and duplicates: no duplicate by rows (grep over the records for airbnb, insideairbnb, the Kaggle slug). Siblings of the same source and task in other cities: `airbnb` (Seattle, Kaggle airbnb/seattle; `TBD -> Yes`, with an AI assessment of 2026-10-22 recommending 2nd Tier) and `melbourne_airbnb_open_data` (`No`, `No Good Target / Scientific Discovery`, checked by Lennart and Mustafa; its note: "One of many https://insideairbnb.com/ datasets", "no predictive task connected so far"). Cuts of one source with the same task are duplicates unless one adds a task (PROV-6), so the curator picks one city at most; New York is the largest of the three. External collections: MulTaBench (extended image release; it also carries Seattle and Melbourne as text sets).
- Better data: a candidate of the benchmark MulTaBench; no further search for this run's finds. Inside Airbnb itself publishes newer New York snapshots than the 2022 Kaggle copy (a version of the same source, PROV-6).
- Papers and pages: the Inside Airbnb get-the-data page and data dictionary; the Kaggle page; MulTaBench, Arazi et al. 2026 (https://arxiv.org/abs/2605.10616), Table 8 and the dataset description of the extended release.
- Metric: none found (the Kaggle page and Inside Airbnb define no task; MulTaBench reports R² for every regression set, a benchmark-wide choice, not one for this task, MET-5), so the fallback `rmse`, with the price shipped on a log scale and scored in dollars (MET-3); inputs none.
- Risks for /add-dataset: review counts and scores, `reviews_per_month`, `first_review`, `last_review` and the availability windows are not known when a host lists (LEAK-10, USE-3); the target is the host's own choice (USE-5); price outliers; grouping by host (SPLIT-1); the three Inside Airbnb records should be settled together (the `melbourne_airbnb_open_data` `No` against the re-opened `airbnb`); the photo is dropped (SEL-12).
- Priority: gap 0 (business & marketing has 25 accepted datasets, regression is not thin), use case 0 (written by the curation, not the source), source + (Inside Airbnb documents its scrape and columns), shape + (16,780 listings, 49 mixed columns), risk - (no source task, post-listing columns, a version of `airbnb`).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 16,780 rows; 46 structured, 3 text, 1 image features (MulTaBench Table 9); target: Nightly price.
- Why: Predict a New York Airbnb listing's nightly price from listing data and main photo
- Notes: Extended release (admitted on Joint Signal only), not one of the 40 benchmark datasets. Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. Inside Airbnb NYC snapshot (Kaggle 2022, CC BY). Sibling records: airbnb ...
