---
unique_name: golf_play_dataset_extended
name: golf_play_dataset_extended
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- 2nd Tier / Scientific Discovery
- Non-IID (Temporal)
- AI-Filled (Verify)
collections:
- TabArena Reject
domain: handcrafted/toy
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/samybaladram/golf-play-extended
source_row: 847
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Assessment (AI, 2026-10-22):** the `No` (TabArena workbook reject, the CC above) holds: the uploader made the table for teaching, so it is handmade data (SEL-16, PROV-3), and no decision is named (USE-1). The curator has the call.
- Source: Kaggle `samybaladram/golf-play-extended`, uploaded 2023-11-03 by Samy Baladram, CC BY 4.0; the card: "designed to extend the classic golf dataset" and "especially useful for teaching because it offers many small datasets within it, each one created for a different learning purpose"; no origin of the rows is named. As published: `golf_dataset_long_format_with_text.csv` (1.6 MB) with Outlook, Temperature, Humidity, Windy, Play (target, Yes/No), ID, Date, Weekday, Holiday, Season, Crowded-ness, PlayTime-Hour and the text columns Review, EmailCampaign, MaintenanceTasks, plus mini files built for exercises (`golf_dataset_mini_dirty.csv`, `..._lotsofmissingvalues.csv`, `..._allcategorical.csv`).
- Use case: none from the source ("Learning With This Dataset" lists teaching skills); the CC's reading (did someone play on a given day) would need a temporal split, but nothing says the rows were observed.
- Siblings and duplicates: none among the records; the classic 14-row golf/weather table and its Kaggle re-uploads (`priy998/golf-play-dataset`, `davorbudimir/golf-play`) have no records. External collections: none found.
- Metric: none (no task).
- Risks: the tags `2nd Tier / Scientific Discovery` and `Non-IID (Temporal)` do not fit a `No`; left for the curator.
- Priority: none (verdict `No`).

Extended version of the classic 'play golf' teaching dataset, already in the TabArena Reject collection. The author describes it as a teaching tool made of many small handmade datasets, not an actual predictive task. It is artificial/handmade/toy data and tiny, so it fails the representativeness criterion. Confidently No.

---

CC: ""This dataset is especially useful for teaching because it offers many small datasets within it, each one created for a different learning purpose." - not an actual predictive task. But still predicting whether on a certain day golf was played could be done. Likely not a predictive task. And if yes, temporal split would be required"

## Reference

Kaggle
