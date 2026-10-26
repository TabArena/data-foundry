---
unique_name: dsn_free_ai_classes_in_every_city_2025
name: dsn-free-ai-classes-in-every-city-2025
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Missing source information
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2025'
required_split:
- '?'
problem_type: Regression
source_links:
- https://zindi.africa/competitions/dsn-free-ai-classes-in-every-city-2025/data
source_row: 945
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: a 2025 re-run of DSN's 2020 "Excellent Store Challenge" (same three files, same byte sizes), whose columns map one to one onto the Big Mart sales practice data under new names; the store chain is a teaching scenario.
- Source: first published as the Zindi hackathon "DSN Pre-Bootcamp Hackathon: The Excellent Store Challenge" by Data Science Nigeria, 8-22 Aug 2020 (https://zindi.africa/hackathons/dsn-pre-bootcamp-hackathon-the-excellent-store-challenge); this record's competition (2-29 Jun 2025) names it as its parent in Zindi's API, and its train.csv (651,526 bytes), test.csv (432,867) and SampleSubmission.csv (84,802) match the 2020 files byte for byte in size. The record's `year` 2025 is the re-run, PROV-9 would give 2020. As published: one table per product and store, `Item_ID, Item_Weight, Item_Sugar_Content, Item_Visibility, Item_Type, Item_Price, Store_ID, Store_Start_Year, Store_Size, Store_Location_Type, Store_Type, Item_Store_ID`, target `Item_Store_Returns` ("profit returns on the product in the particular store"); about 1,500 products in 10 stores. Rows not counted (login, secret code).
- Use case: the page's CEO of "Impact Stores" (2020: "Babatunji Stores") wants to know which products and store types return more profit before expanding; a fictional scenario of a training bootcamp, fit approximate at best; regime unclear (IID over item-store pairs, or grouped by store for the expansion question, with only 10 stores).
- Siblings and duplicates: no record of the 2020 hackathon or of Big Mart Sales; the Big Mart practice problem (Analytics Vidhya, "2013 sales data for 1559 products across 10 stores", target `Item_Outlet_Sales`) has the same columns (Item_Fat_Content -> Item_Sugar_Content, Item_MRP -> Item_Price, Outlet_* -> Store_*); if confirmed, this is Big Mart renamed and its target relabelled from sales to "profit returns" (PROV-3, PROV-4). Big Mart itself has no documented first source.
- Papers and pages: no paper; the Zindi tabs (read through the page API); no public solution read.
- Metric: RMSE ("The evaluation metric for this challenge is Root Mean Squared Error", Evaluation tab); MET-4; inputs none.
- Risks for /add-dataset: confirm or refute the Big Mart match on the rows (PROV-3, a reworked table is `Data Quality Issue`; PROV-4); the target's meaning; the split (store-grouped with 10 stores is thin).
- Priority: gap 0 (business & marketing), use case 0 (a teaching scenario), source - (a likely renamed copy of an undocumented practice set), shape + (mixed types, item x store structure), risk - (PROV-3).


Zindi 'DSN Free AI Classes in Every City 2025' competition, but the record carries no description, comments, or metadata beyond the link. Data Science Nigeria competitions are typically genuine tabular supervised tasks, so the prior is favorable, but there is too little information here to judge target, modality, size, or split. Per the heuristics, lack of record detail alone is not grounds for rejection. A human must open the competition page/data to determine the task type, target, problem domain, and appropriate split.
