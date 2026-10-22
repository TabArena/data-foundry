---
unique_name: free_ai_classes_in_every_city_hackathon
name: free-ai-classes-in-every-city-hackathon
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2022'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/free-ai-classes-in-every-city-hackathon/data
- https://zindi.africa/competitions/free-ai-classes-in-every-city-hackathon
source_row: 990
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: real Nigerian used-car listings (7.2k rows) for a price regression, but the upstream listing site is unnamed and car-price siblings exist.
- Source: Zindi hackathon "FREE AI Classes In Every City Hackathon" (Data Science Nigeria, AI Invasion 2022, 2022-05-28 to 2022-07-03, access restricted, secret code); "There are ~7000 entries in Train and ~2000 entries in Test"; as published: Train 7,205 x 9 (`VehicleID`, `Location`, `Maker`, `Model`, `Year`, `Colour`, `Amount (Million Naira)`, `Type`, `Distance`), target `Amount (Million Naira)`, one table plus VariableDefinitions.csv (preview of a public GitHub copy of Train.csv). Three cities (Lagos, Abuja, Ibadan), 55 makers, 1,223 models, `Type` Foreign Used / Nigerian Used / Brand New, `Distance` 33% missing: the shape of scraped listings (the site is not named; PROV-2).
- Use case: a used-car platform ("Great Motors", the organiser's scenario) lists a car at a price from the mechanic's report; fit approximate (listing prices, a written scenario); regime IID, no listing date.
- Siblings and duplicates: `exploreml_funaab_hackathon_nigerian_cars_price_prediction` (DSN FUNAAB 2023, another column set: fuel, transmission, engine size, condition; a different table, no duplicate by the columns); other used-car price records (`used_cars_pakistan`, `used_cars_saudi_arabia`, `used_cars_24`, `used_cars_dataset_cardekho`, `used_cars_benz_italy`); `free_ai_classes_in_every_city_hackathon_2023` is a different task (house prices). External collections: none found.
- Papers and pages: https://zindi.africa/competitions/free-ai-classes-in-every-city-hackathon (Zindi API read 2026-10-22); public solution repositories on GitHub (top-solution notebooks), no paper.
- Metric: RMSE on `Amount (Million Naira)`, the Zindi Evaluation page ("The evaluation metric for this competition is Root Mean Squared Error"); deliberate leaderboard metric (MET-4); inputs none.
- Risks for /add-dataset: the scraping source and date are unknown (PROV-2); `Year` and `Distance` are strings with thousands separators; possible repeated listings of one car (PROV-4 within the table); heavy-tailed price (max 456 M Naira).
- Priority: gap 0 (business & marketing, IID not thin), use case 0 (organiser's scenario), source 0 (hackathon page only), shape + (7.2k rows, mixed types, high-cardinality model), risk 0.

Zindi hackathon dataset whose task is to predict car selling price, a standard real-world tabular regression problem with a clear target. Used-car price prediction is representative of tabular ML and a random split is appropriate. The main unknowns are dataset size after cleaning and whether the features are genuine (vs. a small/teaching hackathon set). Lean Yes pending verification of row count and that the data is not a trivial/synthetic re-upload.

---

predict car selling price
