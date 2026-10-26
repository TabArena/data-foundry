---
unique_name: speoau_data_hackathon
name: speoau-data-hackathon
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Missing source information
- TBD
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2023'
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://zindi.africa/competitions/speoau-data-hackathon/data
source_row: 972
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: a 4-day private student hackathon (SPE OAU chapter, Nigeria, March 2023) to predict "the Actual Price of Electricity at a given time"; the data's origin is not named and the host frames it as price forecasting.
- Source: Zindi, https://zindi.africa/competitions/speoau-data-hackathon (read through the Zindi API on 2026-10-22), 9-12 March 2023, hosted for the Society of Petroleum Engineers OAU student chapter with Chemotronix, 46 participants; as published: Train.csv (5.1 MB), Test.csv (1.4 MB), Variable_description.csv; the test IDs start at ID_027500, so about 27,500 training rows. Columns not readable without a login; the page names no origin of the data.
- Use case: the page: "forecasting in energy markets is identified as one of the highest leverage contribution areas" and "By predicting demand and price in advance, energy companies can optimize their power generation". An actor (a utility or a trader) is named only in general; fit approximate. Regime temporal: a price series over time; whether it is a fixed task with ex-ante inputs (SEL-11) or forecasting of a series (SEL-10) depends on the columns, which could not be read.
- Siblings and duplicates: `speoau_energy_data_hackathon` (same host, 2024, solar PV output: a different task). The size and the column name "actual price" fit a re-upload of a public market-price table (for example the Irish SEM prices that circulate on Kaggle); unconfirmed, check by rows (PROV-4). External collections: none found.
- Papers and pages: none beyond the Zindi page.
- Metric: RMSE, the Zindi Evaluation page ("The error metric for this competition is the Root Mean Squared Error"); a leaderboard metric, deliberate (MET-4); inputs none.
- Risks for /add-dataset: SEL-10 against SEL-11 and TP-10 once the columns are seen (lagged prices as features would make it forecasting); the origin of the data (PROV-1, PROV-2; `Missing source information` kept as the open question); a likely re-upload.
- Priority: gap - (no thin value), use case - (generic), source - (origin not named), shape + (about 38,000 rows in all), risk - (forecasting framing, unknown origin).

A generic Zindi 'speoau-data-hackathon' with no description, comments, or fields in the record. Without any information on the target, features, modality, or size it cannot be assessed, and Zindi student hackathons vary widely (some are valid tabular tasks, others are forecasting/text/image). Per the heuristic, lack of information alone is not grounds for rejection. A human must open the Zindi page to determine the actual task, target, modality and dataset size before deciding.
