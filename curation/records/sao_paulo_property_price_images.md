---
unique_name: sao_paulo_property_price_images
name: Sao Paulo Apartments
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
collections:
- MulTaBench
original_source: Kaggle
year: '2024'
domain: business & marketing
problem_type: Regression
source_links:
- https://www.kaggle.com/datasets/rogerio/image-based-property-price-prediction-in-so-paulo
- https://arxiv.org/abs/2605.10616
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: 23,433 São Paulo properties for sale in April 2024 with about 30 listing attributes and the asking price; a real tabular price task once the photos are dropped, but an individual's scrape of an unnamed portal, and the benchmark already holds many house-price tasks.
- Source: Kaggle upload by `rogerio`, "Image-Based Property Price Prediction in São Paulo" (CC BY-NC-SA 4.0, last updated 2024-10-28): "data from 23,433 properties for sale in the city of São Paulo (Brazil) advertised during April 2024. The data includes the price, over 30 property characteristics (m2, number of bedrooms, garage, etc.) and images of the listings, for a total of 407,567 images"; "More information will be added soon." The portal is not named. As processed by MulTaBench (App. F.1; Hugging Face `multabench/extended-img-reg-sao-paulo-houses`): 23,432 rows; listing date, featured flag, property category and type, floor area, bedrooms, bathrooms, parking spaces, zone, 19 amenity flags, the neighbourhood as text and one photo; target the price; MulTaBench translated the Portuguese headers and dropped the previous price, the condominium fee and the property tax.
- Use case: a seller, agent or portal prices a listed property from its attributes; the source names no actor, so the fit is approximate (asking prices on one portal, not sale prices); regime IID likely (one month of listings), but the listing date ships, so whether a temporal split is possible is checked once the dates are seen (SPLIT-6, SPLIT-7).
- Siblings and duplicates: no record of this upload (grep by slug, title, "São Paulo"). Related: `sao_paulo_itbi_transactions` (the city's registry of declared sale values, a candidate of this run; another target, a transaction value rather than an asking price), `goiania_apartment_prices` (a MulTaBench sibling: Goiânia listings with a photo), `brazilian_houses` (Lennart, `TBD -> 2nd Tier`: rental ads without a timestamp, "there might be better house price datasets"). External collections: MulTaBench, extended release (admitted on Joint Signal only), as "Sao Paulo Apartments".
- Better data: a candidate of the benchmark MulTaBench (the run searched no further).
- Papers and pages: MulTaBench (Arazi et al. 2026, arXiv 2605.10616, App. F.1); no paper on the data found.
- Metric: none found (the Kaggle page states no task or metric; MulTaBench scores R² min-max normalised to average over datasets, Sec. 3, a benchmark convention rather than the task's), so the fallback `rmse`, with the price modelled on a log scale (MET-3, MET-8).
- Risks for /add-dataset: the photos go (an image embedding would be image-derived features, SEL-13); the previous price is close to a copy of the target (LEAK-10, check); the condominium fee and property tax are known at listing time and stay (USE-6), whatever MulTaBench did; the same unit listed by several agencies would sit on both sides of a split (check for repeated units); the portal and its terms are unknown (PROV-2); the raw Portuguese table was not seen.
- Priority: gap 0 (business & marketing, regression and IID are well covered), use case 0 (none named), source 0 (an individual's upload, portal unnamed), shape + (23,432 rows, about 30 mixed features and a listing date).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 23,432 rows; 28 structured, 1 text, 1 image features (MulTaBench Table 9); target: Asking price.
- Why: Predict a Sao Paulo property's asking price from listing attributes and a photo
- Notes: Extended release (admitted on Joint Signal only), not one of the 40 benchmark datasets. Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. Listings advertised April 2024 (Kaggle, CC BY-NC-SA).
