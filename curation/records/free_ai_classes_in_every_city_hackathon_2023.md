---
unique_name: free_ai_classes_in_every_city_hackathon_2023
name: free-ai-classes-in-every-city-hackathon-2023
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2023'
required_split:
- '?'
problem_type: TBD
source_links:
- https://zindi.africa/competitions/free-ai-classes-in-every-city-hackathon-2023/data
source_row: 984
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`AHDS (Artifical/Handmade/Deterministic/Simulated)`, SEL-16, PROV-3): the "Wazobia Real Estate" house-price table is generated: rows spread evenly over Nigeria's 36 states and nine house types, prices with fractions of a Naira, and about 13% missing values injected in every column.
- Source: Zindi hackathon "DSN and Microsoft Skills for Job" (slug free-ai-classes-in-every-city-hackathon-2023, Data Scientists Network with Microsoft, 2023-06-12 to 2023-08-06); "Can you accurately predict the prices of houses in Nigeria"; "There are ~7000 entries in Train and ~3000 entries in Test" (the data description still names the car task of 2022); files Housing_dataset_train.csv, Housing_dataset_test.csv; Wazobia Real Estate Limited is the scenario's company, no data source named.
- Deciding evidence (a preview of Housing_dataset_train.csv from a public participant repository, github.com/FelixFrankFelix/DSN-MICROSOFT-HACKATHON, not the source's words): 14,000 x 7 (`ID`, `loc`, `title`, `bedroom`, `bathroom`, `parking_space`, `price`); each of the 36 states holds 302 to 370 rows; nine titles hold 1,266 to 1,372 rows each (Cottage 450); `price` has three decimals (1149999.565) and only 0.08% whole numbers; every feature is missing in 12.3% to 12.9% of the rows; a five-bedroom detached duplex in Anambra lists at 2.41 M Naira (median 1.9 M), far below the market.
- Metric: RMSE (Zindi Evaluation page).
- If the checker finds this rests on a reading: `TBD -> 2nd Tier`, priority 1 (gap 0, use case 0, source 0, shape +, risk - for PROV-3).
- Reject check (AI, 2026-10-22): stands. SEL-16 / PROV-3 (Must), on measured marks, not page words (EV-2: a measurement outranks the page). I re-measured the public copy of Housing_dataset_train.csv (github.com/FelixFrankFelix/DSN-MICROSOFT-HACKATHON, Data/). It has 14,000 rows. Test 4 (marginals too even): 36 states with 302-370 rows each, including Lagos. Bedrooms 1-5 have about 1,740 rows each and 6-9 about 880 each, a step-uniform shape. Parking 1-4 have about 2,370 each and 5-6 about 1,335 each. Test 6 (structure the world would show): bathrooms are independent of bedrooms, so a 1-bedroom has 7 bathrooms as often as a 4-bedroom does. Prices have 3 decimals (0.08% whole numbers) and a mansion's median is 3.6M Naira. Missingness was injected: 12.3-13% per column, 7,731 rows have exactly one NaN and only 580 have two or more, and the column-wise missingness correlates at -0.10. A plain log-linear model on the complete rows gives R^2 0.93. That is several calibrated marks from at least two tests, which meets PROV-3 as amended 2026-10-21. The Zindi page names no data source: "Wazobia Real Estate Limited" is a scenario, and the Data Description still describes the 2022 car task. https://zindi.africa/competitions/free-ai-classes-in-every-city-hackathon-2023

Zindi hackathon dataset from the same series as free_ai_classes_in_every_city_hackathon but with no comments or task description in the record. The sibling 2022/earlier edition was a car-price regression task, so this is plausibly a similar real tabular predictive problem, but the actual target is unknown. Do not reject for lack of info alone. A human must open the competition page to confirm the target, problem type, split regime, and dataset size before a final verdict.
