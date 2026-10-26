---
unique_name: ai4d_lab_tanzania_tourism_classification_challenge
name: ai4d-lab-tanzania-tourism-classification-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2022'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/ai4d-lab-tanzania-tourism-classification-challenge/data
- https://zindi.africa/competitions/tanzania-tourism-prediction-challenge
source_row: 901
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 4: a 24,675-row NBS tourist-expenditure survey classified into six cost bins, with a stated actor and a log-loss leaderboard.
- Source: Zindi competition "AI4D Africa's Anglophone Research Lab Tanzania Tourism Classification Challenge", 2022-06-01 to 2022-07-01, 522 participants (Zindi API, read 2026-10-22); "The dataset describes 24,675 rows of up-to-date information on tourist expenditure collected by the National Bureau of Statistics (NBS) in Tanzania", from an exit survey at seven departure points. As published: Train.csv, Test.csv ("6,169 rows"), VariableDefinitions.csv; target six classes (Low, Lower, Normal, High, Higher, Highest Cost). An earlier cut of the same NBS survey was the Pycon Tanzania hackathon "Tanzania Tourism Prediction Challenge" (2020-12-12, 6,476 rows, regression on `total_cost`, MAE), the second link.
- Use case: "The model can be used by different tour operators and the Tanzania Tourism Board to automatically help tourists across the world estimate their expenditure before visiting Tanzania" (Zindi description); fit approximate: the survey is answered at departure, so trip-plan columns (party size, nights, package items) are known before the trip, while any spending or in-trip answers are not; regime IID (one survey cross-section, no date column known), so the `Non-IID (Temporal)` tag needs a check against the columns.
- Siblings and duplicates: `mmu_2022` (`TBD -> Yes`) is the same competition re-hosted on 2022-11-25 ("Tanzania Tourism Classification Challenge", same 24,675 rows, same log loss): a duplicate of this record (PROV-4); the 2020 regression cut has no record. External collections: none found.
- Papers and pages: the Zindi pages; NBS International Visitors' Exit Survey reports (not read).
- Metric: log loss over the six classes (Zindi Evaluation page: "The evaluation metric for this challenge is the Log Loss"); a leaderboard metric (MET-4); inputs none.
- Risks for /add-dataset: columns answered after the trip (LEAK); the bins come from `total_cost` (whether the cut points are stated, and whether the regression framing is the better task); the 2020 6,476-row cut overlaps (PROV-6); the regime tag versus `Random (IID)`.
- Priority: gap 0 (business, multiclass and IID are not thin), use case + (tour operators and the Tourism Board named), source + (NBS survey, variable definitions), shape + (24,675 rows, mixed survey columns), risk 0.

Predict the range (bins) of expenditure a tourist spends in Tanzania; the record specifies using the 2022 multiclass version with ~24,675 rows. This is a genuine real-world tabular classification task with a clear, meaningful target and adequate size. The record carries a Temporal tag, so the split regime needs confirmation (it may simply be the year of collection rather than a true temporal dependency, in which case an IID split fits). A human must verify the row count, the number/definition of expenditure bins, and whether a temporal or random split is appropriate.

---

predict the range of expenditures a tourist spends in Tanzania

One challenge used the cost as a regression task on 2020 data with 6476 rows, the other as multi-class classification on bins with 2022 data with 24675 rows. We would use the second dataset
