---
unique_name: laptop_prices_dataset
name: Laptop_Prices_Dataset
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
- Data Quality Issue
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- TabArena Reject
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

Roughly 4.5k crawled Amazon/Kaggle laptop listings from October 2023 where the nominal task is predicting price. As the curator notes, this is crawled e-commerce data likely with duplicate listings and is more of an analytics/outlier-detection exercise than a genuine predictive task, since price is largely defined by the observed spec features. Already tagged 2nd Tier / TabArena Reject. The data-quality concerns (dedup, scraping artifacts) and weak target make it a poor benchmark candidate. A human should confirm row count after dedup and whether any meaningful price-prediction signal survives, but on current evidence this is a No.

---

CC: "4.5k Amazon laptop listings. Crawled data. Predict price. Likely many duplicate listings and other weird stuff. Also not necessarily a meaningful task - maybe for finding outliers/unreasonable prices?"

## Reference

Kaggle
