---
unique_name: water_potability_classification_hackathon_by_indabax_nigeria_2021
name: Water Potability Classification Hackathon by IndabaX Nigeria 2021
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2021'
domain: environmental science & climate
required_split:
- '?'
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/indabax-nigeria-2021/data
source_row: 1005
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Duplicate`, `AHDS (Artifical/Handmade/Deterministic/Simulated)`, PROV-4, SEL-16): the IndabaX Nigeria 2021 hackathon serves the synthetic Kaggle "water potability" file, split into train and test.
- Source: Zindi "Water Potability Classification Hackathon", IndabaX Nigeria 2021, 16 to 23 Sept 2021 (https://zindi.africa/competitions/indabax-nigeria-2021, read through Zindi's API): "The train contains 2260 rows and the test 1016" (3,276 together, the row count of Kaggle `adityakadiwal/water-potability`); the variable descriptions are the Kaggle card's text word for word, including "The current investigation ranges were 6.52–6.83 which are in the range of WHO standards" (pH, Hardness, Solids, Chloramines, Sulfate, Conductivity, ...). The framing story ("You have been contracted by Water Corporation in Nigeria") is the hackathon's; no Nigerian sampling is described.
- Siblings and duplicates: `water_quality_and_potability` (`No`, `Missing source information` and `AHDS`; CC 2026-10-22, Lennart): the Kaggle first upload's source field reads "Synthetically generated", TDS is 50 times the conductivity, and 1,277 of 1,278 "potable" rows exceed the WHO TDS maximum.
- Metric: F1 (Zindi Evaluation page), moot.
- Not checked: the files (login); the match rests on the row count and the verbatim data card.
- Reject check (AI, 2026-10-22): stands. Zindi Data page (https://zindi.africa/competitions/indabax-nigeria-2021, api.zindi.world, read 2026-10-22): "The train contains 2260 rows and the test 1016" (3,276 = Kaggle adityakadiwal/water-potability) and the variable text is that Kaggle card verbatim ("The current investigation ranges were 6.52-6.83 ..."); no Nigerian sampling is described, the 'Water Corporation' framing is the hackathon's. The first upload's source field reads "Synthetically generated" (record water_quality_and_potability, CC 2026-10-22 Lennart: keep No with AHDS). PROV-4 + SEL-16, both Must.

A Zindi / IndabaX Nigeria 2021 hackathon to classify whether water is potable from physico-chemical measurements — a binary classification task. The key risk is that many 'water potability' datasets (notably the popular Kaggle one) are synthetic/imaginary, so provenance must be checked; if this reuses such synthetic data it should be rejected, but if it is genuine measurements it could qualify. A human must verify the data source/realness, dataset size, class balance, and whether it duplicates the synthetic water_quality dataset before deciding, so a provisional 2nd-tier hold is appropriate.

---

predict if water is potable or not
