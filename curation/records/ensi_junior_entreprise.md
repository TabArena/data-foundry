---
unique_name: ensi_junior_entreprise
name: ensi-junior-entreprise
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Time-series (Regression)
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2021'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/ensi-junior-entreprise
source_row: 1002
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: daily temperature per weather station from only the date, a station id and normalised coordinates; a spatial interpolation of a reading stream with three inputs, from a one-day student hackathon that does not name its data source.
- Source: Zindi private hackathon "ENSI Junior Entreprise" (Hack'prise event of the ENSI student association with Infor Tunisia, 14 Jul 2021, https://zindi.africa/competitions/ensi-junior-entreprise); as published: Train.csv "1,449,100 rows and 5 columns" (`Date, LOC_ID, X, Y, TEMP`), Test.csv 391,661 rows without `TEMP`; "3 years of data, for each day"; values such as 79.8 in September and 15.2 in January suggest degrees Fahrenheit (a US station network?); the provider is not named (PROV-2).
- Use case: the page motivates weather for retail demand, but the task is "predict weather temperature at any location given by its X and Y coordinates": no actor acts on a station's past temperature; fit approximate at best; regime: grouped by station if the test holds new locations, temporal if new dates; the page does not say which (the record's `Grouped (NON-IID)` is an AI guess, kept).
- Siblings and duplicates: none found in `curation/records/`; external collections: none.
- Papers and pages: the competition tabs (read through Zindi's API); no paper, no solution read.
- Metric: RMSE ("The error metric for this challenge is Root Mean Squared Error", Evaluation tab); MET-4; inputs none.
- Risks for /add-dataset: three inputs (date, X, Y) plus an id: the task is a smoother over space and season (TP-4 risk); a station's other days in training make it near-trivial under a random split; the unnamed origin (PROV-2); `Needs extensive data wrangling` dropped (one table as published).
- Priority: gap 0 (environmental science), use case 0, source 0 (a student hackathon, data origin unnamed), shape 0 (1.4M rows but three features), risk - (thin features, unclear split), floored at 1.


Zindi ENSI Junior Entreprise competition: predict weather temperature at a location given its X/Y coordinates. This is essentially a spatial-interpolation regression task whose covariates may be little more than coordinates, which risks being thin/not representative of general tabular ML and would need a spatial (grouped) split to avoid leakage. It is a real predictive target, so not an outright reject. A human must inspect the actual feature set (whether richer covariates exist beyond coordinates), the sample size, and the spatial split requirement before deciding.

---

Predict weather temperature at any location given by its X and Y coordinates
