---
unique_name: dpreview_camera_specifications_price
name: DP Review Product Database
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- No Good Target (yet)
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
original_source: Kaggle
year: '2023'
domain: technology & internet
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://www.kaggle.com/datasets/alvations/dpreview
- https://www.dpreview.com/products
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: a 2023 scrape of DPReview's product database (over 1,700 cameras and 450 lenses with full specifications) whose launch price could serve the spec-to-price task of `1000_cameras`; the uploader poses no task, the price field is unchecked, and spec-to-price scrapes have gone to the second tier.
- Source: Kaggle "DP Review Product Database" by alvations (dataset 3036552, files of 2023-03-23, licence "unknown"; metadata read through the API): scraped with Selenium because DPReview was to close on 10 April 2023, quoting the site: "Our extensive product database holds full specifications for over 1700 digital cameras and over 450 lenses"; main file `dpreview.jsonl` with the parsed specifications, plus one HTML spec page per product (about 139 MB in all). Kaggle is the source under PROV-8 (the table first appeared there; dpreview.com is where the content comes from). The jsonl was not opened: whether each camera has an MSRP, and in which currency and kit, is unchecked.
- Use case: a manufacturer or retailer prices a new camera from its specification at announcement; the source names none; fit approximate (a list price at launch, not adjusted over 25 years); regime temporal by announcement date (`1000_cameras` CC: "if yes, then with temporal split").
- Siblings and duplicates: `1000_cameras` (TBD -> 2nd Tier, `No Good Target (yet)`; CC: "Probably not a predictive task"); the spec-to-price precedents `gsmarena_phone_specifications_price`, `laptop_prices_dataset` and `mobile_phone_market_in_ghana` (TBD -> 2nd Tier, priority 1) and `laptops` (the curator's TBD -> 2nd Tier). No duplicate (grep dpreview, camera). External collections: none found.
- Better data: found as better data for `1000_cameras`; no further search this round.
- Papers and pages: the Kaggle page and the uploader's two notebooks (how to use it, how it was created); no paper.
- Metric: none found (the Kaggle description poses no task), so `rmsle` on the price from the context, as for the house prices (MET-11); inputs none.
- Risks for /add-dataset: the price field (presence, currency, body only or kit) is unchecked, an unclear target (USE-5); lenses and phones mixed with cameras; specifications as strings to parse; the announcement date to parse for the split; licence unknown (EV-4, noted only).
- Priority: gap 0 (technology & internet, regression not thin), use case 0 (none named), source 0 (an individual's scrape without field documentation), shape + (over 1,700 cameras, mixed fields), risk - (an unclear price target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `1000_cameras`.
- as published: spec pages of over 1,700 digital cameras and over 450 lenses (plus phones), one dpreview.jsonl with the parsed specifications and one file per product; 139 MB; target: launch price of a camera (DPReview's MSRP field on the spec page; presence per row not checked) from its specifications and announcement date; access: open.
- Why: the record's task (camera price from sensor, resolution, zoom, weight, dimensions, release year) with the same kind of spec features, from a traceable specialist publisher
- Adds: about 1.6 times the cameras and 16 more years (mirrorless era to 2023) than the 1,038 cameras of 1994-2007; the record's No Good Target concern stays, and the precedent for spec-to-price scrapes is 2nd Tier (gsmarena_phone_specifications_price, laptop_prices_dataset); Kaggle licence Unknown
