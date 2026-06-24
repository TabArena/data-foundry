---
unique_name: used_cars_benz_italy
name: Used Cars Benz Italy
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
decision_markers:
- Missing source information
tags:
- New IID
- Free Text (Short)
- AI-Filled (Verify)
collections:
- CARTE/TARTE
domain: business & marketing
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/bogdansorin/second-hand-mercedes-benz-registered-2000-2023-ita
source_row: 867
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Second-hand Mercedes-Benz listings registered 2000-2023 in Italy (Kaggle), a valid tabular price-regression task with short free-text/categorical fields useful for feature engineering. The main risks noted are that it may duplicate other Mercedes-Benz used-car datasets and that the scraping source is not fully documented. A human must check for overlap/duplication with other used-car records, confirm the price target and size, and verify the data is genuinely scraped real listings before final acceptance.

---

used mercedes data

Maybe duplicate with other Mercedes Benz datasets? Likely scraped from some website from Italy. Otherwise a valid task
