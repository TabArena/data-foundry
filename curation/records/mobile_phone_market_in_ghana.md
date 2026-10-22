---
unique_name: mobile_phone_market_in_ghana
name: Mobile_Phone_Market_in_Ghana
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- No Good Target  / Scientific Discovery
- TBD
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- TabArena Reject
year: '2024'
domain: technology & internet
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/redpen12/mobile-phone-market-in-ghana
source_row: 816
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: phone listings scraped from an unnamed Ghanaian website with specifications, region and price in cedis; a price regression is possible, but the source is an untraced scrape and the uploader frames it as market analysis.
- Source: Kaggle, "Mobile Phone Market in Ghana" by redpen12, one file Mobile-Phones.csv (493 KB, created 2023-10-18), CC0 (https://www.kaggle.com/datasets/redpen12/mobile-phone-market-in-ghana, metadata read with the Kaggle CLI): "The data was collected through web scraping"; described columns: brand and model, SD card, main camera, resolution, display, SIM, operating system, colour, region and location, screen size, battery, storage, RAM, selfie camera, price. The scraped site, the scrape date and whether a row is a listing or a catalogue model are not stated. Rows not counted. The record's year 2024 is unconfirmed (the file dates from October 2023).
- Use case: none stated ("It can be used for market analysis, consumer insights, and decision-making related to mobile phone purchases"); one we could write is a seller pricing a listing on a classifieds site (fit approximate, our wording). Regime IID if the rows are listings from one scrape.
- Siblings and duplicates: none among the records (searched ghana, mobile phone); TabArena v0.1 put it on its reject list (collection `TabArena Reject`; CC: "Simply scraped from a website. Predict the price - more for analysis and insights than for predictive performance"). External collections: none found.
- Papers and pages: none; the Kaggle keywords are "exploratory data analysis", "data cleaning", "gradient boosting".
- Metric: none found (the Kaggle page; no competition, task or paper), so the fallback (rmse; the price likely on a log scale, MET-3).
- Risks for /add-dataset: the first platform of the scrape (PROV-2, approximate fit at best); repeated listings of one model; the CC's concern that the price is set by model and storage (TP-4 to probe); the date and currency of the prices.
- Markers: `Data Quality Issue` dropped (no irreparable damage is documented: that marker needs an undone supervised transform or a manipulated table); `No Good Target  / Scientific Discovery` kept as the curator's concern.
- Priority: gap 0 (technology & internet has 5 accepted), use case 0 (none stated), source 0 (an anonymous scrape), shape 0 (size not counted, mixed types), risk - (untraced source, a possibly near-trivial price).

Scraped Kaggle data on phone models in Ghana with the nominal task of predicting price. As the curator notes, this is web-scraped data better suited to analysis/insights than predictive performance, where price is largely determined by the observed spec features, making it a weak/circular target. It is already in TabArena Reject. The scraping data-quality and weak-target concerns make it a poor benchmark candidate. On current evidence this is a No.

---

CC: "Data about phone models in Ghana. Simply scraped from a website. Predict the price - more for analysis and insights than for predictive performance; again a task where one might not be able to predict the price or the price is defined when the other variables are observed"

## Reference

Kaggle
