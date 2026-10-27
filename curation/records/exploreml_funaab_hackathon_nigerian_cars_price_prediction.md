---
unique_name: exploreml_funaab_hackathon_nigerian_cars_price_prediction
name: exploreml-funaab-hackathon-nigerian-cars-price-prediction
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2023'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/exploreml-funaab-hackathon-nigerian-cars-price-prediction
source_row: 979
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: an in-scope used-car price task, but a 16-participant campus hackathon with no stated data origin, and the benchmark already has several used-car price records.
- Source: Zindi "ExploreML FUNAAB Hackathon: Nigerian Cars Price Prediction" (Data Science Nigeria FUNAAB with GDSC FUNAAB), 2023-06-02 to 06-09, 16 participants. As published: Train, Test and `Variable_Description.csv`; features listed as "Make, Model, Year of Manufacture, Colour, Fuel, Transmission, Condition, Mileage, Engine Size, Selling Condition, Bought Condition"; target the price in Naira; the Data page says only "The data for this challenge is a tabular dataset". Rows not stated.
- Use case: the source: "This solution can help individuals and companies when trying to know the value of their vehicles before buying or selling on the market". Fit approximate (listing prices, not sale prices, is likely); regime IID unless listing dates ship.
- Siblings and duplicates: no other record of these Nigerian listings; the same task on other markets: `used_cars_24`, `used_cars_benz_italy`, `used_cars_dataset_cardekho`, `used_cars_pakistan`, `used_cars_saudi_arabia`, `cars`. The upstream (a scrape of a Nigerian listings site such as Cars45, Jiji or Autochek, or a Kaggle upload) was not found (PROV-2).
- Papers and pages: Zindi description and evaluation pages (read through the Zindi API); a 2025 University of Lagos paper on Nigerian car prices from online platforms (jer.unilag.edu.ng/article/view/2884) uses other data as far as its page shows.
- Metric: Zindi's Evaluation page: "The evaluation metric for this competition is Root Mean Squared Error" on the Naira price; a leaderboard metric (MET-4); inputs none.
- Risks for /add-dataset: the data's origin (PROV-2) and size; duplicates of a public scrape; `Selling Condition` and `Bought Condition` meaning; price outliers and currency scale (MET-3).
- Priority: gap 0 (business not thin), use case + (the source names individuals and companies valuing a car before buying or selling), source 0 (no data documentation), shape 0 (size unknown, about 11 mixed features), risk - (unknown origin, possible re-upload).

Zindi ExploreML/FUNAAB hackathon: predict the price of Nigerian used cars. This is a clear, genuine real-world tabular regression task (price prediction from vehicle attributes such as make, model, year, mileage), a good fit for the benchmark in the business domain, and an IID split is appropriate. The main risks are smallish hackathon size and listing-date leakage. A human must download the data to confirm the row count, the continuous price target, the feature set, and that no temporal/grouped split is required.
